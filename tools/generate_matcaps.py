"""Render the bundled matcap set.

Each preset is evaluated analytically over the hemisphere that a matcap
encodes: for every pixel inside the unit disc the surface normal is
``(x, y, sqrt(1 - x^2 - y^2))`` in view space, so a simple two-light shading
model produces a usable sphere image.  Pixels outside the disc reuse the
silhouette colour, which keeps the texture well defined if a wide field of
view pushes a lookup past the edge.

Run with::

    python tools/generate_matcaps.py
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PySide6.QtGui import QImage  # noqa: E402

from refview.paths import matcap_dir  # noqa: E402

Color = tuple[float, float, float]


@dataclass(frozen=True)
class MatcapPreset:
    """Parameters of one analytic sphere render."""

    name: str
    base: Color
    key_direction: Color = (-0.45, 0.55, 0.70)
    key_color: Color = (1.0, 0.97, 0.92)
    key_intensity: float = 1.0
    fill_direction: Color = (0.65, -0.25, 0.60)
    fill_color: Color = (0.62, 0.70, 0.85)
    fill_intensity: float = 0.35
    ambient: Color = (0.16, 0.17, 0.20)
    specular_color: Color = (1.0, 1.0, 1.0)
    specular_power: float = 40.0
    specular_intensity: float = 0.25
    rim_color: Color = (0.75, 0.82, 1.0)
    rim_intensity: float = 0.20
    rim_power: float = 3.0
    gamma: float = 1.0


PRESETS: tuple[MatcapPreset, ...] = (
    MatcapPreset(
        name="clay_terracotta",
        base=(0.72, 0.38, 0.28),
        specular_intensity=0.10,
        specular_power=18.0,
        rim_intensity=0.14,
    ),
    MatcapPreset(
        name="clay_grey",
        base=(0.55, 0.55, 0.57),
        specular_intensity=0.08,
        specular_power=14.0,
        rim_intensity=0.16,
    ),
    MatcapPreset(
        name="studio_white",
        base=(0.82, 0.81, 0.79),
        key_intensity=0.9,
        specular_intensity=0.22,
        specular_power=48.0,
        rim_intensity=0.22,
    ),
    MatcapPreset(
        name="wax_skin",
        base=(0.86, 0.68, 0.60),
        fill_color=(0.85, 0.45, 0.40),
        fill_intensity=0.45,
        specular_intensity=0.18,
        specular_power=28.0,
        rim_color=(1.0, 0.72, 0.62),
        rim_intensity=0.28,
    ),
    MatcapPreset(
        name="jade",
        base=(0.24, 0.52, 0.42),
        fill_color=(0.35, 0.85, 0.70),
        fill_intensity=0.5,
        specular_intensity=0.35,
        specular_power=64.0,
        rim_color=(0.65, 1.0, 0.88),
        rim_intensity=0.30,
    ),
    MatcapPreset(
        name="steel",
        base=(0.32, 0.34, 0.38),
        key_intensity=1.2,
        specular_intensity=0.85,
        specular_power=120.0,
        rim_color=(0.85, 0.90, 1.0),
        rim_intensity=0.35,
    ),
    MatcapPreset(
        name="charcoal",
        base=(0.18, 0.18, 0.20),
        ambient=(0.07, 0.07, 0.09),
        specular_intensity=0.30,
        specular_power=32.0,
        rim_color=(0.55, 0.62, 0.78),
        rim_intensity=0.40,
    ),
)


def _normalize(vector: Color) -> np.ndarray:
    array = np.asarray(vector, dtype=np.float64)
    return array / max(float(np.linalg.norm(array)), 1e-12)


def render(preset: MatcapPreset, size: int = 512) -> np.ndarray:
    """Return an ``(size, size, 4)`` uint8 image for one preset."""
    axis = np.linspace(-1.0, 1.0, size)
    x, y = np.meshgrid(axis, -axis)

    # Outside the disc, clamp onto the silhouette so the texture stays defined.
    radius = np.sqrt(x * x + y * y)
    scale = np.where(radius > 1.0, 1.0 / np.maximum(radius, 1e-9), 1.0)
    nx, ny = x * scale, y * scale
    nz = np.sqrt(np.clip(1.0 - nx * nx - ny * ny, 0.0, 1.0))
    normal = np.stack([nx, ny, nz], axis=-1)
    view = np.array([0.0, 0.0, 1.0])

    color = np.asarray(preset.ambient, dtype=np.float64) * np.asarray(preset.base)
    for direction, light_color, intensity in (
        (preset.key_direction, preset.key_color, preset.key_intensity),
        (preset.fill_direction, preset.fill_color, preset.fill_intensity),
    ):
        light = _normalize(direction)
        ndl = np.clip(normal @ light, 0.0, 1.0)
        color = color + (
            np.asarray(preset.base) * np.asarray(light_color) * (ndl * intensity)[..., None]
        )
        half = _normalize(np.asarray(light) + view)
        ndh = np.clip(normal @ half, 0.0, 1.0)
        specular = ndh**preset.specular_power * preset.specular_intensity * intensity
        color = color + np.asarray(preset.specular_color) * specular[..., None]

    rim = np.clip(1.0 - nz, 0.0, 1.0) ** preset.rim_power * preset.rim_intensity
    color = color + np.asarray(preset.rim_color) * rim[..., None]

    color = np.clip(color, 0.0, 1.0) ** preset.gamma
    alpha = np.ones((size, size, 1))
    return (np.concatenate([color, alpha], axis=-1) * 255).astype(np.uint8)


def save(pixels: np.ndarray, path: Path) -> None:
    height, width = pixels.shape[:2]
    image = QImage(pixels.tobytes(), width, height, width * 4, QImage.Format.Format_RGBA8888)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not image.save(str(path)):
        raise RuntimeError(f"Could not write {path}")


def main() -> None:
    target = matcap_dir()
    for preset in PRESETS:
        path = target / f"{preset.name}.png"
        save(render(preset), path)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
