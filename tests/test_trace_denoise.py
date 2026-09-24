"""The denoisers, each as far as this machine can run it, and EXR output."""

from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("numba")

from refview.core.path_trace import DenoiserBackend, DenoiseSettings  # noqa: E402
from refview.trace.denoise import DenoiseRequest, DenoiseService  # noqa: E402
from refview.trace.exr import read_exr_channels, write_exr  # noqa: E402
from refview.trace.film import Film  # noqa: E402


@pytest.fixture(scope="module")
def service():
    svc = DenoiseService()
    svc.probe().result()
    yield svc
    svc.shutdown()


def _scene(h=96, w=128, noise=0.15, seed=0):
    clean = np.zeros((h, w, 3), np.float32)
    clean[:, : w // 2] = (0.6, 0.4, 0.3)
    clean[:, w // 2:] = (0.08, 0.1, 0.12)
    normal = np.zeros((h, w, 3), np.float32)
    normal[:, : w // 2] = (0.0, 0.0, 1.0)
    normal[:, w // 2:] = (1.0, 0.0, 0.0)
    albedo = np.where(normal[..., :1] > 0.5, 0.5, 0.9).astype(np.float32) * np.ones(3, np.float32)
    rng = np.random.default_rng(seed)
    noisy = np.maximum(clean + rng.normal(scale=noise, size=clean.shape).astype(np.float32), 0.0)
    return clean, noisy, albedo, normal


def _backends(service):
    return [info.backend for info in service.infos() if info.available]


def test_the_built_in_denoiser_is_always_there(service):
    assert DenoiserBackend.BUILTIN in _backends(service)
    for info in service.infos():
        assert info.available or info.reason


@pytest.mark.parametrize("backend", list(DenoiserBackend))
def test_every_available_denoiser_cleans_and_keeps_edges(service, backend):
    if backend is not DenoiserBackend.AUTO and backend not in _backends(service):
        pytest.skip(next(i.reason for i in service.infos() if i.backend is backend))
    clean, noisy, albedo, normal = _scene()
    request = DenoiseRequest(noisy, albedo, normal, None,
                             np.full(noisy.shape[:2], 0.15, np.float32), np.eye(3))
    out, info, note = service.denoise(request, DenoiseSettings(backend=backend))
    assert note is None, note
    assert out.shape == noisy.shape and out.dtype == np.float32
    assert np.isfinite(out).all()
    before = np.var(noisy - clean)
    after = np.var(out - clean)
    assert after < before / 4.0, (info.summary, before, after)
    # The edge between the halves stays an edge.
    w = noisy.shape[1]
    step = out[:, w // 2 - 3].mean() - out[:, w // 2 + 3].mean()
    assert step > 0.3


def test_a_flat_picture_stays_flat(service):
    flat = np.full((64, 64, 3), 0.25, np.float32)
    out, _info, _note = service.denoise(DenoiseRequest(flat), DenoiseSettings(
        backend=DenoiserBackend.BUILTIN))
    np.testing.assert_allclose(out, flat, atol=1e-5)


def test_mix_blends_toward_the_noisy_picture(service):
    _clean, noisy, albedo, normal = _scene()
    request = DenoiseRequest(noisy, albedo, normal)
    full, *_ = service.denoise(request, DenoiseSettings(backend=DenoiserBackend.BUILTIN))
    half, *_ = service.denoise(request, DenoiseSettings(backend=DenoiserBackend.BUILTIN, mix=0.5))
    np.testing.assert_allclose(half, (full + noisy) * 0.5, atol=1e-5)


def test_exr_layers_round_trip(tmp_path):
    film = Film(6, 4)
    rgba = np.random.default_rng(0).random((4, 6, 4)).astype(np.float32) * 10
    path = write_exr(tmp_path / "r.exr", {"RGBA": rgba, "albedo": rgba[..., :3],
                                          "normal": rgba[..., :3], "depth.Z": rgba[..., 0]},
                     half=True)
    channels = read_exr_channels(path)
    assert set(channels) >= {"RGBA", "depth.Z"}
    np.testing.assert_allclose(channels["RGBA"], rgba, rtol=1e-3)
    assert channels["depth.Z"].dtype == np.float32
    assert film.memory_bytes > 0
