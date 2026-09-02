"""Triangle-mesh containers shared by the loader, the renderer and picking."""

from __future__ import annotations

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
