"""Artist-facing skin parameters, in sRGB colours and relative scene units.

Presets are starting palettes, not biological categories. Radius and pore size
are fractions of the model's bounding radius because OBJ references have no
reliable units. Surface detail, tone variation, blood and fuzz are the knobs
that separate skin from wax: relief for the light to catch, unevenness in the
pigment, red where the dermis shows through, and a soft rim of vellus hair.
The marks -- blemishes, freckles, moles and acne -- are what separate skin
from *perfect* skin, and where they fall is the body's business: see
:mod:`refview.core.body_regions`, whose settings ride along here.
"""

from dataclasses import dataclass, field, replace

from .body_regions import BodyRegionSettings


@dataclass
class SkinSettings:
    color: tuple[float, float, float] = (0.76, 0.53, 0.42)
    roughness: float = 0.48
    specular: float = 1.0
    oiliness: float = 0.12
    sss: float = 0.55
    radius: float = 0.004
    scatter_color: tuple[float, float, float] = (1.0, 0.38, 0.18)
    transmission: float = 0.35
    detail: float = 0.55
    pore_size: float = 0.0028
    mottle: float = 0.35
    blood: float = 0.35
    veins: float = 0.2
    fuzz: float = 0.2
    #: Patches of irritated, reddened and of dry, duller skin, at a scale
    #: well above the pores.
    blemishes: float = 0.0
    #: How thickly the small light-brown dots fall.
    freckles: float = 0.0
    #: How many moles: dark, a few pores across, faintly raised.
    nevi: float = 0.0
    #: How many red papules, raised and shining, some come to a head.
    acne: float = 0.0
    #: Where on the body each of those falls, and how much of it.
    regions: BodyRegionSettings = field(default_factory=BodyRegionSettings)
    light_size: float = 6.0
    exposure: float = 1.0
    indirect: float = 1.0
    progressive: bool = True
    samples: int = 64
    resolution: float = 0.75

    def bounded(self) -> "SkinSettings":
        """Keep loaded settings finite and inside the supported shader domain."""
        import math

        result = replace(self)
        defaults = SkinSettings()
        for name, (low, high) in SKIN_RANGES.items():
            value = float(getattr(self, name))
            if not math.isfinite(value):
                value = getattr(defaults, name)
            setattr(result, name, min(high, max(low, value)))
        result.samples = int(result.samples)
        regions = self.regions
        if not isinstance(regions, BodyRegionSettings):
            regions = BodyRegionSettings()
        result.regions = regions.bounded()
        for name in ("color", "scatter_color"):
            color = getattr(self, name)
            if len(color) != 3 or not all(math.isfinite(v) for v in color):
                color = getattr(defaults, name)
            setattr(result, name, tuple(min(1.0, max(0.0, v)) for v in color))
        return result


SKIN_RANGES = {
    "roughness": (0.12, 1.0), "specular": (0.0, 2.0), "oiliness": (0.0, 1.0),
    "sss": (0.0, 1.0), "radius": (0.001, 0.08), "transmission": (0.0, 1.0),
    "detail": (0.0, 2.0), "pore_size": (0.0005, 0.03), "mottle": (0.0, 1.0),
    "blood": (0.0, 1.0), "veins": (0.0, 1.0), "fuzz": (0.0, 1.0),
    "blemishes": (0.0, 1.0), "freckles": (0.0, 1.0), "nevi": (0.0, 1.0), "acne": (0.0, 1.0),
    "light_size": (0.0, 30.0), "exposure": (-3.0, 3.0), "indirect": (0.0, 2.0),
    "samples": (8, 1024), "resolution": (0.25, 1.0),
}

SKIN_PRESETS = {
    "Fair / rosy": SkinSettings(color=(0.88, 0.67, 0.58), sss=0.65, blood=0.55, mottle=0.45),
    "Light / golden": SkinSettings(color=(0.80, 0.61, 0.43), sss=0.58, blood=0.40),
    "Medium / warm": SkinSettings(),
    "Tan / olive": SkinSettings(color=(0.61, 0.45, 0.30), sss=0.50, blood=0.28,
                                scatter_color=(1.0, 0.34, 0.16)),
    "Brown / warm": SkinSettings(color=(0.47, 0.29, 0.19), sss=0.43, blood=0.20,
                                 scatter_color=(1.0, 0.30, 0.14), oiliness=0.18),
    "Deep / neutral": SkinSettings(color=(0.29, 0.18, 0.13), sss=0.36, blood=0.12,
                                   mottle=0.25, scatter_color=(1.0, 0.26, 0.12),
                                   oiliness=0.24, roughness=0.42),
}
