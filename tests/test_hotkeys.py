"""Hotkeys: the map, the store, the binder, and the gesture that assigns one."""

from __future__ import annotations

import os

import pytest

from refview.core.hotkeys import CONTROL_PREFIX, Command, HotkeyMap

QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from PySide6.QtCore import QEvent, QPointF, QSettings, Qt  # noqa: E402
from PySide6.QtGui import QKeySequence, QMouseEvent  # noqa: E402
from PySide6.QtWidgets import QApplication, QCheckBox, QMessageBox, QPushButton  # noqa: E402

from refview.ui import hotkeys as hotkeys_module  # noqa: E402
from refview.ui.elements.keys import KeyGesture, watch_keys  # noqa: E402
from refview.ui.elements.naming import register  # noqa: E402

# -- the map, which knows nothing of Qt ------------------------------------


def _map() -> HotkeyMap:
    made = HotkeyMap()
    made.declare(Command("view.frame", "Frame Object", "F", "view", "View"))
    made.declare(Command("file.open", "Open Model", "Ctrl+O", "window", "File"))
    made.declare(Command("file.load", "Load Session", "", "window", "File"))
    return made


def test_a_command_keeps_its_shipped_keys_until_the_artist_moves_them():
    made = _map()
    assert made.keys_for("view.frame") == "F"
    assert made.holder_of("F") == "view.frame"
    assert made.assign("view.frame", "H") is None
    assert made.keys_for("view.frame") == "H"
    assert made.holder_of("F") is None
    assert made.is_changed("view.frame")
    assert made.to_dict() == {"view.frame": "H"}


def test_putting_the_shipped_keys_back_is_not_a_choice_worth_writing_down():
    made = _map()
    made.assign("view.frame", "H")
    made.assign("view.frame", "F")
    assert not made.is_changed("view.frame")
    assert made.to_dict() == {}


def test_one_key_one_command():
    """A key given to something else comes off what had it, and the map says what that was."""
    made = _map()
    assert made.assign("file.load", "F") == "view.frame"
    assert made.keys_for("view.frame") == ""
    assert made.keys_for("file.load") == "F"
    assert made.to_dict() == {"view.frame": "", "file.load": "F"}
    assert made.assign("file.load", "F") is None


def test_taking_a_key_away_and_resetting():
    made = _map()
    made.clear("file.open")
    assert made.keys_for("file.open") == ""
    assert made.holder_of("Ctrl+O") is None
    made.reset("file.open")
    assert made.keys_for("file.open") == "Ctrl+O"
    made.assign("file.load", "Ctrl+O")
    assert made.reset("file.open") == "file.load"
    assert made.keys_for("file.load") == ""
    made.assign("view.frame", "Q")
    made.reset()
    assert made.is_default()
    assert made.keys_for("view.frame") == "F"


def test_a_choice_about_a_control_not_yet_seen_is_kept():
    made = _map()
    control = CONTROL_PREFIX + "section.enabled"
    made.assign(control, "K")
    assert made.holder_of("K") == control
    assert made.bound()[control] == "K"
    assert control in made.to_dict()


def test_reading_a_file_keeps_what_makes_sense():
    made = _map()
    made.read(
        {
            "file.open": "Ctrl+P",
            "view.frame": 12,
            "": "X",
            "control:late.button": "F",
            "control:other.button": "F",
            "file.load": "",
        }
    )
    assert made.keys_for("file.open") == "Ctrl+P"
    # The shipped F went to a control, so Frame Object has to give it up.
    assert made.keys_for("view.frame") == ""
    assert made.holder_of("F") == "control:late.button"
    assert made.keys_for("file.load") == ""
    made.read("not a dict")
    assert made.is_default()


def test_a_command_declared_after_its_key_was_given_away_arrives_without_it():
    made = HotkeyMap()
    made.read({"control:late.button": "F"})
    made.declare(Command("view.frame", "Frame Object", "F", "view"))
    assert made.keys_for("view.frame") == ""
    assert made.holder_of("F") == "control:late.button"


def test_an_unknown_scope_is_refused():
    with pytest.raises(ValueError):
        HotkeyMap().declare(Command("x", "X", "", "everywhere"))


# -- the store and the window -------------------------------------------------


@pytest.fixture(scope="session")
def app():
    """One offscreen Qt application for the run; see test_film_recorder."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    existing = QApplication.instance()
    application = existing or QApplication([])
    application.setOrganizationName("refview-tests")
    application.setApplicationName("refview-tests")
    yield application


@pytest.fixture
def store(app):
    QSettings().remove(hotkeys_module.KEY)
    hotkeys_module.forget()
    made = hotkeys_module.store()
    yield made
    hotkeys_module.forget()
    QSettings().remove(hotkeys_module.KEY)


@pytest.fixture
def window(store):
    from refview.ui.main_window import MainWindow

    QSettings().remove("workspace/layout")
    made = MainWindow()
    yield made
    made._layout_write.stop()
    made.close()


def test_the_store_writes_only_the_choices_and_reads_them_back(store):
    store.declare(Command("view.frame", "Frame Object", "F", "view"))
    store.assign("view.frame", "ctrl+k")
    assert store.keys_for("view.frame") == "Ctrl+K"
    assert QSettings().value(hotkeys_module.KEY) == '{"view.frame": "Ctrl+K"}'
    hotkeys_module.forget()
    again = hotkeys_module.store()
    again.declare(Command("view.frame", "Frame Object", "F", "view"))
    assert again.keys_for("view.frame") == "Ctrl+K"


def test_the_window_declares_its_menus_and_letters_and_keys_them(window, store):
    assert store.keys_for("file.open_model") == "Ctrl+O"
    assert store.keys_for("view.frame") == "F"
    assert store.map.command("view.frame").scope == "view"
    assert window._frame_action.text() == "&Frame Object  (F)"
    assert window._frame_action.shortcut().isEmpty()
    assert window._undo_action.shortcut() == QKeySequence("Ctrl+Z")


def test_rekeying_a_command_moves_the_menu_and_the_shortcut(window, store):
    store.assign("file.open_model", "Ctrl+Shift+O")
    actions = window.findChildren(type(window._undo_action))
    action = next(a for a in actions if "Open Model" in a.text())
    assert action.shortcut() == QKeySequence("Ctrl+Shift+O")
    store.assign("view.frame", "H")
    assert window._frame_action.text() == "&Frame Object  (H)"
    assert window._binder.shortcut("view.frame").key() == QKeySequence("H")


def test_a_key_on_a_panels_switch_presses_it(window, store):
    from refview.ui.elements.naming import lookup

    switch = lookup("dock.section.shown")
    assert isinstance(switch, QCheckBox)
    command = hotkeys_module.command_for(switch)
    assert command == CONTROL_PREFIX + "dock.section.shown"
    assert hotkeys_module.describe(store, command) == "Show Section"
    was = switch.isChecked()
    store.assign(command, "Ctrl+Alt+Shift+F9")
    shortcut = window._binder.shortcut(command)
    assert shortcut is not None and shortcut.key() == QKeySequence("Ctrl+Alt+Shift+F9")
    shortcut.activated.emit()
    assert switch.isChecked() is not was
    store.clear(command)
    assert window._binder.shortcut(command) is None


def test_a_control_says_its_key_in_its_tooltip_and_a_tool_button_in_its_name(window, store):
    from refview.ui.elements.naming import lookup

    switch = lookup("dock.section.shown")
    plain = switch.toolTip()
    assert "Hotkey" not in plain
    store.assign(CONTROL_PREFIX + "dock.section.shown", "Ctrl+Alt+F9")
    assert switch.toolTip() == f"{plain}\nHotkey: Ctrl+Alt+F9"
    store.assign(CONTROL_PREFIX + "dock.section.shown", "F10")
    assert switch.toolTip() == f"{plain}\nHotkey: F10"
    store.clear(CONTROL_PREFIX + "dock.section.shown")
    assert switch.toolTip() == plain

    # The panel's arming button is the same command as the view's letter.
    arm = lookup("measure.toggle")
    assert hotkeys_module.command_for(arm) == "measure.tool"
    assert arm.text() == "Measure  (M)" and arm.toolTip().endswith("Hotkey: M")
    store.assign("measure.tool", "Ctrl+M")
    assert arm.text() == "Measure  (Ctrl+M)" and arm.toolTip().endswith("Hotkey: Ctrl+M")
    assert window._measure_action.text() == "&Measure Tool  (Ctrl+M)"
    store.clear("measure.tool")
    assert arm.text() == "Measure" and "Hotkey" not in arm.toolTip()


def test_a_copy_of_a_control_speaks_for_what_the_original_does(window, store):
    from refview.ui.elements.naming import lookup

    panel = window._workspace.new_custom_panel("Mine")
    arm = panel.take(lookup("measure.toggle"))
    assert hotkeys_module.command_for(arm) == "measure.tool"
    clear = panel.take(lookup("dock.section.shown"))
    assert hotkeys_module.command_for(clear) == CONTROL_PREFIX + "dock.section.shown"


def test_the_editor_lists_the_commands_and_the_keyed_controls(window, store):
    listed = hotkeys_module.listed(store)
    assert "file.open_model" in listed and "view.frame" in listed
    assert not any(one.startswith(CONTROL_PREFIX) for one in listed)
    store.assign(CONTROL_PREFIX + "dock.armature.shown", "F7")
    listed = hotkeys_module.listed(store)
    assert listed[-1] == CONTROL_PREFIX + "dock.armature.shown"
    window._show_settings("hotkeys")
    table = window._settings._hotkey_table
    assert table.rowCount() == len(listed)
    names = [table.item(row, 0).text() for row in range(table.rowCount())]
    assert any(name.endswith("Show Armature") for name in names)
    assert any(name.startswith("File") and name.endswith("Open Model") for name in names)


def test_assigning_a_key_that_is_taken_asks_first(window, store, monkeypatch):
    asked = []

    def answer(*args, **kwargs):
        asked.append(args[1])
        return QMessageBox.StandardButton.No

    monkeypatch.setattr(QMessageBox, "question", staticmethod(answer))
    assert not hotkeys_module.assign(store, "file.load_session", "Ctrl+O", window)
    assert asked == ["Hotkey Already Assigned"]
    assert store.keys_for("file.open_model") == "Ctrl+O"
    monkeypatch.setattr(
        QMessageBox, "question", staticmethod(lambda *a, **k: QMessageBox.StandardButton.Yes)
    )
    assert hotkeys_module.assign(store, "file.load_session", "Ctrl+O", window)
    assert store.keys_for("file.load_session") == "Ctrl+O"
    assert store.keys_for("file.open_model") == ""


# -- the gesture ------------------------------------------------------------


def _click(widget, modifiers, kind=QEvent.Type.MouseButtonPress):
    at = QPointF(widget.rect().center())
    left = Qt.MouseButton.LeftButton
    return QMouseEvent(kind, at, at, left, left, modifiers)


def test_ctrl_alt_click_asks_for_a_key_without_pressing_the_button(app):
    button = QPushButton("Fold")
    button.setObjectName("fold")
    register(button, "gesture_test")
    watch_keys(button)
    pressed = []
    button.clicked.connect(lambda: pressed.append(True))
    asked = []
    gesture = KeyGesture.instance()
    connection = gesture.requested.connect(asked.append)
    try:
        both = Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.AltModifier
        assert gesture.eventFilter(button, _click(button, both))
        assert gesture.eventFilter(button, _click(button, both, QEvent.Type.MouseButtonRelease))
        assert asked == [button] and pressed == []
        assert hotkeys_module.command_for(button) == CONTROL_PREFIX + "gesture_test.fold"
        # Alt alone is the copier's gesture, and a plain click is a click.
        assert not gesture.eventFilter(button, _click(button, Qt.KeyboardModifier.AltModifier))
        assert not gesture.eventFilter(button, _click(button, Qt.KeyboardModifier.NoModifier))
        assert asked == [button]
    finally:
        gesture.requested.disconnect(connection)


def test_ctrl_alt_clicking_a_panels_button_reaches_the_window(window, store, monkeypatch):
    """End to end: the filter is on the panel's buttons and the window hears it."""
    from PySide6.QtTest import QTest

    from refview.ui import main_window as main_window_module
    from refview.ui.elements.naming import lookup

    asked = []
    monkeypatch.setattr(
        main_window_module, "ask_for", lambda widget, hotkeys, parent: asked.append(widget) or True
    )
    window.show()
    button = lookup("measure.clear_all") or lookup("measure.toggle")
    assert isinstance(button, QPushButton)
    toggled = []
    button.clicked.connect(lambda: toggled.append(True))
    both = Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.AltModifier
    QTest.mouseClick(button, Qt.MouseButton.LeftButton, both)
    assert asked == [button]
    assert toggled == []


def test_a_window_answers_the_gesture_only_for_its_own_buttons(window, store, monkeypatch):
    from refview.ui import main_window as main_window_module
    from refview.ui.elements.naming import lookup

    asked = []
    monkeypatch.setattr(
        main_window_module, "ask_for", lambda widget, hotkeys, parent: asked.append(widget) or True
    )
    switch = lookup("dock.section.shown")
    KeyGesture.instance().requested.emit(switch)
    assert asked == [switch]
    stranger = QPushButton("Elsewhere")
    KeyGesture.instance().requested.emit(stranger)
    assert asked == [switch]
