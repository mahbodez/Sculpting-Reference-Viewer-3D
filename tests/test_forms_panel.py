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
from refview.core.forms import HEAD, PrimaryForm, build_form, built_count
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
