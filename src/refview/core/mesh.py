"""Triangle-mesh containers shared by the loader, the renderer and picking."""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from .spatial import TriangleIndex

if TYPE_CHECKING:  # pragma: no cover - import cycle, types only
    from .skeleton import Rig


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


#: Hands every mesh a number of its own; see :attr:`Mesh.serial`.
_SERIALS = itertools.count(1)


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
        "rig",
        "serial",
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
        rig: Rig | None = None,
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
        #: The skeleton and skin weights the file came with, in this mesh's
        #: own coordinates, or ``None`` for a model that has no bones.  See
        #: :class:`refview.core.skeleton.Rig`.
        self.rig = rig
        #: A number no other mesh in the process has had.  What the renderer
        #: tells one upload from the next by, since a mesh built afresh for
        #: every frame of a drag can land at the address the last one left.
        self.serial = next(_SERIALS)
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
        turn = np.eye(4)
        turn[:3, :3] = rotation
        return Mesh(
            self.positions @ rotation.T.astype(np.float32),
            self.normals @ rotation.T.astype(np.float32),
            self.indices,
            self.name,
            source_offset=rotation @ self.source_offset,
            units=self.units,
            rig=None if self.rig is None else self.rig.transformed(turn),
        )

    def transformed_by(self, matrix: np.ndarray) -> Mesh:
        """Return a copy carried by a full 4x4 -- a move, a turn and a scale together.

        This is how an object is placed in the scene, so unlike
        :meth:`transformed` it cannot assume a rotation: the normals go
        through the inverse transpose and are made unit again, which is what
        keeps them square to a surface that has been stretched.
        """
        matrix = np.asarray(matrix, dtype=np.float64).reshape(4, 4)
        if np.allclose(matrix, np.eye(4)):
            return self
        linear = matrix[:3, :3]
        positions = self.positions.astype(np.float64) @ linear.T + matrix[:3, 3]
        try:
            normal_matrix = np.linalg.inv(linear).T
        except np.linalg.LinAlgError:
            normal_matrix = linear
        normals = self.normals.astype(np.float64) @ normal_matrix.T
        lengths = np.linalg.norm(normals, axis=1, keepdims=True)
        normals = np.where(lengths > 1e-12, normals / np.maximum(lengths, 1e-20), self.normals)
        return Mesh(
            positions.astype(np.float32),
            normals.astype(np.float32),
            self.indices,
            self.name,
            source_offset=self.source_offset,
            units=self.units,
            rig=None if self.rig is None else self.rig.transformed(matrix),
        )

    def recentered(self) -> "Mesh":
        """Return a copy whose bounding-box centre sits at the origin."""
        offset = self.bounds.center
        if np.allclose(offset, 0.0):
            return self
        shift = np.eye(4)
        shift[:3, 3] = -offset
        return Mesh(
            self.positions - offset.astype(np.float32),
            self.normals,
            self.indices,
            self.name,
            source_offset=self.source_offset + offset,
            units=self.units,
            rig=None if self.rig is None else self.rig.transformed(shift),
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


class SmoothingGroups:
    """Which corners of a mesh share a normal under AutoSmooth, worked out once.

    What :func:`auto_smooth` does, split in two so that the expensive half is
    done once.  Which corners belong together depends on how the triangles
    meet and how sharply they turn, and neither changes when the object is
    moved, turned, scaled or posed a little -- so the groups are read off
    the object's own mesh when it arrives, and each frame of a drag only
    sums the face normals of wherever it now stands into them, which costs a
    few hundredths of what finding them did.

    A loaded model shares its vertices between triangles, and one normal a
    vertex can only be smooth; so the shaded mesh gives every corner a vertex
    of its own, which is what lets a corner on a hard edge keep a normal of
    its own side.  The corners are welded by position for the grouping, so a
    seam a loader split for its texture coordinates is joined like any other
    edge.  Nought degrees shades every triangle flat.
    """

    def __init__(self, mesh: Mesh, degrees: float) -> None:
        self.degrees = float(degrees)
        self.corners = np.asarray(mesh.indices, dtype=np.int64).reshape(-1)
        _, welded = np.unique(mesh.positions, axis=0, return_inverse=True)
        face = welded.ravel()[self.corners].reshape(-1, 3)
        # A turn of a hundredth of a degree joins only coplanar neighbours,
        # which gives each triangle its own face normal: flat shading.
        self.root = _corner_groups(face, _face_cross(mesh.positions, self.corners),
                                   max(self.degrees, 0.01))

    def fits(self, mesh: Mesh) -> bool:
        """Whether ``mesh`` is laid out as the one the groups were read from."""
        return mesh.indices.size == self.corners.size

    def shade(self, mesh: Mesh) -> Mesh:
        """``mesh`` -- the one the groups were read from, or it moved or posed -- shaded so."""
        if mesh.triangle_count == 0:
            return mesh
        corners = np.asarray(mesh.indices, dtype=np.int64).reshape(-1)
        cross = _face_cross(mesh.positions, corners)
        return Mesh(
            mesh.positions[corners],
            _group_normals(self.root, cross),
            np.arange(len(corners), dtype=np.int64).reshape(-1, 3),
            mesh.name,
            source_offset=mesh.source_offset,
            units=mesh.units,
        )


def smoothed_by_angle(mesh: Mesh, degrees: float) -> Mesh:
    """Any mesh shaded hard past ``degrees``, smooth short of it: :class:`SmoothingGroups`."""
    if mesh.triangle_count == 0:
        return mesh
    return SmoothingGroups(mesh, degrees).shade(mesh)


def _face_cross(positions: np.ndarray, corners: np.ndarray) -> np.ndarray:
    """Each triangle's edge cross product: its normal, as long as twice its area."""
    held = np.asarray(positions, dtype=np.float64)[corners].reshape(-1, 3, 3)
    return np.cross(held[:, 1] - held[:, 0], held[:, 2] - held[:, 0])


def _corner_groups(face: np.ndarray, cross: np.ndarray, degrees: float) -> np.ndarray:
    """Join the corners of neighbouring triangles that turn by less than ``degrees``.

    ``face`` names each triangle's corners by welded vertex, so that two
    triangles share an edge when they share its ends.  Returns, per corner,
    the corner its group is gathered on.
    """
    length = np.linalg.norm(cross, axis=1)
    unit = cross / np.maximum(length, 1e-20)[:, None]
    corner = np.arange(3 * len(face), dtype=np.int64).reshape(-1, 3)

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
    return _gathered(links, 3 * len(face))


def _group_normals(root: np.ndarray, cross: np.ndarray) -> np.ndarray:
    """Each corner's normal: the area-weighted mean of its group's faces."""
    weighted = np.repeat(cross, 3, axis=0)
    summed = np.stack(
        [np.bincount(root, weights=weighted[:, a], minlength=len(root)) for a in range(3)],
        axis=1,
    )[root]
    reach = np.linalg.norm(summed, axis=1)
    # A group whose normals cancel outright has nothing to say; the triangle's
    # own facing is the answer there, which is what it had before.
    unit = weighted / np.maximum(np.linalg.norm(weighted, axis=1), 1e-20)[:, None]
    return np.where(
        (reach > 1e-12)[:, None], summed / np.maximum(reach, 1e-20)[:, None], unit
    ).astype(np.float32)


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

    ``mesh`` is flat -- a vertex of its own for every corner, as the planar
    stand-ins are built; :class:`SmoothingGroups` does the same for any mesh.
    ``degrees`` of zero joins nothing and gives back the flat shading it was
    handed, which is how the setting is turned off.
    """
    if float(degrees) <= 0.0 or mesh.triangle_count == 0:
        return mesh
    indices = np.asarray(mesh.indices, dtype=np.int64).reshape(-1)
    # Welded, because the flat mesh holds a separate copy of every corner and
    # two triangles only share an edge if they share its ends.
    _, back = np.unique(mesh.positions, axis=0, return_inverse=True)
    face = back.ravel()[indices].reshape(-1, 3)
    cross = _face_cross(mesh.positions, indices)
    root = _corner_groups(face, cross, float(degrees))
    return Mesh(
        mesh.positions,
        _group_normals(root, cross),
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


def concatenated(meshes: list[Mesh], name: str = "scene") -> Mesh:
    """Several meshes as one, in the coordinates they already stand in.

    The units are the first mesh's, since a scene is measured in one unit or
    not at all, and no rig comes through: skin weights name one file's
    joints, and a joined mesh has no one file.
    """
    live = [mesh for mesh in meshes if mesh.vertex_count > 0]
    if not live:
        return Mesh(np.zeros((0, 3)), np.zeros((0, 3)), np.zeros((0, 3)), name)
    if len(live) == 1:
        one = live[0]
        return Mesh(one.positions, one.normals, one.indices, name, units=one.units)
    offsets = np.cumsum([0, *(mesh.vertex_count for mesh in live[:-1])])
    indices = np.concatenate(
        [
            mesh.indices.astype(np.int64) + int(shift)
            for mesh, shift in zip(live, offsets, strict=True)
        ]
    )
    return Mesh(
        np.concatenate([mesh.positions for mesh in live]),
        np.concatenate([mesh.normals for mesh in live]),
        indices,
        name,
        units=live[0].units,
    )


def submesh(mesh: Mesh, triangles: np.ndarray, name: str | None = None) -> Mesh:
    """The triangles of ``mesh`` named by index, with only the vertices they use."""
    triangles = np.asarray(triangles, dtype=np.int64).reshape(-1)
    faces = np.asarray(mesh.indices, dtype=np.int64)[triangles]
    used, compact = np.unique(faces.ravel(), return_inverse=True)
    return Mesh(
        mesh.positions[used],
        mesh.normals[used],
        compact.reshape(-1, 3),
        mesh.name if name is None else name,
        source_offset=mesh.source_offset,
        units=mesh.units,
    )


def loose_parts(mesh: Mesh) -> list[np.ndarray]:
    """The triangles of ``mesh`` gathered into the pieces that touch, largest first.

    Two triangles are one piece when they share a vertex *position* -- welded
    by where the corners are rather than by index, so a file that stores
    every corner three times over still comes out as the solids it draws.
    Each entry is an array of triangle indices; there is one for a mesh that
    is all one piece.
    """
    if mesh.triangle_count == 0:
        return []
    indices = np.asarray(mesh.indices, dtype=np.int64).reshape(-1, 3)
    _, welded = np.unique(mesh.positions, axis=0, return_inverse=True)
    face = welded.ravel()[indices]
    total = int(face.max()) + 1
    links = np.concatenate([face[:, [0, 1]], face[:, [1, 2]]])
    root = _gathered(links, total)
    # The pointer jumping above can leave a chain a step long; one more
    # round of following settles every corner on its group's least name.
    for _ in range(_GROUP_ROUNDS):
        before = root
        root = root[root]
        if np.array_equal(root, before):
            break
    labels = root[face[:, 0]]
    names, counts = np.unique(labels, return_counts=True)
    order = np.argsort(-counts, kind="stable")
    return [np.flatnonzero(labels == names[at]) for at in order]
