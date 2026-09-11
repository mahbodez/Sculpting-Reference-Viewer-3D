"""The armature: its nodes, the guided presets, and how the wire is drawn."""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QApplication,
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

from ...core.armature import Armature, ArmatureNode, BoneLabels, Buried, PlacedLandmark
from ...core.commands import AddItem, RemoveItem, ReplaceItems, SetAttributes
from ...core.history import ARMATURE
from ...core.landmarks import PRESETS, landmark_title
from ..icons import lock_icon
from ..widgets import PointEdit, SliderSpin, collapsible_group, form_group
from .base import Panel

_NAME_COLUMN = 0
_SIZE_COLUMN = 1
_LOCK_COLUMN = 2

#: The landmark list has its own two columns: what the point is, and whether
#: the artist put it there.
_MARK_COLUMN = 1

_TOGGLE_TIP = (
    "Lay out a wire armature under the model.\n"
    "Left click places a node and joins it to the last one; left drag on a node\n"
    "moves it, and Shift+drag changes how thick the form is there.\n"
    "Alt+drag still orbits, and Esc drops the chain without disarming the tool."
)

_GUIDE_TIP = (
    "Walk a list of anatomical landmarks instead of placing nodes by eye.\n"
    "Each one is a bump or hollow you can actually find on the model; the joints\n"
    "underneath are worked out from them, which is both less to point at and\n"
    "more accurate than guessing at the centre of a hip.\n"
    "The landmarks are kept, so nudging one moves the nodes that read it."
)

_MIRROR_TIP = (
    "Place the midline and one side; the other is reflected across the plane\n"
    "fitted through the midline landmarks.  Nineteen placements instead of\n"
    "thirty-three.  A mirrored point is drawn hollow, and correcting one in the\n"
    "Landmarks list makes it yours: the mirror never writes over it again."
)

_SIZE_TIP = (
    "How thick the form is at this node, as a radius in scene units.\n"
    "A guided preset measures it off the paired landmarks -- the two epicondyles\n"
    "that locate an elbow also say how wide it is -- so it usually arrives\n"
    "already right.  Shift+drag a node in the view to change it by hand."
)

_LANDMARK_TIP = (
    "The anatomy you pointed at, and what the nodes were worked out from.\n"
    "Move one and the joints that read it follow -- the two epicondyles that\n"
    "locate an elbow also say how wide it is, so correcting either does both.\n"
    "A hollow cross is the mirror's guess; editing one makes it yours."
)

_POSITION_TIP = (
    "Where the landmark sits, in the display unit the Measure panel is set to.\n"
    "Nudge it with the arrow keys and watch the wire follow, or type a number\n"
    "read off another view."
)

_REBUILD_TIP = (
    "Put the nodes back under the preset, worked out afresh from the landmarks.\n"
    "The armature stopped following them when you moved a node by hand; this\n"
    "hands it back, keeping the names and whatever you locked."
)

_BURIED_TIP = (
    "An armature lives inside the form, so the part behind the surface is dimmed\n"
    "rather than hidden: you can still read it, and you can still see which side\n"
    "of the skin it is on."
)


def _row(*buttons: QPushButton) -> QWidget:
    """A strip of buttons that one form row can show or hide as a unit."""
    holder = QWidget()
    layout = QHBoxLayout(holder)
    layout.setContentsMargins(0, 0, 0, 0)
    for button in buttons:
        layout.addWidget(button)
    return holder


class _NameOnlyDelegate(QStyledItemDelegate):
    """Allows in-place editing of the name column only."""

    def createEditor(self, parent, option, index):  # noqa: N802 - Qt naming
        if index.column() != _NAME_COLUMN:
            return None
        return super().createEditor(parent, option, index)


class ArmaturePanel(Panel):
    """Arms the armature tool, lists its nodes and runs the guided presets."""

    armature_toggled = Signal(bool)
    center_requested = Signal(object)
    #: The view needs repainting, but nothing about the document changed --
    #: which is the difference between highlighting a node and editing one.
    repaint_requested = Signal()

    def _build(self) -> None:
        self._tool = None
        self._previous_node: tuple[int, int] | None = None

        self._toggle = QPushButton("Armature  (R)")
        self._toggle.setCheckable(True)
        self._toggle.setToolTip(_TOGGLE_TIP)
        self._toggle.toggled.connect(self._on_toggled)
        self._add(self._toggle)

        # The list and the settings under it share the panel through a
        # splitter, so a figure with thirty nodes can be given the height to
        # show them instead of being read four rows at a time.
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

        self._build_guide()
        self._build_landmarks()
        self._build_selection()
        self._build_placement()
        self._build_display()
        self._body.addStretch(1)
        self._connect()

    def _place(self, widget: QWidget) -> QWidget:
        """Add a group below the list rather than to the panel root."""
        self._body.addWidget(widget)
        return widget

    def _build_tree(self) -> None:
        self._tree = QTreeWidget()
        self._tree.setColumnCount(3)
        self._tree.setHeaderLabels(["Node", "Size", ""])
        self._tree.setRootIsDecorated(True)
        self._tree.setAlternatingRowColors(True)
        self._tree.setItemDelegate(_NameOnlyDelegate(self._tree))
        # Double-click renames.  Qt would also start an editor on a single
        # click of an already-selected row, which here is the click that
        # toggles a padlock or joins two nodes, so that trigger is dropped.
        self._tree.setEditTriggers(
            QTreeWidget.EditTrigger.DoubleClicked | QTreeWidget.EditTrigger.EditKeyPressed
        )
        header = self._tree.header()
        header.setSectionResizeMode(_NAME_COLUMN, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(_SIZE_COLUMN, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(_LOCK_COLUMN, QHeaderView.ResizeMode.ResizeToContents)
        self._tree.itemChanged.connect(self._on_item_changed)
        self._tree.itemClicked.connect(self._on_item_clicked)
        self._tree.itemSelectionChanged.connect(self._on_selection_changed)
        self._tree.setMinimumHeight(120)
        self._splitter.addWidget(self._tree)

        self._delete = QPushButton("Delete")
        self._delete.setToolTip("Remove the selected node and the bones that reached it.")
        self._dissolve = QPushButton("Dissolve")
        self._dissolve.setToolTip(
            "Remove the selected node but keep the chain, joining the two it stood between."
        )
        self._connect_button = QPushButton("Join")
        self._connect_button.setToolTip(
            "Run a bone between the selected node and the one held before it."
        )
        self._add_row(self._delete, self._dissolve, self._connect_button)

        self._new = QPushButton("New Armature")
        self._center = QPushButton("Centre View")
        self._clear = QPushButton("Clear All")
        self._add_row(self._new, self._center, self._clear)

    def _build_guide(self) -> None:
        box, form = form_group("Guided preset")
        self._guide_form = form
        self._preset = QComboBox()
        for preset in PRESETS.values():
            self._preset.addItem(preset.name, preset.key)
        self._preset.setToolTip(_GUIDE_TIP)
        self._mirror = QCheckBox("Mirror paired landmarks")
        self._mirror.setToolTip(_MIRROR_TIP)

        self._start = QPushButton("Start")
        self._skip = QPushButton("Skip")
        self._back = QPushButton("Back")
        self._finish = QPushButton("Finish")
        self._running = _row(self._skip, self._back, self._finish)

        self._prompt = QLabel()
        self._prompt.setWordWrap(True)
        self._progress = QLabel()
        self._progress.setWordWrap(True)
        self._progress.setStyleSheet("color: #8f939b;")

        form.addRow("Preset", self._preset)
        form.addRow("", self._mirror)
        form.addRow("", self._start)
        form.addRow("", self._running)
        form.addRow("", self._prompt)
        form.addRow("", self._progress)
        self._place(box)

    def _build_landmarks(self) -> None:
        """The points the preset was built from, and the means to move them.

        Its own list rather than rows folded into the node tree: a landmark is
        not a joint, and the whole idea of the guided run is that the two are
        different things.  The group hides itself until there is something in
        it, so freehand work never sees it.
        """
        box, form = collapsible_group("Landmarks", expanded=True)
        self._landmark_box = box
        self._landmark_form = form

        self._landmark_tree = QTreeWidget()
        self._landmark_tree.setColumnCount(2)
        self._landmark_tree.setHeaderLabels(["Landmark", ""])
        self._landmark_tree.setRootIsDecorated(True)
        self._landmark_tree.setAlternatingRowColors(True)
        self._landmark_tree.setToolTip(_LANDMARK_TIP)
        self._landmark_tree.setMinimumHeight(110)
        self._landmark_tree.setEditTriggers(QTreeWidget.EditTrigger.NoEditTriggers)
        header = self._landmark_tree.header()
        header.setSectionResizeMode(_NAME_COLUMN, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(_MARK_COLUMN, QHeaderView.ResizeMode.ResizeToContents)
        self._landmark_tree.itemSelectionChanged.connect(self._on_landmark_changed)

        self._landmark_point = PointEdit()
        self._landmark_point.setToolTip(_POSITION_TIP)
        self._landmark_delete = QPushButton("Delete")
        self._landmark_delete.setToolTip(
            "Take this landmark back off the model, along with any guess mirrored from it."
        )
        self._landmark_center = QPushButton("Centre View")
        self._landmark_rebuild = QPushButton("Rebuild Nodes")
        self._landmark_rebuild.setToolTip(_REBUILD_TIP)

        form.addRow(self._landmark_tree)
        form.addRow("Position", self._landmark_point)
        self._landmark_buttons = _row(
            self._landmark_delete, self._landmark_center, self._landmark_rebuild
        )
        form.addRow("", self._landmark_buttons)
        self._place(box)

    def _build_selection(self) -> None:
        box, form = form_group("Selected node")
        self._selection_form = form
        self._size = SliderSpin(0.0, 10.0, 0.0, decimals=2, step=0.1, ceiling=1000.0)
        self._size.setToolTip(_SIZE_TIP)
        form.addRow("Thickness", self._size)
        self._place(box)
        self._selection_box = box

    def _build_placement(self) -> None:
        box, form = form_group("Placement")
        self._snap = QCheckBox("Snap to nearest vertex")
        self._free = QCheckBox("Free points (ignore the surface)")
        self._free.setToolTip(
            "A joint sits under the skin rather than on it, so once the landmarks\n"
            "are down this is usually what you want for moving nodes inwards."
        )
        form.addRow("", self._snap)
        form.addRow("", self._free)
        self._place(box)

    def _build_display(self) -> None:
        box, form = form_group("Display")
        self._show_all = QCheckBox("Show armature")
        self._show_names = QCheckBox("Show node names")
        self._show_sizes = QCheckBox("Show node thickness")
        self._show_landmarks = QCheckBox("Show landmarks")
        self._labels = QComboBox()
        for mode in BoneLabels:
            self._labels.addItem(mode.label, mode.value)
        self._buried = QComboBox()
        for mode in Buried:
            self._buried.addItem(mode.label, mode.value)
        self._buried.setToolTip(_BURIED_TIP)
        for widget in (self._show_all, self._show_names, self._show_sizes, self._show_landmarks):
            form.addRow("", widget)
        form.addRow("Bone lengths", self._labels)
        form.addRow("Behind the form", self._buried)
        self._place(box)

        box, form = collapsible_group("Drawing")
        self._bone_width = SliderSpin(1.0, 10.0, 2.5, decimals=1, step=0.5)
        self._node_radius = SliderSpin(2.0, 14.0, 5.0, decimals=1, step=0.5)
        form.addRow("Bone width", self._bone_width)
        form.addRow("Node size", self._node_radius)
        self._place(box)

    def _add_row(self, *buttons: QPushButton) -> None:
        self._place(_row(*buttons))

    def _connect(self) -> None:
        self._delete.clicked.connect(self._delete_selected)
        self._dissolve.clicked.connect(self._dissolve_selected)
        self._connect_button.clicked.connect(self._join_selected)
        self._new.clicked.connect(self.new_armature)
        self._center.clicked.connect(self._center_selected)
        self._clear.clicked.connect(self.clear_all)

        self._start.clicked.connect(self.start_guide)
        self._skip.clicked.connect(self._skip_landmark)
        self._back.clicked.connect(self._back_landmark)
        self._finish.clicked.connect(self.end_guide)
        self._mirror.toggled.connect(lambda v: self._apply("mirror", v))

        self._landmark_point.valueChanged.connect(self._move_landmark)
        self._landmark_delete.clicked.connect(self._delete_landmark)
        self._landmark_center.clicked.connect(self._center_landmark)
        self._landmark_rebuild.clicked.connect(self._rebuild_from_landmarks)

        self._size.valueCommitted.connect(self._resize_selected)
        self._snap.toggled.connect(lambda v: self._apply("snap_to_vertex", v))
        self._free.toggled.connect(lambda v: self._apply("free_placement", v))
        self._show_all.toggled.connect(lambda v: self._apply("show_all", v))
        self._show_names.toggled.connect(lambda v: self._apply("show_names", v))
        self._show_sizes.toggled.connect(lambda v: self._apply("show_sizes", v))
        self._show_landmarks.toggled.connect(lambda v: self._apply("show_landmarks", v))
        self._labels.currentIndexChanged.connect(
            lambda i: self._apply("labels", BoneLabels(self._labels.itemData(i)))
        )
        self._buried.currentIndexChanged.connect(
            lambda i: self._apply("buried", Buried(self._buried.itemData(i)))
        )
        self._bone_width.valueChanged.connect(lambda v: self._apply("bone_width", v))
        self._node_radius.valueChanged.connect(lambda v: self._apply("node_radius", v))

    # -- tool toggle ----------------------------------------------------

    def attach(self, tool) -> None:
        """Adopt the viewport's tool, which is where the guided run lives."""
        self._tool = tool
        self.update_enabled()

    def set_armaturing(self, active: bool) -> None:
        """Reflect the tool state without re-emitting the toggle."""
        with self._suppressed():
            self._toggle.setChecked(active)
        self.update_enabled()

    def _on_toggled(self, active: bool) -> None:
        if self._busy:
            return
        self.armature_toggled.emit(active)

    # -- the guided walk -------------------------------------------------

    def new_armature(self) -> Armature:
        """Add an empty armature and select it."""
        armature = Armature(name=self.state.armatures.next_name())
        self.state.do(
            AddItem(
                self.state.armatures.items,
                armature,
                text=f"Add {armature.name}",
                channel=ARMATURE,
            )
        )
        return armature

    def start_guide(self) -> None:
        """Begin a preset run against a fresh armature."""
        if self._tool is None:
            return
        preset = self._preset.currentData() or ""
        armature = self.new_armature()
        armature.preset = preset
        armature.derived = True
        armature.name = PRESETS[preset].name if preset in PRESETS else armature.name
        self._tool.start_guide(preset, len(self.state.armatures) - 1)
        self.armature_toggled.emit(True)
        self.state.notify_armature()

    def end_guide(self) -> None:
        if self._tool is None:
            return
        self._tool.end_guide()
        self.state.notify_armature()

    def _skip_landmark(self) -> None:
        armature = self._guided_armature()
        if self._tool is None or armature is None:
            return
        self._tool.skip(armature, self.state.armature_settings)
        self.state.notify_armature()

    def _back_landmark(self) -> None:
        """Take back the landmark before this one and ask for it again."""
        armature = self._guided_armature()
        if self._tool is None or armature is None:
            return
        settings = self.state.armature_settings
        key = self._tool.back(armature, settings)
        if key is None:
            self.state.notify_armature()
            return
        landmarks = [entry for entry in armature.landmarks if entry.key != key]
        nodes, bones, landmarks = self._tool.derive(armature, landmarks, settings)
        self.state.do(
            SetAttributes(
                armature,
                {"nodes": nodes, "bones": bones, "landmarks": landmarks},
                text="Take back a landmark",
                channel=ARMATURE,
            )
        )

    def _guided_armature(self) -> Armature | None:
        run = self._tool.guide if self._tool is not None else None
        if run is None or not 0 <= run.armature < len(self.state.armatures):
            return None
        return self.state.armatures[run.armature]

    # -- edits ----------------------------------------------------------

    def apply_edit(self, edit) -> None:
        """Record an edit the viewport's tool worked out."""
        index, nodes, bones, landmarks, text = edit
        if not 0 <= index < len(self.state.armatures):
            return
        armature = self.state.armatures[index]
        self.state.do(
            SetAttributes(
                armature,
                {"nodes": nodes, "bones": bones, "landmarks": landmarks},
                text=text,
                channel=ARMATURE,
            )
        )

    def _restructure(self, text: str, nodes, bones) -> None:
        """Write a structural change, detaching the armature from its preset."""
        found = self._selected()
        if found is None:
            return
        index, _, _ = found
        armature = self.state.armatures[index]
        changes = {"nodes": nodes, "bones": bones}
        if armature.derived:
            changes["derived"] = False
        self.state.do(SetAttributes(armature, changes, text=text, channel=ARMATURE))

    def _delete_selected(self) -> None:
        """Remove the selected node, or the whole armature when its row is picked."""
        whole = self._selected_armature()
        if whole is not None:
            index, armature = whole
            self.end_guide()
            self.state.do(
                RemoveItem(
                    self.state.armatures.items,
                    index,
                    text=f"Delete {armature.name}",
                    channel=ARMATURE,
                )
            )
            return
        found = self._selected()
        if found is None:
            return
        index, position, node = found
        armature = self.state.armatures[index]
        self._restructure(f"Delete {node.name}", *armature.without_node(position))

    def _dissolve_selected(self) -> None:
        found = self._selected()
        if found is None:
            return
        index, position, node = found
        armature = self.state.armatures[index]
        self._restructure(f"Dissolve {node.name}", *armature.dissolved(position))

    def _join_selected(self) -> None:
        """Run a bone between the row selected now and the node held before it."""
        found = self._selected()
        if found is not None:
            self._join_to(self._previous_node, (found[0], found[1]))

    def _join_to(self, anchor, handle) -> None:
        """Join two nodes of one armature, if they are two and they are one armature."""
        if anchor is None or handle is None or anchor == handle:
            return
        index, position = handle
        if anchor[0] != index or not 0 <= index < len(self.state.armatures):
            return
        armature = self.state.armatures[index]
        if not (0 <= anchor[1] < len(armature.nodes) and 0 <= position < len(armature.nodes)):
            return
        nodes, bones = armature.with_bone(anchor[1], position)
        if len(bones) == len(armature.bones):
            return
        name = armature.nodes[position].name
        changes = {"nodes": nodes, "bones": bones}
        if armature.derived:
            changes["derived"] = False
        self.state.do(
            SetAttributes(armature, changes, text=f"Join {name}", channel=ARMATURE)
        )

    def _resize_selected(self, value: float) -> None:
        if self._busy:
            return
        found = self._selected()
        if found is None:
            return
        _, _, node = found
        if node.size == float(value):
            return
        self._commit_later(
            node,
            SetAttributes(
                node, {"size": float(value)}, text=f"Resize {node.name}", channel=ARMATURE
            ),
        )

    def clear_all(self) -> None:
        if not len(self.state.armatures):
            return
        self.end_guide()
        self.state.do(
            ReplaceItems(
                self.state.armatures.items, [], text="Clear armatures", channel=ARMATURE
            )
        )

    def _center_selected(self) -> None:
        found = self._selected()
        if found is not None:
            self.center_requested.emit(found[2].point)

    # -- the landmarks ---------------------------------------------------

    def _write_landmarks(
        self, index: int, landmarks: list[PlacedLandmark], text: str
    ) -> None:
        """Record an edited landmark list, re-deriving the wire if it still follows.

        An armature the artist has taken over keeps the nodes they made: the
        landmarks stay a record of where the anatomy is, and Rebuild Nodes is
        how that is given up deliberately rather than by a stray arrow key.
        """
        armature = self.state.armatures[index]
        changes: dict = {"landmarks": landmarks}
        if armature.derived and self._tool is not None:
            nodes, bones, landmarks = self._tool.derive(
                armature, landmarks, self.state.armature_settings
            )
            changes = {"nodes": nodes, "bones": bones, "landmarks": landmarks}
        self.state.do(SetAttributes(armature, changes, text=text, channel=ARMATURE))

    def _move_landmark(self, at: tuple[float, float, float]) -> None:
        if self._busy:
            return
        found = self._selected_landmark()
        if found is None:
            return
        index, landmark = found
        scene = tuple(value / self._unit_scale for value in at)
        if all(abs(a - b) < 1e-9 for a, b in zip(landmark.at, scene, strict=True)):
            return
        armature = self.state.armatures[index]
        self._write_landmarks(
            index,
            armature.with_landmark_at(landmark.key, scene),
            f"Move {landmark_title(armature, landmark.key)}",
        )

    def _delete_landmark(self) -> None:
        found = self._selected_landmark()
        if found is None:
            return
        index, landmark = found
        armature = self.state.armatures[index]
        title = landmark_title(armature, landmark.key)
        if self._tool is not None:
            self._tool.selected_landmark = None
        self._write_landmarks(
            index,
            armature.without_landmarks(landmark.key, *self._guesses_from(armature, landmark.key)),
            f"Delete {title}",
        )

    def _center_landmark(self) -> None:
        found = self._selected_landmark()
        if found is not None:
            self.center_requested.emit(found[1].point)

    def _rebuild_from_landmarks(self) -> None:
        """Put the nodes back under the preset the landmarks describe."""
        found = self._landmark_armature()
        if found is None or self._tool is None:
            return
        index, armature = found
        nodes, bones, landmarks = self._tool.derive(
            armature, list(armature.landmarks), self.state.armature_settings
        )
        self.state.do(
            SetAttributes(
                armature,
                {"nodes": nodes, "bones": bones, "landmarks": landmarks, "derived": True},
                text=f"Rebuild {armature.name} from its landmarks",
                channel=ARMATURE,
            )
        )

    @staticmethod
    def _guesses_from(armature: Armature, key: str) -> list[str]:
        """The mirrored landmarks reflected from ``key``, which it anchors."""
        preset = PRESETS.get(armature.preset)
        if preset is None:
            return []
        return [
            entry.key
            for entry in armature.landmarks
            if entry.mirrored
            and (spec := preset.landmark(entry.key)) is not None
            and spec.mirror_of == key
        ]

    @staticmethod
    def _ordered(armature: Armature) -> list[PlacedLandmark]:
        """The landmarks in the preset's own order, top of the figure down.

        Placement order would do just as well for a run that went straight
        through, but a skipped point placed later, and every mirrored one,
        arrive at the end -- so the list would stop reading as a figure.
        """
        preset = PRESETS.get(armature.preset)
        if preset is None:
            return list(armature.landmarks)
        order = {entry.key: position for position, entry in enumerate(preset.landmarks)}
        return sorted(armature.landmarks, key=lambda e: order.get(e.key, len(order)))

    @property
    def _unit_scale(self) -> float:
        """The multiplier the position boxes are read and written through."""
        scale = float(self.state.measurement_settings.unit_scale)
        return scale if scale > 0.0 else 1.0

    # -- the list -------------------------------------------------------

    def refresh(self) -> None:
        settings = self.state.armature_settings
        with self._suppressed():
            self._mirror.setChecked(settings.mirror)
            self._snap.setChecked(settings.snap_to_vertex)
            self._free.setChecked(settings.free_placement)
            self._show_all.setChecked(settings.show_all)
            self._show_names.setChecked(settings.show_names)
            self._show_sizes.setChecked(settings.show_sizes)
            self._show_landmarks.setChecked(settings.show_landmarks)
            self._labels.setCurrentIndex(self._labels.findData(settings.labels.value))
            self._buried.setCurrentIndex(self._buried.findData(settings.buried.value))
            self._bone_width.set_value(settings.bone_width)
            self._node_radius.set_value(settings.node_radius)
            # The position boxes speak the Measure panel's unit, and step by a
            # hundredth of the model: an arrow key should be a nudge whether
            # the figure is two units tall or two hundred.
            units = self.state.measurement_settings
            self._landmark_point.set_decimals(units.decimals)
            self._landmark_point.set_step(
                max(float(self.state.camera.scene_radius) * units.unit_scale, 1.0) / 100.0
            )
        self.refresh_list()

    def refresh_list(self) -> None:
        """Rebuild the tree from the store, keeping the tool's selection shown.

        A node being dragged notifies on every mouse move, and rebuilding the
        list that often is both wasted work and a way to yank the selection out
        from under the gesture, so the drag is left to settle first.
        """
        if self._tool is not None and (
            self._tool.grabbed_handle is not None or self._tool.grabbed_landmark is not None
        ):
            return
        units = self.state.measurement_settings
        chosen = self._tool.selected if self._tool is not None else None
        with self._suppressed():
            self._tree.clear()
            for index, armature in enumerate(self.state.armatures):
                parent = QTreeWidgetItem([armature.name, "", ""])
                parent.setFlags(
                    parent.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsUserCheckable
                )
                parent.setCheckState(
                    _NAME_COLUMN,
                    Qt.CheckState.Checked if armature.visible else Qt.CheckState.Unchecked,
                )
                parent.setData(_NAME_COLUMN, Qt.ItemDataRole.UserRole, (index, -1))
                # Into the tree before its children: a row whose parent is not
                # in the model yet can be made current but cannot be selected,
                # so the node picked in the view would never light up here.
                self._tree.addTopLevelItem(parent)
                for position, node in enumerate(armature.nodes):
                    child = QTreeWidgetItem([node.name, units.format_length(node.size), ""])
                    child.setFlags(child.flags() | Qt.ItemFlag.ItemIsEditable)
                    child.setTextAlignment(
                        _SIZE_COLUMN, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                    child.setData(_NAME_COLUMN, Qt.ItemDataRole.UserRole, (index, position))
                    child.setIcon(_LOCK_COLUMN, lock_icon(node.locked))
                    child.setToolTip(
                        _LOCK_COLUMN,
                        "Locked - click to unlock and drag it in the view"
                        if node.locked
                        else "Unlocked - drag it in the view; click to lock",
                    )
                    if node.role:
                        child.setToolTip(_NAME_COLUMN, f"From the preset: {node.role}")
                    parent.addChild(child)
                    if chosen == (index, position):
                        self._tree.setCurrentItem(child)
                parent.setExpanded(True)
        self.refresh_landmarks()
        self.update_enabled()

    def refresh_landmarks(self) -> None:
        """Rebuild the landmark list, keeping the row the panel is editing."""
        chosen = self._tool.selected_landmark if self._tool is not None else None
        matched = False
        with self._suppressed():
            self._landmark_tree.clear()
            for index, armature in enumerate(self.state.armatures):
                if not armature.landmarks:
                    continue
                preset = PRESETS.get(armature.preset)
                parent = QTreeWidgetItem([armature.name, ""])
                parent.setData(_NAME_COLUMN, Qt.ItemDataRole.UserRole, (index, ""))
                # In the tree before its children, so that restoring the
                # selection below really does select: a row whose parent has
                # not been added yet is not in the model to be picked.
                self._landmark_tree.addTopLevelItem(parent)
                for landmark in self._ordered(armature):
                    entry = preset.landmark(landmark.key) if preset is not None else None
                    child = QTreeWidgetItem(
                        [
                            entry.title if entry is not None else landmark.key,
                            "guess" if landmark.mirrored else "",
                        ]
                    )
                    child.setData(
                        _NAME_COLUMN, Qt.ItemDataRole.UserRole, (index, landmark.key)
                    )
                    if entry is not None:
                        child.setToolTip(_NAME_COLUMN, entry.hint)
                    if landmark.mirrored:
                        child.setToolTip(
                            _MARK_COLUMN,
                            "Reflected across the median plane rather than placed.\n"
                            "Move it and it becomes yours.",
                        )
                    parent.addChild(child)
                    if chosen == (index, landmark.key):
                        self._landmark_tree.setCurrentItem(child)
                        matched = True
                parent.setExpanded(True)
        # A landmark that was deleted, undone or renumbered out from under the
        # selection leaves a highlight in the view pointing at nothing.
        if not matched and self._tool is not None:
            self._tool.selected_landmark = None

    def update_enabled(self) -> None:
        """Take off the panel whatever does not apply right now."""
        guiding = self._tool is not None and self._tool.guiding
        for widget in (self._running, self._prompt, self._progress):
            self._guide_form.setRowVisible(widget, guiding)
        for widget in (self._preset, self._mirror, self._start):
            self._guide_form.setRowVisible(widget, not guiding)

        found = self._selected()
        self._selection_box.setVisible(found is not None)
        for button in (self._dissolve, self._connect_button, self._center):
            button.setEnabled(found is not None)
        self._delete.setEnabled(found is not None or self._selected_armature() is not None)
        if found is not None:
            with self._suppressed():
                self._size.set_value(found[2].size)
        self._update_landmarks_enabled()
        if guiding:
            self._refresh_prompt()

    def _update_landmarks_enabled(self) -> None:
        """Show the landmark group only once there are landmarks to show."""
        self._landmark_box.setVisible(self._landmark_tree.topLevelItemCount() > 0)
        found = self._selected_landmark()
        self._landmark_form.setRowVisible(self._landmark_point, found is not None)
        for button in (self._landmark_delete, self._landmark_center):
            button.setEnabled(found is not None)
        # Rebuilding is only ever offered where it would change something: an
        # armature that has been taken over by hand and has a preset to go
        # back to.  One that still follows its landmarks is already rebuilt.
        armature = self._landmark_armature()
        self._landmark_rebuild.setEnabled(
            armature is not None
            and not armature[1].derived
            and armature[1].preset in PRESETS
        )
        if found is not None:
            scale = self._unit_scale
            with self._suppressed():
                self._landmark_point.set_value(value * scale for value in found[1].at)

    def _refresh_prompt(self) -> None:
        armature = self._guided_armature()
        if armature is None or self._tool is None:
            return
        settings = self.state.armature_settings
        placed, wanted = self._tool.progress(armature, settings)
        entry = self._tool.current(armature, settings)
        if entry is None:
            self._prompt.setText("Every landmark is placed.")
            self._progress.setText(f"{placed} of {wanted}. Press Finish to keep the armature.")
            return
        self._prompt.setText(f"<b>{entry.title}</b><br/>{entry.hint}")
        self._progress.setText(f"Landmark {placed + 1} of {wanted}")

    # -- rows -----------------------------------------------------------

    def _selected(self) -> tuple[int, int, ArmatureNode] | None:
        """The node the selected row stands for, if the row is a node at all."""
        item = self._tree.currentItem()
        if item is None:
            return None
        found = item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        if not found:
            return None
        index, position = found
        if not 0 <= index < len(self.state.armatures):
            return None
        armature = self.state.armatures[index]
        if not 0 <= position < len(armature.nodes):
            return None
        return index, position, armature.nodes[position]

    def _selected_armature(self) -> tuple[int, Armature] | None:
        """The armature the selected row stands for, when the row is not a node."""
        item = self._tree.currentItem()
        if item is None:
            return None
        found = item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        if not found or found[1] >= 0 or not 0 <= found[0] < len(self.state.armatures):
            return None
        return found[0], self.state.armatures[found[0]]

    def _selected_landmark(self) -> tuple[int, PlacedLandmark] | None:
        """The landmark the highlighted row stands for, if the row is one."""
        found = self._landmark_row()
        if found is None or not found[1]:
            return None
        index, key = found
        landmark = self.state.armatures[index].landmark_for(key)
        return None if landmark is None else (index, landmark)

    def _landmark_armature(self) -> tuple[int, Armature] | None:
        """Which armature the landmark list is pointing into, row or heading."""
        found = self._landmark_row()
        if found is None:
            return None
        return found[0], self.state.armatures[found[0]]

    def _landmark_row(self) -> tuple[int, str] | None:
        item = self._landmark_tree.currentItem()
        if item is None or not item.isSelected():
            return None
        found = item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        if not found or not 0 <= found[0] < len(self.state.armatures):
            return None
        return found[0], found[1]

    def _on_landmark_changed(self) -> None:
        """Follow the highlighted landmark, and say which one it is in the view."""
        if self._busy:
            return
        found = self._selected_landmark()
        if self._tool is not None:
            self._tool.selected_landmark = None if found is None else (found[0], found[1].key)
        self.update_enabled()
        self.repaint_requested.emit()

    def _on_selection_changed(self) -> None:
        """Follow the highlighted row, without rebuilding the list underneath it.

        Going through ``notify_armature`` here would clear and refill the tree
        on every arrow-key press -- which also destroys the editor a
        double-click has just opened, so renaming would never survive.
        """
        if self._busy:
            return
        found = self._selected()
        if self._tool is not None:
            self._previous_node = self._tool.selected
            self._tool.selected = None if found is None else (found[0], found[1])
        self.update_enabled()
        self.repaint_requested.emit()

    def select_node(self, handle) -> None:
        """Highlight the row for a node picked in the view."""
        if self._tool is not None:
            self._previous_node = self._tool.selected
            self._tool.selected = handle
        with self._suppressed():
            for parent in range(self._tree.topLevelItemCount()):
                top = self._tree.topLevelItem(parent)
                for child in range(top.childCount()):
                    item = top.child(child)
                    if item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole) == handle:
                        self._tree.setCurrentItem(item)
                        self.update_enabled()
                        return
        self.update_enabled()

    def select_landmark(self, ref) -> None:
        """Highlight the row for a landmark picked in the view."""
        if self._tool is not None:
            self._tool.selected_landmark = ref
        with self._suppressed():
            for parent in range(self._landmark_tree.topLevelItemCount()):
                top = self._landmark_tree.topLevelItem(parent)
                for child in range(top.childCount()):
                    item = top.child(child)
                    if item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole) == ref:
                        self._landmark_tree.setCurrentItem(item)
                        self.update_enabled()
                        return
        self.update_enabled()

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        """Commit a renamed or re-checked row, if anything actually changed."""
        if self._busy:
            return
        found = item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        if not found:
            return
        index, position = found
        if not 0 <= index < len(self.state.armatures):
            return
        armature = self.state.armatures[index]
        name = item.text(_NAME_COLUMN)
        if position < 0:
            visible = item.checkState(_NAME_COLUMN) == Qt.CheckState.Checked
            changes = {}
            if name and name != armature.name:
                changes["name"] = name
            if visible != armature.visible:
                changes["visible"] = visible
            if changes:
                verb = "Rename" if "name" in changes else ("Show" if visible else "Hide")
                self._commit_later(
                    armature,
                    SetAttributes(
                        armature, changes, text=f"{verb} {armature.name}", channel=ARMATURE
                    ),
                )
            return
        if not 0 <= position < len(armature.nodes):
            return
        node = armature.nodes[position]
        if not name or name == node.name:
            return
        self._commit_later(
            node,
            SetAttributes(node, {"name": name}, text=f"Rename {node.name}", channel=ARMATURE),
        )

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        found = self._selected()
        if QApplication.keyboardModifiers() & Qt.KeyboardModifier.ControlModifier:
            if found is not None:
                self._join_to(self._previous_node, (found[0], found[1]))
            return
        if column != _LOCK_COLUMN or found is None:
            return
        _, _, node = found
        locked = not node.locked
        self._commit_later(
            node,
            SetAttributes(
                node,
                {"locked": locked},
                text=f"{'Lock' if locked else 'Unlock'} {node.name}",
                channel=ARMATURE,
            ),
        )

    def _commit_later(self, owner, command: SetAttributes) -> None:
        """Run a row's edit once Qt has finished delivering the current signal.

        Committing rebuilds the tree, and destroying the very item whose signal
        is still being delivered takes the application down with it, so the
        edit is queued rather than applied in the slot.
        """

        def commit() -> None:
            for armature in self.state.armatures:
                if armature is owner or any(node is owner for node in armature.nodes):
                    self.state.do(command)
                    return

        QTimer.singleShot(0, commit)

    # -- settings -------------------------------------------------------

    def _apply(self, field: str, value) -> None:
        if self._busy:
            return
        setattr(self.state.armature_settings, field, value)
        self.state.notify_armature()
