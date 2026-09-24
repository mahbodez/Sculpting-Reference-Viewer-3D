"""From scene light to pixel values: exposure, the view transform, and the encoding.

The film holds light as the scene has it, unbounded; a screen and a PNG hold
values from nought to one.  Developing a picture is, in order: scale by the
exposure; push the midtones apart or together about middle grey (contrast);
roll the highlights off with the view transform; encode for the screen
(sRGB); apply the display gamma; and lay the result over the background --
the viewport's gradient, drawn in display values as the viewport draws it --
unless the background is to be left transparent.

The transforms:

* **Standard** clips at one, as a plain sRGB conversion does;
* **Neutral** is Khronos' PBR Neutral: colours stay as they were up to
  about 0.8 and only the highlights are compressed, desaturating as they go;
* **Filmic** is Narkowicz's fit of the ACES film curve: a toe and a
  shoulder, with contrast of its own;
* **Reinhard**, ``x / (1 + x)``, is what Human Skin develops with on screen,
  so a skin render under it matches the viewport.

Developing is quick and needs no re-render, so the Render Window changes the
exposure and the transform on a finished film at once.
"""

from __future__ import annotations

import math

import numpy as np

from ..core.path_trace import ViewTransform
from .jit import device, kernel

TRANSFORM_CODES = {
    ViewTransform.STANDARD: 0,
    ViewTransform.NEUTRAL: 1,
    ViewTransform.FILMIC: 2,
    ViewTransform.REINHARD: 3,
}


@device
def _encode(c):
    c = max(c, 0.0)
    if c <= 0.0031308:
        return 12.92 * c
    return 1.055 * c ** (1.0 / 2.4) - 0.055


@device
def _aces(x):
    return min(max((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0.0), 1.0)


@device
def _neutral(r, g, b):
    start = 0.8 - 0.04
    desaturation = 0.15
    x = min(r, min(g, b))
    offset = x - 6.25 * x * x if x < 0.08 else 0.04
    r -= offset
    g -= offset
    b -= offset
    peak = max(r, max(g, b))
    if peak < start:
        return r, g, b
    d = 1.0 - start
    new_peak = 1.0 - d * d / (peak + d - start)
    k = new_peak / peak
    r *= k
    g *= k
    b *= k
    gray = 1.0 - 1.0 / (desaturation * (peak - new_peak) + 1.0)
    return r + (new_peak - r) * gray, g + (new_peak - g) * gray, b + (new_peak - b) * gray


@device
def develop(r, g, b, transform, exposure, gamma, contrast):
    """Scene-linear rgb to display values in [0, 1]."""
    r = max(r, 0.0) * exposure
    g = max(g, 0.0) * exposure
    b = max(b, 0.0) * exposure
    if contrast != 0.0:
        k = 1.0 + contrast
        r = 0.18 * (r / 0.18) ** k
        g = 0.18 * (g / 0.18) ** k
        b = 0.18 * (b / 0.18) ** k
    if transform == 1:
        r, g, b = _neutral(r, g, b)
    elif transform == 2:
        r, g, b = _aces(r), _aces(g), _aces(b)
    elif transform == 3:
        r, g, b = r / (1.0 + r), g / (1.0 + g), b / (1.0 + b)
    r = _encode(min(max(r, 0.0), 1.0))
    g = _encode(min(max(g, 0.0), 1.0))
    b = _encode(min(max(b, 0.0), 1.0))
    if gamma != 1.0:
        inv = 1.0 / gamma
        r = r ** inv
        g = g ** inv
        b = b ** inv
    return r, g, b


@kernel
def develop_region(sums, count, out, x0, y0, x1, y1, transform, exposure, gamma, contrast,
                   top, bottom, transparent, background):
    """Develop a rectangle of the film into ``out``, ``(h, w, 4)`` float32 display values.

    ``sums`` hold premultiplied light and coverage; ``count`` divides them
    (ones for an image already averaged).  An unsampled pixel is background.
    With ``background`` the viewport's gradient is laid under the picture
    (``top``/``bottom``, display values); with ``transparent`` it is not and
    the alpha is kept.
    """
    height = out.shape[0]
    for y in range(y0, y1):
        t = 1.0 - (y + 0.5) / height
        bg_r = bottom[0] + (top[0] - bottom[0]) * t
        bg_g = bottom[1] + (top[1] - bottom[1]) * t
        bg_b = bottom[2] + (top[2] - bottom[2]) * t
        for x in range(x0, x1):
            n = count[y, x]
            if n <= 0:
                if transparent or not background:
                    out[y, x, 0] = 0.0
                    out[y, x, 1] = 0.0
                    out[y, x, 2] = 0.0
                    out[y, x, 3] = 0.0
                else:
                    out[y, x, 0] = bg_r
                    out[y, x, 1] = bg_g
                    out[y, x, 2] = bg_b
                    out[y, x, 3] = 1.0
                continue
            inv = 1.0 / n
            a = min(max(sums[y, x, 3] * inv, 0.0), 1.0)
            r = sums[y, x, 0] * inv
            g = sums[y, x, 1] * inv
            b = sums[y, x, 2] * inv
            if transparent:
                if a > 1e-6:
                    r, g, b = develop(r / a, g / a, b / a, transform, exposure, gamma, contrast)
                else:
                    r, g, b = 0.0, 0.0, 0.0
                out[y, x, 0] = r
                out[y, x, 1] = g
                out[y, x, 2] = b
                out[y, x, 3] = a
                continue
            r, g, b = develop(r, g, b, transform, exposure, gamma, contrast)
            if background:
                r = r + bg_r * (1.0 - a)
                g = g + bg_g * (1.0 - a)
                b = b + bg_b * (1.0 - a)
                a = 1.0
            out[y, x, 0] = min(r, 1.0)
            out[y, x, 1] = min(g, 1.0)
            out[y, x, 2] = min(b, 1.0)
            out[y, x, 3] = a


@kernel
def quantize_region(display, out, x0, y0, x1, y1):
    """Display values to 8-bit RGBA, rounding to nearest."""
    for y in range(y0, y1):
        for x in range(x0, x1):
            for c in range(4):
                v = display[y, x, c] * 255.0 + 0.5
                out[y, x, c] = np.uint8(min(max(v, 0.0), 255.0))


def exposure_scale(stops: float) -> float:
    return float(2.0 ** float(stops))


def develop_image(rgba: np.ndarray, transform: int, stops: float, gamma: float, contrast: float,
                  top=(0.0, 0.0, 0.0), bottom=(0.0, 0.0, 0.0), transparent: bool = False,
                  background: bool = True) -> np.ndarray:
    """A whole averaged image ``(h, w, 4)`` developed to display values, ``(h, w, 4)`` float32."""
    rgba = np.ascontiguousarray(rgba, dtype=np.float32)
    h, w = rgba.shape[:2]
    out = np.zeros((h, w, 4), np.float32)
    ones = np.ones((h, w), np.int32)
    develop_region(rgba, ones, out, 0, 0, w, h, int(transform), exposure_scale(stops),
                   float(gamma), float(contrast), np.asarray(top, np.float64),
                   np.asarray(bottom, np.float64), bool(transparent), bool(background))
    return out


def to_rgba8(display: np.ndarray) -> np.ndarray:
    return np.clip(np.rint(display * 255.0), 0, 255).astype(np.uint8)


def to_rgba16(display: np.ndarray) -> np.ndarray:
    return np.clip(np.rint(display * 65535.0), 0, 65535).astype(np.uint16)


def linear_to_display(value: float) -> float:
    """The sRGB encoding of one linear value, for tests and the panel."""
    value = max(value, 0.0)
    return 12.92 * value if value <= 0.0031308 else 1.055 * math.pow(value, 1.0 / 2.4) - 0.055
