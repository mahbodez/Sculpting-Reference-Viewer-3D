"""The path tracer's tree and rays, against brute force."""

from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("numba")

from refview.core.mesh import Mesh  # noqa: E402
from refview.core.raycast import raycast_many  # noqa: E402
from refview.trace.geometry import CAP_HIT, MISS, any_rays, cast_rays, flatten  # noqa: E402
from trace_scenes import sphere  # noqa: E402


def _soup(count=1500, seed=3):
    rng = np.random.default_rng(seed)
    centers = rng.normal(size=(count, 3))
    tris = centers[:, None, :] + rng.normal(scale=0.12, size=(count, 3, 3))
    return tris


def _geometry(tris, planes=None, cap=-1, opacity=None):
    n = len(tris)
    normals = np.zeros_like(tris)
    normals[..., 2] = 1.0
    return flatten(tris, normals, np.zeros(n, np.int32),
                   np.ones(n, np.float32) if opacity is None else opacity,
                   np.zeros((0, 4)) if planes is None else planes, cap)


def _sphere_geometry(mesh, planes, cap):
    count = mesh.triangle_count
    return flatten(mesh.triangles, mesh.normals[mesh.indices], np.zeros(count, np.int32),
                   np.ones(count, np.float32), planes, cap)


def _rays(count, seed=5, spread=3.0):
    rng = np.random.default_rng(seed)
    origins = rng.normal(size=(count, 3)) * spread
    directions = rng.normal(size=(count, 3))
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    return origins, directions


def _cast(geo, origins, directions, reach=1e30):
    tri = np.empty(len(origins), np.int32)
    dist = np.empty(len(origins))
    cast_rays(geo, origins, directions, reach, tri, dist)
    return tri, dist


def test_nearest_hit_matches_brute_force_on_a_soup():
    tris = _soup()
    geo = _geometry(tris)
    origins, directions = _rays(3000)
    _tri, dist = _cast(geo, origins, directions)
    corners = tris.size // 3
    mesh = Mesh(positions=tris.reshape(-1, 3), normals=np.tile([0.0, 0.0, 1.0], (corners, 1)),
                indices=np.arange(corners, dtype=np.uint32).reshape(-1, 3))
    reference = np.array([h.distance if h is not None else -1.0
                          for h in raycast_many(origins, directions, mesh)])
    assert (reference > 0).sum() > 100
    np.testing.assert_allclose(dist, reference, atol=1e-5)
    blocked = np.empty(len(origins), np.bool_)
    any_rays(geo, origins, directions, 1e30, blocked)
    np.testing.assert_array_equal(blocked, reference > 0)


def test_rays_from_inside_a_closed_sphere_never_escape():
    mesh = sphere(24)
    geo = _sphere_geometry(mesh, np.zeros((0, 4)), -1)
    rng = np.random.default_rng(0)
    count = 20000
    origins = rng.normal(size=(count, 3)) * 0.05
    directions = rng.normal(size=(count, 3))
    # Aim some straight along the axes and at the poles, where edges meet.
    directions[:6] = np.eye(3).repeat(2, axis=0) * np.tile([1.0, -1.0], 3)[:, None]
    origins[:6] = 0.0
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    tri, dist = _cast(geo, origins, directions)
    assert (tri >= 0).all()
    assert np.all(dist > 0.7) and np.all(dist < 1.3)


def test_the_reach_bounds_the_search():
    geo = _geometry(np.array([[[-1, -1, 0], [1, -1, 0], [0, 1, 0]]], float))
    origins = np.array([[0.0, 0.0, 2.0], [0.0, 0.0, 2.0]])
    directions = np.array([[0.0, 0.0, -1.0], [0.0, 0.0, 1.0]])
    tri, dist = _cast(geo, origins, directions, reach=1.5)
    assert tri[0] == MISS and tri[1] == MISS
    tri, dist = _cast(geo, origins, directions, reach=5.0)
    assert tri[0] == 0 and dist[0] == pytest.approx(2.0)


def test_one_triangle_and_no_triangles():
    geo = _geometry(np.array([[[-1, -1, 0], [1, -1, 0], [0, 1, 0]]], float))
    tri, _ = _cast(geo, np.array([[0.0, 0.0, 1.0]]), np.array([[0.0, 0.0, -1.0]]))
    assert tri[0] == 0
    empty = _geometry(np.zeros((0, 3, 3)))
    tri, _ = _cast(empty, np.array([[0.0, 0.0, 1.0]]), np.array([[0.0, 0.0, -1.0]]))
    assert tri[0] == MISS


def test_section_planes_cut_hits_and_cap_the_solid():
    mesh = sphere(24)
    # Cut away x > 0.
    planes = np.array([[1.0, 0.0, 0.0, 0.0]])
    geo = _sphere_geometry(mesh, planes, -1)
    origin = np.array([[3.0, 0.0, 0.0]])
    direction = np.array([[-1.0, 0.0, 0.0]])
    # Without a cap the ray passes the cut half and meets the far side's inside.
    tri, dist = _cast(geo, origin, direction)
    assert tri[0] >= 0 and dist[0] == pytest.approx(4.0, abs=0.02)
    capped = _sphere_geometry(mesh, planes, 3)
    tri, dist = _cast(capped, origin, direction)
    assert tri[0] == CAP_HIT and dist[0] == pytest.approx(3.0)
    # A ray that stays in the kept half sees the sphere as it was.
    tri, dist = _cast(capped, np.array([[-3.0, 0.0, 0.0]]), np.array([[1.0, 0.0, 0.0]]))
    assert tri[0] >= 0 and dist[0] == pytest.approx(2.0, abs=0.02)


def test_a_ghost_is_hit_as_often_as_it_is_solid():
    tris = np.array([[[-5, -5, 0], [5, -5, 0], [0, 5, 0]]], float)
    geo = _geometry(tris, opacity=np.array([0.3], np.float32))
    count = 20000
    origins = np.tile([0.0, 0.0, 1.0], (count, 1)) + np.random.default_rng(1).normal(
        scale=0.1, size=(count, 3)) * [1, 1, 0]
    directions = np.tile([0.0, 0.0, -1.0], (count, 1))
    tri, _ = _cast(geo, origins, directions)
    assert (tri >= 0).mean() == pytest.approx(0.3, abs=0.02)
