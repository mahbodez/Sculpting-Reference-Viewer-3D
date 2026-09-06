"""Everything that acts on the shading normals rather than on the shading.

Faceted shading and the planes filter both change which direction a fragment
is shaded from, so they read the same whichever shading mode is running and
belong together, away from the light and material controls.
"""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QLabel

from ...core.settings import DETAIL_MAX, DETAIL_MIN, PlaneSettings
from ..widgets import ColorButton, SliderSpin, form_group
from .base import Panel


class PlanesPanel(Panel):
    """Breaks the surface normals down into the planes of the form."""

    def _build(self) -> None:
        box, form = form_group("Normals")
        self._flat = QCheckBox("Flat (faceted) shading")
        self._flat.setToolTip("Shade each triangle from its own face normal, showing the topology")
        form.addRow("", self._flat)
        self._add(box)

        planes_box, planes_form = form_group("Planes")
        self._enabled = QCheckBox("Break the form into planes")
        self._enabled.setToolTip(
            "Snap every normal to one of a small set of directions, so the model "
            "reads as blocked-in planes rather than as a continuous surface"
        )
        self._detail = SliderSpin(
            DETAIL_MIN, DETAIL_MAX, PlaneSettings().detail, decimals=0, step=1.0
        )
        self._detail.setToolTip(
            "Large, blocked-in planes on the left; finer ones on the right.  The "
            "slider moves the size of a plane evenly, so a step at the coarse end "
            "changes as much as a step at the fine end"
        )
        self._count = QLabel()
        self._count.setStyleSheet("color: #8f939b;")
        planes_form.addRow("", self._enabled)
        planes_form.addRow("Detail", self._detail)
        planes_form.addRow("", self._count)
        self._add(planes_box)

        contour_box, contour_form = form_group("Boundaries")
        self._contour = QCheckBox("Draw the plane boundaries")
        self._contour.setToolTip(
            "Line every seam between two planes, the way a construction drawing "
            "marks where the form turns"
        )
        self._contour_color = ColorButton(PlaneSettings().contour_color)
        self._contour_width = SliderSpin(
            0.5, 8.0, PlaneSettings().contour_width, decimals=1, step=0.5, suffix=" px"
        )
        contour_form.addRow("", self._contour)
        contour_form.addRow("Colour", self._contour_color)
        contour_form.addRow("Width", self._contour_width)
        self._contour_box = self._add(contour_box)

        hint = QLabel(
            "At the coarse end the form is a box of six planes, and bevels grow "
            "off its corners as you go finer.  The planes are quantised on the "
            "model rather than on the screen, so they stay put as you orbit; "
            "they filter the normals only, and work under any shading mode, "
            "matcap included."
        )
        hint.setWordWrap(True)
        hint.setStyleSheet("color: #8f939b;")
        self._add(hint)
        self._add_stretch()

        self._flat.toggled.connect(lambda v: self._apply(self.state.render, "flat_shading", v))
        self._enabled.toggled.connect(
            lambda v: self._apply(self.state.render.planes, "enabled", v)
        )
        self._detail.valueChanged.connect(
            lambda v: self._apply(self.state.render.planes, "detail", float(v))
        )
        self._contour.toggled.connect(
            lambda v: self._apply(self.state.render.planes, "show_contour", v)
        )
        self._contour_color.colorChanged.connect(
            lambda v: self._apply(self.state.render.planes, "contour_color", v)
        )
        self._contour_width.valueChanged.connect(
            lambda v: self._apply(self.state.render.planes, "contour_width", v)
        )

    # -- reactions ------------------------------------------------------

    def _apply(self, target, field: str, value) -> None:
        if self._busy:
            return
        setattr(target, field, value)
        self.state.notify_render()
        self.update_enabled()

    def update_enabled(self) -> None:
        planes = self.state.render.planes
        self._detail.setEnabled(planes.enabled)
        self._count.setText(f"Each plane covers about {planes.span_deg:.0f} deg of turn")
        self._contour_box.setEnabled(planes.enabled)
        self._contour_color.setEnabled(planes.show_contour)
        self._contour_width.setEnabled(planes.show_contour)

    def refresh(self) -> None:
        render = self.state.render
        with self._suppressed():
            self._flat.setChecked(render.flat_shading)
            self._enabled.setChecked(render.planes.enabled)
            self._detail.set_value(render.planes.detail)
            self._contour.setChecked(render.planes.show_contour)
            self._contour_color.set_color(render.planes.contour_color)
            self._contour_width.set_value(render.planes.contour_width)
        self.update_enabled()
