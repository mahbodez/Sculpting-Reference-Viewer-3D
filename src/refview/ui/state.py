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
from ..core.armature import ArmatureSettings, ArmatureStore
from ..core.bookmark import BookmarkStore
from ..core.camera import Camera
from ..core.forms import FormSettings, FormStore
from ..core.history import (
    ANNOTATIONS,
    ARMATURE,
    BOOKMARKS,
    FORMS,
    MEASUREMENTS,
    SKELETON,
    Command,
    History,
)
from ..core.measurement import MeasurementSettings, MeasurementStore
from ..core.mesh import Mesh
from ..core.mesh_io import load_mesh as read_mesh
from ..core.orientation import OrientationSettings
from ..core.session import Session, sidecar_path
from ..core.settings import NavigationSettings, RenderSettings
from ..core.skeleton import Skeleton, SkeletonSettings, SkeletonStore, skinned_mesh
from ..render.texture import MatcapLoadError, load_matcap_pixels


class ViewerState(QObject):
    """Everything the viewer displays, plus change notifications."""

    mesh_changed = Signal()
    matcap_changed = Signal()
    render_changed = Signal()
    camera_changed = Signal()
    measurements_changed = Signal()
    annotations_changed = Signal()
    armature_changed = Signal()
    forms_changed = Signal()
    #: A skeleton was made, edited, posed or removed.  The model follows a
    #: bound skeleton, so this is usually followed by :attr:`mesh_changed`.
    skeleton_changed = Signal()
    #: The model has been re-posed under a drag still in progress.  Only
    #: the geometry moved; the caches built on the model are left to the
    #: :attr:`mesh_changed` that follows when the button comes up.
    mesh_deformed = Signal()
    bookmarks_changed = Signal()
    history_changed = Signal()
    #: A film of a form's making gained a stage, or finished.  Carries the
    #: film itself, so the panel can size its scrub slider to what has been
    #: recorded so far rather than to what was asked for.
    film_changed = Signal(object)
    #: Whether a film is being recorded right now.  The settings a recording
    #: is built from are held still while it runs, so this is what the panel
    #: puts its controls to sleep by.
    recording_changed = Signal(bool)
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
        self.armature_settings = ArmatureSettings()
        self.armatures = ArmatureStore()
        self.form_settings = FormSettings()
        self.forms = FormStore()
        self.skeleton_settings = SkeletonSettings()
        self.skeletons = SkeletonStore()
        self.bookmarks = BookmarkStore()
        self.history = History()
        self.orientation = OrientationSettings()
        #: The panel arrangement carried by the last session that was loaded.
        #: A passenger: nothing here reads it, and the window takes it off
        #: after a load.  See :attr:`refview.core.session.Session.layout`.
        self.session_layout: dict = {}
        #: What is drawn: the rest mesh, or the rest mesh as the bound
        #: skeleton poses it.
        self.mesh: Mesh | None = None
        #: The model turned and centred but not posed.  What the skinning
        #: reads, so that one pose is never built on top of another.
        self.rest_mesh: Mesh | None = None
        #: The mesh exactly as the file stored it.  Every orientation is
        #: applied to this rather than to the last result, so switching back
        #: and forth cannot accumulate drift.
        self.source_mesh: Mesh | None = None
        self.mesh_path: Path | None = None
        self.matcap_pixels: np.ndarray | None = None
        #: The pose the drawn mesh was last skinned for; see :meth:`_posed`.
        self._pose_key: tuple | None = None
        #: Whether the drawn mesh was last announced through
        #: :attr:`mesh_deformed`, and so still owes a :attr:`mesh_changed`.
        self._mesh_live = False

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

    def notify_armature(self) -> None:
        self.armature_changed.emit()

    def notify_forms(self) -> None:
        self.forms_changed.emit()

    def notify_skeleton(self, live: bool = False) -> None:
        """The skeletons changed; re-pose the model if one of them drives it.

        ``live`` is a drag in progress: the posed geometry is handed on
        through :attr:`mesh_deformed` rather than :attr:`mesh_changed`, so
        the pedestal, the section and the planes are not rebuilt at every
        pixel of the gesture.
        """
        self.skeleton_changed.emit()
        if self.rest_mesh is None:
            return
        posed = self._posed(self.rest_mesh)
        if posed is self.mesh and not (self._mesh_live and not live):
            return
        self.mesh = posed
        if live:
            self._mesh_live = True
            self.mesh_deformed.emit()
        else:
            # Whatever was built on the model while the drag ran is stale,
            # even when the last frame of the drag is the pose being kept.
            self._mesh_live = False
            self.mesh_changed.emit()

    def notify_bookmarks(self) -> None:
        self.bookmarks_changed.emit()

    def notify_channel(self, channel: str) -> None:
        """Emit the change signal a command's channel maps onto."""
        emit = {
            MEASUREMENTS: self.notify_measurements,
            ANNOTATIONS: self.notify_annotations,
            ARMATURE: self.notify_armature,
            FORMS: self.notify_forms,
            SKELETON: self.notify_skeleton,
            BOOKMARKS: self.notify_bookmarks,
            "render": self.notify_render,
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
        self.rest_mesh = mesh
        self.mesh = mesh
        self.mesh_path = path
        self.camera.scene_radius = mesh.bounds.radius
        self.camera.scene_center = np.asarray(mesh.bounds.center, dtype=np.float64)
        self.measurements.clear()
        self.annotations.clear()
        self.armatures.clear()
        self.forms.clear()
        self.skeletons.clear()
        self.bookmarks.clear()
        self.history.clear()
        # A rigged model brings its skeleton in with it, bound to the skin
        # and standing at rest.
        if mesh.rig is not None:
            self.skeletons.add(mesh.rig.to_skeleton(path.stem))
        self.frame_object()
        self.mesh_changed.emit()
        self.notify_measurements()
        self.notify_annotations()
        self.notify_armature()
        self.notify_forms()
        self.notify_skeleton()
        self.notify_bookmarks()
        self.history_changed.emit()
        self.adopt_units(mesh)
        bones = ""
        if mesh.rig is not None:
            bones = f", {mesh.rig.joint_count} joints"
        self.status_message.emit(
            f"Loaded {path.name}: {mesh.vertex_count:,} vertices, "
            f"{mesh.triangle_count:,} triangles{bones}"
        )
        if load_sidecar:
            companion = sidecar_path(path)
            if companion.is_file():
                self.load_session(companion, load_mesh=False)

    def _oriented(self, source: Mesh) -> Mesh:
        """Turn a freshly read mesh the right way up and centre it."""
        return source.transformed(self.orientation.matrix).recentered()

    def _posed(self, rest: Mesh) -> Mesh:
        """The rest mesh as the bound skeleton poses it, or the rest mesh itself.

        Skinning is done once per pose: the joints are summed up into a
        signature and the mesh last built for that signature is handed back
        again, so that switching the joint names on, or undoing a rename,
        does not re-skin the model and rebuild everything standing on it.
        """
        skeleton = self.skeletons.bound()
        if (
            rest.rig is None
            or skeleton is None
            or not self.skeleton_settings.deform
            or not skeleton.deform
            or not skeleton.posed
        ):
            self._pose_key = None
            return rest
        key = (
            id(rest),
            tuple(
                (joint.parent, joint.rest, joint.rotation, joint.translation, joint.source)
                for joint in skeleton.joints
            ),
        )
        if key == self._pose_key and self.mesh is not None and self.mesh is not rest:
            return self.mesh
        self._pose_key = key
        return skinned_mesh(rest, skeleton)

    def bound_skeleton(self) -> Skeleton | None:
        """The skeleton the model follows, if it has one."""
        return None if self.rest_mesh is None or self.rest_mesh.rig is None else (
            self.skeletons.bound()
        )

    def set_orientation(self, orientation: OrientationSettings, move_marks: bool = True) -> None:
        """Turn the model, bringing the marks made on it along.

        Measurements, annotations, the armature and the forms belong to the
        model, so they are carried through the same rotation; a saved camera
        view is a
        viewpoint on the scene rather than a point on the model, and stays
        where it is.

        The turn is not recorded in the undo history: like the camera, it is a
        way of looking at the model rather than an edit to it, and choosing the
        previous orientation puts everything back exactly.
        """
        if self.source_mesh is None:
            self.orientation = orientation
            return

        previous = self.mesh if self.rest_mesh is None else self.rest_mesh
        was = self.orientation.matrix
        self.orientation = orientation
        self.rest_mesh = self._oriented(self.source_mesh)
        if move_marks and previous is not None:
            self._move_marks(previous, self.rest_mesh, was)
        self.mesh = self._posed(self.rest_mesh)

        self.camera.scene_radius = self.mesh.bounds.radius
        self.camera.scene_center = np.asarray(self.mesh.bounds.center, dtype=np.float64)
        self.frame_object()
        self.mesh_changed.emit()
        self.notify_measurements()
        self.notify_annotations()
        self.notify_armature()
        self.notify_forms()
        self.skeleton_changed.emit()

    def _move_marks(self, previous: Mesh, current: Mesh, was: np.ndarray) -> None:
        """Rotate the measurements, annotations, armature and forms onto the turned model.

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
        for armature in self.armatures:
            for node in armature.nodes:
                node.at = move(node.at)
            for landmark in armature.landmarks:
                landmark.at = move(landmark.at)
        for form in self.forms:
            for landmark in form.landmarks:
                landmark.at = move(landmark.at)
        # A skeleton is carried by its roots; everything below them follows.
        carry = np.eye(4)
        carry[:3, :3] = change
        carry[:3, 3] = change @ before - after
        for skeleton in self.skeletons:
            skeleton.joints = skeleton.transformed(carry)

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
            armature_settings=self.armature_settings,
            armatures=list(self.armatures),
            form_settings=self.form_settings,
            forms=list(self.forms),
            skeleton_settings=self.skeleton_settings,
            skeletons=list(self.skeletons),
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
        self.armature_settings = session.armature_settings
        self.armatures = ArmatureStore(list(session.armatures))
        self.form_settings = session.form_settings
        self.forms = FormStore(list(session.forms))
        self.skeleton_settings = session.skeleton_settings
        self.skeletons = SkeletonStore(list(session.skeletons))
        # A session saved before there were skeletons, or one that had cut
        # the model's own rig loose, is given it back at rest.
        rig = None if self.rest_mesh is None else self.rest_mesh.rig
        if rig is not None and self.skeletons.bound() is None:
            self.skeletons.add(rig.to_skeleton(self.mesh_path.stem if self.mesh_path else "Rig"))
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
        self.notify_armature()
        self.notify_forms()
        self.notify_skeleton()
        self.notify_bookmarks()
        self.history_changed.emit()

    def save_session(self, path: str | Path, layout: dict | None = None) -> Path:
        """Write the document, and whatever the window says its layout is.

        The layout travels through here rather than being written by the
        window, because it belongs in the same file as the document and there
        is only one place that writes that file.  Nothing here looks inside
        it; see :attr:`Session.layout`.
        """
        session = self.to_session()
        session.layout = dict(layout or {})
        saved = session.save(path)
        self.status_message.emit(f"Saved session to {saved.name}")
        return saved

    def load_session(self, path: str | Path, load_mesh: bool = True) -> None:
        session = Session.load(path)
        if load_mesh and session.mesh_path and Path(session.mesh_path).is_file():
            self.load_mesh(session.mesh_path, load_sidecar=False)
        self.apply_session(session)
        self.session_layout = dict(session.layout)
        self.status_message.emit(f"Loaded session {Path(path).name}")

    def default_session_path(self) -> Path | None:
        return sidecar_path(self.mesh_path) if self.mesh_path else None
