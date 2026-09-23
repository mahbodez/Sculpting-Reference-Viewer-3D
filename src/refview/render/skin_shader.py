"""Skin BRDF and bounded-depth light transport, shared by preview and refinement.

The surface carries three normals: the relief-bumped one for the specular
lobes, a gentler bump for diffuse, and the smooth geometric one for diffusion,
since light that has travelled through the dermis has forgotten the pores it
entered by. Two dielectric GGX lobes approximate broad skin and narrow sebum
reflections; a grazing sheen stands in for vellus hair. Albedo is unevenly
pigmented and flushed with blood from the same tileable volume that carries
the relief. Diffusion follows Burley's normalised profile: the preview reads a
curvature-indexed pre-integration of it, idle samples draw radii from it and
project them onto the nearby surface. Transmission is Beer attenuation through
the traced thickness. This is an RGB diffusion approximation, not a spectral
layered tissue or volumetric random-walk solver.

The marks -- freckles, moles and acne -- are round spots on jittered lattices
worked out in the shader from the world position: each lattice cell holds at
most one spot, jittered by no more than a quarter of the cell and no wider
than a quarter, so the cell a point falls in is the only one that can mark
it and one hash per lattice decides everything about that spot.  Blemishes
are patches read off the relief volume's tone channel at a coarser scale.
Where each falls, and how thickly, is scaled by the body map: a small volume
of region weights laid over the scene, read at the same world position, and
a multiplier per region and per kind of mark.
"""

from .shader_files import load_glsl
from .skin_detail import LUT_LOG_MIN, LUT_LOG_SPAN, RELIEF_CELLS

#: The table sizes ``skin.glsl`` is compiled against, set where the tables are built.
SKIN_CONSTANTS = {
    "CELLS": float(RELIEF_CELLS),
    "LUT_MIN": float(LUT_LOG_MIN),
    "LUT_SPAN": float(LUT_LOG_SPAN),
}

#: The skin's functions, spliced into the mesh shader through ``#include``;
#: kept here as a string for the tests that read it.
SKIN_GLSL = load_glsl("skin.glsl", SKIN_CONSTANTS)
ACCUMULATE_FRAGMENT = load_glsl("skin_accumulate.frag")
PRESENT_FRAGMENT = load_glsl("skin_present.frag")
