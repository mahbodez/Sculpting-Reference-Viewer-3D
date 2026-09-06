"""Everything that acts on the shading normals rather than on the shading.

Faceted shading and the planes filter both change which direction a fragment
is shaded from, so they read the same whichever shading mode is running and
belong together, away from the light and material controls.
"""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QComboBox, QLabel

from ...core.plane_axes import MAX_PLANE_AXES
from ...core.settings import DETAIL_MAX, DETAIL_MIN, PlaneMode, PlaneSettings
from ..widgets import ColorButton, SliderSpin, form_group
from .base import Panel

_DETAIL_TIPS = {
    PlaneMode.GRID: (
        "Large, blocked-in planes on the left; finer ones on the right.  The "
        "slider moves the size of a plane evenly, so a step at the coarse end "
        "changes as much as a step at the fine end"
    ),
    PlaneMode.PCA: (
        "The fraction of the model's principal directions to keep.  Every step "
        "adds a plane, and the planes it adds are the next most telling ones, "
        "so the big forms arrive first and the detail after them"
    ),
}

_HINTS = {
    PlaneMode.GRID: (
        "At the coarse end the form is a box of six planes, and bevels grow off "
        "its corners as you go finer.  The planes are quantised on the model "
        "rather than on the screen, so they stay put as you orbit; they filter "
        "the normals only, and work under any shading mode, matcap included."
    ),
    PlaneMode.PCA: (
        "Every vertex normal is read as a point on the sphere, weighted by the "
        "surface it stands for, and that cloud is split along its principal "
        "axes until it has broken into the number of planes you ask for.  The "
        "directions are the model's own, so they follow the plane of a cheek or "
        "the underside of a brow rather than a box the model happens to sit in. "
        "The fit runs once, the first time you turn this on."
    ),
}


def _summary(planes: PlaneSettings) -> str:
    """The line under the slider: what the setting has actually asked for."""
    if planes.mode is PlaneMode.PCA:
        return (
            f"Keeping {planes.axis_count} of {MAX_PLANE_AXES} principal "
            f"directions, about {planes.axis_span_deg:.0f} deg of turn each"
        )
    return f"Each plane covers about {planes.span_deg:.0f} deg of turn"


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
        self._mode = QComboBox()
        for mode in PlaneMode:
            self._mode.addItem(mode.label, mode.value)
        self._mode.setToolTip(
            "Grid rounds every normal onto the same set of directions whatever "
            "the model is.  PCA reads the directions off this model's own "
            "normals, so the planes are the ones the form actually has"
        )
        self._detail = SliderSpin(
            DETAIL_MIN, DETAIL_MAX, PlaneSettings().detail, decimals=0, step=1.0
        )
        self._count = QLabel()
        self._count.setStyleSheet("color: #8f939b;")
        planes_form.addRow("", self._enabled)
        planes_form.addRow("Planes from", self._mode)
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

        self._hint = QLabel()
        self._hint.setWordWrap(True)
        self._hint.setStyleSheet("color: #8f939b;")
        self._add(self._hint)
        self._add_stretch()

        self._flat.toggled.connect(lambda v: self._apply(self.state.render, "flat_shading", v))
        self._enabled.toggled.connect(
            lambda v: self._apply(self.state.render.planes, "enabled", v)
        )
        self._mode.currentIndexChanged.connect(
            lambda i: self._apply(
                self.state.render.planes, "mode", PlaneMode(self._mode.itemData(i))
            )
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
        self._mode.setEnabled(planes.enabled)
        self._detail.setEnabled(planes.enabled)
        self._detail.setToolTip(_DETAIL_TIPS[planes.mode])
        self._count.setText(_summary(planes))
        self._hint.setText(_HINTS[planes.mode])
        self._contour_box.setEnabled(planes.enabled)
        self._contour_color.setEnabled(planes.show_contour)
        self._contour_width.setEnabled(planes.show_contour)

    def refresh(self) -> None:
        render = self.state.render
        with self._suppressed():
            self._flat.setChecked(render.flat_shading)
            self._enabled.setChecked(render.planes.enabled)
            self._mode.setCurrentIndex(self._mode.findData(render.planes.mode.value))
            self._detail.set_value(render.planes.detail)
            self._contour.setChecked(render.planes.show_contour)
            self._contour_color.set_color(render.planes.contour_color)
            self._contour_width.set_value(render.planes.contour_width)
        self.update_enabled()
