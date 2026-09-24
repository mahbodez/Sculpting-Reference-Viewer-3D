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
