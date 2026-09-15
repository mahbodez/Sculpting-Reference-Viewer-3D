"""Spatial index that keeps picking fast on large meshes.

Every click, every hover and every sample of a painted stroke casts a ray, so
the cost of a single intersection query is what decides whether the viewer
still feels direct on a million-triangle scan.

The index sorts the triangles along a Morton curve and groups the sorted order
into fixed-size leaves, each with a bounding box.  Runs of neighbouring leaves
are boxed again, and those boxes again, until a handful remain.  A query
sweeps each level in turn, vectorised, and only descends into the boxes the
ray entered, so on a two-million-triangle scan a ray touches a few hundred
boxes rather than every one of thirty thousand leaves.  That is what keeps
the overlay's occlusion test cheap enough to run for every armature node on
every frame of an orbit.  A pointer-chasing BVH would prune a little better
still, but walking one in Python costs more than the few sweeps it saves.
"""

from __future__ import annotations

import numpy as np

_EPSILON = 1e-12
#: Triangles per leaf.  Larger leaves mean fewer boxes to sweep but more
#: triangles to intersect; the product is flat enough that the exact value
#: hardly matters between roughly 32 and 256.
LEAF_SIZE = 16
#: Boxes gathered under one parent at each level above the leaves.  Wide
#: enough that a level is a few sweeps deep, narrow enough that a parent the
#: ray misses takes a good many leaves out of the running with it.
FANOUT = 8
#: Resolution of the Morton grid, per axis.
_GRID_BITS = 10


class TriangleIndex:
    """Leaf bounding boxes over a Morton-sorted triangle list."""

    __slots__ = ("order", "minimum", "maximum", "leaf_size", "_levels")

    def __init__(self, corners: np.ndarray, leaf_size: int = LEAF_SIZE) -> None:
        """Build the index from expanded triangle corners, shape ``(T, 3, 3)``."""
        corners = np.asarray(corners, dtype=np.float32).reshape(-1, 3, 3)
        self.leaf_size = max(int(leaf_size), 1)
        count = len(corners)
        if count == 0:
            self.order = np.zeros((0, self.leaf_size), dtype=np.int64)
            self.minimum = np.zeros((0, 3), dtype=np.float64)
            self.maximum = np.zeros((0, 3), dtype=np.float64)
            self._levels = []
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
        self._levels = _stack_levels(self.minimum, self.maximum)

    @property
    def leaf_count(self) -> int:
        return len(self.order)

    def candidates(self, origin: np.ndarray, direction: np.ndarray) -> np.ndarray:
        """Triangle indices worth intersecting for this ray, possibly empty."""
        origin = np.asarray(origin, dtype=np.float64)[None]
        direction = np.asarray(direction, dtype=np.float64)[None]
        _, triangles = self.candidates_many(origin, direction)
        return np.unique(triangles)

    def candidates_many(
        self, origins: np.ndarray, directions: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """Which triangles are worth intersecting for each of a batch of rays.

        Returns ``(ray, triangle)`` index pairs, one row per pairing.  A
        triangle can appear twice for the same ray where a padded leaf
        repeats it, which costs one redundant intersection and changes no
        answer.  Sweeping all the rays' boxes through each level together is
        what makes the overlay's per-node occlusion test cost about as much
        for two dozen nodes as it once did for one.
        """
        origins = np.asarray(origins, dtype=np.float64).reshape(-1, 3)
        directions = np.asarray(directions, dtype=np.float64).reshape(-1, 3)
        empty = np.zeros(0, dtype=np.int64)
        if self.leaf_count == 0 or len(origins) == 0:
            return empty, empty
        with np.errstate(divide="ignore", invalid="ignore"):
            inverse = 1.0 / np.where(np.abs(directions) < _EPSILON, _EPSILON, directions)
        top = len(self._levels[0][0])
        ray = np.repeat(np.arange(len(origins)), top)
        box = np.tile(np.arange(top), len(origins))
        for depth, (minimum, maximum) in enumerate(self._levels):
            if depth:
                # Box ``i`` of one level holds boxes ``i * FANOUT`` onward of
                # the next, so the survivors' children are a stride away.
                box = (box[:, None] * FANOUT + np.arange(FANOUT)).ravel()
                ray = np.repeat(ray, FANOUT)
                inside = box < len(minimum)
                box, ray = box[inside], ray[inside]
            with np.errstate(invalid="ignore"):
                near = (minimum[box] - origins[ray]) * inverse[ray]
                far = (maximum[box] - origins[ray]) * inverse[ray]
            entry = np.maximum(np.minimum(near, far), 0.0).max(axis=1)
            exit_ = np.maximum(near, far).min(axis=1)
            entered = exit_ >= entry
            box, ray = box[entered], ray[entered]
            if box.size == 0:
                return empty, empty
        return np.repeat(ray, self.leaf_size), self.order[box].ravel()


def _stack_levels(minimum: np.ndarray, maximum: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
    """Box the leaves up, coarsest level first and the leaves themselves last."""
    levels = [(minimum, maximum)]
    while len(levels[0][0]) > FANOUT:
        fine_min, fine_max = levels[0]
        parents = -(-len(fine_min) // FANOUT)
        # Pad the last parent with its final child, as the leaves pad
        # themselves: a repeated box changes no bound and no answer.
        padded = np.full(parents * FANOUT, len(fine_min) - 1, dtype=np.int64)
        padded[: len(fine_min)] = np.arange(len(fine_min))
        padded = padded.reshape(parents, FANOUT)
        levels.insert(0, (fine_min[padded].min(axis=1), fine_max[padded].max(axis=1)))
    return levels


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
