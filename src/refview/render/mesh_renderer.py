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
from ..core.plane_axes import Coefficients, PlaneAxes, PlaneSet
from ..core.plane_clusters import fit_planes
from ..core.settings import PlaneMode, RenderSettings
from . import shaders
from .framebuffer import (
    AccumTarget,
    ColorTarget,
    DepthTarget,
    GeometryTarget,
    bind_default,
    current_framebuffer,
)
from .program import ShaderProgram
from .stroke_renderer import StrokeBuffers
from .texture import DataTexture, Texture2D, default_matcap_pixels

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
_MATCAP_UNIT, _SHADOW_UNIT, _OCCLUSION_UNIT, _PLANE_UNIT = 0, 1, 2, 3
#: The two the ghost's sums are read back through, used by the resolve pass only.
_GHOST_ACCUM_UNIT, _GHOST_REVEAL_UNIT = 4, 5

#: How many fits to keep alongside the one in use.  Each is a mode and a set of
#: coefficients, so dragging a coefficient slider leaves a trail of them; a
#: handful is enough to make going back to a setting just tried instant without
#: holding a fit for every number the slider passed through.
_PLANE_CACHE_SIZE = 8


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
        #: The planar stand-in drawn in place of the model, when the artist has
        #: asked for the form itself to be broken into planes.  Empty the rest
        #: of the time, and never anything the model is measured or picked
        #: against -- see :mod:`refview.core.plane_solids`.
        self._sculpt: MeshBuffers | None = None
        self._pedestal: MeshBuffers | None = None
        self._strokes: StrokeBuffers | None = None
        self._contour: StrokeBuffers | None = None
        self._shadow_map = DepthTarget(clamp_to_lit=True)
        self._scene_depth = GeometryTarget()
        self._occlusion = ColorTarget()
        self._occlusion_blur = ColorTarget()
        #: Where a see-through model is summed, then resolved over the frame.
        self._ghost = AccumTarget()
        self._empty_vao = 0
        self._matcap: Texture2D | None = None
        self._mesh: Mesh | None = None
        #: Worked out the first frame a fitted mode actually asks for it, so
        #: loading a model costs nothing until the artist turns one on, and
        #: kept per mode and per set of coefficients so that going back to a
        #: setting already tried is instant.
        self._plane_axes: dict[tuple[PlaneMode, Coefficients], PlaneAxes] = {}
        #: The table the shader reads the planes out of, and the level it was
        #: last filled from -- uploading it again every frame would be work
        #: done for nothing, since it only changes when the slider does.
        self._plane_table: DataTexture | None = None
        self._plane_table_level: PlaneSet | None = None

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
            "ghost": ShaderProgram(shaders.FULLSCREEN_VERTEX, shaders.GHOST_FRAGMENT, "ghost"),
        }
        self._buffers = MeshBuffers()
        self._sculpt = MeshBuffers()
        self._pedestal = MeshBuffers()
        self._strokes = StrokeBuffers()
        self._contour = StrokeBuffers()
        self._empty_vao = int(GL.glGenVertexArrays(1))
        self._matcap = Texture2D()
        self._matcap.upload(default_matcap_pixels())
        self._plane_table = DataTexture()
        self._shadow_map.resize(_SHADOW_SIZE, _SHADOW_SIZE)

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_CULL_FACE)  # Reference meshes are often single-sided.

    def dispose(self) -> None:
        for program in self._programs.values():
            program.dispose()
        self._programs.clear()
        for buffers in (
            self._buffers,
            self._sculpt,
            self._pedestal,
            self._strokes,
            self._contour,
        ):
            if buffers is not None:
                buffers.dispose()
        for target in (
            self._shadow_map,
            self._scene_depth,
            self._occlusion,
            self._occlusion_blur,
            self._ghost,
        ):
            target.dispose()
        if self._matcap is not None:
            self._matcap.dispose()
        if self._plane_table is not None:
            self._plane_table.dispose()
            self._plane_table = None
            self._plane_table_level = None
        if self._empty_vao:
            GL.glDeleteVertexArrays(1, [self._empty_vao])
            self._empty_vao = 0

    # -- content --------------------------------------------------------

    def set_mesh(self, mesh: Mesh | None) -> None:
        self._set_geometry(self._buffers, mesh)
        # Any stand-in in hand was built out of the model being replaced, so
        # it goes now rather than being drawn for the frames until a new one
        # arrives.
        self._set_geometry(self._sculpt, None)
        self._mesh = mesh
        self._plane_axes.clear()

    def set_sculpt(self, mesh: Mesh | None) -> None:
        """Draw ``mesh`` in place of the model; pass ``None`` to draw the model.

        The stand-in stands in everywhere the model is drawn -- the shading
        pass, the shadow map, the depth pre-pass the occlusion is read off,
        the wireframe -- because a form that is faceted to the eye and round
        to its own shadow is not a form anyone could work from.
        """
        self._set_geometry(self._sculpt, mesh)

    def set_pedestal(self, mesh: Mesh | None) -> None:
        """Replace the ground disc; pass ``None`` to hide it."""
        self._set_geometry(self._pedestal, mesh)

    @property
    def _model(self) -> MeshBuffers | None:
        """Whichever geometry is standing for the model this frame."""
        if self._sculpt is not None and not self._sculpt.is_empty:
            return self._sculpt
        return self._buffers

    def _planes_for(self, mode: PlaneMode, coefficients: Coefficients, count: int) -> PlaneSet:
        """The model's own planes under ``mode``, fitted once and kept."""
        key = (mode, coefficients)
        fitted = self._plane_axes.get(key)
        if fitted is None:
            if len(self._plane_axes) >= _PLANE_CACHE_SIZE:
                # Plain insertion order: the fit dropped is the one least
                # recently arrived at, which on a slider drag is the furthest
                # back along it.
                del self._plane_axes[next(iter(self._plane_axes))]
            fitted = self._plane_axes[key] = fit_planes(self._mesh, mode, coefficients)
        return fitted.for_count(count)

    def _upload_planes(self, program: ShaderProgram, planes: PlaneSet) -> None:
        """Fill the shader's table with a level, if it is not already in it."""
        if self._plane_table is None:
            return
        program.set_int("uPlaneTable", _PLANE_UNIT)
        if self._plane_table_level is not planes:
            table = np.zeros((2, max(len(planes), 1), 4), dtype=np.float32)
            table[0, : len(planes), :3] = planes.directions
            table[0, : len(planes), 3] = planes.offsets
            table[1, : len(planes), :3] = planes.anchors
            self._plane_table.upload(table)
            self._plane_table_level = planes
        self._plane_table.bind(_PLANE_UNIT)

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
            if self._ghost_opacity(settings) is not None:
                # Sized here, with the other offscreen targets, because
                # allocating one binds both a framebuffer and a texture.  Doing
                # it inside the shading pass would take the widget's own
                # framebuffer out from under that pass and the matcap off its
                # texture unit -- so the first frame at each new size would come
                # out unlike every frame after it.
                self._ghost.resize(width, height)
                bind_default(target)

            GL.glViewport(0, 0, width, height)
            GL.glEnable(GL.GL_DEPTH_TEST)
            GL.glDepthFunc(GL.GL_LESS)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            self._draw_background(settings)

            if not self._has_geometry:
                return

            self._draw_scene(
                camera, settings, view, projection, planes, light_matrix, width, height,
                pixel_ratio,
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

    def _ghost_opacity(self, settings: RenderSettings) -> float | None:
        """How see-through the model is this frame, or ``None`` if it is solid.

        Asked in two places -- where the buffers are allocated and where they
        are filled -- and the two must agree, or a frame allocates nothing and
        then draws into it.
        """
        model = self._model
        opacity = settings.surface_opacity
        if model is None or model.is_empty or opacity >= 1.0:
            return None
        return opacity

    def _accumulate_ghost(
        self,
        program: ShaderProgram,
        model: MeshBuffers,
        camera: Camera,
        opacity: float,
        width: int,
        height: int,
    ) -> None:
        """Sum a see-through model into the ghost buffers, to be resolved after.

        Blending is not commutative, so a ghost drawn straight into the frame
        comes out in whatever order the triangles happen to sit in the buffer
        -- a haze at a low opacity, and at a high one a form visibly shattered,
        with the back of the skull painted over the face.

        What used to stand here was two culled draws, back faces then front,
        on the reading that a closed form puts exactly two surfaces under any
        one pixel.  It does not.  Look along an arm held across a chest and
        there are four, and the two passes cannot order them: both backs land
        in the first draw and both fronts in the second, whichever is actually
        nearer.  The shading comes apart exactly where the form folds over
        itself, which is where an artist is looking.

        So the fragments are not ordered at all.  Each is summed instead --
        colours averaged by how far through the form they lie, transmittances
        multiplied as a sum of logarithms -- and :meth:`_resolve_ghost` divides
        the one by the other.  Addition does not care what order it happens in,
        so the answer is the same from every angle and for any number of
        surfaces.  One draw call over the geometry, where there were two.

        Depth writes stay off, as they were: the form must not hide its own far
        side, and the passes that follow are drawn as though it were not there.
        """
        frame = current_framebuffer()
        self._ghost.bind()
        self._ghost.clear()

        # The ground the model stands behind still has to hide it, and this
        # framebuffer has a depth buffer of its own, so the disc is laid in
        # again with the colour writes shut off.
        if self._pedestal is not None and not self._pedestal.is_empty:
            GL.glColorMask(GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE)
            self._pedestal.draw()
            GL.glColorMask(GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE)

        near, span = _ghost_depth_range(camera)
        program.set_float("uGhostNear", near)
        program.set_float("uGhostSpan", span)
        program.set_float("uOpacity", opacity)
        program.set_bool("uAccumulate", True)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_ONE, GL.GL_ONE)
        GL.glDepthMask(GL.GL_FALSE)
        model.draw()
        GL.glDepthMask(GL.GL_TRUE)
        GL.glDisable(GL.GL_BLEND)
        program.set_bool("uAccumulate", False)
        program.set_float("uOpacity", 1.0)

        bind_default(frame)
        GL.glViewport(0, 0, width, height)

    def _resolve_ghost(self) -> None:
        """Lay the summed ghost over the scene already in the frame."""
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDepthMask(GL.GL_FALSE)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        with self._programs["ghost"] as program:
            program.set_int("uAccum", _GHOST_ACCUM_UNIT)
            program.set_int("uReveal", _GHOST_REVEAL_UNIT)
            self._ghost.bind_texture(_GHOST_ACCUM_UNIT)
            self._ghost.bind_reveal(_GHOST_REVEAL_UNIT)
            GL.glActiveTexture(GL.GL_TEXTURE0)
            self._draw_fullscreen()
        GL.glDisable(GL.GL_BLEND)
        GL.glDepthMask(GL.GL_TRUE)
        GL.glEnable(GL.GL_DEPTH_TEST)

    @staticmethod
    def _reset_state() -> None:
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_BLEND)
        GL.glDepthMask(GL.GL_TRUE)
        GL.glDisable(GL.GL_CULL_FACE)
        GL.glBindVertexArray(0)
        GL.glUseProgram(0)
        for unit in (_SHADOW_UNIT, _OCCLUSION_UNIT, _GHOST_ACCUM_UNIT, _GHOST_REVEAL_UNIT):
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
        pixel_ratio: float = 1.0,
    ) -> None:
        """The model, the pedestal under it and the flat cap over the cut."""
        assert self._buffers is not None and self._pedestal is not None
        key_direction, fill_direction = light_directions(settings, view)

        model = self._model
        ghost_opacity = self._ghost_opacity(settings)

        with self._programs["mesh"] as program:
            program.set_matrix4("uView", view)
            program.set_matrix4("uProjection", projection)
            program.set_matrix3("uNormalMatrix", normal_matrix(view))
            program.set_int("uMode", settings.shading_mode.shader_id)
            program.set_bool("uFlatShading", settings.flat_shading)
            plane_settings = settings.planes
            # A form already rebuilt out of flats has nothing left for the
            # normal quantiser to round, so the two targets never run together.
            shades = plane_settings.shades_normals
            program.set_bool("uPlaneShading", shades)
            program.set_int("uPlaneMode", plane_settings.mode.shader_id)
            program.set_float("uPlaneCellSize", plane_settings.cell_size)
            program.set_bool("uPlaneContour", plane_settings.show_contour)
            program.set_vec3("uPlaneContourColor", plane_settings.contour_color)
            program.set_float(
                "uPlaneContourWidth", plane_settings.contour_width * max(pixel_ratio, 0.1)
            )
            fitted = PlaneSet.empty()
            if shades and plane_settings.mode.fitted:
                fitted = self._planes_for(
                    plane_settings.mode, plane_settings.coefficients, plane_settings.axis_count
                )
                self._upload_planes(program, fitted)
                program.set_vec3("uPlaneOrigin", fitted.origin)
                program.set_float("uPlaneScale", fitted.scale)
            program.set_int("uPlaneAxisCount", len(fitted))
            program.set_float("uPlaneLocality", fitted.locality)
            program.set_float("uPlaneCoplanar", fitted.coplanarity)
            program.set_float("uPlaneSpan", math.radians(plane_settings.axis_span_deg))
            program.set_bool("uOrthographic", camera.projection is Projection.ORTHOGRAPHIC)
            program.set_bool("uAccumulate", False)
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

            # The ground goes down before the form standing on it.  A ghost is
            # blended, and blending only composites over what is already
            # there; the other way round the disc would paint over the legs in
            # front of it, since a ghost leaves no depth to be tested against.
            # With both solid the two orders cannot be told apart, so this is
            # not worth a branch.
            if not self._pedestal.is_empty:
                program.set_vec3("uDiffuseColor", settings.pedestal.color)
                # A fitted set of planes describes the model, not the ground
                # it stands on, so the disc would snap to whichever of them
                # happened to lie nearest its own up.  Leaving it out keeps it
                # reading as the flat plate the grid mode also makes of it.
                if len(fitted):
                    program.set_bool("uPlaneShading", False)
                self._pedestal.draw()
                program.set_bool("uPlaneShading", shades)
            if model is not None:
                program.set_vec3("uDiffuseColor", surface.diffuse_color)
                if ghost_opacity is not None:
                    self._accumulate_ghost(program, model, camera, ghost_opacity, width, height)
                else:
                    program.set_float("uOpacity", 1.0)
                    model.draw()

        # After the program has been let go, since this is a pass of its own --
        # and before the cap, which belongs over the ghost as it did before.
        if ghost_opacity is not None:
            self._resolve_ghost()

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
        return tuple(b for b in (self._model, self._pedestal) if b is not None)

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


def _ghost_depth_range(camera: Camera) -> tuple[float, float]:
    """Where the form starts along the view, and how deep it is.

    The ghost weighs a fragment by how far through the form it lies, which only
    means anything against the form's own depth.  The scene's bounding sphere
    gives it: near the eye side of the sphere, a span of its diameter, under
    either projection, since view-space depth is measured from the eye both
    times.
    """
    radius = max(float(camera.scene_radius), 1e-6)
    distance = float(np.linalg.norm(camera.eye - camera.scene_center))
    return max(distance - radius, 0.0), 2.0 * radius


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
