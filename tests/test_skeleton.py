"""Skeletons: the joint tree, posing, skinning, and where skeletons come from."""

from __future__ import annotations

import json
import struct

import numpy as np
import pytest

from refview.core.armature import Armature, ArmatureNode, Bone
from refview.core.linalg import euler_to_quat, quat_from_axis_angle, quat_to_euler
from refview.core.mesh import Mesh
from refview.core.mesh_io import load_mesh
from refview.core.rigging import (
    HUMANOID_ROLES,
    armature_from_skeleton,
    armature_root,
    build_humanoid_skeleton,
    detail_joints,
    humanoid_roles,
    looks_humanoid,
    read_role,
    simplified,
    skeleton_from_armature,
    with_roles,
)
from refview.core.session import Session
from refview.core.skeleton import (
    Joint,
    Rig,
    Skeleton,
    Skin,
    make_joint,
    skinned_mesh,
)

# ----------------------------------------------------------------------
# Fixtures
# ----------------------------------------------------------------------


def _arm() -> Skeleton:
    """Three joints in a line along +X: shoulder, elbow, wrist."""
    return Skeleton(
        name="arm",
        joints=[
            make_joint("shoulder", -1, (0.0, 0.0, 0.0)),
            make_joint("elbow", 0, (1.0, 0.0, 0.0)),
            make_joint("wrist", 1, (1.0, 0.0, 0.0)),
        ],
    )


def _strip_mesh(count: int = 5) -> tuple[np.ndarray, np.ndarray]:
    """A ribbon of quads along +X from 0 to 2, two vertices per station."""
    xs = np.linspace(0.0, 2.0, count)
    positions = np.array([[x, y, 0.0] for x in xs for y in (0.0, 0.2)], dtype=np.float32)
    indices = []
    for station in range(count - 1):
        a, b = 2 * station, 2 * station + 1
        c, d = a + 2, b + 2
        indices += [[a, b, c], [b, d, c]]
    return positions, np.array(indices, dtype=np.uint32)


def _rig_for_strip(positions: np.ndarray) -> Rig:
    """Two joints: one at x=0 holding x<1, one at x=1 holding x>=1."""
    joint = (positions[:, 0] >= 1.0).astype(np.int32)
    joints = np.zeros((len(positions), 4), dtype=np.int32)
    joints[:, 0] = joint
    weights = np.zeros((len(positions), 4), dtype=np.float32)
    weights[:, 0] = 1.0
    rest_local = np.tile(np.eye(4), (2, 1, 1))
    rest_local[1, 0, 3] = 1.0
    inverse_bind = np.tile(np.eye(4), (2, 1, 1))
    inverse_bind[1, 0, 3] = -1.0
    normals = np.tile([0.0, 0.0, 1.0], (len(positions), 1)).astype(np.float32)
    return Rig(
        ["root", "tip"],
        [-1, 0],
        rest_local,
        Skin(joints, weights, inverse_bind, positions, normals),
    )


def _skinned_strip() -> Mesh:
    positions, indices = _strip_mesh()
    normals = np.tile([0.0, 0.0, 1.0], (len(positions), 1)).astype(np.float32)
    return Mesh(positions, normals, indices, "strip", rig=_rig_for_strip(positions))


# ----------------------------------------------------------------------
# The tree
# ----------------------------------------------------------------------


def test_world_positions_accumulate_down_the_chain():
    arm = _arm()
    assert np.allclose(arm.positions(), [[0, 0, 0], [1, 0, 0], [2, 0, 0]])
    assert arm.bones() == [(0, 1), (1, 2)]
    assert arm.roots() == [0]
    assert arm.depth(2) == 2
    assert arm.descendants(0) == [1, 2]
    assert arm.is_ancestor(0, 2) and not arm.is_ancestor(2, 0)


def test_order_puts_parents_first_whatever_the_list_order():
    tangled = Skeleton(
        joints=[
            make_joint("wrist", 1, (1.0, 0.0, 0.0)),
            make_joint("elbow", 2, (1.0, 0.0, 0.0)),
            make_joint("shoulder", -1, (0.0, 0.0, 0.0)),
        ]
    )
    assert tangled.order() == [2, 1, 0]
    assert np.allclose(tangled.positions()[0], [2, 0, 0])


def test_turning_the_shoulder_carries_the_arm():
    arm = _arm()
    arm.joints[0].rotation = tuple(quat_from_axis_angle([0, 0, 1], np.pi / 2))
    at = arm.positions()
    assert np.allclose(at[1], [0, 1, 0], atol=1e-9)
    assert np.allclose(at[2], [0, 2, 0], atol=1e-9)
    assert arm.posed
    assert not arm.joints[1].posed


def test_the_rest_is_untouched_by_the_pose():
    arm = _arm()
    arm.joints[0].rotation = tuple(quat_from_axis_angle([0, 0, 1], np.pi / 2))
    assert np.allclose(arm.positions(rest=True), [[0, 0, 0], [1, 0, 0], [2, 0, 0]])
    arm.joints = arm.with_pose_reset()
    assert not arm.posed


def test_removing_a_joint_keeps_its_children_in_place():
    arm = _arm()
    joints = arm.without_joint(1)
    assert [joint.name for joint in joints] == ["shoulder", "wrist"]
    assert joints[1].parent == 0
    assert np.allclose(Skeleton(joints=joints).positions(), [[0, 0, 0], [2, 0, 0]])


def test_removing_a_branch_takes_everything_below():
    arm = _arm()
    joints = arm.without_branch(1)
    assert [joint.name for joint in joints] == ["shoulder"]


def test_reparenting_keeps_the_scene_position_and_refuses_a_loop():
    arm = _arm()
    joints = arm.with_parent(2, 0)
    assert joints[2].parent == 0
    assert np.allclose(Skeleton(joints=joints).positions()[2], [2, 0, 0])
    unchanged = arm.with_parent(0, 2)  # the shoulder cannot hang from its own wrist
    assert unchanged[0].parent == -1


def test_moving_a_rest_position_leaves_the_children_where_they_were():
    arm = _arm()
    joints = arm.with_rest_at(1, (1.0, 0.5, 0.0))
    at = Skeleton(joints=joints).positions()
    assert np.allclose(at[1], [1, 0.5, 0])
    assert np.allclose(at[2], [2, 0, 0])


def test_a_rigid_transform_carries_the_whole_skeleton():
    arm = _arm()
    turn = np.eye(4)
    turn[:3, 3] = [0, 0, 5]
    arm.joints = arm.transformed(turn)
    assert np.allclose(arm.positions()[:, 2], 5.0)


def test_euler_sliders_round_trip():
    q = euler_to_quat(20.0, -35.0, 50.0)
    assert np.allclose(quat_to_euler(q), (20.0, -35.0, 50.0))


# ----------------------------------------------------------------------
# Skinning
# ----------------------------------------------------------------------


def test_an_unposed_skeleton_leaves_the_mesh_alone():
    mesh = _skinned_strip()
    skeleton = mesh.rig.to_skeleton("strip")
    assert skeleton.bound
    assert skinned_mesh(mesh, skeleton) is mesh or np.allclose(
        skinned_mesh(mesh, skeleton).positions, mesh.positions
    )


def test_bending_the_tip_joint_folds_the_far_half():
    mesh = _skinned_strip()
    skeleton = mesh.rig.to_skeleton("strip")
    skeleton.joints[1].rotation = tuple(quat_from_axis_angle([0, 0, 1], np.pi / 2))
    posed = skinned_mesh(mesh, skeleton)
    near = mesh.positions[:, 0] < 1.0
    assert np.allclose(posed.positions[near], mesh.positions[near])
    # A vertex at (2, 0) is one unit past the tip joint, so it swings up to (1, 1).
    far = np.flatnonzero((mesh.positions[:, 0] == 2.0) & (mesh.positions[:, 1] == 0.0))
    assert np.allclose(posed.positions[far], [[1.0, 1.0, 0.0]], atol=1e-6)
    assert posed.rig is mesh.rig
    assert np.array_equal(posed.indices, mesh.indices)


def test_a_renamed_joint_keeps_its_weights_and_a_deleted_one_hands_them_up():
    mesh = _skinned_strip()
    skeleton = mesh.rig.to_skeleton("strip")
    skeleton.joints[1].name = "Elbow"
    assert list(mesh.rig.binding(skeleton)[0]) == [0, 1]
    skeleton.joints = skeleton.without_joint(1)
    bound, through = mesh.rig.binding(skeleton)
    assert list(bound) == [0, 0] and list(through) == [0, 0]
    skeleton.joints[0].rotation = tuple(quat_from_axis_angle([0, 0, 1], np.pi / 2))
    posed = skinned_mesh(mesh, skeleton)
    far = np.flatnonzero((mesh.positions[:, 0] == 2.0) & (mesh.positions[:, 1] == 0.0))
    assert np.allclose(posed.positions[far], [[0.0, 2.0, 0.0]], atol=1e-6)


def test_a_turned_mesh_carries_its_rig_with_it():
    mesh = _skinned_strip()
    turn = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]], dtype=np.float64)  # +X -> +Y
    turned = mesh.transformed(turn).recentered()
    skeleton = turned.rig.to_skeleton("strip")
    assert np.allclose(skeleton.positions()[1] - skeleton.positions()[0], [0, 1, 0])
    skeleton.joints[1].rotation = tuple(quat_from_axis_angle([0, 0, 1], np.pi / 2))
    posed = skinned_mesh(turned, skeleton)
    # The far end (was x=2, now y=2 before centring) swings from +Y to -X.
    tip = skeleton.positions()[1]
    far = np.argmax(turned.positions[:, 1])
    assert np.allclose(posed.positions[far], tip + [-1.0, 0.0, 0.0], atol=1e-5)


# ----------------------------------------------------------------------
# Out of a glTF
# ----------------------------------------------------------------------


def _write_skinned_glb(path, bent: bool = False):
    """The strip as a GLB with a two-joint skin, optionally saved mid-bend."""
    positions, indices = _strip_mesh()
    joints = np.zeros((len(positions), 4), dtype=np.uint8)
    joints[:, 0] = (positions[:, 0] >= 1.0).astype(np.uint8)
    weights = np.zeros((len(positions), 4), dtype=np.float32)
    weights[:, 0] = 1.0
    inverse_bind = np.tile(np.eye(4, dtype=np.float32), (2, 1, 1))
    inverse_bind[1, 0, 3] = -1.0
    inverse_bind = np.ascontiguousarray(inverse_bind.transpose(0, 2, 1))  # column-major
    flat = indices.astype(np.uint16).reshape(-1)

    blobs = [positions.tobytes(), flat.tobytes(), joints.tobytes(), weights.tobytes(),
             inverse_bind.tobytes()]
    views, accessors, blob, offset = [], [], b"", 0
    for data in blobs:
        padded = data + b"\0" * (-len(data) % 4)
        views.append({"buffer": 0, "byteOffset": offset, "byteLength": len(data)})
        blob += padded
        offset += len(padded)
    accessors = [
        {"bufferView": 0, "componentType": 5126, "count": len(positions), "type": "VEC3"},
        {"bufferView": 1, "componentType": 5123, "count": len(flat), "type": "SCALAR"},
        {"bufferView": 2, "componentType": 5121, "count": len(positions), "type": "VEC4"},
        {"bufferView": 3, "componentType": 5126, "count": len(positions), "type": "VEC4"},
        {"bufferView": 4, "componentType": 5126, "count": 2, "type": "MAT4"},
    ]
    tip = {"name": "Tip", "translation": [1.0, 0.0, 0.0]}
    if bent:
        half = np.sin(np.pi / 4)
        tip["rotation"] = [0.0, 0.0, float(half), float(np.cos(np.pi / 4))]
    document = {
        "asset": {"version": "2.0"},
        "scene": 0,
        "scenes": [{"nodes": [0, 1]}],
        "nodes": [
            {"name": "Root", "children": [2]},
            {"name": "Body", "mesh": 0, "skin": 0, "translation": [50.0, 0.0, 0.0]},
            tip,
        ],
        "skins": [{"joints": [0, 2], "inverseBindMatrices": 4}],
        "meshes": [
            {
                "primitives": [
                    {
                        "attributes": {"POSITION": 0, "JOINTS_0": 2, "WEIGHTS_0": 3},
                        "indices": 1,
                    }
                ]
            }
        ],
        "accessors": accessors,
        "bufferViews": views,
        "buffers": [{"byteLength": len(blob)}],
    }
    json_chunk = json.dumps(document).encode("utf-8")
    json_chunk += b" " * (-len(json_chunk) % 4)
    body = (
        struct.pack("<II", len(json_chunk), 0x4E4F534A)
        + json_chunk
        + struct.pack("<II", len(blob), 0x004E4942)
        + blob
    )
    path.write_bytes(b"glTF" + struct.pack("<II", 2, 12 + len(body)) + body)
    return path


def test_a_skinned_glb_comes_with_its_rig(tmp_path):
    mesh = load_mesh(_write_skinned_glb(tmp_path / "strip.glb"))
    assert mesh.rig is not None
    assert mesh.rig.names == ["Root", "Tip"]
    assert mesh.rig.parents == [-1, 0]
    # The skinned mesh node's own translation is ignored, as the spec says.
    assert np.allclose(mesh.bounds.minimum[0], 0.0)
    assert np.allclose(mesh.rig.rest_world()[1][:3, 3], [1, 0, 0])
    assert mesh.rig.skin.weights[:, 0].min() == 1.0


def test_a_glb_saved_mid_pose_loads_posed_and_unbends(tmp_path):
    mesh = load_mesh(_write_skinned_glb(tmp_path / "bent.glb", bent=True))
    # The far end was bent a right angle up at load: x=2,y=0 stands at (1, 1).
    assert np.isclose(mesh.positions[:, 1].max(), 1.0, atol=1e-5)
    skeleton = mesh.rig.to_skeleton("bent")
    skeleton.joints[1].rotation = tuple(quat_from_axis_angle([0, 0, 1], -np.pi / 2))
    straight = skinned_mesh(mesh, skeleton)
    assert np.isclose(straight.positions[:, 0].max(), 2.0, atol=1e-5)


# ----------------------------------------------------------------------
# Where skeletons come from
# ----------------------------------------------------------------------


def test_the_humanoid_preset_stands_on_its_feet_and_is_a_tree():
    figure = build_humanoid_skeleton(180.0, feet=(0.0, -90.0, 0.0))
    at = figure.positions()
    assert len(figure.joints) == len(HUMANOID_ROLES)
    assert np.isclose(at[:, 1].max(), 90.0)
    assert np.isclose(at[:, 1].min(), -90.0 + 1.8)
    assert figure.roots() == [0]
    assert figure.joint_for_role("knee.L") is not None
    left = at[figure.joint_for_role("hand.L")]
    right = at[figure.joint_for_role("hand.R")]
    assert np.isclose(left[0], -right[0]) and np.isclose(left[1], right[1])


def test_an_armature_grows_into_a_skeleton_and_back():
    figure = build_humanoid_skeleton(1.8)
    figure.joints[figure.joint_for_role("shoulder.L")].rotation = tuple(
        quat_from_axis_angle([0, 0, 1], -0.5)
    )
    armature = armature_from_skeleton(figure)
    assert len(armature.nodes) == len(figure.joints)
    assert len(armature.bones) == len(figure.bones())
    # The nodes stand where the joints are posed, and keep their roles.
    assert np.allclose(armature.node_array, figure.positions())
    assert armature.node_for_role("knee.R") is not None

    grown, dropped = skeleton_from_armature(armature)
    assert dropped == 0
    assert grown.joints[0].role == "pelvis"  # the pelvis is the root
    by_name = {joint.name: at for joint, at in zip(grown.joints, grown.positions(), strict=True)}
    for joint, at in zip(figure.joints, figure.positions(), strict=True):
        assert np.allclose(by_name[joint.name], at)


def test_a_loop_in_a_freehand_armature_is_dropped_and_counted():
    armature = Armature(
        nodes=[ArmatureNode(name=f"n{i}", at=(float(i), 0.0, 0.0)) for i in range(4)],
        bones=[Bone(0, 1), Bone(1, 2), Bone(2, 3), Bone(3, 0), Bone(0, 2)],
    )
    assert armature_root(armature) == 0  # the best-connected node
    grown, dropped = skeleton_from_armature(armature, root=1)
    assert grown.roots() == [0] and grown.joints[0].name == "n1"
    assert dropped == 2
    assert len(grown.bones()) == 3


def test_a_disconnected_node_becomes_a_root_of_its_own():
    armature = Armature(
        nodes=[ArmatureNode(name="a"), ArmatureNode(name="b", at=(1.0, 0.0, 0.0)),
               ArmatureNode(name="loose", at=(5.0, 0.0, 0.0))],
        bones=[Bone(0, 1)],
    )
    grown, _ = skeleton_from_armature(armature)
    assert len(grown.roots()) == 2


@pytest.mark.parametrize(
    ("name", "role"),
    [
        ("mixamorig:Hips", "pelvis"),
        ("mixamorig:LeftUpLeg", "hip.L"),
        ("mixamorig:RightForeArm", "elbow.R"),
        ("mixamorig:LeftHandMiddle1", "hand.L"),
        ("mixamorig:LeftHandThumb1", ""),
        ("Bip01 L Thigh", "hip.L"),
        ("Bip01 R Clavicle", "clavicle.R"),
        ("Bip01 Pelvis", "pelvis"),
        ("upperarm_l", "shoulder.L"),
        ("ball_r", "foot.R"),
        ("shin.L", "knee.L"),
        ("CC_Base_R_Thigh", "hip.R"),
        ("Bone.042", ""),
        ("hand", ""),  # a hand with no side is not a wrist anyone can place
    ],
)
def test_roles_are_read_off_the_names_rigs_use(name, role):
    assert read_role(name) == role


def test_a_mixamo_rig_is_recognised_as_a_humanoid():
    names = [
        ("mixamorig:Hips", -1), ("mixamorig:Spine", 0), ("mixamorig:Spine1", 1),
        ("mixamorig:Spine2", 2), ("mixamorig:Neck", 3), ("mixamorig:Head", 4),
        ("mixamorig:HeadTop_End", 5), ("mixamorig:LeftShoulder", 3), ("mixamorig:LeftArm", 7),
        ("mixamorig:LeftForeArm", 8), ("mixamorig:LeftHand", 9), ("mixamorig:RightUpLeg", 0),
        ("mixamorig:RightLeg", 11), ("mixamorig:RightFoot", 12), ("mixamorig:RightToeBase", 13),
    ]
    skeleton = Skeleton(joints=[Joint(name=name, parent=parent) for name, parent in names])
    roles = humanoid_roles(skeleton)
    assert looks_humanoid(roles)
    assert roles[0] == "pelvis" and roles[1] == "spine"
    assert roles[3] == "chest"  # the last of the spine chain
    assert roles[6] == "head_top" and roles[14] == "foot.R"
    assert 2 not in roles  # the middle spine fills no slot
    joints = with_roles(skeleton, roles)
    assert joints[7].role == "clavicle.L"
    assert not looks_humanoid(humanoid_roles(_arm()))


# ----------------------------------------------------------------------
# Sessions
# ----------------------------------------------------------------------


def test_a_posed_skeleton_survives_a_session_round_trip():
    figure = build_humanoid_skeleton(1.8)
    figure.joints[3].rotation = tuple(quat_from_axis_angle([1, 0, 0], 0.3))
    figure.joints[0].translation = (0.1, 0.0, 0.0)
    figure.joints[5].source = "Head"
    session = Session(skeletons=[figure])
    back = Session.from_dict(json.loads(json.dumps(session.to_dict())))
    assert back.version == 11
    assert len(back.skeletons) == 1
    restored = back.skeletons[0]
    assert restored.joints[5].source == "Head" and restored.bound
    assert np.allclose(restored.positions(), figure.positions())
    assert isinstance(restored.joints[0].rest, tuple) and len(restored.joints[0].rest) == 16


def test_an_old_session_has_no_skeletons():
    old = Session.from_dict({"version": 7})
    assert old.skeletons == []
    assert old.skeleton_settings.deform


# ----------------------------------------------------------------------
# Simplifying
# ----------------------------------------------------------------------


def _game_rig() -> Skeleton:
    names = [
        ("Root", -1), ("Hips", 0), ("Spine", 1), ("Neck", 2), ("Head", 3), ("HeadTop_End", 4),
        ("Jaw", 4), ("L_Eye", 4), ("LeftShoulder", 2), ("LeftArm", 8), ("LeftArmTwist", 9),
        ("LeftForeArm", 9), ("LeftHand", 11), ("LeftHandIndex1", 12), ("LeftHandIndex2", 13),
        ("LeftHandThumb1", 12), ("L_Breast", 2), ("LeftUpLeg", 1), ("LeftLeg", 17),
        ("LeftFoot", 18), ("LeftToeBase", 19), ("LeftToe_End", 20), ("L_BigToe1", 20),
        ("Shadow_Catcher", -1),
    ]
    return Skeleton(joints=[make_joint(name, parent, (0.0, 1.0, 0.0)) for name, parent in names])


def test_simplifying_takes_the_detail_out_by_name_and_keeps_the_figure():
    rig = _game_rig()
    kinds = detail_joints(rig)
    names = {rig.joints[index].name: kind for index, kind in kinds.items()}
    assert names["LeftHandIndex1"] == "fingers" and names["LeftHandThumb1"] == "fingers"
    assert names["Jaw"] == "face" and names["L_Eye"] == "face"
    assert names["L_Breast"] == "breasts"
    assert names["LeftArmTwist"] == "helpers" and names["Shadow_Catcher"] == "helpers"
    assert names["L_BigToe1"] == "toes" and names["LeftToe_End"] == "toes"
    assert "HeadTop_End" in names  # an unmapped end nub is detail
    assert "LeftToeBase" not in names and "LeftHand" not in names
    joints, counts = simplified(rig)
    assert sum(counts.values()) == len(kinds)
    slim = Skeleton(joints=joints)
    assert [j.name for j in joints][:5] == ["Root", "Hips", "Spine", "Neck", "Head"]
    # The forearm hangs from the arm now that the twist between them is gone.
    forearm = next(i for i, j in enumerate(joints) if j.name == "LeftForeArm")
    assert joints[forearm].parent == next(i for i, j in enumerate(joints) if j.name == "LeftArm")
    by_name = {j.name: at for j, at in zip(rig.joints, rig.positions(), strict=True)}
    for joint, at in zip(slim.joints, slim.positions(), strict=True):
        assert np.allclose(by_name[joint.name], at)


def test_a_role_keeps_a_joint_and_its_ancestors_through_a_simplify():
    rig = _game_rig()
    rig.joints = with_roles(rig, humanoid_roles(rig))
    joints, _ = simplified(rig)
    names = [j.name for j in joints]
    assert "HeadTop_End" in names  # the crown, by its role
    assert "LeftToeBase" in names and "LeftHandIndex1" not in names


def test_simplifying_a_skinned_rig_folds_the_weights_onto_what_stayed():
    mesh = _skinned_strip()
    rig = mesh.rig
    skeleton = Skeleton(
        joints=[
            Joint(name="root", source="root"),
            make_joint("tip_twist", 0, (1.0, 0.0, 0.0), source="tip"),
        ]
    )
    joints, counts = simplified(skeleton)
    assert counts == {"helpers": 1} and len(joints) == 1
    slim = Skeleton(joints=joints)
    bound, through = rig.binding(slim)
    assert list(bound) == [0, 0]
    slim.joints[0].rotation = tuple(quat_from_axis_angle([0, 0, 1], np.pi / 2))
    posed = skinned_mesh(mesh, slim)
    far = np.flatnonzero((mesh.positions[:, 0] == 2.0) & (mesh.positions[:, 1] == 0.0))
    assert np.allclose(posed.positions[far], [[0.0, 2.0, 0.0]], atol=1e-6)
