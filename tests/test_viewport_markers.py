"""Marker interaction, selection identity, and section dragging regressions."""

import os

import numpy as np
import pytest
from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QColor, QImage, QMouseEvent, QPainter
from PySide6.QtWidgets import QApplication

from refview.core.armature import Armature, ArmatureNode, PlacedLandmark
from refview.core.camera import Camera, Projection
from refview.core.forms import PrimaryForm
from refview.core.measurement import Measurement
from refview.core.mesh import Mesh, compute_vertex_normals
from refview.core.section import OFFSET_SPAN, SectionAxis, SectionSettings
from refview.ui.markers import DepthDrag, MarkerVisibility, VisualMarker
from refview.ui.panels.measure_panel import MeasurePanel
from refview.ui.picking import SurfacePicker
from refview.ui.section_gizmo import SectionGizmo
from refview.ui.state import ViewerState
from refview.ui.viewport import Viewport


@pytest.fixture(scope="session")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    return QApplication.instance() or QApplication([])


@pytest.mark.parametrize("projection", list(Projection))
def test_depth_drag_keeps_a_fixed_axis_and_has_no_accumulated_drift(projection):
    camera = Camera(eye=np.array([3.0, 2.0, 5.0]), projection=projection)
    picker = SurfacePicker(camera, None, 800, 600)
    anchor = np.array([0.1, 0.2, 0.3])
    drag = DepthDrag.begin(anchor, 300, picker)
    first = drag.target(250)
    assert np.dot(first - anchor, camera.forward) > 0
    assert np.linalg.norm(np.cross(first - anchor, camera.forward)) < 1e-12
    drag.target(400)
    np.testing.assert_allclose(drag.target(250), first)
    np.testing.assert_allclose(drag.target(300), anchor)


def event(kind, x, y, modifiers=Qt.KeyboardModifier.ControlModifier):
    return QMouseEvent(
        kind,
        QPointF(x, y),
        QPointF(x, y),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        modifiers,
    )


@pytest.mark.parametrize("kind", ["measurement", "node", "landmark", "form"])
@pytest.mark.parametrize("cancel", [False, True])
def test_depth_gesture_changes_only_depth_and_can_undo_or_cancel(app, kind, cancel):
    state = ViewerState()
    viewport = Viewport(state)
    viewport.resize(800, 600)
    if kind == "measurement":
        marker = Measurement((0.0, 0.0, 0.0), (1.0, 0.0, 0.0), locked=False)
        state.measurements.items.append(marker)

        def read():
            return np.array(marker.start)
    elif kind == "node":
        marker = ArmatureNode()
        state.armatures.items.append(Armature(nodes=[marker]))

        def read():
            return marker.point
    elif kind == "landmark":
        arm = Armature(landmarks=[PlacedLandmark("test", (0.0, 0.0, 0.0))])
        state.armatures.items.append(arm)

        def read():
            return arm.landmark_for("test").point
    else:
        form = PrimaryForm(landmarks=[PlacedLandmark("test", (0.0, 0.0, 0.0))])
        state.forms.items.append(form)

        def read():
            return form.landmark_for("test").point

    before = read().copy()
    viewport.mousePressEvent(event(QEvent.Type.MouseButtonPress, 400, 300))
    assert viewport._depth_drag is not None
    viewport.mouseMoveEvent(event(QEvent.Type.MouseMove, 470, 260))
    after = read().copy()
    assert after[2] < before[2]
    np.testing.assert_allclose(after[:2], before[:2])
    if cancel:
        viewport.cancel_tools()
        np.testing.assert_allclose(read(), before)
        assert not state.history.can_undo
    else:
        viewport.mouseReleaseEvent(event(QEvent.Type.MouseButtonRelease, 470, 260))
        state.undo()
        np.testing.assert_allclose(read(), before)
        state.redo()
        np.testing.assert_allclose(read(), after)
    viewport.close()


def test_selection_survives_rebuild_but_does_not_jump_after_deletion(app):
    state = ViewerState()
    first = Measurement((0, 0, 0), (1, 0, 0))
    second = Measurement((0, 1, 0), (1, 1, 0))
    state.measurements.items.extend([first, second])
    panel = MeasurePanel(state)
    selected = []
    panel.selection_changed.connect(selected.append)
    panel._tree.setCurrentItem(panel._tree.topLevelItem(1))
    assert selected[-1] is second
    panel._tree.clearSelection()
    assert selected[-1] is None
    panel._tree.setCurrentItem(panel._tree.topLevelItem(1))
    state.measurements.items.pop(0)
    panel.refresh_list()
    assert selected[-1] is second
    state.measurements.items.clear()
    panel.refresh_list()
    assert selected[-1] is None
    panel.close()


@pytest.mark.parametrize("axis", list(SectionAxis))
@pytest.mark.parametrize("projection", list(Projection))
def test_section_rail_moves_along_normal_including_end_on_views(axis, projection):
    picker = SurfacePicker(Camera(projection=projection), None, 800, 600)
    settings = SectionSettings(enabled=True, axis=axis)
    gizmo = SectionGizmo()
    at, _, direction = gizmo.geometry(picker, settings)
    assert gizmo.begin(*at, picker, settings)
    assert gizmo.move(*(at + direction * 25)) > settings.offset
    assert gizmo.move(*at) == settings.offset


@pytest.mark.parametrize("projection", list(Projection))
def test_marker_occlusion_distinguishes_surface_inside_and_front(projection):
    points = np.array([[-2, -2, 0], [2, -2, 0], [0, 2, 0]], dtype=np.float32)
    faces = np.array([[0, 1, 2]], dtype=np.uint32)
    mesh = Mesh(points, compute_vertex_normals(points, faces), faces)
    picker = SurfacePicker(Camera(projection=projection), mesh, 800, 600)
    visibility = MarkerVisibility()
    visibility.prepare(picker, SectionSettings())
    assert not visibility.buried((0, 0, 0))
    assert not visibility.buried((0, 0, 0.1))
    assert visibility.buried((0, 0, -0.1))


def test_section_rail_is_a_screen_space_cue_at_the_right_edge():
    """The rail stands still while the camera moves, and never leaves the frame."""
    settings = SectionSettings(enabled=True, axis=SectionAxis.Y)
    gizmo = SectionGizmo()
    handles = []
    for yaw, pitch in ((0.0, 0.0), (1.5, 0.0), (0.0, 1.3), (2.4, -0.8)):
        camera = Camera()
        camera.orbit(yaw, pitch)
        picker = SurfacePicker(camera, None, 800, 600)
        at, _, direction = gizmo.geometry(picker, settings)
        handles.append(tuple(at))
        assert 740 < at[0] < 800 and abs(at[1] - 300) < 1
        assert tuple(direction) == (0.0, -1.0)
    assert len(set(handles)) == 1
    picker = SurfacePicker(Camera(), None, 800, 600)
    at, _, direction = gizmo.geometry(picker, settings)
    # The far end of the rail is the far end of the slider, no further.
    assert gizmo.begin(*at, picker, settings)
    span = picker.camera.scene_radius * OFFSET_SPAN
    assert gizmo.move(*(at + direction * 10_000)) == pytest.approx(span)
    assert gizmo.move(*(at - direction * 10_000)) == pytest.approx(-span)
    gizmo.drag = None
    # Grabbing the rail away from its handle takes hold as well, and the
    # handle is drawn where the offset says it is.
    settings.offset = span * 0.5
    assert gizmo.hit(at[0], at[1] + 30, picker, settings)
    assert not gizmo.hit(at[0] - 60, at[1], picker, settings)
    moved, _, _ = gizmo.geometry(picker, settings)
    assert moved[1] < at[1]
    assert gizmo.geometry(picker, SectionSettings(enabled=False)) is None


def test_hovering_the_section_rail_offers_a_hand(app):
    state = ViewerState()
    state.render.section.enabled = True
    viewport = Viewport(state)
    viewport.resize(800, 600)
    at, _, _ = viewport._section_gizmo.geometry(viewport._picker(), state.render.section)
    viewport.mouseMoveEvent(event(QEvent.Type.MouseMove, *at))
    assert viewport._section_gizmo.hover
    assert viewport.cursor().shape() == Qt.CursorShape.OpenHandCursor
    viewport.mouseMoveEvent(event(QEvent.Type.MouseMove, 100, 100))
    assert not viewport._section_gizmo.hover
    assert viewport.cursor().shape() == Qt.CursorShape.ArrowCursor
    viewport.close()


def test_overlay_text_is_drawn_as_outlined_paths(app):
    """The cues that share the overlay's text path get its halo too."""
    from refview.ui.markers import draw_text

    image = QImage(200, 60, QImage.Format.Format_ARGB32)
    image.fill(QColor("white"))
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    draw_text(painter, 10, 40, "Depth +0.5", color=QColor("white"))
    painter.end()
    # White text on white is readable only because of the dark outline.
    dark = sum(
        1 for x in range(200) for y in range(60) if image.pixelColor(x, y).lightness() < 128
    )
    assert dark > 50


def test_section_rail_paints_its_label(app):
    image = QImage(400, 300, QImage.Format.Format_ARGB32)
    image.fill(QColor("gray"))
    painter = QPainter(image)
    picker = SurfacePicker(Camera(), None, 400, 300)
    settings = SectionSettings(enabled=True)
    gizmo = SectionGizmo()
    gizmo.hover = True
    gizmo.draw(painter, picker, settings)
    painter.end()
    at, _, _ = gizmo.geometry(picker, settings)
    assert image.pixelColor(int(at[0]), int(at[1])) != QColor("gray")
    # The label goes on the side with the room for it: the left.
    x, y = int(at[0]), int(at[1])
    assert any(image.pixelColor(left, y) != QColor("gray") for left in range(x - 60, x - 12))


@pytest.mark.parametrize("projection", list(Projection))
def test_depth_gesture_lays_a_grid_in_the_scene_at_the_points_depth(app, projection):
    """A grid facing the camera, through the point wherever it has got to."""
    camera = Camera(projection=projection)
    camera.orbit(0.6, 0.4)
    picker = SurfacePicker(camera, None, 400, 300)
    drag = DepthDrag.begin((0.1, 0.2, 0.3), 150, picker)
    drag.target(110)
    segments, centre, reach = drag.grid(camera)
    assert np.allclose(centre, drag.anchor + drag.direction * drag.delta)
    assert reach == pytest.approx(drag.scale * DepthDrag.GRID_STEP * DepthDrag.GRID_CELLS)
    assert segments.shape == (2 * (2 * DepthDrag.GRID_CELLS + 1), 2, 3)
    # Every end lies in the plane through the point that faces the camera.
    along = (segments.reshape(-1, 3) - centre) @ camera.forward
    assert np.abs(along).max() < 1e-9
    assert np.abs(np.linalg.norm(segments.reshape(-1, 3) - centre, axis=1)).max() <= reach * 1.5

    # The viewport hands it to the renderer while the drag is on, as scene
    # geometry rather than paint, and takes it away when the drag ends.
    state = ViewerState()
    viewport = Viewport(state)
    handed = []
    viewport._renderer.set_guide = lambda vertices, centre=None, reach=0.0: handed.append(
        (len(vertices), centre, reach)
    )
    viewport._depth_drag = drag
    viewport._sync_guide()
    assert handed[-1][0] > 0 and handed[-1][2] == pytest.approx(reach)
    viewport._depth_drag = None
    viewport._sync_guide()
    assert handed[-1] == (0, None, 0.0)
    viewport._sync_guide()
    assert len(handed) == 2
    viewport.close()


def test_shared_marker_styles_and_depth_guide_paint(app):
    image = QImage(400, 300, QImage.Format.Format_ARGB32)
    image.fill(QColor("gray"))
    painter = QPainter(image)
    for i, shape in enumerate(("circle", "square", "cross")):
        VisualMarker(QPointF(50 + i * 100, 60), QColor("orange"), shape=shape).draw(painter)
        VisualMarker(QPointF(50 + i * 100, 140), QColor("orange"), shape=shape, buried=True).draw(
            painter
        )
    camera = Camera()
    drag = DepthDrag.begin((0, 0, 0), 150, SurfacePicker(camera, None, 400, 300))
    drag.target(130)
    drag.draw(painter, camera, 400, 300)
    painter.end()
    assert image.pixelColor(50, 60) != QColor("gray")


def test_section_gesture_undo_and_escape_restore_offset(app):
    state = ViewerState()
    state.render.section.enabled = True
    viewport = Viewport(state)
    viewport.resize(800, 600)
    for cancel in (True, False):
        at, _, direction = viewport._section_gizmo.geometry(
            viewport._picker(), state.render.section
        )
        viewport.mousePressEvent(event(QEvent.Type.MouseButtonPress, *at))
        end = at + direction * 30
        viewport.mouseMoveEvent(event(QEvent.Type.MouseMove, *end))
        assert state.render.section.offset > 0
        if cancel:
            viewport.cancel_tools()
            assert not state.history.can_undo
        else:
            viewport.mouseReleaseEvent(event(QEvent.Type.MouseButtonRelease, *end))
            state.undo()
        assert state.render.section.offset == 0
    viewport.close()


def test_matcap_controls_follow_mode_and_saved_grading(app):
    from refview.core.settings import ShadingMode
    from refview.ui.panels.shading_panel import ShadingPanel

    state = ViewerState()
    panel = ShadingPanel(state)
    for mode in ShadingMode:
        state.render.shading_mode = mode
        panel.update_enabled()
        assert panel.matcap_panel.isHidden() == (mode is not ShadingMode.MATCAP)
    state.render.matcap.gamma = 1.7
    panel.refresh()
    assert panel.matcap_panel._preview.settings().gamma == 1.7
    panel.close()


def test_contour_controls_follow_the_mode_and_pin_the_view(app):
    from refview.core.settings import ContourDirection, ShadingMode
    from refview.ui.panels.shading_panel import ShadingPanel

    state = ViewerState()
    panel = ShadingPanel(state)
    for mode in ShadingMode:
        state.render.shading_mode = mode
        panel.update_enabled()
        assert panel._contour_box.isHidden() == (mode is not ShadingMode.CONTOUR)
    state.render.shading_mode = ShadingMode.CONTOUR
    state.camera.orbit(0.7, 0.3)
    panel.slice_along_view()
    contour = state.render.contour
    assert contour.direction is ContourDirection.CUSTOM
    assert np.allclose(contour.custom_direction, state.camera.forward)
    assert panel._contour_direction.currentData() == "custom"
    panel._contour_direction.setCurrentIndex(panel._contour_direction.findData("y"))
    assert contour.direction is ContourDirection.Y
    panel._contour_density.valueChanged.emit(48.0)
    assert contour.density == 48.0
    panel.close()


def test_fps_counter_sits_in_the_chosen_corner_and_clear_of_the_chrome(app):
    from refview.core.preferences import Preferences
    from refview.ui.overlay import ViewportOverlay

    prefs = Preferences()
    prefs.viewport.fps_corner = "top-left"
    assert Preferences.from_dict(prefs.to_dict()).viewport.fps_corner == "top-left"
    data = prefs.to_dict()
    data["viewport"]["fps_corner"] = "middle"
    assert Preferences.from_dict(data).viewport.fps_corner == "bottom-right"

    image = QImage(400, 300, QImage.Format.Format_ARGB32)
    painter = QPainter(image)
    overlay = ViewportOverlay()
    state = ViewerState()
    viewport = Viewport(state)
    overlay.draw(painter, state, viewport.measure_tool, viewport.annotate_tool, 400, 300)
    rects = {
        corner: overlay.draw_caption(painter, "60.0 FPS", 400, 300, corner)
        for corner in ("top-left", "top-right", "bottom-left", "bottom-right")
    }
    painter.end()
    assert rects["top-right"].right() == pytest.approx(400 - overlay.MARGIN)
    assert rects["top-right"].top() == pytest.approx(overlay.MARGIN)
    assert rects["bottom-right"].bottom() == pytest.approx(300 - overlay.MARGIN)
    # Under the readout, and to the right of the orientation gizmo.
    assert rects["top-left"].top() > overlay._hud_rect.bottom()
    assert rects["bottom-left"].left() > overlay.MARGIN + overlay.GIZMO_RADIUS * 2
    assert rects["bottom-left"].bottom() == pytest.approx(300 - overlay.MARGIN)
    viewport.set_fps_corner("top-right")
    assert viewport._fps_corner == "top-right"
    viewport.close()


def test_fps_is_a_persistent_preference_and_stops_requesting_frames_when_disabled(app, monkeypatch):
    from refview.core.preferences import Preferences

    prefs = Preferences()
    prefs.viewport.show_fps = True
    assert Preferences.from_dict(prefs.to_dict()).viewport.show_fps
    viewport = Viewport(ViewerState())
    frames = []
    monkeypatch.setattr(viewport, "update", lambda: frames.append(1))
    monkeypatch.setattr(viewport, "isVisible", lambda: True)
    viewport.set_show_fps(True)
    viewport._frame_presented()
    assert len(frames) == 2
    viewport.set_show_fps(False)
    frames.clear()
    viewport._frame_presented()
    assert not frames
    viewport.close()


def test_loading_matcap_keeps_sixteen_bit_channels(tmp_path):
    from PySide6.QtGui import QRgba64

    from refview.render.texture import load_matcap_pixels

    image = QImage(2, 2, QImage.Format.Format_RGBA64)
    image.fill(QColor.fromRgba64(QRgba64.fromRgba64(12345, 23456, 34567, 65535)))
    path = tmp_path / "precision.png"
    assert image.save(str(path))
    pixels = load_matcap_pixels(path)
    assert pixels.dtype == np.uint16
    np.testing.assert_array_equal(pixels[0, 0], [12345, 23456, 34567, 65535])
