"""Shading mode, lighting, surface material and scene furniture controls."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QComboBox, QFileDialog, QPushButton

from ...core.body_regions import (
    PROFILE_FIELDS,
    PROFILE_LABELS,
    PROFILE_RANGE,
    REGION_LABELS,
    REGIONS,
    BodyRegionSettings,
    RegionSource,
)
from ...core.grid import COUNT_MAX, COUNT_MIN, FADE_MAX, FADE_MIN
from ...core.settings import (
    CONTOUR_DENSITY_MAX,
    CONTOUR_DENSITY_MIN,
    ENVIRONMENT_BLUR_MAX,
    ENVIRONMENT_STRENGTH_MAX,
    ENVIRONMENT_STRENGTH_MIN,
    GHOST_MIN,
    ContourDirection,
    LightingMode,
    LightSettings,
    ShadingMode,
    SurfaceSettings,
)
from ...core.skin import SKIN_PRESETS, SKIN_RANGES, SkinSettings
from ...paths import available_environments, environment_dir
from ..widgets import ColorButton, SliderSpin, collapsible_group, form_group
from .base import Panel
from .matcap_panel import MatcapPanel


class ShadingPanel(Panel):
    """Chooses the shading model and edits its light and surface parameters."""

    def _build(self) -> None:
        box, form = form_group("Mode")
        self._mode_form = form
        self._mode = QComboBox()
        for mode in ShadingMode:
            self._mode.addItem(mode.label, mode.value)
        self._wireframe = QCheckBox("Show wireframe")
        self._wireframe_color = ColorButton((0.08, 0.09, 0.11))
        self._ghost = QCheckBox("Ghost (see through the model)")
        self._ghost.setToolTip(
            "Draw the model see-through, so you can read what is inside it:\n"
            "the far side of a form, the cut of a cross-section, or the\n"
            "armature standing in it."
        )
        self._ghost_opacity = SliderSpin(GHOST_MIN, 1.0, 0.35, decimals=2, step=0.05)
        form.addRow("Shading", self._mode)
        self._auto_smooth = QCheckBox("AutoSmooth")
        self._auto_smooth.setToolTip(
            "Shade the model smooth across gentle edges and hard across sharp\n"
            "ones, as 3ds Max's AutoSmooth does -- for a scan or a hard-surface\n"
            "model whose normals were lost or averaged over its creases.  Off,\n"
            "the model is shaded with the normals its file came with."
        )
        self._auto_smooth_deg = SliderSpin(0.0, 180.0, 30.0, decimals=0, step=1.0, suffix=" deg")
        self._auto_smooth_deg.setToolTip(
            "How sharp a turn stays hard.  Nought shades every triangle flat;\n"
            "a hundred and eighty smooths everything."
        )
        form.addRow("", self._auto_smooth)
        form.addRow("Smooth angle", self._auto_smooth_deg)
        form.addRow("", self._wireframe)
        form.addRow("Wire colour", self._wireframe_color)
        form.addRow("", self._ghost)
        form.addRow("Solidity", self._ghost_opacity)
        self._add(box)

        self.matcap_panel = MatcapPanel(self.state, self)
        self._add(self.matcap_panel)

        self._light_box, light_form = form_group("Light")
        self._light_box.setToolTip(
            "Shift + right-drag in the view turns the lights -- the key, the fill\n"
            "and the HDRI together.  Esc while dragging puts them back."
        )
        self._light_form = light_form
        self._lighting = QComboBox()
        for lighting in LightingMode:
            self._lighting.addItem(lighting.label, lighting.value)
        self._lighting.setToolTip(
            "What lights the model: the studio key, fill and ambient; an HDRI,\n"
            "a photograph of the light round a real place; or both."
        )
        light_form.addRow("Lighting", self._lighting)
        self._environment = QComboBox()
        self._environment.setToolTip("The HDRI: the ones that ship, and any you have loaded")
        self._environment_load = QPushButton("Load HDRI...")
        self._environment_load.setToolTip("Light with an .hdr or .exr panorama from disk")
        self._environment_strength = SliderSpin(
            ENVIRONMENT_STRENGTH_MIN, ENVIRONMENT_STRENGTH_MAX, 1.0, decimals=2, step=0.05
        )
        self._environment_strength.setToolTip(
            "How bright the HDRI is.  One lights a surface facing its brightest\n"
            "part as brightly as the studio key does, whatever the map's exposure."
        )
        self._environment_rotation = SliderSpin(
            -180.0, 180.0, 0.0, decimals=0, step=1.0, suffix=" deg"
        )
        self._environment_rotation.setToolTip("Turn the HDRI about the vertical")
        self._environment_background = QCheckBox("Show the HDRI behind the model")
        self._environment_blur = SliderSpin(0.0, ENVIRONMENT_BLUR_MAX, 2.0, decimals=1, step=0.5)
        self._environment_blur.setToolTip(
            "How blurred the HDRI is behind the model, so the room does not\n"
            "compete with the form"
        )
        self._environment_shadows = QCheckBox("Cast shadows from its brightest light")
        self._environment_shadows.setToolTip(
            "With the HDRI as the only light, cast the shadow map from the\n"
            "direction most of its light comes from.  Human Skin traces the\n"
            "whole map's shadows while it refines, whatever this says."
        )
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
        light_form.addRow("HDRI", self._environment)
        light_form.addRow("", self._environment_load)
        light_form.addRow("Strength", self._environment_strength)
        light_form.addRow("Rotation", self._environment_rotation)
        light_form.addRow("", self._environment_background)
        light_form.addRow("Blur", self._environment_blur)
        light_form.addRow("", self._environment_shadows)
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

        self._skin_box, skin_form = form_group("Human Skin")
        self._skin_preset = QComboBox()
        self._skin_preset.addItem("Custom")
        self._skin_preset.addItems(list(SKIN_PRESETS))
        self._skin_preset.setToolTip("Starting palettes; every skin tone can be adjusted below.")
        skin_form.addRow("Preset", self._skin_preset)
        self._skin_color = ColorButton(SkinSettings().color)
        self._skin_scatter = ColorButton(SkinSettings().scatter_color)
        skin_form.addRow("Skin colour", self._skin_color)
        skin_form.addRow("Scattering colour", self._skin_scatter)
        self._skin_controls = {}
        for field, label, decimals, step, suffix in (
            ("roughness", "Roughness", 2, 0.01, ""),
            ("specular", "Reflection strength", 2, 0.05, ""),
            ("oiliness", "Oily highlights", 2, 0.05, ""),
            ("sss", "Subsurface scattering", 2, 0.05, ""),
            ("radius", "Scattering depth", 3, 0.001, " × radius"),
            ("transmission", "Backlight transmission", 2, 0.05, ""),
            ("detail", "Surface detail", 2, 0.05, ""),
            ("pore_size", "Pore size", 4, 0.0005, " × radius"),
            ("mottle", "Tone variation", 2, 0.05, ""),
            ("blood", "Blood / flush", 2, 0.05, ""),
            ("veins", "Subtle veins", 2, 0.05, ""),
            ("fuzz", "Peach fuzz", 2, 0.05, ""),
            ("blemishes", "Blemishes", 2, 0.05, ""),
            ("freckles", "Freckles", 2, 0.05, ""),
            ("nevi", "Moles", 2, 0.05, ""),
            ("acne", "Acne", 2, 0.05, ""),
            ("light_size", "Light angular radius", 1, 0.5, " deg"),
            ("indirect", "Indirect light", 2, 0.05, ""),
            ("exposure", "Exposure", 1, 0.1, " EV"),
            ("samples", "Refinement samples", 0, 8, ""),
            ("resolution", "Refinement resolution", 2, 0.05, " × viewport"),
        ):
            low, high = SKIN_RANGES[field]
            control = SliderSpin(low, high, getattr(SkinSettings(), field),
                                 decimals=decimals, step=step, suffix=suffix)
            control.setObjectName("skin_" + field)
            skin_form.addRow(label, control)
            self._skin_controls[field] = control
            control.valueChanged.connect(self._skin_setter(field))
        self._skin_controls["radius"].setToolTip(
            "Fraction of model radius. Adjust for a head versus a full figure; OBJ has no units."
        )
        self._skin_controls["detail"].setToolTip(
            "Pores and furrows bumped into the surface from a tileable volume,\n"
            "so no UV layout is needed. Highlights see the full relief; diffuse\n"
            "sees a third of it and scattering none, as on real skin."
        )
        self._skin_controls["pore_size"].setToolTip(
            "Spacing of the pores as a fraction of model radius. Roughly 0.003 for a\n"
            "full figure and 0.0015 for a head."
        )
        self._skin_controls["mottle"].setToolTip("Uneven pigment: lighter and darker patches.")
        self._skin_controls["blood"].setToolTip(
            "Flush from blood under the surface: reddens patches, cavities and backlight."
        )
        self._skin_controls["veins"].setToolTip(
            "Faint cool vessels on the surface; they absorb more backlight through thin skin."
        )
        self._skin_controls["fuzz"].setToolTip("Soft rim from vellus hair at grazing angles.")
        self._skin_controls["blemishes"].setToolTip(
            "Patches, coarser than the pores, of irritated redness and of dry,\n"
            "duller skin.  Where they fall is the Body Regions group's business."
        )
        self._skin_controls["freckles"].setToolTip(
            "Small light-brown dots, thick on the ground: a pore or two across."
        )
        self._skin_controls["nevi"].setToolTip(
            "Moles: dark, a few pores across, faintly raised, few and far between."
        )
        self._skin_controls["acne"].setToolTip(
            "Red papules, raised and shining; some come to a pale head.\n"
            "Turned up on the face, the chest and the back by the Body Regions group."
        )
        self._skin_progressive = QCheckBox("Refine while idle")
        self._skin_progressive.setToolTip(
            "Trace soft shadows, one indirect bounce and approximate skin scattering.\n"
            "Navigation and ghost mode use the fast preview."
        )
        skin_form.addRow("", self._skin_progressive)
        self._skin_preset.activated.connect(self._apply_skin_preset)
        self._skin_color.colorChanged.connect(self._skin_setter("color"))
        self._skin_scatter.colorChanged.connect(self._skin_setter("scatter_color"))
        self._skin_progressive.toggled.connect(self._skin_setter("progressive"))
        self._add(self._skin_box)
        self._build_body_regions()

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

        self._contour_box, contour_form = form_group("Contour")
        self._contour_box.setToolTip(
            "Parallel slices drawn across the form, used by the Contour shading mode.\n"
            "The lines crowd where the surface turns across the slices and spread\n"
            "where it runs along them, so curves and flats read at a glance."
        )
        self._contour_direction = QComboBox()
        for direction in ContourDirection:
            self._contour_direction.addItem(direction.label, direction.value)
        self._contour_from_view = QPushButton("Slice Along the View")
        self._contour_from_view.setToolTip(
            "Fix the slices the way the camera faces right now, so they stay put\n"
            "when the view turns"
        )
        self._contour_density = SliderSpin(
            CONTOUR_DENSITY_MIN, CONTOUR_DENSITY_MAX, 32.0, decimals=0, step=1.0
        )
        self._contour_density.setToolTip("How many slices fall across the model")
        self._contour_width = SliderSpin(0.5, 6.0, 1.4, decimals=1, step=0.1, suffix=" px")
        self._contour_color = ColorButton((0.10, 0.11, 0.14))
        self._contour_paper = ColorButton((0.90, 0.88, 0.84))
        self._contour_lit = QCheckBox("Light the paper between the lines")
        contour_form.addRow("Slices", self._contour_direction)
        contour_form.addRow("", self._contour_from_view)
        contour_form.addRow("Density", self._contour_density)
        contour_form.addRow("Line width", self._contour_width)
        contour_form.addRow("Line colour", self._contour_color)
        contour_form.addRow("Paper", self._contour_paper)
        contour_form.addRow("", self._contour_lit)
        self._add(self._contour_box)

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
        self._pedestal_form = pedestal_form
        pedestal_form.addRow("Diameter", self._pedestal_diameter)
        pedestal_form.addRow("Thickness", self._pedestal_thickness)
        pedestal_form.addRow("Colour", self._pedestal_color)
        self._add(pedestal_box)

        grid_box, grid_form = form_group("Grid")
        self._grid_ground = QCheckBox("Ground (XZ)")
        self._grid_ground.setToolTip("A floor of squares under the scene")
        self._grid_front = QCheckBox("Front wall (XY)")
        self._grid_front.setToolTip("A wall of squares behind the model, read from the front")
        self._grid_side = QCheckBox("Side wall (YZ)")
        self._grid_side.setToolTip("A wall of squares beside the model, read from the side")
        self._grid_count = SliderSpin(COUNT_MIN, COUNT_MAX, 20, decimals=0, step=1)
        self._grid_count.setToolTip("Lines from the centre of the grid to each of its edges")
        self._grid_spacing = SliderSpin(0.0, 1.0, 0.0, decimals=4)
        self._grid_spacing.setToolTip(
            "Distance between lines, in scene units.  Nought picks a round number\n"
            "that puts the grid a little wider than the scene."
        )
        self._grid_major = SliderSpin(0, 20, 10, decimals=0, step=1)
        self._grid_major.setToolTip("Every this-many lines a heavier one is drawn; nought for none")
        self._grid_fade = SliderSpin(FADE_MIN, FADE_MAX, 2.5, decimals=1, step=0.1)
        self._grid_fade.setToolTip(
            "How far the lines reach before they have faded away, as a multiple\n"
            "of the camera's distance to the grid.  Nought draws them all alike."
        )
        self._grid_opacity = SliderSpin(0.05, 1.0, 0.55, decimals=2, step=0.05)
        self._grid_width = SliderSpin(0.5, 4.0, 1.0, decimals=1, step=0.1)
        self._grid_color = ColorButton((0.55, 0.56, 0.60))
        self._grid_axes = QCheckBox("Colour the axes")
        self._grid_axes.setToolTip("Draw the X, Y and Z lines through the grid in their own colour")
        self._grid_floor = QCheckBox("Ground sits under the scene")
        self._grid_floor.setToolTip(
            "Put the ground grid at the scene's lowest point rather than through\n"
            "the origin, so it never cuts the model in two."
        )
        for widget in (self._grid_ground, self._grid_front, self._grid_side):
            grid_form.addRow("", widget)
        grid_form.addRow("Lines", self._grid_count)
        grid_form.addRow("Spacing", self._grid_spacing)
        grid_form.addRow("Heavy every", self._grid_major)
        grid_form.addRow("Fade", self._grid_fade)
        grid_form.addRow("Opacity", self._grid_opacity)
        grid_form.addRow("Line width", self._grid_width)
        grid_form.addRow("Colour", self._grid_color)
        grid_form.addRow("", self._grid_axes)
        grid_form.addRow("", self._grid_floor)
        self._add(grid_box)

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
        self._auto_smooth.toggled.connect(
            lambda v: self._apply(self.state.render, "auto_smooth", v)
        )
        self._auto_smooth_deg.valueChanged.connect(
            lambda v: self._apply(self.state.render, "auto_smooth_deg", v)
        )
        self._ghost.toggled.connect(lambda v: self._apply(self.state.render, "ghost", v))
        self._ghost_opacity.valueChanged.connect(
            lambda v: self._apply(self.state.render, "ghost_opacity", v)
        )
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
        self._lighting.currentIndexChanged.connect(self._on_lighting)
        self._environment.activated.connect(self._on_environment_chosen)
        self._environment_load.clicked.connect(self.browse_environment)
        self._environment_strength.valueChanged.connect(
            self._light_setter("environment_strength")
        )
        self._environment_rotation.valueChanged.connect(
            self._light_setter("environment_rotation_deg")
        )
        self._environment_background.toggled.connect(
            self._light_setter("environment_background")
        )
        self._environment_blur.valueChanged.connect(self._light_setter("environment_blur"))
        self._environment_shadows.toggled.connect(self._light_setter("environment_shadows"))
        self.state.environment_changed.connect(self._refresh_environments)

        self._shadows.toggled.connect(self._quality_setter("show_shadows"))
        self._shadow_strength.valueChanged.connect(self._quality_setter("shadow_strength"))
        self._shadow_softness.valueChanged.connect(self._quality_setter("shadow_softness"))
        self._shadow_bias.valueChanged.connect(self._quality_setter("shadow_bias"))
        self._occlusion.toggled.connect(self._quality_setter("show_occlusion"))
        self._ao_radius.valueChanged.connect(self._quality_setter("ao_radius"))
        self._ao_intensity.valueChanged.connect(self._quality_setter("ao_intensity"))

        self._contour_direction.currentIndexChanged.connect(self._on_contour_direction)
        self._contour_from_view.clicked.connect(self.slice_along_view)
        self._contour_density.valueChanged.connect(self._contour_setter("density"))
        self._contour_width.valueChanged.connect(self._contour_setter("line_width"))
        self._contour_color.colorChanged.connect(self._contour_setter("line_color"))
        self._contour_paper.colorChanged.connect(self._contour_setter("paper_color"))
        self._contour_lit.toggled.connect(self._contour_setter("lit"))

        self._pedestal.toggled.connect(self._pedestal_setter("enabled"))
        self._pedestal_snap.toggled.connect(self._pedestal_setter("snap_to_lowest"))
        self._pedestal_level.valueChanged.connect(self._pedestal_setter("level"))
        self._pedestal_diameter.valueChanged.connect(self._pedestal_setter("diameter"))
        self._pedestal_thickness.valueChanged.connect(self._pedestal_setter("thickness"))
        self._pedestal_color.colorChanged.connect(self._pedestal_setter("color"))

        self._grid_ground.toggled.connect(self._grid_setter("ground"))
        self._grid_front.toggled.connect(self._grid_setter("front"))
        self._grid_side.toggled.connect(self._grid_setter("side"))
        self._grid_count.valueChanged.connect(lambda v: self._grid_setter("count")(int(v)))
        self._grid_spacing.valueChanged.connect(self._grid_setter("spacing"))
        self._grid_major.valueChanged.connect(lambda v: self._grid_setter("major_every")(int(v)))
        self._grid_fade.valueChanged.connect(self._grid_setter("fade"))
        self._grid_opacity.valueChanged.connect(self._grid_setter("opacity"))
        self._grid_width.valueChanged.connect(self._grid_setter("line_width"))
        self._grid_color.colorChanged.connect(self._grid_setter("color"))
        self._grid_axes.toggled.connect(self._grid_setter("show_axes"))
        self._grid_floor.toggled.connect(self._grid_setter("at_floor"))

        self._diffuse.colorChanged.connect(self._surface_setter("diffuse_color"))
        self._specular_color.colorChanged.connect(self._surface_setter("specular_color"))
        self._specular_level.valueChanged.connect(self._surface_setter("specular_level"))
        self._shininess.valueChanged.connect(self._surface_setter("shininess"))
        self._metalness.valueChanged.connect(self._surface_setter("metalness"))
        self._roughness.valueChanged.connect(self._surface_setter("roughness"))
        self._reflection.colorChanged.connect(self._surface_setter("reflection_color"))

    def _build_body_regions(self) -> None:
        """Where on the body skin effects appear, and their relative strength."""
        self._body_box, form = collapsible_group("Body Regions")
        self._body_box.setToolTip(
            "Acne gathers on the face and the back, freckles on the arms, the\n"
            "knuckles run red: marks and subtle veins are scaled by where on the body\n"
            "the skin is.  The regions come from a skeleton with humanoid\n"
            "roles when the scene has one, else from the height bands of a\n"
            "standing figure; a bust or a hand is best told what it is."
        )
        self._region_source = QComboBox()
        for source in RegionSource:
            self._region_source.addItem(source.label, source.value)
        self._region_source.setToolTip(
            "Where the regions come from.  A skeleton with humanoid roles --\n"
            "the preset, a rig read by its names, one grown from the guided\n"
            "armature -- places every limb; height bands only tell the head,\n"
            "the torso and the legs of a standing figure apart."
        )
        form.addRow("Regions from", self._region_source)
        self._region_whole = QComboBox()
        for region in REGIONS:
            self._region_whole.addItem(REGION_LABELS[region], region)
        self._region_whole.setToolTip("What the whole model is, for a bust, a hand or a foot")
        form.addRow("Whole model is", self._region_whole)
        self._body_form = form

        self._region_edited = QComboBox()
        for region in REGIONS:
            self._region_edited.addItem(REGION_LABELS[region], region)
        self._region_edited.setToolTip("Which region the multipliers below are for")
        form.addRow("Region", self._region_edited)
        self._region_controls: dict[str, SliderSpin] = {}
        low, high = PROFILE_RANGE
        for field in PROFILE_FIELDS:
            control = SliderSpin(low, high, 1.0, decimals=2, step=0.05, suffix=" ×")
            control.setObjectName("region_" + field)
            control.setToolTip(
                f"How much of the {PROFILE_LABELS[field].lower()} slider this region gets:\n"
                "1 is the slider as it is, 0 none, 3 three times as much."
            )
            form.addRow(PROFILE_LABELS[field], control)
            self._region_controls[field] = control
            control.valueChanged.connect(self._region_setter(field))
        reset = QPushButton("Reset Regions")
        reset.setToolTip("Restore each region's skin effect multipliers")
        reset.clicked.connect(self._reset_regions)
        form.addRow("", reset)
        self._add(self._body_box)

        self._region_source.currentIndexChanged.connect(self._on_region_source)
        self._region_whole.currentIndexChanged.connect(self._on_region_whole)
        self._region_edited.currentIndexChanged.connect(lambda _i: self._refresh_regions())

    def _regions(self) -> BodyRegionSettings:
        skin = self.state.render.skin
        if not isinstance(skin.regions, BodyRegionSettings):
            skin.regions = BodyRegionSettings()
        return skin.regions

    def _on_region_source(self, index: int) -> None:
        if self._busy:
            return
        self._regions().source = RegionSource(self._region_source.itemData(index))
        self.state.notify_render()
        self._refresh_regions()

    def _on_region_whole(self, index: int) -> None:
        if self._busy:
            return
        self._regions().whole = str(self._region_whole.itemData(index))
        self.state.notify_render()

    def _region_setter(self, field: str):
        def change(value):
            if self._busy:
                return
            region = str(self._region_edited.currentData())
            self._apply(self._regions().profile(region), field, float(value))

        return change

    def _reset_regions(self) -> None:
        self.state.render.skin.regions = BodyRegionSettings()
        self.state.notify_render()
        self._refresh_regions()

    def _refresh_regions(self) -> None:
        regions = self._regions().bounded()
        with self._suppressed():
            self._region_source.setCurrentIndex(
                max(self._region_source.findData(regions.source.value), 0)
            )
            self._region_whole.setCurrentIndex(max(self._region_whole.findData(regions.whole), 0))
            edited = self._region_edited.currentData() or REGIONS[0]
            profile = regions.profile(edited)
            for field, control in self._region_controls.items():
                control.set_value(getattr(profile, field))
        self._body_form.setRowVisible(
            self._region_whole, regions.source is RegionSource.WHOLE
        )

    def _light_setter(self, field: str):
        """Slot that writes one field of the light settings."""
        return lambda value: self._apply(self.state.render.light, field, value)

    # -- the HDRI -------------------------------------------------------

    def _on_lighting(self, index: int) -> None:
        if self._busy:
            return
        self.state.render.light.mode = LightingMode(self._lighting.itemData(index))
        self.state.ensure_environment()
        self.state.notify_render()

    def _on_environment_chosen(self, index: int) -> None:
        path = self._environment.itemData(index)
        if path:
            self.state.load_environment(path, light=True)

    def browse_environment(self) -> None:
        """Pick an HDRI from disk and light with it."""
        current = self.state.render.light.environment_path
        start = Path(current).parent if current else environment_dir()
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Load HDRI",
            str(start if start.is_dir() else Path.home()),
            "HDRI panoramas (*.hdr *.exr)",
        )
        if path:
            self.state.load_environment(path, light=True)

    def _refresh_environments(self) -> None:
        """List the bundled HDRIs, and the one in use if it is from elsewhere."""
        current = self.state.render.light.environment_path
        paths = [str(path) for path in available_environments()]
        if current and all(Path(current) != Path(path) for path in paths):
            paths.insert(0, current)
        if not current and paths:
            current = paths[0]
        with self._suppressed():
            self._environment.clear()
            for path in paths:
                self._environment.addItem(Path(path).stem, path)
                self._environment.setItemData(
                    self._environment.count() - 1, path, Qt.ItemDataRole.ToolTipRole
                )
            if not paths:
                self._environment.addItem("None -- load one", None)
            chosen = next(
                (i for i, path in enumerate(paths) if current and Path(path) == Path(current)), 0
            )
            self._environment.setCurrentIndex(chosen)

    def refresh_light(self) -> None:
        """Put the light's numbers back in line with the settings, after a drag or an undo."""
        light = self.state.render.light
        with self._suppressed():
            self._azimuth.set_value(light.azimuth_deg)
            self._elevation.set_value(light.elevation_deg)
            self._environment_rotation.set_value(light.environment_rotation_deg)
            self._lighting.setCurrentIndex(max(self._lighting.findData(light.mode.value), 0))

    def _skin_setter(self, field: str):
        def change(value):
            if self._busy:
                return
            self._skin_preset.setCurrentIndex(0)
            self._apply(self.state.render.skin, field, int(value) if field == "samples" else value)
        return change

    def _apply_skin_preset(self, index: int) -> None:
        preset = SKIN_PRESETS.get(self._skin_preset.itemText(index))
        if preset is None or self._busy:
            return
        current = self.state.render.skin
        # Tone belongs to the preset; scale, scene, quality and the marks --
        # which are a person's, not a complexion's -- stay as set.
        self.state.render.skin = replace(
            preset, samples=current.samples, resolution=current.resolution,
            progressive=current.progressive, light_size=current.light_size,
            exposure=current.exposure, indirect=current.indirect,
            detail=current.detail, pore_size=current.pore_size,
            blemishes=current.blemishes, freckles=current.freckles,
            nevi=current.nevi, acne=current.acne, veins=current.veins,
            regions=current.regions,
        )
        self.state.notify_render()
        self.refresh()
        self._skin_preset.setCurrentIndex(index)

    def _surface_setter(self, field: str):
        """Slot that writes one field of the surface settings."""
        return lambda value: self._apply(self.state.render.surface, field, value)

    def _quality_setter(self, field: str):
        """Slot that writes one field of the high-quality settings."""
        return lambda value: self._apply(self.state.render.quality, field, value)

    def _pedestal_setter(self, field: str):
        """Slot that writes one field of the pedestal settings."""
        return lambda value: self._apply(self.state.render.pedestal, field, value)

    def _contour_setter(self, field: str):
        """Slot that writes one field of the contour shading settings."""
        return lambda value: self._apply(self.state.render.contour, field, value)

    def _grid_setter(self, field: str):
        """Slot that writes one field of the grid settings."""
        return lambda value: self._apply(self.state.render.grid, field, value)

    def _on_contour_direction(self, index: int) -> None:
        if self._busy:
            return
        direction = ContourDirection(self._contour_direction.itemData(index))
        self._apply(self.state.render.contour, "direction", direction)

    def slice_along_view(self) -> None:
        """Freeze the slices the way the camera faces now.

        The view direction is the one an artist most often wants the slices
        along, and the one that will not hold still; this pins it, so the
        model can then be turned and the same slices read from the side.
        """
        contour = self.state.render.contour
        contour.custom_direction = tuple(float(v) for v in self.state.camera.forward)
        contour.direction = ContourDirection.CUSTOM
        self.state.notify_render()
        self.refresh()

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
        """Show what this mode is actually lit and shaded by, and hide the rest.

        A matcap carries its own light baked into a picture, so a light to
        aim and a surface to reflect it are not dimmed versions of themselves
        under one -- they are questions the mode does not answer.  Same for the
        pedestal's height once it has been told to sit on the lowest point of
        the model: the model is answering, and a slider that says otherwise is
        a slider that lies.
        """
        mode = self.state.render.shading_mode
        # The Forms panel has a ghost switch of its own, so this one follows
        # the setting rather than only writing it.
        with self._suppressed():
            self._ghost.setChecked(self.state.render.ghost)
        self._mode_form.setRowVisible(self._ghost_opacity, self.state.render.ghost)
        self._mode_form.setRowVisible(self._auto_smooth_deg, self.state.render.auto_smooth)
        self.matcap_panel.setVisible(mode is ShadingMode.MATCAP)
        with self._suppressed():
            self._mode.setCurrentIndex(self._mode.findData(mode.value))
        self._light_box.setVisible(mode.uses_lighting)
        light = self.state.render.light
        self.refresh_light()
        # The rig's rows when the rig lights the model, the map's when the
        # map does; a blur only for a map that is shown, and its shadow only
        # when it is the one light there is to cast one.
        for widget in (self._azimuth, self._elevation, self._light_color, self._intensity,
                       self._fill, self._ambient, self._ambient_color):
            self._light_form.setRowVisible(widget, light.mode.uses_studio)
        for widget in (self._environment, self._environment_load, self._environment_strength,
                       self._environment_rotation, self._environment_background):
            self._light_form.setRowVisible(widget, light.mode.uses_environment)
        self._light_form.setRowVisible(
            self._environment_blur,
            light.mode.uses_environment and light.environment_background,
        )
        self._light_form.setRowVisible(
            self._environment_shadows, light.mode is LightingMode.ENVIRONMENT
        )
        self._surface_box.setVisible(mode.uses_lighting and mode is not ShadingMode.HUMAN_SKIN)
        self._skin_box.setVisible(mode is ShadingMode.HUMAN_SKIN)
        self._body_box.setVisible(mode is ShadingMode.HUMAN_SKIN)
        self._quality_box.setVisible(mode is ShadingMode.HIGH_QUALITY)
        self._contour_box.setVisible(mode.uses_contour)
        self._pedestal_form.setRowVisible(
            self._pedestal_level, not self.state.render.pedestal.snap_to_lowest
        )

    def _reset(self) -> None:
        self.state.render.light = LightSettings()
        self.state.render.surface = SurfaceSettings()
        self.state.render.skin = SkinSettings()
        self.state.notify_render()
        self.refresh()

    def refresh(self) -> None:
        self.matcap_panel.refresh()
        render = self.state.render
        light, surface = render.light, render.surface
        quality, pedestal = render.quality, render.pedestal
        contour = render.contour
        radius = self.state.camera.scene_radius
        with self._suppressed():
            skin = render.skin.bounded()
            self._skin_preset.setCurrentIndex(0)
            self._skin_color.set_color(skin.color)
            self._skin_scatter.set_color(skin.scatter_color)
            self._skin_progressive.setChecked(skin.progressive)
            for field, control in self._skin_controls.items():
                control.set_value(getattr(skin, field))
        self._refresh_regions()
        with self._suppressed():
            self._contour_direction.setCurrentIndex(
                self._contour_direction.findData(contour.direction.value)
            )
            self._contour_density.set_value(contour.density)
            self._contour_width.set_value(contour.line_width)
            self._contour_color.set_color(contour.line_color)
            self._contour_paper.set_color(contour.paper_color)
            self._contour_lit.setChecked(contour.lit)

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

            grid = render.grid
            self._grid_ground.setChecked(grid.ground)
            self._grid_front.setChecked(grid.front)
            self._grid_side.setChecked(grid.side)
            self._grid_count.set_value(grid.count)
            # The spacing slider reaches a good share of the scene, and reads
            # nought as "pick one for me".
            self._grid_spacing.set_range(0.0, max(radius * 0.5, 1e-3))
            self._grid_spacing.set_value(grid.spacing)
            self._grid_major.set_value(grid.major_every)
            self._grid_fade.set_value(grid.fade)
            self._grid_opacity.set_value(grid.opacity)
            self._grid_width.set_value(grid.line_width)
            self._grid_color.set_color(grid.color)
            self._grid_axes.setChecked(grid.show_axes)
            self._grid_floor.setChecked(grid.at_floor)

            self._mode.setCurrentIndex(self._mode.findData(render.shading_mode.value))
            self._wireframe.setChecked(render.show_wireframe)
            self._auto_smooth.setChecked(render.auto_smooth)
            self._auto_smooth_deg.set_value(render.auto_smooth_deg)
            self._wireframe_color.set_color(render.wireframe_color)
            self._ghost.setChecked(render.ghost)
            self._ghost_opacity.set_value(render.ghost_opacity)
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
            self._environment_strength.set_value(light.environment_strength)
            self._environment_background.setChecked(light.environment_background)
            self._environment_blur.set_value(light.environment_blur)
            self._environment_shadows.setChecked(light.environment_shadows)
        self._refresh_environments()
        with self._suppressed():

            self._diffuse.set_color(surface.diffuse_color)
            self._specular_color.set_color(surface.specular_color)
            self._specular_level.set_value(surface.specular_level)
            self._shininess.set_value(surface.shininess)
            self._metalness.set_value(surface.metalness)
            self._roughness.set_value(surface.roughness)
            self._reflection.set_color(surface.reflection_color)
        self.update_enabled()
