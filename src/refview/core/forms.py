"""Primary forms: the big simple masses a figure is blocked in with.

A primary form is not a mesh the artist has to keep; it is a set of surface
landmarks and a rule.  The pelvis is the bucket the hip points, the crests,
the sitting bones and the pubic symphysis describe; the ribcage is the egg the
breastbone, the spine and the widest ribs describe; the head is a wedge the
profile describes, and then whatever the paired landmarks add to it.  The
document holds the landmarks, and the form is worked out from them whenever
it is drawn -- so a landmark nudged is a form re-formed, and a session file
carries a dozen points rather than a dozen thousand triangles.

The forms are bone, and bone is symmetric to within less than a click's
error, so by default every form is worked out from its landmarks made
exactly symmetric about the median plane: the midline points dropped onto
it, each pair averaged across it.  The landmarks stay where the artist put
them; only the clay is straightened.

The forms are staged.  A pelvis is one stage: the landmarks go down and the
bucket appears.  A head is five, and the stages are how a head is actually
built up in clay -- a wedge first, then its width, then the block of the
cranium, then the jaw -- so the landmarks are asked for a stage at a time and
the form grows as each stage's landmarks are placed.  Every stage is kept,
and the panel's slider scrubs back through them, because the order a form
arrives in is the part a sculptor learns from.

Each preset reuses the machinery of the guided armature presets: the same
:class:`~refview.core.landmarks.Landmark` describes what to point at, the
same median plane fitted through the midline landmarks reflects one side
onto the other, and the same :class:`~refview.core.armature.PlacedLandmark`
records where the artist put each one.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field, replace

import numpy as np

from .armature import PlacedLandmark
from .convex import Solid, merged
from .form_shapes import build_head, build_pelvis, build_ribcage
from .landmarks import Landmark, Side, median_plane, mirror_point
from .mesh import Mesh, auto_smooth

Color = tuple[float, float, float]
Point3 = tuple[float, float, float]

Builder = Callable[[dict[str, np.ndarray]], list[list[Solid]]]


# ----------------------------------------------------------------------
# Presets
# ----------------------------------------------------------------------


@dataclass(frozen=True)
class FormStage:
    """One step of a form's making, and the landmarks it asks for."""

    key: str
    name: str
    #: What this stage lays down, in a sentence for the panel.
    description: str
    landmarks: tuple[Landmark, ...]


@dataclass(frozen=True)
class FormPreset:
    """A primary form: its stages, in order, and the rule that builds them."""

    key: str
    name: str
    stages: tuple[FormStage, ...]
    builder: Builder

    @property
    def landmarks(self) -> tuple[Landmark, ...]:
        """Every landmark, in the order the walk asks for them."""
        return tuple(entry for stage in self.stages for entry in stage.landmarks)

    def landmark(self, key: str) -> Landmark | None:
        for entry in self.landmarks:
            if entry.key == key:
                return entry
        return None

    def stage_of(self, key: str) -> int:
        """Which stage a landmark belongs to, or the last for an unknown key."""
        for index, stage in enumerate(self.stages):
            if any(entry.key == key for entry in stage.landmarks):
                return index
        return len(self.stages) - 1

    def centre_keys(self) -> tuple[str, ...]:
        """The midline landmarks, which are what the median plane is fitted to."""
        return tuple(entry.key for entry in self.landmarks if entry.side is Side.CENTRE)

    def build(self, placed: dict[str, np.ndarray]) -> list[list[Solid]]:
        return self.builder(placed)


def _centre(key: str, name: str, hint: str, required: bool = True) -> tuple[Landmark, ...]:
    return (Landmark(key=key, name=name, hint=hint, side=Side.CENTRE, required=required),)


def _pair(key: str, name: str, hint: str, required: bool = True) -> tuple[Landmark, ...]:
    """A left landmark, then the right one that mirrors it."""
    return (
        Landmark(key=f"{key}.L", name=name, hint=hint, side=Side.LEFT, required=required),
        Landmark(
            key=f"{key}.R",
            name=name,
            hint=hint,
            side=Side.RIGHT,
            required=required,
            mirror_of=f"{key}.L",
        ),
    )


PELVIS = FormPreset(
    key="pelvis",
    name="Pelvis",
    stages=(
        FormStage(
            key="bucket",
            name="The bucket",
            description=(
                "A tapered bucket from the rim of the hip bones down to the sitting bones, "
                "with its front corner chipped off along the plane from the two ASIS "
                "down to the pubic symphysis."
            ),
            landmarks=(
                *_centre(
                    "pubic_symphysis",
                    "Pubic symphysis",
                    "The front edge of the pelvic floor, on the midline, where the "
                    "curve of the belly ends.",
                ),
                *_centre(
                    "sacrum_top",
                    "Top of the sacrum",
                    "The flat triangle at the base of the spine, on the midline between "
                    "the two dimples.",
                ),
                *_centre(
                    "coccyx",
                    "Coccyx",
                    "The tail bone: the bottom of the sacrum, at the top of the crease "
                    "between the buttocks.",
                ),
                *_pair(
                    "iliac_crest",
                    "Iliac crest",
                    "The highest point of the rim of the hip bone, at the side of the waist.",
                ),
                *_pair("asis", "ASIS", "The front point of the hip bone, under the pocket."),
                *_pair("psis", "PSIS", "The dimple above the buttock, at the back of the rim."),
                *_pair(
                    "ischial_tuberosity",
                    "Ischial tuberosity",
                    "The sitting bone, under the fold of the buttock: the lowest point of "
                    "the pelvis.  Buried on most models -- skip it, and the bottom of "
                    "the bucket is put where the sitting bones are.",
                    required=False,
                ),
            ),
        ),
    ),
    builder=build_pelvis,
)

RIBCAGE = FormPreset(
    key="ribcage",
    name="Ribcage",
    stages=(
        FormStage(
            key="egg",
            name="The egg",
            description=(
                "An egg lofted from the thoracic inlet through the widest ribs to the "
                "lowest, bowed backward at the apex of the thoracic curve, with the arch "
                "chipped out of the front along the costal margins, point by point."
            ),
            landmarks=(
                *_centre(
                    "jugular_notch",
                    "Jugular notch",
                    "The hollow between the collarbones, at the top of the breastbone.",
                ),
                *_centre(
                    "xiphoid",
                    "Xiphoid process",
                    "The bottom of the breastbone, where the two sides of the rib arch meet.",
                ),
                *_centre(
                    "c7",
                    "C7 spinous process",
                    "The bump at the base of the neck, clearest when the head drops forward.",
                ),
                *_centre(
                    "t12",
                    "Thoracolumbar junction",
                    "In the back, level with the lowest rib: the waist of the ribcage.",
                ),
                *_centre(
                    "thoracic_apex",
                    "Apex of the thoracic curve",
                    "The spine between the shoulder blades, level with the widest ribs: "
                    "where the back bows furthest backward.",
                ),
                *_centre(
                    "sternal_angle",
                    "Sternal angle",
                    "The ridge across the breastbone a hand's width below the notch, where "
                    "the second rib joins.  It bends the front of the egg.",
                    required=False,
                ),
                *_pair(
                    "widest_rib",
                    "Widest point of the ribcage",
                    "The side of the ribcage where it is broadest, a little above the "
                    "level of the xiphoid.",
                ),
                *_pair(
                    "rib_angle",
                    "Back corner of the ribcage",
                    "Where the back of the ribcage turns forward into its side, at the "
                    "widest level: under the lower corner of the shoulder blade.  It "
                    "broadens the back of the egg.",
                    required=False,
                ),
                *_pair(
                    "front_corner",
                    "Front corner of the ribcage",
                    "Where the front of the ribcage turns into its side at the widest "
                    "level, under the outer edge of the pectoral.  It flattens the "
                    "front of the egg.",
                    required=False,
                ),
                *_pair(
                    "rectus_origin",
                    "Top corner of the rectus abdominis",
                    "Where the upper corner of the rectus abdominis meets the rib arch, "
                    "a finger's width out from the xiphoid.  The arch drops steeply "
                    "from the xiphoid to here.",
                ),
                *_pair(
                    "arch_rectus_edge",
                    "Rib arch at the edge of the rectus",
                    "Where the outer edge of the rectus abdominis crosses the rib arch: "
                    "the tip of the ninth rib, roughly under the nipple.",
                ),
                *_pair(
                    "lowest_rib",
                    "Lowest rib, at the side",
                    "Where the rib arch turns the corner at the side: the lowest front "
                    "point of the ribcage.",
                ),
            ),
        ),
    ),
    builder=build_ribcage,
)

HEAD = FormPreset(
    key="head",
    name="Head",
    stages=(
        FormStage(
            key="wedge",
            name="The wedge",
            description=(
                "The profile of the head as a thin slab, no wider than the bridge of the "
                "nose: the crown, the brow, the chin and the back of the skull."
            ),
            landmarks=(
                *_centre("vertex", "Vertex", "The highest point of the skull."),
                *_centre(
                    "glabella",
                    "Glabella",
                    "The brow: the flat between the eyebrows, above the bridge of the nose.",
                ),
                *_centre("menton", "Chin", "The lowest point of the chin, on the midline."),
                *_centre(
                    "occiput",
                    "Occiput",
                    "The back of the skull: the point furthest from the face.",
                ),
                *_centre(
                    "inion",
                    "Inion",
                    "The bump at the base of the back of the skull, where the neck muscles attach.",
                ),
                *_centre(
                    "lambda",
                    "Corner of the back of the crown",
                    "Where the top of the skull turns down into its back, on the midline: "
                    "a hand's width above the occiput.",
                ),
            ),
        ),
        FormStage(
            key="width",
            name="The width",
            description=(
                "The slab widened above and below the eyes: the cranium out to the "
                "skull, the brow corners and the ear holes; the jaw out to the "
                "cheekbones and its corners.  The eye sockets are the gap left between."
            ),
            landmarks=(
                *_pair(
                    "parietal",
                    "Parietal eminence",
                    "The widest point of the skull, above and behind the ear.",
                ),
                *_pair(
                    "tragus",
                    "Tragus",
                    "The little flap of cartilage in front of the ear hole.",
                ),
                *_pair(
                    "brow_corner",
                    "Corner of the brow",
                    "The outer end of the brow ridge, above the outer corner of the eye, "
                    "where it turns down into the temple.",
                ),
                *_pair(
                    "zygomatic",
                    "Cheekbone",
                    "The widest point of the face: the corner of the cheekbone, below "
                    "the outer eye.",
                ),
                *_pair(
                    "gonion",
                    "Angle of the jaw",
                    "The corner of the jaw, below and behind the ear lobe.",
                ),
            ),
        ),
        FormStage(
            key="cranium",
            name="The cranium",
            description=(
                "The block of the skull planed out to the bulges of the forehead, the "
                "corners of the crown, the corners of the back and the base behind the "
                "ears -- planes meeting at edges, not a ball."
            ),
            landmarks=(
                *_pair(
                    "frontal_eminence",
                    "Frontal eminence",
                    "The bulge of the forehead above the outer end of the eyebrow, a "
                    "finger's width under the hairline.",
                ),
                *_pair(
                    "back_corner",
                    "Corner of the back of the skull",
                    "Where the back of the skull turns into its side, between the corner "
                    "of the crown and the parietal eminence.",
                ),
                *_pair(
                    "mastoid",
                    "Mastoid process",
                    "The knob of bone just behind the ear lobe: the base of the skull.",
                ),
                *_pair(
                    "crown_corner",
                    "Corner of the crown",
                    "Where the top of the skull turns down into its side, straight above "
                    "the ear.  It squares the top of the cranium.",
                    required=False,
                ),
            ),
        ),
        FormStage(
            key="jaw",
            name="The jaw and muzzle",
            description=(
                "The mass of the lower face: the cheeks under the eyes, the base of the "
                "nose, the jaw and the chin as one lump, with the eye sockets left open "
                "above it."
            ),
            landmarks=(
                *_pair(
                    "infraorbital",
                    "Cheek, under the eye",
                    "The top of the cheek, just under the lower rim of the eye socket.",
                ),
                *_centre(
                    "subnasale",
                    "Base of the nose",
                    "Where the underside of the nose meets the upper lip.",
                ),
                *_centre(
                    "pogonion",
                    "Point of the chin",
                    "The most forward point of the chin.",
                    required=False,
                ),
            ),
        ),
        FormStage(
            key="nose",
            name="The nose",
            description=(
                "The first secondary form: a wedge from the root of the nose between the "
                "eyes to the tip, spread to the wings at its base, laid on the muzzle."
            ),
            landmarks=(
                *_centre(
                    "nasion",
                    "Root of the nose",
                    "The dip at the top of the bridge of the nose, between the eyes, "
                    "just below the brow.",
                ),
                *_centre("pronasale", "Tip of the nose", "The most forward point of the nose."),
                *_pair(
                    "alare",
                    "Wing of the nose",
                    "The widest point of the nostril wing.",
                ),
            ),
        ),
    ),
    builder=build_head,
)

#: Every primary form the Forms panel offers, in the order it lists them.
FORM_PRESETS: dict[str, FormPreset] = {preset.key: preset for preset in (PELVIS, RIBCAGE, HEAD)}


# ----------------------------------------------------------------------
# The document
# ----------------------------------------------------------------------


@dataclass
class PrimaryForm:
    """One primary form in the document: which preset, and where its landmarks are.

    The solids are never stored.  They are worked out from the landmarks by
    :func:`build_form` whenever the form is drawn, which is what keeps a
    dragged landmark and the form under it in step.
    """

    name: str = "Form"
    #: Key into :data:`FORM_PRESETS`.
    preset: str = ""
    landmarks: list[PlacedLandmark] = field(default_factory=list)
    #: Which stage of the making is shown, counting from zero.  Negative shows
    #: every stage that has been built, which is what a form still being
    #: placed wants: it grows as the landmarks go down.
    stage: int = -1
    visible: bool = True

    def landmark_for(self, key: str) -> PlacedLandmark | None:
        for landmark in self.landmarks:
            if landmark.key == key:
                return landmark
        return None

    def placed_points(self) -> dict[str, np.ndarray]:
        """The landmarks as a mapping a builder can read."""
        return {landmark.key: landmark.point for landmark in self.landmarks}

    def with_landmark_at(self, key: str, at: Point3) -> list[PlacedLandmark]:
        """The landmark list with one point moved, and no longer a guess.

        The same bargain the armature makes: a landmark the artist has taken
        hold of is theirs from then on, so the mirror never writes over it.
        """
        moved = tuple(float(value) for value in at)
        return [
            replace(entry, at=moved, mirrored=False) if entry.key == key else replace(entry)
            for entry in self.landmarks
        ]

    def without_landmarks(self, *keys: str) -> list[PlacedLandmark]:
        dropped = set(keys)
        return [replace(entry) for entry in self.landmarks if entry.key not in dropped]


@dataclass
class FormSettings:
    """How the forms are drawn, and how their landmarks are placed."""

    show_all: bool = True
    show_landmarks: bool = True
    #: The colour of the clay.  Terracotta, so a form reads as clay laid over
    #: the model rather than as another part of it.
    color: Color = (0.80, 0.60, 0.46)
    #: Facets turning by less than this many degrees are shaded as one curve,
    #: so a bucket sampled in forty flats reads as a bucket while its rim and
    #: the chip off its front stay as hard as they are.
    smooth: float = 40.0
    #: During a guided run, reflect each paired landmark across the median
    #: plane instead of asking for both sides.
    mirror: bool = True
    #: Build every form from its landmarks made symmetric about the median
    #: plane.  The pelvis, the ribcage and the skull are bone, and bone is as
    #: near symmetric as makes no difference; a click a little off on one side
    #: would otherwise skew the whole form.
    symmetric: bool = True
    snap_to_vertex: bool = False
    #: Pixel radius within which a click snaps to the nearest triangle corner.
    snap_pixels: float = 12.0


class FormStore:
    """An ordered, named collection of primary forms, like the other stores."""

    def __init__(self, items: list[PrimaryForm] | None = None) -> None:
        self._items: list[PrimaryForm] = list(items or [])

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index: int) -> PrimaryForm:
        return self._items[index]

    @property
    def items(self) -> list[PrimaryForm]:
        """The live list; the undo commands operate on it directly."""
        return self._items

    def add(self, form: PrimaryForm) -> PrimaryForm:
        self._items.append(form)
        return form

    def next_name(self, preset: str) -> str:
        """A name for a new form of this preset, numbered past any it already has."""
        base = FORM_PRESETS[preset].name if preset in FORM_PRESETS else "Form"
        taken = sum(1 for form in self._items if form.preset == preset)
        return base if taken == 0 else f"{base} {taken + 1}"

    def clear(self) -> None:
        self._items.clear()


# ----------------------------------------------------------------------
# Reading a form
# ----------------------------------------------------------------------


def form_landmark_title(form: PrimaryForm, key: str) -> str:
    """What to call a landmark in a list or an undo step."""
    preset = FORM_PRESETS.get(form.preset)
    entry = preset.landmark(key) if preset is not None else None
    return entry.title if entry is not None else key


def mirror_form_landmarks(form: PrimaryForm) -> list[PlacedLandmark]:
    """The landmark list with every paired landmark reflected into place.

    The armature's rule exactly: a point the artist placed or took hold of
    keeps its position for good, and only the mirror's own guesses are ever
    rewritten.  Without a median plane -- too few midline points down yet --
    nothing is guessed.
    """
    preset = FORM_PRESETS.get(form.preset)
    if preset is None:
        return list(form.landmarks)
    existing = {entry.key: entry for entry in form.landmarks}
    placed = {key: entry.point for key, entry in existing.items()}
    plane = median_plane([placed[key] for key in preset.centre_keys() if key in placed])
    if plane is None:
        return list(form.landmarks)

    origin, normal = plane
    out = list(form.landmarks)
    for entry in preset.landmarks:
        source = placed.get(entry.mirror_of) if entry.mirror_of else None
        if source is None:
            continue
        already = existing.get(entry.key)
        if already is not None and not already.mirrored:
            continue
        at = tuple(float(value) for value in mirror_point(source, origin, normal))
        if already is None:
            out.append(PlacedLandmark(key=entry.key, at=at, mirrored=True))
        else:
            already.at = at
    return out


def median_plane_ready(form: PrimaryForm) -> bool:
    """Whether enough of the midline is down for the mirror to have a plane."""
    preset = FORM_PRESETS.get(form.preset)
    if preset is None:
        return False
    placed = form.placed_points()
    return median_plane([placed[key] for key in preset.centre_keys() if key in placed]) is not None


def symmetrised_points(form: PrimaryForm) -> dict[str, np.ndarray]:
    """The placed landmarks made exactly symmetric about the median plane.

    The midline points are dropped onto the plane fitted through them, and
    each pair is replaced by the average of the two across it -- or by the
    one that is down, reflected, when only one is.  Without a plane nothing
    can be said and the points come back as they are.  Only the builder sees
    these; the landmarks the artist placed are not moved.
    """
    preset = FORM_PRESETS.get(form.preset)
    placed = form.placed_points()
    if preset is None:
        return placed
    plane = median_plane([placed[key] for key in preset.centre_keys() if key in placed])
    if plane is None:
        return placed
    origin, normal = plane
    twins = {entry.mirror_of: entry.key for entry in preset.landmarks if entry.mirror_of}
    out: dict[str, np.ndarray] = {}
    for entry in preset.landmarks:
        point = placed.get(entry.key)
        if entry.side is Side.CENTRE:
            if point is not None:
                out[entry.key] = point - float((point - origin) @ normal) * normal
            continue
        if entry.mirror_of:
            continue  # settled from its other side
        twin = twins.get(entry.key)
        other = placed.get(twin) if twin else None
        reflected = mirror_point(other, origin, normal) if other is not None else None
        if point is None and reflected is None:
            continue
        if point is None:
            point = reflected
        elif reflected is not None:
            point = 0.5 * (point + reflected)
        out[entry.key] = point
        if twin:
            out[twin] = mirror_point(point, origin, normal)
    return out


def build_form(form: PrimaryForm, symmetric: bool = False) -> list[list[Solid]]:
    """The solids of every stage the landmarks can build, coarsest first.

    A stage whose landmarks are not all down comes back empty, and so does
    every stage after it: each is laid over the ones before, so there is
    nothing to lay it over yet.  ``symmetric`` builds from the landmarks
    straightened by :func:`symmetrised_points`.
    """
    preset = FORM_PRESETS.get(form.preset)
    if preset is None:
        return []
    return preset.build(symmetrised_points(form) if symmetric else form.placed_points())


def built_count(stages: list[list[Solid]]) -> int:
    """How many stages actually have clay in them, counting from the first."""
    count = 0
    for pieces in stages:
        if not pieces:
            break
        count += 1
    return count


def shown_stages(form: PrimaryForm, stages: list[list[Solid]]) -> list[list[Solid]]:
    """The stages the form is set to show: everything up to its own, and built."""
    held = built_count(stages)
    if held == 0:
        return []
    upto = held if form.stage < 0 else min(int(form.stage) + 1, held)
    return stages[:upto]


def landmark_signature(form: PrimaryForm) -> tuple:
    """What a cache compares to know the landmarks have not moved."""
    return (form.preset, tuple((entry.key, entry.at) for entry in form.landmarks))


def stages_mesh(stages: list[list[Solid]], smooth: float, name: str = "form") -> Mesh | None:
    """The union of some stages as one mesh, shaded as clay.

    The pieces are simply drawn over one another -- a union of opaque solids
    looks like their union from outside -- and the facets are welded into
    curves wherever the turn between them is gentle.
    """
    flat = merged([piece.mesh(name) for pieces in stages for piece in pieces], name)
    if flat is None:
        return None
    return auto_smooth(flat, float(smooth))


def form_mesh(form: PrimaryForm, smooth: float, symmetric: bool = False) -> Mesh | None:
    """The form as it is to be drawn right now."""
    return stages_mesh(shown_stages(form, build_form(form, symmetric)), smooth, form.name)
