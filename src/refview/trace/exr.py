"""Writing a render as OpenEXR: the light as it is, and its passes as layers.

An EXR keeps the scene's light unbounded and linear, so a render can be
graded later without the banding an 8-bit PNG would bring.  The beauty is
the file's RGBA; the other passes go in as layers of their own
(``albedo.R``, ``normal.X``, ``depth.Z`` ...), which a compositor lists by
name.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np


def write_exr(path: str | Path, layers: dict[str, np.ndarray], half: bool = False) -> Path:
    """Write ``layers`` -- ``"RGBA"`` first, then passes by name -- to ``path``.

    Colour arrays are ``(h, w, 3)`` or ``(h, w, 4)``; a single channel is
    ``(h, w)``.  ``half`` stores 16-bit floats, which are plenty for a
    picture and half the size; depth and normals are kept in full floats.
    """
    import OpenEXR

    channels = {}
    for name, array in layers.items():
        array = np.ascontiguousarray(array)
        exact = name.startswith(("depth", "normal"))
        dtype = np.float16 if half and not exact else np.float32
        if array.ndim == 3 and name not in ("RGBA", "RGB"):
            suffix = "XYZ" if name == "normal" else "RGBA"
            for index in range(array.shape[2]):
                channels[f"{name}.{suffix[index]}"] = np.ascontiguousarray(
                    array[..., index], dtype=dtype)
        else:
            channels[name] = np.ascontiguousarray(array, dtype=dtype)
    header = {"compression": OpenEXR.ZIP_COMPRESSION, "type": OpenEXR.scanlineimage}
    path = Path(path)
    with OpenEXR.File(header, channels) as handle:
        handle.write(str(path))
    return path


def read_exr_channels(path: str | Path) -> dict[str, np.ndarray]:
    """Every channel of an EXR by name, as the file groups them; for tests."""
    import OpenEXR

    with OpenEXR.File(str(path)) as handle:
        return {name: np.array(channel.pixels) for name, channel in handle.channels().items()}
