"""Mouse-gesture to camera-motion mapping.

Orbiting pivots on the point where the cursor ray meets the camera-facing
plane through the object centre, and zooming pivots on the point under the
cursor.  Both keep whatever is under the mouse roughly where the user put it,
which is what makes the navigation feel direct.
"""

from __future__ import annotations

import math
from enum import Enum, auto

import numpy as np

from ..core.camera import Camera


class DragMode(Enum):
    NONE = auto()
    ORBIT = auto()
    PAN = auto()


class NavigationController:
    """Tracks an in-progress drag and applies it to a camera."""

    #: Degrees of orbit per pixel of mouse travel.
    ORBIT_DEGREES_PER_PIXEL = 0.35
    #: Multiplier applied per wheel notch.
    ZOOM_PER_NOTCH = 1.15

    def __init__(self) -> None:
        self._mode = DragMode.NONE
        self._last: tuple[float, float] | None = None
        self._pivot: np.ndarray | None = None

    @property
    def mode(self) -> DragMode:
        return self._mode

    @property
    def is_dragging(self) -> bool:
        return self._mode is not DragMode.NONE

    def begin(
        self,
        mode: DragMode,
        x: float,
        y: float,
        camera: Camera,
        width: int,
        height: int,
        scene_center: np.ndarray | None = None,
    ) -> None:
        """Start a drag, resolving the orbit pivot from the cursor position."""
        self._mode = mode
        self._last = (x, y)
        if mode is DragMode.ORBIT:
            self._pivot = camera.plane_point_under_cursor(x, y, width, height, scene_center)
        else:
            self._pivot = None

    def drag(self, x: float, y: float, camera: Camera, width: int, height: int) -> bool:
        """Apply the motion since the previous event.  Returns ``True`` if moved."""
        if self._mode is DragMode.NONE or self._last is None:
            return False
        dx, dy = x - self._last[0], y - self._last[1]
        self._last = (x, y)
        if dx == 0.0 and dy == 0.0:
            return False

        if self._mode is DragMode.ORBIT:
            yaw = math.radians(-dx * self.ORBIT_DEGREES_PER_PIXEL)
            pitch = math.radians(-dy * self.ORBIT_DEGREES_PER_PIXEL)
            camera.orbit(yaw, pitch, self._pivot)
        else:
            camera.pan(dx, dy, height)
        return True

    def end(self) -> None:
        self._mode = DragMode.NONE
        self._last = None
        self._pivot = None

    def zoom(
        self,
        notches: float,
        x: float,
        y: float,
        camera: Camera,
        width: int,
        height: int,
        anchor: np.ndarray | None = None,
    ) -> None:
        """Zoom by wheel notches, keeping the point under the cursor fixed.

        ``anchor`` is the world point to zoom towards; callers pass a surface
        hit when there is one and fall back to the focal plane otherwise.
        """
        if notches == 0.0:
            return
        pivot = (
            camera.plane_point_under_cursor(x, y, width, height)
            if anchor is None
            else np.asarray(anchor, dtype=np.float64)
        )
        camera.zoom(self.ZOOM_PER_NOTCH ** -notches, pivot)
