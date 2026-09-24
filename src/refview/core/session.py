"""Persisted viewer state: camera, shading, measurements and bookmarks."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from .annotation import AnnotationSettings, Stroke
from .armature import Armature, ArmatureSettings
from .bookmark import CameraBookmark
from .forms import FormSettings, PrimaryForm
from .measurement import Measurement, MeasurementSettings
from .orientation import OrientationSettings
from .path_trace import PathTraceSettings
from .scene import ObjectRecord, ObjectSettings
from .serialization import decode, encode
from .settings import NavigationSettings, RenderSettings
from .skeleton import Skeleton, SkeletonSettings

#: Suffix used for the sidecar file saved next to a model.
SESSION_SUFFIX = ".refview.json"


@dataclass
class Session:
    """A snapshot of everything worth keeping between runs."""

    #: 1: the original format.  2 added the annotation layer.  3 added the
    #: cross-section, pedestal, high-quality and navigation settings, 4 the
    #: model orientation, 5 the armature and the landmarks behind it, 6 the
    #: primary forms, 7 the arrangement of the panels, 8 the skeletons and
    #: their pose, 9 the objects -- several models in one scene, each with
    #: its place and its parent -- 10 the skins made here, kept in an
    #: archive beside the session that each object's record names, 11
    #: an orientation for each object, where one had served them all, and
    #: 12 the path tracer's settings.
    #: Older files still load: :func:`decode` fills anything missing from
    #: the defaults.
    version: int = 12
    #: The model, for a file written before there were several; kept as the
    #: first object's file so that an older build can still open a newer
    #: session and see something.
    mesh_path: str | None = None
    #: Every object in the scene, parents by index into this same list.
    #: Empty in a session from before version 9, which is read as one object
    #: standing at :attr:`mesh_path`.
    objects: list[ObjectRecord] = field(default_factory=list)
    object_settings: ObjectSettings = field(default_factory=ObjectSettings)
    camera: dict = field(default_factory=dict)
    render: RenderSettings = field(default_factory=RenderSettings)
    #: What a render is made at: its size, sampling and look.  Kept apart
    #: from :attr:`render`, which is what the viewport draws with.
    path_trace: PathTraceSettings = field(default_factory=PathTraceSettings)
    measurement_settings: MeasurementSettings = field(default_factory=MeasurementSettings)
    measurements: list[Measurement] = field(default_factory=list)
    bookmarks: list[CameraBookmark] = field(default_factory=list)
    annotation_settings: AnnotationSettings = field(default_factory=AnnotationSettings)
    annotations: list[Stroke] = field(default_factory=list)
    armature_settings: ArmatureSettings = field(default_factory=ArmatureSettings)
    armatures: list[Armature] = field(default_factory=list)
    form_settings: FormSettings = field(default_factory=FormSettings)
    forms: list[PrimaryForm] = field(default_factory=list)
    skeleton_settings: SkeletonSettings = field(default_factory=SkeletonSettings)
    #: The skeletons and the pose each stands in.  The skin weights of a
    #: rigged model are not here: they are the model's, and are read back
    #: out of the model file and matched to the joints by name.  A skin made
    #: here is in an archive beside the session; see :attr:`ObjectRecord.skin`.
    skeletons: list[Skeleton] = field(default_factory=list)
    navigation: NavigationSettings = field(default_factory=NavigationSettings)
    #: How the next file added is read in, and how every object of a session
    #: from before version 11 was: since then each object's record carries
    #: its own.
    orientation: OrientationSettings = field(default_factory=OrientationSettings)
    #: Where the panels were, and any the artist had built by hand.  Opaque
    #: here on purpose: what is in it is the window's business, and the core
    #: has no opinion about docks.  A session saved without one loads into
    #: whatever arrangement the window is already in, which is right -- an
    #: older file should not be able to say anything about the panels.
    layout: dict = field(default_factory=dict)

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
