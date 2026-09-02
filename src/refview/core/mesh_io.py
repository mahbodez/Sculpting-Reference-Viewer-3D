"""One entry point for every mesh format the viewer reads.

Callers ask for a path and get a :class:`~refview.core.mesh.Mesh` back; the
suffix decides which reader runs.  Adding a format means writing a loader and
adding a line to :data:`LOADERS`.
"""

from __future__ import annotations

from pathlib import Path

from .gltf_loader import load_gltf
from .mesh import Mesh, MeshLoadError
from .obj_loader import load_obj
from .stl_loader import load_stl

#: Suffix -> reader.  Keys are lower case and include the dot.
LOADERS = {
    ".obj": load_obj,
    ".stl": load_stl,
    ".glb": load_gltf,
    ".gltf": load_gltf,
}

#: Suffixes the file dialog and drag-and-drop accept, in menu order.
MESH_SUFFIXES: tuple[str, ...] = tuple(LOADERS)

#: Qt file-dialog filter listing every supported format.
MESH_FILTER = (
    "Meshes (*.obj *.stl *.glb *.gltf);;Wavefront OBJ (*.obj);;"
    "STL (*.stl);;glTF (*.glb *.gltf)"
)


def load_mesh(path: str | Path) -> Mesh:
    """Load any supported mesh file, raising :class:`MeshLoadError` otherwise."""
    path = Path(path)
    loader = LOADERS.get(path.suffix.lower())
    if loader is None:
        supported = ", ".join(sorted(MESH_SUFFIXES))
        raise MeshLoadError(f"{path.name}: unsupported format (expected one of {supported})")
    return loader(path)
