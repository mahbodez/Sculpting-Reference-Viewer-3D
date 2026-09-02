"""Freehand annotations painted onto the model surface.

A stroke is a polyline of world-space points that were picked off the surface,
each with the surface normal at that point.  Keeping the normal lets the
renderer lift the stroke a hair off the mesh so it reads as paint sitting on
the form rather than as geometry fighting with it.

Erasing works on points rather than on whole strokes: rubbing out the middle
of a line splits it into the two surviving halves, which is what the gesture
looks like it should do.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import numpy as np

Color = tuple[float, float, float]
Point3 = tuple[float, float, float]


class AnnotateMode(str, Enum):
    """What the annotate tool does with a drag.

    The first three describe the shape a drag lays down and are also stored on
    the resulting stroke; :attr:`ERASE` is a tool mode only.
    """

    FREEHAND = "freehand"
    LINE = "line"
    CIRCLE = "circle"
    ERASE = "erase"

    @property
    def label(self) -> str:
        return {
            AnnotateMode.FREEHAND: "Freehand",
            AnnotateMode.LINE: "Line",
            AnnotateMode.CIRCLE: "Circle",
            AnnotateMode.ERASE: "Eraser",
        }[self]

    @property
    def is_eraser(self) -> bool:
        return self is AnnotateMode.ERASE


@dataclass
class Stroke:
    """One painted polyline lying on the surface."""

    points: list[Point3] = field(default_factory=list)
    #: Surface normal per point.  May be empty in files written elsewhere.
    normals: list[Point3] = field(default_factory=list)
    color: Color = (0.94, 0.29, 0.24)
    width: float = 3.0
    kind: AnnotateMode = AnnotateMode.FREEHAND
    closed: bool = False

    @property
    def point_array(self) -> np.ndarray:
        return np.asarray(self.points, dtype=np.float64).reshape(-1, 3)

    @property
    def normal_array(self) -> np.ndarray:
        """Normals padded to match the points, so callers can zip them freely."""
        normals = np.asarray(self.normals, dtype=np.float64).reshape(-1, 3)
        count = len(self.points)
        if len(normals) == count:
            return normals
        padded = np.zeros((count, 3), dtype=np.float64)
        usable = min(len(normals), count)
        padded[:usable] = normals[:usable]
        return padded

    @property
    def is_drawable(self) -> bool:
        return len(self.points) >= 2

    def split(self, keep: np.ndarray) -> list["Stroke"]:
        """Break the stroke into the runs of points ``keep`` marks as surviving."""
        keep = np.asarray(keep, dtype=bool)
        points, normals = self.point_array, self.normal_array
        closed = self.closed
        if closed and keep.size and keep[0] and keep[-1] and not keep.all():
            # Rotate the gap to the front so a broken circle stays one run.
            shift = int(np.argmin(keep))
            keep = np.roll(keep, -shift)
            points = np.roll(points, -shift, axis=0)
            normals = np.roll(normals, -shift, axis=0)
            closed = False

        pieces: list[Stroke] = []
        for start, stop in _runs(keep):
            if stop - start < 2:
                continue
            pieces.append(
                Stroke(
                    points=[tuple(float(v) for v in p) for p in points[start:stop]],
                    normals=[tuple(float(v) for v in n) for n in normals[start:stop]],
                    color=self.color,
                    width=self.width,
                    kind=self.kind,
                    closed=closed and stop - start == len(keep),
                )
            )
        return pieces


def _runs(mask: np.ndarray) -> list[tuple[int, int]]:
    """Half-open index ranges of the contiguous ``True`` regions of ``mask``."""
    if mask.size == 0:
        return []
    padded = np.concatenate(([False], mask, [False]))
    edges = np.flatnonzero(padded[1:] != padded[:-1])
    return list(zip(edges[0::2].tolist(), edges[1::2].tolist()))


@dataclass
class AnnotationSettings:
    """The annotate tool's brush, shared by every stroke it lays down."""

    mode: AnnotateMode = AnnotateMode.FREEHAND
    color: Color = (0.94, 0.29, 0.24)
    width: float = 3.0
    #: Eraser radius in screen pixels, converted to world units at the hit depth.
    erase_radius: float = 16.0
    visible: bool = True

    def new_stroke(self, kind: AnnotateMode | None = None) -> Stroke:
        """An empty stroke carrying the current brush."""
        return Stroke(color=self.color, width=self.width, kind=kind or self.mode)


class AnnotationStore:
    """An ordered collection of strokes, oldest first."""

    def __init__(self, items: list[Stroke] | None = None) -> None:
        self._items: list[Stroke] = list(items or [])

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index: int) -> Stroke:
        return self._items[index]

    @property
    def items(self) -> list[Stroke]:
        """The live list; the undo commands operate on it directly."""
        return self._items

    def add(self, stroke: Stroke) -> Stroke:
        self._items.append(stroke)
        return stroke

    def clear(self) -> None:
        self._items.clear()

    def erased(self, center, radius: float) -> list[Stroke] | None:
        """Strokes with the points within ``radius`` of ``center`` rubbed out.

        Returns ``None`` when the eraser touched nothing, so callers can skip
        the work of recording an undo step for a no-op.
        """
        center = np.asarray(center, dtype=np.float64)
        radius = max(float(radius), 0.0)
        result: list[Stroke] = []
        changed = False
        for stroke in self._items:
            points = stroke.point_array
            if points.size == 0:
                changed = True
                continue
            keep = np.linalg.norm(points - center, axis=1) > radius
            if keep.all():
                result.append(stroke)
                continue
            changed = True
            result.extend(stroke.split(keep))
        return result if changed else None
