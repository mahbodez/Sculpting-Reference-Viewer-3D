"""Blocking a form in out of its planes, as stone is cut and as clay is built.

What matters is not that a particular solve ran.  It is that what comes back
is a *solid*: closed, wound one way out, and made of flats.  That stone always
holds the whole model inside it and clay always sits within it, at every
setting of the slider.  That the sliders behave like sliders -- more cuts
bring the stone down onto the model, more clay builds the form up towards it,
with no step of either quietly doing nothing.  That the model handed in is
never touched, because everything else in the viewer measures and picks
against it.  And that the fit only runs when the fit has gone stale.

The invariant worth naming is the one the whole additive mode rests on: a lump
of clay is grown until it touches the model from the inside and never past it,
so the clay is contained in the model by construction rather than by luck.
:func:`test_a_lump_never_grows_out_through_the_model` is what says so, on the
lump itself rather than on the finished mesh, because the finished mesh is
held under the model anyway and would hide the fault.

The stand-in has its own vertices and its own triangles -- it is found by
working the volume the model encloses, not by moving the model's points -- so
nothing here asserts that its topology matches the model's.  What it asserts
is that the topology it does have is sound.
"""

from __future__ import annotations

import numpy as np
import pytest

from refview.core import plane_volume
from refview.core.armature import Armature, ArmatureNode, Bone
from refview.core.mesh import Mesh, auto_smooth, compute_vertex_normals
from refview.core.plane_axes import PlaneSet
from refview.core.plane_clusters import plane_regions
from refview.core.plane_solids import (
    MAX_BLOCKS,
    MAX_TUBES,
    SculptCache,
    block_count,
    piece_count,
    sculpt_mesh,
    seed_spacing,
    solid_count,
    surface_seeds,
    unit_normals,
    wires_for,
)
from refview.core.settings import (
    DETAIL_CEILING,
    SMOOTH_MAX,
    SMOOTH_MIN,
    PlaneSettings,
    PlaneTarget,
    SculptMode,
)

COUNTS = (6, 14, 40)

#: A lattice fine enough to show what the method does and coarse enough that a
#: whole test run is seconds rather than minutes.
TEST_RESOLUTION = 56


@pytest.fixture(autouse=True)
def coarse_lattice(monkeypatch: pytest.MonkeyPatch) -> None:
    """Read every model on a small lattice, so the suite stays quick."""
    monkeypatch.setattr(plane_volume, "RESOLUTION", TEST_RESOLUTION)
    monkeypatch.setattr("refview.core.plane_solids.RESOLUTION", TEST_RESOLUTION)


# -- shapes ---------------------------------------------------------------
#
# Closed ones, because reading a model into a lattice starts by asking which
# side of it a place is on, and that question only has an answer for a surface
# with no holes in it.


def ball(rings: int = 24, sectors: int = 40, radius: float = 1.0, at=(0.0, 0.0, 0.0)) -> Mesh:
    """A closed sphere: wrapped at the seam, capped at both poles."""
    points = [np.array([0.0, radius, 0.0])]
    for ring in range(1, rings):
        down = np.pi * ring / rings
        for sector in range(sectors):
            around = 2.0 * np.pi * sector / sectors
            points.append(
                radius
                * np.array(
                    [
                        np.sin(down) * np.cos(around),
                        np.cos(down),
                        np.sin(down) * np.sin(around),
                    ]
                )
            )
    points.append(np.array([0.0, -radius, 0.0]))
    bottom = len(points) - 1

    def index(ring: int, sector: int) -> int:
        return 1 + (ring - 1) * sectors + sector % sectors

    triangles = []
    for sector in range(sectors):
        triangles.append([0, index(1, sector + 1), index(1, sector)])
        triangles.append([bottom, index(rings - 1, sector), index(rings - 1, sector + 1)])
    for ring in range(1, rings - 1):
        for sector in range(sectors):
            a, b = index(ring, sector), index(ring, sector + 1)
            c, d = index(ring + 1, sector), index(ring + 1, sector + 1)
            triangles += [[a, b, d], [a, d, c]]
    packed = np.array(points) + np.asarray(at, dtype=np.float64)
    faces = np.array(triangles, dtype=np.uint32)
    return Mesh(packed, compute_vertex_normals(packed, faces), faces, "ball")


def block(steps: int = 6, size: float = 1.0) -> Mesh:
    """A closed box with hard edges, each face cut into a grid of triangles."""
    points: list = []
    triangles: list = []
    grid = np.linspace(-size, size, steps + 1)
    for axis in range(3):
        for sign in (1.0, -1.0):
            out = np.zeros(3)
            out[axis] = sign
            across = np.zeros(3)
            across[(axis + 1) % 3] = 1.0
            up = np.zeros(3)
            up[(axis + 2) % 3] = sign
            base = len(points)
            for u in grid:
                for v in grid:
                    points.append(out * size + u * across + v * up)
            for i in range(steps):
                for j in range(steps):
                    corner = base + i * (steps + 1) + j
                    triangles += [
                        [corner + steps + 1, corner + 1, corner],
                        [corner + steps + 1, corner + steps + 2, corner + 1],
                    ]
    packed = np.array(points)
    faces = np.array(triangles, dtype=np.uint32)
    return Mesh(packed, compute_vertex_normals(packed, faces), faces, "block")


def dumbbell() -> Mesh:
    """Two balls of different size, far enough apart to be two masses."""
    big, small = ball(radius=1.0, at=(-1.1, 0.0, 0.0)), ball(radius=0.55, at=(1.3, 0.0, 0.0))
    points = np.concatenate([big.positions, small.positions])
    faces = np.concatenate(
        [big.indices, small.indices + big.vertex_count]
    ).astype(np.uint32)
    return Mesh(points, compute_vertex_normals(points, faces), faces, "dumbbell")


# -- measuring ------------------------------------------------------------


def welded(mesh: Mesh) -> np.ndarray:
    """Which point each vertex really is, once copies of a position are one point."""
    return np.unique(mesh.positions, axis=0, return_inverse=True)[1].astype(np.int64).ravel()


def volume(mesh: Mesh) -> float:
    """Enclosed volume, by the divergence theorem over the triangles."""
    corners = [mesh.positions[mesh.indices[:, i]].astype(np.float64) for i in range(3)]
    return float(
        np.einsum("ij,ij->i", corners[0], np.cross(corners[1], corners[2])).sum() / 6.0
    )


def edge_use(mesh: Mesh) -> tuple[int, int, int]:
    """Edges used once, edges used more than twice, and edges in all.

    Once would mean a hole, except that a triangle with no area has no normal
    to shade it by and is dropped, which leaves its edges behind: a handful of
    those is expected and encloses nothing.  More than twice means a cell where
    the surface passed through itself, which dual contouring makes a few of on
    any model and which draws perfectly well.  Both are only worth watching to
    see that they stay a handful.
    """
    points = welded(mesh)
    triangles = points[mesh.indices.astype(np.int64)]
    here = triangles[:, [0, 1, 2]].ravel()
    there = triangles[:, [1, 2, 0]].ravel()
    keys = np.minimum(here, there).astype(np.int64) * (points.max() + 1) + np.maximum(
        here, there
    )
    used = np.unique(keys, return_counts=True)[1]
    return int((used == 1).sum()), int((used > 2).sum()), len(used)


def roughness(mesh: Mesh) -> float:
    """How far each point sits from the middle of its neighbours, as a share of
    the form's size.  Exactly what a pass of the relax takes out, which is why
    it is the thing to watch it by.
    """
    place, points = np.unique(mesh.positions, axis=0, return_inverse=True)
    triangles = points.astype(np.int64).ravel()[mesh.indices.astype(np.int64)]
    ends = np.concatenate([triangles[:, [0, 1, 2]].ravel(), triangles[:, [1, 2, 0]].ravel()])
    others = np.concatenate([triangles[:, [1, 2, 0]].ravel(), triangles[:, [0, 1, 2]].ravel()])
    heard = np.bincount(ends, minlength=len(place))
    middle = np.stack(
        [np.bincount(ends, weights=place[others, a], minlength=len(place)) for a in range(3)],
        axis=1,
    )
    live = heard > 0
    drift = middle[live] / heard[live][:, None] - place[live]
    return float(np.linalg.norm(drift, axis=1).mean() / mesh.bounds.radius)


def flatness(mesh: Mesh) -> float:
    """The share of the surface lying in the twenty commonest directions.

    A form made of planes has most of its area facing a handful of ways.  A
    form that is still the model has its area spread over every direction
    there is, and so does one that has been chewed.
    """
    corners = [mesh.positions[mesh.indices[:, i]].astype(np.float64) for i in range(3)]
    facing = np.cross(corners[1] - corners[0], corners[2] - corners[0])
    area = np.linalg.norm(facing, axis=1)
    usable = area > 1e-12
    facing, area = facing[usable] / area[usable, None], area[usable]
    binned = np.rint(facing * 8.0).astype(np.int64)
    keys = (binned[:, 0] * 64 + binned[:, 1]) * 64 + binned[:, 2]
    weights = np.bincount(np.unique(keys, return_inverse=True)[1].ravel(), weights=area)
    return float(np.sort(weights)[-20:].sum() / weights.sum())


@pytest.fixture(scope="module")
def rounded() -> tuple[Mesh, object]:
    mesh = ball()
    return mesh, plane_regions(mesh)


# -- what comes back ------------------------------------------------------


@pytest.mark.parametrize("count", COUNTS)
@pytest.mark.parametrize("sculpt", list(SculptMode))
def test_the_stand_in_is_a_solid(rounded, count, sculpt) -> None:
    mesh, axes = rounded
    out = sculpt_mesh(mesh, axes.for_count(count), sculpt, 4)
    assert out.vertex_count > 0
    holes, crossings, edges = edge_use(out)
    assert holes <= 0.002 * edges
    assert crossings <= 0.002 * edges
    assert volume(out) > 0.0  # wound outwards


@pytest.mark.parametrize("count", COUNTS)
@pytest.mark.parametrize("sculpt", list(SculptMode))
def test_the_stand_in_is_made_of_flats(rounded, count, sculpt) -> None:
    """Twice the model's own concentration, and not more, because the model
    here is a ball.  A ball has no flats to find, so the fine end of the slider
    -- which is a couple of hundred facings now -- comes back as a ball made of
    a couple of hundred flats, and no measure of flatness can tell that from a
    ball.  On a form that has flats in it the margin is far wider; this is the
    hardest case there is, and it is meant to be."""
    mesh, axes = rounded
    out = sculpt_mesh(mesh, axes.for_count(count), sculpt, 4)
    assert flatness(out) > 2.0 * flatness(mesh)


@pytest.mark.parametrize("count", COUNTS)
def test_stone_holds_the_model_and_clay_sits_within_it(rounded, count) -> None:
    mesh, axes = rounded
    model = volume(mesh)
    assert volume(sculpt_mesh(mesh, axes.for_count(count), SculptMode.ADDITIVE, 4)) < model
    assert volume(sculpt_mesh(mesh, axes.for_count(count), SculptMode.SUBTRACTIVE, 4)) > model


def test_the_coarsest_stone_is_the_block_the_model_came_out_of() -> None:
    """One block is the block of stone: a single hull round the whole model,
    bridging whatever gaps are in it.  On two masses with air between them
    that is half again as much stone as there is model, and the air between
    them is filled -- which is exactly what a carver starts the day with."""
    mesh = dumbbell()
    stone = sculpt_mesh(mesh, plane_regions(mesh).for_count(2), SculptMode.SUBTRACTIVE, 4)
    assert volume(stone) > 1.5 * volume(mesh)
    # The block reaches at least as far as the model does, on every axis.
    assert (stone.positions.max(axis=0) >= mesh.positions.max(axis=0) - 1e-6).all()
    assert (stone.positions.min(axis=0) <= mesh.positions.min(axis=0) + 1e-6).all()


@pytest.mark.parametrize("sculpt", list(SculptMode))
def test_the_form_stays_the_size_it_was(rounded, sculpt) -> None:
    mesh, axes = rounded
    for count in COUNTS:
        out = sculpt_mesh(mesh, axes.for_count(count), sculpt, 4)
        assert 0.3 < out.bounds.radius / mesh.bounds.radius < 2.5


def test_more_cuts_bring_the_stone_down_onto_the_model() -> None:
    """Every step of the slider is another cut, and a cut can only take stone
    off.  Not asserted step by step -- a cut through one block can leave the
    total a hair up -- but firmly across the range."""
    mesh = dumbbell()
    axes = plane_regions(mesh)
    coarse = volume(sculpt_mesh(mesh, axes.for_count(2), SculptMode.SUBTRACTIVE, 4))
    fine = volume(sculpt_mesh(mesh, axes.for_count(40), SculptMode.SUBTRACTIVE, 4))
    assert fine < 0.8 * coarse
    assert fine > volume(mesh)


def test_more_clay_builds_the_form_up_towards_the_model() -> None:
    """Every step of the slider lays another lump in, and a lump can only add
    material.  Across the range that has to show, and no step of it may quietly
    do nothing -- which is the failure the old mode had, where the top half of
    its slider was a row of settings all showing the same shape."""
    mesh = dumbbell()
    axes = plane_regions(mesh)
    sizes = [
        volume(sculpt_mesh(mesh, axes.for_count(count), SculptMode.ADDITIVE, 2))
        for count in (2, 6, 14, 40)
    ]
    assert all(later > earlier for earlier, later in zip(sizes, sizes[1:], strict=False))
    assert sizes[-1] < volume(mesh)


def test_the_first_masses_are_blocks_pressed_into_the_biggest_forms() -> None:
    """One mass on two balls of different size lands in the larger, because
    that is where the most material is; two puts a block in each.  This is the
    ordering the whole mode rests on -- the biggest forms first -- and it is
    read here off where the clay actually ends up."""
    mesh = dumbbell()
    planes = plane_regions(mesh).for_count(2)
    alone = sculpt_mesh(mesh, planes, SculptMode.ADDITIVE, 1)
    assert not (alone.positions[:, 0] > 0.4).any()  # nothing in the small ball
    assert (alone.positions[:, 0] < 0.0).any()  # and a block in the large one

    both = sculpt_mesh(mesh, planes, SculptMode.ADDITIVE, 2)
    assert (both.positions[:, 0] > 0.4).any()  # now the small one has its own
    assert volume(both) > volume(alone)


def test_more_masses_block_in_more_of_the_form() -> None:
    """The masses slider is a reading of the form rather than a resolution, so
    what it has to do is simply be a slider: every step of it is another block
    pressed in, and another block is more of the model covered."""
    mesh = dumbbell()
    planes = plane_regions(mesh).for_count(2)
    sizes = [
        volume(sculpt_mesh(mesh, planes, SculptMode.ADDITIVE, masses))
        for masses in (1, 2, 4, 8)
    ]
    assert all(later > earlier for earlier, later in zip(sizes, sizes[1:], strict=False))
    assert sizes[-1] < volume(mesh)


def test_relaxing_settles_the_clay_and_leaves_the_stone_alone() -> None:
    """The relax is a pass over the finished surface rather than anything the
    volume knows about, so what it has to do is settle that surface -- and it
    has to leave stone, which is meant to keep the corners it was cut with,
    exactly as it was."""
    mesh = ball()
    planes = plane_regions(mesh).for_count(14)
    settled = [
        roughness(sculpt_mesh(mesh, planes, SculptMode.ADDITIVE, 4, rounds))
        for rounds in (0, 4, 12)
    ]
    assert all(later < earlier for earlier, later in zip(settled, settled[1:], strict=False))

    cut = sculpt_mesh(mesh, planes, SculptMode.SUBTRACTIVE, 4, 0)
    again = sculpt_mesh(mesh, planes, SculptMode.SUBTRACTIVE, 4, 20)
    assert np.array_equal(cut.positions, again.positions)


def test_relaxing_cannot_push_the_clay_out_through_the_model() -> None:
    """Everything upstream of the relax is careful to keep the clay inside the
    model, and the relax moves the surface after all of it has finished -- so
    the care has to be repeated here or it is undone.  Read on a ball, where
    what is inside the model is a fact rather than a measurement."""
    mesh = ball()
    planes = plane_regions(mesh).for_count(14)
    cell = 2.2 / TEST_RESOLUTION
    for rounds in (0, 8, 20):
        out = sculpt_mesh(mesh, planes, SculptMode.ADDITIVE, 4, rounds)
        assert volume(out) < volume(mesh)
        assert np.linalg.norm(out.positions, axis=1).max() < 1.0 + cell


def test_a_form_already_made_of_flats_is_left_about_where_it_was() -> None:
    mesh = block()
    axes = plane_regions(mesh)
    for sculpt in SculptMode:
        out = sculpt_mesh(mesh, axes.for_count(14), sculpt, 4)
        assert 0.45 * volume(mesh) < volume(out) < 2.2 * volume(mesh)


@pytest.mark.parametrize("sculpt", list(SculptMode))
def test_the_model_is_never_touched(rounded, sculpt) -> None:
    mesh, axes = rounded
    before = (mesh.positions.copy(), mesh.normals.copy(), mesh.indices.copy())
    out = sculpt_mesh(mesh, axes.for_count(14), sculpt, 4)
    assert out is not mesh
    assert np.array_equal(mesh.positions, before[0])
    assert np.array_equal(mesh.normals, before[1])
    assert np.array_equal(mesh.indices, before[2])


def test_a_model_with_no_planes_in_it_comes_back_as_it_went_in() -> None:
    mesh = ball()
    assert sculpt_mesh(mesh, PlaneSet.empty(), SculptMode.ADDITIVE, 4) is mesh


# -- reading the model in -------------------------------------------------


def test_the_lattice_reads_the_model_it_was_given() -> None:
    mesh = ball()
    origin, step, shape = plane_volume.lattice(
        mesh.positions.min(axis=0), mesh.positions.max(axis=0), 0.1
    )
    within = plane_volume.solid(mesh.positions, mesh.indices, origin, step, shape)
    assert float(within.sum()) * step**3 == pytest.approx(volume(mesh), rel=0.05)
    grid = plane_volume._axes(origin, step, shape)
    inside = sum(grid[a] ** 2 for a in range(3)) < 0.8**2
    assert within[inside].all()


def test_an_open_model_is_read_some_other_way() -> None:
    """Counting crossings is exact on a closed surface and meaningless on
    anything else, so the two have to be told apart before it is believed."""
    mesh = block()
    origin, step, shape = plane_volume.lattice(
        mesh.positions.min(axis=0), mesh.positions.max(axis=0), 0.1
    )
    whole = plane_volume.solid(mesh.positions, mesh.indices, origin, step, shape)
    assert plane_volume.encloses(whole, mesh.positions, mesh.indices, step)

    # The same box with its lid taken off, which is the shape of half the
    # scans an artist has: a surface with no inside.
    middles = mesh.positions[mesh.indices.astype(np.int64)].mean(axis=1)
    open_faces = mesh.indices[middles[:, 2] < 1.0 - 1e-9]
    holed = plane_volume.solid(mesh.positions, open_faces, origin, step, shape)
    assert not plane_volume.encloses(holed, mesh.positions, open_faces, step)


def test_the_samples_cover_a_surface_however_it_was_tessellated() -> None:
    """A box is six triangles the size of the whole thing; the lattice has to
    feel it as densely as it feels a scan."""
    mesh = block(steps=1)
    points = np.asarray(mesh.positions, dtype=np.float64)
    triangles = np.asarray(mesh.indices, dtype=np.int64).reshape(-1, 3)
    normals = np.asarray(mesh.normals, dtype=np.float64)
    seeds, leaning = surface_seeds(points, triangles, normals, 0.1)
    assert len(seeds) == len(leaning) > 20 * mesh.vertex_count
    assert np.allclose(np.linalg.norm(leaning, axis=1), 1.0)
    # Every seed lies on the surface of the box.
    assert np.isclose(np.abs(seeds).max(axis=1), 1.0).all()


# -- the blocks -----------------------------------------------------------


def test_a_cut_is_taken_where_the_block_holds_the_most_air() -> None:
    """Two masses with a gap between them: the first cut has to go through the
    gap, because that is where the block round both of them is holding air."""
    mesh = dumbbell()
    origin, step, shape = plane_volume.lattice(
        mesh.positions.min(axis=0), mesh.positions.max(axis=0), 0.1
    )
    within = plane_volume.solid(mesh.positions, mesh.indices, origin, step, shape)
    label, stride, count = plane_volume.blocks(within, origin, step, 2)
    assert count == 2

    coarse = np.ascontiguousarray(within[::stride, ::stride, ::stride])
    at = np.stack(np.nonzero(coarse), axis=1)
    across = origin[0] + at[:, 0] * step * stride
    who = label[coarse]
    # Each block is on one side of the gap, whichever way round they came out.
    for side in (0, 1):
        assert np.ptp(np.sign(across[who == side])) == 0.0


def test_a_block_holds_every_point_it_was_measured_from() -> None:
    """A hull cut from the surface itself, rather than from the corners the
    lattice found, is what lets stone be outside the model everywhere."""
    points = np.array([[0.0, 0.0, 0.0], [1.0, 0.2, -0.3], [-0.4, 0.9, 0.6], [0.3, -0.7, 0.8]])
    who = np.zeros(len(points), dtype=np.int64)
    facings = plane_volume.facings(np.zeros((0, 3)))
    offsets = plane_volume.point_support(points, who, facings, 1)
    assert (points @ facings.T <= offsets[0][None, :] + 1e-5).all()


def test_a_hull_is_cut_from_every_side() -> None:
    """Six directions make a box however well they were chosen, and a box is
    no use as clay -- it contains the model instead of fitting inside it."""
    bare = plane_volume.facings(np.zeros((0, 3)))
    assert len(bare) >= 26
    assert np.allclose(np.linalg.norm(bare, axis=1), 1.0)

    # Near-duplicates of what is already there buy nothing and cost a pass.
    doubled = plane_volume.facings(np.repeat(bare, 3, axis=0))
    assert len(doubled) == len(bare)

    many = plane_volume.facings(np.random.default_rng(0).normal(size=(400, 3)))
    assert len(many) <= plane_volume.MAX_FACINGS


def test_a_lump_never_grows_out_through_the_model() -> None:
    """The one thing the additive mode rests on, asked of the lump rather than
    of the finished mesh: the mesh is held under the model afterwards, so a
    lump that had burst out of the form would be quietly trimmed back and the
    fault would never show."""
    mesh = ball()
    origin, step, shape = plane_volume.lattice(
        mesh.positions.min(axis=0), mesh.positions.max(axis=0), 0.1
    )
    within = plane_volume.solid(mesh.positions, mesh.indices, origin, step, shape)
    grid = plane_volume._axes(origin, step, shape)
    place = np.stack([np.asarray(g) for g in grid], axis=-1)

    wall = plane_volume.outside_points(within, origin, step)
    facings = plane_volume.facings(np.zeros((0, 3)))
    seed = np.array([0.2, -0.1, 0.05])
    caps = np.full(len(facings), 10.0)
    offsets = plane_volume.grow_piece(seed, facings, wall, caps)
    assert offsets is not None
    assert (facings @ seed <= offsets + 1e-9).all()  # it holds its own seed

    held = (place @ facings.T <= offsets).all(axis=-1)
    assert held.any()
    # A lump may bulge through by up to one corner of the lattice it was grown
    # on, because between two corners the lattice has nothing to say -- which
    # is what the safety margin is for, and after it the model itself, which
    # the finished field is held under.  Any further than that and the wall is
    # not doing its job.
    near = within.copy()
    for axis in range(3):
        for forward in (True, False):
            here, there = plane_volume._shifts(axis, forward, 1)
            near[here] |= within[there]
    assert not held[~near].any()


def test_a_lump_is_held_to_the_material_it_was_pressed_into() -> None:
    """Left to itself a facing that no single point of the wall is holding back
    runs away until some other facing catches it, which is a good solid but not
    a reading of the mass it started in.  The caps are what stop that, and this
    is what says they are honoured."""
    mesh = ball()
    origin, step, shape = plane_volume.lattice(
        mesh.positions.min(axis=0), mesh.positions.max(axis=0), 0.1
    )
    within = plane_volume.solid(mesh.positions, mesh.indices, origin, step, shape)
    wall = plane_volume.outside_points(within, origin, step)
    facings = plane_volume.facings(np.zeros((0, 3)))
    seed = np.zeros(3)
    loose = plane_volume.grow_piece(seed, facings, wall, np.full(len(facings), 10.0))
    cap = float(0.5 * (loose.min() + loose.max()))
    tight = plane_volume.grow_piece(seed, facings, wall, np.full(len(facings), cap))
    assert (tight <= cap + 1e-9).all()  # not one facing past its own cap
    assert (tight <= loose + 1e-9).all()
    assert (tight < loose - 1e-6).any()  # and the cap really did bite
    # A cap under the lump's own inscribed core is no cap at all: a lump is at
    # least the largest copy of its own shape that fits round the seed.
    shrunk = plane_volume.grow_piece(seed, facings, wall, np.zeros(len(facings)))
    assert (shrunk > 0.0).all()


def test_the_fill_leaves_a_flat_alone_and_closes_a_slot() -> None:
    """The two halves of what the seam-filler is for, and the first is why it
    is safe to run over a form whose whole point is its flats.

    The filler works the solid rather than the field, and only ever adds: a
    cell of a slot that has material on enough sides is taken up into it.  A
    flat is all material on one side and all air on the other as far as the
    fill can reach, so it comes back untouched, exactly, however many passes
    are run.  A slot one cell wide -- which is what two solids crossing at an
    angle leave, and what dual contouring turns into a spike -- has material
    either side and is filled.
    """
    step = 1.0
    grid = np.stack(
        np.meshgrid(*[np.arange(16, dtype=np.float32)] * 3, indexing="ij"), axis=-1
    )
    lean = np.array([0.6, 0.8, 0.0], dtype=np.float32)
    plane = (grid @ lean - 9.0).astype(np.float32)
    inner = (slice(2, -2),) * 3  # away from the edge, where the lattice stops

    settled = plane_volume.close_gaps(plane, step, 3)
    assert np.array_equal(settled[inner], plane[inner])

    slotted = plane.copy()
    slotted[:, :, 8] = 1.0  # a slot cut clean through the material
    cut = (plane < -1.0) & (slotted > 0.0)
    assert cut.any()
    closed = plane_volume.close_gaps(slotted, step, 1, 1)
    assert (closed[cut] < 0.0).all()  # the slot is material again
    # And only there: a cell more than one cell from the slot never had one in
    # its neighbourhood, so it is left with the flat it was part of.
    away = np.ones_like(plane, dtype=bool)
    away[:, :, 6:11] = False
    assert np.array_equal(closed[inner][away[inner]], plane[inner][away[inner]])


def test_the_fill_never_takes_clay_away() -> None:
    """A thumb adds clay to a seam; it must not shave the block beside it.

    A corner of a block has air on more sides than material, and the median
    this replaced shaved it for exactly that reason.  The fill works the
    solid, and only ever adds to it: whatever was in the clay before is in it
    after, however many passes are run and however far they reach.
    """
    grid = np.stack(
        np.meshgrid(*[np.arange(-8, 9, dtype=np.float32)] * 3, indexing="ij"), axis=-1
    )
    block_field = (np.abs(grid) - np.array([4.5, 4.5, 1.5])).max(axis=-1)
    slotted = block_field.copy()
    slotted[8, :, :] = np.maximum(slotted[8, :, :], 0.5)  # a seam cut into a face
    before = slotted.copy()
    for rounds, reach in ((1, 1), (3, 2), (6, 3)):
        closed = plane_volume.close_gaps(slotted, 1.0, rounds, reach)
        assert np.all(closed <= before)  # every point of the solid survives
        assert np.array_equal(slotted, before)  # no writes into the caller's field
    assert (plane_volume.close_gaps(slotted, 1.0, 3, 2) < before - 0.1).any()  # the seam is filled


def test_how_far_the_fill_reaches_says_how_wide_a_slot_it_closes() -> None:
    """What the size of the filter buys, and why it is worth asking for.

    The fill grows the solid ``reach`` cells into a slot and lets the surface
    back the same distance, so a slot is closed if the grow can reach across
    it.  One cell of reach takes a slot one cell wide; a slot two wide is past
    it, and asks for a pass that reaches two.
    """
    step = 1.0
    grid = np.stack(
        np.meshgrid(*[np.arange(16, dtype=np.float32)] * 3, indexing="ij"), axis=-1
    )
    lean = np.array([0.6, 0.8, 0.0], dtype=np.float32)
    plane = (grid @ lean - 9.0).astype(np.float32)

    # The fill grows the solid ``reach`` cells and lets the surface back the
    # same distance, so a slot is closed when the grow can reach across it:
    # one cell of reach closes a slot two cells wide, and a wider one asks for
    # a pass that reaches further.  A flat, though, is a flat however far the
    # pass reaches -- a cell in from the surface by more than the reach is
    # never looked at, so what a flat is cut with is what it keeps, to the
    # last digit.
    wide = plane.copy()
    wide[:, :, 7:9] = 1.0  # a slot two cells across
    cut = (plane < -1.0) & (wide > 0.0)
    assert cut.any()
    assert (plane_volume.close_gaps(wide, step, 1, 1)[cut] < 0.0).all()  # closed
    # A flat, though, never loses clay however far the pass reaches: the fill
    # only ever adds.  (Its outer edge can gain a cell as the grow-and-let-
    # back rounds the corner the slot left, which is the fill doing its work
    # and not the median's shave.)
    for reach in (1, 2, 3):
        settled = plane_volume.close_gaps(plane, step, 2, reach)
        assert np.all(settled <= plane)


def test_the_fill_can_be_asked_for_more_of_itself_or_none() -> None:
    """Both ends of the filter are the artist's to set.  More passes, or a
    wider reach, close more of the slots -- and that is all they can do,
    because the fill only ever adds clay and never takes it away, so the form
    only ever grows.  Zero leaves the block-in exactly as it was laid.

    Stone hears neither: it leaves no slots between its cuts, and the corners
    it was cut with are the point of it."""
    mesh = ball()
    planes = plane_regions(mesh).for_count(14)
    sizes = [
        volume(sculpt_mesh(mesh, planes, SculptMode.ADDITIVE, 4, 0, 0.0, rounds, reach))
        for rounds, reach in ((0, 1), (1, 1), (3, 1), (3, 2))
    ]
    assert all(later >= earlier for earlier, later in zip(sizes, sizes[1:], strict=False))
    assert sizes[-1] < volume(mesh)  # asked for the most, still inside the model

    cut = sculpt_mesh(mesh, planes, SculptMode.SUBTRACTIVE, 4, 0, 0.0, 0, 1)
    again = sculpt_mesh(mesh, planes, SculptMode.SUBTRACTIVE, 4, 0, 0.0, 6, 3)
    assert np.array_equal(cut.positions, again.positions)


def test_a_solid_handed_in_too_big_is_pulled_back_inside_the_model() -> None:
    """A join starts life as the hull of two lumps, which is a shape that pokes
    out of the model wherever the form between them is not convex.  What makes
    it clay pushed into a seam rather than a cast taken off the surface is that
    it is then pulled back until it fits, and this is that claim on its own."""
    mesh = ball()  # a unit ball, so that "inside" is a fact and not a sample
    origin, step, shape = plane_volume.lattice(
        mesh.positions.min(axis=0), mesh.positions.max(axis=0), 0.1
    )
    within = plane_volume.solid(mesh.positions, mesh.indices, origin, step, shape)
    grid = plane_volume._axes(origin, step, shape)
    place = np.stack([np.asarray(g) for g in grid], axis=-1)
    wall = plane_volume.outside_points(within, origin, step)

    facings = plane_volume.facings(np.zeros((0, 3)))
    swollen = np.full(len(facings), 2.0)  # a solid twice the ball across
    offsets, room = plane_volume.fit_piece(facings, swollen, wall, swollen)
    assert room < 0.0  # it had to come in, and by a real distance
    assert (offsets <= swollen + 1e-9).all()  # never past the shape it was given

    held = (place @ facings.T <= offsets).all(axis=-1)
    assert held.any()
    # Within a cell of the surface, and no further.  The wall is a sampling of
    # the model on a lattice, so a corner of the solid can slip between two of
    # its points; anything past that and the wall is not doing its job.  See
    # test_a_lump_never_grows_out_through_the_model, which is the same limit.
    assert np.linalg.norm(place[held], axis=1).max() <= 1.0 + 1.5 * step


def test_a_join_fills_the_seam_the_lumps_leave_between_them(monkeypatch) -> None:
    """Two lumps pressed into a form cross in a notch, and a form full of
    notches reads as a heap of stones.  A dumbbell is the plainest case there
    is: a lump in each ball and a bar between them that neither reaches."""
    mesh = dumbbell()
    planes = plane_regions(mesh).for_count(6)
    joined = sculpt_mesh(mesh, planes, SculptMode.ADDITIVE, 2)
    monkeypatch.setattr(plane_volume, "MAX_JOINS", 0)
    bare = sculpt_mesh(mesh, planes, SculptMode.ADDITIVE, 2)
    assert volume(joined) > volume(bare) * 1.1
    assert volume(joined) < volume(mesh)


def test_the_joins_never_turn_the_clay_into_a_cast_of_the_model() -> None:
    """Filling the seams is the point; filling the model is not.

    A ball is where the difference is sharpest, because a ball is convex: the
    hull of any two lumps inside it is inside it as well, so a join allowed to
    span two whole lumps would come back as the ball itself and the mode would
    have quietly become a way of copying the model.  Held to a collar round the
    seam it cannot -- so the clay stays well inside the form, and stays made of
    flats rather than wearing the model's own rounded surface.
    """
    mesh = ball()
    axes = plane_regions(mesh)
    for count in (14, 40):
        out = sculpt_mesh(mesh, axes.for_count(count), SculptMode.ADDITIVE, 4)
        assert volume(out) < 0.9 * volume(mesh)
        assert flatness(out) > 2.0 * flatness(mesh)


def test_a_lump_lies_in_the_box_it_says_it_does() -> None:
    """Every lump is written into the lattice over its own bounding box only,
    so a box that did not hold the lump would quietly clip it."""
    rng = np.random.default_rng(3)
    frame = np.linalg.qr(rng.normal(size=(3, 3)))[0]
    directions = plane_volume._tube_facings(frame, np.zeros((0, 3)))
    offsets = np.abs(rng.normal(size=len(directions))) + 0.4
    low, high = plane_volume.piece_bounds(frame, offsets)
    points = rng.uniform(low - 0.5, high + 0.5, size=(20000, 3))
    inside = (points @ directions.T <= offsets).all(axis=1)
    assert inside.any()
    assert (points[inside] >= low - 1e-9).all()
    assert (points[inside] <= high + 1e-9).all()


def test_the_lumps_are_joined_as_a_volume_and_not_as_surfaces() -> None:
    """Two overlapping blocks come back as one solid, which is what a union is
    and what stops a tube laid across a mass leaving a seam.  Exactly the
    union, too: nothing of either block is lost and nothing at all is added.
    That second half is the one worth testing, because the softened union this
    replaced could reach past both blocks, and everything it reached past the
    model with came back wearing the model's own surface."""
    origin, step, shape = plane_volume.lattice(
        np.array([-1.0, -1.0, -1.0]), np.array([1.0, 1.0, 1.0]), 0.05
    )
    frame = np.eye(3)
    facing = plane_volume._box_facings(frame)
    left = np.array([0.1, 0.5, 0.4, 0.4, 0.4, 0.4])
    right = np.array([0.5, 0.1, 0.4, 0.4, 0.4, 0.4])
    scale = 0.1
    field, faces = plane_volume.union_field(
        origin,
        step,
        shape,
        [(facing, left, frame, scale), (facing, right, frame, scale)],
        9.0,
    )
    grid = plane_volume._axes(origin, step, shape)
    place = np.stack([np.asarray(g) for g in grid], axis=-1)
    held = place @ facing.T
    inside = (held <= left).all(axis=-1) | (held <= right).all(axis=-1)
    solid = field <= 0.0
    assert (solid | ~inside).all()  # nothing the union held was lost
    assert (inside | ~solid).all()  # and nothing outside it was added
    assert solid.sum() > (held <= left).all(axis=-1).sum()  # one solid, not two
    # Every corner the solid holds was given the facing of some real plane.
    assert np.isclose(np.linalg.norm(faces[solid], axis=-1), 1.0).all()


def test_a_chip_that_never_touches_the_form_is_dropped() -> None:
    corner = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    faces = np.array([[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]], dtype=np.int64)
    vertex = np.concatenate([corner, corner + np.array([9.0, 0.0, 0.0])])
    both = np.concatenate([faces, faces + 4])
    against = np.array([True] * 4 + [False] * 4)
    kept = plane_volume.whole_pieces(vertex, both, 0.0, against)
    assert len(kept) == 4
    assert kept.max() < 4


def test_stone_starts_at_one_block_and_clay_at_the_masses_asked_for() -> None:
    assert solid_count(2, SculptMode.SUBTRACTIVE, 4) == 1
    assert solid_count(2, SculptMode.ADDITIVE, 4) == 4
    assert solid_count(1000, SculptMode.SUBTRACTIVE, 4) == MAX_BLOCKS
    assert solid_count(1000, SculptMode.ADDITIVE, 4) == 4 + MAX_TUBES
    for made in (block_count, lambda k: piece_count(k, 4)):
        counts = [made(k) for k in (2, 8, 20, 60, 200)]
        assert all(
            later >= earlier for earlier, later in zip(counts, counts[1:], strict=False)
        )


def test_asking_for_more_masses_never_costs_the_clay_its_detail() -> None:
    """The masses are a reading of the form and the tubes are how far the
    modelling is taken, so they are two questions rather than one budget.  A
    shared budget would mean that reading a figure as more masses quietly took
    the detail away again, which is not what either slider says it does."""
    for planes in (2, 20, 200, 1000):
        tubes = [piece_count(planes, masses) - masses for masses in (1, 4, 12, 32)]
        assert len(set(tubes)) == 1
    assert piece_count(1000, 32) == 32 + MAX_TUBES


# -- AutoSmooth -----------------------------------------------------------


def box() -> Mesh:
    """A unit cube, shaded flat: six planes and twelve right angles."""
    corner = np.array(
        [[a, b, c] for a in (-1.0, 1.0) for b in (-1.0, 1.0) for c in (-1.0, 1.0)]
    )
    face = np.array(
        [
            [0, 1, 3], [0, 3, 2], [4, 7, 5], [4, 6, 7],
            [0, 4, 5], [0, 5, 1], [2, 3, 7], [2, 7, 6],
            [0, 2, 6], [0, 6, 4], [1, 5, 7], [1, 7, 3],
        ],
        dtype=np.int64,
    )
    return plane_volume._flat_mesh(corner, face, "box")


def test_autosmooth_leaves_a_real_plane_change_hard() -> None:
    """Every edge of a cube is a right angle, and no reading of AutoSmooth short
    of one that joins right angles may touch it.  The two triangles of a face
    are a different matter: they lie in the same plane, so they were always one
    facet and joining them changes nothing."""
    cube = box()
    for degrees in (SMOOTH_MIN, 30.0, 60.0, SMOOTH_MAX):
        shaded = auto_smooth(cube, degrees)
        assert np.array_equal(shaded.normals, cube.normals)
        assert np.array_equal(shaded.positions, cube.positions)


def test_autosmooth_changes_the_shading_and_never_the_shape() -> None:
    """It is a re-reading of the normals: the same points, the same triangles,
    and unit normals throughout.  At zero it is not even that."""
    mesh = ball()
    planes = plane_regions(mesh).for_count(14)
    flat = sculpt_mesh(mesh, planes, SculptMode.SUBTRACTIVE, 4, 0, 0.0)
    shaded = sculpt_mesh(mesh, planes, SculptMode.SUBTRACTIVE, 4, 0, 30.0)
    assert np.array_equal(shaded.positions, flat.positions)
    assert np.array_equal(shaded.indices, flat.indices)
    assert not np.array_equal(shaded.normals, flat.normals)
    assert np.allclose(np.linalg.norm(shaded.normals, axis=1), 1.0, atol=1e-5)
    assert volume(shaded) == pytest.approx(volume(flat))
    assert auto_smooth(flat, 0.0) is flat


def test_autosmooth_reads_a_lattice_facet_as_one_plane() -> None:
    """The reason it is here.  A facet that comes out of a lattice is only
    roughly one plane -- its triangles each lean by a fraction of a degree --
    so shading each on its own turns a flat into a mosaic.  Grouping them
    leaves far fewer directions on the form, and every one of the ones that
    survives is a plane change the fit actually found."""
    mesh = ball()
    planes = plane_regions(mesh).for_count(14)
    flat = sculpt_mesh(mesh, planes, SculptMode.SUBTRACTIVE, 4, 0, 0.0)
    counted = [
        len(np.unique(np.round(auto_smooth(flat, deg).normals, 4), axis=0))
        for deg in (0.0, 30.0)
    ]
    assert counted[1] < counted[0]


# -- the cache ------------------------------------------------------------


def test_the_cache_only_refits_what_has_actually_gone_stale(monkeypatch) -> None:
    """The fit is the expensive part and it only goes stale when the model or
    the design matrix changes.  Turning the form over from clay to stone, or
    working the masses, must never touch it."""
    mesh = ball()
    fits = 0
    real = plane_regions

    def counted(*args, **rest):
        nonlocal fits
        fits += 1
        return real(*args, **rest)

    monkeypatch.setattr("refview.core.plane_solids.plane_regions", counted)
    cache = SculptCache()

    first = cache.mesh_for(
        mesh, PlaneSettings(enabled=True, target=PlaneTarget.GEOMETRY, sculpt_detail=30.0)
    )
    assert fits == 1 and first is not None

    settings = PlaneSettings(
        enabled=True, target=PlaneTarget.GEOMETRY, sculpt_detail=70.0
    )
    assert cache.mesh_for(mesh, settings) is not first
    assert fits == 1  # a different count, the same fit

    stone = PlaneSettings(
        enabled=True,
        target=PlaneTarget.GEOMETRY,
        sculpt_detail=70.0,
        sculpt=SculptMode.SUBTRACTIVE,
    )
    clay = PlaneSettings(
        enabled=True,
        target=PlaneTarget.GEOMETRY,
        sculpt_detail=70.0,
        sculpt=SculptMode.ADDITIVE,
    )
    assert volume(cache.mesh_for(mesh, stone)) > volume(cache.mesh_for(mesh, clay))
    assert fits == 1

    fuller = PlaneSettings(
        enabled=True,
        target=PlaneTarget.GEOMETRY,
        sculpt_detail=70.0,
        sculpt=SculptMode.ADDITIVE,
        sculpt_masses=8,
    )
    assert volume(cache.mesh_for(mesh, fuller)) > volume(cache.mesh_for(mesh, clay))
    assert fits == 1  # the masses are not a reason to refit either

    settled = PlaneSettings(
        enabled=True,
        target=PlaneTarget.GEOMETRY,
        sculpt_detail=70.0,
        sculpt=SculptMode.ADDITIVE,
        sculpt_relax=8,
    )
    assert cache.mesh_for(mesh, settled) is not cache.mesh_for(mesh, clay)
    assert fits == 1  # nor is the relax

    cache.clear()
    assert cache.mesh_for(mesh, settings) is not None
    assert fits == 2


def test_a_finer_lattice_resolves_the_same_form_more_closely() -> None:
    """What a number typed past the end of the detail slider buys.  The reading
    of the form is the same -- the same planes, the same count of blocks -- and
    it is resolved on a finer lattice, which shows as more and smaller facets.
    Both modes still stand where they did: stone outside the model, clay in."""
    mesh = ball()
    planes = plane_regions(mesh).for_count(14)
    for sculpt in SculptMode:
        coarse = sculpt_mesh(mesh, planes, sculpt, 4, 0, 0.0, fineness=1.0)
        fine = sculpt_mesh(mesh, planes, sculpt, 4, 0, 0.0, fineness=1.8)
        assert len(fine.indices) > 1.5 * len(coarse.indices)
        if sculpt is SculptMode.ADDITIVE:
            assert volume(coarse) < volume(mesh) and volume(fine) < volume(mesh)
        else:
            assert volume(coarse) > volume(mesh) and volume(fine) > volume(mesh)

    # A fineness at or under one is the lattice the slider itself asks for, so
    # it has to come back bit for bit the same as not asking at all.
    plain = sculpt_mesh(mesh, planes, SculptMode.ADDITIVE, 4, 0, 0.0, fineness=1.0)
    under = sculpt_mesh(mesh, planes, SculptMode.ADDITIVE, 4, 0, 0.0, fineness=0.5)
    assert np.array_equal(plain.positions, under.positions)


def test_reshading_the_form_does_not_rebuild_it(monkeypatch) -> None:
    """AutoSmooth reads the normals of a form that has already been built, so
    it must cost a tenth of a second rather than the seconds a rebuild costs.
    Sharing a cache slot with the volume would have made a shading knob into
    the most expensive one on the panel."""
    mesh = ball()
    builds = 0
    real = plane_volume.carve

    def counted(*args, **rest):
        nonlocal builds
        builds += 1
        return real(*args, **rest)

    monkeypatch.setattr("refview.core.plane_solids.carve", counted)
    cache = SculptCache()

    kept = {"enabled": True, "target": PlaneTarget.GEOMETRY, "sculpt_detail": 30.0}
    first = cache.mesh_for(mesh, PlaneSettings(**kept, sculpt_smooth=30.0))
    assert builds == 1 and first is not None

    again = cache.mesh_for(mesh, PlaneSettings(**kept, sculpt_smooth=70.0))
    assert builds == 1  # the volume was not touched
    assert again is not first
    assert np.array_equal(again.positions, first.positions)
    assert not np.array_equal(again.normals, first.normals)

    assert cache.mesh_for(mesh, PlaneSettings(**kept, sculpt_masses=9)) is not again
    assert builds == 2  # and a change to the volume still rebuilds it

    # The lattice is part of the volume, so a detail typed past the slider's
    # end has to rebuild even though it asks for exactly the same planes.
    fine = PlaneSettings(
        enabled=True, target=PlaneTarget.GEOMETRY, sculpt_detail=DETAIL_CEILING
    )
    assert cache.mesh_for(mesh, fine) is not None
    assert builds == 3

    # So is the median, which is run over the volume before its surface is
    # found rather than over the surface afterwards.
    assert cache.mesh_for(mesh, PlaneSettings(**kept, sculpt_median=4)) is not None
    assert builds == 4
    assert cache.mesh_for(mesh, PlaneSettings(**kept, sculpt_median_reach=2)) is not None
    assert builds == 5


def test_the_cache_stands_aside_unless_the_geometry_target_asked_for_it() -> None:
    mesh = ball()
    cache = SculptCache()
    assert cache.mesh_for(mesh, PlaneSettings(enabled=True, target=PlaneTarget.NORMALS)) is None
    assert cache.mesh_for(None, PlaneSettings(enabled=True, target=PlaneTarget.GEOMETRY)) is None
    assert (
        cache.mesh_for(mesh, PlaneSettings(enabled=True, target=PlaneTarget.GEOMETRY))
        is not None
    )


# -- clay built on an armature --------------------------------------------
#
# The free-seeded mode asks the distance field where the masses of a form are.
# Given an armature it asks nobody: the artist has already said, by bending a
# wire, and the whole of what these assert is that the answer is honoured --
# each lump is laid *on* its length of wire, in the order they were listed,
# and the lumps that follow still land wherever the wire did not reach.


def _bar(length: float = 2.2, radius: float = 0.5) -> Mesh:
    """A long ellipsoid: one closed form with an obvious axis to lie along."""
    round_one = ball(radius=radius)
    points = round_one.positions * np.array([0.5 * length / radius, 1.0, 1.0])
    faces = round_one.indices
    return Mesh(points, compute_vertex_normals(points, faces), faces, "bar")


def _bed_for(mesh: Mesh) -> tuple:
    """A model read onto a lattice, ready for lumps to be laid on it."""
    triangles = np.asarray(mesh.indices, dtype=np.int64).reshape(-1, 3)
    seeds, leaning = surface_seeds(
        np.asarray(mesh.positions, dtype=np.float64),
        triangles,
        unit_normals(mesh),
        seed_spacing(mesh, TEST_RESOLUTION),
    )
    bed = plane_volume.lay_bed(mesh.positions, triangles, seeds, leaning, TEST_RESOLUTION)
    return bed, plane_volume.fitted_facings(plane_regions(mesh).for_count(14).directions)


def _holds(lump, point) -> bool:
    """Whether a fitted solid has a point inside it."""
    facing, offsets = lump[0], lump[1]
    return bool((facing @ np.asarray(point, dtype=np.float64) - offsets).max() <= 1e-9)


def _wires(*segments, girth: float = 0.3, off: tuple = ()) -> plane_volume.Wires:
    """An armature for the volume, with ``off`` naming the rows taking no clay."""
    ends = np.asarray(segments, dtype=np.float64).reshape(-1, 2, 3)
    laid = np.ones(len(ends), dtype=bool)
    laid[list(off)] = False
    return plane_volume.Wires(
        ends=ends, girth=np.full((len(ends), 2), girth), laid=laid
    )


def test_a_lump_laid_on_a_wire_holds_the_wire() -> None:
    """The claim the whole armature mode rests on.

    A lump that merely landed near its bone would be the free seeding wearing
    a different label.  What makes this building *on* an armature is that the
    segment is inside the solid, so the clay is wrapped round the wire the way
    clay really is.
    """
    mesh = _bar()
    bed, bevels = _bed_for(mesh)
    wires = _wires(
        [[-0.8, 0.0, 0.0], [0.0, 0.0, 0.0]],
        [[0.0, 0.0, 0.0], [0.8, 0.0, 0.0]],
    )
    lumps = plane_volume.clay_lumps(bed.model, bed.origin, bed.step, bevels, 1, 2, wires)[0]

    assert len(lumps) == 2
    for lump, (first, second) in zip(lumps, wires.ends, strict=True):
        assert _holds(lump, first)
        assert _holds(lump, second)
        assert _holds(lump, 0.5 * (first + second))


def test_a_lump_laid_on_a_wire_still_never_grows_out_through_the_model() -> None:
    """The wire says where the clay goes; the model still says how far.

    A lump started from a whole segment rather than from a point has a far
    larger shape to be pulled back in, so this is the one that would break if
    the pulling back were skipped -- and asked of the lump rather than of the
    finished mesh, which is held under the model afterwards and would hide the
    fault.

    Measured in cells, because cells are the whole of the tolerance: a lump is
    grown against corners of the lattice, so between two of them it has
    nothing to hold it and it may bulge by about that much.  What is asserted
    is that the bulge stays at the scale of the lattice, which is where the
    model itself takes over.
    """
    mesh = _bar()
    bed, bevels = _bed_for(mesh)
    # Deliberately far fatter than the bar, so the model has to do the
    # stopping rather than the thickness the wire declares.
    wires = _wires([[-0.9, 0.0, 0.0], [0.9, 0.0, 0.0]], girth=2.0)
    lumps = plane_volume.clay_lumps(bed.model, bed.origin, bed.step, bevels, 1, 1, wires)[0]
    assert len(lumps) == 1

    grid = np.stack(plane_volume._axes(bed.origin, bed.step, bed.shape), axis=-1)
    inside = (grid @ lumps[0][0].T <= lumps[0][1]).all(axis=-1)
    assert inside.any()
    beyond = inside & ~bed.within
    overshoot = 0.0 if not beyond.any() else float(bed.model[beyond].max())
    assert overshoot <= 2.0 * bed.step


def test_clay_built_on_a_wire_still_sits_within_the_model() -> None:
    """The invariant an artist actually sees, on the finished stand-in: clay
    is added from the inside out, and being told where to add it does not
    change which side of the surface it ends up on."""
    mesh = _bar()
    planes = plane_regions(mesh).for_count(14)
    wires = _wires([[-0.8, 0.0, 0.0], [0.8, 0.0, 0.0]], girth=0.6)
    out = sculpt_mesh(mesh, planes, SculptMode.ADDITIVE, 1, wires=wires)
    assert volume(out) < volume(mesh)
    assert out.bounds.radius <= mesh.bounds.radius + 1e-6


def test_the_clay_goes_down_the_wire_in_the_order_it_is_listed() -> None:
    """Which is what makes the order worth reordering, and what a film of a
    block-in built on an armature scrubs through."""
    mesh = _bar()
    bed, bevels = _bed_for(mesh)
    ends = [
        [[-0.9, 0.0, 0.0], [-0.4, 0.0, 0.0]],
        [[-0.1, 0.0, 0.0], [0.1, 0.0, 0.0]],
        [[0.4, 0.0, 0.0], [0.9, 0.0, 0.0]],
    ]
    forward, backward = _wires(*ends), _wires(*reversed(ends))

    first = plane_volume.clay_lumps(bed.model, bed.origin, bed.step, bevels, 1, 1, forward)[0]
    last = plane_volume.clay_lumps(bed.model, bed.origin, bed.step, bevels, 1, 1, backward)[0]

    assert len(first) == 1
    assert len(last) == 1
    assert _holds(first[0], ends[0][0])
    assert _holds(last[0], ends[-1][1])
    assert not _holds(first[0], ends[-1][1])


def test_a_budget_shorter_than_the_wire_takes_the_wire_from_the_top() -> None:
    mesh = _bar()
    bed, bevels = _bed_for(mesh)
    wires = _wires(
        [[-0.9, 0.0, 0.0], [-0.4, 0.0, 0.0]],
        [[-0.1, 0.0, 0.0], [0.1, 0.0, 0.0]],
        [[0.4, 0.0, 0.0], [0.9, 0.0, 0.0]],
    )
    for wanted in (1, 2, 3):
        lumps = plane_volume.clay_lumps(
            bed.model, bed.origin, bed.step, bevels, 1, wanted, wires
        )[0]
        assert len(lumps) == wanted
        # The wire is taken from the top, so the lumps are its first `wanted`
        # bones and nothing else.
        for lump, (a, b) in zip(lumps, wires.ends[:wanted], strict=True):
            assert _holds(lump, 0.5 * (a + b))


def test_detail_past_the_end_of_the_wire_is_still_found_the_old_way() -> None:
    """An armature is a guide, not a cage.

    Once the wire has been laid on, the lumps that follow go wherever the most
    material is still uncovered -- which is what puts the hands and the feet in
    after the block-in.
    """
    mesh = _bar()
    bed, bevels = _bed_for(mesh)
    wires = _wires([[-0.7, 0.0, 0.0], [-0.3, 0.0, 0.0]])

    lumps = plane_volume.clay_lumps(bed.model, bed.origin, bed.step, bevels, 1, 6, wires)[0]
    assert len(lumps) > 1
    # The far end of the bar is nowhere near the single length of wire, so
    # something laid after it has to have reached there by itself.
    assert any(_holds(lump, [0.85, 0.0, 0.0]) for lump in lumps[1:])


def test_a_wire_the_model_has_nothing_to_say_about_is_passed_over() -> None:
    """A guide may reach somewhere this model does not go -- a wire drawn for
    one figure and reused on another, or a preset half placed.  That should
    cost the wire rather than the whole block-in."""
    mesh = _bar()
    bed, bevels = _bed_for(mesh)
    wires = _wires(
        [[0.0, 6.0, 0.0], [0.0, 8.0, 0.0]],  # nowhere near the model
        [[-0.5, 0.0, 0.0], [0.5, 0.0, 0.0]],
    )
    lumps = plane_volume.clay_lumps(bed.model, bed.origin, bed.step, bevels, 1, 2, wires)[0]

    assert len(lumps) == 2  # the budget is spent, not lost
    assert _holds(lumps[0], [0.0, 0.0, 0.0])  # by the wire that could be laid on


def test_the_wire_says_how_thick_the_clay_is() -> None:
    """A node's size is a measurement the artist took, so thinning one thins
    the clay laid along the bone it ends -- which is the only way to say that
    the arm is thinner than the sleeve a scan gave it."""
    mesh = ball()
    bed, bevels = _bed_for(mesh)
    ends = [[[-0.5, 0.0, 0.0], [0.5, 0.0, 0.0]]]
    thin, fat = _wires(*ends, girth=0.05), _wires(*ends, girth=1.0)

    def across(wires) -> float:
        lump = plane_volume.clay_lumps(
            bed.model, bed.origin, bed.step, bevels, 1, 1, wires
        )[0][0]
        low, high = plane_volume.piece_bounds(lump[2], lump[1])
        return float((high - low)[1:].max())  # across the wire, not along it

    assert across(thin) < 0.5 * across(fat)


def test_an_armature_is_read_into_the_wire_the_volume_wants() -> None:
    assert wires_for(None) is None
    assert wires_for(Armature()) is None  # nothing joined up yet

    armature = Armature(
        nodes=[
            ArmatureNode(name="A", at=(0.0, 0.0, 0.0), size=0.4),
            ArmatureNode(name="B", at=(1.0, 0.0, 0.0)),
        ],
        bones=[Bone(0, 1, "Shin")],
    )
    wires = wires_for(armature)
    assert wires is not None
    assert len(wires) == 1
    assert wires.ends[0][1] == pytest.approx([1.0, 0.0, 0.0])
    assert wires.girth[0][0] == pytest.approx(0.4)
    assert wires.girth[0][1] == pytest.approx(armature.default_size())
    # Two readings of one wire have to compare equal, or the cache would
    # re-cut the form every time the panel looked at it.
    assert wires.signature == wires_for(armature).signature


def test_stone_is_never_built_on_an_armature(rounded) -> None:
    """It is cut out of a block rather than built up on anything, so handing
    it a wire has to be a no-op rather than a quiet change of shape."""
    mesh, axes = rounded
    planes = axes.for_count(14)
    wires = _wires([[-0.5, 0.0, 0.0], [0.5, 0.0, 0.0]])
    bare = sculpt_mesh(mesh, planes, SculptMode.SUBTRACTIVE, 4)
    wired = sculpt_mesh(mesh, planes, SculptMode.SUBTRACTIVE, 4, wires=wires)
    assert np.array_equal(bare.positions, wired.positions)


def test_the_cache_re_cuts_the_form_when_the_wire_moves(rounded) -> None:
    mesh, _axes = rounded
    settings = PlaneSettings(
        enabled=True, target=PlaneTarget.GEOMETRY, sculpt=SculptMode.ADDITIVE
    )
    cache = SculptCache()
    here = _wires([[-0.4, 0.0, 0.0], [0.4, 0.0, 0.0]])
    first = cache.mesh_for(mesh, settings, here)
    assert cache.mesh_for(mesh, settings, here) is first  # nothing moved

    there = _wires([[0.0, -0.4, 0.0], [0.0, 0.4, 0.0]])
    assert cache.mesh_for(mesh, settings, there) is not first


def test_a_bone_turned_off_is_carried_through_rather_than_dropped() -> None:
    """It has to be, because it says where the clay may not go, and the volume
    cannot keep off a part of the form nobody told it about."""
    armature = Armature(
        nodes=[
            ArmatureNode(name="A", at=(0.0, 0.0, 0.0), size=0.3),
            ArmatureNode(name="B", at=(1.0, 0.0, 0.0), size=0.3),
            ArmatureNode(name="C", at=(2.0, 0.0, 0.0), size=0.3),
        ],
        bones=[Bone(0, 1, "Thigh"), Bone(1, 2, "Shin")],
    )
    assert wires_for(armature).count == 2

    armature.bones[0].laid = False
    wires = wires_for(armature)
    assert len(wires) == 2  # both are still described ...
    assert wires.count == 1  # ... and one of them takes a lump
    assert list(wires.laying) == [1]

    # An armature with nothing laid on it says nothing at all, rather than
    # saying to leave the whole figure bare: that is the artist emptying the
    # list in order to tick a few bones back.
    armature.bones[1].laid = False
    assert wires_for(armature) is None


def test_the_clay_keeps_off_a_bone_that_was_turned_off_however_much_detail_is_asked_for() -> None:
    """Turning a bone off is a statement about the form, not about the seeding.

    Skipping the *lump* would be no use at all: the next turn of the Detail
    slider would find that part of the form by itself and fill it in anyway,
    which is exactly what an artist meaning to model it themselves does not
    want.  So the material under a bone that takes no clay leaves the lattice
    altogether, and no amount of detail brings it back.
    """
    mesh = _bar()
    bed, bevels = _bed_for(mesh)
    here, off_the_end = [-0.6, 0.0, 0.0], [0.7, 0.0, 0.0]
    wires = _wires(
        [[-0.9, 0.0, 0.0], [-0.3, 0.0, 0.0]],
        [[0.4, 0.0, 0.0], [1.0, 0.0, 0.0]],
        girth=0.5,
        off=(1,),
    )
    for wanted in (1, 4, 16):
        lumps = plane_volume.clay_lumps(
            bed.model, bed.origin, bed.step, bevels, 1, wanted, wires
        )[0]
        assert any(_holds(lump, here) for lump in lumps)
        assert not any(_holds(lump, off_the_end) for lump in lumps)


def test_what_no_bone_claims_is_still_found_the_old_way() -> None:
    """An armature is a guide over the parts it speaks for and silent about
    the rest, so detail past the end of the wire still lands wherever the most
    material is uncovered -- which is what puts the hands and the feet in."""
    mesh = _bar()
    bed, bevels = _bed_for(mesh)
    wires = _wires([[-0.7, 0.0, 0.0], [-0.3, 0.0, 0.0]])

    only_wire = plane_volume.clay_lumps(
        bed.model, bed.origin, bed.step, bevels, 1, 1, wires
    )[0]
    assert not _holds(only_wire[0], [0.7, 0.0, 0.0])

    with_detail = plane_volume.clay_lumps(
        bed.model, bed.origin, bed.step, bevels, 1, 5, wires
    )[0]
    assert any(_holds(lump, [0.7, 0.0, 0.0]) for lump in with_detail)


def test_material_two_bones_share_belongs_to_the_one_still_being_laid() -> None:
    """Or turning the hand off would take a bite out of the forearm it shares
    a wrist with, and the artist would be punished for saying something
    reasonable."""
    mesh = _bar()
    bed, bevels = _bed_for(mesh)
    joint = [0.0, 0.0, 0.0]
    wires = _wires(
        [[-0.9, 0.0, 0.0], joint],
        [joint, [0.9, 0.0, 0.0]],
        girth=0.5,
        off=(1,),
    )
    lumps = plane_volume.clay_lumps(bed.model, bed.origin, bed.step, bevels, 1, 3, wires)[0]

    assert lumps
    # The joint the two share is still laid on, by the bone that kept it.
    assert _holds(lumps[0], joint)
    assert not any(_holds(lump, [0.8, 0.0, 0.0]) for lump in lumps)
