"""OpenGL scene renderer: background, shaded mesh, wireframe, section and paint.

Ordinary frames are one pass over the geometry.  The high-quality mode adds
three cheap ones in front of it -- a shadow map from the key light, a depth
pre-pass from the camera, and the screen-space occlusion computed from that
depth -- so the shading pass can look both up while it runs.  Nothing here
traces a ray; the point is a reference view that stays interactive while the
artist turns it.
"""

from __future__ import annotations

import math

import numpy as np
from OpenGL import GL

from ..core.annotation import Stroke
from ..core.camera import Camera, Projection
from ..core.linalg import look_at, orthographic, spherical_direction, vec3
from ..core.mesh import Mesh
from ..core.settings import RenderSettings
from . import shaders
from .framebuffer import (
    ColorTarget,
    DepthTarget,
    GeometryTarget,
    bind_default,
    current_framebuffer,
)
from .program import ShaderProgram
from .stroke_renderer import StrokeBuffers
from .texture import Texture2D, default_matcap_pixels

#: How far annotations are lifted off the surface, as a share of the scene
#: radius.  Enough to clear the depth buffer's precision at any zoom, small
#: enough that the paint still reads as sitting on the form.
_STROKE_LIFT = 0.0015
#: Additional nudge towards the viewer in NDC, for strokes seen edge-on.
_STROKE_DEPTH_BIAS = 2e-4
#: The section contour sits exactly on the cut, so it needs a larger nudge.
_CONTOUR_DEPTH_BIAS = 8e-4
#: Shadow map resolution.  2048 keeps the penumbra smooth without a
#: measurable cost next to drawing the model itself.
_SHADOW_SIZE = 2048
#: Texture units, fixed so the uniforms can be set once per frame.
_MATCAP_UNIT, _SHADOW_UNIT, _OCCLUSION_UNIT = 0, 1, 2


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

    def clear(self) -> None:
        """Forget the contents without releasing the buffer objects."""
        self._index_count = 0

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
        self._programs: dict[str, ShaderProgram] = {}
        self._buffers: MeshBuffers | None = None
        self._pedestal: MeshBuffers | None = None
        self._strokes: StrokeBuffers | None = None
        self._contour: StrokeBuffers | None = None
        self._shadow_map = DepthTarget(clamp_to_lit=True)
        self._scene_depth = GeometryTarget()
        self._occlusion = ColorTarget()
        self._occlusion_blur = ColorTarget()
        self._empty_vao = 0
        self._matcap: Texture2D | None = None

    # -- lifetime -------------------------------------------------------

    def initialize(self) -> None:
        self._programs = {
            "mesh": ShaderProgram(shaders.MESH_VERTEX, shaders.MESH_FRAGMENT, "mesh"),
            "flat": ShaderProgram(shaders.FLAT_VERTEX, shaders.FLAT_FRAGMENT, "flat"),
            "background": ShaderProgram(
                shaders.BACKGROUND_VERTEX, shaders.BACKGROUND_FRAGMENT, "background"
            ),
            "stroke": ShaderProgram(shaders.STROKE_VERTEX, shaders.STROKE_FRAGMENT, "stroke"),
            "depth": ShaderProgram(shaders.DEPTH_VERTEX, shaders.DEPTH_FRAGMENT, "depth"),
            "occlusion": ShaderProgram(
                shaders.FULLSCREEN_VERTEX, shaders.OCCLUSION_FRAGMENT, "occlusion"
            ),
            "blur": ShaderProgram(shaders.FULLSCREEN_VERTEX, shaders.BLUR_FRAGMENT, "blur"),
        }
        self._buffers = MeshBuffers()
        self._pedestal = MeshBuffers()
        self._strokes = StrokeBuffers()
        self._contour = StrokeBuffers()
        self._empty_vao = int(GL.glGenVertexArrays(1))
        self._matcap = Texture2D()
        self._matcap.upload(default_matcap_pixels())
        self._shadow_map.resize(_SHADOW_SIZE, _SHADOW_SIZE)

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_CULL_FACE)  # Reference meshes are often single-sided.

    def dispose(self) -> None:
        for program in self._programs.values():
            program.dispose()
        self._programs.clear()
        for buffers in (self._buffers, self._pedestal, self._strokes, self._contour):
            if buffers is not None:
                buffers.dispose()
        for target in (
            self._shadow_map,
            self._scene_depth,
            self._occlusion,
            self._occlusion_blur,
        ):
            target.dispose()
        if self._matcap is not None:
            self._matcap.dispose()
        if self._empty_vao:
            GL.glDeleteVertexArrays(1, [self._empty_vao])
            self._empty_vao = 0

    # -- content --------------------------------------------------------

    def set_mesh(self, mesh: Mesh | None) -> None:
        self._set_geometry(self._buffers, mesh)

    def set_pedestal(self, mesh: Mesh | None) -> None:
        """Replace the ground disc; pass ``None`` to hide it."""
        self._set_geometry(self._pedestal, mesh)

    @staticmethod
    def _set_geometry(buffers: MeshBuffers | None, mesh: Mesh | None) -> None:
        if buffers is None:
            return
        if mesh is None:
            buffers.clear()
        else:
            buffers.upload(mesh)

    def set_matcap(self, pixels: np.ndarray | None) -> None:
        if self._matcap is None:
            return
        self._matcap.upload(default_matcap_pixels() if pixels is None else pixels)

    def set_strokes(self, strokes: list[Stroke]) -> None:
        """Replace the annotation geometry; pass an empty list to hide it."""
        if self._strokes is not None:
            self._strokes.upload(strokes)

    def set_contour(self, vertices: np.ndarray) -> None:
        """Replace the section contour, prepared by the caller as stroke vertices."""
        if self._contour is not None:
            self._contour.upload_vertices(vertices)

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
        width, height = max(width, 1), max(height, 1)
        aspect = width / height
        view = camera.view_matrix()
        projection = camera.projection_matrix(aspect)
        planes = settings.section.planes()
        target = current_framebuffer()

        try:
            light_matrix = None
            if settings.shading_mode.uses_quality and self._has_geometry:
                light_matrix = self._render_shadow_map(camera, settings, planes)
                self._render_occlusion(camera, settings, projection, view, width, height, planes)
                bind_default(target)

            GL.glViewport(0, 0, width, height)
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glDepthFunc(GL.GL_LESS)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            self._draw_background(settings)

            if not self._has_geometry:
                return

            self._draw_scene(
                camera, settings, view, projection, planes, light_matrix, width, height
            )
            if settings.show_wireframe:
                self._draw_wireframe(settings, view, projection, planes)
            self._draw_contour(camera, projection @ view, settings, width, height, pixel_ratio)
            self._draw_strokes(camera, projection @ view, width, height, pixel_ratio, planes)
        finally:
            self._reset_state()

    @property
    def _has_geometry(self) -> bool:
        model = self._buffers is not None and not self._buffers.is_empty
        disc = self._pedestal is not None and not self._pedestal.is_empty
        return model or disc

    @staticmethod
    def _reset_state() -> None:
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
        for unit in (_SHADOW_UNIT, _OCCLUSION_UNIT):
            GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
            GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def _draw_background(self, settings: RenderSettings) -> None:
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDepthMask(GL.GL_FALSE)
        with self._programs["background"] as program:
            program.set_vec3("uTopColor", settings.background_top)
            program.set_vec3("uBottomColor", settings.background_bottom)
            self._draw_fullscreen()
        GL.glDepthMask(GL.GL_TRUE)
        GL.glEnable(GL.GL_DEPTH_TEST)

    def _draw_fullscreen(self) -> None:
        GL.glBindVertexArray(self._empty_vao)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
        GL.glBindVertexArray(0)

    def _draw_scene(
        self,
        camera: Camera,
        settings: RenderSettings,
        view: np.ndarray,
        projection: np.ndarray,
        planes: list,
        light_matrix: np.ndarray | None,
        width: int,
        height: int,
    ) -> None:
        """The model, the pedestal under it and the flat cap over the cut."""
        assert self._buffers is not None and self._pedestal is not None
        key_direction, fill_direction = light_directions(settings, view)

        with self._programs["mesh"] as program:
            program.set_matrix4("uView", view)
            program.set_matrix4("uProjection", projection)
            program.set_matrix3("uNormalMatrix", normal_matrix(view))
            program.set_int("uMode", settings.shading_mode.shader_id)
            program.set_bool("uFlatShading", settings.flat_shading)
            program.set_bool("uOrthographic", camera.projection is Projection.ORTHOGRAPHIC)
            _set_section(program, planes)

            matcap = settings.matcap
            program.set_int("uMatcap", _MATCAP_UNIT)
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
            program.set_vec3("uSpecularColor", surface.specular_color)
            program.set_float("uSpecularLevel", surface.specular_level)
            program.set_float("uShininess", surface.shininess)
            program.set_float("uMetalness", surface.metalness)
            program.set_float("uRoughness", surface.roughness)
            program.set_vec3("uReflectionColor", surface.reflection_color)

            self._bind_quality(program, settings, light_matrix, width, height)
            if self._matcap is not None:
                self._matcap.bind(_MATCAP_UNIT)

            program.set_vec3("uDiffuseColor", surface.diffuse_color)
            self._buffers.draw()
            if not self._pedestal.is_empty:
                program.set_vec3("uDiffuseColor", settings.pedestal.color)
                self._pedestal.draw()

        if planes and settings.section.fill_cut:
            self._draw_cap(settings, view, projection)

    def _bind_quality(
        self,
        program: ShaderProgram,
        settings: RenderSettings,
        light_matrix: np.ndarray | None,
        width: int,
        height: int,
    ) -> None:
        """Point the shading pass at the shadow map and the occlusion buffer."""
        quality = settings.quality
        shadows = light_matrix is not None and quality.show_shadows
        occlusion = settings.shading_mode.uses_quality and quality.show_occlusion
        program.set_bool("uUseShadow", shadows)
        program.set_bool("uUseOcclusion", occlusion)
        program.set_vec2("uViewportSize", (width, height))
        program.set_int("uShadowMap", _SHADOW_UNIT)
        program.set_int("uOcclusion", _OCCLUSION_UNIT)
        program.set_float("uShadowStrength", quality.shadow_strength)
        program.set_float("uShadowSoftness", quality.shadow_softness)
        program.set_float("uShadowBias", quality.shadow_bias)
        if light_matrix is not None:
            program.set_matrix4("uLightViewProjection", light_matrix)
        self._shadow_map.bind_texture(_SHADOW_UNIT)
        self._occlusion_blur.bind_texture(_OCCLUSION_UNIT)
        GL.glActiveTexture(GL.GL_TEXTURE0)

    def _draw_cap(
        self, settings: RenderSettings, view: np.ndarray, projection: np.ndarray
    ) -> None:
        """Flood the exposed interior with a flat colour so the cut reads solid.

        The surfaces visible through a cut are the model's back faces, so
        drawing just those in the cap colour fills the opening without any
        capping geometry -- and without touching the outside of the model.
        """
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glCullFace(GL.GL_FRONT)
        GL.glDepthFunc(GL.GL_LEQUAL)
        with self._programs["flat"] as program:
            program.set_matrix4("uView", view)
            program.set_matrix4("uProjection", projection)
            program.set_vec4("uColor", (*settings.section.cap_color, 1.0))
            _set_section(program, settings.section.planes())
            for buffers in self._flat_targets:
                buffers.draw()
        GL.glDepthFunc(GL.GL_LESS)
        GL.glDisable(GL.GL_CULL_FACE)

    def _draw_wireframe(
        self, settings: RenderSettings, view: np.ndarray, projection: np.ndarray, planes: list
    ) -> None:
        GL.glEnable(GL.GL_POLYGON_OFFSET_LINE)
        GL.glPolygonOffset(-1.0, -1.0)
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        with self._programs["flat"] as program:
            program.set_matrix4("uView", view)
            program.set_matrix4("uProjection", projection)
            program.set_vec4("uColor", (*settings.wireframe_color, 1.0))
            _set_section(program, planes)
            for buffers in self._flat_targets:
                buffers.draw()
        GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
        GL.glDisable(GL.GL_POLYGON_OFFSET_LINE)

    @property
    def _flat_targets(self) -> tuple[MeshBuffers, ...]:
        return tuple(b for b in (self._buffers, self._pedestal) if b is not None)

    def _draw_contour(
        self,
        camera: Camera,
        view_projection: np.ndarray,
        settings: RenderSettings,
        width: int,
        height: int,
        pixel_ratio: float,
    ) -> None:
        """The bright outline where the section plane meets the surface."""
        if self._contour is None or self._contour.is_empty:
            return
        if not (settings.section.enabled and settings.section.show_contour):
            return
        with self._programs["stroke"] as program:
            program.set_matrix4("uViewProjection", view_projection)
            program.set_vec2("uViewport", (width, height))
            program.set_float("uWidthScale", max(pixel_ratio, 0.1))
            program.set_float("uNormalOffset", camera.scene_radius * 1e-3)
            program.set_float("uDepthBias", _CONTOUR_DEPTH_BIAS)
            _set_section(program, [])  # The contour lies on the cut; never clip it.
            self._contour.draw()

    def _draw_strokes(
        self,
        camera: Camera,
        view_projection: np.ndarray,
        width: int,
        height: int,
        pixel_ratio: float,
        planes: list,
    ) -> None:
        """Draw the annotations, depth-tested against the model but not each other.

        Leaving depth writes off lets overlapping segments of the same stroke
        blend into one continuous line instead of z-fighting along the joins,
        while the mesh still hides anything painted on the far side.
        """
        if self._strokes is None or self._strokes.is_empty:
            return
        GL.glDepthMask(GL.GL_FALSE)
        with self._programs["stroke"] as program:
            program.set_matrix4("uViewProjection", view_projection)
            program.set_vec2("uViewport", (width, height))
            program.set_float("uWidthScale", max(pixel_ratio, 0.1))
            program.set_float("uNormalOffset", camera.scene_radius * _STROKE_LIFT)
            program.set_float("uDepthBias", _STROKE_DEPTH_BIAS)
            _set_section(program, planes)
            self._strokes.draw()
        GL.glDepthMask(GL.GL_TRUE)

    # -- high-quality pre-passes ----------------------------------------

    def _render_shadow_map(
        self, camera: Camera, settings: RenderSettings, planes: list
    ) -> np.ndarray | None:
        """Render scene depth from the key light and return its view-projection."""
        if not settings.quality.show_shadows or settings.light.intensity <= 0.0:
            return None
        light_matrix = light_view_projection(camera, settings)

        self._shadow_map.bind()
        GL.glClear(GL.GL_DEPTH_BUFFER_BIT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDepthFunc(GL.GL_LESS)
        # Recording only the far side of the geometry puts the stored depth
        # behind every lit surface, which is what keeps a curved form from
        # shadowing itself in stripes.  The slope-scaled offset covers the
        # thin places where front and back nearly meet.
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glCullFace(GL.GL_FRONT)
        GL.glEnable(GL.GL_POLYGON_OFFSET_FILL)
        GL.glPolygonOffset(2.0, 4.0)
        self._draw_depth(np.eye(4), light_matrix, planes)
        GL.glDisable(GL.GL_POLYGON_OFFSET_FILL)
        GL.glDisable(GL.GL_CULL_FACE)
        return light_matrix

    def _render_occlusion(
        self,
        camera: Camera,
        settings: RenderSettings,
        projection: np.ndarray,
        view: np.ndarray,
        width: int,
        height: int,
        planes: list,
    ) -> None:
        """Depth pre-pass from the camera, then occlusion and a blur over it."""
        for target in (self._scene_depth, self._occlusion, self._occlusion_blur):
            target.resize(width, height)

        self._scene_depth.bind()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glEnable(GL.GL_DEPTH_TEST)
        self._draw_depth(view, projection, planes)

        self._occlusion.bind()
        GL.glDisable(GL.GL_DEPTH_TEST)
        with self._programs["occlusion"] as program:
            program.set_int("uDepth", 0)
            program.set_int("uNormals", 1)
            program.set_matrix4("uProjection", projection)
            program.set_matrix4("uInverseProjection", np.linalg.inv(projection))
            program.set_vec2("uViewportSize", (width, height))
            program.set_float("uRadius", camera.scene_radius * settings.quality.ao_radius)
            program.set_float("uIntensity", settings.quality.ao_intensity)
            self._scene_depth.bind_texture(0)
            self._scene_depth.bind_normals(1)
            self._draw_fullscreen()

        self._occlusion_blur.bind()
        with self._programs["blur"] as program:
            program.set_int("uSource", 0)
            self._occlusion.bind_texture(0)
            self._draw_fullscreen()
        GL.glEnable(GL.GL_DEPTH_TEST)

    def _draw_depth(self, view: np.ndarray, projection: np.ndarray, planes: list) -> None:
        """Fill the bound depth buffer -- and normal buffer, if any -- with the scene."""
        with self._programs["depth"] as program:
            program.set_matrix4("uView", view)
            program.set_matrix4("uProjection", projection)
            program.set_matrix3("uNormalMatrix", normal_matrix(view))
            _set_section(program, planes)
            for buffers in self._flat_targets:
                buffers.draw()


def _set_section(program: ShaderProgram, planes: list) -> None:
    """Upload up to two clipping half-spaces; more than two are ignored."""
    program.set_int("uSectionCount", min(len(planes), 2))
    for index, plane in enumerate(planes[:2]):
        program.set_vec4(f"uSectionPlanes[{index}]", (*plane.normal, plane.offset))


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


def key_world_direction(settings: RenderSettings, view: np.ndarray) -> np.ndarray:
    """The key light's direction in world space, pointing surface -> light."""
    key = spherical_direction(settings.light.azimuth_deg, settings.light.elevation_deg)
    if settings.light.follow_camera:
        # A head lamp is defined in view space, so rotate it back out.
        return view[:3, :3].T @ key
    return key


def light_view_projection(camera: Camera, settings: RenderSettings) -> np.ndarray:
    """An orthographic camera at the key light, framing the whole scene.

    The extent is taken from the scene's bounding sphere, so the map covers the
    model wherever the view camera happens to be and the shadow does not swim
    while the artist orbits.
    """
    direction = key_world_direction(settings, camera.view_matrix())
    # A pedestal sits below the model, so allow for a little more than the
    # model's own radius before the shadow gets clipped off the map.
    radius = max(camera.scene_radius, 1e-6) * 1.6
    centre = np.asarray(camera.scene_center, dtype=np.float64)
    eye = centre + direction * radius * 2.0
    view = look_at(eye, centre, vec3(0.0, 1.0, 0.0))
    return orthographic(radius, 1.0, 0.01, radius * 4.0) @ view
