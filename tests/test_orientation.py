"""Turning an imported model the right way up."""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.annotation import Stroke
from refview.core.measurement import Measurement
from refview.core.mesh import Mesh, compute_vertex_normals
from refview.core.orientation import OrientationSettings, UpAxis
from refview.ui.state import ViewerState

_AXES = {UpAxis.X: (1.0, 0.0, 0.0), UpAxis.Y: (0.0, 1.0, 0.0), UpAxis.Z: (0.0, 0.0, 1.0)}


def _tower() -> Mesh:
    """A tall, thin shape lying along +Z, as a Z-up export would store it."""
    points = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 8.0],
        ],
        dtype=np.float32,
    )
    faces = np.array([[0, 1, 2], [0, 1, 3], [1, 2, 3], [0, 2, 3]], dtype=np.uint32)
    return Mesh(points, compute_vertex_normals(points, faces), faces, name="tower")


def test_every_up_axis_lands_on_world_up():
    for axis, direction in _AXES.items():
        matrix = OrientationSettings(up_axis=axis).matrix
        assert np.allclose(matrix @ np.array(direction), [0.0, 1.0, 0.0], atol=1e-12)


def test_orientations_never_mirror_the_model():
    """A negative determinant would turn the model inside out."""
    for axis in UpAxis:
        for flip in (False, True):
            matrix = OrientationSettings(up_axis=axis, flip_up=flip, spin_deg=90.0).matrix
            assert np.linalg.det(matrix) == pytest.approx(1.0)


def test_flipping_points_the_up_axis_down():
    matrix = OrientationSettings(up_axis=UpAxis.Z, flip_up=True).matrix
    assert np.allclose(matrix @ np.array([0.0, 0.0, 1.0]), [0.0, -1.0, 0.0], atol=1e-12)


def test_spin_turns_about_the_vertical():
    matrix = OrientationSettings(spin_deg=90.0).matrix
    assert np.allclose(matrix @ np.array([0.0, 0.0, 1.0]), [1.0, 0.0, 0.0], atol=1e-12)
    assert np.allclose(matrix @ np.array([0.0, 1.0, 0.0]), [0.0, 1.0, 0.0], atol=1e-12)


def test_the_file_s_own_axes_are_the_default():
    assert OrientationSettings().is_identity
    assert not OrientationSettings(up_axis=UpAxis.Z).is_identity
    assert not OrientationSettings(spin_deg=90.0).is_identity


def test_an_identity_turn_reuses_the_mesh():
    mesh = _tower()
    assert mesh.transformed(np.eye(3)) is mesh


def test_turning_a_z_up_model_stands_it_up():
    mesh = _tower()
    assert mesh.bounds.size[2] == pytest.approx(8.0)  # tallest along Z as stored
    turned = mesh.transformed(OrientationSettings(up_axis=UpAxis.Z).matrix)
    assert turned.bounds.size[1] == pytest.approx(8.0)  # and along Y afterwards
    assert turned.triangle_count == mesh.triangle_count
    assert np.allclose(np.linalg.norm(turned.normals, axis=1), 1.0, atol=1e-5)


def test_marks_follow_the_model_when_it_is_turned(tmp_path):
    """A measurement is attached to the surface, so it turns with it."""
    path = tmp_path / "tower.obj"
    path.write_text(
        "v 0 0 0\nv 1 0 0\nv 0 1 0\nv 0 0 8\nf 1 2 3\nf 1 2 4\nf 2 3 4\nf 1 3 4\n",
        encoding="utf-8",
    )
    state = ViewerState()
    state.load_mesh(path, load_sidecar=False)

    # Put a measurement on the model's highest point, whichever way it faces.
    top = state.mesh.positions[np.argmax(state.mesh.positions[:, 2])].astype(float)
    state.measurements.add(Measurement(start=tuple(top), end=(0.0, 0.0, 0.0)))
    state.annotations.add(
        Stroke(points=[tuple(top), (0.0, 0.0, 0.0)], normals=[(0.0, 0.0, 1.0), (0.0, 0.0, 1.0)])
    )

    state.set_orientation(OrientationSettings(up_axis=UpAxis.Z))
    moved = np.asarray(state.measurements[0].start)
    highest = state.mesh.positions[np.argmax(state.mesh.positions[:, 1])]
    assert np.allclose(moved, highest, atol=1e-4)
    assert np.allclose(state.annotations[0].points[0], highest, atol=1e-4)
    # The normal turned with the point rather than staying in the file's axes.
    assert np.allclose(state.annotations[0].normals[0], [0.0, 1.0, 0.0], atol=1e-6)


def test_going_back_restores_the_original_positions(tmp_path):
    path = tmp_path / "tower.obj"
    path.write_text(
        "v 0 0 0\nv 1 0 0\nv 0 1 0\nv 0 0 8\nf 1 2 3\nf 1 2 4\nf 2 3 4\nf 1 3 4\n",
        encoding="utf-8",
    )
    state = ViewerState()
    state.load_mesh(path, load_sidecar=False)
    original = state.mesh.positions.copy()
    point = tuple(float(v) for v in original[0])
    state.measurements.add(Measurement(start=point, end=point))

    state.set_orientation(OrientationSettings(up_axis=UpAxis.Z, spin_deg=90.0))
    state.set_orientation(OrientationSettings())
    assert np.allclose(state.mesh.positions, original, atol=1e-5)
    assert np.allclose(state.measurements[0].start, point, atol=1e-5)
