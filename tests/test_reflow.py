"""The layout that decides how many columns a panel is.

A panel does not know which edge of the window it has been dragged to, and
nothing in it is rebuilt when it moves.  All that changes is how much width
the layout is handed, so that is the only input worth testing: narrow gives
one column, wide gives several, and what comes back from ``heightForWidth``
is the height the panel actually takes at that width -- which is what the
scroll area around it is sized from, so being wrong about it is a panel that
scrolls when it should not, or clips when it should scroll.
"""

from __future__ import annotations

import os

import pytest

QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from PySide6.QtWidgets import QLabel, QSizePolicy, QTreeWidget  # noqa: E402

from refview.ui.elements.reflow import COLUMN_WIDTH, Reflow  # noqa: E402


@pytest.fixture(scope="session")
def app():
    """One offscreen Qt application for the run; see test_film_recorder."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    existing = QtWidgets.QApplication.instance()
    yield existing or QtWidgets.QApplication([])


def _block(height: int = 60) -> QLabel:
    block = QLabel("x")
    block.setFixedHeight(height)
    return block


def _panel(app, count: int = 6, height: int = 60) -> Reflow:
    panel = Reflow(column_width=COLUMN_WIDTH, spacing=6, margin=6)
    for _ in range(count):
        panel.add(_block(height))
    return panel


def test_a_narrow_panel_is_one_column(app):
    panel = _panel(app)
    panel.resize(COLUMN_WIDTH, 900)
    assert panel.columns() == 1


def test_a_wide_panel_breaks_into_columns(app):
    panel = _panel(app)
    panel.resize(COLUMN_WIDTH * 4 + 60, 300)
    assert panel.columns() == 4


def test_it_never_makes_more_columns_than_it_has_things(app):
    panel = _panel(app, count=2)
    panel.resize(COLUMN_WIDTH * 6, 300)
    assert panel.columns() == 2


def test_a_panel_too_narrow_for_a_column_still_has_one(app):
    panel = _panel(app)
    panel.resize(40, 900)
    assert panel.columns() == 1


def test_columns_make_the_panel_shorter(app):
    """What the columns are for: the same groups, in less height."""
    panel = _panel(app, count=6)
    tall = panel.heightForWidth(COLUMN_WIDTH)
    short = panel.heightForWidth(COLUMN_WIDTH * 3 + 40)
    assert short < tall
    # Six blocks over three columns is two blocks apiece, near enough.
    assert short == pytest.approx(tall / 3, rel=0.25)


def test_the_height_it_reports_is_the_height_it_takes(app):
    """The scroll area sizes the panel from this, so it has to be the truth."""
    panel = _panel(app, count=5)
    for width in (COLUMN_WIDTH, COLUMN_WIDTH * 2 + 20, COLUMN_WIDTH * 3 + 40):
        panel.resize(width, 50)
        reported = panel.heightForWidth(width)
        bottom = max(
            child.geometry().bottom()
            for child in panel.findChildren(QLabel)
        )
        assert reported >= bottom


def test_nothing_grows_unless_it_asked_to(app):
    """A column of plain groups sits at the top of a tall panel."""
    panel = _panel(app, count=2, height=40)
    panel.resize(COLUMN_WIDTH, 800)
    for child in panel.findChildren(QLabel):
        assert child.height() == 40


def test_what_asked_to_grow_is_given_the_room_left_over(app):
    """A tree or a gallery is worth as much of the dock as is going spare."""
    panel = Reflow(column_width=COLUMN_WIDTH)
    panel.add(_block(40))
    tree = QTreeWidget()
    tree.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
    panel.add(tree)
    panel.resize(COLUMN_WIDTH, 800)
    panel.layout().activate()
    assert tree.height() > 400


def test_a_hidden_group_takes_up_no_room(app):
    panel = _panel(app, count=4, height=50)
    panel.resize(COLUMN_WIDTH, 900)
    full = panel.heightForWidth(COLUMN_WIDTH)
    panel.findChildren(QLabel)[0].hide()
    assert panel.heightForWidth(COLUMN_WIDTH) < full
