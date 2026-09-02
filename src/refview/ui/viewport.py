"""The interactive 3D view.

Navigation is: left-drag orbits about the point under the cursor, right- or
middle-drag pans, and the wheel zooms towards whatever the cursor is over.

The left button does triple duty, resolved in this order: a drag on the
endpoint handle of an unlocked measurement moves that point; a drag with the
annotate tool armed paints; anything else orbits.  With the measuring tool
armed a left *click* -- as opposed to a drag -- places a measurement point, so
that gesture too shares the button without fighting the camera.  Holding Alt
always orbits, which is the escape hatch while painting.
"""

from __future__ import annotations

import numpy as np
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QSurfaceFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget

from ..core.annotation import Stroke
from ..core.commands import AddItem, ReplaceItems, SetAttributes
from ..core.history import ANNOTATIONS, MEASUREMENTS
from ..core.measurement import Measurement
from ..render.mesh_renderer import SceneRenderer
from .annotate_tool import AnnotateTool
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
    pick_failed = Signal()

    def __init__(self, state: ViewerState, parent=None) -> None:
        super().__init__(parent)
        self._state = state
        self._renderer = SceneRenderer()
        self._navigation = NavigationController()
        self._overlay = ViewportOverlay()
        self.measure_tool = MeasureTool()
        self.annotate_tool = AnnotateTool()
        self._ready = False
        self._press_position: tuple[float, float] | None = None
        self._travel = 0.0
        self._grab_previous: tuple[Measurement, str, tuple] | None = None
        self._erase_previous: list[Stroke] | None = None

        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMinimumSize(320, 240)

        state.mesh_changed.connect(self._upload_mesh)
        state.matcap_changed.connect(self._upload_matcap)
        state.annotations_changed.connect(self._upload_strokes)
        for signal in (state.render_changed, state.camera_changed, state.measurements_changed):
            signal.connect(self.update)

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
        )
        painter.end()

    def _upload_mesh(self) -> None:
        if not self._ready:
            return
        self.makeCurrent()
        self._renderer.set_mesh(self._state.mesh)
        self.doneCurrent()
        self.update()

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
        self.measure_tool.set_active(active)
        if active:
            self.annotate_tool.set_active(False)
        self._refresh_cursor()
        self.update()

    def set_annotate_active(self, active: bool) -> None:
        self.annotate_tool.set_active(active)
        if active:
            self.measure_tool.set_active(False)
        self._refresh_cursor()
        self.update()

    def cancel_tools(self) -> None:
        """Drop whatever gesture is half-finished, without disarming the tool."""
        self.measure_tool.cancel()
        self.annotate_tool.cancel()
        self.update()

    def _refresh_cursor(self) -> None:
        if self.measure_tool.active or self.annotate_tool.active:
            self.setCursor(Qt.CursorShape.CrossCursor)
        elif self.measure_tool.hover_handle is not None:
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
            claimed = (
                self._begin_annotation(x, y)
                if self.annotate_tool.active
                else self._begin_handle_drag(x, y)
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
            if self._navigation.drag(x, y, self._state.camera, self.width(), self.height()):
                self.update()
            return

        self._update_hover(x, y)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802 - Qt naming
        was_click = self._travel <= self.CLICK_TOLERANCE
        position = event.position()

        if self.measure_tool.grabbed_handle is not None:
            self._commit_handle_drag()
        elif self.annotate_tool.is_drawing or self._erase_previous is not None:
            self._commit_annotation()
        else:
            self._navigation.end()
            left = event.button() == Qt.MouseButton.LeftButton
            if was_click and left and self.measure_tool.active:
                self._place_measure_point(position.x(), position.y())

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

        previous = self.measure_tool.hover_handle
        self.measure_tool.hover_handle = (
            None
            if self.annotate_tool.active
            else self.measure_tool.handle_at(
                x, y, self._state.measurements, self._picker(), self._state.measurement_settings
            )
        )
        if self.measure_tool.hover_handle != previous:
            self._refresh_cursor()
            dirty = True
        if dirty:
            self.update()

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
