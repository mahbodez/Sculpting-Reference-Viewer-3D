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

from PySide6.QtCore import QEvent, Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSlider,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ...core.commands import SetAttributes
from ...core.history import ARMATURE
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
    plane_count,
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
    "at once where a cut opens one hollow.  Rebuilding geometry is real work, so it "
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
    "in subtractive, which starts from a block rather than from a lump.\n\n"
    "Built on an armature, this is the same count read down the wire: the "
    "first few lengths of wire are laid as plain blocks and everything after "
    "them as bevelled tubes, so it says how much of the figure is blocked in "
    "square before the modelling starts"
)

_ARMATURE_TIP = (
    "Build the clay on an armature instead of letting the mode look for the "
    "masses itself.  A real armature is a wire bent to say where the masses "
    "of a figure are and how thick it is at each joint, and clay goes on top "
    "of it; this is the same thing.  One lump is laid along each length of "
    "wire, centred on it, and pushed out until the model or the thickness the "
    "wire declares stops it -- so the pelvis is the pelvis because you said "
    "so, not because it happened to be the deepest material the field could "
    "find.  Anything no bone speaks for is still found the old way, which is "
    "what puts the hands and the feet in after the block-in -- unless you "
    "untick the bone that does speak for it, which keeps the clay off that "
    "part of the form at any Detail at all.  Bend a node and the clay follows "
    "it when you let go"
)

_ORDER_TIP = (
    "The order the clay goes down in, one lump per length of wire, top of the "
    "list first.  A wire derived from a preset arrives already in the order a "
    "figure is built up -- the hips, then the ribcage, then the head, then "
    "the limbs largest mass first -- because that is the order a sculptor "
    "works in and the order the block-in reads in.  Move a row to say "
    "otherwise.  Detail decides how far down this list the clay gets, so what "
    "is at the top is what survives a coarse setting; the rows past the end "
    "of the budget are shown greyed rather than hidden, so you can see what "
    "another step of Detail would buy.\n\n"
    "Untick a row to keep the clay off that length of wire altogether -- not "
    "merely to skip its lump, but to leave that part of the form bare and "
    "keep it bare.  However far you then push Detail, nothing seeds there and "
    "nothing grows in, which is the whole point: it is the difference between "
    "the parts of a figure you want blocked in and the parts you mean to "
    "model yourself.  The bone is still wire, still drawn and measured and "
    "holding its two joints apart; it simply has no clay on it, and it gives "
    "its place in the budget to the bones after it.  How wide a berth the "
    "clay gives it is the thickness its two nodes declare, so a bone that "
    "keeps off more of the form than you meant is one whose nodes are too "
    "fat.  Material a bone you kept also reaches stays with that one, so "
    "turning the hand off does not take a bite out of the forearm.\n\n"
    "Rows come in handfuls, so they are picked in handfuls: Ctrl-click or "
    "Shift-click as many as you mean, and ticking any one of them ticks the "
    "lot, as a single step.  All and None do the whole list, which is the "
    "quick way to start from one end or the other -- None, then tick back the "
    "four bones you actually want blocked in.\n\n"
    "Both are edits of the armature, so they undo with everything else, and "
    "re-deriving a preset keeps them"
)

_MEDIAN_TIP = (
    "How many passes of the seam-filler to run over the clay volume before "
    "its surface is read back out.  Two solids crossing at an angle leave a "
    "slot between them, and a slot one cell wide is a dark slit to the eye "
    "and a spike to the thing that finds the surface; this closes them where "
    "they are, in the volume, where there is no surface to mend yet.  What a "
    "sculptor does about a slot is press clay into it, and that is all this "
    "does: it works the solid rather than the field, so a cell of a slot with "
    "material on enough sides is taken up into the form and nothing is ever "
    "taken away.  A flat comes through untouched, and so does every corner "
    "and thin wall -- which the median this replaced could not say, because a "
    "slot closed by outvoting it shaved a corner by the very same arithmetic. "
    " More passes close wider slots and cost more; none of them make the form "
    "smaller.  Does nothing in subtractive, which has no slots to fill"
)

_MEDIAN_REACH_TIP = (
    "How far each pass of the fill reaches, in cells: it grows the clay this "
    "far into a slot and then lets the surface back the same distance, which "
    "leaves the fill in the slot and nowhere else.  So the size says which "
    "slots are within reach -- one cell closes the slots two solids leave "
    "where they cross, and a wider setting reaches a wider gap.  It costs: "
    "the reach is taken along each axis in turn, so asking for more of it is "
    "more passes over the lattice"
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
        "thumb would push into the join.  Give it an armature and the wire "
        "says where the lumps go and in what order instead, and the free "
        "seeding only picks up where the wire stops reaching.  Masses is the "
        "control to start with "
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

_FILM_TIP = (
    "Record the whole making of the form rather than only its end, and scrub "
    "back and forth through it.  A block-in is a sequence before it is a "
    "shape: which mass went down first, what the second cut took off, where "
    "the thing stopped being a block and started being a body.  The modes "
    "already work that way -- stone splits the block holding the most air, "
    "over and over, and clay lays each lump into whatever the ones before it "
    "left bare -- so the order is really there to be read rather than "
    "reconstructed afterwards.  Every stage is the form exactly as the Detail "
    "slider set that far would build it, finishing passes and all, so what "
    "you scrub past is what you could stop at.  It costs a run of the mode "
    "per stage; recording happens in the background and the stages become "
    "scrubbable as they land, coarsest first"
)

_STAGE_TIP = (
    "Which stage of the making to show.  The left of the slider is the "
    "coarsest the mode admits -- for stone the plain hull, the block before "
    "any cut has been made; for clay a single mass -- and the right is the "
    "form the Detail slider is set to.  The slider grows as the recording "
    "runs, so it can be scrubbed before the film is finished.  Dragging is "
    "free: every stage was built when the film was recorded, and moving the "
    "handle only picks one"
)

_EXPORT_TIP = (
    "Write the film out as a file -- MP4, AVI, GIF or WebP -- with each stage "
    "of the making held on screen for as long as you say.  The scrub slider "
    "is for you at the machine; this is for everyone who was not there.  The "
    "frames are rendered at whatever size you ask for rather than at the size "
    "of the window, and you choose which of the helpers are in shot: a clip "
    "meant to be watched usually wants the form and nothing else"
)

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


def _sculpt_summary(planes: PlaneSettings, wires: int = 0) -> str:
    """The line under the geometry slider: how the form is being worked.

    ``wires`` is how many lengths of armature the clay has been given to
    build on, which changes what the count of solids is a count *of*: the
    first of them are the wire, and only what is left over is found by
    seeding.
    """
    solids = solid_count(planes.sculpt_count, planes.sculpt, planes.sculpt_masses)
    if planes.sculpt is SculptMode.ADDITIVE:
        tubes = solids - planes.sculpt_masses
        laid = "no tubes yet" if tubes <= 0 else f"{tubes} tubes"
        made = f"{planes.sculpt_masses} masses and {laid}"
        if wires > 0:
            on = min(wires, solids)
            rest = solids - on
            made = f"{on} lengths of wire" if on == wires else f"{on} of {wires} lengths of wire"
            if rest == 1:
                made += " and one lump beyond it"
            elif rest > 1:
                made += f" and {rest} lumps beyond it"
        after = []
        if planes.sculpt_median > 0:
            reach = planes.sculpt_median_reach
            after.append(f"filled {planes.sculpt_median}x at {reach} cell" + "s" * (reach > 1))
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

    #: The artist asked for the film to be written out to a file.  The panel
    #: knows there is a film and the window knows how to render one, so the
    #: asking happens here and the doing happens there.
    export_film_requested = Signal()

    def _build(self) -> None:
        #: Whether a film is being recorded, which holds still every setting
        #: that would change what is being recorded.  See
        #: :meth:`recording_changed`.
        self._recording = False
        #: How many stages the film in hand has, which is what says whether
        #: there is anything to export yet.
        self._stages_held = 0
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
        self._armature = QComboBox()
        self._armature.setToolTip(_ARMATURE_TIP)
        self._order = QListWidget()
        self._order.setToolTip(_ORDER_TIP)
        self._order.setAlternatingRowColors(True)
        self._order.setMinimumHeight(110)
        # Several rows at a time, because a limb is four bones and an artist
        # deciding not to block the arms in has made one decision rather than
        # eight.  Ticking any row of a selection ticks the whole of it.
        self._order.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        # Clicking a checkbox selects its row before it ticks it, so by the
        # time the tick is heard the selection it was made against is gone.
        # This is that selection, caught on the way past.  See
        # :meth:`_on_bone_toggled`.
        self._selected_at_press: set[int] = set()
        self._order.viewport().installEventFilter(self)
        self._up = QToolButton()
        self._up.setArrowType(Qt.ArrowType.UpArrow)
        self._up.setToolTip("Lay the selected length of wire earlier.")
        self._down = QToolButton()
        self._down.setArrowType(Qt.ArrowType.DownArrow)
        self._down.setToolTip("Lay the selected length of wire later.")
        self._all = QToolButton()
        self._all.setText("All")
        self._all.setToolTip("Lay clay along every length of wire.")
        self._none = QToolButton()
        self._none.setText("None")
        self._none.setToolTip(
            "Take the clay off every length of wire, leaving the armature to be "
            "drawn and measured while the form is found the way it was before "
            "there was one.  Tick the few you do want back."
        )
        self._order_row = QWidget()
        order_layout = QHBoxLayout(self._order_row)
        order_layout.setContentsMargins(0, 0, 0, 0)
        order_layout.setSpacing(4)
        order_layout.addWidget(self._order, 1)
        buttons = QWidget()
        button_layout = QVBoxLayout(buttons)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(4)
        button_layout.addWidget(self._up)
        button_layout.addWidget(self._down)
        button_layout.addSpacing(6)
        button_layout.addWidget(self._all)
        button_layout.addWidget(self._none)
        button_layout.addStretch(1)
        order_layout.addWidget(buttons)
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
        self._film = QCheckBox("Record the making, and scrub through it")
        self._film.setToolTip(_FILM_TIP)
        self._stage = QSlider(Qt.Orientation.Horizontal)
        self._stage.setToolTip(_STAGE_TIP)
        self._stage.setRange(0, 0)
        self._stage.setPageStep(1)
        self._stage_label = QLabel()
        self._stage_label.setStyleSheet("color: #8f939b;")
        self._export = QPushButton("Export Video...")
        self._export.setToolTip(_EXPORT_TIP)
        self._export.clicked.connect(self.export_film_requested.emit)
        self._recording_note = QLabel(
            "Recording. The settings the form is being built from are held "
            "still until it finishes -- scrub, or untick to stop."
        )
        self._recording_note.setWordWrap(True)
        self._recording_note.setStyleSheet("color: #c8a95a;")
        self._recording_note.setVisible(False)
        self._sculpt_note = QLabel(_SCULPT_NOTE)
        self._sculpt_note.setWordWrap(True)
        self._sculpt_note.setStyleSheet("color: #8f939b;")
        sculpt_form.addRow("Method", self._sculpt)
        sculpt_form.addRow("Detail", self._sculpt_detail)
        sculpt_form.addRow("Built on", self._armature)
        sculpt_form.addRow("Masses", self._masses)
        sculpt_form.addRow("Order", self._order_row)
        sculpt_form.addRow("", self._sculpt_count)
        sculpt_form.addRow("", self._film)
        sculpt_form.addRow("Stage", self._stage)
        sculpt_form.addRow("", self._stage_label)
        sculpt_form.addRow("", self._export)
        sculpt_form.addRow("", self._recording_note)
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
        finish_form.addRow("Fill seams", self._median)
        finish_form.addRow("Fill size", self._median_reach)
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
        self._armature.currentIndexChanged.connect(self._on_armature_picked)
        self._up.clicked.connect(lambda: self._move_bone(-1))
        self._down.clicked.connect(lambda: self._move_bone(1))
        self._all.clicked.connect(lambda: self._lay_every_bone(True))
        self._none.clicked.connect(lambda: self._lay_every_bone(False))
        self._order.itemSelectionChanged.connect(self._sync_order_buttons)
        self._order.itemChanged.connect(self._on_bone_toggled)
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
        self._film.toggled.connect(
            lambda v: self._apply(self.state.render.planes, "sculpt_film", v)
        )
        # The scrub is a lookup rather than a build, so it follows the handle
        # rather than waiting to be let go of -- that is the whole point of it.
        self._stage.valueChanged.connect(
            lambda v: self._apply(self.state.render.planes, "sculpt_stage", int(v))
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

    # -- the armature the clay is built on -------------------------------

    def _chosen_armature(self):
        """The armature the clay is being built on, or ``None``.

        An index past the end of the store reads as none rather than as an
        error: a session saved with two armatures and reopened with one has to
        come back as something, and coming back as no armature is the
        behaviour the mode had before there were any.
        """
        index = int(self.state.render.planes.sculpt_armature)
        if not 0 <= index < len(self.state.armatures):
            return None
        return self.state.armatures[index]

    def _on_armature_picked(self, row: int) -> None:
        if self._busy:
            return
        self._apply(self.state.render.planes, "sculpt_armature", int(self._armature.itemData(row)))
        self.refresh_armatures()

    def refresh_armatures(self) -> None:
        """Re-read the armatures and what the chosen one is laying down.

        Called whenever the document's armatures change, which is a node
        dragged, a preset re-derived, a wire deleted or one of these very
        reorderings.  Everything here is rebuilt rather than patched: the list
        is a dozen rows on a figure, and a panel that patches is a panel that
        disagrees with the document one day.
        """
        with self._suppressed():
            self._armature.clear()
            self._armature.addItem("None -- find the masses", -1)
            for index, armature in enumerate(self.state.armatures):
                bones = len(armature.intact_bones())
                if bones == 0:
                    continue  # nothing to lay clay along yet
                # Listed by what will be laid, but offered whenever there are
                # bones at all: an armature with every bone turned off has to
                # stay pickable, or there would be no way to turn one back on.
                laid = len(armature.laid_bones())
                count = f"{laid} bones" if laid == bones else f"{laid} of {bones} bones"
                self._armature.addItem(f"{armature.name}  ({count})", index)
            chosen = int(self.state.render.planes.sculpt_armature)
            at = self._armature.findData(chosen)
            self._armature.setCurrentIndex(max(at, 0))
        # Through the whole of it rather than only the list: how many lengths
        # of wire there are to lay on is part of the line under the sliders,
        # and a bone deleted or turned off changes that count.
        self.update_enabled()

    def _refresh_order(self) -> None:
        """The bones of the chosen armature, in the order the clay goes down.

        Every intact bone is listed, whether or not it takes clay, because the
        tick beside it is how an artist turns one back on.  Only the ones that
        do take clay are numbered, and the numbers are what the budget is
        counted against -- so turning a bone off visibly hands its place to
        the bones below it.

        The rows past what Detail has bought are greyed rather than dropped,
        because the question an artist has in front of this list is what one
        more step of the slider would buy them, and a row that is not there
        cannot answer it.
        """
        armature = self._chosen_armature()
        planes = self.state.render.planes
        budget = solid_count(
            plane_count(float(self._sculpt_detail.value())),
            planes.sculpt,
            int(self._masses.value()),
        )
        # The list is rebuilt rather than patched on every change, so what the
        # artist had picked out has to be put back on top of it -- otherwise
        # ticking one row of a selected limb would drop the rest of the limb.
        held = self._order.currentRow()
        chosen = {
            int(self._order.item(row).data(Qt.ItemDataRole.UserRole))
            for row in range(self._order.count())
            if self._order.item(row).isSelected()
        }
        with self._suppressed():
            self._order.clear()
            if armature is not None:
                where = {id(bone): at for at, bone in enumerate(armature.bones)}
                laid = 0
                for bone in armature.intact_bones():
                    count = f"{laid + 1}." if bone.laid else "--"
                    item = QListWidgetItem(f"{count}  {armature.bone_name(bone)}")
                    item.setData(Qt.ItemDataRole.UserRole, where[id(bone)])
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    item.setCheckState(
                        Qt.CheckState.Checked if bone.laid else Qt.CheckState.Unchecked
                    )
                    if not bone.laid:
                        item.setForeground(Qt.GlobalColor.gray)
                        item.setToolTip("No clay on this one; tick it to lay a lump along it.")
                    elif laid >= budget:
                        item.setForeground(Qt.GlobalColor.gray)
                        item.setToolTip("Past what Detail has bought; raise it, or move this up.")
                    self._order.addItem(item)
                    laid += bone.laid
                # The current row first and the selection after it: setting
                # the current row is itself a selection, and would otherwise
                # wipe the one being put back.
                self._order.setCurrentRow(min(held, self._order.count() - 1))
                for row in range(self._order.count()):
                    entry = self._order.item(row)
                    entry.setSelected(int(entry.data(Qt.ItemDataRole.UserRole)) in chosen)
        self._sync_order_buttons()

    def eventFilter(self, watched, event) -> bool:  # noqa: N802 - Qt naming
        """Catch the selection a click on a checkbox is about to collapse.

        Qt selects a row on the way to toggling its checkbox, so a plain click
        inside a selection has already thrown that selection away by the time
        the tick is heard -- and a tick that only ever applied to one row would
        make selecting several of them pointless.  Keyboard toggles change no
        selection at all, so they are read straight off the list instead; see
        :meth:`_on_bone_toggled`.
        """
        if watched is self._order.viewport() and event.type() == QEvent.Type.MouseButtonPress:
            self._selected_at_press = self._selected_rows()
        return super().eventFilter(watched, event)

    def _selected_rows(self) -> set[int]:
        """Which bones of the armature the picked-out rows stand for."""
        return {
            int(item.data(Qt.ItemDataRole.UserRole)) for item in self._order.selectedItems()
        }

    def _on_bone_toggled(self, item: QListWidgetItem) -> None:
        """Take lengths of wire out of the clay, or put them back.

        A tick on a row that was part of a selection carries the whole
        selection with it, because a limb is four bones and deciding not to
        block the arms in is one decision rather than four.  A tick anywhere
        else is that row alone, which is what a click on an unpicked checkbox
        looks like it should do.
        """
        if self._busy:
            return
        armature = self._chosen_armature()
        position = int(item.data(Qt.ItemDataRole.UserRole))
        if armature is None or not 0 <= position < len(armature.bones):
            return
        laid = item.checkState() is Qt.CheckState.Checked
        if laid == armature.bones[position].laid:
            return
        rows = self._selected_rows()
        if position not in rows or len(rows) <= 1:
            rows = self._selected_at_press
        self._lay_bones(rows if position in rows and len(rows) > 1 else [position], laid)

    def _lay_every_bone(self, laid: bool) -> None:
        """Put the clay on all of the wire, or take it off all of it."""
        armature = self._chosen_armature()
        if armature is None:
            return
        self._lay_bones(range(len(armature.bones)), laid, whole=True)

    def _lay_bones(self, positions, laid: bool, whole: bool = False) -> None:
        """Write which lengths of wire take clay, as one undoable step."""
        armature = self._chosen_armature()
        if armature is None:
            return
        rows = [row for row in positions if 0 <= row < len(armature.bones)]
        bones = armature.with_bones_laid(rows, laid)
        if [bone.laid for bone in bones] == [bone.laid for bone in armature.bones]:
            return  # nothing to say, so nothing to undo
        verb = "Lay" if laid else "Skip"
        if whole:
            what = "every length of wire"
        elif len(rows) == 1:
            what = armature.bone_name(armature.bones[rows[0]])
        else:
            what = f"{len(rows)} lengths of wire"
        self.state.do(
            SetAttributes(armature, {"bones": bones}, text=f"{verb} {what}", channel=ARMATURE)
        )
        self.refresh_armatures()
        self.update_enabled()

    def _sync_order_buttons(self) -> None:
        """What can be done to the list, given where the handle is and whether
        a film is being recorded from it."""
        row, last = self._order.currentRow(), self._order.count() - 1
        settled = not self._recording
        # The list edits the armature the film is being recorded from, so it
        # holds still for the duration along with everything else that would
        # change what is being recorded.
        self._order.setEnabled(settled)
        self._up.setEnabled(settled and row > 0)
        self._down.setEnabled(settled and 0 <= row < last)
        self._all.setEnabled(settled and last >= 0)
        self._none.setEnabled(settled and last >= 0)

    def _move_bone(self, offset: int) -> None:
        """Lay one length of wire earlier or later, as one undoable step."""
        armature = self._chosen_armature()
        item = self._order.currentItem()
        if armature is None or item is None:
            return
        position = int(item.data(Qt.ItemDataRole.UserRole))
        if not 0 <= position < len(armature.bones):
            return
        bone = armature.bones[position]
        bones = armature.with_bone_moved(position, offset)
        if bones == armature.bones:
            return
        # Only the laying order moves, so the armature stays derived from its
        # preset: nothing about the wire itself has been touched.
        self.state.do(
            SetAttributes(
                armature,
                {"bones": bones},
                text=f"Lay {armature.bone_name(bone)} {'earlier' if offset < 0 else 'later'}",
                channel=ARMATURE,
            )
        )
        self.refresh_armatures()
        # The bones are the same objects in a new order, so the row to follow
        # the move to is the one holding the very bone that moved -- which is
        # what lets the button be pressed twice to move something twice.
        rows = [id(entry) for entry in armature.intact_bones()]
        if id(bone) in rows:
            self._order.setCurrentRow(rows.index(id(bone)))

    def _restore_defaults(self) -> None:
        """Put the design matrix back the way it reads a figure."""
        planes = self.state.render.planes
        planes.locality = DEFAULT_COEFFICIENTS.locality
        planes.coplanarity = DEFAULT_COEFFICIENTS.coplanarity
        planes.flat_span_deg = DEFAULT_COEFFICIENTS.flat_span_deg
        self.refresh()
        self.state.notify_render()

    def recording_changed(self, recording: bool) -> None:
        """Hold the settings a recording is built from still while it runs.

        A film is a walk through one set of settings, and changing one of them
        part way through does not make a film of the new settings -- it makes
        a recording of one form wearing the label of another.  So the controls
        a stage is built from go to sleep for the duration.

        The scrub slider deliberately does not: it picks among stages already
        recorded rather than asking for new ones, and being able to watch the
        form arrive while it is still arriving is the point of recording in
        the background at all.  Nor does AutoSmooth, which re-reads normals
        and cannot change a stage's shape.
        """
        self._recording = bool(recording)
        if self._recording:
            # A recording that has just started is a film with nothing in it,
            # whatever the last one held.
            self._stages_held = 0
        self.update_enabled()

    def film_changed(self, film) -> None:
        """Size the scrub slider to the film as it is recorded.

        The stages arrive one at a time, so the slider grows under the handle
        rather than appearing whole at the end.  Where the handle is stays put
        unless the film has grown past it and it was sitting at the end, in
        which case it follows -- so leaving it at the right-hand end means
        "show me the newest stage" and it keeps up with the recording.
        """
        if film is None:
            return
        planes = self.state.render.planes
        self._stages_held = len(film)
        self._export.setEnabled(self._stages_held > 0)
        last = max(len(film) - 1, 0)
        # Sitting at the end means "show me the newest stage", so the handle
        # follows the recording rather than being left behind by it.  A slider
        # that has not been dragged yet counts as at the end: the first stage
        # arrives with the handle at zero and the maximum still zero, and a
        # film that grew away from it under the artist's nose would be worse
        # than one that keeps up.
        at_end = self._stage.value() >= self._stage.maximum()
        with self._suppressed():
            self._stage.setRange(0, last)
            if at_end or self._stage.value() > last:
                self._stage.setValue(last)
                planes.sculpt_stage = last
        self._film_note(film)

    def _film_note(self, film) -> None:
        """The line under the scrub handle: which stage, and of how many."""
        if film is None or not len(film):
            self._stage_label.setText("Recording...")
            return
        stage = film.at(self._stage.value())
        of = f"of {len(film)}" if film.complete else f"of {len(film)} so far"
        where = ""
        if stage is not None:
            # A stage the sliders cannot reach says so rather than naming a
            # setting that would give you something else.
            back = "" if stage.planes is None else f", Detail {stage.planes}"
            where = f" -- {stage.label}{back}"
        self._stage_label.setText(f"Stage {self._stage.value() + 1} {of}{where}")

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
        armature = self._chosen_armature()
        wires = 0 if armature is None else len(armature.laid_bones())
        self._sculpt_count.setText(_sculpt_summary(pending, wires))
        # None of these has anything to say to stone: it starts from a block
        # rather than from a lump, it leaves no slots between its cuts, and it
        # is meant to keep the corners it was cut with.  AutoSmooth is the one
        # that belongs to both, being a reading of a surface either way.
        clay = planes.sculpt is SculptMode.ADDITIVE
        self._sculpt_form.setRowVisible(self._masses, clay)
        # Stone is cut out of a block rather than built up on anything, so it
        # has no use for a wire; and the order of the bones is only worth
        # showing once there is an armature whose bones they are.
        self._sculpt_form.setRowVisible(self._armature, clay)
        self._sculpt_form.setRowVisible(self._order_row, clay and armature is not None)
        for widget in (self._median, self._median_reach, self._relax):
            self._finish_form.setRowVisible(widget, clay)
        # The scrub only means anything once there is a film to scrub, so the
        # slider and its note come and go with the checkbox rather than
        # sitting there dead.
        self._sculpt_form.setRowVisible(self._stage, planes.sculpt_film)
        self._sculpt_form.setRowVisible(self._stage_label, planes.sculpt_film)
        # The export goes with them, and is dead until there is something
        # recorded to export.  A film still being recorded can be exported as
        # far as it has got, which is deliberate: a recording abandoned half
        # way is still a making, and waiting for a minute of work you have
        # already decided not to want is a strange thing to insist on.
        self._sculpt_form.setRowVisible(self._export, planes.sculpt_film)
        self._export.setEnabled(self._stages_held > 0)

        # While a film is being recorded, everything it is being recorded
        # *from* is held still.  Changing one of these mid-recording would
        # abandon the film and start another, which is a minute of work
        # thrown away for a slider the artist may only have brushed past --
        # and the settings a stage was built from have to be the settings the
        # stage is labelled with, or the scrub is lying about what it shows.
        settled = not self._recording
        for widget in (
            self._sculpt,
            self._sculpt_detail,
            self._armature,
            self._masses,
            self._median,
            self._median_reach,
            self._relax,
            self._locality,
            self._coplanarity,
            self._flat_span,
            self._reset_design,
            self._mode,
        ):
            widget.setEnabled(settled)
        # The target picker is only live when the filter is on at all, and
        # never while a film is being made of the target it would switch away
        # from.
        self._target.setEnabled(planes.enabled and settled)
        # These two stay live on purpose.  The scrub picks among stages that
        # are already recorded, which is the whole reason for recording in the
        # background; AutoSmooth only re-reads normals and cannot change a
        # stage's shape.  Turning the film off is how you cancel a recording,
        # so it has to stay reachable as well.
        self._enabled.setEnabled(True)
        self._film.setEnabled(True)
        self._stage.setEnabled(True)
        self._smooth.setEnabled(True)
        self._recording_note.setVisible(self._recording)
        # The list greys out whatever Detail has not bought, so it has to be
        # re-read when Detail moves and not only when the armature does.
        if clay and armature is not None:
            self._refresh_order()
        else:
            self._sync_order_buttons()

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
            self._film.setChecked(render.planes.sculpt_film)
            self._stage.setValue(int(render.planes.sculpt_stage))
            self._contour.setChecked(render.planes.show_contour)
            self._contour_color.set_color(render.planes.contour_color)
            self._contour_width.set_value(render.planes.contour_width)
            self._locality.set_value(render.planes.locality)
            self._coplanarity.set_value(render.planes.coplanarity)
            self._flat_span.set_value(render.planes.flat_span_deg)
        self.refresh_armatures()  # which ends in update_enabled
