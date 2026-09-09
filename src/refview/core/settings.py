"""Serialisable description of how the object should be shaded.

Every value here maps onto a shader uniform or a draw-state toggle; the UI
panels edit these dataclasses and nothing else.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum

from .pedestal import PedestalSettings
from .plane_axes import DEFAULT_COEFFICIENTS, MAX_PLANE_AXES, Coefficients
from .section import SectionSettings

Color = tuple[float, float, float]


class ShadingMode(str, Enum):
    """Shading model applied to the mesh.

    ``shader_id`` must stay in sync with the branch constants in
    :mod:`refview.render.shaders`.
    """

    MATCAP = "matcap"
    LAMBERT = "lambert"
    PHONG = "phong"
    BLINN_PHONG = "blinn_phong"
    PBR = "pbr"
    NORMALS = "normals"
    HIGH_QUALITY = "high_quality"

    @property
    def label(self) -> str:
        return {
            ShadingMode.MATCAP: "Matcap",
            ShadingMode.LAMBERT: "Lambert",
            ShadingMode.PHONG: "Phong",
            ShadingMode.BLINN_PHONG: "Blinn-Phong",
            ShadingMode.PBR: "PBR (GGX)",
            ShadingMode.NORMALS: "Normals",
            ShadingMode.HIGH_QUALITY: "High Quality",
        }[self]

    @property
    def shader_id(self) -> int:
        return list(ShadingMode).index(self)

    @property
    def uses_matcap(self) -> bool:
        return self is ShadingMode.MATCAP

    @property
    def uses_lighting(self) -> bool:
        return self in (
            ShadingMode.LAMBERT,
            ShadingMode.PHONG,
            ShadingMode.BLINN_PHONG,
            ShadingMode.PBR,
            ShadingMode.HIGH_QUALITY,
        )

    @property
    def uses_quality(self) -> bool:
        """Whether the shadow and occlusion pre-passes need to run."""
        return self is ShadingMode.HIGH_QUALITY


@dataclass
class MatcapSettings:
    """Post-processing applied to the sampled matcap texel."""

    rotation_deg: float = 0.0
    contrast: float = 1.0
    gamma: float = 1.0
    brightness: float = 1.0
    saturation: float = 1.0
    tint: Color = (1.0, 1.0, 1.0)
    flip_y: bool = False


@dataclass
class LightSettings:
    """A key light, an opposing fill and a hemispherical ambient term."""

    azimuth_deg: float = 40.0
    elevation_deg: float = 35.0
    color: Color = (1.0, 0.98, 0.95)
    intensity: float = 1.0
    fill_intensity: float = 0.25
    ambient_color: Color = (0.42, 0.47, 0.55)
    ambient_intensity: float = 0.30
    #: When true the light stays fixed relative to the camera, like a head lamp.
    follow_camera: bool = True


@dataclass
class SurfaceSettings:
    """Material parameters shared by the analytic shading modes."""

    diffuse_color: Color = (0.72, 0.70, 0.68)
    specular_color: Color = (1.0, 1.0, 1.0)
    specular_level: float = 0.4
    shininess: float = 32.0
    metalness: float = 0.0
    roughness: float = 0.40
    reflection_color: Color = (1.0, 1.0, 1.0)


@dataclass
class QualitySettings:
    """Soft shadows and ambient occlusion for the high-quality mode.

    Both are screen- and light-space approximations rather than traced rays:
    the point is a reference view that stays interactive while you turn it.
    """

    #: How dark a fully shadowed surface goes, 0 (off) to 1.
    shadow_strength: float = 0.55
    #: Radius of the shadow-map blur, in shadow texels.  Larger reads softer.
    shadow_softness: float = 2.0
    #: Depth offset that keeps a lit surface from shadowing itself.
    shadow_bias: float = 0.0022
    #: Occlusion sampling radius, as a share of the scene radius.
    ao_radius: float = 0.09
    #: How strongly cavities darken, 0 (off) to 1.
    ao_intensity: float = 0.85
    show_shadows: bool = True
    show_occlusion: bool = True


class PlaneTarget(str, Enum):
    """What the planes filter is allowed to act on.

    The two are mutually exclusive because they are two answers to the same
    question and the second contains the first: once the form has been rebuilt
    out of flats, quantising the normals over the top of it has nothing left
    to round.
    """

    NORMALS = "normals"
    GEOMETRY = "geometry"

    @property
    def label(self) -> str:
        return {
            PlaneTarget.NORMALS: "Simplify Normals",
            PlaneTarget.GEOMETRY: "Simplify Geometry",
        }[self]


class SculptMode(str, Enum):
    """Which side of the surface the planes are worked from.

    The two ways of making a form: clay is added from the inside out and stone
    is cut from the outside in, and the same set of planes read either way
    gives a form that sits inside the model or one that sits outside it.
    """

    ADDITIVE = "additive"
    SUBTRACTIVE = "subtractive"

    @property
    def label(self) -> str:
        return {
            SculptMode.ADDITIVE: "Additive (build up, like clay)",
            SculptMode.SUBTRACTIVE: "Subtractive (cut back, like stone)",
        }[self]


class PlaneMode(str, Enum):
    """How the plane directions are arrived at.

    ``shader_id`` must stay in sync with the branch constants in
    :mod:`refview.render.shaders`.
    """

    GRID = "grid"
    PCA = "pca"
    REGIONS = "regions"
    FLATS = "flats"

    @property
    def label(self) -> str:
        return {
            PlaneMode.GRID: "Grid",
            PlaneMode.PCA: "PCA (directions only)",
            PlaneMode.REGIONS: "Regions (merged patches)",
            PlaneMode.FLATS: "Flats (largest first)",
        }[self]

    @property
    def fitted(self) -> bool:
        """Whether the directions are read off the model rather than imposed."""
        return self is not PlaneMode.GRID

    @property
    def clustered(self) -> bool:
        """Whether the mode reads the design matrix, and so its coefficients.

        Grid reads nothing off the model and PCA reads only the normals, so
        neither has any use for them.
        """
        return self in (PlaneMode.REGIONS, PlaneMode.FLATS)

    @property
    def shader_id(self) -> int:
        return list(PlaneMode).index(self)


#: Ends of the Planes detail slider.
DETAIL_MIN, DETAIL_MAX = 0.0, 100.0
#: How far past the end of the geometry slider a value may be typed.
#:
#: At its own end the slider has already asked for every plane a fit will give
#: and every block or lump those planes buy; measured on a figure, going past
#: that buys nothing at all -- twice the planes moved the carving by a
#: hundredth of its volume.  What is holding it there is the lattice the form
#: is worked on, not the reading of the form, so that is what a typed value
#: lifts: the same reading, resolved finer.  It shows as crisper flats and
#: straighter creases rather than as more of them, it is the only thing left
#: that does show, and it costs -- the lattice is three-dimensional, so twice
#: as fine is eight times the corners, and the rebuild goes from about three
#: seconds to about eight.  Two hundred is where the lattice runs into its own
#: memory ceiling and stops getting finer, so there is no point offering more.
DETAIL_CEILING = 200.0
#: Ends of the masses slider: how many principal blocks an additive block-in
#: is built on before any detail is laid into it.  One is a single lump in the
#: largest mass of the form; thirty-two is every mass a standing figure has and
#: then some -- head, neck, ribcage, pelvis, and upper arm, forearm, hand,
#: thigh, shin and foot twice over comes to twenty-one.  The blocks stay clean
#: all the way up, because a mass is a plain box and boxes stacked along a limb
#: do not fight each other the way bevelled tubes crossing at angles do.
#: Sixty-four is past every mass anyone reads a figure as; the slider stops
#: there because that is where the useful range stops, and a number may be
#: typed past it up to the ceiling for a form that is not a figure at all.
MASSES_MIN, MASSES_MAX = 1, 64
MASSES_CEILING = 256
#: Ends of the relax slider: how many passes are run over a finished additive
#: block-in to take the corners off it.  Zero leaves it as it was cut, which is
#: the block-in proper; twenty is as far as it has anywhere left to settle to.
RELAX_MIN, RELAX_MAX = 0, 20
#: Ends of the AutoSmooth slider, in degrees of turn.  Zero shades every facet
#: on its own, which is the form exactly as it was built; ninety joins every
#: edge that is not a fold back on itself.  Thirty is the usual reading of a
#: blocked-in form: a plane change is a plane change and anything gentler was
#: the lattice, not the sculptor.
SMOOTH_MIN, SMOOTH_MAX = 0.0, 90.0
#: Ends of the two median sliders: how many passes of the filter that closes
#: the clay's slots are run, and how far each pass reaches, in cells.
#:
#: Both are short ranges because a median cuts both ways.  A slot has material
#: either side of it and closes; a convex corner has air on more sides than
#: material and is shaved.  One pass reaching one cell takes the slots out and
#: leaves the form its size; past that the shaving starts to win, and at the
#: far corner of the two ranges most of the form has gone with it.
MEDIAN_MIN, MEDIAN_MAX = 0, 6
MEDIAN_REACH_MIN, MEDIAN_REACH_MAX = 1, 3
#: How much of a turn one plane covers at either end of that slider.  The
#: coarse end is 90 degrees, which is exactly the six planes of a blocked-in
#: box; the fine end is small enough that only the sheen still facets.
COARSEST_SPAN_DEG, FINEST_SPAN_DEG = 90.0, 8.0


def _along(detail: float) -> float:
    """Where a detail setting sits on its slider, 0 to 1."""
    return min(max((detail - DETAIL_MIN) / (DETAIL_MAX - DETAIL_MIN), 0.0), 1.0)


def lattice_fineness(detail: float) -> float:
    """How much finer than usual a detail setting asks the lattice to be.

    One at the slider's own end and everywhere below it, so nothing about a
    setting anyone has ever saved changes; above it, in step with how far past
    the end the number was typed.  See :data:`DETAIL_CEILING` for why this is
    what the extra range buys rather than more planes.
    """
    return max((detail - DETAIL_MIN) / (DETAIL_MAX - DETAIL_MIN), 1.0)


def plane_count(detail: float) -> int:
    """How many planes a detail setting asks for.  See :attr:`PlaneSettings.axis_count`."""
    count = round(2.0 * (max(MAX_PLANE_AXES, 2) / 2.0) ** _along(detail))
    return min(max(int(count), 2), MAX_PLANE_AXES)


def plane_span_deg(count: int) -> float:
    """Roughly how much of a turn one of ``count`` planes covers, in degrees.

    The directions share the sphere out between them, so a plane holds about
    ``4 pi / count`` of solid angle; this is the width of a round patch that
    size.  It is what lets the boundary lines fade where the planes themselves
    have shrunk to a pixel or two, and it gives the panel a number in the same
    units as the grid mode's.
    """
    share = 2.0 / max(int(count), 1)
    return math.degrees(2.0 * math.acos(min(max(1.0 - share, -1.0), 1.0)))


@dataclass
class PlaneSettings:
    """Discretisation of the shading normals into the planes of the form.

    A sculptor blocks a head in as flats before rounding anything off, and a
    draughtsman reads those same planes to place a shadow.  This snaps every
    shading normal onto a small set of directions so the model is seen that
    way, and it filters the normals only, so it applies whichever shading
    model is running: matcap, an analytic light rig or the normals view.

    :attr:`target` switches that for the other half of the same idea, in
    :mod:`refview.core.plane_solids`: rather than shading the form as though
    it were flats, rebuild it out of them.  That one moves geometry, so it
    draws a stand-in and leaves the model alone.
    """

    enabled: bool = False
    #: Whether the planes are used to round the shading normals or to rebuild
    #: the form itself.  The two are mutually exclusive; see
    #: :class:`PlaneTarget`.
    target: PlaneTarget = PlaneTarget.NORMALS
    #: Whether the directions come off a fixed grid or out of the model.
    mode: PlaneMode = PlaneMode.GRID
    #: Where the slider sits between the coarsest planes and the finest.  It
    #: reads through to :attr:`span_deg` rather than to a count of planes,
    #: because the size of a plane is what the eye judges, and a slider that
    #: moves it evenly is one that behaves the same at both ends.
    detail: float = 60.0
    #: Which side of the surface :attr:`PlaneTarget.GEOMETRY` works the planes
    #: from.  Stone by default: a roughed-out form still reaches as far as the
    #: model does, which is the less startling of the two to arrive at.
    sculpt: SculptMode = SculptMode.SUBTRACTIVE
    #: Where the geometry slider sits.  Kept apart from :attr:`detail` because
    #: the two are different jobs at different costs -- rounding a normal is
    #: free and rebuilding a form is not -- and each wants its own working
    #: point to come back to.  It reads through to a count of planes the same
    #: way :attr:`axis_count` does.  It starts a little left of the middle,
    #: which for stone is a dozen or so cuts into the block: enough that the
    #: figure is plainly there and coarse enough that it still reads as
    #: roughed out rather than finished.
    sculpt_detail: float = 60.0
    #: How many principal masses an additive block-in is built on: the
    #: rectangular blocks pressed into the form before any detail is laid into
    #: it.  How many masses a figure has is a reading rather than a fact -- a
    #: torso is one mass or two depending on who is looking -- so this is asked
    #: for rather than worked out.  Four is a figure read as ribcage, pelvis
    #: and the two masses of the legs; the top of the range is every mass it
    #: has, down to the feet.  It says nothing to stone, which starts from a
    #: block rather than from a lump.
    sculpt_masses: int = 4
    #: How many passes are run over the finished clay to settle its surface
    #: into itself -- what a sculptor does last, going over a block-in with the
    #: flat of a tool so the planes still read but the form is no longer
    #: quarried out of them.  Off by default, because the block-in as cut is
    #: the thing this mode is for and the softening is a choice on top of it.
    #: It says nothing to stone, which is meant to keep its corners.
    sculpt_relax: int = 0
    #: How sharp a turn has to be before it is shaded as an edge rather than
    #: averaged away, in degrees.  The same knob as 3ds Max's AutoSmooth and
    #: the same default: a facet that comes out of a lattice is only roughly
    #: one plane, and shading each of its triangles on its own turns a clean
    #: flat into a mosaic.  Thirty degrees takes that off without touching a
    #: single real plane change.  Zero leaves every triangle to itself.
    sculpt_smooth: float = 30.0
    #: How many passes of the median filter are run over the finished clay
    #: volume, before its surface is read back out, to close the slots two
    #: solids leave where they cross.  One is enough to take every slot out of
    #: a figure; see :data:`MEDIAN_MIN`.  It says nothing to stone, which has
    #: no slots to close and corners it is meant to keep.
    sculpt_median: int = 1
    #: How far each of those passes reaches, in cells.  One is the
    #: three-by-three-by-three neighbourhood around a corner.
    sculpt_median_reach: int = 1
    #: What a step across the form counts for against a turn in the surface,
    #: when the mode is one that reads the surface.  See
    #: :class:`~refview.core.plane_axes.Coefficients`; these three are the same
    #: numbers, kept here so a session remembers them.
    locality: float = DEFAULT_COEFFICIENTS.locality
    coplanarity: float = DEFAULT_COEFFICIENTS.coplanarity
    flat_span_deg: float = DEFAULT_COEFFICIENTS.flat_span_deg
    #: Draw the seams between the planes, the way a construction drawing puts
    #: a line where the form turns.
    show_contour: bool = False
    contour_color: Color = (0.08, 0.09, 0.11)
    #: Line thickness, in logical pixels, held at that width at any zoom.
    contour_width: float = 1.5

    @property
    def span_deg(self) -> float:
        """How much of a turn in the surface one plane covers, in degrees.

        Linear in :attr:`detail`, so every step of the slider changes the
        planes by the same amount whether they are large or small.
        """
        return COARSEST_SPAN_DEG + _along(self.detail) * (FINEST_SPAN_DEG - COARSEST_SPAN_DEG)

    @property
    def cell_size(self) -> float:
        """The grid step, in cube-face coordinates, that gives that span.

        A cell of this size on the face of the cube subtends :attr:`span_deg`
        seen from the centre, which is what the shader quantises against.
        """
        return 2.0 * math.tan(math.radians(self.span_deg) / 2.0)

    @property
    def coefficients(self) -> Coefficients:
        """The design-matrix settings, in the form the fitters want them."""
        return Coefficients(
            locality=self.locality,
            coplanarity=self.coplanarity,
            flat_span_deg=self.flat_span_deg,
        )

    @property
    def axis_count(self) -> int:
        """How many planes a mode fitted to the model keeps.

        The climb from two planes to :data:`MAX_PLANE_AXES` is geometric
        rather than straight, because that is how the eye reads it: going from
        four planes to five redraws the form, going from two hundred to two
        hundred and one is invisible.  A step of the slider is therefore a
        roughly constant *proportion* more planes, which keeps the coarse end
        -- where the blocking-in happens, and where a single plane matters --
        controllable at the same time as the fine end reaches into the
        hundreds.  Two is the floor: one direction would shade the whole model
        as a single plane.
        """
        return plane_count(self.detail)

    @property
    def axis_span_deg(self) -> float:
        """Roughly how much of a turn one of those planes covers, in degrees."""
        return plane_span_deg(self.axis_count)

    @property
    def plane_span_deg(self) -> float:
        """The plane size of whichever mode is running."""
        return self.axis_span_deg if self.mode.fitted else self.span_deg

    @property
    def sculpt_count(self) -> int:
        """How many planes the form itself is rebuilt out of."""
        return plane_count(self.sculpt_detail)

    @property
    def sculpt_fineness(self) -> float:
        """How much finer than usual the geometry's lattice is worked on."""
        return lattice_fineness(self.sculpt_detail)

    @property
    def sculpt_span_deg(self) -> float:
        """Roughly how much of a turn one of those planes covers, in degrees."""
        return plane_span_deg(self.sculpt_count)

    @property
    def shades_normals(self) -> bool:
        """Whether the shader should be rounding normals onto planes."""
        return self.enabled and self.target is PlaneTarget.NORMALS

    @property
    def sculpts_geometry(self) -> bool:
        """Whether a planar stand-in should be built and drawn in place of the model."""
        return self.enabled and self.target is PlaneTarget.GEOMETRY


@dataclass
class RenderSettings:
    """Everything the viewport needs in order to draw a frame."""

    shading_mode: ShadingMode = ShadingMode.MATCAP
    matcap: MatcapSettings = field(default_factory=MatcapSettings)
    light: LightSettings = field(default_factory=LightSettings)
    surface: SurfaceSettings = field(default_factory=SurfaceSettings)
    quality: QualitySettings = field(default_factory=QualitySettings)
    planes: PlaneSettings = field(default_factory=PlaneSettings)
    section: SectionSettings = field(default_factory=SectionSettings)
    pedestal: PedestalSettings = field(default_factory=PedestalSettings)
    matcap_path: str | None = None
    #: Shade each triangle from its own face normal.  The Planes panel edits
    #: this, but it stays on the render settings so that sessions written
    #: before that panel existed still restore it.
    flat_shading: bool = False
    show_wireframe: bool = False
    wireframe_color: Color = (0.08, 0.09, 0.11)
    background_top: Color = (0.26, 0.27, 0.30)
    background_bottom: Color = (0.10, 0.10, 0.12)


@dataclass
class NavigationSettings:
    """How mouse gestures drive the camera."""

    #: Orbit increment, in degrees, while Shift is held.  Snapping to round
    #: angles makes it possible to come back to the same three-quarter view.
    snap_angle_deg: float = 15.0
