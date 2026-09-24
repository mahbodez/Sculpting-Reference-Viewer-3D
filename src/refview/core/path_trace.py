"""What the path tracer is asked to make: its size, its sampling, its look.

The viewport's own settings (:class:`~refview.core.settings.RenderSettings`)
say what the model is made of and how it is lit, and the path tracer reads
those as they are: the Human Skin sliders, the Surface colours, the studio
key and the HDRI all mean the same in a render as on screen.  These settings
say only what a render engine adds on top -- how large a picture, how many
samples, how many bounces, how the light is turned into pixel values -- and
they are kept apart on purpose: a change here must not restart the viewport's
own skin refinement, which is keyed on everything in ``RenderSettings``.

Numbers are in the artist's units: samples per pixel, bounces, seconds,
stops of exposure.  Lengths (the lens aperture) are fractions of the scene's
radius, as the skin's are, because a model has no reliable units.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, fields, is_dataclass, replace
from enum import Enum

from .settings import Color, RenderSettings, ShadingMode


class RenderMethod(str, Enum):
    """How the picture is filled in."""

    PROGRESSIVE = "progressive"
    BUCKET = "bucket"

    @property
    def label(self) -> str:
        return {RenderMethod.PROGRESSIVE: "Progressive", RenderMethod.BUCKET: "Bucket"}[self]

    @property
    def note(self) -> str:
        return {
            RenderMethod.PROGRESSIVE: (
                "The whole picture at once, a few samples at a time: noisy at first,\n"
                "clearer with every pass. Good for judging the light early."
            ),
            RenderMethod.BUCKET: (
                "One square at a time, each finished before the next begins.\n"
                "Uses a little less memory traffic and shows finished detail early."
            ),
        }[self]


class BucketOrder(str, Enum):
    """Which bucket is rendered next."""

    SPIRAL = "spiral"
    HILBERT = "hilbert"
    ROWS = "rows"
    RANDOM = "random"

    @property
    def label(self) -> str:
        return {
            BucketOrder.SPIRAL: "Spiral from centre",
            BucketOrder.HILBERT: "Hilbert curve",
            BucketOrder.ROWS: "Rows, top down",
            BucketOrder.RANDOM: "Random",
        }[self]


class PixelFilter(str, Enum):
    """How the samples in and around a pixel are weighed."""

    BOX = "box"
    GAUSSIAN = "gaussian"
    BLACKMAN_HARRIS = "blackman_harris"

    @property
    def label(self) -> str:
        return {
            PixelFilter.BOX: "Box (sharpest, can alias)",
            PixelFilter.GAUSSIAN: "Gaussian (soft)",
            PixelFilter.BLACKMAN_HARRIS: "Blackman-Harris (balanced)",
        }[self]


class ViewTransform(str, Enum):
    """How scene light becomes pixel values."""

    AUTO = "auto"
    STANDARD = "standard"
    NEUTRAL = "neutral"
    FILMIC = "filmic"
    REINHARD = "reinhard"

    @property
    def label(self) -> str:
        return {
            ViewTransform.AUTO: "Auto (match the viewport)",
            ViewTransform.STANDARD: "Standard (clip)",
            ViewTransform.NEUTRAL: "Neutral (PBR Neutral)",
            ViewTransform.FILMIC: "Filmic (ACES fit)",
            ViewTransform.REINHARD: "Reinhard (as Human Skin)",
        }[self]

    def resolved(self, skin: bool) -> ViewTransform:
        """What :attr:`AUTO` stands for: the skin's own curve in Human Skin."""
        if self is not ViewTransform.AUTO:
            return self
        return ViewTransform.REINHARD if skin else ViewTransform.NEUTRAL


class OutputFormat(str, Enum):
    """What a saved render is written as."""

    PNG8 = "png8"
    PNG16 = "png16"
    EXR_HALF = "exr_half"
    EXR_FLOAT = "exr_float"

    @property
    def label(self) -> str:
        return {
            OutputFormat.PNG8: "PNG, 8-bit",
            OutputFormat.PNG16: "PNG, 16-bit",
            OutputFormat.EXR_HALF: "OpenEXR, half float",
            OutputFormat.EXR_FLOAT: "OpenEXR, full float",
        }[self]

    @property
    def suffix(self) -> str:
        return ".exr" if self in (OutputFormat.EXR_HALF, OutputFormat.EXR_FLOAT) else ".png"

    @property
    def linear(self) -> bool:
        """Whether the file keeps scene light rather than display values."""
        return self in (OutputFormat.EXR_HALF, OutputFormat.EXR_FLOAT)


class DenoiserBackend(str, Enum):
    """Which denoiser cleans up a render."""

    AUTO = "auto"
    OIDN = "oidn"
    OPTIX = "optix"
    BUILTIN = "builtin"

    @property
    def label(self) -> str:
        return {
            DenoiserBackend.AUTO: "Auto",
            DenoiserBackend.OIDN: "Intel Open Image Denoise",
            DenoiserBackend.OPTIX: "NVIDIA OptiX",
            DenoiserBackend.BUILTIN: "Built-in (edge-aware blur)",
        }[self]


class DenoiserDevice(str, Enum):
    """Where Open Image Denoise runs."""

    AUTO = "auto"
    GPU = "gpu"
    CPU = "cpu"

    @property
    def label(self) -> str:
        return {
            DenoiserDevice.AUTO: "Fastest available",
            DenoiserDevice.GPU: "GPU",
            DenoiserDevice.CPU: "CPU",
        }[self]


class DenoiserQuality(str, Enum):
    HIGH = "high"
    BALANCED = "balanced"
    FAST = "fast"

    @property
    def label(self) -> str:
        return self.value.capitalize()


class NeuralStyle(str, Enum):
    """The look DLSS 5 Neural Rendering aims for."""

    DEFAULT = "default"
    NATURAL = "natural"
    CINEMATIC = "cinematic"

    @property
    def label(self) -> str:
        return self.value.capitalize()

    @property
    def code(self) -> int:
        """The number the engine knows the style by."""
        return {NeuralStyle.DEFAULT: 0, NeuralStyle.NATURAL: 1, NeuralStyle.CINEMATIC: 2}[self]


@dataclass
class OutputSettings:
    """How large the picture is and how it is saved."""

    width: int = 1920
    height: int = 1080
    #: A percentage of the size above, for a quick look at a large frame.
    scale: int = 100
    lock_aspect: bool = True
    #: The size preset last chosen, by name; see ``OUTPUT_SIZES``.
    size_preset: str = "Full HD 1080p"
    format: OutputFormat = OutputFormat.PNG8
    #: Leave the background out, for compositing.
    transparent: bool = False


@dataclass
class SafeFrameSettings:
    """The frame drawn over the viewport to show what a render will hold."""

    show: bool = False
    #: How dark the part of the view outside the frame is shaded.
    dim: float = 0.55
    action_safe: bool = True
    title_safe: bool = True
    #: The share of the frame each safe area keeps, per side.
    action: float = 0.93
    title: float = 0.90
    #: Print the output size in the frame's corner.
    label: bool = True


@dataclass
class SamplingSettings:
    """How many light paths each pixel averages, and when to stop."""

    samples: int = 512
    #: The fewest any pixel takes, however quiet it looks.
    min_samples: int = 32
    #: Stop sampling a pixel once its noise falls below this; nought for never.
    noise_threshold: float = 0.01
    #: Stop the render after this many seconds; nought for no limit.
    time_limit_s: float = 0.0
    #: Changes the noise pattern, not how much of it there is.
    seed: int = 0


@dataclass
class LightPathSettings:
    """How far each path goes."""

    max_bounces: int = 8
    diffuse: int = 4
    glossy: int = 4
    transmission: int = 8
    #: The brightest a sample of direct light may be; nought for no limit.
    clamp_direct: float = 0.0
    #: The brightest a sample of bounced light may be; nought for no limit.
    clamp_indirect: float = 10.0
    #: Blur sharp reflections seen only by bounced light, which is where
    #: fireflies come from.
    filter_glossy: float = 0.5
    #: Let bounced light focus through reflections.
    caustics: bool = False


@dataclass
class FilmSettings:
    filter: PixelFilter = PixelFilter.BLACKMAN_HARRIS
    #: The filter's width, in pixels.
    filter_width: float = 1.5


@dataclass
class ColorSettings:
    view_transform: ViewTransform = ViewTransform.AUTO
    #: Stops, on top of the Human Skin exposure in that mode.
    exposure: float = 0.0
    gamma: float = 1.0
    #: Pushes midtones apart (positive) or together (negative).
    contrast: float = 0.0


@dataclass
class DenoiseSettings:
    #: Clean the finished render.
    final: bool = True
    #: Clean the rendered viewport as it refines.
    preview: bool = True
    backend: DenoiserBackend = DenoiserBackend.AUTO
    device: DenoiserDevice = DenoiserDevice.AUTO
    quality: DenoiserQuality = DenoiserQuality.HIGH
    use_albedo: bool = True
    use_normal: bool = True
    #: Treat the albedo and normal passes as noisy too (they are, where there
    #: is depth of field or ghosting) and clean them first.
    prefilter_guides: bool = True
    #: How much of the denoised picture is kept over the noisy one.
    mix: float = 1.0
    #: Passes of the built-in filter; each doubles its reach.
    atrous_passes: int = 5


@dataclass
class NeuralSettings:
    """NVIDIA DLSS 5 Neural Rendering, run on the developed picture after denoising.

    The numbers are the engine's own, with its defaults; see
    :mod:`refview.trace.neural`.
    """

    #: Enhance the finished render.
    final: bool = False
    #: Enhance the rendered viewport as it refines.
    preview: bool = False
    style: NeuralStyle = NeuralStyle.DEFAULT
    #: How far the picture is taken towards the model's version of it.
    intensity: float = 1.0
    #: Times the model is run over its own result; each goes further.
    passes: int = 1
    #: Local contrast of light and shade.
    local_tone: float = 1.0
    #: Fine surface detail.
    local_structure: float = 1.0
    #: Detail the model adds to skin; -1 leaves it to the model.
    skin_structure: float = -1.0
    #: How much of the model's colour is kept, over the picture's own.
    color_strength: float = 1.0
    #: How much of the picture's own brightness is kept.
    tone_preservation: float = 0.0
    #: How far faces and skin are kept from change.
    face_skin_protection: float = 0.0
    #: Let the model decide where to work, and leave the rest.
    auto_mask: bool = False


@dataclass
class LensSettings:
    depth_of_field: bool = False
    #: Keep the orbit target in focus, wherever the camera goes.
    focus_on_target: bool = True
    #: The focus distance when not on the target, as a share of the scene radius.
    focus_distance: float = 2.0
    #: The aperture radius, as a share of the scene radius.
    aperture: float = 0.02
    #: Blades of the iris; nought for a round one.
    blades: int = 0


@dataclass
class PerformanceSettings:
    method: RenderMethod = RenderMethod.PROGRESSIVE
    #: A bucket's side, in pixels.
    bucket_size: int = 32
    bucket_order: BucketOrder = BucketOrder.SPIRAL
    #: Render threads; nought for all the cores but one.
    threads: int = 0
    #: Run below normal priority, so the rest of the computer stays responsive.
    low_priority: bool = True


@dataclass
class PreviewSettings:
    """The rendered viewport."""

    #: The share of the viewport's pixels traced once it is still.
    resolution: float = 0.5
    samples: int = 256
    noise_threshold: float = 0.02
    #: The share traced while the view is being turned.
    interactive_resolution: float = 0.25


@dataclass
class ClaySettings:
    """The material of a model in a mode that has none: Matcap, Normals, Contour."""

    color: Color = (0.75, 0.72, 0.69)
    roughness: float = 0.55
    specular: float = 0.3


@dataclass
class PathTraceSettings:
    output: OutputSettings = field(default_factory=OutputSettings)
    safe_frame: SafeFrameSettings = field(default_factory=SafeFrameSettings)
    sampling: SamplingSettings = field(default_factory=SamplingSettings)
    paths: LightPathSettings = field(default_factory=LightPathSettings)
    film: FilmSettings = field(default_factory=FilmSettings)
    color: ColorSettings = field(default_factory=ColorSettings)
    denoise: DenoiseSettings = field(default_factory=DenoiseSettings)
    neural: NeuralSettings = field(default_factory=NeuralSettings)
    lens: LensSettings = field(default_factory=LensSettings)
    performance: PerformanceSettings = field(default_factory=PerformanceSettings)
    preview: PreviewSettings = field(default_factory=PreviewSettings)
    clay: ClaySettings = field(default_factory=ClaySettings)
    #: How wide the studio key and fill are, in degrees, outside Human Skin
    #: (which has its own): nought is a sharp-shadowed point, wider is softer.
    light_size_deg: float = 6.0
    #: The sampling preset last applied; "Custom" once anything it sets is edited.
    preset: str = "Final"

    def bounded(self) -> PathTraceSettings:
        """Keep loaded settings finite and inside what the panel and the tracer allow."""
        result = _copy(self)
        defaults = PathTraceSettings()
        for name, (low, high) in PATH_TRACE_RANGES.items():
            owner_name, _, attribute = name.rpartition(".")
            owner = _resolve(result, owner_name)
            default_value = getattr(_resolve(defaults, owner_name), attribute)
            try:
                value = float(getattr(owner, attribute))
            except (TypeError, ValueError):
                value = float(default_value)
            if not math.isfinite(value):
                value = float(default_value)
            value = min(high, max(low, value))
            setattr(owner, attribute, int(round(value)) if isinstance(default_value, int)
                    and not isinstance(default_value, bool) else value)
        clay = result.clay
        color = clay.color
        try:
            ok = len(color) == 3 and all(math.isfinite(float(v)) for v in color)
        except TypeError:
            ok = False
        if not ok:
            color = defaults.clay.color
        clay.color = tuple(min(1.0, max(0.0, float(v))) for v in color)
        paths = result.paths
        paths.diffuse = min(paths.diffuse, paths.max_bounces)
        paths.glossy = min(paths.glossy, paths.max_bounces)
        paths.transmission = min(paths.transmission, paths.max_bounces)
        result.sampling.min_samples = min(result.sampling.min_samples, result.sampling.samples)
        if not isinstance(result.preset, str):
            result.preset = CUSTOM_PRESET
        return result


def _copy(settings):
    """A deep copy of nested dataclasses, cheap enough for every render."""
    changes = {}
    for f in fields(settings):
        value = getattr(settings, f.name)
        if is_dataclass(value):
            changes[f.name] = _copy(value)
    return replace(settings, **changes)


def _resolve(settings, path: str):
    for part in path.split(".") if path else ():
        settings = getattr(settings, part)
    return settings


#: Every number the tracer reads, and the range it is kept in.  The panel
#: builds its sliders from the same table.
PATH_TRACE_RANGES: dict[str, tuple[float, float]] = {
    "output.width": (16, 7680),
    "output.height": (16, 7680),
    "output.scale": (10, 200),
    "safe_frame.dim": (0.0, 1.0),
    "safe_frame.action": (0.5, 1.0),
    "safe_frame.title": (0.5, 1.0),
    "sampling.samples": (1, 16384),
    "sampling.min_samples": (1, 4096),
    "sampling.noise_threshold": (0.0, 0.5),
    "sampling.time_limit_s": (0.0, 86400.0),
    "sampling.seed": (0, 1_000_000),
    "paths.max_bounces": (0, 64),
    "paths.diffuse": (0, 64),
    "paths.glossy": (0, 64),
    "paths.transmission": (0, 64),
    "paths.clamp_direct": (0.0, 1000.0),
    "paths.clamp_indirect": (0.0, 1000.0),
    "paths.filter_glossy": (0.0, 5.0),
    "film.filter_width": (0.5, 4.0),
    "color.exposure": (-10.0, 10.0),
    "color.gamma": (0.2, 5.0),
    "color.contrast": (-1.0, 1.0),
    "denoise.mix": (0.0, 1.0),
    "denoise.atrous_passes": (1, 8),
    "neural.intensity": (0.0, 2.0),
    "neural.passes": (1, 4),
    "neural.local_tone": (0.0, 2.0),
    "neural.local_structure": (0.0, 2.0),
    "neural.skin_structure": (-1.0, 2.0),
    "neural.color_strength": (0.0, 1.0),
    "neural.tone_preservation": (0.0, 1.0),
    "neural.face_skin_protection": (0.0, 1.0),
    "lens.focus_distance": (0.01, 100.0),
    "lens.aperture": (0.0, 1.0),
    "lens.blades": (0, 12),
    "performance.bucket_size": (8, 256),
    "performance.threads": (0, 256),
    "preview.resolution": (0.1, 1.0),
    "preview.samples": (1, 16384),
    "preview.noise_threshold": (0.0, 0.5),
    "preview.interactive_resolution": (0.05, 1.0),
    "clay.roughness": (0.02, 1.0),
    "clay.specular": (0.0, 1.0),
    "light_size_deg": (0.0, 30.0),
}

CUSTOM_PRESET = "Custom"


@dataclass(frozen=True)
class PathTracePreset:
    """What a preset sets: how much work a render does, never its size or look."""

    sampling: SamplingSettings
    paths: LightPathSettings
    denoise_final: bool

    def applied_to(self, settings: PathTraceSettings, name: str) -> PathTraceSettings:
        result = _copy(settings)
        result.sampling = replace(self.sampling, seed=settings.sampling.seed)
        result.paths = replace(self.paths)
        result.denoise.final = self.denoise_final
        result.preset = name
        return result

    def matches(self, settings: PathTraceSettings) -> bool:
        return (
            replace(settings.sampling, seed=0) == replace(self.sampling, seed=0)
            and settings.paths == self.paths
            and settings.denoise.final == self.denoise_final
        )


PATH_TRACE_PRESETS: dict[str, PathTracePreset] = {
    "Preview": PathTracePreset(
        SamplingSettings(samples=32, min_samples=8, noise_threshold=0.05),
        LightPathSettings(max_bounces=4, diffuse=2, glossy=2, transmission=4, clamp_indirect=5.0,
                          filter_glossy=1.0),
        denoise_final=True,
    ),
    "Draft": PathTracePreset(
        SamplingSettings(samples=128, min_samples=16, noise_threshold=0.03),
        LightPathSettings(max_bounces=6, diffuse=3, glossy=3, transmission=6, clamp_indirect=10.0,
                          filter_glossy=0.75),
        denoise_final=True,
    ),
    "Final": PathTracePreset(
        SamplingSettings(samples=512, min_samples=32, noise_threshold=0.01),
        LightPathSettings(max_bounces=8, diffuse=4, glossy=4, transmission=8, clamp_indirect=10.0,
                          filter_glossy=0.5),
        denoise_final=True,
    ),
    "Production": PathTracePreset(
        SamplingSettings(samples=2048, min_samples=64, noise_threshold=0.005),
        LightPathSettings(max_bounces=12, diffuse=6, glossy=6, transmission=12,
                          clamp_indirect=0.0, filter_glossy=0.25),
        denoise_final=False,
    ),
}


def mode_note(render: RenderSettings) -> str:
    """How the current shading mode renders, in a line for the Render panel."""
    mode = render.shading_mode
    if mode is ShadingMode.HUMAN_SKIN:
        return "Human Skin: the full skin, with traced scattering and backlight."
    if mode is ShadingMode.PBR:
        return "PBR: the Surface colour, metalness and roughness."
    if mode in (ShadingMode.PHONG, ShadingMode.BLINN_PHONG, ShadingMode.HIGH_QUALITY):
        return f"{mode.label}: the Surface colour, with a gloss matched to its shininess."
    if mode is ShadingMode.LAMBERT:
        return "Lambert: the Surface colour, matte."
    return f"{mode.label} is a way of looking, not a material: the model renders as clay."
