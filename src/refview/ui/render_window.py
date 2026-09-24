"""The Render Window: a render filling in, and the controls to look at it and keep it.

The picture is shown as it is made -- bucket by bucket, with the buckets
being worked on marked by their corners, or pass by pass as the whole frame
clears.  It can be zoomed about the cursor with the wheel and moved by
dragging; a double click fits it to the window again.

What is shown can be any of the passes the render keeps: the picture, the
denoised picture, the albedo, normals, depth and coverage the denoisers are
guided by, and a map of how many samples each pixel took.  The view
transform and the exposure develop the finished light again, straight
away, with no new render -- as a frame buffer in Corona or V-Ray does.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PySide6.QtCore import QPointF, QRectF, Qt, Signal
from PySide6.QtGui import QColor, QImage, QKeySequence, QPainter, QPen, QShortcut
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core.path_trace import OutputFormat, ViewTransform
from .render_controller import RenderController, RenderResult
from .state import ViewerState
from .widgets import SliderSpin

PASSES = ("Beauty", "Denoised", "Albedo", "Normal", "Depth", "Alpha", "Samples")
ZOOMS = (("Fit", None), ("25%", 0.25), ("50%", 0.5), ("100%", 1.0), ("200%", 2.0),
         ("400%", 4.0))
_BRACKET = QColor(255, 196, 92)


class RenderView(QWidget):
    """The picture, over a checkerboard where it is transparent, zoomed and moved at will."""

    zoom_changed = Signal(object)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setMinimumSize(320, 240)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self._image: QImage | None = None
        self._zoom: float | None = None     # None: fit to the window
        self._centre = QPointF(0.5, 0.5)    # the picture point at the view's centre
        self._drag: QPointF | None = None
        self._buckets: list = []
        self.show_buckets = True

    # -- what is shown ---------------------------------------------------------

    def set_image(self, image: QImage | None) -> None:
        self._image = image
        self.update()

    def set_buckets(self, buckets: list) -> None:
        self._buckets = list(buckets)
        self.update()

    @property
    def zoom(self) -> float | None:
        return self._zoom

    def set_zoom(self, zoom: float | None) -> None:
        self._zoom = zoom
        if zoom is None:
            self._centre = QPointF(0.5, 0.5)
        self.zoom_changed.emit(zoom)
        self.update()

    def fit(self) -> None:
        self.set_zoom(None)

    def _scale(self) -> float:
        if self._image is None or self._image.isNull():
            return 1.0
        if self._zoom is not None:
            return self._zoom / self.devicePixelRatioF()
        w, h = self._image.width(), self._image.height()
        return min(max(self.width() - 16, 1) / w, max(self.height() - 16, 1) / h)

    def _target(self) -> QRectF:
        image = self._image
        scale = self._scale()
        w, h = image.width() * scale, image.height() * scale
        cx = self.width() / 2.0 - (self._centre.x() - 0.5) * w
        cy = self.height() / 2.0 - (self._centre.y() - 0.5) * h
        return QRectF(cx - w / 2.0, cy - h / 2.0, w, h)

    # -- painting --------------------------------------------------------------

    def paintEvent(self, _event) -> None:  # noqa: N802 - Qt naming
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(30, 31, 34))
        image = self._image
        if image is None or image.isNull():
            painter.setPen(QColor(150, 152, 158))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter,
                             "Press F12 to render the view.")
            return
        target = self._target()
        self._checkerboard(painter, target)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, self._scale() < 2.0)
        painter.drawImage(target, image)
        if self.show_buckets and self._buckets:
            scale = self._scale()
            pen = QPen(_BRACKET, 1.5)
            painter.setPen(pen)
            for x0, y0, x1, y1 in self._buckets:
                rect = QRectF(target.left() + x0 * scale, target.top() + y0 * scale,
                              (x1 - x0) * scale, (y1 - y0) * scale)
                arm = min(rect.width(), rect.height()) * 0.25
                for cx, cy, dx, dy in ((rect.left(), rect.top(), 1, 1),
                                       (rect.right(), rect.top(), -1, 1),
                                       (rect.left(), rect.bottom(), 1, -1),
                                       (rect.right(), rect.bottom(), -1, -1)):
                    painter.drawLine(QPointF(cx, cy), QPointF(cx + dx * arm, cy))
                    painter.drawLine(QPointF(cx, cy), QPointF(cx, cy + dy * arm))

    def _checkerboard(self, painter: QPainter, rect: QRectF) -> None:
        painter.save()
        painter.setClipRect(rect.intersected(QRectF(self.rect())))
        size = 12
        light, dark = QColor(88, 90, 94), QColor(64, 66, 70)
        painter.fillRect(rect, dark)
        x0 = int(rect.left()) - int(rect.left()) % (2 * size)
        y0 = int(rect.top()) - int(rect.top()) % (2 * size)
        for y in range(y0, int(rect.bottom()) + size, size):
            for x in range(x0 + ((y - y0) // size % 2) * size, int(rect.right()) + size,
                           2 * size):
                painter.fillRect(x, y, size, size, light)
        painter.restore()

    # -- navigation ------------------------------------------------------------

    def wheelEvent(self, event) -> None:  # noqa: N802 - Qt naming
        if self._image is None:
            return
        steps = event.angleDelta().y() / 120.0
        if steps == 0:
            return
        ratio = self.devicePixelRatioF()
        current = self._scale() * ratio
        zoom = min(max(current * (1.25 ** steps), 0.05), 32.0)
        # Keep the picture point under the cursor where it is.
        target = self._target()
        pos = event.position()
        u = (pos.x() - target.left()) / max(target.width(), 1e-9)
        v = (pos.y() - target.top()) / max(target.height(), 1e-9)
        self._zoom = zoom
        scale = self._scale()
        w, h = self._image.width() * scale, self._image.height() * scale
        self._centre = QPointF(u - (pos.x() - self.width() / 2.0) / w,
                               v - (pos.y() - self.height() / 2.0) / h)
        self.zoom_changed.emit(zoom)
        self.update()

    def mousePressEvent(self, event) -> None:  # noqa: N802 - Qt naming
        if event.button() in (Qt.MouseButton.LeftButton, Qt.MouseButton.MiddleButton):
            self._drag = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802 - Qt naming
        if self._drag is None or self._image is None:
            return
        delta = event.position() - self._drag
        self._drag = event.position()
        target = self._target()
        if self._zoom is None:
            self._zoom = self._scale() * self.devicePixelRatioF()
            self.zoom_changed.emit(self._zoom)
        self._centre = QPointF(self._centre.x() - delta.x() / max(target.width(), 1e-9),
                               self._centre.y() - delta.y() / max(target.height(), 1e-9))
        self.update()

    def mouseReleaseEvent(self, _event) -> None:  # noqa: N802 - Qt naming
        self._drag = None
        self.unsetCursor()

    def mouseDoubleClickEvent(self, _event) -> None:  # noqa: N802 - Qt naming
        self.fit()

    def keyPressEvent(self, event) -> None:  # noqa: N802 - Qt naming
        if event.key() in (Qt.Key.Key_F, Qt.Key.Key_Home):
            self.fit()
            return
        super().keyPressEvent(event)


def _duration(seconds: float | None) -> str:
    if seconds is None:
        return "--:--"
    seconds = int(round(seconds))
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes:02d}:{secs:02d}"


def stats_text(result: RenderResult) -> str:
    """The status line: pass, samples, time, speed, threads, memory."""
    stats = result.stats
    if stats is None:
        return "Preparing..."
    from ..trace.job import JobState

    parts = []
    if result.settings.performance.method.value == "bucket":
        parts.append(f"Bucket {stats.tiles_done}/{stats.tiles_total}")
    else:
        parts.append(f"Pass {stats.pass_index}")
    parts.append(f"{stats.samples_done:.0f}/{stats.samples_target} spp")
    if stats.state is JobState.RENDERING:
        parts.append(f"{_duration(stats.elapsed)} elapsed")
        parts.append(f"~{_duration(stats.remaining)} left")
    elif stats.state is JobState.DONE:
        parts.append(f"done in {_duration(stats.elapsed)}")
    elif stats.state is JobState.CANCELLED:
        parts.append(f"stopped at {_duration(stats.elapsed)}")
    parts.append(f"{stats.rays_per_second / 1e6:.1f} M rays/s")
    parts.append(f"{stats.threads} threads")
    parts.append(f"{stats.memory_bytes / 2 ** 20:.0f} MB")
    if result.denoiser:
        parts.append(f"denoised: {result.denoiser}")
    return "  ·  ".join(parts)


class RenderWindow(QWidget):
    """The window renders are shown in; made once and kept."""

    render_requested = Signal()

    def __init__(self, state: ViewerState, controller: RenderController,
                 parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Render")
        self.resize(1100, 760)
        self._state = state
        self._controller = controller
        self._result: RenderResult | None = None
        self._display: np.ndarray | None = None     # (h, w, 4) float32 display values
        self._bytes: np.ndarray | None = None       # (h, w, 4) uint8
        self._qimage: QImage | None = None
        self._busy = False

        self._view = RenderView(self)
        self._render = QPushButton("Render")
        self._render.setToolTip("Render the view as it is now (F12)")
        self._stop = QPushButton("Stop")
        self._stop.setToolTip("Stop the render; what has been rendered is kept (Esc)")
        self._save = QPushButton("Save...")
        self._save.setToolTip("Save the pass shown, in the format the Render panel sets (Ctrl+S)")
        self._save_all = QPushButton("Save all passes...")
        self._save_all.setToolTip(
            "Save the picture and every pass as layers of one OpenEXR file,\n"
            "linear, for compositing")
        self._denoise = QPushButton("Denoise")
        self._denoise.setToolTip("Denoise the render now, with the Render panel's denoiser")
        self._pass = QComboBox()
        self._pass.addItems(PASSES)
        self._pass.setToolTip(
            "What to show: the picture, the denoised picture, or one of the passes\n"
            "the denoisers are guided by, or how many samples each pixel took")
        self._transform = QComboBox()
        for transform in ViewTransform:
            self._transform.addItem(transform.label, transform.value)
        self._transform.setToolTip(
            "How the light becomes pixel values.  Changes the finished render\n"
            "at once, without rendering again.")
        self._exposure = SliderSpin(-10.0, 10.0, 0.0, decimals=1, step=0.1, suffix=" EV",
                                    caption="Exposure")
        self._exposure.setToolTip("Brighter or darker, in stops, without rendering again")
        self._zoom = QComboBox()
        for label, _value in ZOOMS:
            self._zoom.addItem(label)
        self._zoom.setToolTip("Zoom; the mouse wheel zooms about the cursor, a double click fits")
        self._buckets = QCheckBox("Show buckets")
        self._buckets.setChecked(True)
        self._buckets.setToolTip("Mark the buckets being rendered with their corners")
        self._status = QLabel("Press F12 to render the view.")
        self._status.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self._progress = QProgressBar()
        self._progress.setRange(0, 1000)
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(6)

        bar = QHBoxLayout()
        for widget in (self._render, self._stop, self._save, self._save_all, self._denoise):
            bar.addWidget(widget)
        bar.addSpacing(12)
        bar.addWidget(QLabel("Show"))
        bar.addWidget(self._pass)
        bar.addWidget(self._transform)
        bar.addWidget(self._exposure, 1)
        bar.addWidget(self._zoom)
        bar.addWidget(self._buckets)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.addLayout(bar)
        layout.addWidget(self._view, 1)
        layout.addWidget(self._progress)
        layout.addWidget(self._status)

        self._render.clicked.connect(self.render_requested)
        self._stop.clicked.connect(controller.cancel)
        self._save.clicked.connect(self.save)
        self._save_all.clicked.connect(self.save_all_passes)
        self._denoise.clicked.connect(lambda: controller.denoise())
        self._pass.currentIndexChanged.connect(lambda _i: self._develop_all())
        self._transform.currentIndexChanged.connect(self._on_transform)
        self._exposure.valueChanged.connect(self._on_exposure)
        self._zoom.activated.connect(lambda i: self._view.set_zoom(ZOOMS[i][1]))
        self._view.zoom_changed.connect(self._on_zoom_changed)
        self._buckets.toggled.connect(self._on_buckets)
        QShortcut(QKeySequence("F12"), self, activated=self.render_requested.emit)
        QShortcut(QKeySequence("Esc"), self, activated=controller.cancel)
        QShortcut(QKeySequence("Ctrl+S"), self, activated=self.save)

        controller.started.connect(self._on_started)
        controller.progressed.connect(self._on_progressed)
        controller.finished.connect(self._on_finished)
        controller.denoised.connect(self._on_denoised)
        controller.status_changed.connect(self._on_status)
        controller.failed.connect(self._on_failed)
        state.path_trace_changed.connect(self.refresh_colour)
        self.refresh_colour()
        self._sync_buttons()

    # -- the colour controls ---------------------------------------------------

    def refresh_colour(self) -> None:
        color = self._state.path_trace.color
        self._busy = True
        try:
            self._transform.setCurrentIndex(
                max(self._transform.findData(color.view_transform.value), 0))
            self._exposure.set_value(color.exposure)
        finally:
            self._busy = False
        self._develop_all()

    def _on_transform(self, index: int) -> None:
        if self._busy:
            return
        self._state.path_trace.color.view_transform = ViewTransform(
            self._transform.itemData(index))
        self._state.notify_path_trace()

    def _on_exposure(self, value: float) -> None:
        if self._busy:
            return
        self._state.path_trace.color.exposure = float(value)
        self._state.notify_path_trace()

    def _on_zoom_changed(self, zoom) -> None:
        for index, (_label, value) in enumerate(ZOOMS):
            if value == zoom or (value is not None and zoom is not None
                                 and abs(value - zoom) < 1e-6):
                self._zoom.setCurrentIndex(index)
                return

    def _on_buckets(self, on: bool) -> None:
        self._view.show_buckets = on
        self._view.update()

    # -- a render's life ---------------------------------------------------------

    def _on_started(self, result: RenderResult) -> None:
        self._result = result
        w, h = result.size
        self._display = np.zeros((h, w, 4), np.float32)
        self._bytes = np.zeros((h, w, 4), np.uint8)
        self._qimage = QImage(self._bytes.data, w, h, w * 4, QImage.Format.Format_RGBA8888)
        if self._pass.currentText() == "Denoised":
            self._pass.setCurrentIndex(0)
        self._view.set_image(self._qimage)
        self._develop_all()
        self._sync_buttons()
        self._status.setText(f"Rendering {w} x {h}...")

    def _on_progressed(self, result: RenderResult, dirty: list) -> None:
        if result is not self._result:
            return
        if self._pass.currentText() == "Beauty":
            if len(dirty) > 64:
                self._develop_all()
            else:
                for rect in dirty:
                    self._develop_rect(rect)
                self._view.update()
        elif dirty:
            self._develop_all()
        job = result.job
        self._view.set_buckets(job.active_tiles() if job is not None else [])
        self._status.setText(stats_text(result))
        stats = result.stats
        if stats is not None and stats.samples_target:
            if stats.tiles_total and result.settings.performance.method.value == "bucket":
                fraction = stats.tiles_done / stats.tiles_total
            else:
                fraction = max(min(stats.samples_done / stats.samples_target, 1.0),
                               1.0 - stats.open_share)
            self._progress.setValue(int(fraction * 1000))

    def _on_finished(self, result: RenderResult) -> None:
        if result is not self._result:
            return
        self._view.set_buckets([])
        self._develop_all()
        self._status.setText(stats_text(result))
        self._progress.setValue(1000)
        self._sync_buttons()

    def _on_denoised(self, result: RenderResult) -> None:
        if result is not self._result:
            return
        # A finished, denoised render is shown denoised, as the result.
        if self._pass.currentText() == "Beauty":
            self._pass.setCurrentIndex(PASSES.index("Denoised"))
        else:
            self._develop_all()
        self._status.setText(stats_text(result) + "".join(f"  ·  {n}" for n in result.notes))
        self._sync_buttons()

    def _on_status(self, text: str) -> None:
        if self._result is None or self._result.stats is None:
            self._status.setText(text)
        self._sync_buttons()

    def _on_failed(self, text: str) -> None:
        self._status.setText(text)
        self._sync_buttons()
        if self.isVisible():
            QMessageBox.warning(self, "Render", text)

    def _sync_buttons(self) -> None:
        running = self._controller.running
        has = bool(self._result is not None and self._result.film.count.max() > 0)
        self._stop.setEnabled(running)
        self._save.setEnabled(has)
        self._save_all.setEnabled(has)
        self._denoise.setEnabled(has and not running)
        model = self._pass.model()
        item = model.item(PASSES.index("Denoised"))
        if item is not None:
            item.setEnabled(self._result is not None and self._result.denoised is not None)

    # -- developing --------------------------------------------------------------

    def _colour_args(self):
        from ..trace.colour import TRANSFORM_CODES, exposure_scale

        result = self._result
        color = self._state.path_trace.color
        transform = TRANSFORM_CODES[color.view_transform.resolved(result.skin)]
        stops = color.exposure + (result.skin_exposure if result.skin else 0.0)
        transparent = bool(result.settings.output.transparent)
        return (transform, exposure_scale(stops), float(color.gamma), float(color.contrast),
                np.asarray(result.background_top, np.float64),
                np.asarray(result.background_bottom, np.float64), transparent, not transparent)

    def _develop_rect(self, rect) -> None:
        from ..trace.colour import develop_region, quantize_region

        result = self._result
        x0, y0, x1, y1 = rect
        develop_region(result.film.rgba, result.film.count, self._display, x0, y0, x1, y1,
                       *self._colour_args())
        quantize_region(self._display, self._bytes, x0, y0, x1, y1)

    def _develop_all(self) -> None:
        result = self._result
        if result is None or self._bytes is None:
            return
        w, h = result.size
        shown = self._pass.currentText()
        if shown == "Beauty" or (shown == "Denoised" and result.denoised is None):
            self._develop_rect((0, 0, w, h))
        else:
            self._bytes[...] = self._pass_bytes(shown)
        self._view.update()

    def _pass_bytes(self, shown: str) -> np.ndarray:
        from ..trace.colour import develop_image, to_rgba8

        result = self._result
        film = result.film
        h, w = film.height, film.width
        out = np.zeros((h, w, 4), np.float32)
        out[..., 3] = 1.0
        if shown == "Denoised":
            args = self._colour_args()
            ones = np.ones((h, w), np.int32)
            from ..trace.colour import develop_region

            develop_region(np.ascontiguousarray(result.denoised, dtype=np.float32), ones, out,
                           0, 0, w, h, *args)
        elif shown == "Albedo":
            albedo = film.albedo_pass()
            if albedo is not None:
                image = np.concatenate([albedo, np.ones((h, w, 1), np.float32)], -1)
                out = develop_image(image, 0, 0.0, 1.0, 0.0, background=False)
                out[..., 3] = 1.0
        elif shown == "Normal":
            normal = film.normal_pass()
            if normal is not None:
                out[..., :3] = normal * 0.5 + 0.5
        elif shown == "Depth":
            depth = film.depth_pass()
            if depth is not None and np.any(depth > 0):
                near = depth[depth > 0].min()
                far = depth[depth > 0].max()
                value = np.where(depth > 0, 1.0 - (depth - near) / max(far - near, 1e-9), 0.0)
                out[..., :3] = value[..., None]
        elif shown == "Alpha":
            out[..., :3] = np.clip(film.beauty()[..., 3:4], 0.0, 1.0)
        elif shown == "Samples":
            count = film.count.astype(np.float32)
            value = count / max(float(count.max()), 1.0)
            out[..., 0] = np.clip(value * 2.0, 0.0, 1.0)
            out[..., 1] = np.clip(value * 2.0 - 0.6, 0.0, 1.0)
            out[..., 2] = np.clip(1.0 - value * 1.5, 0.0, 1.0) * 0.6
        return to_rgba8(out)

    # -- saving ------------------------------------------------------------------

    def _suggested(self, suffix: str) -> str:
        from ..paths import PROJECT_ROOT

        first = next((obj for obj in self._state.objects if obj.path is not None), None)
        stem = first.path.stem if first is not None else "render"
        folder = first.path.parent if first is not None else Path.home()
        if not folder.exists():
            folder = PROJECT_ROOT
        return str(folder / f"{stem}_render{suffix}")

    def save(self) -> None:
        result = self._result
        if result is None:
            return
        fmt = self._state.path_trace.output.format
        path, _ = QFileDialog.getSaveFileName(
            self, "Save render", self._suggested(fmt.suffix),
            "OpenEXR (*.exr)" if fmt.linear else "PNG image (*.png)")
        if not path:
            return
        path = Path(path)
        if path.suffix.lower() != fmt.suffix:
            path = path.with_suffix(fmt.suffix)
        try:
            self.write(path, fmt)
        except Exception as error:  # noqa: BLE001 -- reported, never lost silently
            QMessageBox.warning(self, "Save render", f"Could not save {path.name}: {error}")
            return
        self._status.setText(f"Saved {path}")

    def write(self, path: Path, fmt: OutputFormat) -> None:
        """Write the pass shown to ``path`` in ``fmt``."""
        result = self._result
        shown = self._pass.currentText()
        use_denoised = shown == "Denoised" and result.denoised is not None
        if fmt.linear:
            from ..trace.exr import write_exr

            rgba = result.denoised if use_denoised else result.film.beauty()
            write_exr(path, {"RGBA": rgba}, half=fmt is OutputFormat.EXR_HALF)
            return
        if shown in ("Beauty", "Denoised"):
            from ..trace.colour import develop_region

            h, w = result.film.height, result.film.width
            display = np.zeros((h, w, 4), np.float32)
            if use_denoised:
                develop_region(np.ascontiguousarray(result.denoised, dtype=np.float32),
                               np.ones((h, w), np.int32), display, 0, 0, w, h,
                               *self._colour_args())
            else:
                develop_region(result.film.rgba, result.film.count, display, 0, 0, w, h,
                               *self._colour_args())
        else:
            display = self._pass_bytes(shown).astype(np.float32) / 255.0
        save_display(path, display, sixteen=fmt is OutputFormat.PNG16)

    def save_all_passes(self) -> None:
        result = self._result
        if result is None:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save all passes",
                                              self._suggested("_passes.exr"), "OpenEXR (*.exr)")
        if not path:
            return
        path = Path(path).with_suffix(".exr")
        from ..trace.exr import write_exr

        film = result.film
        layers = {"RGBA": film.beauty()}
        if result.denoised is not None:
            layers["denoised"] = result.denoised[..., :3]
        for name, array in (("albedo", film.albedo_pass()), ("normal", film.normal_pass()),
                            ("depth.Z", film.depth_pass())):
            if array is not None:
                layers[name] = array
        layers["samples.Y"] = film.count.astype(np.float32)
        try:
            write_exr(path, layers, half=False)
        except Exception as error:  # noqa: BLE001
            QMessageBox.warning(self, "Save all passes", f"Could not save {path.name}: {error}")
            return
        self._status.setText(f"Saved {path}")

    @property
    def result(self) -> RenderResult | None:
        return self._result

    @property
    def view(self) -> RenderView:
        return self._view


def save_display(path: Path, display: np.ndarray, sixteen: bool = False) -> None:
    """Display values ``(h, w, 4)`` in [0, 1] to a PNG, 8 or 16 bits a channel."""
    from ..trace.colour import to_rgba8, to_rgba16

    h, w = display.shape[:2]
    if sixteen:
        data = np.ascontiguousarray(to_rgba16(display))
        image = QImage(data.data, w, h, w * 8, QImage.Format.Format_RGBA64)
    else:
        data = np.ascontiguousarray(to_rgba8(display))
        image = QImage(data.data, w, h, w * 4, QImage.Format.Format_RGBA8888)
    if not image.copy().save(str(path)):
        raise OSError("the image could not be written")
