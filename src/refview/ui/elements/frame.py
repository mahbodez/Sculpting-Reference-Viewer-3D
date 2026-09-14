"""A titled frame that folds away behind its own bar.

Every group of controls in the application is one of these, so that the same
gesture opens and closes all of them and a panel can be pared down to the two
groups someone is actually working in.  The bar is drawn rather than styled:
a style sheet can colour a group box but it cannot make its title the thing
you click, and being able to click the title is most of the point.

A frame that is switched off folds itself shut.  Controls that cannot be used
are worse than absent -- they take up the room of controls that can -- so a
frame whose contents have gone dead gets out of the way and leaves its bar
behind to say why.  Opening it again is still possible; it is a fold, not a
lock.
"""

from __future__ import annotations

from PySide6.QtCore import QEvent, QRect, QRectF, QSize, Qt, Signal
from PySide6.QtGui import QFont, QPainter, QPen
from PySide6.QtWidgets import (
    QFormLayout,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from . import palette

#: How tall a frame's bar is.  Two lines of a form row, near enough, which is
#: the smallest bar that still reads as a bar rather than as a rule.
BAR_HEIGHT = 22

#: Whether a group folds itself away when its settings go dead.  The rule the
#: panels were rebuilt around -- a control that cannot be used is worse than
#: absent, because it takes the room of one that can -- but a rule somebody is
#: entitled to switch off, so it is a number read at the moment it applies
#: rather than a branch compiled into the class.  See
#: :class:`refview.core.preferences.InterfacePreferences`.
FOLD_DISABLED = True


def set_fold_disabled(fold: bool) -> None:
    """Whether a group that goes dead folds away or merely greys out.

    Turning it back on does not fold the groups that are already dead and
    open: a frame folds on the event that switches it off, and one that was
    switched off while the rule was not in force never saw that event.  It
    will fold the next time it goes dead, which is the moment anybody would
    be looking.
    """
    global FOLD_DISABLED
    FOLD_DISABLED = bool(fold)

#: How far the mark beside a group's name sits in from the left, and across.
_ARROW_INSET = 5
_DOT_SIZE = 6


def _title_ink(live: bool, hover: bool):
    """What colour a group's name is written in."""
    if not live:
        return palette.INK_DIM
    return palette.INK if hover else palette.INK_SOFT


class FrameBar(QWidget):
    """The bar across the top of a :class:`Frame`: its name and its fold."""

    #: The bar was clicked, which is the frame's cue to fold or unfold.
    toggled = Signal()

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._title = title
        self._open = True
        self._foldable = True
        self._hover = False
        self.setFixedHeight(BAR_HEIGHT)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

    def title(self) -> str:
        return self._title

    def set_title(self, title: str) -> None:
        self._title = title
        self.update()

    def set_open(self, is_open: bool) -> None:
        self._open = bool(is_open)
        self.update()

    def set_foldable(self, foldable: bool) -> None:
        self._foldable = bool(foldable)
        self.setCursor(
            Qt.CursorShape.PointingHandCursor if foldable else Qt.CursorShape.ArrowCursor
        )
        self.update()

    # -- interaction -----------------------------------------------------

    def enterEvent(self, event) -> None:  # noqa: N802 - Qt contract
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802 - Qt contract
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802 - Qt contract
        inside = self.rect().contains(event.position().toPoint())
        if self._foldable and event.button() == Qt.MouseButton.LeftButton and inside:
            self.toggled.emit()
        super().mouseReleaseEvent(event)

    # -- painting --------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt contract
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        rect = self.rect()
        live = self.isEnabled()

        # No fill and no border: a group is marked by its name and by the
        # space around it.  A bar drawn behind every group turns a panel of
        # eight into eight stripes, which is a lot of ink spent saying only
        # that the groups are separate -- which their names already say.
        left = _ARROW_INSET
        if self._foldable:
            self._draw_dot(painter, left, live)
            left += _DOT_SIZE + 7

        font = QFont(self.font())
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(_title_ink(live, self._hover))
        text_rect = QRect(left, rect.top(), max(rect.width() - left - 6, 0), rect.height())
        elided = painter.fontMetrics().elidedText(
            self._title, Qt.TextElideMode.ElideRight, text_rect.width()
        )
        painter.drawText(
            text_rect,
            int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
            elided,
        )

    def _draw_dot(self, painter: QPainter, left: int, live: bool) -> None:
        """The mark beside a group's name: filled when open, a ring when shut.

        It is the fold arrow's job done by something that takes less room and
        reads at a glance down a column of eight of them -- lit means open.
        """
        middle = self.rect().center().y() + 1
        box = QRectF(left, middle - _DOT_SIZE / 2, _DOT_SIZE, _DOT_SIZE)
        colour = palette.ACCENT if live else palette.INK_DIM
        if self._open:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(colour)
        else:
            painter.setPen(QPen(colour, 1.4))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            box = box.adjusted(0.7, 0.7, -0.7, -0.7)
        painter.drawEllipse(box)

    def sizeHint(self) -> QSize:  # noqa: N802 - Qt contract
        return QSize(80, BAR_HEIGHT)

    def minimumSizeHint(self) -> QSize:  # noqa: N802 - Qt contract
        return QSize(40, BAR_HEIGHT)


class Frame(QWidget):
    """A named box of controls that folds away behind its bar."""

    #: Opened or closed, by hand or otherwise.
    folded = Signal(bool)

    def __init__(
        self,
        title: str,
        expanded: bool = True,
        foldable: bool = True,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._bar = FrameBar(title, self)
        self._bar.set_foldable(foldable)
        self._body = QWidget(self)
        self._body.setAutoFillBackground(False)
        self._body.setObjectName("frame_body")
        #: Whether this frame was open before something switched it off, so
        #: that switching it back on puts it back the way it was found.
        self._open_before_disabled: bool | None = None

        column = QVBoxLayout(self)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(0)
        column.addWidget(self._bar)
        column.addWidget(self._body)

        self._bar.toggled.connect(self.toggle)
        self.set_expanded(expanded)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

    # -- the parts -------------------------------------------------------

    def bar(self) -> FrameBar:
        return self._bar

    def body(self) -> QWidget:
        return self._body

    def form(self) -> QFormLayout | None:
        """The rows inside the frame.

        ``layout()`` is the frame's own, which stacks the bar above the body
        and is no business of anything filling the frame in.  This is what a
        caller means when it asks a group for its layout.
        """
        inner = self._body.layout()
        return inner if isinstance(inner, QFormLayout) else None

    def title(self) -> str:
        return self._bar.title()

    def set_title(self, title: str) -> None:
        self._bar.set_title(title)

    # -- folding ---------------------------------------------------------

    def is_expanded(self) -> bool:
        return self._body.isVisibleTo(self)

    def set_expanded(self, expanded: bool) -> None:
        expanded = bool(expanded)
        if expanded == self._body.isVisibleTo(self):
            self._bar.set_open(expanded)
            return
        self._body.setVisible(expanded)
        self._bar.set_open(expanded)
        self.updateGeometry()
        self.folded.emit(expanded)

    def toggle(self) -> None:
        self.set_expanded(not self.is_expanded())

    # -- switching off ---------------------------------------------------

    def changeEvent(self, event) -> None:  # noqa: N802 - Qt contract
        if event.type() == QEvent.Type.EnabledChange and FOLD_DISABLED:
            if not self.isEnabled():
                if self._open_before_disabled is None:
                    self._open_before_disabled = self.is_expanded()
                self.set_expanded(False)
            elif self._open_before_disabled is not None:
                was_open, self._open_before_disabled = self._open_before_disabled, None
                self.set_expanded(was_open)
        super().changeEvent(event)

    # -- geometry --------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt contract
        super().paintEvent(event)
        if not self.is_expanded():
            # Closed, the frame is its bar and nothing else, and the bar
            # paints itself.
            return
        # A hairline under the name, stopping short of the right-hand edge:
        # enough to tie the rows below to the name above without drawing a box
        # round every group in the panel.
        rect = self.rect()
        painter = QPainter(self)
        painter.setPen(QPen(palette.WELL.lighter(160), 1))
        under = rect.top() + BAR_HEIGHT - 1
        painter.drawLine(rect.left() + 4, under, rect.right() - 4, under)

    def hasHeightForWidth(self) -> bool:  # noqa: N802 - Qt contract
        layout = self._body.layout()
        return bool(layout is not None and layout.hasHeightForWidth())

    def heightForWidth(self, width: int) -> int:  # noqa: N802 - Qt contract
        if not self.is_expanded():
            return BAR_HEIGHT
        layout = self._body.layout()
        if layout is None or not layout.hasHeightForWidth():
            return self.sizeHint().height()
        return BAR_HEIGHT + layout.heightForWidth(width)


def frame_form(parent: QWidget) -> QFormLayout:
    """The row layout the frames are filled with."""
    layout = QFormLayout(parent)
    layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    layout.setFormAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
    layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.DontWrapRows)
    layout.setContentsMargins(7, 6, 7, 7)
    layout.setHorizontalSpacing(6)
    layout.setVerticalSpacing(4)
    return layout


def framed(title: str, expanded: bool = True) -> tuple[Frame, QFormLayout]:
    """A frame with a form layout in it, ready to be filled."""
    frame = Frame(title, expanded)
    return frame, frame_form(frame.body())
