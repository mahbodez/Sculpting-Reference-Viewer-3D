"""Session persistence, measurements and bookmarks."""

from __future__ import annotations

import json

import numpy as np
import pytest

from refview.core.annotation import AnnotateMode, Stroke
from refview.core.bookmark import BookmarkStore
from refview.core.camera import Camera, Projection
from refview.core.commands import RemoveItem
from refview.core.history import BOOKMARKS, History
from refview.core.measurement import Measurement, MeasurementSettings, MeasurementStore
from refview.core.session import Session, sidecar_path
from refview.core.settings import RenderSettings, ShadingMode


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
    path = session.save(tmp_path / "bust.refview.json")

    restored = Session.load(path)
    assert restored.render.shading_mode is ShadingMode.PBR
    assert restored.render.matcap.contrast == pytest.approx(1.4)
    assert restored.measurement_settings.unit_name == "in"
    assert restored.measurements[0].name == "Height"
    assert restored.measurements[0].length == pytest.approx(2.0)
    assert restored.measurements[0].locked is False
    assert Camera.from_dict(restored.camera).projection is Projection.ORTHOGRAPHIC

    stroke = restored.annotations[0]
    assert stroke.kind is AnnotateMode.LINE
    assert stroke.width == pytest.approx(4.5)
    assert stroke.point_array.shape == (2, 3)


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
