"""Matcap texture loading and upload, and the small data table beside it."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from OpenGL import GL
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage

#: Matcaps are square by convention; anything larger is downscaled on load.
MAX_MATCAP_SIZE = 1024


class MatcapLoadError(RuntimeError):
    """Raised when an image cannot be used as a matcap."""


def load_matcap_pixels(path: str | Path) -> np.ndarray:
    """Read an image file into an ``(H, W, 4)`` uint8 array ready for GL.

    The image is flipped vertically because Qt's origin is top-left while
    OpenGL samples from the bottom-left.
    """
    path = Path(path)
    image = QImage(str(path))
    if image.isNull():
        raise MatcapLoadError(f"{path.name} is not a readable image")
    if max(image.width(), image.height()) > MAX_MATCAP_SIZE:
        image = image.scaled(
            MAX_MATCAP_SIZE,
            MAX_MATCAP_SIZE,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
    image = image.convertToFormat(QImage.Format.Format_RGBA8888)
    width, height, stride = image.width(), image.height(), image.bytesPerLine()
    buffer = np.frombuffer(image.constBits(), dtype=np.uint8, count=height * stride)
    pixels = buffer.reshape(height, stride // 4, 4)[:, :width, :]
    return np.ascontiguousarray(pixels[::-1])  # GL samples from the bottom-left.


def default_matcap_pixels(size: int = 256) -> np.ndarray:
    """A neutral studio matcap, used before the user picks one."""
    axis = np.linspace(-1.0, 1.0, size)
    x, y = np.meshgrid(axis, -axis)
    z = np.sqrt(np.clip(1.0 - x * x - y * y, 0.0, 1.0))
    inside = (x * x + y * y) <= 1.0

    key = np.clip(0.45 * x + 0.72 * y + 0.53 * z, 0.0, 1.0) ** 1.3
    fill = np.clip(-0.62 * x - 0.35 * y + 0.70 * z, 0.0, 1.0) * 0.35
    rim = np.clip(1.0 - z, 0.0, 1.0) ** 3.0 * 0.30
    shade = 0.10 + 0.78 * key + fill + rim

    rgb = np.stack([shade * 1.00, shade * 0.97, shade * 0.94], axis=-1)
    rgb = np.clip(rgb, 0.0, 1.0) * inside[..., None]
    alpha = np.ones((size, size), dtype=np.float32)
    return (np.concatenate([rgb, alpha[..., None]], axis=-1) * 255).astype(np.uint8)


class DataTexture:
    """A small RGBA32F table the shader reads exact values out of.

    Not a picture: nothing here is filtered or mipmapped, and the shader
    fetches whole texels by index rather than sampling between them.  It
    carries the fitted planes, which a uniform array could also do -- but a
    uniform array is charged against a budget the GL 3.3 spec only promises
    1024 floats of, and a driver honouring exactly that would refuse to
    compile the shader outright rather than degrade.  A texture has no such
    ceiling, so how many planes the viewer offers is a question about what the
    eye can read rather than about whose GPU it is running on.
    """

    def __init__(self) -> None:
        self._id = int(GL.glGenTextures(1))
        self._shape: tuple[int, int] | None = None
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._id)
        for name in (GL.GL_TEXTURE_WRAP_S, GL.GL_TEXTURE_WRAP_T):
            GL.glTexParameteri(GL.GL_TEXTURE_2D, name, GL.GL_CLAMP_TO_EDGE)
        for name in (GL.GL_TEXTURE_MIN_FILTER, GL.GL_TEXTURE_MAG_FILTER):
            GL.glTexParameteri(GL.GL_TEXTURE_2D, name, GL.GL_NEAREST)
        # Without this a texture with no mipmaps is incomplete, and sampling it
        # quietly returns black on some drivers.
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAX_LEVEL, 0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def upload(self, rows: np.ndarray) -> None:
        """Store an ``(h, w, 4)`` float array, reallocating only when resized."""
        rows = np.ascontiguousarray(rows, dtype=np.float32)
        height, width = rows.shape[:2]
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._id)
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 4)
        if self._shape == (height, width):
            GL.glTexSubImage2D(
                GL.GL_TEXTURE_2D, 0, 0, 0, width, height, GL.GL_RGBA, GL.GL_FLOAT, rows
            )
        else:
            GL.glTexImage2D(
                GL.GL_TEXTURE_2D, 0, GL.GL_RGBA32F, width, height, 0,
                GL.GL_RGBA, GL.GL_FLOAT, rows,
            )
            self._shape = (height, width)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def bind(self, unit: int = 0) -> None:
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._id)

    def dispose(self) -> None:
        if self._id:
            GL.glDeleteTextures([self._id])
            self._id = 0
            self._shape = None


class Texture2D:
    """An RGBA8 2D texture with clamped edges and mipmapped minification."""

    def __init__(self) -> None:
        self._id = int(GL.glGenTextures(1))
        self._configure()

    def _configure(self) -> None:
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._id)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def upload(self, pixels: np.ndarray) -> None:
        pixels = np.ascontiguousarray(pixels, dtype=np.uint8)
        height, width = pixels.shape[:2]
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._id)
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_RGBA8,
            width,
            height,
            0,
            GL.GL_RGBA,
            GL.GL_UNSIGNED_BYTE,
            pixels,
        )
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def bind(self, unit: int = 0) -> None:
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._id)

    def dispose(self) -> None:
        if self._id:
            GL.glDeleteTextures([self._id])
            self._id = 0
