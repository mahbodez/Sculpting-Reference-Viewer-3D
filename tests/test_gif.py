"""The GIF written here, read back by something that is not this.

A format this old is all off-by-ones -- a code width that grows one entry
sooner than it looks like it should, a table that has to be cleared before it
is full rather than after, a palette whose size is stated as a power minus
one.  Every one of those produces a file, and the file is noise from the point
the mistake happens onwards.  So the test that matters is not that the writer
runs: it is that a decoder nobody here wrote agrees about what came out.

Qt ships one, which is the decoder the artist's chat window is using anyway.
The LZW layer gets a round trip of its own on top of that, because a bug that
only shows up on a frame with four thousand distinct runs in it is a bug that
the small pictures here would sail past.
"""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.gif import GifWriter, lzw, palette_of

QtGui = pytest.importorskip("PySide6.QtGui")
QtCore = pytest.importorskip("PySide6.QtCore")


def unlzw(payload: bytes, min_code_size: int) -> bytes:
    """A plain GIF LZW decoder, for testing the encoder against.

    Deliberately written from the specification rather than from the encoder,
    including the width rule: a decoder grows its width when the entry it has
    just added fills the current one, which is one entry behind where the
    encoder grows.  The two meeting on the same code is the thing under test.
    """
    clear = 1 << min_code_size
    end = clear + 1
    table: dict[int, bytes] = {}
    out = bytearray()
    held = 0
    bits = 0
    width = min_code_size + 1
    previous: int | None = None

    def reset() -> None:
        nonlocal table, width, previous
        table = {index: bytes([index]) for index in range(clear)}
        width = min_code_size + 1
        previous = None

    reset()
    following = end + 1
    for byte in payload:
        held |= byte << bits
        bits += 8
        while bits >= width:
            code = held & ((1 << width) - 1)
            held >>= width
            bits -= width
            if code == clear:
                reset()
                following = end + 1
                continue
            if code == end:
                return bytes(out)
            if previous is None or code in table:
                entry = table[code]
            else:
                # The code the encoder is about to define, used in the same
                # breath as defining it.  The classic one.
                entry = table[previous] + table[previous][:1]
            out += entry
            if previous is not None:
                table[following] = table[previous] + entry[:1]
                following += 1
                if following >= (1 << width) and width < 12:
                    width += 1
            previous = code
    return bytes(out)


def frames(count: int, width: int, height: int) -> list[np.ndarray]:
    """A little film: a bar that grows, over a vertical gradient."""
    made = []
    ramp = np.linspace(20, 200, height).astype(np.uint8)
    for index in range(count):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[..., 2] = ramp[:, None]
        frame[..., 0] = np.linspace(0, 120, width).astype(np.uint8)[None, :]
        reach = int(width * (index + 1) / count)
        frame[height // 3 : 2 * height // 3, :reach] = (230, 180, 60)
        made.append(frame)
    return made


def read_back(path):
    """Every frame of a GIF, as Qt's own decoder reads them."""
    reader = QtGui.QImageReader(str(path))
    if not reader.canRead():  # pragma: no cover - a Qt without the gif plugin
        pytest.skip("Qt cannot read GIFs in this build")
    images = []
    delays = []
    # read() walks an animation forward by itself and ends by handing back a
    # null image; asking it to jump as well skips every other frame.
    while True:
        image = reader.read()
        if image.isNull():
            break
        delays.append(reader.nextImageDelay())
        images.append(image.convertToFormat(QtGui.QImage.Format.Format_RGB888))
    return images, delays


class TestLzw:
    def test_a_run_of_bytes_comes_back_as_itself(self):
        payload = bytes(range(256)) * 3
        assert unlzw(lzw(payload, 8), 8) == payload

    def test_enough_data_to_grow_the_code_width_several_times(self):
        rng = np.random.default_rng(11)
        # Random bytes build the table fast, which is what walks the width up
        # through nine, ten, eleven and twelve bits inside one frame.
        payload = rng.integers(0, 256, 200_000, dtype=np.uint8).tobytes()
        assert unlzw(lzw(payload, 8), 8) == payload

    def test_enough_data_to_fill_the_table_and_clear_it(self):
        rng = np.random.default_rng(3)
        payload = rng.integers(0, 256, 900_000, dtype=np.uint8).tobytes()
        decoded = lzw(payload, 8)
        # Long enough that the table filled: a clear code is four thousand
        # entries in, and at twelve bits that is well under a megabyte.
        assert unlzw(decoded, 8) == payload

    def test_a_small_palette_uses_a_small_code(self):
        payload = bytes([0, 1, 2, 3] * 500)
        assert unlzw(lzw(payload, 2), 2) == payload

    def test_a_single_pixel_is_still_a_frame(self):
        assert unlzw(lzw(b"\x05", 8), 8) == b"\x05"

    def test_nothing_at_all_is_still_a_valid_stream(self):
        assert unlzw(lzw(b"", 8), 8) == b""


class TestPalette:
    def test_a_picture_with_few_colours_keeps_all_of_them(self):
        pixels = np.array([[10, 20, 30], [200, 100, 0], [10, 20, 30]], dtype=np.uint8)
        table = palette_of(pixels, 256)
        assert len(table) == 2
        assert {tuple(row) for row in table} == {(10, 20, 30), (200, 100, 0)}

    def test_a_gradient_is_cut_into_as_many_colours_as_asked_for(self):
        ramp = np.stack([np.arange(256)] * 3, axis=1).astype(np.uint8)
        table = palette_of(ramp, 16)
        assert len(table) == 16
        # Median cut splits where the colours are, so the entries should be
        # spread across the ramp rather than bunched at one end.
        assert table[:, 0].min() < 32
        assert table[:, 0].max() > 220

    def test_an_empty_picture_does_not_fall_over(self):
        assert len(palette_of(np.zeros((0, 3), dtype=np.uint8))) == 1


class TestGifWriter:
    def test_every_frame_comes_back_at_the_right_size(self, tmp_path):
        made = frames(6, 64, 48)
        path = tmp_path / "film.gif"
        writer = GifWriter(path, 64, 48)
        writer.prime(made[-1])
        for frame in made:
            writer.add(frame, 0.2)
        writer.close()

        images, _ = read_back(path)
        assert len(images) == len(made)
        for image in images:
            assert (image.width(), image.height()) == (64, 48)

    def test_the_colours_are_near_enough_the_ones_asked_for(self, tmp_path):
        made = frames(3, 48, 32)
        path = tmp_path / "film.gif"
        writer = GifWriter(path, 48, 32, dither=0.0)
        for frame in made:
            writer.add(frame, 0.1)
        writer.close()

        images, _ = read_back(path)
        for original, image in zip(made, images, strict=True):
            raw = np.frombuffer(memoryview(image.constBits()), dtype=np.uint8)
            raw = raw[: image.bytesPerLine() * image.height()]
            raw = raw.reshape(image.height(), image.bytesPerLine())[:, : image.width() * 3]
            back = raw.reshape(image.height(), image.width(), 3).astype(np.int16)
            # A 256-colour palette fitted to this picture should land every
            # pixel within a few levels of where it started.
            assert np.abs(back - original.astype(np.int16)).max() <= 12

    def test_each_frame_carries_the_delay_it_was_given(self, tmp_path):
        path = tmp_path / "film.gif"
        writer = GifWriter(path, 32, 32)
        for index in range(3):
            writer.add(frames(3, 32, 32)[index], 0.25)
        writer.close()

        _, delays = read_back(path)
        # Qt reports the delay in milliseconds, and a GIF holds hundredths.
        assert delays[0] == pytest.approx(250, abs=10)

    def test_a_delay_shorter_than_a_gif_can_say_is_lifted_to_its_floor(self, tmp_path):
        path = tmp_path / "film.gif"
        writer = GifWriter(path, 16, 16)
        writer.add(np.zeros((16, 16, 3), dtype=np.uint8), 0.001)
        writer.close()

        _, delays = read_back(path)
        # Not the one-millisecond that was asked for: a GIF cannot say it, and
        # a player handed a delay below two hundredths substitutes a tenth of
        # a second, which is the opposite of what asking for a short one meant.
        assert delays[0] >= 20

    def test_the_palette_is_read_from_whatever_primed_the_writer(self, tmp_path):
        # The first frame is a single grey; the last has the colour in it.  A
        # writer primed with the last must keep that colour, which is the
        # whole reason priming exists.
        first = np.full((16, 16, 3), 60, dtype=np.uint8)
        last = np.zeros((16, 16, 3), dtype=np.uint8)
        last[..., 0] = 220
        last[..., 1] = 40
        path = tmp_path / "film.gif"
        writer = GifWriter(path, 16, 16, dither=0.0)
        writer.prime(last)
        writer.add(first, 0.1)
        writer.add(last, 0.1)
        writer.close()

        images, _ = read_back(path)
        pixel = images[-1].pixelColor(8, 8)
        assert (pixel.red(), pixel.green(), pixel.blue()) == (220, 40, 0)

    def test_an_abandoned_file_is_not_left_behind(self, tmp_path):
        path = tmp_path / "film.gif"
        writer = GifWriter(path, 16, 16)
        writer.add(np.zeros((16, 16, 3), dtype=np.uint8), 0.1)
        writer.abort()
        assert not path.exists()

    def test_raw_bytes_are_taken_as_readily_as_an_array(self, tmp_path):
        frame = frames(1, 24, 16)[0]
        path = tmp_path / "film.gif"
        writer = GifWriter(path, 24, 16)
        writer.add(frame.tobytes(), 0.1)
        writer.close()

        images, _ = read_back(path)
        assert (images[0].width(), images[0].height()) == (24, 16)
