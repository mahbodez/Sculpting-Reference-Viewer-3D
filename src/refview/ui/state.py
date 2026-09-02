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
from ..core.obj_loader import load_obj
from ..core.session import Session, sidecar_path
from ..core.settings import RenderSettings
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
        self.measurements = MeasurementStore()
        self.annotation_settings = AnnotationSettings()
        self.annotations = AnnotationStore()
        self.bookmarks = BookmarkStore()
        self.history = History()
        self.mesh: Mesh | None = None
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
        """Load an OBJ, centre it on the origin and frame it in the view."""
        path = Path(path)
        mesh = load_obj(path).recentered()
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
        self.status_message.emit(
            f"Loaded {path.name}: {mesh.vertex_count:,} vertices, {mesh.triangle_count:,} triangles"
        )
        if load_sidecar:
            companion = sidecar_path(path)
            if companion.is_file():
                self.load_session(companion, load_mesh=False)

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
            measurements=list(self.measurements),
            bookmarks=list(self.bookmarks),
            annotation_settings=self.annotation_settings,
            annotations=list(self.annotations),
        )

    def apply_session(self, session: Session) -> None:
        """Adopt a session's settings, leaving the loaded mesh alone."""
        self.render = session.render
        self.measurement_settings = session.measurement_settings
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
