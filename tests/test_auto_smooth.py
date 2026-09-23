"""AutoSmooth on a loaded model: hard past the angle, smooth short of it, kept through drags."""

from __future__ import annotations

import numpy as np

from refview.core.mesh import Mesh, SmoothingGroups, smoothed_by_angle


def _box() -> Mesh:
    """A cube sharing its eight corners, as a loader would give it: every normal averaged."""
    corners = np.array(
        [[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)], np.float32
    )
    faces = [
        (0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3),
    ]
    indices = []
    for a, b, c, d in faces:
        indices += [(a, b, c), (a, c, d)]
    normals = corners / np.linalg.norm(corners, axis=1, keepdims=True)
    return Mesh(corners, normals, np.array(indices))


def _face_normals(mesh: Mesh) -> np.ndarray:
    p = mesh.positions[mesh.indices]
    cross = np.cross(p[:, 1] - p[:, 0], p[:, 2] - p[:, 0])
    return cross / np.linalg.norm(cross, axis=1, keepdims=True)


def test_a_box_comes_out_hard_edged_and_a_high_angle_rounds_it():
    box = _box()
    hard = smoothed_by_angle(box, 30.0)
    # A vertex per corner, and every corner facing the way its face does.
    assert hard.vertex_count == 3 * box.triangle_count
    faces = np.repeat(_face_normals(box), 3, axis=0)
    np.testing.assert_allclose(hard.normals, faces, atol=1e-6)
    # Nothing moved.
    np.testing.assert_allclose(hard.positions, box.positions[box.indices.reshape(-1)])
    # Past ninety degrees the cube's edges are gentle enough to join.
    round_ = smoothed_by_angle(box, 100.0)
    corner_ways = round_.positions / np.linalg.norm(round_.positions, axis=1, keepdims=True)
    assert float(np.einsum("ij,ij->i", round_.normals, corner_ways).min()) > 0.9


def test_the_groups_found_once_shade_the_object_wherever_it_goes():
    box = _box()
    groups = SmoothingGroups(box, 30.0)
    turn = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]], np.float32)
    moved = Mesh(box.positions @ turn.T + 5.0, box.normals @ turn.T, box.indices)
    assert groups.fits(moved)
    shaded = groups.shade(moved)
    np.testing.assert_allclose(shaded.normals, smoothed_by_angle(moved, 30.0).normals, atol=1e-6)
    np.testing.assert_allclose(shaded.normals, np.repeat(_face_normals(moved), 3, axis=0),
                               atol=1e-6)
    assert not groups.fits(Mesh(box.positions, box.normals, box.indices[:6]))


def test_split_seams_are_joined_and_nought_is_flat():
    """A loader that split a vertex for its texture coordinates leaves no seam in the shading."""
    axis = np.linspace(-1.0, 1.0, 5, dtype=np.float32)
    x, y = np.meshgrid(axis, axis)
    heights = 0.2 * (x * x + y * y)
    positions = np.stack([x, y, heights], -1).reshape(-1, 3)
    index = np.arange(25).reshape(5, 5)
    quads = np.stack([index[:-1, :-1], index[1:, :-1], index[1:, 1:], index[:-1, 1:]], -1)
    triangles = np.concatenate([quads[..., [0, 1, 2]], quads[..., [0, 2, 3]]]).reshape(-1, 3)
    # Split every vertex on the middle column in two, as a UV seam does.
    seam = index[:, 2]
    duplicates = {int(v): 25 + i for i, v in enumerate(seam)}
    split_positions = np.concatenate([positions, positions[seam]])
    right = positions[triangles].mean(axis=1)[:, 0] > 0.0
    split = triangles.copy()
    for row in np.flatnonzero(right):
        split[row] = [duplicates.get(int(v), int(v)) for v in split[row]]
    mesh = Mesh(split_positions, np.tile([0, 0, 1], (30, 1)), split)
    smooth = smoothed_by_angle(mesh, 60.0)
    corners = smooth.positions
    on_seam = np.isclose(corners[:, 0], 0.0)
    # Each point on the seam has one normal, whichever side's triangle it is in.
    for point in np.unique(corners[on_seam], axis=0):
        at = np.all(np.isclose(corners, point), axis=1)
        assert np.allclose(smooth.normals[at], smooth.normals[at][0], atol=1e-6)
    flat = smoothed_by_angle(mesh, 0.0)
    np.testing.assert_allclose(flat.normals, np.repeat(_face_normals(mesh), 3, axis=0), atol=1e-6)
