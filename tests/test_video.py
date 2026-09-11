"""How long the film runs, and what happens when there is nothing to write it.

The arithmetic here is small and it is the part an artist feels: a fifth of a
second a stage is a number they typed, and the clip has to be that long.  It
is tested on its own because the encoders it feeds are either a subprocess or
a file format, and neither is a good place to find out that the hold on the
last stage was counted twice.

The rest is about ffmpeg not being there, which on an artist's machine is the
normal case rather than the exceptional one.  What must happen then is a
sentence they can act on, and a GIF that still works.
"""

from __future__ import annotations

import numpy as np
import pytest

from refview.core import video
from refview.core.video import (
    Quality,
    VideoError,
    VideoFormat,
    VideoSettings,
    open_writer,
    unavailable,
)


@pytest.fixture
def no_ffmpeg(monkeypatch):
    """A machine with no video encoder on it, which is most of them."""
    monkeypatch.setattr(video, "ffmpeg_path", lambda: None)
    monkeypatch.setattr(video, "_encoders", frozenset)
    return None


def frames(count: int, width: int, height: int):
    ramp = np.linspace(30, 220, height).astype(np.uint8)
    for index in range(count):
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[..., 1] = ramp[:, None]
        frame[:, : int(width * (index + 1) / count)] = (200, 120, 40)
        yield frame.tobytes()


class TestTiming:
    def test_a_stage_is_held_for_what_was_asked_for(self):
        settings = VideoSettings(seconds_per_stage=0.2, hold_last=0.0)
        assert settings.seconds_at(0, 10) == pytest.approx(0.2)
        assert settings.step_ms == 200

    def test_the_last_stage_is_held_for_longer(self):
        settings = VideoSettings(seconds_per_stage=0.2, hold_last=1.0)
        assert settings.seconds_at(8, 10) == pytest.approx(0.2)
        assert settings.seconds_at(9, 10) == pytest.approx(1.2)

    def test_the_clip_is_as_long_as_its_stages_plus_the_hold(self):
        settings = VideoSettings(seconds_per_stage=0.25, hold_last=2.0)
        assert settings.duration(8) == pytest.approx(4.0)

    def test_a_film_with_no_stages_runs_for_no_time(self):
        assert VideoSettings().duration(0) == 0.0

    def test_the_hold_is_counted_once_however_short_the_film(self):
        # One stage is both the first and the last, and it is held for its own
        # time and the hold -- not for two holds.
        settings = VideoSettings(seconds_per_stage=0.5, hold_last=1.5)
        assert settings.seconds_at(0, 1) == pytest.approx(2.0)
        assert settings.duration(1) == pytest.approx(2.0)

    def test_a_stage_shorter_than_a_millisecond_still_has_a_rate(self):
        # The input frame rate is 1000/step_ms, so a step that rounded to zero
        # would be a division by zero rather than a fast clip.
        assert VideoSettings(seconds_per_stage=0.0001).step_ms == 1


class TestFormats:
    def test_every_format_names_a_suffix_and_a_filter(self):
        for chosen in VideoFormat:
            assert chosen.suffix.startswith(".")
            assert chosen.suffix[1:] in chosen.filter
            assert chosen.label and chosen.note

    def test_a_gif_is_the_one_format_that_needs_nothing_installed(self):
        assert not VideoFormat.GIF.needs_ffmpeg
        for chosen in (VideoFormat.MP4, VideoFormat.AVI, VideoFormat.WEBP):
            assert chosen.needs_ffmpeg

    def test_quality_runs_the_right_way_round(self):
        # Lower is better for both of these, and the labels say the opposite,
        # so the two are easy to wire up backwards.
        assert Quality.BEST.crf < Quality.GOOD.crf < Quality.DRAFT.crf
        assert Quality.BEST.qscale < Quality.GOOD.qscale < Quality.DRAFT.qscale
        assert Quality.BEST.webp_quality > Quality.DRAFT.webp_quality


class TestWithoutFfmpeg:
    def test_a_gif_can_still_be_written(self, tmp_path, no_ffmpeg):
        assert unavailable(VideoFormat.GIF) is None
        assert not video.written_by_ffmpeg(VideoFormat.GIF)
        path = tmp_path / "film.gif"
        writer = open_writer(path, (32, 24), VideoSettings(format=VideoFormat.GIF))
        for frame in frames(4, 32, 24):
            writer.add(frame, 0.2)
        writer.close()
        assert path.stat().st_size > 0

    def test_the_others_say_what_is_missing_rather_than_failing(self, no_ffmpeg):
        for chosen in (VideoFormat.MP4, VideoFormat.AVI, VideoFormat.WEBP):
            said = unavailable(chosen)
            assert said is not None
            assert "ffmpeg" in said.lower()

    def test_asking_for_one_anyway_is_an_error_in_words(self, tmp_path, no_ffmpeg):
        with pytest.raises(VideoError, match="ffmpeg"):
            open_writer(tmp_path / "f.mp4", (32, 24), VideoSettings(format=VideoFormat.MP4))


@pytest.mark.skipif(video.ffmpeg_path() is None, reason="no ffmpeg on this machine")
class TestWithFfmpeg:
    @pytest.mark.parametrize(
        "chosen", [VideoFormat.MP4, VideoFormat.AVI, VideoFormat.GIF, VideoFormat.WEBP]
    )
    def test_a_short_film_comes_out_as_a_playable_file(self, tmp_path, chosen):
        if unavailable(chosen) is not None:
            pytest.skip(f"this ffmpeg cannot write {chosen.value}")
        settings = VideoSettings(format=chosen, seconds_per_stage=0.2, hold_last=0.4)
        path = tmp_path / f"film{chosen.suffix}"
        writer = open_writer(path, (64, 48), settings)
        made = list(frames(5, 64, 48))
        for index, frame in enumerate(made):
            writer.add(frame, settings.seconds_at(index, len(made)))
        writer.close()
        assert path.stat().st_size > 200

    def test_a_frame_of_the_wrong_size_is_reported_rather_than_ignored(self, tmp_path):
        settings = VideoSettings(format=VideoFormat.MP4)
        writer = open_writer(tmp_path / "film.mp4", (64, 48), settings)
        # Half a frame: ffmpeg reads it as a truncated stream and stops, and
        # what must not happen is a file that silently contains nonsense.
        writer.add(b"\x00" * (64 * 48 * 3 // 2), 0.2)
        with pytest.raises(VideoError):
            writer.close()

    def test_an_abandoned_export_leaves_no_file_behind(self, tmp_path):
        path = tmp_path / "film.mp4"
        writer = open_writer(path, (64, 48), VideoSettings(format=VideoFormat.MP4))
        writer.add(next(frames(1, 64, 48)), 0.2)
        writer.abort()
        assert not path.exists()
