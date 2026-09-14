"""The slider the whole application is set with.

One flat bar: the name of the setting along the left, the number along the
right, and how far along the range it stands shown by how much of the bar is
filled.  Drag it to set it, double-click it to type a number in.  That is the
control a sculpting application is mostly made of, and the reason to draw it
rather than to assemble it out of a groove, a handle and a spin box is density:
this is one row tall and still says what it is and what it is set to, where the
three-piece version costs two rows or half the panel's width.

A slider may be given a ``ceiling`` above its ``maximum``, which makes the end
of the bar a soft one: a number typed past it is accepted and the bar grows to
reach it.  That is for the settings where the useful range and the possible
range are different sizes -- where a bar covering everything possible would
spend most of its length on values nobody wants, and a bar covering only what
is useful would be a wall.  Typing past the end says "further than this", and
from then on the bar can be dragged over the wider range too.  It only ever
grows, because a range that shrank back would throw away the room that was
just asked for.
"""

from __future__ import annotations

from PySide6.QtCore import QRect, QSize, Qt, Signal
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QLineEdit, QSizePolicy, QWidget

from . import palette

#: How tall a slider is: a row of text, with the track underneath it.
SLIDER_HEIGHT = 22

#: The narrowest a slider is ever given.  Below this the number has nowhere to
#: go and the bar is not worth dragging, so the panel scrolls instead.
MIN_WIDTH = 54

#: How much slower a drag moves the value while Ctrl is held.
_FINE = 0.2

#: The track across the foot of the bar: how far in from each end it starts,
#: how thick it is, and how far up from the bottom edge it sits.
_TRACK_INSET = 3
_TRACK_HEIGHT = 2
_TRACK_DROP = 3

#: The upright marking the end of the track.
_GRIP_WIDTH = 3
_GRIP_RISE = 3


class ValueSlider(QWidget):
    """A named, filled bar that sets one number."""

    #: Every change, including each pixel of a drag.  What most settings want.
    valueChanged = Signal(float)
    #: Only where the value comes to rest: the end of a drag, or a number
    #: typed in.  For settings whose change costs real work, so that dragging
    #: one does not pay that cost at every value it passes through.
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
        caption: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._minimum = float(minimum)
        self._maximum = float(maximum)
        self._ceiling = self._maximum if ceiling is None else max(float(ceiling), self._maximum)
        self._decimals = int(decimals)
        self._step = float(step) if step else (self._maximum - self._minimum) / 100.0
        self._suffix = suffix
        self._caption = caption
        self._value = 0.0
        self._hover = False
        self._dragging = False
        self._drag_origin = 0.0
        self._drag_value = 0.0
        self._editor: QLineEdit | None = None

        self.setFixedHeight(SLIDER_HEIGHT)
        self.setMinimumWidth(MIN_WIDTH)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setCursor(Qt.CursorShape.SizeHorCursor)
        self.set_value(value)

    # -- the value -------------------------------------------------------

    def value(self) -> float:
        return self._value

    def minimum(self) -> float:
        return self._minimum

    def maximum(self) -> float:
        return self._maximum

    def ceiling(self) -> float:
        return self._ceiling

    def decimals(self) -> int:
        return self._decimals

    def step(self) -> float:
        return self._step

    def suffix(self) -> str:
        return self._suffix

    def caption(self) -> str:
        return self._caption

    def set_caption(self, caption: str) -> None:
        self._caption = caption
        self.update()

    def set_range(
        self, minimum: float, maximum: float, ceiling: float | None = None
    ) -> None:
        """Re-scale the bar, e.g. once a model's size is known."""
        self._minimum, self._maximum = float(minimum), float(maximum)
        self._ceiling = self._maximum if ceiling is None else max(float(ceiling), self._maximum)
        self.set_value(self._value)

    def set_value(self, value: float) -> None:
        """Put the bar at a value without telling anyone it moved."""
        value = min(max(float(value), self._minimum), self._ceiling)
        self._reach(value)
        if value != self._value:
            self._value = value
        self.update()

    def _reach(self, value: float) -> None:
        """Grow the bar to take in a value from beyond its end."""
        if value > self._maximum:
            self._maximum = min(value, self._ceiling)

    def _write(self, value: float, commit: bool) -> None:
        """Set the value the way a hand on the control would."""
        value = min(max(float(value), self._minimum), self._ceiling)
        self._reach(value)
        changed = value != self._value
        self._value = value
        self.update()
        if changed:
            self.valueChanged.emit(value)
        if commit:
            self.valueCommitted.emit(value)

    # -- the text --------------------------------------------------------

    def text(self) -> str:
        return f"{self._value:.{self._decimals}f}{self._suffix}"

    # -- pointing at it --------------------------------------------------

    def _value_at(self, x: float) -> float:
        """The value the track stands at ``x`` pixels across."""
        span = max(self.width() - 2 * _TRACK_INSET, 1)
        fraction = min(max((x - _TRACK_INSET) / span, 0.0), 1.0)
        return self._minimum + fraction * (self._maximum - self._minimum)

    def _fraction(self) -> float:
        span = self._maximum - self._minimum
        if span <= 0:
            return 0.0
        return min(max((self._value - self._minimum) / span, 0.0), 1.0)

    def enterEvent(self, event) -> None:  # noqa: N802 - Qt contract
        self._hover = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:  # noqa: N802 - Qt contract
        self._hover = False
        self.update()
        super().leaveEvent(event)

    def mousePressEvent(self, event) -> None:  # noqa: N802 - Qt contract
        if event.button() != Qt.MouseButton.LeftButton or self._editor is not None:
            super().mousePressEvent(event)
            return
        self.setFocus(Qt.FocusReason.MouseFocusReason)
        self._dragging = True
        self._drag_origin = event.position().x()
        self._drag_value = self._value
        if not event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            # A plain click jumps to where it landed, which is what makes the
            # bar a bar rather than a knob you have to find first.
            self._write(self._value_at(event.position().x()), commit=False)
        event.accept()

    def mouseMoveEvent(self, event) -> None:  # noqa: N802 - Qt contract
        if not self._dragging:
            super().mouseMoveEvent(event)
            return
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            span = max(self.width() - 2, 1)
            moved = (event.position().x() - self._drag_origin) / span
            reach = (self._maximum - self._minimum) * moved * _FINE
            self._write(self._drag_value + reach, commit=False)
        else:
            self._write(self._value_at(event.position().x()), commit=False)
        event.accept()

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802 - Qt contract
        if self._dragging and event.button() == Qt.MouseButton.LeftButton:
            self._dragging = False
            self.valueCommitted.emit(self._value)
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:  # noqa: N802 - Qt contract
        self._dragging = False
        self.begin_editing()
        event.accept()

    def wheelEvent(self, event) -> None:  # noqa: N802 - Qt contract
        notches = event.angleDelta().y() / 120.0
        if not notches:
            return
        scale = _FINE if event.modifiers() & Qt.KeyboardModifier.ControlModifier else 1.0
        self._write(self._value + notches * self._step * scale, commit=True)
        event.accept()

    def keyPressEvent(self, event) -> None:  # noqa: N802 - Qt contract
        keys = {
            Qt.Key.Key_Left: -1,
            Qt.Key.Key_Down: -1,
            Qt.Key.Key_Right: 1,
            Qt.Key.Key_Up: 1,
        }
        direction = keys.get(Qt.Key(event.key()))
        if direction is not None:
            scale = _FINE if event.modifiers() & Qt.KeyboardModifier.ControlModifier else 1.0
            self._write(self._value + direction * self._step * scale, commit=True)
            event.accept()
            return
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_F2):
            self.begin_editing()
            event.accept()
            return
        super().keyPressEvent(event)

    # -- typing a number in ----------------------------------------------

    def begin_editing(self) -> None:
        """Put a text box over the bar so an exact number can be typed."""
        if self._editor is not None:
            return
        editor = QLineEdit(f"{self._value:.{self._decimals}f}", self)
        editor.setGeometry(self.rect())
        editor.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        editor.selectAll()
        editor.editingFinished.connect(self._finish_editing)
        editor.show()
        editor.setFocus(Qt.FocusReason.OtherFocusReason)
        self._editor = editor

    def _finish_editing(self) -> None:
        editor, self._editor = self._editor, None
        if editor is None:
            return
        text = editor.text().strip().removesuffix(self._suffix.strip())
        editor.deleteLater()
        try:
            typed = float(text)
        except ValueError:
            self.update()
            return
        self._write(typed, commit=True)

    def focusOutEvent(self, event) -> None:  # noqa: N802 - Qt contract
        if self._editor is not None and not self._editor.hasFocus():
            self._finish_editing()
        super().focusOutEvent(event)

    # -- painting --------------------------------------------------------

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt contract
        if self._editor is not None:
            return
        painter = QPainter(self)
        rect = self.rect()
        live = self.isEnabled()

        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(palette.FACE_DOWN if self._hover and live else palette.WELL)
        painter.drawRoundedRect(
            rect.adjusted(0, 0, -1, -1), palette.RADIUS, palette.RADIUS
        )
        palette.outline(
            painter, rect, palette.ACCENT if self.hasFocus() and live else palette.EDGE
        )

        # How far along the range it stands is a thin track across the foot of
        # the bar rather than the bar filled in.  A bar filled to the value is
        # a block of colour whose size is the setting, and a panel of twenty
        # of those is twenty blocks of colour competing with the model; a
        # track is the same information in two pixels.
        span = rect.width() - 2 * _TRACK_INSET
        foot = rect.bottom() - _TRACK_DROP
        painter.setPen(Qt.PenStyle.NoPen)
        # The whole track first, dim: a slider standing at nought still has to
        # look like a slider, and a bar with nothing drawn in it looks like a
        # readout.
        painter.setBrush(palette.EDGE.darker(115) if live else palette.WELL.lighter(125))
        painter.drawRect(QRect(_TRACK_INSET, foot, span, _TRACK_HEIGHT))

        filled = int(round(self._fraction() * span))
        colour = palette.ACCENT_FILL
        if not live:
            colour = palette.INK_DIM
        elif self._hover or self._dragging:
            colour = palette.ACCENT_LIVE
        painter.setBrush(colour)
        if filled > 0:
            painter.drawRect(QRect(_TRACK_INSET, foot, filled, _TRACK_HEIGHT))
        # A short upright at the end of the track, so the exact value can be
        # read off, and aimed at, without hunting along a fading bar.
        grip = min(
            max(_TRACK_INSET + filled - _GRIP_WIDTH // 2, _TRACK_INSET),
            rect.right() - _GRIP_WIDTH,
        )
        painter.drawRect(
            QRect(grip, foot - _GRIP_RISE, _GRIP_WIDTH, _TRACK_HEIGHT + _GRIP_RISE)
        )

        painter.setFont(self.font())
        metrics = painter.fontMetrics()
        # The words sit above the track rather than across it.
        inner = rect.adjusted(6, 0, -6, -_TRACK_DROP - _TRACK_HEIGHT)

        number = self.text()
        number_width = metrics.horizontalAdvance(number)
        painter.setPen(palette.INK if live else palette.INK_DIM)
        painter.drawText(
            inner,
            int(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter),
            number,
        )

        if self._caption:
            room = inner.width() - number_width - 8
            if room > 12:
                painter.setPen(palette.INK_SOFT if live else palette.INK_DIM)
                painter.drawText(
                    QRect(inner.left(), inner.top(), room, inner.height()),
                    int(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter),
                    metrics.elidedText(self._caption, Qt.TextElideMode.ElideRight, room),
                )

    def sizeHint(self) -> QSize:  # noqa: N802 - Qt contract
        return QSize(140, SLIDER_HEIGHT)

    def minimumSizeHint(self) -> QSize:  # noqa: N802 - Qt contract
        return QSize(MIN_WIDTH, SLIDER_HEIGHT)
