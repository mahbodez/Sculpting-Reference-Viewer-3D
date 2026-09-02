"""Locations of the bundled resources.

``REFVIEW_RESOURCES`` overrides the search, which is handy when the package is
installed somewhere other than the source checkout.
"""

from __future__ import annotations

import os
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent

#: Repository root when running from a source checkout (``src/refview``).
PROJECT_ROOT = PACKAGE_ROOT.parents[1]

IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff", ".webp")


def resources_dir() -> Path:
    override = os.environ.get("REFVIEW_RESOURCES")
    if override:
        return Path(override).expanduser()
    return PROJECT_ROOT / "resources"


def matcap_dir() -> Path:
    return resources_dir() / "matcaps"


def model_dir() -> Path:
    return resources_dir() / "models"


def available_matcaps() -> list[Path]:
    """Every image in the matcap folder, sorted by name."""
    directory = matcap_dir()
    if not directory.is_dir():
        return []
    return sorted(
        path for path in directory.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES
    )
