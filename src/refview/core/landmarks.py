"""Guided presets: the anatomy an artist points at, and the joints it implies.

A preset is an ordered list of surface landmarks -- bumps and hollows an artist
can actually find on a model -- and a rule for turning them into an armature.
The landmarks are not the armature.  Nobody can point at the centre of a femoral
head, but everybody can find the greater trochanter beside it and the two hip
points in front, and the joint falls out of those three.  Asking for what is
visible and inferring what is not is both less to ask and more accurate than
asking for a guess at the joint itself.

Every inference here is a ratio of the figure's *own* measured spans rather than
an absolute distance, so one rule fits a child and a heroic nude, and nothing
drifts when the pose changes.

The same paired landmarks pay for themselves twice: two epicondyles locate the
elbow, and the distance between them is the width of the elbow, so a node comes
out sized without the artist ever being asked for a size.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

import numpy as np

from .armature import ArmatureNode, Bone, PlacedLandmark

# ----------------------------------------------------------------------
# Ratios
#
# Each is a share of a span the artist has already measured by placing the
# landmarks, so they scale with the figure and hold under pose.
# ----------------------------------------------------------------------

#: T12 is a landmark on the back; the spine of the wire runs through the core,
#: so the node is carried forward by this share of the depth of the ribcage.
SPINE_FORWARD = 0.5
#: The centre of the shoulder joint sits below the acromion, this far along the
#: line to the elbow ...
SHOULDER_DOWN_ARM = 0.13
#: ... and this far in towards the middle of the chest.
SHOULDER_INTO_TRUNK = 0.18
#: The femoral head lies medial to the greater trochanter, this share of the way
#: towards the centre of the pelvis -- which carries it a little up and back as
#: well, which is where it really is.
HIP_TOWARD_PELVIS = 0.25
#: Head node when the mastoids were skipped: this far from C7 up to the vertex.
HEAD_UP_FROM_NECK = 0.5
#: A hand, a foot and the crown are ends of wire rather than joints, so they
#: take this share of the joint above them for their thickness.
END_SHARE = 0.8
#: Two landmarks a span apart describe a joint of about this radius.
JOINT_RADIUS = 0.5

#: A centre line whose second spread is this small a share of its first is
#: effectively a straight line, and no plane through it can be trusted.
PLANE_SPREAD = 0.02


class Side(str, Enum):
    """Which side of the figure a landmark belongs to."""

    CENTRE = "centre"
    LEFT = "left"
    RIGHT = "right"

    @property
    def label(self) -> str:
        return {Side.CENTRE: "", Side.LEFT: "left", Side.RIGHT: "right"}[self]


@dataclass(frozen=True)
class Landmark:
    """One point of anatomy the artist is asked to find."""

    key: str
    name: str
    #: What to look for, in the words an artist would use.
    hint: str
    side: Side = Side.CENTRE
    #: Optional landmarks refine the armature; the required ones make it.
    required: bool = True
    #: For a right-hand landmark, the key of the left one it mirrors.
    mirror_of: str = ""

    @property
    def title(self) -> str:
        """The name with its side, for a prompt."""
        return f"{self.name} ({self.side.label})" if self.side.label else self.name


@dataclass(frozen=True)
class Preset:
    """An ordered set of landmarks and the armature they build."""

    key: str
    name: str
    landmarks: tuple[Landmark, ...]
    builder: Callable[[dict[str, np.ndarray]], tuple[list[ArmatureNode], list[Bone]]]

    def landmark(self, key: str) -> Landmark | None:
        for entry in self.landmarks:
            if entry.key == key:
                return entry
        return None

    def steps(self, mirror: bool = True, optional: bool = True) -> tuple[Landmark, ...]:
        """The landmarks worth asking for under these choices.

        With mirroring on the reflected half drops out of the walk: the artist
        places one side and the other follows, which is the difference between
        nineteen placements and thirty-three.
        """
        return tuple(
            entry
            for entry in self.landmarks
            if (optional or entry.required) and not (mirror and entry.mirror_of)
        )

    def centre_keys(self) -> tuple[str, ...]:
        """The midline landmarks, which are what the median plane is fitted to."""
        return tuple(entry.key for entry in self.landmarks if entry.side is Side.CENTRE)

    def build(self, placed: dict[str, np.ndarray]) -> tuple[list[ArmatureNode], list[Bone]]:
        return self.builder(placed)


# ----------------------------------------------------------------------
# The median plane
# ----------------------------------------------------------------------


def median_plane(points) -> tuple[np.ndarray, np.ndarray] | None:
    """The plane of symmetry through the midline points, as ``(origin, normal)``.

    Least squares: the normal is the direction the points vary least along.
    Returns ``None`` when they are too nearly a straight line to say -- the
    midline of a figure very nearly is one, and it is only the front points
    (the jugular notch, the pubic symphysis) set against the back ones (C7,
    T12) that open it out into a plane.  Guessing from a line would mirror the
    whole figure into the wrong place, so this refuses instead.
    """
    cloud = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    if len(cloud) < 3:
        return None
    origin = cloud.mean(axis=0)
    _, spread, directions = np.linalg.svd(cloud - origin, full_matrices=False)
    if spread[0] <= 0.0 or spread[1] <= PLANE_SPREAD * spread[0]:
        return None
    normal = directions[2]
    length = float(np.linalg.norm(normal))
    if length <= 0.0:
        return None
    return origin, normal / length


def mirror_point(point, origin, normal) -> np.ndarray:
    """Reflect a point across the plane through ``origin`` with ``normal``."""
    point = np.asarray(point, dtype=np.float64)
    origin = np.asarray(origin, dtype=np.float64)
    normal = np.asarray(normal, dtype=np.float64)
    length = float(np.linalg.norm(normal))
    if length <= 0.0:
        return point.copy()
    normal = normal / length
    return point - 2.0 * float(np.dot(point - origin, normal)) * normal


# ----------------------------------------------------------------------
# The humanoid landmarks
# ----------------------------------------------------------------------

#: ``(key, name, hint)`` for the midline, top to bottom.  Two of these are on
#: the back and two on the front, which is what keeps the median plane honest.
_CENTRE: tuple[tuple[str, str, str], ...] = (
    ("vertex", "Vertex", "The highest point of the skull."),
    (
        "c7",
        "C7 spinous process",
        "The bump at the base of the neck, clearest when the head drops forward.",
    ),
    (
        "jugular_notch",
        "Jugular notch",
        "The hollow between the collarbones, at the top of the breastbone.",
    ),
    (
        "t12",
        "Thoracolumbar junction",
        "In the back, level with the lowest rib: the waist of the ribcage.",
    ),
    ("pubic_symphysis", "Pubic symphysis", "The front edge of the pelvic floor, on the midline."),
)

#: ``(key, name, hint, required)`` for the paired landmarks, top to bottom.
_PAIRED: tuple[tuple[str, str, str, bool], ...] = (
    ("mastoid", "Mastoid process", "The knob of bone just behind the ear lobe.", False),
    ("acromion", "Acromion", "The flat bony corner at the top outside of the shoulder.", True),
    (
        "sternoclavicular",
        "Sternoclavicular joint",
        "Where the collarbone meets the breastbone, to one side of the notch.",
        False,
    ),
    ("humerus_lateral_epicondyle", "Lateral epicondyle", "The outside of the elbow.", True),
    (
        "humerus_medial_epicondyle",
        "Medial epicondyle",
        "The inside of the elbow: the funny bone.",
        True,
    ),
    ("radial_styloid", "Radial styloid", "The thumb-side bump of the wrist.", True),
    ("ulnar_styloid", "Ulnar styloid", "The little-finger-side bump of the wrist.", True),
    ("third_metacarpal_head", "Third knuckle", "The middle knuckle of a closed fist.", True),
    ("iliac_crest", "Iliac crest", "The highest point of the rim of the hip bone.", False),
    ("asis", "ASIS", "The front point of the hip bone, under the pocket.", True),
    ("psis", "PSIS", "The dimple above the buttock.", True),
    ("greater_trochanter", "Greater trochanter", "The broad bump on the outside of the hip.", True),
    ("femur_lateral_epicondyle", "Lateral femoral epicondyle", "The outside of the knee.", True),
    ("femur_medial_epicondyle", "Medial femoral epicondyle", "The inside of the knee.", True),
    (
        "lateral_malleolus",
        "Lateral malleolus",
        "The outside ankle bone, the lower of the two.",
        True,
    ),
    ("medial_malleolus", "Medial malleolus", "The inside ankle bone, the higher of the two.", True),
    (
        "second_metatarsal_head",
        "Ball of the foot",
        "Behind the second toe, where the foot takes weight.",
        True,
    ),
    ("calcaneal_tuberosity", "Heel", "The back of the heel bone.", False),
)


def _humanoid_landmarks() -> tuple[Landmark, ...]:
    """The midline first, then each pair left before right."""
    entries = [
        Landmark(key=key, name=name, hint=hint, side=Side.CENTRE) for key, name, hint in _CENTRE
    ]
    for key, name, hint, required in _PAIRED:
        entries.append(
            Landmark(key=f"{key}.L", name=name, hint=hint, side=Side.LEFT, required=required)
        )
        entries.append(
            Landmark(
                key=f"{key}.R",
                name=name,
                hint=hint,
                side=Side.RIGHT,
                required=required,
                mirror_of=f"{key}.L",
            )
        )
    return tuple(entries)


HUMANOID_LANDMARKS = _humanoid_landmarks()


# ----------------------------------------------------------------------
# Building the humanoid armature
# ----------------------------------------------------------------------


def _mid(first, second) -> np.ndarray:
    return (np.asarray(first, dtype=np.float64) + np.asarray(second, dtype=np.float64)) * 0.5


def _span(first, second) -> float:
    return float(np.linalg.norm(np.subtract(second, first)))


class _Build:
    """Somewhere to collect nodes while the rules that need each other run."""

    def __init__(self, placed: dict[str, np.ndarray]) -> None:
        self._placed = placed
        self.points: dict[str, np.ndarray] = {}
        self.sizes: dict[str, float] = {}

    def at(self, *keys: str) -> tuple[np.ndarray, ...] | None:
        """Every named landmark, or ``None`` when any one of them is missing."""
        found = []
        for key in keys:
            value = self._placed.get(key)
            if value is None:
                return None
            found.append(np.asarray(value, dtype=np.float64))
        return tuple(found)

    def add(self, role: str, point, size: float = 0.0) -> None:
        self.points[role] = np.asarray(point, dtype=np.float64)
        self.sizes[role] = max(float(size), 0.0)

    def size(self, role: str, share: float = 1.0) -> float:
        return self.sizes.get(role, 0.0) * share

    def has(self, role: str) -> bool:
        return role in self.points


def _build_torso(build: _Build) -> None:
    """The midline chain, from the pelvis up to the crown."""
    shoulders = build.at("acromion.L", "acromion.R")
    chest_size = JOINT_RADIUS * _span(*shoulders) if shoulders is not None else 0.0

    pelvis_points = build.at("asis.L", "asis.R", "psis.L", "psis.R")
    if pelvis_points is not None:
        asis_left, asis_right = pelvis_points[0], pelvis_points[1]
        build.add(
            "pelvis",
            np.mean(np.stack(pelvis_points), axis=0),
            JOINT_RADIUS * _span(asis_left, asis_right),
        )

    ribcage = build.at("jugular_notch", "c7")
    if ribcage is not None:
        jugular, c7 = ribcage
        build.add("chest", _mid(jugular, c7), chest_size)
        build.add("neck", c7, JOINT_RADIUS * chest_size)
        waist = build.at("t12")
        if waist is not None:
            build.add(
                "spine",
                waist[0] + SPINE_FORWARD * (jugular - c7),
                (chest_size + build.size("pelvis")) * 0.5,
            )

    mastoids = build.at("mastoid.L", "mastoid.R")
    skull = build.at("vertex", "c7")
    if mastoids is not None:
        build.add("head", _mid(*mastoids), JOINT_RADIUS * _span(*mastoids))
    elif skull is not None:
        vertex, c7 = skull
        build.add(
            "head",
            c7 + HEAD_UP_FROM_NECK * (vertex - c7),
            JOINT_RADIUS * HEAD_UP_FROM_NECK * _span(vertex, c7),
        )

    crown = build.at("vertex")
    if crown is not None:
        build.add("head_top", crown[0], build.size("head", END_SHARE))


def _build_arm(build: _Build, side: str) -> None:
    """One arm, shoulder to hand.  The shoulder needs the elbow, so it waits."""
    elbow = build.at(f"humerus_medial_epicondyle.{side}", f"humerus_lateral_epicondyle.{side}")
    if elbow is not None:
        build.add(f"elbow.{side}", _mid(*elbow), JOINT_RADIUS * _span(*elbow))

    wrist = build.at(f"radial_styloid.{side}", f"ulnar_styloid.{side}")
    if wrist is not None:
        build.add(f"wrist.{side}", _mid(*wrist), JOINT_RADIUS * _span(*wrist))

    hand = build.at(f"third_metacarpal_head.{side}")
    if hand is not None:
        build.add(f"hand.{side}", hand[0], build.size(f"wrist.{side}", END_SHARE))

    acromion = build.at(f"acromion.{side}")
    if acromion is None or not build.has("chest"):
        return
    corner, chest = acromion[0], build.points["chest"]
    joint = corner + SHOULDER_INTO_TRUNK * (chest - corner)
    if build.has(f"elbow.{side}"):
        joint = joint + SHOULDER_DOWN_ARM * (build.points[f"elbow.{side}"] - corner)
    build.add(f"shoulder.{side}", joint, JOINT_RADIUS * _span(corner, chest))

    collar = build.at(f"sternoclavicular.{side}")
    if collar is not None:
        build.add(f"clavicle.{side}", collar[0], build.size(f"shoulder.{side}", END_SHARE))


def _build_leg(build: _Build, side: str) -> None:
    """One leg, hip to foot.  The hip needs the pelvis, so it waits."""
    knee = build.at(f"femur_medial_epicondyle.{side}", f"femur_lateral_epicondyle.{side}")
    if knee is not None:
        build.add(f"knee.{side}", _mid(*knee), JOINT_RADIUS * _span(*knee))

    ankle = build.at(f"medial_malleolus.{side}", f"lateral_malleolus.{side}")
    if ankle is not None:
        build.add(f"ankle.{side}", _mid(*ankle), JOINT_RADIUS * _span(*ankle))

    foot = build.at(f"second_metatarsal_head.{side}")
    if foot is not None:
        build.add(f"foot.{side}", foot[0], build.size(f"ankle.{side}", END_SHARE))

    heel = build.at(f"calcaneal_tuberosity.{side}")
    if heel is not None:
        build.add(f"heel.{side}", heel[0], build.size(f"ankle.{side}", END_SHARE))

    trochanter = build.at(f"greater_trochanter.{side}")
    if trochanter is None or not build.has("pelvis"):
        return
    bump, pelvis = trochanter[0], build.points["pelvis"]
    build.add(
        f"hip.{side}",
        bump + HIP_TOWARD_PELVIS * (pelvis - bump),
        JOINT_RADIUS * _span(bump, pelvis),
    )


#: Limb roles in the order the wire runs out from the trunk.
_ARM = ("clavicle", "shoulder", "elbow", "wrist", "hand")
_LEG = ("hip", "knee", "ankle", "foot", "heel")

#: The order nodes are listed in, root first, so the panel reads top-down.
_ORDER: tuple[str, ...] = (
    "pelvis",
    "spine",
    "chest",
    "neck",
    "head",
    "head_top",
    *(f"{role}.{side}" for side in "LR" for role in _ARM),
    *(f"{role}.{side}" for side in "LR" for role in _LEG),
)

#: The names shown in the list, by role.
_NAMES: dict[str, str] = {
    "pelvis": "Pelvis",
    "spine": "Spine",
    "chest": "Chest",
    "neck": "Neck",
    "head": "Head",
    "head_top": "Crown",
    "clavicle": "Clavicle",
    "shoulder": "Shoulder",
    "elbow": "Elbow",
    "wrist": "Wrist",
    "hand": "Hand",
    "hip": "Hip",
    "knee": "Knee",
    "ankle": "Ankle",
    "foot": "Foot",
    "heel": "Heel",
}


def _node_name(role: str) -> str:
    base, _, side = role.partition(".")
    name = _NAMES.get(base, base.replace("_", " ").title())
    return f"{name} {side}" if side else name


def _humanoid_bones(build: _Build) -> list[tuple[str, str]]:
    """The roles each length of wire runs between, whether or not both exist."""
    pairs: list[tuple[str, str]] = [
        ("pelvis", "spine"),
        ("spine", "chest"),
        ("chest", "neck"),
        ("neck", "head"),
        ("head", "head_top"),
    ]
    for side in "LR":
        if build.has(f"clavicle.{side}"):
            pairs += [("neck", f"clavicle.{side}"), (f"clavicle.{side}", f"shoulder.{side}")]
        else:
            pairs.append(("neck", f"shoulder.{side}"))
        pairs += [
            (f"shoulder.{side}", f"elbow.{side}"),
            (f"elbow.{side}", f"wrist.{side}"),
            (f"wrist.{side}", f"hand.{side}"),
            ("pelvis", f"hip.{side}"),
            (f"hip.{side}", f"knee.{side}"),
            (f"knee.{side}", f"ankle.{side}"),
            (f"ankle.{side}", f"foot.{side}"),
            (f"ankle.{side}", f"heel.{side}"),
        ]
    return pairs


def build_humanoid(placed: dict[str, np.ndarray]) -> tuple[list[ArmatureNode], list[Bone]]:
    """Turn placed landmarks into a figure's armature.

    Anything whose landmarks are missing is simply left out, along with the
    bones that would have reached it, so a run abandoned half way still draws
    as far as it got rather than failing outright.
    """
    build = _Build(placed)
    _build_torso(build)
    for side in "LR":
        _build_arm(build, side)
        _build_leg(build, side)

    roles = [role for role in _ORDER if build.has(role)]
    index = {role: position for position, role in enumerate(roles)}
    nodes = [
        ArmatureNode(
            name=_node_name(role),
            at=tuple(float(value) for value in build.points[role]),
            size=build.sizes[role],
            role=role,
        )
        for role in roles
    ]
    bones = [
        Bone(index[first], index[second])
        for first, second in _humanoid_bones(build)
        if first in index and second in index
    ]
    return nodes, bones


HUMANOID = Preset(
    key="humanoid",
    name="Humanoid",
    landmarks=HUMANOID_LANDMARKS,
    builder=build_humanoid,
)

#: Every preset the guided mode offers.  More forms will join the figure here.
PRESETS: dict[str, Preset] = {HUMANOID.key: HUMANOID}


def landmark_title(armature, key: str) -> str:
    """What to call a landmark in a menu or an undo step.

    The preset's own words when it has any, the bare key otherwise -- which is
    all a freehand armature carrying stray landmarks can offer.
    """
    preset = PRESETS.get(getattr(armature, "preset", ""))
    entry = preset.landmark(key) if preset is not None else None
    return entry.title if entry is not None else key


# ----------------------------------------------------------------------
# Mirroring and re-deriving
# ----------------------------------------------------------------------


def mirror_landmarks(armature) -> list[PlacedLandmark]:
    """The landmark list with every paired landmark reflected into place.

    A point the artist has taken hold of keeps its own position for good -- the
    mirror only ever writes entries that are still its own -- so correcting one
    shoulder does not put it back the moment the other side moves.
    """
    preset = PRESETS.get(armature.preset)
    existing = {entry.key: entry for entry in armature.landmarks}
    if preset is None:
        return list(armature.landmarks)

    placed = {key: entry.point for key, entry in existing.items()}
    plane = median_plane([placed[key] for key in preset.centre_keys() if key in placed])
    if plane is None:
        return list(armature.landmarks)

    origin, normal = plane
    out = list(armature.landmarks)
    for entry in preset.landmarks:
        source = placed.get(entry.mirror_of) if entry.mirror_of else None
        if source is None:
            continue
        already = existing.get(entry.key)
        if already is not None and not already.mirrored:
            continue
        at = tuple(float(value) for value in mirror_point(source, origin, normal))
        if already is None:
            out.append(PlacedLandmark(key=entry.key, at=at, mirrored=True))
        else:
            already.at = at
    return out


def rebuild(armature) -> tuple[list[ArmatureNode], list[Bone]] | None:
    """The nodes and bones an armature's landmarks now imply.

    A node's name and padlock always carry over, and a locked node keeps its
    place and its size as well: one padlock, one meaning, which is *leave this
    one alone*.  Returns ``None`` when there is no preset to rebuild from.
    """
    preset = PRESETS.get(armature.preset)
    if preset is None:
        return None
    nodes, bones = preset.build(armature.placed_points())
    for node in nodes:
        kept = armature.node_for_role(node.role)
        if kept is None:
            continue
        node.name = kept.name
        node.locked = kept.locked
        if kept.locked:
            node.at = kept.at
            node.size = kept.size
    return nodes, bones
