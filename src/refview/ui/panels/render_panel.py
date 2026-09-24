"""The Render panel: everything a path-traced render needs, from its size to its denoising.

The first group is all most renders need: a button, a size, a preset.  The
rest are there for when the defaults are not what is wanted -- sampling and
light paths for the noise and the time, the method and threads for how the
machine is used, the lens for depth of field, the film and colour for how
light becomes pixels, the denoiser, and the rendered viewport's own
settings.  The groups that are seldom needed start folded.

The look of the model is not set here: a render uses the Shading panel's
mode, surface, skin and lights as they are, so what the viewport shows is
what renders.  The one thing a mode without a material leaves open -- what a
matcap or normals model is made of -- is the clay at the bottom.
"""

from __future__ import annotations

from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QCheckBox, QComboBox, QLabel, QPushButton, QSpinBox

from ...core.path_trace import (
    CUSTOM_PRESET,
    PATH_TRACE_PRESETS,
    PATH_TRACE_RANGES,
    BucketOrder,
    DenoiserBackend,
    DenoiserDevice,
    DenoiserQuality,
    OutputFormat,
    PixelFilter,
    RenderMethod,
    ViewTransform,
    mode_note,
)
from ...core.render_frame import (
    CUSTOM_SIZE,
    OUTPUT_SIZES,
    SIZE_MAX,
    SIZE_MIN,
    memory_estimate,
    output_size,
)
from ...core.settings import ShadingMode
from ..widgets import ColorButton, SliderSpin, collapsible_group, form_group
from .base import Panel

#: The settings a preset sets; editing one of them leaves the preset behind.
_PRESET_OWNED = ("sampling", "paths")


def _format_bytes(count: int) -> str:
    if count >= 2 ** 30:
        return f"{count / 2 ** 30:.1f} GB"
    return f"{count / 2 ** 20:.0f} MB"


class RenderPanel(Panel):
    """Sets up and starts path-traced renders."""

    render_requested = Signal()
    preview_toggled = Signal(bool)
    window_requested = Signal()

    def _build(self) -> None:
        self._rows: dict[str, tuple] = {}
        self._build_render()
        self._build_output()
        self._build_safe_frame()
        self._build_sampling()
        self._build_paths()
        self._build_method()
        self._build_lens()
        self._build_film()
        self._build_denoise()
        self._build_preview()
        self._build_materials()
        self._add_stretch()
        self._connect()
        self._probe_timer = QTimer(self)
        self._probe_timer.setInterval(250)
        self._probe_timer.timeout.connect(self._refresh_denoisers)
        self._denoisers_known = False

    # -- construction ----------------------------------------------------------

    def _slider(self, key: str, decimals: int = 2, step: float | None = None, suffix: str = "",
                tip: str = "") -> SliderSpin:
        low, high = PATH_TRACE_RANGES[key]
        slider = SliderSpin(low, high, low, decimals=decimals, step=step, suffix=suffix)
        if tip:
            slider.setToolTip(tip)
        owner, _, field = key.rpartition(".")
        self._rows[key] = (slider, owner, field, decimals == 0)
        return slider

    def _build_render(self) -> None:
        box, form = form_group("Render")
        self._render_button = QPushButton("Render Image")
        self._render_button.setToolTip(
            "Path-trace the view into the Render window (F12).\n"
            "What is inside the safe frame is what renders.")
        self._render_button.setMinimumHeight(34)
        font = self._render_button.font()
        font.setBold(True)
        self._render_button.setFont(font)
        self._preview = QCheckBox("Rendered viewport")
        self._preview.setToolTip(
            "Path-trace the viewport itself as you work (Shift+F12): it refines\n"
            "while the view is still and starts over when anything changes.")
        self._window_button = QPushButton("Show Render Window")
        self._window_button.setToolTip("Bring back the last render (Ctrl+F12)")
        self._engine = QLabel("")
        self._engine.setToolTip("What the path tracer is doing, or why it cannot run")
        self._mode_note = QLabel("")
        self._mode_note.setToolTip(
            "A render uses the Shading panel's mode, colours and lights as they are.")
        form.addRow(self._render_button)
        form.addRow("", self._preview)
        form.addRow(self._window_button)
        form.addRow(self._engine)
        form.addRow(self._mode_note)
        self._add(box)

    def _build_output(self) -> None:
        box, form = form_group("Output")
        self._size = QComboBox()
        for label, width, height in OUTPUT_SIZES:
            self._size.addItem(label if width is None else f"{label}  ({width} x {height})",
                               label)
        self._size.addItem(CUSTOM_SIZE, CUSTOM_SIZE)
        self._size.setToolTip("Common picture sizes; type a size below for any other")
        self._width = QSpinBox()
        self._height = QSpinBox()
        for spin, tip in ((self._width, "Width in pixels"), (self._height, "Height in pixels")):
            spin.setRange(SIZE_MIN, SIZE_MAX)
            spin.setSuffix(" px")
            spin.setToolTip(tip)
        self._lock = QCheckBox("Keep proportions")
        self._lock.setToolTip("Change the height with the width, and the width with the height")
        self._scale = self._slider("output.scale", 0, 5.0, " %",
                                   "Render smaller for a quick look, or larger, without\n"
                                   "changing the size set above")
        self._format = QComboBox()
        for fmt in OutputFormat:
            self._format.addItem(fmt.label, fmt.value)
        self._format.setToolTip(
            "PNG keeps the developed picture; OpenEXR keeps the light itself,\n"
            "linear and unclipped, for grading or compositing later")
        self._transparent = QCheckBox("Transparent background")
        self._transparent.setToolTip(
            "Leave the background out (alpha), for putting the model over\n"
            "something else.  An HDRI shown behind the model is left out too.")
        self._memory = QLabel("")
        self._memory.setToolTip("Roughly how much memory the render will hold while it runs")
        form.addRow("Size", self._size)
        form.addRow("Width", self._width)
        form.addRow("Height", self._height)
        form.addRow("", self._lock)
        form.addRow("Scale", self._scale)
        form.addRow("Format", self._format)
        form.addRow("", self._transparent)
        form.addRow("Memory", self._memory)
        self._add(box)

    def _build_safe_frame(self) -> None:
        box, form = form_group("Safe Frame")
        self._safe_show = QCheckBox("Show in the viewport")
        self._safe_show.setToolTip(
            "Shade what lies outside the render's frame, so you can compose\n"
            "the shot as it will be rendered")
        self._safe_dim = self._slider("safe_frame.dim", 2, 0.05, "",
                                      "How dark the view outside the frame is shaded")
        self._safe_action = QCheckBox("Action safe")
        self._safe_action.setToolTip(
            "A guide just inside the frame: keep what matters within it")
        self._safe_title = QCheckBox("Title safe")
        self._safe_title.setToolTip("A tighter guide, for text and anything that must not be cut")
        self._safe_label = QCheckBox("Size label")
        self._safe_label.setToolTip("Write the output size in the frame's corner")
        form.addRow("", self._safe_show)
        form.addRow("Shade", self._safe_dim)
        form.addRow("", self._safe_action)
        form.addRow("", self._safe_title)
        form.addRow("", self._safe_label)
        self._add(box)

    def _build_sampling(self) -> None:
        box, form = form_group("Sampling")
        self._preset = QComboBox()
        self._preset.addItem(CUSTOM_PRESET)
        self._preset.addItems(list(PATH_TRACE_PRESETS))
        self._preset.setToolTip(
            "Preview: seconds, grainy but denoised.  Draft: a clean look at the light.\n"
            "Final: a finished picture.  Production: as clean as it gets, and slow.\n"
            "A preset sets the samples and bounces; the size and look are yours.")
        self._samples = self._slider("sampling.samples", 0, 16.0, "",
                                     "Light paths averaged per pixel: more is cleaner and slower")
        self._noise = self._slider("sampling.noise_threshold", 3, 0.001, "",
                                   "Stop sampling a pixel once its noise is below this.  Smaller\n"
                                   "is cleaner and slower; nought samples every pixel fully.")
        self._min_samples = self._slider("sampling.min_samples", 0, 4.0, "",
                                         "Every pixel takes at least this many, however quiet")
        self._time_limit = self._slider("sampling.time_limit_s", 0, 10.0, " s",
                                        "Stop after this long, however far it got; nought for no\n"
                                        "limit.  Good for 'give me the best in five minutes'.")
        self._seed = self._slider("sampling.seed", 0, 1.0, "",
                                  "A different pattern of noise, no more and no less of it")
        form.addRow("Preset", self._preset)
        form.addRow("Samples", self._samples)
        form.addRow("Noise threshold", self._noise)
        form.addRow("Min samples", self._min_samples)
        form.addRow("Time limit", self._time_limit)
        form.addRow("Seed", self._seed)
        self._add(box)

    def _build_paths(self) -> None:
        box, form = collapsible_group("Light Paths")
        box.setToolTip("How far light is followed from surface to surface")
        form.addRow("Total bounces", self._slider(
            "paths.max_bounces", 0, 1.0, "", "The most surfaces a path meets after the first"))
        form.addRow("Diffuse", self._slider(
            "paths.diffuse", 0, 1.0, "", "Matte bounces: light carried from one surface to\n"
            "the next, and scattered under the skin"))
        form.addRow("Glossy", self._slider(
            "paths.glossy", 0, 1.0, "", "Shiny bounces: reflections of reflections"))
        form.addRow("Transmission", self._slider(
            "paths.transmission", 0, 1.0, "", "Light passed through the skin to its far side"))
        form.addRow("Clamp direct", self._slider(
            "paths.clamp_direct", 1, 0.5, "", "The brightest a sample of direct light may be;\n"
            "nought for no limit.  Tames fireflies at the cost of some sparkle."))
        form.addRow("Clamp indirect", self._slider(
            "paths.clamp_indirect", 1, 0.5, "", "The brightest a sample of bounced light may be;\n"
            "nought for no limit.  The usual cure for fireflies."))
        form.addRow("Filter glossy", self._slider(
            "paths.filter_glossy", 2, 0.05, "", "Blur sharp reflections seen only in bounced\n"
            "light, which is where fireflies come from"))
        self._caustics = QCheckBox("Caustics")
        self._caustics.setToolTip(
            "Let bounced light focus through shiny reflections.  Real, but slow\n"
            "to clear; off is what most renderers default to.")
        form.addRow("", self._caustics)
        self._paths_box = box
        self._add(box)

    def _build_method(self) -> None:
        box, form = form_group("Method")
        self._method = QComboBox()
        for method in RenderMethod:
            self._method.addItem(method.label, method.value)
            self._method.setItemData(self._method.count() - 1, method.note,
                                     role=3)  # Qt.ToolTipRole
        self._method.setToolTip(
            "Progressive: the whole picture at once, clearing pass by pass.\n"
            "Bucket: square by square, each finished before the next.")
        self._bucket_size = self._slider("performance.bucket_size", 0, 8.0, " px",
                                         "A bucket's side.  Smaller shows progress sooner;\n"
                                         "32 or 64 is usually quickest.")
        self._bucket_order = QComboBox()
        for order in BucketOrder:
            self._bucket_order.addItem(order.label, order.value)
        self._bucket_order.setToolTip("Which bucket is rendered next")
        self._threads = self._slider("performance.threads", 0, 1.0, "",
                                     "How many threads render; nought uses all the processor's\n"
                                     "cores but one, which leaves the window responsive")
        self._low_priority = QCheckBox("Low priority")
        self._low_priority.setToolTip(
            "Render below normal priority, so the rest of the computer stays quick")
        form.addRow("Method", self._method)
        self._method_form = form
        form.addRow("Bucket size", self._bucket_size)
        form.addRow("Bucket order", self._bucket_order)
        form.addRow("Threads", self._threads)
        form.addRow("", self._low_priority)
        self._add(box)

    def _build_lens(self) -> None:
        box, form = collapsible_group("Camera Lens")
        box.setToolTip("Depth of field: a real lens's shallow focus")
        self._dof = QCheckBox("Depth of field")
        self._dof.setToolTip("Blur what is nearer or further than the focus, as a real lens does")
        self._focus_target = QCheckBox("Focus on the orbit target")
        self._focus_target.setToolTip(
            "Keep the point the camera orbits about in focus, wherever it moves")
        self._focus = self._slider("lens.focus_distance", 2, 0.05, " × radius",
                                   "The distance in focus, in the model's radius")
        self._aperture = self._slider("lens.aperture", 3, 0.005, " × radius",
                                      "The lens opening: larger is shallower focus")
        form.addRow("", self._dof)
        form.addRow("", self._focus_target)
        form.addRow("Focus distance", self._focus)
        form.addRow("Aperture", self._aperture)
        self._lens_form = form
        self._add(box)

    def _build_film(self) -> None:
        box, form = collapsible_group("Film and Colour")
        box.setToolTip("How the light is turned into the picture's pixels")
        self._filter = QComboBox()
        for kind in PixelFilter:
            self._filter.addItem(kind.label, kind.value)
        self._filter.setToolTip("How samples in and round a pixel are weighed")
        self._filter_width = self._slider("film.filter_width", 2, 0.1, " px",
                                          "The filter's width: wider is softer")
        self._transform = QComboBox()
        for transform in ViewTransform:
            self._transform.addItem(transform.label, transform.value)
        self._transform.setToolTip(
            "Auto develops Human Skin as the viewport does and everything else\n"
            "with PBR Neutral.  Filmic compresses highlights like film; Standard\n"
            "clips them.  Changes a finished render without rendering again.")
        self._exposure = self._slider("color.exposure", 1, 0.1, " EV",
                                      "Brighter or darker, in stops, on top of Human Skin's own")
        self._gamma = self._slider("color.gamma", 2, 0.05, "",
                                   "The display gamma, after the transform")
        self._contrast = self._slider("color.contrast", 2, 0.05, "",
                                      "Push the tones apart from middle grey, or together")
        form.addRow("Pixel filter", self._filter)
        form.addRow("Filter width", self._filter_width)
        form.addRow("View transform", self._transform)
        form.addRow("Exposure", self._exposure)
        form.addRow("Gamma", self._gamma)
        form.addRow("Contrast", self._contrast)
        self._add(box)

    def _build_denoise(self) -> None:
        box, form = form_group("Denoise")
        self._denoise_final = QCheckBox("Denoise the render")
        self._denoise_final.setToolTip(
            "Clean the finished render with an AI denoiser; the noisy picture is\n"
            "kept too, as the Beauty pass")
        self._denoise_preview = QCheckBox("Denoise the rendered viewport")
        self._denoise_preview.setToolTip("Clean the rendered viewport as it refines")
        self._denoiser = QComboBox()
        for backend in DenoiserBackend:
            self._denoiser.addItem(backend.label, backend.value)
        self._denoiser.setToolTip(
            "Auto picks the best that runs here: Intel Open Image Denoise on a GPU,\n"
            "then NVIDIA OptiX, then Open Image Denoise on the CPU.  The built-in\n"
            "filter works everywhere but is far less clever.")
        self._device = QComboBox()
        for device in DenoiserDevice:
            self._device.addItem(device.label, device.value)
        self._device.setToolTip("Where Open Image Denoise runs")
        self._quality = QComboBox()
        for quality in DenoiserQuality:
            self._quality.addItem(quality.label, quality.value)
        self._quality.setToolTip("Open Image Denoise: High for renders, Fast for the viewport")
        self._use_albedo = QCheckBox("Guide by albedo")
        self._use_albedo.setToolTip(
            "Tell the denoiser the surface colours, so it keeps texture sharp:\n"
            "pores, freckles, the edges of marks")
        self._use_normal = QCheckBox("Guide by normals")
        self._use_normal.setToolTip("Tell the denoiser the surface's turn, so it keeps edges sharp")
        self._prefilter = QCheckBox("Clean the guides first")
        self._prefilter.setToolTip(
            "Treat the albedo and normals as noisy too -- they are, under depth\n"
            "of field or a ghost -- and clean them before they guide")
        self._mix = self._slider("denoise.mix", 2, 0.05, "",
                                 "How much of the denoised picture is kept over the noisy one")
        self._atrous = self._slider("denoise.atrous_passes", 0, 1.0, "",
                                    "The built-in filter's reach: each pass doubles it")
        self._denoise_status = QLabel("")
        self._denoise_status.setToolTip("Which denoisers can run on this machine")
        form.addRow("", self._denoise_final)
        form.addRow("", self._denoise_preview)
        form.addRow("Denoiser", self._denoiser)
        form.addRow("Device", self._device)
        form.addRow("Quality", self._quality)
        form.addRow("", self._use_albedo)
        form.addRow("", self._use_normal)
        form.addRow("", self._prefilter)
        form.addRow("Mix", self._mix)
        form.addRow("Built-in passes", self._atrous)
        form.addRow(self._denoise_status)
        self._denoise_form = form
        self._add(box)

    def _build_preview(self) -> None:
        box, form = collapsible_group("Rendered Viewport")
        box.setToolTip("The rendered viewport's own settings, kept light so it stays quick")
        form.addRow("Resolution", self._slider(
            "preview.resolution", 2, 0.05, " × view",
            "The share of the view's pixels traced once it is still"))
        form.addRow("Samples", self._slider(
            "preview.samples", 0, 16.0, "", "Where the rendered viewport stops refining"))
        form.addRow("Noise threshold", self._slider(
            "preview.noise_threshold", 3, 0.005, "",
            "Stop refining a part of the view once its noise is below this"))
        form.addRow("While moving", self._slider(
            "preview.interactive_resolution", 2, 0.05, " × view",
            "The share traced while the view is being turned: lower is smoother"))
        self._add(box)

    def _build_materials(self) -> None:
        box, form = collapsible_group("Lights and Clay")
        box.setToolTip(
            "The lights and materials come from the Shading panel.  These are what\n"
            "a render needs that the viewport does not.")
        self._light_size = self._slider(
            "light_size_deg", 1, 0.5, " deg",
            "How wide the studio key and fill are in the sky: nought is a point\n"
            "with a sharp shadow, wider is softer.  Human Skin has its own, the\n"
            "Light angular radius in the Shading panel.")
        self._clay_color = ColorButton((0.75, 0.72, 0.69))
        self._clay_color.setToolTip(
            "What a Matcap, Normals or Contour model is made of in a render:\n"
            "a matcap is a picture of light, not a material, so it renders as clay")
        self._clay_roughness = self._slider("clay.roughness", 2, 0.05, "", "The clay's roughness")
        self._clay_specular = self._slider("clay.specular", 2, 0.05, "", "The clay's shine")
        form.addRow("Light softness", self._light_size)
        form.addRow("Clay colour", self._clay_color)
        form.addRow("Clay roughness", self._clay_roughness)
        form.addRow("Clay shine", self._clay_specular)
        self._materials_form = form
        self._add(box)

    # -- wiring ------------------------------------------------------------------

    def _connect(self) -> None:
        self._render_button.clicked.connect(self.render_requested)
        self._window_button.clicked.connect(self.window_requested)
        self._preview.toggled.connect(self._on_preview)
        for slider, owner, field, whole in self._rows.values():
            slider.valueChanged.connect(
                lambda value, owner=owner, field=field, whole=whole: self._set(
                    owner, field, int(round(value)) if whole else float(value)))
        combos = (
            (self._format, "output", "format", OutputFormat),
            (self._method, "performance", "method", RenderMethod),
            (self._bucket_order, "performance", "bucket_order", BucketOrder),
            (self._filter, "film", "filter", PixelFilter),
            (self._transform, "color", "view_transform", ViewTransform),
            (self._denoiser, "denoise", "backend", DenoiserBackend),
            (self._device, "denoise", "device", DenoiserDevice),
            (self._quality, "denoise", "quality", DenoiserQuality),
        )
        for combo, owner, field, kind in combos:
            combo.currentIndexChanged.connect(
                lambda index, combo=combo, owner=owner, field=field, kind=kind: self._set(
                    owner, field, kind(combo.itemData(index))))
        checks = (
            (self._transparent, "output", "transparent"),
            (self._lock, "output", "lock_aspect"),
            (self._safe_show, "safe_frame", "show"),
            (self._safe_action, "safe_frame", "action_safe"),
            (self._safe_title, "safe_frame", "title_safe"),
            (self._safe_label, "safe_frame", "label"),
            (self._caustics, "paths", "caustics"),
            (self._low_priority, "performance", "low_priority"),
            (self._dof, "lens", "depth_of_field"),
            (self._focus_target, "lens", "focus_on_target"),
            (self._denoise_final, "denoise", "final"),
            (self._denoise_preview, "denoise", "preview"),
            (self._use_albedo, "denoise", "use_albedo"),
            (self._use_normal, "denoise", "use_normal"),
            (self._prefilter, "denoise", "prefilter_guides"),
        )
        for box, owner, field in checks:
            box.toggled.connect(
                lambda value, owner=owner, field=field: self._set(owner, field, bool(value)))
        self._clay_color.colorChanged.connect(lambda c: self._set("clay", "color", tuple(c)))
        self._size.activated.connect(self._on_size_preset)
        self._width.valueChanged.connect(lambda v: self._on_dimension("width", v))
        self._height.valueChanged.connect(lambda v: self._on_dimension("height", v))
        self._preset.activated.connect(self._on_preset)
        self.state.render_changed.connect(self.update_enabled)
        self.state.path_trace_changed.connect(self._refresh_derived)

    def _target(self, owner: str):
        trace = self.state.path_trace
        return trace if not owner else getattr(trace, owner)

    def _set(self, owner: str, field: str, value) -> None:
        if self._busy:
            return
        setattr(self._target(owner), field, value)
        if owner in _PRESET_OWNED or (owner == "denoise" and field == "final"):
            self.state.path_trace.preset = CUSTOM_PRESET
            with self._suppressed():
                self._preset.setCurrentIndex(self._preset_index())
        self.state.notify_path_trace()
        self.update_enabled()

    def _on_preview(self, on: bool) -> None:
        if self._busy:
            return
        self.preview_toggled.emit(bool(on))

    def set_preview_checked(self, on: bool) -> None:
        with self._suppressed():
            self._preview.setChecked(on)

    def _on_preset(self, index: int) -> None:
        if self._busy:
            return
        name = self._preset.itemText(index)
        preset = PATH_TRACE_PRESETS.get(name)
        if preset is None:
            return
        self.state.path_trace = preset.applied_to(self.state.path_trace, name)
        self.state.notify_path_trace()
        self.refresh()

    def _preset_index(self) -> int:
        trace = self.state.path_trace
        name = trace.preset
        preset = PATH_TRACE_PRESETS.get(name)
        if preset is None or not preset.matches(trace):
            return 0
        return self._preset.findText(name)

    def _viewport_size(self) -> tuple[int, int]:
        window = self.window()
        central = window.centralWidget() if hasattr(window, "centralWidget") else None
        if central is not None:
            ratio = central.devicePixelRatioF()
            return int(central.width() * ratio), int(central.height() * ratio)
        return 1280, 720

    def _on_size_preset(self, index: int) -> None:
        if self._busy:
            return
        name = self._size.itemData(index)
        output = self.state.path_trace.output
        output.size_preset = name
        if name != CUSTOM_SIZE:
            output.width, output.height = output_size(
                type(output)(size_preset=name, scale=100), self._viewport_size())
        self.state.notify_path_trace()
        self.refresh()

    def _on_dimension(self, field: str, value: int) -> None:
        if self._busy:
            return
        output = self.state.path_trace.output
        old_w, old_h = output.width, output.height
        setattr(output, field, int(value))
        if output.lock_aspect and old_w > 0 and old_h > 0:
            if field == "width":
                output.height = int(min(max(round(value * old_h / old_w), SIZE_MIN), SIZE_MAX))
            else:
                output.width = int(min(max(round(value * old_w / old_h), SIZE_MIN), SIZE_MAX))
        output.size_preset = CUSTOM_SIZE
        self.state.notify_path_trace()
        self.refresh()

    # -- state into widgets --------------------------------------------------------

    def refresh(self) -> None:
        trace = self.state.path_trace
        with self._suppressed():
            for slider, owner, field, _whole in self._rows.values():
                slider.set_value(float(getattr(self._target(owner), field)))
            for combo, value in (
                (self._format, trace.output.format.value),
                (self._method, trace.performance.method.value),
                (self._bucket_order, trace.performance.bucket_order.value),
                (self._filter, trace.film.filter.value),
                (self._transform, trace.color.view_transform.value),
                (self._denoiser, trace.denoise.backend.value),
                (self._device, trace.denoise.device.value),
                (self._quality, trace.denoise.quality.value),
            ):
                combo.setCurrentIndex(max(combo.findData(value), 0))
            for box, value in (
                (self._transparent, trace.output.transparent),
                (self._lock, trace.output.lock_aspect),
                (self._safe_show, trace.safe_frame.show),
                (self._safe_action, trace.safe_frame.action_safe),
                (self._safe_title, trace.safe_frame.title_safe),
                (self._safe_label, trace.safe_frame.label),
                (self._caustics, trace.paths.caustics),
                (self._low_priority, trace.performance.low_priority),
                (self._dof, trace.lens.depth_of_field),
                (self._focus_target, trace.lens.focus_on_target),
                (self._denoise_final, trace.denoise.final),
                (self._denoise_preview, trace.denoise.preview),
                (self._use_albedo, trace.denoise.use_albedo),
                (self._use_normal, trace.denoise.use_normal),
                (self._prefilter, trace.denoise.prefilter_guides),
            ):
                box.setChecked(bool(value))
            self._clay_color.set_color(trace.clay.color)
            self._size.setCurrentIndex(max(self._size.findData(trace.output.size_preset), 0)
                                       if self._size.findData(trace.output.size_preset) >= 0
                                       else self._size.count() - 1)
            self._width.setValue(int(trace.output.width))
            self._height.setValue(int(trace.output.height))
            self._preset.setCurrentIndex(self._preset_index())
        self._refresh_derived()
        self.update_enabled()

    def _refresh_derived(self) -> None:
        """What follows from the settings: the size in pixels, the memory, the notes."""
        trace = self.state.path_trace
        width, height = output_size(trace.output, self._viewport_size())
        if trace.output.size_preset != CUSTOM_SIZE:
            with self._suppressed():
                self._width.setValue(int(round(width * 100 / max(trace.output.scale, 1))))
                self._height.setValue(int(round(height * 100 / max(trace.output.scale, 1))))
        self._memory.setText(f"{width} x {height} px, about "
                             f"{_format_bytes(memory_estimate(width, height))}")

    def update_enabled(self) -> None:
        trace = self.state.path_trace
        mode = self.state.render.shading_mode
        skin = mode is ShadingMode.HUMAN_SKIN
        clay = mode in (ShadingMode.MATCAP, ShadingMode.NORMALS, ShadingMode.CONTOUR)
        self._mode_note.setText(mode_note(self.state.render))
        bucket = trace.performance.method is RenderMethod.BUCKET
        self._method_form.setRowVisible(self._bucket_size, bucket)
        self._method_form.setRowVisible(self._bucket_order, bucket)
        dof = trace.lens.depth_of_field
        self._focus_target.setEnabled(dof)
        self._focus.setEnabled(dof and not trace.lens.focus_on_target)
        self._aperture.setEnabled(dof)
        self._materials_form.setRowVisible(self._light_size, not skin)
        for widget in (self._clay_color, self._clay_roughness, self._clay_specular):
            self._materials_form.setRowVisible(widget, clay)
        backend = trace.denoise.backend
        oidn = backend in (DenoiserBackend.AUTO, DenoiserBackend.OIDN)
        self._denoise_form.setRowVisible(self._device, backend is DenoiserBackend.OIDN)
        self._denoise_form.setRowVisible(self._quality, oidn)
        self._denoise_form.setRowVisible(self._prefilter, oidn)
        self._denoise_form.setRowVisible(self._atrous, backend is DenoiserBackend.BUILTIN)

    # -- the engine and the denoisers --------------------------------------------

    def set_engine_status(self, text: str) -> None:
        self._engine.setText(text)

    def showEvent(self, event) -> None:  # noqa: N802 - Qt naming
        super().showEvent(event)
        if not self._denoisers_known:
            self._probe_timer.start()

    def _refresh_denoisers(self) -> None:
        from ..render_controller import denoise_service

        infos = denoise_service().infos()
        if infos is None:
            self._denoise_status.setText("Looking for denoisers...")
            return
        self._probe_timer.stop()
        self._denoisers_known = True
        model = self._denoiser.model()
        lines = []
        for info in infos:
            index = self._denoiser.findData(info.backend.value)
            item = model.item(index)
            if item is not None:
                item.setEnabled(info.available)
                item.setToolTip(info.summary)
            lines.append(("✓ " if info.available else "✗ ") + info.summary)
        self._denoise_status.setText("\n".join(lines))
