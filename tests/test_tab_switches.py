"""The switch on each tab: it reads what the panel draws and writes it back.

Every panel that puts something on the model answers :meth:`Panel.shown`
with a bool, and the main window hangs a checkbox on its tab that reads it
and drives :meth:`Panel.set_shown`.  What is worth asserting is that each
answer is the same setting the panel's own Display switch writes, so the two
can never disagree, and that a panel which draws nothing answers ``None``
and so gets no switch.
"""

from __future__ import annotations

import pytest

QtCore = pytest.importorskip("PySide6.QtCore")
QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from refview.ui.panels.annotate_panel import AnnotatePanel  # noqa: E402 - needs Qt first
from refview.ui.panels.armature_panel import ArmaturePanel  # noqa: E402 - needs Qt first
from refview.ui.panels.camera_panel import CameraPanel  # noqa: E402 - needs Qt first
from refview.ui.panels.forms_panel import FormsPanel  # noqa: E402 - needs Qt first
from refview.ui.panels.measure_panel import MeasurePanel  # noqa: E402 - needs Qt first
from refview.ui.panels.planes_panel import PlanesPanel  # noqa: E402 - needs Qt first
from refview.ui.panels.section_panel import SectionPanel  # noqa: E402 - needs Qt first
from refview.ui.panels.shading_panel import ShadingPanel  # noqa: E402 - needs Qt first
from refview.ui.state import ViewerState  # noqa: E402 - needs Qt first


@pytest.fixture(scope="session")
def app():
    """One offscreen Qt application for the run; see test_film_recorder."""
    import os

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    existing = QtWidgets.QApplication.instance()
    yield existing or QtWidgets.QApplication([])


@pytest.mark.parametrize(
    ("make", "read"),
    [
        (PlanesPanel, lambda state: state.render.planes.enabled),
        (SectionPanel, lambda state: state.render.section.enabled),
        (MeasurePanel, lambda state: state.measurement_settings.show_all),
        (AnnotatePanel, lambda state: state.annotation_settings.visible),
        (ArmaturePanel, lambda state: state.armature_settings.show_all),
        (FormsPanel, lambda state: state.form_settings.show_all),
    ],
)
def test_the_switch_is_the_panels_own_visibility_setting(app, make, read):
    state = ViewerState()
    panel = make(state)
    assert panel.shown() is read(state)
    for on in (True, False, True):
        panel.set_shown(on)
        assert read(state) is on
        assert panel.shown() is on
    # And the setting changing underneath is what the switch reads back.
    panel.set_shown(False)
    assert panel.shown() is False


@pytest.mark.parametrize("make", [CameraPanel, ShadingPanel])
def test_a_panel_that_draws_nothing_has_no_switch(app, make):
    assert make(ViewerState()).shown() is None


def test_the_camera_panel_takes_the_clip_planes_in_hand_where_the_fit_left_them(app):
    state = ViewerState()
    panel = CameraPanel(state)
    camera = state.camera
    panel.refresh_camera()
    # Fitted: the bars show the fit and cannot be dragged.
    assert not panel._clip_by_hand.isChecked() and not panel._near.isEnabled()
    fitted = camera.fitted_clip_planes()
    assert panel._near.value() == pytest.approx(fitted[0], abs=1e-3)
    assert panel._far.value() == pytest.approx(fitted[1], abs=1e-3)
    # Taken in hand, they start where the fit left them and then hold still.
    heard = []
    state.camera_changed.connect(lambda: heard.append(1))
    panel._clip_by_hand.setChecked(True)
    assert (camera.near, camera.far) == fitted and heard
    assert panel._near.isEnabled() and panel._far.isEnabled()
    panel._far._write(fitted[1] * 3.0, commit=True)
    assert camera.far == pytest.approx(fitted[1] * 3.0)
    camera.eye = camera.eye * 2.0
    state.notify_camera()
    assert camera.far == pytest.approx(fitted[1] * 3.0)  # The fit moved; the hand did not.
    # Handed back, the fit takes over again.
    panel._clip_by_hand.setChecked(False)
    assert camera.near is None and camera.far is None
    assert not panel._near.isEnabled()
