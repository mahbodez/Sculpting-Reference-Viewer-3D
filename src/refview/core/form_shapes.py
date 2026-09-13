"""The primary forms of a figure, worked out from surface landmarks.

A sculptor blocks a figure in as a few big simple masses before anything else
is allowed to happen: the pelvis is a bucket with its front corner knocked
off, the ribcage is an egg with an arch chipped out of the bottom of its
front, the head is a wedge that is then given its width, its cranium and its
jaw.  None of those masses can be measured off a model directly -- nobody can
point at the axis of the pelvic bucket -- but every one of them is pinned down
by anatomy an artist *can* find: the crests of the hips and the two points at
the front of them, the notch at the top of the breastbone and the bottom of
it, the widest point of the skull.  So the forms here are built the way the
armature presets build their joints: ask for what is visible, and work out
the mass from it.

Each builder takes the placed landmarks and hands back the form as a list of
stages, each stage a list of convex solids (:class:`~refview.core.convex.Solid`)
to be laid over the ones before it.  Additive on purpose.  Clay goes on and
does not come off, so a head is not a ball with its sides sliced away but a
plate that is widened, then rounded, then given a jaw -- and a stage the
artist scrubs back to is a form they could have stopped at.

The measurements are ratios of the figure's own spans wherever a landmark
cannot say them outright, so one rule fits a child and a heroic nude; the
ratios are named below with what they stand for.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np

from .convex import DegenerateHullError, Solid

#: How many points a ring is sampled with.  Enough that the turn between two
#: facets is under ten degrees and reads as a curve once smoothed.
RING_SAMPLES = 40

#: Levels an egg is lofted through between the rings its landmarks pin down.
LOFT_LEVELS = 7

# -- ratios ----------------------------------------------------------------

#: Where the sitting bones are when a model does not show them, which is
#: most models: half the width between the ASIS apart, and this far below
#: the line from the pubic symphysis to the coccyx, both as shares of the
#: width between the ASIS.
OUTLET_HALF_WIDTH = 0.25
OUTLET_DROP = 0.12

#: The half-width of the top of the ribcage, the thoracic inlet, as a share
#: of its widest half-width.  The inlet itself is narrower than this, but the
#: mass of the ribcage a sculptor blocks in carries the first ribs and the
#: shoulders' roots.
INLET_WIDTH = 0.55

#: The half-thickness of the wedge the head starts as, as a share of the
#: height from chin to crown: about the width of the bridge of the nose, so
#: the slab stands between the eye sockets rather than over them.
WEDGE_HALF_WIDTH = 0.05

#: How wide the head is at each midline landmark once the paired ones are in,
#: as a share of the width they measure.  The crown narrows from the parietal
#: eminences; the chin is a fraction of the jaw's width; the back of the
#: skull stays broad, and the corner where the top turns into the back is
#: between the two.
CROWN_WIDTH = 0.45
CHIN_WIDTH = 0.35
OCCIPUT_WIDTH = 0.80
LAMBDA_WIDTH = 0.65
NAPE_WIDTH = 0.60

#: A ring's radius is never interpolated to more than this multiple of its
#: largest anchor, nor less than this share of its smallest, however the
#: anchors are spaced.
RADIUS_OVER = 1.5
RADIUS_UNDER = 0.6


def _unit(vector) -> np.ndarray:
    vector = np.asarray(vector, dtype=np.float64)
    length = float(np.linalg.norm(vector))
    return vector / length if length > 0.0 else vector


def _mid(*points) -> np.ndarray:
    return np.mean(np.stack([np.asarray(p, dtype=np.float64) for p in points]), axis=0)


def _across(vector, normal) -> np.ndarray:
    """``vector`` with its component along ``normal`` removed, made unit."""
    normal = _unit(normal)
    return _unit(np.asarray(vector, dtype=np.float64) - float(vector @ normal) * normal)


def fit_plane(points, toward) -> tuple[np.ndarray, np.ndarray]:
    """The least-squares plane through some points, its normal leaning ``toward``.

    Three points give their own plane exactly; more give the one they vary
    least across.  Two, or a straight line, fall back on the plane through
    them square to ``toward``, which is the best that can be said.
    """
    cloud = np.asarray(points, dtype=np.float64).reshape(-1, 3)
    origin = cloud.mean(axis=0)
    toward = _unit(toward)
    if len(cloud) < 3:
        return origin, toward
    _, spread, directions = np.linalg.svd(cloud - origin, full_matrices=False)
    if spread[0] <= 0.0 or spread[1] <= 1e-6 * spread[0]:
        return origin, toward
    normal = directions[2]
    if float(normal @ toward) < 0.0:
        normal = -normal
    return origin, normal


def plane_through(a, b, c, inside) -> tuple[np.ndarray, float]:
    """The plane through three points, as ``(normal, offset)`` with ``inside`` kept.

    Shaped for :meth:`~refview.core.convex.Solid.cut`: the side of the plane
    that ``inside`` lies on is the side ``normal @ x <= offset``.
    """
    a, b, c = (np.asarray(p, dtype=np.float64) for p in (a, b, c))
    normal = _unit(np.cross(b - a, c - a))
    if float(normal @ (np.asarray(inside, dtype=np.float64) - a)) > 0.0:
        normal = -normal
    return normal, float(normal @ a)


# -- rings and lofts ---------------------------------------------------------


@dataclass(frozen=True)
class Ring:
    """A closed curve round a mass, sampled at fixed angles about its centre.

    Kept as a polar profile rather than as points so that two rings can be
    interpolated angle by angle -- which is how an egg is lofted between the
    three rings its landmarks actually pin down.
    """

    origin: np.ndarray
    #: The two in-plane directions the angle is measured from, and the normal.
    u: np.ndarray
    v: np.ndarray
    normal: np.ndarray
    #: The radius at each sample angle, and how far above the plane the curve
    #: lies there -- so a rim can rise at the crests and dip at the front.
    radius: np.ndarray
    height: np.ndarray

    @property
    def points(self) -> np.ndarray:
        angles = np.linspace(0.0, 2.0 * np.pi, len(self.radius), endpoint=False)
        return (
            self.origin
            + np.outer(self.radius * np.cos(angles), self.u)
            + np.outer(self.radius * np.sin(angles), self.v)
            + np.outer(self.height, self.normal)
        )


def _periodic_hermite(angles: np.ndarray, values: np.ndarray, samples: int) -> np.ndarray:
    """A smooth closed curve through ``(angle, value)`` pairs, sampled evenly.

    Cubic Hermite spans between neighbouring anchors with finite-difference
    tangents -- a Catmull-Rom spline on an uneven, periodic knot vector -- so
    the curve passes through every anchor and turns smoothly at each.
    """
    order = np.argsort(angles)
    knots, held = angles[order], values[order]
    count = len(knots)
    wrapped_knots = np.concatenate([knots[-1:] - 2.0 * np.pi, knots, knots[:1] + 2.0 * np.pi])
    wrapped = np.concatenate([held[-1:], held, held[:1]])
    tangent = (wrapped[2:] - wrapped[:-2]) / np.maximum(
        wrapped_knots[2:] - wrapped_knots[:-2], 1e-9
    )
    tangent = np.concatenate([tangent[-1:], tangent, tangent[:1]])

    where = np.linspace(0.0, 2.0 * np.pi, samples, endpoint=False)
    where = knots[0] + (where - knots[0]) % (2.0 * np.pi)
    span = np.searchsorted(wrapped_knots, where, side="right") - 1
    span = np.clip(span, 0, count)
    left, right = wrapped_knots[span], wrapped_knots[span + 1]
    width = np.maximum(right - left, 1e-9)
    t = (where - left) / width
    t2, t3 = t * t, t * t * t
    return (
        (2.0 * t3 - 3.0 * t2 + 1.0) * wrapped[span]
        + (t3 - 2.0 * t2 + t) * width * tangent[span]
        + (-2.0 * t3 + 3.0 * t2) * wrapped[span + 1]
        + (t3 - t2) * width * tangent[span + 1]
    )


def ring_through(anchors: Sequence, origin, normal, across, samples: int = RING_SAMPLES) -> Ring:
    """A ring in the plane ``(origin, normal)`` passing through ``anchors``.

    The anchors are read in polar coordinates about the origin -- an angle,
    a radius, and a height above the plane -- and a smooth closed curve is
    fitted through them.  The radius is interpolated as ``1 / r²``, which is
    what makes four anchors a quarter turn apart come out as very nearly an
    ellipse rather than a rounded diamond; it is clamped so an uneven spacing
    cannot throw the curve far outside or inside its anchors.  ``across`` says which
    way angle zero lies, so two rings built with the same direction can be
    matched sample for sample.
    """
    origin = np.asarray(origin, dtype=np.float64)
    normal = _unit(normal)
    u = _across(across, normal)
    v = np.cross(normal, u)
    cloud = np.asarray(anchors, dtype=np.float64).reshape(-1, 3) - origin
    x, y, h = cloud @ u, cloud @ v, cloud @ normal
    r = np.hypot(x, y)
    if len(cloud) < 3:
        radius = np.full(samples, float(r.mean()) if len(cloud) else 1.0)
        return Ring(origin, u, v, normal, radius, np.zeros(samples))
    angles = np.arctan2(y, x)
    squeeze = 1.0 / np.maximum(r, 1e-9) ** 2
    fitted = _periodic_hermite(angles, squeeze, samples)
    fitted = np.clip(fitted, squeeze.min() / RADIUS_OVER**2, squeeze.max() / RADIUS_UNDER**2)
    radius = 1.0 / np.sqrt(fitted)
    height = _periodic_hermite(angles, h, samples)
    return Ring(origin, u, v, normal, radius, height)


def blend_rings(rings: Sequence[Ring], levels: Sequence[float], count: int) -> list[Ring]:
    """Rings lofted through the given ones, ``count`` of them evenly spaced.

    Each of origin, frame, radius and height is fitted with a polynomial
    through the rings at their ``levels`` -- a line through two, a parabola
    through three -- so a widest ring in the middle bulges the loft into an
    egg rather than a pair of cones.  The rings must share their sample count
    and have been built with the same ``across`` direction.
    """
    levels = np.asarray(levels, dtype=np.float64)
    where = np.linspace(float(levels.min()), float(levels.max()), count)
    weight = np.stack([_lagrange(levels, k, where) for k in range(len(levels))], axis=1)
    out: list[Ring] = []
    for row in weight:
        origin = sum(w * ring.origin for w, ring in zip(row, rings, strict=True))
        normal = _unit(sum(w * ring.normal for w, ring in zip(row, rings, strict=True)))
        u = _across(sum(w * ring.u for w, ring in zip(row, rings, strict=True)), normal)
        radius = sum(w * ring.radius for w, ring in zip(row, rings, strict=True))
        height = sum(w * ring.height for w, ring in zip(row, rings, strict=True))
        floor = RADIUS_UNDER * min(float(ring.radius.min()) for ring in rings)
        out.append(Ring(origin, u, np.cross(normal, u), normal, np.maximum(radius, floor), height))
    return out


def _lagrange(knots: np.ndarray, k: int, where: np.ndarray) -> np.ndarray:
    """The ``k``-th Lagrange basis polynomial through ``knots``, at ``where``."""
    out = np.ones_like(where)
    for j, knot in enumerate(knots):
        if j != k:
            out *= (where - knot) / (knots[k] - knot)
    return out


def loft(rings: Sequence[Ring]) -> Solid:
    """The convex solid through a stack of rings."""
    return Solid.from_points(np.concatenate([ring.points for ring in rings]))


# -- reading the landmarks --------------------------------------------------


class Placed:
    """The placed landmarks, read a few at a time."""

    def __init__(self, placed: dict[str, np.ndarray]) -> None:
        self._placed = placed

    def at(self, *keys: str) -> tuple[np.ndarray, ...] | None:
        """Every named landmark, or ``None`` when any one of them is missing."""
        found = []
        for key in keys:
            value = self._placed.get(key)
            if value is None:
                return None
            found.append(np.asarray(value, dtype=np.float64))
        return tuple(found)

    def pair(self, key: str) -> tuple[np.ndarray, np.ndarray] | None:
        return self.at(f"{key}.L", f"{key}.R")

    def maybe(self, key: str) -> np.ndarray | None:
        value = self._placed.get(key)
        return None if value is None else np.asarray(value, dtype=np.float64)


def _solids(*pieces: Solid | None) -> list[Solid]:
    return [piece for piece in pieces if piece is not None]


# -- the pelvis ---------------------------------------------------------------


def build_pelvis(placed: dict[str, np.ndarray]) -> list[list[Solid]]:
    """The bucket of the pelvis, with its front corner chipped off.

    The rim of the bucket is the rim of the hip bones: through the two iliac
    crests, which is where it rises highest, and the ASIS and PSIS, which is
    where it comes round the front and the back.  The bottom is the pelvic
    outlet: the ring through the pubic symphysis, the coccyx and the two
    sitting bones.  That ring is far narrower than the rim -- the sitting
    bones are a hand's width apart, the crests three -- which is what tapers
    the bucket.  The sitting bones are buried on most models, so they are
    asked for but not waited for: unless they are placed, they are put half
    the width of the hip points apart, a little below the line from the
    pubic symphysis to the coccyx, which is where they are.  The trochanters
    are left out on purpose: they are the widest point of the hips, but they
    are the femur's, not the pelvis's, and a bucket dropped to them flares
    instead of tapering.

    Then the chip.  The front of the pelvis is not the front of the bucket:
    from the two ASIS the bone falls away back to the pubic symphysis, and
    that plane -- through those three points exactly -- is what the corner
    is knocked off along.  It is the plane a sculptor reads the tilt of the
    pelvis from, so it comes out of the landmarks rather than being guessed.
    """
    marks = Placed(placed)
    centre = marks.at("pubic_symphysis", "sacrum_top", "coccyx")
    crest, asis, psis = (marks.pair(key) for key in ("iliac_crest", "asis", "psis"))
    if any(found is None for found in (centre, crest, asis, psis)):
        return [[]]
    pubic, _sacrum, coccyx = centre

    top_anchors = [*crest, *asis, *psis]
    seat = _mid(pubic, coccyx)
    top_origin, top_normal = fit_plane(top_anchors, _mid(*top_anchors) - seat)
    up = top_normal
    right = _across(crest[1] - crest[0], up)

    ischial = marks.pair("ischial_tuberosity")
    if ischial is None:
        width = float(np.linalg.norm(asis[1] - asis[0]))
        seat = seat - up * OUTLET_DROP * width
        ischial = (
            seat - right * OUTLET_HALF_WIDTH * width,
            seat + right * OUTLET_HALF_WIDTH * width,
        )
    bottom_anchors = [pubic, coccyx, *ischial]
    bottom_origin, bottom_normal = fit_plane(bottom_anchors, up)
    rim = ring_through(top_anchors, top_origin, top_normal, right)
    base = ring_through(bottom_anchors, bottom_origin, bottom_normal, right)
    try:
        bucket = loft([rim, base])
    except DegenerateHullError:
        return [[]]
    inside = _mid(top_origin, bottom_origin)
    normal, offset = plane_through(asis[0], asis[1], pubic, inside)
    return [_solids(bucket.cut(normal, offset) or bucket)]


# -- the ribcage --------------------------------------------------------------

#: The paired landmarks along the costal margin between the xiphoid and the
#: lowest rib, any of which may be missing.  The order here is the order
#: they are asked for; the builder sorts them round the axis anyway.
ARCH_KEYS = ("rectus_origin", "arch_rectus_edge")


def build_ribcage(placed: dict[str, np.ndarray]) -> list[list[Solid]]:
    """The egg of the ribcage, with the arch chipped out of the front of it.

    Three rings pin the egg down.  The top is the thoracic inlet, between C7
    and the jugular notch, tilted steeply forward and down as the real one is;
    its width is taken as a share of the widest ring, since nothing on the
    surface marks it.  The widest ring passes through the two points the
    artist found at the sides, through the breastbone at that height, and
    through the apex of the thoracic curve at the back -- and through the
    back corners of the ribcage under the shoulder blades, when they are
    given, since a ribcage is broader behind than in front -- and through
    the front corners, where the cartilages turn back from the breastbone,
    when those are given, since the front of a ribcage is flatter than an
    ellipse.  The bottom ring is the costal margin itself: T12, the lowest
    rib at each side, whatever was placed along the arch, and the xiphoid,
    rising from the back to the front as the margin does.  So the surface
    of the egg passes through every point of the arch before the arch is
    chipped out along them, and the chip lands on the landmarks rather than
    wherever a plane happens to meet an egg built without them.  The egg is
    lofted through the three rings with a parabola, so it bulges between
    rather than running straight from one to the next.

    The spine is read as the curve through C7, the apex and T12 rather than
    the line from one end to the other, which is where the back of the egg
    gets its arch: the thoracic spine bows backward between the shoulder
    blades, and the ribs hang from it, so the back of the ribcage is furthest
    back at the apex and comes forward again above and below it.

    The thoracic arch is the two costal margins meeting at the xiphoid, and
    the egg is chipped along each of them.  A margin is not a straight line:
    from the xiphoid it drops steeply past the corners of the rectus
    abdominis, runs out along the ninth rib to where the outer edge of the
    rectus crosses it, and turns the corner at the tenth -- a curve that bows
    in under the ribcage, which no single plane can follow and no one convex
    solid can hold, since the clay above it is concave there.  So each half
    of the egg is split into sectors about the ribcage's axis, one per
    segment of the margin, and each sector is cut along its own segment:
    the plane through the segment's two points and the axis at their
    height, a shelf under the arch.
    The union of the sectors has the margin as its lower edge, point by
    point, and the sectors meet along planes through the axis where nothing
    shows.  The segments run round to T12 at the back, so the lower border
    behind the arch is a segment too.  The margin points are sorted round
    the axis before any of that, so the order they were clicked in does not
    matter, and however many of them are down the same rule holds.
    """
    marks = Placed(placed)
    centre = marks.at("jugular_notch", "xiphoid", "c7", "t12", "thoracic_apex")
    widest, lowest = marks.pair("widest_rib"), marks.pair("lowest_rib")
    if centre is None or widest is None or lowest is None:
        return [[]]
    jugular, xiphoid, c7, t12, apex = centre
    angle = marks.maybe("sternal_angle")
    rib_angle, front_corner = marks.pair("rib_angle"), marks.pair("front_corner")
    arch = [pair for pair in (marks.pair(key) for key in ARCH_KEYS) if pair is not None]

    top_origin = _mid(c7, jugular)
    bottom_origin = _mid(t12, *lowest)
    up = _unit(top_origin - bottom_origin)
    right = _across(widest[1] - widest[0], up)
    half_width = 0.5 * float(np.linalg.norm(widest[1] - widest[0]))

    # The breastbone and the spine, as lines to read a front and a back point
    # off at any height.
    sternum = [jugular, *([angle] if angle is not None else []), xiphoid]
    spine = [c7, apex, t12]

    def along(line: list[np.ndarray], level: float) -> np.ndarray:
        """The point of a polyline at a height along the axis, run on past its ends."""
        heights = [float(p @ up) for p in line]
        for a, b, ha, hb in zip(line[:-1], line[1:], heights[:-1], heights[1:], strict=True):
            last = b is line[-1]
            if (min(ha, hb) <= level <= max(ha, hb)) or last or level > max(ha, hb):
                share = 0.0 if abs(ha - hb) < 1e-12 else (level - ha) / (hb - ha)
                return a + (b - a) * share
        return line[-1]  # pragma: no cover - the loop always returns

    top_normal = _unit(np.cross(right, jugular - c7))
    if float(top_normal @ up) < 0.0:
        top_normal = -top_normal
    inlet = ring_through(
        [
            c7,
            jugular,
            top_origin + right * INLET_WIDTH * half_width,
            top_origin - right * INLET_WIDTH * half_width,
        ],
        top_origin,
        top_normal,
        right,
    )

    wide_level = float(_mid(*widest) @ up)
    wide_anchors = [*widest, along(sternum, wide_level), along(spine, wide_level)]
    wide_origin = _mid(*wide_anchors)
    wide = ring_through(
        [*wide_anchors, *(rib_angle or ()), *(front_corner or ())], wide_origin, up, right
    )

    # The bottom ring is the margin: it climbs from T12 at the back to the
    # xiphoid at the front, and the ring's height field carries that.
    margin_anchors = [t12, *lowest, *(point for pair in arch for point in pair), xiphoid]
    bottom_origin, bottom_normal = fit_plane(margin_anchors, up)
    bottom_level = float(bottom_origin @ up)
    base = ring_through(margin_anchors, bottom_origin, bottom_normal, right)

    levels = [bottom_level, wide_level, float(top_origin @ up)]
    if not levels[0] < levels[1] < levels[2]:
        return [[]]
    try:
        egg = loft(blend_rings([base, wide, inlet], levels, LOFT_LEVELS))
    except DegenerateHullError:
        return [[]]
    # Each half is cut at the median plane first, so the two meet along the
    # midline rather than lying over each other -- two copies of one surface
    # drawn in the same place would flicker against each other -- and then
    # split into sectors about the axis, one per segment of its margin.
    front = _across(xiphoid - t12, up)
    scale = float(np.linalg.norm(widest[1] - widest[0]))

    def around(point: np.ndarray, sign: float) -> float:
        """Angle about the axis, from the front round to the back on one side."""
        flat = point - top_origin
        flat = flat - float(flat @ up) * up
        # Held to this side of the median plane, so a midline point a hair
        # over it -- T12, say -- still reads as the back, not as minus the
        # back.  Written out because ``max(-0.0, 0.0)`` is ``-0.0``, and
        # ``arctan2`` reads the sign of a zero.
        sideways = sign * float(flat @ right)
        if sideways <= 0.0:
            sideways = 0.0
        return float(np.arctan2(sideways, float(flat @ front)))

    pieces = []
    for index, sign in ((0, -1.0), (1, 1.0)):
        half = egg.cut(-sign * right, float(-sign * right @ top_origin))
        if half is None:
            continue
        margin = sorted(
            [xiphoid, *(pair[index] for pair in arch), lowest[index], t12],
            key=lambda point: around(point, sign),
        )
        for a, b in zip(margin[:-1], margin[1:], strict=True):
            sector = half
            for own, other in ((a, b), (b, a)):
                wall = np.cross(up, own - top_origin)
                if float(np.linalg.norm(wall)) < 1e-6 * scale:
                    continue  # on the axis: no wall to raise there
                wall = _unit(wall)
                if float(wall @ (other - top_origin)) > 0.0:
                    wall = -wall
                sector = sector.cut(wall, float(wall @ top_origin)) if sector is not None else None
            if sector is None:
                continue
            level = 0.5 * float((a + b) @ up)
            hinge = top_origin + up * (level - float(top_origin @ up))
            normal, offset = plane_through(a, b, hinge, top_origin)
            if float(np.linalg.norm(normal)) > 0.0:
                sector = sector.cut(normal, offset)
            if sector is not None:
                pieces.append(sector)
    if not pieces:
        return [[egg]]
    return [pieces]


# -- the head -----------------------------------------------------------------


@dataclass(frozen=True)
class _HeadFrame:
    right: np.ndarray
    up: np.ndarray
    forward: np.ndarray
    #: The point on the median plane every width is measured from.
    middle: np.ndarray

    def half_width(self, point) -> float:
        return abs(float((np.asarray(point, dtype=np.float64) - self.middle) @ self.right))


def _head_frame(marks: Placed) -> tuple[_HeadFrame, tuple[np.ndarray, ...]] | None:
    profile = marks.at("vertex", "glabella", "menton", "occiput", "inion")
    if profile is None:
        return None
    vertex, glabella, menton, occiput, inion = profile
    up = _unit(vertex - menton)
    forward = _across(glabella - occiput, up)
    right = np.cross(up, forward)
    # The paired landmarks say which way is the figure's right; without them
    # the wedge is symmetric and either will do.
    parietal = marks.pair("parietal")
    if parietal is not None and float((parietal[1] - parietal[0]) @ right) < 0.0:
        right = -right
    middle = _mid(*profile)
    return _HeadFrame(right, up, forward, middle), profile


def build_head(placed: dict[str, np.ndarray]) -> list[list[Solid]]:
    """The head, in five stages of clay.

    *The wedge.*  The profile of the head -- crown, brow, chin, the back of
    the skull, the nape, and the corner where the crown turns down into the
    back -- as a thin plate no wider than the bridge of the nose.  It is the
    side view, standing up, and it is where a head is read from.

    *The width.*  The plate is widened above and below the eyes, and not
    between them.  Above: the cranium, out to the parietal eminences, the
    corners of the brow and the ear holes, narrowing to the crown and the
    nape by the ratios above.  Below: the jaw, out to the cheekbones, the
    ear holes and the corners of the jaw, tapering to the chin.  Two blocks,
    and the eye sockets are the gap left between them -- which is the point
    of building this way round.  One hull from the crown to the chin would
    fill the sockets, and clay laid on cannot be dug out again.

    *The cranium.*  The block of the skull planed out to the rest of what
    can be found on it: the bulges of the forehead, the corners of the crown
    where its top turns down into its sides, the corners at the back where
    it turns down into the occiput, and the mastoids at its base behind the
    ears.  A hull through all of that and the width stage's points, so it is
    planes meeting at edges like every other form here, not a ball -- and
    its lower front edge is still the brow line, so the sockets stay open
    under it.

    *The jaw and muzzle.*  The mass of the lower face, hung from the ear
    holes: the cheeks under the eyes, the base of the nose, the jaw and the
    chin as one lump, its top no higher than the lower rims of the sockets.
    Where the primary forms stop.

    *The nose.*  The first of the secondary forms, and the one a head cannot
    be read without: a wedge from the root of the nose between the eyes out
    to the tip, spread to the wings at its base and back to the lip under
    it.  Laid on the muzzle; the sockets either side of its root stay open.
    """
    marks = Placed(placed)
    found = _head_frame(marks)
    if found is None:
        return [[]]
    frame, profile = found
    vertex, glabella, menton, occiput, inion = profile
    height = float(np.linalg.norm(vertex - menton))
    thin = WEDGE_HALF_WIDTH * height
    stages: list[list[Solid]] = []

    def hull(*points) -> Solid | None:
        try:
            return Solid.from_points(np.stack([np.asarray(p, dtype=np.float64) for p in points]))
        except DegenerateHullError:
            return None

    def spread(point: np.ndarray, width: float) -> tuple[np.ndarray, np.ndarray]:
        """A midline point pushed out to either side."""
        return point + frame.right * width, point - frame.right * width

    lambda_ = marks.maybe("lambda")
    outline = [*profile, *([lambda_] if lambda_ is not None else [])]
    wedge = hull(*(side for point in outline for side in spread(point, thin)))
    stages.append(_solids(wedge))

    pairs = [
        marks.pair(key) for key in ("parietal", "brow_corner", "zygomatic", "gonion", "tragus")
    ]
    if any(pair is None for pair in pairs):
        return stages
    parietal, brow, zygomatic, gonion, tragus = pairs
    skull = max(frame.half_width(p) for p in parietal)
    jaw = max(frame.half_width(p) for p in gonion)
    crown = spread(vertex, max(CROWN_WIDTH * skull, thin))
    back = spread(occiput, max(OCCIPUT_WIDTH * skull, thin))
    corner = spread(lambda_, max(LAMBDA_WIDTH * skull, thin)) if lambda_ is not None else ()
    nape = spread(inion, max(NAPE_WIDTH * skull, thin))
    chin = spread(menton, max(CHIN_WIDTH * jaw, thin))
    cranium = hull(
        *crown, *spread(glabella, thin), *brow, *back, *corner, *nape, *parietal, *tragus
    )
    jaw_block = hull(*zygomatic, *tragus, *gonion, menton, *chin)
    stages.append(_solids(cranium, jaw_block))

    frontal, back_corner, mastoid = (
        marks.pair(key) for key in ("frontal_eminence", "back_corner", "mastoid")
    )
    if frontal is None or back_corner is None or mastoid is None:
        return stages
    crown_corner = marks.pair("crown_corner") or ()
    skull_block = hull(
        *crown,
        *crown_corner,
        *frontal,
        *spread(glabella, thin),
        *brow,
        *parietal,
        *tragus,
        *mastoid,
        *back_corner,
        *back,
        *corner,
        *nape,
    )
    stages.append(_solids(skull_block))

    infraorbital, subnasale = marks.pair("infraorbital"), marks.maybe("subnasale")
    if infraorbital is None or subnasale is None:
        return stages
    pogonion = marks.maybe("pogonion")
    muzzle = hull(
        *zygomatic,
        *infraorbital,
        *gonion,
        *tragus,
        subnasale,
        menton,
        *chin,
        *([pogonion] if pogonion is not None else []),
    )
    stages.append(_solids(muzzle))

    nose = marks.at("nasion", "pronasale")
    alare = marks.pair("alare")
    if nose is None or alare is None:
        return stages
    nasion, pronasale = nose
    stages.append(_solids(hull(nasion, pronasale, subnasale, *alare)))
    return stages
