"""Files arriving from outside: the command line, a drop, or the desktop's "Open with"."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from PySide6.QtCore import QSettings  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402

from refview import application  # noqa: E402
from refview.ui.main_window import MainWindow, opens_as  # noqa: E402


@pytest.fixture(scope="session")
def app():
    """One offscreen Qt application for the run; see test_film_recorder."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    made = QApplication.instance() or QApplication([])
    made.setOrganizationName("refview-tests")
    made.setApplicationName("refview-tests")
    return made


@pytest.fixture
def window(app):
    QSettings().clear()
    made = MainWindow()
    yield made
    made._layout_write.stop()
    made.close()
    QSettings().clear()


@pytest.fixture
def opened(window, monkeypatch):
    """What the window was asked to open, by kind, without loading anything."""
    seen = []
    monkeypatch.setattr(window, "open_model", lambda path, **_: seen.append(("model", Path(path))))
    monkeypatch.setattr(window, "load_session", lambda path, **_: seen.append(("session", Path(path))))
    monkeypatch.setattr(window, "load_matcap", lambda path: seen.append(("matcap", Path(path))))
    return seen


@pytest.mark.parametrize(
    ("name", "kind"),
    [
        ("figure.obj", "model"),
        ("FIGURE.STL", "model"),
        ("scan.glb", "model"),
        ("scan.gltf", "model"),
        ("figure.refview.json", "session"),
        ("clay.png", "matcap"),
        ("clay.JPG", "matcap"),
        ("notes.txt", None),
        ("figure", None),
    ],
)
def test_a_file_is_known_by_its_suffix(name, kind):
    assert opens_as(name) == kind


def test_the_window_opens_a_file_as_what_it_is(window, opened):
    assert window.open_path("figure.obj")
    assert window.open_path(Path("figure.refview.json"))
    assert window.open_path("clay.png")
    assert not window.open_path("notes.txt")
    assert opened == [
        ("model", Path("figure.obj")),
        ("session", Path("figure.refview.json")),
        ("matcap", Path("clay.png")),
    ]


def test_files_named_on_the_command_line_open_and_stand_in_for_the_last_session(
    window, opened, monkeypatch
):
    reopened = []
    monkeypatch.setattr(window, "reopen_last_session", lambda **_: reopened.append(True))
    arguments = application.build_parser().parse_args(["figure.obj", "clay.png"])
    application._apply_startup_arguments(window, arguments)
    assert [kind for kind, _ in opened][:2] == ["model", "matcap"]
    assert reopened == []


def test_an_empty_command_line_goes_back_to_the_last_session(window, opened, monkeypatch):
    reopened = []
    monkeypatch.setattr(window, "reopen_last_session", lambda **_: reopened.append(True))
    application._apply_startup_arguments(window, application.build_parser().parse_args([]))
    assert reopened == [True]


def test_a_file_the_desktop_hands_over_early_waits_for_the_window(window, opened):
    """Finder sends the launching file as an event, which can land before the window."""
    requests = application.OpenRequests()
    requests.open("figure.obj")
    assert requests.pending == (Path("figure.obj"),)
    assert opened == []
    requests.deliver_to(window)
    assert requests.pending == ()
    assert opened == [("model", Path("figure.obj"))]
    requests.open("clay.png")
    assert opened[-1] == ("matcap", Path("clay.png"))
