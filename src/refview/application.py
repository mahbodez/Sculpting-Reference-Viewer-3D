"""Command-line entry point and application bootstrap."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontMetrics, QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QSplashScreen

from . import APP_NAME, __version__
from .paths import available_matcaps, image_path
from .ui.main_window import MainWindow
from .ui.theme import apply_dark_theme
from .ui.viewport import configure_surface_format


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="refview",
        description="A 3D reference viewer for clay sculpting: matcaps, shading and measurements.",
    )
    parser.add_argument(
        "model", nargs="?", type=Path, help="model to open on startup (OBJ, STL, GLB or glTF)"
    )
    parser.add_argument("--matcap", type=Path, help="matcap image to apply on startup")
    parser.add_argument("--session", type=Path, help="session file to restore on startup")
    return parser


def run(argv: list[str] | None = None) -> int:
    """Start the viewer and block until the window closes."""
    arguments = build_parser().parse_args(argv)

    configure_surface_format()
    app = QApplication(sys.argv[:1])
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("refview")
    app.setWindowIcon(QPixmap(str(image_path("icon-large.png"))))
    apply_dark_theme(app)

    splash = _create_splash()
    splash.show()
    app.processEvents()
    window = MainWindow()
    _apply_startup_arguments(window, arguments)
    window.show()
    splash.finish(window)
    return app.exec()


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
    if arguments.model is not None:
        window.open_model(arguments.model)
    if arguments.session is not None:
        window.load_session(arguments.session)

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
