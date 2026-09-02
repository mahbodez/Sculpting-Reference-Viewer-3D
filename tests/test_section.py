"""Cutting planes, the contour they produce and the pedestal under the model."""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.mesh import Bounds, Mesh, compute_vertex_normals
from refview.core.pedestal import PedestalSettings, build_pedestal
from refview.core.section import (
    SectionAxis,
    SectionMode,
    SectionSettings,
    section_segments,
)


def _box(size: float = 1.0) -> Mesh:
    """A closed axis-aligned cube centred on the origin."""
    half = size * 0.5
    corners = np.array(
        [(x, y, z) for x in (-half, half) for y in (-half, half) for z in (-half, half)],
        dtype=np.float32,
    )
    faces = np.array(
        [
            (0, 1, 3), (0, 3, 2),  # -x
            (4, 7, 5), (4, 6, 7),  # +x
            (0, 4, 5), (0, 5, 1),  # -y
            (2, 3, 7), (2, 7, 6),  # +y
            (0, 2, 6), (0, 6, 4),  # -z
            (1, 5, 7), (1, 7, 3),  # +z
        ],
        dtype=np.uint32,
    )
    return Mesh(corners, compute_vertex_normals(corners, faces), faces)


def test_a_disabled_section_cuts_with_nothing():
    assert SectionSettings().planes() == []


def test_keeping_below_cuts_away_the_positive_side():
    settings = SectionSettings(enabled=True, axis=SectionAxis.Y, offset=0.25)
    (plane,) = settings.planes()
    assert np.allclose(plane.normal, [0.0, 1.0, 0.0])
    # Above the plane is cut away, below it survives.
    assert plane.distances(np.array([[0.0, 1.0, 0.0]]))[0] > 0.0
    assert plane.distances(np.array([[0.0, -1.0, 0.0]]))[0] < 0.0


def test_flipping_reverses_which_side_survives():
    settings = SectionSettings(enabled=True, axis=SectionAxis.Y, flip=True)
    (plane,) = settings.planes()
    assert plane.distances(np.array([[0.0, 1.0, 0.0]]))[0] < 0.0


def test_a_slice_keeps_the_material_between_two_planes():
    settings = SectionSettings(
        enabled=True, axis=SectionAxis.Y, mode=SectionMode.SLAB, thickness=0.4, offset=1.0
    )
    top, bottom = settings.planes()
    inside = np.array([[0.0, 1.0, 0.0]])
    assert top.distances(inside)[0] < 0.0 and bottom.distances(inside)[0] < 0.0
    for outside in ([[0.0, 1.5, 0.0]], [[0.0, 0.5, 0.0]]):
        distances = [plane.distances(np.array(outside))[0] for plane in (top, bottom)]
        assert max(distances) > 0.0


def test_a_custom_normal_is_normalised():
    settings = SectionSettings(
        enabled=True, axis=SectionAxis.CUSTOM, custom_normal=(0.0, 0.0, 5.0)
    )
    assert np.allclose(settings.normal, [0.0, 0.0, 1.0])


def test_cutting_a_cube_traces_a_closed_square():
    """The contour of a plane through a cube is its cross-section outline."""
    mesh = _box(2.0)
    (plane,) = SectionSettings(enabled=True, axis=SectionAxis.Y).planes()
    segments = section_segments(mesh, plane)
    assert len(segments) >= 8  # two triangles cut per side face
    assert np.allclose(segments[:, :, 1], 0.0)  # every point sits on the plane
    extent = segments.reshape(-1, 3)
    assert extent[:, 0].min() == pytest.approx(-1.0)
    assert extent[:, 0].max() == pytest.approx(1.0)


def test_a_plane_that_misses_the_model_traces_nothing():
    mesh = _box()
    (plane,) = SectionSettings(enabled=True, axis=SectionAxis.Y, offset=10.0).planes()
    assert len(section_segments(mesh, plane)) == 0


def test_the_pedestal_sits_under_the_lowest_vertex():
    bounds = Bounds(np.array([-1.0, -2.0, -1.0]), np.array([1.0, 2.0, 1.0]))
    disc = build_pedestal(bounds, PedestalSettings(enabled=True, diameter=2.0))
    assert disc is not None
    assert disc.bounds.maximum[1] == pytest.approx(-2.0)  # top face at the model's base
    assert disc.bounds.minimum[1] < -2.0  # and thickness below it
    assert disc.bounds.size[0] == pytest.approx(4.0)  # diameter 2 x the 2-unit footprint


def test_the_pedestal_can_be_placed_at_a_chosen_level():
    bounds = Bounds(np.array([-1.0, -2.0, -1.0]), np.array([1.0, 2.0, 1.0]))
    settings = PedestalSettings(enabled=True, snap_to_lowest=False, level=0.5)
    disc = build_pedestal(bounds, settings)
    assert disc is not None and disc.bounds.maximum[1] == pytest.approx(0.5)


def test_no_pedestal_when_it_is_switched_off():
    bounds = Bounds(np.zeros(3), np.ones(3))
    assert build_pedestal(bounds, PedestalSettings()) is None
