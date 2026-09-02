"""Two-click measuring, plus dragging the endpoints of an unlocked measurement."""

from __future__ import annotations

import numpy as np

from ..core.measurement import Measurement, MeasurementSettings
from .picking import SurfacePicker

#: A measurement endpoint, as ``(index in the store, 0 for start or 1 for end)``.
Handle = tuple[int, int]


class MeasureTool:
    """Picks points and turns pairs of them into measurements.

    The tool stays armed after completing a measurement so several can be
    taken in a row; Escape clears any half-finished one.  Endpoint editing is
    separate: an unlocked measurement can be adjusted whether or not the tool
    is armed, which is what makes the lock in the list worth having.
    """

    def __init__(self) -> None:
        self.active = False
        self.pending_start: np.ndarray | None = None
        self.hover_point: np.ndarray | None = None
        #: Handle under the cursor, highlighted so it looks grabbable.
        self.hover_handle: Handle | None = None
        #: Handle currently being dragged.
        self.grabbed_handle: Handle | None = None

    # -- state ----------------------------------------------------------

    def set_active(self, active: bool) -> None:
        self.active = active
        if not active:
            self.cancel()

    def cancel(self) -> None:
        """Drop the half-finished measurement and the hover preview."""
        self.pending_start = None
        self.hover_point = None

    @property
    def has_pending(self) -> bool:
        return self.pending_start is not None

    # -- picking --------------------------------------------------------

    def pick(
        self,
        x: float,
        y: float,
        picker: SurfacePicker,
        settings: MeasurementSettings,
    ) -> np.ndarray | None:
        """Where a click at ``(x, y)`` would put a point.

        With free placement the point lands on the camera-facing plane through
        the object centre, so measurements are not confined to the surface;
        otherwise it must hit the model and may snap to the nearest vertex.
        """
        if settings.free_placement:
            return picker.plane_point(x, y, picker.camera.scene_center)
        return picker.point(x, y, snap=settings.snap_to_vertex, snap_pixels=settings.snap_pixels)

    def drag_target(
        self,
        x: float,
        y: float,
        picker: SurfacePicker,
        settings: MeasurementSettings,
        current: np.ndarray,
    ) -> np.ndarray:
        """Where a grabbed endpoint should move to.

        Free placement -- and a drag that wanders off the model -- slides the
        point across the plane it already sits on, so it never jumps to a
        surface the artist did not aim at.
        """
        if not settings.free_placement:
            point = picker.point(
                x, y, snap=settings.snap_to_vertex, snap_pixels=settings.snap_pixels
            )
            if point is not None:
                return point
        return picker.plane_point(x, y, current)

    # -- endpoint handles -----------------------------------------------

    def handle_at(
        self,
        x: float,
        y: float,
        measurements,
        picker: SurfacePicker,
        settings: MeasurementSettings,
    ) -> Handle | None:
        """The nearest grabbable endpoint under the cursor, if any.

        Only unlocked, visible measurements offer handles; everything else is
        inert, so orbiting near a measurement never disturbs it.
        """
        if not settings.show_all:
            return None
        radius = settings.handle_radius + 4.0
        best: Handle | None = None
        best_distance = radius
        for index, measurement in enumerate(measurements):
            if measurement.locked or not measurement.visible:
                continue
            for handle in (0, 1):
                distance = picker.screen_distance(measurement.endpoint(handle), x, y)
                if distance is not None and distance <= best_distance:
                    best, best_distance = (index, handle), distance
        return best

    # -- gesture --------------------------------------------------------

    def click(self, point: np.ndarray, name: str | None = None) -> Measurement | None:
        """Consume a picked point; returns a measurement on the second click."""
        if self.pending_start is None:
            self.pending_start = np.asarray(point, dtype=np.float64)
            return None
        start, self.pending_start = self.pending_start, None
        return Measurement(
            start=tuple(float(v) for v in start),
            end=tuple(float(v) for v in np.asarray(point, dtype=np.float64)),
            name=name or "Measurement",
        )

    def pending_length(self) -> float | None:
        """Length of the rubber band currently being dragged out, if any."""
        if self.pending_start is None or self.hover_point is None:
            return None
        return float(np.linalg.norm(self.hover_point - self.pending_start))
