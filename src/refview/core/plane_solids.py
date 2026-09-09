"""Handing the planes of a fit to the thing that actually works the volume.

The planes filter next door changes what a fragment is shaded *as*.  The form
underneath it is untouched: the silhouette still curves, the wireframe still
runs over a rounded surface, and a raking light still washes across a shape
that has no flats in it.  What a sculptor does when they block a form in is
coarser and more honest than that -- they move the material.

So this moves it.  The directions come from the same fit the shading filter
uses -- the surface clustered by facing and place, see
:mod:`refview.core.plane_clusters` -- and everything after that is volume, in
:mod:`refview.core.plane_volume`: the model is read into a lattice, cut into
blocks, each block replaced by the flats that hold it, and the surface of what
is left is found again from scratch.

What this module has left to do is small and worth being plain about.

The fit hands back *facings*, and only facings: which way the planes of the
form point.  Nothing else about it survives the trip -- not where the fit put
each plane, not which vertex belongs to which -- because a block decides where
its own flats go by asking how far its own material reaches along them, and
that is a better answer than any offset a fit could name.  It is also why none
of the machinery that used to hand vertices out to planes is here any more:
there is nothing left for it to do, and every bug it ever had went with it.

What the volume does need is the model's shape at a finer grain than the
lattice, which means points spread over the surface closely enough that the
distance to the nearest one is the distance to the surface.  A scan of a face
has thousands of triangles to a cell and needs nothing; a box has six
triangles the size of the whole thing and needs a great many.  That is
:func:`surface_seeds`, and it is the only reason this module reads the
triangles at all.

Then the knobs.  How many planes the artist asked for says how many solids the
form is made of: blocks of stone, starting at the one plain convex hull that is
the block before any cut, or lumps of clay, starting at however many principal
masses the artist says the form has.  That second number is the only one a fit
could never have told us -- how many masses a figure is depends on who is
looking at it -- so it is asked for rather than worked out.  The last of them
says how far the finished clay is then settled into itself, which is a question
about the surface rather than about the volume, and so is asked at the end.

Nothing in here touches the model.  What comes back is a new mesh with its own
vertices and its own triangles, drawn in the model's place, and the model
itself goes on being what picking, measuring, painting and the section cut
read.
"""

from __future__ import annotations

import numpy as np

from .mesh import Mesh, auto_smooth, compute_vertex_normals
from .plane_axes import Coefficients, PlaneAxes, PlaneSet
from .plane_clusters import plane_regions
from .plane_volume import RESOLUTION, carve
from .settings import PlaneSettings, SculptMode

#: Most rows of samples a single triangle is filled in with.  A model made of
#: a handful of enormous triangles would otherwise be sampled to death.
_SEED_DEPTH = 24

#: How close together those samples go, as a share of a lattice cell.  Under a
#: half, so the distance to the nearest sample is the distance to the surface
#: to well inside a cell, which is the accuracy the model's own shape is read
#: back with.
SEED_SHARE = 0.4

#: How many planes it takes to buy one more block of the form.  Fewer than it
#: once was: a block is a mass and a form has far fewer masses than facings, so
#: the coarse end of the slider wants blocks handed out sparingly -- but the
#: fine end is meant to be a figure rather than a rough-out, and the only way
#: to a hollow that no single hull can hold is another block through it.
PLANES_PER_BLOCK = 1.5

#: Most blocks the form is ever cut into.  Sixty-four brings a figure to within
#: a fifth of its own volume and a hundred and ninety to within a twelfth,
#: which is a carving rather than a rough-out and is what the fine end of the
#: slider is for.  Past that the blocks are smaller than anything the form has
#: to say and every extra one is another seam.
MAX_BLOCKS = 192

#: How many planes it takes to buy one more tube of clay.  Two apiece, where
#: stone wants three planes to a block: a cut of the stone re-hulls a whole
#: part of the form and is felt right across it, while a tube is one more lump
#: laid into one more hollow, so the clay wants rather more of them to arrive
#: at the same reading of the form.
PLANES_PER_TUBE = 2.0

#: Most tubes the clay is ever detailed with.  A sculptor laying down clay
#: does not stop at a handful: the masses first, then a tube into every
#: hollow that is still bare, and a figure has a great many of them.  The
#: slider spends its whole range laying them because that is what builds the
#: form up towards the model -- a seam between two lumps is closed by the
#: fill that runs after (:func:`~refview.core.plane_volume.close_gaps`), not
#: by laying fewer lumps, and the reason sixty-odd used to read as rubble was
#: the median shaving the ridges between them, which the fill no longer does.
MAX_TUBES = 128


def unit_normals(mesh: Mesh) -> np.ndarray:
    """The mesh's normals, made unit, with anything unusable recomputed."""
    normals = np.asarray(mesh.normals, dtype=np.float64).reshape(-1, 3)
    lengths = np.linalg.norm(normals, axis=1)
    unusable = lengths <= 1e-9
    if unusable.any():
        fresh = np.asarray(
            compute_vertex_normals(mesh.positions, mesh.indices), dtype=np.float64
        )
        normals = np.where(unusable[:, None], fresh, normals)
        lengths = np.linalg.norm(normals, axis=1)
    return normals / np.where(lengths > 1e-9, lengths, 1.0)[:, None]


def seed_spacing(mesh: Mesh, resolution: int = RESOLUTION) -> float:
    """How finely the model has to be sampled for the lattice it will be read on."""
    reach = float(np.ptp(np.asarray(mesh.positions), axis=0).max())
    return SEED_SHARE * reach / max(int(resolution), 8)


def surface_seeds(
    points: np.ndarray,
    triangles: np.ndarray,
    normals: np.ndarray,
    spacing: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Points spread over the model closely enough for a lattice to feel it.

    The lattice learns the model's shape by measuring how far each of its
    corners is from the nearest of these, so anywhere they are further apart
    than a cell the model comes out lumpy at the scale of the gaps -- and that
    lumpiness is what shows through wherever the form falls back on the model
    rather than on a flat.  So every triangle is filled in to a spacing finer
    than a cell, however the model happens to be tessellated.

    Each sample carries the way the surface faces there, which is what tells a
    model with holes in it from a model turned inside out.
    """
    corners = points[triangles]
    facing = normals[triangles]
    edges = np.stack(
        [
            np.linalg.norm(corners[:, 1] - corners[:, 0], axis=1),
            np.linalg.norm(corners[:, 2] - corners[:, 1], axis=1),
            np.linalg.norm(corners[:, 0] - corners[:, 2], axis=1),
        ],
        axis=1,
    ).max(axis=1)
    depth = np.clip(np.ceil(edges / max(spacing, 1e-9)), 1, _SEED_DEPTH).astype(np.int64)

    places: list[np.ndarray] = [points]
    leaning: list[np.ndarray] = [normals]
    for level in range(2, int(depth.max()) + 1) if len(depth) else ():
        rows = np.flatnonzero(depth == level)
        if len(rows) == 0:
            continue
        # The barycentric lattice of the triangle, corners left out because the
        # model's own vertices are already in.
        i, j = np.meshgrid(np.arange(level + 1), np.arange(level + 1), indexing="ij")
        keep = (i + j <= level) & ~(((i == 0) | (i == level)) & ((j == 0) | (j == level)))
        weight = (
            np.stack([i[keep], j[keep], level - i[keep] - j[keep]], axis=1).astype(np.float64)
            / level
        )
        places.append(np.einsum("tcx,sc->tsx", corners[rows], weight).reshape(-1, 3))
        leaning.append(np.einsum("tcx,sc->tsx", facing[rows], weight).reshape(-1, 3))
    spread = np.concatenate(places)
    lean = np.concatenate(leaning)
    return spread, lean / np.maximum(np.linalg.norm(lean, axis=1), 1e-12)[:, None]


def block_count(planes: int) -> int:
    """How many blocks a count of planes asks the stone to be cut into.

    One at the coarse end, which is the convex hull of the whole model and the
    honest block it would be carved out of; then a block for every few planes
    after that, up to a ceiling well past any block-in.
    """
    return int(np.clip(1 + round((int(planes) - 2) / PLANES_PER_BLOCK), 1, MAX_BLOCKS))


def piece_count(planes: int, masses: int) -> int:
    """How many lumps a count of planes asks the clay to be built out of.

    The masses first, which the artist has said outright and which are
    therefore never cut back, and then a tube for every couple of planes on top
    of them.  The coarse end of the slider is the masses and nothing else,
    which is the block-in a sculptor starts with; everything after that is
    detail laid into it.
    """
    tubes = max(round((int(planes) - 2) / PLANES_PER_TUBE), 0)
    return max(int(masses), 1) + int(min(tubes, MAX_TUBES))


def solid_count(planes: int, sculpt: SculptMode, masses: int) -> int:
    """How many solids the form is made of, whichever way it is being worked."""
    if sculpt is SculptMode.ADDITIVE:
        return piece_count(planes, masses)
    return block_count(planes)


def sculpt_mesh(
    mesh: Mesh,
    planes: PlaneSet,
    sculpt: SculptMode,
    masses: int = PlaneSettings().sculpt_masses,
    relax: int = PlaneSettings().sculpt_relax,
    smooth: float = PlaneSettings().sculpt_smooth,
    median: int = PlaneSettings().sculpt_median,
    median_reach: int = PlaneSettings().sculpt_median_reach,
    fineness: float = 1.0,
) -> Mesh:
    """A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side.

    The model is read, never written: what comes back is a new mesh, found by
    working the volume the model encloses rather than by moving its vertices
    -- see :mod:`refview.core.plane_volume` for why that is the only way a
    plane can be made to behave like a cut.  A model that cannot be broken
    into planes at all comes back as it went in.

    ``fineness`` multiplies the lattice the form is worked on.  It is one for
    every setting the detail slider itself can reach, and more only where a
    number has been typed past the end of it -- see
    :data:`~refview.core.settings.DETAIL_CEILING`.
    """
    if mesh.vertex_count == 0 or len(planes) == 0:
        return mesh  # nothing was built, so there is nothing to shade either
    triangles = np.asarray(mesh.indices, dtype=np.int64).reshape(-1, 3)
    if len(triangles) == 0:
        return mesh
    points = np.asarray(mesh.positions, dtype=np.float64)
    resolution = max(int(round(RESOLUTION * max(float(fineness), 1.0))), RESOLUTION)
    seeds, leaning = surface_seeds(
        points, triangles, unit_normals(mesh), seed_spacing(mesh, resolution)
    )
    return auto_smooth(
        carve(
            points,
            triangles,
            seeds,
            leaning,
            np.asarray(planes.directions, dtype=np.float64).reshape(-1, 3),
            sculpt is SculptMode.ADDITIVE,
            int(masses),
            solid_count(len(planes), sculpt, int(masses)),
            int(relax),
            int(median),
            int(median_reach),
            resolution,
            f"{mesh.name} (planes)",
            source_offset=mesh.source_offset,
            units=mesh.units,
        ),
        float(smooth),
    )


class SculptCache:
    """Holds the working state between one turn of the sliders and the next.

    Rebuilding the stand-in has two costs and they are very different sizes:
    fitting the model's planes is the expensive one, and it only goes stale
    when the model or the design matrix changes.  Keeping it apart from the
    carving is what lets clay and stone -- and the masses behind the clay --
    be compared back and forth without the fit being run again.
    """

    __slots__ = (
        "_mesh",
        "_coefficients",
        "_axes",
        "_count",
        "_planes",
        "_work",
        "_carved",
        "_smooth",
        "_result",
    )

    def __init__(self) -> None:
        self._mesh: Mesh | None = None
        self._coefficients: Coefficients | None = None
        self._axes = PlaneAxes([])
        self._count = -1
        self._planes = PlaneSet.empty()
        self._work: tuple | None = None
        self._carved: Mesh | None = None
        self._smooth: float | None = None
        self._result: Mesh | None = None

    def clear(self) -> None:
        """Drop everything held, so the next call starts from the fit."""
        self._mesh = None
        self._coefficients = None
        self._axes = PlaneAxes([])
        self._count = -1
        self._planes = PlaneSet.empty()
        self._work = None
        self._carved = None
        self._smooth = None
        self._result = None

    def planes_for(self, mesh: Mesh, settings: PlaneSettings) -> PlaneSet:
        """The fit these settings ask for, refitting only if it has gone stale.

        The fit is the expensive half of the cache and it does not depend on
        how the form is then worked, so a film -- which works it many times
        over -- wants the same one the single build would have used rather
        than a fit of its own.
        """
        coefficients = settings.coefficients
        if mesh is not self._mesh or coefficients != self._coefficients:
            self._mesh, self._coefficients = mesh, coefficients
            self._axes = plane_regions(mesh, coefficients)
            self._count, self._work, self._carved = -1, None, None
        count = settings.sculpt_count
        if count != self._count:
            self._count = count
            self._planes = self._axes.for_count(count)
            self._work, self._carved = None, None
        return self._planes

    def mesh_for(self, mesh: Mesh | None, settings: PlaneSettings) -> Mesh | None:
        """The stand-in these settings ask for, or ``None`` for the model itself."""
        if mesh is None or not settings.sculpts_geometry:
            return None

        self.planes_for(mesh, settings)
        work = (
            settings.sculpt,
            settings.sculpt_masses,
            settings.sculpt_relax,
            settings.sculpt_median,
            settings.sculpt_median_reach,
            settings.sculpt_fineness,
        )
        if work != self._work or self._carved is None:
            self._work = work
            self._smooth = None
            # Built flat and shaded afterwards, kept apart on purpose: working
            # the volume again costs seconds and re-reading its normals costs
            # a tenth of one, so the AutoSmooth slider must not be able to ask
            # for the first when all it wants is the second.
            self._carved = sculpt_mesh(
                mesh,
                self._planes,
                settings.sculpt,
                settings.sculpt_masses,
                settings.sculpt_relax,
                smooth=0.0,
                median=settings.sculpt_median,
                median_reach=settings.sculpt_median_reach,
                fineness=settings.sculpt_fineness,
            )
        if settings.sculpt_smooth != self._smooth or self._result is None:
            self._smooth = settings.sculpt_smooth
            self._result = auto_smooth(self._carved, settings.sculpt_smooth)
        return self._result
