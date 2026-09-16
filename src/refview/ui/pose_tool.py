"""Posing a skeleton with the mouse, and building one by clicking.

The gesture is the one a figure is posed with in 3ds Max once a bone is
picked: take hold of a joint and pull, and the bone above it swings to follow
the cursor, carrying everything below.  Nothing is solved for -- there is no
IK -- because a pose is worked out from the trunk outwards, and swinging one
bone at a time is how an artist thinks about it.  A root has no bone above
it, so pulling a root moves the whole figure.  Shift rolls the held joint
about its own bone instead, which is the one turn a swing cannot make.  In
*fit* mode the same pull moves where the joint rests, and its children stay
put, so a preset can be pulled into the model joint by joint.

With the tool armed, a click that lands on nothing adds a joint under the
selected one, so a chain is built by clicking along it, as an armature is.

Nothing here touches the document: each method works out what the edit is
and hands the answer back, and the viewport records it through the history.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..core.linalg import (
    matrix_to_quat,
    quat_between,
    quat_from_axis_angle,
    quat_to_matrix,
    vec3,
)
from ..core.skeleton import Joint, Skeleton, SkeletonSettings, make_joint, normalized_rotation
from .picking import SurfacePicker

#: A joint, as ``(index in the store, index in the skeleton)``.
JointRef = tuple[int, int]


@dataclass(frozen=True)
class Swing:
    """What a pull on a joint does to its parent: ``joint`` is the one held."""

    parent: int
    rotation: tuple[float, float, float, float]


class PoseTool:
    """Turns pulls on joints into pose edits, and clicks into new joints."""

    #: A bone is picked within this many pixels of its line, over the width.
    BONE_REACH = 5.0

    def __init__(self) -> None:
        self.active = False
        #: The joint the panel edits, and the one a new joint hangs from.
        self.selected: JointRef | None = None
        self.hover_joint: JointRef | None = None
        #: The bone under the cursor, by the joint at its far end.
        self.hover_bone: JointRef | None = None
        self.hover_point: np.ndarray | None = None
        #: The joint being pulled, and how.
        self.grabbed: JointRef | None = None
        self.mode: str = ""

    # -- state ----------------------------------------------------------

    def set_active(self, active: bool) -> None:
        self.active = active
        if not active:
            self.cancel()

    def cancel(self) -> None:
        self.hover_point = None
        self.grabbed = None
        self.mode = ""

    # -- picking --------------------------------------------------------

    def pick(
        self, x: float, y: float, picker: SurfacePicker, settings: SkeletonSettings
    ) -> np.ndarray | None:
        """Where a click at ``(x, y)`` would put a new joint."""
        if settings.free_placement:
            return picker.plane_point(x, y, picker.camera.scene_center)
        point = picker.point(x, y, snap=settings.snap_to_vertex, snap_pixels=settings.snap_pixels)
        return point if point is not None else picker.plane_point(x, y, picker.camera.scene_center)

    def drag_target(
        self, x: float, y: float, picker: SurfacePicker, current: np.ndarray
    ) -> np.ndarray:
        """Where a pulled joint is being pulled to.

        Across the camera-facing plane through where it is, so a swing
        stays in the picture plane unless Ctrl is held, which pulls it in
        depth along the rail instead.  Never the surface: a joint is under
        the skin, and snapping it to the skin would throw every pull off.
        """
        if picker.depth_drag is not None:
            return picker.depth_drag.target(y)
        return picker.plane_point(x, y, current)

    def joint_at(
        self,
        x: float,
        y: float,
        skeletons,
        picker: SurfacePicker,
        settings: SkeletonSettings,
    ) -> JointRef | None:
        """The nearest unlocked joint of a visible skeleton under the cursor."""
        if not settings.show_all:
            return None
        best: JointRef | None = None
        best_distance = settings.handle_radius + 4.0
        for outer, skeleton in enumerate(skeletons):
            if not skeleton.visible or not skeleton.joints:
                continue
            screen = _project_many(picker, skeleton.positions())
            for inner, at in enumerate(screen):
                if at is None or skeleton.joints[inner].locked:
                    continue
                distance = float(np.hypot(at[0] - x, at[1] - y))
                if distance <= best_distance:
                    best, best_distance = (outer, inner), distance
        return best

    def bone_at(
        self,
        x: float,
        y: float,
        skeletons,
        picker: SurfacePicker,
        settings: SkeletonSettings,
    ) -> JointRef | None:
        """The bone under the cursor, named by the joint at its far end.

        Taking hold of a bone is taking hold of its far end: pulling the
        forearm is pulling the wrist, which is what swings the elbow.
        """
        if not settings.show_all:
            return None
        best: JointRef | None = None
        best_distance = settings.bone_width + self.BONE_REACH
        for outer, skeleton in enumerate(skeletons):
            if not skeleton.visible or not skeleton.joints:
                continue
            screen = _project_many(picker, skeleton.positions())
            for parent, child in skeleton.bones():
                if skeleton.joints[child].locked:
                    continue
                distance = _segment_distance(screen[parent], screen[child], (x, y))
                if distance is not None and distance <= best_distance:
                    best, best_distance = (outer, child), distance
        return best

    # -- the pose ---------------------------------------------------------

    def swing(self, skeleton: Skeleton, index: int, target) -> Swing | None:
        """The turn the parent takes so that joint ``index`` points at ``target``.

        The shortest turn in the scene carrying the bone's present direction
        onto the direction of the target, re-expressed in the parent's own
        rest frame, where its pose lives.  The bone keeps its length: the
        target says which way, not how far.
        """
        if not 0 <= index < len(skeleton.joints):
            return None
        joint = skeleton.joints[index]
        parent = joint.parent
        if not 0 <= parent < len(skeleton.joints) or skeleton.joints[parent].locked:
            return None
        world = skeleton.world_matrices()
        pivot = world[parent][:3, 3]
        now = world[index][:3, 3] - pivot
        wanted = np.asarray(target, dtype=np.float64) - pivot
        if np.linalg.norm(now) < 1e-12 or np.linalg.norm(wanted) < 1e-12:
            return None
        delta = quat_to_matrix(quat_between(now, wanted))
        return Swing(parent, self._turned(skeleton, world, parent, delta))

    def twist(
        self, skeleton: Skeleton, index: int, pixels: float, settings: SkeletonSettings
    ) -> tuple[float, float, float, float] | None:
        """The rotation joint ``index`` takes after rolling about its own bone."""
        if not 0 <= index < len(skeleton.joints):
            return None
        world = skeleton.world_matrices()
        axis = self.bone_axis(skeleton, index, world)
        angle = np.radians(float(pixels) * settings.twist_per_pixel)
        delta = quat_to_matrix(quat_from_axis_angle(axis, angle))
        return self._turned(skeleton, world, index, delta)

    def move(self, skeleton: Skeleton, index: int, target) -> tuple[float, float, float] | None:
        """The pose shift that puts joint ``index`` at ``target``, children and all."""
        if not 0 <= index < len(skeleton.joints):
            return None
        frame = self._frame(skeleton, skeleton.world_matrices(), index)
        local = np.linalg.inv(frame) @ np.array([*np.asarray(target, dtype=np.float64), 1.0])
        return tuple(float(v) for v in local[:3])

    def fit(self, skeleton: Skeleton, index: int, target) -> list[Joint]:
        """The joint list with ``index`` resting at ``target`` and its children left be."""
        return skeleton.with_rest_at(index, target)

    def bone_axis(self, skeleton: Skeleton, index: int, world=None) -> np.ndarray:
        """Which way the bone at joint ``index`` runs, in the scene.

        Towards its first child, or -- for a hand, a crown, any end of a
        chain -- away from its parent.  A lone joint rolls about the
        scene's up, which is as good an answer as there is.
        """
        world = skeleton.world_matrices() if world is None else world
        at = world[:, :3, 3]
        children = skeleton.children(index)
        parent = skeleton.joints[index].parent
        if children:
            axis = at[children[0]] - at[index]
        elif 0 <= parent < len(skeleton.joints):
            axis = at[index] - at[parent]
        else:
            axis = vec3(0.0, 1.0, 0.0)
        length = float(np.linalg.norm(axis))
        return axis / length if length > 1e-12 else vec3(0.0, 1.0, 0.0)

    @staticmethod
    def _frame(skeleton: Skeleton, world: np.ndarray, index: int) -> np.ndarray:
        """The frame a joint's pose is written in: its parent's, then its rest."""
        joint = skeleton.joints[index]
        parent = joint.parent
        above = world[parent] if 0 <= parent < len(skeleton.joints) else np.eye(4)
        return above @ joint.rest_matrix

    def _turned(
        self, skeleton: Skeleton, world: np.ndarray, index: int, delta: np.ndarray
    ) -> tuple[float, float, float, float]:
        """Joint ``index``'s pose rotation after a scene-space turn ``delta``."""
        frame = self._frame(skeleton, world, index)[:3, :3]
        present = quat_to_matrix(skeleton.joints[index].rotation)
        turned = np.linalg.inv(frame) @ delta @ frame @ present
        return normalized_rotation(matrix_to_quat(turned))

    # -- building ---------------------------------------------------------

    def place(self, skeleton: Skeleton, point, parent: int = -1) -> list[Joint]:
        """The joint list with a new joint at ``point``, hung from ``parent``.

        A root when ``parent`` names no joint.  Written against the parent
        as it stands, pose and all, so the joint appears exactly where the
        click was; the rest frame carries no turn of its own, so its
        sliders read as scene turns.
        """
        if not 0 <= parent < len(skeleton.joints):
            parent = -1
        target = np.asarray(point, dtype=np.float64)
        name = f"Joint {len(skeleton.joints) + 1}"
        if parent >= 0:
            frame = skeleton.world_matrices()[parent]
            local = (np.linalg.inv(frame) @ np.array([*target, 1.0]))[:3]
            joint = make_joint(name, parent, local)
        else:
            joint = make_joint(name, -1, target)
        joint.radius = skeleton.default_radius()
        return skeleton.with_joint(joint)


# ----------------------------------------------------------------------
# Screen-space geometry
# ----------------------------------------------------------------------


def _project_many(picker: SurfacePicker, points) -> list[tuple[float, float] | None]:
    """Every point in widget pixels, ``None`` where one is behind the camera."""
    points = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    camera = picker.camera
    ahead = (points - camera.eye) @ camera.forward > 0.0
    xs, ys, _ = camera.project_many(points, picker.width, picker.height)
    return [
        (float(sx), float(sy)) if ok else None for sx, sy, ok in zip(xs, ys, ahead, strict=True)
    ]


def _segment_distance(start, end, cursor) -> float | None:
    if start is None or end is None:
        return None
    first = np.asarray(start, dtype=np.float64)
    second = np.asarray(end, dtype=np.float64)
    at = np.asarray(cursor, dtype=np.float64)
    along = second - first
    span = float(np.dot(along, along))
    if span <= 0.0:
        return float(np.linalg.norm(at - first))
    share = min(max(float(np.dot(at - first, along)) / span, 0.0), 1.0)
    return float(np.linalg.norm(at - (first + share * along)))
