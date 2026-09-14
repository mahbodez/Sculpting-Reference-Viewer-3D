"""Each panel in a dock of its own, and putting the docks back next time.

Two claims worth holding to.  Every panel can go to any edge -- that is the
whole reason there are ten docks instead of one -- and the switch that takes
what a panel draws off the model is on the dock's own bar, so it can be
reached while the panel is tabbed away behind another.

And the layout survives being closed: Qt writes down where the docks are, and
the panels the artist built are written down alongside, because Qt cannot
describe a panel that did not exist when it started.  The order matters --
those panels have to be rebuilt before Qt is asked to place the docks -- so
what is tested is the round trip through the settings, not the two halves.
"""

from __future__ import annotations

import os

import pytest

QtCore = pytest.importorskip("PySide6.QtCore")
QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from PySide6.QtCore import QSettings, Qt  # noqa: E402
from PySide6.QtWidgets import QFormLayout  # noqa: E402

from refview.core.session import Session  # noqa: E402
from refview.ui.elements import clone as cloning  # noqa: E402
from refview.ui.main_window import MainWindow  # noqa: E402


@pytest.fixture(scope="session")
def app():
    """One offscreen Qt application for the run; see test_film_recorder."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    existing = QtWidgets.QApplication.instance()
    application = existing or QtWidgets.QApplication([])
    application.setOrganizationName("refview-tests")
    application.setApplicationName("refview-tests")
    yield application


@pytest.fixture
def window(app):
    """A window with the saved layout out of the way, and put back after.

    Shown, because a main window that has never been shown has never laid its
    docks out either: the viewport is still at its default size and every
    point in the window is inside it, which would make a test about where a
    drop landed agree with anything.
    """
    QSettings().clear()
    made = MainWindow()
    made.resize(1400, 900)
    made.show()
    app.processEvents()
    yield made
    made._layout_write.stop()
    made.close()
    QSettings().clear()


PANELS = (
    "model",
    "shading",
    "planes",
    "section",
    "measure",
    "annotate",
    "armature",
    "forms",
    "camera",
)


def test_every_panel_has_a_dock_of_its_own(window):
    keys = [dock.key() for dock in window._workspace.docks()]
    assert keys == list(PANELS)


def test_a_panel_may_be_docked_to_any_edge(window):
    for dock in window._workspace.docks():
        assert dock.allowedAreas() == Qt.DockWidgetArea.AllDockWidgetAreas


def test_a_panel_may_be_floated_off(window):
    dock = window._workspace.docks()[0]
    dock.setFloating(True)
    assert dock.isFloating()
    dock.setFloating(False)


@pytest.mark.parametrize(
    ("key", "read"),
    [
        ("planes", lambda state: state.render.planes.enabled),
        ("section", lambda state: state.render.section.enabled),
        ("measure", lambda state: state.measurement_settings.show_all),
        ("annotate", lambda state: state.annotation_settings.visible),
        ("armature", lambda state: state.armature_settings.show_all),
        ("forms", lambda state: state.form_settings.show_all),
    ],
)
def test_the_switch_on_a_dock_bar_is_the_panels_own_visibility(window, key, read):
    dock = next(d for d in window._workspace.docks() if d.key() == key)
    switch = dock.bar().switch()
    assert switch is not None
    for on in (True, False, True):
        switch.setChecked(on)
        assert read(window.state) is on


@pytest.mark.parametrize("key", ["camera", "shading", "model"])
def test_a_panel_that_draws_nothing_has_no_switch(window, key):
    dock = next(d for d in window._workspace.docks() if d.key() == key)
    assert dock.bar().switch() is None


# -- panels built by hand ----------------------------------------------


def test_a_new_hand_built_panel_gets_a_dock(window):
    panel = window._workspace.new_custom_panel()
    keys = [dock.key() for dock in window._workspace.docks()]
    assert keys[-1] == "custom_1"
    assert panel.title() == "Custom 1"


def test_hand_built_panels_are_numbered_apart(window):
    window._workspace.new_custom_panel()
    window._workspace.new_custom_panel()
    keys = [dock.key() for dock in window._workspace.docks()]
    assert keys[-2:] == ["custom_1", "custom_2"]


def test_removing_a_hand_built_panel_takes_its_dock_with_it(window):
    window._workspace.new_custom_panel()
    window._workspace.remove_custom_panel("custom_1")
    assert "custom_1" not in [dock.key() for dock in window._workspace.docks()]
    assert not window._workspace.custom_panels()


# -- putting it back ---------------------------------------------------


def test_the_layout_comes_back_through_the_settings(window, app):
    panel = window._workspace.new_custom_panel("Blocking in")
    section = window._workspace.panel("section")
    panel.take(section._offset)
    panel.take(section._enabled)
    window._workspace.save()

    again = MainWindow()
    try:
        rebuilt = again._workspace.custom_panels()
        assert list(rebuilt) == ["custom_1"]
        assert rebuilt["custom_1"].title() == "Blocking in"
        rows = rebuilt["custom_1"].to_dict()["groups"][0]["rows"]
        assert [row["element"] for row in rows] == [
            "section.offset",
            "section.enabled",
        ]
    finally:
        again._layout_write.stop()
        again.close()


def test_a_restored_copy_drives_the_new_windows_own_control(window, app):
    panel = window._workspace.new_custom_panel("Blocking in")
    panel.take(window._workspace.panel("section")._offset)
    window._workspace.save()

    again = MainWindow()
    try:
        rebuilt = again._workspace.custom_panels()["custom_1"]
        form = rebuilt.frames()[0].form()
        copy = form.itemAt(0, QFormLayout.ItemRole.FieldRole).widget()
        copy._write(0.33, commit=True)
        assert again.state.render.section.offset == pytest.approx(0.33)
        # And it drove *that* window's control, not the one it was built from.
        assert window.state.render.section.offset != pytest.approx(0.33)
    finally:
        again._layout_write.stop()
        again.close()


# -- throwing a copy away ----------------------------------------------


def _drag_over(window, point, holder, monkeypatch, kind):
    """A drag of ``holder`` arriving at ``point`` in the window's coordinates.

    A real drag keeps its payload alive in the ``QDrag`` carrying it and the
    copy in a module-level handle; neither exists here, so both are stood in
    for -- the payload is handed back for the caller to hold, because letting
    go of it leaves the event pointing at freed memory.
    """
    from PySide6.QtCore import QPointF
    from PySide6.QtGui import QDropEvent

    import refview.ui.main_window as main_window

    monkeypatch.setattr(main_window, "in_flight", lambda: holder)
    mime = cloning.payload("section.offset", moving=holder)
    # A drop is given the fractional position; the two before it are not.
    where = QPointF(point) if kind is QDropEvent else point
    event = kind(
        where,
        Qt.DropAction.MoveAction,
        mime,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    return event, mime


def _middle_of_the_view(window):
    view = window.centralWidget()
    return view.mapTo(window, view.rect().center())


def test_a_copy_dropped_on_the_model_is_thrown_away(window, monkeypatch):
    """The gesture the whole thing rests on: drag it onto the model, it goes."""
    from PySide6.QtGui import QDropEvent

    panel = window._workspace.new_custom_panel("Blocking in")
    copy = panel.take(window._workspace.panel("section")._offset)
    assert not panel.is_empty()

    event, mime = _drag_over(
        window, _middle_of_the_view(window), copy, monkeypatch, QDropEvent
    )
    window.dropEvent(event)

    assert event.isAccepted()
    assert panel.is_empty()
    del mime


def test_a_copy_let_go_anywhere_but_the_model_is_kept(window, monkeypatch):
    """A gesture that destroys something only fires where it clearly meant to."""
    from PySide6.QtCore import QPoint
    from PySide6.QtGui import QDropEvent

    panel = window._workspace.new_custom_panel("Blocking in")
    copy = panel.take(window._workspace.panel("section")._offset)

    event, mime = _drag_over(window, QPoint(2, 2), copy, monkeypatch, QDropEvent)
    window.dropEvent(event)

    assert not event.isAccepted()
    assert not panel.is_empty()
    del mime


def test_a_copy_is_let_into_the_window_wherever_it_arrives(window, monkeypatch):
    """Refused at the door it would never reach the model; so it is let in."""
    from PySide6.QtCore import QPoint
    from PySide6.QtGui import QDragEnterEvent

    panel = window._workspace.new_custom_panel("Blocking in")
    copy = panel.take(window._workspace.panel("section")._offset)

    event, mime = _drag_over(
        window, QPoint(2, 2), copy, monkeypatch, QDragEnterEvent
    )
    window.dragEnterEvent(event)

    assert event.isAccepted()
    del mime


def test_the_drop_is_only_offered_over_the_model(window, monkeypatch):
    from PySide6.QtCore import QPoint
    from PySide6.QtGui import QDragMoveEvent

    panel = window._workspace.new_custom_panel("Blocking in")
    copy = panel.take(window._workspace.panel("section")._offset)

    over_the_bar, mime_a = _drag_over(
        window, QPoint(2, 2), copy, monkeypatch, QDragMoveEvent
    )
    window.dragMoveEvent(over_the_bar)
    assert not over_the_bar.isAccepted()

    over_the_model, mime_b = _drag_over(
        window, _middle_of_the_view(window), copy, monkeypatch, QDragMoveEvent
    )
    window.dragMoveEvent(over_the_model)
    assert over_the_model.isAccepted()
    del mime_a, mime_b


def test_resetting_forgets_the_saved_layout(window):
    window._workspace.new_custom_panel()
    window._workspace.save()
    window._workspace.reset()
    assert not QSettings().value("workspace/custom", "")


# -- and into the session file -----------------------------------------


def test_a_session_carries_the_hand_built_panels(window, tmp_path):
    panel = window._workspace.new_custom_panel("Blocking in")
    panel.take(window._workspace.panel("section")._offset)

    path = tmp_path / "bust.refview.json"
    window.state.save_session(path, layout=window._workspace.to_dict())

    written = Session.load(path)
    assert written.version >= 7
    assert written.layout["custom"][0]["title"] == "Blocking in"


def test_a_session_saved_without_panels_leaves_the_ones_open_alone(window, tmp_path):
    """An older file must not be able to sweep away the artist's own panels."""
    path = tmp_path / "plain.refview.json"
    window.state.save_session(path)
    window._workspace.new_custom_panel("Keep me")

    window.load_session(path)

    assert [p.title() for p in window._workspace.custom_panels().values()] == ["Keep me"]


# -- the switch where it is actually needed ----------------------------


def _tab_switch(window, title):
    """The show/hide switch on the tab named ``title``, if it has one."""
    from PySide6.QtWidgets import QTabBar

    window._workspace.dress_tabs()
    for bar in window.findChildren(QTabBar):
        for index in range(bar.count()):
            if bar.tabText(index) == title:
                return bar.tabButton(index, QTabBar.ButtonPosition.LeftSide)
    return None


def test_a_tabbed_panel_still_shows_its_switch(window):
    """Stacked behind another panel is where the switch is worth the most."""
    assert _tab_switch(window, "Armature") is not None


def test_a_panel_that_draws_nothing_gets_no_switch_on_its_tab(window):
    assert _tab_switch(window, "Camera") is None


def test_clicking_the_switch_on_a_tab_works(window, app):
    """It is fifteen pixels wide and carries no words, which is exactly the
    shape the style computes an empty click area for.  So: clicked, not set."""
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest

    switch = _tab_switch(window, "Armature")
    assert switch is not None
    for _ in range(2):
        before = window.state.armature_settings.show_all
        QTest.mouseClick(switch, Qt.MouseButton.LeftButton)
        app.processEvents()
        assert window.state.armature_settings.show_all is not before


def test_the_switch_on_a_dock_bar_can_be_clicked_too(window, app):
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest

    dock = next(d for d in window._workspace.docks() if d.key() == "section")
    before = window.state.render.section.enabled
    QTest.mouseClick(dock.bar().switch(), Qt.MouseButton.LeftButton)
    app.processEvents()
    assert window.state.render.section.enabled is not before


def test_resetting_the_layout_puts_the_docks_back_at_once(window):
    """Not "clear the setting and restart": tidied now, or it is not tidying."""
    dock = next(d for d in window._workspace.docks() if d.key() == "camera")
    window.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)
    assert window.dockWidgetArea(dock) == Qt.DockWidgetArea.BottomDockWidgetArea

    window._reset_layout()

    assert window.dockWidgetArea(dock) == Qt.DockWidgetArea.RightDockWidgetArea
    assert all(not d.isFloating() and d.isVisible() for d in window._workspace.docks())


def test_resetting_keeps_the_panels_built_by_hand(window):
    """They are work, not arrangement."""
    panel = window._workspace.new_custom_panel("Blocking in")
    panel.take(window._workspace.panel("section")._offset)
    window._reset_layout()
    kept = window._workspace.custom_panels()
    assert list(kept) == ["custom_1"]
    assert kept["custom_1"].to_dict()["groups"][0]["rows"]


def test_a_panel_does_not_cover_its_own_title(window):
    """A dock puts the panel below its bar's *hint*, not below its bar.

    Leave the hint to the layout and it comes back as the height of the two
    little buttons in the corner; the panel is then laid over the bottom of
    the bar and every panel's name loses its lower half.  A fixed height on
    the widget does not help, because that is not the number the dock reads.
    """
    from refview.ui.elements.dock import BAR_HEIGHT

    for dock in window._workspace.docks():
        assert dock.bar().sizeHint().height() == BAR_HEIGHT
        assert dock.widget().geometry().y() >= BAR_HEIGHT


def test_the_switch_is_not_squeezed_to_nothing(window):
    """The style sheet's width beats the widget's own, so it has to agree."""
    from refview.ui.elements.dock import SWITCH_SIZE

    for dock in window._workspace.docks():
        switch = dock.bar().switch()
        if switch is not None:
            assert switch.width() >= SWITCH_SIZE
            assert switch.height() >= SWITCH_SIZE


# -- taking a hand-built panel away, after a layout has been restored ------
#
# Qt will not let a restored dock arrangement be edited.  Once
# ``restoreState`` has placed the docks, taking one out and putting another
# in reads freed memory and the process goes down inside Qt's own layout --
# every way of putting the dock down does it, and a window whose layout was
# never restored survives all of them.  So a dock is never given up: it is
# emptied, hidden and handed back out for the next panel.  These are here
# because the failure is a crash rather than a wrong answer, which means the
# test that catches it is the test that survives running.


@pytest.fixture
def restored(app, window):
    """A second window, built from a layout the first one saved.

    The point is ``restoreState``: a window that never restored a layout is
    not the window this is about.
    """
    window._workspace.new_custom_panel("Blocking in", key="custom_1")
    window._workspace.save()

    made = MainWindow()
    made.resize(1400, 900)
    made.show()
    app.processEvents()
    yield made
    made._layout_write.stop()
    made.close()


def test_a_restored_layout_brings_the_hand_built_panels_with_it(restored):
    assert "custom_1" in restored._workspace.custom_panels()


def test_a_panel_can_be_taken_away_and_another_built_after_a_restore(restored):
    """The crash this is about takes the process with it, so arriving is passing."""
    restored._workspace.remove_custom_panel("custom_1")
    panel = restored._workspace.new_custom_panel("Another")
    assert panel.title() == "Another"


def test_loading_a_session_over_a_restored_layout_survives(restored, tmp_path):
    """The path the artist actually walks: File, Load Session, twice."""
    session = tmp_path / "work.refview"
    restored._state.save_session(session, layout=restored._workspace.to_dict())
    restored.load_session(session)
    restored.load_session(session)
    assert restored._workspace.custom_panels()


def test_a_panel_taken_away_leaves_no_dock_behind(restored):
    restored._workspace.remove_custom_panel("custom_1")
    assert "custom_1" not in restored._workspace.custom_panels()
    assert all(dock.key() != "custom_1" for dock in restored._workspace.docks())


def test_the_dock_of_a_panel_taken_away_is_used_again(restored):
    """Parked rather than destroyed, so the count does not climb for ever."""
    was = next(d for d in restored._workspace.docks() if d.key() == "custom_1")
    before = len(restored._workspace.docks())
    restored._workspace.remove_custom_panel("custom_1")
    restored._workspace.new_custom_panel("Another")
    assert len(restored._workspace.docks()) == before
    assert any(dock is was for dock in restored._workspace.docks())


def test_a_reused_dock_does_not_bring_the_old_panels_contents_with_it(restored):
    """It is a new panel, whatever it happens to be made out of."""
    panel = restored._workspace.custom_panels()["custom_1"]
    panel.add_frame("Some group")
    assert [frame.title() for frame in panel.frames()] == ["Some group"]

    restored._workspace.remove_custom_panel("custom_1")
    fresh = restored._workspace.new_custom_panel("Another")
    assert fresh.frames() == []
    assert fresh.title() == "Another"
