"""The path tracer's random numbers: Owen-scrambled Sobol."""

from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("numba")

from refview.trace.sampler import (  # noqa: E402
    SOBOL_DIRECTIONS,
    hash32,
    nested_uniform_scramble,
    pixel_seed,
    reverse_bits,
    sample4,
)


def test_direction_numbers_are_sobols():
    # The second dimension's well-known first entries.
    assert [int(v) for v in SOBOL_DIRECTIONS[1][:8]] == [
        0x80000000, 0xC0000000, 0xA0000000, 0xF0000000,
        0x88000000, 0xCC000000, 0xAA000000, 0xFF000000,
    ]
    assert [int(v) for v in SOBOL_DIRECTIONS[0][:3]] == [0x80000000, 0x40000000, 0x20000000]


def test_bit_tricks():
    assert reverse_bits(1) == 0x80000000
    assert reverse_bits(reverse_bits(0x12345678)) == 0x12345678
    assert 0 <= hash32(12345) <= 0xFFFFFFFF
    assert hash32(1) != hash32(2)
    # Scrambling permutes: distinct inputs stay distinct.
    outs = {nested_uniform_scramble(i << 24, 99) for i in range(256)}
    assert len(outs) == 256


def test_samples_are_in_the_unit_interval_and_stratified():
    points = np.array([sample4(pixel_seed(3, 4, 0), i, 5) for i in range(256)])
    assert points.min() >= 0.0 and points.max() < 1.0
    # The first two dimensions are a (0, 2)-sequence: 256 points, one per cell of 16 x 16.
    cells = {tuple(c) for c in (points[:, :2] * 16).astype(int)}
    assert len(cells) == 256
    # Every dimension on its own is stratified too.
    for d in range(4):
        assert len(set((points[:, d] * 256).astype(int))) == 256


def test_pixels_and_dimension_sets_are_decorrelated():
    a = np.array([sample4(pixel_seed(0, 0, 0), i, 1) for i in range(64)])
    b = np.array([sample4(pixel_seed(1, 0, 0), i, 1) for i in range(64)])
    c = np.array([sample4(pixel_seed(0, 0, 0), i, 2) for i in range(64)])
    for other in (b, c):
        corr = np.corrcoef(a[:, 0], other[:, 0])[0, 1]
        assert abs(corr) < 0.4
        assert not np.allclose(a, other)


def test_a_sample_depends_only_on_its_pixel_index_and_seed():
    assert sample4(pixel_seed(7, 9, 3), 17, 4) == sample4(pixel_seed(7, 9, 3), 17, 4)
    assert sample4(pixel_seed(7, 9, 3), 17, 4) != sample4(pixel_seed(7, 9, 4), 17, 4)
