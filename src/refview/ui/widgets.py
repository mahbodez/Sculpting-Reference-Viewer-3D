"""Small reusable controls shared by the side panels."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractButton,
    QColorDialog,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSlider,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class SliderSpin(QWidget):
    """A float slider paired with a spin box, kept in sync.

    The slider works in integer steps internally; ``decimals`` controls both
    the spin box display and the slider resolution.

    A control may be given a ``ceiling`` above its ``maximum``, which makes the
    slider's end a soft one: the box will accept a number typed past it, and
    the slider grows to reach whatever was typed.  That is for the settings
    where the useful range and the possible range are different sizes -- where
    a slider covering the whole of what is possible would spend most of its
    travel on values nobody wants, and a slider covering only what is useful
    would be a wall.  Typing past the end says "further than this", and from
    then on the slider can be dragged over the wider range as well.  It only
    ever grows, because a range that shrank back would throw away the room the
    artist just asked for.
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
        ceiling: float | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._scale = 10**decimals
        self._minimum = minimum
        self._maximum = maximum
        self._ceiling = maximum if ceiling is None else max(float(ceiling), maximum)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setRange(int(minimum * self._scale), int(maximum * self._scale))
        self._slider.setSingleStep(max(1, int((step or (maximum - minimum) / 100) * self._scale)))
        # A groove narrower than this is not worth dragging, and anything
        # wider than it is room the row is welcome to give back.
        self._slider.setMinimumWidth(48)

        self._spin = QDoubleSpinBox()
        self._spin.setDecimals(decimals)
        self._spin.setRange(minimum, self._ceiling)
        self._spin.setSingleStep(step or (maximum - minimum) / 100)
        self._spin.setSuffix(suffix)
        self._spin.setMinimumWidth(70)
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

    def set_range(
        self, minimum: float, maximum: float, ceiling: float | None = None
    ) -> None:
        """Re-scale the control, e.g. once a model's size is known."""
        self._minimum, self._maximum = minimum, maximum
        self._ceiling = maximum if ceiling is None else max(float(ceiling), maximum)
        current = self.value()
        for widget, converted in (
            (self._slider, (int(minimum * self._scale), int(maximum * self._scale))),
            (self._spin, (minimum, self._ceiling)),
        ):
            blocked = widget.blockSignals(True)
            widget.setRange(*converted)
            widget.blockSignals(blocked)
        self.set_value(current)

    def _reach(self, value: float) -> None:
        """Grow the slider to take in a value from beyond its end."""
        if value <= self._maximum:
            return
        self._maximum = min(value, self._ceiling)
        blocked = self._slider.blockSignals(True)
        self._slider.setRange(
            int(self._minimum * self._scale), int(self._maximum * self._scale)
        )
        self._slider.blockSignals(blocked)

    def set_value(self, value: float) -> None:
        value = min(max(value, self._minimum), self._ceiling)
        self._reach(value)
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
        self._reach(value)
        blocked = self._slider.blockSignals(True)
        self._slider.setValue(int(value * self._scale))
        self._slider.blockSignals(blocked)
        self.valueChanged.emit(value)
        # The box does not track keystrokes, so this is already the final word.
        self.valueCommitted.emit(value)


class PointEdit(QWidget):
    """Three spin boxes for one point in space.

    Keyboard tracking is off, so a typed number arrives once it is finished
    rather than at every digit: each change here is an undo step, and the edit
    it drives can be as large as rebuilding a whole armature.  The arrows and
    the wheel still step live, which is what makes nudging a point by hand
    feel like nudging it.
    """

    #: The whole point, whichever axis moved.
    valueChanged = Signal(tuple)

    #: Far enough to hold any scene, in any unit anyone is likely to choose.
    REACH = 1e7

    def __init__(self, decimals: int = 2, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._boxes: list[QDoubleSpinBox] = []
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        for axis in ("X", "Y", "Z"):
            label = QLabel(axis)
            label.setStyleSheet("color: #8f939b;")
            box = QDoubleSpinBox()
            box.setDecimals(decimals)
            box.setRange(-self.REACH, self.REACH)
            box.setSingleStep(0.1)
            box.setKeyboardTracking(False)
            box.setMinimumWidth(58)
            box.valueChanged.connect(self._emit)
            layout.addWidget(label, 0)
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

    def set_decimals(self, decimals: int) -> None:
        for box in self._boxes:
            box.setDecimals(decimals)

    def set_step(self, step: float) -> None:
        """Match the arrows to the size of the thing being moved."""
        for box in self._boxes:
            box.setSingleStep(max(step, 10.0**-box.decimals()))

    def _emit(self) -> None:
        self.valueChanged.emit(self.value())


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


#: How many characters of a combo box's own text it is allowed to insist on
#: room for.  Enough to tell one entry from another at a glance when the dock
#: has been pulled narrow, and short enough that the longest entry in a list is
#: no longer what decides how narrow the dock may go.
SQUEEZED_CHARS = 8

#: The narrowest a squeezed control is ever given, in pixels.  A check box
#: still shows its box and the start of its word here, and a combo box still
#: shows its arrow, which is enough to know what a row is while the dock is
#: pulled in.  Nought would be tidier arithmetic and would let a control
#: disappear entirely.
SQUEEZED_WIDTH = 40


def relax_widths(root: QWidget) -> None:
    """Let a panel be narrower than the sentences inside it.

    How narrow a panel will go is decided by whichever of its children insists
    hardest, and the ones that insist hardest are the ones holding words.  A
    label that cannot wrap asks for its whole line at once, so a readout that
    grows as a slider moves takes the dock wider with it and never gives the
    width back -- which is a control that resizes the window as a side effect
    of being used.  A combo box asks for its longest entry whether or not that
    entry is the one showing, and a check box asks for its text and cannot wrap
    at all.

    So labels are allowed to wrap, which drops what they ask for from a line to
    a word; and combo boxes and check boxes are told they may be squeezed, with
    their text kept in a tooltip for when they are.  None of this changes how a
    panel looks at a comfortable width.  It changes what happens when there is
    not one, which before was: the dock grew.

    Saying that to a check box takes both halves of what is below, and neither
    half does anything alone.  A layout asks a widget for a floor, and takes
    the width of its text unless the size policy says the widget may shrink --
    which for a button it does not, by default.  Grant the policy and the
    layout starts reading the widget's own minimum width instead, but only
    where that minimum is greater than nought, so a floor still has to be set
    for it to read.  Hence a policy and a number, together.

    The one thing left on a single line is the caption down the left of a form
    row.  Those are two words naming the control beside them, they are already
    as narrow as they are going to get, and wrapping one only buys a second
    line that the row -- whose height is set by the control, not by its name --
    has nowhere to put.

    Run over a whole panel once it is built, so a control added later is
    covered by the same rule as the rest without having to remember it.
    """
    captions = set()
    for form in root.findChildren(QFormLayout):
        for row in range(form.rowCount()):
            item = form.itemAt(row, QFormLayout.ItemRole.LabelRole)
            if item is not None and item.widget() is not None:
                captions.add(item.widget())
    for label in root.findChildren(QLabel):
        if label not in captions:
            label.setWordWrap(True)
    for combo in root.findChildren(QComboBox):
        combo.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )
        combo.setMinimumContentsLength(SQUEEZED_CHARS)
        _squeezable(combo)
    for button in root.findChildren(QAbstractButton):
        # A swatch or an arrow has nothing to squeeze and a width it needs.
        if not button.text():
            continue
        if not button.toolTip():
            button.setToolTip(button.text())
        _squeezable(button)


def _squeezable(widget: QWidget) -> None:
    """Let a widget be given less width than its own text asks for."""
    policy = widget.sizePolicy()
    policy.setHorizontalPolicy(QSizePolicy.Policy.Preferred)
    widget.setSizePolicy(policy)
    widget.setMinimumWidth(SQUEEZED_WIDTH)


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
