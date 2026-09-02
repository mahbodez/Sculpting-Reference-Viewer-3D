"""Persisted viewer state: camera, shading, measurements and bookmarks."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .annotation import AnnotationSettings, Stroke
from .bookmark import CameraBookmark
from .measurement import Measurement, MeasurementSettings
from .serialization import decode, encode
from .settings import RenderSettings

#: Suffix used for the sidecar file saved next to a model.
SESSION_SUFFIX = ".refview.json"


@dataclass
class Session:
    """A snapshot of everything worth keeping between runs."""

    #: 1: the original format.  2 added the annotation layer.  Older files
    #: still load: :func:`decode` fills anything missing from the defaults.
    version: int = 2
    mesh_path: str | None = None
    camera: dict = field(default_factory=dict)
    render: RenderSettings = field(default_factory=RenderSettings)
    measurement_settings: MeasurementSettings = field(default_factory=MeasurementSettings)
    measurements: list[Measurement] = field(default_factory=list)
    bookmarks: list[CameraBookmark] = field(default_factory=list)
    annotation_settings: AnnotationSettings = field(default_factory=AnnotationSettings)
    annotations: list[Stroke] = field(default_factory=list)

    def to_dict(self) -> dict:
        return encode(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        return decode(cls, data)

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        return path

    @classmethod
    def load(cls, path: str | Path) -> "Session":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls.from_dict(data)


def sidecar_path(mesh_path: str | Path) -> Path:
    """Session file that sits beside a model, e.g. ``bust.refview.json``."""
    mesh_path = Path(mesh_path)
    return mesh_path.with_name(mesh_path.stem + SESSION_SUFFIX)
