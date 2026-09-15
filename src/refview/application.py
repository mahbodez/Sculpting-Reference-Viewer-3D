"""Command-line entry point and application bootstrap."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QEvent, Qt
from PySide6.QtGui import QFont, QFontMetrics, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QMessageBox, QSplashScreen

from . import APP_NAME, __version__
from .paths import available_matcaps, image_path
from .ui.main_window import MainWindow
from .ui.preferences import store as preference_store
from .ui.theme import apply_dark_theme
from .ui.viewport import configure_surface_format


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="refview",
        description="A 3D reference viewer for clay sculpting: matcaps, shading and measurements.",
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        metavar="FILE",
        help=(
            "files to open on startup: a model (OBJ, STL, GLB or glTF), a session "
            "(JSON) or a matcap image.  This is also how a file arrives when the "
            "desktop opens it with the viewer or it is dragged onto the application."
        ),
    )
    parser.add_argument("--matcap", type=Path, help="matcap image to apply on startup")
    parser.add_argument("--session", type=Path, help="session file to restore on startup")
    return parser


def run(argv: list[str] | None = None) -> int:
    """Start the viewer and block until the window closes."""
    arguments = build_parser().parse_args(argv)

    # Before the application object, not after: the settings are found by the
    # organisation and application name, and the first thing read out of them
    # is the multisample count, which belongs to the GL context and so has to
    # be decided before there is one.  Setting the two names on QCoreApplication
    # is how that is done without a QApplication to hang them on yet.
    QCoreApplication.setApplicationName(APP_NAME)
    QCoreApplication.setOrganizationName("refview")
    preferences = preference_store().value

    configure_surface_format(preferences.viewport.samples)
    app = Application(sys.argv[:1])
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("refview")
    app.setWindowIcon(QPixmap(str(image_path("icon-large.png"))))
    apply_dark_theme(app)

    splash = _create_splash() if preferences.startup.show_splash else None
    if splash is not None:
        splash.show()
        app.processEvents()
    window = MainWindow()
    _apply_startup_arguments(window, arguments)
    app.requests.deliver_to(window)
    window.show()
    if splash is not None:
        splash.finish(window)
    return app.exec()


class OpenRequests:
    """Files the desktop asked the viewer to open, kept until there is a window.

    On Windows and most Linux desktops a file opened with the viewer arrives
    on the command line.  On macOS it does not: Finder starts the bundle
    with no arguments and then sends the file as an event, once for the
    file that launched it and again for every file opened while it is
    running.  The first of those can land before the window exists, so a
    request made early is held and delivered with the window.
    """

    def __init__(self) -> None:
        self._pending: list[Path] = []
        self._window: MainWindow | None = None

    def open(self, path: str | Path) -> None:
        """Open ``path`` in the window, or hold it until there is one."""
        path = Path(path)
        if self._window is None:
            self._pending.append(path)
            return
        self._window.open_path(path)

    def deliver_to(self, window: MainWindow) -> None:
        """Name the window files go to, and hand over any that came early."""
        self._window = window
        pending, self._pending = self._pending, []
        for path in pending:
            self.open(path)

    @property
    def pending(self) -> tuple[Path, ...]:
        return tuple(self._pending)


class Application(QApplication):
    """The Qt application, listening for the desktop's way of handing over a file."""

    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)
        self.requests = OpenRequests()

    def event(self, event) -> bool:  # noqa: N802 - Qt naming
        if event.type() == QEvent.Type.FileOpen:
            self.requests.open(event.file())
            return True
        return super().event(event)


def _fitted_title_font(width: int) -> QFont:
    """Largest title font that still draws the whole app name inside ``width``."""
    font = QFont("Georgia", max(24, width // 22))
    font.setWeight(QFont.Weight.DemiBold)
    while (
        font.pointSize() > 12
        and QFontMetrics(font).horizontalAdvance(APP_NAME) > width
    ):
        font.setPointSize(font.pointSize() - 1)
    return font


def _create_splash() -> QSplashScreen:
    pixmap = QPixmap(str(image_path("splashscreen.png")))
    screen = QApplication.primaryScreen()
    if screen is not None:
        available = screen.availableGeometry().size()
        pixmap = pixmap.scaled(
            min(available.width() - 120, 1280),
            min(available.height() - 160, 720),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

    painter = QPainter(pixmap)
    margin = max(24, pixmap.width() // 18)
    title_font = _fitted_title_font(pixmap.width() - 2 * margin)
    painter.setPen(Qt.GlobalColor.white)
    painter.setFont(title_font)
    painter.drawText(
        margin,
        pixmap.height() // 2,
        QFontMetrics(title_font).horizontalAdvance(APP_NAME) + 1,
        title_font.pointSize() * 2,
        Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
        APP_NAME,
    )
    version_font = QFont("Georgia", max(11, pixmap.width() // 75))
    version_font.setWeight(QFont.Weight.Normal)
    painter.setPen(Qt.GlobalColor.lightGray)
    painter.setFont(version_font)
    painter.drawText(
        margin,
        pixmap.height() // 2 + title_font.pointSize() * 2,
        f"Version {__version__}",
    )
    painter.end()
    splash = QSplashScreen(pixmap, Qt.WindowType.WindowStaysOnTopHint)
    return splash


def _apply_startup_arguments(window: MainWindow, arguments: argparse.Namespace) -> None:
    """Open whatever the command line asked for, falling back to sane defaults."""
    opened = False
    for path in arguments.files:
        if not window.open_path(path):
            QMessageBox.warning(
                window,
                "Open",
                f"{path.name} is not a model, session or matcap the viewer can open.",
            )
            continue
        opened = True
    if arguments.session is not None:
        window.load_session(arguments.session)
    elif not opened:
        # Nothing was asked for, so the artist's own answer applies: carry on
        # with the session they were last in, if they asked to.  A file named
        # on the command line beats it, because that is somebody opening this
        # application *at* something.
        window.reopen_last_session()

    matcap = arguments.matcap
    if matcap is None and window.state.render.matcap_path is None:
        # Start on the first bundled matcap rather than the plain built-in one.
        candidates = available_matcaps()
        matcap = candidates[0] if candidates else None
    if matcap is not None:
        window.load_matcap(matcap)


def main() -> None:
    raise SystemExit(run(sys.argv[1:]))


if __name__ == "__main__":  # pragma: no cover
    main()
