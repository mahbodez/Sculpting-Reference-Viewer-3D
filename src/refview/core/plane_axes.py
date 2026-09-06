"""Reading the planes of a form out of the model's own normals.

The grid quantiser in the shader imposes the same set of directions on every
model: a cube, bevelled as far as the detail slider asks.  That is how a
sculptor blocks a form in before they have looked at it.  Once they have, the
planes they choose are the ones the form actually has -- the plane of the
cheek, the plane under the brow -- and those are particular to the model.

This finds them.  Every vertex normal is a point on the sphere, weighted by
how much surface it stands for, and that cloud is split along its principal
axes: the covariance of a group of normals is taken, the direction of greatest
spread is its first principal component, and the group is cut in half across
it.  The group with the most spread left in it is always the one cut next, so
the first few directions are the big planes of the form and the later ones are
refinements of them.  Splitting stops at :data:`MAX_PLANE_AXES`, and every
count along the way is kept, so the panel's slider can pick up any of them
without the work being done again.
"""

from __future__ import annotations

import typing

import numpy as np

if typing.TYPE_CHECKING:  # pragma: no cover - import cost, not behaviour
    from .mesh import Mesh

#: The most directions this will ever pull out of a model.  Past this a plane
#: is smaller than the eye reads as a plane, and the grid mode is the better
#: tool for a finely faceted surface anyway.
MAX_PLANE_AXES = 64

#: Normals looked at when splitting.  A dense model says nothing more about
#: its planes than an evenly thinned copy of it does, and the thinning keeps
#: the work off the frame that first turns the mode on.
SAMPLE_LIMIT = 60_000


class PlaneAxes:
    """The directions a model's normals fall into, at every count.

    Built once per mesh.  :meth:`for_count` is what the renderer asks each
    frame, and it is a lookup rather than a fit.
    """

    __slots__ = ("_levels",)

    def __init__(self, levels: list[np.ndarray]) -> None:
        self._levels = levels

    def __len__(self) -> int:
        return len(self._levels)

    @property
    def is_empty(self) -> bool:
        return not self._levels

    def for_count(self, count: int) -> np.ndarray:
        """The best ``count`` directions, or as many as the model supports.

        A model whose normals collapse onto fewer distinct directions than are
        asked for simply gives back what it has, rather than padding the set
        with duplicates that would draw boundaries where the surface is flat.
        """
        if not self._levels:
            return np.zeros((0, 3), dtype=np.float32)
        index = min(max(int(count), 1), len(self._levels)) - 1
        return self._levels[index]


def vertex_weights(mesh: Mesh) -> np.ndarray:
    """How much surface each vertex stands for: a third of each triangle on it.

    Weighting by area rather than by vertex count keeps a densely tessellated
    ear from outvoting the whole side of a head.
    """
    count = mesh.vertex_count
    if count == 0 or mesh.triangle_count == 0:
        return np.ones(count, dtype=np.float64)
    corners = mesh.positions[mesh.indices].astype(np.float64)
    cross = np.cross(corners[:, 1] - corners[:, 0], corners[:, 2] - corners[:, 0])
    areas = np.linalg.norm(cross, axis=1) * 0.5
    weights = np.bincount(
        mesh.indices.ravel(), weights=np.repeat(areas / 3.0, 3), minlength=count
    )
    # A vertex no triangle uses would otherwise drop out of the fit entirely.
    return np.where(weights > 0.0, weights, 1e-12)


def _summarise(
    normals: np.ndarray, weights: np.ndarray, members: np.ndarray
) -> tuple[np.ndarray, float, float]:
    """The plane direction of a group, its spread, and its total weight."""
    group = normals[members]
    mass = weights[members]
    total = float(mass.sum())
    if total <= 0.0:
        return group[0].copy(), 0.0, 0.0
    moment = mass @ group
    length = float(np.linalg.norm(moment))
    # Every normal is a unit vector, so the weighted variance about the mean
    # reduces to this; it is the spread that splitting the group removes.  It
    # has to be measured even when the mean direction below is undefined: a
    # cube's six faces cancel out exactly, and a group reporting no spread is
    # a group that never gets split.
    scatter = max(total - length * length / total, 0.0)
    if length <= 1e-12:
        # Normals that cancel have no one direction, so any of them will do
        # until the group is split -- which, having spread, it will be.
        return group[0].copy(), scatter, total
    return moment / length, scatter, total


def _split(
    normals: np.ndarray, weights: np.ndarray, members: np.ndarray
) -> tuple[np.ndarray, np.ndarray] | None:
    """Cut a group across its first principal component, or refuse to."""
    if len(members) < 2:
        return None
    group = normals[members]
    mass = weights[members]
    total = float(mass.sum())
    if total <= 0.0:
        return None
    centred = group - (mass @ group) / total
    covariance = (centred * mass[:, None]).T @ centred
    # eigh orders ascending, so the last eigenvector is the principal one.
    axis = np.linalg.eigh(covariance)[1][:, -1]
    near = centred @ axis > 0.0
    if not near.any() or near.all():
        # Every normal on one side: the group is a point, not a spread.
        return None
    return members[near], members[~near]


def plane_axes(
    mesh: Mesh, max_count: int = MAX_PLANE_AXES, sample_limit: int = SAMPLE_LIMIT
) -> PlaneAxes:
    """Split the mesh's normals into planes, keeping every count on the way."""
    normals = np.asarray(mesh.normals, dtype=np.float64)
    if len(normals) == 0:
        return PlaneAxes([])
    weights = vertex_weights(mesh)

    lengths = np.linalg.norm(normals, axis=1)
    usable = lengths > 1e-9
    if not usable.any():
        return PlaneAxes([])
    normals = normals[usable] / lengths[usable, None]
    weights = weights[usable]

    if len(normals) > sample_limit:
        # A fixed stride rather than a random draw, so the same model always
        # breaks into the same planes.
        stride = int(np.ceil(len(normals) / sample_limit))
        normals, weights = normals[::stride], weights[::stride]

    everything = np.arange(len(normals))
    direction, scatter, _ = _summarise(normals, weights, everything)
    groups: list[np.ndarray] = [everything]
    directions: list[np.ndarray] = [direction]
    # None marks a group that has already refused to split.
    spreads: list[float | None] = [scatter]
    levels = [np.asarray(directions, dtype=np.float32)]

    while len(groups) < max(int(max_count), 1):
        candidates = [(s, i) for i, s in enumerate(spreads) if s is not None and s > 0.0]
        if not candidates:
            break
        index = max(candidates)[1]
        halves = _split(normals, weights, groups[index])
        if halves is None:
            spreads[index] = None
            continue
        near, far = halves
        near_direction, near_scatter, _ = _summarise(normals, weights, near)
        far_direction, far_scatter, _ = _summarise(normals, weights, far)
        groups[index : index + 1] = [near, far]
        directions[index : index + 1] = [near_direction, far_direction]
        spreads[index : index + 1] = [near_scatter, far_scatter]
        levels.append(np.asarray(directions, dtype=np.float32))

    return PlaneAxes(levels)
