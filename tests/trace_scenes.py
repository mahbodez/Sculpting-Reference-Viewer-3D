"""Small scenes the path tracer's tests render: a sphere, a soup, a constant sky."""

from __future__ import annotations

import numpy as np

from refview.core.camera import Camera
from refview.core.environment import prepare_environment
from refview.core.mesh import Mesh


def sphere(n: int = 32, radius: float = 1.0, center=(0.0, 0.0, 0.0)) -> Mesh:
    """A closed UV sphere with smooth normals and shared vertices at the seam and poles."""
    theta = np.linspace(0.0, np.pi, n + 1)
    phi = np.linspace(0.0, 2.0 * np.pi, 2 * n, endpoint=False)
    t, p = np.meshgrid(theta[1:-1], phi, indexing="ij")
    ring = np.stack([np.sin(t) * np.cos(p), np.cos(t), np.sin(t) * np.sin(p)], -1).reshape(-1, 3)
    points = np.concatenate([[[0.0, 1.0, 0.0]], ring, [[0.0, -1.0, 0.0]]])
    cols = 2 * n
    rows = n - 1
    top, bottom = 0, len(points) - 1
    tris = []
    for j in range(cols):
        tris.append((top, 1 + (j + 1) % cols, 1 + j))
    for i in range(rows - 1):
        for j in range(cols):
            a = 1 + i * cols + j
            b = 1 + i * cols + (j + 1) % cols
            c = a + cols
            d = b + cols
            tris.append((a, b, c))
            tris.append((b, d, c))
    base = 1 + (rows - 1) * cols
    for j in range(cols):
        tris.append((base + j, base + (j + 1) % cols, bottom))
    positions = points * radius + np.asarray(center)
    return Mesh(positions=positions, normals=points, indices=np.array(tris, np.uint32))


def looking_at_origin(distance: float = 4.0, fov: float = 30.0, radius: float = 1.0) -> Camera:
    camera = Camera(eye=np.array([0.0, 0.0, distance]), target=np.zeros(3), fov_deg=fov)
    camera.scene_radius = radius
    return camera


def constant_sky(value=(1.0, 1.0, 1.0), width: int = 64):
    """An HDRI of one colour everywhere."""
    pixels = np.ones((width // 2, width, 3), np.float32) * np.asarray(value, np.float32)
    return prepare_environment(pixels, "constant")


def gradient_sky(width: int = 128):
    """An HDRI brighter in one patch, for the importance-sampling tests."""
    h = width // 2
    pixels = np.full((h, width, 3), 0.2, np.float32)
    pixels[h // 4: h // 3, width // 3: width // 2] = 40.0
    pixels[:, :, 1] *= 0.8
    return prepare_environment(pixels, "gradient")
