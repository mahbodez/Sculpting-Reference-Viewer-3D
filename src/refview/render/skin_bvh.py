"""Stackless BVH tables for the OpenGL 3.3 skin tracer (no compute extension).

Nodes have three RGBA texels: min/escape, max/first triangle, unused/count.
Preorder layout makes the first child node+1; escape skips the entire subtree.
Triangles have six texels: three corners, then three interpolated normals.
The corner w components store a material id, followed by two unused values;
normal w components store furniture RGB. Material zero is the skin model.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..core.mesh import Mesh


@dataclass
class TraceScene:
    nodes: np.ndarray
    triangles: np.ndarray


def build_scene(parts: list[tuple[Mesh, int, tuple]]) -> TraceScene:
    """Build on a worker from the immutable meshes currently drawn by the renderer."""
    tables = []
    for mesh, material, color in parts:
        if not mesh.triangle_count:
            continue
        table = np.zeros((mesh.triangle_count, 6, 4), dtype=np.float32)
        table[:, :3, :3] = mesh.triangles
        table[:, 3:, :3] = mesh.normals[mesh.indices]
        table[:, 0, 3] = material
        table[:, 3:, 3] = color
        tables.append(table)
    if not tables:
        return TraceScene(np.zeros((0, 3, 4), np.float32), np.zeros((0, 6, 4), np.float32))
    triangles = np.concatenate(tables)
    minimum = triangles[:, :3, :3].min(axis=1)
    maximum = triangles[:, :3, :3].max(axis=1)
    centers = (minimum + maximum) * 0.5
    order = np.arange(len(triangles))
    nodes = []

    def split(start: int, end: int) -> None:
        node = np.zeros((3, 4), np.float32)
        nodes.append(node)
        ids = order[start:end]
        node[0, :3] = minimum[ids].min(axis=0)
        node[1, :3] = maximum[ids].max(axis=0)
        if end - start <= 8:
            node[1, 3], node[2, 3] = start, end - start
        else:
            axis = int(np.argmax(np.ptp(centers[ids], axis=0)))
            half = len(ids) // 2
            order[start:end] = ids[np.argpartition(centers[ids, axis], half)]
            middle = start + half
            split(start, middle)
            split(middle, end)
        node[0, 3] = len(nodes)

    split(0, len(order))
    return TraceScene(np.asarray(nodes), triangles[order])


def texture_table(values: np.ndarray, limit: int) -> np.ndarray:
    """Pack a linear texel array within the driver's actual 2D texture limit."""
    values = values.reshape(-1, 4)
    # Float32 indices must also represent every integer exactly.
    if len(values) > min(limit * limit, 2**24):
        raise ValueError("This mesh exceeds the skin tracer's texture capacity")
    width = min(max(len(values), 1), min(limit, 2048))
    height = max(1, (len(values) + width - 1) // width)
    if height > limit:
        width = limit
        height = (len(values) + width - 1) // width
    table = np.zeros((height * width, 4), np.float32)
    table[:len(values)] = values
    return table.reshape(height, width, 4)
