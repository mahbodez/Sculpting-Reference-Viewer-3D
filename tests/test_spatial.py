"""The picking accelerator: it must be fast without changing any answer."""

from __future__ import annotations

import numpy as np

from refview.core.mesh import Mesh, compute_vertex_normals
from refview.core.raycast import raycast_mesh
from refview.core.spatial import TriangleIndex


def _grid(cells: int = 24) -> Mesh:
    """A bumpy height field, so rays hit different triangles at different depths."""
    axis = np.linspace(-1.0, 1.0, cells + 1)
    x, z = np.meshgrid(axis, axis, indexing="ij")
    y = 0.2 * np.sin(x * 6.0) * np.cos(z * 6.0)
    points = np.stack((x, y, z), axis=-1).reshape(-1, 3).astype(np.float32)

    order = np.arange((cells + 1) ** 2).reshape(cells + 1, cells + 1)
    a = order[:-1, :-1].ravel()
    b = order[:-1, 1:].ravel()
    c = order[1:, 1:].ravel()
    d = order[1:, :-1].ravel()
    faces = np.concatenate((np.stack((a, b, c), 1), np.stack((a, c, d), 1))).astype(np.uint32)
    return Mesh(points, compute_vertex_normals(points, faces), faces)


def test_an_empty_index_returns_no_candidates():
    index = TriangleIndex(np.zeros((0, 3, 3), dtype=np.float32))
    assert index.leaf_count == 0
    assert index.candidates(np.zeros(3), np.array([0.0, 0.0, -1.0])).size == 0


def test_every_triangle_lands_in_exactly_one_leaf():
    mesh = _grid()
    index = mesh.spatial_index
    stored = np.unique(index.order)
    assert stored.size == mesh.triangle_count
    assert stored.min() == 0 and stored.max() == mesh.triangle_count - 1


def test_the_index_finds_the_triangle_a_ray_actually_hits():
    """The pruned candidate set must never miss the true intersection."""
    mesh = _grid()
    rng = np.random.default_rng(7)
    direction = np.array([0.0, -1.0, 0.0])
    checked = 0
    for _ in range(40):
        origin = np.array([rng.uniform(-0.9, 0.9), 2.0, rng.uniform(-0.9, 0.9)])
        hit = raycast_mesh(origin, direction, mesh)
        assert hit is not None
        assert hit.triangle in set(mesh.spatial_index.candidates(origin, direction).tolist())
        checked += 1
    assert checked == 40


def test_a_ray_that_misses_the_model_is_pruned_away():
    mesh = _grid()
    origin = np.array([5.0, 5.0, 5.0])
    direction = np.array([1.0, 1.0, 1.0]) / np.sqrt(3.0)
    assert mesh.spatial_index.candidates(origin, direction).size == 0
    assert raycast_mesh(origin, direction, mesh) is None


def test_the_index_is_built_once_and_kept():
    mesh = _grid()
    assert mesh.spatial_index is mesh.spatial_index
