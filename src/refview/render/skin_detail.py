"""Procedural skin micro-relief and the pre-integrated diffusion table.

Reference meshes have no UV layout, so the relief is a tileable 3D field the
shader samples at world position: pores as pits, the polygonal furrow network
between them, and a little organic noise. The volume stores the height slope
rather than the height, so bump mapping is a single fetch and needs no tangent
frame. Slopes are unitless (height per cell width), which keeps the relief
looking the same whatever pore size the artist chooses.

The diffusion table is Penner-style pre-integration of Burley's normalised
diffusion profile over a sphere, indexed by cos(theta) and log2(radius / d).
The preview reads it once per channel to bend the terminator red without any
ray queries. All of this runs on NumPy once, at start-up.
"""

from __future__ import annotations

from itertools import product

import numpy as np

#: Pore cells per edge of one tile; the shader sizes a tile from the pore size.
RELIEF_CELLS = 8
#: Table axis: log2(sphere radius / diffusion length) runs from -2 to 6.
LUT_LOG_MIN, LUT_LOG_SPAN = -2.0, 8.0


def _fade(t: np.ndarray) -> np.ndarray:
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


def value_noise(size: int, period: int, rng: np.random.Generator) -> np.ndarray:
    """Tileable value noise in ``[0, 1]`` on a ``size``-cubed grid."""
    lattice = rng.random((period, period, period))
    coords = (np.arange(size) + 0.5) * period / size
    i0 = np.floor(coords).astype(int) % period
    i1 = (i0 + 1) % period
    w = _fade(coords - np.floor(coords))
    result = np.zeros((size, size, size))
    for dz, dy, dx in product((0, 1), repeat=3):
        corner = lattice[np.ix_(i1 if dz else i0, i1 if dy else i0, i1 if dx else i0)]
        weight = (
            (w if dz else 1.0 - w)[:, None, None]
            * (w if dy else 1.0 - w)[None, :, None]
            * (w if dx else 1.0 - w)[None, None, :]
        )
        result += corner * weight
    return result


def fbm(size: int, period: int, octaves: int, rng: np.random.Generator) -> np.ndarray:
    """Octaves of value noise, normalised back to ``[0, 1]``."""
    total = np.zeros((size, size, size))
    amplitude = 1.0
    for octave in range(octaves):
        total += amplitude * (value_noise(size, period << octave, rng) - 0.5)
        amplitude *= 0.5
    total -= total.min()
    return total / max(total.max(), 1e-9)


def cellular(size: int, cells: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Tileable Worley F1 and F2 distances, in cell widths."""
    points = (np.indices((cells,) * 3).transpose(1, 2, 3, 0) + rng.random((cells,) * 3 + (3,)))
    points /= cells
    axis = (np.arange(size) + 0.5) / size
    grid = np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1)
    cell = np.floor(grid * cells).astype(int)
    f1 = np.full((size,) * 3, np.inf)
    f2 = np.full((size,) * 3, np.inf)
    for step in product((-1, 0, 1), repeat=3):
        neighbour = (cell + np.array(step)) % cells
        offset = points[neighbour[..., 0], neighbour[..., 1], neighbour[..., 2]] - grid
        offset -= np.round(offset)  # Shortest way round the torus.
        distance = np.linalg.norm(offset, axis=-1)
        closer = distance < f1
        f2 = np.where(closer, f1, np.minimum(f2, distance))
        f1 = np.where(closer, distance, f1)
    return f1 * cells, f2 * cells


def _smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def relief_volume(size: int = 64, cells: int = RELIEF_CELLS, seed: int = 7) -> np.ndarray:
    """``(size, size, size, 4)`` float32: xyz = height slope, w = smooth tone noise.

    Height is in cell widths, so the stored slope is unitless. Pores are
    Gaussian pits at the cell points, furrows follow the Voronoi edges between
    them, and both vary in depth with a low-frequency field so the pattern
    reads as skin rather than as a stamp.
    """
    rng = np.random.default_rng(seed)
    f1, f2 = cellular(size, cells, rng)
    variation = fbm(size, 2, 2, rng)
    pore_depth = 0.22 * (0.5 + 1.0 * variation)
    furrow_depth = 0.14 * (0.6 + 0.8 * (1.0 - variation))
    height = -pore_depth * np.exp(-((f1 / 0.2) ** 2))
    height -= furrow_depth * (1.0 - _smoothstep(0.0, 0.22, f2 - f1))
    height += 0.09 * (value_noise(size, cells * 2, rng) - 0.5)
    height += 0.045 * (value_noise(size, cells * 4, rng) - 0.5)
    spacing = cells / size
    gradient = [
        (np.roll(height, -1, axis) - np.roll(height, 1, axis)) / (2.0 * spacing)
        for axis in (2, 1, 0)  # Texture x is the last array axis.
    ]
    tone = fbm(size, 2, 3, rng)
    volume = np.stack([*gradient, tone], axis=-1)
    return np.ascontiguousarray(volume, dtype=np.float32)


def burley_profile(r: np.ndarray) -> np.ndarray:
    """Normalised diffusion profile for unit albedo and ``d = 1``."""
    r = np.maximum(r, 1e-9)
    return (np.exp(-r) + np.exp(-r / 3.0)) / (8.0 * np.pi * r)


def burley_marginal(x: np.ndarray, samples: int = 2048) -> np.ndarray:
    """The 2D profile integrated across one axis, so it can be used along a curve."""
    y = np.geomspace(1e-5, 80.0, samples)
    dy = np.gradient(y)
    r = np.sqrt(x[:, None] ** 2 + y[None, :] ** 2)
    return 2.0 * np.sum(burley_profile(r) * dy[None, :], axis=1)


def diffusion_lut(size: int = 64, steps: int = 1024) -> np.ndarray:
    """``(size, size, 4)`` float32, red = pre-integrated wrap for a sphere.

    Row ``v`` covers a sphere of radius ``2 ** (v * 8 - 2)`` diffusion lengths;
    column ``u`` covers ``cos(theta) = 2u - 1``. The last row is Lambert.
    """
    theta = np.arccos(np.linspace(-1.0, 1.0, size))
    x = (np.arange(steps) + 0.5) / steps * 2.0 * np.pi - np.pi
    cosine = np.maximum(np.cos(theta[:, None] + x[None, :]), 0.0)
    # The marginal has a logarithmic spike at zero, so tabulate it once on a
    # log axis and read the rows out of that rather than integrating each.
    knots = np.geomspace(1e-6, 400.0, 768)
    marginal = burley_marginal(knots)
    table = np.zeros((size, size, 4), np.float32)
    table[..., 3] = 1.0
    for row in range(size):
        radius = 2.0 ** (LUT_LOG_MIN + LUT_LOG_SPAN * row / (size - 1))
        distance = np.maximum(2.0 * radius * np.abs(np.sin(x * 0.5)), knots[0])
        kernel = np.interp(np.log(distance), np.log(knots), marginal)
        table[row, :, 0] = cosine @ kernel / kernel.sum()
    return np.clip(table, 0.0, 1.0)
