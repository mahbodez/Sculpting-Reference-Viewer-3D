"""Recording a film on a thread, without taking the process down with it.

The rest of the film suite is pure arithmetic and needs no Qt.  This is the
part that does, because what it guards against is not a wrong answer but a
crash: a QThread that is destroyed while it is still running does not raise,
it aborts the process outright, and the way an artist meets that is by moving
a slider while a recording is in flight.

Every setting change abandons the recording it no longer wants, so that path
is walked constantly in normal use.  What must survive it is the thread: it is
told to stop and then held on to until it says it has, rather than being
dropped on the floor the moment nobody wants its film any more.
"""

from __future__ import annotations

import pytest

from refview.core import plane_volume
from refview.core.mesh import Mesh
from refview.core.plane_clusters import plane_regions
from refview.core.plane_film import film_key
from refview.core.settings import PlaneSettings, SculptMode

QtCore = pytest.importorskip("PySide6.QtCore")
QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from refview.ui.film_recorder import FilmRecorder  # noqa: E402 - needs Qt first
from test_plane_solids import TEST_RESOLUTION, ball  # noqa: E402 - path fixture


@pytest.fixture(scope="session")
def app():
    """One Qt application for the whole run; offscreen, so CI needs no display.

    Deliberately never destroyed.  A QApplication that is torn down while Qt
    still holds objects queued for deletion aborts the interpreter, and there
    is nothing to gain by tidying it away microseconds before the process
    exits anyway -- so it is made once and left alone.
    """
    import os

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    existing = QtWidgets.QApplication.instance()
    yield existing or QtWidgets.QApplication([])


@pytest.fixture(autouse=True)
def coarse_lattice(monkeypatch: pytest.MonkeyPatch) -> None:
    """Read every model on a small lattice, so the suite stays quick."""
    monkeypatch.setattr(plane_volume, "RESOLUTION", TEST_RESOLUTION)
    monkeypatch.setattr("refview.core.plane_solids.RESOLUTION", TEST_RESOLUTION)


def run_until(app, done, timeout_ms: int = 30_000) -> bool:
    """Pump the event loop until ``done()`` or the clock runs out."""
    clock = QtCore.QElapsedTimer()
    clock.start()
    while not done() and clock.elapsed() < timeout_ms:
        app.processEvents(QtCore.QEventLoop.ProcessEventsFlag.AllEvents, 20)
    return done()


def recorded(mesh: Mesh, settings: PlaneSettings):
    planes = plane_regions(mesh).for_count(settings.sculpt_count)
    return planes, film_key(settings, settings.coefficients)


def test_changing_a_setting_mid_recording_does_not_take_the_process_down(app) -> None:
    """The bug this file exists for.

    A recording is abandoned by every change to a setting it is built from,
    and the abandoning used to drop the last reference to a running QThread --
    which Qt answers by aborting.  Restarting over and over is what a drag of
    the Detail slider does, so it has to be survivable.
    """
    mesh = ball()
    recorder = FilmRecorder()
    try:
        for detail in (20.0, 24.0, 28.0, 32.0, 36.0):
            settings = PlaneSettings(
                sculpt=SculptMode.SUBTRACTIVE, sculpt_detail=detail, sculpt_film=True
            )
            planes, key = recorded(mesh, settings)
            recorder.start(mesh, planes, settings, key)
            # Let it get properly under way before pulling the rug out, so the
            # thread really is running when the next start abandons it.
            run_until(app, lambda: bool(recorder.film and len(recorder.film)), 5_000)
        assert recorder.recording
    finally:
        recorder.wait()
    assert not recorder.recording


def test_an_abandoned_thread_is_held_until_it_has_really_stopped(app) -> None:
    """Not merely told to stop: kept alive until it says it has.

    Letting go of a QThread the instant it is unwanted is the crash; the pile
    of retiring threads is what stands between the two, and it has to empty
    itself as they finish rather than growing without bound.
    """
    mesh = ball()
    recorder = FilmRecorder()
    try:
        settings = PlaneSettings(
            sculpt=SculptMode.SUBTRACTIVE, sculpt_detail=30.0, sculpt_film=True
        )
        planes, key = recorded(mesh, settings)
        recorder.start(mesh, planes, settings, key)
        run_until(app, lambda: bool(recorder.film and len(recorder.film)), 5_000)

        recorder.abandon()
        assert recorder.film is None  # the film is gone at once
        assert recorder._retiring, "a running thread was dropped rather than held"
        # And the pile clears itself once the thread actually finishes.
        assert run_until(app, lambda: not recorder._retiring, 30_000)
    finally:
        recorder.wait()


def test_a_recording_says_whether_it_is_running(app) -> None:
    """Which is what the panel puts its controls to sleep by, so it has to be
    true while a film is being made and false the moment it is not."""
    mesh = ball()
    recorder = FilmRecorder()
    try:
        assert not recorder.recording
        settings = PlaneSettings(
            sculpt=SculptMode.ADDITIVE,
            sculpt_detail=20.0,
            sculpt_masses=2,
            sculpt_film=True,
        )
        planes, key = recorded(mesh, settings)
        recorder.start(mesh, planes, settings, key)
        assert recorder.recording

        settled: list = []
        recorder.settled.connect(lambda *_: settled.append(True))
        assert run_until(app, lambda: bool(settled), 60_000), "the film never finished"
        assert recorder.film is not None and recorder.film.complete
    finally:
        recorder.wait()


def test_waiting_survives_a_thread_qt_has_already_cleaned_up(app) -> None:
    """Shutdown must not care whether the thread beat it to the exit.

    A recording that finishes between being put on the retiring pile and being
    waited for leaves a Python handle to a deleted C++ object, and touching it
    raises.  That is the good case -- the thread is gone -- so it must not be
    the thing that crashes the window on the way out.
    """
    mesh = ball()
    recorder = FilmRecorder()
    settings = PlaneSettings(
        sculpt=SculptMode.SUBTRACTIVE, sculpt_detail=20.0, sculpt_film=True
    )
    planes, key = recorded(mesh, settings)
    recorder.start(mesh, planes, settings, key)

    settled: list = []
    recorder.settled.connect(lambda *_: settled.append(True))
    run_until(app, lambda: bool(settled), 60_000)
    # Wait twice: the second finds a pile whose threads are already deleted.
    recorder.wait()
    recorder.wait()
    assert not recorder.recording


def test_a_film_is_only_handed_back_for_the_settings_that_made_it(app) -> None:
    """The guard that decides whether to scrub an existing film or record a
    new one.  Getting it wrong is what would show one form under another
    form's label."""
    mesh = ball()
    recorder = FilmRecorder()
    try:
        settings = PlaneSettings(
            sculpt=SculptMode.SUBTRACTIVE, sculpt_detail=20.0, sculpt_film=True
        )
        planes, key = recorded(mesh, settings)
        recorder.start(mesh, planes, settings, key)
        assert recorder.matching(key) is not None
        assert recorder.matching(("something", "else")) is None
    finally:
        recorder.wait()
