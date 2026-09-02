"""Cutting the model open with planes.

A section is described by one plane -- an axis or an arbitrary direction, plus
a distance along it -- and a mode that says what survives: the material below
the plane, the material above it, or a slab of a chosen thickness centred on
it.  Each of those is expressed as one or two half-spaces, so the renderer only
ever deals with a list of planes and discards whatever falls outside them.

The cut contour is worked out here as well.  Intersecting the plane with every
triangle gives the outline of the cut, which is drawn as a bright line so the
silhouette at that level reads clearly -- exactly the profile a sculptor holds
a caliper against.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from .mesh import Mesh

Color = tuple[float, float, float]


class SectionAxis(str, Enum):
    """The direction the section plane faces."""

    X = "x"
    Y = "y"
    Z = "z"
    CUSTOM = "custom"

    @property
    def label(self) -> str:
        return {
            SectionAxis.X: "X (side)",
            SectionAxis.Y: "Y (height)",
            SectionAxis.Z: "Z (front)",
            SectionAxis.CUSTOM: "Custom",
        }[self]

    @property
    def direction(self) -> np.ndarray | None:
        """Unit axis, or ``None`` for a custom direction."""
        vectors = {
            SectionAxis.X: (1.0, 0.0, 0.0),
            SectionAxis.Y: (0.0, 1.0, 0.0),
            SectionAxis.Z: (0.0, 0.0, 1.0),
        }
        vector = vectors.get(self)
        return None if vector is None else np.asarray(vector, dtype=np.float64)


class SectionMode(str, Enum):
    """Which side of the plane survives the cut."""

    BELOW = "below"
    ABOVE = "above"
    SLAB = "slab"

    @property
    def label(self) -> str:
        return {
            SectionMode.BELOW: "Keep below",
            SectionMode.ABOVE: "Keep above",
            SectionMode.SLAB: "Slice",
        }[self]


@dataclass(frozen=True)
class SectionPlane:
    """A half-space: everything past ``offset`` along ``normal`` is cut away."""

    normal: np.ndarray
    offset: float

    def distances(self, points: np.ndarray) -> np.ndarray:
        """Signed distance of each point; positive means cut away."""
        return np.asarray(points, dtype=np.float64) @ self.normal - self.offset


@dataclass
class SectionSettings:
    """How the model is cut open, and how the cut is drawn."""

    enabled: bool = False
    axis: SectionAxis = SectionAxis.X
    #: Direction used when ``axis`` is :attr:`SectionAxis.CUSTOM`.
    custom_normal: tuple[float, float, float] = (1.0, 0.0, 0.0)
    #: Distance of the plane from the origin, in scene units.
    offset: float = 0.0
    mode: SectionMode = SectionMode.BELOW
    #: Total thickness of the retained slab, in scene units.
    thickness: float = 0.1
    flip: bool = False
    show_contour: bool = True
    contour_color: Color = (1.0, 0.86, 0.35)
    contour_width: float = 2.5
    #: Paint the exposed interior flat so the cut reads as solid material.
    fill_cut: bool = True
    cap_color: Color = (0.62, 0.34, 0.30)

    @property
    def normal(self) -> np.ndarray:
        """Unit plane normal, honouring the flip toggle."""
        direction = self.axis.direction
        if direction is None:
            direction = np.asarray(self.custom_normal, dtype=np.float64)
        length = float(np.linalg.norm(direction))
        if length < 1e-9:
            direction, length = np.array([1.0, 0.0, 0.0]), 1.0
        return direction / length * (-1.0 if self.flip else 1.0)

    def planes(self) -> list[SectionPlane]:
        """The half-spaces the current mode cuts with; empty when disabled."""
        if not self.enabled:
            return []
        normal = self.normal
        if self.mode is SectionMode.ABOVE:
            return [SectionPlane(-normal, -self.offset)]
        if self.mode is SectionMode.SLAB:
            half = max(self.thickness, 1e-6) * 0.5
            return [
                SectionPlane(normal, self.offset + half),
                SectionPlane(-normal, -(self.offset - half)),
            ]
        return [SectionPlane(normal, self.offset)]


def section_segments(mesh: Mesh, plane: SectionPlane) -> np.ndarray:
    """Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``.

    Every triangle with corners on both sides of the plane contributes one
    segment, found by interpolating along the two edges that cross it.  The
    result is an unordered soup of segments rather than joined-up loops, which
    is all the renderer needs and avoids stitching a contour that may well be
    open where the model is.
    """
    if mesh.triangle_count == 0:
        return np.zeros((0, 2, 3), dtype=np.float64)

    # Measure once per vertex and only expand the triangles that straddle the
    # plane: on a scan mesh that is the difference between a slider that keeps
    # up with the mouse and one that stutters.
    distances = plane.distances(mesh.positions)[mesh.indices]
    outside = distances > 0.0
    count = outside.sum(axis=1)
    straddling = np.flatnonzero((count == 1) | (count == 2))
    if straddling.size == 0:
        return np.zeros((0, 2, 3), dtype=np.float64)

    corners = mesh.positions[mesh.indices[straddling]].astype(np.float64)
    distances = distances[straddling]
    outside = outside[straddling]

    # Edges (0,1), (1,2), (2,0); exactly two of the three change sign.
    heads = np.arange(3)
    tails = (heads + 1) % 3
    crossing = outside[:, heads] != outside[:, tails]
    near, far = distances[:, heads], distances[:, tails]
    with np.errstate(divide="ignore", invalid="ignore"):
        blend = near / np.where(np.abs(near - far) < 1e-20, 1e-20, near - far)
    points = corners[:, heads] + (corners[:, tails] - corners[:, heads]) * blend[..., None]

    rows, columns = np.nonzero(crossing)
    return points[rows, columns].reshape(-1, 2, 3)
