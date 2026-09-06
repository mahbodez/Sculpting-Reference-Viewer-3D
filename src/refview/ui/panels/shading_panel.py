"""Shading mode, lighting, surface material and scene furniture controls."""

from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QComboBox, QPushButton

from ...core.settings import LightSettings, ShadingMode, SurfaceSettings
from ..widgets import ColorButton, SliderSpin, form_group
from .base import Panel


class ShadingPanel(Panel):
    """Chooses the shading model and edits its light and surface parameters."""

    def _build(self) -> None:
        box, form = form_group("Mode")
        self._mode = QComboBox()
        for mode in ShadingMode:
            self._mode.addItem(mode.label, mode.value)
        self._wireframe = QCheckBox("Show wireframe")
        self._wireframe_color = ColorButton((0.08, 0.09, 0.11))
        form.addRow("Shading", self._mode)
        form.addRow("", self._wireframe)
        form.addRow("Wire colour", self._wireframe_color)
        self._add(box)

        self._light_box, light_form = form_group("Light")
        self._azimuth = SliderSpin(-180.0, 180.0, 40.0, decimals=0, step=1.0, suffix=" deg")
        self._elevation = SliderSpin(-90.0, 90.0, 35.0, decimals=0, step=1.0, suffix=" deg")
        self._light_color = ColorButton((1.0, 1.0, 1.0))
        self._intensity = SliderSpin(0.0, 3.0, 1.0)
        self._fill = SliderSpin(0.0, 2.0, 0.25)
        self._ambient_color = ColorButton((0.42, 0.47, 0.55))
        self._ambient = SliderSpin(0.0, 2.0, 0.30)
        self._follow = QCheckBox("Light follows camera")
        light_form.addRow("Azimuth", self._azimuth)
        light_form.addRow("Elevation", self._elevation)
        light_form.addRow("Colour", self._light_color)
        light_form.addRow("Key", self._intensity)
        light_form.addRow("Fill", self._fill)
        light_form.addRow("Ambient", self._ambient)
        light_form.addRow("Ambient colour", self._ambient_color)
        light_form.addRow("", self._follow)
        self._add(self._light_box)

        self._surface_box, surface_form = form_group("Surface")
        self._diffuse = ColorButton((0.72, 0.70, 0.68))
        self._specular_color = ColorButton((1.0, 1.0, 1.0))
        self._specular_level = SliderSpin(0.0, 2.0, 0.4)
        self._shininess = SliderSpin(1.0, 256.0, 32.0, decimals=0, step=1.0)
        self._metalness = SliderSpin(0.0, 1.0, 0.0)
        self._roughness = SliderSpin(0.02, 1.0, 0.40)
        self._reflection = ColorButton((1.0, 1.0, 1.0))
        surface_form.addRow("Diffuse", self._diffuse)
        surface_form.addRow("Specular", self._specular_color)
        surface_form.addRow("Spec level", self._specular_level)
        surface_form.addRow("Shininess", self._shininess)
        surface_form.addRow("Metalness", self._metalness)
        surface_form.addRow("Roughness", self._roughness)
        surface_form.addRow("Reflection", self._reflection)
        self._add(self._surface_box)

        self._quality_box, quality_form = form_group("High Quality")
        self._quality_box.setToolTip(
            "Soft shadows and ambient occlusion, used by the High Quality shading mode"
        )
        self._shadows = QCheckBox("Soft shadows")
        self._shadow_strength = SliderSpin(0.0, 1.0, 0.55)
        self._shadow_softness = SliderSpin(0.0, 8.0, 2.0, decimals=1, step=0.5)
        self._shadow_bias = SliderSpin(0.0, 0.02, 0.0022, decimals=4, step=0.0005)
        self._shadow_bias.setToolTip("Raise this if a lit surface shadows itself in stripes")
        self._occlusion = QCheckBox("Ambient occlusion")
        self._ao_radius = SliderSpin(0.01, 0.4, 0.09, decimals=3)
        self._ao_intensity = SliderSpin(0.0, 2.0, 0.85)
        quality_form.addRow("", self._shadows)
        quality_form.addRow("Strength", self._shadow_strength)
        quality_form.addRow("Softness", self._shadow_softness)
        quality_form.addRow("Bias", self._shadow_bias)
        quality_form.addRow("", self._occlusion)
        quality_form.addRow("AO radius", self._ao_radius)
        quality_form.addRow("AO strength", self._ao_intensity)
        self._add(self._quality_box)

        pedestal_box, pedestal_form = form_group("Pedestal")
        self._pedestal = QCheckBox("Stand the model on a disc")
        self._pedestal_snap = QCheckBox("Sit at the lowest point")
        self._pedestal_level = SliderSpin(-1.0, 1.0, 0.0, decimals=3)
        self._pedestal_level.setToolTip("Height of the top face, in scene units")
        self._pedestal_diameter = SliderSpin(0.5, 4.0, 1.35)
        self._pedestal_thickness = SliderSpin(0.005, 0.5, 0.06, decimals=3)
        self._pedestal_color = ColorButton((0.34, 0.35, 0.38))
        pedestal_form.addRow("", self._pedestal)
        pedestal_form.addRow("", self._pedestal_snap)
        pedestal_form.addRow("Level", self._pedestal_level)
        pedestal_form.addRow("Diameter", self._pedestal_diameter)
        pedestal_form.addRow("Thickness", self._pedestal_thickness)
        pedestal_form.addRow("Colour", self._pedestal_color)
        self._add(pedestal_box)

        background_box, background_form = form_group("Background")
        self._background_top = ColorButton((0.26, 0.27, 0.30))
        self._background_bottom = ColorButton((0.10, 0.10, 0.12))
        background_form.addRow("Top", self._background_top)
        background_form.addRow("Bottom", self._background_bottom)
        self._add(background_box)

        reset = QPushButton("Reset Light and Surface")
        reset.clicked.connect(self._reset)
        self._add(reset)
        self._add_stretch()

        self._connect()

    def _connect(self) -> None:
        self._mode.currentIndexChanged.connect(self._on_mode_changed)
        self._wireframe.toggled.connect(
            lambda v: self._apply(self.state.render, "show_wireframe", v)
        )
        self._wireframe_color.colorChanged.connect(
            lambda v: self._apply(self.state.render, "wireframe_color", v)
        )
        self._background_top.colorChanged.connect(
            lambda v: self._apply(self.state.render, "background_top", v)
        )
        self._background_bottom.colorChanged.connect(
            lambda v: self._apply(self.state.render, "background_bottom", v)
        )

        self._azimuth.valueChanged.connect(self._light_setter("azimuth_deg"))
        self._elevation.valueChanged.connect(self._light_setter("elevation_deg"))
        self._light_color.colorChanged.connect(self._light_setter("color"))
        self._intensity.valueChanged.connect(self._light_setter("intensity"))
        self._fill.valueChanged.connect(self._light_setter("fill_intensity"))
        self._ambient.valueChanged.connect(self._light_setter("ambient_intensity"))
        self._ambient_color.colorChanged.connect(self._light_setter("ambient_color"))
        self._follow.toggled.connect(self._light_setter("follow_camera"))

        self._shadows.toggled.connect(self._quality_setter("show_shadows"))
        self._shadow_strength.valueChanged.connect(self._quality_setter("shadow_strength"))
        self._shadow_softness.valueChanged.connect(self._quality_setter("shadow_softness"))
        self._shadow_bias.valueChanged.connect(self._quality_setter("shadow_bias"))
        self._occlusion.toggled.connect(self._quality_setter("show_occlusion"))
        self._ao_radius.valueChanged.connect(self._quality_setter("ao_radius"))
        self._ao_intensity.valueChanged.connect(self._quality_setter("ao_intensity"))

        self._pedestal.toggled.connect(self._pedestal_setter("enabled"))
        self._pedestal_snap.toggled.connect(self._pedestal_setter("snap_to_lowest"))
        self._pedestal_level.valueChanged.connect(self._pedestal_setter("level"))
        self._pedestal_diameter.valueChanged.connect(self._pedestal_setter("diameter"))
        self._pedestal_thickness.valueChanged.connect(self._pedestal_setter("thickness"))
        self._pedestal_color.colorChanged.connect(self._pedestal_setter("color"))

        self._diffuse.colorChanged.connect(self._surface_setter("diffuse_color"))
        self._specular_color.colorChanged.connect(self._surface_setter("specular_color"))
        self._specular_level.valueChanged.connect(self._surface_setter("specular_level"))
        self._shininess.valueChanged.connect(self._surface_setter("shininess"))
        self._metalness.valueChanged.connect(self._surface_setter("metalness"))
        self._roughness.valueChanged.connect(self._surface_setter("roughness"))
        self._reflection.colorChanged.connect(self._surface_setter("reflection_color"))

    def _light_setter(self, field: str):
        """Slot that writes one field of the light settings."""
        return lambda value: self._apply(self.state.render.light, field, value)

    def _surface_setter(self, field: str):
        """Slot that writes one field of the surface settings."""
        return lambda value: self._apply(self.state.render.surface, field, value)

    def _quality_setter(self, field: str):
        """Slot that writes one field of the high-quality settings."""
        return lambda value: self._apply(self.state.render.quality, field, value)

    def _pedestal_setter(self, field: str):
        """Slot that writes one field of the pedestal settings."""
        return lambda value: self._apply(self.state.render.pedestal, field, value)

    # -- reactions ------------------------------------------------------

    def _apply(self, target, field: str, value) -> None:
        if self._busy:
            return
        setattr(target, field, value)
        self.state.notify_render()

    def _on_mode_changed(self, index: int) -> None:
        if self._busy:
            return
        self.state.render.shading_mode = ShadingMode(self._mode.itemData(index))
        self.state.notify_render()
        self.update_enabled()

    def update_enabled(self) -> None:
        mode = self.state.render.shading_mode
        self._light_box.setEnabled(mode.uses_lighting)
        self._surface_box.setEnabled(mode.uses_lighting)
        self._quality_box.setEnabled(mode.uses_quality)
        self._pedestal_level.setEnabled(not self.state.render.pedestal.snap_to_lowest)

    def _reset(self) -> None:
        self.state.render.light = LightSettings()
        self.state.render.surface = SurfaceSettings()
        self.state.notify_render()
        self.refresh()

    def refresh(self) -> None:
        render = self.state.render
        light, surface = render.light, render.surface
        quality, pedestal = render.quality, render.pedestal
        radius = self.state.camera.scene_radius
        with self._suppressed():
            self._shadows.setChecked(quality.show_shadows)
            self._shadow_strength.set_value(quality.shadow_strength)
            self._shadow_softness.set_value(quality.shadow_softness)
            self._shadow_bias.set_value(quality.shadow_bias)
            self._occlusion.setChecked(quality.show_occlusion)
            self._ao_radius.set_value(quality.ao_radius)
            self._ao_intensity.set_value(quality.ao_intensity)

            self._pedestal.setChecked(pedestal.enabled)
            self._pedestal_snap.setChecked(pedestal.snap_to_lowest)
            self._pedestal_level.set_range(-radius * 1.5, radius * 1.5)
            self._pedestal_level.set_value(pedestal.level)
            self._pedestal_diameter.set_value(pedestal.diameter)
            self._pedestal_thickness.set_value(pedestal.thickness)
            self._pedestal_color.set_color(pedestal.color)

            self._mode.setCurrentIndex(self._mode.findData(render.shading_mode.value))
            self._wireframe.setChecked(render.show_wireframe)
            self._wireframe_color.set_color(render.wireframe_color)
            self._background_top.set_color(render.background_top)
            self._background_bottom.set_color(render.background_bottom)

            self._azimuth.set_value(light.azimuth_deg)
            self._elevation.set_value(light.elevation_deg)
            self._light_color.set_color(light.color)
            self._intensity.set_value(light.intensity)
            self._fill.set_value(light.fill_intensity)
            self._ambient.set_value(light.ambient_intensity)
            self._ambient_color.set_color(light.ambient_color)
            self._follow.setChecked(light.follow_camera)

            self._diffuse.set_color(surface.diffuse_color)
            self._specular_color.set_color(surface.specular_color)
            self._specular_level.set_value(surface.specular_level)
            self._shininess.set_value(surface.shininess)
            self._metalness.set_value(surface.metalness)
            self._roughness.set_value(surface.roughness)
            self._reflection.set_color(surface.reflection_color)
        self.update_enabled()
