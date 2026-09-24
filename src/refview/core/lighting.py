"""Which lights are on for a frame and where they point.

:func:`light_rig` settles, once a frame, which lights are on and where they
point: the studio key and fill, the HDRI, or both, and the one direction the
shadow map is cast from -- the key's when there is a key, the map's dominant
light when the map is all there is.  The viewport's shaders read it, and so
does the CPU path tracer, which is why it lives here rather than beside the
GL code: two renderers that settle the lights the same way cannot disagree
about where the key is.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .environment import EnvironmentMap, rotation_y
from .linalg import spherical_direction
from .settings import RenderSettings


@dataclass
class LightRig:
    """Which lights are on this frame and where they point.

    Directions point from the surface to the light.  ``key`` and ``fill``
    are in view space, as the shaders want them; ``shadow`` is in world
    space, for the shadow map, or ``None`` when nothing casts.
    """

    key: np.ndarray
    fill: np.ndarray
    key_intensity: float
    fill_intensity: float
    ambient_intensity: float
    shadow: np.ndarray | None
    environment: bool
    env_from_world: np.ndarray
    #: Radiance multiplier: the strength over the map's own brightness.
    env_scale: float
    #: The map's dominant light, in view space, and its irradiance before
    #: ``env_scale``; the shaders take its share out where it is shadowed.
    sun: np.ndarray
    sun_color: np.ndarray
    #: Whether the shadow map was cast from the map's dominant light.
    env_shadow: bool


def environment_matrix(settings: RenderSettings, view: np.ndarray) -> np.ndarray:
    """World directions into the map's frame, for this view."""
    light = settings.light
    turn = rotation_y(-light.environment_rotation_deg)
    if light.follow_camera:
        return turn @ np.asarray(view, dtype=np.float64)[:3, :3]
    return turn


def light_rig(
    settings: RenderSettings, view: np.ndarray, environment: EnvironmentMap | None
) -> LightRig:
    """Settle the lights for one frame."""
    light = settings.light
    rotation = np.asarray(view, dtype=np.float64)[:3, :3]
    key = spherical_direction(light.azimuth_deg, light.elevation_deg)
    fill = spherical_direction(light.azimuth_deg + 180.0, light.elevation_deg * 0.35 - 10.0)
    if not light.follow_camera:
        key, fill = rotation @ key, rotation @ fill
    key_world = rotation.T @ key
    mode = light.mode
    # A matcap, the normals and the contour paper carry their own light.
    lit_by_map = (
        mode.uses_environment and environment is not None and settings.shading_mode.uses_lighting
    )
    studio = mode.uses_studio or not lit_by_map
    matrix = environment_matrix(settings, view)
    sun_world = np.array([0.0, 1.0, 0.0])
    sun_color = np.zeros(3)
    scale = 0.0
    if lit_by_map:
        sun_world = matrix.T @ np.asarray(environment.sun_direction, dtype=np.float64)
        sun_color = np.asarray(environment.sun_color, dtype=np.float64)
        scale = max(float(light.environment_strength), 0.0) * environment.normalization
    shadow: np.ndarray | None = None
    env_shadow = False
    if studio and light.intensity > 0.0:
        shadow = key_world
    elif lit_by_map and light.environment_shadows and scale > 0.0:
        shadow = sun_world
        env_shadow = True
    return LightRig(
        key=np.asarray(key, dtype=np.float64),
        fill=np.asarray(fill, dtype=np.float64),
        key_intensity=float(light.intensity) if studio else 0.0,
        fill_intensity=float(light.fill_intensity) if studio else 0.0,
        ambient_intensity=float(light.ambient_intensity) if studio else 0.0,
        shadow=shadow,
        environment=lit_by_map,
        env_from_world=matrix,
        env_scale=scale,
        sun=rotation @ sun_world,
        sun_color=sun_color,
        env_shadow=env_shadow,
    )
