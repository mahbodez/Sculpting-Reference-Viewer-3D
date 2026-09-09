"""Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting."""

import sys
import tomllib
from pathlib import Path

#: Shown in the window title, the splash screen and the platform task switcher.
APP_NAME = "Reference Viewer 3D"

#: Used when ``pyproject.toml`` is not shipped next to us; keep in step with it.
_FALLBACK_VERSION = "1.6.0"


def _read_version() -> str:
    """Read the version from ``pyproject.toml``, bundled or in the source checkout."""
    roots = [Path(__file__).parents[2]]
    if getattr(sys, "frozen", False):
        roots.insert(0, Path(getattr(sys, "_MEIPASS", roots[0])))
    for root in roots:
        project_file = root / "pyproject.toml"
        if project_file.is_file():
            with project_file.open("rb") as handle:
                return tomllib.load(handle)["project"]["version"]
    return _FALLBACK_VERSION


__version__ = _read_version()
__all__ = ["APP_NAME", "__version__"]
