"""Camera behaviour: framing, projection round trips and the navigation gestures."""

from __future__ import annotations

import math

import numpy as np
import pytest

from refview.core.camera import Camera, Projection
from refview.core.mesh import Bounds

WIDTH, HEIGHT = 800, 600


@pytest.fixture
def camera() -> Camera:
    bounds = Bounds(np.array([-1.0, -2.0, -1.0]), np.array([1.0, 2.0, 1.0]))
    cam = Camera()
    cam.frame(bounds)
    return cam


def test_framing_fits_the_bounds(camera):
    half_height = camera.distance * math.tan(math.radians(camera.fov_deg) * 0.5)
    assert half_height > 2.0  # the object's half-height
    assert np.allclose(camera.target, 0.0)


def test_projecting_the_target_lands_in_the_centre(camera):
    x, y, _ = camera.project(camera.target, WIDTH, HEIGHT)
    assert x == pytest.approx(WIDTH / 2, abs=1e-6)
    assert y == pytest.approx(HEIGHT / 2, abs=1e-6)


def test_ray_through_the_centre_points_along_the_view(camera):
    _, direction = camera.ray(WIDTH / 2, HEIGHT / 2, WIDTH, HEIGHT)
    assert np.allclose(direction, camera.forward, atol=1e-9)


@pytest.mark.parametrize("projection", list(Projection))
def test_zoom_keeps_the_anchor_under_the_cursor(camera, projection):
    camera.projection = projection
    anchor = camera.plane_point_under_cursor(620, 180, WIDTH, HEIGHT)
    before = camera.project(anchor, WIDTH, HEIGHT)[:2]
    camera.zoom(0.4, anchor)
    after = camera.project(anchor, WIDTH, HEIGHT)[:2]
    assert np.allclose(before, after, atol=1e-6)


def test_orbit_preserves_the_distance_to_the_pivot(camera):
    pivot = camera.plane_point_under_cursor(500, 250, WIDTH, HEIGHT)
    before = np.linalg.norm(pivot - camera.eye)
    camera.orbit(math.radians(25.0), math.radians(10.0), pivot)
    assert np.linalg.norm(pivot - camera.eye) == pytest.approx(before)


def test_orbit_keeps_the_pivot_under_the_cursor(camera):
    """A drag applies many small steps, and the pivot barely moves on screen.

    It is not pinned exactly: turntable orbiting re-derives the camera's roll
    from the fixed world up so the horizon stays level, and that correction
    shifts the pivot a few pixels over a large rotation.
    """
    pivot = camera.plane_point_under_cursor(500, 250, WIDTH, HEIGHT)
    before = camera.project(pivot, WIDTH, HEIGHT)[:2]
    for _ in range(25):
        camera.orbit(math.radians(1.0), math.radians(0.4), pivot)
    after = camera.project(pivot, WIDTH, HEIGHT)[:2]
    assert np.allclose(before, after, atol=5.0)


def test_orbit_never_flips_over_the_pole(camera):
    for _ in range(200):
        camera.orbit(0.0, math.radians(5.0), camera.target)
    assert abs(float(np.dot(camera.forward, camera.world_up))) < 1.0


def test_pan_moves_eye_and_target_together(camera):
    offset_before = camera.target - camera.eye
    camera.pan(40.0, -25.0, HEIGHT)
    assert np.allclose(camera.target - camera.eye, offset_before)


def test_zoom_is_clamped_to_the_scene_radius(camera):
    for _ in range(200):
        camera.zoom(0.5, camera.target)
    assert camera.distance >= camera.scene_radius * Camera.MIN_DISTANCE_FACTOR * 0.999


def test_orthographic_matches_perspective_framing(camera):
    perspective_extent = camera.ortho_half_height
    camera.projection = Projection.ORTHOGRAPHIC
    assert camera.ortho_half_height == pytest.approx(perspective_extent)
    near, far = camera.clip_planes()
    assert near < 0.0 < far


def test_serialisation_round_trip(camera):
    camera.projection = Projection.ORTHOGRAPHIC
    camera.fov_deg = 27.5
    restored = Camera.from_dict(camera.to_dict())
    assert np.allclose(restored.eye, camera.eye)
    assert np.allclose(restored.target, camera.target)
    assert restored.projection is Projection.ORTHOGRAPHIC
    assert restored.fov_deg == pytest.approx(27.5)
    assert restored.near is None and restored.far is None


def test_clip_planes_set_by_hand_override_the_fit_within_reason(camera):
    fitted = camera.fitted_clip_planes()
    assert camera.clip_planes() == fitted
    camera.near, camera.far = 2.0, 30.0
    assert camera.clip_planes() == (2.0, 30.0)
    # Either one alone; the other stays fitted.
    camera.far = None
    assert camera.clip_planes() == (2.0, fitted[1])
    # A perspective near plane stays in front of the eye, and the far beyond it.
    camera.near, camera.far = -5.0, 1.0
    near, far = camera.clip_planes()
    assert 0.0 < near < 1e-3 and far > near
    camera.near, camera.far = 10.0, 3.0
    near, far = camera.clip_planes()
    assert near == 10.0 and far > 10.0
    # Under an orthographic projection a near plane may sit behind the eye.
    camera.projection = Projection.ORTHOGRAPHIC
    camera.near, camera.far = -4.0, 4.0
    assert camera.clip_planes() == (-4.0, 4.0)
    # The projection follows a change of plane, cache or no cache.
    before = camera.view_projection(1.5).copy()
    camera.far = 8.0
    assert not np.allclose(camera.view_projection(1.5), before)
    # And the settings travel with the camera: saved, copied, and adopted.
    restored = Camera.from_dict(camera.to_dict())
    assert (restored.near, restored.far) == (-4.0, 8.0)
    assert Camera.from_dict({"near": "nonsense", "far": float("inf")}).near is None
    assert Camera.from_dict({"near": "nonsense", "far": float("inf")}).far is None
    copied = camera.copy()
    assert (copied.near, copied.far) == (-4.0, 8.0)
    other = Camera()
    other.apply(camera)
    assert (other.near, other.far) == (-4.0, 8.0)
