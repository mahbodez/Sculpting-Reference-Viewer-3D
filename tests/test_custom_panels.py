"""Panels the artist builds, and putting them back next time.

A hand-built panel is the one part of the layout Qt cannot write down for
itself, so it is written down here: a name, some groups, and in each group the
ids of the controls that were copied into it.  What matters is that the round
trip is faithful, and that it is forgiving in the one direction that counts --
a saved panel naming a control the application no longer has must come back
with the rest of its rows intact, because a layout that refuses to load is
worth less than one that loads with a gap in it.
"""

from __future__ import annotations

import os

import pytest

QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from PySide6.QtWidgets import QFormLayout, QLabel  # noqa: E402

from refview.ui.elements import clone as cloning  # noqa: E402
from refview.ui.elements import naming  # noqa: E402
from refview.ui.elements.custom import CustomPanel  # noqa: E402
from refview.ui.elements.frame import Frame  # noqa: E402
from refview.ui.elements.slider import ValueSlider  # noqa: E402
from refview.ui.panels.section_panel import SectionPanel  # noqa: E402
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


@pytest.fixture
def custom(app):
    panel = CustomPanel("Blocking in")
    panel.resize(300, 600)
    return panel


def test_a_new_panel_is_empty_and_says_so(custom):
    assert custom.is_empty()
    hints = [
        label
        for label in custom.findChildren(QLabel)
        if "Alt-drag" in label.text() and label.isVisibleTo(custom)
    ]
    assert hints


def test_a_copied_slider_brings_its_caption_inside_itself(custom, section):
    """It is named "Offset" in the panel it came from; it says so here too."""
    custom.take(section._offset)
    assert not custom.is_empty()
    form = custom.frames()[0].form()
    assert form.rowCount() == 1
    copy = form.itemAt(0, QFormLayout.ItemRole.FieldRole).widget()
    assert isinstance(copy, ValueSlider)
    assert copy.caption() == "Offset"
    # And no caption beside it as well, which would be the name twice.
    assert form.itemAt(0, QFormLayout.ItemRole.LabelRole) is None


def test_a_control_that_says_its_own_name_gets_no_caption(custom, section):
    """A check box already carries its words; a caption beside it repeats them."""
    custom.take(section._enabled)
    form = custom.frames()[0].form()
    assert form.itemAt(0, QFormLayout.ItemRole.LabelRole) is None


def test_a_control_with_nothing_written_on_it_gets_a_caption(custom, section):
    """A swatch is a coloured square; without its caption it is anonymous."""
    custom.take(section._contour_color)
    form = custom.frames()[0].form()
    label = form.itemAt(0, QFormLayout.ItemRole.LabelRole).widget()
    assert isinstance(label, QLabel)
    assert label.text() == "Outline"


def test_a_copy_in_a_hand_built_panel_still_drives_the_original(custom, section):
    copy = custom.take(section._offset)
    copy._write(0.3, commit=True)
    assert section.state.render.section.offset == pytest.approx(0.3)


def test_what_it_holds_survives_a_round_trip(custom, section):
    custom.add_frame("Cut")
    custom.take(section._offset, custom.frames()[0])
    custom.take(section._enabled, custom.frames()[0])
    custom.add_frame("Look")
    custom.take(section._contour_color, custom.frames()[1])

    written = custom.to_dict()
    custom.clear()
    assert custom.is_empty()
    custom.restore(written)

    assert custom.to_dict() == written
    assert [frame.title() for frame in custom.frames()] == ["Cut", "Look"]


def test_a_restored_copy_drives_the_original_again(custom, section):
    custom.take(section._offset)
    written = custom.to_dict()
    custom.clear()
    custom.restore(written)
    copy = custom.frames()[0].form().itemAt(0, QFormLayout.ItemRole.FieldRole).widget()
    copy._write(0.42, commit=True)
    assert section.state.render.section.offset == pytest.approx(0.42)


def test_a_row_naming_a_control_that_is_gone_is_skipped(custom, section):
    """A panel reorganised between versions loads with a gap, not an error."""
    custom.take(section._offset)
    written = custom.to_dict()
    written["groups"][0]["rows"].insert(0, {"element": "section.long_since_removed"})
    custom.clear()
    custom.restore(written)
    assert [row["element"] for row in custom.to_dict()["groups"][0]["rows"]] == [
        "section.offset"
    ]


def test_taking_a_copy_out_leaves_the_group_behind(custom, section):
    copy = custom.take(section._offset)
    custom.take(section._enabled)
    custom.drop_holder(copy)
    assert [row["element"] for row in custom.to_dict()["groups"][0]["rows"]] == [
        "section.enabled"
    ]


def test_a_panel_emptied_of_its_last_copy_invites_another(custom, section):
    copy = custom.take(section._offset)
    custom.drop_holder(copy)
    assert custom.is_empty()


def test_a_copy_can_be_moved_to_another_group(custom, section):
    copy = custom.take(section._offset)
    custom.add_frame("Look")
    custom.move_holder(copy, custom.frames()[1], row=-1)
    written = custom.to_dict()["groups"]
    assert [row["element"] for row in written[0]["rows"]] == []
    assert [row["element"] for row in written[1]["rows"]] == ["section.offset"]


def test_a_moved_copy_still_drives_the_original(custom, section):
    copy = custom.take(section._offset)
    custom.add_frame("Look")
    custom.move_holder(copy, custom.frames()[1], row=-1)
    copy._write(0.17, commit=True)
    assert section.state.render.section.offset == pytest.approx(0.17)


def test_a_copied_group_is_moved_among_the_groups(custom, section):
    """A group is not a row, so it goes ahead of the group it was dropped on."""
    custom.add_frame("First")
    custom.add_frame("Second")
    appearance = next(
        frame for frame in section.findChildren(Frame) if frame.title() == "Appearance"
    )
    moved = custom.take(appearance)
    assert [frame.title() for frame in custom.frames()][-1] == "Appearance"

    custom.move_holder(moved, custom.frames()[0], row=3)
    assert [frame.title() for frame in custom.frames()] == [
        "Appearance",
        "First",
        "Second",
    ]


def test_a_drop_carrying_a_control_takes_a_copy_of_it(custom, section):
    """The end of the gesture: the payload a drag carries, delivered."""
    carried = cloning.payload("section.offset")
    accepted = _drop_on(custom, carried)
    assert accepted
    assert [row["element"] for row in custom.to_dict()["groups"][0]["rows"]] == [
        "section.offset"
    ]


def test_a_drop_carrying_something_else_is_refused(custom, section):
    from PySide6.QtCore import QMimeData

    other = QMimeData()
    other.setText("a file, or a word, or anything at all")
    assert not _drop_on(custom, other)
    assert custom.is_empty()


def test_a_drop_naming_a_control_that_is_gone_is_refused(custom, section):
    carried = cloning.payload("section.long_since_removed")
    assert not _drop_on(custom, carried)
    assert custom.is_empty()


def _drop_on(panel, mime) -> bool:
    """Drop ``mime`` on the top-left of ``panel``; was it taken?

    The caller keeps hold of ``mime``: a real drag's payload belongs to the
    ``QDrag`` carrying it, and one made here belongs to nobody, so letting go
    of it leaves the event pointing at freed memory.
    """
    from PySide6.QtCore import QPointF, Qt
    from PySide6.QtGui import QDropEvent

    event = QDropEvent(
        QPointF(8, 8),
        Qt.DropAction.CopyAction,
        mime,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    panel.dropEvent(event)
    return event.isAccepted()


def test_renaming_says_so(custom):
    seen = []
    custom.changed.connect(lambda: seen.append(custom.title()))
    custom.set_title("Clay")
    assert seen == ["Clay"]
    assert custom.to_dict()["title"] == "Clay"
