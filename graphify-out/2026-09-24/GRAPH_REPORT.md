# Graph Report - reference-viewer  (2026-09-24)

## Corpus Check
- 222 files · ~584,862 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 6953 nodes · 16471 edges · 219 communities (214 shown, 5 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 869 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `68f0ac33`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SettingsWindow
- test_preferences.py
- Release
- Viewport
- SceneObject
- trace/scene.py
- MainWindow
- Stroke
- GifWriter
- core/camera.py
- Camera
- autoskin.py
- Cuda
- _wires
- Bone
- environment.yml
- ViewerState
- Skeleton
- build_form
- CameraPanel
- PosePanel
- ShaderProgram
- PoseTool
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- Writer
- core/__init__.py
- viewport.py
- ControlsWindow
- DenoiseService
- ShadingPanel
- FilmRecorder
- convex.py
- test_plane_clusters.py
- WakeLock
- trace_sample
- integrator.py
- Frame
- VideoFormat
- RenderJob
- test_navigation.py
- auto_skin
- ValueSlider
- Rig
- ExportVideoDialog
- trace/skin.py
- landmarks.py
- Agent Graph-First Instructions
- body_regions.py
- settings.py
- test_matcap_preview.py
- test_armature.py
- ArmaturePanel
- RegionSource
- HotkeyMap
- FilmExport
- FormsPanel
- PlanesPanel
- test_skeleton.py
- Progress
- Workspace
- form_group
- test_forms.py
- application.py
- render_frame.py
- ColorButton
- PrimaryForm
- ShadingMode
- test_objects.py
- test_skin.py
- plane_regions
- ObjectTool
- sample
- ArmatureSettings
- test_trace_integrator.py
- load_matcap_pixels
- test_custom_panels.py
- render_controller.py
- core/preferences.py
- core/environment.py
- NavigationController
- ._apply
- ._commit_objects
- test_forms_panel.py
- test_session.py
- skeleton.py
- ViewportRenderPreview
- MatcapPanel
- AnnotatePanel
- overlay.py
- main_window.py
- RenderWindow
- test_elements.py
- Mesh
- Measurement
- ReflowLayout
- state.py
- ball
- FormStore
- clone.py
- skin_detail.py
- Path
- plane_axes
- .mouseReleaseEvent
- rigging.py
- MarkerVisibility
- gif.py
- test_tasks.py
- materials.py
- DockTitle
- test_reflow.py
- Path
- Task
- History
- PathTraceSettings
- test_open_files.py
- sampler.py
- Session
- .process
- ViewportOverlay
- test_hotkeys.py
- Armature
- DenoiserDevice
- test_trace_neural.py
- FakeEngine
- forms.py
- SectionPanel
- ._upload_sculpt
- ._sync_scene
- colour.py
- SurfacePicker
- ExportLook
- obj_loader.py
- preview
- watch_keys
- paths.py
- UpdateChecker
- Film
- Command
- VideoError
- RenderController
- vec.py
- MatcapPreview
- ._picker
- ._carrying_a_copy
- HotkeyStore
- .mouseMoveEvent
- ._turn
- armature.py
- test_body_regions.py
- ContourShadingSettings
- EnvironmentMap
- OidnDenoiser
- .probe
- RenderView
- WholeFaceToggles
- jit.py
- .stage_images
- .paintGL
- tasks.py
- wakelock.py
- solid_count
- neural.py
- Human Skin renderer
- .__init__
- BodySource
- test_plane_film.py
- ._place_armature_node
- _Export
- test_trace_denoise.py
- test_trace_bvh.py
- Path tracer
- TriangleIndex
- ._active_changed
- _Encoder
- picking.py
- matcap_panel.py
- write_exr
- ._start_update_check
- step
- VideoSettings
- SectionAxis
- HotkeyBinder
- ._build
- lzw
- ModelPanel
- ui/preferences.py
- MeasureTool
- ThreadWakeLock
- test_render_panel.py
- release.yml
- role_bones
- ui/hotkeys.py
- .__init__
- .update_enabled
- cube
- test_workspace_layout.py
- ask_for
- _drop_on
- build_bvh
- denoise.py
- ._on_bone_toggled
- bent_plate
- OutputFormat
- _WindowsBackend
- refview/__init__.py
- _MacBackend
- section
- panel
- ._commit_node_drag
- FormRun
- .film
- app
- test_plane_solids.py
- rounded
- test_a_copied_slider_brings_its_caption_inside_itself
- test_a_control_with_nothing_written_on_it_gets_a_caption
- test_a_group_the_mode_does_not_answer_leaves_no_room_behind

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 250 edges
2. `ViewerState` - 203 edges
3. `Viewport` - 167 edges
4. `Skeleton` - 114 edges
5. `Camera` - 113 edges
6. `MainWindow` - 103 edges
7. `RenderSettings` - 95 edges
8. `SceneObject` - 83 edges
9. `Armature` - 81 edges
10. `PrimaryForm` - 79 edges

## Surprising Connections (you probably didn't know these)
- `Orthographic extent derived from FOV and distance` --rationale_for--> `Camera`  [EXTRACTED]
  README.md → src/refview/core/camera.py
- `Pedestal (1.1.0)` --rationale_for--> `PedestalSettings`  [EXTRACTED]
  CHANGELOG.md → src/refview/core/pedestal.py
- `REFVIEW_RESOURCES resource override` --rationale_for--> `available_matcaps()`  [EXTRACTED]
  README.md → src/refview/paths.py
- `Terracotta clay matcap` --shares_data_with--> `available_matcaps()`  [INFERRED]
  resources/matcaps/clay_terracotta.png → src/refview/paths.py
- `The cut interior is flooded flat` --rationale_for--> `SceneRenderer`  [INFERRED]
  README.md → src/refview/render/mesh_renderer.py

## Import Cycles
- 3-file cycle: `src/refview/ui/elements/__init__.py -> src/refview/ui/elements/clone.py -> src/refview/ui/elements/slider.py -> src/refview/ui/elements/__init__.py`
- 4-file cycle: `src/refview/ui/elements/__init__.py -> src/refview/ui/elements/custom.py -> src/refview/ui/elements/clone.py -> src/refview/ui/elements/slider.py -> src/refview/ui/elements/__init__.py`

## Hyperedges (group relationships)
- **The bundled matcap set** — resources_matcaps_clay_terracotta_matcap, resources_matcaps_charcoal_matcap, resources_matcaps_jade_matcap, resources_matcaps_steel_matcap, resources_matcaps_studio_white_matcap, resources_matcaps_wax_skin_matcap, tools_generate_matcaps_matcappreset, tools_generate_matcaps_render [INFERRED 0.85]
- **The four generic undo commands** — src_refview_core_commands_setattributes, src_refview_core_commands_additem, src_refview_core_commands_removeitem, src_refview_core_commands_replaceitems, src_refview_core_history_command, readme_every_edit_is_a_command [EXTRACTED 1.00]
- **Windows binary-compatibility decisions** — readme_pyside6_pinned_below_68, environment_pip_installed_binaries, environment_python_311, github_workflows_release_pyinstaller_build [INFERRED 0.75]

## Communities (219 total, 5 thin omitted)

### Community 0 - "SettingsWindow"
Cohesion: 0.14
Nodes (11): The preferences as they stand. Treat as read-only; use :meth:`set`., QWidget, Fill in the groups. A switch with nothing to put in the caption column is given…, Every command with its keys, each key a box that takes one keystroke. The list…, The one button that is not a preference, and what the window is for., Say what the view is really drawing with, beside what was asked for. A sample…, Put one field back into the store, which applies and saves it., Pull every control back into line with the store. Run when the window is built,… (+3 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.07
Nodes (41): Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, app(), model(), fixture, What the artist prefers: kept apart from the document, and acted upon. Two…, An external drive that is not plugged in is not an empty gallery. (+33 more)

### Community 2 - "Release"
Cohesion: 0.08
Nodes (39): check_for_update(), fetch_latest_release(), is_newer(), _macos_root_certificates(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and… (+31 more)

### Community 3 - "Viewport"
Cohesion: 0.06
Nodes (20): QOpenGLWidget, Free every GL object while the owning context is still current., Arm one tool, disarming the rest. Only one gesture can own the left button, so…, Drop whatever gesture is half-finished, without disarming the tool., One of the renderer's :data:`~refview.render.mesh_renderer.ANTIALIASING_MODES`., Renders the scene and turns mouse gestures into camera and tool actions., Slide the view so a point sits at the centre, keeping the angle., The gesture a key press chooses, if the transform tool is armed to hear it. (+12 more)

### Community 4 - "SceneObject"
Cohesion: 0.07
Nodes (19): ObjectSettings, ObjectStore, ndarray, Snapshot, What a parent's state means for its children, and how the tools scale. Each is…, One model in the scene. Three meshes are kept, as the viewer kept them when…, The centred mesh carried by ``matrix`` -- the mesh itself for the identity., Drop the derived meshes, after the rest mesh has been replaced. (+11 more)

### Community 5 - "trace/scene.py"
Cohesion: 0.08
Nodes (49): IntEnum, filter_table(), ndarray, The inverse cumulative distribution of a separable filter, as offsets in…, empty_geometry(), flatten(), Geometry, NamedTuple (+41 more)

### Community 6 - "MainWindow"
Cohesion: 0.05
Nodes (17): MainWindow, QMainWindow, The document this window edits., Open the window that writes the film of a form's making to a file. Nothing is…, Keep the menu entry agreeing with the panel's own checkbox., Put every panel button and menu entry where the tools now stand. Only one tool…, Swap between the eraser and the drawing mode it was called from., Path-trace the view, at the Render panel's size, into the Render window. (+9 more)

### Community 7 - "Stroke"
Cohesion: 0.05
Nodes (42): AnnotationStore, Enum, ndarray, Freehand annotations painted onto the model surface. A stroke is a polyline of…, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns… (+34 more)

### Community 8 - "GifWriter"
Cohesion: 0.15
Nodes (12): GifWriter, Path, An animated GIF, written a frame at a time. Frames are handed in as ``(height,…, Finish the file. A GIF with no frames in it is still a valid GIF., Give up, leaving no half-written file behind., frames(), ndarray, The GIF written here, read back by something that is not this. A format this… (+4 more)

### Community 9 - "core/camera.py"
Cohesion: 0.05
Nodes (60): Quat, Quat4, Projection, Enum, ndarray, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`. (+52 more)

### Community 10 - "Camera"
Cohesion: 0.02
Nodes (116): Camera, Near/far planes fitted to the scene bounding sphere., The near and far planes this frame: the fitted ones, unless set by hand. A…, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Rays through a batch of pixels, as ``(origins, unit directions)``, ``(N, 3)``…, Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Screen-to-world scale at the focal plane; identical in both modes., Slide the camera parallel to the image plane by a pixel delta. (+108 more)

### Community 11 - "autoskin.py"
Cohesion: 0.10
Nodes (27): _baked_rest(), _conjugate_gradients(), _CotLaplacian, _envelope_weights(), _Graph, _heat_weights(), _joint_distances(), _nearest_weights() (+19 more)

### Community 12 - "Cuda"
Cohesion: 0.05
Nodes (32): FunctionTable, OptixDenoiserGuideLayer, OptixDenoiserLayer, OptixDenoiserOptions, OptixDenoiserParams, OptixDenoiserSizes, OptixDeviceContextOptions, OptixImage2D (+24 more)

### Community 13 - "_wires"
Cohesion: 0.11
Nodes (32): The order the artist put the bones in is what the scrub walks through, which is…, The claim the whole film rests on, asked again with an armature under it: an…, test_a_film_of_clay_on_a_wire_lays_it_down_in_the_order_it_was_listed(), test_the_last_stage_of_a_film_on_a_wire_is_the_form_the_slider_gives(), _bar(), _bed_for(), _holds(), A long ellipsoid: one closed form with an obvious axis to lie along. (+24 more)

### Community 14 - "Bone"
Cohesion: 0.06
Nodes (39): ArmatureNode, Bone, The end that is not ``index``., Every node joined to ``index`` by a bone, each listed once., The graph with ``node`` appended, optionally joined to an existing one., The graph with a node removed and every surviving bone renumbered., Remove a node, bridging the two it stood between. Taking a node out of the…, The graph with a node dropped into the middle of a bone. The bone becomes two,… (+31 more)

### Community 15 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 16 - "ViewerState"
Cohesion: 0.04
Nodes (38): BakeEdit, Command, QObject, Write ``obj``'s turn and scale into its mesh, leaving it standing as it is.…, A parenting policy changed: what is shown and how solid may have too., Dressing an object in a skin made for a skeleton, or taking it off. One step…, Turn every object the same way; see :meth:`set_object_orientation`. For files…, Turn one object, bringing the marks made on it along. Measurements,… (+30 more)

### Community 17 - "Skeleton"
Cohesion: 0.06
Nodes (31): Joint, _matrix16(), _pose_matrices(), ndarray, Whether the pose differs from the rest at all., A copy with the rest translation replaced and the frame kept., A tree -- or a forest -- of joints and the pose they stand in., Every joint, parents before children. A file may list a child before its… (+23 more)

### Community 18 - "build_form"
Cohesion: 0.12
Nodes (25): merged(), Several flat meshes as one, or ``None`` when there is nothing to draw., build_form(), built_count(), form_mesh(), landmark_signature(), The solids of every stage the landmarks can build, coarsest first. A stage…, How many stages actually have clay in them, counting from the first. (+17 more)

### Community 19 - "CameraPanel"
Cohesion: 0.10
Nodes (9): CameraPanel, QListWidgetItem, Take the planes in hand where the fit left them, or hand them back., Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions. (+1 more)

### Community 20 - "PosePanel"
Cohesion: 0.05
Nodes (25): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, PosePanel, QTreeWidgetItem, QWidget, The skeleton the panel is about: the selected row's, else the last., Highlight a row, in the tree and in the view. (+17 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.14
Nodes (7): ndarray, RuntimeError, Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "PoseTool"
Cohesion: 0.07
Nodes (44): JointRef, How skeletons are drawn, and how the pose tool behaves., SkeletonSettings, PoseTool, _project_many(), ndarray, The nearest unlocked joint of a visible skeleton under the cursor., The bone under the cursor, named by the joint at its far end. Taking hold of a… (+36 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.08
Nodes (21): _names(), The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as…, Or there would be no way to turn one back on., A limb is four bones, and deciding not to block the arms in is one decision.…, It is rebuilt on every change, and ticking one row of a selected limb would be… (+13 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.12
Nodes (8): MeasurePanel, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn.

### Community 25 - "BookmarkStore"
Cohesion: 0.06
Nodes (17): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around. (+9 more)

### Community 26 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 27 - "core/__init__.py"
Cohesion: 0.03
Nodes (79): High Quality shading mode (1.1.0), core never imports Qt, The cut interior is flooded flat, High Quality without ray tracing, Three-layer separation: core, render, ui, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets, The pedestal is ordinary geometry so it catches the shadow (+71 more)

### Community 28 - "viewport.py"
Cohesion: 0.02
Nodes (154): Film, film_key(), planes_for(), The stages a form passes through on its way from a block to a figure. The…, The stage at ``index``, clamped to what has actually been recorded., What a film depends on. Everything that changes the shape of any stage, and…, How many solids each stage of a film is made of. Every count from the coarsest…, The detail setting that asks for ``solids``, or ``None`` if none does. The… (+146 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "DenoiseService"
Cohesion: 0.16
Nodes (11): DenoiseSettings, DenoiseRequest, DenoiserInfo, DenoiseService, Future, The denoiser a setting stands for, here; probes if nothing has yet., Denoise off the calling thread; the future holds ``(image, info, note)``., The one thread every denoise runs on, and the denoisers it has started. (+3 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.11
Nodes (9): Chooses the shading model and edits its light and surface parameters., Pick an HDRI from disk and light with it., List the bundled HDRIs, and the one in use if it is from elsewhere., Put the light's numbers back in line with the settings, after a drag or an undo., Freeze the slices the way the camera faces now. The view direction is the one…, Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel, test_contour_controls_follow_the_mode_and_pin_the_view() (+1 more)

### Community 32 - "FilmRecorder"
Cohesion: 0.11
Nodes (15): QThread, FilmRecorder, Film, QObject, The film being recorded, or the last one finished., Whether a film is being made right now., The film already held for ``key``, if there is one., Stop any recording in flight and forget what it was making. The thread is asked… (+7 more)

### Community 33 - "convex.py"
Cohesion: 0.12
Nodes (24): convex_hull(), DegenerateHullError, flat_mesh(), _outward(), _patch_samples(), ndarray, ValueError, Convex solids from points: the hull, a cut through it, and its mesh. A primary… (+16 more)

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.17
Nodes (20): parametrize, Fitting planes to a model's surface rather than only to its normals. What…, Merging back from patches is a hierarchy, so the cuts of it nest. This is what…, Every plane of a level as a hashable whole: direction, place and offset., Nothing is seeded at random, so a session reopens looking the same., The renderer reads an empty set as "leave the normals alone"., The shader has to put a fragment into that frame before it can look up which…, The planes moved out of a uniform array and into a texture so that the count… (+12 more)

### Community 35 - "WakeLock"
Cohesion: 0.17
Nodes (13): Holds sleep off while the window that owns it is the one in front. The class…, WakeLock, Broken, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do., A platform that refuses, the way an old or locked-down one might., The viewer must open and close normally on a machine that says no., Recorder (+5 more)

### Community 36 - "trace_sample"
Cohesion: 0.10
Nodes (40): _accept(), any_rays(), cap_normal(), cast_rays(), clipped(), intersect(), new_stacks(), occluded() (+32 more)

### Community 37 - "integrator.py"
Cohesion: 0.11
Nodes (40): The path tracer's integrator: what one sample of one pixel sees. A path leaves…, disc_hit(), disc_sample(), env_background(), _env_frame(), env_pdf(), env_radiance(), env_sample() (+32 more)

### Community 38 - "Frame"
Cohesion: 0.04
Nodes (39): carried(), _pull_frame(), _push_frame(), Nothing: each row inside the copy is linked on its own., Read a drag's payload back, or ``None`` if it is not one of ours., CustomPanel, _detach(), QFormLayout (+31 more)

### Community 39 - "VideoFormat"
Cohesion: 0.08
Nodes (16): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+8 more)

### Community 40 - "RenderJob"
Cohesion: 0.07
Nodes (20): How the picture is filled in., RenderMethod, adaptive_error(), Mark blocks whose noise has fallen below ``threshold`` as done; returns pixels…, _hilbert_index(), JobState, _lower_priority(), pass_schedule() (+12 more)

### Community 41 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 42 - "auto_skin"
Cohesion: 0.12
Nodes (37): auto_skin(), AutoSkin, AutoSkinError, bone_segments(), ValueError, Skin ``mesh`` to ``skeleton``, both given in the same coordinates. The skeleton…, ``names`` with any repeat numbered, since the skin matches joints by name., Every bone as ``(start, end)`` points, and which joint each belongs to. A joint… (+29 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (11): _pull_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end., Set the value the way a hand on the control would., The value the track stands at ``x`` pixels across. (+3 more)

### Community 44 - "Rig"
Cohesion: 0.05
Nodes (52): Shift-snapped orbiting (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, STL and glTF import (1.1.0) (+44 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.09
Nodes (14): even(), ExportVideoDialog, Film, Path, QDialog, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Open the file and begin. Any failure here is reported, not raised. (+6 more)

### Community 46 - "trace/skin.py"
Cohesion: 0.14
Nodes (34): body_fetch(), bump(), burley_pdf(), diffusion_lengths(), dome(), _fract32(), hash4(), marks() (+26 more)

### Community 47 - "landmarks.py"
Cohesion: 0.14
Nodes (20): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _humanoid_landmarks(), _kept_laying(), _mid() (+12 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "body_regions.py"
Cohesion: 0.24
Nodes (13): band_weights(), bone_weights(), ndarray, Where on the body a point of the skin is, so that the skin can be marked as…, Distance from each point to each bone, ``(points, bones)``., Region weights of each point from the bones nearest it, ``(points, regions)``.…, Region weights of each point from its height between ``bottom`` and ``top``., The region weights of every vertex of one part of the scene. (+5 more)

### Community 50 - "settings.py"
Cohesion: 0.02
Nodes (134): BodyRegionSettings, Where the regions come from, and what each does to the skin effects., build_grid(), GridLines, GridSettings, nice_step(), Reference grids on the three axis planes, fading with distance. A grid gives…, Segments, with their colours and widths, ready for the stroke buffer. (+126 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.10
Nodes (33): QPoint, _drag(), _listed(), _matcap_file(), parametrize, The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc. (+25 more)

### Community 52 - "test_armature.py"
Cohesion: 0.12
Nodes (36): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other., The femoral head is in from the ASIS, below it and behind it, by shares of the…, A wire in two halves is not an armature anybody could bend. (+28 more)

### Community 53 - "ArmaturePanel"
Cohesion: 0.04
Nodes (39): QTreeWidget, ArmaturePanel, QPushButton, QTreeWidgetItem, QWidget, Run a row's edit once Qt has finished delivering the current signal. Committing…, Arms the armature tool, lists its nodes and runs the guided presets., Add a group below the list rather than to the panel root. (+31 more)

### Community 54 - "RegionSource"
Cohesion: 0.14
Nodes (9): _default_profiles(), Enum, str, How much of each skin effect one region gets, relative to its slider., Starting values for skin effects across a generic body., One region's multiplier for ``effect`` after another, in :data:`REGIONS` order., Where the region map comes from., RegionProfile (+1 more)

### Community 55 - "HotkeyMap"
Cohesion: 0.08
Nodes (18): Command, HotkeyMap, Any, Which keys do what, as the artist has decided rather than as it ships. A hotkey…, Whether the artist has moved this command off what it ships with., Which command has these keys, if any., Every command with keys on it, declared or not, as id -> keys., Put ``keys`` on a command, taking them off whatever had them. Returns the id of… (+10 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (10): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in…, Offer the encoder the last stage before the first is written. Only the built-in… (+2 more)

### Community 57 - "FormsPanel"
Cohesion: 0.05
Nodes (31): FormsPanel, QTreeWidgetItem, Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Begin a run against a fresh form: a preset's walk, or a freeform's., Take up the selected freeform again, so more landmarks can go on it. The same…, The freeform the highlighted row belongs to, when no run is on. (+23 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.18
Nodes (6): PlanesPanel, Put the design matrix back the way it reads a figure., Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Breaks the form into planes, in the shading or in the geometry itself., Re-read the armatures and what the chosen one is laying down. Called whenever…

### Community 59 - "test_skeleton.py"
Cohesion: 0.08
Nodes (42): detail_joints(), Which joints are detail, and which kind, read off their names. A toe past the…, The joint list with the detail taken out, and how much of each kind went. What…, The joint list with these roles written in, and every other role cleared., simplified(), with_roles(), make_joint(), A joint at a position in its parent's frame, with no turn of its own. (+34 more)

### Community 60 - "Progress"
Cohesion: 0.08
Nodes (21): Exception, CancelledError, Progress, What a long piece of work says about itself while it runs, and how it is…, Ask the work to stop at its next report., How far along, 0 to 1, or ``None`` when the work has not said., Whether the work has said how much there is to do., A window onto part of a parent's range; see :meth:`Progress.slice`. (+13 more)

### Community 61 - "Workspace"
Cohesion: 0.05
Nodes (30): QDockWidget, QTabBar, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top., forget(), Drop every id under a prefix; for a panel that has been thrown away., _number_in(), QMainWindow (+22 more)

### Community 62 - "form_group"
Cohesion: 0.08
Nodes (18): QComboBox, QSpinBox, _push_combo(), QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row(), _format_bytes() (+10 more)

### Community 63 - "test_forms.py"
Cohesion: 0.05
Nodes (73): One convex piece of a form: its hull vertices and outward-wound faces., The hull of the points with its faces bowed out; see :func:`rounded_hull`., The longest side of the box the solid sits in., Whether a point lies inside, or within ``slack`` of the surface., Solid, _across(), blend_rings(), build_head() (+65 more)

### Community 64 - "application.py"
Cohesion: 0.07
Nodes (28): ArgumentParser, QSplashScreen, Application, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font(), main() (+20 more)

### Community 65 - "render_frame.py"
Cohesion: 0.11
Nodes (28): Rect, OutputSettings, How large the picture is and how it is saved., clamp_size(), frame_rect(), framed_camera(), memory_estimate(), output_size() (+20 more)

### Community 66 - "ColorButton"
Cohesion: 0.05
Nodes (23): CloneGesture, Link, _pull_point(), _pull_swatch(), _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it… (+15 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.06
Nodes (43): FormLandmarkRef, PlacedLandmark, One anatomical point the artist put on the model during a guided run., FormSettings, PrimaryForm, ndarray, Point3, One form in the document: which recipe, and where its landmarks are. The solids… (+35 more)

### Community 68 - "ShadingMode"
Cohesion: 0.08
Nodes (23): ClaySettings, ColorSettings, FilmSettings, LensSettings, LightPathSettings, mode_note(), PathTracePreset, PerformanceSettings (+15 more)

### Community 69 - "test_objects.py"
Cohesion: 0.09
Nodes (41): Write a mesh out; only OBJ is written, whatever the suffix asked for., save_mesh(), loose_parts(), The triangles of ``mesh`` named by index, with only the vertices they use., The triangles of ``mesh`` gathered into the pieces that touch, largest first.…, submesh(), Path, Where an object stands relative to its parent: an affine placement. Held as the… (+33 more)

### Community 70 - "test_skin.py"
Cohesion: 0.05
Nodes (42): build_scene(), ndarray, Bounding-volume hierarchy tables for the OpenGL 3.3 skin tracer. The tree…, How wide the tables are laid out under a driver's texture limit: a power of two., Pack a linear texel array within the driver's actual 2D texture limit. Always…, Build on a worker from the immutable meshes currently drawn by the renderer., table_width(), texture_table() (+34 more)

### Community 71 - "plane_regions"
Cohesion: 0.08
Nodes (47): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), dumbbell(), flatness(), parametrize, The invariant an artist actually sees, on the finished stand-in: clay is added… (+39 more)

### Community 72 - "ObjectTool"
Cohesion: 0.12
Nodes (14): _axis_param(), Gizmo, _Grip, ObjectTool, ndarray, The three directions the arms run along, in world space. A move and a turn are…, Where the gizmo for an object at ``world`` falls on screen, or ``None`` if…, Which handle a screen point is over: ``"centre"``, ``"x"``, ``"y"``, ``"z"`` or… (+6 more)

### Community 73 - "sample"
Cohesion: 0.18
Nodes (11): grade(), ndarray, QImage, Draw the matcap onto a sphere of ``size`` pixels, graded. Returns ``(size,…, The matcap as a picture, at its own resolution. Square and opaque, with the…, The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…, Apply the matcap grading to float RGB in 0-1, as the shader does. A…, sample() (+3 more)

### Community 74 - "ArmatureSettings"
Cohesion: 0.06
Nodes (50): ArmatureSettings, How the armature is drawn, and how new nodes are placed., The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now., Pass over the landmark being asked for; the figure loses what it fed., Un-skip or un-place the landmark before this one, and ask again. Returns the… (+42 more)

### Community 75 - "test_trace_integrator.py"
Cohesion: 0.15
Nodes (24): _inputs(), Whole renders: energy, determinism, the two methods, stopping, adaptive…, Under light of radiance one from everywhere, a convex matte ball shows its…, _render(), test_a_cancel_stops_the_render_promptly(), test_adaptive_sampling_spends_less_on_the_quiet_background(), test_bucket_and_progressive_make_the_same_picture(), test_no_sample_is_ever_nan() (+16 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.15
Nodes (23): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+15 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.10
Nodes (12): app(), custom(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error., A group is not a row, so it goes ahead of the group it was dropped on., One offscreen Qt application for the run; see test_film_recorder., A check box already carries its words; a caption beside it repeats them. (+4 more)

### Community 78 - "render_controller.py"
Cohesion: 0.09
Nodes (22): exposure_scale(), Film, ndarray, The picture and its guides, as a film holds them., request_from_film(), available(), The CPU path tracer: numpy and numba, never Qt and never OpenGL. Importing this…, Whether the path tracer can run here (numba loads). (+14 more)

### Community 79 - "core/preferences.py"
Cohesion: 0.11
Nodes (20): _as_kind_of(), _clamp(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any (+12 more)

### Community 80 - "core/environment.py"
Cohesion: 0.07
Nodes (60): direction_to_uv(), dominant_light(), downsized(), EnvironmentLoadError, evaluate_sh(), _exr_rgb(), _halve(), irradiance_sh() (+52 more)

### Community 81 - "NavigationController"
Cohesion: 0.08
Nodes (18): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Degrees of yaw per pixel, signed by whether the drag is inverted. (+10 more)

### Community 82 - "._apply"
Cohesion: 0.21
Nodes (6): Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Slot that writes one field of the contour shading settings., Slot that writes one field of the grid settings.

### Community 83 - "._commit_objects"
Cohesion: 0.06
Nodes (23): ObjectsEdit, ndarray, Snapshot, A copy of ``obj``'s mesh on top of it, made active, as one undo step., Scale ``objects`` so each is the size of the active one, as one undo step. The…, The largest of ``obj``'s three extents as it stands in the world., The 4x4 that takes a point on the old rest mesh onto the new one. A point sits…, Carry the measurements, annotations, armature and forms through ``carry``. (+15 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.11
Nodes (30): app(), _click(), panel(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The… (+22 more)

### Community 85 - "test_session.py"
Cohesion: 0.10
Nodes (17): Named camera positions the artist can jump between while sculpting., Named point-to-point measurements and their presentation options., Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., A step of the slider is worth a fixed share more planes, not a fixed number of…, The ceiling went from 64 planes to 256 without moving the slider under anyone:…, The panel edits the settings; the fit has to be told what they are., Both modes answer in degrees of turn, so the panel can just ask. (+9 more)

### Community 86 - "skeleton.py"
Cohesion: 0.09
Nodes (13): BoneLabels, Buried, Enum, str, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…, Enum, A hierarchy of joints, the pose it is in, and the skin that moves with it.… (+5 more)

### Community 87 - "ViewportRenderPreview"
Cohesion: 0.12
Nodes (11): quantize_region(), Display values to 8-bit RGBA, rounding to nearest., ndarray, QImage, QObject, Hold the preview still while a render runs, and pick it up again after., The picture to draw over a ``width`` by ``height`` view, or ``None`` for the GL…, The best picture there is: enhanced, denoised, or as it is. (+3 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.13
Nodes (11): MatcapPanel, Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, Rebuild the thumbnail list: the built-in, the ones added, then the folder., Put the matcap on the model into the gallery, if it came from somewhere else.…, The disc was dragged: show the renderer and the numbers what it did., A different matcap: the disc draws whichever one is on the model., Put the numbers back in line with the settings, and redraw the disc. Separate… (+3 more)

### Community 89 - "AnnotatePanel"
Cohesion: 0.21
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 90 - "overlay.py"
Cohesion: 0.11
Nodes (19): QPointF, Annotations drawn as widened geometry, Measurements drawn in screen space with QPainter, DepthDrag, draw_rail(), draw_text(), Shared marker appearance, visibility, and constrained depth gestures., A grid across the depth axis, at the depth the point has reached. Returns… (+11 more)

### Community 91 - "main_window.py"
Cohesion: 0.03
Nodes (74): QScrollArea, Every document edit is a command, AddItem, Command, The handful of undoable edits the whole application is built from.…, Append an item to a document list., Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the… (+66 more)

### Community 92 - "RenderWindow"
Cohesion: 0.10
Nodes (18): enhance_key(), What an enhanced picture depends on besides the render: colour and engine…, A render, finished or under way, and everything needed to show and save it., RenderResult, _duration(), ndarray, Path, QImage (+10 more)

### Community 93 - "test_elements.py"
Cohesion: 0.09
Nodes (17): Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., Run the refresh the shared timer would have run., ``self._mode`` is ``mode``; the group called Mode settles for a number., test_a_copied_group_still_drives_the_originals() (+9 more)

### Community 94 - "Mesh"
Cohesion: 0.03
Nodes (73): auto_smooth(), compute_vertex_normals(), _corner_groups(), _face_cross(), _gathered(), _group_normals(), One entry point for every mesh format the viewer reads. Callers ask for a path…, Mesh (+65 more)

### Community 95 - "Measurement"
Cohesion: 0.10
Nodes (14): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+6 more)

### Community 96 - "ReflowLayout"
Cohesion: 0.08
Nodes (19): Orientations, QLayout, QLayoutItem, _height_of(), QRect, QSize, QWidget, How many columns this layout would break into at ``width``. (+11 more)

### Community 97 - "state.py"
Cohesion: 0.06
Nodes (45): concatenated(), Several meshes as one, in the coordinates they already stand in. The units are…, OrientationSettings, Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world. (+37 more)

### Community 98 - "ball"
Cohesion: 0.13
Nodes (24): app(), coarse_lattice(), fixture, MonkeyPatch, Recording a film on a thread, without taking the process down with it. The rest…, Which is what the panel puts its controls to sleep by, so it has to be true…, Shutdown must not care whether the thread beat it to the exit. A recording that…, The guard that decides whether to scrub an existing film or record a new one.… (+16 more)

### Community 99 - "FormStore"
Cohesion: 0.15
Nodes (5): FormStore, An ordered, named collection of forms, like the other stores., The live list; the undo commands operate on it directly., A name for a new form of this recipe, numbered past any it already has. A form…, test_a_form_store_names_forms_past_the_ones_it_has()

### Community 100 - "clone.py"
Cohesion: 0.04
Nodes (91): QAbstractButton, QLineEdit, QSlider, _begin(), can_clone(), clone(), _clone_button(), _clone_check() (+83 more)

### Community 101 - "skin_detail.py"
Cohesion: 0.09
Nodes (30): burley_marginal(), burley_profile(), cellular(), diffusion_lut(), _fade(), fbm(), ndarray, Procedural skin micro-relief and the pre-integrated diffusion table. Reference… (+22 more)

### Community 102 - "Path"
Cohesion: 0.11
Nodes (14): A flat-shaded mesh, every triangle with its own three corners. Corners are not…, looks_humanoid(), Whether a guessed mapping is enough of a figure to be worth offering., Path, Pick up whatever was last being worked on, if that was asked for. A session…, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window. In the… (+6 more)

### Community 103 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.08
Nodes (11): Record the finished drag as a single undo step., Record the turn as one undo step., Alt forces the camera gesture, whichever tool is armed., Record the finished drag as one step, or read a press as a selection., Make the object under the cursor the active one., Which skeleton an edit lands in: the selected one, else the last., Add a joint where the click landed, under the selected joint., Record the finished pull as one step, or read a press as a selection. (+3 more)

### Community 105 - "rigging.py"
Cohesion: 0.11
Nodes (23): What to call the joint filling a humanoid slot: ``"knee.L"`` is ``"Knee L"``., role_name(), armature_from_skeleton(), armature_root(), build_humanoid_skeleton(), humanoid_positions(), ndarray, Where skeletons come from: an armature, a preset, or the names in a file. Three… (+15 more)

### Community 106 - "MarkerVisibility"
Cohesion: 0.18
Nodes (5): MarkerVisibility, Cache surface occlusion by view and position for every kind of marker. The…, Whether the last pass is recent enough to be read instead of repeated., Mark these points as standing in front of the surface, untested. For frames…, Answer for a batch of points at once, ahead of being asked one by one. Every…

### Community 107 - "gif.py"
Cohesion: 0.14
Nodes (15): _bayer(), _blocks(), _indices(), _lookup(), palette_of(), ndarray, Writing an animated GIF with nothing but numpy and the standard library. The…, For every colour on a 32x32x32 grid, the nearest entry in ``palette``. Thirty-… (+7 more)

### Community 108 - "test_tasks.py"
Cohesion: 0.17
Nodes (16): app(), fixture, Work run off the window, and the cards that show it running., Turn the event loop until ``until()`` says so, or give up., runner(), _spin(), test_a_result_arriving_after_the_cross_is_thrown_away(), test_a_task_called_off_while_waiting_never_starts() (+8 more)

### Community 109 - "materials.py"
Cohesion: 0.16
Nodes (26): ggx_d(), ggx_eval(), ggx_sample(), material_alpha(), principled_eval(), _principled_parts(), principled_sample(), device (+18 more)

### Community 110 - "DockTitle"
Cohesion: 0.06
Nodes (24): QToolButton, DockTitle, make_switch(), QCheckBox, QSize, QWidget, One dock per panel, with a bar of its own across the top. Every panel is its…, Put a show/hide switch at the left of the bar and return it. (+16 more)

### Community 111 - "test_reflow.py"
Cohesion: 0.14
Nodes (20): app(), _block(), _panel(), fixture, QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., One offscreen Qt application for the run; see test_film_recorder. (+12 more)

### Community 112 - "Path"
Cohesion: 0.07
Nodes (24): setter, Path, Write ``rig`` -- everything but the vertices, which the model has., save_rig(), Path, Take the display unit from the file when the format declares one. Only glTF…, Set the active matcap, or fall back to the built-in one., Write the document, and whatever the window says its layout is. The layout… (+16 more)

### Community 113 - "Task"
Cohesion: 0.06
Nodes (24): _outcome(), ProgressCard, Any, BaseException, QObject, QPainter, QWidget, T (+16 more)

### Community 114 - "History"
Cohesion: 0.17
Nodes (14): History, A bounded undo/redo stack., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch(), test_commands_carry_their_channel_and_name() (+6 more)

### Community 115 - "PathTraceSettings"
Cohesion: 0.08
Nodes (28): _copy(), PathTraceSettings, Keep loaded settings finite and inside what the panel and the tracer allow., A deep copy of nested dataclasses, cheap enough for every render., _resolve(), What of the settings a rendered picture shows, as a key. The viewport preview…, trace_settings_key(), Version 4 files predate the armature; they open with an empty one. (+20 more)

### Community 116 - "test_open_files.py"
Cohesion: 0.18
Nodes (9): app(), opened(), fixture, Files arriving from outside: the command line, a drop, or the desktop's "Open…, One offscreen Qt application for the run; see test_film_recorder., What the window was asked to open, by kind, without loading anything., Finder sends the launching file as an event, which can land before the window., test_a_file_the_desktop_hands_over_early_waits_for_the_window() (+1 more)

### Community 117 - "sampler.py"
Cohesion: 0.16
Nodes (24): bounce_set(), _direction_numbers(), hash32(), hash_combine(), hash_float(), _laine_karras(), nested_uniform_scramble(), pixel_seed() (+16 more)

### Community 118 - "Session"
Cohesion: 0.10
Nodes (21): _coerce(), decode(), encode(), Any, T, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``. (+13 more)

### Community 119 - ".process"
Cohesion: 0.13
Nodes (15): check_size(), NeuralError, NeuralPoisonedError, ndarray, RuntimeError, Raise if the engine cannot take a ``width`` by ``height`` picture., Neural Rendering could not be done, and says why., The engine hung or faulted; it is not called again until the application… (+7 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.07
Nodes (35): ArmatureTool, Turns clicks into nodes, and drags into moved or resized ones. The tool stays…, Drop the hover preview and the chain, leaving any guided run alone. Escape…, OverlayParts, project_visible(), Handle, ndarray, QColor (+27 more)

### Community 121 - "test_hotkeys.py"
Cohesion: 0.10
Nodes (24): QKeySequence, app(), _click(), _map(), fixture, Hotkeys: the map, the store, the binder, and the gesture that assigns one., One offscreen Qt application for the run; see test_film_recorder., End to end: the filter is on the panel's buttons and the window hears it. (+16 more)

### Community 122 - "Armature"
Cohesion: 0.05
Nodes (25): Armature, ArmatureStore, ndarray, Point3, A graph of nodes and the bones joining them. When it came from a preset the…, Every node position as ``(n, 3)``., The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves. (+17 more)

### Community 123 - "DenoiserDevice"
Cohesion: 0.11
Nodes (14): BucketOrder, DenoiserBackend, DenoiserDevice, DenoiserQuality, PixelFilter, Enum, str, What :attr:`AUTO` stands for: the skin's own curve in Human Skin. (+6 more)

### Community 124 - "test_trace_neural.py"
Cohesion: 0.18
Nodes (16): NeuralService, The one thread Neural Rendering runs on, and the engine it has loaded. One…, Look for the engine in ``folder`` (from the preferences), or only where it…, set_engine_dir(), test_the_controller_enhances_after_denoising(), test_the_rendered_viewport_shows_the_enhanced_picture(), _install(), _no_engine_folder() (+8 more)

### Community 125 - "FakeEngine"
Cohesion: 0.16
Nodes (11): NeuralSettings, NVIDIA DLSS 5 Neural Rendering, run on the developed picture after denoising.…, NeuralBridge, The engine, loaded once, and the calls into it. ``library`` stands in for the…, FakeEngine, parametrize, The engine's exported functions, in Python: inverts the picture, or misbehaves., test_a_crash_or_a_hang_stops_the_engine_for_good() (+3 more)

### Community 126 - "forms.py"
Cohesion: 0.05
Nodes (58): build_freeform(), _centre(), form_landmark_title(), form_spec(), FormFill, FormPreset, FormStage, freeform_landmark() (+50 more)

### Community 127 - "SectionPanel"
Cohesion: 0.18
Nodes (7): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 128 - "._upload_sculpt"
Cohesion: 0.12
Nodes (7): The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, Cut the stand-in on a thread; see :meth:`_upload_sculpt`., Show the recording as a task, its bar the stages landed so far., The cross on the recording's card: the film is dropped, the switch too., A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on.

### Community 129 - "._sync_scene"
Cohesion: 0.09
Nodes (11): Cut the mesh with each section plane and expand the result to strokes., The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, A skeleton changed: redraw it, and let the skin's body map follow its bones., What the renderer draws: each object as it stands, AutoSmoothed if asked., ``mesh`` shaded by the object's smoothing groups, found once and kept. The…, The whole scene as one mesh, as the planes and the skin tracer read it. The…, Tell the renderer what the skin's body map is made from now., Hand the renderer a re-posed model and nothing else. For the frames of a pose… (+3 more)

### Community 130 - "colour.py"
Cohesion: 0.15
Nodes (25): _aces(), develop(), develop_image(), develop_region(), _encode(), linear_to_display(), _neutral(), device (+17 more)

### Community 131 - "SurfacePicker"
Cohesion: 0.05
Nodes (34): BoneRef, LandmarkRef, AnnotateMode, AnnotationSettings, str, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a… (+26 more)

### Community 132 - "ExportLook"
Cohesion: 0.10
Nodes (13): ExportLook, What the frames are to look like, as against what they are of. Laid over the…, Which of the things drawn over the model belong in the frames., ``base`` with this export's choices laid over it., The line burned into the corner of the frame for ``stage``. Counted off the…, FakeViewport, QImage, Pump the event loop until ``done()`` or the clock runs out. (+5 more)

### Community 133 - "obj_loader.py"
Cohesion: 0.07
Nodes (47): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast() (+39 more)

### Community 134 - "preview"
Cohesion: 0.29
Nodes (7): app(), gallery_settings(), preview(), fixture, The gallery's list on a settings file of the tests' own, empty to begin with., One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "watch_keys"
Cohesion: 0.16
Nodes (13): can_take_key(), is_hotkey_click(), KeyGesture, QObject, QWidget, The gesture that puts a key on a control: Ctrl/Cmd, Alt and a click. It sits…, Whether a mouse press is the assignment gesture rather than a click., Whether a widget is the kind a key can sensibly be put on. A button or a switch… (+5 more)

### Community 136 - "paths.py"
Cohesion: 0.18
Nodes (19): available_environments(), available_matcaps(), _bundled_root(), cache_dir(), environment_dir(), image_path(), matcap_dir(), model_dir() (+11 more)

### Community 137 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 138 - "Film"
Cohesion: 0.24
Nodes (5): Film, ndarray, Linear radiance and coverage per pixel, ``(h, w, 4)`` float32, premultiplied., World-space normals of the first surface, unit length where there is one., Distance of the first surface along the view, 0 where there is none.

### Community 139 - "Command"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 140 - "VideoError"
Cohesion: 0.18
Nodes (12): _encode_arguments(), _encoders(), _FFmpegWriter, _no_window(), RuntimeError, An export that could not be written, said in words for the artist., Which encoders this ffmpeg was built with. Asked once, because a build without…, Keep a console window from flashing up on Windows for each ffmpeg call. (+4 more)

### Community 141 - "RenderController"
Cohesion: 0.14
Nodes (8): BaseException, QObject, Starts, watches and finishes renders for the Render panel and window., Render ``inputs`` (a :class:`~refview.trace.scene.TraceInputs`), stopping any…, Denoise a render's film now, with the settings as they are., Run DLSS 5 Neural Rendering on a render as it is developed now., Enhance again once the colour or Neural Rendering sliders stop moving., RenderController

### Community 142 - "vec.py"
Cohesion: 0.16
Nodes (21): ndarray, The parameter row and the region multipliers for…, skin_parameters(), add(), clamp(), length(), linear3(), madd() (+13 more)

### Community 143 - "MatcapPreview"
Cohesion: 0.07
Nodes (21): QMenu, _clone_preview(), MatcapPreview, _pull_preview(), _push_preview(), Path, QSize, QWidget (+13 more)

### Community 144 - "._picker"
Cohesion: 0.10
Nodes (12): ndarray, Rub out the stroke points under the eraser, live., Take hold of a node, to move it, resize it, or just to select it. This works…, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Where the active object's gizmo falls on screen, or ``None``. (+4 more)

### Community 145 - "._carrying_a_copy"
Cohesion: 0.11
Nodes (10): opens_as(), Apply a matcap image, reporting unreadable files to the user., Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model., Take a copied control out of whichever hand-built panel holds it., Open a file by what it is: a model, a session, a matcap or an HDRI. The one…, What a file opens as, by its suffix: a model, a session, a matcap or an HDRI. (+2 more)

### Community 146 - "HotkeyStore"
Cohesion: 0.18
Nodes (8): assign(), HotkeyStore, QSettings, Put ``keys`` on a command; says what they came off, if anything., Read the choices off the machine. Never raises., Put ``keys`` on a command, asking first if they are on something else. Returns…, The map, and one signal saying it has changed., The map as it stands. Treat as read-only; change it through the store.

### Community 147 - ".mouseMoveEvent"
Cohesion: 0.13
Nodes (6): Turn the lights by how far the drag has come: across about the vertical, up in…, Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Apply the pull live, so the figure moves under the cursor., Apply the drag live, so the clay re-forms under the cursor.

### Community 148 - "._turn"
Cohesion: 0.22
Nodes (7): _angle(), QRect, Turn the matcap by the angle the cursor swept about the centre. By angle and…, Where the sphere goes: square, centred, above the legend., The angle of ``point`` about ``centre``, anticlockwise with y upwards., An angle difference brought back into -pi to pi., _wrapped()

### Community 149 - "armature.py"
Cohesion: 0.08
Nodes (21): A graph of named points under the form, and the wire it stands for. An armature…, mirror_landmarks(), Preset, An ordered set of landmarks and the armature they build., The landmarks worth asking for under these choices. With mirroring on the…, The midline landmarks, which are what the median plane is fitted to., What to call a landmark in a menu or an undo step. The preset's own words when…, The landmark list with every paired landmark reflected into place. A point the… (+13 more)

### Community 150 - "test_body_regions.py"
Cohesion: 0.29
Nodes (12): _column(), _figure_bones(), ndarray, Where on the body the skin is: bones, height bands, the map, and the settings., A thin column standing from the ground to ``height``., _region(), test_height_bands_follow_the_canon_and_are_soft_at_the_edges(), test_points_go_to_the_region_of_the_nearest_bone_and_blend_between() (+4 more)

### Community 151 - "ContourShadingSettings"
Cohesion: 0.20
Nodes (9): ContourShadingSettings, Parallel slices drawn across the form, the way a contour map reads land. The…, The unit direction the slices are stacked along, in world space., parametrize, The contour shading mode: slices across the form, read off it like a map., test_a_custom_direction_is_normalised_and_an_empty_one_falls_back(), test_the_density_floor_keeps_the_spacing_finite(), test_the_settings_survive_a_session_and_an_older_file_has_them_by_default() (+1 more)

### Community 152 - "EnvironmentMap"
Cohesion: 0.07
Nodes (26): EnvironmentMap, An HDRI read and made ready for the renderer. Built off the thread., What the radiance is multiplied by so that :attr:`peak` comes out at one. One…, A turn about the vertical axis, as a 3x3 matrix., rotation_y(), environment_matrix(), light_rig(), LightRig (+18 more)

### Community 153 - "OidnDenoiser"
Cohesion: 0.21
Nodes (9): gpu_name(), _module(), OidnDenoiser, OidnError, ndarray, RuntimeError, Intel Open Image Denoise, through the ``mitsuba-oidn`` bindings. Open Image…, The GPU Open Image Denoise would use, or ``None`` for none. (+1 more)

### Community 154 - ".probe"
Cohesion: 0.16
Nodes (8): missing_reason(), NeuralInfo, Future, Why no engine was found, in words that say what to do., Whether Neural Rendering can run here, and on what., Find out, on the service thread, whether the engine is here. The future holds a…, What the last probe found, or ``None`` before one has finished., Enhance ``display``, ``(h, w, 4)`` display values, off the calling thread. The…

### Community 155 - "RenderView"
Cohesion: 0.18
Nodes (5): QPainter, QRectF, QWidget, The picture, over a checkerboard where it is transparent, zoomed and moved at…, RenderView

### Community 156 - "WholeFaceToggles"
Cohesion: 0.14
Nodes (10): QApplication, QObject, Making the whole of a switch the part you can press. The theme turns every…, Turns a press anywhere on a switch into a click on it., Put the rule in place for every switch in the application., WholeFaceToggles, The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter. (+2 more)

### Community 157 - "jit.py"
Cohesion: 0.11
Nodes (18): camera_ray(), filter_offset(), device, Primary rays: the pixel filter, the lens, and the two projections. The pixel…, The ray through film position ``(x, y)`` in pixels, top-left origin., _pass(), The built-in denoiser: an edge-avoiding a-trous wavelet filter (Dammertz et al.…, Add samples ``s0`` to ``s1`` of every unfinished pixel in the rectangle to the… (+10 more)

### Community 158 - ".stage_images"
Cohesion: 0.21
Nodes (7): QOpenGLFramebufferObject, QImage, Draw the scene into ``surface`` and read it back as an image., Lay the overlay -- and the caption, if it was asked for -- on a frame. Painted…, One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A…, An offscreen target the frames are drawn into, made once per export.…

### Community 159 - ".paintGL"
Cohesion: 0.17
Nodes (5): Use the same cached visibility test for bones and all point markers., Which part wears the line this frame, and how solid it is, or ``None``. Also…, Hand the renderer the depth grid, or take it away, before a frame., Whether a gesture in the view is moving something right now. What holds the…, The render's size in pixels, as the Render panel sets it for this view.

### Community 160 - "tasks.py"
Cohesion: 0.23
Nodes (11): _draw_glyph(), glyph(), lock_icon(), QColor, QIcon, QPixmap, Small painted icons. Drawing the padlock rather than shipping an image file…, One of the small line drawings above, as an icon. A button whose whole job is… (+3 more)

### Community 161 - "wakelock.py"
Cohesion: 0.16
Nodes (9): _Backend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., A way of asking one platform to stay awake., Ask for sleep to be held off., Withdraw the request. (+1 more)

### Community 162 - "solid_count"
Cohesion: 0.22
Nodes (11): block_count(), piece_count(), How many blocks a count of planes asks the stone to be cut into. One at the…, How many lumps a count of planes asks the clay to be built out of. The masses…, How many solids the form is made of, whichever way it is being worked., solid_count(), However many stages it is thinned to, the last one is the form itself., A slider with a thousand stops is not a slider, and a stage that differs from… (+3 more)

### Community 163 - "neural.py"
Cohesion: 0.24
Nodes (10): _complete(), engine_dir(), Path, NVIDIA DLSS 5 Neural Rendering on a finished picture, through Merserk's…, The engine's controls for one frame, as its ABI version 6 lays them out. Each…, The engine's controls for a still picture with ``settings``. A still has no…, The folder holding all three engine files, or ``None`` when there is none. The…, render_parameters() (+2 more)

### Community 164 - "Human Skin renderer"
Cohesion: 0.25
Nodes (7): Human Skin renderer, Marks and body regions, Material and transport, Scheduling, precision and compatibility, Surface, The HDRI, Where to change it

### Community 165 - ".__init__"
Cohesion: 0.27
Nodes (4): Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo

### Community 166 - "BodySource"
Cohesion: 0.21
Nodes (8): BodyMap, BodySource, build_body_map(), What a body map is worked out from: the meshes, the bones over them, and how., Region weights over the scene, as two RGBA volumes the shader samples by…, Work the region weights out and lay them over the scene as a volume. Every…, Say what the skin's body map is to be worked out from; see :mod:`body_regions`.…, Have the body map for ``source`` built off the thread, and take it when it…

### Community 167 - "test_plane_film.py"
Cohesion: 0.08
Nodes (33): coarse_lattice(), film_of(), fixture, MonkeyPatch, parametrize, Scrubbing through the making of a form, rather than only arriving at it. The…, A cut takes material away, so no stage of a carving is larger than the one…, The same the other way about: a lump adds material, so the form grows. (+25 more)

### Community 168 - "._place_armature_node"
Cohesion: 0.33
Nodes (3): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 169 - "_Export"
Cohesion: 0.20
Nodes (5): NeuralStyle, The look DLSS 5 Neural Rendering aims for., The number the engine knows the style by., _Export, A function as a DLL exports it: callable, and taking ``argtypes`` and…

### Community 170 - "test_trace_denoise.py"
Cohesion: 0.29
Nodes (9): _backends(), fixture, parametrize, The denoisers, each as far as this machine can run it, and EXR output., _scene(), service(), test_every_available_denoiser_cleans_and_keeps_edges(), test_mix_blends_toward_the_noisy_picture() (+1 more)

### Community 171 - "test_trace_bvh.py"
Cohesion: 0.29
Nodes (14): _cast(), _geometry(), The path tracer's tree and rays, against brute force., _rays(), _soup(), _sphere_geometry(), test_a_ghost_is_hit_as_often_as_it_is_solid(), test_nearest_hit_matches_brute_force_on_a_soup() (+6 more)

### Community 172 - "Path tracer"
Cohesion: 0.13
Nodes (14): Colour, Compilation, Denoisers, DLSS 5 Neural Rendering, Human Skin, Integrator, Jobs, Lights (+6 more)

### Community 173 - "TriangleIndex"
Cohesion: 0.09
Nodes (28): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Box the leaves up, coarsest level first and the leaves themselves last., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the… (+20 more)

### Community 175 - "_Encoder"
Cohesion: 0.25
Nodes (5): Queue, _Encoder, QObject, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 176 - "picking.py"
Cohesion: 0.08
Nodes (33): _cross(), Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Row-wise cross product, without :func:`numpy.cross`'s axis shuffling., Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface. (+25 more)

### Community 177 - "matcap_panel.py"
Cohesion: 0.21
Nodes (14): added_matcaps(), forget_matcap(), Path, QIcon, Matcap selection and colour grading. The grading is done on the matcap itself:…, The matcaps added from outside the folder that are still on disk, newest first.…, Keep ``path`` in the gallery from now on., Take ``path`` out of the gallery; the file itself is left alone. (+6 more)

### Community 178 - "write_exr"
Cohesion: 0.31
Nodes (8): ndarray, Path, Writing a render as OpenEXR: the light as it is, and its passes as layers. An…, Write ``layers`` -- ``"RGBA"`` first, then passes by name -- to ``path``.…, Every channel of an EXR by name, as the file groups them; for tests., read_exr_channels(), write_exr(), test_exr_layers_round_trip()

### Community 179 - "._start_update_check"
Cohesion: 0.31
Nodes (4): Ask GitHub for the newest release in the background. The startup check is…, QWidget, show_failure_dialog(), show_up_to_date_dialog()

### Community 180 - "step"
Cohesion: 0.25
Nodes (8): quad(), The reason for reading where the surface is and not only which way. Both faces…, The limit the clustered fits exist to lift, stated as a fact., Add one flat quad, with its own vertices, to a mesh under construction., Two broad faces both looking straight up, one raised above the other. The case…, step(), test_reading_the_normals_alone_cannot_tell_that_step_apart(), test_two_faces_looking_the_same_way_stay_two_planes()

### Community 181 - "VideoSettings"
Cohesion: 0.09
Nodes (23): ffmpeg_path(), open_writer(), Path, How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds. (+15 more)

### Community 182 - "SectionAxis"
Cohesion: 0.18
Nodes (7): Enum, str, The direction the section plane faces., Unit axis, or ``None`` for a custom direction., Which side of the plane survives the cut., SectionAxis, SectionMode

### Community 183 - "HotkeyBinder"
Cohesion: 0.17
Nodes (11): QShortcut, command_for(), HotkeyBinder, QObject, The command a control stands for, or ``None`` if it has no name to go by. A…, Turns the map into the shortcuts of one window, and keeps them current., Put every command's keys where they are heard. Cheap; run on any change., Say in a control's tooltip what key it answers to, if it is one of ours. A copy… (+3 more)

### Community 184 - "._build"
Cohesion: 0.28
Nodes (4): Lay one length of wire earlier or later, as one undoable step., The armature the clay is being built on, or ``None``. An index past the end of…, Put the clay on all of the wire, or take it off all of it., Write which lengths of wire take clay, as one undoable step.

### Community 185 - "lzw"
Cohesion: 0.36
Nodes (5): lzw(), The GIF flavour of LZW: variable-width codes, packed low bit first. Straight…, A plain GIF LZW decoder, for testing the encoder against. Deliberately written…, TestLzw, unlzw()

### Community 186 - "ModelPanel"
Cohesion: 0.05
Nodes (20): ModelPanel, _ObjectTree, QPushButton, QTreeWidgetItem, QWidget, Bind the panel to the viewport's transform tool., Reflect the tool state without re-emitting the toggle., Choose the gesture, from the menu or a key. (+12 more)

### Community 187 - "ui/preferences.py"
Cohesion: 0.10
Nodes (19): current(), forget(), PreferenceStore, QObject, QSettings, _qcolor(), Where the preferences are kept, and what happens when one changes.…, Push the preferences that something in the process holds a copy of.… (+11 more)

### Community 188 - "MeasureTool"
Cohesion: 0.10
Nodes (15): MeasurementSettings, How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., MeasureTool, Handle, ndarray, Two-click measuring, plus dragging the endpoints of an unlocked measurement., The nearest grabbable endpoint under the cursor, if any. Only unlocked, visible… (+7 more)

### Community 189 - "ThreadWakeLock"
Cohesion: 0.22
Nodes (4): Hold sleep off, or stop holding it, whichever is not already true., Drop the request, if one is out. Safe to call more than once., Holds sleep off from a thread of its own, for as long as some work runs. For a…, ThreadWakeLock

### Community 190 - "test_render_panel.py"
Cohesion: 0.18
Nodes (4): app(), panel(), fixture, The Render panel and the Render window, offscreen.

### Community 191 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 192 - "role_bones"
Cohesion: 0.25
Nodes (6): looks_like_a_figure(), The bones a skeleton's humanoid roles describe, as ``(count, 7)`` rows. Each…, Whether the bones say enough about a body to place its skin by., role_bones(), What the skin shader's body map is worked out from, or ``None`` for no map. The…, test_unnamed_helper_joints_are_stepped_over_and_a_lone_pelvis_is_a_point()

### Community 193 - "ui/hotkeys.py"
Cohesion: 0.09
Nodes (23): QKeySequenceEdit, control_of(), decorate(), describe(), forget(), group_of(), KeyBox, listed() (+15 more)

### Community 194 - ".__init__"
Cohesion: 0.10
Nodes (10): _plain(), QAction, Open the preferences, on one group when the menu asked for one., Push the preferences that this window's own parts hold a copy of. The store has…, Put the docks and the hand-built panels back where they were. Unless the artist…, A menu entry's text as a name: no accelerator ampersand, no trailing dots., Give each panel a dock of its own, tabbed together on the right. Each panel can…, Which panels are open, and the panels the artist builds. Rebuilt every time it… (+2 more)

### Community 195 - ".update_enabled"
Cohesion: 0.29
Nodes (4): Hold the settings a recording is built from still while it runs. A film is a…, Show what this way of working needs, and put the rest away. A setting that does…, The bones of the chosen armature, in the order the clay goes down. Every intact…, What can be done to the list, given where the handle is and whether a film is…

### Community 196 - "cube"
Cohesion: 0.22
Nodes (10): cube(), How far the least well served of ``wanted`` is from anything offered., The one form whose planes are not a matter of opinion., The sample limit is a speed measure, so it must not move the planes. Asked of a…, A cube with hard edges, each face cut into a grid of triangles., A mode with no fitter behind it would shade as an unbroken surface., test_a_cube_breaks_into_its_own_six_faces(), test_every_mode_the_panel_offers_can_be_fitted() (+2 more)

### Community 197 - "test_workspace_layout.py"
Cohesion: 0.24
Nodes (7): app(), _Plain, fixture, QMainWindow, A layout saved before a panel existed still tabs that panel in with the rest., test_a_new_panel_joins_the_tab_strip_of_an_old_layout(), _window()

### Community 198 - "ask_for"
Cohesion: 0.16
Nodes (12): ask_for(), HotkeyDialog, normalize(), Command, QAction, QDialog, A menu entry. Its keys are heard anywhere in the window and shown in the menu., A key heard only while the view has the focus. The menu entry for it, if there… (+4 more)

### Community 199 - "_drop_on"
Cohesion: 0.29
Nodes (7): QMimeData, _drop_on(), The end of the gesture: the payload a drag carries, delivered., Drop ``mime`` on the top-left of ``panel``; was it taken? The caller keeps hold…, test_a_drop_carrying_a_control_takes_a_copy_of_it(), test_a_drop_carrying_something_else_is_refused(), test_a_drop_naming_a_control_that_is_gone_is_refused()

### Community 200 - "build_bvh"
Cohesion: 0.38
Nodes (6): _area(), build_bvh(), ndarray, A bounding-volume hierarchy over triangle boxes, built by the surface-area…, Half the surface area of boxes; nought for an empty (inverted) one., Build the tree over triangle boxes. Returns the triangle order, and per node…

### Community 201 - "denoise.py"
Cohesion: 0.29
Nodes (5): atrous(), ndarray, ``(h, w, 3)`` light in, smoothed light out. ``noise`` is the expected error of…, Denoising a render: choosing a denoiser, and running it on a thread of its own.…, The film: the sums a render adds its samples into, and the passes read off…

### Community 202 - "._on_bone_toggled"
Cohesion: 0.29
Nodes (4): QListWidgetItem, Catch the selection a click on a checkbox is about to collapse. Qt selects a…, Which bones of the armature the picked-out rows stand for., Take lengths of wire out of the clay, or put them back. A tick on a row that…

### Community 203 - "bent_plate"
Cohesion: 0.17
Nodes (12): angle_deg(), bent_plate(), ndarray, A flat with a scattering of bad normals is still shaded as that flat. Averaging…, A plate creased down the middle, and which column each vertex is in. Flat to…, Vertices on a turn are ambiguous about their plane, so they are quieted. The…, Splitting a broad flat by place must not invent a turn in it. The plate below…, How many planes have another plane pointing very nearly where they do. (+4 more)

### Community 204 - "OutputFormat"
Cohesion: 0.33
Nodes (3): OutputFormat, What a saved render is written as., Whether the file keeps scene light rather than display values.

### Community 205 - "_WindowsBackend"
Cohesion: 0.25
Nodes (5): ``SetThreadExecutionState``: a flag on this thread, not a handle. The flags…, _WindowsBackend, skipif, The flag the viewer sets is the one Windows reports back afterwards., test_windows_really_sets_the_execution_state()

### Community 206 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 207 - "_MacBackend"
Cohesion: 0.33
Nodes (3): c_void_p, _MacBackend, An IOKit power assertion, held by id until it is released.

### Community 208 - "section"
Cohesion: 0.50
Nodes (4): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., section()

### Community 209 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 210 - "._commit_node_drag"
Cohesion: 0.33
Nodes (3): Record the finished gesture: a move, a resize, or a plain click. A press that…, Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…

### Community 211 - "FormRun"
Cohesion: 0.40
Nodes (3): FormRun, Begin a run against a form already in the store., A guided form part-way through.

### Community 213 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 214 - "test_plane_solids.py"
Cohesion: 0.05
Nodes (41): block(), box(), Blocking a form in out of its planes, as stone is cut and as clay is built.…, A closed box with hard edges, each face cut into a grid of triangles., It is cut out of a block rather than built up on anything, so handing it a wire…, How far each point sits from the middle of its neighbours, as a share of the…, The relax is a pass over the finished surface rather than anything the volume…, Counting crossings is exact on a closed surface and meaningless on anything… (+33 more)

### Community 215 - "rounded"
Cohesion: 0.40
Nodes (5): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick., rounded()

## Knowledge Gaps
- **27 isolated node(s):** `refview`, `FunctionTable`, `OptixDenoiserOptions`, `OptixDenoiserGuideLayer`, `OptixDenoiserLayer` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `SceneObject`, `obj_loader.py`, `trace/scene.py`, `ExportLook`, `Camera`, `autoskin.py`, `_wires`, `ViewerState`, `Skeleton`, `build_form`, `PoseTool`, `test_body_regions.py`, `core/__init__.py`, `viewport.py`, `FilmRecorder`, `convex.py`, `test_plane_clusters.py`, `BodySource`, `test_plane_film.py`, `auto_skin`, `test_trace_bvh.py`, `Rig`, `TriangleIndex`, `picking.py`, `body_regions.py`, `settings.py`, `step`, `RegionSource`, `SectionAxis`, `test_skeleton.py`, `test_forms.py`, `PrimaryForm`, `cube`, `test_objects.py`, `test_skin.py`, `plane_regions`, `bent_plate`, `._commit_objects`, `skeleton.py`, `test_plane_solids.py`, `rounded`, `main_window.py`, `state.py`, `ball`, `FormStore`, `Path`, `plane_axes`, `Path`, `forms.py`?**
  _High betweenness centrality (0.181) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `test_preferences.py`, `Viewport`, `SceneObject`, `MainWindow`, `RenderController`, `Bone`, `CameraPanel`, `test_body_regions.py`, `PoseTool`, `core/__init__.py`, `RenderView`, `viewport.py`, `ShadingPanel`, `.__init__`, `auto_skin`, `test_matcap_preview.py`, `test_render_panel.py`, `role_bones`, `.__init__`, `PrimaryForm`, `test_objects.py`, `test_skin.py`, `test_workspace_layout.py`, `test_custom_panels.py`, `render_controller.py`, `section`, `panel`, `._commit_objects`, `test_forms_panel.py`, `MatcapPanel`, `overlay.py`, `main_window.py`, `RenderWindow`, `test_elements.py`, `test_a_group_the_mode_does_not_answer_leaves_no_room_behind`, `Measurement`, `state.py`, `Path`, `Session`, `ViewportOverlay`, `Armature`, `test_trace_neural.py`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `._upload_sculpt`, `._sync_scene`, `test_preferences.py`, `SurfacePicker`, `ExportLook`, `MainWindow`, `ViewerState`, `._picker`, `build_form`, `.mouseMoveEvent`, `PoseTool`, `core/__init__.py`, `viewport.py`, `.stage_images`, `.paintGL`, `FilmRecorder`, `.__init__`, `._place_armature_node`, `ExportVideoDialog`, `._active_changed`, `_Encoder`, `FilmExport`, `MeasureTool`, `.__init__`, `PrimaryForm`, `test_objects.py`, `ObjectTool`, `NavigationController`, `._commit_node_drag`, `.film`, `ViewportRenderPreview`, `overlay.py`, `main_window.py`, `Measurement`, `state.py`, `.mouseReleaseEvent`, `ViewportOverlay`, `Armature`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Are the 60 inferred relationships involving `Mesh` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Mesh` has 60 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `OverlayParts`) actually correct?**
  _`ViewerState` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Skeleton` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Skeleton` has 9 INFERRED edges - model-reasoned connections that need verification._