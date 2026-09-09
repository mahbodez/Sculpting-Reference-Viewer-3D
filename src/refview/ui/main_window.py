"""Application window: viewport, docked panels, menus and shortcuts."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QAction, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QDockWidget,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QTabWidget,
)

from .. import APP_NAME
from ..core.annotation import AnnotateMode
from ..core.camera import Projection
from ..core.commands import AddItem
from ..core.history import MEASUREMENTS
from ..core.mesh import MeshLoadError
from ..core.mesh_io import MESH_FILTER, MESH_SUFFIXES
from ..core.session import SESSION_SUFFIX
from ..core.update_check import Release
from ..paths import model_dir
from ..render.texture import MatcapLoadError
from ..wakelock import WakeLock
from .panels.annotate_panel import AnnotatePanel
from .panels.camera_panel import STANDARD_VIEWS, CameraPanel
from .panels.matcap_panel import MatcapPanel
from .panels.measure_panel import MeasurePanel
from .panels.model_panel import ModelPanel
from .panels.planes_panel import PlanesPanel
from .panels.section_panel import SectionPanel
from .panels.shading_panel import ShadingPanel
from .state import ViewerState
from .update_notice import (
    UpdateChecker,
    is_skipped,
    show_failure_dialog,
    show_up_to_date_dialog,
    show_update_dialog,
)
from .viewport import Viewport
from .widgets import scrollable

CONTROLS_TEXT = """
<h3>Navigation</h3>
<table cellpadding='3'>
<tr><td><b>Left drag</b></td><td>Orbit around the point under the cursor</td></tr>
<tr><td><b>Right / middle drag</b></td><td>Pan</td></tr>
<tr><td><b>Wheel</b></td><td>Zoom towards the cursor</td></tr>
<tr><td><b>Alt + left drag</b></td><td>Orbit even while a tool is armed</td></tr>
<tr><td><b>Shift + left drag</b></td><td>Orbit in round steps (set the angle in Camera)</td></tr>
<tr><td><b>F</b></td><td>Frame the object</td></tr>
<tr><td><b>P</b></td><td>Toggle perspective / orthographic</td></tr>
<tr><td><b>1</b> ... <b>6</b></td><td>Front, back, left, right, top, bottom</td></tr>
</table>
<h3>Measuring</h3>
<table cellpadding='3'>
<tr><td><b>M</b></td><td>Arm the measuring tool</td></tr>
<tr><td><b>Left click</b></td><td>Place a point (dragging still orbits)</td></tr>
<tr><td><b>Padlock</b></td><td>Unlock a measurement to drag its endpoints</td></tr>
<tr><td><b>Esc</b></td><td>Cancel a half-finished measurement</td></tr>
</table>
<h3>Annotating</h3>
<table cellpadding='3'>
<tr><td><b>A</b></td><td>Arm the annotate tool</td></tr>
<tr><td><b>Left drag</b></td><td>Paint freehand, a line or a circle on the surface</td></tr>
<tr><td><b>E</b></td><td>Switch between the brush and the eraser</td></tr>
</table>
<h3>Cross-section</h3>
<table cellpadding='3'>
<tr><td><b>Ctrl+K</b></td><td>Cut the model with a plane</td></tr>
<tr><td><b>Section panel</b></td><td>Pick the plane, slide it, and keep the top,
the bottom or a slice</td></tr>
</table>
<h3>Saved views</h3>
<table cellpadding='3'>
<tr><td><b>Ctrl+B</b></td><td>Save the current camera</td></tr>
<tr><td><b>F2</b></td><td>Rename the selected view</td></tr>
<tr><td><b>[</b> / <b>]</b></td><td>Cycle through saved views</td></tr>
<tr><td><b>Ctrl+1</b> ... <b>Ctrl+9</b></td><td>Recall a saved view</td></tr>
</table>
<h3>Editing</h3>
<table cellpadding='3'>
<tr><td><b>Ctrl+Z</b> / <b>Ctrl+Shift+Z</b></td><td>Undo / redo</td></tr>
</table>
<p>Undo covers measurements, annotations and saved views.  Camera moves are
not recorded, so a hundred orbits never bury the edit you wanted back.</p>
<p>OBJ, STL, GLB and glTF models can be opened or dropped onto the window.
A glTF file states that its units are metres, so the measurement panel adopts
that automatically; OBJ and STL declare nothing and are left alone.</p>
<p>Formats also disagree about which axis points up, so a file can arrive lying
on its side.  The Model tab turns it upright: pick the up axis the file used,
flip it if it came in upside down, and spin it a quarter turn to face forwards.
Measurements and annotations turn with the model.</p>
<p>The Planes tab breaks the surface into the flat planes a form is blocked
in with, from a six-sided box down to a barely faceted surface.  Its detail
slider moves the size of a plane evenly, so it bites as hard at the coarse end
as at the fine end, and it can line every seam between two planes.  The
directions can come off a fixed grid, or be read out of the model's own
normals by PCA, in which case the slider is the fraction of those principal
directions to keep.  It works on the normals
rather than on the shading, so it applies whichever shading mode is set, and
the planes are worked out on the model, so they stay put as you orbit.</p>
<p>Single-key shortcuts act while the 3D view has focus, so they never
interfere with typing names into the panels.</p>
<p>While this window is the one in front, the screen is kept awake: a pose you
are working from should still be there when you look up from the clay.  Put
another window in front and the machine sleeps as usual.</p>
"""

_IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp")

#: How narrow the control dock may be pulled.  The panels no longer insist on
#: a width of their own -- see :func:`~refview.ui.widgets.relax_widths` -- so
#: this is the only thing left that decides, and it wants to be the smallest
#: number at which a row is still worth using: a caption, a groove long enough
#: to drag, and the box beside it.  A panel with a longer caption than that
#: scrolls the last few pixels rather than holding every other panel wide.
_DOCK_MIN_WIDTH = 300


class MainWindow(QMainWindow):
    """Wires the viewport, the panels and the document together."""

    #: Drawing mode the eraser toggle returns to.
    _previous_annotate_mode = AnnotateMode.FREEHAND

    def __init__(self, state: ViewerState | None = None) -> None:
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1440, 900)
        self.setAcceptDrops(True)

        self._state = state or ViewerState(self)
        self._session_path: Path | None = None
        #: Held while this window is the one in front: an artist reads a pose
        #: for minutes at a time without touching the machine.
        self._wake_lock = WakeLock()

        self._viewport = Viewport(self._state)
        self.setCentralWidget(self._viewport)

        self._model_panel = ModelPanel(self._state)
        self._matcap_panel = MatcapPanel(self._state)
        self._shading_panel = ShadingPanel(self._state)
        self._planes_panel = PlanesPanel(self._state)
        self._measure_panel = MeasurePanel(self._state)
        self._section_panel = SectionPanel(self._state)
        self._annotate_panel = AnnotatePanel(self._state)
        self._camera_panel = CameraPanel(self._state)

        self._build_dock()
        self._build_menus()
        self._build_viewport_shortcuts()
        self._connect()
        self._update_history_actions()

        self.statusBar().showMessage("Open a model with Ctrl+O, then press M to measure.")

        self._start_update_check(manual=False)

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def _build_dock(self) -> None:
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        # Every panel scrolls, because several are taller than the dock on a
        # laptop screen.  The matcap panel is the exception: it manages its own
        # scrolling so that its gallery can take the space the artist drags it.
        tabs.addTab(self._matcap_panel, "Matcap")
        for panel, title in (
            (self._model_panel, "Model"),
            (self._shading_panel, "Shading"),
            (self._planes_panel, "Planes"),
            (self._section_panel, "Section"),
            (self._measure_panel, "Measure"),
            (self._annotate_panel, "Annotate"),
            (self._camera_panel, "Camera"),
        ):
            tabs.addTab(scrollable(panel), title)

        dock = QDockWidget("Controls", self)
        dock.setObjectName("controls_dock")
        dock.setWidget(tabs)
        dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | Qt.DockWidgetArea.RightDockWidgetArea
        )
        dock.setMinimumWidth(_DOCK_MIN_WIDTH)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        self._dock = dock

    def _build_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        self._menu_action(file_menu, "&Open Model...", self._open_model, "Ctrl+O")
        self._menu_action(file_menu, "Load &Matcap...", self._matcap_panel.browse)
        file_menu.addSeparator()
        self._menu_action(file_menu, "&Save Session", self._save_session, "Ctrl+S")
        self._menu_action(file_menu, "Save Session &As...", self._save_session_as, "Ctrl+Shift+S")
        self._menu_action(file_menu, "&Load Session...", self._load_session)
        file_menu.addSeparator()
        self._menu_action(file_menu, "E&xit", self.close, "Ctrl+Q")

        edit_menu = self.menuBar().addMenu("&Edit")
        self._undo_action = self._menu_action(edit_menu, "&Undo", self._state.undo, "Ctrl+Z")
        self._redo_action = self._menu_action(edit_menu, "&Redo", self._state.redo, "Ctrl+Shift+Z")
        self._redo_alternate = QShortcut(QKeySequence("Ctrl+Y"), self)
        self._redo_alternate.activated.connect(self._state.redo)

        view_menu = self.menuBar().addMenu("&View")
        self._menu_action(view_menu, "&Frame Object  (F)", self._state.frame_object)
        self._menu_action(view_menu, "Toggle &Projection  (P)", self._toggle_projection)
        view_menu.addSeparator()
        for index, (label, direction) in enumerate(STANDARD_VIEWS, start=1):
            self._menu_action(
                view_menu,
                f"{label}  ({index})",
                lambda _=False, d=direction: self._camera_panel.look_along(d),
            )
        view_menu.addSeparator()
        self._section_action = self._menu_action(
            view_menu, "Cross-&section", self._toggle_section, "Ctrl+K", checkable=True
        )
        self._menu_action(
            view_menu, "Section Plane From &View", self._section_panel.set_plane_from_view
        )
        view_menu.addSeparator()
        view_menu.addAction(self._dock.toggleViewAction())

        measure_menu = self.menuBar().addMenu("&Measure")
        self._measure_action = self._menu_action(
            measure_menu, "&Measure Tool  (M)", self._toggle_measure, checkable=True
        )
        self._menu_action(measure_menu, "&Cancel Current  (Esc)", self._viewport.cancel_tools)
        self._menu_action(measure_menu, "Clear &All", self._measure_panel.clear_all)

        annotate_menu = self.menuBar().addMenu("&Annotate")
        self._annotate_action = self._menu_action(
            annotate_menu, "&Annotate Tool  (A)", self._toggle_annotate, checkable=True
        )
        annotate_menu.addSeparator()
        for mode in AnnotateMode:
            self._menu_action(
                annotate_menu, mode.label, lambda _=False, m=mode: self._set_annotate_mode(m)
            )
        annotate_menu.addSeparator()
        self._menu_action(annotate_menu, "Clear A&ll", self._annotate_panel.clear_all)

        camera_menu = self.menuBar().addMenu("&Camera")
        self._menu_action(
            camera_menu, "&Save Current View", self._camera_panel.save_current_view, "Ctrl+B"
        )
        self._menu_action(
            camera_menu, "&Rename Selected View  (F2)", self._camera_panel.rename_selected
        )
        self._menu_action(camera_menu, "&Next Saved View  (])", lambda: self._camera_panel.cycle(1))
        self._menu_action(
            camera_menu, "&Previous Saved View  ([)", lambda: self._camera_panel.cycle(-1)
        )
        camera_menu.addSeparator()
        for slot in range(1, 10):
            self._menu_action(
                camera_menu,
                f"Recall View {slot}",
                lambda _=False, index=slot - 1: self._camera_panel.recall(index),
                f"Ctrl+{slot}",
            )

        help_menu = self.menuBar().addMenu("&Help")
        self._menu_action(help_menu, "&Controls", self._show_controls, "F1")
        self._menu_action(help_menu, "Check for &Updates...", self._check_for_updates)

    def _menu_action(self, menu, text, slot, shortcut=None, checkable: bool = False) -> QAction:
        """Add a menu entry, optionally with a window-wide shortcut."""
        action = QAction(text, self)
        action.setCheckable(checkable)
        if shortcut is not None:
            action.setShortcut(QKeySequence(shortcut))
        action.triggered.connect(slot)
        menu.addAction(action)
        return action

    def _build_viewport_shortcuts(self) -> None:
        """Single-key shortcuts, scoped so they never eat text input.

        They only fire while the 3D view has focus, which keeps keys like ``1``
        available for renaming measurements and typing unit labels.
        """
        bindings: list[tuple[str, object]] = [
            ("F", self._state.frame_object),
            ("P", self._toggle_projection),
            ("M", self._toggle_measure),
            ("A", self._toggle_annotate),
            ("E", self._toggle_eraser),
            ("Esc", self._viewport.cancel_tools),
            ("[", lambda: self._camera_panel.cycle(-1)),
            ("]", lambda: self._camera_panel.cycle(1)),
        ]
        for index, (_, direction) in enumerate(STANDARD_VIEWS, start=1):
            bindings.append((str(index), lambda d=direction: self._camera_panel.look_along(d)))

        self._shortcuts = []
        for key, slot in bindings:
            shortcut = QShortcut(QKeySequence(key), self._viewport)
            shortcut.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)
            shortcut.activated.connect(slot)
            self._shortcuts.append(shortcut)

    def _connect(self) -> None:
        self._state.status_message.connect(self.statusBar().showMessage)
        self._state.measurements_changed.connect(self._measure_panel.refresh_list)
        self._state.annotations_changed.connect(self._annotate_panel.refresh_list)
        self._state.bookmarks_changed.connect(self._camera_panel.refresh_bookmarks)
        self._state.render_changed.connect(self._shading_panel.update_enabled)
        self._state.render_changed.connect(self._planes_panel.update_enabled)
        self._state.film_changed.connect(self._planes_panel.film_changed)
        self._state.recording_changed.connect(self._planes_panel.recording_changed)
        self._state.camera_changed.connect(self._camera_panel.refresh_camera)
        self._state.history_changed.connect(self._update_history_actions)
        self._state.render_changed.connect(self._sync_section_action)
        self._state.mesh_changed.connect(self._model_panel.refresh)

        self._viewport.measurement_created.connect(self._on_measurement_created)
        self._viewport.pick_failed.connect(
            lambda: self.statusBar().showMessage("No surface under the cursor", 2000)
        )
        self._measure_panel.measure_toggled.connect(self._set_measuring)
        self._measure_panel.center_requested.connect(self._viewport.center_on)
        self._annotate_panel.annotate_toggled.connect(self._set_annotating)

    # ------------------------------------------------------------------
    # Public surface
    # ------------------------------------------------------------------

    @property
    def state(self) -> ViewerState:
        """The document this window edits."""
        return self._state

    def load_matcap(self, path: str | Path | None) -> None:
        """Apply a matcap image, reporting unreadable files to the user."""
        try:
            self._state.load_matcap(path)
        except MatcapLoadError as error:
            QMessageBox.warning(self, "Matcap", str(error))
            return
        self._matcap_panel.refresh()

    # ------------------------------------------------------------------
    # Reactions
    # ------------------------------------------------------------------

    def _on_measurement_created(self, measurement) -> None:
        self._state.do(
            AddItem(
                self._state.measurements.items,
                measurement,
                text=f"Add {measurement.name}",
                channel=MEASUREMENTS,
            )
        )
        settings = self._state.measurement_settings
        self.statusBar().showMessage(
            f"{measurement.name}: {settings.format_length(measurement.length)}", 5000
        )

    def _sync_section_action(self) -> None:
        """Keep the menu entry agreeing with the panel's own checkbox."""
        self._section_action.setChecked(self._state.render.section.enabled)

    def _update_history_actions(self) -> None:
        history = self._state.history
        self._undo_action.setEnabled(history.can_undo)
        self._redo_action.setEnabled(history.can_redo)
        self._undo_action.setText(f"&Undo {history.undo_text}".rstrip())
        self._redo_action.setText(f"&Redo {history.redo_text}".rstrip())

    # -- tools ----------------------------------------------------------

    def _set_measuring(self, active: bool) -> None:
        self._viewport.set_measure_active(active)
        self._measure_panel.set_measuring(active)
        self._measure_action.setChecked(active)
        if active:
            self._sync_annotating(False)

    def _set_annotating(self, active: bool) -> None:
        self._viewport.set_annotate_active(active)
        self._sync_annotating(active)
        if active:
            self._measure_panel.set_measuring(False)
            self._measure_action.setChecked(False)

    def _sync_annotating(self, active: bool) -> None:
        """Keep the panel button and the menu entry agreeing with the tool."""
        self._annotate_panel.set_annotating(active)
        self._annotate_action.setChecked(active)

    def _toggle_measure(self) -> None:
        self._set_measuring(not self._viewport.measure_tool.active)

    def _toggle_annotate(self) -> None:
        self._set_annotating(not self._viewport.annotate_tool.active)

    def _toggle_eraser(self) -> None:
        """Swap between the eraser and the drawing mode it was called from."""
        settings = self._state.annotation_settings
        self._set_annotate_mode(
            self._previous_annotate_mode if settings.mode.is_eraser else AnnotateMode.ERASE
        )

    def _set_annotate_mode(self, mode: AnnotateMode) -> None:
        settings = self._state.annotation_settings
        if not settings.mode.is_eraser:
            self._previous_annotate_mode = settings.mode
        settings.mode = mode
        self._state.notify_annotations()
        self._annotate_panel.refresh()
        if not self._viewport.annotate_tool.active:
            self._set_annotating(True)
        self.statusBar().showMessage(mode.label, 2000)

    def _toggle_section(self) -> None:
        self._section_panel.toggle()
        section = self._state.render.section
        self._section_action.setChecked(section.enabled)
        self.statusBar().showMessage(
            f"Cross-section {'on' if section.enabled else 'off'}: {section.mode.label.lower()}",
            2000,
        )

    def _toggle_projection(self) -> None:
        camera = self._state.camera
        camera.projection = (
            Projection.ORTHOGRAPHIC
            if camera.projection is Projection.PERSPECTIVE
            else Projection.PERSPECTIVE
        )
        self._state.notify_camera()
        self.statusBar().showMessage(camera.projection.label, 2000)

    def _show_controls(self) -> None:
        QMessageBox.information(self, "Controls", CONTROLS_TEXT)

    # ------------------------------------------------------------------
    # Updates
    # ------------------------------------------------------------------

    def _start_update_check(self, manual: bool) -> None:
        """Ask GitHub for the newest release in the background.

        The startup check is quiet: it only speaks up for a version the artist
        has not already skipped, and says nothing at all when the machine is
        offline.  Asking from the Help menu always reports what happened.
        """
        checker = UpdateChecker(self)
        checker.update_available.connect(
            lambda release: self._on_update_available(release, manual)
        )
        checker.up_to_date.connect(lambda: self._on_up_to_date(manual))
        checker.check_failed.connect(lambda error: self._on_update_check_failed(error, manual))
        self._update_checker = checker
        if manual:
            self.statusBar().showMessage("Checking for updates...", 4000)
        checker.start()

    def _check_for_updates(self) -> None:
        self._start_update_check(manual=True)

    def _on_update_available(self, release: Release, manual: bool) -> None:
        if not manual and is_skipped(release):
            return
        self.statusBar().showMessage(f"Version {release.version} is available", 8000)
        show_update_dialog(self, release)

    def _on_up_to_date(self, manual: bool) -> None:
        if manual:
            show_up_to_date_dialog(self)

    def _on_update_check_failed(self, error: str, manual: bool) -> None:
        if manual:
            show_failure_dialog(self, error)

    # ------------------------------------------------------------------
    # File handling
    # ------------------------------------------------------------------

    def open_model(self, path: str | Path) -> None:
        """Load a model, reporting failures without tearing down the window."""
        try:
            self._state.load_mesh(path)
        except (MeshLoadError, OSError) as error:
            QMessageBox.critical(self, "Open Model", str(error))
            return
        self._session_path = self._state.default_session_path()
        self.setWindowTitle(f"{APP_NAME} - {Path(path).name}")
        self._refresh_panels()

    def _open_model(self) -> None:
        start = model_dir()
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Model",
            str(start if start.is_dir() else Path.home()),
            MESH_FILTER,
        )
        if path:
            self.open_model(path)

    def _save_session(self) -> None:
        target = self._session_path or self._state.default_session_path()
        if target is None:
            self._save_session_as()
            return
        self._state.save_session(target)
        self._session_path = Path(target)

    def _save_session_as(self) -> None:
        suggestion = self._session_path or self._state.default_session_path()
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Session",
            str(suggestion or Path.home() / f"untitled{SESSION_SUFFIX}"),
            f"Reference Viewer session (*{SESSION_SUFFIX});;JSON (*.json)",
        )
        if path:
            self._state.save_session(path)
            self._session_path = Path(path)

    def _load_session(self) -> None:
        suggestion = self._session_path or self._state.default_session_path()
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Session",
            str(suggestion.parent if suggestion else Path.home()),
            f"Reference Viewer session (*{SESSION_SUFFIX});;JSON (*.json)",
        )
        if path:
            self.load_session(path)

    def load_session(self, path: str | Path) -> None:
        try:
            self._state.load_session(path)
        except (OSError, ValueError, MeshLoadError) as error:
            QMessageBox.critical(self, "Load Session", str(error))
            return
        self._session_path = Path(path)
        self._refresh_panels()

    def _refresh_panels(self) -> None:
        for panel in (
            self._model_panel,
            self._matcap_panel,
            self._shading_panel,
            self._planes_panel,
            self._measure_panel,
            self._annotate_panel,
            self._section_panel,
            self._camera_panel,
        ):
            panel.refresh()

    # ------------------------------------------------------------------
    # Window state
    # ------------------------------------------------------------------

    def changeEvent(self, event) -> None:  # noqa: N802 - Qt naming
        """Follow the machine's sleep to whether this window is in front."""
        super().changeEvent(event)
        if event.type() == QEvent.Type.ActivationChange:
            self._wake_lock.set_held(self.isActiveWindow())

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt naming
        self._wake_lock.release()
        # A recording still running when the interpreter tears its modules
        # down is a crash on the way out, so the window does not leave
        # without it.  It is asked to stop first, so the wait is one stage.
        self._viewport.stop_recording()
        super().closeEvent(event)

    # ------------------------------------------------------------------
    # Drag and drop
    # ------------------------------------------------------------------

    def dragEnterEvent(self, event) -> None:  # noqa: N802 - Qt naming
        if any(self._droppable(url) for url in event.mimeData().urls()):
            event.acceptProposedAction()

    def dropEvent(self, event) -> None:  # noqa: N802 - Qt naming
        for url in event.mimeData().urls():
            path = Path(url.toLocalFile())
            suffix = path.suffix.lower()
            if suffix in MESH_SUFFIXES:
                self.open_model(path)
            elif suffix == ".json":
                self.load_session(path)
            elif suffix in _IMAGE_SUFFIXES:
                self._state.load_matcap(path)
                self._matcap_panel.refresh()
            else:
                continue
            event.acceptProposedAction()
            return

    @staticmethod
    def _droppable(url) -> bool:
        path = Path(url.toLocalFile())
        return path.suffix.lower() in (*MESH_SUFFIXES, ".json", *_IMAGE_SUFFIXES)
