"""GLSL sources for the viewport, read from :file:`render/glsl`.

A handful of small programs cover everything the viewer draws: a fullscreen
background -- the gradient, or the HDRI -- the shaded mesh, a constant-colour
pass reused for the wireframe and the cut cap, the widened surface strokes, a
depth-only pass that feeds both the shadow map and the occlusion pre-pass, the
two fullscreen passes that turn that depth into ambient occlusion, and one
more that resolves a ghosted model out of the sums the mesh pass left for
it.  The mesh shader branches on ``uMode``, whose values mirror
:attr:`refview.core.settings.ShadingMode.shader_id`, and on ``uPlaneMode``,
which mirrors :attr:`refview.core.settings.PlaneMode.shader_id`.

The sources themselves are ``.vert``, ``.frag`` and ``.glsl`` files beside
this module; :mod:`refview.render.shader_files` reads them.  Cross-section
clipping is shared rather than duplicated: any shader that includes
``section.glsl`` gets the half-space test, so the mesh, the wireframe, the
annotations and the shadow map all disappear at the cut together.

Lighting is deliberately evaluated in display space rather than linear space:
the colour swatches in the UI are what lands on screen, which is the
behaviour artists expect from a reference viewer.  The Human Skin mode is the
exception, and works in linear radiance; see ``skin.glsl``.
"""

from __future__ import annotations

from ..core.plane_axes import MAX_PLANE_AXES
from .shader_files import load_glsl
from .skin_shader import SKIN_CONSTANTS

#: Numbers the shaders are compiled with, which the Python side also uses.
CONSTANTS = {"MAX_PLANE_AXES": MAX_PLANE_AXES, **SKIN_CONSTANTS}

FULLSCREEN_VERTEX = load_glsl("fullscreen.vert")
BACKGROUND_VERTEX = FULLSCREEN_VERTEX
BACKGROUND_FRAGMENT = load_glsl("background.frag")

MESH_VERTEX = load_glsl("mesh.vert")
#: The mesh shader twice over.  Whether the skin traces rays is a constant
#: in each rather than a uniform: a GPU sizes a shader's registers for the
#: heaviest path in it, and the tracer is by far the heaviest, so with the
#: two in one program every mode -- Lambert as much as the skin preview --
#: ran as slowly as the tracer let it.  The renderer switches to the second
#: only for the frames it is refining.
MESH_FRAGMENT = load_glsl("mesh.frag", CONSTANTS, {"uSkinTrace": "false"})
MESH_TRACE_FRAGMENT = load_glsl("mesh.frag", CONSTANTS, {"uSkinTrace": "true"})

FLAT_VERTEX = load_glsl("flat.vert")
FLAT_FRAGMENT = load_glsl("flat.frag")
DEPTH_VERTEX = load_glsl("depth.vert")
DEPTH_FRAGMENT = load_glsl("depth.frag")
STROKE_VERTEX = load_glsl("stroke.vert")
STROKE_FRAGMENT = load_glsl("stroke.frag")
OCCLUSION_FRAGMENT = load_glsl("occlusion.frag")
RESOLVE_FRAGMENT = load_glsl("resolve.frag")
BLUR_FRAGMENT = load_glsl("blur.frag")
OUTLINE_FRAGMENT = load_glsl("outline.frag")
GHOST_FRAGMENT = load_glsl("ghost.frag")
