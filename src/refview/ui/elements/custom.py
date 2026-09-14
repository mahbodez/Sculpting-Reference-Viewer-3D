"""A panel the artist builds, out of copies of controls from the fixed ones.

The panels that come with the application are organised by subject, because
that is the only way to organise controls for someone who has not arrived yet.
A session is organised by task, and the three or four controls a task keeps
reaching for are hardly ever the three that share a subject: a pass of
blocking-in wants the ghost slider, the form opacity and the section offset,
which live in three different panels two clicks apart.

So: Alt-drag those three here and they stand together, still driving the
controls they came from.  The panel is a column of named groups and the groups
hold rows, which is the same shape as every other panel -- what is different is
that this one is arranged by hand, and that it can be thrown away when the task
is done without losing anything, because nothing here is the original.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFormLayout,
    QInputDialog,
    QLabel,
    QMenu,
    QWidget,
)

from . import palette
from .clone import HOLDER_PROPERTY, carried, clone, in_flight, watch_tree
from .clone import source_of as clone_source
from .frame import Frame, frame_form
from .naming import caption_for, lookup
from .reflow import Reflow

#: The group a copy lands in when it was not dropped on one.
DEFAULT_GROUP = "Controls"


class CustomPanel(Reflow):
    """A panel of copied controls, arranged by hand."""

    #: Anything that changes what would be written down: a copy added, moved,
    #: removed, a group renamed.  The window listens so the layout is saved.
    changed = Signal()

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._title = title
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._menu_at)
        self._hint = QLabel(
            "Alt-drag a control from any panel and drop it here.", self
        )
        self._hint.setWordWrap(True)
        self._hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._hint.setStyleSheet(f"color: {palette.css(palette.INK_DIM)};")
        self.add(self._hint)

    # -- what it is ------------------------------------------------------

    def title(self) -> str:
        return self._title

    def set_title(self, title: str) -> None:
        self._title = title
        self.changed.emit()

    def frames(self) -> list[Frame]:
        layout = self.reflow()
        found = []
        for index in range(layout.count()):
            item = layout.itemAt(index)
            widget = item.widget() if item is not None else None
            if isinstance(widget, Frame):
                found.append(widget)
        return found

    def is_empty(self) -> bool:
        return not any(_rows_of(frame) for frame in self.frames())

    # -- building it -----------------------------------------------------

    def add_frame(self, title: str, expanded: bool = True) -> Frame:
        """A new named group, empty, at the end of the panel."""
        frame = Frame(title, expanded)
        frame_form(frame.body())
        self.add(frame)
        self._retune()
        self.changed.emit()
        return frame

    def take(self, source: QWidget, frame: Frame | None = None, row: int = -1) -> QWidget | None:
        """Put a copy of ``source`` into this panel."""
        copy = clone(source)
        if copy is None:
            return None
        caption = caption_for(source)
        if isinstance(copy, Frame):
            self.insert(self._row_at_end(), copy)
            watch_tree(copy)
            copy.setProperty(HOLDER_PROPERTY, True)
            self._retune()
            self.changed.emit()
            return copy
        target = frame or self._default_frame()
        self._put(target, copy, caption, row)
        return copy

    def _put(self, frame: Frame, copy: QWidget, caption: str, row: int) -> None:
        form = frame.body().layout()
        if not isinstance(form, QFormLayout):
            form = frame_form(frame.body())
        copy.setProperty(HOLDER_PROPERTY, True)
        label: QLabel | None = None
        if caption and not _speaks_for_itself(copy):
            label = QLabel(caption)
            label.setToolTip(caption)
        at = form.rowCount() if row < 0 else min(row, form.rowCount())
        if label is not None:
            form.insertRow(at, label, copy)
            copy._refview_row_label = label  # noqa: SLF001 - see Link.refresh
        else:
            form.insertRow(at, copy)
        watch_tree(copy)
        self._retune()
        self.changed.emit()

    def drop_holder(self, holder: QWidget) -> None:
        """Take a copy out of this panel and destroy it."""
        _detach(holder)
        holder.setParent(None)
        holder.deleteLater()
        self._retune()
        self.changed.emit()

    def move_holder(self, holder: QWidget, frame: Frame | None, row: int) -> None:
        """Move a copy already in a panel to a new place in this one.

        ``frame`` and ``row`` say where the drop landed among the rows.  A
        whole group ignores both and goes in among the groups instead, ahead
        of whichever one was dropped on -- it is not a row and cannot be put
        between two.
        """
        if isinstance(holder, Frame):
            # Where the target sits is read after the moved group has been
            # taken out, since taking it out shifts everything after it.
            _detach(holder)
            before = self.reflow().index_of(frame) if frame is not None else -1
            self.insert(before if before >= 0 else self._row_at_end(), holder)
            self._retune()
            self.changed.emit()
            return
        caption = ""
        label = getattr(holder, "_refview_row_label", None)
        if isinstance(label, QLabel):
            caption = label.text()
        _detach(holder)
        self._put(frame or self._default_frame(), holder, caption, row)

    # -- where a drop lands ----------------------------------------------

    def _default_frame(self) -> Frame:
        existing = self.frames()
        if existing:
            return existing[-1]
        return self.add_frame(DEFAULT_GROUP)

    def _row_at_end(self) -> int:
        return self.reflow().count()

    def frame_at(self, point) -> Frame | None:
        """The group under a point in the panel, if there is one."""
        node = self.childAt(point)
        while node is not None and node is not self:
            if isinstance(node, Frame):
                return node
            node = node.parentWidget()
        return None

    def row_at(self, frame: Frame, point) -> int:
        """Which row of a group a drop at ``point`` should become."""
        form = frame.body().layout()
        if not isinstance(form, QFormLayout):
            return -1
        local = frame.body().mapFrom(self, point)
        for row in range(form.rowCount()):
            item = form.itemAt(row, QFormLayout.ItemRole.FieldRole) or form.itemAt(
                row, QFormLayout.ItemRole.SpanningRole
            )
            widget = item.widget() if item is not None else None
            if widget is None:
                continue
            middle = widget.geometry().center().y()
            if local.y() < middle:
                return row
        return form.rowCount()

    # -- drops -----------------------------------------------------------

    def dragEnterEvent(self, event) -> None:  # noqa: N802 - Qt contract
        if carried(event.mimeData()) is None:
            event.ignore()
            return
        event.acceptProposedAction()

    def dragMoveEvent(self, event) -> None:  # noqa: N802 - Qt contract
        if carried(event.mimeData()) is None:
            event.ignore()
            return
        event.acceptProposedAction()

    def dropEvent(self, event) -> None:  # noqa: N802 - Qt contract
        note = carried(event.mimeData())
        if note is None:
            event.ignore()
            return
        point = event.position().toPoint()
        frame = self.frame_at(point)
        row = self.row_at(frame, point) if frame is not None else -1

        moving = in_flight()
        if note.get("moving") and moving is not None:
            self.move_holder(moving, frame, row)
            event.acceptProposedAction()
            return

        source = lookup(str(note.get("element") or ""))
        if source is None:
            event.ignore()
            return
        self.take(source, frame, row)
        event.acceptProposedAction()

    # -- the menu --------------------------------------------------------

    def _menu_at(self, point) -> None:
        menu = QMenu(self)
        frame = self.frame_at(point)
        menu.addAction("New Group...", self._ask_for_frame)
        if frame is not None:
            menu.addAction("Rename Group...", lambda: self._rename(frame))
            menu.addAction("Remove Group", lambda: self._remove(frame))
        menu.addSeparator()
        menu.addAction("Rename Panel...", self._ask_for_title)
        menu.addAction("Empty the Panel", self.clear)
        menu.exec(self.mapToGlobal(point))

    def _ask_for_frame(self) -> None:
        title, taken = QInputDialog.getText(self, "New Group", "Name")
        if taken and title.strip():
            self.add_frame(title.strip())

    def _ask_for_title(self) -> None:
        title, taken = QInputDialog.getText(
            self, "Rename Panel", "Name", text=self._title
        )
        if taken and title.strip():
            self.set_title(title.strip())

    def _rename(self, frame: Frame) -> None:
        title, taken = QInputDialog.getText(
            self, "Rename Group", "Name", text=frame.title()
        )
        if taken and title.strip():
            frame.set_title(title.strip())
            self.changed.emit()

    def _remove(self, frame: Frame) -> None:
        self.reflow().removeWidget(frame)
        frame.setParent(None)
        frame.deleteLater()
        self._retune()
        self.changed.emit()

    def clear(self) -> None:
        for frame in self.frames():
            self.reflow().removeWidget(frame)
            frame.setParent(None)
            frame.deleteLater()
        self._retune()
        self.changed.emit()

    # -- housekeeping ----------------------------------------------------

    def _retune(self) -> None:
        """Show the invitation only while there is nothing else to show."""
        self._hint.setVisible(self.is_empty())
        self.reflow().invalidate()
        self._settle()

    # -- writing it down --------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "title": self._title,
            "groups": [
                {
                    "title": frame.title(),
                    "expanded": frame.is_expanded(),
                    "rows": _rows_of(frame),
                }
                for frame in self.frames()
            ],
        }

    def restore(self, data: dict) -> None:
        """Rebuild the panel from what :meth:`to_dict` wrote.

        A row naming a control the application no longer has is skipped, not
        an error: panels get reorganised between versions, and a saved layout
        that mostly still works is worth more than one that refuses to load.
        """
        self.clear()
        self._title = str(data.get("title") or self._title)
        for group in data.get("groups") or []:
            frame = self.add_frame(
                str(group.get("title") or DEFAULT_GROUP),
                bool(group.get("expanded", True)),
            )
            for row in group.get("rows") or []:
                source = lookup(str(row.get("element") or ""))
                if source is not None:
                    self.take(source, frame)
        self._retune()


def _rows_of(frame: Frame) -> list[dict]:
    """What a group holds, as ids that can be looked up again."""
    form = frame.body().layout()
    if not isinstance(form, QFormLayout):
        return []
    rows = []
    for row in range(form.rowCount()):
        item = form.itemAt(row, QFormLayout.ItemRole.FieldRole) or form.itemAt(
            row, QFormLayout.ItemRole.SpanningRole
        )
        widget = item.widget() if item is not None else None
        if widget is None:
            continue
        element = clone_source(widget)
        if element:
            rows.append({"element": element})
    return rows


def _speaks_for_itself(widget: QWidget) -> bool:
    """Whether a control already says what it is, so needs no caption.

    Three do.  A group has its name on its bar.  A check box or a button has
    its words written across it.  And a slider carries its caption inside the
    bar it draws, which is the whole reason it draws one -- putting a caption
    beside it as well would be the name twice on one row.

    Everything else -- a list of choices, a swatch, a point -- is a control
    with nothing on it, and arrives from a panel where what it was called was
    written down the left of its row.  That is the caption it brings with it.
    """
    if isinstance(widget, Frame) or hasattr(widget, "caption"):
        return True
    text = getattr(widget, "text", None)
    return callable(text) and bool(str(text() or "").strip())


def _detach(holder: QWidget) -> None:
    """Take a copy out of whatever row or column currently holds it."""
    label = getattr(holder, "_refview_row_label", None)
    parent = holder.parentWidget()
    form = parent.layout() if parent is not None else None
    if isinstance(form, QFormLayout):
        index = _row_index(form, holder)
        if index >= 0:
            form.takeRow(index)
            if isinstance(label, QLabel):
                label.setParent(None)
                label.deleteLater()
            holder._refview_row_label = None  # noqa: SLF001 - paired with _put
            holder.setParent(None)
            return
    if parent is not None and parent.layout() is not None:
        parent.layout().removeWidget(holder)
    holder.setParent(None)


def _row_index(form: QFormLayout, widget: QWidget) -> int:
    for row in range(form.rowCount()):
        item = form.itemAt(row, QFormLayout.ItemRole.FieldRole) or form.itemAt(
            row, QFormLayout.ItemRole.SpanningRole
        )
        if item is not None and item.widget() is widget:
            return row
    return -1
