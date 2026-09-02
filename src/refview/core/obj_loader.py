"""Minimal, dependency-free Wavefront OBJ reader.

Only the geometry statements a reference viewer needs are honoured: ``v``,
``vn`` and ``f``.  Materials, texture coordinates and groups are parsed far
enough to be skipped safely.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .mesh import Mesh, compute_vertex_normals


class ObjLoadError(RuntimeError):
    """Raised when a file cannot be interpreted as an OBJ mesh."""


def load_obj(path: str | Path) -> Mesh:
    """Load ``path`` and return a :class:`~refview.core.mesh.Mesh`.

    Faces with more than three corners are triangulated with a simple fan,
    which is correct for the convex polygons DCC tools export.  When the file
    carries no normals, smooth vertex normals are computed instead.
    """
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:  # pragma: no cover - filesystem dependent
        raise ObjLoadError(f"Cannot read {path}: {exc}") from exc

    positions: list[tuple[float, float, float]] = []
    normals: list[tuple[float, float, float]] = []
    # Maps an OBJ corner ("v/vt/vn" token) onto an index in the output buffers.
    corner_cache: dict[str, int] = {}
    out_positions: list[tuple[float, float, float]] = []
    out_normals: list[tuple[float, float, float]] = []
    triangles: list[tuple[int, int, int]] = []
    has_normals = True

    def corner_index(token: str) -> int:
        cached = corner_cache.get(token)
        if cached is not None:
            return cached
        parts = token.split("/")
        try:
            vi = int(parts[0])
        except ValueError as exc:
            raise ObjLoadError(f"Malformed face corner {token!r}") from exc
        vi = vi - 1 if vi > 0 else len(positions) + vi
        if not 0 <= vi < len(positions):
            raise ObjLoadError(f"Face references undefined vertex {token!r}")

        ni = None
        if len(parts) > 2 and parts[2]:
            ni = int(parts[2])
            ni = ni - 1 if ni > 0 else len(normals) + ni
            if not 0 <= ni < len(normals):
                ni = None

        index = len(out_positions)
        out_positions.append(positions[vi])
        out_normals.append(normals[ni] if ni is not None else (0.0, 0.0, 0.0))
        corner_cache[token] = index
        return index

    for line in text.splitlines():
        if not line or line[0] == "#":
            continue
        tag, _, rest = line.partition(" ")
        if tag == "v":
            values = rest.split()
            positions.append((float(values[0]), float(values[1]), float(values[2])))
        elif tag == "vn":
            values = rest.split()
            normals.append((float(values[0]), float(values[1]), float(values[2])))
        elif tag == "f":
            corners = [corner_index(tok) for tok in rest.split()]
            if len(corners) < 3:
                continue
            if not normals:
                has_normals = False
            for i in range(1, len(corners) - 1):
                triangles.append((corners[0], corners[i], corners[i + 1]))

    if not triangles:
        raise ObjLoadError(f"{path.name} contains no triangles")

    vertex_array = np.asarray(out_positions, dtype=np.float32)
    index_array = np.asarray(triangles, dtype=np.uint32)
    normal_array = np.asarray(out_normals, dtype=np.float32)
    if not has_normals or not np.any(normal_array):
        normal_array = compute_vertex_normals(vertex_array, index_array)
    else:
        lengths = np.linalg.norm(normal_array, axis=1, keepdims=True)
        normal_array = normal_array / np.maximum(lengths, 1e-20)

    return Mesh(vertex_array, normal_array, index_array, name=path.stem)
