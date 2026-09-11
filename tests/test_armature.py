"""The armature graph, the humanoid landmarks and the joints they infer."""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.armature import (
    Armature,
    ArmatureNode,
    ArmatureSettings,
    ArmatureStore,
    Bone,
    PlacedLandmark,
)
from refview.core.camera import Camera
from refview.core.landmarks import (
    HUMANOID,
    HUMANOID_LANDMARKS,
    build_humanoid,
    median_plane,
    mirror_landmarks,
    mirror_point,
    rebuild,
)
from refview.core.session import Session
from refview.ui.armature_tool import ArmatureTool
from refview.ui.picking import SurfacePicker

#: A standing figure with +Y up, +Z forward and +X out to the figure's left.
#: Every paired landmark is written for the left side and mirrored in ``_figure``.
_CENTRE = {
    "vertex": (0.0, 180.0, 0.0),
    "c7": (0.0, 150.0, -6.0),
    "jugular_notch": (0.0, 148.0, 6.0),
    "t12": (0.0, 115.0, -6.0),
    "pubic_symphysis": (0.0, 90.0, 5.0),
}

_LEFT = {
    "acromion": (20.0, 148.0, 0.0),
    "humerus_lateral_epicondyle": (24.0, 112.0, 0.0),
    "humerus_medial_epicondyle": (16.0, 112.0, 0.0),
    "radial_styloid": (23.0, 85.0, 0.0),
    "ulnar_styloid": (17.0, 85.0, 0.0),
    "third_metacarpal_head": (20.0, 75.0, 0.0),
    "asis": (10.0, 100.0, 8.0),
    "psis": (8.0, 102.0, -8.0),
    "greater_trochanter": (16.0, 96.0, 0.0),
    "femur_lateral_epicondyle": (14.0, 55.0, 0.0),
    "femur_medial_epicondyle": (8.0, 55.0, 0.0),
    "lateral_malleolus": (12.0, 10.0, 0.0),
    "medial_malleolus": (8.0, 12.0, 0.0),
    "second_metatarsal_head": (10.0, 3.0, 12.0),
}


def _figure(scale: float = 1.0) -> dict[str, np.ndarray]:
    """Every required humanoid landmark, both sides, scaled about the origin."""
    placed = {key: np.array(at, dtype=np.float64) for key, at in _CENTRE.items()}
    for key, at in _LEFT.items():
        left = np.array(at, dtype=np.float64)
        placed[f"{key}.L"] = left
        placed[f"{key}.R"] = left * np.array([-1.0, 1.0, 1.0])
    return {key: at * scale for key, at in placed.items()}


def _roles(nodes: list[ArmatureNode]) -> dict[str, ArmatureNode]:
    return {node.role: node for node in nodes}


def _chain(count: int = 4) -> Armature:
    """A straight run of nodes one unit apart along +X."""
    return Armature(
        nodes=[ArmatureNode(name=f"N{i}", at=(float(i), 0.0, 0.0)) for i in range(count)],
        bones=[Bone(i, i + 1) for i in range(count - 1)],
    )


# -- the graph ----------------------------------------------------------


def test_dissolving_a_node_bridges_the_two_it_joined():
    nodes, bones = _chain().dissolved(1)
    assert [node.name for node in nodes] == ["N0", "N2", "N3"]
    assert {frozenset(bone.ends) for bone in bones} == {frozenset({0, 1}), frozenset({1, 2})}


def test_dissolving_an_end_just_removes_it():
    """Nothing stands between one neighbour, so there is nothing to bridge."""
    nodes, bones = _chain().dissolved(0)
    assert [node.name for node in nodes] == ["N1", "N2", "N3"]
    assert {frozenset(bone.ends) for bone in bones} == {frozenset({0, 1}), frozenset({1, 2})}


def test_deleting_a_node_reindexes_the_bones_that_outlived_it():
    armature = _chain(5)
    nodes, bones = armature.without_node(1)
    assert len(nodes) == 4
    # N2-N3 and N3-N4 were indices 2-3 and 3-4; everything above 1 shifts down.
    assert {frozenset(bone.ends) for bone in bones} == {frozenset({1, 2}), frozenset({2, 3})}
    for bone in bones:
        assert 0 <= bone.a < len(nodes) and 0 <= bone.b < len(nodes)


def test_a_bone_never_joins_a_node_to_itself():
    armature = _chain()
    assert armature.with_bone(2, 2)[1] == armature.bones


def test_a_bone_is_never_laid_twice_between_the_same_pair():
    armature = _chain()
    assert armature.with_bone(1, 0)[1] == armature.bones


def test_a_new_node_is_joined_to_the_one_it_was_drawn_from():
    nodes, bones = _chain(2).with_node(ArmatureNode(name="tip", at=(9.0, 0.0, 0.0)), connect_to=1)
    assert nodes[-1].name == "tip"
    assert frozenset(bones[-1].ends) == frozenset({1, 2})


def test_a_hand_placed_node_starts_at_a_plausible_thickness():
    armature = _chain()
    assert armature.longest_bone() == pytest.approx(1.0)
    assert 0.0 < armature.default_size() < 1.0


# -- the median plane ---------------------------------------------------


def test_the_median_plane_is_fitted_from_the_centre_landmarks():
    plane = median_plane(list(_CENTRE.values()))
    assert plane is not None
    origin, normal = plane
    assert abs(float(np.dot(normal, [1.0, 0.0, 0.0]))) == pytest.approx(1.0, abs=1e-9)
    assert origin[0] == pytest.approx(0.0)


def test_a_collinear_centre_line_refuses_to_fit_a_plane():
    """Every plane through a straight line is as good as every other."""
    assert median_plane([(0.0, y, 0.0) for y in (0.0, 10.0, 20.0, 30.0)]) is None


def test_mirroring_puts_the_right_side_where_the_left_side_is():
    origin, normal = median_plane(list(_CENTRE.values()))
    mirrored = mirror_point(_LEFT["acromion"], origin, normal)
    assert mirrored == pytest.approx([-20.0, 148.0, 0.0])


def test_the_mirror_fills_in_the_side_the_artist_did_not_place():
    armature = Armature(preset="humanoid")
    armature.landmarks = [PlacedLandmark(key=key, at=at) for key, at in _CENTRE.items()]
    armature.landmarks += [
        PlacedLandmark(key=f"{key}.L", at=at) for key, at in _LEFT.items()
    ]
    armature.landmarks = mirror_landmarks(armature)

    right = {entry.key: entry for entry in armature.landmarks if entry.key.endswith(".R")}
    assert len(right) == len(_LEFT)
    assert all(entry.mirrored for entry in right.values())
    assert right["acromion.R"].at == pytest.approx((-20.0, 148.0, 0.0))


def test_the_mirror_leaves_a_corrected_point_where_the_artist_put_it():
    armature = Armature(preset="humanoid")
    armature.landmarks = [PlacedLandmark(key=key, at=at) for key, at in _CENTRE.items()]
    armature.landmarks += [PlacedLandmark(key=f"{key}.L", at=at) for key, at in _LEFT.items()]
    armature.landmarks = mirror_landmarks(armature)

    corrected = next(e for e in armature.landmarks if e.key == "acromion.R")
    corrected.at = (-19.0, 147.0, 1.0)
    corrected.mirrored = False

    armature.landmarks = mirror_landmarks(armature)
    again = next(e for e in armature.landmarks if e.key == "acromion.R")
    assert again.at == pytest.approx((-19.0, 147.0, 1.0))


# -- the humanoid preset ------------------------------------------------


def test_the_humanoid_preset_asks_for_every_landmark_once():
    keys = [entry.key for entry in HUMANOID_LANDMARKS]
    assert len(keys) == len(set(keys))
    assert HUMANOID.landmark("acromion.R").mirror_of == "acromion.L"


def test_mirroring_roughly_halves_what_the_artist_is_asked_for():
    with_mirror = HUMANOID.steps(mirror=True, optional=False)
    without = HUMANOID.steps(mirror=False, optional=False)
    assert len(with_mirror) == 19
    assert len(without) == 33
    assert not any(entry.mirror_of for entry in with_mirror)


def test_the_knee_sits_between_the_two_epicondyles():
    roles = _roles(build_humanoid(_figure())[0])
    assert roles["knee.L"].at == pytest.approx((11.0, 55.0, 0.0))


def test_the_humanoid_preset_infers_the_hip_medial_to_the_trochanter():
    """The femoral head is inside the bump you can feel, not on it."""
    roles = _roles(build_humanoid(_figure())[0])
    hip, pelvis = roles["hip.L"].point, roles["pelvis"].point
    trochanter = np.array(_LEFT["greater_trochanter"])

    assert hip[0] < trochanter[0]  # medial
    assert hip[1] > trochanter[1]  # and a little higher
    assert np.linalg.norm(hip - pelvis) < np.linalg.norm(trochanter - pelvis)
    assert roles["hip.R"].at[0] == pytest.approx(-roles["hip.L"].at[0])


def test_the_shoulder_sits_below_and_inside_the_acromion():
    roles = _roles(build_humanoid(_figure())[0])
    shoulder = roles["shoulder.L"].point
    acromion = np.array(_LEFT["acromion"])
    assert shoulder[0] < acromion[0]
    assert shoulder[1] < acromion[1]


def test_the_spine_is_carried_forward_off_the_back_landmark():
    roles = _roles(build_humanoid(_figure())[0])
    assert roles["spine"].at[2] > _CENTRE["t12"][2]


def test_the_wrist_is_sized_from_the_span_of_its_styloids():
    roles = _roles(build_humanoid(_figure())[0])
    span = np.linalg.norm(np.subtract(_LEFT["radial_styloid"], _LEFT["ulnar_styloid"]))
    assert roles["wrist.L"].size == pytest.approx(span * 0.5)
    assert roles["elbow.L"].size > roles["wrist.L"].size


def test_a_bigger_figure_gets_bigger_joints():
    small = _roles(build_humanoid(_figure())[0])
    large = _roles(build_humanoid(_figure(scale=2.0))[0])
    for role in ("elbow.L", "knee.L", "pelvis", "ankle.R"):
        assert large[role].size == pytest.approx(small[role].size * 2.0)


def test_every_joint_comes_out_with_a_thickness():
    for node in build_humanoid(_figure())[0]:
        assert node.size > 0.0, node.role


def test_the_armature_hangs_together_as_one_piece():
    """A wire in two halves is not an armature anybody could bend."""
    nodes, bones = build_humanoid(_figure())
    seen, queue = {0}, [0]
    while queue:
        current = queue.pop()
        for bone in bones:
            if not bone.touches(current):
                continue
            other = bone.other(current)
            if other not in seen:
                seen.add(other)
                queue.append(other)
    assert len(seen) == len(nodes)


def test_a_half_finished_preset_still_builds_what_it_can():
    placed = _figure()
    torso = {k: v for k, v in placed.items() if "malleolus" not in k and "metatarsal" not in k}
    nodes, bones = build_humanoid(torso)
    roles = _roles(nodes)
    assert "knee.L" in roles
    assert "ankle.L" not in roles
    for bone in bones:
        assert 0 <= bone.a < len(nodes) and 0 <= bone.b < len(nodes)


def test_placing_nothing_builds_nothing():
    assert build_humanoid({}) == ([], [])


def test_the_optional_landmarks_add_the_nodes_they_describe():
    placed = _figure()
    placed["calcaneal_tuberosity.L"] = np.array([10.0, 6.0, -8.0])
    roles = _roles(build_humanoid(placed)[0])
    assert "heel.L" in roles
    assert "heel.R" not in roles


# -- re-deriving --------------------------------------------------------


def _derived() -> Armature:
    placed = _figure()
    armature = Armature(preset="humanoid", derived=True)
    armature.landmarks = [
        PlacedLandmark(key=key, at=tuple(float(v) for v in at)) for key, at in placed.items()
    ]
    armature.nodes, armature.bones = build_humanoid(placed)
    return armature


def test_re_deriving_keeps_a_renamed_node_named():
    armature = _derived()
    armature.node_for_role("pelvis").name = "Hips"
    armature.nodes, armature.bones = rebuild(armature)
    assert armature.node_for_role("pelvis").name == "Hips"


def test_moving_a_landmark_moves_the_nodes_that_read_it():
    armature = _derived()
    before = armature.node_for_role("pelvis").point.copy()
    armature.landmark_for("asis.L").at = (10.0, 120.0, 8.0)
    armature.nodes, armature.bones = rebuild(armature)
    assert armature.node_for_role("pelvis").point[1] > before[1]


# -- editing a placed landmark ------------------------------------------


def test_moving_a_landmark_from_the_list_takes_it_off_the_mirror():
    """A guess the artist corrects is theirs, and the mirror leaves it alone."""
    armature = _derived()
    armature.landmark_for("asis.R").mirrored = True

    landmarks = armature.with_landmark_at("asis.R", (-11.0, 101.0, 9.0))
    moved = next(entry for entry in landmarks if entry.key == "asis.R")
    assert moved.at == pytest.approx((-11.0, 101.0, 9.0))
    assert moved.mirrored is False


def test_editing_a_landmark_leaves_the_document_list_alone():
    """The new list is the edit; the old one has to survive to be undone to."""
    armature = _derived()
    before = armature.landmark_for("asis.L").at

    armature.with_landmark_at("asis.L", (10.0, 120.0, 8.0))

    assert armature.landmark_for("asis.L").at == pytest.approx(before)


def test_deriving_from_an_edited_landmark_rebuilds_the_wire():
    armature = _derived()
    tool, settings = ArmatureTool(), ArmatureSettings()
    before = armature.node_for_role("pelvis").point.copy()

    nodes, bones, landmarks = tool.derive(
        armature, armature.with_landmark_at("asis.L", (10.0, 120.0, 8.0)), settings
    )

    rebuilt = {node.role: node for node in nodes}["pelvis"]
    assert rebuilt.point[1] > before[1]
    assert bones
    # The armature itself is untouched until the command runs.
    assert armature.node_for_role("pelvis").point == pytest.approx(before)
    assert len(landmarks) == len(armature.landmarks)


def test_deriving_never_writes_through_the_landmarks_it_is_handed():
    """Mirroring moves a guess in place, which must not reach the undo history."""
    armature = _derived()
    armature.landmark_for("asis.R").mirrored = True
    kept = armature.landmark_for("asis.R").at

    tool = ArmatureTool()
    tool.derive(
        armature,
        armature.with_landmark_at("asis.L", (10.0, 120.0, 8.0)),
        ArmatureSettings(mirror=True),
    )

    assert armature.landmark_for("asis.R").at == pytest.approx(kept)


def test_dropping_a_landmark_can_take_its_reflection_with_it():
    armature = _derived()
    landmarks = armature.without_landmarks("asis.L", "asis.R")
    assert {entry.key for entry in landmarks}.isdisjoint({"asis.L", "asis.R"})
    assert len(landmarks) == len(armature.landmarks) - 2


def test_a_locked_node_keeps_the_size_it_was_given():
    armature = _derived()
    kept = armature.node_for_role("elbow.L")
    kept.locked, kept.size, kept.at = True, 99.0, (1.0, 2.0, 3.0)
    loose = armature.node_for_role("elbow.R")
    loose.size = 99.0

    armature.nodes, armature.bones = rebuild(armature)
    assert armature.node_for_role("elbow.L").size == pytest.approx(99.0)
    assert armature.node_for_role("elbow.L").at == pytest.approx((1.0, 2.0, 3.0))
    assert armature.node_for_role("elbow.R").size != pytest.approx(99.0)


def test_a_freehand_armature_has_no_preset_to_rebuild_from():
    assert rebuild(_chain()) is None


# -- persistence --------------------------------------------------------


def test_an_armature_survives_a_session_round_trip(tmp_path):
    armature = _derived()
    armature.name = "Figure"
    store = ArmatureStore([armature])
    path = Session(armatures=list(store)).save(tmp_path / "figure.refview.json")

    loaded = Session.load(path).armatures[0]
    assert loaded.name == "Figure"
    assert loaded.preset == "humanoid"
    assert loaded.derived is True
    assert len(loaded.nodes) == len(armature.nodes)
    assert len(loaded.landmarks) == len(armature.landmarks)
    assert isinstance(loaded.bones[0], Bone)
    assert loaded.node_for_role("pelvis").at == pytest.approx(
        armature.node_for_role("pelvis").at
    )
    assert loaded.node_for_role("elbow.L").size == pytest.approx(
        armature.node_for_role("elbow.L").size
    )


def test_a_session_from_before_the_armature_still_loads(tmp_path):
    """Version 4 files predate the armature; they open with an empty one."""
    path = tmp_path / "old.refview.json"
    path.write_text('{"version": 4, "mesh_path": "bust.obj"}', encoding="utf-8")
    session = Session.load(path)
    assert session.armatures == []
    assert session.armature_settings.show_all is True


# -- the guided walk ----------------------------------------------------
#
# ArmatureTool lives under ui/ but imports no Qt, so the order it asks for
# landmarks in can be pinned here with everything else.


def _run(mirror: bool = True) -> tuple[ArmatureTool, Armature, ArmatureSettings]:
    tool = ArmatureTool()
    armature = Armature(preset="humanoid", derived=True)
    tool.start_guide("humanoid", armature=0)
    return tool, armature, ArmatureSettings(mirror=mirror)


def _walk(tool, armature, settings, placed) -> int:
    """Place every landmark the run asks for; returns how many were asked."""
    asked = 0
    while (entry := tool.current(armature, settings)) is not None:
        at = placed.get(entry.key)
        if at is None:
            tool.skip(armature, settings)
            continue
        armature.nodes, armature.bones, armature.landmarks = tool.place(armature, at, settings)
        asked += 1
    return asked


def test_a_guided_run_asks_for_the_midline_first():
    tool, armature, settings = _run()
    assert tool.current(armature, settings).key == "vertex"
    assert [e.key for e in tool.remaining(armature, settings)[:5]] == list(_CENTRE)


def test_mirroring_means_the_run_never_asks_for_the_right_side():
    tool, armature, settings = _run(mirror=True)
    assert all(not e.mirror_of for e in tool.remaining(armature, settings))
    assert _walk(tool, armature, settings, _figure()) == 19


def test_without_mirroring_the_run_asks_for_both_sides():
    tool, armature, settings = _run(mirror=False)
    assert _walk(tool, armature, settings, _figure()) == 33


def test_a_guided_run_builds_the_same_figure_the_preset_would():
    tool, armature, settings = _run()
    _walk(tool, armature, settings, _figure())
    assert {n.role for n in armature.nodes} == {n.role for n in build_humanoid(_figure())[0]}
    assert all(node.size > 0.0 for node in armature.nodes)


def test_the_mirrored_half_is_marked_as_a_guess():
    tool, armature, settings = _run()
    _walk(tool, armature, settings, _figure())
    mirrored = [entry for entry in armature.landmarks if entry.mirrored]
    assert len(mirrored) == 14
    assert all(entry.key.endswith(".R") for entry in mirrored)


def test_a_skipped_landmark_is_not_asked_for_again():
    tool, armature, settings = _run()
    tool.skip(armature, settings)
    assert tool.current(armature, settings).key == "c7"
    # 5 midline plus 18 unmirrored pairs, less the one just passed over.
    assert tool.progress(armature, settings) == (0, 22)


def test_going_back_hands_the_last_landmark_over_to_be_placed_again():
    tool, armature, settings = _run()
    placed = _figure()
    for key in ("vertex", "c7"):
        armature.nodes, armature.bones, armature.landmarks = tool.place(
            armature, placed[key], settings
        )
    assert tool.current(armature, settings).key == "jugular_notch"
    assert tool.back(armature, settings) == "c7"


def test_going_back_over_a_skip_un_skips_it():
    tool, armature, settings = _run()
    armature.nodes, armature.bones, armature.landmarks = tool.place(
        armature, _figure()["vertex"], settings
    )
    tool.skip(armature, settings)
    assert tool.current(armature, settings).key == "jugular_notch"
    assert tool.back(armature, settings) == "c7"
    assert tool.current(armature, settings).key == "c7"


def test_progress_counts_what_will_actually_be_asked_for():
    tool, armature, settings = _run()
    assert tool.progress(armature, settings) == (0, 23)
    _walk(tool, armature, settings, _figure())
    placed, wanted = tool.progress(armature, settings)
    assert placed == wanted == 19


# -- inserting into a bone ----------------------------------------------


def test_inserting_into_a_bone_lengthens_the_chain_rather_than_branching():
    armature = _chain(3)
    nodes, bones = armature.split_bone(0, ArmatureNode(name="mid", at=(0.5, 0.0, 0.0)))
    assert [node.name for node in nodes] == ["N0", "N1", "N2", "mid"]
    assert {frozenset(bone.ends) for bone in bones} == {
        frozenset({1, 2}),
        frozenset({0, 3}),
        frozenset({3, 1}),
    }


def test_a_node_inserted_into_a_bone_has_no_loose_ends():
    armature = _chain(2)
    nodes, bones = armature.split_bone(0, ArmatureNode(at=(0.5, 0.0, 0.0)))
    for bone in bones:
        assert 0 <= bone.a < len(nodes) and 0 <= bone.b < len(nodes)
    inserted = len(nodes) - 1
    assert sorted(Armature(nodes=nodes, bones=bones).neighbours(inserted)) == [0, 1]


def test_splitting_a_bone_that_is_not_there_changes_nothing():
    armature = _chain(3)
    assert armature.split_bone(9, ArmatureNode()) == (armature.nodes, armature.bones)


# -- taking hold of a landmark in the view --------------------------------
#
# A landmark is an answer the artist can get wrong, and the wire is derived
# from it, so correcting it by dragging the node it produced would throw the
# preset away to fix something the preset could have rebuilt itself.


def _view(width: int = 800, height: int = 600) -> SurfacePicker:
    """A camera looking at the test figure from the front, and no mesh.

    No mesh on purpose: picking a landmark is a question about where its cross
    landed on screen, not about what the ray hits out there.
    """
    camera = Camera()
    camera.scene_center = np.array([0.0, 95.0, 0.0])
    camera.scene_radius = 110.0
    camera.target = camera.scene_center.copy()
    camera.eye = camera.scene_center + np.array([0.0, 0.0, 400.0])
    return SurfacePicker(camera=camera, mesh=None, width=width, height=height)


def _at(picker: SurfacePicker, point) -> tuple[float, float]:
    """Where a world point lands, in widget pixels."""
    x, y, _ = picker.camera.project(point, picker.width, picker.height)
    return float(x), float(y)


def test_a_landmark_is_grabbable_where_its_cross_is():
    armature = _derived()
    picker, settings = _view(), ArmatureSettings()
    x, y = _at(picker, armature.landmark_for("asis.L").point)

    found = ArmatureTool().landmark_at(x, y, [armature], picker, settings)

    assert found == (0, "asis.L")


def test_the_cursor_has_to_be_on_the_cross_to_find_it():
    armature = _derived()
    picker, settings = _view(), ArmatureSettings()
    x, y = _at(picker, armature.landmark_for("asis.L").point)

    assert ArmatureTool().landmark_at(x + 40.0, y, [armature], picker, settings) is None


def test_a_node_beside_a_landmark_still_has_the_wider_reach():
    """Which is what settles the two when they overlap, as half a preset does.

    Inside the cross's reach the landmark answers; a little outside it the node
    does, rather than neither of them.
    """
    tool = ArmatureTool()
    armature = _derived()
    picker, settings = _view(), ArmatureSettings()
    mark = armature.landmark_for("asis.L").point
    armature.nodes.append(ArmatureNode(name="Beside it", at=tuple(mark)))
    x, y = _at(picker, mark)
    just_off = tool.LANDMARK_REACH + 2.0

    assert tool.landmark_at(x, y, [armature], picker, settings) == (0, "asis.L")
    assert tool.landmark_at(x + just_off, y, [armature], picker, settings) is None
    assert tool.handle_at(x + just_off, y, [armature], picker, settings) is not None


def test_hiding_the_crosses_makes_them_inert():
    """Nothing invisible should move when the cursor crosses it."""
    armature = _derived()
    picker = _view()
    x, y = _at(picker, armature.landmark_for("asis.L").point)

    hidden = ArmatureSettings(show_landmarks=False)
    assert ArmatureTool().landmark_at(x, y, [armature], picker, hidden) is None
    packed = ArmatureSettings(show_all=False)
    assert ArmatureTool().landmark_at(x, y, [armature], picker, packed) is None


def test_a_hidden_armature_offers_no_landmark_to_grab():
    armature = _derived()
    armature.visible = False
    picker, settings = _view(), ArmatureSettings()
    x, y = _at(picker, armature.landmark_for("asis.L").point)

    assert ArmatureTool().landmark_at(x, y, [armature], picker, settings) is None


def test_a_mirrored_guess_can_be_taken_hold_of():
    """Grabbing one is how the artist says the guess was wrong."""
    armature = _derived()
    armature.landmark_for("asis.R").mirrored = True
    picker, settings = _view(), ArmatureSettings()
    x, y = _at(picker, armature.landmark_for("asis.R").point)

    assert ArmatureTool().landmark_at(x, y, [armature], picker, settings) == (0, "asis.R")


def test_a_landmark_behind_the_camera_is_not_grabbable():
    """It projects somewhere on screen regardless, which is not where it is."""
    picker, settings = _view(), ArmatureSettings()
    behind = picker.camera.eye + np.array([0.0, 0.0, 50.0])
    armature = Armature(landmarks=[PlacedLandmark(key="behind", at=tuple(behind))])
    x, y = _at(picker, behind)

    assert ArmatureTool().landmark_at(x, y, [armature], picker, settings) is None


def test_the_nearest_cross_wins_when_two_overlap():
    armature = _derived()
    picker, settings = _view(), ArmatureSettings()
    near = armature.landmark_for("asis.L").point
    x, y = _at(picker, near)
    # A second cross a few pixels along, so both are within reach of one point
    # between them but one of them is nearer to it.
    beside = tuple(near + np.array([1.5, 0.0, 0.0]))
    armature.landmarks.append(PlacedLandmark(key="nudged", at=beside))
    other_x, other_y = _at(picker, armature.landmark_for("nudged").point)
    assert abs(other_x - x) < ArmatureTool().LANDMARK_REACH

    assert ArmatureTool().landmark_at(x, y, [armature], picker, settings) == (0, "asis.L")
    found = ArmatureTool().landmark_at(other_x, other_y, [armature], picker, settings)
    assert found == (0, "nudged")


def test_the_drag_a_landmark_makes_is_the_edit_the_panel_would_make():
    """Which is what keeps a dragged cross and a typed position one behaviour.

    The viewport applies ``with_landmark_at`` and then ``derive``, exactly as
    the position boxes do, so the wire bends live and the whole drag lands in
    the history as one step.
    """
    tool = ArmatureTool()
    armature = _derived()
    settings = ArmatureSettings()
    before = armature.node_for_role("pelvis").point.copy()

    moved = armature.with_landmark_at("asis.L", (10.0, 120.0, 8.0))
    nodes, bones, landmarks = tool.derive(armature, moved, settings)

    assert armature.landmark_for("asis.L").at == pytest.approx((10.0, 100.0, 8.0))
    armature.nodes, armature.bones, armature.landmarks = nodes, bones, landmarks
    assert armature.node_for_role("pelvis").point[1] > before[1]
