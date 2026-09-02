"""What was imported and which way up it should stand."""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QComboBox, QLabel, QPushButton

from ...core.orientation import SPIN_STEPS, OrientationSettings, UpAxis
from ..widgets import form_group
from .base import Panel


class ModelPanel(Panel):
    """Turns the model the right way up and reports what came out of the file."""

    def _build(self) -> None:
        box, form = form_group("Orientation")
        self._up_axis = QComboBox()
        for axis in UpAxis:
            self._up_axis.addItem(axis.label, axis.value)
        self._up_axis.setToolTip(
            "Which axis of the file points up.  Z-up is what CAD and Blender\n"
            "usually export; STL says nothing, so try both."
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
        reset.clicked.connect(self._reset)
        form.addRow("", reset)
        self._add(box)

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
        self._add_stretch()

        self._up_axis.currentIndexChanged.connect(self._on_changed)
        self._flip.toggled.connect(self._on_changed)
        self._spin.currentIndexChanged.connect(self._on_changed)

    # -- reactions ------------------------------------------------------

    def _on_changed(self, *_args) -> None:
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

    def _reset(self) -> None:
        self.state.set_orientation(OrientationSettings())
        self.refresh()

    # -- refreshing -----------------------------------------------------

    def refresh(self) -> None:
        orientation = self.state.orientation
        with self._suppressed():
            self._up_axis.setCurrentIndex(self._up_axis.findData(orientation.up_axis.value))
            self._flip.setChecked(orientation.flip_up)
            spin = self._spin.findData(orientation.spin_deg % 360.0)
            self._spin.setCurrentIndex(max(spin, 0))
        self._refresh_info()

    def _refresh_info(self) -> None:
        mesh = self.state.mesh
        if mesh is None:
            for label in (self._name, self._counts, self._size, self._units):
                label.setText("-")
            self._name.setText("Nothing loaded")
            return

        path = self.state.mesh_path
        settings = self.state.measurement_settings
        self._name.setText(path.name if path else mesh.name)
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
