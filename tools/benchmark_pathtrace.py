"""Time the path tracer on a mesh: compile, ray casting, and a render each way.

Prints how long the kernels take to compile or load, how many primary rays a
second the triangle tree answers across every core, and for a render in each
method -- progressive and bucket -- the wall time, the seconds per sample and
the rays a second.  Adaptive sampling is off, so both methods do the same
work and draw the same image; the two are compared, and any difference is
reported.

Run with::

    python tools/benchmark_pathtrace.py [mesh] [--mode pbr] [--size 640x480]
                                        [--samples 32] [--threads 0]

With no mesh, the bundled ``resources/models/Pose_02.obj`` is used.
"""

from __future__ import annotations

import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from refview.core.camera import Camera  # noqa: E402
from refview.core.mesh_io import load_mesh  # noqa: E402
from refview.core.path_trace import PathTraceSettings, RenderMethod  # noqa: E402
from refview.core.settings import RenderSettings, ShadingMode  # noqa: E402


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("mesh", nargs="?",
                        default=str(ROOT / "resources" / "models" / "Pose_02.obj"))
    parser.add_argument("--mode", default=ShadingMode.PBR.value,
                        choices=[mode.value for mode in ShadingMode])
    parser.add_argument("--size", default="640x480", help="width x height of the render")
    parser.add_argument("--samples", type=int, default=32)
    parser.add_argument("--threads", type=int, default=0, help="0 for every core but one")
    return parser.parse_args()


def _cast(geo, camera: Camera, width: int, height: int, threads: int) -> tuple[float, float]:
    """Primary rays through every pixel, across the cores: (rays a second, hit share)."""
    from refview.trace.geometry import cast_rays

    ys, xs = np.mgrid[0:height, 0:width]
    origins, directions = camera.rays(xs.ravel() + 0.5, ys.ravel() + 0.5, width, height)
    origins = np.ascontiguousarray(origins, np.float64)
    directions = np.ascontiguousarray(directions, np.float64)
    triangles = np.empty(len(origins), np.int32)
    distances = np.empty(len(origins), np.float64)
    chunks = np.array_split(np.arange(len(origins)), threads * 8)

    def run(index):
        cast_rays(geo, origins[index], directions[index], np.inf, triangles[index],
                  distances[index])

    run(chunks[0][:16])     # compiled or loaded before the clock starts
    best = np.inf
    with ThreadPoolExecutor(threads) as pool:
        for _ in range(3):
            started = time.perf_counter()
            # Slices are views, so each chunk writes its own part of the outputs.
            list(pool.map(run, [slice(c[0], c[-1] + 1) for c in chunks if len(c)]))
            best = min(best, time.perf_counter() - started)
    return len(origins) / best, float(np.mean(triangles >= 0))


def main() -> None:
    args = _arguments()
    width, height = (int(v) for v in args.size.lower().split("x"))

    from refview.trace import available, unavailable_reason
    if not available():
        raise SystemExit(f"The path tracer cannot run here: {unavailable_reason()}")
    from refview.trace.job import RenderJob, default_threads
    from refview.trace.scene import PartKind, SceneCache, TraceInputs, TracePart, compile_scene
    from refview.trace.warmup import warm_up

    threads = args.threads or default_threads()
    seconds = warm_up()
    print(f"kernels        {seconds:6.1f} s to compile or load")

    started = time.perf_counter()
    mesh = load_mesh(args.mesh)
    print(f"mesh           {Path(args.mesh).name}: {mesh.triangle_count:,} triangles, "
          f"read in {time.perf_counter() - started:.1f} s")
    camera = Camera()
    camera.frame(mesh.bounds)

    render = RenderSettings(shading_mode=ShadingMode(args.mode))
    trace = PathTraceSettings()
    trace.sampling.noise_threshold = 0.0     # the same work in both methods
    trace.denoise.final = False
    inputs = TraceInputs(parts=(TracePart(mesh, PartKind.MODEL),), camera=camera,
                         width=width, height=height, render=render, path_trace=trace)
    started = time.perf_counter()
    scene = compile_scene(inputs, SceneCache())
    print(f"scene          compiled (tree and tables) in {time.perf_counter() - started:.2f} s")

    rate, hit = _cast(scene.geometry, camera, width, height, threads)
    print(f"ray casting    {rate / 1e6:6.1f} M primary rays/s on {threads} threads "
          f"({hit:.0%} hit the mesh)")

    images = {}
    for method in (RenderMethod.PROGRESSIVE, RenderMethod.BUCKET):
        job = RenderJob(scene, trace, samples=args.samples, noise_threshold=0.0,
                        threads=threads, passes=False, method=method)
        started = time.perf_counter()
        job.run()
        wall = time.perf_counter() - started
        stats = job.stats()
        images[method] = job.film.beauty().copy()
        print(f"{method.value:<14} {wall:6.2f} s for {args.samples} spp at {width}x{height}  "
              f"({wall / args.samples * 1000:.0f} ms/spp, "
              f"{stats.rays_per_second / 1e6:.1f} M rays/s)")
    a, b = images[RenderMethod.PROGRESSIVE], images[RenderMethod.BUCKET]
    difference = float(np.max(np.abs(a - b)))
    print("methods        " + ("identical images" if difference == 0.0
                               else f"differ by up to {difference:.3g}"))


if __name__ == "__main__":
    main()
