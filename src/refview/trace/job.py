"""A render in progress: the threads, the order the pixels are done in, and when to stop.

Two ways of filling the picture in, over the same kernel:

* **progressive** -- the whole frame a few samples at a time, in passes of
  1, 1, 2, 4, 8, 16, 16... samples, so the first picture comes quickly and
  every pass halves what noise is left or near enough;
* **bucket** -- one square at a time, each rendered to the end (or until its
  noise is below the threshold) before the next is started, in the order the
  artist chose: from the centre out, along a Hilbert curve, in rows, or at
  random.

The work is cut into tiles that the thread pool takes one at a time; the
kernels release the interpreter lock, so the threads run side by side.  A
render stops when every pixel has its samples, when every pixel's noise is
under the threshold, when its time is up, or when it is cancelled -- which
the kernels notice at the end of a row, so a cancel lands within a moment.
"""

from __future__ import annotations

import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait
from dataclasses import dataclass, field
from enum import Enum

import numpy as np

from ..core.path_trace import BucketOrder, PathTraceSettings, RenderMethod
from .film import Film
from .integrator import adaptive_error, render_tile
from .scene import CompiledScene

#: Samples a bucket takes between looks at its noise.
BUCKET_ROUND = 16
#: A progressive pass's tiles: big enough to keep the per-call cost small,
#: small enough that fifteen threads share a pass evenly.
PASS_TILE = 64
#: Adaptive sampling decides by blocks of this many pixels a side.
ADAPTIVE_BLOCK = 8


class JobState(Enum):
    WAITING = "waiting"
    RENDERING = "rendering"
    DONE = "done"
    CANCELLED = "cancelled"
    FAILED = "failed"

    @property
    def finished(self) -> bool:
        return self in (JobState.DONE, JobState.CANCELLED, JobState.FAILED)


@dataclass
class RenderStats:
    state: JobState = JobState.WAITING
    elapsed: float = 0.0
    remaining: float | None = None
    pass_index: int = 0
    #: The mean samples a pixel has, and what each is to have.
    samples_done: float = 0.0
    samples_target: int = 0
    tiles_done: int = 0
    tiles_total: int = 0
    rays: int = 0
    rays_per_second: float = 0.0
    threads: int = 1
    memory_bytes: int = 0
    #: The share of pixels still taking samples.
    open_share: float = 1.0
    error: str | None = None
    extra: dict = field(default_factory=dict)


def default_threads() -> int:
    return max(1, (os.cpu_count() or 2) - 1)


def tile_order(width: int, height: int, size: int, order: BucketOrder = BucketOrder.SPIRAL,
               seed: int = 0) -> list[tuple[int, int, int, int]]:
    """The picture cut into ``size``-pixel squares, in the order they are rendered."""
    size = max(int(size), 1)
    cols = (width + size - 1) // size
    rows = (height + size - 1) // size
    cells = [(c, r) for r in range(rows) for c in range(cols)]
    if order is BucketOrder.SPIRAL:
        cx, cy = (cols - 1) / 2.0, (rows - 1) / 2.0
        import math

        cells.sort(key=lambda cr: (max(abs(cr[0] - cx), abs(cr[1] - cy)),
                                   math.atan2(cr[1] - cy, cr[0] - cx)))
    elif order is BucketOrder.HILBERT:
        n = 1
        while n < max(cols, rows):
            n *= 2
        cells.sort(key=lambda cr: _hilbert_index(n, cr[0], cr[1]))
    elif order is BucketOrder.RANDOM:
        random.Random(seed).shuffle(cells)
    return [(c * size, r * size, min((c + 1) * size, width), min((r + 1) * size, height))
            for c, r in cells]


def _hilbert_index(n: int, x: int, y: int) -> int:
    d = 0
    s = n // 2
    while s > 0:
        rx = 1 if (x & s) > 0 else 0
        ry = 1 if (y & s) > 0 else 0
        d += s * s * ((3 * rx) ^ ry)
        if ry == 0:
            if rx == 1:
                x, y = s - 1 - x, s - 1 - y
            x, y = y, x
        s //= 2
    return d


def pass_schedule(total: int) -> list[tuple[int, int]]:
    """Sample ranges of the progressive passes: 1, 1, 2, 4, 8, 16, 16, ... up to ``total``."""
    ranges = []
    start = 0
    size = 1
    first = True
    while start < total:
        end = min(start + size, total)
        ranges.append((start, end))
        start = end
        if first:
            first = False
        else:
            size = min(size * 2, 16)
    return ranges


def _lower_priority() -> None:
    """Run this thread below normal priority, so the rest of the computer stays quick."""
    if sys.platform == "win32":
        try:
            import ctypes

            kernel32 = ctypes.windll.kernel32
            kernel32.SetThreadPriority(kernel32.GetCurrentThread(), -1)  # BELOW_NORMAL
        except Exception:  # noqa: BLE001 -- a priority is a nicety
            pass


class RenderJob:
    """One render of a compiled scene into a film, on a pool of threads."""

    def __init__(self, scene: CompiledScene, settings: PathTraceSettings, *,
                 samples: int | None = None, noise_threshold: float | None = None,
                 min_samples: int | None = None, time_limit: float | None = None,
                 method: RenderMethod | None = None, threads: int | None = None,
                 passes: bool = True, film: Film | None = None) -> None:
        self.scene = scene
        params = scene.params
        self.width, self.height = int(params.width), int(params.height)
        sampling = settings.sampling
        perf = settings.performance
        self.samples = max(int(samples if samples is not None else sampling.samples), 1)
        self.threshold = float(noise_threshold if noise_threshold is not None
                               else sampling.noise_threshold)
        self.min_samples = min(max(int(min_samples if min_samples is not None
                                       else sampling.min_samples), 2), self.samples)
        limit = time_limit if time_limit is not None else sampling.time_limit_s
        self.time_limit = float(limit) if limit and limit > 0 else None
        self.method = method or perf.method
        self.bucket_size = int(perf.bucket_size)
        self.bucket_order = perf.bucket_order
        self.seed = int(sampling.seed)
        self.threads = int(threads or perf.threads or default_threads())
        self.low_priority = bool(perf.low_priority)
        self.film = film if film is not None else Film(self.width, self.height, passes)
        self._cancel = np.zeros(1, np.int32)
        self._counters = np.zeros((self.threads + 1, 2), np.int64)
        self._lock = threading.Lock()
        self._dirty: list[tuple[int, int, int, int]] = []
        self._active: set[tuple[int, int, int, int]] = set()
        self._state = JobState.WAITING
        self._error: str | None = None
        self._started = 0.0
        self._finished_at: float | None = None
        self._pass_index = 0
        self._tiles_done = 0
        self._tiles_total = 0
        self._open = self.width * self.height
        self._thread: threading.Thread | None = None
        self._done = threading.Event()
        self._slot = threading.local()
        self._slots = 0

    # -- control ---------------------------------------------------------------

    def start(self) -> None:
        self._started = time.perf_counter()
        self._state = JobState.RENDERING
        self._thread = threading.Thread(target=self._run, name="render-job", daemon=True)
        self._thread.start()

    def run(self) -> None:
        """Render on the calling thread, to the end; for tests and tools."""
        self._started = time.perf_counter()
        self._state = JobState.RENDERING
        self._run()

    def cancel(self) -> None:
        self._cancel[0] = 1

    def wait(self, timeout: float | None = None) -> bool:
        return self._done.wait(timeout)

    @property
    def state(self) -> JobState:
        return self._state

    @property
    def cancelled(self) -> bool:
        return bool(self._cancel[0])

    # -- what the interface reads ------------------------------------------------

    def take_dirty(self) -> list[tuple[int, int, int, int]]:
        with self._lock:
            dirty, self._dirty = self._dirty, []
        return dirty

    def active_tiles(self) -> list[tuple[int, int, int, int]]:
        with self._lock:
            return list(self._active)

    def stats(self) -> RenderStats:
        now = self._finished_at or time.perf_counter()
        elapsed = max(now - self._started, 0.0) if self._started else 0.0
        rays = int(self._counters[:, 1].sum())
        taken = int(self._counters[:, 0].sum())
        pixels = max(self.width * self.height, 1)
        done_mean = taken / pixels
        open_share = self._open / pixels
        remaining = None
        if self._state is JobState.RENDERING and elapsed > 0.5 and taken > 0:
            if self.method is RenderMethod.BUCKET and self._tiles_total:
                fraction = self._tiles_done / self._tiles_total
            else:
                fraction = min(done_mean / self.samples, 1.0)
                fraction = max(fraction, 1.0 - open_share)
            if fraction > 0.0:
                remaining = elapsed * (1.0 - fraction) / fraction
            if self.time_limit is not None:
                left = max(self.time_limit - elapsed, 0.0)
                remaining = left if remaining is None else min(remaining, left)
        return RenderStats(
            state=self._state, elapsed=elapsed, remaining=remaining,
            pass_index=self._pass_index, samples_done=done_mean, samples_target=self.samples,
            tiles_done=self._tiles_done, tiles_total=self._tiles_total, rays=rays,
            rays_per_second=rays / elapsed if elapsed > 0 else 0.0, threads=self.threads,
            memory_bytes=self.film.memory_bytes, open_share=open_share, error=self._error,
        )

    # -- the work --------------------------------------------------------------

    def _slot_index(self) -> int:
        slot = getattr(self._slot, "index", None)
        if slot is None:
            with self._lock:
                self._slots += 1
                slot = min(self._slots, self.threads)
            self._slot.index = slot
            if self.low_priority:
                _lower_priority()
        return slot

    def _out_of_time(self) -> bool:
        return (self.time_limit is not None
                and time.perf_counter() - self._started >= self.time_limit)

    def _render(self, rect, s0, s1) -> int:
        film = self.film
        scene = self.scene
        x0, y0, x1, y1 = rect
        return render_tile(scene.geometry, scene.shading, scene.params, film.rgba, film.even,
                           film.count, film.albedo, film.normal, film.depth, film.converged,
                           x0, y0, x1, y1, s0, s1, self._cancel, self._counters,
                           self._slot_index())

    def _mark(self, rect) -> None:
        with self._lock:
            self._dirty.append(rect)

    def _run(self) -> None:
        try:
            with ThreadPoolExecutor(self.threads, thread_name_prefix="render") as pool:
                if self.method is RenderMethod.BUCKET:
                    self._run_buckets(pool)
                else:
                    self._run_passes(pool)
            if self._cancel[0]:
                self._state = JobState.CANCELLED
            else:
                self._state = JobState.DONE
        except Exception as error:  # noqa: BLE001 -- reported to the interface
            self._error = f"{error.__class__.__name__}: {error}"
            self._state = JobState.FAILED
        finally:
            self._finished_at = time.perf_counter()
            with self._lock:
                self._active.clear()
            self._done.set()

    def _adaptive(self, rect) -> int:
        x0, y0, x1, y1 = rect
        return adaptive_error(self.film.rgba, self.film.even, self.film.count,
                              self.film.converged, x0, y0, x1, y1, self.threshold,
                              self.min_samples, ADAPTIVE_BLOCK)

    def _run_passes(self, pool) -> None:
        size = PASS_TILE if self.width * self.height > 256 * 256 else 32
        tiles = tile_order(self.width, self.height, size, BucketOrder.ROWS)
        self._tiles_total = len(tiles)
        whole = (0, 0, self.width, self.height)
        for index, (s0, s1) in enumerate(pass_schedule(self.samples)):
            if self._cancel[0] or self._out_of_time():
                break
            self._pass_index = index + 1

            def work(rect, s0=s0, s1=s1):
                if self._cancel[0] or self._out_of_time():
                    return 0
                taken = self._render(rect, s0, s1)
                self._mark(rect)
                return taken

            futures = [pool.submit(work, rect) for rect in tiles]
            wait(futures)
            for future in futures:
                future.result()
            if self.threshold > 0.0 and s1 >= self.min_samples:
                self._open = self._adaptive(whole)
                self._mark(whole)
                if self._open == 0:
                    break
            self._tiles_done = self._tiles_total

    def _run_buckets(self, pool) -> None:
        tiles = tile_order(self.width, self.height, self.bucket_size, self.bucket_order,
                           self.seed)
        self._tiles_total = len(tiles)
        pixels = max(self.width * self.height, 1)

        def work(rect):
            if self._cancel[0] or self._out_of_time():
                return
            with self._lock:
                self._active.add(rect)
            try:
                for s0 in range(0, self.samples, BUCKET_ROUND):
                    if self._cancel[0] or self._out_of_time():
                        break
                    s1 = min(s0 + BUCKET_ROUND, self.samples)
                    self._render(rect, s0, s1)
                    self._mark(rect)
                    if (self.threshold > 0.0 and s1 >= self.min_samples
                            and self._adaptive(rect) == 0):
                        break
            finally:
                with self._lock:
                    self._active.discard(rect)
                    self._tiles_done += 1
                    x0, y0, x1, y1 = rect
                    self._open -= (x1 - x0) * (y1 - y0)
                    self._open = max(self._open, 0)
                    self._pass_index = self._tiles_done
                self._mark(rect)

        futures = [pool.submit(work, rect) for rect in tiles]
        wait(futures)
        for future in futures:
            future.result()
        self._open = max(self._open, 0) if self._open < pixels else pixels
