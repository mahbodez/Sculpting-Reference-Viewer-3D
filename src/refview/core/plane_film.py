"""The stages a form passes through on its way from a block to a figure.

The geometry modes hand back a finished thing: the form at the detail the
slider was left on.  What they do not show is the part a sculptor actually
learns from -- the order the form arrives in.  Which mass was laid first, what
the second cut took off, where the figure stopped being a block and started
being a body.  That order is not a reconstruction after the fact.  It is
already there in how both modes work, and this reads it out.

Stone splits greedily: one block to start with, then over and over the block
holding the most air is cut in two.  So the form in ``k`` blocks is the form in
``k + 1`` blocks with the last cut not yet made, and the whole carving is one
walk with a photograph taken after every cut.

Clay lays lumps one at a time, each into whatever the ones before it left
bare.  So the first ``k`` lumps are exactly the form at ``k`` lumps -- with one
wrinkle, which is that the joins between lumps are worked out afresh for each
stage rather than shared, because which pairs are near enough to bridge
changes as lumps are added.  That is the cheap half, so it costs little.

What makes this affordable at all is that the expensive half of a carving --
reading the model into a lattice and finding its distance field, about a second
on a figure -- depends on neither the count nor the mode.  It is laid once, as
a :class:`~refview.core.plane_volume.Bed`, and every stage is then a matter of
laying its own solids on that bed and reading the surface back: a fifth of a
second apiece rather than a second and a half.

The stages come back as finished meshes, worked exactly the way the form
itself is worked, because they *are* the form: stage ``n`` of a film is the
same mesh the detail slider at ``n`` would give you.  That is deliberate.  A
scrub that showed something subtly other than what the slider gives would be
a lie, and an artist comparing the two would be right not to trust either.
"""

from __future__ import annotations

import typing
from dataclasses import dataclass, field

import numpy as np

from . import plane_volume as pv
from .mesh import Mesh, auto_smooth
from .plane_axes import PlaneSet
from .plane_solids import (
    seed_spacing,
    solid_count,
    surface_seeds,
    unit_normals,
)
from .settings import PlaneSettings, SculptMode

if typing.TYPE_CHECKING:  # pragma: no cover - import cost, not behaviour
    from collections.abc import Callable, Iterator


#: Most stages a film is ever cut into.  A film is scrubbed rather than read,
#: so what matters is that the handle moves smoothly and that consecutive
#: stages differ by something the eye can see.  Past a hundred-odd the
#: difference between one stage and the next is a single small block on a form
#: already made of dozens, which is neither.
MAX_STAGES = 96


@dataclass(frozen=True)
class Stage:
    """One moment in the making of a form.

    :attr:`solids` is how many blocks or lumps the form is made of here, and
    :attr:`planes` the detail setting that asks for it -- so an artist who
    stops the scrub somewhere worth keeping can be told what to set the slider
    to in order to get back to it.
    """

    #: Where this stage sits in the film, from zero.
    index: int
    #: How many blocks of stone or lumps of clay the form is made of.
    solids: int
    #: The detail setting that would rebuild this stage, where there is one.
    #: ``None`` for a stage the sliders cannot reach -- clay's masses arrive
    #: together, so a film shows them going down one at a time but the Masses
    #: setting has no way to ask for half of them.
    planes: int | None
    #: The form itself, finished exactly as the mode would finish it.
    mesh: Mesh

    @property
    def label(self) -> str:
        """What to call this stage in the panel, under the scrub handle."""
        thing = "solid" if self.solids == 1 else "solids"
        return f"{self.solids} {thing}"


@dataclass
class Film:
    """A whole making, from the coarsest stage to the one the slider asks for.

    Held by the viewport between one turn of the sliders and the next, and
    indexed rather than searched: the scrub handle moves every frame and must
    not do work.
    """

    #: Which way the form was worked.
    sculpt: SculptMode
    #: The settings the film was recorded under.  A film is only good for the
    #: settings that made it, and this is what that is checked against.
    key: tuple
    #: The stages, coarsest first.
    stages: list[Stage] = field(default_factory=list)
    #: Whether every stage has been recorded yet.  A film is scrubbable while
    #: it is still being made, so this says whether what is there is all there
    #: will be.
    complete: bool = False

    def __len__(self) -> int:
        return len(self.stages)

    def at(self, index: int) -> Stage | None:
        """The stage at ``index``, clamped to what has actually been recorded."""
        if not self.stages:
            return None
        return self.stages[min(max(int(index), 0), len(self.stages) - 1)]


def film_key(
    settings: PlaneSettings, coefficients: object, wires: pv.Wires | None = None
) -> tuple:
    """What a film depends on.

    Everything that changes the shape of any stage, and nothing that does not.
    AutoSmooth is left out on purpose: it re-reads normals rather than
    rebuilding a form, so it is applied to a stage as it is handed out and a
    film survives it being changed.  The armature is in by its positions
    rather than by which one it is: bending the wire rebuilds the form, so it
    has to rebuild the film of the form as well.
    """
    return (
        settings.sculpt,
        settings.sculpt_count,
        settings.sculpt_masses,
        settings.sculpt_relax,
        settings.sculpt_median,
        settings.sculpt_median_reach,
        settings.sculpt_fineness,
        None if wires is None else wires.signature,
        coefficients,
    )


def stage_counts(sculpt: SculptMode, planes: int, masses: int) -> list[int]:
    """How many solids each stage of a film is made of.

    Every count from the coarsest the mode admits up to the one the slider is
    set to.  Stone starts at one -- the plain hull, the block before any cut --
    and clay at one mass, because a block-in that showed every mass at once
    would skip the part where the figure is two shapes and then three.

    Where that would be more stages than :data:`MAX_STAGES`, they are thinned
    evenly, and the last is always kept: the stage the slider is actually set
    to has to be in the film, or scrubbing to the end would land somewhere
    other than where letting go of the slider does.
    """
    last = solid_count(planes, sculpt, masses)
    first = 1
    counts = list(range(first, last + 1))
    if len(counts) <= MAX_STAGES:
        return counts
    picked = np.unique(
        np.rint(np.linspace(first, last, MAX_STAGES)).astype(int)
    ).tolist()
    if picked[-1] != last:  # pragma: no cover - linspace already ends there
        picked[-1] = last
    return picked


def planes_for(sculpt: SculptMode, solids: int, masses: int, planes: int) -> int | None:
    """The detail setting that asks for ``solids``, or ``None`` if none does.

    The inverse of :func:`~refview.core.plane_solids.solid_count`, so a stage
    can say what to set the slider to in order to come back to it.  It is a
    search rather than arithmetic because the forward direction rounds.

    Not every stage has an answer, and the ones that do not are the
    interesting ones: clay's first few lumps are the masses, and the Masses
    setting puts them all down at once, so a figure read as four masses has no
    slider setting that shows only two of them.  Those stages are worth
    watching -- they are the block-in arriving -- but claiming a setting that
    would not reproduce them would be a lie, so this says nothing instead.
    """
    for count in range(1, max(int(planes), 1) + 1):
        if solid_count(count, sculpt, masses) == int(solids):
            return count
    return None


def record(
    mesh: Mesh,
    planes: PlaneSet,
    settings: PlaneSettings,
    should_stop: Callable[[], bool] | None = None,
    wires: pv.Wires | None = None,
) -> Iterator[Stage]:
    """Work the form stage by stage, handing each one back as it is finished.

    A generator rather than a list, because the recording is slow enough to be
    worth watching happen: the caller can show each stage as it lands, and can
    stop part way by way of ``should_stop`` when the artist has moved on to
    something else.  A film that stops early is still a film -- it just ends
    sooner than the slider does.

    With an armature, what the scrub walks through is the artist's own order:
    stage one is the first bone they put at the top of the list, and the film
    is the block-in arriving the way they said to build it.
    """
    if mesh.vertex_count == 0 or len(planes) == 0:
        return
    triangles = np.asarray(mesh.indices, dtype=np.int64).reshape(-1, 3)
    if len(triangles) == 0:
        return
    points = np.asarray(mesh.positions, dtype=np.float64)
    sculpt = settings.sculpt
    additive = sculpt is SculptMode.ADDITIVE
    masses = int(settings.sculpt_masses)
    count = settings.sculpt_count

    resolution = max(
        int(round(pv.RESOLUTION * max(float(settings.sculpt_fineness), 1.0))),
        pv.RESOLUTION,
    )
    seeds, leaning = surface_seeds(
        points, triangles, unit_normals(mesh), seed_spacing(mesh, resolution)
    )
    bed = pv.lay_bed(points, triangles, seeds, leaning, resolution)
    if should_stop is not None and should_stop():
        return

    directions = np.asarray(planes.directions, dtype=np.float64).reshape(-1, 3)
    wanted = stage_counts(sculpt, count, masses)
    if not wanted:  # pragma: no cover - a slider that asks for nothing
        return

    name = f"{mesh.name} (planes)"
    finish = dict(
        relax=int(settings.sculpt_relax),
        median=int(settings.sculpt_median),
        median_reach=int(settings.sculpt_median_reach),
        name=name,
        source_offset=mesh.source_offset,
        units=mesh.units,
    )

    if additive:
        bevels = pv.fitted_facings(directions)
        # Every lump the finest stage will need, laid once.  A stage is then a
        # prefix of them, which is exactly what it would have laid for itself.
        lumps, held, place, wall = pv.clay_lumps(
            bed.model, bed.origin, bed.step, bevels, masses, wanted[-1], wires
        )
        if not lumps:  # pragma: no cover - a model the lattice never found
            return
        for index, solids in enumerate(wanted):
            if should_stop is not None and should_stop():
                return
            take = min(int(solids), len(lumps))
            if take <= 0:  # pragma: no cover - guarded by stage_counts
                continue
            mine = lumps[:take]
            pieces = mine + pv.join_pieces(
                mine, held[:take], place, wall, bevels, min(take, pv.MAX_JOINS)
            )
            field, facing = pv.union_field(
                bed.origin, bed.step, bed.shape, pieces, bed.outside
            )
            yield Stage(
                index=index,
                solids=take,
                planes=planes_for(sculpt, take, masses, count),
                mesh=pv.surface_of(bed, field, facing, True, **finish),
            )
            if take >= len(lumps):
                # The clay ran out before the slider did: every stage after
                # this one would be the same form again.
                return
    else:
        facing_set = pv.facings(directions)
        # The whole greedy split, made once; a stage replays a prefix of it.
        at, who, records, stride, coarse = pv.block_splits(
            bed.within, bed.origin, bed.step, wanted[-1]
        )
        if len(at) == 0:  # pragma: no cover - a model the lattice never found
            return
        # Replayed from the start rather than from wherever the last stage
        # left off, because the stages may be thinned and a prefix is cheap:
        # it is an assignment into an array of a few hundred thousand int32.
        for index, solids in enumerate(wanted):
            if should_stop is not None and should_stop():
                return
            splits = min(int(solids) - 1, len(records))
            if splits < 0:  # pragma: no cover - guarded by stage_counts
                continue
            here = np.zeros(len(at), dtype=np.int32)
            for _cut, made, moved in records[:splits]:
                here[moved] = made
            label = pv.block_labels(at, here, coarse)
            field, facing = pv.stone_field(
                bed, facing_set, label, stride, splits + 1
            )
            yield Stage(
                index=index,
                solids=splits + 1,
                planes=planes_for(sculpt, splits + 1, masses, count),
                mesh=pv.surface_of(bed, field, facing, False, **finish),
            )
            if splits >= len(records):
                # The stone stopped splitting before the slider ran out.
                return


def shaded(stage: Stage, smooth: float) -> Mesh:
    """A stage as it is to be drawn, with its normals read at ``smooth``.

    Kept out of the recording so that changing AutoSmooth costs a tenth of a
    second over the film rather than making the whole of it again.
    """
    return auto_smooth(stage.mesh, float(smooth))
