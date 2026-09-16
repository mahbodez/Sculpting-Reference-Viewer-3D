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


# ----------------------------------------------------------------------
# Quaternions
#
# Stored as ``(x, y, z, w)``, which is glTF's order and the one a file's
# skeleton arrives in.  Kept as plain arrays rather than a class: a pose is a
# handful of these and the arithmetic on them is four lines each.
# ----------------------------------------------------------------------

Quat = np.ndarray

#: No turn at all.
IDENTITY_QUAT: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0)


def quat_normalize(q) -> Quat:
    """A unit quaternion, or the identity for one that has collapsed."""
    q = np.asarray(q, dtype=np.float64).reshape(4)
    length = float(np.linalg.norm(q))
    if length < 1e-12:
        return np.array(IDENTITY_QUAT, dtype=np.float64)
    return q / length


def quat_multiply(first, second) -> Quat:
    """The turn ``second`` followed by the turn ``first`` (matrix order)."""
    x1, y1, z1, w1 = np.asarray(first, dtype=np.float64).reshape(4)
    x2, y2, z2, w2 = np.asarray(second, dtype=np.float64).reshape(4)
    return np.array(
        [
            w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2,
            w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2,
            w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2,
            w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2,
        ]
    )


def quat_conjugate(q) -> Quat:
    """The inverse turn of a unit quaternion."""
    x, y, z, w = np.asarray(q, dtype=np.float64).reshape(4)
    return np.array([-x, -y, -z, w])


def quat_from_axis_angle(axis, angle_rad: float) -> Quat:
    axis = normalize(axis)
    half = float(angle_rad) * 0.5
    return np.array([*(axis * math.sin(half)), math.cos(half)])


def quat_to_matrix(q) -> np.ndarray:
    """The 3x3 rotation a unit quaternion stands for."""
    x, y, z, w = quat_normalize(q)
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ]
    )


def matrix_to_quat(matrix) -> Quat:
    """The unit quaternion of a rotation matrix (Shepperd's method).

    The matrix may carry a scale; only its rotation is read.  Picks the
    largest of the four candidates so that no division goes through zero.
    """
    m = np.asarray(matrix, dtype=np.float64)[:3, :3]
    scale = np.linalg.norm(m, axis=0)
    m = m / np.where(scale > 1e-12, scale, 1.0)
    trace = float(np.trace(m))
    if trace > 0.0:
        s = math.sqrt(trace + 1.0) * 2.0
        q = [(m[2, 1] - m[1, 2]) / s, (m[0, 2] - m[2, 0]) / s, (m[1, 0] - m[0, 1]) / s, 0.25 * s]
    elif m[0, 0] > m[1, 1] and m[0, 0] > m[2, 2]:
        s = math.sqrt(1.0 + m[0, 0] - m[1, 1] - m[2, 2]) * 2.0
        q = [0.25 * s, (m[0, 1] + m[1, 0]) / s, (m[0, 2] + m[2, 0]) / s, (m[2, 1] - m[1, 2]) / s]
    elif m[1, 1] > m[2, 2]:
        s = math.sqrt(1.0 + m[1, 1] - m[0, 0] - m[2, 2]) * 2.0
        q = [(m[0, 1] + m[1, 0]) / s, 0.25 * s, (m[1, 2] + m[2, 1]) / s, (m[0, 2] - m[2, 0]) / s]
    else:
        s = math.sqrt(1.0 + m[2, 2] - m[0, 0] - m[1, 1]) * 2.0
        q = [(m[0, 2] + m[2, 0]) / s, (m[1, 2] + m[2, 1]) / s, 0.25 * s, (m[1, 0] - m[0, 1]) / s]
    return quat_normalize(q)


def quat_between(source, target) -> Quat:
    """The shortest turn carrying direction ``source`` onto ``target``."""
    a = normalize(source)
    b = normalize(target)
    dot = float(np.clip(np.dot(a, b), -1.0, 1.0))
    if dot < -0.999999:
        # Opposite directions: any axis square to ``a`` will do.
        helper = vec3(1.0, 0.0, 0.0) if abs(a[0]) < 0.9 else vec3(0.0, 1.0, 0.0)
        return quat_from_axis_angle(np.cross(a, helper), math.pi)
    axis = np.cross(a, b)
    return quat_normalize(np.array([*axis, 1.0 + dot]))


def euler_to_quat(x_deg: float, y_deg: float, z_deg: float) -> Quat:
    """A turn from three angles applied about the local X, then Y, then Z axes."""
    qx = quat_from_axis_angle(vec3(1.0, 0.0, 0.0), math.radians(x_deg))
    qy = quat_from_axis_angle(vec3(0.0, 1.0, 0.0), math.radians(y_deg))
    qz = quat_from_axis_angle(vec3(0.0, 0.0, 1.0), math.radians(z_deg))
    return quat_multiply(qx, quat_multiply(qy, qz))


def quat_to_euler(q) -> tuple[float, float, float]:
    """The three angles :func:`euler_to_quat` would build ``q`` from, in degrees."""
    m = quat_to_matrix(q)
    # R = Rx Ry Rz, so the top row holds the Y and Z angles outright.
    sy = float(np.clip(m[0, 2], -1.0, 1.0))
    y = math.asin(sy)
    if abs(sy) < 0.999999:
        x = math.atan2(-m[1, 2], m[2, 2])
        z = math.atan2(-m[0, 1], m[0, 0])
    else:
        # Gimbal lock: fold everything into X.
        x = math.atan2(m[2, 1], m[1, 1])
        z = 0.0
    return (math.degrees(x), math.degrees(y), math.degrees(z))


def compose(translation, rotation, scale=(1.0, 1.0, 1.0)) -> np.ndarray:
    """A 4x4 from a translation, a quaternion and a scale, applied scale first."""
    matrix = np.eye(4)
    matrix[:3, :3] = quat_to_matrix(rotation) * np.asarray(scale, dtype=np.float64)
    matrix[:3, 3] = np.asarray(translation, dtype=np.float64)
    return matrix
