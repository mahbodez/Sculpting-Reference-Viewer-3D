"""Geometry for the surface annotations and the cross-section contour.

Strokes are drawn as real geometry rather than as a 2D overlay so that the
depth buffer hides the ones on the far side of the model -- paint on the back
of a head must not show through the face.  Each segment becomes a quad that
the vertex shader widens in screen space, which gives a constant pixel width
at any zoom without relying on ``glLineWidth``.
"""

from __future__ import annotations

import ctypes

import numpy as np
from OpenGL import GL

from ..core.annotation import Stroke

#: pos(3) other(3) normal(3) colour(3) side(1) width(1)
_FLOATS_PER_VERTEX = 14
_STRIDE = _FLOATS_PER_VERTEX * 4
#: (offset in floats, component count) for each vertex attribute.
_ATTRIBUTES = ((0, 3), (3, 3), (6, 3), (9, 3), (12, 1), (13, 1))


def build_vertices(strokes: list[Stroke]) -> np.ndarray:
    """Expand strokes into the triangle soup the stroke shader expects.

    Every segment contributes six vertices.  A vertex carries its own position
    and the segment's other end, so the shader can derive the screen-space
    direction it needs to widen the quad.
    """
    blocks = []
    for stroke in strokes:
        block = _segment_block(stroke)
        if block is not None:
            blocks.append(block)
    if not blocks:
        return np.zeros((0, _FLOATS_PER_VERTEX), dtype=np.float32)
    return np.concatenate(blocks, axis=0)


def build_segment_vertices(
    segments: np.ndarray, color, width: float, normal=(0.0, 0.0, 0.0)
) -> np.ndarray:
    """Expand loose ``(n, 2, 3)`` segments -- the section contour -- the same way.

    The contour is not a polyline: plane-cut triangles produce segments in no
    particular order, and joining them into loops would buy nothing the shader
    does not already handle.
    """
    segments = np.asarray(segments, dtype=np.float64).reshape(-1, 2, 3)
    if len(segments) == 0:
        return np.zeros((0, _FLOATS_PER_VERTEX), dtype=np.float32)
    lift = np.tile(np.asarray(normal, dtype=np.float64), (len(segments), 1))
    return _expand(segments[:, 0], segments[:, 1], lift, lift, color, width)


def _segment_block(stroke: Stroke) -> np.ndarray | None:
    if not stroke.is_drawable:
        return None
    points = stroke.point_array
    normals = stroke.normal_array
    if stroke.closed and len(points) > 2:
        points = np.vstack((points, points[:1]))
        normals = np.vstack((normals, normals[:1]))
    return _expand(points[:-1], points[1:], normals[:-1], normals[1:], stroke.color, stroke.width)


def _expand(
    head: np.ndarray,
    tail: np.ndarray,
    head_normal: np.ndarray,
    tail_normal: np.ndarray,
    color,
    width: float,
) -> np.ndarray:
    """Six vertices per segment, in the layout the stroke shader expects."""
    count = len(head)

    # Corner order: (head, left) (tail, left) (tail, right) then the second
    # triangle (head, left) (tail, right) (head, right).  A vertex at the tail
    # looks back down the segment, so its side flips to stay on the same edge.
    position = np.stack((head, tail, tail, head, tail, head), axis=1)
    other = np.stack((tail, head, head, tail, head, tail), axis=1)
    normal = np.stack(
        (head_normal, tail_normal, tail_normal, head_normal, tail_normal, head_normal), axis=1
    )
    side = np.tile(np.array([1.0, -1.0, 1.0, 1.0, 1.0, -1.0]), (count, 1))

    block = np.empty((count, 6, _FLOATS_PER_VERTEX), dtype=np.float32)
    block[..., 0:3] = position
    block[..., 3:6] = other
    block[..., 6:9] = normal
    block[..., 9:12] = np.asarray(color, dtype=np.float32)
    block[..., 12] = side
    block[..., 13] = width
    return block.reshape(-1, _FLOATS_PER_VERTEX)


class StrokeBuffers:
    """A single vertex buffer holding every visible stroke."""

    def __init__(self) -> None:
        self._vao = int(GL.glGenVertexArrays(1))
        self._vbo = int(GL.glGenBuffers(1))
        self._vertex_count = 0
        self._capacity = 0

        GL.glBindVertexArray(self._vao)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._vbo)
        for index, (offset, size) in enumerate(_ATTRIBUTES):
            GL.glEnableVertexAttribArray(index)
            GL.glVertexAttribPointer(
                index, size, GL.GL_FLOAT, GL.GL_FALSE, _STRIDE, ctypes.c_void_p(offset * 4)
            )
        GL.glBindVertexArray(0)

    @property
    def is_empty(self) -> bool:
        return self._vertex_count == 0

    def upload(self, strokes: list[Stroke]) -> None:
        self.upload_vertices(build_vertices(strokes))

    def upload_vertices(self, vertices: np.ndarray) -> None:
        """Replace the buffer contents with a prepared vertex block."""
        vertices = np.ascontiguousarray(vertices, dtype=np.float32)
        self._vertex_count = len(vertices)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self._vbo)
        if vertices.nbytes > self._capacity:
            # Painting grows the buffer stroke by stroke; reallocating only
            # when it actually outgrows the storage keeps that cheap.
            GL.glBufferData(GL.GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL.GL_DYNAMIC_DRAW)
            self._capacity = vertices.nbytes
        elif vertices.nbytes:
            GL.glBufferSubData(GL.GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

    def draw(self) -> None:
        if self.is_empty:
            return
        GL.glBindVertexArray(self._vao)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self._vertex_count)
        GL.glBindVertexArray(0)

    def dispose(self) -> None:
        GL.glDeleteBuffers(1, [self._vbo])
        GL.glDeleteVertexArrays(1, [self._vao])
        self._vertex_count = 0
        self._capacity = 0
