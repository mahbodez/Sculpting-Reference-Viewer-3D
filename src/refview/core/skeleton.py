"""A hierarchy of joints, the pose it is in, and the skin that moves with it.

Where an :class:`~refview.core.armature.Armature` is a graph of points read off
the screen, a skeleton is what a rigging application means by the word: every
joint but the root hangs from a parent, turning a joint carries everything
below it, and a model that came with skin weights follows the bones.  It is
the thing that lets a figure be *posed* rather than only measured.

The two are kept apart on purpose.  An armature can close a loop -- a pelvic
bar, a shoulder girdle -- and a skeleton cannot, and the clay modes read the
one while the skinning reads the other.  :mod:`refview.core.rigging` turns
either into the other.

A joint holds two transforms.  Its *rest* is where the file, the preset or the
artist put it, relative to its parent, and it does not move while posing.  Its
*pose* is a turn about its own origin and a shift, both in its rest frame, and
that is what the sliders and the drags edit.  Undo therefore has one attribute
to put back per gesture, and "reset the pose" is writing the identity into
every joint without touching where any of them sits.

Joints refer to their parent by index into :attr:`Skeleton.joints`, as bones
of an armature do to their nodes, and for the same reason: every structural
edit rewrites the whole list in one undo command, so the numbers never go
stale between one step and the next.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

import numpy as np

from .armature import Buried
from .linalg import IDENTITY_QUAT, compose, quat_normalize
from .mesh import Mesh

Color = tuple[float, float, float]
Point3 = tuple[float, float, float]
Quat4 = tuple[float, float, float, float]

#: A row-major 4x4 with nothing in it, as the sixteen numbers a joint keeps.
IDENTITY16: tuple[float, ...] = tuple(float(v) for v in np.eye(4).reshape(-1))

#: A joint placed by hand takes this share of the skeleton's longest bone as
#: its drawn thickness, so a fresh chain reads at a plausible size.
DEFAULT_RADIUS_SHARE = 0.08


def _matrix16(matrix) -> tuple[float, ...]:
    return tuple(float(v) for v in np.asarray(matrix, dtype=np.float64).reshape(-1))


@dataclass
class Joint:
    """One joint: where it sits at rest, and how it is turned right now."""

    name: str = "Joint"
    #: Index of the parent joint, or ``-1`` for a root.
    parent: int = -1
    #: Where the joint sits at rest, relative to its parent, as a row-major
    #: 4x4.  A full matrix rather than a position because a file's joints
    #: carry rotations and scales of their own, and the skin weights were
    #: painted against exactly those.
    rest: tuple[float, ...] = IDENTITY16
    #: The pose: a turn about the joint's own origin, ``(x, y, z, w)``.
    rotation: Quat4 = IDENTITY_QUAT
    #: The pose's shift, in the joint's rest frame.  Mostly for the root,
    #: which is how a whole figure is moved; on any other joint it stretches
    #: the bone above it.
    translation: Point3 = (0.0, 0.0, 0.0)
    #: Which slot of a humanoid this joint fills, such as ``"knee.L"``, or
    #: empty.  Comes from a preset, a converted armature, or the name mapper.
    role: str = ""
    #: How thick to draw the bone leaving this joint, in scene units.  Zero
    #: means unset, and the skeleton's default is used.
    radius: float = 0.0
    #: A locked joint ignores the mouse.
    locked: bool = False
    #: The name the model's own rig gave this joint, which is what the skin
    #: weights are matched back to.  Empty on a joint the artist made.
    source: str = ""

    @property
    def rest_matrix(self) -> np.ndarray:
        return np.asarray(self.rest, dtype=np.float64).reshape(4, 4)

    @property
    def rest_position(self) -> np.ndarray:
        return self.rest_matrix[:3, 3]

    @property
    def pose_matrix(self) -> np.ndarray:
        return compose(self.translation, self.rotation)

    @property
    def local_matrix(self) -> np.ndarray:
        """The joint's transform relative to its parent, pose included."""
        return self.rest_matrix @ self.pose_matrix

    @property
    def posed(self) -> bool:
        """Whether the pose differs from the rest at all."""
        return any(abs(v) > 1e-9 for v in self.translation) or any(
            abs(a - b) > 1e-9 for a, b in zip(self.rotation, IDENTITY_QUAT, strict=True)
        )

    def with_rest_position(self, at) -> Joint:
        """A copy with the rest translation replaced and the frame kept."""
        rest = self.rest_matrix.copy()
        rest[:3, 3] = np.asarray(at, dtype=np.float64)
        return replace(self, rest=_matrix16(rest))


def make_joint(name: str, parent: int, at_parent_frame, **kwargs) -> Joint:
    """A joint at a position in its parent's frame, with no turn of its own."""
    rest = np.eye(4)
    rest[:3, 3] = np.asarray(at_parent_frame, dtype=np.float64)
    return Joint(name=name, parent=parent, rest=_matrix16(rest), **kwargs)


@dataclass
class Skeleton:
    """A tree -- or a forest -- of joints and the pose they stand in."""

    name: str = "Skeleton"
    joints: list[Joint] = field(default_factory=list)
    visible: bool = True
    color: Color = (1.0, 0.64, 0.30)
    #: Whether the model follows this skeleton, where it has a skin to
    #: follow it by.  Off, the bones pose in the air and the model stands
    #: still, which is how a rig is read without being disturbed.
    deform: bool = True

    # -- reading --------------------------------------------------------

    def _holds(self, index: int) -> bool:
        return 0 <= index < len(self.joints)

    def roots(self) -> list[int]:
        return [i for i, joint in enumerate(self.joints) if not self._holds(joint.parent)]

    def children(self, index: int) -> list[int]:
        return [i for i, joint in enumerate(self.joints) if joint.parent == index and i != index]

    def order(self) -> list[int]:
        """Every joint, parents before children.

        A file may list a child before its parent, and an edit may reparent
        anything, so the order the list happens to be in is never trusted.
        A joint caught in a cycle -- which no editor here can make, but a
        file could -- is treated as a root rather than left out.
        """
        count = len(self.joints)
        kids: dict[int, list[int]] = {}
        roots: list[int] = []
        for index, joint in enumerate(self.joints):
            if self._holds(joint.parent) and joint.parent != index:
                kids.setdefault(joint.parent, []).append(index)
            else:
                roots.append(index)
        seen: list[int] = []
        placed = set()
        stack = list(reversed(roots))
        while stack:
            index = stack.pop()
            if index in placed:
                continue
            placed.add(index)
            seen.append(index)
            stack.extend(reversed(kids.get(index, [])))
        for index in range(count):
            if index not in placed:
                placed.add(index)
                seen.append(index)
        return seen

    def depth(self, index: int) -> int:
        depth, seen = 0, set()
        while self._holds(index) and index not in seen:
            seen.add(index)
            index = self.joints[index].parent
            depth += 1
        return max(depth - 1, 0)

    def descendants(self, index: int) -> list[int]:
        """Every joint below ``index``, nearest first."""
        found: list[int] = []
        stack = self.children(index)
        while stack:
            child = stack.pop(0)
            if child in found or child == index:
                continue
            found.append(child)
            stack.extend(self.children(child))
        return found

    def is_ancestor(self, ancestor: int, index: int) -> bool:
        seen = set()
        while self._holds(index) and index not in seen:
            seen.add(index)
            index = self.joints[index].parent
            if index == ancestor:
                return True
        return False

    def world_matrices(self, rest: bool = False) -> np.ndarray:
        """Every joint's transform in scene space, as ``(n, 4, 4)``.

        With ``rest`` the pose is left out, which is the frame the skin
        weights were painted in.
        """
        count = len(self.joints)
        if count == 0:
            return np.zeros((0, 4, 4), dtype=np.float64)
        # Every joint's local transform in one go -- the rests as one array
        # off their tuples, the poses by a batched quaternion-to-matrix --
        # so the walk down the tree is one small product per joint.
        local = np.array([joint.rest for joint in self.joints], dtype=np.float64).reshape(
            count, 4, 4
        )
        if not rest:
            local = local @ _pose_matrices(self.joints)
        world = np.empty_like(local)
        for index in self.order():
            parent = self.joints[index].parent
            if self._holds(parent) and parent != index:
                world[index] = world[parent] @ local[index]
            else:
                world[index] = local[index]
        return world

    def positions(self, rest: bool = False) -> np.ndarray:
        """Where every joint sits, as ``(n, 3)``."""
        if not self.joints:
            return np.zeros((0, 3), dtype=np.float64)
        return self.world_matrices(rest)[:, :3, 3].copy()

    def bones(self) -> list[tuple[int, int]]:
        """Every ``(parent, child)`` pair, parents first."""
        return [
            (self.joints[index].parent, index)
            for index in self.order()
            if self._holds(self.joints[index].parent) and self.joints[index].parent != index
        ]

    def bone_length(self, index: int, positions: np.ndarray | None = None) -> float:
        """How long the bone above joint ``index`` is, or zero for a root."""
        joint = self.joints[index] if self._holds(index) else None
        if joint is None or not self._holds(joint.parent):
            return 0.0
        at = self.positions() if positions is None else positions
        return float(np.linalg.norm(at[index] - at[joint.parent]))

    def longest_bone(self) -> float:
        at = self.positions()
        lengths = [self.bone_length(child, at) for _, child in self.bones()]
        longest = max(lengths, default=0.0)
        if longest > 0.0:
            return longest
        if len(at) < 2:
            return 0.0
        return float(np.linalg.norm(at.max(axis=0) - at.min(axis=0)))

    def default_radius(self) -> float:
        return self.longest_bone() * DEFAULT_RADIUS_SHARE

    def joint_radius(self, index: int) -> float:
        radius = self.joints[index].radius if self._holds(index) else 0.0
        return float(radius) if radius > 0.0 else self.default_radius()

    @property
    def posed(self) -> bool:
        return any(joint.posed for joint in self.joints)

    @property
    def bound(self) -> bool:
        """Whether any joint answers to a name out of the model's own rig."""
        return any(joint.source for joint in self.joints)

    def joint_for_role(self, role: str) -> int | None:
        if not role:
            return None
        for index, joint in enumerate(self.joints):
            if joint.role == role:
                return index
        return None

    def roles(self) -> dict[str, int]:
        return {joint.role: index for index, joint in enumerate(self.joints) if joint.role}

    # -- editing --------------------------------------------------------
    #
    # Each returns a fresh joint list for one command to write, as the
    # armature's editors do.  Nothing here touches this skeleton.

    def with_joint(self, joint: Joint) -> list[Joint]:
        """The list with ``joint`` appended, hung from whatever it names."""
        added = replace(joint)
        if not self._holds(added.parent):
            added.parent = -1
        return [*(replace(j) for j in self.joints), added]

    def without_joint(self, index: int) -> list[Joint]:
        """The list with a joint removed and its children re-hung from its parent.

        The children keep their places in the scene: their rest transforms
        are recomposed against the new parent, so taking a joint out of the
        middle of a chain leaves the chain where it was, one joint shorter.
        """
        if not self._holds(index):
            return [replace(j) for j in self.joints]
        rest_world = self.world_matrices(rest=True)
        removed = self.joints[index]
        grandparent = removed.parent if self._holds(removed.parent) else -1
        joints: list[Joint] = []
        for position, joint in enumerate(self.joints):
            if position == index:
                continue
            copy = replace(joint)
            if joint.parent == index:
                if grandparent >= 0:
                    rest = np.linalg.inv(rest_world[grandparent]) @ rest_world[position]
                else:
                    rest = rest_world[position]
                copy.rest = _matrix16(rest)
                copy.parent = grandparent
            copy.parent = self._shift(copy.parent, index)
            joints.append(copy)
        return joints

    def without_joints(self, indices) -> list[Joint]:
        """The list with these joints removed and every survivor re-hung.

        Each kept joint hangs from its nearest kept ancestor and keeps its
        place in the scene, as :meth:`without_joint` does for one; done for
        the whole set at once so that simplifying a rig is one command.
        """
        gone = {index for index in indices if self._holds(index)}
        if not gone:
            return [replace(j) for j in self.joints]
        rest_world = self.world_matrices(rest=True)
        kept = [position for position in range(len(self.joints)) if position not in gone]
        renumber = {old: new for new, old in enumerate(kept)}
        joints: list[Joint] = []
        for position in kept:
            copy = replace(self.joints[position])
            above = copy.parent
            seen = set()
            while self._holds(above) and above in gone and above not in seen:
                seen.add(above)
                above = self.joints[above].parent
            if not self._holds(above) or above in seen:
                above = -1
            if above != copy.parent:
                rest = rest_world[position]
                if above >= 0:
                    rest = np.linalg.inv(rest_world[above]) @ rest
                copy.rest = _matrix16(rest)
            copy.parent = renumber.get(above, -1)
            joints.append(copy)
        return joints

    def without_branch(self, index: int) -> list[Joint]:
        """The list with a joint and everything below it removed."""
        if not self._holds(index):
            return [replace(j) for j in self.joints]
        gone = {index, *self.descendants(index)}
        kept = [position for position in range(len(self.joints)) if position not in gone]
        renumber = {old: new for new, old in enumerate(kept)}
        joints = []
        for position in kept:
            copy = replace(self.joints[position])
            copy.parent = renumber.get(copy.parent, -1)
            joints.append(copy)
        return joints

    def with_parent(self, index: int, parent: int) -> list[Joint]:
        """The list with one joint re-hung from another, keeping its place.

        Refused -- the list comes back unchanged -- when the new parent is
        the joint itself or anything below it, since that would close a
        loop.  ``-1`` makes the joint a root.
        """
        joints = [replace(j) for j in self.joints]
        if not self._holds(index) or parent == index or self.is_ancestor(index, parent):
            return joints
        rest_world = self.world_matrices(rest=True)
        if self._holds(parent):
            rest = np.linalg.inv(rest_world[parent]) @ rest_world[index]
        else:
            rest, parent = rest_world[index], -1
        joints[index].rest = _matrix16(rest)
        joints[index].parent = parent
        return joints

    def with_rest_at(self, index: int, at) -> list[Joint]:
        """The list with one joint's rest position moved and its children left be.

        What fitting a skeleton to a model wants: pull the knee into the
        knee and the hip and the ankle stay where they were, so both bones
        adjust rather than the whole leg swinging.  The joint's own frame is
        kept; only its origin moves.
        """
        joints = [replace(j) for j in self.joints]
        if not self._holds(index):
            return joints
        rest_world = self.world_matrices(rest=True)
        target = np.asarray(at, dtype=np.float64)
        parent = self.joints[index].parent
        frame = rest_world[parent] if self._holds(parent) else np.eye(4)
        local = np.linalg.inv(frame) @ np.array([*target, 1.0])
        moved = rest_world[index].copy()
        moved[:3, 3] = target
        joints[index] = joints[index].with_rest_position(local[:3])
        for child in self.children(index):
            rest = np.linalg.inv(moved) @ rest_world[child]
            joints[child].rest = _matrix16(rest)
        return joints

    def with_pose_reset(self, indices=None) -> list[Joint]:
        """The list with these joints -- or every joint -- put back at rest."""
        chosen = None if indices is None else set(indices)
        return [
            replace(joint, rotation=IDENTITY_QUAT, translation=(0.0, 0.0, 0.0))
            if chosen is None or position in chosen
            else replace(joint)
            for position, joint in enumerate(self.joints)
        ]

    def transformed(self, matrix) -> list[Joint]:
        """The list with the whole skeleton carried through a rigid transform.

        Applied to the roots alone: every other joint is relative to its
        parent and comes along.  How the model's orientation is changed
        under a skeleton that has already been posed.
        """
        matrix = np.asarray(matrix, dtype=np.float64).reshape(4, 4)
        joints = [replace(j) for j in self.joints]
        for index in self.roots():
            joints[index].rest = _matrix16(matrix @ joints[index].rest_matrix)
        return joints

    @staticmethod
    def _shift(index: int, removed: int) -> int:
        return index - 1 if index > removed else index


@dataclass
class SkeletonSettings:
    """How skeletons are drawn, and how the pose tool behaves."""

    show_all: bool = True
    show_names: bool = False
    #: Draw the joints' thickness as rings, as the armature does its nodes.
    show_radii: bool = False
    buried: Buried = Buried.DIM
    bone_width: float = 3.0
    #: Screen radius of a joint.
    joint_radius: float = 5.0
    handle_radius: float = 6.0
    buried_alpha: float = 0.3
    #: Let a skinned model follow its skeleton at all.  One switch for the
    #: document, over each skeleton's own :attr:`Skeleton.deform`.
    deform: bool = True
    #: Dragging a joint moves where it *rests* rather than bending the bone
    #: above it: fitting a skeleton to a model rather than posing it.
    fit: bool = False
    #: Place new joints anywhere in space rather than on the surface.
    free_placement: bool = False
    snap_to_vertex: bool = False
    snap_pixels: float = 12.0
    #: Degrees of twist per pixel of a Shift-drag.
    twist_per_pixel: float = 0.5


class SkeletonStore:
    """An ordered collection of skeletons, like the other document stores."""

    def __init__(self, items: list[Skeleton] | None = None) -> None:
        self._items: list[Skeleton] = list(items or [])

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index: int) -> Skeleton:
        return self._items[index]

    @property
    def items(self) -> list[Skeleton]:
        return self._items

    def add(self, skeleton: Skeleton) -> Skeleton:
        self._items.append(skeleton)
        return skeleton

    def next_name(self) -> str:
        return f"Skeleton {len(self._items) + 1}"

    def clear(self) -> None:
        self._items.clear()

    def bound(self) -> Skeleton | None:
        """The skeleton the model follows: the first one bound to its rig."""
        for skeleton in self._items:
            if skeleton.bound:
                return skeleton
        return None


# ----------------------------------------------------------------------
# The skin
# ----------------------------------------------------------------------


class Skin:
    """Which joints move each vertex, and by how much.

    Plain arrays, and never written into a session: a hundred thousand
    vertices' worth of weights belongs to the model file, which is where it
    is read back from.  The session keeps the pose and the names.
    """

    __slots__ = ("joints", "weights", "inverse_bind", "base", "base_normals")

    def __init__(self, joints, weights, inverse_bind, base, base_normals) -> None:
        self.joints = np.ascontiguousarray(joints, dtype=np.int32).reshape(-1, 4)
        self.weights = np.ascontiguousarray(weights, dtype=np.float32).reshape(-1, 4)
        self.inverse_bind = np.ascontiguousarray(inverse_bind, dtype=np.float64).reshape(-1, 4, 4)
        self.base = np.ascontiguousarray(base, dtype=np.float32).reshape(-1, 3)
        self.base_normals = np.ascontiguousarray(base_normals, dtype=np.float32).reshape(-1, 3)
        if len(self.joints) != len(self.weights) or len(self.base) != len(self.joints):
            raise ValueError("skin arrays must have one row per vertex")
        if self.joints.size and int(self.joints.max()) >= len(self.inverse_bind):
            raise ValueError("skin refers to a joint it has no bind matrix for")

    @property
    def joint_count(self) -> int:
        return len(self.inverse_bind)

    def transformed(self, matrix) -> Skin:
        """The skin in the space a rigid ``matrix`` carries the model into."""
        matrix = np.asarray(matrix, dtype=np.float64).reshape(4, 4)
        rotation = matrix[:3, :3]
        base = self.base.astype(np.float64) @ rotation.T + matrix[:3, 3]
        normals = self.base_normals.astype(np.float64) @ np.linalg.inv(rotation)
        inverse = np.linalg.inv(matrix)
        return Skin(
            self.joints,
            self.weights,
            np.einsum("jik,kl->jil", self.inverse_bind, inverse),
            base,
            normals,
        )


class Rig:
    """The skeleton a model file came with, in the model's own coordinates.

    Read once by the loader and carried on the :class:`Mesh` through every
    turn and recentring, so that the document's :class:`Skeleton` -- which
    is what the artist edits -- can always be matched back to it by name.
    """

    __slots__ = ("names", "parents", "rest_local", "skin")

    def __init__(self, names, parents, rest_local, skin: Skin) -> None:
        self.names = [str(name) for name in names]
        self.parents = [int(parent) for parent in parents]
        self.rest_local = np.ascontiguousarray(rest_local, dtype=np.float64).reshape(-1, 4, 4)
        self.skin = skin
        if not len(self.names) == len(self.parents) == len(self.rest_local) == skin.joint_count:
            raise ValueError("a rig needs one name, parent and rest transform per joint")

    @property
    def joint_count(self) -> int:
        return len(self.names)

    def rest_world(self) -> np.ndarray:
        return self.to_skeleton().world_matrices(rest=True)

    def to_skeleton(self, name: str = "Skeleton") -> Skeleton:
        """A document skeleton standing exactly where the file's joints stand."""
        joints = [
            Joint(
                name=self.names[index],
                parent=self.parents[index],
                rest=_matrix16(self.rest_local[index]),
                source=self.names[index],
            )
            for index in range(self.joint_count)
        ]
        return Skeleton(name=name, joints=joints)

    def transformed(self, matrix) -> Rig:
        matrix = np.asarray(matrix, dtype=np.float64).reshape(4, 4)
        rest = self.rest_local.copy()
        for index, parent in enumerate(self.parents):
            if not 0 <= parent < self.joint_count:
                rest[index] = matrix @ rest[index]
        return Rig(self.names, self.parents, rest, self.skin.transformed(matrix))

    def binding(self, skeleton: Skeleton) -> tuple[np.ndarray, np.ndarray]:
        """Which document joint each rig joint answers to.

        Returns two ``(j,)`` arrays: the document joint carrying each rig
        joint, and the rig joint that document joint was matched *through*.
        Matched by the name the file gave the joint, so renaming one in the
        panel does not lose its weights.  A rig joint the artist has deleted
        hands its weights to the nearest ancestor that still exists, which
        is what deleting it meant, and the second array says which ancestor
        so that the rest offset between the two can be kept.  One with no
        ancestor left is ``-1`` and holds its part of the model still.
        """
        by_source: dict[str, list[int]] = {}
        for index, joint in enumerate(skeleton.joints):
            if joint.source:
                by_source.setdefault(joint.source, []).append(index)
        direct = np.full(self.joint_count, -1, dtype=np.int64)
        for index, name in enumerate(self.names):
            claimants = by_source.get(name)
            if claimants:
                direct[index] = claimants.pop(0)
        bound = direct.copy()
        through = np.arange(self.joint_count, dtype=np.int64)
        for index in range(self.joint_count):
            walk = index
            while 0 <= walk < self.joint_count and direct[walk] < 0:
                walk = self.parents[walk]
            if 0 <= walk < self.joint_count:
                bound[index], through[index] = direct[walk], walk
            else:
                bound[index], through[index] = -1, index
        return bound, through


def skinned_mesh(rest: Mesh, skeleton: Skeleton) -> Mesh:
    """The model as ``skeleton`` poses it, or ``rest`` itself when it cannot.

    Linear blend skinning: each vertex is carried by up to four joints, each
    from where it stood when the weights were painted (the inverse bind) to
    where the joint is now, and the four results are mixed by weight.  A
    vertex no joint claims -- a prop, a base -- keeps its place.

    The matrices are made per joint and gathered per weight slot, so the
    cost is a few vectorised passes over the vertex arrays and no Python
    loop over vertices.
    """
    rig = rest.rig
    if rig is None or not skeleton.joints:
        return rest
    bound, through = rig.binding(skeleton)
    if not np.any(bound >= 0):
        return rest
    posed = skeleton.world_matrices()
    rig_rest = rig.rest_world()
    matrices = np.empty((rig.joint_count, 4, 4), dtype=np.float64)
    for index in range(rig.joint_count):
        if bound[index] < 0:
            world = rig_rest[index]
        elif through[index] == index:
            world = posed[bound[index]]
        else:
            # Carried by an ancestor: keep the rest offset from it to here.
            via = through[index]
            world = posed[bound[index]] @ np.linalg.inv(rig_rest[via]) @ rig_rest[index]
        matrices[index] = world @ rig.skin.inverse_bind[index]

    skin = rig.skin
    base = skin.base.astype(np.float64)
    base_normals = skin.base_normals.astype(np.float64)
    positions = np.zeros_like(base)
    normals = np.zeros_like(base_normals)
    for slot in range(4):
        weight = skin.weights[:, slot].astype(np.float64)
        carried = weight > 0.0
        if not np.any(carried):
            continue
        rows = np.flatnonzero(carried)
        gathered = matrices[skin.joints[rows, slot]]
        turned = np.einsum("nij,nj->ni", gathered[:, :3, :3], base[rows]) + gathered[:, :3, 3]
        positions[rows] += weight[rows, None] * turned
        normals[rows] += weight[rows, None] * np.einsum(
            "nij,nj->ni", gathered[:, :3, :3], base_normals[rows]
        )
    total = skin.weights.sum(axis=1)
    still = total <= 0.0
    if np.any(still):
        positions[still] = rest.positions[still]
        normals[still] = rest.normals[still]
    lengths = np.linalg.norm(normals, axis=1, keepdims=True)
    normals = np.where(lengths > 1e-12, normals / np.maximum(lengths, 1e-20), rest.normals)
    return Mesh(
        positions.astype(np.float32),
        normals.astype(np.float32),
        rest.indices,
        rest.name,
        source_offset=rest.source_offset,
        units=rest.units,
        rig=rest.rig,
    )


def _pose_matrices(joints: list[Joint]) -> np.ndarray:
    """Every joint's pose as ``(n, 4, 4)``, the quaternions turned in one pass."""
    q = np.array([joint.rotation for joint in joints], dtype=np.float64).reshape(-1, 4)
    length = np.linalg.norm(q, axis=1, keepdims=True)
    q = np.where(length > 1e-12, q / np.maximum(length, 1e-20), np.array(IDENTITY_QUAT))
    x, y, z, w = q[:, 0], q[:, 1], q[:, 2], q[:, 3]
    out = np.tile(np.eye(4), (len(joints), 1, 1))
    out[:, 0, 0] = 1 - 2 * (y * y + z * z)
    out[:, 0, 1] = 2 * (x * y - z * w)
    out[:, 0, 2] = 2 * (x * z + y * w)
    out[:, 1, 0] = 2 * (x * y + z * w)
    out[:, 1, 1] = 1 - 2 * (x * x + z * z)
    out[:, 1, 2] = 2 * (y * z - x * w)
    out[:, 2, 0] = 2 * (x * z - y * w)
    out[:, 2, 1] = 2 * (y * z + x * w)
    out[:, 2, 2] = 1 - 2 * (x * x + y * y)
    out[:, :3, 3] = np.array([joint.translation for joint in joints], dtype=np.float64)
    return out


def rest_skinned_positions(skin: Skin, world: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Positions and normals of a skin under the joint transforms ``world``.

    What the loader uses to put a file's vertices where its own default
    pose has them, before the viewer has a skeleton of its own to ask.
    """
    matrices = np.einsum("jik,jkl->jil", world, skin.inverse_bind)
    base = skin.base.astype(np.float64)
    base_normals = skin.base_normals.astype(np.float64)
    positions = np.zeros_like(base)
    normals = np.zeros_like(base_normals)
    for slot in range(4):
        weight = skin.weights[:, slot].astype(np.float64)
        rows = np.flatnonzero(weight > 0.0)
        if not len(rows):
            continue
        gathered = matrices[skin.joints[rows, slot]]
        positions[rows] += weight[rows, None] * (
            np.einsum("nij,nj->ni", gathered[:, :3, :3], base[rows]) + gathered[:, :3, 3]
        )
        normals[rows] += weight[rows, None] * np.einsum(
            "nij,nj->ni", gathered[:, :3, :3], base_normals[rows]
        )
    still = skin.weights.sum(axis=1) <= 0.0
    positions[still] = base[still]
    normals[still] = base_normals[still]
    lengths = np.linalg.norm(normals, axis=1, keepdims=True)
    normals = np.where(lengths > 1e-12, normals / np.maximum(lengths, 1e-20), base_normals)
    return positions, normals


def normalized_rotation(rotation) -> Quat4:
    """A pose rotation as the plain tuple a joint stores."""
    return tuple(float(v) for v in quat_normalize(rotation))
