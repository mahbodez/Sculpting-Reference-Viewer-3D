"""Minimal, dependency-free Wavefront OBJ reader.

Only the geometry statements a reference viewer needs are honoured: ``v``,
``vn`` and ``f``.  Materials, texture coordinates and groups are parsed far
enough to be skipped safely.

Parsing runs in numpy wherever the file is regular -- one statement per line,
one space between fields -- because a scan mesh can be hundreds of megabytes
and a per-character Python loop is the difference between a blink and a stall.
Anything the fast path cannot vouch for falls through to a plain reader that
handles the awkward cases one line at a time.
"""

from __future__ import annotations

from itertools import chain
from pathlib import Path

import numpy as np

from .mesh import Mesh, MeshLoadError, compute_vertex_normals


class ObjLoadError(MeshLoadError):
    """Raised when a file cannot be interpreted as an OBJ mesh."""


def load_obj(path: str | Path) -> Mesh:
    """Load ``path`` and return a :class:`~refview.core.mesh.Mesh`.

    Faces with more than three corners are triangulated with a simple fan,
    which is correct for the convex polygons DCC tools export.  When the file
    carries no normals, smooth vertex normals are computed instead.
    """
    path = Path(path)
    try:
        data = path.read_bytes()
    except OSError as exc:  # pragma: no cover - filesystem dependent
        raise ObjLoadError(f"Cannot read {path}: {exc}") from exc

    lines = data.splitlines()
    mesh = _load_fast(lines, path.stem)
    if mesh is None:
        mesh = _load_generic(data.decode("utf-8", errors="replace"), path.stem)
    if mesh.triangle_count == 0:
        raise ObjLoadError(f"{path.name} contains no triangles")
    return mesh


# ----------------------------------------------------------------------
# Fast path
# ----------------------------------------------------------------------


def _load_fast(lines: list[bytes], name: str) -> Mesh | None:
    """Parse the statements with numpy, or return ``None`` if they look irregular."""
    positions = _float_table([line[2:] for line in lines if line[:2] == b"v "], columns=3)
    if positions is None or len(positions) == 0:
        return None
    normals = _float_table([line[3:] for line in lines if line[:3] == b"vn "], columns=3)
    if normals is None:
        return None

    faces = [line[2:].split() for line in lines if line[:2] == b"f "]
    corners = _face_corners(faces, len(positions), len(normals))
    if corners is None:
        return None
    return _assemble(positions, normals, corners, name)


def _float_table(lines: list[bytes], columns: int) -> np.ndarray | None:
    """Stack whitespace-separated numbers into an ``(n, columns)`` array."""
    if not lines:
        return np.zeros((0, columns), dtype=np.float64)
    fields = b" ".join(lines).split()
    if len(fields) % len(lines) or len(fields) // len(lines) < columns:
        return None
    try:
        values = np.array(fields, dtype=np.float64)
    except ValueError:
        return None
    return values.reshape(len(lines), -1)[:, :columns]


def _face_corners(
    faces: list[list[bytes]], vertex_count: int, normal_count: int
) -> np.ndarray | None:
    """Triangle corners as ``(t, 3, 2)`` pairs of vertex and normal indices."""
    if not faces:
        return None
    sizes = np.fromiter(map(len, faces), dtype=np.int64, count=len(faces))
    if sizes.min() < 3:
        return None  # A degenerate face; let the generic path decide what to skip.
    tokens = list(chain.from_iterable(faces))

    pairs = _index_pairs(tokens, vertex_count, normal_count)
    if pairs is None:
        return None

    # Fan-triangulate each polygon: corner 0 with every consecutive pair.
    starts = np.concatenate(([0], np.cumsum(sizes)[:-1]))
    blocks = []
    for size in np.unique(sizes):
        rows = starts[sizes == size, None] + np.arange(size)
        fan = pairs[rows]  # (faces, size, 2)
        for corner in range(1, size - 1):
            blocks.append(np.stack((fan[:, 0], fan[:, corner], fan[:, corner + 1]), axis=1))
    return np.concatenate(blocks) if blocks else None


def _index_pairs(tokens: list[bytes], vertex_count: int, normal_count: int) -> np.ndarray | None:
    """Resolve ``v``, ``v/vt``, ``v//vn`` or ``v/vt/vn`` corners to 0-based pairs.

    Every corner in a file uses the same layout in practice, so the layout is
    read off the first token and the total field count confirms it.
    """
    sample = tokens[0]
    separator, fields = (b"//", 2) if b"//" in sample else (b"/", sample.count(b"/") + 1)
    blob = b" ".join(tokens)
    if separator == b"/":
        blob = blob.replace(b"/", b" ")
    else:
        blob = blob.replace(b"//", b" ")
    values = blob.split()
    if len(values) != len(tokens) * fields:
        return None
    try:
        table = np.array(values, dtype=np.int64).reshape(-1, fields)
    except ValueError:
        return None

    vertices = _resolve(table[:, 0], vertex_count)
    if vertices is None:
        return None
    if fields == 3 or (separator == b"//" and fields == 2):
        normals = _resolve(table[:, -1], normal_count)
        if normals is None:
            return None
    else:
        normals = np.full(len(table), -1, dtype=np.int64)
    return np.stack((vertices, normals), axis=1)


def _resolve(indices: np.ndarray, count: int) -> np.ndarray | None:
    """Turn 1-based (or negative, relative) OBJ indices into 0-based ones."""
    resolved = np.where(indices > 0, indices - 1, count + indices)
    if count == 0 or resolved.min() < 0 or resolved.max() >= count:
        return None
    return resolved


def _assemble(
    positions: np.ndarray, normals: np.ndarray, corners: np.ndarray, name: str
) -> Mesh:
    """Build a mesh, sharing one output vertex per distinct corner."""
    flat = corners.reshape(-1, 2)
    # Pack the pair into a single key: uniquing one integer column is markedly
    # faster than a lexicographic sort over two.
    key = flat[:, 0] * (len(normals) + 1) + flat[:, 1] + 1
    _, first, inverse = np.unique(key, return_index=True, return_inverse=True)
    unique = flat[first]
    vertex_array = positions[unique[:, 0]].astype(np.float32)
    index_array = inverse.reshape(-1, 3).astype(np.uint32)

    has_normals = len(normals) > 0 and bool((unique[:, 1] >= 0).all())
    if has_normals:
        normal_array = normals[unique[:, 1]].astype(np.float32)
        lengths = np.linalg.norm(normal_array, axis=1, keepdims=True)
        normal_array = normal_array / np.maximum(lengths, 1e-20)
    else:
        normal_array = compute_vertex_normals(vertex_array, index_array)
    return Mesh(vertex_array, normal_array, index_array, name=name)


# ----------------------------------------------------------------------
# Generic path
# ----------------------------------------------------------------------


def _load_generic(text: str, name: str) -> Mesh:
    """Line-by-line reader for files the fast path declines."""
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
        return Mesh(np.zeros((0, 3)), np.zeros((0, 3)), np.zeros((0, 3)), name=name)

    vertex_array = np.asarray(out_positions, dtype=np.float32)
    index_array = np.asarray(triangles, dtype=np.uint32)
    normal_array = np.asarray(out_normals, dtype=np.float32)
    if not has_normals or not np.any(normal_array):
        normal_array = compute_vertex_normals(vertex_array, index_array)
    else:
        lengths = np.linalg.norm(normal_array, axis=1, keepdims=True)
        normal_array = normal_array / np.maximum(lengths, 1e-20)

    return Mesh(vertex_array, normal_array, index_array, name=name)
