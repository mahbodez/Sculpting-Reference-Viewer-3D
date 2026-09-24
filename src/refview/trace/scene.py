"""What a render is made from, gathered once and laid out for the kernels.

:class:`TraceInputs` is a snapshot of everything a render depends on -- the
meshes as they stand, the camera, both sets of settings, the HDRI -- taken on
the interface thread and never touched again, so the render threads can read
it while the artist goes on working.  :func:`compile_scene` turns it into
the three tables the kernels read:

* the geometry (:class:`~refview.trace.geometry.Geometry`): the tree and the
  triangles, which is slow to build and so kept by :class:`SceneCache` for
  as long as the meshes do not change;
* the shading (:class:`Shading`): materials, lights, the HDRI's tables, the
  skin's parameters and volumes;
* the parameters (:class:`Params`): the camera, the size, the bounces.

How each shading mode becomes a material is decided here.  The modes with a
physical reading -- PBR, the analytic modes, Human Skin -- keep their own
colours and shine; a matcap or the normals picture is a way of looking, not a
material, so those render as clay (:class:`~refview.core.path_trace.ClaySettings`).
The pedestal and the forms keep their own colours in every mode.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from enum import IntEnum
from typing import NamedTuple

import numpy as np

from ..core.body_regions import BodyMap, BodySource, build_body_map
from ..core.camera import Camera, Projection
from ..core.environment import EnvironmentMap, downsized
from ..core.lighting import light_rig
from ..core.mesh import Mesh
from ..core.path_trace import PathTraceSettings
from ..core.progress import Progress
from ..core.settings import RenderSettings, ShadingMode
from ..core.skin_detail import relief_volume
from .camera import filter_table
from .geometry import Geometry, flatten
from .lights import LIGHT_STRIDE, light_row
from .materials import MAT_PRINCIPLED, MAT_SKIN, material_row
from .skin import skin_parameters


def _linear(c: float) -> float:
    c = float(c)
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_color(color) -> tuple[float, float, float]:
    return tuple(_linear(min(max(float(v), 0.0), 1.0)) for v in color)


class PartKind(IntEnum):
    MODEL = 0
    PEDESTAL = 1
    FORMS = 2


@dataclass(frozen=True)
class TracePart:
    """One mesh of the scene, as the renderer draws it, in world space."""

    mesh: Mesh
    kind: PartKind
    #: The part's own colour, as the panel shows it (sRGB); the model's
    #: comes from the shading mode instead.
    color: tuple[float, float, float] = (0.8, 0.8, 0.8)
    #: How solid it is drawn: a ghost is seen through.
    opacity: float = 1.0


@dataclass(frozen=True)
class TraceInputs:
    parts: tuple[TracePart, ...]
    #: The camera that fills the frame (see :func:`~refview.core.render_frame.framed_camera`).
    camera: Camera
    width: int
    height: int
    render: RenderSettings
    path_trace: PathTraceSettings
    environment: EnvironmentMap | None = None
    #: What the skin's body map is worked out from, or ``None`` for no map.
    body: BodySource | None = None

    @property
    def geometry_key(self) -> tuple:
        """What the triangle tree depends on: two inputs with equal keys share a tree."""
        planes = tuple((tuple(np.round(p.normal, 12)), round(float(p.offset), 12))
                       for p in self.render.section.planes())
        return (
            tuple((id(p.mesh), p.mesh.serial, int(p.kind), round(p.opacity, 6))
                  for p in self.parts),
            planes,
            self.render.section.fill_cut,
        )


class Shading(NamedTuple):
    materials: np.ndarray
    lights: np.ndarray
    sky: np.ndarray
    env_on: bool
    env_background: bool
    env_rgb: np.ndarray
    env_bg: np.ndarray
    env_density: np.ndarray
    env_conditional: np.ndarray
    env_marginal: np.ndarray
    env_rotation: np.ndarray
    env_scale: float
    skin: np.ndarray
    regions: np.ndarray
    relief: np.ndarray
    body: np.ndarray


class Params(NamedTuple):
    width: int
    height: int
    seed: int
    max_bounces: int
    max_diffuse: int
    max_glossy: int
    max_transmission: int
    clamp_direct: float
    clamp_indirect: float
    filter_glossy: float
    caustics: bool
    transparent: bool
    cam_origin: np.ndarray
    cam_right: np.ndarray
    cam_up: np.ndarray
    cam_forward: np.ndarray
    ortho: bool
    tan_half: float
    aspect: float
    ortho_half: float
    ortho_back: float
    aperture: float
    focus_distance: float
    filter_table: np.ndarray
    #: How wide a pixel's cone grows per unit of distance, and its fixed width
    #: for an orthographic camera.
    pixel_spread: float
    ortho_footprint: float


@dataclass
class CompiledScene:
    geometry: Geometry
    shading: Shading
    params: Params
    #: Human Skin: the view transform's "Auto" and the skin's exposure follow it.
    skin: bool
    #: The skin's exposure, in stops, added to the render's own.
    exposure: float
    triangles: int


# Material rows.
MAT_ROW_MODEL, MAT_ROW_PEDESTAL, MAT_ROW_FORMS, MAT_ROW_CAP = range(4)


def model_material(render: RenderSettings, trace: PathTraceSettings) -> np.ndarray:
    """The model's material row for the current shading mode."""
    mode = render.shading_mode
    surface = render.surface
    if mode is ShadingMode.HUMAN_SKIN:
        return material_row(linear_color(render.skin.color), kind=MAT_SKIN)
    if mode is ShadingMode.PBR:
        f0 = tuple(0.16 * surface.specular_level * c for c in surface.specular_color)
        return material_row(linear_color(surface.diffuse_color), metallic=surface.metalness,
                            roughness=surface.roughness, f0=f0,
                            tint=tuple(surface.reflection_color))
    if mode is ShadingMode.LAMBERT:
        return material_row(linear_color(surface.diffuse_color), roughness=1.0, f0=(0, 0, 0))
    if mode in (ShadingMode.PHONG, ShadingMode.BLINN_PHONG, ShadingMode.HIGH_QUALITY):
        exponent = max(surface.shininess, 1.0) * (1.0 if mode is ShadingMode.PHONG else 4.0)
        roughness = math.sqrt(math.sqrt(2.0 / (exponent + 2.0)))
        f0 = tuple(0.16 * surface.specular_level * c for c in surface.specular_color)
        return material_row(linear_color(surface.diffuse_color), roughness=roughness, f0=f0)
    clay = trace.clay
    f0 = (0.08 * clay.specular,) * 3
    return material_row(linear_color(clay.color), roughness=clay.roughness, f0=f0)


def furniture_material(color, render: RenderSettings, trace: PathTraceSettings) -> np.ndarray:
    """The pedestal's or the forms' row: their own colour, and the model's shine in its mode."""
    base = linear_color(color)
    if render.shading_mode is ShadingMode.HUMAN_SKIN:
        # The skin's own furniture is matte, as the viewport draws it.
        return material_row(base, roughness=1.0, f0=(0.0, 0.0, 0.0))
    row = model_material(render, trace)
    row[1:4] = base
    return row


class SceneCache:
    """The slow parts of a compile, kept between renders of the same meshes.

    Confined to one thread at a time: the controller that owns it compiles on
    a worker, one render after another.
    """

    def __init__(self) -> None:
        self._geometry_key: tuple | None = None
        self._geometry: Geometry | None = None
        self._body_key = None
        self._body: BodyMap | None = None
        self._relief: np.ndarray | None = None
        self._env_key = None
        self._env_tables = None

    def geometry(self, inputs: TraceInputs, progress: Progress | None = None) -> Geometry:
        key = inputs.geometry_key
        if self._geometry is not None and key == self._geometry_key:
            return self._geometry
        if progress is not None:
            progress.report(message="Building the ray-tracing tree...")
        self._geometry = build_geometry(inputs)
        self._geometry_key = key
        return self._geometry

    def body_map(self, source: BodySource | None) -> BodyMap | None:
        if source is None:
            return None
        if self._body_key == source.key and self._body is not None:
            return self._body
        self._body = build_body_map(source)
        self._body_key = source.key
        return self._body

    def relief(self) -> np.ndarray:
        if self._relief is None:
            self._relief = relief_volume()
        return self._relief

    def environment(self, env: EnvironmentMap, blur: float) -> tuple[np.ndarray, ...]:
        key = (id(env), round(float(blur), 3))
        if self._env_key == key and self._env_tables is not None:
            return self._env_tables
        rgb = np.ascontiguousarray(env.radiance, dtype=np.float32)
        width = max(int(rgb.shape[1] / 2.0 ** max(float(blur), 0.0)), 8)
        bg = rgb if width >= rgb.shape[1] else np.ascontiguousarray(
            downsized(rgb, width), dtype=np.float32)
        sampling = env.sampling
        self._env_tables = (
            rgb, bg,
            np.ascontiguousarray(sampling.density, dtype=np.float32),
            np.ascontiguousarray(sampling.conditional, dtype=np.float32),
            np.ascontiguousarray(sampling.marginal, dtype=np.float32),
        )
        self._env_key = key
        return self._env_tables


def build_geometry(inputs: TraceInputs) -> Geometry:
    corners, normals, materials, opacity = [], [], [], []
    rows = {PartKind.MODEL: MAT_ROW_MODEL, PartKind.PEDESTAL: MAT_ROW_PEDESTAL,
            PartKind.FORMS: MAT_ROW_FORMS}
    for part in inputs.parts:
        mesh = part.mesh
        if mesh is None or not mesh.triangle_count or part.opacity <= 0.0:
            continue
        corners.append(np.asarray(mesh.triangles, dtype=np.float32))
        normals.append(np.asarray(mesh.normals, dtype=np.float32)[mesh.indices])
        materials.append(np.full(mesh.triangle_count, rows[part.kind], np.int32))
        opacity.append(np.full(mesh.triangle_count, min(float(part.opacity), 1.0), np.float32))
    section = inputs.render.section
    planes = np.array([[*p.normal, p.offset] for p in section.planes()], dtype=np.float64)
    cap = MAT_ROW_CAP if (len(planes) and section.fill_cut) else -1
    if not corners:
        return flatten(np.zeros((0, 3, 3)), np.zeros((0, 3, 3)), np.zeros(0, np.int32),
                       np.ones(0, np.float32), planes.reshape(-1, 4), cap)
    return flatten(np.concatenate(corners), np.concatenate(normals), np.concatenate(materials),
                   np.concatenate(opacity), planes.reshape(-1, 4), cap)


def compile_scene(inputs: TraceInputs, cache: SceneCache,
                  progress: Progress | None = None) -> CompiledScene:
    """Everything the kernels read, for one render of ``inputs``."""
    render = inputs.render
    trace = inputs.path_trace
    camera = inputs.camera
    geometry = cache.geometry(inputs, progress)
    if progress is not None:
        progress.report(message="Preparing lights and materials...")
    is_skin = render.shading_mode is ShadingMode.HUMAN_SKIN
    skin_settings = render.skin.bounded()
    scene_radius = max(float(camera.scene_radius), 1e-6)

    # Materials.
    materials = np.zeros((4, 12), np.float64)
    materials[MAT_ROW_MODEL] = model_material(render, trace)
    pedestal = next((p for p in inputs.parts if p.kind is PartKind.PEDESTAL), None)
    forms = next((p for p in inputs.parts if p.kind is PartKind.FORMS), None)
    materials[MAT_ROW_PEDESTAL] = furniture_material(
        pedestal.color if pedestal else render.pedestal.color, render, trace)
    materials[MAT_ROW_FORMS] = furniture_material(
        forms.color if forms else (0.8, 0.8, 0.8), render, trace)
    materials[MAT_ROW_CAP] = material_row(linear_color(render.section.cap_color),
                                          roughness=1.0, f0=(0.0, 0.0, 0.0),
                                          kind=MAT_PRINCIPLED)

    # Lights, as the viewport settles them for this camera.
    view = camera.view_matrix()
    rig = light_rig(render, view, inputs.environment)
    # The display-space modes read a key of one as white on white: pi times
    # what the same irradiance makes of a physical surface.
    light_scale = 1.0 if is_skin else math.pi
    to_world = np.asarray(view, dtype=np.float64)[:3, :3].T
    color = np.array(linear_color(render.light.color))
    size_deg = skin_settings.light_size if is_skin else trace.light_size_deg
    rows = []
    for direction, intensity in ((rig.key, rig.key_intensity), (rig.fill, rig.fill_intensity)):
        if intensity <= 0.0:
            continue
        world = to_world @ np.asarray(direction, dtype=np.float64)
        world /= max(np.linalg.norm(world), 1e-12)
        rows.append(light_row(world, color * intensity * light_scale, math.radians(size_deg)))
    lights = np.array(rows, dtype=np.float64).reshape(-1, LIGHT_STRIDE)
    sky = np.zeros(4, np.float64)
    if rig.ambient_intensity > 0.0:
        sky[:3] = np.array(linear_color(render.light.ambient_color)) * rig.ambient_intensity
        sky[3] = 1.0

    env = inputs.environment if rig.environment else None
    if env is not None:
        rgb, bg, density, conditional, marginal = cache.environment(
            env, render.light.environment_blur)
        env_scale = rig.env_scale * light_scale
        rotation = np.ascontiguousarray(rig.env_from_world, dtype=np.float64)
    else:
        rgb = bg = np.zeros((1, 2, 3), np.float32)
        density = np.ones((1, 1), np.float32)
        conditional = np.array([[0.0, 1.0]], np.float32)
        marginal = np.array([0.0, 1.0], np.float32)
        env_scale = 0.0
        rotation = np.eye(3)

    # The skin.
    body_map = cache.body_map(inputs.body) if is_skin else None
    skin, regions = skin_parameters(skin_settings, scene_radius, body_map)
    body = (np.ascontiguousarray(body_map.voxels, dtype=np.float32) if body_map is not None
            else np.zeros((1, 1, 1, 8), np.float32))
    relief = cache.relief() if is_skin else np.zeros((1, 1, 1, 4), np.float32)

    shading = Shading(
        materials=materials, lights=lights, sky=sky,
        env_on=env is not None,
        env_background=bool(env is not None and render.light.environment_background),
        env_rgb=rgb, env_bg=bg, env_density=density, env_conditional=conditional,
        env_marginal=marginal, env_rotation=rotation, env_scale=float(env_scale),
        skin=skin, regions=regions, relief=relief, body=body,
    )
    params = make_params(inputs, geometry)
    return CompiledScene(
        geometry=geometry, shading=shading, params=params, skin=is_skin,
        exposure=float(skin_settings.exposure) if is_skin else 0.0,
        triangles=int(len(geometry.material)),
    )


def make_params(inputs: TraceInputs, geometry: Geometry, width: int | None = None,
                height: int | None = None) -> Params:
    """The camera and the path settings, for a picture ``width`` by ``height``."""
    trace = inputs.path_trace
    camera = inputs.camera
    width = int(width or inputs.width)
    height = int(height or inputs.height)
    paths = trace.paths
    lens = trace.lens
    radius = max(float(camera.scene_radius), 1e-6)
    ortho = camera.projection is Projection.ORTHOGRAPHIC
    tan_half = math.tan(math.radians(camera.fov_deg) * 0.5)
    ortho_half = camera.ortho_half_height
    eye = np.asarray(camera.eye, dtype=np.float64)
    reach = float(np.linalg.norm(eye - np.asarray(geometry.center))) + geometry.radius * 2.0
    aperture = 0.0
    focus = camera.distance
    if lens.depth_of_field and not ortho:
        aperture = lens.aperture * radius
        if not lens.focus_on_target:
            focus = lens.focus_distance * radius
    return Params(
        width=width, height=height, seed=int(trace.sampling.seed),
        max_bounces=int(paths.max_bounces), max_diffuse=int(paths.diffuse),
        max_glossy=int(paths.glossy), max_transmission=int(paths.transmission),
        clamp_direct=float(paths.clamp_direct), clamp_indirect=float(paths.clamp_indirect),
        filter_glossy=float(paths.filter_glossy), caustics=bool(paths.caustics),
        transparent=bool(trace.output.transparent),
        cam_origin=eye.copy(), cam_right=np.asarray(camera.right, dtype=np.float64),
        cam_up=np.asarray(camera.up, dtype=np.float64),
        cam_forward=np.asarray(camera.forward, dtype=np.float64),
        ortho=ortho, tan_half=tan_half, aspect=width / max(height, 1),
        ortho_half=ortho_half, ortho_back=reach, aperture=aperture,
        focus_distance=max(focus, 1e-6),
        filter_table=filter_table(trace.film.filter, trace.film.filter_width),
        pixel_spread=0.0 if ortho else 2.0 * tan_half / max(height, 1),
        ortho_footprint=2.0 * ortho_half / max(height, 1) if ortho else 0.0,
    )


def with_size(scene: CompiledScene, inputs: TraceInputs, width: int, height: int) -> CompiledScene:
    """The same scene for a picture of another size (the viewport preview's resolutions)."""
    return replace(scene, params=make_params(inputs, scene.geometry, width, height))


def trace_settings_key(render: RenderSettings, trace: PathTraceSettings) -> str:
    """What of the settings a rendered picture shows, as a key.

    The viewport preview starts over when this changes.  It leaves out what
    no rendered pixel reads: the grid, the wireframe, the matcap image, the
    contour paper and the section's contour line, and of the path tracer's
    own settings the output size, the safe frame, the colour (applied after
    rendering) and the denoiser.
    """
    render_part = repr(replace(
        render, matcap=None, matcap_path=None, contour=None, grid=None, quality=None,
        show_wireframe=False, wireframe_color=None,
        section=replace(render.section, show_contour=False, contour_color=None,
                        contour_width=None),
    ))
    trace_part = repr(replace(trace, output=None, safe_frame=None, color=None, denoise=None,
                              preset=None))
    return render_part + trace_part
