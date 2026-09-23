"""Bounding-volume hierarchy tables for the OpenGL 3.3 skin tracer.

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

Each interior node stores both children's boxes, so the tracer tests the two
at once, walks into the nearer and keeps the farther on a short stack -- the
nearest hit is usually found in the first leaf reached, and everything
behind it is then culled by distance.  Four RGBA texels a node:

    child 0 lower corner, child 0 reference
    child 0 upper corner, child 1 reference
    child 1 lower corner, unused
    child 1 upper corner, unused

A reference of zero or more is an interior node's row; a negative one ``r``
is a leaf whose triangles start at ``-r - 1`` and run to the one flagged last.

Triangles are two tables of three texels, one for the intersection test and
one read only for the nearest hit:

    corner 0, flags (material + 2 if last in its leaf)   normal 0, red
    edge 1, degeneracy threshold                         normal 1, green
    edge 2, unused                                       normal 2, blue

Material zero is the skin model; anything else is furniture of the colour
carried in the second table.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..core.mesh import Mesh

#: The most triangles a leaf is let hold, and how many it may hold before
#: the heuristic is even asked.  Four is the usual answer on a GPU: one more
#: triangle test costs less than one more box pair.
_LEAF_SIZE = 4
_MAX_LEAF = 16
#: Bins per split.  Twelve is where more stops paying for itself.
_BINS = 12
#: What a node costs to step into, against one triangle test.
_TRAVERSAL_COST = 1.2
#: Widest a table is laid out; a power of two so the shader can find a
#: texel with a shift and a mask rather than a division.
_TABLE_WIDTH = 2048


@dataclass
class TraceScene:
    nodes: np.ndarray       # (interior nodes, 4, 4)
    triangles: np.ndarray   # (triangles, 3, 4): the intersection table
    attributes: np.ndarray  # (triangles, 3, 4): normals and colour


def _area(low: np.ndarray, high: np.ndarray) -> np.ndarray:
    """Half the surface area of boxes; nought for an empty (inverted) one."""
    d = np.maximum(high - low, 0.0)
    return d[..., 0] * d[..., 1] + d[..., 1] * d[..., 2] + d[..., 2] * d[..., 0]


def build_bvh(minimum: np.ndarray, maximum: np.ndarray):
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

        leaf = (lengths <= _LEAF_SIZE) | ((lengths <= _MAX_LEAF) & (split_cost >= lengths))
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


def build_scene(parts: list[tuple[Mesh, int, tuple]]) -> TraceScene:
    """Build on a worker from the immutable meshes currently drawn by the renderer."""
    corners, normals, materials, colors = [], [], [], []
    for mesh, material, color in parts:
        if not mesh.triangle_count:
            continue
        corners.append(np.asarray(mesh.triangles, dtype=np.float64))
        normals.append(np.asarray(mesh.normals[mesh.indices], dtype=np.float32))
        materials.append(np.full(mesh.triangle_count, float(material)))
        colors.append(np.tile(np.asarray(color, dtype=np.float32), (mesh.triangle_count, 1)))
    if not corners:
        empty = np.zeros((0, 3, 4), np.float32)
        return TraceScene(np.zeros((0, 4, 4), np.float32), empty, empty.copy())
    corner = np.concatenate(corners)
    normal = np.concatenate(normals)
    material = np.concatenate(materials)
    color = np.concatenate(colors)

    order, low, high, kids, runs = build_bvh(corner.min(axis=1), corner.max(axis=1))

    # Only interior nodes get a row; a leaf lives in its parent's reference.
    interior = np.flatnonzero(kids[:, 0] >= 0)
    if len(interior) == 0:
        # The whole scene is one leaf: stand a root over it with an empty
        # second child, so the tracer has a node to start from.
        row_of = np.full(len(kids), -1, dtype=np.int64)
        nodes = np.zeros((1, 4, 4), np.float32)
        nodes[0, 0, :3], nodes[0, 1, :3] = low[0], high[0]
        nodes[0, 0, 3] = -(runs[0, 0] + 1)
        nodes[0, 2, :3], nodes[0, 3, :3] = 3.0e38, -3.0e38
        nodes[0, 1, 3] = -1.0
    else:
        row_of = np.full(len(kids), -1, dtype=np.int64)
        row_of[interior] = np.arange(len(interior))
        nodes = np.zeros((len(interior), 4, 4), np.float32)
        for slot, (corner_low, corner_high, ref) in enumerate(((0, 1, (0, 3)), (2, 3, (1, 3)))):
            child = kids[interior, slot]
            nodes[:, corner_low, :3] = low[child]
            nodes[:, corner_high, :3] = high[child]
            is_leaf = kids[child, 0] < 0
            reference = np.where(is_leaf, -(runs[child, 0] + 1), row_of[child])
            nodes[:, ref[0], ref[1]] = reference

    # Flag the last triangle of every leaf, so the shader can stop there.
    last = np.zeros(len(order), dtype=bool)
    leaf_runs = runs[runs[:, 0] >= 0]
    last[leaf_runs[:, 1] - 1] = True

    p = corner[order]
    e1 = p[:, 1] - p[:, 0]
    e2 = p[:, 2] - p[:, 0]
    triangles = np.zeros((len(order), 3, 4), np.float32)
    triangles[:, 0, :3] = p[:, 0]
    triangles[:, 0, 3] = material[order] + 2.0 * last
    triangles[:, 1, :3] = e1
    # The determinant below which a triangle is too thin to trust, scaled to
    # its own size so a model in millimetres and one in metres agree.
    triangles[:, 1, 3] = 1e-12 * np.linalg.norm(e1, axis=1) * np.linalg.norm(e2, axis=1)
    triangles[:, 2, :3] = e2
    attributes = np.zeros((len(order), 3, 4), np.float32)
    attributes[:, :, :3] = normal[order]
    attributes[:, :, 3] = color[order]
    return TraceScene(nodes, triangles, attributes)


def table_width(limit: int) -> int:
    """How wide the tables are laid out under a driver's texture limit: a power of two."""
    width = 1
    while width * 2 <= min(int(limit), _TABLE_WIDTH):
        width *= 2
    return width


def texture_table(values: np.ndarray, limit: int) -> np.ndarray:
    """Pack a linear texel array within the driver's actual 2D texture limit.

    Always :func:`table_width` wide, whatever the length, so every table the
    tracer reads shares one layout and one shift.
    """
    values = values.reshape(-1, 4)
    width = table_width(limit)
    # Float32 indices must also represent every integer exactly.
    if len(values) > min(width * int(limit), 2**24):
        raise ValueError("This mesh exceeds the skin tracer's texture capacity")
    height = max(1, (len(values) + width - 1) // width)
    table = np.zeros((height * width, 4), np.float32)
    table[:len(values)] = values
    return table.reshape(height, width, 4)
