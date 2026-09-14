"""The window the controls reference is read in.

It was a message box, which is the wrong shape for a page of prose: a message
box sizes itself to whatever it is handed, so a reference that grows as the
application does eventually grows past the bottom of the screen, and it has no
scroll bar to rescue it when it does.  It is also modal, which means the one
thing you cannot do while reading how a shortcut works is try the shortcut.

So: an ordinary window, scrolled, resizable, remembered at the size it was
left, and not modal.  A search box across the top, because a page this long is
one somebody arrives at with a particular question.
"""

from __future__ import annotations

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QKeySequence, QShortcut, QTextDocument
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

#: Where the window's size is remembered.
_GEOMETRY = "help/geometry"


class ControlsWindow(QWidget):
    """A scrolled, searchable page of prose."""

    def __init__(self, html: str, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Controls")
        self.resize(680, 760)

        column = QVBoxLayout(self)
        column.setContentsMargins(10, 10, 10, 10)
        column.setSpacing(8)

        self._find = QLineEdit()
        self._find.setPlaceholderText("Find...")
        self._find.setClearButtonEnabled(True)
        self._note = QLabel("")
        self._note.setMinimumWidth(90)
        previous = QPushButton("Previous")
        following = QPushButton("Next")
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)
        row.addWidget(self._find, 1)
        row.addWidget(previous, 0)
        row.addWidget(following, 0)
        row.addWidget(self._note, 0)
        column.addLayout(row)

        self._page = QTextBrowser()
        self._page.setOpenExternalLinks(True)
        self._page.setHtml(html)
        column.addWidget(self._page, 1)

        self._find.returnPressed.connect(lambda: self._seek(forwards=True))
        self._find.textChanged.connect(lambda _text: self._note.clear())
        following.clicked.connect(lambda: self._seek(forwards=True))
        previous.clicked.connect(lambda: self._seek(forwards=False))
        for keys in ("Ctrl+F", "/"):
            shortcut = QShortcut(QKeySequence(keys), self)
            shortcut.activated.connect(self._find.setFocus)
        close = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        close.activated.connect(self.close)

        saved = QSettings().value(_GEOMETRY)
        if saved is not None and not isinstance(saved, str):
            self.restoreGeometry(saved)

    def _seek(self, forwards: bool) -> None:
        """Find the next occurrence, wrapping round the end."""
        wanted = self._find.text()
        if not wanted:
            return
        flags = QTextDocument.FindFlag(0)
        if not forwards:
            flags |= QTextDocument.FindFlag.FindBackward
        if self._page.find(wanted, flags):
            self._note.clear()
            return
        # Off the end: go back to the other end and try once more, so that
        # pressing Return repeatedly cycles rather than stopping.
        cursor = self._page.textCursor()
        cursor.movePosition(
            cursor.MoveOperation.End if not forwards else cursor.MoveOperation.Start
        )
        self._page.setTextCursor(cursor)
        self._note.setText("" if self._page.find(wanted, flags) else "Not found")

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt contract
        QSettings().setValue(_GEOMETRY, self.saveGeometry())
        super().closeEvent(event)
