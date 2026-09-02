"""Projection settings, standard views and named camera bookmarks."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QWidget,
)

from ...core.bookmark import CameraBookmark
from ...core.camera import Projection
from ...core.commands import AddItem, RemoveItem, SetAttributes
from ...core.history import BOOKMARKS
from ...core.linalg import vec3
from ..widgets import SliderSpin, form_group
from .base import Panel

#: Object-to-eye directions for the standard orthographic-style views.
STANDARD_VIEWS = (
    ("Front", vec3(0.0, 0.0, 1.0)),
    ("Back", vec3(0.0, 0.0, -1.0)),
    ("Left", vec3(-1.0, 0.0, 0.0)),
    ("Right", vec3(1.0, 0.0, 0.0)),
    ("Top", vec3(0.0, 1.0, 0.05)),
    ("Bottom", vec3(0.0, -1.0, 0.05)),
)


class CameraPanel(Panel):
    """Edits the projection and manages the saved camera positions."""

    def _build(self) -> None:
        box, form = form_group("Projection")
        self._projection = QComboBox()
        for projection in Projection:
            self._projection.addItem(projection.label, projection.value)
        self._fov = SliderSpin(5.0, 120.0, 40.0, decimals=0, step=1.0, suffix=" deg")
        self._fov.setToolTip(
            "Vertical field of view.  In orthographic mode it still sets the\n"
            "framing, so switching projection keeps the object the same size."
        )
        self._snap = SliderSpin(0.0, 90.0, 15.0, decimals=0, step=5.0, suffix=" deg")
        self._snap.setToolTip(
            "Orbit increment while Shift is held.  0 turns snapping off."
        )
        form.addRow("Type", self._projection)
        form.addRow("FOV", self._fov)
        form.addRow("Shift snap", self._snap)
        self._add(box)

        views_box, _ = form_group("Standard Views")
        grid = QGridLayout()
        grid.setSpacing(4)
        for index, (label, direction) in enumerate(STANDARD_VIEWS):
            button = QPushButton(label)
            button.clicked.connect(lambda _=False, d=direction: self.look_along(d))
            grid.addWidget(button, index // 3, index % 3)
        frame = QPushButton("Frame Object  (F)")
        frame.clicked.connect(self._frame)
        grid.addWidget(frame, 2, 0, 1, 3)
        views_box.layout().addRow(grid)
        self._add(views_box)

        bookmarks_box, _ = form_group("Saved Views")
        self._list = QListWidget()
        self._list.setAlternatingRowColors(True)
        self._list.setToolTip("Click to jump there; double-click the name to rename it.")
        self._list.itemClicked.connect(self._recall_item)
        self._list.itemChanged.connect(self._rename_item)
        bookmarks_box.layout().addRow(self._list)

        buttons = QWidget()
        row = QHBoxLayout(buttons)
        row.setContentsMargins(0, 0, 0, 0)
        for label, slot, tip in (
            ("Save", self.save_current_view, "Store the current camera as a new view (Ctrl+B)"),
            ("Update", self._update, "Overwrite the selected view with the current camera"),
            ("Rename", self.rename_selected, "Edit the selected view's name (F2)"),
            ("Delete", self._delete, "Remove the selected view"),
        ):
            button = QPushButton(label)
            button.setToolTip(tip)
            button.clicked.connect(slot)
            row.addWidget(button)
        bookmarks_box.layout().addRow(buttons)

        cycle = QWidget()
        cycle_row = QHBoxLayout(cycle)
        cycle_row.setContentsMargins(0, 0, 0, 0)
        previous = QPushButton("< Previous  ([)")
        previous.clicked.connect(lambda: self.cycle(-1))
        following = QPushButton("Next  (])  >")
        following.clicked.connect(lambda: self.cycle(1))
        cycle_row.addWidget(previous)
        cycle_row.addWidget(following)
        bookmarks_box.layout().addRow(cycle)
        self._add(bookmarks_box)
        self._add_stretch()

        self._projection.currentIndexChanged.connect(self._on_projection)
        self._fov.valueChanged.connect(self._on_fov)
        self._snap.valueChanged.connect(self._on_snap)

        # Scoped to the panel so F2 keeps its usual meaning everywhere else.
        rename = QShortcut(QKeySequence("F2"), self)
        rename.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
        rename.activated.connect(self.rename_selected)

    # -- projection -----------------------------------------------------

    def _on_projection(self, index: int) -> None:
        if self._busy:
            return
        self.state.camera.projection = Projection(self._projection.itemData(index))
        self.state.notify_camera()

    def _on_fov(self, value: float) -> None:
        if self._busy:
            return
        self.state.camera.fov_deg = value
        self.state.notify_camera()

    def _on_snap(self, value: float) -> None:
        if not self._busy:
            self.state.navigation.snap_angle_deg = value

    def look_along(self, direction) -> None:
        camera = self.state.camera
        camera.look_along(direction)
        if self.state.mesh is not None:
            camera.frame(self.state.mesh.bounds)
        self.state.notify_camera()

    def _frame(self) -> None:
        self.state.frame_object()

    # -- refreshing -----------------------------------------------------

    def refresh(self) -> None:
        self.refresh_camera()
        self.refresh_bookmarks()

    def refresh_camera(self) -> None:
        """Update the projection controls only.

        The camera changes on every frame of an orbit; rebuilding the saved
        view list that often would also cancel a rename the moment it started.
        """
        camera = self.state.camera
        with self._suppressed():
            self._projection.setCurrentIndex(self._projection.findData(camera.projection.value))
            self._fov.set_value(camera.fov_deg)
            self._snap.set_value(self.state.navigation.snap_angle_deg)

    def refresh_bookmarks(self) -> None:
        row = self.state.bookmarks.current_index
        if row < 0:
            row = self._list.currentRow()
        with self._suppressed():
            self._list.clear()
            for bookmark in self.state.bookmarks:
                item = QListWidgetItem(bookmark.name)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self._list.addItem(item)
            if 0 <= row < self._list.count():
                self._list.setCurrentRow(row)

    # -- bookmarks ------------------------------------------------------

    def save_current_view(self) -> None:
        bookmarks = self.state.bookmarks
        bookmark = CameraBookmark.capture(bookmarks.next_name(), self.state.camera)
        self.state.do(
            AddItem(bookmarks.items, bookmark, text=f"Save {bookmark.name}", channel=BOOKMARKS)
        )
        bookmarks.set_current(len(bookmarks) - 1)
        self.refresh_bookmarks()

    def _update(self) -> None:
        bookmark = self._selected()
        if bookmark is None:
            return
        self.state.do(
            SetAttributes(
                bookmark,
                {"camera": self.state.camera.to_dict()},
                text=f"Update {bookmark.name}",
                channel=BOOKMARKS,
            )
        )

    def _delete(self) -> None:
        row = self._list.currentRow()
        if not 0 <= row < len(self.state.bookmarks):
            return
        name = self.state.bookmarks[row].name
        self.state.do(
            RemoveItem(self.state.bookmarks.items, row, text=f"Delete {name}", channel=BOOKMARKS)
        )
        self.state.bookmarks.set_current(min(row, len(self.state.bookmarks) - 1))
        self.refresh_bookmarks()

    def rename_selected(self) -> None:
        """Start editing the selected view's name in place."""
        item = self._list.currentItem()
        if item is not None:
            self._list.editItem(item)

    def _rename_item(self, item: QListWidgetItem) -> None:
        if self._busy:
            return
        row = self._list.row(item)
        if not 0 <= row < len(self.state.bookmarks):
            return
        bookmark = self.state.bookmarks[row]
        name = item.text().strip()
        if not name or name == bookmark.name:
            self.refresh_bookmarks()  # Put the old name back in the widget.
            return
        self.state.do(
            SetAttributes(
                bookmark, {"name": name}, text=f"Rename to {name}", channel=BOOKMARKS
            )
        )

    def _selected(self) -> CameraBookmark | None:
        row = self._list.currentRow()
        return self.state.bookmarks[row] if 0 <= row < len(self.state.bookmarks) else None

    def _recall_item(self, item: QListWidgetItem) -> None:
        self.recall(self._list.row(item))

    def recall(self, index: int) -> None:
        """Jump to a stored view by index."""
        camera = self.state.bookmarks.recall(index)
        if camera is None:
            return
        self.state.camera.apply(camera)
        self.state.notify_camera()
        self._select(index)

    def cycle(self, step: int) -> None:
        """Step to the next or previous stored view, wrapping around."""
        result = self.state.bookmarks.cycle(step)
        if result is None:
            return
        index, camera = result
        self.state.camera.apply(camera)
        self.state.notify_camera()
        self._select(index)

    def _select(self, index: int) -> None:
        with self._suppressed():
            self._list.setCurrentRow(index)
