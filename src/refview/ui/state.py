"""The observable document shared by the viewport and the side panels.

Panels mutate the plain dataclasses held here and then call one of the
``notify_*`` methods; the viewport listens for the signals and repaints.  All
of the domain logic lives in :mod:`refview.core`, so this class stays a thin
Qt-aware shell.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PySide6.QtCore import QObject, Signal

from ..core.annotation import AnnotationSettings, AnnotationStore
from ..core.bookmark import BookmarkStore
from ..core.camera import Camera
from ..core.history import ANNOTATIONS, BOOKMARKS, MEASUREMENTS, Command, History
from ..core.measurement import MeasurementSettings, MeasurementStore
from ..core.mesh import Mesh
from ..core.mesh_io import load_mesh as read_mesh
from ..core.orientation import OrientationSettings
from ..core.session import Session, sidecar_path
from ..core.settings import NavigationSettings, RenderSettings
from ..render.texture import MatcapLoadError, load_matcap_pixels


class ViewerState(QObject):
    """Everything the viewer displays, plus change notifications."""

    mesh_changed = Signal()
    matcap_changed = Signal()
    render_changed = Signal()
    camera_changed = Signal()
    measurements_changed = Signal()
    annotations_changed = Signal()
    bookmarks_changed = Signal()
    history_changed = Signal()
    status_message = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.camera = Camera()
        self.render = RenderSettings()
        self.measurement_settings = MeasurementSettings()
        self.navigation = NavigationSettings()
        self.measurements = MeasurementStore()
        self.annotation_settings = AnnotationSettings()
        self.annotations = AnnotationStore()
        self.bookmarks = BookmarkStore()
        self.history = History()
        self.orientation = OrientationSettings()
        self.mesh: Mesh | None = None
        #: The mesh exactly as the file stored it.  Every orientation is
        #: applied to this rather than to the last result, so switching back
        #: and forth cannot accumulate drift.
        self.source_mesh: Mesh | None = None
        self.mesh_path: Path | None = None
        self.matcap_pixels: np.ndarray | None = None

    # ------------------------------------------------------------------
    # Change notification
    # ------------------------------------------------------------------

    def notify_render(self) -> None:
        self.render_changed.emit()

    def notify_camera(self) -> None:
        self.camera_changed.emit()

    def notify_measurements(self) -> None:
        self.measurements_changed.emit()

    def notify_annotations(self) -> None:
        self.annotations_changed.emit()

    def notify_bookmarks(self) -> None:
        self.bookmarks_changed.emit()

    def notify_channel(self, channel: str) -> None:
        """Emit the change signal a command's channel maps onto."""
        emit = {
            MEASUREMENTS: self.notify_measurements,
            ANNOTATIONS: self.notify_annotations,
            BOOKMARKS: self.notify_bookmarks,
        }.get(channel)
        if emit is not None:
            emit()

    # ------------------------------------------------------------------
    # Undo / redo
    # ------------------------------------------------------------------

    def do(self, command: Command, apply: bool = True) -> None:
        """Run an edit through the history so it can be undone.

        ``apply=False`` records a change the user already made by hand -- a
        dragged endpoint, a swipe of the eraser -- which the gesture applied
        live so the artist could see it happen.
        """
        self.history.push(command, apply=apply)
        self.notify_channel(command.channel)
        self.history_changed.emit()

    def undo(self) -> bool:
        return self._step(self.history.undo(), "Undo")

    def redo(self) -> bool:
        return self._step(self.history.redo(), "Redo")

    def _step(self, command: Command | None, verb: str) -> bool:
        if command is None:
            self.status_message.emit(f"Nothing to {verb.lower()}")
            return False
        self.notify_channel(command.channel)
        self.history_changed.emit()
        self.status_message.emit(f"{verb}: {command.text}")
        return True

    # ------------------------------------------------------------------
    # Content
    # ------------------------------------------------------------------

    def load_mesh(self, path: str | Path, load_sidecar: bool = True) -> None:
        """Load a model, centre it on the origin and frame it in the view.

        The current orientation carries over to the new model: files from one
        pipeline share an up axis, so having set it once is usually right, and
        the Model panel shows what is being applied.
        """
        path = Path(path)
        self.source_mesh = read_mesh(path)
        mesh = self._oriented(self.source_mesh)
        self.mesh = mesh
        self.mesh_path = path
        self.camera.scene_radius = mesh.bounds.radius
        self.camera.scene_center = np.asarray(mesh.bounds.center, dtype=np.float64)
        self.measurements.clear()
        self.annotations.clear()
        self.bookmarks.clear()
        self.history.clear()
        self.frame_object()
        self.mesh_changed.emit()
        self.notify_measurements()
        self.notify_annotations()
        self.notify_bookmarks()
        self.history_changed.emit()
        self.adopt_units(mesh)
        self.status_message.emit(
            f"Loaded {path.name}: {mesh.vertex_count:,} vertices, {mesh.triangle_count:,} triangles"
        )
        if load_sidecar:
            companion = sidecar_path(path)
            if companion.is_file():
                self.load_session(companion, load_mesh=False)

    def _oriented(self, source: Mesh) -> Mesh:
        """Turn a freshly read mesh the right way up and centre it."""
        return source.transformed(self.orientation.matrix).recentered()

    def set_orientation(self, orientation: OrientationSettings, move_marks: bool = True) -> None:
        """Turn the model, bringing the marks made on it along.

        Measurements and annotations belong to the surface, so they are carried
        through the same rotation; a saved camera view is a viewpoint on the
        scene rather than a point on the model, and stays where it is.

        The turn is not recorded in the undo history: like the camera, it is a
        way of looking at the model rather than an edit to it, and choosing the
        previous orientation puts everything back exactly.
        """
        if self.source_mesh is None:
            self.orientation = orientation
            return

        previous, was = self.mesh, self.orientation.matrix
        self.orientation = orientation
        self.mesh = self._oriented(self.source_mesh)
        if move_marks and previous is not None:
            self._move_marks(previous, self.mesh, was)

        self.camera.scene_radius = self.mesh.bounds.radius
        self.camera.scene_center = np.asarray(self.mesh.bounds.center, dtype=np.float64)
        self.frame_object()
        self.mesh_changed.emit()
        self.notify_measurements()
        self.notify_annotations()

    def _move_marks(self, previous: Mesh, current: Mesh, was: np.ndarray) -> None:
        """Rotate the measurements and annotations onto the turned model.

        A point sits at ``rotation @ file_point - centre`` in both orientations,
        so going from one to the other means undoing the old centring, applying
        the change in rotation, and re-centring.
        """
        change = self.orientation.matrix @ was.T
        before = np.asarray(previous.source_offset, dtype=np.float64)
        after = np.asarray(current.source_offset, dtype=np.float64)

        def move(point) -> tuple[float, float, float]:
            moved = change @ (np.asarray(point, dtype=np.float64) + before) - after
            return tuple(float(value) for value in moved)

        for measurement in self.measurements:
            for handle in range(2):
                field = measurement.endpoint_field(handle)
                setattr(measurement, field, move(getattr(measurement, field)))
        for stroke in self.annotations:
            stroke.points = [move(point) for point in stroke.points]
            stroke.normals = [
                tuple(float(v) for v in change @ np.asarray(normal, dtype=np.float64))
                for normal in stroke.normals
            ]

    def adopt_units(self, mesh: Mesh) -> None:
        """Take the display unit from the file when the format declares one.

        Only glTF does; OBJ and STL carry no unit, so those keep whatever the
        artist set rather than having a guess imposed on them.
        """
        if mesh.units is None:
            return
        self.measurement_settings.unit_name = mesh.units.name
        self.measurement_settings.unit_scale = mesh.units.scale
        self.status_message.emit(f"Scene units: 1 unit = 1 {mesh.units.name} (from the file)")

    def load_matcap(self, path: str | Path | None) -> None:
        """Set the active matcap, or fall back to the built-in one."""
        if path is None:
            self.matcap_pixels = None
            self.render.matcap_path = None
        else:
            path = Path(path)
            self.matcap_pixels = load_matcap_pixels(path)
            self.render.matcap_path = str(path)
        self.matcap_changed.emit()

    def frame_object(self) -> None:
        """Fit the current mesh in the view without changing the direction."""
        if self.mesh is not None:
            self.camera.frame(self.mesh.bounds)
            self.notify_camera()

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------

    def to_session(self) -> Session:
        return Session(
            mesh_path=str(self.mesh_path) if self.mesh_path else None,
            camera=self.camera.to_dict(),
            render=self.render,
            measurement_settings=self.measurement_settings,
            navigation=self.navigation,
            orientation=self.orientation,
            measurements=list(self.measurements),
            bookmarks=list(self.bookmarks),
            annotation_settings=self.annotation_settings,
            annotations=list(self.annotations),
        )

    def apply_session(self, session: Session) -> None:
        """Adopt a session's settings, leaving the loaded mesh alone."""
        self.render = session.render
        self.measurement_settings = session.measurement_settings
        self.navigation = session.navigation
        # The saved marks were made in the saved orientation, so the model is
        # turned to match them rather than the other way round.
        self.set_orientation(session.orientation, move_marks=False)
        self.measurements = MeasurementStore(list(session.measurements))
        self.annotation_settings = session.annotation_settings
        self.annotations = AnnotationStore(list(session.annotations))
        self.bookmarks = BookmarkStore(list(session.bookmarks))
        self.history.clear()
        if session.camera:
            self.camera.apply(Camera.from_dict(session.camera))
        try:
            self.load_matcap(session.render.matcap_path)
        except (MatcapLoadError, OSError) as error:
            # A missing matcap must not cost the artist the rest of the session.
            self.render.matcap_path = None
            self.load_matcap(None)
            self.status_message.emit(f"Matcap unavailable, using the built-in one ({error})")
        self.notify_render()
        self.notify_camera()
        self.notify_measurements()
        self.notify_annotations()
        self.notify_bookmarks()
        self.history_changed.emit()

    def save_session(self, path: str | Path) -> Path:
        saved = self.to_session().save(path)
        self.status_message.emit(f"Saved session to {saved.name}")
        return saved

    def load_session(self, path: str | Path, load_mesh: bool = True) -> None:
        session = Session.load(path)
        if load_mesh and session.mesh_path and Path(session.mesh_path).is_file():
            self.load_mesh(session.mesh_path, load_sidecar=False)
        self.apply_session(session)
        self.status_message.emit(f"Loaded session {Path(path).name}")

    def default_session_path(self) -> Path | None:
        return sidecar_path(self.mesh_path) if self.mesh_path else None
