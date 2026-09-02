"""Measurement list and display options."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QSpinBox,
    QStyledItemDelegate,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)

from ...core.commands import RemoveItem, ReplaceItems, SetAttributes
from ...core.history import MEASUREMENTS
from ...core.measurement import UNIT_NAMES, Measurement
from ..icons import lock_icon
from ..widgets import SliderSpin, form_group
from .base import Panel

_NAME_COLUMN = 0
_LENGTH_COLUMN = 1
_LOCK_COLUMN = 2


class _NameOnlyDelegate(QStyledItemDelegate):
    """Allows in-place editing of the name column only."""

    def createEditor(self, parent, option, index):  # noqa: N802 - Qt naming
        if index.column() != _NAME_COLUMN:
            return None
        return super().createEditor(parent, option, index)


class MeasurePanel(Panel):
    """Lists saved measurements and controls how they are drawn."""

    measure_toggled = Signal(bool)
    center_requested = Signal(object)

    def _build(self) -> None:
        self._toggle = QPushButton("Measure  (M)")
        self._toggle.setCheckable(True)
        self._toggle.setToolTip(
            "Click two points on the model to record a distance.\n"
            "Dragging still orbits; Esc clears a half-finished measurement."
        )
        self._toggle.toggled.connect(self._on_toggled)
        self._add(self._toggle)

        self._tree = QTreeWidget()
        self._tree.setColumnCount(3)
        self._tree.setHeaderLabels(["Name", "Length", ""])
        self._tree.setRootIsDecorated(False)
        self._tree.setAlternatingRowColors(True)
        self._tree.setItemDelegate(_NameOnlyDelegate(self._tree))
        self._tree.header().setSectionResizeMode(_NAME_COLUMN, QHeaderView.ResizeMode.Stretch)
        for column in (_LENGTH_COLUMN, _LOCK_COLUMN):
            self._tree.header().setSectionResizeMode(
                column, QHeaderView.ResizeMode.ResizeToContents
            )
        self._tree.itemChanged.connect(self._on_item_changed)
        self._tree.itemClicked.connect(self._on_item_clicked)
        self._tree.itemDoubleClicked.connect(self._on_double_clicked)
        self._add(self._tree)

        hint = QLabel("Click a padlock to unlock a measurement, then drag its handles in the view.")
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #8f939b;")
        self._add(hint)

        buttons = QWidget()
        row = QHBoxLayout(buttons)
        row.setContentsMargins(0, 0, 0, 0)
        for label, slot in (
            ("Delete", self._delete_selected),
            ("Clear All", self.clear_all),
            ("Centre View", self._center_selected),
        ):
            button = QPushButton(label)
            button.clicked.connect(slot)
            row.addWidget(button)
        self._add(buttons)

        units_box, units_form = form_group("Units")
        self._unit_name = QComboBox()
        self._unit_name.setEditable(True)
        self._unit_name.addItems(UNIT_NAMES)
        self._unit_scale = QDoubleSpinBox()
        self._unit_scale.setDecimals(4)
        self._unit_scale.setRange(0.0001, 100000.0)
        self._unit_scale.setSingleStep(0.1)
        self._unit_scale.setToolTip(
            "Multiplier from scene units to display units.\n"
            "An OBJ carries no units, so set this once for your model."
        )
        self._decimals = QSpinBox()
        self._decimals.setRange(0, 5)
        units_form.addRow("Unit", self._unit_name)
        units_form.addRow("Scale", self._unit_scale)
        units_form.addRow("Decimals", self._decimals)
        self._add(units_box)

        placement_box, placement_form = form_group("Placement")
        self._snap = QCheckBox("Snap to nearest vertex")
        self._free = QCheckBox("Free points (ignore the surface)")
        self._free.setToolTip(
            "Place and drag points anywhere in space rather than on the model.\n"
            "They land on the plane facing the camera through the object centre."
        )
        placement_form.addRow("", self._snap)
        placement_form.addRow("", self._free)
        self._add(placement_box)

        display_box, display_form = form_group("Display")
        self._show_all = QCheckBox("Show measurements")
        self._show_labels = QCheckBox("Show labels")
        self._line_width = SliderSpin(1.0, 12.0, 3.0, decimals=1, step=0.5)
        self._point_radius = SliderSpin(1.0, 12.0, 4.0, decimals=1, step=0.5)
        self._label_size = SliderSpin(6.0, 24.0, 11.0, decimals=0, step=1.0)
        display_form.addRow("", self._show_all)
        display_form.addRow("", self._show_labels)
        display_form.addRow("Line width", self._line_width)
        display_form.addRow("Point size", self._point_radius)
        display_form.addRow("Label size", self._label_size)
        self._add(display_box)
        self._add_stretch()

        self._unit_name.currentTextChanged.connect(lambda v: self._apply("unit_name", v))
        self._unit_scale.valueChanged.connect(lambda v: self._apply("unit_scale", v))
        self._decimals.valueChanged.connect(lambda v: self._apply("decimals", v))
        self._show_all.toggled.connect(lambda v: self._apply("show_all", v))
        self._show_labels.toggled.connect(lambda v: self._apply("show_labels", v))
        self._snap.toggled.connect(lambda v: self._apply("snap_to_vertex", v))
        self._free.toggled.connect(lambda v: self._apply("free_placement", v))
        self._line_width.valueChanged.connect(lambda v: self._apply("line_width", v))
        self._point_radius.valueChanged.connect(lambda v: self._apply("point_radius", v))
        self._label_size.valueChanged.connect(lambda v: self._apply("label_size", int(v)))

    # -- measuring toggle -----------------------------------------------

    def set_measuring(self, active: bool) -> None:
        """Reflect the tool state without re-emitting the toggle."""
        with self._suppressed():
            self._toggle.setChecked(active)

    def _on_toggled(self, active: bool) -> None:
        if self._busy:
            return
        self.measure_toggled.emit(active)

    # -- list -----------------------------------------------------------

    def refresh(self) -> None:
        settings = self.state.measurement_settings
        with self._suppressed():
            self._unit_name.setCurrentText(settings.unit_name)
            self._unit_scale.setValue(settings.unit_scale)
            self._decimals.setValue(settings.decimals)
            self._show_all.setChecked(settings.show_all)
            self._show_labels.setChecked(settings.show_labels)
            self._snap.setChecked(settings.snap_to_vertex)
            self._free.setChecked(settings.free_placement)
            self._line_width.set_value(settings.line_width)
            self._point_radius.set_value(settings.point_radius)
            self._label_size.set_value(settings.label_size)
        self.refresh_list()

    def refresh_list(self) -> None:
        """Rebuild the tree from the store, preserving the selected row."""
        settings = self.state.measurement_settings
        selected = self._selected_index()
        with self._suppressed():
            self._tree.clear()
            for measurement in self.state.measurements:
                item = QTreeWidgetItem(
                    [measurement.name, settings.format_length(measurement.length), ""]
                )
                item.setFlags(
                    item.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsUserCheckable
                )
                item.setCheckState(
                    _NAME_COLUMN,
                    Qt.CheckState.Checked if measurement.visible else Qt.CheckState.Unchecked,
                )
                item.setTextAlignment(
                    _LENGTH_COLUMN, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                )
                self._set_lock_cell(item, measurement.locked)
                self._tree.addTopLevelItem(item)
            if 0 <= selected < self._tree.topLevelItemCount():
                self._tree.setCurrentItem(self._tree.topLevelItem(selected))

    @staticmethod
    def _set_lock_cell(item: QTreeWidgetItem, locked: bool) -> None:
        item.setIcon(_LOCK_COLUMN, lock_icon(locked))
        item.setToolTip(
            _LOCK_COLUMN,
            "Locked - click to unlock and drag its endpoints"
            if locked
            else "Unlocked - drag the square handles in the view; click to lock",
        )

    def _selected_index(self) -> int:
        item = self._tree.currentItem()
        return self._tree.indexOfTopLevelItem(item) if item is not None else -1

    def _measurement_at(self, item: QTreeWidgetItem) -> tuple[int, Measurement] | None:
        index = self._tree.indexOfTopLevelItem(item)
        if 0 <= index < len(self.state.measurements):
            return index, self.state.measurements[index]
        return None

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        """Commit a renamed or re-checked row, if anything actually changed."""
        if self._busy:
            return
        found = self._measurement_at(item)
        if found is None:
            return
        _, measurement = found
        name = item.text(_NAME_COLUMN) or measurement.name
        visible = item.checkState(_NAME_COLUMN) == Qt.CheckState.Checked
        changes = {}
        if name != measurement.name:
            changes["name"] = name
        if visible != measurement.visible:
            changes["visible"] = visible
        if not changes:
            return
        verb = "Rename" if "name" in changes else ("Show" if visible else "Hide")
        self.state.do(
            SetAttributes(
                measurement, changes, text=f"{verb} {measurement.name}", channel=MEASUREMENTS
            )
        )

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        if column != _LOCK_COLUMN:
            return
        found = self._measurement_at(item)
        if found is None:
            return
        _, measurement = found
        self.toggle_lock(measurement)

    def toggle_lock(self, measurement: Measurement) -> None:
        """Lock or unlock one measurement, making its endpoints draggable."""
        locked = not measurement.locked
        self.state.do(
            SetAttributes(
                measurement,
                {"locked": locked},
                text=f"{'Lock' if locked else 'Unlock'} {measurement.name}",
                channel=MEASUREMENTS,
            )
        )

    def _on_double_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        if column == _LENGTH_COLUMN:
            self._center_selected()

    def _selected_measurement(self) -> Measurement | None:
        index = self._selected_index()
        if 0 <= index < len(self.state.measurements):
            return self.state.measurements[index]
        return None

    def _delete_selected(self) -> None:
        index = self._selected_index()
        if index < 0 or index >= len(self.state.measurements):
            return
        name = self.state.measurements[index].name
        self.state.do(
            RemoveItem(
                self.state.measurements.items, index, text=f"Delete {name}", channel=MEASUREMENTS
            )
        )

    def clear_all(self) -> None:
        if not len(self.state.measurements):
            return
        self.state.do(
            ReplaceItems(
                self.state.measurements.items, [], text="Clear measurements", channel=MEASUREMENTS
            )
        )

    def _center_selected(self) -> None:
        measurement = self._selected_measurement()
        if measurement is not None:
            self.center_requested.emit(measurement)

    # -- settings -------------------------------------------------------

    def _apply(self, field: str, value) -> None:
        if self._busy:
            return
        setattr(self.state.measurement_settings, field, value)
        self.state.notify_measurements()
