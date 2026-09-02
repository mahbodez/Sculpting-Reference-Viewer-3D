"""Painting annotations onto the model surface.

Every shape is laid down the same way: sample the gesture in screen space and
raycast each sample onto the model.  A freehand drag samples as it goes, while
a line or a circle is sampled once on release, which is why they can be
rubber-banded in 2D while the mouse is down.  Sampling through the camera is
also what makes the shapes wrap correctly -- a circle drawn over a shoulder
follows the form instead of cutting through it.

A gesture that wanders off the silhouette breaks into several strokes rather
than bridging the gap, so paint never floats in front of the background.
"""

from __future__ import annotations

import math

import numpy as np

from ..core.annotation import AnnotateMode, AnnotationSettings, Stroke
from .picking import SurfacePicker


class AnnotateTool:
    """Turns drags into strokes, and reports what the eraser is touching."""

    #: Cursor travel between freehand samples, in pixels.
    SAMPLE_STEP = 2.5
    #: Spacing of the samples along a line or a circle, in pixels.
    SHAPE_STEP = 4.0
    MAX_SAMPLES = 400

    def __init__(self) -> None:
        self.active = False
        #: Cursor position in widget pixels, kept fresh for the brush preview.
        self.cursor: tuple[float, float] | None = None
        #: Where the current drag started, for the line and circle previews.
        self.origin: tuple[float, float] | None = None
        self._drawing = False
        self._runs: list[Stroke] = []
        self._open: Stroke | None = None
        self._last_sample: tuple[float, float] | None = None

    # -- state ----------------------------------------------------------

    def set_active(self, active: bool) -> None:
        self.active = active
        if not active:
            self.cancel()
            self.cursor = None

    def cancel(self) -> None:
        """Abandon the stroke in progress."""
        self._drawing = False
        self._runs = []
        self._open = None
        self._last_sample = None
        self.origin = None

    @property
    def is_drawing(self) -> bool:
        return self._drawing

    @property
    def current_strokes(self) -> list[Stroke]:
        """The strokes being laid down; the overlay previews them in 2D."""
        return self._runs

    # -- gesture --------------------------------------------------------

    def begin(
        self, x: float, y: float, picker: SurfacePicker, settings: AnnotationSettings
    ) -> bool:
        """Start a drag.  Returns ``False`` when there is nothing to paint on."""
        if not self.active or picker.mesh is None:
            return False
        self.cancel()
        self.origin = (x, y)
        self.cursor = (x, y)
        self._drawing = True
        if settings.mode is AnnotateMode.FREEHAND:
            self._sample(x, y, picker, settings)
        return True

    def drag(
        self, x: float, y: float, picker: SurfacePicker, settings: AnnotationSettings
    ) -> bool:
        """Extend the drag.  Returns ``True`` when the view needs repainting."""
        self.cursor = (x, y)
        if not self._drawing:
            return False
        if settings.mode is AnnotateMode.FREEHAND:
            self._sample(x, y, picker, settings)
        return True

    def finish(self, picker: SurfacePicker, settings: AnnotationSettings) -> list[Stroke]:
        """End the drag and return the strokes it produced."""
        if not self._drawing:
            return []
        if settings.mode is AnnotateMode.LINE:
            self._trace(self._line_samples(), picker, settings, AnnotateMode.LINE)
        elif settings.mode is AnnotateMode.CIRCLE:
            self._trace(self._circle_samples(), picker, settings, AnnotateMode.CIRCLE)
        strokes = [stroke for stroke in self._runs if stroke.is_drawable]
        self.cancel()
        return strokes

    def erase_target(
        self, x: float, y: float, picker: SurfacePicker, settings: AnnotationSettings
    ) -> tuple[np.ndarray, float] | None:
        """Centre and world radius of the eraser, or ``None`` when off the model."""
        hit = picker.hit(x, y)
        if hit is None:
            return None
        return hit.point, picker.world_per_pixel(hit.distance) * settings.erase_radius

    # -- sampling -------------------------------------------------------

    def _sample(
        self, x: float, y: float, picker: SurfacePicker, settings: AnnotationSettings
    ) -> None:
        """Add one freehand point, unless the cursor has barely moved."""
        previous = self._last_sample
        if previous is not None and math.dist(previous, (x, y)) < self.SAMPLE_STEP:
            return
        self._last_sample = (x, y)
        self._extend(picker.hit(x, y), settings, AnnotateMode.FREEHAND)

    def _trace(
        self,
        samples: list[tuple[float, float]],
        picker: SurfacePicker,
        settings: AnnotationSettings,
        kind: AnnotateMode,
    ) -> None:
        """Project screen-space samples onto the surface, breaking at the misses."""
        if len(samples) < 2:
            return
        hits = [picker.hit(x, y) for x, y in samples]
        if kind is AnnotateMode.CIRCLE:
            gaps = [index for index, hit in enumerate(hits) if hit is None]
            if gaps:
                # Rotate a gap to the end of the ring, so an arc that crosses
                # the seam stays one stroke instead of splitting there.
                hits = hits[gaps[0] + 1 :] + hits[: gaps[0] + 1]
        for hit in hits:
            self._extend(hit, settings, kind)
        if kind is AnnotateMode.CIRCLE and len(self._runs) == 1:
            # Unbroken, so the ring can close back onto its first point.
            self._runs[0].closed = len(self._runs[0].points) == len(samples)

    def _extend(self, hit, settings: AnnotationSettings, kind: AnnotateMode) -> None:
        """Continue the open run with a hit, or end it where the ray missed."""
        if hit is None:
            self._open = None
            return
        if self._open is None:
            self._open = settings.new_stroke(kind)
            self._runs.append(self._open)
        self._open.points.append(tuple(float(v) for v in hit.point))
        self._open.normals.append(tuple(float(v) for v in hit.normal))

    def _line_samples(self) -> list[tuple[float, float]]:
        if self.origin is None or self.cursor is None:
            return []
        (x0, y0), (x1, y1) = self.origin, self.cursor
        count = self._sample_count(math.dist(self.origin, self.cursor), minimum=2)
        return [
            (x0 + (x1 - x0) * index / (count - 1), y0 + (y1 - y0) * index / (count - 1))
            for index in range(count)
        ]

    def _circle_samples(self) -> list[tuple[float, float]]:
        if self.origin is None or self.cursor is None:
            return []
        radius = math.dist(self.origin, self.cursor)
        if radius < 2.0:
            return []
        count = self._sample_count(2.0 * math.pi * radius, minimum=24)
        centre_x, centre_y = self.origin
        return [
            (
                centre_x + radius * math.cos(2.0 * math.pi * index / count),
                centre_y + radius * math.sin(2.0 * math.pi * index / count),
            )
            for index in range(count)
        ]

    def _sample_count(self, screen_length: float, minimum: int) -> int:
        return int(min(max(screen_length / self.SHAPE_STEP, minimum), self.MAX_SAMPLES))
