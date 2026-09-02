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

    candidates = mesh.spatial_index.candidates(origin, direction)
    if candidates.size == 0:
        return None

    # Only the candidate triangles are expanded to float64; on a large mesh
    # materialising the whole corner array per ray costs far more than the
    # intersection maths does.
    corners = mesh.positions[mesh.indices[candidates]].astype(np.float64)
    v0, v1, v2 = corners[:, 0], corners[:, 1], corners[:, 2]
    edge1 = v1 - v0
    edge2 = v2 - v0

    pvec = np.cross(direction, edge2)
    det = np.einsum("ij,ij->i", edge1, pvec)
    valid = np.abs(det) > _EPSILON
    if not valid.any():
        return None

    inv_det = np.zeros_like(det)
    inv_det[valid] = 1.0 / det[valid]

    tvec = origin - v0
    u = np.einsum("ij,ij->i", tvec, pvec) * inv_det
    valid &= (u >= 0.0) & (u <= 1.0)
    if not valid.any():
        return None

    qvec = np.cross(tvec, edge1)
    v = (qvec @ direction) * inv_det
    valid &= (v >= 0.0) & (u + v <= 1.0)
    if not valid.any():
        return None

    t = np.einsum("ij,ij->i", edge2, qvec) * inv_det
    valid &= t > 1e-9
    if not valid.any():
        return None

    reachable = np.flatnonzero(valid)
    best = int(reachable[np.argmin(t[reachable])])
    distance = float(t[best])
    point = origin + direction * distance

    normal = np.cross(edge1[best], edge2[best])
    length = float(np.linalg.norm(normal))
    normal = normal / length if length > _EPSILON else np.array([0.0, 0.0, 1.0])
    if float(np.dot(normal, direction)) > 0.0:
        normal = -normal
    return Hit(point=point, normal=normal, triangle=int(candidates[best]), distance=distance)


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
