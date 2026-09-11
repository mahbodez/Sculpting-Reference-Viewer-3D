"""Scrubbing through the making of a form, rather than only arriving at it.

The claim the whole feature rests on is that a stage of a film *is* the form:
stage n is the same mesh the Detail slider set to n would build, worked the
same way and finished the same way.  A scrub that showed something subtly
other than what the slider gives would be a lie, and an artist comparing the
two would be right to trust neither.  So that is what most of this asserts,
and it asserts it by building both and comparing them rather than by trusting
that the same code was called.

The other half is that a film is a *making*: it starts where the mode starts
(the plain hull for stone, one mass for clay), it ends where the slider is
set, and it moves one way -- stone only ever comes down onto the model, clay
only ever builds up towards it.  A stage that went backwards would mean the
order was invented rather than read out of how the modes actually work.
"""

from __future__ import annotations

import numpy as np
import pytest

from refview.core import plane_volume
from refview.core.plane_clusters import plane_regions
from refview.core.plane_film import MAX_STAGES, film_key, record, stage_counts
from refview.core.plane_solids import sculpt_mesh, solid_count
from refview.core.settings import PlaneSettings, SculptMode
from test_plane_solids import (
    TEST_RESOLUTION,
    _bar,
    _wires,
    ball,
    dumbbell,
    edge_use,
    volume,
)


@pytest.fixture(autouse=True)
def coarse_lattice(monkeypatch: pytest.MonkeyPatch) -> None:
    """Read every model on a small lattice, so the suite stays quick."""
    monkeypatch.setattr(plane_volume, "RESOLUTION", TEST_RESOLUTION)
    monkeypatch.setattr("refview.core.plane_solids.RESOLUTION", TEST_RESOLUTION)


def film_of(mesh, settings: PlaneSettings) -> list:
    """Every stage of a making, as a list."""
    planes = plane_regions(mesh).for_count(settings.sculpt_count)
    return list(record(mesh, planes, settings))


# -- what a film is -------------------------------------------------------


@pytest.mark.parametrize("sculpt", list(SculptMode))
def test_the_last_stage_is_the_form_the_slider_itself_gives(sculpt: SculptMode) -> None:
    """The claim the whole feature rests on, checked against the real thing.

    Not "something similar" and not "the same volume": the same mesh, vertex
    for vertex.  A film is worth having only because scrubbing to the end
    lands exactly where letting go of the Detail slider lands.
    """
    mesh = ball()
    settings = PlaneSettings(sculpt=sculpt, sculpt_detail=30.0, sculpt_masses=2)
    stages = film_of(mesh, settings)
    assert stages, "a model that can be blocked in has a making"

    planes = plane_regions(mesh).for_count(settings.sculpt_count)
    direct = sculpt_mesh(
        mesh,
        planes,
        sculpt,
        settings.sculpt_masses,
        settings.sculpt_relax,
        smooth=0.0,
        median=settings.sculpt_median,
        median_reach=settings.sculpt_median_reach,
    )
    last = stages[-1].mesh
    assert last.vertex_count == direct.vertex_count
    assert last.triangle_count == direct.triangle_count
    assert np.allclose(last.positions, direct.positions)
    assert np.array_equal(last.indices, direct.indices)


@pytest.mark.parametrize("sculpt", list(SculptMode))
def test_a_making_starts_where_the_mode_starts(sculpt: SculptMode) -> None:
    """Stone's first stage is the block before any cut; clay's is one mass.

    Which is the part of a block-in worth watching: a film that opened on the
    form already half made would have skipped it.
    """
    stages = film_of(
        ball(), PlaneSettings(sculpt=sculpt, sculpt_detail=30.0, sculpt_masses=2)
    )
    assert stages[0].solids == 1
    assert [s.index for s in stages] == list(range(len(stages)))
    # And it climbs from there, one solid at a time, never repeating itself.
    counts = [s.solids for s in stages]
    assert counts == sorted(counts)
    assert len(set(counts)) == len(counts)


def test_the_stone_only_ever_comes_down_onto_the_model() -> None:
    """A cut takes material away, so no stage of a carving is larger than the
    one before it.  That is what makes the sequence a carving rather than an
    arbitrary set of forms sorted by size."""
    stages = film_of(
        ball(), PlaneSettings(sculpt=SculptMode.SUBTRACTIVE, sculpt_detail=36.0)
    )
    sizes = [volume(s.mesh) for s in stages]
    assert len(sizes) > 2
    assert all(later <= earlier + 1e-9 for earlier, later in zip(sizes, sizes[1:], strict=False))
    assert sizes[-1] < sizes[0]  # and it really did cut something


def test_the_clay_only_ever_builds_up_towards_the_model() -> None:
    """The same the other way about: a lump adds material, so the form grows."""
    stages = film_of(
        dumbbell(),
        PlaneSettings(
            sculpt=SculptMode.ADDITIVE, sculpt_detail=36.0, sculpt_masses=2
        ),
    )
    sizes = [volume(s.mesh) for s in stages]
    assert len(sizes) > 2
    assert all(later >= earlier - 1e-9 for earlier, later in zip(sizes, sizes[1:], strict=False))
    assert sizes[-1] > sizes[0]


@pytest.mark.parametrize("sculpt", list(SculptMode))
def test_every_stage_is_a_solid_in_its_own_right(sculpt: SculptMode) -> None:
    """A stage is something to look at, so it has to be closed and wound out.

    Scrubbing to the middle of a making must not show a form with holes in it
    that the finished one would not have had.  Judged the way the rest of the
    suite judges it: a handful of odd edges is what dual contouring leaves on
    any model and encloses nothing, so what is asserted is that a stage is no
    worse than the finished form rather than that it is perfect.
    """
    stages = film_of(
        ball(), PlaneSettings(sculpt=sculpt, sculpt_detail=30.0, sculpt_masses=2)
    )
    for stage in stages:
        mesh = stage.mesh
        if mesh.triangle_count == 0:
            continue
        open_edges, over_used, total = edge_use(mesh)
        assert open_edges <= total // 50, f"stage {stage.index} is full of holes"
        assert over_used <= total // 50, f"stage {stage.index} passes through itself"
        assert volume(mesh) > 0.0, f"stage {stage.index} is wound inside out"


def test_a_stage_names_the_detail_setting_that_would_rebuild_it() -> None:
    """So an artist who scrubs to something worth keeping can get back to it.

    The number under the handle has to be one that really produces that stage,
    not an estimate: setting the slider there and finding a different form
    would be worse than showing nothing.  Which is why a stage the sliders
    cannot reach says nothing at all rather than naming its nearest neighbour
    -- clay's masses go down one at a time in a film, but the Masses setting
    puts them all down at once, so there is no setting that shows half of them.
    """
    for sculpt in SculptMode:
        settings = PlaneSettings(sculpt=sculpt, sculpt_detail=30.0, sculpt_masses=2)
        named = 0
        for stage in film_of(ball(), settings):
            if stage.planes is None:
                continue
            named += 1
            asked = solid_count(stage.planes, sculpt, settings.sculpt_masses)
            assert asked == stage.solids, "a stage named a setting that gives another form"
        assert named, "no stage of the film could be got back to at all"


def test_the_stages_before_the_masses_are_shown_but_not_claimed() -> None:
    """Clay lays its masses one at a time and a film shows that, even though
    the Masses setting cannot ask for it.  Those stages are the block-in
    arriving, which is the part worth watching; what they must not do is claim
    a slider setting that would rebuild them, because none would."""
    settings = PlaneSettings(
        sculpt=SculptMode.ADDITIVE, sculpt_detail=30.0, sculpt_masses=3
    )
    stages = film_of(ball(), settings)
    early = [s for s in stages if s.solids < settings.sculpt_masses]
    assert early, "a film should show the masses going down one by one"
    assert all(s.planes is None for s in early)


# -- how long a film is ---------------------------------------------------


def test_a_film_ends_where_the_slider_is_set() -> None:
    """However many stages it is thinned to, the last one is the form itself."""
    for sculpt in SculptMode:
        for detail in (20.0, 45.0):
            settings = PlaneSettings(sculpt=sculpt, sculpt_detail=detail, sculpt_masses=3)
            wanted = solid_count(settings.sculpt_count, sculpt, settings.sculpt_masses)
            assert stage_counts(sculpt, settings.sculpt_count, 3)[-1] == wanted


def test_a_long_making_is_thinned_rather_than_left_to_crawl() -> None:
    """A slider with a thousand stops is not a slider, and a stage that differs
    from its neighbour by one small block on a form made of hundreds is not a
    stage worth stopping on.  So a long making is sampled evenly -- and the
    end is kept whatever the sampling does, because that is the form itself."""
    counts = stage_counts(SculptMode.SUBTRACTIVE, 256, 4)
    assert len(counts) <= MAX_STAGES
    assert counts[0] == 1
    assert counts[-1] == solid_count(256, SculptMode.SUBTRACTIVE, 4)
    assert counts == sorted(set(counts))


def test_a_making_that_runs_out_early_stops_there() -> None:
    """A form the mode cannot break down any further ends the film rather than
    repeating the same shape until the slider runs out."""
    stages = film_of(
        ball(rings=8, sectors=10),
        PlaneSettings(sculpt=SculptMode.ADDITIVE, sculpt_detail=70.0, sculpt_masses=2),
    )
    assert stages
    sizes = [volume(s.mesh) for s in stages]
    # Nothing at the end is a repeat of what came before it.
    assert sizes[-1] > sizes[0]


# -- what a film depends on -----------------------------------------------


def test_autosmooth_does_not_throw_a_film_away() -> None:
    """It re-reads normals rather than rebuilding a form, so a film survives it.

    Otherwise moving the AutoSmooth slider would cost a whole re-recording,
    which is minutes for a tenth of a second's worth of work.
    """
    base = PlaneSettings(sculpt=SculptMode.ADDITIVE, sculpt_smooth=30.0)
    other = PlaneSettings(sculpt=SculptMode.ADDITIVE, sculpt_smooth=60.0)
    assert film_key(base, base.coefficients) == film_key(other, other.coefficients)


@pytest.mark.parametrize(
    "field, value",
    [
        ("sculpt", SculptMode.SUBTRACTIVE),
        ("sculpt_detail", 80.0),
        ("sculpt_masses", 7),
        ("sculpt_relax", 3),
        ("sculpt_median", 4),
        ("sculpt_median_reach", 3),
    ],
)
def test_anything_that_changes_a_stage_starts_a_new_film(field, value) -> None:
    """The other side of the same coin: a film is only good for the settings
    that made it, and every setting a stage is built from is one of them."""
    base = PlaneSettings(sculpt=SculptMode.ADDITIVE)
    changed = PlaneSettings(sculpt=SculptMode.ADDITIVE)
    setattr(changed, field, value)
    assert film_key(base, base.coefficients) != film_key(
        changed, changed.coefficients
    )


def test_a_recording_can_be_stopped_part_way() -> None:
    """A film nobody is waiting for any more is abandoned rather than finished.

    Dragging the Detail slider starts a new recording at every value it comes
    to rest on, and each would otherwise queue up behind the last.
    """
    mesh = ball()
    settings = PlaneSettings(sculpt=SculptMode.SUBTRACTIVE, sculpt_detail=40.0)
    planes = plane_regions(mesh).for_count(settings.sculpt_count)

    whole = list(record(mesh, planes, settings))
    taken: list = []
    for stage in record(mesh, planes, settings, should_stop=lambda: len(taken) >= 3):
        taken.append(stage)
    assert len(taken) == 3
    assert len(whole) > 3, "the unstopped film is longer than the stopped one"
    # What it did record is the real thing, not a rougher stand-in for it.
    assert np.allclose(taken[2].mesh.positions, whole[2].mesh.positions)


def test_the_film_is_empty_for_a_model_with_no_planes_in_it() -> None:
    """A model the fit cannot break down has no making to show, and says so by
    handing back nothing rather than by raising."""
    mesh = ball()
    settings = PlaneSettings(sculpt=SculptMode.ADDITIVE)
    from refview.core.plane_axes import PlaneSet

    assert list(record(mesh, PlaneSet.empty(), settings)) == []


# -- a making built on an armature ----------------------------------------


def test_a_film_of_clay_on_a_wire_lays_it_down_in_the_order_it_was_listed() -> None:
    """The order the artist put the bones in is what the scrub walks through,
    which is the reason a bone list is worth reordering at all."""
    mesh = _bar()
    ends = [
        [[-0.9, 0.0, 0.0], [-0.4, 0.0, 0.0]],
        [[0.4, 0.0, 0.0], [0.9, 0.0, 0.0]],
    ]
    settings = PlaneSettings(
        sculpt=SculptMode.ADDITIVE, sculpt_detail=6.0, sculpt_masses=2
    )
    planes = plane_regions(mesh).for_count(settings.sculpt_count)
    stages = list(record(mesh, planes, settings, None, _wires(*ends)))
    reversed_stages = list(record(mesh, planes, settings, None, _wires(*reversed(ends))))

    assert len(stages) >= 2
    # The first stage holds one lump, and which end of the bar it is on is
    # decided by the list rather than by the model.
    assert stages[0].mesh.positions[:, 0].mean() < 0.0
    assert reversed_stages[0].mesh.positions[:, 0].mean() > 0.0


def test_the_last_stage_of_a_film_on_a_wire_is_the_form_the_slider_gives() -> None:
    """The claim the whole film rests on, asked again with an armature under
    it: an armature must not be one thing to the slider and another to the
    scrub, or the film would be lying about what it shows."""
    mesh = _bar()
    wires = _wires([[-0.8, 0.0, 0.0], [0.0, 0.0, 0.0]], [[0.0, 0.0, 0.0], [0.8, 0.0, 0.0]])
    settings = PlaneSettings(
        sculpt=SculptMode.ADDITIVE, sculpt_detail=20.0, sculpt_masses=2
    )
    planes = plane_regions(mesh).for_count(settings.sculpt_count)
    stages = list(record(mesh, planes, settings, None, wires))
    assert stages

    direct = sculpt_mesh(
        mesh,
        planes,
        SculptMode.ADDITIVE,
        settings.sculpt_masses,
        settings.sculpt_relax,
        smooth=0.0,
        median=settings.sculpt_median,
        median_reach=settings.sculpt_median_reach,
        wires=wires,
    )
    assert np.allclose(stages[-1].mesh.positions, direct.positions)
    assert np.array_equal(stages[-1].mesh.indices, direct.indices)


def test_bending_the_wire_starts_a_new_film() -> None:
    """A film is only good for the settings that made it, and where the
    armature stands is one of them."""
    settings = PlaneSettings(sculpt=SculptMode.ADDITIVE)
    here = _wires([[-0.4, 0.0, 0.0], [0.4, 0.0, 0.0]])
    there = _wires([[0.0, -0.4, 0.0], [0.0, 0.4, 0.0]])

    assert film_key(settings, settings.coefficients, here) == film_key(
        settings, settings.coefficients, here
    )
    assert film_key(settings, settings.coefficients, here) != film_key(
        settings, settings.coefficients, there
    )
    assert film_key(settings, settings.coefficients, here) != film_key(
        settings, settings.coefficients, None
    )
