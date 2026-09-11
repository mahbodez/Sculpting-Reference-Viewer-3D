"""Offscreen render targets used by the high-quality and ghost passes.

Four of them are needed: a depth map rendered from the light for shadows, a
depth-and-normal buffer rendered from the camera for ambient occlusion, a pair
of single-channel colour buffers the occlusion is computed and blurred in, and
the two-attachment buffer a see-through model is summed into.

Qt draws a :class:`QOpenGLWidget` into a framebuffer of its own, so the
"default" framebuffer is rarely object zero.  Callers capture whatever was
bound before they started and hand it to :func:`bind_default` afterwards.
"""

from __future__ import annotations

from OpenGL import GL


def current_framebuffer() -> int:
    """The framebuffer object bound right now -- Qt's, in a widget."""
    return int(GL.glGetIntegerv(GL.GL_FRAMEBUFFER_BINDING))


def bind_default(framebuffer: int) -> None:
    """Restore a framebuffer captured with :func:`current_framebuffer`."""
    GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, framebuffer)


def _require_complete(name: str) -> None:
    """Fail loudly on an unusable attachment rather than rendering nothing.

    An incomplete framebuffer draws silently into the void, which looks like a
    subtly wrong shader instead of the driver refusing the format it was given.
    """
    status = GL.glCheckFramebufferStatus(GL.GL_FRAMEBUFFER)
    if status != GL.GL_FRAMEBUFFER_COMPLETE:
        raise RuntimeError(f"The {name} framebuffer is incomplete (status 0x{status:04x})")


class _Target:
    """Shared lifetime handling for a framebuffer with one attachment.

    The GL objects are created on the first :meth:`resize`, so a target can be
    constructed alongside the renderer -- before a context exists.
    """

    def __init__(self) -> None:
        self._fbo = 0
        self._texture = 0
        self._width = 0
        self._height = 0

    @property
    def texture(self) -> int:
        return self._texture

    def resize(self, width: int, height: int) -> None:
        """Reallocate the attachment, but only when the size actually changed."""
        width, height = max(int(width), 1), max(int(height), 1)
        if (width, height) == (self._width, self._height):
            return
        if not self._fbo:
            self._fbo = int(GL.glGenFramebuffers(1))
            self._texture = int(GL.glGenTextures(1))
        self._width, self._height = width, height
        self._allocate(width, height)

    def bind(self) -> None:
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._fbo)
        GL.glViewport(0, 0, self._width, self._height)

    def bind_texture(self, unit: int) -> None:
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)

    def dispose(self) -> None:
        if self._texture:
            GL.glDeleteTextures(1, [self._texture])
            self._texture = 0
        if self._fbo:
            GL.glDeleteFramebuffers(1, [self._fbo])
            self._fbo = 0

    def _allocate(self, width: int, height: int) -> None:  # pragma: no cover - overridden
        raise NotImplementedError


class DepthTarget(_Target):
    """A depth-only framebuffer, sampled afterwards as a texture."""

    def __init__(self, clamp_to_lit: bool = False) -> None:
        """``clamp_to_lit`` makes everything outside the map read as unshadowed."""
        super().__init__()
        self._clamp_to_lit = clamp_to_lit

    def _allocate(self, width: int, height: int) -> None:
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D,
            0,
            GL.GL_DEPTH_COMPONENT24,
            width,
            height,
            0,
            GL.GL_DEPTH_COMPONENT,
            GL.GL_FLOAT,
            None,
        )
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
        wrap = GL.GL_CLAMP_TO_BORDER if self._clamp_to_lit else GL.GL_CLAMP_TO_EDGE
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, wrap)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, wrap)
        if self._clamp_to_lit:
            GL.glTexParameterfv(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_BORDER_COLOR, [1.0, 1.0, 1.0, 1.0])

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._fbo)
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, GL.GL_TEXTURE_2D, self._texture, 0
        )
        # A depth-only target still has to say it draws no colour.
        GL.glDrawBuffer(GL.GL_NONE)
        GL.glReadBuffer(GL.GL_NONE)
        _require_complete("depth")
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)


class ColorTarget(_Target):
    """A single-channel colour framebuffer, used for the occlusion buffers."""

    def _allocate(self, width: int, height: int) -> None:
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._texture)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D, 0, GL.GL_R8, width, height, 0, GL.GL_RED, GL.GL_UNSIGNED_BYTE, None
        )
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP_TO_EDGE)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP_TO_EDGE)

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._fbo)
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self._texture, 0
        )
        _require_complete("colour")
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)


class GeometryTarget(DepthTarget):
    """Depth plus view-space normals: the inputs the occlusion pass reads.

    Storing the normal rather than deriving it from neighbouring depth samples
    is what keeps a large flat surface -- a pedestal seen almost edge-on --
    from occluding itself in bands.
    """

    def __init__(self) -> None:
        super().__init__()
        self._normals = 0

    def _allocate(self, width: int, height: int) -> None:
        super()._allocate(width, height)
        if not self._normals:
            self._normals = int(GL.glGenTextures(1))
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._normals)
        GL.glTexImage2D(
            GL.GL_TEXTURE_2D, 0, GL.GL_RGBA16F, width, height, 0, GL.GL_RGBA, GL.GL_FLOAT, None
        )
        for parameter in (GL.GL_TEXTURE_MIN_FILTER, GL.GL_TEXTURE_MAG_FILTER):
            GL.glTexParameteri(GL.GL_TEXTURE_2D, parameter, GL.GL_NEAREST)
        for parameter in (GL.GL_TEXTURE_WRAP_S, GL.GL_TEXTURE_WRAP_T):
            GL.glTexParameteri(GL.GL_TEXTURE_2D, parameter, GL.GL_CLAMP_TO_EDGE)

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._fbo)
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self._normals, 0
        )
        GL.glDrawBuffer(GL.GL_COLOR_ATTACHMENT0)  # DepthTarget switched this off.
        _require_complete("geometry")
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def bind_normals(self, unit: int) -> None:
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._normals)

    def dispose(self) -> None:
        if self._normals:
            GL.glDeleteTextures(1, [self._normals])
            self._normals = 0
        super().dispose()


class AccumTarget(_Target):
    """The pair of buffers a see-through model is summed into.

    Attachment 0 holds the weighted sum of the colours that covered a pixel,
    with the total weight in its alpha; attachment 1 holds the sum of
    ``log(1 - alpha)`` over the same fragments, whose exponential is the
    product of their transmittances -- how much of the scene behind still
    shows through.  Both are plain additions, so one blend function serves for
    both attachments, which is all OpenGL 3.3 offers, and neither sum can
    depend on the order the fragments arrived in.

    A depth attachment comes with them.  The model still has to be hidden by
    the opaque geometry already drawn, and an offscreen framebuffer cannot
    borrow the depth buffer Qt handed the widget, so the opaque shapes are laid
    in here again depth-only.  It is never sampled, hence a renderbuffer.
    """

    def __init__(self) -> None:
        super().__init__()
        self._reveal = 0
        self._depth = 0

    def _allocate(self, width: int, height: int) -> None:
        if not self._reveal:
            self._reveal = int(GL.glGenTextures(1))
        if not self._depth:
            self._depth = int(GL.glGenRenderbuffers(1))

        # Floating point, and not for the dynamic range: the colour sum passes
        # one as soon as a second surface lands on a pixel, and clamping it at
        # the attachment would be exactly the breakage the sum exists to avoid.
        for texture, internal, layout in (
            (self._texture, GL.GL_RGBA16F, GL.GL_RGBA),
            (self._reveal, GL.GL_R16F, GL.GL_RED),
        ):
            GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
            GL.glTexImage2D(
                GL.GL_TEXTURE_2D, 0, internal, width, height, 0, layout, GL.GL_FLOAT, None
            )
            for parameter in (GL.GL_TEXTURE_MIN_FILTER, GL.GL_TEXTURE_MAG_FILTER):
                GL.glTexParameteri(GL.GL_TEXTURE_2D, parameter, GL.GL_NEAREST)
            for parameter in (GL.GL_TEXTURE_WRAP_S, GL.GL_TEXTURE_WRAP_T):
                GL.glTexParameteri(GL.GL_TEXTURE_2D, parameter, GL.GL_CLAMP_TO_EDGE)

        GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, self._depth)
        GL.glRenderbufferStorage(GL.GL_RENDERBUFFER, GL.GL_DEPTH_COMPONENT24, width, height)
        GL.glBindRenderbuffer(GL.GL_RENDERBUFFER, 0)

        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self._fbo)
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, GL.GL_TEXTURE_2D, self._texture, 0
        )
        GL.glFramebufferTexture2D(
            GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT1, GL.GL_TEXTURE_2D, self._reveal, 0
        )
        GL.glFramebufferRenderbuffer(
            GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, GL.GL_RENDERBUFFER, self._depth
        )
        # Kept with the framebuffer, so the shader's second output lands on the
        # second attachment every time this target is bound.
        GL.glDrawBuffers(2, [GL.GL_COLOR_ATTACHMENT0, GL.GL_COLOR_ATTACHMENT1])
        _require_complete("accumulation")
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def clear(self) -> None:
        """Empty both sums, and the depth nothing has been laid into yet.

        Zero starts each of them: no colour, and ``log(1) == 0`` for a pixel
        nothing has passed through.
        """
        empty = [0.0, 0.0, 0.0, 0.0]
        GL.glClearBufferfv(GL.GL_COLOR, 0, empty)
        GL.glClearBufferfv(GL.GL_COLOR, 1, empty)
        GL.glClear(GL.GL_DEPTH_BUFFER_BIT)

    def bind_reveal(self, unit: int) -> None:
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self._reveal)

    def dispose(self) -> None:
        if self._reveal:
            GL.glDeleteTextures(1, [self._reveal])
            self._reveal = 0
        if self._depth:
            GL.glDeleteRenderbuffers(1, [self._depth])
            self._depth = 0
        super().dispose()
