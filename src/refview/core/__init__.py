"""Qt-free geometry, camera and document model for the reference viewer."""

from .armature import (
    Armature,
    ArmatureNode,
    ArmatureSettings,
    ArmatureStore,
    Bone,
    BoneLabels,
    Buried,
    PlacedLandmark,
)
from .bookmark import BookmarkStore, CameraBookmark
from .camera import Camera, Projection
from .landmarks import (
    HUMANOID,
    HUMANOID_LANDMARKS,
    PRESETS,
    Landmark,
    Preset,
    Side,
    build_humanoid,
    median_plane,
    mirror_landmarks,
    mirror_point,
    rebuild,
)
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
    "HUMANOID",
    "HUMANOID_LANDMARKS",
    "MESH_FILTER",
    "MESH_SUFFIXES",
    "PRESETS",
    "SESSION_SUFFIX",
    "SPIN_STEPS",
    "UNIT_NAMES",
    "Armature",
    "ArmatureNode",
    "ArmatureSettings",
    "ArmatureStore",
    "Bone",
    "BoneLabels",
    "BookmarkStore",
    "Bounds",
    "Buried",
    "Camera",
    "CameraBookmark",
    "Hit",
    "Landmark",
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
    "PlacedLandmark",
    "Preset",
    "Projection",
    "QualitySettings",
    "RenderSettings",
    "SectionAxis",
    "SectionMode",
    "SectionSettings",
    "Session",
    "ShadingMode",
    "Side",
    "StlLoadError",
    "SurfaceSettings",
    "UpAxis",
    "build_humanoid",
    "build_pedestal",
    "compute_vertex_normals",
    "load_mesh",
    "load_obj",
    "load_stl",
    "median_plane",
    "mirror_landmarks",
    "mirror_point",
    "raycast_mesh",
    "rebuild",
    "section_segments",
    "sidecar_path",
    "snap_to_vertex",
]
