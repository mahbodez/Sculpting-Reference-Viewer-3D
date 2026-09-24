"""DLSS 5 Neural Rendering through the Neuroframe Engine: its ABI, the engine's
search, and the calls, against a stand-in for the DLL.

The engine itself is not in the repository.  Set ``REFVIEW_NEURAL_ENGINE`` to
a Visual Enhancer folder to run the last test against the real one, on an
RTX 50 series GPU.
"""

from __future__ import annotations

import ctypes
import os
import time

import numpy as np
import pytest

from refview.core.path_trace import NeuralSettings, NeuralStyle
from refview.trace import neural
from refview.trace.neural import (
    REQUIRED_FILES,
    NeuralBridge,
    NeuralError,
    NeuralPoisonedError,
    NeuralService,
    RenderParameters,
    check_size,
    engine_dir,
    render_parameters,
    set_engine_dir,
)


@pytest.fixture(autouse=True)
def _no_engine_folder():
    set_engine_dir(None)
    yield
    set_engine_dir(None)


def _install(folder):
    folder.mkdir(parents=True, exist_ok=True)
    for name in REQUIRED_FILES:
        (folder / name).write_bytes(b"")
    return folder


class _Export:
    """A function as a DLL exports it: callable, and taking ``argtypes`` and ``restype``."""

    def __init__(self, function):
        self.function = function

    def __call__(self, *args):
        return self.function(*args)


class FakeEngine:
    """The engine's exported functions, in Python: inverts the picture, or misbehaves."""

    def __init__(self, abi=6, fail=None, delay=0.0):
        self.abi = abi
        self.fail = fail
        self.delay = delay
        self.params: list[dict] = []
        self.sizes: list[tuple[int, int]] = []
        self.inits = 0
        self.releases = 0
        for name in dir(self):
            if name.startswith("dlss5nr_"):
                setattr(self, name, _Export(getattr(self, name)))

    def dlss5nr_version(self):
        return b"11.0"

    def dlss5nr_gpu_name(self):
        return b"NVIDIA GeForce RTX 5070 Laptop GPU"

    def dlss5nr_frame_abi_version(self):
        return self.abi

    def dlss5nr_init(self, ordinal, directory, error, size):
        self.inits += 1
        return 1

    def dlss5nr_process_v6(self, source, dest, width, height, params, error, size):
        if self.delay:
            time.sleep(self.delay)
        if self.fail == "raise":
            raise OSError("exception: access violation reading 0x0")
        if self.fail:
            error.value = self.fail.encode()
            return 0
        struct = params._obj
        self.params.append({name: getattr(struct, name) for name, _ in struct._fields_})
        self.sizes.append((width, height))
        count = width * height * 3
        src = np.ctypeslib.as_array(source, shape=(count,))
        np.ctypeslib.as_array(dest, shape=(count,))[:] = 1.0 - src
        return 1

    def dlss5nr_release_session(self):
        self.releases += 1
        return 1


def test_the_parameters_are_laid_out_as_the_engine_reads_them():
    # Natural C alignment: the 64-bit mask pointer is padded to offset 64.
    assert RenderParameters.mask_plane.offset == 64
    assert RenderParameters.face_skin_protection.offset == 72
    assert RenderParameters.nr_passes.offset == 80
    assert RenderParameters.prefer_nvof.offset == 88
    assert ctypes.sizeof(RenderParameters) == 96


def test_settings_become_the_engines_controls():
    settings = NeuralSettings(style=NeuralStyle.CINEMATIC, intensity=1.5, passes=3,
                              local_tone=0.5, local_structure=1.25, skin_structure=0.75,
                              color_strength=0.25, tone_preservation=0.5,
                              face_skin_protection=0.4, auto_mask=True)
    params = render_parameters(settings)
    assert params.struct_size == 96 and params.abi_version == 6
    assert params.style == 2
    assert params.intensity == pytest.approx(1.5)
    assert params.tone == pytest.approx(0.5)
    assert params.structure == pytest.approx(1.25)
    assert params.skin == pytest.approx(0.75)
    assert params.color_strength == pytest.approx(0.25)
    assert params.tone_preservation == pytest.approx(0.5)
    assert params.face_skin_protection == pytest.approx(0.4)
    assert params.nr_passes == 3
    assert params.automask == 1
    # A still: history reset every time, no mask, no temporal smoothing.
    assert params.reset == 1
    assert params.mask_memory_type == 2 and params.mask_plane == 0
    assert params.shimmer_suppression == 0.0 and params.prefer_nvof == 0


def test_the_engine_is_found_in_any_of_a_visual_enhancer_folders(tmp_path, monkeypatch):
    monkeypatch.setenv("REFVIEW_RESOURCES", str(tmp_path / "no-resources"))
    assert engine_dir() is None
    root = tmp_path / "Visual Enhancer"
    runtime = _install(root / "bin" / "runtime" / "dlssnr")
    for chosen in (root, root / "bin", root / "bin" / "runtime", runtime):
        set_engine_dir(chosen)
        assert engine_dir() == runtime
    (runtime / REQUIRED_FILES[2]).unlink()
    assert engine_dir() is None
    assert str(root) in neural.missing_reason()


def test_a_bundled_engine_is_used_when_no_folder_is_set(tmp_path, monkeypatch):
    monkeypatch.setenv("REFVIEW_RESOURCES", str(tmp_path))
    bundled = _install(tmp_path / "dlssnr")
    assert engine_dir() == bundled


def test_sizes_outside_the_engines_are_refused():
    check_size(64, 64)
    check_size(7680, 4320)
    for width, height in ((63, 200), (7681, 100), (4400, 4400)):
        with pytest.raises(NeuralError):
            check_size(width, height)


def test_the_bridge_runs_a_picture_through_the_engine(tmp_path):
    engine = FakeEngine()
    bridge = NeuralBridge(tmp_path, library=engine)
    bridge.load()
    assert bridge.version == "11.0"
    bridge.initialize()
    bridge.initialize()
    assert engine.inits == 1
    assert "RTX 5070" in bridge.gpu_name
    rgb = np.random.default_rng(0).random((80, 96, 3), dtype=np.float32)
    out = bridge.process(rgb, NeuralSettings(passes=2))
    np.testing.assert_allclose(out, 1.0 - rgb, atol=1e-6)
    assert engine.sizes == [(96, 80)]
    assert engine.params[0]["nr_passes"] == 2
    # A new size frees the features made for the old one first.
    bridge.process(rgb[:64, :64], NeuralSettings(passes=2))
    assert engine.releases == 1


def test_an_engine_of_another_abi_is_refused(tmp_path):
    bridge = NeuralBridge(tmp_path, library=FakeEngine(abi=5))
    with pytest.raises(NeuralError, match="ABI 5"):
        bridge.load()


def test_an_engine_failure_is_reported_and_the_next_call_still_goes(tmp_path):
    engine = FakeEngine(fail="feature 18 is not supported on this GPU")
    bridge = NeuralBridge(tmp_path, library=engine)
    bridge.load()
    bridge.initialize()
    rgb = np.zeros((64, 64, 3), np.float32)
    with pytest.raises(NeuralError, match="not supported"):
        bridge.process(rgb, NeuralSettings())
    engine.fail = None
    bridge.process(rgb, NeuralSettings())


@pytest.mark.parametrize("fail, delay", [("raise", 0.0), (None, 1.0),
                                         ("device removal detected", 0.0)])
def test_a_crash_or_a_hang_stops_the_engine_for_good(tmp_path, monkeypatch, fail, delay):
    monkeypatch.setattr(neural, "WATCHDOG_SECONDS", 0.2)
    engine = FakeEngine(fail=fail, delay=delay)
    bridge = NeuralBridge(tmp_path, library=engine)
    bridge.load()
    bridge.initialize()
    rgb = np.zeros((64, 64, 3), np.float32)
    with pytest.raises(NeuralPoisonedError):
        bridge.process(rgb, NeuralSettings())
    engine.fail, engine.delay = None, 0.0
    with pytest.raises(NeuralPoisonedError, match="restart"):
        bridge.process(rgb, NeuralSettings())


def test_the_service_says_why_it_cannot_run(tmp_path, monkeypatch):
    monkeypatch.setenv("REFVIEW_RESOURCES", str(tmp_path))
    service = NeuralService()
    try:
        info = service.probe().result(timeout=5)
        assert not info.available
        assert "Preferences" in info.reason
        with pytest.raises(NeuralError):
            service.submit(np.zeros((64, 64, 4), np.float32), NeuralSettings()).result(5)
    finally:
        service.shutdown()


def test_the_service_enhances_and_keeps_the_alpha(tmp_path, monkeypatch):
    monkeypatch.setenv("REFVIEW_RESOURCES", str(tmp_path))
    set_engine_dir(_install(tmp_path / "engine"))
    engine = FakeEngine()
    service = NeuralService(lambda folder: NeuralBridge(folder, library=engine))
    try:
        info = service.probe().result(timeout=5)
        assert info.available and info.engine == "Neuroframe Engine 11.0"
        display = np.full((64, 72, 4), 0.25, np.float32)
        display[..., 3] = np.linspace(0.0, 1.0, 72, dtype=np.float32)
        image, info = service.submit(display, NeuralSettings()).result(timeout=5)
        np.testing.assert_allclose(image[..., :3], 0.75, atol=1e-6)
        np.testing.assert_array_equal(image[..., 3], display[..., 3])
        assert "RTX 5070" in info.summary
    finally:
        service.shutdown()


@pytest.mark.skipif(not os.environ.get("REFVIEW_NEURAL_ENGINE"),
                    reason="REFVIEW_NEURAL_ENGINE names no Visual Enhancer folder")
def test_the_real_engine_enhances_a_picture():
    set_engine_dir(os.environ["REFVIEW_NEURAL_ENGINE"])
    service = NeuralService()
    try:
        info = service.probe().result(timeout=30)
        assert info.available, info.reason
        y, x = np.mgrid[0:256, 0:320].astype(np.float32)
        display = np.ones((256, 320, 4), np.float32)
        display[..., 0] = x / 320.0
        display[..., 1] = y / 256.0
        display[..., 2] = 0.5 + 0.4 * np.sin(x / 9.0) * np.cos(y / 7.0)
        image, info = service.submit(display, NeuralSettings()).result(timeout=240)
        assert image.shape == display.shape
        assert np.isfinite(image).all()
        assert image.min() >= 0.0 and image.max() <= 1.0
        assert np.abs(image[..., :3] - display[..., :3]).mean() > 1e-3
        print(info.summary)
    finally:
        service.shutdown()


def test_a_relative_engine_folder_is_made_absolute(tmp_path, monkeypatch):
    # Windows refuses a relative DLL directory ("The parameter is incorrect").
    monkeypatch.chdir(tmp_path)
    bridge = NeuralBridge("engine", library=FakeEngine())
    assert bridge.directory == tmp_path / "engine"
    assert bridge.directory.is_absolute()
