"""Small reusable controls shared by the side panels."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QColorDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QDoubleSpinBox,
    QWidget,
)


class SliderSpin(QWidget):
    """A float slider paired with a spin box, kept in sync.

    The slider works in integer steps internally; ``decimals`` controls both
    the spin box display and the slider resolution.
    """

    valueChanged = Signal(float)

    def __init__(
        self,
        minimum: float,
        maximum: float,
        value: float,
        decimals: int = 2,
        step: float | None = None,
        suffix: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._scale = 10**decimals
        self._minimum = minimum
        self._maximum = maximum

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setRange(int(minimum * self._scale), int(maximum * self._scale))
        self._slider.setSingleStep(max(1, int((step or (maximum - minimum) / 100) * self._scale)))

        self._spin = QDoubleSpinBox()
        self._spin.setDecimals(decimals)
        self._spin.setRange(minimum, maximum)
        self._spin.setSingleStep(step or (maximum - minimum) / 100)
        self._spin.setSuffix(suffix)
        self._spin.setMinimumWidth(78)
        self._spin.setKeyboardTracking(False)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.addWidget(self._slider, 1)
        layout.addWidget(self._spin, 0)

        self._slider.valueChanged.connect(self._on_slider)
        self._spin.valueChanged.connect(self._on_spin)
        self.set_value(value)

    def value(self) -> float:
        return self._spin.value()

    def set_value(self, value: float) -> None:
        value = min(max(value, self._minimum), self._maximum)
        for widget, converted in ((self._slider, int(value * self._scale)), (self._spin, value)):
            blocked = widget.blockSignals(True)
            widget.setValue(converted)
            widget.blockSignals(blocked)

    def _on_slider(self, raw: int) -> None:
        value = raw / self._scale
        blocked = self._spin.blockSignals(True)
        self._spin.setValue(value)
        self._spin.blockSignals(blocked)
        self.valueChanged.emit(value)

    def _on_spin(self, value: float) -> None:
        blocked = self._slider.blockSignals(True)
        self._slider.setValue(int(value * self._scale))
        self._slider.blockSignals(blocked)
        self.valueChanged.emit(value)


class ColorButton(QPushButton):
    """A swatch button that opens a colour picker.

    Colours are exchanged as 0-1 RGB tuples, matching the settings dataclasses.
    """

    colorChanged = Signal(tuple)

    def __init__(self, color: tuple[float, float, float], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._color = color
        self.setFixedHeight(24)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(self._choose)
        self._refresh()

    def color(self) -> tuple[float, float, float]:
        return self._color

    def set_color(self, color: tuple[float, float, float]) -> None:
        self._color = tuple(float(c) for c in color)
        self._refresh()

    def _refresh(self) -> None:
        r, g, b = (int(round(min(max(c, 0.0), 1.0) * 255)) for c in self._color)
        border = "#1c1d21" if (r + g + b) > 200 else "#8a8d95"
        self.setStyleSheet(
            f"background-color: rgb({r},{g},{b}); border: 1px solid {border}; border-radius: 3px;"
        )

    def _choose(self) -> None:
        r, g, b = (int(round(min(max(c, 0.0), 1.0) * 255)) for c in self._color)
        chosen = QColorDialog.getColor(QColor(r, g, b), self, "Select colour")
        if chosen.isValid():
            self.set_color((chosen.redF(), chosen.greenF(), chosen.blueF()))
            self.colorChanged.emit(self._color)


def form_group(title: str) -> tuple[QGroupBox, QFormLayout]:
    """A titled group box with a form layout, ready to be filled."""
    box = QGroupBox(title)
    layout = QFormLayout(box)
    layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(6)
    return box, layout
