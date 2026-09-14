"""The matcap itself, as the control for grading it.

A matcap is a picture of a sphere, and the sphere is the whole of what it
says: every direction the surface can face is somewhere on that disc, so a
model shaded with it can show you nothing the disc does not already show.
Which makes the row of sliders a strange way to have gone about it.  Rotation,
gamma, brightness, contrast, saturation -- five numbers, five rows, and the
thing all five of them are describing sitting in a gallery two inches above,
not participating.

So the disc is the control.  It is drawn with the grading applied, at the size
of a thumbnail, and it is dragged: round to turn it, across to brighten or
warm it.  What you are adjusting is what you are looking at, which is how the
adjustment is judged anyway -- nobody has ever wanted a gamma of 1.2, they
have wanted the shadows to come up a little.

What is drawn here is exactly what the shader does, arrived at twice.  For a
sphere facing the camera the reflection lookup in
:func:`~refview.render.shaders.sampleMatcap` collapses to sampling the texture
at the surface normal's own ``xy``, halved and centred -- so the disc is the
matcap image, turned, and there is no approximation anywhere in it.  The
grading below is :func:`gradeMatcap` transcribed into numpy, in the same order
and with the same clamps, because a preview that grades differently from the
renderer is worse than no preview.

The gestures are three, and which one you get is chosen with a modifier rather
than a mode, because a mode is a thing you have to remember you are in:

``drag``
    Turns the matcap under your hand.  The angle is taken from the centre, so
    the picture follows the cursor round rather than tracking a distance.
``shift + drag``
    Brightness across, contrast up and down -- the two that do most of the
    work, on the gesture that needs no aiming.
``ctrl + drag``
    Saturation across, gamma up and down.

Alt is deliberately not used: Alt and a drag copies a control out of its
panel, and that has to keep working here like everywhere else.
"""

from __future__ import annotations

import math

import numpy as np
from PySide6.QtCore import QPoint, QRect, QSize, Qt, Signal
from PySide6.QtGui import QImage, QPainter, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from ..core.settings import MatcapSettings
from ..render.texture import default_matcap_pixels
from .elements import palette
from .elements.clone import register_cloner

#: The smallest the disc is drawn, and the largest.  Below the floor the
#: highlight is a few pixels across and there is nothing to judge; above the
#: ceiling it is taking room from the gallery of matcaps above it, which is
#: the control you use more often.
MIN_SIZE = 110
MAX_SIZE = 240

#: Room under the disc for the line that says what a drag is doing.
LEGEND_HEIGHT = 16

#: What a drag of the whole width of the widget is worth, for each of the four
#: grades that are set by distance rather than by angle.  Roughly the range
#: the sliders offered, so a full sweep covers it and an inch does not.
_SPAN = {
    "brightness": 2.0,
    "contrast": 2.0,
    "saturation": 2.0,
    "gamma": 2.0,
}

#: What each grade may be set to.  The same limits the sliders had, so that
#: the two cannot disagree about what is reachable.
_LIMITS = {
    "brightness": (0.0, 3.0),
    "contrast": (0.0, 3.0),
    "saturation": (0.0, 3.0),
    "gamma": (0.1, 3.0),
}

#: Degrees per wheel notch, and the finer step with Ctrl held.
_WHEEL_STEP = 5.0
_WHEEL_FINE = 1.0

#: The luminance weights the shader grades saturation against.
_LUMA = np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)


def grade(rgb: np.ndarray, settings: MatcapSettings) -> np.ndarray:
    """Apply the matcap grading to float RGB in 0-1, as the shader does.

    A transcription of ``gradeMatcap``, kept in the same order: gamma, then
    contrast about the mid grey, then saturation towards the luminance, then
    brightness and the tint together.  The order is not arbitrary and is not
    ours to change -- it is what the renderer does, and this exists to agree
    with the renderer.
    """
    out = np.power(np.maximum(rgb, 0.0), 1.0 / max(settings.gamma, 0.01))
    out = (out - 0.5) * settings.contrast + 0.5
    luma = out @ _LUMA
    out = luma[..., None] + (out - luma[..., None]) * settings.saturation
    tint = np.asarray(settings.tint, dtype=np.float32)
    return np.maximum(out * settings.brightness * tint, 0.0)


def sample(pixels: np.ndarray, settings: MatcapSettings, size: int) -> np.ndarray:
    """Draw the matcap onto a sphere of ``size`` pixels, graded.

    Returns ``(size, size, 4)`` uint8 with the corners outside the sphere left
    transparent.  ``pixels`` is the array the renderer uploads -- rows running
    from the bottom of the picture up, because that is the way round OpenGL
    samples -- and is read here in exactly that orientation, so that the disc
    is never accidentally the other way up from the model.
    """
    axis = (np.arange(size, dtype=np.float32) + 0.5) / size * 2.0 - 1.0
    across = axis[None, :]
    # Row nought is the top of the widget and the top of the sphere, which is
    # where the normal's y is greatest.
    down = -axis[:, None]
    inside = across * across + down * down <= 1.0

    turn = math.radians(settings.rotation_deg)
    cos, sin = math.cos(turn), math.sin(turn)
    # The shader turns the lookup rather than the picture, so a positive angle
    # samples anticlockwise and the picture comes out turned the other way.
    u = (across * cos - down * sin) * 0.5 + 0.5
    v = (across * sin + down * cos) * 0.5 + 0.5
    if settings.flip_y:
        v = 1.0 - v

    height, width = pixels.shape[:2]
    columns = np.clip((u * width).astype(np.int32), 0, width - 1)
    rows = np.clip((v * height).astype(np.int32), 0, height - 1)
    rgb = pixels[rows, columns, :3].astype(np.float32) / 255.0

    graded = np.clip(grade(rgb, settings), 0.0, 1.0)
    out = np.zeros((size, size, 4), dtype=np.uint8)
    out[..., :3] = (graded * 255.0 + 0.5).astype(np.uint8)
    out[..., 3] = np.where(inside, 255, 0).astype(np.uint8)
    return out


class MatcapPreview(QWidget):
    """A matcap on a sphere, which is also how the matcap is graded."""

    #: A grade moved.  Emitted continuously through a drag, because the point
    #: of the thing is that the model follows your hand.
    changed = Signal()
    #: Where the drag came to rest, for anything that costs real work.
    committed = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._settings = MatcapSettings()
        self._pixels: np.ndarray | None = None
        self._image: QImage | None = None
        self._drawn_for: tuple | None = None
        self._drag: str | None = None
        self._last: QPoint | None = None
        self._saying = ""

        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.setMinimumSize(MIN_SIZE, MIN_SIZE + LEGEND_HEIGHT)
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.setToolTip(
            "Drag to turn the matcap.\n"
            "Shift-drag: brightness across, contrast up and down.\n"
            "Ctrl-drag: saturation across, gamma up and down.\n"
            "Double-click to put the grading back."
        )

    # -- what is being shown ---------------------------------------------

    def settings(self) -> MatcapSettings:
        return self._settings

    def set_settings(self, settings: MatcapSettings) -> None:
        """Point the preview at the settings it edits.

        The object itself, not a copy: this widget writes the numbers the
        renderer reads, the same way a slider does.  Re-pointed rather than
        merely refreshed because Reset Adjustments replaces the whole object.
        """
        self._settings = settings
        self._invalidate()

    def set_source(self, pixels: np.ndarray | None) -> None:
        """The matcap image, in the orientation the renderer uploads it.

        ``None`` for the built-in matcap, which is the one the viewport falls
        back to and so the one the disc has to show.
        """
        self._pixels = pixels
        self._invalidate()

    def refresh(self) -> None:
        """Redraw from the settings, which something else has changed."""
        self._invalidate()

    def _invalidate(self) -> None:
        self._drawn_for = None
        self.update()

    # -- gestures ---------------------------------------------------------

    def mousePressEvent(self, event) -> None:  # noqa: N802 - Qt contract
        if event.button() != Qt.MouseButton.LeftButton:
            super().mousePressEvent(event)
            return
        modifiers = event.modifiers()
        if modifiers & Qt.KeyboardModifier.AltModifier:
            # Alt-drag copies the control; it is not ours to swallow.
            event.ignore()
            return
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            self._drag = "light"
        elif modifiers & Qt.KeyboardModifier.ControlModifier:
            self._drag = "colour"
        else:
            self._drag = "turn"
        self._last = event.position().toPoint()
        self.setCursor(Qt.CursorShape.ClosedHandCursor)
        event.accept()

    def mouseMoveEvent(self, event) -> None:  # noqa: N802 - Qt contract
        if self._drag is None or self._last is None:
            super().mouseMoveEvent(event)
            return
        point = event.position().toPoint()
        if self._drag == "turn":
            self._turn(self._last, point)
        elif self._drag == "light":
            self._slide(self._last, point, "brightness", "contrast")
        else:
            self._slide(self._last, point, "saturation", "gamma")
        self._last = point
        self._invalidate()
        self.changed.emit()
        event.accept()

    def mouseReleaseEvent(self, event) -> None:  # noqa: N802 - Qt contract
        if self._drag is None:
            super().mouseReleaseEvent(event)
            return
        self._drag = None
        self._last = None
        self._saying = ""
        self.setCursor(Qt.CursorShape.OpenHandCursor)
        self.update()
        self.committed.emit()
        event.accept()

    def mouseDoubleClickEvent(self, event) -> None:  # noqa: N802 - Qt contract
        """Put the grading back, which is the one thing a disc cannot show."""
        if event.button() != Qt.MouseButton.LeftButton:
            super().mouseDoubleClickEvent(event)
            return
        fresh = MatcapSettings()
        for name in ("rotation_deg", "contrast", "gamma", "brightness", "saturation"):
            setattr(self._settings, name, getattr(fresh, name))
        self._say("Grading reset")
        self._invalidate()
        self.changed.emit()
        self.committed.emit()
        event.accept()

    def wheelEvent(self, event) -> None:  # noqa: N802 - Qt contract
        notches = event.angleDelta().y() / 120.0
        if not notches:
            super().wheelEvent(event)
            return
        fine = bool(event.modifiers() & Qt.KeyboardModifier.ControlModifier)
        step = _WHEEL_FINE if fine else _WHEEL_STEP
        self._set_rotation(self._settings.rotation_deg + notches * step)
        self._invalidate()
        self.changed.emit()
        self.committed.emit()
        event.accept()

    # -- what the gestures do ---------------------------------------------

    def _turn(self, was: QPoint, now: QPoint) -> None:
        """Turn the matcap by the angle the cursor swept about the centre.

        By angle and not by distance, so the picture stays under the hand all
        the way round.  A drag that starts on the centre pixel has no angle to
        report and is ignored rather than jumping.
        """
        centre = self._disc().center()
        before = _angle(was, centre)
        after = _angle(now, centre)
        if before is None or after is None:
            return
        # The picture turns against the lookup, so the number moves against
        # the cursor for the picture to move with it.
        self._set_rotation(self._settings.rotation_deg - math.degrees(_wrapped(after - before)))
        self._say("Rotation", self._settings.rotation_deg, "deg")

    def _slide(self, was: QPoint, now: QPoint, across: str, upward: str) -> None:
        """Two grades on one drag: one along each axis of the movement.

        Both move together -- a diagonal drag changes both, which is what a
        diagonal drag should do.  Only one of them can be written under the
        disc, so the one that moved furthest gets the line.
        """
        span = max(self.width(), 1)
        sideways = now.x() - was.x()
        # Up is more, which is the way round every other control in the
        # application reads and the opposite of the way Qt counts pixels.
        upwards = was.y() - now.y()
        told = None
        if sideways:
            told = self._nudge(across, sideways / span * _SPAN[across])
        if upwards:
            changed = self._nudge(upward, upwards / span * _SPAN[upward])
            if told is None or abs(upwards) >= abs(sideways):
                told = changed
        if told is not None:
            self._say(*told)

    def _nudge(self, name: str, amount: float) -> tuple[str, float]:
        low, high = _LIMITS[name]
        value = min(max(getattr(self._settings, name) + amount, low), high)
        setattr(self._settings, name, value)
        return name.title(), value

    def _set_rotation(self, degrees: float) -> None:
        """Keep the angle in -180 to 180, the range the setting is stored in."""
        turned = (degrees + 180.0) % 360.0 - 180.0
        self._settings.rotation_deg = turned
        self._say("Rotation", turned, "deg")

    def _say(self, name: str, value: float | None = None, suffix: str = "") -> None:
        if value is None:
            self._saying = name
        elif suffix:
            self._saying = f"{name}  {value:.0f}{suffix}"
        else:
            self._saying = f"{name}  {value:.2f}"

    # -- drawing ----------------------------------------------------------

    def _disc(self) -> QRect:
        """Where the sphere goes: square, centred, above the legend."""
        side = max(
            MIN_SIZE,
            min(self.width(), self.height() - LEGEND_HEIGHT, MAX_SIZE),
        )
        left = (self.width() - side) // 2
        return QRect(left, 0, side, side)

    def _built(self, side: int) -> QImage | None:
        """The graded disc at ``side`` pixels, rebuilt only when it has to be.

        A drag changes one number and asks for a repaint, and Qt asks for
        rather more repaints than that.  The key is everything the picture
        depends on, so an expose event costs nothing and a moved slider costs
        one pass over a disc the size of a thumbnail.
        """
        settings = self._settings
        source = self._pixels
        key = (
            side,
            id(source),
            None if source is None else source.shape,
            settings.rotation_deg,
            settings.contrast,
            settings.gamma,
            settings.brightness,
            settings.saturation,
            tuple(settings.tint),
            settings.flip_y,
        )
        if self._drawn_for == key and self._image is not None:
            return self._image
        if source is None:
            source = default_matcap_pixels()
        if source.ndim != 3 or source.shape[2] < 3:
            return None
        pixels = np.ascontiguousarray(sample(source, settings, side))
        # Copied off the array at once: a QImage does not take a reference to
        # the buffer it is handed, and this one goes out of scope on the next
        # line.
        self._image = QImage(
            pixels.data, side, side, side * 4, QImage.Format.Format_RGBA8888
        ).copy()
        self._drawn_for = key
        return self._image

    def paintEvent(self, event) -> None:  # noqa: N802 - Qt contract
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        disc = self._disc()
        image = self._built(disc.width())
        if image is not None:
            painter.drawImage(disc, image)
        painter.setPen(QPen(palette.EDGE if self.isEnabled() else palette.WELL, 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(disc.adjusted(0, 0, -1, -1))

        painter.setPen(palette.ACCENT if self._saying else palette.INK_DIM)
        painter.drawText(
            QRect(0, disc.bottom() + 1, self.width(), LEGEND_HEIGHT - 1),
            Qt.AlignmentFlag.AlignCenter,
            self._saying or "drag turn · shift light · ctrl colour",
        )

    def hasHeightForWidth(self) -> bool:  # noqa: N802 - Qt contract
        return True

    def heightForWidth(self, width: int) -> int:  # noqa: N802 - Qt contract
        return min(max(width, MIN_SIZE), MAX_SIZE) + LEGEND_HEIGHT

    def sizeHint(self) -> QSize:  # noqa: N802 - Qt contract
        return QSize(MAX_SIZE, MAX_SIZE + LEGEND_HEIGHT)

    def minimumSizeHint(self) -> QSize:  # noqa: N802 - Qt contract
        return QSize(MIN_SIZE, MIN_SIZE + LEGEND_HEIGHT)

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt contract
        # The height has to follow the width for the disc to stay round, and
        # a form row will not ask unless it is told the answer has changed.
        self.setFixedHeight(self.heightForWidth(self.width()))
        super().resizeEvent(event)

    def source_pixels(self):
        """The matcap image this is drawing, for a copy of it to draw too."""
        return self._pixels

    def caption(self) -> str:
        """What a copy of this is called when it is dropped into a panel."""
        return "Matcap"


def _angle(point: QPoint, centre: QPoint) -> float | None:
    """The angle of ``point`` about ``centre``, anticlockwise with y upwards."""
    across = point.x() - centre.x()
    up = centre.y() - point.y()
    if across == 0 and up == 0:
        return None
    return math.atan2(up, across)


def _wrapped(radians: float) -> float:
    """An angle difference brought back into -pi to pi."""
    return (radians + math.pi) % (2.0 * math.pi) - math.pi


# ----------------------------------------------------------------------
# Copying one out into a panel of the artist's own
# ----------------------------------------------------------------------
#
# Registered from here rather than from the copier, because the copier sits
# underneath this module and has no business importing back up.  A copy is
# unusually cheap to make honest: it is pointed at the same settings object,
# so a drag on either disc moves the same numbers, and all the link has to
# carry is the news that they moved.


def _clone_preview(source: MatcapPreview) -> QWidget:
    copy = MatcapPreview()
    copy.set_settings(source.settings())
    copy.set_source(source.source_pixels())
    return copy


def _push_preview(copy: MatcapPreview, source: MatcapPreview) -> None:
    # The copy writes the settings directly; what the original needs is to
    # hear about it, so that the renderer and the numbers under the disc are
    # brought along by a drag on either of them.
    copy.changed.connect(source.changed.emit)
    copy.committed.connect(source.committed.emit)


def _pull_preview(copy: MatcapPreview, source: MatcapPreview) -> None:
    if copy.settings() is not source.settings():
        copy.set_settings(source.settings())
    if copy.source_pixels() is not source.source_pixels():
        copy.set_source(source.source_pixels())
    # Cheap: the disc is only redrawn when something it depends on moved, and
    # the cache works that out for itself.
    copy.update()


register_cloner(MatcapPreview, _clone_preview, _push_preview, _pull_preview)
