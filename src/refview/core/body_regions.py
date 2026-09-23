"""Where on the body a point of the skin is, so that the skin can be marked as skin is.

Acne gathers on the face, the chest and the back; moles and freckles on
the arms and the shoulders the sun reaches; the knuckles and the feet run
redder than the forearm; the forehead shines where the calf does not.  A
skin shader that drops the same marks everywhere reads as a texture; one
that knows a hand from a cheek reads as a body.  A reference mesh carries
no such knowledge, so it is worked out here, as well as it can be, from
what the scene does know:

* **The skeleton**, when there is one with humanoid roles -- a rig read by
  its names, the humanoid preset, one grown out of the guided armature --
  says exactly where the limbs are.  Each point of the skin goes to the
  region of the bone nearest it, softened between bones.
* **Height bands** otherwise: a standing figure is eight heads tall, and
  the canon says where the feet, the legs, the torso, the neck and the
  head fall as shares of that height.  Arms and hands cannot be told this
  way and are counted with whatever they hang beside.
* **The whole model as one region**, for a bust, a hand or a foot.

The result is a small volume over the scene, a few weights per voxel,
which the shader reads at the world position it is shading; no UV layout
and no per-vertex attribute is needed, and the same map serves however the
scene is joined and however many objects it holds.  What each region does
to each kind of mark is a table of multipliers, :class:`RegionProfile`,
that the artist can edit and the shader reads as uniforms.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields, replace
from enum import Enum

import numpy as np

from .mesh import Mesh

#: The regions, in the order the map stores their weights.
REGIONS: tuple[str, ...] = ("head", "neck", "torso", "arms", "hands", "legs", "feet")
REGION_LABELS: dict[str, str] = {
    "head": "Head and face",
    "neck": "Neck",
    "torso": "Torso, chest and back",
    "arms": "Arms",
    "hands": "Hands",
    "legs": "Legs",
    "feet": "Feet",
}
#: Weights stored in the map: seven regions and, last, how much of the
#: point is assigned at all.  Two RGBA volumes' worth.
MAP_CHANNELS = 8

#: Which region the bone *ending* at a humanoid role lies in.  The bone
#: from the neck to the head is the neck; the one from the head to its top
#: is the head; the one from the hip to the knee is the thigh.
ROLE_REGIONS: dict[str, str] = {
    "pelvis": "torso",
    "spine": "torso",
    "chest": "torso",
    "neck": "torso",
    "head": "neck",
    "head_top": "head",
    "clavicle": "torso",
    "shoulder": "torso",
    "elbow": "arms",
    "wrist": "arms",
    "hand": "hands",
    "hip": "torso",
    "knee": "legs",
    "ankle": "legs",
    "foot": "feet",
    "heel": "feet",
}

#: Where the bands of a standing figure begin, as shares of its height,
#: from the ground up: the feet, then the legs, the torso, the neck and the
#: head.  The eight-head canon the humanoid preset is proportioned to.
BAND_REGIONS: tuple[str, ...] = ("feet", "legs", "torso", "neck", "head")
BAND_EDGES: tuple[float, ...] = (0.05, 0.50, 0.815, 0.865)
#: Half the width of the blend between two bands, as a share of the height.
BAND_SOFTNESS = 0.025


class RegionSource(str, Enum):
    """Where the region map comes from."""

    #: A skeleton with humanoid roles, when the scene has one; else bands.
    AUTO = "auto"
    BANDS = "bands"
    WHOLE = "whole"
    OFF = "off"

    @property
    def label(self) -> str:
        return {
            RegionSource.AUTO: "Skeleton, else height bands",
            RegionSource.BANDS: "Height bands of a standing figure",
            RegionSource.WHOLE: "The whole model is one region",
            RegionSource.OFF: "Off (effects fall evenly)",
        }[self]


@dataclass
class RegionProfile:
    """How much of each skin effect one region gets, relative to its slider."""

    acne: float = 1.0
    nevi: float = 1.0
    freckles: float = 1.0
    blemishes: float = 1.0
    oil: float = 1.0
    blood: float = 1.0
    veins: float = 1.0

    def bounded(self) -> RegionProfile:
        out = replace(self)
        for item in fields(self):
            value = getattr(self, item.name)
            try:
                value = float(value)
            except (TypeError, ValueError):
                value = 1.0
            if not np.isfinite(value):
                value = 1.0
            setattr(out, item.name, min(max(value, PROFILE_RANGE[0]), PROFILE_RANGE[1]))
        return out


#: How far a region's multiplier can be turned.
PROFILE_RANGE = (0.0, 3.0)

#: The multiplier fields of a profile, in the order the panel lists them.
PROFILE_FIELDS: tuple[str, ...] = tuple(item.name for item in fields(RegionProfile))
PROFILE_LABELS: dict[str, str] = {
    "acne": "Acne",
    "nevi": "Moles",
    "freckles": "Freckles",
    "blemishes": "Blemishes",
    "oil": "Oily highlights",
    "blood": "Blood / flush",
    "veins": "Subtle veins",
}


def _default_profiles() -> dict[str, RegionProfile]:
    """Starting values for skin effects across a generic body."""
    return {
        "head": RegionProfile(acne=1.0, nevi=0.7, freckles=1.5, blemishes=1.0, oil=1.6,
                              blood=1.2, veins=0.75),
        "neck": RegionProfile(acne=0.5, nevi=0.8, freckles=0.8, blemishes=0.8, oil=0.9,
                              blood=1.0, veins=0.9),
        "torso": RegionProfile(acne=0.8, nevi=1.2, freckles=0.6, blemishes=0.8, oil=0.7,
                               blood=0.9, veins=0.65),
        "arms": RegionProfile(acne=0.15, nevi=1.1, freckles=1.3, blemishes=0.7, oil=0.4,
                              blood=0.9, veins=1.15),
        "hands": RegionProfile(acne=0.0, nevi=0.4, freckles=0.7, blemishes=0.5, oil=0.2,
                               blood=1.4, veins=1.5),
        "legs": RegionProfile(acne=0.15, nevi=0.8, freckles=0.5, blemishes=0.9, oil=0.3,
                              blood=0.8, veins=0.9),
        "feet": RegionProfile(acne=0.0, nevi=0.3, freckles=0.2, blemishes=0.6, oil=0.1,
                              blood=1.3, veins=1.25),
    }


@dataclass
class BodyRegionSettings:
    """Where the regions come from, and what each does to the skin effects."""

    source: RegionSource = RegionSource.AUTO
    #: The region the whole model is, under :attr:`RegionSource.WHOLE`.
    whole: str = "head"
    head: RegionProfile = field(default_factory=lambda: _default_profiles()["head"])
    neck: RegionProfile = field(default_factory=lambda: _default_profiles()["neck"])
    torso: RegionProfile = field(default_factory=lambda: _default_profiles()["torso"])
    arms: RegionProfile = field(default_factory=lambda: _default_profiles()["arms"])
    hands: RegionProfile = field(default_factory=lambda: _default_profiles()["hands"])
    legs: RegionProfile = field(default_factory=lambda: _default_profiles()["legs"])
    feet: RegionProfile = field(default_factory=lambda: _default_profiles()["feet"])

    def profile(self, region: str) -> RegionProfile:
        return getattr(self, region)

    def multipliers(self, effect: str) -> list[float]:
        """One region's multiplier for ``effect`` after another, in :data:`REGIONS` order."""
        return [float(getattr(self.profile(region), effect)) for region in REGIONS]

    def bounded(self) -> BodyRegionSettings:
        out = replace(self)
        try:
            out.source = RegionSource(self.source)
        except ValueError:
            out.source = RegionSource.AUTO
        out.whole = self.whole if self.whole in REGIONS else "head"
        for region in REGIONS:
            profile = getattr(self, region)
            if not isinstance(profile, RegionProfile):
                profile = _default_profiles()[region]
            setattr(out, region, profile.bounded())
        return out


# ----------------------------------------------------------------------
# Working the regions out
# ----------------------------------------------------------------------


def role_bones(skeleton) -> np.ndarray:
    """The bones a skeleton's humanoid roles describe, as ``(count, 7)`` rows.

    Each row is where a bone starts, where it ends and the index of its
    region.  A bone runs from a joint with a role to its nearest ancestor
    with one, so a file rig's unnamed helper joints in between are stepped
    over; a role'd root is a bone of no length, so a lone pelvis still
    claims the skin round it.  Empty for a skeleton without roles.
    """
    joints = list(getattr(skeleton, "joints", []))
    if not joints:
        return np.zeros((0, 7), dtype=np.float64)
    positions = np.asarray(skeleton.positions(), dtype=np.float64)
    rows: list[list[float]] = []
    for index, joint in enumerate(joints):
        # A paired role is ``knee.L``; the side says nothing about the region.
        region = ROLE_REGIONS.get((joint.role or "").split(".")[0])
        if region is None:
            continue
        above = joint.parent
        seen: set[int] = set()
        while 0 <= above < len(joints) and above not in seen and not joints[above].role:
            seen.add(above)
            above = joints[above].parent
        found = 0 <= above < len(joints) and above not in seen
        start = positions[above] if found else positions[index]
        rows.append([*start, *positions[index], float(REGIONS.index(region))])
    return np.asarray(rows, dtype=np.float64).reshape(-1, 7)


def looks_like_a_figure(bones: np.ndarray) -> bool:
    """Whether the bones say enough about a body to place its skin by."""
    if len(bones) < 4:
        return False
    found = {REGIONS[int(row[6])] for row in bones}
    return "torso" in found and len(found) >= 3


@dataclass(frozen=True)
class BodySource:
    """What a body map is worked out from: the meshes, the bones over them, and how."""

    parts: tuple[Mesh, ...]
    #: Rows of :func:`role_bones`, from every skeleton in the scene together.
    bones: np.ndarray
    source: RegionSource
    whole: int
    #: What the map depends on: two sources with the same key make the same map.
    key: tuple

    @property
    def uses_bones(self) -> bool:
        return self.source is RegionSource.AUTO and looks_like_a_figure(self.bones)


def _segment_distances(points: np.ndarray, bones: np.ndarray) -> np.ndarray:
    """Distance from each point to each bone, ``(points, bones)``."""
    # Single precision: a figure is metres across and a voxel centimetres,
    # and it halves the pass over a scan of a few hundred thousand points.
    points = np.asarray(points, dtype=np.float32)
    a = np.asarray(bones[:, :3], dtype=np.float32)
    b = np.asarray(bones[:, 3:6], dtype=np.float32)
    ab = b - a
    length2 = np.einsum("ij,ij->i", ab, ab)
    out = np.empty((len(points), len(bones)), dtype=np.float32)
    for column in range(len(bones)):
        offset = points - a[column]
        if length2[column] <= 1e-12:
            out[:, column] = np.linalg.norm(offset, axis=1)
            continue
        t = np.clip(offset @ ab[column] / length2[column], 0.0, 1.0)
        nearest = a[column] + t[:, None] * ab[column]
        out[:, column] = np.linalg.norm(points - nearest, axis=1)
    return out


def bone_weights(
    points: np.ndarray, bones: np.ndarray, softness: float | None = None
) -> np.ndarray:
    """Region weights of each point from the bones nearest it, ``(points, regions)``.

    The nearest bone's region takes most of the point; other bones count
    for as much as they are nearly as near, over a distance ``softness``
    -- by default a share of the figure's height -- so that the boundary
    between a thigh and the pelvis is a blend rather than a line.
    """
    points = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    weights = np.zeros((len(points), len(REGIONS)), dtype=np.float32)
    if not len(points) or not len(bones):
        return weights
    if softness is None:
        ends = np.concatenate([bones[:, :3], bones[:, 3:6]])
        height = float(np.max(ends.max(axis=0) - ends.min(axis=0)))
        softness = max(height * 0.03, 1e-9)
    distances = _segment_distances(points, bones)
    nearest = distances.min(axis=1, keepdims=True)
    share = np.exp(-(distances - nearest) / softness)
    share /= share.sum(axis=1, keepdims=True)
    for column in range(len(bones)):
        weights[:, int(bones[column, 6])] += share[:, column].astype(np.float32)
    return weights


def _smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = np.clip((x - edge0) / max(edge1 - edge0, 1e-12), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def band_weights(points: np.ndarray, bottom: float, top: float) -> np.ndarray:
    """Region weights of each point from its height between ``bottom`` and ``top``."""
    points = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    weights = np.zeros((len(points), len(REGIONS)), dtype=np.float32)
    if not len(points):
        return weights
    height = max(float(top - bottom), 1e-12)
    share = (points[:, 1] - bottom) / height
    # How much of a point lies below each edge in turn; a band is the
    # difference between its top edge and the one beneath.
    beneath = np.zeros(len(points))
    for band, edge in zip(BAND_REGIONS, (*BAND_EDGES, None), strict=True):
        below = (
            np.ones(len(points))
            if edge is None
            else 1.0 - _smoothstep(edge - BAND_SOFTNESS, edge + BAND_SOFTNESS, share)
        )
        weights[:, REGIONS.index(band)] += (below - beneath).astype(np.float32)
        beneath = below
    return weights


def region_weights(mesh: Mesh, source: BodySource) -> np.ndarray:
    """The region weights of every vertex of one part of the scene."""
    count = mesh.vertex_count
    weights = np.zeros((count, len(REGIONS)), dtype=np.float32)
    if source.source is RegionSource.OFF or not count:
        return weights
    if source.source is RegionSource.WHOLE:
        weights[:, source.whole] = 1.0
        return weights
    if source.uses_bones:
        return bone_weights(mesh.positions, source.bones)
    low, high = mesh.bounds.minimum[1], mesh.bounds.maximum[1]
    return band_weights(mesh.positions, float(low), float(high))


# ----------------------------------------------------------------------
# The map
# ----------------------------------------------------------------------


@dataclass
class BodyMap:
    """Region weights over the scene, as two RGBA volumes the shader samples by position."""

    #: The corner of the box the volume covers, and its size, in world units.
    origin: np.ndarray
    size: np.ndarray
    #: ``(depth, height, width, 8)``: seven regions, then how much is assigned.
    voxels: np.ndarray

    @property
    def first(self) -> np.ndarray:
        return np.ascontiguousarray(self.voxels[..., :4])

    @property
    def second(self) -> np.ndarray:
        return np.ascontiguousarray(self.voxels[..., 4:])


def _shifted(volume: np.ndarray, axis: int, step: int) -> np.ndarray:
    """``volume`` moved one voxel along ``axis``, with nothing coming in at the edge."""
    out = np.zeros_like(volume)
    src = [slice(None)] * volume.ndim
    dst = [slice(None)] * volume.ndim
    if step > 0:
        src[axis], dst[axis] = slice(0, -1), slice(1, None)
    else:
        src[axis], dst[axis] = slice(1, None), slice(0, -1)
    out[tuple(dst)] = volume[tuple(src)]
    return out


def build_body_map(source: BodySource, resolution: int = 64, passes: int = 6) -> BodyMap | None:
    """Work the region weights out and lay them over the scene as a volume.

    Every vertex and every triangle's centre puts its weights into the
    voxel it falls in; the voxels round the surface that nothing fell in
    are then filled from their neighbours, ``passes`` voxels out, so that
    a fragment between two coarse vertices still reads a value.  Voxels
    further from the skin than that stay unassigned, which the shader
    reads as "no region": the map is only ever sampled on the skin.
    """
    parts = [mesh for mesh in source.parts if mesh is not None and mesh.vertex_count]
    if not parts or source.source is RegionSource.OFF:
        return None
    resolution = max(int(resolution), 4)
    low = np.min([mesh.bounds.minimum for mesh in parts], axis=0)
    high = np.max([mesh.bounds.maximum for mesh in parts], axis=0)
    size = np.maximum(high - low, 1e-9)
    # A margin of a voxel, so that a fragment on the outermost skin has
    # neighbours to blend with rather than the box's edge.
    margin = size / resolution
    origin = low - margin
    size = size + 2.0 * margin
    accumulated = np.zeros((resolution**3, MAP_CHANNELS), dtype=np.float32)
    counts = np.zeros(resolution**3, dtype=np.float32)
    for mesh in parts:
        weights = region_weights(mesh, source)
        points = np.asarray(mesh.positions, dtype=np.float64)
        indices = np.asarray(mesh.indices, dtype=np.int64).reshape(-1, 3)
        if len(indices):
            points = np.concatenate([points, points[indices].mean(axis=1)])
            weights = np.concatenate([weights, weights[indices].mean(axis=1)])
        assigned = weights.sum(axis=1, keepdims=True)
        rows = np.concatenate([weights, assigned], axis=1)
        cell = np.floor((points - origin) / size * resolution).astype(np.int64)
        cell = np.clip(cell, 0, resolution - 1)
        # Texture x is the last array axis: (depth, height, width) is (z, y, x).
        flat = (cell[:, 2] * resolution + cell[:, 1]) * resolution + cell[:, 0]
        for channel in range(MAP_CHANNELS):
            accumulated[:, channel] += np.bincount(
                flat, weights=rows[:, channel], minlength=resolution**3
            ).astype(np.float32)
        counts += np.bincount(flat, minlength=resolution**3).astype(np.float32)
    filled = counts > 0
    accumulated[filled] /= counts[filled, None]
    volume = accumulated.reshape(resolution, resolution, resolution, MAP_CHANNELS)
    filled = filled.reshape(resolution, resolution, resolution)
    for _ in range(max(int(passes), 0)):
        total = np.zeros_like(volume)
        neighbours = np.zeros(filled.shape, dtype=np.float32)
        known = volume * filled[..., None]
        mask = filled.astype(np.float32)
        for axis in range(3):
            for step in (-1, 1):
                total += _shifted(known, axis, step)
                neighbours += _shifted(mask, axis, step)
        fresh = ~filled & (neighbours > 0)
        if not fresh.any():
            break
        volume[fresh] = total[fresh] / neighbours[fresh, None]
        filled |= fresh
    return BodyMap(origin=origin, size=size, voxels=np.ascontiguousarray(volume, dtype=np.float32))
