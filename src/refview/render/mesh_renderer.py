"""OpenGL scene renderer: background, shaded mesh, wireframe, section and paint.

Ordinary frames are one pass over the geometry.  The high-quality mode adds
three cheap ones in front of it -- a shadow map from the key light, a depth
pre-pass from the camera, and the screen-space occlusion computed from that
depth -- so the shading pass can look both up while it runs. Human Skin adds
progressive BVH ray tracing while the camera rests.
"""

from __future__ import annotations

import math

import numpy as np
from OpenGL import GL

from ..core.annotation import Stroke
from ..core.camera import Camera, Projection
from ..core.grid import GridSettings
from ..core.linalg import look_at, orthographic, spherical_direction, vec3
from ..core.mesh import Mesh
from ..core.plane_axes import Coefficients, PlaneAxes, PlaneSet
from ..core.plane_clusters import fit_planes
from ..core.settings import CONTOUR_DENSITY_MIN, PlaneMode, RenderSettings, ShadingMode
from . import shaders
from .framebuffer import (
    AccumTarget,
    ColorTarget,
    DepthTarget,
    FrameTarget,
    GeometryTarget,
    bind_default,
    current_framebuffer,
)
from .program import ShaderProgram
from .skin_refinement import (
    DIFFUSION_UNIT,
    NODES_UNIT,
    RELIEF_UNIT,
    TRIANGLES_UNIT,
    SkinRefinement,
)
from .stroke_renderer import StrokeBuffers, build_segment_vertices
from .texture import DataTexture, Texture2D, default_matcap_pixels

#: How far annotations are lifted off the surface, as a share of the scene
#: radius.  Enough to clear the depth buffer's precision at any zoom, small
#: enough that the paint still reads as sitting on the form.
_STROKE_LIFT = 0.0015
#: Additional nudge towards the viewer in NDC, for strokes seen edge-on.
_STROKE_DEPTH_BIAS = 2e-4
#: The section contour sits exactly on the cut, so it needs a larger nudge.
_CONTOUR_DEPTH_BIAS = 8e-4
#: How solid the depth guide is where it is not faded: never quite, so the
#: form still reads through it.
_GUIDE_PEAK = 0.7
#: Shadow map resolution.  2048 keeps the penumbra smooth without a
#: measurable cost next to drawing the model itself.
_SHADOW_SIZE = 2048
#: Texture units, fixed so the uniforms can be set once per frame.
_MATCAP_UNIT, _SHADOW_UNIT, _OCCLUSION_UNIT, _PLANE_UNIT = 0, 1, 2, 3
#: The two the ghost's sums are read back through, used by the resolve pass only.
_GHOST_ACCUM_UNIT, _GHOST_REVEAL_UNIT = 4, 5
#: The whole frame, read back by the resolve pass.  On unit nought, because
#: that pass runs alone once everything else has let go of its textures.
_FRAME_UNIT = 0
#: How wide the line round a highlighted object is, in logical pixels.
_HIGHLIGHT_WIDTH = 2.5

#: How the frame is smoothed on its way to the screen: not at all, FXAA over a
#: frame the screen's own size, or supersampling -- the frame drawn at twice
#: the size in each direction and averaged down.  These are the values the
#: viewport preference holds.
ANTIALIASING_MODES = ("off", "fxaa", "ssaa")
_SUPERSAMPLE = 2

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
        #: The :attr:`~refview.core.mesh.Mesh.serial` of what is uploaded,
        #: so the same mesh handed over twice is not sent twice.
        self._serial = 0

    def holds(self, mesh: Mesh) -> bool:
        return self._index_count > 0 and self._serial == mesh.serial

    def upload(self, mesh: Mesh) -> None:
        self._serial = mesh.serial
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
        self._serial = 0

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
        #: One set of buffers per object drawn, with how solid each is; the
        #: scene is several models now, and a ghosted one beside a solid one
        #: has to be drawn in a pass of its own.  The list grows to the most
        #: objects ever shown and the spare entries sit empty.
        self._buffers: list[MeshBuffers] = []
        self._parts: list[tuple[MeshBuffers, float]] = []
        #: The planar stand-in drawn in place of the model, when the artist has
        #: asked for the form itself to be broken into planes.  Empty the rest
        #: of the time, and never anything the model is measured or picked
        #: against -- see :mod:`refview.core.plane_solids`.
        self._sculpt: MeshBuffers | None = None
        #: The primary forms -- the bucket, the egg, the wedge -- drawn as clay
        #: alongside the model rather than in place of it.  Nothing is picked
        #: or measured against them either.
        self._forms: MeshBuffers | None = None
        self._forms_color: tuple[float, float, float] = (0.8, 0.6, 0.46)
        self._pedestal: MeshBuffers | None = None
        self._strokes: StrokeBuffers | None = None
        self._contour: StrokeBuffers | None = None
        #: The grid laid across the depth axis while a marker is being moved
        #: in depth, and the point and radius it fades about.  Drawn into the
        #: scene rather than over it, so the model stands in front of it or
        #: behind it and says which.
        self._guide: StrokeBuffers | None = None
        self._guide_fade: tuple[np.ndarray, float] | None = None
        #: The reference grids, and the point they fade about.
        self._grid: StrokeBuffers | None = None
        self._grid_centre: np.ndarray | None = None
        self._shadow_map = DepthTarget(clamp_to_lit=True)
        self._scene_depth = GeometryTarget()
        self._occlusion = ColorTarget()
        self._occlusion_blur = ColorTarget()
        #: Where a see-through model is summed, then resolved over the frame.
        self._ghost = AccumTarget()
        #: Where the frame is drawn when it is to be smoothed before the
        #: screen sees it; untouched when it is not.
        self._frame = FrameTarget()
        #: Where one object is stamped on its own, so that the line drawn
        #: round it can be found; and which part wears the line this frame,
        #: how solid, and in what colour.  See :meth:`set_highlight`.
        self._mask = ColorTarget()
        self._highlight: tuple[int, float, tuple[float, float, float]] | None = None
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
        self.skin = SkinRefinement()
        self._trace_parts = {}
        self._content_revision = 0

    # -- lifetime -------------------------------------------------------

    def initialize(self) -> None:
        self.skin.initialize(shaders.FULLSCREEN_VERTEX)
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
            "resolve": ShaderProgram(
                shaders.FULLSCREEN_VERTEX, shaders.RESOLVE_FRAGMENT, "resolve"
            ),
            "outline": ShaderProgram(
                shaders.FULLSCREEN_VERTEX, shaders.OUTLINE_FRAGMENT, "outline"
            ),
        }
        self._buffers = []
        self._parts = []
        self._sculpt = MeshBuffers()
        self._forms = MeshBuffers()
        self._pedestal = MeshBuffers()
        self._strokes = StrokeBuffers()
        self._contour = StrokeBuffers()
        self._guide = StrokeBuffers()
        self._grid = StrokeBuffers()
        self._empty_vao = int(GL.glGenVertexArrays(1))
        self._matcap = Texture2D()
        self._matcap.upload(default_matcap_pixels())
        self._plane_table = DataTexture()
        self._shadow_map.resize(_SHADOW_SIZE, _SHADOW_SIZE)

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_CULL_FACE)  # Reference meshes are often single-sided.

    def dispose(self) -> None:
        self.skin.dispose()
        for program in self._programs.values():
            program.dispose()
        self._programs.clear()
        for buffers in (
            *self._buffers,
            self._sculpt,
            self._forms,
            self._pedestal,
            self._strokes,
            self._contour,
            self._guide,
            self._grid,
        ):
            if buffers is not None:
                buffers.dispose()
        self._buffers = []
        self._parts = []
        for target in (
            self._shadow_map,
            self._scene_depth,
            self._occlusion,
            self._occlusion_blur,
            self._ghost,
            self._frame,
            self._mask,
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

    def set_mesh(
        self, mesh: Mesh | None, parts: list[tuple[Mesh, float]] | None = None
    ) -> None:
        """Replace the model: the whole scene as one mesh, and the objects it is made of.

        ``mesh`` is what the planes are fitted to and the skin tracer reads;
        ``parts`` is what is drawn, one entry per object with how solid it
        is, so that each object can be ghosted on its own.  Left out, the
        mesh is drawn as the one solid part it used to be.
        """
        self._trace_parts["model"] = mesh
        self._trace_parts["sculpt"] = None
        self._content_revision += 1
        if parts is None:
            parts = [] if mesh is None else [(mesh, 1.0)]
        while len(self._buffers) < len(parts):
            self._buffers.append(MeshBuffers())
        self._parts = []
        for buffers, (part, opacity) in zip(self._buffers, parts, strict=False):
            # Only the object that moved is sent again: on a drag the others
            # are the very meshes already in their buffers.
            if not buffers.holds(part):
                self._set_geometry(buffers, part)
            self._parts.append((buffers, min(max(float(opacity), 0.0), 1.0)))
        for buffers in self._buffers[len(parts):]:
            buffers.clear()
        # Any stand-in in hand was built out of the model being replaced, so
        # it goes now rather than being drawn for the frames until a new one
        # arrives.
        self._set_geometry(self._sculpt, None)
        self._mesh = mesh
        self._plane_axes.clear()

    def set_part_opacities(self, opacities: list[float]) -> None:
        """Change how solid each object is drawn, leaving the geometry where it is."""
        self._parts = [
            (buffers, min(max(float(opacity), 0.0), 1.0))
            for (buffers, _), opacity in zip(self._parts, opacities, strict=False)
        ] + self._parts[len(opacities):]
        self._content_revision += 1

    def set_highlight(
        self,
        part: int | None,
        alpha: float = 1.0,
        color: tuple[float, float, float] = (1.0, 0.77, 0.36),
    ) -> None:
        """Draw a line round the object at ``part`` -- the index into the parts -- or none.

        The line is laid over the finished frame, so it is not part of the
        picture: the skin tracer's samples, the smoothing and the ghost all
        come out the same with it as without.  Which is why it is not in the
        content revision, and a fade needs no more than a frame a step.
        """
        if part is None or alpha <= 0.0:
            self._highlight = None
        else:
            self._highlight = (int(part), min(float(alpha), 1.0), tuple(color))

    def set_sculpt(self, mesh: Mesh | None) -> None:
        """Draw ``mesh`` in place of the model; pass ``None`` to draw the model.

        The stand-in stands in everywhere the model is drawn -- the shading
        pass, the shadow map, the depth pre-pass the occlusion is read off,
        the wireframe -- because a form that is faceted to the eye and round
        to its own shadow is not a form anyone could work from.
        """
        self._set_geometry(self._sculpt, mesh)
        self._trace_parts["sculpt"] = mesh
        self._content_revision += 1

    def set_pedestal(self, mesh: Mesh | None) -> None:
        """Replace the ground disc; pass ``None`` to hide it."""
        self._set_geometry(self._pedestal, mesh)
        self._trace_parts["pedestal"] = mesh
        self._content_revision += 1

    def set_forms(self, mesh: Mesh | None, color: tuple[float, float, float]) -> None:
        """Replace the clay of the primary forms; pass ``None`` to hide it.

        The forms are drawn with the model, not instead of it: they are laid
        over the reference, and it is the reference that is ghosted when the
        artist wants to see them inside it.  They throw shadows and take
        occlusion like anything else standing on the pedestal.
        """
        self._forms_color = tuple(float(value) for value in color)
        self._set_geometry(self._forms, mesh)
        self._trace_parts["forms"] = mesh
        self._content_revision += 1

    def _model_parts(self, settings: RenderSettings) -> list[tuple[MeshBuffers, float]]:
        """Whatever is standing for the model this frame, with how solid each piece is.

        The planar stand-in, when there is one, stands in for every object at
        once; otherwise each object is its own part at its own solidity,
        under the scene-wide ghost.
        """
        opacity = settings.surface_opacity
        if self._sculpt is not None and not self._sculpt.is_empty:
            return [(self._sculpt, opacity)]
        return [
            (buffers, opacity * own) for buffers, own in self._parts if not buffers.is_empty
        ]

    @property
    def _model_buffers(self) -> list[MeshBuffers]:
        """Every buffer standing for the model, for the passes that draw them all alike."""
        if self._sculpt is not None and not self._sculpt.is_empty:
            return [self._sculpt]
        return [buffers for buffers, _ in self._parts if not buffers.is_empty]

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
        self.skin.clock.key = None

    def set_contour(self, vertices: np.ndarray) -> None:
        """Replace the section contour, prepared by the caller as stroke vertices."""
        if self._contour is not None:
            self._contour.upload_vertices(vertices)
        self.skin.clock.key = None

    def set_guide(self, vertices: np.ndarray, centre=None, reach: float = 0.0) -> None:
        """Replace the depth guide: stroke vertices fading about ``centre``.

        Empty vertices take it away, which is what happens the moment the
        marker is let go of.
        """
        if self._guide is not None:
            self._guide.upload_vertices(vertices)
        self.skin.clock.key = None
        self._guide_fade = (
            None if centre is None or reach <= 0.0
            else (np.asarray(centre, dtype=np.float64), float(reach))
        )

    def set_grid(self, lines) -> None:
        """Replace the reference grids; pass ``None`` to take them away.

        ``lines`` is a :class:`~refview.core.grid.GridLines`: the segments
        arrive with a colour and a width each, since the axis lines and the
        heavy lines differ from the rest.
        """
        if self._grid is None:
            return
        if lines is None or len(lines.segments) == 0:
            self._grid.upload_vertices(np.zeros((0, 14), dtype=np.float32))
            self._grid_centre = None
        else:
            blocks = []
            # One block per distinct colour-and-width, which is a handful.
            keys = np.concatenate([lines.colors, lines.widths[:, None]], axis=1)
            distinct, back = np.unique(keys, axis=0, return_inverse=True)
            back = back.ravel()
            for index, key in enumerate(distinct):
                chosen = lines.segments[back == index]
                blocks.append(build_segment_vertices(chosen, key[:3], float(key[3])))
            self._grid.upload_vertices(np.concatenate(blocks))
            self._grid_centre = np.asarray(lines.centre, dtype=np.float64)
        self.skin.clock.key = None

    # -- drawing --------------------------------------------------------

    def render(
        self,
        camera: Camera,
        settings: RenderSettings,
        width: int,
        height: int,
        pixel_ratio: float = 1.0,
        antialiasing: str = "off",
        *,
        refine: bool = False,
        interactive: bool = False,
    ) -> None:
        """Draw one frame, then hand a neutral GL state back to the caller.

        ``width``/``height`` are in device pixels; ``pixel_ratio`` converts the
        logical pixel sizes coming from the UI into the same units.
        ``antialiasing`` is one of :data:`ANTIALIASING_MODES`; anything but
        ``"off"`` draws the frame offscreen and smooths it on the way out.

        The widget paints its 2D overlay with QPainter straight afterwards, and
        Qt's paint engine assumes depth testing is off and nothing is bound --
        leaving the scene's state behind silently swallows strokes and text.
        """
        width, height = max(width, 1), max(height, 1)
        screen = current_framebuffer()
        skin = settings.skin.bounded()
        is_skin = settings.shading_mode is ShadingMode.HUMAN_SKIN
        key = (
            camera.view_matrix().tobytes(), camera.projection_matrix(width / height).tobytes(),
            repr(settings), self._content_revision, width, height, pixel_ratio, antialiasing,
        )
        model_mesh = self._trace_parts.get("sculpt")
        if model_mesh is None or not model_mesh.triangle_count:
            model_mesh = self._trace_parts.get("model")
        parts = [(mesh, material, color) for mesh, material, color in (
            (model_mesh, 0, skin.color),
            (self._trace_parts.get("pedestal"), 1, settings.pedestal.color),
            (self._trace_parts.get("forms"), 1, self._forms_color),
        ) if mesh is not None]
        revision = (self._content_revision, settings.pedestal.color, self._forms_color)
        traced = self.skin.prepare(
            key, revision, parts, skin, interactive,
            refine and is_skin and skin.progressive and settings.surface_opacity >= 1.0,
        )
        scale = _SUPERSAMPLE if antialiasing == "ssaa" else 1
        offscreen = antialiasing in ("fxaa", "ssaa")
        try:
            if traced:
                if self.skin.clock.samples < skin.samples:
                    rw = max(1, int(width * skin.resolution * scale))
                    rh = max(1, int(height * skin.resolution * scale))
                    self.skin.begin(rw, rh)
                    self._draw_frame(
                        camera, settings, rw, rh, pixel_ratio * skin.resolution * scale
                    )
                    self.skin.accumulate(self._draw_fullscreen)
                if antialiasing == "fxaa":
                    self._frame.resize(width, height)
                    self._frame.bind()
                    self.skin.present(current_framebuffer(), width, height, self._draw_fullscreen)
                    bind_default(screen)
                    self._resolve_frame(True)
                else:
                    self.skin.present(screen, width, height, self._draw_fullscreen)
                self.skin.needs_frame = self.skin.clock.samples < skin.samples
                self.skin.status = f"Human Skin · {self.skin.clock.samples}/{skin.samples} samples"
                self._draw_highlight(camera, settings, screen, width, height, pixel_ratio)
                return
            if offscreen:
                # Allocated before anything else is bound, for the same reason
                # the ghost's buffers are: see _draw_frame.
                self._frame.resize(width * scale, height * scale)
                self._frame.bind()
            self._draw_frame(
                camera, settings, width * scale, height * scale, pixel_ratio * scale
            )
            if offscreen:
                bind_default(screen)
                GL.glViewport(0, 0, width, height)
                self._resolve_frame(antialiasing == "fxaa")
            self._draw_highlight(camera, settings, screen, width, height, pixel_ratio)
        finally:
            bind_default(screen)
            self._reset_state()

    def _resolve_frame(self, fxaa: bool) -> None:
        """Lay the offscreen frame over the screen, smoothed."""
        frame_width, frame_height = self._frame.size
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDepthMask(GL.GL_FALSE)
        GL.glDisable(GL.GL_BLEND)
        with self._programs["resolve"] as program:
            program.set_int("uFrame", _FRAME_UNIT)
            program.set_vec2("uTexelSize", (1.0 / frame_width, 1.0 / frame_height))
            program.set_bool("uFxaa", fxaa)
            self._frame.bind_texture(_FRAME_UNIT)
            self._draw_fullscreen()
        GL.glDepthMask(GL.GL_TRUE)
        GL.glEnable(GL.GL_DEPTH_TEST)

    def _draw_highlight(
        self,
        camera: Camera,
        settings: RenderSettings,
        screen: int,
        width: int,
        height: int,
        pixel_ratio: float,
    ) -> None:
        """Lay the line round the highlighted object over the finished frame.

        Two passes: the object alone is stamped into the mask, with no depth
        test so that the line follows its whole silhouette and not only the
        part standing in front of the others -- the point of the line is to
        say which object was picked, even one half behind another -- and
        then the pixels just outside the stamp are coloured on the screen.
        """
        if self._highlight is None:
            return
        index, alpha, color = self._highlight
        if not 0 <= index < len(self._parts):
            return
        buffers = self._parts[index][0]
        if buffers.is_empty:
            return
        view = camera.view_matrix()
        projection = camera.projection_matrix(width / height)
        self._mask.resize(width, height)
        self._mask.bind()
        GL.glClearBufferfv(GL.GL_COLOR, 0, [0.0, 0.0, 0.0, 0.0])
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDepthMask(GL.GL_FALSE)
        GL.glDisable(GL.GL_BLEND)
        with self._programs["flat"] as program:
            program.set_matrix4("uView", view)
            program.set_matrix4("uProjection", projection)
            program.set_vec4("uColor", (1.0, 1.0, 1.0, 1.0))
            _set_section(program, settings.section.planes())
            buffers.draw()
        bind_default(screen)
        GL.glViewport(0, 0, width, height)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        with self._programs["outline"] as program:
            program.set_int("uMask", _FRAME_UNIT)
            program.set_vec2("uTexelSize", (1.0 / width, 1.0 / height))
            program.set_float("uRadius", _HIGHLIGHT_WIDTH * max(pixel_ratio, 0.1))
            program.set_vec4("uColor", (*color, alpha))
            self._mask.bind_texture(_FRAME_UNIT)
            self._draw_fullscreen()
        GL.glDisable(GL.GL_BLEND)
        GL.glDepthMask(GL.GL_TRUE)
        GL.glEnable(GL.GL_DEPTH_TEST)

    def _draw_frame(
        self,
        camera: Camera,
        settings: RenderSettings,
        width: int,
        height: int,
        pixel_ratio: float,
    ) -> None:
        """Everything in the frame, into whichever framebuffer is bound."""
        aspect = width / height
        view = camera.view_matrix()
        projection = camera.projection_matrix(aspect)
        if self.skin.tracing:
            # Halton jitter integrates primary visibility at silhouettes as
            # well as the light transport. The history key stays unjittered.
            from .skin_refinement import pixel_jitter

            dx, dy = pixel_jitter(self.skin.clock.samples)
            projection = projection.copy()
            projection[0] += (2.0 * dx / width) * projection[3]
            projection[1] += (2.0 * dy / height) * projection[3]
        planes = settings.section.planes()
        target = current_framebuffer()

        light_matrix = None
        if settings.shading_mode.uses_quality and self._has_geometry and not self.skin.tracing:
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
            self._draw_grid(camera, projection @ view, settings.grid, width, height, pixel_ratio)
            return

        self._draw_scene(
            camera, settings, view, projection, planes, light_matrix, width, height,
            pixel_ratio,
        )
        if settings.show_wireframe:
            self._draw_wireframe(settings, view, projection, planes)
        self._draw_contour(camera, projection @ view, settings, width, height, pixel_ratio)
        self._draw_strokes(camera, projection @ view, width, height, pixel_ratio, planes)
        self._draw_guide(projection @ view, width, height, pixel_ratio)

    @property
    def _has_geometry(self) -> bool:
        model = any(not buffers.is_empty for buffers, _ in self._parts)
        disc = self._pedestal is not None and not self._pedestal.is_empty
        return model or disc

    def _ghost_opacity(self, settings: RenderSettings) -> float | None:
        """How see-through the model is this frame, or ``None`` if it is solid.

        Asked in two places -- where the buffers are allocated and where they
        are filled -- and the two must agree, or a frame allocates nothing and
        then draws into it.  With several objects it is the most see-through
        of them; what matters to the caller is whether any is.
        """
        ghosted = [opacity for _, opacity in self._model_parts(settings) if opacity < 1.0]
        return min(ghosted) if ghosted else None

    def _accumulate_ghost(
        self,
        program: ShaderProgram,
        ghosts: list[tuple[MeshBuffers, float]],
        solid: list[MeshBuffers],
        camera: Camera,
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

        # The ground the model stands behind still has to hide it -- and so
        # do the objects drawn solid -- and this framebuffer has a depth
        # buffer of its own, so they are laid in again with the colour writes
        # shut off.
        blockers = [*solid]
        if self._pedestal is not None and not self._pedestal.is_empty:
            blockers.append(self._pedestal)
        if self._forms is not None and not self._forms.is_empty:
            blockers.append(self._forms)
        if blockers:
            GL.glColorMask(GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE, GL.GL_FALSE)
            for buffers in blockers:
                buffers.draw()
            GL.glColorMask(GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE, GL.GL_TRUE)

        near, span = _ghost_depth_range(camera)
        program.set_float("uGhostNear", near)
        program.set_float("uGhostSpan", span)
        program.set_bool("uAccumulate", True)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_ONE, GL.GL_ONE)
        GL.glDepthMask(GL.GL_FALSE)
        for buffers, opacity in ghosts:
            program.set_float("uOpacity", opacity)
            buffers.draw()
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
        for unit in (_SHADOW_UNIT, _OCCLUSION_UNIT, _GHOST_ACCUM_UNIT, _GHOST_REVEAL_UNIT,
                     NODES_UNIT, TRIANGLES_UNIT, DIFFUSION_UNIT):
            GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
            GL.glBindTexture(GL.GL_TEXTURE_2D, 0)
        GL.glActiveTexture(GL.GL_TEXTURE0 + RELIEF_UNIT)
        GL.glBindTexture(GL.GL_TEXTURE_3D, 0)
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
        assert self._pedestal is not None
        key_direction, fill_direction = light_directions(settings, view)

        parts = self._model_parts(settings)
        solid = [buffers for buffers, opacity in parts if opacity >= 1.0]
        ghosts = [(buffers, opacity) for buffers, opacity in parts if opacity < 1.0]
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

            contour = settings.contour
            program.set_vec3("uSliceDirection", contour.normal(tuple(camera.forward)))
            program.set_float(
                "uSliceSpacing",
                2.0 * max(camera.scene_radius, 1e-6)
                / max(contour.density, CONTOUR_DENSITY_MIN),
            )
            program.set_float("uSliceWidth", contour.line_width * max(pixel_ratio, 0.1))
            program.set_vec3("uSliceColor", contour.line_color)
            program.set_vec3("uSlicePaper", contour.paper_color)
            program.set_bool("uSliceLit", contour.lit)

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

            skin = settings.skin.bounded()
            self.skin.bind(program)
            program.set_vec3("uSkinColor", skin.color)
            program.set_vec3("uSkinScatter", skin.scatter_color)
            for uniform, value in (
                ("Roughness", skin.roughness), ("Specular", skin.specular),
                ("Oil", skin.oiliness), ("SSS", skin.sss),
                ("Transmission", skin.transmission), ("Exposure", skin.exposure),
                ("Indirect", skin.indirect), ("LightSize", math.radians(skin.light_size)),
                ("Detail", skin.detail), ("Mottle", skin.mottle),
                ("Blood", skin.blood), ("Fuzz", skin.fuzz),
                ("Radius", skin.radius * max(camera.scene_radius, 1e-6)),
                ("PoreSize", skin.pore_size * max(camera.scene_radius, 1e-6)),
                ("Epsilon", max(camera.scene_radius, 1e-6) * 1e-5),
            ):
                program.set_float("uSkin" + uniform, value)
            program.set_bool("uSkinFurniture", True)

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
            if self._forms is not None and not self._forms.is_empty:
                # Clay, in its own colour: under a matcap the tint is what
                # carries a colour, elsewhere the diffuse term does.  Drawn
                # solid before the model so that a ghosted model composites
                # over it and the forms show through.  Already flats, so the
                # planes filter has nothing to add to them.
                program.set_vec3("uDiffuseColor", self._forms_color)
                program.set_vec3(
                    "uMatcapTint",
                    tuple(t * c for t, c in zip(matcap.tint, self._forms_color, strict=True)),
                )
                program.set_bool("uPlaneShading", False)
                program.set_float("uOpacity", 1.0)
                self._forms.draw()
                program.set_vec3("uMatcapTint", matcap.tint)
                program.set_bool("uPlaneShading", shades)
            if parts:
                program.set_bool("uSkinFurniture", False)
                program.set_vec3("uDiffuseColor", surface.diffuse_color)
                program.set_float("uOpacity", 1.0)
                # The solid objects first, so that the ghosts can be hidden
                # behind them; the ghosts are summed afterwards into buffers
                # of their own and laid over the frame.
                for buffers in solid:
                    buffers.draw()
                if ghosts:
                    self._accumulate_ghost(program, ghosts, solid, camera, width, height)

        # The grid goes down before the ghost is laid over the frame, so a
        # see-through figure still reads as standing on it rather than
        # behind it.
        self._draw_grid(camera, projection @ view, settings.grid, width, height, pixel_ratio)

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
        return tuple(
            b for b in (*self._model_buffers, self._forms, self._pedestal) if b is not None
        )

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
            program.set_float("uFadeRadius", 0.0)
            program.set_float("uAlpha", 1.0)
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
            program.set_float("uFadeRadius", 0.0)
            program.set_float("uAlpha", 1.0)
            _set_section(program, planes)
            self._strokes.draw()
        GL.glDepthMask(GL.GL_TRUE)

    def _draw_guide(
        self, view_projection: np.ndarray, width: int, height: int, pixel_ratio: float
    ) -> None:
        """The depth grid, in the scene: hidden where the model is nearer.

        Depth-tested and not depth-written, like the strokes, and blended,
        because it fades towards its edges -- a grid with a hard edge would
        read as a floor with a rim, and this is a cue and not a floor.  Never
        clipped by the section: a marker is as likely to be moved inside a
        cut-open form as anywhere, and the grid has to follow it in.
        """
        if self._guide is None or self._guide.is_empty or self._guide_fade is None:
            return
        centre, reach = self._guide_fade
        GL.glDepthMask(GL.GL_FALSE)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        with self._programs["stroke"] as program:
            program.set_matrix4("uViewProjection", view_projection)
            program.set_vec2("uViewport", (width, height))
            program.set_float("uWidthScale", max(pixel_ratio, 0.1))
            program.set_float("uNormalOffset", 0.0)
            program.set_float("uDepthBias", _STROKE_DEPTH_BIAS)
            program.set_vec3("uFadeCentre", centre)
            program.set_float("uFadeRadius", reach)
            program.set_float("uFadePeak", _GUIDE_PEAK)
            _set_section(program, [])
            self._guide.draw()
        GL.glDisable(GL.GL_BLEND)
        GL.glDepthMask(GL.GL_TRUE)

    def _draw_grid(
        self,
        camera: Camera,
        view_projection: np.ndarray,
        grid: GridSettings,
        width: int,
        height: int,
        pixel_ratio: float,
    ) -> None:
        """The reference grids: in the scene, behind whatever stands on them.

        Drawn as the depth guide is -- tested against the depth buffer, not
        written into it, blended, never cut by the section -- and faded about
        the camera rather than about a point on the grid, so the far squares
        go before they can crowd into a moire at the horizon.  The fade is a
        multiple of how far the camera stands from the grid's centre, which
        is what keeps it looking the same at every zoom.
        """
        if self._grid is None or self._grid.is_empty or self._grid_centre is None:
            return
        if not grid.any:
            return  # an export can ask for the frame without it
        eye = np.asarray(camera.eye, dtype=np.float64)
        away = float(np.linalg.norm(eye - self._grid_centre))
        if camera.projection is Projection.ORTHOGRAPHIC:
            # An orthographic eye can sit anywhere along its own axis; what
            # is meaningful is the framed height.
            away = max(camera.ortho_half_height * 2.0, away)
        reach = max(float(grid.fade), 0.0) * max(away, 1e-6)
        GL.glDepthMask(GL.GL_FALSE)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        with self._programs["stroke"] as program:
            program.set_matrix4("uViewProjection", view_projection)
            program.set_vec2("uViewport", (width, height))
            program.set_float("uWidthScale", max(pixel_ratio, 0.1))
            program.set_float("uNormalOffset", 0.0)
            program.set_float("uDepthBias", _STROKE_DEPTH_BIAS)
            program.set_vec3("uFadeCentre", eye)
            program.set_float("uFadeRadius", reach)
            peak = min(max(float(grid.opacity), 0.0), 1.0)
            program.set_float("uFadePeak", peak)
            program.set_float("uAlpha", peak)
            _set_section(program, [])
            self._grid.draw()
        GL.glDisable(GL.GL_BLEND)
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
