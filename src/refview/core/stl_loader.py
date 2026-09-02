"""Binary and ASCII STL reader.

STL stores three loose corners per facet and declares no units, so the loader
welds identical corners back together: sharing vertices shrinks the buffers by
about two thirds and gives smooth normals something to average over.  The
per-facet normal in the file is ignored -- it is often stale, and the viewer
has a flat-shading toggle for when facets are what you want to see.
"""

from __future__ import annotations

import struct
from pathlib import Path

import numpy as np

from .mesh import Mesh, MeshLoadError, compute_vertex_normals

#: 80-byte header plus a uint32 facet count.
_HEADER_SIZE = 84
_FACET_SIZE = 50


class StlLoadError(MeshLoadError):
    """Raised when a file cannot be interpreted as an STL mesh."""


def load_stl(path: str | Path) -> Mesh:
    """Load ``path``, choosing the binary or ASCII reader by inspection."""
    path = Path(path)
    try:
        data = path.read_bytes()
    except OSError as exc:  # pragma: no cover - filesystem dependent
        raise StlLoadError(f"Cannot read {path}: {exc}") from exc

    corners = _binary_corners(data)
    if corners is None:
        corners = _ascii_corners(data)
    if corners is None or len(corners) == 0:
        raise StlLoadError(f"{path.name} contains no triangles")
    return _weld(corners, path.stem)


def _binary_corners(data: bytes) -> np.ndarray | None:
    """Facet corners from a binary STL, or ``None`` if this is not one.

    The declared facet count has to match the file length exactly; an ASCII
    file that happens to start with ``solid`` never will.
    """
    if len(data) < _HEADER_SIZE:
        return None
    (count,) = struct.unpack_from("<I", data, 80)
    if len(data) != _HEADER_SIZE + count * _FACET_SIZE or count == 0:
        return None

    # Each facet is a normal, three corners and a 2-byte attribute word; read
    # it as a padded record so numpy can skip the parts we do not need.
    record = np.dtype([("normal", "<3f4"), ("corners", "<3,3f4"), ("attribute", "<u2")])
    facets = np.frombuffer(data, dtype=record, count=count, offset=_HEADER_SIZE)
    return np.asarray(facets["corners"], dtype=np.float32)


def _ascii_corners(data: bytes) -> np.ndarray | None:
    """Facet corners from an ASCII STL."""
    if not data.lstrip()[:5].lower().startswith(b"solid"):
        return None
    values = [
        line.split()[1:4]
        for line in data.splitlines()
        if line.lstrip()[:6].lower() == b"vertex"
    ]
    if not values or len(values) % 3:
        return None
    try:
        points = np.array(values, dtype=np.float32)
    except ValueError as exc:
        raise StlLoadError("Malformed vertex in the ASCII STL") from exc
    return points.reshape(-1, 3, 3)


def _weld(corners: np.ndarray, name: str) -> Mesh:
    """Share one vertex per distinct position and recompute smooth normals."""
    flat = corners.reshape(-1, 3)
    positions, inverse = np.unique(flat, axis=0, return_inverse=True)
    indices = inverse.reshape(-1, 3).astype(np.uint32)
    positions = positions.astype(np.float32)
    return Mesh(positions, compute_vertex_normals(positions, indices), indices, name=name)
