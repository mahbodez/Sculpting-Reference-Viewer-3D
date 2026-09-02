"""OpenGL scene renderer: background gradient, shaded mesh and wireframe."""

from __future__ import annotations

import math

import numpy as np
from OpenGL import GL

from ..core.annotation import Stroke
from ..core.camera import Camera, Projection
from ..core.linalg import spherical_direction
from ..core.mesh import Mesh
from ..core.settings import RenderSettings
from . import shaders
from .program import ShaderProgram
from .stroke_renderer import StrokeBuffers
from .texture import Texture2D, default_matcap_pixels

#: How far annotations are lifted off the surface, as a share of the scene
#: radius.  Enough to clear the depth buffer's precision at any zoom, small
#: enough that the paint still reads as sitting on the form.
_STROKE_LIFT = 0.0015
#: Additional nudge towards the viewer in NDC, for strokes seen edge-on.
_STROKE_DEPTH_BIAS = 2e-4


class MeshBuffers:
    """Vertex/index buffers for one mesh, bound through a single VAO."""

    def __init__(self) -> None:
        self._vao = int(GL.glGenVertexArrays(1))
        self._position_vbo = int(GL.glGenBuffers(1))
        self._normal_vbo = int(GL.glGenBuffers(1))
        self._ebo = int(GL.glGenBuffers(1))
        self._index_count = 0

    def upload(self, mesh: Mesh) -> None:
        GL.glBindVertexArray(self._vao)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._position_vbo)
        GL.glBufferData(
            GL.GL_ARRAY_BUFFER, mesh.positions.nbytes, mesh.positions, GL.GL_STATIC_DRAW
        )
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._normal_vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, mesh.normals.nbytes, mesh.normals, GL.GL_STATIC_DRAW)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self._ebo)
        GL.glBufferData(
            GL.GL_ELEMENT_ARRAY_BUFFER, mesh.indices.nbytes, mesh.indices, GL.GL_STATIC_DRAW
        )
        self._index_count = mesh.indices.size

        GL.glBindVertexArray(0)

    @property
    def is_empty(self) -> bool:
        return self._index_count == 0

    def draw(self) -> None:
        if self.is_empty:
            return
        GL.glBindVertexArray(self._vao)
        GL.glDrawElements(GL.GL_TRIANGLES, self._index_count, GL.GL_UNSIGNED_INT, None)
        GL.glBindVertexArray(0)

    def dispose(self) -> None:
        GL.glDeleteBuffers(3, [self._position_vbo, self._normal_vbo, self._ebo])
        GL.glDeleteVertexArrays(1, [self._vao])
        self._index_count = 0


class SceneRenderer:
    """Owns every GL resource the viewport needs.

    The widget calls :meth:`initialize` once a context exists, feeds it a mesh
    and a matcap, then calls :meth:`render` per frame.  Keeping all GL state
    here means the Qt widget stays free of graphics detail.
    """

    def __init__(self) -> None:
        self._mesh_program: ShaderProgram | None = None
        self._flat_program: ShaderProgram | None = None
        self._background_program: ShaderProgram | None = None
        self._stroke_program: ShaderProgram | None = None
        self._buffers: MeshBuffers | None = None
        self._strokes: StrokeBuffers | None = None
        self._empty_vao = 0
        self._matcap: Texture2D | None = None

    # -- lifetime -------------------------------------------------------

    def initialize(self) -> None:
        self._mesh_program = ShaderProgram(shaders.MESH_VERTEX, shaders.MESH_FRAGMENT, "mesh")
        self._flat_program = ShaderProgram(shaders.FLAT_VERTEX, shaders.FLAT_FRAGMENT, "flat")
        self._background_program = ShaderProgram(
            shaders.BACKGROUND_VERTEX, shaders.BACKGROUND_FRAGMENT, "background"
        )
        self._stroke_program = ShaderProgram(
            shaders.STROKE_VERTEX, shaders.STROKE_FRAGMENT, "stroke"
        )
        self._buffers = MeshBuffers()
        self._strokes = StrokeBuffers()
        self._empty_vao = int(GL.glGenVertexArrays(1))
        self._matcap = Texture2D()
        self._matcap.upload(default_matcap_pixels())

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_CULL_FACE)  # Reference meshes are often single-sided.

    def dispose(self) -> None:
        for resource in (
            self._mesh_program,
            self._flat_program,
            self._background_program,
            self._stroke_program,
        ):
            if resource is not None:
                resource.dispose()
        for buffers in (self._buffers, self._strokes):
            if buffers is not None:
                buffers.dispose()
        if self._matcap is not None:
            self._matcap.dispose()
        if self._empty_vao:
            GL.glDeleteVertexArrays(1, [self._empty_vao])
            self._empty_vao = 0

    # -- content --------------------------------------------------------

    def set_mesh(self, mesh: Mesh | None) -> None:
        if self._buffers is None:
            return
        if mesh is None:
            self._buffers.dispose()
            self._buffers = MeshBuffers()
        else:
            self._buffers.upload(mesh)

    def set_matcap(self, pixels: np.ndarray | None) -> None:
        if self._matcap is None:
            return
        self._matcap.upload(default_matcap_pixels() if pixels is None else pixels)

    def set_strokes(self, strokes: list[Stroke]) -> None:
        """Replace the annotation geometry; pass an empty list to hide it."""
        if self._strokes is not None:
            self._strokes.upload(strokes)

    # -- drawing --------------------------------------------------------

    def render(
        self,
        camera: Camera,
        settings: RenderSettings,
        width: int,
        height: int,
        pixel_ratio: float = 1.0,
    ) -> None:
        """Draw one frame, then hand a neutral GL state back to the caller.

        ``width``/``height`` are in device pixels; ``pixel_ratio`` converts the
        logical pixel sizes coming from the UI into the same units.

        The widget paints its 2D overlay with QPainter straight afterwards, and
        Qt's paint engine assumes depth testing is off and nothing is bound --
        leaving the scene's state behind silently swallows strokes and text.
        """
        try:
            GL.glViewport(0, 0, max(width, 1), max(height, 1))
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glDepthFunc(GL.GL_LESS)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            self._draw_background(settings)

            if self._buffers is None or self._buffers.is_empty:
                return

            aspect = max(width, 1) / max(height, 1)
            view = camera.view_matrix()
            projection = camera.projection_matrix(aspect)

            self._draw_mesh(camera, settings, view, projection)
            if settings.show_wireframe:
                self._draw_wireframe(settings, view, projection)
            self._draw_strokes(camera, projection @ view, width, height, pixel_ratio)
        finally:
            self._reset_state()

    @staticmethod
    def _reset_state() -> None:
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def _draw_background(self, settings: RenderSettings) -> None:
        assert self._background_program is not None
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDepthMask(GL.GL_FALSE)
        with self._background_program as program:
            program.set_vec3("uTopColor", settings.background_top)
            program.set_vec3("uBottomColor", settings.background_bottom)
            GL.glBindVertexArray(self._empty_vao)
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
            GL.glBindVertexArray(0)
        GL.glDepthMask(GL.GL_TRUE)
        GL.glEnable(GL.GL_DEPTH_TEST)

    def _draw_mesh(
        self,
        camera: Camera,
        settings: RenderSettings,
        view: np.ndarray,
        projection: np.ndarray,
    ) -> None:
        assert self._mesh_program is not None and self._buffers is not None
        key_direction, fill_direction = light_directions(settings, view)

        with self._mesh_program as program:
            program.set_matrix4("uView", view)
            program.set_matrix4("uProjection", projection)
            program.set_matrix3("uNormalMatrix", normal_matrix(view))
            program.set_int("uMode", settings.shading_mode.shader_id)
            program.set_bool("uFlatShading", settings.flat_shading)
            program.set_bool("uOrthographic", camera.projection is Projection.ORTHOGRAPHIC)

            matcap = settings.matcap
            program.set_int("uMatcap", 0)
            program.set_float("uMatcapRotation", math.radians(matcap.rotation_deg))
            program.set_float("uMatcapContrast", matcap.contrast)
            program.set_float("uMatcapGamma", matcap.gamma)
            program.set_float("uMatcapBrightness", matcap.brightness)
            program.set_float("uMatcapSaturation", matcap.saturation)
            program.set_vec3("uMatcapTint", matcap.tint)
            program.set_bool("uMatcapFlipY", matcap.flip_y)

            light = settings.light
            program.set_vec3("uKeyDirection", key_direction)
            program.set_vec3("uFillDirection", fill_direction)
            program.set_vec3("uLightColor", light.color)
            program.set_float("uKeyIntensity", light.intensity)
            program.set_float("uFillIntensity", light.fill_intensity)
            program.set_vec3("uAmbientColor", light.ambient_color)
            program.set_float("uAmbientIntensity", light.ambient_intensity)

            surface = settings.surface
            program.set_vec3("uDiffuseColor", surface.diffuse_color)
            program.set_vec3("uSpecularColor", surface.specular_color)
            program.set_float("uSpecularLevel", surface.specular_level)
            program.set_float("uShininess", surface.shininess)
            program.set_float("uMetalness", surface.metalness)
            program.set_float("uRoughness", surface.roughness)
            program.set_vec3("uReflectionColor", surface.reflection_color)

            if self._matcap is not None:
                self._matcap.bind(0)
            self._buffers.draw()

    def _draw_wireframe(
        self, settings: RenderSettings, view: np.ndarray, projection: np.ndarray
    ) -> None:
        assert self._flat_program is not None and self._buffers is not None
        GL.glEnable(GL.GL_POLYGON_OFFSET_LINE)
        GL.glPolygonOffset(-1.0, -1.0)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        with self._flat_program as program:
            program.set_matrix4("uView", view)
            program.set_matrix4("uProjection", projection)
            program.set_vec4("uColor", (*settings.wireframe_color, 1.0))
            self._buffers.draw()
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glDisable(GL.GL_POLYGON_OFFSET_LINE)

    def _draw_strokes(
        self,
        camera: Camera,
        view_projection: np.ndarray,
        width: int,
        height: int,
        pixel_ratio: float,
    ) -> None:
        """Draw the annotations, depth-tested against the model but not each other.

        Leaving depth writes off lets overlapping segments of the same stroke
        blend into one continuous line instead of z-fighting along the joins,
        while the mesh still hides anything painted on the far side.
        """
        if self._strokes is None or self._strokes.is_empty or self._stroke_program is None:
            return
        GL.glDepthMask(GL.GL_FALSE)
        with self._stroke_program as program:
            program.set_matrix4("uViewProjection", view_projection)
            program.set_vec2("uViewport", (max(width, 1), max(height, 1)))
            program.set_float("uWidthScale", max(pixel_ratio, 0.1))
            program.set_float("uNormalOffset", camera.scene_radius * _STROKE_LIFT)
            program.set_float("uDepthBias", _STROKE_DEPTH_BIAS)
            self._strokes.draw()
        GL.glDepthMask(GL.GL_TRUE)


def normal_matrix(view: np.ndarray) -> np.ndarray:
    """Inverse-transpose of the view rotation, for transforming normals."""
    return np.linalg.inv(view[:3, :3]).T


def light_directions(settings: RenderSettings, view: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Key and fill directions in view space, pointing surface -> light.

    With ``follow_camera`` the angles are interpreted directly in view space,
    which makes the light behave like a head lamp; otherwise they describe a
    fixed world direction that the object turns within.
    """
    light = settings.light
    key = spherical_direction(light.azimuth_deg, light.elevation_deg)
    fill = spherical_direction(light.azimuth_deg + 180.0, light.elevation_deg * 0.35 - 10.0)
    if not light.follow_camera:
        rotation = view[:3, :3]
        key = rotation @ key
        fill = rotation @ fill
    return key, fill
