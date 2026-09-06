"""Everything that acts on the shading normals rather than on the shading.

Faceted shading and the planes filter both change which direction a fragment
is shaded from, so they read the same whichever shading mode is running and
belong together, away from the light and material controls.
"""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QComboBox, QLabel, QPushButton

from ...core.plane_axes import (
    COPLANARITY_RANGE,
    DEFAULT_COEFFICIENTS,
    FLAT_SPAN_RANGE,
    LOCALITY_RANGE,
    MAX_PLANE_AXES,
)
from ...core.settings import DETAIL_MAX, DETAIL_MIN, PlaneMode, PlaneSettings
from ..widgets import ColorButton, SliderSpin, collapsible_group, form_group
from .base import Panel

_COEFFICIENT_TIPS = {
    "locality": (
        "What a whole radius of travel across the form counts for against a "
        "right angle of turn in the surface.  At zero the fit reads facings "
        "only, like PCA, and two parts of the form that face the same way come "
        "back as one plane.  Raise it and the form is broken up as well as "
        "broken down, until at the top the planes are patches of surface that "
        "happen to face somewhere"
    ),
    "coplanarity": (
        "What the gap between two parallel planes counts for.  This is what "
        "keeps two patches that face alike and lie in one plane together as a "
        "single plane of the form however far apart they sit, and what "
        "separates a raised face from the one it is parallel to"
    ),
    "flat_span_deg": (
        "How far a vertex's neighbours may turn away from it before it stops "
        "counting as part of a flat.  Vertices on a rounded transition are "
        "ambiguous about which plane they belong to, so they are quieted: "
        "narrow this and only the flattest surface decides where the planes "
        "go, widen it and the turns get their say back"
    ),
}

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
    PlaneMode.REGIONS: (
        "How many planes to break the form into.  Every step splits one plane "
        "in two rather than starting the break again, so the big planes hold "
        "still while the detail arrives inside them"
    ),
    PlaneMode.FLATS: (
        "How many of the form's flats to pull out, largest first.  A step is a "
        "fresh reading of the form rather than a subdivision of the last one, "
        "so the planes shift about as you move rather than nesting"
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
        "Only the facing is read, so two parts of the form that face the same "
        "way come back as one plane however far apart they are.  The fit runs "
        "once, the first time you turn this on."
    ),
    PlaneMode.REGIONS: (
        "Reads where the surface is as well as which way it faces, so the plane "
        "of a cheek and the plane of a temple stay two planes with a seam "
        "between them.  The surface is cut into small patches and then merged "
        "back, always joining the two that cost the least, which makes the "
        "planes nest: coarse ones split into finer ones as you move right, "
        "rather than being found again.  The flats of the form get the loudest "
        "voice and the rounded turns between them the quietest, so a plane sits "
        "where the form is actually flat.  The best first thing to try."
    ),
    PlaneMode.FLATS: (
        "Asks which single plane the most surface agrees on, takes it, and asks "
        "again of what is left -- so the largest flat of the form arrives first "
        "and the rest in the order a sculptor would block them in.  Nothing is "
        "averaged, so a stray patch or a noisy scan cannot pull a plane off the "
        "flat it belongs to; the price is that the planes are found again at "
        "every step rather than subdivided, so they shift as you drag.  Reach "
        "for it when a form has real flats in it and you want those, not an "
        "even share-out of the surface."
    ),
}


def _summary(planes: PlaneSettings) -> str:
    """The line under the slider: what the setting has actually asked for."""
    if planes.mode is PlaneMode.PCA:
        return (
            f"Keeping {planes.axis_count} of {MAX_PLANE_AXES} principal "
            f"directions, about {planes.axis_span_deg:.0f} deg of turn each"
        )
    if planes.mode.fitted:
        return (
            f"{planes.axis_count} of {MAX_PLANE_AXES} planes, about "
            f"{planes.axis_span_deg:.0f} deg of turn each"
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
            "the model is.  The rest read the planes off this model itself, so "
            "they are the ones the form actually has: PCA from the facings "
            "alone, Regions and Flats from where the surface is as well"
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

        design_box, design_form = collapsible_group("Design matrix")
        design_box.setToolTip(
            "The coefficients the clustered modes weigh their design matrix "
            "with.  The defaults are chosen to read a figure; a form built out "
            "of hard flats, or one with none at all, may want otherwise"
        )
        self._locality = SliderSpin(
            *LOCALITY_RANGE, DEFAULT_COEFFICIENTS.locality, decimals=2, step=0.05
        )
        self._coplanarity = SliderSpin(
            *COPLANARITY_RANGE, DEFAULT_COEFFICIENTS.coplanarity, decimals=2, step=0.05
        )
        self._flat_span = SliderSpin(
            *FLAT_SPAN_RANGE,
            DEFAULT_COEFFICIENTS.flat_span_deg,
            decimals=0,
            step=1.0,
            suffix=" deg",
        )
        for widget, key in (
            (self._locality, "locality"),
            (self._coplanarity, "coplanarity"),
            (self._flat_span, "flat_span_deg"),
        ):
            widget.setToolTip(_COEFFICIENT_TIPS[key])
        self._reset_design = QPushButton("Reset to defaults")
        self._design_note = QLabel(
            "Changing one of these refits the model, so it takes effect when "
            "you let go of the slider rather than as you drag."
        )
        self._design_note.setWordWrap(True)
        self._design_note.setStyleSheet("color: #8f939b;")
        design_form.addRow("Position", self._locality)
        design_form.addRow("Coplanarity", self._coplanarity)
        design_form.addRow("Flat within", self._flat_span)
        design_form.addRow("", self._reset_design)
        design_form.addRow("", self._design_note)
        self._design_box = self._add(design_box)

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
        # Committed rather than changed: each of these is a refit of the whole
        # model, which is not something to do at every value a drag passes over.
        for widget, field in (
            (self._locality, "locality"),
            (self._coplanarity, "coplanarity"),
            (self._flat_span, "flat_span_deg"),
        ):
            widget.valueCommitted.connect(
                lambda v, field=field: self._apply(self.state.render.planes, field, float(v))
            )
        self._reset_design.clicked.connect(self._restore_defaults)

    # -- reactions ------------------------------------------------------

    def _apply(self, target, field: str, value) -> None:
        if self._busy:
            return
        setattr(target, field, value)
        self.state.notify_render()
        self.update_enabled()

    def _restore_defaults(self) -> None:
        """Put the design matrix back the way it reads a figure."""
        planes = self.state.render.planes
        planes.locality = DEFAULT_COEFFICIENTS.locality
        planes.coplanarity = DEFAULT_COEFFICIENTS.coplanarity
        planes.flat_span_deg = DEFAULT_COEFFICIENTS.flat_span_deg
        self.refresh()
        self.state.notify_render()

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
        # Grid reads nothing off the model and PCA reads only its normals, so
        # in those modes there is no design matrix for these to weigh.
        self._design_box.setEnabled(planes.enabled and planes.mode.clustered)

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
            self._locality.set_value(render.planes.locality)
            self._coplanarity.set_value(render.planes.coplanarity)
            self._flat_span.set_value(render.planes.flat_span_deg)
        self.update_enabled()
