"""The render's frame: its size, where it sits in the view, and the camera that fills it.

A render seldom has the viewport's shape.  The frame is the render's shape
fitted inside the view -- as wide as the view with bars above and below
(letterboxed), or as tall with bars at the sides (pillarboxed) -- and the
safe-frame overlay shades everything outside it.  :func:`framed_camera`
turns the view's camera into the one that sees exactly what is inside that
frame, so a render never holds more or less than the frame promised.
"""

from __future__ import annotations

import math

from .camera import Camera
from .path_trace import OutputSettings

SIZE_MIN, SIZE_MAX = 16, 7680

#: The sizes offered by name.  ``None`` means "read it from the viewport".
OUTPUT_SIZES: tuple[tuple[str, int | None, int | None], ...] = (
    ("Viewport size", None, None),
    ("HD 720p", 1280, 720),
    ("Full HD 1080p", 1920, 1080),
    ("QHD 1440p", 2560, 1440),
    ("4K UHD", 3840, 2160),
    ("Square 1080", 1080, 1080),
    ("Square 2048", 2048, 2048),
    ("Portrait 4:5", 1080, 1350),
    ("Portrait 9:16", 1080, 1920),
    ("A4 portrait, 300 dpi", 2480, 3508),
    ("A4 landscape, 300 dpi", 3508, 2480),
)
CUSTOM_SIZE = "Custom"

Rect = tuple[float, float, float, float]


def preset_size(name: str, viewport: tuple[int, int]) -> tuple[int, int] | None:
    """The size a named preset stands for, or ``None`` for a name that is not one."""
    for label, width, height in OUTPUT_SIZES:
        if label == name:
            if width is None or height is None:
                return clamp_size(viewport[0]), clamp_size(viewport[1])
            return width, height
    return None


def clamp_size(value: float) -> int:
    return int(min(max(round(value), SIZE_MIN), SIZE_MAX))


def output_size(output: OutputSettings, viewport: tuple[int, int]) -> tuple[int, int]:
    """The render's size in pixels, with the scale applied.

    The "Viewport size" preset follows the viewport as it is resized, so the
    frame always fills the view.
    """
    size = None
    if output.size_preset != CUSTOM_SIZE:
        size = preset_size(output.size_preset, viewport)
    if size is None:
        size = (output.width, output.height)
    scale = max(float(output.scale), 1.0) / 100.0
    return clamp_size(size[0] * scale), clamp_size(size[1] * scale)


def frame_rect(view_width: float, view_height: float, width: int, height: int) -> Rect:
    """Where a ``width`` by ``height`` frame sits, centred and fitted, in the view."""
    view_width = max(float(view_width), 1.0)
    view_height = max(float(view_height), 1.0)
    aspect = max(width, 1) / max(height, 1)
    if aspect >= view_width / view_height:
        w, h = view_width, view_width / aspect
    else:
        w, h = view_height * aspect, view_height
    return (view_width - w) * 0.5, (view_height - h) * 0.5, w, h


def safe_rect(rect: Rect, fraction: float) -> Rect:
    """The part of ``rect`` that keeps ``fraction`` of its width and height, centred."""
    x, y, w, h = rect
    fraction = min(max(float(fraction), 0.0), 1.0)
    inset_x = w * (1.0 - fraction) * 0.5
    inset_y = h * (1.0 - fraction) * 0.5
    return x + inset_x, y + inset_y, w - 2.0 * inset_x, h - 2.0 * inset_y


def framed_camera(camera: Camera, view_width: float, view_height: float, width: int,
                  height: int) -> Camera:
    """The camera that sees what is inside the frame, for a ``width`` by ``height`` render.

    The view's camera fixes the vertical field of view across the whole view;
    a letterboxed frame is shorter than the view, so it sees a narrower field.
    A pillarboxed frame is as tall as the view and keeps the field as it is.
    The orthographic extent follows the field of view, so it narrows alike.
    """
    _x, _y, _w, h = frame_rect(view_width, view_height, width, height)
    result = camera.copy()
    share = h / max(float(view_height), 1.0)
    if share < 1.0 - 1e-9:
        half = math.tan(math.radians(camera.fov_deg) * 0.5) * share
        result.fov_deg = math.degrees(2.0 * math.atan(half))
    return result


def memory_estimate(width: int, height: int, passes: bool = True) -> int:
    """Roughly how many bytes a render of this size holds while it runs.

    The sums of light (four floats a pixel), the even-sample half used to
    measure noise (three), the sample counts and the done flags, and with
    ``passes`` the albedo, normal and depth the denoisers read (seven), and
    the displayed picture (four bytes).
    """
    pixels = int(width) * int(height)
    per_pixel = 4 * 4 + 3 * 4 + 4 + 1 + 4
    if passes:
        per_pixel += 7 * 4
    return pixels * per_pixel
