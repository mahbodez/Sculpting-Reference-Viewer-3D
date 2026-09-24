"""Renders on the interface's side: starting one, watching it, and denoising what it made.

The path tracer itself knows nothing of Qt (:mod:`refview.trace`).  This is
the part that does: it prepares a render on a task thread, so reading the
scene and building its tree show on a card and never stall the window;
starts the render on its thread pool; looks at it ten times a second to say
how it is doing; and, when it is done, hands the film to the denoiser.

Only one render runs at a time.  Asking for another stops the one running,
as pressing F12 twice in Blender does.  The computer is kept awake while a
render runs, since a render left overnight is the usual kind.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from PySide6.QtCore import QObject, QTimer, Signal

from ..core.path_trace import PathTraceSettings
from ..wakelock import ThreadWakeLock
from .state import ViewerState

_SERVICE = None


def denoise_service():
    """The one denoiser thread the whole window shares; see :mod:`refview.trace.denoise`."""
    global _SERVICE
    if _SERVICE is None:
        from ..trace.denoise import DenoiseService

        _SERVICE = DenoiseService()
        _SERVICE.probe()
    return _SERVICE


def shutdown_denoise_service() -> None:
    global _SERVICE
    if _SERVICE is not None:
        _SERVICE.shutdown()
        _SERVICE = None


@dataclass
class RenderResult:
    """A render, finished or under way, and everything needed to show and save it."""

    film: object                      # refview.trace.film.Film
    settings: PathTraceSettings       # as it was rendered
    skin: bool
    skin_exposure: float
    background_top: tuple
    background_bottom: tuple
    view_rotation: np.ndarray
    stats: object = None              # refview.trace.job.RenderStats
    denoised: np.ndarray | None = None
    denoiser: str = ""
    notes: list[str] = field(default_factory=list)
    job: object = None

    @property
    def size(self) -> tuple[int, int]:
        return self.film.width, self.film.height


class RenderController(QObject):
    """Starts, watches and finishes renders for the Render panel and window."""

    #: A render began: the :class:`RenderResult` it fills.
    started = Signal(object)
    #: Ten times a second while it runs: the result, and the regions that changed.
    progressed = Signal(object, list)
    #: It ended, finished or stopped: the result.
    finished = Signal(object)
    #: The denoised picture arrived.
    denoised = Signal(object)
    #: Something went wrong, in words.
    failed = Signal(str)
    #: What the path tracer can do here: ready, compiling, or why it cannot.
    status_changed = Signal(str)

    def __init__(self, state: ViewerState, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._state = state
        self._cache = None
        self._job = None
        self._result: RenderResult | None = None
        self._preparing = None
        self._timer = QTimer(self)
        self._timer.setInterval(100)
        self._timer.timeout.connect(self._poll)
        self._wake = ThreadWakeLock()
        self._status = ""
        self._denoise_future = None
        self._denoise_timer = QTimer(self)
        self._denoise_timer.setInterval(50)
        self._denoise_timer.timeout.connect(self._poll_denoise)

    # -- what can run ------------------------------------------------------------

    @property
    def status(self) -> str:
        return self._status

    def _set_status(self, text: str) -> None:
        self._status = text
        self.status_changed.emit(text)

    def available(self) -> tuple[bool, str | None]:
        from .. import trace

        if trace.available():
            return True, None
        return False, trace.unavailable_reason()

    @property
    def result(self) -> RenderResult | None:
        return self._result

    @property
    def running(self) -> bool:
        return self._job is not None or self._preparing is not None

    # -- rendering ---------------------------------------------------------------

    def render(self, inputs) -> None:
        """Render ``inputs`` (a :class:`~refview.trace.scene.TraceInputs`), stopping any render."""
        ok, reason = self.available()
        if not ok:
            self.failed.emit(f"The path tracer cannot run: {reason}")
            return
        self.cancel()
        from ..trace.warmup import is_warm

        cold = not is_warm()

        def work(progress):
            from ..trace.scene import SceneCache, compile_scene
            from ..trace.warmup import warm_up

            if cold:
                warm_up(progress)
            progress.report(message="Reading the scene...")
            if self._cache is None:
                self._cache = SceneCache()
            return compile_scene(inputs, self._cache, progress)

        self._set_status("Compiling render kernels (first run only)..." if cold
                         else "Preparing the scene...")
        task = self._state.tasks.run(
            "Preparing render", work, lambda scene: self._start(inputs, scene),
            self._prepare_failed, blocking=False, cancellable=True,
        )
        self._preparing = task
        task.finished.connect(lambda: self._prepared(task))

    def _prepared(self, task) -> None:
        if self._preparing is task:
            self._preparing = None
            if task.cancelled:
                self._set_status("Stopped")

    def _prepare_failed(self, error: BaseException) -> None:
        self._preparing = None
        self._set_status("Failed")
        self.failed.emit(f"The render could not start: {error}")

    def _start(self, inputs, scene) -> None:
        from ..trace.job import RenderJob

        trace = inputs.path_trace
        job = RenderJob(scene, trace, passes=True)
        view = np.asarray(inputs.camera.view_matrix(), dtype=np.float64)[:3, :3]
        render = inputs.render
        result = RenderResult(
            film=job.film, settings=trace, skin=scene.skin, skin_exposure=scene.exposure,
            background_top=tuple(render.background_top),
            background_bottom=tuple(render.background_bottom),
            view_rotation=view, job=job,
        )
        self._job = job
        self._result = result
        self._wake.set_held(True)
        job.start()
        self._timer.start()
        self._set_status(f"Rendering on {job.threads} threads")
        self.started.emit(result)

    def _poll(self) -> None:
        job = self._job
        if job is None:
            self._timer.stop()
            return
        result = self._result
        result.stats = job.stats()
        dirty = job.take_dirty()
        self.progressed.emit(result, dirty)
        if result.stats.state.finished:
            self._finish()

    def _finish(self) -> None:
        from ..trace.job import JobState

        job = self._job
        self._job = None
        self._timer.stop()
        self._wake.set_held(False)
        result = self._result
        result.stats = job.stats()
        state = result.stats.state
        if state is JobState.FAILED:
            self._set_status("Failed")
            self.failed.emit(f"The render failed: {result.stats.error}")
        elif state is JobState.CANCELLED:
            self._set_status("Stopped")
        else:
            self._set_status("Done")
        self.finished.emit(result)
        if state is not JobState.FAILED and result.settings.denoise.final:
            self.denoise(result)

    def denoise(self, result: RenderResult | None = None) -> None:
        """Denoise a render's film now, with the settings as they are."""
        result = result or self._result
        if result is None or result.film.count.max() == 0:
            return
        from ..trace.denoise import request_from_film

        request = request_from_film(result.film, result.view_rotation)
        settings = self._state.path_trace.denoise
        self._set_status("Denoising...")
        self._denoise_future = (result, denoise_service().submit(request, settings))
        self._denoise_timer.start()

    def _poll_denoise(self) -> None:
        if self._denoise_future is None:
            self._denoise_timer.stop()
            return
        result, future = self._denoise_future
        if not future.done():
            return
        self._denoise_timer.stop()
        self._denoise_future = None
        try:
            image, info, note = future.result()
        except Exception as error:  # noqa: BLE001
            self.failed.emit(f"Denoising failed: {error}")
            self._set_status("Done")
            return
        coverage = result.film.beauty()[..., 3:4]
        result.denoised = np.concatenate([image, coverage], axis=-1)
        result.denoiser = info.summary
        if note:
            result.notes.append(note)
        self._set_status(f"Done - denoised with {info.summary}")
        self.denoised.emit(result)

    def cancel(self) -> None:
        if self._preparing is not None:
            self._preparing.cancel()
            self._preparing = None
        if self._job is not None:
            self._job.cancel()

    def shutdown(self) -> None:
        self.cancel()
        if self._job is not None:
            self._job.wait(2.0)
        self._timer.stop()
        self._wake.release()
