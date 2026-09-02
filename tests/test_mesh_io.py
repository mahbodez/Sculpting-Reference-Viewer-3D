"""Reading the mesh formats the viewer imports."""

from __future__ import annotations

import json
import struct

import numpy as np
import pytest

from refview.core.mesh import MeshLoadError
from refview.core.mesh_io import load_mesh
from refview.core.obj_loader import load_obj

#: A tetrahedron, as loose triangle corners.
_CORNERS = np.array(
    [
        [[0, 0, 0], [1, 0, 0], [0, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 1]],
        [[0, 0, 0], [0, 0, 1], [1, 0, 0]],
        [[1, 0, 0], [0, 0, 1], [0, 1, 0]],
    ],
    dtype=np.float32,
)


def _write_binary_stl(path):
    facets = b"".join(
        struct.pack("<12fH", 0.0, 0.0, 0.0, *triangle.reshape(-1).tolist(), 0)
        for triangle in _CORNERS
    )
    path.write_bytes(b"\0" * 80 + struct.pack("<I", len(_CORNERS)) + facets)
    return path


def _write_ascii_stl(path):
    lines = ["solid test"]
    for triangle in _CORNERS:
        lines.append("facet normal 0 0 0")
        lines.append("  outer loop")
        lines.extend(f"    vertex {x} {y} {z}" for x, y, z in triangle)
        lines.append("  endloop")
        lines.append("endfacet")
    lines.append("endsolid test")
    path.write_text("\n".join(lines), encoding="ascii")
    return path


def _write_glb(path, scale=(1.0, 1.0, 1.0)):
    """A minimal GLB holding the tetrahedron under a scaled node."""
    points = np.unique(_CORNERS.reshape(-1, 3), axis=0).astype(np.float32)
    lookup = {tuple(point): index for index, point in enumerate(points)}
    indices = np.array(
        [[lookup[tuple(corner)] for corner in triangle] for triangle in _CORNERS],
        dtype=np.uint16,
    ).reshape(-1)
    blob = points.tobytes() + indices.tobytes()
    blob += b"\0" * (-len(blob) % 4)

    document = {
        "asset": {"version": "2.0"},
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "scale": list(scale)}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "indices": 1}]}],
        "accessors": [
            {
                "bufferView": 0,
                "componentType": 5126,
                "count": len(points),
                "type": "VEC3",
            },
            {
                "bufferView": 1,
                "componentType": 5123,
                "count": len(indices),
                "type": "SCALAR",
            },
        ],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": points.nbytes},
            {"buffer": 0, "byteOffset": points.nbytes, "byteLength": indices.nbytes},
        ],
        "buffers": [{"byteLength": len(blob)}],
    }
    json_chunk = json.dumps(document).encode("utf-8")
    json_chunk += b" " * (-len(json_chunk) % 4)
    body = (
        struct.pack("<II", len(json_chunk), 0x4E4F534A)
        + json_chunk
        + struct.pack("<II", len(blob), 0x004E4942)
        + blob
    )
    path.write_bytes(b"glTF" + struct.pack("<II", 2, 12 + len(body)) + body)
    return path


def test_binary_stl_welds_shared_corners(tmp_path):
    mesh = load_mesh(_write_binary_stl(tmp_path / "shape.stl"))
    assert mesh.triangle_count == 4
    assert mesh.vertex_count == 4  # 12 loose corners, 4 distinct positions
    assert mesh.units is None  # STL declares no unit


def test_ascii_stl_matches_the_binary_one(tmp_path):
    binary = load_mesh(_write_binary_stl(tmp_path / "shape.stl"))
    text = load_mesh(_write_ascii_stl(tmp_path / "text.stl"))
    assert text.triangle_count == binary.triangle_count
    assert np.allclose(np.sort(text.positions, axis=0), np.sort(binary.positions, axis=0))


def test_glb_applies_node_transforms_and_reports_metres(tmp_path):
    mesh = load_mesh(_write_glb(tmp_path / "shape.glb", scale=(2.0, 2.0, 2.0)))
    assert mesh.triangle_count == 4
    assert mesh.units is not None and mesh.units.name == "m"
    # The node scale doubles the tetrahedron's extent.
    assert np.allclose(mesh.bounds.size, [2.0, 2.0, 2.0])


def test_glb_computes_normals_when_the_file_has_none(tmp_path):
    mesh = load_mesh(_write_glb(tmp_path / "shape.glb"))
    lengths = np.linalg.norm(mesh.normals, axis=1)
    assert np.allclose(lengths, 1.0, atol=1e-5)


def test_an_unsupported_suffix_is_reported(tmp_path):
    path = tmp_path / "model.fbx"
    path.write_bytes(b"")
    with pytest.raises(MeshLoadError, match="unsupported"):
        load_mesh(path)


def test_obj_quads_are_triangulated(tmp_path):
    path = tmp_path / "quad.obj"
    path.write_text(
        "v 0 0 0\nv 1 0 0\nv 1 1 0\nv 0 1 0\nf 1 2 3 4\n",
        encoding="utf-8",
    )
    mesh = load_obj(path)
    assert mesh.triangle_count == 2
    assert mesh.vertex_count == 4


def test_obj_relative_indices_still_load(tmp_path):
    """Negative face indices count back from the most recent vertex."""
    path = tmp_path / "relative.obj"
    path.write_text("v 0 0 0\nv 1 0 0\nv 0 1 0\nf -3 -2 -1\n", encoding="utf-8")
    mesh = load_obj(path)
    assert mesh.triangle_count == 1
    assert np.allclose(np.sort(mesh.positions, axis=0)[-1], [1.0, 1.0, 0.0])
