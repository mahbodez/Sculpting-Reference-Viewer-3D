"""Where an auto-skinned rig is kept between runs: a small file beside the session.

A file's own skin weights stay in the file and are read back from it.  A
skin made here has no file to stay in -- the model's OBJ has no idea of
bones -- and it is too big for the session, which is JSON and meant to be
read: a hundred thousand vertices' worth of joints and weights is megabytes
of numbers nobody wants to scroll past.  So it goes in a numpy archive of
its own, named for the session and the object, and the session's record of
the object says where.  What is written is the rig in the coordinates of the
model's own file, as the rig on the mesh is kept, so that loading it is
handing it to the mesh and nothing more.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .mesh import Mesh
from .skeleton import Rig, Skin

#: What the archive's name ends in, after the session's stem and the object's.
RIG_SUFFIX = ".skin.npz"


class RigFileError(RuntimeError):
    """Raised when a skin archive cannot be read, or does not fit the model."""


def save_rig(rig: Rig, path: str | Path) -> Path:
    """Write ``rig`` -- everything but the vertices, which the model has."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    skin = rig.skin
    np.savez_compressed(
        path,
        names=np.array(rig.names, dtype=str),
        parents=np.asarray(rig.parents, dtype=np.int64),
        rest_local=rig.rest_local,
        joints=skin.joints,
        weights=skin.weights,
        inverse_bind=skin.inverse_bind,
        tag=np.array(rig.tag, dtype=str),
    )
    return path


def load_rig(path: str | Path, mesh: Mesh) -> Rig:
    """Read a rig back and stand it on ``mesh``, whose vertices it was made for."""
    path = Path(path)
    try:
        with np.load(path, allow_pickle=False) as data:
            names = [str(name) for name in data["names"]]
            parents = data["parents"]
            rest_local = data["rest_local"]
            joints = data["joints"]
            weights = data["weights"]
            inverse_bind = data["inverse_bind"]
            tag = str(data["tag"]) if "tag" in data else ""
    except (OSError, KeyError, ValueError) as error:
        raise RigFileError(f"{path.name} could not be read as a skin: {error}") from error
    if len(joints) != mesh.vertex_count:
        raise RigFileError(
            f"{path.name} was made for a model of {len(joints):,} vertices; "
            f"{mesh.name} has {mesh.vertex_count:,}"
        )
    try:
        skin = Skin(joints, weights, inverse_bind, mesh.positions, mesh.normals)
        return Rig(names, parents, rest_local, skin, tag)
    except ValueError as error:
        raise RigFileError(f"{path.name} is not a skin this model can wear: {error}") from error
