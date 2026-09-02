"""Surface annotation tool: brush, shape and eraser settings."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QCheckBox,
    QGridLayout,
    QLabel,
    QPushButton,
)

from ...core.annotation import AnnotateMode
from ...core.commands import ReplaceItems
from ...core.history import ANNOTATIONS
from ..widgets import ColorButton, SliderSpin, form_group
from .base import Panel

_TOOLTIPS = {
    AnnotateMode.FREEHAND: "Draw along the surface, following the cursor.",
    AnnotateMode.LINE: "Drag out a straight line; it wraps onto the form.",
    AnnotateMode.CIRCLE: "Drag from the centre outwards.",
    AnnotateMode.ERASE: "Rub out the parts of a stroke under the brush.",
}


class AnnotatePanel(Panel):
    """Arms the annotate tool and edits the brush it paints with."""

    annotate_toggled = Signal(bool)

    def _build(self) -> None:
        self._toggle = QPushButton("Annotate  (A)")
        self._toggle.setCheckable(True)
        self._toggle.setToolTip(
            "Sketch on the surface: muscle masses, bony landmarks, plane breaks.\n"
            "Left drag paints, Alt+drag still orbits, Esc drops the current stroke."
        )
        self._toggle.toggled.connect(self._on_toggled)
        self._add(self._toggle)

        tools_box, _ = form_group("Tool")
        grid = QGridLayout()
        grid.setSpacing(4)
        self._modes = QButtonGroup(self)
        self._modes.setExclusive(True)
        for index, mode in enumerate(AnnotateMode):
            button = QPushButton(mode.label)
            button.setCheckable(True)
            button.setToolTip(_TOOLTIPS[mode])
            self._modes.addButton(button, index)
            grid.addWidget(button, index // 2, index % 2)
        tools_box.layout().addRow(grid)
        self._add(tools_box)

        brush_box, brush_form = form_group("Brush")
        self._color = ColorButton((0.94, 0.29, 0.24))
        self._width = SliderSpin(1.0, 20.0, 3.0, decimals=1, step=0.5)
        self._erase_radius = SliderSpin(4.0, 80.0, 16.0, decimals=0, step=1.0, suffix=" px")
        brush_form.addRow("Colour", self._color)
        brush_form.addRow("Width", self._width)
        brush_form.addRow("Eraser", self._erase_radius)
        self._add(brush_box)

        display_box, display_form = form_group("Display")
        self._visible = QCheckBox("Show annotations")
        self._count = QLabel()
        self._count.setStyleSheet("color: #8f939b;")
        clear = QPushButton("Clear All")
        clear.clicked.connect(self.clear_all)
        display_form.addRow("", self._visible)
        display_form.addRow("", self._count)
        display_form.addRow("", clear)
        self._add(display_box)

        hint = QLabel(
            "Strokes sit on the surface and are hidden by the model when you "
            "turn it around, so the far side stays out of the way."
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #8f939b;")
        self._add(hint)
        self._add_stretch()

        self._modes.idClicked.connect(self._on_mode)
        self._color.colorChanged.connect(lambda v: self._apply("color", v))
        self._width.valueChanged.connect(lambda v: self._apply("width", v))
        self._erase_radius.valueChanged.connect(lambda v: self._apply("erase_radius", v))
        self._visible.toggled.connect(lambda v: self._apply("visible", v))

    # -- tool toggle ----------------------------------------------------

    def set_annotating(self, active: bool) -> None:
        """Reflect the tool state without re-emitting the toggle."""
        with self._suppressed():
            self._toggle.setChecked(active)

    def _on_toggled(self, active: bool) -> None:
        if self._busy:
            return
        self.annotate_toggled.emit(active)

    def _on_mode(self, index: int) -> None:
        if self._busy:
            return
        self._apply("mode", list(AnnotateMode)[index])

    # -- content --------------------------------------------------------

    def refresh(self) -> None:
        settings = self.state.annotation_settings
        with self._suppressed():
            button = self._modes.button(list(AnnotateMode).index(settings.mode))
            if button is not None:
                button.setChecked(True)
            self._color.set_color(settings.color)
            self._width.set_value(settings.width)
            self._erase_radius.set_value(settings.erase_radius)
            self._visible.setChecked(settings.visible)
        self.refresh_list()

    def refresh_list(self) -> None:
        count = len(self.state.annotations)
        self._count.setText("No strokes yet" if not count else f"{count:,} strokes")

    def clear_all(self) -> None:
        if not len(self.state.annotations):
            return
        self.state.do(
            ReplaceItems(
                self.state.annotations.items, [], text="Clear annotations", channel=ANNOTATIONS
            )
        )

    def _apply(self, field: str, value) -> None:
        if self._busy:
            return
        setattr(self.state.annotation_settings, field, value)
        self.state.notify_annotations()
