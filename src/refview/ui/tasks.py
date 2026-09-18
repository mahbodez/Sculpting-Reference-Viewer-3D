"""Work that takes a while, run off the window and shown while it runs.

Three things live here, and every long job in the viewer goes through them:

:class:`TaskRunner` takes a function, runs it on a thread of its own with a
:class:`~refview.core.progress.Progress` to report through, and hands the
result back on the GUI thread.  Work that has to stay on the GUI thread --
rendering, which owns the graphics context -- is *begun* instead, and drives
its own task's progress a step at a time.  Either way the runner knows what
is in flight, which is what the banner draws and what the window waits for
on the way out.

:class:`ProgressCard` is the picture of one task: its name, what it is doing
right now, a bar that fills when the work can count and sweeps when it
cannot, and a cross to call it off.  Painted by hand in the panels' own
colours, so a wait looks like part of the application rather than a box the
system put up.

:class:`TaskBanner` holds a card over the bottom of the viewport for each
task the window is running, fading them in and out.  A job that finishes in
a blink is never shown at all: the card waits a moment before appearing, so
opening a small file does not flash a bar at the artist.

The threading follows :mod:`refview.ui.film_recorder`, and for the same
reasons: a ``QThread`` is never let go of while it runs, and the way out of
the application waits for the work rather than killing it.
"""

from __future__ import annotations

import typing
from collections.abc import Callable

from PySide6.QtCore import (
    QEasingCurve,
    QObject,
    QPropertyAnimation,
    QRect,
    QRectF,
    Qt,
    QThread,
    QTimer,
    Signal,
)
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import (
    QGraphicsOpacityEffect,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ..core.progress import CancelledError, Progress
from .elements import palette as ink
from .icons import glyph

T = typing.TypeVar("T")

#: How long a task has to have been running before its card is shown.
SHOW_AFTER_MS = 350

#: Height of the bar under the words, and how far its corners are rounded.
_BAR_HEIGHT = 5

#: The sweeping segment of a bar that cannot count, as a share of the track,
#: and how long one sweep takes.
_SWEEP_SHARE = 0.28
_SWEEP_MS = 1400

#: How often a card repaints while its bar is sweeping.
_TICK_MS = 33


class Task(QObject):
    """One piece of work in flight, as the window sees it.

    Made by the runner, never directly.  :attr:`progress` is what the work
    writes to; :attr:`changed` is emitted on the GUI thread whenever it does,
    coalesced so that a loop reporting a thousand times a second asks for a
    repaint once per frame.
    """

    #: The progress moved, or the message changed.
    changed = Signal()
    #: The task is over: done, failed or called off.
    finished = Signal()
    #: For a task the caller drives itself: the cross was pressed.
    cancel_requested = Signal()
    #: Emitted from the working thread; wired back to :meth:`_moved` here.
    _relayed = Signal()

    def __init__(
        self,
        title: str,
        blocking: bool,
        cancellable: bool,
        hosted: bool,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self.title = title
        #: Whether the window should refuse another such task meanwhile.
        self.blocking = blocking
        #: Whether the card gets a cross.
        self.cancellable = cancellable
        #: Whether something other than the banner is showing this task --
        #: a dialog with a card of its own -- so the banner leaves it be.
        self.hosted = hosted
        self.progress = Progress(title, self._report)
        self.result: typing.Any = None
        self.error: BaseException | None = None
        self._running = True
        self._pending = False
        self._relayed.connect(self._moved, Qt.ConnectionType.QueuedConnection)

    @property
    def running(self) -> bool:
        return self._running

    @property
    def cancelled(self) -> bool:
        return self.progress.cancelled

    def cancel(self) -> None:
        """Ask the work to stop.  It stops at its next report, not before."""
        if not self._running or not self.cancellable:
            return
        self.progress.cancel()
        self.cancel_requested.emit()

    def end(self, result: typing.Any = None, error: BaseException | None = None) -> None:
        """Mark the task over.  The runner does this; a begun task's driver does."""
        if not self._running:
            return
        self._running = False
        self.result = result
        self.error = error
        self.finished.emit()

    # -- from the working thread ------------------------------------------

    def _report(self, _progress: Progress) -> None:
        # One queued signal at a time: a report that lands while the last
        # is still on its way to the GUI thread is folded into it.
        if not self._pending:
            self._pending = True
            self._relayed.emit()

    def _moved(self) -> None:
        self._pending = False
        self.changed.emit()


class _Worker(QObject):
    """The function itself, living on the worker thread."""

    done = Signal(object)
    failed = Signal(object)

    def __init__(self, work: Callable[[Progress], typing.Any], progress: Progress) -> None:
        super().__init__()
        self._work = work
        self._progress = progress

    def run(self) -> None:
        try:
            result = self._work(self._progress)
        except Exception as error:
            self.failed.emit(error)
            return
        self.done.emit(result)


class TaskRunner(QObject):
    """Runs work off the GUI thread and keeps the window told.

    :attr:`started` and :attr:`ended` carry the task, so the banner can put
    a card up and take it down.  The runner keeps every thread it starts
    until the thread has really stopped, and :meth:`wait` is for shutdown
    only; everywhere else a task that is no longer wanted is cancelled and
    left to finish on its own.

    A *blocking* task is one the scene changes at the end of -- a model
    read, a skin made -- and two of those are not run together, since the
    second would land on a scene the first is about to replace.  Asked for
    while one runs, another waits its turn and starts when the first ends,
    in the order asked; its card says it is waiting.
    """

    started = Signal(object)
    ended = Signal(object)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._tasks: list[Task] = []
        self._threads: dict[int, QThread] = {}
        self._workers: list[_Worker] = []
        #: Blocking work asked for while other blocking work ran, in order.
        self._waiting: list[tuple[Task, Callable, Callable | None, Callable | None]] = []

    @property
    def tasks(self) -> list[Task]:
        """Every task in flight, oldest first."""
        return list(self._tasks)

    @property
    def busy(self) -> Task | None:
        """The blocking task running now, if there is one."""
        waiting = {id(held[0]) for held in self._waiting}
        for task in self._tasks:
            if task.blocking and id(task) not in waiting:
                return task
        return None

    def run(
        self,
        title: str,
        work: Callable[[Progress], T],
        done: Callable[[T], None] | None = None,
        failed: Callable[[BaseException], None] | None = None,
        *,
        blocking: bool = True,
        cancellable: bool = True,
        hosted: bool = False,
    ) -> Task:
        """Run ``work(progress)`` on a thread; ``done(result)`` back here.

        ``failed`` is told of any error the work raised, except that being
        cancelled is not an error and is told to nobody: the artist pressed
        the cross and knows.  Both are called on the GUI thread, after the
        task has ended and the banner has been told.
        """
        task = Task(title, blocking, cancellable, hosted, self)
        if blocking and self.busy is not None:
            task.progress.message = "Waiting..."
            self._waiting.append((task, work, done, failed))
            self._tasks.append(task)
            self.started.emit(task)
            return task
        self._tasks.append(task)
        self.started.emit(task)
        self._launch(task, work, done, failed)
        return task

    def _launch(self, task: Task, work, done, failed) -> None:
        if task.cancelled:
            # Called off while it waited its turn: over before it began.
            task.end(None, CancelledError(task.title))
            self._ended(task)
            return
        worker = _Worker(work, task.progress)
        thread = QThread(self)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.done.connect(lambda result: self._finish(task, result, None, done, failed))
        worker.failed.connect(lambda error: self._finish(task, None, error, done, failed))
        # The thread stops itself whichever way the work ends, and is held
        # on the pile until it has: a QThread collected while running takes
        # the process down with it.
        worker.done.connect(thread.quit)
        worker.failed.connect(thread.quit)
        thread.finished.connect(lambda: self._threads.pop(id(thread), None))
        self._threads[id(thread)] = thread
        self._workers.append(worker)
        thread.start()

    def begin(
        self,
        title: str,
        *,
        blocking: bool = True,
        cancellable: bool = True,
        hosted: bool = False,
    ) -> Task:
        """A task driven by the caller, on the GUI thread, a step at a time.

        For work that cannot leave the GUI thread.  The caller reports
        through ``task.progress`` as it goes, listens to
        :attr:`Task.cancel_requested`, and calls :meth:`Task.end` when it is
        over, whichever way it ended.
        """
        task = Task(title, blocking, cancellable, hosted, self)
        task.finished.connect(lambda: self._ended(task))
        self._tasks.append(task)
        self.started.emit(task)
        return task

    def wait(self, milliseconds: int = 30_000) -> None:
        """Cancel everything and let the threads finish, for shutdown."""
        for task in list(self._tasks):
            task.progress.cancel()
        for thread in list(self._threads.values()):
            try:
                thread.quit()
                thread.wait(int(milliseconds))
            except RuntimeError:  # pragma: no cover - Qt deleted it already
                pass
        self._threads.clear()

    # -- back on the GUI thread -------------------------------------------

    def _finish(self, task: Task, result, error, done, failed) -> None:
        if isinstance(error, CancelledError) or (error is None and task.cancelled):
            # Cancelled at a report, or finished in the moment between the
            # cross and the next one: either way the result is not wanted.
            task.end(None, error)
            self._ended(task)
            return
        task.end(result, error)
        self._ended(task)
        if error is not None:
            if failed is not None:
                failed(error)
        elif done is not None:
            done(result)

    def _ended(self, task: Task) -> None:
        if task in self._tasks:
            self._tasks.remove(task)
            self.ended.emit(task)
        if task.blocking and self._waiting and self.busy is None:
            waiting, work, done, failed = self._waiting.pop(0)
            waiting.progress.message = ""
            self._launch(waiting, work, done, failed)


# ----------------------------------------------------------------------
# The picture
# ----------------------------------------------------------------------


class ProgressCard(QWidget):
    """One task: its name, its message, its bar, and a cross to stop it.

    Painted by hand: the ground and the bar with the palette's colours, so
    a wait looks like the rest of the interface.  Given ``framed`` the card
    is a rounded panel of its own, for floating over the viewport; without,
    it is bare, for sitting inside a dialog that already has a ground.
    """

    def __init__(self, task: Task, framed: bool = True, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._task = task
        self._framed = framed
        self._sweep = 0.0
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumWidth(320)
        self.setFixedHeight(66 if framed else 56)
        self._cancel = QPushButton(self)
        self._cancel.setIcon(glyph("cross", 12))
        self._cancel.setFlat(True)
        self._cancel.setFixedSize(24, 24)
        self._cancel.setToolTip("Stop")
        self._cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self._cancel.clicked.connect(task.cancel)
        self._cancel.setVisible(task.cancellable)
        self._ticker = QTimer(self)
        self._ticker.setInterval(_TICK_MS)
        self._ticker.timeout.connect(self._tick)
        task.changed.connect(self.update)
        task.finished.connect(self._finished)
        self._sync_ticker()

    @property
    def task(self) -> Task:
        return self._task

    def _finished(self) -> None:
        self._ticker.stop()
        self._cancel.setEnabled(False)
        self.update()

    def _sync_ticker(self) -> None:
        if self._task.running and not self._task.progress.determinate:
            if not self._ticker.isActive():
                self._ticker.start()
        else:
            self._ticker.stop()

    def _tick(self) -> None:
        self._sweep = (self._sweep + _TICK_MS / _SWEEP_MS) % 1.0
        self.update()

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt naming
        super().resizeEvent(event)
        pad = 12 if self._framed else 4
        self._cancel.move(self.width() - pad - self._cancel.width(), pad - 2)

    def paintEvent(self, _event) -> None:  # noqa: N802 - Qt naming
        self._sync_ticker()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        try:
            self._paint(painter)
        finally:
            painter.end()

    def _paint(self, painter: QPainter) -> None:
        rect = self.rect()
        pad = 12 if self._framed else 4
        if self._framed:
            ground = QColor(ink.PANEL)
            ground.setAlpha(238)
            painter.setPen(QPen(ink.EDGE_LIT, 1))
            painter.setBrush(ground)
            painter.drawRoundedRect(
                QRectF(rect).adjusted(0.5, 0.5, -0.5, -0.5), ink.RADIUS + 2, ink.RADIUS + 2
            )
        progress = self._task.progress
        fraction = progress.fraction
        right = rect.width() - pad - (self._cancel.width() + 6 if self._task.cancellable else 0)

        # The title, and the share done beside it.
        title_font = QFont(self.font())
        title_font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(title_font)
        metrics = QFontMetrics(title_font)
        line = metrics.height()
        top = pad
        share = ""
        if not self._task.running:
            share = _outcome(self._task)
        elif fraction is not None:
            share = f"{int(round(fraction * 100)):d}%"
        share_width = metrics.horizontalAdvance(share) + 8 if share else 0
        painter.setPen(ink.INK)
        title = metrics.elidedText(
            self._task.title, Qt.TextElideMode.ElideRight, right - pad - share_width
        )
        painter.drawText(QRect(pad, top, right - pad - share_width, line), 0, title)
        if share:
            painter.setPen(ink.INK_SOFT)
            painter.drawText(
                QRect(right - share_width, top, share_width, line),
                Qt.AlignmentFlag.AlignRight,
                share,
            )

        # What it is doing right now.
        painter.setFont(self.font())
        metrics = QFontMetrics(self.font())
        painter.setPen(ink.INK_SOFT)
        message = metrics.elidedText(progress.message, Qt.TextElideMode.ElideRight, right - pad)
        painter.drawText(QRect(pad, top + line + 1, right - pad, metrics.height()), 0, message)

        # The bar.
        track = QRectF(pad, rect.height() - pad - _BAR_HEIGHT, rect.width() - 2 * pad, _BAR_HEIGHT)
        radius = _BAR_HEIGHT / 2.0
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(ink.WELL)
        painter.drawRoundedRect(track, radius, radius)
        if not self._task.running:
            fill = QColor(ink.INK_DIM) if self._task.cancelled or self._task.error else ink.ACCENT
            painter.setBrush(fill)
            painter.drawRoundedRect(track, radius, radius)
            return
        painter.setBrush(ink.ACCENT_FILL)
        if fraction is not None:
            width = max(track.width() * fraction, _BAR_HEIGHT if fraction > 0.0 else 0.0)
            if width > 0.0:
                filled = QRectF(track.left(), track.top(), width, track.height())
                painter.drawRoundedRect(filled, radius, radius)
            return
        # Cannot count: a segment sweeps the track, easing at each end so
        # that it reads as motion rather than as a bar that is stuck.
        clip = QPainterPath()
        clip.addRoundedRect(track, radius, radius)
        painter.setClipPath(clip)
        span = track.width() * _SWEEP_SHARE
        eased = QEasingCurve(QEasingCurve.Type.InOutSine).valueForProgress(self._sweep)
        left = track.left() - span + (track.width() + span) * eased
        painter.drawRoundedRect(QRectF(left, track.top(), span, track.height()), radius, radius)


def _outcome(task: Task) -> str:
    """The word a finished card ends on."""
    if task.cancelled:
        return "Stopped"
    return "Failed" if task.error else "Done"


class TaskBanner(QWidget):
    """The cards for the window's tasks, floated over the bottom of the viewport.

    Told about tasks by the runner; keeps a card per task that is not
    hosted elsewhere, and takes each down a moment after its task ends so
    that "Done" is seen.  Sized to its cards and placed by whoever owns it,
    which is the main window, on every resize.
    """

    #: The banner has cards to show, or none: the owner places or hides it.
    changed = Signal()

    def __init__(self, runner: TaskRunner, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._runner = runner
        self._cards: dict[int, ProgressCard] = {}
        self._pending: dict[int, QTimer] = {}
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(6)
        self._effect = QGraphicsOpacityEffect(self)
        self._effect.setOpacity(0.0)
        self.setGraphicsEffect(self._effect)
        self._fade = QPropertyAnimation(self._effect, b"opacity", self)
        self._fade.setDuration(180)
        self._fade.finished.connect(self._faded)
        runner.started.connect(self._started)
        runner.ended.connect(self._ended)
        self.hide()

    @property
    def cards(self) -> list[ProgressCard]:
        return list(self._cards.values())

    def _started(self, task: Task) -> None:
        if task.hosted:
            return
        # A moment's grace, so a task that is over in a blink never shows.
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.setInterval(SHOW_AFTER_MS)
        timer.timeout.connect(lambda: self._show_card(task))
        self._pending[id(task)] = timer
        timer.start()

    def _show_card(self, task: Task) -> None:
        self._pending.pop(id(task), None)
        if not task.running or id(task) in self._cards:
            return
        card = ProgressCard(task, True, self)
        self._cards[id(task)] = card
        self._layout.addWidget(card)
        self.adjustSize()
        if not self.isVisible():
            self.show()
        self.raise_()
        # Placed by the owner once it is showing: a hidden banner has no
        # place to be.
        self.changed.emit()
        if self._effect.opacity() < 1.0:
            self._fade_to(1.0)

    def _ended(self, task: Task) -> None:
        timer = self._pending.pop(id(task), None)
        if timer is not None:
            timer.stop()
        card = self._cards.get(id(task))
        if card is None:
            return
        # Leave the finished card up long enough to be read, then take it
        # down; the last one down takes the banner with it.
        QTimer.singleShot(650, lambda: self._drop(task))

    def _drop(self, task: Task) -> None:
        card = self._cards.pop(id(task), None)
        if card is None:
            return
        if not self._cards:
            # The last card fades out with the banner and goes when it has.
            self._fade_to(0.0)
            return
        self._layout.removeWidget(card)
        card.deleteLater()
        self.adjustSize()
        self.changed.emit()

    def _fade_to(self, opacity: float) -> None:
        self._fade.stop()
        self._fade.setStartValue(self._effect.opacity())
        self._fade.setEndValue(opacity)
        self._fade.start()

    def _faded(self) -> None:
        if self._effect.opacity() > 0.0 or self._cards:
            return
        while self._layout.count():
            item = self._layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.hide()
        self.changed.emit()
