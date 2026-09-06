"""Fitting planes to a model's own normals.

The properties that matter are not "the numbers came out": they are that a
form whose planes are known is broken into those planes, that turning the
slider refines the break rather than rebuilding it, and that a model which
cannot supply what is asked for says so instead of inventing directions.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from refview.core.mesh import Mesh
from refview.core.plane_axes import MAX_PLANE_AXES, plane_axes, vertex_weights

AXIS_DIRECTIONS = np.array(
    [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]], dtype=np.float64
)


def cube() -> Mesh:
    """A unit cube with hard edges: six faces, four corners each."""
    points: list[np.ndarray] = []
    normals: list[np.ndarray] = []
    triangles: list[list[int]] = []
    for axis in range(3):
        for sign in (1.0, -1.0):
            normal = np.zeros(3)
            normal[axis] = sign
            across = np.zeros(3)
            across[(axis + 1) % 3] = 1.0
            up = np.zeros(3)
            up[(axis + 2) % 3] = 1.0
            base = len(points)
            for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                points.append(normal + u * across + v * up)
                normals.append(normal)
            triangles += [[base, base + 1, base + 2], [base, base + 2, base + 3]]
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


def worst_miss_deg(wanted: np.ndarray, offered: np.ndarray) -> float:
    """How far the least well served of ``wanted`` is from anything offered."""
    nearest = (wanted @ offered.T).max(axis=1)
    return float(np.degrees(np.arccos(np.clip(nearest, -1.0, 1.0))).max())


def test_a_cube_breaks_into_its_own_six_faces():
    """The one form whose planes are not a matter of opinion."""
    axes = plane_axes(cube()).for_count(6).directions
    assert len(axes) == 6
    assert worst_miss_deg(AXIS_DIRECTIONS, axes.astype(np.float64)) == pytest.approx(0.0, abs=1e-4)


def test_normals_that_cancel_exactly_still_have_spread_to_split():
    """A cube's faces sum to nothing, which once read as nothing to split."""
    assert len(plane_axes(cube())) == 6


def test_every_direction_is_a_direction():
    axes = plane_axes(sphere()).for_count(MAX_PLANE_AXES).directions
    assert len(axes) == MAX_PLANE_AXES
    assert np.allclose(np.linalg.norm(axes, axis=1), 1.0, atol=1e-5)


def test_a_step_of_the_slider_refines_the_break_rather_than_redoing_it():
    """Going from k planes to k + 1 splits one of them and leaves the rest.

    This is what makes the slider usable: an artist adding a plane sees a
    plane appear, not the whole model rearrange itself.
    """
    fitted = plane_axes(sphere())
    for count in range(1, len(fitted)):
        coarse = {tuple(np.round(axis, 6)) for axis in fitted.for_count(count).directions}
        fine = {tuple(np.round(axis, 6)) for axis in fitted.for_count(count + 1).directions}
        assert len(coarse & fine) == count - 1


def test_the_same_model_always_breaks_the_same_way():
    """Sampling is strided, not random, so a session reopens looking the same."""
    once, twice = plane_axes(sphere()), plane_axes(sphere())
    for count in (2, 9, 33, MAX_PLANE_AXES):
        assert np.array_equal(
            once.for_count(count).directions, twice.for_count(count).directions
        )


def test_a_model_with_one_direction_offers_one_plane():
    """Asking a flat plate for eight planes gets its one, not eight copies."""
    flat = Mesh(
        np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]),
        np.tile([0.0, 1.0, 0.0], (3, 1)),
        np.array([[0, 1, 2]], dtype=np.uint32),
    )
    fitted = plane_axes(flat)
    assert len(fitted) == 1
    assert fitted.for_count(8).directions == pytest.approx(np.array([[0.0, 1.0, 0.0]]))


def test_a_model_with_no_geometry_offers_nothing():
    """The renderer reads an empty set as "leave the normals alone"."""
    empty = Mesh(np.zeros((0, 3)), np.zeros((0, 3)), np.zeros((0, 3), dtype=np.uint32))
    fitted = plane_axes(empty)
    assert fitted.is_empty
    assert fitted.for_count(8).directions.shape == (0, 3)


def test_counts_outside_what_was_fitted_are_held_at_the_ends():
    fitted = plane_axes(sphere())
    assert len(fitted.for_count(0)) == 1
    assert len(fitted.for_count(-5)) == 1
    assert len(fitted.for_count(10_000)) == len(fitted)


def test_a_plane_is_weighed_by_its_area_not_by_its_vertex_count():
    """A finely tessellated sliver must not outvote a broad flat face.

    The mesh here is one large square facing up and a tiny one facing forward,
    cut into far more triangles.  Counting vertices would make the sliver the
    dominant direction; counting area gives the square its due.
    """
    points = [[-1.0, 0.0, -1.0], [1.0, 0.0, -1.0], [1.0, 0.0, 1.0], [-1.0, 0.0, 1.0]]
    normals = [[0.0, 1.0, 0.0]] * 4
    triangles = [[0, 1, 2], [0, 2, 3]]
    for step in range(40):
        base = len(points)
        low, high = step * 0.001, (step + 1) * 0.001
        points += [[low, 2.0, 0.0], [high, 2.0, 0.0], [low, 2.001, 0.0]]
        normals += [[0.0, 0.0, 1.0]] * 3
        triangles.append([base, base + 1, base + 2])
    mesh = Mesh(np.array(points), np.array(normals), np.array(triangles, dtype=np.uint32))

    weights = vertex_weights(mesh)
    assert weights[:4].sum() > weights[4:].sum() * 100
    # With one plane to give, it must be the square's.
    kept = plane_axes(mesh).for_count(1).directions[0]
    assert kept == pytest.approx(np.array([0.0, 1.0, 0.0]), abs=1e-3)


def test_thinning_a_dense_model_does_not_change_what_it_is_made_of():
    """The sample limit is a speed measure, so it must not move the planes."""
    dense = sphere(rings=90, sectors=180)
    assert dense.vertex_count > 10_000
    thinned = plane_axes(dense, sample_limit=8_000).for_count(8).directions.astype(np.float64)
    whole = plane_axes(dense, sample_limit=dense.vertex_count).for_count(8).directions
    whole = whole.astype(np.float64)
    assert worst_miss_deg(whole, thinned) < 6.0


def test_asking_for_fewer_planes_stops_the_fit_early():
    assert len(plane_axes(sphere(), max_count=5)) == 5
