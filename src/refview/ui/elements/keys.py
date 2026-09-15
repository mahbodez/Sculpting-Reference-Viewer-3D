"""The gesture that puts a key on a control: Ctrl/Cmd, Alt and a click.

It sits beside the copying gesture and is built the same way, for the same
reason: Alt and a drag copies a control, so Ctrl and Alt and a click on one
is where a key gets assigned, and both have to take the press away from the
control before the control acts on it.  Ctrl-Alt-clicking a checkbox must not
also tick the checkbox.

What happens after the click is not decided here.  The gesture only says
which widget was pointed at, and the window -- which has the hotkey store,
the dialog and the status bar -- takes it from there.  That keeps this module
free of everything above it, so that the same ``watch_tree`` the copier uses
can install both gestures on a panel without the elements knowing what a
hotkey is.
"""

from __future__ import annotations

from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtWidgets import QAbstractButton, QWidget

#: Property naming the command a widget stands for, where that is not the
#: widget's own id -- the switch on a dock's tab speaks for the same panel as
#: the switch on its bar, and a key put on either belongs to the panel.
COMMAND_PROPERTY = "refview_hotkey_command"

#: The modifiers the gesture wants, and nothing else: Ctrl and Alt together,
#: which on a Mac is Cmd and Option.
_WANTED = Qt.KeyboardModifier.ControlModifier | Qt.KeyboardModifier.AltModifier
_CONSIDERED = _WANTED | Qt.KeyboardModifier.ShiftModifier | Qt.KeyboardModifier.MetaModifier


def is_hotkey_click(event) -> bool:
    """Whether a mouse press is the assignment gesture rather than a click."""
    return (
        event.button() == Qt.MouseButton.LeftButton
        and (event.modifiers() & _CONSIDERED) == _WANTED
    )


def can_take_key(widget: QWidget) -> bool:
    """Whether a widget is the kind a key can sensibly be put on.

    A button or a switch does one thing when pressed, and a key can do that
    thing.  A slider, a list, a colour swatch have no one thing a key could
    mean, and are left to the copier.
    """
    return isinstance(widget, QAbstractButton)


class KeyGesture(QObject):
    """Watches for Ctrl-Alt-click on a button and says which one it was."""

    #: The widget a key was asked for.
    requested = Signal(QWidget)
    #: A widget newly under watch, for whoever writes keys into tooltips.
    watched = Signal(QWidget)

    _instance: KeyGesture | None = None

    def __init__(self) -> None:
        super().__init__()
        self._armed: QWidget | None = None

    @classmethod
    def instance(cls) -> KeyGesture:
        if cls._instance is None:
            cls._instance = KeyGesture()
        return cls._instance

    def watch(self, widget: QWidget) -> None:
        widget.installEventFilter(self)
        self.watched.emit(widget)

    def eventFilter(self, watched, event) -> bool:  # noqa: N802 - Qt contract
        kind = event.type()
        if kind == QEvent.Type.MouseButtonPress:
            if is_hotkey_click(event) and isinstance(watched, QWidget) and can_take_key(watched):
                self._armed = watched
                return True
        elif kind == QEvent.Type.MouseButtonRelease and self._armed is watched:
            # The press was taken away from the control, so the release has
            # to be too, or the control sees half a click and acts on it.
            self._armed = None
            if watched.rect().contains(event.position().toPoint()):
                self.requested.emit(watched)
            return True
        elif kind == QEvent.Type.Leave and self._armed is watched:
            self._armed = None
        return False


def watch_keys(root: QWidget) -> None:
    """Make every button and switch under ``root`` answer to the gesture."""
    gesture = KeyGesture.instance()
    for widget in [root, *root.findChildren(QWidget)]:
        if can_take_key(widget):
            gesture.watch(widget)
