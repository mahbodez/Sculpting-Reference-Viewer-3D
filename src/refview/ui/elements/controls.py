"""The small controls that are not sliders: a swatch, and a point in space."""

from __future__ import annotations

from PySide6.QtCore import QRect, QSize, Qt, Signal
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QColorDialog,
    QDoubleSpinBox,
    QHBoxLayout,
    QSizePolicy,
    QWidget,
)

from . import palette

#: How tall the swatch and the point boxes are, so a row of them lines up with
#: a row of sliders.
ROW_HEIGHT = 20

#: The widest a colour swatch is drawn.
SWATCH_WIDTH = 76


class ColorButton(QWidget):
    """A swatch that opens a colour picker.

    Colours are exchanged as 0-1 RGB tuples, matching the settings dataclasses.
    Drawn rather than styled so that it keeps its border and its sunken well
    whatever the colour is, including the ones that would otherwise disappear
    into the panel behind them.
    """

    colorChanged = Signal(tuple)

    def __init__(self, color: tuple[float, float, float], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._color = tuple(float(channel) for channel in color)
        self._hover = False
        self.setFixedHeight(ROW_HEIGHT)
        self.setMinimumWidth(28)
        # A swatch is read, not filled in: at the width of a whole row a
        # saturated colour is the loudest thing on the panel, and what it is
        # saying is only "this is the colour".  Wide enough to judge a hue
        # against the one below it is as wide as it needs to be.
        self.setMaximumWidth(SWATCH_WIDTH)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

    def color(self) -> tuple[float, float, float]:
        return self._color

    def set_color(self, color: tuple[float, float, float]) -> None:
        self._color = tuple(float(channel) for channel in color)
        self.update()

    def _qcolor(self) -> QColor:
        red, green, blue = (
            int(round(min(max(channel, 0.0), 1.0) * 255)) for channel in self._color
        )
        return QColor(red, green, blue)

    def enterEvent(self, event) -> None:  # noqa: N802 - Qt contract
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802 - Qt contract
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802 - Qt contract
        if event.button() == Qt.MouseButton.LeftButton and self.rect().contains(
            event.position().toPoint()
        ):
            self.choose()
        super().mouseReleaseEvent(event)

    def choose(self) -> None:
        """Open the picker, as a click on the swatch does."""
        chosen = QColorDialog.getColor(self._qcolor(), self, "Select colour")
        if chosen.isValid():
            self.set_color((chosen.redF(), chosen.greenF(), chosen.blueF()))
            self.colorChanged.emit(self._color)

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt contract
        painter = QPainter(self)
        rect = self.rect()
        painter.fillRect(rect, palette.WELL)
        swatch = rect.adjusted(2, 2, -2, -2)
        colour = self._qcolor()
        if not self.isEnabled():
            grey = (colour.red() + colour.green() + colour.blue()) // 3
            colour = QColor(grey, grey, grey).darker(130)
        painter.fillRect(swatch, colour)
        lit = self._hover and self.isEnabled()
        painter.setPen(QPen(palette.ACCENT if lit else palette.EDGE, 1))
        painter.drawRect(rect.adjusted(0, 0, -1, -1))

    def sizeHint(self) -> QSize:  # noqa: N802 - Qt contract
        return QSize(60, ROW_HEIGHT)

    def minimumSizeHint(self) -> QSize:  # noqa: N802 - Qt contract
        return QSize(28, ROW_HEIGHT)


class PointEdit(QWidget):
    """Three boxes for one point in space.

    Keyboard tracking is off, so a typed number arrives once it is finished
    rather than at every digit: each change here is an undo step, and the edit
    it drives can be as large as rebuilding a whole armature.  The arrows and
    the wheel still step live, which is what makes nudging a point by hand
    feel like nudging it.

    The axis letters are painted into the boxes rather than set beside them,
    because a caption beside each of three boxes is three captions' worth of
    width spent on three letters.
    """

    #: The whole point, whichever axis moved.
    valueChanged = Signal(tuple)

    #: Far enough to hold any scene, in any unit anyone is likely to choose.
    REACH = 1e7

    AXES = ("X", "Y", "Z")

    def __init__(self, decimals: int = 2, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._boxes: list[QDoubleSpinBox] = []
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        for axis in self.AXES:
            box = _AxisBox(axis)
            box.setDecimals(decimals)
            box.setRange(-self.REACH, self.REACH)
            box.setSingleStep(0.1)
            box.setKeyboardTracking(False)
            box.setMinimumWidth(46)
            box.valueChanged.connect(self._emit)
            layout.addWidget(box, 1)
            self._boxes.append(box)

    def value(self) -> tuple[float, float, float]:
        first, second, third = (box.value() for box in self._boxes)
        return (first, second, third)

    def set_value(self, point) -> None:
        for box, value in zip(self._boxes, point, strict=True):
            blocked = box.blockSignals(True)
            box.setValue(float(value))
            box.blockSignals(blocked)

    def decimals(self) -> int:
        return self._boxes[0].decimals()

    def set_decimals(self, decimals: int) -> None:
        for box in self._boxes:
            box.setDecimals(decimals)

    def set_step(self, step: float) -> None:
        """Match the arrows to the size of the thing being moved."""
        for box in self._boxes:
            box.setSingleStep(max(step, 10.0**-box.decimals()))

    def _emit(self) -> None:
        self.valueChanged.emit(self.value())


class _AxisBox(QDoubleSpinBox):
    """A spin box with its axis letter written faintly down its left."""

    def __init__(self, axis: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._axis = axis
        self.setFixedHeight(ROW_HEIGHT)
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt contract
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(palette.INK_SOFT if self.isEnabled() else palette.INK_DIM)
        painter.drawText(
            QRect(4, 0, 12, self.height()),
            int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
            self._axis,
        )
