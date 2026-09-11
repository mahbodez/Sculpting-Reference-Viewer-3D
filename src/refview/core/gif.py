"""Writing an animated GIF with nothing but numpy and the standard library.

The other three video formats are handed to ffmpeg, which does them properly
and does them fast.  This one is written here as well, and the reason is not
that ffmpeg does GIFs badly -- it does them better than this.  It is that a GIF
is what an artist actually sends someone: a block-in arriving, dropped into a
message, playing by itself.  A feature that works only on the machines that
happen to carry a video encoder is a feature half the people who want it
cannot use, and the whole of a GIF -- a palette, LZW, and a header with the
frame delays in it -- is small enough to simply write.

So this is the floor.  When ffmpeg is there it is used for GIFs too, because
its palette handling is better and its inner loop is not Python; when it is
not, this still hands back a file that plays.

Two things carry the quality.  The palette is read by median cut, which splits
the colours of the frame along whichever axis they are most spread on and
keeps splitting the widest box until there are as many boxes as colours
allowed -- so a form lit by one matcap over a gradient spends its 256 colours
where that form actually has them, rather than on a cube of colours most of
which nothing on screen is.  And the mapping onto that palette is dithered on
an ordered 8x8 grid, because the background *is* a gradient and a gradient
quantised without dither is a flight of steps.

The palette is global: one for the whole film rather than one per frame.  That
is what lets every frame after the first be a plain table lookup, and it costs
little here because the stages of a film are the same form at different
coarsenesses under the same light -- the colours barely move.  It is read from
whichever frame the caller primes the writer with, and the caller should prime
it with the *last* stage, which is the one with the most of the form in it.
"""

from __future__ import annotations

import contextlib
from pathlib import Path

import numpy as np

#: Most colours a GIF palette can hold.
MAX_COLORS = 256
#: How many pixels the palette is read from.  Median cut wants the shape of
#: the colour cloud rather than every point in it, and a sixty-fourth of a
#: 1080p frame still has sixty thousand samples in it.
PALETTE_SAMPLE = 65536
#: How far the ordered dither moves a channel before it is quantised, in
#: levels.  The lookup table is built on a 32-step grid per channel, so noise
#: smaller than eight levels would be rounded away before it did anything.
DITHER_SPREAD = 8.0
#: The shortest delay a GIF may carry.  Anything under two hundredths is read
#: by most browsers as "unspecified" and silently played at a tenth of a
#: second, which is slower than what was asked for rather than faster -- so
#: the floor is set here, where it can be seen, rather than met out there.
MIN_DELAY_CS = 2


def _bayer(order: int = 3) -> np.ndarray:
    """The ordered-dither threshold grid, as offsets in -0.5 to 0.5."""
    matrix = np.zeros((1, 1), dtype=np.float64)
    for _ in range(order):
        matrix = np.block(
            [
                [4.0 * matrix, 4.0 * matrix + 2.0],
                [4.0 * matrix + 3.0, 4.0 * matrix + 1.0],
            ]
        )
    return (matrix + 0.5) / matrix.size - 0.5


_DITHER = _bayer()


def palette_of(pixels: np.ndarray, colors: int = MAX_COLORS) -> np.ndarray:
    """The ``colors`` that best stand for ``pixels``, by median cut.

    One box to start with, holding every colour in the frame; then over and
    over the box whose colours are most spread out along some axis is sorted
    along that axis and split at its median, until there are as many boxes as
    colours wanted.  Each box comes back as the mean of what fell in it.

    Which is, not by accident, the same shape of argument as the stone mode in
    :mod:`~refview.core.plane_volume`: split the piece holding the most of
    what you are trying to account for, and keep going.
    """
    pixels = np.asarray(pixels, dtype=np.uint8).reshape(-1, 3)
    if len(pixels) == 0:
        return np.zeros((1, 3), dtype=np.uint8)
    if len(pixels) > PALETTE_SAMPLE:
        pixels = pixels[:: len(pixels) // PALETTE_SAMPLE + 1]
    unique = np.unique(pixels, axis=0)
    colors = max(int(colors), 2)
    if len(unique) <= colors:
        return unique

    boxes = [pixels.astype(np.int16)]
    while len(boxes) < colors:
        widest, axis, extent = -1, 0, 0
        for index, box in enumerate(boxes):
            if len(box) < 2:
                continue
            spread = box.max(axis=0) - box.min(axis=0)
            along = int(np.argmax(spread))
            if int(spread[along]) > extent:
                widest, axis, extent = index, along, int(spread[along])
        if widest < 0:
            break  # every box holds one colour; there is nothing left to split
        box = boxes.pop(widest)
        box = box[np.argsort(box[:, axis], kind="stable")]
        half = len(box) // 2
        boxes.append(box[:half])
        boxes.append(box[half:])
    table = np.array([box.mean(axis=0) for box in boxes])
    return np.rint(table).clip(0, 255).astype(np.uint8)


def _lookup(palette: np.ndarray) -> np.ndarray:
    """For every colour on a 32x32x32 grid, the nearest entry in ``palette``.

    Thirty-two thousand nearest-neighbour searches once, rather than one per
    pixel per frame.  Five bits a channel is finer than the palette itself can
    resolve anywhere it is dense, and the dither is what covers the rest.
    """
    levels = (np.arange(32, dtype=np.int32) << 3) | 4
    grid = np.stack(np.meshgrid(levels, levels, levels, indexing="ij"), axis=-1)
    grid = grid.reshape(-1, 3)
    table = palette.astype(np.int32)
    nearest = np.empty(len(grid), dtype=np.uint8)
    # In slabs, because the full distance matrix would be a gigabyte.
    for start in range(0, len(grid), 4096):
        chunk = grid[start : start + 4096]
        distance = ((chunk[:, None, :] - table[None, :, :]) ** 2).sum(axis=-1)
        nearest[start : start + 4096] = np.argmin(distance, axis=1)
    return nearest


def _indices(frame: np.ndarray, lookup: np.ndarray, spread: float) -> np.ndarray:
    """``frame`` as one palette index per pixel, dithered on the way."""
    values = frame.astype(np.float32)
    if spread > 0.0:
        height, width = values.shape[:2]
        tiles = (height // 8 + 1, width // 8 + 1)
        noise = np.tile(_DITHER, tiles)[:height, :width]
        values = values + (noise * spread)[:, :, None]
    keys = np.clip(values, 0.0, 255.0).astype(np.int32) >> 3
    return lookup[(keys[..., 0] << 10) | (keys[..., 1] << 5) | keys[..., 2]]


def lzw(indices: bytes, min_code_size: int) -> bytes:
    """The GIF flavour of LZW: variable-width codes, packed low bit first.

    Straight out of the specification, with the two details that are easy to
    get wrong spelled out.

    The code width grows *after* a code has been written, when the next entry
    to be handed out would no longer fit in the current width -- not before
    writing it, and not when the entry is used.  A decoder's table lags the
    encoder's by one entry, and this is the ordering under which the two of
    them still change width on the same code.  Off by one either way and the
    file decodes as noise from that point on.

    And when the table fills at 4096 entries a clear code is written at the
    current width and everything starts over, rather than the table being left
    to go stale on a film whose colours have moved on.
    """
    clear = 1 << min_code_size
    end = clear + 1
    out = bytearray()
    pending = 0
    held = 0
    width = min_code_size + 1
    table: dict[tuple[int, int], int] = {}
    following = end + 1

    def emit(code: int) -> None:
        nonlocal pending, held
        pending |= code << held
        held += width
        while held >= 8:
            out.append(pending & 0xFF)
            pending >>= 8
            held -= 8

    emit(clear)
    stream = iter(indices)
    prefix = next(stream, None)
    if prefix is not None:
        for value in stream:
            key = (prefix, value)
            known = table.get(key)
            if known is not None:
                prefix = known
                continue
            emit(prefix)
            if following >= 4096:
                emit(clear)
                table.clear()
                following = end + 1
                width = min_code_size + 1
            else:
                if following > (1 << width) - 1 and width < 12:
                    width += 1
                table[key] = following
                following += 1
            prefix = value
        emit(prefix)
    emit(end)
    if held:
        out.append(pending & 0xFF)
    return bytes(out)


def _blocks(payload: bytes) -> bytes:
    """Chop a byte stream into the length-prefixed runs a GIF is made of."""
    out = bytearray()
    for start in range(0, len(payload), 255):
        chunk = payload[start : start + 255]
        out.append(len(chunk))
        out.extend(chunk)
    out.append(0)
    return bytes(out)


class GifWriter:
    """An animated GIF, written a frame at a time.

    Frames are handed in as ``(height, width, 3)`` uint8 arrays, or as the raw
    RGB bytes of one.  Each carries how long it is to be held for, in seconds,
    which is the whole reason a GIF suits a film of stages: a stage can linger
    without the frame being written out thirty times over.

    Call :meth:`prime` with the frame the palette should be read from before
    the first :meth:`add`, or the first frame added is used for it.
    """

    def __init__(
        self,
        path: Path | str,
        width: int,
        height: int,
        loop: bool = True,
        colors: int = MAX_COLORS,
        dither: float = DITHER_SPREAD,
    ) -> None:
        self._path = path
        self._width = max(int(width), 1)
        self._height = max(int(height), 1)
        self._loop = bool(loop)
        self._colors = max(min(int(colors), MAX_COLORS), 2)
        self._dither = float(dither)
        self._lookup: np.ndarray | None = None
        self._bits = 8
        self._file = open(path, "wb")  # noqa: SIM115 - closed by close()/abort()
        self._started = False

    @property
    def size(self) -> tuple[int, int]:
        return self._width, self._height

    def prime(self, frame: np.ndarray | bytes) -> None:
        """Read the palette from ``frame`` rather than from the first one added."""
        if self._lookup is not None:
            return
        pixels = self._as_array(frame).reshape(-1, 3)
        palette = palette_of(pixels, self._colors)
        self._bits = max(2, int(np.ceil(np.log2(max(len(palette), 2)))))
        self._lookup = _lookup(palette)
        self._write_header(palette)

    def add(self, frame: np.ndarray | bytes, seconds: float) -> None:
        """Write one frame, to be held on screen for ``seconds``."""
        self.prime(frame)
        lookup = self._lookup
        if lookup is None:  # pragma: no cover - prime() has just set it
            raise RuntimeError("The GIF palette was not read")
        indices = _indices(self._as_array(frame), lookup, self._dither)
        delay = max(MIN_DELAY_CS, int(round(float(seconds) * 100.0)))
        self._file.write(
            b"\x21\xf9\x04\x04"
            + delay.to_bytes(2, "little")
            + b"\x00\x00"
            + b"\x2c"
            + (0).to_bytes(2, "little")
            + (0).to_bytes(2, "little")
            + self._width.to_bytes(2, "little")
            + self._height.to_bytes(2, "little")
            + b"\x00"
        )
        min_code_size = max(2, self._bits)
        self._file.write(bytes([min_code_size]))
        self._file.write(_blocks(lzw(indices.astype(np.uint8).tobytes(), min_code_size)))

    def close(self) -> None:
        """Finish the file.  A GIF with no frames in it is still a valid GIF."""
        if self._file.closed:
            return
        if not self._started:
            self._write_header(np.zeros((2, 3), dtype=np.uint8))
        self._file.write(b"\x3b")
        self._file.close()

    def abort(self) -> None:
        """Give up, leaving no half-written file behind."""
        if not self._file.closed:
            self._file.close()
        # A file the platform is still holding open is not worth an error on
        # the way out of one.
        with contextlib.suppress(OSError):
            Path(self._path).unlink(missing_ok=True)

    # -- the parts of the format ------------------------------------------

    def _as_array(self, frame: np.ndarray | bytes) -> np.ndarray:
        if isinstance(frame, np.ndarray):
            return frame.reshape(self._height, self._width, 3)
        return np.frombuffer(frame, dtype=np.uint8).reshape(self._height, self._width, 3)

    def _write_header(self, palette: np.ndarray) -> None:
        self._started = True
        entries = 1 << self._bits
        table = np.zeros((entries, 3), dtype=np.uint8)
        table[: len(palette)] = palette[:entries]
        packed = 0x80 | ((self._bits - 1) << 4) | (self._bits - 1)
        self._file.write(
            b"GIF89a"
            + self._width.to_bytes(2, "little")
            + self._height.to_bytes(2, "little")
            + bytes([packed, 0, 0])
            + table.tobytes()
        )
        # The looping block is Netscape's, not Compuserve's, and every player
        # reads it: without it a GIF plays once and stops on its last frame.
        repeats = 0 if self._loop else 1
        self._file.write(
            b"\x21\xff\x0bNETSCAPE2.0\x03\x01" + repeats.to_bytes(2, "little") + b"\x00"
        )
