"""Several objects in one scene: placing, linking, merging, splitting, saving."""

from __future__ import annotations

import json
import os

import numpy as np
import pytest
from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtWidgets import QApplication

from refview.core.grid import GridSettings, build_grid, nice_step
from refview.core.linalg import quat_from_axis_angle
from refview.core.mesh import Bounds, Mesh, concatenated, loose_parts, submesh
from refview.core.mesh_io import save_mesh
from refview.core.scene import (
    ObjectSettings,
    ObjectStore,
    SceneObject,
    Transform,
    merge_objects,
    split_object,
)
from refview.core.session import Session
from refview.core.skeleton import Rig, Skin
from refview.ui.object_tool import ObjectTool
from refview.ui.picking import SurfacePicker
from refview.ui.state import ViewerState


@pytest.fixture(scope="session")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    return QApplication.instance() or QApplication([])


def _tetra(shift=(0.0, 0.0, 0.0)) -> Mesh:
    points = np.array(
        [[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32
    ) + np.asarray(shift, dtype=np.float32)
    faces = np.array([[0, 2, 1], [0, 1, 3], [0, 3, 2], [1, 2, 3]], dtype=np.uint32)
    normals = np.tile([0, 0, 1], (4, 1)).astype(np.float32)
    return Mesh(points, normals, faces, name="tetra")


def _two_pieces() -> Mesh:
    one, two = _tetra(), _tetra((5.0, 0.0, 0.0))
    return concatenated([one, two], name="pair")


# ----------------------------------------------------------------------
# Transforms and the store
# ----------------------------------------------------------------------


def test_transform_round_trips_through_its_matrix():
    original = Transform(translation=(1.0, -2.0, 3.0), rotation_deg=(10.0, -35.0, 80.0),
                         scale=(2.0, 0.5, 1.5))
    back = Transform.from_matrix(original.matrix)
    assert np.allclose(back.matrix, original.matrix, atol=1e-9)
    assert back.translation == pytest.approx(original.translation)
    assert back.scale == pytest.approx(original.scale)
    assert Transform().is_identity and not original.is_identity


def test_world_matrices_chain_through_parents_and_linking_keeps_place():
    store = ObjectStore()
    parent = store.add(SceneObject(_tetra(), name="parent"))
    child = store.add(SceneObject(_tetra(), name="child"))
    parent.transform = Transform(translation=(10.0, 0.0, 0.0), rotation_deg=(0.0, 90.0, 0.0))
    child.transform = Transform(translation=(1.0, 2.0, 3.0))
    before = store.world_matrix(child).copy()
    assert store.set_parent(child, parent, keep_transform=True)
    assert child.parent is parent
    assert np.allclose(store.world_matrix(child), before, atol=1e-9)
    assert child.transform.translation != pytest.approx((1.0, 2.0, 3.0))
    # A loop is refused: the parent cannot hang from its own child.
    assert not store.set_parent(parent, child)
    assert [obj.name for obj, _ in store.ordered()] == ["parent", "child"]
    assert store.ordered()[1][1] == 1


def test_visibility_and_solidity_follow_the_parent_when_asked():
    store = ObjectStore()
    parent = store.add(SceneObject(_tetra(), name="parent"))
    child = store.add(SceneObject(_tetra(), name="child"))
    store.set_parent(child, parent)
    parent.visible = False
    parent.opacity = 0.5
    child.opacity = 0.5
    strict = ObjectSettings()
    loose = ObjectSettings(hide_children=False, ghost_children=False)
    assert not store.shown(child, strict) and store.shown(child, loose)
    assert store.opacity(child, strict) == pytest.approx(0.25)
    assert store.opacity(child, loose) == pytest.approx(0.5)


def test_removing_a_parent_rehangs_or_removes_its_children():
    store = ObjectStore()
    parent = store.add(SceneObject(_tetra(), name="parent"))
    child = store.add(SceneObject(_tetra(), name="child"))
    parent.transform = Transform(translation=(3.0, 0.0, 0.0))
    store.set_parent(child, parent)
    world = store.world_matrix(child).copy()
    gone = store.remove(parent, ObjectSettings(remove_children=False))
    assert gone == [parent] and child.parent is None and len(store) == 1
    assert np.allclose(store.world_matrix(child), world)

    store = ObjectStore()
    parent = store.add(SceneObject(_tetra(), name="parent"))
    child = store.add(SceneObject(_tetra(), name="child"))
    store.set_parent(child, parent)
    gone = store.remove(parent, ObjectSettings(remove_children=True))
    assert len(gone) == 2 and len(store) == 0 and store.active == -1


def test_snapshots_put_the_list_back_exactly():
    store = ObjectStore()
    a = store.add(SceneObject(_tetra(), name="a"))
    b = store.add(SceneObject(_tetra(), name="b"))
    snapshot = store.snapshot()
    b.transform = Transform(translation=(1.0, 1.0, 1.0))
    store.set_parent(b, a, keep_transform=False)
    store.remove(a, ObjectSettings(remove_children=True))
    assert len(store) == 0
    store.restore(snapshot)
    assert [obj.name for obj in store] == ["a", "b"]
    assert b.parent is None and b.transform.is_identity


# ----------------------------------------------------------------------
# Meshes: joining and splitting
# ----------------------------------------------------------------------


def test_loose_parts_are_found_by_shared_positions_and_split_apart():
    pair = _two_pieces()
    pieces = loose_parts(pair)
    assert [len(piece) for piece in pieces] == [4, 4]
    part = submesh(pair, pieces[1])
    assert part.vertex_count == 4 and part.triangle_count == 4
    assert loose_parts(_tetra()) and len(loose_parts(_tetra())) == 1
    assert loose_parts(Mesh(np.zeros((0, 3)), np.zeros((0, 3)), np.zeros((0, 3)))) == []


def test_merging_and_splitting_objects_leaves_the_geometry_where_it_stood():
    store = ObjectStore()
    left = store.add(SceneObject(_tetra(), name="left"))
    right = store.add(SceneObject(_tetra(), name="right"))
    right.transform = Transform(translation=(5.0, 0.0, 0.0), scale=(2.0, 2.0, 2.0))
    expected = np.concatenate(
        [left.world_rest(store.world_matrix(left)).positions,
         right.world_rest(store.world_matrix(right)).positions]
    )
    merged = merge_objects(store, [left, right], name="both")
    store.add(merged)
    world = merged.world_rest(store.world_matrix(merged))
    assert world.vertex_count == 8
    assert np.allclose(np.sort(world.positions, axis=0), np.sort(expected, axis=0), atol=1e-5)
    # The pivot sits at the middle of the joined box, not at either source.
    assert merged.transform.translation == pytest.approx(tuple(world.bounds.center), abs=1e-5)

    pieces = split_object(store, merged)
    assert pieces is not None and len(pieces) == 2
    back = np.concatenate(
        [piece.world_rest(store.world_matrix(piece)).positions for piece in pieces]
    )
    assert np.allclose(np.sort(back, axis=0), np.sort(expected, axis=0), atol=1e-4)
    assert split_object(store, left) is None


def test_transformed_by_keeps_normals_square_to_a_stretched_surface():
    mesh = Mesh(
        np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], np.float32),
        np.tile([0, 0, 1], (3, 1)).astype(np.float32),
        [[0, 1, 2]],
    )
    matrix = Transform(rotation_deg=(0.0, 0.0, 90.0), scale=(1.0, 4.0, 1.0)).matrix
    carried = mesh.transformed_by(matrix)
    assert np.allclose(np.linalg.norm(carried.normals, axis=1), 1.0)
    assert np.allclose(carried.normals, [[0, 0, 1]] * 3)
    assert mesh.transformed_by(np.eye(4)) is mesh


# ----------------------------------------------------------------------
# The grid
# ----------------------------------------------------------------------


def test_grid_lines_cover_the_enabled_planes_and_pick_round_spacings():
    assert nice_step(0.37) == pytest.approx(0.2)
    assert nice_step(7.0) == pytest.approx(5.0)
    assert nice_step(0.0) == 1.0
    bounds = Bounds(np.array([-1.0, -2.0, -1.0]), np.array([1.0, 2.0, 1.0]))
    settings = GridSettings(count=10)
    lines = build_grid(settings, bounds, 2.0)
    assert lines is not None
    assert len(lines.segments) == 2 * 21
    assert np.allclose(lines.segments[:, :, 1], -2.0)  # the floor sits under the scene
    assert lines.widths.max() > lines.widths.min()  # heavy lines every tenth
    settings = GridSettings(ground=False, front=True, side=True, count=4, spacing=0.5,
                            at_floor=False, show_axes=False)
    lines = build_grid(settings, bounds, 2.0)
    assert len(lines.segments) == 4 * 9
    assert np.allclose(np.abs(lines.segments).max(), 2.0)
    assert build_grid(GridSettings(ground=False), bounds, 1.0) is None


# ----------------------------------------------------------------------
# The document
# ----------------------------------------------------------------------


def _skinned_strip() -> Mesh:
    positions = np.array(
        [[0, 0, 0], [1, 0, 0], [0, 0, 1], [1, 0, 1], [0, 1, 0], [1, 1, 0], [0, 1, 1], [1, 1, 1]],
        dtype=np.float32,
    )
    normals = np.tile([0, 0, 1], (8, 1)).astype(np.float32)
    faces = np.array([[0, 1, 5], [0, 5, 4], [2, 3, 7], [2, 7, 6]], dtype=np.uint32)
    joints = np.zeros((8, 4), dtype=np.int32)
    joints[4:, 0] = 1
    weights = np.zeros((8, 4), dtype=np.float32)
    weights[:, 0] = 1.0
    rest = np.array([np.eye(4), np.eye(4)])
    rest[1, 1, 3] = 1.0
    inverse_bind = np.array([np.eye(4), np.linalg.inv(rest[1])])
    skin = Skin(joints, weights, inverse_bind, positions, normals)
    return Mesh(positions, normals, faces, name="strip",
                rig=Rig(["root", "tip"], [-1, 0], rest, skin))


def test_adding_objects_builds_one_scene_mesh_and_records_undo_steps(app):
    state = ViewerState()
    state.source_mesh = _tetra()
    state.notify_skeleton()
    assert state.mesh is not None and len(state.objects) == 1
    only = state.active_object
    state.set_transform(only, Transform(translation=(2.0, 0.0, 0.0)))
    assert state.mesh is not only.rest_mesh
    shifted = only.rest_mesh.bounds.center + [2, 0, 0]
    assert np.allclose(state.mesh.bounds.center, shifted, atol=1e-5)
    assert state.history.can_undo
    state.undo()
    assert only.transform.is_identity and state.mesh is only.rest_mesh
    state.redo()
    assert only.transform.translation == pytest.approx((2.0, 0.0, 0.0))


def test_hidden_objects_leave_the_scene_mesh_and_come_back(app):
    state = ViewerState()
    state.source_mesh = _tetra()
    first = state.active_object
    other = _tetra((3.0, 0.0, 0.0))
    second = SceneObject(other, state._oriented(other, state.orientation), name="second")
    before = state.snapshot_objects()
    state.objects.add(second)
    state._commit_objects(before, "Add second")
    assert state.mesh.vertex_count == 8 and len(state.mesh_parts) == 2
    assert state.triangle_owner(0) is first and state.triangle_owner(5) is second
    state.set_object_visible(first, False)
    assert state.mesh.vertex_count == 4 and state.mesh_parts[0][0] is second
    state.set_object_visible(second, False)
    assert state.mesh is None and state.mesh_parts == []
    state.undo()
    state.undo()
    assert state.mesh.vertex_count == 8
    # Solidity travels to the renderer's parts without touching geometry.
    state.set_object_opacity(second, 0.4)
    assert state.mesh_parts[1][2] == pytest.approx(0.4)
    state.set_parent(second, first)
    first.opacity = 0.5
    state.notify_object_settings()
    assert state.mesh_parts[1][2] == pytest.approx(0.2)


def test_moving_a_rigged_object_carries_its_skeleton_and_keeps_the_pose(app):
    state = ViewerState()
    mesh = _skinned_strip()
    state.source_mesh = mesh
    state.rest_mesh = state.mesh = mesh
    state.skeletons.add(mesh.rig.to_skeleton("strip"))
    skeleton = state.skeletons[0]
    skeleton.joints[1].rotation = tuple(quat_from_axis_angle([0, 0, 1], np.pi / 2))
    state.notify_skeleton()
    posed = state.mesh.positions.copy()
    joints = skeleton.positions().copy()
    obj = state.active_object
    state.set_transform(obj, Transform(translation=(0.0, 0.0, 4.0)))
    assert np.allclose(state.mesh.positions, posed + [0, 0, 4], atol=1e-5)
    assert np.allclose(skeleton.positions(), joints + [0, 0, 4], atol=1e-6)
    state.undo()
    assert np.allclose(state.mesh.positions, posed, atol=1e-5)
    assert np.allclose(skeleton.positions(), joints, atol=1e-6)


def test_merge_split_and_remove_are_undoable_edits(app):
    state = ViewerState()
    state.source_mesh = _two_pieces()
    whole = state.active_object
    pieces = state.split_object(whole)
    assert len(pieces) == 2 and len(state.objects) == 2 and whole not in state.objects.items
    assert state.mesh.vertex_count == 8
    merged = state.merge_objects(list(state.objects))
    assert merged is not None and len(state.objects) == 1
    assert state.mesh.vertex_count == 8
    state.remove_object(merged)
    assert len(state.objects) == 0 and state.mesh is None
    state.undo()
    assert len(state.objects) == 1 and state.active_object is merged
    state.undo()
    assert len(state.objects) == 2
    state.undo()
    assert [obj.name for obj in state.objects] == [whole.name]


def test_sessions_carry_the_objects_and_write_out_the_ones_without_files(app, tmp_path):
    state = ViewerState()
    file = save_mesh(_tetra(), tmp_path / "one.obj")
    state.load_mesh(file, load_sidecar=False)
    first = state.active_object
    second = state.add_mesh(file)
    assert second is not first and second.name == "one.001"
    state.set_transform(second, Transform(translation=(1.0, 2.0, 3.0), scale=(2.0, 2.0, 2.0)))
    state.set_parent(second, first)
    merged = state.merge_objects([first, second])
    assert merged.path is None
    saved = state.save_session(tmp_path / "scene.refview.json")
    assert merged.path is not None and merged.path.is_file()
    written = json.loads(saved.read_text(encoding="utf-8"))
    assert written["version"] == 11 and len(written["objects"]) == 1

    fresh = ViewerState()
    fresh.load_session(saved)
    assert [obj.name for obj in fresh.objects] == ["Merged"]
    assert np.allclose(
        fresh.mesh.positions.mean(axis=0), state.mesh.positions.mean(axis=0), atol=1e-4
    )

    # A hierarchy comes back with its parents and places.
    tree = ViewerState()
    tree.load_mesh(file, load_sidecar=False)
    root = tree.active_object
    leaf = tree.add_mesh(file)
    tree.set_transform(root, Transform(translation=(5.0, 0.0, 0.0)))
    tree.set_parent(leaf, root)
    leaf.opacity = 0.3
    path = tree.save_session(tmp_path / "tree.refview.json")
    back = ViewerState()
    back.load_session(path)
    names = {obj.name: obj for obj in back.objects}
    assert names["one.001"].parent is names["one"]
    assert names["one.001"].opacity == pytest.approx(0.3)
    assert names["one"].transform.translation == pytest.approx((5.0, 0.0, 0.0))
    assert np.allclose(back.mesh.positions, tree.mesh.positions, atol=1e-5)


def test_an_old_session_reads_as_one_object_at_its_mesh_path(tmp_path):
    session = Session.from_dict({"version": 8, "mesh_path": "bust.obj"})
    assert session.objects == [] and session.mesh_path == "bust.obj"
    assert ViewerState._records(None, session)[0].path == "bust.obj"


# ----------------------------------------------------------------------
# The gizmo
# ----------------------------------------------------------------------


def test_gizmo_gestures_move_turn_and_scale_the_object(app):
    state = ViewerState()
    state.source_mesh = _tetra()
    obj = state.active_object
    state.camera.frame(state.mesh.bounds)
    state.camera.eye = np.array([0.0, 0.0, 10.0])
    state.camera.target = np.zeros(3)
    picker = SurfacePicker(state.camera, state.mesh, 400, 300)
    tool = ObjectTool()
    world = state.objects.world_matrix(obj)
    gizmo = tool.gizmo(picker, world)
    assert gizmo is not None
    ox, oy = gizmo.origin
    assert tool.handle_at(ox, oy, gizmo) == "centre"
    tip = gizmo.arms[0][0]
    assert tool.handle_at(*tip, gizmo) == "x"

    # A drag along the X arm moves along X and nothing else.
    assert tool.begin("x", *tip, picker, world, np.eye(4))
    moved = tool.drag(tip[0] + 40.0, tip[1], picker)
    assert moved.translation[0] > 0.0
    assert moved.translation[1:] == pytest.approx((0.0, 0.0), abs=1e-6)
    assert moved.rotation_deg == pytest.approx((0.0, 0.0, 0.0), abs=1e-6)
    tool.end()

    # A turn about the ring goes about the line of sight, snapped when asked.
    tool.set_mode("rotate")
    assert tool.begin("centre", ox + 50.0, oy, picker, world, np.eye(4))
    turned = tool.drag(ox, oy - 50.0, picker, snap_deg=15.0)
    assert turned.rotation_deg[2] == pytest.approx(90.0, abs=1e-6)
    tool.end()

    # A scale from the ring is uniform; from an arm it can be one axis.
    tool.set_mode("scale")
    assert tool.begin("centre", ox + 40.0, oy, picker, world, np.eye(4))
    grown = tool.drag(ox + 80.0, oy, picker)
    assert grown.scale == pytest.approx((2.0, 2.0, 2.0), abs=1e-6)
    tool.end()
    gizmo = tool.gizmo(picker, world)
    tip = gizmo.arms[1][0]
    assert tool.begin("y", *tip, picker, world, np.eye(4))
    stretched = tool.drag(ox + (tip[0] - ox) * 3.0, oy + (tip[1] - oy) * 3.0, picker, uniform=False)
    assert stretched.scale == pytest.approx((1.0, 3.0, 1.0), abs=1e-6)


def test_duplicating_copies_the_mesh_alone_where_it_stands(app):
    state = ViewerState()
    mesh = _skinned_strip()
    state.source_mesh = mesh
    state.rest_mesh = state.mesh = mesh
    state.skeletons.add(mesh.rig.to_skeleton("strip"))
    original = state.active_object
    child = SceneObject(_tetra(), name="child")
    state.objects.add(child, activate=False)
    state.objects.set_parent(child, original)
    state.set_transform(original, Transform(translation=(1.0, 2.0, 3.0), scale=(2.0, 2.0, 2.0)))

    copy = state.duplicate_object(original)
    assert copy is not None and state.active_object is copy
    assert copy.name == f"{original.name}.001" and copy.path is None
    # The same vertices, standing in the same place, hung from the same parent.
    assert copy.transform == original.transform and copy.parent is original.parent
    assert np.shares_memory(copy.rest_mesh.positions, original.rest_mesh.positions)
    assert copy.rest_mesh is not original.rest_mesh
    # But no rig -- the skeleton stays the original's -- and no children.
    assert copy.rig is None and original.rig is not None
    assert state.objects.children(copy) == [] and child.parent is original
    assert len(state.mesh_parts) == 3
    assert state.history.undo_text == f"Duplicate {original.name}"
    state.undo()
    assert len(state.objects) == 2 and state.objects.index(copy) < 0
    state.redo()
    assert state.active_object is copy


def _viewport(state):
    from refview.ui.viewport import Viewport

    made = Viewport(state)
    made.resize(800, 600)
    return made


def _mouse(kind, x, y, modifiers=Qt.KeyboardModifier.NoModifier):
    from PySide6.QtGui import QMouseEvent

    return QMouseEvent(
        kind, QPointF(x, y), QPointF(x, y), Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton, modifiers,
    )


def _key(kind, key, modifiers=Qt.KeyboardModifier.NoModifier):
    from PySide6.QtGui import QKeyEvent

    return QKeyEvent(kind, key, modifiers)


def _overridden(viewport, key, modifiers=Qt.KeyboardModifier.NoModifier) -> bool:
    """Whether the view claims ``key`` ahead of its shortcuts, as Qt would ask it."""
    offer = _key(QEvent.Type.ShortcutOverride, key, modifiers)
    offer.ignore()  # Qt offers the key declined, and reads whether it was taken.
    viewport.event(offer)
    return offer.isAccepted()


def test_gesture_keys_choose_the_gesture_only_while_the_tool_is_armed(app):
    state = ViewerState()
    state.source_mesh = _tetra()
    viewport = _viewport(state)
    try:
        heard = []
        viewport.object_mode_changed.connect(heard.append)
        # Disarmed, the letters are the view's own: the override is declined.
        assert not _overridden(viewport, Qt.Key.Key_E)
        viewport.keyPressEvent(_key(QEvent.Type.KeyPress, Qt.Key.Key_E))
        assert viewport.object_tool.mode == "move" and heard == []

        viewport.set_object_active(True)
        assert _overridden(viewport, Qt.Key.Key_E)
        for key, mode in ((Qt.Key.Key_E, "rotate"), (Qt.Key.Key_R, "scale"),
                          (Qt.Key.Key_W, "move")):
            viewport.keyPressEvent(_key(QEvent.Type.KeyPress, key))
            assert viewport.object_tool.mode == mode
        assert heard == ["rotate", "scale", "move"]
        # With a modifier the letter is somebody else's key.
        assert not _overridden(viewport, Qt.Key.Key_E, Qt.KeyboardModifier.ControlModifier)
    finally:
        viewport.close()


def test_alt_click_picks_an_object_under_any_tool_and_lights_it_up(app, monkeypatch):
    state = ViewerState()
    state.source_mesh = _tetra()
    first = state.active_object
    other = _tetra((3.0, 0.0, 0.0))
    second = SceneObject(
        other, state._oriented(other, state.orientation), name="second",
        transform=Transform(translation=(3.0, 0.0, 0.0)),
    )
    state.objects.add(second, activate=False)
    state.notify_object_settings()
    assert state.active_object is first
    state.camera.frame(state.mesh.bounds)
    state.camera.eye = np.array([1.5, 0.0, 12.0])
    state.camera.target = np.array([1.5, 0.0, 0.0])
    viewport = _viewport(state)
    try:
        viewport.set_annotate_active(True)  # Any tool: Alt-click still picks.
        inside = np.asarray(second.rest_mesh.bounds.center, dtype=np.float64) - 0.2
        x, y, _ = state.camera.project(
            inside + [3.0, 0.0, 0.0], viewport.width(), viewport.height()
        )
        hit = SurfacePicker(state.camera, state.mesh, viewport.width(), viewport.height()).hit(x, y)
        assert hit is not None and state.triangle_owner(hit.triangle) is second
        alt = Qt.KeyboardModifier.AltModifier
        viewport.mousePressEvent(_mouse(QEvent.Type.MouseButtonPress, x, y, alt))
        viewport.mouseReleaseEvent(_mouse(QEvent.Type.MouseButtonRelease, x, y, alt))
        assert state.active_object is second
        # Making it active put a line round it, which fades and then goes.
        assert viewport._highlight is not None and viewport._highlight[0] is second
        index, alpha = viewport._highlight_now()
        assert index == 1 and alpha == pytest.approx(1.0)
        from refview.ui import viewport as module

        began = viewport._highlight[1]
        monkeypatch.setattr(module, "perf_counter", lambda: began + module.HIGHLIGHT_HOLD + 0.45)
        _, alpha = viewport._highlight_now()
        assert 0.0 < alpha < 1.0
        monkeypatch.setattr(module, "perf_counter", lambda: began + 10.0)
        assert viewport._highlight_now() is None and viewport._highlight is None
        # An Alt-drag that travelled is an orbit, not a pick.
        viewport.mousePressEvent(_mouse(QEvent.Type.MouseButtonPress, x, y, alt))
        viewport.mouseMoveEvent(_mouse(QEvent.Type.MouseMove, x + 40, y + 40, alt))
        viewport.mouseReleaseEvent(_mouse(QEvent.Type.MouseButtonRelease, x + 40, y + 40, alt))
        assert state.active_object is second
    finally:
        viewport.close()


def test_normalizing_scales_the_selected_objects_to_the_active_one_as_one_undo_step():
    state = ViewerState()
    state.source_mesh = _tetra()
    first = state.active_object
    tall = Mesh(
        np.array([[0, 0, 0], [0.1, 0, 0], [0, 4, 0], [0, 0, 0.1]], dtype=np.float32),
        np.tile([0, 0, 1], (4, 1)).astype(np.float32),
        np.array([[0, 2, 1], [0, 1, 3], [0, 3, 2], [1, 2, 3]], dtype=np.uint32),
        name="tall",
    )
    second = SceneObject(tall, tall.recentered(), name="second")
    small = _tetra()
    third = SceneObject(small, small.recentered(), name="third",
                        transform=Transform(scale=(0.25, 0.25, 0.25)))
    state.objects.add(second, activate=False)
    state.objects.add(third, activate=False)
    state.set_parent(third, second)
    state.notify_object_settings()
    assert state.active_object is first
    steps = len(state.history._undo)

    assert state.normalize_objects([second, third]) == 2
    # Each is now as big as the active tetrahedron, in its largest extent,
    # the child measured after its parent was resized.
    for obj in (second, third):
        assert state._extent(obj) == pytest.approx(state._extent(first), rel=1e-6)
    # Uniform: the shape is kept.
    assert second.transform.scale[0] == pytest.approx(second.transform.scale[1])
    assert second.transform.scale[0] == pytest.approx(0.25)
    assert len(state.history._undo) == steps + 1
    state.undo()
    assert second.transform.scale == (1.0, 1.0, 1.0)
    assert third.transform.scale == pytest.approx((0.25, 0.25, 0.25))
    # Nothing but the active object chosen: nothing to do, nothing recorded.
    assert state.normalize_objects([first]) == 0
    assert len(state.history._undo) == steps


def test_reset_xform_bakes_the_turn_and_scale_into_the_mesh_and_nothing_moves(tmp_path):
    state = ViewerState()
    state.source_mesh = _tetra()
    obj = state.active_object
    state.set_transform(
        obj,
        Transform(translation=(1.0, 2.0, 3.0), rotation_deg=(30.0, -45.0, 10.0),
                  scale=(2.0, 0.5, 1.5)),
    )
    seen = state.mesh.positions.copy()
    was_source, was_rest, was_path = obj.source_mesh, obj.rest_mesh, obj.path
    steps = len(state.history._undo)

    assert state.reset_xform(obj)
    assert obj.transform.rotation_deg == (0.0, 0.0, 0.0)
    assert obj.transform.scale == (1.0, 1.0, 1.0)
    assert np.allclose(state.mesh.positions, seen, atol=1e-5)  # nothing in the view moved
    assert np.allclose(obj.rest_mesh.bounds.center, 0.0, atol=1e-5)  # the pivot is the centre
    assert obj.path is None  # the mesh is not the file's any more
    # The rest mesh is still the file mesh read through the orientation.
    again = state._oriented(obj.source_mesh, obj.orientation)
    assert np.allclose(again.positions, obj.rest_mesh.positions, atol=1e-5)
    assert len(state.history._undo) == steps + 1
    # Already reset: nothing to do and nothing recorded.
    assert not state.reset_xform(obj)
    assert len(state.history._undo) == steps + 1

    state.undo()
    assert obj.source_mesh is was_source and obj.rest_mesh is was_rest and obj.path is was_path
    assert obj.transform.scale == (2.0, 0.5, 1.5)
    assert np.allclose(state.mesh.positions, seen, atol=1e-5)
    state.redo()
    assert obj.transform.scale == (1.0, 1.0, 1.0)

    # Saved, the baked mesh is written beside the session and comes back as it stands.
    saved = state.save_session(tmp_path / "baked.refview.json")
    fresh = ViewerState()
    fresh.load_session(saved)
    assert np.allclose(fresh.mesh.positions, seen, atol=1e-4)
    assert fresh.active_object.transform.scale == (1.0, 1.0, 1.0)


def test_reset_xform_keeps_a_file_s_rig_and_its_skeleton_answering(tmp_path):
    path = tmp_path / "strip.obj"
    save_mesh(_skinned_strip(), path)
    state = ViewerState()
    state.load_mesh(path, load_sidecar=False, source=_skinned_strip())
    obj = state.active_object
    assert obj.rig is not None and state.bound_skeleton() is not None
    skeleton = state.bound_skeleton()
    state.set_transform(obj, Transform(rotation_deg=(0.0, 90.0, 0.0), scale=(2.0, 2.0, 2.0)))
    seen = state.mesh.positions.copy()

    assert state.reset_xform(obj)
    assert obj.rig is not None and obj.rig.tag and skeleton.rig_tag == obj.rig.tag
    assert state.bound_skeleton() is skeleton
    assert np.allclose(state.mesh.positions, seen, atol=1e-5)
    # Posing still deforms the baked mesh through the carried rig.
    skeleton.joints[1].translation = (0.0, 0.5, 0.0)
    state.notify_skeleton()
    assert not np.allclose(state.mesh.positions, seen, atol=1e-5)
    skeleton.joints[1].translation = (0.0, 0.0, 0.0)
    state.notify_skeleton()

    saved = state.save_session(tmp_path / "strip.refview.json")
    assert obj.skin_path is not None and obj.skin_path.is_file()
    fresh = ViewerState()
    fresh.load_session(saved)
    assert fresh.active_object.rig is not None and fresh.bound_skeleton() is not None
    assert np.allclose(fresh.mesh.positions, seen, atol=1e-4)

    state.undo()
    assert obj.rig is not None and not obj.rig.tag and skeleton.rig_tag == ""
    assert state.bound_skeleton() is skeleton
