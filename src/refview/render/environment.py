"""The HDRI on the GPU: its textures, the GLSL that reads them, and the light rig.

:mod:`refview.core.environment` reads a map and works out what the shaders
need from it; this is where that goes onto the card and how every lit mode
reads it back.  One piece of GLSL, ``glsl/environment.glsl``, is included by
the mesh shader and the background alike, so a reflection and the photograph
behind the model can never disagree about where the window is.

:func:`light_rig` settles, once a frame, which lights are on and where they
point: the studio key and fill, the HDRI, or both, and the one direction the
shadow map is cast from -- the key's when there is a key, the map's dominant
light when the map is all there is.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from OpenGL import GL

from ..core.environment import EnvironmentMap, rotation_y
from ..core.linalg import spherical_direction
from ..core.settings import RenderSettings
from .shader_files import load_glsl
from .texture import DataTexture, Texture2D

#: Texture units, after the skin's tables and the body map.
ENV_MAP_UNIT, ENV_TEXELS_UNIT, ENV_CDF_UNIT = 12, 13, 14

ENV_GLSL = load_glsl("environment.glsl")


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


def background_basis(camera, aspect: float) -> np.ndarray:
    """Columns that turn a screen position (-1 to 1 each way, 1) into a world ray.

    An orthographic view has no rays to speak of, so the background is drawn
    as the perspective camera with the same field of view would see it --
    which is also what keeps it still when the projection is switched.
    """
    tan_half = math.tan(math.radians(camera.fov_deg) * 0.5)
    right = np.asarray(camera.right, dtype=np.float64) * tan_half * aspect
    up = np.asarray(camera.up, dtype=np.float64) * tan_half
    forward = np.asarray(camera.forward, dtype=np.float64)
    return np.stack([right, up, forward], axis=1)


class EnvironmentTextures:
    """The map, the sampling tables, and the uniforms that describe them."""

    def __init__(self) -> None:
        self.environment: EnvironmentMap | None = None
        self._map: Texture2D | None = None
        self._texels: DataTexture | None = None
        self._cdf: DataTexture | None = None

    def initialize(self) -> None:
        self._map = Texture2D(wrap=True)
        self._texels = DataTexture()
        self._cdf = DataTexture()
        self._upload(self.environment)

    def set(self, environment: EnvironmentMap | None) -> None:
        """Put a map on the card, or take it off; cheap when it is the one already there."""
        if environment is self.environment:
            return
        self.environment = environment
        if self._map is not None:
            self._upload(environment)

    def _upload(self, environment: EnvironmentMap | None) -> None:
        # Complete samplers even with no map, so a shader that never reads
        # them still binds something valid.
        if environment is None:
            self._map.upload(np.zeros((1, 2, 4), np.float32))
            self._texels.upload(np.zeros((1, 2, 4), np.float32))
            cdf = np.zeros((2, 3, 4), np.float32)
            cdf[:, -1, 0] = 1.0
            self._cdf.upload(cdf)
            return
        radiance = environment.radiance
        rgba = np.concatenate([radiance, np.ones(radiance.shape[:2] + (1,), np.float32)], axis=-1)
        self._map.upload(rgba)
        texels, cdf = environment.sampling.packed()
        self._texels.upload(texels)
        self._cdf.upload(cdf)

    def bind(self, program, rig: LightRig, scale_factor: float = 1.0) -> None:
        """Point ``program`` at the map, scaled by ``scale_factor`` on top of the rig's own.

        The display-space modes want a factor of pi here: they read a key of
        one as a white surface lit white, where a physical surface under an
        irradiance of one is only 1/pi as bright.
        """
        on = rig.environment and self.environment is not None and self._map is not None
        program.set_bool("uEnvOn", on)
        program.set_int("uEnvMap", ENV_MAP_UNIT)
        program.set_int("uEnvTexels", ENV_TEXELS_UNIT)
        program.set_int("uEnvCdf", ENV_CDF_UNIT)
        scale = rig.env_scale * scale_factor
        program.set_float("uEnvScale", scale)
        program.set_matrix3("uEnvFromWorld", rig.env_from_world)
        program.set_vec3("uEnvSunView", rig.sun)
        program.set_vec3("uEnvSunColor", rig.sun_color * scale)
        program.set_bool("uEnvShadow", rig.env_shadow)
        if self._map is not None:
            program.set_float("uEnvLevels", float(self._map.levels))
            program.set_float("uEnvWidth", float(self._map.width))
            self._map.bind(ENV_MAP_UNIT)
            self._texels.bind(ENV_TEXELS_UNIT)
            self._cdf.bind(ENV_CDF_UNIT)
            GL.glActiveTexture(GL.GL_TEXTURE0)
        sh = self.environment.sh if self.environment is not None else np.zeros((9, 3))
        for index in range(9):
            program.set_vec3(f"uEnvSH[{index}]", sh[index])

    def dispose(self) -> None:
        for texture in (self._map, self._texels, self._cdf):
            if texture is not None:
                texture.dispose()
        self._map = self._texels = self._cdf = None
