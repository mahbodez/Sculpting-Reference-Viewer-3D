"""Thin wrapper around an OpenGL shader program."""

from __future__ import annotations

import numpy as np
from OpenGL import GL


class ShaderError(RuntimeError):
    """Raised when a shader fails to compile or link."""


class ShaderProgram:
    """Compiles a vertex/fragment pair and caches its uniform locations.

    Uniform setters silently ignore names the driver optimised away, so the
    render code can stay declarative and set everything every frame.
    """

    def __init__(self, vertex_source: str, fragment_source: str, name: str = "program") -> None:
        self.name = name
        self._locations: dict[str, int] = {}
        vertex = self._compile(vertex_source, GL.GL_VERTEX_SHADER)
        fragment = self._compile(fragment_source, GL.GL_FRAGMENT_SHADER)
        self._id = GL.glCreateProgram()
        GL.glAttachShader(self._id, vertex)
        GL.glAttachShader(self._id, fragment)
        GL.glLinkProgram(self._id)
        if not GL.glGetProgramiv(self._id, GL.GL_LINK_STATUS):
            log = GL.glGetProgramInfoLog(self._id).decode("utf-8", "replace")
            raise ShaderError(f"Linking {name} failed:\n{log}")
        GL.glDetachShader(self._id, vertex)
        GL.glDetachShader(self._id, fragment)
        GL.glDeleteShader(vertex)
        GL.glDeleteShader(fragment)

    def _compile(self, source: str, stage: int) -> int:
        shader = GL.glCreateShader(stage)
        GL.glShaderSource(shader, source)
        GL.glCompileShader(shader)
        if not GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS):
            log = GL.glGetShaderInfoLog(shader).decode("utf-8", "replace")
            GL.glDeleteShader(shader)
            stage_name = "vertex" if stage == GL.GL_VERTEX_SHADER else "fragment"
            raise ShaderError(f"Compiling the {self.name} {stage_name} shader failed:\n{log}")
        return shader

    # -- lifetime -------------------------------------------------------

    def __enter__(self) -> "ShaderProgram":
        self.bind()
        return self

    def __exit__(self, *_exc) -> None:
        GL.glUseProgram(0)

    def bind(self) -> None:
        GL.glUseProgram(self._id)

    def dispose(self) -> None:
        if self._id:
            GL.glDeleteProgram(self._id)
            self._id = 0

    # -- uniforms -------------------------------------------------------

    def location(self, name: str) -> int:
        if name not in self._locations:
            self._locations[name] = GL.glGetUniformLocation(self._id, name)
        return self._locations[name]

    def set_int(self, name: str, value: int) -> None:
        location = self.location(name)
        if location >= 0:
            GL.glUniform1i(location, int(value))

    def set_bool(self, name: str, value: bool) -> None:
        self.set_int(name, 1 if value else 0)

    def set_float(self, name: str, value: float) -> None:
        location = self.location(name)
        if location >= 0:
            GL.glUniform1f(location, float(value))

    def set_vec2(self, name: str, value) -> None:
        location = self.location(name)
        if location >= 0:
            x, y = (float(v) for v in value)
            GL.glUniform2f(location, x, y)

    def set_vec3(self, name: str, value) -> None:
        location = self.location(name)
        if location >= 0:
            x, y, z = (float(v) for v in value)
            GL.glUniform3f(location, x, y, z)

    def set_vec4(self, name: str, value) -> None:
        location = self.location(name)
        if location >= 0:
            x, y, z, w = (float(v) for v in value)
            GL.glUniform4f(location, x, y, z, w)

    def set_matrix4(self, name: str, matrix: np.ndarray) -> None:
        """Upload a row-major numpy 4x4, transposing for GL's column-major."""
        location = self.location(name)
        if location >= 0:
            data = np.ascontiguousarray(matrix, dtype=np.float32)
            GL.glUniformMatrix4fv(location, 1, GL.GL_TRUE, data)

    def set_matrix3(self, name: str, matrix: np.ndarray) -> None:
        location = self.location(name)
        if location >= 0:
            data = np.ascontiguousarray(matrix, dtype=np.float32)
            GL.glUniformMatrix3fv(location, 1, GL.GL_TRUE, data)
