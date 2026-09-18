"""The objects in the scene: what they are called, where they stand, what they hang from.

The list is a tree, as a modelling application draws its outliner: a child
is indented under its parent, and dragging a row onto another hangs it there.
Each row carries the object's name, a box for whether it is shown and a bar
for how solid it is drawn -- the same ghost the Shading panel applies to the
whole scene, one object at a time.  Below it the active object's placement is
written out in numbers, and the transform tool that moves it by hand is
armed.  The orientation the files are read in, and what came out of the
active one, follow as they always did.
"""

from __future__ import annotations

from dataclasses import replace

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QStyledItemDelegate,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)

from ...core.orientation import SPIN_STEPS, OrientationSettings, UpAxis
from ...core.scene import SceneObject, Transform
from ..object_tool import MODE_LABELS, MODES
from ..widgets import PointEdit, SliderSpin, collapsible_group, form_group, symbol_button
from .base import Panel

_NAME_COLUMN, _SOLIDITY_COLUMN = 0, 1

_TOGGLE_TIP = (
    "Arm the transform tool.  The active object grows a gizmo: drag one of its\n"
    "arms to move, turn or scale it along that axis, or the ring at its centre\n"
    "for a free gesture.  W, E and R choose the gesture while the tool is armed.\n"
    "Clicking another object makes that one active.  Dragging elsewhere still\n"
    "orbits; Shift snaps a turn to round angles."
)


class _NameOnlyDelegate(QStyledItemDelegate):
    """Allows in-place editing of the name column only."""

    def createEditor(self, parent, option, index):  # noqa: N802 - Qt naming
        if index.column() != _NAME_COLUMN:
            return None
        return super().createEditor(parent, option, index)


class _ObjectTree(QTreeWidget):
    """A tree whose rows can be dropped onto one another to hang one from another.

    Qt would move the rows itself; instead the drop is read off and handed
    up as ``(child, parent)``, and the tree is rebuilt from the document,
    which is the only place the hierarchy really lives.
    """

    #: ``(object, new parent or None)`` -- a row was dropped somewhere.
    reparented = Signal(object, object)

    def dropEvent(self, event) -> None:  # noqa: N802 - Qt naming
        dragged = self.currentItem()
        target = self.itemAt(event.position().toPoint())
        where = self.dropIndicatorPosition()
        event.setDropAction(Qt.DropAction.IgnoreAction)
        event.accept()
        if dragged is None:
            return
        child = dragged.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        if target is None or where == QAbstractItemView.DropIndicatorPosition.OnViewport:
            parent = None
        elif where == QAbstractItemView.DropIndicatorPosition.OnItem:
            parent = target.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        else:
            above = target.parent()
            parent = None if above is None else above.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        if child is not None and child is not parent:
            self.reparented.emit(child, parent)


class ModelPanel(Panel):
    """Lists the objects, places the active one, and reports what came out of its file."""

    #: The transform tool was armed or disarmed from the panel.
    object_toggled = Signal(bool)
    #: The Add button: the window opens the file dialog, since it owns the folders.
    add_requested = Signal()
    #: The view needs repainting, but nothing about the document changed.
    repaint_requested = Signal()

    def _build(self) -> None:
        self._tool = None
        #: Where the objects stood when a solidity drag began, so the drag
        #: is one undo step; ``None`` between drags.
        self._opacity_before = None

        self._build_objects()
        self._build_transform()
        self._build_linking()
        self._build_orientation()
        self._build_info()
        self._add_stretch()

    # -- objects --------------------------------------------------------

    def _build_objects(self) -> None:
        box, form = form_group("Objects")
        self._tree = _ObjectTree()
        self._tree.setColumnCount(2)
        self._tree.setHeaderLabels(["Object", "Solidity"])
        self._tree.setRootIsDecorated(True)
        self._tree.setAlternatingRowColors(True)
        self._tree.setItemDelegate(_NameOnlyDelegate(self._tree))
        self._tree.setEditTriggers(
            QTreeWidget.EditTrigger.DoubleClicked | QTreeWidget.EditTrigger.EditKeyPressed
        )
        self._tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self._tree.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self._tree.setDefaultDropAction(Qt.DropAction.MoveAction)
        self._tree.setToolTip(
            "Double-click a name to rename it.  Tick a box to show or hide an object.\n"
            "Drag a row onto another to hang it from that one; drag it to empty\n"
            "space to set it free.  Ctrl-click to pick several to merge.\n"
            "Alt-click an object in the view to make it active from there."
        )
        header = self._tree.header()
        header.setSectionResizeMode(_NAME_COLUMN, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(_SOLIDITY_COLUMN, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(_SOLIDITY_COLUMN, 92)
        self._tree.setMinimumHeight(110)
        self._tree.itemChanged.connect(self._on_item_changed)
        self._tree.itemSelectionChanged.connect(self._on_selection_changed)
        self._tree.reparented.connect(self._on_reparented)
        form.addRow(self._tree)

        self._add_button = symbol_button("plus", "Add a model to the scene")
        self._add_button.setToolTip(
            "Add another model, standing at the origin.  File > Add Model... does the same."
        )
        self._remove = symbol_button("trash", "Remove the active object")
        self._duplicate = QPushButton("Duplicate")
        self._duplicate.setToolTip(
            "A copy of the active object's mesh, standing on top of it and hung\n"
            "where it hangs.  Only the mesh: no rig, no children."
        )
        self._merge = QPushButton("Merge")
        self._merge.setToolTip(
            "Join the selected objects into one, standing where they stood.\n"
            "Ctrl-click rows in the list to select more than one."
        )
        self._split = QPushButton("Split")
        self._split.setToolTip(
            "Break the active object into its loose pieces -- the parts that\n"
            "share no vertices -- each an object of its own, standing where it was."
        )
        form.addRow(
            _row(self._add_button, self._remove, self._duplicate, self._merge, self._split)
        )

        self._parent = QComboBox()
        self._parent.setToolTip(
            "What the active object hangs from.  A child follows its parent's\n"
            "moves, turns and scales; see Linking for what else it follows."
        )
        form.addRow("Parent", self._parent)
        self._add(box)

        self._add_button.clicked.connect(self.add_requested)
        self._remove.clicked.connect(self.remove_active)
        self._duplicate.clicked.connect(self.duplicate_active)
        self._merge.clicked.connect(self.merge_selected)
        self._split.clicked.connect(self.split_active)
        self._parent.currentIndexChanged.connect(self._on_parent_chosen)

    # -- transform ------------------------------------------------------

    def _build_transform(self) -> None:
        box, form = form_group("Transform")
        self._toggle = QPushButton("Transform")
        self._toggle.setCheckable(True)
        self._toggle.setToolTip(_TOGGLE_TIP)
        self._toggle.toggled.connect(self._on_toggled)
        form.addRow(self._toggle)

        self._mode = QComboBox()
        for mode in MODES:
            self._mode.addItem(MODE_LABELS[mode], mode)
        self._mode.setToolTip("What a drag on the gizmo does")
        form.addRow("Gesture", self._mode)

        self._position = PointEdit(decimals=3)
        self._position.setToolTip("Where the object's pivot stands, in its parent's frame")
        self._rotation = PointEdit(decimals=1)
        self._rotation.setToolTip("Turns about the object's own X, then Y, then Z, in degrees")
        self._rotation.set_step(5.0)
        self._scale = PointEdit(decimals=3)
        self._scale.setToolTip("How many times its own size the object is drawn, per axis")
        self._scale.set_step(0.05)
        form.addRow("Position", self._position)
        form.addRow("Rotation", self._rotation)
        form.addRow("Scale", self._scale)

        self._uniform = QCheckBox("Scale all axes together")
        self._uniform.setToolTip(
            "The scale gesture, and a number typed into any scale box, move all\n"
            "three axes by the same factor.  Off, each axis is stretched on its own."
        )
        form.addRow("", self._uniform)

        self._reset = QPushButton("Place at Origin")
        self._reset.setToolTip("Put the active object back at the origin, unturned and unscaled")
        form.addRow("", self._reset)
        self._add(box)

        self._mode.currentIndexChanged.connect(self._on_mode_chosen)
        self._position.valueChanged.connect(lambda v: self._on_transform_typed("translation", v))
        self._rotation.valueChanged.connect(lambda v: self._on_transform_typed("rotation_deg", v))
        self._scale.valueChanged.connect(lambda v: self._on_transform_typed("scale", v))
        self._uniform.toggled.connect(lambda v: self._apply_setting("uniform_scale", v))
        self._reset.clicked.connect(self.reset_transform)

    # -- linking --------------------------------------------------------

    def _build_linking(self) -> None:
        box, form = collapsible_group("Linking")
        self._hide_children = QCheckBox("Hiding a parent hides its children")
        self._ghost_children = QCheckBox("A parent's solidity is handed down")
        self._ghost_children.setToolTip(
            "A child of a half-ghosted parent is drawn at half of its own solidity."
        )
        self._keep_transform = QCheckBox("Keep an object in place when linking it")
        self._keep_transform.setToolTip(
            "Hanging an object from a parent re-expresses where it stands in the\n"
            "parent's frame, so nothing moves.  Off, its numbers are kept and it\n"
            "jumps to wherever they land under the new parent."
        )
        self._remove_children = QCheckBox("Removing a parent removes its children")
        self._remove_children.setToolTip(
            "Off, the children are hung from the grandparent, where they stood."
        )
        for widget in (
            self._hide_children,
            self._ghost_children,
            self._keep_transform,
            self._remove_children,
        ):
            form.addRow("", widget)
        self._add(box)

        self._hide_children.toggled.connect(lambda v: self._apply_setting("hide_children", v))
        self._ghost_children.toggled.connect(lambda v: self._apply_setting("ghost_children", v))
        self._keep_transform.toggled.connect(lambda v: self._apply_setting("keep_transform", v))
        self._remove_children.toggled.connect(
            lambda v: self._apply_setting("remove_children", v)
        )

    # -- orientation and the file ---------------------------------------

    def _build_orientation(self) -> None:
        box, form = form_group("Orientation")
        self._up_axis = QComboBox()
        for axis in UpAxis:
            self._up_axis.addItem(axis.label, axis.value)
        self._up_axis.setToolTip(
            "Which axis of the files points up.  Z-up is what CAD and Blender\n"
            "usually export; STL says nothing, so try both.  Applies to every\n"
            "object: files from one pipeline share an up axis."
        )
        self._flip = QCheckBox("Upside down")
        self._spin = QComboBox()
        for angle in SPIN_STEPS:
            self._spin.addItem(f"{angle:.0f} deg", angle)
        self._spin.setToolTip("Quarter turn about the vertical, to face the model forwards")
        form.addRow("Up axis", self._up_axis)
        form.addRow("", self._flip)
        form.addRow("Spin", self._spin)

        reset = QPushButton("Use the File's Axes")
        reset.setToolTip("Go back to the orientation the file was stored in")
        reset.clicked.connect(self._reset_orientation)
        form.addRow("", reset)
        self._add(box)

        self._up_axis.currentIndexChanged.connect(self._on_orientation_changed)
        self._flip.toggled.connect(self._on_orientation_changed)
        self._spin.currentIndexChanged.connect(self._on_orientation_changed)

    def _build_info(self) -> None:
        info_box, info_form = form_group("Imported")
        self._name = QLabel("-")
        self._counts = QLabel("-")
        self._size = QLabel("-")
        self._units = QLabel("-")
        for label in (self._name, self._counts, self._size, self._units):
            label.setWordWrap(True)
        info_form.addRow("File", self._name)
        info_form.addRow("Geometry", self._counts)
        info_form.addRow("Size", self._size)
        info_form.addRow("Units", self._units)
        self._add(info_box)

    # -- the tool -------------------------------------------------------

    def attach(self, tool) -> None:
        """Bind the panel to the viewport's transform tool."""
        self._tool = tool
        self.refresh()

    def set_active(self, active: bool) -> None:
        """Reflect the tool state without re-emitting the toggle."""
        with self._suppressed():
            self._toggle.setChecked(active)

    def _on_toggled(self, active: bool) -> None:
        if self._busy:
            return
        self.object_toggled.emit(active)

    def _on_mode_chosen(self, index: int) -> None:
        if self._busy or self._tool is None:
            return
        self._tool.set_mode(self._mode.itemData(index))
        self.repaint_requested.emit()

    def set_mode(self, mode: str) -> None:
        """Choose the gesture, from the menu or a key."""
        if self._tool is not None:
            self._tool.set_mode(mode)
        with self._suppressed():
            self._mode.setCurrentIndex(max(self._mode.findData(mode), 0))
        self.repaint_requested.emit()

    # -- the list -------------------------------------------------------

    def refresh_list(self) -> None:
        """Rebuild the tree from the store, with the active object current."""
        state = self.state
        active = state.active_object
        selected = {id(obj) for obj in self.selected_objects()}
        with self._suppressed():
            self._tree.clear()
            rows: dict[int, QTreeWidgetItem] = {}
            for obj, _depth in state.objects.ordered():
                item = QTreeWidgetItem([obj.name, ""])
                item.setFlags(
                    item.flags()
                    | Qt.ItemFlag.ItemIsEditable
                    | Qt.ItemFlag.ItemIsUserCheckable
                    | Qt.ItemFlag.ItemIsDragEnabled
                    | Qt.ItemFlag.ItemIsDropEnabled
                )
                item.setCheckState(
                    _NAME_COLUMN,
                    Qt.CheckState.Checked if obj.visible else Qt.CheckState.Unchecked,
                )
                item.setData(_NAME_COLUMN, Qt.ItemDataRole.UserRole, obj)
                if obj.path is not None:
                    item.setToolTip(_NAME_COLUMN, str(obj.path))
                else:
                    item.setToolTip(
                        _NAME_COLUMN, "No file of its own yet; saving the session writes one"
                    )
                if not state.objects.shown(obj, state.object_settings):
                    item.setForeground(_NAME_COLUMN, self.palette().placeholderText())
                above = rows.get(id(obj.parent)) if obj.parent is not None else None
                if above is None:
                    self._tree.addTopLevelItem(item)
                else:
                    above.addChild(item)
                    above.setExpanded(True)
                rows[id(obj)] = item
                slider = SliderSpin(0.0, 1.0, obj.opacity, decimals=2, step=0.05)
                slider.setToolTip("How solid this object is drawn; less is a ghost")
                slider.valueChanged.connect(lambda v, o=obj: self._on_opacity_dragged(o, v))
                slider.valueCommitted.connect(lambda v, o=obj: self._on_opacity_committed(o, v))
                self._tree.setItemWidget(item, _SOLIDITY_COLUMN, slider)
                if obj is active:
                    self._tree.setCurrentItem(item)
                    font = item.font(_NAME_COLUMN)
                    font.setBold(True)
                    item.setFont(_NAME_COLUMN, font)
                if id(obj) in selected and obj is not active:
                    item.setSelected(True)
            self._refresh_parent_choices()
        self.update_enabled()

    def _refresh_parent_choices(self) -> None:
        """Offer every object the active one could hang from."""
        state = self.state
        active = state.active_object
        self._parent.clear()
        self._parent.addItem("None", None)
        if active is None:
            return
        for obj, depth in state.objects.ordered():
            if obj is active or state.objects.is_ancestor(active, obj):
                continue
            self._parent.addItem("    " * depth + obj.name, obj)
        for index in range(self._parent.count()):
            if self._parent.itemData(index) is active.parent:
                self._parent.setCurrentIndex(index)
                break

    def selected_objects(self) -> list[SceneObject]:
        """The objects whose rows are selected, in list order."""
        chosen = {
            id(item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole))
            for item in self._tree.selectedItems()
        }
        return [obj for obj in self.state.objects if id(obj) in chosen]

    def _on_selection_changed(self) -> None:
        if self._busy:
            return
        item = self._tree.currentItem()
        if item is None:
            return
        obj = item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        if obj is not None and obj is not self.state.active_object:
            # Deferred, as every edit made from a row is: making an object
            # active rebuilds the tree, and the row that was clicked is
            # still delivering its signal.
            QTimer.singleShot(0, lambda: self.state.set_active(obj))

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        """Commit a renamed or re-checked row, if anything actually changed."""
        if self._busy or column != _NAME_COLUMN:
            return
        obj = item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        if obj is None or self.state.objects.index(obj) < 0:
            return
        name = item.text(_NAME_COLUMN).strip()
        visible = item.checkState(_NAME_COLUMN) == Qt.CheckState.Checked
        # Committing rebuilds the tree, and destroying the very item whose
        # signal is still being delivered takes the application down with
        # it, so the edit is queued rather than applied in the slot.
        if name and name != obj.name:
            QTimer.singleShot(0, lambda: self.state.rename_object(obj, name))
        elif visible != obj.visible:
            QTimer.singleShot(0, lambda: self.state.set_object_visible(obj, visible))

    def _on_opacity_dragged(self, obj: SceneObject, value: float) -> None:
        if self._busy:
            return
        if self._opacity_before is None:
            self._opacity_before = self.state.snapshot_objects()
        self.state.preview_object_opacity(obj, value)

    def _on_opacity_committed(self, obj: SceneObject, value: float) -> None:
        if self._busy:
            return
        before, self._opacity_before = self._opacity_before, None
        QTimer.singleShot(0, lambda: self.state.set_object_opacity(obj, value, before))

    def _on_reparented(self, child, parent) -> None:
        if child is not None:
            QTimer.singleShot(0, lambda: self.state.set_parent(child, parent))

    def _on_parent_chosen(self, index: int) -> None:
        if self._busy:
            return
        active = self.state.active_object
        if active is None:
            return
        parent = self._parent.itemData(index)
        if parent is not active.parent:
            QTimer.singleShot(0, lambda: self.state.set_parent(active, parent))

    # -- the buttons ----------------------------------------------------

    def remove_active(self) -> None:
        active = self.state.active_object
        if active is not None:
            self.state.remove_object(active)

    def duplicate_active(self) -> None:
        active = self.state.active_object
        if active is not None:
            self.state.duplicate_object(active)

    def merge_selected(self) -> None:
        chosen = self.selected_objects()
        active = self.state.active_object
        if active is not None and not any(obj is active for obj in chosen):
            chosen.append(active)
        self.state.merge_objects(chosen)

    def split_active(self) -> None:
        active = self.state.active_object
        if active is not None:
            self.state.split_object(active)

    def reset_transform(self) -> None:
        active = self.state.active_object
        if active is not None:
            self.state.set_transform(active, Transform(), f"Place {active.name} at the origin")

    def _on_transform_typed(self, field: str, value) -> None:
        if self._busy:
            return
        active = self.state.active_object
        if active is None:
            return
        value = tuple(float(v) for v in value)
        if field == "scale" and self.state.object_settings.uniform_scale:
            # Whichever box moved carries the other two with it.
            was = active.transform.scale
            moved = next((i for i in range(3) if abs(value[i] - was[i]) > 1e-12), None)
            if moved is not None:
                value = (value[moved],) * 3
        if field == "scale":
            value = tuple(v if abs(v) > 1e-6 else 1e-6 for v in value)
        transform = replace(active.transform, **{field: value})
        verb = {"translation": "Move", "rotation_deg": "Turn", "scale": "Scale"}[field]
        self.state.set_transform(active, transform, f"{verb} {active.name}")

    def _apply_setting(self, field: str, value) -> None:
        if self._busy:
            return
        setattr(self.state.object_settings, field, bool(value))
        self.state.notify_object_settings()

    # -- orientation ----------------------------------------------------

    def _on_orientation_changed(self, *_args) -> None:
        if self._busy:
            return
        self.state.set_orientation(
            OrientationSettings(
                up_axis=UpAxis(self._up_axis.currentData()),
                flip_up=self._flip.isChecked(),
                spin_deg=float(self._spin.currentData()),
            )
        )
        self.refresh()

    def _reset_orientation(self) -> None:
        self.state.set_orientation(OrientationSettings())
        self.refresh()

    # -- refreshing -----------------------------------------------------

    def refresh(self) -> None:
        orientation = self.state.orientation
        settings = self.state.object_settings
        with self._suppressed():
            self._up_axis.setCurrentIndex(self._up_axis.findData(orientation.up_axis.value))
            self._flip.setChecked(orientation.flip_up)
            spin = self._spin.findData(orientation.spin_deg % 360.0)
            self._spin.setCurrentIndex(max(spin, 0))
            self._hide_children.setChecked(settings.hide_children)
            self._ghost_children.setChecked(settings.ghost_children)
            self._keep_transform.setChecked(settings.keep_transform)
            self._remove_children.setChecked(settings.remove_children)
            self._uniform.setChecked(settings.uniform_scale)
            if self._tool is not None:
                self._mode.setCurrentIndex(max(self._mode.findData(self._tool.mode), 0))
        self.refresh_list()
        self.refresh_transform()
        self._refresh_info()

    def refresh_transform(self) -> None:
        """Write the active object's placement into the boxes."""
        active = self.state.active_object
        transform = Transform() if active is None else active.transform
        with self._suppressed():
            self._position.set_value(transform.translation)
            self._rotation.set_value(transform.rotation_deg)
            self._scale.set_value(transform.scale)
        radius = self.state.camera.scene_radius
        self._position.set_step(max(radius * 0.01, 1e-3))

    def update_enabled(self) -> None:
        state = self.state
        count = len(state.objects)
        active = state.active_object
        self._remove.setEnabled(active is not None)
        self._duplicate.setEnabled(active is not None)
        self._split.setEnabled(active is not None)
        self._merge.setEnabled(count >= 2)
        self._parent.setEnabled(count >= 2)
        for widget in (self._position, self._rotation, self._scale, self._reset):
            widget.setEnabled(active is not None)

    def _refresh_info(self) -> None:
        active = self.state.active_object
        if active is None:
            for label in (self._name, self._counts, self._size, self._units):
                label.setText("-")
            self._name.setText("Nothing loaded")
            return

        mesh = active.rest_mesh
        path = active.path
        settings = self.state.measurement_settings
        self._name.setText(path.name if path else f"{active.name} (no file yet)")
        self._counts.setText(
            f"{mesh.triangle_count:,} triangles, {mesh.vertex_count:,} vertices"
        )
        width, height, depth = (settings.format_length(v) for v in mesh.bounds.size)
        self._size.setText(f"{width} x {height} x {depth}")
        source = mesh.units
        self._units.setText(
            f"1 unit = 1 {source.name}, from the file"
            if source is not None
            else f"{settings.unit_name}, set by hand (the file declares none)"
        )


def _row(*buttons: QPushButton) -> QWidget:
    """A strip of buttons that one form row can show or hide as a unit."""
    holder = QWidget()
    layout = QHBoxLayout(holder)
    layout.setContentsMargins(0, 0, 0, 0)
    for button in buttons:
        layout.addWidget(button)
    return holder
