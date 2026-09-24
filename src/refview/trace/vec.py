"""Three-vectors as tuples of floats, for the kernels.

numba keeps a tuple of three floats in registers, where a small array would
be a heap allocation per call; these helpers are what the tracer's maths is
written in.  LLVM inlines every one of them.
"""

from __future__ import annotations

import math

from .jit import device

PI = math.pi
INV_PI = 1.0 / math.pi
TWO_PI = 2.0 * math.pi


@device
def v3(x, y, z):
    return (float(x), float(y), float(z))


@device
def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


@device
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


@device
def mul(a, b):
    return (a[0] * b[0], a[1] * b[1], a[2] * b[2])


@device
def scale(a, s):
    return (a[0] * s, a[1] * s, a[2] * s)


@device
def madd(a, b, s):
    """``a + b * s``."""
    return (a[0] + b[0] * s, a[1] + b[1] * s, a[2] + b[2] * s)


@device
def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


@device
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


@device
def length(a):
    return math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])


@device
def normalize(a):
    n = math.sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])
    if n < 1e-30:
        return (0.0, 0.0, 1.0)
    inv = 1.0 / n
    return (a[0] * inv, a[1] * inv, a[2] * inv)


@device
def neg(a):
    return (-a[0], -a[1], -a[2])


@device
def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t)


@device
def vmax(a):
    return max(a[0], max(a[1], a[2]))


@device
def luminance(a):
    return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2]


@device
def clamp(x, lo, hi):
    return min(max(x, lo), hi)


@device
def clamp3(a, lo, hi):
    return (min(max(a[0], lo), hi), min(max(a[1], lo), hi), min(max(a[2], lo), hi))


@device
def smoothstep(e0, e1, x):
    t = min(max((x - e0) / (e1 - e0), 0.0), 1.0)
    return t * t * (3.0 - 2.0 * t)


@device
def basis(n):
    """Two unit tangents that make a right-handed frame with unit ``n``.

    Duff et al.'s branchless construction: continuous everywhere but at one
    pole, and no normalisation needed.
    """
    sign = 1.0 if n[2] >= 0.0 else -1.0
    a = -1.0 / (sign + n[2])
    b = n[0] * n[1] * a
    t = (1.0 + sign * n[0] * n[0] * a, sign * b, -sign * n[0])
    s = (b, sign + n[1] * n[1] * a, -n[1])
    return t, s


@device
def to_world(local, t, s, n):
    return (
        t[0] * local[0] + s[0] * local[1] + n[0] * local[2],
        t[1] * local[0] + s[1] * local[1] + n[1] * local[2],
        t[2] * local[0] + s[2] * local[1] + n[2] * local[2],
    )


@device
def to_local(v, t, s, n):
    return (dot(v, t), dot(v, s), dot(v, n))


@device
def reflect(v, n):
    """``v`` mirrored about ``n``, both pointing away from the surface."""
    d = 2.0 * dot(v, n)
    return (n[0] * d - v[0], n[1] * d - v[1], n[2] * d - v[2])


@device
def cosine_hemisphere(u1, u2):
    r = math.sqrt(u1)
    phi = TWO_PI * u2
    return (r * math.cos(phi), r * math.sin(phi), math.sqrt(max(0.0, 1.0 - u1)))


@device
def srgb_to_linear(c):
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


@device
def linear3(c):
    return (srgb_to_linear(c[0]), srgb_to_linear(c[1]), srgb_to_linear(c[2]))
