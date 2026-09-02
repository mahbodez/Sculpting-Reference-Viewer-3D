"""Ray/mesh intersection and vertex snapping."""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.mesh import Mesh
from refview.core.raycast import Hit, raycast_mesh, snap_to_vertex


@pytest.fixture
def quad() -> Mesh:
    """Two triangles covering the unit square on the z = 0 plane."""
    positions = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]], dtype=np.float32
    )
    normals = np.tile([0.0, 0.0, 1.0], (4, 1)).astype(np.float32)
    indices = np.array([[0, 1, 2], [0, 2, 3]], dtype=np.uint32)
    return Mesh(positions, normals, indices)


def test_hits_the_surface(quad):
    hit = raycast_mesh(np.array([0.3, 0.4, 5.0]), np.array([0.0, 0.0, -1.0]), quad)
    assert hit is not None
    assert np.allclose(hit.point, [0.3, 0.4, 0.0], atol=1e-6)
    assert hit.distance == pytest.approx(5.0)


def test_normal_faces_the_ray(quad):
    hit = raycast_mesh(np.array([0.3, 0.4, -5.0]), np.array([0.0, 0.0, 1.0]), quad)
    assert hit is not None
    assert hit.normal[2] < 0.0


def test_misses_return_none(quad):
    assert raycast_mesh(np.array([5.0, 5.0, 5.0]), np.array([0.0, 0.0, -1.0]), quad) is None


def test_ray_pointing_away_misses(quad):
    assert raycast_mesh(np.array([0.3, 0.4, 5.0]), np.array([0.0, 0.0, 1.0]), quad) is None


def test_closest_of_two_surfaces_wins():
    positions = np.array(
        [
            [-1.0, -1.0, 0.0], [1.0, -1.0, 0.0], [0.0, 1.0, 0.0],
            [-1.0, -1.0, 2.0], [1.0, -1.0, 2.0], [0.0, 1.0, 2.0],
        ],
        dtype=np.float32,
    )
    normals = np.tile([0.0, 0.0, 1.0], (6, 1)).astype(np.float32)
    indices = np.array([[0, 1, 2], [3, 4, 5]], dtype=np.uint32)
    mesh = Mesh(positions, normals, indices)
    hit = raycast_mesh(np.array([0.0, 0.0, 10.0]), np.array([0.0, 0.0, -1.0]), mesh)
    assert hit is not None
    assert hit.point[2] == pytest.approx(2.0)


def test_snapping_prefers_a_nearby_corner(quad):
    hit = Hit(
        point=np.array([0.05, 0.05, 0.0]),
        normal=np.array([0.0, 0.0, 1.0]),
        triangle=0,
        distance=1.0,
    )
    assert np.allclose(snap_to_vertex(hit, quad, max_distance=0.2), [0.0, 0.0, 0.0])


def test_snapping_leaves_distant_hits_alone(quad):
    hit = Hit(
        point=np.array([0.5, 0.3, 0.0]),
        normal=np.array([0.0, 0.0, 1.0]),
        triangle=0,
        distance=1.0,
    )
    assert np.allclose(snap_to_vertex(hit, quad, max_distance=0.05), [0.5, 0.3, 0.0])
