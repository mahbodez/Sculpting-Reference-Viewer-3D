"""Locations of the bundled resources.

``REFVIEW_RESOURCES`` overrides the search, which is handy when the package is
installed somewhere other than the source checkout.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent

#: Repository root when running from a source checkout (``src/refview``).
PROJECT_ROOT = PACKAGE_ROOT.parents[1]


def _bundled_root() -> Path | None:
    """Return PyInstaller's extracted application directory when frozen."""
    if not getattr(sys, "frozen", False):
        return None
    return Path(getattr(sys, "_MEIPASS", PACKAGE_ROOT))


IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp")


def resources_dir() -> Path:
    override = os.environ.get("REFVIEW_RESOURCES")
    if override:
        return Path(override).expanduser()
    bundled_root = _bundled_root()
    if bundled_root is not None:
        return bundled_root / "resources"
    return PROJECT_ROOT / "resources"


#: A folder of the artist's own to read matcaps from, in place of the bundled
#: one.  Set from the preferences; ``None`` means the ones that ship.  A
#: module-level override rather than an argument threaded through every caller
#: because "where the matcaps are" is one answer for the whole run, and the
#: three places that ask are not the places that know.
_matcap_override: Path | None = None


def set_matcap_dir(folder: str | Path | None) -> None:
    """Read matcaps from ``folder`` instead of the bundled ones.

    A folder that has gone -- an external drive that is not plugged in, a
    path copied from another machine -- is not an error and not a reason to
    show an empty gallery: :func:`available_matcaps` falls back to the ones
    that ship, so the application is never without a matcap to draw with.
    """
    global _matcap_override
    if folder is None or not str(folder).strip():
        _matcap_override = None
        return
    _matcap_override = Path(folder).expanduser()


def matcap_dir() -> Path:
    """Where matcaps are read from: the artist's folder, or the bundled one."""
    if _matcap_override is not None and _matcap_override.is_dir():
        return _matcap_override
    return resources_dir() / "matcaps"


def model_dir() -> Path:
    return resources_dir() / "models"


#: What an HDRI can be read from.  Mirrors
#: :data:`refview.core.environment.ENVIRONMENT_SUFFIXES`, which this module
#: does not import so that it stays free of numpy.
ENVIRONMENT_SUFFIXES = (".hdr", ".exr")


def environment_dir() -> Path:
    """Where the bundled HDRIs are."""
    return resources_dir() / "hdris"


def available_environments() -> list[Path]:
    """Every HDRI in the bundled folder, sorted by name."""
    directory = environment_dir()
    if not directory.is_dir():
        return []
    return sorted(
        path for path in directory.iterdir() if path.suffix.lower() in ENVIRONMENT_SUFFIXES
    )


def image_path(name: str) -> Path:
    return resources_dir() / "images" / name


def available_matcaps() -> list[Path]:
    """Every image in the matcap folder, sorted by name."""
    directory = matcap_dir()
    if not directory.is_dir():
        return []
    return sorted(
        path for path in directory.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES
    )
