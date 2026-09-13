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
