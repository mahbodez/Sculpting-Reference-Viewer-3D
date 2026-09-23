"""Real GL tests; skipped only when the test host cannot create a GL context."""

from __future__ import annotations

import time

import numpy as np
import pytest

from refview.core.camera import Camera
from refview.core.mesh import Mesh
from refview.core.settings import RenderSettings, ShadingMode
from refview.render import shaders
from refview.render.framebuffer import FrameTarget
from refview.render.mesh_renderer import SceneRenderer
from refview.render.program import ShaderProgram
from refview.render.skin_bvh import build_scene, table_width, texture_table
from refview.render.skin_detail import relief_volume
from refview.render.texture import DataTexture, Texture3D


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


def triangle():
    return Mesh(np.array([[-1, -1, 0], [1, -1, 0], [0, 1, 0]], np.float32),
                np.tile([0, 0, 1], (3, 1)), [[0, 1, 2]])


class _Tables:
    """A scene's three tracer tables on the card, bound where a test program reads them."""

    def __init__(self, scene) -> None:
        self.scene = scene
        self.textures = [DataTexture(), DataTexture(), DataTexture()]
        for texture, table in zip(
            self.textures, (scene.nodes, scene.triangles, scene.attributes), strict=True
        ):
            texture.upload(texture_table(table, 4096))

    def bind(self, program) -> None:
        for unit, (texture, name) in enumerate(
            zip(self.textures, ("uSkinNodes", "uSkinTriangles", "uSkinAttributes"), strict=True)
        ):
            texture.bind(6 + unit)
            program.set_int(name, 6 + unit)
        program.set_int("uSkinNodeCount", len(self.scene.nodes))
        program.set_int("uSkinTableShift", table_width(4096).bit_length() - 1)

    def dispose(self) -> None:
        for texture in self.textures:
            texture.dispose()


def _ray_program(body: str) -> ShaderProgram:
    fragment = shaders.MESH_TRACE_FRAGMENT[
        :shaders.MESH_TRACE_FRAGMENT.rindex("void main() {")
    ] + body
    return ShaderProgram(shaders.FULLSCREEN_VERTEX, fragment, "skin ray test")


def test_gpu_bvh_nearest_hit_miss_and_section_clip(gl_context):
    gl = gl_context
    tables = _Tables(build_scene([(triangle(), 0, (0.7, 0.5, 0.4))]))
    program = _ray_program("""
uniform vec3 testOrigin;
void main() {
    SkinHit hit;
    bool found = skinRay(testOrigin, vec3(0,0,-1), 10.0, hit);
    fragColor = found ? vec4(hit.distance,hit.normal.z,hit.material,1) : vec4(-1);
    fragReveal = vec4(0);
}
""")
    target = FrameTarget(floating=True)
    target.resize(1, 1)
    vao = int(gl.glGenVertexArrays(1))
    try:
        target.bind()
        gl.glDisable(gl.GL_DEPTH_TEST)
        with program:
            tables.bind(program)
            program.set_float("uSkinEpsilon", 1e-5)
            program.set_int("uSectionCount", 0)
            gl.glBindVertexArray(vao)

            def trace(origin):
                program.set_vec3("testOrigin", origin)
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
                return np.asarray(gl.glReadPixels(0, 0, 1, 1, gl.GL_RGBA, gl.GL_FLOAT)).ravel()

            np.testing.assert_allclose(trace((0, 0, 2)), [2, 1, 0, 1], atol=1e-5)
            np.testing.assert_allclose(trace((2, 0, 2)), [-1]*4)
            program.set_int("uSectionCount", 1)
            program.set_vec4("uSectionPlanes[0]", (0, 0, 1, -0.1))
            np.testing.assert_allclose(trace((0, 0, 2)), [-1]*4)
    finally:
        gl.glBindVertexArray(0)
        gl.glDeleteVertexArrays(1, [vao])
        for resource in (program, target, tables):
            resource.dispose()


def test_gpu_traversal_agrees_with_brute_force_on_a_soup(gl_context):
    """Nearest hits and shadow rays through a deep tree, pixel by pixel, against numpy."""
    gl = gl_context
    rng = np.random.default_rng(4)
    count = 600
    centres = rng.normal(size=(count, 1, 3))
    corners = (centres + rng.normal(scale=0.15, size=(count, 3, 3))).reshape(-1, 3)
    soup = Mesh(corners.astype(np.float32), np.tile([0, 0, 1], (3 * count, 1)),
                np.arange(3 * count).reshape(-1, 3))
    tables = _Tables(build_scene([(soup, 0, (0.7, 0.5, 0.4))]))
    size = 32
    program = _ray_program("""
uniform vec3 testOrigin;
void main() {
    vec2 grid = gl_FragCoord.xy / 32.0 * 2.0 - 1.0;
    vec3 ray = normalize(vec3(grid * 0.6, -1.0));
    SkinHit hit;
    bool found = skinRay(testOrigin, ray, 1e30, hit);
    float open = skinVisible(testOrigin, vec3(0.0), ray);
    fragColor = vec4(found ? hit.distance : -1.0, open, 0.0, 1.0);
    fragReveal = vec4(0);
}
""")
    target = FrameTarget(floating=True)
    target.resize(size, size)
    vao = int(gl.glGenVertexArrays(1))
    origin = np.array([0.0, 0.0, 6.0])
    try:
        target.bind()
        gl.glDisable(gl.GL_DEPTH_TEST)
        with program:
            tables.bind(program)
            program.set_float("uSkinEpsilon", 1e-6)
            program.set_int("uSectionCount", 0)
            program.set_vec3("testOrigin", origin)
            gl.glBindVertexArray(vao)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
            pixels = np.asarray(
                gl.glReadPixels(0, 0, size, size, gl.GL_RGBA, gl.GL_FLOAT)
            ).reshape(size, size, 4)
    finally:
        gl.glBindVertexArray(0)
        gl.glDeleteVertexArrays(1, [vao])
        for resource in (program, target, tables):
            resource.dispose()

    p = corners.reshape(-1, 3, 3).astype(np.float64)
    e1, e2 = p[:, 1] - p[:, 0], p[:, 2] - p[:, 0]
    grid = (np.arange(size) + 0.5) / size * 2.0 - 1.0
    hits = 0
    for row in range(size):
        for column in range(size):
            ray = np.array([grid[column] * 0.6, grid[row] * 0.6, -1.0])
            ray /= np.linalg.norm(ray)
            q = np.cross(ray, e2)
            det = (e1 * q).sum(1)
            s = origin - p[:, 0]
            with np.errstate(all="ignore"):
                u = (s * q).sum(1) / det
                v = (np.cross(s, e1) @ ray) / det
                t = (e2 * np.cross(s, e1)).sum(1) / det
            ok = (np.abs(det) > 1e-12) & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 1e-6)
            nearest, open_ = pixels[row, column, :2]
            if ok.any():
                hits += 1
                assert nearest == pytest.approx(t[ok].min(), rel=1e-4)
                assert open_ == 0.0
            else:
                assert nearest == -1.0 and open_ == 1.0
    assert hits > 100   # the soup is in the way of plenty of rays, and misses plenty


def test_relief_volume_samples_seamlessly_on_the_gpu(gl_context):
    """The tile wraps: the slope read just past the edge equals the one at the start."""
    gl = gl_context
    volume = relief_volume(size=16, cells=2, seed=5)
    texture = Texture3D()
    texture.upload(volume)
    program = ShaderProgram(shaders.FULLSCREEN_VERTEX, """
#version 330 core
out vec4 fragColor;
uniform sampler3D uVolume;
uniform vec3 testCoord;
void main() { fragColor = textureLod(uVolume, testCoord, 0.0); }
""", "relief test")
    target = FrameTarget(floating=True)
    target.resize(1, 1)
    vao = int(gl.glGenVertexArrays(1))
    try:
        target.bind()
        gl.glDisable(gl.GL_DEPTH_TEST)
        with program:
            texture.bind(8)
            program.set_int("uVolume", 8)
            gl.glBindVertexArray(vao)

            def fetch(coord):
                program.set_vec3("testCoord", coord)
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
                return np.asarray(gl.glReadPixels(0, 0, 1, 1, gl.GL_RGBA, gl.GL_FLOAT)).ravel()

            centre = (0.5 + 3) / 16
            np.testing.assert_allclose(fetch((centre, centre, centre)), volume[3, 3, 3], atol=2e-3)
            np.testing.assert_allclose(fetch((centre + 1.0, centre - 2.0, centre)),
                                       fetch((centre, centre, centre)), atol=2e-3)
    finally:
        gl.glBindVertexArray(0)
        gl.glDeleteVertexArrays(1, [vao])
        for resource in (program, target, texture):
            resource.dispose()


def test_relief_and_flush_change_the_shaded_image(gl_context):
    gl = gl_context
    renderer = SceneRenderer()
    renderer.initialize()
    # A dense patch seen close up, so a pore spans many pixels and the relief
    # is well inside its fade-out footprint.
    axis = np.linspace(-1.0, 1.0, 24, dtype=np.float32)
    x, y = np.meshgrid(axis, axis)
    positions = np.stack([x, y, np.zeros_like(x)], -1).reshape(-1, 3)
    index = np.arange(24 * 24).reshape(24, 24)
    quads = np.stack([index[:-1, :-1], index[1:, :-1], index[1:, 1:], index[:-1, 1:]], -1)
    indices = np.concatenate([quads[..., [0, 1, 2]], quads[..., [0, 2, 3]]]).reshape(-1, 3)
    mesh = Mesh(positions, np.tile([0, 0, 1], (len(positions), 1)).astype(np.float32), indices)
    renderer.set_mesh(mesh)
    camera = Camera()
    camera.frame(mesh.bounds)
    camera.eye = camera.target + (camera.eye - camera.target) * 0.25
    settings = RenderSettings(shading_mode=ShadingMode.HUMAN_SKIN)
    settings.skin.progressive = False
    target = FrameTarget()
    target.resize(192, 192)

    def render(**skin):
        for name, value in skin.items():
            setattr(settings.skin, name, value)
        target.bind()
        renderer.render(camera, settings, 192, 192)
        pixels = np.asarray(gl.glReadPixels(0, 0, 192, 192, gl.GL_RGBA, gl.GL_FLOAT))[..., :3]
        assert np.all(np.isfinite(pixels)) and gl.glGetError() == gl.GL_NO_ERROR
        return pixels[48:144, 48:144]

    try:
        smooth = render(detail=0.0, mottle=0.0, blood=0.0, pore_size=0.03)
        bumped = render(detail=1.5)
        # Pores break up a flat plane; compare luminance so channel differences do not count.
        assert bumped.mean(-1).std() > smooth.mean(-1).std() + 0.01
        flushed = render(detail=0.0, blood=1.0)
        red_shift = (flushed[..., 0] - flushed[..., 2]).mean() - (smooth[..., 0] - smooth[..., 2]).mean()
        assert red_shift > 0.005
    finally:
        renderer.dispose()
        target.dispose()


def test_render_refinement_resets_stops_and_other_modes_work(gl_context):
    gl = gl_context
    renderer = SceneRenderer()
    renderer.initialize()
    mesh = triangle()
    renderer.set_mesh(mesh)
    camera = Camera()
    camera.frame(mesh.bounds)
    settings = RenderSettings(shading_mode=ShadingMode.HUMAN_SKIN)
    settings.skin.samples = 8
    target = FrameTarget()
    target.resize(64, 64)

    def render(**kwargs):
        target.bind()
        renderer.render(camera, settings, 64, 64, **kwargs)
        pixels = np.asarray(gl.glReadPixels(0, 0, 64, 64, gl.GL_RGBA, gl.GL_FLOAT))
        assert np.all(np.isfinite(pixels))
        assert gl.glGetError() == gl.GL_NO_ERROR
        return pixels

    try:
        for mode in ShadingMode:
            settings.shading_mode = mode
            render()
        settings.shading_mode = ShadingMode.HUMAN_SKIN
        start = time.monotonic()
        while renderer.skin.clock.samples < 8 and time.monotonic() - start < 10:
            render(refine=True)
        assert renderer.skin.clock.samples == 8
        assert not renderer.skin.needs_frame
        before = render(refine=True)
        after = render(refine=True)
        np.testing.assert_array_equal(before, after)
        render(refine=True, interactive=True)
        assert renderer.skin.clock.samples == 0
        assert not renderer.skin.tracing
        settings.skin.color = (0.3, 0.2, 0.1)
        render(refine=True)
        assert renderer.skin.clock.samples == 0
        settings.ghost = True
        render(refine=True)
        assert not renderer.skin.needs_frame
        assert not renderer.skin.tracing
        renderer.set_mesh(None)
        render(refine=True)
        assert gl.glGetError() == gl.GL_NO_ERROR
    finally:
        renderer.dispose()
        target.dispose()


def _patch(size: int = 24) -> Mesh:
    axis = np.linspace(-1.0, 1.0, size, dtype=np.float32)
    x, y = np.meshgrid(axis, axis)
    positions = np.stack([x, y, np.zeros_like(x)], -1).reshape(-1, 3)
    index = np.arange(size * size).reshape(size, size)
    quads = np.stack([index[:-1, :-1], index[1:, :-1], index[1:, 1:], index[:-1, 1:]], -1)
    indices = np.concatenate([quads[..., [0, 1, 2]], quads[..., [0, 2, 3]]]).reshape(-1, 3)
    return Mesh(positions, np.tile([0, 0, 1], (len(positions), 1)).astype(np.float32), indices)


def test_marks_fall_on_the_skin_and_the_body_map_says_where(gl_context):
    """Moles and acne darken and redden a patch; a map that gives the patch none takes them off."""
    from refview.core.body_regions import BodySource, RegionSource

    gl = gl_context
    renderer = SceneRenderer()
    renderer.initialize()
    mesh = _patch()
    renderer.set_mesh(mesh)
    camera = Camera()
    camera.frame(mesh.bounds)
    camera.eye = camera.target + (camera.eye - camera.target) * 0.25
    settings = RenderSettings(shading_mode=ShadingMode.HUMAN_SKIN)
    settings.skin.progressive = False
    settings.skin.detail = 0.0
    settings.skin.mottle = 0.0
    settings.skin.blood = 0.0
    settings.skin.pore_size = 0.02
    target = FrameTarget()
    target.resize(192, 192)

    def render(**skin):
        for name, value in skin.items():
            setattr(settings.skin, name, value)
        target.bind()
        renderer.render(camera, settings, 192, 192)
        pixels = np.asarray(gl.glReadPixels(0, 0, 192, 192, gl.GL_RGBA, gl.GL_FLOAT))[..., :3]
        assert np.all(np.isfinite(pixels)) and gl.glGetError() == gl.GL_NO_ERROR
        return pixels[48:144, 48:144]

    try:
        clear = render(nevi=0.0, acne=0.0, freckles=0.0, blemishes=0.0)
        marked = render(nevi=1.0, acne=1.0, freckles=1.0)
        # Spots break up a flat, evenly lit plane.
        assert marked.mean(-1).std() > clear.mean(-1).std() + 0.01
        # Blemishes are patches many pores across, so the pores are made
        # small enough for a few patches to fall in the view.
        plain = render(nevi=0.0, acne=0.0, freckles=0.0, blemishes=0.0, pore_size=0.003)
        blotched = render(blemishes=1.0)
        assert not np.allclose(blotched, plain, atol=1e-3)
        render(blemishes=0.0, pore_size=0.02)

        # The whole patch is "feet", where the profile gives no acne and no
        # freckles at all and few moles; with the map on, the marks thin out.
        settings.skin.regions.source = RegionSource.WHOLE
        settings.skin.regions.whole = "feet"
        settings.skin.regions.feet.acne = 0.0
        settings.skin.regions.feet.nevi = 0.0
        settings.skin.regions.feet.freckles = 0.0
        key = ("test", 1)
        renderer.set_body(BodySource(parts=(mesh,), bones=np.zeros((0, 7)),
                                     source=RegionSource.WHOLE, whole=6, key=key))
        # The map is built off the thread: render until it lands.
        for _ in range(200):
            mapped = render(nevi=1.0, acne=1.0, freckles=1.0, blemishes=0.0)
            if renderer.skin.body_on:
                break
            time.sleep(0.02)
        assert renderer.skin.body_on and renderer.skin.body_pending is None
        mapped = render()
        assert mapped.mean(-1).std() < marked.mean(-1).std() - 0.005
        np.testing.assert_allclose(mapped, clear, atol=0.02)
        # Turning the region up again brings them back without a new map.
        settings.skin.regions.feet.acne = 1.0
        settings.skin.regions.feet.nevi = 1.0
        settings.skin.regions.feet.freckles = 1.0
        again = render()
        assert renderer.skin.body_pending is None
        np.testing.assert_allclose(again, marked, atol=0.02)
        renderer.set_body(None)
        render()
        assert not renderer.skin.body_on
    finally:
        renderer.dispose()
        target.dispose()
