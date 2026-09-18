"""Small painted icons.

Drawing the padlock rather than shipping an image file keeps it crisp at any
scale, keeps the repository free of binary assets, and sidesteps the question
of which fonts on which machine happen to carry the emoji.
"""

from __future__ import annotations

from PySide6.QtCore import QPointF, QRectF, Qt
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


#: The glyphs, by name.  Each is a list of strokes in a 0-1 box, drawn with a
#: round cap so that they hold up at the sizes a panel actually uses them at.
#: Kept as line work rather than as filled shapes for the same reason: a
#: hairline scales, a silhouette turns to mud.
_STROKES: dict[str, list[list[tuple[float, float]]]] = {
    # A bin: lid, handle, body, and two lines down the inside of it.
    "trash": [
        [(0.16, 0.26), (0.84, 0.26)],
        [(0.40, 0.26), (0.40, 0.16), (0.60, 0.16), (0.60, 0.26)],
        [(0.24, 0.26), (0.30, 0.86), (0.70, 0.86), (0.76, 0.26)],
        [(0.42, 0.40), (0.44, 0.72)],
        [(0.58, 0.40), (0.56, 0.72)],
    ],
    "plus": [
        [(0.50, 0.18), (0.50, 0.82)],
        [(0.18, 0.50), (0.82, 0.50)],
    ],
    # A ring with a cross through it: put the thing in the middle of the view.
    "centre": [
        [(0.50, 0.10), (0.50, 0.30)],
        [(0.50, 0.70), (0.50, 0.90)],
        [(0.10, 0.50), (0.30, 0.50)],
        [(0.70, 0.50), (0.90, 0.50)],
    ],
    # An arrow coming back round on itself.
    "refresh": [
        [(0.82, 0.50), (0.72, 0.36), (0.88, 0.32)],
    ],
    # Two strokes crossed: stop, close, no.
    "cross": [
        [(0.24, 0.24), (0.76, 0.76)],
        [(0.76, 0.24), (0.24, 0.76)],
    ],
}

#: Which glyphs are drawn as a ring as well as their strokes.
_RINGED = {"centre", "refresh"}

_GLYPH_COLOR = QColor(206, 206, 206)
_GLYPHS: dict[tuple[str, int, int], QIcon] = {}


def glyph(name: str, size: int = 14, color: QColor | None = None) -> QIcon:
    """One of the small line drawings above, as an icon.

    A button whose whole job is "delete this" says it faster with a bin on it
    than with the word, and takes a third of the width doing so -- which in a
    panel that has to fit beside the model is most of the argument.  Only for
    the handful of actions that have a drawing everybody already knows; a verb
    nobody has a picture for stays a verb.
    """
    tint = color or _GLYPH_COLOR
    key = (name, size, tint.rgba())
    if key not in _GLYPHS:
        _GLYPHS[key] = QIcon(_draw_glyph(name, size, tint))
    return _GLYPHS[key]


def _draw_glyph(name: str, size: int, color: QColor) -> QPixmap:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    try:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        pen = QPen(color, max(size * 0.095, 1.1))
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        if name in _RINGED:
            inset = size * 0.18
            box = QRectF(inset, inset, size - 2 * inset, size - 2 * inset)
            if name == "refresh":
                painter.drawArc(box, 40 * 16, 290 * 16)
            else:
                painter.drawEllipse(box)
        for stroke in _STROKES.get(name, ()):
            points = [QPointF(x * size, y * size) for x, y in stroke]
            for start, end in zip(points, points[1:], strict=False):
                painter.drawLine(start, end)
    finally:
        painter.end()
    return pixmap
