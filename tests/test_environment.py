"""HDRIs: reading them, what is made of them, the light rig, and lighting with them on the GPU."""

from __future__ import annotations

import math

import numpy as np
import pytest

from refview.core.environment import (
    EnvironmentLoadError,
    direction_to_uv,
    dominant_light,
    evaluate_sh,
    irradiance_sh,
    load_environment,
    prepare_environment,
    read_radiance,
    rotation_y,
    sampling_tables,
    uv_to_direction,
)
from refview.core.linalg import spherical_direction
from refview.core.session import Session
from refview.core.settings import LightingMode, LightSettings, RenderSettings, ShadingMode
from refview.render.environment import environment_matrix, light_rig


def _rgbe(pixels: np.ndarray) -> np.ndarray:
    """Encode linear RGB as Radiance's shared-exponent bytes."""
    brightest = pixels.max(axis=-1)
    mantissa, exponent = np.frexp(brightest)
    scale = np.where(brightest > 1e-32, mantissa * 256.0 / np.maximum(brightest, 1e-32), 0.0)
    out = np.zeros(pixels.shape[:2] + (4,), np.uint8)
    out[..., :3] = np.clip(pixels * scale[..., None], 0, 255).astype(np.uint8)
    out[..., 3] = np.where(brightest > 1e-32, exponent + 128, 0)
    return out


def _write_hdr(path, pixels: np.ndarray, compressed: bool) -> None:
    height, width = pixels.shape[:2]
    rgbe = _rgbe(pixels)
    body = bytearray()
    for row in rgbe:
        if not compressed:
            body += row.tobytes()
            continue
        body += bytes([2, 2, width >> 8, width & 0xFF])
        for channel in range(4):
            values = row[:, channel]
            x = 0
            while x < width:
                # A run where the next few bytes repeat, a dump otherwise.
                run = 1
                while x + run < width and run < 127 and values[x + run] == values[x]:
                    run += 1
                if run >= 4:
                    body += bytes([128 + run, int(values[x])])
                    x += run
                else:
                    count = min(128, width - x)
                    body += bytes([count]) + values[x:x + count].tobytes()
                    x += count
    header = b"#?RADIANCE\nFORMAT=32-bit_rle_rgbe\n\n" + f"-Y {height} +X {width}\n".encode()
    path.write_bytes(header + bytes(body))


def _panorama(height: int = 32, width: int = 64) -> np.ndarray:
    """A dim room with one bright window, above and in front."""
    u = (np.arange(width) + 0.5) / width
    v = (np.arange(height) + 0.5) / height
    directions = uv_to_direction(*np.meshgrid(u, v))
    window = np.clip(directions @ np.array([0.0, 0.6, -0.8]), 0.0, 1.0) ** 40
    pixels = 0.2 + 30.0 * window[..., None] * np.array([1.0, 0.9, 0.8])
    return pixels.astype(np.float32)


@pytest.mark.parametrize("compressed", [False, True])
def test_radiance_hdr_reads_back_what_was_written(tmp_path, compressed):
    pixels = _panorama()
    path = tmp_path / "room.hdr"
    _write_hdr(path, pixels, compressed)
    read = read_radiance(path)
    assert read.shape == pixels.shape and read.dtype == np.float32
    # RGBE keeps eight bits of mantissa against the brightest channel.
    np.testing.assert_allclose(read, pixels, rtol=0.02, atol=0.01)


def test_unreadable_files_say_so(tmp_path):
    with pytest.raises(EnvironmentLoadError, match="not an HDRI"):
        read_radiance(tmp_path / "picture.png")
    bad = tmp_path / "broken.hdr"
    bad.write_bytes(b"not a radiance file")
    with pytest.raises(EnvironmentLoadError):
        read_radiance(bad)
    with pytest.raises(EnvironmentLoadError):
        read_radiance(tmp_path / "missing.hdr")


def test_directions_and_panorama_coordinates_round_trip():
    rng = np.random.default_rng(1)
    uv = rng.uniform(0.01, 0.99, size=(200, 2))
    directions = uv_to_direction(uv[:, 0], uv[:, 1])
    np.testing.assert_allclose(np.linalg.norm(directions, axis=1), 1.0, atol=1e-12)
    np.testing.assert_allclose(direction_to_uv(directions), uv, atol=1e-9)
    # The centre of the picture looks down -z, and its top row straight up.
    np.testing.assert_allclose(uv_to_direction(0.5, 0.5), [0.0, 0.0, -1.0], atol=1e-12)
    np.testing.assert_allclose(uv_to_direction(0.3, 0.0), [0.0, 1.0, 0.0], atol=1e-12)


def test_harmonic_irradiance_matches_a_brute_force_sum():
    pixels = _panorama(64, 128)
    sh = irradiance_sh(pixels)
    height, width = pixels.shape[:2]
    u, v = (np.arange(width) + 0.5) / width, (np.arange(height) + 0.5) / height
    directions = uv_to_direction(*np.meshgrid(u, v))
    solid = (2 * math.pi / width) * (math.pi / height) * np.sin(v * math.pi)

    def brute(normal):
        cosine = np.maximum(directions @ np.array(normal, float), 0.0)
        return (pixels * (cosine * solid[:, None])[..., None]).sum(axis=(0, 1))

    peak = brute([0.0, 0.6, -0.8]).max()
    for normal in ([0, 0.6, -0.8], [0, 1, 0], [0, 0, -1], [1, 0, 0], [0, -1, 0]):
        # Three bands cannot hold a sharp window exactly; they hold the
        # irradiance it makes to within a few percent of the brightest.
        error = np.abs(evaluate_sh(sh, np.array(normal, float)) - brute(normal)).max()
        assert error < 0.08 * peak


def test_a_uniform_sky_lights_every_way_alike():
    sky = np.full((32, 64, 3), 0.5, np.float32)
    sh = irradiance_sh(sky)
    for normal in ([0, 1, 0], [0, -1, 0], [1, 0, 0], [0, 0, 1]):
        irradiance = evaluate_sh(sh, np.array(normal, float))
        np.testing.assert_allclose(irradiance, 0.5 * math.pi, rtol=0.02)
    direction, color = dominant_light(sh)
    assert np.all(color < 0.05)   # nothing to cast a shadow from


def test_the_dominant_light_points_at_the_window():
    environment = prepare_environment(_panorama(64, 128))
    window = np.array([0.0, 0.6, -0.8])
    assert float(environment.sun_direction @ window) > 0.95
    assert np.all(environment.sun_color > 0.0)
    facing = evaluate_sh(environment.sh, environment.sun_direction)
    assert np.all(environment.sun_color <= facing + 1e-6)
    assert environment.peak == pytest.approx(
        float(np.maximum(facing, 0) @ np.array([0.2126, 0.7152, 0.0722])), rel=1e-5
    )
    assert environment.normalization == pytest.approx(1.0 / environment.peak)


def test_sampling_tables_are_distributions_and_find_the_light():
    tables = sampling_tables(_panorama(64, 128))
    h, w = tables.density.shape
    assert tables.marginal[0] == 0.0 and tables.marginal[-1] == 1.0
    assert np.all(np.diff(tables.marginal) >= 0.0)
    assert np.all(tables.conditional[:, 0] == 0.0) and np.all(tables.conditional[:, -1] == 1.0)
    assert np.all(np.diff(tables.conditional, axis=1) >= -1e-7)
    # A density over the unit square integrates to one.
    assert tables.density.mean() == pytest.approx(1.0, rel=1e-4)
    # Most of the picks land on the window, though it is a sliver of the sphere.
    row = np.argmax(tables.density.sum(axis=1))
    direction = uv_to_direction(0.5, (row + 0.5) / h)
    assert direction[1] > 0.2
    texels, cdf = tables.packed()
    assert texels.shape == (h, w, 4) and cdf.shape == (h + 1, w + 1, 4)
    np.testing.assert_array_equal(cdf[h, : h + 1, 0], tables.marginal)


def test_prepared_maps_are_sanitised_and_sized_for_the_card():
    pixels = _panorama(512, 4096)
    pixels[0, 0] = np.nan
    pixels[1, 1] = np.inf
    pixels[2, 2] = -5.0
    environment = prepare_environment(pixels, "room.exr")
    assert environment.radiance.shape == (1024, 2048, 3)
    assert np.all(np.isfinite(environment.radiance)) and environment.radiance.min() >= 0.0
    assert environment.radiance.max() <= 65000.0
    assert environment.name == "room"


def test_the_bundled_hdri_loads_when_it_is_there():
    from refview.paths import available_environments

    bundled = available_environments()
    if not bundled:
        pytest.skip("No bundled HDRI in this checkout")
    environment = load_environment(bundled[0])
    assert environment.radiance.shape[1] == 2 * environment.radiance.shape[0]
    assert environment.peak > 0.0


def test_turning_the_lights_turns_the_key_and_the_map_together():
    light = LightSettings(azimuth_deg=170.0, environment_rotation_deg=-170.0, elevation_deg=80.0)
    light.turned(20.0, 15.0)
    assert light.azimuth_deg == pytest.approx(-170.0)
    assert light.environment_rotation_deg == pytest.approx(-150.0)
    assert light.elevation_deg == 90.0
    # The same number of degrees turns the key and the map the same way.
    key = spherical_direction(0.0, 0.0)
    np.testing.assert_allclose(rotation_y(30.0) @ key, spherical_direction(30.0, 0.0), atol=1e-12)


def test_the_rig_says_what_lights_the_model():
    environment = prepare_environment(_panorama(64, 128))
    view = np.eye(4)
    settings = RenderSettings(shading_mode=ShadingMode.PBR)

    studio = light_rig(settings, view, environment)
    assert not studio.environment and studio.key_intensity == settings.light.intensity
    np.testing.assert_allclose(studio.shadow, spherical_direction(40.0, 35.0))

    settings.light.mode = LightingMode.ENVIRONMENT
    lit = light_rig(settings, view, environment)
    assert lit.environment and lit.key_intensity == lit.fill_intensity == 0.0
    assert lit.ambient_intensity == 0.0 and lit.env_shadow
    # The shadow is cast from the window, in the world.
    np.testing.assert_allclose(lit.shadow, environment.sun_direction, atol=1e-6)
    assert lit.env_scale == pytest.approx(environment.normalization)

    settings.light.mode = LightingMode.BOTH
    both = light_rig(settings, view, environment)
    assert both.environment and both.key_intensity > 0.0 and not both.env_shadow

    # A map not yet read leaves the studio lights on rather than the model dark.
    settings.light.mode = LightingMode.ENVIRONMENT
    waiting = light_rig(settings, view, None)
    assert not waiting.environment and waiting.key_intensity > 0.0

    # A matcap carries its own light.
    settings.shading_mode = ShadingMode.MATCAP
    assert not light_rig(settings, view, environment).environment


def test_a_map_that_follows_the_camera_turns_with_the_view():
    settings = RenderSettings()
    turn = np.eye(4)
    turn[:3, :3] = rotation_y(90.0)
    settings.light.follow_camera = False
    np.testing.assert_allclose(environment_matrix(settings, turn), np.eye(3), atol=1e-12)
    settings.light.follow_camera = True
    np.testing.assert_allclose(environment_matrix(settings, turn), rotation_y(90.0), atol=1e-12)
    settings.light.environment_rotation_deg = 90.0
    np.testing.assert_allclose(environment_matrix(settings, turn), np.eye(3), atol=1e-12)


def test_sessions_keep_the_hdri_and_old_ones_light_as_before():
    session = Session()
    light = session.render.light
    light.mode = LightingMode.BOTH
    light.environment_path = "C:/maps/room.exr"
    light.environment_rotation_deg = 45.0
    light.environment_strength = 1.5
    light.environment_background = True
    restored = Session.from_dict(session.to_dict()).render.light
    assert restored == light
    old = session.to_dict()
    for name in ("mode", "environment_path", "environment_rotation_deg"):
        del old["render"]["light"][name]
    before = Session.from_dict(old).render.light
    assert before.mode is LightingMode.STUDIO and before.environment_path is None


# -- on the GPU ----------------------------------------------------------------


@pytest.fixture(scope="module")
def gl_context():
    from OpenGL import GL
    from PySide6.QtGui import QOffscreenSurface, QOpenGLContext, QSurfaceFormat
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    ctx = QOpenGLContext()
    ctx.setFormat(fmt)
    if not ctx.create():
        pytest.skip("No OpenGL context on this test host")
    surface = QOffscreenSurface()
    surface.setFormat(ctx.format())
    surface.create()
    if not ctx.makeCurrent(surface):
        pytest.skip("No offscreen OpenGL surface on this test host")
    yield GL
    ctx.doneCurrent()
    app.processEvents()


def test_every_lit_mode_takes_the_hdri_and_the_background_shows_it(gl_context):
    from refview.core.camera import Camera
    from refview.core.mesh import Mesh
    from refview.render.framebuffer import FrameTarget
    from refview.render.mesh_renderer import SceneRenderer

    gl = gl_context
    axis = np.linspace(-1.0, 1.0, 12, dtype=np.float32)
    x, y = np.meshgrid(axis, axis)
    positions = np.stack([x, y, np.zeros_like(x)], -1).reshape(-1, 3)
    index = np.arange(144).reshape(12, 12)
    quads = np.stack([index[:-1, :-1], index[1:, :-1], index[1:, 1:], index[:-1, 1:]], -1)
    indices = np.concatenate([quads[..., [0, 1, 2]], quads[..., [0, 2, 3]]]).reshape(-1, 3)
    mesh = Mesh(positions, np.tile([0, 0, 1], (144, 1)).astype(np.float32), indices)
    renderer = SceneRenderer()
    renderer.initialize()
    renderer.set_mesh(mesh)
    camera = Camera()
    camera.frame(mesh.bounds)
    target = FrameTarget()
    target.resize(96, 96)
    settings = RenderSettings()
    settings.skin.progressive = False

    def render():
        target.bind()
        renderer.render(camera, settings, 96, 96)
        pixels = np.asarray(gl.glReadPixels(0, 0, 96, 96, gl.GL_RGBA, gl.GL_FLOAT))
        assert np.all(np.isfinite(pixels)) and gl.glGetError() == gl.GL_NO_ERROR
        return pixels[..., :3]

    try:
        renderer.set_environment(prepare_environment(_panorama(64, 128)))
        for mode in (ShadingMode.LAMBERT, ShadingMode.PHONG, ShadingMode.BLINN_PHONG,
                     ShadingMode.PBR, ShadingMode.HIGH_QUALITY, ShadingMode.HUMAN_SKIN):
            settings.shading_mode = mode
            settings.light.mode = LightingMode.STUDIO
            studio = render()
            settings.light.mode = LightingMode.ENVIRONMENT
            lit = render()
            centre = (slice(36, 60), slice(36, 60))
            assert not np.allclose(lit[centre], studio[centre], atol=1e-3), mode
            assert lit[centre].mean() > 0.02, mode
            # Turning the map moves the light on the plate.
            settings.light.environment_rotation_deg = 180.0
            turned = render()
            settings.light.environment_rotation_deg = 0.0
            assert not np.allclose(turned[centre], lit[centre], atol=1e-3), mode
        # The background is the gradient until it is asked to be the map.
        settings.shading_mode = ShadingMode.LAMBERT
        corner = (slice(0, 6), slice(0, 6))
        gradient = render()[corner]
        settings.light.environment_background = True
        assert not np.allclose(render()[corner], gradient, atol=1e-3)
    finally:
        renderer.dispose()
        target.dispose()
