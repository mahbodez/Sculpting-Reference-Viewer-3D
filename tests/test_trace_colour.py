"""Developing a render: exposure, view transforms, encoding, background."""

from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("numba")

from refview.core.path_trace import ViewTransform  # noqa: E402
from refview.trace.colour import (  # noqa: E402
    TRANSFORM_CODES,
    develop,
    develop_image,
    linear_to_display,
    to_rgba8,
    to_rgba16,
)

STANDARD = TRANSFORM_CODES[ViewTransform.STANDARD]
NEUTRAL = TRANSFORM_CODES[ViewTransform.NEUTRAL]
FILMIC = TRANSFORM_CODES[ViewTransform.FILMIC]
REINHARD = TRANSFORM_CODES[ViewTransform.REINHARD]


def test_reinhard_is_the_viewports_skin_curve():
    for x in (0.0, 0.1, 0.5, 1.0, 4.0, 50.0):
        expected = linear_to_display(x / (1.0 + x))
        assert develop(x, x, x, REINHARD, 1.0, 1.0, 0.0)[0] == pytest.approx(expected, abs=1e-12)


def test_standard_is_plain_srgb_and_clips():
    assert develop(0.18, 0.18, 0.18, STANDARD, 1.0, 1.0, 0.0)[0] == pytest.approx(
        linear_to_display(0.18))
    assert develop(5.0, 5.0, 5.0, STANDARD, 1.0, 1.0, 0.0)[0] == pytest.approx(1.0)
    assert develop(-1.0, 0.0, 0.0, STANDARD, 1.0, 1.0, 0.0)[0] == 0.0


def test_one_stop_is_twice_the_light():
    a = develop(0.1, 0.1, 0.1, STANDARD, 2.0, 1.0, 0.0)[0]
    assert a == pytest.approx(linear_to_display(0.2))


def test_neutral_keeps_the_midtones_and_rolls_off_the_highlights():
    mid = develop(0.3, 0.2, 0.1, NEUTRAL, 1.0, 1.0, 0.0)
    assert mid[0] > mid[1] > mid[2]
    assert develop(0.5, 0.5, 0.5, NEUTRAL, 1.0, 1.0, 0.0)[0] == pytest.approx(
        linear_to_display(0.5 - 0.04), abs=1e-3)
    highs = [develop(x, x, x, NEUTRAL, 1.0, 1.0, 0.0)[0] for x in (1.0, 4.0, 100.0)]
    assert highs == sorted(highs) and highs[-1] <= 1.0


def test_filmic_is_monotonic_and_bounded():
    values = [develop(x, x, x, FILMIC, 1.0, 1.0, 0.0)[0] for x in np.geomspace(1e-4, 1e3, 50)]
    assert np.all(np.diff(values) >= 0) and values[-1] <= 1.0


def test_contrast_pivots_on_middle_grey():
    grey = develop(0.18, 0.18, 0.18, STANDARD, 1.0, 1.0, 0.5)[0]
    assert grey == pytest.approx(linear_to_display(0.18))
    assert develop(0.05, 0.05, 0.05, STANDARD, 1.0, 1.0, 0.5)[0] < linear_to_display(0.05)


def test_the_background_fills_what_the_picture_leaves_uncovered():
    image = np.zeros((4, 2, 4), np.float32)
    image[:, 1] = (0.18, 0.18, 0.18, 1.0)
    out = develop_image(image, STANDARD, 0.0, 1.0, 0.0, top=(1.0, 0.0, 0.0),
                        bottom=(0.0, 0.0, 1.0))
    # The empty column is the gradient, red at the top and blue at the bottom.
    assert out[0, 0, 0] > out[3, 0, 0] and out[3, 0, 2] > out[0, 0, 2]
    assert (out[:, 0, 3] == 1.0).all()
    assert out[0, 1, 0] == pytest.approx(linear_to_display(0.18), abs=1e-6)
    transparent = develop_image(image, STANDARD, 0.0, 1.0, 0.0, transparent=True)
    assert transparent[0, 0, 3] == 0.0 and transparent[0, 1, 3] == 1.0


def test_quantizing():
    display = np.array([[[0.0, 0.5, 1.0, 1.0]]], np.float32)
    assert to_rgba8(display).tolist() == [[[0, 128, 255, 255]]]
    assert to_rgba16(display)[0, 0, 1] == 32768
