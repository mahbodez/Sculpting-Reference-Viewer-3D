"""The lights: the studio key and fill, the studio sky, and the HDRI.

The key and fill are distant lights with a size -- a disc of sky an angle
across, as the sun is -- which is what gives a shadow its soft edge.  Their
brightness is set, as the viewport sets it, by the irradiance they put on a
surface facing them; the radiance of the disc is that over its projected
solid angle.  A light of no size is a point in the sky, and can only be
found by aiming at it.

The sky is the studio rig's ambient: brighter overhead than underfoot,
smooth, and so left to the surfaces to find by bouncing into it.

The HDRI is picked from in proportion to its light (the tables built in
:mod:`refview.core.environment`), and its radiance read from the full map.
Its frame turns with the view while the lights follow the camera, as in the
viewport; ``env_rotation`` takes a world direction into the map's frame.
"""

from __future__ import annotations

import math

from .jit import device
from .vec import PI, TWO_PI, basis, to_world

# Light table layout: one row per distant light.
LIGHT_DIR = 0           # 0-2: unit direction toward the light, world
LIGHT_COS = 3           # cosine of the disc's angular radius; 1 for a point
LIGHT_RADIANCE = 4      # 4-6: radiance, or for a point, irradiance
LIGHT_PDF = 7           # one over the disc's solid angle; 0 for a point
LIGHT_STRIDE = 8


def light_row(direction, irradiance, radius_rad: float) -> list[float]:
    """A light's row, from the irradiance it puts on a surface facing it."""
    radius_rad = max(float(radius_rad), 0.0)
    if radius_rad < 1e-4:
        return [*direction, 1.0, *irradiance, 0.0]
    cos_max = math.cos(radius_rad)
    solid = TWO_PI * (1.0 - cos_max)
    projected = PI * math.sin(radius_rad) ** 2
    radiance = [c / projected for c in irradiance]
    return [*direction, cos_max, *radiance, 1.0 / solid]


@device
def disc_sample(lights, i, u1, u2):
    """``(direction, radiance / pdf, pdf)`` toward a point of light ``i``; pdf 0 for a point."""
    d = (lights[i, 0], lights[i, 1], lights[i, 2])
    cos_max = lights[i, LIGHT_COS]
    rad = (lights[i, 4], lights[i, 5], lights[i, 6])
    pdf = lights[i, LIGHT_PDF]
    if pdf <= 0.0:
        return d, rad, 0.0
    c = 1.0 - u1 * (1.0 - cos_max)
    s = math.sqrt(max(0.0, 1.0 - c * c))
    phi = TWO_PI * u2
    t, b = basis(d)
    wi = to_world((s * math.cos(phi), s * math.sin(phi), c), t, b, d)
    inv = 1.0 / pdf
    return wi, (rad[0] * inv, rad[1] * inv, rad[2] * inv), pdf


@device
def disc_hit(lights, i, direction):
    """The radiance of light ``i`` seen along ``direction``, and its pdf; zeros if outside it."""
    pdf = lights[i, LIGHT_PDF]
    if pdf <= 0.0:
        return (0.0, 0.0, 0.0), 0.0
    c = direction[0] * lights[i, 0] + direction[1] * lights[i, 1] + direction[2] * lights[i, 2]
    if c < lights[i, LIGHT_COS]:
        return (0.0, 0.0, 0.0), 0.0
    return (lights[i, 4], lights[i, 5], lights[i, 6]), pdf


@device
def sky_radiance(sky, d):
    if sky[3] <= 0.0:
        return (0.0, 0.0, 0.0)
    t = min(max(d[1] * 0.5 + 0.5, 0.0), 1.0)
    w = 0.35 + 0.65 * t
    return (sky[0] * w, sky[1] * w, sky[2] * w)


@device
def _env_frame(rotation, d):
    return (
        rotation[0, 0] * d[0] + rotation[0, 1] * d[1] + rotation[0, 2] * d[2],
        rotation[1, 0] * d[0] + rotation[1, 1] * d[1] + rotation[1, 2] * d[2],
        rotation[2, 0] * d[0] + rotation[2, 1] * d[1] + rotation[2, 2] * d[2],
    )


@device
def _env_world(rotation, d):
    return (
        rotation[0, 0] * d[0] + rotation[1, 0] * d[1] + rotation[2, 0] * d[2],
        rotation[0, 1] * d[0] + rotation[1, 1] * d[1] + rotation[2, 1] * d[2],
        rotation[0, 2] * d[0] + rotation[1, 2] * d[1] + rotation[2, 2] * d[2],
    )


@device
def _uv(d):
    u = math.atan2(d[0], -d[2]) / TWO_PI + 0.5
    v = math.acos(min(max(d[1], -1.0), 1.0)) / PI
    return u, v


@device
def map_lookup(image, u, v):
    """Bilinear radiance from a panorama, wrapping across and clamped down."""
    h = image.shape[0]
    w = image.shape[1]
    x = u * w - 0.5
    y = v * h - 0.5
    x0 = math.floor(x)
    y0 = math.floor(y)
    fx = x - x0
    fy = y - y0
    ix0 = int(x0) % w
    ix1 = (ix0 + 1) % w
    iy0 = min(max(int(y0), 0), h - 1)
    iy1 = min(max(int(y0) + 1, 0), h - 1)
    r = 0.0
    g = 0.0
    b = 0.0
    for yy, wy in ((iy0, 1.0 - fy), (iy1, fy)):
        for xx, wx in ((ix0, 1.0 - fx), (ix1, fx)):
            wgt = wx * wy
            r += image[yy, xx, 0] * wgt
            g += image[yy, xx, 1] * wgt
            b += image[yy, xx, 2] * wgt
    return (r, g, b)


@device
def env_radiance(sh, d):
    """The HDRI's light arriving along world direction ``d``."""
    if not sh.env_on:
        return (0.0, 0.0, 0.0)
    u, v = _uv(_env_frame(sh.env_rotation, d))
    c = map_lookup(sh.env_rgb, u, v)
    s = sh.env_scale
    return (c[0] * s, c[1] * s, c[2] * s)


@device
def env_background(sh, d):
    """The HDRI as the camera sees it behind the model: blurred as the viewport blurs it."""
    u, v = _uv(_env_frame(sh.env_rotation, d))
    c = map_lookup(sh.env_bg, u, v)
    s = sh.env_scale
    return (c[0] * s, c[1] * s, c[2] * s)


@device
def env_pdf(sh, d):
    """The density over solid angle of :func:`env_sample` picking world direction ``d``."""
    if not sh.env_on:
        return 0.0
    u, v = _uv(_env_frame(sh.env_rotation, d))
    h = sh.env_density.shape[0]
    w = sh.env_density.shape[1]
    row = min(int(v * h), h - 1)
    col = min(int(u * w), w - 1)
    sin_theta = math.sin(v * PI)
    if sin_theta <= 1e-12:
        return 0.0
    return sh.env_density[row, col] / (2.0 * PI * PI * sin_theta)


@device
def _search(cdf, count, xi):
    """The largest index ``i < count`` with ``cdf[i] <= xi``."""
    lo = 0
    hi = count
    while lo + 1 < hi:
        mid = (lo + hi) >> 1
        if cdf[mid] <= xi:
            lo = mid
        else:
            hi = mid
    return lo


@device
def env_sample(sh, u1, u2):
    """``(direction, radiance / pdf, pdf)`` for a direction picked in proportion to the light."""
    h = sh.env_density.shape[0]
    w = sh.env_density.shape[1]
    row = _search(sh.env_marginal, h, u1)
    lo = sh.env_marginal[row]
    hi = sh.env_marginal[row + 1]
    fy = (u1 - lo) / (hi - lo) if hi > lo else 0.5
    col = _search(sh.env_conditional[row], w, u2)
    lo = sh.env_conditional[row, col]
    hi = sh.env_conditional[row, col + 1]
    fx = (u2 - lo) / (hi - lo) if hi > lo else 0.5
    u = (col + min(max(fx, 0.0), 1.0)) / w
    v = (row + min(max(fy, 0.0), 1.0)) / h
    phi = (u - 0.5) * TWO_PI
    theta = v * PI
    st = math.sin(theta)
    local = (st * math.sin(phi), math.cos(theta), -st * math.cos(phi))
    d = _env_world(sh.env_rotation, local)
    if st <= 1e-12:
        return d, (0.0, 0.0, 0.0), 0.0
    pdf = sh.env_density[row, col] / (2.0 * PI * PI * st)
    if pdf <= 0.0:
        return d, (0.0, 0.0, 0.0), 0.0
    c = map_lookup(sh.env_rgb, u, v)
    s = sh.env_scale / pdf
    return d, (c[0] * s, c[1] * s, c[2] * s), pdf


@device
def power_heuristic(a, b):
    a2 = a * a
    b2 = b * b
    if a2 + b2 <= 0.0:
        return 0.0
    return a2 / (a2 + b2)
