"""Skin persistence, UI wiring, relief and diffusion tables, acceleration layout."""

from dataclasses import replace

import numpy as np
import pytest

from refview.core.mesh import Mesh
from refview.core.session import Session
from refview.core.settings import ShadingMode
from refview.core.skin import SKIN_PRESETS, SkinSettings
from refview.core.skin_detail import (
    LUT_LOG_MIN,
    LUT_LOG_SPAN,
    RELIEF_CELLS,
    cellular,
    diffusion_lut,
    relief_volume,
    value_noise,
)
from refview.render.skin_bvh import build_scene, table_width, texture_table
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
    for name in ("detail", "pore_size", "mottle", "blood", "veins", "fuzz"):
        del data["render"]["skin"][name]
    restored = Session.from_dict(data).render.skin
    assert restored.color == SKIN_PRESETS["Fair / rosy"].color
    assert (restored.detail, restored.pore_size) == (
        SkinSettings().detail, SkinSettings().pore_size
    )
    assert restored.veins == SkinSettings().veins


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


def _leaves(scene):
    """Walk the tree: every leaf's triangles, with the box its parent keeps for it."""
    nodes, triangles = scene.nodes, scene.triangles
    found = []
    stack = [0]
    visited = set()
    while stack:
        index = stack.pop()
        assert index not in visited   # a tree, not a graph
        visited.add(index)
        node = nodes[index]
        for low, high, ref in ((node[0], node[1], node[0, 3]), (node[2], node[3], node[1, 3])):
            ref = int(ref)
            if ref >= 0:
                child = nodes[ref]
                # The child's own two boxes sit inside the box kept for it.
                for inner_low, inner_high in ((child[0], child[1]), (child[2], child[3])):
                    if inner_low[0] <= inner_high[0]:
                        assert np.all(inner_low[:3] >= low[:3] - 1e-6)
                        assert np.all(inner_high[:3] <= high[:3] + 1e-6)
                stack.append(ref)
            elif low[0] <= high[0]:
                first = -ref - 1
                run = [first]
                while triangles[run[-1], 0, 3] < 2.0:
                    run.append(run[-1] + 1)
                corners = triangles[run, 0, :3][:, None] + np.stack(
                    [np.zeros((len(run), 3)), triangles[run, 1, :3], triangles[run, 2, :3]], 1
                )
                assert np.all(corners >= low[:3] - 1e-5)
                assert np.all(corners <= high[:3] + 1e-5)
                found.append(run)
    assert visited == set(range(len(nodes)))
    return found


def test_bvh_covers_every_triangle_once_inside_its_boxes():
    rng = np.random.default_rng(12)
    positions = rng.normal(size=(900, 3)).astype(np.float32)
    mesh = Mesh(positions, np.tile([0, 1, 0], (900, 1)), np.arange(900).reshape(-1, 3))
    scene = build_scene([(mesh, 0, (0.7, 0.5, 0.4))])
    runs = _leaves(scene)
    seen = sorted(index for run in runs for index in run)
    assert seen == list(range(mesh.triangle_count))
    assert max(len(run) for run in runs) <= 16
    assert sorted(scene.triangles[:, 0, 0]) == sorted(mesh.triangles[:, 0, 0])
    # The corners come back out of the edge form the table stores them in.
    rebuilt = scene.triangles[:, 0, :3] + scene.triangles[:, 1, :3]
    assert {tuple(np.round(row, 4)) for row in rebuilt} <= {
        tuple(np.round(row, 4)) for row in mesh.triangles.reshape(-1, 3)
    }


def test_bvh_of_one_leaf_still_has_a_root():
    mesh = Mesh(np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], np.float32),
                np.tile([0, 0, 1], (3, 1)), [[0, 1, 2]])
    scene = build_scene([(mesh, 1, (0.2, 0.3, 0.4))])
    assert len(scene.nodes) == 1
    assert _leaves(scene) == [[0]]
    assert scene.triangles[0, 0, 3] == 1.0 + 2.0   # furniture, and the last of its leaf
    np.testing.assert_allclose(scene.attributes[0, :, 3], (0.2, 0.3, 0.4))


def test_bvh_splits_coincident_triangles_by_rank():
    """Centres all in one place cannot be binned; the build must still end in small leaves."""
    corner = np.tile(np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], np.float32), (40, 1))
    mesh = Mesh(corner, np.tile([0, 0, 1], (120, 1)), np.arange(120).reshape(-1, 3))
    runs = _leaves(build_scene([(mesh, 0, (0.7, 0.5, 0.4))]))
    assert sorted(index for run in runs for index in run) == list(range(40))
    assert max(len(run) for run in runs) <= 16


def test_packing_and_empty_scene():
    scene = build_scene([])
    assert scene.nodes.size == scene.triangles.size == 0
    # Always a power of two wide, so the shader finds a texel with a shift.
    assert table_width(8) == 8 and table_width(3000) == 2048 and table_width(4096) == 2048
    assert texture_table(scene.nodes, 8).shape == (1, 8, 4)
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
    panel._skin_controls["veins"].valueChanged.emit(0.6)
    assert state.render.skin.pore_size == 0.002 and state.render.skin.blood == 0.9
    assert state.render.skin.veins == 0.6
    # Tone comes from the preset; the model-dependent relief scale is kept.
    panel._apply_skin_preset(panel._skin_preset.findText("Fair / rosy"))
    assert state.render.skin.blood == SKIN_PRESETS["Fair / rosy"].blood
    assert state.render.skin.pore_size == 0.002
    assert state.render.skin.sss == SKIN_PRESETS["Fair / rosy"].sss
    assert state.render.skin.veins == 0.6
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
    panel._region_controls["veins"].valueChanged.emit(2.5)
    assert skin.regions.hands.acne == 2.0 and skin.regions.head.acne == 1.0
    assert skin.regions.hands.veins == 2.5
    assert skin.regions.head.veins == BodyRegionSettings().head.veins
    panel._region_edited.setCurrentIndex(panel._region_edited.findData("head"))
    assert panel._region_controls["acne"].value() == pytest.approx(1.0)
    assert panel._region_controls["veins"].value() == pytest.approx(0.75)
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


def test_refinement_restarts_only_for_what_the_traced_image_shows():
    from refview.core.settings import RenderSettings
    from refview.render.mesh_renderer import traced_settings_key

    settings = RenderSettings(shading_mode=ShadingMode.HUMAN_SKIN)
    before = traced_settings_key(settings)
    # Controls of other modes, and of things that are off, leave it alone.
    settings.matcap.contrast = 2.0
    settings.matcap_path = "elsewhere.png"
    settings.contour.density = 90.0
    settings.surface.roughness = 0.9
    settings.quality.shadow_strength = 0.1
    settings.planes.detail = 12.0
    settings.wireframe_color = (1.0, 0.0, 0.0)
    assert traced_settings_key(settings) == before
    # What the picture shows restarts it.
    for change in (
        lambda s: setattr(s.skin, "roughness", 0.7),
        lambda s: setattr(s.light, "azimuth_deg", 10.0),
        lambda s: setattr(s, "background_top", (1.0, 1.0, 1.0)),
        lambda s: setattr(s.planes, "enabled", True),
        lambda s: setattr(s, "show_wireframe", True),
        lambda s: setattr(s.section, "enabled", True),
    ):
        changed = replace(settings, skin=replace(settings.skin), light=replace(settings.light),
                          planes=replace(settings.planes), section=replace(settings.section))
        change(changed)
        assert traced_settings_key(changed) != before
