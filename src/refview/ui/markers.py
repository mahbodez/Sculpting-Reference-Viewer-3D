"""Shared marker appearance, visibility, and constrained depth gestures."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import (
    QColor,
    QFont,
    QFontMetricsF,
    QLinearGradient,
    QPainterPath,
    QPen,
)

from ..core.raycast import raycast_many

TEXT_HALO = QColor(0, 0, 0, 215)
DEPTH_COLOR = QColor(120, 200, 255)


def draw_text(painter, left, baseline, text, font=None, color=None):
    """Draw text as a filled outline rather than as glyphs.

    Qt's OpenGL paint engine renders glyphs through a texture cache, which on
    several drivers comes out thin and washed out over a multisampled widget.
    Converting to a path routes the text through the same solid geometry path
    as everything else drawn over the model, and the dark stroke underneath
    keeps it readable over both the model and the background.
    """
    path = QPainterPath()
    path.addText(QPointF(left, baseline), painter.font() if font is None else font, text)
    pen = QPen(TEXT_HALO, 2.6)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.save()
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawPath(path)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(226, 228, 232) if color is None else color)
    painter.drawPath(path)
    painter.restore()


def draw_rail(painter, x, y, half, color, travel, label, width, centre_tick=False):
    """The screen-space cue for one degree of freedom.

    A vertical rail that fades out at both ends, a marker showing how far
    along it the value has travelled, and a label beside it.  The depth
    gesture and the section slider both draw this, so the two read as the
    same kind of control.
    """
    faded = QColor(color)
    faded.setAlpha(0)
    gradient = QLinearGradient(x, y - half, x, y + half)
    gradient.setColorAt(0, faded)
    gradient.setColorAt(0.5, color)
    gradient.setColorAt(1, faded)
    painter.save()
    painter.setPen(QPen(QColor(0, 0, 0, 140), 5))
    painter.drawLine(QPointF(x, y - half * 0.8), QPointF(x, y + half * 0.8))
    painter.setPen(QPen(gradient, 3))
    painter.drawLine(QPointF(x, y - half), QPointF(x, y + half))
    if centre_tick:
        painter.setPen(QPen(color, 1.5))
        painter.drawLine(QPointF(x - 6, y), QPointF(x + 6, y))
    travel = float(np.clip(travel, -half + 5, half - 5))
    VisualMarker(QPointF(x, y - travel), color, radius=5, highlighted=True).draw(painter)
    font = QFont(painter.font())
    font.setPointSize(9)
    font.setBold(True)
    advance = QFontMetricsF(font).horizontalAdvance(label)
    # Beside the rail, on whichever side has the room for it.
    left = x + 12 if x + 12 + advance <= width - 4 else x - 12 - advance
    pale = QColor(color).lighter(140)
    pale.setAlpha(255)
    draw_text(painter, left, y + 4, label, font, pale)
    painter.restore()


@dataclass
class DepthDrag:
    """A fixed world axis through the grabbed point; upward drags go deeper."""

    anchor: np.ndarray
    direction: np.ndarray
    start_y: float
    scale: float
    delta: float = 0.0

    @classmethod
    def begin(cls, point, y, picker):
        anchor = np.array(point, dtype=np.float64, copy=True)
        depth = float(np.dot(anchor - picker.camera.eye, picker.camera.forward))
        return cls(
            anchor, picker.camera.forward.copy(), y, picker.world_per_pixel(max(depth, 1e-6))
        )

    def target(self, y):
        self.delta = (self.start_y - y) * self.scale
        return self.anchor + self.direction * self.delta

    #: The grid's cell, in pixels at the depth the drag began, and how many
    #: cells it reaches from the point in each direction.  Wide, because
    #: what it is for is the model's silhouette crossing it: a grid that
    #: stopped short of the form would say nothing about where the form is.
    GRID_STEP = 36.0
    GRID_CELLS = 10

    def grid(self, camera):
        """A grid across the depth axis, at the depth the point has reached.

        Returns ``(segments, centre, reach)``: world-space line segments of
        shape ``(n, 2, 3)`` lying in the plane through the point that faces
        the camera, the point itself, and the grid's half-width in world
        units.  The rail says how far the point has travelled; this, drawn
        into the scene where the model can stand in front of it or behind
        it, says where that has put it.
        """
        centre = self.anchor + self.direction * self.delta
        step = self.scale * self.GRID_STEP
        reach = step * self.GRID_CELLS
        right, up = camera.right, camera.up
        segments = []
        for index in range(-self.GRID_CELLS, self.GRID_CELLS + 1):
            offset = step * index
            segments.append((centre + right * offset - up * reach,
                             centre + right * offset + up * reach))
            segments.append((centre - right * reach + up * offset,
                             centre + right * reach + up * offset))
        return np.asarray(segments, dtype=np.float64), centre, reach

    def draw(self, painter, camera, width, height):
        # Draw the projected world axis when perspective gives it a visible
        # length. The adjacent ruler below also works for an end-on axis.
        span = self.scale * 70
        a = self.anchor - self.direction * span
        b = self.anchor + self.direction * span
        start = QPointF(*camera.project(a, width, height)[:2])
        end = QPointF(*camera.project(b, width, height)[:2])
        if (end - start).manhattanLength() > 8:
            faded = QColor(DEPTH_COLOR)
            faded.setAlpha(0)
            gradient = QLinearGradient(start, end)
            gradient.setColorAt(0, faded)
            gradient.setColorAt(0.5, QColor(120, 200, 255, 220))
            gradient.setColorAt(1, faded)
            painter.save()
            painter.setPen(QPen(gradient, 2))
            painter.drawLine(start, end)
            painter.restore()
        # A view-normal line projects to a point in orthographic views. Show a
        # screen-space ruler beside that point, with the actual signed travel.
        x, y, _ = camera.project(self.anchor, width, height)
        x = min(max(x + 28, 35), width - 35)
        y = min(max(y, 85), height - 85)
        travel = self.delta / max(self.scale, 1e-9)
        draw_rail(painter, x, y, 70, DEPTH_COLOR, travel, f"Depth {self.delta:+.3g}", width)

@dataclass
class VisualMarker:
    """One marker object for endpoints, nodes, landmarks and tool previews."""

    point: QPointF
    color: QColor
    radius: float = 5.0
    shape: str = "circle"
    highlighted: bool = False
    hollow: bool = False
    buried: bool = False

    def draw(self, painter):
        painter.save()
        p = self.point
        r = self.radius + (2 if self.highlighted else 0)
        color = QColor(self.color)
        if self.buried:
            color.setAlphaF(color.alphaF() * 0.55)
        else:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(0, 0, 0, 90))
            painter.drawEllipse(p + QPointF(2, 3), r + 2, r + 1)
        pen = QPen(QColor("white") if self.highlighted else QColor(10, 12, 16, 230), 1.6)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush if self.hollow else color)
        if self.shape == "square":
            painter.drawRect(QRectF(p.x() - r, p.y() - r, r * 2, r * 2))
        elif self.shape == "cross":
            for stroke in (QPen(QColor(0, 0, 0, 210), 3.5), QPen(color, 1.7)):
                painter.setPen(stroke)
                painter.drawLine(p + QPointF(-r, -r), p + QPointF(r, r))
                painter.drawLine(p + QPointF(-r, r), p + QPointF(r, -r))
            if not self.hollow:
                painter.setBrush(color)
                painter.drawEllipse(p, 2, 2)
        else:
            painter.drawEllipse(p, r, r)
        if self.buried:
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor(225, 235, 255, 210), 1.3, Qt.PenStyle.DashLine))
            painter.drawEllipse(p, r + 4, r + 4)
        painter.restore()


class MarkerVisibility:
    """Cache surface occlusion by view and position for every kind of marker."""

    def __init__(self):
        self._view = None
        self._cache = {}

    def prepare(self, picker, section):
        camera = picker.camera
        key = (
            id(picker.mesh),
            tuple(camera.eye),
            tuple(camera.target),
            tuple(camera.up),
            camera.projection,
            camera.fov_deg,
            camera.scene_radius,
            picker.width,
            picker.height,
            repr(section),
            camera.world_units_per_pixel(max(picker.height, 1)),
        )
        if key != self._view:
            self._view = key
            self._cache.clear()
        self.picker = picker
        self.section = section

    def buried(self, point):
        key = tuple(float(v) for v in point)
        if key not in self._cache:
            self.prefetch([key])
        return self._cache[key]

    def prefetch(self, points) -> None:
        """Answer for a batch of points at once, ahead of being asked one by one.

        Every point still unanswered gets its ray cast in the same pass, so
        the overlay pays the price of one occlusion test for a whole wire of
        nodes rather than once per node on every frame of an orbit.
        """
        wanted = dict.fromkeys(tuple(float(v) for v in point) for point in points)
        missing = [key for key in wanted if key not in self._cache]
        if not missing:
            return
        picker = self.picker
        camera = picker.camera
        if len(self._cache) + len(missing) > 4096:
            self._cache.clear()
        if picker.mesh is None:
            self._cache.update(dict.fromkeys(missing, False))
            return
        targets = np.array(missing, dtype=np.float64)
        xs, ys, _ = camera.project_many(targets, picker.width, picker.height)
        origins, directions = camera.rays(xs, ys, picker.width, picker.height)
        hits = raycast_many(origins, directions, picker.mesh)
        planes = self.section.planes()
        forward = camera.forward
        tolerance = max(camera.scene_radius * 1e-4, 1e-7)
        for key, target, hit in zip(missing, targets, hits, strict=True):
            sunk = False
            if hit is not None:
                clipped = any(plane.distances(hit.point) > 0 for plane in planes)
                depth = np.dot(target - hit.point, forward)
                sunk = not clipped and depth > tolerance
            self._cache[key] = bool(sunk)
