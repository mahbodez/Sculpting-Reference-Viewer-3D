"""Primary rays: the pixel filter, the lens, and the two projections.

The pixel filter is importance-sampled rather than splatted: each sample
lands at an offset drawn in proportion to the filter's weight and counts
fully toward its own pixel alone.  No sample reaches into a neighbour's
pixel, so tiles rendered on different threads never write the same memory,
and a bucket render is the same as a progressive one.  The filters are
separable, so an offset is a pair of draws from a one-dimensional table.
"""

from __future__ import annotations

import math

import numpy as np

from ..core.path_trace import PixelFilter
from .jit import device

FILTER_TABLE_SIZE = 256


def filter_table(kind: PixelFilter, width: float) -> np.ndarray:
    """The inverse cumulative distribution of a separable filter, as offsets in pixels.

    Entry ``i`` is the offset below which ``i / (size - 1)`` of the filter's
    weight lies; the kernel interpolates between entries.
    """
    radius = max(float(width), 0.5) * 0.5
    if kind is PixelFilter.BOX:
        return np.linspace(-radius, radius, FILTER_TABLE_SIZE + 1)
    x = np.linspace(-radius, radius, 4097)
    if kind is PixelFilter.GAUSSIAN:
        sigma = radius / 2.0
        weight = np.exp(-0.5 * (x / sigma) ** 2)
    else:
        # Blackman-Harris over the filter's width.
        t = (x + radius) / (2.0 * radius)
        weight = (0.35875 - 0.48829 * np.cos(2 * np.pi * t) + 0.14128 * np.cos(4 * np.pi * t)
                  - 0.01168 * np.cos(6 * np.pi * t))
    weight = np.maximum(weight, 0.0)
    cdf = np.concatenate([[0.0], np.cumsum((weight[1:] + weight[:-1]) * 0.5)])
    cdf /= cdf[-1]
    return np.interp(np.linspace(0.0, 1.0, FILTER_TABLE_SIZE + 1), cdf, x)


@device
def filter_offset(table, u):
    n = table.shape[0] - 1
    x = u * n
    i = min(int(x), n - 1)
    f = x - i
    return table[i] + (table[i + 1] - table[i]) * f


@device
def camera_ray(prm, x, y, lens_u, lens_v):
    """The ray through film position ``(x, y)`` in pixels, top-left origin."""
    ndc_x = 2.0 * x / prm.width - 1.0
    ndc_y = 1.0 - 2.0 * y / prm.height
    e = prm.cam_origin
    r = prm.cam_right
    u = prm.cam_up
    f = prm.cam_forward
    if prm.ortho:
        sx = ndc_x * prm.ortho_half * prm.aspect
        sy = ndc_y * prm.ortho_half
        o = (e[0] + r[0] * sx + u[0] * sy - f[0] * prm.ortho_back,
             e[1] + r[1] * sx + u[1] * sy - f[1] * prm.ortho_back,
             e[2] + r[2] * sx + u[2] * sy - f[2] * prm.ortho_back)
        return o, (f[0], f[1], f[2])
    sx = ndc_x * prm.tan_half * prm.aspect
    sy = ndc_y * prm.tan_half
    d = (f[0] + r[0] * sx + u[0] * sy, f[1] + r[1] * sx + u[1] * sy,
         f[2] + r[2] * sx + u[2] * sy)
    n = math.sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2])
    d = (d[0] / n, d[1] / n, d[2] / n)
    o = (e[0], e[1], e[2])
    if prm.aperture > 0.0:
        # Thin lens: the point in focus along the pinhole ray stays put; the
        # ray starts from a point of the aperture instead of the pinhole.
        along = prm.focus_distance / max(d[0] * f[0] + d[1] * f[1] + d[2] * f[2], 1e-6)
        focus = (o[0] + d[0] * along, o[1] + d[1] * along, o[2] + d[2] * along)
        rr = prm.aperture * math.sqrt(lens_u)
        phi = 2.0 * math.pi * lens_v
        lx = rr * math.cos(phi)
        ly = rr * math.sin(phi)
        o = (o[0] + r[0] * lx + u[0] * ly, o[1] + r[1] * lx + u[1] * ly,
             o[2] + r[2] * lx + u[2] * ly)
        d = (focus[0] - o[0], focus[1] - o[1], focus[2] - o[2])
        n = math.sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2])
        d = (d[0] / n, d[1] / n, d[2] / n)
    return o, d
