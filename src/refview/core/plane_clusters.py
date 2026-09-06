"""Finding the planes of a form by clustering the surface, not just its normals.

The PCA fit next door reads a model as a cloud of directions and nothing else.
That is enough to find the *set* of planes a form is built from, but not to
find the planes themselves: the top of a shoulder and the top of a head face
the same way, so they arrive as one direction and the shader shades them as
one plane with no seam between.  A sculptor does not see it that way.  A plane
is a patch of surface -- somewhere on the form, of some size, facing some way
-- and two patches facing alike are still two planes.

So the cloud clustered here carries a place as well as a direction.  Each
sampled vertex becomes a row of a design matrix

    [ n ,  locality * p ,  coplanarity * (p . n) ]

with ``n`` the unit normal, ``p`` the position scaled so the model's bounding
sphere has radius one, and ``p . n`` the distance from the origin out to the
tangent plane at that vertex.  The first three columns group by facing, the
next three by whereabouts, and the last one by *lying in the same plane* --
two patches can be near each other and face alike and still belong to
different planes of the form, and that last column is what separates them.
Every row is weighted by the area it stands for and by how flat its
neighbourhood is, so the flats of the form decide where the planes go and the
rounded turns between them follow along rather than dragging a plane off true.

Two clusterings run over that matrix, and they answer to different tastes:

*Regions* over-segments the surface and then merges it back together by Ward's
criterion -- at every step the two clusters that cost the least added variance
are joined.  It is agglomerative, so it yields a whole dendrogram in one pass
and every count from one plane to :data:`~refview.core.plane_axes.MAX_PLANE_AXES`
is a cut of the same tree.  Turning the slider therefore refines the break
rather than rebuilding it, and the count asked for is the count delivered.

*Flats* asks a blunter question, and asks it of the whole model at once: which
single plane does the most surface agree on?  Every patch proposes the plane
it lies in, the proposals are scored by how much surface falls within a
tolerance of them, the winner is taken, its surface is removed, and the
question is asked again of what is left.  That is maximum consensus -- the
same idea RANSAC is built on, minus the guessing, because there are only a few
hundred patches and every one of them can be tried.  It gives the largest flat
of the form first and the next largest after it, so the planes arrive in the
order a sculptor would block them in, and geometry that agrees with nothing is
simply never the winner rather than being averaged into a plane it does not
belong to.  What it does not give is nesting: the tolerance is what the slider
moves, and a finer tolerance re-asks the question rather than subdividing the
last answer.

Density methods -- DBSCAN, mean shift -- were tried first and are the wrong
tool here.  A closed surface is a connected dense manifold: every radius
either chains the whole model into one cluster or shatters it into the
tessellation, with nothing useful in between.  Measured on a sphere, the count
went from one straight to forty-three with no bandwidth in between, which is a
slider that does nothing for most of its travel.  Consensus does not care how
the data connects up, only how much of it agrees, so it is the robust method
that survives contact with a surface.

Both fits are robust in the same way at the end.  A cluster's direction is not
the mean of its normals but an M-estimate of it: the mean is taken, the
members that disagree most with it are down-weighted by Tukey's biweight, and
the mean is taken again.  A handful of stray normals inside a patch therefore
cannot tilt the plane the patch is shaded with.
"""

from __future__ import annotations

import math
import typing
from dataclasses import dataclass

import numpy as np

from .plane_axes import (
    DEFAULT_COEFFICIENTS,
    MAX_PLANE_AXES,
    SAMPLE_LIMIT,
    Coefficients,
    PlaneAxes,
    PlaneSet,
    plane_axes,
    vertex_weights,
)
from .settings import PlaneMode

if typing.TYPE_CHECKING:  # pragma: no cover - import cost, not behaviour
    from .mesh import Mesh

#: How many patches the surface is cut into before the merge starts.  The cut
#: is fast and the clustering is not, so this is where the cost of a fit is
#: set.  It has to stay well clear of :data:`MAX_PLANE_AXES` -- a plane built
#: from one or two patches is a plane quantised to the over-segmentation
#: rather than to the form -- so there are several patches per plane even with
#: the slider all the way over.
LEAF_COUNT = 1536

#: The consensus fit holds every patch measured against every other in memory,
#: so it starts from a coarser cut than the merge does.
FLAT_LEAF_COUNT = 1024

#: The widest and narrowest a plane may be, in degrees of turn, for a patch to
#: still count as agreeing with it.  The wide end is loose enough that a whole
#: side of a form is one flat; the narrow end is tight enough to reach the full
#: sixty-four planes on anything with that much in it.
COARSEST_FLAT_DEG, FINEST_FLAT_DEG = 65.0, 7.0

#: How many tolerances between those the consensus fit tries.  Geometric, so
#: the counts they produce spread across the slider rather than bunching.
FLAT_STEPS = 18

#: How much say the least flat vertex on a model keeps.  Never zero: a model
#: with no flats anywhere at all must still break into planes somehow.
FLOOR_FLATNESS = 0.02

#: Passes of the re-weighted fit that settles a cluster's direction.
ROBUST_ROUNDS = 3


# -- the sample -------------------------------------------------------------


@dataclass(frozen=True)
class Surface:
    """The design matrix, and the frame it was measured in."""

    #: Unit normals.  ``(m, 3)``.
    normals: np.ndarray
    #: Positions, centred on the model and scaled to a unit radius.  ``(m, 3)``.
    points: np.ndarray
    #: Area, discounted by how rounded the neighbourhood is.  ``(m,)``.
    weights: np.ndarray
    #: World point :attr:`points` is measured from.
    origin: np.ndarray
    #: World units to normalised units.
    scale: float
    #: What each block of the matrix counts for.
    coefficients: Coefficients

    @property
    def offsets(self) -> np.ndarray:
        """Distance out to each vertex's own tangent plane.  ``(m,)``."""
        return np.einsum("ij,ij->i", self.points, self.normals)

    def design(self) -> np.ndarray:
        """The rows the clusterers actually see.  ``(m, 7)``."""
        return np.hstack(
            [
                self.normals,
                self.coefficients.locality * self.points,
                self.coefficients.coplanarity * self.offsets[:, None],
            ]
        )


def neighbour_agreement(mesh: Mesh) -> np.ndarray:
    """How nearly each vertex faces the way its neighbours do, as a cosine.

    One along a flat, falling off around a turn.  Taken over the edges of the
    triangles rather than over any wider neighbourhood, so it costs one pass
    and reads the same on a model however it was tessellated.
    """
    count = mesh.vertex_count
    if count == 0 or mesh.triangle_count == 0:
        return np.ones(count, dtype=np.float64)
    normals = np.asarray(mesh.normals, dtype=np.float64)
    lengths = np.linalg.norm(normals, axis=1)
    normals = normals / np.where(lengths > 1e-9, lengths, 1.0)[:, None]

    triangles = mesh.indices.astype(np.int64)
    here = triangles[:, [0, 1, 2]].ravel()
    there = triangles[:, [1, 2, 0]].ravel()
    agreement = np.einsum("ij,ij->i", normals[here], normals[there])
    # Each edge speaks for both of its ends.
    seen = np.bincount(here, minlength=count) + np.bincount(there, minlength=count)
    total = np.bincount(here, weights=agreement, minlength=count) + np.bincount(
        there, weights=agreement, minlength=count
    )
    return np.where(seen > 0, total / np.maximum(seen, 1), 1.0)


def flatness(mesh: Mesh, span_deg: float = DEFAULT_COEFFICIENTS.flat_span_deg) -> np.ndarray:
    """How much each vertex's opinion of its plane is worth, 0 to 1."""
    turn = 1.0 - neighbour_agreement(mesh)
    span = max(1.0 - math.cos(math.radians(max(span_deg, 1e-3))), 1e-9)
    return np.maximum(np.exp(-((np.maximum(turn, 0.0) / span) ** 2)), FLOOR_FLATNESS)


def sample_surface(
    mesh: Mesh,
    coefficients: Coefficients = DEFAULT_COEFFICIENTS,
    sample_limit: int = SAMPLE_LIMIT,
) -> Surface | None:
    """Thin the model down to a design matrix, or say it has nothing to give."""
    normals = np.asarray(mesh.normals, dtype=np.float64)
    if len(normals) == 0:
        return None
    lengths = np.linalg.norm(normals, axis=1)
    usable = lengths > 1e-9
    if not usable.any():
        return None

    weights = vertex_weights(mesh) * flatness(mesh, coefficients.flat_span_deg)
    radius = float(mesh.bounds.radius)
    origin = np.asarray(mesh.bounds.center, dtype=np.float64)
    points = (np.asarray(mesh.positions, dtype=np.float64) - origin) / radius

    normals = normals[usable] / lengths[usable, None]
    points, weights = points[usable], weights[usable]
    if len(normals) > sample_limit:
        # A fixed stride rather than a random draw, so the same model always
        # breaks into the same planes.
        stride = int(np.ceil(len(normals) / sample_limit))
        normals, points, weights = normals[::stride], points[::stride], weights[::stride]

    weights = np.where(weights > 0.0, weights, 1e-12)
    return Surface(
        normals=normals,
        points=points,
        weights=weights,
        origin=origin.astype(np.float32),
        scale=1.0 / radius,
        coefficients=coefficients,
    )


# -- over-segmentation ------------------------------------------------------


def _spread(design: np.ndarray, weights: np.ndarray, members: np.ndarray) -> float:
    """Weighted scatter of a group about its own centre."""
    block = design[members]
    mass = weights[members]
    total = float(mass.sum())
    if total <= 0.0:
        return 0.0
    centred = block - (mass @ block) / total
    return float(mass @ np.einsum("ij,ij->i", centred, centred))


def _cut(
    design: np.ndarray, weights: np.ndarray, members: np.ndarray
) -> tuple[np.ndarray, np.ndarray] | None:
    """Halve a group across its first principal component, or refuse to."""
    if len(members) < 2:
        return None
    block = design[members]
    mass = weights[members]
    total = float(mass.sum())
    if total <= 0.0:
        return None
    centred = block - (mass @ block) / total
    covariance = (centred * mass[:, None]).T @ centred
    # eigh orders ascending, so the last eigenvector is the principal one.
    axis = np.linalg.eigh(covariance)[1][:, -1]
    near = centred @ axis > 0.0
    if not near.any() or near.all():
        return None
    return members[near], members[~near]


def _leaves(design: np.ndarray, weights: np.ndarray, count: int) -> np.ndarray:
    """Cut the sample into ``count`` tight patches, the loosest cut first.

    A patch is small enough to be inside one plane of the form and large
    enough that the clustering afterwards is over hundreds of rows instead of
    tens of thousands.  Both fits start here.
    """
    groups: list[np.ndarray] = [np.arange(len(design))]
    # None marks a group that has already refused to split.
    spreads: list[float | None] = [_spread(design, weights, groups[0])]
    while len(groups) < max(int(count), 1):
        candidates = [(s, i) for i, s in enumerate(spreads) if s is not None and s > 0.0]
        if not candidates:
            break
        index = max(candidates)[1]
        halves = _cut(design, weights, groups[index])
        if halves is None:
            spreads[index] = None
            continue
        near, far = halves
        groups[index : index + 1] = [near, far]
        spreads[index : index + 1] = [
            _spread(design, weights, near),
            _spread(design, weights, far),
        ]

    labels = np.zeros(len(design), dtype=np.int64)
    for index, members in enumerate(groups):
        labels[members] = index
    return labels


@dataclass(frozen=True)
class Patches:
    """What the clusterers see: one row per patch of surface.

    ``moments`` is the *sum* of the weighted normals in a patch rather than
    their average, so its length says how much the patch agrees with itself.
    A patch straddling a hard edge has a short moment and is quietly given
    less of a say in the direction of whatever cluster it joins.
    """

    #: Total weight.  ``(p,)``.
    mass: np.ndarray
    #: Summed weighted normals.  ``(p, 3)``.
    moments: np.ndarray
    #: Mean position, normalised frame.  ``(p, 3)``.
    points: np.ndarray
    #: Mean tangent-plane offset.  ``(p,)``.
    offsets: np.ndarray
    #: What each block of the matrix counts for.
    coefficients: Coefficients

    def __len__(self) -> int:
        return len(self.mass)

    @property
    def directions(self) -> np.ndarray:
        """Unit direction of each patch.  ``(p, 3)``."""
        lengths = np.linalg.norm(self.moments, axis=1)
        return self.moments / np.where(lengths > 1e-12, lengths, 1.0)[:, None]

    @property
    def coherence(self) -> np.ndarray:
        """How much weight each patch brings to a direction.  ``(p,)``."""
        return np.maximum(np.linalg.norm(self.moments, axis=1), 1e-12)

    def design(self) -> np.ndarray:
        """The patch centres, in the same space the vertices were cut in."""
        mean_normal = self.moments / self.mass[:, None]
        return np.hstack(
            [
                mean_normal,
                self.coefficients.locality * self.points,
                self.coefficients.coplanarity * self.offsets[:, None],
            ]
        )


def _patches(surface: Surface, labels: np.ndarray) -> Patches:
    count = int(labels.max()) + 1
    weights = surface.weights
    mass = np.bincount(labels, weights=weights, minlength=count)
    mass = np.where(mass > 0.0, mass, 1e-12)
    moments = np.stack(
        [
            np.bincount(labels, weights=weights * surface.normals[:, axis], minlength=count)
            for axis in range(3)
        ],
        axis=1,
    )
    points = (
        np.stack(
            [
                np.bincount(labels, weights=weights * surface.points[:, axis], minlength=count)
                for axis in range(3)
            ],
            axis=1,
        )
        / mass[:, None]
    )
    offsets = np.bincount(labels, weights=weights * surface.offsets, minlength=count) / mass
    return Patches(
        mass=mass,
        moments=moments,
        points=points,
        offsets=offsets,
        coefficients=surface.coefficients,
    )


# -- turning a clustering into planes ---------------------------------------


def _compact(labels: np.ndarray) -> tuple[np.ndarray, int]:
    """Renumber arbitrary cluster ids to ``0 .. k-1``, keeping their order."""
    _, packed = np.unique(labels, return_inverse=True)
    return packed.astype(np.int64), int(packed.max()) + 1 if len(packed) else 0


def _fit(patches: Patches, labels: np.ndarray, count: int, surface: Surface) -> PlaneSet:
    """The plane of every cluster: an M-estimate of where its patches face.

    Starting from the plain weighted mean -- which is what the PCA fit would
    have given -- each round asks how far each patch has ended up from its
    cluster's direction, calls anything past twice the average disagreement an
    outlier, and re-takes the mean without it.  Three rounds is enough: the
    estimate is being nudged off a handful of strays, not searched for.
    """
    directions = patches.directions
    coherence = patches.coherence
    weight = coherence.copy()

    axes = np.zeros((count, 3), dtype=np.float64)
    for _ in range(ROBUST_ROUNDS):
        for axis in range(3):
            axes[:, axis] = np.bincount(
                labels, weights=weight * directions[:, axis], minlength=count
            )
        lengths = np.linalg.norm(axes, axis=1)
        # A cluster whose patches cancel exactly keeps the direction of its
        # heaviest patch rather than collapsing to nothing.
        blank = lengths <= 1e-12
        if blank.any():
            heaviest = np.full(count, -1)
            order = np.argsort(coherence)
            heaviest[labels[order]] = order
            axes[blank] = directions[heaviest[blank]]
            lengths = np.linalg.norm(axes, axis=1)
        axes /= np.where(lengths > 1e-12, lengths, 1.0)[:, None]

        miss = 1.0 - np.einsum("ij,ij->i", directions, axes[labels])
        scale = np.bincount(labels, weights=coherence * miss, minlength=count) / np.bincount(
            labels, weights=coherence, minlength=count
        )
        cutoff = np.maximum(2.0 * scale[labels], 1e-4)
        tukey = np.clip(1.0 - (miss / cutoff) ** 2, 0.0, 1.0) ** 2
        weight = np.maximum(coherence * tukey, coherence * 1e-3)

    # Anchor and offset follow the same weights, so the point the shader
    # measures a fragment against is the middle of what the direction was
    # actually fitted to.
    total = np.bincount(labels, weights=weight, minlength=count)
    total = np.where(total > 0.0, total, 1e-12)
    anchors = (
        np.stack(
            [
                np.bincount(labels, weights=weight * patches.points[:, axis], minlength=count)
                for axis in range(3)
            ],
            axis=1,
        )
        / total[:, None]
    )
    offsets = np.bincount(labels, weights=weight * patches.offsets, minlength=count) / total
    return PlaneSet(
        directions=axes.astype(np.float32),
        anchors=anchors.astype(np.float32),
        offsets=offsets.astype(np.float32),
        # Squared, because the fit measures a squared distance and the columns
        # carry the coefficients themselves: a step of position costs
        # ``(locality * step)^2``, which is what the shader has to charge too.
        locality=surface.coefficients.locality ** 2,
        coplanarity=surface.coefficients.coplanarity ** 2,
        origin=surface.origin.astype(np.float32),
        scale=surface.scale,
    )


# -- regions: agglomerative merging by Ward's criterion ---------------------


def _ward(features: np.ndarray, mass: np.ndarray, keep_upto: int) -> dict[int, np.ndarray]:
    """Merge patches two at a time, cheapest first, recording the way down.

    The cost of joining two clusters is the variance the join adds, which for
    weighted points is ``m_i m_j / (m_i + m_j)`` times the squared distance
    between their centres.  After a merge the row of costs for the survivor
    follows from the two old rows by Lance and Williams' recurrence, so the
    whole dendrogram costs one distance matrix and a pass per merge.
    """
    count = len(features)
    if count == 0:
        return {}
    square = np.einsum("ij,ij->i", features, features)
    gaps = square[:, None] + square[None, :] - 2.0 * (features @ features.T)
    np.maximum(gaps, 0.0, out=gaps)
    cost = (mass[:, None] * mass[None, :]) / (mass[:, None] + mass[None, :]) * gaps
    np.fill_diagonal(cost, np.inf)

    # Scanning the whole matrix for the cheapest pair at every merge is what
    # makes the naive form of this cubic, and with a patch for every plane and
    # then some that is felt.  Each row's own cheapest is kept instead, so the
    # search is down one row; a row only has to be looked at again when the
    # partner it was pointing at has just been merged away.
    nearest = np.argmin(cost, axis=1)
    closest = cost[np.arange(count), nearest]

    size = mass.astype(np.float64).copy()
    labels = np.arange(count)
    alive = np.ones(count, dtype=bool)
    levels: dict[int, np.ndarray] = {}
    remaining = count
    while True:
        if remaining <= keep_upto:
            levels[remaining] = labels.copy()
        if remaining <= 1:
            break
        here = int(np.argmin(closest))
        if not np.isfinite(closest[here]):
            break
        there = int(nearest[here])
        if here > there:
            here, there = there, here
        joined = cost[here, there]
        merged = (
            (size[here] + size) * cost[here] + (size[there] + size) * cost[there] - size * joined
        ) / (size[here] + size[there] + size)
        merged[here] = merged[there] = np.inf
        merged[~alive] = np.inf
        cost[here, :] = merged
        cost[:, here] = merged
        cost[there, :] = np.inf
        cost[:, there] = np.inf
        size[here] += size[there]
        labels[labels == there] = here
        alive[there] = False
        remaining -= 1

        # The survivor's row is new, and so is every row that had been pointing
        # at either half of the merge.  Every other row still holds.
        closest[there] = np.inf
        nearest[there] = there
        stale = np.flatnonzero(alive & ((nearest == here) | (nearest == there)))
        for row in (here, *stale.tolist()):
            nearest[row] = int(np.argmin(cost[row]))
            closest[row] = cost[row, nearest[row]]
    return levels


def plane_regions(
    mesh: Mesh,
    coefficients: Coefficients = DEFAULT_COEFFICIENTS,
    max_count: int = MAX_PLANE_AXES,
    sample_limit: int = SAMPLE_LIMIT,
    leaf_count: int = LEAF_COUNT,
) -> PlaneAxes:
    """Break the surface into patches and merge them back into planes."""
    surface = sample_surface(mesh, coefficients, sample_limit)
    if surface is None:
        return PlaneAxes([])
    patches = _patches(surface, _leaves(surface.design(), surface.weights, leaf_count))
    wanted = max(int(max_count), 1)
    levels = _ward(patches.design(), patches.mass, wanted)

    fitted: list[PlaneSet] = []
    for count in range(1, wanted + 1):
        if count not in levels:
            break
        labels, actual = _compact(levels[count])
        fitted.append(_fit(patches, labels, actual, surface))
    return PlaneAxes(fitted)


# -- flats: the plane the most surface agrees on, over and over -------------


def _consensus(
    gaps: np.ndarray, mass: np.ndarray, tolerance: float, max_count: int
) -> tuple[np.ndarray, np.ndarray]:
    """Take the plane the most surface agrees on, remove it, and ask again.

    ``gaps`` is every patch measured against every other in the space the fit
    was made in, so a row of it is one patch's proposal for a plane and the
    entries under ``tolerance`` are the patches that would go along with it.
    The proposal carrying the most surface wins, which is the estimate a
    handful of stray patches cannot reach: they are never the winner, and they
    are never inside the winner either.

    Comes back as a label per patch and the patches that were the winners, in
    the order they won, so that stopping the list short is the same thing as
    having asked for fewer planes in the first place.
    """
    within = gaps <= tolerance
    alive = np.ones(len(mass), dtype=bool)
    labels = np.full(len(mass), -1, dtype=np.int64)
    seeds: list[int] = []
    # Taking a plane only ever removes surface, so rather than re-asking every
    # proposal how much it now carries, the surface just taken is subtracted
    # from all of them.  Over a whole run that is one pass of the matrix
    # instead of one pass per plane, which is what keeps the cost flat as the
    # slider's reach grows.
    support = within @ mass
    while alive.any() and len(seeds) < max_count:
        support[~alive] = -1.0
        seed = int(np.argmax(support))
        members = within[seed] & alive
        members[seed] = True  # A plane always holds the patch that proposed it.
        labels[members] = len(seeds)
        seeds.append(seed)
        alive &= ~members
        taken = np.flatnonzero(members)
        support -= within[:, taken] @ mass[taken]
    return labels, np.array(seeds, dtype=np.int64)


def _first_planes(
    gaps: np.ndarray, labels: np.ndarray, seeds: np.ndarray, count: int
) -> np.ndarray:
    """The clustering that keeping only the first ``count`` winners leaves.

    Extraction is greedy, so the strongest ``count`` planes of a long run are
    exactly the planes a run asked to stop at ``count`` would have found; all
    that is left to do is hand the surface they did not take to whichever of
    them it agrees with most.  That is what lets one pass down the tolerance
    answer for every setting of the slider at that tolerance.
    """
    kept = labels[:, None] == np.arange(count)[None, :]
    taken = kept.any(axis=1)
    packed = np.where(taken, labels, 0)
    spare = np.flatnonzero(~taken)
    if len(spare):
        packed[spare] = np.argmin(gaps[np.ix_(seeds[:count], spare)], axis=0)
    return packed


def plane_flats(
    mesh: Mesh,
    coefficients: Coefficients = DEFAULT_COEFFICIENTS,
    max_count: int = MAX_PLANE_AXES,
    sample_limit: int = SAMPLE_LIMIT,
    leaf_count: int = FLAT_LEAF_COUNT,
) -> PlaneAxes:
    """Pull the flats of the form out largest first, at every tolerance."""
    surface = sample_surface(mesh, coefficients, sample_limit)
    if surface is None:
        return PlaneAxes([])
    patches = _patches(surface, _leaves(surface.design(), surface.weights, leaf_count))
    features = patches.design()
    square = np.einsum("ij,ij->i", features, features)
    gaps = square[:, None] + square[None, :] - 2.0 * (features @ features.T)
    np.maximum(gaps, 0.0, out=gaps)
    wanted = max(int(max_count), 1)

    # Loosest first.  A loose tolerance reads the form in big flats and finds
    # few of them; each step tightens it until the slider's full travel is
    # covered, and every count is served by the loosest reading that can still
    # supply it, so the planes stay as broad as the count allows.
    runs: list[tuple[np.ndarray, np.ndarray]] = []
    for span in np.geomspace(COARSEST_FLAT_DEG, FINEST_FLAT_DEG, FLAT_STEPS):
        # A tolerance is quoted as a turn, and this is what that turn costs in
        # the space the patches live in.
        tolerance = 2.0 * (1.0 - math.cos(math.radians(float(span))))
        labels, seeds = _consensus(gaps, patches.mass, tolerance, wanted)
        if not len(seeds):
            continue
        if not runs or len(seeds) > len(runs[-1][1]):
            runs.append((labels, seeds))
        if len(seeds) >= wanted:
            break
    if not runs:
        return PlaneAxes([])

    fitted: list[PlaneSet] = []
    for count in range(1, min(wanted, len(runs[-1][1])) + 1):
        labels, seeds = next(run for run in runs if len(run[1]) >= count)
        fitted.append(_fit(patches, _first_planes(gaps, labels, seeds, count), count, surface))
    return PlaneAxes(fitted)


# -- what the renderer asks for ---------------------------------------------

#: The clustered fits read the design matrix; PCA reads the normals and has no
#: use for its coefficients, so it is handed them and ignores them.
_FITTERS: dict[PlaneMode, typing.Callable[[Mesh, Coefficients], PlaneAxes]] = {
    PlaneMode.PCA: lambda mesh, _coefficients: plane_axes(mesh),
    PlaneMode.REGIONS: plane_regions,
    PlaneMode.FLATS: plane_flats,
}


def fit_planes(
    mesh: Mesh | None, mode: PlaneMode, coefficients: Coefficients = DEFAULT_COEFFICIENTS
) -> PlaneAxes:
    """The planes of ``mesh`` under ``mode``; empty where the mode needs none."""
    fitter = _FITTERS.get(mode)
    if mesh is None or fitter is None:
        return PlaneAxes([])
    return fitter(mesh, coefficients)
