"""Qt-free geometry, camera and document model for the reference viewer."""

from .bookmark import BookmarkStore, CameraBookmark
from .camera import Camera, Projection
from .measurement import (
    UNIT_NAMES,
    Measurement,
    MeasurementSettings,
    MeasurementStore,
)
from .mesh import Bounds, Mesh, MeshLoadError, MeshUnits, compute_vertex_normals
from .mesh_io import MESH_FILTER, MESH_SUFFIXES, load_mesh
from .obj_loader import ObjLoadError, load_obj
from .orientation import SPIN_STEPS, OrientationSettings, UpAxis
from .pedestal import PedestalSettings, build_pedestal
from .raycast import Hit, raycast_mesh, snap_to_vertex
from .section import SectionAxis, SectionMode, SectionSettings, section_segments
from .session import SESSION_SUFFIX, Session, sidecar_path
from .settings import (
    LightSettings,
    MatcapSettings,
    NavigationSettings,
    QualitySettings,
    RenderSettings,
    ShadingMode,
    SurfaceSettings,
)
from .stl_loader import StlLoadError, load_stl

__all__ = [
    "MESH_FILTER",
    "MESH_SUFFIXES",
    "SESSION_SUFFIX",
    "UNIT_NAMES",
    "BookmarkStore",
    "Bounds",
    "Camera",
    "CameraBookmark",
    "Hit",
    "LightSettings",
    "MatcapSettings",
    "Measurement",
    "MeasurementSettings",
    "MeasurementStore",
    "Mesh",
    "MeshLoadError",
    "MeshUnits",
    "NavigationSettings",
    "ObjLoadError",
    "OrientationSettings",
    "PedestalSettings",
    "Projection",
    "QualitySettings",
    "RenderSettings",
    "SectionAxis",
    "SectionMode",
    "SPIN_STEPS",
    "SectionSettings",
    "Session",
    "ShadingMode",
    "StlLoadError",
    "SurfaceSettings",
    "UpAxis",
    "build_pedestal",
    "compute_vertex_normals",
    "load_mesh",
    "load_obj",
    "load_stl",
    "raycast_mesh",
    "section_segments",
    "sidecar_path",
    "snap_to_vertex",
]
