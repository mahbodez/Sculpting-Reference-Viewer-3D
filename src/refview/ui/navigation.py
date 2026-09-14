"""Mouse-gesture to camera-motion mapping.

Orbiting pivots on the point where the cursor ray meets the camera-facing
plane through the object centre, and zooming pivots on the point under the
cursor.  Both keep whatever is under the mouse roughly where the user put it,
which is what makes the navigation feel direct.

Holding Shift while orbiting snaps to round angles.  The snapped rotation is
always measured from the pose the drag started in rather than accumulated step
by step, so releasing Shift mid-drag picks the free rotation back up exactly
where it would have been.
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
        #: Multiples of the two rates above, and which way round a drag turns
        #: the model.  Instance attributes rather than arguments to every call
        #: because they are the artist's standing answer and not something a
        #: gesture decides; the window writes them from the preferences.  See
        #: :class:`refview.core.preferences.NavigationPreferences`.
        self.orbit_speed = 1.0
        self.zoom_speed = 1.0
        self.invert_orbit_x = False
        self.invert_orbit_y = False
        self._mode = DragMode.NONE
        self._last: tuple[float, float] | None = None
        self._pivot: np.ndarray | None = None
        self._origin: tuple[float, float] | None = None
        self._start: Camera | None = None
        self._snapped: tuple[float, float] | None = None

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
        self._origin = (x, y)
        # The camera starts the drag at zero rotation from its own pose, which
        # is a snapped state already: a Shift-drag that has not yet reached the
        # first increment then has nothing to do.
        self._snapped = (0.0, 0.0)
        if mode is DragMode.ORBIT:
            self._pivot = camera.plane_point_under_cursor(x, y, width, height, scene_center)
            self._start = camera.copy()
        else:
            self._pivot = None
            self._start = None

    def drag(
        self,
        x: float,
        y: float,
        camera: Camera,
        width: int,
        height: int,
        snap_degrees: float = 0.0,
    ) -> bool:
        """Apply the motion since the previous event.  Returns ``True`` if moved."""
        if self._mode is DragMode.NONE or self._last is None:
            return False
        if self._mode is DragMode.ORBIT and snap_degrees > 0.0:
            return self._snap(x, y, camera, snap_degrees)

        dx, dy = x - self._last[0], y - self._last[1]
        self._last = (x, y)
        if dx == 0.0 and dy == 0.0:
            return False

        if self._mode is DragMode.ORBIT:
            yaw = math.radians(-dx * self._orbit_x)
            pitch = math.radians(-dy * self._orbit_y)
            camera.orbit(yaw, pitch, self._pivot)
            self._snapped = None  # Free motion; the next snap must reapply.
        else:
            camera.pan(dx, dy, height)
        return True

    def _snap(self, x: float, y: float, camera: Camera, step: float) -> bool:
        """Orbit in whole increments of ``step`` degrees from the drag's start."""
        if self._start is None or self._origin is None:
            return False
        travel_x = (x - self._origin[0]) * self._orbit_x
        travel_y = (y - self._origin[1]) * self._orbit_y
        angles = (-round(travel_x / step) * step, -round(travel_y / step) * step)
        self._last = (x, y)
        if angles == self._snapped:
            return False
        self._snapped = angles
        camera.apply(self._start)
        camera.orbit(math.radians(angles[0]), math.radians(angles[1]), self._pivot)
        return True

    def end(self) -> None:
        self._mode = DragMode.NONE
        self._last = None
        self._pivot = None
        self._origin = None
        self._start = None
        self._snapped = None

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
        camera.zoom(self._zoom_per_notch ** -notches, pivot)

    # -- what the preferences set ---------------------------------------

    @property
    def _orbit_x(self) -> float:
        """Degrees of yaw per pixel, signed by whether the drag is inverted."""
        rate = self.ORBIT_DEGREES_PER_PIXEL * self.orbit_speed
        return -rate if self.invert_orbit_x else rate

    @property
    def _orbit_y(self) -> float:
        rate = self.ORBIT_DEGREES_PER_PIXEL * self.orbit_speed
        return -rate if self.invert_orbit_y else rate

    @property
    def _zoom_per_notch(self) -> float:
        """The per-notch multiplier, scaled about 1 rather than multiplied.

        Zoom is geometric: a notch multiplies the distance, so twice the speed
        has to mean twice the *exponent* and not twice the factor.  Scaling the
        step away from 1 is the same thing said in one line, and it keeps the
        rate continuous through the shipped setting rather than jumping at it.
        """
        return 1.0 + (self.ZOOM_PER_NOTCH - 1.0) * self.zoom_speed
