"""Command-line entry point and application bootstrap."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from .paths import available_matcaps
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
    app.setApplicationName("Reference Viewer")
    app.setOrganizationName("refview")
    apply_dark_theme(app)

    window = MainWindow()
    _apply_startup_arguments(window, arguments)
    window.show()
    return app.exec()


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
