"""The Forms panel: the guided run it drives, and the document it writes.

The geometry is covered in test_forms; what is worth asserting here is the
plumbing between the panel, the tool and the document -- that Start makes a
form and arms the tool, that a placed landmark is one undo step, that Back
and Delete write through the history, and that the stage slider speaks for
the form being guided.
"""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.armature import PlacedLandmark
from refview.core.forms import (
    FREEFORM,
    HEAD,
    FormFill,
    PrimaryForm,
    build_form,
    built_count,
    form_landmark_title,
)
from refview.core.landmarks import Side
from refview.core.mesh import Mesh
from refview.core.orientation import OrientationSettings, UpAxis

QtCore = pytest.importorskip("PySide6.QtCore")
QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from refview.ui.form_tool import FormTool  # noqa: E402 - needs Qt first
from refview.ui.panels.forms_panel import FormsPanel  # noqa: E402 - needs Qt first
from refview.ui.state import ViewerState  # noqa: E402 - needs Qt first
from test_forms import HEAD_MARKS, PELVIS_MARKS  # noqa: E402 - needs Qt first


@pytest.fixture(scope="session")
def app():
    """One offscreen Qt application for the run; see test_film_recorder."""
    import os

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    existing = QtWidgets.QApplication.instance()
    yield existing or QtWidgets.QApplication([])


@pytest.fixture
def panel(app):
    state = ViewerState()
    panel = FormsPanel(state)
    tool = FormTool()
    panel.attach(tool)
    state.forms_changed.connect(panel.refresh_list)  # as the main window wires it
    return panel


def _pick(panel: FormsPanel, key: str) -> None:
    index = panel._preset.findData(key)
    assert index >= 0
    panel._preset.setCurrentIndex(index)


def _place_all(panel: FormsPanel, marks: dict) -> None:
    state, tool = panel.state, panel._tool
    form = state.forms[tool.guide.form]
    settings = state.form_settings
    while (entry := tool.current(form, settings)) is not None:
        landmarks = tool.place(form, marks[entry.key], settings)
        panel.apply_edit((tool.guide.form, landmarks, "Place landmark"))


def test_start_makes_a_form_and_arms_the_tool(panel):
    armed = []
    panel.form_toggled.connect(armed.append)
    _pick(panel, "pelvis")
    panel.start_guide()
    assert len(panel.state.forms) == 1
    assert panel.state.forms[0].preset == "pelvis"
    assert panel.state.forms[0].name == "Pelvis"
    assert panel._tool.guiding and panel._tool.guide.form == 0
    assert armed == [True]
    assert panel.state.history.can_undo  # adding the form is a step


def test_each_placed_landmark_is_one_undo_step_and_the_form_builds(panel):
    _pick(panel, "pelvis")
    panel.start_guide()
    steps = len(panel.state.history._undo)
    _place_all(panel, PELVIS_MARKS)
    form = panel.state.forms[0]
    placed = len(panel.state.history._undo) - steps
    assert placed == sum(1 for entry in form.landmarks if not entry.mirrored)
    assert built_count(build_form(form)) == 1
    panel.state.undo()  # the sitting bones, which are optional ...
    assert built_count(build_form(form)) == 1
    panel.state.undo()  # ... and the PSIS, which are not
    assert built_count(build_form(form)) == 0
    panel.state.redo()
    panel.state.redo()
    assert built_count(build_form(form)) == 1


def test_back_takes_a_landmark_off_through_the_history(panel):
    _pick(panel, "head")
    panel.start_guide()
    form = panel.state.forms[0]
    tool, settings = panel._tool, panel.state.form_settings
    first = tool.current(form, settings)
    panel.apply_edit((0, tool.place(form, HEAD_MARKS[first.key], settings), "Place landmark"))
    assert form.landmark_for(first.key) is not None
    panel._back_landmark()
    assert form.landmark_for(first.key) is None
    assert tool.current(form, settings).key == first.key
    panel.state.undo()
    assert form.landmark_for(first.key) is not None


def test_the_stage_slider_speaks_for_the_guided_form(panel):
    _pick(panel, "head")
    panel.start_guide()
    form = panel.state.forms[0]
    assert panel._stage_box.isVisibleTo(panel)
    assert panel._stage.maximum() == len(HEAD.stages) - 1
    assert panel._stage.value() == len(HEAD.stages) - 1  # the open end
    panel._stage.setValue(1)
    assert form.stage == 1
    panel._stage.setValue(len(HEAD.stages) - 1)
    assert form.stage == -1


def test_a_one_stage_form_hides_the_slider(panel):
    _pick(panel, "pelvis")
    panel.start_guide()
    assert not panel._stage_box.isVisibleTo(panel)


def test_finish_ends_the_run_and_the_form_stays(panel):
    _pick(panel, "ribcage")
    panel.start_guide()
    panel.end_guide()
    assert not panel._tool.guiding
    assert len(panel.state.forms) == 1


def test_deleting_a_landmark_takes_its_mirrored_guess_with_it(panel):
    _pick(panel, "pelvis")
    panel.start_guide()
    _place_all(panel, PELVIS_MARKS)
    panel.end_guide()
    form = panel.state.forms[0]
    assert form.landmark_for("asis.R").mirrored
    panel.select_landmark((0, "asis.L"))
    panel._delete_selected()
    assert form.landmark_for("asis.L") is None
    assert form.landmark_for("asis.R") is None
    panel.state.undo()
    assert form.landmark_for("asis.R") is not None


def test_clear_all_ends_the_run_and_undoes_as_one_step(panel):
    _pick(panel, "pelvis")
    panel.start_guide()
    panel.clear_all()
    assert not panel._tool.guiding
    assert len(panel.state.forms) == 0
    panel.state.undo()
    assert len(panel.state.forms) == 1


def test_the_list_shows_forms_and_their_landmarks_in_preset_order(panel):
    panel.state.forms.add(
        PrimaryForm(
            name="Head",
            preset="head",
            landmarks=[
                PlacedLandmark(key="menton", at=tuple(HEAD_MARKS["menton"])),
                PlacedLandmark(key="vertex", at=tuple(HEAD_MARKS["vertex"])),
            ],
        )
    )
    panel.refresh_list()
    top = panel._tree.topLevelItem(0)
    assert top.text(0) == "Head"
    assert [top.child(i).text(0) for i in range(top.childCount())] == ["Vertex", "Chin"]


def test_ghosting_from_the_forms_panel_writes_the_render_setting(panel):
    panel._ghost.setChecked(True)
    assert panel.state.render.ghost is True
    panel._ghost.setChecked(False)
    assert panel.state.render.ghost is False


def test_settings_write_through(panel):
    panel._smooth.set_value(10.0)
    panel._smooth.valueCommitted.emit(10.0)
    assert panel.state.form_settings.smooth == 10.0
    panel._show_all.setChecked(False)
    assert panel.state.form_settings.show_all is False
    panel._mirror.setChecked(False)
    assert panel.state.form_settings.mirror is False
    panel._symmetric.setChecked(False)
    assert panel.state.form_settings.symmetric is False


def test_forms_turn_with_the_model(app):
    state = ViewerState()
    triangle = Mesh(
        np.array([[0, 0, 0], [2, 0, 0], [0, 2, 0]], dtype=np.float32),
        np.array([[0, 0, 1]] * 3, dtype=np.float32),
        np.array([[0, 1, 2]], dtype=np.uint32),
    )
    state.source_mesh = triangle
    state.mesh = state._oriented(triangle)
    state.forms.add(
        PrimaryForm(preset="pelvis", landmarks=[PlacedLandmark(key="asis.L", at=(1.0, 2.0, 3.0))])
    )
    corner = np.asarray(state.mesh.positions[1], dtype=np.float64)
    before = np.array(state.forms[0].landmarks[0].at) - corner
    state.set_orientation(OrientationSettings(up_axis=UpAxis.Z))
    corner = np.asarray(state.mesh.positions[1], dtype=np.float64)
    after = np.array(state.forms[0].landmarks[0].at) - corner
    # The landmark rode round with the model: same distance from the same
    # corner of it, in a different direction.
    assert np.linalg.norm(after) == pytest.approx(np.linalg.norm(before), rel=1e-6)
    assert not np.allclose(before, after)


def test_selecting_a_form_row_enables_the_buttons_and_does_not_raise(panel):
    """A form row hands the whole form to update_enabled, whose landmark
    list must be read as a bool, not handed to Qt as one."""
    _pick(panel, "pelvis")
    panel.start_guide()
    _place_all(panel, PELVIS_MARKS)
    panel.end_guide()
    panel._tree.setCurrentItem(panel._tree.topLevelItem(0))
    panel.update_enabled()
    assert panel._delete.isEnabled() and panel._center.isEnabled()
    # An empty form's row offers Delete but nothing to centre on.
    panel.state.forms.add(PrimaryForm(name="Head", preset="head"))
    panel.refresh_list()
    panel._tree.setCurrentItem(panel._tree.topLevelItem(1))
    panel.update_enabled()
    assert panel._delete.isEnabled() and not panel._center.isEnabled()


# -- the freeform ---------------------------------------------------------------


def _pending(panel: FormsPanel, name: str, side: str | None = None) -> None:
    """Type a name for the next landmark and, if given, pick its side."""
    panel._point_name.setText(name)
    panel._point_name.textEdited.emit(name)
    if side is not None:
        panel._point_side.setCurrentIndex(panel._point_side.findData(side))


def _click(panel: FormsPanel, at: tuple) -> None:
    """What the viewport does when a freeform run gets a click."""
    tool, state = panel._tool, panel.state
    form = state.forms[tool.guide.form]
    landmarks = tool.place(form, np.array(at, dtype=np.float64), state.form_settings)
    panel.apply_edit((tool.guide.form, landmarks, "Place landmark"))


def test_a_freeform_is_named_and_started_from_the_panel(panel):
    _pick(panel, FREEFORM)
    panel.update_enabled()
    assert panel._guide_form.isRowVisible(panel._form_name)
    assert panel._guide_form.isRowVisible(panel._fill)
    panel._form_name.setText("Left hand")
    panel._fill.setCurrentIndex(panel._fill.findData(FormFill.SMOOTH.value))
    panel.start_guide()
    form = panel.state.forms[0]
    assert form.name == "Left hand" and form.freeform and form.fill is FormFill.SMOOTH
    assert panel._tool.guiding and panel._tool.guide.freeform
    # The run asks for nothing: the panel offers a name and a side instead.
    assert panel._guide_form.isRowVisible(panel._point_name)
    assert panel._guide_form.isRowVisible(panel._point_side)
    assert not panel._guide_form.isRowVisible(panel._prompt)
    assert not panel._skip.isVisibleTo(panel)
    assert panel._point_name.text() == "Point 1"
    assert panel._tool.guide.pending.key == "point_1"
    assert panel._form_name.text() == ""
    # A blank name is numbered like the presets'.
    panel.end_guide()
    panel.start_guide()
    assert panel.state.forms[1].name == "Form"


def test_each_click_lays_the_pending_landmark_down_and_the_side_carries_over(panel):
    _pick(panel, FREEFORM)
    panel.start_guide()
    form = panel.state.forms[0]
    steps = len(panel.state.history._undo)
    _pending(panel, "Wrist")
    _click(panel, (20, 80, 0))
    assert [entry.key for entry in form.points] == ["wrist"]
    assert form.point_for("wrist").side is Side.CENTRE
    assert form.landmark_for("wrist").at == (20.0, 80.0, 0.0)
    # The next one is numbered and readied, on the same side.
    assert panel._point_name.text() == "Point 2"
    _pending(panel, "Thumb", Side.LEFT.value)
    _click(panel, (24, 76, 4))
    assert form.point_for("thumb.L").side is Side.LEFT
    # Left stays left until it is changed.
    assert panel._point_side.currentData() == Side.LEFT.value
    _click(panel, (16, 70, -1))
    assert form.points[-1].key == "point_3.L" and form.points[-1].side is Side.LEFT
    _click(panel, (21, 72, 2))
    assert built_count(build_form(form)) == 1
    # One undo step a landmark, and undo takes the point off the list too.
    assert len(panel.state.history._undo) - steps == 4
    panel.state.undo()
    assert len(form.points) == 3 and form.landmark_for("point_4.L") is None
    panel.state.redo()
    assert len(form.points) == 4
    assert panel._tool.progress(form, panel.state.form_settings) == (4, 4)


def test_a_freeform_mirrors_a_side_once_the_midline_gives_a_plane(panel):
    _pick(panel, FREEFORM)
    panel.start_guide()
    form = panel.state.forms[0]
    for name, at in (("Notch", (0, 148, 6)), ("Xiphoid", (0, 128, 9)), ("C7", (0, 152, -7))):
        _pending(panel, name)
        _click(panel, at)
    _pending(panel, "Nipple", Side.LEFT.value)
    _click(panel, (10, 135, 8))
    guess = form.landmark_for("nipple.R")
    assert guess is not None and guess.mirrored
    assert np.allclose(guess.point, (-10, 135, 8), atol=1e-6)
    # The guess is listed under the form, named for its source, and is not
    # one of the artist's own points.
    assert form.point_for("nipple.R") is None
    top = panel._tree.topLevelItem(0)
    titles = [top.child(i).text(0) for i in range(top.childCount())]
    assert "Nipple (left)" in titles and "Nipple (right)" in titles
    # Placing the right by hand makes it the artist's, and a pair.
    _pending(panel, "Nipple", Side.RIGHT.value)
    assert panel._tool.guide.pending.key == "nipple.R"
    _click(panel, (-11, 135, 8))
    assert form.point_for("nipple.R") is not None
    assert not form.landmark_for("nipple.R").mirrored


def test_back_takes_a_freeform_point_off_with_its_guess(panel):
    _pick(panel, FREEFORM)
    panel.start_guide()
    form = panel.state.forms[0]
    for name, at in (("Notch", (0, 148, 6)), ("Xiphoid", (0, 128, 9)), ("C7", (0, 152, -7))):
        _pending(panel, name)
        _click(panel, at)
    _pending(panel, "Nipple", Side.LEFT.value)
    _click(panel, (10, 135, 8))
    assert form.landmark_for("nipple.R") is not None
    panel._back_landmark()
    assert form.point_for("nipple.L") is None
    assert form.landmark_for("nipple.L") is None and form.landmark_for("nipple.R") is None
    assert len(form.points) == 3
    panel.state.undo()
    assert form.point_for("nipple.L") is not None and form.landmark_for("nipple.R") is not None
    # Delete does the same for a chosen row, guess and all.
    panel.refresh_list()
    panel.select_landmark((0, "nipple.L"))
    panel._delete_selected()
    assert form.point_for("nipple.L") is None and form.landmark_for("nipple.R") is None


def test_a_freeform_landmark_can_be_renamed_in_the_list(panel):
    _pick(panel, FREEFORM)
    panel.start_guide()
    form = panel.state.forms[0]
    _pending(panel, "Wrist", Side.LEFT.value)
    _click(panel, (20, 80, 0))
    panel.end_guide()
    row = panel._tree.topLevelItem(0).child(0)
    assert row.text(0) == "Wrist (left)"
    assert row.flags() & QtCore.Qt.ItemFlag.ItemIsEditable
    row.setText(0, "Radial styloid (left)")
    QtCore.QCoreApplication.processEvents()  # the rename commits after the signal
    assert form.point_for("wrist.L").name == "Radial styloid"
    assert form_landmark_title(form, "wrist.L") == "Radial styloid (left)"
    assert panel._tree.topLevelItem(0).child(0).text(0) == "Radial styloid (left)"
    panel.state.undo()
    assert form.point_for("wrist.L").name == "Wrist"


def test_the_fill_refits_the_focused_freeform_through_the_history(panel):
    _pick(panel, FREEFORM)
    panel.start_guide()
    form = panel.state.forms[0]
    assert form.fill is FormFill.FACETED
    panel._fill.setCurrentIndex(panel._fill.findData(FormFill.SMOOTH.value))
    assert form.fill is FormFill.SMOOTH
    panel.state.undo()
    assert form.fill is FormFill.FACETED
    panel.end_guide()
    # Off the run, the picked form is the one the fill speaks for.
    panel._tree.setCurrentItem(panel._tree.topLevelItem(0))
    panel.update_enabled()
    assert panel._guide_form.isRowVisible(panel._fill)
    assert panel._fill.currentData() == FormFill.FACETED.value
    panel._fill.setCurrentIndex(panel._fill.findData(FormFill.SMOOTH.value))
    assert form.fill is FormFill.SMOOTH


def test_free_points_write_through_and_a_freeform_reads_them(panel):
    panel._free.setChecked(True)
    assert panel.state.form_settings.free_placement is True
    tool = panel._tool
    assert tool.free_points(PrimaryForm(preset=FREEFORM), panel.state.form_settings)
    assert not tool.free_points(PrimaryForm(preset="pelvis"), panel.state.form_settings)


def test_the_tab_switch_reads_and_writes_the_forms_visibility(panel):
    assert panel.shown() is True
    panel.set_shown(False)
    assert panel.state.form_settings.show_all is False and panel.shown() is False
    panel.set_shown(True)
    assert panel.state.form_settings.show_all is True


def test_append_takes_a_finished_freeform_up_again(panel):
    _pick(panel, FREEFORM)
    panel.start_guide()
    form = panel.state.forms[0]
    _pending(panel, "Wrist", Side.LEFT.value)
    _click(panel, (20, 80, 0))
    panel.end_guide()
    assert not panel._tool.guiding
    # Nothing selected: nothing to append to.
    panel._tree.clearSelection()
    panel.update_enabled()
    assert not panel._append.isEnabled()
    panel.append_landmarks()
    assert not panel._tool.guiding
    # The form's row, or one of its landmarks, offers the button.
    armed = []
    panel.form_toggled.connect(armed.append)
    panel.select_landmark((0, "wrist.L"))
    assert panel._append.isEnabled()
    panel.append_landmarks()
    assert panel._tool.guiding and panel._tool.guide.form == 0
    assert armed == [True]
    assert panel._point_name.text() == "Point 2"
    assert panel._point_side.currentData() == Side.LEFT.value
    _click(panel, (24, 76, 4))
    assert [entry.key for entry in form.points] == ["wrist.L", "point_2.L"]
    assert len(panel.state.forms) == 1
    # While a run is on, there is nothing further to append to.
    assert not panel._append.isEnabled()
    panel.end_guide()


def test_a_preset_cannot_be_appended_to(panel):
    _pick(panel, "pelvis")
    panel.start_guide()
    panel.end_guide()
    panel._tree.setCurrentItem(panel._tree.topLevelItem(0))
    panel.update_enabled()
    assert not panel._append.isEnabled()
    panel.append_landmarks()
    assert not panel._tool.guiding
