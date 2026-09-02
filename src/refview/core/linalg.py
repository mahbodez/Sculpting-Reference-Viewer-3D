"""Small linear-algebra helpers using OpenGL conventions.

Matrices are stored row-major in numpy and transposed on upload, so
``matrix @ vector`` behaves as expected in Python while the shader still sees
column-major data.
"""

from __future__ import annotations

import math

import numpy as np

Vec3 = np.ndarray


def vec3(x: float, y: float, z: float) -> Vec3:
    return np.array([x, y, z], dtype=np.float64)


def normalize(v: np.ndarray, fallback: Vec3 | None = None) -> Vec3:
    """Return ``v`` scaled to unit length, or ``fallback`` for a zero vector."""
    v = np.asarray(v, dtype=np.float64)
    length = float(np.linalg.norm(v))
    if length < 1e-12:
        return vec3(0.0, 0.0, 1.0) if fallback is None else np.asarray(fallback, dtype=np.float64)
    return v / length


def look_at(eye: Vec3, target: Vec3, up: Vec3) -> np.ndarray:
    """Right-handed view matrix looking from ``eye`` towards ``target``."""
    eye = np.asarray(eye, dtype=np.float64)
    forward = normalize(np.asarray(target, dtype=np.float64) - eye)
    up = normalize(up)
    if abs(float(np.dot(forward, up))) > 0.9999:
        # Degenerate: pick any axis that is not parallel to the view direction.
        helper = vec3(0.0, 0.0, 1.0) if abs(forward[2]) < 0.9 else vec3(1.0, 0.0, 0.0)
        right = normalize(np.cross(forward, helper))
    else:
        right = normalize(np.cross(forward, up))
    true_up = np.cross(right, forward)

    matrix = np.eye(4)
    matrix[0, :3] = right
    matrix[1, :3] = true_up
    matrix[2, :3] = -forward
    matrix[:3, 3] = -matrix[:3, :3] @ eye
    return matrix


def perspective(fov_y_deg: float, aspect: float, near: float, far: float) -> np.ndarray:
    """Standard OpenGL perspective projection."""
    f = 1.0 / math.tan(math.radians(fov_y_deg) * 0.5)
    matrix = np.zeros((4, 4))
    matrix[0, 0] = f / max(aspect, 1e-6)
    matrix[1, 1] = f
    matrix[2, 2] = (far + near) / (near - far)
    matrix[2, 3] = (2.0 * far * near) / (near - far)
    matrix[3, 2] = -1.0
    return matrix


def orthographic(half_height: float, aspect: float, near: float, far: float) -> np.ndarray:
    """Symmetric orthographic projection with the given vertical half-extent."""
    half_width = half_height * max(aspect, 1e-6)
    span = max(far - near, 1e-9)
    matrix = np.eye(4)
    matrix[0, 0] = 1.0 / max(half_width, 1e-9)
    matrix[1, 1] = 1.0 / max(half_height, 1e-9)
    matrix[2, 2] = -2.0 / span
    matrix[2, 3] = -(far + near) / span
    return matrix


def rotation_matrix(axis: Vec3, angle_rad: float) -> np.ndarray:
    """3x3 rotation about an arbitrary axis, via the Rodrigues formula."""
    axis = normalize(axis)
    c, s = math.cos(angle_rad), math.sin(angle_rad)
    t = 1.0 - c
    x, y, z = axis
    return np.array(
        [
            [c + x * x * t, x * y * t - z * s, x * z * t + y * s],
            [y * x * t + z * s, c + y * y * t, y * z * t - x * s],
            [z * x * t - y * s, z * y * t + x * s, c + z * z * t],
        ]
    )


def spherical_direction(azimuth_deg: float, elevation_deg: float) -> Vec3:
    """Unit vector for an azimuth/elevation pair, with +Y as the pole."""
    az = math.radians(azimuth_deg)
    el = math.radians(elevation_deg)
    cos_el = math.cos(el)
    return vec3(cos_el * math.sin(az), math.sin(el), cos_el * math.cos(az))
