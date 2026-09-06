"""Fitting planes to a model's surface rather than only to its normals.

What matters is not that a particular algorithm ran.  It is that a form whose
planes are known is broken into those planes; that two parts of a form facing
the same way are two planes and not one, which is the whole reason for reading
where the surface is; that the flats of the form decide where a plane sits and
a scattering of bad normals inside one does not; and that the slider behaves,
handing back the count it names and refining the break rather than rebuilding
it where the fit is a hierarchy.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from refview.core.mesh import Mesh, compute_vertex_normals
from refview.core.plane_axes import MAX_PLANE_AXES, Coefficients, plane_axes
from refview.core.plane_clusters import flatness, plane_flats, plane_regions
from refview.core.settings import PlaneMode

FITTERS = (plane_regions, plane_flats)

AXIS_DIRECTIONS = np.array(
    [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], dtype=np.float64
)


def quad(points: list, normals: list, triangles: list, corners, normal) -> None:
    """Add one flat quad, with its own vertices, to a mesh under construction."""
    base = len(points)
    for corner in corners:
        points.append(corner)
        normals.append(normal)
    triangles += [[base, base + 1, base + 2], [base, base + 2, base + 3]]


def cube(steps: int = 6) -> Mesh:
    """A cube with hard edges, each face cut into a grid of triangles."""
    points: list = []
    normals: list = []
    triangles: list = []
    grid = np.linspace(-1.0, 1.0, steps + 1)
    for axis in range(3):
        for sign in (1.0, -1.0):
            normal = np.zeros(3)
            normal[axis] = sign
            across = np.zeros(3)
            across[(axis + 1) % 3] = 1.0
            up = np.zeros(3)
            up[(axis + 2) % 3] = 1.0
            base = len(points)
            for u in grid:
                for v in grid:
                    points.append(normal + u * across + v * up)
                    normals.append(normal)
            for i in range(steps):
                for j in range(steps):
                    corner = base + i * (steps + 1) + j
                    triangles += [
                        [corner, corner + 1, corner + steps + 1],
                        [corner + 1, corner + steps + 2, corner + steps + 1],
                    ]
    return Mesh(np.array(points), np.array(normals), np.array(triangles, dtype=np.uint32))


def sphere(rings: int = 40, sectors: int = 80) -> Mesh:
    """A UV sphere, whose normals cover every direction evenly."""
    down = np.linspace(1e-3, math.pi - 1e-3, rings)
    around = np.linspace(0.0, 2.0 * math.pi, sectors)
    dd, aa = np.meshgrid(down, around, indexing="ij")
    points = np.stack(
        [np.sin(dd) * np.cos(aa), np.cos(dd), np.sin(dd) * np.sin(aa)], axis=-1
    ).reshape(-1, 3)
    triangles = []
    for ring in range(rings - 1):
        for sector in range(sectors - 1):
            corner = ring * sectors + sector
            triangles += [
                [corner, corner + 1, corner + sectors],
                [corner + 1, corner + sectors + 1, corner + sectors],
            ]
    return Mesh(points, points, np.array(triangles, dtype=np.uint32))


def step() -> Mesh:
    """Two broad faces both looking straight up, one raised above the other.

    The case the normals alone cannot read: every normal in the model is the
    same, so a fit that sees only facings has one plane to offer and no way to
    know there are two.
    """
    points: list = []
    normals: list = []
    triangles: list = []
    quad(points, normals, triangles, [[-2, 0, -1], [0, 0, -1], [0, 0, 1], [-2, 0, 1]], [0, 1, 0])
    quad(points, normals, triangles, [[0, 1, -1], [2, 1, -1], [2, 1, 1], [0, 1, 1]], [0, 1, 0])
    return Mesh(np.array(points, float), np.array(normals, float), np.array(triangles, np.uint32))


def worst_miss_deg(wanted: np.ndarray, offered: np.ndarray) -> float:
    """How far the least well served of ``wanted`` is from anything offered."""
    nearest = (wanted @ offered.T).max(axis=1)
    return float(np.degrees(np.arccos(np.clip(nearest, -1.0, 1.0))).max())


def angle_deg(direction: np.ndarray, against: np.ndarray) -> float:
    return float(np.degrees(np.arccos(np.clip(direction @ against, -1.0, 1.0))))


@pytest.mark.parametrize("fit", FITTERS)
def test_a_cube_breaks_into_its_own_six_faces(fit):
    """The one form whose planes are not a matter of opinion."""
    planes = fit(cube()).for_count(6)
    assert len(planes) == 6
    found = planes.directions.astype(np.float64)
    assert worst_miss_deg(AXIS_DIRECTIONS, found) == pytest.approx(0.0, abs=1e-3)


@pytest.mark.parametrize("fit", FITTERS)
def test_two_faces_looking_the_same_way_stay_two_planes(fit):
    """The reason for reading where the surface is and not only which way.

    Both faces of the step point straight up, so nothing in their normals
    tells them apart; only their places do.  A fit that reads the places gives
    two planes with the same direction and different anchors, and the shader
    can then put a seam between them.
    """
    planes = fit(step()).for_count(2)
    assert len(planes) == 2
    assert planes.locality > 0.0
    apart = np.linalg.norm(planes.anchors[0] - planes.anchors[1])
    assert apart > 0.5
    assert abs(planes.offsets[0] - planes.offsets[1]) > 0.1


def test_reading_the_normals_alone_cannot_tell_that_step_apart():
    """The limit the clustered fits exist to lift, stated as a fact."""
    assert len(plane_axes(step()).for_count(2)) == 1


@pytest.mark.parametrize("fit", FITTERS)
def test_the_slider_hands_back_the_count_it_names(fit):
    fitted = fit(sphere())
    assert len(fitted) == MAX_PLANE_AXES
    for count in (1, 2, 5, 17, 40, MAX_PLANE_AXES):
        assert len(fitted.for_count(count)) == count


def test_a_step_of_the_slider_refines_the_break_rather_than_redoing_it():
    """Merging back from patches is a hierarchy, so the cuts of it nest.

    This is what makes the slider usable in Regions mode: an artist adding a
    plane sees a plane appear, not the whole model rearrange itself.  Flats
    makes no such promise -- it re-asks the question at every count -- so it
    is deliberately not held to this.
    """
    fitted = plane_regions(sphere())
    for count in range(2, 24):
        coarse = _rows(fitted.for_count(count))
        fine = _rows(fitted.for_count(count + 1))
        assert len(coarse & fine) == count - 1


def _rows(planes) -> set:
    """Every plane of a level as a hashable whole: direction, place and offset."""
    return {
        tuple(np.round(np.concatenate([direction, anchor, [offset]]), 5))
        for direction, anchor, offset in zip(
            planes.directions, planes.anchors, planes.offsets, strict=True
        )
    }


def test_strays_inside_a_plane_do_not_tilt_it():
    """A flat with a scattering of bad normals is still shaded as that flat.

    Averaging is what a stray normal gets its leverage from, so the direction
    of a plane is an M-estimate instead: the members that disagree most with
    the first guess are down-weighted and the guess is taken again.  The plain
    weighted mean is worked out here too, so the test says what the robustness
    is actually worth rather than only that some number came out small.
    """
    points: list = []
    normals: list = []
    triangles: list = []
    steps = 24
    grid = np.linspace(-1.0, 1.0, steps + 1)
    for i, u in enumerate(grid):
        for j, v in enumerate(grid):
            points.append([u, 0.0, v])
            stray = (i * (steps + 1) + j) % 17 == 0
            normals.append([0.6, 0.8, 0.0] if stray else [0.0, 1.0, 0.0])
    for i in range(steps):
        for j in range(steps):
            corner = i * (steps + 1) + j
            triangles += [
                [corner, corner + 1, corner + steps + 1],
                [corner + 1, corner + steps + 2, corner + steps + 1],
            ]
    mesh = Mesh(np.array(points, float), np.array(normals, float), np.array(triangles, np.uint32))

    up = np.array([0.0, 1.0, 0.0])
    averaged = np.asarray(normals, dtype=np.float64).mean(axis=0)
    averaged /= np.linalg.norm(averaged)
    assert angle_deg(averaged, up) > 1.5  # What plain averaging would have given.

    fitted = plane_regions(mesh).for_count(1).directions[0].astype(np.float64)
    assert angle_deg(fitted, up) < 0.5


def bent_plate(columns: int = 4) -> tuple[Mesh, np.ndarray]:
    """A plate creased down the middle, and which column each vertex is in.

    Flat to the left of the crease and turned up to the right of it, with the
    vertices along the crease shared and carrying the average of the two.  The
    columns well away from the crease have nothing but their own flat around
    them; the ones on it have the turn.
    """
    across = np.arange(-columns, columns + 1)
    along = np.linspace(-1.0, 1.0, 5)
    points: list = []
    normals: list = []
    columns_of: list = []
    flat = np.array([0.0, 1.0, 0.0])
    raised = np.array([-1.0, 1.0, 0.0]) / math.sqrt(2.0)
    crease = (flat + raised) / np.linalg.norm(flat + raised)
    for x in across:
        for z in along:
            height = 0.0 if x <= 0 else float(x)
            points.append([float(x), height, float(z)])
            normals.append(flat if x < 0 else (crease if x == 0 else raised))
            columns_of.append(int(x))
    triangles = []
    for i in range(len(across) - 1):
        for j in range(len(along) - 1):
            corner = i * len(along) + j
            triangles += [
                [corner, corner + 1, corner + len(along)],
                [corner + 1, corner + len(along) + 1, corner + len(along)],
            ]
    mesh = Mesh(np.array(points), np.array(normals), np.array(triangles, dtype=np.uint32))
    return mesh, np.array(columns_of)


def test_a_turn_in_the_form_gets_less_of_a_say_than_a_flat():
    """Vertices on a turn are ambiguous about their plane, so they are quieted.

    The crease normals belong to neither flat, and it is exactly those that
    would pull a plane off the flat it was meant to describe.  Well away from
    the crease every neighbour agrees, and there the vertex keeps its full say.
    """
    mesh, column = bent_plate()
    weights = flatness(mesh)

    assert weights[column == -3] == pytest.approx(1.0)   # deep inside the flat
    assert weights[column == 3] == pytest.approx(1.0)    # deep inside the raised side
    # Quietest on the crease itself, and back to full a couple of rows away.
    assert weights[column == 0].max() < weights[abs(column) == 1].min()
    assert weights[abs(column) == 1].max() < 1.0
    assert weights[column == 0].max() < 0.9
    # Never silenced: a model that is all turn has to break into planes too.
    assert (weights > 0.0).all()


def test_a_model_that_is_flat_all_over_gets_the_same_direction_everywhere():
    """Splitting a broad flat by place must not invent a turn in it.

    The plate below has one facing and a lot of surface, so a fit that reads
    place will happily divide it.  That is allowed -- the planes it makes
    shade identically, and the shader draws no seam between two planes facing
    the same way -- but every direction it hands back has to be the plate's.
    """
    planes = plane_regions(step()).for_count(6)
    up = np.array([0.0, 1.0, 0.0])
    for direction in planes.directions.astype(np.float64):
        assert angle_deg(direction, up) == pytest.approx(0.0, abs=1e-3)


@pytest.mark.parametrize("fit", FITTERS)
def test_every_direction_that_comes_back_is_a_unit_vector(fit):
    directions = fit(sphere()).for_count(MAX_PLANE_AXES).directions
    assert np.allclose(np.linalg.norm(directions, axis=1), 1.0, atol=1e-5)


@pytest.mark.parametrize("fit", FITTERS)
def test_the_same_model_always_breaks_the_same_way(fit):
    """Nothing is seeded at random, so a session reopens looking the same."""
    once, twice = fit(sphere()), fit(sphere())
    for count in (2, 9, 33, MAX_PLANE_AXES):
        assert np.array_equal(once.for_count(count).directions, twice.for_count(count).directions)
        assert np.array_equal(once.for_count(count).anchors, twice.for_count(count).anchors)


@pytest.mark.parametrize("fit", FITTERS)
def test_thinning_a_dense_model_does_not_change_what_it_is_made_of(fit):
    """The sample limit is a speed measure, so it must not move the planes.

    Asked of a cube rather than of a sphere, because a sphere has no planes to
    move: any even tiling of it is as good as any other, so a tiling that came
    out differently would say nothing about whether the thinning had cost
    anything.  A cube's six faces are the answer or they are not.
    """
    dense = cube(steps=48)
    assert dense.vertex_count > 10_000
    thinned = fit(dense, sample_limit=8_000).for_count(6).directions.astype(np.float64)
    assert worst_miss_deg(AXIS_DIRECTIONS, thinned) == pytest.approx(0.0, abs=1e-3)


@pytest.mark.parametrize("fit", FITTERS)
def test_a_model_with_no_geometry_offers_nothing(fit):
    """The renderer reads an empty set as "leave the normals alone"."""
    empty = Mesh(np.zeros((0, 3)), np.zeros((0, 3)), np.zeros((0, 3), dtype=np.uint32))
    fitted = fit(empty)
    assert fitted.is_empty
    assert fitted.for_count(8).directions.shape == (0, 3)


@pytest.mark.parametrize("fit", FITTERS)
def test_counts_outside_what_was_fitted_are_held_at_the_ends(fit):
    fitted = fit(sphere())
    assert len(fitted.for_count(0)) == 1
    assert len(fitted.for_count(-5)) == 1
    assert len(fitted.for_count(10_000)) == len(fitted)


@pytest.mark.parametrize("fit", FITTERS)
def test_asking_for_fewer_planes_stops_the_fit_early(fit):
    assert len(fit(sphere(), max_count=5)) == 5


@pytest.mark.parametrize("fit", FITTERS)
def test_the_frame_the_places_are_measured_in_comes_back_with_them(fit):
    """The shader has to put a fragment into that frame before it can look up
    which plane it belongs to, so the fit must say what the frame was."""
    mesh = sphere()
    planes = fit(mesh).for_count(8)
    assert planes.scale == pytest.approx(1.0 / mesh.bounds.radius)
    assert planes.origin == pytest.approx(mesh.bounds.center, abs=1e-5)
    assert np.abs(planes.anchors).max() < 2.0   # Inside the normalised frame.


def lumpy(rings: int = 60, sectors: int = 120) -> Mesh:
    """A form with real planes in it, and more than one facing the same way."""
    down = np.linspace(1e-3, math.pi - 1e-3, rings)
    around = np.linspace(0.0, 2.0 * math.pi, sectors)
    dd, aa = np.meshgrid(down, around, indexing="ij")
    reach = 1.0 + 0.30 * np.cos(3 * aa) * np.sin(2 * dd) + 0.18 * np.cos(4 * dd)
    points = np.stack(
        [
            np.sin(dd) * np.cos(aa) * reach,
            np.cos(dd) * reach * 1.25,
            np.sin(dd) * np.sin(aa) * reach,
        ],
        axis=-1,
    ).reshape(-1, 3)
    rr, ss = np.meshgrid(np.arange(rings - 1), np.arange(sectors - 1), indexing="ij")
    corner = (rr * sectors + ss).ravel()
    triangles = np.concatenate(
        [
            np.stack([corner, corner + 1, corner + sectors], axis=1),
            np.stack([corner + 1, corner + sectors + 1, corner + sectors], axis=1),
        ]
    ).astype(np.uint32)
    return Mesh(points, compute_vertex_normals(points, triangles), triangles)


def same_facing(directions: np.ndarray, within_deg: float = 12.0) -> int:
    """How many planes have another plane pointing very nearly where they do."""
    directions = directions.astype(np.float64)
    cosines = np.clip(directions @ directions.T, -1.0, 1.0)
    np.fill_diagonal(cosines, -1.0)
    return int((cosines.max(axis=1) > math.cos(math.radians(within_deg))).sum())


def test_leaning_on_position_breaks_a_form_up_as_well_as_down():
    """The coefficients have to reach the fit, and reaching it has to show.

    Two planes facing within a few degrees of each other are only worth having
    when they sit in different places; how readily the fit spends a plane on
    that is exactly what the position coefficient buys.
    """
    mesh = lumpy()
    quiet = plane_regions(mesh, Coefficients(locality=0.0, coplanarity=0.0)).for_count(24)
    loud = plane_regions(mesh, Coefficients(locality=2.0, coplanarity=2.0)).for_count(24)

    assert same_facing(quiet.directions) == 0
    assert same_facing(loud.directions) >= 4


def test_a_coefficient_of_zero_takes_the_term_out_of_the_shader_too():
    """The fit and the shader have to agree, or the boundaries drawn are not
    the boundaries between the clusters that were found.

    The columns carry the coefficients, and the fit measures a squared
    distance, so what the shader has to charge is the square of each.
    """
    mesh = lumpy()
    coefficients = Coefficients(locality=0.5, coplanarity=1.5)
    planes = plane_regions(mesh, coefficients).for_count(8)
    assert planes.locality == pytest.approx(0.25)
    assert planes.coplanarity == pytest.approx(2.25)

    off = plane_regions(mesh, Coefficients(locality=0.0, coplanarity=0.0)).for_count(8)
    assert off.locality == 0.0
    assert off.coplanarity == 0.0


def test_the_flat_span_says_how_much_of_the_form_counts_as_flat():
    """Narrow it and only the flattest surface has a say; widen it and the
    rounded turns get theirs back."""
    mesh = lumpy()
    narrow = flatness(mesh, 8.0)
    wide = flatness(mesh, 90.0)
    assert narrow.min() < 0.1
    assert wide.min() > 0.9
    # Nothing is ever silenced outright, at any setting.
    assert (narrow > 0.0).all()
    assert narrow.max() <= 1.0 and wide.max() <= 1.0


@pytest.mark.parametrize("fit", FITTERS)
def test_the_fit_reaches_past_the_old_ceiling_of_sixty_four(fit):
    """The planes moved out of a uniform array and into a texture so that the
    count could climb; the fit has to actually climb with it."""
    assert MAX_PLANE_AXES >= 256
    fitted = fit(lumpy())
    assert len(fitted) == MAX_PLANE_AXES
    for count in (65, 128, MAX_PLANE_AXES):
        planes = fitted.for_count(count)
        assert len(planes) == count
        # Still planes, not padding: every direction is a real unit vector.
        assert np.allclose(np.linalg.norm(planes.directions, axis=1), 1.0, atol=1e-5)
        assert len(np.unique(np.round(planes.directions, 4), axis=0)) > count // 2


def test_every_mode_the_panel_offers_can_be_fitted():
    """A mode with no fitter behind it would shade as an unbroken surface."""
    from refview.core.plane_clusters import fit_planes

    mesh = cube(steps=2)
    for mode in PlaneMode:
        fitted = fit_planes(mesh, mode)
        assert fitted.is_empty is (mode is PlaneMode.GRID)
    assert fit_planes(None, PlaneMode.REGIONS).is_empty
