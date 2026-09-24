"""Compiling the kernels before the first render needs them.

numba compiles a kernel the first time it is called and keeps the result on
disk (see :mod:`refview.trace.jit`); on a new install, or after an upgrade,
that first call takes a while -- the integrator with the whole skin in it is
a large function.  :func:`warm_up` makes those first calls on a scene of a
few triangles, so the time goes on a progress card the artist can see
rather than on a render that seems to hang.  With the kernels on disk it
takes a moment.
"""

from __future__ import annotations

import time

import numpy as np

from ..core.camera import Camera
from ..core.mesh import Mesh
from ..core.path_trace import PathTraceSettings
from ..core.progress import Progress
from ..core.settings import RenderSettings, ShadingMode

_done = False


def is_warm() -> bool:
    return _done


def _tetrahedron() -> Mesh:
    positions = np.array([[0, 1, 0], [-1, -1, 1], [1, -1, 1], [0, -1, -1]], np.float32)
    indices = np.array([[0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 3, 2]], np.uint32)
    return Mesh(positions=positions, normals=positions / np.linalg.norm(positions, axis=1)[:, None],
                indices=indices)


def warm_up(progress: Progress | None = None) -> float:
    """Compile (or load) every kernel; returns the seconds it took."""
    global _done
    started = time.perf_counter()
    if progress is not None:
        progress.report(message="Loading the path tracer...")
    from .colour import develop_region, quantize_region
    from .denoise_atrous import atrous
    from .job import RenderJob
    from .scene import PartKind, SceneCache, TraceInputs, TracePart, compile_scene

    render = RenderSettings(shading_mode=ShadingMode.HUMAN_SKIN)
    trace = PathTraceSettings()
    trace.sampling.samples = 2
    trace.sampling.noise_threshold = 0.5
    trace.sampling.min_samples = 2
    camera = Camera(eye=np.array([0.0, 0.0, 4.0]))
    inputs = TraceInputs(parts=(TracePart(_tetrahedron(), PartKind.MODEL),), camera=camera,
                         width=4, height=4, render=render, path_trace=trace)
    if progress is not None:
        progress.report(message="Compiling render kernels (first run only)...")
    scene = compile_scene(inputs, SceneCache())
    job = RenderJob(scene, trace, threads=1)
    job.run()
    if job.stats().error:
        raise RuntimeError(job.stats().error)
    if progress is not None:
        progress.report(message="Compiling the picture developer...")
    film = job.film
    out = np.zeros((4, 4, 4), np.float32)
    develop_region(film.rgba, film.count, out, 0, 0, 4, 4, 1, 1.0, 1.0, 0.0,
                   np.zeros(3), np.zeros(3), False, True)
    quantize_region(out, np.zeros((4, 4, 4), np.uint8), 0, 0, 4, 4)
    if progress is not None:
        progress.report(message="Compiling the built-in denoiser...")
    atrous(film.beauty()[..., :3], film.albedo_pass(), film.normal_pass(), film.depth_pass(),
           None, passes=1)
    _done = True
    return time.perf_counter() - started
