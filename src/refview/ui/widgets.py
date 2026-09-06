"""Small reusable controls shared by the side panels."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QColorDialog,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QPushButton,
    QScrollArea,
    QSlider,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class SliderSpin(QWidget):
    """A float slider paired with a spin box, kept in sync.

    The slider works in integer steps internally; ``decimals`` controls both
    the spin box display and the slider resolution.
    """

    #: Every change, including each pixel of a drag.  What most controls want.
    valueChanged = Signal(float)
    #: Only where the value comes to rest: the end of a drag, or a number
    #: typed into the box.  For settings whose change costs real work, so that
    #: dragging one does not pay that cost at every value it passes through.
    valueCommitted = Signal(float)

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
        self._slider.sliderReleased.connect(self._on_release)
        self._spin.valueChanged.connect(self._on_spin)
        self.set_value(value)

    def value(self) -> float:
        return self._spin.value()

    def set_range(self, minimum: float, maximum: float) -> None:
        """Re-scale the control, e.g. once a model's size is known."""
        self._minimum, self._maximum = minimum, maximum
        current = self.value()
        for widget, converted in (
            (self._slider, (int(minimum * self._scale), int(maximum * self._scale))),
            (self._spin, (minimum, maximum)),
        ):
            blocked = widget.blockSignals(True)
            widget.setRange(*converted)
            widget.blockSignals(blocked)
        self.set_value(current)

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
        # A change that did not come from a drag -- an arrow key, the wheel, a
        # click on the groove -- has already come to rest.
        if not self._slider.isSliderDown():
            self.valueCommitted.emit(value)

    def _on_release(self) -> None:
        self.valueCommitted.emit(self.value())

    def _on_spin(self, value: float) -> None:
        blocked = self._slider.blockSignals(True)
        self._slider.setValue(int(value * self._scale))
        self._slider.blockSignals(blocked)
        self.valueChanged.emit(value)
        # The box does not track keystrokes, so this is already the final word.
        self.valueCommitted.emit(value)


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


def scrollable(widget: QWidget) -> QScrollArea:
    """Wrap a panel so it scrolls when it is taller than the dock.

    The controls keep their natural height and the viewport grows to the dock's
    width, which is what stops a long panel from squashing its own rows.
    """
    area = QScrollArea()
    area.setWidget(widget)
    area.setWidgetResizable(True)
    area.setFrameShape(QFrame.Shape.NoFrame)
    area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    return area


def _panel_form(parent: QWidget) -> QFormLayout:
    """The row layout every group in the side panels is built on."""
    layout = QFormLayout(parent)
    layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(6)
    return layout


def form_group(title: str) -> tuple[QGroupBox, QFormLayout]:
    """A titled group box with a form layout, ready to be filled."""
    box = QGroupBox(title)
    return box, _panel_form(box)


class CollapsibleGroup(QWidget):
    """A group whose rows fold away behind its title.

    For settings that are worth having but not worth reading past: they stay
    out of the way of the controls an artist actually reaches for, and the
    panel is no longer than it was until someone asks for them.
    """

    def __init__(self, title: str, expanded: bool = False, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._header = QToolButton()
        self._header.setText(title)
        self._header.setCheckable(True)
        self._header.setAutoRaise(True)
        self._header.setCursor(Qt.CursorShape.PointingHandCursor)
        self._header.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self._header.setStyleSheet("QToolButton { border: none; padding: 2px; }")

        self._body = QFrame()
        self._body.setFrameShape(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        layout.addWidget(self._header)
        layout.addWidget(self._body)

        self._header.toggled.connect(self._on_toggled)
        self.set_expanded(expanded)

    def body(self) -> QFrame:
        return self._body

    def is_expanded(self) -> bool:
        return self._header.isChecked()

    def set_expanded(self, expanded: bool) -> None:
        self._header.setChecked(expanded)
        self._on_toggled(expanded)

    def _on_toggled(self, expanded: bool) -> None:
        self._header.setArrowType(
            Qt.ArrowType.DownArrow if expanded else Qt.ArrowType.RightArrow
        )
        self._body.setVisible(expanded)


def collapsible_group(
    title: str, expanded: bool = False
) -> tuple[CollapsibleGroup, QFormLayout]:
    """A folded-away group with a form layout, shaped like :func:`form_group`."""
    group = CollapsibleGroup(title, expanded)
    return group, _panel_form(group.body())
