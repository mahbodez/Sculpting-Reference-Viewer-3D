"""Human Skin in the path tracer: the port of the shader, and its light."""

from __future__ import annotations

import math

import numpy as np
import pytest

pytest.importorskip("numba")

from refview.core.body_regions import BodyRegionSettings  # noqa: E402
from refview.core.path_trace import PathTraceSettings  # noqa: E402
from refview.core.settings import LightingMode, RenderSettings, ShadingMode  # noqa: E402
from refview.core.skin import SKIN_RANGES, SkinSettings  # noqa: E402
from refview.trace.job import RenderJob  # noqa: E402
from refview.trace.scene import (  # noqa: E402
    PartKind,
    SceneCache,
    TraceInputs,
    TracePart,
    compile_scene,
)
from refview.trace.skin import hash4, skin_parameters, spot  # noqa: E402
from trace_scenes import constant_sky, looking_at_origin, sphere  # noqa: E402

F32 = np.float32


def _glsl_hash4(cx, cy, cz):
    """skinHash4 written out in numpy single precision, from the GLSL."""
    p4 = np.array([cx, cy, cz, cx], F32) * np.array([0.1031, 0.1030, 0.0973, 0.1099], F32)
    p4 = p4 - np.floor(p4)
    wzxy = p4[[3, 2, 0, 1]]
    p4 = p4 + F32(np.dot(p4, wzxy + F32(33.33)))
    a = p4[[0, 0, 1, 2]] + p4[[1, 2, 2, 3]]
    b = p4[[2, 1, 3, 0]]
    r = a * b
    return r - np.floor(r)


def test_the_spot_hash_is_the_shaders():
    rng = np.random.default_rng(0)
    for cx, cy, cz in rng.integers(-500, 500, size=(200, 3)):
        ours = np.array(hash4(float(cx), float(cy), float(cz)))
        # Single precision in another order: a spot lands within a hundredth of a cell.
        np.testing.assert_allclose(ours, _glsl_hash4(cx, cy, cz), atol=1e-2)


def test_a_spot_covers_its_centre_and_not_its_cell_corner():
    # Density one: every cell has a spot.
    cover, _kind, _away, t = spot(10.5, 20.5, 1.0, 1.0, 0.25, 0.1)
    assert t < 1.5
    cover_corner, *_ = spot(10.001, 20.001, 1.0, 1.0, 0.25, 0.1)
    assert cover_corner == 0.0
    assert spot(10.5, 20.5, 1.0, 0.0, 0.25, 0.1)[0] == 0.0


def test_parameters_scale_with_the_scene():
    skin = SkinSettings()
    small, _ = skin_parameters(skin, 1.0)
    large, regions = skin_parameters(skin, 10.0)
    assert large[10] == pytest.approx(small[10] * 10.0)   # radius
    assert large[13] == pytest.approx(small[13] * 10.0)   # pore size
    assert regions.shape == (7, 8)
    assert np.allclose(regions[:, 7], 0.0)
    assert np.allclose(regions[:, :7], [BodyRegionSettings().multipliers(e) for e in (
        "acne", "nevi", "freckles", "blemishes", "oil", "blood", "veins")])


def _skin_render(skin: SkinSettings, env=None, samples=16, size=(40, 40), distance=4.0,
                 mode=LightingMode.STUDIO):
    render = RenderSettings(shading_mode=ShadingMode.HUMAN_SKIN, skin=skin)
    render.light.mode = mode
    trace = PathTraceSettings()
    trace.sampling.samples = samples
    trace.sampling.noise_threshold = 0.0
    inputs = TraceInputs(parts=(TracePart(sphere(32), PartKind.MODEL),),
                         camera=looking_at_origin(distance), width=size[0], height=size[1],
                         render=render, path_trace=trace, environment=env)
    job = RenderJob(compile_scene(inputs, SceneCache()), trace, threads=4)
    job.run()
    return job.film.beauty()


def test_every_knob_at_its_top_stays_finite():
    skin = SkinSettings()
    for name, (_low, high) in SKIN_RANGES.items():
        if name in ("samples", "resolution"):
            continue
        setattr(skin, name, high)
    beauty = _skin_render(skin.bounded(), env=constant_sky(), samples=8)
    assert np.isfinite(beauty).all()
    assert beauty[..., :3].max() > 0.0


def test_scattered_light_is_not_more_than_arrived():
    """A white, fully scattering, shineless skin under a uniform sky reflects at most the sky."""
    skin = SkinSettings(color=(1.0, 1.0, 1.0), scatter_color=(1.0, 1.0, 1.0), sss=1.0,
                        specular=0.0, fuzz=0.0, transmission=0.0, detail=0.0, mottle=0.0,
                        blood=0.0, veins=0.0)
    beauty = _skin_render(skin, env=constant_sky(), samples=64, mode=LightingMode.ENVIRONMENT)
    covered = beauty[..., 3] > 0.999
    # The skin is physical: a uniform sky of strength one has radiance 1/pi.
    radiance = beauty[covered, :3].mean()
    assert radiance <= 1.03 / math.pi
    assert radiance > 0.8 / math.pi


def test_a_thin_slab_lets_more_backlight_through_than_a_thick_one():
    """Lit from straight behind, a thin shell glows and a thick ball does not."""
    skin = SkinSettings(transmission=1.0, sss=1.0, radius=0.05, specular=0.0, fuzz=0.0)
    results = []
    for radius in (0.05, 1.0):
        render = RenderSettings(shading_mode=ShadingMode.HUMAN_SKIN, skin=skin)
        render.light.follow_camera = True
        # The key straight behind the model, as seen from the camera.
        render.light.azimuth_deg = 180.0
        render.light.elevation_deg = 0.0
        render.light.fill_intensity = 0.0
        render.light.ambient_intensity = 0.0
        trace = PathTraceSettings()
        trace.sampling.samples = 32
        trace.sampling.noise_threshold = 0.0
        # A flat ball, a disc facing the camera, radius thick.
        mesh = sphere(24)
        mesh = type(mesh)(positions=mesh.positions * np.array([1.0, 1.0, radius], np.float32),
                          normals=mesh.normals, indices=mesh.indices)
        camera = looking_at_origin()
        inputs = TraceInputs(parts=(TracePart(mesh, PartKind.MODEL),), camera=camera, width=24,
                             height=24, render=render, path_trace=trace)
        job = RenderJob(compile_scene(inputs, SceneCache()), trace, threads=4)
        job.run()
        results.append(job.film.beauty()[10:14, 10:14, :3].mean())
    thin, thick = results
    assert thin > thick * 2.0
