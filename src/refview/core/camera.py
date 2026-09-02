"""Interactive camera model driving both perspective and orthographic views."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum

import numpy as np

from .linalg import look_at, normalize, orthographic, perspective, rotation_matrix, vec3
from .mesh import Bounds


class Projection(str, Enum):
    """Projection used by :class:`Camera`."""

    PERSPECTIVE = "perspective"
    ORTHOGRAPHIC = "orthographic"

    @property
    def label(self) -> str:
        return "Perspective" if self is Projection.PERSPECTIVE else "Orthographic"


@dataclass
class Camera:
    """A look-at camera with orbit / pan / zoom behaviour.

    The orthographic extent is derived from ``distance`` and ``fov_deg`` rather
    than stored separately.  Switching projection therefore keeps the object at
    roughly the same size on screen, and one zoom implementation serves both
    modes.
    """

    eye: np.ndarray = field(default_factory=lambda: vec3(0.0, 0.0, 5.0))
    target: np.ndarray = field(default_factory=lambda: vec3(0.0, 0.0, 0.0))
    world_up: np.ndarray = field(default_factory=lambda: vec3(0.0, 1.0, 0.0))
    fov_deg: float = 40.0
    projection: Projection = Projection.PERSPECTIVE
    scene_radius: float = 1.0
    scene_center: np.ndarray = field(default_factory=lambda: vec3(0.0, 0.0, 0.0))

    #: Zoom limits, expressed as multiples of the scene radius.
    MIN_DISTANCE_FACTOR = 1e-3
    MAX_DISTANCE_FACTOR = 5e2
    #: Closest the view direction may come to the up axis, in radians.
    MIN_POLE_ANGLE = math.radians(1.5)

    def __post_init__(self) -> None:
        self.eye = np.asarray(self.eye, dtype=np.float64).copy()
        self.target = np.asarray(self.target, dtype=np.float64).copy()
        self.world_up = normalize(self.world_up)
        self.scene_center = np.asarray(self.scene_center, dtype=np.float64).copy()

    # ------------------------------------------------------------------
    # Derived frame
    # ------------------------------------------------------------------

    @property
    def forward(self) -> np.ndarray:
        return normalize(self.target - self.eye)

    @property
    def right(self) -> np.ndarray:
        forward = self.forward
        if abs(float(np.dot(forward, self.world_up))) > 0.9999:
            helper = vec3(0.0, 0.0, 1.0) if abs(forward[2]) < 0.9 else vec3(1.0, 0.0, 0.0)
            return normalize(np.cross(forward, helper))
        return normalize(np.cross(forward, self.world_up))

    @property
    def up(self) -> np.ndarray:
        return np.cross(self.right, self.forward)

    @property
    def distance(self) -> float:
        return max(float(np.linalg.norm(self.target - self.eye)), 1e-9)

    @property
    def ortho_half_height(self) -> float:
        """Vertical half-extent of the frustum at the focal plane."""
        return self.distance * math.tan(math.radians(self.fov_deg) * 0.5)

    # ------------------------------------------------------------------
    # Matrices
    # ------------------------------------------------------------------

    def view_matrix(self) -> np.ndarray:
        return look_at(self.eye, self.target, self.world_up)

    def clip_planes(self) -> tuple[float, float]:
        """Near/far planes fitted to the scene bounding sphere."""
        radius = max(self.scene_radius, 1e-6)
        eye_distance = float(np.linalg.norm(self.eye - self.scene_center))
        far = eye_distance + radius * 3.0
        if self.projection is Projection.ORTHOGRAPHIC:
            return -far, far
        near = max(eye_distance - radius * 1.5, radius * 1e-3, far * 1e-5)
        return near, far

    def projection_matrix(self, aspect: float) -> np.ndarray:
        near, far = self.clip_planes()
        if self.projection is Projection.ORTHOGRAPHIC:
            return orthographic(self.ortho_half_height, aspect, near, far)
        return perspective(self.fov_deg, aspect, near, far)

    def view_projection(self, aspect: float) -> np.ndarray:
        return self.projection_matrix(aspect) @ self.view_matrix()

    # ------------------------------------------------------------------
    # Screen <-> world
    # ------------------------------------------------------------------

    def ray(self, x: float, y: float, width: int, height: int) -> tuple[np.ndarray, np.ndarray]:
        """Ray through a pixel, as ``(origin, unit direction)``.

        ``x``/``y`` are Qt widget coordinates, with the origin at the top-left.
        """
        aspect = max(width, 1) / max(height, 1)
        ndc_x = (2.0 * x / max(width, 1)) - 1.0
        ndc_y = 1.0 - (2.0 * y / max(height, 1))
        right, up, forward = self.right, self.up, self.forward
        if self.projection is Projection.ORTHOGRAPHIC:
            half_h = self.ortho_half_height
            origin = self.eye + right * (ndc_x * half_h * aspect) + up * (ndc_y * half_h)
            return origin, forward
        tan_half = math.tan(math.radians(self.fov_deg) * 0.5)
        direction = forward + right * (ndc_x * tan_half * aspect) + up * (ndc_y * tan_half)
        return self.eye.copy(), normalize(direction)

    def project(self, point: np.ndarray, width: int, height: int) -> tuple[float, float, float]:
        """Project a world point to ``(x, y, ndc_depth)`` in widget pixels."""
        aspect = max(width, 1) / max(height, 1)
        clip = self.view_projection(aspect) @ np.append(np.asarray(point, dtype=np.float64), 1.0)
        w = clip[3] if abs(clip[3]) > 1e-9 else 1e-9
        ndc = clip[:3] / w
        return (ndc[0] * 0.5 + 0.5) * width, (0.5 - ndc[1] * 0.5) * height, float(ndc[2])

    def plane_point_under_cursor(
        self,
        x: float,
        y: float,
        width: int,
        height: int,
        plane_point: np.ndarray | None = None,
    ) -> np.ndarray:
        """Intersect the pixel ray with the camera-facing plane through a point.

        Defaults to the plane through the camera target -- the plane the orbit
        and zoom gestures pivot on.
        """
        anchor = self.target if plane_point is None else np.asarray(plane_point, dtype=np.float64)
        origin, direction = self.ray(x, y, width, height)
        normal = -self.forward
        denominator = float(np.dot(direction, normal))
        if abs(denominator) < 1e-9:
            return np.asarray(anchor, dtype=np.float64).copy()
        t = float(np.dot(anchor - origin, normal)) / denominator
        return origin + direction * t

    def world_units_per_pixel(self, height: int) -> float:
        """Screen-to-world scale at the focal plane; identical in both modes."""
        return 2.0 * self.ortho_half_height / max(height, 1)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def orbit(self, yaw_rad: float, pitch_rad: float, pivot: np.ndarray | None = None) -> None:
        """Turntable-orbit around ``pivot`` (defaults to the camera target)."""
        centre = self.target if pivot is None else np.asarray(pivot, dtype=np.float64)
        rotation = rotation_matrix(self.world_up, yaw_rad)
        with_pitch = rotation_matrix(self.right, pitch_rad) @ rotation
        if self._pitch_is_safe(with_pitch):
            rotation = with_pitch
        self.eye = centre + rotation @ (self.eye - centre)
        self.target = centre + rotation @ (self.target - centre)

    def _pitch_is_safe(self, rotation: np.ndarray) -> bool:
        """Reject rotations that would drive the view onto the up-axis pole."""
        new_forward = normalize(rotation @ self.forward)
        return abs(float(np.dot(new_forward, self.world_up))) < math.cos(self.MIN_POLE_ANGLE)

    def pan(self, dx_pixels: float, dy_pixels: float, height: int) -> None:
        """Slide the camera parallel to the image plane by a pixel delta."""
        scale = self.world_units_per_pixel(height)
        offset = self.right * (-dx_pixels * scale) + self.up * (dy_pixels * scale)
        self.eye += offset
        self.target += offset

    def zoom(self, factor: float, pivot: np.ndarray | None = None) -> None:
        """Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer).

        Scaling eye *and* target about the pivot keeps that point pinned under
        the mouse cursor, in both projections.
        """
        centre = self.target if pivot is None else np.asarray(pivot, dtype=np.float64)
        factor = self._clamped_zoom_factor(factor)
        self.eye = centre + (self.eye - centre) * factor
        self.target = centre + (self.target - centre) * factor

    def _clamped_zoom_factor(self, factor: float) -> float:
        radius = max(self.scene_radius, 1e-6)
        distance = self.distance
        new_distance = distance * factor
        low = radius * self.MIN_DISTANCE_FACTOR
        high = radius * self.MAX_DISTANCE_FACTOR
        if new_distance < low:
            return low / distance
        if new_distance > high:
            return high / distance
        return factor

    def frame(self, bounds: Bounds, margin: float = 1.15) -> None:
        """Move the camera so ``bounds`` fills the view, keeping the direction."""
        self.scene_radius = bounds.radius
        self.scene_center = np.asarray(bounds.center, dtype=np.float64).copy()
        radius = bounds.radius * margin
        distance = radius / max(math.sin(math.radians(self.fov_deg) * 0.5), 1e-3)
        direction = self.forward
        self.target = self.scene_center.copy()
        self.eye = self.target - direction * distance

    def look_along(self, direction: np.ndarray, bounds: Bounds | None = None) -> None:
        """Point the camera along ``direction``, measured object-to-eye."""
        self.eye = self.target + normalize(direction) * self.distance
        if bounds is not None:
            self.frame(bounds)

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "eye": self.eye.tolist(),
            "target": self.target.tolist(),
            "world_up": self.world_up.tolist(),
            "fov_deg": self.fov_deg,
            "projection": self.projection.value,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Camera":
        return cls(
            eye=np.asarray(data.get("eye", (0.0, 0.0, 5.0)), dtype=np.float64),
            target=np.asarray(data.get("target", (0.0, 0.0, 0.0)), dtype=np.float64),
            world_up=np.asarray(data.get("world_up", (0.0, 1.0, 0.0)), dtype=np.float64),
            fov_deg=float(data.get("fov_deg", 40.0)),
            projection=Projection(data.get("projection", Projection.PERSPECTIVE.value)),
        )

    def copy(self) -> "Camera":
        clone = Camera.from_dict(self.to_dict())
        clone.scene_radius = self.scene_radius
        clone.scene_center = self.scene_center.copy()
        return clone

    def apply(self, other: "Camera") -> None:
        """Adopt the pose of ``other`` without replacing this instance."""
        self.eye = other.eye.copy()
        self.target = other.target.copy()
        self.world_up = other.world_up.copy()
        self.fov_deg = other.fov_deg
        self.projection = other.projection
