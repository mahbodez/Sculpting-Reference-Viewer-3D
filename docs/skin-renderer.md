# Human Skin renderer

The mode is a practical reference material for untextured meshes. It does not
infer pigmentation, pores, blood flow, or regional tissue properties from shape.
Palettes are editable tone examples rather than measurements of populations.

## Surface

Meshes arrive without a UV layout, so the surface detail is a tileable 3D field
sampled at world position rather than a texture that needs an unwrap. NumPy
builds a 64³ RGBA16F volume once at start-up (`core/skin_detail.py`): pores
are Gaussian pits at Worley cell points, furrows follow the Voronoi edges
between them, low-frequency noise varies their depth, and two octaves of value
noise add grain. The volume stores the *slope* of that height field, in height
per cell width, so bump mapping is one fetch with no tangent frame and the
relief keeps its look at any pore size. A second, rotated fetch hides the tile
period. The alpha channel is a smooth tileable noise used at larger scales for
pigment mottling and blood flush.

The shader derives three normals from the relief, as skin behaves as if it had:

- **Specular** sees the full relief (`Surface detail`).
- **Diffuse** sees roughly a third of it.
- **Diffusion** sees none: light that has travelled through the dermis has
  forgotten the pore it entered by, so scattering, the pre-integrated wrap and
  curvature all use the smooth geometric normal.

The relief fades out once a pore covers only a few pixels, because past that
point its bumps can only alias; the volume's mip chain averages what remains.
Detail is anchored in world space, so a posed or sculpted mesh carries the
pattern through its surface rather than with it.

Albedo is not uniform. `Tone variation` lightens and darkens patches of pigment
and `Blood / flush` pulls patches, cavities and transmitted light towards a
haemoglobin tint. `Peach fuzz` is a grazing-angle sheen standing in for vellus
hair, lit from the light's side and a little from behind.

`Subtle veins` draws a narrow, warped contour from two coarse samples of the
same volume. It leaves a faint cool trace in reflected light and adds local
absorption when light travels through the tissue. Its footprint fades below a
pixel, and setting it to zero skips both extra volume reads. The pattern is a
procedural visual cue, not an inferred vascular map. Existing tone and flush
samples introduce small changes in the width and intensity along each vein,
without adding a third vessel texture lookup.

## Marks and body regions

Skin is marked, and the marks are what separate it from *perfect* skin. Four
controls, all starting at nought:

- `Freckles`: small light-brown dots, thick on the ground, flat.
- `Moles`: dark, a few pores across, few and far between, faintly raised, a
  minority lighter.
- `Acne`: red papules, raised and shining (the oily lobe is turned up on the
  dome), a share of them with a pale head at the centre.
- `Blemishes`: patches, coarser than the pores, of irritated redness and of
  dry, duller and rougher skin, read off the relief volume's tone channel at
  two scales that share no period.

The spots are not textures. Each kind lives on a jittered lattice in world
units, its cell a fixed number of pores wide (4, 10 and 6 for freckles,
moles and acne), so the marks scale with `Pore size`. A cell holds at most
one spot, jittered by no more than a quarter of the cell and no wider than a
quarter, which means the cell a point falls in is the only one whose spot can
reach it: one hash of the cell index decides whether there is a spot, where
in the cell it sits, how big it is and what kind it is, and there is no
period to hide. A 3D lattice would seldom put a sphere on a surface, so the
lattices are two-dimensional and *triplanar*: each point is marked on the
three axis planes, blended by how squarely the surface faces each, the way a
texture is put on a mesh with no UV layout. Every spot is therefore a disc on
the skin whichever way the skin turns; the cost of the blend is a spot fading
in or out across a 45° zone, which the eye reads as a freckle no more than
it does the pores. Each lattice fades out once a cell covers a few pixels,
before its spots could sparkle. The bumps of moles and papules are slopes
added to the relief's, applied whatever `Surface detail` says: a papule
stands up on the smoothest skin.

Where the marks fall is the **Body Regions** group's business, and
`core/body_regions.py` works it out from what the scene knows. A skeleton
with humanoid roles -- the preset, a rig read by its names, one grown out of
the guided armature -- gives a bone per role (a role'd joint to its nearest
role'd ancestor, unnamed helpers stepped over), and each vertex goes to the
region of the nearest bone, softened between bones over a few percent of
the figure's height. Without one, height bands from the eight-head canon
tell the feet, the legs, the torso, the neck and the head apart -- arms and
hands cannot be told this way -- and the artist can instead say the whole
model is one region, for a bust or a hand. Seven regions, each a
`RegionProfile` of multipliers for acne, moles, freckles, blemishes, the
oily lobe, the flush and veins, starting from where those effects tend to fall.
The default vein multiplier is higher for hands, feet and arms, and lower on
the torso. Old saved profiles lacking this field load it as one, preserving
their previous global vein strength.

The shader reads the regions from a *body map*: a 64³ volume over the
scene's box, two RGBA textures' worth, with a weight per region and, last,
how much of the voxel is assigned at all. It is splatted from the vertices
and the triangle centres of every shown object and filled six voxels out
from them by neighbour averaging, so a fragment between coarse vertices
still reads a value and the inside of a solid, which nothing samples, stays
unassigned; unassigned reads as a multiplier of one. `ViewerState.body_source`
snapshots the parts, the bones and the settings under a key; the renderer
hands that to `SkinRefinement.prepare_body`, which builds the map on the
shared worker when the key changes and the scene is not being dragged, and
bumps a serial the accumulation key includes when a map lands. The
per-region multipliers are fourteen `vec4` uniforms, so turning a region up
or down costs nothing but a frame.

## Material and transport

Colours are sRGB controls, decoded before lighting. The surface is dielectric
(index of refraction approximately 1.4, normal reflectance 0.0278), with two GGX
lobes: adjustable broad roughness and a narrower 0.18-roughness oil lobe. Oiliness
mixes the lobes; reflection strength scales Fresnel and removes that energy from
the diffuse term. Skin is never metallic. The hemispherical ambient also reflects
glossily off the specular normal. The studio key and fill are directional disks
sampled uniformly over their solid angle; intensity stays constant as angular
radius changes.

Diffusion follows Burley's normalised profile, `(e^{-r/d} + e^{-r/3d}) / (8πdr)`,
with `d` per channel from the scattering depth, scattering colour and albedo via
Burley's fit. Its sharp centre keeps the shading crisp while its long tail lets
red bleed across the terminator, which is the difference between skin and wax.

Navigation shades with shadow-map visibility, screen-space occlusion, a
pre-integrated diffusion wrap and cheap backlighting. The wrap is a 64×64 table
of the Burley profile integrated around a sphere (Penner's approach), indexed by
`cos θ` and `log2(sphere radius / d)`; the shader estimates the sphere radius from
screen derivatives and reads the table once per channel. Occlusion is coloured,
absorbing blue before red so cavities flush rather than grey. Idle samples
replace those approximations with:

- Full scene triangle visibility for each light, including offscreen occluders.
- One cosine-sampled diffuse bounce, terminated at direct illumination on the
  next surface or the hemispherical environment on a miss.
- A tangent-disk Burley diffusion sample projected onto nearby skin with a ray:
  a quarter of the radii come from the short exponential, three quarters from
  the one three times longer, and a mixture of the three channel PDFs weights
  the result. Red's default diffusion length is longer than green's and blue's.
  Scattering colour controls these relative distances, not a surface colour.
- Beer attenuation through the measured distance to the next outward-facing
  skin surface along a backlight ray, followed by a visibility ray from that
  exit to the light. Local blood and vessel strength increase the extinction;
  a thin shell therefore carries more warm light than a thick one.

This bounded transport is **not** a full volumetric random walk, spectral skin
model, or unlimited-bounce path tracer. Secondary glossy paths are not traced;
the ambient hemisphere stands in for them. Diffusion uses one projection axis
and falls back to local illumination when the projected sample misses or finds
incompatible geometry. Transmission assumes a closed, consistently oriented skin
shell; overlapping shells, open scans and cut surfaces can violate that
assumption. Section planes clip ray intersections, but the display's synthetic
section caps are not part of the ray geometry. There is no anatomical thickness
map or texture requirement. Navigation still uses a constant-cost backlight
approximation; thickness-dependent transmission appears after idle refinement.

The design follows the separation of surface reflection and subsurface transport
described in [GPU Gems 3's skin rendering chapter](https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-14-advanced-techniques-realistic-real-time-skin),
the per-normal blurring and coloured occlusion of Jimenez et al.'s separable
subsurface work, Penner's pre-integrated skin shading, Burley's
[normalised diffusion profile](https://graphics.pixar.com/library/ApproxBSSRDF/)
and surface-projection sampling discussed in
[PBRT's BSSRDF sampling chapter](https://www.pbr-book.org/3ed-2018/Light_Transport_II_Volume_Rendering/Sampling_Subsurface_Reflection_Functions).

## Scheduling, precision and compatibility

The viewport requests another frame only while preparation/refinement is pending.
After 200 ms without a changed image or held mouse button, a worker builds the
BVH. Obsolete worker results are discarded. Mesh uploads, posed or
sculpted replacements, forms and pedestal colour update the trace scene. Camera,
material, lights, section, overlays, output dimensions and AA mode invalidate
image history. The worker never touches OpenGL. Each frame then runs as many
samples as fit in 24 ms (`SAMPLE_BUDGET`), waiting on each, so a fast card
clears the image in a handful of frames and a slow one still answers the mouse.

Primary hits use rasterization; secondary queries traverse a binary BVH in
GLSL 330 (`render/skin_bvh.py`). It is built by the binned surface-area
heuristic, a level of the tree at a time in numpy -- about a quarter of a
second for sixty thousand triangles, four for a million -- and each interior
node keeps both children's boxes, four texels: the ray tests the two at once,
walks into the nearer and keeps the farther on a short stack, so the nearest
hit is usually found in the first leaf and everything behind it is culled.
Shadow rays stop at the first triangle. Triangles are stored as a corner and
two edges with a scaled degeneracy threshold; their normals and furniture
colour sit in a third table read only for a nearest hit. All tables are laid
out a power of two wide, so a texel is found with a shift and a mask, within
the driver's texture-size limit and float32 integer precision. Capacity errors
keep the preview available and appear in the viewport caption. Geometry is
prepared only when idle refinement is enabled.

A GPU inlines every call and sizes a shader's registers for its heaviest path,
which shapes the shader as much as the tree does. Every ray of a sample goes
through a single traversal in a loop of jobs -- the lights seen from the point,
the backlight's exits and whether they see the light, the diffusion sample's
entry and what it sees, the bounce and what it sees, the HDRI's cosine ray and
its reflection -- later jobs reading what earlier ones found. And the mesh
shader is compiled twice (`MESH_FRAGMENT`, `MESH_TRACE_FRAGMENT`) with
`uSkinTrace` a constant in each, so neither the preview nor any other mode
carries the tracer's register load.

Random numbers are stratified: each pixel walks a two-dimensional
low-discrepancy sequence per pair of dimensions -- R2 for the first, Kronecker
lattices on square roots of primes for the rest -- from a random start of its
own. A pixel's first samples cover the key's disc, the diffusion radii and the
bounce hemisphere evenly, and the pixels stay uncorrelated, so what noise is
left is fine grain; sixteen samples look about as clean as the 128 of white
noise the mode used to default to, and the default is now 64.

## The HDRI

With the **Lighting** set to an HDRI, the preview reads the map's irradiance
from its nine spherical-harmonic coefficients (`core/environment.py`), with the
higher bands softened per channel by the diffusion length against the local
curvature -- the harmonic counterpart of the pre-integrated wrap -- and takes
the dominant light's share out where the shadow map, cast from it, says it is
blocked. The reflection is the map's mip level whose texels are as wide as the
lobe, `log2(width * alpha / 2 pi)`.

Traced, the map is a third light. Each sample picks a direction in proportion
to the light arriving along it, from a marginal and a conditional distribution
over a 256-wide copy of the map, and that direction carries the backlight
through thin places. The diffuse is a ratio estimator: the harmonic irradiance,
scaled by the share of the light that two rays -- the importance-sampled one
and a cosine-distributed one -- find unblocked, each weighted by the light it
would have brought. Radiance over density through one direction a sample is a
whole panorama squeezed through a keyhole and is grainy for a long time; the
ratio's noise is only the visibility's. A bounce that misses sees the studio
sky and not the map, which was already counted as a light.

Two RGBA32F histories alternate; a separate float frame supplies the next sample.
Samples are averaged in linear radiance with an online mean. Skin uses an
invertible Reinhard/sRGB display transform before composition with the existing
display-space renderer. Accumulation reverses that transform and presentation
reapplies it, preserving static backgrounds and annotations. FXAA runs after
presentation; SSAA multiplies the requested refinement resolution. No preview
samples enter the accumulated image. There is no denoiser, so a low sample count
shows noise; raising samples reduces it.

Ghost transparency and form-stage video exports use preview shading. Screenshots
capture the displayed result. Existing material modes retain their display-space
lighting. Sessions without skin settings receive defaults; every skin parameter
is persisted by the existing dataclass serializer.

## Where to change it

- `core/skin.py`: parameters, safe ranges, and tone presets.
- `core/body_regions.py`: the regions, their profiles, the bones and bands that
  place a vertex, and the body map the shader samples.
- `core/skin_detail.py`: the relief volume and the pre-integrated diffusion table.
- `render/glsl/skin.glsl`: BRDF, relief, marks and regions, diffusion, ray
  queries and the job loop; `skin_accumulate.frag` and `skin_present.frag`:
  accumulation and display. `render/skin_shader.py` loads them.
- `render/glsl/environment.glsl` and `render/environment.py`: the HDRI's
  lookups, sampling and textures, and the light rig; `core/environment.py`:
  reading maps and preparing them.
- `render/skin_bvh.py`: CPU acceleration layout and texture packing.
- `render/skin_refinement.py`: idle state, worker lifetime, skin tables, history targets.
- `render/mesh_renderer.py`: drawn geometry and uniform integration.
- `ui/panels/shading_panel.py`: artist controls; `ui/viewport.py`: repaint scheduling.

Run `python -m pytest tests/test_skin.py tests/test_skin_gl.py
tests/test_body_regions.py tests/test_environment.py` in the `refview` environment. GL tests verify actual compiled ray queries and image history;
they skip only when the host cannot create an OpenGL context. The supplied
`resources/models/Pose_02.obj` is useful for visual testing of concavities,
ear/finger backlighting, and cast shadows from the raised arm.
