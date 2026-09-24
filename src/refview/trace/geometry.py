"""The scene's triangles as the kernels see them, and the rays cast through them.

The bounding-volume hierarchy is built by :func:`refview.core.bvh.build_bvh`,
the same builder the viewport's skin refinement uses; :func:`flatten` lays it
out for the CPU.  Each node holds both of its children's boxes, so a ray
tests the two together, walks into the nearer and keeps the farther on a
stack with the distance it was entered at -- a node whose entry lies beyond
the nearest hit found since is dropped unopened.

Triangles are kept as their three corners in single precision and tested in
double (Moller and Trumbore).  Neighbouring triangles compute their shared
edge from the very same two corners, so a ray along an edge cannot slip
between them, which is what lets a subsurface probe or a shadow ray trust a
closed mesh to stay closed.

Two things are decided per hit, not per triangle.  The section planes cut
away every hit beyond them, as the viewport's do, and where a ray entering
the kept side first meets the inside of the model, it meets the cut face --
the cap -- instead.  A ghosted object is see-through by chance: a hit on it
counts with the object's opacity as its probability, so over the samples it
is exactly as solid as it is drawn.
"""

from __future__ import annotations

import math
from typing import NamedTuple

import numpy as np

from ..core.bvh import build_bvh
from .jit import device, kernel
from .sampler import hash_float
from .vec import cross, dot, sub

#: Deepest the traversal stack can go.  The builder splits by area, and only
#: the farther child of each node on the way down is ever held.
STACK_SIZE = 64
#: Returned in place of a triangle for a hit on the section's cut face.
CAP_HIT = -2
MISS = -1


class Geometry(NamedTuple):
    #: Per interior node, both children's boxes: ``(nodes, 2, 3)``.
    node_low: np.ndarray
    node_high: np.ndarray
    #: Per child: an interior node's row, or ``-1 - first`` for a leaf of
    #: triangles ``first`` to ``first + count``.
    node_ref: np.ndarray
    node_count: np.ndarray
    #: Triangle corners and vertex normals, in tree order: ``(triangles, 3, 3)``.
    corners: np.ndarray
    normals: np.ndarray
    #: Material row of each triangle.
    material: np.ndarray
    #: The chance a ray stops at the triangle rather than passing through.
    opacity: np.ndarray
    #: Section half-spaces, ``(planes, 4)``: a point is cut away where
    #: ``dot(p, n) > offset``.
    planes: np.ndarray
    #: The material of the cut face, or ``-1`` for no cap.
    cap_material: int
    #: The scene's centre and radius, for the ray offsets and the camera.
    center: np.ndarray
    radius: float


def empty_geometry() -> Geometry:
    return flatten(np.zeros((0, 3, 3)), np.zeros((0, 3, 3)), np.zeros(0, np.int32),
                   np.ones(0, np.float32), np.zeros((0, 4)), -1)


def flatten(corners: np.ndarray, normals: np.ndarray, material: np.ndarray,
            opacity: np.ndarray, planes: np.ndarray, cap_material: int,
            leaf_size: int = 4, max_leaf: int = 8) -> Geometry:
    """Build the tree over ``(triangles, 3, 3)`` corners and lay it out for the kernels."""
    corners = np.asarray(corners, dtype=np.float64).reshape(-1, 3, 3)
    count = len(corners)
    planes = np.ascontiguousarray(np.asarray(planes, dtype=np.float64).reshape(-1, 4))
    if count:
        low_all, high_all = corners.min(axis=(0, 1)), corners.max(axis=(0, 1))
        center = (low_all + high_all) * 0.5
        radius = max(float(np.linalg.norm(high_all - low_all)) * 0.5, 1e-9)
    else:
        center, radius = np.zeros(3), 1.0
    if count == 0:
        # A root with two empty boxes: every ray misses.
        node_low = np.full((1, 2, 3), 3.0e38, np.float32)
        node_high = np.full((1, 2, 3), -3.0e38, np.float32)
        node_ref = np.full((1, 2), -1, np.int32)
        node_count = np.zeros((1, 2), np.int32)
        return Geometry(node_low, node_high, node_ref, node_count,
                        np.zeros((0, 3, 3), np.float32), np.zeros((0, 3, 3), np.float32),
                        np.zeros(0, np.int32), np.ones(0, np.float32), planes,
                        int(cap_material), center, radius)

    order, low, high, kids, runs = build_bvh(corners.min(axis=1), corners.max(axis=1),
                                             leaf_size=leaf_size, max_leaf=max_leaf)
    interior = np.flatnonzero(kids[:, 0] >= 0)
    if len(interior) == 0:
        # One leaf holds everything: stand a root over it with an empty twin.
        node_low = np.empty((1, 2, 3), np.float32)
        node_high = np.empty((1, 2, 3), np.float32)
        node_low[0, 0], node_high[0, 0] = low[0], high[0]
        node_low[0, 1], node_high[0, 1] = 3.0e38, -3.0e38
        node_ref = np.array([[-1 - runs[0, 0], -1]], np.int32)
        node_count = np.array([[runs[0, 1] - runs[0, 0], 0]], np.int32)
    else:
        row_of = np.full(len(kids), -1, dtype=np.int64)
        row_of[interior] = np.arange(len(interior))
        child = kids[interior]                              # (n, 2)
        node_low = low[child].astype(np.float32)            # (n, 2, 3)
        node_high = high[child].astype(np.float32)
        is_leaf = kids[child, 0] < 0
        node_ref = np.where(is_leaf, -1 - runs[child, 0], row_of[child]).astype(np.int32)
        node_count = np.where(is_leaf, runs[child, 1] - runs[child, 0], 0).astype(np.int32)
        # Single precision rounds a box in or out; widen every box by a hair so
        # a triangle lying on its face is never missed.
        pad = np.float32(radius * 1e-6)
        node_low -= pad
        node_high += pad
    return Geometry(
        np.ascontiguousarray(node_low), np.ascontiguousarray(node_high),
        np.ascontiguousarray(node_ref), np.ascontiguousarray(node_count),
        np.ascontiguousarray(corners[order], dtype=np.float32),
        np.ascontiguousarray(np.asarray(normals, dtype=np.float32).reshape(-1, 3, 3)[order]),
        np.ascontiguousarray(np.asarray(material, dtype=np.int32)[order]),
        np.ascontiguousarray(np.asarray(opacity, dtype=np.float32)[order]),
        planes, int(cap_material), np.asarray(center, dtype=np.float64), float(radius),
    )


def new_stacks() -> tuple[np.ndarray, np.ndarray]:
    """A traversal stack for one thread: node rows and their entry distances."""
    return np.empty(STACK_SIZE, np.int32), np.empty(STACK_SIZE, np.float64)


@device
def clipped(planes, p):
    for i in range(planes.shape[0]):
        if p[0] * planes[i, 0] + p[1] * planes[i, 1] + p[2] * planes[i, 2] > planes[i, 3]:
            return True
    return False


@device
def _slab(geo, node, side, o, inv, t_max):
    lo = geo.node_low[node, side]
    hi = geo.node_high[node, side]
    t0 = (lo[0] - o[0]) * inv[0]
    t1 = (hi[0] - o[0]) * inv[0]
    enter = min(t0, t1)
    leave = max(t0, t1)
    t0 = (lo[1] - o[1]) * inv[1]
    t1 = (hi[1] - o[1]) * inv[1]
    enter = max(enter, min(t0, t1))
    leave = min(leave, max(t0, t1))
    t0 = (lo[2] - o[2]) * inv[2]
    t1 = (hi[2] - o[2]) * inv[2]
    enter = max(enter, min(t0, t1))
    leave = min(leave, max(t0, t1))
    enter = max(enter, 0.0)
    leave = min(leave, t_max)
    return enter, leave


@device
def _triangle(geo, tri, o, d, t_min, t_max):
    """Distance along the ray to ``tri`` and the barycentrics, or ``-1`` for a miss."""
    c = geo.corners[tri]
    p0 = (float(c[0, 0]), float(c[0, 1]), float(c[0, 2]))
    e1 = (float(c[1, 0]) - p0[0], float(c[1, 1]) - p0[1], float(c[1, 2]) - p0[2])
    e2 = (float(c[2, 0]) - p0[0], float(c[2, 1]) - p0[1], float(c[2, 2]) - p0[2])
    q = cross(d, e2)
    det = dot(e1, q)
    if det == 0.0:
        return -1.0, 0.0, 0.0
    inv_det = 1.0 / det
    s = sub(o, p0)
    u = dot(s, q) * inv_det
    if u < 0.0 or u > 1.0:
        return -1.0, 0.0, 0.0
    r = cross(s, e1)
    v = dot(d, r) * inv_det
    if v < 0.0 or u + v > 1.0:
        return -1.0, 0.0, 0.0
    t = dot(e2, r) * inv_det
    if t <= t_min or t >= t_max:
        return -1.0, 0.0, 0.0
    return t, u, v


@device
def _accept(geo, tri, o, d, t, opacity_seed):
    if geo.planes.shape[0] > 0:
        p = (o[0] + d[0] * t, o[1] + d[1] * t, o[2] + d[2] * t)
        if clipped(geo.planes, p):
            return False
    op = geo.opacity[tri]
    if op < 1.0:
        if op <= 0.0:
            return False
        if hash_float(opacity_seed, tri, 0x0DDBA11) >= op:
            return False
    return True


@device
def _traverse(geo, o, d, t_min, t_max, any_hit, opacity_seed, stack, stack_t):
    inv = (
        1.0 / d[0] if d[0] != 0.0 else 1e30,
        1.0 / d[1] if d[1] != 0.0 else 1e30,
        1.0 / d[2] if d[2] != 0.0 else 1e30,
    )
    best = t_max
    found = MISS
    bu = 0.0
    bv = 0.0
    top = 0
    node = 0
    while True:
        ea, xa = _slab(geo, node, 0, o, inv, best)
        eb, xb = _slab(geo, node, 1, o, inv, best)
        hit_a = ea <= xa
        hit_b = eb <= xb
        ref_a = geo.node_ref[node, 0]
        ref_b = geo.node_ref[node, 1]
        if hit_a and ref_a < 0:
            hit_a = False
            first = -1 - ref_a
            for tri in range(first, first + geo.node_count[node, 0]):
                t, u, v = _triangle(geo, tri, o, d, t_min, best)
                if t > 0.0 and _accept(geo, tri, o, d, t, opacity_seed):
                    best, found, bu, bv = t, tri, u, v
                    if any_hit:
                        return found, best, bu, bv
        if hit_b and ref_b < 0:
            hit_b = False
            first = -1 - ref_b
            for tri in range(first, first + geo.node_count[node, 1]):
                t, u, v = _triangle(geo, tri, o, d, t_min, best)
                if t > 0.0 and _accept(geo, tri, o, d, t, opacity_seed):
                    best, found, bu, bv = t, tri, u, v
                    if any_hit:
                        return found, best, bu, bv
        if hit_a and hit_b:
            if ea <= eb:
                near, far, far_t = ref_a, ref_b, eb
            else:
                near, far, far_t = ref_b, ref_a, ea
            if top < STACK_SIZE:
                stack[top] = far
                stack_t[top] = far_t
                top += 1
            node = near
        elif hit_a:
            node = ref_a
        elif hit_b:
            node = ref_b
        else:
            # Pop, skipping anything entered beyond the nearest hit found since.
            node = -1
            while top > 0:
                top -= 1
                if stack_t[top] <= best:
                    node = stack[top]
                    break
            if node < 0:
                break
    return found, best, bu, bv


@device
def intersect(geo, o, d, t_max, opacity_seed, stack, stack_t):
    """The nearest hit along a unit ray: ``(triangle, distance, u, v)``.

    ``triangle`` is :data:`MISS` for nothing, or :data:`CAP_HIT` for the
    section's cut face, whose normal :func:`cap_normal` gives.
    """
    found, best, bu, bv = _traverse(geo, o, d, 0.0, t_max, False, opacity_seed, stack, stack_t)
    if geo.cap_material < 0 or geo.planes.shape[0] == 0:
        return found, best, bu, bv
    # Where does the ray enter the kept side, if it starts cut away?
    enter = 0.0
    for i in range(geo.planes.shape[0]):
        n = (geo.planes[i, 0], geo.planes[i, 1], geo.planes[i, 2])
        side = dot(o, n) - geo.planes[i, 3]
        if side > 0.0:
            along = dot(d, n)
            if along >= 0.0:
                return found, best, bu, bv   # Never enters: there is nothing to cap.
            enter = max(enter, side / -along)
    if enter <= 0.0 or found < 0 or enter >= best:
        return found, best, bu, bv
    # It enters, and the first surface beyond faces away: the entry point is
    # inside the model, so what the ray meets there is the cut face.
    c = geo.corners[found]
    e1 = (float(c[1, 0] - c[0, 0]), float(c[1, 1] - c[0, 1]), float(c[1, 2] - c[0, 2]))
    e2 = (float(c[2, 0] - c[0, 0]), float(c[2, 1] - c[0, 1]), float(c[2, 2] - c[0, 2]))
    if dot(cross(e1, e2), d) > 0.0:
        return CAP_HIT, enter, 0.0, 0.0
    return found, best, bu, bv


@device
def cap_normal(geo, o, d, t):
    """The cut face's normal where a ray met it: the plane it entered through, toward the ray."""
    p = (o[0] + d[0] * t, o[1] + d[1] * t, o[2] + d[2] * t)
    best = 0
    closest = 1e300
    for i in range(geo.planes.shape[0]):
        gap = abs(p[0] * geo.planes[i, 0] + p[1] * geo.planes[i, 1] + p[2] * geo.planes[i, 2]
                  - geo.planes[i, 3])
        if gap < closest:
            closest = gap
            best = i
    return (geo.planes[best, 0], geo.planes[best, 1], geo.planes[best, 2])


@device
def occluded(geo, o, d, t_max, opacity_seed, stack, stack_t):
    """Whether anything lies along a unit ray before ``t_max``."""
    found, _t, _u, _v = _traverse(geo, o, d, 0.0, t_max, True, opacity_seed, stack, stack_t)
    return found >= 0


@device
def surface(geo, tri, u, v):
    """The geometric normal (unnormalised winding order) and the interpolated normal."""
    c = geo.corners[tri]
    e1 = (float(c[1, 0] - c[0, 0]), float(c[1, 1] - c[0, 1]), float(c[1, 2] - c[0, 2]))
    e2 = (float(c[2, 0] - c[0, 0]), float(c[2, 1] - c[0, 1]), float(c[2, 2] - c[0, 2]))
    ng = cross(e1, e2)
    w = 1.0 - u - v
    nv = geo.normals[tri]
    ns = (
        float(nv[0, 0]) * w + float(nv[1, 0]) * u + float(nv[2, 0]) * v,
        float(nv[0, 1]) * w + float(nv[1, 1]) * u + float(nv[2, 1]) * v,
        float(nv[0, 2]) * w + float(nv[1, 2]) * u + float(nv[2, 2]) * v,
    )
    return ng, ns


@device
def offset_origin(p, n, radius):
    """A point nudged off a surface along ``n``, far enough that it cannot hit it again.

    The nudge grows with the point's distance from the origin, since that is
    what the rounding of its coordinates grows with, and never falls below a
    fixed share of the scene, since the corners are single precision.
    """
    size = max(abs(p[0]), max(abs(p[1]), abs(p[2])))
    eps = max(radius * 2e-6, size * 4e-7)
    return (p[0] + n[0] * eps, p[1] + n[1] * eps, p[2] + n[2] * eps)


@device
def safe_normalize(v, fallback):
    n = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    if not n > 1e-30:
        return fallback
    return (v[0] / n, v[1] / n, v[2] / n)


@kernel
def cast_rays(geo, origins, directions, t_max, out_triangle, out_distance):
    """The nearest hit of each of a batch of unit rays; for tests and the benchmark."""
    stack, stack_t = np.empty(STACK_SIZE, np.int32), np.empty(STACK_SIZE, np.float64)
    for i in range(origins.shape[0]):
        o = (origins[i, 0], origins[i, 1], origins[i, 2])
        d = (directions[i, 0], directions[i, 1], directions[i, 2])
        tri, t, _u, _v = intersect(geo, o, d, t_max, i, stack, stack_t)
        out_triangle[i] = tri
        out_distance[i] = t if tri != MISS else -1.0


@kernel
def any_rays(geo, origins, directions, t_max, out_blocked):
    """Whether each of a batch of unit rays is blocked; for tests and the benchmark."""
    stack, stack_t = np.empty(STACK_SIZE, np.int32), np.empty(STACK_SIZE, np.float64)
    for i in range(origins.shape[0]):
        o = (origins[i, 0], origins[i, 1], origins[i, 2])
        d = (directions[i, 0], directions[i, 1], directions[i, 2])
        out_blocked[i] = occluded(geo, o, d, t_max, i, stack, stack_t)
