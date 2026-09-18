"""Skinning a model to a skeleton it did not come with.

A rigged file arrives with weights painted by someone who knew the figure.
A skeleton the artist built here -- clicked in, grown out of an armature,
fitted from the humanoid preset -- has none, and without them it poses in the
air while the model stands still.  This is what gives it some: not the
weights a rigger would paint, but weights good enough that a figure can be
turned to read a pose off it, made in one click and undone in one.

Three ways of deciding which joint moves each vertex, coarsest first:

* **Nearest bone.**  Every vertex goes wholly to the joint whose bone it is
  closest to.  Rigid pieces, hard creases at the joints; what a puppet does.

* **Envelope.**  Every vertex is shared out among its nearest few bones in
  inverse proportion to a power of the distance.  Soft, and blind: a hand
  resting on a hip takes some of the hip's weight through the air between.

* **Heat diffusion**, the default, after Baran and Popović's *Pinocchio*.
  Each bone is a source of heat clamped to one on the vertices it is nearest
  to, and the heat is let spread over the *surface* of the mesh until it
  settles; the temperature it settles at is the weight.  Heat goes along the
  skin and not through the air, so the hand on the hip stays the hand's, and
  the blend at a knee is as wide as the leg is thick.  On the mesh's graph
  that is one sparse linear system, ``(L + H) w = H p``, with the cotangent
  Laplacian ``L`` for the spreading and a diagonal ``H`` for the clamping,
  the same matrix for every bone and solved for all of them at once by
  conjugate gradients.

Which bone is *nearest* is judged with the surface's facing as well as the
distance: a bone that lies in front of a vertex -- out through the skin
rather than behind it -- is the other arm, or the torso beside the arm, and
is passed over for the nearest bone that lies inside.  That is the cheap
stand-in for the visibility test the paper does with rays, and it settles
the cases that matter most: arms held by the sides, thighs touching.

Everything here works on a *welded* copy of the mesh, since a file that
stores every corner three times over has three copies of every vertex and
a surface that is nowhere joined up; the weights are handed back to every
copy.  The skeleton is bound where it stands: its pose becomes its rest, so
that what the artist sees at the moment of skinning is what a reset pose
puts back.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass, replace

import numpy as np

from .linalg import IDENTITY_QUAT
from .mesh import Mesh, _gathered, compute_vertex_normals
from .progress import Progress, silent
from .skeleton import (
    AutoSkinSettings,
    Joint,
    Rig,
    Skeleton,
    Skin,
    SkinMethod,
    _matrix16,
)

__all__ = [
    "AutoSkin",
    "AutoSkinError",
    "AutoSkinSettings",
    "SkinMethod",
    "auto_skin",
    "bone_segments",
    "unique_names",
]


#: A blend across a joint is judged against the surface's facing at this
#: cosine: a bone that lies within sixty degrees of straight out through the
#: skin is in front of it, not inside it.
_FACING_COSINE = 0.5

#: Joints solved for in one pass of the conjugate gradients.  Sixteen
#: columns is a matvec the cache still likes; the passes are chunked so a
#: hundred-joint rig on a heavy scan does not want a gigabyte at once.
_SOLVE_COLUMNS = 16

#: A weight below this share is the far tail of a bone's warmth, and is
#: dropped before the top influences are picked: a hand does not follow the
#: hip by a hundredth, however the numbers came out.
_WEIGHT_FLOOR = 5e-3


class AutoSkinError(ValueError):
    """Raised when there is nothing to skin, or nothing to skin it to."""


@dataclass
class AutoSkin:
    """What :func:`auto_skin` hands back: the rig, and the joints to keep with it."""

    #: The skin, in the coordinates the mesh and skeleton were given in.
    rig: Rig
    #: The skeleton's joints with the pose baked into the rest and each
    #: named for the rig, ready to be written into the skeleton.
    joints: list[Joint]
    #: How many vertices ended up with no joint at all and so keep their
    #: place.  None, as the methods stand -- every vertex has a nearest
    #: bone -- but counted, so that the panel could say so if one ever did.
    unclaimed: int = 0


def auto_skin(
    mesh: Mesh,
    skeleton: Skeleton,
    settings: AutoSkinSettings | None = None,
    progress: Progress | None = None,
) -> AutoSkin:
    """Skin ``mesh`` to ``skeleton``, both given in the same coordinates.

    The skeleton is bound as it stands: the rig's rest is the skeleton's
    current pose, and the joints handed back have that pose written into
    their rests.  Raises :class:`AutoSkinError` for a mesh with no
    triangles or a skeleton with no bones.
    """
    settings = settings or AutoSkinSettings()
    progress = progress or silent()
    if mesh.triangle_count == 0:
        raise AutoSkinError("The model has no surface to skin")
    if not skeleton.joints:
        raise AutoSkinError("The skeleton has no joints")

    world = skeleton.world_matrices()
    names = unique_names([joint.name or "Joint" for joint in skeleton.joints])
    segments, owners = bone_segments(skeleton, world[:, :3, 3])
    if not len(segments):
        raise AutoSkinError("The skeleton has no bones")

    progress.report(0, 1, "Welding the surface...")
    welded = _Welded.of(mesh)
    progress.report(0.08, message="Measuring the bones...")
    distances = _joint_distances(welded, segments, owners, len(skeleton.joints), settings.facing)
    nearest = np.argmin(distances, axis=1)

    solve = progress.slice(0.12, 0.94)
    if settings.method is SkinMethod.HEAT:
        weights = _heat_weights(welded, distances, nearest, settings.heat, solve)
    elif settings.method is SkinMethod.ENVELOPE:
        solve.report(0, 1, "Sharing out the weights...")
        weights = _envelope_weights(distances, settings.falloff)
    else:
        solve.report(0, 1, "Assigning the nearest bone...")
        weights = _nearest_weights(nearest, len(skeleton.joints))

    progress.report(0.95, message="Binding...")
    joints, slot_weights = _top_influences(weights, settings.influences)
    joints = joints[welded.back]
    slot_weights = slot_weights[welded.back]
    inverse_bind = np.linalg.inv(world)
    skin = Skin(joints, slot_weights, inverse_bind, mesh.positions, mesh.normals)
    rest_local = _baked_rest(skeleton, world)
    rig = Rig(
        names,
        [joint.parent for joint in skeleton.joints],
        rest_local,
        skin,
        tag=secrets.token_hex(4),
    )
    bound = [
        replace(
            joint,
            rest=_matrix16(rest_local[index]),
            rotation=IDENTITY_QUAT,
            translation=(0.0, 0.0, 0.0),
            source=names[index],
        )
        for index, joint in enumerate(skeleton.joints)
    ]
    progress.report(1.0, message="Skinned")
    return AutoSkin(rig, bound, int(np.count_nonzero(slot_weights.sum(axis=1) <= 0.0)))


def unique_names(names: list[str]) -> list[str]:
    """``names`` with any repeat numbered, since the skin matches joints by name."""
    seen: dict[str, int] = {}
    out: list[str] = []
    for name in names:
        if name not in seen:
            seen[name] = 1
            out.append(name)
            continue
        while True:
            seen[name] += 1
            candidate = f"{name}.{seen[name]}"
            if candidate not in seen:
                seen[candidate] = 1
                out.append(candidate)
                break
    return out


def bone_segments(skeleton: Skeleton, positions: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Every bone as ``(start, end)`` points, and which joint each belongs to.

    A joint owns the bones that leave it -- turning the joint swings them --
    so a joint with three children owns three bones.  A leaf owns a bone
    that is not drawn: the last phalanx of a finger, the skull above the
    head joint, carried on past the leaf in the direction its parent's
    bone was going and as long as that bone was, since that is where a
    rigger puts the tail of an end bone and what a file's weights on such
    a joint were painted for.  A joint alone in the world, with neither
    parent nor child, owns the point it stands on, so that a one-joint rig
    still holds the model.
    """
    positions = np.asarray(positions, dtype=np.float64).reshape(-1, 3)
    segments: list[tuple[np.ndarray, np.ndarray]] = []
    owners: list[int] = []
    for parent, child in skeleton.bones():
        segments.append((positions[parent], positions[child]))
        owners.append(parent)
    for index, joint in enumerate(skeleton.joints):
        if skeleton.children(index):
            continue
        if skeleton._holds(joint.parent) and joint.parent != index:
            reach = positions[index] - positions[joint.parent]
            segments.append((positions[index], positions[index] + reach))
        else:
            segments.append((positions[index], positions[index]))
        owners.append(index)
    if not segments:
        return np.zeros((0, 2, 3)), np.zeros(0, dtype=np.int64)
    return np.array(segments, dtype=np.float64), np.array(owners, dtype=np.int64)


# ----------------------------------------------------------------------
# The welded surface
# ----------------------------------------------------------------------


class _Welded:
    """The mesh with every position held once, and the graph over it."""

    __slots__ = ("positions", "faces", "back", "normals", "used")

    def __init__(self, positions: np.ndarray, faces: np.ndarray, back: np.ndarray) -> None:
        self.positions = positions
        self.faces = faces
        #: Which welded vertex each of the mesh's own vertices is.
        self.back = back
        self.normals = compute_vertex_normals(positions, faces).astype(np.float64)
        #: Whether a welded vertex is on any triangle.  One that is not has
        #: no surface to diffuse over and is given its nearest bone outright.
        self.used = np.zeros(len(positions), dtype=bool)
        if len(faces):
            self.used[faces.ravel()] = True

    @classmethod
    def of(cls, mesh: Mesh) -> _Welded:
        positions, back = np.unique(
            np.asarray(mesh.positions, dtype=np.float32), axis=0, return_inverse=True
        )
        back = np.asarray(back, dtype=np.int64).ravel()
        faces = back[np.asarray(mesh.indices, dtype=np.int64).reshape(-1, 3)]
        # A triangle two of whose corners weld together is a line, and has
        # no area to weight an edge by.
        whole = (faces[:, 0] != faces[:, 1]) & (faces[:, 1] != faces[:, 2])
        whole &= faces[:, 0] != faces[:, 2]
        return cls(positions.astype(np.float64), faces[whole], back)

    @property
    def count(self) -> int:
        return len(self.positions)


def _joint_distances(
    welded: _Welded,
    segments: np.ndarray,
    owners: np.ndarray,
    joint_count: int,
    facing: bool,
) -> np.ndarray:
    """How far each welded vertex is from each joint's nearest bone, ``(n, j)``.

    A joint with no bone is infinitely far.  With ``facing``, a bone that
    lies out in front of the surface at a vertex is put beyond every bone
    behind it, so that it is never the nearest while anything inside the
    body is -- and if nothing is, the facing is ignored for that vertex
    rather than leaving it boneless.
    """
    points = welded.positions
    count = len(points)
    distances = np.full((count, joint_count), np.inf, dtype=np.float32)
    rejected = np.full((count, joint_count), np.inf, dtype=np.float32)
    for (start, end), owner in zip(segments, owners, strict=True):
        along = end - start
        length2 = float(along @ along)
        if length2 > 1e-24:
            t = np.clip(((points - start) @ along) / length2, 0.0, 1.0)
            closest = start + t[:, None] * along
        else:
            closest = np.broadcast_to(start, points.shape)
        toward = closest - points
        distance = np.linalg.norm(toward, axis=1)
        if facing:
            cosine = np.einsum("ij,ij->i", welded.normals, toward) / np.maximum(distance, 1e-12)
            inside = cosine < _FACING_COSINE
            held = distances[:, owner]
            np.minimum(held, np.where(inside, distance, np.inf), out=held)
            np.minimum(rejected[:, owner], distance, out=rejected[:, owner])
        else:
            np.minimum(distances[:, owner], distance, out=distances[:, owner])
    if facing:
        boneless = ~np.isfinite(distances).any(axis=1)
        if np.any(boneless):
            distances[boneless] = rejected[boneless]
    return distances


# ----------------------------------------------------------------------
# The three methods
# ----------------------------------------------------------------------


def _nearest_weights(nearest: np.ndarray, joint_count: int) -> np.ndarray:
    weights = np.zeros((len(nearest), joint_count), dtype=np.float64)
    weights[np.arange(len(nearest)), nearest] = 1.0
    return weights


def _envelope_weights(distances: np.ndarray, falloff: float) -> np.ndarray:
    finite = np.isfinite(distances)
    reach = np.where(finite, distances, 0.0)
    # Nothing is nearer than a sliver of the nearest bone's distance, so a
    # vertex sitting on a bone takes it wholly rather than dividing by nought.
    nearest = np.min(np.where(finite, distances, np.inf), axis=1, keepdims=True)
    floor = np.maximum(nearest * 1e-3, 1e-9)
    with np.errstate(divide="ignore", over="ignore"):
        weights = np.where(finite, 1.0 / np.maximum(reach, floor) ** max(float(falloff), 0.1), 0.0)
    weights[~np.isfinite(weights)] = 0.0
    return weights


def _heat_weights(
    welded: _Welded,
    distances: np.ndarray,
    nearest: np.ndarray,
    heat: float,
    progress: Progress,
) -> np.ndarray:
    """Solve ``(L + H) w = H p`` for every joint at once; see the module note."""
    count, joint_count = distances.shape
    used = np.flatnonzero(welded.used)
    weights = _nearest_weights(nearest, joint_count)
    if len(used) < 3:
        return weights
    # The solve runs over the vertices that are on the surface; the rest
    # keep their nearest bone.
    renumber = np.full(count, -1, dtype=np.int64)
    renumber[used] = np.arange(len(used))
    faces = renumber[welded.faces]
    points = welded.positions[used]
    fine = _CotLaplacian(points, faces)

    # H: the pull towards the nearest bone's value, strong close to a bone
    # and weak far from every bone.  Weighted by the vertex's share of the
    # surface, as the Laplacian is, so the balance between the two does not
    # depend on how finely the mesh is cut or how big it is.
    near = distances[used, nearest[used]]
    floor = max(0.25 * fine.mean_edge, 1e-9)
    clamp = fine.areas * max(float(heat), 1e-6) / np.maximum(near, floor) ** 2
    solver = _TwoLevel(fine, points, clamp)

    solved = np.zeros((len(used), joint_count), dtype=np.float64)
    labels = nearest[used]
    present = np.unique(labels)
    total = len(present)
    for start in range(0, total, _SOLVE_COLUMNS):
        chunk = present[start : start + _SOLVE_COLUMNS]
        rhs = np.zeros((len(used), len(chunk)), dtype=np.float64)
        for column, joint in enumerate(chunk):
            rows = np.flatnonzero(labels == joint)
            rhs[rows, column] = clamp[rows]

        done = start + len(chunk)

        def watch(share: float, start=start, done=done) -> None:
            progress.report(
                start + share * (done - start),
                total,
                f"Diffusing heat from {min(done, total)} of {total} bones...",
            )

        solved[:, chunk] = solver.solve(rhs, watch)
    progress.report(total, total)
    weights[used] = np.clip(solved, 0.0, None)
    return weights


#: Neighbours a vertex is given a slot for in the padded table below.  A
#: regular mesh has six; a pole in a fan has more, and the few that go past
#: the table are kept on a list of their own.
_SLOTS = 16


class _Graph:
    """A symmetric sparse matrix with a diagonal, kept as a matvec.

    Held as a table with one row per vertex and a slot per neighbour --
    the neighbour's index and the edge's weight, padded with a weightless
    edge to itself -- so that applying it to a block of columns is one
    gather and one small matrix product, both of which numpy does at the
    speed of memory.  The segmented sums a sparse matrix usually wants are
    what numpy does slowest, and this is the inner loop of the whole
    skinning.  The odd vertex with more neighbours than slots keeps the
    rest on a list applied the slow way, which is nothing when it is odd.

    Everything is single precision: the solve is stopped at three figures,
    and half the bytes is half the time.
    """

    __slots__ = (
        "count",
        "slot_cols",
        "slot_weights",
        "spill",
        "diagonal",
        "_rows",
        "_cols",
        "_weights",
    )

    def __init__(self, count: int, rows: np.ndarray, cols: np.ndarray, weights: np.ndarray) -> None:
        """From directed edges ``rows -> cols``; repeats of a pair are summed."""
        self.count = int(count)
        rows = np.asarray(rows, dtype=np.int64)
        cols = np.asarray(cols, dtype=np.int64)
        weights = np.asarray(weights, dtype=np.float64)
        if len(rows):
            order = np.lexsort((cols, rows))
            rows, cols, weights = rows[order], cols[order], weights[order]
            key = rows * self.count + cols
            starts = np.flatnonzero(np.concatenate([[True], key[1:] != key[:-1]]))
            weights = np.add.reduceat(weights, starts)
            rows, cols = rows[starts], cols[starts]
        self._rows, self._cols, self._weights = rows, cols, weights
        self.diagonal = np.bincount(rows, weights, minlength=self.count)
        degree = np.bincount(rows, minlength=self.count)
        first = np.concatenate([[0], np.cumsum(degree)[:-1]])
        slot = np.arange(len(rows)) - first[rows]
        held = slot < _SLOTS
        self.slot_cols = np.tile(np.arange(self.count, dtype=np.int32)[:, None], (1, _SLOTS))
        self.slot_weights = np.zeros((self.count, _SLOTS), dtype=np.float32)
        self.slot_cols[rows[held], slot[held]] = cols[held]
        self.slot_weights[rows[held], slot[held]] = weights[held]
        over = ~held
        self.spill = (rows[over], cols[over].astype(np.int32), weights[over].astype(np.float32))

    def apply(self, block: np.ndarray, diagonal: np.ndarray) -> np.ndarray:
        """``(diag(diagonal) - W) @ block`` for a ``(n, k)`` block."""
        gathered = np.take(block, self.slot_cols.ravel(), axis=0).reshape(
            self.count, _SLOTS, block.shape[1]
        )
        summed = np.matmul(self.slot_weights[:, None, :], gathered)[:, 0, :]
        out = diagonal[:, None] * block - summed
        rows, cols, weights = self.spill
        if len(rows):
            np.subtract.at(out, rows, weights[:, None] * block[cols])
        return out

    def coarsened(self, cluster: np.ndarray, count: int) -> _Graph:
        """The graph with each cluster of vertices folded into one node.

        Edge weights between two clusters add up, which is exactly the
        Laplacian of the clustered surface: what flows between two patches
        is the sum of what flows across every edge between them.
        """
        a, b = cluster[self._rows], cluster[self._cols]
        across = a != b
        return _Graph(count, a[across], b[across], self._weights[across])


class _CotLaplacian(_Graph):
    """The cotangent Laplacian of a triangle mesh, as a :class:`_Graph`.

    Cotangents are clamped at nought: an obtuse triangle's negative weight
    is what makes the matrix indefinite and the solve wander, and the
    answer is barely changed by losing it.
    """

    __slots__ = ("areas", "mean_edge")

    def __init__(self, points: np.ndarray, faces: np.ndarray) -> None:
        a, b, c = (points[faces[:, i]] for i in range(3))
        corners = []
        for tip, left, right in ((a, b, c), (b, c, a), (c, a, b)):
            u, v = left - tip, right - tip
            cross = np.linalg.norm(np.cross(u, v), axis=1)
            cot = np.einsum("ij,ij->i", u, v) / np.maximum(cross, 1e-20)
            corners.append(np.clip(cot, 0.0, None) * 0.5)
        # The edge opposite each corner takes half that corner's cotangent.
        ends = np.concatenate([faces[:, [1, 2]], faces[:, [2, 0]], faces[:, [0, 1]]])
        weight = np.concatenate(corners)
        super().__init__(
            len(points),
            np.concatenate([ends[:, 0], ends[:, 1]]),
            np.concatenate([ends[:, 1], ends[:, 0]]),
            np.concatenate([weight, weight]),
        )
        area = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
        self.areas = np.bincount(faces.ravel(), np.repeat(area / 3.0, 3), minlength=len(points))
        lengths = np.linalg.norm(points[ends[:, 0]] - points[ends[:, 1]], axis=1)
        self.mean_edge = float(lengths.mean()) if len(lengths) else 0.0


#: A coarse node gathers the vertices within a cell this many mean edges
#: across.  Four is a dozen or so vertices to a node on a regular mesh:
#: enough that the coarse solve is a fraction of the fine one, and fine
#: enough that what it gets wrong is a few rings' worth of smoothing.
_COARSE_CELL = 4.0

#: The fine solve stops when the residual is this far down, or after this
#: many iterations.  Loose, on purpose: the coarse solve has the answer's
#: shape already, and the fine iterations are there to take the patch
#: edges out of it, which they do in a few dozen.
_FINE_TOLERANCE = 3e-3
_FINE_ITERATIONS = 40
_COARSE_TOLERANCE = 1e-4
_COARSE_ITERATIONS = 600


class _TwoLevel:
    """Solve ``(L + H) x = b`` coarse first, then finish on the mesh itself.

    Conjugate gradients on a Laplacian take as many iterations as the mesh
    is wide, in edges, and every iteration is a pass over every edge.  So
    the mesh is first gathered into patches a few edges across -- vertices
    in one grid cell that are joined to each other by the surface, so two
    thighs touching through a cell wall stay two patches -- and the same
    system is solved over the patches, which is a small fraction of the
    work.  The patch answer, handed to every vertex in its patch, is then
    within a few smoothing steps of the fine answer, and conjugate
    gradients smooth first.  What comes out is not the fine answer to the
    last figure; it is the fine answer to the figures a weight is read to,
    in a tenth of the time.
    """

    def __init__(self, fine: _CotLaplacian, points: np.ndarray, clamp: np.ndarray) -> None:
        self.fine = fine
        self.diagonal = fine.diagonal + clamp
        self.cluster, self.coarse_count = _patches(fine, points)
        self.coarse = fine.coarsened(self.cluster, self.coarse_count)
        coarse_clamp = np.bincount(self.cluster, clamp, minlength=self.coarse_count)
        self.coarse_diagonal = self.coarse.diagonal + coarse_clamp

    def solve(self, rhs: np.ndarray, watch) -> np.ndarray:
        coarse_rhs = np.stack(
            [
                np.bincount(self.cluster, rhs[:, c], minlength=self.coarse_count)
                for c in range(rhs.shape[1])
            ],
            axis=1,
        )
        coarse = _conjugate_gradients(
            self.coarse,
            self.coarse_diagonal,
            coarse_rhs,
            np.zeros_like(coarse_rhs),
            _COARSE_TOLERANCE,
            _COARSE_ITERATIONS,
            lambda share: watch(0.5 * share),
        )
        return _conjugate_gradients(
            self.fine,
            self.diagonal,
            rhs,
            coarse[self.cluster],
            _FINE_TOLERANCE,
            _FINE_ITERATIONS,
            lambda share: watch(0.5 + 0.5 * share),
        ).astype(np.float64)


def _patches(graph: _CotLaplacian, points: np.ndarray) -> tuple[np.ndarray, int]:
    """Gather the vertices into patches; see :class:`_TwoLevel`."""
    cell = max(graph.mean_edge * _COARSE_CELL, 1e-9)
    cells = np.floor(points / cell).astype(np.int64)
    _, cell_of = np.unique(cells, axis=0, return_inverse=True)
    cell_of = np.asarray(cell_of).ravel()
    rows, cols = graph._rows, graph._cols
    within = cell_of[rows] == cell_of[cols]
    links = np.stack([rows[within], cols[within]], axis=1)
    root = _gathered(links, graph.count)
    _, cluster = np.unique(root, return_inverse=True)
    cluster = np.asarray(cluster).ravel()
    return cluster, (int(cluster.max()) + 1 if len(cluster) else 0)


def _conjugate_gradients(
    graph: _Graph,
    diagonal: np.ndarray,
    rhs: np.ndarray,
    guess: np.ndarray,
    tolerance: float,
    iterations: int,
    watch,
) -> np.ndarray:
    """Solve ``(diag - W) x = rhs`` for every column of ``rhs`` together.

    Preconditioned by the diagonal, which is nearly the whole matrix near
    the bones.  Every column takes every step until the last of them is
    within tolerance: the columns are the whole point of the batching, and
    picking the finished ones out costs more than carrying them.
    """
    diagonal = np.asarray(diagonal, dtype=np.float32)
    rhs = np.asarray(rhs, dtype=np.float32)
    x = np.array(guess, dtype=np.float32)
    r = rhs - graph.apply(x, diagonal)
    inverse = (1.0 / np.maximum(diagonal, 1e-30))[:, None]
    z = inverse * r
    p = z.copy()
    rz = np.einsum("ij,ij->j", r, z)
    target = tolerance * np.maximum(np.linalg.norm(rhs, axis=0), 1e-30)
    for iteration in range(iterations):
        if np.all(np.linalg.norm(r, axis=0) <= target):
            break
        if iteration % 10 == 0:
            watch(iteration / iterations)
        ap = graph.apply(p, diagonal)
        pap = np.einsum("ij,ij->j", p, ap)
        alpha = np.where(pap > 0.0, rz / np.where(pap > 0.0, pap, 1.0), 0.0)
        x += alpha * p
        r -= alpha * ap
        np.multiply(inverse, r, out=z)
        rz_next = np.einsum("ij,ij->j", r, z)
        beta = np.where(rz > 0.0, rz_next / np.where(rz > 0.0, rz, 1.0), 0.0)
        p *= beta
        p += z
        rz = rz_next
    watch(1.0)
    return x


# ----------------------------------------------------------------------
# From weights to a skin
# ----------------------------------------------------------------------


def _top_influences(weights: np.ndarray, influences: int) -> tuple[np.ndarray, np.ndarray]:
    """Each vertex's heaviest few joints, renormalised, in the four slots a skin has."""
    keep = max(1, min(int(influences), 4))
    count, joint_count = weights.shape
    weights = np.where(weights >= _WEIGHT_FLOOR, weights, 0.0)
    joints = np.zeros((count, 4), dtype=np.int32)
    slots = np.zeros((count, 4), dtype=np.float32)
    if count == 0 or joint_count == 0:
        return joints, slots
    take = min(keep, joint_count)
    order = np.argpartition(-weights, take - 1, axis=1)[:, :take]
    picked = np.take_along_axis(weights, order, axis=1)
    total = picked.sum(axis=1, keepdims=True)
    picked = np.where(total > 0.0, picked / np.maximum(total, 1e-30), 0.0)
    # Heaviest first, as a file lays them out, so a reader that only looks
    # at the first slot sees the joint that matters.
    rank = np.argsort(-picked, axis=1)
    joints[:, :take] = np.take_along_axis(order, rank, axis=1)
    slots[:, :take] = np.take_along_axis(picked, rank, axis=1)
    joints[slots <= 0.0] = 0
    return joints, slots


def _baked_rest(skeleton: Skeleton, world: np.ndarray) -> np.ndarray:
    """Each joint's world transform relative to its parent's: the pose as a rest."""
    rest = np.empty_like(world)
    for index, joint in enumerate(skeleton.joints):
        parent = joint.parent
        if 0 <= parent < len(skeleton.joints) and parent != index:
            rest[index] = np.linalg.inv(world[parent]) @ world[index]
        else:
            rest[index] = world[index]
    return rest
