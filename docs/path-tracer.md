# Path tracer

The Render panel's engine is a unidirectional path tracer that runs on the
processor, written in Python and compiled to machine code by numba. It lives
in `src/refview/trace/`, imports neither Qt nor OpenGL, and is loaded the
first time something is rendered, so the viewer starts as fast as it did
without it. These notes describe what it computes, where its limits are,
and where to change it.

## Why our own

Cycles was the obvious candidate and was ruled out on three counts. Its only
Python binding is Blender's `bpy`, which is GPL-3 (this application is MIT),
tied to one Python version (3.13 for current Blender, against our 3.11), and
several hundred megabytes. Standalone Cycles has no Python binding at all.
A tracer of our own, meanwhile, can read the viewer's scene directly -- the
BVH builder, the HDRI's importance tables, the light rig and the skin's
detail volumes are shared with the GPU renderer -- and can port the Human
Skin shader exactly rather than approximately.

## Compilation

`trace/jit.py` is the only module that imports numba. Every kernel is
`njit(cache=True, nogil=True)` with a fast-math set that leaves out *no NaNs*
and *no infinities*: those two let LLVM delete the `x != x` checks that drop
a broken sample. Compiled kernels go to a per-user folder named after the
application version (`%LOCALAPPDATA%\refview\numba-<version>` on Windows,
`~/Library/Caches/refview` on a Mac, `$XDG_CACHE_HOME/refview` elsewhere),
so an upgrade never loads a kernel built from older source. The first render
of a version compiles for 15-20 s behind a progress card; later launches load
the cache in about two seconds.

A one-file PyInstaller build unpacks into a new temporary folder on every
launch, and numba's own cache locators key the cache on the source folder.
`jit.py` therefore installs a locator for frozen builds that ignores the
folder and relies on numba's frozen-build stamp (the executable's size and
time) to tell builds apart. It uses numba internals; if installing it fails,
the cache is turned off and the kernels compile on each launch.

When numba cannot be imported at all, `trace.available()` is false and the
Render panel shows `trace.unavailable_reason()` instead of a Render button.

## Scene

`trace/scene.py` compiles what the viewport shows into three named tuples of
arrays -- `Geometry`, `Shading` and `Params` -- because numba cannot cache a
kernel that takes a class. `Geometry` is every triangle of the model,
pedestal, forms and section cap in one flattened binned-SAH BVH
(`core/bvh.py`, the GPU skin tracer's builder), traversed with a fixed
64-entry stack and a double-precision Möller-Trumbore test on the stored
single-precision corners. Ray origins are offset along the geometric normal
by a few ULPs of the hit position.

The section plane clips hits, and a ray that enters the kept side through
the cut hits the cap instead. Ghosted objects use stochastic opacity: a hit
is accepted with the object's opacity as its probability.

`SceneCache` keeps the BVH, the body-region map and the HDRI's sampling
tables between renders, so a change of light or material does not rebuild
the geometry. `trace_settings_key()` lists exactly what changes the light in
the film. The rendered viewport restarts on those and ignores the safe
frame, output size, colour and denoiser settings.

## Materials

| Shading mode | Model | Pedestal and forms |
|---|---|---|
| Human Skin | the skin port (below) | diffuse, their own colour |
| PBR | principled: base colour, metalness, roughness, specular level and colour | principled, own colour |
| Lambert | principled with no specular lobe | the same |
| Phong, Blinn-Phong, High Quality | dielectric, F0 from the specular level, roughness from the shininess (as the GLSL maps it) | the same |
| Matcap, Normals, Contour | the Render panel's clay | the same |

The principled lobe is GGX, sampled from its visible normals (Heitz 2018),
with Schlick Fresnel and a Lambert base weighted by what the specular leaves.
An F0 of zero has no specular lobe at all.

Colours are sRGB in the panels and linear in the tracer. The analytic modes
will not match the viewport pixel for pixel, because the viewport shades
them in display space. This is intended.

## Lights

The key and fill are the studio rig's (`core/lighting.py`), as discs of the
**Light softness** angle (Human Skin uses its own light radius). The HDRI is
sampled by the same marginal and conditional distributions the GPU skin
tracer builds (`SamplingTables`), evaluated at full resolution. Each vertex
gets one next-event sample per light, combined with the BSDF sample by the
power heuristic. The ambient sky is reached only by bounces.

Light units follow the viewport. Outside Human Skin the key, the fill and
the HDRI are multiplied by π, which is what makes a white Lambert surface
under the key as bright as the GLSL draws it; in Human Skin they are not,
matching `skin.glsl`. The sky is ×1 in every mode.

## Integrator

`trace/integrator.py` traces one path per sample:

- next-event estimation at every non-specular vertex, MIS-weighted;
- separate limits for diffuse, glossy and transmission bounces under an
  overall maximum;
- Russian roulette from the third bounce;
- clamping of direct and indirect contributions (direct is unclamped by
  default);
- **filter glossy**, which roughens glossy lobes after a diffuse bounce to
  keep caustic fireflies down, and a **caustics** switch;
- a finite check on every sample, so a numerical accident drops one sample
  rather than painting a white pixel.

Samples come from Owen-scrambled Sobol sequences (Burley 2020), indexed by
pixel and absolute sample number. Bucket and progressive renders therefore
produce bit-identical images with adaptive sampling off.

Pixel filters (box, Gaussian, Blackman-Harris) are applied by importance
sampling the filter in the primary ray rather than by splatting, so each
pixel is written by one tile and the tiles need no locks. The camera is the
viewport's, with thin-lens depth of field and orthographic projection.
`framed_camera()` (`core/render_frame.py`) narrows the field of view to the
safe frame when the output is letterboxed, so `F12` renders what the frame
shows.

## Human Skin

`trace/skin.py` is a port of `skin.glsl`. Relief, regions, marks (with the
same float32 hash, so the same freckle lands in the same place) and vessels
come from the same volumes the GPU reads. The pixel's ray cone replaces
`fwidth`, so pores fade with distance as they do in the viewport.

- **Specular.** Two GGX lobes, the skin's and the oil's, chosen by one-sample
  MIS against their mixture pdf. This removes the fireflies the narrow oil
  lobe caused under a small key light.
- **Diffuse.** Lambert, weighted by what the scattering leaves.
- **Subsurface.** Christensen-Burley disk projection, with the GPU's
  diffusion lengths. A probe ray along one of three axes (50% normal, 25%
  each tangent) finds up to four skin hits, one of which is kept by
  reservoir sampling. Light is estimated at that exit, and the path continues
  from a white-Lambert vertex there. A random walk was rejected because scans
  are open and non-manifold, where it leaks; the disk costs one probe ray
  instead of tens of steps.
- **Transmission.** A cosine-sampled ray about the inward normal finds the
  outward-facing exit. Beer attenuation along it is raised by blood and by
  the vessels, as in the GLSL.
- **Fuzz.** Evaluated in next-event estimation only, never sampled.

Full detail is traced to the first bounce. Marks are skipped where the pixel
footprint is larger than their cell.

Human Skin's tone curve is Reinhard after the skin exposure, as in the
viewport, so a render matches the refined view it was made from.

## Jobs

`RenderJob` (`trace/job.py`) runs `render_tile` on a thread pool of
`cores - 1` threads by default, below normal priority on Windows. The kernels
release the GIL, so the interface stays responsive.

- **Progressive**: passes of 1, 1, 2, 4, 8, 16, 16, ... samples over 64-pixel
  tiles, with an adaptive check after each pass.
- **Bucket**: tiles of the chosen size in spiral, Hilbert, row or random
  order, each rendered in rounds of 16 samples with an adaptive check
  between rounds.

The adaptive check is Cycles': the film keeps a second sum of the
even-numbered samples, and `|I - 2·I_even| / sqrt(I)`, maxed over 8×8
blocks, estimates the visible error. A block under the noise threshold,
after the minimum samples, is done. A render stops at the sample count, at
convergence or at the time limit, whichever comes first. The cancel flag is
read once per row, so Stop takes effect within a fraction of a second.

`Film` (`trace/film.py`) holds the RGBA sums, the even sums, the sample
counts and, when a denoiser will want them, albedo, normal and depth passes
from the first non-specular hit.

## Colour

`trace/colour.py` develops the film for display: exposure, contrast, a view
transform (Standard, Neutral (Khronos PBR Neutral), Filmic (an ACES fit),
Reinhard, or Auto: Reinhard in Human Skin, Neutral otherwise), sRGB
encoding and gamma, and the viewport's background gradient composited
behind uncovered pixels. With **Transparent background** the gradient is left out, and
PNG and EXR keep the alpha. EXR files are written linear, before the view
transform.

## Denoisers

`trace/denoise.py` puts every denoiser behind one `DenoiseService`, which
runs them all on one thread so each GPU context stays on the thread that
made it. **Auto** tries, in order:

1. **Open Image Denoise on the GPU**, via the `mitsuba-oidn` wheel (CUDA on
   NVIDIA, Metal on Apple Silicon). The filter and its device buffers are
   kept between calls: 4K in about 0.2 s on an RTX 5070 laptop GPU.
2. **NVIDIA OptiX** (`trace/optix/`), through ctypes. `nvoptix.dll` or
   `libnvoptix.so.1` is found beside the graphics driver and its function
   table is queried for ABI 87 (the OptiX 8.0 headers). `abi.py`
   transcribes the structures that ABI uses, and `tests/test_optix_abi.py`
   checks their sizes and offsets. The HDR model runs with albedo and
   camera-space normal guides: 4K in about 0.3 s. Nothing is bundled; a
   machine without an NVIDIA driver simply does not offer it.
3. **Open Image Denoise on the processor.**
4. **The built-in filter** (`denoise_atrous.py`), an edge-avoiding à-trous
   wavelet guided by albedo, normal and depth. It always works and is
   clearly the weakest.

Every backend failure becomes an "unavailable" reason in the panel's
denoiser list rather than an error. The rendered viewport denoises a few
times a second on a GPU and about once a second on the processor.

## DLSS 5 Neural Rendering

After denoising, a render can go through NVIDIA DLSS 5 Neural Rendering
(`trace/neural.py`), an AI model that relights the finished picture. NVIDIA
has no public SDK for it on still images; it runs through the **Neuroframe
Engine** from Merserk's Visual Enhancer. 
The engine is three DLLs that are never committed here:

| File | Whose |
| --- | --- |
| `neuroframe_engine_neural_rendering.dll` | Merserk: the engine (MIT) |
| `neuroframe_caller.dll` | Merserk: its loader shim (MIT) |
| `nvngx_dlssnr.dll` | NVIDIA: the Neural Rendering runtime (DLSS license) |

`engine_dir()` looks for them in the Preferences' **Neural engine** folder
(a Visual Enhancer folder, its `bin`, `bin/runtime`, or the `dlssnr` folder
itself), then in `resources/dlssnr`, which `.gitignore` keeps out of the
repository and the release spec bundles with the rest of `resources/`.

- **What goes in.** Display values, not light: the picture developed through
  the view transform, exposure, gamma and contrast, `(h, w, 3)` float32 in
  [0, 1], which is what the engine takes from an 8-bit image. The alpha is
  kept aside and put back. The engine accepts 64 × 64 up to 7680 × 4320.
- **The call.** `dlss5nr_init(cuda_ordinal, runtime_dir)` once per process,
  then `dlss5nr_process_v6(src, dst, w, h, params)`, host memory in and out.
  `RenderParameters` is the engine's ABI-6 struct (96 bytes; the test pins
  its offsets). A still sets `reset` every time and leaves the mask and the
  temporal controls off. `dlss5nr_release_session` frees the features before
  a picture of another size.
- **Never shut down.** The engine keeps NGX loaded for the life of the
  process: its author found that shutting NGX down or unloading it can wedge
  the driver. Every call runs under a watchdog (45 s a pass); a call that
  hangs, raises, or reports device loss or corruption marks the engine
  unusable until restart instead of calling into broken state again.
- **Threads.** One service thread (`NeuralService`), as with the denoisers:
  NGX is always called from where it started, one picture at a time.
- **Where it runs.** The Render window's **Neural** pass
  (`RenderController.enhance`), made after each denoise when **Enhance the
  render** is on and again 400 ms after a colour or Neural Rendering slider
  stops. The rendered viewport enhances each new denoised picture, one at a
  time, skipping pictures under 64 pixels (as they are while the view turns).
- **Testing.** `tests/test_trace_neural.py` drives the bridge with a Python
  stand-in for the DLL. Set `REFVIEW_NEURAL_ENGINE` to a Visual Enhancer
  folder to run its last test against the real engine.

## Limits

- One CPU engine. The kernels take scalars and named tuples of arrays and
  allocate nothing in their loops, so `numba.cuda` could compile the same
  source later, and the flattened BVH is what an OptiX backend would upload.
  No GPU rendering is done in 2.8.0.
- No textures: the viewer's materials are uniform, so the tracer's are too.
- No motion blur, volumes or spectral rendering. Skin scattering is RGB
  diffusion, as on the GPU.
- Open, non-manifold scans can leak light through their holes in the
  transmission and subsurface lobes, as they can in the viewport.

## Where to change it

- A material parameter: `model_material()` / `furniture_material()` in
  `trace/scene.py`, the row layout in `trace/materials.py`.
- A new setting: `core/path_trace.py` (dataclass, `PATH_TRACE_RANGES`,
  presets), then `trace/scene.py` (`make_params`, and `trace_settings_key` if
  it changes the light), then the Render panel.
- A skin look change: port it from `skin.glsl` into `trace/skin.py` and keep
  `tests/test_trace_skin.py`'s parity checks passing.
- Performance: `tools/benchmark_pathtrace.py` prints compile time, rays per
  second and seconds per sample for a mesh, in both render methods.
