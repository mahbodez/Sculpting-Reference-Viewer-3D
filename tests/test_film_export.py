"""Writing a film out: the loop, the thread behind it, and the way out of both.

The rendering half of an export needs a graphics context and is not tested
here.  What is tested is everything around it, which is where an export can go
wrong in ways that are worse than a bad picture: a frame handed to the encoder
sheared because Qt padded its rows, a clip that is one frame short because the
last one was still in the queue when the file was closed, a thread left
running behind a window that has already gone.

So the viewport is stood in for.  It hands back frames of the right size with
nothing in them, which is all the encoder cares about, and the real one is
exercised by running the application.
"""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.mesh import Mesh
from refview.core.plane_film import Stage
from refview.core.settings import RenderSettings, ShadingMode
from refview.core.video import VideoFormat, VideoSettings

QtCore = pytest.importorskip("PySide6.QtCore")
QtGui = pytest.importorskip("PySide6.QtGui")
QtWidgets = pytest.importorskip("PySide6.QtWidgets")

from refview.ui.film_export import (  # noqa: E402 - needs Qt first
    ExportLook,
    FilmExport,
    even,
    frame_bytes,
)


@pytest.fixture(scope="session")
def app():
    """One offscreen Qt application, made once and never torn down."""
    import os

    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    existing = QtWidgets.QApplication.instance()
    yield existing or QtWidgets.QApplication([])


def run_until(app, done, timeout_ms: int = 30_000) -> bool:
    """Pump the event loop until ``done()`` or the clock runs out."""
    clock = QtCore.QElapsedTimer()
    clock.start()
    while not done() and clock.elapsed() < timeout_ms:
        app.processEvents(QtCore.QEventLoop.ProcessEventsFlag.AllEvents, 20)
    return done()


def stages(count: int) -> list[Stage]:
    mesh = Mesh(
        name="block",
        positions=np.zeros((3, 3), dtype=np.float32),
        normals=np.zeros((3, 3), dtype=np.float32),
        indices=np.arange(3, dtype=np.uint32),
    )
    return [
        Stage(index=index, solids=index + 1, planes=index + 2, mesh=mesh)
        for index in range(count)
    ]


class FakeViewport:
    """A viewport that renders nothing, at whatever size it is asked for."""

    def __init__(self, width: int = 800, height: int = 600) -> None:
        self._size = (width, height)
        self.rendered = 0
        self.closed = False

    def width(self) -> int:
        return self._size[0]

    def height(self) -> int:
        return self._size[1]

    def _image(self, look: ExportLook, tint: int) -> QtGui.QImage:
        image = QtGui.QImage(look.width, look.height, QtGui.QImage.Format.Format_RGB888)
        image.fill(QtGui.QColor(tint, 40, 200 - tint))
        return image

    def stage_image(self, stage, look):
        self.rendered += 1
        return self._image(look, 10)

    def stage_images(self, wanted, look):
        try:
            for index, _ in enumerate(wanted):
                self.rendered += 1
                yield self._image(look, min(index * 20, 255))
        finally:
            # The real one restores the scene it borrowed here.
            self.closed = True


class TestEven:
    def test_a_size_is_taken_down_to_a_multiple_of_four(self):
        assert even(1080) == 1080
        assert even(1081) == 1080
        assert even(1083) == 1080
        assert even(721) == 720

    def test_a_size_never_reaches_zero(self):
        assert even(1) == 4
        assert even(0) == 4


class TestFrameBytes:
    @pytest.mark.parametrize("width", [64, 65, 66, 67])
    def test_a_frame_is_packed_tight_whatever_its_width(self, app, width):
        image = QtGui.QImage(width, 5, QtGui.QImage.Format.Format_RGB888)
        image.fill(QtGui.QColor(10, 20, 30))
        packed = frame_bytes(image)
        assert len(packed) == width * 5 * 3
        # Every pixel is the one colour, so any padding left in would show up
        # as a run of something else.
        assert set(packed[0::3]) == {10}
        assert set(packed[1::3]) == {20}
        assert set(packed[2::3]) == {30}


class TestExportLook:
    def test_the_viewport_shading_is_kept_unless_one_is_named(self):
        base = RenderSettings(shading_mode=ShadingMode.PBR)
        assert ExportLook().render_settings(base).shading_mode is ShadingMode.PBR
        chosen = ExportLook(shading=ShadingMode.NORMALS).render_settings(base)
        assert chosen.shading_mode is ShadingMode.NORMALS

    def test_what_is_not_named_here_comes_out_as_the_artist_left_it(self):
        base = RenderSettings()
        base.surface.diffuse_color = (0.1, 0.2, 0.3)
        base.matcap.rotation_deg = 45.0
        settings = ExportLook(ghost=True).render_settings(base)
        assert settings.surface.diffuse_color == (0.1, 0.2, 0.3)
        assert settings.matcap.rotation_deg == 45.0
        assert settings.ghost

    def test_the_document_itself_is_not_touched(self):
        base = RenderSettings()
        ExportLook(ghost=True, wireframe=True).render_settings(base)
        assert not base.ghost
        assert not base.show_wireframe

    def test_nothing_in_progress_is_ever_drawn_into_a_frame(self):
        # There is no half-placed measurement during an export, but a brush
        # ring under a cursor that happens to be over the view would be.
        assert not ExportLook().parts.tools

    def test_the_helpers_asked_for_are_the_ones_drawn(self):
        parts = ExportLook(measurements=True, armature=True, readout=False).parts
        assert parts.measurements and parts.armature
        assert not parts.readout

    def test_a_caption_says_where_in_the_making_this_is(self):
        look = ExportLook(stage_count=40)
        caption = look.caption_for(stages(3)[1])
        assert "2/40" in caption
        assert "2 solids" in caption
        assert "Detail 3" in caption

    def test_a_caption_counts_off_the_film_rather_than_off_the_export(self):
        # The preview renders one stage on its own, and it must not call the
        # last stage of a film the first.
        look = ExportLook(stage_count=6)
        assert "6/6" in look.caption_for(stages(6)[-1])

    def test_a_stage_no_slider_can_reach_claims_no_setting(self):
        mesh = stages(1)[0].mesh
        stage = Stage(index=0, solids=2, planes=None, mesh=mesh)
        assert "Detail" not in ExportLook(stage_count=5).caption_for(stage)


class TestFilmExport:
    def _run(self, app, path, settings, count=5, look=None):
        viewport = FakeViewport()
        look = look or ExportLook(width=64, height=48, stage_count=count)
        export = FilmExport(viewport, stages(count), look, settings, path)
        ended: list = []
        export.finished.connect(lambda ok, said: ended.append((ok, said)))
        export.start()
        run_until(app, lambda: bool(ended))
        export.wait(5_000)
        return viewport, export, ended

    def test_a_film_is_written_frame_for_stage(self, app, tmp_path):
        path = tmp_path / "film.gif"
        settings = VideoSettings(format=VideoFormat.GIF, seconds_per_stage=0.1, hold_last=0.0)
        viewport, export, ended = self._run(app, path, settings, count=5)
        assert ended == [(True, str(path))]
        assert viewport.rendered == 5
        assert path.stat().st_size > 0

        reader = QtGui.QImageReader(str(path))
        read = 0
        while not reader.read().isNull():
            read += 1
        assert read == 5

    def test_the_scene_is_given_back_when_the_export_ends(self, app, tmp_path):
        settings = VideoSettings(format=VideoFormat.GIF, seconds_per_stage=0.1)
        viewport, _, _ = self._run(app, tmp_path / "film.gif", settings, count=4)
        assert viewport.closed

    def test_progress_counts_frames_that_are_really_written(self, app, tmp_path):
        settings = VideoSettings(format=VideoFormat.GIF, seconds_per_stage=0.1)
        viewport = FakeViewport()
        look = ExportLook(width=64, height=48)
        export = FilmExport(viewport, stages(6), look, settings, tmp_path / "f.gif")
        seen: list[tuple[int, int]] = []
        ended: list = []
        export.progress.connect(lambda done, total: seen.append((done, total)))
        export.finished.connect(lambda ok, said: ended.append(ok))
        export.start()
        run_until(app, lambda: bool(ended))
        export.wait(5_000)
        assert seen == [(index, 6) for index in range(1, 7)]

    def test_a_cancelled_export_leaves_no_file_behind(self, app, tmp_path):
        path = tmp_path / "film.gif"
        settings = VideoSettings(format=VideoFormat.GIF, seconds_per_stage=0.1)
        viewport = FakeViewport()
        export = FilmExport(viewport, stages(40), ExportLook(width=64, height=48), settings, path)
        ended: list = []
        export.finished.connect(lambda ok, said: ended.append((ok, said)))
        export.start()
        # Let a couple of frames land, then change your mind.
        run_until(app, lambda: export._index >= 2, timeout_ms=5_000)
        export.cancel()
        run_until(app, lambda: bool(ended))
        export.wait(5_000)
        assert ended and ended[0][0] is False
        assert not path.exists()
        assert viewport.closed

    def test_a_format_that_cannot_be_written_says_so_and_writes_nothing(
        self, app, tmp_path, monkeypatch
    ):
        from refview.core import video

        monkeypatch.setattr(video, "ffmpeg_path", lambda: None)
        path = tmp_path / "film.mp4"
        settings = VideoSettings(format=VideoFormat.MP4)
        _, _, ended = self._run(app, path, settings, count=3)
        assert ended and ended[0][0] is False
        assert "ffmpeg" in ended[0][1].lower()
        assert not path.exists()

    def test_waiting_on_an_export_still_running_ends_it(self, app, tmp_path):
        # What a window closing mid-export does.  The thread is blocked on the
        # queue rather than on an event loop, so a wait that did not first
        # call the export off would time out and then drop a live thread.
        path = tmp_path / "film.gif"
        settings = VideoSettings(format=VideoFormat.GIF, seconds_per_stage=0.1)
        viewport = FakeViewport()
        export = FilmExport(viewport, stages(40), ExportLook(width=64, height=48), settings, path)
        export.start()
        run_until(app, lambda: export._index >= 1, timeout_ms=5_000)
        export.wait(5_000)
        assert export._thread is not None
        assert export._thread.isFinished()
        assert not path.exists()

    def test_a_one_stage_film_is_still_a_film(self, app, tmp_path):
        path = tmp_path / "one.gif"
        settings = VideoSettings(format=VideoFormat.GIF, seconds_per_stage=0.3, hold_last=0.9)
        _, _, ended = self._run(app, path, settings, count=1)
        assert ended == [(True, str(path))]

        reader = QtGui.QImageReader(str(path))
        held = 0
        while not reader.read().isNull():
            held += reader.nextImageDelay()
        # However it was written -- as one frame with a long delay on it, or
        # as several with short ones -- the single stage is on screen for its
        # own time and the closing hold.
        assert held == pytest.approx(settings.duration(1) * 1000, abs=40)
