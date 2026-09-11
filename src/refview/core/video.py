"""Turning a sequence of rendered frames into a file someone can play.

A film of a form's making is already a sequence of stages, each one a finished
mesh -- so exporting it is not a recording problem, it is an encoding one: how
long each stage is held for, and what container the held frames go into.

Four formats, and they are not four ways of doing the same thing.  MP4 is what
goes into a portfolio or a lesson.  AVI is what the older editing suites still
want handed to them.  GIF is what gets sent to another artist, because it
plays by itself in the message it arrives in.  WebP is the same errand as the
GIF with a quarter of the bytes, for anywhere modern enough to take it.

Three of those are ffmpeg's job.  Writing an H.264 stream is not something to
attempt by hand, and ffmpeg is on most machines that do anything with video --
so it is looked for, used when it is there, and said to be missing in plain
words when it is not, rather than the export failing with a traceback.  GIF is
the exception: ffmpeg does it better and faster, and is used when present, but
:mod:`refview.core.gif` will write one without it.  See that module for why
that floor is worth having.

Timing is stated as seconds per stage rather than as a frame rate, because
that is the question an artist actually has -- how long do I want to look at
each step -- and because the stages of a film are not frames of anything.  A
fifth of a second a stage is a block-in arriving at about the pace of a hand.
The frame-based formats are given that as their input rate and asked for a
normal playback rate on the way out, so ffmpeg holds each stage for as many
frames as it takes; the GIF carries the delay per frame, which is what a GIF
is for.
"""

from __future__ import annotations

import contextlib
import functools
import os
import shutil
import subprocess
import sys
import tempfile
import typing
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from .gif import GifWriter

if typing.TYPE_CHECKING:  # pragma: no cover - import cost, not behaviour
    import numpy as np

#: Environment override for where ffmpeg lives, for a machine that has one
#: somewhere unusual or a build that ships its own.
FFMPEG_ENV = "REFVIEW_FFMPEG"

#: Playback rate of the frame-based formats.  A film is held a stage at a
#: time rather than animated, so this is not how fast anything moves -- it is
#: only what a player expects to be handed.  Thirty is what everything plays
#: without thinking about it.
PLAYBACK_FPS = 30

#: Shortest and longest a stage may be held for, in seconds.  The short end is
#: a stage a frame long at normal playback; the long end is a slideshow.
STAGE_MIN, STAGE_MAX = 0.02, 5.0
#: How long the finished form may be left on screen at the end, in seconds.
HOLD_MAX = 10.0


class VideoFormat(str, Enum):
    """A container, and with it a codec and a set of trade-offs."""

    MP4 = "mp4"
    AVI = "avi"
    GIF = "gif"
    WEBP = "webp"

    @property
    def label(self) -> str:
        return {
            VideoFormat.MP4: "MP4 (H.264)",
            VideoFormat.AVI: "AVI (MPEG-4)",
            VideoFormat.GIF: "Animated GIF",
            VideoFormat.WEBP: "Animated WebP",
        }[self]

    @property
    def suffix(self) -> str:
        return f".{self.value}"

    @property
    def filter(self) -> str:
        """The file dialog's filter line for this format."""
        return f"{self.label} (*{self.suffix})"

    @property
    def needs_ffmpeg(self) -> bool:
        """Whether this format can only be written by ffmpeg.

        GIF is the one that cannot: see :mod:`refview.core.gif`.
        """
        return self is not VideoFormat.GIF

    @property
    def note(self) -> str:
        """What an artist should know before picking this one."""
        return {
            VideoFormat.MP4: (
                "The usual choice: small, sharp, and playable everywhere."
            ),
            VideoFormat.AVI: (
                "For an editing suite that will not take an MP4. Much larger "
                "files for the same picture."
            ),
            VideoFormat.GIF: (
                "Plays by itself wherever it is pasted, which is what makes it "
                "the one to send. Only 256 colours, and large frames make "
                "large files -- keep it small."
            ),
            VideoFormat.WEBP: (
                "A GIF's job done properly: full colour, a fraction of the "
                "size. Browsers and chat apps take it; older software may not."
            ),
        }[self]


class Quality(str, Enum):
    """How hard the encoder is asked to work at keeping the picture."""

    DRAFT = "draft"
    GOOD = "good"
    BEST = "best"

    @property
    def label(self) -> str:
        return {
            Quality.DRAFT: "Draft (smallest file)",
            Quality.GOOD: "Good",
            Quality.BEST: "Best (largest file)",
        }[self]

    @property
    def crf(self) -> int:
        """H.264's constant-rate factor, where lower keeps more."""
        return {Quality.DRAFT: 28, Quality.GOOD: 21, Quality.BEST: 16}[self]

    @property
    def qscale(self) -> int:
        """MPEG-4's quantiser, 1 (best) to 31."""
        return {Quality.DRAFT: 8, Quality.GOOD: 4, Quality.BEST: 2}[self]

    @property
    def webp_quality(self) -> int:
        """WebP's quality, 0 to 100."""
        return {Quality.DRAFT: 60, Quality.GOOD: 80, Quality.BEST: 95}[self]


class VideoError(RuntimeError):
    """An export that could not be written, said in words for the artist."""


@dataclass(frozen=True)
class VideoSettings:
    """How long the film runs and what it is written as.

    Everything here is about time and bytes.  What the frames *look* like is a
    separate question, settled by the viewport rather than by the encoder.
    """

    format: VideoFormat = VideoFormat.MP4
    #: How long one stage of the film is held on screen.
    seconds_per_stage: float = 0.2
    #: Extra seconds the last stage is held for, over and above its own.  The
    #: finished form is the one worth looking at, and a clip that cuts away
    #: from it the instant it arrives -- or, looping, never rests on it at all
    #: -- is a clip that never shows what was made.
    hold_last: float = 1.0
    quality: Quality = Quality.GOOD
    #: Whether the GIF or WebP plays round again.  Says nothing to MP4 or AVI,
    #: where looping is the player's business rather than the file's.
    loop: bool = True

    @property
    def step_ms(self) -> int:
        """One stage's hold, in whole milliseconds.

        The encoders are driven off this rather than off the float, so that
        the input frame rate and the count of repeats for the closing hold are
        two readings of exactly the same number.
        """
        return max(int(round(float(self.seconds_per_stage) * 1000.0)), 1)

    def repeats_at(self, index: int, count: int) -> int:
        """How many input frames the stage at ``index`` of ``count`` takes.

        One, except for the last, which takes as many more as the closing hold
        is worth.  The hold is counted in whole stages rather than in seconds
        because a stream going into ffmpeg has one rate and every frame in it
        lasts exactly one tick of that rate -- so a hold of a second at a
        third of a second a stage is three more frames, and saying it was 1.0
        when the file says 0.9 would be the export lying about itself.  The
        rounding is at most half a stage, and it is the same rounding the GIF
        writer is handed, so every path agrees on the number.
        """
        if count > 0 and index >= count - 1:
            return 1 + max(int(round(max(float(self.hold_last), 0.0) * 1000.0 / self.step_ms)), 0)
        return 1

    def seconds_at(self, index: int, count: int) -> float:
        """How long the stage at ``index`` of ``count`` is held for."""
        return self.repeats_at(index, count) * self.step_ms / 1000.0

    def duration(self, count: int) -> float:
        """How long the whole film runs, in seconds."""
        if count <= 0:
            return 0.0
        frames = (count - 1) + self.repeats_at(count - 1, count)
        return frames * self.step_ms / 1000.0


@functools.lru_cache(maxsize=1)
def ffmpeg_path() -> str | None:
    """Where ffmpeg is, or ``None``.

    Looked for in the order of how deliberate each answer is: an override the
    user set, a copy shipped beside the application, one on the path, and
    finally one belonging to ``imageio-ffmpeg`` if that happens to be
    installed -- which it is not by default, but a scientific Python
    environment often has it and there is no reason not to use it.
    """
    override = os.environ.get(FFMPEG_ENV)
    if override and Path(override).exists():
        return str(Path(override))

    beside = Path(getattr(sys, "_MEIPASS", "")) if getattr(sys, "frozen", False) else None
    if beside is not None:
        for name in ("ffmpeg.exe", "ffmpeg"):
            candidate = beside / name
            if candidate.exists():
                return str(candidate)

    found = shutil.which("ffmpeg")
    if found:
        return found

    try:  # pragma: no cover - depends on the environment, not on us
        import imageio_ffmpeg

        return str(imageio_ffmpeg.get_ffmpeg_exe())
    except Exception:
        return None


@functools.lru_cache(maxsize=1)
def _encoders() -> frozenset[str]:
    """Which encoders this ffmpeg was built with.

    Asked once, because a build without ``libx264`` is common enough -- the
    licence keeps it out of some distributions' packages -- that falling back
    to plain MPEG-4 quietly is better than handing the artist an error about a
    codec they have never heard of.
    """
    ffmpeg = ffmpeg_path()
    if ffmpeg is None:
        return frozenset()
    try:
        result = subprocess.run(
            [ffmpeg, "-hide_banner", "-encoders"],
            capture_output=True,
            text=True,
            timeout=20,
            **_no_window(),
        )
    except (OSError, subprocess.SubprocessError):  # pragma: no cover - a broken binary
        return frozenset()
    names = set()
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and len(parts[0]) == 6:
            names.add(parts[1])
    return frozenset(names)


def _no_window() -> dict:
    """Keep a console window from flashing up on Windows for each ffmpeg call."""
    if sys.platform == "win32":
        return {"creationflags": 0x08000000}  # CREATE_NO_WINDOW
    return {}


def unavailable(format: VideoFormat) -> str | None:
    """Why ``format`` cannot be written here, or ``None`` if it can."""
    if not format.needs_ffmpeg:
        return None
    if ffmpeg_path() is None:
        return (
            "Needs ffmpeg, which was not found. Install it and put it on the "
            "path, or point the REFVIEW_FFMPEG variable at it."
        )
    if format is VideoFormat.WEBP and "libwebp" not in _encoders():
        return "This ffmpeg was built without libwebp, so it cannot write WebP."
    return None


def written_by_ffmpeg(format: VideoFormat) -> bool:
    """Whether this export will go through ffmpeg.

    Only GIF can answer no, and only when there is no ffmpeg to answer yes
    with -- which is worth showing in the dialog, because the built-in writer
    is slower and its palette is simpler.
    """
    return format.needs_ffmpeg or ffmpeg_path() is not None


class Writer(typing.Protocol):  # pragma: no cover - a shape, not code
    """What an export needs of whatever is doing the encoding."""

    def prime(self, frame: np.ndarray | bytes) -> None:
        """Offered the last frame before the first is written, if it helps."""

    def add(self, frame: np.ndarray | bytes, seconds: float) -> None:
        """Write one frame, held for ``seconds``."""

    def close(self) -> None:
        """Finish the file."""

    def abort(self) -> None:
        """Give up, leaving nothing half-written behind."""


class _FFmpegWriter:
    """Raw frames down a pipe, a finished file out the other end.

    The frames go in as rgb24 at one stage per input frame, which is what lets
    the hold on the last stage be a handful of repeats rather than a second's
    worth: at five input frames a second, a one-second hold is five writes,
    and ffmpeg does the work of turning that into thirty frames a second of
    output.
    """

    def __init__(
        self, path: Path | str, size: tuple[int, int], settings: VideoSettings, ffmpeg: str
    ) -> None:
        width, height = (max(int(value), 2) for value in size)
        self._path = Path(path)
        self._settings = settings
        # Keeping stderr on a file rather than a pipe: a pipe nobody is
        # reading fills up and stops the process we are trying to feed, which
        # is a deadlock that only shows itself on the one export that happens
        # to produce a lot of warnings.
        self._log = tempfile.TemporaryFile()  # noqa: SIM115 - closed by close()/abort()
        arguments = [
            ffmpeg,
            "-hide_banner",
            "-loglevel", "error",
            "-y",
            "-f", "rawvideo",
            "-pix_fmt", "rgb24",
            "-s", f"{width}x{height}",
            "-framerate", f"1000/{settings.step_ms}",
            "-i", "-",
            *_encode_arguments(settings),
            str(self._path),
        ]
        try:
            self._process = subprocess.Popen(  # noqa: S603 - our own argument list
                arguments,
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=self._log,
                **_no_window(),
            )
        except OSError as error:
            self._log.close()
            raise VideoError(f"ffmpeg would not start: {error}") from error

    def prime(self, frame: np.ndarray | bytes) -> None:
        """Nothing to do: ffmpeg reads the whole stream before it decides."""

    def add(self, frame: np.ndarray | bytes, seconds: float) -> None:
        payload = frame if isinstance(frame, bytes) else bytes(memoryview(frame))
        repeats = max(int(round(seconds * 1000.0 / self._settings.step_ms)), 1)
        stdin = self._process.stdin
        if stdin is None:  # pragma: no cover - Popen always gives us one
            raise VideoError("ffmpeg has no input to write to")
        try:
            for _ in range(repeats):
                stdin.write(payload)
        except (BrokenPipeError, OSError) as error:
            raise VideoError(self._complaint(str(error))) from error

    def close(self) -> None:
        if self._process.poll() is None and self._process.stdin is not None:
            with contextlib.suppress(OSError):  # pragma: no cover - already gone
                self._process.stdin.close()
        code = self._process.wait()
        complaint = self._complaint()
        self._log.close()
        if code != 0:
            raise VideoError(complaint)

    def abort(self) -> None:
        if self._process.poll() is None:
            self._process.kill()
            self._process.wait()
        self._log.close()
        with contextlib.suppress(OSError):  # pragma: no cover - a held file
            self._path.unlink(missing_ok=True)

    def _complaint(self, fallback: str = "") -> str:
        """The last thing ffmpeg said, which is usually the useful thing."""
        try:
            self._log.seek(0)
            said = self._log.read().decode("utf-8", "replace").strip()
        except (OSError, ValueError):  # pragma: no cover - the log went away
            said = ""
        lines = [line for line in said.splitlines() if line.strip()]
        if lines:
            return "ffmpeg: " + lines[-1]
        return fallback or "ffmpeg stopped without saying why"


def _encode_arguments(settings: VideoSettings) -> list[str]:
    """What to ask ffmpeg for, once the raw frames are going in."""
    quality = settings.quality
    have = _encoders()
    if settings.format is VideoFormat.MP4:
        if "libx264" in have:
            return [
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", str(quality.crf),
                # Chroma subsampling and even dimensions, because a player
                # that cannot open the file is not a smaller file.
                "-pix_fmt", "yuv420p",
                "-movflags", "+faststart",
                "-r", str(PLAYBACK_FPS),
            ]
        return [
            "-c:v", "mpeg4",
            "-q:v", str(quality.qscale),
            "-pix_fmt", "yuv420p",
            "-r", str(PLAYBACK_FPS),
        ]
    if settings.format is VideoFormat.AVI:
        return [
            "-c:v", "mpeg4",
            "-vtag", "xvid",
            "-q:v", str(quality.qscale),
            "-pix_fmt", "yuv420p",
            "-r", str(PLAYBACK_FPS),
        ]
    if settings.format is VideoFormat.WEBP:
        return [
            "-c:v", "libwebp",
            "-lossless", "0",
            "-q:v", str(quality.webp_quality),
            "-compression_level", "4",
            "-loop", "0" if settings.loop else "1",
            "-r", str(PLAYBACK_FPS),
        ]
    # A GIF holds its own delays, so it keeps the input rate rather than being
    # padded out to thirty frames a second -- padding one would multiply the
    # file by six for a picture nobody could tell apart.  The palette is read
    # from the whole clip and then applied to it, which is two passes over the
    # frames inside one filter graph.
    return [
        "-filter_complex",
        "split[a][b];[a]palettegen=max_colors=255[p];[b][p]paletteuse=dither=bayer:bayer_scale=3",
        "-loop", "0" if settings.loop else "1",
    ]


def open_writer(path: Path | str, size: tuple[int, int], settings: VideoSettings) -> Writer:
    """Start an encoder for ``settings``, or say why there cannot be one."""
    reason = unavailable(settings.format)
    if reason is not None:
        raise VideoError(reason)
    ffmpeg = ffmpeg_path()
    if ffmpeg is not None:
        return _FFmpegWriter(path, size, settings, ffmpeg)
    width, height = size
    return GifWriter(path, width, height, loop=settings.loop)
