"""The film: the sums a render adds its samples into, and the passes read off them.

Each pixel keeps the sum of its samples' light and coverage, the sum of its
even-numbered samples' light (half the samples: the difference between the
two images is the noise), and how many it has taken.  Nothing is averaged
until it is shown or saved, so a pixel can take more samples at any time and
the picture refines in place.  The albedo, normal and depth the denoisers
guide themselves by are summed alongside, only when asked for.
"""

from __future__ import annotations

import numpy as np


class Film:
    def __init__(self, width: int, height: int, passes: bool = True) -> None:
        self.width = int(width)
        self.height = int(height)
        h, w = self.height, self.width
        self.rgba = np.zeros((h, w, 4), np.float32)
        self.even = np.zeros((h, w, 3), np.float32)
        self.count = np.zeros((h, w), np.int32)
        self.converged = np.zeros((h, w), np.uint8)
        self.passes = bool(passes)
        if passes:
            self.albedo = np.zeros((h, w, 3), np.float32)
            self.normal = np.zeros((h, w, 3), np.float32)
            self.depth = np.zeros((h, w), np.float32)
        else:
            self.albedo = np.zeros((0, 0, 3), np.float32)
            self.normal = np.zeros((0, 0, 3), np.float32)
            self.depth = np.zeros((0, 0), np.float32)

    @property
    def memory_bytes(self) -> int:
        return sum(a.nbytes for a in (self.rgba, self.even, self.count, self.converged,
                                      self.albedo, self.normal, self.depth))

    def _mean(self, sums: np.ndarray) -> np.ndarray:
        n = np.maximum(self.count, 1).astype(np.float32)
        return sums / (n[..., None] if sums.ndim == 3 else n)

    def beauty(self) -> np.ndarray:
        """Linear radiance and coverage per pixel, ``(h, w, 4)`` float32, premultiplied."""
        return self._mean(self.rgba)

    def albedo_pass(self) -> np.ndarray | None:
        return self._mean(self.albedo) if self.passes else None

    def normal_pass(self) -> np.ndarray | None:
        """World-space normals of the first surface, unit length where there is one."""
        if not self.passes:
            return None
        n = self._mean(self.normal)
        length = np.linalg.norm(n, axis=-1, keepdims=True)
        return np.where(length > 1e-6, n / np.maximum(length, 1e-6), 0.0).astype(np.float32)

    def depth_pass(self) -> np.ndarray | None:
        """Distance of the first surface along the view, 0 where there is none."""
        if not self.passes:
            return None
        coverage = self._mean(self.rgba[..., 3])
        depth = self._mean(self.depth)
        return np.where(coverage > 1e-6, depth / np.maximum(coverage, 1e-6), 0.0).astype(
            np.float32)

    def samples_pass(self) -> np.ndarray:
        return self.count.copy()

    def clear(self) -> None:
        for array in (self.rgba, self.even, self.count, self.converged, self.albedo, self.normal,
                      self.depth):
            array.fill(0)
