"""The window the preferences are set in.

Built out of the same elements the panels are -- folding groups, sliders with
their names written into them, switches that look like buttons -- because a
preferences window that looked like a different application would be the one
place in the interface where the rules did not hold.  It is a
:class:`~refview.ui.elements.reflow.Reflow`, so widening it breaks the groups
into columns exactly as widening a dock does, and every control in it can be
Alt-dragged into a panel of the artist's own.  Somebody who changes the orbit
speed twice a week should be able to keep it beside the camera controls, and
there is no reason the preferences should be the one place that refuses.

Nothing is applied on the way out, because there is no way out to apply it on:
every change takes effect as it is made and is written down at once.  An OK
button exists to answer the question "what happens if I press Cancel", and
that question only arises because the window put the artist's settings
somewhere provisional in the first place.  The accent, the type size, the
orbit rate -- these are things you judge by looking at them, and a preview you
have to commit to is not a preview.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSettings, Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..core.preferences import (
    MAX_FONT_SIZE,
    MAX_SPEED,
    MIN_FONT_SIZE,
    MIN_SPEED,
    SAMPLE_COUNTS,
    Preferences,
)
from .elements.clone import watch_tree
from .elements.naming import name_tree, register
from .elements.reflow import Reflow
from .preferences import PreferenceStore
from .widgets import ColorButton, SliderSpin, form_group, name_sliders, relax_widths, scrollable

#: Where the window's size is remembered.
_GEOMETRY = "preferences/geometry"

#: The groups, in the order they appear, and what each one is called in the
#: Settings menu.  One list so that the menu and the window cannot come to
#: disagree about what the groups are.
GROUPS = ("interface", "navigation", "startup", "viewport", "folders")

_TITLES = {
    "interface": "Interface",
    "navigation": "Navigation",
    "startup": "Startup",
    "viewport": "Viewport",
    "folders": "Folders",
}


class SettingsWindow(QWidget):
    """Every preference, in groups, applied as it is changed."""

    def __init__(self, store: PreferenceStore, parent: QWidget | None = None) -> None:
        super().__init__(parent, Qt.WindowType.Window)
        self.setWindowTitle("Preferences")
        self.resize(460, 640)

        self._store = store
        self._busy = False
        self._groups: dict[str, QWidget] = {}

        self._body = Reflow()
        self._build()

        column = QVBoxLayout(self)
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(0)
        self._scroll = scrollable(self._body)
        column.addWidget(self._scroll, 1)
        column.addWidget(self._footer())

        name_sliders(self._body)
        relax_widths(self._body)
        name_tree(self._body, owner=self)
        register(self._body, "settings")
        watch_tree(self._body)

        self._store.changed.connect(self.refresh)
        self.refresh()

        close = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        close.activated.connect(self.close)
        saved = QSettings().value(_GEOMETRY)
        if saved is not None and not isinstance(saved, str):
            self.restoreGeometry(saved)

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def _build(self) -> None:
        """Fill in the groups.

        A switch with nothing to put in the caption column is given the whole
        row rather than the field half of one, because a group that happens to
        have a named row in it would otherwise indent its switches past that
        name, and the indent would be saying nothing.
        """
        self._build_interface()
        self._build_navigation()
        self._build_startup()
        self._build_viewport()
        self._build_folders()

    def _build_interface(self) -> None:
        box, form = form_group(_TITLES["interface"])
        self._accent = ColorButton((0.929, 0.545, 0.129))
        self._accent.setToolTip(
            "The one colour the interface uses for state: a switch that is on, "
            "the track of a slider, the dot beside a group's name."
        )
        self._font_size = SliderSpin(
            float(MIN_FONT_SIZE), float(MAX_FONT_SIZE), 11.0, decimals=0, step=1.0
        )
        self._fold_disabled = QCheckBox("Fold groups that go dead")
        self._fold_disabled.setToolTip(
            "A group whose settings cannot be used folds itself away, rather "
            "than staying open and greyed out."
        )
        self._restore_layout = QCheckBox("Restore the panel layout at start")

        form.addRow("Accent", self._accent)
        form.addRow("Type Size", self._font_size)
        form.addRow(self._fold_disabled)
        form.addRow(self._restore_layout)
        self._add("interface", box)

        self._accent.colorChanged.connect(lambda value: self._write("interface", "accent", value))
        self._font_size.valueCommitted.connect(
            lambda value: self._write("interface", "font_size", int(round(value)))
        )
        self._fold_disabled.toggled.connect(
            lambda value: self._write("interface", "fold_disabled", value)
        )
        self._restore_layout.toggled.connect(
            lambda value: self._write("interface", "restore_layout", value)
        )

    def _build_navigation(self) -> None:
        box, form = form_group(_TITLES["navigation"])
        self._orbit_speed = SliderSpin(MIN_SPEED, MAX_SPEED, 1.0, decimals=2, step=0.05)
        self._zoom_speed = SliderSpin(MIN_SPEED, MAX_SPEED, 1.0, decimals=2, step=0.05)
        self._invert_x = QCheckBox("Invert orbit left/right")
        self._invert_y = QCheckBox("Invert orbit up/down")

        form.addRow("Orbit Speed", self._orbit_speed)
        form.addRow("Zoom Speed", self._zoom_speed)
        form.addRow(self._invert_x)
        form.addRow(self._invert_y)
        self._add("navigation", box)

        self._orbit_speed.valueChanged.connect(
            lambda value: self._write("navigation", "orbit_speed", value)
        )
        self._zoom_speed.valueChanged.connect(
            lambda value: self._write("navigation", "zoom_speed", value)
        )
        self._invert_x.toggled.connect(
            lambda value: self._write("navigation", "invert_orbit_x", value)
        )
        self._invert_y.toggled.connect(
            lambda value: self._write("navigation", "invert_orbit_y", value)
        )

    def _build_startup(self) -> None:
        box, form = form_group(_TITLES["startup"])
        self._splash = QCheckBox("Show the splash screen")
        self._check_updates = QCheckBox("Check for updates")
        self._check_updates.setToolTip(
            "A quiet check on the way in, which says nothing unless there is a "
            "newer release."
        )
        self._reopen = QCheckBox("Carry on from last time")
        self._reopen.setToolTip(
            "Open whatever was last being worked on: the session, if one was "
            "saved, and otherwise the model that was open."
        )

        form.addRow(self._splash)
        form.addRow(self._check_updates)
        form.addRow(self._reopen)
        self._add("startup", box)

        self._splash.toggled.connect(lambda value: self._write("startup", "show_splash", value))
        self._check_updates.toggled.connect(
            lambda value: self._write("startup", "check_updates", value)
        )
        self._reopen.toggled.connect(
            lambda value: self._write("startup", "reopen_last_session", value)
        )

    def _build_viewport(self) -> None:
        box, form = form_group(_TITLES["viewport"])
        self._samples = QComboBox()
        for count in SAMPLE_COUNTS:
            self._samples.addItem("Off" if count == 0 else f"{count}x", count)
        self._samples.setToolTip("Takes effect the next time the application starts.")
        self._keep_awake = QCheckBox("Keep the machine awake")
        self._keep_awake.setToolTip(
            "While this window is the one in front.  An artist reads a pose for "
            "minutes at a time without touching the machine."
        )
        self._samples_note = QLabel("")
        self._samples_note.setWordWrap(True)
        note = self._samples_note
        self.set_samples_in_use(None)

        form.addRow("Multisampling", self._samples)
        form.addRow(self._keep_awake)
        form.addRow(note)
        self._add("viewport", box)

        self._samples.currentIndexChanged.connect(
            lambda _index: self._write("viewport", "samples", self._samples.currentData())
        )
        self._keep_awake.toggled.connect(
            lambda value: self._write("viewport", "keep_awake", value)
        )

    def _build_folders(self) -> None:
        box, form = form_group(_TITLES["folders"])
        self._matcaps = QLineEdit()
        self._matcaps.setPlaceholderText("The matcaps that ship with the application")
        self._matcaps.setToolTip(
            "A folder of your own to read matcaps from.  Leave it empty for the "
            "bundled ones."
        )
        browse = QPushButton("Browse...")
        clear = QPushButton("Use Bundled")
        row = QWidget()
        buttons = QHBoxLayout(row)
        buttons.setContentsMargins(0, 0, 0, 0)
        buttons.setSpacing(6)
        buttons.addWidget(browse, 1)
        buttons.addWidget(clear, 1)

        form.addRow("Matcaps", self._matcaps)
        form.addRow(row)
        self._add("folders", box)

        self._matcaps.editingFinished.connect(
            lambda: self._write("folders", "matcaps", self._matcaps.text().strip())
        )
        browse.clicked.connect(self._browse_matcaps)
        clear.clicked.connect(lambda: self._write("folders", "matcaps", ""))

    def _footer(self) -> QWidget:
        """The one button that is not a preference, and what the window is for."""
        strip = QWidget()
        row = QHBoxLayout(strip)
        row.setContentsMargins(10, 8, 10, 10)
        row.setSpacing(8)
        note = QLabel("Every change applies at once.")
        note.setWordWrap(True)
        defaults = QPushButton("Restore Defaults")
        defaults.clicked.connect(self._store.reset)
        close = QPushButton("Close")
        close.clicked.connect(self.close)
        row.addWidget(note, 1)
        row.addWidget(defaults, 0)
        row.addWidget(close, 0)
        return strip

    def set_samples_in_use(self, samples: int | None) -> None:
        """Say what the view is really drawing with, beside what was asked for.

        A sample count belongs to the framebuffer, which is made once when the
        view is, so changing this cannot take effect until the next start --
        and the only way to tell whether it ever did is to be told.  Left as a
        plain note about the restart when nobody has asked the view yet.
        """
        restart = "Multisampling is fixed when the view is made, so it takes a restart."
        if samples is None:
            self._samples_note.setText(restart)
        elif samples <= 1:
            self._samples_note.setText(f"Drawing without multisampling.  {restart}")
        else:
            self._samples_note.setText(f"Drawing at {samples}x now.  {restart}")

    def _add(self, key: str, box: QWidget) -> None:
        self._groups[key] = box
        self._body.add(box)

    # ------------------------------------------------------------------
    # Reading and writing
    # ------------------------------------------------------------------

    def _write(self, group: str, name: str, value) -> None:
        """Put one field back into the store, which applies and saves it."""
        if self._busy:
            return
        prefs = Preferences.from_dict(self._store.value.to_dict())
        setattr(getattr(prefs, group), name, value)
        self._store.set(prefs)

    def refresh(self) -> None:
        """Pull every control back into line with the store.

        Run when the window is built, and again whenever the store changes --
        which includes changes this window did not make, such as Restore
        Defaults, and changes made from a copy of one of these controls that
        the artist dragged into a panel of their own.
        """
        prefs = self._store.value
        self._busy = True
        try:
            self._accent.set_color(prefs.interface.accent)
            self._font_size.set_value(float(prefs.interface.font_size))
            self._fold_disabled.setChecked(prefs.interface.fold_disabled)
            self._restore_layout.setChecked(prefs.interface.restore_layout)

            self._orbit_speed.set_value(prefs.navigation.orbit_speed)
            self._zoom_speed.set_value(prefs.navigation.zoom_speed)
            self._invert_x.setChecked(prefs.navigation.invert_orbit_x)
            self._invert_y.setChecked(prefs.navigation.invert_orbit_y)

            self._splash.setChecked(prefs.startup.show_splash)
            self._check_updates.setChecked(prefs.startup.check_updates)
            self._reopen.setChecked(prefs.startup.reopen_last_session)

            index = self._samples.findData(prefs.viewport.samples)
            if index >= 0:
                self._samples.setCurrentIndex(index)
            self._keep_awake.setChecked(prefs.viewport.keep_awake)

            self._matcaps.setText(prefs.folders.matcaps)
        finally:
            self._busy = False

    def show_group(self, key: str) -> None:
        """Open one group and fold the rest, for the Settings menu's entries.

        Folding the others is not tidiness: the menu entry is a question about
        one group, and the answer is the group on its own with nothing else
        competing for the eye.  They are all one click from open again.
        """
        for name, box in self._groups.items():
            if hasattr(box, "set_expanded"):
                box.set_expanded(name == key)
        wanted = self._groups.get(key)
        if wanted is not None:
            self._scroll.ensureWidgetVisible(wanted)

    # ------------------------------------------------------------------
    # Odds and ends
    # ------------------------------------------------------------------

    def _browse_matcaps(self) -> None:
        start = self._matcaps.text().strip() or str(Path.home())
        folder = QFileDialog.getExistingDirectory(self, "Matcap Folder", start)
        if folder:
            self._matcaps.setText(folder)
            self._write("folders", "matcaps", folder)

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt contract
        QSettings().setValue(_GEOMETRY, self.saveGeometry())
        super().closeEvent(event)
