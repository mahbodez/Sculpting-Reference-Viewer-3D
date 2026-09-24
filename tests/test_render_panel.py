"""The Render panel and the Render window, offscreen."""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.path_trace import (
    CUSTOM_PRESET,
    PATH_TRACE_PRESETS,
    OutputFormat,
    RenderMethod,
    ViewTransform,
)
from refview.core.settings import ShadingMode

QtCore = pytest.importorskip("PySide6.QtCore")
QtWidgets = pytest.importorskip("PySide6.QtWidgets")
QtGui = pytest.importorskip("PySide6.QtGui")

from refview.ui.panels.render_panel import RenderPanel  # noqa: E402 - needs Qt first
from refview.ui.state import ViewerState  # noqa: E402 - needs Qt first


@pytest.fixture(scope="session")
def app():
    import os

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    existing = QtWidgets.QApplication.instance()
    yield existing or QtWidgets.QApplication([])


@pytest.fixture
def panel(app):
    state = ViewerState()
    return RenderPanel(state)


def test_the_panel_shows_the_settings(panel):
    trace = panel.state.path_trace
    assert panel._preset.currentText() == "Final"
    assert panel._samples.value() == trace.sampling.samples
    assert panel._method.currentData() == RenderMethod.PROGRESSIVE.value
    assert "px" in panel._memory.text()


def test_a_preset_applies_and_an_edit_leaves_it(panel):
    state = panel.state
    heard = []
    state.path_trace_changed.connect(lambda: heard.append(1))
    index = panel._preset.findText("Draft")
    panel._preset.setCurrentIndex(index)
    panel._preset.activated.emit(index)
    assert state.path_trace.preset == "Draft"
    assert PATH_TRACE_PRESETS["Draft"].matches(state.path_trace)
    assert heard
    panel._samples.valueChanged.emit(300.0)
    assert state.path_trace.sampling.samples == 300
    assert state.path_trace.preset == CUSTOM_PRESET
    assert panel._preset.currentText() == CUSTOM_PRESET


def test_bucket_rows_show_only_for_the_bucket_method(panel):
    form = panel._method_form
    assert not form.isRowVisible(panel._bucket_size)
    panel._method.setCurrentIndex(panel._method.findData(RenderMethod.BUCKET.value))
    assert panel.state.path_trace.performance.method is RenderMethod.BUCKET
    assert form.isRowVisible(panel._bucket_size)


def test_the_clay_is_offered_only_where_a_mode_has_no_material(panel):
    state = panel.state
    state.render.shading_mode = ShadingMode.MATCAP
    state.notify_render()
    assert panel._materials_form.isRowVisible(panel._clay_color)
    assert "clay" in panel._mode_note.text()
    state.render.shading_mode = ShadingMode.HUMAN_SKIN
    state.notify_render()
    assert not panel._materials_form.isRowVisible(panel._clay_color)
    assert not panel._materials_form.isRowVisible(panel._light_size)


def test_width_and_height_keep_proportions(panel):
    output = panel.state.path_trace.output
    output.lock_aspect = True
    output.width, output.height = 1000, 500
    panel.refresh()
    panel._width.setValue(800)
    assert (output.width, output.height) == (800, 400)
    assert output.size_preset == "Custom"


def test_combos_write_their_enums(panel):
    trace = panel.state.path_trace
    panel._format.setCurrentIndex(panel._format.findData(OutputFormat.EXR_HALF.value))
    panel._transform.setCurrentIndex(panel._transform.findData(ViewTransform.FILMIC.value))
    assert trace.output.format is OutputFormat.EXR_HALF
    assert trace.color.view_transform is ViewTransform.FILMIC


def test_neural_rendering_controls_write_their_settings(panel):
    from refview.core.path_trace import NeuralStyle

    neural = panel.state.path_trace.neural
    assert not neural.final and not neural.preview
    panel._neural_final.setChecked(True)
    panel._neural_preview.setChecked(True)
    panel._neural_auto_mask.setChecked(True)
    panel._neural_style.setCurrentIndex(panel._neural_style.findData(NeuralStyle.NATURAL.value))
    panel._rows["neural.passes"][0]._write(3.0, True)
    panel._rows["neural.skin_structure"][0]._write(0.5, True)
    assert neural.final and neural.preview and neural.auto_mask
    assert neural.style is NeuralStyle.NATURAL
    assert neural.passes == 3 and isinstance(neural.passes, int)
    assert neural.skin_structure == pytest.approx(0.5)
    # None of it restarts the rendered viewport.
    from refview.trace.scene import trace_settings_key

    before = trace_settings_key(panel.state.render, panel.state.path_trace)
    neural.intensity = 1.7
    assert trace_settings_key(panel.state.render, panel.state.path_trace) == before


def test_the_panel_says_when_there_is_no_engine(panel, tmp_path, monkeypatch):
    monkeypatch.setenv("REFVIEW_RESOURCES", str(tmp_path))
    panel.probe_neural()
    panel._neural_probe.result(timeout=5)
    panel._refresh_neural()
    assert panel._neural_status.text().startswith("✗")
    assert "Preferences" in panel._neural_status.text()


def _grey_result(state):
    from refview.trace.film import Film
    from refview.ui.render_controller import RenderResult

    film = Film(96, 72)
    film.rgba[..., :3] = 0.18
    film.rgba[..., 3] = 1.0
    film.count[...] = 1
    return RenderResult(film=film, settings=state.path_trace, skin=False, skin_exposure=0.0,
                        background_top=(0, 0, 0), background_bottom=(0, 0, 0),
                        view_rotation=np.eye(3))


def test_the_render_window_shows_and_saves_the_neural_pass(app, tmp_path):
    pytest.importorskip("numba")
    from refview.ui.render_controller import RenderController, enhance_key
    from refview.ui.render_window import PASSES, RenderWindow

    state = ViewerState()
    controller = RenderController(state)
    window = RenderWindow(state, controller)
    result = _grey_result(state)
    window._on_started(result)
    window._on_finished(result)
    item = window._pass.model().item(PASSES.index("Neural"))
    assert not item.isEnabled()
    result.enhanced = np.full((72, 96, 4), 1.0, np.float32)
    result.enhanced[..., 0] = 0.5
    result.enhanced_key = enhance_key(state.path_trace)
    result.enhancer = "DLSS 5 Neural Rendering (Neuroframe Engine 11.0)"
    window._on_enhanced(result)
    assert window._pass.currentText() == "Neural"
    assert item.isEnabled()
    assert tuple(window._bytes[0, 0]) == (128, 255, 255, 255)
    # Made again, it leaves a pass chosen by hand alone.
    window._pass.setCurrentText("Beauty")
    window._on_enhanced(result)
    assert window._pass.currentText() == "Beauty"
    window._pass.setCurrentText("Neural")
    window.write(tmp_path / "n.png", OutputFormat.PNG8)
    assert (tmp_path / "n.png").stat().st_size > 0
    with pytest.raises(ValueError, match="PNG"):
        window.write(tmp_path / "n.exr", OutputFormat.EXR_FLOAT)
    # A colour change makes it again, once the slider has stopped.
    assert not controller._enhance_later.isActive()
    state.path_trace.color.exposure = 0.5
    state.notify_path_trace()
    assert controller._enhance_later.isActive()
    # A new render starts from the picture, not the old enhanced one.
    window._on_started(_grey_result(state))
    assert window._pass.currentText() == "Beauty"


def test_the_controller_enhances_after_denoising(app, tmp_path, monkeypatch):
    pytest.importorskip("numba")
    from refview.trace.neural import NeuralBridge, NeuralService, set_engine_dir
    from refview.ui import render_controller
    from refview.ui.render_controller import RenderController
    from test_trace_neural import FakeEngine, _install

    monkeypatch.setenv("REFVIEW_RESOURCES", str(tmp_path))
    set_engine_dir(_install(tmp_path / "engine"))
    engine = FakeEngine()
    service = NeuralService(lambda folder: NeuralBridge(folder, library=engine))
    monkeypatch.setattr(render_controller, "_NEURAL", service)
    try:
        state = ViewerState()
        state.path_trace.neural.final = True
        controller = RenderController(state)
        seen = []
        controller.enhanced.connect(seen.append)
        result = _grey_result(state)
        controller._result = result
        result.denoised = result.film.beauty().copy()
        controller.enhance(result)
        _owner, _key, future = controller._enhance_future
        future.result(timeout=5)
        controller._poll_enhance()
        assert seen == [result]
        assert result.enhanced.shape == (72, 96, 4)
        assert "Neuroframe Engine 11.0" in result.enhancer
        assert engine.sizes == [(96, 72)]
    finally:
        set_engine_dir(None)
        service.shutdown()


def test_the_render_window_develops_and_saves_a_film(app, tmp_path):
    pytest.importorskip("numba")
    from refview.trace.film import Film
    from refview.ui.render_controller import RenderController, RenderResult
    from refview.ui.render_window import RenderWindow

    state = ViewerState()
    controller = RenderController(state)
    window = RenderWindow(state, controller)
    film = Film(32, 16)
    film.rgba[..., :3] = 0.18
    film.rgba[..., 3] = 1.0
    film.count[...] = 1
    film.albedo[...] = 0.5
    film.normal[..., 2] = 1.0
    result = RenderResult(film=film, settings=state.path_trace, skin=False, skin_exposure=0.0,
                          background_top=(0, 0, 0), background_bottom=(0, 0, 0),
                          view_rotation=np.eye(3))
    window._on_started(result)
    window._on_finished(result)
    grey = window._bytes[0, 0, 0]
    assert 90 < grey < 130   # 0.18 through PBR Neutral, about 115
    # A brighter exposure develops brighter, with no render.
    state.path_trace.color.exposure = 1.0
    state.notify_path_trace()
    assert window._bytes[0, 0, 0] > grey
    for shown in ("Albedo", "Normal", "Depth", "Alpha", "Samples"):
        window._pass.setCurrentText(shown)
        assert window._bytes[..., 3].min() == 255
    window._pass.setCurrentText("Beauty")
    window.write(tmp_path / "r.png", OutputFormat.PNG8)
    window.write(tmp_path / "r16.png", OutputFormat.PNG16)
    window.write(tmp_path / "r.exr", OutputFormat.EXR_FLOAT)
    for name in ("r.png", "r16.png", "r.exr"):
        assert (tmp_path / name).stat().st_size > 0
    from PySide6.QtGui import QImage

    assert QImage(str(tmp_path / "r16.png")).depth() == 64
    view = window.view
    view.set_zoom(2.0)
    assert view.zoom == 2.0
    view.fit()
    assert view.zoom is None


def test_the_rendered_viewport_shows_the_enhanced_picture(app, tmp_path, monkeypatch):
    from refview.trace.neural import NeuralBridge, NeuralService, set_engine_dir
    from refview.ui import render_controller
    from refview.ui.render_preview import ViewportRenderPreview
    from test_trace_neural import FakeEngine, _install

    class View(QtCore.QObject):
        def __init__(self, state):
            super().__init__()
            self.state = state

    monkeypatch.setenv("REFVIEW_RESOURCES", str(tmp_path))
    set_engine_dir(_install(tmp_path / "engine"))
    engine = FakeEngine()
    service = NeuralService(lambda folder: NeuralBridge(folder, library=engine))
    monkeypatch.setattr(render_controller, "_NEURAL", service)
    try:
        state = ViewerState()
        preview = ViewportRenderPreview(View(state))
        job, display = object(), np.full((64, 80, 4), 0.25, np.float32)
        display[..., 3] = 1.0
        preview._offer(job, display)
        assert preview._best is None            # Off: nothing is kept to enhance.
        state.path_trace.neural.preview = True
        preview._offer(job, display)
        preview._maybe_enhance(job)
        preview._enhance[2].result(timeout=5)
        preview._collect_enhance(job)
        assert preview._picture() is preview._enhanced
        assert preview._enhanced.pixel(0, 0) == QtGui.QColor(191, 191, 191).rgba()
        # The same picture and settings are not sent again; new settings are.
        preview._maybe_enhance(job)
        assert preview._enhance is None
        state.path_trace.neural.intensity = 0.5
        preview._maybe_enhance(job)
        assert preview._enhance is not None
        preview._enhance[2].result(timeout=5)
        preview._collect_enhance(job)
        # Too small to enhance, as while the view turns: left as it is.
        preview._offer(job, np.zeros((32, 48, 4), np.float32))
        preview._maybe_enhance(job)
        assert preview._enhance is None
        state.path_trace.neural.preview = False
        assert preview._picture() is not preview._enhanced
        assert engine.sizes == [(80, 64), (80, 64)]
    finally:
        set_engine_dir(None)
        service.shutdown()
