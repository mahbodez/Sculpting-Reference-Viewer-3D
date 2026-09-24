"""The path tracer's settings: their ranges, presets, and life in a session."""

from __future__ import annotations

import json
import math

from refview.core.path_trace import (
    CUSTOM_PRESET,
    PATH_TRACE_PRESETS,
    PATH_TRACE_RANGES,
    DenoiserBackend,
    OutputFormat,
    PathTraceSettings,
    RenderMethod,
    ViewTransform,
)
from refview.core.session import Session


def test_defaults_are_the_final_preset_and_already_in_bounds():
    settings = PathTraceSettings()
    assert settings.preset == "Final"
    assert PATH_TRACE_PRESETS["Final"].matches(settings)
    assert settings.bounded() == settings


def test_bounded_repairs_what_a_hand_edited_file_can_hold():
    settings = PathTraceSettings()
    settings.sampling.samples = math.nan
    settings.sampling.noise_threshold = -3.0
    settings.output.width = 1e9
    settings.paths.max_bounces = 3
    settings.paths.diffuse = 40
    settings.sampling.min_samples = 5000
    settings.clay.color = (2.0, -1.0, 0.5)
    settings.light_size_deg = math.inf
    bounded = settings.bounded()
    assert bounded.sampling.samples == PathTraceSettings().sampling.samples
    assert isinstance(bounded.sampling.samples, int)
    assert bounded.sampling.noise_threshold == 0.0
    assert bounded.output.width == PATH_TRACE_RANGES["output.width"][1]
    # A bounce kind can never go further than the path as a whole.
    assert bounded.paths.diffuse == 3
    assert bounded.sampling.min_samples <= bounded.sampling.samples
    assert bounded.clay.color == (1.0, 0.0, 0.5)
    assert bounded.light_size_deg == PathTraceSettings().light_size_deg
    # The original is left as it was.
    assert settings.paths.diffuse == 40


def test_every_range_names_a_real_setting():
    settings = PathTraceSettings()
    for name in PATH_TRACE_RANGES:
        owner = settings
        *path, attribute = name.split(".")
        for part in path:
            owner = getattr(owner, part)
        assert hasattr(owner, attribute), name


def test_presets_set_the_work_and_never_the_size_or_the_look():
    settings = PathTraceSettings()
    settings.output.width, settings.output.height = 800, 600
    settings.color.exposure = 1.5
    settings.color.view_transform = ViewTransform.FILMIC
    settings.sampling.seed = 42
    for name, preset in PATH_TRACE_PRESETS.items():
        applied = preset.applied_to(settings, name)
        assert applied.preset == name
        assert preset.matches(applied)
        assert (applied.output.width, applied.output.height) == (800, 600)
        assert applied.color == settings.color
        # The noise pattern chosen is kept too.
        assert applied.sampling.seed == 42
        assert applied.bounded() == applied, name
    # Presets climb in effort.
    samples = [p.sampling.samples for p in PATH_TRACE_PRESETS.values()]
    assert samples == sorted(samples)


def test_an_edit_leaves_the_preset_unmatched():
    settings = PATH_TRACE_PRESETS["Draft"].applied_to(PathTraceSettings(), "Draft")
    settings.sampling.samples += 1
    assert not PATH_TRACE_PRESETS["Draft"].matches(settings)
    assert CUSTOM_PRESET not in PATH_TRACE_PRESETS


def test_auto_view_transform_follows_the_shading_mode():
    assert ViewTransform.AUTO.resolved(skin=True) is ViewTransform.REINHARD
    assert ViewTransform.AUTO.resolved(skin=False) is ViewTransform.NEUTRAL
    assert ViewTransform.FILMIC.resolved(skin=True) is ViewTransform.FILMIC


def test_a_session_from_before_the_path_tracer_loads_the_defaults(tmp_path):
    path = tmp_path / "v11.refview.json"
    path.write_text(json.dumps({"version": 11, "render": {"shading_mode": "pbr"}}),
                    encoding="utf-8")
    session = Session.load(path)
    assert session.path_trace == PathTraceSettings()


def test_path_trace_settings_survive_a_session_round_trip(tmp_path):
    session = Session()
    assert session.version == 12
    trace = session.path_trace
    trace.output.width, trace.output.height = 1234, 567
    trace.output.format = OutputFormat.EXR_HALF
    trace.performance.method = RenderMethod.BUCKET
    trace.denoise.backend = DenoiserBackend.OPTIX
    trace.color.view_transform = ViewTransform.FILMIC
    trace.clay.color = (0.1, 0.2, 0.3)
    trace.safe_frame.show = True
    trace.preset = CUSTOM_PRESET
    loaded = Session.load(session.save(tmp_path / "s.refview.json"))
    assert loaded.path_trace == trace
    assert loaded.path_trace.performance.method is RenderMethod.BUCKET


def test_a_malformed_path_trace_block_falls_back_field_by_field(tmp_path):
    path = tmp_path / "odd.refview.json"
    path.write_text(json.dumps({"version": 12, "path_trace": {
        "sampling": {"samples": "lots", "seed": 7},
        "performance": {"method": "teleport"},
        "unknown": 1,
    }}), encoding="utf-8")
    trace = Session.load(path).path_trace
    assert trace.sampling.samples == PathTraceSettings().sampling.samples
    assert trace.sampling.seed == 7
    assert trace.performance.method is RenderMethod.PROGRESSIVE
