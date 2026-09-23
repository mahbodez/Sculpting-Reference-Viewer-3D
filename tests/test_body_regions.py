"""Where on the body the skin is: bones, height bands, the map, and the settings."""

from __future__ import annotations

import json
from dataclasses import replace

import numpy as np
import pytest

from refview.core.body_regions import (
    BAND_EDGES,
    REGIONS,
    BodyRegionSettings,
    BodySource,
    RegionProfile,
    RegionSource,
    band_weights,
    bone_weights,
    build_body_map,
    looks_like_a_figure,
    region_weights,
    role_bones,
)
from refview.core.mesh import Mesh, compute_vertex_normals
from refview.core.rigging import build_humanoid_skeleton
from refview.core.session import Session
from refview.core.settings import ShadingMode
from refview.core.skeleton import Skeleton, make_joint
from refview.core.skin import SkinSettings
from refview.ui.state import ViewerState


def _figure_bones() -> np.ndarray:
    return role_bones(build_humanoid_skeleton(1.8))


def _region(weights: np.ndarray) -> str:
    return REGIONS[int(np.argmax(weights))]


def test_the_humanoid_preset_gives_a_bone_for_every_role_and_looks_like_a_figure():
    bones = _figure_bones()
    assert bones.shape[1] == 7 and len(bones) >= 20
    assert looks_like_a_figure(bones)
    found = {REGIONS[int(row[6])] for row in bones}
    assert found == set(REGIONS)
    # A bone runs from a joint to its parent: the thigh is a bone of some length.
    lengths = np.linalg.norm(bones[:, 3:6] - bones[:, :3], axis=1)
    assert lengths.max() > 0.3


def test_unnamed_helper_joints_are_stepped_over_and_a_lone_pelvis_is_a_point():
    joints = [  # each placed in its parent's frame
        make_joint("hips", -1, (0.0, 1.0, 0.0), role="pelvis"),
        make_joint("helper", 0, (0.0, 0.1, 0.0)),  # no role
        make_joint("spine", 1, (0.0, 0.2, 0.0), role="spine"),
    ]
    bones = role_bones(Skeleton(name="s", joints=joints))
    assert len(bones) == 2
    pelvis = bones[0]
    assert np.allclose(pelvis[:3], pelvis[3:6])  # a root is a bone of no length
    spine = bones[1]
    assert np.allclose(spine[:3], [0.0, 1.0, 0.0]) and np.allclose(spine[3:6], [0.0, 1.3, 0.0])
    assert not looks_like_a_figure(bones)
    assert len(role_bones(Skeleton(name="bare", joints=[make_joint("a", -1, (0, 0, 0))]))) == 0


def test_points_go_to_the_region_of_the_nearest_bone_and_blend_between():
    bones = _figure_bones()
    crown = bone_weights(np.array([[0.0, 1.78, 0.0]]), bones)[0]
    assert _region(crown) == "head" and crown[REGIONS.index("head")] > 0.8
    assert _region(bone_weights(np.array([[0.0, 0.04, 0.1]]), bones)[0]) == "feet"
    assert _region(bone_weights(np.array([[0.25, 1.0, 0.0]]), bones)[0]) == "arms"
    assert _region(bone_weights(np.array([[0.28, 0.72, 0.0]]), bones)[0]) == "hands"
    assert _region(bone_weights(np.array([[0.12, 0.6, 0.0]]), bones)[0]) == "legs"
    assert _region(bone_weights(np.array([[0.0, 1.2, 0.05]]), bones)[0]) == "torso"
    # Weights are a partition of unity, so a boundary is a blend, not a line.
    ankle = bone_weights(np.array([[0.135, 0.09, 0.0]]), bones)[0]
    assert ankle.sum() == pytest.approx(1.0, abs=1e-5)
    assert ankle[REGIONS.index("legs")] > 0.05 and ankle[REGIONS.index("feet")] > 0.05


def test_height_bands_follow_the_canon_and_are_soft_at_the_edges():
    points = np.array([[0, 0.02, 0], [0, 0.3, 0], [0, 0.7, 0], [0, 0.84, 0], [0, 0.95, 0]])
    weights = band_weights(points, 0.0, 1.0)
    assert [_region(w) for w in weights] == ["feet", "legs", "torso", "neck", "head"]
    assert np.allclose(weights.sum(axis=1), 1.0)
    edge = band_weights(np.array([[0.0, BAND_EDGES[1], 0.0]]), 0.0, 1.0)[0]
    assert edge[REGIONS.index("legs")] == pytest.approx(0.5, abs=0.05)
    assert edge[REGIONS.index("torso")] == pytest.approx(0.5, abs=0.05)
    # Scaled with the figure: the same shares of a figure twice as tall.
    tall = band_weights(points * 2.0, 0.0, 2.0)
    assert np.allclose(tall, weights)


def _column(height: float = 1.8, count: int = 40) -> Mesh:
    """A thin column standing from the ground to ``height``."""
    ys = np.linspace(0.0, height, count)
    ring = np.array([[0.05, 0.0], [0.0, 0.05], [-0.05, 0.0], [0.0, -0.05]])
    positions = np.array([[x, y, z] for y in ys for x, z in ring], dtype=np.float32)
    faces = []
    for row in range(count - 1):
        for k in range(4):
            a, b = row * 4 + k, row * 4 + (k + 1) % 4
            c, d = a + 4, b + 4
            faces += [[a, b, c], [b, d, c]]
    indices = np.asarray(faces, dtype=np.uint32)
    return Mesh(positions, compute_vertex_normals(positions, indices), indices, name="column")


def test_region_weights_come_from_bones_when_they_describe_a_figure_else_bands():
    mesh = _column()
    key = ("test",)
    with_bones = BodySource((mesh,), _figure_bones(), RegionSource.AUTO, 0, key)
    assert with_bones.uses_bones
    weights = region_weights(mesh, with_bones)
    assert _region(weights[-1]) == "head" and _region(weights[0]) == "feet"
    bare = BodySource((mesh,), np.zeros((0, 7)), RegionSource.AUTO, 0, key)
    assert not bare.uses_bones
    banded = region_weights(mesh, bare)
    assert _region(banded[-1]) == "head" and _region(banded[len(banded) // 2]) == "torso"
    forced = BodySource((mesh,), _figure_bones(), RegionSource.BANDS, 0, key)
    assert np.allclose(region_weights(mesh, forced), banded)
    whole = BodySource((mesh,), _figure_bones(), RegionSource.WHOLE, REGIONS.index("hands"), key)
    hands = region_weights(mesh, whole)
    assert np.all(hands[:, REGIONS.index("hands")] == 1.0)
    off = BodySource((mesh,), _figure_bones(), RegionSource.OFF, 0, key)
    assert not region_weights(mesh, off).any()


def test_the_map_covers_the_skin_and_a_little_round_it_and_reads_back_the_regions():
    mesh = _column()
    source = BodySource((mesh,), np.zeros((0, 7)), RegionSource.BANDS, 0, ("k",))
    body = build_body_map(source, resolution=32, passes=3)
    assert body is not None
    assert body.voxels.shape == (32, 32, 32, 8) and body.voxels.dtype == np.float32
    assert np.all(body.origin <= mesh.bounds.minimum) and np.all(
        body.origin + body.size >= mesh.bounds.maximum
    )
    assigned = body.voxels[..., 7]
    filled = assigned > 0.5
    # The skin's own voxels are assigned, a few voxels out from it are too,
    # and the corners of the box, far from any skin, are not.
    assert 0.02 < filled.mean() < 0.9
    assert assigned[0, 0, 0] == 0.0 and assigned[-1, -1, -1] == 0.0

    def read(point):
        cell = np.clip(((point - body.origin) / body.size * 32).astype(int), 0, 31)
        return body.voxels[cell[2], cell[1], cell[0]]

    # Read on the skin, which is the only place the shader reads it: the
    # inside of a solid is nobody's business and stays unassigned.
    assert _region(read(np.array([0.05, 1.75, 0.0]))[:7]) == "head"
    assert _region(read(np.array([0.05, 1.0, 0.0]))[:7]) == "torso"
    assert _region(read(np.array([0.05, 0.3, 0.0]))[:7]) == "legs"
    assert read(np.array([0.05, 1.0, 0.0]))[7] == pytest.approx(1.0, abs=1e-5)
    assert body.first.shape[-1] == 4 and body.second.shape[-1] == 4
    assert build_body_map(replace(source, source=RegionSource.OFF)) is None
    assert build_body_map(replace(source, parts=())) is None


def test_region_settings_round_trip_bound_and_default_where_a_session_has_none():
    settings = BodyRegionSettings(source=RegionSource.WHOLE, whole="arms")
    settings.arms.acne = 2.5
    settings.arms.veins = 2.25
    session = Session()
    session.render.shading_mode = ShadingMode.HUMAN_SKIN
    session.render.skin = replace(SkinSettings(acne=0.4, nevi=0.2), regions=settings)
    back = Session.from_dict(json.loads(json.dumps(session.to_dict()))).render.skin
    assert back.regions.source is RegionSource.WHOLE and back.regions.whole == "arms"
    assert back.regions.arms.acne == 2.5 and back.acne == 0.4 and back.nevi == 0.2
    assert back.regions.multipliers("acne")[REGIONS.index("arms")] == 2.5
    assert back.regions.arms.veins == 2.25
    assert back.regions.multipliers("veins")[REGIONS.index("arms")] == 2.25

    old_profile_data = session.to_dict()
    del old_profile_data["render"]["skin"]["regions"]["arms"]["veins"]
    old_profile = Session.from_dict(old_profile_data).render.skin.regions.arms
    # A saved profile from before vein regions keeps the old global appearance.
    assert old_profile.veins == 1.0

    data = session.to_dict()
    for name in ("acne", "nevi", "freckles", "blemishes", "regions"):
        del data["render"]["skin"][name]
    old = Session.from_dict(data).render.skin
    assert old.acne == 0.0 and old.regions == BodyRegionSettings()
    # The defaults know a face from a foot.
    assert old.regions.head.acne > old.regions.feet.acne
    assert old.regions.feet.blood > old.regions.arms.blood
    assert old.regions.hands.veins > old.regions.torso.veins

    wild = SkinSettings(acne=7.0, regions=BodyRegionSettings(whole="nowhere"))
    wild.regions.head = RegionProfile(acne=float("nan"), oil=-4.0, nevi=99.0,
                                      veins=float("nan"))
    tame = wild.bounded()
    assert tame.acne == 1.0 and tame.regions.whole == "head"
    assert tame.regions.head.acne == 1.0 and tame.regions.head.oil == 0.0
    assert tame.regions.head.nevi == 3.0
    assert tame.regions.head.veins == 1.0


def test_the_state_hands_the_renderer_a_source_whose_key_follows_the_scene():
    state = ViewerState()
    state.source_mesh = _column()
    state.render.shading_mode = ShadingMode.HUMAN_SKIN
    first = state.body_source()
    assert first is not None and len(first.parts) == 1 and not first.uses_bones
    assert state.body_source().key == first.key
    figure = build_humanoid_skeleton(1.8)
    state.skeletons.add(figure)
    with_bones = state.body_source()
    assert with_bones.uses_bones and with_bones.key != first.key
    figure.joints[0].translation = (0.2, 0.0, 0.0)
    assert state.body_source().key != with_bones.key
    state.render.skin.regions.source = RegionSource.OFF
    assert state.body_source() is None
