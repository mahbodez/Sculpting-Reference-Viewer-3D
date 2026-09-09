"""Everything that acts on the shading normals rather than on the shading.

Faceted shading and the planes filter both change which direction a fragment
is shaded from, so they read the same whichever shading mode is running and
belong together, away from the light and material controls.

The planes filter itself comes in two, and they are mutually exclusive because
the second contains the first: round the shading normals onto the planes of
the form, or rebuild the form out of those planes so that it really has them.
Only one group of controls is live at a time, but both stay on show -- which
of the two is on offer is the thing worth seeing at a glance.
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
from ...core.plane_solids import solid_count
from ...core.settings import (
    DETAIL_CEILING,
    DETAIL_MAX,
    DETAIL_MIN,
    MASSES_CEILING,
    MASSES_MAX,
    MASSES_MIN,
    MEDIAN_MAX,
    MEDIAN_MIN,
    MEDIAN_REACH_MAX,
    MEDIAN_REACH_MIN,
    RELAX_MAX,
    RELAX_MIN,
    SMOOTH_MAX,
    SMOOTH_MIN,
    PlaneMode,
    PlaneSettings,
    PlaneTarget,
    SculptMode,
)
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

_SCULPT_DETAIL_TIP = (
    "How many planes the form is rebuilt out of, and with them how many solids "
    "it is made of.  In stone that is cuts: the whole model starts as one block "
    "and every step to the right cuts through whichever block is holding the "
    "most air, so the hollows come back deepest first -- between the arm and "
    "the ribs, then the knees, then the face.  In clay it is lumps: the masses "
    "are already there at the coarse end and every step lays another tube into "
    "whatever the clay has not covered yet, so the arms arrive before the hands "
    "and the hands before the fingers.  Past the middle the slider spends less "
    "on solids and more on the directions they are cut along, which is what "
    "brings either one down onto the model -- a direction shaves the whole form "
    "at once where a cut opens one hollow, and past sixty lumps the clay reads "
    "as rubble rather than as masses.  Rebuilding geometry is real work, so it "
    "happens when you let go of the slider rather than as you drag.  At the "
    "end of the slider the form has every plane a fit will give it and every "
    "block or lump those planes buy; a number typed past the end spends itself "
    "on the lattice the form is worked on instead, which shows as crisper "
    "flats and straighter creases rather than as more of them, and costs -- "
    "twice as fine a lattice is eight times the corners"
)

_MASSES_TIP = (
    "How many principal masses the form is blocked in as before any detail is "
    "laid into it.  Each one is the largest rectangular block that will fit "
    "inside the model without poking out of it anywhere, pressed into whatever "
    "part of the form has the most material still uncovered -- so on a figure "
    "one is the ribcage, two adds the pelvis, four reads the legs as masses of "
    "their own, and the top of the range is every mass it has down to the "
    "feet.  How many masses a form has is a reading rather than a fact, which "
    "is why it is yours to say.  Turn Detail all the way down to see these "
    "alone; turning it up never costs them, because the detail is laid on top "
    "of the masses rather than sharing a budget with them.  The slider stops "
    "at every mass anyone reads a figure as; type a number past the end for a "
    "form that is not a figure, and the slider will take it in.  Does nothing "
    "in subtractive, which starts from a block rather than from a lump"
)

_MEDIAN_TIP = (
    "How many passes of the median filter to run over the clay volume before "
    "its surface is read back out.  Two solids crossing at an angle leave a "
    "slot between them, and a slot one cell wide is a dark slit to the eye and "
    "a spike to the thing that finds the surface; a median closes them where "
    "they are, in the volume, where there is no surface to mend yet.  It is "
    "the right filter for a form made of flats because a flat comes through it "
    "untouched -- over a neighbourhood laid evenly about a corner the values "
    "above and below its own pair off, so the median is the corner itself.  "
    "One pass takes every slot out of a figure.  Past that it starts to tell: "
    "a slot closes because it has material either side of it, and by the same "
    "arithmetic a corner is shaved because it has air on more sides than "
    "material, so more passes take the form down as well as smooth it.  Does "
    "nothing in subtractive, which has no slots and corners to keep"
)

_MEDIAN_REACH_TIP = (
    "How far each pass of the median reaches, in cells: one is the "
    "three-by-three-by-three block of corners around each corner, two is "
    "five-by-five-by-five.  Reaching further closes a wider slot in one pass "
    "and shaves the form harder for it -- on a figure, one cell leaves the "
    "volume where it was and three takes half of it away.  It also costs: the "
    "neighbourhood is a cube, so twice the reach is eight times the reading"
)

_RELAX_TIP = (
    "How many passes to run over the finished clay, settling its surface into "
    "itself -- what a sculptor does last, going over a block-in with the flat "
    "of a tool so the planes still read but the form is no longer quarried out "
    "of them.  Every pass draws each corner of the mesh towards its neighbours "
    "and then pushes it back out by a shade more, which takes the edges off "
    "without letting the form shrink, and anything that ends up outside the "
    "model is put back onto it, so relaxing can never push the clay out "
    "through the surface.  At zero you get the block-in exactly as it was cut. "
    " Does nothing in subtractive, which is meant to keep its corners"
)

_SMOOTH_TIP = (
    "How sharp a turn has to be before it is drawn as an edge rather than "
    "shaded through, in degrees -- the same knob as 3ds Max's AutoSmooth.  A "
    "facet that comes out of a lattice is only roughly one plane: its "
    "triangles each lean by a fraction of a degree, and shading every one of "
    "them on its own turns a clean flat into a mosaic.  Grouping the ones that "
    "agree to within this much takes the mosaic off and leaves every real "
    "plane change exactly as hard as it was, because a plane change is a "
    "sharper turn than this by a long way.  Nothing moves: it is a change of "
    "shading and not of shape, it costs a tenth of a second rather than a "
    "rebuild, and at zero every triangle is shaded on its own again"
)

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

_SCULPT_HINTS = {
    SculptMode.ADDITIVE: (
        "Clay.  Rectangular blocks are pressed into the model -- the largest "
        "that will fit inside it without poking out -- one to a mass, and then "
        "tubes are laid into whatever is still bare, largest first, so the arms "
        "arrive before the hands and the hands before the fingers.  Everything "
        "is joined as volume rather than as surfaces, so a tube laid across a "
        "mass leaves no seam where they meet, and the groove where two of them "
        "cross is filled with the plane that bisects them -- the material a "
        "thumb would push into the join.  Masses is the control to start with "
        "and Detail is how far the modelling is taken; read against the model's "
        "own silhouette it says how much of the form is mass and how much is "
        "detail."
    ),
    SculptMode.SUBTRACTIVE: (
        "Stone.  The form starts as the block it would be carved out of -- the "
        "convex hull of the whole model -- and every step of Detail is another "
        "cut, taken through whichever part of the block is holding the most "
        "air.  So the hollows open up deepest first, and the form is always "
        "outside the model rather than merely near it.  This is the roughing "
        "out a carver leaves at the end of the first day, and the one to reach "
        "for when you want to see where the form actually turns."
    ),
}

_SCULPT_NOTE = (
    "The model itself is never touched: this is a stand-in drawn in its place, "
    "so picking, measuring, painting and the section cut all still read the "
    "real surface underneath.  The stand-in is a mesh of its own -- its own "
    "vertices and triangles, found from the volume rather than moved from the "
    "model's -- so marks already made will sit off the flats by however far the "
    "flats moved."
)


def _summary(planes: PlaneSettings) -> str:
    """The line under the normals slider: what the setting has asked for."""
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


def _sculpt_summary(planes: PlaneSettings) -> str:
    """The line under the geometry slider: how the form is being worked."""
    solids = solid_count(planes.sculpt_count, planes.sculpt, planes.sculpt_masses)
    if planes.sculpt is SculptMode.ADDITIVE:
        tubes = solids - planes.sculpt_masses
        laid = "no tubes yet" if tubes <= 0 else f"{tubes} tubes"
        made = f"{planes.sculpt_masses} masses and {laid}"
        after = []
        if planes.sculpt_median > 0:
            reach = planes.sculpt_median_reach
            after.append(f"median {planes.sculpt_median}x at {reach} cell" + "s" * (reach > 1))
        if planes.sculpt_relax > 0:
            after.append(f"relaxed {planes.sculpt_relax}x")
        way = "clay, pressed into the model" + (
            "" if not after else ", " + " and ".join(after)
        )
    else:
        made = "one block" if solids == 1 else f"{solids} blocks"
        way = "stone, cut from the hull"
    finer = planes.sculpt_fineness
    return (
        f"{planes.sculpt_count} of {MAX_PLANE_AXES} planes over {made}, about "
        f"{planes.sculpt_span_deg:.0f} deg of turn each"
        + ("" if finer <= 1.0 else f", on a lattice {finer:.2f}x finer")
        + f"; {way}"
    )


class PlanesPanel(Panel):
    """Breaks the form into planes, in the shading or in the geometry itself."""

    def _build(self) -> None:
        box, form = form_group("Normals")
        self._flat = QCheckBox("Flat (faceted) shading")
        self._flat.setToolTip("Shade each triangle from its own face normal, showing the topology")
        form.addRow("", self._flat)
        self._add(box)

        planes_box, planes_form = form_group("Planes")
        self._enabled = QCheckBox("Break the form into planes")
        self._enabled.setToolTip(
            "Read the planes a sculptor would block this form in as, and either "
            "shade the model as though it had them or rebuild it so that it does"
        )
        self._target = QComboBox()
        for target in PlaneTarget:
            self._target.addItem(target.label, target.value)
        self._target.setToolTip(
            "Normals leaves the geometry alone and snaps every shading normal "
            "onto one of the planes, so the model reads as blocked-in flats "
            "while its silhouette stays round.  Geometry moves the surface onto "
            "those planes instead, so the form really is faceted: straight runs "
            "of silhouette, hard edges where the planes meet, and a shadow to "
            "match.  The model itself is left alone either way"
        )
        planes_form.addRow("", self._enabled)
        planes_form.addRow("Simplify", self._target)
        self._add(planes_box)

        normals_box, normals_form = form_group("Simplify normals")
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
        normals_form.addRow("Planes from", self._mode)
        normals_form.addRow("Detail", self._detail)
        normals_form.addRow("", self._count)
        self._normals_box = self._add(normals_box)

        sculpt_box, sculpt_form = form_group("Simplify geometry")
        self._sculpt = QComboBox()
        for sculpt in SculptMode:
            self._sculpt.addItem(sculpt.label, sculpt.value)
        self._sculpt.setToolTip(
            "The two ways of making a form.  Additive presses blocks of clay "
            "into the model and lays tubes into what they miss, so the result "
            "sits within the model and is smaller than it.  Subtractive starts "
            "from the block the model would be carved out of and cuts into it, "
            "so the result contains the model and is larger than it"
        )
        self._sculpt_detail = SliderSpin(
            DETAIL_MIN,
            DETAIL_MAX,
            PlaneSettings().sculpt_detail,
            decimals=0,
            step=1.0,
            ceiling=DETAIL_CEILING,
        )
        self._sculpt_detail.setToolTip(_SCULPT_DETAIL_TIP)
        self._masses = SliderSpin(
            MASSES_MIN,
            MASSES_MAX,
            PlaneSettings().sculpt_masses,
            decimals=0,
            step=1.0,
            ceiling=MASSES_CEILING,
        )
        self._masses.setToolTip(_MASSES_TIP)
        self._relax = SliderSpin(
            RELAX_MIN,
            RELAX_MAX,
            PlaneSettings().sculpt_relax,
            decimals=0,
            step=1.0,
        )
        self._relax.setToolTip(_RELAX_TIP)
        self._smooth = SliderSpin(
            SMOOTH_MIN,
            SMOOTH_MAX,
            PlaneSettings().sculpt_smooth,
            decimals=0,
            step=1.0,
        )
        self._smooth.setToolTip(_SMOOTH_TIP)
        self._median = SliderSpin(
            MEDIAN_MIN, MEDIAN_MAX, PlaneSettings().sculpt_median, decimals=0, step=1.0
        )
        self._median.setToolTip(_MEDIAN_TIP)
        self._median_reach = SliderSpin(
            MEDIAN_REACH_MIN,
            MEDIAN_REACH_MAX,
            PlaneSettings().sculpt_median_reach,
            decimals=0,
            step=1.0,
            suffix=" cells",
        )
        self._median_reach.setToolTip(_MEDIAN_REACH_TIP)
        self._sculpt_count = QLabel()
        self._sculpt_count.setStyleSheet("color: #8f939b;")
        self._sculpt_note = QLabel(_SCULPT_NOTE)
        self._sculpt_note.setWordWrap(True)
        self._sculpt_note.setStyleSheet("color: #8f939b;")
        sculpt_form.addRow("Method", self._sculpt)
        sculpt_form.addRow("Detail", self._sculpt_detail)
        sculpt_form.addRow("Masses", self._masses)
        sculpt_form.addRow("", self._sculpt_count)
        sculpt_form.addRow("", self._sculpt_note)
        self._sculpt_form = sculpt_form
        self._sculpt_box = self._add(sculpt_box)

        # What is done to the form after it has been built, which is a
        # different question from how it was built and is folded away until it
        # is asked for.
        finish_box, finish_form = collapsible_group("Finishing")
        finish_box.setToolTip(
            "The passes made over a form that has already been built: the "
            "slots closed in its volume, the corners settled on its surface, "
            "and how it is shaded"
        )
        finish_form.addRow("Median", self._median)
        finish_form.addRow("Median size", self._median_reach)
        finish_form.addRow("Relax", self._relax)
        finish_form.addRow("AutoSmooth", self._smooth)
        self._finish_form = finish_form
        self._finish_box = self._add(finish_box)

        contour_box, contour_form = form_group("Boundaries")
        self._contour = QCheckBox("Draw the plane boundaries")
        self._contour.setToolTip(
            "Line every seam between two planes, the way a construction drawing "
            "marks where the form turns.  For the normals target only: once the "
            "geometry has been cut the seams are real edges, and the wireframe "
            "or faceted shading already shows them"
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
        self._target.currentIndexChanged.connect(
            lambda i: self._apply(
                self.state.render.planes, "target", PlaneTarget(self._target.itemData(i))
            )
        )
        self._mode.currentIndexChanged.connect(
            lambda i: self._apply(
                self.state.render.planes, "mode", PlaneMode(self._mode.itemData(i))
            )
        )
        self._detail.valueChanged.connect(
            lambda v: self._apply(self.state.render.planes, "detail", float(v))
        )
        self._sculpt.currentIndexChanged.connect(
            lambda i: self._apply(
                self.state.render.planes, "sculpt", SculptMode(self._sculpt.itemData(i))
            )
        )
        # Committed rather than changed: every value a drag passes over would
        # otherwise be a fresh cut of the whole model.  The count under the
        # slider still follows the handle, so the drag is not blind.
        self._sculpt_detail.valueCommitted.connect(
            lambda v: self._apply(self.state.render.planes, "sculpt_detail", float(v))
        )
        self._sculpt_detail.valueChanged.connect(lambda _v: self.update_enabled())
        self._masses.valueCommitted.connect(
            lambda v: self._apply(self.state.render.planes, "sculpt_masses", int(v))
        )
        self._masses.valueChanged.connect(lambda _v: self.update_enabled())
        self._relax.valueCommitted.connect(
            lambda v: self._apply(self.state.render.planes, "sculpt_relax", int(v))
        )
        self._relax.valueChanged.connect(lambda _v: self.update_enabled())
        self._smooth.valueCommitted.connect(
            lambda v: self._apply(self.state.render.planes, "sculpt_smooth", float(v))
        )
        self._smooth.valueChanged.connect(lambda _v: self.update_enabled())
        for widget, field in (
            (self._median, "sculpt_median"),
            (self._median_reach, "sculpt_median_reach"),
        ):
            widget.valueCommitted.connect(
                lambda v, field=field: self._apply(self.state.render.planes, field, int(v))
            )
            widget.valueChanged.connect(lambda _v: self.update_enabled())
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
        """Show what this way of working needs, and put the rest away.

        A setting that does not apply is not greyed out but taken off the
        panel.  Half of these groups belong to one target and half to the
        other, and the two have almost nothing in common: leaving both up
        makes the panel twice as long as the work in front of you, and reading
        past a column of dead controls to find the live ones is the cost of
        that.  What is left is what this mode can actually be told.
        """
        planes = self.state.render.planes
        shading, sculpting = planes.shades_normals, planes.sculpts_geometry
        self._target.setEnabled(planes.enabled)

        self._normals_box.setVisible(shading)
        self._detail.setToolTip(_DETAIL_TIPS[planes.mode])
        self._count.setText(_summary(planes))

        self._sculpt_box.setVisible(sculpting)
        self._finish_box.setVisible(sculpting)
        # The cut waits for the slider to be let go, but the count under it
        # follows the handle, so a drag says what letting go will ask for.
        pending = PlaneSettings(
            sculpt=planes.sculpt,
            sculpt_detail=float(self._sculpt_detail.value()),
            sculpt_masses=int(self._masses.value()),
            sculpt_relax=int(self._relax.value()),
            sculpt_smooth=float(self._smooth.value()),
            sculpt_median=int(self._median.value()),
            sculpt_median_reach=int(self._median_reach.value()),
        )
        self._sculpt_count.setText(_sculpt_summary(pending))
        # None of these has anything to say to stone: it starts from a block
        # rather than from a lump, it leaves no slots between its cuts, and it
        # is meant to keep the corners it was cut with.  AutoSmooth is the one
        # that belongs to both, being a reading of a surface either way.
        clay = planes.sculpt is SculptMode.ADDITIVE
        self._sculpt_form.setRowVisible(self._masses, clay)
        for widget in (self._median, self._median_reach, self._relax):
            self._finish_form.setRowVisible(widget, clay)

        self._hint.setText(_SCULPT_HINTS[planes.sculpt] if sculpting else _HINTS[planes.mode])
        self._hint.setVisible(planes.enabled)
        # The seams are drawn by the normal quantiser; a cut form wears them as
        # real edges instead, and has no use for a line over the top.
        self._contour_box.setVisible(shading)
        self._contour_color.setEnabled(planes.show_contour)
        self._contour_width.setEnabled(planes.show_contour)
        # Grid reads nothing off the model and PCA reads only its normals, so
        # in those modes there is no design matrix for these to weigh.  The
        # geometry target always clusters the surface, so it always has one.
        self._design_box.setVisible(sculpting or (shading and planes.mode.clustered))

    def refresh(self) -> None:
        render = self.state.render
        with self._suppressed():
            self._flat.setChecked(render.flat_shading)
            self._enabled.setChecked(render.planes.enabled)
            self._target.setCurrentIndex(self._target.findData(render.planes.target.value))
            self._mode.setCurrentIndex(self._mode.findData(render.planes.mode.value))
            self._detail.set_value(render.planes.detail)
            self._sculpt.setCurrentIndex(self._sculpt.findData(render.planes.sculpt.value))
            self._sculpt_detail.set_value(render.planes.sculpt_detail)
            self._masses.set_value(render.planes.sculpt_masses)
            self._relax.set_value(render.planes.sculpt_relax)
            self._smooth.set_value(render.planes.sculpt_smooth)
            self._median.set_value(render.planes.sculpt_median)
            self._median_reach.set_value(render.planes.sculpt_median_reach)
            self._contour.setChecked(render.planes.show_contour)
            self._contour_color.set_color(render.planes.contour_color)
            self._contour_width.set_value(render.planes.contour_width)
            self._locality.set_value(render.planes.locality)
            self._coplanarity.set_value(render.planes.coplanarity)
            self._flat_span.set_value(render.planes.flat_span_deg)
        self.update_enabled()
