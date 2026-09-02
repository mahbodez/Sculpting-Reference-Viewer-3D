"""The handful of undoable edits the whole application is built from.

Measurements, annotations and camera bookmarks are all ordered lists of plain
objects, so four generic commands cover every edit the UI makes.  Adding a new
kind of document object needs no new command type.
"""

from __future__ import annotations

from typing import Any

from .history import Command


class SetAttributes(Command):
    """Assign one or more attributes on an object, remembering the old values.

    ``previous`` exists for gestures that edit the object live and only record
    the step when the mouse is released; they pass the values captured before
    the drag started.
    """

    def __init__(
        self,
        target: Any,
        changes: dict[str, Any],
        text: str = "Edit",
        channel: str = "",
        previous: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(text, channel)
        self._target = target
        self._new = dict(changes)
        self._old = (
            dict(previous)
            if previous is not None
            else {name: getattr(target, name) for name in changes}
        )

    def apply(self) -> None:
        self._assign(self._new)

    def revert(self) -> None:
        self._assign(self._old)

    def _assign(self, values: dict[str, Any]) -> None:
        for name, value in values.items():
            setattr(self._target, name, value)


class AddItem(Command):
    """Append an item to a document list."""

    def __init__(self, items: list, item: Any, text: str = "Add", channel: str = "") -> None:
        super().__init__(text, channel)
        self._items = items
        self._item = item

    def apply(self) -> None:
        self._items.append(self._item)

    def revert(self) -> None:
        if self._items and self._items[-1] is self._item:
            self._items.pop()
        elif self._item in self._items:
            self._items.remove(self._item)


class RemoveItem(Command):
    """Delete the item at ``index``, putting it back in place on undo."""

    def __init__(self, items: list, index: int, text: str = "Delete", channel: str = "") -> None:
        super().__init__(text, channel)
        self._items = items
        self._index = index
        self._item = items[index]

    def apply(self) -> None:
        del self._items[self._index]

    def revert(self) -> None:
        self._items.insert(self._index, self._item)


class ReplaceItems(Command):
    """Swap the whole contents of a document list.

    Used for bulk edits -- clearing the list, or an eraser stroke that rewrites
    several strokes at once -- where tracking individual moves would be more
    machinery than the operation is worth.
    """

    def __init__(
        self,
        items: list,
        new_items: list,
        text: str = "Replace",
        channel: str = "",
        previous: list | None = None,
    ) -> None:
        super().__init__(text, channel)
        self._items = items
        self._new = list(new_items)
        self._old = list(items if previous is None else previous)

    def apply(self) -> None:
        self._items[:] = self._new

    def revert(self) -> None:
        self._items[:] = self._old
