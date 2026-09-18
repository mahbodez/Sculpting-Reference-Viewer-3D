"""Application window: viewport, docked panels, menus and shortcuts."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QEvent, QPoint, QSettings, QTimer
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
)

from .. import APP_NAME
from ..core.annotation import AnnotateMode
from ..core.camera import Projection
from ..core.commands import AddItem
from ..core.history import MEASUREMENTS
from ..core.mesh import Mesh, MeshLoadError
from ..core.mesh_io import MESH_FILTER, MESH_SUFFIXES
from ..core.mesh_io import load_mesh as read_mesh
from ..core.rigging import humanoid_roles, looks_humanoid
from ..core.session import SESSION_SUFFIX, Session
from ..core.update_check import Release
from ..paths import model_dir
from ..render.texture import MatcapLoadError
from ..wakelock import WakeLock
from .elements.clone import carried, in_flight
from .elements.keys import COMMAND_PROPERTY, KeyGesture
from .elements.naming import lookup, slug
from .film_export import ExportVideoDialog
from .help_window import ControlsWindow
from .hotkeys import HotkeyBinder, ask_for
from .hotkeys import store as hotkey_store
from .panels.annotate_panel import AnnotatePanel
from .panels.armature_panel import ArmaturePanel
from .panels.camera_panel import STANDARD_VIEWS, CameraPanel
from .panels.forms_panel import FormsPanel
from .panels.measure_panel import MeasurePanel
from .panels.model_panel import ModelPanel
from .panels.planes_panel import PlanesPanel
from .panels.pose_panel import PosePanel
from .panels.section_panel import SectionPanel
from .panels.shading_panel import ShadingPanel
from .preferences import LAST_MODEL, LAST_SESSION
from .preferences import store as preference_store
from .settings_window import GROUPS, SettingsWindow
from .state import ViewerState, same_file
from .tasks import TaskBanner
from .update_notice import (
    UpdateChecker,
    is_skipped,
    show_failure_dialog,
    show_up_to_date_dialog,
    show_update_dialog,
)
from .viewport import Viewport
from .workspace import Workspace

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
<tr><td><b>Shading panel</b></td><td>Ghost the model to see through it</td></tr>
<tr><td><b>1</b> ... <b>6</b></td><td>Front, back, left, right, top, bottom</td></tr>
</table>
<h3>Objects</h3>
<table cellpadding='3'>
<tr><td><b>Ctrl+Shift+O</b></td><td>Add another model to the scene, at the origin</td></tr>
<tr><td><b>T</b></td><td>Arm the transform tool on the active object</td></tr>
<tr><td><b>Drag an arm</b></td><td>Move, turn or scale along that axis (the panel says
which)</td></tr>
<tr><td><b>Drag the ring</b></td><td>Move across the view, turn about it, or scale the
whole</td></tr>
<tr><td><b>Shift + drag</b></td><td>Turn in round steps</td></tr>
<tr><td><b>Click an object</b></td><td>Make it the active one (tool armed)</td></tr>
<tr><td><b>Model panel</b></td><td>Rename, show, ghost, link, merge and split objects</td></tr>
</table>
<h3>Measuring</h3>
<table cellpadding='3'>
<tr><td><b>M</b></td><td>Arm the measuring tool</td></tr>
<tr><td><b>Left click</b></td><td>Place a point (dragging still orbits)</td></tr>
<tr><td><b>Padlock</b></td><td>Unlock a measurement to drag its endpoints</td></tr>
<tr><td><b>Ctrl/Cmd-drag endpoint</b></td><td>Move in depth; Esc restores the start</td></tr>
<tr><td><b>Esc</b></td><td>Cancel a half-finished measurement</td></tr>
</table>
<h3>Annotating</h3>
<table cellpadding='3'>
<tr><td><b>A</b></td><td>Arm the annotate tool</td></tr>
<tr><td><b>Left drag</b></td><td>Paint freehand, a line or a circle on the surface</td></tr>
<tr><td><b>E</b></td><td>Switch between the brush and the eraser</td></tr>
</table>
<h3>Armature</h3>
<table cellpadding='3'>
<tr><td><b>R</b></td><td>Arm the armature tool</td></tr>
<tr><td><b>Click a node</b></td><td>Select it — in or out of armature mode</td></tr>
<tr><td><b>Click a second node</b></td><td>Join the two with a bone (armed)</td></tr>
<tr><td><b>Ctrl + click a node</b></td><td>Join it to the selected one, always</td></tr>
<tr><td><b>Click a bone</b></td><td>Insert a node into it, splitting it in two</td></tr>
<tr><td><b>Left click elsewhere</b></td><td>Place a node, joined to the last one</td></tr>
<tr><td><b>Left drag a node</b></td><td>Move it (dragging elsewhere still orbits)</td></tr>
<tr><td><b>Shift + drag a node</b></td><td>Change how thick the form is there</td></tr>
<tr><td><b>Left drag a landmark</b></td><td>Move the cross; the wire follows it</td></tr>
<tr><td><b>Double-click a row</b></td><td>Rename a node or an armature</td></tr>
<tr><td><b>Esc</b></td><td>Drop the chain without disarming the tool</td></tr>
</table>
<h3>Forms</h3>
<table cellpadding='3'>
<tr><td><b>G</b></td><td>Arm the forms tool</td></tr>
<tr><td><b>Forms panel</b></td><td>Pick a form -- pelvis, ribcage, head, or a freeform --
and press Start</td></tr>
<tr><td><b>Left click</b></td><td>Place the landmark being asked for, or the one you named</td></tr>
<tr><td><b>Landmark / Side</b></td><td>Name a freeform's next landmark and say which side
it is on</td></tr>
<tr><td><b>Fill</b></td><td>A freeform's clay as flat planes, or bowed out between the
points</td></tr>
<tr><td><b>Ctrl/Cmd-drag marker</b></td><td>Up moves deeper; down moves toward the camera</td></tr>
<tr><td><b>Left drag a landmark</b></td><td>Move it; the clay follows</td></tr>
<tr><td><b>Double-click a row</b></td><td>Rename a form, or a freeform's landmark</td></tr>
<tr><td><b>Append</b></td><td>Take up the selected freeform again and add landmarks to it</td></tr>
<tr><td><b>Stage slider</b></td><td>Scrub back through the stages of a head</td></tr>
<tr><td><b>Symmetrical forms</b></td><td>Build the clay from the landmarks made symmetric</td></tr>
<tr><td><b>Panel switch</b></td><td>Show or hide what a panel puts on the model, from the
panel's bar or from its tab</td></tr>
</table>
<h3>Panels</h3>
<table cellpadding='3'>
<tr><td><b>Drag a panel's bar</b></td><td>Move it to any edge, stack it with another,
or float it off</td></tr>
<tr><td><b>Alt + drag a control</b></td><td>Take a working copy of it away on the
cursor</td></tr>
<tr><td><b>Alt + drag a group's bar</b></td><td>Take a copy of the whole group</td></tr>
<tr><td><b>Ctrl+Shift+N</b></td><td>Open an empty panel of your own to drop copies
into</td></tr>
<tr><td><b>Alt + drag a copy</b></td><td>Move it; drop it on the model to throw it
away</td></tr>
<tr><td><b>Right-click a custom panel</b></td><td>Add or rename a group, rename the
panel</td></tr>
<tr><td><b>Click a group's name</b></td><td>Fold the group away</td></tr>
<tr><td><b>Panels &gt; Reset Layout</b></td><td>Put every panel back where it
started</td></tr>
</table>
<h3>Matcap</h3>
<table cellpadding='3'>
<tr><td><b>Drag the sphere</b></td><td>Turn the matcap; it follows your hand
round</td></tr>
<tr><td><b>Shift + drag</b></td><td>Brightness across, contrast up and down</td></tr>
<tr><td><b>Ctrl + drag</b></td><td>Saturation across, gamma up and down</td></tr>
<tr><td><b>Wheel</b></td><td>Turn it in steps of five degrees, or one with Ctrl</td></tr>
<tr><td><b>Double-click</b></td><td>Put the grading back</td></tr>
<tr><td><b>Fine Adjustments</b></td><td>The same five numbers, to type into</td></tr>
</table>
<h3>Preferences</h3>
<table cellpadding='3'>
<tr><td><b>Ctrl+,</b></td><td>Open the preferences</td></tr>
<tr><td><b>Settings menu</b></td><td>Or straight to one group of them</td></tr>
</table>
<h3>Hotkeys</h3>
<table cellpadding='3'>
<tr><td><b>Ctrl/Cmd + Alt/Option + click</b></td><td>Put a key on any button or
switch in a panel: press the key you want, and it is kept</td></tr>
<tr><td><b>Settings &gt; Hotkeys</b></td><td>Every menu entry and every letter the
view answers to, each with a box to press a new key into; and the buttons you
have put keys on</td></tr>
<tr><td><b>A key that is taken</b></td><td>You are told what it does now, and asked
before it is moved</td></tr>
<tr><td><b>Tooltips</b></td><td>A control with a key on it says so in its tooltip</td></tr>
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
<h3>The making of a form</h3>
<table cellpadding='3'>
<tr><td><b>Planes tab</b></td><td>Record the making, and scrub through it</td></tr>
<tr><td><b>Ctrl+E</b></td><td>Export the making as a video</td></tr>
</table>
<h3>Pose</h3>
<table cellpadding='3'>
<tr><td><b>B</b></td><td>Arm the pose tool</td></tr>
<tr><td><b>Click a joint</b></td><td>Select it — in or out of pose mode</td></tr>
<tr><td><b>Left drag a joint</b></td><td>Swing the bone above it, carrying everything
below</td></tr>
<tr><td><b>Left drag a root</b></td><td>Move the whole figure</td></tr>
<tr><td><b>Left drag a bone</b></td><td>The same as dragging the joint at its far
end</td></tr>
<tr><td><b>Shift + drag a joint</b></td><td>Roll it about its own bone</td></tr>
<tr><td><b>Ctrl/Cmd-drag a joint</b></td><td>Pull it in depth</td></tr>
<tr><td><b>Left click elsewhere</b></td><td>Add a joint under the selected one
(armed)</td></tr>
<tr><td><b>Fit</b></td><td>Dragging a joint moves where it rests; its children stay
put</td></tr>
<tr><td><b>Simplify</b></td><td>Take the fingers, face, breasts and helper bones out of
a rig</td></tr>
<tr><td><b>Double-click a row</b></td><td>Rename a joint or a skeleton</td></tr>
<tr><td><b>Esc</b></td><td>Drop a pull without disarming the tool</td></tr>
</table>
<h3>Editing</h3>
<table cellpadding='3'>
<tr><td><b>Ctrl+Z</b> / <b>Ctrl+Shift+Z</b></td><td>Undo / redo</td></tr>
</table>
<p>Undo covers measurements, annotations, the armature, the forms, the
skeletons and saved views.
Camera moves are not recorded, so a hundred orbits never bury the edit you
wanted back.</p>
<p>The Armature tab lays a wire under the model: a graph of named nodes, each
carrying how thick the form is where it sits.  Nothing is animated by it -- it
is there to be read off while you bend real wire, and to tell the clay modes
where the masses of a figure are.  You can place the nodes by eye, or walk a
guided preset instead, which asks for anatomical landmarks you can actually
find on the model -- the C7 bump, the two hip points, the epicondyles either
side of a knee -- and works the joints out from them.  The pairs pay twice: the
distance between two epicondyles locates the elbow and also says how wide it
is.  Place the midline and one side and the other is mirrored across the plane
fitted through the midline, which is eighteen placements rather than
thirty-one.  The landmarks are kept afterwards and listed in the panel with
their positions; nudge one, by dragging its cross in the view or typing into
the panel, and the nodes that read it move with it.  That holds until you move
a node by hand and take the armature over yourself -- after which the list
stays editable and <i>Rebuild Nodes</i> hands the wire back to the preset.  A
cross sits closer to hand than the node beside it, so aiming at one picks the
landmark; a few pixels out picks the node.</p>
<p>The Forms tab builds the big simple masses a figure is blocked in with, in
clay, over the model: the pelvis as a bucket with its front corner chipped off
along the plane from the hip points to the pubic symphysis, the ribcage as an
egg with the thoracic arch chipped out of its front, and the head as a wedge
that is then given its width, the block of its cranium and its jaw.  Each is a
guided walk like the armature's: pick the form, press Start, and point at the
landmarks it asks for -- the crests of the hips, the notch at the top of the
breastbone, the widest point of the skull -- and the form is worked out from
them, growing as they go down.  The head arrives in stages, every stage is
kept, and the slider scrubs back through them.  The landmarks stay editable
afterwards; ghost the model to read the clay standing inside it.</p>
<p>The Pose tab is a skeleton in the sense a rigging application means it:
every joint but the root hangs from a parent, turning a joint carries
everything below it, and a model that came with skin weights follows the
bones.  A rigged GLB or glTF brings its skeleton in with it, bound to the
skin, and if its joints are named the way Mixamo, Biped, Unreal, Rigify or
Character Creator name them you are offered a mapping onto the humanoid
roles the Armature tab uses, and <i>Simplify</i> takes the fingers, the face,
the breasts and the twist and helper bones out of it, leaving the figure a
pose is read from.  Posing is by pulling: drag a joint and the bone
above it swings to follow, as a bone is turned in 3ds Max; drag a root and
the figure moves; Shift rolls a joint about its own bone.  A skeleton can also
be built by clicking, stood up from the Humanoid preset and pulled into the
model in Fit mode, or grown out of an armature -- the guided humanoid comes
across whole, and a freehand wire is grown from the node you have selected,
dropping any bone that would close a loop.  The other way round, any
skeleton lays an armature under itself as it is posed.  A skeleton's pose is
kept in the session; its skin weights are the model's and are read back out
of the model file.</p>
<p>OBJ, STL, GLB and glTF models can be opened or dropped onto the window.
A glTF file states that its units are metres, so the measurement panel adopts
that automatically; OBJ and STL declare nothing and are left alone.  A glTF
with a skin arrives posable.</p>
<p>Formats also disagree about which axis points up, so a file can arrive lying
on its side.  The Model tab turns it upright: pick the up axis the file used,
flip it if it came in upside down, and spin it a quarter turn to face forwards.
Measurements, annotations, the armature and the skeletons turn with the
model.</p>
<p>The Planes tab breaks the surface into the flat planes a form is blocked
in with, from a six-sided box down to a barely faceted surface.  Its detail
slider moves the size of a plane evenly, so it bites as hard at the coarse end
as at the fine end, and it can line every seam between two planes.  The
directions can come off a fixed grid, or be read out of the model's own
normals by PCA, in which case the slider is the fraction of those principal
directions to keep.  It works on the normals
rather than on the shading, so it applies whichever shading mode is set, and
the planes are worked out on the model, so they stay put as you orbit.</p>
<p>Every panel is its own dock and goes wherever you put it.  Dragged to the
top or the bottom of the window a panel has width rather than height, so its
groups break into columns to use it -- nothing about the panel changes, only
how much room it was given.</p>
<p>A control can be copied out of the panel it lives in: hold Alt, drag it,
and drop it into a panel of your own.  The copy is a second pair of hands on
the same control, not a second setting -- move either and both move, because
there is only one of them.  That is for the handful of controls a particular
piece of work keeps reaching for, which are almost never the handful that
share a panel.  Drop a copy on the model to be rid of it.  Where the panels
are, and any you have built, are remembered between runs and saved into the
session file alongside the marks on the model.</p>
<p>The sphere under the matcap gallery is the matcap, graded exactly as the
renderer will grade it, and it is also the control: drag it and it turns under
your hand, drag it with Shift or Ctrl and the light or the colour changes.
Nobody has ever wanted a gamma of 1.2; they have wanted the shadows to come up
a little, and this is that, done by looking.  The five numbers are still there,
folded away underneath, for typing an exact rotation into -- or for copying one
of them out into a panel of your own.</p>
<p>What you prefer is kept apart from what the model says.  Anything about the
piece of work -- the matcap on it, where it is cut, how the planes are fitted
-- travels in the session file, because handing somebody the session should
hand them the view you were talking about.  Anything about you -- how fast the
orbit turns under your hand, how large the type is, which orange the interface
uses, where your own matcaps are kept, whether opening the application puts
you back in front of whatever you were last looking at -- stays on this
machine and follows you from one model to the next.  Settings &gt; Preferences,
and every change applies
as you make it.</p>
<p>Single-key shortcuts act while the 3D view has focus, so they never
interfere with typing names into the panels.</p>
<p>While this window is the one in front, the screen is kept awake: a pose you
are working from should still be there when you look up from the clay.  Put
another window in front and the machine sleeps as usual.  A laptop on a train
is a different proposition, so that can be switched off in the preferences
along with the splash screen and the check for new releases.</p>
"""

_IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp")


def opens_as(path: str | Path) -> str | None:
    """What a file would open as -- ``"model"``, ``"session"`` or ``"matcap"`` -- by its suffix."""
    suffix = Path(path).suffix.lower()
    if suffix in MESH_SUFFIXES:
        return "model"
    if suffix == ".json":
        return "session"
    if suffix in _IMAGE_SUFFIXES:
        return "matcap"
    return None


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
        #: The controls reference, once it has been opened; kept so that it
        #: comes back where it was left rather than being built again.
        self._controls: ControlsWindow | None = None
        #: The preferences window, likewise.
        self._settings: SettingsWindow | None = None
        #: What the artist prefers, as against what the document says.  Loaded
        #: off the machine the first time anything asks; see
        #: :mod:`refview.ui.preferences`.
        self._preferences = preference_store()
        #: The matcap folder as last applied, so that changing some other
        #: preference does not send the gallery back to the disk.
        self._matcap_folder = self._preferences.value.folders.matcaps
        #: Held while this window is the one in front: an artist reads a pose
        #: for minutes at a time without touching the machine.
        self._wake_lock = WakeLock()

        self._viewport = Viewport(self._state)
        self.setCentralWidget(self._viewport)
        #: The cards for whatever is running -- a file being read, a figure
        #: being skinned, a form being cut -- floated over the foot of the
        #: view; see :mod:`refview.ui.tasks`.
        self._banner = TaskBanner(self._state.tasks, self)
        self._banner.changed.connect(self._place_banner)
        self._viewport.installEventFilter(self)
        #: The check for updates being shown as a task, when it is.
        self._update_task = None
        #: Which keys do what, as the artist has set them; see
        #: :mod:`refview.ui.hotkeys`.  The binder turns the store into this
        #: window's shortcuts and re-keys them whenever the store moves.
        self._hotkeys = hotkey_store()
        self._binder = HotkeyBinder(self, self._viewport, self._hotkeys)

        self._model_panel = ModelPanel(self._state)
        self._shading_panel = ShadingPanel(self._state)
        self._matcap_panel = self._shading_panel.matcap_panel
        self._planes_panel = PlanesPanel(self._state)
        self._measure_panel = MeasurePanel(self._state)
        self._section_panel = SectionPanel(self._state)
        self._annotate_panel = AnnotatePanel(self._state)
        self._armature_panel = ArmaturePanel(self._state)
        self._forms_panel = FormsPanel(self._state)
        self._pose_panel = PosePanel(self._state)
        self._camera_panel = CameraPanel(self._state)

        self._workspace = Workspace(self)
        # The layout is written down a moment after it stops changing rather
        # than on the way out, so that a panel built over an afternoon is not
        # lost to a crash.  A moment, because dragging a dock across the window
        # changes it continuously and none of the states it passes through is
        # worth a write.
        self._layout_write = QTimer(self)
        self._layout_write.setSingleShot(True)
        self._layout_write.setInterval(1500)
        self._layout_write.timeout.connect(self._save_layout)
        self._workspace.changed.connect(self._layout_write.start)

        self._build_docks()
        self._build_menus()
        self._build_viewport_shortcuts()
        self._speak_for_commands()
        self._binder.rebind()
        KeyGesture.instance().requested.connect(self._assign_hotkey)
        self._connect()
        self._update_history_actions()
        self._restore_layout()
        self._apply_preferences()
        self._preferences.changed.connect(self._apply_preferences)

        self.statusBar().showMessage("Open a model with Ctrl+O, then press M to measure.")

        if self._preferences.value.startup.check_updates:
            self._start_update_check(manual=False)

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def _build_docks(self) -> None:
        """Give each panel a dock of its own, tabbed together on the right.

        Each panel can be moved to any edge or floated. Matcap controls live
        inside Shading, where they follow the selected shading mode.
        """
        for key, title, panel in (
            ("model", "Model", self._model_panel),
            ("shading", "Shading", self._shading_panel),
            ("planes", "Planes", self._planes_panel),
            ("section", "Section", self._section_panel),
            ("measure", "Measure", self._measure_panel),
            ("annotate", "Annotate", self._annotate_panel),
            ("armature", "Armature", self._armature_panel),
            ("forms", "Forms", self._forms_panel),
            ("pose", "Pose", self._pose_panel),
            ("camera", "Camera", self._camera_panel),
        ):
            self._workspace.add_panel(key, title, panel)
        # Retain saved custom-control references from the former Matcap dock.
        from .elements.naming import register
        register(self._matcap_panel, "matcap")
        self._workspace.raise_first()

    def _sync_tab_switches(self) -> None:
        """Keep every dock's switch agreeing with the panel it speaks for."""
        self._workspace.sync_switches()

    def _build_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        self._menu_action(
            file_menu, "&Open Model...", self._open_model, "Ctrl+O", command="file.open_model"
        )
        self._menu_action(
            file_menu, "&Add Model...", self._add_model, "Ctrl+Shift+O", command="file.add_model"
        )
        self._menu_action(
            file_menu, "Load &Matcap...", self._matcap_panel.browse, command="file.load_matcap"
        )
        file_menu.addSeparator()
        self._menu_action(
            file_menu, "Export &Video...", self._export_film, "Ctrl+E", command="file.export_video"
        )
        file_menu.addSeparator()
        self._menu_action(
            file_menu, "&Save Session", self._save_session, "Ctrl+S", command="file.save_session"
        )
        self._menu_action(
            file_menu, "Save Session &As...", self._save_session_as, "Ctrl+Shift+S",
            command="file.save_session_as",
        )
        self._menu_action(
            file_menu, "&Load Session...", self._load_session, command="file.load_session"
        )
        file_menu.addSeparator()
        self._menu_action(file_menu, "E&xit", self.close, "Ctrl+Q", command="file.exit")

        edit_menu = self.menuBar().addMenu("&Edit")
        self._undo_action = self._menu_action(
            edit_menu, "&Undo", self._state.undo, "Ctrl+Z", command="edit.undo"
        )
        self._redo_action = self._menu_action(
            edit_menu, "&Redo", self._state.redo, "Ctrl+Shift+Z", command="edit.redo"
        )
        self._binder.add_key(
            "edit.redo_again", "Redo (second key)", self._state.redo, "Ctrl+Y", "Edit"
        )

        view_menu = self.menuBar().addMenu("&View")
        self._frame_action = self._menu_action(view_menu, "&Frame Object", self._state.frame_object)
        self._projection_action = self._menu_action(
            view_menu, "Toggle &Projection", self._toggle_projection
        )
        view_menu.addSeparator()
        self._view_actions = [
            self._menu_action(
                view_menu, label, lambda _=False, d=direction: self._camera_panel.look_along(d)
            )
            for label, direction in STANDARD_VIEWS
        ]
        view_menu.addSeparator()
        self._section_action = self._menu_action(
            view_menu, "Cross-&section", self._toggle_section, "Ctrl+K", checkable=True,
            command="view.section",
        )
        self._menu_action(
            view_menu, "Section Plane From &View", self._section_panel.set_plane_from_view,
            command="view.section_from_view",
        )
        model_menu = self.menuBar().addMenu("Mo&del")
        self._object_action = self._menu_action(
            model_menu, "&Transform Tool", self._toggle_object, checkable=True
        )
        model_menu.addSeparator()
        for mode, label in (("move", "&Move"), ("rotate", "&Rotate"), ("scale", "&Scale")):
            self._menu_action(
                model_menu, label, lambda _=False, m=mode: self._model_panel.set_mode(m),
                command=f"model.{mode}", label=f"Gesture: {label.replace('&', '')}",
            )
        model_menu.addSeparator()
        self._menu_action(
            model_menu, "&Remove Object", self._model_panel.remove_active, command="model.remove"
        )
        self._menu_action(
            model_menu, "D&uplicate Object", self._model_panel.duplicate_active,
            command="model.duplicate",
        )
        self._menu_action(
            model_menu, "Mer&ge Selected", self._model_panel.merge_selected, command="model.merge"
        )
        self._menu_action(
            model_menu, "S&plit Object", self._model_panel.split_active, command="model.split"
        )
        self._menu_action(
            model_menu, "Place at &Origin", self._model_panel.reset_transform,
            command="model.reset_transform",
        )
        panels_menu = self.menuBar().addMenu("&Panels")
        self._build_panels_menu(panels_menu)

        measure_menu = self.menuBar().addMenu("&Measure")
        self._measure_action = self._menu_action(
            measure_menu, "&Measure Tool", self._toggle_measure, checkable=True
        )
        self._cancel_action = self._menu_action(
            measure_menu, "&Cancel Current", self._viewport.cancel_tools
        )
        self._menu_action(
            measure_menu, "Clear &All", self._measure_panel.clear_all, command="measure.clear_all"
        )

        armature_menu = self.menuBar().addMenu("A&rmature")
        self._armature_action = self._menu_action(
            armature_menu, "A&rmature Tool", self._toggle_armature, checkable=True
        )
        armature_menu.addSeparator()
        self._menu_action(
            armature_menu, "&New Armature", self._armature_panel.new_armature,
            command="armature.new",
        )
        self._menu_action(
            armature_menu, "Start &Guided Preset", self._armature_panel.start_guide,
            command="armature.start_guide",
        )
        self._menu_action(
            armature_menu, "&Finish Preset", self._armature_panel.end_guide,
            command="armature.end_guide",
        )
        armature_menu.addSeparator()
        self._menu_action(
            armature_menu, "Clear &All", self._armature_panel.clear_all,
            command="armature.clear_all",
        )

        forms_menu = self.menuBar().addMenu("F&orms")
        self._forms_action = self._menu_action(
            forms_menu, "F&orms Tool", self._toggle_forms, checkable=True
        )
        forms_menu.addSeparator()
        self._menu_action(
            forms_menu, "&Start Form", self._forms_panel.start_guide, command="forms.start"
        )
        self._menu_action(
            forms_menu, "&Append Landmarks", self._forms_panel.append_landmarks,
            command="forms.append",
        )
        self._menu_action(
            forms_menu, "&Finish Form", self._forms_panel.end_guide, command="forms.finish"
        )
        forms_menu.addSeparator()
        self._menu_action(
            forms_menu, "Clear &All", self._forms_panel.clear_all, command="forms.clear_all"
        )

        pose_menu = self.menuBar().addMenu("&Pose")
        self._pose_action = self._menu_action(
            pose_menu, "&Pose Tool", self._toggle_pose, checkable=True
        )
        pose_menu.addSeparator()
        self._menu_action(
            pose_menu, "&New Skeleton", self._pose_panel.new_skeleton, command="pose.new"
        )
        self._menu_action(
            pose_menu, "&Humanoid Skeleton", self._pose_panel.humanoid_preset,
            command="pose.humanoid",
        )
        self._menu_action(
            pose_menu, "Skeleton From &Armature", self._pose_panel.from_armature,
            command="pose.from_armature",
        )
        self._menu_action(
            pose_menu, "Armature From &Skeleton", self._pose_panel.to_armature,
            command="pose.to_armature",
        )
        self._menu_action(
            pose_menu, "&Map to Humanoid", self._pose_panel.map_humanoid,
            command="pose.map_humanoid",
        )
        self._menu_action(
            pose_menu, "&Simplify Rig", self._pose_panel.simplify, command="pose.simplify"
        )
        pose_menu.addSeparator()
        self._menu_action(
            pose_menu, "&Reset Pose", self._pose_panel.reset_pose, command="pose.reset"
        )
        self._menu_action(
            pose_menu, "Clear &All", self._pose_panel.clear_all, command="pose.clear_all"
        )

        annotate_menu = self.menuBar().addMenu("&Annotate")
        self._annotate_action = self._menu_action(
            annotate_menu, "&Annotate Tool", self._toggle_annotate, checkable=True
        )
        annotate_menu.addSeparator()
        for mode in AnnotateMode:
            self._menu_action(
                annotate_menu, mode.label, lambda _=False, m=mode: self._set_annotate_mode(m),
                command=f"annotate.mode.{mode.value}", label=f"Draw: {mode.label}",
            )
        annotate_menu.addSeparator()
        self._menu_action(
            annotate_menu, "Clear A&ll", self._annotate_panel.clear_all,
            command="annotate.clear_all",
        )

        camera_menu = self.menuBar().addMenu("&Camera")
        self._menu_action(
            camera_menu, "&Save Current View", self._camera_panel.save_current_view, "Ctrl+B",
            command="camera.save_view",
        )
        self._menu_action(
            camera_menu, "&Rename Selected View", self._camera_panel.rename_selected,
            command="camera.rename_view",
        )
        self._next_view_action = self._menu_action(
            camera_menu, "&Next Saved View", lambda: self._camera_panel.cycle(1)
        )
        self._previous_view_action = self._menu_action(
            camera_menu, "&Previous Saved View", lambda: self._camera_panel.cycle(-1)
        )
        camera_menu.addSeparator()
        for slot in range(1, 10):
            self._menu_action(
                camera_menu,
                f"Recall View {slot}",
                lambda _=False, index=slot - 1: self._camera_panel.recall(index),
                f"Ctrl+{slot}",
                command=f"camera.recall_{slot}",
            )

        settings_menu = self.menuBar().addMenu("&Settings")
        self._menu_action(
            settings_menu, "&Preferences...", self._show_settings, "Ctrl+,", command="settings.open"
        )
        settings_menu.addSeparator()
        for key in GROUPS:
            self._menu_action(
                settings_menu,
                f"{key.title()}...",
                lambda _=False, group=key: self._show_settings(group),
                command=f"settings.open_{key}",
            )
        settings_menu.addSeparator()
        self._menu_action(
            settings_menu, "&Restore Defaults", self._reset_preferences, command="settings.restore"
        )

        help_menu = self.menuBar().addMenu("&Help")
        self._menu_action(
            help_menu, "&Controls", self._show_controls, "F1", command="help.controls"
        )
        self._menu_action(
            help_menu, "Check for &Updates...", self._check_for_updates, command="help.updates"
        )

    def _build_panels_menu(self, menu) -> None:
        """Which panels are open, and the panels the artist builds.

        Rebuilt every time it is opened, because the list of panels built by
        hand is not fixed and a menu that listed the ones that existed when
        the window was made would go stale the first time one was added.
        """

        def fill() -> None:
            menu.clear()
            self._menu_action(
                menu, "&New Custom Panel", self._new_custom_panel, "Ctrl+Shift+N",
                command="panels.new_custom",
            )
            custom = self._workspace.custom_panels()
            if custom:
                remove = menu.addMenu("&Remove Custom Panel")
                for key, panel in custom.items():
                    self._menu_action(
                        remove,
                        panel.title(),
                        lambda _=False, k=key: self._workspace.remove_custom_panel(k),
                    )
            menu.addSeparator()
            for dock in self._workspace.docks():
                action = dock.toggleViewAction()
                menu.addAction(action)
                # A dock's own action, which lives as long as the dock does,
                # so a key put on it stays put across the menu being rebuilt.
                self._binder.add_action(
                    f"panels.open.{dock.key()}", f"Open {dock.windowTitle()} Panel", action,
                    group="Panels",
                )
            menu.addSeparator()
            self._menu_action(menu, "Reset &Layout", self._reset_layout, command="panels.reset")
            # The entries made afresh just now have to be keyed like the rest.
            self._binder.rebind()

        menu.aboutToShow.connect(fill)
        fill()

    def _menu_action(
        self,
        menu,
        text,
        slot,
        shortcut=None,
        checkable: bool = False,
        command: str | None = None,
        label: str | None = None,
    ) -> QAction:
        """Add a menu entry, optionally with a window-wide shortcut.

        Given a ``command`` id the entry is the artist's to re-key: it is
        declared to the hotkey store with ``shortcut`` as what it ships with,
        and the binder puts whatever the store says on it.  Without one the
        shortcut, if any, is fixed -- for an entry made afresh each time a
        menu opens, which is no place to keep a key.
        """
        action = QAction(text, self)
        action.setCheckable(checkable)
        action.triggered.connect(slot)
        menu.addAction(action)
        if command is not None:
            self._binder.add_action(
                command, label or _plain(text), action, shortcut or "", _plain(menu.title())
            )
        elif shortcut is not None:
            action.setShortcut(QKeySequence(shortcut))
        return action

    def _build_viewport_shortcuts(self) -> None:
        """Single-key shortcuts, scoped so they never eat text input.

        They only fire while the 3D view has focus, which keeps keys like ``1``
        available for renaming measurements and typing unit labels.  Each is
        a command of the hotkey store, so the letter is the artist's to
        change; the menu entry beside each shows the key in its text rather
        than carrying it, because an entry carrying a key answers anywhere.
        """
        add = self._binder.add_view_key
        add("view.frame", "Frame Object", self._state.frame_object, "F", self._frame_action)
        add("view.projection", "Toggle Projection", self._toggle_projection, "P",
            self._projection_action)
        add("measure.tool", "Measure Tool", self._toggle_measure, "M", self._measure_action,
            "Measure")
        add("annotate.tool", "Annotate Tool", self._toggle_annotate, "A", self._annotate_action,
            "Annotate")
        add("annotate.eraser", "Brush / Eraser", self._toggle_eraser, "E", None, "Annotate")
        add("armature.tool", "Armature Tool", self._toggle_armature, "R", self._armature_action,
            "Armature")
        add("forms.tool", "Forms Tool", self._toggle_forms, "G", self._forms_action, "Forms")
        add("pose.tool", "Pose Tool", self._toggle_pose, "B", self._pose_action, "Pose")
        add("model.tool", "Transform Tool", self._toggle_object, "T", self._object_action,
            "Model")
        add("tools.cancel", "Cancel Current", self._viewport.cancel_tools, "Esc",
            self._cancel_action, "Measure")
        add("camera.previous_view", "Previous Saved View", lambda: self._camera_panel.cycle(-1),
            "[", self._previous_view_action, "Camera")
        add("camera.next_view", "Next Saved View", lambda: self._camera_panel.cycle(1), "]",
            self._next_view_action, "Camera")
        for index, ((label, direction), action) in enumerate(
            zip(STANDARD_VIEWS, self._view_actions, strict=True), start=1
        ):
            add(
                f"view.look.{slug(label)}",
                f"Look: {label}",
                lambda d=direction: self._camera_panel.look_along(d),
                str(index),
                action,
            )

    def _speak_for_commands(self) -> None:
        """Say which panel buttons are the same thing as a menu entry.

        The button that arms the measuring tool and the ``M`` that arms it
        are one command, not two: the button shows the letter after its
        name, its tooltip says the key, and Ctrl-Alt-clicking it re-keys the
        letter itself rather than putting a second key on the same thing.
        """
        for element, command in (
            ("measure.toggle", "measure.tool"),
            ("annotate.toggle", "annotate.tool"),
            ("armature.toggle", "armature.tool"),
            ("forms.toggle", "forms.tool"),
            ("pose.toggle", "pose.tool"),
            ("model.toggle", "model.tool"),
            ("section.enabled", "view.section"),
        ):
            control = lookup(element)
            if control is not None:
                control.setProperty(COMMAND_PROPERTY, command)

    def _assign_hotkey(self, widget) -> None:
        """The gesture's other half: Ctrl-Alt-click on a button asks for a key.

        The gesture is one object for the process, so every window hears
        it; only the one the button lives in answers.
        """
        top = widget.window()
        while top is not None and top is not self:
            top = top.parentWidget()
        if top is None:
            return
        if not ask_for(widget, self._hotkeys, self):
            self.statusBar().showMessage(
                "That control has no name a key could be kept under.", 4000
            )

    def _connect(self) -> None:
        self._state.status_message.connect(self.statusBar().showMessage)
        self._state.measurements_changed.connect(self._measure_panel.refresh_list)
        self._state.annotations_changed.connect(self._annotate_panel.refresh_list)
        self._state.armature_changed.connect(self._armature_panel.refresh_list)
        # The clay can be built on an armature, so the Planes panel has to
        # know when there is a new one, when one has been deleted, and when
        # the bones of the chosen one have been reordered or re-derived.
        self._state.armature_changed.connect(self._planes_panel.refresh_armatures)
        self._state.forms_changed.connect(self._forms_panel.refresh_list)
        self._state.skeleton_changed.connect(self._pose_panel.refresh_list)
        # The pose panel offers a skeleton grown out of any armature, so it
        # lists them and has to hear when they come and go.
        self._state.armature_changed.connect(self._pose_panel.refresh_list)
        self._state.render_changed.connect(self._forms_panel.refresh_display)
        self._state.bookmarks_changed.connect(self._camera_panel.refresh_bookmarks)
        self._state.render_changed.connect(self._shading_panel.update_enabled)
        self._state.render_changed.connect(self._planes_panel.update_enabled)
        self._state.film_changed.connect(self._planes_panel.film_changed)
        self._state.recording_changed.connect(self._planes_panel.recording_changed)
        self._state.camera_changed.connect(self._camera_panel.refresh_camera)
        # The clipping bars are scaled to the scene, which a new model resizes.
        self._state.mesh_changed.connect(self._camera_panel.refresh_camera)
        self._state.history_changed.connect(self._update_history_actions)
        self._state.render_changed.connect(self._sync_section_action)
        self._state.mesh_changed.connect(self._model_panel.refresh)
        self._state.objects_changed.connect(self._model_panel.refresh)
        self._state.mesh_deformed.connect(self._model_panel.refresh_transform)
        self._model_panel.attach(self._viewport.object_tool)
        self._model_panel.object_toggled.connect(self._set_transforming)
        self._model_panel.add_requested.connect(self._add_model)
        self._model_panel.repaint_requested.connect(self._viewport.update)
        self._viewport.object_mode_changed.connect(self._model_panel.set_mode)
        for signal in (
            self._state.render_changed,
            self._state.measurements_changed,
            self._state.annotations_changed,
            self._state.armature_changed,
            self._state.forms_changed,
            self._state.skeleton_changed,
            self._state.objects_changed,
        ):
            signal.connect(self._sync_tab_switches)

        self._viewport.measurement_created.connect(self._on_measurement_created)
        self._viewport.pick_failed.connect(
            lambda: self.statusBar().showMessage("No surface under the cursor", 2000)
        )
        self._planes_panel.export_film_requested.connect(self._export_film)
        self._measure_panel.measure_toggled.connect(self._set_measuring)
        self._measure_panel.center_requested.connect(self._viewport.center_on)
        self._measure_panel.selection_changed.connect(self._viewport.select_measurement)
        self._state.render_changed.connect(self._section_panel.refresh)
        self._annotate_panel.annotate_toggled.connect(self._set_annotating)
        self._armature_panel.attach(self._viewport.armature_tool)
        self._armature_panel.armature_toggled.connect(self._set_armaturing)
        self._armature_panel.center_requested.connect(self._viewport.center_on_point)
        self._viewport.armature_edited.connect(self._armature_panel.apply_edit)
        self._viewport.armature_selected.connect(self._armature_panel.select_node)
        self._viewport.landmark_selected.connect(self._armature_panel.select_landmark)
        self._armature_panel.repaint_requested.connect(self._viewport.update)
        self._forms_panel.attach(self._viewport.form_tool)
        self._forms_panel.form_toggled.connect(self._set_forming)
        self._forms_panel.center_requested.connect(self._viewport.center_on_point)
        self._forms_panel.repaint_requested.connect(self._viewport.update)
        self._viewport.form_edited.connect(self._forms_panel.apply_edit)
        self._viewport.form_landmark_selected.connect(self._forms_panel.select_landmark)
        self._pose_panel.attach(self._viewport.pose_tool, self._viewport.armature_tool)
        self._pose_panel.pose_toggled.connect(self._set_posing)
        self._pose_panel.center_requested.connect(self._viewport.center_on_point)
        self._pose_panel.repaint_requested.connect(self._viewport.update)
        self._viewport.skeleton_edited.connect(self._pose_panel.apply_edit)
        self._viewport.joint_selected.connect(self._pose_panel.select_joint)

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

    def _export_film(self) -> None:
        """Open the window that writes the film of a form's making to a file.

        Nothing is asked of the artist first except that there be a film: the
        recording may still be running, and exporting what has landed so far
        is a reasonable thing to want.  What is not reasonable is a dialog
        full of options for a film that does not exist, so that case is turned
        away here with the one sentence that says how to get one.
        """
        film = self._viewport.film
        if film is None or not len(film):
            QMessageBox.information(
                self,
                "Export Video",
                "There is no film to export yet.\n\nTurn on Planes > Simplify "
                "geometry, tick 'Record the making', and let a few stages land.",
            )
            return
        ExportVideoDialog(self._viewport, film, self).exec()

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
        self._sync_tools(measuring=active)

    def _set_annotating(self, active: bool) -> None:
        self._viewport.set_annotate_active(active)
        self._sync_tools(annotating=active)

    def _set_armaturing(self, active: bool) -> None:
        self._viewport.set_armature_active(active)
        self._sync_tools(armaturing=active)

    def _set_forming(self, active: bool) -> None:
        self._viewport.set_form_active(active)
        self._sync_tools(forming=active)

    def _set_posing(self, active: bool) -> None:
        self._viewport.set_pose_active(active)
        self._sync_tools(posing=active)

    def _set_transforming(self, active: bool) -> None:
        self._viewport.set_object_active(active)
        self._sync_tools(transforming=active)

    def _sync_tools(
        self,
        measuring: bool = False,
        annotating: bool = False,
        armaturing: bool = False,
        forming: bool = False,
        posing: bool = False,
        transforming: bool = False,
    ) -> None:
        """Put every panel button and menu entry where the tools now stand.

        Only one tool is ever armed, so arming one is also disarming the
        others; saying that once here keeps the four of them from drifting
        apart.
        """
        self._measure_panel.set_measuring(measuring)
        self._measure_action.setChecked(measuring)
        self._annotate_panel.set_annotating(annotating)
        self._annotate_action.setChecked(annotating)
        self._armature_panel.set_armaturing(armaturing)
        self._armature_action.setChecked(armaturing)
        self._forms_panel.set_forming(forming)
        self._forms_action.setChecked(forming)
        self._pose_panel.set_posing(posing)
        self._pose_action.setChecked(posing)
        self._model_panel.set_active(transforming)
        self._object_action.setChecked(transforming)

    def _toggle_object(self) -> None:
        self._set_transforming(not self._viewport.object_tool.active)

    def _toggle_measure(self) -> None:
        self._set_measuring(not self._viewport.measure_tool.active)

    def _toggle_annotate(self) -> None:
        self._set_annotating(not self._viewport.annotate_tool.active)

    def _toggle_armature(self) -> None:
        self._set_armaturing(not self._viewport.armature_tool.active)

    def _toggle_forms(self) -> None:
        self._set_forming(not self._viewport.form_tool.active)

    def _toggle_pose(self) -> None:
        self._set_posing(not self._viewport.pose_tool.active)

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
        """Open the controls reference.

        A message box was the wrong container for this: it grows to fit
        whatever it is given, has no scroll bar when that is taller than the
        screen, and cannot be left open beside the thing it is describing.
        This is a window -- scrolled, resizable, and not modal, so the
        shortcut you just looked up can be tried while it is still on screen.
        """
        if self._controls is None:
            self._controls = ControlsWindow(CONTROLS_TEXT, self)
        self._controls.show()
        self._controls.raise_()
        self._controls.activateWindow()

    # ------------------------------------------------------------------
    # Preferences
    # ------------------------------------------------------------------

    def _show_settings(self, group: str | None = None) -> None:
        """Open the preferences, on one group when the menu asked for one."""
        if self._settings is None:
            self._settings = SettingsWindow(self._preferences, self, self._hotkeys)
        # What the driver actually gave us, which is the only honest answer to
        # "did changing that do anything": a QOpenGLWidget reports nought for
        # its own sample count whatever it is really drawing with.
        self._settings.set_samples_in_use(self._viewport.samples_in_use())
        if isinstance(group, str) and group in GROUPS:
            self._settings.show_group(group)
        self._settings.show()
        self._settings.raise_()
        self._settings.activateWindow()

    def _reset_preferences(self) -> None:
        self._preferences.reset()
        self.statusBar().showMessage("Preferences are back to how they ship.", 4000)

    def _apply_preferences(self) -> None:
        """Push the preferences that this window's own parts hold a copy of.

        The store has already dealt with the ones belonging to the process --
        the accent, the type size, the folder the matcaps come from.  What is
        left is everything owned by a widget, which the store has no business
        knowing about.  Run once on the way up and again on every change, so
        there is one path rather than two that have to agree.
        """
        prefs = self._preferences.value
        self._viewport.set_show_fps(prefs.viewport.show_fps)
        self._viewport.set_fps_corner(prefs.viewport.fps_corner)
        self._viewport.set_antialiasing(prefs.viewport.antialiasing)
        navigation = self._viewport.navigation
        navigation.orbit_speed = prefs.navigation.orbit_speed
        navigation.zoom_speed = prefs.navigation.zoom_speed
        navigation.invert_orbit_x = prefs.navigation.invert_orbit_x
        navigation.invert_orbit_y = prefs.navigation.invert_orbit_y
        # Switching this off while it is held has to let go now, not at the
        # next time the window changes hands.
        self._wake_lock.set_held(prefs.viewport.keep_awake and self.isActiveWindow())
        # Where the matcaps are read from is a preference, and the gallery is
        # a list of what was in that folder when it was last looked at.  Only
        # when it has actually moved: rereading a folder of images is not
        # something to do every time somebody nudges the accent colour.
        folder = prefs.folders.matcaps
        if folder != self._matcap_folder:
            self._matcap_folder = folder
            self._matcap_panel.reload_gallery()

    def reopen_last_session(self, background: bool = False) -> bool:
        """Pick up whatever was last being worked on, if that was asked for.

        A session first, because a session carries the marks on the model as
        well as the model; the model on its own when there is no session,
        because most of what gets looked at never becomes one -- an afternoon
        spent turning a figure over saves nothing and is still the thing you
        expect to find in the morning.

        Called on the way up, after anything named on the command line has
        been dealt with: something asked for explicitly always beats something
        remembered.  A remembered path that has since been moved or deleted is
        not an error worth a dialog on startup, so it is passed over in
        silence and the next one is tried.
        """
        if not self._preferences.value.startup.reopen_last_session:
            return False
        settings = QSettings()
        session = _remembered(settings.value(LAST_SESSION, ""))
        if session is not None:
            self.load_session(session, background=background)
            return True
        model = _remembered(settings.value(LAST_MODEL, ""))
        if model is not None:
            self.open_model(model, background=background)
            return True
        return False

    def _remember_session(self, path: str | Path) -> None:
        """Write down the session just saved or loaded, for the next start."""
        QSettings().setValue(LAST_SESSION, str(path))

    def _remember_model(self, path: str | Path) -> None:
        """Write down the model just opened, for when there is no session.

        This also clears the remembered session: opening a different model is
        moving on to another piece of work, and coming back to the session
        belonging to the last one would be the wrong answer said confidently.
        """
        settings = QSettings()
        settings.setValue(LAST_MODEL, str(path))
        settings.remove(LAST_SESSION)

    # ------------------------------------------------------------------
    # Updates
    # ------------------------------------------------------------------

    def _end_update_task(self) -> None:
        if self._update_task is not None:
            self._update_task.end()
            self._update_task = None

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
            self._end_update_task()
            self._update_task = self._state.tasks.begin(
                "Checking for updates", blocking=False, cancellable=False
            )
            self._update_task.progress.report(message="Asking GitHub for the newest release...")
        checker.start()

    def _check_for_updates(self) -> None:
        self._start_update_check(manual=True)

    def _on_update_available(self, release: Release, manual: bool) -> None:
        self._end_update_task()
        if not manual and is_skipped(release):
            return
        self.statusBar().showMessage(f"Version {release.version} is available", 8000)
        show_update_dialog(self, release)

    def _on_up_to_date(self, manual: bool) -> None:
        self._end_update_task()
        if manual:
            show_up_to_date_dialog(self)

    def _on_update_check_failed(self, error: str, manual: bool) -> None:
        self._end_update_task()
        if manual:
            show_failure_dialog(self, error)

    # ------------------------------------------------------------------
    # File handling
    # ------------------------------------------------------------------

    def open_model(self, path: str | Path, background: bool = False) -> None:
        """Load a model, reporting failures without tearing down the window.

        In the ``background`` the file is read on a thread with a card over
        the view saying so, and the scene changes when it has been; the
        window stays answerable meanwhile.  Otherwise the read is done here
        and now, which is what a caller that goes on to look at the result
        wants.
        """
        path = Path(path)
        if background:
            self._read_then(path, f"Opening {path.name}", "Open Model", self._adopt_model)
            return
        try:
            mesh = read_mesh(path)
        except (MeshLoadError, OSError) as error:
            QMessageBox.critical(self, "Open Model", str(error))
            return
        self._adopt_model(path, mesh)

    def _adopt_model(self, path: Path, mesh: Mesh) -> None:
        try:
            self._state.load_mesh(path, source=mesh)
        except (MeshLoadError, OSError, ValueError) as error:
            QMessageBox.critical(self, "Open Model", str(error))
            return
        self._session_path = self._state.default_session_path()
        self._remember_model(path)
        self.setWindowTitle(f"{APP_NAME} - {Path(path).name}")
        self._refresh_panels()
        self._offer_humanoid_mapping()

    def _read_then(self, path: Path, title: str, box: str, adopt) -> None:
        """Read a model file off the window, then hand it to ``adopt`` here."""

        def work(progress) -> Mesh:
            progress.report(message=f"Reading {path.name}...")
            mesh = read_mesh(path)
            progress.report(message=f"Placing {mesh.vertex_count:,} vertices...")
            return mesh

        self._state.tasks.run(
            title,
            work,
            done=lambda mesh: adopt(path, mesh),
            failed=lambda error: QMessageBox.critical(self, box, str(error)),
        )

    def _offer_humanoid_mapping(self) -> None:
        """Ask whether a rig that arrived with the model should be read as a figure.

        Only when the names say it is one, only when nothing has mapped it
        yet -- a session loaded beside the model may already have -- and
        as a question rather than a deed: the guess is a guess, and the
        artist may be after the rig's own names.
        """
        skeleton = self._state.bound_skeleton()
        if skeleton is None or any(joint.role for joint in skeleton.joints):
            return
        roles = humanoid_roles(skeleton)
        if not looks_humanoid(roles):
            return
        answer = QMessageBox.question(
            self,
            "Humanoid rig",
            f"{skeleton.name} came with {len(skeleton.joints)} joints, and their names "
            f"read as a humanoid: {len(roles)} of them fit the figure's roles.\n\n"
            "Map them onto the humanoid roles?  The names are kept; each joint's "
            "Role box in the Pose tab is where to correct a guess.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self._pose_panel.map_humanoid()

    def add_model(self, path: str | Path, background: bool = False) -> None:
        """Add a model to the scene beside what is already there."""
        path = Path(path)
        if background:
            self._read_then(path, f"Adding {path.name}", "Add Model", self._adopt_added)
            return
        try:
            mesh = read_mesh(path)
        except (MeshLoadError, OSError) as error:
            QMessageBox.critical(self, "Add Model", str(error))
            return
        self._adopt_added(path, mesh)

    def _adopt_added(self, path: Path, mesh: Mesh) -> None:
        try:
            self._state.add_mesh(path, source=mesh)
        except (MeshLoadError, OSError, ValueError) as error:
            QMessageBox.critical(self, "Add Model", str(error))
            return
        self._remember_model(path)
        if self._session_path is None:
            self._session_path = self._state.default_session_path()
        self._refresh_panels()
        self._offer_humanoid_mapping()

    def _add_model(self) -> None:
        start = model_dir()
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Add Model",
            str(start if start.is_dir() else Path.home()),
            MESH_FILTER,
        )
        if path:
            self.add_model(path, background=True)

    def _open_model(self) -> None:
        start = model_dir()
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Model",
            str(start if start.is_dir() else Path.home()),
            MESH_FILTER,
        )
        if path:
            self.open_model(path, background=True)

    def _save_session(self) -> None:
        target = self._session_path or self._state.default_session_path()
        if target is None:
            self._save_session_as()
            return
        self._state.save_session(target, layout=self._workspace.to_dict())
        self._session_path = Path(target)
        self._remember_session(target)

    def _save_session_as(self) -> None:
        suggestion = self._session_path or self._state.default_session_path()
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Session",
            str(suggestion or Path.home() / f"untitled{SESSION_SUFFIX}"),
            f"Reference Viewer session (*{SESSION_SUFFIX});;JSON (*.json)",
        )
        if path:
            self._state.save_session(path, layout=self._workspace.to_dict())
            self._session_path = Path(path)
            self._remember_session(path)

    def _load_session(self) -> None:
        suggestion = self._session_path or self._state.default_session_path()
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Session",
            str(suggestion.parent if suggestion else Path.home()),
            f"Reference Viewer session (*{SESSION_SUFFIX});;JSON (*.json)",
        )
        if path:
            self.load_session(path, background=True)

    def load_session(self, path: str | Path, background: bool = False) -> None:
        """Load a session; in the ``background``, its models are read on a thread first."""
        path = Path(path)
        if not background:
            self._adopt_session(path, None)
            return
        try:
            session = Session.load(path)
        except (OSError, ValueError) as error:
            QMessageBox.critical(self, "Load Session", str(error))
            return
        files = [
            Path(record.path)
            for record in self._state.records_of(session)
            if record.path and Path(record.path).is_file()
        ]

        def work(progress) -> dict[str, Mesh]:
            read: dict[str, Mesh] = {}
            for index, file in enumerate(files):
                progress.report(index, len(files), f"Reading {file.name}...")
                try:
                    read[same_file(file)] = read_mesh(file)
                except (MeshLoadError, OSError):
                    continue  # the state says which files it could not place
            progress.report(len(files), len(files), "Placing the scene...")
            return read

        self._state.tasks.run(
            f"Loading {path.name}",
            work,
            done=lambda read: self._adopt_session(path, read),
            failed=lambda error: QMessageBox.critical(self, "Load Session", str(error)),
        )

    def _adopt_session(self, path: Path, read: dict[str, Mesh] | None) -> None:
        try:
            self._state.load_session(path, sources=read)
        except (OSError, ValueError, MeshLoadError) as error:
            QMessageBox.critical(self, "Load Session", str(error))
            return
        self._session_path = Path(path)
        self._remember_session(path)
        self._refresh_panels()
        # A session carries the panels the artist had built for that piece of
        # work.  Only when it has some: a file saved before panels were part
        # of one, or by someone who never built any, must not be able to
        # sweep away the ones the window already has.
        if self._state.session_layout.get("custom"):
            self._workspace.restore(self._state.session_layout)

    def _refresh_panels(self) -> None:
        for panel in self._workspace.panels():
            panel.refresh()

    # ------------------------------------------------------------------
    # The layout
    # ------------------------------------------------------------------

    def _new_custom_panel(self) -> None:
        """Open an empty panel of the artist's own and bring it to the front."""
        self._workspace.reveal(self._workspace.new_custom_panel())
        self.statusBar().showMessage(
            "Alt-drag any control into the new panel; drag it into the view to "
            "take it out again.",
            8000,
        )

    def _restore_layout(self) -> None:
        """Put the docks and the hand-built panels back where they were.

        Unless the artist would rather every session started from the
        arrangement the application ships with, which is what a shared machine
        or a teaching room wants.
        """
        if self._preferences.value.interface.restore_layout:
            self._workspace.load()

    def _save_layout(self) -> None:
        self._workspace.save()

    def _reset_layout(self) -> None:
        """Put the panels back where they started, now."""
        self._workspace.reset()
        self.statusBar().showMessage("The panels are back where they started.", 4000)

    # ------------------------------------------------------------------
    # Window state
    # ------------------------------------------------------------------

    def changeEvent(self, event) -> None:  # noqa: N802 - Qt naming
        """Follow the machine's sleep to whether this window is in front."""
        super().changeEvent(event)
        if event.type() == QEvent.Type.ActivationChange:
            awake = self._preferences.value.viewport.keep_awake
            self._wake_lock.set_held(awake and self.isActiveWindow())

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt naming
        self._save_layout()
        self._wake_lock.release()
        # A recording still running when the interpreter tears its modules
        # down is a crash on the way out, so the window does not leave
        # without it.  It is asked to stop first, so the wait is one stage.
        # The same goes for whatever else is being worked on a thread.
        self._viewport.stop_recording()
        self._state.tasks.wait()
        super().closeEvent(event)

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt naming
        super().resizeEvent(event)
        self._place_banner()

    def eventFilter(self, watched, event) -> bool:  # noqa: N802 - Qt naming
        """Keep the banner over the view as the docks push the view about."""
        if watched is self._viewport and event.type() in (
            QEvent.Type.Resize,
            QEvent.Type.Move,
        ):
            self._place_banner()
        return super().eventFilter(watched, event)

    def _place_banner(self) -> None:
        """Sit the banner at the foot of the view, centred, above the status bar."""
        if not self._banner.isVisible():
            return
        corner = self._viewport.mapTo(self, QPoint(0, 0))
        width = min(440, max(self._viewport.width() - 32, 240))
        self._banner.setFixedWidth(width)
        self._banner.adjustSize()
        x = corner.x() + (self._viewport.width() - width) // 2
        y = corner.y() + self._viewport.height() - self._banner.height() - 18
        self._banner.move(x, max(y, corner.y()))
        self._banner.raise_()

    # ------------------------------------------------------------------
    # Drag and drop
    # ------------------------------------------------------------------

    def dragEnterEvent(self, event) -> None:  # noqa: N802 - Qt naming
        # A copied control is let in wherever it arrives, and where it may
        # actually land is decided on the way past instead.  Refusing it here
        # would take this window out of the drag for good -- a drag refused at
        # the door gets no further events from it -- so a copy that entered
        # over the menu bar could never then be dropped on the model.
        if self._carrying_a_copy(event):
            event.acceptProposedAction()
            return
        if self._carrying_a_file(event):
            event.acceptProposedAction()

    def dragMoveEvent(self, event) -> None:  # noqa: N802 - Qt naming
        if self._discarding(event):
            event.acceptProposedAction()
            return
        # A file the window can open is welcome anywhere over it.  This has
        # to be said on every move, not only at the door: a drop lands only
        # where the last move was accepted, so a file that was let in and
        # then refused on the way past could never be dropped at all.
        if not self._carrying_a_copy(event) and self._carrying_a_file(event):
            event.acceptProposedAction()
            return
        # Refusing one position says only that; the moves keep coming.
        event.ignore()

    def _carrying_a_file(self, event) -> bool:
        return any(self._droppable(url) for url in event.mimeData().urls())

    @staticmethod
    def _carrying_a_copy(event) -> bool:
        """Whether the drag is a copy being moved out of a hand-built panel."""
        note = carried(event.mimeData())
        return bool(note is not None and note.get("moving") and in_flight() is not None)

    def _discarding(self, event) -> bool:
        """Whether this drag is a copied control being let go over the model.

        Dragging a copy out of the panel it was put in and letting go over the
        view is how it is thrown away: the view is the one large target that
        is never a place a control could land, so dropping one there can only
        mean getting rid of it.  Anywhere else -- the menu bar, the status bar,
        another panel's dock -- the drop is refused and the copy stays where it
        was, which is the safe answer for a gesture that destroys something.
        """
        if not self._carrying_a_copy(event):
            return False
        return self._over_the_view(event.position().toPoint())

    def _over_the_view(self, point) -> bool:
        """Whether a point in the window's own coordinates is on the model."""
        central = self.centralWidget()
        if central is None:
            return False
        corner = central.mapTo(self, central.rect().topLeft())
        return central.rect().translated(corner).contains(point)

    def dropEvent(self, event) -> None:  # noqa: N802 - Qt naming
        if self._discarding(event):
            self._discard(in_flight())
            event.acceptProposedAction()
            return
        for url in event.mimeData().urls():
            if self.open_path(url.toLocalFile(), background=True):
                event.acceptProposedAction()
                return
        # Nothing here wanted it.  Saying so matters for a copy let go
        # somewhere that is not the model: the copy has to stay where it was,
        # and a drop that quietly did nothing would read as one that worked.
        event.ignore()

    def _discard(self, holder) -> bool:
        """Take a copied control out of whichever hand-built panel holds it."""
        if holder is None:
            return False
        for panel in self._workspace.custom_panels().values():
            if panel.isAncestorOf(holder):
                panel.drop_holder(holder)
                self.statusBar().showMessage("Removed the copied control.", 4000)
                return True
        return False

    @staticmethod
    def _droppable(url) -> bool:
        return opens_as(url.toLocalFile()) is not None

    def open_path(self, path: str | Path, background: bool = False) -> bool:
        """Open a file by what it is: a model, a session or a matcap.

        The one door every file arrives through, whether dropped on the
        window, named on the command line, handed over by the desktop's
        "Open with" or dragged onto the application itself.  Returns whether
        the file was one of ours; a file that is but will not load reports
        that to the artist and still counts as taken, so a drop or a launch
        does not go on looking for somewhere else to put it.
        """
        path = Path(path)
        kind = opens_as(path)
        if kind == "model":
            self.open_model(path, background=background)
        elif kind == "session":
            self.load_session(path, background=background)
        elif kind == "matcap":
            self.load_matcap(path)
        else:
            return False
        return True


def _plain(text: str) -> str:
    """A menu entry's text as a name: no accelerator ampersand, no trailing dots."""
    return text.replace("&", "").rstrip(".").strip()


def _remembered(written) -> Path | None:
    """A path written down last time, if it is one and it is still there."""
    if not isinstance(written, str) or not written.strip():
        return None
    path = Path(written)
    return path if path.is_file() else None
