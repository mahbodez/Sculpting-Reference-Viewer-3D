"""Cross-section controls: the cutting plane, what it keeps and how it reads."""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QComboBox, QPushButton

from ...core.section import SectionAxis, SectionMode
from ..widgets import ColorButton, SliderSpin, form_group
from .base import Panel

#: Slider extent for the plane offset and the slab thickness, as multiples of
#: the scene radius.  Wide enough to push the plane clear of the model.
_OFFSET_SPAN = 1.2
_THICKNESS_SPAN = 1.0


class SectionPanel(Panel):
    """Slices the model with a plane and shows the profile at the cut."""

    def _build(self) -> None:
        box, form = form_group("Cross-section")
        self._enabled = QCheckBox("Cut the model")
        self._enabled.setToolTip("Slice the scene with a plane (Ctrl+K)")
        self._axis = QComboBox()
        for axis in SectionAxis:
            self._axis.addItem(axis.label, axis.value)
        self._from_view = QPushButton("Set Plane From View")
        self._from_view.setToolTip("Cut straight across the direction you are looking from")
        self._flip = QCheckBox("Flip the plane")
        self._offset = SliderSpin(-1.0, 1.0, 0.0, decimals=3)
        self._offset.setToolTip("Slide the plane along its normal, in scene units")
        form.addRow("", self._enabled)
        form.addRow("Plane", self._axis)
        form.addRow("", self._from_view)
        form.addRow("Offset", self._offset)
        form.addRow("", self._flip)
        self._add(box)

        keep_box, keep_form = form_group("Keep")
        self._mode = QComboBox()
        for mode in SectionMode:
            self._mode.addItem(mode.label, mode.value)
        self._thickness = SliderSpin(0.001, 1.0, 0.1, decimals=3)
        self._thickness.setToolTip("Thickness of the retained slice, in scene units")
        keep_form.addRow("Side", self._mode)
        keep_form.addRow("Slice", self._thickness)
        self._keep_form = keep_form
        self._add(keep_box)

        look_box, look_form = form_group("Appearance")
        self._contour = QCheckBox("Outline the cut")
        self._contour_color = ColorButton((1.0, 0.86, 0.35))
        self._contour_width = SliderSpin(0.5, 10.0, 2.5, decimals=1, step=0.5, suffix=" px")
        self._fill = QCheckBox("Fill the cut")
        self._fill.setToolTip("Flood the exposed interior so the cut reads as solid material")
        self._cap_color = ColorButton((0.62, 0.34, 0.30))
        look_form.addRow("", self._contour)
        look_form.addRow("Outline", self._contour_color)
        look_form.addRow("Width", self._contour_width)
        look_form.addRow("", self._fill)
        look_form.addRow("Cut colour", self._cap_color)
        self._look_form = look_form
        self._add(look_box)

        centre = QPushButton("Centre the Plane")
        centre.setToolTip("Put the plane back through the middle of the model")
        centre.clicked.connect(lambda: self._on_centre())
        self._add(centre)
        self._add_stretch()

        self._connect()

    def _connect(self) -> None:
        self._enabled.toggled.connect(lambda v: self._set("enabled", v))
        self._flip.toggled.connect(lambda v: self._set("flip", v, arms=True))
        self._offset.valueChanged.connect(lambda v: self._set("offset", v, arms=True))
        self._thickness.valueChanged.connect(lambda v: self._set("thickness", v, arms=True))
        self._contour.toggled.connect(lambda v: self._set("show_contour", v))
        self._contour_color.colorChanged.connect(lambda v: self._set("contour_color", v))
        self._contour_width.valueChanged.connect(lambda v: self._set("contour_width", v))
        self._fill.toggled.connect(lambda v: self._set("fill_cut", v))
        self._cap_color.colorChanged.connect(lambda v: self._set("cap_color", v))
        self._axis.currentIndexChanged.connect(self._on_axis)
        self._mode.currentIndexChanged.connect(self._on_mode)
        self._from_view.clicked.connect(self.set_plane_from_view)

    # -- reactions ------------------------------------------------------

    @property
    def _settings(self):
        return self.state.render.section

    def _set(self, field: str, value, arms: bool = False) -> None:
        """Write one field; ``arms`` also switches the cut on.

        Moving the plane is a clear enough sign the cut is wanted, whereas
        picking a colour for it is not.
        """
        if self._busy:
            return
        setattr(self._settings, field, value)
        if arms and not self._settings.enabled:
            self._settings.enabled = True
            with self._suppressed():
                self._enabled.setChecked(True)
        self.state.notify_render()
        self._update_enabled()

    def _on_axis(self, index: int) -> None:
        self._set("axis", SectionAxis(self._axis.itemData(index)), arms=True)

    def _on_mode(self, index: int) -> None:
        self._set("mode", SectionMode(self._mode.itemData(index)), arms=True)

    def _on_centre(self) -> None:
        self._set("offset", 0.0, arms=True)
        self.refresh()

    def toggle(self) -> None:
        """Turn the cut on or off, for the menu and the keyboard shortcut."""
        self._set("enabled", not self._settings.enabled)
        with self._suppressed():
            self._enabled.setChecked(self._settings.enabled)

    def set_plane_from_view(self) -> None:
        """Face the plane along the camera, so the cut squares up with the view."""
        direction = self.state.camera.forward
        self._settings.custom_normal = tuple(float(v) for v in -direction)
        self._settings.flip = False
        self._set("axis", SectionAxis.CUSTOM, arms=True)
        self.refresh()

    def _update_enabled(self) -> None:
        """Only the settings this cut has a use for.

        A thickness is what a slab is; the other two ways of keeping a cut have
        no thickness to set rather than a thickness of zero.  A colour for a
        line nobody is drawing is the same kind of nothing.
        """
        settings = self._settings
        self._keep_form.setRowVisible(self._thickness, settings.mode is SectionMode.SLAB)
        for widget in (self._contour_color, self._contour_width):
            self._look_form.setRowVisible(widget, settings.show_contour)
        self._look_form.setRowVisible(self._cap_color, settings.fill_cut)

    # -- refreshing -----------------------------------------------------

    def refresh(self) -> None:
        settings = self._settings
        radius = self.state.camera.scene_radius
        with self._suppressed():
            self._offset.set_range(-radius * _OFFSET_SPAN, radius * _OFFSET_SPAN)
            self._thickness.set_range(radius * 1e-3, radius * _THICKNESS_SPAN)
            self._enabled.setChecked(settings.enabled)
            self._axis.setCurrentIndex(self._axis.findData(settings.axis.value))
            self._mode.setCurrentIndex(self._mode.findData(settings.mode.value))
            self._flip.setChecked(settings.flip)
            self._offset.set_value(settings.offset)
            self._thickness.set_value(settings.thickness)
            self._contour.setChecked(settings.show_contour)
            self._contour_color.set_color(settings.contour_color)
            self._contour_width.set_value(settings.contour_width)
            self._fill.setChecked(settings.fill_cut)
            self._cap_color.set_color(settings.cap_color)
        self._update_enabled()
