"""Surface annotations: erasing, splitting and the geometry handed to GL."""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.annotation import AnnotateMode, AnnotationSettings, AnnotationStore, Stroke
from refview.render.stroke_renderer import build_vertices


def line_stroke(count: int = 5, **kwargs) -> Stroke:
    """A stroke running along +X, one unit apart, with +Y normals."""
    return Stroke(
        points=[(float(index), 0.0, 0.0) for index in range(count)],
        normals=[(0.0, 1.0, 0.0)] * count,
        **kwargs,
    )


def test_normals_are_padded_to_match_the_points():
    stroke = Stroke(points=[(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)], normals=[(0.0, 1.0, 0.0)])
    assert stroke.normal_array.shape == (2, 3)
    assert np.allclose(stroke.normal_array[1], [0.0, 0.0, 0.0])


def test_erasing_the_middle_splits_a_stroke_in_two():
    store = AnnotationStore([line_stroke(5)])
    remaining = store.erased((2.0, 0.0, 0.0), 0.5)
    assert remaining is not None
    assert len(remaining) == 2
    assert [len(piece.points) for piece in remaining] == [2, 2]


def test_erasing_keeps_the_brush_and_drops_stubs():
    store = AnnotationStore([line_stroke(3, color=(0.1, 0.2, 0.3), width=5.0)])
    # Wide enough to leave a single orphaned point, which is not drawable.
    remaining = store.erased((1.0, 0.0, 0.0), 1.5)
    assert remaining == []

    store = AnnotationStore([line_stroke(4, color=(0.1, 0.2, 0.3), width=5.0)])
    remaining = store.erased((0.0, 0.0, 0.0), 0.5)
    assert len(remaining) == 1
    assert remaining[0].color == (0.1, 0.2, 0.3)
    assert remaining[0].width == 5.0


def test_erasing_nothing_reports_no_change():
    store = AnnotationStore([line_stroke(4)])
    assert store.erased((0.0, 10.0, 0.0), 0.5) is None


def test_a_broken_circle_stays_one_piece():
    """The surviving arc wraps past the start of the list, so the gap is
    rotated to the front rather than cutting the arc into two pieces."""
    angles = np.linspace(0.0, 2.0 * np.pi, 12, endpoint=False)
    stroke = Stroke(
        points=[(float(np.cos(a)), float(np.sin(a)), 0.0) for a in angles],
        normals=[(0.0, 0.0, 1.0)] * len(angles),
        kind=AnnotateMode.CIRCLE,
        closed=True,
    )
    remaining = AnnotationStore([stroke]).erased((-1.0, 0.0, 0.0), 0.4)
    assert remaining is not None
    assert len(remaining) == 1
    assert len(remaining[0].points) == 11
    assert not remaining[0].closed


def test_settings_stamp_the_brush_onto_new_strokes():
    settings = AnnotationSettings(color=(0.2, 0.4, 0.6), width=7.0, mode=AnnotateMode.LINE)
    stroke = settings.new_stroke()
    assert stroke.kind is AnnotateMode.LINE
    assert stroke.color == (0.2, 0.4, 0.6)
    assert stroke.width == pytest.approx(7.0)


def test_each_segment_becomes_six_vertices():
    vertices = build_vertices([line_stroke(4)])
    assert vertices.shape == (3 * 6, 14)
    # Every vertex carries its own end and the segment's other end.
    first, second = vertices[0], vertices[1]
    assert np.allclose(first[0:3], [0.0, 0.0, 0.0])
    assert np.allclose(first[3:6], [1.0, 0.0, 0.0])
    assert np.allclose(second[0:3], [1.0, 0.0, 0.0])
    assert np.allclose(second[3:6], [0.0, 0.0, 0.0])
    # The two corners at one end sit on opposite sides of the ribbon.
    assert vertices[0][12] == pytest.approx(1.0)
    assert vertices[5][12] == pytest.approx(-1.0)


def test_a_closed_stroke_gains_the_wrapping_segment():
    stroke = line_stroke(4, closed=True)
    assert build_vertices([stroke]).shape[0] == 4 * 6


def test_strokes_too_short_to_draw_are_skipped():
    assert build_vertices([Stroke(points=[(0.0, 0.0, 0.0)])]).shape == (0, 14)
    assert build_vertices([]).shape == (0, 14)
