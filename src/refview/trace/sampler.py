"""Random numbers for the tracer: Owen-scrambled Sobol points, after Burley (2020).

Every random decision a path makes -- where in the pixel, which way to
bounce, which point of a light -- reads a number from a low-discrepancy
sequence rather than from a generator, so the first sixteen samples of a
pixel already cover the pixel, the light and the bounce hemisphere evenly.
Owen scrambling, done by hashing, keeps the sequence's evenness while making
every pixel's sequence independent of its neighbours', so what noise is left
is fine and without pattern.

A sample's numbers depend only on its pixel, its index and which decision
asks -- never on which thread traced it or in what order -- so a bucket
render and a progressive one of the same scene are the same picture, and a
seed changes the noise and nothing else.

The four dimensions of a :func:`sample4` call come from the first four Sobol
dimensions; separate calls are decorrelated by scrambling with a different
seed, which is Burley's padding.
"""

from __future__ import annotations

import numpy as np

from .jit import device

MASK32 = 0xFFFFFFFF
#: 2^-32, and the largest float below one, so a number is never exactly one.
_INV_2_32 = 1.0 / 4294967296.0
ONE_MINUS_EPSILON = 0.99999994

# Primitive polynomials and initial direction numbers for Sobol dimensions
# two to four (Joe and Kuo); the first dimension is van der Corput.
_JOE_KUO = ((1, 0, (1,)), (2, 1, (1, 3)), (3, 1, (1, 3, 1)))


def _direction_numbers() -> np.ndarray:
    table = np.zeros((4, 32), dtype=np.int64)
    for i in range(32):
        table[0, i] = 1 << (31 - i)
    for dim, (s, a, m) in enumerate(_JOE_KUO, start=1):
        v = [0] * 33
        for i in range(1, s + 1):
            v[i] = m[i - 1] << (32 - i)
        for i in range(s + 1, 33):
            v[i] = v[i - s] ^ (v[i - s] >> s)
            for k in range(1, s):
                v[i] ^= ((a >> (s - 1 - k)) & 1) * v[i - k]
        table[dim] = v[1:33]
    return table & MASK32


SOBOL_DIRECTIONS = _direction_numbers()


@device
def hash32(x):
    """A 32-bit integer hash (lowbias32, Wellons)."""
    x &= MASK32
    x ^= x >> 16
    x = (x * 0x7FEB352D) & MASK32
    x ^= x >> 15
    x = (x * 0x846CA68B) & MASK32
    x ^= x >> 16
    return x


@device
def hash_combine(seed, value):
    return hash32((seed ^ (value + 0x9E3779B9 + ((seed << 6) & MASK32) + (seed >> 2))) & MASK32)


@device
def reverse_bits(x):
    x &= MASK32
    x = ((x >> 1) & 0x55555555) | ((x & 0x55555555) << 1)
    x = ((x >> 2) & 0x33333333) | ((x & 0x33333333) << 2)
    x = ((x >> 4) & 0x0F0F0F0F) | ((x & 0x0F0F0F0F) << 4)
    x = ((x >> 8) & 0x00FF00FF) | ((x & 0x00FF00FF) << 8)
    x = ((x >> 16) & 0x0000FFFF) | ((x & 0x0000FFFF) << 16)
    return x & MASK32


@device
def _laine_karras(x, seed):
    x = (x + seed) & MASK32
    x ^= (x * 0x6C50B47C) & MASK32
    x ^= (x * 0xB82F1E52) & MASK32
    x ^= (x * 0xC7AFE638) & MASK32
    x ^= (x * 0x8D22F6E6) & MASK32
    return x


@device
def nested_uniform_scramble(x, seed):
    """Owen scrambling of a 32-bit fixed-point number, by hashing its reversed bits."""
    return reverse_bits(_laine_karras(reverse_bits(x), seed))


@device
def sobol32(index, dim):
    x = 0
    i = 0
    while index != 0:
        if index & 1:
            x ^= SOBOL_DIRECTIONS[dim, i]
        index >>= 1
        i += 1
    return x


@device
def to_unit(x):
    return min(float(x) * _INV_2_32, ONE_MINUS_EPSILON)


@device
def sample4(pixel_seed, index, dimension_set):
    """Four numbers in [0, 1) for sample ``index`` of a pixel, for one set of decisions."""
    seed = hash_combine(pixel_seed, dimension_set)
    shuffled = nested_uniform_scramble(index & MASK32, seed)
    a = nested_uniform_scramble(sobol32(shuffled, 0), hash_combine(seed, 0))
    b = nested_uniform_scramble(sobol32(shuffled, 1), hash_combine(seed, 1))
    c = nested_uniform_scramble(sobol32(shuffled, 2), hash_combine(seed, 2))
    d = nested_uniform_scramble(sobol32(shuffled, 3), hash_combine(seed, 3))
    return to_unit(a), to_unit(b), to_unit(c), to_unit(d)


@device
def pixel_seed(x, y, seed):
    return hash_combine(hash_combine(hash32(seed + 0x5BD1E995), x), y)


@device
def hash_float(a, b, c):
    """A number in [0, 1) from three integers, for decisions no sequence needs to stratify."""
    return to_unit(hash_combine(hash_combine(hash32(a), b), c))


# Dimension sets.  A path's decisions at each bounce read from their own sets,
# so adding a decision to one never shifts the numbers another reads.
DIM_CAMERA = 0          # pixel filter x, y; lens u, v
DIMS_PER_BOUNCE = 4
DIM_BSDF = 0            # lobe choice, direction u, v, Russian roulette
DIM_LIGHT = 1           # key u, v; fill u, v
DIM_ENV = 2             # HDRI u, v; subsurface axis, channel
DIM_SUBSURFACE = 3      # radius, angle, reservoir, transmission spare


@device
def bounce_set(bounce, which):
    return 1 + bounce * DIMS_PER_BOUNCE + which
