"""A graph of named points under the form, and the wire it stands for.

An armature here is not a skeleton in the sense a DCC application means it:
nothing is animated, nothing is skinned, no weights are ever painted.  It is a
guide.  The artist reads the nodes off the screen while bending wire, and the
clay modes read them to find out where the masses of a figure actually are
rather than inferring it from the distance field alone.

Bones hold indices into :attr:`Armature.nodes` rather than identifiers, which is
only safe because every structural edit rewrites both lists together in a single
undo command.  The helpers below therefore all return new lists instead of
mutating in place: the caller hands the pair to one ``SetAttributes`` and the
graph is never half-rewritten.

Edges connect whichever nodes the artist joins, so a general graph rather than a
strict tree: a shoulder girdle or a pelvic bar closes a loop, and refusing that
would make the wire it stands for impossible to describe.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum

import numpy as np

Color = tuple[float, float, float]
Point3 = tuple[float, float, float]

#: A hand-placed node is given this share of the armature's longest bone as its
#: thickness, so a freehand ring starts at a plausible size rather than at zero.
DEFAULT_SIZE_SHARE = 0.08


class BoneLabels(str, Enum):
    """When the length of a bone is written beside it."""

    NEVER = "never"
    HOVER = "hover"
    ALWAYS = "always"

    @property
    def label(self) -> str:
        return {
            BoneLabels.NEVER: "Never",
            BoneLabels.HOVER: "On hover",
            BoneLabels.ALWAYS: "Always",
        }[self]


class Buried(str, Enum):
    """What becomes of the part of the armature the model is standing in front of.

    An armature lives inside the form, so hiding the buried part would hide
    almost all of it.  Dimming keeps it readable while still saying which side
    of the surface it is on.
    """

    SHOW = "show"
    DIM = "dim"

    @property
    def label(self) -> str:
        return {
            Buried.SHOW: "Draw at full strength",
            Buried.DIM: "Dim behind the surface",
        }[self]


@dataclass
class ArmatureNode:
    """One joint of the wire: where it is, and how thick the form is there."""

    name: str = "Node"
    at: Point3 = (0.0, 0.0, 0.0)
    #: How thick the form is at this joint, as a radius in scene units.  Zero
    #: means unset, and the node draws as a flat dot rather than a ring.  It is
    #: world-space rather than pixels because it is a fact about the figure:
    #: it is what a guided preset measures off its paired landmarks, and what
    #: the clay modes will later read to size a lump.
    size: float = 0.0
    #: Which slot of a preset this node fills, such as ``"hip.L"``; empty on a
    #: hand-made node.  Re-deriving a preset matches on this, so a renamed node
    #: keeps the name the artist gave it.
    role: str = ""
    #: A locked node ignores the mouse, and keeps its place and size through a
    #: re-derive.  One padlock, one meaning: leave this one alone.
    locked: bool = False

    @property
    def point(self) -> np.ndarray:
        return np.asarray(self.at, dtype=np.float64)


@dataclass
class Bone:
    """A length of wire between two nodes, by their index in the armature.

    A bone carries a name of its own rather than borrowing the names of the two
    nodes it runs between, because the two say different things: the nodes of a
    figure are joints, and the bones are the masses slung between them.  What a
    sculptor lays down is a *thigh*, not a *hip to knee*.  The clay mode lays
    one lump per bone in the order the bones are listed, so this name is what
    the artist reorders and what the panel shows them reordering.  Empty on a
    hand-drawn bone, where the two node names are the best anyone can do; see
    :meth:`Armature.bone_name`.
    """

    a: int
    b: int
    name: str = ""
    #: Whether the clay mode lays a lump along this bone.  A bone turned off
    #: is still wire -- it is drawn, it is measured, it holds the nodes at its
    #: ends apart -- it simply takes no clay, which is what an artist wants
    #: for the parts of a figure they mean to model rather than block in, and
    #: for a bone that stands for a direction rather than for a mass.  What
    #: the clay then does with that part of the form is what it did before
    #: there was an armature: find it, if there is detail left to spend.
    laid: bool = True

    @property
    def ends(self) -> tuple[int, int]:
        return (self.a, self.b)

    def touches(self, index: int) -> bool:
        return index in (self.a, self.b)

    def other(self, index: int) -> int:
        """The end that is not ``index``."""
        return self.b if self.a == index else self.a


@dataclass
class PlacedLandmark:
    """One anatomical point the artist put on the model during a guided run."""

    key: str
    at: Point3 = (0.0, 0.0, 0.0)
    #: Reflected across the median plane rather than placed by hand.  Drawn
    #: hollow, so a guess reads as a guess; editing one clears the flag.
    mirrored: bool = False

    @property
    def point(self) -> np.ndarray:
        return np.asarray(self.at, dtype=np.float64)


@dataclass
class Armature:
    """A graph of nodes and the bones joining them.

    When it came from a preset the landmarks that produced it are kept, so
    nudging one re-derives the nodes it feeds.  Editing a node by hand ends
    that: :attr:`derived` goes false, the landmarks stay as a record, and the
    graph is the artist's from then on.
    """

    name: str = "Armature"
    nodes: list[ArmatureNode] = field(default_factory=list)
    bones: list[Bone] = field(default_factory=list)
    landmarks: list[PlacedLandmark] = field(default_factory=list)
    #: Key into :data:`refview.core.landmarks.PRESETS`, empty when freehand.
    preset: str = ""
    #: Whether the nodes still follow the landmarks.
    derived: bool = False
    visible: bool = True
    color: Color = (0.35, 0.78, 1.0)

    # -- reading --------------------------------------------------------

    @property
    def node_array(self) -> np.ndarray:
        """Every node position as ``(n, 3)``."""
        if not self.nodes:
            return np.zeros((0, 3), dtype=np.float64)
        return np.asarray([node.at for node in self.nodes], dtype=np.float64)

    def bone_ends(self, bone: Bone) -> tuple[np.ndarray, np.ndarray] | None:
        """The two points a bone runs between, or ``None`` if it dangles."""
        if not self._holds(bone.a) or not self._holds(bone.b):
            return None
        return self.nodes[bone.a].point, self.nodes[bone.b].point

    def bone_length(self, bone: Bone) -> float:
        ends = self.bone_ends(bone)
        if ends is None:
            return 0.0
        return float(np.linalg.norm(ends[1] - ends[0]))

    def longest_bone(self) -> float:
        """The longest bone, falling back to the span of the nodes themselves."""
        lengths = [self.bone_length(bone) for bone in self.bones]
        longest = max(lengths, default=0.0)
        if longest > 0.0:
            return longest
        points = self.node_array
        if len(points) < 2:
            return 0.0
        return float(np.linalg.norm(points.max(axis=0) - points.min(axis=0)))

    def default_size(self) -> float:
        """A plausible thickness for a node placed by hand."""
        return self.longest_bone() * DEFAULT_SIZE_SHARE

    def bone_name(self, bone: Bone) -> str:
        """What to call a bone: its own name, or the two nodes it runs between."""
        if bone.name:
            return bone.name
        if not (self._holds(bone.a) and self._holds(bone.b)):
            return "Bone"
        return f"{self.nodes[bone.a].name} to {self.nodes[bone.b].name}"

    def bone_girth(self, bone: Bone) -> tuple[float, float]:
        """How thick the form is at each end of a bone, in scene units.

        A node whose thickness was never set falls back to the armature's own
        default rather than to nothing, so a wire drawn by hand still says how
        fat the clay laid along it ought to be.
        """
        if not (self._holds(bone.a) and self._holds(bone.b)):
            return (0.0, 0.0)
        fallback = self.default_size()
        first, second = (self.nodes[index].size for index in bone.ends)
        return (
            float(first) if first > 0.0 else fallback,
            float(second) if second > 0.0 else fallback,
        )

    def intact_bones(self) -> list[Bone]:
        """Every bone whose two ends still exist, in list order.

        What the panel lists.  A bone left dangling by an edit is not one
        anything can be done with, so it is left out here rather than checked
        for again at every use.
        """
        return [bone for bone in self.bones if self.bone_ends(bone) is not None]

    def laid_bones(self) -> list[Bone]:
        """The bones the clay is laid on, in the order it lays them.

        List order, because that *is* the order: a preset writes its bones out
        the way a figure is blocked in -- hips, ribcage, head, then the rest --
        and moving one up the list is how the artist says otherwise.  A bone
        the artist has turned off drops out of it entirely rather than being
        laid on and then hidden, so turning one off gives its budget to the
        bones after it.
        """
        return [bone for bone in self.intact_bones() if bone.laid]

    def neighbours(self, index: int) -> list[int]:
        """Every node joined to ``index`` by a bone, each listed once."""
        seen: list[int] = []
        for bone in self.bones:
            if not bone.touches(index):
                continue
            other = bone.other(index)
            if other != index and other not in seen:
                seen.append(other)
        return seen

    def node_for_role(self, role: str) -> ArmatureNode | None:
        if not role:
            return None
        for node in self.nodes:
            if node.role == role:
                return node
        return None

    def landmark_for(self, key: str) -> PlacedLandmark | None:
        for landmark in self.landmarks:
            if landmark.key == key:
                return landmark
        return None

    def placed_points(self) -> dict[str, np.ndarray]:
        """The landmarks as a mapping a preset builder can read."""
        return {landmark.key: landmark.point for landmark in self.landmarks}

    def _holds(self, index: int) -> bool:
        return 0 <= index < len(self.nodes)

    # -- editing --------------------------------------------------------
    #
    # Each of these returns a fresh ``(nodes, bones)`` pair for the caller to
    # write with one command, rather than editing this armature in place.

    def with_node(
        self, node: ArmatureNode, connect_to: int | None = None
    ) -> tuple[list[ArmatureNode], list[Bone]]:
        """The graph with ``node`` appended, optionally joined to an existing one."""
        nodes = [*self.nodes, node]
        bones = list(self.bones)
        added = len(nodes) - 1
        if connect_to is not None and 0 <= connect_to < len(self.nodes):
            bones.append(Bone(connect_to, added))
        return nodes, bones

    def without_node(self, index: int) -> tuple[list[ArmatureNode], list[Bone]]:
        """The graph with a node removed and every surviving bone renumbered."""
        if not self._holds(index):
            return list(self.nodes), list(self.bones)
        nodes = [node for position, node in enumerate(self.nodes) if position != index]
        return nodes, self._reindexed(index)

    def dissolved(self, index: int) -> tuple[list[ArmatureNode], list[Bone]]:
        """Remove a node, bridging the two it stood between.

        Taking a node out of the middle of a chain should leave the chain, not
        two loose ends; anywhere else there is nothing sensible to bridge, so
        this falls back to a plain removal.
        """
        neighbours = self.neighbours(index)
        nodes, bones = self.without_node(index)
        if len(neighbours) != 2:
            return nodes, bones
        left, right = (self._shift(value, index) for value in neighbours)
        if left == right or any(set(bone.ends) == {left, right} for bone in bones):
            return nodes, bones
        return nodes, [*bones, Bone(left, right)]

    def with_bone(self, a: int, b: int) -> tuple[list[ArmatureNode], list[Bone]]:
        """The graph with a bone between two nodes, ignoring a duplicate or a loop."""
        if a == b or not self._holds(a) or not self._holds(b):
            return list(self.nodes), list(self.bones)
        if any(set(bone.ends) == {a, b} for bone in self.bones):
            return list(self.nodes), list(self.bones)
        return list(self.nodes), [*self.bones, Bone(a, b)]

    def split_bone(
        self, index: int, node: ArmatureNode
    ) -> tuple[list[ArmatureNode], list[Bone]]:
        """The graph with a node dropped into the middle of a bone.

        The bone becomes two, so inserting into a chain lengthens it rather
        than branching off it -- which is what clicking on a length of wire
        looks like it should do.
        """
        if not 0 <= index < len(self.bones):
            return list(self.nodes), list(self.bones)
        bone = self.bones[index]
        nodes = [*self.nodes, node]
        added = len(nodes) - 1
        bones = [existing for position, existing in enumerate(self.bones) if position != index]
        bones += [Bone(bone.a, added), Bone(added, bone.b)]
        return nodes, bones

    def with_bone_moved(self, index: int, offset: int) -> list[Bone]:
        """The bone list with one bone moved up or down it.

        The order of that list is the order the clay is laid in and nothing
        else reads it, so this is a reordering of the *making* rather than a
        structural edit: no node moves, no bone is made or unmade, and an
        armature that was derived from a preset stays derived from it.
        """
        if not 0 <= index < len(self.bones):
            return list(self.bones)
        bones = list(self.bones)
        bones.insert(min(max(index + int(offset), 0), len(bones) - 1), bones.pop(index))
        return bones

    def with_bones_laid(self, positions, laid: bool) -> list[Bone]:
        """The bone list with these bones taking clay, or not taking it.

        A fresh list of fresh bones, in the spirit of every other editor here,
        so that turning a whole limb off is one command and therefore one undo
        step.  Turning them off one at a time and undoing four times would be
        nobody's idea of a single decision.
        """
        chosen = set(positions)
        return [
            replace(bone, laid=bool(laid)) if position in chosen else replace(bone)
            for position, bone in enumerate(self.bones)
        ]

    def without_bone(self, index: int) -> tuple[list[ArmatureNode], list[Bone]]:
        if not 0 <= index < len(self.bones):
            return list(self.nodes), list(self.bones)
        bones = [bone for position, bone in enumerate(self.bones) if position != index]
        return list(self.nodes), bones

    # -- editing the landmarks -------------------------------------------
    #
    # These return a fresh landmark list in the same spirit, for the caller to
    # feed back through the preset before writing both in one command.

    def with_landmark_at(self, key: str, at: Point3) -> list[PlacedLandmark]:
        """The landmark list with one point moved, and no longer a guess.

        A landmark the artist has taken hold of is theirs from then on, so
        :attr:`PlacedLandmark.mirrored` is cleared: that is what stops the
        mirror writing over it the next time the other side moves.  The
        entries that did not move are copied rather than shared, so the list
        an undo puts back is not one the next rebuild can reach into.
        """
        moved = tuple(float(value) for value in at)
        return [
            replace(entry, at=moved, mirrored=False) if entry.key == key else replace(entry)
            for entry in self.landmarks
        ]

    def without_landmarks(self, *keys: str) -> list[PlacedLandmark]:
        """The landmark list with these points taken back off the model.

        More than one at a time because dropping a landmark the mirror was
        reading from leaves its reflection anchored to nothing, and the two
        belong in the same step.
        """
        dropped = set(keys)
        return [replace(entry) for entry in self.landmarks if entry.key not in dropped]

    def _reindexed(self, removed: int) -> list[Bone]:
        """Bones that survive ``removed``, with their ends renumbered."""
        return [
            Bone(self._shift(bone.a, removed), self._shift(bone.b, removed))
            for bone in self.bones
            if not bone.touches(removed)
        ]

    @staticmethod
    def _shift(index: int, removed: int) -> int:
        return index - 1 if index > removed else index


@dataclass
class ArmatureSettings:
    """How the armature is drawn, and how new nodes are placed."""

    show_all: bool = True
    show_names: bool = False
    show_landmarks: bool = True
    #: Draw each node's thickness as a ring; off leaves plain dots.
    show_sizes: bool = True
    labels: BoneLabels = BoneLabels.HOVER
    buried: Buried = Buried.DIM
    bone_width: float = 2.5
    #: Screen radius of a plain node, and the floor a size ring never draws below.
    node_radius: float = 5.0
    #: Pixel radius of the draggable handles on an unlocked node.
    handle_radius: float = 6.0
    snap_to_vertex: bool = False
    #: Pixel radius within which a click snaps to the nearest triangle corner.
    snap_pixels: float = 12.0
    #: Place and drag nodes anywhere in space instead of on the surface.  A
    #: joint is under the skin rather than on it, so this is often what an
    #: artist wants once the landmarks are down.
    free_placement: bool = False
    #: During a guided run, reflect each paired landmark across the median
    #: plane instead of asking for both sides.
    mirror: bool = True
    #: How strongly a buried node is faded, as a share of full strength.
    buried_alpha: float = 0.3


class ArmatureStore:
    """An ordered, named collection of armatures, usually holding one.

    Deliberately plain, like the other document stores: the Qt layer wraps it
    and emits change signals, which keeps this class testable without a running
    application.
    """

    def __init__(self, items: list[Armature] | None = None) -> None:
        self._items: list[Armature] = list(items or [])

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index: int) -> Armature:
        return self._items[index]

    @property
    def items(self) -> list[Armature]:
        """The live list; the undo commands operate on it directly."""
        return self._items

    def add(self, armature: Armature) -> Armature:
        self._items.append(armature)
        return armature

    def create(self, name: str | None = None) -> Armature:
        """Append an empty armature, auto-naming it when no name is supplied."""
        return self.add(Armature(name=name or self.next_name()))

    def next_name(self) -> str:
        return f"Armature {len(self._items) + 1}"

    def clear(self) -> None:
        self._items.clear()
