"""One dock per panel, with a bar of its own across the top.

Every panel is its own dock, so any of them can be dragged to any edge of the
window, stacked with others into a tab strip, or floated off on its own.  The
alternative -- one dock holding a tab widget -- is one decision for all ten
panels: you can have the controls on the left or on the right, and that is the
whole of the freedom.  Ten docks is ten decisions, which is what it takes
before someone can put the two panels they are working between side by side.

The bar is ours rather than Qt's because a panel's switch belongs on it: the
one that says whether what the panel draws is on the model at all.  That has
to be reachable without opening the panel -- most of the time the question is
"take the armature off for a second", not "edit the armature" -- and a dock
that is tabbed behind another has nothing showing except its bar.
"""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QFont, QPainter, QPen
from PySide6.QtWidgets import (
    QCheckBox,
    QDockWidget,
    QHBoxLayout,
    QSizePolicy,
    QStyle,
    QToolButton,
    QWidget,
)

from . import palette

#: How wide and tall the show/hide switch is.  Square, because with the tick
#: box given no size by the theme what is left is the face of a button, and a
#: switch with no words on it has to be given a size of its own.
SWITCH_SIZE = 15

#: How tall a dock's bar is.  A little taller than a frame's, so that the two
#: do not read as the same rank of thing when a dock's first group is open --
#: and tall enough that a bold name has a pixel above and below it, which at
#: the height a title bar wants to be is not a given.
BAR_HEIGHT = 26


class DockTitle(QWidget):
    """The bar across the top of a dock: a switch, a name and two buttons."""

    #: The close button was pressed.
    closed = Signal()
    #: The float button was pressed.
    floated = Signal()

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._title = title
        self._switch: QCheckBox | None = None
        self.setFixedHeight(BAR_HEIGHT)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        row = QHBoxLayout(self)
        row.setContentsMargins(5, 0, 1, 0)
        row.setSpacing(1)
        row.addStretch(1)
        self._row = row

        self._float = self._button(
            QStyle.StandardPixmap.SP_TitleBarNormalButton, "Float this panel"
        )
        self._float.clicked.connect(self.floated.emit)
        self._close = self._button(
            QStyle.StandardPixmap.SP_TitleBarCloseButton, "Close this panel"
        )
        self._close.clicked.connect(self.closed.emit)
        row.addWidget(self._float, 0)
        row.addWidget(self._close, 0)

    def _button(self, pixmap: QStyle.StandardPixmap, tip: str) -> QToolButton:
        button = QToolButton(self)
        button.setIcon(self.style().standardIcon(pixmap))
        button.setIconSize(QSize(10, 10))
        button.setAutoRaise(True)
        button.setFixedSize(15, 15)
        button.setToolTip(tip)
        button.setCursor(Qt.CursorShape.ArrowCursor)
        return button

    def sizeHint(self) -> QSize:  # noqa: N802 - Qt contract
        """As tall as the bar really is.

        A dock puts the panel directly below its title bar's *hint*, not below
        the title bar.  Leave the hint to the layout and it comes back as the
        height of the little buttons in the corner, the panel is laid over the
        bottom third of the bar, and every panel's name loses its lower half
        -- a fixed height on the widget does not help, because that is not the
        number the dock reads.
        """
        return QSize(super().sizeHint().width(), BAR_HEIGHT)

    def minimumSizeHint(self) -> QSize:  # noqa: N802 - Qt contract
        return QSize(super().minimumSizeHint().width(), BAR_HEIGHT)

    def title(self) -> str:
        return self._title

    def set_title(self, title: str) -> None:
        self._title = title
        self.update()

    def add_switch(self, tip: str) -> QCheckBox:
        """Put a show/hide switch at the left of the bar and return it."""
        switch = make_switch(tip, self)
        self._row.insertWidget(0, switch, 0)
        self._switch = switch
        return switch

    def switch(self) -> QCheckBox | None:
        return self._switch

    # -- dragging ---------------------------------------------------------

    def mousePressEvent(self, event) -> None:  # noqa: N802 - Qt contract
        # Let the press fall through to the dock, which is what moves it.  A
        # custom title bar that swallowed this would be a dock that cannot be
        # dragged anywhere, which is the entire point of having ten of them.
        event.ignore()

    def mouseMoveEvent(self, event) -> None:  # noqa: N802 - Qt contract
        event.ignore()

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802 - Qt contract
        event.ignore()

    def mouseDoubleClickEvent(self, event) -> None:  # noqa: N802 - Qt contract
        event.ignore()

    # -- painting ---------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt contract
        painter = QPainter(self)
        rect = self.rect()
        painter.fillRect(rect, palette.HEADER)
        painter.setPen(QPen(palette.EDGE_LIT, 1))
        painter.drawLine(rect.left(), rect.top(), rect.right(), rect.top())
        painter.setPen(QPen(palette.EDGE, 1))
        painter.drawLine(rect.left(), rect.bottom(), rect.right(), rect.bottom())

        left = 5
        if self._switch is not None:
            left = self._switch.geometry().right() + 5

        font = QFont(self.font())
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(palette.INK)
        room = max(self._float.geometry().left() - left - 4, 0)
        if room > 8:
            painter.drawText(
                left,
                rect.top(),
                room,
                rect.height(),
                int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
                painter.fontMetrics().elidedText(
                    self._title, Qt.TextElideMode.ElideRight, room
                ),
            )


class PanelDock(QDockWidget):
    """A dock that can go anywhere, with :class:`DockTitle` across the top."""

    def __init__(self, key: str, title: str, parent: QWidget | None = None) -> None:
        super().__init__(title, parent)
        self._key = key
        self.setObjectName(f"dock_{key}")
        self.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
            | QDockWidget.DockWidgetFeature.DockWidgetClosable
        )
        self._bar = DockTitle(title, self)
        self._bar.closed.connect(self.close)
        self._bar.floated.connect(lambda: self.setFloating(not self.isFloating()))
        self.setTitleBarWidget(self._bar)

    def key(self) -> str:
        return self._key

    def bar(self) -> DockTitle:
        return self._bar

    def setWindowTitle(self, title: str) -> None:  # noqa: N802 - Qt contract
        super().setWindowTitle(title)
        self._bar.set_title(title)


class Switch(QCheckBox):
    """A square that is on or off, and is clickable all over.

    A check box decides where it can be clicked by asking the style, and the
    style works that out from the box, the gap and the words -- none of which
    this has, because the theme turns a check box into a plain lit button and
    this one carries no text.  What comes back is an empty rectangle, and a
    control with an empty click rectangle is one that quietly does nothing.

    So it answers the question itself: all of it is the target.  Which is what
    you would want anyway for something fifteen pixels across.
    """

    def hitButton(self, point) -> bool:  # noqa: N802 - Qt contract
        return self.rect().contains(point)


def make_switch(tip: str, parent: QWidget | None = None) -> QCheckBox:
    """The square that shows or hides what a panel draws.

    One is kept on each dock's own bar, and another is hung on that dock's tab
    when it is stacked behind others -- which is most of the time, and is
    exactly when being able to take the armature off the model without first
    finding the armature panel is worth the most.  Both drive the same panel
    and both are refreshed from it, so which one you reach for never matters.
    """
    switch = Switch(parent)
    switch.setProperty("refviewSwitch", True)
    switch.setToolTip(tip)
    switch.setCursor(Qt.CursorShape.ArrowCursor)
    switch.setFixedSize(SWITCH_SIZE, SWITCH_SIZE)
    return switch
