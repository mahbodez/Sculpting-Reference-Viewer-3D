"""Recording a form's making in the background, so the app stays usable.

A film is a run of the geometry mode per stage, which is seconds on a coarse
setting and a couple of minutes on a fine one.  Doing that on the GUI thread
would be a freeze of exactly the kind the wait cursor exists to apologise for,
and apologising for two minutes is not good enough.

So it runs on a worker thread and hands each stage over as it is finished.
Two things fall out of that and both are the point:

The film is scrubbable while it is still being recorded.  The first stages are
the coarse ones, which are also the fast ones, so by the time the artist has
looked at the block the next few are already there.  The slider grows under
the handle rather than appearing all at once at the end.

And a recording that is no longer wanted is abandoned rather than waited for.
Every change to a setting the film depends on starts a new one, so dragging
the detail slider does not queue up a minute of work per value it passes over
-- the old recording is told to stop at its next stage boundary and drops what
it has.

The worker only ever reads the mesh and the settings it was handed, and the
meshes it makes are its own.  Nothing it touches is touched by the GUI thread
while it runs, which is what makes this safe without a lock around the model.
"""

from __future__ import annotations

import typing

from PySide6.QtCore import QObject, QThread, Signal

from ..core import plane_film
from ..core.mesh import Mesh
from ..core.plane_film import Film, Stage

if typing.TYPE_CHECKING:  # pragma: no cover - import cost, not behaviour
    from ..core.plane_axes import PlaneSet
    from ..core.plane_volume import Wires
    from ..core.settings import PlaneSettings


class _Recorder(QObject):
    """The work itself, living on the worker thread."""

    staged = Signal(object)
    finished = Signal(bool)

    def __init__(
        self,
        mesh: Mesh,
        planes: PlaneSet,
        settings: PlaneSettings,
        wires: Wires | None = None,
    ) -> None:
        super().__init__()
        self._mesh = mesh
        self._planes = planes
        self._settings = settings
        self._wires = wires
        self._stop = False

    def stop(self) -> None:
        """Ask the recording to end at the next stage boundary.

        Called from the GUI thread.  Reading and writing a bool is atomic
        under the GIL, and the worst a race can do is record one more stage
        than was wanted, which is thrown away.
        """
        self._stop = True

    def run(self) -> None:
        try:
            for stage in plane_film.record(
                self._mesh, self._planes, self._settings, lambda: self._stop, self._wires
            ):
                if self._stop:
                    break
                self.staged.emit(stage)
        except Exception:  # pragma: no cover - a mode that fell over mid-film
            self.finished.emit(False)
            raise
        self.finished.emit(not self._stop)


class FilmRecorder(QObject):
    """Keeps one recording running at a time, on a thread of its own.

    :attr:`grew` is emitted as each stage lands, with the film so far, so the
    panel can widen its slider and the viewport can show the stage if that is
    the one being looked at.  :attr:`settled` says the film is as long as it
    is going to get, which is what turns the progress note off.
    """

    #: The film gained a stage.  ``(film,)``.
    grew = Signal(object)
    #: The film is finished, or was abandoned.  ``(film, complete)``.
    settled = Signal(object, bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._thread: QThread | None = None
        self._worker: _Recorder | None = None
        self._film: Film | None = None
        #: Threads told to stop but not yet finished, and the workers that
        #: ride on them.  A QThread destroyed while it is still running takes
        #: the whole process down with it -- Qt aborts rather than trying to
        #: unwind it -- and dropping the last Python reference to one is
        #: exactly that.  So an abandoned recording is held here until it says
        #: it is done, and only then let go of.
        self._retiring: set[QThread] = set()
        #: Every worker ever started, kept alive for as long as this recorder
        #: is.  They are small, there are few of them, and a worker collected
        #: while its thread is still delivering its signals is a crash.
        self._workers: list[_Recorder] = []

    @property
    def film(self) -> Film | None:
        """The film being recorded, or the last one finished."""
        return self._film

    @property
    def recording(self) -> bool:
        """Whether a film is being made right now."""
        return self._thread is not None

    def matching(self, key: tuple) -> Film | None:
        """The film already held for ``key``, if there is one."""
        if self._film is not None and self._film.key == key:
            return self._film
        return None

    def abandon(self) -> bool:
        """Stop any recording in flight and forget what it was making.

        The thread is asked to stop and then left to finish on its own: it
        checks between stages, so it ends within one stage's work.  Waiting
        for it here would be the freeze this whole class exists to avoid.

        What is *not* dropped is the thread object.  It goes on the retiring
        pile until it reports itself finished, because letting Python collect
        a QThread that is still running aborts the process outright.

        Says whether there was anything to abandon, so a caller can tell the
        difference between cancelling a recording and doing nothing at all.
        """
        was_recording = self._thread is not None
        if self._worker is not None:
            self._worker.stop()
        if self._thread is not None:
            # Held whatever it is currently doing.  Asking whether it is
            # running is the wrong question: a thread that has been started
            # but has not yet got as far as its first instruction answers no,
            # and dropping that one is the same crash as dropping a busy one.
            # _retired takes it off the pile when it has really stopped.
            self._retiring.add(self._thread)
        self._thread = None
        self._worker = None
        self._film = None
        return was_recording

    def start(
        self,
        mesh: Mesh,
        planes: PlaneSet,
        settings: PlaneSettings,
        key: tuple,
        wires: Wires | None = None,
    ) -> Film:
        """Begin recording, abandoning whatever was being recorded before."""
        self.abandon()
        film = Film(sculpt=settings.sculpt, key=key)
        self._film = film

        thread = QThread(self)
        worker = _Recorder(mesh, planes, settings, wires)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.staged.connect(lambda stage: self._took(film, stage))
        worker.finished.connect(lambda done: self._done(film, done))
        # The thread stops itself whichever way the recording ends, so an
        # abandoned one is not left sitting on a core.  Neither it nor the
        # worker is deleteLater'd: the thread is parented to this recorder and
        # the worker is kept alive by the pile below, so Qt tears both down
        # when the recorder goes rather than out from under a Python handle
        # that is still pointing at them.
        worker.finished.connect(thread.quit)
        thread.finished.connect(lambda t=thread: self._retired(t))
        self._thread, self._worker = thread, worker
        self._workers.append(worker)
        thread.start()
        return film

    def wait(self, milliseconds: int = 30_000) -> None:
        """Let every thread finish, for shutdown.

        The only place waiting is the right thing to do: the window is going
        away, and a thread still running when the interpreter tears down its
        module globals is a crash on the way out.

        The wait is generous because the worker stops between stages and a
        stage can be a second or two.  What it must never do is give up and
        terminate one: a thread killed in the middle of a numpy call leaves
        the allocator in pieces and takes the process down exactly the way
        this method exists to prevent.  So it asks, and then it waits.
        """
        self.abandon()
        for thread in list(self._retiring):
            try:
                # A thread is stopped by its event loop being told to quit,
                # and one that has not reached its loop yet has nothing to
                # tell -- the wait covers both, because the worker checks
                # its stop flag between stages either way.
                thread.quit()
                thread.wait(int(milliseconds))
            except RuntimeError:  # pragma: no cover - Qt deleted it already
                # It finished and was cleaned up between going on the pile
                # and being waited for, which is the good case.
                pass
        self._retiring.clear()

    # -- back on the GUI thread -------------------------------------------

    def _retired(self, thread: QThread) -> None:
        """A thread has really stopped, so it is safe to let go of it.

        Every handle to it goes at once -- the one on the retiring pile and,
        if this was the live recording, ``_thread`` as well.  A recording that
        ends by itself is never abandoned, so both can be pointing at the same
        object.  The thread itself is left for Qt to collect with its parent:
        deleting it here would be deleting it from inside its own finished
        signal, which is how a tidy-up becomes a segfault.
        """
        self._retiring.discard(thread)
        if self._thread is thread:
            self._thread = None
            self._worker = None

    def _took(self, film: Film, stage: Stage) -> None:
        if film is not self._film:
            return  # a stage from a recording that has since been abandoned
        film.stages.append(stage)
        self.grew.emit(film)

    def _done(self, film: Film, complete: bool) -> None:
        if film is not self._film:
            return
        film.complete = complete
        self.settled.emit(film, complete)
