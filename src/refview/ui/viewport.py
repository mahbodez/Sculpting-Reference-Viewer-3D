"""The interactive 3D view.

Navigation is: left-drag orbits about the point under the cursor, right- or
middle-drag pans, and the wheel zooms towards whatever the cursor is over.

The left button does sextuple duty, resolved in this order: a drag with the
annotate tool armed paints; a drag on a form's landmark moves it, and
the clay derived from it follows; a drag on an armature landmark's cross moves
it, and the wire derived from it follows; a drag on an unlocked armature node
moves it, or resizes it with Shift held; a drag on the endpoint handle of an
unlocked measurement moves that point; anything else orbits.  A cross is
offered before the node beside it, and within a tighter reach, which is what
settles the two where a preset has put them on top of each other.  With the
measuring, armature or forms tool armed a left *click* -- as opposed to a drag
-- places a point, so those gestures too share the button without fighting the
camera.  A drag on a skeleton's joint swings the bone above it, or moves the
figure when the joint is a root, and with Shift rolls the joint about its own
bone; with the pose tool armed a click adds a joint.  Holding Alt always
orbits, which is the escape hatch while painting, and holding Shift snaps an
orbit to round angles.  With the transform tool armed the active object's
gizmo takes the button before anything else: a drag on one of its handles
moves, turns or scales the object, and a click on another object makes that
one active.  An Alt-*click* -- Alt held, no travel -- makes the object under
the cursor active whatever tool is armed, as it does in ZBrush; and whichever
object becomes active, by any road, wears a line round its edge for a moment
so the eye can find it.
"""

from __future__ import annotations

import typing
from dataclasses import astuple, replace
from time import perf_counter

import numpy as np
from PySide6.QtCore import QEvent, Qt, QTimer, Signal
from PySide6.QtGui import QImage, QPainter, QSurfaceFormat
from PySide6.QtOpenGL import QOpenGLFramebufferObject, QOpenGLFramebufferObjectFormat
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QApplication

from ..core.annotation import Stroke
from ..core.armature import ArmatureNode, Buried
from ..core.commands import AddItem, ReplaceItems, SetAttributes
from ..core.convex import merged
from ..core.forms import (
    PrimaryForm,
    build_form,
    form_landmark_title,
    landmark_signature,
    shown_stages,
    stages_mesh,
)
from ..core.grid import build_grid
from ..core.history import ANNOTATIONS, ARMATURE, FORMS, MEASUREMENTS, SKELETON
from ..core.landmarks import landmark_title
from ..core.measurement import Measurement
from ..core.pedestal import build_pedestal
from ..core.plane_film import film_key
from ..core.plane_film import shaded as film_shaded
from ..core.plane_solids import SculptCache, wires_for
from ..core.section import section_segments
from ..core.settings import SculptMode, ShadingMode
from ..core.skeleton import Skeleton
from ..render.framebuffer import bind_default, current_framebuffer, sample_count
from ..render.mesh_renderer import SceneRenderer
from ..render.stroke_renderer import build_segment_vertices
from .annotate_tool import AnnotateTool
from .armature_tool import ArmatureTool
from .film_recorder import FilmRecorder
from .form_tool import FormTool
from .markers import DepthDrag
from .measure_tool import MeasureTool
from .navigation import DragMode, NavigationController
from .object_tool import ObjectTool
from .overlay import ViewportOverlay
from .picking import SurfacePicker
from .pose_tool import PoseTool
from .section_gizmo import SectionGizmo
from .state import ViewerState

if typing.TYPE_CHECKING:  # pragma: no cover - import cost, not behaviour
    from collections.abc import Iterable, Iterator

    from ..core.plane_film import Film, Stage
    from .film_export import ExportLook


def configure_surface_format(samples: int = 4) -> None:
    """Request a core-profile context; must run before the QApplication.

    ``samples`` is the multisample count, and it is an argument rather than a
    constant because it is the one render setting that cannot be changed once
    the application is running: the sample count belongs to the context, and
    the context is made before the window.  Hence a preference read on the way
    up, and a note in the Preferences window that it takes a restart.
    """
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    fmt.setDepthBufferSize(24)
    fmt.setStencilBufferSize(8)
    fmt.setSamples(max(int(samples), 0))
    QSurfaceFormat.setDefaultFormat(fmt)


#: The letters that choose the transform tool's gesture while it is armed --
#: the ones every modelling application puts them on.  Heard ahead of the
#: view's own keys, two of which they share, so that with the tool armed E
#: turns the object rather than picking up the eraser.
GESTURE_KEYS = {Qt.Key.Key_W: "move", Qt.Key.Key_E: "rotate", Qt.Key.Key_R: "scale"}

#: How long an object just made active wears its line, in seconds: held
#: solid, then faded to nothing.
HIGHLIGHT_HOLD = 0.7
HIGHLIGHT_FADE = 0.9
#: The line's colour: the amber the overlay marks a chosen landmark in.
HIGHLIGHT_COLOR = (1.0, 0.77, 0.36)


class Viewport(QOpenGLWidget):
    """Renders the scene and turns mouse gestures into camera and tool actions."""

    #: Pixels of travel below which a left-drag counts as a click.
    CLICK_TOLERANCE = 4.0

    measurement_created = Signal(object)
    #: A finished armature edit, as ``(index, nodes, bones, landmarks, text)``.
    #: The tool works out what the edit is; the window records it.
    armature_edited = Signal(object)
    #: A node was clicked, as ``(armature, node)``, or ``None`` for a miss.
    armature_selected = Signal(object)
    #: A landmark was clicked, as ``(armature, key)``, so the panel's list can
    #: follow the cross the artist just pointed at.
    landmark_selected = Signal(object)
    #: A finished edit to a form, as ``(index, landmarks, text)``.
    form_edited = Signal(object)
    #: A form's landmark was clicked, as ``(form, key)``.
    form_landmark_selected = Signal(object)
    #: A finished structural edit to a skeleton, as ``(index, joints, text)``.
    #: An index of ``-1`` means there was no skeleton to put the joint in.
    skeleton_edited = Signal(object)
    #: A joint was clicked, as ``(skeleton, joint)``.
    joint_selected = Signal(object)
    #: The transform tool's gesture was chosen by a key, so the panel's box
    #: can say so.
    object_mode_changed = Signal(str)
    pick_failed = Signal()

    def __init__(self, state: ViewerState, parent=None) -> None:
        super().__init__(parent)
        self._state = state
        self._renderer = SceneRenderer()
        self._skin_timer = QTimer(self)
        self._skin_timer.setSingleShot(True)
        self._skin_timer.timeout.connect(self.update)
        self._navigation = NavigationController()
        self._overlay = ViewportOverlay()
        self.measure_tool = MeasureTool()
        self.annotate_tool = AnnotateTool()
        self.armature_tool = ArmatureTool()
        self.form_tool = FormTool()
        self.pose_tool = PoseTool()
        self.object_tool = ObjectTool()
        self._ready = False
        self._depth_drag = None
        self._guide_shown = False
        self._section_gizmo = SectionGizmo()
        self._show_fps = False
        self._fps_corner = "bottom-right"
        self._antialiasing = "off"
        self._fps_start = perf_counter()
        self._fps_frames = 0
        self._fps = 0.0
        self.frameSwapped.connect(self._frame_presented)
        self._press_position: tuple[float, float] | None = None
        self._travel = 0.0
        self._grab_previous: tuple[Measurement, str, tuple] | None = None
        self._node_previous: tuple[ArmatureNode, str, object] | None = None
        #: A landmark drag in progress, as ``(armature index, key, what the
        #: armature held before it started)``.  A landmark is not edited in
        #: place -- moving one re-derives the whole wire -- so the undo step has
        #: to be able to put the lists back, not one attribute of one object.
        self._landmark_previous: tuple[int, str, dict] | None = None
        #: A form landmark drag in progress, as ``(form index, key, the
        #: landmark list before it started)``.
        self._form_previous: tuple[int, str, list] | None = None
        #: A pull on a joint in progress, as ``(skeleton index, the joint
        #: being written, the attribute, what it held, the x the pull began
        #: at)``.  The joint written is the parent of the one held when the
        #: pull is a swing, which is why it is named separately.
        self._pose_previous: tuple[int, int, str, object, float] | None = None
        #: Where the held joint stood when the pull began: the plane the
        #: cursor is read across, so the joint does not chase its own depth.
        self._pose_anchor: np.ndarray | None = None
        self._pose_dragged = False
        #: A transform gesture in progress: where the objects all stood when
        #: it began, so the whole gesture is one undo step and Esc can put it
        #: back, and the object being moved.
        self._object_previous: tuple | None = None
        self._object_held = None
        #: The object wearing a line round it, and when it was put on; the
        #: timer that keeps the frames coming while it fades; and which
        #: object was active the last time the list spoke, so that a change
        #: of active object can be told from any other change to the list.
        self._highlight: tuple[object, float] | None = None
        self._highlight_timer = QTimer(self)
        self._highlight_timer.setInterval(16)
        self._highlight_timer.timeout.connect(self.update)
        self._active_seen = state.active_object
        #: The solids of each form, kept by the landmarks that built them so
        #: that scrubbing a form's stages or recolouring the clay does not
        #: work the hull out again.
        self._form_solids: dict[int, tuple[tuple, list]] = {}
        #: What was selected before the current press, so that clicking a
        #: second node can join the two.
        self._join_from: tuple[int, int] | None = None
        self._erase_previous: list[Stroke] | None = None
        # Signatures of the generated scene geometry, so a light-slider tweak
        # does not re-cut the model or rebuild the pedestal.
        self._pedestal_key: tuple | None = None
        self._section_key: tuple | None = None
        self._sculpt_key: tuple | None = None
        self._grid_key: tuple | None = None
        #: Keeps the plane fit and the vertex-to-plane assignment between one
        #: turn of the geometry sliders and the next, so only the part that
        #: actually went stale is worked out again.
        self._sculpt = SculptCache()
        #: Records the whole making of a form, in the background, when the
        #: film is asked for.  Kept here rather than in the panel because it
        #: is the viewport that draws a stage.
        self._film = FilmRecorder(self)
        self._film.grew.connect(self._film_grew)
        self._film.settled.connect(self._film_settled)
        #: Whether frames are being rendered out of a film right now.  While
        #: they are, the stand-in belongs to the export rather than to the
        #: scrub handle, and a stage landing from the recorder must not put
        #: its own mesh into the middle of somebody's video.
        self._exporting = False

        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMinimumSize(320, 240)

        state.mesh_changed.connect(self._upload_mesh)
        state.matcap_changed.connect(self._upload_matcap)
        state.annotations_changed.connect(self._upload_strokes)
        state.render_changed.connect(self._sync_scene)
        state.armature_changed.connect(self._armature_moved)
        state.mesh_changed.connect(self._armature_moved)
        state.forms_changed.connect(self._forms_moved)
        state.skeleton_changed.connect(self._skeleton_moved)
        state.mesh_deformed.connect(self._upload_geometry)
        state.parts_changed.connect(self._upload_opacities)
        for signal in (
            state.camera_changed,
            state.measurements_changed,
            state.objects_changed,
        ):
            signal.connect(self.update)
        state.objects_changed.connect(self._active_changed)
        state.camera_changed.connect(self._stale_buried)

    # ------------------------------------------------------------------
    # GL lifecycle
    # ------------------------------------------------------------------

    def initializeGL(self) -> None:  # noqa: N802 - Qt naming
        # Qt destroys and recreates the context on some display changes, so
        # resources are released through the context's own signal.
        self.context().aboutToBeDestroyed.connect(self._release_gl)
        self._renderer.initialize()
        self._ready = True
        self._upload_mesh()
        self._upload_matcap()
        self._upload_strokes()
        self._upload_forms()
        self._sync_scene()

    #: How the depth grid is drawn: the depth cue's own blue, a hair over a
    #: pixel wide so it reads at any zoom without competing with the model.
    GUIDE_COLOR = (120 / 255, 200 / 255, 255 / 255)
    GUIDE_WIDTH = 1.2

    def _sync_guide(self) -> None:
        """Hand the renderer the depth grid, or take it away, before a frame."""
        drag = self._depth_drag
        if drag is None:
            if self._guide_shown:
                self._renderer.set_guide(build_segment_vertices(np.zeros((0, 2, 3)), (0, 0, 0), 1.0))
                self._guide_shown = False
            return
        segments, centre, reach = drag.grid(self._state.camera)
        self._renderer.set_guide(
            build_segment_vertices(segments, self.GUIDE_COLOR, self.GUIDE_WIDTH), centre, reach
        )
        self._guide_shown = True

    def paintGL(self) -> None:  # noqa: N802 - Qt naming
        self._sync_guide()
        glow = self._highlight_now()
        self._renderer.set_highlight(
            None if glow is None else glow[0], 0.0 if glow is None else glow[1], HIGHLIGHT_COLOR
        )
        painter = QPainter(self)
        painter.beginNativePainting()
        ratio = self.devicePixelRatioF()
        self._renderer.render(
            self._state.camera,
            self._state.render,
            int(self.width() * ratio),
            int(self.height() * ratio),
            ratio,
            self._antialiasing,
            refine=True,
            interactive=QApplication.mouseButtons() != Qt.MouseButton.NoButton,
        )
        painter.endNativePainting()
        if self._state.render.shading_mode is ShadingMode.HUMAN_SKIN:
            self._overlay.draw_caption(
                painter, self._renderer.skin.status, self.width(), self.height(), "bottom-left"
            )
        if self._renderer.skin.needs_frame and not self._exporting:
            self._skin_timer.start(16 if self._renderer.skin.tracing else 80)
        else:
            self._skin_timer.stop()
        self._overlay.draw(
            painter,
            self._state,
            self.measure_tool,
            self.annotate_tool,
            self.width(),
            self.height(),
            self.armature_tool,
            self._buried_nodes(),
            forms=self.form_tool,
            pose=self.pose_tool,
            occlude=self.pose_tool.grabbed is None and self._object_previous is None,
            objects=self.object_tool,
        )
        self._section_gizmo.draw(painter, self._picker(), self._state.render.section)
        if self._depth_drag is not None:
            self._depth_drag.draw(painter, self._state.camera, self.width(), self.height())
        if self._show_fps:
            self._overlay.draw_caption(
                painter, f"{self._fps:.1f} FPS", self.width(), self.height(), self._fps_corner
            )
        painter.end()
        if self._overlay.pending:
            # The markers were dimmed by the last view's answers to keep the
            # orbit smooth; one more frame after the throttle puts them right.
            QTimer.singleShot(int(self._overlay.THROTTLE * 1000) + 20, self.update)

    def _parts(self) -> list:
        return [(mesh, opacity) for _, mesh, opacity in self._state.mesh_parts]

    def _upload_mesh(self) -> None:
        if not self._ready:
            return
        self.makeCurrent()
        self._renderer.set_mesh(self._state.mesh, self._parts())
        self.doneCurrent()
        self._pedestal_key = self._section_key = self._sculpt_key = None
        self._sculpt.clear()
        self._sync_scene()

    def _upload_geometry(self) -> None:
        """Hand the renderer a re-posed model and nothing else.

        For the frames of a pose drag.  The pedestal, the section and the
        planes are all built on the model and all go stale, but rebuilding
        them at every pixel of a pull is what would make the pull unusable;
        they catch up on the :attr:`~ViewerState.mesh_changed` that follows
        when the button comes up.
        """
        if not self._ready:
            return
        self.makeCurrent()
        self._renderer.set_mesh(self._state.mesh, self._parts())
        self.doneCurrent()
        self._stale_buried()
        self.update()

    def _upload_opacities(self) -> None:
        """Hand the renderer how solid each object is now; nothing else moved."""
        if not self._ready:
            return
        self.makeCurrent()
        self._renderer.set_part_opacities([opacity for _, _, opacity in self._state.mesh_parts])
        self.doneCurrent()
        self.update()

    def _upload_matcap(self) -> None:
        if not self._ready:
            return
        self.makeCurrent()
        self._renderer.set_matcap(self._state.matcap_pixels)
        self.doneCurrent()
        self.update()

    def _upload_strokes(self) -> None:
        if not self._ready:
            return
        settings = self._state.annotation_settings
        self.makeCurrent()
        self._renderer.set_strokes(list(self._state.annotations) if settings.visible else [])
        self.doneCurrent()
        self.update()

    def _sync_scene(self) -> None:
        """Regenerate the pedestal and the cut contour when their settings move.

        Both are derived geometry rather than document state, so they are built
        here on demand instead of being kept in the viewer state.
        """
        if self._ready:
            render = self._state.render
            pedestal_key = (id(self._state.mesh), astuple(render.pedestal))
            if pedestal_key != self._pedestal_key:
                self._pedestal_key = pedestal_key
                self._upload_pedestal()
            section_key = (id(self._state.mesh), astuple(render.section))
            if section_key != self._section_key:
                self._section_key = section_key
                self._upload_contour()
            grid_key = (id(self._state.mesh), astuple(render.grid))
            if grid_key != self._grid_key:
                self._grid_key = grid_key
                self._upload_grid()
            planes = render.planes
            # Only the settings the stand-in is actually built from: the rest
            # of the Planes panel moves the shading, and re-cutting the form
            # for a change of contour colour would be a stall for nothing.
            sculpt_key = (
                id(self._state.mesh),
                planes.sculpts_geometry,
                planes.sculpt,
                planes.sculpt_count,
                planes.sculpt_masses,
                planes.sculpt_relax,
                planes.sculpt_smooth,
                planes.sculpt_median,
                planes.sculpt_median_reach,
                planes.sculpt_fineness,
                planes.sculpt_film,
                planes.sculpt_stage,
                planes.coefficients,
                # By where the wire is rather than by which one it is: bending
                # it is what asks for a fresh cut, and choosing a different
                # armature that happens to stand in the same place is not.
                self._wires_signature(),
            )
            if sculpt_key != self._sculpt_key:
                self._sculpt_key = sculpt_key
                self._upload_sculpt()
        self.update()

    def _upload_pedestal(self) -> None:
        mesh = self._state.mesh
        settings = self._state.render.pedestal
        disc = None if mesh is None else build_pedestal(mesh.bounds, settings)
        self.makeCurrent()
        self._renderer.set_pedestal(disc)
        self.doneCurrent()

    def _upload_grid(self) -> None:
        """Rebuild the reference grids for the scene as it stands."""
        mesh = self._state.mesh
        lines = build_grid(
            self._state.render.grid,
            None if mesh is None else mesh.bounds,
            self._state.camera.scene_radius,
        )
        self.makeCurrent()
        self._renderer.set_grid(lines)
        self.doneCurrent()

    def stop_recording(self) -> None:
        """End any film being recorded, and wait for its thread to really stop.

        For shutdown only.  Everywhere else a recording is abandoned rather
        than waited for, because waiting is the freeze the thread exists to
        avoid -- but on the way out the alternative is a live thread meeting
        an interpreter that is dismantling itself, which is a crash.
        """
        self._film.wait()

    def _sculpt_wires(self):
        """The armature the clay is to be built on, if one was chosen.

        Read here rather than held, because it is read from the document and
        the document is what the artist has just been editing.  Anything that
        is not an armature with bones in it -- no choice made, a choice left
        behind by a session with more armatures than this one, a wire with
        nothing joined up yet -- comes back as nothing at all, which is the
        mode finding its own masses the way it always has.
        """
        planes = self._state.render.planes
        index = int(planes.sculpt_armature)
        if planes.sculpt is not SculptMode.ADDITIVE:
            return None  # stone is cut out of a block, not built up on a wire
        if not 0 <= index < len(self._state.armatures):
            return None
        return wires_for(self._state.armatures[index])

    def _wires_signature(self) -> tuple | None:
        wires = self._sculpt_wires()
        return None if wires is None else wires.signature

    def _upload_sculpt(self) -> None:
        """Rebuild the planar stand-in and hand it to the renderer.

        Cutting a form into planes takes long enough on a heavy model to be
        felt, so the wait is shown for what it is rather than looking like a
        hang.  The model itself is untouched throughout: picking, measuring,
        painting and the section cut all still read the real surface.

        When the film is asked for, the same work is done a stage at a time on
        a thread instead, and what is drawn is whichever stage the scrub
        handle is on.  The first stage arrives in a fraction of the time the
        finished form would take, so the viewport fills rather than waiting.
        """
        planes = self._state.render.planes
        if self._state.mesh is None or not planes.sculpts_geometry:
            self._film.abandon()
            self._state.recording_changed.emit(False)
            self._show_sculpt(None)
            return
        wires = self._sculpt_wires()
        if not planes.sculpt_film:
            self._film.abandon()
            self._state.recording_changed.emit(False)
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            try:
                proxy = self._sculpt.mesh_for(self._state.mesh, planes, wires)
            finally:
                QApplication.restoreOverrideCursor()
            if proxy is not None:
                on = "" if wires is None else f" on {wires.count} lengths of wire"
                self._state.status_message.emit(
                    f"Form rebuilt from {planes.sculpt_count} planes{on}, "
                    f"{planes.sculpt.value}"
                )
            self._show_sculpt(proxy)
            return

        key = film_key(planes, planes.coefficients, wires)
        held = self._film.matching(key)
        if held is not None:
            # The same film the settings already asked for: only the stage
            # being looked at has changed, which is a lookup.
            self._show_stage(held)
            return
        film = self._film.start(
            self._state.mesh,
            self._sculpt.planes_for(self._state.mesh, planes),
            planes,
            key,
            wires,
        )
        self._state.recording_changed.emit(True)
        self._state.status_message.emit(
            f"Recording the making of the form, {planes.sculpt.value}..."
        )
        self._show_stage(film)

    def _film_grew(self, film) -> None:
        """A stage landed: show it if it is the one being looked at."""
        if film is not self._film.film:
            return
        self._state.film_changed.emit(film)
        self._show_stage(film)

    def _film_settled(self, film, complete: bool) -> None:
        if film is not self._film.film:
            return
        self._state.film_changed.emit(film)
        self._state.recording_changed.emit(False)
        if complete:
            self._state.status_message.emit(
                f"The making of the form, in {len(film)} stages"
            )

    def _show_stage(self, film) -> None:
        """Draw whichever stage of ``film`` the scrub handle is on."""
        planes = self._state.render.planes
        stage = film.at(planes.sculpt_stage)
        if stage is None:
            return  # nothing recorded yet; the viewport keeps what it has
        self._show_sculpt(film_shaded(stage, planes.sculpt_smooth))

    def _show_sculpt(self, proxy) -> None:
        if self._exporting:
            # The stand-in belongs to the export while one is running.  A
            # stage landing from the recorder mid-export would otherwise be
            # rendered into whichever frame happened to be next, and the film
            # is put back as it was when the export lets go.
            return
        self.makeCurrent()
        self._renderer.set_sculpt(proxy)
        self.doneCurrent()
        self.update()

    # ------------------------------------------------------------------
    # Rendering a film out to frames
    # ------------------------------------------------------------------

    @property
    def state(self) -> ViewerState:
        """The document being drawn."""
        return self._state

    @property
    def navigation(self) -> NavigationController:
        """How a drag turns into camera motion, so the preferences can set it."""
        return self._navigation

    def samples_in_use(self) -> int | None:
        """How many samples this view is really drawing with, or ``None``.

        Asked of GL rather than of the widget, because ``format().samples()``
        on a QOpenGLWidget reports nought whatever it was given -- the
        multisampling lives in the framebuffer Qt composites from and not in
        the context, and the context is what that method describes.  Which
        leaves the preference looking inert when it is working perfectly, so
        the number is fetched from the thing that knows and shown in the
        Preferences window.

        ``None`` before the view has a context, and on any driver that
        declines the question.
        """
        if not self._ready:
            return None
        try:
            self.makeCurrent()
            try:
                return sample_count()
            finally:
                self.doneCurrent()
        except Exception:  # pragma: no cover - driver-specific
            return None

    @property
    def film(self) -> Film | None:
        """The film of the form's making, as far as it has been recorded."""
        return self._film.film

    @property
    def exporting(self) -> bool:
        """Whether frames are being rendered out of a film right now."""
        return self._exporting

    def stage_image(self, stage: Stage, look: ExportLook) -> QImage:
        """One stage, rendered as it would be exported.  For the preview."""
        for image in self.stage_images([stage], look):
            return image
        raise RuntimeError("There was no stage to render")  # pragma: no cover

    def stage_images(self, stages: Iterable[Stage], look: ExportLook) -> Iterator[QImage]:
        """Render each of ``stages`` offscreen, at the size and look asked for.

        A generator, and deliberately one: the caller drives it a frame at a
        time from the event loop, so a hundred stages at four thousand pixels
        does not hold the GUI thread for the whole of a minute.  Closing it
        early -- which is what abandoning an export does -- runs the same
        tidy-up as finishing it, because that tidy-up is in a ``finally``.

        The frames are drawn into a framebuffer of this widget's own context
        rather than into the widget: the export size has nothing to do with
        the size of the window, and an artist should not have to make the
        viewport 4K in order to export at it.  Everything else is the code
        that draws the viewport, called with different arguments -- which is
        the point.  A clip that did not match what the artist had been looking
        at would be worth nothing to them.
        """
        if not self._ready:
            raise RuntimeError("The view has no graphics context yet")
        settings = look.render_settings(self._state.render)
        smooth = self._state.render.planes.sculpt_smooth
        # Line widths and handle radii arrive in logical pixels, and the same
        # numbers at four times the size would be hairlines.  This is the
        # same conversion the widget does for a high-DPI screen.
        ratio = look.width / max(self.width(), 1)
        width, height = look.width, look.height
        self._exporting = True
        surface: QOpenGLFramebufferObject | None = None
        try:
            self.makeCurrent()
            if not look.annotations:
                self._renderer.set_strokes([])
            if not look.pedestal:
                self._renderer.set_pedestal(None)
            surface = self._export_surface(width, height)
            self.doneCurrent()
            for stage in stages:
                self.makeCurrent()
                self._renderer.set_sculpt(film_shaded(stage, smooth))
                image = self._render_offscreen(surface, settings, width, height, ratio)
                self.doneCurrent()
                self._draw_over(image, look, stage, ratio)
                yield image
        finally:
            self._exporting = False
            self.makeCurrent()
            del surface
            self._renderer.set_strokes(
                list(self._state.annotations)
                if self._state.annotation_settings.visible
                else []
            )
            self.doneCurrent()
            if not look.pedestal:
                self._upload_pedestal()
            film = self._film.film
            if film is not None:
                self._show_stage(film)
            self.update()

    @staticmethod
    def _export_surface(width: int, height: int) -> QOpenGLFramebufferObject:
        """An offscreen target the frames are drawn into, made once per export.

        Multisampled, because the edges of a blocked-in form are all straight
        lines at odd angles and are exactly what aliasing ruins -- and a video
        codec then spends its bits on the stair steps.  A driver that refuses
        the samples at the size asked for gets a second chance without them,
        since a frame with jagged edges beats no export at all.
        """
        for samples in (4, 0):
            layout = QOpenGLFramebufferObjectFormat()
            layout.setAttachment(QOpenGLFramebufferObject.Attachment.CombinedDepthStencil)
            layout.setSamples(samples)
            surface = QOpenGLFramebufferObject(width, height, layout)
            if surface.isValid():
                return surface
        raise RuntimeError(
            f"The graphics driver would not give a {width}x{height} frame to draw into"
        )

    def _render_offscreen(
        self,
        surface: QOpenGLFramebufferObject,
        settings,
        width: int,
        height: int,
        ratio: float,
    ) -> QImage:
        """Draw the scene into ``surface`` and read it back as an image."""
        kept = current_framebuffer()
        surface.bind()
        try:
            # A line round the active object is a thing of the view, not of
            # the film; whatever is fading on screen stays off the frames.
            self._renderer.set_highlight(None)
            self._renderer.render(
                self._state.camera, settings, width, height, ratio, self._antialiasing
            )
        finally:
            # Not `release`, which binds framebuffer zero: in a widget the
            # default framebuffer is Qt's own, and leaving zero bound behind
            # is a window that draws nothing until something else rebinds it.
            bind_default(kept)
        return surface.toImage().convertToFormat(QImage.Format.Format_RGB888)

    def _draw_over(
        self, image: QImage, look: ExportLook, stage: Stage, ratio: float
    ) -> None:
        """Lay the overlay -- and the caption, if it was asked for -- on a frame.

        Painted in logical pixels and scaled up, rather than being given the
        export's own size: the overlay places things by projecting the camera
        through a width and a height, and the projection has to agree with the
        one the scene was just drawn with.
        """
        painter = QPainter(image)
        painter.scale(ratio, ratio)
        width = int(round(image.width() / ratio))
        height = int(round(image.height() / ratio))
        self._overlay.draw(
            painter,
            self._state,
            self.measure_tool,
            self.annotate_tool,
            width,
            height,
            self.armature_tool,
            self._buried_nodes(),
            look.parts,
            forms=self.form_tool,
            pose=self.pose_tool,
        )
        if look.caption:
            self._overlay.draw_caption(painter, look.caption_for(stage), width, height)
        painter.end()

    def _upload_contour(self) -> None:
        """Cut the mesh with each section plane and expand the result to strokes."""
        settings = self._state.render.section
        mesh = self._state.mesh
        blocks = []
        if mesh is not None and settings.enabled and settings.show_contour:
            for plane in settings.planes():
                segments = section_segments(mesh, plane)
                # The stroke shader lifts along the supplied normal, so point it
                # into the material that survives the cut.
                blocks.append(
                    build_segment_vertices(
                        segments, settings.contour_color, settings.contour_width, -plane.normal
                    )
                )
        vertices = np.concatenate(blocks) if blocks else np.zeros((0, 14), dtype=np.float32)
        self.makeCurrent()
        self._renderer.set_contour(vertices)
        self.doneCurrent()

    def _release_gl(self) -> None:
        """Free every GL object while the owning context is still current."""
        self._skin_timer.stop()
        if not self._ready:
            return
        self.makeCurrent()
        self._renderer.dispose()
        self.doneCurrent()
        self._ready = False

    # ------------------------------------------------------------------
    # Tool control
    # ------------------------------------------------------------------

    def set_measure_active(self, active: bool) -> None:
        self._arm(self.measure_tool, active)

    def set_annotate_active(self, active: bool) -> None:
        self._arm(self.annotate_tool, active)

    def set_armature_active(self, active: bool) -> None:
        self._arm(self.armature_tool, active)

    def set_form_active(self, active: bool) -> None:
        self._arm(self.form_tool, active)

    def set_pose_active(self, active: bool) -> None:
        self._arm(self.pose_tool, active)

    def set_object_active(self, active: bool) -> None:
        self._arm(self.object_tool, active)

    def _arm(self, tool, active: bool) -> None:
        """Arm one tool, disarming the rest.

        Only one gesture can own the left button, so arming is written once
        here rather than as a pairwise dance between every two tools.
        """
        self.cancel_tools()
        tool.set_active(active)
        if active:
            for other in (
                self.measure_tool,
                self.annotate_tool,
                self.armature_tool,
                self.form_tool,
                self.pose_tool,
                self.object_tool,
            ):
                if other is not tool:
                    other.set_active(False)
        self._refresh_cursor()
        self.update()

    def cancel_tools(self) -> None:
        """Drop whatever gesture is half-finished, without disarming the tool."""
        if self._section_gizmo.drag is not None:
            self._state.render.section.offset = self._section_gizmo.drag[1]
            self._section_gizmo.drag = None
            self._state.notify_render()
        if self._grab_previous is not None:
            target, field, value = self._grab_previous
            setattr(target, field, value)
            self._grab_previous = None
            self.measure_tool.grabbed_handle = None
            self._state.notify_measurements()
        if self._node_previous is not None:
            target, field, value = self._node_previous
            setattr(target, field, value)
            self._node_previous = None
            self.armature_tool.grabbed_handle = None
            self.armature_tool.resizing = False
            self._state.notify_armature()
        if self._landmark_previous is not None:
            index, _, previous = self._landmark_previous
            for field, value in previous.items():
                setattr(self._state.armatures[index], field, value)
            self._landmark_previous = None
            self.armature_tool.grabbed_landmark = None
            self._state.notify_armature()
        if self._form_previous is not None:
            index, _, previous = self._form_previous
            self._state.forms[index].landmarks = previous
            self._form_previous = None
            self.form_tool.grabbed_landmark = None
            self._state.notify_forms()
        if self._pose_previous is not None:
            index, target, field, previous, _ = self._pose_previous
            skeleton = self._state.skeletons[index]
            if field == "joints":
                skeleton.joints = previous
            else:
                setattr(skeleton.joints[target], field, previous)
            self._pose_previous = None
            self._pose_anchor = None
            self._pose_dragged = False
            self.pose_tool.grabbed = None
            self.pose_tool.mode = ""
            self._state.notify_skeleton()
        if self._object_previous is not None:
            before, self._object_previous = self._object_previous, None
            self._object_held = None
            self.object_tool.end()
            self._state.restore_objects(before)
        self._depth_drag = None
        self._press_position = None
        self._join_from = None
        self._navigation.end()
        self.measure_tool.cancel()
        self.annotate_tool.cancel()
        self.armature_tool.cancel()
        self.form_tool.cancel()
        self.pose_tool.cancel()
        self.object_tool.cancel()
        self._refresh_cursor()
        self.update()

    def _refresh_cursor(self) -> None:
        armed = self.measure_tool.active or self.annotate_tool.active
        if self.object_tool.active:
            # The gizmo's handles are what is taken hold of; the rest of the
            # view still orbits, and the cursor says which is which.
            self.setCursor(
                Qt.CursorShape.OpenHandCursor
                if self.object_tool.hover_handle
                else Qt.CursorShape.ArrowCursor
            )
        elif armed or self.armature_tool.active or self.form_tool.active or self.pose_tool.active:
            self.setCursor(Qt.CursorShape.CrossCursor)
        elif (
            self.measure_tool.hover_handle
            or self.armature_tool.hover_handle
            or self.armature_tool.hover_landmark
            or self.form_tool.hover_landmark
            or self.pose_tool.hover_joint
            or self.pose_tool.hover_bone
            or self._section_gizmo.hover
        ):
            self.setCursor(Qt.CursorShape.OpenHandCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    # ------------------------------------------------------------------
    # Interaction
    # ------------------------------------------------------------------

    def set_show_fps(self, enabled: bool) -> None:
        if self._show_fps == enabled:
            return
        self._show_fps = enabled
        self._fps_start = perf_counter()
        self._fps_frames = 0
        self.update()

    def set_antialiasing(self, mode: str) -> None:
        """One of the renderer's :data:`~refview.render.mesh_renderer.ANTIALIASING_MODES`."""
        if self._antialiasing == mode:
            return
        self._antialiasing = mode
        self.update()

    def set_fps_corner(self, corner: str) -> None:
        if self._fps_corner == corner:
            return
        self._fps_corner = corner
        self.update()

    def _frame_presented(self) -> None:
        if not self._show_fps or not self.isVisible():
            return
        self._fps_frames += 1
        elapsed = perf_counter() - self._fps_start
        if elapsed >= 0.5:
            self._fps = self._fps_frames / elapsed
            self._fps_frames = 0
            self._fps_start = perf_counter()
        self.update()

    def select_measurement(self, measurement) -> None:
        self.measure_tool.selected = measurement
        self.update()

    def _begin_depth_drag(self, y):
        point = None
        if self._form_previous is not None:
            index, key, _ = self._form_previous
            point = self._state.forms[index].landmark_for(key).point
        elif self._landmark_previous is not None:
            index, key, _ = self._landmark_previous
            point = self._state.armatures[index].landmark_for(key).point
        elif self._node_previous is not None:
            point = self._node_previous[0].point
        elif self._pose_anchor is not None:
            point = self._pose_anchor
        elif self._grab_previous is not None:
            point = self._grab_previous[2]
        if point is not None:
            self._depth_drag = DepthDrag.begin(point, y, self._picker())
            self.update()

    def mousePressEvent(self, event) -> None:  # noqa: N802 - Qt naming
        position = event.position()
        x, y = position.x(), position.y()
        self._press_position = (x, y)
        self._travel = 0.0

        if event.button() == Qt.MouseButton.LeftButton and not self._orbit_override(event):
            depth = bool(event.modifiers() & Qt.KeyboardModifier.ControlModifier)
            if self.object_tool.active and self._begin_object_drag(x, y):
                self.update()
                return
            if self._section_gizmo.begin(x, y, self._picker(), self._state.render.section):
                self.update()
                return
            # Painting owns the button outright; otherwise a press that lands on
            # an unlocked endpoint moves it instead of turning the camera.
            if self.annotate_tool.active and not depth:
                claimed = self._begin_annotation(x, y)
            else:
                resize = not depth and bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
                # Landmarks are offered first, within a tighter reach: a node
                # derived from one sits right beside it, and the landmark is the
                # thing that can still be corrected without the armature
                # leaving its preset.
                claimed = (
                    self._begin_form_landmark_drag(x, y)
                    or self._begin_landmark_drag(x, y)
                    or self._begin_node_drag(x, y, resize)
                    or self._begin_joint_drag(x, y, resize)
                    or self._begin_handle_drag(x, y)
                )
            if claimed:
                if depth:
                    self._begin_depth_drag(y)
                return
        elif event.button() not in (
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.RightButton,
            Qt.MouseButton.MiddleButton,
        ):
            return

        mode = DragMode.ORBIT if event.button() == Qt.MouseButton.LeftButton else DragMode.PAN
        self._navigation.begin(
            mode, x, y, self._state.camera, self.width(), self.height(), self._scene_center()
        )

    def mouseMoveEvent(self, event) -> None:  # noqa: N802 - Qt naming
        position = event.position()
        x, y = position.x(), position.y()

        if self._press_position is not None:
            self._travel = max(self._travel, abs(x - self._press_position[0])
                               + abs(y - self._press_position[1]))
        if self._object_previous is not None:
            self._move_grabbed_object(x, y, self._snap_degrees(event))
            return
        if self._section_gizmo.drag is not None:
            self._state.render.section.offset = self._section_gizmo.move(x, y)
            self._state.notify_render()
            return
        if self.form_tool.grabbed_landmark is not None:
            self._move_grabbed_form_landmark(x, y)
            return
        if self.armature_tool.grabbed_landmark is not None:
            self._move_grabbed_landmark(x, y)
            return
        if self.armature_tool.grabbed_handle is not None:
            self._move_grabbed_node(x, y)
            return
        if self.pose_tool.grabbed is not None:
            self._move_grabbed_joint(x, y)
            return
        if self.measure_tool.grabbed_handle is not None:
            self._move_grabbed_handle(x, y)
            return
        if self.annotate_tool.is_drawing or self._erase_previous is not None:
            self._continue_annotation(x, y)
            return
        if self._navigation.is_dragging:
            if self._press_position is not None:
                self._travel = max(
                    self._travel,
                    abs(x - self._press_position[0]) + abs(y - self._press_position[1]),
                )
            snap = self._snap_degrees(event)
            if self._navigation.drag(
                x, y, self._state.camera, self.width(), self.height(), snap
            ):
                self.update()
            return

        self._update_hover(x, y)

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802 - Qt naming
        if self._press_position is None:
            return
        was_click = self._travel <= self.CLICK_TOLERANCE
        position = event.position()

        if event.button() != Qt.MouseButton.LeftButton and (
            self._depth_drag is not None or self._section_gizmo.drag is not None
        ):
            return
        if self._object_previous is not None:
            self._commit_object_drag()
        elif self._section_gizmo.drag is not None:
            previous = self._section_gizmo.drag[1]
            self._section_gizmo.drag = None
            section = self._state.render.section
            if section.offset != previous:
                self._state.do(SetAttributes(section, {"offset": section.offset},
                    text="Move cutting plane", channel="render", previous={"offset": previous}),
                    apply=False)
        elif self.form_tool.grabbed_landmark is not None:
            self._commit_form_landmark_drag(was_click)
        elif self.armature_tool.grabbed_landmark is not None:
            self._commit_landmark_drag(was_click)
        elif self.armature_tool.grabbed_handle is not None:
            joining = self.armature_tool.active or bool(
                event.modifiers() & Qt.KeyboardModifier.ControlModifier
            )
            self._commit_node_drag(was_click, joining)
        elif self.pose_tool.grabbed is not None:
            self._commit_joint_drag(was_click)
        elif self.measure_tool.grabbed_handle is not None:
            self._commit_handle_drag()
        elif self.annotate_tool.is_drawing or self._erase_previous is not None:
            self._commit_annotation()
        else:
            self._navigation.end()
            left = event.button() == Qt.MouseButton.LeftButton
            if was_click and left and self._orbit_override(event):
                # Alt went down for an orbit that never travelled: an
                # Alt-click, which picks an object whatever tool is armed.
                self._pick_object(position.x(), position.y())
            elif was_click and left and self.measure_tool.active:
                self._place_measure_point(position.x(), position.y())
            elif was_click and left and self.armature_tool.active:
                self._place_armature_node(position.x(), position.y())
            elif was_click and left and self.form_tool.active:
                self._place_form_landmark(position.x(), position.y())
            elif was_click and left and self.pose_tool.active:
                self._place_joint(position.x(), position.y())
            elif was_click and left and self.object_tool.active:
                self._pick_object(position.x(), position.y())

        self._depth_drag = None
        self._press_position = None
        self._travel = 0.0
        self.update()

    def wheelEvent(self, event) -> None:  # noqa: N802 - Qt naming
        if self._press_position is not None:
            return
        notches = event.angleDelta().y() / 120.0
        if notches == 0.0:
            return
        position = event.position()
        picker = self._picker()
        self._navigation.zoom(
            notches,
            position.x(),
            position.y(),
            self._state.camera,
            self.width(),
            self.height(),
            anchor=picker.point(position.x(), position.y()),
        )
        self.update()

    def event(self, event) -> bool:
        # A key the view's shortcuts would take is offered to the widget
        # first; accepting the offer is what keeps W, E and R for the
        # transform tool while it is armed, and leaves them where they were
        # -- the eraser, the armature tool -- the rest of the time.
        if event.type() == QEvent.Type.ShortcutOverride and self._gesture_for(event) is not None:
            event.accept()
            return True
        return super().event(event)

    def keyPressEvent(self, event) -> None:  # noqa: N802 - Qt naming
        if event.key() == Qt.Key.Key_Escape:
            self.cancel_tools()
            return
        mode = self._gesture_for(event)
        if mode is not None:
            self.object_tool.set_mode(mode)
            self.object_mode_changed.emit(mode)
            self.update()
            return
        super().keyPressEvent(event)

    # ------------------------------------------------------------------
    # Measurement handles
    # ------------------------------------------------------------------

    def _begin_handle_drag(self, x: float, y: float) -> bool:
        handle = self.measure_tool.handle_at(
            x, y, self._state.measurements, self._picker(), self._state.measurement_settings
        )
        if handle is None:
            return False
        index, end = handle
        measurement = self._state.measurements[index]
        field = measurement.endpoint_field(end)
        self._grab_previous = (measurement, field, getattr(measurement, field))
        self.measure_tool.grabbed_handle = handle
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        return True

    def _move_grabbed_handle(self, x: float, y: float) -> None:
        if self._grab_previous is None:
            return
        measurement, field, _ = self._grab_previous
        point = self.measure_tool.drag_target(
            x,
            y,
            self._picker(),
            self._state.measurement_settings,
            np.asarray(getattr(measurement, field), dtype=np.float64),
        )
        setattr(measurement, field, tuple(float(v) for v in point))
        self._state.notify_measurements()

    def _commit_handle_drag(self) -> None:
        """Record the finished drag as a single undo step."""
        self.measure_tool.grabbed_handle = None
        self._refresh_cursor()
        if self._grab_previous is None:
            return
        measurement, field, previous = self._grab_previous
        self._grab_previous = None
        if getattr(measurement, field) == previous:
            return
        self._state.do(
            SetAttributes(
                measurement,
                {field: getattr(measurement, field)},
                text=f"Move {measurement.name}",
                channel=MEASUREMENTS,
                previous={field: previous},
            ),
            apply=False,
        )

    # ------------------------------------------------------------------
    # Annotations
    # ------------------------------------------------------------------

    def _begin_annotation(self, x: float, y: float) -> bool:
        if not self.annotate_tool.active or self._state.mesh is None:
            return False
        if self._state.annotation_settings.mode.is_eraser:
            self._erase_previous = list(self._state.annotations)
            self._erase_at(x, y)
            return True
        return self.annotate_tool.begin(x, y, self._picker(), self._state.annotation_settings)

    def _continue_annotation(self, x: float, y: float) -> None:
        if self._erase_previous is not None:
            self.annotate_tool.cursor = (x, y)
            self._erase_at(x, y)
            return
        if self.annotate_tool.drag(x, y, self._picker(), self._state.annotation_settings):
            self.update()

    def _commit_annotation(self) -> None:
        if self._erase_previous is not None:
            previous, self._erase_previous = self._erase_previous, None
            current = self._state.annotations.items
            if len(current) != len(previous) or any(
                a is not b for a, b in zip(current, previous, strict=True)
            ):
                self._state.do(
                    ReplaceItems(
                        current,
                        list(current),
                        text="Erase annotation",
                        channel=ANNOTATIONS,
                        previous=previous,
                    ),
                    apply=False,
                )
            return

        strokes = self.annotate_tool.finish(self._picker(), self._state.annotation_settings)
        if not strokes:
            self.update()
            return
        items = self._state.annotations.items
        label = f"Paint {strokes[0].kind.label.lower()}"
        # A gesture that crossed the silhouette lands as several strokes; they
        # were one movement, so they undo as one step.
        command = (
            AddItem(items, strokes[0], text=label, channel=ANNOTATIONS)
            if len(strokes) == 1
            else ReplaceItems(items, [*items, *strokes], text=label, channel=ANNOTATIONS)
        )
        self._state.do(command)

    def _erase_at(self, x: float, y: float) -> None:
        """Rub out the stroke points under the eraser, live."""
        target = self.annotate_tool.erase_target(
            x, y, self._picker(), self._state.annotation_settings
        )
        if target is None:
            self.update()
            return
        remaining = self._state.annotations.erased(*target)
        if remaining is None:
            self.update()
            return
        self._state.annotations.items[:] = remaining
        self._state.notify_annotations()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _orbit_override(event) -> bool:
        """Alt forces the camera gesture, whichever tool is armed."""
        return bool(event.modifiers() & Qt.KeyboardModifier.AltModifier)

    # ------------------------------------------------------------------
    # Armature
    # ------------------------------------------------------------------

    def _armature_index(self) -> int:
        """Which armature an edit lands in, counting a guided run as binding."""
        run = self.armature_tool.guide
        if run is not None and 0 <= run.armature < len(self._state.armatures):
            return run.armature
        selected = self.armature_tool.selected
        if selected is not None and selected[0] < len(self._state.armatures):
            return selected[0]
        return len(self._state.armatures) - 1

    def _place_armature_node(self, x: float, y: float) -> None:
        """Drop a node, or record the landmark a guided run is asking for."""
        index = self._armature_index()
        if index < 0:
            return
        armature = self._state.armatures[index]
        settings = self._state.armature_settings
        point = self.armature_tool.pick(x, y, self._picker(), settings)
        if point is None:
            self.pick_failed.emit()
            return

        self.armature_tool.hover_point = point
        edit = self._insert_on_bone(x, y) or self.armature_tool.place(armature, point, settings)
        if edit is None:
            return
        nodes, bones, landmarks = edit
        label = "Place landmark" if self.armature_tool.guiding else f"Add node to {armature.name}"
        self.armature_edited.emit((index, nodes, bones, landmarks, label))
        if not self.armature_tool.guiding and nodes:
            self.armature_tool.selected = (index, len(nodes) - 1)
            self.armature_selected.emit((index, len(nodes) - 1))
        self._stale_buried()
        self.update()

    def _insert_on_bone(self, x: float, y: float):
        """A click on a length of wire lengthens the chain rather than branching off it.

        Only outside a guided run: while a preset is asking for the next
        landmark, a click is an answer to that question and nothing else.
        """
        tool = self.armature_tool
        if tool.guiding:
            return None
        picker = self._picker()
        found = tool.bone_at(x, y, self._state.armatures, picker, self._state.armature_settings)
        if found is None:
            return None
        index, position = found
        armature = self._state.armatures[index]
        point = tool.split_point(armature, armature.bones[position], x, y, picker)
        if point is None:
            return None
        return tool.insert_on_bone(armature, position, point)

    def _begin_node_drag(self, x: float, y: float, resize: bool) -> bool:
        """Take hold of a node, to move it, resize it, or just to select it.

        This works whether or not the tool is armed, exactly as an unlocked
        measurement endpoint does: clicking a node to see which one it is
        should not first require arming anything.
        """
        handle = self.armature_tool.handle_at(
            x, y, self._state.armatures, self._picker(), self._state.armature_settings
        )
        if handle is None:
            return False
        index, position = handle
        node = self._state.armatures[index].nodes[position]
        field = "size" if resize else "at"
        self._node_previous = (node, field, getattr(node, field))
        self._join_from = self.armature_tool.selected
        self.armature_tool.grabbed_handle = handle
        self.armature_tool.resizing = resize
        self.armature_tool.selected = handle
        self.setCursor(
            Qt.CursorShape.SizeHorCursor if resize else Qt.CursorShape.ClosedHandCursor
        )
        return True

    def _move_grabbed_node(self, x: float, y: float) -> None:
        """Apply the drag live, so the artist sees the wire bend as they pull it."""
        if self._node_previous is None:
            return
        node, field, _ = self._node_previous
        picker = self._picker()
        if field == "size":
            node.size = self.armature_tool.size_target(x, y, picker, node)
        else:
            point = self.armature_tool.drag_target(
                x, y, picker, self._state.armature_settings, node.point
            )
            node.at = tuple(float(value) for value in point)
        self._state.notify_armature()

    def _commit_node_drag(self, was_click: bool = False, joining: bool = False) -> None:
        """Record the finished gesture: a move, a resize, or a plain click.

        A press that never travelled did not edit anything, so it is read as a
        selection instead -- and, with the tool armed or Ctrl held, as a second
        node to run a bone to.
        """
        handle = self.armature_tool.grabbed_handle
        self.armature_tool.grabbed_handle = None
        self.armature_tool.resizing = False
        self._refresh_cursor()
        anchor, self._join_from = self._join_from, None
        if self._node_previous is None:
            return
        node, field, previous = self._node_previous
        self._node_previous = None

        if getattr(node, field) != previous:
            verb = "Resize" if field == "size" else "Move"
            self._state.do(
                SetAttributes(
                    node,
                    {field: getattr(node, field)},
                    text=f"{verb} {node.name}",
                    channel=ARMATURE,
                    previous={field: previous},
                ),
                apply=False,
            )
            self._detach_from_preset(node)
            return

        if not was_click or handle is None:
            return
        self.armature_selected.emit(handle)
        if joining and anchor is not None and anchor != handle:
            self._join_nodes(anchor, handle)
        self.update()

    # -- landmarks ------------------------------------------------------
    #
    # A node is one object with a position, so dragging one writes through to it
    # and the undo step is one attribute.  A landmark is not: the wire is
    # derived from the whole set, so moving one rewrites three lists at once.
    # Hence its own trio of methods rather than a flag through the node drag.

    def _begin_landmark_drag(self, x: float, y: float) -> bool:
        """Take hold of a landmark, to move it or just to say which one it is."""
        found = self.armature_tool.landmark_at(
            x, y, self._state.armatures, self._picker(), self._state.armature_settings
        )
        if found is None:
            return False
        index, key = found
        armature = self._state.armatures[index]
        # Copied, not shared: the re-derive below builds fresh lists, and what
        # an undo puts back must not be something a later drag can reach into.
        self._landmark_previous = (
            index,
            key,
            {
                "nodes": list(armature.nodes),
                "bones": list(armature.bones),
                "landmarks": [replace(entry) for entry in armature.landmarks],
            },
        )
        self.armature_tool.grabbed_landmark = found
        self.armature_tool.selected_landmark = found
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        return True

    def _move_grabbed_landmark(self, x: float, y: float) -> None:
        """Apply the drag live, so the figure re-forms under the cursor."""
        if self._landmark_previous is None:
            return
        index, key, _ = self._landmark_previous
        armature = self._state.armatures[index]
        landmark = armature.landmark_for(key)
        if landmark is None:
            return
        point = self.armature_tool.drag_target(
            x, y, self._picker(), self._state.armature_settings, landmark.point
        )
        landmarks = armature.with_landmark_at(key, tuple(float(value) for value in point))
        # The same re-derive the panel's position boxes go through, applied
        # straight rather than through the history: the whole drag is one step,
        # recorded when the button comes up.
        if armature.derived:
            nodes, bones, landmarks = self.armature_tool.derive(
                armature, landmarks, self._state.armature_settings
            )
            armature.nodes, armature.bones = nodes, bones
        armature.landmarks = landmarks
        self._state.notify_armature()

    def _commit_landmark_drag(self, was_click: bool = False) -> None:
        """Record the finished drag as one step, or read a press as a selection."""
        found = self.armature_tool.grabbed_landmark
        self.armature_tool.grabbed_landmark = None
        self._refresh_cursor()
        if self._landmark_previous is None:
            return
        index, key, previous = self._landmark_previous
        self._landmark_previous = None
        armature = self._state.armatures[index]

        before = next((entry for entry in previous["landmarks"] if entry.key == key), None)
        after = armature.landmark_for(key)
        if after is not None and (before is None or before.at != after.at):
            self._state.do(
                SetAttributes(
                    armature,
                    {name: getattr(armature, name) for name in previous},
                    text=f"Move {landmark_title(armature, key)}",
                    channel=ARMATURE,
                    previous=previous,
                ),
                apply=False,
            )
            return

        if was_click and found is not None:
            self.landmark_selected.emit(found)
        self.update()

    def _join_nodes(self, first: tuple[int, int], second: tuple[int, int]) -> None:
        """Run a bone between two nodes of the same armature."""
        if first[0] != second[0] or not 0 <= first[0] < len(self._state.armatures):
            return
        armature = self._state.armatures[first[0]]
        edit = self.armature_tool.join(armature, first[1], second[1])
        if edit is None:
            return
        name = armature.nodes[second[1]].name
        self.armature_edited.emit((first[0], *edit, f"Join {name}"))

    def _detach_from_preset(self, node: ArmatureNode) -> None:
        """A node moved by hand stops following its landmarks.

        Recorded as its own step rather than folded into the drag, so undoing
        the move puts the armature back under the preset as well.
        """
        for armature in self._state.armatures:
            if not armature.derived or node not in armature.nodes:
                continue
            self._state.do(
                SetAttributes(
                    armature,
                    {"derived": False},
                    text=f"Detach {armature.name} from its preset",
                    channel=ARMATURE,
                )
            )
            return

    def _armature_moved(self) -> None:
        """The wire changed: redraw it, and re-cut anything built on it.

        Not mid-drag, though.  A node being pulled about emits on every mouse
        move, and cutting a form takes seconds, so the clay follows the wire
        when the wire is let go of -- the same bargain the geometry sliders
        make, and for the same reason.  The overlay still follows the drag
        itself, so the wire bends under the cursor either way.
        """
        self._stale_buried()
        held = (
            self.armature_tool.grabbed_handle is not None
            or self.armature_tool.grabbed_landmark is not None
        )
        if not held:
            self._sync_scene()
        self.update()

    def _stale_buried(self) -> None:
        self._overlay.invalidate_visibility()

    def _buried_nodes(self) -> frozenset[tuple[int, int]]:
        """Use the same cached visibility test for bones and all point markers."""
        settings = self._state.armature_settings
        if settings.buried is Buried.SHOW or not settings.show_all:
            return frozenset()
        return self._overlay.buried_nodes(self._state, self.width(), self.height())

    def center_on_point(self, point) -> None:
        """Slide the view so a point sits at the centre, keeping the angle."""
        camera = self._state.camera
        offset = np.asarray(point, dtype=np.float64) - camera.target
        camera.eye = camera.eye + offset
        camera.target = camera.target + offset
        self._state.notify_camera()

    def _snap_degrees(self, event) -> float:
        """Orbit increment while Shift is held, or 0 for a free orbit."""
        shift = bool(event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
        return self._state.navigation.snap_angle_deg if shift else 0.0

    def _picker(self) -> SurfacePicker:
        return SurfacePicker(self._state.camera, self._state.mesh, self.width(), self.height(),
                             self._depth_drag)

    def _scene_center(self) -> np.ndarray | None:
        """Object centre, which anchors the plane the orbit pivot lies on."""
        mesh = self._state.mesh
        return None if mesh is None else np.asarray(mesh.bounds.center, dtype=np.float64)

    def _update_hover(self, x: float, y: float) -> None:
        """Track whatever the cursor is over, so the overlay can respond."""
        dirty = False
        if self.object_tool.active:
            handle = self.object_tool.handle_at(x, y, self._object_gizmo())
            if handle != self.object_tool.hover_handle:
                self.object_tool.hover_handle = handle
                self._refresh_cursor()
                dirty = True
        # The rail takes the press before any tool does, so it is offered first.
        over_rail = self._section_gizmo.hit(x, y, self._picker(), self._state.render.section)
        if over_rail != self._section_gizmo.hover:
            self._section_gizmo.hover = over_rail
            self._refresh_cursor()
            dirty = True
        if self.annotate_tool.active:
            self.annotate_tool.cursor = (x, y)
            dirty = True
        if self.measure_tool.active:
            self.measure_tool.hover_point = self.measure_tool.pick(
                x, y, self._picker(), self._state.measurement_settings
            )
            dirty = True

        if self.armature_tool.active:
            self.armature_tool.hover_point = self.armature_tool.pick(
                x, y, self._picker(), self._state.armature_settings
            )
            dirty = True
        if self.form_tool.active:
            self.form_tool.hover_point = self.form_tool.pick(
                x, y, self._picker(), self._state.form_settings
            )
            dirty = True
        if self.pose_tool.active:
            self.pose_tool.hover_point = self.pose_tool.pick(
                x, y, self._picker(), self._state.skeleton_settings
            )
            dirty = True
        if self._update_form_hover(x, y):
            dirty = True
        if self._update_armature_hover(x, y):
            dirty = True
        if self._update_pose_hover(x, y):
            dirty = True

        previous = self.measure_tool.hover_handle
        self.measure_tool.hover_handle = (
            None
            if self.annotate_tool.active
            or self.armature_tool.hover_handle is not None
            or self.armature_tool.hover_landmark is not None
            or self.form_tool.hover_landmark is not None
            or self.pose_tool.hover_joint is not None
            else self.measure_tool.handle_at(
                x, y, self._state.measurements, self._picker(), self._state.measurement_settings
            )
        )
        if self.measure_tool.hover_handle != previous:
            self._refresh_cursor()
            dirty = True
        if dirty:
            self.update()

    def _update_armature_hover(self, x: float, y: float) -> bool:
        """Track the node and bone under the cursor; True when anything changed."""
        tool = self.armature_tool
        settings = self._state.armature_settings
        picker = self._picker()
        # In the order the press resolves them, so what lights up under the
        # cursor is what taking hold would actually grab.
        landmark = (
            None
            if self.annotate_tool.active or self.form_tool.hover_landmark is not None
            else tool.landmark_at(x, y, self._state.armatures, picker, settings)
        )
        handle = (
            None
            if landmark is not None or self.annotate_tool.active
            else tool.handle_at(x, y, self._state.armatures, picker, settings)
        )
        bone = (
            None
            if landmark is not None or handle is not None or self.annotate_tool.active
            else tool.bone_at(x, y, self._state.armatures, picker, settings)
        )
        changed = (
            handle != tool.hover_handle
            or bone != tool.hover_bone
            or landmark != tool.hover_landmark
        )
        if handle != tool.hover_handle or landmark != tool.hover_landmark:
            tool.hover_handle = handle
            tool.hover_landmark = landmark
            self._refresh_cursor()
        tool.hover_bone = bone
        return changed

    # ------------------------------------------------------------------
    # Objects
    # ------------------------------------------------------------------
    #
    # A drag on the gizmo rewrites the active object's transform on every
    # move, so the figure follows the hand, and the whole drag is recorded
    # as one step when the button comes up: the snapshot of the objects
    # taken at the press against the one taken at the release.

    def _object_gizmo(self):
        """Where the active object's gizmo falls on screen, or ``None``."""
        active = self._state.active_object
        if active is None or not self._state.objects.shown(active, self._state.object_settings):
            return None
        return self.object_tool.gizmo(self._picker(), self._state.objects.world_matrix(active))

    def _begin_object_drag(self, x: float, y: float) -> bool:
        active = self._state.active_object
        if active is None:
            return False
        handle = self.object_tool.handle_at(x, y, self._object_gizmo())
        if handle is None:
            return False
        objects = self._state.objects
        began = self.object_tool.begin(
            handle,
            x,
            y,
            self._picker(),
            objects.world_matrix(active),
            objects.parent_matrix(active),
        )
        if not began:
            return False
        self._object_previous = self._state.snapshot_objects()
        self._object_held = active
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        return True

    def _move_grabbed_object(self, x: float, y: float, snap_deg: float) -> None:
        held = self._object_held
        if held is None:
            return
        transform = self.object_tool.drag(
            x, y, self._picker(), snap_deg, self._state.object_settings.uniform_scale
        )
        if transform is None:
            return
        self._state.preview_transform(held, transform)

    def _commit_object_drag(self) -> None:
        before, self._object_previous = self._object_previous, None
        held, self._object_held = self._object_held, None
        self.object_tool.end()
        self._refresh_cursor()
        if before is None or held is None:
            return
        verb = {"move": "Move", "rotate": "Turn", "scale": "Scale"}[self.object_tool.mode]
        self._state.commit_transform(held, before, f"{verb} {held.name}")

    def _pick_object(self, x: float, y: float) -> None:
        """Make the object under the cursor the active one."""
        hit = self._picker().hit(x, y)
        if hit is None:
            return
        owner = self._state.triangle_owner(hit.triangle)
        if owner is not None:
            self._state.set_active(owner)
            self.update()

    def _gesture_for(self, event) -> str | None:
        """The gesture a key press chooses, if the transform tool is armed to hear it."""
        if not self.object_tool.active or self.object_tool.dragging:
            return None
        if event.modifiers() != Qt.KeyboardModifier.NoModifier:
            return None
        return GESTURE_KEYS.get(Qt.Key(event.key()))

    # The line round a newly active object is drawn by the renderer, over
    # the finished frame; the view only says which object, and how far
    # along the fade the frame is.

    def _active_changed(self) -> None:
        """Put the line on the active object, if it is a different one than before."""
        active = self._state.active_object
        if active is self._active_seen:
            return
        self._active_seen = active
        # With one object there is nothing to tell it from; the line would
        # only say what loading a model already said.
        if active is not None and len(self._state.objects) > 1:
            self.highlight_object(active)

    def highlight_object(self, obj) -> None:
        """Draw a line round ``obj`` for a moment, then let it fade."""
        self._highlight = (obj, perf_counter())
        self._highlight_timer.start()
        self.update()

    def _highlight_now(self) -> tuple[int, float] | None:
        """Which part wears the line this frame, and how solid it is, or ``None``.

        Also where the fade is retired: the frame that finds it over stops
        the timer that was feeding the frames.
        """
        if self._highlight is None:
            return None
        obj, began = self._highlight
        elapsed = perf_counter() - began
        if elapsed >= HIGHLIGHT_HOLD + HIGHLIGHT_FADE or self._state.objects.index(obj) < 0:
            self._highlight = None
            self._highlight_timer.stop()
            return None
        alpha = 1.0 - max(elapsed - HIGHLIGHT_HOLD, 0.0) / HIGHLIGHT_FADE
        index = next(
            (i for i, (held, _, _) in enumerate(self._state.mesh_parts) if held is obj), -1
        )
        if index < 0:
            return None  # Hidden; the line waits for it to be shown again.
        return index, alpha

    # ------------------------------------------------------------------
    # Skeletons
    # ------------------------------------------------------------------
    #
    # A pull on a joint edits one attribute of one joint -- the parent's
    # rotation for a swing, the joint's own for a roll, its shift for a move
    # -- so the undo step is that attribute, exactly as a node drag is.  A
    # pull in fit mode rewrites the joint list instead, since the children's
    # rest transforms move with it.

    def _skeleton_index(self) -> int:
        """Which skeleton an edit lands in: the selected one, else the last."""
        chosen = self.pose_tool.selected
        if chosen is not None and 0 <= chosen[0] < len(self._state.skeletons):
            return chosen[0]
        return len(self._state.skeletons) - 1

    def _place_joint(self, x: float, y: float) -> None:
        """Add a joint where the click landed, under the selected joint."""
        settings = self._state.skeleton_settings
        point = self.pose_tool.pick(x, y, self._picker(), settings)
        if point is None:
            self.pick_failed.emit()
            return
        index = self._skeleton_index()
        skeleton = self._state.skeletons[index] if index >= 0 else Skeleton()
        chosen = self.pose_tool.selected
        parent = chosen[1] if chosen is not None and chosen[0] == index else -1
        joints = self.pose_tool.place(skeleton, point, parent)
        self.pose_tool.hover_point = point
        self.skeleton_edited.emit((index, joints, f"Add {joints[-1].name}"))
        landed = max(index, 0)
        self.pose_tool.selected = (landed, len(joints) - 1)
        self.joint_selected.emit((landed, len(joints) - 1))
        self.update()

    def _begin_joint_drag(self, x: float, y: float, twist: bool) -> bool:
        """Take hold of a joint -- or of a bone, by its far end."""
        tool = self.pose_tool
        settings = self._state.skeleton_settings
        picker = self._picker()
        found = tool.joint_at(x, y, self._state.skeletons, picker, settings) or tool.bone_at(
            x, y, self._state.skeletons, picker, settings
        )
        if found is None:
            return False
        index, position = found
        skeleton = self._state.skeletons[index]
        joint = skeleton.joints[position]
        parent = joint.parent
        if settings.fit and not skeleton.bound:
            target, field, previous = position, "joints", [replace(j) for j in skeleton.joints]
            mode = "fit"
        elif twist:
            target, field, previous, mode = position, "rotation", joint.rotation, "twist"
        elif 0 <= parent < len(skeleton.joints) and not skeleton.joints[parent].locked:
            target, field, previous = parent, "rotation", skeleton.joints[parent].rotation
            mode = "swing"
        else:
            target, field, previous, mode = position, "translation", joint.translation, "move"
        self._pose_previous = (index, target, field, previous, x)
        self._pose_anchor = skeleton.positions()[position].copy()
        self._pose_dragged = False
        tool.grabbed = found
        tool.mode = mode
        tool.selected = found
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        return True

    def _move_grabbed_joint(self, x: float, y: float) -> None:
        """Apply the pull live, so the figure moves under the cursor."""
        if self._pose_previous is None or self.pose_tool.grabbed is None:
            return
        index, target, field, previous, start_x = self._pose_previous
        skeleton = self._state.skeletons[index]
        held = self.pose_tool.grabbed[1]
        tool = self.pose_tool
        settings = self._state.skeleton_settings
        picker = self._picker()
        anchor = self._pose_anchor if self._pose_anchor is not None else skeleton.positions()[held]
        if tool.mode == "twist":
            # From where the joint started, by the whole travel so far, so
            # the roll cannot creep with the rounding of a hundred steps.
            skeleton.joints[target].rotation = previous
            turned = tool.twist(skeleton, target, x - start_x, settings)
            if turned is not None:
                skeleton.joints[target].rotation = turned
        elif tool.mode == "swing":
            swing = tool.swing(skeleton, held, tool.drag_target(x, y, picker, anchor))
            if swing is not None:
                skeleton.joints[swing.parent].rotation = swing.rotation
        elif tool.mode == "move":
            shift = tool.move(skeleton, held, tool.drag_target(x, y, picker, anchor))
            if shift is not None:
                skeleton.joints[held].translation = shift
        elif tool.mode == "fit":
            skeleton.joints = tool.fit(skeleton, held, tool.drag_target(x, y, picker, anchor))
        self._pose_dragged = True
        self._state.notify_skeleton(live=True)

    def _commit_joint_drag(self, was_click: bool = False) -> None:
        """Record the finished pull as one step, or read a press as a selection."""
        found = self.pose_tool.grabbed
        self.pose_tool.grabbed = None
        self.pose_tool.mode = ""
        self._pose_anchor = None
        self._refresh_cursor()
        if self._pose_previous is None:
            return
        index, target, field, previous, _ = self._pose_previous
        self._pose_previous = None
        dragged, self._pose_dragged = self._pose_dragged, False
        skeleton = self._state.skeletons[index]
        name = skeleton.joints[target].name if 0 <= target < len(skeleton.joints) else "joint"

        if field == "joints":
            changed = any(
                a.rest != b.rest for a, b in zip(skeleton.joints, previous, strict=False)
            ) or len(skeleton.joints) != len(previous)
            if changed:
                self._state.do(
                    SetAttributes(
                        skeleton,
                        {"joints": skeleton.joints},
                        text=f"Fit {name}",
                        channel=SKELETON,
                        previous={"joints": previous},
                    ),
                    apply=False,
                )
                return
        else:
            joint = skeleton.joints[target]
            if getattr(joint, field) != previous:
                verb = "Move" if field == "translation" else "Turn"
                self._state.do(
                    SetAttributes(
                        joint,
                        {field: getattr(joint, field)},
                        text=f"{verb} {joint.name}",
                        channel=SKELETON,
                        previous={field: previous},
                    ),
                    apply=False,
                )
                return
        if dragged:
            # Pulled and let go where it was: the live frames re-posed the
            # model, so the caches built on it are told to catch up.
            self._state.notify_skeleton()
        if was_click and found is not None:
            self.joint_selected.emit(found)
        self.update()

    def _update_pose_hover(self, x: float, y: float) -> bool:
        """Track the joint and bone under the cursor; True when either changed."""
        tool = self.pose_tool
        settings = self._state.skeleton_settings
        picker = self._picker()
        busy = (
            self.annotate_tool.active
            or self.form_tool.hover_landmark is not None
            or self.armature_tool.hover_landmark is not None
            or self.armature_tool.hover_handle is not None
        )
        joint = None if busy else tool.joint_at(x, y, self._state.skeletons, picker, settings)
        bone = (
            None
            if busy or joint is not None
            else tool.bone_at(x, y, self._state.skeletons, picker, settings)
        )
        changed = joint != tool.hover_joint or bone != tool.hover_bone
        if changed:
            tool.hover_joint = joint
            tool.hover_bone = bone
            self._refresh_cursor()
        return changed

    def _skeleton_moved(self) -> None:
        """A skeleton changed: redraw it."""
        self._stale_buried()
        self.update()

    # ------------------------------------------------------------------
    # Forms
    # ------------------------------------------------------------------
    #
    # A form is its landmarks and nothing else, so every edit here is a new
    # landmark list handed to the panel to record; the clay is worked out
    # again from the list whenever it changes.

    def _form_index(self) -> int:
        """Which form an edit lands in, counting a guided run as binding."""
        run = self.form_tool.guide
        if run is not None and 0 <= run.form < len(self._state.forms):
            return run.form
        chosen = self.form_tool.selected_landmark
        if chosen is not None and chosen[0] < len(self._state.forms):
            return chosen[0]
        return len(self._state.forms) - 1

    def _place_form_landmark(self, x: float, y: float) -> None:
        """Record the landmark a guided form is asking for."""
        index = self._form_index()
        if index < 0 or not self.form_tool.guiding:
            return
        form = self._state.forms[index]
        settings = self._state.form_settings
        free = self.form_tool.free_points(form, settings)
        point = self.form_tool.pick(x, y, self._picker(), settings, free)
        if point is None:
            self.pick_failed.emit()
            return
        self.form_tool.hover_point = point
        landmarks = self.form_tool.place(form, point, settings)
        if landmarks is None:
            return
        self.form_edited.emit((index, landmarks, "Place landmark"))
        self.update()

    def _begin_form_landmark_drag(self, x: float, y: float) -> bool:
        """Take hold of a form's landmark, to move it or just to say which one it is."""
        found = self.form_tool.landmark_at(
            x, y, self._state.forms, self._picker(), self._state.form_settings
        )
        if found is None:
            return False
        index, key = found
        form = self._state.forms[index]
        self._form_previous = (index, key, [replace(entry) for entry in form.landmarks])
        self.form_tool.grabbed_landmark = found
        self.form_tool.selected_landmark = found
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        return True

    def _move_grabbed_form_landmark(self, x: float, y: float) -> None:
        """Apply the drag live, so the clay re-forms under the cursor."""
        if self._form_previous is None:
            return
        index, key, _ = self._form_previous
        form = self._state.forms[index]
        landmark = form.landmark_for(key)
        if landmark is None:
            return
        settings = self._state.form_settings
        free = self.form_tool.free_points(form, settings)
        point = self.form_tool.drag_target(x, y, self._picker(), settings, landmark.point, free)
        form.landmarks = self.form_tool.derive(
            form, form.with_landmark_at(key, tuple(float(v) for v in point)), settings
        )
        self._state.notify_forms()

    def _commit_form_landmark_drag(self, was_click: bool = False) -> None:
        """Record the finished drag as one step, or read a press as a selection."""
        found = self.form_tool.grabbed_landmark
        self.form_tool.grabbed_landmark = None
        self._refresh_cursor()
        if self._form_previous is None:
            return
        index, key, previous = self._form_previous
        self._form_previous = None
        form = self._state.forms[index]
        before = next((entry for entry in previous if entry.key == key), None)
        after = form.landmark_for(key)
        if after is not None and (before is None or before.at != after.at):
            self._state.do(
                SetAttributes(
                    form,
                    {"landmarks": form.landmarks},
                    text=f"Move {form_landmark_title(form, key)}",
                    channel=FORMS,
                    previous={"landmarks": previous},
                ),
                apply=False,
            )
            return
        if was_click and found is not None:
            self.form_landmark_selected.emit(found)
        self.update()

    def _update_form_hover(self, x: float, y: float) -> bool:
        """Track the form landmark under the cursor; True when it changed."""
        tool = self.form_tool
        landmark = (
            None
            if self.annotate_tool.active
            else tool.landmark_at(
                x, y, self._state.forms, self._picker(), self._state.form_settings
            )
        )
        if landmark == tool.hover_landmark:
            return False
        tool.hover_landmark = landmark
        self._refresh_cursor()
        return True

    def _forms_moved(self) -> None:
        """A form changed: work its clay out again and redraw."""
        self._upload_forms()
        self.update()

    def _form_stages(self, form: PrimaryForm) -> list:
        """The solids of a form, worked out once per set of landmarks."""
        symmetric = self._state.form_settings.symmetric
        signature = (landmark_signature(form), symmetric)
        held = self._form_solids.get(id(form))
        if held is None or held[0] != signature:
            held = (signature, build_form(form, symmetric))
            self._form_solids[id(form)] = held
        return held[1]

    def _upload_forms(self) -> None:
        """Hand the renderer the clay of every visible form, or nothing."""
        if not self._ready:
            return
        settings = self._state.form_settings
        live = {id(form) for form in self._state.forms}
        for stale in [key for key in self._form_solids if key not in live]:
            del self._form_solids[stale]
        meshes = []
        if settings.show_all:
            for form in self._state.forms:
                if not form.visible:
                    continue
                mesh = stages_mesh(
                    shown_stages(form, self._form_stages(form)), settings.smooth, form.name
                )
                if mesh is not None:
                    meshes.append(mesh)
        self.makeCurrent()
        self._renderer.set_forms(merged(meshes) if meshes else None, settings.color)
        self.doneCurrent()

    def _place_measure_point(self, x: float, y: float) -> None:
        point = self.measure_tool.pick(x, y, self._picker(), self._state.measurement_settings)
        if point is None:
            self.pick_failed.emit()
            return
        self.measure_tool.hover_point = point
        measurement = self.measure_tool.click(point, self._state.measurements.next_name())
        if measurement is not None:
            self.measurement_created.emit(measurement)
        self.update()

    def center_on(self, measurement: Measurement) -> None:
        """Slide the view so a measurement sits at the centre, keeping the angle."""
        camera = self._state.camera
        offset = measurement.midpoint - camera.target
        camera.eye = camera.eye + offset
        camera.target = camera.target + offset
        self._state.notify_camera()
