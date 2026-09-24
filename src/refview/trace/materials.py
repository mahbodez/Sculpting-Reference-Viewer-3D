"""Surface scattering: the GGX microfacet lobe, Lambert, and the principled blend of them.

Directions are unit vectors pointing away from the surface, in a local frame
whose third axis is the shading normal.  Each lobe can be evaluated -- its
value times the cosine, and the density :func:`principled_sample` would pick
the direction with -- and sampled.  Keeping the two in step is what lets a
light found both ways, by aiming at it and by bouncing into it, be weighed
by multiple importance sampling instead of counted twice.

GGX is sampled by its visible normals (Heitz 2018), with Dupuy and Benyoub's
spherical-cap construction, so a direction is never wasted below the
surface, and shadowed by the height-correlated Smith term.
"""

from __future__ import annotations

import math

import numpy as np

from .jit import device
from .vec import INV_PI, PI, TWO_PI, cosine_hemisphere, lerp, luminance

# Material table layout: one row of MAT_STRIDE numbers per material.
MAT_KIND = 0            # MAT_PRINCIPLED or MAT_SKIN
MAT_BASE = 1            # 1-3: linear base colour
MAT_METALLIC = 4
MAT_ROUGHNESS = 5       # perceptual; alpha is its square
MAT_F0 = 6              # 6-8: a dielectric's reflectance at normal incidence
MAT_TINT = 9            # 9-11: a tint over the whole specular lobe
MAT_STRIDE = 12

MAT_PRINCIPLED = 0
MAT_SKIN = 1

#: The smoothest a lobe is let be: an alpha below this is a mirror in all but
#: name, whose density no float can hold.
MIN_ALPHA = 2e-3


def material_row(base, metallic=0.0, roughness=0.5, f0=(0.04, 0.04, 0.04),
                 tint=(1.0, 1.0, 1.0), kind=MAT_PRINCIPLED) -> np.ndarray:
    row = np.zeros(MAT_STRIDE, np.float64)
    row[MAT_KIND] = kind
    row[MAT_BASE:MAT_BASE + 3] = base
    row[MAT_METALLIC] = metallic
    row[MAT_ROUGHNESS] = roughness
    row[MAT_F0:MAT_F0 + 3] = f0
    row[MAT_TINT:MAT_TINT + 3] = tint
    return row


@device
def schlick(f0, cos_theta):
    """Schlick's Fresnel; a reflectance of nought everywhere means no specular lobe at all."""
    if f0[0] <= 0.0 and f0[1] <= 0.0 and f0[2] <= 0.0:
        return (0.0, 0.0, 0.0)
    m = min(max(1.0 - cos_theta, 0.0), 1.0)
    m2 = m * m
    w = m2 * m2 * m
    return (f0[0] + (1.0 - f0[0]) * w, f0[1] + (1.0 - f0[1]) * w, f0[2] + (1.0 - f0[2]) * w)


@device
def ggx_d(nh, alpha):
    if nh <= 0.0:
        return 0.0
    a2 = alpha * alpha
    t = nh * nh * (a2 - 1.0) + 1.0
    return a2 / (PI * t * t)


@device
def smith_lambda(cos_theta, alpha):
    c2 = cos_theta * cos_theta
    if c2 <= 0.0:
        return 1e30
    tan2 = max(1.0 - c2, 0.0) / c2
    return 0.5 * (-1.0 + math.sqrt(1.0 + alpha * alpha * tan2))


@device
def ggx_eval(wo, wi, alpha):
    """``D G / (4 cos_o cos_i)`` times ``cos_i``, and the density of sampling ``wi``.

    ``wo`` and ``wi`` are local; returns ``(value, pdf, cos_oh)``.  Both are
    nought when either direction is below the surface.
    """
    if wo[2] <= 0.0 or wi[2] <= 0.0:
        return 0.0, 0.0, 0.0
    h = (wo[0] + wi[0], wo[1] + wi[1], wo[2] + wi[2])
    hl = math.sqrt(h[0] * h[0] + h[1] * h[1] + h[2] * h[2])
    if hl < 1e-20:
        return 0.0, 0.0, 0.0
    h = (h[0] / hl, h[1] / hl, h[2] / hl)
    d = ggx_d(h[2], alpha)
    lo = smith_lambda(wo[2], alpha)
    li = smith_lambda(wi[2], alpha)
    g2 = 1.0 / (1.0 + lo + li)
    g1 = 1.0 / (1.0 + lo)
    value = d * g2 / (4.0 * wo[2])
    pdf = d * g1 / (4.0 * wo[2])
    cos_oh = max(wo[0] * h[0] + wo[1] * h[1] + wo[2] * h[2], 0.0)
    return value, pdf, cos_oh


@device
def ggx_sample(wo, alpha, u1, u2):
    """A direction from the visible normals of the lobe about local ``wo``."""
    vh = (alpha * wo[0], alpha * wo[1], wo[2])
    vl = math.sqrt(vh[0] * vh[0] + vh[1] * vh[1] + vh[2] * vh[2])
    vh = (vh[0] / vl, vh[1] / vl, vh[2] / vl)
    phi = TWO_PI * u1
    z = (1.0 - u2) * (1.0 + vh[2]) - vh[2]
    sin_theta = math.sqrt(min(max(1.0 - z * z, 0.0), 1.0))
    c = (sin_theta * math.cos(phi), sin_theta * math.sin(phi), z)
    h = (c[0] + vh[0], c[1] + vh[1], c[2] + vh[2])
    h = (alpha * h[0], alpha * h[1], max(h[2], 0.0))
    hl = math.sqrt(h[0] * h[0] + h[1] * h[1] + h[2] * h[2])
    if hl < 1e-20:
        return (0.0, 0.0, 1.0)
    h = (h[0] / hl, h[1] / hl, h[2] / hl)
    d = 2.0 * (wo[0] * h[0] + wo[1] * h[1] + wo[2] * h[2])
    return (h[0] * d - wo[0], h[1] * d - wo[1], h[2] * d - wo[2])


@device
def _principled_parts(mat, wo):
    base = (mat[MAT_BASE], mat[MAT_BASE + 1], mat[MAT_BASE + 2])
    metallic = mat[MAT_METALLIC]
    f0d = (mat[MAT_F0], mat[MAT_F0 + 1], mat[MAT_F0 + 2])
    tint = (mat[MAT_TINT], mat[MAT_TINT + 1], mat[MAT_TINT + 2])
    f0 = lerp(f0d, base, metallic)
    f0 = (f0[0] * tint[0], f0[1] * tint[1], f0[2] * tint[2])
    fv = schlick(f0, max(wo[2], 0.0))
    kd = ((1.0 - metallic) * base[0] * (1.0 - fv[0]),
          (1.0 - metallic) * base[1] * (1.0 - fv[1]),
          (1.0 - metallic) * base[2] * (1.0 - fv[2]))
    ld = luminance(kd)
    ls = luminance(fv)
    p_spec = 0.5 if ld + ls <= 0.0 else ls / (ld + ls)
    p_spec = min(max(p_spec, 0.05), 0.95) if ls > 0.0 else 0.0
    if ld <= 0.0 and ls > 0.0:
        p_spec = 1.0
    return f0, kd, p_spec


@device
def principled_eval(mat, wo, wi, alpha):
    """``f cos`` for local directions, and the mixture density of sampling ``wi``."""
    if wo[2] <= 0.0 or wi[2] <= 0.0:
        return (0.0, 0.0, 0.0), 0.0
    f0, kd, p_spec = _principled_parts(mat, wo)
    diffuse = wi[2] * INV_PI
    value, pdf_s, cos_oh = ggx_eval(wo, wi, alpha)
    f = schlick(f0, cos_oh)
    out = (kd[0] * diffuse + f[0] * value, kd[1] * diffuse + f[1] * value,
           kd[2] * diffuse + f[2] * value)
    pdf = p_spec * pdf_s + (1.0 - p_spec) * diffuse
    return out, pdf


@device
def principled_sample(mat, wo, alpha, u0, u1, u2):
    """``(wi, f cos / pdf, pdf, glossy)`` for a direction picked from one lobe.

    The weight divides by the mixture density of both lobes -- the
    one-sample form of multiple importance sampling -- so a direction the
    other lobe was likelier to pick is not over-counted.
    """
    if wo[2] <= 0.0:
        return (0.0, 0.0, 1.0), (0.0, 0.0, 0.0), 0.0, False
    _f0, _kd, p_spec = _principled_parts(mat, wo)
    glossy = u0 < p_spec
    wi = ggx_sample(wo, alpha, u1, u2) if glossy else cosine_hemisphere(u1, u2)
    if wi[2] <= 0.0:
        return wi, (0.0, 0.0, 0.0), 0.0, glossy
    f, pdf = principled_eval(mat, wo, wi, alpha)
    if pdf <= 0.0:
        return wi, (0.0, 0.0, 0.0), 0.0, glossy
    return wi, (f[0] / pdf, f[1] / pdf, f[2] / pdf), pdf, glossy


@device
def material_alpha(roughness, floor):
    r = max(roughness, floor)
    return max(r * r, MIN_ALPHA)
