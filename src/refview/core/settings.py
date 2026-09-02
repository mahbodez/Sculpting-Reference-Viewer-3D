"""Serialisable description of how the object should be shaded.

Every value here maps onto a shader uniform or a draw-state toggle; the UI
panels edit these dataclasses and nothing else.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .pedestal import PedestalSettings
from .section import SectionSettings

Color = tuple[float, float, float]


class ShadingMode(str, Enum):
    """Shading model applied to the mesh.

    ``shader_id`` must stay in sync with the branch constants in
    :mod:`refview.render.shaders`.
    """

    MATCAP = "matcap"
    LAMBERT = "lambert"
    PHONG = "phong"
    BLINN_PHONG = "blinn_phong"
    PBR = "pbr"
    NORMALS = "normals"
    HIGH_QUALITY = "high_quality"

    @property
    def label(self) -> str:
        return {
            ShadingMode.MATCAP: "Matcap",
            ShadingMode.LAMBERT: "Lambert",
            ShadingMode.PHONG: "Phong",
            ShadingMode.BLINN_PHONG: "Blinn-Phong",
            ShadingMode.PBR: "PBR (GGX)",
            ShadingMode.NORMALS: "Normals",
            ShadingMode.HIGH_QUALITY: "High Quality",
        }[self]

    @property
    def shader_id(self) -> int:
        return list(ShadingMode).index(self)

    @property
    def uses_matcap(self) -> bool:
        return self is ShadingMode.MATCAP

    @property
    def uses_lighting(self) -> bool:
        return self in (
            ShadingMode.LAMBERT,
            ShadingMode.PHONG,
            ShadingMode.BLINN_PHONG,
            ShadingMode.PBR,
            ShadingMode.HIGH_QUALITY,
        )

    @property
    def uses_quality(self) -> bool:
        """Whether the shadow and occlusion pre-passes need to run."""
        return self is ShadingMode.HIGH_QUALITY


@dataclass
class MatcapSettings:
    """Post-processing applied to the sampled matcap texel."""

    rotation_deg: float = 0.0
    contrast: float = 1.0
    gamma: float = 1.0
    brightness: float = 1.0
    saturation: float = 1.0
    tint: Color = (1.0, 1.0, 1.0)
    flip_y: bool = False


@dataclass
class LightSettings:
    """A key light, an opposing fill and a hemispherical ambient term."""

    azimuth_deg: float = 40.0
    elevation_deg: float = 35.0
    color: Color = (1.0, 0.98, 0.95)
    intensity: float = 1.0
    fill_intensity: float = 0.25
    ambient_color: Color = (0.42, 0.47, 0.55)
    ambient_intensity: float = 0.30
    #: When true the light stays fixed relative to the camera, like a head lamp.
    follow_camera: bool = True


@dataclass
class SurfaceSettings:
    """Material parameters shared by the analytic shading modes."""

    diffuse_color: Color = (0.72, 0.70, 0.68)
    specular_color: Color = (1.0, 1.0, 1.0)
    specular_level: float = 0.4
    shininess: float = 32.0
    metalness: float = 0.0
    roughness: float = 0.40
    reflection_color: Color = (1.0, 1.0, 1.0)


@dataclass
class QualitySettings:
    """Soft shadows and ambient occlusion for the high-quality mode.

    Both are screen- and light-space approximations rather than traced rays:
    the point is a reference view that stays interactive while you turn it.
    """

    #: How dark a fully shadowed surface goes, 0 (off) to 1.
    shadow_strength: float = 0.55
    #: Radius of the shadow-map blur, in shadow texels.  Larger reads softer.
    shadow_softness: float = 2.0
    #: Depth offset that keeps a lit surface from shadowing itself.
    shadow_bias: float = 0.0022
    #: Occlusion sampling radius, as a share of the scene radius.
    ao_radius: float = 0.09
    #: How strongly cavities darken, 0 (off) to 1.
    ao_intensity: float = 0.85
    show_shadows: bool = True
    show_occlusion: bool = True


@dataclass
class RenderSettings:
    """Everything the viewport needs in order to draw a frame."""

    shading_mode: ShadingMode = ShadingMode.MATCAP
    matcap: MatcapSettings = field(default_factory=MatcapSettings)
    light: LightSettings = field(default_factory=LightSettings)
    surface: SurfaceSettings = field(default_factory=SurfaceSettings)
    quality: QualitySettings = field(default_factory=QualitySettings)
    section: SectionSettings = field(default_factory=SectionSettings)
    pedestal: PedestalSettings = field(default_factory=PedestalSettings)
    matcap_path: str | None = None
    flat_shading: bool = False
    show_wireframe: bool = False
    wireframe_color: Color = (0.08, 0.09, 0.11)
    background_top: Color = (0.26, 0.27, 0.30)
    background_bottom: Color = (0.10, 0.10, 0.12)


@dataclass
class NavigationSettings:
    """How mouse gestures drive the camera."""

    #: Orbit increment, in degrees, while Shift is held.  Snapping to round
    #: angles makes it possible to come back to the same three-quarter view.
    snap_angle_deg: float = 15.0
