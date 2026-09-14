"""Copies of controls: what they drive, and what keeps them honest.

The contract a copy makes is narrow and worth pinning down exactly.  Setting
the copy sets the original, and through it the document -- a copy is a second
pair of hands on one control, never a second control.  Coming back the other
way the copy follows the original, including where the original changed for a
reason nobody announced, which is what the tick is for.  And a control whose
kind cannot be copied says so rather than producing something that looks
right and does nothing.
"""

from __future__ import annotations

import os

import pytest

QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from PySide6.QtWidgets import QCheckBox, QListWidget  # noqa: E402

from refview.ui.elements import clone as cloning  # noqa: E402
from refview.ui.elements import naming  # noqa: E402
from refview.ui.elements.frame import Frame  # noqa: E402
from refview.ui.elements.slider import ValueSlider  # noqa: E402
from refview.ui.panels.section_panel import SectionPanel  # noqa: E402
from refview.ui.panels.shading_panel import ShadingPanel  # noqa: E402
from refview.ui.state import ViewerState  # noqa: E402


@pytest.fixture(scope="session")
def app():
    """One offscreen Qt application for the run; see test_film_recorder."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    existing = QtWidgets.QApplication.instance()
    yield existing or QtWidgets.QApplication([])


@pytest.fixture
def section(app):
    state = ViewerState()
    panel = SectionPanel(state)
    naming.register(panel, "section")
    return panel


# -- names -------------------------------------------------------------


def test_a_control_is_named_after_the_attribute_it_lives_on(section):
    assert naming.element_id(section._offset) == "section.offset"
    assert naming.lookup("section.offset") is section._offset


def test_an_attribute_beats_a_group_title_to_a_name(app):
    """``self._mode`` is ``mode``; the group called Mode settles for a number."""
    panel = ShadingPanel(ViewerState())
    naming.register(panel, "shading")
    assert naming.element_id(panel._mode) == "shading.mode"


def test_an_id_that_names_nothing_looks_up_as_nothing(section):
    assert naming.lookup("section.no_such_control") is None


# -- what a copy drives -------------------------------------------------


def test_setting_a_copy_sets_the_original_and_the_document(section):
    copy = cloning.clone(section._offset)
    copy._write(0.25, commit=True)
    assert section._offset.value() == pytest.approx(0.25)
    assert section.state.render.section.offset == pytest.approx(0.25)


def test_a_copied_switch_drives_the_original(section):
    copy = cloning.clone(section._enabled)
    copy.setChecked(True)
    assert section._enabled.isChecked()
    assert section.state.render.section.enabled


def test_a_copied_list_of_choices_drives_the_original(section):
    copy = cloning.clone(section._axis)
    assert copy.count() == section._axis.count()
    copy.setCurrentIndex(2)
    assert section._axis.currentIndex() == 2


def test_a_copied_button_presses_the_original(section):
    pressed = []
    section._from_view.clicked.connect(lambda: pressed.append(True))
    cloning.clone(section._from_view).click()
    assert pressed


# -- what keeps a copy honest -------------------------------------------


def test_a_copy_follows_the_original_on_the_tick(section):
    """The original changed without saying so; the copy catches up anyway."""
    copy = cloning.clone(section._offset)
    section._offset.set_value(0.4)
    assert copy.value() != pytest.approx(0.4)
    _tick(copy)
    assert copy.value() == pytest.approx(0.4)


def test_a_copy_goes_dead_when_its_original_does(section):
    """A panel taken apart underneath a copy must not take the window with it."""
    shiboken = pytest.importorskip("shiboken6")
    copy = cloning.clone(section._offset)
    shiboken.Shiboken.delete(section._offset)
    _tick(copy)
    assert not copy.isEnabled()
    assert "gone" in copy.toolTip()
    _tick(copy)  # and it stays gone, quietly, on every tick after.


def test_switching_the_original_off_switches_the_copy_off(section):
    copy = cloning.clone(section._thickness)
    section._thickness.setEnabled(False)
    _tick(copy)
    assert not copy.isEnabled()


# -- groups that get out of the way -------------------------------------


def test_a_group_folds_away_when_its_settings_go_dead(app):
    """Controls that cannot be used take the room of controls that can."""
    frame = Frame("Light", expanded=True)
    assert frame.is_expanded()
    frame.setEnabled(False)
    assert not frame.is_expanded()


def test_a_group_comes_back_the_way_it_was_left(app):
    """Folding is not a lock: switching it on again restores what was there."""
    frame = Frame("Light", expanded=True)
    frame.setEnabled(False)
    frame.setEnabled(True)
    assert frame.is_expanded()

    closed = Frame("Drawing", expanded=False)
    closed.setEnabled(False)
    closed.setEnabled(True)
    assert not closed.is_expanded()


def test_a_group_the_mode_does_not_answer_leaves_no_room_behind(app):
    """A matcap has no light to aim, so the Light group goes -- and its space.

    The panel takes the group off rather than folding it, which is the other
    half of the same rule: a control that cannot be used is worse than absent,
    because it takes the room of one that can.  What is tested here is the
    second half of that -- the layout gives the room back.
    """
    from refview.core.settings import ShadingMode
    from refview.ui.elements.reflow import COLUMN_WIDTH

    panel = ShadingPanel(ViewerState())
    panel.state.render.shading_mode = ShadingMode.LAMBERT
    panel.update_enabled()

    panel.state.render.shading_mode = ShadingMode.MATCAP
    panel.update_enabled()
    assert not panel._light_box.isVisibleTo(panel)
    without_light = panel.heightForWidth(COLUMN_WIDTH)
    # Matcap now brings its own gallery and preview into this panel. Compare
    # the same mode with and without Light, not two different sets of controls.
    panel._light_box.show()
    assert panel.heightForWidth(COLUMN_WIDTH) > without_light


def test_a_folded_group_is_only_as_tall_as_its_bar(app):
    from refview.ui.elements.frame import BAR_HEIGHT

    frame = Frame("Light", expanded=False)
    assert frame.sizeHint().height() == BAR_HEIGHT


# -- what can and cannot be copied --------------------------------------


def test_a_control_with_no_single_value_cannot_be_copied(app):
    assert cloning.clone(QListWidget()) is None
    assert not cloning.can_clone(QListWidget())


def test_copying_a_group_brings_its_rows(app):
    panel = ShadingPanel(ViewerState())
    naming.register(panel, "shading")
    copy = cloning.clone(panel._light_box)
    assert isinstance(copy, Frame)
    assert copy.title() == panel._light_box.title()
    rows = copy.findChildren(ValueSlider) + copy.findChildren(QCheckBox)
    assert len(rows) >= 4


def test_a_copied_group_still_drives_the_originals(app):
    panel = ShadingPanel(ViewerState())
    naming.register(panel, "shading")
    copy = cloning.clone(panel._light_box)
    first = copy.findChildren(ValueSlider)[0]
    first._write(first.maximum(), commit=True)
    assert panel._azimuth.value() == pytest.approx(first.value())


def _tick(copy) -> None:
    """Run the refresh the shared timer would have run."""
    for child in copy.children():
        if isinstance(child, cloning.Link):
            child.refresh()


# -- switches are buttons, and a button is pressed anywhere ---------------


def test_a_switch_answers_a_press_anywhere_on_its_face(app):
    """The theme makes a check box a button; Qt still thinks it is a tick box.

    Left alone, the style says such a control can be clicked on its words and
    nowhere else -- so a switch the width of the panel answers only in the
    middle, which is the worst of both shapes.
    """
    from PySide6.QtCore import QPoint, Qt
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QCheckBox

    from refview.ui.elements.toggles import WholeFaceToggles

    WholeFaceToggles.install(app)
    switch = QCheckBox("On")
    switch.resize(240, 22)
    switch.show()
    app.processEvents()

    far_side = QPoint(switch.width() - 6, switch.height() // 2)
    for expected in (True, False, True):
        QTest.mouseClick(
            switch, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, far_side
        )
        app.processEvents()
        assert switch.isChecked() is expected


def test_alt_is_left_alone_so_a_switch_can_still_be_copied(app):
    """Alt and a drag copies a control; that gesture must reach its own filter."""
    from PySide6.QtCore import QPoint, Qt
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QCheckBox

    from refview.ui.elements.toggles import WholeFaceToggles

    WholeFaceToggles.install(app)
    switch = QCheckBox("On")
    switch.resize(240, 22)
    switch.show()
    app.processEvents()

    QTest.mouseClick(
        switch,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.AltModifier,
        QPoint(switch.width() - 6, switch.height() // 2),
    )
    app.processEvents()
    assert not switch.isChecked()
