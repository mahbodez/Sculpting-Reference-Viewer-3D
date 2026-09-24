"""The rendered viewport: the path tracer drawing the view as you work in it.

While it is on, the view is path-traced progressively at a fraction of its
resolution and the picture laid over the viewport as it clears.  Anything
that changes the picture -- the camera, a slider, the model, a pose, the
HDRI -- starts it over; what cannot, such as the grid or the safe frame, is
left out of what it watches (see :func:`~refview.trace.scene.trace_settings_key`).
While the view is being turned it renders coarser still, so the picture
follows the hand, and it sharpens once the hand stops.

The scene is compiled on a thread of its own, the render runs on the path
tracer's pool, and the interface only ever develops what is already in the
film, so the window stays as responsive with it on as off.  With a
denoiser at hand the picture is denoised as it refines, a few times a
second -- which is what makes a handful of samples look like a finished
render.  With DLSS 5 Neural Rendering on for the viewport, each new
denoised picture (or, undenoised, the finished one) is enhanced too, one at
a time, and shown once it is back.
"""

from __future__ import annotations

import threading
import time
from dataclasses import replace

import numpy as np
from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtGui import QImage

from ..trace.neural import MIN_SIDE, engine_dir

#: How long the view must be still before the preview renders at its full resolution.
SETTLE_SECONDS = 0.15


class ViewportRenderPreview(QObject):
    """Keeps a progressive render of the view going while the rendered viewport is on."""

    #: A new picture is ready to be drawn.
    updated = Signal()

    def __init__(self, viewport) -> None:
        super().__init__(viewport)
        self._viewport = viewport
        self._state = viewport.state
        self.enabled = False
        #: Held still while a final render has the processor: the last
        #: picture stays up and nothing new is started until it is let go.
        self.suspended = False
        self._key = None
        self._serial = 0
        self._lock = threading.Lock()
        self._wake = threading.Condition(self._lock)
        self._request = None
        self._stop = False
        self._worker: threading.Thread | None = None
        self._job = None
        self._job_serial = -1
        self._job_started = 0.0
        self._error: str | None = None
        self._compiling = False
        self._image: QImage | None = None
        self._bytes: np.ndarray | None = None
        self._display: np.ndarray | None = None
        self._denoise = None
        self._denoised: QImage | None = None
        self._denoised_bytes: np.ndarray | None = None
        self._denoised_display: np.ndarray | None = None
        self._denoised_samples = 0.0
        self._shown_job = None
        self._last_denoise = 0.0
        #: The newest picture worth enhancing: (job, serial, display values).
        self._best = None
        self._best_serial = 0
        self._enhance = None
        self._enhanced: QImage | None = None
        self._enhanced_bytes: np.ndarray | None = None
        self._enhanced_key = None
        #: The settings Neural Rendering last failed with, and why.
        self._neural_error: tuple[str, str] | None = None
        self._last_interaction = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(40)
        self._timer.timeout.connect(self._tick)

    # -- switching -------------------------------------------------------------

    def set_enabled(self, on: bool) -> None:
        if on == self.enabled:
            return
        self.enabled = on
        if on:
            ok, reason = self._available()
            if not ok:
                self.enabled = False
                self._error = reason
                self._state.status_message.emit(f"The rendered viewport cannot run: {reason}")
                return
            self._error = None
            self._key = None
            self._timer.start()
        else:
            self._key = None
            self._cancel_job()
            self._image = None
            self._denoised = None
            self._forget_enhanced()
            self._timer.stop()
        self.updated.emit()

    @staticmethod
    def _available() -> tuple[bool, str | None]:
        from .. import trace

        return (True, None) if trace.available() else (False, trace.unavailable_reason())

    def shutdown(self) -> None:
        self.enabled = False
        with self._lock:
            self._stop = True
            self._wake.notify_all()
        self._cancel_job()
        if self._worker is not None:
            self._worker.join(2.0)
        self._timer.stop()

    def suspend(self, on: bool) -> None:
        """Hold the preview still while a render runs, and pick it up again after."""
        self.suspended = bool(on)
        if on:
            self._cancel_job()
        else:
            self._key = None
            self.updated.emit()

    def _cancel_job(self) -> None:
        with self._lock:
            job = self._job
            self._job = None
            self._request = None
        if job is not None:
            job.cancel()

    # -- the viewport asks -------------------------------------------------------

    def frame(self, width: int, height: int, interacting: bool) -> QImage | None:
        """The picture to draw over a ``width`` by ``height`` view, or ``None`` for the GL one.

        Starts the render over when what it shows has changed.
        """
        if not self.enabled:
            return None
        now = time.perf_counter()
        if interacting:
            self._last_interaction = now
        moving = interacting or now - self._last_interaction < SETTLE_SECONDS
        preview = self._state.path_trace.preview
        share = preview.interactive_resolution if moving else preview.resolution
        w = max(int(width * share), 8)
        h = max(int(height * share), 8)
        if self.suspended:
            return self._picture()
        key = self._picture_key(w, h, width, height)
        if key != self._key:
            self._key = key
            self._restart(w, h, moving)
        if moving and not interacting:
            # Come back once the view has settled, to render it sharp.
            QTimer.singleShot(int(SETTLE_SECONDS * 1000) + 10, self._viewport.update)
        return self._picture()

    def _picture(self) -> QImage | None:
        """The best picture there is: enhanced, denoised, or as it is."""
        if self._enhanced is not None and self._state.path_trace.neural.preview:
            return self._enhanced
        return self._denoised if self._denoised is not None else self._image

    def caption(self) -> str:
        if self.suspended:
            return "Rendered: paused while the render runs"
        if self._error:
            return f"Rendered: {self._error}"
        if self._compiling:
            from ..trace.warmup import is_warm

            return ("Rendered: compiling render kernels (first run only)..." if not is_warm()
                    else "Rendered: preparing...")
        job = self._job
        if job is None:
            return "Rendered"
        stats = job.stats()
        text = (f"Rendered  ·  {stats.samples_done:.0f}/{stats.samples_target} spp  ·  "
                f"{stats.elapsed:.1f} s")
        if self._denoised is not None:
            text += "  ·  denoised"
        if self._state.path_trace.neural.preview:
            if self._enhanced is not None:
                text += "  ·  DLSS 5 Neural Rendering"
            elif self._neural_error is not None:
                text += f"  ·  Neural Rendering: {self._neural_error[1]}"
        return text

    def _picture_key(self, w: int, h: int, width: int, height: int) -> tuple:
        from ..trace.scene import trace_settings_key

        state = self._state
        camera = state.camera
        renderer = self._viewport.renderer
        body = state.body_source() if state.render.shading_mode.value == "human_skin" else None
        return (
            camera.view_matrix().tobytes(), camera.fov_deg, camera.projection, camera.near,
            camera.far, w, h, width, height,
            trace_settings_key(state.render, state.path_trace),
            renderer.content_revision, id(state.environment),
            None if body is None else body.key,
        )

    def _restart(self, w: int, h: int, moving: bool) -> None:
        inputs = self._viewport.trace_inputs(w, h, framed=False)
        with self._lock:
            self._serial += 1
            self._request = (self._serial, inputs, moving)
            self._wake.notify_all()
        if self._worker is None or not self._worker.is_alive():
            self._stop = False
            self._worker = threading.Thread(target=self._work, name="render-preview",
                                            daemon=True)
            self._worker.start()

    # -- the worker --------------------------------------------------------------

    def _work(self) -> None:
        from ..trace.job import RenderJob, default_threads
        from ..trace.scene import SceneCache, compile_scene
        from ..trace.warmup import is_warm, warm_up

        cache = SceneCache()
        while True:
            with self._lock:
                while self._request is None and not self._stop:
                    self._wake.wait()
                if self._stop:
                    return
                serial, inputs, moving = self._request
                self._request = None
            self._compiling = True
            try:
                if not is_warm():
                    warm_up()
                scene = compile_scene(inputs, cache)
            except Exception as error:  # noqa: BLE001 -- shown in the caption
                self._error = str(error)
                self._compiling = False
                continue
            finally:
                self._compiling = False
            trace = inputs.path_trace
            preview = trace.preview
            job = RenderJob(
                scene, trace, samples=1 if moving else preview.samples,
                noise_threshold=0.0 if moving else preview.noise_threshold,
                min_samples=4, time_limit=0.0, threads=max(1, default_threads() - 1),
                passes=trace.denoise.preview,
            )
            from ..core.path_trace import RenderMethod

            job.method = RenderMethod.PROGRESSIVE
            with self._lock:
                if serial != self._serial or self._stop:
                    continue
                old = self._job
                self._job = job
                self._job_serial = serial
            if old is not None:
                old.cancel()
            self._job_started = time.perf_counter()
            job.start()

    # -- developing, on the interface thread --------------------------------------

    def _tick(self) -> None:
        job = self._job
        if job is None:
            if self._compiling:
                self.updated.emit()
            return
        if job is not self._shown_job:
            # A new picture: what was denoised belongs to the old one.
            self._shown_job = job
            self._denoised = None
            self._denoised_samples = 0.0
            self._forget_enhanced()
        dirty = job.take_dirty()
        if dirty or self._image is None or self._bytes is None \
                or self._bytes.shape[:2] != (job.height, job.width):
            self._develop(job)
            self._maybe_denoise(job)
            self.updated.emit()
        elif job.state.finished:
            # The last samples may have landed between two denoises.
            self._maybe_denoise(job, force=True)
            if self._best is None and self._denoise is None:
                # Nothing newer is coming: enhance the finished picture as it is shown.
                self._offer(job, self._denoised_display if self._denoised is not None
                            else self._display.copy())
        self._collect_denoise(job)
        self._collect_enhance(job)
        self._maybe_enhance(job)

    def _colour_args(self, job):
        from ..trace.colour import TRANSFORM_CODES, exposure_scale

        scene = job.scene
        color = self._state.path_trace.color
        render = self._state.render
        transform = TRANSFORM_CODES[color.view_transform.resolved(scene.skin)]
        stops = color.exposure + (scene.exposure if scene.skin else 0.0)
        return (transform, exposure_scale(stops), float(color.gamma), float(color.contrast),
                np.asarray(render.background_top, np.float64),
                np.asarray(render.background_bottom, np.float64), False, True)

    def _develop(self, job) -> None:
        from ..trace.colour import develop_region, quantize_region

        w, h = job.width, job.height
        if self._bytes is None or self._bytes.shape[:2] != (h, w):
            self._bytes = np.zeros((h, w, 4), np.uint8)
            self._display = np.zeros((h, w, 4), np.float32)
            self._image = QImage(self._bytes.data, w, h, w * 4, QImage.Format.Format_RGBA8888)
            self._denoised = None
        film = job.film
        develop_region(film.rgba, film.count, self._display, 0, 0, w, h, *self._colour_args(job))
        quantize_region(self._display, self._bytes, 0, 0, w, h)

    def _maybe_denoise(self, job, force: bool = False) -> None:
        trace = self._state.path_trace
        if not trace.denoise.preview or not job.film.passes:
            self._denoised = None
            return
        if self._denoise is not None:
            return
        now = time.perf_counter()
        from .render_controller import denoise_service

        service = denoise_service()
        infos = service.infos()
        gpu = infos is not None and any(i.available and i.on_gpu for i in infos)
        if not force and now - self._last_denoise < (0.25 if gpu else 1.0):
            return
        stats = job.stats()
        if stats.samples_done < 1.0 or stats.samples_done <= self._denoised_samples:
            return
        from ..trace.denoise import request_from_film

        rotation = self._state.camera.view_matrix()[:3, :3]
        request = request_from_film(job.film, rotation)
        self._last_denoise = now
        self._denoise = (job, stats.samples_done, service.submit(request, trace.denoise))

    def _collect_denoise(self, job) -> None:
        if self._denoise is None:
            return
        owner, samples, future = self._denoise
        if not future.done():
            return
        self._denoise = None
        if owner is not job:
            return
        try:
            image, _info, _note = future.result()
        except Exception:  # noqa: BLE001 -- the noisy picture is shown instead
            return
        from ..trace.colour import develop_region, quantize_region

        h, w = job.height, job.width
        coverage = job.film.beauty()[..., 3:4]
        rgba = np.ascontiguousarray(np.concatenate([image, coverage], axis=-1), dtype=np.float32)
        display = np.zeros((h, w, 4), np.float32)
        develop_region(rgba, np.ones((h, w), np.int32), display, 0, 0, w, h,
                       *self._colour_args(job))
        self._denoised_bytes = np.zeros((h, w, 4), np.uint8)
        quantize_region(display, self._denoised_bytes, 0, 0, w, h)
        self._denoised = QImage(self._denoised_bytes.data, w, h, w * 4,
                                QImage.Format.Format_RGBA8888)
        self._denoised_samples = samples
        self._denoised_display = display
        self._offer(job, display)
        self.updated.emit()
        if job.state.finished:
            return
        self._maybe_denoise(job)

    # -- DLSS 5 Neural Rendering ---------------------------------------------------

    def _forget_enhanced(self) -> None:
        self._best = None
        self._enhanced = None
        self._enhanced_key = None

    def _offer(self, job, display: np.ndarray) -> None:
        """Make ``display`` the next picture to enhance, when enhancing is on."""
        if not self._state.path_trace.neural.preview:
            return
        self._best_serial += 1
        self._best = (job, self._best_serial, display)

    def _maybe_enhance(self, job) -> None:
        from .render_controller import enhance_key, neural_service

        trace = self._state.path_trace
        if not trace.neural.preview or self._best is None or self._enhance is not None:
            return
        owner, serial, display = self._best
        settings = enhance_key(trace)
        key = (serial, settings)
        if owner is not job or key == self._enhanced_key:
            return
        if self._neural_error is not None \
                and self._neural_error[0] == (settings, str(engine_dir())):
            return      # Failed like this already; wait for the settings or the engine to change.
        if min(display.shape[:2]) < MIN_SIDE:
            return      # Too small, as it is while the view turns.
        self._enhance = (job, key, neural_service().submit(display, replace(trace.neural)))

    def _collect_enhance(self, job) -> None:
        if self._enhance is None:
            return
        owner, key, future = self._enhance
        if not future.done():
            return
        self._enhance = None
        if owner is not job:
            return
        try:
            image, _info = future.result()
        except Exception as error:  # noqa: BLE001 -- shown in the caption
            self._neural_error = ((key[1], str(engine_dir())), str(error))
            self.updated.emit()
            return
        from ..trace.colour import to_rgba8

        self._neural_error = None
        h, w = image.shape[:2]
        self._enhanced_bytes = np.ascontiguousarray(to_rgba8(image))
        self._enhanced = QImage(self._enhanced_bytes.data, w, h, w * 4,
                                QImage.Format.Format_RGBA8888)
        self._enhanced_key = key
        self.updated.emit()
