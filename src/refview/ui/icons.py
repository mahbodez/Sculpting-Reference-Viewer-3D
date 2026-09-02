"""Small painted icons.

Drawing the padlock rather than shipping an image file keeps it crisp at any
scale, keeps the repository free of binary assets, and sidesteps the question
of which fonts on which machine happen to carry the emoji.
"""

from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap

_LOCKED_COLOR = QColor(150, 156, 164)
_UNLOCKED_COLOR = QColor(240, 180, 41)
_CACHE: dict[tuple[bool, int], QIcon] = {}


def lock_icon(locked: bool, size: int = 16) -> QIcon:
    """A padlock, shut or hanging open.

    Open reads as "this measurement will move if you drag it", so it is drawn
    in the warning colour: an unlocked dimension is the exceptional state.
    """
    key = (locked, size)
    if key not in _CACHE:
        _CACHE[key] = QIcon(_render(locked, size))
    return _CACHE[key]


def _render(locked: bool, size: int) -> QPixmap:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    try:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        color = _LOCKED_COLOR if locked else _UNLOCKED_COLOR

        shackle = QPen(color, max(size * 0.11, 1.2))
        shackle.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(shackle)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        # The hoop's ends land on the top of the body when shut; opening it
        # slides the hoop sideways and lifts it clear.
        left = size * (0.28 if locked else 0.44)
        top = size * (0.26 if locked else 0.20)
        painter.drawArc(QRectF(left, top, size * 0.44, size * 0.44), 0, 180 * 16)

        painter.setPen(QPen(color.darker(150), max(size * 0.06, 1.0)))
        painter.setBrush(color)
        painter.drawRoundedRect(
            QRectF(size * 0.16, size * 0.48, size * 0.68, size * 0.40),
            size * 0.12,
            size * 0.12,
        )
    finally:
        painter.end()
    return pixmap
