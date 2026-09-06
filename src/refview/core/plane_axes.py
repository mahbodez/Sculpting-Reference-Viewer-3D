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

A fit that reads only the normals cannot tell two parts of a form apart when
they happen to face the same way: the plane of a cheek and the plane of a
temple come back as one direction, and the seam the eye expects between them
never gets drawn.  :mod:`refview.core.plane_clusters` fits planes that carry a
place as well as a direction.  :class:`PlaneSet` is the shape both kinds of
fit arrive in, and a fit with no use for a place simply leaves the place
weighted at zero, which is the same arithmetic the shader was already doing.
"""

from __future__ import annotations

import typing
from dataclasses import dataclass, field

import numpy as np

if typing.TYPE_CHECKING:  # pragma: no cover - import cost, not behaviour
    from .mesh import Mesh

#: The most planes any fit will ever pull out of a model.  The shader reads
#: them out of a texture rather than a uniform array, so this is not bounded by
#: a driver's uniform budget; what bounds it is that past a few hundred a plane
#: is smaller than the eye reads as a plane, and the grid mode is the better
#: tool for a finely faceted surface anyway.
MAX_PLANE_AXES = 256

#: Normals looked at when splitting.  A dense model says nothing more about
#: its planes than an evenly thinned copy of it does, and the thinning keeps
#: the work off the frame that first turns the mode on.
SAMPLE_LIMIT = 60_000


def _empty(columns: int = 3) -> np.ndarray:
    return np.zeros((0, columns) if columns else (0,), dtype=np.float32)


@dataclass(frozen=True)
class Coefficients:
    """What each block of the design matrix counts for, against the normals.

    A fit that clusters the surface reads every vertex as a row of

        [ n ,  locality * p ,  coplanarity * (p . n) ]

    with ``n`` the unit normal and ``p`` the position scaled so the model's
    bounding sphere has radius one.  These are the numbers in front of the
    second and third blocks, so they say how much a step across the form, or
    between two parallel planes, counts against a turn in the surface.  Both
    at zero leaves the normals alone and the fit reads facings only.

    :attr:`flat_span_deg` is not a column but a weight on the rows: how far a
    vertex's neighbours may turn away from it before it stops counting as part
    of a flat.  Narrow it and only the flattest surface has a say in where the
    planes go; widen it and the rounded turns get their say back.

    The same numbers travel through to the shader inside a :class:`PlaneSet`,
    so a fragment is given to a plane under the measure the fit was made with.
    """

    #: What a whole radius of travel across the form counts for against a
    #: right angle of turn in the surface.  The default is low enough that
    #: facing still leads -- a plane is a direction first -- but high enough
    #: that a form is broken up as well as broken down.
    locality: float = 0.70
    #: What the gap between two parallel planes counts for, on the same scale.
    #: Slightly the stronger by default, because two patches that face alike
    #: and lie in one plane really are one plane of the form however far apart
    #: they sit, and that is the case position alone gets wrong.
    coplanarity: float = 0.80
    #: The turn, in degrees, at which a vertex stops counting as part of a
    #: flat.  Vertices on a rounded transition are ambiguous about which plane
    #: they belong to, and letting them vote at full strength is what tilts a
    #: plane away from the flat it was meant to describe.
    flat_span_deg: float = 30.0

    @property
    def reads_position(self) -> bool:
        """Whether anything but the normals is being read at all."""
        return self.locality > 0.0 or self.coplanarity > 0.0


#: The coefficients a fit uses unless it is told otherwise.  Frozen, so one
#: instance can stand as the default everywhere without being copied about.
DEFAULT_COEFFICIENTS = Coefficients()

#: How far the panel lets each coefficient be pushed.  The tops are well past
#: anything useful on purpose: the point of exposing them is to let a form be
#: argued with, and a setting that only ever looks sensible cannot be.
LOCALITY_RANGE = (0.0, 3.0)
COPLANARITY_RANGE = (0.0, 3.0)
FLAT_SPAN_RANGE = (2.0, 90.0)


@dataclass(frozen=True)
class PlaneSet:
    """One level of a fit: the planes the shader is to quantise against.

    A plane is a direction and, where the fit found one, somewhere that
    direction lives.  A fragment belongs to whichever plane is nearest it
    under

    ``|n - direction|^2 + locality |p - anchor|^2 + coplanarity (p.n - offset)^2``

    where ``p`` is the fragment's position in the normalised frame that
    :attr:`origin` and :attr:`scale` describe.  Both weights at zero leaves
    the nearest direction and nothing else, which is what a fit made purely of
    normals wants, so one rule in the shader serves every mode.
    """

    #: Unit, world space.  ``(k, 3)``.
    directions: np.ndarray
    #: Where each plane sits, in the normalised frame.  ``(k, 3)``.
    anchors: np.ndarray = field(default_factory=_empty)
    #: Origin to plane distance along the direction, normalised.  ``(k,)``.
    offsets: np.ndarray = field(default_factory=lambda: _empty(0))
    #: What a step across the form counts for against a step of direction.
    locality: float = 0.0
    #: What the gap between two parallel planes counts for.
    coplanarity: float = 0.0
    #: World point the normalised frame is measured from.
    origin: np.ndarray = field(default_factory=lambda: np.zeros(3, dtype=np.float32))
    #: World units to normalised units.
    scale: float = 1.0

    def __len__(self) -> int:
        return len(self.directions)

    @classmethod
    def empty(cls) -> PlaneSet:
        return cls(directions=_empty())

    @classmethod
    def from_directions(cls, directions: list[np.ndarray] | np.ndarray) -> PlaneSet:
        """A level with no place in it: nearest direction wins, as before."""
        packed = np.asarray(directions, dtype=np.float32).reshape(-1, 3)
        return cls(
            directions=packed,
            anchors=np.zeros_like(packed),
            offsets=np.zeros(len(packed), dtype=np.float32),
        )


class PlaneAxes:
    """The planes a model falls into, at every count.

    Built once per mesh and per mode.  :meth:`for_count` is what the renderer
    asks each frame, and it is a lookup rather than a fit.
    """

    __slots__ = ("_levels",)

    def __init__(self, levels: list[PlaneSet]) -> None:
        self._levels = levels

    def __len__(self) -> int:
        return len(self._levels)

    @property
    def is_empty(self) -> bool:
        return not self._levels

    def for_count(self, count: int) -> PlaneSet:
        """The best ``count`` planes, or as many as the model supports.

        A model whose surface collapses onto fewer distinct planes than are
        asked for simply gives back what it has, rather than padding the set
        with duplicates that would draw boundaries where the surface is flat.
        """
        if not self._levels:
            return PlaneSet.empty()
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
    levels = [PlaneSet.from_directions(directions)]

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
        levels.append(PlaneSet.from_directions(directions))

    return PlaneAxes(levels)
