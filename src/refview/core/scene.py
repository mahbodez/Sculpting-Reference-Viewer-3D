"""Several models in one scene: what each is called, where it stands, what it hangs from.

The viewer began as a window on one file, and most of it still reads the
scene as one mesh -- picking, the section, the pedestal, the planes and the
shadows all take a single :class:`~refview.core.mesh.Mesh` and are none the
wiser.  What this module adds underneath is a list of *objects*, each a mesh
of its own with a place in the world and, if the artist says so, a parent it
follows.  The one mesh the rest of the viewer reads is then built out of the
objects that are shown, in world space, by :mod:`refview.ui.state`.

An object's :class:`Transform` is local to its parent, as it is in every
modelling application: move the parent and the children come along, because
their world matrix is the product of the chain above them.  Parenting keeps
the child where it stands by default, which means re-expressing its transform
in the new parent's frame rather than carrying it off to wherever the parent
happens to be.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path

import numpy as np

from .linalg import compose, euler_to_quat, matrix_to_quat, quat_to_euler
from .mesh import Mesh, concatenated, loose_parts, submesh
from .orientation import OrientationSettings

Vector = tuple[float, float, float]


def _triple(values, fallback: float) -> Vector:
    try:
        x, y, z = (float(v) for v in values)
    except (TypeError, ValueError):
        return (fallback, fallback, fallback)
    return (x, y, z)


@dataclass
class Transform:
    """Where an object stands relative to its parent: an affine placement.

    Held as the three things an artist types -- a move, three angles and a
    scale -- rather than as a matrix, because a matrix cannot say which of
    the infinitely many angle triples it was made from and a panel has to
    show one.  The angles are applied about the object's own X, then Y, then
    Z, the same convention :func:`~refview.core.linalg.euler_to_quat` uses
    for the skeletons.  The scale is applied first, then the turn, then the
    move, which is what makes a scale of two "twice as big" and not "twice
    as far away".
    """

    translation: Vector = (0.0, 0.0, 0.0)
    rotation_deg: Vector = (0.0, 0.0, 0.0)
    scale: Vector = (1.0, 1.0, 1.0)

    @property
    def matrix(self) -> np.ndarray:
        """The 4x4 that carries the object's own coordinates into its parent's."""
        return compose(
            _triple(self.translation, 0.0),
            euler_to_quat(*_triple(self.rotation_deg, 0.0)),
            _triple(self.scale, 1.0),
        )

    @property
    def is_identity(self) -> bool:
        return (
            all(abs(v) < 1e-12 for v in self.translation)
            and all(abs(v) < 1e-12 for v in self.rotation_deg)
            and all(abs(v - 1.0) < 1e-12 for v in self.scale)
        )

    @classmethod
    def from_matrix(cls, matrix: np.ndarray) -> Transform:
        """The transform a matrix stands for, read back out of it.

        The scale is the length of each column and the turn is what is left
        once it is divided out.  A matrix carrying a shear -- a child turned
        under a parent scaled unevenly -- loses the shear here, since there
        is no box in the panel to show it in; the nearest transform without
        one is what comes back.
        """
        matrix = np.asarray(matrix, dtype=np.float64).reshape(4, 4)
        linear = matrix[:3, :3]
        scale = np.linalg.norm(linear, axis=0)
        scale = np.where(scale > 1e-12, scale, 1.0)
        rotation = linear / scale
        # A mirrored placement has a negative determinant; give the mirror to
        # one axis of the scale so the turn stays a proper rotation.
        if np.linalg.det(rotation) < 0.0:
            scale[0] = -scale[0]
            rotation[:, 0] = -rotation[:, 0]
        angles = quat_to_euler(matrix_to_quat(rotation))
        return cls(
            translation=tuple(float(v) for v in matrix[:3, 3]),
            rotation_deg=tuple(_tidy_angle(a) for a in angles),
            scale=tuple(float(v) for v in scale),
        )


def _tidy_angle(degrees: float) -> float:
    """An angle in (-180, 180], with the floating-point dust brushed off."""
    wrapped = (float(degrees) + 180.0) % 360.0 - 180.0
    if wrapped <= -180.0:
        wrapped += 360.0
    return 0.0 if abs(wrapped) < 1e-9 else wrapped


@dataclass
class ObjectSettings:
    """What a parent's state means for its children, and how the tools scale.

    Each is the answer to a question with more than one sensible answer, so
    each is a switch; what ships is the reading Blender and its peers give.
    """

    #: Hiding a parent hides everything hung from it.  Off, every object's
    #: box is its own and a hidden parent leaves its children standing.
    hide_children: bool = True
    #: A parent's solidity is handed down: a child of a half-ghosted parent is
    #: drawn at half of its own.  Off, the slider on each row is the whole
    #: story for that row.
    ghost_children: bool = True
    #: Parenting keeps the child where it stands, re-expressing its place in
    #: the parent's frame.  Off, the child's numbers are kept as they are and
    #: it jumps to wherever those numbers land under the new parent.
    keep_transform: bool = True
    #: Removing a parent removes its children with it.  Off, the children are
    #: hung from the grandparent, where they stood.
    remove_children: bool = False
    #: The scale gesture and the scale boxes move all three axes together.
    #: Off, each axis is its own, which is how a form is stretched.
    uniform_scale: bool = True


class SceneObject:
    """One model in the scene.

    Three meshes are kept, as the viewer kept them when there was only one
    object: the file's own, that file turned the right way up and centred on
    its pivot, and -- worked out on demand -- the centred mesh carried to
    where the object stands in the world.  The turning is this object's
    :attr:`orientation`, since a Z-up scan and a Y-up sculpt can stand in
    one scene; the standing is its :attr:`transform` under its
    :attr:`parent`.
    """

    __slots__ = (
        "name",
        "source_mesh",
        "rest_mesh",
        "path",
        "transform",
        "orientation",
        "parent",
        "visible",
        "opacity",
        "skin_path",
        "_world",
        "_pose",
    )

    def __init__(
        self,
        source_mesh: Mesh,
        rest_mesh: Mesh | None = None,
        name: str | None = None,
        path: str | Path | None = None,
        transform: Transform | None = None,
        visible: bool = True,
        opacity: float = 1.0,
        orientation: OrientationSettings | None = None,
    ) -> None:
        self.source_mesh = source_mesh
        self.rest_mesh = source_mesh if rest_mesh is None else rest_mesh
        self.name = name or (Path(path).stem if path else source_mesh.name)
        self.path: Path | None = None if path is None else Path(path)
        self.transform = transform or Transform()
        #: The rigid turn that took :attr:`source_mesh` to :attr:`rest_mesh`:
        #: which axis of the file is up, and so on.  The identity for an
        #: object made here out of others, whose own mesh is already upright.
        self.orientation = orientation or OrientationSettings()
        #: The object this one hangs from, or ``None`` at the root.
        self.parent: SceneObject | None = None
        self.visible = bool(visible)
        #: How solid the object is drawn on its own account, 0 to 1.
        self.opacity = float(opacity)
        #: Where the skin this object was auto-skinned into was last written,
        #: if it has one and it has been; see :mod:`refview.core.rig_file`.
        self.skin_path: Path | None = None
        #: The rest mesh carried to a world matrix, kept with what it was
        #: carried by, so that a frame that moved nothing costs nothing.
        self._world: tuple[tuple, Mesh] | None = None
        #: The world mesh as a skeleton last posed it, with the pose it was
        #: posed for; see :meth:`ViewerState._rebuild`.
        self._pose: tuple[tuple, Mesh] | None = None

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"SceneObject({self.name!r})"

    @property
    def rig(self):
        return self.rest_mesh.rig

    def world_rest(self, matrix: np.ndarray) -> Mesh:
        """The centred mesh carried by ``matrix`` -- the mesh itself for the identity."""
        matrix = np.asarray(matrix, dtype=np.float64)
        key = (id(self.rest_mesh), matrix.tobytes())
        if self._world is not None and self._world[0] == key:
            return self._world[1]
        if np.allclose(matrix, np.eye(4)):
            carried = self.rest_mesh
        else:
            carried = self.rest_mesh.transformed_by(matrix)
        self._world = (key, carried)
        return carried

    def forget(self) -> None:
        """Drop the derived meshes, after the rest mesh has been replaced."""
        self._world = None
        self._pose = None


#: A snapshot of the store: each object with the parent, placement, visibility
#: and solidity it had, in order, and which was active.  What an undo step
#: holds for any edit to the list.
Snapshot = tuple[list[tuple["SceneObject", "SceneObject | None", Transform, bool, float]], int]


class ObjectStore:
    """The objects of the scene, in the order the panel lists their roots.

    Exactly one object is *active* whenever there are any: it is the one the
    transform tool moves, the boxes in the panel describe, and the Imported
    group reports on.
    """

    def __init__(self, items=None) -> None:
        self._items: list[SceneObject] = list(items or [])
        self.active: int = 0 if self._items else -1

    # -- the list -------------------------------------------------------

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index: int) -> SceneObject:
        return self._items[index]

    @property
    def items(self) -> list[SceneObject]:
        return self._items

    def index(self, obj: SceneObject | None) -> int:
        for index, held in enumerate(self._items):
            if held is obj:
                return index
        return -1

    @property
    def active_object(self) -> SceneObject | None:
        if 0 <= self.active < len(self._items):
            return self._items[self.active]
        return None

    def set_active(self, obj: SceneObject | None) -> None:
        self.active = self.index(obj)
        if self.active < 0 and self._items:
            self.active = 0

    def add(self, obj: SceneObject, activate: bool = True) -> SceneObject:
        self._items.append(obj)
        if activate or self.active < 0:
            self.active = len(self._items) - 1
        return obj

    def clear(self) -> None:
        self._items.clear()
        self.active = -1

    def next_name(self, stem: str) -> str:
        """``stem``, or ``stem.001`` and upwards when the name is taken."""
        taken = {obj.name for obj in self._items}
        if stem not in taken:
            return stem
        for count in range(1, 10_000):
            candidate = f"{stem}.{count:03d}"
            if candidate not in taken:
                return candidate
        return stem  # pragma: no cover - ten thousand copies of one name

    # -- the tree -------------------------------------------------------

    def children(self, obj: SceneObject | None) -> list[SceneObject]:
        return [held for held in self._items if held.parent is obj]

    def roots(self) -> list[SceneObject]:
        return self.children(None)

    def descendants(self, obj: SceneObject) -> list[SceneObject]:
        found: list[SceneObject] = []
        for child in self.children(obj):
            found.append(child)
            found.extend(self.descendants(child))
        return found

    def is_ancestor(self, obj: SceneObject, of: SceneObject) -> bool:
        walk = of.parent
        while walk is not None:
            if walk is obj:
                return True
            walk = walk.parent
        return False

    def ordered(self) -> list[tuple[SceneObject, int]]:
        """Every object depth-first with its depth, the order a tree lists them."""
        out: list[tuple[SceneObject, int]] = []

        def visit(parent: SceneObject | None, depth: int) -> None:
            for child in self.children(parent):
                out.append((child, depth))
                visit(child, depth + 1)

        visit(None, 0)
        # An object whose parent has gone missing is still an object.
        listed = {id(obj) for obj, _ in out}
        out.extend((obj, 0) for obj in self._items if id(obj) not in listed)
        return out

    def parent_matrix(self, obj: SceneObject) -> np.ndarray:
        return np.eye(4) if obj.parent is None else self.world_matrix(obj.parent)

    def world_matrix(self, obj: SceneObject) -> np.ndarray:
        matrix = obj.transform.matrix
        walk = obj.parent
        guard = 0
        while walk is not None and guard < len(self._items) + 1:
            matrix = walk.transform.matrix @ matrix
            walk = walk.parent
            guard += 1
        return matrix

    def set_parent(
        self, child: SceneObject, parent: SceneObject | None, keep_transform: bool = True
    ) -> bool:
        """Hang ``child`` from ``parent``; False when that would close a loop."""
        if parent is child or (parent is not None and self.is_ancestor(child, parent)):
            return False
        if child.parent is parent:
            return True
        if keep_transform:
            world = self.world_matrix(child)
            above = np.eye(4) if parent is None else self.world_matrix(parent)
            child.transform = Transform.from_matrix(np.linalg.inv(above) @ world)
        child.parent = parent
        return True

    def set_world_matrix(self, obj: SceneObject, world: np.ndarray) -> None:
        """Put ``obj`` at ``world``, whatever its parent is doing."""
        obj.transform = Transform.from_matrix(np.linalg.inv(self.parent_matrix(obj)) @ world)

    def remove(self, obj: SceneObject, settings: ObjectSettings) -> list[SceneObject]:
        """Take ``obj`` out, and say what went with it.

        The children go too, or are hung from the grandparent where they
        stood, as :attr:`ObjectSettings.remove_children` says.
        """
        if self.index(obj) < 0:
            return []
        gone = [obj]
        if settings.remove_children:
            gone.extend(self.descendants(obj))
        else:
            for child in self.children(obj):
                self.set_parent(child, obj.parent, keep_transform=True)
        active = self.active_object
        for held in gone:
            self._items.remove(held)
        if active in gone or active is None:
            self.active = min(max(self.active, 0), len(self._items) - 1)
        else:
            self.active = self.index(active)
        return gone

    # -- what is shown --------------------------------------------------

    def shown(self, obj: SceneObject, settings: ObjectSettings) -> bool:
        """Whether ``obj`` is drawn: its own box, and its parents' if they count."""
        if not obj.visible:
            return False
        if settings.hide_children:
            walk = obj.parent
            while walk is not None:
                if not walk.visible:
                    return False
                walk = walk.parent
        return True

    def opacity(self, obj: SceneObject, settings: ObjectSettings) -> float:
        """How solid ``obj`` is drawn, after its parents have had their say."""
        value = min(max(float(obj.opacity), 0.0), 1.0)
        if settings.ghost_children:
            walk = obj.parent
            while walk is not None:
                value *= min(max(float(walk.opacity), 0.0), 1.0)
                walk = walk.parent
        return value

    def any_shown(self, settings: ObjectSettings) -> bool:
        return any(self.shown(obj, settings) for obj in self._items)

    # -- undo -----------------------------------------------------------

    def snapshot(self) -> Snapshot:
        return (
            [
                (obj, obj.parent, replace(obj.transform), obj.visible, obj.opacity)
                for obj in self._items
            ],
            self.active,
        )

    def restore(self, snapshot: Snapshot) -> None:
        rows, active = snapshot
        self._items = [obj for obj, *_ in rows]
        for obj, parent, transform, visible, opacity in rows:
            obj.parent = parent
            obj.transform = replace(transform)
            obj.visible = visible
            obj.opacity = opacity
        self.active = active if 0 <= active < len(self._items) else (0 if self._items else -1)


# ----------------------------------------------------------------------
# Merging and splitting
# ----------------------------------------------------------------------

#: More loose pieces than this and a "split" would bury the panel in rows
#: rather than give the artist anything to take hold of.
MAX_SPLIT_PIECES = 256


def merge_objects(
    store: ObjectStore, objects: list[SceneObject], name: str = "Merged"
) -> SceneObject:
    """One object out of several, standing where they stood.

    The meshes are carried into the world and joined there, so the result is
    the same shape the artist was looking at; its pivot is put at the centre
    of the joined box.  Any rig is left behind: skin weights belong to one
    file's joints and two files' joints are not one skeleton.
    """
    world = concatenated(
        [obj.world_rest(store.world_matrix(obj)) for obj in objects], name=name
    )
    centre = world.bounds.center
    rest = world.recentered()
    merged = SceneObject(
        rest, rest, name=name, transform=Transform(translation=tuple(float(v) for v in centre))
    )
    return merged


def split_object(store: ObjectStore, obj: SceneObject) -> list[SceneObject] | None:
    """The loose pieces of ``obj`` as objects of their own, or ``None`` if it is one piece.

    Each piece is centred on its own pivot and placed so that nothing moves,
    and all of them are hung where the original was.  Pieces are found by
    shared vertices, as a modelling application's "separate by loose parts"
    finds them; a file that stores its parts as separate index ranges but
    never welds them across the seam comes out the same way.
    """
    pieces = loose_parts(obj.rest_mesh)
    if len(pieces) <= 1:
        return None
    if len(pieces) > MAX_SPLIT_PIECES:
        raise ValueError(
            f"{obj.name} is {len(pieces):,} loose pieces; more than {MAX_SPLIT_PIECES} "
            "is too many to hold as separate objects"
        )
    world = store.world_matrix(obj)
    out: list[SceneObject] = []
    for number, triangles in enumerate(pieces, start=1):
        part = submesh(obj.rest_mesh, triangles, name=f"{obj.name}.{number:03d}")
        centre = part.bounds.center
        rest = part.recentered()
        shift = np.eye(4)
        shift[:3, 3] = centre
        piece = SceneObject(rest, rest, name=part.name, visible=obj.visible, opacity=obj.opacity)
        piece.parent = obj.parent
        store_matrix = world @ shift
        piece.transform = Transform.from_matrix(
            np.linalg.inv(store.parent_matrix(piece)) @ store_matrix
        )
        out.append(piece)
    return out


def duplicate_object(store: ObjectStore, obj: SceneObject) -> SceneObject:
    """A copy of ``obj``, standing exactly where it stands and hung where it hangs.

    Only the mesh comes across: the copy reads the same vertices, but a rig
    is left behind -- skin weights belong to one figure's skeleton, and the
    copy has none -- and so are the children, which still hang from the
    original.  It has no file of its own until the session is saved.
    """
    source = _bare(obj.source_mesh)
    rest = source if obj.rest_mesh is obj.source_mesh else _bare(obj.rest_mesh)
    copy = SceneObject(
        source,
        rest,
        name=store.next_name(obj.name),
        transform=replace(obj.transform),
        visible=obj.visible,
        opacity=obj.opacity,
        orientation=replace(obj.orientation),
    )
    copy.parent = obj.parent
    return copy


def _bare(mesh: Mesh) -> Mesh:
    """``mesh`` without its rig, sharing its vertices; nothing writes those in place."""
    return Mesh(
        mesh.positions,
        mesh.normals,
        mesh.indices,
        mesh.name,
        source_offset=mesh.source_offset,
        units=mesh.units,
    )


@dataclass
class ObjectRecord:
    """What a session writes down about an object; the mesh itself stays in its file."""

    name: str = ""
    path: str | None = None
    transform: Transform = field(default_factory=Transform)
    #: Index of the parent in the same list, or -1 at the root.
    parent: int = -1
    visible: bool = True
    opacity: float = 1.0
    #: The archive holding the skin the object was auto-skinned into, or
    #: ``None`` for an object wearing its file's own skin or none.
    skin: str | None = None
    #: Which way up the file is read.  ``None`` in a session from before
    #: version 11, when one orientation served every object; that one is
    #: the session's own and is applied in its place.
    orientation: OrientationSettings | None = None


def records_for(store: ObjectStore) -> list[ObjectRecord]:
    """The store as a session writes it: parents by index into the same list."""
    return [
        ObjectRecord(
            name=obj.name,
            path=None if obj.path is None else str(obj.path),
            transform=replace(obj.transform),
            parent=store.index(obj.parent),
            visible=obj.visible,
            opacity=float(obj.opacity),
            skin=None if obj.skin_path is None else str(obj.skin_path),
            orientation=replace(obj.orientation),
        )
        for obj in store
    ]

