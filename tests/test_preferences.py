"""What the artist prefers: kept apart from the document, and acted upon.

Two claims.  A preference is not a render setting -- it lives on the machine,
survives a restart, and no session file can reach it -- and every preference
in the window actually does something, which is the claim that rots first.  A
settings dialogue full of switches wired to nothing is the easiest thing in
an application to build and the hardest to notice, so each one here is
followed all the way to the thing that reads it.

The settings file is also treated as hostile: it is plain text on somebody's
disk, written by versions of this application that do not exist yet, and the
right answer to nonsense in it is the default for that one field and a working
window, never an exception on the way up.
"""

from __future__ import annotations

import os

import pytest

QtCore = pytest.importorskip("PySide6.QtCore")
QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from PySide6.QtCore import QSettings  # noqa: E402

from refview import paths  # noqa: E402
from refview.core.preferences import (  # noqa: E402
    MAX_FONT_SIZE,
    MAX_SPEED,
    Preferences,
)
from refview.ui import preferences as prefs_module  # noqa: E402
from refview.ui import theme  # noqa: E402
from refview.ui.elements import frame as frame_module  # noqa: E402
from refview.ui.elements import palette  # noqa: E402
from refview.ui.elements.frame import Frame  # noqa: E402
from refview.ui.navigation import NavigationController  # noqa: E402
from refview.ui.settings_window import GROUPS, SettingsWindow  # noqa: E402


@pytest.fixture(scope="session")
def app():
    """One offscreen Qt application for the run; see test_film_recorder."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    existing = QtWidgets.QApplication.instance()
    application = existing or QtWidgets.QApplication([])
    application.setOrganizationName("refview-tests")
    application.setApplicationName("refview-tests")
    yield application


@pytest.fixture
def store(app):
    """A store of its own, and the application put back the way it was found.

    Everything a preference touches is process-wide -- the palette, the style
    sheet, the folder the matcaps come from -- so a test that changed one and
    walked away would be changing the next test's application.
    """
    QSettings().remove(prefs_module.KEY)
    prefs_module.forget()
    made = prefs_module.store()
    yield made
    made.set(Preferences())
    prefs_module.forget()
    QSettings().remove(prefs_module.KEY)


# -- reading a settings file nobody has been careful with ----------------


def test_preferences_come_back_the_way_they_went_in():
    written = Preferences()
    written.interface.font_size = 14
    written.navigation.orbit_speed = 2.0
    written.folders.matcaps = "/somewhere/of/my/own"
    read = Preferences.from_dict(written.to_dict())
    assert read == written


def test_one_nonsense_field_does_not_cost_the_others():
    """The font size is a string; everything beside it still arrives."""
    data = Preferences().to_dict()
    data["interface"]["font_size"] = "enormous"
    data["interface"]["restore_layout"] = False
    read = Preferences.from_dict(data)
    assert read.interface.font_size == Preferences().interface.font_size
    assert read.interface.restore_layout is False


def test_a_setting_out_of_range_is_brought_back_into_it():
    data = Preferences().to_dict()
    data["interface"]["font_size"] = 400
    data["navigation"]["orbit_speed"] = 99.0
    data["viewport"]["samples"] = 3
    read = Preferences.from_dict(data)
    assert read.interface.font_size == MAX_FONT_SIZE
    assert read.navigation.orbit_speed == MAX_SPEED
    assert read.viewport.samples == Preferences().viewport.samples


def test_a_settings_file_that_is_not_settings_at_all_still_starts(store):
    QSettings().setValue(prefs_module.KEY, "{ this is not json")
    assert store.load() == Preferences()


def test_a_field_from_a_later_version_is_ignored(store):
    data = Preferences().to_dict()
    data["interface"]["hovercraft"] = True
    data["eels"] = {"count": 3}
    assert Preferences.from_dict(data) == Preferences()


# -- the settings file ---------------------------------------------------


def test_a_preference_survives_the_application_closing(store):
    prefs = Preferences()
    prefs.interface.font_size = 16
    store.set(prefs)

    prefs_module.forget()
    assert prefs_module.store().value.interface.font_size == 16


def test_restoring_defaults_puts_everything_back(store):
    prefs = Preferences()
    prefs.interface.font_size = 16
    prefs.navigation.invert_orbit_y = True
    store.set(prefs)
    store.reset()
    assert store.value == Preferences()


# -- every switch reaches something --------------------------------------


def test_the_accent_reaches_the_colours_the_panels_paint_with(store):
    prefs = Preferences()
    prefs.interface.accent = (0.2, 0.4, 0.8)
    store.set(prefs)
    assert palette.ACCENT.blue() > palette.ACCENT.red()
    # Words sitting on the accent have to be legible against it, which for a
    # dark accent means light words rather than the near-black the amber uses.
    assert palette.ON_INK.lightness() > 128


def test_the_type_size_reaches_the_style_sheet(store):
    prefs = Preferences()
    prefs.interface.font_size = 17
    store.set(prefs)
    assert theme.FONT_SIZE == 17
    assert "17px" in theme._stylesheet()


def test_folding_dead_groups_can_be_switched_off(store):
    prefs = Preferences()
    prefs.interface.fold_disabled = False
    store.set(prefs)

    box = Frame("Light", expanded=True)
    box.setEnabled(False)
    assert box.is_expanded(), "the group folded although the artist asked it not to"
    assert frame_module.FOLD_DISABLED is False


def test_the_matcap_folder_can_be_moved_and_moved_back(store, tmp_path):
    mine = tmp_path / "matcaps"
    mine.mkdir()
    prefs = Preferences()
    prefs.folders.matcaps = str(mine)
    store.set(prefs)
    assert paths.matcap_dir() == mine

    store.reset()
    assert paths.matcap_dir() != mine


def test_a_matcap_folder_that_has_gone_falls_back_to_the_bundled_ones(store, tmp_path):
    """An external drive that is not plugged in is not an empty gallery."""
    prefs = Preferences()
    prefs.folders.matcaps = str(tmp_path / "never-existed")
    store.set(prefs)
    assert paths.matcap_dir().name == "matcaps"
    assert paths.matcap_dir() != tmp_path / "never-existed"


def test_orbit_speed_is_a_multiple_of_the_shipped_rate():
    navigation = NavigationController()
    shipped = navigation._orbit_x
    navigation.orbit_speed = 2.0
    assert navigation._orbit_x == pytest.approx(shipped * 2.0)


def test_inverting_the_orbit_turns_a_drag_the_other_way():
    navigation = NavigationController()
    forwards = navigation._orbit_x
    navigation.invert_orbit_x = True
    assert navigation._orbit_x == pytest.approx(-forwards)


def test_zoom_speed_scales_the_step_and_not_the_factor():
    """Zoom is geometric, so twice the speed is twice the exponent."""
    navigation = NavigationController()
    at_rest = navigation._zoom_per_notch
    navigation.zoom_speed = 2.0
    assert navigation._zoom_per_notch - 1.0 == pytest.approx((at_rest - 1.0) * 2.0)
    navigation.zoom_speed = 0.0
    assert navigation._zoom_per_notch == pytest.approx(1.0), "no zoom at all, not backwards"


# -- the window ----------------------------------------------------------


@pytest.fixture
def window(store):
    made = SettingsWindow(store)
    yield made
    made.close()


def test_the_window_writes_what_it_is_set_to(window, store):
    window._font_size.set_value(13.0)
    window._font_size.valueCommitted.emit(13.0)
    assert store.value.interface.font_size == 13
    assert theme.FONT_SIZE == 13


def test_the_window_follows_a_change_it_did_not_make(window, store):
    """Restore Defaults, or a copy of one of these controls in another panel."""
    prefs = Preferences()
    prefs.navigation.orbit_speed = 2.5
    store.set(prefs)
    assert window._orbit_speed.value() == pytest.approx(2.5)


def test_a_group_opened_from_the_menu_is_the_only_one_open(window):
    window.show_group("navigation")
    assert window._groups["navigation"].is_expanded()
    assert not window._groups["interface"].is_expanded()


def test_every_group_has_somewhere_to_be_shown(window):
    assert set(window._groups) == set(GROUPS)


def test_the_multisample_choices_are_all_reachable(window, store):
    for index in range(window._samples.count()):
        window._samples.setCurrentIndex(index)
        assert store.value.viewport.samples == window._samples.itemData(index)


def test_every_anti_aliasing_mode_is_reachable_and_nonsense_falls_back(window, store):
    from refview.core.preferences import ANTIALIASING_MODES
    from refview.render.mesh_renderer import ANTIALIASING_MODES as RENDERER_MODES

    assert ANTIALIASING_MODES == RENDERER_MODES
    for index in range(window._antialiasing.count()):
        window._antialiasing.setCurrentIndex(index)
        assert store.value.viewport.antialiasing == window._antialiasing.itemData(index)
    offered = {window._antialiasing.itemData(i) for i in range(window._antialiasing.count())}
    assert offered == set(ANTIALIASING_MODES)
    data = Preferences().to_dict()
    data["viewport"]["antialiasing"] = "msaa64"
    assert Preferences.from_dict(data).viewport.antialiasing == "off"
    prefs = Preferences()
    prefs.viewport.antialiasing = "ssaa"
    store.set(prefs)
    assert window._antialiasing.currentData() == "ssaa"


def test_the_fps_corner_is_offered_only_with_the_counter_and_reaches_the_store(window, store):
    window._show_fps.setChecked(False)
    assert not window._fps_corner.isEnabled()
    window._show_fps.setChecked(True)
    assert window._fps_corner.isEnabled()
    for index in range(window._fps_corner.count()):
        window._fps_corner.setCurrentIndex(index)
        assert store.value.viewport.fps_corner == window._fps_corner.itemData(index)
    prefs = Preferences()
    prefs.viewport.fps_corner = "top-left"
    store.set(prefs)
    assert window._fps_corner.currentData() == "top-left"


# -- carrying on from last time ------------------------------------------
#
# The preference that is easiest to get wrong, because the thing it restores
# is usually not there in the first place: most of what an artist looks at
# never becomes a session file, and a switch that only worked for the ones
# that did would look broken to everybody else.


@pytest.fixture
def model(tmp_path):
    """One triangle, which is a mesh as far as any of this is concerned."""
    path = tmp_path / "one.stl"
    path.write_text(
        "solid p\nfacet normal 0 0 1\n outer loop\n"
        "  vertex 0 0 0\n  vertex 1 0 0\n  vertex 0 1 0\n"
        " endloop\nendfacet\nendsolid p\n",
        encoding="utf-8",
    )
    return path


@pytest.fixture
def windows(store):
    """Windows that clean up after themselves, and a settings file that does."""
    from refview.ui.main_window import MainWindow

    prefs = Preferences()
    prefs.startup.reopen_last_session = True
    store.set(prefs)

    made = []

    def build():
        window = MainWindow()
        made.append(window)
        return window

    yield build
    for window in made:
        window._layout_write.stop()
        window.close()
    for key in ("session/last", "session/last_model"):
        QSettings().remove(key)


def test_the_model_last_opened_comes_back(windows, model):
    """A session is not the only thing worth carrying on from."""
    windows().open_model(model)

    next_time = windows()
    assert next_time.reopen_last_session()
    assert next_time.state.mesh is not None


def test_a_saved_session_beats_the_model_it_was_saved_from(windows, model, tmp_path):
    first = windows()
    first.open_model(model)
    session = tmp_path / "work.refview"
    first._state.save_session(session, layout=first._workspace.to_dict())
    first._remember_session(session)

    next_time = windows()
    assert next_time.reopen_last_session()
    assert next_time._session_path == session


def test_opening_another_model_forgets_the_session_belonging_to_the_last(
    windows, model, tmp_path
):
    """Otherwise the marks from one piece of work arrive on top of another."""
    first = windows()
    first.open_model(model)
    session = tmp_path / "work.refview"
    first._state.save_session(session, layout=first._workspace.to_dict())
    first._remember_session(session)
    first.open_model(model)

    assert not QSettings().value("session/last", "")


def test_nothing_comes_back_when_it_was_not_asked_for(windows, model, store):
    windows().open_model(model)
    store.reset()  # reopen_last_session is off as it ships
    assert not windows().reopen_last_session()


def test_a_remembered_file_that_has_gone_is_passed_over(windows, model, tmp_path):
    windows().open_model(model)
    model.unlink()
    # No dialog, no exception, no mesh: an external drive that is not plugged
    # in is not an error worth stopping the application for.
    assert not windows().reopen_last_session()
