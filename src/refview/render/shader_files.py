"""Reading the GLSL out of :file:`render/glsl`.

Each program's source lives in a file of its own -- ``.vert`` and ``.frag``
for the stages, ``.glsl`` for the pieces several of them share -- so that it
reads, diffs and highlights as GLSL rather than as a Python string.  GLSL 3.30
has no way of pulling one file into another, so two small conveniences are
worked here before the driver sees anything:

- A line ``#include "name.glsl"`` is replaced by that file, itself expanded
  the same way.  It is how the cross-section test, the HDRI's lookups and the
  skin reach the programs that use them.
- ``@NAME@`` is replaced by a constant from Python -- an array size or a table
  range that the code on the CPU side sets and the shader must agree with.

``defines`` go in straight after the ``#version`` line, which is how one file
is compiled twice with a different constant in each.
"""

from __future__ import annotations

import re
from functools import cache
from pathlib import Path

GLSL_DIRECTORY = Path(__file__).resolve().parent / "glsl"

_INCLUDE = re.compile(r'^[ \t]*#include[ \t]+"([^"]+)"[ \t]*$', re.MULTILINE)
_CONSTANT = re.compile(r"@([A-Z_][A-Z0-9_]*)@")


@cache
def _read(name: str) -> str:
    return (GLSL_DIRECTORY / name).read_text(encoding="utf-8")


def _expand(name: str, seen: tuple[str, ...]) -> str:
    if name in seen:
        raise ValueError(f"GLSL include cycle: {' -> '.join((*seen, name))}")
    return _INCLUDE.sub(lambda match: _expand(match.group(1), (*seen, name)), _read(name))


def load_glsl(
    name: str,
    constants: dict[str, object] | None = None,
    defines: dict[str, object] | None = None,
) -> str:
    """The source of ``name`` with its includes, constants and defines worked in."""
    text = _expand(name, ())
    values = constants or {}

    def constant(match: re.Match) -> str:
        key = match.group(1)
        if key not in values:
            raise KeyError(f"{name} needs a value for @{key}@")
        return str(values[key])

    text = _CONSTANT.sub(constant, text)
    if defines:
        lines = "".join(f"#define {key} {value}\n" for key, value in defines.items())
        head, newline, rest = text.partition("\n")
        text = head + newline + lines + rest
    return text
