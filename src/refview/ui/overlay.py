"""2D overlay drawn on top of the GL scene with QPainter.

Measurements are deliberately drawn as screen-space strokes rather than as
geometry: it gives reliable thickness and antialiasing on every driver, keeps
the annotations legible in front of the model, and gets text labels for free.

Surface annotations are the exception -- they are real geometry, drawn by the
scene renderer so the model can hide the ones painted on its far side.  Only
the stroke in progress is previewed here, where it costs nothing.

An armature is drawn here too, and for the opposite reason: it lives *inside*
the form, so geometry the model could hide would be a wire nobody ever saw.
It is drawn over the model instead, and the part standing behind the surface
is dimmed rather than cut away, which says where it is without losing it.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QFontMetricsF, QPainter, QPainterPath, QPen

from ..core.annotation import AnnotateMode, Stroke
from ..core.armature import Armature, ArmatureSettings, BoneLabels
from ..core.camera import Camera
from ..core.measurement import Measurement, MeasurementSettings
from .annotate_tool import AnnotateTool
from .armature_tool import ArmatureTool, Handle
from .measure_tool import MeasureTool
from .state import ViewerState

_AXIS_COLORS = (QColor(226, 92, 92), QColor(126, 200, 108), QColor(96, 152, 228))
_AXIS_LABELS = ("X", "Y", "Z")
_HUD_TEXT = QColor(226, 228, 232)
_HUD_BACKDROP = QColor(16, 17, 20, 190)
_TEXT_HALO = QColor(0, 0, 0, 215)
_PENDING_COLOR = QColor(120, 200, 255)
_HANDLE_OUTLINE = QColor(12, 13, 16, 220)
_HANDLE_HOVER = QColor(255, 255, 255)
_ERASER_COLOR = QColor(255, 120, 120)
_LANDMARK_COLOR = QColor(255, 196, 92)


@dataclass(frozen=True)
class OverlayParts:
    """Which of the things drawn over the model are wanted this time.

    The viewport wants all of them: what is on screen is what the artist is
    working with, and hiding half of it would only be a second set of
    visibility switches to keep in step with the first.

    An export wants to choose.  A clip of a form arriving is usually the form
    and nothing else -- the readout naming a file and a triangle count is
    worth having while you work and is clutter in something you send someone,
    and the armature that told the clay where to go has done its job by the
    time anyone watches.  So the parts are named here and the export says
    which it wants, rather than the document's own visibility flags being
    turned off and back on around the render.
    """

    #: Finished measurements, with their labels and handles.
    measurements: bool = True
    #: The gesture under way: a half-placed measurement, the brush ring, a
    #: stroke being painted.  Never anything during an export, since nothing
    #: is being drawn while one runs -- but it is what the flag means.
    tools: bool = True
    #: The wire standing inside the form, its nodes and its landmarks.
    armature: bool = True
    #: The axis cross in the corner.
    gizmo: bool = True
    #: The readout: model name, triangle count, projection, tool hints.
    readout: bool = True


#: Everything, which is what the viewport itself always asks for.
ALL_PARTS = OverlayParts()


def to_qcolor(color, alpha: float = 1.0) -> QColor:
    """Convert a 0-1 RGB tuple to a QColor."""
    r, g, b = (int(round(max(0.0, min(1.0, c)) * 255)) for c in color)
    return QColor(r, g, b, int(round(alpha * 255)))


def project_visible(camera: Camera, point, width: int, height: int) -> QPointF | None:
    """Project a world point, returning ``None`` when it is behind the camera."""
    point = np.asarray(point, dtype=np.float64)
    if float(np.dot(point - camera.eye, camera.forward)) <= 0.0:
        return None
    x, y, depth = camera.project(point, width, height)
    if not -1.0 <= depth <= 1.0:
        return None
    return QPointF(x, y)


class ViewportOverlay:
    """Draws measurements, tool previews, the orientation gizmo and the readout."""

    MARGIN = 12.0
    GIZMO_RADIUS = 26.0

    def draw(
        self,
        painter: QPainter,
        state: ViewerState,
        tool: MeasureTool,
        annotate: AnnotateTool,
        width: int,
        height: int,
        armature: ArmatureTool | None = None,
        buried: frozenset[Handle] = frozenset(),
        parts: OverlayParts = ALL_PARTS,
    ) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        settings = state.measurement_settings
        if parts.measurements and settings.show_all:
            for index, measurement in enumerate(state.measurements):
                if measurement.visible:
                    self._draw_measurement(
                        painter, state.camera, measurement, index, settings, tool, width, height
                    )
        if parts.tools:
            self._draw_pending(painter, state, tool, width, height)
        if parts.armature and armature is not None:
            self._draw_armature(painter, state, armature, width, height, buried)
        if parts.tools:
            self._draw_annotation(painter, state, annotate, width, height)
        if parts.gizmo:
            self._draw_gizmo(painter, state.camera, width, height)
        if parts.readout:
            self._draw_hud(painter, state, tool, annotate, armature, width, height)

    def draw_caption(self, painter: QPainter, text: str, width: int, height: int) -> None:
        """Burn a line into the bottom of a frame, for an exported clip.

        Which stage of the making this is, and what to set the sliders to in
        order to come back to it.  In the viewport that belongs under the
        scrub handle where it can be read at leisure; in a clip, where there
        is no panel and no handle, it has to be in the picture or it is
        nowhere.
        """
        font = QFont(painter.font())
        font.setPointSize(10)
        font.setBold(True)
        metrics = QFontMetricsF(font)
        padding = 9.0
        rect = QRectF(
            self.MARGIN,
            height - self.MARGIN - metrics.height() - padding,
            metrics.horizontalAdvance(text) + padding * 2.0,
            metrics.height() + padding,
        )
        # Bottom right, because bottom left is where the gizmo stands and an
        # export that kept both would have them on top of one another.
        rect.moveLeft(width - self.MARGIN - rect.width())
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(_HUD_BACKDROP)
        painter.drawRoundedRect(rect, 5.0, 5.0)
        self._draw_text(
            painter,
            rect.x() + padding,
            rect.y() + padding * 0.5 + metrics.ascent(),
            text,
            font,
            _HUD_TEXT,
        )

    # ------------------------------------------------------------------
    # Measurements
    # ------------------------------------------------------------------

    def _draw_measurement(
        self,
        painter: QPainter,
        camera: Camera,
        measurement: Measurement,
        index: int,
        settings: MeasurementSettings,
        tool: MeasureTool,
        width: int,
        height: int,
    ) -> None:
        start = project_visible(camera, measurement.endpoint(0), width, height)
        end = project_visible(camera, measurement.endpoint(1), width, height)
        if start is None or end is None:
            return
        color = to_qcolor(measurement.color)
        self._stroke_segment(painter, start, end, color, settings, points=measurement.locked)
        if not measurement.locked:
            active = tool.grabbed_handle or tool.hover_handle
            for handle, position in enumerate((start, end)):
                highlighted = active == (index, handle)
                self._draw_handle(painter, position, color, settings.handle_radius, highlighted)
        if settings.show_labels:
            label = f"{measurement.name}  {settings.format_length(measurement.length)}"
            self._draw_label(painter, (start + end) * 0.5, label, settings.label_size, color)

    def _draw_pending(
        self,
        painter: QPainter,
        state: ViewerState,
        tool: MeasureTool,
        width: int,
        height: int,
    ) -> None:
        if not tool.active:
            return
        settings = state.measurement_settings
        camera = state.camera
        hover = (
            project_visible(camera, tool.hover_point, width, height)
            if tool.hover_point is not None
            else None
        )
        if tool.pending_start is not None:
            start = project_visible(camera, tool.pending_start, width, height)
            if start is not None and hover is not None:
                self._stroke_segment(painter, start, hover, _PENDING_COLOR, settings, dashed=True)
                length = tool.pending_length()
                if length is not None:
                    self._draw_label(
                        painter,
                        (start + hover) * 0.5,
                        settings.format_length(length),
                        settings.label_size,
                        _PENDING_COLOR,
                    )
            elif start is not None:
                self._draw_point(painter, start, _PENDING_COLOR, settings.point_radius)
        if hover is not None:
            self._draw_crosshair(painter, hover, _PENDING_COLOR)

    def _stroke_segment(
        self,
        painter: QPainter,
        start: QPointF,
        end: QPointF,
        color: QColor,
        settings: MeasurementSettings,
        dashed: bool = False,
        points: bool = True,
    ) -> None:
        self._stroke(painter, start, end, color, settings.line_width, dashed)
        if points:
            for point in (start, end):
                self._draw_point(painter, point, color, settings.point_radius)

    def _stroke(
        self,
        painter: QPainter,
        start: QPointF,
        end: QPointF,
        color: QColor,
        width: float,
        dashed: bool = False,
    ) -> None:
        """A line laid over its own dark outline, so it reads against anything."""
        outline = QPen(QColor(0, 0, 0, 150), width + 2.0)
        outline.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(outline)
        painter.drawLine(start, end)

        pen = QPen(color, width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        if dashed:
            pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.drawLine(start, end)

    def _draw_ring(self, painter: QPainter, point: QPointF, color: QColor, radius: float) -> None:
        """An unfilled circle: how thick the form is here, not how big a dot is."""
        painter.setPen(QPen(color, 1.4))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(point, radius, radius)

    def _draw_point(self, painter: QPainter, point: QPointF, color: QColor, radius: float) -> None:
        painter.setPen(QPen(QColor(0, 0, 0, 180), 1.5))
        painter.setBrush(color)
        painter.drawEllipse(point, radius, radius)
        painter.setBrush(Qt.BrushStyle.NoBrush)

    def _draw_handle(
        self,
        painter: QPainter,
        point: QPointF,
        color: QColor,
        radius: float,
        highlighted: bool,
    ) -> None:
        """A square grip, so an editable end reads differently from a fixed one."""
        size = radius + (2.0 if highlighted else 0.0)
        painter.setPen(QPen(_HANDLE_HOVER if highlighted else _HANDLE_OUTLINE, 1.6))
        painter.setBrush(color.lighter(130) if highlighted else color)
        painter.drawRect(QRectF(point.x() - size, point.y() - size, size * 2.0, size * 2.0))
        painter.setBrush(Qt.BrushStyle.NoBrush)

    def _draw_crosshair(self, painter: QPainter, point: QPointF, color: QColor) -> None:
        painter.setPen(QPen(color, 1.5))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(point, 7.0, 7.0)
        painter.drawLine(QPointF(point.x() - 11, point.y()), QPointF(point.x() - 3, point.y()))
        painter.drawLine(QPointF(point.x() + 3, point.y()), QPointF(point.x() + 11, point.y()))
        painter.drawLine(QPointF(point.x(), point.y() - 11), QPointF(point.x(), point.y() - 3))
        painter.drawLine(QPointF(point.x(), point.y() + 3), QPointF(point.x(), point.y() + 11))

    # ------------------------------------------------------------------
    # Armature
    # ------------------------------------------------------------------

    def _draw_armature(
        self,
        painter: QPainter,
        state: ViewerState,
        tool: ArmatureTool,
        width: int,
        height: int,
        buried: frozenset[Handle],
    ) -> None:
        settings = state.armature_settings
        if not settings.show_all:
            return
        for index, armature in enumerate(state.armatures):
            if armature.visible:
                self._draw_wire(painter, state, armature, index, tool, width, height, buried)
        self._draw_guide(painter, state, tool, width, height)

    def _draw_wire(
        self,
        painter: QPainter,
        state: ViewerState,
        armature: Armature,
        index: int,
        tool: ArmatureTool,
        width: int,
        height: int,
        buried: frozenset[Handle],
    ) -> None:
        settings = state.armature_settings
        camera = state.camera
        color = to_qcolor(armature.color)
        faded = to_qcolor(armature.color, settings.buried_alpha)
        screen = [project_visible(camera, node.at, width, height) for node in armature.nodes]

        for position, bone in enumerate(armature.bones):
            if not (0 <= bone.a < len(screen) and 0 <= bone.b < len(screen)):
                continue
            start, end = screen[bone.a], screen[bone.b]
            if start is None or end is None:
                continue
            sunk = (index, bone.a) in buried and (index, bone.b) in buried
            self._stroke(painter, start, end, faded if sunk else color, settings.bone_width)
            if self._labels_bone(settings, tool, (index, position)):
                self._draw_label(
                    painter,
                    (start + end) * 0.5,
                    state.measurement_settings.format_length(armature.bone_length(bone)),
                    state.measurement_settings.label_size,
                    color,
                )

        active = tool.grabbed_handle or tool.hover_handle
        for position, node in enumerate(armature.nodes):
            at = screen[position]
            if at is None:
                continue
            here = faded if (index, position) in buried else color
            if settings.show_sizes and node.size > 0.0:
                radius = self._pixel_radius(camera, node, width, height, settings)
                self._draw_ring(painter, at, here, radius)
            if node.locked:
                self._draw_point(painter, at, here, settings.node_radius)
            else:
                chosen = tool.selected == (index, position)
                self._draw_handle(
                    painter,
                    at,
                    here,
                    settings.handle_radius,
                    active == (index, position) or chosen,
                )
            if settings.show_names:
                self._draw_label(
                    painter, at, node.name, state.measurement_settings.label_size, here
                )

    def _labels_bone(self, settings: ArmatureSettings, tool: ArmatureTool, bone: Handle) -> bool:
        if settings.labels is BoneLabels.ALWAYS:
            return True
        return settings.labels is BoneLabels.HOVER and tool.hover_bone == bone

    def _pixel_radius(
        self,
        camera: Camera,
        node,
        width: int,
        height: int,
        settings: ArmatureSettings,
    ) -> float:
        """A world radius in pixels, measured rather than converted.

        Projecting the node and a point one radius to its right and taking the
        distance between them gets the answer right under both projections,
        without the overlay needing to know which one is in force.
        """
        at = project_visible(camera, node.at, width, height)
        edge = project_visible(camera, node.point + camera.right * node.size, width, height)
        if at is None or edge is None:
            return settings.node_radius
        span = float(np.hypot(edge.x() - at.x(), edge.y() - at.y()))
        return max(span, settings.node_radius)

    def _draw_guide(
        self,
        painter: QPainter,
        state: ViewerState,
        tool: ArmatureTool,
        width: int,
        height: int,
    ) -> None:
        """The landmarks of a guided run, and the point about to be placed."""
        settings = state.armature_settings
        camera = state.camera
        if settings.show_landmarks:
            # A cross being dragged or merely pointed at is ringed like the one
            # the panel is editing: a landmark that can be taken hold of has to
            # look as grabbable as a node handle does.
            active = tool.grabbed_landmark or tool.hover_landmark
            for index, armature in enumerate(state.armatures):
                if not armature.visible:
                    continue
                for landmark in armature.landmarks:
                    at = project_visible(camera, landmark.at, width, height)
                    if at is None:
                        continue
                    here = (index, landmark.key)
                    self._draw_cross(painter, at, _LANDMARK_COLOR, landmark.mirrored)
                    if tool.selected_landmark == here:
                        self._draw_ring(painter, at, _PENDING_COLOR, 9.0)
                    elif active == here:
                        self._draw_ring(painter, at, _HANDLE_HOVER, 8.0)
        if tool.active and tool.hover_point is not None:
            hover = project_visible(camera, tool.hover_point, width, height)
            if hover is not None:
                self._draw_crosshair(painter, hover, _PENDING_COLOR)

    def _draw_cross(self, painter: QPainter, point: QPointF, color: QColor, hollow: bool) -> None:
        """A small cross for a landmark; hollow when the mirror guessed it."""
        for pen in (QPen(QColor(0, 0, 0, 170), 3.0), QPen(color, 1.6)):
            painter.setPen(pen)
            painter.drawLine(
                QPointF(point.x() - 5.0, point.y() - 5.0),
                QPointF(point.x() + 5.0, point.y() + 5.0),
            )
            painter.drawLine(
                QPointF(point.x() - 5.0, point.y() + 5.0),
                QPointF(point.x() + 5.0, point.y() - 5.0),
            )
        if not hollow:
            self._draw_point(painter, point, color, 2.4)

    # ------------------------------------------------------------------
    # Annotations in progress
    # ------------------------------------------------------------------

    def _draw_annotation(
        self,
        painter: QPainter,
        state: ViewerState,
        annotate: AnnotateTool,
        width: int,
        height: int,
    ) -> None:
        """Preview the gesture under way; finished strokes are drawn in 3D."""
        if not annotate.active:
            return
        settings = state.annotation_settings
        color = to_qcolor(settings.color)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        if settings.mode is AnnotateMode.FREEHAND:
            for stroke in annotate.current_strokes:
                self._draw_stroke_preview(
                    painter, state.camera, stroke, color, settings.width, width, height
                )
        elif annotate.is_drawing and annotate.origin and annotate.cursor:
            pen = QPen(color, max(settings.width, 1.0))
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            origin = QPointF(*annotate.origin)
            cursor = QPointF(*annotate.cursor)
            if settings.mode is AnnotateMode.LINE:
                painter.drawLine(origin, cursor)
            else:
                radius = float(np.hypot(cursor.x() - origin.x(), cursor.y() - origin.y()))
                painter.drawEllipse(origin, radius, radius)

        if annotate.cursor is not None:
            self._draw_brush(painter, QPointF(*annotate.cursor), settings, color)

    def _draw_stroke_preview(
        self,
        painter: QPainter,
        camera: Camera,
        stroke: Stroke | None,
        color: QColor,
        line_width: float,
        width: int,
        height: int,
    ) -> None:
        if stroke is None or not stroke.is_drawable:
            return
        pen = QPen(color, max(line_width, 1.0))
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        path = QPainterPath()
        started = False
        for point in stroke.points:
            projected = project_visible(camera, point, width, height)
            if projected is None:
                continue
            if started:
                path.lineTo(projected)
            else:
                path.moveTo(projected)
                started = True
        painter.drawPath(path)

    def _draw_brush(self, painter: QPainter, point: QPointF, settings, color: QColor) -> None:
        """The cursor ring: the eraser's reach, or the width of the brush."""
        if settings.mode.is_eraser:
            painter.setPen(QPen(_ERASER_COLOR, 1.4, Qt.PenStyle.DashLine))
            radius = settings.erase_radius
        else:
            painter.setPen(QPen(color, 1.2))
            radius = max(settings.width * 0.5, 2.0)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(point, radius, radius)

    # ------------------------------------------------------------------
    # Text
    # ------------------------------------------------------------------

    def _draw_text(
        self,
        painter: QPainter,
        left: float,
        baseline: float,
        text: str,
        font: QFont,
        color: QColor,
    ) -> None:
        """Draw text as a filled outline rather than as glyphs.

        Qt's OpenGL paint engine renders glyphs through a texture cache, which
        on several drivers comes out thin and washed out over a multisampled
        widget.  Converting to a path routes the text through the same solid
        geometry path as everything else here, and the dark stroke underneath
        keeps it readable over both the model and the background.
        """
        path = QPainterPath()
        path.addText(QPointF(left, baseline), font, text)
        pen = QPen(_TEXT_HALO, 2.6)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        painter.drawPath(path)

    def _draw_label(
        self, painter: QPainter, anchor: QPointF, text: str, size: int, color: QColor
    ) -> None:
        font = QFont(painter.font())
        font.setPointSize(max(size, 6))
        font.setBold(True)
        metrics = QFontMetricsF(font)
        width = metrics.horizontalAdvance(text)
        padding = 6.0
        rect = QRectF(
            anchor.x() - width * 0.5 - padding,
            anchor.y() - metrics.height() - 12.0,
            width + padding * 2.0,
            metrics.height() + padding,
        )
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(_HUD_BACKDROP)
        painter.drawRoundedRect(rect, 4.0, 4.0)
        self._draw_text(
            painter,
            rect.x() + padding,
            rect.y() + padding * 0.5 + metrics.ascent(),
            text,
            font,
            color,
        )

    # ------------------------------------------------------------------
    # Chrome
    # ------------------------------------------------------------------

    def _armature_hud(self, state: ViewerState, tool: ArmatureTool) -> list[str]:
        """What the armature tool is waiting for, said in as few lines as it takes."""
        settings = state.armature_settings
        if not tool.guiding or tool.guide is None:
            anchor = "click to chain on" if tool.selected is not None else "click to place a node"
            free = ", free placement" if settings.free_placement else ""
            return [f"Armature: {anchor}{free}  (Shift+drag a node resizes it)"]

        held = tool.guide.armature
        armature = state.armatures[held] if 0 <= held < len(state.armatures) else Armature()
        placed, wanted = tool.progress(armature, settings)
        entry = tool.current(armature, settings)
        if entry is None:
            return [f"Armature: every landmark placed ({placed} of {wanted})"]
        return [f"Landmark {placed + 1} of {wanted}: {entry.title}", entry.hint]

    def _draw_gizmo(self, painter: QPainter, camera: Camera, width: int, height: int) -> None:
        origin = QPointF(
            self.MARGIN + self.GIZMO_RADIUS + 8, height - self.MARGIN - self.GIZMO_RADIUS - 8
        )
        rotation = camera.view_matrix()[:3, :3]
        font = QFont(painter.font())
        font.setPointSize(9)
        font.setBold(True)
        metrics = QFontMetricsF(font)
        for index, color in enumerate(_AXIS_COLORS):
            axis = np.zeros(3)
            axis[index] = 1.0
            view_axis = rotation @ axis
            tip = QPointF(
                origin.x() + float(view_axis[0]) * self.GIZMO_RADIUS,
                origin.y() - float(view_axis[1]) * self.GIZMO_RADIUS,
            )
            faded = QColor(color)
            faded.setAlpha(120 if view_axis[2] < 0 else 240)
            painter.setPen(QPen(faded, 2.0))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawLine(origin, tip)
            label = _AXIS_LABELS[index]
            self._draw_text(
                painter,
                tip.x() - metrics.horizontalAdvance(label) * 0.5,
                tip.y() + metrics.ascent() * 0.5,
                label,
                font,
                faded,
            )

    def _draw_hud(
        self,
        painter: QPainter,
        state: ViewerState,
        tool: MeasureTool,
        annotate: AnnotateTool,
        armature: ArmatureTool | None,
        width: int,
        height: int,
    ) -> None:
        lines = []
        if state.mesh is None:
            lines.append("No model loaded  -  File > Open Model... (Ctrl+O)")
        else:
            lines.append(f"{state.mesh.name}  -  {state.mesh.triangle_count:,} tris")
            projection = state.camera.projection.label
            lines.append(f"{projection}  -  {state.camera.fov_deg:.0f} deg FOV")
            section = state.render.section
            if section.enabled:
                offset = state.measurement_settings.format_length(section.offset)
                axis = section.axis.label.split(" ")[0]
                lines.append(f"Section: {section.mode.label.lower()} {axis} at {offset}")
        if tool.active:
            hint = "click the second point" if tool.has_pending else "click the first point"
            if state.measurement_settings.free_placement:
                hint += ", free placement"
            lines.append(f"Measure: {hint}  (Esc cancels)")
        if annotate.active:
            mode = state.annotation_settings.mode
            action = "drag to erase" if mode.is_eraser else "drag to draw"
            lines.append(f"{mode.label}: {action}  (Alt+drag orbits)")
        if armature is not None and armature.active:
            lines.extend(self._armature_hud(state, armature))

        font = QFont(painter.font())
        font.setPointSize(10)
        font.setBold(True)
        metrics = QFontMetricsF(font)
        line_height = metrics.height()
        text_width = max(metrics.horizontalAdvance(line) for line in lines)
        padding = 9.0
        rect = QRectF(
            self.MARGIN,
            self.MARGIN,
            text_width + padding * 2.0,
            line_height * len(lines) + padding,
        )
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(_HUD_BACKDROP)
        painter.drawRoundedRect(rect, 5.0, 5.0)
        for index, line in enumerate(lines):
            self._draw_text(
                painter,
                rect.x() + padding,
                rect.y() + padding * 0.5 + metrics.ascent() + index * line_height,
                line,
                font,
                _HUD_TEXT,
            )
