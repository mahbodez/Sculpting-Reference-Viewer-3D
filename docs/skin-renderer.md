# Human Skin renderer

The mode is a practical reference material for untextured meshes. It does not
infer pigmentation, pores, blood flow, or regional tissue properties from shape.
Palettes are editable tone examples rather than measurements of populations.

## Surface

Meshes arrive without a UV layout, so the surface detail is a tileable 3D field
sampled at world position rather than a texture that needs an unwrap. NumPy
builds a 64³ RGBA16F volume once at start-up (`render/skin_detail.py`): pores
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
- Beer attenuation through the distance to the next surface along a backlight
  ray, followed by a visibility ray from that exit to the light.

This bounded transport is **not** a full volumetric random walk, spectral skin
model, or unlimited-bounce path tracer. Secondary glossy paths are not traced;
the ambient hemisphere stands in for them. Diffusion uses one projection axis
and falls back to local illumination when the projected sample misses or finds
incompatible geometry. Transmission assumes a closed, consistently oriented skin
shell; overlapping shells, open scans and cut surfaces can violate that
assumption. Section planes clip ray intersections, but the display's synthetic
section caps are not part of the ray geometry. There is no anatomical thickness
map or texture requirement.

The design follows the separation of surface reflection and subsurface transport
described in [GPU Gems 3's skin rendering chapter](https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-14-advanced-techniques-realistic-real-time-skin),
the per-normal blurring and coloured occlusion of Jimenez et al.'s separable
subsurface work, Penner's pre-integrated skin shading, Burley's
[normalised diffusion profile](https://graphics.pixar.com/library/ApproxBSSRDF/)
and surface-projection sampling discussed in
[PBRT's BSSRDF sampling chapter](https://www.pbr-book.org/3ed-2018/Light_Transport_II_Volume_Rendering/Sampling_Subsurface_Reflection_Functions).

## Scheduling, precision and compatibility

The viewport requests another frame only while preparation/refinement is pending.
After 200 ms without a changed image or held mouse button, a worker prepares a
median-split BVH. Obsolete worker results are discarded. Mesh uploads, posed or
sculpted replacements, forms and pedestal colour update the trace scene. Camera,
material, lights, section, overlays, output dimensions and AA mode invalidate
image history. The worker never touches OpenGL.

Primary hits use rasterization; secondary queries traverse a stackless preorder
BVH in GLSL 330. Two RGBA32F textures hold nodes and triangles, respecting the
driver's texture-size limit and float32 integer precision. Capacity errors keep
the preview available and appear in the viewport caption. Geometry is prepared
only when idle refinement is enabled.

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
- `render/skin_detail.py`: the relief volume and the pre-integrated diffusion table.
- `render/skin_shader.py`: BRDF, relief, diffusion, ray queries, accumulation, display.
- `render/skin_bvh.py`: CPU acceleration layout and texture packing.
- `render/skin_refinement.py`: idle state, worker lifetime, skin tables, history targets.
- `render/mesh_renderer.py`: drawn geometry and uniform integration.
- `ui/panels/shading_panel.py`: artist controls; `ui/viewport.py`: repaint scheduling.

Run `python -m pytest tests/test_skin.py tests/test_skin_gl.py` in the `refview`
environment. GL tests verify actual compiled ray queries and image history;
they skip only when the host cannot create an OpenGL context. The supplied
`resources/models/Pose_02.obj` is useful for visual testing of concavities,
ear/finger backlighting, and cast shadows from the raised arm.
