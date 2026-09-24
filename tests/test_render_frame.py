"""The render frame: sizes, the frame in the view, and the camera that fills it."""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.camera import Camera, Projection
from refview.core.path_trace import OutputSettings
from refview.core.render_frame import (
    CUSTOM_SIZE,
    SIZE_MAX,
    SIZE_MIN,
    frame_rect,
    framed_camera,
    memory_estimate,
    output_size,
    safe_rect,
)


def test_output_size_reads_presets_the_viewport_and_the_scale():
    out = OutputSettings(size_preset="HD 720p", width=5, height=5)
    assert output_size(out, (800, 600)) == (1280, 720)
    out.size_preset = "Viewport size"
    assert output_size(out, (800, 600)) == (800, 600)
    out.size_preset = CUSTOM_SIZE
    out.width, out.height = 1000, 500
    out.scale = 50
    assert output_size(out, (800, 600)) == (500, 250)
    out.scale = 10
    out.width = out.height = 20
    assert output_size(out, (800, 600)) == (SIZE_MIN, SIZE_MIN)
    out.scale = 200
    out.width = 7000
    assert output_size(out, (800, 600))[0] == SIZE_MAX


def test_an_unknown_preset_name_uses_the_typed_size():
    out = OutputSettings(size_preset="Something removed", width=640, height=480)
    assert output_size(out, (800, 600)) == (640, 480)


@pytest.mark.parametrize(
    ("view", "size", "expected"),
    [
        ((1000, 500), (1000, 500), (0.0, 0.0, 1000.0, 500.0)),
        # A wide frame in a squarer view is letterboxed.
        ((800, 800), (1600, 800), (0.0, 200.0, 800.0, 400.0)),
        # A tall frame is pillarboxed.
        ((800, 400), (400, 400), (200.0, 0.0, 400.0, 400.0)),
    ],
)
def test_frame_rect_fits_and_centres(view, size, expected):
    assert frame_rect(*view, *size) == pytest.approx(expected)


def test_safe_rect_insets_evenly():
    x, y, w, h = safe_rect((100.0, 50.0, 200.0, 100.0), 0.9)
    assert (w, h) == pytest.approx((180.0, 90.0))
    assert (x + w / 2, y + h / 2) == pytest.approx((200.0, 100.0))
    assert safe_rect((0, 0, 10, 10), 2.0) == pytest.approx((0, 0, 10, 10))


def _corner_hits_corner(camera, view, size):
    """The world point at the frame's corner in the view lands on the render's corner."""
    vw, vh = view
    x, y, w, h = frame_rect(vw, vh, *size)
    origin, direction = camera.ray(x, y, vw, vh)
    point = origin + direction * camera.distance
    framed = framed_camera(camera, vw, vh, *size)
    px, py, _ = framed.project(point, *size)
    return px, py


@pytest.mark.parametrize("projection", [Projection.PERSPECTIVE, Projection.ORTHOGRAPHIC])
@pytest.mark.parametrize("size", [(1600, 800), (400, 800), (800, 600)])
def test_framed_camera_sees_exactly_the_frame(projection, size):
    camera = Camera(eye=np.array([0.3, 1.0, 4.0]), target=np.array([0.0, 0.5, 0.0]),
                    fov_deg=50.0, projection=projection)
    px, py = _corner_hits_corner(camera, (800, 600), size)
    assert px == pytest.approx(0.0, abs=1e-6 * size[0])
    assert py == pytest.approx(0.0, abs=1e-6 * size[1])


def test_framed_camera_leaves_the_view_camera_alone():
    camera = Camera(fov_deg=40.0)
    framed = framed_camera(camera, 800, 800, 1600, 800)
    assert camera.fov_deg == 40.0
    assert framed.fov_deg < 40.0
    assert framed is not camera


def test_memory_estimate_grows_with_size_and_passes():
    small = memory_estimate(100, 100, passes=False)
    assert memory_estimate(200, 100, passes=False) == 2 * small
    assert memory_estimate(100, 100, passes=True) > small
