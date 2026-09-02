"""OBJ parsing: normals, triangulation and index handling."""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.mesh import Bounds
from refview.core.obj_loader import ObjLoadError, load_obj

QUAD = """
# a unit quad on the XY plane
v 0 0 0
v 1 0 0
v 1 1 0
v 0 1 0
vn 0 0 1
f 1//1 2//1 3//1 4//1
"""

TRIANGLE_WITHOUT_NORMALS = """
v 0 0 0
v 2 0 0
v 0 2 0
f 1 2 3
"""

NEGATIVE_INDICES = """
v 0 0 0
v 1 0 0
v 0 1 0
f -3 -2 -1
"""


def write(tmp_path, text, name="mesh.obj"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_quad_is_triangulated(tmp_path):
    mesh = load_obj(write(tmp_path, QUAD))
    assert mesh.triangle_count == 2
    assert np.allclose(mesh.normals, [0.0, 0.0, 1.0])


def test_missing_normals_are_computed(tmp_path):
    mesh = load_obj(write(tmp_path, TRIANGLE_WITHOUT_NORMALS))
    assert mesh.triangle_count == 1
    assert np.allclose(np.linalg.norm(mesh.normals, axis=1), 1.0)
    assert np.allclose(np.abs(mesh.normals), [0.0, 0.0, 1.0])


def test_negative_indices_are_relative(tmp_path):
    mesh = load_obj(write(tmp_path, NEGATIVE_INDICES))
    assert mesh.triangle_count == 1
    assert mesh.vertex_count == 3


def test_empty_file_is_rejected(tmp_path):
    with pytest.raises(ObjLoadError):
        load_obj(write(tmp_path, "# nothing here\n"))


def test_recentering_moves_bounds_onto_the_origin(tmp_path):
    mesh = load_obj(write(tmp_path, QUAD)).recentered()
    assert np.allclose(mesh.bounds.center, 0.0, atol=1e-6)
    assert np.allclose(mesh.source_offset, [0.5, 0.5, 0.0])


def test_bounds_of_an_empty_point_set():
    bounds = Bounds.from_points(np.empty((0, 3)))
    assert bounds.radius > 0.0
