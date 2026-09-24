# Graph Report - reference-viewer  (2026-09-24)

## Corpus Check
- 222 files · ~584,923 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 6954 nodes · 16474 edges · 221 communities (215 shown, 6 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 869 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `68f0ac33`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SettingsWindow
- test_preferences.py
- update_check.py
- Viewport
- SceneObject
- trace/scene.py
- MainWindow
- Stroke
- GifWriter
- pose_panel.py
- RenderSettings
- auto_skin
- Cuda
- SurfacePicker
- Armature
- environment.yml
- ViewerState
- Skeleton
- PrimaryForm
- CameraPanel
- PosePanel
- ShaderProgram
- PoseTool
- test_planes_panel.py
- MeasurePanel
- Camera
- _Target
- core/__init__.py
- plane_volume.py
- ControlsWindow
- DenoiseService
- .refresh
- FilmRecorder
- convex.py
- test_plane_clusters.py
- WakeLock
- integrator.py
- lights.py
- Frame
- VideoFormat
- RenderJob
- core/camera.py
- FrameBar
- ValueSlider
- Rig
- ExportVideoDialog
- trace/skin.py
- _Build
- Agent Graph-First Instructions
- body_regions.py
- settings.py
- test_matcap_preview.py
- test_armature.py
- ArmaturePanel
- RegionSource
- test_hotkeys.py
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
- Link
- FormTool
- _derived
- test_objects.py
- test_skin.py
- test_plane_solids.py
- ObjectTool
- default_matcap_pixels
- ArmatureSettings
- test_trace_integrator.py
- load_matcap_pixels
- test_custom_panels.py
- test_trace_jit.py
- core/preferences.py
- core/environment.py
- NavigationController
- ShadingPanel
- ._commit_objects
- test_forms_panel.py
- test_session.py
- ArmatureTool
- render_controller.py
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
- MeshBuffers
- FormStore
- clone.py
- skin_detail.py
- Path
- plane_axes
- .mouseReleaseEvent
- PointEdit
- plane_count
- ColorButton
- test_tasks.py
- trace_sample
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
- test_camera.py
- ArmatureStore
- path_trace.py
- obj_loader.py
- FakeEngine
- forms.py
- SectionPanel
- ._upload_sculpt
- ._sync_scene
- colour.py
- AnnotateTool
- ExportLook
- load_mesh
- preview
- elements/__init__.py
- paths.py
- Release
- Film
- Command
- VideoError
- RenderController
- vec.py
- MatcapPreview
- ._picker
- in_flight
- shader_files.py
- OpenRequests
- matcap_preview.py
- Preset
- test_body_regions.py
- load_obj
- EnvironmentMap
- stl_loader.py
- NeuralService
- PanelDock
- palette.py
- jit.py
- .stage_images
- .paintGL
- tasks.py
- wakelock.py
- mesh_io.py
- neural.py
- Human Skin renderer
- .__init__
- SkinRefinement
- coarse_lattice
- ._place_armature_node
- _Export
- Reflow
- test_trace_bvh.py
- Path tracer
- TriangleIndex
- TaskRunner
- make_switch
- picking.py
- .reset
- CHANGELOG.md
- .dress_tabs
- step
- VideoSettings
- .column_of
- lumpy
- ._build
- lzw
- ModelPanel
- ui/preferences.py
- MeasureTool
- ThreadWakeLock
- test_render_panel.py
- release.yml
- ndarray
- ui/hotkeys.py
- .__init__
- .update_enabled
- cube
- test_workspace_layout.py
- _height_of
- .install
- .new_custom_panel
- reflow.py
- ._on_bone_toggled
- bent_plate
- .plane_span_deg
- _WindowsBackend
- ._place_joint
- _MacBackend
- section
- panel
- ._commit_node_drag
- ._place_form_landmark
- .film
- app
- FrameTarget
- .with_landmark_at
- save_obj
- new_stacks
- app
- _share_between
- .browse_environment

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

## Communities (221 total, 6 thin omitted)

### Community 0 - "SettingsWindow"
Cohesion: 0.13
Nodes (14): PreferenceStore, QObject, The preferences, and one signal saying they have changed. A single instance,…, The preferences as they stand. Treat as read-only; use :meth:`set`., QWidget, Fill in the groups. A switch with nothing to put in the caption column is given…, Every command with its keys, each key a box that takes one keystroke. The list…, The one button that is not a preference, and what the window is for. (+6 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.06
Nodes (45): _clamp(), Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, Pull anything out of range back into it. The window cannot produce these…, Back to how the application ships., Read the preferences off the machine. Never raises., app() (+37 more)

### Community 2 - "update_check.py"
Cohesion: 0.10
Nodes (31): check_for_update(), fetch_latest_release(), is_newer(), _macos_root_certificates(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and… (+23 more)

### Community 3 - "Viewport"
Cohesion: 0.06
Nodes (17): QOpenGLWidget, Free every GL object while the owning context is still current., Arm one tool, disarming the rest. Only one gesture can own the left button, so…, Drop whatever gesture is half-finished, without disarming the tool., One of the renderer's :data:`~refview.render.mesh_renderer.ANTIALIASING_MODES`., Renders the scene and turns mouse gestures into camera and tool actions., Slide the view so a point sits at the centre, keeping the angle., The gesture a key press chooses, if the transform tool is armed to hear it. (+9 more)

### Community 4 - "SceneObject"
Cohesion: 0.07
Nodes (18): ObjectSettings, ObjectStore, ndarray, Snapshot, What a parent's state means for its children, and how the tools scale. Each is…, One model in the scene. Three meshes are kept, as the viewer kept them when…, The centred mesh carried by ``matrix`` -- the mesh itself for the identity., Drop the derived meshes, after the rest mesh has been replaced. (+10 more)

### Community 5 - "trace/scene.py"
Cohesion: 0.07
Nodes (49): IntEnum, filter_table(), ndarray, The inverse cumulative distribution of a separable filter, as offsets in…, empty_geometry(), flatten(), Geometry, NamedTuple (+41 more)

### Community 6 - "MainWindow"
Cohesion: 0.05
Nodes (16): MainWindow, QMainWindow, The document this window edits., Keep the menu entry agreeing with the panel's own checkbox., Put every panel button and menu entry where the tools now stand. Only one tool…, Swap between the eraser and the drawing mode it was called from., Path-trace the view, at the Render panel's size, into the Render window., Open an empty panel of the artist's own and bring it to the front. (+8 more)

### Community 7 - "Stroke"
Cohesion: 0.05
Nodes (39): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+31 more)

### Community 8 - "GifWriter"
Cohesion: 0.08
Nodes (27): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), palette_of(), ndarray, Path (+19 more)

### Community 9 - "pose_panel.py"
Cohesion: 0.05
Nodes (62): JointRef, Quat, Quat4, BoneLabels, Buried, Enum, str, When the length of a bone is written beside it. (+54 more)

### Community 10 - "RenderSettings"
Cohesion: 0.06
Nodes (41): Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, bind_default(), Restore a framebuffer captured with :func:`current_framebuffer`., light_directions(), normal_matrix(), ndarray (+33 more)

### Community 11 - "auto_skin"
Cohesion: 0.06
Nodes (55): auto_skin(), _baked_rest(), bone_segments(), _conjugate_gradients(), _CotLaplacian, _envelope_weights(), _Graph, _heat_weights() (+47 more)

### Community 12 - "Cuda"
Cohesion: 0.05
Nodes (32): FunctionTable, OptixDenoiserGuideLayer, OptixDenoiserLayer, OptixDenoiserOptions, OptixDenoiserParams, OptixDenoiserSizes, OptixDeviceContextOptions, OptixImage2D (+24 more)

### Community 13 - "SurfacePicker"
Cohesion: 0.07
Nodes (33): BoneRef, _project(), The nearest bone under the cursor, for showing its length., A world point in widget pixels, or ``None`` when it is behind the camera., Where a click at ``(x, y)`` would put a landmark: on the surface, or nowhere.…, ndarray, A view of the scene from one camera, sized to the widget., Point on the camera-facing plane through ``anchor``. This is where free-… (+25 more)

### Community 14 - "Armature"
Cohesion: 0.05
Nodes (48): Armature, ArmatureNode, Bone, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves., A plausible thickness for a node placed by hand. (+40 more)

### Community 15 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 16 - "ViewerState"
Cohesion: 0.05
Nodes (35): Qt user interface: the viewport widget, the panels and the main window., Command, ndarray, Write ``obj``'s turn and scale into its mesh, leaving it standing as it is.…, A parenting policy changed: what is shown and how solid may have too., Turn every object the same way; see :meth:`set_object_orientation`. For files…, Turn one object, bringing the marks made on it along. Measurements,…, The 4x4 that takes a point on the old rest mesh onto the new one. A point sits… (+27 more)

### Community 17 - "Skeleton"
Cohesion: 0.05
Nodes (34): Joint, _matrix16(), _pose_matrices(), ndarray, Whether the pose differs from the rest at all., A copy with the rest translation replaced and the frame kept., A tree -- or a forest -- of joints and the pose they stand in., Every joint, parents before children. A file may list a child before its… (+26 more)

### Community 18 - "PrimaryForm"
Cohesion: 0.06
Nodes (58): PlacedLandmark, One anatomical point the artist put on the model during a guided run., build_form(), built_count(), form_mesh(), landmark_signature(), median_plane_ready(), mirror_form_landmarks() (+50 more)

### Community 19 - "CameraPanel"
Cohesion: 0.11
Nodes (9): CameraPanel, QListWidgetItem, Take the planes in hand where the fit left them, or hand them back., Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions. (+1 more)

### Community 20 - "PosePanel"
Cohesion: 0.05
Nodes (25): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Record an edit the viewport's tool worked out., PosePanel, QTreeWidgetItem, The skeleton the panel is about: the selected row's, else the last., Highlight a row, in the tree and in the view. (+17 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): Fill the shader's table with a level, if it is not already in it., ndarray, RuntimeError, Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "PoseTool"
Cohesion: 0.09
Nodes (35): PoseTool, ndarray, The pose shift that puts joint ``index`` at ``target``, children and all., Which way the bone at joint ``index`` runs, in the scene. Towards its first…, The frame a joint's pose is written in: its parent's, then its rest., Turns pulls on joints into pose edits, and clicks into new joints., Where a click at ``(x, y)`` would put a new joint., Where a pulled joint is being pulled to. Across the camera-facing plane through… (+27 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.08
Nodes (21): _names(), The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as…, Or there would be no way to turn one back on., A limb is four bones, and deciding not to block the arms in is one decision.…, It is rebuilt on every change, and ticking one row of a selected limb would be… (+13 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.12
Nodes (8): MeasurePanel, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn.

### Community 25 - "Camera"
Cohesion: 0.04
Nodes (33): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around. (+25 more)

### Community 26 - "_Target"
Cohesion: 0.07
Nodes (15): AccumTarget, ColorTarget, DepthTarget, GeometryTarget, A depth-only framebuffer, sampled afterwards as a texture., ``clamp_to_lit`` makes everything outside the map read as unshadowed., A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the… (+7 more)

### Community 27 - "core/__init__.py"
Cohesion: 0.05
Nodes (52): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, Qt-free geometry, camera and document model for the reference viewer., Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal() (+44 more)

### Community 28 - "plane_volume.py"
Cohesion: 0.04
Nodes (108): _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field(), block_labels(), block_splits() (+100 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "DenoiseService"
Cohesion: 0.07
Nodes (36): DenoiserDevice, DenoiseSettings, Where Open Image Denoise runs., atrous(), ndarray, ``(h, w, 3)`` light in, smoothed light out. ``noise`` is the expected error of…, DenoiseRequest, DenoiserInfo (+28 more)

### Community 31 - ".refresh"
Cohesion: 0.18
Nodes (4): List the bundled HDRIs, and the one in use if it is from elsewhere., Put the light's numbers back in line with the settings, after a drag or an undo., Freeze the slices the way the camera faces now. The view direction is the one…, Show what this mode is actually lit and shaded by, and hide the rest. A matcap…

### Community 32 - "FilmRecorder"
Cohesion: 0.06
Nodes (35): QThread, FilmRecorder, Film, QObject, The film being recorded, or the last one finished., Whether a film is being made right now., The film already held for ``key``, if there is one., Stop any recording in flight and forget what it was making. The thread is asked… (+27 more)

### Community 33 - "convex.py"
Cohesion: 0.13
Nodes (21): convex_hull(), flat_mesh(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, The outward unit normal at each vertex: the area-weighted mean of its faces'. A…, The barycentric ``(w, u, v)`` of an even grid over a triangle. (+13 more)

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.17
Nodes (20): parametrize, Fitting planes to a model's surface rather than only to its normals. What…, Merging back from patches is a hierarchy, so the cuts of it nest. This is what…, Every plane of a level as a hashable whole: direction, place and offset., Nothing is seeded at random, so a session reopens looking the same., The renderer reads an empty set as "leave the normals alone"., The shader has to put a fragment into that frame before it can look up which…, The planes moved out of a uniform array and into a texture so that the count… (+12 more)

### Community 35 - "WakeLock"
Cohesion: 0.17
Nodes (13): Holds sleep off while the window that owns it is the one in front. The class…, WakeLock, Broken, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do., A platform that refuses, the way an old or locked-down one might., The viewer must open and close normally on a machine that says no., Recorder (+5 more)

### Community 36 - "integrator.py"
Cohesion: 0.11
Nodes (39): _accept(), any_rays(), cap_normal(), cast_rays(), clipped(), intersect(), occluded(), offset_origin() (+31 more)

### Community 37 - "lights.py"
Cohesion: 0.12
Nodes (34): disc_hit(), env_background(), _env_frame(), env_pdf(), env_radiance(), env_sample(), _env_world(), light_row() (+26 more)

### Community 38 - "Frame"
Cohesion: 0.08
Nodes (26): carried(), _push_frame(), Nothing: each row inside the copy is linked on its own., Read a drag's payload back, or ``None`` if it is not one of ours., CustomPanel, _detach(), QFormLayout, QWidget (+18 more)

### Community 39 - "VideoFormat"
Cohesion: 0.08
Nodes (16): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+8 more)

### Community 40 - "RenderJob"
Cohesion: 0.09
Nodes (17): adaptive_error(), Mark blocks whose noise has fallen below ``threshold`` as done; returns pixels…, _hilbert_index(), JobState, _lower_priority(), pass_schedule(), Enum, A render in progress: the threads, the order the pixels are done in, and when… (+9 more)

### Community 41 - "core/camera.py"
Cohesion: 0.10
Nodes (24): Named camera positions the artist can jump between while sculpting., _distance_or_none(), Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., A clipping distance as a file wrote it, or ``None`` for one left to the fit. (+16 more)

### Community 42 - "FrameBar"
Cohesion: 0.09
Nodes (8): FrameBar, QPainter, QSize, QWidget, The mark beside a group's name: filled when open, a ring when shut. It is the…, What colour a group's name is written in., The bar across the top of a :class:`Frame`: its name and its fold., _title_ink()

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (11): _pull_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end., Set the value the way a hand on the control would., The value the track stands at ``x`` pixels across. (+3 more)

### Community 44 - "Rig"
Cohesion: 0.06
Nodes (53): Model orientation (1.1.0), STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), _first_skin(), GltfLoadError, load_gltf() (+45 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.09
Nodes (14): even(), ExportVideoDialog, Film, Path, QDialog, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+6 more)

### Community 46 - "trace/skin.py"
Cohesion: 0.15
Nodes (32): body_fetch(), bump(), diffusion_lengths(), dome(), _fract32(), hash4(), marks(), device (+24 more)

### Community 47 - "_Build"
Cohesion: 0.21
Nodes (14): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _mid(), ndarray, Somewhere to collect nodes while the rules that need each other run. (+6 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "body_regions.py"
Cohesion: 0.11
Nodes (26): band_weights(), BodyMap, BodySource, bone_weights(), build_body_map(), looks_like_a_figure(), ndarray, Where on the body a point of the skin is, so that the skin can be marked as… (+18 more)

### Community 50 - "settings.py"
Cohesion: 0.02
Nodes (115): BodyRegionSettings, Where the regions come from, and what each does to the skin effects., One region's multiplier for ``effect`` after another, in :data:`REGIONS` order., build_grid(), GridLines, GridSettings, nice_step(), Reference grids on the three axis planes, fading with distance. A grid gives… (+107 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.10
Nodes (33): QPoint, _drag(), _listed(), _matcap_file(), parametrize, The matcap as its own control, and whether it tells the truth. The disc is only…, The picture follows the hand, which is the whole reason for the disc., Dragging further than the range goes is not a negative gamma. (+25 more)

### Community 52 - "test_armature.py"
Cohesion: 0.08
Nodes (53): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _chain(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other., The femoral head is in from the ASIS, below it and behind it, by shares of the… (+45 more)

### Community 53 - "ArmaturePanel"
Cohesion: 0.04
Nodes (38): QTreeWidget, ArmaturePanel, QPushButton, QTreeWidgetItem, QWidget, Run a row's edit once Qt has finished delivering the current signal. Committing…, Arms the armature tool, lists its nodes and runs the guided presets., Add a group below the list rather than to the panel root. (+30 more)

### Community 54 - "RegionSource"
Cohesion: 0.18
Nodes (8): _default_profiles(), Enum, str, How much of each skin effect one region gets, relative to its slider., Starting values for skin effects across a generic body., Where the region map comes from., RegionProfile, RegionSource

### Community 55 - "test_hotkeys.py"
Cohesion: 0.04
Nodes (46): QKeySequence, Command, HotkeyMap, Any, Which keys do what, as the artist has decided rather than as it ships. A hotkey…, Whether the artist has moved this command off what it ships with., Which command has these keys, if any., Every command with keys on it, declared or not, as id -> keys. (+38 more)

### Community 56 - "FilmExport"
Cohesion: 0.09
Nodes (16): Queue, _Encoder, FilmExport, frame_bytes(), QImage, QObject, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, The encoding itself, living on a thread of its own. It takes frames off a short… (+8 more)

### Community 57 - "FormsPanel"
Cohesion: 0.04
Nodes (32): FormsPanel, QTreeWidgetItem, Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Begin a run against a fresh form: a preset's walk, or a freeform's., Take up the selected freeform again, so more landmarks can go on it. The same…, The freeform the highlighted row belongs to, when no run is on. (+24 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.18
Nodes (6): PlanesPanel, Put the design matrix back the way it reads a figure., Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Breaks the form into planes, in the shading or in the geometry itself., Re-read the armatures and what the chosen one is laying down. Called whenever…

### Community 59 - "test_skeleton.py"
Cohesion: 0.05
Nodes (67): What to call the joint filling a humanoid slot: ``"knee.L"`` is ``"Knee L"``., role_name(), quat_from_axis_angle(), armature_from_skeleton(), build_humanoid_skeleton(), detail_joints(), humanoid_positions(), humanoid_roles() (+59 more)

### Community 60 - "Progress"
Cohesion: 0.08
Nodes (21): Exception, CancelledError, Progress, What a long piece of work says about itself while it runs, and how it is…, Ask the work to stop at its next report., How far along, 0 to 1, or ``None`` when the work has not said., Whether the work has said how much there is to do., A window onto part of a parent's range; see :meth:`Progress.slice`. (+13 more)

### Community 61 - "Workspace"
Cohesion: 0.12
Nodes (9): QMainWindow, QObject, Keep every switch agreeing with the panel it speaks for., Open the dock a hand-built panel lives in and bring it to the front., Take a hand-built panel away. Its dock is parked, not destroyed. The dock has…, Rebuild the panels built by hand. Call before :meth:`restore_state`. Whatever…, Put the layout back. Returns whether there was one to put back., The docks of one window: the fixed panels and the ones built by hand. (+1 more)

### Community 62 - "form_group"
Cohesion: 0.05
Nodes (30): QComboBox, QSpinBox, memory_estimate(), Roughly how many bytes a render of this size holds while it runs. The sums of…, framed(), A frame with a form layout in it, ready to be filled., QPushButton, QWidget (+22 more)

### Community 63 - "test_forms.py"
Cohesion: 0.05
Nodes (76): merged(), One convex piece of a form: its hull vertices and outward-wound faces., The hull of the points with its faces bowed out; see :func:`rounded_hull`., The longest side of the box the solid sits in., Whether a point lies inside, or within ``slack`` of the surface., Several flat meshes as one, or ``None`` when there is nothing to draw., Solid, _across() (+68 more)

### Community 64 - "application.py"
Cohesion: 0.13
Nodes (20): ArgumentParser, QSplashScreen, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font(), main(), Namespace (+12 more)

### Community 65 - "render_frame.py"
Cohesion: 0.12
Nodes (25): Rect, OutputSettings, How large the picture is and how it is saved., clamp_size(), frame_rect(), framed_camera(), output_size(), preset_size() (+17 more)

### Community 66 - "Link"
Cohesion: 0.12
Nodes (9): CloneGesture, Link, _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original., Whether the copy is being used right now and must not be written. (+1 more)

### Community 67 - "FormTool"
Cohesion: 0.06
Nodes (30): FormLandmarkRef, FormSettings, How the forms are drawn, and how their landmarks are placed., FormRun, FormTool, ndarray, Placing the landmarks of a form, led by a preset or by the artist, and…, Begin a run against a form already in the store. (+22 more)

### Community 68 - "_derived"
Cohesion: 0.08
Nodes (28): _kept_laying(), Fresh bones, laid the way the armature was already laying them. The bone list…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _derived(), A guess the artist corrects is theirs, and the mirror leaves it alone., The new list is the edit; the old one has to survive to be undone to., Mirroring moves a guess in place, which must not reach the undo history. (+20 more)

### Community 69 - "test_objects.py"
Cohesion: 0.10
Nodes (37): Write a mesh out; only OBJ is written, whatever the suffix asked for., save_mesh(), Path, Where an object stands relative to its parent: an affine placement. Held as the…, Transform, Moving, turning and scaling an object by taking hold of it in the view. One…, app(), _key() (+29 more)

### Community 70 - "test_skin.py"
Cohesion: 0.08
Nodes (31): _area(), build_bvh(), ndarray, A bounding-volume hierarchy over triangle boxes, built by the surface-area…, Half the surface area of boxes; nought for an empty (inverted) one., Build the tree over triangle boxes. Returns the triangle order, and per node…, build_scene(), ndarray (+23 more)

### Community 71 - "test_plane_solids.py"
Cohesion: 0.02
Nodes (169): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, Holds the working state between one turn of the sliders and the next.…, The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., sculpt_mesh(), SculptCache (+161 more)

### Community 72 - "ObjectTool"
Cohesion: 0.12
Nodes (14): _axis_param(), Gizmo, _Grip, ObjectTool, ndarray, The three directions the arms run along, in world space. A move and a turn are…, Where the gizmo for an object at ``world`` falls on screen, or ``None`` if…, Which handle a screen point is over: ``"centre"``, ``"x"``, ``"y"``, ``"z"`` or… (+6 more)

### Community 73 - "default_matcap_pixels"
Cohesion: 0.16
Nodes (13): default_matcap_pixels(), A neutral studio matcap, used before the user picks one., QImage, Draw the matcap onto a sphere of ``size`` pixels, graded. Returns ``(size,…, The matcap as a picture, at its own resolution. Square and opaque, with the…, The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…, sample(), Positive rotation moves a feature clockwise, which is the way a drag goes.… (+5 more)

### Community 74 - "ArmatureSettings"
Cohesion: 0.11
Nodes (24): ArmatureSettings, How the armature is drawn, and how new nodes are placed., The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now., How many landmarks are placed, out of how many will be asked for., Pass over the landmark being asked for; the figure loses what it fed., Un-skip or un-place the landmark before this one, and ask again. Returns the…, _at() (+16 more)

### Community 75 - "test_trace_integrator.py"
Cohesion: 0.13
Nodes (29): _inputs(), Whole renders: energy, determinism, the two methods, stopping, adaptive…, Under light of radiance one from everywhere, a convex matte ball shows its…, _render(), test_a_cancel_stops_the_render_promptly(), test_adaptive_sampling_spends_less_on_the_quiet_background(), test_bucket_and_progressive_make_the_same_picture(), test_no_sample_is_ever_nan() (+21 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.18
Nodes (20): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+12 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.07
Nodes (23): QMimeData, app(), custom(), _drop_on(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error., A group is not a row, so it goes ahead of the group it was dropped on. (+15 more)

### Community 78 - "test_trace_jit.py"
Cohesion: 0.20
Nodes (8): available(), The CPU path tracer: numpy and numba, never Qt and never OpenGL. Importing this…, Whether the path tracer can run here (numba loads)., Why the path tracer cannot run, or ``None`` when it can., unavailable_reason(), The path tracer's plumbing: numba, its cache, and what restarts a preview., test_a_frozen_builds_cache_locator_can_be_installed(), test_numba_is_here_and_caches_in_a_folder_of_ours()

### Community 79 - "core/preferences.py"
Cohesion: 0.12
Nodes (18): _as_kind_of(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any, What the artist prefers, as distinct from what the document says. There are two… (+10 more)

### Community 80 - "core/environment.py"
Cohesion: 0.07
Nodes (61): direction_to_uv(), dominant_light(), downsized(), EnvironmentLoadError, evaluate_sh(), _exr_rgb(), _halve(), irradiance_sh() (+53 more)

### Community 81 - "NavigationController"
Cohesion: 0.07
Nodes (28): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Degrees of yaw per pixel, signed by whether the drag is inverted. (+20 more)

### Community 82 - "ShadingPanel"
Cohesion: 0.14
Nodes (8): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Slot that writes one field of the contour shading settings., Slot that writes one field of the grid settings., ShadingPanel

### Community 83 - "._commit_objects"
Cohesion: 0.07
Nodes (20): ObjectsEdit, Snapshot, A copy of ``obj``'s mesh on top of it, made active, as one undo step., Scale ``objects`` so each is the size of the active one, as one undo step. The…, The largest of ``obj``'s three extents as it stands in the world., Re-read how solid each part is drawn, without touching the geometry., An edit to the objects -- a move, a parenting, a removal -- as two snapshots.…, Where everything stands now; the start of a gesture keeps one. (+12 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.11
Nodes (30): app(), _click(), panel(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The… (+22 more)

### Community 85 - "test_session.py"
Cohesion: 0.09
Nodes (21): Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., A step of the slider is worth a fixed share more planes, not a fixed number of…, The ceiling went from 64 planes to 256 without moving the slider under anyone:…, The panel edits the settings; the fit has to be told what they are., Both modes answer in degrees of turn, so the panel can just ask., Version 1 files predate the annotation layer and the endpoint lock., Version 6 files predate panels being something a session could carry. (+13 more)

### Community 86 - "ArmatureTool"
Cohesion: 0.08
Nodes (14): LandmarkRef, ArmatureTool, GuideRun, Handle, Begin a preset run against an armature already in the store., Where a click at ``(x, y)`` would put a node. With free placement the node…, Where a grabbed node should move to. Free placement -- and a drag that wanders…, The thickness a resize drag is asking for: the cursor's reach, in world units. (+6 more)

### Community 87 - "render_controller.py"
Cohesion: 0.07
Nodes (30): develop_region(), exposure_scale(), quantize_region(), Develop a rectangle of the film into ``out``, ``(h, w, 4)`` float32 display…, Display values to 8-bit RGBA, rounding to nearest., Film, ndarray, The picture and its guides, as a film holds them. (+22 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.09
Nodes (23): added_matcaps(), forget_matcap(), MatcapPanel, Path, QIcon, The matcaps added from outside the folder that are still on disk, newest first.…, Keep ``path`` in the gallery from now on., Take ``path`` out of the gallery; the file itself is left alone. (+15 more)

### Community 89 - "AnnotatePanel"
Cohesion: 0.21
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 90 - "overlay.py"
Cohesion: 0.07
Nodes (23): DepthDrag, draw_rail(), draw_text(), MarkerVisibility, Shared marker appearance, visibility, and constrained depth gestures., A grid across the depth axis, at the depth the point has reached. Returns…, One marker object for endpoints, nodes, landmarks and tool previews., Cache surface occlusion by view and position for every kind of marker. The… (+15 more)

### Community 91 - "main_window.py"
Cohesion: 0.04
Nodes (65): QScrollArea, Every document edit is a command, AddItem, Command, The handful of undoable edits the whole application is built from.…, Append an item to a document list., Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the… (+57 more)

### Community 92 - "RenderWindow"
Cohesion: 0.07
Nodes (23): ndarray, to_rgba16(), to_rgba8(), A render, finished or under way, and everything needed to show and save it., RenderResult, _duration(), ndarray, Path (+15 more)

### Community 93 - "test_elements.py"
Cohesion: 0.08
Nodes (19): Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., A matcap has no light to aim, so the Light group goes -- and its space. The…, Run the refresh the shared timer would have run., ``self._mode`` is ``mode``; the group called Mode settles for a number. (+11 more)

### Community 94 - "Mesh"
Cohesion: 0.03
Nodes (102): auto_smooth(), compute_vertex_normals(), _corner_groups(), _face_cross(), _gathered(), _group_normals(), Mesh, ndarray (+94 more)

### Community 95 - "Measurement"
Cohesion: 0.10
Nodes (13): Measurement, MeasurementStore, ndarray, Named point-to-point measurements and their presentation options., The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units. (+5 more)

### Community 96 - "ReflowLayout"
Cohesion: 0.18
Nodes (6): QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Lays its items out in as many equal columns as the width allows., ReflowLayout

### Community 97 - "state.py"
Cohesion: 0.05
Nodes (52): concatenated(), loose_parts(), Several meshes as one, in the coordinates they already stand in. The units are…, The triangles of ``mesh`` named by index, with only the vertices they use., The triangles of ``mesh`` gathered into the pieces that touch, largest first.…, submesh(), OrientationSettings, Enum (+44 more)

### Community 98 - "MeshBuffers"
Cohesion: 0.10
Nodes (9): MeshBuffers, Vertex/index buffers for one mesh, bound through a single VAO., Forget the contents without releasing the buffer objects., Replace the model: the whole scene as one mesh, and the objects it is made of.…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are…, Every buffer standing for the model, for the passes that draw them all alike. (+1 more)

### Community 99 - "FormStore"
Cohesion: 0.18
Nodes (4): FormStore, An ordered, named collection of forms, like the other stores., A name for a new form of this recipe, numbered past any it already has. A form…, test_a_form_store_names_forms_past_the_ones_it_has()

### Community 100 - "clone.py"
Cohesion: 0.05
Nodes (67): QAbstractButton, QLineEdit, QSlider, _begin(), can_clone(), clone(), _clone_button(), _clone_check() (+59 more)

### Community 101 - "skin_detail.py"
Cohesion: 0.17
Nodes (20): burley_marginal(), burley_profile(), cellular(), diffusion_lut(), _fade(), fbm(), ndarray, Procedural skin micro-relief and the pre-integrated diffusion table. Reference… (+12 more)

### Community 102 - "Path"
Cohesion: 0.11
Nodes (13): A flat-shaded mesh, every triangle with its own three corners. Corners are not…, Path, Apply a matcap image, reporting unreadable files to the user., Pick up whatever was last being worked on, if that was asked for. A session…, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window. In the…, Read a model file off the window, then hand it to ``adopt`` here. (+5 more)

### Community 103 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.09
Nodes (11): Record the finished drag as a single undo step., Record the turn as one undo step., Alt forces the camera gesture, whichever tool is armed., Record the finished drag as one step, or read a press as a selection., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Make the object under the cursor the active one., Record the finished pull as one step, or read a press as a selection. (+3 more)

### Community 105 - "PointEdit"
Cohesion: 0.14
Nodes (9): _pull_point(), _AxisBox, PointEdit, QDoubleSpinBox, QWidget, The small controls that are not sliders: a swatch, and a point in space., Three boxes for one point in space. Keyboard tracking is off, so a typed number…, Match the arrows to the size of the thing being moved. (+1 more)

### Community 106 - "plane_count"
Cohesion: 0.12
Nodes (12): _along(), lattice_fineness(), plane_count(), Where a detail setting sits on its slider, 0 to 1., How much finer than usual a detail setting asks the lattice to be. One at the…, How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., How much of a turn in the surface one plane covers, in degrees. Linear in…, How many planes a mode fitted to the model keeps. The climb from two planes to… (+4 more)

### Community 107 - "ColorButton"
Cohesion: 0.17
Nodes (6): _pull_swatch(), ColorButton, QColor, QSize, A swatch that opens a colour picker. Colours are exchanged as 0-1 RGB tuples,…, Open the picker, as a click on the swatch does.

### Community 108 - "test_tasks.py"
Cohesion: 0.17
Nodes (16): app(), fixture, Work run off the window, and the cards that show it running., Turn the event loop until ``until()`` says so, or give up., runner(), _spin(), test_a_result_arriving_after_the_cross_is_thrown_away(), test_a_task_called_off_while_waiting_never_starts() (+8 more)

### Community 109 - "trace_sample"
Cohesion: 0.13
Nodes (32): The two-lobe skin specular, ``f cos``, and its mixture density, in the spec…, One sample of pixel ``(px, py)``. Returns ``(rgb, alpha, albedo, normal, depth,…, _skin_spec(), trace_sample(), ggx_d(), ggx_eval(), ggx_sample(), material_alpha() (+24 more)

### Community 110 - "DockTitle"
Cohesion: 0.15
Nodes (7): QToolButton, DockTitle, QSize, QWidget, The bar across the top of a dock: a switch, a name and two buttons., As tall as the bar really is. A dock puts the panel directly below its title…, StandardPixmap

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - "Path"
Cohesion: 0.07
Nodes (21): setter, Path, Take the display unit from the file when the format declares one. Only glTF…, Set the active matcap, or fall back to the built-in one., Write the document, and whatever the window says its layout is. The layout…, Write every skin made here beside the session; see :mod:`rig_file`., A file for ``obj`` next to the session, named for both., Open a session: its models, then everything it says about them. ``sources`` are… (+13 more)

### Community 113 - "Task"
Cohesion: 0.06
Nodes (24): _outcome(), ProgressCard, Any, BaseException, QObject, QPainter, QWidget, T (+16 more)

### Community 114 - "History"
Cohesion: 0.17
Nodes (14): History, A bounded undo/redo stack., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch(), test_commands_carry_their_channel_and_name() (+6 more)

### Community 115 - "PathTraceSettings"
Cohesion: 0.11
Nodes (22): _copy(), PathTracePreset, PathTraceSettings, Keep loaded settings finite and inside what the panel and the tracer allow., A deep copy of nested dataclasses, cheap enough for every render., What a preset sets: how much work a render does, never its size or look., _resolve(), What of the settings a rendered picture shows, as a key. The viewport preview… (+14 more)

### Community 116 - "test_open_files.py"
Cohesion: 0.12
Nodes (13): opens_as(), What a file opens as, by its suffix: a model, a session, a matcap or an HDRI., app(), opened(), fixture, parametrize, Files arriving from outside: the command line, a drop, or the desktop's "Open…, One offscreen Qt application for the run; see test_film_recorder. (+5 more)

### Community 117 - "sampler.py"
Cohesion: 0.16
Nodes (24): bounce_set(), _direction_numbers(), hash32(), hash_combine(), hash_float(), _laine_karras(), nested_uniform_scramble(), pixel_seed() (+16 more)

### Community 118 - "Session"
Cohesion: 0.12
Nodes (18): _coerce(), decode(), encode(), Any, T, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``. (+10 more)

### Community 119 - ".process"
Cohesion: 0.14
Nodes (14): check_size(), NeuralError, NeuralPoisonedError, RuntimeError, Raise if the engine cannot take a ``width`` by ``height`` picture., Neural Rendering could not be done, and says why., The engine hung or faulted; it is not called again until the application…, Load the engine and check it speaks this module's ABI; binds no GPU yet. (+6 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.09
Nodes (30): QPointF, project_visible(), Handle, ndarray, QColor, QFont, QPainter, QRectF (+22 more)

### Community 121 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 122 - "ArmatureStore"
Cohesion: 0.16
Nodes (5): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied., test_an_armature_survives_a_session_round_trip()

### Community 123 - "path_trace.py"
Cohesion: 0.05
Nodes (37): BucketOrder, ClaySettings, ColorSettings, DenoiserBackend, DenoiserQuality, FilmSettings, LensSettings, LightPathSettings (+29 more)

### Community 124 - "obj_loader.py"
Cohesion: 0.22
Nodes (14): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), ndarray, Minimal, dependency-free Wavefront OBJ reader. Only the geometry statements a…, Resolve ``v``, ``v/vt``, ``v//vn`` or ``v/vt/vn`` corners to 0-based pairs.… (+6 more)

### Community 125 - "FakeEngine"
Cohesion: 0.10
Nodes (28): NeuralSettings, NVIDIA DLSS 5 Neural Rendering, run on the developed picture after denoising.…, NeuralBridge, The engine's controls for a still picture with ``settings``. A still has no…, The engine, loaded once, and the calls into it. ``library`` stands in for the…, Look for the engine in ``folder`` (from the preferences), or only where it…, render_parameters(), set_engine_dir() (+20 more)

### Community 126 - "forms.py"
Cohesion: 0.05
Nodes (57): A graph of named points under the form, and the wire it stands for. An armature…, DegenerateHullError, ValueError, The points are flat, collinear or too few to hold any volume., build_freeform(), _centre(), form_landmark_title(), form_spec() (+49 more)

### Community 127 - "SectionPanel"
Cohesion: 0.18
Nodes (6): Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 128 - "._upload_sculpt"
Cohesion: 0.12
Nodes (7): The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, Cut the stand-in on a thread; see :meth:`_upload_sculpt`., Show the recording as a task, its bar the stages landed so far., The cross on the recording's card: the film is dropped, the switch too., A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on.

### Community 129 - "._sync_scene"
Cohesion: 0.09
Nodes (10): Cut the mesh with each section plane and expand the result to strokes., The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, A skeleton changed: redraw it, and let the skin's body map follow its bones., What the renderer draws: each object as it stands, AutoSmoothed if asked., ``mesh`` shaded by the object's smoothing groups, found once and kept. The…, The whole scene as one mesh, as the planes and the skin tracer read it. The…, Tell the renderer what the skin's body map is made from now., Hand the renderer a re-posed model and nothing else. For the frames of a pose… (+2 more)

### Community 130 - "colour.py"
Cohesion: 0.19
Nodes (19): _aces(), develop(), develop_image(), _encode(), linear_to_display(), _neutral(), device, From scene light to pixel values: exposure, the view transform, and the… (+11 more)

### Community 131 - "AnnotateTool"
Cohesion: 0.08
Nodes (21): AnnotateMode, AnnotationSettings, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a… (+13 more)

### Community 132 - "ExportLook"
Cohesion: 0.10
Nodes (13): ExportLook, What the frames are to look like, as against what they are of. Laid over the…, Which of the things drawn over the model belong in the frames., ``base`` with this export's choices laid over it., The line burned into the corner of the frame for ``stage``. Counted off the…, FakeViewport, QImage, Pump the event loop until ``done()`` or the clock runs out. (+5 more)

### Community 133 - "load_mesh"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

### Community 134 - "preview"
Cohesion: 0.29
Nodes (7): app(), gallery_settings(), preview(), fixture, The gallery's list on a settings file of the tests' own, empty to begin with., One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "elements/__init__.py"
Cohesion: 0.06
Nodes (47): One dock per panel, with a bar of its own across the top. Every panel is its…, QFormLayout, A titled frame that folds away behind its own bar. Every group of controls in…, The rows inside the frame. ``layout()`` is the frame's own, which stacks the…, The row layout the frames are filled with., Whether a group that goes dead folds away or merely greys out. Turning it back…, set_fold_disabled(), The widgets the panels are built out of, and the rules they follow. Four ideas,… (+39 more)

### Community 136 - "paths.py"
Cohesion: 0.19
Nodes (18): available_environments(), available_matcaps(), _bundled_root(), cache_dir(), environment_dir(), matcap_dir(), model_dir(), Path (+10 more)

### Community 137 - "Release"
Cohesion: 0.11
Nodes (19): QRunnable, The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, _CheckTask, is_skipped(), QObject, QWidget (+11 more)

### Community 138 - "Film"
Cohesion: 0.13
Nodes (13): ndarray, Path, Writing a render as OpenEXR: the light as it is, and its passes as layers. An…, Write ``layers`` -- ``"RGBA"`` first, then passes by name -- to ``path``.…, Every channel of an EXR by name, as the file groups them; for tests., read_exr_channels(), write_exr(), Film (+5 more)

### Community 139 - "Command"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 140 - "VideoError"
Cohesion: 0.09
Nodes (19): _encode_arguments(), _encoders(), _FFmpegWriter, _no_window(), ndarray, RuntimeError, An export that could not be written, said in words for the artist., Which encoders this ffmpeg was built with. Asked once, because a build without… (+11 more)

### Community 141 - "RenderController"
Cohesion: 0.12
Nodes (12): enhance_key(), BaseException, QObject, Starts, watches and finishes renders for the Render panel and window., Render ``inputs`` (a :class:`~refview.trace.scene.TraceInputs`), stopping any…, Denoise a render's film now, with the settings as they are., Run DLSS 5 Neural Rendering on a render as it is developed now., Enhance again once the colour or Neural Rendering sliders stop moving. (+4 more)

### Community 142 - "vec.py"
Cohesion: 0.13
Nodes (26): disc_sample(), ``(direction, radiance / pdf, pdf)`` toward a point of light ``i``; pdf 0 for a…, ndarray, The parameter row and the region multipliers for…, skin_parameters(), add(), basis(), clamp() (+18 more)

### Community 143 - "MatcapPreview"
Cohesion: 0.08
Nodes (15): QMenu, MatcapPreview, Path, QRect, QSize, QWidget, A matcap on a sphere, which is also how the matcap is graded., Redraw from the settings, which something else has changed. (+7 more)

### Community 144 - "._picker"
Cohesion: 0.08
Nodes (14): ndarray, Rub out the stroke points under the eraser, live., Turn the lights by how far the drag has come: across about the vertical, up in…, Take hold of a node, to move it, resize it, or just to select it. This works…, Apply the drag live, so the artist sees the wire bend as they pull it., Take hold of a landmark, to move it or just to say which one it is., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit. (+6 more)

### Community 145 - "in_flight"
Cohesion: 0.19
Nodes (5): in_flight(), Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model., Take a copied control out of whichever hand-built panel holds it.

### Community 146 - "shader_files.py"
Cohesion: 0.19
Nodes (9): _expand(), load_glsl(), Reading the GLSL out of :file:`render/glsl`. Each program's source lives in a…, The source of ``name`` with its includes, constants and defines worked in., _read(), GLSL sources for the viewport, read from :file:`render/glsl`. A handful of…, Skin BRDF and bounded-depth light transport, shared by preview and refinement.…, The GLSL on disk: its includes and constants, and that every program is whole. (+1 more)

### Community 147 - "OpenRequests"
Cohesion: 0.15
Nodes (8): Application, OpenRequests, Path, QApplication, The Qt application, listening for the desktop's way of handing over a file., Files the desktop asked the viewer to open, kept until there is a window. On…, Open ``path`` in the window, or hold it until there is one., Name the window files go to, and hand over any that came early.

### Community 148 - "matcap_preview.py"
Cohesion: 0.11
Nodes (17): _angle(), _clone_preview(), grade(), _pull_preview(), _push_preview(), ndarray, The matcap itself, as the control for grading it. A matcap is a picture of a…, Point the preview at the settings it edits. The object itself, not a copy: this… (+9 more)

### Community 149 - "Preset"
Cohesion: 0.29
Nodes (4): Preset, An ordered set of landmarks and the armature they build., The landmarks worth asking for under these choices. With mirroring on the…, The midline landmarks, which are what the median plane is fitted to.

### Community 150 - "test_body_regions.py"
Cohesion: 0.29
Nodes (12): _column(), _figure_bones(), ndarray, Where on the body the skin is: bones, height bands, the map, and the settings., A thin column standing from the ground to ``height``., _region(), test_height_bands_follow_the_canon_and_are_soft_at_the_edges(), test_points_go_to_the_region_of_the_nearest_bone_and_blend_between() (+4 more)

### Community 151 - "load_obj"
Cohesion: 0.24
Nodes (13): _load_generic(), load_obj(), ObjLoadError, Line-by-line reader for files the fast path declines., Raised when a file cannot be interpreted as an OBJ mesh., Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, OBJ parsing: normals, triangulation and index handling., test_empty_file_is_rejected() (+5 more)

### Community 152 - "EnvironmentMap"
Cohesion: 0.05
Nodes (34): EnvironmentMap, An HDRI read and made ready for the renderer. Built off the thread., What the radiance is multiplied by so that :attr:`peak` comes out at one. One…, A turn about the vertical axis, as a 3x3 matrix., rotation_y(), environment_matrix(), light_rig(), LightRig (+26 more)

### Community 153 - "stl_loader.py"
Cohesion: 0.22
Nodes (13): _ascii_corners(), _binary_corners(), load_stl(), ndarray, Path, Binary and ASCII STL reader. STL stores three loose corners per facet and…, Raised when a file cannot be interpreted as an STL mesh., Load ``path``, choosing the binary or ASCII reader by inspection. (+5 more)

### Community 154 - "NeuralService"
Cohesion: 0.17
Nodes (10): NeuralInfo, NeuralService, Future, ndarray, Whether Neural Rendering can run here, and on what., The one thread Neural Rendering runs on, and the engine it has loaded. One…, Find out, on the service thread, whether the engine is here. The future holds a…, What the last probe found, or ``None`` before one has finished. (+2 more)

### Community 155 - "PanelDock"
Cohesion: 0.18
Nodes (5): QDockWidget, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top., QWidget, Dress the tabs once Qt has finished rearranging them.

### Community 156 - "palette.py"
Cohesion: 0.11
Nodes (18): css(), outline(), QColor, The colours the hand-drawn elements paint with. Kept apart from…, Draw the hairline that separates a control from the panel. One line, the same…, A colour as a style sheet function, for the parts Qt draws., Change the one colour that is not grey, everywhere at once. The hand-painted…, set_accent() (+10 more)

### Community 157 - "jit.py"
Cohesion: 0.12
Nodes (15): camera_ray(), filter_offset(), device, Primary rays: the pixel filter, the lens, and the two projections. The pixel…, The ray through film position ``(x, y)`` in pixels, top-left origin., _pass(), The built-in denoiser: an edge-avoiding a-trous wavelet filter (Dammertz et al.…, available() (+7 more)

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

### Community 162 - "mesh_io.py"
Cohesion: 0.24
Nodes (10): Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets, render owns every GL call (+2 more)

### Community 163 - "neural.py"
Cohesion: 0.28
Nodes (7): _complete(), engine_dir(), missing_reason(), Path, NVIDIA DLSS 5 Neural Rendering on a finished picture, through Merserk's…, Why no engine was found, in words that say what to do., The folder holding all three engine files, or ``None`` when there is none. The…

### Community 164 - "Human Skin renderer"
Cohesion: 0.25
Nodes (7): Human Skin renderer, Marks and body regions, Material and transport, Scheduling, precision and compatibility, Surface, The HDRI, Where to change it

### Community 165 - ".__init__"
Cohesion: 0.24
Nodes (5): Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo, test_section_rail_paints_its_label()

### Community 166 - "SkinRefinement"
Cohesion: 0.12
Nodes (8): Have the body map for ``source`` built off the thread, and take it when it…, Restart on any image change; never mix a moving preview into the sum., RefinementClock, SkinRefinement, An RGBA16F volume, trilinear, for detail sampled by world position. Sampled by…, Texture3D, test_history_resets_on_changes_and_held_navigation(), test_worker_failure_leaves_a_preview_and_stops_repainting()

### Community 167 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 168 - "._place_armature_node"
Cohesion: 0.33
Nodes (3): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 169 - "_Export"
Cohesion: 0.29
Nodes (4): The engine's controls for one frame, as its ABI version 6 lays them out. Each…, RenderParameters, _Export, A function as a DLL exports it: callable, and taking ``argtypes`` and…

### Community 170 - "Reflow"
Cohesion: 0.33
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 171 - "test_trace_bvh.py"
Cohesion: 0.33
Nodes (12): _cast(), _geometry(), The path tracer's tree and rays, against brute force., _rays(), _soup(), _sphere_geometry(), test_a_ghost_is_hit_as_often_as_it_is_solid(), test_nearest_hit_matches_brute_force_on_a_soup() (+4 more)

### Community 172 - "Path tracer"
Cohesion: 0.13
Nodes (14): Colour, Compilation, Denoisers, DLSS 5 Neural Rendering, Human Skin, Integrator, Jobs, Lights (+6 more)

### Community 173 - "TriangleIndex"
Cohesion: 0.09
Nodes (28): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Box the leaves up, coarsest level first and the leaves themselves last., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the… (+20 more)

### Community 174 - "TaskRunner"
Cohesion: 0.25
Nodes (6): BakeEdit, Dressing an object in a skin made for a skeleton, or taking it off. One step…, Writing an object's turn and scale into its mesh -- Reset XForm -- or undoing…, SkinEdit, Runs work off the GUI thread and keeps the window told. :attr:`started` and…, TaskRunner

### Community 175 - "make_switch"
Cohesion: 0.28
Nodes (6): make_switch(), QCheckBox, Put a show/hide switch at the left of the bar and return it., A square that is on or off, and is clickable all over. A check box decides…, The square that shows or hides what a panel draws. One is kept on each dock's…, Switch

### Community 176 - "picking.py"
Cohesion: 0.10
Nodes (30): _cross(), Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Row-wise cross product, without :func:`numpy.cross`'s axis shuffling., Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface. (+22 more)

### Community 177 - ".reset"
Cohesion: 0.22
Nodes (5): QSettings, Bring the first panel to the front of the tab strip., The part of the layout Qt cannot describe., Write the whole layout, ours and Qt's, into the settings., Put every dock back where it started, now. Not "forget the saved layout and…

### Community 178 - "CHANGELOG.md"
Cohesion: 0.25
Nodes (7): Shift-snapped orbiting (1.1.0), Cross-section tool (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding

### Community 179 - ".dress_tabs"
Cohesion: 0.29
Nodes (5): QTabBar, Hang a show/hide switch on every dock tab that wants one. A dock stacked behind…, The panel whose dock is called ``title``, if there is one., Let a strip of tabs keep its names, and scroll if they do not fit. Ten panels…, _widen()

### Community 180 - "step"
Cohesion: 0.25
Nodes (8): quad(), The reason for reading where the surface is and not only which way. Both faces…, The limit the clustered fits exist to lift, stated as a fact., Add one flat quad, with its own vertices, to a mesh under construction., Two broad faces both looking straight up, one raised above the other. The case…, step(), test_reading_the_normals_alone_cannot_tell_that_step_apart(), test_two_faces_looking_the_same_way_stay_two_planes()

### Community 181 - "VideoSettings"
Cohesion: 0.09
Nodes (23): ffmpeg_path(), open_writer(), Path, How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds. (+15 more)

### Community 182 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 183 - "lumpy"
Cohesion: 0.25
Nodes (8): lumpy(), A form with real planes in it, and more than one facing the same way., The coefficients have to reach the fit, and reaching it has to show. Two planes…, The fit and the shader have to agree, or the boundaries drawn are not the…, Narrow it and only the flattest surface has a say; widen it and the rounded…, test_a_coefficient_of_zero_takes_the_term_out_of_the_shader_too(), test_leaning_on_position_breaks_a_form_up_as_well_as_down(), test_the_flat_span_says_how_much_of_the_form_counts_as_flat()

### Community 184 - "._build"
Cohesion: 0.28
Nodes (4): Lay one length of wire earlier or later, as one undoable step., The armature the clay is being built on, or ``None``. An index past the end of…, Put the clay on all of the wire, or take it off all of it., Write which lengths of wire take clay, as one undoable step.

### Community 185 - "lzw"
Cohesion: 0.36
Nodes (5): lzw(), The GIF flavour of LZW: variable-width codes, packed low bit first. Straight…, A plain GIF LZW decoder, for testing the encoder against. Deliberately written…, TestLzw, unlzw()

### Community 186 - "ModelPanel"
Cohesion: 0.06
Nodes (14): ModelPanel, QTreeWidgetItem, Bind the panel to the viewport's transform tool., Reflect the tool state without re-emitting the toggle., Choose the gesture, from the menu or a key., Rebuild the tree from the store, with the active object current., Offer every object the active one could hang from., The objects whose rows are selected, in list order. (+6 more)

### Community 187 - "ui/preferences.py"
Cohesion: 0.11
Nodes (15): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version(), current(), forget(), QSettings, _qcolor(), Where the preferences are kept, and what happens when one changes.… (+7 more)

### Community 188 - "MeasureTool"
Cohesion: 0.10
Nodes (14): MeasurementSettings, How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., MeasureTool, Handle, ndarray, Two-click measuring, plus dragging the endpoints of an unlocked measurement., The nearest grabbable endpoint under the cursor, if any. Only unlocked, visible… (+6 more)

### Community 189 - "ThreadWakeLock"
Cohesion: 0.22
Nodes (4): Hold sleep off, or stop holding it, whichever is not already true., Drop the request, if one is out. Safe to call more than once., Holds sleep off from a thread of its own, for as long as some work runs. For a…, ThreadWakeLock

### Community 190 - "test_render_panel.py"
Cohesion: 0.18
Nodes (4): app(), panel(), fixture, The Render panel and the Render window, offscreen.

### Community 191 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 192 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 193 - "ui/hotkeys.py"
Cohesion: 0.05
Nodes (56): QKeySequenceEdit, QShortcut, ask_for(), assign(), command_for(), control_of(), decorate(), describe() (+48 more)

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

### Community 198 - "_height_of"
Cohesion: 0.38
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 199 - ".install"
Cohesion: 0.29
Nodes (6): QApplication, Put the rule in place for every switch in the application., The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter., test_a_switch_answers_a_press_anywhere_on_its_face(), test_alt_is_left_alone_so_a_switch_can_still_be_copied()

### Community 200 - ".new_custom_panel"
Cohesion: 0.29
Nodes (4): _number_in(), An empty panel of the artist's own, docked on the right. A dock put away…, Take a parked dock back out under ``key``, emptied and renamed., The number at the end of a custom panel's key, or nought.

### Community 201 - "reflow.py"
Cohesion: 0.33
Nodes (4): Orientations, A layout that turns a column of groups into columns when given the width. A…, Whether an item asked to be given more height than it needs., _wants_height()

### Community 202 - "._on_bone_toggled"
Cohesion: 0.29
Nodes (4): QListWidgetItem, Catch the selection a click on a checkbox is about to collapse. Qt selects a…, Which bones of the armature the picked-out rows stand for., Take lengths of wire out of the clay, or put them back. A tick on a row that…

### Community 203 - "bent_plate"
Cohesion: 0.20
Nodes (10): angle_deg(), bent_plate(), ndarray, A plate creased down the middle, and which column each vertex is in. Flat to…, Vertices on a turn are ambiguous about their plane, so they are quieted. The…, Splitting a broad flat by place must not invent a turn in it. The plate below…, How many planes have another plane pointing very nearly where they do., same_facing() (+2 more)

### Community 204 - ".plane_span_deg"
Cohesion: 0.33
Nodes (3): Roughly how much of a turn one of those planes covers, in degrees., The plane size of whichever mode is running., Roughly how much of a turn one of those planes covers, in degrees.

### Community 205 - "_WindowsBackend"
Cohesion: 0.25
Nodes (5): ``SetThreadExecutionState``: a flag on this thread, not a handle. The flags…, _WindowsBackend, skipif, The flag the viewer sets is the one Windows reports back afterwards., test_windows_really_sets_the_execution_state()

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

### Community 213 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 214 - "FrameTarget"
Cohesion: 0.07
Nodes (40): A progress for one part of the work, mapped onto ``[start, end]`` of this one.…, current_framebuffer(), FrameTarget, Offscreen render targets used by the high-quality, ghost and smoothing passes.…, The framebuffer object bound right now -- Qt's, in a widget., The whole frame, drawn offscreen so it can be smoothed on the way out. A colour…, How many samples the framebuffer bound right now is drawing with. One where…, sample_count() (+32 more)

### Community 216 - "save_obj"
Cohesion: 0.67
Nodes (3): Path, Write ``mesh`` as a plain OBJ: positions, normals and triangles. What a session…, save_obj()

### Community 217 - "new_stacks"
Cohesion: 0.67
Nodes (3): new_stacks(), ndarray, A traversal stack for one thread: node rows and their entry distances.

### Community 218 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

## Knowledge Gaps
- **27 isolated node(s):** `refview`, `FunctionTable`, `OptixDenoiserOptions`, `OptixDenoiserGuideLayer`, `OptixDenoiserLayer` (+22 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `SceneObject`, `load_mesh`, `trace/scene.py`, `ExportLook`, `pose_panel.py`, `RenderSettings`, `auto_skin`, `ViewerState`, `Skeleton`, `PrimaryForm`, `test_body_regions.py`, `load_obj`, `PoseTool`, `stl_loader.py`, `core/__init__.py`, `plane_volume.py`, `FilmRecorder`, `convex.py`, `mesh_io.py`, `test_plane_clusters.py`, `test_trace_bvh.py`, `Rig`, `TriangleIndex`, `picking.py`, `body_regions.py`, `settings.py`, `step`, `RegionSource`, `lumpy`, `test_skeleton.py`, `test_forms.py`, `FormTool`, `cube`, `test_objects.py`, `test_skin.py`, `test_plane_solids.py`, `bent_plate`, `test_trace_integrator.py`, `core/environment.py`, `FrameTarget`, `save_obj`, `main_window.py`, `state.py`, `MeshBuffers`, `FormStore`, `Path`, `plane_axes`, `Path`, `obj_loader.py`, `forms.py`?**
  _High betweenness centrality (0.177) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `test_preferences.py`, `Viewport`, `SceneObject`, `MainWindow`, `auto_skin`, `RenderController`, `Armature`, `SurfacePicker`, `PrimaryForm`, `CameraPanel`, `test_body_regions.py`, `PoseTool`, `mesh_io.py`, `.__init__`, `TaskRunner`, `body_regions.py`, `test_matcap_preview.py`, `test_render_panel.py`, `.__init__`, `test_objects.py`, `test_skin.py`, `test_workspace_layout.py`, `test_custom_panels.py`, `section`, `panel`, `._commit_objects`, `test_forms_panel.py`, `ArmatureTool`, `render_controller.py`, `MatcapPanel`, `overlay.py`, `main_window.py`, `RenderWindow`, `test_elements.py`, `Mesh`, `Measurement`, `state.py`, `Path`, `Session`, `ViewportOverlay`, `FakeEngine`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `._upload_sculpt`, `._sync_scene`, `test_preferences.py`, `AnnotateTool`, `ExportLook`, `trace/scene.py`, `MainWindow`, `SurfacePicker`, `Armature`, `ViewerState`, `._picker`, `PrimaryForm`, `PoseTool`, `.stage_images`, `.paintGL`, `FilmRecorder`, `.__init__`, `._place_armature_node`, `ExportVideoDialog`, `FilmExport`, `MeasureTool`, `.__init__`, `FormTool`, `test_objects.py`, `ObjectTool`, `._place_joint`, `NavigationController`, `._commit_node_drag`, `._place_form_landmark`, `.film`, `ArmatureTool`, `render_controller.py`, `overlay.py`, `main_window.py`, `Mesh`, `Measurement`, `.mouseReleaseEvent`, `ViewportOverlay`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Are the 60 inferred relationships involving `Mesh` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Mesh` has 60 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `OverlayParts`) actually correct?**
  _`ViewerState` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Skeleton` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Skeleton` has 9 INFERRED edges - model-reasoned connections that need verification._