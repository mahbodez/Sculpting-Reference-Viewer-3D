"""A neutral dark theme, so the viewport is what draws the eye."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

_BACKGROUND = QColor(38, 39, 43)
_SURFACE = QColor(46, 47, 52)
_TEXT = QColor(223, 225, 229)
_ACCENT = QColor(94, 148, 214)

_STYLESHEET = """
QGroupBox {
    border: 1px solid #43454b;
    border-radius: 4px;
    margin-top: 10px;
    font-weight: 600;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
}
QTabWidget::pane { border: 1px solid #43454b; }
QTreeWidget, QListWidget { border: 1px solid #43454b; border-radius: 3px; }
QPushButton { padding: 4px 10px; }
QPushButton:checked { background-color: #3f6ea8; }
QStatusBar { border-top: 1px solid #43454b; }
"""


def apply_dark_theme(app: QApplication) -> None:
    """Switch the application to the Fusion style with a dark palette."""
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, _BACKGROUND)
    palette.setColor(QPalette.ColorRole.WindowText, _TEXT)
    palette.setColor(QPalette.ColorRole.Base, QColor(32, 33, 36))
    palette.setColor(QPalette.ColorRole.AlternateBase, _SURFACE)
    palette.setColor(QPalette.ColorRole.Text, _TEXT)
    palette.setColor(QPalette.ColorRole.Button, _SURFACE)
    palette.setColor(QPalette.ColorRole.ButtonText, _TEXT)
    palette.setColor(QPalette.ColorRole.ToolTipBase, _SURFACE)
    palette.setColor(QPalette.ColorRole.ToolTipText, _TEXT)
    palette.setColor(QPalette.ColorRole.Highlight, _ACCENT)
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    palette.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(128, 130, 136)
    )
    palette.setColor(
        QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(128, 130, 136)
    )
    app.setPalette(palette)
    app.setStyleSheet(_STYLESHEET)
