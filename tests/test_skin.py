"""Skin persistence, UI wiring, relief and diffusion tables, acceleration layout."""

from dataclasses import replace

import numpy as np
import pytest

from refview.core.mesh import Mesh
from refview.core.session import Session
from refview.core.settings import ShadingMode
from refview.core.skin import SKIN_PRESETS, SkinSettings
from refview.render.skin_bvh import build_scene, texture_table
from refview.render.skin_detail import (
    LUT_LOG_MIN,
    LUT_LOG_SPAN,
    RELIEF_CELLS,
    cellular,
    diffusion_lut,
    relief_volume,
    value_noise,
)
from refview.render.skin_refinement import RefinementClock, SkinRefinement, pixel_jitter


def test_skin_session_roundtrip_and_old_defaults():
    session = Session()
    session.render.shading_mode = ShadingMode.HUMAN_SKIN
    session.render.skin = replace(SKIN_PRESETS["Deep / neutral"], radius=0.035, samples=256)
    restored = Session.from_dict(session.to_dict())
    assert restored.render.skin == session.render.skin
    assert restored.render.shading_mode is ShadingMode.HUMAN_SKIN
    old = session.to_dict()
    del old["render"]["skin"]
    assert Session.from_dict(old).render.skin == SkinSettings()
    assert ShadingMode.CONTOUR.shader_id == 7
    assert ShadingMode.HUMAN_SKIN.uses_lighting


def test_bad_loaded_parameters_cannot_poison_history():
    skin = SkinSettings(roughness=float("nan"), radius=-2, samples=10**9,
                        color=(float("inf"), 0, 0), scatter_color=(1,))
    valid = skin.bounded()
    assert valid.roughness == SkinSettings().roughness
    assert valid.radius > 0
    assert valid.samples == 1024
    assert valid.color == SkinSettings().color
    assert valid.scatter_color == SkinSettings().scatter_color
    detail = SkinSettings(detail=9.0, pore_size=0.0, blood=-1.0, fuzz=float("nan")).bounded()
    assert detail.detail == 2.0 and detail.pore_size == 0.0005
    assert detail.blood == 0.0 and detail.fuzz == SkinSettings().fuzz


def test_old_sessions_without_relief_fields_load_with_defaults():
    session = Session()
    session.render.skin = replace(SKIN_PRESETS["Fair / rosy"], pore_size=0.002)
    data = session.to_dict()
    for name in ("detail", "pore_size", "mottle", "blood", "fuzz"):
        del data["render"]["skin"][name]
    restored = Session.from_dict(data).render.skin
    assert restored.color == SKIN_PRESETS["Fair / rosy"].color
    assert (restored.detail, restored.pore_size) == (SkinSettings().detail, SkinSettings().pore_size)


def test_relief_volume_tiles_seamlessly_and_stores_unitless_slopes():
    volume = relief_volume(size=32, cells=4, seed=3)
    assert volume.shape == (32, 32, 32, 4) and volume.dtype == np.float32
    assert np.all(np.isfinite(volume))
    tone = volume[..., 3]
    assert tone.min() >= 0.0 and tone.max() <= 1.0
    # A central difference across the wrap edge is as smooth as one inside:
    # the slope field is periodic by construction, so seams cannot appear.
    for axis in range(3):
        edge = np.abs(np.take(volume, 0, axis) - np.take(volume, -1, axis))[..., :3]
        inner = np.abs(np.take(volume, 16, axis) - np.take(volume, 15, axis))[..., :3]
        assert edge.mean() < inner.mean() * 3.0 + 1e-3
    # Slopes are height per cell width, so a pore is a few tenths at most.
    assert 0.05 < np.abs(volume[..., :3]).mean() < 0.6
    assert np.abs(volume[..., :3]).max() < 4.0
    assert not np.array_equal(relief_volume(size=16, cells=2, seed=1),
                              relief_volume(size=16, cells=2, seed=2))


def test_cellular_and_value_noise_wrap():
    rng = np.random.default_rng(0)
    f1, f2 = cellular(24, 3, rng)
    assert np.all(f2 >= f1) and f1.min() >= 0.0
    assert f1.max() < 3.0 ** 0.5  # Never further than a cell diagonal.
    noise = value_noise(24, 2, rng)
    assert noise.min() >= 0.0 and noise.max() <= 1.0
    # Interpolation is continuous across the tile boundary.
    for axis in range(3):
        wrap = np.abs(np.take(noise, 0, axis) - np.take(noise, -1, axis)).max()
        assert wrap < 0.25


def test_diffusion_table_is_lambert_when_flat_and_wraps_when_curved():
    table = diffusion_lut(size=32, steps=512)
    assert table.shape == (32, 32, 4)
    profile = table[..., 0]
    assert np.all(np.diff(profile, axis=1) >= -1e-5)  # Brighter as the light rises.
    cosine = np.linspace(-1.0, 1.0, 32)
    lambert = np.maximum(cosine, 0.0)
    assert np.allclose(profile[-1], lambert, atol=0.02)   # Huge sphere: no wrap.
    assert profile[0, 0] > 0.15                            # Tiny sphere: lit all round.
    assert profile[0, -1] < profile[-1, -1]                # ...and flatter overall.
    radius = 2.0 ** (LUT_LOG_MIN + LUT_LOG_SPAN)
    assert radius == 64.0 and RELIEF_CELLS == 8


def test_history_resets_on_changes_and_held_navigation():
    clock = RefinementClock()
    assert not clock.ready("camera one", 10.0)
    assert not clock.ready("camera one", 10.1)
    assert clock.ready("camera one", 10.3)
    clock.samples = 42
    assert not clock.ready("camera two", 11.0)
    assert clock.samples == 0
    assert not clock.ready("camera two", 12.0, interactive=True)
    assert not clock.ready("camera two", 12.1)
    assert clock.ready("camera two", 12.3)


def test_subpixel_samples_are_bounded_and_centred():
    offsets = np.array([pixel_jitter(i) for i in range(128)])
    assert np.all(np.abs(offsets) <= 0.5)
    assert np.all(np.abs(offsets.mean(axis=0)) < 0.02)
    assert len(np.unique(offsets, axis=0)) == 128


def test_obsolete_worker_result_is_discarded_without_touching_gl(monkeypatch):
    from concurrent.futures import Future

    refinement = SkinRefinement()
    refinement.clock.key = "current"
    refinement.clock.changed = 0
    future = Future()
    future.set_result(build_scene([]))
    refinement.pending = ("old geometry", future)
    monkeypatch.setattr("refview.render.skin_refinement.monotonic", lambda: 1.0)
    assert not refinement.prepare("current", "new geometry", [], SkinSettings(), False, True)
    assert refinement.pending is None
    assert refinement.revision is None
    assert refinement.needs_frame


def test_worker_failure_leaves_a_preview_and_stops_repainting(monkeypatch):
    from concurrent.futures import Future

    refinement = SkinRefinement()
    refinement.clock.key = "current"
    refinement.clock.changed = 0
    future = Future()
    future.set_exception(MemoryError("geometry allocation failed"))
    refinement.pending = ("geometry", future)
    monkeypatch.setattr("refview.render.skin_refinement.monotonic", lambda: 1.0)
    assert not refinement.prepare("current", "geometry", [], SkinSettings(), False, True)
    assert not refinement.tracing
    assert not refinement.needs_frame
    assert "geometry allocation failed" in refinement.status


def test_bvh_covers_all_triangles_and_escape_links_skip_subtrees():
    rng = np.random.default_rng(12)
    positions = rng.normal(size=(90, 3)).astype(np.float32)
    mesh = Mesh(positions, np.tile([0, 1, 0], (90, 1)), np.arange(90).reshape(-1, 3))
    scene = build_scene([(mesh, 0, (0.7, 0.5, 0.4))])
    nodes = scene.nodes
    assert int(nodes[0, 0, 3]) == len(nodes)
    seen = []

    def visit(index):
        node = nodes[index]
        count, start = int(node[2, 3]), int(node[1, 3])
        escape = int(node[0, 3])
        assert index < escape <= len(nodes)
        if count:
            corners = scene.triangles[start:start+count, :3, :3]
            assert np.all(corners >= node[0, :3])
            assert np.all(corners <= node[1, :3])
            assert escape == index + 1
            seen.extend(range(start, start+count))
        else:
            left = index + 1
            right = int(nodes[left, 0, 3])
            visit(left)
            visit(right)
            assert int(nodes[right, 0, 3]) == escape
    visit(0)
    assert sorted(seen) == list(range(mesh.triangle_count))
    assert sorted(scene.triangles[:, 0, 0]) == sorted(mesh.triangles[:, 0, 0])


def test_packing_and_empty_scene():
    scene = build_scene([])
    assert scene.nodes.size == scene.triangles.size == 0
    assert texture_table(scene.nodes, 8).shape == (1, 1, 4)
    values = np.arange(15*4, dtype=np.float32).reshape(15, 4)
    table = texture_table(values, 4)
    assert table.shape == (4, 4, 4)
    np.testing.assert_array_equal(table.reshape(-1, 4)[:15], values)
    with pytest.raises(ValueError, match="capacity"):
        texture_table(np.zeros((17, 4)), 4)


def test_controls_and_presets_write_to_saved_material():
    import os
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication

    from refview.ui.panels.shading_panel import ShadingPanel
    from refview.ui.state import ViewerState
    app = QApplication.instance() or QApplication([])
    state = ViewerState()
    panel = ShadingPanel(state)
    panel._mode.setCurrentIndex(panel._mode.findData("human_skin"))
    assert state.render.shading_mode is ShadingMode.HUMAN_SKIN
    assert not panel._skin_box.isHidden()
    assert panel._surface_box.isHidden()
    state.render.skin.samples = 512
    panel._apply_skin_preset(panel._skin_preset.findText("Deep / neutral"))
    assert state.render.skin.color == SKIN_PRESETS["Deep / neutral"].color
    assert state.render.skin.samples == 512
    panel._skin_controls["sss"].valueChanged.emit(0.8)
    assert state.render.skin.sss == 0.8
    assert panel._skin_preset.currentText() == "Custom"
    panel._skin_controls["pore_size"].valueChanged.emit(0.002)
    panel._skin_controls["blood"].valueChanged.emit(0.9)
    assert state.render.skin.pore_size == 0.002 and state.render.skin.blood == 0.9
    # Tone comes from the preset; the model-dependent relief scale is kept.
    panel._apply_skin_preset(panel._skin_preset.findText("Fair / rosy"))
    assert state.render.skin.blood == SKIN_PRESETS["Fair / rosy"].blood
    assert state.render.skin.pore_size == 0.002
    assert state.render.skin.sss == SKIN_PRESETS["Fair / rosy"].sss
    panel.refresh()
    assert state.render.skin.pore_size == 0.002
    panel._reset()
    assert state.render.skin == SkinSettings()
    panel.close()
    app.processEvents()


def test_marks_and_body_regions_write_to_the_material_and_presets_leave_them_alone():
    import os
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from PySide6.QtWidgets import QApplication

    from refview.core.body_regions import BodyRegionSettings, RegionSource
    from refview.ui.panels.shading_panel import ShadingPanel
    from refview.ui.state import ViewerState
    app = QApplication.instance() or QApplication([])
    state = ViewerState()
    panel = ShadingPanel(state)
    panel._mode.setCurrentIndex(panel._mode.findData("human_skin"))
    assert not panel._body_box.isHidden()
    panel._skin_controls["acne"].valueChanged.emit(0.4)
    panel._skin_controls["nevi"].valueChanged.emit(0.3)
    panel._skin_controls["freckles"].valueChanged.emit(0.7)
    panel._skin_controls["blemishes"].valueChanged.emit(0.2)
    skin = state.render.skin
    assert (skin.acne, skin.nevi, skin.freckles, skin.blemishes) == (0.4, 0.3, 0.7, 0.2)
    # The marks are a person's, not a complexion's: a preset keeps them.
    panel._apply_skin_preset(panel._skin_preset.findText("Tan / olive"))
    skin = state.render.skin
    assert (skin.acne, skin.nevi, skin.freckles, skin.blemishes) == (0.4, 0.3, 0.7, 0.2)

    # The region being edited is the one the sliders write to.
    panel._region_edited.setCurrentIndex(panel._region_edited.findData("hands"))
    panel._region_controls["acne"].valueChanged.emit(2.0)
    assert skin.regions.hands.acne == 2.0 and skin.regions.head.acne == 1.0
    panel._region_edited.setCurrentIndex(panel._region_edited.findData("head"))
    assert panel._region_controls["acne"].value() == pytest.approx(1.0)
    panel._region_source.setCurrentIndex(panel._region_source.findData("whole"))
    assert skin.regions.source is RegionSource.WHOLE
    assert panel._body_form.isRowVisible(panel._region_whole)
    panel._region_whole.setCurrentIndex(panel._region_whole.findData("feet"))
    assert skin.regions.whole == "feet"
    panel._region_source.setCurrentIndex(panel._region_source.findData("auto"))
    assert panel._body_form.isRowVisible(panel._region_whole) is False
    panel._reset_regions()
    assert state.render.skin.regions == BodyRegionSettings()
    # Another shading mode hides the group along with the rest of the skin.
    panel._mode.setCurrentIndex(panel._mode.findData("matcap"))
    assert panel._body_box.isHidden()
    panel.close()
    app.processEvents()
