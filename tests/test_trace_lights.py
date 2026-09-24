"""The path tracer's lights: discs, the sky and the HDRI's importance sampling."""

from __future__ import annotations

import math

import numpy as np
import pytest

pytest.importorskip("numba")

from refview.core.camera import Camera  # noqa: E402
from refview.core.path_trace import PathTraceSettings  # noqa: E402
from refview.core.settings import LightingMode, RenderSettings, ShadingMode  # noqa: E402
from refview.trace.lights import (  # noqa: E402
    disc_hit,
    disc_sample,
    env_pdf,
    env_radiance,
    env_sample,
    light_row,
    sky_radiance,
)
from refview.trace.scene import (  # noqa: E402
    PartKind,
    SceneCache,
    TraceInputs,
    TracePart,
    compile_scene,
)
from trace_scenes import gradient_sky, sphere  # noqa: E402


def _shading(env, rotation_deg=30.0):
    render = RenderSettings(shading_mode=ShadingMode.PBR)
    render.light.mode = LightingMode.ENVIRONMENT
    render.light.environment_rotation_deg = rotation_deg
    camera = Camera(eye=np.array([0.3, 0.4, 3.0]))
    inputs = TraceInputs(parts=(TracePart(sphere(8), PartKind.MODEL),), camera=camera, width=8,
                         height=8, render=render, path_trace=PathTraceSettings(), environment=env)
    return compile_scene(inputs, SceneCache()).shading


def _uniform_directions(count, seed=0):
    d = np.random.default_rng(seed).normal(size=(count, 3))
    return d / np.linalg.norm(d, axis=1, keepdims=True)


def test_the_hdri_pdf_integrates_to_one_over_the_sphere():
    sh = _shading(gradient_sky())
    directions = _uniform_directions(200000)
    pdfs = np.array([env_pdf(sh, tuple(d)) for d in directions])
    # E[pdf / uniform pdf] over uniform directions is the integral of the pdf.
    assert np.mean(pdfs) * 4.0 * math.pi == pytest.approx(1.0, abs=0.02)


def test_a_sampled_direction_has_the_pdf_env_pdf_gives_it():
    sh = _shading(gradient_sky())
    rng = np.random.default_rng(2)
    for u1, u2 in rng.random((500, 2)):
        d, weight, pdf = env_sample(sh, u1, u2)
        assert np.linalg.norm(d) == pytest.approx(1.0, abs=1e-9)
        assert pdf == pytest.approx(env_pdf(sh, d), rel=1e-4)
        radiance = env_radiance(sh, d)
        np.testing.assert_allclose(np.array(weight) * pdf, radiance, rtol=1e-4, atol=1e-9)


def test_importance_sampling_estimates_the_irradiance():
    """Radiance over pdf, averaged, is the integral of the radiance: the same both ways."""
    sh = _shading(gradient_sky())
    rng = np.random.default_rng(3)
    estimates = []
    for u1, u2 in rng.random((40000, 2)):
        _d, weight, pdf = env_sample(sh, u1, u2)
        if pdf > 0:
            estimates.append(weight[1])
    sampled = np.mean(estimates)
    directions = _uniform_directions(400000, seed=4)
    uniform = np.mean([env_radiance(sh, tuple(d))[1] for d in directions]) * 4.0 * math.pi
    assert sampled == pytest.approx(uniform, rel=0.03)


def test_a_disc_light_delivers_its_irradiance():
    direction = (0.0, 0.0, 1.0)
    lights = np.array([light_row(direction, (2.0, 1.0, 0.5), math.radians(8.0))])
    rng = np.random.default_rng(0)
    total = np.zeros(3)
    count = 20000
    for u1, u2 in rng.random((count, 2)):
        wi, weight, pdf = disc_sample(lights, 0, u1, u2)
        assert pdf > 0
        # Every sampled direction lies in the disc, and seen there has the same pdf.
        _le, hit_pdf = disc_hit(lights, 0, wi)
        assert hit_pdf == pytest.approx(pdf)
        total += np.array(weight) * wi[2]
    np.testing.assert_allclose(total / count, (2.0, 1.0, 0.5), rtol=0.01)


def test_a_point_light_is_a_delta():
    lights = np.array([light_row((0.0, 1.0, 0.0), (1.0, 1.0, 1.0), 0.0)])
    wi, weight, pdf = disc_sample(lights, 0, 0.3, 0.7)
    assert pdf == 0.0 and wi == (0.0, 1.0, 0.0) and weight == (1.0, 1.0, 1.0)
    _le, hit_pdf = disc_hit(lights, 0, (0.0, 1.0, 0.0))
    assert hit_pdf == 0.0


def test_the_sky_is_brighter_overhead():
    sky = np.array([1.0, 1.0, 1.0, 1.0])
    assert sky_radiance(sky, (0.0, 1.0, 0.0))[0] == pytest.approx(1.0)
    assert sky_radiance(sky, (0.0, -1.0, 0.0))[0] == pytest.approx(0.35)
    assert sky_radiance(np.zeros(4), (0.0, 1.0, 0.0)) == (0.0, 0.0, 0.0)
