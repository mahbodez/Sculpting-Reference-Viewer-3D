"""Triangle-mesh containers shared by the loader, the renderer and picking."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .spatial import TriangleIndex


class MeshLoadError(RuntimeError):
    """Raised when a file cannot be interpreted as a triangle mesh."""


@dataclass(frozen=True)
class MeshUnits:
    """The real-world unit a file declared its coordinates in.

    Only some formats say: glTF is defined in metres, while OBJ and STL carry
    no unit at all.  When a loader knows, the viewer adopts it for measurement
    readouts instead of making the artist guess.
    """

    #: Label shown next to a length, e.g. ``"m"``.
    name: str
    #: Multiplier from scene units to that label.
    scale: float = 1.0


@dataclass(frozen=True)
class Bounds:
    """An axis-aligned bounding box."""

    minimum: np.ndarray
    maximum: np.ndarray

    @classmethod
    def from_points(cls, points: np.ndarray) -> "Bounds":
        pts = np.asarray(points, dtype=np.float64).reshape(-1, 3)
        if pts.size == 0:
            return cls(np.zeros(3), np.zeros(3))
        return cls(pts.min(axis=0), pts.max(axis=0))

    @property
    def center(self) -> np.ndarray:
        return (self.minimum + self.maximum) * 0.5

    @property
    def size(self) -> np.ndarray:
        return self.maximum - self.minimum

    @property
    def diagonal(self) -> float:
        return float(np.linalg.norm(self.size))

    @property
    def radius(self) -> float:
        """Radius of the sphere circumscribing the box (never zero)."""
        return max(self.diagonal * 0.5, 1e-6)


class Mesh:
    """An indexed triangle mesh with per-vertex positions and normals.

    The viewer keeps the model matrix at identity, so mesh coordinates *are*
    world coordinates.  :meth:`recentered` is used at load time to move the
    geometry onto the origin, which makes orbiting and measuring predictable
    regardless of where the artist modelled the object.
    """

    __slots__ = (
        "positions",
        "normals",
        "indices",
        "name",
        "source_offset",
        "units",
        "_bounds",
        "_index",
    )

    def __init__(
        self,
        positions: np.ndarray,
        normals: np.ndarray,
        indices: np.ndarray,
        name: str = "mesh",
        source_offset: np.ndarray | None = None,
        units: MeshUnits | None = None,
    ) -> None:
        self.positions = np.ascontiguousarray(positions, dtype=np.float32).reshape(-1, 3)
        self.normals = np.ascontiguousarray(normals, dtype=np.float32).reshape(-1, 3)
        self.indices = np.ascontiguousarray(indices, dtype=np.uint32).reshape(-1, 3)
        if len(self.normals) != len(self.positions):
            raise ValueError("positions and normals must have the same length")
        if self.indices.size and int(self.indices.max()) >= len(self.positions):
            raise ValueError("index buffer references a missing vertex")
        self.name = name
        self.source_offset = (
            np.zeros(3) if source_offset is None else np.asarray(source_offset, dtype=np.float64)
        )
        self.units = units
        self._bounds: Bounds | None = None
        self._index: TriangleIndex | None = None

    # -- geometry -------------------------------------------------------

    @property
    def vertex_count(self) -> int:
        return len(self.positions)

    @property
    def triangle_count(self) -> int:
        return len(self.indices)

    @property
    def bounds(self) -> Bounds:
        if self._bounds is None:
            self._bounds = Bounds.from_points(self.positions)
        return self._bounds

    @property
    def triangles(self) -> np.ndarray:
        """Expanded triangle corners, shape ``(T, 3, 3)``."""
        return self.positions[self.indices]

    @property
    def spatial_index(self) -> TriangleIndex:
        """Picking accelerator, built on first use and kept for the mesh's life."""
        if self._index is None:
            self._index = TriangleIndex(self.triangles)
        return self._index

    def transformed(self, rotation: np.ndarray) -> "Mesh":
        """Return a copy turned by a 3x3 rotation, e.g. to fix the up axis.

        Rotations leave normals valid as they are, so no inverse-transpose is
        needed; anything that is not a rotation would need one.
        """
        rotation = np.asarray(rotation, dtype=np.float64)
        if np.allclose(rotation, np.eye(3)):
            return self
        return Mesh(
            self.positions @ rotation.T.astype(np.float32),
            self.normals @ rotation.T.astype(np.float32),
            self.indices,
            self.name,
            source_offset=rotation @ self.source_offset,
            units=self.units,
        )

    def recentered(self) -> "Mesh":
        """Return a copy whose bounding-box centre sits at the origin."""
        offset = self.bounds.center
        if np.allclose(offset, 0.0):
            return self
        return Mesh(
            self.positions - offset.astype(np.float32),
            self.normals,
            self.indices,
            self.name,
            source_offset=self.source_offset + offset,
            units=self.units,
        )

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return (
            f"Mesh(name={self.name!r}, vertices={self.vertex_count}, "
            f"triangles={self.triangle_count})"
        )


#: Rounds of pointer jumping allowed when gathering corners into smoothing
#: groups.  Each round squares how far a group can have spread, so this is a
#: formality: a group would have to be wider than the atom count to need them.
_GROUP_ROUNDS = 64


def _gathered(links: np.ndarray, total: int) -> np.ndarray:
    """Which group each of ``total`` things lands in, given pairs that agree.

    Hooking and pointer jumping: each round every thing takes the lowest name
    it can see, and then every name is replaced by the name *it* points at, so
    a chain of any length collapses in a handful of rounds.
    """
    root = np.arange(total)
    if len(links) == 0:
        return root
    for _ in range(_GROUP_ROUNDS):
        before = root.copy()
        np.minimum.at(root, links[:, 0], root[links[:, 1]])
        np.minimum.at(root, links[:, 1], root[links[:, 0]])
        root = root[root]
        if np.array_equal(root, before):
            break
    return root


def auto_smooth(mesh: Mesh, degrees: float) -> Mesh:
    """A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.

    The same thing 3ds Max's AutoSmooth does, and for the same reason.  A form
    built out of flats is meant to read as flats, but a facet that comes out of
    a lattice is only *approximately* one plane: its triangles each lean by a
    fraction of a degree, and flat shading shows every one of those leans as a
    separate tone.  What should read as one clean plane reads as a mosaic.

    So the triangles are gathered into groups -- neighbours joined wherever the
    turn between them is gentler than ``degrees``, which is what a smoothing
    group is -- and each corner takes the average of the normals in its own
    group.  Within a facet that averaging is nearly a no-op geometrically and
    removes the mosaic entirely.  Across a real plane change the turn is too
    sharp to join, so the two sides stay in different groups, keep different
    normals at the shared corner, and the edge stays every bit as hard as it
    was.  Nothing moves: this is a change of shading and not of shape.

    ``degrees`` of zero joins nothing and gives back the flat shading it was
    handed, which is how the setting is turned off.
    """
    if float(degrees) <= 0.0 or mesh.triangle_count == 0:
        return mesh
    indices = np.asarray(mesh.indices, dtype=np.int64).reshape(-1, 3)
    # Welded, because the flat mesh holds a separate copy of every corner and
    # two triangles only share an edge if they share its ends.
    _, back = np.unique(mesh.positions, axis=0, return_inverse=True)
    face = back.ravel()[indices]
    corner = np.arange(3 * len(face), dtype=np.int64).reshape(-1, 3)

    points = np.asarray(mesh.positions, dtype=np.float64)
    held = points[indices]
    cross = np.cross(held[:, 1] - held[:, 0], held[:, 2] - held[:, 0])
    length = np.linalg.norm(cross, axis=1)
    unit = cross / np.maximum(length, 1e-20)[:, None]

    # Every edge of every triangle, named by its two ends in a fixed order so
    # that the same edge of two triangles is written the same way.
    ends = np.concatenate([face[:, [0, 1]], face[:, [1, 2]], face[:, [2, 0]]])
    slots = np.concatenate([corner[:, [0, 1]], corner[:, [1, 2]], corner[:, [2, 0]]])
    turned = ends[:, 0] > ends[:, 1]
    ends = np.where(turned[:, None], ends[:, ::-1], ends)
    slots = np.where(turned[:, None], slots[:, ::-1], slots)
    owner = np.tile(np.arange(len(face), dtype=np.int64), 3)

    _, named, counts = np.unique(ends, axis=0, return_inverse=True, return_counts=True)
    named = named.ravel()
    order = np.argsort(named, kind="stable")
    starts = np.searchsorted(named[order], np.arange(len(counts)))
    # Only edges with exactly two triangles on them: an open edge has nothing
    # to average with, and one with three or more is not a surface, so leaving
    # it hard is both the safe answer and the honest one.
    paired = np.flatnonzero(counts == 2)
    here, there = order[starts[paired]], order[starts[paired] + 1]
    gentle = np.einsum("ij,ij->i", unit[owner[here]], unit[owner[there]]) >= math.cos(
        math.radians(min(float(degrees), 180.0))
    )
    links = np.concatenate(
        [
            np.stack([slots[here, 0], slots[there, 0]], axis=1)[gentle],
            np.stack([slots[here, 1], slots[there, 1]], axis=1)[gentle],
        ]
    )

    root = _gathered(links, 3 * len(face))
    weighted = np.repeat(cross, 3, axis=0)
    summed = np.stack(
        [np.bincount(root, weights=weighted[:, a], minlength=len(root)) for a in range(3)],
        axis=1,
    )[root]
    reach = np.linalg.norm(summed, axis=1)
    # A group whose normals cancel outright has nothing to say; the triangle's
    # own facing is the answer there, which is what it had before.
    normals = np.where(
        (reach > 1e-12)[:, None],
        summed / np.maximum(reach, 1e-20)[:, None],
        np.repeat(unit, 3, axis=0),
    )
    return Mesh(
        mesh.positions,
        normals.astype(np.float32),
        mesh.indices,
        mesh.name,
        source_offset=mesh.source_offset,
        units=mesh.units,
    )


def compute_vertex_normals(positions: np.ndarray, indices: np.ndarray) -> np.ndarray:
    """Area-weighted smooth vertex normals for an indexed triangle soup."""
    positions = np.asarray(positions, dtype=np.float64).reshape(-1, 3)
    indices = np.asarray(indices, dtype=np.int64).reshape(-1, 3)
    normals = np.zeros_like(positions)
    if indices.size:
        a, b, c = (positions[indices[:, i]] for i in range(3))
        face_normals = np.cross(b - a, c - a)
        for i in range(3):
            np.add.at(normals, indices[:, i], face_normals)
    lengths = np.linalg.norm(normals, axis=1, keepdims=True)
    np.divide(normals, np.maximum(lengths, 1e-20), out=normals)
    return normals.astype(np.float32)
