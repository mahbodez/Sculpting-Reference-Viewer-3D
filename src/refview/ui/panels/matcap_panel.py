"""Matcap selection and colour grading.

The grading is done on the matcap itself: the disc under the gallery is the
control, and the five numbers that used to be five rows are folded away
underneath it for the times a number is what you want.  See
:mod:`refview.ui.matcap_preview` for why the disc can be trusted to show what
the renderer will do with it.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings, QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMenu,
    QMessageBox,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from ...core.settings import MatcapSettings
from ...paths import available_matcaps, matcap_dir
from ...render.texture import MatcapLoadError
from ..matcap_preview import MatcapPreview
from ..widgets import (
    ColorButton,
    SliderSpin,
    collapsible_group,
    form_group,
    scrollable,
    symbol_button,
)
from .base import Panel

_THUMBNAIL = QSize(56, 56)
#: Starting split between the gallery and the adjustments, in pixels.  The
#: handle between them is draggable, so this is only where it opens.
_GALLERY_HEIGHT = 220
#: Where the matcaps loaded from outside the folder are remembered, so that
#: one loaded once stays in the gallery from then on.  A list of paths, most
#: recent first.  On the machine rather than in the session, as the gallery
#: is the artist's collection and not the document's.
ADDED_MATCAPS_KEY = "matcaps/added"
#: How many of those the gallery keeps before the oldest drop off.
_ADDED_LIMIT = 64
#: Marks a gallery item as one of those, which is what may be removed.
_ADDED_ROLE = Qt.ItemDataRole.UserRole + 1


#: Thumbnails already made, by path and modification time, shared by every
#: gallery in the process, so a rescan or a second window does not decode the
#: collection again -- but does pick up a file changed on disk.
_THUMBNAIL_CACHE: dict[tuple[str, float], QIcon] = {}


def _thumbnail_key(path: str) -> tuple[str, float]:
    try:
        return path, Path(path).stat().st_mtime
    except OSError:
        return path, 0.0


def _thumbnail(path: str) -> QIcon:
    key = _thumbnail_key(path)
    icon = _THUMBNAIL_CACHE.get(key)
    if icon is None:
        pixmap = QPixmap(path)
        icon = QIcon() if pixmap.isNull() else QIcon(
            pixmap.scaled(
                _THUMBNAIL,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )
        _THUMBNAIL_CACHE[key] = icon
    return icon


def _read_added() -> list[str]:
    # One path a line: a list round-trips through the Windows registry as a
    # bare string when it has one entry, and a string does not.
    written = QSettings().value(ADDED_MATCAPS_KEY, "")
    return [line for line in str(written or "").splitlines() if line.strip()]


def _write_added(paths: list[str]) -> None:
    QSettings().setValue(ADDED_MATCAPS_KEY, "\n".join(paths[:_ADDED_LIMIT]))


def added_matcaps(folder: list[Path] | None = None) -> list[Path]:
    """The matcaps added from outside the folder that are still on disk, newest first.

    One that has since been copied into the folder is listed there instead,
    and one whose file has gone is left out without being forgotten -- an
    external drive comes back.
    """
    listed = {path.resolve() for path in (folder if folder is not None else available_matcaps())}
    seen: set[Path] = set()
    found = []
    for line in _read_added():
        path = Path(line)
        key = path.resolve()
        if key in seen or key in listed or not path.is_file():
            continue
        seen.add(key)
        found.append(path)
    return found


def remember_matcap(path: str | Path) -> None:
    """Keep ``path`` in the gallery from now on."""
    path = str(Path(path))
    _write_added([path, *(line for line in _read_added() if Path(line) != Path(path))])


def forget_matcap(path: str | Path) -> None:
    """Take ``path`` out of the gallery; the file itself is left alone."""
    _write_added([line for line in _read_added() if Path(line) != Path(path)])


class MatcapPanel(Panel):
    """Picks the matcap image and tunes how it is sampled."""

    def _build(self) -> None:
        """A draggable split: thumbnails above, adjustments below.

        The gallery is the one control that benefits from as much room as the
        artist wants to give it, so it gets a splitter rather than a fixed
        height, and the adjustments under it scroll in whatever is left.
        """
        self._gallery = QListWidget()
        self._gallery.setViewMode(QListWidget.ViewMode.IconMode)
        self._gallery.setIconSize(_THUMBNAIL)
        self._gallery.setGridSize(QSize(_THUMBNAIL.width() + 16, _THUMBNAIL.height() + 22))
        self._gallery.setResizeMode(QListWidget.ResizeMode.Adjust)
        self._gallery.setMovement(QListWidget.Movement.Static)
        self._gallery.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self._gallery.setMinimumHeight(90)
        self._gallery.setWordWrap(True)
        self._gallery.itemSelectionChanged.connect(self._on_selected)
        self._gallery.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._gallery.customContextMenuRequested.connect(self._gallery_menu)

        controls = QWidget()
        column = QVBoxLayout(controls)
        column.setContentsMargins(0, 8, 0, 0)
        column.setSpacing(8)

        buttons = QWidget()
        row = QHBoxLayout(buttons)
        row.setContentsMargins(0, 0, 0, 0)
        browse_button = QPushButton("Load Matcap...")
        browse_button.clicked.connect(self.browse)
        rescan = symbol_button("refresh", "Rescan Folder")
        rescan.clicked.connect(self.reload_gallery)
        row.addWidget(browse_button)
        row.addWidget(rescan)
        column.addWidget(buttons)

        # The disc goes straight into the column, outside any group.  Every
        # other group in the application folds, and a control that is the
        # whole point of the panel should not be one click on a bar away from
        # being gone -- least of all a click on a bar named Adjustments, which
        # is what the disc now is.
        self._preview = MatcapPreview()
        column.addWidget(self._preview)

        # The two settings a disc cannot be dragged into: a tint is a colour
        # and wants a picker, and a flip is a yes or a no.
        box, form = form_group("Adjustments")
        self._tint = ColorButton((1.0, 1.0, 1.0))
        self._flip_y = QCheckBox("Flip vertically")
        form.addRow("Tint", self._tint)
        form.addRow("", self._flip_y)
        column.addWidget(box)

        # The same five numbers the disc sets, for when a number is what you
        # want -- to type an exact rotation, or to pull one of them out into a
        # panel of your own, which a copy of the disc could not do one at a
        # time.  Folded, because reaching for them is the exception now.
        fine, numbers = collapsible_group("Fine Adjustments")
        self._rotation = SliderSpin(-180.0, 180.0, 0.0, decimals=0, step=1.0, suffix=" deg")
        self._contrast = SliderSpin(0.0, 3.0, 1.0)
        self._gamma = SliderSpin(0.1, 3.0, 1.0)
        self._brightness = SliderSpin(0.0, 3.0, 1.0)
        self._saturation = SliderSpin(0.0, 3.0, 1.0)
        numbers.addRow("Rotation", self._rotation)
        numbers.addRow("Contrast", self._contrast)
        numbers.addRow("Gamma", self._gamma)
        numbers.addRow("Brightness", self._brightness)
        numbers.addRow("Saturation", self._saturation)
        column.addWidget(fine)

        reset = QPushButton("Reset Adjustments")
        reset.clicked.connect(self._reset)
        column.addWidget(reset)
        column.addStretch(1)

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(self._gallery)
        splitter.addWidget(scrollable(controls))
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setChildrenCollapsible(False)
        splitter.setSizes([_GALLERY_HEIGHT, 400])
        self._add(splitter)

        self._rotation.valueChanged.connect(lambda v: self._apply("rotation_deg", v))
        self._contrast.valueChanged.connect(lambda v: self._apply("contrast", v))
        self._gamma.valueChanged.connect(lambda v: self._apply("gamma", v))
        self._brightness.valueChanged.connect(lambda v: self._apply("brightness", v))
        self._saturation.valueChanged.connect(lambda v: self._apply("saturation", v))
        self._tint.colorChanged.connect(lambda v: self._apply("tint", v))
        self._flip_y.toggled.connect(lambda v: self._apply("flip_y", v))

        # The disc writes the settings itself, being pointed at the same
        # object the sliders write; what is left to do is tell the renderer
        # and put the numbers back in line with what the drag did.
        self._preview.changed.connect(self._preview_changed)
        self.state.matcap_changed.connect(self._matcap_changed)

        self.reload_gallery()
        self._matcap_changed()

    # -- gallery --------------------------------------------------------

    def reload_gallery(self) -> None:
        """Rebuild the thumbnail list: the built-in, the ones added, then the folder."""
        with self._suppressed():
            self._gallery.clear()
            builtin = QListWidgetItem("Built-in")
            builtin.setData(Qt.ItemDataRole.UserRole, None)
            builtin.setToolTip("Neutral studio matcap generated at runtime")
            self._gallery.addItem(builtin)
            folder = available_matcaps()
            for path in added_matcaps(folder):
                self._add_item(path, f"{path}\n(added -- right-click to remove)", added=True)
            for path in folder:
                self._add_item(path, str(path))
        self._select_current()

    def _add_item(self, path: Path, tooltip: str, added: bool = False) -> None:
        item = QListWidgetItem(path.stem)
        item.setData(Qt.ItemDataRole.UserRole, str(path))
        item.setData(_ADDED_ROLE, added)
        item.setToolTip(tooltip)
        item.setIcon(_thumbnail(str(path)))
        self._gallery.addItem(item)

    def _adopt_current(self) -> None:
        """Put the matcap on the model into the gallery, if it came from somewhere else.

        However it arrived -- loaded, dropped on the window, opened from the
        File menu or brought in by a session -- a matcap the gallery does not
        list is remembered and shown, so it can be picked again later.
        """
        current = self.state.render.matcap_path
        if current is None:
            return
        path = Path(current)
        if any(path == Path(listed) for listed in self._listed()):
            return
        remember_matcap(path)
        self.reload_gallery()

    def _listed(self) -> list[str]:
        return [
            stored
            for index in range(self._gallery.count())
            if (stored := self._gallery.item(index).data(Qt.ItemDataRole.UserRole)) is not None
        ]

    def _gallery_menu(self, point) -> None:
        item = self._gallery.itemAt(point)
        if item is None or not item.data(_ADDED_ROLE):
            return
        menu = QMenu(self)
        remove = menu.addAction("Remove from Gallery")
        if menu.exec(self._gallery.viewport().mapToGlobal(point)) is remove:
            forget_matcap(Path(item.data(Qt.ItemDataRole.UserRole)))
            self.reload_gallery()

    def _select_current(self) -> None:
        current = self.state.render.matcap_path
        with self._suppressed():
            for index in range(self._gallery.count()):
                item = self._gallery.item(index)
                stored = item.data(Qt.ItemDataRole.UserRole)
                if (stored is None and current is None) or (
                    stored is not None and current is not None and Path(stored) == Path(current)
                ):
                    self._gallery.setCurrentItem(item)
                    return
            self._gallery.clearSelection()

    def _on_selected(self) -> None:
        if self._busy:
            return
        item = self._gallery.currentItem()
        if item is None:
            return
        self._load(item.data(Qt.ItemDataRole.UserRole))

    def browse(self) -> None:
        start = matcap_dir()
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Matcap",
            str(start if start.is_dir() else Path.home()),
            "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp)",
        )
        if path:
            self._load(path)

    def _load(self, path: str | None) -> None:
        try:
            self.state.load_matcap(path)
        except MatcapLoadError as error:
            QMessageBox.warning(self, "Matcap", str(error))
            return
        self._select_current()

    # -- adjustments ----------------------------------------------------

    def _apply(self, field: str, value) -> None:
        if self._busy:
            return
        setattr(self.state.render.matcap, field, value)
        self._preview.refresh()
        self.state.notify_render()

    def _preview_changed(self) -> None:
        """The disc was dragged: show the renderer and the numbers what it did."""
        if self._busy:
            return
        self._sync_adjustments()
        self.state.notify_render()

    def _matcap_changed(self) -> None:
        """A different matcap: the disc draws whichever one is on the model."""
        self._preview.set_settings(self.state.render.matcap)
        self._preview.set_source(self.state.matcap_pixels)
        self._adopt_current()
        self._select_current()

    def _reset(self) -> None:
        self.state.render.matcap = MatcapSettings()
        self.state.notify_render()
        self.refresh()

    def _sync_adjustments(self) -> None:
        """Put the numbers back in line with the settings, and redraw the disc.

        Separate from :meth:`refresh` because this runs on every event of a
        drag across the disc, and walking the gallery looking for the selected
        thumbnail -- which cannot have changed -- is not work worth doing sixty
        times a second.
        """
        matcap = self.state.render.matcap
        with self._suppressed():
            self._rotation.set_value(matcap.rotation_deg)
            self._contrast.set_value(matcap.contrast)
            self._gamma.set_value(matcap.gamma)
            self._brightness.set_value(matcap.brightness)
            self._saturation.set_value(matcap.saturation)
            self._tint.set_color(matcap.tint)
            self._flip_y.setChecked(matcap.flip_y)
        self._preview.set_settings(matcap)

    def refresh(self) -> None:
        self._sync_adjustments()
        self._select_current()
