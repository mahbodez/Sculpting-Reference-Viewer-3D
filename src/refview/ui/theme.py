"""A dark theme, so the viewport is what draws the eye.

The colours themselves live in :mod:`refview.ui.elements.palette`, because
half the controls are painted by hand and the other half are painted by Qt,
and if the two took their colours from different places they would drift.
This is the half Qt paints.

The look is borrowed from the sculpting applications an artist already has
open: a dark neutral ground, flat faces separated by hairlines rather than by
moulding, and one orange kept for the state of things -- a switch that is on,
the track of a slider, the dot beside a group's name -- so that what is lit is
always what is live.  Rows are packed close, because a panel you can read
without scrolling is a panel you stop having to think about.
"""

from __future__ import annotations

from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication

from .elements import palette as ink
from .elements.dock import SWITCH_SIZE
from .elements.palette import RADIUS, css
from .elements.toggles import WholeFaceToggles

#: Interface type size, in pixels.  A module-level number rather than a
#: literal in the sheet below, because the Preferences window can change it
#: and the whole of the interface is measured against it: a row is as tall as
#: the words in it, so the panels grow and shrink with this and nothing has to
#: be told about it separately.
FONT_SIZE = 11


def set_font_size(size: int) -> None:
    """Set the interface type size; run :func:`apply_dark_theme` afterwards."""
    global FONT_SIZE
    FONT_SIZE = int(size)


def _stylesheet() -> str:
    """The style sheet, written out of the palette so the two cannot disagree."""
    return f"""
QWidget {{
    font-size: {FONT_SIZE}px;
}}
QMainWindow, QDialog {{
    background: {css(ink.BACKDROP)};
}}
QMainWindow::separator {{
    background: {css(ink.EDGE)};
    width: 4px;
    height: 4px;
}}
QMainWindow::separator:hover {{
    background: {css(ink.ACCENT_FILL)};
}}

/* -- docks ---------------------------------------------------------- */
QDockWidget {{
    background: {css(ink.PANEL)};
    titlebar-close-icon: none;
    titlebar-normal-icon: none;
}}
QDockWidget > QWidget {{
    background: {css(ink.PANEL)};
}}
QScrollArea {{
    background: {css(ink.PANEL)};
    border: none;
}}
QScrollArea > QWidget > QWidget {{
    background: {css(ink.PANEL)};
}}

/* The strip of tabs along the bottom of a stack of docks. */
QTabBar::tab {{
    background: {css(ink.HEADER)};
    color: {css(ink.INK_SOFT)};
    border: 1px solid {css(ink.EDGE)};
    /* Tight, because the strip holds one tab per panel and the names on
       them are the only way to tell one from another. */
    padding: 3px 6px;
    margin-right: 1px;
}}
QTabBar::tab:selected {{
    background: {css(ink.HEADER_OPEN)};
    color: {css(ink.INK)};
    border-bottom: 2px solid {css(ink.ACCENT)};
}}
QTabBar::tab:!selected:hover {{
    background: {css(ink.FACE)};
    color: {css(ink.INK)};
}}
QTabWidget::pane {{
    border: 1px solid {css(ink.EDGE)};
}}

/* -- the menu bar --------------------------------------------------- */
QMenuBar {{
    background: {css(ink.HEADER)};
    color: {css(ink.INK)};
    border-bottom: 1px solid {css(ink.EDGE)};
}}
QMenuBar::item {{
    padding: 4px 9px;
    background: transparent;
}}
QMenuBar::item:selected {{
    background: {css(ink.ACCENT)};
    color: {css(ink.ON_INK)};
}}
QMenu {{
    background: {css(ink.PANEL)};
    color: {css(ink.INK)};
    border: 1px solid {css(ink.EDGE)};
    padding: 3px;
}}
QMenu::item {{
    padding: 4px 22px 4px 22px;
    border-radius: {RADIUS}px;
}}
QMenu::item:selected {{
    background: {css(ink.ACCENT)};
    color: {css(ink.ON_INK)};
}}
QMenu::item:disabled {{
    color: {css(ink.INK_DIM)};
}}
QMenu::separator {{
    height: 1px;
    background: {css(ink.EDGE)};
    margin: 4px 6px;
}}

/* -- buttons -------------------------------------------------------- */
/* Flat, with the same hairline the hand-drawn controls carry.  Lit when it
   is on, which for a button is the only state worth colouring. */
QPushButton {{
    background: {css(ink.FACE)};
    color: {css(ink.INK)};
    border: 1px solid {css(ink.EDGE)};
    border-radius: {RADIUS}px;
    padding: 3px 8px;
    min-height: 15px;
    text-align: center;
}}
QPushButton:hover {{
    background: {css(ink.FACE_DOWN)};
}}
QPushButton:pressed, QPushButton:checked {{
    background: {css(ink.ACCENT)};
    border-color: {css(ink.ACCENT)};
    /* Dark words on the lit face: the accent is bright enough that light
       ones on it are the hardest thing in the panel to read. */
    color: {css(ink.ON_INK)};
}}
QPushButton:disabled {{
    background: {css(ink.PANEL)};
    color: {css(ink.INK_DIM)};
}}
QToolButton {{
    background: transparent;
    border: none;
    border-radius: {RADIUS}px;
    padding: 2px;
}}
QToolButton:hover {{
    background: {css(ink.FACE_DOWN)};
}}
QToolButton:pressed, QToolButton:checked {{
    background: {css(ink.ACCENT)};
}}

/* -- boxes with text or a list in them ------------------------------ */
QLineEdit, QSpinBox, QDoubleSpinBox, QPlainTextEdit, QTextEdit {{
    background: {css(ink.WELL)};
    color: {css(ink.INK)};
    border: 1px solid {css(ink.EDGE)};
    border-radius: {RADIUS}px;
    padding: 1px 4px;
    selection-background-color: {css(ink.ACCENT_FILL)};
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
    border-color: {css(ink.ACCENT)};
}}
/* The two tiny arrows on a spin box are a control nobody aims at, and at
   this size they are barely visible either.  The box is typed into, or the
   wheel is rolled over it, both of which were always the real gestures. */
QAbstractSpinBox {{
    qproperty-buttonSymbols: NoButtons;
}}
QComboBox {{
    background: {css(ink.FACE)};
    color: {css(ink.INK)};
    border: 1px solid {css(ink.EDGE)};
    border-radius: {RADIUS}px;
    padding: 1px 4px;
    min-height: 16px;
}}
QComboBox:hover {{
    background: {css(ink.FACE_DOWN)};
}}
QComboBox::drop-down {{
    border: none;
    width: 14px;
}}
QComboBox QAbstractItemView {{
    background: {css(ink.WELL)};
    color: {css(ink.INK)};
    border: 1px solid {css(ink.EDGE)};
    selection-background-color: {css(ink.ACCENT_FILL)};
    outline: none;
}}
QTreeWidget, QListWidget, QTreeView, QListView, QTableView {{
    background: {css(ink.WELL)};
    color: {css(ink.INK)};
    border: 1px solid {css(ink.EDGE)};
    border-radius: {RADIUS}px;
    alternate-background-color: {css(ink.PANEL)};
    outline: none;
}}
QTreeWidget::item:selected, QListWidget::item:selected,
QTreeView::item:selected, QListView::item:selected {{
    background: {css(ink.ACCENT_FILL)};
    color: {css(ink.INK)};
}}
QHeaderView::section {{
    background: {css(ink.HEADER)};
    color: {css(ink.INK_SOFT)};
    border: none;
    border-right: 1px solid {css(ink.EDGE)};
    padding: 2px 5px;
}}

/* -- switches -------------------------------------------------------
   A switch is a button that stays down, not a box with a tick in it.  It
   is the same shape and the same size as the buttons around it, it lights
   when it is on, and the whole of it is the target rather than a twelve
   pixel square at one end -- which is the difference between glancing at a
   panel and reading it.  The tick box itself is given no size at all, so
   what is left is the word on the face of a button. */
QCheckBox, QRadioButton {{
    background: {css(ink.FACE)};
    color: {css(ink.INK)};
    border: 1px solid {css(ink.EDGE)};
    border-radius: {RADIUS}px;
    padding: 3px 8px;
    spacing: 0;
    min-height: 15px;
}}
QCheckBox:hover, QRadioButton:hover {{
    background: {css(ink.FACE_DOWN)};
}}
QCheckBox:checked, QRadioButton:checked {{
    background: {css(ink.ACCENT)};
    border-color: {css(ink.ACCENT)};
    color: {css(ink.ON_INK)};
}}
QCheckBox:disabled, QRadioButton:disabled {{
    background: {css(ink.PANEL)};
    color: {css(ink.INK_DIM)};
}}
QCheckBox:checked:disabled, QRadioButton:checked:disabled {{
    background: {css(ink.ACCENT_FILL.darker(160))};
    border-color: {css(ink.ACCENT_FILL.darker(160))};
}}
/* The tick box itself is given nothing at all: no size, no border, no
   image.  Leaving any of those out leaves Qt drawing the remains of one,
   which arrives as a stray mark in front of every label. */
QCheckBox::indicator, QRadioButton::indicator {{
    width: 0px;
    height: 0px;
    margin: 0px;
    padding: 0px;
    border: none;
    background: transparent;
    image: none;
}}

/* The little square on a dock's bar and on its tab.  It has no words on it,
   so the padding that shapes the rest of them would leave it with a content
   rectangle of negative width -- and a control with no content rectangle is
   one that cannot be clicked, which is the whole of what it is for. */
QCheckBox[refviewSwitch="true"] {{
    padding: 0px;
    min-width: {SWITCH_SIZE}px;
    max-width: {SWITCH_SIZE}px;
    min-height: {SWITCH_SIZE}px;
    max-height: {SWITCH_SIZE}px;
}}

/* -- the plain Qt slider, for the few places one is still used ------- */
QSlider::groove:horizontal {{
    background: {css(ink.WELL)};
    border: 1px solid {css(ink.EDGE)};
    height: 4px;
    border-radius: {RADIUS}px;
}}
QSlider::sub-page:horizontal {{
    background: {css(ink.ACCENT_FILL)};
    border-radius: {RADIUS}px;
}}
QSlider::handle:horizontal {{
    background: {css(ink.FACE_DOWN)};
    border: 1px solid {css(ink.EDGE)};
    width: 8px;
    margin: -5px 0;
    border-radius: {RADIUS}px;
}}
QSlider::handle:horizontal:hover {{
    background: {css(ink.ACCENT)};
}}

/* -- splitters and scrollbars --------------------------------------- */
QSplitter::handle {{
    background: {css(ink.EDGE)};
}}
QSplitter::handle:hover {{
    background: {css(ink.ACCENT_FILL)};
}}
QScrollBar:vertical {{
    background: transparent;
    width: 10px;
    margin: 0;
}}
QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
    margin: 0;
}}
QScrollBar::handle {{
    background: {css(ink.FACE)};
    border-radius: 4px;
    min-height: 24px;
    min-width: 24px;
}}
QScrollBar::handle:hover {{
    background: {css(ink.FACE_DOWN)};
}}
QScrollBar::add-line, QScrollBar::sub-line {{
    height: 0;
    width: 0;
}}
QScrollBar::add-page, QScrollBar::sub-page {{
    background: transparent;
}}

/* -- odds and ends -------------------------------------------------- */
QStatusBar {{
    background: {css(ink.HEADER)};
    color: {css(ink.INK_SOFT)};
    border-top: 1px solid {css(ink.EDGE)};
}}
QToolTip {{
    background: {css(ink.WELL)};
    color: {css(ink.INK)};
    border: 1px solid {css(ink.ACCENT_FILL)};
    padding: 3px;
}}
QProgressBar {{
    background: {css(ink.WELL)};
    border: 1px solid {css(ink.EDGE)};
    border-radius: {RADIUS}px;
    text-align: center;
    color: {css(ink.INK)};
}}
QProgressBar::chunk {{
    background: {css(ink.ACCENT_FILL)};
}}
QGroupBox {{
    border: 1px solid {css(ink.EDGE)};
    border-radius: {RADIUS}px;
    margin-top: 9px;
    font-weight: 600;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 7px;
    padding: 0 3px;
    color: {css(ink.INK_SOFT)};
}}
"""


def apply_dark_theme(app: QApplication) -> None:
    """Switch the application to the Fusion style with the warm grey palette."""
    app.setStyle("Fusion")

    colours = QPalette()
    colours.setColor(QPalette.ColorRole.Window, ink.PANEL)
    colours.setColor(QPalette.ColorRole.WindowText, ink.INK)
    colours.setColor(QPalette.ColorRole.Base, ink.WELL)
    colours.setColor(QPalette.ColorRole.AlternateBase, ink.BODY)
    colours.setColor(QPalette.ColorRole.Text, ink.INK)
    colours.setColor(QPalette.ColorRole.Button, ink.FACE)
    colours.setColor(QPalette.ColorRole.ButtonText, ink.INK)
    colours.setColor(QPalette.ColorRole.ToolTipBase, ink.WELL)
    colours.setColor(QPalette.ColorRole.ToolTipText, ink.INK)
    colours.setColor(QPalette.ColorRole.Highlight, ink.ACCENT_FILL)
    colours.setColor(QPalette.ColorRole.HighlightedText, ink.INK)
    colours.setColor(QPalette.ColorRole.PlaceholderText, ink.INK_DIM)
    for role in (QPalette.ColorRole.Text, QPalette.ColorRole.ButtonText,
                 QPalette.ColorRole.WindowText):
        colours.setColor(QPalette.ColorGroup.Disabled, role, ink.INK_DIM)
    app.setPalette(colours)
    app.setStyleSheet(_stylesheet())
    # The style sheet turns every check box into a button, and Qt goes on
    # thinking only the words on it can be clicked.  See the module below.
    WholeFaceToggles.install(app)
