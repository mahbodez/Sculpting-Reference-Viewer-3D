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
is dimmed rather than cut away, which says where it is without losing it.  A
skeleton is drawn the same way, its bones as the tapered lozenges a rigging
application draws so that which end is the joint can be read at a glance.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QFontMetricsF, QPainter, QPainterPath, QPen

from ..core.annotation import AnnotateMode, Stroke
from ..core.armature import Armature, ArmatureSettings, BoneLabels
from ..core.camera import Camera
from ..core.forms import form_spec
from ..core.measurement import Measurement, MeasurementSettings
from ..core.skeleton import Skeleton, SkeletonSettings
from .annotate_tool import AnnotateTool
from .armature_tool import ArmatureTool, Handle
from .form_tool import FormTool
from .markers import MarkerVisibility, VisualMarker, draw_text
from .measure_tool import MeasureTool
from .object_tool import (
    CENTRE_RADIUS,
    HANDLE_RADIUS,
    MODE_LABELS,
    ObjectTool,
)
from .picking import SurfacePicker
from .pose_tool import PoseTool
from .state import ViewerState

_AXIS_COLORS = (QColor(226, 92, 92), QColor(126, 200, 108), QColor(96, 152, 228))
_AXIS_LABELS = ("X", "Y", "Z")
_HUD_TEXT = QColor(226, 228, 232)
_HUD_BACKDROP = QColor(16, 17, 20, 190)
_PENDING_COLOR = QColor(120, 200, 255)
_HANDLE_OUTLINE = QColor(12, 13, 16, 220)
_HANDLE_HOVER = QColor(255, 255, 255)
_ERASER_COLOR = QColor(255, 120, 120)
_LANDMARK_COLOR = QColor(255, 196, 92)
#: A form's landmark, told apart from the armature's by colour: the
#: two kinds can sit on the same bump, and which preset a cross feeds should
#: be readable at a glance.
_FORM_LANDMARK_COLOR = QColor(126, 220, 196)


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
    #: The landmarks the forms were built from.  The clay itself is
    #: geometry and is drawn by the renderer whatever this says.
    forms: bool = True
    #: The skeletons: joints and the bones between them.
    skeleton: bool = True
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


def project_visible_many(camera: Camera, points, width: int, height: int) -> list:
    """Every point of a batch in widget pixels, ``None`` where one is behind the camera."""
    points = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    if len(points) == 0:
        return []
    ahead = (points - camera.eye) @ camera.forward > 0.0
    xs, ys, depth = camera.project_many(points, width, height)
    shown = ahead & (depth >= -1.0) & (depth <= 1.0)
    return [QPointF(x, y) if ok else None for x, y, ok in zip(xs, ys, shown, strict=True)]


class ViewportOverlay:
    """Draws measurements, tool previews, the orientation gizmo and the readout."""

    MARGIN = 12.0
    GIZMO_RADIUS = 26.0

    def __init__(self):
        self._visibility = MarkerVisibility()
        # Where this frame's readout box ended up, so a caption asked to
        # share its corner can sit under it rather than on it.
        self._hud_rect: QRectF | None = None
        #: Each skeleton's joint positions, worked out once per frame and
        #: read by everything in the frame that wants them.
        self._joints: dict[int, np.ndarray] = {}

    @property
    def pending(self) -> bool:
        """Whether the last frame drew from stale occlusion answers."""
        return self._visibility.pending

    @property
    def THROTTLE(self) -> float:  # noqa: N802 - named for the constant it forwards
        return self._visibility.THROTTLE

    def _joint_positions(self, skeleton: Skeleton) -> np.ndarray:
        held = self._joints.get(id(skeleton))
        if held is None:
            held = self._joints[id(skeleton)] = skeleton.positions()
        return held

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
        forms: FormTool | None = None,
        pose: PoseTool | None = None,
        occlude: bool = True,
        objects: ObjectTool | None = None,
    ) -> None:
        """Draw everything over the scene.

        ``occlude`` off skips asking the surface which markers stand behind
        it, and draws them all at full strength.  For the frames of a pose
        drag: the model is re-posed at every one, the test would have to
        index the fresh surface each time, and the wire being pulled is
        what the artist is watching, not its depth.
        """
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)
        self._hud_rect = None
        self._joints = {}

        self._visibility.prepare(SurfacePicker(state.camera, state.mesh, width, height),
                                 state.render.section)
        if occlude:
            self._visibility.prefetch(
                self._marked_points(state, parts, forms is not None, pose is not None)
            )
        else:
            self._visibility.assume_seen(
                self._marked_points(state, parts, forms is not None, pose is not None)
            )
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
        if parts.forms and forms is not None:
            self._draw_forms(painter, state, forms, width, height)
        if parts.skeleton and pose is not None:
            self._draw_skeletons(painter, state, pose, width, height)
        if parts.tools:
            self._draw_annotation(painter, state, annotate, width, height)
        if parts.tools and objects is not None and objects.active:
            self._draw_object_gizmo(painter, state, objects, width, height)
        if parts.gizmo:
            self._draw_gizmo(painter, state.camera, width, height)
        if parts.readout:
            self._draw_hud(
                painter, state, tool, annotate, armature, width, height, forms, pose, objects
            )

    def invalidate_visibility(self) -> None:
        self._visibility = MarkerVisibility()

    def buried_nodes(self, state, width, height):
        self._visibility.prepare(SurfacePicker(state.camera, state.mesh, width, height),
                                 state.render.section)
        self._visibility.prefetch(self._marked_points(state, ALL_PARTS, False))
        return frozenset(
            (index, position)
            for index, armature in enumerate(state.armatures) if armature.visible
            for position, node in enumerate(armature.nodes)
            if self._visibility.buried(node.at)
        )

    def _marked_points(
        self, state: ViewerState, parts: OverlayParts, forms: bool, pose: bool = False
    ) -> list:
        """Every point the frame will ask the surface about, so it is asked once.

        Casting the rays one at a time made a visible wire cost more than
        the model behind it; gathered up they cost one pass.
        """
        points = []
        if parts.measurements and state.measurement_settings.show_all:
            for measurement in state.measurements:
                if measurement.visible:
                    points += [measurement.endpoint(0), measurement.endpoint(1)]
        if parts.armature and state.armature_settings.show_all:
            for armature in state.armatures:
                if armature.visible:
                    points += [node.at for node in armature.nodes]
                    if state.armature_settings.show_landmarks:
                        points += [landmark.at for landmark in armature.landmarks]
        settings = state.form_settings
        if parts.forms and forms and settings.show_all and settings.show_landmarks:
            for form in state.forms:
                if form.visible:
                    points += [landmark.at for landmark in form.landmarks]
        if parts.skeleton and pose and state.skeleton_settings.show_all:
            for skeleton in state.skeletons:
                if skeleton.visible:
                    points += [tuple(at) for at in self._joint_positions(skeleton)]
        return points

    def draw_safe_frame(self, painter: QPainter, width: int, height: int,
                        size: tuple[int, int], settings) -> None:
        """Shade the view outside the render's frame, and draw its safe areas.

        The frame is the render's shape fitted inside the view (see
        :mod:`refview.core.render_frame`); what lies inside it is exactly
        what a render holds.  The action-safe and title-safe guides are the
        broadcast ones: keep what matters inside the first, and anything
        that must not be cut -- text above all -- inside the second.
        """
        from ..core.render_frame import frame_rect, safe_rect

        x, y, w, h = frame_rect(width, height, *size)
        frame = QRectF(x, y, w, h)
        painter.save()
        dim = min(max(float(settings.dim), 0.0), 1.0)
        if dim > 0.0:
            outside = QPainterPath()
            outside.addRect(QRectF(0.0, 0.0, float(width), float(height)))
            inner = QPainterPath()
            inner.addRect(frame)
            painter.fillPath(outside.subtracted(inner), QColor(0, 0, 0, int(round(dim * 255))))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(255, 255, 255, 180), 1.0))
        painter.drawRect(frame.adjusted(0.5, 0.5, -0.5, -0.5))
        dashed = QPen(QColor(255, 255, 255, 110), 1.0, Qt.PenStyle.DashLine)
        painter.setPen(dashed)
        if settings.action_safe:
            painter.drawRect(QRectF(*safe_rect((x, y, w, h), settings.action)))
        if settings.title_safe:
            painter.drawRect(QRectF(*safe_rect((x, y, w, h), settings.title)))
        if settings.label:
            font = QFont(painter.font())
            font.setPointSize(9)
            painter.setFont(font)
            text = f"{size[0]} x {size[1]}"
            metrics = QFontMetricsF(font)
            # Top right, inside the title-safe guide's corner: the readout
            # has the view's top left, and the lines must not cross the words.
            box_w = metrics.horizontalAdvance(text) + 12.0
            box_h = metrics.height() + 6.0
            box = QRectF(frame.right() - box_w - 8.0, frame.top() + 8.0, box_w, box_h)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(_HUD_BACKDROP)
            painter.drawRoundedRect(box, 4.0, 4.0)
            # As outlines, as every word over the model is: the GL engine's
            # glyph cache garbles plain text on some drivers.
            self._draw_text(painter, box.x() + 6.0, box.y() + 3.0 + metrics.ascent(), text,
                            font, _HUD_TEXT)
        painter.restore()

    def draw_caption(
        self,
        painter: QPainter,
        text: str,
        width: int,
        height: int,
        corner: str = "bottom-right",
    ) -> QRectF:
        """A short line in one corner of the frame; returns where it went.

        For an exported clip that is which stage of the making this is, and
        what to set the sliders to in order to come back to it.  In the
        viewport that belongs under the scrub handle where it can be read at
        leisure; in a clip, where there is no panel and no handle, it has to
        be in the picture or it is nowhere.  In the viewport it is the frame
        counter, in whichever corner the artist asked for.

        The default is bottom right because bottom left is where the gizmo
        stands and top left is the readout's; a caption sent to either of
        those is moved along so the two are not on top of one another.
        """
        font = QFont(painter.font())
        font.setPointSize(10)
        font.setBold(True)
        metrics = QFontMetricsF(font)
        padding = 9.0
        rect = QRectF(
            self.MARGIN,
            self.MARGIN,
            metrics.horizontalAdvance(text) + padding * 2.0,
            metrics.height() + padding,
        )
        vertical, _, horizontal = corner.partition("-")
        if horizontal == "right":
            rect.moveLeft(width - self.MARGIN - rect.width())
        elif vertical == "bottom":
            rect.moveLeft(self.MARGIN + self.GIZMO_RADIUS * 2.0 + 24.0)
        if vertical == "bottom":
            rect.moveTop(height - self.MARGIN - rect.height())
        elif horizontal == "left" and self._hud_rect is not None:
            rect.moveTop(self._hud_rect.bottom() + 6.0)
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
        return rect

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
        selected = tool.selected is measurement
        color = _PENDING_COLOR if selected else to_qcolor(measurement.color)
        if selected:
            self._stroke(painter, start, end, QColor(120, 200, 255, 130), settings.line_width + 5)
        self._stroke_segment(painter, start, end, color, settings, points=False)
        if measurement.locked:
            for handle, position in enumerate((start, end)):
                self._draw_point(painter, position, color, settings.point_radius,
                                 self._visibility.buried(measurement.endpoint(handle)))
        if not measurement.locked:
            active = tool.grabbed_handle or tool.hover_handle
            for handle, position in enumerate((start, end)):
                highlighted = selected or active == (index, handle)
                self._draw_handle(painter, position, color, settings.handle_radius, highlighted,
                                  self._visibility.buried(measurement.endpoint(handle)))
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

    def _draw_point(self, painter, point, color, radius, buried=False) -> None:
        VisualMarker(point, color, radius, buried=buried).draw(painter)

    def _draw_handle(self, painter, point, color, radius, highlighted, buried=False) -> None:
        VisualMarker(point, color, radius, "square", highlighted, buried=buried).draw(painter)

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
            sunk = self._visibility.buried(node.at)
            here = color
            if settings.show_sizes and node.size > 0.0:
                radius = self._pixel_radius(camera, node, width, height, settings)
                self._draw_ring(painter, at, here, radius)
            if node.locked:
                self._draw_point(painter, at, here, settings.node_radius, sunk)
            else:
                chosen = tool.selected == (index, position)
                self._draw_handle(
                    painter,
                    at,
                    here,
                    settings.handle_radius,
                    active == (index, position) or chosen,
                    sunk,
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
                    self._draw_cross(painter, at, _LANDMARK_COLOR, landmark.mirrored,
                                     self._visibility.buried(landmark.at))
                    if tool.selected_landmark == here:
                        self._draw_ring(painter, at, _PENDING_COLOR, 9.0)
                    elif active == here:
                        self._draw_ring(painter, at, _HANDLE_HOVER, 8.0)
        if tool.active and tool.hover_point is not None:
            hover = project_visible(camera, tool.hover_point, width, height)
            if hover is not None:
                self._draw_crosshair(painter, hover, _PENDING_COLOR)

    def _draw_cross(self, painter, point, color, hollow, buried=False) -> None:
        VisualMarker(point, color, 5, "cross", hollow=hollow, buried=buried).draw(painter)

    # ------------------------------------------------------------------
    # Skeletons
    # ------------------------------------------------------------------

    def _draw_skeletons(
        self,
        painter: QPainter,
        state: ViewerState,
        tool: PoseTool,
        width: int,
        height: int,
    ) -> None:
        settings = state.skeleton_settings
        if not settings.show_all:
            return
        for index, skeleton in enumerate(state.skeletons):
            if skeleton.visible:
                self._draw_bones(painter, state, skeleton, index, tool, width, height)
        if tool.active and tool.hover_point is not None:
            hover = project_visible(state.camera, tool.hover_point, width, height)
            if hover is not None:
                self._draw_crosshair(painter, hover, _PENDING_COLOR)

    def _draw_bones(
        self,
        painter: QPainter,
        state: ViewerState,
        skeleton: Skeleton,
        index: int,
        tool: PoseTool,
        width: int,
        height: int,
    ) -> None:
        settings = state.skeleton_settings
        camera = state.camera
        color = to_qcolor(skeleton.color)
        faded = to_qcolor(skeleton.color, settings.buried_alpha)
        at = self._joint_positions(skeleton)
        screen = project_visible_many(camera, at, width, height)
        sunk = [self._visibility.buried(point) for point in at]

        held = tool.grabbed or tool.hover_bone
        for parent, child in skeleton.bones():
            start, end = screen[parent], screen[child]
            if start is None or end is None:
                continue
            buried = sunk[parent] and sunk[child]
            lit = held == (index, child) or tool.selected == (index, child)
            self._draw_bone(painter, start, end, faded if buried else color, settings, lit)

        active = tool.grabbed or tool.hover_joint
        for position, joint in enumerate(skeleton.joints):
            point = screen[position]
            if point is None:
                continue
            if settings.show_radii and joint.radius > 0.0:
                self._draw_ring(painter, point, color, self._joint_pixels(
                    camera, at[position], joint.radius, width, height, settings.joint_radius
                ))
            # A buried joint is faded rather than ringed: half a rig's joints
            # stand inside the body at all times, and a dashed ring on every
            # one of them would be the loudest thing on the screen.
            here = faded if sunk[position] else color
            chosen = tool.selected == (index, position)
            lit = active == (index, position) or chosen
            radius = settings.joint_radius if joint.locked else settings.handle_radius
            # One ellipse per joint rather than the marker with its drop
            # shadow: a rig has a hundred of these, drawn at every frame.
            if lit:
                radius += 2.0
            painter.setPen(QPen(_HANDLE_HOVER if lit else _HANDLE_OUTLINE, 1.4))
            painter.setBrush(here)
            painter.drawEllipse(point, radius, radius)
            if chosen:
                self._draw_ring(painter, point, _PENDING_COLOR, settings.handle_radius + 5.0)
            if settings.show_names:
                self._draw_label(
                    painter, point, joint.name, state.measurement_settings.label_size, color
                )

    def _draw_bone(
        self,
        painter: QPainter,
        start: QPointF,
        end: QPointF,
        color: QColor,
        settings: SkeletonSettings,
        lit: bool,
    ) -> None:
        """A bone as a lozenge: wide near the joint it hangs from, tapering to its end.

        The shape says which end is which, which a plain line cannot, and it
        is how every rigging application draws one, so an artist arriving
        from Max or Blender reads it without being told.
        """
        along = end - start
        length = float(np.hypot(along.x(), along.y()))
        if length < 1e-6:
            return
        direction = along / length
        normal = QPointF(-direction.y(), direction.x())
        half = min(settings.bone_width * 1.6, length * 0.12) + (1.5 if lit else 0.0)
        waist = start + direction * min(length * 0.18, 18.0)
        path = QPainterPath(start)
        path.lineTo(waist + normal * half)
        path.lineTo(end)
        path.lineTo(waist - normal * half)
        path.closeSubpath()
        fill = QColor(color)
        fill.setAlphaF(fill.alphaF() * (0.6 if lit else 0.4))
        painter.setPen(QPen(_HANDLE_HOVER if lit else color, 1.4 if lit else 1.1))
        painter.setBrush(fill)
        painter.drawPath(path)

    @staticmethod
    def _joint_pixels(camera, at, radius, width, height, floor) -> float:
        centre = project_visible(camera, at, width, height)
        edge = project_visible(camera, np.asarray(at) + camera.right * radius, width, height)
        if centre is None or edge is None:
            return floor
        return max(float(np.hypot(edge.x() - centre.x(), edge.y() - centre.y())), floor)

    # ------------------------------------------------------------------
    # Forms
    # ------------------------------------------------------------------

    def _draw_forms(
        self,
        painter: QPainter,
        state: ViewerState,
        tool: FormTool,
        width: int,
        height: int,
    ) -> None:
        """The landmarks of the forms, and the point about to be placed.

        The clay itself is real geometry and the renderer draws it; what
        goes over the top is the crosses the artist put down, ringed where
        one is being edited or can be taken hold of, exactly as the armature's
        are.
        """
        settings = state.form_settings
        camera = state.camera
        if not settings.show_all:
            return
        if settings.show_landmarks:
            active = tool.grabbed_landmark or tool.hover_landmark
            for index, form in enumerate(state.forms):
                if not form.visible:
                    continue
                for landmark in form.landmarks:
                    at = project_visible(camera, landmark.at, width, height)
                    if at is None:
                        continue
                    here = (index, landmark.key)
                    self._draw_cross(painter, at, _FORM_LANDMARK_COLOR, landmark.mirrored,
                                     self._visibility.buried(landmark.at))
                    if tool.selected_landmark == here:
                        self._draw_ring(painter, at, _PENDING_COLOR, 9.0)
                    elif active == here:
                        self._draw_ring(painter, at, _HANDLE_HOVER, 8.0)
        if tool.active and tool.hover_point is not None:
            hover = project_visible(camera, tool.hover_point, width, height)
            if hover is not None:
                self._draw_crosshair(painter, hover, _PENDING_COLOR)

    def _forms_hud(self, state: ViewerState, tool: FormTool) -> list[str]:
        """What the forms tool is waiting for, said in as few lines as it takes."""
        run = tool.guide
        if run is None or not 0 <= run.form < len(state.forms):
            return ["Forms: start a form in the Forms panel to place its landmarks"]
        form = state.forms[run.form]
        settings = state.form_settings
        spec = form_spec(form)
        placed, wanted = tool.progress(form, settings)
        entry = tool.current(form, settings)
        if run.freeform:
            if entry is None:
                return [f"{form.name}: {placed} landmarks placed"]
            return [
                f"{form.name}: {placed} placed, next {entry.title}",
                "Click to place it; name it and pick its side in the Forms panel",
            ]
        if entry is None or spec is None:
            return [f"{form.name}: every landmark placed ({placed} of {wanted})"]
        progress = tool.stage_progress(form, settings)
        stage = ""
        if progress is not None and len(spec.stages) > 1:
            index, _, _ = progress
            stage = f" - {spec.stages[index].name.lower()}"
        return [f"{form.name}{stage}: landmark {placed + 1} of {wanted}, {entry.title}", entry.hint]

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
        """Text as filled outlines; see :func:`markers.draw_text` for why."""
        draw_text(painter, left, baseline, text, font, color)

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

    def _pose_hud(self, state: ViewerState, tool: PoseTool) -> list[str]:
        """What the pose tool is waiting for."""
        settings = state.skeleton_settings
        if settings.fit:
            return ["Pose (fit): drag a joint to move it; its children stay put"]
        if tool.selected is not None:
            return ["Pose: drag a joint to swing it, Shift+drag rolls it, click adds a child"]
        return ["Pose: drag a joint to swing the bone above it, click elsewhere to start one"]

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

    def _draw_object_gizmo(
        self, painter: QPainter, state: ViewerState, tool: ObjectTool, width: int, height: int
    ) -> None:
        """The transform handles on the active object: three arms and a ring.

        The arm pointing away from the viewer is drawn paler, as the corner
        gizmo draws its axes, so the depth of the three can be read; the
        handle under the cursor, or in hand, is drawn white.
        """
        active = state.active_object
        if active is None or not state.objects.shown(active, state.object_settings):
            return
        picker = SurfacePicker(state.camera, state.mesh, width, height)
        gizmo = tool.gizmo(picker, state.objects.world_matrix(active))
        if gizmo is None:
            return
        origin = QPointF(*gizmo.origin)
        lit = tool.grabbed or tool.hover_handle
        painter.save()
        for name, color, (tip, towards, _) in zip("xyz", _AXIS_COLORS, gizmo.arms, strict=True):
            faded = QColor(color)
            faded.setAlpha(240 if towards else 130)
            point = QPointF(*tip)
            painter.setPen(QPen(QColor(0, 0, 0, 140), 4.0))
            painter.drawLine(origin, point)
            painter.setPen(QPen(faded, 2.0))
            painter.drawLine(origin, point)
            fill = _HANDLE_HOVER if lit == name else faded
            painter.setPen(QPen(_HANDLE_OUTLINE, 1.5))
            painter.setBrush(fill)
            if tool.mode == "scale":
                half = HANDLE_RADIUS * 0.85
                painter.drawRect(QRectF(point.x() - half, point.y() - half, 2 * half, 2 * half))
            elif tool.mode == "rotate":
                painter.setBrush(Qt.BrushStyle.NoBrush)
                painter.setPen(QPen(fill, 2.5))
                painter.drawEllipse(point, HANDLE_RADIUS, HANDLE_RADIUS)
            else:
                painter.drawEllipse(point, HANDLE_RADIUS, HANDLE_RADIUS)
        ring = _HANDLE_HOVER if lit == "centre" else QColor(236, 238, 242, 220)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor(0, 0, 0, 140), 4.0))
        painter.drawEllipse(origin, CENTRE_RADIUS, CENTRE_RADIUS)
        painter.setPen(QPen(ring, 2.0))
        painter.drawEllipse(origin, CENTRE_RADIUS, CENTRE_RADIUS)
        font = QFont(painter.font())
        font.setPointSize(9)
        font.setBold(True)
        label = f"{MODE_LABELS[tool.mode]}: {active.name}"
        draw_text(painter, origin.x() + CENTRE_RADIUS + 6, origin.y() - CENTRE_RADIUS, label, font)
        painter.restore()

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
        forms: FormTool | None = None,
        pose: PoseTool | None = None,
        objects: ObjectTool | None = None,
    ) -> None:
        lines = []
        if state.mesh is None and len(state.objects):
            count = len(state.objects)
            lines.append(
                f"All {count} objects are hidden  -  tick one in the Model panel"
                if count > 1
                else f"{state.objects[0].name} is hidden  -  tick it in the Model panel"
            )
        elif state.mesh is None:
            lines.append("No model loaded  -  File > Open Model... (Ctrl+O)")
        else:
            shown = len(state.mesh_parts)
            if shown > 1:
                lines.append(
                    f"{shown} of {len(state.objects)} objects  -  "
                    f"{state.mesh.triangle_count:,} tris"
                )
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
        if forms is not None and forms.active:
            lines.extend(self._forms_hud(state, forms))
        if pose is not None and pose.active:
            lines.extend(self._pose_hud(state, pose))
        if objects is not None and objects.active:
            active = state.active_object
            if active is None:
                lines.append("Transform: add a model first")
            else:
                verb = MODE_LABELS[objects.mode].lower()
                lines.append(
                    f"Transform {active.name}: drag a handle to {verb}, the ring to {verb} freely"
                )
                lines.append("W move, E rotate, R scale")
                lines.append("Click another object to make it active  (Alt+drag orbits)")

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
        self._hud_rect = rect
        for index, line in enumerate(lines):
            self._draw_text(
                painter,
                rect.x() + padding,
                rect.y() + padding * 0.5 + metrics.ascent() + index * line_height,
                line,
                font,
                _HUD_TEXT,
            )
