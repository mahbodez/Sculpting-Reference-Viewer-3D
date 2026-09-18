"""Real GL: several objects drawn at their own solidity, and the grid under them."""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.camera import Camera
from refview.core.grid import GridSettings, build_grid
from refview.core.mesh import Mesh
from refview.core.settings import RenderSettings, ShadingMode
from refview.render.framebuffer import FrameTarget
from refview.render.mesh_renderer import SceneRenderer


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


def _square(x: float, size: float = 0.8, z: float = 0.5) -> Mesh:
    """A square facing the camera, standing a little in front of the grid's wall."""
    positions = np.array(
        [[x - size, -size, z], [x + size, -size, z], [x + size, size, z], [x - size, size, z]],
        dtype=np.float32,
    )
    normals = np.tile([0, 0, 1], (4, 1)).astype(np.float32)
    return Mesh(positions, normals, [[0, 1, 2], [0, 2, 3]])


def test_objects_are_drawn_at_their_own_solidity_over_the_grid(gl_context):
    gl = gl_context
    renderer = SceneRenderer()
    renderer.initialize()
    left, right = _square(-1.0), _square(1.0)
    camera = Camera()
    camera.eye = np.array([0.0, 0.0, 6.0])
    camera.target = np.zeros(3)
    camera.scene_radius = 2.5
    settings = RenderSettings(shading_mode=ShadingMode.LAMBERT)
    settings.grid = GridSettings(ground=False, front=True, count=10, spacing=0.25, fade=0.0,
                                 opacity=1.0, at_floor=False)
    size = 128
    target = FrameTarget()
    target.resize(size, size)

    def render() -> np.ndarray:
        target.bind()
        renderer.render(camera, settings, size, size)
        pixels = np.asarray(gl.glReadPixels(0, 0, size, size, gl.GL_RGBA, gl.GL_FLOAT))[..., :3]
        assert np.all(np.isfinite(pixels)) and gl.glGetError() == gl.GL_NO_ERROR
        return pixels

    try:
        renderer.set_mesh(None, [])
        plain = render()
        lines = build_grid(settings.grid, None, camera.scene_radius)
        renderer.set_grid(lines)
        # No model, yet the grid is there: the frame is not the plain gradient.
        assert not np.allclose(render(), plain, atol=1e-3)

        renderer.set_mesh(None, [(left, 1.0), (right, 1.0)])
        solid = render()
        renderer.set_part_opacities([1.0, 0.3])
        ghosted = render()
        # The left square is untouched; the right one let the background through.
        left_patch = (slice(size // 2 - 8, size // 2 + 8), slice(size // 4 - 8, size // 4 + 8))
        right_patch = (
            slice(size // 2 - 8, size // 2 + 8),
            slice(3 * size // 4 - 8, 3 * size // 4 + 8),
        )
        assert np.allclose(solid[left_patch], ghosted[left_patch], atol=1e-3)
        assert not np.allclose(solid[right_patch], ghosted[right_patch], atol=1e-2)

        # Fewer parts than before leaves no stale object behind.
        renderer.set_mesh(None, [(left, 1.0)])
        alone = render()
        assert np.allclose(alone[left_patch], solid[left_patch], atol=1e-3)
        assert not np.allclose(alone[right_patch], solid[right_patch], atol=1e-2)

        # The grid is depth-tested against the objects and drawn where they are not.
        renderer.set_grid(None)
        bare = render()
        assert np.allclose(bare[left_patch], alone[left_patch], atol=1e-3)
        renderer.set_grid(lines)
        assert not np.allclose(render(), bare, atol=1e-3)
    finally:
        renderer.dispose()
        target.dispose()


def test_a_highlighted_object_wears_a_line_round_it_and_only_it(gl_context):
    gl = gl_context
    renderer = SceneRenderer()
    renderer.initialize()
    left, right = _square(-1.0), _square(1.0)
    camera = Camera()
    camera.eye = np.array([0.0, 0.0, 6.0])
    camera.target = np.zeros(3)
    camera.scene_radius = 2.5
    settings = RenderSettings(shading_mode=ShadingMode.LAMBERT)
    settings.grid = GridSettings(ground=False, front=False)
    size = 128
    target = FrameTarget()
    target.resize(size, size)
    amber = (1.0, 0.77, 0.36)

    def render() -> np.ndarray:
        target.bind()
        renderer.render(camera, settings, size, size)
        pixels = np.asarray(gl.glReadPixels(0, 0, size, size, gl.GL_RGBA, gl.GL_FLOAT))[..., :3]
        assert np.all(np.isfinite(pixels)) and gl.glGetError() == gl.GL_NO_ERROR
        return pixels

    try:
        renderer.set_mesh(None, [(left, 1.0), (right, 1.0)])
        plain = render()
        renderer.set_highlight(1, 1.0, amber)
        lit = render()
        # Somewhere the frame turned amber, and the squares themselves did not.
        changed = np.abs(lit - plain).sum(axis=-1) > 0.05
        assert changed.any()
        tinted = lit[changed]
        assert np.all(tinted[:, 0] > tinted[:, 2])  # Red above blue: the line's colour.
        centre = (slice(size // 2 - 4, size // 2 + 4), slice(3 * size // 4 - 4, 3 * size // 4 + 4))
        assert np.allclose(lit[centre], plain[centre], atol=1e-3)
        # The line sits round the highlighted square and not round the other.
        columns = np.where(changed.any(axis=0))[0]
        assert columns.min() > size // 2
        # Half solid is half the tint; nought is none at all.
        renderer.set_highlight(1, 0.5, amber)
        half = render()
        assert np.abs(half - plain).sum() < np.abs(lit - plain).sum()
        assert np.abs(half - plain).sum() > 0.0
        renderer.set_highlight(None)
        assert np.allclose(render(), plain, atol=1e-3)
        # An index past the parts is nothing to draw, not a crash.
        renderer.set_highlight(7, 1.0, amber)
        assert np.allclose(render(), plain, atol=1e-3)
    finally:
        renderer.dispose()
        target.dispose()
