"""The HDRI on the GPU: its textures, the GLSL that reads them, and the light rig.

:mod:`refview.core.environment` reads a map and works out what the shaders
need from it; this is where that goes onto the card and how every lit mode
reads it back.  One piece of GLSL, ``glsl/environment.glsl``, is included by
the mesh shader and the background alike, so a reflection and the photograph
behind the model can never disagree about where the window is.

The light rig itself -- which lights are on and where they point -- is
settled in :mod:`refview.core.lighting`, where the CPU path tracer reads it
too; it is re-exported here for the renderer.
"""

from __future__ import annotations

import math

import numpy as np
from OpenGL import GL

from ..core.environment import EnvironmentMap
from ..core.lighting import LightRig, environment_matrix, light_rig
from .shader_files import load_glsl
from .texture import DataTexture, Texture2D

#: Texture units, after the skin's tables and the body map.
ENV_MAP_UNIT, ENV_TEXELS_UNIT, ENV_CDF_UNIT = 12, 13, 14

__all__ = [
    "ENV_GLSL", "EnvironmentTextures", "LightRig", "background_basis",
    "environment_matrix", "light_rig",
]

ENV_GLSL = load_glsl("environment.glsl")


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
