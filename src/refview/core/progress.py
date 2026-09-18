"""What a long piece of work says about itself while it runs, and how it is stopped.

Reading a scan, skinning a figure, writing a film: each is seconds to minutes
of work, and each used to say nothing about it -- a wait cursor at best, a
window that stopped answering at worst.  This is the one shape all of them
report through now, so that whatever shows the reports (see
:mod:`refview.ui.tasks`) has one thing to draw and the work has one thing to
call.

A :class:`Progress` is handed to the work.  The work calls :meth:`report` at
its natural boundaries -- a file read, a chunk of joints solved, a frame
written -- with how far it has got and, when it knows, how far there is to
go.  Every report is also the moment the work is stopped at, if it has been
asked to stop: :meth:`report` raises :class:`CancelledError`, which unwinds
the work cleanly through whatever ``finally`` blocks it has, and the caller
catches it and throws the half-made result away.  Work that cannot say how far along it
is reports without a total and is shown as busy rather than as a fraction.

Nothing here knows about threads beyond being safe to use across them: the
fields are written by the work and read by whoever is watching, and reading
a few plain attributes torn across a report is at worst one frame out of
date, which is what a progress bar is anyway.
"""

from __future__ import annotations

import threading
from collections.abc import Callable


class CancelledError(Exception):
    """Raised inside the work when it has been told to stop."""


class Progress:
    """How far a task has got, and whether it has been told to stop.

    ``on_change`` is called after every report, from whichever thread made
    it; the UI's job is to get from there back to its own thread.
    """

    __slots__ = ("title", "message", "done", "total", "_stop", "_on_change", "_lock")

    def __init__(
        self, title: str = "", on_change: Callable[[Progress], None] | None = None
    ) -> None:
        self.title = title
        self.message = ""
        #: Steps done so far, in whatever unit the work counts in.
        self.done = 0
        #: Steps there are in all, or ``0`` when the work cannot say.
        self.total = 0
        self._stop = threading.Event()
        self._on_change = on_change
        self._lock = threading.Lock()

    # -- for the work ---------------------------------------------------

    def report(
        self,
        done: int | float | None = None,
        total: int | float | None = None,
        message: str | None = None,
    ) -> None:
        """Say how far along the work is; raises :class:`CancelledError` to stop it.

        Any argument left out keeps its value, so a loop that set the total
        once can report only the count, and a message can be changed without
        moving the bar.
        """
        self.check()
        with self._lock:
            if done is not None:
                self.done = done
            if total is not None:
                self.total = total
            if message is not None:
                self.message = message
        if self._on_change is not None:
            self._on_change(self)

    def check(self) -> None:
        """Raise :class:`CancelledError` if the work has been told to stop."""
        if self._stop.is_set():
            raise CancelledError(self.title or "cancelled")

    def slice(self, start: float, end: float, total: int | float = 1) -> Progress:
        """A progress for one part of the work, mapped onto ``[start, end]`` of this one.

        A task in stages -- read the file, then weld it, then solve -- hands
        each stage a slice, so that the stage can count in its own unit and
        the bar still moves once from left to right.  Cancelling the whole
        cancels every slice.
        """
        return _Slice(self, float(start), float(end), total)

    # -- for whoever is watching ----------------------------------------

    def cancel(self) -> None:
        """Ask the work to stop at its next report."""
        self._stop.set()

    @property
    def cancelled(self) -> bool:
        return self._stop.is_set()

    @property
    def fraction(self) -> float | None:
        """How far along, 0 to 1, or ``None`` when the work has not said."""
        total = self.total
        if not total or total <= 0:
            return None
        return max(0.0, min(1.0, float(self.done) / float(total)))

    @property
    def determinate(self) -> bool:
        """Whether the work has said how much there is to do."""
        return self.fraction is not None


class _Slice(Progress):
    """A window onto part of a parent's range; see :meth:`Progress.slice`."""

    __slots__ = ("_parent", "_start", "_end")

    def __init__(self, parent: Progress, start: float, end: float, total: int | float) -> None:
        super().__init__(parent.title)
        self._parent = parent
        self._start = start
        self._end = end
        self.total = total
        # One stop flag for the whole task: a slice cancelled is the task
        # cancelled, and a task cancelled stops every slice.
        self._stop = parent._stop

    def report(
        self,
        done: int | float | None = None,
        total: int | float | None = None,
        message: str | None = None,
    ) -> None:
        super().report(done, total, message)
        fraction = self.fraction
        if fraction is None:
            # A stage that cannot count still moves the parent to its start,
            # so the bar shows the stages before it as done.
            self._parent.report(self._start, 1.0, message)
        else:
            at = self._start + (self._end - self._start) * fraction
            self._parent.report(at, 1.0, message)


def silent(title: str = "") -> Progress:
    """A progress nobody is watching, for work run without a window."""
    return Progress(title)
