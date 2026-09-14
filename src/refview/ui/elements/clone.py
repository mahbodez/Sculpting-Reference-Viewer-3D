"""Copying a control out of its panel and keeping the copy honest.

Alt and drag any control and a copy of it comes away on the cursor; drop the
copy into a panel of your own and it stands there doing exactly what the
original does.  That is the whole of it from the outside, and it exists
because a panel is organised by subject and a session is organised by what
you happen to be doing: the three controls someone reaches for every minute
are almost never the three that belong in the same group.

A copy is not a second setting.  Everything it is given goes straight to the
control it was copied from, which is still the one thing that owns the value;
the copy is a second pair of hands on the same control.  Coming back the other
way, the copy is refreshed off the original on a slow tick rather than by
following its signals.  A tick is the coarser instrument, and it is the right
one here: it catches an original that changed for a reason nobody thought to
announce -- a panel refreshing itself from a loaded session, a label rewritten
in place, a control being switched off -- where following signals catches only
the changes somebody remembered to declare, which is the class of bug that
would show up as a copy quietly disagreeing with the thing it copies.  Nothing
here is in a frame budget; a fifth of a second is imperceptible on a slider
somebody else is dragging.

Which controls can be copied is a table of small adapters, one per kind, each
saying how to build the copy, how to send a change to the original, and how to
read the original back.  A kind with no adapter simply cannot be copied, which
is the correct answer for a list, a gallery, or anything else whose meaning is
in what it contains rather than in one value.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from weakref import WeakKeyDictionary

from PySide6.QtCore import QEvent, QMimeData, QObject, QPoint, Qt, QTimer
from PySide6.QtGui import QDrag, QPixmap
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QSpinBox,
    QWidget,
)

from .controls import ColorButton, PointEdit
from .frame import Frame, frame_form
from .naming import caption_for, element_id
from .slider import ValueSlider

#: What a dragged copy is carried as.
CLONE_MIME = "application/x-refview-element"

#: How often a copy checks the control it copies, in milliseconds.
PULSE_MS = 200

#: Property set on a copy, holding the id of what it copies.
SOURCE_PROPERTY = "refview_clone_source"

#: Property marking a copy that has been placed in a custom panel, so that
#: Alt-dragging it moves it rather than copying the copy.
HOLDER_PROPERTY = "refview_clone_holder"


# ----------------------------------------------------------------------
# The table of what can be copied
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class Cloner:
    """How to make, drive and refresh a copy of one kind of control."""

    build: Callable[[QWidget], QWidget]
    push: Callable[[QWidget, QWidget], None]
    pull: Callable[[QWidget, QWidget], None]


_CLONERS: list[tuple[type, Cloner]] = []


def register_cloner(
    kind: type,
    build: Callable[[QWidget], QWidget],
    push: Callable[[QWidget, QWidget], None],
    pull: Callable[[QWidget, QWidget], None],
) -> None:
    """Teach the copier about a kind of control."""
    _CLONERS.append((kind, Cloner(build, push, pull)))


def cloner_for(widget: QWidget) -> Cloner | None:
    """The most specific adapter that covers ``widget``, if any."""
    best: Cloner | None = None
    reach = -1
    for kind, cloner in _CLONERS:
        if isinstance(widget, kind) and len(kind.__mro__) > reach:
            best, reach = cloner, len(kind.__mro__)
    return best


def can_clone(widget: QWidget) -> bool:
    return cloner_for(widget) is not None


# ----------------------------------------------------------------------
# The link that keeps a copy and its original together
# ----------------------------------------------------------------------


class _Pulse(QObject):
    """One timer for every copy in the window."""

    _instance: "_Pulse | None" = None

    def __init__(self) -> None:
        super().__init__()
        self._timer = QTimer(self)
        self._timer.setInterval(PULSE_MS)
        self._links: list[Link] = []
        self._timer.timeout.connect(self._tick)

    @classmethod
    def instance(cls) -> "_Pulse":
        if cls._instance is None:
            cls._instance = _Pulse()
        return cls._instance

    def join(self, link: "Link") -> None:
        self._links.append(link)
        if not self._timer.isActive():
            self._timer.start()

    def leave(self, link: "Link") -> None:
        if link in self._links:
            self._links.remove(link)
        if not self._links:
            self._timer.stop()

    def _tick(self) -> None:
        for link in list(self._links):
            link.refresh()


class Link(QObject):
    """Holds a copy to the control it was copied from.

    Parented to the copy, so it goes when the copy goes.
    """

    def __init__(self, source: QWidget, copy: QWidget, cloner: Cloner) -> None:
        super().__init__(copy)
        self._source = source
        self._copy = copy
        self._cloner = cloner
        self._broken = False
        cloner.push(copy, source)
        _Pulse.instance().join(self)
        copy.destroyed.connect(lambda *_: _Pulse.instance().leave(self))

    @property
    def source(self) -> QWidget:
        return self._source

    def is_broken(self) -> bool:
        return self._broken

    def refresh(self) -> None:
        """Bring the copy up to date with its original."""
        if self._broken:
            return
        try:
            enabled = self._source.isEnabled()
            tip = self._source.toolTip()
            shown = self._source.isVisibleTo(self._source.window())
        except RuntimeError:
            # The panel it lived in has been taken apart under us.
            self._break()
            return
        self._copy.setEnabled(enabled)
        if tip and self._copy.toolTip() != tip:
            self._copy.setToolTip(tip)
        # A row that the panel it came from has hidden -- a setting that only
        # applies in one mode, say -- is hidden here too, caption and all.
        # Otherwise a custom panel slowly fills up with controls that are no
        # longer connected to anything the artist can see.
        if self._copy.isVisible() != shown:
            self._copy.setVisible(shown)
        label = getattr(self._copy, "_refview_row_label", None)
        if isinstance(label, QWidget) and label.isVisible() != shown:
            label.setVisible(shown)
        if self._busy():
            return
        try:
            self._cloner.pull(self._copy, self._source)
        except RuntimeError:
            self._break()

    def _busy(self) -> bool:
        """Whether the copy is being used right now and must not be written."""
        grabber = QWidget.mouseGrabber()
        if grabber is not None and (grabber is self._copy or self._copy.isAncestorOf(grabber)):
            return True
        focused = QApplication.focusWidget()
        return isinstance(focused, QLineEdit | QSpinBox | QDoubleSpinBox) and (
            focused is self._copy or self._copy.isAncestorOf(focused)
        )

    def _break(self) -> None:
        self._broken = True
        _Pulse.instance().leave(self)
        self._copy.setEnabled(False)
        self._copy.setToolTip("The control this was copied from is gone.")


def clone(source: QWidget) -> QWidget | None:
    """A working copy of ``source``, or ``None`` if its kind cannot be copied."""
    cloner = cloner_for(source)
    if cloner is None:
        return None
    copy = cloner.build(source)
    copy.setProperty(SOURCE_PROPERTY, element_id(source) or "")
    if source.toolTip():
        copy.setToolTip(source.toolTip())
    copy.setEnabled(source.isEnabled())
    Link(source, copy, cloner)
    return copy


def source_of(copy: QWidget) -> str:
    """The id of what a copy copies, or an empty string."""
    return str(copy.property(SOURCE_PROPERTY) or "")


# ----------------------------------------------------------------------
# The adapters
# ----------------------------------------------------------------------


def _quiet(widget: QWidget, write: Callable[[], None]) -> None:
    blocked = widget.blockSignals(True)
    try:
        write()
    finally:
        widget.blockSignals(blocked)


def _clone_slider(source: ValueSlider) -> QWidget:
    return ValueSlider(
        source.minimum(),
        source.maximum(),
        source.value(),
        decimals=source.decimals(),
        step=source.step(),
        suffix=source.suffix(),
        ceiling=source.ceiling(),
        caption=source.caption() or caption_for(source),
    )


def _push_slider(copy: ValueSlider, source: ValueSlider) -> None:
    def write(value: float) -> None:
        source.set_value(value)
        source.valueChanged.emit(source.value())

    copy.valueChanged.connect(write)
    copy.valueCommitted.connect(lambda _v: source.valueCommitted.emit(source.value()))


def _pull_slider(copy: ValueSlider, source: ValueSlider) -> None:
    if (copy.minimum(), copy.maximum(), copy.ceiling()) != (
        source.minimum(),
        source.maximum(),
        source.ceiling(),
    ):
        copy.set_range(source.minimum(), source.maximum(), source.ceiling())
    if copy.value() != source.value():
        copy.set_value(source.value())


def _clone_check(source: QCheckBox) -> QWidget:
    copy = QCheckBox(source.text() or caption_for(source))
    copy.setChecked(source.isChecked())
    copy.setTristate(source.isTristate())
    return copy


def _push_check(copy: QCheckBox, source: QCheckBox) -> None:
    copy.toggled.connect(source.setChecked)


def _pull_check(copy: QCheckBox, source: QCheckBox) -> None:
    if copy.isChecked() != source.isChecked():
        _quiet(copy, lambda: copy.setChecked(source.isChecked()))
    if source.text() and copy.text() != source.text():
        copy.setText(source.text())


def _clone_button(source: QAbstractButton) -> QWidget:
    copy = QPushButton(source.text())
    copy.setIcon(source.icon())
    copy.setCheckable(source.isCheckable())
    copy.setChecked(source.isChecked())
    return copy


def _push_button(copy: QPushButton, source: QAbstractButton) -> None:
    if source.isCheckable():
        copy.toggled.connect(source.setChecked)
    else:
        copy.clicked.connect(lambda _checked=False: source.click())


def _pull_button(copy: QPushButton, source: QAbstractButton) -> None:
    if copy.text() != source.text():
        copy.setText(source.text())
    if source.isCheckable() and copy.isChecked() != source.isChecked():
        _quiet(copy, lambda: copy.setChecked(source.isChecked()))


def _clone_swatch(source: ColorButton) -> QWidget:
    return ColorButton(source.color())


def _push_swatch(copy: ColorButton, source: ColorButton) -> None:
    def write(colour: tuple[float, float, float]) -> None:
        source.set_color(colour)
        source.colorChanged.emit(source.color())

    copy.colorChanged.connect(write)


def _pull_swatch(copy: ColorButton, source: ColorButton) -> None:
    if copy.color() != source.color():
        copy.set_color(source.color())


def _clone_combo(source: QComboBox) -> QWidget:
    copy = QComboBox()
    _fill_combo(copy, source)
    return copy


def _fill_combo(copy: QComboBox, source: QComboBox) -> None:
    def write() -> None:
        copy.clear()
        for row in range(source.count()):
            copy.addItem(source.itemText(row), source.itemData(row))
        copy.setCurrentIndex(source.currentIndex())

    _quiet(copy, write)


def _push_combo(copy: QComboBox, source: QComboBox) -> None:
    copy.currentIndexChanged.connect(source.setCurrentIndex)


def _pull_combo(copy: QComboBox, source: QComboBox) -> None:
    same = copy.count() == source.count() and all(
        copy.itemText(row) == source.itemText(row) for row in range(source.count())
    )
    if not same:
        _fill_combo(copy, source)
        return
    if copy.currentIndex() != source.currentIndex():
        _quiet(copy, lambda: copy.setCurrentIndex(source.currentIndex()))


def _clone_spin(source: QDoubleSpinBox | QSpinBox) -> QWidget:
    copy = type(source)()
    if isinstance(source, QDoubleSpinBox):
        copy.setDecimals(source.decimals())
    copy.setRange(source.minimum(), source.maximum())
    copy.setSingleStep(source.singleStep())
    copy.setSuffix(source.suffix())
    copy.setPrefix(source.prefix())
    copy.setKeyboardTracking(False)
    copy.setValue(source.value())
    return copy


def _push_spin(copy, source) -> None:
    copy.valueChanged.connect(source.setValue)


def _pull_spin(copy, source) -> None:
    if copy.value() != source.value():
        _quiet(copy, lambda: copy.setValue(source.value()))


def _clone_point(source: PointEdit) -> QWidget:
    copy = PointEdit(source.decimals())
    copy.set_value(source.value())
    return copy


def _push_point(copy: PointEdit, source: PointEdit) -> None:
    def write(point: tuple[float, float, float]) -> None:
        source.set_value(point)
        source.valueChanged.emit(source.value())

    copy.valueChanged.connect(write)


def _pull_point(copy: PointEdit, source: PointEdit) -> None:
    if copy.value() != source.value():
        copy.set_value(source.value())


def _clone_label(source: QLabel) -> QWidget:
    copy = QLabel(source.text())
    copy.setWordWrap(source.wordWrap())
    copy.setTextFormat(source.textFormat())
    return copy


def _push_label(copy: QLabel, source: QLabel) -> None:
    """Nothing: a label is read, not set."""


def _pull_label(copy: QLabel, source: QLabel) -> None:
    if copy.text() != source.text():
        copy.setText(source.text())


def _clone_line(source: QLineEdit) -> QWidget:
    copy = QLineEdit(source.text())
    copy.setPlaceholderText(source.placeholderText())
    copy.setReadOnly(source.isReadOnly())
    return copy


def _push_line(copy: QLineEdit, source: QLineEdit) -> None:
    copy.textEdited.connect(source.setText)
    copy.editingFinished.connect(source.editingFinished.emit)


def _pull_line(copy: QLineEdit, source: QLineEdit) -> None:
    if copy.text() != source.text():
        _quiet(copy, lambda: copy.setText(source.text()))


def _clone_qslider(source: QSlider) -> QWidget:
    copy = QSlider(source.orientation())
    copy.setRange(source.minimum(), source.maximum())
    copy.setSingleStep(source.singleStep())
    copy.setPageStep(source.pageStep())
    copy.setValue(source.value())
    return copy


def _push_qslider(copy: QSlider, source: QSlider) -> None:
    copy.valueChanged.connect(source.setValue)


def _pull_qslider(copy: QSlider, source: QSlider) -> None:
    if copy.value() != source.value():
        _quiet(copy, lambda: copy.setValue(source.value()))


def _clone_frame(source: Frame) -> QWidget:
    """A copy of a whole group: its bar, and a copy of every row in it.

    A group is how a panel is organised, and someone who wants three controls
    together usually wants the three that were already together.  Rows whose
    control cannot be copied are left out rather than left dead, so what
    arrives is a working group with a gap in it instead of a decorated one.
    """
    copy = Frame(source.title(), source.is_expanded())
    form = frame_form(copy.body())
    inner = source.body().layout()
    if isinstance(inner, QFormLayout):
        for row in range(inner.rowCount()):
            field = inner.itemAt(row, QFormLayout.ItemRole.FieldRole)
            spanning = inner.itemAt(row, QFormLayout.ItemRole.SpanningRole)
            item = field or spanning
            widget = item.widget() if item is not None else None
            if widget is None:
                continue
            child = clone(widget)
            if child is None:
                continue
            label = inner.itemAt(row, QFormLayout.ItemRole.LabelRole)
            holder = label.widget() if label is not None else None
            text = holder.text() if isinstance(holder, QLabel) else ""
            form.addRow(text, child)
    return copy


def _push_frame(copy: Frame, source: Frame) -> None:
    """Nothing: each row inside the copy is linked on its own."""


def _pull_frame(copy: Frame, source: Frame) -> None:
    if copy.title() != source.title():
        copy.set_title(source.title())


register_cloner(ValueSlider, _clone_slider, _push_slider, _pull_slider)
register_cloner(QCheckBox, _clone_check, _push_check, _pull_check)
register_cloner(QAbstractButton, _clone_button, _push_button, _pull_button)
register_cloner(ColorButton, _clone_swatch, _push_swatch, _pull_swatch)
register_cloner(QComboBox, _clone_combo, _push_combo, _pull_combo)
register_cloner(QSpinBox, _clone_spin, _push_spin, _pull_spin)
register_cloner(QDoubleSpinBox, _clone_spin, _push_spin, _pull_spin)
register_cloner(PointEdit, _clone_point, _push_point, _pull_point)
register_cloner(QLabel, _clone_label, _push_label, _pull_label)
register_cloner(QLineEdit, _clone_line, _push_line, _pull_line)
register_cloner(QSlider, _clone_qslider, _push_qslider, _pull_qslider)
register_cloner(Frame, _clone_frame, _push_frame, _pull_frame)


# ----------------------------------------------------------------------
# The gesture
# ----------------------------------------------------------------------


def payload(element: str, moving: QWidget | None = None) -> QMimeData:
    """What a drag carries: which control, and whether a copy is being moved."""
    mime = QMimeData()
    mime.setData(
        CLONE_MIME,
        json.dumps({"element": element, "moving": moving is not None}).encode("utf-8"),
    )
    return mime


def carried(mime: QMimeData) -> dict | None:
    """Read a drag's payload back, or ``None`` if it is not one of ours."""
    if not mime.hasFormat(CLONE_MIME):
        return None
    try:
        return json.loads(bytes(mime.data(CLONE_MIME)).decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None


#: The copy currently being dragged from one panel to another, if any.  Drags
#: never leave the process, so the widget itself can be handed over; what goes
#: in the payload is only enough for a drop target to know what it is holding.
_IN_FLIGHT: QWidget | None = None


def in_flight() -> QWidget | None:
    return _IN_FLIGHT


def start_drag(source: QWidget, moving: QWidget | None = None) -> None:
    """Begin carrying a copy of ``source`` on the cursor."""
    global _IN_FLIGHT
    identifier = element_id(source) or source_of(source)
    if not identifier and moving is None:
        return
    # The drag is hung off the window, not off the control being dragged: a
    # copy dropped on the model is destroyed while this is still running, and
    # a drag whose owner has just been deleted under it is a crash on the way
    # out of the gesture.
    drag = QDrag(source.window() or source)
    drag.setMimeData(payload(identifier, moving))
    picture = _portrait(moving or source)
    drag.setPixmap(picture)
    drag.setHotSpot(QPoint(picture.width() // 2, picture.height() // 2))
    _IN_FLIGHT = moving
    try:
        drag.exec(
            Qt.DropAction.MoveAction if moving is not None else Qt.DropAction.CopyAction
        )
    finally:
        _IN_FLIGHT = None


def _portrait(widget: QWidget) -> QPixmap:
    """A picture of the control, to carry under the cursor."""
    picture = widget.grab()
    if picture.isNull() or picture.width() < 4:
        picture = QPixmap(80, 20)
        picture.fill(Qt.GlobalColor.darkGray)
    return picture


class CloneGesture(QObject):
    """Watches for Alt and a drag, and turns it into a copy on the cursor.

    Installed on the control itself rather than on the window, because the
    press has to be swallowed: Alt-dragging a slider must not also drag the
    slider, and the only place that can be decided is before the slider sees
    the event.
    """

    _instance: "CloneGesture | None" = None

    def __init__(self) -> None:
        super().__init__()
        self._armed: QWidget | None = None
        self._origin = QPoint()
        #: Watched widget -> what Alt-dragging it actually copies.
        self._subjects: "WeakKeyDictionary[QWidget, QWidget]" = WeakKeyDictionary()

    @classmethod
    def instance(cls) -> "CloneGesture":
        if cls._instance is None:
            cls._instance = CloneGesture()
        return cls._instance

    def watch(self, widget: QWidget, subject: QWidget | None = None) -> None:
        """Alt-drag on ``widget`` copies ``subject``, which defaults to itself.

        The two differ for a group: the thing you can point at is its bar, and
        the thing you mean by pointing at it is the whole group.
        """
        widget.installEventFilter(self)
        if subject is not None and subject is not widget:
            self._subjects[widget] = subject

    def subject_of(self, widget: QWidget) -> QWidget:
        return self._subjects.get(widget, widget)

    def eventFilter(self, watched, event) -> bool:  # noqa: N802 - Qt contract
        kind = event.type()
        if kind == QEvent.Type.MouseButtonPress:
            if (
                event.button() == Qt.MouseButton.LeftButton
                and event.modifiers() & Qt.KeyboardModifier.AltModifier
                and isinstance(watched, QWidget)
            ):
                self._armed = watched
                self._origin = event.globalPosition().toPoint()
                return True
        elif kind == QEvent.Type.MouseMove and self._armed is watched:
            moved = (event.globalPosition().toPoint() - self._origin).manhattanLength()
            if moved >= QApplication.startDragDistance():
                held, self._armed = self._armed, None
                _begin(self.subject_of(held))
            return True
        elif (
            kind in (QEvent.Type.MouseButtonRelease, QEvent.Type.Leave)
            and self._armed is watched
        ):
            # Alt and a click that never became a drag: the press was taken
            # away from the control, so the release has to be too, or the
            # control sees half a click and acts on it.
            self._armed = None
            return kind == QEvent.Type.MouseButtonRelease
        return False


def _begin(widget: QWidget) -> None:
    """Start the drag the gesture asked for.

    Dragging a control that lives in a panel takes a copy of it; dragging a
    copy that is already in a panel of your own moves that copy, so the same
    gesture rearranges what it built.
    """
    holder = _holder_of(widget)
    start_drag(widget, moving=holder)


def _holder_of(widget: QWidget) -> QWidget | None:
    """The row in a custom panel that a copy sits in, if this is a copy."""
    node: QWidget | None = widget
    while node is not None:
        if node.property(HOLDER_PROPERTY):
            return node
        node = node.parentWidget()
    return None


def watch_tree(root: QWidget) -> None:
    """Make every control under ``root`` that can be copied Alt-draggable.

    A group is pointed at by its bar, since the group itself is only ever
    under the cursor where one of its rows is not.
    """
    gesture = CloneGesture.instance()
    for widget in [root, *root.findChildren(QWidget)]:
        if isinstance(widget, Frame):
            gesture.watch(widget.bar(), widget)
        elif can_clone(widget):
            gesture.watch(widget)
