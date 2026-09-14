"""A screen-space rail for sliding the cutting plane along its normal.

The rail stands at the right edge of the viewport rather than in the scene:
the plane's own position in the scene is already shown by the cut, and a rail
projected beside it fell over the model from half the angles it was looked at
from.  What is drawn is the same cue the depth gesture uses -- a fading rail,
a marker that travels along it, a label -- so the two controls read alike.
"""

from __future__ import annotations

import numpy as np
from PySide6.QtGui import QColor

from ..core.section import OFFSET_SPAN
from .markers import draw_rail

#: Distance of the rail from the right edge, and the reach of a grab.
_INSET = 30.0
_GRAB = 14.0


class SectionGizmo:
    def __init__(self):
        self.drag = None
        self.hover = False

    def _rail(self, picker, settings):
        """Centre, half-length and offset span of the rail, or ``None``."""
        if not settings.enabled:
            return None
        half = float(np.clip(picker.height * 0.2, 60.0, 140.0))
        span = max(float(picker.camera.scene_radius), 1e-6) * OFFSET_SPAN
        centre = np.array([picker.width - _INSET, picker.height * 0.5])
        return centre, half, span

    def geometry(self, picker, settings):
        """Handle position, drag axis in pixels per scene unit, and its direction."""
        rail = self._rail(picker, settings)
        if rail is None:
            return None
        centre, half, span = rail
        direction = np.array([0.0, -1.0])
        axis = direction * (half / span)
        handle = centre + axis * float(np.clip(settings.offset, -span, span))
        return handle, axis, direction

    def hit(self, x, y, picker, settings):
        """Whether ``(x, y)`` lands on the rail or its handle."""
        rail = self._rail(picker, settings)
        if rail is None:
            return False
        centre, half, _ = rail
        handle = self.geometry(picker, settings)[0]
        if np.linalg.norm(handle - (x, y)) <= _GRAB:
            return True
        return abs(x - centre[0]) <= _GRAB * 0.6 and abs(y - centre[1]) <= half

    def begin(self, x, y, picker, settings):
        if not self.hit(x, y, picker, settings):
            return False
        _, axis, _ = self.geometry(picker, settings)
        _, _, span = self._rail(picker, settings)
        self.drag = (np.array([x, y], dtype=np.float64), settings.offset, axis, span)
        return True

    def move(self, x, y):
        origin, offset, axis, span = self.drag
        travelled = float((np.array([x, y]) - origin) @ axis / (axis @ axis))
        return float(np.clip(offset + travelled, -span, span))

    def draw(self, painter, picker, settings):
        rail = self._rail(picker, settings)
        if rail is None:
            return
        centre, half, span = rail
        color = QColor.fromRgbF(*settings.contour_color)
        travel = float(np.clip(settings.offset, -span, span)) * half / span
        label = f"Cut {settings.offset:+.3g}" if self.drag or self.hover else "Cut"
        draw_rail(
            painter, centre[0], centre[1], half, color, travel, label, picker.width,
            centre_tick=True,
        )
