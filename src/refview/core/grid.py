"""Reference grids on the three axis planes, fading with distance.

A grid gives the eye a scale and a level: how tall the figure is against the
squares, whether it stands plumb, where the ground is.  The ground grid is on
by default and the other two are there for reading a profile or a front
against something straight.

The lines are built as plain segments and drawn by the stroke shader, which
already knows how to keep a line a pixel wide at any zoom and how to fade it
about a point; here the point is the camera itself, so the far squares melt
away before the grid can turn into a moire pattern at the horizon.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .mesh import Bounds

Color = tuple[float, float, float]

#: Ends of the line-count slider: lines from the centre to one edge of the
#: grid.  Four is a coarse floor under a model; two hundred is where the
#: squares are a pixel or two wide at the size a model is looked at.
COUNT_MIN, COUNT_MAX = 4, 200
#: Ends of the fade slider, as a multiple of the camera's distance to the
#: grid.  Nought turns the fade off.
FADE_MIN, FADE_MAX = 0.0, 10.0

#: The world axes drawn in their own colours where they cross the grid, so
#: the ground grid also says which way is which.  The same reds and blues as
#: the corner gizmo.
AXIS_COLORS: tuple[Color, Color, Color] = (
    (0.90, 0.32, 0.30),
    (0.42, 0.78, 0.36),
    (0.30, 0.55, 0.95),
)


def nice_step(value: float) -> float:
    """The nearest 1, 2 or 5 times a power of ten at or below ``value``."""
    if not math.isfinite(value) or value <= 0.0:
        return 1.0
    power = 10.0 ** math.floor(math.log10(value))
    for factor in (5.0, 2.0, 1.0):
        if factor * power <= value * (1.0 + 1e-9):
            return factor * power
    return power


@dataclass
class GridSettings:
    """Which planes carry a grid, how fine it is, and how it fades."""

    #: The XZ plane -- the floor.
    ground: bool = True
    #: The XY plane -- a wall behind the model, read from the front.
    front: bool = False
    #: The YZ plane -- a wall beside it, read from the side.
    side: bool = False
    #: Lines from the centre of the grid to each of its edges.
    count: int = 20
    #: Distance between lines in scene units, or nought to pick a round
    #: number that puts the grid a little wider than the scene.
    spacing: float = 0.0
    #: Every this-many lines a heavier one is drawn; nought for none.
    major_every: int = 10
    #: How far the lines are drawn before they have faded away, as a
    #: multiple of the camera's distance to the grid's centre.  Measured that
    #: way so the same setting reads the same close up and far off; nought
    #: draws the whole grid at one strength.
    fade: float = 2.5
    #: How solid a line is at its strongest.
    opacity: float = 0.55
    #: Line thickness in logical pixels; the heavy lines are half again.
    line_width: float = 1.0
    color: Color = (0.55, 0.56, 0.60)
    #: Draw the X, Y and Z axes through the grid in their own colours.
    show_axes: bool = True
    #: Sit the ground grid under the scene's lowest point rather than
    #: through the origin, so it never cuts the model in two.  The two
    #: walls always pass through the origin.
    at_floor: bool = True

    @property
    def any(self) -> bool:
        return self.ground or self.front or self.side

    def step(self, scene_radius: float) -> float:
        """The spacing in use: the artist's, or a round share of the scene."""
        if self.spacing > 0.0:
            return float(self.spacing)
        count = max(int(self.count), COUNT_MIN)
        return nice_step(2.5 * max(float(scene_radius), 1e-6) / count)


@dataclass(frozen=True)
class GridLines:
    """Segments, with their colours and widths, ready for the stroke buffer."""

    segments: np.ndarray  # (n, 2, 3)
    colors: np.ndarray  # (n, 3)
    widths: np.ndarray  # (n,)
    #: Where the grids meet, which the fade is measured against.
    centre: np.ndarray


def build_grid(
    settings: GridSettings, bounds: Bounds | None, scene_radius: float
) -> GridLines | None:
    """Every line of every enabled grid, or ``None`` when none is on."""
    if not settings.any:
        return None
    count = int(min(max(int(settings.count), COUNT_MIN), COUNT_MAX))
    step = settings.step(scene_radius)
    reach = count * step
    offsets = np.arange(-count, count + 1, dtype=np.float64) * step
    major = max(int(settings.major_every), 0)
    heavy = np.zeros(len(offsets), dtype=bool)
    if major > 0:
        heavy = (np.arange(-count, count + 1) % major) == 0
    centre_line = np.arange(-count, count + 1) == 0

    floor = 0.0
    if settings.at_floor and bounds is not None:
        floor = float(bounds.minimum[1])
    origin = np.array([0.0, floor if settings.ground else 0.0, 0.0])

    segments, colors, widths = [], [], []
    base = np.asarray(settings.color, dtype=np.float64)
    thin, thick = float(settings.line_width), float(settings.line_width) * 1.6

    def plane(normal_axis: int, level: float) -> None:
        """The two families of lines lying in the plane square to ``normal_axis``."""
        along = [axis for axis in range(3) if axis != normal_axis]
        for run_axis, step_axis in ((along[0], along[1]), (along[1], along[0])):
            head = np.zeros((len(offsets), 3))
            tail = np.zeros((len(offsets), 3))
            head[:, normal_axis] = tail[:, normal_axis] = level
            head[:, step_axis] = tail[:, step_axis] = offsets
            head[:, run_axis] = -reach
            tail[:, run_axis] = reach
            color = np.tile(base, (len(offsets), 1))
            width = np.where(heavy, thick, thin)
            if settings.show_axes:
                # The line through the centre runs along run_axis: it is
                # that axis, and is coloured as such.
                color[centre_line] = AXIS_COLORS[run_axis]
                width[centre_line] = thick
            segments.append(np.stack((head, tail), axis=1))
            colors.append(color)
            widths.append(width)

    if settings.ground:
        plane(1, floor)
    if settings.front:
        plane(2, 0.0)
    if settings.side:
        plane(0, 0.0)
    return GridLines(
        np.concatenate(segments),
        np.concatenate(colors),
        np.concatenate(widths),
        origin,
    )
