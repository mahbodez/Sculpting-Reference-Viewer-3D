"""Where the hotkeys are kept, and how they become keys that do things.

:mod:`refview.core.hotkeys` says what the map *is*; this says where it lives,
how it is turned into shortcuts in a window, and how a key gets put on a
control without opening the preferences.  Three jobs:

Living: one JSON blob under one settings key, the way the preferences are
kept, holding only what the artist changed.

Binding: the window declares its commands with the :class:`HotkeyBinder`,
which owns a shortcut for each and re-keys the lot whenever the store moves.
A menu entry shows its keys in the menu; a key scoped to the view shows them
in the entry's text instead, since the entry itself must not answer to a key
the view alone should hear.  A button in a panel gets a shortcut only once
the artist has put a key on it, and the shortcut presses the button, so
whatever the button does when clicked is what the key does.

Asking: Ctrl-Alt-click on a button asks for a key.  The dialog takes one
keystroke, and if that key already does something the artist is told what,
and asked, before it is taken away.
"""

from __future__ import annotations

import json
from collections.abc import Callable

from PySide6.QtCore import QObject, QSettings, Qt, QTimer, Signal
from PySide6.QtGui import QAction, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QAbstractButton,
    QDialog,
    QDialogButtonBox,
    QKeySequenceEdit,
    QLabel,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from ..core.hotkeys import CONTROL_PREFIX, Command, HotkeyMap
from .elements.clone import SOURCE_PROPERTY
from .elements.keys import COMMAND_PROPERTY, KeyGesture, can_take_key
from .elements.naming import caption_for, element_id, lookup

#: Where the whole of it is written.
KEY = "hotkeys/all"

#: Property holding what was last written into a widget's tooltip about its
#: key, so that it can be taken out again when the key moves.
_TIP_PROPERTY = "refview_hotkey_tip"
#: Property holding a button's text before the key was written after it, for
#: a button that stands for one of the view's letters.
_TEXT_PROPERTY = "refview_hotkey_text"


# ----------------------------------------------------------------------
# Keys as text
# ----------------------------------------------------------------------


def normalize(keys: str | QKeySequence) -> str:
    """One spelling for a key, so that ``ctrl+k`` and ``Ctrl+K`` are the same key.

    Portable text, which is what is written down and compared; see
    :func:`spoken` for what is shown.  Empty for nothing, or for nonsense.
    """
    sequence = keys if isinstance(keys, QKeySequence) else QKeySequence(keys)
    if sequence.isEmpty():
        return ""
    return sequence.toString(QKeySequence.SequenceFormat.PortableText)


def spoken(keys: str) -> str:
    """A key the way the platform writes it -- ``⌘K`` on a Mac, ``Ctrl+K`` elsewhere."""
    if not keys:
        return ""
    return QKeySequence(keys, QKeySequence.SequenceFormat.PortableText).toString(
        QKeySequence.SequenceFormat.NativeText
    )


# ----------------------------------------------------------------------
# The store
# ----------------------------------------------------------------------


class HotkeyStore(QObject):
    """The map, and one signal saying it has changed."""

    changed = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._map = HotkeyMap()

    @property
    def map(self) -> HotkeyMap:
        """The map as it stands.  Treat as read-only; change it through the store."""
        return self._map

    def declare(self, command: Command) -> None:
        self._map.declare(command)

    def keys_for(self, command_id: str) -> str:
        return self._map.keys_for(command_id)

    def holder_of(self, keys: str) -> str | None:
        return self._map.holder_of(normalize(keys))

    def assign(self, command_id: str, keys: str, *, save: bool = True) -> str | None:
        """Put ``keys`` on a command; says what they came off, if anything."""
        previous = self._map.assign(command_id, normalize(keys))
        self._announce(save)
        return previous

    def clear(self, command_id: str, *, save: bool = True) -> None:
        self._map.clear(command_id)
        self._announce(save)

    def reset(self, command_id: str | None = None, *, save: bool = True) -> None:
        self._map.reset(command_id)
        self._announce(save)

    def _announce(self, save: bool) -> None:
        if save:
            self.save()
        self.changed.emit()

    # -- the settings file ----------------------------------------------

    def load(self, settings: QSettings | None = None) -> None:
        """Read the choices off the machine.  Never raises."""
        settings = settings or QSettings()
        written = settings.value(KEY, "")
        data = None
        if isinstance(written, str) and written.strip():
            try:
                data = json.loads(written)
            except ValueError:
                data = None
        self._map.read(data)

    def save(self, settings: QSettings | None = None) -> None:
        settings = settings or QSettings()
        settings.setValue(KEY, json.dumps(self._map.to_dict()))


_store: HotkeyStore | None = None


def store() -> HotkeyStore:
    """The one store, loading it off the machine the first time it is asked."""
    global _store
    if _store is None:
        _store = HotkeyStore()
        _store.load()
    return _store


def forget() -> None:
    """Drop the loaded store, so the next call reads the settings again.  For tests."""
    global _store
    _store = None


# ----------------------------------------------------------------------
# Commands made out of controls
# ----------------------------------------------------------------------


def command_for(widget: QWidget) -> str | None:
    """The command a control stands for, or ``None`` if it has no name to go by.

    A widget may say outright which command it speaks for; a copy speaks for
    whatever the control it was copied from speaks for; anything else speaks
    for itself, if it was registered under an id when its panel was built.
    """
    named = widget.property(COMMAND_PROPERTY)
    if isinstance(named, str) and named:
        return named
    source = widget.property(SOURCE_PROPERTY)
    if isinstance(source, str) and source:
        original = lookup(source)
        if original is not None and original is not widget:
            return command_for(original)
        return CONTROL_PREFIX + source
    own = element_id(widget)
    return CONTROL_PREFIX + own if own else None


def control_of(command_id: str) -> QWidget | None:
    """The live control a control command names, if the window still has it."""
    if not command_id.startswith(CONTROL_PREFIX):
        return None
    return lookup(command_id[len(CONTROL_PREFIX) :])


def describe(hotkeys: HotkeyStore, command_id: str) -> str:
    """What a command is called, for a list or a question about it."""
    command = hotkeys.map.command(command_id)
    if command is not None:
        return command.label
    control = control_of(command_id)
    if control is not None:
        return caption_for(control) or command_id
    return command_id


def group_of(hotkeys: HotkeyStore, command_id: str) -> str:
    command = hotkeys.map.command(command_id)
    if command is not None and command.group:
        return command.group
    if command_id.startswith(CONTROL_PREFIX):
        prefix = command_id[len(CONTROL_PREFIX) :].split(".", 1)[0]
        return "Panels" if prefix == "dock" else prefix.replace("_", " ").title()
    return ""


def listed(hotkeys: HotkeyStore) -> list[str]:
    """The commands worth a row in the editor, in the order they are shown.

    Every command the window declared, and every control the artist has put
    a key on -- but not every button in every panel, of which there are
    hundreds, and for which the gesture is the way in.  Grouped as the menus
    are, and the panels' controls after them.
    """
    ids = {command.id for command in hotkeys.map.commands()}
    ids.update(one for one in hotkeys.map.bound() if one.startswith(CONTROL_PREFIX))
    return sorted(
        ids,
        key=lambda one: (
            one.startswith(CONTROL_PREFIX),
            group_of(hotkeys, one).lower(),
            describe(hotkeys, one).lower(),
        ),
    )


def tip_for(keys: str) -> str:
    """What a tooltip says about a key."""
    return f"Hotkey: {spoken(keys)}" if keys else ""


def decorate(widget: QWidget, keys: str) -> None:
    """Write a control's key into its tooltip, or take the old one out.

    The line is added under whatever the tooltip already said and remembered
    on the widget, so that the next time round it is the line and not the
    sentence above it that gets replaced -- a tooltip the panel rewrites in
    the meantime keeps its new words.
    """
    tip = widget.toolTip()
    previous = widget.property(_TIP_PROPERTY)
    if isinstance(previous, str) and previous and tip.endswith(previous):
        tip = tip[: -len(previous)].rstrip("\n")
    line = tip_for(keys)
    widget.setProperty(_TIP_PROPERTY, line)
    widget.setToolTip(f"{tip}\n{line}" if tip and line else tip or line)


def press(widget: QWidget | None) -> bool:
    """Do to a control what a click would; says whether there was one to do it to."""
    if not isinstance(widget, QAbstractButton) or not widget.isEnabled():
        return False
    widget.click()
    return True


# ----------------------------------------------------------------------
# Binding the map to one window
# ----------------------------------------------------------------------


class HotkeyBinder(QObject):
    """Turns the map into the shortcuts of one window, and keeps them current."""

    def __init__(self, window: QWidget, view: QWidget, hotkeys: HotkeyStore) -> None:
        super().__init__(window)
        self._window = window
        self._view = view
        self._hotkeys = hotkeys
        #: Menu entries, which carry their own keys.
        self._actions: dict[str, QAction] = {}
        #: Entries whose keys are shown in the text rather than carried,
        #: because the keys are scoped to the view.
        self._captioned: dict[str, tuple[QAction, str]] = {}
        #: Everything answered by a shortcut of the binder's own.
        self._slots: dict[str, Callable[[], None]] = {}
        self._shortcuts: dict[str, QShortcut] = {}
        #: Keys on the panels' controls, by command id.
        self._controls: dict[str, QShortcut] = {}
        hotkeys.changed.connect(self.rebind)
        # A button made after the window was -- a tab's switch, a copy
        # dropped into a panel -- gets its key written in as it arrives.
        KeyGesture.instance().watched.connect(self.decorate)

    # -- declaring ------------------------------------------------------

    def add_action(
        self, command_id: str, label: str, action: QAction, default: str = "", group: str = ""
    ) -> None:
        """A menu entry.  Its keys are heard anywhere in the window and shown in the menu."""
        self._hotkeys.declare(Command(command_id, label, normalize(default), "window", group))
        self._actions[command_id] = action

    def add_view_key(
        self,
        command_id: str,
        label: str,
        slot: Callable[[], None],
        default: str,
        action: QAction | None = None,
        group: str = "View",
    ) -> None:
        """A key heard only while the view has the focus.

        The menu entry for it, if there is one, shows the keys in its text
        instead of carrying them: an entry that carried them would answer
        anywhere in the window, which is exactly what a single letter must
        not do while somebody is typing a name.
        """
        self._hotkeys.declare(Command(command_id, label, normalize(default), "view", group))
        self._slots[command_id] = slot
        if action is not None:
            self._captioned[command_id] = (action, action.text())

    def add_key(
        self,
        command_id: str,
        label: str,
        slot: Callable[[], None],
        default: str,
        group: str = "",
    ) -> None:
        """A key heard anywhere in the window, with no menu entry of its own."""
        self._hotkeys.declare(Command(command_id, label, normalize(default), "window", group))
        self._slots[command_id] = slot

    # -- keeping the shortcuts current ------------------------------------

    def rebind(self) -> None:
        """Put every command's keys where they are heard.  Cheap; run on any change."""
        hotkeys = self._hotkeys
        for command_id, action in self._actions.items():
            action.setShortcut(QKeySequence(hotkeys.keys_for(command_id)))
        for command_id, (action, text) in self._captioned.items():
            keys = spoken(hotkeys.keys_for(command_id))
            action.setText(f"{text}  ({keys})" if keys else text)
        for command_id, slot in self._slots.items():
            self._own(command_id, slot).setKey(QKeySequence(hotkeys.keys_for(command_id)))
        wanted = {
            command_id: keys
            for command_id, keys in hotkeys.map.bound().items()
            if command_id.startswith(CONTROL_PREFIX)
        }
        for command_id in [one for one in self._controls if one not in wanted]:
            stale = self._controls.pop(command_id)
            stale.setEnabled(False)
            stale.setParent(None)
            stale.deleteLater()
        for command_id, keys in wanted.items():
            shortcut = self._controls.get(command_id)
            if shortcut is None:
                shortcut = QShortcut(self._window)
                shortcut.setContext(Qt.ShortcutContext.WindowShortcut)
                shortcut.activated.connect(
                    lambda command_id=command_id: press(control_of(command_id))
                )
                self._controls[command_id] = shortcut
            shortcut.setKey(QKeySequence(keys))
        for widget in self._window.findChildren(QAbstractButton):
            self.decorate(widget)

    def decorate(self, widget: QWidget) -> None:
        """Say in a control's tooltip what key it answers to, if it is one of ours.

        A copy is left to the copier, which keeps its tooltip in step with
        the control it copies -- and that one has the key written in.
        """
        if not can_take_key(widget) or widget.property(SOURCE_PROPERTY):
            return
        command_id = command_for(widget)
        if command_id is None:
            return
        keys = self._hotkeys.keys_for(command_id)
        decorate(widget, keys)
        # A panel's button that arms a tool says the tool's letter after its
        # name, as the menu entry does, and for the same reason: the letter
        # is the artist's to change, so the button cannot have it baked in.
        command = self._hotkeys.map.command(command_id)
        if command is not None and command.scope == "view" and isinstance(widget, QAbstractButton):
            base = widget.property(_TEXT_PROPERTY)
            if not isinstance(base, str):
                base = widget.text()
                widget.setProperty(_TEXT_PROPERTY, base)
            widget.setText(f"{base}  ({spoken(keys)})" if keys else base)

    def _own(self, command_id: str, slot: Callable[[], None]) -> QShortcut:
        shortcut = self._shortcuts.get(command_id)
        if shortcut is None:
            command = self._hotkeys.map.command(command_id)
            if command is not None and command.scope == "view":
                shortcut = QShortcut(self._view)
                shortcut.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
            else:
                shortcut = QShortcut(self._window)
                shortcut.setContext(Qt.ShortcutContext.WindowShortcut)
            shortcut.activated.connect(slot)
            self._shortcuts[command_id] = shortcut
        return shortcut

    def shortcut(self, command_id: str) -> QShortcut | None:
        """The shortcut answering for a command, for a test that wants to press it."""
        return self._shortcuts.get(command_id) or self._controls.get(command_id)


# ----------------------------------------------------------------------
# Asking for a key
# ----------------------------------------------------------------------


class KeyBox(QKeySequenceEdit):
    """A box that takes one keystroke and says when it has one, or has none.

    Qt's box says when a key has been entered but not when its clear button
    has been pressed -- that only changes the sequence, and it changes the
    sequence the same way at the start of every keystroke, since a new key
    begins by wiping the old.  So an emptying is taken as a clearing only if
    the box is still empty once the event that emptied it has run its course.
    """

    #: The keys the box now holds, portable text, ``""`` for none.
    committed = Signal(str)

    def __init__(self, keys: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMaximumSequenceLength(1)
        self.setClearButtonEnabled(True)
        self._held = ""
        self.hold(keys)
        self.editingFinished.connect(self._finished)
        self.keySequenceChanged.connect(self._changed)

    def hold(self, keys: str) -> None:
        """Show ``keys`` without that counting as the artist entering them."""
        self._held = normalize(keys)
        self.setKeySequence(QKeySequence(self._held))

    def _finished(self) -> None:
        keys = normalize(self.keySequence())
        if keys != self._held:
            self._held = keys
            self.committed.emit(keys)

    def _changed(self, sequence: QKeySequence) -> None:
        if sequence.isEmpty() and self._held:
            QTimer.singleShot(0, self._maybe_cleared)

    def _maybe_cleared(self) -> None:
        if self.keySequence().isEmpty() and self._held:
            self._held = ""
            self.committed.emit("")


class HotkeyDialog(QDialog):
    """One keystroke for one command, and the question if it is already taken."""

    def __init__(self, hotkeys: HotkeyStore, command_id: str, parent: QWidget | None = None):
        super().__init__(parent)
        self._hotkeys = hotkeys
        self._command = command_id
        self._label = describe(hotkeys, command_id)
        self.setWindowTitle("Assign Hotkey")
        self.setModal(True)

        column = QVBoxLayout(self)
        column.setContentsMargins(14, 12, 14, 12)
        column.setSpacing(8)
        prompt = QLabel(f"Press the key for <b>{self._label}</b>.")
        prompt.setWordWrap(True)
        self._edit = KeyBox(hotkeys.keys_for(command_id))
        note = QLabel("Clear the box, or assign it empty, to take the current key away.")
        note.setWordWrap(True)
        note.setStyleSheet("color: palette(mid);")
        self._buttons = QDialogButtonBox()
        self._assign = self._buttons.addButton("Assign", QDialogButtonBox.ButtonRole.AcceptRole)
        self._buttons.addButton(QDialogButtonBox.StandardButton.Cancel)
        self._buttons.accepted.connect(self._commit)
        self._buttons.rejected.connect(self.reject)
        self._edit.committed.connect(self._take)
        column.addWidget(prompt)
        column.addWidget(self._edit)
        column.addWidget(note)
        column.addWidget(self._buttons)
        self._edit.setFocus()

    def _commit(self) -> None:
        self._take(normalize(self._edit.keySequence()))

    def _take(self, keys: str) -> None:
        if assign(self._hotkeys, self._command, keys, self):
            self.accept()


def assign(hotkeys: HotkeyStore, command_id: str, keys: str, parent: QWidget | None) -> bool:
    """Put ``keys`` on a command, asking first if they are on something else.

    Returns whether the assignment went through.  ``""`` takes the command's
    keys away, which needs no asking.
    """
    keys = normalize(keys)
    holder = hotkeys.holder_of(keys) if keys else None
    if holder is not None and holder != command_id:
        answer = QMessageBox.question(
            parent,
            "Hotkey Already Assigned",
            f"{spoken(keys)} already does <b>{describe(hotkeys, holder)}</b>.<br><br>"
            f"Take it away from that and put it on <b>{describe(hotkeys, command_id)}</b>?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return False
    hotkeys.assign(command_id, keys)
    return True


def ask_for(widget: QWidget, hotkeys: HotkeyStore, parent: QWidget | None = None) -> bool:
    """The gesture's other half: a key for whatever control was Ctrl-Alt-clicked.

    Returns whether there was a command to ask about.  A control that was
    never registered -- a button in a dialog, say -- has no name a key could
    be written down against, and is left alone.
    """
    command_id = command_for(widget)
    if command_id is None:
        return False
    if hotkeys.map.command(command_id) is None:
        hotkeys.declare(
            Command(
                command_id,
                caption_for(widget) or command_id,
                "",
                "window",
                group_of(hotkeys, command_id),
            )
        )
    HotkeyDialog(hotkeys, command_id, parent or widget.window()).exec()
    return True
