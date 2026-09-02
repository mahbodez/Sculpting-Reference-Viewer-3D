"""Putting an imported model the right way up.

Formats disagree about which axis points up -- CAD and Blender exports are
usually Z-up, most game and sculpting tools are Y-up -- and STL says nothing at
all, so a file arrives lying on its side often enough to need a fix.  Rather
than guess, the viewer offers the handful of rigid turns that put it right:
which axis of the file is up, whether it is upside down, and a quarter turn
about the vertical to face the model forwards.

The result is a plain rotation applied to the mesh once, so the rest of the
viewer keeps its rule that mesh coordinates *are* world coordinates.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np

from .linalg import rotation_matrix, vec3


class UpAxis(str, Enum):
    """Which axis of the file points up."""

    X = "x"
    Y = "y"
    Z = "z"

    @property
    def label(self) -> str:
        return {
            UpAxis.X: "X up",
            UpAxis.Y: "Y up (as authored)",
            UpAxis.Z: "Z up (CAD, Blender)",
        }[self]


#: Quarter turns offered for the spin control, in degrees.
SPIN_STEPS: tuple[float, ...] = (0.0, 90.0, 180.0, 270.0)


@dataclass
class OrientationSettings:
    """A rigid turn from the file's axes to the viewer's Y-up world."""

    up_axis: UpAxis = UpAxis.Y
    #: The up axis points the other way -- the model arrived upside down.
    flip_up: bool = False
    #: Rotation about the vertical afterwards, to face the model forwards.
    spin_deg: float = 0.0

    @property
    def is_identity(self) -> bool:
        """Whether the model is used exactly as the file stored it."""
        return self.up_axis is UpAxis.Y and not self.flip_up and self.spin_deg % 360.0 == 0.0

    @property
    def matrix(self) -> np.ndarray:
        """The 3x3 rotation taking file coordinates to world coordinates."""
        rotation = _UP_ROTATIONS[self.up_axis]()
        if self.flip_up:
            # Turning about Z rather than mirroring keeps the winding intact,
            # so a flipped model still shades and casts shadows correctly.
            rotation = rotation_matrix(vec3(0.0, 0.0, 1.0), np.pi) @ rotation
        if self.spin_deg % 360.0:
            spin = rotation_matrix(vec3(0.0, 1.0, 0.0), np.radians(self.spin_deg))
            rotation = spin @ rotation
        return rotation


#: Rotations that bring each file axis onto world +Y, built lazily so the
#: dataclass stays free of shared mutable state.
_UP_ROTATIONS = {
    UpAxis.X: lambda: rotation_matrix(vec3(0.0, 0.0, 1.0), np.pi / 2.0),
    UpAxis.Y: lambda: np.eye(3),
    UpAxis.Z: lambda: rotation_matrix(vec3(1.0, 0.0, 0.0), -np.pi / 2.0),
}
