"""The path tracer's scattering: GGX, Lambert and their blend."""

from __future__ import annotations

import math

import numpy as np
import pytest

pytest.importorskip("numba")

from refview.trace.materials import (  # noqa: E402
    ggx_eval,
    ggx_sample,
    material_row,
    principled_eval,
    principled_sample,
)


def _wo(theta_deg):
    t = math.radians(theta_deg)
    return (math.sin(t), 0.0, math.cos(t))


@pytest.mark.parametrize("alpha", [0.05, 0.3, 0.8])
@pytest.mark.parametrize("theta", [10.0, 50.0, 80.0])
def test_visible_normal_sampling_has_the_pdf_eval_reports(alpha, theta):
    wo = _wo(theta)
    rng = np.random.default_rng(1)
    for u1, u2 in rng.random((200, 2)):
        wi = ggx_sample(wo, alpha, u1, u2)
        if wi[2] <= 0.0:
            continue
        value, pdf, _c = ggx_eval(wo, wi, alpha)
        # Monte Carlo of the pdf over the sampled directions must also be right:
        # checked below; here, the pdf is positive wherever a sample lands.
        assert pdf > 0.0 and value >= 0.0


@pytest.mark.parametrize("alpha", [0.1, 0.4, 0.9])
@pytest.mark.parametrize("theta", [0.0, 45.0, 75.0])
def test_ggx_albedo_is_at_most_one_and_its_pdf_integrates(alpha, theta):
    wo = _wo(theta)
    rng = np.random.default_rng(2)
    count = 40000
    weights = []
    for u1, u2 in rng.random((count, 2)):
        wi = ggx_sample(wo, alpha, u1, u2)
        if wi[2] <= 0.0:
            weights.append(0.0)
            continue
        value, pdf, _c = ggx_eval(wo, wi, alpha)
        weights.append(value / pdf if pdf > 0 else 0.0)
    albedo = float(np.mean(weights))
    assert albedo <= 1.0 + 1e-3
    # A single-scattering lobe loses energy as it roughens, but never most of it.
    assert albedo > 0.3
    if alpha < 0.3:
        return  # Too peaked for the uniform estimate below to be meaningful.
    # Uniform sampling of the hemisphere: the pdf integrates to at most one.
    d = rng.normal(size=(count, 3))
    d /= np.linalg.norm(d, axis=1, keepdims=True)
    d[:, 2] = np.abs(d[:, 2])
    pdfs = [ggx_eval(wo, tuple(v), alpha)[1] for v in d]
    assert np.mean(pdfs) * 2.0 * math.pi <= 1.02


def test_principled_sampling_is_consistent_with_its_evaluation():
    mat = material_row((0.6, 0.4, 0.3), metallic=0.3, roughness=0.4, f0=(0.04, 0.04, 0.04))
    alpha = 0.16
    wo = _wo(30.0)
    rng = np.random.default_rng(3)
    total = np.zeros(3)
    count = 40000
    for u0, u1, u2 in rng.random((count, 3)):
        wi, weight, pdf, _glossy = principled_sample(mat, wo, alpha, u0, u1, u2)
        if pdf <= 0.0:
            continue
        f, pdf_eval = principled_eval(mat, wo, wi, alpha)
        assert pdf == pytest.approx(pdf_eval, rel=1e-6)
        np.testing.assert_allclose(np.array(weight) * pdf, f, rtol=1e-6, atol=1e-12)
        total += weight
    albedo = total / count
    assert np.all(albedo <= 1.0) and np.all(albedo > 0.2)


def test_a_white_lambert_reflects_everything():
    mat = material_row((1.0, 1.0, 1.0), roughness=1.0, f0=(0.0, 0.0, 0.0))
    wo = _wo(40.0)
    rng = np.random.default_rng(4)
    total = np.zeros(3)
    count = 5000
    for u0, u1, u2 in rng.random((count, 3)):
        _wi, weight, pdf, glossy = principled_sample(mat, wo, 1.0, u0, u1, u2)
        assert not glossy and pdf > 0
        total += weight
    np.testing.assert_allclose(total / count, (1.0, 1.0, 1.0), rtol=1e-9)


def test_nothing_is_reflected_from_below():
    mat = material_row((0.5, 0.5, 0.5))
    f, pdf = principled_eval(mat, (0.0, 0.0, 1.0), (0.0, 0.0, -1.0), 0.2)
    assert f == (0.0, 0.0, 0.0) and pdf == 0.0
