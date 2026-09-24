"""A layout saved before a panel existed still tabs that panel in with the rest."""

from __future__ import annotations

import os

import pytest

QtCore = pytest.importorskip("PySide6.QtCore")
QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from PySide6.QtCore import QSettings  # noqa: E402
from PySide6.QtWidgets import QLabel, QMainWindow  # noqa: E402

from refview.ui.panels.base import Panel  # noqa: E402
from refview.ui.state import ViewerState  # noqa: E402
from refview.ui.workspace import Workspace  # noqa: E402


@pytest.fixture(scope="session")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    existing = QtWidgets.QApplication.instance()
    yield existing or QtWidgets.QApplication([])


class _Plain(Panel):
    def _build(self) -> None:
        self.add(QLabel("nothing"))

    def refresh(self) -> None:
        pass


def _window(state: ViewerState, keys: list[str]) -> tuple[QMainWindow, Workspace]:
    window = QMainWindow()
    window.setCentralWidget(QLabel("view"))
    workspace = Workspace(window)
    for key in keys:
        workspace.add_panel(key, key.title(), _Plain(state))
    return window, workspace


def test_a_new_panel_joins_the_tab_strip_of_an_old_layout(app, tmp_path):
    state = ViewerState()
    settings = QSettings(str(tmp_path / "layout.ini"), QSettings.Format.IniFormat)
    old, old_space = _window(state, ["model", "shading", "camera"])
    old.show()
    old_space.save(settings)
    old.close()

    new, space = _window(state, ["model", "shading", "camera", "render"])
    new.show()
    assert space.load(settings)
    render = new.findChild(QtWidgets.QDockWidget, "dock_render")
    camera = new.findChild(QtWidgets.QDockWidget, "dock_camera")
    # Qt leaves a dock its saved state does not name where it was added:
    # tabbed behind the others, not split off on its own.
    assert camera in new.tabifiedDockWidgets(render)
    new.close()
