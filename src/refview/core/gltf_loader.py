"""glTF 2.0 reader for ``.glb`` and ``.gltf`` files.

Only what a reference viewer draws and poses is read: the node hierarchy, so
each mesh lands where the scene puts it, the POSITION/NORMAL attributes of
every triangle primitive, and the first skin -- its joints, their bind
matrices and the JOINTS_0/WEIGHTS_0 that tie the vertices to them, which is
what lets the Pose tool move the figure.  Materials, animation and morph
targets are skipped: the viewer shades with matcaps and its own lights.

glTF is the one common format that states its unit: the specification fixes
scene coordinates as metres, so the loader reports that and the viewer adopts
it for measurement readouts instead of asking the artist to guess a scale.
"""

from __future__ import annotations

import base64
import json
import struct
from pathlib import Path
from urllib.parse import unquote

import numpy as np

from .mesh import Mesh, MeshLoadError, MeshUnits, compute_vertex_normals
from .skeleton import Rig, Skin, rest_skinned_positions

_GLB_MAGIC = b"glTF"
_JSON_CHUNK = 0x4E4F534A
_BIN_CHUNK = 0x004E4942

#: glTF componentType -> numpy dtype.
_COMPONENTS = {
    5120: np.int8,
    5121: np.uint8,
    5122: np.int16,
    5123: np.uint16,
    5125: np.uint32,
    5126: np.float32,
}
#: glTF accessor type -> component count.
_SHAPES = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT2": 4, "MAT3": 9, "MAT4": 16}
_TRIANGLES, _TRIANGLE_STRIP, _TRIANGLE_FAN = 4, 5, 6

#: The specification defines glTF scene units as metres.
GLTF_UNITS = MeshUnits(name="m", scale=1.0)


class GltfLoadError(MeshLoadError):
    """Raised when a file cannot be interpreted as a glTF document."""


def load_gltf(path: str | Path) -> Mesh:
    """Load a ``.glb`` or ``.gltf`` file and flatten it into one mesh.

    A skinned file comes back with its :class:`~refview.core.skeleton.Rig`
    attached and its vertices standing where the file's own node transforms
    put the joints -- which is the bind pose in most files, and the pose the
    file was saved in otherwise, exactly as any other viewer shows it.
    """
    path = Path(path)
    try:
        data = path.read_bytes()
    except OSError as exc:  # pragma: no cover - filesystem dependent
        raise GltfLoadError(f"Cannot read {path}: {exc}") from exc

    document, binary = _split(data, path)
    buffers = _buffers(document, binary, path.parent)

    visited = list(_visit(document))
    skin_index = _first_skin(document, visited)

    positions: list[np.ndarray] = []
    normals: list[np.ndarray] = []
    indices: list[np.ndarray] = []
    joints: list[np.ndarray] = []
    weights: list[np.ndarray] = []
    offset = 0
    for _, node, transform, _ in visited:
        skinned = skin_index is not None and node.get("skin") == skin_index
        for primitive in _primitives(document, node):
            # A skinned primitive is carried by its joints alone: the
            # specification says the mesh node's own transform is ignored.
            block = _primitive_geometry(
                document, buffers, primitive, np.eye(4) if skinned else transform
            )
            if block is None:
                continue
            block_positions, block_normals, block_indices = block
            influence = _primitive_skin(document, buffers, primitive) if skinned else None
            if influence is None:
                influence = (
                    np.zeros((len(block_positions), 4), dtype=np.int32),
                    np.zeros((len(block_positions), 4), dtype=np.float32),
                )
            positions.append(block_positions)
            normals.append(block_normals)
            indices.append(block_indices + offset)
            joints.append(influence[0])
            weights.append(influence[1])
            offset += len(block_positions)

    if not positions:
        raise GltfLoadError(f"{path.name} contains no triangle geometry")

    vertex_array = np.concatenate(positions).astype(np.float32)
    index_array = np.concatenate(indices).astype(np.uint32)
    normal_array = np.concatenate(normals).astype(np.float32)
    if not np.any(normal_array):
        normal_array = compute_vertex_normals(vertex_array, index_array)

    rig = None
    if skin_index is not None:
        rig = _rig(
            document,
            buffers,
            skin_index,
            visited,
            vertex_array,
            normal_array,
            np.concatenate(joints),
            np.concatenate(weights),
        )
        if rig is not None:
            posed, turned = rest_skinned_positions(rig.skin, rig.rest_world())
            vertex_array = posed.astype(np.float32)
            normal_array = turned.astype(np.float32)
    return Mesh(
        vertex_array, normal_array, index_array, name=path.stem, units=GLTF_UNITS, rig=rig
    )


# ----------------------------------------------------------------------
# Containers
# ----------------------------------------------------------------------


def _split(data: bytes, path: Path) -> tuple[dict, bytes | None]:
    """Return the JSON document and the embedded binary chunk, if any."""
    if not data.startswith(_GLB_MAGIC):
        try:
            return json.loads(data.decode("utf-8")), None
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise GltfLoadError(f"{path.name} is not a glTF document") from exc

    document: dict | None = None
    binary: bytes | None = None
    cursor = 12  # magic, version, total length
    while cursor + 8 <= len(data):
        length, kind = struct.unpack_from("<II", data, cursor)
        chunk = data[cursor + 8 : cursor + 8 + length]
        if kind == _JSON_CHUNK:
            document = json.loads(chunk.decode("utf-8"))
        elif kind == _BIN_CHUNK:
            binary = chunk
        cursor += 8 + length + (-length % 4)  # chunks are 4-byte aligned
    if document is None:
        raise GltfLoadError(f"{path.name} has no glTF JSON chunk")
    return document, binary


def _buffers(document: dict, binary: bytes | None, base: Path) -> list[bytes]:
    """Resolve every buffer: the GLB chunk, a data URI or a neighbouring file."""
    resolved: list[bytes] = []
    for buffer in document.get("buffers", []):
        uri = buffer.get("uri")
        if uri is None:
            resolved.append(binary or b"")
        elif uri.startswith("data:"):
            _, _, payload = uri.partition(",")
            resolved.append(base64.b64decode(payload))
        else:
            companion = base / unquote(uri)
            try:
                resolved.append(companion.read_bytes())
            except OSError as exc:
                raise GltfLoadError(f"Cannot read the buffer {uri!r}") from exc
    return resolved


def _accessor(document: dict, buffers: list[bytes], index: int) -> np.ndarray:
    """Read one accessor into an ``(n, components)`` array."""
    try:
        accessor = document["accessors"][index]
        dtype = _COMPONENTS[accessor["componentType"]]
        components = _SHAPES[accessor["type"]]
    except (KeyError, IndexError) as exc:
        raise GltfLoadError("Malformed accessor") from exc

    count = int(accessor.get("count", 0))
    view_index = accessor.get("bufferView")
    if view_index is None:
        return np.zeros((count, components), dtype=dtype)

    view = document["bufferViews"][view_index]
    data = buffers[view.get("buffer", 0)]
    start = view.get("byteOffset", 0) + accessor.get("byteOffset", 0)
    item = np.dtype(dtype).itemsize
    stride = view.get("byteStride") or item * components
    if stride == item * components:
        values = np.frombuffer(data, dtype=dtype, count=count * components, offset=start)
        return values.reshape(count, components)

    # Interleaved data: step through the stride and take the leading fields.
    raw = np.frombuffer(data, dtype=np.uint8, count=stride * count, offset=start)
    rows = raw.reshape(count, stride)[:, : item * components]
    return np.ascontiguousarray(rows).view(dtype).reshape(count, components)


# ----------------------------------------------------------------------
# Scene graph
# ----------------------------------------------------------------------


def _visit(document: dict):
    """Yield ``(index, node, world transform, parent index)`` for the active scene."""
    nodes = document.get("nodes", [])
    scenes = document.get("scenes", [])
    scene = scenes[document.get("scene", 0)] if scenes else {"nodes": range(len(nodes))}

    stack = [(index, np.eye(4), -1) for index in reversed(list(scene.get("nodes", [])))]
    seen: set[int] = set()
    while stack:
        index, parent, above = stack.pop()
        if not 0 <= index < len(nodes) or index in seen:
            continue
        seen.add(index)
        node = nodes[index]
        transform = parent @ _local_transform(node)
        yield index, node, transform, above
        stack.extend((child, transform, index) for child in reversed(node.get("children", [])))


def _local_transform(node: dict) -> np.ndarray:
    """A node's own transform, from either a matrix or a TRS triple."""
    if "matrix" in node:
        # glTF matrices are column-major, which is the transpose of ours.
        return np.asarray(node["matrix"], dtype=np.float64).reshape(4, 4).T

    transform = np.eye(4)
    transform[:3, :3] = _quaternion_matrix(node.get("rotation", (0.0, 0.0, 0.0, 1.0)))
    transform[:3, :3] *= np.asarray(node.get("scale", (1.0, 1.0, 1.0)), dtype=np.float64)
    transform[:3, 3] = np.asarray(node.get("translation", (0.0, 0.0, 0.0)), dtype=np.float64)
    return transform


def _quaternion_matrix(rotation) -> np.ndarray:
    """Rotation matrix for a glTF ``(x, y, z, w)`` quaternion."""
    x, y, z, w = (float(v) for v in rotation)
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ]
    )


def _primitives(document: dict, node: dict) -> list[dict]:
    index = node.get("mesh")
    meshes = document.get("meshes", [])
    if index is None or not 0 <= index < len(meshes):
        return []
    return meshes[index].get("primitives", [])


def _primitive_geometry(
    document: dict, buffers: list[bytes], primitive: dict, transform: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray] | None:
    """Positions, normals and triangle indices for one primitive, in world space."""
    mode = primitive.get("mode", _TRIANGLES)
    attributes = primitive.get("attributes", {})
    if mode not in (_TRIANGLES, _TRIANGLE_STRIP, _TRIANGLE_FAN) or "POSITION" not in attributes:
        return None

    points = _accessor(document, buffers, attributes["POSITION"])[:, :3].astype(np.float64)
    points = points @ transform[:3, :3].T + transform[:3, 3]

    if "NORMAL" in attributes:
        normals = _accessor(document, buffers, attributes["NORMAL"])[:, :3].astype(np.float64)
        normals = normals @ np.linalg.inv(transform[:3, :3])
        lengths = np.linalg.norm(normals, axis=1, keepdims=True)
        normals = normals / np.maximum(lengths, 1e-20)
    else:
        normals = np.zeros_like(points)

    if "indices" in primitive:
        order = _accessor(document, buffers, primitive["indices"]).reshape(-1).astype(np.int64)
    else:
        order = np.arange(len(points), dtype=np.int64)
    triangles = _triangulate(order, mode)
    if triangles is None:
        return None
    return points, normals, triangles


def _triangulate(order: np.ndarray, mode: int) -> np.ndarray | None:
    """Turn a triangle list, strip or fan into an ``(t, 3)`` index array."""
    if mode == _TRIANGLES:
        usable = len(order) - len(order) % 3
        return order[:usable].reshape(-1, 3) if usable else None
    if len(order) < 3:
        return None
    if mode == _TRIANGLE_FAN:
        return np.stack((np.full(len(order) - 2, order[0]), order[1:-1], order[2:]), axis=1)
    # Strips alternate winding, so every other triangle swaps two corners.
    triangles = np.stack((order[:-2], order[1:-1], order[2:]), axis=1)
    triangles[1::2] = triangles[1::2][:, [1, 0, 2]]
    return triangles


# ----------------------------------------------------------------------
# Skins
# ----------------------------------------------------------------------

#: Component type -> the value that means "all of it" for a normalized weight.
_WEIGHT_FULL = {np.uint8: 255.0, np.uint16: 65535.0}


def _first_skin(document: dict, visited: list) -> int | None:
    """The skin the first skinned mesh node uses, or ``None``.

    One skin is read.  A file with several -- a character and a separate
    rigged prop -- keeps its first figure posable and loads the rest still.
    """
    skins = document.get("skins", [])
    for _, node, _, _ in visited:
        index = node.get("skin")
        if index is not None and 0 <= index < len(skins) and node.get("mesh") is not None:
            return int(index)
    return None


def _primitive_skin(
    document: dict, buffers: list[bytes], primitive: dict
) -> tuple[np.ndarray, np.ndarray] | None:
    """The four joints and four weights of every vertex of a primitive."""
    attributes = primitive.get("attributes", {})
    if "JOINTS_0" not in attributes or "WEIGHTS_0" not in attributes:
        return None
    joints = _accessor(document, buffers, attributes["JOINTS_0"])[:, :4].astype(np.int32)
    raw = _accessor(document, buffers, attributes["WEIGHTS_0"])[:, :4]
    full = _WEIGHT_FULL.get(raw.dtype.type)
    weights = raw.astype(np.float32) / full if full else raw.astype(np.float32)
    # Weights are meant to sum to one; a file that rounded them is put right.
    total = weights.sum(axis=1, keepdims=True)
    weights = np.where(total > 0.0, weights / np.maximum(total, 1e-12), weights)
    return joints, weights.astype(np.float32)


def _rig(
    document: dict,
    buffers: list[bytes],
    skin_index: int,
    visited: list,
    positions: np.ndarray,
    normals: np.ndarray,
    joints: np.ndarray,
    weights: np.ndarray,
) -> Rig | None:
    """The file's skeleton and its skin, in the file's own coordinates."""
    skin = document["skins"][skin_index]
    joint_nodes = [int(index) for index in skin.get("joints", [])]
    if not joint_nodes:
        return None
    nodes = document.get("nodes", [])
    world = {index: transform for index, _, transform, _ in visited}
    above = {index: parent for index, _, _, parent in visited}
    # A joint the scene never reaches still needs a place; it stands at the
    # origin, which is wrong but is not a crash.
    for index in joint_nodes:
        world.setdefault(index, np.eye(4))
        above.setdefault(index, -1)

    slot = {node: position for position, node in enumerate(joint_nodes)}
    parents = []
    rest_local = np.empty((len(joint_nodes), 4, 4), dtype=np.float64)
    for position, node in enumerate(joint_nodes):
        # The parent joint is the nearest ancestor node that is also a joint;
        # nodes in between (a group, an empty) fold into the rest transform.
        walk = above.get(node, -1)
        while walk >= 0 and walk not in slot:
            walk = above.get(walk, -1)
        parent = slot.get(walk, -1) if walk >= 0 else -1
        parents.append(parent)
        if parent >= 0:
            rest_local[position] = np.linalg.inv(world[joint_nodes[parent]]) @ world[node]
        else:
            rest_local[position] = world[node]

    if "inverseBindMatrices" in skin:
        # Column-major in the file, like a node's matrix.
        inverse_bind = (
            _accessor(document, buffers, skin["inverseBindMatrices"])
            .astype(np.float64)
            .reshape(-1, 4, 4)
            .transpose(0, 2, 1)
        )
        if len(inverse_bind) < len(joint_nodes):
            raise GltfLoadError("The skin has fewer bind matrices than joints")
        inverse_bind = inverse_bind[: len(joint_nodes)]
    else:
        inverse_bind = np.tile(np.eye(4), (len(joint_nodes), 1, 1))

    names = []
    for position, node in enumerate(joint_nodes):
        name = nodes[node].get("name") if 0 <= node < len(nodes) else None
        names.append(name if name else f"joint_{position}")
    # A vertex claiming a joint the skin does not have is let go of.
    stray = joints >= len(joint_nodes)
    if np.any(stray):
        joints = np.where(stray, 0, joints)
        weights = np.where(stray, 0.0, weights)
    return Rig(names, parents, rest_local, Skin(joints, weights, inverse_bind, positions, normals))
