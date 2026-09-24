"""Human Skin, as the path tracer shades it: a port of ``render/glsl/skin.glsl``.

The surface is the viewport's, function for function -- the pore relief read
from the same tileable volume, the pigment and blood mottling, the vessels,
the freckles, moles, acne and blemishes laid by the same hashes on the same
lattices, and the body map turning each of them up or down by region -- so a
mole is in the same place in a render as on screen.  Only two things change:

* the derivatives the shader takes of screen position, to fade detail that
  is smaller than a pixel, come from the width of the ray's cone instead;
* the light is traced rather than approximated.  The viewport's fixed list of
  rays becomes lobes a path chooses between -- the two specular lobes (the
  skin's own and the oil's), the diffuse lobe, the subsurface lobe and the
  backlight -- so every light, the HDRI and bounced light reach every lobe.

Subsurface scattering is Christensen and Burley's disk projection, with the
viewport's own diffusion lengths and radius distribution: a radius and an
angle are picked on the plane of the surface, and a probe dropped through
the skin there finds where the light entered.  That is one ray, where a
random walk inside the body would be dozens, and it does not leak out of an
open scan the way a walk does.

Hashes are computed in single precision, as the GPU computes them, so the
spots land where the viewport put them.
"""

from __future__ import annotations

import math

import numpy as np

from ..core.skin_detail import RELIEF_CELLS
from .jit import device
from .vec import clamp, clamp3, dot, lerp, normalize, smoothstep

# Skin parameter layout.
SK_COLOR = 0            # 0-2: linear base colour
SK_SCATTER = 3          # 3-5: the scatter colour, as the slider gives it
SK_ROUGHNESS = 6
SK_SPECULAR = 7
SK_OIL = 8
SK_SSS = 9
SK_RADIUS = 10          # world units
SK_TRANSMISSION = 11
SK_DETAIL = 12
SK_PORE = 13            # world units
SK_MOTTLE = 14
SK_BLOOD = 15
SK_VEINS = 16
SK_FUZZ = 17
SK_BLEMISHES = 18
SK_FRECKLES = 19
SK_NEVI = 20
SK_ACNE = 21
SK_INDIRECT = 22
SK_EPSILON = 23
SK_BODY_ON = 24
SK_BODY_ORIGIN = 25     # 25-27
SK_BODY_INV_SIZE = 28   # 28-30
SK_STRIDE = 32

# Region multiplier rows, one per effect, eight regions to a row.
RG_ACNE, RG_NEVI, RG_FRECKLES, RG_BLEMISH, RG_OIL, RG_BLOOD, RG_VEIN = range(7)
REGION_EFFECTS = ("acne", "nevi", "freckles", "blemishes", "oil", "blood", "veins")

CELLS = float(RELIEF_CELLS)
#: Linear tint of light that has passed through blood-rich dermis.
FLUSH = (1.04, 0.70, 0.64)
#: The skin's reflectance at normal incidence: eta = 1.4.
SKIN_F0 = 0.02778

_F32 = np.float32


def skin_parameters(skin, scene_radius: float, body=None) -> tuple[np.ndarray, np.ndarray]:
    """The parameter row and the region multipliers for :class:`~refview.core.skin.SkinSettings`."""
    from .vec import srgb_to_linear

    radius = max(float(scene_radius), 1e-6)
    p = np.zeros(SK_STRIDE, np.float64)
    p[SK_COLOR:SK_COLOR + 3] = [srgb_to_linear(float(c)) for c in skin.color]
    p[SK_SCATTER:SK_SCATTER + 3] = skin.scatter_color
    p[SK_ROUGHNESS] = skin.roughness
    p[SK_SPECULAR] = skin.specular
    p[SK_OIL] = skin.oiliness
    p[SK_SSS] = skin.sss
    p[SK_RADIUS] = skin.radius * radius
    p[SK_TRANSMISSION] = skin.transmission
    p[SK_DETAIL] = skin.detail
    p[SK_PORE] = skin.pore_size * radius
    p[SK_MOTTLE] = skin.mottle
    p[SK_BLOOD] = skin.blood
    p[SK_VEINS] = skin.veins
    p[SK_FUZZ] = skin.fuzz
    p[SK_BLEMISHES] = skin.blemishes
    p[SK_FRECKLES] = skin.freckles
    p[SK_NEVI] = skin.nevi
    p[SK_ACNE] = skin.acne
    p[SK_INDIRECT] = skin.indirect
    p[SK_EPSILON] = radius * 1e-5
    if body is not None:
        p[SK_BODY_ON] = 1.0
        p[SK_BODY_ORIGIN:SK_BODY_ORIGIN + 3] = body.origin
        p[SK_BODY_INV_SIZE:SK_BODY_INV_SIZE + 3] = 1.0 / np.maximum(body.size, 1e-12)
    regions = np.zeros((7, 8), np.float64)
    for row, effect in enumerate(REGION_EFFECTS):
        regions[row, :7] = skin.regions.multipliers(effect)
    return p, regions


# -- volumes -------------------------------------------------------------------


@device
def relief_fetch(vol, q):
    """Trilinear, wrapping read of the relief volume at tile coordinates ``q``."""
    n = vol.shape[0]
    x = q[0] * n - 0.5
    y = q[1] * n - 0.5
    z = q[2] * n - 0.5
    fx0 = math.floor(x)
    fy0 = math.floor(y)
    fz0 = math.floor(z)
    fx = x - fx0
    fy = y - fy0
    fz = z - fz0
    x0 = int(fx0) % n
    y0 = int(fy0) % n
    z0 = int(fz0) % n
    x1 = (x0 + 1) % n
    y1 = (y0 + 1) % n
    z1 = (z0 + 1) % n
    a = 0.0
    b = 0.0
    c = 0.0
    d = 0.0
    for zi, wz in ((z0, 1.0 - fz), (z1, fz)):
        for yi, wy in ((y0, 1.0 - fy), (y1, fy)):
            for xi, wx in ((x0, 1.0 - fx), (x1, fx)):
                w = wx * wy * wz
                a += vol[zi, yi, xi, 0] * w
                b += vol[zi, yi, xi, 1] * w
                c += vol[zi, yi, xi, 2] * w
                d += vol[zi, yi, xi, 3] * w
    return a, b, c, d


@device
def _tone(vol, q, s, o0, o1, o2):
    return relief_fetch(vol, (q[0] * s + o0, q[1] * s + o1, q[2] * s + o2))[3]


@device
def body_fetch(body, uvw, channel):
    """Trilinear, clamped read of one channel of the body map."""
    nz = body.shape[0]
    ny = body.shape[1]
    nx = body.shape[2]
    x = min(max(uvw[0], 0.0), 1.0) * nx - 0.5
    y = min(max(uvw[1], 0.0), 1.0) * ny - 0.5
    z = min(max(uvw[2], 0.0), 1.0) * nz - 0.5
    fx0 = math.floor(x)
    fy0 = math.floor(y)
    fz0 = math.floor(z)
    fx = x - fx0
    fy = y - fy0
    fz = z - fz0
    x0 = min(max(int(fx0), 0), nx - 1)
    y0 = min(max(int(fy0), 0), ny - 1)
    z0 = min(max(int(fz0), 0), nz - 1)
    x1 = min(x0 + 1, nx - 1) if fx0 >= 0 else x0
    y1 = min(y0 + 1, ny - 1) if fy0 >= 0 else y0
    z1 = min(z0 + 1, nz - 1) if fz0 >= 0 else z0
    total = 0.0
    for zi, wz in ((z0, 1.0 - fz), (z1, fz)):
        for yi, wy in ((y0, 1.0 - fy), (y1, fy)):
            for xi, wx in ((x0, 1.0 - fx), (x1, fx)):
                total += body[zi, yi, xi, channel] * wx * wy * wz
    return total


# -- the surface ---------------------------------------------------------------

# The twist that hides the relief tile's period, as a GLSL mat3 (columns).
_TWIST = ((0.36, 0.48, -0.80), (-0.80, 0.60, 0.00), (0.48, 0.64, 0.60))


@device
def relief(vol, p, pore, footprint_q):
    """``(slope, tone, flush, fade)`` at ``p``: the pores and the pigment's broad variation."""
    tile = pore * CELLS
    q = (p[0] / tile, p[1] / tile, p[2] / tile)
    fade = 1.0 - smoothstep(0.12, 0.5, footprint_q * CELLS)
    a = relief_fetch(vol, q)
    # twist * q, with the GLSL matrix column-major.
    tq = (
        _TWIST[0][0] * q[0] + _TWIST[1][0] * q[1] + _TWIST[2][0] * q[2],
        _TWIST[0][1] * q[0] + _TWIST[1][1] * q[1] + _TWIST[2][1] * q[2],
        _TWIST[0][2] * q[0] + _TWIST[1][2] * q[1] + _TWIST[2][2] * q[2],
    )
    b = relief_fetch(vol, (tq[0] * 1.63 + 0.37, tq[1] * 1.63 + 0.71, tq[2] * 1.63 + 0.19))
    # b.xyz * twist (row vector times matrix): component j is dot(b, column j).
    bt = (
        b[0] * _TWIST[0][0] + b[1] * _TWIST[0][1] + b[2] * _TWIST[0][2],
        b[0] * _TWIST[1][0] + b[1] * _TWIST[1][1] + b[2] * _TWIST[1][2],
        b[0] * _TWIST[2][0] + b[1] * _TWIST[2][1] + b[2] * _TWIST[2][2],
    )
    k = 0.5 * 1.63
    slope = (a[0] + bt[0] * k, a[1] + bt[1] * k, a[2] + bt[2] * k)
    broad = _tone(vol, q, 0.19, 0.50, 0.13, 0.77)
    tone = broad + (a[3] - broad) * 0.25
    flush = _tone(vol, q, 0.11, 0.23, 0.61, 0.41)
    return slope, tone, flush, fade


@device
def bump(n, slope, amount):
    d = dot(n, slope)
    t = (slope[0] - n[0] * d, slope[1] - n[1] * d, slope[2] - n[2] * d)
    return normalize((n[0] - t[0] * amount, n[1] - t[1] * amount, n[2] - t[2] * amount))


@device
def skin_albedo(base, mottle, tone, flush, blood):
    k = 1.0 + mottle * 0.22 * (tone * 2.0 - 1.0)
    albedo = (base[0] * k, base[1] * k, base[2] * k)
    pooled = blood * smoothstep(0.25, 0.85, flush)
    flushed = (albedo[0] * FLUSH[0], albedo[1] * FLUSH[1], albedo[2] * FLUSH[2])
    return clamp3(lerp(albedo, flushed, pooled), 0.0, 1.0)


@device
def vessel(vol, p, pore, tone, flush, footprint_q):
    tile = pore * CELLS
    q = (p[0] / tile, p[1] / tile, p[2] / tile)
    footprint = footprint_q * 1.4 * 0.16
    fade = 1.0 - smoothstep(0.04, 0.13, footprint)
    if fade <= 0.0:
        return 0.0
    broad = _tone(vol, q, 0.16, 0.43, 0.17, 0.69)
    warp = _tone(vol, q, 0.39, 0.11, 0.79, 0.31)
    width = 0.06 + (0.085 - 0.06) * tone
    line = 1.0 - smoothstep(width * 0.3, width, abs(broad + 0.22 * (warp - 0.5) - 0.51))
    strength = 0.78 + (1.0 - 0.78) * flush
    return line * smoothstep(0.30, 0.62, warp) * strength * fade


@device
def region(sk, regions, body, p):
    """The seven effect multipliers where ``p`` is on the body; all one off the map."""
    if sk[SK_BODY_ON] <= 0.0:
        return 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0
    uvw = ((p[0] - sk[SK_BODY_ORIGIN]) * sk[SK_BODY_INV_SIZE],
           (p[1] - sk[SK_BODY_ORIGIN + 1]) * sk[SK_BODY_INV_SIZE + 1],
           (p[2] - sk[SK_BODY_ORIGIN + 2]) * sk[SK_BODY_INV_SIZE + 2])
    w0 = body_fetch(body, uvw, 0)
    w1 = body_fetch(body, uvw, 1)
    w2 = body_fetch(body, uvw, 2)
    w3 = body_fetch(body, uvw, 3)
    w4 = body_fetch(body, uvw, 4)
    w5 = body_fetch(body, uvw, 5)
    w6 = body_fetch(body, uvw, 6)
    rest = max(1.0 - body_fetch(body, uvw, 7), 0.0)
    out0 = 0.0
    out1 = 0.0
    out2 = 0.0
    out3 = 0.0
    out4 = 0.0
    out5 = 0.0
    out6 = 0.0
    for effect in range(7):
        m = regions[effect]
        v = (rest + w0 * m[0] + w1 * m[1] + w2 * m[2] + w3 * m[3] + w4 * m[4] + w5 * m[5]
             + w6 * m[6])
        if effect == 0:
            out0 = v
        elif effect == 1:
            out1 = v
        elif effect == 2:
            out2 = v
        elif effect == 3:
            out3 = v
        elif effect == 4:
            out4 = v
        elif effect == 5:
            out5 = v
        else:
            out6 = v
    return out0, out1, out2, out3, out4, out5, out6


# -- marks ---------------------------------------------------------------------


@device
def _fract32(x):
    x = _F32(x)
    return _F32(x - _F32(math.floor(x)))


@device
def hash4(cx, cy, cz):
    """``skinHash4`` in single precision."""
    p0 = _fract32(_F32(cx) * _F32(0.1031))
    p1 = _fract32(_F32(cy) * _F32(0.1030))
    p2 = _fract32(_F32(cz) * _F32(0.0973))
    p3 = _fract32(_F32(cx) * _F32(0.1099))
    # p4 += dot(p4, p4.wzxy + 33.33)
    k = _F32(33.33)
    d = _F32(_F32(p0 * _F32(p3 + k)) + _F32(p1 * _F32(p2 + k)))
    d = _F32(d + _F32(p2 * _F32(p0 + k)))
    d = _F32(d + _F32(p3 * _F32(p1 + k)))
    p0 = _F32(p0 + d)
    p1 = _F32(p1 + d)
    p2 = _F32(p2 + d)
    p3 = _F32(p3 + d)
    # fract((p4.xxyz + p4.yzzw) * p4.zywx)
    return (
        float(_fract32(_F32(p0 + p1) * p2)),
        float(_fract32(_F32(p0 + p2) * p1)),
        float(_fract32(_F32(p1 + p2) * p3)),
        float(_fract32(_F32(p2 + p3) * p0)),
    )


@device
def spot(qx, qy, seed, density, radius, soft):
    """``(cover, kind, away, t)`` of the one spot that can reach ``q``, as ``skinSpot``."""
    cx = math.floor(qx)
    cy = math.floor(qy)
    h = hash4(cx, cy, seed)
    k = hash4(cx, cy, seed + 71.0)
    kind = k[0]
    if h[3] >= density:
        return 0.0, kind, (1.0, 0.0), 2.0
    centre_x = cx + 0.5 + (h[0] - 0.5) * 0.5
    centre_y = cy + 0.5 + (h[1] - 0.5) * 0.5
    r = radius * (0.55 + 0.45 * k[1])
    dx = qx - centre_x
    dy = qy - centre_y
    s = math.sqrt(dx * dx + dy * dy)
    t = s / r
    inv = 1.0 / max(s, 1e-6)
    return 1.0 - smoothstep(soft, 1.0, t), kind, (dx * inv, dy * inv), t


@device
def dome(away, t, h, r):
    edge = 1.0 - smoothstep(0.75, 1.0, t)
    k = -(2.0 * h * t / max(r, 1e-6)) * edge
    return away[0] * k, away[1] * k


@device
def spots(u, v, u_axis, v_axis, seed, per_pixel, pore, freckles, nevi, acne):
    """``(tint, slope, oil, rough)`` of the spots on one plane, as ``skinSpots``."""
    tint = (1.0, 1.0, 1.0)
    slope = (0.0, 0.0, 0.0)
    oil = 0.0
    rough = 0.0
    pore = max(pore, 1e-9)
    # Freckles: small, thick on the ground, light brown, flat.
    cell = 4.0 * pore
    fade = 1.0 - smoothstep(0.08, 0.30, per_pixel / cell)
    if fade > 0.0 and freckles > 0.0:
        cover, kind, _away, _t = spot(u / cell + 11.3, v / cell + 7.1, seed,
                                      min(freckles * 0.6, 1.0), 0.25, 0.1)
        cover *= fade
        strength = 0.3 + (0.85 - 0.3) * kind
        tint = lerp(tint, (0.62, 0.45, 0.35), cover * strength)
    # Moles: dark, a few pores across, few, faintly raised.
    cell = 10.0 * pore
    fade = 1.0 - smoothstep(0.05, 0.20, per_pixel / cell)
    if fade > 0.0 and nevi > 0.0:
        cover, kind, away, t = spot(u / cell + 5.7, v / cell + 13.1, seed + 3.0,
                                    min(nevi * 0.08, 1.0), 0.25, 0.65)
        cover *= fade
        dark = (0.52, 0.36, 0.30) if kind >= 0.7 else (0.30, 0.20, 0.17)
        m = lerp((1.0, 1.0, 1.0), dark, cover)
        tint = (tint[0] * m[0], tint[1] * m[1], tint[2] * m[2])
        dx, dy = dome(away, t, 0.04, 0.25)
        dx *= cover
        dy *= cover
        slope = (slope[0] + u_axis[0] * dx + v_axis[0] * dy,
                 slope[1] + u_axis[1] * dx + v_axis[1] * dy,
                 slope[2] + u_axis[2] * dx + v_axis[2] * dy)
        rough += cover * 0.15
    # Acne: red papules, raised and shining, some come to a pale head.
    cell = 6.0 * pore
    fade = 1.0 - smoothstep(0.06, 0.25, per_pixel / cell)
    if fade > 0.0 and acne > 0.0:
        cover, kind, away, t = spot(u / cell + 2.3, v / cell + 4.7, seed + 6.0,
                                    min(acne * 0.25, 1.0), 0.25, 0.45)
        cover *= fade
        flush = cover * (0.55 + 0.45 * (1.0 - smoothstep(0.0, 0.8, t)))
        m = lerp((1.0, 1.0, 1.0), (1.08, 0.52, 0.46), flush)
        tint = (tint[0] * m[0], tint[1] * m[1], tint[2] * m[2])
        raised = 1.0 - smoothstep(0.35, 0.7, t)
        dx, dy = dome(away, t * 1.4, 0.15, 0.25)
        dx *= cover * raised
        dy *= cover * raised
        slope = (slope[0] + u_axis[0] * dx + v_axis[0] * dy,
                 slope[1] + u_axis[1] * dx + v_axis[1] * dy,
                 slope[2] + u_axis[2] * dx + v_axis[2] * dy)
        head = (1.0 if kind >= 0.62 else 0.0) * (1.0 - smoothstep(0.0, 0.30, t)) * cover
        tint = lerp(tint, (1.0, 0.90, 0.72), head)
        oil += cover * raised * 0.6
    return tint, slope, oil, rough


@device
def marks(sk, vol, p, n, per_pixel, r_acne, r_nevi, r_freckles, r_blemish):
    """``(tint, slope, oil, rough)`` of every mark at ``p``, as ``skinMarks``."""
    pore = sk[SK_PORE]
    freckles = sk[SK_FRECKLES] * r_freckles
    nevi = sk[SK_NEVI] * r_nevi
    acne = sk[SK_ACNE] * r_acne
    blemishes = sk[SK_BLEMISHES] * r_blemish
    tint = (0.0, 0.0, 0.0)
    slope = (0.0, 0.0, 0.0)
    oil = 0.0
    rough = 0.0
    wx = abs(n[0]) ** 4
    wy = abs(n[1]) ** 4
    wz = abs(n[2]) ** 4
    total = max(wx + wy + wz, 1e-6)
    wx /= total
    wy /= total
    wz /= total
    if freckles + nevi + acne > 0.0:
        if wx > 0.005:
            t, s, o, r = spots(p[1], p[2], (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), 1.0, per_pixel,
                               pore, freckles, nevi, acne)
            tint = (tint[0] + t[0] * wx, tint[1] + t[1] * wx, tint[2] + t[2] * wx)
            slope = (slope[0] + s[0] * wx, slope[1] + s[1] * wx, slope[2] + s[2] * wx)
            oil += o * wx
            rough += r * wx
        else:
            tint = (tint[0] + wx, tint[1] + wx, tint[2] + wx)
        if wy > 0.005:
            t, s, o, r = spots(p[2], p[0], (0.0, 0.0, 1.0), (1.0, 0.0, 0.0), 2.0, per_pixel,
                               pore, freckles, nevi, acne)
            tint = (tint[0] + t[0] * wy, tint[1] + t[1] * wy, tint[2] + t[2] * wy)
            slope = (slope[0] + s[0] * wy, slope[1] + s[1] * wy, slope[2] + s[2] * wy)
            oil += o * wy
            rough += r * wy
        else:
            tint = (tint[0] + wy, tint[1] + wy, tint[2] + wy)
        if wz > 0.005:
            t, s, o, r = spots(p[0], p[1], (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), 3.0, per_pixel,
                               pore, freckles, nevi, acne)
            tint = (tint[0] + t[0] * wz, tint[1] + t[1] * wz, tint[2] + t[2] * wz)
            slope = (slope[0] + s[0] * wz, slope[1] + s[1] * wz, slope[2] + s[2] * wz)
            oil += o * wz
            rough += r * wz
        else:
            tint = (tint[0] + wz, tint[1] + wz, tint[2] + wz)
    else:
        tint = (1.0, 1.0, 1.0)
    if blemishes > 0.0:
        tile = pore * CELLS
        q = (p[0] / tile, p[1] / tile, p[2] / tile)
        red = _tone(vol, q, 0.043, 0.71, 0.29, 0.53) * _tone(vol, q, 0.027, 0.17, 0.61, 0.37) * 2.0
        sore = smoothstep(0.52, 0.80, red) * blemishes
        m = lerp((1.0, 1.0, 1.0), (1.05, 0.78, 0.72), sore)
        tint = (tint[0] * m[0], tint[1] * m[1], tint[2] * m[2])
        dry = smoothstep(0.58, 0.82, _tone(vol, q, 0.031, 0.13, 0.83, 0.47)) * blemishes
        m = lerp((1.0, 1.0, 1.0), (0.86, 0.79, 0.75), dry)
        tint = (tint[0] * m[0], tint[1] * m[1], tint[2] * m[2])
        rough += dry * 0.3
    return tint, slope, oil, rough


@device
def diffusion_lengths(sk, albedo):
    """Burley's fit from mean free path and albedo to the profile's length ``d``, per channel."""
    radius = sk[SK_RADIUS]
    floor = sk[SK_EPSILON] * 2.0
    out0 = 0.0
    out1 = 0.0
    out2 = 0.0
    for c in range(3):
        a = albedo[c]
        s = 1.9 - a + 3.5 * (a - 0.8) * (a - 0.8)
        v = max(radius * sk[SK_SCATTER + c] / s, floor)
        if c == 0:
            out0 = v
        elif c == 1:
            out1 = v
        else:
            out2 = v
    return (out0, out1, out2)


@device
def skin_closure(sk, regions, vol, body, p, n, footprint, detailed):
    """The skin at ``p`` with smooth normal ``n`` (facing the viewer).

    Returns ``(albedo, n_spec, n_diff, roughness, oil, blood, vessel)``.
    ``footprint`` is the world width of the pixel's cone there; ``detailed``
    is false for points only bounced light sees, which get the skin without
    its fine detail -- no one can see a pore in a reflection's reflection.
    """
    base = (sk[SK_COLOR], sk[SK_COLOR + 1], sk[SK_COLOR + 2])
    if not detailed:
        blood = clamp(sk[SK_BLOOD], 0.0, 1.0)
        return (base, n, n, clamp(sk[SK_ROUGHNESS], 0.12, 1.0), clamp(sk[SK_OIL], 0.0, 1.0),
                blood, 0.0)
    pore = max(sk[SK_PORE], 1e-9)
    footprint_q = footprint * 1.41 / (pore * CELLS)
    slope, tone, flush, fade = relief(vol, p, pore, footprint_q)
    r_acne, r_nevi, r_freckles, r_blemish, r_oil, r_blood, r_vein = region(sk, regions, body, p)
    m_tint, m_slope, m_oil, m_rough = marks(sk, vol, p, n, footprint * 1.41, r_acne, r_nevi,
                                             r_freckles, r_blemish)
    detail = sk[SK_DETAIL] * fade
    oil = clamp(sk[SK_OIL] * r_oil + m_oil, 0.0, 1.0)
    roughness = clamp(sk[SK_ROUGHNESS] + m_rough, 0.12, 1.0)
    blood = clamp(sk[SK_BLOOD] * r_blood, 0.0, 1.0)
    vein_amount = clamp(sk[SK_VEINS] * r_vein, 0.0, 1.0)
    vessel_amount = 0.0
    if sk[SK_VEINS] > 0.0:
        vessel_amount = vessel(vol, p, pore, tone, flush, footprint_q) * vein_amount
    n_spec = bump(n, (slope[0] * detail + m_slope[0], slope[1] * detail + m_slope[1],
                      slope[2] * detail + m_slope[2]), 1.0)
    n_diff = bump(n, (slope[0] * detail * 0.35 + m_slope[0] * 0.6,
                      slope[1] * detail * 0.35 + m_slope[1] * 0.6,
                      slope[2] * detail * 0.35 + m_slope[2] * 0.6), 1.0)
    albedo = skin_albedo(base, sk[SK_MOTTLE], tone, flush, blood)
    albedo = clamp3((albedo[0] * m_tint[0], albedo[1] * m_tint[1], albedo[2] * m_tint[2]),
                    0.0, 1.0)
    veil = lerp((1.0, 1.0, 1.0), (0.68, 0.78, 0.90), vessel_amount * 0.55)
    albedo = (albedo[0] * veil[0], albedo[1] * veil[1], albedo[2] * veil[2])
    return albedo, n_spec, n_diff, roughness, oil, blood, vessel_amount


@device
def skin_fresnel(specular, cos_theta):
    m = min(max(1.0 - cos_theta, 0.0), 1.0)
    m2 = m * m
    f = SKIN_F0 + (1.0 - SKIN_F0) * m2 * m2 * m
    return min(max(f * specular, 0.0), 0.99)


@device
def burley_pdf(r, d):
    """The density of radius ``r`` for length ``d``: a quarter at ``d``, the rest at ``3d``."""
    if d <= 0.0:
        return 0.0
    return (0.25 * math.exp(-r / d) + 0.25 * math.exp(-r / (3.0 * d))) / d
