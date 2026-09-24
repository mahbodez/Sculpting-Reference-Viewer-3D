"""The path tracer's plumbing: numba, its cache, and what restarts a preview."""

from __future__ import annotations

import os
import sys

import pytest

pytest.importorskip("numba")

from refview import trace  # noqa: E402
from refview.core.path_trace import PathTraceSettings  # noqa: E402
from refview.core.settings import RenderSettings, ShadingMode  # noqa: E402
from refview.trace import jit  # noqa: E402
from refview.trace.scene import trace_settings_key  # noqa: E402


def test_numba_is_here_and_caches_in_a_folder_of_ours():
    assert trace.available() and trace.unavailable_reason() is None
    assert os.environ["NUMBA_CACHE_DIR"].endswith(jit.CACHE_DIR.name)
    assert "nnan" not in jit.FASTMATH and "ninf" not in jit.FASTMATH


def test_a_frozen_builds_cache_locator_can_be_installed(monkeypatch):
    from numba.core import caching

    impl = getattr(caching, "CacheImpl", None) or caching._CacheImpl
    monkeypatch.setattr(impl, "_locator_classes", list(impl._locator_classes))
    monkeypatch.setattr(jit, "CACHE", True)
    monkeypatch.setattr(jit, "CACHE_NOTE", None)
    jit._install_frozen_locator()
    assert jit.CACHE and jit.CACHE_NOTE is None
    frozen = impl._locator_classes[0]
    assert frozen.__name__ == "FrozenLocator"
    function = test_numba_is_here_and_caches_in_a_folder_of_ours
    # Out of a frozen build it stands aside for numba's own.
    assert frozen.from_function(function, __file__) is None
    # In one, it keys the cache on the package, not the folder it was unpacked to.
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    located = frozen.from_function(function, "C:/Temp/_MEI1234/refview/trace/integrator.py")
    assert located is not None
    assert located.get_cache_path() == str(jit.CACHE_DIR / "frozen" / "trace")


def test_importing_the_interface_does_not_load_numba():
    import subprocess

    code = ("import sys; sys.path.insert(0, 'src'); import refview.ui.main_window; "
            "print('numba' in sys.modules)")
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                         cwd=os.path.dirname(os.path.dirname(__file__)), timeout=120)
    assert out.stdout.strip().endswith("False"), out.stderr


def test_the_preview_restarts_for_what_it_shows_and_nothing_else():
    render = RenderSettings(shading_mode=ShadingMode.PBR)
    trace_settings = PathTraceSettings()
    key = trace_settings_key(render, trace_settings)
    # Framing, colour and the denoiser do not change the light in the film.
    trace_settings.safe_frame.show = True
    trace_settings.output.width = 123
    trace_settings.color.exposure = 2.0
    trace_settings.denoise.mix = 0.5
    render.grid.ground = not render.grid.ground
    render.show_wireframe = True
    assert trace_settings_key(render, trace_settings) == key
    # The material, the light and the bounces do.
    render.surface.roughness = 0.9
    assert trace_settings_key(render, trace_settings) != key
    key = trace_settings_key(render, trace_settings)
    render.light.azimuth_deg += 10.0
    assert trace_settings_key(render, trace_settings) != key
    key = trace_settings_key(render, trace_settings)
    trace_settings.paths.max_bounces = 3
    assert trace_settings_key(render, trace_settings) != key
