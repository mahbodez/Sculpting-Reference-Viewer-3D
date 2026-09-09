"""Session persistence, measurements and bookmarks."""

from __future__ import annotations

import json
from itertools import pairwise

import numpy as np
import pytest

from refview.core.annotation import AnnotateMode, Stroke
from refview.core.bookmark import BookmarkStore
from refview.core.camera import Camera, Projection
from refview.core.commands import RemoveItem
from refview.core.history import BOOKMARKS, History
from refview.core.measurement import Measurement, MeasurementSettings, MeasurementStore
from refview.core.plane_axes import MAX_PLANE_AXES
from refview.core.session import Session, sidecar_path
from refview.core.settings import (
    DETAIL_CEILING,
    DETAIL_MAX,
    PlaneMode,
    PlaneSettings,
    RenderSettings,
    ShadingMode,
    lattice_fineness,
    plane_count,
)


def test_measurement_length_and_midpoint():
    measurement = Measurement(start=(0.0, 0.0, 0.0), end=(3.0, 4.0, 0.0))
    assert measurement.length == pytest.approx(5.0)
    assert np.allclose(measurement.midpoint, [1.5, 2.0, 0.0])


def test_length_formatting_uses_the_display_unit():
    settings = MeasurementSettings(unit_name="mm", unit_scale=10.0, decimals=1)
    assert settings.format_length(2.5) == "25.0 mm"


def test_store_auto_names_new_measurements():
    store = MeasurementStore()
    first = store.create(np.zeros(3), np.array([1.0, 0.0, 0.0]))
    second = store.create(np.zeros(3), np.array([0.0, 1.0, 0.0]))
    assert (first.name, second.name) == ("Measurement 1", "Measurement 2")
    assert len(store) == 2


def test_bookmarks_cycle_and_wrap():
    store = BookmarkStore()
    camera = Camera()
    for name in ("A", "B", "C"):
        store.add(name, camera)
    store.recall(0)
    assert store.cycle(1)[0] == 1
    assert store.cycle(1)[0] == 2
    assert store.cycle(1)[0] == 0
    assert store.cycle(-1)[0] == 2


def test_deleting_a_bookmark_moves_the_cycling_position():
    """Deletion goes through the undo stack, so the store only tracks position."""
    store = BookmarkStore()
    camera = Camera()
    store.add("A", camera)
    store.add("B", camera)
    History().push(RemoveItem(store.items, 0, channel=BOOKMARKS))
    store.set_current(0)
    assert [bookmark.name for bookmark in store] == ["B"]
    assert store.current_index == 0


def test_session_round_trip(tmp_path):
    camera = Camera(fov_deg=61.0, projection=Projection.ORTHOGRAPHIC)
    session = Session(
        mesh_path="bust.obj",
        camera=camera.to_dict(),
        render=RenderSettings(shading_mode=ShadingMode.PBR),
        measurement_settings=MeasurementSettings(unit_name="in", unit_scale=0.3937),
        measurements=[
            Measurement((0.0, 0.0, 0.0), (0.0, 2.0, 0.0), name="Height", locked=False)
        ],
        annotations=[
            Stroke(
                points=[(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)],
                normals=[(0.0, 1.0, 0.0), (0.0, 1.0, 0.0)],
                kind=AnnotateMode.LINE,
                width=4.5,
            )
        ],
    )
    session.render.matcap.contrast = 1.4
    session.render.planes = PlaneSettings(
        enabled=True, mode=PlaneMode.PCA, detail=42.5, show_contour=True, contour_width=3.5
    )
    path = session.save(tmp_path / "bust.refview.json")

    restored = Session.load(path)
    assert restored.render.shading_mode is ShadingMode.PBR
    assert restored.render.matcap.contrast == pytest.approx(1.4)
    assert restored.render.planes.enabled is True
    assert restored.render.planes.mode is PlaneMode.PCA
    assert restored.render.planes.detail == pytest.approx(42.5)
    assert restored.render.planes.show_contour is True
    assert restored.render.planes.contour_width == pytest.approx(3.5)
    assert restored.measurement_settings.unit_name == "in"
    assert restored.measurements[0].name == "Height"
    assert restored.measurements[0].length == pytest.approx(2.0)
    assert restored.measurements[0].locked is False
    assert Camera.from_dict(restored.camera).projection is Projection.ORTHOGRAPHIC

    stroke = restored.annotations[0]
    assert stroke.kind is AnnotateMode.LINE
    assert stroke.width == pytest.approx(4.5)
    assert stroke.point_array.shape == (2, 3)


def test_plane_detail_moves_the_plane_size_evenly():
    """The slider is linear in how much of a turn one plane covers."""
    coarsest, finest = PlaneSettings(detail=0.0), PlaneSettings(detail=100.0)
    assert coarsest.span_deg == pytest.approx(90.0)
    assert finest.span_deg == pytest.approx(8.0)
    # A full-width cell on the cube face is what leaves the six axis planes.
    assert coarsest.cell_size == pytest.approx(2.0)

    steps = [PlaneSettings(detail=d).span_deg for d in range(0, 101, 10)]
    changes = [before - after for before, after in pairwise(steps)]
    assert max(changes) == pytest.approx(min(changes))

    # A detail outside the slider is held at its end rather than extrapolated.
    assert PlaneSettings(detail=-20.0).span_deg == pytest.approx(90.0)
    assert PlaneSettings(detail=140.0).span_deg == pytest.approx(8.0)


def test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else():
    """The slider's own end already asks for every plane a fit will give, so
    what a number typed past it can still buy is the lattice the form is worked
    on -- and nothing below the end may move a hair, because every setting
    anyone has saved is down there.
    """
    for detail in (0.0, 25.0, 60.0, 99.0, DETAIL_MAX):
        assert lattice_fineness(detail) == pytest.approx(1.0)
    assert lattice_fineness(-40.0) == pytest.approx(1.0)

    finer = [lattice_fineness(d) for d in (120.0, 150.0, DETAIL_CEILING)]
    assert finer == pytest.approx([1.2, 1.5, DETAIL_CEILING / DETAIL_MAX])
    assert all(later > earlier for earlier, later in pairwise(finer))

    # The count of planes is done climbing by then, which is the whole reason
    # the extra range spends itself somewhere else.
    assert plane_count(DETAIL_CEILING) == plane_count(DETAIL_MAX) == MAX_PLANE_AXES
    assert PlaneSettings(sculpt_detail=DETAIL_CEILING).sculpt_fineness > 1.0
    assert PlaneSettings(sculpt_detail=60.0).sculpt_fineness == pytest.approx(1.0)


def test_the_slider_climbs_to_the_plane_count_by_proportion_not_by_step():
    """A step of the slider is worth a fixed share more planes, not a fixed
    number of them.

    Going from four planes to five redraws a form and going from two hundred
    to two hundred and one is invisible, so a slider that added a constant
    number per step would spend most of its travel doing nothing an eye could
    see, and would have no resolution left where the blocking-in happens.
    """
    assert PlaneSettings(detail=100.0).axis_count == MAX_PLANE_AXES
    assert PlaneSettings(detail=0.0).axis_count == 2

    counts = [PlaneSettings(detail=d).axis_count for d in range(0, 101, 10)]
    assert all(after >= before for before, after in pairwise(counts))
    # Equal steps of the slider multiply the count by roughly equal factors.
    # Roughly, because a count is a whole number of planes and the rounding
    # tells at the coarse end, where a step is worth a plane or two.
    ideal = (MAX_PLANE_AXES / 2.0) ** 0.1
    factors = [after / before for before, after in pairwise(counts)]
    assert all(0.85 * ideal < factor < 1.15 * ideal for factor in factors)

    # One plane would shade the whole model flat, so the coarse end holds at two.
    assert PlaneSettings(detail=-20.0).axis_count == 2
    assert PlaneSettings(detail=140.0).axis_count == MAX_PLANE_AXES


def test_raising_the_ceiling_left_the_settings_people_already_have_alone():
    """The ceiling went from 64 planes to 256 without moving the slider under
    anyone: a session saved at the default detail reopens on the same form it
    was left on, because the climb is proportional rather than a fraction of
    the maximum.  Read straight, the default would have jumped from 38 planes
    to 154.
    """
    assert PlaneSettings().axis_count == 37
    assert PlaneSettings(detail=50.0).axis_count == 23


def test_the_design_matrix_coefficients_reach_the_fitters():
    """The panel edits the settings; the fit has to be told what they are."""
    planes = PlaneSettings(locality=0.25, coplanarity=1.5, flat_span_deg=12.0)
    assert planes.coefficients.locality == pytest.approx(0.25)
    assert planes.coefficients.coplanarity == pytest.approx(1.5)
    assert planes.coefficients.flat_span_deg == pytest.approx(12.0)
    # Frozen and comparable, so the renderer can key a cached fit on them.
    assert planes.coefficients == PlaneSettings(
        locality=0.25, coplanarity=1.5, flat_span_deg=12.0
    ).coefficients
    assert planes.coefficients != PlaneSettings().coefficients
    assert hash(planes.coefficients) == hash(planes.coefficients)


def test_only_the_modes_that_read_the_surface_care_about_the_coefficients():
    assert not PlaneMode.GRID.clustered
    assert not PlaneMode.PCA.clustered
    assert PlaneMode.REGIONS.clustered
    assert PlaneMode.FLATS.clustered


def test_the_plane_size_reported_is_the_one_the_running_mode_makes():
    """Both modes answer in degrees of turn, so the panel can just ask."""
    grid = PlaneSettings(detail=0.0)
    assert grid.plane_span_deg == pytest.approx(grid.span_deg)

    pca = PlaneSettings(mode=PlaneMode.PCA, detail=0.0)
    assert pca.plane_span_deg == pytest.approx(pca.axis_span_deg)
    # Two planes are two hemispheres; more planes are smaller ones.
    assert pca.axis_span_deg == pytest.approx(180.0)
    spans = [PlaneSettings(mode=PlaneMode.PCA, detail=d).axis_span_deg for d in range(10, 101, 10)]
    assert all(after < before for before, after in pairwise(spans))


def test_a_session_from_before_annotations_still_loads(tmp_path):
    """Version 1 files predate the annotation layer and the endpoint lock."""
    path = tmp_path / "v1.refview.json"
    path.write_text(
        json.dumps(
            {
                "version": 1,
                "measurements": [{"start": [0, 0, 0], "end": [1, 0, 0], "name": "Span"}],
            }
        ),
        encoding="utf-8",
    )
    session = Session.load(path)
    assert session.measurements[0].name == "Span"
    assert session.measurements[0].locked is True
    assert session.annotations == []


def test_unknown_and_missing_keys_are_tolerated(tmp_path):
    path = tmp_path / "old.refview.json"
    path.write_text(
        json.dumps({"version": 1, "render": {"shading_mode": "phong", "legacy_flag": True}}),
        encoding="utf-8",
    )
    session = Session.load(path)
    assert session.render.shading_mode is ShadingMode.PHONG
    assert session.measurements == []
    # Fields the old file never had fall back to the current defaults.
    assert session.render.surface.roughness == RenderSettings().surface.roughness


def test_sidecar_path_sits_next_to_the_model():
    assert sidecar_path("/models/bust.obj").name == "bust.refview.json"
