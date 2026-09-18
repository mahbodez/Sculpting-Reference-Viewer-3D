"""Skinning a model to a skeleton it did not come with, and keeping the skin."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
import pytest

from refview.core.autoskin import (
    AutoSkinError,
    AutoSkinSettings,
    SkinMethod,
    auto_skin,
    bone_segments,
    unique_names,
)
from refview.core.linalg import quat_from_axis_angle
from refview.core.mesh import Mesh
from refview.core.progress import CancelledError, Progress
from refview.core.rig_file import RigFileError, load_rig, save_rig
from refview.core.skeleton import Skeleton, make_joint, skinned_mesh


def _tube(length: float = 4.0, radius: float = 0.3, rings: int = 41, around: int = 12) -> Mesh:
    """A closed tube along +X, the simplest limb there is."""
    xs = np.linspace(0.0, length, rings)
    angles = np.linspace(0.0, 2 * np.pi, around, endpoint=False)
    positions = np.array(
        [[x, radius * np.cos(a), radius * np.sin(a)] for x in xs for a in angles],
        dtype=np.float32,
    )
    faces = []
    for ring in range(rings - 1):
        for k in range(around):
            a = ring * around + k
            b = ring * around + (k + 1) % around
            c = a + around
            d = b + around
            faces.append([a, b, d])
            faces.append([a, d, c])
    # Caps: a fan to the centre of each end.
    front = len(positions)
    positions = np.concatenate(
        [positions, np.array([[0.0, 0.0, 0.0], [length, 0.0, 0.0]], dtype=np.float32)]
    )
    for k in range(around):
        faces.append([front, (k + 1) % around, k])
        base = (rings - 1) * around
        faces.append([front + 1, base + k, base + (k + 1) % around])
    indices = np.array(faces, dtype=np.uint32)
    normals = positions.copy()
    normals[:, 0] = 0.0
    normals[front] = [-1.0, 0.0, 0.0]
    normals[front + 1] = [1.0, 0.0, 0.0]
    lengths = np.linalg.norm(normals, axis=1, keepdims=True)
    normals = normals / np.maximum(lengths, 1e-9)
    return Mesh(positions, normals.astype(np.float32), indices, "tube")


def _arm(length: float = 4.0) -> Skeleton:
    """Three joints along the tube: root, an elbow half way, a tip at the end."""
    return Skeleton(
        name="arm",
        joints=[
            make_joint("shoulder", -1, (0.0, 0.0, 0.0)),
            make_joint("elbow", 0, (length / 2, 0.0, 0.0)),
            make_joint("wrist", 1, (length / 2, 0.0, 0.0)),
        ],
    )


def _dense(rig, joint_count: int) -> np.ndarray:
    skin = rig.skin
    dense = np.zeros((len(skin.joints), joint_count))
    for slot in range(4):
        np.add.at(dense, (np.arange(len(dense)), skin.joints[:, slot]), skin.weights[:, slot])
    return dense


# -- the bones ---------------------------------------------------------


def test_a_joint_owns_the_bones_that_leave_it_and_a_leaf_a_bone_of_its_own() -> None:
    skeleton = _arm()
    segments, owners = bone_segments(skeleton, skeleton.positions())
    assert owners.tolist() == [0, 1, 2]
    # The leaf's bone carries on past it as far as its parent's bone went.
    assert np.allclose(segments[2], [[4.0, 0.0, 0.0], [6.0, 0.0, 0.0]])


def test_a_lone_joint_owns_the_point_it_stands_on() -> None:
    skeleton = Skeleton(joints=[make_joint("only", -1, (1.0, 2.0, 3.0))])
    segments, owners = bone_segments(skeleton, skeleton.positions())
    assert owners.tolist() == [0]
    assert np.allclose(segments[0][0], segments[0][1])


def test_names_are_made_unique_for_the_skin_to_match_by() -> None:
    assert unique_names(["a", "b", "a", "a", "a.2"]) == ["a", "b", "a.2", "a.3", "a.2.2"]


# -- the methods -------------------------------------------------------


@pytest.mark.parametrize("method", list(SkinMethod))
def test_every_method_holds_the_whole_tube_and_sums_to_one(method: SkinMethod) -> None:
    mesh, skeleton = _tube(), _arm()
    made = auto_skin(mesh, skeleton, AutoSkinSettings(method=method))
    dense = _dense(made.rig, 3)
    assert dense.shape == (mesh.vertex_count, 3)
    assert np.allclose(dense.sum(axis=1), 1.0, atol=1e-4)
    assert made.unclaimed == 0
    assert made.rig.tag and all(joint.source for joint in made.joints)


def test_the_near_half_follows_the_shoulder_and_the_far_half_the_elbow() -> None:
    mesh, skeleton = _tube(), _arm()
    made = auto_skin(mesh, skeleton, AutoSkinSettings(method=SkinMethod.HEAT))
    dense = _dense(made.rig, 3)
    x = mesh.positions[:, 0]
    near = dense[x < 1.0]
    far = dense[(x > 3.0) & (x < 3.9)]
    assert near[:, 0].min() > 0.9
    assert far[:, 1].min() > 0.9
    # Across the elbow the weights blend rather than jump.
    across = dense[np.abs(x - 2.0) < 0.15]
    assert 0.2 < across[:, 0].mean() < 0.8


def test_nearest_bone_is_rigid_and_envelope_is_soft() -> None:
    mesh, skeleton = _tube(), _arm()
    rigid = _dense(auto_skin(mesh, skeleton, AutoSkinSettings(method=SkinMethod.NEAREST)).rig, 3)
    soft = _dense(auto_skin(mesh, skeleton, AutoSkinSettings(method=SkinMethod.ENVELOPE)).rig, 3)
    assert np.all(np.isin(rigid, (0.0, 1.0)))
    assert np.any((soft > 0.05) & (soft < 0.95))


def test_influences_cap_how_many_bones_share_a_vertex() -> None:
    mesh, skeleton = _tube(), _arm()
    made = auto_skin(mesh, skeleton, AutoSkinSettings(method=SkinMethod.ENVELOPE, influences=1))
    assert np.all(np.isin(made.rig.skin.weights[:, 1:], 0.0))
    assert np.allclose(made.rig.skin.weights[:, 0], 1.0)


# -- binding -----------------------------------------------------------


def test_the_pose_at_skinning_becomes_the_rest() -> None:
    mesh, skeleton = _tube(), _arm()
    skeleton.joints[1] = replace(
        skeleton.joints[1], rotation=tuple(quat_from_axis_angle([0, 0, 1], 0.5))
    )
    before = skeleton.positions()
    made = auto_skin(mesh, skeleton)
    bound = Skeleton(name="arm", joints=made.joints, rig_tag=made.rig.tag)
    assert not bound.posed
    assert np.allclose(bound.positions(), before)
    assert np.allclose(made.rig.rest_world()[:, :3, 3], before)


def test_a_skinned_mesh_stands_still_at_rest_and_bends_at_the_elbow() -> None:
    mesh, skeleton = _tube(), _arm()
    made = auto_skin(mesh, skeleton)
    dressed = Mesh(mesh.positions, mesh.normals, mesh.indices, "tube", rig=made.rig)
    bound = Skeleton(name="arm", joints=made.joints, rig_tag=made.rig.tag)
    still = skinned_mesh(dressed, bound)
    assert np.allclose(still.positions, mesh.positions, atol=1e-5)
    bound.joints[1] = replace(
        bound.joints[1], rotation=tuple(quat_from_axis_angle([0, 0, 1], np.pi / 2))
    )
    bent = skinned_mesh(dressed, bound)
    x = mesh.positions[:, 0]
    # The near half all but stays: what moves there is the far tail of the
    # elbow's warmth, a few hundredths at most.
    assert np.abs(bent.positions[x < 1.0] - mesh.positions[x < 1.0]).max() < 0.1
    tip = bent.positions[x > 3.9]
    # The far end has swung up: it now stands above the elbow, not beyond it.
    assert tip[:, 1].mean() > 1.5 and abs(tip[:, 0].mean() - 2.0) < 0.5


def test_the_rig_only_answers_to_the_skeleton_it_was_made_for() -> None:
    mesh, skeleton = _tube(), _arm()
    made = auto_skin(mesh, skeleton)
    twin = Skeleton(name="arm", joints=[replace(j) for j in made.joints], rig_tag="other")
    assert made.rig.answers_to(Skeleton(name="arm", joints=made.joints, rig_tag=made.rig.tag))
    assert not made.rig.answers_to(twin)


def test_nothing_to_skin_is_said_so() -> None:
    mesh = _tube()
    with pytest.raises(AutoSkinError):
        auto_skin(mesh, Skeleton(joints=[]))
    empty = Mesh(np.zeros((0, 3)), np.zeros((0, 3)), np.zeros((0, 3)))
    with pytest.raises(AutoSkinError):
        auto_skin(empty, _arm())


# -- progress ----------------------------------------------------------


def test_skinning_reports_as_it_goes_and_stops_when_told() -> None:
    mesh, skeleton = _tube(), _arm()
    seen: list[float] = []

    def watch(progress: Progress) -> None:
        seen.append(progress.fraction)

    progress = Progress("skin", watch)
    auto_skin(mesh, skeleton, progress=progress)
    assert seen and seen[-1] == 1.0 and seen == sorted(seen)

    stopping = Progress("skin")
    stopping.cancel()
    with pytest.raises(CancelledError):
        auto_skin(mesh, skeleton, progress=stopping)


# -- the file ----------------------------------------------------------


def test_a_skin_survives_the_archive_and_refuses_another_model(tmp_path) -> None:
    mesh, skeleton = _tube(), _arm()
    made = auto_skin(mesh, skeleton)
    path = save_rig(made.rig, tmp_path / "tube.skin.npz")
    back = load_rig(path, mesh)
    assert back.names == made.rig.names and back.parents == made.rig.parents
    assert back.tag == made.rig.tag
    assert np.array_equal(back.skin.joints, made.rig.skin.joints)
    assert np.allclose(back.skin.weights, made.rig.skin.weights)
    assert np.allclose(back.rest_local, made.rig.rest_local)
    with pytest.raises(RigFileError):
        load_rig(path, _tube(rings=5))
    with pytest.raises(RigFileError):
        load_rig(tmp_path / "missing.skin.npz", mesh)


# -- in the document ---------------------------------------------------


def _scene(tmp_path):
    from refview.core.mesh_io import save_mesh
    from refview.ui.state import ViewerState

    state = ViewerState()
    path = save_mesh(_tube(), tmp_path / "tube.obj")
    state.load_mesh(path, load_sidecar=False)
    return state, state.active_object


def test_the_document_dresses_an_object_and_undresses_it_again(tmp_path) -> None:
    from refview.core.scene import Transform

    state, obj = _scene(tmp_path)
    state.set_transform(obj, Transform(translation=(1.0, 2.0, 3.0), rotation_deg=(0, 30, 0)))
    skeleton = _arm()
    state.skeletons.add(skeleton)
    world = state.objects.world_matrix(obj)
    # The skeleton stands in the world, so it is carried to where the tube is.
    skeleton.carry(world)
    made = auto_skin(obj.world_rest(world), skeleton)
    before = state.mesh.positions.copy()
    assert state.skin_object(obj, skeleton, made, world)
    assert state.bound_skeleton() is skeleton and state.object_for(skeleton) is obj
    assert np.allclose(state.mesh.positions, before, atol=1e-4)

    posed = [replace(joint) for joint in skeleton.joints]
    posed[1] = replace(posed[1], rotation=tuple(quat_from_axis_angle([0, 0, 1], 1.0)))
    from refview.core.commands import SetAttributes
    from refview.core.history import SKELETON

    state.do(SetAttributes(skeleton, {"joints": posed}, text="pose", channel=SKELETON))
    assert not np.allclose(state.mesh.positions, before, atol=1e-2)
    state.undo()
    assert np.allclose(state.mesh.positions, before, atol=1e-4)
    state.undo()
    assert obj.rig is None and state.bound_skeleton() is None
    assert not any(joint.source for joint in skeleton.joints)
    state.redo()
    assert state.bound_skeleton() is skeleton
    state.unskin_object(obj, skeleton)
    assert obj.rig is None and skeleton.rig_tag == ""


def test_a_skin_made_here_goes_with_the_session_and_comes_back(tmp_path) -> None:
    from refview.ui.state import ViewerState

    state, obj = _scene(tmp_path)
    skeleton = _arm()
    state.skeletons.add(skeleton)
    world = state.objects.world_matrix(obj)
    made = auto_skin(obj.world_rest(world), skeleton)
    state.skin_object(obj, skeleton, made, world)
    session = state.save_session(tmp_path / "tube.refview.json")
    archive = tmp_path / "tube.tube.skin.npz"
    assert archive.is_file() and obj.skin_path == archive

    back = ViewerState()
    back.load_session(session)
    again = back.active_object
    bound = back.bound_skeleton()
    assert again.rig is not None and again.rig.tag == made.rig.tag
    assert bound is not None and bound.rig_tag == made.rig.tag
    assert np.array_equal(again.rig.skin.joints, obj.rig.skin.joints)

    # A second skeleton built from the same preset names its joints the
    # same way, and must not be taken for the one the skin was made for.
    twin = _arm()
    twin.joints = [replace(joint, source=joint.name) for joint in twin.joints]
    back.skeletons.items.insert(0, twin)
    assert back.bound_skeleton() is bound
