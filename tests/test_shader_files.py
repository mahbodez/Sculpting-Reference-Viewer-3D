"""The GLSL on disk: its includes and constants, and that every program is whole."""

from __future__ import annotations

import re

import pytest

from refview.render import shader_files, shaders
from refview.render.shader_files import GLSL_DIRECTORY, load_glsl


def test_every_program_is_expanded_completely():
    for name in dir(shaders):
        source = getattr(shaders, name)
        if not isinstance(source, str) or "#version" not in source:
            continue
        assert source.startswith("#version 330 core"), name
        assert "#include" not in source, name
        assert not re.search(r"@[A-Z_]+@", source), name
    # One file, two programs: the tracer is a constant in each.
    assert "#define uSkinTrace false" in shaders.MESH_FRAGMENT
    assert "#define uSkinTrace true" in shaders.MESH_TRACE_FRAGMENT
    assert "uniform bool uSkinTrace" not in shaders.MESH_FRAGMENT


def test_every_file_is_used():
    used = set()
    for path in GLSL_DIRECTORY.iterdir():
        used.update(re.findall(r'#include "([^"]+)"', path.read_text(encoding="utf-8")))
    loaded = {"fullscreen.vert", "background.frag", "mesh.vert", "mesh.frag", "flat.vert",
              "flat.frag", "depth.vert", "depth.frag", "stroke.vert", "stroke.frag",
              "occlusion.frag", "resolve.frag", "blur.frag", "outline.frag", "ghost.frag",
              "skin.glsl", "skin_accumulate.frag", "skin_present.frag", "environment.glsl"}
    on_disk = {path.name for path in GLSL_DIRECTORY.iterdir()}
    assert on_disk == loaded | used


def test_includes_constants_and_defines(tmp_path, monkeypatch):
    (tmp_path / "top.frag").write_text(
        '#version 330 core\n#include "part.glsl"\nconst int N = @COUNT@;\n', encoding="utf-8"
    )
    (tmp_path / "part.glsl").write_text("float part() { return 1.0; }\n", encoding="utf-8")
    (tmp_path / "loop.glsl").write_text('#include "loop.glsl"\n', encoding="utf-8")
    monkeypatch.setattr(shader_files, "GLSL_DIRECTORY", tmp_path)
    shader_files._read.cache_clear()
    try:
        text = load_glsl("top.frag", {"COUNT": 7}, {"FLAG": "true"})
        assert text.splitlines()[:3] == [
            "#version 330 core", "#define FLAG true", "float part() { return 1.0; }"
        ]
        assert "const int N = 7;" in text
        with pytest.raises(KeyError, match="COUNT"):
            load_glsl("top.frag")
        with pytest.raises(ValueError, match="cycle"):
            load_glsl("loop.glsl")
    finally:
        shader_files._read.cache_clear()
