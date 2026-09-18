"""The forms: convex solids, the landmarks that build them, the walk, and the freeform."""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.armature import PlacedLandmark
from refview.core.convex import DegenerateHullError, Solid, convex_hull, merged, rounded_hull
from refview.core.form_shapes import (
    blend_rings,
    build_head,
    build_pelvis,
    build_ribcage,
    fit_plane,
    plane_through,
    ring_through,
)
from refview.core.forms import (
    FORM_PRESETS,
    FREEFORM,
    HEAD,
    PELVIS,
    RIBCAGE,
    FormFill,
    FormSettings,
    FormStore,
    PrimaryForm,
    build_form,
    built_count,
    form_landmark_title,
    form_mesh,
    form_spec,
    freeform_landmark,
    landmark_key,
    landmark_signature,
    median_plane_ready,
    mirror_form_landmarks,
    paired_landmarks,
    shown_stages,
    stages_mesh,
    symmetrised_points,
    twin_key,
)
from refview.core.landmarks import Side
from refview.core.session import Session
from refview.ui.form_tool import FormTool

# A standing figure with +Y up, +Z forward and +X out to the figure's left.
# Every paired landmark is written for the left side and mirrored in ``_marks``.


def _marks(centre: dict, left: dict, scale: float = 1.0) -> dict[str, np.ndarray]:
    placed = {key: np.array(at, dtype=np.float64) for key, at in centre.items()}
    for key, at in left.items():
        point = np.array(at, dtype=np.float64)
        placed[f"{key}.L"] = point
        placed[f"{key}.R"] = point * np.array([-1.0, 1.0, 1.0])
    return {key: at * scale for key, at in placed.items()}


PELVIS_MARKS = _marks(
    {"pubic_symphysis": (0, 90, 6), "sacrum_top": (0, 104, -10), "coccyx": (0, 92, -8)},
    {
        "iliac_crest": (14, 108, -2),
        "asis": (11, 102, 7),
        "psis": (5, 103, -9),
        "ischial_tuberosity": (6, 86, -6),
    },
)

#: Where the trochanter would be on that figure: the widest point of the hips,
#: and no part of the pelvis.
TROCHANTER = np.array([17.0, 94.0, -1.0])

RIBCAGE_MARKS = _marks(
    {
        "jugular_notch": (0, 148, 6),
        "xiphoid": (0, 128, 9),
        "c7": (0, 152, -7),
        "t12": (0, 118, -8),
        "thoracic_apex": (0, 132, -10),
        "sternal_angle": (0, 143, 9),
    },
    {
        "widest_rib": (15, 130, 0),
        "rib_angle": (10, 130, -8),
        "front_corner": (10, 130, 5),
        "rectus_origin": (3, 125, 8.5),
        "arch_rectus_edge": (8, 122, 6.5),
        "lowest_rib": (12, 121, 4),
    },
)

#: Sectors the ribcage is built in: one per segment of each margin, which
#: runs xiphoid, two arch points, lowest rib, T12.
RIBCAGE_SECTORS = 2 * 4

HEAD_MARKS = _marks(
    {
        "vertex": (0, 183, -1),
        "glabella": (0, 172, 9),
        "menton": (0, 160, 6),
        "occiput": (0, 175, -10),
        "inion": (0, 168, -8),
        "subnasale": (0, 166, 9),
        "pogonion": (0, 161, 8),
        "lambda": (0, 180, -7),
        "nasion": (0, 170.5, 8.2),
        "pronasale": (0, 167.5, 11.5),
    },
    {
        "parietal": (7.5, 175, -3),
        "tragus": (7, 171, -2),
        "brow_corner": (4.5, 172, 6),
        "zygomatic": (6.5, 170, 5),
        "gonion": (5, 163, -1),
        "frontal_eminence": (3.5, 177.5, 7),
        "back_corner": (6.5, 178, -7.5),
        "mastoid": (6, 166, -4),
        "crown_corner": (5.5, 181, -2),
        "infraorbital": (3.5, 169, 7.5),
        "alare": (1.7, 166.3, 9.2),
    },
)

#: The middle of each eye socket on that figure: below the brow, above the
#: cheekbone, out from the bridge of the nose.  Nothing should ever be there.
ORBITS = (np.array([3.2, 170.5, 6.0]), np.array([-3.2, 170.5, 6.0]))


def _inside(pieces, point) -> bool:
    return any(piece.contains(point) for piece in pieces)


def _closed(solid: Solid) -> bool:
    """Every edge shared by exactly two faces: the hull is a closed surface."""
    edges = np.sort(
        np.concatenate([solid.faces[:, [0, 1]], solid.faces[:, [1, 2]], solid.faces[:, [2, 0]]]),
        axis=1,
    )
    _, counts = np.unique(edges, axis=0, return_counts=True)
    return bool(np.all(counts == 2))


# -- convex solids -----------------------------------------------------------


def test_the_hull_of_a_cube_is_the_cube():
    rng = np.random.default_rng(1)
    corners = np.array([[a, b, c] for a in (0, 1) for b in (0, 1) for c in (0, 1)], dtype=float)
    inside = rng.random((100, 3)) * 0.8 + 0.1
    solid = Solid.from_points(np.concatenate([corners, inside]))
    assert solid.volume() == pytest.approx(1.0)
    assert _closed(solid)
    assert solid.contains([0.5, 0.5, 0.5])
    assert not solid.contains([1.1, 0.5, 0.5])
    # The faces wind outward: every normal points away from the centre.
    normals, offsets = solid.planes
    assert np.all(normals @ np.full(3, 0.5) < offsets)


def test_points_on_a_face_plane_extend_the_face_rather_than_folding_it():
    rng = np.random.default_rng(2)
    corners = np.array([[a, b, c] for a in (0, 1) for b in (0, 1) for c in (0, 1)], dtype=float)
    on_top = np.column_stack([rng.random(40), rng.random(40), np.ones(40)])
    solid = Solid.from_points(np.concatenate([corners, on_top]))
    assert solid.volume() == pytest.approx(1.0)
    assert _closed(solid)


def test_a_flat_or_tiny_cloud_is_refused():
    with pytest.raises(DegenerateHullError):
        convex_hull([[0, 0, 0], [1, 0, 0], [0, 1, 0]])
    with pytest.raises(DegenerateHullError):
        convex_hull([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0.5, 0.5, 0]])


def test_a_cut_keeps_the_named_side_and_its_share_of_the_volume():
    rng = np.random.default_rng(3)
    around = rng.random(400) * 2.0 * np.pi
    z = rng.random(400) * 2.0 - 1.0
    flat = np.sqrt(1.0 - z * z)
    ball = Solid.from_points(np.column_stack([flat * np.cos(around), flat * np.sin(around), z]))
    half = ball.cut([0.0, 0.0, 1.0], 0.0)
    assert half is not None
    assert half.volume() == pytest.approx(ball.volume() / 2.0, rel=0.02)
    assert half.contains([0.0, 0.0, -0.5]) and not half.contains([0.0, 0.0, 0.5])
    assert ball.cut([0.0, 0.0, 1.0], -2.0) is None  # the plane took everything


def test_a_solid_meshes_flat_and_merges_with_others():
    corners = np.array([[a, b, c] for a in (0, 1) for b in (0, 1) for c in (0, 1)], dtype=float)
    solid = Solid.from_points(corners)
    mesh = solid.mesh("cube")
    assert mesh.triangle_count == len(solid.faces)
    assert mesh.vertex_count == 3 * len(solid.faces)  # no corner is shared
    both = merged([mesh, Solid.from_points(corners + 5.0).mesh()])
    assert both is not None
    assert both.triangle_count == 2 * mesh.triangle_count
    assert int(both.indices.max()) == both.vertex_count - 1
    assert merged([]) is None


# -- rings and lofts ---------------------------------------------------------


def test_a_ring_through_four_axis_points_is_very_nearly_an_ellipse():
    ring = ring_through(
        [[3, 0, 0], [-3, 0, 0], [0, 0, 1], [0, 0, -1]],
        origin=[0, 0, 0],
        normal=[0, 1, 0],
        across=[1, 0, 0],
        samples=36,
    )
    points = ring.points
    # Every sample sits close to x²/9 + z² = 1, and the axis points exactly on it.
    assert np.allclose(points[:, 0] ** 2 / 9.0 + points[:, 2] ** 2, 1.0, atol=0.05)
    assert np.allclose(points[0], [3, 0, 0]) and np.allclose(np.abs(points[9]), [0, 0, 1])
    assert np.allclose(points[:, 1], 0.0)


def test_a_ring_passes_through_its_anchors_heights_included():
    anchors = np.array([[2, 0.5, 0], [-2, 0.5, 0], [0, -0.5, 1.5], [0, 0, -1.5]], dtype=float)
    ring = ring_through(anchors, [0, 0, 0], [0, 1, 0], [1, 0, 0], samples=360)
    for anchor in anchors:
        assert np.min(np.linalg.norm(ring.points - anchor, axis=1)) < 0.05


def test_blending_three_rings_bulges_where_the_middle_one_is_widest():
    def circle(radius, height):
        return ring_through(
            [[radius, height, 0], [-radius, height, 0], [0, height, radius], [0, height, -radius]],
            [0, height, 0],
            [0, 1, 0],
            [1, 0, 0],
        )

    rings = blend_rings([circle(1.0, 0.0), circle(3.0, 1.0), circle(1.0, 3.0)], [0, 1, 3], 7)
    radii = [float(ring.radius.mean()) for ring in rings]
    assert radii[0] == pytest.approx(1.0) and radii[-1] == pytest.approx(1.0)
    assert max(radii) > 2.5


def test_planes_are_fitted_and_oriented():
    origin, normal = fit_plane([[0, 1, 0], [1, 1, 0], [0, 1, 1], [1, 1, 1]], toward=[0, -1, 0])
    assert np.allclose(origin, [0.5, 1, 0.5])
    assert np.allclose(normal, [0, -1, 0])
    normal, offset = plane_through([0, 0, 0], [1, 0, 0], [0, 1, 0], inside=[0, 0, -2])
    assert np.allclose(normal, [0, 0, 1]) and offset == pytest.approx(0.0)


# -- the pelvis ---------------------------------------------------------------


def test_the_pelvis_is_one_bucket_that_holds_its_landmarks():
    stages = build_pelvis(PELVIS_MARKS)
    assert len(stages) == 1 and len(stages[0]) == 1
    bucket = stages[0][0]
    assert _closed(bucket)
    slack = 0.5
    for key in ("iliac_crest.L", "psis.R", "ischial_tuberosity.L", "pubic_symphysis", "coccyx"):
        assert bucket.contains(PELVIS_MARKS[key], slack=slack), key
    assert bucket.contains([0.0, 98.0, -2.0])


def test_the_bucket_tapers_from_the_crests_to_the_sitting_bones():
    bucket = build_pelvis(PELVIS_MARKS)[0][0]
    # The rim is as wide as the crests; the bottom is as wide as the sitting
    # bones and no wider, so the trochanter -- the widest point of the hips,
    # but the femur's -- lies outside the clay.
    rim = bucket.vertices[bucket.vertices[:, 1] > 100.0]
    base = bucket.vertices[bucket.vertices[:, 1] < 92.0]
    assert np.abs(rim[:, 0]).max() == pytest.approx(14.0, abs=1.0)
    assert np.abs(base[:, 0]).max() < 8.0
    assert not bucket.contains(TROCHANTER, slack=1.0)
    assert not bucket.contains(TROCHANTER * np.array([-1.0, 1.0, 1.0]), slack=1.0)


def test_the_front_of_the_pelvis_is_chipped_off_along_the_asis_to_pubis_plane():
    bucket = build_pelvis(PELVIS_MARKS)[0][0]
    # The plane through the two ASIS and the pubic symphysis, with the bucket
    # behind it: nothing of the bucket lies in front of it.
    normal, offset = plane_through(
        PELVIS_MARKS["asis.L"],
        PELVIS_MARKS["asis.R"],
        PELVIS_MARKS["pubic_symphysis"],
        inside=[0.0, 98.0, -2.0],
    )
    assert np.all(bucket.vertices @ normal <= offset + 1e-6)
    # ... but the plane is a face of it, not a cut clean past it.
    assert np.any(bucket.vertices @ normal > offset - 0.5)
    # Whereas a bucket of the same rings without the chip would reach further.
    assert not bucket.contains([0.0, 100.0, 9.0])


def test_the_pelvis_needs_every_required_landmark():
    missing = dict(PELVIS_MARKS)
    del missing["asis.R"]
    assert build_pelvis(missing) == [[]]
    without_sitting_bones = {k: v for k, v in PELVIS_MARKS.items() if "ischial" not in k}
    assert len(build_pelvis(without_sitting_bones)[0]) == 1


def test_the_sitting_bones_are_guessed_from_the_hip_points_when_not_placed():
    without = {k: v for k, v in PELVIS_MARKS.items() if "ischial" not in k}
    guessed = build_pelvis(without)[0][0]
    placed = build_pelvis(PELVIS_MARKS)[0][0]
    # The guess puts the sitting bones half the ASIS width apart, a little
    # under the line from the pubic symphysis to the coccyx: near where this
    # figure's really are, so the two buckets are much the same size, and
    # the guessed one still tapers and still leaves the trochanter out.
    assert guessed.volume() == pytest.approx(placed.volume(), rel=0.25)
    base = guessed.vertices[guessed.vertices[:, 1] < 92.0]
    assert 4.0 < np.abs(base[:, 0]).max() < 8.0
    assert not guessed.contains(TROCHANTER, slack=1.0)
    # Placed sitting bones are used exactly.
    assert placed.contains(PELVIS_MARKS["ischial_tuberosity.L"], slack=0.5)


def test_the_pelvis_scales_with_the_figure():
    small = build_pelvis(_marks({}, {}) | PELVIS_MARKS)[0][0]
    large = build_pelvis({k: v * 2.0 for k, v in PELVIS_MARKS.items()})[0][0]
    assert large.volume() == pytest.approx(8.0 * small.volume(), rel=1e-6)


# -- the ribcage --------------------------------------------------------------


def test_the_ribcage_is_two_halves_meeting_at_the_midline():
    stages = build_ribcage(RIBCAGE_MARKS)
    assert len(stages) == 1 and len(stages[0]) == RIBCAGE_SECTORS
    pieces = stages[0]
    assert all(_closed(piece) for piece in pieces)
    left = [p for p in pieces if p.vertices[:, 0].mean() > 0.0]
    right = [p for p in pieces if p.vertices[:, 0].mean() < 0.0]
    assert len(left) == len(right) == RIBCAGE_SECTORS // 2
    assert all(p.vertices[:, 0].min() >= -1e-6 for p in left)
    assert all(p.vertices[:, 0].max() <= 1e-6 for p in right)
    assert sum(p.volume() for p in left) == pytest.approx(sum(p.volume() for p in right), rel=1e-6)


def test_the_arch_follows_the_costal_margin_point_by_point():
    pieces = build_ribcage(RIBCAGE_MARKS)[0]
    # Every margin point is on the clay's lower edge: on it (or a hair in),
    # and nothing a little below it.
    for key in ("xiphoid", "rectus_origin.L", "arch_rectus_edge.R", "lowest_rib.L"):
        at = RIBCAGE_MARKS[key]
        assert any(p.contains(at, slack=0.6) for p in pieces), key
        assert not _inside(pieces, at - np.array([0.0, 1.5, 0.0])), key
    # The arch curves in under the ribcage: the straight line from the
    # xiphoid to the lowest rib passes above the margin's middle points, so
    # the clay reaches below that line there.
    xiphoid, lowest = RIBCAGE_MARKS["xiphoid"], RIBCAGE_MARKS["lowest_rib.L"]
    edge = RIBCAGE_MARKS["arch_rectus_edge.L"]
    share = edge[0] / lowest[0]
    on_line = xiphoid + share * (lowest - xiphoid)
    assert edge[1] < on_line[1] - 1.0
    assert _inside(pieces, on_line - np.array([0.0, 0.6, 0.0]))
    # With no arch points at all the old single plane comes back, and the
    # clay stops at that line.
    plain = {k: v for k, v in RIBCAGE_MARKS.items() if not k.startswith(("rectus", "arch"))}
    pieces = build_ribcage(plain)[0]
    assert len(pieces) == 4
    assert not _inside(pieces, on_line - np.array([0.0, 0.6, 0.0]))


def test_the_egg_passes_through_the_arch_before_it_is_chipped():
    """An arch point well inside the egg an old build would have made is on
    the surface of this one: the margin is the bottom ring, not a cut."""
    marks = dict(RIBCAGE_MARKS)
    # Push the arch points forward of where the egg would otherwise run.
    for key in ("rectus_origin", "arch_rectus_edge"):
        for side in "LR":
            marks[f"{key}.{side}"] = marks[f"{key}.{side}"] + np.array([0.0, 0.0, 3.0])
    pieces = build_ribcage(marks)[0]
    for key in ("rectus_origin.L", "arch_rectus_edge.R"):
        at = marks[key]
        assert any(p.contains(at, slack=0.6) for p in pieces), key
        # On the surface: a little further forward is outside ...
        assert not _inside(pieces, at + np.array([0.0, 0.0, 1.0])), key
        # ... and a little below is outside too, since it is the lower edge.
        assert not _inside(pieces, at - np.array([0.0, 1.5, 0.0])), key


def test_the_front_corners_flatten_the_front_of_the_egg():
    wide = build_ribcage(RIBCAGE_MARKS)[0]
    without = build_ribcage({k: v for k, v in RIBCAGE_MARKS.items() if "front_corner" not in k})[0]
    # The corner is placed inside the ellipse the other anchors imply, so
    # the egg with it is flatter across the front at that height.
    probe = np.array([10.0, 130.0, 5.6])
    assert _inside(without, probe)
    assert not _inside(wide, probe)


def test_the_arch_is_chipped_out_of_the_front_of_the_ribcage():
    pieces = build_ribcage(RIBCAGE_MARKS)[0]
    assert not _inside(pieces, [0.3, 122.0, 6.0])  # under the arch, front midline
    assert _inside(pieces, [0.3, 121.0, -6.0])  # the back, at the same height
    assert _inside(pieces, [11.0, 121.0, 2.0])  # the side, at the lowest rib
    assert _inside(pieces, [0.3, 135.0, 0.0])  # the middle of the egg
    for key in ("widest_rib.L", "c7", "jugular_notch", "t12", "lowest_rib.R", "xiphoid"):
        assert _inside([p for p in pieces], RIBCAGE_MARKS[key]) or any(
            p.contains(RIBCAGE_MARKS[key], slack=0.75) for p in pieces
        ), key


def test_the_ribcage_bulges_between_its_rings():
    pieces = build_ribcage(RIBCAGE_MARKS)[0]
    # Half way between the widest ring and the inlet a straight loft would be
    # narrower than a parabolic one; the egg keeps most of its width there.
    assert _inside(pieces, [13.0, 141.0, 0.0])


def test_the_back_of_the_ribcage_arches_at_the_apex_of_the_thoracic_curve():
    pieces = build_ribcage(RIBCAGE_MARKS)[0]
    # The line from C7 to T12 passes 7.4 behind the midline at the widest
    # level; the apex is placed 10 behind, and the egg reaches it.  Probed a
    # hair off the midline, which is where the two halves meet.
    assert _inside(pieces, [0.3, 132.0, -9.3])
    assert _inside(pieces, [-0.3, 132.0, -9.3])
    assert _inside(pieces, RIBCAGE_MARKS["thoracic_apex"]) or any(
        p.contains(RIBCAGE_MARKS["thoracic_apex"], slack=0.5) for p in pieces
    )
    # Above and below the apex the back comes forward again: the egg is
    # furthest back at the apex.
    back = {}
    for level in (124.0, 132.0, 146.0):
        rows = np.concatenate([p.vertices for p in pieces])
        near = rows[np.abs(rows[:, 1] - level) < 1.5]
        back[level] = near[:, 2].min()
    assert back[132.0] < back[124.0] and back[132.0] < back[146.0]
    # Without the apex there is no ribcage; without the back corners there is.
    assert build_ribcage({k: v for k, v in RIBCAGE_MARKS.items() if k != "thoracic_apex"}) == [[]]
    narrow = {k: v for k, v in RIBCAGE_MARKS.items() if not k.startswith("rib_angle")}
    assert len(build_ribcage(narrow)[0]) == RIBCAGE_SECTORS
    # The back corners broaden the back of the widest ring.
    assert _inside(pieces, [10.0, 130.0, -7.8])
    assert not _inside(build_ribcage(narrow)[0], [10.0, 130.0, -7.8])


def test_the_ribcage_refuses_rings_out_of_order():
    upside_down = dict(RIBCAGE_MARKS)
    upside_down["widest_rib.L"] = np.array([15.0, 160.0, 0.0])
    upside_down["widest_rib.R"] = np.array([-15.0, 160.0, 0.0])
    assert build_ribcage(upside_down) == [[]]


# -- the head -----------------------------------------------------------------


def test_the_head_arrives_in_five_stages_each_laid_over_the_last():
    stages = build_head(HEAD_MARKS)
    assert len(stages) == 5
    assert [len(pieces) for pieces in stages] == [1, 2, 1, 1, 1]
    wedge = stages[0][0]
    cranium, jaw_block = stages[1]
    skull = stages[2][0]
    muzzle = stages[3][0]
    nose = stages[4][0]
    for piece in (wedge, cranium, jaw_block, skull, muzzle, nose):
        assert _closed(piece)
    # The wedge carries the corner of the back of the crown.
    assert wedge.contains(HEAD_MARKS["lambda"], slack=0.1)
    # The wedge is no wider than the bridge of the nose; the cranium block is
    # as wide as the skull.
    assert wedge.vertices[:, 0].max() < 1.5
    assert cranium.vertices[:, 0].max() == pytest.approx(7.5)
    # Each stage adds.  The cheekbone is in the jaw block but not the wedge;
    # the brow corner and the ear hole are in the cranium block.
    assert not wedge.contains(HEAD_MARKS["zygomatic.L"], slack=0.1)
    assert jaw_block.contains(HEAD_MARKS["zygomatic.L"], slack=0.1)
    assert cranium.contains(HEAD_MARKS["brow_corner.R"], slack=0.1)
    assert cranium.contains(HEAD_MARKS["tragus.L"], slack=0.1)
    # The skull is planed out to everything found on it, and is planes: a
    # hull of a couple of dozen landmarks, not a sampled ball.
    for key in (
        "vertex",
        "frontal_eminence.L",
        "crown_corner.R",
        "back_corner.L",
        "mastoid.L",
        "occiput",
        "lambda",
    ):
        assert skull.contains(HEAD_MARKS[key], slack=0.1), key
    assert not cranium.contains(HEAD_MARKS["frontal_eminence.L"], slack=0.1)
    assert not cranium.contains(HEAD_MARKS["back_corner.L"], slack=0.1)
    assert len(skull.vertices) <= 30
    assert not skull.contains(HEAD_MARKS["menton"], slack=1.0)
    # The muzzle reaches the jaw angles, the chin and the cheeks under the
    # eyes.
    assert muzzle.contains(HEAD_MARKS["gonion.R"], slack=0.1)
    assert muzzle.contains(HEAD_MARKS["menton"], slack=0.1)
    assert muzzle.contains(HEAD_MARKS["infraorbital.L"], slack=0.1)
    # The nose is a wedge from its root to its tip and out to its wings, and
    # stands proud of the muzzle at the tip.
    for key in ("nasion", "pronasale", "subnasale", "alare.L", "alare.R"):
        assert nose.contains(HEAD_MARKS[key], slack=0.1), key
    assert not muzzle.contains(HEAD_MARKS["pronasale"], slack=0.5)
    assert nose.vertices[:, 0].max() <= 1.7 + 1e-6


def test_the_eye_sockets_stay_empty_at_every_stage():
    """Clay goes on and does not come off, so nothing may ever fill a socket."""
    stages = build_head(HEAD_MARKS)
    for index, pieces in enumerate(stages):
        for orbit in ORBITS:
            assert not _inside(pieces, orbit), (index, orbit)
    # ... and not for want of anything around them: the brow above, the
    # cheek below and the bridge of the nose between are all clay.
    everything = [piece for pieces in stages for piece in pieces]
    assert _inside(everything, [3.2, 172.5, 6.5])  # the brow ridge
    assert _inside(everything, [3.2, 168.5, 6.5])  # the cheek under the eye
    assert _inside(everything, [0.0, 170.5, 8.0])  # the bridge of the nose


def test_the_head_stops_at_the_stage_its_landmarks_reach():
    only_profile = {k: v for k, v in HEAD_MARKS.items() if "." not in k}
    stages = build_head(only_profile)
    assert len(stages) == 1 and len(stages[0]) == 1
    no_ears = {k: v for k, v in HEAD_MARKS.items() if not k.startswith("tragus")}
    assert len(build_head(no_ears)) == 1
    no_mastoids = {k: v for k, v in HEAD_MARKS.items() if not k.startswith("mastoid")}
    assert len(build_head(no_mastoids)) == 2
    no_corners = {k: v for k, v in HEAD_MARKS.items() if not k.startswith("crown_corner")}
    assert len(build_head(no_corners)) == 5
    no_cheeks = {k: v for k, v in HEAD_MARKS.items() if not k.startswith("infraorbital")}
    assert len(build_head(no_cheeks)) == 3
    no_nose = {k: v for k, v in HEAD_MARKS.items() if not k.startswith("alare")}
    assert len(build_head(no_nose)) == 4
    no_lambda = {k: v for k, v in HEAD_MARKS.items() if k != "lambda"}
    assert len(build_head(no_lambda)) == 5  # the corner of the crown is not waited for
    assert build_head({}) == [[]]


def test_the_wedge_is_symmetric_without_any_paired_landmarks():
    only_profile = {k: v for k, v in HEAD_MARKS.items() if "." not in k}
    wedge = build_head(only_profile)[0][0]
    assert wedge.vertices[:, 0].max() == pytest.approx(-wedge.vertices[:, 0].min())


# -- the presets --------------------------------------------------------------


def test_every_preset_lists_its_landmarks_stage_by_stage_and_left_before_right():
    for preset in FORM_PRESETS.values():
        keys = [entry.key for entry in preset.landmarks]
        assert len(keys) == len(set(keys)), preset.key
        for entry in preset.landmarks:
            if entry.mirror_of:
                assert keys.index(entry.mirror_of) == keys.index(entry.key) - 1
                assert preset.stage_of(entry.key) == preset.stage_of(entry.mirror_of)
        # Three midline points at least, so the mirror has a plane to fit.
        assert len(preset.centre_keys()) >= 3
    assert [s.key for s in HEAD.stages] == ["wedge", "width", "cranium", "jaw", "nose"]
    assert len(PELVIS.stages) == 1 and len(RIBCAGE.stages) == 1


def test_a_form_builds_from_its_placed_landmarks_and_shows_the_stage_it_is_set_to():
    form = PrimaryForm(
        preset="head",
        landmarks=[PlacedLandmark(key=k, at=tuple(v)) for k, v in HEAD_MARKS.items()],
    )
    stages = build_form(form)
    assert built_count(stages) == 5
    assert len(shown_stages(form, stages)) == 5
    form.stage = 1
    assert len(shown_stages(form, stages)) == 2
    form.stage = 9
    assert len(shown_stages(form, stages)) == 5
    mesh = form_mesh(form, smooth=40.0)
    assert mesh is not None and mesh.triangle_count > 0
    assert stages_mesh([], 40.0) is None
    assert form_landmark_title(form, "vertex") == "Vertex"
    assert form_landmark_title(form, "parietal.L") == "Parietal eminence (left)"
    assert form_landmark_title(form, "what") == "what"


def test_a_partly_placed_form_builds_what_it_can():
    form = PrimaryForm(
        preset="head",
        landmarks=[
            PlacedLandmark(key=k, at=tuple(v)) for k, v in HEAD_MARKS.items() if "." not in k
        ],
    )
    assert built_count(build_form(form)) == 1
    assert form_mesh(PrimaryForm(preset="pelvis"), 40.0) is None
    assert build_form(PrimaryForm(preset="nothing")) == []


# -- mirroring ----------------------------------------------------------------


def _left_only(marks: dict, preset) -> list[PlacedLandmark]:
    return [
        PlacedLandmark(key=entry.key, at=tuple(marks[entry.key]))
        for entry in preset.landmarks
        if not entry.mirror_of and entry.key in marks
    ]


def test_the_mirror_reflects_the_left_side_across_the_midline():
    form = PrimaryForm(preset="pelvis", landmarks=_left_only(PELVIS_MARKS, PELVIS))
    assert median_plane_ready(form)
    mirrored = mirror_form_landmarks(form)
    keys = {entry.key for entry in mirrored}
    assert "asis.R" in keys and "ischial_tuberosity.R" in keys
    guess = next(entry for entry in mirrored if entry.key == "asis.R")
    assert guess.mirrored
    assert np.allclose(guess.point, PELVIS_MARKS["asis.R"], atol=1e-6)
    # And the bucket built from the mirrored set is the bucket.
    form.landmarks = mirrored
    assert built_count(build_form(form)) == 1


def test_the_mirror_leaves_a_landmark_the_artist_took_hold_of_alone():
    form = PrimaryForm(preset="pelvis", landmarks=_left_only(PELVIS_MARKS, PELVIS))
    form.landmarks = mirror_form_landmarks(form)
    moved = form.with_landmark_at("asis.R", (-9.0, 101.0, 7.5))
    form.landmarks = moved
    held = next(entry for entry in form.landmarks if entry.key == "asis.R")
    assert not held.mirrored
    again = mirror_form_landmarks(form)
    assert next(entry for entry in again if entry.key == "asis.R").at == (-9.0, 101.0, 7.5)


def test_symmetric_building_straightens_the_landmarks_without_moving_them():
    form = PrimaryForm(preset="pelvis")
    skew = np.array([1.5, 0.0, 0.0])
    for key, at in PELVIS_MARKS.items():
        # The left side is placed a little too far out.
        off = at + skew if key.endswith(".L") else at
        form.landmarks.append(PlacedLandmark(key=key, at=tuple(off)))
    straight = symmetrised_points(form)
    # Each pair is the same distance off the plane either side: what was 1.5
    # too far left is now 0.75 each way.
    assert straight["asis.L"][0] == pytest.approx(11.75, abs=1e-6)
    assert straight["asis.R"][0] == pytest.approx(-11.75, abs=1e-6)
    assert np.allclose(straight["asis.L"][1:], straight["asis.R"][1:])
    # The landmarks the artist placed are untouched.
    assert form.landmark_for("asis.L").point[0] == pytest.approx(12.5)
    # The clay built symmetric is symmetric, and the clay built as placed is
    # not.
    bucket = build_form(form, symmetric=True)[0][0]
    assert bucket.vertices[:, 0].max() == pytest.approx(-bucket.vertices[:, 0].min(), abs=1e-6)
    skewed = build_form(form)[0][0]
    assert skewed.vertices[:, 0].max() > -skewed.vertices[:, 0].min() + 1.0


def test_symmetric_building_drops_the_midline_onto_one_plane():
    form = PrimaryForm(preset="head")
    for key, at in HEAD_MARKS.items():
        off = at + np.array([1.5, 0.0, 0.0]) if key == "inion" else at
        form.landmarks.append(PlacedLandmark(key=key, at=tuple(off)))
    straight = symmetrised_points(form)
    midline = np.stack([straight[key] for key in HEAD.centre_keys()])
    spread = np.linalg.svd(midline - midline.mean(axis=0), compute_uv=False)
    assert spread[2] == pytest.approx(0.0, abs=1e-9)  # coplanar
    assert abs(straight["inion"][0]) < 1.0  # and nearer the midline than it was


def test_symmetric_building_reflects_a_side_that_is_missing():
    form = PrimaryForm(preset="ribcage")
    for key, at in RIBCAGE_MARKS.items():
        if not key.endswith(".R"):
            form.landmarks.append(PlacedLandmark(key=key, at=tuple(at)))
    straight = symmetrised_points(form)
    assert np.allclose(straight["widest_rib.R"], RIBCAGE_MARKS["widest_rib.R"], atol=1e-6)
    assert built_count(build_form(form, symmetric=True)) == 1
    assert built_count(build_form(form)) == 0
    # Without a plane the points come back as they are.
    lone = PrimaryForm(preset="ribcage", landmarks=form.landmarks[:2])
    assert set(symmetrised_points(lone)) == {entry.key for entry in lone.landmarks}


def test_the_mirror_waits_for_a_plane():
    form = PrimaryForm(
        preset="ribcage",
        landmarks=[
            PlacedLandmark(key="jugular_notch", at=(0, 148, 6)),
            PlacedLandmark(key="widest_rib.L", at=(15, 130, 0)),
        ],
    )
    assert not median_plane_ready(form)
    assert [entry.key for entry in mirror_form_landmarks(form)] == ["jugular_notch", "widest_rib.L"]


# -- the guided walk ----------------------------------------------------------


def _walk(preset, marks: dict, settings: FormSettings) -> tuple[FormTool, PrimaryForm]:
    """Place every landmark the tool asks for, off the synthetic figure."""
    tool = FormTool()
    form = PrimaryForm(preset=preset.key)
    tool.start_guide(preset.key, 0)
    for _ in range(100):
        entry = tool.current(form, settings)
        if entry is None:
            break
        if entry.key not in marks:
            tool.skip(form, settings)
            continue
        form.landmarks = tool.place(form, marks[entry.key], settings)
    return tool, form


def test_the_walk_asks_for_one_side_and_builds_the_form():
    settings = FormSettings(mirror=True)
    tool, form = _walk(PELVIS, PELVIS_MARKS, settings)
    placed, wanted = tool.progress(form, settings)
    asked = sum(1 for entry in PELVIS.landmarks if not entry.mirror_of)
    assert (placed, wanted) == (asked, asked)
    assert tool.current(form, settings) is None
    # The right side arrived by reflection.
    assert form.landmark_for("psis.R") is not None and form.landmark_for("psis.R").mirrored
    assert built_count(build_form(form)) == 1


def test_the_walk_asks_for_both_sides_with_the_mirror_off():
    settings = FormSettings(mirror=False)
    tool, form = _walk(RIBCAGE, RIBCAGE_MARKS, settings)
    assert tool.progress(form, settings) == (len(RIBCAGE.landmarks), len(RIBCAGE.landmarks))
    assert not form.landmark_for("widest_rib.R").mirrored


def test_the_walk_goes_stage_by_stage_and_the_form_grows_with_it():
    settings = FormSettings()
    tool = FormTool()
    form = PrimaryForm(preset="head")
    tool.start_guide("head", 0)
    seen: list[int] = []
    built: list[int] = []
    while (entry := tool.current(form, settings)) is not None:
        stage, done, asked = tool.stage_progress(form, settings)
        seen.append(stage)
        assert 0 <= done < asked
        form.landmarks = tool.place(form, HEAD_MARKS[entry.key], settings)
        built.append(built_count(build_form(form)))
    assert seen == sorted(seen)
    assert set(seen) == {0, 1, 2, 3, 4}
    assert built == sorted(built) and built[-1] == 5
    assert tool.stage_progress(form, settings) is None


def test_skip_and_back_walk_the_list_both_ways():
    settings = FormSettings()
    tool = FormTool()
    form = PrimaryForm(preset="pelvis")
    tool.start_guide("pelvis", 0)
    first = tool.current(form, settings)
    form.landmarks = tool.place(form, PELVIS_MARKS[first.key], settings)
    second = tool.current(form, settings)
    tool.skip(form, settings)
    assert tool.current(form, settings).key != second.key
    # Back un-skips the second before it un-places the first.
    assert tool.back(form, settings) == second.key
    assert tool.current(form, settings).key == second.key
    assert tool.back(form, settings) == first.key
    form.landmarks = form.without_landmarks(first.key)
    assert tool.current(form, settings).key == first.key
    assert tool.back(form, settings) is None


def test_the_walk_asks_for_the_other_side_when_the_midline_cannot_give_a_plane():
    # A preset walked out of order: a paired landmark before the midline is
    # down.  The mirror has no plane, so the right side is asked for.
    settings = FormSettings(mirror=True)
    tool = FormTool()
    form = PrimaryForm(
        preset="ribcage",
        landmarks=[PlacedLandmark(key="widest_rib.L", at=tuple(RIBCAGE_MARKS["widest_rib.L"]))],
    )
    tool.start_guide("ribcage", 0)
    assert any(entry.key == "widest_rib.R" for entry in tool.remaining(form, settings))


def test_a_form_store_names_forms_past_the_ones_it_has():
    store = FormStore()
    assert store.next_name("pelvis") == "Pelvis"
    store.add(PrimaryForm(name="Pelvis", preset="pelvis"))
    assert store.next_name("pelvis") == "Pelvis 2"
    assert store.next_name("head") == "Head"
    assert len(store) == 1
    store.clear()
    assert len(store) == 0


# -- sessions -----------------------------------------------------------------


def test_forms_survive_a_session_round_trip(tmp_path):
    form = PrimaryForm(
        name="Pelvis",
        preset="pelvis",
        landmarks=[PlacedLandmark(key="asis.L", at=(1.0, 2.0, 3.0), mirrored=False)],
        stage=0,
        visible=False,
    )
    session = Session(forms=[form], form_settings=FormSettings(color=(0.1, 0.2, 0.3), smooth=15.0))
    path = session.save(tmp_path / "forms.refview.json")
    loaded = Session.load(path)
    assert loaded.version == 11
    assert len(loaded.forms) == 1
    back = loaded.forms[0]
    assert back.name == "Pelvis" and back.preset == "pelvis"
    assert back.landmarks[0].key == "asis.L" and back.landmarks[0].at == (1.0, 2.0, 3.0)
    assert back.stage == 0 and back.visible is False
    assert loaded.form_settings.color == (0.1, 0.2, 0.3)
    assert loaded.form_settings.smooth == 15.0


def test_an_older_session_loads_without_forms():
    loaded = Session.from_dict({"version": 5, "armatures": []})
    assert loaded.forms == []
    assert loaded.form_settings == FormSettings()


# -- the rounded hull ----------------------------------------------------------


def test_a_rounded_hull_bows_out_between_its_points_and_keeps_them():
    cube = np.array([[x, y, z] for x in (0, 1) for y in (0, 1) for z in (0, 1)], dtype=np.float64)
    flat = Solid.from_points(cube)
    rounded = Solid.rounded(cube)
    # Still convex and closed, and bigger: the faces swell outward.
    assert _closed(rounded)
    assert rounded.volume() > flat.volume() * 1.3
    assert rounded.contains([0.5, 0.5, 1.05]) and not flat.contains([0.5, 0.5, 1.05])
    # Every original corner is still a corner of the clay.
    for corner in cube:
        assert any(np.allclose(corner, vertex) for vertex in rounded.vertices)
    # And nothing has gone inward: the flat hull sits inside the rounded one.
    for vertex in flat.vertices:
        assert rounded.contains(vertex, slack=1e-9)


def test_a_rounded_hull_refuses_what_a_flat_one_refuses():
    with pytest.raises(DegenerateHullError):
        rounded_hull([[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]])


# -- the freeform --------------------------------------------------------------

#: A left hand's worth of points: enough to hold a volume, none on a midline.
HAND = {
    "wrist": (20.0, 80.0, 0.0),
    "thumb": (24.0, 76.0, 4.0),
    "little": (16.0, 70.0, -1.0),
    "knuckle": (21.0, 72.0, 2.0),
    "palm": (20.0, 75.0, -3.0),
}


def _freeform(points: dict[str, tuple], side: Side = Side.CENTRE, **kwargs) -> PrimaryForm:
    form = PrimaryForm(name="Hand", preset=FREEFORM, **kwargs)
    for name, at in points.items():
        entry = freeform_landmark(name, side, (held.key for held in form.points))
        form.points = form.with_point(entry)
        form.landmarks.append(PlacedLandmark(key=entry.key, at=at))
    return form


def test_freeform_landmarks_are_keyed_by_name_and_side_and_never_collide():
    assert landmark_key("Nipple", Side.LEFT) == ("nipple.L", "Nipple")
    assert landmark_key("Top of the crest", Side.CENTRE) == ("top_of_the_crest", "Top of the crest")
    assert landmark_key("", Side.RIGHT) == ("point.R", "Point")
    # The same name on the same side is numbered, in the key and the name.
    assert landmark_key("Nipple", Side.LEFT, ["nipple.L"]) == ("nipple_2.L", "Nipple 2")
    assert landmark_key("Nipple", Side.LEFT, ["nipple.L", "nipple_2.L"]) == (
        "nipple_3.L",
        "Nipple 3",
    )
    # The other side is not a collision: it is the pair.
    assert landmark_key("Nipple", Side.RIGHT, ["nipple.L"]) == ("nipple.R", "Nipple")
    assert twin_key("nipple.L") == "nipple.R" and twin_key("nipple.R") == "nipple.L"
    assert twin_key("sternum") == ""


def test_a_freeform_is_its_own_recipe_and_pairs_its_sides():
    left = freeform_landmark("Nipple", Side.LEFT)
    centre = freeform_landmark("Sternum", Side.CENTRE)
    spec = form_spec(PrimaryForm(preset=FREEFORM, points=[centre, left]))
    assert spec is not None and spec.key == FREEFORM and len(spec.stages) == 1
    keys = [(entry.key, entry.mirror_of) for entry in spec.landmarks]
    # The left is followed by a right for the mirror to guess at.
    assert keys == [("sternum", ""), ("nipple.L", ""), ("nipple.R", "nipple.L")]
    guess = spec.landmark("nipple.R")
    assert guess.side is Side.RIGHT and guess.name == "Nipple" and guess.title == "Nipple (right)"
    # Placed on both sides by hand, they are a pair and the right mirrors the left.
    right = freeform_landmark("Nipple", Side.RIGHT, ["nipple.L"])
    paired = paired_landmarks([left, right])
    assert [(entry.key, entry.mirror_of) for entry in paired] == [
        ("nipple.L", ""),
        ("nipple.R", "nipple.L"),
    ]
    # Placed on the right first, the left is the guess.
    paired = paired_landmarks([right])
    assert [(entry.key, entry.mirror_of) for entry in paired] == [
        ("nipple.R", ""),
        ("nipple.L", "nipple.R"),
    ]


def test_a_freeform_builds_the_hull_of_its_points_once_they_hold_a_volume():
    form = _freeform(HAND)
    stages = build_form(form)
    assert built_count(stages) == 1
    hull = stages[0][0]
    for at in HAND.values():
        assert hull.contains(at, slack=1e-9)
    assert form_mesh(form, smooth=40.0) is not None
    # Fewer points, or flat ones, are not a form yet -- and not an error.
    flat = _freeform({"a": (0, 0, 0), "b": (1, 0, 0), "c": (0, 1, 0), "d": (1, 1, 0)})
    assert built_count(build_form(flat)) == 0
    few = _freeform({"a": (0, 0, 0), "b": (1, 0, 0), "c": (0, 1, 0)})
    assert built_count(build_form(few)) == 0 and form_mesh(few, smooth=40.0) is None


def test_a_freeform_can_be_smooth_and_the_fill_is_part_of_its_signature():
    faceted = _freeform(HAND, fill=FormFill.FACETED)
    smooth = _freeform(HAND, fill=FormFill.SMOOTH)
    assert build_form(smooth)[0][0].volume() > build_form(faceted)[0][0].volume()
    assert landmark_signature(faceted) != landmark_signature(smooth)
    # Which side a point is on is part of it too: it decides what is paired.
    assert landmark_signature(_freeform(HAND)) != landmark_signature(_freeform(HAND, Side.LEFT))


def test_a_freeform_with_no_pair_is_left_alone_by_the_symmetric_build():
    # A hand marked "centre" throughout is a hand, not a slab: nothing is
    # dropped onto a plane.
    form = _freeform(HAND)
    straight = symmetrised_points(form)
    for key, at in form.placed_points().items():
        assert np.allclose(straight[key], at)
    assert built_count(build_form(form, symmetric=True)) == 1


def test_a_freeform_with_pairs_is_mirrored_and_symmetrised_like_a_preset():
    # A midline of three points opened out into a plane, and one side of a chest.
    form = _freeform({"Notch": (0, 148, 6), "Xiphoid": (0, 128, 9), "C7": (0, 152, -7)})
    assert median_plane_ready(form)
    for name, at in (("Nipple", (10.0, 135.0, 8.0)), ("Widest rib", (15.0, 130.0, 0.0))):
        entry = freeform_landmark(name, Side.LEFT, (held.key for held in form.points))
        form.points = form.with_point(entry)
        form.landmarks.append(PlacedLandmark(key=entry.key, at=at))
    form.landmarks = mirror_form_landmarks(form)
    guess = form.landmark_for("nipple.R")
    assert guess is not None and guess.mirrored
    assert np.allclose(guess.point, (-10.0, 135.0, 8.0), atol=1e-6)
    assert form_landmark_title(form, "nipple.R") == "Nipple (right)"
    # Knock the left out of true and the symmetric build averages the pair.
    form.landmarks = form.with_landmark_at("nipple.L", (12.0, 135.0, 8.0))
    straight = symmetrised_points(form)
    assert straight["nipple.L"][0] == pytest.approx(11.0, abs=1e-6)
    assert straight["nipple.R"][0] == pytest.approx(-11.0, abs=1e-6)
    assert built_count(build_form(form, symmetric=True)) == 1


def test_the_freeform_walk_lays_down_whatever_is_pending():
    settings = FormSettings(mirror=False)
    tool = FormTool()
    form = PrimaryForm(name="Knee", preset=FREEFORM)
    run = tool.start_guide(FREEFORM, 0)
    assert run is not None and run.freeform
    # Nothing pending, nothing placed.
    assert tool.current(form, settings) is None
    assert tool.place(form, np.zeros(3), settings) is None
    run.pending = freeform_landmark("Patella", Side.LEFT)
    assert tool.current(form, settings) is run.pending
    landmarks = tool.place(form, np.array([5.0, 50.0, 8.0]), settings)
    assert [entry.key for entry in landmarks] == ["patella.L"]
    form.landmarks = landmarks
    form.points = form.with_point(run.pending)
    assert tool.progress(form, settings) == (1, 1)
    assert tool.stage_progress(form, settings) is None
    assert tool.back(form, settings) is None  # the panel takes a freeform's points back
    # Free points are a freeform's alone.
    assert tool.free_points(form, FormSettings(free_placement=True))
    assert not tool.free_points(PrimaryForm(preset="pelvis"), FormSettings(free_placement=True))
    assert not tool.free_points(form, FormSettings(free_placement=False))


def test_a_freeform_survives_a_session_round_trip(tmp_path):
    form = _freeform(HAND, Side.LEFT, fill=FormFill.SMOOTH)
    form.points = form.with_point_named("thumb.L", "Thumb tip")
    session = Session(forms=[form, PrimaryForm(name="Pelvis", preset="pelvis")])
    loaded = Session.load(session.save(tmp_path / "hand.refview.json"))
    back = loaded.forms[0]
    assert back.preset == FREEFORM and back.freeform
    assert back.fill is FormFill.SMOOTH
    assert [entry.key for entry in back.points] == [entry.key for entry in form.points]
    assert back.point_for("thumb.L").name == "Thumb tip"
    assert back.point_for("thumb.L").side is Side.LEFT
    assert built_count(build_form(back)) == 1
    # A preset carries the new fields at their defaults.
    pelvis = loaded.forms[1]
    assert not pelvis.freeform and pelvis.points == [] and pelvis.fill is FormFill.FACETED
