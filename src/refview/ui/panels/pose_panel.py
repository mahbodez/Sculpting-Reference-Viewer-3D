"""The skeletons: their joints, the pose they stand in, and how they are drawn."""

from __future__ import annotations

from dataclasses import replace

import numpy as np
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QSplitter,
    QStyledItemDelegate,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ...core.armature import Buried
from ...core.autoskin import AutoSkinError, auto_skin
from ...core.commands import AddItem, RemoveItem, ReplaceItems, SetAttributes
from ...core.history import ARMATURE, SKELETON
from ...core.landmarks import role_name
from ...core.linalg import euler_to_quat, quat_to_euler
from ...core.rigging import (
    HUMANOID_ROLES,
    armature_from_skeleton,
    build_humanoid_skeleton,
    humanoid_roles,
    simplified,
    skeleton_from_armature,
    with_roles,
)
from ...core.skeleton import Joint, Skeleton, SkinMethod, normalized_rotation
from ..icons import lock_icon
from ..widgets import PointEdit, SliderSpin, collapsible_group, form_group, symbol_button
from .base import Panel

_NAME_COLUMN = 0
_LOCK_COLUMN = 1

_TOGGLE_TIP = (
    "Pose the model by its bones.\n"
    "Drag a joint and the bone above it swings to follow, carrying everything\n"
    "below; drag a root and the whole figure moves.  Shift+drag rolls a joint\n"
    "about its own bone, Ctrl+drag pulls it in depth.  With the tool armed a\n"
    "click that lands on nothing adds a joint under the selected one.\n"
    "Alt+drag still orbits, and Esc drops a pull without disarming the tool."
)

_FIT_TIP = (
    "Dragging a joint moves where it rests instead of bending the bone above\n"
    "it, and its children stay where they were: pull the knee into the knee\n"
    "and both the thigh and the shin adjust.  For fitting a preset to a model.\n"
    "A skeleton the model is skinned to keeps its rest, so this leaves it be."
)

_HUMANOID_TIP = (
    "A proportioned figure, eight heads tall, standing on the bottom of the\n"
    "model's box and facing forwards.  A starting point to be fitted, not a\n"
    "fit: turn on Fit and pull the joints into place, or measure the figure\n"
    "with the Armature tab's guided preset and grow a skeleton out of that."
)

_FROM_ARMATURE_TIP = (
    "Grow a skeleton out of an armature.  An armature is a graph and a\n"
    "skeleton is a tree, so it is grown from a root -- the node selected in\n"
    "the Armature tab, else the pelvis, else the best-connected node -- and\n"
    "a bone that would close a loop is left out and counted."
)

_TO_ARMATURE_TIP = (
    "Lay an armature under the skeleton as it is posed: every joint a node,\n"
    "every bone a bone, the roles kept, so the clay modes can read a figure\n"
    "off a rig that arrived with the model."
)

_MAP_TIP = (
    "Read the joints' names and guess which is the pelvis, which the left knee\n"
    "and so on, the way Mixamo, Biped, Unreal, Rigify and Character Creator\n"
    "name them.  A guess, and each joint's Role box is where to correct it."
)

_SIMPLIFY_TIP = (
    "Take the detail out of a rig: the fingers, the toes past the ball, the\n"
    "face, the breasts, and the twist, share, roll and end helpers a game rig\n"
    "carries.  What is left is the figure a pose is read from.  A joint with a\n"
    "humanoid role always stays, and the skin weights of what went fold onto\n"
    "the nearest joint that stayed, so the model still follows."
)

_DEFORM_TIP = (
    "Whether the model follows this skeleton.  A skeleton that came with the\n"
    "model has the skin weights to move it by, and one skinned to it here\n"
    "has been given some; any other poses in the air."
)

_SKIN_TIP = (
    "Give the active model skin weights for this skeleton, so that posing the\n"
    "bones poses the model.  Not the weights a rigger would paint, but weights\n"
    "made in a moment and good enough to read a pose off; one undo step, and\n"
    "Unskin takes them off again.  The skeleton is bound as it stands: its\n"
    "pose becomes its rest.  A skin made here is saved beside the session."
)

_METHOD_TIP = (
    "How the weights are decided.  Heat diffusion lets each bone's warmth\n"
    "spread over the surface of the model and takes the temperature as the\n"
    "weight, so a hand on a hip stays the hand's; the blend at a joint is as\n"
    "wide as the limb is thick.  Envelope shares each vertex among the\n"
    "nearest few bones by distance, through the air.  Nearest bone gives\n"
    "each vertex wholly to one bone, like a puppet."
)

_HEAT_TIP = (
    "How tightly the weights hug the nearest bone.  Higher is a narrower\n"
    "blend at every joint; lower lets each bone reach further along the skin."
)

_FALLOFF_TIP = (
    "The power the distance is raised to.  Two is inverse-square; higher\n"
    "sharpens each vertex towards its nearest bone."
)

_INFLUENCES_TIP = "How many bones may share one vertex.  One is rigid pieces."

_FACING_TIP = (
    "Pass over a bone that lies out in front of the skin rather than behind\n"
    "it when choosing the nearest -- the other thigh, the torso beside an\n"
    "arm.  Turn off only for a model whose normals point the wrong way."
)

_ROLE_TIP = (
    "Which slot of a humanoid this joint fills.  What the Armature tab's\n"
    "presets call it, so a skeleton turned into an armature is read as a figure."
)

_ROTATION_TIP = (
    "The turn at this joint, about its own axes, in degrees.  What dragging\n"
    "a child joint in the view sets; the sliders are for a number read off a\n"
    "reference or a nudge too small to drag."
)

_OFFSET_TIP = (
    "How far the joint is shifted from where it rests, in the display unit.\n"
    "On a root this is how the figure is moved; on any other joint it\n"
    "stretches the bone above it."
)


def _row(*buttons: QWidget) -> QWidget:
    holder = QWidget()
    layout = QHBoxLayout(holder)
    layout.setContentsMargins(0, 0, 0, 0)
    for button in buttons:
        layout.addWidget(button)
    return holder


class _NameOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):  # noqa: N802 - Qt naming
        if index.column() != _NAME_COLUMN:
            return None
        return super().createEditor(parent, option, index)


class PosePanel(Panel):
    """Arms the pose tool, lists the joints and poses the selected one."""

    pose_toggled = Signal(bool)
    center_requested = Signal(object)
    repaint_requested = Signal()

    def _build(self) -> None:
        self._tool = None
        self._armature_tool = None
        #: What the selected joint's rotation was when a slider drag began.
        self._turn_previous: tuple | None = None

        self._toggle = QPushButton("Pose")
        self._toggle.setCheckable(True)
        self._toggle.setToolTip(_TOGGLE_TIP)
        self._toggle.toggled.connect(self._on_toggled)
        self._add(self._toggle)

        self._splitter = QSplitter(Qt.Orientation.Vertical)
        self._splitter.setChildrenCollapsible(False)
        self._add(self._splitter)

        below = QWidget()
        self._body = QVBoxLayout(below)
        self._body.setContentsMargins(0, 8, 0, 0)
        self._body.setSpacing(8)

        self._build_tree()
        self._splitter.addWidget(below)
        self._splitter.setStretchFactor(0, 1)
        self._splitter.setStretchFactor(1, 0)

        self._build_selection()
        self._build_skeleton()
        self._build_skinning()
        self._build_placement()
        self._build_display()
        self._body.addStretch(1)
        self._connect()

    def _place(self, widget: QWidget) -> QWidget:
        self._body.addWidget(widget)
        return widget

    def _build_tree(self) -> None:
        self._tree = QTreeWidget()
        self._tree.setColumnCount(2)
        self._tree.setHeaderLabels(["Joint", ""])
        self._tree.setRootIsDecorated(True)
        # A rig runs eight or nine joints deep; Qt's usual step would push
        # the fingers off the edge of any dock.
        self._tree.setIndentation(11)
        self._tree.setAlternatingRowColors(True)
        self._tree.setItemDelegate(_NameOnlyDelegate(self._tree))
        self._tree.setEditTriggers(
            QTreeWidget.EditTrigger.DoubleClicked | QTreeWidget.EditTrigger.EditKeyPressed
        )
        header = self._tree.header()
        header.setSectionResizeMode(_NAME_COLUMN, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(_LOCK_COLUMN, QHeaderView.ResizeMode.ResizeToContents)
        self._tree.itemChanged.connect(self._on_item_changed)
        self._tree.itemClicked.connect(self._on_item_clicked)
        self._tree.itemSelectionChanged.connect(self._on_selection_changed)
        self._tree.setMinimumHeight(140)
        self._splitter.addWidget(self._tree)

        self._delete = symbol_button("trash", "Delete")
        self._delete.setToolTip(
            "Remove the selected joint, re-hanging its children from its parent --\n"
            "or the whole skeleton, when its row is selected."
        )
        self._delete_branch = QPushButton("Delete Branch")
        self._delete_branch.setToolTip("Remove the selected joint and everything below it.")
        self._center = symbol_button("centre", "Centre View")
        self._add_row(self._delete, self._delete_branch, self._center)

        self._new = symbol_button("plus", "New Skeleton")
        self._humanoid = QPushButton("Humanoid")
        self._humanoid.setToolTip(_HUMANOID_TIP)
        self._clear = QPushButton("Clear All")
        self._add_row(self._new, self._humanoid, self._clear)

    def _build_selection(self) -> None:
        box, form = form_group("Selected joint")
        self._selection_box = box
        self._selection_form = form
        self._turn = []
        for axis in ("X", "Y", "Z"):
            slider = SliderSpin(-180.0, 180.0, 0.0, decimals=1, step=1.0, suffix="°")
            slider.setToolTip(_ROTATION_TIP)
            form.addRow(f"Turn {axis}", slider)
            self._turn.append(slider)
        self._offset = PointEdit()
        self._offset.setToolTip(_OFFSET_TIP)
        form.addRow("Offset", self._offset)
        self._role = QComboBox()
        self._role.addItem("(none)", "")
        for role in HUMANOID_ROLES:
            self._role.addItem(role_name(role), role)
        self._role.setToolTip(_ROLE_TIP)
        form.addRow("Role", self._role)
        self._parent = QComboBox()
        self._parent.setToolTip(
            "Which joint this one hangs from.  It keeps its place in the scene\n"
            "when re-hung; a joint cannot hang from anything below itself."
        )
        form.addRow("Parent", self._parent)
        self._reset_joint = QPushButton("Reset Joint")
        self._reset_joint.setToolTip("Put this joint back at rest, leaving its children posed.")
        self._reset_branch = QPushButton("Reset Branch")
        self._reset_branch.setToolTip("Put this joint and everything below it back at rest.")
        form.addRow("", _row(self._reset_joint, self._reset_branch))
        self._place(box)

    def _build_skeleton(self) -> None:
        box, form = form_group("Skeleton")
        self._skeleton_box = box
        self._skeleton_form = form
        self._bound_note = QLabel()
        self._bound_note.setWordWrap(True)
        self._bound_note.setStyleSheet("color: #8f939b;")
        form.addRow(self._bound_note)
        self._deform = QCheckBox("Model follows this skeleton")
        self._deform.setToolTip(_DEFORM_TIP)
        form.addRow("", self._deform)
        self._reset_pose = QPushButton("Reset Pose")
        self._reset_pose.setToolTip("Put every joint of this skeleton back at rest.")
        self._map = QPushButton("Map to Humanoid")
        self._map.setToolTip(_MAP_TIP)
        form.addRow("", _row(self._reset_pose, self._map))
        self._simplify = QPushButton("Simplify")
        self._simplify.setToolTip(_SIMPLIFY_TIP)
        self._to_armature = QPushButton("To Armature")
        self._to_armature.setToolTip(_TO_ARMATURE_TIP)
        form.addRow("", _row(self._simplify, self._to_armature))
        self._armature_source = QComboBox()
        self._armature_source.setToolTip(_FROM_ARMATURE_TIP)
        self._from_armature = QPushButton("From Armature")
        self._from_armature.setToolTip(_FROM_ARMATURE_TIP)
        form.addRow("Armature", self._armature_source)
        form.addRow("", self._from_armature)
        self._place(box)

    def _build_skinning(self) -> None:
        box, form = collapsible_group("Auto-skin")
        self._skin_box = box
        self._skin_form = form
        self._skin_method = QComboBox()
        for method in SkinMethod:
            self._skin_method.addItem(method.label, method.value)
        self._skin_method.setToolTip(_METHOD_TIP)
        form.addRow("Method", self._skin_method)
        self._skin_influences = SliderSpin(1.0, 4.0, 4.0, decimals=0, step=1.0)
        self._skin_influences.setToolTip(_INFLUENCES_TIP)
        form.addRow("Bones per vertex", self._skin_influences)
        self._skin_heat = SliderSpin(0.1, 10.0, 1.0, decimals=2, step=0.1)
        self._skin_heat.setToolTip(_HEAT_TIP)
        form.addRow("Heat", self._skin_heat)
        self._skin_falloff = SliderSpin(0.5, 6.0, 2.0, decimals=1, step=0.5)
        self._skin_falloff.setToolTip(_FALLOFF_TIP)
        form.addRow("Falloff", self._skin_falloff)
        self._skin_facing = QCheckBox("Prefer bones behind the surface")
        self._skin_facing.setToolTip(_FACING_TIP)
        form.addRow("", self._skin_facing)
        self._skin = QPushButton("Skin to Model")
        self._skin.setToolTip(_SKIN_TIP)
        self._unskin = QPushButton("Unskin")
        self._unskin.setToolTip("Take off the skin made here; the skeleton keeps its joints.")
        form.addRow("", _row(self._skin, self._unskin))
        self._place(box)

    def _build_placement(self) -> None:
        box, form = form_group("Placement")
        self._fit = QCheckBox("Fit: drag joints into place")
        self._fit.setToolTip(_FIT_TIP)
        self._free = QCheckBox("Place new joints in free space")
        self._free.setToolTip(
            "A click lands on the camera-facing plane through the object centre\n"
            "instead of on the surface.  A joint is under the skin, not on it."
        )
        self._snap = QCheckBox("Snap to nearest vertex")
        for widget in (self._fit, self._free, self._snap):
            form.addRow("", widget)
        hint = QLabel("Ctrl/Cmd-drag a joint up/down to pull it in depth.")
        hint.setWordWrap(True)
        form.addRow(hint)
        self._place(box)

    def _build_display(self) -> None:
        box, form = form_group("Display")
        self._show_all = QCheckBox("Show skeletons")
        self._show_names = QCheckBox("Show joint names")
        self._show_radii = QCheckBox("Show joint thickness")
        self._deform_all = QCheckBox("Skinned models follow their skeleton")
        self._deform_all.setToolTip(
            "One switch over every skeleton: off, the model stands at rest\n"
            "whatever the bones are doing, which is how a pose is compared\n"
            "against the reference it was read from."
        )
        self._buried = QComboBox()
        for mode in Buried:
            self._buried.addItem(mode.label, mode.value)
        for widget in (self._show_all, self._show_names, self._show_radii, self._deform_all):
            form.addRow("", widget)
        form.addRow("Behind the form", self._buried)
        self._place(box)

        box, form = collapsible_group("Drawing")
        self._bone_width = SliderSpin(1.0, 10.0, 3.0, decimals=1, step=0.5)
        self._joint_radius = SliderSpin(2.0, 14.0, 5.0, decimals=1, step=0.5)
        form.addRow("Bone width", self._bone_width)
        form.addRow("Joint size", self._joint_radius)
        self._place(box)

    def _add_row(self, *buttons: QWidget) -> None:
        self._place(_row(*buttons))

    def _connect(self) -> None:
        self._delete.clicked.connect(self._delete_selected)
        self._delete_branch.clicked.connect(self._delete_branch_selected)
        self._center.clicked.connect(self._center_selected)
        self._new.clicked.connect(self.new_skeleton)
        self._humanoid.clicked.connect(self.humanoid_preset)
        self._clear.clicked.connect(self.clear_all)

        for slider in self._turn:
            slider.valueChanged.connect(self._turn_live)
            slider.valueCommitted.connect(self._turn_commit)
        self._offset.valueChanged.connect(self._move_offset)
        self._role.currentIndexChanged.connect(self._set_role)
        self._parent.currentIndexChanged.connect(self._set_parent)
        self._reset_joint.clicked.connect(lambda: self._reset_selected(branch=False))
        self._reset_branch.clicked.connect(lambda: self._reset_selected(branch=True))

        self._deform.toggled.connect(self._set_deform)
        self._reset_pose.clicked.connect(self.reset_pose)
        self._map.clicked.connect(self.map_humanoid)
        self._simplify.clicked.connect(self.simplify)
        self._to_armature.clicked.connect(self.to_armature)
        self._from_armature.clicked.connect(self.from_armature)

        self._skin_method.currentIndexChanged.connect(
            lambda i: self._apply_skinning("method", SkinMethod(self._skin_method.itemData(i)))
        )
        self._skin_influences.valueChanged.connect(
            lambda v: self._apply_skinning("influences", int(round(v)))
        )
        self._skin_heat.valueChanged.connect(lambda v: self._apply_skinning("heat", float(v)))
        self._skin_falloff.valueChanged.connect(
            lambda v: self._apply_skinning("falloff", float(v))
        )
        self._skin_facing.toggled.connect(lambda v: self._apply_skinning("facing", bool(v)))
        self._skin.clicked.connect(self.skin_to_model)
        self._unskin.clicked.connect(self.unskin)

        self._fit.toggled.connect(lambda v: self._apply("fit", v))
        self._free.toggled.connect(lambda v: self._apply("free_placement", v))
        self._snap.toggled.connect(lambda v: self._apply("snap_to_vertex", v))
        self._show_all.toggled.connect(lambda v: self._apply("show_all", v))
        self._show_names.toggled.connect(lambda v: self._apply("show_names", v))
        self._show_radii.toggled.connect(lambda v: self._apply("show_radii", v))
        self._deform_all.toggled.connect(lambda v: self._apply("deform", v))
        self._buried.currentIndexChanged.connect(
            lambda i: self._apply("buried", Buried(self._buried.itemData(i)))
        )
        self._bone_width.valueChanged.connect(lambda v: self._apply("bone_width", v))
        self._joint_radius.valueChanged.connect(lambda v: self._apply("joint_radius", v))

    # -- tool toggle ----------------------------------------------------

    def attach(self, tool, armature_tool=None) -> None:
        """Adopt the viewport's tools: the pose tool, and the armature's for its selection."""
        self._tool = tool
        self._armature_tool = armature_tool
        self.update_enabled()

    def set_posing(self, active: bool) -> None:
        with self._suppressed():
            self._toggle.setChecked(active)
        self.update_enabled()

    def _on_toggled(self, active: bool) -> None:
        if self._busy:
            return
        self.pose_toggled.emit(active)

    # -- skeletons ------------------------------------------------------

    def _add_skeleton(self, skeleton: Skeleton, text: str | None = None) -> Skeleton:
        self.state.do(
            AddItem(
                self.state.skeletons.items,
                skeleton,
                text=text or f"Add {skeleton.name}",
                channel=SKELETON,
            )
        )
        self._select(len(self.state.skeletons) - 1, 0 if skeleton.joints else -1)
        return skeleton

    def new_skeleton(self) -> Skeleton:
        """Add an empty skeleton, for a chain to be clicked into."""
        return self._add_skeleton(Skeleton(name=self.state.skeletons.next_name()))

    def humanoid_preset(self) -> Skeleton:
        """Stand a proportioned humanoid skeleton in the model's box."""
        mesh = self.state.mesh
        if mesh is None:
            height, feet = 1.8, (0.0, -0.9, 0.0)
        else:
            bounds = mesh.bounds
            height = float(bounds.size[1]) or float(bounds.diagonal) or 1.0
            feet = (float(bounds.center[0]), float(bounds.minimum[1]), float(bounds.center[2]))
        figure = build_humanoid_skeleton(height, feet, name="Humanoid")
        return self._add_skeleton(figure)

    def from_armature(self) -> None:
        """Grow a skeleton out of the armature chosen in the box."""
        index = self._armature_source.currentData()
        if index is None or not 0 <= index < len(self.state.armatures):
            return
        armature = self.state.armatures[index]
        root = None
        chosen = self._armature_tool.selected if self._armature_tool is not None else None
        if chosen is not None and chosen[0] == index:
            root = chosen[1]
        skeleton, dropped = skeleton_from_armature(armature, root)
        if not skeleton.joints:
            self.state.status_message.emit(f"{armature.name} has no nodes to grow from")
            return
        self._add_skeleton(skeleton, text=f"Skeleton from {armature.name}")
        if dropped:
            self.state.status_message.emit(
                f"{skeleton.name}: {dropped} bone{'s' if dropped != 1 else ''} closing a loop "
                "left out"
            )

    def to_armature(self) -> None:
        """Lay an armature under the selected skeleton as it is posed."""
        found = self._current_skeleton()
        if found is None:
            return
        _, skeleton = found
        armature = armature_from_skeleton(skeleton)
        armature.name = self._free_armature_name(skeleton.name)
        self.state.do(
            AddItem(
                self.state.armatures.items,
                armature,
                text=f"Armature from {skeleton.name}",
                channel=ARMATURE,
            )
        )
        self.state.status_message.emit(
            f"Laid {armature.name}: {len(armature.nodes)} nodes, {len(armature.bones)} bones"
        )

    def _free_armature_name(self, wanted: str) -> str:
        taken = {armature.name for armature in self.state.armatures}
        if wanted not in taken:
            return wanted
        count = 2
        while f"{wanted} {count}" in taken:
            count += 1
        return f"{wanted} {count}"

    def map_humanoid(self) -> int:
        """Guess the humanoid roles off the joint names; returns how many were found."""
        found = self._current_skeleton()
        if found is None:
            return 0
        _, skeleton = found
        roles = humanoid_roles(skeleton)
        if not roles:
            self.state.status_message.emit(f"{skeleton.name}: no joint name reads as a humanoid")
            return 0
        self.state.do(
            SetAttributes(
                skeleton,
                {"joints": with_roles(skeleton, roles)},
                text=f"Map {skeleton.name} to a humanoid",
                channel=SKELETON,
            )
        )
        self.state.status_message.emit(
            f"{skeleton.name}: {len(roles)} of {len(HUMANOID_ROLES)} humanoid roles found"
        )
        return len(roles)

    def simplify(self) -> int:
        """Take the detail joints out of the current skeleton; returns how many went."""
        found = self._current_skeleton()
        if found is None:
            return 0
        _, skeleton = found
        joints, counts = simplified(skeleton)
        gone = len(skeleton.joints) - len(joints)
        if not gone:
            self.state.status_message.emit(f"{skeleton.name}: nothing reads as detail")
            return 0
        if self._tool is not None:
            self._tool.selected = None
        self.state.do(
            SetAttributes(
                skeleton,
                {"joints": joints},
                text=f"Simplify {skeleton.name}",
                channel=SKELETON,
            )
        )
        kinds = ", ".join(f"{count} {kind}" for kind, count in counts.items())
        self.state.status_message.emit(
            f"{skeleton.name}: {gone} joints taken out ({kinds}); {len(joints)} left"
        )
        return gone

    def reset_pose(self) -> None:
        found = self._current_skeleton()
        if found is None or not found[1].posed:
            return
        _, skeleton = found
        self.state.do(
            SetAttributes(
                skeleton,
                {"joints": skeleton.with_pose_reset()},
                text=f"Reset {skeleton.name}",
                channel=SKELETON,
            )
        )

    def clear_all(self) -> None:
        if not len(self.state.skeletons):
            return
        self.state.do(
            ReplaceItems(self.state.skeletons.items, [], text="Clear skeletons", channel=SKELETON)
        )

    def _set_deform(self, on: bool) -> None:
        if self._busy:
            return
        found = self._current_skeleton()
        if found is None or found[1].deform == bool(on):
            return
        _, skeleton = found
        self.state.do(
            SetAttributes(
                skeleton,
                {"deform": bool(on)},
                text=f"{'Follow' if on else 'Release'} {skeleton.name}",
                channel=SKELETON,
            )
        )

    # -- skinning -------------------------------------------------------

    def skin_to_model(self):
        """Skin the active model to the current skeleton, on a thread, with a bar.

        Returns the task, or ``None`` when there was nothing to do.  The mesh
        and the skeleton are copied for the thread, so the artist can go on
        working -- and if what they do is change the skeleton, the skin made
        for the old one is turned away when it arrives.
        """
        found = self._current_skeleton()
        obj = self.state.active_object
        if found is None or obj is None:
            return None
        _, skeleton = found
        if len(skeleton.joints) < 2:
            self.state.status_message.emit(f"{skeleton.name} needs at least two joints to skin")
            return None
        busy = self.state.tasks.busy
        if busy is not None:
            self.state.status_message.emit(f"Wait for {busy.title} to finish")
            return None
        settings = replace(self.state.skeleton_settings.skinning)
        world = self.state.objects.world_matrix(obj)
        mesh = obj.world_rest(world)
        frozen = Skeleton(name=skeleton.name, joints=[replace(j) for j in skeleton.joints])
        state = self.state

        def failed(error: BaseException) -> None:
            if isinstance(error, AutoSkinError):
                state.status_message.emit(str(error))
            else:
                state.status_message.emit(f"Skinning {obj.name} failed: {error}")

        return state.tasks.run(
            f"Skinning {obj.name} to {skeleton.name}",
            lambda progress: auto_skin(mesh, frozen, settings, progress),
            done=lambda made: state.skin_object(obj, skeleton, made, world),
            failed=failed,
        )

    def unskin(self) -> None:
        found = self._current_skeleton()
        if found is None:
            return
        _, skeleton = found
        obj = self.state.object_for(skeleton)
        if obj is None or not skeleton.rig_tag:
            return
        self.state.unskin_object(obj, skeleton)

    def _apply_skinning(self, field: str, value) -> None:
        if self._busy:
            return
        setattr(self.state.skeleton_settings.skinning, field, value)
        self._sync_skinning()

    def _sync_skinning(self) -> None:
        """Show the knobs the chosen method reads, and no others."""
        method = self.state.skeleton_settings.skinning.method
        self._skin_form.setRowVisible(self._skin_heat, method is SkinMethod.HEAT)
        self._skin_form.setRowVisible(self._skin_falloff, method is SkinMethod.ENVELOPE)
        self._skin_form.setRowVisible(self._skin_influences, method is not SkinMethod.NEAREST)

    # -- edits from the view --------------------------------------------

    def apply_edit(self, edit) -> None:
        """Record a structural edit the viewport's tool worked out."""
        index, joints, text = edit
        if index < 0 or index >= len(self.state.skeletons):
            # A joint clicked with no skeleton to put it in starts one.
            self._add_skeleton(
                Skeleton(name=self.state.skeletons.next_name(), joints=list(joints)), text=text
            )
            return
        skeleton = self.state.skeletons[index]
        self.state.do(
            SetAttributes(skeleton, {"joints": joints}, text=text, channel=SKELETON)
        )

    def _rewrite(self, index: int, joints: list[Joint], text: str) -> None:
        skeleton = self.state.skeletons[index]
        self.state.do(SetAttributes(skeleton, {"joints": joints}, text=text, channel=SKELETON))

    def _delete_selected(self) -> None:
        whole = self._selected_skeleton()
        if whole is not None:
            index, skeleton = whole
            if self._tool is not None:
                self._tool.selected = None
            self.state.do(
                RemoveItem(
                    self.state.skeletons.items,
                    index,
                    text=f"Delete {skeleton.name}",
                    channel=SKELETON,
                )
            )
            return
        found = self._selected()
        if found is None:
            return
        index, position, joint = found
        if self._tool is not None:
            self._tool.selected = None
        self._rewrite(
            index, self.state.skeletons[index].without_joint(position), f"Delete {joint.name}"
        )

    def _delete_branch_selected(self) -> None:
        found = self._selected()
        if found is None:
            return
        index, position, joint = found
        if self._tool is not None:
            self._tool.selected = None
        self._rewrite(
            index,
            self.state.skeletons[index].without_branch(position),
            f"Delete {joint.name} and below",
        )

    def _center_selected(self) -> None:
        found = self._selected()
        if found is None:
            return
        index, position, _ = found
        self.center_requested.emit(self.state.skeletons[index].positions()[position])

    def _reset_selected(self, branch: bool) -> None:
        found = self._selected()
        if found is None:
            return
        index, position, joint = found
        skeleton = self.state.skeletons[index]
        chosen = [position, *(skeleton.descendants(position) if branch else [])]
        if not any(skeleton.joints[i].posed for i in chosen):
            return
        self._rewrite(
            index,
            skeleton.with_pose_reset(chosen),
            f"Reset {joint.name}{' and below' if branch else ''}",
        )

    # -- the selected joint's pose ----------------------------------------

    def _turn_live(self, _value: float) -> None:
        """Turn the joint as the slider moves, remembering where it started."""
        if self._busy:
            return
        found = self._selected()
        if found is None:
            return
        _, _, joint = found
        if self._turn_previous is None:
            self._turn_previous = (joint, joint.rotation)
        joint.rotation = normalized_rotation(
            euler_to_quat(*(slider.value() for slider in self._turn))
        )
        self.state.notify_skeleton(live=True)

    def _turn_commit(self, _value: float) -> None:
        """Record the finished slider drag as one step."""
        if self._busy:
            return
        held = self._turn_previous
        self._turn_previous = None
        found = self._selected()
        if found is None:
            return
        _, _, joint = found
        previous = held[1] if held is not None and held[0] is joint else joint.rotation
        rotation = normalized_rotation(euler_to_quat(*(slider.value() for slider in self._turn)))
        if np.allclose(rotation, previous, atol=1e-9):
            joint.rotation = previous
            self.state.notify_skeleton()
            return
        joint.rotation = rotation
        self.state.do(
            SetAttributes(
                joint,
                {"rotation": rotation},
                text=f"Turn {joint.name}",
                channel=SKELETON,
                previous={"rotation": previous},
            ),
            apply=False,
        )

    def _move_offset(self, at: tuple[float, float, float]) -> None:
        if self._busy:
            return
        found = self._selected()
        if found is None:
            return
        _, _, joint = found
        shift = tuple(float(value) / self._unit_scale for value in at)
        if all(abs(a - b) < 1e-9 for a, b in zip(joint.translation, shift, strict=True)):
            return
        self._commit_later(
            joint,
            SetAttributes(
                joint, {"translation": shift}, text=f"Move {joint.name}", channel=SKELETON
            ),
        )

    def _set_role(self, _index: int) -> None:
        if self._busy:
            return
        found = self._selected()
        if found is None:
            return
        _, _, joint = found
        role = self._role.currentData() or ""
        if role == joint.role:
            return
        self._commit_later(
            joint,
            SetAttributes(joint, {"role": role}, text=f"Role of {joint.name}", channel=SKELETON),
        )

    def _set_parent(self, _index: int) -> None:
        if self._busy:
            return
        found = self._selected()
        if found is None:
            return
        index, position, joint = found
        parent = self._parent.currentData()
        if parent is None or parent == joint.parent:
            return
        skeleton = self.state.skeletons[index]
        joints = skeleton.with_parent(position, int(parent))
        if joints[position].parent == joint.parent:
            self.state.status_message.emit(f"{joint.name} cannot hang from anything below it")
            self._fill_parents(skeleton, position, joint)
            return
        self._commit_later(
            skeleton,
            SetAttributes(
                skeleton, {"joints": joints}, text=f"Re-hang {joint.name}", channel=SKELETON
            ),
        )

    @property
    def _unit_scale(self) -> float:
        scale = float(self.state.measurement_settings.unit_scale)
        return scale if scale > 0.0 else 1.0

    # -- the list -------------------------------------------------------

    def refresh(self) -> None:
        settings = self.state.skeleton_settings
        with self._suppressed():
            self._fit.setChecked(settings.fit)
            self._free.setChecked(settings.free_placement)
            self._snap.setChecked(settings.snap_to_vertex)
            self._show_all.setChecked(settings.show_all)
            self._show_names.setChecked(settings.show_names)
            self._show_radii.setChecked(settings.show_radii)
            self._deform_all.setChecked(settings.deform)
            self._buried.setCurrentIndex(self._buried.findData(settings.buried.value))
            self._bone_width.set_value(settings.bone_width)
            self._joint_radius.set_value(settings.joint_radius)
            skinning = settings.skinning
            self._skin_method.setCurrentIndex(
                max(self._skin_method.findData(skinning.method.value), 0)
            )
            self._skin_influences.set_value(float(skinning.influences))
            self._skin_heat.set_value(skinning.heat)
            self._skin_falloff.set_value(skinning.falloff)
            self._skin_facing.setChecked(skinning.facing)
            units = self.state.measurement_settings
            self._offset.set_decimals(units.decimals)
            self._offset.set_step(
                max(float(self.state.camera.scene_radius) * units.unit_scale, 1.0) / 100.0
            )
        self._sync_skinning()
        self.refresh_list()

    def refresh_list(self) -> None:
        """Rebuild the tree from the store, keeping the tool's selection shown.

        Not under a pull, and not under a slider drag: both notify at every
        step, and rebuilding the list would yank the row out from under
        the gesture.
        """
        if self._tool is not None and self._tool.grabbed is not None:
            return
        if self._turn_previous is not None:
            return
        chosen = self._tool.selected if self._tool is not None else None
        with self._suppressed():
            self._tree.clear()
            for index, skeleton in enumerate(self.state.skeletons):
                parent = QTreeWidgetItem([skeleton.name, ""])
                parent.setFlags(
                    parent.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsUserCheckable
                )
                parent.setCheckState(
                    _NAME_COLUMN,
                    Qt.CheckState.Checked if skeleton.visible else Qt.CheckState.Unchecked,
                )
                parent.setData(_NAME_COLUMN, Qt.ItemDataRole.UserRole, (index, -1))
                self._tree.addTopLevelItem(parent)
                rows: dict[int, QTreeWidgetItem] = {}
                for position in skeleton.order():
                    joint = skeleton.joints[position]
                    row = QTreeWidgetItem([joint.name, ""])
                    row.setFlags(row.flags() | Qt.ItemFlag.ItemIsEditable)
                    row.setData(_NAME_COLUMN, Qt.ItemDataRole.UserRole, (index, position))
                    row.setIcon(_LOCK_COLUMN, lock_icon(joint.locked))
                    row.setToolTip(
                        _LOCK_COLUMN,
                        "Locked - click to unlock and drag it in the view"
                        if joint.locked
                        else "Unlocked - drag it in the view; click to lock",
                    )
                    tip = []
                    if joint.role:
                        tip.append(f"Humanoid: {role_name(joint.role)}")
                    if joint.source and joint.source != joint.name:
                        tip.append(f"In the file: {joint.source}")
                    if joint.posed:
                        tip.append("Posed")
                    if tip:
                        row.setToolTip(_NAME_COLUMN, "\n".join(tip))
                    above = rows.get(joint.parent)
                    (above if above is not None else parent).addChild(row)
                    rows[position] = row
                    if chosen == (index, position):
                        self._tree.setCurrentItem(row)
                self._expand_from(parent)
            self._fill_armatures()
        self.update_enabled()

    def _expand_from(self, item: QTreeWidgetItem) -> None:
        item.setExpanded(True)
        for child in range(item.childCount()):
            self._expand_from(item.child(child))

    def _fill_armatures(self) -> None:
        chosen = self._armature_source.currentData()
        self._armature_source.clear()
        for index, armature in enumerate(self.state.armatures):
            self._armature_source.addItem(armature.name, index)
        if chosen is not None:
            at = self._armature_source.findData(chosen)
            if at >= 0:
                self._armature_source.setCurrentIndex(at)

    def _fill_parents(self, skeleton: Skeleton, position: int, joint: Joint) -> None:
        with self._suppressed():
            self._parent.clear()
            self._parent.addItem("(root)", -1)
            below = {position, *skeleton.descendants(position)}
            for other, candidate in enumerate(skeleton.joints):
                if other not in below:
                    self._parent.addItem(candidate.name, other)
            at = self._parent.findData(joint.parent if joint.parent >= 0 else -1)
            self._parent.setCurrentIndex(max(at, 0))

    def update_enabled(self) -> None:
        """Take off the panel whatever does not apply right now."""
        found = self._selected()
        self._selection_box.setVisible(found is not None)
        for button in (self._delete_branch, self._center):
            button.setEnabled(found is not None)
        self._delete.setEnabled(found is not None or self._selected_skeleton() is not None)
        if found is not None:
            index, position, joint = found
            skeleton = self.state.skeletons[index]
            with self._suppressed():
                for slider, angle in zip(self._turn, quat_to_euler(joint.rotation), strict=True):
                    slider.set_value(angle)
                scale = self._unit_scale
                self._offset.set_value(value * scale for value in joint.translation)
                self._role.setCurrentIndex(max(self._role.findData(joint.role), 0))
            self._fill_parents(skeleton, position, joint)

        current = self._current_skeleton()
        self._skeleton_box.setVisible(current is not None)
        self._skin_box.setVisible(current is not None)
        if current is not None:
            _, skeleton = current
            wearer = self.state.object_for(skeleton) if skeleton.bound else None
            bound = wearer is not None
            with self._suppressed():
                self._deform.setChecked(skeleton.deform)
            self._deform.setVisible(bound)
            if bound and skeleton.rig_tag:
                self._bound_note.setText(
                    f"Skinned here to {wearer.name}: {len(skeleton.joints)} joints."
                )
            elif bound:
                self._bound_note.setText(
                    f"Came with {wearer.name}: {len(skeleton.joints)} joints, skinned."
                )
            elif skeleton.bound:
                self._bound_note.setText("Was skinned to a model that is not the one loaded.")
            else:
                self._bound_note.setText(
                    f"{len(skeleton.joints)} joints.  Not skinned: the model does not follow it."
                )
            self._reset_pose.setEnabled(skeleton.posed)
            self._map.setEnabled(bool(skeleton.joints))
            self._simplify.setEnabled(bool(skeleton.joints))
            self._to_armature.setEnabled(bool(skeleton.joints))
            active = self.state.active_object
            self._skin.setEnabled(active is not None and len(skeleton.joints) >= 2)
            self._skin.setText(f"Skin to {active.name}" if active is not None else "Skin to Model")
            self._unskin.setEnabled(bound and bool(skeleton.rig_tag))
        self._from_armature.setEnabled(self._armature_source.count() > 0)
        self._armature_source.setEnabled(self._armature_source.count() > 0)
        self._skeleton_form.setRowVisible(self._armature_source, len(self.state.armatures) > 0)
        self._skeleton_form.setRowVisible(self._from_armature, len(self.state.armatures) > 0)

    # -- rows -----------------------------------------------------------

    def _selected(self) -> tuple[int, int, Joint] | None:
        item = self._tree.currentItem()
        if item is None:
            return None
        found = item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        if not found:
            return None
        index, position = found
        if not 0 <= index < len(self.state.skeletons):
            return None
        skeleton = self.state.skeletons[index]
        if not 0 <= position < len(skeleton.joints):
            return None
        return index, position, skeleton.joints[position]

    def _selected_skeleton(self) -> tuple[int, Skeleton] | None:
        item = self._tree.currentItem()
        if item is None:
            return None
        found = item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        if not found or found[1] >= 0 or not 0 <= found[0] < len(self.state.skeletons):
            return None
        return found[0], self.state.skeletons[found[0]]

    def _current_skeleton(self) -> tuple[int, Skeleton] | None:
        """The skeleton the panel is about: the selected row's, else the last."""
        whole = self._selected_skeleton()
        if whole is not None:
            return whole
        found = self._selected()
        if found is not None:
            return found[0], self.state.skeletons[found[0]]
        if len(self.state.skeletons):
            last = len(self.state.skeletons) - 1
            return last, self.state.skeletons[last]
        return None

    def _select(self, index: int, position: int) -> None:
        """Highlight a row, in the tree and in the view."""
        if self._tool is not None:
            self._tool.selected = (index, position) if position >= 0 else None
        self.refresh_list()

    def _on_selection_changed(self) -> None:
        if self._busy:
            return
        found = self._selected()
        if self._tool is not None:
            self._tool.selected = None if found is None else (found[0], found[1])
        self.update_enabled()
        self.repaint_requested.emit()

    def select_joint(self, ref) -> None:
        """Highlight the row for a joint picked in the view."""
        if self._tool is not None:
            self._tool.selected = ref
        with self._suppressed():
            stack = [self._tree.topLevelItem(i) for i in range(self._tree.topLevelItemCount())]
            while stack:
                item = stack.pop()
                if item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole) == ref:
                    self._tree.setCurrentItem(item)
                    self.update_enabled()
                    return
                stack.extend(item.child(i) for i in range(item.childCount()))
        self.update_enabled()

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        if self._busy:
            return
        found = item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        if not found:
            return
        index, position = found
        if not 0 <= index < len(self.state.skeletons):
            return
        skeleton = self.state.skeletons[index]
        name = item.text(_NAME_COLUMN)
        if position < 0:
            visible = item.checkState(_NAME_COLUMN) == Qt.CheckState.Checked
            changes = {}
            if name and name != skeleton.name:
                changes["name"] = name
            if visible != skeleton.visible:
                changes["visible"] = visible
            if changes:
                verb = "Rename" if "name" in changes else ("Show" if visible else "Hide")
                self._commit_later(
                    skeleton,
                    SetAttributes(
                        skeleton, changes, text=f"{verb} {skeleton.name}", channel=SKELETON
                    ),
                )
            return
        if not 0 <= position < len(skeleton.joints):
            return
        joint = skeleton.joints[position]
        if not name or name == joint.name:
            return
        self._commit_later(
            joint,
            SetAttributes(joint, {"name": name}, text=f"Rename {joint.name}", channel=SKELETON),
        )

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        found = self._selected()
        if column != _LOCK_COLUMN or found is None:
            return
        _, _, joint = found
        locked = not joint.locked
        self._commit_later(
            joint,
            SetAttributes(
                joint,
                {"locked": locked},
                text=f"{'Lock' if locked else 'Unlock'} {joint.name}",
                channel=SKELETON,
            ),
        )

    def _commit_later(self, owner, command: SetAttributes) -> None:
        """Run a row's edit once Qt has finished delivering the current signal."""

        def commit() -> None:
            for skeleton in self.state.skeletons:
                if skeleton is owner or any(joint is owner for joint in skeleton.joints):
                    self.state.do(command)
                    return

        QTimer.singleShot(0, commit)

    # -- settings -------------------------------------------------------

    def _apply(self, field: str, value) -> None:
        if self._busy:
            return
        setattr(self.state.skeleton_settings, field, value)
        self.state.notify_skeleton()

    def shown(self) -> bool | None:
        return self.state.skeleton_settings.show_all

    def set_shown(self, on: bool) -> None:
        self._show_all.setChecked(bool(on))

