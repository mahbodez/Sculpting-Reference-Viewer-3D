"""Placing and editing the nodes of an armature, freehand or led by a preset.

Freehand, a click drops a node and joins it to the last one, so a chain draws
by clicking along it.  Led by a preset, the same click records the landmark the
panel is currently asking for, and the armature is rebuilt from everything
placed so far -- the artist sees the figure assemble as they go rather than at
the end.

A landmark already placed is grabbable in the same way a node is, which is the
only way to correct one: the wire is derived from the landmarks, so nudging the
node a mis-placed landmark produced would throw the preset away to fix a point
the preset could have rebuilt itself.

Nothing here touches the document.  The tool works out what the edit *is* and
the viewport hands it to the undo history, which is what keeps a whole preset
run, or a single dragged node or landmark, to one step.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

import numpy as np

from ..core.armature import Armature, ArmatureNode, ArmatureSettings, Bone, PlacedLandmark
from ..core.landmarks import PRESETS, Landmark, Preset, mirror_landmarks, rebuild
from .picking import SurfacePicker

#: A node, as ``(index in the store, index in the armature)``.
Handle = tuple[int, int]
#: A bone, in the same shape.
BoneRef = tuple[int, int]
#: A placed landmark, as ``(index in the store, the preset's key for it)``.
#: Keyed rather than numbered because a landmark list is re-derived rather than
#: edited in place, and the row the panel is showing has to survive that.
LandmarkRef = tuple[int, str]


@dataclass
class GuideRun:
    """A guided preset part-way through.

    The index walks the preset's own list rather than the shortened one the
    panel shows, so turning mirroring off half way through simply reveals the
    steps that were being skipped instead of losing the artist's place.
    """

    preset: str
    index: int = 0
    #: Which armature in the store the run is building into.
    armature: int = -1
    #: Landmarks the artist chose to pass over.
    skipped: set[str] = field(default_factory=set)

    @property
    def spec(self) -> Preset | None:
        return PRESETS.get(self.preset)


class ArmatureTool:
    """Turns clicks into nodes, and drags into moved or resized ones.

    The tool stays armed after each node so a chain can be drawn in one go;
    Escape drops the selection without disarming.  Editing an existing node is
    separate: an unlocked node can be moved whether or not the tool is armed,
    which is what makes the padlock in the list worth having.
    """

    def __init__(self) -> None:
        self.active = False
        #: The node a new one will be joined to, and the one the panel edits.
        self.selected: Handle | None = None
        #: The landmark the panel's list is editing, highlighted in the view so
        #: the row and the cross on the model are obviously the same point.
        self.selected_landmark: LandmarkRef | None = None
        self.hover_point: np.ndarray | None = None
        #: Node under the cursor, highlighted so it looks grabbable.
        self.hover_handle: Handle | None = None
        #: Landmark under the cursor, highlighted for the same reason.
        self.hover_landmark: LandmarkRef | None = None
        #: Bone under the cursor, so its length can be shown on hover.
        self.hover_bone: BoneRef | None = None
        #: Node currently being dragged.
        self.grabbed_handle: Handle | None = None
        #: Landmark currently being dragged.
        self.grabbed_landmark: LandmarkRef | None = None
        #: Whether that drag is changing the node's thickness rather than its place.
        self.resizing = False
        self.guide: GuideRun | None = None

    # -- state ----------------------------------------------------------

    def set_active(self, active: bool) -> None:
        self.active = active
        if not active:
            self.cancel()

    def cancel(self) -> None:
        """Drop the hover preview and the chain, leaving any guided run alone.

        Escape means "stop drawing from here", not "throw away the landmarks I
        spent ten minutes placing"; ending a run is the panel's Cancel button.
        """
        self.selected = None
        self.hover_point = None

    def end_guide(self) -> None:
        self.guide = None

    @property
    def guiding(self) -> bool:
        return self.guide is not None

    # -- the guided walk -------------------------------------------------

    def start_guide(self, preset: str, armature: int) -> GuideRun | None:
        """Begin a preset run against an armature already in the store."""
        if preset not in PRESETS:
            return None
        self.guide = GuideRun(preset=preset, armature=armature)
        return self.guide

    def remaining(self, armature: Armature, settings: ArmatureSettings) -> list[Landmark]:
        """The landmarks still to place, in order, the current one first."""
        run = self.guide
        spec = run.spec if run is not None else None
        if run is None or spec is None:
            return []
        done = {entry.key for entry in armature.landmarks}
        return [
            entry
            for position, entry in enumerate(spec.landmarks)
            if position >= run.index
            and entry.key not in done
            and entry.key not in run.skipped
            and not (settings.mirror and entry.mirror_of)
        ]

    def current(self, armature: Armature, settings: ArmatureSettings) -> Landmark | None:
        """The landmark the artist is being asked for right now."""
        remaining = self.remaining(armature, settings)
        return remaining[0] if remaining else None

    def progress(self, armature: Armature, settings: ArmatureSettings) -> tuple[int, int]:
        """How many landmarks are placed, out of how many will be asked for."""
        run = self.guide
        spec = run.spec if run is not None else None
        if run is None or spec is None:
            return (0, 0)
        wanted = [
            entry
            for entry in spec.landmarks
            if entry.key not in run.skipped and not (settings.mirror and entry.mirror_of)
        ]
        done = {entry.key for entry in armature.landmarks}
        return (sum(1 for entry in wanted if entry.key in done), len(wanted))

    def skip(self, armature: Armature, settings: ArmatureSettings) -> None:
        """Pass over the landmark being asked for; the figure loses what it fed."""
        entry = self.current(armature, settings)
        if entry is not None and self.guide is not None:
            self.guide.skipped.add(entry.key)

    def back(self, armature: Armature, settings: ArmatureSettings) -> str | None:
        """Un-skip or un-place the landmark before this one, and ask again.

        Returns the key that was taken back, so the caller can drop it from the
        armature within the same undo step.
        """
        run = self.guide
        spec = run.spec if run is not None else None
        if run is None or spec is None:
            return None
        current = self.current(armature, settings)
        limit = next(
            (i for i, entry in enumerate(spec.landmarks) if current and entry.key == current.key),
            len(spec.landmarks),
        )
        done = {entry.key for entry in armature.landmarks}
        for entry in reversed(spec.landmarks[:limit]):
            if settings.mirror and entry.mirror_of:
                continue
            if entry.key in run.skipped:
                run.skipped.discard(entry.key)
                return entry.key
            if entry.key in done:
                return entry.key
        return None

    # -- picking --------------------------------------------------------

    def pick(
        self,
        x: float,
        y: float,
        picker: SurfacePicker,
        settings: ArmatureSettings,
    ) -> np.ndarray | None:
        """Where a click at ``(x, y)`` would put a node.

        With free placement the node lands on the camera-facing plane through
        the object centre, so the wire is not confined to the skin; otherwise
        it must hit the model and may snap to the nearest vertex.
        """
        if settings.free_placement:
            return picker.plane_point(x, y, picker.camera.scene_center)
        return picker.point(x, y, snap=settings.snap_to_vertex, snap_pixels=settings.snap_pixels)

    def drag_target(
        self,
        x: float,
        y: float,
        picker: SurfacePicker,
        settings: ArmatureSettings,
        current: np.ndarray,
    ) -> np.ndarray:
        """Where a grabbed node should move to.

        Free placement -- and a drag that wanders off the model -- slides the
        node across the plane it already sits on, so it never jumps to a
        surface the artist did not aim at.
        """
        if not settings.free_placement:
            point = picker.point(
                x, y, snap=settings.snap_to_vertex, snap_pixels=settings.snap_pixels
            )
            if point is not None:
                return point
        return picker.plane_point(x, y, current)

    def size_target(self, x: float, y: float, picker: SurfacePicker, node: ArmatureNode) -> float:
        """The thickness a resize drag is asking for: the cursor's reach, in world units."""
        distance = picker.screen_distance(node.at, x, y)
        if distance is None:
            return node.size
        depth = float(np.linalg.norm(node.point - picker.camera.eye))
        return max(distance * picker.world_per_pixel(depth), 0.0)

    # -- node handles ---------------------------------------------------

    def handle_at(
        self,
        x: float,
        y: float,
        armatures,
        picker: SurfacePicker,
        settings: ArmatureSettings,
    ) -> Handle | None:
        """The nearest grabbable node under the cursor, if any.

        Only unlocked nodes of a visible armature offer handles; everything
        else is inert, so orbiting across the wire never disturbs it.
        """
        if not settings.show_all:
            return None
        best: Handle | None = None
        best_distance = settings.handle_radius + 4.0
        for outer, armature in enumerate(armatures):
            if not armature.visible:
                continue
            for inner, node in enumerate(armature.nodes):
                if node.locked:
                    continue
                distance = picker.screen_distance(node.at, x, y)
                if distance is not None and distance <= best_distance:
                    best, best_distance = (outer, inner), distance
        return best

    #: A landmark is picked within a tighter reach than a node, which is what
    #: settles the two when they overlap -- and they do, since half the nodes of
    #: a preset are worked out from landmarks lying right beside them.  Aim at
    #: the cross and the cross is what comes up; a few pixels out and the node
    #: does.
    LANDMARK_REACH = 7.0

    def landmark_at(
        self,
        x: float,
        y: float,
        armatures,
        picker: SurfacePicker,
        settings: ArmatureSettings,
    ) -> LandmarkRef | None:
        """The nearest grabbable landmark under the cursor, if any.

        Only the ones actually on screen offer a grip, for the same reason the
        nodes do: nothing invisible should move when the cursor crosses it.  A
        mirrored guess is included -- taking hold of one is how the artist says
        it was a bad guess, and :meth:`Armature.with_landmark_at` clears the
        flag for them.
        """
        if not settings.show_all or not settings.show_landmarks:
            return None
        best: LandmarkRef | None = None
        best_distance = self.LANDMARK_REACH
        for outer, armature in enumerate(armatures):
            if not armature.visible:
                continue
            for landmark in armature.landmarks:
                distance = picker.screen_distance(landmark.at, x, y)
                if distance is not None and distance <= best_distance:
                    best, best_distance = (outer, landmark.key), distance
        return best

    def bone_at(
        self,
        x: float,
        y: float,
        armatures,
        picker: SurfacePicker,
        settings: ArmatureSettings,
    ) -> BoneRef | None:
        """The nearest bone under the cursor, for showing its length."""
        if not settings.show_all:
            return None
        best: BoneRef | None = None
        best_distance = settings.bone_width + 6.0
        for outer, armature in enumerate(armatures):
            if not armature.visible:
                continue
            for inner, bone in enumerate(armature.bones):
                ends = armature.bone_ends(bone)
                if ends is None:
                    continue
                distance = _segment_distance(
                    _project(picker, ends[0]), _project(picker, ends[1]), (x, y)
                )
                if distance is not None and distance <= best_distance:
                    best, best_distance = (outer, inner), distance
        return best

    def split_point(
        self, armature: Armature, bone: Bone, x: float, y: float, picker: SurfacePicker
    ) -> np.ndarray | None:
        """Where on a bone a click at ``(x, y)`` landed.

        The share along the bone is read in screen space, where the cursor
        actually is, and then used to walk the same share along the bone in
        three dimensions -- so the new node lands on the wire the artist
        clicked rather than on the surface behind it.
        """
        ends = armature.bone_ends(bone)
        if ends is None:
            return None
        start, end = _project(picker, ends[0]), _project(picker, ends[1])
        if start is None or end is None:
            return None
        share = _segment_share(start, end, (x, y))
        return ends[0] + (ends[1] - ends[0]) * share

    def insert_on_bone(
        self, armature: Armature, index: int, point: np.ndarray
    ) -> tuple[list[ArmatureNode], list[Bone], list[PlacedLandmark]] | None:
        """Drop a new node into the middle of a bone, taking its thickness from the ends."""
        if not 0 <= index < len(armature.bones):
            return None
        bone = armature.bones[index]
        ends = armature.bone_ends(bone)
        if ends is None:
            return None
        share = _share_between(ends[0], ends[1], point)
        first, second = armature.nodes[bone.a], armature.nodes[bone.b]
        node = ArmatureNode(
            name=f"Node {len(armature.nodes) + 1}",
            at=tuple(float(value) for value in point),
            size=first.size + (second.size - first.size) * share,
        )
        nodes, bones = armature.split_bone(index, node)
        return nodes, bones, list(armature.landmarks)

    def join(
        self, armature: Armature, first: int, second: int
    ) -> tuple[list[ArmatureNode], list[Bone], list[PlacedLandmark]] | None:
        """Run a bone between two nodes, or ``None`` when there is nothing to add."""
        if first == second:
            return None
        nodes, bones = armature.with_bone(first, second)
        if len(bones) == len(armature.bones):
            return None
        return nodes, bones, list(armature.landmarks)

    # -- gestures -------------------------------------------------------

    def place(
        self,
        armature: Armature,
        point: np.ndarray,
        settings: ArmatureSettings,
    ) -> tuple[list[ArmatureNode], list[Bone], list[PlacedLandmark]] | None:
        """What the armature becomes when a picked point is dropped into it.

        Returns the three lists to write in one command, or ``None`` when the
        click had nothing to do -- a guided run with every landmark already
        placed, say.
        """
        if self.guiding:
            return self._place_landmark(armature, point, settings)
        return self._place_node(armature, point)

    def _place_node(
        self, armature: Armature, point: np.ndarray
    ) -> tuple[list[ArmatureNode], list[Bone], list[PlacedLandmark]]:
        anchor = None
        if self.selected is not None and self.selected[1] < len(armature.nodes):
            anchor = self.selected[1]
        node = ArmatureNode(
            name=f"Node {len(armature.nodes) + 1}",
            at=tuple(float(value) for value in point),
            size=armature.default_size(),
        )
        nodes, bones = armature.with_node(node, connect_to=anchor)
        return nodes, bones, list(armature.landmarks)

    def _place_landmark(
        self, armature: Armature, point: np.ndarray, settings: ArmatureSettings
    ) -> tuple[list[ArmatureNode], list[Bone], list[PlacedLandmark]] | None:
        entry = self.current(armature, settings)
        if entry is None:
            return None
        landmarks = [existing for existing in armature.landmarks if existing.key != entry.key]
        landmarks.append(
            PlacedLandmark(key=entry.key, at=tuple(float(value) for value in point))
        )
        return self.derive(armature, landmarks, settings)

    def derive(
        self,
        armature: Armature,
        landmarks: list[PlacedLandmark],
        settings: ArmatureSettings,
    ) -> tuple[list[ArmatureNode], list[Bone], list[PlacedLandmark]]:
        """Mirror what is missing, then rebuild the figure from the whole set.

        The landmarks are copied first.  Mirroring moves an existing guess in
        place, and the list handed in is usually built out of the document's
        own entries -- writing through them would reach past the undo history,
        which keeps the *lists* but not what they point at.
        """
        proxy = Armature(
            nodes=list(armature.nodes),
            bones=list(armature.bones),
            landmarks=[replace(entry) for entry in landmarks],
            preset=armature.preset,
        )
        if settings.mirror:
            proxy.landmarks = mirror_landmarks(proxy)
        built = rebuild(proxy)
        if built is None:
            return list(armature.nodes), list(armature.bones), proxy.landmarks
        nodes, bones = built
        return nodes, bones, proxy.landmarks


# ----------------------------------------------------------------------
# Screen-space geometry
# ----------------------------------------------------------------------


def _project(picker: SurfacePicker, point) -> tuple[float, float] | None:
    """A world point in widget pixels, or ``None`` when it is behind the camera."""
    point = np.asarray(point, dtype=np.float64)
    if float(np.dot(point - picker.camera.eye, picker.camera.forward)) <= 0.0:
        return None
    screen_x, screen_y, _ = picker.camera.project(point, picker.width, picker.height)
    return (screen_x, screen_y)


def _segment_share(start, end, cursor) -> float:
    """How far along a screen-space segment the cursor's nearest point lies."""
    first = np.asarray(start, dtype=np.float64)
    second = np.asarray(end, dtype=np.float64)
    at = np.asarray(cursor, dtype=np.float64)
    along = second - first
    span = float(np.dot(along, along))
    if span <= 0.0:
        return 0.0
    return min(max(float(np.dot(at - first, along)) / span, 0.0), 1.0)


def _share_between(start, end, point) -> float:
    """The same question in three dimensions, for interpolating along a bone."""
    along = np.asarray(end, dtype=np.float64) - np.asarray(start, dtype=np.float64)
    span = float(np.dot(along, along))
    if span <= 0.0:
        return 0.0
    offset = np.asarray(point, dtype=np.float64) - np.asarray(start, dtype=np.float64)
    return min(max(float(np.dot(offset, along)) / span, 0.0), 1.0)


def _segment_distance(start, end, cursor) -> float | None:
    """Pixels from the cursor to the segment, or ``None`` if either end is behind."""
    if start is None or end is None:
        return None
    first = np.asarray(start, dtype=np.float64)
    second = np.asarray(end, dtype=np.float64)
    at = np.asarray(cursor, dtype=np.float64)
    along = second - first
    span = float(np.dot(along, along))
    if span <= 0.0:
        return float(np.linalg.norm(at - first))
    share = _segment_share(first, second, at)
    return float(np.linalg.norm(at - (first + share * along)))
