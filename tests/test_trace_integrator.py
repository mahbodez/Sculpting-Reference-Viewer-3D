"""Whole renders: energy, determinism, the two methods, stopping, adaptive sampling."""

from __future__ import annotations

import time

import numpy as np
import pytest

pytest.importorskip("numba")

from refview.core.path_trace import PathTraceSettings, RenderMethod  # noqa: E402
from refview.core.settings import LightingMode, RenderSettings, ShadingMode  # noqa: E402
from refview.trace.job import JobState, RenderJob, pass_schedule, tile_order  # noqa: E402
from refview.trace.scene import (  # noqa: E402
    PartKind,
    SceneCache,
    TraceInputs,
    TracePart,
    compile_scene,
)
from trace_scenes import constant_sky, looking_at_origin, sphere  # noqa: E402


def _inputs(mode=ShadingMode.LAMBERT, env=None, size=(48, 48), samples=16, distance=4.0,
            **light):
    render = RenderSettings(shading_mode=mode)
    render.surface.diffuse_color = (0.5, 0.5, 0.5)
    if env is not None:
        render.light.mode = LightingMode.ENVIRONMENT
    for key, value in light.items():
        setattr(render.light, key, value)
    trace = PathTraceSettings()
    trace.sampling.samples = samples
    trace.sampling.noise_threshold = 0.0
    return TraceInputs(parts=(TracePart(sphere(32), PartKind.MODEL),),
                       camera=looking_at_origin(distance), width=size[0], height=size[1],
                       render=render,
                       path_trace=trace, environment=env)


def _render(inputs, **job):
    scene = compile_scene(inputs, SceneCache())
    render = RenderJob(scene, inputs.path_trace, threads=job.pop("threads", 4), **job)
    render.run()
    return render


def test_white_furnace_a_grey_ball_under_a_uniform_sky_is_its_albedo():
    """Under light of radiance one from everywhere, a convex matte ball shows its albedo."""
    env = constant_sky((1.0, 1.0, 1.0))
    render = _render(_inputs(env=env, samples=64))
    beauty = render.film.beauty()
    covered = beauty[..., 3] > 0.999
    assert covered.sum() > 200
    albedo = (0.5 + 0.055) / 1.055
    albedo = albedo ** 2.4   # the linear value of sRGB 0.5
    # The HDRI's strength of one puts the map's peak irradiance at pi (display modes).
    radiance = beauty[covered, :3].mean(axis=0)
    np.testing.assert_allclose(radiance, albedo, rtol=0.02)


def test_the_background_is_left_out_and_the_ball_covers_its_pixels():
    render = _render(_inputs(samples=4))
    alpha = render.film.beauty()[..., 3]
    assert alpha[0, 0] == 0.0
    assert alpha[24, 24] == pytest.approx(1.0)


def test_bucket_and_progressive_make_the_same_picture():
    inputs = _inputs(samples=24)
    progressive = _render(inputs, method=RenderMethod.PROGRESSIVE)
    bucket = _render(inputs, method=RenderMethod.BUCKET)
    np.testing.assert_array_equal(progressive.film.count, bucket.film.count)
    np.testing.assert_array_equal(progressive.film.rgba, bucket.film.rgba)


def test_the_seed_changes_the_noise_and_only_the_noise():
    inputs = _inputs(samples=8)
    a = _render(inputs).film.beauty()
    b = _render(inputs).film.beauty()
    np.testing.assert_array_equal(a, b)
    inputs.path_trace.sampling.seed = 99
    c = _render(inputs).film.beauty()
    assert not np.array_equal(a, c)
    assert abs(float(a[..., :3].mean()) - float(c[..., :3].mean())) < 0.02


def test_no_sample_is_ever_nan():
    for mode in (ShadingMode.PBR, ShadingMode.PHONG, ShadingMode.MATCAP, ShadingMode.HUMAN_SKIN):
        render = _render(_inputs(mode=mode, env=constant_sky(), samples=4))
        assert np.isfinite(render.film.rgba).all(), mode


def test_a_cancel_stops_the_render_promptly():
    inputs = _inputs(size=(320, 240), samples=100000)
    scene = compile_scene(inputs, SceneCache())
    job = RenderJob(scene, inputs.path_trace, threads=4)
    job.start()
    time.sleep(0.3)
    started = time.perf_counter()
    job.cancel()
    assert job.wait(5.0)
    assert time.perf_counter() - started < 1.0
    assert job.state is JobState.CANCELLED


def test_the_time_limit_is_honoured():
    inputs = _inputs(size=(160, 120), samples=100000)
    inputs.path_trace.sampling.time_limit_s = 0.5
    started = time.perf_counter()
    job = _render(inputs)
    assert time.perf_counter() - started < 3.0
    assert job.state is JobState.DONE
    assert job.film.count.max() < 100000


def test_adaptive_sampling_spends_less_on_the_quiet_background():
    inputs = _inputs(env=constant_sky(), samples=256, distance=8.0)
    inputs.path_trace.sampling.noise_threshold = 0.05
    inputs.path_trace.sampling.min_samples = 8
    job = _render(inputs)
    count = job.film.count
    # The empty corners converge at the minimum; the ball takes more.
    assert count[0, 0] < count[24, 24]
    assert count.mean() < 256


def test_schedules():
    assert pass_schedule(40) == [(0, 1), (1, 2), (2, 4), (4, 8), (8, 16), (16, 32), (32, 40)]
    tiles = tile_order(100, 70, 32)
    covered = np.zeros((70, 100), int)
    for x0, y0, x1, y1 in tiles:
        covered[y0:y1, x0:x1] += 1
    assert (covered == 1).all()
    # A spiral starts at the centre: its first bucket is one of those touching it.
    x0, y0, x1, y1 = tiles[0]
    assert abs((x0 + x1) / 2 - 50) <= 32 and abs((y0 + y1) / 2 - 35) <= 32
