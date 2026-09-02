"""Spatial index that keeps picking fast on large meshes.

Every click, every hover and every sample of a painted stroke casts a ray, so
the cost of a single intersection query is what decides whether the viewer
still feels direct on a million-triangle scan.

The index sorts the triangles along a Morton curve and groups the sorted order
into fixed-size leaves, each with a bounding box.  A query tests the ray
against *all* of the leaf boxes in one vectorised sweep and hands back only the
triangles inside the leaves it entered.  A full BVH would prune a little
better, but walking one in Python costs more than the numpy sweep it saves.
"""

from __future__ import annotations

import numpy as np

_EPSILON = 1e-12
#: Triangles per leaf.  Larger leaves mean fewer boxes to sweep but more
#: triangles to intersect; the product is flat enough that the exact value
#: hardly matters between roughly 32 and 256.
LEAF_SIZE = 64
#: Resolution of the Morton grid, per axis.
_GRID_BITS = 10


class TriangleIndex:
    """Leaf bounding boxes over a Morton-sorted triangle list."""

    __slots__ = ("order", "minimum", "maximum", "leaf_size")

    def __init__(self, corners: np.ndarray, leaf_size: int = LEAF_SIZE) -> None:
        """Build the index from expanded triangle corners, shape ``(T, 3, 3)``."""
        corners = np.asarray(corners, dtype=np.float32).reshape(-1, 3, 3)
        self.leaf_size = max(int(leaf_size), 1)
        count = len(corners)
        if count == 0:
            self.order = np.zeros((0, self.leaf_size), dtype=np.int64)
            self.minimum = np.zeros((0, 3), dtype=np.float64)
            self.maximum = np.zeros((0, 3), dtype=np.float64)
            return

        order = _morton_order(corners.mean(axis=1))
        # Pad the last leaf by repeating its final triangle: a duplicate costs
        # one redundant intersection and keeps the layout a clean rectangle.
        leaves = -(-count // self.leaf_size)
        padded = np.full(leaves * self.leaf_size, order[-1], dtype=np.int64)
        padded[:count] = order
        self.order = padded.reshape(leaves, self.leaf_size)

        grouped = corners[self.order]  # (leaves, leaf_size, 3, 3)
        self.minimum = grouped.min(axis=(1, 2)).astype(np.float64)
        self.maximum = grouped.max(axis=(1, 2)).astype(np.float64)

    @property
    def leaf_count(self) -> int:
        return len(self.order)

    def candidates(self, origin: np.ndarray, direction: np.ndarray) -> np.ndarray:
        """Triangle indices worth intersecting for this ray, possibly empty."""
        if self.leaf_count == 0:
            return np.zeros(0, dtype=np.int64)
        with np.errstate(divide="ignore", invalid="ignore"):
            inverse = 1.0 / np.where(np.abs(direction) < _EPSILON, _EPSILON, direction)
            near = (self.minimum - origin) * inverse
            far = (self.maximum - origin) * inverse
        entry = np.maximum(np.minimum(near, far), 0.0).max(axis=1)
        exit_ = np.maximum(near, far).min(axis=1)
        hits = np.flatnonzero(exit_ >= entry)
        if hits.size == 0:
            return np.zeros(0, dtype=np.int64)
        return np.unique(self.order[hits])


def _morton_order(points: np.ndarray) -> np.ndarray:
    """Indices that sort ``points`` along a Morton (Z-order) curve.

    Neighbours on the curve are neighbours in space, so consecutive runs of the
    sorted order make compact leaves without any tree building.
    """
    minimum = points.min(axis=0)
    extent = np.maximum(points.max(axis=0) - minimum, 1e-20)
    resolution = (1 << _GRID_BITS) - 1
    cells = ((points - minimum) / extent * resolution).astype(np.int64)
    code = np.zeros(len(points), dtype=np.int64)
    for axis in range(3):
        code |= _spread_bits(cells[:, axis]) << axis
    return np.argsort(code, kind="stable")


def _spread_bits(values: np.ndarray) -> np.ndarray:
    """Interleave each 10-bit value with two zero bits, ready to be shifted."""
    values = values & 0x3FF
    values = (values | (values << 16)) & 0x030000FF
    values = (values | (values << 8)) & 0x0300F00F
    values = (values | (values << 4)) & 0x030C30C3
    return (values | (values << 2)) & 0x09249249
