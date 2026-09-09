"""Blocking a form in out of its own planes, from the outside or from a core.

A plane is not something a surface can be put onto.  Moving the model's own
vertices onto the planes of the fit folds the surface wherever the patch it
came from wraps -- a shoulder flattened onto the shoulder's plane turns a
third of its triangles inside out -- and no arrangement of the arithmetic gets
round that, because it is what projecting a curved thing onto a flat one does.

A sculptor never projects.  Both ways of working are volume, and each one has
a shape it starts from.

*Stone* starts as a block.  The block is the convex hull of the model: the
smallest thing made of flats that still has the whole figure inside it, and an
honest first day of a carving.  Every cut after that splits a block in two and
takes the hull of each half, and two hulls hold the model more tightly than
the one did -- the hollow between an arm and a ribcage comes back the moment a
cut runs between them.  Which block to split, and where, is settled by asking
which one is holding the most air: the deepest hollow is the one the block is
wasting the most stone on, so it is the one the next cut goes through.  One
block is the rough-out, forty blocks is a figure, and the slider is how many
cuts have been made.

*Clay* starts as a lump.  A rectangular block of it is pressed into the model
-- the largest one that fits inside the form without poking out anywhere --
and then another into whatever is still bare, and another: on a figure that is
the ribcage, then the pelvis, then the thighs.  How many of those principal
masses to block in is the artist's to say, because it is a reading of the form
rather than a fact about it.

After the masses come the tubes.  Each is another lump pressed into whichever
part of the model has the most material still uncovered, largest first, so the
arms arrive before the hands and the hands before the fingers.  A tube is
grown exactly as a mass is, but it is allowed the form's own planes as well as
the three axes of the mass it sits in, so it comes out bevelled where the
model turns.  Nothing here is ever told what a limb is: the order falls out of
asking, over and over, where the most uncovered material is.

Growing a lump is one question asked twice, and both times the answer is a
single pass over the model's surface.  How far the lump's own shape will
inflate about its seed before it touches is the least, over every point just
outside the model, of how far that point lies past the nearest of the lump's
own facings.  Then each facing in turn is pushed out on its own as far as it
will go, which is the least, over just those outside points that every *other*
facing is already holding out, of how far past this one they are.  Convexity
is what makes both exact and what makes them cheap: a lump that holds its seed
and some point beyond the surface holds the whole way between them, so only
the outside points nearest the model can ever bind, and the rest need never be
looked at.

Both ways of working end as the same kind of object -- a union of convex
solids, each one the meeting of a handful of half-spaces -- and a union of
convex solids is a thing a lattice can hold exactly.  Each solid writes the
largest of its own planes into the field; the solids are combined by taking
the smallest, which is what a union is.  That is also why the clay is joined
as a volume and never as surfaces: a tube laid across a mass leaves no seam
where they meet and no sliver where they cross, because there is nothing there
to stitch.  Both operations are continuous, so the surface this leaves has
nothing to tear along.  The model itself is then held against the result, as a
floor under the stone and a ceiling over the clay, so that one comes back
larger than the model and the other smaller by construction rather than by
luck.

The surface is read back by dual contouring, which puts one vertex in each
cell of the lattice where the planes crossing that cell agree.  Those planes
are exact, so the vertex is exact: a cell in the middle of a facet lands dead
on it, a cell along a crease lands on the line where two facets cross, a cell
at a corner lands on the point where three do.  The flats come out flat to the
last digit, the creases come out straight, and the surface comes out closed
and free of folds because an isosurface always is.

The result is a different mesh from the model: its own vertices, its own
triangles, a good deal fewer of both.  That is the point of it, and it is safe
because this mesh is only ever drawn.  The model is untouched and is what
picking, measuring, painting and the section cut go on reading.
"""

from __future__ import annotations

import math

import numpy as np

from .mesh import Mesh

#: Cells across the model's longest side.  What this buys is not flatness --
#: the facets are exact at any resolution -- but how finely the outline of a
#: facet, and the smallest form the model still has, are resolved.
RESOLUTION = 144

#: Most lattice corners to carry, whatever the resolution asks for.  A form
#: that is roughly as deep as it is tall costs a great deal more than a figure
#: of the same height, and this is what keeps the slider honest on both.
MAX_CORNERS = 2_200_000

#: Room left around the model, as a share of its longest side.  A block only
#: ever has to hold the convex hull of some of the model, and the hull of a
#: thing sits inside the box the thing sits in, so a few cells is all this
#: needs to be.
MARGIN_SHARE = 0.03

#: How far the model's own distance is carried out from its surface, in cells.
#: Past this it saturates, which is harmless: out there all the field has to
#: say is which side of the model a corner is on.
SDF_REACH = 48

#: Most supporting directions a block is cut with.  This, rather than the
#: number of blocks, is what tightens a rough-out onto the model: another
#: direction shaves every block at once and leaves the form whole, while
#: another block only ever tightens its own corner of it and leaves a seam
#: where it meets its neighbour.  So the slider spends its detail here first,
#: and the ceiling is high enough that the fine end of it is a figure rather
#: than a rough-out -- doubling the directions brings the stone in about twice
#: as far as tripling the blocks does.
MAX_FACINGS = 256

#: How close two supporting directions may be before they count as one, in
#: degrees.  The fit is free to hand back near-duplicates, and a duplicate
#: costs a whole pass over the lattice for a facet that is already there.
MERGE_ANGLE_DEG = 6.0

#: Corners the block-splitting is allowed to work on.  Where to cut is a
#: question about masses, not about millimetres, so it is asked of a lattice
#: coarse enough that a few dozen trial hulls are affordable.  It also decides
#: how finely a block knows its own edge, which is what the model's surface is
#: handed out by, so it cannot go much below this without blocks reaching into
#: each other's material.
SPLIT_CORNERS = 150_000

#: Corners the clay's lumps are fitted on.  A lump is a geometric solid -- a
#: few planes with real offsets -- so the lattice it is grown on settles only
#: how finely it feels the model's surface, never how finely it is drawn.  It
#: does have to feel the surface properly, though: a figure is a few cells
#: through even on the main lattice, and a lump fitted on half of that is a
#: die rolled into a torso.  So this is set to take the main lattice whole on
#: anything but a form that is as deep as it is tall.
GROW_CORNERS = 1_200_000

#: How far inside the surface a lump of clay has to stop, in cells of the
#: lattice it was grown on.  A quarter of a cell, which is as good as none and
#: is meant to be: a lump held further back than that loses a shell of itself
#: on every side, and on a limb four cells through that is most of the limb.
#: What is left of it is caught by the model, which the finished field is held
#: under, so the worst a lump can do by reaching too far is to have a sliver of
#: itself replaced by the model's own surface.
PIECE_SAFETY = 0.25

#: How much of the form around a seed is read to find which way its mass runs,
#: as a multiple of how deep that seed lies.  Wide enough that an arm is read
#: as an arm, narrow enough that it is not read as part of the torso it joins.
FRAME_SPAN = 3.0

#: Most of the form's own facings a tube may be bevelled with, on top of the
#: six of its own frame.  The principal masses get none of them at all: a mass
#: is a rectangular block, which is what a lump of clay pressed into a form
#: with the heel of the hand actually is.
#:
#: How many are really used is however many the fit found, so this is the top
#: of a range the detail slider runs up.  That matters more than it sounds: a
#: lump that can be bevelled fits the form it was pressed into, and one that
#: cannot has to be joined to by another lump instead.  Detail spent here
#: comes back as clean flats, and detail spent on more lumps comes back as
#: rubble, so past a point the slider stops adding lumps and spends the rest
#: of itself here.
TUBE_FACINGS = 48

#: How far the hull of two lumps may be pulled back into the model and still
#: be worth laying in as a join, as a share of the thinner lump's own
#: half-thickness.
#:
#: The join between two lumps is the hull of the two, held inside the model.
#: How far that hull has to come in before it is inside says what the two lumps
#: really are to each other: a little, and they are two readings of one mass
#: with a notch between them, which is exactly what wants filling; a long way,
#: and they lie on opposite sides of a gap in the form -- an arm beside a
#: ribcage, two fingers -- and the hull is spanning air rather than joining
#: anything.  Pulled in that far it would come back smaller than the lumps it
#: was meant to join, so nothing is lost by dropping it, and a good deal of
#: time is saved.
JOIN_ROOM = 0.75

#: How much of each lump a join is allowed to be made of, as a share of the
#: thinner one's half-thickness.
#:
#: A join is a thumb-full of clay pushed across a seam, not a slab laid over
#: both of the masses it joins.  The difference matters more than it sounds.
#: The hull of two whole lumps, on a form that is anywhere near convex, is most
#: of the form: it would fill a torso between one lump and the next in a single
#: piece, and every further lump the detail slider bought would then have
#: nothing left to add.  Held to a collar this wide round the seam, a join
#: fills the notch it was meant to fill and leaves the rest of the form to the
#: lumps -- so the slider still runs from a block-in to a reading, which is the
#: whole of what it is for.
JOIN_SPAN = 0.5

#: Most joins that may be laid in on top of the lumps.
#:
#: Every join is a solid the lattice has to be written with, and a join spans
#: two lumps, so it is a larger solid than either.  The pairs are taken biggest
#: first, which is the same order the lumps themselves are laid down in: the
#: join between a ribcage and a pelvis is worth more than the join between two
#: knuckles, and it is worth more for the same reason.
MAX_JOINS = 64

#: How many passes of the median are run over the finished clay volume, and
#: how far each of them reaches, in cells.
#:
#: A median is the right filter for this and a blur is not, and the reason is
#: worth stating.  Over a neighbourhood laid symmetrically about a corner, the
#: median of a field that is *planar* there is the corner's own value exactly
#: -- the values above and below it pair off.  So a flat comes through a median
#: pass unchanged, however many passes are run: this cannot soften the thing
#: the whole mode exists to show.  What it does change is everything a flat is
#: not.  A slot between two lumps has most of a neighbourhood inside the
#: material and so is filled; a spike has most of one outside and so is taken
#: off; a cell of a hole is outvoted by its neighbours and closed.  That is the
#: list of things dual contouring cannot make a clean surface out of, and one
#: pass of a three-cell median removes all of them.
#:
#: Both ends of this are the artist's to set, and the reason to be careful
#: with them is that a median does not only fill.  A slot has material either
#: side of it and closes; a convex corner has air on more sides than material
#: and so is shaved, which is the same arithmetic read the other way round.
#: One pass at one cell of reach takes a slot out and leaves the form where it
#: was; four passes at three cells of reach take three fifths of the form away
#: with them.  These are the defaults, not the limits.
MEDIAN_ROUNDS = 1
MEDIAN_REACH = 1

#: Cells of room left round a block when its field is written, so that the
#: surface of the block is always inside the box the block was computed in.
BOX_PAD = 3

#: How firmly the planes crossing a cell must hold a direction before the
#: cell's vertex is moved along it, as a share of the strongest direction they
#: hold.  Two facets meeting at a shallow angle do cross somewhere, but a
#: vertex sent to sit on that line travels a long way for an answer a degree
#: of noise would move again; below this it keeps the middle of the cell
#: instead.  The difference between a corner and a spike.
QEF_FLOOR = 0.06

#: A whisper of a pull towards the middle of the cell, so the division is
#: never by nothing.
QEF_ANCHOR = 1e-3

#: How far a lattice vertex may be pushed outside its own cell.  Dual
#: contouring's one failure is a vertex solved for out in space; keeping it
#: near its cell costs a little sharpness on a very shallow crease and nothing
#: anywhere else.
CELL_SLACK = 0.75

#: Where in a column the model is sampled for inside-or-out, as a fraction of
#: a cell.  Irrational enough that a ray never runs exactly along an edge of
#: the model, which is the only thing that makes a parity count lie.
JITTER = (0.00037, 0.00021)

#: How far a vertex is drawn towards its neighbours in one pass of the relax,
#: and how far it is pushed back out again in the pass after it.
#:
#: Taubin's pair, and the second number is what makes it worth having.  Plain
#: smoothing pulls every vertex towards the middle of its neighbours, which on
#: a closed surface means every vertex moves inwards a little every pass: run
#: it long enough and the form shrinks to nothing.  Following each pull with a
#: slightly larger push undoes that at the scale of the whole form while
#: leaving it done at the scale of a facet edge, so the block-in keeps its size
#: and loses only its corners.
RELAX_PULL = 0.5
RELAX_PUSH = -0.53

#: How much of the largest piece a piece must hold to be kept.
PIECE_SHARE = 0.05

#: How far the lattice's idea of the model's volume may differ from the
#: triangles' own before the crossing count is disbelieved.  Generous: it is
#: telling a closed model from an open one, not measuring anything.
ENCLOSURE_SLACK = 0.25

#: How near the model a piece has to come, in cells, to be part of the
#: carving rather than a chip off it.
PIECE_TOUCH = 2.5

#: Candidate column-triangle pairs weighed at once while reading the model in.
_RASTER_CHUNK = 4_000_000

#: Most passes the piece-finding may take before it keeps what it has.  Each
#: pass halves the chains left over from the last.
_PIECE_ROUNDS = 64

#: Passes of handing a block's number to the corners just outside it, so that
#: every corner of the model belongs to some block even where the coarse
#: lattice the blocks were cut on did not reach.
_SPREAD_ROUNDS = 3


# -- the lattice ----------------------------------------------------------


def lattice(
    low: np.ndarray, high: np.ndarray, margin: float, resolution: int = RESOLUTION
) -> tuple[np.ndarray, float, tuple]:
    """A cubic lattice covering the model with ``margin`` of room around it.

    Cubic cells rather than a fixed count per side, so a figure -- tall, thin,
    and mostly air -- costs a fraction of what a head of the same height does
    instead of the same amount.

    ``resolution`` is how many cells the longest side is cut into, and it is
    asked for rather than fixed because the fine end of the detail slider buys
    a finer lattice once it has run out of planes to buy.  Either way the
    corner count is the last word: a lattice that would need more than
    :data:`MAX_CORNERS` of them is coarsened until it does not.
    """
    low = np.asarray(low, dtype=np.float64) - margin
    high = np.asarray(high, dtype=np.float64) + margin
    span = np.maximum(high - low, 1e-9)
    step = float(span.max()) / max(int(resolution), 8)
    shape = tuple(int(np.ceil(s / step)) + 1 for s in span)
    while shape[0] * shape[1] * shape[2] > MAX_CORNERS:
        step *= 1.15
        shape = tuple(int(np.ceil(s / step)) + 1 for s in span)
    return low, step, shape


def _axes(origin: np.ndarray, step: float, shape: tuple) -> tuple:
    """The three coordinates of every lattice corner.

    Stretched views rather than real arrays, so all three together cost one
    row of numbers each and still slice like the fields they are read beside.
    """
    return tuple(
        np.broadcast_to(
            (origin[a] + step * np.arange(shape[a], dtype=np.float32)).reshape(
                [-1 if i == a else 1 for i in range(3)]
            ),
            shape,
        )
        for a in range(3)
    )


def _rows(origin: np.ndarray, step: float, box: tuple) -> list:
    """One row of coordinates per axis over ``box``, shaped so they broadcast."""
    return [
        (origin[a] + step * np.arange(box[a].start, box[a].stop, dtype=np.float32)).reshape(
            [-1 if i == a else 1 for i in range(3)]
        )
        for a in range(3)
    ]


def _shifts(axis: int, forward: bool, span: int) -> tuple[tuple, tuple]:
    """The pair of slices that read a lattice ``span`` cells over along ``axis``."""
    here: list = [slice(None)] * 3
    there: list = [slice(None)] * 3
    here[axis] = slice(span, None) if forward else slice(0, -span)
    there[axis] = slice(0, -span) if forward else slice(span, None)
    return tuple(here), tuple(there)


def _passes(reach: int) -> tuple[int, ...]:
    """The strides that carry an answer ``reach`` cells.

    Halving the stride each pass carries it as far as the first stride in as
    many passes as there are strides, rather than one cell per pass, which is
    the difference between this being affordable and not.  The last pass
    repeats at one cell to tidy up what the long strides jumped over.
    """
    reach = max(int(reach), 1)
    strides = []
    span = 1
    while span * 2 <= reach:
        span *= 2
    while span >= 1:
        strides.append(span)
        span //= 2
    return tuple(strides) + (1,)


# -- reading the model in -------------------------------------------------


def solid(
    vertices: np.ndarray,
    triangles: np.ndarray,
    origin: np.ndarray,
    step: float,
    shape: tuple,
) -> np.ndarray:
    """Which lattice corners are inside the model.  ``(nx, ny, nz)`` of bool.

    A ray straight up from every corner, counting the model's own triangles as
    it goes: an odd number above means the corner is inside.  It asks only
    that the model be closed, which is what an artist's reference model is,
    and it does not care whether the surface is convex, nested, or wound
    consistently.
    """
    counts = np.zeros(int(shape[0]) * int(shape[1]) * int(shape[2]), dtype=np.int32)
    corners = np.asarray(vertices, dtype=np.float64)[np.asarray(triangles, dtype=np.int64)]
    if len(corners) == 0:
        return counts.reshape(shape) > 0

    # Columns are indexed in lattice units, sampled a hair off the corner so a
    # ray never grazes an edge of the model.
    across = (corners[:, :, 0] - origin[0]) / step - JITTER[0]
    along = (corners[:, :, 1] - origin[1]) / step - JITTER[1]
    first = np.maximum(np.ceil(across.min(1)).astype(np.int64), 0)
    last = np.minimum(np.floor(across.max(1)).astype(np.int64), shape[0] - 1)
    lower = np.maximum(np.ceil(along.min(1)).astype(np.int64), 0)
    upper = np.minimum(np.floor(along.max(1)).astype(np.int64), shape[1] - 1)
    wide = np.maximum(last - first + 1, 0)
    tall = np.maximum(upper - lower + 1, 0)
    covering = wide * tall
    rows = np.flatnonzero(covering > 0)

    for begin in range(0, len(rows), 4096):
        block = rows[begin : begin + 4096]
        while len(block):
            room = np.searchsorted(np.cumsum(covering[block]), _RASTER_CHUNK) + 1
            take, block = block[:room], block[room:]
            spread = covering[take]
            which = np.repeat(take, spread)
            within = np.arange(int(spread.sum())) - np.repeat(
                np.cumsum(spread) - spread, spread
            )
            column = first[which] + within % wide[which]
            row = lower[which] + within // wide[which]

            u, v = across[which], along[which]
            twice = (u[:, 1] - u[:, 0]) * (v[:, 2] - v[:, 0]) - (u[:, 2] - u[:, 0]) * (
                v[:, 1] - v[:, 0]
            )
            usable = np.abs(twice) > 1e-12
            px, py = column.astype(np.float64), row.astype(np.float64)
            a = ((u[:, 1] - px) * (v[:, 2] - py) - (u[:, 2] - px) * (v[:, 1] - py)) / np.where(
                usable, twice, 1.0
            )
            b = ((u[:, 2] - px) * (v[:, 0] - py) - (u[:, 0] - px) * (v[:, 2] - py)) / np.where(
                usable, twice, 1.0
            )
            c = 1.0 - a - b
            hit = usable & (a >= 0.0) & (b >= 0.0) & (c >= 0.0)
            if not hit.any():
                continue
            depth = (
                a[hit] * corners[which[hit], 0, 2]
                + b[hit] * corners[which[hit], 1, 2]
                + c[hit] * corners[which[hit], 2, 2]
            )
            level = np.clip(
                np.floor((depth - origin[2]) / step).astype(np.int64), 0, shape[2] - 1
            )
            flat = (column[hit] * shape[1] + row[hit]) * shape[2] + level
            counts += np.bincount(flat, minlength=len(counts)).astype(np.int32)

    # Crossings at or above a corner, so the parity is read downwards.
    above = np.cumsum(counts.reshape(shape)[:, :, ::-1], axis=2)[:, :, ::-1]
    return (above & 1).astype(bool)


def encloses(within: np.ndarray, vertices: np.ndarray, triangles: np.ndarray, step: float) -> bool:
    """Whether counting crossings actually described the model it was given.

    It is exact on a closed surface and meaningless on anything else, and the
    two are told apart by asking the lattice and the triangles the same
    question: how much room is inside.  A closed model gives the same answer
    twice over.
    """
    corners = np.asarray(vertices, dtype=np.float64)[np.asarray(triangles, dtype=np.int64)]
    if len(corners) == 0:
        return False
    sealed = abs(
        float(
            np.einsum("ij,ij->i", corners[:, 0], np.cross(corners[:, 1], corners[:, 2])).sum()
            / 6.0
        )
    )
    counted = float(within.sum()) * step**3
    return sealed > 0.0 and abs(counted - sealed) <= ENCLOSURE_SLACK * sealed


def nearest_surface(
    seeds: np.ndarray,
    origin: np.ndarray,
    step: float,
    shape: tuple,
    rounds: int,
) -> tuple[np.ndarray, np.ndarray]:
    """For every corner, how far the model is and which sample of it is nearest.

    The surface is dropped into the lattice and then the closest point itself
    -- not the distance -- is handed outwards from cell to cell, each cell
    keeping whichever of its neighbours' closest points is really closest to
    it.  Passing the point rather than the number is what keeps the distance a
    true straight-line one instead of a staircase, which matters because the
    model's own shape is read back out of it.

    Comes back as the squared distance and the sample that won it.
    """
    gap = np.full(shape, np.float32(np.inf), dtype=np.float32)
    which = np.zeros(shape, dtype=np.int32)
    close = [np.zeros(shape, dtype=np.float32) for _ in range(3)]
    if len(seeds) == 0:
        return gap, which

    cell = np.clip(
        np.rint((seeds - origin) / step).astype(np.int64),
        0,
        np.array(shape, dtype=np.int64) - 1,
    )
    at = (cell[:, 0] * shape[1] + cell[:, 1]) * shape[2] + cell[:, 2]
    corner = origin + cell * step
    reach = np.einsum("ij,ij->i", seeds - corner, seeds - corner)
    # Written furthest first, so the nearest seed in a cell is what survives.
    order = np.argsort(-reach, kind="stable")
    gap.reshape(-1)[at[order]] = reach[order].astype(np.float32)
    which.reshape(-1)[at[order]] = order.astype(np.int32)
    for a in range(3):
        close[a].reshape(-1)[at[order]] = seeds[order, a].astype(np.float32)

    grid = _axes(origin, step, shape)
    for span in _passes(rounds):
        for axis in range(3):
            if shape[axis] <= span:
                continue
            for forward in (True, False):
                here, there = _shifts(axis, forward, span)
                offered = [close[a][there].copy() for a in range(3)]
                trial = np.zeros_like(gap[here])
                for a in range(3):
                    spread = grid[a][here] - offered[a]
                    trial += spread * spread
                better = trial < gap[here]
                if not better.any():
                    continue
                mine = which[there].copy()
                np.copyto(gap[here], trial, where=better)
                np.copyto(which[here], mine, where=better)
                for a in range(3):
                    np.copyto(close[a][here], offered[a], where=better)
    return gap, which


# -- the directions a block is cut along ----------------------------------


def _corner_facings() -> np.ndarray:
    """Twenty-six directions round a cube, for judging how much air a block holds.

    Deliberately not the fit's own directions: this is measuring a volume, and
    a measure that leaned the way the answer does would prefer whichever cut
    happened to suit the planes already found.
    """
    steps = np.array([-1.0, 0.0, 1.0])
    grid = np.stack(np.meshgrid(steps, steps, steps, indexing="ij"), axis=-1).reshape(-1, 3)
    grid = grid[np.any(grid != 0.0, axis=1)]
    return grid / np.linalg.norm(grid, axis=1)[:, None]


def facings(directions: np.ndarray, limit: int = MAX_FACINGS) -> np.ndarray:
    """The supporting directions a block may be cut along.  ``(m, 3)``.

    The twenty-six round a cube first, and they are not negotiable.  A hull is
    only a hull if it is cut from every side, and a block cut along six
    directions is a box however cleverly the six were chosen -- which is fine
    for stone, whose block is meant to be crude, and useless for clay, whose
    block has to end up *inside* the model to be a block-in of it at all.  So
    the form always gets a full set of paddles, and what the artist's plane
    count buys is how many of them are the form's own.

    Then the planes of the fit, each of them both ways, because a plane of a
    form names one facing and a block has to be cut from both sides of it.
    Near-duplicates are dropped throughout: a duplicate costs a pass over the
    lattice and adds a facet that is already there.
    """
    given = np.asarray(directions, dtype=np.float64).reshape(-1, 3)
    length = np.linalg.norm(given, axis=1)
    given = given[length > 1e-9] / np.maximum(length[length > 1e-9], 1e-12)[:, None]
    both = np.empty((2 * len(given), 3))
    both[0::2], both[1::2] = given, -given
    offered = np.concatenate([_corner_facings(), both])

    apart = math.cos(math.radians(MERGE_ANGLE_DEG))
    kept: list[np.ndarray] = []
    for facing in offered:
        if kept and float(np.max(np.asarray(kept) @ facing)) >= apart:
            continue
        kept.append(facing)
        if len(kept) >= max(int(limit), 26):
            break
    return np.asarray(kept, dtype=np.float64)


def fitted_facings(directions: np.ndarray, limit: int = TUBE_FACINGS) -> np.ndarray:
    """The form's own facings alone, both ways round and without duplicates.

    What a tube of clay is bevelled with.  The twenty-six round a cube are
    already the frame of the mass the tube sits in, turned to suit it, so what
    is worth adding on top of them is only what the fit found and a cube does
    not have: the plane of a shin, the underside of a jaw.
    """
    corners = len(_corner_facings())
    return facings(directions, limit=corners + max(int(limit), 0))[corners:]


# -- cutting the model into blocks ----------------------------------------


def _hull_air(points: np.ndarray, directions: np.ndarray, step: float) -> np.ndarray:
    """The corners a hull round ``points`` holds that ``points`` do not fill.

    The hull is read as the meeting of half-spaces, one per direction, each
    pushed out to the furthest point along it -- the convex hull seen from a
    fixed set of angles, which is never smaller than the hull itself.  What
    comes back is *where* the air is, because where the air is is what says
    where the next cut should go.
    """
    low = points.min(axis=0)
    counts = np.maximum(np.rint((points.max(axis=0) - low) / step).astype(np.int64) + 1, 1)
    rows = [
        (low[a] + step * np.arange(counts[a])).reshape([-1 if i == a else 1 for i in range(3)])
        for a in range(3)
    ]
    reach = (points @ directions.T).max(axis=0)
    room = np.ones(tuple(counts), dtype=bool)
    for j in range(len(directions)):
        room &= (
            rows[0] * directions[j, 0] + rows[1] * directions[j, 1] + rows[2] * directions[j, 2]
        ) <= reach[j] + 0.5 * step
    at = np.rint((points - low) / step).astype(np.int64)
    room[at[:, 0], at[:, 1], at[:, 2]] = False
    return low + np.stack(np.nonzero(room), axis=1) * step


def _cuts(points: np.ndarray, air: np.ndarray) -> list:
    """Where a block might be cut in two: a direction, and a point to pass through.

    Three cuts across the air the block is holding, which is what a carver
    looks at -- the hollow between two masses is the thing the block has not
    been opened up along yet -- and three across the block itself, to fall
    back on when a block holds no air worth speaking of but is still a great
    deal longer than it is thick.
    """
    out: list = []
    for cloud in (air, points):
        if len(cloud) < 4:
            continue
        middle = cloud.mean(axis=0)
        centred = cloud - middle
        frame = np.linalg.eigh(centred.T @ centred / len(cloud))[1]
        out.extend((frame[:, a], middle) for a in range(3))
    return out


def blocks(
    within: np.ndarray, origin: np.ndarray, step: float, wanted: int
) -> tuple[np.ndarray, int, int]:
    """Cut the model into nearly convex blocks.  ``(coarse labels, stride, count)``.

    One block to start with -- the whole model, whose hull is the block of
    stone -- and then, over and over, the block holding the most air is split
    in two.  Each candidate cut is judged by how much air the two halves would
    hold between them and the best is taken, so a cut runs through the middle
    of a hollow and the hollow comes back.

    Asked on a lattice coarse enough that a few dozen trial hulls are cheap,
    because where the masses of a form are is not a question that needs
    millimetres.  Corners outside the model carry ``-1``.
    """
    stride = 1
    while within.size // (stride**3) > SPLIT_CORNERS:
        stride += 1
    coarse = np.ascontiguousarray(within[::stride, ::stride, ::stride])
    label = np.full(coarse.shape, -1, dtype=np.int32)
    at = np.stack(np.nonzero(coarse), axis=1)
    if len(at) == 0:
        return label, stride, 0

    coarse_step = step * stride
    place = origin + at * coarse_step
    who = np.zeros(len(at), dtype=np.int32)
    facing = _corner_facings()
    air = [_hull_air(place, facing, coarse_step)]
    held = [float(len(air[0]))]

    while len(held) < max(int(wanted), 1):
        pick = int(np.argmax(held))
        if held[pick] <= 0.0:
            break
        mine = np.flatnonzero(who == pick)
        points = place[mine]
        best = None
        for normal, through in _cuts(points, air[pick]):
            side = points @ normal > float(through @ normal)
            if not side.any() or side.all():
                continue
            over = _hull_air(points[side], facing, coarse_step)
            under = _hull_air(points[~side], facing, coarse_step)
            cost = len(over) + len(under)
            if best is None or cost < best[0]:
                best = (cost, side, over, under)
        if best is None:
            held[pick] = 0.0
            continue
        _, side, over, under = best
        who[mine[side]] = len(held)
        air[pick], held[pick] = under, float(len(under))
        air.append(over)
        held.append(float(len(over)))

    label[at[:, 0], at[:, 1], at[:, 2]] = who
    return _spread(label, _SPREAD_ROUNDS), stride, len(held)


def _spread(label: np.ndarray, rounds: int) -> np.ndarray:
    """Hand a block's number to the corners just outside it.

    The blocks are cut on a coarse lattice, so a corner of the fine one that
    sits inside the model can easily fall on a coarse corner that did not.
    Those corners are the model's own surface, which is precisely the material
    a hull is measured from, so they have to belong somewhere.
    """
    out = label.copy()
    for _ in range(max(int(rounds), 0)):
        if (out >= 0).all():
            break
        for axis in range(3):
            for forward in (True, False):
                here, there = _shifts(axis, forward, 1)
                offered = out[there]
                np.copyto(out[here], offered, where=(out[here] < 0) & (offered >= 0))
    return out


def block_bounds(label: np.ndarray, count: int) -> tuple[np.ndarray, np.ndarray]:
    """The index range each block covers.  ``(count, 3)`` lows and highs, inclusive.

    A block with nothing in it comes back with its high below its low, which
    is what everything downstream reads as "pass over this one".
    """
    low = np.zeros((count, 3), dtype=np.int64)
    high = np.full((count, 3), -1, dtype=np.int64)
    live = label >= 0
    if count == 0 or not live.any():
        return low, high
    at = np.stack(np.nonzero(live), axis=1)
    who = label[live]
    for a in range(3):
        least = np.full(count, np.iinfo(np.int64).max)
        np.minimum.at(least, who, at[:, a])
        most = np.full(count, -1, dtype=np.int64)
        np.maximum.at(most, who, at[:, a])
        low[:, a], high[:, a] = np.where(most >= 0, least, 0), most
    return low, high


def coarse_bounds(
    label: np.ndarray, count: int, stride: int, shape: tuple
) -> tuple[np.ndarray, np.ndarray]:
    """Those ranges, read on the fine lattice the coarse one stands for."""
    low, high = block_bounds(label, count)
    limit = np.array(shape, dtype=np.int64) - 1
    return low * stride, np.where(high < 0, -1, np.minimum((high + 1) * stride - 1, limit))


# -- what a block reaches to ----------------------------------------------


def point_support(
    points: np.ndarray, who: np.ndarray, directions: np.ndarray, count: int
) -> np.ndarray:
    """The same, read off the model's own surface rather than off the lattice.

    Which is what stone has to be measured with.  A hull taken from the
    corners the lattice happens to have found sits up to a cell inside the
    real surface, and a block that sits inside the model is a block the model
    shows through; a hull taken from the surface itself holds every point of
    it, so the stone is genuinely outside the model everywhere.
    """
    out = np.full((count, len(directions)), -np.inf)
    keep = who >= 0
    if count == 0 or not keep.any():
        return out
    place, who = points[keep].astype(np.float32), who[keep]
    order = np.argsort(who, kind="stable")
    place, who = place[order], who[order]
    every = np.arange(count)
    start = np.searchsorted(who, every, side="left")
    filled = np.searchsorted(who, every, side="right") > start
    for j in range(len(directions)):
        reach = place @ directions[j].astype(np.float32)
        out[filled, j] = np.maximum.reduceat(reach, start[filled]).astype(np.float64)
    return out


def block_field(
    origin: np.ndarray,
    step: float,
    shape: tuple,
    directions: np.ndarray,
    offsets: np.ndarray,
    low: np.ndarray,
    high: np.ndarray,
    outside: float,
) -> tuple[np.ndarray, np.ndarray]:
    """The union of the blocks, as a field whose zero is its surface.

    Each block is the meeting of its own half-spaces, which is a maximum; the
    blocks are joined by a minimum, which is what a union is.  Both are
    continuous, so the surface this leaves has nothing to tear along.  A block
    is only written inside the box it lives in, because that is where it is: a
    hull of a set of corners sits inside the box those corners sit in, and a
    few cells of room round that is more than enough for the surface to be
    found.

    Comes back as the field and, at every corner, which direction won it.
    """
    value = np.full(shape, np.float32(outside), dtype=np.float32)
    facing = np.zeros(shape, dtype=np.int16)
    for p in range(len(offsets)):
        if high[p, 0] < low[p, 0] or not np.isfinite(offsets[p]).all():
            continue
        box = tuple(
            slice(
                max(int(low[p, a]) - BOX_PAD, 0),
                min(int(high[p, a]) + 1 + BOX_PAD, shape[a]),
            )
            for a in range(3)
        )
        if any(b.stop <= b.start for b in box):
            continue
        rows = _rows(origin, step, box)
        room = tuple(b.stop - b.start for b in box)
        held = np.empty(room, dtype=np.float32)
        won = np.zeros(room, dtype=np.int16)
        for j in range(len(directions)):
            trial = (
                rows[0] * np.float32(directions[j, 0])
                + rows[1] * np.float32(directions[j, 1])
                + rows[2] * np.float32(directions[j, 2])
                - np.float32(offsets[p, j])
            )
            if j == 0:
                held[...] = trial
                continue
            better = trial > held
            np.copyto(held, np.broadcast_to(trial, room), where=better)
            np.copyto(won, np.int16(j), where=better)
        better = held < value[box]
        np.copyto(value[box], held, where=better)
        np.copyto(facing[box], won, where=better)
    return value, facing


#: The eight corners of a box, as which end of each range to take.
_BOX_CORNERS = np.array(
    [[a, b, c] for a in (False, True) for b in (False, True) for c in (False, True)]
)


def piece_bounds(frame: np.ndarray, offsets: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The box a lump of clay lives in, read off the six facings of its frame.

    Those six come first in every lump and they are a box on their own, so
    whatever else the lump is cut with it sits inside them -- which is all a
    bounding box has to be right about.
    """
    ends = np.where(_BOX_CORNERS, offsets[0:6:2], -offsets[1:6:2]) @ frame.T
    return ends.min(axis=0), ends.max(axis=0)


def union_field(
    origin: np.ndarray,
    step: float,
    shape: tuple,
    pieces: list,
    outside: float,
) -> tuple[np.ndarray, np.ndarray]:
    """The union of a set of convex solids, as a field whose zero is its surface.

    The same arithmetic as :func:`block_field` -- a maximum within a solid,
    which is an intersection of half-spaces, and a minimum between them, which
    is a union -- but with two differences, and both are what makes clay clay.

    Each solid brings its own facings rather than sharing one set, because a
    lump is set square to the mass it was pressed into and no two masses of a
    figure lie the same way.  So the direction that won a corner is handed back
    as the direction itself rather than as an index into a shared table.

    And the union is exact: whichever solid is nearer, outright.  There was a
    softened version of this once, which rounded off the crease two lumps leave
    where they cross -- but a soft minimum reaches past both of the solids it
    joins, and the only thing standing between it and the model was the model
    itself, so wherever it reached that far the clay came back wearing the
    model's own rounded surface instead of a flat.  Creases are dealt with
    afterwards instead, in :func:`close_gaps`, which cannot leave the material
    the solids actually hold.
    """
    value = np.full(shape, np.float32(outside), dtype=np.float32)
    facing = np.zeros((*shape, 3), dtype=np.float32)
    for directions, offsets, frame, _scale in pieces:
        low, high = piece_bounds(frame, offsets)
        box = tuple(
            slice(
                max(int(np.floor((low[a] - origin[a]) / step)) - BOX_PAD, 0),
                min(int(np.ceil((high[a] - origin[a]) / step)) + 1 + BOX_PAD, shape[a]),
            )
            for a in range(3)
        )
        if any(b.stop <= b.start for b in box):
            continue
        rows = _rows(origin, step, box)
        room = tuple(b.stop - b.start for b in box)
        held = np.empty(room, dtype=np.float32)
        won = np.zeros(room, dtype=np.int16)
        for j in range(len(directions)):
            trial = (
                rows[0] * np.float32(directions[j, 0])
                + rows[1] * np.float32(directions[j, 1])
                + rows[2] * np.float32(directions[j, 2])
                - np.float32(offsets[j])
            )
            if j == 0:
                held[...] = trial
                continue
            better = trial > held
            np.copyto(held, np.broadcast_to(trial, room), where=better)
            np.copyto(won, np.int16(j), where=better)
        nearer = held < value[box]
        np.copyto(value[box], held, where=nearer)
        np.copyto(facing[box], directions.astype(np.float32)[won], where=nearer[..., None])
    return value, facing


# -- reading the surface back out -----------------------------------------


def _truncated_solve(moment: np.ndarray, reach: np.ndarray, anchor: np.ndarray) -> np.ndarray:
    """How far to move, along the directions the planes actually pin down."""
    firmness, frame = np.linalg.eigh(moment)
    residual = reach - np.einsum("pij,pj->pi", moment, anchor)
    strongest = np.maximum(firmness[:, -1:], 1e-12)
    held = firmness >= np.maximum(QEF_FLOOR * strongest, 1e-12)
    along = np.einsum("pji,pj->pi", frame, residual) / np.where(
        held, firmness + QEF_ANCHOR * strongest, 1.0
    )
    return np.einsum("pij,pj->pi", frame, np.where(held, along, 0.0))


def dual_contour(
    value: np.ndarray, facing: np.ndarray, origin: np.ndarray, step: float
) -> tuple[np.ndarray, np.ndarray]:
    """The surface where ``value`` changes sign, one vertex per lattice cell.

    Each cell that the surface passes through gets a single vertex, placed
    where the planes crossing that cell agree best -- the crossings themselves
    say where, and the normals there say how firmly each direction is held.  A
    cell inside a facet is held in one direction and its vertex slides onto
    the facet; a cell along a crease is held in two and its vertex lands on the
    line; a cell at a corner is held in three.  Nothing has to detect an edge:
    what the surface is doing in a cell and how well determined the cell is
    turn out to be the same question.

    Then every crossing edge of the lattice is a little quad joining the four
    cells around it, which is what makes the result closed.
    """
    inside = value <= 0.0
    corners = (
        inside[:-1, :-1, :-1].astype(np.uint8)
        + inside[1:, :-1, :-1]
        + inside[:-1, 1:, :-1]
        + inside[1:, 1:, :-1]
        + inside[:-1, :-1, 1:]
        + inside[1:, :-1, 1:]
        + inside[:-1, 1:, 1:]
        + inside[1:, 1:, 1:]
    )
    live = (corners > 0) & (corners < 8)
    cell = np.stack(np.nonzero(live), axis=1)
    if len(cell) == 0:
        return np.zeros((0, 3)), np.zeros((0, 3), dtype=np.int64)
    numbering = np.full(live.shape, -1, dtype=np.int64)
    numbering[live[...]] = np.arange(len(cell))

    total = len(cell)
    moment = np.zeros((total, 3, 3))
    reach = np.zeros((total, 3))
    middle = np.zeros((total, 3))
    heard = np.zeros(total)
    base = origin + cell * step

    for axis in range(3):
        others = [(axis + 1) % 3, (axis + 2) % 3]
        for near in (0, 1):
            for far in (0, 1):
                step_in = np.zeros((1, 3), dtype=np.int64)
                step_in[0, others[0]] = near
                step_in[0, others[1]] = far
                low = cell + step_in
                high = low.copy()
                high[:, axis] += 1
                start = value[low[:, 0], low[:, 1], low[:, 2]].astype(np.float64)
                stop = value[high[:, 0], high[:, 1], high[:, 2]].astype(np.float64)
                crossing = np.flatnonzero((start <= 0.0) != (stop <= 0.0))
                if len(crossing) == 0:
                    continue
                a, b = start[crossing], stop[crossing]
                walk = np.clip(a / np.where(np.abs(a - b) > 1e-30, a - b, 1.0), 0.0, 1.0)
                point = origin + low[crossing] * step
                point[:, axis] += walk * step
                # The plane the surface is actually on here is the one holding
                # the nearer end of the edge.
                closer = np.where((np.abs(a) <= np.abs(b))[:, None], low[crossing], high[crossing])
                normal = facing[closer[:, 0], closer[:, 1], closer[:, 2]].astype(np.float64)
                depth = np.einsum("ij,ij->i", normal, point)
                np.add.at(heard, crossing, 1.0)
                np.add.at(middle, crossing, point)
                np.add.at(reach, crossing, normal * depth[:, None])
                np.add.at(moment, crossing, normal[:, :, None] * normal[:, None, :])

    share = np.maximum(heard, 1.0)
    moment /= share[:, None, None]
    reach /= share[:, None]
    middle /= share[:, None]
    anchor = np.where(heard[:, None] > 0.0, middle, base + 0.5 * step)
    vertex = anchor + _truncated_solve(moment, reach, anchor)
    vertex = np.clip(vertex, base - CELL_SLACK * step, base + (1.0 + CELL_SLACK) * step)
    vertex = np.where(np.isfinite(vertex), vertex, anchor)

    faces: list[np.ndarray] = []
    for axis in range(3):
        others = [(axis + 1) % 3, (axis + 2) % 3]
        limit = [live.shape[a] for a in range(3)]
        span: list = [slice(None)] * 3
        span[axis] = slice(0, limit[axis])
        span[others[0]] = slice(1, limit[others[0]])
        span[others[1]] = slice(1, limit[others[1]])
        low = tuple(span)
        high: list = list(span)
        high[axis] = slice(1, limit[axis] + 1)
        start = value[low]
        stop = value[tuple(high)]
        crossing = np.stack(np.nonzero((start <= 0.0) != (stop <= 0.0)), axis=1)
        if len(crossing) == 0:
            continue
        seed = crossing + np.array([[0 if a == axis else 1 for a in range(3)]], dtype=np.int64)
        ring = []
        for back, side in ((0, 0), (1, 0), (1, 1), (0, 1)):
            corner = seed.copy()
            corner[:, others[0]] -= 1 - back
            corner[:, others[1]] -= 1 - side
            ring.append(numbering[corner[:, 0], corner[:, 1], corner[:, 2]])
        quad = np.stack(ring, axis=1)
        outward = start[crossing[:, 0], crossing[:, 1], crossing[:, 2]] <= 0.0
        quad = np.where(outward[:, None], quad, quad[:, ::-1])
        faces.append(np.stack([quad[:, 0], quad[:, 1], quad[:, 2]], axis=1))
        faces.append(np.stack([quad[:, 0], quad[:, 2], quad[:, 3]], axis=1))

    if not faces:
        return vertex, np.zeros((0, 3), dtype=np.int64)
    return vertex, np.concatenate(faces)


def close_gaps(
    value: np.ndarray, step: float, rounds: int, reach: int = MEDIAN_REACH
) -> np.ndarray:
    """Median-filter the volume, so that what is remeshed has no slots in it.

    The surface between two solids that cross at an angle is a groove running
    into the material, and a groove one cell wide is worse than it sounds: it
    is a dark slot to the eye, and to dual contouring it is a cell whose planes
    agree on a point deep inside the material, which comes back as a spike.
    Closing them here, in the volume, is both cheaper and better behaved than
    trying to mend the surface afterwards -- there is nothing to mend, because
    the surface is found after this rather than before it.

    Only the band the surface actually runs through is filtered, which is a few
    cells of a lattice rather than all of it; everywhere else the field is far
    from zero and its median is itself.  See :data:`MEDIAN_ROUNDS` for why this
    leaves the flats alone.
    """
    if int(rounds) <= 0:
        return value
    reach = max(int(reach), 1)
    steps = range(-reach, reach + 1)
    limit = np.array(value.shape, dtype=np.int64) - 1
    for _ in range(int(rounds)):
        # Wide enough that every corner whose neighbourhood straddles the
        # surface is in it, and no wider.
        band = np.abs(value) <= np.float32((reach + 1.5) * step)
        at = np.nonzero(band)
        if len(at[0]) == 0:  # pragma: no cover - a field with no surface in it
            return value
        seen = np.empty(((2 * reach + 1) ** 3, len(at[0])), dtype=np.float32)
        row = 0
        for dx in steps:
            for dy in steps:
                for dz in steps:
                    seen[row] = value[
                        np.clip(at[0] + dx, 0, limit[0]),
                        np.clip(at[1] + dy, 0, limit[1]),
                        np.clip(at[2] + dz, 0, limit[2]),
                    ]
                    row += 1
        value = value.copy()
        value[band] = np.median(seen, axis=0)
    return value


def _slope(field: np.ndarray, step: float) -> list:
    """The gradient of a lattice field, by central differences.

    Which is the direction a distance field's own surface faces, and steadier
    than working it out from the nearest point on the model: the nearest point
    is only found to within a fraction of a cell, and a corner sitting almost
    on the surface has that fraction pointing sideways.
    """
    out = []
    for axis in range(3):
        rise = np.zeros_like(field)
        ahead: list = [slice(None)] * 3
        behind: list = [slice(None)] * 3
        middle: list = [slice(None)] * 3
        ahead[axis] = slice(2, None)
        behind[axis] = slice(0, -2)
        middle[axis] = slice(1, -1)
        rise[tuple(middle)] = (field[tuple(ahead)] - field[tuple(behind)]) / (2.0 * step)
        out.append(rise)
    return out


def whole_pieces(
    vertex: np.ndarray, face: np.ndarray, share: float, against: np.ndarray
) -> np.ndarray:
    """Drop the loose pieces, keeping the form and anything of its size.

    A block is a bounded thing and a model is not always a connected one, so
    what comes back can honestly be in several parts.  Occasionally one of
    them is a chip of stone on the floor rather than part of the carving.

    Two things mark a chip.  It never comes near the model -- ``against`` says
    which vertices do -- and it is small.  Either is enough to drop it, and
    between them they keep a model that genuinely comes in several parts while
    losing what fell off it.
    """
    total = len(vertex)
    if len(face) == 0:
        return face
    root = np.arange(total)
    for _ in range(_PIECE_ROUNDS):
        before = root.copy()
        for a, b in ((0, 1), (1, 2), (2, 0)):
            np.minimum.at(root, face[:, a], root[face[:, b]])
            np.minimum.at(root, face[:, b], root[face[:, a]])
        root = root[root]
        if np.array_equal(root, before):
            break
    piece = np.unique(root, return_inverse=True)[1].ravel()[face[:, 0]]
    corners = vertex[face]
    area = np.linalg.norm(
        np.cross(corners[:, 1] - corners[:, 0], corners[:, 2] - corners[:, 0]), axis=1
    )
    spread = np.bincount(piece, weights=area)
    lands = np.bincount(piece, weights=against[face[:, 0]].astype(np.float64)) > 0.0
    return face[lands[piece] & (spread[piece] >= share * spread.max())]


def _read_at(fields: list, points: np.ndarray, origin: np.ndarray, step: float) -> list:
    """Read lattice fields at places between their corners, straight-line.

    Nearest-corner would do for telling inside from outside, and will not do
    here: a surface pushed back onto the model by a value that only changes at
    a corner is pushed back in steps, and the steps show as a ripple running
    across the form in lattice rows.
    """
    shape = np.array(fields[0].shape[:3], dtype=np.int64)
    at = (np.asarray(points, dtype=np.float64) - origin) / step
    low = np.clip(np.floor(at).astype(np.int64), 0, shape - 2)
    near = np.clip(at - low, 0.0, 1.0)
    far = 1.0 - near
    out = [np.zeros((len(points), *field.shape[3:])) for field in fields]
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                share = (
                    (near[:, 0] if dx else far[:, 0])
                    * (near[:, 1] if dy else far[:, 1])
                    * (near[:, 2] if dz else far[:, 2])
                )
                corner = (low[:, 0] + dx, low[:, 1] + dy, low[:, 2] + dz)
                for held, field in zip(out, fields, strict=True):
                    weight = share.reshape(-1, *([1] * (held.ndim - 1)))
                    held += weight * field[corner]
    return out


def _back_inside(
    points: np.ndarray,
    model: np.ndarray,
    slope: np.ndarray,
    origin: np.ndarray,
    step: float,
) -> np.ndarray:
    """Put anything that has drifted out of the model back onto its surface.

    One Newton step down the model's own distance field, which is a true
    straight-line distance near the surface, so a point a little way out lands
    on the surface rather than merely nearer it.
    """
    depth, away = _read_at([model, slope], points, origin, step)
    reach = np.linalg.norm(away, axis=1)
    over = (depth > 0.0) & (reach > 1e-9)
    if not over.any():
        return points
    points = points.copy()
    points[over] -= away[over] * (depth[over] / reach[over])[:, None]
    return points


def relax_surface(
    vertex: np.ndarray,
    face: np.ndarray,
    rounds: int,
    model: np.ndarray,
    origin: np.ndarray,
    step: float,
    shape: tuple,
) -> np.ndarray:
    """Settle the surface into itself, without letting it out of the model.

    What a sculptor does last: go over the block-in with the flat of a tool and
    take the corners off it, so the planes still read but the form is no longer
    quarried out of them.  It is worked on the mesh rather than on the volume
    because by this point the volume has said everything it has to say -- where
    the flats are and where they meet -- and what is left is a question about
    the surface itself.

    Every round is a pull towards the middle of each vertex's neighbours and
    then a slightly larger push back out; see :data:`RELAX_PULL`.  After each
    of those, anything that has ended up outside the model is put back onto it,
    which is the one thing clay may not do and the reason the relax cannot
    quietly undo the containment everything upstream was careful about.
    """
    if int(rounds) <= 0 or len(face) == 0 or len(vertex) == 0:
        return vertex
    ends = np.concatenate([face[:, 0], face[:, 1], face[:, 2], face[:, 1], face[:, 2], face[:, 0]])
    others = np.concatenate(
        [face[:, 1], face[:, 2], face[:, 0], face[:, 0], face[:, 1], face[:, 2]]
    )
    heard = np.bincount(ends, minlength=len(vertex))
    moving = heard > 0
    share = np.maximum(heard, 1).astype(np.float64)
    slope = np.stack(_slope(model, step), axis=-1)
    out = np.asarray(vertex, dtype=np.float64).copy()
    for _ in range(int(rounds)):
        for pull in (RELAX_PULL, RELAX_PUSH):
            middle = np.stack(
                [
                    np.bincount(ends, weights=out[others, a], minlength=len(vertex))
                    for a in range(3)
                ],
                axis=1,
            )
            drift = (middle / share[:, None] - out) * pull
            out[moving] += drift[moving]
            out = _back_inside(out, model, slope, origin, step)
    return out


def _flat_mesh(vertex: np.ndarray, face: np.ndarray, name: str, **rest) -> Mesh:
    """A mesh that shades every facet flat and every crease as an edge.

    A vertex on a crease belongs to both facets, and averaging their normals
    into it would round off the one thing this is for.  So each triangle keeps
    its own corners and its own normal, which is exact: every triangle of the
    result lies in one of the planes, so all the triangles of a facet report
    the same direction and the facet reads as one flat.
    """
    corners = vertex[face]
    cross = np.cross(corners[:, 1] - corners[:, 0], corners[:, 2] - corners[:, 0])
    length = np.linalg.norm(cross, axis=1)
    keep = length > 1e-12
    corners, cross, length = corners[keep], cross[keep], length[keep]
    normal = cross / length[:, None]
    return Mesh(
        corners.reshape(-1, 3).astype(np.float32),
        np.repeat(normal, 3, axis=0).astype(np.float32),
        np.arange(3 * len(corners), dtype=np.uint32).reshape(-1, 3),
        name,
        **rest,
    )


# -- the two ways of working ----------------------------------------------


def _frame(points: np.ndarray) -> np.ndarray:
    """Which three ways a lump of material runs.  Columns, thinnest first.

    Thinnest first because that is the order a lump is grown in.  A lump that
    has taken its thickness first can then sweep that whole cross-section down
    the length of the mass; one that took its length first is a needle, and
    there is nothing left to sweep.
    """
    if len(points) < 8:
        return np.eye(3)
    centred = points - points.mean(axis=0)
    return np.ascontiguousarray(np.linalg.eigh(centred.T @ centred / len(points))[1])


def _box_facings(frame: np.ndarray) -> np.ndarray:
    """The six faces of a block set square to ``frame``, thin axis first."""
    out = np.empty((6, 3))
    out[0::2] = frame.T
    out[1::2] = -frame.T
    return out


def _tube_facings(frame: np.ndarray, bevels: np.ndarray) -> np.ndarray:
    """Those six, the twenty corners off them, and the form's own planes."""
    corners = _corner_facings()
    slanted = corners[np.count_nonzero(np.abs(corners) > 1e-9, axis=1) > 1]
    return np.concatenate([_box_facings(frame), slanted @ frame.T, bevels])


def outside_points(room: np.ndarray, origin: np.ndarray, step: float) -> np.ndarray:
    """Where the model stops: the corners just outside ``room``.  ``(n, 3)``.

    Only the ones with material beside them, and that is not a shortcut but the
    whole boundary a convex lump can ever feel.  A lump holds its seed, which
    is inside the model; if it also held a corner further out than the surface
    it would hold every corner on the way there, the first one past the surface
    included.  So the first ones are the only ones worth measuring against, and
    there are a great many fewer of them than there are corners outside.
    """
    edge = np.zeros(room.shape, dtype=bool)
    for axis in range(3):
        for forward in (True, False):
            here, there = _shifts(axis, forward, 1)
            edge[here] |= room[there]
    edge &= ~room
    return origin + np.stack(np.nonzero(edge), axis=1) * step


def fit_piece(
    directions: np.ndarray, offsets: np.ndarray, wall: np.ndarray, caps: np.ndarray
) -> tuple[np.ndarray, float]:
    """The largest solid of those facings that fits in the model, from a start.

    Two passes, and both are exact rather than stepped.

    The first moves the whole shape in or out together, keeping it the shape it
    was.  A point of the wall is inside the shape with every facing moved out
    by ``t`` exactly when ``t`` is at least how far that point lies past the
    furthest of the facings, so the largest such move that touches nothing is
    the least of that over the whole wall.  It can be negative, and that is the
    useful half: a shape handed in already poking out of the model is pulled
    back in by exactly enough.

    The second takes up the slack one facing at a time.  A facing may be pushed
    out until it lets a point of the wall in, and the only points it *can* let
    in are those every other facing is already holding out -- so the distance
    is the least, over exactly those points, of how far past this facing they
    lie.  Pushing one facing can only ever take points out of that set, never
    add them, so a single sweep settles the whole solid.

    ``caps`` are offsets no facing may be pushed past.  Without them a facing
    that no point of the wall is holding on its own runs away to nothing --
    which is a perfectly good solid, since some other facing catches it in the
    end, but it is a solid that has left the mass it was seeded in and gone
    looking down the leg.  The cap is what keeps a piece a reading of the form
    it was fitted to.

    Comes back as the fitted offsets and as how far the first pass moved the
    shape: out of the model if it is negative, into room it had if not.
    """
    across = np.asarray(directions, dtype=np.float64)
    base = np.asarray(offsets, dtype=np.float64)
    caps = np.asarray(caps, dtype=np.float64)
    if len(wall) == 0:  # pragma: no cover - a lattice with no outside at all
        return np.maximum(base, caps), math.inf
    past = wall.astype(np.float32) @ across.astype(np.float32).T - base.astype(np.float32)
    room = float(past.max(axis=1).min())
    past -= np.float32(room)
    grown = base + room
    reach = np.maximum(caps, grown)

    # Most of the wall is nowhere near this solid, and the second pass is the
    # expensive one.  A point that is still held out when every facing has been
    # pushed as far as its cap allows can never be the point that stops a push,
    # so it can be dropped outright: whichever facing is holding it either
    # keeps holding it, in which case it is never the last one, or is the
    # facing being pushed, in which case the cap stops the push before it does.
    kept = (past - (reach - grown).astype(np.float32)).max(axis=1) <= 0.0
    past = np.ascontiguousarray(past[kept])

    over = past > 0.0
    count = over.sum(axis=1)
    total = over @ np.arange(len(across), dtype=np.int64)
    for j in range(len(across)):
        alone = (count == 1) & (total == j)
        push = float(past[alone, j].min()) if alone.any() else np.inf
        push = min(max(push, 0.0), float(reach[j] - grown[j]))
        if push <= 0.0:
            continue
        grown[j] += push
        past[:, j] -= np.float32(push)
        dropped = over[:, j] & ~(past[:, j] > 0.0)
        if dropped.any():
            over[dropped, j] = False
            count[dropped] -= 1
            total[dropped] -= j
    return grown, room


def grow_piece(
    seed: np.ndarray, directions: np.ndarray, wall: np.ndarray, caps: np.ndarray
) -> np.ndarray | None:
    """The largest solid of those facings that fits in the model round ``seed``.

    :func:`fit_piece` started from nothing at all: every facing on the seed
    itself, so the first pass inflates the lump's own shape about it.  ``caps``
    is how far the material round the seed actually reaches along each facing,
    read from the seed.

    Comes back as the offset of each facing, or ``None`` for a seed with no
    room round it at all.
    """
    base = np.asarray(directions, dtype=np.float64) @ np.asarray(seed, dtype=np.float64)
    offsets, room = fit_piece(directions, base, wall, base + np.asarray(caps, dtype=np.float64))
    return None if room <= 0.0 else offsets


def join_pieces(
    pieces: list, held: list, place: np.ndarray, wall: np.ndarray, bevels: np.ndarray, budget: int
) -> list:
    """Clay pushed across the joins between the lumps already laid down.

    Two lumps pressed into the same form leave a notch where they cross, and a
    surface full of notches reads as a heap of stones rather than as a body.
    What a sculptor does about it is push a further piece of clay across the
    join and work it down until it lies flush with both -- and the shape of
    that piece, before it is worked down, is the hull of the two it bridges.

    So that is what this is.  Each pair of lumps lying near enough to be joined
    is given the smallest solid of well-spread facings that holds all of both
    lumps' material, which is the hull of the two read off the material itself;
    and that hull is then pulled back until it is inside the model, exactly the
    way a lump is grown out to it.  Nothing here can reach past the model, and
    nothing here is a rounded blend: what fills the notch is a handful of
    flats, cut from the same facings the lumps themselves are cut from.

    Pairs are taken biggest first and a join that has to be pulled in further
    than the lumps are thick is dropped -- see :data:`JOIN_ROOM`.
    """
    if len(pieces) < 2 or int(budget) <= 0:
        return []
    boxes = [piece_bounds(frame, offsets) for _, offsets, frame, _ in pieces]
    pairs = []
    for i in range(len(pieces)):
        for j in range(i + 1, len(pieces)):
            reach = min(pieces[i][3], pieces[j][3])
            apart = np.maximum(boxes[i][0] - boxes[j][1], boxes[j][0] - boxes[i][1]).max()
            if apart > reach:  # too far apart for one piece of clay to bridge
                continue
            pairs.append((reach, i, j))
    pairs.sort(key=lambda pair: -pair[0])

    out: list = []
    for reach, i, j in pairs:
        if len(out) >= int(budget):
            break
        # The seam, and only the seam: what of each lump lies within a collar
        # of the other.  Two lumps that never come that close have no seam and
        # nothing to join, which is most of the pairs a bounding box lets
        # through.
        span = JOIN_SPAN * reach
        mine, theirs = place[held[i]], place[held[j]]
        points = np.concatenate(
            [
                mine[(mine @ pieces[j][0].T - pieces[j][1]).max(axis=1) <= span],
                theirs[(theirs @ pieces[i][0].T - pieces[i][1]).max(axis=1) <= span],
            ]
        )
        if len(points) < 8:
            continue
        middle = points.mean(axis=0)
        frame = _frame(points - middle)
        facing = _tube_facings(frame, bevels)
        hull = (points @ facing.T).max(axis=0)
        low = np.minimum(boxes[i][0], boxes[j][0])
        high = np.maximum(boxes[i][1], boxes[j][1])
        near = np.all((wall >= low) & (wall <= high), axis=1)
        offsets, room = fit_piece(facing, hull, wall[near], hull)
        if -room > JOIN_ROOM * reach:
            continue
        out.append((facing, offsets, frame, max(float((offsets - facing @ middle).min()), 0.0)))
    return out


def clay_pieces(
    model: np.ndarray,
    origin: np.ndarray,
    step: float,
    bevels: np.ndarray,
    masses: int,
    wanted: int,
) -> list:
    """Lumps of clay pressed into the model, the biggest masses first.

    The seed of the next lump is the material that is at once deepest inside
    the model and furthest from the clay already there, which is the one
    question this whole mode turns on.  The first few land in the ribcage, the
    pelvis, the thighs -- the masses a figure is blocked in as.  The ones after
    that land in whatever is left over, which is how the arms come before the
    hands and the hands before the fingers.  Nothing is ever told what a limb
    is: the order falls out of asking where the most uncovered material is.

    The first ``masses`` lumps are plain rectangular blocks, set square to the
    mass each sits in.  The rest are tubes, allowed the form's own planes as
    well, so they are bevelled where the model turns.  Then the joins between
    them are filled, which is :func:`join_pieces`.

    Comes back as ``(facings, offsets, frame, half-thickness)`` for each lump,
    the last of these being how far the lump reaches along its nearest facing,
    which is the scale everything about it is judged on.
    """
    stride = 1
    while model.size // stride**3 > GROW_CORNERS:
        stride += 1
    grow_step = step * stride
    depth = -np.ascontiguousarray(model[::stride, ::stride, ::stride]).astype(np.float64)
    safety = PIECE_SAFETY * grow_step
    room = depth > safety
    if not room.any():  # a form thinner than the lattice can hold a lump in
        safety, room = 0.0, depth > 0.0
    if not room.any():  # pragma: no cover - a model the lattice never found
        return []

    wall = outside_points(room, origin, grow_step)
    place = origin + np.stack(np.nonzero(room), axis=1) * grow_step
    spots = place.astype(np.float32)
    deep = depth[room]
    free = np.full(len(place), np.inf)

    out: list = []
    held: list = []
    for lump in range(max(int(wanted), 1)):
        # Deepest in the model and furthest from the clay, both at once.
        pick = int(np.argmax(np.minimum(deep, free)))
        if min(deep[pick], free[pick]) <= safety:
            break
        seed = place[pick]
        # The mass this seed sits in: near enough to be part of it, and read
        # over the material the clay has not already taken, so a second lump in
        # a mass lies along what is left of it rather than along the whole.
        span = max(FRAME_SPAN * deep[pick], 3.0 * grow_step)
        near = np.abs(place - seed).max(axis=1) <= span
        bare = near & (free > 0.0)
        mass = place[near] - seed
        # Which way the lump lies is read off what is still bare, so a second
        # lump in a mass runs along what is left of it rather than along the
        # whole; how far it may reach is read off all of the material, bare or
        # not, so that it can lie *across* the clay already there and join to
        # it.  A lump held to the bare sliver it was seeded in could never
        # bridge a gap, and the form would stay a heap of separate stones.
        frame = _frame(place[bare] - seed if bare.sum() >= 8 else mass)
        facing = _box_facings(frame) if lump < masses else _tube_facings(frame, bevels)
        offsets = grow_piece(seed, facing, wall, (mass @ facing.T).max(axis=0))
        if offsets is None:  # pragma: no cover - a seed with no room round it
            deep[pick] = 0.0
            continue
        out.append((facing, offsets, frame, float((offsets - facing @ seed).min())))
        mine = (spots @ facing.astype(np.float32).T - offsets).max(axis=1)
        held.append(np.flatnonzero(mine <= 0.0))
        free = np.minimum(free, mine)
    return out + join_pieces(out, held, place, wall, bevels, min(len(out), MAX_JOINS))


def carve(
    vertices: np.ndarray,
    triangles: np.ndarray,
    seeds: np.ndarray,
    seed_normals: np.ndarray,
    directions: np.ndarray,
    additive: bool,
    masses: int,
    wanted: int,
    relax: int = 0,
    median: int = MEDIAN_ROUNDS,
    median_reach: int = MEDIAN_REACH,
    resolution: int = RESOLUTION,
    name: str = "mesh",
    source_offset: np.ndarray | None = None,
    units: object = None,
) -> Mesh:
    """The form ``directions`` leave of the model, worked one way or the other.

    ``seeds`` are points spread over the model with the way it faces at each,
    which is how the lattice learns the model's own shape.  ``directions`` are
    the planes of the fit.  ``wanted`` is how many solids the form is made of
    -- blocks of stone cut down from the hull, or lumps of clay pressed into
    the model -- and ``masses`` how many of the lumps are the plain rectangular
    blocks a figure is first blocked in as, and ``relax`` how many passes are
    then run over the finished surface to take the corners off it.  Neither
    says anything to stone, which starts from a block rather than from a lump
    and is meant to keep its corners.  ``median`` and ``median_reach`` are how
    many passes of the filter that closes the clay's slots are run and how far
    each of them reaches; see :func:`close_gaps`.  ``resolution`` is how fine a
    lattice the whole of it is worked on, which is what the detail slider
    spends itself on once it has bought every plane there is.
    """
    vertices = np.asarray(vertices, dtype=np.float64).reshape(-1, 3)
    seeds = np.asarray(seeds, dtype=np.float64).reshape(-1, 3)
    seed_normals = np.asarray(seed_normals, dtype=np.float64).reshape(-1, 3)
    facing_set = facings(directions)
    span = float(np.ptp(vertices, axis=0).max()) if len(vertices) else 1.0
    origin, step, shape = lattice(
        vertices.min(axis=0), vertices.max(axis=0), MARGIN_SHARE * span, resolution
    )

    within = solid(vertices, triangles, origin, step, shape)
    band = np.float32(SDF_REACH * step)
    gap, which = nearest_surface(seeds, origin, step, shape, SDF_REACH + 2)
    if not encloses(within, vertices, triangles, step):
        # A model with holes in it cannot be read by counting crossings, and
        # plenty of them have holes -- a scan left open at the base, a garment
        # with no inside.  Falling back on which way the nearest surface faces
        # is worse near a thin part and fine everywhere else, which is a good
        # deal better than a form turned inside out.
        grid = _axes(origin, step, shape)
        toward = seed_normals[which]
        closest = seeds[which]
        within = (
            sum(
                (grid[a] - closest[..., a].astype(np.float32))
                * toward[..., a].astype(np.float32)
                for a in range(3)
            )
            < 0.0
        )
    # The model's own field: a true distance where the lattice found the
    # surface, and flat at the edge of the band beyond that.  Saturating it is
    # harmless -- out there all it has to say is which side of the model a
    # corner is on.
    off = np.sqrt(np.minimum(gap, band * band)).astype(np.float32)
    model = np.where(within, -off, off).astype(np.float32)

    outside = float(band) * 8.0
    if additive:
        # Clay is fitted to the model's own thickness rather than cut out of
        # anything, so it never asks where the blocks are: a lump goes wherever
        # the most uncovered material is, and the next lump asks again.
        made = clay_pieces(
            model, origin, step, fitted_facings(directions), masses, wanted
        )
        if not made:  # pragma: no cover - a model the lattice never found
            return _flat_mesh(
                np.zeros((0, 3)),
                np.zeros((0, 3), dtype=np.int64),
                name,
                source_offset=source_offset,
                units=units,
            )
        field, facing = union_field(origin, step, shape, made, outside)
    else:
        label, stride, count = blocks(within, origin, step, wanted)
        if count == 0:  # pragma: no cover - a model the lattice never found
            return _flat_mesh(
                np.zeros((0, 3)),
                np.zeros((0, 3), dtype=np.int64),
                name,
                source_offset=source_offset,
                units=units,
            )
        # Which block each sample of the surface belongs to.  Stone is measured
        # off the surface itself rather than off the lattice, so that a block
        # provably holds every point of the model it stands for.
        at = np.clip(
            np.rint((seeds - origin) / (step * stride)).astype(np.int64),
            0,
            np.array(label.shape, dtype=np.int64) - 1,
        )
        who = label[at[:, 0], at[:, 1], at[:, 2]]
        offsets = point_support(seeds, who, facing_set, count)
        low, high = coarse_bounds(label, count, stride, shape)
        field, won = block_field(
            origin, step, shape, facing_set, offsets, low, high, outside
        )
        facing = facing_set[won].astype(np.float32)

    # The model is what the blocks are held against.  Stone may only add
    # material to it and clay may only take material away, which is what makes
    # one larger and the other smaller by construction rather than by luck; it
    # is also what keeps a hollow no block reached from being carved out to
    # nothing, because the model is in the way.
    value = np.maximum(field, model) if additive else np.minimum(field, model)
    theirs = (model > field) if additive else (model < field)

    # Which way the surface faces at a corner: where the model is what the
    # corner fell back on, the model's own rather than the plane that lost.
    if theirs.any():
        slope = np.stack(_slope(model, step), axis=-1)
        length = np.linalg.norm(slope, axis=-1)
        facing = np.where(
            (theirs & (length > 1e-6))[..., None],
            slope / np.maximum(length, 1e-9)[..., None],
            facing,
        ).astype(np.float32)

    if additive:
        # The slots the lumps leave between them, closed in the volume; then
        # held under the model again, because a median fills a groove by adding
        # material and some of those grooves run along the surface.
        settled = np.maximum(close_gaps(value, step, median, median_reach), model)
        # Where it filled something, and not merely where the arithmetic came
        # out a bit-width different: a facet that has been left alone must keep
        # the exact plane it was cut with, or the flats stop reading as flats.
        moved = np.abs(settled - value) > np.float32(0.25 * step)
        value = settled
        # Where it filled, the two planes that made the groove are no longer
        # what the surface is: the fill has a facing of its own, and leaving
        # the old pair in place would have the vertex solver put its corner
        # back down in the groove they cross at.
        if moved.any():
            slope = np.stack(_slope(value, step), axis=-1)
            length = np.linalg.norm(slope, axis=-1)
            facing = np.where(
                (moved & (length > 1e-6))[..., None],
                slope / np.maximum(length, 1e-9)[..., None],
                facing,
            ).astype(np.float32)

    vertex, face = dual_contour(value, facing, origin, step)
    at = np.clip(np.rint((vertex - origin) / step).astype(np.int64), 0, np.array(shape) - 1)
    against = np.abs(model[at[:, 0], at[:, 1], at[:, 2]]) <= PIECE_TOUCH * step
    # Stone can shed a chip; every lump of clay was put where it is on
    # purpose, and a small one is a finger rather than a mistake.
    kept = whole_pieces(vertex, face, 0.0 if additive else PIECE_SHARE, against)
    if additive:
        # After the chips are gone, so that a piece dropped from the form
        # cannot drag on the part of it that stayed.
        vertex = relax_surface(vertex, kept, relax, model, origin, step, shape)
    return _flat_mesh(
        vertex,
        kept,
        name,
        source_offset=source_offset,
        units=units,
    )
