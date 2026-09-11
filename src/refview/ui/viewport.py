"""The interactive 3D view.

Navigation is: left-drag orbits about the point under the cursor, right- or
middle-drag pans, and the wheel zooms towards whatever the cursor is over.

The left button does quintuple duty, resolved in this order: a drag with the
annotate tool armed paints; a drag on a landmark's cross moves it, and the wire
derived from it follows; a drag on an unlocked armature node moves it, or
resizes it with Shift held; a drag on the endpoint handle of an unlocked
measurement moves that point; anything else orbits.  A cross is offered before
the node beside it, and within a tighter reach, which is what settles the two
where a preset has put them on top of each other.  With the measuring or
armature tool armed a left *click* -- as opposed to a drag -- places a point, so
those gestures too share the button without fighting the camera.  Holding Alt
always orbits, which is the escape hatch while painting, and holding Shift snaps
an orbit to round angles.
"""

from __future__ import annotations

from dataclasses import astuple, replace

import numpy as np
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QApplication

from ..core.annotation import Stroke
from ..core.armature import ArmatureNode, Buried
from ..core.commands import AddItem, ReplaceItems, SetAttributes
from ..core.history import ANNOTATIONS, ARMATURE, MEASUREMENTS
from ..core.landmarks import landmark_title
from ..core.measurement import Measurement
from ..core.pedestal import build_pedestal
from ..core.plane_film import film_key
from ..core.plane_film import shaded as film_shaded
from ..core.plane_solids import SculptCache
from ..core.section import section_segments
from ..render.mesh_renderer import SceneRenderer
from ..render.stroke_renderer import build_segment_vertices
from .annotate_tool import AnnotateTool
from .armature_tool import ArmatureTool
from .film_recorder import FilmRecorder
from .measure_tool import MeasureTool
from .navigation import DragMode, NavigationController
from .overlay import ViewportOverlay
from .picking import SurfacePicker
from .state import ViewerState


def configure_surface_format() -> None:
    """Request a core-profile context; must run before the QApplication."""
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    fmt.setDepthBufferSize(24)
    fmt.setStencilBufferSize(8)
    fmt.setSamples(4)
    QSurfaceFormat.setDefaultFormat(fmt)


class Viewport(QOpenGLWidget):
    """Renders the scene and turns mouse gestures into camera and tool actions."""

    #: Pixels of travel below which a left-drag counts as a click.
    CLICK_TOLERANCE = 4.0

    measurement_created = Signal(object)
    #: A finished armature edit, as ``(index, nodes, bones, landmarks, text)``.
    #: The tool works out what the edit is; the window records it.
    armature_edited = Signal(object)
    #: A node was clicked, as ``(armature, node)``, or ``None`` for a miss.
    armature_selected = Signal(object)
    #: A landmark was clicked, as ``(armature, key)``, so the panel's list can
    #: follow the cross the artist just pointed at.
    landmark_selected = Signal(object)
    pick_failed = Signal()

    def __init__(self, state: ViewerState, parent=None) -> None:
        super().__init__(parent)
        self._state = state
        self._renderer = SceneRenderer()
        self._navigation = NavigationController()
        self._overlay = ViewportOverlay()
        self.measure_tool = MeasureTool()
        self.annotate_tool = AnnotateTool()
        self.armature_tool = ArmatureTool()
        self._ready = False
        self._press_position: tuple[float, float] | None = None
        self._travel = 0.0
        self._grab_previous: tuple[Measurement, str, tuple] | None = None
        self._node_previous: tuple[ArmatureNode, str, object] | None = None
        #: A landmark drag in progress, as ``(armature index, key, what the
        #: armature held before it started)``.  A landmark is not edited in
        #: place -- moving one re-derives the whole wire -- so the undo step has
        #: to be able to put the lists back, not one attribute of one object.
        self._landmark_previous: tuple[int, str, dict] | None = None
        #: What was selected before the current press, so that clicking a
        #: second node can join the two.
        self._join_from: tuple[int, int] | None = None
        #: Which nodes are standing behind the surface.  Ray-casting a
        #: handful of nodes is cheap, but not cheap enough to repeat on
        #: every frame of an orbit, so the answer is kept until the camera
        #: or the armature moves.
        self._buried: frozenset[tuple[int, int]] = frozenset()
        self._buried_stale = True
        self._erase_previous: list[Stroke] | None = None
        # Signatures of the generated scene geometry, so a light-slider tweak
        # does not re-cut the model or rebuild the pedestal.
        self._pedestal_key: tuple | None = None
        self._section_key: tuple | None = None
        self._sculpt_key: tuple | None = None
        #: Keeps the plane fit and the vertex-to-plane assignment between one
        #: turn of the geometry sliders and the next, so only the part that
        #: actually went stale is worked out again.
        self._sculpt = SculptCache()
        #: Records the whole making of a form, in the background, when the
        #: film is asked for.  Kept here rather than in the panel because it
        #: is the viewport that draws a stage.
        self._film = FilmRecorder(self)
        self._film.grew.connect(self._film_grew)
        self._film.settled.connect(self._film_settled)

        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMinimumSize(320, 240)

        state.mesh_changed.connect(self._upload_mesh)
        state.matcap_changed.connect(self._upload_matcap)
        state.annotations_changed.connect(self._upload_strokes)
        state.render_changed.connect(self._sync_scene)
        state.armature_changed.connect(self._armature_moved)
        state.mesh_changed.connect(self._armature_moved)
        for signal in (state.camera_changed, state.measurements_changed):
            signal.connect(self.update)
        state.camera_changed.connect(self._stale_buried)

    # ------------------------------------------------------------------
    # GL lifecycle
    # ------------------------------------------------------------------

    def initializeGL(self) -> None:  # noqa: N802 - Qt naming
        # Qt destroys and recreates the context on some display changes, so
        # resources are released through the context's own signal.
        self.context().aboutToBeDestroyed.connect(self._release_gl)
        self._renderer.initialize()
        self._ready = True
        self._upload_mesh()
        self._upload_matcap()
        self._upload_strokes()
        self._sync_scene()

    def paintGL(self) -> None:  # noqa: N802 - Qt naming
        painter = QPainter(self)
        painter.beginNativePainting()
        ratio = self.devicePixelRatioF()
        self._renderer.render(
            self._state.camera,
            self._state.render,
            int(self.width() * ratio),
            int(self.height() * ratio),
            ratio,
        )
        painter.endNativePainting()
        self._overlay.draw(
            painter,
            self._state,
            self.measure_tool,
            self.annotate_tool,
            self.width(),
            self.height(),
            self.armature_tool,
            self._buried_nodes(),
        )
        painter.end()

    def _upload_mesh(self) -> None:
        if not self._ready:
            return
        self.makeCurrent()
        self._renderer.set_mesh(self._state.mesh)
        self.doneCurrent()
        self._pedestal_key = self._section_key = self._sculpt_key = None
        self._sculpt.clear()
        self._sync_scene()

    def _upload_matcap(self) -> None:
        if not self._ready:
            return
        self.makeCurrent()
        self._renderer.set_matcap(self._state.matcap_pixels)
        self.doneCurrent()
        self.update()

    def _upload_strokes(self) -> None:
        if not self._ready:
            return
        settings = self._state.annotation_settings
        self.makeCurrent()
        self._renderer.set_strokes(list(self._state.annotations) if settings.visible else [])
        self.doneCurrent()
        self.update()

    def _sync_scene(self) -> None:
        """Regenerate the pedestal and the cut contour when their settings move.

        Both are derived geometry rather than document state, so they are built
        here on demand instead of being kept in the viewer state.
        """
        if self._ready:
            render = self._state.render
            pedestal_key = (id(self._state.mesh), astuple(render.pedestal))
            if pedestal_key != self._pedestal_key:
                self._pedestal_key = pedestal_key
                self._upload_pedestal()
            section_key = (id(self._state.mesh), astuple(render.section))
            if section_key != self._section_key:
                self._section_key = section_key
                self._upload_contour()
            planes = render.planes
            # Only the settings the stand-in is actually built from: the rest
            # of the Planes panel moves the shading, and re-cutting the form
            # for a change of contour colour would be a stall for nothing.
            sculpt_key = (
                id(self._state.mesh),
                planes.sculpts_geometry,
                planes.sculpt,
                planes.sculpt_count,
                planes.sculpt_masses,
                planes.sculpt_relax,
                planes.sculpt_smooth,
                planes.sculpt_median,
                planes.sculpt_median_reach,
                planes.sculpt_fineness,
                planes.sculpt_film,
                planes.sculpt_stage,
                planes.coefficients,
            )
            if sculpt_key != self._sculpt_key:
                self._sculpt_key = sculpt_key
                self._upload_sculpt()
        self.update()

    def _upload_pedestal(self) -> None:
        mesh = self._state.mesh
        settings = self._state.render.pedestal
        disc = None if mesh is None else build_pedestal(mesh.bounds, settings)
        self.makeCurrent()
        self._renderer.set_pedestal(disc)
        self.doneCurrent()

    def stop_recording(self) -> None:
        """End any film being recorded, and wait for its thread to really stop.

        For shutdown only.  Everywhere else a recording is abandoned rather
        than waited for, because waiting is the freeze the thread exists to
        avoid -- but on the way out the alternative is a live thread meeting
        an interpreter that is dismantling itself, which is a crash.
        """
        self._film.wait()

    def _upload_sculpt(self) -> None:
        """Rebuild the planar stand-in and hand it to the renderer.

        Cutting a form into planes takes long enough on a heavy model to be
        felt, so the wait is shown for what it is rather than looking like a
        hang.  The model itself is untouched throughout: picking, measuring,
        painting and the section cut all still read the real surface.

        When the film is asked for, the same work is done a stage at a time on
        a thread instead, and what is drawn is whichever stage the scrub
        handle is on.  The first stage arrives in a fraction of the time the
        finished form would take, so the viewport fills rather than waiting.
        """
        planes = self._state.render.planes
        if self._state.mesh is None or not planes.sculpts_geometry:
            self._film.abandon()
            self._state.recording_changed.emit(False)
            self._show_sculpt(None)
            return
        if not planes.sculpt_film:
            self._film.abandon()
            self._state.recording_changed.emit(False)
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            try:
                proxy = self._sculpt.mesh_for(self._state.mesh, planes)
            finally:
                QApplication.restoreOverrideCursor()
            if proxy is not None:
                self._state.status_message.emit(
                    f"Form rebuilt from {planes.sculpt_count} planes, {planes.sculpt.value}"
                )
            self._show_sculpt(proxy)
            return

        key = film_key(planes, planes.coefficients)
        held = self._film.matching(key)
        if held is not None:
            # The same film the settings already asked for: only the stage
            # being looked at has changed, which is a lookup.
            self._show_stage(held)
            return
        film = self._film.start(
            self._state.mesh, self._sculpt.planes_for(self._state.mesh, planes), planes, key
        )
        self._state.recording_changed.emit(True)
        self._state.status_message.emit(
            f"Recording the making of the form, {planes.sculpt.value}..."
        )
        self._show_stage(film)

    def _film_grew(self, film) -> None:
        """A stage landed: show it if it is the one being looked at."""
        if film is not self._film.film:
            return
        self._state.film_changed.emit(film)
        self._show_stage(film)

    def _film_settled(self, film, complete: bool) -> None:
        if film is not self._film.film:
            return
        self._state.film_changed.emit(film)
        self._state.recording_changed.emit(False)
        if complete:
            self._state.status_message.emit(
                f"The making of the form, in {len(film)} stages"
            )

    def _show_stage(self, film) -> None:
        """Draw whichever stage of ``film`` the scrub handle is on."""
        planes = self._state.render.planes
        stage = film.at(planes.sculpt_stage)
        if stage is None:
            return  # nothing recorded yet; the viewport keeps what it has
        self._show_sculpt(film_shaded(stage, planes.sculpt_smooth))

    def _show_sculpt(self, proxy) -> None:
        self.makeCurrent()
        self._renderer.set_sculpt(proxy)
        self.doneCurrent()
        self.update()

    def _upload_contour(self) -> None:
        """Cut the mesh with each section plane and expand the result to strokes."""
        settings = self._state.render.section
        mesh = self._state.mesh
        blocks = []
        if mesh is not None and settings.enabled and settings.show_contour:
            for plane in settings.planes():
                segments = section_segments(mesh, plane)
                # The stroke shader lifts along the supplied normal, so point it
                # into the material that survives the cut.
                blocks.append(
                    build_segment_vertices(
                        segments, settings.contour_color, settings.contour_width, -plane.normal
                    )
                )
        vertices = np.concatenate(blocks) if blocks else np.zeros((0, 14), dtype=np.float32)
        self.makeCurrent()
        self._renderer.set_contour(vertices)
        self.doneCurrent()

    def _release_gl(self) -> None:
        """Free every GL object while the owning context is still current."""
        if not self._ready:
            return
        self.makeCurrent()
        self._renderer.dispose()
        self.doneCurrent()
        self._ready = False

    # ------------------------------------------------------------------
    # Tool control
    # ------------------------------------------------------------------

    def set_measure_active(self, active: bool) -> None:
        self._arm(self.measure_tool, active)

    def set_annotate_active(self, active: bool) -> None:
        self._arm(self.annotate_tool, active)

    def set_armature_active(self, active: bool) -> None:
        self._arm(self.armature_tool, active)

    def _arm(self, tool, active: bool) -> None:
        """Arm one tool, disarming the rest.

        Only one gesture can own the left button, so arming is written once
        here rather than as a pairwise dance between every two tools.
        """
        tool.set_active(active)
        if active:
            for other in (self.measure_tool, self.annotate_tool, self.armature_tool):
                if other is not tool:
                    other.set_active(False)
        self._refresh_cursor()
        self.update()

    def cancel_tools(self) -> None:
        """Drop whatever gesture is half-finished, without disarming the tool."""
        self.measure_tool.cancel()
        self.annotate_tool.cancel()
        self.armature_tool.cancel()
        self.update()

    def _refresh_cursor(self) -> None:
        armed = self.measure_tool.active or self.annotate_tool.active
        if armed or self.armature_tool.active:
            self.setCursor(Qt.CursorShape.CrossCursor)
        elif (
            self.measure_tool.hover_handle
            or self.armature_tool.hover_handle
            or self.armature_tool.hover_landmark
        ):
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------

    def mousePressEvent(self, event) -> None:  # noqa: N802 - Qt naming
        position = event.position()
        x, y = position.x(), position.y()
        self._press_position = (x, y)
        self._travel = 0.0

        if event.button() == Qt.MouseButton.LeftButton and not self._orbit_override(event):
            # Painting owns the button outright; otherwise a press that lands on
            # an unlocked endpoint moves it instead of turning the camera.
            if self.annotate_tool.active:
                claimed = self._begin_annotation(x, y)
            else:
                resize = bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
                # Landmarks are offered first, within a tighter reach: a node
                # derived from one sits right beside it, and the landmark is the
                # thing that can still be corrected without the armature
                # leaving its preset.
                claimed = (
                    self._begin_landmark_drag(x, y)
                    or self._begin_node_drag(x, y, resize)
                    or self._begin_handle_drag(x, y)
                )
            if claimed:
                return
        elif event.button() not in (
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.RightButton,
            Qt.MouseButton.MiddleButton,
        ):
            return

        mode = DragMode.ORBIT if event.button() == Qt.MouseButton.LeftButton else DragMode.PAN
        self._navigation.begin(
            mode, x, y, self._state.camera, self.width(), self.height(), self._scene_center()
        )

    def mouseMoveEvent(self, event) -> None:  # noqa: N802 - Qt naming
        position = event.position()
        x, y = position.x(), position.y()

        if self.armature_tool.grabbed_landmark is not None:
            self._move_grabbed_landmark(x, y)
            return
        if self.armature_tool.grabbed_handle is not None:
            self._move_grabbed_node(x, y)
            return
        if self.measure_tool.grabbed_handle is not None:
            self._move_grabbed_handle(x, y)
            return
        if self.annotate_tool.is_drawing or self._erase_previous is not None:
            self._continue_annotation(x, y)
            return
        if self._navigation.is_dragging:
            if self._press_position is not None:
                self._travel = max(
                    self._travel,
                    abs(x - self._press_position[0]) + abs(y - self._press_position[1]),
                )
            snap = self._snap_degrees(event)
            if self._navigation.drag(
                x, y, self._state.camera, self.width(), self.height(), snap
            ):
                self.update()
            return

        self._update_hover(x, y)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802 - Qt naming
        was_click = self._travel <= self.CLICK_TOLERANCE
        position = event.position()

        if self.armature_tool.grabbed_landmark is not None:
            self._commit_landmark_drag(was_click)
        elif self.armature_tool.grabbed_handle is not None:
            joining = self.armature_tool.active or bool(
                event.modifiers() & Qt.KeyboardModifier.ControlModifier
            )
            self._commit_node_drag(was_click, joining)
        elif self.measure_tool.grabbed_handle is not None:
            self._commit_handle_drag()
        elif self.annotate_tool.is_drawing or self._erase_previous is not None:
            self._commit_annotation()
        else:
            self._navigation.end()
            left = event.button() == Qt.MouseButton.LeftButton
            if was_click and left and self.measure_tool.active:
                self._place_measure_point(position.x(), position.y())
            elif was_click and left and self.armature_tool.active:
                self._place_armature_node(position.x(), position.y())

        self._press_position = None
        self._travel = 0.0

    def wheelEvent(self, event) -> None:  # noqa: N802 - Qt naming
        notches = event.angleDelta().y() / 120.0
        if notches == 0.0:
            return
        position = event.position()
        picker = self._picker()
        self._navigation.zoom(
            notches,
            position.x(),
            position.y(),
            self._state.camera,
            self.width(),
            self.height(),
            anchor=picker.point(position.x(), position.y()),
        )
        self.update()

    def keyPressEvent(self, event) -> None:  # noqa: N802 - Qt naming
        if event.key() == Qt.Key.Key_Escape:
            self.cancel_tools()
            return
        super().keyPressEvent(event)

    # ------------------------------------------------------------------
    # Measurement handles
    # ------------------------------------------------------------------

    def _begin_handle_drag(self, x: float, y: float) -> bool:
        handle = self.measure_tool.handle_at(
            x, y, self._state.measurements, self._picker(), self._state.measurement_settings
        )
        if handle is None:
            return False
        index, end = handle
        measurement = self._state.measurements[index]
        field = measurement.endpoint_field(end)
        self._grab_previous = (measurement, field, getattr(measurement, field))
        self.measure_tool.grabbed_handle = handle
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        return True

    def _move_grabbed_handle(self, x: float, y: float) -> None:
        if self._grab_previous is None:
            return
        measurement, field, _ = self._grab_previous
        point = self.measure_tool.drag_target(
            x,
            y,
            self._picker(),
            self._state.measurement_settings,
            np.asarray(getattr(measurement, field), dtype=np.float64),
        )
        setattr(measurement, field, tuple(float(v) for v in point))
        self._state.notify_measurements()

    def _commit_handle_drag(self) -> None:
        """Record the finished drag as a single undo step."""
        self.measure_tool.grabbed_handle = None
        self._refresh_cursor()
        if self._grab_previous is None:
            return
        measurement, field, previous = self._grab_previous
        self._grab_previous = None
        if getattr(measurement, field) == previous:
            return
        self._state.do(
            SetAttributes(
                measurement,
                {field: getattr(measurement, field)},
                text=f"Move {measurement.name}",
                channel=MEASUREMENTS,
                previous={field: previous},
            ),
            apply=False,
        )

    # ------------------------------------------------------------------
    # Annotations
    # ------------------------------------------------------------------

    def _begin_annotation(self, x: float, y: float) -> bool:
        if not self.annotate_tool.active or self._state.mesh is None:
            return False
        if self._state.annotation_settings.mode.is_eraser:
            self._erase_previous = list(self._state.annotations)
            self._erase_at(x, y)
            return True
        return self.annotate_tool.begin(x, y, self._picker(), self._state.annotation_settings)

    def _continue_annotation(self, x: float, y: float) -> None:
        if self._erase_previous is not None:
            self.annotate_tool.cursor = (x, y)
            self._erase_at(x, y)
            return
        if self.annotate_tool.drag(x, y, self._picker(), self._state.annotation_settings):
            self.update()

    def _commit_annotation(self) -> None:
        if self._erase_previous is not None:
            previous, self._erase_previous = self._erase_previous, None
            current = self._state.annotations.items
            if len(current) != len(previous) or any(a is not b for a, b in zip(current, previous)):
                self._state.do(
                    ReplaceItems(
                        current,
                        list(current),
                        text="Erase annotation",
                        channel=ANNOTATIONS,
                        previous=previous,
                    ),
                    apply=False,
                )
            return

        strokes = self.annotate_tool.finish(self._picker(), self._state.annotation_settings)
        if not strokes:
            self.update()
            return
        items = self._state.annotations.items
        label = f"Paint {strokes[0].kind.label.lower()}"
        # A gesture that crossed the silhouette lands as several strokes; they
        # were one movement, so they undo as one step.
        command = (
            AddItem(items, strokes[0], text=label, channel=ANNOTATIONS)
            if len(strokes) == 1
            else ReplaceItems(items, [*items, *strokes], text=label, channel=ANNOTATIONS)
        )
        self._state.do(command)

    def _erase_at(self, x: float, y: float) -> None:
        """Rub out the stroke points under the eraser, live."""
        target = self.annotate_tool.erase_target(
            x, y, self._picker(), self._state.annotation_settings
        )
        if target is None:
            self.update()
            return
        remaining = self._state.annotations.erased(*target)
        if remaining is None:
            self.update()
            return
        self._state.annotations.items[:] = remaining
        self._state.notify_annotations()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _orbit_override(event) -> bool:
        """Alt forces the camera gesture, whichever tool is armed."""
        return bool(event.modifiers() & Qt.KeyboardModifier.AltModifier)

    # ------------------------------------------------------------------
    # Armature
    # ------------------------------------------------------------------

    def _armature_index(self) -> int:
        """Which armature an edit lands in, counting a guided run as binding."""
        run = self.armature_tool.guide
        if run is not None and 0 <= run.armature < len(self._state.armatures):
            return run.armature
        selected = self.armature_tool.selected
        if selected is not None and selected[0] < len(self._state.armatures):
            return selected[0]
        return len(self._state.armatures) - 1

    def _place_armature_node(self, x: float, y: float) -> None:
        """Drop a node, or record the landmark a guided run is asking for."""
        index = self._armature_index()
        if index < 0:
            return
        armature = self._state.armatures[index]
        settings = self._state.armature_settings
        point = self.armature_tool.pick(x, y, self._picker(), settings)
        if point is None:
            self.pick_failed.emit()
            return

        self.armature_tool.hover_point = point
        edit = self._insert_on_bone(x, y) or self.armature_tool.place(armature, point, settings)
        if edit is None:
            return
        nodes, bones, landmarks = edit
        label = "Place landmark" if self.armature_tool.guiding else f"Add node to {armature.name}"
        self.armature_edited.emit((index, nodes, bones, landmarks, label))
        if not self.armature_tool.guiding and nodes:
            self.armature_tool.selected = (index, len(nodes) - 1)
            self.armature_selected.emit((index, len(nodes) - 1))
        self._stale_buried()
        self.update()

    def _insert_on_bone(self, x: float, y: float):
        """A click on a length of wire lengthens the chain rather than branching off it.

        Only outside a guided run: while a preset is asking for the next
        landmark, a click is an answer to that question and nothing else.
        """
        tool = self.armature_tool
        if tool.guiding:
            return None
        picker = self._picker()
        found = tool.bone_at(x, y, self._state.armatures, picker, self._state.armature_settings)
        if found is None:
            return None
        index, position = found
        armature = self._state.armatures[index]
        point = tool.split_point(armature, armature.bones[position], x, y, picker)
        if point is None:
            return None
        return tool.insert_on_bone(armature, position, point)

    def _begin_node_drag(self, x: float, y: float, resize: bool) -> bool:
        """Take hold of a node, to move it, resize it, or just to select it.

        This works whether or not the tool is armed, exactly as an unlocked
        measurement endpoint does: clicking a node to see which one it is
        should not first require arming anything.
        """
        handle = self.armature_tool.handle_at(
            x, y, self._state.armatures, self._picker(), self._state.armature_settings
        )
        if handle is None:
            return False
        index, position = handle
        node = self._state.armatures[index].nodes[position]
        field = "size" if resize else "at"
        self._node_previous = (node, field, getattr(node, field))
        self._join_from = self.armature_tool.selected
        self.armature_tool.grabbed_handle = handle
        self.armature_tool.resizing = resize
        self.armature_tool.selected = handle
        self.setCursor(
            Qt.CursorShape.SizeHorCursor if resize else Qt.CursorShape.ClosedHandCursor
        )
        return True

    def _move_grabbed_node(self, x: float, y: float) -> None:
        """Apply the drag live, so the artist sees the wire bend as they pull it."""
        if self._node_previous is None:
            return
        node, field, _ = self._node_previous
        picker = self._picker()
        if field == "size":
            node.size = self.armature_tool.size_target(x, y, picker, node)
        else:
            point = self.armature_tool.drag_target(
                x, y, picker, self._state.armature_settings, node.point
            )
            node.at = tuple(float(value) for value in point)
        self._state.notify_armature()

    def _commit_node_drag(self, was_click: bool = False, joining: bool = False) -> None:
        """Record the finished gesture: a move, a resize, or a plain click.

        A press that never travelled did not edit anything, so it is read as a
        selection instead -- and, with the tool armed or Ctrl held, as a second
        node to run a bone to.
        """
        handle = self.armature_tool.grabbed_handle
        self.armature_tool.grabbed_handle = None
        self.armature_tool.resizing = False
        self._refresh_cursor()
        anchor, self._join_from = self._join_from, None
        if self._node_previous is None:
            return
        node, field, previous = self._node_previous
        self._node_previous = None

        if getattr(node, field) != previous:
            verb = "Resize" if field == "size" else "Move"
            self._state.do(
                SetAttributes(
                    node,
                    {field: getattr(node, field)},
                    text=f"{verb} {node.name}",
                    channel=ARMATURE,
                    previous={field: previous},
                ),
                apply=False,
            )
            self._detach_from_preset(node)
            return

        if not was_click or handle is None:
            return
        self.armature_selected.emit(handle)
        if joining and anchor is not None and anchor != handle:
            self._join_nodes(anchor, handle)
        self.update()

    # -- landmarks ------------------------------------------------------
    #
    # A node is one object with a position, so dragging one writes through to it
    # and the undo step is one attribute.  A landmark is not: the wire is
    # derived from the whole set, so moving one rewrites three lists at once.
    # Hence its own trio of methods rather than a flag through the node drag.

    def _begin_landmark_drag(self, x: float, y: float) -> bool:
        """Take hold of a landmark, to move it or just to say which one it is."""
        found = self.armature_tool.landmark_at(
            x, y, self._state.armatures, self._picker(), self._state.armature_settings
        )
        if found is None:
            return False
        index, key = found
        armature = self._state.armatures[index]
        # Copied, not shared: the re-derive below builds fresh lists, and what
        # an undo puts back must not be something a later drag can reach into.
        self._landmark_previous = (
            index,
            key,
            {
                "nodes": list(armature.nodes),
                "bones": list(armature.bones),
                "landmarks": [replace(entry) for entry in armature.landmarks],
            },
        )
        self.armature_tool.grabbed_landmark = found
        self.armature_tool.selected_landmark = found
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        return True

    def _move_grabbed_landmark(self, x: float, y: float) -> None:
        """Apply the drag live, so the figure re-forms under the cursor."""
        if self._landmark_previous is None:
            return
        index, key, _ = self._landmark_previous
        armature = self._state.armatures[index]
        landmark = armature.landmark_for(key)
        if landmark is None:
            return
        point = self.armature_tool.drag_target(
            x, y, self._picker(), self._state.armature_settings, landmark.point
        )
        landmarks = armature.with_landmark_at(key, tuple(float(value) for value in point))
        # The same re-derive the panel's position boxes go through, applied
        # straight rather than through the history: the whole drag is one step,
        # recorded when the button comes up.
        if armature.derived:
            nodes, bones, landmarks = self.armature_tool.derive(
                armature, landmarks, self._state.armature_settings
            )
            armature.nodes, armature.bones = nodes, bones
        armature.landmarks = landmarks
        self._state.notify_armature()

    def _commit_landmark_drag(self, was_click: bool = False) -> None:
        """Record the finished drag as one step, or read a press as a selection."""
        found = self.armature_tool.grabbed_landmark
        self.armature_tool.grabbed_landmark = None
        self._refresh_cursor()
        if self._landmark_previous is None:
            return
        index, key, previous = self._landmark_previous
        self._landmark_previous = None
        armature = self._state.armatures[index]

        before = next((entry for entry in previous["landmarks"] if entry.key == key), None)
        after = armature.landmark_for(key)
        if after is not None and (before is None or before.at != after.at):
            self._state.do(
                SetAttributes(
                    armature,
                    {name: getattr(armature, name) for name in previous},
                    text=f"Move {landmark_title(armature, key)}",
                    channel=ARMATURE,
                    previous=previous,
                ),
                apply=False,
            )
            return

        if was_click and found is not None:
            self.landmark_selected.emit(found)
        self.update()

    def _join_nodes(self, first: tuple[int, int], second: tuple[int, int]) -> None:
        """Run a bone between two nodes of the same armature."""
        if first[0] != second[0] or not 0 <= first[0] < len(self._state.armatures):
            return
        armature = self._state.armatures[first[0]]
        edit = self.armature_tool.join(armature, first[1], second[1])
        if edit is None:
            return
        name = armature.nodes[second[1]].name
        self.armature_edited.emit((first[0], *edit, f"Join {name}"))

    def _detach_from_preset(self, node: ArmatureNode) -> None:
        """A node moved by hand stops following its landmarks.

        Recorded as its own step rather than folded into the drag, so undoing
        the move puts the armature back under the preset as well.
        """
        for armature in self._state.armatures:
            if not armature.derived or node not in armature.nodes:
                continue
            self._state.do(
                SetAttributes(
                    armature,
                    {"derived": False},
                    text=f"Detach {armature.name} from its preset",
                    channel=ARMATURE,
                )
            )
            return

    def _armature_moved(self) -> None:
        self._stale_buried()
        self.update()

    def _stale_buried(self) -> None:
        self._buried_stale = True

    def _buried_nodes(self) -> frozenset[tuple[int, int]]:
        """The nodes the model is standing in front of, worked out at most once.

        A node is buried when the surface under it is nearer the eye than the
        node itself.  That is one ray per node, which is nothing for a figure
        and everything if it were done per frame of an orbit -- hence the
        cache, invalidated when the camera or the armature moves.
        """
        settings = self._state.armature_settings
        if settings.buried is Buried.SHOW or not settings.show_all:
            return frozenset()
        if not self._buried_stale:
            return self._buried

        picker = self._picker()
        eye = self._state.camera.eye
        sunk: set[tuple[int, int]] = set()
        if picker.mesh is not None:
            for index, armature in enumerate(self._state.armatures):
                if not armature.visible:
                    continue
                for position, node in enumerate(armature.nodes):
                    screen = self._state.camera.project(node.point, self.width(), self.height())
                    hit = picker.hit(screen[0], screen[1])
                    if hit is None:
                        continue
                    if hit.distance < float(np.linalg.norm(node.point - eye)):
                        sunk.add((index, position))
        self._buried = frozenset(sunk)
        self._buried_stale = False
        return self._buried

    def center_on_point(self, point) -> None:
        """Slide the view so a point sits at the centre, keeping the angle."""
        camera = self._state.camera
        offset = np.asarray(point, dtype=np.float64) - camera.target
        camera.eye = camera.eye + offset
        camera.target = camera.target + offset
        self._state.notify_camera()

    def _snap_degrees(self, event) -> float:
        """Orbit increment while Shift is held, or 0 for a free orbit."""
        shift = bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
        return self._state.navigation.snap_angle_deg if shift else 0.0

    def _picker(self) -> SurfacePicker:
        return SurfacePicker(self._state.camera, self._state.mesh, self.width(), self.height())

    def _scene_center(self) -> np.ndarray | None:
        """Object centre, which anchors the plane the orbit pivot lies on."""
        mesh = self._state.mesh
        return None if mesh is None else np.asarray(mesh.bounds.center, dtype=np.float64)

    def _update_hover(self, x: float, y: float) -> None:
        """Track whatever the cursor is over, so the overlay can respond."""
        dirty = False
        if self.annotate_tool.active:
            self.annotate_tool.cursor = (x, y)
            dirty = True
        if self.measure_tool.active:
            self.measure_tool.hover_point = self.measure_tool.pick(
                x, y, self._picker(), self._state.measurement_settings
            )
            dirty = True

        if self.armature_tool.active:
            self.armature_tool.hover_point = self.armature_tool.pick(
                x, y, self._picker(), self._state.armature_settings
            )
            dirty = True
        if self._update_armature_hover(x, y):
            dirty = True

        previous = self.measure_tool.hover_handle
        self.measure_tool.hover_handle = (
            None
            if self.annotate_tool.active
            or self.armature_tool.hover_handle is not None
            or self.armature_tool.hover_landmark is not None
            else self.measure_tool.handle_at(
                x, y, self._state.measurements, self._picker(), self._state.measurement_settings
            )
        )
        if self.measure_tool.hover_handle != previous:
            self._refresh_cursor()
            dirty = True
        if dirty:
            self.update()

    def _update_armature_hover(self, x: float, y: float) -> bool:
        """Track the node and bone under the cursor; True when anything changed."""
        tool = self.armature_tool
        settings = self._state.armature_settings
        picker = self._picker()
        # In the order the press resolves them, so what lights up under the
        # cursor is what taking hold would actually grab.
        landmark = (
            None
            if self.annotate_tool.active
            else tool.landmark_at(x, y, self._state.armatures, picker, settings)
        )
        handle = (
            None
            if landmark is not None or self.annotate_tool.active
            else tool.handle_at(x, y, self._state.armatures, picker, settings)
        )
        bone = (
            None
            if landmark is not None or handle is not None or self.annotate_tool.active
            else tool.bone_at(x, y, self._state.armatures, picker, settings)
        )
        changed = (
            handle != tool.hover_handle
            or bone != tool.hover_bone
            or landmark != tool.hover_landmark
        )
        if handle != tool.hover_handle or landmark != tool.hover_landmark:
            tool.hover_handle = handle
            tool.hover_landmark = landmark
            self._refresh_cursor()
        tool.hover_bone = bone
        return changed

    def _place_measure_point(self, x: float, y: float) -> None:
        point = self.measure_tool.pick(x, y, self._picker(), self._state.measurement_settings)
        if point is None:
            self.pick_failed.emit()
            return
        self.measure_tool.hover_point = point
        measurement = self.measure_tool.click(point, self._state.measurements.next_name())
        if measurement is not None:
            self.measurement_created.emit(measurement)
        self.update()

    def center_on(self, measurement: Measurement) -> None:
        """Slide the view so a measurement sits at the centre, keeping the angle."""
        camera = self._state.camera
        offset = measurement.midpoint - camera.target
        camera.eye = camera.eye + offset
        camera.target = camera.target + offset
        self._state.notify_camera()
