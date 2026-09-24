"""The built-in denoiser: an edge-avoiding a-trous wavelet filter (Dammertz et al. 2010).

It needs nothing but the render itself, so it works everywhere.  The light
is first divided by the surface's albedo, so the filter smooths the lighting
and not the texture -- pores and freckles come back sharp when it is
multiplied again.  Then a 5 by 5 blur is applied a few times, its taps
twice as far apart each time, and each tap is weighed down wherever it
crosses an edge: a turn of the normal, a jump in depth, or a difference in
light larger than the noise there is expected to be.  The noise is known
per pixel, from the difference between the image of all its samples and of
the even-numbered half.

It is far less capable than a trained network, but it is quick, and it
never invents detail.
"""

from __future__ import annotations

import math

import numpy as np

from .jit import kernel

_WEIGHTS = np.array([1.0 / 16.0, 1.0 / 4.0, 3.0 / 8.0, 1.0 / 4.0, 1.0 / 16.0])


@kernel
def _pass(src, dst, normal, depth, sigma, step, sigma_n, sigma_z, sigma_l, y0, y1):
    h = src.shape[0]
    w = src.shape[1]
    for y in range(y0, y1):
        for x in range(w):
            lp = 0.2126 * src[y, x, 0] + 0.7152 * src[y, x, 1] + 0.0722 * src[y, x, 2]
            npx = normal[y, x, 0]
            npy = normal[y, x, 1]
            npz = normal[y, x, 2]
            zp = depth[y, x]
            sp = sigma[y, x] * sigma_l + 1e-6
            acc0 = 0.0
            acc1 = 0.0
            acc2 = 0.0
            total = 0.0
            for j in range(-2, 3):
                yy = min(max(y + j * step, 0), h - 1)
                for i in range(-2, 3):
                    xx = min(max(x + i * step, 0), w - 1)
                    k = _WEIGHTS[j + 2] * _WEIGHTS[i + 2]
                    dn = npx * normal[yy, xx, 0] + npy * normal[yy, xx, 1] + npz * normal[yy, xx, 2]
                    wn = max(dn, 0.0) ** sigma_n
                    wz = math.exp(-abs(zp - depth[yy, xx]) / (sigma_z * step + 1e-6))
                    lq = 0.2126 * src[yy, xx, 0] + 0.7152 * src[yy, xx, 1] + 0.0722 * src[yy, xx, 2]
                    wl = math.exp(-abs(lp - lq) / sp)
                    wgt = k * wn * wz * wl
                    acc0 += src[yy, xx, 0] * wgt
                    acc1 += src[yy, xx, 1] * wgt
                    acc2 += src[yy, xx, 2] * wgt
                    total += wgt
            if total > 0.0:
                dst[y, x, 0] = acc0 / total
                dst[y, x, 1] = acc1 / total
                dst[y, x, 2] = acc2 / total
            else:
                dst[y, x, 0] = src[y, x, 0]
                dst[y, x, 1] = src[y, x, 1]
                dst[y, x, 2] = src[y, x, 2]


def atrous(color: np.ndarray, albedo: np.ndarray | None, normal: np.ndarray | None,
           depth: np.ndarray | None, noise: np.ndarray | None, passes: int = 5,
           pool=None) -> np.ndarray:
    """``(h, w, 3)`` light in, smoothed light out.

    ``noise`` is the expected error of each pixel's value, as a luminance;
    without it the filter falls back to the local contrast.
    """
    color = np.ascontiguousarray(color[..., :3], dtype=np.float32)
    h, w = color.shape[:2]
    if albedo is not None:
        demod = np.maximum(np.asarray(albedo, np.float32)[..., :3], 0.02)
        src = color / demod
    else:
        demod = None
        src = color.copy()
    src = np.ascontiguousarray(src, dtype=np.float32)
    normal = (np.ascontiguousarray(normal, dtype=np.float32) if normal is not None
              else np.dstack([np.zeros((h, w, 2), np.float32), np.ones((h, w, 1), np.float32)]))
    depth = (np.ascontiguousarray(depth, dtype=np.float32) if depth is not None
             else np.zeros((h, w), np.float32))
    if noise is None:
        lum = src @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        noise = np.full((h, w), float(np.std(lum)) * 0.5 + 1e-4, np.float32)
    else:
        noise = np.asarray(noise, np.float32)
        if demod is not None:
            noise = noise / (demod @ np.array([0.2126, 0.7152, 0.0722], np.float32))
    sigma = np.ascontiguousarray(np.maximum(noise, 1e-4), dtype=np.float32)
    span = float(np.ptp(depth[depth > 0])) if np.any(depth > 0) else 1.0
    sigma_z = max(span * 0.01, 1e-6)
    dst = np.empty_like(src)
    for index in range(max(int(passes), 1)):
        step = 1 << index
        bands = [(y, min(y + 32, h)) for y in range(0, h, 32)]
        if pool is not None:
            futures = [pool.submit(_pass, src, dst, normal, depth, sigma, step, 64.0, sigma_z,
                                   4.0, y0, y1) for y0, y1 in bands]
            for future in futures:
                future.result()
        else:
            for y0, y1 in bands:
                _pass(src, dst, normal, depth, sigma, step, 64.0, sigma_z, 4.0, y0, y1)
        src, dst = dst, src
        # Each pass has smoothed the noise it was told to expect.
        sigma = sigma * 0.5
    return src * demod if demod is not None else src
