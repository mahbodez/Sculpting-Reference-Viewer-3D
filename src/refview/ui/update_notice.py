"""Background release check and the notice it puts in front of the artist.

The lookup runs on the global thread pool so a slow or unreachable GitHub never
delays the window, and a silent startup check stays silent unless there really
is something newer to install.
"""

from __future__ import annotations

from PySide6.QtCore import (
    QObject,
    QRunnable,
    QSettings,
    Qt,
    QThreadPool,
    QTimer,
    QUrl,
    Signal,
)
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMessageBox, QWidget

from .. import APP_NAME, __version__
from ..core.update_check import RELEASES_PAGE, Release, UpdateCheckError, check_for_update

#: Version the artist asked us to stop mentioning.
_SKIPPED_KEY = "updates/skipped_version"


class UpdateChecker(QObject):
    """Runs :func:`check_for_update` off the UI thread and reports back."""

    update_available = Signal(object)  # Release
    up_to_date = Signal()
    check_failed = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._running = False

    def start(self) -> None:
        """Begin a check, unless one is already in flight."""
        if self._running:
            return
        self._running = True
        QThreadPool.globalInstance().start(_CheckTask(self))

    def finish(self, release: Release | None, error: str | None) -> None:
        """Announce the outcome.  Always called on the checker's own thread."""
        self._running = False
        if error is not None:
            self.check_failed.emit(error)
        elif release is None:
            self.up_to_date.emit()
        else:
            self.update_available.emit(release)


class _CheckTask(QRunnable):
    def __init__(self, checker: UpdateChecker) -> None:
        super().__init__()
        self._checker = checker

    def run(self) -> None:  # pragma: no cover - needs a network round trip
        try:
            release = check_for_update(__version__)
        except UpdateCheckError as error:
            self._report(None, str(error))
        else:
            self._report(release, None)

    def _report(self, release: Release | None, error: str | None) -> None:
        # Hop back onto the thread that owns the checker before anything the
        # signals are wired to can touch a widget.
        checker = self._checker
        QTimer.singleShot(0, checker, lambda: checker.finish(release, error))


def is_skipped(release: Release) -> bool:
    """Whether the artist already dismissed this exact version."""
    return QSettings().value(_SKIPPED_KEY, "") == release.version


def remember_skipped(release: Release) -> None:
    QSettings().setValue(_SKIPPED_KEY, release.version)


def show_update_dialog(parent: QWidget, release: Release) -> None:
    """Offer the release page, with the option never to be asked again."""
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Information)
    box.setWindowTitle("Update Available")
    box.setTextFormat(Qt.TextFormat.RichText)
    box.setText(
        f"<b>{APP_NAME} {release.version}</b> is available.<br>You are running {__version__}."
    )
    box.setInformativeText("Downloads for every platform are on the release page.")
    box.setStandardButtons(QMessageBox.StandardButton.Close)
    open_page = box.addButton("Open Release Page", QMessageBox.ButtonRole.AcceptRole)
    skip = box.addButton("Skip This Version", QMessageBox.ButtonRole.RejectRole)
    box.setDefaultButton(open_page)
    box.exec()
    clicked = box.clickedButton()
    if clicked is open_page:
        QDesktopServices.openUrl(QUrl(release.url))
    elif clicked is skip:
        remember_skipped(release)


def show_up_to_date_dialog(parent: QWidget) -> None:
    QMessageBox.information(
        parent,
        "Check for Updates",
        f"{APP_NAME} {__version__} is the latest release.",
    )


def show_failure_dialog(parent: QWidget, error: str) -> None:
    QMessageBox.warning(
        parent,
        "Check for Updates",
        f"Could not reach GitHub: {error}\n\nRelease page: {RELEASES_PAGE}",
    )
