"""Idle scheduling, asynchronous BVH preparation, shared skin tables and history."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from time import monotonic

from OpenGL import GL
from OpenGL.error import GLError

from .framebuffer import FrameTarget, bind_default
from .program import ShaderProgram
from .skin_bvh import build_scene, texture_table
from .skin_detail import diffusion_lut, relief_volume
from .skin_shader import ACCUMULATE_FRAGMENT, PRESENT_FRAGMENT
from .texture import DataTexture, Texture3D

#: Texture units the skin tables live on, after the ghost's pair.
NODES_UNIT, TRIANGLES_UNIT, RELIEF_UNIT, DIFFUSION_UNIT = 6, 7, 8, 9


def pixel_jitter(sample: int) -> tuple[float, float]:
    """Centred Halton 2,3 subpixel sample, stable across repeated exports."""
    def radical(base):
        index, weight, result = sample + 1, 1.0, 0.0
        while index:
            index, digit = divmod(index, base)
            weight /= base
            result += digit * weight
        return result - 0.5
    return radical(2), radical(3)


class RefinementClock:
    """Restart on any image change; never mix a moving preview into the sum."""

    def __init__(self):
        self.key = None
        self.changed = 0.0
        self.samples = 0

    def ready(self, key, now: float, interactive: bool = False) -> bool:
        if key != self.key or interactive:
            self.key, self.changed, self.samples = key, now, 0
        return now - self.changed >= 0.20


class SkinRefinement:
    def __init__(self):
        self.clock = RefinementClock()
        self.current = FrameTarget(floating=True)
        self.history = [FrameTarget(floating=True), FrameTarget(floating=True)]
        self.nodes = self.triangles = None
        self.relief = self.diffusion = None
        self.node_count = 0
        self.programs = {}
        self.executor = None
        self.pending = None
        self.revision = None
        self.failure = ""
        self.needs_frame = False
        self.tracing = False
        self.status = ""

    def initialize(self, vertex):
        self.programs = {
            "accumulate": ShaderProgram(vertex, ACCUMULATE_FRAGMENT, "skin accumulation"),
            "present": ShaderProgram(vertex, PRESENT_FRAGMENT, "skin presentation"),
        }
        self.nodes, self.triangles = DataTexture(), DataTexture()
        # Complete sampler textures even before any mesh has been prepared.
        import numpy as np
        empty = np.zeros((1, 1, 4), np.float32)
        self.nodes.upload(empty)
        self.triangles.upload(empty)
        # The preview needs these as much as refinement does; both are fixed
        # tables, built once from NumPy.
        self.relief = Texture3D()
        self.relief.upload(relief_volume())
        self.diffusion = DataTexture(filtered=True)
        self.diffusion.upload(diffusion_lut())

    def prepare(self, key, revision, parts, skin, interactive, enabled):
        self.tracing = False
        self.needs_frame = False
        if not enabled:
            self.clock.key = None
            self.clock.samples = 0
            self.status = "Preview"
            return False
        idle = self.clock.ready(key, monotonic(), interactive)
        self.needs_frame = self.clock.samples < skin.samples
        self.status = "Preview — refining when idle"
        if not idle:
            return False
        if revision != self.revision:
            if self.pending is None:
                if self.executor is None:
                    self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="skin-bvh")
                self.pending = (revision, self.executor.submit(build_scene, parts))
            pending_revision, future = self.pending
            if not future.done():
                self.status = "Preview — preparing ray tracing"
                return False
            self.pending = None
            if pending_revision != revision:
                return False  # Discard an obsolete mesh; submit the new one next frame.
            self.revision = revision
            self.failure = ""
            try:
                scene = future.result()
                limit = int(GL.glGetIntegerv(GL.GL_MAX_TEXTURE_SIZE))
                nodes = texture_table(scene.nodes, limit)
                triangles = texture_table(scene.triangles, limit)
                self.nodes.upload(nodes)
                self.triangles.upload(triangles)
                self.node_count = len(scene.nodes)
            except (ValueError, MemoryError, RuntimeError, GLError) as error:
                self.failure = str(error)
                self.node_count = 0
        if self.failure or not self.node_count:
            self.status = "Preview — " + (self.failure or "no geometry")
            self.needs_frame = False
            return False
        self.tracing = True
        self.status = f"Human Skin · {self.clock.samples}/{skin.samples} samples"
        return True

    def bind(self, program):
        program.set_bool("uSkinTrace", self.tracing)
        program.set_int("uSkinSample", self.clock.samples)
        program.set_int("uSkinNodeCount", self.node_count)
        program.set_int("uSkinNodes", NODES_UNIT)
        program.set_int("uSkinTriangles", TRIANGLES_UNIT)
        program.set_int("uSkinRelief", RELIEF_UNIT)
        program.set_int("uSkinDiffusion", DIFFUSION_UNIT)
        self.nodes.bind(NODES_UNIT)
        self.triangles.bind(TRIANGLES_UNIT)
        self.relief.bind(RELIEF_UNIT)
        self.diffusion.bind(DIFFUSION_UNIT)
        GL.glActiveTexture(GL.GL_TEXTURE0)

    def begin(self, width, height):
        self.current.resize(width, height)
        for target in self.history:
            target.resize(width, height)
        self.current.bind()

    def accumulate(self, draw):
        index = self.clock.samples % 2
        self.history[index].bind()
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_BLEND)
        with self.programs["accumulate"] as program:
            self.current.bind_texture(0)
            self.history[1-index].bind_texture(1)
            program.set_int("uCurrent", 0)
            program.set_int("uHistory", 1)
            program.set_int("uSamples", self.clock.samples)
            draw()
        self.clock.samples += 1

    def present(self, screen, width, height, draw):
        bind_default(screen)
        GL.glViewport(0, 0, width, height)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glDisable(GL.GL_BLEND)
        with self.programs["present"] as program:
            self.history[(self.clock.samples-1) % 2].bind_texture(0)
            program.set_int("uFrame", 0)
            draw()

    def dispose(self):
        if self.executor is not None:
            self.executor.shutdown(wait=False, cancel_futures=True)
            self.executor = None
        self.pending = None
        for target in [self.current, *self.history]:
            target.dispose()
        # New objects reset cached dimensions if Qt recreates the GL context.
        self.current = FrameTarget(floating=True)
        self.history = [FrameTarget(floating=True), FrameTarget(floating=True)]
        for texture in (self.nodes, self.triangles, self.relief, self.diffusion):
            if texture is not None:
                texture.dispose()
        for program in self.programs.values():
            program.dispose()
        self.programs.clear()
        self.revision = None
        self.clock = RefinementClock()
