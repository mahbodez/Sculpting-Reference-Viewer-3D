"""The path tracer's integrator: what one sample of one pixel sees.

A path leaves the camera and at each surface it meets does two things:

* next-event estimation -- it aims a shadow ray at every light (the key, the
  fill and a point of the HDRI picked by its brightness) and adds what gets
  through, weighed against the chance that the bounce would have found the
  same light (the power heuristic);
* it bounces, picking a direction from the surface's scattering, and carries
  on, until it leaves the scene, runs out of bounces or loses at Russian
  roulette.  A bounce that escapes adds the sky, and the HDRI and the lights
  weighed the other way round.

Human Skin adds three things a path may do at the skin that a plain surface
cannot (see :mod:`refview.trace.skin`): enter it and leave it again nearby,
at the point a Burley-distributed probe finds (subsurface scattering); pass
through it, to leave on the far side attenuated by the thickness crossed
(the backlight); and catch the light at a grazing rim (the vellus fuzz).  The
light arriving where the scattered light entered is always estimated, as the
viewport's refinement does, since that is most of what skin looks like.

Everything here is a numba kernel.  :func:`render_tile` renders a rectangle
of pixels over a range of sample indices into the film's sums; tiles never
share a pixel, so the render threads need no locks.
"""

from __future__ import annotations

import math

import numpy as np

from .camera import camera_ray, filter_offset
from .geometry import (
    CAP_HIT,
    MISS,
    STACK_SIZE,
    cap_normal,
    intersect,
    occluded,
    offset_origin,
    safe_normalize,
    surface,
)
from .jit import device, kernel
from .lights import (
    disc_hit,
    disc_sample,
    env_background,
    env_pdf,
    env_radiance,
    env_sample,
    power_heuristic,
    sky_radiance,
)
from .materials import (
    MAT_BASE,
    MAT_KIND,
    MAT_ROUGHNESS,
    MAT_SKIN,
    ggx_eval,
    ggx_sample,
    material_alpha,
    principled_eval,
    principled_sample,
)
from .sampler import (
    DIM_BSDF,
    DIM_CAMERA,
    DIM_ENV,
    DIM_LIGHT,
    DIM_SUBSURFACE,
    bounce_set,
    hash_combine,
    pixel_seed,
    sample4,
)
from .skin import (
    FLUSH,
    SK_FUZZ,
    SK_INDIRECT,
    SK_RADIUS,
    SK_SCATTER,
    SK_SPECULAR,
    SK_SSS,
    SK_TRANSMISSION,
    burley_pdf,
    diffusion_lengths,
    skin_closure,
    skin_fresnel,
)
from .vec import (
    INV_PI,
    TWO_PI,
    basis,
    cosine_hemisphere,
    dot,
    luminance,
    to_local,
    to_world,
)

#: The oil's own lobe: a thin film of sebum is far smoother than the skin under it.
OIL_ROUGHNESS = 0.18


@device
def _clamped(c, limit):
    if limit <= 0.0:
        return c
    m = max(c[0], max(c[1], c[2]))
    if m <= limit:
        return c
    k = limit / m
    return (c[0] * k, c[1] * k, c[2] * k)


@device
def _add(acc, t, c, k, limit):
    """``acc + clamp(t * c * k)``."""
    v = _clamped((t[0] * c[0] * k, t[1] * c[1] * k, t[2] * c[2] * k), limit)
    return (acc[0] + v[0], acc[1] + v[1], acc[2] + v[2])


@device
def _skin_spec(wo_l, wi_l, roughness, oil, specular):
    """The two-lobe skin specular, ``f cos``, and its mixture density, in the spec frame."""
    a1 = max(roughness * roughness, 1e-4)
    a2 = OIL_ROUGHNESS * OIL_ROUGHNESS
    v1, p1, cos_oh = ggx_eval(wo_l, wi_l, a1)
    v2, p2, _c = ggx_eval(wo_l, wi_l, a2)
    if cos_oh <= 0.0 and v1 <= 0.0 and v2 <= 0.0:
        return 0.0, 0.0
    f = skin_fresnel(specular, cos_oh)
    return f * ((1.0 - oil) * v1 + oil * v2), (1.0 - oil) * p1 + oil * p2


@device
def _thickness(geo, sh, p, ng, d, radius, blood, vessel, seed, stack, stack_t):
    """Where a ray into the skin along ``d`` leaves it again, and what survives the crossing.

    Returns ``(found, exit point, exit normal, carried)``; the exit must be
    skin facing out along the ray within twelve radii, as in the viewport.
    """
    o = offset_origin(p, (-ng[0], -ng[1], -ng[2]), geo.radius)
    tri, t, u, v = intersect(geo, o, d, radius * 12.0, seed, stack, stack_t)
    if tri < 0:
        return False, p, ng, (0.0, 0.0, 0.0)
    if sh.materials[geo.material[tri], MAT_KIND] != MAT_SKIN:
        return False, p, ng, (0.0, 0.0, 0.0)
    ng_raw, ns_raw = surface(geo, tri, u, v)
    n_hit = safe_normalize(ns_raw, safe_normalize(ng_raw, (0.0, 0.0, 1.0)))
    if dot(n_hit, d) <= 0.05:
        return False, p, ng, (0.0, 0.0, 0.0)
    sk = sh.skin
    eps = sk[23]
    k = 1.0 + 0.35 * blood + 0.9 * vessel
    carried = (
        math.exp(-t * k / max(radius * sk[SK_SCATTER], eps)),
        math.exp(-t * k / max(radius * sk[SK_SCATTER + 1], eps)),
        math.exp(-t * k / max(radius * sk[SK_SCATTER + 2], eps)),
    )
    g = safe_normalize(ng_raw, n_hit)
    if dot(g, d) < 0.0:
        g = (-g[0], -g[1], -g[2])
    exit_point = (o[0] + d[0] * t, o[1] + d[1] * t, o[2] + d[2] * t)
    return True, exit_point, g, carried


@device
def _probe(geo, sh, p, ng, n, lengths, radius, ua, ub, uc, seed, stack, stack_t):
    """Where the light that leaves at ``p`` entered: one Burley-distributed probe.

    Returns ``(entry, entry normal, per-channel weight)``; with no skin found
    the entry is ``p`` itself, as the viewport falls back to.
    """
    channel = min(int(ua * 3.0), 2)
    reach = 1.0 if ub < 0.25 else 3.0
    d_c = lengths[channel]
    r = -math.log(max(1.0 - uc, 1e-5)) * d_c * reach
    # The angle reuses the low bits the channel and reach picks leave unused.
    phi = TWO_PI * ((ub * 4.0) % 1.0)
    height = max(3.0 * radius, r)
    t_axis, s_axis = basis(ng)
    lx = r * math.cos(phi)
    ly = r * math.sin(phi)
    o = (p[0] + t_axis[0] * lx + s_axis[0] * ly + ng[0] * height,
         p[1] + t_axis[1] * lx + s_axis[1] * ly + ng[1] * height,
         p[2] + t_axis[2] * lx + s_axis[2] * ly + ng[2] * height)
    down = (-ng[0], -ng[1], -ng[2])
    pdf0 = burley_pdf(r, lengths[0])
    pdf1 = burley_pdf(r, lengths[1])
    pdf2 = burley_pdf(r, lengths[2])
    mean = (pdf0 + pdf1 + pdf2) / 3.0
    if mean <= 1e-30:
        return p, n, (1.0, 1.0, 1.0)
    weight = (pdf0 / mean, pdf1 / mean, pdf2 / mean)
    tri, t, u, v = intersect(geo, o, down, 2.0 * height, seed, stack, stack_t)
    if tri < 0 or sh.materials[geo.material[tri], MAT_KIND] != MAT_SKIN:
        return p, n, weight
    ng_raw, ns_raw = surface(geo, tri, u, v)
    n_hit = safe_normalize(ns_raw, safe_normalize(ng_raw, (0.0, 0.0, 1.0)))
    if dot(n_hit, n) <= 0.25:
        return p, n, weight
    entry = (o[0] + down[0] * t, o[1] + down[1] * t, o[2] + down[2] * t)
    return entry, n_hit, weight


@device
def trace_sample(geo, sh, prm, px, py, s, stack, stack_t):
    """One sample of pixel ``(px, py)``.

    Returns ``(rgb, alpha, albedo, normal, depth, rays)``: the light found, how
    much of the sample met the scene, the first surface's albedo and normal
    and its distance, for the denoisers, and how many rays were cast.
    """
    pseed = pixel_seed(px, py, prm.seed)
    cam = sample4(pseed, s, DIM_CAMERA)
    fx = filter_offset(prm.filter_table, cam[0])
    fy = filter_offset(prm.filter_table, cam[1])
    o, d = camera_ray(prm, px + 0.5 + fx, py + 0.5 + fy, cam[2], cam[3])
    radiance = (0.0, 0.0, 0.0)
    through = (1.0, 1.0, 1.0)
    alpha = 0.0
    albedo_aov = (0.0, 0.0, 0.0)
    normal_aov = (0.0, 0.0, 0.0)
    depth_aov = 0.0
    rays = 0
    opacity_seed = hash_combine(pseed, s)
    diffuse_n = 0
    glossy_n = 0
    trans_n = 0
    had_diffuse = False
    last_pdf = 0.0
    travelled = 0.0
    # Light after a skin vertex is scaled by the skin's indirect slider; the
    # HDRI and the lights reached straight from that vertex are direct light.
    indirect_total = 1.0
    indirect_last = 1.0
    # A subsurface continuation starts at the entry point the probe found,
    # a white Lambert surface there, whose light was already estimated.
    pending = False
    pend_p = (0.0, 0.0, 0.0)
    pend_n = (0.0, 0.0, 1.0)
    pend_prob = 1.0
    wi = (0.0, 0.0, 1.0)
    lights = sh.lights
    n_lights = lights.shape[0]
    bounce = 0
    while True:
        limit = prm.clamp_direct if bounce == 0 else prm.clamp_indirect
        if pending:
            p = pend_p
            ng = pend_n
            ns = pend_n
            mat_row = -1
            t = 0.0
            pending = False
        else:
            tri, t, u, v = intersect(geo, o, d, 1e30, opacity_seed + bounce, stack, stack_t)
            rays += 1
            if tri == MISS:
                if bounce == 0:
                    if sh.env_on and sh.env_background and not prm.transparent:
                        radiance = _add(radiance, through, env_background(sh, d), 1.0, 0.0)
                        alpha = 1.0
                else:
                    limit = prm.clamp_direct if bounce == 1 else prm.clamp_indirect
                    direct = indirect_total / indirect_last
                    radiance = _add(radiance, through, sky_radiance(sh.sky, d), indirect_total,
                                    limit)
                    if sh.env_on:
                        w = 1.0
                        if last_pdf > 0.0:
                            w = power_heuristic(last_pdf, env_pdf(sh, d))
                        radiance = _add(radiance, through, env_radiance(sh, d), direct * w, limit)
                    for i in range(n_lights):
                        le, lp = disc_hit(lights, i, d)
                        if lp > 0.0:
                            w = 1.0
                            if last_pdf > 0.0:
                                w = power_heuristic(last_pdf, lp)
                            radiance = _add(radiance, through, le, direct * w, limit)
                break
            travelled += t
            p = (o[0] + d[0] * t, o[1] + d[1] * t, o[2] + d[2] * t)
            if tri == CAP_HIT:
                ng = cap_normal(geo, o, d, t)
                ns = ng
                mat_row = geo.cap_material
            else:
                ng_raw, ns_raw = surface(geo, tri, u, v)
                ng = safe_normalize(ng_raw, (-d[0], -d[1], -d[2]))
                ns = safe_normalize(ns_raw, ng)
                mat_row = geo.material[tri]
            if dot(ng, d) > 0.0:
                ng = (-ng[0], -ng[1], -ng[2])
            if dot(ns, ng) < 0.0:
                ns = (-ns[0], -ns[1], -ns[2])
        wo = (-d[0], -d[1], -d[2])
        if dot(ns, wo) <= 0.0:
            ns = ng
        if bounce == 0:
            alpha = 1.0
            depth_aov = t * (d[0] * prm.cam_forward[0] + d[1] * prm.cam_forward[1]
                             + d[2] * prm.cam_forward[2])
        origin = offset_origin(p, ng, geo.radius)
        lu = sample4(pseed, s, bounce_set(bounce, DIM_LIGHT))
        eu = sample4(pseed, s, bounce_set(bounce, DIM_ENV))
        bu = sample4(pseed, s, bounce_set(bounce, DIM_BSDF))
        is_skin = mat_row >= 0 and sh.materials[mat_row, MAT_KIND] == MAT_SKIN

        if mat_row < 0:
            # -- the entry point of scattered light: a white Lambert surface --------
            t_axis, s_axis = basis(ns)
            wi_l = cosine_hemisphere(bu[1], bu[2])
            wi = to_world(wi_l, t_axis, s_axis, ns)
            if wi_l[2] <= 0.0 or dot(wi, ng) <= 0.0:
                break
            # The estimate at the entry weighed this direction with the chance
            # the subsurface lobe was chosen at all; so must the bounce.
            last_pdf = pend_prob * wi_l[2] * INV_PI
            diffuse_n += 1
            had_diffuse = True
            if diffuse_n > prm.max_diffuse:
                break
            indirect_last = 1.0
        elif not is_skin:
            # -- a plain surface ----------------------------------------------------
            mat = sh.materials[mat_row]
            if bounce == 0:
                albedo_aov = (mat[MAT_BASE], mat[MAT_BASE + 1], mat[MAT_BASE + 2])
                normal_aov = ns
            floor = 0.3 * prm.filter_glossy if had_diffuse else 0.0
            alpha_r = material_alpha(mat[MAT_ROUGHNESS], floor)
            t_axis, s_axis = basis(ns)
            wo_l = to_local(wo, t_axis, s_axis, ns)
            for i in range(n_lights):
                if i == 0:
                    wi, li, lp = disc_sample(lights, i, lu[0], lu[1])
                else:
                    wi, li, lp = disc_sample(lights, i, lu[2], lu[3])
                if dot(wi, ng) <= 0.0:
                    continue
                f, bp = principled_eval(mat, wo_l, to_local(wi, t_axis, s_axis, ns), alpha_r)
                if f[0] + f[1] + f[2] <= 0.0:
                    continue
                rays += 1
                if occluded(geo, origin, wi, 1e30, opacity_seed + 7 * bounce + i, stack,
                            stack_t):
                    continue
                w = 1.0 if lp <= 0.0 else power_heuristic(lp, bp)
                radiance = _add(radiance, through, (f[0] * li[0], f[1] * li[1], f[2] * li[2]),
                                indirect_total * w, limit)
            if sh.env_on:
                wi, le, ep = env_sample(sh, eu[0], eu[1])
                if ep > 0.0 and dot(wi, ng) > 0.0:
                    f, bp = principled_eval(mat, wo_l, to_local(wi, t_axis, s_axis, ns), alpha_r)
                    if f[0] + f[1] + f[2] > 0.0:
                        rays += 1
                        if not occluded(geo, origin, wi, 1e30, opacity_seed + 7 * bounce + 5,
                                        stack, stack_t):
                            w = power_heuristic(ep, bp)
                            radiance = _add(radiance, through,
                                            (f[0] * le[0], f[1] * le[1], f[2] * le[2]),
                                            indirect_total * w, limit)
            wi_l, weight, pdf, glossy = principled_sample(mat, wo_l, alpha_r, bu[0], bu[1], bu[2])
            if pdf <= 0.0:
                break
            wi = to_world(wi_l, t_axis, s_axis, ns)
            if dot(wi, ng) <= 0.0:
                break
            if glossy:
                glossy_n += 1
                if glossy_n > prm.max_glossy or (had_diffuse and not prm.caustics):
                    break
            else:
                diffuse_n += 1
                had_diffuse = True
                if diffuse_n > prm.max_diffuse:
                    break
            through = (through[0] * weight[0], through[1] * weight[1], through[2] * weight[2])
            last_pdf = pdf
            indirect_last = 1.0
        else:
            # -- skin ---------------------------------------------------------------
            sk = sh.skin
            footprint = travelled * prm.pixel_spread + prm.ortho_footprint
            albedo, n_spec, n_diff, roughness, oil, blood, vessel = skin_closure(
                sk, sh.regions, sh.relief, sh.body, p, ns, footprint, bounce == 0)
            if dot(n_spec, wo) <= 0.0:
                n_spec = ns
            if dot(n_diff, wo) <= 0.0:
                n_diff = ns
            if had_diffuse:
                roughness = max(roughness, min(1.0, 0.3 * prm.filter_glossy))
            radius = sk[SK_RADIUS]
            sss = sk[SK_SSS]
            transmission = sk[SK_TRANSMISSION]
            specular = sk[SK_SPECULAR]
            fv = skin_fresnel(specular, max(dot(n_spec, wo), 0.0))
            kd = (albedo[0] * (1.0 - fv), albedo[1] * (1.0 - fv), albedo[2] * (1.0 - fv))
            lengths = diffusion_lengths(sk, albedo)
            fuzz = sk[SK_FUZZ]
            rim = (1.0 - max(dot(ns, wo), 0.0)) ** 3
            fuzz_k = fuzz * rim * INV_PI
            fuzz_color = (albedo[0] + (1.0 - albedo[0]) * 0.6,
                          albedo[1] + (1.0 - albedo[1]) * 0.6,
                          albedo[2] + (1.0 - albedo[2]) * 0.6)
            back_k = transmission * sss
            back = (albedo[0] * FLUSH[0] * back_k, albedo[1] * FLUSH[1] * back_k,
                    albedo[2] * FLUSH[2] * back_k)
            if bounce == 0:
                albedo_aov = albedo
                normal_aov = n_spec
            # Lobe choice, by how much light each returns.
            w_spec = fv * 1.0
            w_diff = luminance(kd) * (1.0 - sss)
            w_sss = luminance(kd) * sss
            w_back = luminance(back) if back_k > 0.0 else 0.0
            w_total = w_spec + w_diff + w_sss + w_back
            if w_total <= 0.0:
                break
            p_spec = w_spec / w_total
            p_diff = w_diff / w_total
            p_sss = w_sss / w_total
            p_back = w_back / w_total
            ts, ss = basis(n_spec)
            wo_s = to_local(wo, ts, ss, n_spec)
            su = sample4(pseed, s, bounce_set(bounce, DIM_SUBSURFACE))
            # Light where the scattered light entered: always estimated.
            entry = p
            entry_n = n_diff
            sss_w = (0.0, 0.0, 0.0)
            if sss > 0.0:
                entry, entry_n, sss_w = _probe(geo, sh, p, ng, n_diff, lengths, radius,
                                               eu[2], eu[3], su[0], opacity_seed + 11 * bounce,
                                               stack, stack_t)
                rays += 1
                sss_w = (kd[0] * sss * sss_w[0], kd[1] * sss * sss_w[1],
                         kd[2] * sss * sss_w[2])
            entry_origin = offset_origin(entry, entry_n, geo.radius)
            # The lights: key, fill, then the HDRI's pick.
            n_total = n_lights + (1 if sh.env_on else 0)
            for i in range(n_total):
                if i < n_lights:
                    if i == 0:
                        wi, li, lp = disc_sample(lights, i, lu[0], lu[1])
                    else:
                        wi, li, lp = disc_sample(lights, i, lu[2], lu[3])
                    fuzz_share = 1.0
                else:
                    wi, li, lp = env_sample(sh, eu[0], eu[1])
                    if lp <= 0.0:
                        continue
                    fuzz_share = 0.25
                cos_n = dot(ns, wi)
                # Vellus fuzz: from the lit side and a little from behind,
                # and not shadowed the way the surface is.
                if fuzz > 0.0:
                    side = min(max(cos_n * 0.5 + 0.5, 0.0), 1.0)
                    k = fuzz_k * side * fuzz_share * indirect_total
                    if cos_n < 0.0 or i >= n_lights:
                        radiance = _add(radiance, through,
                                        (fuzz_color[0] * li[0], fuzz_color[1] * li[1],
                                         fuzz_color[2] * li[2]), k, limit)
                if cos_n >= 0.0 or dot(n_diff, wi) > 0.0:
                    if dot(wi, ng) <= 0.0:
                        continue
                    wi_s = to_local(wi, ts, ss, n_spec)
                    spec_v, spec_p = _skin_spec(wo_s, wi_s, roughness, oil, specular)
                    cos_d = max(dot(n_diff, wi), 0.0)
                    f = (spec_v + kd[0] * (1.0 - sss) * cos_d * INV_PI,
                         spec_v + kd[1] * (1.0 - sss) * cos_d * INV_PI,
                         spec_v + kd[2] * (1.0 - sss) * cos_d * INV_PI)
                    bp = p_spec * spec_p + p_diff * cos_d * INV_PI
                    rays += 1
                    if occluded(geo, origin, wi, 1e30, opacity_seed + 7 * bounce + i, stack,
                                stack_t):
                        continue
                    w = 1.0 if lp <= 0.0 else power_heuristic(lp, bp)
                    radiance = _add(radiance, through, (f[0] * li[0], f[1] * li[1],
                                                        f[2] * li[2]), indirect_total * w, limit)
                    if fuzz > 0.0 and i < n_lights and cos_n >= 0.0:
                        side = min(max(cos_n * 0.5 + 0.5, 0.0), 1.0)
                        radiance = _add(radiance, through,
                                        (fuzz_color[0] * li[0], fuzz_color[1] * li[1],
                                         fuzz_color[2] * li[2]), fuzz_k * side * indirect_total,
                                        limit)
                elif back_k > 0.0:
                    # Behind the surface: the backlight, through the thickness.
                    found, exit_p, exit_n, carried = _thickness(
                        geo, sh, p, ng, wi, radius, blood, vessel, opacity_seed + 13 * bounce + i,
                        stack, stack_t)
                    rays += 1
                    if not found:
                        continue
                    rays += 1
                    if occluded(geo, offset_origin(exit_p, exit_n, geo.radius), wi, 1e30,
                                opacity_seed + 17 * bounce + i, stack, stack_t):
                        continue
                    c = -cos_n * INV_PI
                    bp = p_back * c
                    w = 1.0 if lp <= 0.0 else power_heuristic(lp, bp)
                    radiance = _add(radiance, through,
                                    (back[0] * carried[0] * c * li[0],
                                     back[1] * carried[1] * c * li[1],
                                     back[2] * carried[2] * c * li[2]), indirect_total * w, limit)
            # ... and at the entry point, lit as a white Lambert surface.
            if sss > 0.0:
                for i in range(n_total):
                    if i < n_lights:
                        if i == 0:
                            wi, li, lp = disc_sample(lights, i, lu[0], lu[1])
                        else:
                            wi, li, lp = disc_sample(lights, i, lu[2], lu[3])
                    else:
                        wi, li, lp = env_sample(sh, eu[0], eu[1])
                        if lp <= 0.0:
                            continue
                    c = dot(entry_n, wi)
                    if c <= 0.0:
                        continue
                    rays += 1
                    if occluded(geo, entry_origin, wi, 1e30, opacity_seed + 19 * bounce + i,
                                stack, stack_t):
                        continue
                    w = 1.0 if lp <= 0.0 else power_heuristic(lp, p_sss * c * INV_PI)
                    k = c * INV_PI * w * indirect_total
                    radiance = _add(radiance, through,
                                    (sss_w[0] * li[0], sss_w[1] * li[1], sss_w[2] * li[2]),
                                    k, limit)
            # The bounce.
            pick = bu[0]
            indirect_last = sk[SK_INDIRECT]
            if pick < p_spec + p_diff:
                if pick < p_spec:
                    a1 = max(roughness * roughness, 1e-4)
                    a = OIL_ROUGHNESS * OIL_ROUGHNESS if su[1] < oil else a1
                    wi_s = ggx_sample(wo_s, a, bu[1], bu[2])
                    wi = to_world(wi_s, ts, ss, n_spec)
                else:
                    td, sd = basis(n_diff)
                    wi = to_world(cosine_hemisphere(bu[1], bu[2]), td, sd, n_diff)
                    wi_s = to_local(wi, ts, ss, n_spec)
                if dot(wi, ng) <= 0.0:
                    break
                spec_v, spec_p = _skin_spec(wo_s, wi_s, roughness, oil, specular)
                cos_d = max(dot(n_diff, wi), 0.0)
                pdf = p_spec * spec_p + p_diff * cos_d * INV_PI
                if pdf <= 0.0:
                    break
                through = (through[0] * (spec_v + kd[0] * (1.0 - sss) * cos_d * INV_PI) / pdf,
                           through[1] * (spec_v + kd[1] * (1.0 - sss) * cos_d * INV_PI) / pdf,
                           through[2] * (spec_v + kd[2] * (1.0 - sss) * cos_d * INV_PI) / pdf)
                last_pdf = pdf
                if pick < p_spec:
                    glossy_n += 1
                    if glossy_n > prm.max_glossy or (had_diffuse and not prm.caustics):
                        break
                else:
                    diffuse_n += 1
                    had_diffuse = True
                    if diffuse_n > prm.max_diffuse:
                        break
            elif pick < p_spec + p_diff + p_sss:
                # Enter the skin and leave at the entry point the probe found.
                through = (through[0] * sss_w[0] / p_sss, through[1] * sss_w[1] / p_sss,
                           through[2] * sss_w[2] / p_sss)
                diffuse_n += 1
                had_diffuse = True
                if diffuse_n > prm.max_diffuse:
                    break
                pending = True
                pend_p = entry
                pend_n = entry_n
                pend_prob = p_sss
                indirect_total *= indirect_last
                bounce += 1
                if bounce > prm.max_bounces:
                    break
                continue
            else:
                # Through the skin to its far side.
                wl = cosine_hemisphere(bu[1], bu[2])
                tb, sb = basis(ns)
                wi = to_world((wl[0], wl[1], -wl[2]), tb, sb, ns)
                found, exit_p, exit_n, carried = _thickness(
                    geo, sh, p, ng, wi, radius, blood, vessel, opacity_seed + 23 * bounce, stack,
                    stack_t)
                rays += 1
                if not found or p_back <= 0.0:
                    break
                through = (through[0] * back[0] * carried[0] / p_back,
                           through[1] * back[1] * carried[1] / p_back,
                           through[2] * back[2] * carried[2] / p_back)
                last_pdf = p_back * wl[2] * INV_PI
                trans_n += 1
                if trans_n > prm.max_transmission:
                    break
                origin = offset_origin(exit_p, exit_n, geo.radius)
                indirect_total *= indirect_last
                o = origin
                d = wi
                bounce += 1
                if bounce > prm.max_bounces:
                    break
                continue
        indirect_total *= indirect_last
        bounce += 1
        if bounce > prm.max_bounces:
            break
        # Russian roulette, once the path has had its say.
        if bounce >= 3:
            q = max(through[0], max(through[1], through[2]))
            if q < 1.0:
                if bu[3] >= q:
                    break
                through = (through[0] / q, through[1] / q, through[2] / q)
        o = offset_origin(p, ng, geo.radius) if mat_row < 0 else origin
        d = wi
    return radiance, alpha, albedo_aov, normal_aov, depth_aov, rays


@kernel
def render_tile(geo, sh, prm, film, even, count, albedo, normal, depth, converged,
                x0, y0, x1, y1, s0, s1, cancel, counters, slot):
    """Add samples ``s0`` to ``s1`` of every unfinished pixel in the rectangle to the film.

    ``film`` sums rgb and alpha, ``even`` the rgb of the even-numbered
    samples (for the noise estimate), ``count`` the samples taken; the pass
    arrays sum the first surface's albedo, normal and depth.  Returns the
    samples taken; stops early, at a row's end, when ``cancel[0]`` is set.
    """
    stack = np.empty(STACK_SIZE, np.int32)
    stack_t = np.empty(STACK_SIZE, np.float64)
    taken = 0
    rays = 0
    for y in range(y0, y1):
        if cancel[0] != 0:
            break
        for x in range(x0, x1):
            if converged[y, x] != 0:
                continue
            for s in range(s0, s1):
                rgb, a, alb, nrm, dep, r = trace_sample(geo, sh, prm, x, y, s, stack, stack_t)
                rays += r
                if not (math.isfinite(rgb[0]) and math.isfinite(rgb[1])
                        and math.isfinite(rgb[2])):
                    rgb = (0.0, 0.0, 0.0)
                film[y, x, 0] += rgb[0]
                film[y, x, 1] += rgb[1]
                film[y, x, 2] += rgb[2]
                film[y, x, 3] += a
                if (s & 1) == 0:
                    even[y, x, 0] += rgb[0]
                    even[y, x, 1] += rgb[1]
                    even[y, x, 2] += rgb[2]
                count[y, x] += 1
                if albedo.shape[0] > 0:
                    albedo[y, x, 0] += alb[0]
                    albedo[y, x, 1] += alb[1]
                    albedo[y, x, 2] += alb[2]
                    normal[y, x, 0] += nrm[0]
                    normal[y, x, 1] += nrm[1]
                    normal[y, x, 2] += nrm[2]
                    depth[y, x] += dep
                taken += 1
    counters[slot, 0] += taken
    counters[slot, 1] += rays
    return taken


@kernel
def adaptive_error(film, even, count, converged, x0, y0, x1, y1, threshold, min_samples, block):
    """Mark blocks whose noise has fallen below ``threshold`` as done; returns pixels still open.

    The noise estimate is Cycles': the difference between the image of every
    sample and that of the even-numbered half, over the square root of the
    brightness -- which is how visible that difference is.  A block is only
    as done as its noisiest pixel, so a quiet pixel beside a noisy one is not
    left grainy.
    """
    open_pixels = 0
    for by in range(y0, y1, block):
        for bx in range(x0, x1, block):
            worst = 0.0
            fewest = 1 << 30
            for y in range(by, min(by + block, y1)):
                for x in range(bx, min(bx + block, x1)):
                    n = count[y, x]
                    fewest = min(fewest, n)
                    if n < 2:
                        worst = 1e30
                        continue
                    half = (n + 1) // 2
                    e = 0.0
                    total = 0.0
                    for c in range(3):
                        i_c = film[y, x, c] / n
                        a_c = even[y, x, c] / half
                        e += abs(i_c - a_c)
                        total += i_c
                    err = e / (1e-4 + math.sqrt(max(total, 0.0)))
                    worst = max(worst, err)
            done = fewest >= min_samples and worst < threshold
            for y in range(by, min(by + block, y1)):
                for x in range(bx, min(bx + block, x1)):
                    converged[y, x] = 1 if done else 0
                    if not done:
                        open_pixels += 1
    return open_pixels
