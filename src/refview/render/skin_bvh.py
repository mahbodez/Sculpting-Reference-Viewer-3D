"""Bounding-volume hierarchy tables for the OpenGL 3.3 skin tracer.

The tree itself is built in :mod:`refview.core.bvh`.  Each interior node
stores both children's boxes, so the tracer tests the two at once, walks
into the nearer and keeps the farther on a short stack -- the nearest hit is
usually found in the first leaf reached, and everything behind it is then
culled by distance.  Four RGBA texels a node:

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

from ..core.bvh import build_bvh
from ..core.mesh import Mesh

#: Widest a table is laid out; a power of two so the shader can find a
#: texel with a shift and a mask rather than a division.
_TABLE_WIDTH = 2048


@dataclass
class TraceScene:
    nodes: np.ndarray       # (interior nodes, 4, 4)
    triangles: np.ndarray   # (triangles, 3, 4): the intersection table
    attributes: np.ndarray  # (triangles, 3, 4): normals and colour


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
