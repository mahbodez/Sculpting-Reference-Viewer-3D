"""Ray/mesh intersection used by the measuring and annotating tools.

The test itself is a vectorised Moller-Trumbore pass.  It runs only over the
triangles the mesh's :class:`~refview.core.spatial.TriangleIndex` reports as
reachable, which is what keeps hovering and painting responsive once a model
runs into the millions of triangles.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .mesh import Bounds, Mesh

_EPSILON = 1e-12


@dataclass(frozen=True)
class Hit:
    """A point where a ray met the mesh surface."""

    point: np.ndarray
    normal: np.ndarray
    triangle: int
    distance: float


def intersects_bounds(origin: np.ndarray, direction: np.ndarray, bounds: Bounds) -> bool:
    """Slab test against an axis-aligned box; tolerant of axis-parallel rays."""
    with np.errstate(divide="ignore", invalid="ignore"):
        inv = 1.0 / np.where(np.abs(direction) < _EPSILON, _EPSILON, direction)
        t0 = (bounds.minimum - origin) * inv
        t1 = (bounds.maximum - origin) * inv
    t_near = float(np.max(np.minimum(t0, t1)))
    t_far = float(np.min(np.maximum(t0, t1)))
    return t_far >= max(t_near, 0.0)


def raycast_mesh(origin: np.ndarray, direction: np.ndarray, mesh: Mesh) -> Hit | None:
    """Return the closest front- or back-facing hit along the ray, or ``None``."""
    origin = np.asarray(origin, dtype=np.float64)
    direction = np.asarray(direction, dtype=np.float64)
    if mesh.triangle_count == 0 or not intersects_bounds(origin, direction, mesh.bounds):
        return None
    return raycast_many(origin[None], direction[None], mesh)[0]


def raycast_many(origins: np.ndarray, directions: np.ndarray, mesh: Mesh) -> list[Hit | None]:
    """The closest hit along each of a batch of rays, ``None`` where one misses.

    One pass over every ray's candidates together, rather than a pass per
    ray: the overlay asks about every armature node on every frame of an
    orbit, and for two dozen short questions the bookkeeping around the
    maths was costing more than the maths.
    """
    origins = np.asarray(origins, dtype=np.float64).reshape(-1, 3)
    directions = np.asarray(directions, dtype=np.float64).reshape(-1, 3)
    hits: list[Hit | None] = [None] * len(origins)
    if mesh.triangle_count == 0 or len(origins) == 0:
        return hits
    ray, candidates = mesh.spatial_index.candidates_many(origins, directions)
    if candidates.size == 0:
        return hits

    # Only the candidate triangles are expanded to float64; on a large mesh
    # materialising the whole corner array per ray costs far more than the
    # intersection maths does.
    corners = mesh.positions[mesh.indices[candidates]].astype(np.float64)
    v0, v1, v2 = corners[:, 0], corners[:, 1], corners[:, 2]
    edge1 = v1 - v0
    edge2 = v2 - v0
    origin = origins[ray]
    direction = directions[ray]

    pvec = _cross(direction, edge2)
    det = np.einsum("ij,ij->i", edge1, pvec)
    valid = np.abs(det) > _EPSILON
    if not valid.any():
        return hits

    inv_det = np.zeros_like(det)
    inv_det[valid] = 1.0 / det[valid]

    tvec = origin - v0
    u = np.einsum("ij,ij->i", tvec, pvec) * inv_det
    valid &= (u >= 0.0) & (u <= 1.0)
    if not valid.any():
        return hits

    qvec = _cross(tvec, edge1)
    v = np.einsum("ij,ij->i", qvec, direction) * inv_det
    valid &= (v >= 0.0) & (u + v <= 1.0)
    if not valid.any():
        return hits

    t = np.einsum("ij,ij->i", edge2, qvec) * inv_det
    valid &= t > 1e-9
    if not valid.any():
        return hits

    # The nearest reachable triangle of each ray: sort the survivors by ray
    # and then by distance, and the first of every ray's run is its hit.
    reachable = np.flatnonzero(valid)
    reachable = reachable[np.lexsort((t[reachable], ray[reachable]))]
    _, first = np.unique(ray[reachable], return_index=True)
    for best in reachable[first]:
        which = int(ray[best])
        distance = float(t[best])
        point = origins[which] + directions[which] * distance
        normal = np.cross(edge1[best], edge2[best])
        length = float(np.linalg.norm(normal))
        normal = normal / length if length > _EPSILON else np.array([0.0, 0.0, 1.0])
        if float(np.dot(normal, directions[which])) > 0.0:
            normal = -normal
        hits[which] = Hit(
            point=point, normal=normal, triangle=int(candidates[best]), distance=distance
        )
    return hits


def _cross(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Row-wise cross product, without :func:`numpy.cross`'s axis shuffling."""
    out = np.empty_like(a)
    out[:, 0] = a[:, 1] * b[:, 2] - a[:, 2] * b[:, 1]
    out[:, 1] = a[:, 2] * b[:, 0] - a[:, 0] * b[:, 2]
    out[:, 2] = a[:, 0] * b[:, 1] - a[:, 1] * b[:, 0]
    return out


def snap_to_vertex(hit: Hit, mesh: Mesh, max_distance: float) -> np.ndarray:
    """Snap a hit onto the nearest corner of its triangle, when close enough.

    ``max_distance`` is a world-space radius; callers derive it from a pixel
    tolerance so the behaviour stays consistent at any zoom level.
    """
    corners = mesh.positions[mesh.indices[hit.triangle]].astype(np.float64)
    distances = np.linalg.norm(corners - hit.point, axis=1)
    nearest = int(np.argmin(distances))
    if distances[nearest] <= max_distance:
        return corners[nearest]
    return hit.point
