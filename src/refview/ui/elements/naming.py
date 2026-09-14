"""Names for the controls, so that a copy of one can be written down.

A cloned control has to survive the application closing, and what gets written
into the settings file cannot be the control itself -- it has to be a name
that finds the control again next time.  Panels are built in code and nothing
in them was ever named, so the names are worked out here, once, after a panel
has finished building itself.  That way ten panels get stable names without
ten panels having to remember to hand them out.

A control is named after the attribute it was stored on: ``self._offset`` in
the section panel becomes ``section.offset``.  That is a name someone reading
the panel would recognise, it is already unique within the panel, and it only
changes when the attribute is renamed -- at which point a saved copy of it
pointing at nothing is the correct outcome, because the control it pointed at
is gone.

What is left over -- a frame built as a local, a button handed straight to a
row -- is named after its title or its text, and anything still nameless after
that is numbered in the order the tree walks it.  Numbering is the weakest of
the three: inserting a control ahead of a numbered one renames it.  So the
numbers are a floor, not the plan, and a control worth copying is worth
storing on an attribute.
"""

from __future__ import annotations

import re
from weakref import WeakValueDictionary

from PySide6.QtWidgets import QAbstractButton, QFormLayout, QGroupBox, QLabel, QWidget

from .frame import Frame

#: Every named control in the window, by its full id.  Weak, so that closing a
#: custom panel does not keep the controls it copied alive.
_REGISTRY: WeakValueDictionary[str, QWidget] = WeakValueDictionary()


def slug(text: str) -> str:
    """A name out of a piece of prose: lower case, words joined by ``_``."""
    cleaned = re.sub(r"[^a-z0-9]+", "_", text.strip().lower())
    return cleaned.strip("_") or "item"


def name_tree(root: QWidget, owner: object | None = None) -> None:
    """Give everything under ``root`` an object name, if it has not got one.

    ``owner`` is the object whose attributes the controls were stored on --
    the panel itself, usually.  Run once, after the panel has built.
    """
    by_widget: dict[int, str] = {}
    if owner is not None:
        for attribute, value in vars(owner).items():
            if isinstance(value, QWidget):
                by_widget[id(value)] = slug(attribute)

    everything = [root, *root.findChildren(QWidget)]
    taken = {widget.objectName() for widget in everything if widget.objectName()}
    waiting = [widget for widget in everything if not widget.objectName()]

    # Three passes, weakest last, so that the strongest claim on a name gets
    # it: a control stored on ``self._mode`` is ``mode``, and the group titled
    # "Mode" that happens to hold it settles for ``mode_2``.  One pass in tree
    # order would hand the name to whichever came first, which is a name that
    # moves when a group is renamed.
    for pick in (
        lambda widget: by_widget.get(id(widget)),
        _named_after,
        lambda widget: slug(type(widget).__name__),
    ):
        for widget in waiting:
            if widget.objectName():
                continue
            wanted = pick(widget)
            if not wanted:
                continue
            widget.setObjectName(_free(wanted, taken))


def _free(wanted: str, taken: set[str]) -> str:
    """``wanted`` if nothing has it, else the same with a number after it."""
    name = wanted
    suffix = 2
    while name in taken:
        name = f"{wanted}_{suffix}"
        suffix += 1
    taken.add(name)
    return name


def _named_after(widget: QWidget) -> str | None:
    """A name read off whatever the widget already says on it."""
    if isinstance(widget, Frame):
        return slug(widget.title())
    if isinstance(widget, QGroupBox) and widget.title():
        return slug(widget.title())
    if isinstance(widget, QAbstractButton) and widget.text():
        return slug(widget.text())
    return None


def register(root: QWidget, prefix: str) -> None:
    """Record everything under ``root`` under ``prefix.<object name>``."""
    for widget in [root, *root.findChildren(QWidget)]:
        name = widget.objectName()
        if name:
            _REGISTRY[f"{prefix}.{name}"] = widget


def element_id(widget: QWidget) -> str | None:
    """The id a widget was registered under, or ``None`` if it was not."""
    for key, known in list(_REGISTRY.items()):
        if known is widget:
            return key
    return None


def lookup(element_id: str) -> QWidget | None:
    """The control an id names, if the window still has it."""
    return _REGISTRY.get(element_id)


def forget(prefix: str) -> None:
    """Drop every id under a prefix; for a panel that has been thrown away."""
    for key in [key for key in _REGISTRY if key.split(".", 1)[0] == prefix]:
        _REGISTRY.pop(key, None)


def caption_for(widget: QWidget) -> str:
    """What a control is called, read off the row it sits in.

    A copy of a control taken out of its panel arrives somewhere with none of
    the context that told you what it was, so it has to bring its caption with
    it.  Most controls sit in a form row whose left-hand side is exactly that
    caption; the rest say it on themselves, or fall back to their id.
    """
    for candidate in (
        _asked(widget, "caption"),
        _row_label(widget),
        _asked(widget, "text"),
        _from_id(widget),
    ):
        if candidate:
            return candidate
    return ""


def _asked(widget: QWidget, method: str) -> str:
    """What a widget answers when asked its own name, if it answers at all.

    A slider is asked for its caption and not for its ``text``, which is the
    number it is currently showing -- a caption read off that would be a name
    that changed every time the control was dragged.
    """
    if method == "text" and hasattr(widget, "caption"):
        return ""
    answer = getattr(widget, method, None)
    if not callable(answer):
        return ""
    given = answer()
    return given.strip() if isinstance(given, str) else ""


def _row_label(widget: QWidget) -> str:
    """The caption down the left of the form row the control sits in."""
    node: QWidget | None = widget
    while node is not None:
        parent = node.parentWidget()
        if parent is None:
            return ""
        layout = parent.layout()
        if isinstance(layout, QFormLayout):
            for row in range(layout.rowCount()):
                field = layout.itemAt(row, QFormLayout.ItemRole.FieldRole)
                if field is not None and field.widget() is node:
                    label = layout.itemAt(row, QFormLayout.ItemRole.LabelRole)
                    holder = label.widget() if label is not None else None
                    if isinstance(holder, QLabel):
                        return holder.text().strip()
                    return ""
        node = parent
    return ""


def _from_id(widget: QWidget) -> str:
    """A name made out of the id, for a control that answers to nothing else."""
    identifier = element_id(widget)
    if not identifier:
        return ""
    return identifier.rsplit(".", 1)[-1].replace("_", " ").capitalize()
