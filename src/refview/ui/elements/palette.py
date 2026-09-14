"""The colours the hand-drawn elements paint with.

Kept apart from :mod:`refview.ui.theme` because the theme dresses the widgets
Qt draws and this dresses the ones we draw ourselves, and the two have to
agree or the panels look like two applications sharing a window.  Everything
here is a plain ``QColor`` so a painter can reach for it without going through
a style sheet.

The scheme is a warm neutral grey with a single amber accent -- the palette a
sculpting application wants, because every colour that is not the model is a
colour competing with it.  Amber rather than blue: it reads as "this is live"
against grey without ever being mistaken for part of a matcap.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

#: Behind everything.
BACKDROP = QColor(38, 38, 38)
#: A panel's own ground.
PANEL = QColor(46, 46, 46)
#: A group's body.  The same as the panel: a group is marked out by its name
#: and the space around it, not by being a different colour.
BODY = QColor(46, 46, 46)
#: The strip a stack of docks is tabbed along.
HEADER = QColor(54, 54, 54)
#: That strip's chosen tab.
HEADER_OPEN = QColor(64, 64, 64)
#: Sunken things: the inside of a slider, the well of a list.
WELL = QColor(35, 35, 35)
#: The face of a button.
FACE = QColor(58, 58, 58)
#: A button under the cursor.
FACE_DOWN = QColor(72, 72, 72)

#: Words.
INK = QColor(201, 201, 201)
#: Words that are only there to name something.
INK_SOFT = QColor(160, 160, 160)
#: Words on something switched off.
INK_DIM = QColor(110, 110, 110)

#: The one colour that is not grey: a switch that is on, the track of a
#: slider, the dot beside a group's name.  Used for the state of things and
#: for nothing else, so that what is lit is always what is live.
ACCENT = QColor(237, 139, 33)
#: The track of a slider at rest.
ACCENT_FILL = QColor(237, 139, 33)
#: The track of the slider under the cursor, or being dragged.
ACCENT_LIVE = QColor(255, 164, 66)
#: Words on something the accent has filled.
ON_INK = QColor(26, 26, 26)

#: The hairline round a control.  Lighter than what it encloses, not darker:
#: on a dark ground an outline is what separates one control from the next,
#: and a dark line on a dark ground separates nothing.
EDGE = QColor(86, 86, 86)
#: A stronger outline, for the edge of a whole group.
EDGE_LIT = QColor(106, 106, 106)

#: A cloned element wears this, so it is always clear which control is the one
#: that lives in a panel and which is the copy standing in for it.
CLONE_TAG = QColor(96, 148, 196)


#: How far a control's corners are rounded.
RADIUS = 4


def outline(painter, rect, color: QColor | None = None, radius: int = RADIUS) -> None:
    """Draw the hairline that separates a control from the panel.

    One line, the same on all four sides, a shade lighter than what it
    encloses.  Not a bevel: the relief that makes a control look moulded
    belongs to a light interface, and on a dark one it reads as grime.  What
    does the work here is the outline and the space around it.
    """
    from PySide6.QtGui import QPen

    painter.setPen(QPen(color or EDGE, 1))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), radius, radius)


def css(color: QColor, alpha: float = 1.0) -> str:
    """A colour as a style sheet function, for the parts Qt draws."""
    if alpha >= 1.0:
        return f"rgb({color.red()},{color.green()},{color.blue()})"
    return f"rgba({color.red()},{color.green()},{color.blue()},{alpha:.3f})"


def set_accent(color: QColor) -> None:
    """Change the one colour that is not grey, everywhere at once.

    The hand-painted elements reach for ``palette.ACCENT`` at the moment they
    paint rather than holding on to a copy from when they were built, which is
    what makes this possible: rebinding the name here is enough, and the next
    repaint is in the new colour.  The two shades beside it are derived rather
    than asked for, because what they mean -- the track at rest, the track
    under the cursor -- is a relationship to the accent and not an independent
    choice anybody wants to make twice.

    :func:`refview.ui.theme.apply_dark_theme` still has to be run afterwards
    for the half of the interface Qt paints, which reads its colours through a
    style sheet built once rather than at every repaint.
    """
    global ACCENT, ACCENT_FILL, ACCENT_LIVE, ON_INK
    ACCENT = QColor(color)
    ACCENT_FILL = QColor(color)
    ACCENT_LIVE = QColor(color).lighter(115)
    # Words sitting on the accent: black on a light accent, white on a dark
    # one.  A fixed near-black works for the amber this ships with and turns
    # illegible the moment somebody chooses a deep blue.
    lightness = (
        0.2126 * color.redF() + 0.7152 * color.greenF() + 0.0722 * color.blueF()
    )
    ON_INK = QColor(26, 26, 26) if lightness > 0.5 else QColor(238, 238, 238)
