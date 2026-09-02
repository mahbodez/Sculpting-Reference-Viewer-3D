"""Mouse gestures driving the camera, including Shift-snapped orbiting."""

from __future__ import annotations

import math

import numpy as np
import pytest

from refview.core.camera import Camera
from refview.ui.navigation import DragMode, NavigationController

#: Pixels of travel that add up to one degree of free orbit.
_PIXELS_PER_DEGREE = 1.0 / NavigationController.ORBIT_DEGREES_PER_PIXEL


def _azimuth(camera: Camera) -> float:
    """Compass angle of the camera around the object, in degrees."""
    return math.degrees(math.atan2(camera.eye[0], camera.eye[2]))


def _start(camera: Camera) -> NavigationController:
    controller = NavigationController()
    # Press in the middle of the widget, so the orbit pivot is the target and
    # the applied yaw shows up directly as a change in azimuth.
    controller.begin(DragMode.ORBIT, 400, 300, camera, 800, 600, np.zeros(3))
    return controller


def test_a_free_orbit_follows_the_mouse_exactly():
    camera = Camera()
    controller = _start(camera)
    controller.drag(400 + 20 * _PIXELS_PER_DEGREE, 300, camera, 800, 600)
    assert _azimuth(camera) == pytest.approx(-20.0)


def test_snapping_holds_still_until_the_next_step():
    camera = Camera()
    controller = _start(camera)
    moved = controller.drag(400 + 5, 300, camera, 800, 600, snap_degrees=15.0)
    assert not moved
    assert _azimuth(camera) == pytest.approx(0.0)


def test_snapping_lands_on_whole_increments():
    camera = Camera()
    controller = _start(camera)
    for degrees, expected in ((17.0, -15.0), (40.0, -45.0), (72.0, -75.0)):
        controller.drag(400 + degrees * _PIXELS_PER_DEGREE, 300, camera, 800, 600, snap_degrees=15)
        assert _azimuth(camera) == pytest.approx(expected)


def test_the_snap_step_is_configurable():
    camera = Camera()
    controller = _start(camera)
    controller.drag(400 + 13 * _PIXELS_PER_DEGREE, 300, camera, 800, 600, snap_degrees=5.0)
    assert _azimuth(camera) == pytest.approx(-15.0)


def test_releasing_shift_resumes_the_free_orbit_from_there():
    """Snapped angles are measured from the press, so the two modes agree."""
    camera = Camera()
    controller = _start(camera)
    controller.drag(400 + 30 * _PIXELS_PER_DEGREE, 300, camera, 800, 600, snap_degrees=15.0)
    assert _azimuth(camera) == pytest.approx(-30.0)
    controller.drag(400 + 40 * _PIXELS_PER_DEGREE, 300, camera, 800, 600)
    assert _azimuth(camera) == pytest.approx(-40.0)


def test_panning_ignores_the_snap_angle():
    camera = Camera()
    controller = NavigationController()
    controller.begin(DragMode.PAN, 400, 300, camera, 800, 600)
    before = camera.eye.copy()
    controller.drag(410, 300, camera, 800, 600, snap_degrees=15.0)
    assert not np.allclose(camera.eye, before)
