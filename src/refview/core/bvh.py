"""A bounding-volume hierarchy over triangle boxes, built by the surface-area heuristic.

The tree is built by the surface-area heuristic (MacDonald and Booth; binned,
after Wald): at each node the triangles are sorted into a dozen bins along
the widest spread of their centres, and the split kept is the one that
minimises the area of each side times the triangles in it -- the expected
cost of a random ray that enters the node.  A median split cuts a figure
down the middle whatever is there; this one cuts round the arm held out
from the body, which is what lets a ray going past the arm never look at it.

The build runs a level of the tree at a time, all of that level's nodes at
once as numpy arrays, so the cost is a sort or two per level rather than a
Python call per node: a few tenths of a second for a figure of sixty
thousand triangles, a few seconds for a scan of millions.

Two tracers read it: the skin refinement on the GPU packs it into textures
(:mod:`refview.render.skin_bvh`), and the CPU path tracer flattens it into
arrays (:mod:`refview.trace.geometry`).
"""

from __future__ import annotations

import numpy as np

#: The most triangles a leaf is let hold, and how many it may hold before
#: the heuristic is even asked.  Four is the usual answer on a GPU: one more
#: triangle test costs less than one more box pair.
_LEAF_SIZE = 4
_MAX_LEAF = 16
#: Bins per split.  Twelve is where more stops paying for itself.
_BINS = 12
#: What a node costs to step into, against one triangle test.
_TRAVERSAL_COST = 1.2


def _area(low: np.ndarray, high: np.ndarray) -> np.ndarray:
    """Half the surface area of boxes; nought for an empty (inverted) one."""
    d = np.maximum(high - low, 0.0)
    return d[..., 0] * d[..., 1] + d[..., 1] * d[..., 2] + d[..., 2] * d[..., 0]


def build_bvh(
    minimum: np.ndarray,
    maximum: np.ndarray,
    leaf_size: int = _LEAF_SIZE,
    max_leaf: int = _MAX_LEAF,
):
    """Build the tree over triangle boxes.

    Returns the triangle order, and per node its bounds, its two children
    (``-1`` for none) and, for a leaf, the run of the order it holds.  Nodes
    are numbered level by level from the root.
    """
    count = len(minimum)
    order = np.empty(count, dtype=np.int64)
    node_low: list[np.ndarray] = []
    node_high: list[np.ndarray] = []
    children: list[np.ndarray] = []
    leaves: list[np.ndarray] = []   # blocks of (node, start, end) rows
    # The working set: every triangle of a node still to be split, grouped
    # by node, with its box and centre alongside so that each level reads
    # them in order rather than gathering them from all over memory.
    tris = np.arange(count)
    lo = np.ascontiguousarray(minimum, dtype=np.float32)
    hi = np.ascontiguousarray(maximum, dtype=np.float32)
    centre = (lo + hi) * 0.5
    starts = np.array([0])          # where each node's run begins in ``order``
    lengths = np.array([count])
    ids = np.array([0])
    next_id = 1
    while len(starts):
        offsets = np.concatenate([[0], np.cumsum(lengths)[:-1]])
        segment = np.repeat(np.arange(len(starts)), lengths)
        low = np.minimum.reduceat(lo, offsets)
        high = np.maximum.reduceat(hi, offsets)
        node_low.append(np.column_stack([ids, low]))
        node_high.append(np.column_stack([ids, high]))

        cmin = np.minimum.reduceat(centre, offsets)
        cmax = np.maximum.reduceat(centre, offsets)
        extent = cmax - cmin
        axis = np.argmax(extent, axis=1)
        along = np.take_along_axis(centre, axis[segment][:, None], axis=1)[:, 0]
        spread = extent[np.arange(len(starts)), axis]
        origin = cmin[np.arange(len(starts)), axis]
        scale = np.where(spread > 0.0, _BINS / np.maximum(spread, 1e-30), 0.0)
        bins = np.clip(((along - origin[segment]) * scale[segment]).astype(np.int64), 0, _BINS - 1)

        # Bounds and counts per bin, per segment.
        key = segment * _BINS + bins
        slots = len(starts) * _BINS
        bin_low = np.full((slots, 3), np.inf, dtype=np.float32)
        bin_high = np.full((slots, 3), -np.inf, dtype=np.float32)
        np.minimum.at(bin_low, key, lo)
        np.maximum.at(bin_high, key, hi)
        bin_count = np.bincount(key, minlength=slots).reshape(-1, _BINS)
        bin_low = bin_low.reshape(-1, _BINS, 3)
        bin_high = bin_high.reshape(-1, _BINS, 3)

        # Every split between two bins, costed from both ends at once.
        left_low = np.minimum.accumulate(bin_low, axis=1)[:, :-1]
        left_high = np.maximum.accumulate(bin_high, axis=1)[:, :-1]
        right_low = np.minimum.accumulate(bin_low[:, ::-1], axis=1)[:, ::-1][:, 1:]
        right_high = np.maximum.accumulate(bin_high[:, ::-1], axis=1)[:, ::-1][:, 1:]
        left_count = np.cumsum(bin_count, axis=1)[:, :-1]
        right_count = lengths[:, None] - left_count
        with np.errstate(invalid="ignore"):
            cost = (_area(left_low, left_high) * left_count
                    + _area(right_low, right_high) * right_count)
        cost = np.where((left_count > 0) & (right_count > 0), cost, np.inf)
        best = np.argmin(cost, axis=1)
        best_cost = cost[np.arange(len(starts)), best]
        parent_area = np.maximum(_area(low, high), 1e-30)
        split_cost = _TRAVERSAL_COST + best_cost / parent_area
        binned = np.isfinite(best_cost)

        leaf = (lengths <= leaf_size) | ((lengths <= max_leaf) & (split_cost >= lengths))
        # Where the centres all fall in one bin -- coincident, or one huge
        # triangle among specks -- the bins cannot split them; halve by
        # rank instead so the leaf does not grow without end.
        median = ~leaf & ~binned
        side = bins > best[segment]
        if median.any():
            chosen = median[segment]
            rank_order = np.lexsort((along[chosen], segment[chosen]))
            ranks = np.empty(int(chosen.sum()), dtype=np.int64)
            ranks[rank_order] = np.arange(len(ranks))
            chosen_segment = segment[chosen]
            first_rank = np.searchsorted(chosen_segment[rank_order], chosen_segment, side="left")
            within = ranks - first_rank
            side[chosen] = within >= (lengths[chosen_segment] // 2)

        leaves.append(np.column_stack([ids[leaf], starts[leaf], starts[leaf] + lengths[leaf]]))
        # A leaf's triangles are final: write them into the order and let
        # them drop out of the working set.
        done = leaf[segment]
        if done.any():
            at = np.flatnonzero(done)
            order[at - offsets[segment[at]] + starts[segment[at]]] = tris[at]
        split = ~leaf
        if not split.any():
            break
        keep = ~done
        # Left side before right within each node; the nodes stay in order,
        # so the children come out as left, right, left, right, ...
        permutation = np.flatnonzero(keep)[np.lexsort((side[keep], segment[keep]))]
        tris, lo, hi, centre = tris[permutation], lo[permutation], hi[permutation], centre[
            permutation
        ]
        left_sizes = np.bincount(segment, weights=~side & keep, minlength=len(starts))
        left_sizes = left_sizes.astype(np.int64)[split]
        parent_starts = starts[split]
        parent_lengths = lengths[split]
        parents = ids[split]
        left_ids = next_id + 2 * np.arange(len(parents))
        next_id += 2 * len(parents)
        children.append(np.column_stack([parents, left_ids, left_ids + 1]))
        starts = np.column_stack([parent_starts, parent_starts + left_sizes]).ravel()
        lengths = np.column_stack([left_sizes, parent_lengths - left_sizes]).ravel()
        ids = np.column_stack([left_ids, left_ids + 1]).ravel()

    total = next_id
    bounds_low = np.zeros((total, 3))
    bounds_high = np.zeros((total, 3))
    for block in node_low:
        bounds_low[block[:, 0].astype(np.int64)] = block[:, 1:]
    for block in node_high:
        bounds_high[block[:, 0].astype(np.int64)] = block[:, 1:]
    kids = np.full((total, 2), -1, dtype=np.int64)
    for block in children:
        kids[block[:, 0]] = block[:, 1:]
    runs = np.full((total, 2), -1, dtype=np.int64)
    rows = np.concatenate(leaves).astype(np.int64)
    runs[rows[:, 0]] = rows[:, 1:]
    return order, bounds_low, bounds_high, kids, runs
