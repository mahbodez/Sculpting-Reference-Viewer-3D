"""The observable document shared by the viewport and the side panels.

Panels mutate the plain dataclasses held here and then call one of the
``notify_*`` methods; the viewport listens for the signals and repaints.  All
of the domain logic lives in :mod:`refview.core`, so this class stays a thin
Qt-aware shell.

The scene holds any number of objects, but most of the viewer still reads it
as one mesh -- picking, the section, the pedestal, the planes and the shadows
all take :attr:`ViewerState.mesh` and are none the wiser.  So that is what it
is: the objects that are shown, each carried to where it stands in the world,
joined into one mesh here whenever any of them changes.  When there is one
object standing at the origin, as there always was before, the mesh is that
object's own and nothing is copied.
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
    OBJECTS,
    SKELETON,
    Command,
    History,
)
from ..core.measurement import MeasurementSettings, MeasurementStore
from ..core.mesh import Mesh, MeshLoadError, concatenated
from ..core.mesh_io import load_mesh as read_mesh
from ..core.mesh_io import save_mesh
from ..core.orientation import OrientationSettings
from ..core.scene import (
    ObjectRecord,
    ObjectSettings,
    ObjectStore,
    SceneObject,
    Snapshot,
    Transform,
    duplicate_object,
    merge_objects,
    records_for,
    split_object,
)
from ..core.session import Session, sidecar_path
from ..core.settings import NavigationSettings, RenderSettings
from ..core.skeleton import Skeleton, SkeletonSettings, SkeletonStore, skinned_mesh
from ..render.texture import MatcapLoadError, load_matcap_pixels


class ObjectsEdit(Command):
    """An edit to the objects -- a move, a parenting, a removal -- as two snapshots.

    Every edit to the list is recorded whole rather than as the difference,
    because the differences are many kinds -- a transform, a parent, a
    removal that re-hangs three children -- and a snapshot of the list is
    small: a few references and a transform per object.  Applying one puts
    the skeletons bound to the objects back where the objects are.
    """

    def __init__(
        self,
        state: ViewerState,
        after: Snapshot,
        before: Snapshot,
        text: str,
        skeleton: Skeleton | None = None,
    ) -> None:
        super().__init__(text, OBJECTS)
        self._state = state
        self._after = after
        self._before = before
        #: A skeleton that came in with the object -- a rigged model's own --
        #: and so goes out with it when the step is undone.
        self._skeleton = skeleton

    def apply(self) -> None:
        skeletons = self._state.skeletons
        if self._skeleton is not None and not any(s is self._skeleton for s in skeletons):
            skeletons.add(self._skeleton)
            self._state.skeleton_changed.emit()
        self._state._restore_objects(self._after)

    def revert(self) -> None:
        skeletons = self._state.skeletons
        if self._skeleton is not None and any(s is self._skeleton for s in skeletons):
            skeletons.items.remove(self._skeleton)
            self._state.skeleton_changed.emit()
        self._state._restore_objects(self._before)


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
    #: The list of objects changed: one was added, removed, renamed, hidden,
    #: re-hung or made active.  What the Model panel rebuilds its tree on;
    #: the geometry itself announces through :attr:`mesh_changed` as it
    #: always did.
    objects_changed = Signal()
    #: Only how solid the objects are drawn changed, not what or where they
    #: are: the renderer takes the new numbers and nothing is rebuilt.
    parts_changed = Signal()
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
        #: The models in the scene, and which of them is active.
        self.objects = ObjectStore()
        self.object_settings = ObjectSettings()
        #: The panel arrangement carried by the last session that was loaded.
        #: A passenger: nothing here reads it, and the window takes it off
        #: after a load.  See :attr:`refview.core.session.Session.layout`.
        self.session_layout: dict = {}
        #: What is drawn and picked: every object that is shown, standing
        #: where it stands, posed as its skeleton poses it, as one mesh.
        self.mesh: Mesh | None = None
        #: The same, object by object: each with its world mesh and how solid
        #: it is drawn, in the order the composite was joined in.  What the
        #: renderer draws, so that one object can be ghosted beside another.
        self.mesh_parts: list[tuple[SceneObject, Mesh, float]] = []
        self.matcap_pixels: np.ndarray | None = None
        #: Whether the drawn mesh was last announced through
        #: :attr:`mesh_deformed`, and so still owes a :attr:`mesh_changed`.
        self._mesh_live = False

    # ------------------------------------------------------------------
    # The active object, in the names the rest of the viewer knows
    # ------------------------------------------------------------------

    @property
    def active_object(self) -> SceneObject | None:
        return self.objects.active_object

    @property
    def rest_mesh(self) -> Mesh | None:
        """The active object turned and centred but not posed or placed."""
        active = self.active_object
        return None if active is None else active.rest_mesh

    @rest_mesh.setter
    def rest_mesh(self, mesh: Mesh | None) -> None:
        active = self._active_or_new(mesh)
        if active is not None and mesh is not None:
            active.rest_mesh = mesh
            active.forget()

    @property
    def source_mesh(self) -> Mesh | None:
        """The active object exactly as its file stored it."""
        active = self.active_object
        return None if active is None else active.source_mesh

    @source_mesh.setter
    def source_mesh(self, mesh: Mesh | None) -> None:
        """Set the active object's file mesh; its rest mesh is turned from it as at a load."""
        active = self._active_or_new(mesh)
        if active is not None and mesh is not None:
            active.source_mesh = mesh
            active.rest_mesh = self._oriented(mesh)
            active.forget()
            self._rebuild(quiet_if_same=True)

    @property
    def mesh_path(self) -> Path | None:
        active = self.active_object
        return None if active is None else active.path

    @mesh_path.setter
    def mesh_path(self, path: str | Path | None) -> None:
        active = self.active_object
        if active is not None:
            active.path = None if path is None else Path(path)

    def _active_or_new(self, mesh: Mesh | None) -> SceneObject | None:
        """The active object, made on the spot when a mesh is handed to an empty scene."""
        active = self.active_object
        if active is None and mesh is not None:
            active = self.objects.add(SceneObject(mesh, self._oriented(mesh), name=mesh.name))
        return active

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

    def notify_objects(self) -> None:
        self.objects_changed.emit()

    def notify_skeleton(self, live: bool = False) -> None:
        """The skeletons changed; re-pose the model if one of them drives it.

        ``live`` is a drag in progress: the posed geometry is handed on
        through :attr:`mesh_deformed` rather than :attr:`mesh_changed`, so
        the pedestal, the section and the planes are not rebuilt at every
        pixel of the gesture.
        """
        self.skeleton_changed.emit()
        if not len(self.objects):
            return
        self._rebuild(live=live, quiet_if_same=True)

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
            OBJECTS: self.notify_objects,
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
    # The one mesh the viewer reads
    # ------------------------------------------------------------------

    def _skeleton_for(self, obj: SceneObject, claimed: set[int]) -> Skeleton | None:
        """The skeleton bound to ``obj``'s rig, if one is and no other object has it."""
        rig = obj.rig
        if rig is None:
            return None
        names = set(rig.names)
        for skeleton in self.skeletons:
            if id(skeleton) in claimed or not skeleton.bound:
                continue
            if any(joint.source in names for joint in skeleton.joints):
                claimed.add(id(skeleton))
                return skeleton
        return None

    def _posed(self, obj: SceneObject, rest: Mesh, skeleton: Skeleton | None) -> Mesh:
        """``rest`` as the bound skeleton poses it, or ``rest`` itself.

        Skinning is done once per pose: the joints are summed up into a
        signature and the mesh last built for that signature is handed back
        again, so that switching the joint names on, or undoing a rename,
        does not re-skin the model and rebuild everything standing on it.
        """
        if (
            rest.rig is None
            or skeleton is None
            or not self.skeleton_settings.deform
            or not skeleton.deform
            or not skeleton.posed
        ):
            obj._pose = None
            return rest
        key = (
            id(rest),
            tuple(
                (joint.parent, joint.rest, joint.rotation, joint.translation, joint.source)
                for joint in skeleton.joints
            ),
        )
        if obj._pose is not None and obj._pose[0] == key:
            return obj._pose[1]
        posed = skinned_mesh(rest, skeleton)
        obj._pose = (key, posed)
        return posed

    def _rebuild(self, live: bool = False, quiet_if_same: bool = False) -> None:
        """Join the shown objects into :attr:`mesh` and say that it changed.

        ``live`` announces through :attr:`mesh_deformed`, for the frames of a
        drag; ``quiet_if_same`` says nothing at all when the mesh that comes
        out is the one already held and nothing is owed from a drag.
        """
        parts: list[tuple[SceneObject, Mesh, float]] = []
        claimed: set[int] = set()
        for obj in self.objects:
            if not self.objects.shown(obj, self.object_settings):
                continue
            rest = obj.world_rest(self.objects.world_matrix(obj))
            posed = self._posed(obj, rest, self._skeleton_for(obj, claimed))
            parts.append((obj, posed, self.objects.opacity(obj, self.object_settings)))
        unchanged = (
            self.mesh is not None
            and len(parts) == len(self.mesh_parts)
            and all(
                part is held
                for (_, part, _), (_, held, _) in zip(parts, self.mesh_parts, strict=True)
            )
        )
        if not parts:
            mesh = None
        elif len(parts) == 1:
            mesh = parts[0][1]
        elif unchanged:
            mesh = self.mesh  # the same meshes in the same places: keep the join
        else:
            mesh = concatenated([part for _, part, _ in parts], name="scene")
        self.mesh_parts = parts
        if unchanged and mesh is self.mesh and quiet_if_same and not (
            self._mesh_live and not live
        ):
            return
        self.mesh = mesh
        if live:
            self._mesh_live = True
            self.mesh_deformed.emit()
            return
        # Whatever was built on the model while the drag ran is stale, even
        # when the last frame of the drag is the pose being kept.
        self._mesh_live = False
        if mesh is not None:
            self.camera.scene_radius = mesh.bounds.radius
            self.camera.scene_center = np.asarray(mesh.bounds.center, dtype=np.float64)
        self.mesh_changed.emit()

    def _refresh_parts(self) -> None:
        """Re-read how solid each part is drawn, without touching the geometry."""
        self.mesh_parts = [
            (obj, part, self.objects.opacity(obj, self.object_settings))
            for obj, part, _ in self.mesh_parts
        ]
        self.parts_changed.emit()

    def triangle_owner(self, triangle: int) -> SceneObject | None:
        """Which object a triangle of :attr:`mesh` belongs to, by its index."""
        start = 0
        for obj, part, _ in self.mesh_parts:
            if start <= triangle < start + part.triangle_count:
                return obj
            start += part.triangle_count
        return None

    # ------------------------------------------------------------------
    # Content
    # ------------------------------------------------------------------

    def load_mesh(self, path: str | Path, load_sidecar: bool = True) -> None:
        """Open a model as the whole scene: centre it on the origin and frame it.

        Everything the previous scene held -- other objects, marks, history
        -- goes.  :meth:`add_mesh` is the door for a model that is to stand
        beside what is already there.

        The current orientation carries over to the new model: files from one
        pipeline share an up axis, so having set it once is usually right, and
        the Model panel shows what is being applied.
        """
        path = Path(path)
        source = read_mesh(path)
        self.objects.clear()
        self.measurements.clear()
        self.annotations.clear()
        self.armatures.clear()
        self.forms.clear()
        self.skeletons.clear()
        self.bookmarks.clear()
        self.history.clear()
        obj = self._make_object(source, path)
        self.objects.add(obj)
        # A rigged model brings its skeleton in with it, bound to the skin
        # and standing at rest.
        if obj.rig is not None:
            self.skeletons.add(obj.rig.to_skeleton(path.stem))
        self._rebuild()
        self.frame_object()
        self.notify_objects()
        self.notify_measurements()
        self.notify_annotations()
        self.notify_armature()
        self.notify_forms()
        self.notify_skeleton()
        self.notify_bookmarks()
        self.history_changed.emit()
        self.adopt_units(obj.rest_mesh)
        self.status_message.emit(f"Loaded {path.name}: {self._describe(obj)}")
        if load_sidecar:
            companion = sidecar_path(path)
            if companion.is_file():
                self.load_session(companion, load_mesh=False)

    def add_mesh(self, path: str | Path, record: ObjectRecord | None = None) -> SceneObject:
        """Add a model to the scene, standing at the origin, and make it active.

        The scene it joins is left alone: the other objects, the marks on
        them and the history all stay.  A rigged model brings its skeleton.
        """
        path = Path(path)
        source = read_mesh(path)
        obj = self._make_object(source, path)
        if record is not None:
            self._describe_from(obj, record)
        else:
            obj.name = self.objects.next_name(obj.name)
        before = self.objects.snapshot()
        was_empty = not len(self.objects)
        self.objects.add(obj)
        skeleton = None
        if obj.rig is not None:
            skeleton = self.skeletons.add(obj.rig.to_skeleton(path.stem))
        if record is None:
            self._commit_objects(before, f"Add {obj.name}", skeleton=skeleton)
            self.notify_skeleton()
            if was_empty:
                self.frame_object()
                self.adopt_units(obj.rest_mesh)
            self.status_message.emit(f"Added {path.name}: {self._describe(obj)}")
        return obj

    def _make_object(self, source: Mesh, path: Path | None) -> SceneObject:
        rest = self._oriented(source)
        return SceneObject(source, rest, name=path.stem if path else source.name, path=path)

    @staticmethod
    def _describe(obj: SceneObject) -> str:
        mesh = obj.rest_mesh
        bones = "" if obj.rig is None else f", {obj.rig.joint_count} joints"
        return f"{mesh.vertex_count:,} vertices, {mesh.triangle_count:,} triangles{bones}"

    def _oriented(self, source: Mesh) -> Mesh:
        """Turn a freshly read mesh the right way up and centre it."""
        return source.transformed(self.orientation.matrix).recentered()

    def bound_skeleton(self) -> Skeleton | None:
        """The skeleton the active object follows, if it has one."""
        active = self.active_object
        if active is None or active.rig is None:
            return None
        return self._skeleton_for(active, set())

    # ------------------------------------------------------------------
    # Editing the objects
    # ------------------------------------------------------------------
    #
    # Every edit to the list -- a move, a parenting, a removal, a merge --
    # is recorded as the snapshot before and the snapshot after, so that one
    # command type covers them all and undoing any of them puts back the
    # whole list, parents and places included.  A skeleton bound to an
    # object is carried along with it in every case, by the change in the
    # object's world matrix.

    def snapshot_objects(self) -> Snapshot:
        """Where everything stands now; the start of a gesture keeps one."""
        return self.objects.snapshot()

    def _worlds(self) -> dict[int, np.ndarray]:
        return {id(obj): self.objects.world_matrix(obj) for obj in self.objects}

    def _carry_skeletons(self, before: dict[int, np.ndarray]) -> bool:
        """Move each bound skeleton by however far its object moved since ``before``."""
        moved = False
        claimed: set[int] = set()
        for obj in self.objects:
            skeleton = self._skeleton_for(obj, claimed)
            was = before.get(id(obj))
            if skeleton is None or was is None:
                continue
            now = self.objects.world_matrix(obj)
            if np.allclose(now, was):
                continue
            skeleton.carry(now @ np.linalg.inv(was))
            moved = True
        return moved

    def _restore_objects(self, snapshot: Snapshot) -> None:
        worlds = self._worlds()
        self.objects.restore(snapshot)
        if self._carry_skeletons(worlds):
            self.skeleton_changed.emit()
        self._rebuild()

    def restore_objects(self, snapshot: Snapshot) -> None:
        """Put the objects back as a snapshot had them -- how a gesture is cancelled."""
        self._restore_objects(snapshot)

    def _commit_objects(
        self,
        before: Snapshot,
        text: str,
        geometry: bool = True,
        skeleton: Skeleton | None = None,
    ) -> None:
        """Record the list as it is now against ``before``, and rebuild.

        ``geometry`` off is for an edit that changed only how solid
        something is drawn, which the renderer can take without a rebuild.
        """
        self.do(ObjectsEdit(self, self.objects.snapshot(), before, text, skeleton), apply=False)
        if geometry:
            self._rebuild()
        else:
            self._refresh_parts()

    def preview_transform(self, obj: SceneObject, transform: Transform) -> None:
        """Put ``obj`` at ``transform`` for the frames of a drag, without recording it."""
        worlds = self._worlds()
        obj.transform = transform
        if self._carry_skeletons(worlds):
            self.skeleton_changed.emit()
        self._rebuild(live=True)

    def commit_transform(self, obj: SceneObject, before: Snapshot, text: str | None = None) -> None:
        """Record a finished transform gesture, begun from ``before``."""
        text = text or f"Move {obj.name}"
        rows, _ = before
        held = next((row for row in rows if row[0] is obj), None)
        if held is not None and held[2] == obj.transform:
            # Let go where it began: nothing to record, but the live frames
            # deformed the scene, so the caches built on it are told to catch up.
            self._rebuild()
            return
        self._commit_objects(before, text)

    def set_transform(
        self, obj: SceneObject, transform: Transform, text: str | None = None
    ) -> None:
        """Put ``obj`` at ``transform`` as one undo step -- the panel's boxes."""
        if transform == obj.transform:
            return
        before = self.objects.snapshot()
        worlds = self._worlds()
        obj.transform = transform
        if self._carry_skeletons(worlds):
            self.skeleton_changed.emit()
        self._commit_objects(before, text or f"Move {obj.name}")

    def set_active(self, obj: SceneObject | None) -> None:
        """Make ``obj`` the active object.  Not an edit: nothing is undone."""
        if obj is self.active_object:
            return
        self.objects.set_active(obj)
        self.notify_objects()

    def rename_object(self, obj: SceneObject, name: str) -> None:
        name = name.strip()
        if not name or name == obj.name:
            return
        was = obj.name
        obj.name = name
        # A name is not in a snapshot; the command carries it itself.
        self.do(_RenameObject(obj, name, was), apply=False)

    def set_object_visible(self, obj: SceneObject, visible: bool) -> None:
        if bool(visible) == obj.visible:
            return
        before = self.objects.snapshot()
        obj.visible = bool(visible)
        self._commit_objects(before, f"{'Show' if visible else 'Hide'} {obj.name}")

    def preview_object_opacity(self, obj: SceneObject, opacity: float) -> None:
        """Set an object's solidity for the frames of a slider drag."""
        obj.opacity = min(max(float(opacity), 0.0), 1.0)
        self._refresh_parts()

    def set_object_opacity(
        self, obj: SceneObject, opacity: float, before: Snapshot | None = None
    ) -> None:
        """Record a solidity, from ``before`` if a drag began there."""
        before = before or self.objects.snapshot()
        obj.opacity = min(max(float(opacity), 0.0), 1.0)
        rows, _ = before
        held = next((row for row in rows if row[0] is obj), None)
        if held is not None and abs(held[4] - obj.opacity) < 1e-9:
            self._refresh_parts()
            return
        self._commit_objects(before, f"Ghost {obj.name}", geometry=False)

    def set_parent(self, obj: SceneObject, parent: SceneObject | None) -> bool:
        """Hang ``obj`` from ``parent`` -- or from nothing -- as one undo step."""
        if obj.parent is parent:
            return True
        before = self.objects.snapshot()
        worlds = self._worlds()
        if not self.objects.set_parent(obj, parent, self.object_settings.keep_transform):
            self.status_message.emit(f"{obj.name} cannot hang from something hung from it")
            return False
        if self._carry_skeletons(worlds):
            self.skeleton_changed.emit()
        text = f"Link {obj.name} to {parent.name}" if parent else f"Unlink {obj.name}"
        self._commit_objects(before, text)
        return True

    def remove_object(self, obj: SceneObject) -> None:
        before = self.objects.snapshot()
        worlds = self._worlds()
        gone = self.objects.remove(obj, self.object_settings)
        if not gone:
            return
        if self._carry_skeletons(worlds):
            self.skeleton_changed.emit()
        text = f"Remove {obj.name}"
        if len(gone) > 1:
            text += f" and {len(gone) - 1} more"
        self._commit_objects(before, text)

    def merge_objects(self, objects: list[SceneObject]) -> SceneObject | None:
        """Join several objects into one, standing where they stood."""
        objects = [obj for obj in objects if self.objects.index(obj) >= 0]
        if len(objects) < 2:
            self.status_message.emit("Pick two or more objects to merge")
            return None
        before = self.objects.snapshot()
        worlds = self._worlds()
        merged = merge_objects(self.objects, objects, name=self.objects.next_name("Merged"))
        # Hung where the first of them was; the children of any of them are
        # handed to the merged object, where they stood.
        standing = merged.transform.matrix
        parent = objects[0].parent
        while parent is not None and any(parent is obj for obj in objects):
            parent = parent.parent
        merged.parent = parent
        self.objects.set_world_matrix(merged, standing)
        self.objects.add(merged)
        for obj in objects:
            for child in self.objects.children(obj):
                if not any(child is held for held in objects):
                    self.objects.set_parent(child, merged, keep_transform=True)
        settings = ObjectSettings(remove_children=False)
        for obj in objects:
            self.objects.remove(obj, settings)
        self.objects.set_active(merged)
        if self._carry_skeletons(worlds):
            self.skeleton_changed.emit()
        self._commit_objects(before, f"Merge {len(objects)} objects")
        self.status_message.emit(
            f"Merged {len(objects)} objects into {merged.name}: {self._describe(merged)}"
        )
        return merged

    def split_object(self, obj: SceneObject) -> list[SceneObject]:
        """Break ``obj`` into its loose pieces, each an object of its own."""
        try:
            pieces = split_object(self.objects, obj)
        except ValueError as error:
            self.status_message.emit(str(error))
            return []
        if pieces is None:
            self.status_message.emit(f"{obj.name} is one piece already")
            return []
        before = self.objects.snapshot()
        worlds = self._worlds()
        for piece in pieces:
            piece.name = self.objects.next_name(piece.name)
            self.objects.add(piece, activate=False)
        # The children of the whole go to its largest piece.
        for child in self.objects.children(obj):
            self.objects.set_parent(child, pieces[0], keep_transform=True)
        self.objects.remove(obj, ObjectSettings(remove_children=False))
        self.objects.set_active(pieces[0])
        if self._carry_skeletons(worlds):
            self.skeleton_changed.emit()
        self._commit_objects(before, f"Split {obj.name}")
        self.status_message.emit(f"Split {obj.name} into {len(pieces)} pieces")
        return pieces

    def duplicate_object(self, obj: SceneObject) -> SceneObject | None:
        """A copy of ``obj``'s mesh on top of it, made active, as one undo step."""
        if self.objects.index(obj) < 0:
            return None
        before = self.objects.snapshot()
        copy = duplicate_object(self.objects, obj)
        self.objects.add(copy)
        self._commit_objects(before, f"Duplicate {obj.name}")
        self.status_message.emit(f"Duplicated {obj.name} as {copy.name}")
        return copy

    def notify_object_settings(self) -> None:
        """A parenting policy changed: what is shown and how solid may have too."""
        self.notify_objects()
        self._rebuild()

    # ------------------------------------------------------------------
    # Orientation
    # ------------------------------------------------------------------

    def set_orientation(self, orientation: OrientationSettings, move_marks: bool = True) -> None:
        """Turn the models, bringing the marks made on them along.

        Measurements, annotations, the armature and the forms belong to the
        model, so they are carried through the same rotation; a saved camera
        view is a viewpoint on the scene rather than a point on the model,
        and stays where it is.  With several objects the marks follow the
        active one, and each skeleton follows the object it is bound to.

        The turn is not recorded in the undo history: like the camera, it is a
        way of looking at the model rather than an edit to it, and choosing the
        previous orientation puts everything back exactly.
        """
        if not len(self.objects):
            self.orientation = orientation
            return

        was = self.orientation.matrix
        self.orientation = orientation
        change = self.orientation.matrix @ was.T
        active = self.active_object
        claimed: set[int] = set()
        for obj in self.objects:
            previous = obj.rest_mesh
            obj.rest_mesh = self._oriented(obj.source_mesh)
            obj.forget()
            if not move_marks:
                continue
            carry = self._carry_matrix(previous, obj.rest_mesh, change)
            world = self.objects.world_matrix(obj)
            carry_world = world @ carry @ np.linalg.inv(world)
            if obj is active:
                self._move_marks(carry_world)
            skeleton = self._skeleton_for(obj, claimed)
            if skeleton is not None:
                skeleton.carry(carry_world)
        self._rebuild()
        self.frame_object()
        self.notify_measurements()
        self.notify_annotations()
        self.notify_armature()
        self.notify_forms()
        self.skeleton_changed.emit()

    @staticmethod
    def _carry_matrix(previous: Mesh, current: Mesh, change: np.ndarray) -> np.ndarray:
        """The 4x4 that takes a point on the old rest mesh onto the new one.

        A point sits at ``rotation @ file_point - centre`` in both orientations,
        so going from one to the other means undoing the old centring, applying
        the change in rotation, and re-centring.
        """
        before = np.asarray(previous.source_offset, dtype=np.float64)
        after = np.asarray(current.source_offset, dtype=np.float64)
        carry = np.eye(4)
        carry[:3, :3] = change
        carry[:3, 3] = change @ before - after
        return carry

    def _move_marks(self, carry: np.ndarray) -> None:
        """Carry the measurements, annotations, armature and forms through ``carry``."""
        change = carry[:3, :3]

        def move(point) -> tuple[float, float, float]:
            moved = change @ np.asarray(point, dtype=np.float64) + carry[:3, 3]
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
        """Fit the scene in the view without changing the direction."""
        if self.mesh is not None:
            self.camera.frame(self.mesh.bounds)
            self.notify_camera()

    # ------------------------------------------------------------------
    # Sessions
    # ------------------------------------------------------------------

    def to_session(self) -> Session:
        first = next((obj for obj in self.objects if obj.path is not None), None)
        return Session(
            mesh_path=str(first.path) if first is not None else None,
            objects=records_for(self.objects),
            object_settings=self.object_settings,
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
        """Adopt a session's settings, leaving the loaded meshes alone."""
        self.render = session.render
        self.measurement_settings = session.measurement_settings
        self.navigation = session.navigation
        self.object_settings = session.object_settings
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
        # a model's own rig loose, is given it back at rest.
        claimed: set[int] = set()
        for obj in self.objects:
            if obj.rig is not None and self._skeleton_for(obj, claimed) is None:
                self.skeletons.add(obj.rig.to_skeleton(obj.path.stem if obj.path else obj.name))
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
        self._rebuild()
        self.notify_objects()
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

        An object with no file of its own -- merged out of several, or split
        off one -- is written out as an OBJ beside the session first, since
        a session names its objects by their files.
        """
        path = Path(path)
        written = self._write_loose_objects(path)
        session = self.to_session()
        session.layout = dict(layout or {})
        saved = session.save(path)
        note = "" if not written else f" (and {written} object file{'s' if written > 1 else ''})"
        self.status_message.emit(f"Saved session to {saved.name}{note}")
        return saved

    def _write_loose_objects(self, session_path: Path) -> int:
        count = 0
        for obj in self.objects:
            if obj.path is not None:
                continue
            stem = session_path.name
            for suffix in (".refview.json", ".json"):
                if stem.endswith(suffix):
                    stem = stem[: -len(suffix)]
                    break
            slug = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in obj.name)
            target = session_path.with_name(f"{stem}.{slug}.obj")
            # What is written is the object's own mesh, unturned: it is read
            # back through the same orientation as any other file.
            obj.path = save_mesh(self._unoriented(obj.rest_mesh), target)
            count += 1
        return count

    def _unoriented(self, rest: Mesh) -> Mesh:
        """A rest mesh as a file would store it, so that re-orienting it comes back to itself."""
        return rest.transformed(self.orientation.matrix.T)

    def load_session(self, path: str | Path, load_mesh: bool = True) -> None:
        session = Session.load(path)
        if load_mesh:
            self._load_session_objects(session)
        else:
            self._match_session_objects(session)
        self.apply_session(session)
        self.session_layout = dict(session.layout)
        self.status_message.emit(f"Loaded session {Path(path).name}")

    def _records(self, session: Session) -> list[ObjectRecord]:
        if session.objects:
            return list(session.objects)
        if session.mesh_path:
            return [ObjectRecord(name=Path(session.mesh_path).stem, path=session.mesh_path)]
        return []

    def _load_session_objects(self, session: Session) -> None:
        """Open every object a session names, as the whole scene."""
        records = self._records(session)
        loadable = [r for r in records if r.path and Path(r.path).is_file()]
        if not loadable:
            return
        first = loadable[0]
        self.load_mesh(first.path, load_sidecar=False)
        primary = self.active_object
        if primary is not None:
            self._describe_from(primary, first)
        made: dict[int, SceneObject] = {
            next(i for i, r in enumerate(records) if r is first): primary
        }
        missing = 0
        for index, record in enumerate(records):
            if record is first:
                continue
            if not record.path or not Path(record.path).is_file():
                missing += 1
                continue
            try:
                made[index] = self.add_mesh(record.path, record)
            except (MeshLoadError, OSError):
                missing += 1
        self._hang_records(records, made)
        self.objects.set_active(primary)
        if missing:
            self.status_message.emit(
                f"{missing} object file(s) named by the session were not found"
            )

    def _match_session_objects(self, session: Session) -> None:
        """Lay a session's object records over the objects already open.

        For the sidecar opened beside a model: the model is already in, so
        its record is matched by file and applied to it, and any other
        object the session names is added.  A record no open object answers
        to by file falls to the active object if that has none of its own
        -- the session was saved beside it, whatever it is called now.
        """
        records = self._records(session)
        if not records:
            return
        held = {_same_file(obj.path): obj for obj in self.objects if obj.path is not None}
        made: dict[int, SceneObject] = {}
        for index, record in enumerate(records):
            obj = held.pop(_same_file(record.path), None) if record.path else None
            if obj is not None:
                self._describe_from(obj, record)
                made[index] = obj
        active = self.active_object
        if active is not None and not any(obj is active for obj in made.values()):
            index = next((i for i, r in enumerate(records) if i not in made), None)
            if index is not None:
                self._describe_from(active, records[index])
                made[index] = active
        for index, record in enumerate(records):
            if index in made or not record.path or not Path(record.path).is_file():
                continue
            try:
                made[index] = self.add_mesh(record.path, record)
            except (MeshLoadError, OSError):
                continue
        self._hang_records(records, made)

    @staticmethod
    def _describe_from(obj: SceneObject, record: ObjectRecord) -> None:
        obj.name = record.name or obj.name
        obj.transform = record.transform
        obj.visible = bool(record.visible)
        obj.opacity = float(record.opacity)

    def _hang_records(self, records: list[ObjectRecord], made: dict[int, SceneObject]) -> None:
        for index, record in enumerate(records):
            child = made.get(index)
            parent = made.get(record.parent) if record.parent >= 0 else None
            if child is not None and parent is not None:
                self.objects.set_parent(child, parent, keep_transform=False)

    def default_session_path(self) -> Path | None:
        return sidecar_path(self.mesh_path) if self.mesh_path else None


class _RenameObject(Command):
    def __init__(self, obj: SceneObject, name: str, was: str) -> None:
        super().__init__(f"Rename {was}", OBJECTS)
        self._obj, self._name, self._was = obj, name, was

    def apply(self) -> None:
        self._obj.name = self._name

    def revert(self) -> None:
        self._obj.name = self._was


def _same_file(path) -> str:
    """A path as a key two spellings of one file agree on."""
    try:
        return str(Path(path).resolve()).lower()
    except OSError:  # pragma: no cover - a path the system will not look at
        return str(path).lower()
