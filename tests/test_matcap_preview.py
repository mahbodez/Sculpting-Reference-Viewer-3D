"""The matcap as its own control, and whether it tells the truth.

The disc is only worth having if it shows what the renderer will do, so the
first half of this is a second, independent transcription of the shader --
``reflect`` and all -- compared against the short form the widget uses.  If
somebody changes ``sampleMatcap`` or ``gradeMatcap`` without changing the
widget, these are what should notice.

The second half is the gestures, and the claim there is direct manipulation:
a drag that goes clockwise turns the matcap clockwise.  Not "changes the
rotation" -- which is true of turning it the wrong way as well -- but that the
picture stays under the hand, which is the only reason to have replaced the
slider with a disc.
"""

from __future__ import annotations

import math
import os

import numpy as np
import pytest

QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from PySide6.QtCore import QPoint, Qt  # noqa: E402
from PySide6.QtTest import QTest  # noqa: E402

from refview.core.settings import MatcapSettings  # noqa: E402
from refview.render.texture import default_matcap_pixels  # noqa: E402
from refview.ui.elements.clone import can_clone, clone  # noqa: E402
from refview.ui.matcap_preview import MatcapPreview, grade, sample  # noqa: E402
from refview.ui.panels.matcap_panel import MatcapPanel  # noqa: E402
from refview.ui.state import ViewerState  # noqa: E402


@pytest.fixture(scope="session")
def app():
    """One offscreen Qt application for the run; see test_film_recorder."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    existing = QtWidgets.QApplication.instance()
    yield existing or QtWidgets.QApplication([])


@pytest.fixture
def preview(app):
    """A disc the size the panel gives it, with settings of its own to write."""
    made = MatcapPreview()
    made.resize(240, 256)
    made.set_settings(MatcapSettings())
    made.show()
    app.processEvents()
    yield made
    made.close()


# -- the same arithmetic the shader does ---------------------------------


def _shader_uv(normal, rotation_deg: float, flip_y: bool):
    """``sampleMatcap``, transcribed from the GLSL, for a camera down +z.

    Deliberately the long way round -- the reflection vector, the magnitude,
    the halving -- because the widget takes the short way, and two roads to
    the same number is the whole point of writing this out again.
    """
    n = np.asarray(normal, dtype=float)
    view = np.array([0.0, 0.0, 1.0])
    incident = -view
    reflected = incident - 2.0 * np.dot(n, incident) * n
    cos, sin = math.cos(math.radians(rotation_deg)), math.sin(math.radians(rotation_deg))
    rotated = np.array(
        [
            reflected[0] * cos - reflected[1] * sin,
            reflected[0] * sin + reflected[1] * cos,
        ]
    )
    magnitude = 2.0 * math.sqrt(rotated @ rotated + (reflected[2] + 1.0) ** 2)
    uv = rotated / max(magnitude, 1e-4) + 0.5
    if flip_y:
        uv[1] = 1.0 - uv[1]
    return uv


def _widget_uv(nx: float, ny: float, rotation_deg: float, flip_y: bool):
    """The mapping :func:`sample` uses, for one normal rather than a grid."""
    cos, sin = math.cos(math.radians(rotation_deg)), math.sin(math.radians(rotation_deg))
    u = (nx * cos - ny * sin) * 0.5 + 0.5
    v = (nx * sin + ny * cos) * 0.5 + 0.5
    return np.array([u, 1.0 - v if flip_y else v])


@pytest.mark.parametrize("rotation", [0.0, 37.0, -120.0, 180.0])
@pytest.mark.parametrize("flip", [False, True])
def test_the_disc_samples_where_the_shader_would(rotation, flip):
    for nx, ny in ((0.0, 0.0), (0.5, 0.2), (-0.7, 0.3), (0.1, -0.9)):
        nz = math.sqrt(max(1.0 - nx * nx - ny * ny, 0.0))
        if nz <= 1e-6:
            continue
        wanted = _shader_uv((nx, ny, nz), rotation, flip)
        assert _widget_uv(nx, ny, rotation, flip) == pytest.approx(wanted, abs=1e-9)


def test_the_grading_is_the_shaders_grading():
    settings = MatcapSettings(
        gamma=1.6, contrast=1.3, saturation=0.4, brightness=1.1, tint=(1.0, 0.9, 0.8)
    )
    colour = np.array([[[0.3, 0.5, 0.7]]], dtype=np.float32)

    # gradeMatcap, in order: gamma, contrast about mid grey, saturation
    # towards the luminance, then brightness and tint.
    by_hand = np.power(np.maximum(colour[0, 0], 0.0), 1.0 / max(settings.gamma, 0.01))
    by_hand = (by_hand - 0.5) * settings.contrast + 0.5
    luma = float(np.dot(by_hand, [0.2126, 0.7152, 0.0722]))
    by_hand = luma + (by_hand - luma) * settings.saturation
    by_hand = np.maximum(by_hand * settings.brightness * np.array(settings.tint), 0.0)

    assert grade(colour, settings)[0, 0] == pytest.approx(by_hand, abs=1e-5)


def test_a_gamma_of_nothing_does_not_divide_by_nothing():
    """The shader floors it at 0.01; a preview that raised here would crash."""
    settings = MatcapSettings(gamma=0.0)
    out = grade(np.array([[[0.5, 0.5, 0.5]]], dtype=np.float32), settings)
    assert np.isfinite(out).all()


# -- what is drawn -------------------------------------------------------


def test_the_disc_is_a_disc():
    pixels = sample(default_matcap_pixels(), MatcapSettings(), 64)
    assert pixels[0, 0, 3] == 0, "the corner should be transparent"
    assert pixels[32, 32, 3] == 255, "the middle should be opaque"


def test_turning_it_turns_the_picture_clockwise():
    """Positive rotation moves a feature clockwise, which is the way a drag goes.

    Followed by where the brightest part of the built-in matcap ends up: it
    starts low and to one side, and a quarter turn should put it a quarter of
    the way round in the direction a clock's hands go -- remembering that a
    widget counts rows downwards.
    """
    source = default_matcap_pixels()

    def brightest(rotation: float) -> tuple[int, int]:
        pixels = sample(source, MatcapSettings(rotation_deg=rotation), 64)
        lit = pixels[..., :3].astype(float).mean(axis=2) * (pixels[..., 3] > 0)
        row, column = np.unravel_index(int(np.argmax(lit)), lit.shape)
        return int(column - 32), int(32 - row)  # x right, y up, from the centre

    x0, y0 = brightest(0.0)
    x1, y1 = brightest(90.0)
    before = math.atan2(y0, x0)
    after = math.atan2(y1, x1)
    turned = math.degrees((after - before + math.pi) % (2.0 * math.pi) - math.pi)
    # Anticlockwise is positive in atan2 and clockwise is what we want, so a
    # quarter turn clockwise reads as roughly minus ninety.
    assert turned == pytest.approx(-90.0, abs=12.0)


# -- the gestures --------------------------------------------------------


def _drag(preview, start, end, modifier=Qt.KeyboardModifier.NoModifier):
    QTest.mousePress(preview, Qt.MouseButton.LeftButton, modifier, start)
    QTest.mouseMove(preview, end)
    QtWidgets.QApplication.processEvents()
    QTest.mouseRelease(preview, Qt.MouseButton.LeftButton, modifier, end)
    QtWidgets.QApplication.processEvents()


def test_a_clockwise_drag_turns_it_clockwise(preview):
    """The picture follows the hand, which is the whole reason for the disc."""
    _drag(preview, QPoint(120, 30), QPoint(210, 120))
    assert preview.settings().rotation_deg == pytest.approx(90.0, abs=1.0)


def test_an_anticlockwise_drag_turns_it_back(preview):
    _drag(preview, QPoint(210, 120), QPoint(120, 30))
    assert preview.settings().rotation_deg == pytest.approx(-90.0, abs=1.0)


def test_shift_drags_the_light(preview):
    _drag(preview, QPoint(120, 120), QPoint(220, 40), Qt.KeyboardModifier.ShiftModifier)
    assert preview.settings().brightness > 1.0
    assert preview.settings().contrast > 1.0


def test_ctrl_drags_the_colour(preview):
    _drag(preview, QPoint(120, 120), QPoint(20, 200), Qt.KeyboardModifier.ControlModifier)
    assert preview.settings().saturation < 1.0
    assert preview.settings().gamma < 1.0


def test_a_drag_off_the_end_stops_at_the_end(preview):
    """Dragging further than the range goes is not a negative gamma."""
    for _ in range(6):
        _drag(preview, QPoint(230, 10), QPoint(10, 250), Qt.KeyboardModifier.ControlModifier)
    assert preview.settings().gamma >= 0.1
    assert preview.settings().saturation >= 0.0


def test_the_wheel_turns_it_in_steps(preview):
    from PySide6.QtCore import QPointF
    from PySide6.QtGui import QWheelEvent

    event = QWheelEvent(
        QPointF(120, 120),
        QPointF(120, 120),
        QPoint(0, 0),
        QPoint(0, 120),
        Qt.MouseButton.NoButton,
        Qt.KeyboardModifier.NoModifier,
        Qt.ScrollPhase.NoScrollPhase,
        False,
    )
    preview.wheelEvent(event)
    assert preview.settings().rotation_deg == pytest.approx(5.0)


def test_alt_is_left_alone_so_the_disc_can_be_copied(preview):
    """Alt and a drag copies a control; the disc must not swallow that."""
    _drag(preview, QPoint(120, 30), QPoint(210, 120), Qt.KeyboardModifier.AltModifier)
    assert preview.settings().rotation_deg == pytest.approx(0.0)


def test_a_double_click_puts_the_grading_back_but_not_the_matcap(preview):
    """Tint and flip are not dragged on the disc, so they are not reset by it."""
    settings = preview.settings()
    settings.rotation_deg = 40.0
    settings.gamma = 2.0
    settings.tint = (1.0, 0.5, 0.5)
    settings.flip_y = True

    QTest.mouseDClick(preview, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
    QtWidgets.QApplication.processEvents()

    assert settings.rotation_deg == pytest.approx(0.0)
    assert settings.gamma == pytest.approx(1.0)
    assert settings.tint == (1.0, 0.5, 0.5)
    assert settings.flip_y is True


def test_turning_it_says_what_it_is_doing(preview):
    """A gesture nobody can see the result of is a gesture nobody trusts."""
    QTest.mousePress(preview, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier,
                     QPoint(120, 30))
    QTest.mouseMove(preview, QPoint(180, 50))
    QtWidgets.QApplication.processEvents()
    assert "Rotation" in preview._saying
    QTest.mouseRelease(preview, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier,
                       QPoint(180, 50))


# -- copies, and the panel around it -------------------------------------


def test_a_copy_of_the_disc_drives_the_original(preview):
    assert can_clone(preview)
    copy = clone(preview)
    heard = []
    preview.changed.connect(lambda: heard.append(True))

    copy.resize(240, 256)
    _drag(copy, QPoint(120, 30), QPoint(210, 120))

    assert preview.settings().rotation_deg == pytest.approx(90.0, abs=1.0)
    assert heard, "the original was never told, so nothing would have redrawn"


def test_the_numbers_follow_a_drag_on_the_disc(app):
    """The sliders are still there for typing into, so they have to keep up."""
    panel = MatcapPanel(ViewerState())
    panel._preview.resize(240, 256)
    panel._preview.show()
    app.processEvents()

    _drag(panel._preview, QPoint(120, 30), QPoint(210, 120))
    assert panel._rotation.value() == pytest.approx(
        panel.state.render.matcap.rotation_deg, abs=0.5
    )
    assert panel._rotation.value() != pytest.approx(0.0)


def test_the_disc_is_not_inside_anything_that_folds(app):
    """It is the panel's main control; a click on a bar must not take it away."""
    from refview.ui.elements.frame import Frame

    panel = MatcapPanel(ViewerState())
    parent = panel._preview.parentWidget()
    while parent is not None and parent is not panel:
        assert not isinstance(parent, Frame), "the disc can be folded away"
        parent = parent.parentWidget()


def test_the_disc_draws_the_matcap_that_is_on_the_model(app):
    panel = MatcapPanel(ViewerState())
    assert panel._preview.settings() is panel.state.render.matcap
    panel.state.load_matcap(None)
    assert panel._preview.source_pixels() is panel.state.matcap_pixels


# -- saving it back out --------------------------------------------------


def test_the_original_saves_the_way_it_was_read(app, tmp_path):
    """A matcap written out and read back in is the same matcap."""
    from PySide6.QtGui import QImage

    from refview.render.texture import load_matcap_pixels

    preview = MatcapPreview()
    source = default_matcap_pixels(64)
    preview.set_source(source)
    path = preview.save_image(tmp_path / "back.png", graded=False)
    image = QImage(str(path))
    assert (image.width(), image.height()) == (64, 64)
    again = load_matcap_pixels(path)
    assert again.shape[:2] == source.shape[:2]
    scale = np.iinfo(source.dtype).max if np.issubdtype(source.dtype, np.integer) else 1.0
    original = source[..., :3].astype(np.float32) / scale
    read = again[..., :3].astype(np.float32) / np.iinfo(again.dtype).max
    assert np.abs(original - read).max() < 2.5 / 255.0


def test_the_graded_save_carries_the_grading(app, tmp_path):
    from PySide6.QtGui import QImage

    preview = MatcapPreview()
    preview.set_source(default_matcap_pixels(64))
    plain = preview.image(graded=True)
    preview.settings().brightness = 0.3
    preview.refresh()
    dim = preview.image(graded=True)
    assert plain.pixelColor(32, 32).lightness() > dim.pixelColor(32, 32).lightness()
    # Square, and opaque to the corners, so it loads back as a matcap.
    assert dim.pixelColor(0, 0).alpha() == 255
    path = preview.save_image(tmp_path / "graded.png")
    assert QImage(str(path)).width() == 64


def test_a_right_click_offers_to_save(app, monkeypatch):
    """The menu is the way in; what it runs is the save that was just tested."""
    preview = MatcapPreview()
    asked = []
    monkeypatch.setattr(preview, "_ask_to_save", lambda graded: asked.append(graded))
    menu = preview.save_menu()
    assert [action.text() for action in menu.actions()] == [
        "Save Graded Matcap as Image...",
        "Save Original Matcap as Image...",
    ]
    menu.actions()[1].trigger()
    menu.actions()[0].trigger()
    assert asked == [False, True]
