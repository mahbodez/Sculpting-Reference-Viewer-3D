"""Undo/redo stack.

Every document edit is expressed as a :class:`Command` that knows how to apply
and revert itself, which keeps the undo logic out of the widgets: a panel
builds a command, hands it to the history, and the history decides what the
document looks like.

Camera motion is deliberately *not* recorded.  Orbiting is a continuous
gesture rather than an edit, and burying real changes under a hundred camera
steps is exactly what makes undo useless in a 3D viewer.
"""

from __future__ import annotations

#: Names of the document channels a command can change, used by the UI to
#: decide which change signal to emit.
MEASUREMENTS = "measurements"
ANNOTATIONS = "annotations"
BOOKMARKS = "bookmarks"
ARMATURE = "armature"


class Command:
    """One reversible change, named for the undo menu."""

    def __init__(self, text: str = "Change", channel: str = "") -> None:
        self.text = text
        self.channel = channel

    def apply(self) -> None:  # pragma: no cover - overridden
        raise NotImplementedError

    def revert(self) -> None:  # pragma: no cover - overridden
        raise NotImplementedError

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"<{type(self).__name__} {self.text!r}>"


class History:
    """A bounded undo/redo stack."""

    def __init__(self, limit: int = 200) -> None:
        self._limit = max(int(limit), 1)
        self._undo: list[Command] = []
        self._redo: list[Command] = []

    def push(self, command: Command, apply: bool = True) -> Command:
        """Record ``command``, applying it first unless it already ran.

        Interactive gestures such as dragging a measurement endpoint edit the
        document as they go and pass ``apply=False`` when they commit.
        """
        if apply:
            command.apply()
        self._undo.append(command)
        del self._undo[: -self._limit]
        self._redo.clear()
        return command

    def undo(self) -> Command | None:
        if not self._undo:
            return None
        command = self._undo.pop()
        command.revert()
        self._redo.append(command)
        return command

    def redo(self) -> Command | None:
        if not self._redo:
            return None
        command = self._redo.pop()
        command.apply()
        self._undo.append(command)
        return command

    def clear(self) -> None:
        self._undo.clear()
        self._redo.clear()

    @property
    def can_undo(self) -> bool:
        return bool(self._undo)

    @property
    def can_redo(self) -> bool:
        return bool(self._redo)

    @property
    def undo_text(self) -> str:
        return self._undo[-1].text if self._undo else ""

    @property
    def redo_text(self) -> str:
        return self._redo[-1].text if self._redo else ""
