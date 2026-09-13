"""Convex solids from points: the hull, a cut through it, and its mesh.

A primary form -- the bucket of a pelvis, the egg of a ribcage, the wedge of a
head -- is a handful of convex solids and nothing else.  Each is either the
hull of some points (a ring sampled round a rim, an ellipsoid sampled over its
surface, the landmarks themselves) or such a hull with a plane cut through it,
and a form is the union of a few of them.  That is the same representation the
clay modes work in, and it is enough for anything a block-in has to say: the
one non-convex thing a primary form ever needs, the arch chipped out of the
front of the ribcage, is two cut pieces of one egg laid over each other.

So this is deliberately small.  A hull, built one point at a time; a cut,
which is the hull of what survives the plane plus where the edges crossed it;
a test for whether a point is inside; a flat-shaded mesh; and a rounded hull,
which bows each face of the flat one out into a cubic patch and hulls the
result, for the forms that are muscle and fat rather than bone.  Nothing here
knows what a pelvis is.

The hull is the plain incremental algorithm: each point in turn is either
inside the hull so far or can see some of its faces, and the faces it can see
are replaced by a cone of new ones from the rim of that view.  Points on the
plane of a face are counted as not seeing it, so a flat cap sampled round its
edge comes out as one coplanar fan rather than a fold.  A few hundred points
take a few milliseconds, which is all a form ever has.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .mesh import Mesh

#: How far past a face a point has to lie before it counts as seeing it, as a
#: share of the cloud's longest side.  Loose enough that a point lying on a
#: cap plane to within rounding does not carve a sliver off the cap.
_ABOVE_SHARE = 1e-7

#: Fewer points than this cannot enclose a volume.
_MIN_POINTS = 4

#: How many spans each edge of a hull face is split into when the hull is
#: rounded: four gives fifteen samples a face, enough that the bow between
#: two landmarks turns in steps of well under ten degrees and reads as a
#: curve once the facets are smoothed.
ROUND_SAMPLES = 4


class DegenerateHullError(ValueError):
    """The points are flat, collinear or too few to hold any volume."""


def _unit(vector: np.ndarray) -> np.ndarray:
    length = float(np.linalg.norm(vector))
    return vector / length if length > 0.0 else vector


def _seed(points: np.ndarray, above: float) -> tuple[int, int, int, int]:
    """Four points spanning a volume, or a :class:`DegenerateHullError`."""
    first, second = 0, 0
    widest = -1.0
    for axis in range(3):
        low, high = int(np.argmin(points[:, axis])), int(np.argmax(points[:, axis]))
        span = float(points[high, axis] - points[low, axis])
        if span > widest:
            first, second, widest = low, high, span
    if widest <= above:
        raise DegenerateHullError("every point is the same point")
    along = _unit(points[second] - points[first])
    offset = points - points[first]
    aside = np.linalg.norm(offset - np.outer(offset @ along, along), axis=1)
    third = int(np.argmax(aside))
    if float(aside[third]) <= above:
        raise DegenerateHullError("every point lies on one line")
    normal = _unit(np.cross(points[second] - points[first], points[third] - points[first]))
    height = np.abs(offset @ normal)
    fourth = int(np.argmax(height))
    if float(height[fourth]) <= above:
        raise DegenerateHullError("every point lies on one plane")
    return first, second, third, fourth


def _outward(points: np.ndarray, face: tuple[int, int, int], inside: np.ndarray) -> tuple:
    """``face`` wound so that its normal points away from ``inside``."""
    a, b, c = face
    normal = np.cross(points[b] - points[a], points[c] - points[a])
    return (a, c, b) if float(normal @ (inside - points[a])) > 0.0 else (a, b, c)


def convex_hull(points) -> tuple[np.ndarray, np.ndarray]:
    """The hull of a cloud, as ``(vertices, faces)`` with the faces wound outward.

    The vertices are the points themselves, deduplicated; a point that ended
    up inside is simply referenced by no face.  Raises :class:`DegenerateHullError`
    when the cloud is flat or too small to hold any volume.
    """
    cloud = np.unique(np.asarray(points, dtype=np.float64).reshape(-1, 3), axis=0)
    if len(cloud) < _MIN_POINTS:
        raise DegenerateHullError("fewer than four distinct points")
    above = _ABOVE_SHARE * float(np.ptp(cloud, axis=0).max())
    first, second, third, fourth = _seed(cloud, above)
    inside = cloud[[first, second, third, fourth]].mean(axis=0)
    faces = [
        _outward(cloud, face, inside)
        for face in (
            (first, second, third),
            (first, second, fourth),
            (first, third, fourth),
            (second, third, fourth),
        )
    ]

    for index in range(len(cloud)):
        if index in (first, second, third, fourth):
            continue
        point = cloud[index]
        held = np.asarray(faces, dtype=np.int64)
        corners = cloud[held]
        normals = np.cross(corners[:, 1] - corners[:, 0], corners[:, 2] - corners[:, 0])
        normals /= np.maximum(np.linalg.norm(normals, axis=1), 1e-300)[:, None]
        seen = np.einsum("ij,ij->i", normals, point - corners[:, 0]) > above
        if not seen.any():
            continue
        # The rim of what the point can see: every directed edge of a seen
        # face whose reverse is not also on a seen face.
        edges: set[tuple[int, int]] = set()
        for a, b, c in held[seen]:
            edges.update(((int(a), int(b)), (int(b), int(c)), (int(c), int(a))))
        rim = [edge for edge in edges if (edge[1], edge[0]) not in edges]
        faces = [face for face, visible in zip(faces, seen, strict=True) if not visible]
        faces.extend((a, b, index) for a, b in rim)

    face = np.asarray(faces, dtype=np.int64).reshape(-1, 3)
    corners = cloud[face]
    area = np.linalg.norm(
        np.cross(corners[:, 1] - corners[:, 0], corners[:, 2] - corners[:, 0]), axis=1
    )
    return cloud, face[area > 0.0]


def vertex_normals(vertices: np.ndarray, faces: np.ndarray) -> np.ndarray:
    """The outward unit normal at each vertex: the area-weighted mean of its faces'.

    A vertex no face references -- a point that ended up inside the hull --
    gets a zero normal, which is the honest answer.
    """
    corners = vertices[faces]
    normals = np.cross(corners[:, 1] - corners[:, 0], corners[:, 2] - corners[:, 0])
    out = np.zeros_like(vertices, dtype=np.float64)
    for corner in range(3):
        np.add.at(out, faces[:, corner], normals)
    return out / np.maximum(np.linalg.norm(out, axis=1), 1e-300)[:, None]


def _patch_samples(samples: int) -> np.ndarray:
    """The barycentric ``(w, u, v)`` of an even grid over a triangle."""
    grid = [
        (i / samples, j / samples, (samples - i - j) / samples)
        for i in range(samples + 1)
        for j in range(samples + 1 - i)
    ]
    return np.asarray(grid, dtype=np.float64)


def rounded_hull(points, samples: int = ROUND_SAMPLES) -> tuple[np.ndarray, np.ndarray]:
    """The hull of the points with every face bowed out into a cubic patch.

    A flat hull is planes meeting at edges, which is right for bone and wrong
    for a muscle or a breast.  So each face of it is replaced by a curved
    triangle -- Vlachos's point-normal triangle: the cubic Bezier patch that
    passes through the face's three corners and lies tangent at each to the
    surface's normal there, the normal being the mean of the faces that meet
    at the corner.  The patches are sampled and the samples hulled again, so
    the result is still convex and still passes through every corner of the
    flat hull: the landmarks stay on the clay, and the clay swells between
    them instead of running straight.

    Raises :class:`DegenerateHullError` as :func:`convex_hull` does.
    """
    vertices, faces = convex_hull(points)
    normals = vertex_normals(vertices, faces)
    corner = vertices[faces]  # (faces, 3, 3)
    normal = normals[faces]

    def toward(a: int, b: int) -> np.ndarray:
        """The control point a third of the way from ``a`` to ``b``, in ``a``'s tangent plane."""
        step = corner[:, b] - corner[:, a]
        lean = np.einsum("ij,ij->i", step, normal[:, a])[:, None] * normal[:, a]
        return (2.0 * corner[:, a] + corner[:, b] - lean) / 3.0

    b300, b030, b003 = corner[:, 0], corner[:, 1], corner[:, 2]
    b210, b120 = toward(0, 1), toward(1, 0)
    b021, b012 = toward(1, 2), toward(2, 1)
    b102, b201 = toward(2, 0), toward(0, 2)
    edge_mean = (b210 + b120 + b021 + b012 + b102 + b201) / 6.0
    b111 = edge_mean + (edge_mean - (b300 + b030 + b003) / 3.0) * 0.5

    w, u, v = _patch_samples(samples).T
    basis = np.stack(
        [
            w**3,
            u**3,
            v**3,
            3.0 * w * w * u,
            3.0 * w * u * u,
            3.0 * u * u * v,
            3.0 * u * v * v,
            3.0 * w * v * v,
            3.0 * w * w * v,
            6.0 * w * u * v,
        ],
        axis=1,
    )
    control = np.stack([b300, b030, b003, b210, b120, b021, b012, b102, b201, b111], axis=1)
    patched = np.einsum("sc,fcd->fsd", basis, control).reshape(-1, 3)
    return convex_hull(np.concatenate([vertices, patched]))


@dataclass(frozen=True)
class Solid:
    """One convex piece of a form: its hull vertices and outward-wound faces."""

    vertices: np.ndarray
    faces: np.ndarray

    @classmethod
    def from_points(cls, points) -> Solid:
        vertices, faces = convex_hull(points)
        return cls(vertices, faces)

    @classmethod
    def rounded(cls, points, samples: int = ROUND_SAMPLES) -> Solid:
        """The hull of the points with its faces bowed out; see :func:`rounded_hull`."""
        vertices, faces = rounded_hull(points, samples)
        return cls(vertices, faces)

    @property
    def planes(self) -> tuple[np.ndarray, np.ndarray]:
        """Every face as a unit normal and an offset, ``normal @ x <= offset`` inside."""
        corners = self.vertices[self.faces]
        normals = np.cross(corners[:, 1] - corners[:, 0], corners[:, 2] - corners[:, 0])
        normals /= np.maximum(np.linalg.norm(normals, axis=1), 1e-300)[:, None]
        return normals, np.einsum("ij,ij->i", normals, corners[:, 0])

    @property
    def extent(self) -> float:
        """The longest side of the box the solid sits in."""
        return float(np.ptp(self.vertices, axis=0).max()) if len(self.vertices) else 0.0

    def contains(self, point, slack: float = 0.0) -> bool:
        """Whether a point lies inside, or within ``slack`` of the surface."""
        normals, offsets = self.planes
        return bool(np.all(normals @ np.asarray(point, dtype=np.float64) <= offsets + slack))

    def volume(self) -> float:
        corners = self.vertices[self.faces]
        return float(
            abs(np.einsum("ij,ij->i", corners[:, 0], np.cross(corners[:, 1], corners[:, 2])).sum())
            / 6.0
        )

    def cut(self, normal, offset: float) -> Solid | None:
        """What is left on the ``normal @ x <= offset`` side of a plane.

        The hull of the vertices that side of the plane together with the
        points where the edges crossed it -- which is the whole intersection,
        since a convex solid cut by a plane is convex.  ``None`` when the plane
        took everything, or left too little to hold a volume.
        """
        normal = _unit(np.asarray(normal, dtype=np.float64))
        depth = self.vertices @ normal - float(offset)
        slack = _ABOVE_SHARE * max(self.extent, 1e-300)
        kept = [self.vertices[depth <= slack]]
        edges = np.unique(
            np.sort(
                np.concatenate(
                    [self.faces[:, [0, 1]], self.faces[:, [1, 2]], self.faces[:, [2, 0]]]
                ),
                axis=1,
            ),
            axis=0,
        )
        start, stop = depth[edges[:, 0]], depth[edges[:, 1]]
        crossing = (start > slack) != (stop > slack)
        if crossing.any():
            a, b = start[crossing], stop[crossing]
            share = a / np.where(np.abs(a - b) > 1e-300, a - b, 1.0)
            first, second = self.vertices[edges[crossing, 0]], self.vertices[edges[crossing, 1]]
            kept.append(first + (second - first) * share[:, None])
        try:
            return Solid.from_points(np.concatenate(kept))
        except DegenerateHullError:
            return None

    def mesh(self, name: str = "form") -> Mesh:
        """A flat-shaded mesh, every triangle with its own three corners.

        Corners are not shared between faces so each facet reads as one plane;
        :func:`~refview.core.mesh.auto_smooth` welds them back together where
        the artist wants the turn between two facets to read as a curve.
        """
        return flat_mesh(self.vertices[self.faces], name)


def flat_mesh(corners: np.ndarray, name: str = "form") -> Mesh:
    """A mesh from ``(n, 3, 3)`` triangle corners, shaded flat per triangle."""
    corners = np.asarray(corners, dtype=np.float64).reshape(-1, 3, 3)
    cross = np.cross(corners[:, 1] - corners[:, 0], corners[:, 2] - corners[:, 0])
    length = np.linalg.norm(cross, axis=1)
    keep = length > 1e-300
    corners, cross, length = corners[keep], cross[keep], length[keep]
    normal = cross / length[:, None]
    return Mesh(
        corners.reshape(-1, 3).astype(np.float32),
        np.repeat(normal, 3, axis=0).astype(np.float32),
        np.arange(3 * len(corners), dtype=np.uint32).reshape(-1, 3),
        name,
    )


def merged(meshes: list[Mesh], name: str = "forms") -> Mesh | None:
    """Several flat meshes as one, or ``None`` when there is nothing to draw."""
    live = [mesh for mesh in meshes if mesh.triangle_count > 0]
    if not live:
        return None
    positions = np.concatenate([mesh.positions for mesh in live])
    normals = np.concatenate([mesh.normals for mesh in live])
    offsets = np.cumsum([0, *(mesh.vertex_count for mesh in live[:-1])])
    indices = np.concatenate(
        [
            mesh.indices.astype(np.int64) + int(shift)
            for mesh, shift in zip(live, offsets, strict=True)
        ]
    )
    return Mesh(positions, normals, indices, name)
