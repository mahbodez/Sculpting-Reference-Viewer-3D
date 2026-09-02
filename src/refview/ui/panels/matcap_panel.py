"""Matcap selection and colour grading."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QWidget,
)

from ...core.settings import MatcapSettings
from ...paths import available_matcaps, matcap_dir
from ...render.texture import MatcapLoadError
from ..widgets import ColorButton, SliderSpin, form_group
from .base import Panel

_THUMBNAIL = QSize(56, 56)


class MatcapPanel(Panel):
    """Picks the matcap image and tunes how it is sampled."""

    def _build(self) -> None:
        self._gallery = QListWidget()
        self._gallery.setViewMode(QListWidget.ViewMode.IconMode)
        self._gallery.setIconSize(_THUMBNAIL)
        self._gallery.setGridSize(QSize(_THUMBNAIL.width() + 16, _THUMBNAIL.height() + 22))
        self._gallery.setResizeMode(QListWidget.ResizeMode.Adjust)
        self._gallery.setMovement(QListWidget.Movement.Static)
        self._gallery.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self._gallery.setMaximumHeight(210)
        self._gallery.setWordWrap(True)
        self._gallery.itemSelectionChanged.connect(self._on_selected)
        self._add(self._gallery)

        buttons = QWidget()
        row = QHBoxLayout(buttons)
        row.setContentsMargins(0, 0, 0, 0)
        browse_button = QPushButton("Load Matcap...")
        browse_button.clicked.connect(self.browse)
        rescan = QPushButton("Rescan Folder")
        rescan.clicked.connect(self.reload_gallery)
        row.addWidget(browse_button)
        row.addWidget(rescan)
        self._add(buttons)

        box, form = form_group("Adjustments")
        self._rotation = SliderSpin(-180.0, 180.0, 0.0, decimals=0, step=1.0, suffix=" deg")
        self._contrast = SliderSpin(0.0, 3.0, 1.0)
        self._gamma = SliderSpin(0.1, 3.0, 1.0)
        self._brightness = SliderSpin(0.0, 3.0, 1.0)
        self._saturation = SliderSpin(0.0, 3.0, 1.0)
        self._tint = ColorButton((1.0, 1.0, 1.0))
        self._flip_y = QCheckBox("Flip vertically")

        form.addRow("Rotation", self._rotation)
        form.addRow("Contrast", self._contrast)
        form.addRow("Gamma", self._gamma)
        form.addRow("Brightness", self._brightness)
        form.addRow("Saturation", self._saturation)
        form.addRow("Tint", self._tint)
        form.addRow("", self._flip_y)
        self._add(box)

        reset = QPushButton("Reset Adjustments")
        reset.clicked.connect(self._reset)
        self._add(reset)
        self._add_stretch()

        self._rotation.valueChanged.connect(lambda v: self._apply("rotation_deg", v))
        self._contrast.valueChanged.connect(lambda v: self._apply("contrast", v))
        self._gamma.valueChanged.connect(lambda v: self._apply("gamma", v))
        self._brightness.valueChanged.connect(lambda v: self._apply("brightness", v))
        self._saturation.valueChanged.connect(lambda v: self._apply("saturation", v))
        self._tint.colorChanged.connect(lambda v: self._apply("tint", v))
        self._flip_y.toggled.connect(lambda v: self._apply("flip_y", v))

        self.reload_gallery()

    # -- gallery --------------------------------------------------------

    def reload_gallery(self) -> None:
        """Rebuild the thumbnail list from the resources folder."""
        with self._suppressed():
            self._gallery.clear()
            builtin = QListWidgetItem("Built-in")
            builtin.setData(Qt.ItemDataRole.UserRole, None)
            builtin.setToolTip("Neutral studio matcap generated at runtime")
            self._gallery.addItem(builtin)
            for path in available_matcaps():
                item = QListWidgetItem(path.stem)
                item.setData(Qt.ItemDataRole.UserRole, str(path))
                item.setToolTip(str(path))
                pixmap = QPixmap(str(path))
                if not pixmap.isNull():
                    item.setIcon(
                        QIcon(
                            pixmap.scaled(
                                _THUMBNAIL,
                                Qt.AspectRatioMode.KeepAspectRatio,
                                Qt.TransformationMode.SmoothTransformation,
                            )
                        )
                    )
                self._gallery.addItem(item)
        self._select_current()

    def _select_current(self) -> None:
        current = self.state.render.matcap_path
        with self._suppressed():
            for index in range(self._gallery.count()):
                item = self._gallery.item(index)
                stored = item.data(Qt.ItemDataRole.UserRole)
                if (stored is None and current is None) or (
                    stored is not None and current is not None and Path(stored) == Path(current)
                ):
                    self._gallery.setCurrentItem(item)
                    return
            self._gallery.clearSelection()

    def _on_selected(self) -> None:
        if self._busy:
            return
        item = self._gallery.currentItem()
        if item is None:
            return
        self._load(item.data(Qt.ItemDataRole.UserRole))

    def browse(self) -> None:
        start = matcap_dir()
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Matcap",
            str(start if start.is_dir() else Path.home()),
            "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp)",
        )
        if path:
            self._load(path)
            self.reload_gallery()

    def _load(self, path: str | None) -> None:
        try:
            self.state.load_matcap(path)
        except MatcapLoadError as error:
            QMessageBox.warning(self, "Matcap", str(error))
            return
        self._select_current()

    # -- adjustments ----------------------------------------------------

    def _apply(self, field: str, value) -> None:
        if self._busy:
            return
        setattr(self.state.render.matcap, field, value)
        self.state.notify_render()

    def _reset(self) -> None:
        self.state.render.matcap = MatcapSettings()
        self.state.notify_render()
        self.refresh()

    def refresh(self) -> None:
        matcap = self.state.render.matcap
        with self._suppressed():
            self._rotation.set_value(matcap.rotation_deg)
            self._contrast.set_value(matcap.contrast)
            self._gamma.set_value(matcap.gamma)
            self._brightness.set_value(matcap.brightness)
            self._saturation.set_value(matcap.saturation)
            self._tint.set_color(matcap.tint)
            self._flip_y.setChecked(matcap.flip_y)
        self._select_current()
