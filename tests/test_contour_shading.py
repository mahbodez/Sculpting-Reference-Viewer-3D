"""The contour shading mode: slices across the form, read off it like a map."""

from __future__ import annotations

import numpy as np
import pytest

from refview.core.session import Session
from refview.core.settings import (
    CONTOUR_DENSITY_MIN,
    ContourDirection,
    ContourShadingSettings,
    RenderSettings,
    ShadingMode,
)
from refview.render import shaders


def test_the_mode_has_a_shader_branch_in_step_with_its_id():
    assert ShadingMode.CONTOUR.uses_contour
    assert not ShadingMode.CONTOUR.uses_lighting
    assert not ShadingMode.CONTOUR.uses_matcap
    branch = f"const int MODE_CONTOUR      = {ShadingMode.CONTOUR.shader_id};"
    assert branch in shaders.MESH_FRAGMENT
    for uniform in ("uSliceDirection", "uSliceSpacing", "uSliceWidth", "uSliceColor",
                    "uSlicePaper", "uSliceLit"):
        assert uniform in shaders.MESH_FRAGMENT
    assert "uMode == MODE_CONTOUR" in shaders.MESH_FRAGMENT


@pytest.mark.parametrize(
    ("direction", "forward", "expected"),
    [
        (ContourDirection.VIEW, (0.0, 0.0, -1.0), (0.0, 0.0, -1.0)),
        (ContourDirection.VIEW, (0.0, 3.0, 0.0), (0.0, 1.0, 0.0)),
        (ContourDirection.X, (0.0, 0.0, -1.0), (1.0, 0.0, 0.0)),
        (ContourDirection.Y, (0.0, 0.0, -1.0), (0.0, 1.0, 0.0)),
        (ContourDirection.Z, (0.0, 0.0, -1.0), (0.0, 0.0, 1.0)),
    ],
)
def test_the_slices_face_the_way_that_was_asked(direction, forward, expected):
    settings = ContourShadingSettings(direction=direction)
    assert np.allclose(settings.normal(forward), expected)


def test_a_custom_direction_is_normalised_and_an_empty_one_falls_back():
    settings = ContourShadingSettings(direction=ContourDirection.CUSTOM, custom_direction=(0, 0, 2))
    assert np.allclose(settings.normal((1.0, 0.0, 0.0)), (0.0, 0.0, 1.0))
    settings.custom_direction = (0.0, 0.0, 0.0)
    assert np.allclose(settings.normal((1.0, 0.0, 0.0)), (0.0, 1.0, 0.0))


def test_the_settings_survive_a_session_and_an_older_file_has_them_by_default():
    session = Session()
    session.render.shading_mode = ShadingMode.CONTOUR
    session.render.contour.direction = ContourDirection.Z
    session.render.contour.density = 50.0
    session.render.contour.line_color = (0.5, 0.1, 0.1)
    data = session.to_dict()
    back = Session.from_dict(data)
    assert back.render.shading_mode is ShadingMode.CONTOUR
    assert back.render.contour.direction is ContourDirection.Z
    assert back.render.contour.density == 50.0
    assert tuple(back.render.contour.line_color) == (0.5, 0.1, 0.1)
    data["render"].pop("contour")
    assert Session.from_dict(data).render.contour == ContourShadingSettings()


def test_the_density_floor_keeps_the_spacing_finite():
    assert RenderSettings().contour.density >= CONTOUR_DENSITY_MIN
    assert CONTOUR_DENSITY_MIN > 0
