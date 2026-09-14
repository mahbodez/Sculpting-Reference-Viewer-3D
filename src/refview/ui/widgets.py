"""The controls the side panels are built from.

Most of what was once here now lives in :mod:`refview.ui.elements`, because a
control that can be copied out of its panel and dropped into another one needs
rather more behind it than a widget did.  What is left is the names the panels
already call things by, pointed at the new controls, and the two rules that
apply to a panel as a whole rather than to any one control in it: that it may
be squeezed narrower than the sentences inside it, and that it scrolls when it
is taller than the dock.
"""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QAbstractButton,
    QComboBox,
    QFormLayout,
    QFrame,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QWidget,
)

from .elements.controls import ColorButton, PointEdit
from .elements.frame import Frame, frame_form, framed
from .elements.slider import ValueSlider
from .icons import glyph

__all__ = [
    "SQUEEZED_CHARS",
    "SQUEEZED_WIDTH",
    "ColorButton",
    "Frame",
    "PointEdit",
    "SliderSpin",
    "ValueSlider",
    "collapsible_group",
    "form_group",
    "frame_form",
    "framed",
    "name_sliders",
    "relax_widths",
    "scrollable",
    "symbol_button",
]


class SliderSpin(ValueSlider):
    """What the panels call :class:`~refview.ui.elements.slider.ValueSlider`.

    It was a slider next to a spin box, which is where the name came from; it
    is now one bar with the number written into it.  The name is kept because
    a dozen panels say it, and because what it means -- one row that both
    shows a number and sets it -- has not changed.
    """


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

#: How wide a button carrying a drawing rather than a word is.  Square enough
#: to read as an icon, and narrow enough that a row of three of them leaves
#: the rest of the row to whatever it is acting on.
SYMBOL_WIDTH = 30


def symbol_button(name: str, meaning: str) -> QPushButton:
    """A button that carries a drawing instead of a word.

    For the few actions that already have a picture everybody knows -- a bin,
    a plus, a target.  The word it replaces becomes the tooltip, so nothing is
    lost to anyone who does not recognise the drawing, and what is gained is
    the width: three of these fit where "Centre View" alone was.

    Only where the drawing is unambiguous on its own.  A verb with no picture
    -- Dissolve, Rebuild Nodes, Append Landmarks -- stays a verb, because a
    symbol nobody can read is a button nobody presses.
    """
    button = QPushButton()
    button.setIcon(glyph(name))
    button.setIconSize(QSize(14, 14))
    button.setToolTip(meaning)
    button.setFixedWidth(SYMBOL_WIDTH)
    return button


def name_sliders(root: QWidget) -> None:
    """Move each slider's caption off the row and into the slider itself.

    A slider draws its own name down the left of its bar, so a panel that also
    puts that name in the column beside it says everything twice and pays a
    column's width for the privilege.  Taking the caption inside gives the bar
    the whole row: a wider bar is a finer one to drag, and a panel of them is
    half as wide as it was for the same controls.

    Done here, once, rather than in the dozen panels that build the rows,
    because it is a rule about how a row looks and not about what any
    particular row is for -- and because a panel that forgot would be the one
    row in the application shaped differently from the rest.

    A slider given a caption when it was built keeps it; a row whose caption
    is empty is left alone, because there was nothing to move.
    """
    for form in root.findChildren(QFormLayout):
        for row in reversed(range(form.rowCount())):
            item = form.itemAt(row, QFormLayout.ItemRole.FieldRole)
            slider = item.widget() if item is not None else None
            if not isinstance(slider, ValueSlider) or slider.caption():
                continue
            label = form.itemAt(row, QFormLayout.ItemRole.LabelRole)
            holder = label.widget() if label is not None else None
            if not isinstance(holder, QLabel) or not holder.text().strip():
                continue
            slider.set_caption(holder.text().strip())
            if not slider.toolTip():
                slider.setToolTip(holder.text().strip())
            form.takeRow(row)
            holder.setParent(None)
            holder.deleteLater()
            slider.setParent(None)
            form.insertRow(row, slider)


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


def form_group(title: str) -> tuple[Frame, QFormLayout]:
    """A named group with a form layout in it, ready to be filled."""
    return framed(title, expanded=True)


def collapsible_group(
    title: str, expanded: bool = False
) -> tuple[Frame, QFormLayout]:
    """A group that starts folded away, shaped like :func:`form_group`.

    Every group folds now, so this differs from :func:`form_group` only in
    where it starts.  It is still worth saying at the call site which groups
    are the ones nobody reads past.
    """
    return framed(title, expanded=expanded)
