"""A turntable-style disc the model can stand on.

A ground plane gives the eye somewhere to read height and contact from, which
is exactly what is missing when a scan floats in an empty view.  The disc is
generated as an ordinary mesh, so it shades, casts and receives shadows with
everything else instead of needing a special case in the renderer.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .mesh import Bounds, Mesh

Color = tuple[float, float, float]


@dataclass
class PedestalSettings:
    """Where the disc sits and how big it is."""

    enabled: bool = False
    #: Sit the top face at the model's lowest vertex rather than at ``level``.
    snap_to_lowest: bool = True
    #: Height of the top face when :attr:`snap_to_lowest` is off, in scene units.
    level: float = 0.0
    #: Diameter as a multiple of the model's widest horizontal span.
    diameter: float = 1.35
    #: Thickness as a share of the scene radius.
    thickness: float = 0.06
    #: Segments around the rim.  64 reads as round at any sensible zoom.
    sides: int = 64
    color: Color = (0.34, 0.35, 0.38)

    def top_level(self, bounds: Bounds) -> float:
        """Height of the disc's top face for the current model."""
        return float(bounds.minimum[1]) if self.snap_to_lowest else float(self.level)


def build_pedestal(bounds: Bounds, settings: PedestalSettings) -> Mesh | None:
    """Build the disc for a model with these ``bounds``, or ``None`` if off."""
    if not settings.enabled:
        return None

    footprint = float(max(bounds.size[0], bounds.size[2], bounds.radius * 0.5))
    radius = max(footprint * 0.5 * settings.diameter, 1e-4)
    thickness = max(bounds.radius * settings.thickness, 1e-5)
    top = settings.top_level(bounds)
    centre = np.asarray(bounds.center, dtype=np.float64)
    return _disc(
        centre=np.array([centre[0], top, centre[2]]),
        radius=radius,
        thickness=thickness,
        sides=max(int(settings.sides), 8),
    )


def _disc(centre: np.ndarray, radius: float, thickness: float, sides: int) -> Mesh:
    """A closed cylinder with hard edges: separate vertices per face group."""
    angles = np.linspace(0.0, 2.0 * np.pi, sides, endpoint=False)
    rim = np.stack((np.cos(angles) * radius, np.zeros(sides), np.sin(angles) * radius), axis=1)
    top = rim + centre
    bottom = top - np.array([0.0, thickness, 0.0])
    following = (np.arange(sides) + 1) % sides

    positions = [top, bottom, centre[None, :], centre[None, :] - [0.0, thickness, 0.0]]
    normals = [
        np.tile((0.0, 1.0, 0.0), (sides, 1)),
        np.tile((0.0, -1.0, 0.0), (sides, 1)),
        np.array([[0.0, 1.0, 0.0]]),
        np.array([[0.0, -1.0, 0.0]]),
    ]
    side_normals = rim / max(radius, 1e-9)
    positions += [top, bottom]
    normals += [side_normals, side_normals]

    top_hub, bottom_hub = 2 * sides, 2 * sides + 1
    wall_top, wall_bottom = 2 * sides + 2, 3 * sides + 2
    indices = np.concatenate(
        (
            # Caps, fanned from a hub vertex; the underside winds the other way.
            np.stack((np.full(sides, top_hub), following, np.arange(sides)), axis=1),
            np.stack(
                (np.full(sides, bottom_hub), sides + np.arange(sides), sides + following), axis=1
            ),
            # Wall, two triangles per segment.
            np.stack(
                (
                    wall_top + np.arange(sides),
                    wall_bottom + following,
                    wall_bottom + np.arange(sides),
                ),
                axis=1,
            ),
            np.stack(
                (wall_top + np.arange(sides), wall_top + following, wall_bottom + following),
                axis=1,
            ),
        )
    )
    return Mesh(
        np.concatenate(positions).astype(np.float32),
        np.concatenate(normals).astype(np.float32),
        indices.astype(np.uint32),
        name="pedestal",
    )
