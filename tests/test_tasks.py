"""Work run off the window, and the cards that show it running."""

from __future__ import annotations

import os
import threading
import time

import pytest
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from refview.core.progress import CancelledError, Progress
from refview.ui import tasks as tasks_module
from refview.ui.tasks import ProgressCard, TaskBanner, TaskRunner


@pytest.fixture(scope="session")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    return QApplication.instance() or QApplication([])


@pytest.fixture
def runner(app):
    made = TaskRunner()
    yield made
    made.wait(5_000)


def _spin(until, timeout: float = 5.0) -> None:
    """Turn the event loop until ``until()`` says so, or give up."""
    deadline = time.monotonic() + timeout
    while not until():
        QCoreApplication.processEvents()
        if time.monotonic() > deadline:
            raise AssertionError("timed out waiting")
        time.sleep(0.005)


# -- the runner --------------------------------------------------------


def test_work_runs_on_another_thread_and_its_result_comes_back_here(runner) -> None:
    where: list[int] = []
    got: list = []

    def work(progress: Progress) -> str:
        where.append(threading.get_ident())
        progress.report(1, 2, "half")
        return "done"

    def landed(result: str) -> None:
        got.append(result)
        where.append(threading.get_ident())

    task = runner.run("Work", work, done=landed)
    assert task in runner.tasks and runner.busy is task
    _spin(lambda: not task.running and got)
    assert got == ["done"]
    assert where[0] != threading.get_ident() and where[1] == threading.get_ident()
    assert task.result == "done" and task.error is None
    assert task not in runner.tasks and runner.busy is None


def test_progress_reports_are_relayed_to_the_gui_thread_coalesced(runner) -> None:
    moved: list[float] = []

    def work(progress: Progress) -> None:
        for step in range(50):
            progress.report(step, 50)
        progress.report(50, 50, "finished")

    task = runner.run("Work", work)
    task.changed.connect(lambda: moved.append(task.progress.fraction))
    _spin(lambda: not task.running)
    QCoreApplication.processEvents()
    assert moved and moved[-1] == 1.0 and task.progress.message == "finished"
    assert len(moved) <= 51


def test_an_error_is_handed_to_failed_and_nothing_to_done(runner) -> None:
    got: list = []
    errors: list = []

    def work(progress: Progress) -> None:
        raise ValueError("no good")

    task = runner.run("Work", work, done=got.append, failed=errors.append)
    _spin(lambda: not task.running and errors)
    assert got == [] and isinstance(errors[0], ValueError)
    assert isinstance(task.error, ValueError)


def test_cancelling_stops_the_work_and_tells_nobody(runner) -> None:
    got: list = []
    errors: list = []
    started = threading.Event()
    release = threading.Event()

    def work(progress: Progress) -> str:
        started.set()
        release.wait(5.0)
        progress.report(1, 1)  # raises: the cross was pressed meanwhile
        return "never"

    task = runner.run("Work", work, done=got.append, failed=errors.append)
    assert started.wait(5.0)
    task.cancel()
    release.set()
    _spin(lambda: not task.running)
    assert task.cancelled and got == [] and errors == []
    assert isinstance(task.error, CancelledError)


def test_a_result_arriving_after_the_cross_is_thrown_away(runner) -> None:
    got: list = []
    release = threading.Event()

    def work(progress: Progress) -> str:
        release.wait(5.0)
        return "late"

    task = runner.run("Work", work, done=got.append)
    task.cancel()
    release.set()
    _spin(lambda: not task.running)
    assert got == [] and task.result is None


def test_blocking_work_waits_its_turn_behind_blocking_work(runner) -> None:
    order: list[str] = []
    release = threading.Event()

    def first(progress: Progress) -> None:
        release.wait(5.0)
        order.append("first")

    def second(progress: Progress) -> None:
        order.append("second")

    one = runner.run("One", first)
    two = runner.run("Two", second)
    assert runner.busy is one and two.progress.message == "Waiting..."
    assert two in runner.tasks
    time.sleep(0.05)
    QCoreApplication.processEvents()
    assert order == []
    release.set()
    _spin(lambda: not one.running and not two.running)
    assert order == ["first", "second"]


def test_a_task_called_off_while_waiting_never_starts(runner) -> None:
    ran: list[str] = []
    release = threading.Event()

    def first(progress: Progress) -> None:
        release.wait(5.0)

    def second(progress: Progress) -> None:
        ran.append("second")

    one = runner.run("One", first)
    two = runner.run("Two", second)
    two.cancel()
    release.set()
    _spin(lambda: not one.running and not two.running)
    assert ran == [] and two.cancelled


def test_unblocking_work_runs_alongside(runner) -> None:
    release = threading.Event()
    seen: list[str] = []

    def slow(progress: Progress) -> None:
        release.wait(5.0)

    def quick(progress: Progress) -> None:
        seen.append("quick")

    one = runner.run("One", slow)
    two = runner.run("Two", quick, blocking=False)
    _spin(lambda: not two.running)
    assert seen == ["quick"] and one.running
    release.set()
    _spin(lambda: not one.running)


def test_a_begun_task_is_driven_by_its_caller(runner) -> None:
    ended: list[object] = []
    runner.ended.connect(ended.append)
    task = runner.begin("Render", blocking=False)
    assert task in runner.tasks
    task.progress.report(2, 4, "frame 2")
    QCoreApplication.processEvents()
    assert task.progress.fraction == 0.5
    pressed: list[bool] = []
    task.cancel_requested.connect(lambda: pressed.append(True))
    task.cancel()
    assert pressed == [True] and task.cancelled
    task.end()
    assert not task.running and ended == [task] and task not in runner.tasks


def test_wait_cancels_and_outlives_nothing(runner) -> None:
    release = threading.Event()

    def slow(progress: Progress) -> None:
        release.wait(0.2)
        progress.report(1, 1)

    task = runner.run("Slow", slow)
    runner.wait(5_000)
    _spin(lambda: not task.running)
    assert task.cancelled


# -- the picture -------------------------------------------------------


def test_a_card_paints_every_state_it_can_be_in(app, runner) -> None:
    task = runner.begin("Busy", blocking=False)
    card = ProgressCard(task, framed=True)
    card.resize(360, 66)
    card.show()
    card.grab()  # sweeping: nothing said yet
    task.progress.report(1, 3, "a third")
    card.grab()  # a fraction
    task.end()
    card.grab()  # done
    bare = ProgressCard(runner.begin("Bare", blocking=False, cancellable=False), framed=False)
    bare.resize(360, 56)
    bare.grab()
    bare.task.end()


def test_the_banner_shows_a_card_only_for_work_that_lasts(app, runner, monkeypatch) -> None:
    monkeypatch.setattr(tasks_module, "SHOW_AFTER_MS", 30)
    banner = TaskBanner(runner)
    quick = runner.begin("Quick", blocking=False)
    quick.end()
    _spin(lambda: True)
    time.sleep(0.06)
    QCoreApplication.processEvents()
    assert banner.cards == [] and not banner.isVisible()

    slow = runner.begin("Slow", blocking=False)
    _spin(lambda: banner.cards, timeout=2.0)
    assert banner.isVisible() and banner.cards[0].task is slow
    hosted = runner.begin("Hosted", blocking=False, hosted=True)
    time.sleep(0.06)
    QCoreApplication.processEvents()
    assert [card.task for card in banner.cards] == [slow]
    hosted.end()
    slow.end()
    _spin(lambda: not banner.cards, timeout=3.0)
    _spin(lambda: not banner.isVisible(), timeout=3.0)
