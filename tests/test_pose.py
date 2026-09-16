"""The pose tool, its gestures in the viewport, and the panel that lists the joints."""

from __future__ import annotations

import os

import numpy as np
import pytest
from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication

from refview.core.armature import Armature, ArmatureNode, Bone
from refview.core.camera import Camera
from refview.core.linalg import quat_from_axis_angle
from refview.core.mesh import Mesh
from refview.core.orientation import OrientationSettings, UpAxis
from refview.core.rigging import build_humanoid_skeleton
from refview.core.skeleton import Rig, Skeleton, SkeletonSettings, Skin, make_joint
from refview.ui.panels.pose_panel import PosePanel
from refview.ui.picking import SurfacePicker
from refview.ui.pose_tool import PoseTool
from refview.ui.state import ViewerState
from refview.ui.viewport import Viewport


@pytest.fixture(scope="session")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    return QApplication.instance() or QApplication([])


def _arm() -> Skeleton:
    return Skeleton(
        name="arm",
        joints=[
            make_joint("shoulder", -1, (0.0, 0.0, 0.0)),
            make_joint("elbow", 0, (1.0, 0.0, 0.0)),
            make_joint("wrist", 1, (1.0, 0.0, 0.0)),
        ],
    )


def _skinned_strip() -> Mesh:
    """A ribbon along +X with two joints, the far half held by the second."""
    xs = np.linspace(0.0, 2.0, 5)
    positions = np.array([[x, y, 0.0] for x in xs for y in (0.0, 0.2)], dtype=np.float32)
    indices = []
    for station in range(4):
        a, b = 2 * station, 2 * station + 1
        indices += [[a, b, a + 2], [b, b + 2, a + 2]]
    joints = np.zeros((len(positions), 4), dtype=np.int32)
    joints[:, 0] = (positions[:, 0] >= 1.0).astype(np.int32)
    weights = np.zeros((len(positions), 4), dtype=np.float32)
    weights[:, 0] = 1.0
    rest_local = np.tile(np.eye(4), (2, 1, 1))
    rest_local[1, 0, 3] = 1.0
    inverse_bind = np.tile(np.eye(4), (2, 1, 1))
    inverse_bind[1, 0, 3] = -1.0
    normals = np.tile([0.0, 0.0, 1.0], (len(positions), 1)).astype(np.float32)
    rig = Rig(["root", "tip"], [-1, 0], rest_local, Skin(joints, weights, inverse_bind,
                                                          positions, normals))
    return Mesh(positions, normals, np.array(indices, dtype=np.uint32), "strip", rig=rig)


def _front_camera() -> Camera:
    """Looking down -Z at the origin, so X is across and Y is up on screen."""
    return Camera(eye=np.array([0.0, 0.0, 10.0]), target=np.zeros(3))


# ----------------------------------------------------------------------
# The tool
# ----------------------------------------------------------------------


def test_pulling_a_joint_swings_its_parent_and_keeps_the_bone_length():
    arm = _arm()
    tool = PoseTool()
    swing = tool.swing(arm, 1, (0.0, 3.0, 0.0))
    assert swing is not None and swing.parent == 0
    arm.joints[0].rotation = swing.rotation
    at = arm.positions()
    assert np.allclose(at[1], [0, 1, 0], atol=1e-9)
    assert np.allclose(at[2], [0, 2, 0], atol=1e-9)


def test_a_locked_parent_refuses_the_swing_and_a_root_is_moved_instead():
    arm = _arm()
    arm.joints[0].locked = True
    assert PoseTool().swing(arm, 1, (0.0, 3.0, 0.0)) is None
    shift = PoseTool().move(arm, 0, (2.0, 2.0, 2.0))
    arm.joints[0].translation = shift
    assert np.allclose(arm.positions()[0], [2, 2, 2])
    assert np.allclose(arm.positions()[2], [4, 2, 2])


def test_twisting_rolls_about_the_bone_and_swinging_after_a_twist_still_aims():
    arm = _arm()
    tool = PoseTool()
    settings = SkeletonSettings(twist_per_pixel=1.0)
    arm.joints[0].rotation = tool.twist(arm, 0, 90.0, settings)
    # Rolling the shoulder about the +X bone leaves the arm where it was.
    assert np.allclose(arm.positions(), [[0, 0, 0], [1, 0, 0], [2, 0, 0]], atol=1e-9)
    swing = tool.swing(arm, 1, (0.0, 0.0, 5.0))
    arm.joints[0].rotation = swing.rotation
    assert np.allclose(arm.positions()[1], [0, 0, 1], atol=1e-9)


def test_fit_moves_the_rest_and_a_click_hangs_a_new_joint_under_the_selected_one():
    arm = _arm()
    tool = PoseTool()
    arm.joints = tool.fit(arm, 1, (1.0, 1.0, 0.0))
    assert np.allclose(arm.positions()[1], [1, 1, 0]) and np.allclose(arm.positions()[2], [2, 0, 0])
    joints = tool.place(arm, (2.0, 1.0, 0.0), parent=2)
    assert len(joints) == 4 and joints[3].parent == 2
    assert np.allclose(Skeleton(joints=joints).positions()[3], [2, 1, 0])
    roots = tool.place(arm, (5.0, 5.0, 5.0), parent=-1)
    assert roots[3].parent == -1


def test_joints_and_bones_are_picked_on_screen_and_locked_ones_are_not():
    arm = _arm()
    picker = SurfacePicker(_front_camera(), None, 800, 600)
    tool = PoseTool()
    settings = SkeletonSettings()
    x, y, _ = picker.camera.project(np.array([1.0, 0.0, 0.0]), 800, 600)
    assert tool.joint_at(x, y, [arm], picker, settings) == (0, 1)
    mid_x, mid_y, _ = picker.camera.project(np.array([1.5, 0.0, 0.0]), 800, 600)
    assert tool.joint_at(mid_x, mid_y, [arm], picker, settings) is None
    assert tool.bone_at(mid_x, mid_y, [arm], picker, settings) == (0, 2)
    arm.joints[1].locked = True
    assert tool.joint_at(x, y, [arm], picker, settings) is None
    arm.visible = False
    assert tool.bone_at(mid_x, mid_y, [arm], picker, settings) is None


# ----------------------------------------------------------------------
# The viewport
# ----------------------------------------------------------------------


def _event(kind, x, y, modifiers=Qt.KeyboardModifier.NoModifier):
    return QMouseEvent(
        kind, QPointF(x, y), QPointF(x, y), Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton, modifiers,
    )


def _screen(viewport: Viewport, point) -> tuple[float, float]:
    x, y, _ = viewport._state.camera.project(
        np.asarray(point, dtype=np.float64), viewport.width(), viewport.height()
    )
    return x, y


@pytest.fixture
def viewport(app):
    state = ViewerState()
    state.camera.apply(_front_camera())
    made = Viewport(state)
    made.resize(800, 600)
    yield made
    made.close()


def test_a_drag_on_a_joint_swings_the_bone_as_one_undo_step(viewport):
    state = viewport._state
    arm = _arm()
    state.skeletons.items.append(arm)
    x, y = _screen(viewport, [1.0, 0.0, 0.0])
    viewport.mousePressEvent(_event(QEvent.Type.MouseButtonPress, x, y))
    assert viewport.pose_tool.grabbed == (0, 1) and viewport.pose_tool.mode == "swing"
    up_x, up_y = _screen(viewport, [0.0, 1.0, 0.0])
    viewport.mouseMoveEvent(_event(QEvent.Type.MouseMove, up_x, up_y))
    assert np.allclose(arm.positions()[1], [0, 1, 0], atol=1e-6)
    viewport.mouseReleaseEvent(_event(QEvent.Type.MouseButtonRelease, up_x, up_y))
    assert viewport.pose_tool.grabbed is None
    assert state.history.undo_text == "Turn shoulder"
    state.undo()
    assert np.allclose(arm.positions()[1], [1, 0, 0])
    assert not arm.posed


def test_escape_puts_a_half_pulled_joint_back(viewport):
    state = viewport._state
    arm = _arm()
    state.skeletons.items.append(arm)
    x, y = _screen(viewport, [2.0, 0.0, 0.0])
    viewport.mousePressEvent(_event(QEvent.Type.MouseButtonPress, x, y))
    viewport.mouseMoveEvent(_event(QEvent.Type.MouseMove, x, y - 80))
    assert arm.posed
    viewport.cancel_tools()
    assert not arm.posed and not state.history.can_undo


def test_a_click_on_a_joint_selects_it_and_a_shift_drag_rolls_it(viewport):
    state = viewport._state
    arm = _arm()
    state.skeletons.items.append(arm)
    picked = []
    viewport.joint_selected.connect(picked.append)
    x, y = _screen(viewport, [1.0, 0.0, 0.0])
    viewport.mousePressEvent(_event(QEvent.Type.MouseButtonPress, x, y))
    viewport.mouseReleaseEvent(_event(QEvent.Type.MouseButtonRelease, x, y))
    assert picked == [(0, 1)] and not state.history.can_undo
    shift = Qt.KeyboardModifier.ShiftModifier
    viewport.mousePressEvent(_event(QEvent.Type.MouseButtonPress, x, y, shift))
    assert viewport.pose_tool.mode == "twist"
    viewport.mouseMoveEvent(_event(QEvent.Type.MouseMove, x + 90, y, shift))
    viewport.mouseReleaseEvent(_event(QEvent.Type.MouseButtonRelease, x + 90, y, shift))
    assert state.history.undo_text == "Turn elbow"
    assert arm.joints[1].posed
    # A roll about the bone leaves every joint where it was.
    assert np.allclose(arm.positions(), [[0, 0, 0], [1, 0, 0], [2, 0, 0]], atol=1e-9)


def test_dragging_a_root_moves_the_figure_and_fit_moves_the_rest(viewport):
    state = viewport._state
    arm = _arm()
    state.skeletons.items.append(arm)
    x, y = _screen(viewport, [0.0, 0.0, 0.0])
    viewport.mousePressEvent(_event(QEvent.Type.MouseButtonPress, x, y))
    assert viewport.pose_tool.mode == "move"
    viewport.mouseMoveEvent(_event(QEvent.Type.MouseMove, x, y - 60))
    viewport.mouseReleaseEvent(_event(QEvent.Type.MouseButtonRelease, x, y - 60))
    assert state.history.undo_text == "Move shoulder"
    assert arm.positions()[0][1] > 0.0 and arm.positions()[2][1] > 0.0
    state.undo()

    state.skeleton_settings.fit = True
    x, y = _screen(viewport, [1.0, 0.0, 0.0])
    viewport.mousePressEvent(_event(QEvent.Type.MouseButtonPress, x, y))
    assert viewport.pose_tool.mode == "fit"
    viewport.mouseMoveEvent(_event(QEvent.Type.MouseMove, x, y - 60))
    viewport.mouseReleaseEvent(_event(QEvent.Type.MouseButtonRelease, x, y - 60))
    assert state.history.undo_text == "Fit elbow"
    assert arm.positions()[1][1] > 0.0
    assert np.allclose(arm.positions()[2], [2, 0, 0], atol=1e-6)  # the wrist stayed put
    assert not arm.posed  # the rest moved, not the pose


def test_the_armed_tool_adds_a_joint_where_a_click_lands(viewport):
    state = viewport._state
    edits = []
    viewport.skeleton_edited.connect(edits.append)
    viewport.set_pose_active(True)
    state.skeleton_settings.free_placement = True
    viewport.mousePressEvent(_event(QEvent.Type.MouseButtonPress, 400, 300))
    viewport.mouseReleaseEvent(_event(QEvent.Type.MouseButtonRelease, 400, 300))
    assert len(edits) == 1
    index, joints, text = edits[0]
    assert index == -1 and len(joints) == 1 and joints[0].parent == -1
    assert text.startswith("Add")


# ----------------------------------------------------------------------
# The document
# ----------------------------------------------------------------------


def test_posing_the_bound_skeleton_re_skins_the_model_and_undo_puts_it_back(app):
    state = ViewerState()
    mesh = _skinned_strip()
    state.source_mesh = mesh
    state.rest_mesh = state.mesh = mesh
    state.skeletons.add(mesh.rig.to_skeleton("strip"))
    deformed, changed = [], []
    state.mesh_deformed.connect(lambda: deformed.append(True))
    state.mesh_changed.connect(lambda: changed.append(True))
    skeleton = state.skeletons[0]
    skeleton.joints[1].rotation = tuple(quat_from_axis_angle([0, 0, 1], np.pi / 2))
    state.notify_skeleton(live=True)
    assert deformed == [True] and changed == []
    assert state.mesh is not mesh and np.isclose(state.mesh.positions[:, 1].max(), 1.0)
    state.notify_skeleton()
    assert changed == [True]
    posed = state.mesh
    state.notify_skeleton()  # the same pose is not skinned twice
    assert state.mesh is posed
    state.skeleton_settings.deform = False
    state.notify_skeleton()
    assert state.mesh is mesh
    state.skeleton_settings.deform = True
    skeleton.joints = skeleton.with_pose_reset()
    state.notify_skeleton()
    assert state.mesh is mesh


def test_turning_the_model_carries_the_skeleton_and_the_skin_with_it(app, tmp_path):
    state = ViewerState()
    mesh = _skinned_strip()
    state.source_mesh = mesh
    state.rest_mesh = state.mesh = mesh
    state.skeletons.add(mesh.rig.to_skeleton("strip"))
    skeleton = state.skeletons[0]
    skeleton.joints[1].rotation = tuple(quat_from_axis_angle([0, 0, 1], np.pi / 2))
    state.notify_skeleton()
    before = state.mesh.positions.copy()
    state.set_orientation(OrientationSettings(up_axis=UpAxis.Z))
    turn = OrientationSettings(up_axis=UpAxis.Z).matrix
    # The joints and the posed model turned together: same shape, new frame.
    tip_before = mesh.rig.to_skeleton("t").positions()[1]
    expected_tip = turn @ tip_before - state.rest_mesh.source_offset + mesh.source_offset
    assert np.allclose(state.skeletons[0].positions()[1], expected_tip, atol=1e-6)
    rotated = before @ turn.T - (state.rest_mesh.source_offset - mesh.source_offset)
    assert np.allclose(state.mesh.positions, rotated, atol=1e-5)


def test_a_session_saved_beside_a_rigged_model_keeps_the_pose(app, tmp_path):
    state = ViewerState()
    mesh = _skinned_strip()
    state.source_mesh = mesh
    state.rest_mesh = state.mesh = mesh
    state.skeletons.add(mesh.rig.to_skeleton("strip"))
    state.skeletons[0].joints[1].rotation = tuple(quat_from_axis_angle([0, 0, 1], 0.5))
    state.notify_skeleton()
    path = state.save_session(tmp_path / "strip.refview.json")
    fresh = ViewerState()
    fresh.source_mesh = mesh
    fresh.rest_mesh = fresh.mesh = mesh
    fresh.load_session(path, load_mesh=False)
    assert fresh.skeletons[0].bound and fresh.skeletons[0].posed
    assert fresh.mesh is not mesh
    assert np.allclose(fresh.mesh.positions, state.mesh.positions)


# ----------------------------------------------------------------------
# The panel
# ----------------------------------------------------------------------


def test_the_panel_lists_joints_under_their_parents_and_follows_the_view(app):
    state = ViewerState()
    state.skeletons.add(_arm())
    panel = PosePanel(state)
    tool = PoseTool()
    panel.attach(tool)
    panel.refresh_list()
    top = panel._tree.topLevelItem(0)
    assert top.text(0) == "arm" and top.childCount() == 1
    shoulder = top.child(0)
    assert shoulder.text(0) == "shoulder" and shoulder.child(0).text(0) == "elbow"
    panel.select_joint((0, 2))
    assert panel._selected()[2].name == "wrist"
    assert tool.selected == (0, 2)
    panel.close()


def test_the_panel_turns_resets_and_re_hangs_the_selected_joint(app):
    state = ViewerState()
    state.skeletons.add(_arm())
    arm = state.skeletons[0]
    panel = PosePanel(state)
    panel.attach(PoseTool())
    panel.refresh_list()
    panel.select_joint((0, 0))
    panel._turn[2].set_value(90.0)
    panel._turn_live(90.0)
    assert arm.joints[0].posed
    panel._turn_commit(90.0)
    assert state.history.undo_text == "Turn shoulder"
    assert np.allclose(arm.positions()[1], [0, 1, 0], atol=1e-6)
    panel.reset_pose()
    assert not arm.posed and state.history.undo_text == "Reset arm"

    panel.select_joint((0, 2))
    panel._parent.setCurrentIndex(panel._parent.findData(0))
    app.processEvents()
    assert arm.joints[2].parent == 0
    assert np.allclose(arm.positions()[2], [2, 0, 0])
    panel.close()


def test_the_panel_grows_a_skeleton_from_an_armature_and_lays_one_back(app):
    state = ViewerState()
    wire = Armature(
        name="wire",
        nodes=[ArmatureNode(name=f"n{i}", at=(float(i), 0.0, 0.0)) for i in range(3)],
        bones=[Bone(0, 1), Bone(1, 2)],
    )
    state.armatures.add(wire)
    panel = PosePanel(state)
    panel.attach(PoseTool())
    panel.refresh_list()
    panel.from_armature()
    assert len(state.skeletons) == 1 and len(state.skeletons[0].joints) == 3
    assert state.history.undo_text == "Skeleton from wire"
    panel.to_armature()
    assert len(state.armatures) == 2 and state.armatures[1].name == "wire 2"
    assert len(state.armatures[1].bones) == 2
    panel.close()


def test_the_humanoid_preset_stands_in_the_models_box(app):
    state = ViewerState()
    figure = build_humanoid_skeleton(1.0)
    assert figure.roots() == [0]
    panel = PosePanel(state)
    panel.attach(PoseTool())
    panel.humanoid_preset()
    assert len(state.skeletons) == 1
    at = state.skeletons[0].positions()
    assert np.isclose(at[:, 1].min(), -0.9 + 0.018) and np.isclose(at[:, 1].max(), 0.9)
    assert state.skeletons[0].joint_for_role("pelvis") == 0
    panel.close()


def test_deleting_a_joint_keeps_the_chain_and_mapping_names_fills_roles(app):
    state = ViewerState()
    state.skeletons.add(
        Skeleton(
            joints=[
                make_joint("Hips", -1, (0.0, 1.0, 0.0)),
                make_joint("Spine", 0, (0.0, 0.2, 0.0)),
                make_joint("LeftUpLeg", 0, (0.1, 0.0, 0.0)),
                make_joint("LeftLeg", 2, (0.0, -0.5, 0.0)),
                make_joint("RightArm", 1, (-0.2, 0.0, 0.0)),
            ]
        )
    )
    panel = PosePanel(state)
    panel.attach(PoseTool())
    panel.refresh_list()
    assert panel.map_humanoid() == 5
    assert state.skeletons[0].joints[3].role == "knee.L"
    panel.select_joint((0, 2))
    panel._delete_selected()
    joints = state.skeletons[0].joints
    assert [joint.name for joint in joints] == ["Hips", "Spine", "LeftLeg", "RightArm"]
    assert joints[2].parent == 0
    assert np.allclose(state.skeletons[0].positions()[2], [0.1, 0.5, 0.0])
    panel.close()
