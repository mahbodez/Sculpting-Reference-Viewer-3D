"""Turning cursor positions into points in the scene.

Both interactive tools need the same three answers -- what the ray hits, where
the free-floating plane is, and how big a pixel is out there -- so the lookup
lives in one small object that the viewport builds per event and hands around.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from ..core.camera import Camera, Projection
from ..core.mesh import Mesh
from ..core.raycast import Hit, raycast_mesh, snap_to_vertex


@dataclass(frozen=True)
class SurfacePicker:
    """A view of the scene from one camera, sized to the widget."""

    camera: Camera
    mesh: Mesh | None
    width: int
    height: int

    def hit(self, x: float, y: float) -> Hit | None:
        """Closest surface intersection under the cursor, or ``None``."""
        if self.mesh is None:
            return None
        origin, direction = self.camera.ray(x, y, self.width, self.height)
        return raycast_mesh(origin, direction, self.mesh)

    def point(
        self, x: float, y: float, snap: bool = False, snap_pixels: float = 12.0
    ) -> np.ndarray | None:
        """Surface point under the cursor, optionally snapped to a vertex."""
        hit = self.hit(x, y)
        if hit is None:
            return None
        if snap:
            tolerance = self.world_per_pixel(hit.distance) * snap_pixels
            return snap_to_vertex(hit, self.mesh, tolerance)
        return hit.point

    def plane_point(self, x: float, y: float, anchor=None) -> np.ndarray:
        """Point on the camera-facing plane through ``anchor``.

        This is where free-floating measurement points live: dragging one keeps
        it at its own depth, so it stays put when the view turns.
        """
        return self.camera.plane_point_under_cursor(x, y, self.width, self.height, anchor)

    def world_per_pixel(self, distance: float) -> float:
        """Screen-to-world scale at a given depth along the view direction."""
        camera = self.camera
        if camera.projection is Projection.ORTHOGRAPHIC:
            return camera.world_units_per_pixel(self.height)
        half_extent = math.tan(math.radians(camera.fov_deg) * 0.5) * distance
        return 2.0 * half_extent / max(self.height, 1)

    def screen_distance(self, point, x: float, y: float) -> float | None:
        """Pixels between a world point and the cursor, or ``None`` if behind."""
        point = np.asarray(point, dtype=np.float64)
        if float(np.dot(point - self.camera.eye, self.camera.forward)) <= 0.0:
            return None
        screen_x, screen_y, _ = self.camera.project(point, self.width, self.height)
        return math.hypot(screen_x - x, screen_y - y)
