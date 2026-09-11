"""Handing the film of a form's making to someone who was not there.

The scrub slider is for the artist at the machine.  What the film is *for*,
though, is usually somebody else -- a student who needs to see that a figure
arrives as four masses before it arrives as a figure, a class that will watch
it once, a portfolio where nobody is going to be dragging a slider.  That
wants a file, and this is the window that makes one.

Two halves, kept apart on purpose:

How long it runs is asked for in seconds per stage rather than in frames per
second, because a stage of a film is not a frame of anything.  It is a step in
the making, it took the mode a second or two to build, and how long it should
be looked at is a judgement about reading a form -- a fifth of a second is
about the pace of a hand, half a second is a lesson, two seconds is a
slideshow of block-ins.  :mod:`refview.core.video` turns that into whatever
the container wants.

What it looks like is asked for separately, because a clip is not a
screenshot.  The readout naming a file and a triangle count earns its place
while you work and is clutter in something you send; the armature that told
the clay where the masses go has done its job before anyone presses play.  So
the helpers are listed and ticked here rather than being read off the
document, and the frames come out of the same renderer the viewport uses, at
whatever size was asked for -- an artist should not have to make the window
4K in order to export at it.

The whole of it runs off the event loop a frame at a time, with the encoding
on a thread behind a short queue.  Rendering a hundred stages at 4K is a
minute of work, and a minute of a frozen window with no way out of it is not
something to hand anybody.
"""

from __future__ import annotations

import queue
import typing
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
from PySide6.QtCore import QObject, Qt, QThread, QTimer, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressDialog,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ..core.settings import GHOST_MIN, RenderSettings, ShadingMode
from ..core.video import (
    HOLD_MAX,
    STAGE_MAX,
    STAGE_MIN,
    Quality,
    VideoError,
    VideoFormat,
    VideoSettings,
    open_writer,
    unavailable,
    written_by_ffmpeg,
)
from .overlay import OverlayParts
from .widgets import form_group

if typing.TYPE_CHECKING:  # pragma: no cover - import cost, not behaviour
    from collections.abc import Sequence

    from ..core.plane_film import Film, Stage
    from .viewport import Viewport

#: Sizes offered, as ``(label, width, height)``.  ``None`` for either means
#: "read it off the viewport", which is the two entries that keep the framing
#: exactly as the artist has been looking at it -- a taller or wider frame
#: than the window is not a crop, it is a different camera.
_SIZES: tuple[tuple[str, int | None, int | None], ...] = (
    ("Viewport size", None, None),
    ("Viewport shape, 1080 tall", None, 1080),
    ("1280 x 720", 1280, 720),
    ("1920 x 1080", 1920, 1080),
    ("2560 x 1440", 2560, 1440),
    ("3840 x 2160 (4K)", 3840, 2160),
)

#: Smallest and largest frame offered.  The top is where the drivers stop
#: giving out framebuffers on ordinary hardware.
SIZE_MIN, SIZE_MAX = 160, 7680

#: How wide the preview is drawn, in logical pixels.
_PREVIEW_WIDTH = 360

#: What an export that was called off reports.  A constant rather than a
#: sentence written twice, because the window tells these apart to decide
#: whether to say anything at all: an artist who pressed Cancel does not need
#: a dialog telling them that they pressed Cancel.
CANCELLED = "Export cancelled"


def even(value: int) -> int:
    """``value`` rounded down to a multiple of four.

    Two would do for H.264, which cannot take an odd dimension at all; four is
    taken because it also makes every row of a read-back frame land on a word
    boundary, and so saves a copy on the way to the encoder.
    """
    return max(int(value) // 4 * 4, 4)


def frame_bytes(image: QImage) -> bytes:
    """An image's pixels, packed tight, whatever padding Qt left on its rows.

    Qt pads every scanline out to a word, so a frame whose width is not a
    multiple of four carries bytes at the end of each row that are not
    picture.  An encoder handed those reads the frame as sheared.
    """
    width, height = image.width(), image.height()
    stride = image.bytesPerLine()
    tight = width * 3
    raw = np.frombuffer(memoryview(image.constBits()), dtype=np.uint8)
    raw = raw[: stride * height].reshape(height, stride)
    if stride == tight:
        return raw.tobytes()
    return np.ascontiguousarray(raw[:, :tight]).tobytes()


@dataclass(frozen=True)
class ExportLook:
    """What the frames are to look like, as against what they are of.

    Laid over the viewport's own settings rather than replacing them, so
    everything not named here -- the matcap and how it is graded, the light
    rig, the section cut, the colours -- comes out exactly as the artist left
    it.  What is named here is what someone sending a clip actually wants to
    decide separately from how they have been working.
    """

    width: int = 1920
    height: int = 1080
    #: Which shading model, or ``None`` to keep the viewport's.
    shading: ShadingMode | None = None
    ghost: bool = False
    ghost_opacity: float = 0.35
    wireframe: bool = False
    pedestal: bool = True
    #: Strokes painted on the surface.  Real geometry, so this one is a matter
    #: of what the renderer is handed rather than of what is drawn over it.
    annotations: bool = True
    measurements: bool = False
    armature: bool = False
    gizmo: bool = False
    readout: bool = False
    #: Burn which stage this is into the corner of every frame.
    caption: bool = True
    #: How many stages the film has, for that caption to count against.
    stage_count: int = 0

    @property
    def parts(self) -> OverlayParts:
        """Which of the things drawn over the model belong in the frames."""
        return OverlayParts(
            measurements=self.measurements,
            tools=False,  # nothing is being drawn while an export runs
            armature=self.armature,
            gizmo=self.gizmo,
            readout=self.readout,
        )

    def render_settings(self, base: RenderSettings) -> RenderSettings:
        """``base`` with this export's choices laid over it."""
        return replace(
            base,
            shading_mode=base.shading_mode if self.shading is None else self.shading,
            ghost=self.ghost,
            ghost_opacity=max(float(self.ghost_opacity), GHOST_MIN),
            show_wireframe=self.wireframe,
        )

    def caption_for(self, stage: Stage) -> str:
        """The line burned into the corner of the frame for ``stage``.

        Counted off the stage's own place in the film rather than off how far
        into the export it is, so that the preview -- which renders one stage
        on its own -- says which stage it really is rather than calling
        everything the first.
        """
        place = stage.index + 1
        where = f"{place}" if self.stage_count <= 0 else f"{place}/{self.stage_count}"
        detail = "" if stage.planes is None else f"  -  Detail {stage.planes}"
        return f"{where}  -  {stage.label}{detail}"


class _Encoder(QObject):
    """The encoding itself, living on a thread of its own.

    It takes frames off a short queue and writes them.  Short on purpose: the
    queue is the backpressure, so a slow encoder -- the built-in GIF writer on
    a large frame, say -- makes the renderer wait rather than making the
    machine hold a hundred uncompressed 4K frames in memory.
    """

    wrote = Signal(int)
    failed = Signal(str)
    done = Signal()

    def __init__(self, writer, frames: queue.Queue) -> None:
        super().__init__()
        self._writer = writer
        self._frames = frames
        self._stop = False

    def cancel(self) -> None:
        """Abandon the file.  Called from the GUI thread; see :meth:`run`."""
        self._stop = True

    def run(self) -> None:
        written = 0
        try:
            while True:
                item = self._frames.get()
                if self._stop or item is None:
                    break
                frame, seconds = item
                self._writer.add(frame, seconds)
                written += 1
                self.wrote.emit(written)
            if self._stop:
                self._writer.abort()
                self.done.emit()
                return
            self._writer.close()
        except VideoError as error:
            self._writer.abort()
            self.failed.emit(str(error))
            return
        except Exception as error:  # pragma: no cover - a writer that fell over
            self._writer.abort()
            self.failed.emit(f"{type(error).__name__}: {error}")
            return
        self.done.emit()


class FilmExport(QObject):
    """One export, rendered from the event loop and encoded behind it.

    The renderer runs on the GUI thread because that is where the graphics
    context lives, and there is no moving it: a second context sharing the
    first one's meshes would be a second copy of everything the scene holds.
    So instead the work is cut into single frames and let go of between each,
    which keeps the window answering -- including answering the Cancel button,
    which is the whole reason this is not one long loop.
    """

    #: Frames written, out of how many there are to write.
    progress = Signal(int, int)
    #: ``(succeeded, what to tell the artist)``.
    finished = Signal(bool, str)

    def __init__(
        self,
        viewport: Viewport,
        stages: Sequence[Stage],
        look: ExportLook,
        settings: VideoSettings,
        path: Path,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._viewport = viewport
        self._stages = list(stages)
        self._look = look
        self._settings = settings
        self._path = Path(path)
        self._images = None
        self._index = 0
        self._queue: queue.Queue = queue.Queue(maxsize=3)
        self._thread: QThread | None = None
        self._encoder: _Encoder | None = None
        self._timer = QTimer(self)
        self._timer.setInterval(0)
        self._timer.timeout.connect(self._tick)
        self._ended = False

    @property
    def total(self) -> int:
        return len(self._stages)

    def start(self) -> None:
        """Open the file and begin.  Any failure here is reported, not raised."""
        try:
            writer = open_writer(self._path, (self._look.width, self._look.height), self._settings)
        except VideoError as error:
            self._end(False, str(error))
            return
        try:
            self._prime(writer)
        except Exception as error:  # pragma: no cover - a driver that refused
            writer.abort()
            self._end(False, f"The frames could not be rendered: {error}")
            return

        self._encoder = _Encoder(writer, self._queue)
        self._thread = QThread(self)
        self._encoder.moveToThread(self._thread)
        self._thread.started.connect(self._encoder.run)
        self._encoder.wrote.connect(self._wrote)
        self._encoder.failed.connect(self._failed)
        self._encoder.done.connect(self._done)
        for signal in (self._encoder.done, self._encoder.failed):
            signal.connect(self._thread.quit)
        self._thread.start()

        self._images = self._viewport.stage_images(self._stages, self._look)
        self._timer.start()

    def cancel(self) -> None:
        """Stop where it is and leave no half-written file behind."""
        if self._ended:
            return
        self._timer.stop()
        self._close_images()
        if self._encoder is not None:
            self._encoder.cancel()
            # Something has to arrive for the thread to notice the flag, and
            # the queue may be full of frames it will now never write.
            self._drain()
            self._queue.put(None)
        else:  # pragma: no cover - cancelled before it started
            self._end(False, CANCELLED)

    def wait(self, milliseconds: int = 30_000) -> None:
        """Let the encoding thread finish, for shutdown.

        It calls off an export still in flight first, because the thread is
        not sitting in an event loop that :meth:`QThread.quit` could reach --
        it is blocked on the queue, and what wakes it is something arriving on
        that queue.  Waiting without cancelling would therefore wait the whole
        timeout out and then drop a still-running thread, which is the crash
        the waiting was for.
        """
        if self._thread is None:
            return
        if not self._ended:
            self.cancel()
        self._thread.quit()
        self._thread.wait(int(milliseconds))

    # -- the loop ---------------------------------------------------------

    def _prime(self, writer) -> None:
        """Offer the encoder the last stage before the first is written.

        Only the built-in GIF writer wants it, and what it wants it for is the
        palette: the colours of the *finished* form are the ones the whole
        clip should be fitted to, and it has no way to see them until they
        arrive.  ffmpeg reads the clip twice and needs no such favour.
        """
        if written_by_ffmpeg(self._settings.format) or not self._stages:
            return
        image = self._viewport.stage_image(self._stages[-1], self._look)
        writer.prime(frame_bytes(image))

    def _tick(self) -> None:
        if self._images is None or self._queue.full():
            return
        try:
            image = next(self._images)
        except StopIteration:
            self._timer.stop()
            self._images = None
            self._queue.put(None)
            return
        except Exception as error:  # pragma: no cover - a driver that gave up
            self._timer.stop()
            self._images = None
            self.cancel()
            self._end(False, f"The frames could not be rendered: {error}")
            return
        seconds = self._settings.seconds_at(self._index, self.total)
        self._queue.put((frame_bytes(image), seconds))
        self._index += 1

    def _drain(self) -> None:
        while True:
            try:
                self._queue.get_nowait()
            except queue.Empty:
                return

    def _close_images(self) -> None:
        if self._images is not None:
            self._images.close()  # runs the viewport's tidy-up
            self._images = None

    def _wrote(self, written: int) -> None:
        self.progress.emit(written, self.total)

    def _failed(self, message: str) -> None:
        self._timer.stop()
        self._close_images()
        self._end(False, message)

    def _done(self) -> None:
        self._timer.stop()
        self._close_images()
        if self._ended:
            return
        if self._index < self.total:
            self._end(False, CANCELLED)
            return
        self._end(True, str(self._path))

    def _end(self, ok: bool, message: str) -> None:
        if self._ended:
            return
        self._ended = True
        self.finished.emit(ok, message)


class ExportVideoDialog(QDialog):
    """Where an artist says how the film should be written out.

    Everything on the right changes the picture, and the picture is shown on
    the left as it changes -- the preview is a real frame, rendered through
    the same path the export will use, at the shape the export will have.  A
    dialog full of checkboxes whose effect you only find out about after
    waiting a minute for a file is a dialog people fill in twice.
    """

    def __init__(self, viewport: Viewport, film: Film, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Export Video")
        self.setModal(True)
        self._viewport = viewport
        # A copy, because the recorder may still be laying stages down behind
        # this window and a clip has to be of something that stopped moving.
        self._stages: list[Stage] = list(film.stages)
        self._complete = film.complete
        self._export: FilmExport | None = None

        self._build()
        self._preview_timer = QTimer(self)
        self._preview_timer.setSingleShot(True)
        self._preview_timer.setInterval(150)
        self._preview_timer.timeout.connect(self._draw_preview)
        self._changed()

    # -- construction -----------------------------------------------------

    def _build(self) -> None:
        self._preview = QLabel()
        self._preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._preview.setFrameShape(QFrame.Shape.StyledPanel)
        self._preview.setStyleSheet("background: #17181b;")
        self._preview.setFixedSize(_PREVIEW_WIDTH, _PREVIEW_WIDTH * 3 // 4)
        self._summary = QLabel()
        self._summary.setWordWrap(True)
        self._summary.setStyleSheet("color: #8f939b;")

        left = QVBoxLayout()
        left.setSpacing(8)
        left.addWidget(self._preview, 0, Qt.AlignmentFlag.AlignTop)
        left.addWidget(self._summary)
        left.addStretch(1)

        right = QVBoxLayout()
        right.setSpacing(8)
        for group in (self._film_group(), self._picture_group(), self._helpers_group(),
                      self._file_group()):
            right.addWidget(group)
        right.addStretch(1)

        columns = QHBoxLayout()
        columns.setSpacing(12)
        columns.addLayout(left, 1)
        columns.addLayout(right, 0)

        buttons = QDialogButtonBox()
        self._export_button = buttons.addButton(
            "Export...", QDialogButtonBox.ButtonRole.AcceptRole
        )
        buttons.addButton(QDialogButtonBox.StandardButton.Close)
        self._export_button.clicked.connect(self._begin)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(columns, 1)
        layout.addWidget(buttons)
        # Last, once every control exists: the first thing any of them does is
        # re-read all of them.
        self._connect()

    def _film_group(self):
        box, form = form_group("Timing")
        self._seconds = QDoubleSpinBox()
        self._seconds.setRange(STAGE_MIN, STAGE_MAX)
        self._seconds.setDecimals(2)
        self._seconds.setSingleStep(0.05)
        self._seconds.setValue(VideoSettings().seconds_per_stage)
        self._seconds.setSuffix(" s")
        self._seconds.setToolTip(
            "How long one stage of the making is held on screen. A fifth of a "
            "second is about the pace of a hand; half a second is a lesson"
        )
        self._hold = QDoubleSpinBox()
        self._hold.setRange(0.0, HOLD_MAX)
        self._hold.setDecimals(1)
        self._hold.setSingleStep(0.5)
        self._hold.setValue(VideoSettings().hold_last)
        self._hold.setSuffix(" s")
        self._hold.setToolTip(
            "Extra time on the last stage, over and above its own. A clip that "
            "cuts away the instant the form arrives never shows what was made"
        )
        form.addRow("Each stage", self._seconds)
        form.addRow("Hold the last", self._hold)
        return box

    def _picture_group(self):
        box, form = form_group("Picture")
        self._size = QComboBox()
        for label, width, height in _SIZES:
            self._size.addItem(label, (width, height))
        self._size.addItem("Custom", None)
        self._size.setCurrentIndex(3)
        self._width = QSpinBox()
        self._height = QSpinBox()
        for spin in (self._width, self._height):
            spin.setRange(SIZE_MIN, SIZE_MAX)
            spin.setSingleStep(4)
            spin.setSuffix(" px")
        self._shading = QComboBox()
        self._shading.addItem("As the viewport has it", None)
        for mode in ShadingMode:
            self._shading.addItem(mode.label, mode.value)
        self._ghost = QCheckBox("See through the form")
        self._ghost.setToolTip(
            "Draw the form see-through, which is how the wire inside it -- or "
            "the far side of it -- is seen at all"
        )
        self._ghost_opacity = QDoubleSpinBox()
        self._ghost_opacity.setRange(GHOST_MIN, 1.0)
        self._ghost_opacity.setDecimals(2)
        self._ghost_opacity.setSingleStep(0.05)
        self._ghost_opacity.setValue(RenderSettings().ghost_opacity)
        self._wireframe = QCheckBox("Wireframe over the form")
        self._pedestal = QCheckBox("Pedestal under the form")
        self._pedestal.setChecked(True)
        form.addRow("Size", self._size)
        form.addRow("Width", self._width)
        form.addRow("Height", self._height)
        form.addRow("Shading", self._shading)
        form.addRow("", self._ghost)
        form.addRow("Opacity", self._ghost_opacity)
        form.addRow("", self._wireframe)
        form.addRow("", self._pedestal)
        self._picture_form = form
        self._set_size()
        return box

    def _helpers_group(self):
        box, form = form_group("What else is in shot")
        self._annotations = QCheckBox("Annotations painted on the surface")
        self._annotations.setChecked(True)
        self._measurements = QCheckBox("Measurements")
        self._armature = QCheckBox("Armature")
        self._gizmo = QCheckBox("Orientation gizmo")
        self._readout = QCheckBox("Model readout")
        self._caption = QCheckBox("Which stage this is")
        self._caption.setChecked(True)
        self._caption.setToolTip(
            "Burn the stage number, how many solids it is made of and the "
            "Detail setting that rebuilds it into the corner of every frame"
        )
        for widget in (
            self._annotations,
            self._measurements,
            self._armature,
            self._gizmo,
            self._readout,
            self._caption,
        ):
            form.addRow("", widget)
        return box

    def _file_group(self):
        box, form = form_group("File")
        self._format = QComboBox()
        for video in VideoFormat:
            self._format.addItem(video.label, video.value)
        self._quality = QComboBox()
        for quality in Quality:
            self._quality.addItem(quality.label, quality.value)
        self._quality.setCurrentIndex(1)
        self._loop = QCheckBox("Play round again")
        self._loop.setChecked(True)
        self._note = QLabel()
        self._note.setWordWrap(True)
        self._note.setStyleSheet("color: #8f939b;")
        form.addRow("Format", self._format)
        form.addRow("Quality", self._quality)
        form.addRow("", self._loop)
        form.addRow("", self._note)
        self._file_form = form
        return box

    def _connect(self) -> None:
        self._size.currentIndexChanged.connect(self._apply_size)
        for spin in (self._width, self._height):
            spin.valueChanged.connect(self._size_typed)
        for spin in (self._seconds, self._hold, self._ghost_opacity):
            spin.valueChanged.connect(self._changed)
        for combo in (self._shading, self._format, self._quality):
            combo.currentIndexChanged.connect(self._changed)
        for check in (
            self._ghost,
            self._wireframe,
            self._pedestal,
            self._annotations,
            self._measurements,
            self._armature,
            self._gizmo,
            self._readout,
            self._caption,
            self._loop,
        ):
            check.toggled.connect(self._changed)

    # -- reading the controls ---------------------------------------------

    def look(self) -> ExportLook:
        """What the frames are to look like, as the controls have it."""
        shading = self._shading.currentData()
        return ExportLook(
            width=even(self._width.value()),
            height=even(self._height.value()),
            shading=None if shading is None else ShadingMode(shading),
            ghost=self._ghost.isChecked(),
            ghost_opacity=self._ghost_opacity.value(),
            wireframe=self._wireframe.isChecked(),
            pedestal=self._pedestal.isChecked(),
            annotations=self._annotations.isChecked(),
            measurements=self._measurements.isChecked(),
            armature=self._armature.isChecked(),
            gizmo=self._gizmo.isChecked(),
            readout=self._readout.isChecked(),
            caption=self._caption.isChecked(),
            stage_count=len(self._stages),
        )

    def settings(self) -> VideoSettings:
        """How long it runs and what it is written as."""
        return VideoSettings(
            format=VideoFormat(self._format.currentData()),
            seconds_per_stage=self._seconds.value(),
            hold_last=self._hold.value(),
            quality=Quality(self._quality.currentData()),
            loop=self._loop.isChecked(),
        )

    def _apply_size(self) -> None:
        self._set_size()
        self._changed()

    def _set_size(self) -> None:
        """Fill the width and height boxes from whichever preset is chosen.

        A preset with no width of its own takes the viewport's shape, so that
        the framing of the clip is the framing the artist has been looking at:
        a frame taller or wider than the window is not a crop of that view, it
        is a different camera.
        """
        chosen = self._size.currentData()
        if chosen is None:
            return  # custom: the boxes are the answer
        width, height = chosen
        if height is None:
            height = max(self._viewport.height(), SIZE_MIN)
        if width is None:
            shape = self._viewport.width() / max(self._viewport.height(), 1)
            width = int(round(height * shape))
        for spin, value in ((self._width, width), (self._height, height)):
            blocked = spin.blockSignals(True)
            spin.setValue(even(min(max(value, SIZE_MIN), SIZE_MAX)))
            spin.blockSignals(blocked)

    def _size_typed(self) -> None:
        """A width or a height typed by hand is a custom size, and says so."""
        index = self._size.findData(None)
        if index >= 0 and self._size.currentIndex() != index:
            blocked = self._size.blockSignals(True)
            self._size.setCurrentIndex(index)
            self._size.blockSignals(blocked)
        self._changed()

    def _changed(self) -> None:
        settings = self.settings()
        video = settings.format
        reason = unavailable(video)
        note = video.note
        if reason is not None:
            note = reason
            self._note.setStyleSheet("color: #c8a95a;")
        elif video is VideoFormat.GIF and not written_by_ffmpeg(video):
            note = (
                f"{video.note} Written here rather than by ffmpeg, which is "
                "slower and simpler about colour -- keep the frame small."
            )
            self._note.setStyleSheet("color: #8f939b;")
        else:
            self._note.setStyleSheet("color: #8f939b;")
        self._note.setText(note)
        self._export_button.setEnabled(reason is None and bool(self._stages))

        self._picture_form.setRowVisible(self._ghost_opacity, self._ghost.isChecked())
        self._file_form.setRowVisible(self._quality, video is not VideoFormat.GIF)
        self._file_form.setRowVisible(
            self._loop, video in (VideoFormat.GIF, VideoFormat.WEBP)
        )

        count = len(self._stages)
        look = self.look()
        so_far = "" if self._complete else " recorded so far"
        self._summary.setText(
            f"{count} stage{'s' * (count != 1)}{so_far}, "
            f"{settings.duration(count):.1f} s at {look.width} x {look.height}."
        )
        self._preview_timer.start()

    # -- the preview ------------------------------------------------------

    def _draw_preview(self) -> None:
        if not self._stages:
            self._preview.setText("Nothing recorded yet")
            return
        look = self.look()
        shape = look.height / max(look.width, 1)
        small = replace(
            look,
            width=even(_PREVIEW_WIDTH),
            height=even(min(max(int(round(_PREVIEW_WIDTH * shape)), 120), 420)),
        )
        try:
            image = self._viewport.stage_image(self._stages[-1], small)
        except Exception as error:  # pragma: no cover - a driver that refused
            self._preview.setText(f"No preview: {error}")
            return
        # The box takes the shape of the frame rather than the frame being
        # letterboxed into a box of its own: the preview is there to show what
        # the clip will be, and its proportions are part of that.
        self._preview.setFixedSize(small.width, small.height)
        self._preview.setPixmap(QPixmap.fromImage(image))

    # -- doing it ---------------------------------------------------------

    def _begin(self) -> None:
        settings = self.settings()
        suggestion = self._suggested_name(settings.format)
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Video", str(suggestion), settings.format.filter
        )
        if not path:
            return
        chosen = Path(path)
        if chosen.suffix.lower() != settings.format.suffix:
            chosen = chosen.with_suffix(settings.format.suffix)

        progress = QProgressDialog("Rendering the making...", "Cancel", 0, len(self._stages), self)
        progress.setWindowTitle("Export Video")
        progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        progress.setMinimumDuration(0)
        progress.setAutoClose(False)
        progress.setAutoReset(False)
        progress.setValue(0)

        run = FilmExport(self._viewport, self._stages, self.look(), settings, chosen, self)
        self._export = run
        run.progress.connect(lambda done, total: self._advance(progress, done, total))
        progress.canceled.connect(run.cancel)
        run.finished.connect(lambda ok, said: self._ended(progress, ok, said))
        self.setEnabled(False)
        run.start()

    @staticmethod
    def _advance(progress: QProgressDialog, done: int, total: int) -> None:
        progress.setValue(done)
        progress.setLabelText(f"Writing frame {done} of {total}...")

    def _ended(self, progress: QProgressDialog, ok: bool, said: str) -> None:
        progress.close()
        self.setEnabled(True)
        self._export = None
        if ok:
            QMessageBox.information(self, "Export Video", f"Written to\n{said}")
        elif said == CANCELLED:
            pass  # the artist already knows; they pressed the button
        else:
            QMessageBox.warning(self, "Export Video", said)

    def _suggested_name(self, video: VideoFormat) -> Path:
        mesh = self._viewport.state.mesh
        stem = "making"
        if mesh is not None and mesh.name:
            stem = f"{Path(mesh.name).stem} making"
        return Path.home() / f"{stem}{video.suffix}"

    def reject(self) -> None:
        """Close, and do not leave an encoding thread behind.

        Waiting is the right thing here for the same reason it is on the way
        out of the application and nowhere else: the window is going away, and
        a QThread that is still running when the last Python reference to it
        drops does not raise, it aborts the process.  What is being waited for
        is one frame's encoding, which is the work the cancel flag is checked
        between.
        """
        if self._export is not None:
            self._export.cancel()
            self._export.wait(10_000)
            self._export = None
        super().reject()
