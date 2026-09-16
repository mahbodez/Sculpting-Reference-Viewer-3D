"""Where skeletons come from: an armature, a preset, or the names in a file.

Three ways to arrive at a :class:`~refview.core.skeleton.Skeleton` that were
not "the model came with one":

* **Out of an armature.**  An armature is a graph and a skeleton is a tree, so
  the conversion is a spanning tree grown from a root.  A humanoid armature
  has a pelvis to grow from and no loops, and comes across whole.  A freehand
  one is grown from whichever node the artist picked -- or, failing that, the
  best-connected one -- and any bone that would close a loop is left out and
  counted, so the panel can say how many.  The reverse direction is simple:
  every joint is a node, every parent-child pair a bone.

* **A humanoid preset**, proportioned to the model's height: eight heads
  tall, feet at the bottom of the model's box, facing +Z.  It is a starting
  point to be fitted, not a fit -- the guided armature is the way to measure
  a figure, and a skeleton grown out of *that* stands where the model does.

* **The names in a file.**  Rigs from Mixamo, 3ds Max's Biped, Unreal,
  Blender's Rigify and Character Creator all name their joints differently
  and all name them recognisably, so a skeleton read out of a glTF can
  usually be told which joint is which.  :func:`humanoid_roles` guesses,
  and the guess is offered rather than imposed.  The role vocabulary is the
  armature's, so a mapped skeleton converts into an armature the clay modes
  already understand, and a Biped or any other rig that arrives later only
  needs its names added to the table.
"""

from __future__ import annotations

import re
from dataclasses import replace

import numpy as np

from .armature import Armature, ArmatureNode, Bone
from .landmarks import role_name
from .skeleton import Joint, Skeleton, make_joint

# ----------------------------------------------------------------------
# The humanoid
# ----------------------------------------------------------------------

#: Which joint each humanoid role hangs from.  The same tree the guided
#: armature's bones describe, so the two agree about what a figure is.
HUMANOID_PARENTS: dict[str, str] = {
    "pelvis": "",
    "spine": "pelvis",
    "chest": "spine",
    "neck": "chest",
    "head": "neck",
    "head_top": "head",
    **{f"clavicle.{s}": "neck" for s in "LR"},
    **{f"shoulder.{s}": f"clavicle.{s}" for s in "LR"},
    **{f"elbow.{s}": f"shoulder.{s}" for s in "LR"},
    **{f"wrist.{s}": f"elbow.{s}" for s in "LR"},
    **{f"hand.{s}": f"wrist.{s}" for s in "LR"},
    **{f"hip.{s}": "pelvis" for s in "LR"},
    **{f"knee.{s}": f"hip.{s}" for s in "LR"},
    **{f"ankle.{s}": f"knee.{s}" for s in "LR"},
    **{f"foot.{s}": f"ankle.{s}" for s in "LR"},
    **{f"heel.{s}": f"ankle.{s}" for s in "LR"},
}

#: The humanoid roles in the order a figure is read: trunk, then limbs.
HUMANOID_ROLES: tuple[str, ...] = tuple(HUMANOID_PARENTS)

#: Where each joint of a standing figure sits, as shares of its height, with
#: +Y up, +Z forward and +X out to the figure's left.  Paired roles are given
#: for the left and mirrored.  An eight-head canon: the pelvis at the half,
#: the shoulders a head and a half down from the crown.
_HUMANOID_SHARES: dict[str, tuple[float, float, float]] = {
    "pelvis": (0.0, 0.53, 0.0),
    "spine": (0.0, 0.62, 0.0),
    "chest": (0.0, 0.72, 0.0),
    "neck": (0.0, 0.815, 0.0),
    "head": (0.0, 0.88, 0.01),
    "head_top": (0.0, 1.0, 0.0),
    "clavicle": (0.03, 0.81, 0.015),
    "shoulder": (0.11, 0.80, 0.0),
    "elbow": (0.13, 0.62, 0.0),
    "wrist": (0.145, 0.47, 0.0),
    "hand": (0.15, 0.40, 0.0),
    "hip": (0.06, 0.50, 0.0),
    "knee": (0.07, 0.28, 0.0),
    "ankle": (0.075, 0.04, 0.0),
    "foot": (0.075, 0.01, 0.10),
    "heel": (0.075, 0.01, -0.04),
}

#: How thick each joint draws, as a share of the height.
_HUMANOID_RADII: dict[str, float] = {
    "pelvis": 0.085,
    "spine": 0.075,
    "chest": 0.095,
    "neck": 0.035,
    "head": 0.065,
    "head_top": 0.05,
    "clavicle": 0.03,
    "shoulder": 0.04,
    "elbow": 0.03,
    "wrist": 0.022,
    "hand": 0.02,
    "hip": 0.05,
    "knee": 0.04,
    "ankle": 0.03,
    "foot": 0.025,
    "heel": 0.02,
}


def humanoid_positions(height: float, feet=(0.0, 0.0, 0.0)) -> dict[str, np.ndarray]:
    """Every humanoid role's place for a figure this tall standing on ``feet``."""
    feet = np.asarray(feet, dtype=np.float64)
    out: dict[str, np.ndarray] = {}
    for role in HUMANOID_ROLES:
        base, _, side = role.partition(".")
        x, y, z = _HUMANOID_SHARES[base]
        if side == "R":
            x = -x
        out[role] = feet + np.array([x, y, z]) * float(height)
    return out


def build_humanoid_skeleton(
    height: float, feet=(0.0, 0.0, 0.0), name: str = "Humanoid"
) -> Skeleton:
    """A proportioned humanoid skeleton, roles and all, standing on ``feet``."""
    height = max(float(height), 1e-6)
    at = humanoid_positions(height, feet)
    index = {role: position for position, role in enumerate(HUMANOID_ROLES)}
    joints: list[Joint] = []
    for role in HUMANOID_ROLES:
        parent_role = HUMANOID_PARENTS[role]
        parent = index[parent_role] if parent_role else -1
        local = at[role] - (at[parent_role] if parent_role else 0.0)
        joints.append(
            make_joint(
                role_name(role),
                parent,
                local,
                role=role,
                radius=_HUMANOID_RADII[role.partition(".")[0]] * height,
            )
        )
    return Skeleton(name=name, joints=joints)


# ----------------------------------------------------------------------
# Armature <-> skeleton
# ----------------------------------------------------------------------


def armature_root(armature: Armature, preferred: int | None = None) -> int | None:
    """Which node a skeleton grown out of an armature hangs from.

    The one the artist picked if they picked one; else the pelvis, which is
    where a figure is weighed from; else the best-connected node, which on
    a freehand wire is usually the trunk.
    """
    if not armature.nodes:
        return None
    if preferred is not None and 0 <= preferred < len(armature.nodes):
        return preferred
    pelvis = next((i for i, node in enumerate(armature.nodes) if node.role == "pelvis"), None)
    if pelvis is not None:
        return pelvis
    degrees = [len(armature.neighbours(i)) for i in range(len(armature.nodes))]
    return int(np.argmax(degrees))


def skeleton_from_armature(
    armature: Armature, root: int | None = None
) -> tuple[Skeleton, int]:
    """A skeleton grown out of an armature, and how many bones did not fit.

    Breadth first from the root, so each node hangs from the neighbour
    nearest the root.  A node the root cannot reach starts a tree of its own.
    A bone joining two nodes already placed would close a loop, which a
    skeleton has no way to say, and is dropped; the count comes back so the
    panel can tell the artist.  Every joint's rest frame is the scene's own,
    with only a position in it, so the pose sliders read as world turns.
    """
    count = len(armature.nodes)
    skeleton = Skeleton(name=armature.name, color=armature.color)
    if count == 0:
        return skeleton, 0
    start = armature_root(armature, root)
    assert start is not None

    order: list[int] = []
    parent_of: dict[int, int] = {}
    kept_bones = 0
    seen: set[int] = set()
    roots = [start, *(i for i in range(count) if i != start)]
    for candidate in roots:
        if candidate in seen:
            continue
        queue = [candidate]
        seen.add(candidate)
        parent_of[candidate] = -1
        while queue:
            here = queue.pop(0)
            order.append(here)
            for other in armature.neighbours(here):
                if other in seen:
                    continue
                seen.add(other)
                parent_of[other] = here
                kept_bones += 1
                queue.append(other)

    position = {node: slot for slot, node in enumerate(order)}
    at = armature.node_array
    joints: list[Joint] = []
    for node_index in order:
        node = armature.nodes[node_index]
        parent = parent_of[node_index]
        local = at[node_index] - (at[parent] if parent >= 0 else 0.0)
        joints.append(
            make_joint(
                node.name,
                position[parent] if parent >= 0 else -1,
                local,
                role=node.role,
                radius=float(node.size),
                locked=node.locked,
            )
        )
    skeleton.joints = joints
    dropped = len(armature.intact_bones()) - kept_bones
    return skeleton, max(dropped, 0)


def armature_from_skeleton(skeleton: Skeleton) -> Armature:
    """The armature a skeleton stands for: joints as nodes, bones as bones.

    The nodes land where the joints are *posed*, since what the artist sees
    is what they mean to measure.  Roles carry across, so an armature out of
    a mapped rig is one the clay modes can read a figure off; the landmarks
    do not, because nothing was ever pointed at.
    """
    at = skeleton.positions()
    nodes = [
        ArmatureNode(
            name=joint.name,
            at=tuple(float(v) for v in at[index]),
            size=float(joint.radius),
            role=joint.role,
            locked=joint.locked,
        )
        for index, joint in enumerate(skeleton.joints)
    ]
    bones = [
        Bone(parent, child, f"{skeleton.joints[parent].name} to {skeleton.joints[child].name}")
        for parent, child in skeleton.bones()
    ]
    return Armature(name=skeleton.name, nodes=nodes, bones=bones, color=skeleton.color)


# ----------------------------------------------------------------------
# Reading roles off names
# ----------------------------------------------------------------------

#: Prefixes rigs put on every joint, dropped before anything is read.
_PREFIXES: tuple[str, ...] = (
    "mixamorig",
    "bip001",
    "bip01",
    "bip",
    "def-",
    "def_",
    "character1_",
    "cc_base_",
    "j_bip_",
    "armature|",
    "root|",
    "valvebiped.",
)

_SIDE_TOKENS: dict[str, str] = {
    "l": "L",
    "left": "L",
    "lft": "L",
    "lf": "L",
    "r": "R",
    "right": "R",
    "rgt": "R",
    "rt": "R",
}

#: ``(role, needs a side, pattern)``: the pattern is matched whole against
#: the name with its prefix, its side and every separator taken out.  First
#: match wins, so the specific comes before the general.
_ROLE_PATTERNS: tuple[tuple[str, bool, str], ...] = (
    ("head_top", False, r"(headtop|headtopend|headend|crown|skulltop)"),
    ("head", False, r"head\d*"),
    ("neck", False, r"neck(twist)?\d*"),
    ("chest", False, r"(chest|upperchest|ribcage|torso)"),
    ("spine", False, r"spine\d*"),
    ("pelvis", False, r"(hips?|pelvis|cog|body|waist)"),
    ("clavicle", True, r"(clavicle|collar|collarbone|shoulder|shoulderblade)"),
    ("shoulder", True, r"(upperarm|uparm|arm|humerus|upperarm\d*)"),
    ("elbow", True, r"(forearm|lowerarm|lowarm|elbow|ulna)"),
    (
        "hand",
        True,
        r"(handmiddle1|handmiddle01|middle01|middle1|mid1|mid01|fmiddle01|finger2|finger21)",
    ),
    ("wrist", True, r"(hand|wrist)"),
    ("hip", True, r"(upleg|thigh|upperleg|hip|femur|leg\d*up)"),
    ("knee", True, r"(leg|calf|shin|lowerleg|lowleg|knee|tibia)"),
    ("ankle", True, r"(foot|ankle)"),
    ("foot", True, r"(toebase|toe|toes|ball|toe0|toe1|toes0)"),
    ("heel", True, r"heel\w*"),
)

_CAMEL = re.compile(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Za-z])")
_SEPARATORS = re.compile(r"[^a-z0-9]+")


def _tokens(name: str) -> list[str]:
    """A joint name broken into lower-case words.

    ``LeftUpLeg`` is ``left up leg``; ``mixamorig:Spine1`` is ``spine 1``;
    ``Bip01 L Thigh`` is ``l thigh``; ``upper_arm.L`` is ``upper arm l``.
    """
    text = name.strip()
    lowered = text.lower()
    for prefix in _PREFIXES:
        if lowered.startswith(prefix):
            text = text[len(prefix) :]
            break
    text = _CAMEL.sub(" ", text)
    return [token for token in _SEPARATORS.split(text.lower()) if token]


def read_role(name: str) -> str:
    """The humanoid role a joint name suggests, or empty when it says nothing."""
    tokens = _tokens(name)
    if not tokens:
        return ""
    side = ""
    rest: list[str] = []
    for token in tokens:
        found = _SIDE_TOKENS.get(token)
        if found and not side:
            side = found
        else:
            rest.append(token)
    compact = "".join(rest)
    # A number stuck to a word is part of the word (``spine1``), but a number
    # standing alone is a chain index and says nothing about the role.
    for role, needs_side, pattern in _ROLE_PATTERNS:
        if not re.fullmatch(pattern, compact):
            continue
        if needs_side and not side:
            return ""
        if not needs_side and side:
            return ""
        return f"{role}.{side}" if needs_side else role
    return ""


def humanoid_roles(skeleton: Skeleton) -> dict[int, str]:
    """A guess at which joint fills which humanoid slot, from the names alone.

    Where several joints claim one slot -- three spines, two necks -- the one
    nearest the root takes it, except that the last of a spine chain is the
    chest when nothing else is, and the crown is the deepest of the heads'
    ends.  Each slot is filled at most once and each joint fills at most one.
    """
    claims: dict[str, list[int]] = {}
    for index, joint in enumerate(skeleton.joints):
        role = read_role(joint.name or joint.source)
        if role:
            claims.setdefault(role, []).append(index)

    depth = {index: skeleton.depth(index) for index in range(len(skeleton.joints))}
    chosen: dict[str, int] = {}
    for role, indices in claims.items():
        ordered = sorted(indices, key=lambda i: (depth[i], i))
        chosen[role] = ordered[-1] if role == "head_top" else ordered[0]

    spines = sorted(claims.get("spine", []), key=lambda i: (depth[i], i))
    if len(spines) >= 2 and "chest" not in chosen:
        chosen["chest"] = spines[-1]

    taken: set[int] = set()
    out: dict[int, str] = {}
    for role in HUMANOID_ROLES:
        index = chosen.get(role)
        if index is not None and index not in taken:
            taken.add(index)
            out[index] = role
    return out


# ----------------------------------------------------------------------
# Simplifying
# ----------------------------------------------------------------------

#: Words in a joint's name that mark it as detail a figure is posed without:
#: the fingers, the face, the breasts, and the helper bones a game rig
#: carries to spread a twist or drive a correction.  Whole words, after the
#: name is broken up, so that ``forearm`` is never read as an ``ear``.
_DETAIL_WORDS: dict[str, frozenset[str]] = {
    "fingers": frozenset({
        "index", "middle", "mid", "ring", "pinky", "pinkie", "little", "thumb",
        "finger", "fingers", "metacarpal", "palm",
    }),
    "face": frozenset({
        "facial", "face", "jaw", "jawroot", "upperjaw", "lowerjaw", "tongue", "teeth",
        "tooth", "eye", "eyes", "eyelid", "eyelids", "eyeball", "eyeballs", "brow", "brows",
        "eyebrow", "lip", "lips", "cheek", "cheeks", "nose", "nostril", "ear", "ears",
        "mouth", "chin", "forehead", "hair", "beard", "moustache", "mustache",
    }),
    "breasts": frozenset({"breast", "breasts", "pectoral", "pec", "pecs", "boob", "bust"}),
    "helpers": frozenset({
        "twist", "share", "sharebone", "roll", "helper", "ik", "fk", "target", "pole",
        "nub", "end", "effector", "ctrl", "control", "driver", "tweak", "mch", "dummy",
        "null", "pivot", "catcher", "shadow", "prop", "weapon", "attach", "socket",
        "tail", "wing", "wings", "cloth", "skirt", "cape",
    }),
}


def detail_joints(skeleton: Skeleton) -> dict[int, str]:
    """Which joints are detail, and which kind, read off their names.

    A toe past the ball is a toe by any of its words, and a chain of them
    comes out whole because every link says so.  A joint carrying a
    humanoid role is never detail whatever its name -- the ball of the foot
    is a *toe base*, the wrist a *hand*, the crown a *head top end* -- and
    nor is anything a role'd joint hangs from, since taking that out would
    re-hang the figure itself.
    """
    if not skeleton.joints:
        return {}
    kept: set[int] = set()
    for index, joint in enumerate(skeleton.joints):
        if not joint.role:
            continue
        walk = index
        seen: set[int] = set()
        while 0 <= walk < len(skeleton.joints) and walk not in seen:
            kept.add(walk)
            seen.add(walk)
            walk = skeleton.joints[walk].parent
    found: dict[int, str] = {}
    for index, joint in enumerate(skeleton.joints):
        if index in kept:
            continue
        words = set(_tokens(joint.name or joint.source)) - set(_SIDE_TOKENS)
        # A toe is detail when its name says which toe -- ``BigToe1``,
        # ``IndexToe`` -- or that it is an end.  ``Toe``, ``ToeBase`` and
        # ``Toe0`` are the ball of the foot, which a figure stands on.
        if words & {"toe", "toes"}:
            extra = {word for word in words - {"toe", "toes", "base", "ball"} if not word.isdigit()}
            if extra:
                found[index] = "toes"
                continue
        for kind, marks in _DETAIL_WORDS.items():
            if words & marks:
                found[index] = kind
                break
    return found


def simplified(skeleton: Skeleton) -> tuple[list[Joint], dict[str, int]]:
    """The joint list with the detail taken out, and how much of each kind went.

    What is left is the figure a pose is read from: the trunk, the limbs,
    the head, the hands and the feet.  The skin weights of what went fold
    onto the nearest joint that stayed, so a model still follows.
    """
    detail = detail_joints(skeleton)
    counts: dict[str, int] = {}
    for kind in detail.values():
        counts[kind] = counts.get(kind, 0) + 1
    return skeleton.without_joints(detail), counts


def looks_humanoid(roles: dict[int, str]) -> bool:
    """Whether a guessed mapping is enough of a figure to be worth offering."""
    found = set(roles.values())
    has_trunk = "pelvis" in found or "spine" in found
    has_legs = any(role.startswith("hip.") or role.startswith("knee.") for role in found)
    has_arms = any(role.startswith("shoulder.") or role.startswith("elbow.") for role in found)
    return has_trunk and has_legs and has_arms and len(found) >= 6


def with_roles(skeleton: Skeleton, roles: dict[int, str]) -> list[Joint]:
    """The joint list with these roles written in, and every other role cleared."""
    return [
        replace(joint, role=roles.get(index, ""))
        for index, joint in enumerate(skeleton.joints)
    ]
