"""The forms: the presets and the freeform that build them, their stages, and the clay."""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)

from ...core.armature import PlacedLandmark
from ...core.commands import AddItem, RemoveItem, ReplaceItems, SetAttributes
from ...core.forms import (
    FORM_PRESETS,
    FREEFORM,
    FREEFORM_NAME,
    FormFill,
    PrimaryForm,
    form_landmark_title,
    form_spec,
    freeform_landmark,
)
from ...core.history import FORMS
from ...core.landmarks import Landmark, Side
from ..widgets import ColorButton, PointEdit, SliderSpin, form_group
from .base import Panel

_NAME_COLUMN = 0
#: The second column says whether the artist put a landmark there or the
#: mirror guessed it.
_MARK_COLUMN = 1

_TOGGLE_TIP = (
    "Build the simple masses of a figure in clay, over the model.\n"
    "Pick a form, press Start, and point at the landmarks it asks for -- or,\n"
    "for a freeform, at whatever landmarks you choose; the form is worked out\n"
    "from them and grows as they go down.  Left drag on a landmark moves it\n"
    "and the clay follows.  Alt+drag still orbits."
)

_PRESET_TIP = (
    "Which form to build.\n"
    "The pelvis is a bucket with its front corner chipped off, the ribcage an\n"
    "egg with the arch chipped out of its front, and the head a wedge that is\n"
    "given its width, its cranium and its jaw in turn.  A freeform is the hull\n"
    "of any landmarks you care to put down, named as you go: a hand, a knee, a\n"
    "breast, a scapula, a muscle -- the presets are special cases of it."
)

_FORM_NAME_TIP = "What to call the freeform.  Leave it blank for a numbered one."

_FILL_TIP = (
    "How a freeform's clay is fitted to its landmarks.\n"
    "Faceted is the convex hull of the points as it comes, planes meeting at\n"
    "edges, which is right for bone.  Smooth bows each face of that hull out\n"
    "into a cubic patch between the points, for muscle and fat.  Either way\n"
    "the clay passes through every landmark."
)

_POINT_NAME_TIP = (
    "What to call the landmark the next click lays down.  A name already used\n"
    "on that side is numbered.  Landmarks can be renamed in the list below."
)

_SIDE_TIP = (
    "Which side of the figure the next landmark is on.  It stays as set from\n"
    "one landmark to the next until you change it.  A left or right landmark\n"
    "is mirrored to the other side when the mirror is on and enough of the\n"
    "midline is down to fit a plane through; a landmark placed on both sides\n"
    "by hand is a pair, and the symmetric build averages the two."
)

_FREE_TIP = (
    "Place and drag a freeform's landmarks anywhere in space rather than on\n"
    "the model -- inside it, for a mass the skin only hints at.  They land on\n"
    "the plane facing the camera through the object centre.  The presets\n"
    "ignore this: their landmarks are anatomy on the skin."
)

_MIRROR_TIP = (
    "Place the midline and one side; the other is reflected across the plane\n"
    "fitted through the midline landmarks.  A mirrored point is drawn hollow,\n"
    "and correcting one makes it yours: the mirror never writes over it again."
)

_SYMMETRIC_TIP = (
    "Build every form from its landmarks made symmetric about the median plane:\n"
    "the midline points dropped onto it, each pair averaged across it.  The\n"
    "pelvis, the ribcage and the skull are bone, and bone is symmetric to within\n"
    "less than a click's error.  The landmarks stay where you put them."
)

_STAGE_TIP = (
    "Which stage of the making to show.  A head is built up in stages -- the\n"
    "wedge, its width, the cranium, the jaw, the nose -- and every stage is kept, so this\n"
    "scrubs back through them.  At the right-hand end the form shows every\n"
    "stage it has, including ones that arrive later."
)

_LANDMARK_TIP = (
    "The anatomy you pointed at, and what the form was worked out from.\n"
    "Move one and the clay follows.  A hollow cross is the mirror's guess;\n"
    "editing one makes it yours."
)

_POSITION_TIP = (
    "Where the landmark sits, in the display unit the Measure panel is set to.\n"
    "Nudge it with the arrow keys and watch the form follow."
)

_GHOST_TIP = (
    "Draw the model see-through, so the clay laid inside it can be read.\n"
    "The same switch as the one in the Shading panel."
)

_SMOOTH_TIP = (
    "Facets turning by less than this many degrees are shaded as one curve, so\n"
    "a bucket sampled in forty flats reads as a bucket while its rim, and the\n"
    "chip off its front, stay as hard as they are.  Zero shows every facet."
)


def _row(*buttons: QPushButton) -> QWidget:
    """A strip of buttons that one form row can show or hide as a unit."""
    holder = QWidget()
    layout = QHBoxLayout(holder)
    layout.setContentsMargins(0, 0, 0, 0)
    for button in buttons:
        layout.addWidget(button)
    return holder


class FormsPanel(Panel):
    """Arms the forms tool, runs the guided presets and lists what they built."""

    form_toggled = Signal(bool)
    center_requested = Signal(object)
    #: The view needs repainting, but nothing about the document changed.
    repaint_requested = Signal()

    def _build(self) -> None:
        self._tool = None

        self._toggle = QPushButton("Forms  (G)")
        self._toggle.setCheckable(True)
        self._toggle.setToolTip(_TOGGLE_TIP)
        self._toggle.toggled.connect(self._on_toggled)
        self._add(self._toggle)

        self._build_guide()
        self._build_stages()
        self._build_list()
        self._build_placement()
        self._build_display()
        self._add_stretch()
        self._connect()

    def _build_guide(self) -> None:
        box, form = form_group("Build")
        self._guide_form = form
        self._preset = QComboBox()
        for preset in FORM_PRESETS.values():
            self._preset.addItem(preset.name, preset.key)
        self._preset.addItem(FREEFORM_NAME, FREEFORM)
        self._preset.setToolTip(_PRESET_TIP)
        self._form_name = QLineEdit()
        self._form_name.setPlaceholderText("Form")
        self._form_name.setToolTip(_FORM_NAME_TIP)
        self._fill = QComboBox()
        for fill in FormFill:
            self._fill.addItem(fill.label, fill.value)
        self._fill.setToolTip(_FILL_TIP)
        self._mirror = QCheckBox("Mirror paired landmarks")
        self._mirror.setToolTip(_MIRROR_TIP)
        self._symmetric = QCheckBox("Symmetrical forms")
        self._symmetric.setToolTip(_SYMMETRIC_TIP)

        self._start = QPushButton("Start")
        self._skip = QPushButton("Skip")
        self._back = QPushButton("Back")
        self._finish = QPushButton("Finish")
        self._running = _row(self._skip, self._back, self._finish)

        # A freeform run asks for nothing; these say what the next click
        # lays down.
        self._point_name = QLineEdit()
        self._point_name.setToolTip(_POINT_NAME_TIP)
        self._point_side = QComboBox()
        for side, label in ((Side.CENTRE, "Centre"), (Side.LEFT, "Left"), (Side.RIGHT, "Right")):
            self._point_side.addItem(label, side.value)
        self._point_side.setToolTip(_SIDE_TIP)

        self._prompt = QLabel()
        self._prompt.setWordWrap(True)
        self._progress = QLabel()
        self._progress.setWordWrap(True)
        self._progress.setStyleSheet("color: #8f939b;")

        form.addRow("Form", self._preset)
        form.addRow("Name", self._form_name)
        form.addRow("Fill", self._fill)
        form.addRow("", self._mirror)
        form.addRow("", self._symmetric)
        form.addRow("", self._start)
        form.addRow("", self._running)
        form.addRow("Landmark", self._point_name)
        form.addRow("Side", self._point_side)
        form.addRow("", self._prompt)
        form.addRow("", self._progress)
        self._add(box)

    def _build_stages(self) -> None:
        box, form = form_group("Stages")
        self._stage_box = box
        self._stage = QSlider(Qt.Orientation.Horizontal)
        self._stage.setToolTip(_STAGE_TIP)
        self._stage.setRange(0, 0)
        self._stage.setPageStep(1)
        self._stage_label = QLabel()
        self._stage_label.setWordWrap(True)
        self._stage_label.setStyleSheet("color: #8f939b;")
        form.addRow("Stage", self._stage)
        form.addRow("", self._stage_label)
        self._add(box)

    def _build_list(self) -> None:
        self._tree = QTreeWidget()
        self._tree.setColumnCount(2)
        self._tree.setHeaderLabels(["Form", ""])
        self._tree.setRootIsDecorated(True)
        self._tree.setAlternatingRowColors(True)
        self._tree.setToolTip(_LANDMARK_TIP)
        self._tree.setMinimumHeight(140)
        self._tree.setEditTriggers(
            QTreeWidget.EditTrigger.DoubleClicked | QTreeWidget.EditTrigger.EditKeyPressed
        )
        header = self._tree.header()
        header.setSectionResizeMode(_NAME_COLUMN, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(_MARK_COLUMN, QHeaderView.ResizeMode.ResizeToContents)
        self._tree.itemChanged.connect(self._on_item_changed)
        self._tree.itemSelectionChanged.connect(self._on_selection_changed)
        self._add(self._tree)

        self._delete = QPushButton("Delete")
        self._delete.setToolTip(
            "Take the selected landmark back off the model, along with any guess\n"
            "mirrored from it -- or delete the whole form when its row is selected."
        )
        self._append = QPushButton("Append Landmarks")
        self._append.setToolTip(
            "Take up the selected freeform again and add landmarks to it: the\n"
            "next click lays down whatever is named above, as when it was started.\n"
            "A preset's landmarks are fixed, so only a freeform can be appended to."
        )
        self._center = QPushButton("Centre View")
        self._clear = QPushButton("Clear All")
        self._add(self._append)
        self._add(_row(self._delete, self._center, self._clear))

        box, form = form_group("Selected landmark")
        self._landmark_box = box
        self._landmark_point = PointEdit()
        self._landmark_point.setToolTip(_POSITION_TIP)
        form.addRow("Position", self._landmark_point)
        self._add(box)

    def _build_placement(self) -> None:
        box, form = form_group("Placement")
        self._snap = QCheckBox("Snap to nearest vertex")
        self._free = QCheckBox("Free points (ignore the surface)")
        self._free.setToolTip(_FREE_TIP)
        form.addRow("", self._snap)
        form.addRow("", self._free)
        self._add(box)

    def _build_display(self) -> None:
        box, form = form_group("Display")
        self._show_all = QCheckBox("Show forms")
        self._show_landmarks = QCheckBox("Show landmarks")
        self._ghost = QCheckBox("Ghost the model")
        self._ghost.setToolTip(_GHOST_TIP)
        self._color = ColorButton(self.state.form_settings.color)
        self._smooth = SliderSpin(0.0, 90.0, 40.0, decimals=0, step=5.0, suffix=" deg")
        self._smooth.setToolTip(_SMOOTH_TIP)
        for widget in (self._show_all, self._show_landmarks, self._ghost):
            form.addRow("", widget)
        form.addRow("Clay colour", self._color)
        form.addRow("Smoothing", self._smooth)
        self._add(box)

    def _connect(self) -> None:
        self._start.clicked.connect(self.start_guide)
        self._skip.clicked.connect(self._skip_landmark)
        self._back.clicked.connect(self._back_landmark)
        self._finish.clicked.connect(self.end_guide)
        self._preset.currentIndexChanged.connect(lambda _: self.update_enabled())
        self._fill.currentIndexChanged.connect(self._on_fill)
        self._point_name.textEdited.connect(lambda _: self._set_pending())
        self._point_side.currentIndexChanged.connect(lambda _: self._set_pending())
        self._mirror.toggled.connect(lambda v: self._apply("mirror", v))
        self._symmetric.toggled.connect(lambda v: self._apply("symmetric", v))
        self._stage.valueChanged.connect(self._scrub)

        self._append.clicked.connect(self.append_landmarks)
        self._delete.clicked.connect(self._delete_selected)
        self._center.clicked.connect(self._center_selected)
        self._clear.clicked.connect(self.clear_all)
        self._landmark_point.valueChanged.connect(self._move_landmark)

        self._snap.toggled.connect(lambda v: self._apply("snap_to_vertex", v))
        self._free.toggled.connect(lambda v: self._apply("free_placement", v))
        self._show_all.toggled.connect(lambda v: self._apply("show_all", v))
        self._show_landmarks.toggled.connect(lambda v: self._apply("show_landmarks", v))
        self._ghost.toggled.connect(self._set_ghost)
        self._color.colorChanged.connect(lambda c: self._apply("color", tuple(c)))
        self._smooth.valueCommitted.connect(lambda v: self._apply("smooth", float(v)))

    # -- tool toggle ----------------------------------------------------

    def attach(self, tool) -> None:
        """Adopt the viewport's tool, which is where the guided run lives."""
        self._tool = tool
        self.update_enabled()

    def set_forming(self, active: bool) -> None:
        """Reflect the tool state without re-emitting the toggle."""
        with self._suppressed():
            self._toggle.setChecked(active)
        self.update_enabled()

    def _on_toggled(self, active: bool) -> None:
        if self._busy:
            return
        self.form_toggled.emit(active)

    # -- the guided walk -------------------------------------------------

    def start_guide(self) -> None:
        """Begin a run against a fresh form: a preset's walk, or a freeform's."""
        if self._tool is None:
            return
        preset = self._preset.currentData() or ""
        if preset not in FORM_PRESETS and preset != FREEFORM:
            return
        if preset == FREEFORM:
            name = self._form_name.text().strip() or self.state.forms.next_name(preset)
            form = PrimaryForm(name=name, preset=preset, fill=self._fill_choice())
        else:
            form = PrimaryForm(name=self.state.forms.next_name(preset), preset=preset)
        self.state.do(AddItem(self.state.forms.items, form, text=f"Add {form.name}", channel=FORMS))
        self._tool.start_guide(preset, len(self.state.forms) - 1)
        if preset == FREEFORM:
            with self._suppressed():
                self._form_name.clear()
            self._advance_pending(form)
        self.form_toggled.emit(True)
        self.state.notify_forms()

    def end_guide(self) -> None:
        if self._tool is None:
            return
        self._tool.end_guide()
        self.state.notify_forms()

    def append_landmarks(self) -> None:
        """Take up the selected freeform again, so more landmarks can go on it.

        The same run Start begins, against a form already in the store: the
        panel names the next landmark and each click lays it down.  A preset
        has nothing to append -- its landmarks are named in advance -- so
        the button only answers for a freeform.
        """
        found = self._appendable_form()
        if found is None or self._tool is None:
            return
        index, form = found
        self._tool.start_guide(FREEFORM, index)
        self._advance_pending(form)
        self.form_toggled.emit(True)
        self.state.notify_forms()

    def _appendable_form(self) -> tuple[int, PrimaryForm] | None:
        """The freeform the highlighted row belongs to, when no run is on."""
        if self._tool is None or self._tool.guiding:
            return None
        found = self._row_data()
        if found is None:
            return None
        form = self.state.forms[found[0]]
        return (found[0], form) if form.freeform else None

    def _skip_landmark(self) -> None:
        form = self._guided_form()
        if self._tool is None or form is None:
            return
        self._tool.skip(form, self.state.form_settings)
        self.state.notify_forms()

    def _back_landmark(self) -> None:
        """Take back the landmark before this one and ask for it again."""
        form = self._guided_form()
        if self._tool is None or form is None:
            return
        if form.freeform:
            self._back_point(form)
            return
        settings = self.state.form_settings
        key = self._tool.back(form, settings)
        if key is None:
            self.state.notify_forms()
            return
        landmarks = self._tool.derive(form, form.without_landmarks(key), settings)
        self.state.do(
            SetAttributes(
                form, {"landmarks": landmarks}, text="Take back a landmark", channel=FORMS
            )
        )

    def _back_point(self, form: PrimaryForm) -> None:
        """Take back the last landmark a freeform was given, guess and all."""
        if not form.points:
            self.state.notify_forms()
            return
        last = form.points[-1]
        points = form.without_points(last.key)
        landmarks = self._tool.derive(
            form,
            form.without_landmarks(last.key, *self._guesses_from(form, last.key)),
            self.state.form_settings,
            points,
        )
        self.state.do(
            SetAttributes(
                form,
                {"landmarks": landmarks, "points": points},
                text=f"Take back {last.title}",
                channel=FORMS,
            )
        )

    def _guided_form(self) -> PrimaryForm | None:
        run = self._tool.guide if self._tool is not None else None
        if run is None or not 0 <= run.form < len(self.state.forms):
            return None
        return self.state.forms[run.form]

    # -- the freeform's next landmark -----------------------------------

    def _fill_choice(self) -> FormFill:
        return FormFill(self._fill.currentData() or FormFill.FACETED.value)

    def _side_choice(self) -> Side:
        return Side(self._point_side.currentData() or Side.CENTRE.value)

    def _set_pending(self) -> None:
        """Ready the landmark the next click lays down, from the name and side boxes."""
        if self._busy:
            return
        run = self._tool.guide if self._tool is not None else None
        form = self._guided_form()
        if run is None or form is None or not run.freeform:
            return
        run.pending = freeform_landmark(
            self._point_name.text(), self._side_choice(), (entry.key for entry in form.points)
        )
        self.repaint_requested.emit()

    def _advance_pending(self, form: PrimaryForm) -> None:
        """After a landmark goes down: a fresh numbered name, the same side."""
        run = self._tool.guide if self._tool is not None else None
        if run is None or not run.freeform:
            return
        with self._suppressed():
            self._point_name.setText(f"Point {len(form.points) + 1}")
        run.pending = freeform_landmark(
            self._point_name.text(), self._side_choice(), (entry.key for entry in form.points)
        )

    def _on_fill(self, _index: int) -> None:
        """Refit the focused freeform's clay; for a new one, remember the choice."""
        if self._busy:
            return
        found = self._focused_form()
        if found is None or not found[1].freeform:
            return
        fill = self._fill_choice()
        form = found[1]
        if fill is form.fill:
            return
        self.state.do(SetAttributes(form, {"fill": fill}, text=f"Refit {form.name}", channel=FORMS))

    # -- edits ----------------------------------------------------------

    def apply_edit(self, edit) -> None:
        """Record an edit the viewport's tool worked out.

        A freeform's placed landmark is new to the form's own list as well,
        so the two go into the document in the one step, and the next
        landmark is readied.
        """
        index, landmarks, text = edit
        if not 0 <= index < len(self.state.forms):
            return
        form = self.state.forms[index]
        changes = {"landmarks": landmarks}
        pending = self._pending_for(index)
        placed = pending is not None and any(entry.key == pending.key for entry in landmarks)
        if placed and form.point_for(pending.key) is None:
            changes["points"] = form.with_point(pending)
        self.state.do(SetAttributes(form, changes, text=text, channel=FORMS))
        if placed:
            self._advance_pending(form)
            self.update_enabled()

    def _pending_for(self, index: int) -> Landmark | None:
        run = self._tool.guide if self._tool is not None else None
        if run is None or run.form != index or not run.freeform:
            return None
        return run.pending

    def _write_landmarks(
        self,
        index: int,
        landmarks: list[PlacedLandmark],
        text: str,
        points: list[Landmark] | None = None,
    ) -> None:
        """Record an edited landmark list, mirrored where the mirror is on."""
        form = self.state.forms[index]
        if self._tool is not None:
            landmarks = self._tool.derive(form, landmarks, self.state.form_settings, points)
        changes = {"landmarks": landmarks}
        if points is not None:
            changes["points"] = points
        self.state.do(SetAttributes(form, changes, text=text, channel=FORMS))

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
        form = self.state.forms[index]
        self._write_landmarks(
            index,
            form.with_landmark_at(landmark.key, scene),
            f"Move {form_landmark_title(form, landmark.key)}",
        )

    def _delete_selected(self) -> None:
        """Remove the selected landmark, or the whole form when its row is picked."""
        found = self._selected_landmark()
        if found is not None:
            index, landmark = found
            form = self.state.forms[index]
            if self._tool is not None:
                self._tool.selected_landmark = None
            points = form.without_points(landmark.key) if form.freeform else None
            self._write_landmarks(
                index,
                form.without_landmarks(landmark.key, *self._guesses_from(form, landmark.key)),
                f"Delete {form_landmark_title(form, landmark.key)}",
                points,
            )
            return
        whole = self._selected_form()
        if whole is None:
            return
        index, form = whole
        run = self._tool.guide if self._tool is not None else None
        if run is not None and run.form == index:
            self.end_guide()
        self.state.do(
            RemoveItem(self.state.forms.items, index, text=f"Delete {form.name}", channel=FORMS)
        )

    def clear_all(self) -> None:
        if not len(self.state.forms):
            return
        self.end_guide()
        self.state.do(ReplaceItems(self.state.forms.items, [], text="Clear forms", channel=FORMS))

    def _center_selected(self) -> None:
        found = self._selected_landmark()
        if found is not None:
            self.center_requested.emit(found[1].point)
            return
        whole = self._selected_form()
        if whole is not None and whole[1].landmarks:
            points = [entry.point for entry in whole[1].landmarks]
            self.center_requested.emit(sum(points) / len(points))

    def _scrub(self, value: int) -> None:
        """Show a stage of the focused form.  A view choice, so not an undo step."""
        if self._busy:
            return
        found = self._focused_form()
        if found is None:
            return
        _, form = found
        spec = form_spec(form)
        stages = len(spec.stages) if spec is not None else 1
        # The right-hand end means "everything there is", including stages
        # still to come, so it is stored as the open-ended value.
        form.stage = -1 if int(value) >= stages - 1 else int(value)
        self.state.notify_forms()

    @staticmethod
    def _guesses_from(form: PrimaryForm, key: str) -> list[str]:
        """The mirrored landmarks reflected from ``key``, which it anchors."""
        preset = form_spec(form)
        if preset is None:
            return []
        return [
            entry.key
            for entry in form.landmarks
            if entry.mirrored
            and (spec := preset.landmark(entry.key)) is not None
            and spec.mirror_of == key
        ]

    @staticmethod
    def _ordered(form: PrimaryForm) -> list[PlacedLandmark]:
        """The landmarks in the recipe's own order, stage by stage."""
        preset = form_spec(form)
        if preset is None:
            return list(form.landmarks)
        order = {entry.key: position for position, entry in enumerate(preset.landmarks)}
        return sorted(form.landmarks, key=lambda e: order.get(e.key, len(order)))

    @property
    def _unit_scale(self) -> float:
        """The multiplier the position boxes are read and written through."""
        scale = float(self.state.measurement_settings.unit_scale)
        return scale if scale > 0.0 else 1.0

    # -- the list -------------------------------------------------------

    def refresh(self) -> None:
        settings = self.state.form_settings
        with self._suppressed():
            self._mirror.setChecked(settings.mirror)
            self._symmetric.setChecked(settings.symmetric)
            self._snap.setChecked(settings.snap_to_vertex)
            self._free.setChecked(settings.free_placement)
            self._show_all.setChecked(settings.show_all)
            self._show_landmarks.setChecked(settings.show_landmarks)
            self._ghost.setChecked(self.state.render.ghost)
            self._color.set_color(settings.color)
            self._smooth.set_value(settings.smooth)
            units = self.state.measurement_settings
            self._landmark_point.set_decimals(units.decimals)
            self._landmark_point.set_step(
                max(float(self.state.camera.scene_radius) * units.unit_scale, 1.0) / 100.0
            )
        self.refresh_list()

    def refresh_display(self) -> None:
        """Keep the ghost switch agreeing with the Shading panel's."""
        with self._suppressed():
            self._ghost.setChecked(self.state.render.ghost)

    def refresh_list(self) -> None:
        """Rebuild the tree from the store, keeping the landmark being edited shown.

        Not mid-drag: a landmark being pulled about notifies on every mouse
        move, and rebuilding the list that often would yank the selection out
        from under the gesture.
        """
        if self._tool is not None and self._tool.grabbed_landmark is not None:
            return
        chosen = self._tool.selected_landmark if self._tool is not None else None
        matched = False
        with self._suppressed():
            self._tree.clear()
            for index, form in enumerate(self.state.forms):
                preset = form_spec(form)
                parent = QTreeWidgetItem([form.name, ""])
                parent.setFlags(
                    parent.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsUserCheckable
                )
                parent.setCheckState(
                    _NAME_COLUMN,
                    Qt.CheckState.Checked if form.visible else Qt.CheckState.Unchecked,
                )
                parent.setData(_NAME_COLUMN, Qt.ItemDataRole.UserRole, (index, ""))
                if preset is not None:
                    parent.setToolTip(_NAME_COLUMN, preset.stages[0].description)
                # Into the tree before its children, so that restoring the
                # selection below really does select.
                self._tree.addTopLevelItem(parent)
                for landmark in self._ordered(form):
                    entry = preset.landmark(landmark.key) if preset is not None else None
                    child = QTreeWidgetItem(
                        [
                            entry.title if entry is not None else landmark.key,
                            "guess" if landmark.mirrored else "",
                        ]
                    )
                    child.setData(_NAME_COLUMN, Qt.ItemDataRole.UserRole, (index, landmark.key))
                    if form.freeform and form.point_for(landmark.key) is not None:
                        # The artist's own landmark: theirs to rename.
                        child.setFlags(child.flags() | Qt.ItemFlag.ItemIsEditable)
                        child.setToolTip(_NAME_COLUMN, "Double-click to rename.")
                    elif entry is not None:
                        child.setToolTip(_NAME_COLUMN, entry.hint)
                    if landmark.mirrored:
                        child.setToolTip(
                            _MARK_COLUMN,
                            "Reflected across the median plane rather than placed.\n"
                            "Move it and it becomes yours.",
                        )
                    parent.addChild(child)
                    if chosen == (index, landmark.key):
                        self._tree.setCurrentItem(child)
                        matched = True
                parent.setExpanded(True)
        if not matched and self._tool is not None:
            self._tool.selected_landmark = None
        self.update_enabled()

    def update_enabled(self) -> None:
        """Take off the panel whatever does not apply right now."""
        guiding = self._tool is not None and self._tool.guiding
        guided = self._guided_form()
        freeform_run = guiding and guided is not None and guided.freeform
        freeform_pick = not guiding and self._preset.currentData() == FREEFORM
        focused = self._focused_form()
        freeform_focus = focused is not None and focused[1].freeform
        for widget in (self._running, self._progress):
            self._guide_form.setRowVisible(widget, guiding)
        self._guide_form.setRowVisible(self._prompt, guiding and not freeform_run)
        for widget in (self._point_name, self._point_side):
            self._guide_form.setRowVisible(widget, freeform_run)
        self._skip.setVisible(not freeform_run)
        for widget in (self._preset, self._mirror, self._start):
            self._guide_form.setRowVisible(widget, not guiding)
        self._guide_form.setRowVisible(self._form_name, freeform_pick)
        self._guide_form.setRowVisible(self._fill, freeform_pick or freeform_focus)
        if freeform_focus:
            with self._suppressed():
                self._fill.setCurrentIndex(self._fill.findData(focused[1].fill.value))
        if guiding:
            self._refresh_prompt()

        landmark = self._selected_landmark()
        whole = self._selected_form()
        self._landmark_box.setVisible(landmark is not None)
        self._append.setEnabled(self._appendable_form() is not None)
        self._delete.setEnabled(landmark is not None or whole is not None)
        self._center.setEnabled(
            landmark is not None or (whole is not None and bool(whole[1].landmarks))
        )
        if landmark is not None:
            scale = self._unit_scale
            with self._suppressed():
                self._landmark_point.set_value(value * scale for value in landmark[1].at)
        self._refresh_stages()

    def _refresh_stages(self) -> None:
        """Size the stage slider to the focused form, and hide it for a one-stage form."""
        found = self._focused_form()
        preset = form_spec(found[1]) if found is not None else None
        if found is None or preset is None or len(preset.stages) <= 1:
            self._stage_box.setVisible(False)
            return
        _, form = found
        count = len(preset.stages)
        shown = count - 1 if form.stage < 0 else min(max(int(form.stage), 0), count - 1)
        stage = preset.stages[shown]
        with self._suppressed():
            self._stage.setRange(0, count - 1)
            self._stage.setValue(shown)
            self._stage_label.setText(f"{shown + 1} of {count}: {stage.name}.  {stage.description}")
        self._stage_box.setVisible(True)

    def _refresh_prompt(self) -> None:
        form = self._guided_form()
        if form is None or self._tool is None:
            return
        settings = self.state.form_settings
        placed, wanted = self._tool.progress(form, settings)
        entry = self._tool.current(form, settings)
        if form.freeform:
            held = "landmark" if placed == 1 else "landmarks"
            self._progress.setText(
                f"{placed} {held} placed.  Click to place the next; the clay is the hull "
                "of them once four span a volume.  Press Finish to keep the form."
            )
            return
        if entry is None:
            self._prompt.setText("Every landmark is placed.")
            self._progress.setText(f"{placed} of {wanted}. Press Finish to keep the form.")
            return
        self._prompt.setText(f"<b>{entry.title}</b><br/>{entry.hint}")
        progress = self._tool.stage_progress(form, settings)
        spec = form_spec(form)
        if progress is not None and spec is not None and len(spec.stages) > 1:
            index, done, asked = progress
            self._progress.setText(
                f"Landmark {placed + 1} of {wanted}  -  {spec.stages[index].name}, "
                f"{done + 1} of {asked}"
            )
        else:
            self._progress.setText(f"Landmark {placed + 1} of {wanted}")

    # -- rows -----------------------------------------------------------

    def _row_data(self) -> tuple[int, str] | None:
        item = self._tree.currentItem()
        if item is None or not item.isSelected():
            return None
        found = item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        if not found or not 0 <= found[0] < len(self.state.forms):
            return None
        return found[0], found[1]

    def _selected_form(self) -> tuple[int, PrimaryForm] | None:
        """The form the selected row stands for, when the row is a form."""
        found = self._row_data()
        if found is None or found[1]:
            return None
        return found[0], self.state.forms[found[0]]

    def _selected_landmark(self) -> tuple[int, PlacedLandmark] | None:
        """The landmark the highlighted row stands for, if the row is one."""
        found = self._row_data()
        if found is None or not found[1]:
            return None
        index, key = found
        landmark = self.state.forms[index].landmark_for(key)
        return None if landmark is None else (index, landmark)

    def _focused_form(self) -> tuple[int, PrimaryForm] | None:
        """The form the stage slider speaks for: the one being guided, else the one picked."""
        run = self._tool.guide if self._tool is not None else None
        if run is not None and 0 <= run.form < len(self.state.forms):
            return run.form, self.state.forms[run.form]
        found = self._row_data()
        if found is None:
            return None
        return found[0], self.state.forms[found[0]]

    def _on_selection_changed(self) -> None:
        """Follow the highlighted landmark, and say which one it is in the view."""
        if self._busy:
            return
        found = self._selected_landmark()
        if self._tool is not None:
            self._tool.selected_landmark = None if found is None else (found[0], found[1].key)
        self.update_enabled()
        self.repaint_requested.emit()

    def select_landmark(self, ref) -> None:
        """Highlight the row for a landmark picked in the view."""
        if self._tool is not None:
            self._tool.selected_landmark = ref
        with self._suppressed():
            for parent in range(self._tree.topLevelItemCount()):
                top = self._tree.topLevelItem(parent)
                for child in range(top.childCount()):
                    item = top.child(child)
                    if item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole) == ref:
                        self._tree.setCurrentItem(item)
                        self.update_enabled()
                        return
        self.update_enabled()

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        """Commit a renamed or re-checked form, or a renamed landmark, if anything changed."""
        if self._busy:
            return
        found = item.data(_NAME_COLUMN, Qt.ItemDataRole.UserRole)
        if not found or not 0 <= found[0] < len(self.state.forms):
            return
        form = self.state.forms[found[0]]
        if found[1]:
            self._rename_point(form, found[1], item.text(_NAME_COLUMN))
            return
        name = item.text(_NAME_COLUMN)
        visible = item.checkState(_NAME_COLUMN) == Qt.CheckState.Checked
        changes = {}
        if name and name != form.name:
            changes["name"] = name
        if visible != form.visible:
            changes["visible"] = visible
        if not changes:
            return
        verb = "Rename" if "name" in changes else ("Show" if visible else "Hide")
        self._commit_later(
            form, SetAttributes(form, changes, text=f"{verb} {form.name}", channel=FORMS)
        )

    def _rename_point(self, form: PrimaryForm, key: str, text: str) -> None:
        """Give a freeform's own landmark the name typed into its row."""
        held = form.point_for(key)
        if held is None:
            return
        # The row shows the title, name and side; what was typed is the name,
        # with the side the artist may have left on the end taken back off.
        name = text.strip()
        suffix = f" ({held.side.label})" if held.side.label else ""
        if suffix and name.endswith(suffix):
            name = name[: -len(suffix)].strip()
        if not name or name == held.name:
            self.refresh_list()
            return
        self._commit_later(
            form,
            SetAttributes(
                form,
                {"points": form.with_point_named(key, name)},
                text=f"Rename {held.title}",
                channel=FORMS,
            ),
        )

    def _commit_later(self, owner, command: SetAttributes) -> None:
        """Run a row's edit once Qt has finished delivering the current signal.

        Committing rebuilds the tree, and destroying the very item whose
        signal is still being delivered takes the application down with it.
        """

        def commit() -> None:
            if any(form is owner for form in self.state.forms):
                self.state.do(command)

        QTimer.singleShot(0, commit)

    # -- settings -------------------------------------------------------

    def _apply(self, field: str, value) -> None:
        if self._busy:
            return
        setattr(self.state.form_settings, field, value)
        self.state.notify_forms()

    # -- the tab's switch -----------------------------------------------

    def shown(self) -> bool | None:
        return self.state.form_settings.show_all

    def set_shown(self, on: bool) -> None:
        self._show_all.setChecked(bool(on))

    def _set_ghost(self, on: bool) -> None:
        if self._busy:
            return
        self.state.render.ghost = bool(on)
        self.state.notify_render()
