# Graph Report - reference-viewer  (2026-09-24)

## Corpus Check
- 220 files · ~578,701 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 6824 nodes · 16153 edges · 216 communities (212 shown, 4 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 836 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cf7ce249`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- form_group
- test_preferences.py
- update_check.py
- Viewport
- SceneObject
- trace/scene.py
- MainWindow
- Stroke
- GifWriter
- core/camera.py
- RenderSettings
- naming.py
- Cuda
- MeshBuffers
- Armature
- environment.yml
- ViewerState
- Skeleton
- framebuffer.py
- CameraPanel
- PosePanel
- ShaderProgram
- PoseTool
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- Writer
- Bounds
- plane_volume.py
- ControlsWindow
- DenoiseService
- ShadingPanel
- FilmRecorder
- test_camera.py
- test_plane_clusters.py
- WakeLock
- integrator.py
- lights.py
- CustomPanel
- film_export.py
- RenderJob
- Camera
- skeleton.py
- ValueSlider
- gltf_loader.py
- ExportVideoDialog
- trace/skin.py
- landmarks.py
- Agent Graph-First Instructions
- body_regions.py
- Coefficients
- test_matcap_preview.py
- test_armature.py
- ArmaturePanel
- BodyRegionSettings
- HotkeyMap
- FilmExport
- FormsPanel
- PlanesPanel
- test_skeleton.py
- Progress
- Workspace
- RenderPanel
- test_forms.py
- application.py
- render_panel.py
- PointEdit
- PrimaryForm
- ShadingMode
- test_objects.py
- test_skin.py
- test_plane_solids.py
- ObjectTool
- MatcapSettings
- ArmatureTool
- SkinSettings
- load_matcap_pixels
- test_custom_panels.py
- SkinEdit
- core/preferences.py
- core/environment.py
- NavigationController
- ._apply
- ._commit_objects
- test_forms_panel.py
- PlaneSettings
- viewport.py
- ViewportRenderPreview
- MatcapPanel
- AnnotatePanel
- Frame
- main_window.py
- RenderWindow
- test_elements.py
- Mesh
- MeasurementStore
- ReflowLayout
- OrientationSettings
- ColorButton
- FormStore
- clone.py
- skin_detail.py
- Path
- plane_axes
- .mouseReleaseEvent
- ._delete_selected
- OverlayParts
- SectionSettings
- test_tasks.py
- materials.py
- DockTitle
- test_reflow.py
- Path
- Task
- History
- PathTraceSettings
- refview/__init__.py
- sampler.py
- Session
- SetAttributes
- ViewportOverlay
- test_hotkeys.py
- ArmatureStore
- VideoSettings
- .refresh_list
- Reflow
- Landmark
- SectionPanel
- ._upload_sculpt
- ._sync_scene
- colour.py
- AnnotateTool
- ExportLook
- obj_loader.py
- preview
- ._build
- paths.py
- Release
- Film
- Command
- ._advance_pending
- RenderController
- vec.py
- MatcapPreview
- ._picker
- ._carrying_a_copy
- ._build
- LightingMode
- ._turn
- SurfacePicker
- test_body_regions.py
- ContourShadingSettings
- mesh_renderer.py
- .refresh_list
- ._focused_form
- RenderView
- render_window.py
- jit.py
- shader_files.py
- .paintGL
- ._build_objects
- wakelock.py
- .column_of
- panel
- Human Skin renderer
- .__init__
- FrameTarget
- coarse_lattice
- ._place_armature_node
- sample_count
- _height_of
- test_trace_bvh.py
- Path tracer
- README.md
- ._active_changed
- test_annotation.py
- raycast_mesh
- Path
- section_segments
- app
- step
- open_writer
- section.py
- HotkeyBinder
- .refresh
- lzw
- ModelPanel
- ui/preferences.py
- MeasureTool
- ThreadWakeLock
- test_render_panel.py
- release.yml
- stroke_renderer.py
- ui/hotkeys.py
- .__init__
- .refresh_list
- cube
- test_workspace_layout.py
- ask_for
- ._place_joint
- ._place_form_landmark
- .source_mesh
- StrokeBuffers
- test_leaning_on_position_breaks_a_form_up_as_well_as_down
- CHANGELOG.md
- _WindowsBackend
- lumpy
- _MacBackend
- .refresh_list
- ._back_point
- ._commit_node_drag
- FormRun
- .selected_objects
- _NameOnlyDelegate
- box
- coarse_lattice

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 250 edges
2. `ViewerState` - 200 edges
3. `Viewport` - 167 edges
4. `Skeleton` - 114 edges
5. `Camera` - 113 edges
6. `MainWindow` - 103 edges
7. `RenderSettings` - 93 edges
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

## Communities (216 total, 4 thin omitted)

### Community 0 - "form_group"
Cohesion: 0.14
Nodes (14): The preferences as they stand. Treat as read-only; use :meth:`set`., QWidget, Fill in the groups. A switch with nothing to put in the caption column is given…, Every command with its keys, each key a box that takes one keystroke. The list…, The one button that is not a preference, and what the window is for., Say what the view is really drawing with, beside what was asked for. A sample…, Put one field back into the store, which applies and saves it., Pull every control back into line with the store. Run when the window is built,… (+6 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.07
Nodes (44): _clamp(), Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, Pull anything out of range back into it. The window cannot produce these…, Read the preferences off the machine. Never raises., app(), model() (+36 more)

### Community 2 - "update_check.py"
Cohesion: 0.10
Nodes (31): check_for_update(), fetch_latest_release(), is_newer(), _macos_root_certificates(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and… (+23 more)

### Community 3 - "Viewport"
Cohesion: 0.05
Nodes (20): QOpenGLWidget, Film, Free every GL object while the owning context is still current., Arm one tool, disarming the rest. Only one gesture can own the left button, so…, Drop whatever gesture is half-finished, without disarming the tool., One of the renderer's :data:`~refview.render.mesh_renderer.ANTIALIASING_MODES`., Renders the scene and turns mouse gestures into camera and tool actions., Slide the view so a point sits at the centre, keeping the angle. (+12 more)

### Community 4 - "SceneObject"
Cohesion: 0.07
Nodes (25): ObjectSettings, ObjectStore, ndarray, Snapshot, An angle in (-180, 180], with the floating-point dust brushed off., What a parent's state means for its children, and how the tools scale. Each is…, One model in the scene. Three meshes are kept, as the viewer kept them when…, Drop the derived meshes, after the rest mesh has been replaced. (+17 more)

### Community 5 - "trace/scene.py"
Cohesion: 0.06
Nodes (52): IntEnum, filter_table(), ndarray, The inverse cumulative distribution of a separable filter, as offsets in…, empty_geometry(), flatten(), Geometry, new_stacks() (+44 more)

### Community 6 - "MainWindow"
Cohesion: 0.05
Nodes (17): MainWindow, QMainWindow, The document this window edits., Open the window that writes the film of a form's making to a file. Nothing is…, Keep the menu entry agreeing with the panel's own checkbox., Put every panel button and menu entry where the tools now stand. Only one tool…, Swap between the eraser and the drawing mode it was called from., Path-trace the view, at the Render panel's size, into the Render window. (+9 more)

### Community 7 - "Stroke"
Cohesion: 0.08
Nodes (16): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An empty stroke carrying the current brush., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface. (+8 more)

### Community 8 - "GifWriter"
Cohesion: 0.08
Nodes (27): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), palette_of(), ndarray, Path (+19 more)

### Community 9 - "core/camera.py"
Cohesion: 0.04
Nodes (68): Quat, Quat4, _distance_or_none(), Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`. (+60 more)

### Community 10 - "RenderSettings"
Cohesion: 0.05
Nodes (54): EnvironmentMap, An HDRI read and made ready for the renderer. Built off the thread., What the radiance is multiplied by so that :attr:`peak` comes out at one. One…, A turn about the vertical axis, as a 3x3 matrix., rotation_y(), environment_matrix(), light_rig(), LightRig (+46 more)

### Community 11 - "naming.py"
Cohesion: 0.10
Nodes (30): QTabBar, _asked(), caption_for(), element_id(), forget(), _free(), _from_id(), name_tree() (+22 more)

### Community 12 - "Cuda"
Cohesion: 0.05
Nodes (32): FunctionTable, OptixDenoiserGuideLayer, OptixDenoiserLayer, OptixDenoiserOptions, OptixDenoiserParams, OptixDenoiserSizes, OptixDeviceContextOptions, OptixImage2D (+24 more)

### Community 13 - "MeshBuffers"
Cohesion: 0.08
Nodes (14): current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., _ghost_depth_range(), MeshBuffers, Vertex/index buffers for one mesh, bound through a single VAO., Forget the contents without releasing the buffer objects., Where the form starts along the view, and how deep it is. The ghost weighs a…, Replace the model: the whole scene as one mesh, and the objects it is made of.… (+6 more)

### Community 14 - "Armature"
Cohesion: 0.04
Nodes (67): Armature, ArmatureNode, Bone, ndarray, Point3, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, Every node position as ``(n, 3)``. (+59 more)

### Community 15 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 16 - "ViewerState"
Cohesion: 0.07
Nodes (22): QObject, A copy of ``obj``'s mesh on top of it, made active, as one undo step., A parenting policy changed: what is shown and how solid may have too., Set the active matcap, or fall back to the built-in one., Have the HDRI at ``path`` read off the thread, and light with it when it lands.…, Light with a map already read -- or with none., Read the HDRI the settings name, if they light with one that is not here yet.…, Fit the scene in the view without changing the direction. (+14 more)

### Community 17 - "Skeleton"
Cohesion: 0.04
Nodes (35): Joint, _matrix16(), _pose_matrices(), ndarray, Whether the pose differs from the rest at all., A copy with the rest translation replaced and the frame kept., A tree -- or a forest -- of joints and the pose they stand in., Every joint, parents before children. A file may list a child before its… (+27 more)

### Community 18 - "framebuffer.py"
Cohesion: 0.07
Nodes (16): AccumTarget, ColorTarget, DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality, ghost and smoothing passes.…, A depth-only framebuffer, sampled afterwards as a texture., ``clamp_to_lit`` makes everything outside the map read as unshadowed., A single-channel colour framebuffer, used for the occlusion buffers. (+8 more)

### Community 19 - "CameraPanel"
Cohesion: 0.11
Nodes (9): CameraPanel, QListWidgetItem, Take the planes in hand where the fit left them, or hand them back., Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions. (+1 more)

### Community 20 - "PosePanel"
Cohesion: 0.08
Nodes (12): PosePanel, QWidget, The skeleton the panel is about: the selected row's, else the last., Highlight the row for a joint picked in the view., Arms the pose tool, lists the joints and poses the selected one., Adopt the viewport's tools: the pose tool, and the armature's for its selection., Lay an armature under the selected skeleton as it is posed., Guess the humanoid roles off the joint names; returns how many were found. (+4 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): Fill the shader's table with a level, if it is not already in it., ndarray, RuntimeError, Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "PoseTool"
Cohesion: 0.06
Nodes (45): JointRef, How skeletons are drawn, and how the pose tool behaves., SkeletonSettings, PoseTool, _project_many(), ndarray, The nearest unlocked joint of a visible skeleton under the cursor., The bone under the cursor, named by the joint at its far end. Taking hold of a… (+37 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.07
Nodes (25): app(), _names(), panel(), fixture, The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as… (+17 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.10
Nodes (11): MeasurePanel, _NameOnlyDelegate, QStyledItemDelegate, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing… (+3 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.11
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around. (+1 more)

### Community 26 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 27 - "Bounds"
Cohesion: 0.15
Nodes (15): Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray, A turntable-style disc the model can stand on. A ground plane gives the eye… (+7 more)

### Community 28 - "plane_volume.py"
Cohesion: 0.04
Nodes (111): _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field(), block_labels(), block_splits() (+103 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "DenoiseService"
Cohesion: 0.07
Nodes (32): DenoiserDevice, DenoiseSettings, Where Open Image Denoise runs., DenoiseRequest, DenoiserInfo, DenoiseService, gpu_name(), _module() (+24 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.10
Nodes (13): Chooses the shading model and edits its light and surface parameters., Where on the body skin effects appear, and their relative strength., List the bundled HDRIs, and the one in use if it is from elsewhere., Put the light's numbers back in line with the settings, after a drag or an undo., Freeze the slices the way the camera faces now. The view direction is the one…, Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel, A matcap has no light to aim, so the Light group goes -- and its space. The… (+5 more)

### Community 32 - "FilmRecorder"
Cohesion: 0.06
Nodes (35): QThread, FilmRecorder, Film, QObject, The film being recorded, or the last one finished., Whether a film is being made right now., The film already held for ``key``, if there is one., Stop any recording in flight and forget what it was making. The thread is asked… (+27 more)

### Community 33 - "test_camera.py"
Cohesion: 0.11
Nodes (9): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_clip_planes_set_by_hand_override_the_fit_within_reason(), test_orbit_keeps_the_pivot_under_the_cursor(), test_serialisation_round_trip() (+1 more)

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.19
Nodes (18): parametrize, Fitting planes to a model's surface rather than only to its normals. What…, Merging back from patches is a hierarchy, so the cuts of it nest. This is what…, Every plane of a level as a hashable whole: direction, place and offset., Nothing is seeded at random, so a session reopens looking the same., The renderer reads an empty set as "leave the normals alone"., The shader has to put a fragment into that frame before it can look up which…, A UV sphere, whose normals cover every direction evenly. (+10 more)

### Community 35 - "WakeLock"
Cohesion: 0.17
Nodes (13): Holds sleep off while the window that owns it is the one in front. The class…, WakeLock, Broken, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do., A platform that refuses, the way an old or locked-down one might., The viewer must open and close normally on a machine that says no., Recorder (+5 more)

### Community 36 - "integrator.py"
Cohesion: 0.10
Nodes (47): camera_ray(), filter_offset(), device, Primary rays: the pixel filter, the lens, and the two projections. The pixel…, The ray through film position ``(x, y)`` in pixels, top-left origin., _accept(), any_rays(), cap_normal() (+39 more)

### Community 37 - "lights.py"
Cohesion: 0.10
Nodes (39): disc_hit(), disc_sample(), env_background(), _env_frame(), env_pdf(), env_radiance(), env_sample(), _env_world() (+31 more)

### Community 38 - "CustomPanel"
Cohesion: 0.09
Nodes (21): carried(), Read a drag's payload back, or ``None`` if it is not one of ours., CustomPanel, _detach(), QFormLayout, QWidget, Take a copy out of this panel and destroy it., Move a copy already in a panel to a new place in this one. ``frame`` and… (+13 more)

### Community 39 - "film_export.py"
Cohesion: 0.07
Nodes (21): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+13 more)

### Community 40 - "RenderJob"
Cohesion: 0.08
Nodes (19): BucketOrder, Which bucket is rendered next., adaptive_error(), Mark blocks whose noise has fallen below ``threshold`` as done; returns pixels…, _hilbert_index(), JobState, _lower_priority(), pass_schedule() (+11 more)

### Community 41 - "Camera"
Cohesion: 0.06
Nodes (31): Camera, ndarray, Near/far planes fitted to the scene bounding sphere., The near and far planes this frame: the fitted ones, unless set by hand. A…, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Rays through a batch of pixels, as ``(origins, unit directions)``, ``(N, 3)``…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Project ``(N, 3)`` world points to ``(xs, ys, ndc_depths)`` in widget pixels. (+23 more)

### Community 42 - "skeleton.py"
Cohesion: 0.05
Nodes (74): Buried, What becomes of the part of the armature the model is standing in front of. An…, auto_skin(), AutoSkin, AutoSkinError, _baked_rest(), bone_segments(), _conjugate_gradients() (+66 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (11): _pull_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end., Set the value the way a hand on the control would., The value the track stands at ``x`` pixels across. (+3 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.10
Nodes (36): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), _first_skin(), GltfLoadError, load_gltf(), _local_transform() (+28 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.09
Nodes (14): even(), ExportVideoDialog, Film, Path, QDialog, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+6 more)

### Community 46 - "trace/skin.py"
Cohesion: 0.14
Nodes (34): body_fetch(), bump(), burley_pdf(), diffusion_lengths(), dome(), _fract32(), hash4(), marks() (+26 more)

### Community 47 - "landmarks.py"
Cohesion: 0.10
Nodes (27): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _mid(), mirror_landmarks(), mirror_point() (+19 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "body_regions.py"
Cohesion: 0.12
Nodes (22): band_weights(), BodyMap, bone_weights(), build_body_map(), looks_like_a_figure(), ndarray, Where on the body a point of the skin is, so that the skin can be marked as…, The bones a skeleton's humanoid roles describe, as ``(count, 7)`` rows. Each… (+14 more)

### Community 50 - "Coefficients"
Cohesion: 0.03
Nodes (96): Coefficients, _empty(), PlaneAxes, PlaneSet, ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, One level of a fit: the planes the shader is to quantise against. A plane is a…, A level with no place in it: nearest direction wins, as before. (+88 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.10
Nodes (33): QPoint, _drag(), _listed(), _matcap_file(), parametrize, The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc. (+25 more)

### Community 52 - "test_armature.py"
Cohesion: 0.05
Nodes (75): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _chain(), _derived(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other. (+67 more)

### Community 53 - "ArmaturePanel"
Cohesion: 0.05
Nodes (24): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Begin a preset run against a fresh armature., Take back the landmark before this one and ask for it again., Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked. (+16 more)

### Community 54 - "BodyRegionSettings"
Cohesion: 0.12
Nodes (13): BodyRegionSettings, _default_profiles(), Enum, str, How much of each skin effect one region gets, relative to its slider., Starting values for skin effects across a generic body., Where the regions come from, and what each does to the skin effects., One region's multiplier for ``effect`` after another, in :data:`REGIONS` order. (+5 more)

### Community 55 - "HotkeyMap"
Cohesion: 0.07
Nodes (19): Command, HotkeyMap, Any, Which keys do what, as the artist has decided rather than as it ships. A hotkey…, Whether the artist has moved this command off what it ships with., Which command has these keys, if any., Every command with keys on it, declared or not, as id -> keys., Put ``keys`` on a command, taking them off whatever had them. Returns the id of… (+11 more)

### Community 56 - "FilmExport"
Cohesion: 0.09
Nodes (17): Queue, _Encoder, FilmExport, frame_bytes(), QImage, QObject, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, The encoding itself, living on a thread of its own. It takes frames off a short… (+9 more)

### Community 57 - "FormsPanel"
Cohesion: 0.10
Nodes (10): FormsPanel, Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Ready the landmark the next click lays down, from the name and side boxes., The multiplier the position boxes are read and written through., Keep the ghost switch agreeing with the Shading panel's., Take off the panel whatever does not apply right now. (+2 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.08
Nodes (20): PlanesPanel, QListWidgetItem, Lay one length of wire earlier or later, as one undoable step., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Show what this way of working needs, and put the rest away. A setting that does… (+12 more)

### Community 59 - "test_skeleton.py"
Cohesion: 0.07
Nodes (53): quat_from_axis_angle(), build_humanoid_skeleton(), detail_joints(), humanoid_positions(), ndarray, Every humanoid role's place for a figure this tall standing on ``feet``., A proportioned humanoid skeleton, roles and all, standing on ``feet``., Which joints are detail, and which kind, read off their names. A toe past the… (+45 more)

### Community 60 - "Progress"
Cohesion: 0.07
Nodes (28): Exception, CancelledError, Progress, What a long piece of work says about itself while it runs, and how it is…, Ask the work to stop at its next report., How far along, 0 to 1, or ``None`` when the work has not said., Whether the work has said how much there is to do., A window onto part of a parent's range; see :meth:`Progress.slice`. (+20 more)

### Community 61 - "Workspace"
Cohesion: 0.06
Nodes (27): QDockWidget, QScrollArea, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top., Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, scrollable(), QMainWindow, QObject (+19 more)

### Community 62 - "RenderPanel"
Cohesion: 0.13
Nodes (6): QComboBox, _push_combo(), _format_bytes(), Sets up and starts path-traced renders., What follows from the settings: the size in pixels, the memory, the notes., RenderPanel

### Community 63 - "test_forms.py"
Cohesion: 0.03
Nodes (124): convex_hull(), DegenerateHullError, flat_mesh(), merged(), _outward(), _patch_samples(), ndarray, ValueError (+116 more)

### Community 64 - "application.py"
Cohesion: 0.07
Nodes (26): ArgumentParser, QSplashScreen, Application, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font(), main() (+18 more)

### Community 65 - "render_panel.py"
Cohesion: 0.09
Nodes (31): Rect, mode_note(), OutputSettings, How large the picture is and how it is saved., How the current shading mode renders, in a line for the Render panel., clamp_size(), frame_rect(), framed_camera() (+23 more)

### Community 66 - "PointEdit"
Cohesion: 0.09
Nodes (13): CloneGesture, Link, _pull_point(), _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original. (+5 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.04
Nodes (85): FormLandmarkRef, PlacedLandmark, One anatomical point the artist put on the model during a guided run., build_form(), built_count(), form_landmark_title(), form_mesh(), form_spec() (+77 more)

### Community 68 - "ShadingMode"
Cohesion: 0.05
Nodes (39): ClaySettings, ColorSettings, _copy(), DenoiserBackend, DenoiserQuality, FilmSettings, LensSettings, LightPathSettings (+31 more)

### Community 69 - "test_objects.py"
Cohesion: 0.14
Nodes (29): Where an object stands relative to its parent: an affine placement. Held as the…, Transform, app(), _key(), _mouse(), _overridden(), fixture, Several objects in one scene: placing, linking, merging, splitting, saving. (+21 more)

### Community 70 - "test_skin.py"
Cohesion: 0.06
Nodes (41): Future, _area(), build_bvh(), ndarray, A bounding-volume hierarchy over triangle boxes, built by the surface-area…, Half the surface area of boxes; nought for an empty (inverted) one., Build the tree over triangle boxes. Returns the triangle order, and per node…, bind_default() (+33 more)

### Community 71 - "test_plane_solids.py"
Cohesion: 0.03
Nodes (144): compute_vertex_normals(), Area-weighted smooth vertex normals for an indexed triangle soup., plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), film_of(), parametrize (+136 more)

### Community 72 - "ObjectTool"
Cohesion: 0.12
Nodes (14): _axis_param(), Gizmo, _Grip, ObjectTool, ndarray, The three directions the arms run along, in world space. A move and a turn are…, Where the gizmo for an object at ``world`` falls on screen, or ``None`` if…, Which handle a screen point is over: ``"centre"``, ``"x"``, ``"y"``, ``"z"`` or… (+6 more)

### Community 73 - "MatcapSettings"
Cohesion: 0.13
Nodes (20): MatcapSettings, Post-processing applied to the sampled matcap texel., _angle(), _clone_preview(), grade(), _pull_preview(), _push_preview(), ndarray (+12 more)

### Community 74 - "ArmatureTool"
Cohesion: 0.06
Nodes (39): BoneRef, LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, Handle, The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now. (+31 more)

### Community 75 - "SkinSettings"
Cohesion: 0.13
Nodes (29): SkinSettings, test_bad_loaded_parameters_cannot_poison_history(), test_controls_and_presets_write_to_saved_material(), _inputs(), Whole renders: energy, determinism, the two methods, stopping, adaptive…, Under light of radiance one from everywhere, a convex matte ball shows its…, _render(), test_a_cancel_stops_the_render_promptly() (+21 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.17
Nodes (21): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+13 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.07
Nodes (23): QMimeData, app(), custom(), _drop_on(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error., A group is not a row, so it goes ahead of the group it was dropped on. (+15 more)

### Community 78 - "SkinEdit"
Cohesion: 0.07
Nodes (15): BakeEdit, Command, ndarray, Write ``obj``'s turn and scale into its mesh, leaving it standing as it is.…, Dressing an object in a skin made for a skeleton, or taking it off. One step…, The 4x4 that takes a point on the old rest mesh onto the new one. A point sits…, Carry the measurements, annotations, armature and forms through ``carry``., An object's rest mesh as a file stores it, so that reading it back comes to… (+7 more)

### Community 79 - "core/preferences.py"
Cohesion: 0.12
Nodes (18): _as_kind_of(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any, What the artist prefers, as distinct from what the document says. There are two… (+10 more)

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
Cohesion: 0.07
Nodes (19): ObjectsEdit, Snapshot, Scale ``objects`` so each is the size of the active one, as one undo step. The…, The largest of ``obj``'s three extents as it stands in the world., Re-read how solid each part is drawn, without touching the geometry., An edit to the objects -- a move, a parenting, a removal -- as two snapshots.…, Where everything stands now; the start of a gesture keeps one., Move each bound skeleton by however far its object moved since ``before``. (+11 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.14
Nodes (26): _click(), _pending(), _pick(), _place_all(), The Forms panel: the guided run it drives, and the document it writes. The…, A form row hands the whole form to update_enabled, whose landmark list must be…, Type a name for the next landmark and, if given, pick its side., What the viewport does when a freeform run gets a click. (+18 more)

### Community 85 - "PlaneSettings"
Cohesion: 0.04
Nodes (45): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, Holds the working state between one turn of the sliders and the next.…, The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache, An armature, as the clay reads it: where each length of wire runs. The order…, How many lumps the wire itself asks for. (+37 more)

### Community 86 - "viewport.py"
Cohesion: 0.03
Nodes (74): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, What the annotate tool does with a drag. The first three describe the shape a…, BoneLabels, Enum, str (+66 more)

### Community 87 - "ViewportRenderPreview"
Cohesion: 0.10
Nodes (16): exposure_scale(), quantize_region(), Display values to 8-bit RGBA, rounding to nearest., Film, ndarray, The picture and its guides, as a film holds them., request_from_film(), denoise_service() (+8 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.13
Nodes (11): MatcapPanel, Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, Rebuild the thumbnail list: the built-in, the ones added, then the folder., Put the matcap on the model into the gallery, if it came from somewhere else.…, The disc was dragged: show the renderer and the numbers what it did., A different matcap: the disc draws whichever one is on the model., Put the numbers back in line with the settings, and redraw the disc. Separate… (+3 more)

### Community 89 - "AnnotatePanel"
Cohesion: 0.19
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 90 - "Frame"
Cohesion: 0.07
Nodes (18): _pull_frame(), _push_frame(), Nothing: each row inside the copy is linked on its own., Frame, FrameBar, framed(), QFormLayout, QPainter (+10 more)

### Community 91 - "main_window.py"
Cohesion: 0.04
Nodes (68): Every document edit is a command, AddItem, Command, The handful of undoable edits the whole application is built from.…, Append an item to a document list., Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem (+60 more)

### Community 92 - "RenderWindow"
Cohesion: 0.12
Nodes (8): A render, finished or under way, and everything needed to show and save it., RenderResult, ndarray, QImage, QWidget, The window renders are shown in; made once and kept., RenderWindow, test_the_render_window_develops_and_saves_a_film()

### Community 93 - "test_elements.py"
Cohesion: 0.05
Nodes (29): QApplication, QObject, Making the whole of a switch the part you can press. The theme turns every…, Turns a press anywhere on a switch into a click on it., Put the rule in place for every switch in the application., WholeFaceToggles, app(), fixture (+21 more)

### Community 94 - "Mesh"
Cohesion: 0.04
Nodes (77): auto_smooth(), concatenated(), _corner_groups(), _face_cross(), _gathered(), _group_normals(), Path, One entry point for every mesh format the viewer reads. Callers ask for a path… (+69 more)

### Community 95 - "MeasurementStore"
Cohesion: 0.12
Nodes (8): MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., One end of the measurement, ``0`` for the start and ``1`` for the end., An ordered, named collection of measurements. Deliberately plain: the Qt layer…, test_the_stack_is_bounded(), test_store_auto_names_new_measurements()

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - "OrientationSettings"
Cohesion: 0.10
Nodes (24): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Path, Turn every object the same way; see :meth:`set_object_orientation`. For files…, Turn one object, bringing the marks made on it along. Measurements,…, Turning an imported model the right way up., A Z-up scan and a Y-up sculpt stand in one scene, each read its own way. (+16 more)

### Community 98 - "ColorButton"
Cohesion: 0.12
Nodes (10): _pull_swatch(), _AxisBox, ColorButton, QColor, QDoubleSpinBox, QSize, QWidget, A spin box with its axis letter written faintly down its left. (+2 more)

### Community 99 - "FormStore"
Cohesion: 0.18
Nodes (4): FormStore, An ordered, named collection of forms, like the other stores., A name for a new form of this recipe, numbered past any it already has. A form…, test_a_form_store_names_forms_past_the_ones_it_has()

### Community 100 - "clone.py"
Cohesion: 0.04
Nodes (87): QAbstractButton, QLineEdit, QSlider, QSpinBox, _begin(), can_clone(), clone(), _clone_button() (+79 more)

### Community 101 - "skin_detail.py"
Cohesion: 0.17
Nodes (20): burley_marginal(), burley_profile(), cellular(), diffusion_lut(), _fade(), fbm(), ndarray, Procedural skin micro-relief and the pre-integrated diffusion table. Reference… (+12 more)

### Community 102 - "Path"
Cohesion: 0.13
Nodes (11): A flat-shaded mesh, every triangle with its own three corners. Corners are not…, Path, Pick up whatever was last being worked on, if that was asked for. A session…, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window. In the…, Read a model file off the window, then hand it to ``adopt`` here., Add a model to the scene beside what is already there. (+3 more)

### Community 103 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.09
Nodes (11): Record the finished drag as a single undo step., Record the turn as one undo step., Alt forces the camera gesture, whichever tool is armed., Record the finished drag as one step, or read a press as a selection., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Make the object under the cursor the active one., Record the finished pull as one step, or read a press as a selection. (+3 more)

### Community 105 - "._delete_selected"
Cohesion: 0.19
Nodes (5): The freeform the highlighted row belongs to, when no run is on., Record an edited landmark list, mirrored where the mirror is on., Remove the selected landmark, or the whole form when its row is picked., The form the selected row stands for, when the row is a form., The landmark the highlighted row stands for, if the row is one.

### Community 106 - "OverlayParts"
Cohesion: 0.13
Nodes (8): Which of the things drawn over the model belong in the frames., MarkerVisibility, Cache surface occlusion by view and position for every kind of marker. The…, Whether the last pass is recent enough to be read instead of repeated., Mark these points as standing in front of the surface, untested. For frames…, Answer for a batch of points at once, ahead of being asked one by one. Every…, OverlayParts, Which of the things drawn over the model are wanted this time. The viewport…

### Community 107 - "SectionSettings"
Cohesion: 0.19
Nodes (15): How the model is cut open, and how the cut is drawn., SectionSettings, _box(), Cutting planes, the contour they produce and the pedestal under the model., A closed axis-aligned cube centred on the origin., The contour of a plane through a cube is its cross-section outline., test_a_custom_normal_is_normalised(), test_a_disabled_section_cuts_with_nothing() (+7 more)

### Community 108 - "test_tasks.py"
Cohesion: 0.17
Nodes (16): app(), fixture, Work run off the window, and the cards that show it running., Turn the event loop until ``until()`` says so, or give up., runner(), _spin(), test_a_result_arriving_after_the_cross_is_thrown_away(), test_a_task_called_off_while_waiting_never_starts() (+8 more)

### Community 109 - "materials.py"
Cohesion: 0.16
Nodes (26): ggx_d(), ggx_eval(), ggx_sample(), material_alpha(), principled_eval(), _principled_parts(), principled_sample(), device (+18 more)

### Community 110 - "DockTitle"
Cohesion: 0.09
Nodes (13): QToolButton, DockTitle, make_switch(), QCheckBox, QSize, QWidget, Put a show/hide switch at the left of the bar and return it., A square that is on or off, and is clickable all over. A check box decides… (+5 more)

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - "Path"
Cohesion: 0.09
Nodes (18): ObjectRecord, What a session writes down about an object; the mesh itself stays in its file., Path, Take the display unit from the file when the format declares one. Only glTF…, Write the document, and whatever the window says its layout is. The layout…, Write every skin made here beside the session; see :mod:`rig_file`., A file for ``obj`` next to the session, named for both., Open a session: its models, then everything it says about them. ``sources`` are… (+10 more)

### Community 113 - "Task"
Cohesion: 0.06
Nodes (26): _outcome(), ProgressCard, Any, BaseException, QObject, QPainter, QWidget, T (+18 more)

### Community 114 - "History"
Cohesion: 0.17
Nodes (14): History, A bounded undo/redo stack., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch(), test_commands_carry_their_channel_and_name() (+6 more)

### Community 115 - "PathTraceSettings"
Cohesion: 0.10
Nodes (21): PathTraceSettings, available(), The CPU path tracer: numpy and numba, never Qt and never OpenGL. Importing this…, Whether the path tracer can run here (numba loads)., Why the path tracer cannot run, or ``None`` when it can., unavailable_reason(), Film, What of the settings a rendered picture shows, as a key. The viewport preview… (+13 more)

### Community 116 - "refview/__init__.py"
Cohesion: 0.13
Nodes (12): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version(), app(), opened(), fixture, Files arriving from outside: the command line, a drop, or the desktop's "Open…, One offscreen Qt application for the run; see test_film_recorder. (+4 more)

### Community 117 - "sampler.py"
Cohesion: 0.16
Nodes (24): bounce_set(), _direction_numbers(), hash32(), hash_combine(), hash_float(), _laine_karras(), nested_uniform_scramble(), pixel_seed() (+16 more)

### Community 118 - "Session"
Cohesion: 0.08
Nodes (29): _coerce(), decode(), encode(), Any, T, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``. (+21 more)

### Community 119 - "SetAttributes"
Cohesion: 0.10
Nodes (9): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Run a row's edit once Qt has finished delivering the current signal. Committing…, Record an edit the viewport's tool worked out., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal., Turn the joint as the slider moves, remembering where it started. (+1 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.08
Nodes (36): QPointF, draw_text(), Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, project_visible(), project_visible_many(), Handle, ndarray, QColor (+28 more)

### Community 121 - "test_hotkeys.py"
Cohesion: 0.07
Nodes (35): can_take_key(), is_hotkey_click(), KeyGesture, QObject, QWidget, The gesture that puts a key on a control: Ctrl/Cmd, Alt and a click. It sits…, Whether a mouse press is the assignment gesture rather than a click., Whether a widget is the kind a key can sensibly be put on. A button or a switch… (+27 more)

### Community 122 - "ArmatureStore"
Cohesion: 0.18
Nodes (4): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 123 - "VideoSettings"
Cohesion: 0.15
Nodes (8): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, TestFilmExport, TestTiming

### Community 124 - ".refresh_list"
Cohesion: 0.24
Nodes (5): QTreeWidgetItem, Rebuild the tree from the store, keeping the landmark being edited shown. Not…, Commit a renamed or re-checked form, or a renamed landmark, if anything changed., Give a freeform's own landmark the name typed into its row., Run a row's edit once Qt has finished delivering the current signal. Committing…

### Community 125 - "Reflow"
Cohesion: 0.30
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 126 - "Landmark"
Cohesion: 0.08
Nodes (18): _centre(), FormPreset, _pair(), Which stage a landmark belongs to, or the last for an unknown key., A left landmark, then the right one that mirrors it., The freeform landmark the artist named with this key, if any., The named landmarks with one more, or the same one re-described., A form's recipe: its stages, in order, and the rule that builds them. (+10 more)

### Community 127 - "SectionPanel"
Cohesion: 0.19
Nodes (6): Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 128 - "._upload_sculpt"
Cohesion: 0.12
Nodes (7): The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, Cut the stand-in on a thread; see :meth:`_upload_sculpt`., Show the recording as a task, its bar the stages landed so far., The cross on the recording's card: the film is dropped, the switch too., A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on.

### Community 129 - "._sync_scene"
Cohesion: 0.08
Nodes (11): Cut the mesh with each section plane and expand the result to strokes., The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, A skeleton changed: redraw it, and let the skin's body map follow its bones., What the renderer draws: each object as it stands, AutoSmoothed if asked., ``mesh`` shaded by the object's smoothing groups, found once and kept. The…, The whole scene as one mesh, as the planes and the skin tracer read it. The…, Tell the renderer what the skin's body map is made from now., Hand the renderer a re-posed model and nothing else. For the frames of a pose… (+3 more)

### Community 130 - "colour.py"
Cohesion: 0.17
Nodes (21): _aces(), develop(), develop_image(), develop_region(), _encode(), linear_to_display(), _neutral(), device (+13 more)

### Community 131 - "AnnotateTool"
Cohesion: 0.13
Nodes (13): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses., Continue the open run with a hit, or end it where the ray missed. (+5 more)

### Community 132 - "ExportLook"
Cohesion: 0.07
Nodes (22): QOpenGLFramebufferObject, The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, ExportLook, What the frames are to look like, as against what they are of. Laid over the…, ``base`` with this export's choices laid over it. (+14 more)

### Community 133 - "obj_loader.py"
Cohesion: 0.07
Nodes (45): load_mesh(), Load any supported mesh file, raising :class:`MeshLoadError` otherwise., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic() (+37 more)

### Community 134 - "preview"
Cohesion: 0.29
Nodes (7): app(), gallery_settings(), preview(), fixture, The gallery's list on a settings file of the tests' own, empty to begin with., One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "._build"
Cohesion: 0.18
Nodes (10): QTreeWidget, _NameOnlyDelegate, QPushButton, QStyledItemDelegate, QWidget, Allows in-place editing of the name column only., Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list… (+2 more)

### Community 136 - "paths.py"
Cohesion: 0.16
Nodes (20): available_environments(), available_matcaps(), _bundled_root(), cache_dir(), environment_dir(), image_path(), matcap_dir(), model_dir() (+12 more)

### Community 137 - "Release"
Cohesion: 0.11
Nodes (19): QRunnable, The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, _CheckTask, is_skipped(), QObject, QWidget (+11 more)

### Community 138 - "Film"
Cohesion: 0.13
Nodes (13): ndarray, Path, Writing a render as OpenEXR: the light as it is, and its passes as layers. An…, Write ``layers`` -- ``"RGBA"`` first, then passes by name -- to ``path``.…, Every channel of an EXR by name, as the file groups them; for tests., read_exr_channels(), write_exr(), Film (+5 more)

### Community 139 - "Command"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 140 - "._advance_pending"
Cohesion: 0.25
Nodes (4): Begin a run against a fresh form: a preset's walk, or a freeform's., Take up the selected freeform again, so more landmarks can go on it. The same…, After a landmark goes down: a fresh numbered name, the same side., Record an edit the viewport's tool worked out. A freeform's placed landmark is…

### Community 141 - "RenderController"
Cohesion: 0.16
Nodes (6): BaseException, QObject, Render ``inputs`` (a :class:`~refview.trace.scene.TraceInputs`), stopping any…, Denoise a render's film now, with the settings as they are., Starts, watches and finishes renders for the Render panel and window., RenderController

### Community 142 - "vec.py"
Cohesion: 0.19
Nodes (18): add(), clamp(), length(), linear3(), madd(), mul(), neg(), normalize() (+10 more)

### Community 143 - "MatcapPreview"
Cohesion: 0.08
Nodes (18): QMenu, MatcapPreview, Path, QImage, QRect, QSize, QWidget, A matcap on a sphere, which is also how the matcap is graded. (+10 more)

### Community 144 - "._picker"
Cohesion: 0.08
Nodes (14): ndarray, Rub out the stroke points under the eraser, live., Turn the lights by how far the drag has come: across about the vertical, up in…, Take hold of a node, to move it, resize it, or just to select it. This works…, Apply the drag live, so the artist sees the wire bend as they pull it., Take hold of a landmark, to move it or just to say which one it is., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit. (+6 more)

### Community 145 - "._carrying_a_copy"
Cohesion: 0.11
Nodes (10): opens_as(), Apply a matcap image, reporting unreadable files to the user., Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model., Take a copied control out of whichever hand-built panel holds it., Open a file by what it is: a model, a session, a matcap or an HDRI. The one…, What a file opens as, by its suffix: a model, a session, a matcap or an HDRI. (+2 more)

### Community 146 - "._build"
Cohesion: 0.33
Nodes (4): QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 147 - "LightingMode"
Cohesion: 0.13
Nodes (9): ContourDirection, LightingMode, PlaneTarget, Enum, str, The world axis, or ``None`` when it is the camera's or the artist's., What the lit shading modes are lit by. The studio rig is a key, a fill opposite…, What the planes filter is allowed to act on. The two are mutually exclusive… (+1 more)

### Community 148 - "._turn"
Cohesion: 0.15
Nodes (7): Redraw from the settings, which something else has changed., Put the grading back, which is the one thing a disc cannot show., Turn the matcap by the angle the cursor swept about the centre. By angle and…, Two grades on one drag: one along each axis of the movement. Both move together…, Keep the angle in -180 to 180, the range the setting is stored in., An angle difference brought back into -pi to pi., _wrapped()

### Community 149 - "SurfacePicker"
Cohesion: 0.06
Nodes (28): GuideRun, _project(), Begin a preset run against an armature already in the store., The thickness a resize drag is asking for: the cursor's reach, in world units., Where on a bone a click at ``(x, y)`` landed. The share along the bone is read…, A guided preset part-way through. The index walks the preset's own list rather…, A world point in widget pixels, or ``None`` when it is behind the camera., How far along a screen-space segment the cursor's nearest point lies. (+20 more)

### Community 150 - "test_body_regions.py"
Cohesion: 0.29
Nodes (12): _column(), _figure_bones(), ndarray, Where on the body the skin is: bones, height bands, the map, and the settings., A thin column standing from the ground to ``height``., _region(), test_height_bands_follow_the_canon_and_are_soft_at_the_edges(), test_points_go_to_the_region_of_the_nearest_bone_and_blend_between() (+4 more)

### Community 151 - "ContourShadingSettings"
Cohesion: 0.20
Nodes (8): ContourShadingSettings, Parallel slices drawn across the form, the way a contour map reads land. The…, The unit direction the slices are stacked along, in world space., parametrize, The contour shading mode: slices across the form, read off it like a map., test_a_custom_direction_is_normalised_and_an_empty_one_falls_back(), test_the_density_floor_keeps_the_spacing_finite(), test_the_slices_face_the_way_that_was_asked()

### Community 152 - "mesh_renderer.py"
Cohesion: 0.06
Nodes (26): background_basis(), EnvironmentTextures, ndarray, Columns that turn a screen position (-1 to 1 each way, 1) into a world ray. An…, The map, the sampling tables, and the uniforms that describe them., Put a map on the card, or take it off; cheap when it is the one already there., Point ``program`` at the map, scaled by ``scale_factor`` on top of the rig's…, OpenGL rendering layer: shader programs, textures and the scene renderer. (+18 more)

### Community 153 - ".refresh_list"
Cohesion: 0.12
Nodes (7): QTreeWidgetItem, Highlight a row, in the tree and in the view., Add an empty skeleton, for a chain to be clicked into., Stand a proportioned humanoid skeleton in the model's box., Grow a skeleton out of the armature chosen in the box., Record a structural edit the viewport's tool worked out., Rebuild the tree from the store, keeping the tool's selection shown. Not under…

### Community 154 - "._focused_form"
Cohesion: 0.22
Nodes (4): Refit the focused freeform's clay; for a new one, remember the choice., Show a stage of the focused form. A view choice, so not an undo step., Size the stage slider to the focused form, and hide it for a one-stage form., The form the stage slider speaks for: the one being guided, else the one picked.

### Community 155 - "RenderView"
Cohesion: 0.22
Nodes (4): QPainter, QRectF, The picture, over a checkerboard where it is transparent, zoomed and moved at…, RenderView

### Community 156 - "render_window.py"
Cohesion: 0.20
Nodes (11): ndarray, to_rgba16(), to_rgba8(), _duration(), Path, The Render Window: a render filling in, and the controls to look at it and keep…, The status line: pass, samples, time, speed, threads, memory., Display values ``(h, w, 4)`` in [0, 1] to a PNG, 8 or 16 bits a channel. (+3 more)

### Community 157 - "jit.py"
Cohesion: 0.14
Nodes (13): atrous(), _pass(), ndarray, The built-in denoiser: an edge-avoiding a-trous wavelet filter (Dammertz et al.…, ``(h, w, 3)`` light in, smoothed light out. ``noise`` is the expected error of…, available(), _install_frozen_locator(), numba, and how the tracer's kernels are compiled. Every kernel in… (+5 more)

### Community 158 - "shader_files.py"
Cohesion: 0.19
Nodes (9): _expand(), load_glsl(), Reading the GLSL out of :file:`render/glsl`. Each program's source lives in a…, The source of ``name`` with its includes, constants and defines worked in., _read(), GLSL sources for the viewport, read from :file:`render/glsl`. A handful of…, Skin BRDF and bounded-depth light transport, shared by preview and refinement.…, The GLSL on disk: its includes and constants, and that every program is whole. (+1 more)

### Community 159 - ".paintGL"
Cohesion: 0.17
Nodes (5): Use the same cached visibility test for bones and all point markers., Which part wears the line this frame, and how solid it is, or ``None``. Also…, Hand the renderer the depth grid, or take it away, before a frame., Whether a gesture in the view is moving something right now. What holds the…, The render's size in pixels, as the Render panel sets it for this view.

### Community 160 - "._build_objects"
Cohesion: 0.19
Nodes (6): _ObjectTree, QPushButton, QWidget, A tree whose rows can be dropped onto one another to hang one from another. Qt…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 161 - "wakelock.py"
Cohesion: 0.16
Nodes (9): _Backend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., A way of asking one platform to stay awake., Ask for sleep to be held off., Withdraw the request. (+1 more)

### Community 162 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 163 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 164 - "Human Skin renderer"
Cohesion: 0.25
Nodes (7): Human Skin renderer, Marks and body regions, Material and transport, Scheduling, precision and compatibility, Surface, The HDRI, Where to change it

### Community 165 - ".__init__"
Cohesion: 0.14
Nodes (11): draw_rail(), One marker object for endpoints, nodes, landmarks and tool previews., The screen-space cue for one degree of freedom. A vertical rail that fades out…, VisualMarker, Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo (+3 more)

### Community 166 - "FrameTarget"
Cohesion: 0.09
Nodes (34): BodySource, What a body map is worked out from: the meshes, the bones over them, and how., FrameTarget, The whole frame, drawn offscreen so it can be smoothed on the way out. A colour…, Say what the skin's body map is to be worked out from; see :mod:`body_regions`.…, Draw one frame, then hand a neutral GL state back to the caller.…, gl_context(), fixture (+26 more)

### Community 167 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 168 - "._place_armature_node"
Cohesion: 0.33
Nodes (3): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 169 - "sample_count"
Cohesion: 0.50
Nodes (3): How many samples the framebuffer bound right now is drawing with. One where…, sample_count(), How many samples this view is really drawing with, or ``None``. Asked of GL…

### Community 170 - "_height_of"
Cohesion: 0.40
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 171 - "test_trace_bvh.py"
Cohesion: 0.29
Nodes (14): _cast(), _geometry(), The path tracer's tree and rays, against brute force., _rays(), _soup(), _sphere_geometry(), test_a_ghost_is_hit_as_often_as_it_is_solid(), test_nearest_hit_matches_brute_force_on_a_soup() (+6 more)

### Community 172 - "Path tracer"
Cohesion: 0.14
Nodes (13): Colour, Compilation, Denoisers, Human Skin, Integrator, Jobs, Lights, Limits (+5 more)

### Community 173 - "README.md"
Cohesion: 0.14
Nodes (15): Picking about a hundred times faster, Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Morton-curve leaf boxes for picking, Orthographic extent derived from FOV and distance (+7 more)

### Community 175 - "test_annotation.py"
Cohesion: 0.22
Nodes (13): build_vertices(), Expand strokes into the triangle soup the stroke shader expects. Every segment…, line_stroke(), Surface annotations: erasing, splitting and the geometry handed to GL., A stroke running along +X, one unit apart, with +Y normals., test_a_closed_stroke_gains_the_wrapping_segment(), test_each_segment_becomes_six_vertices(), test_erasing_keeps_the_brush_and_drops_stubs() (+5 more)

### Community 176 - "raycast_mesh"
Cohesion: 0.05
Nodes (52): _cross(), Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Row-wise cross product, without :func:`numpy.cross`'s axis shuffling., Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface. (+44 more)

### Community 177 - "Path"
Cohesion: 0.21
Nodes (13): added_matcaps(), forget_matcap(), Path, QIcon, The matcaps added from outside the folder that are still on disk, newest first.…, Keep ``path`` in the gallery from now on., Take ``path`` out of the gallery; the file itself is left alone., _read_added() (+5 more)

### Community 178 - "section_segments"
Cohesion: 0.18
Nodes (9): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, Unit axis, or ``None`` for a custom direction., A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., section_segments() (+1 more)

### Community 179 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 180 - "step"
Cohesion: 0.15
Nodes (13): angle_deg(), quad(), The reason for reading where the surface is and not only which way. Both faces…, The limit the clustered fits exist to lift, stated as a fact., A flat with a scattering of bad normals is still shaded as that flat. Averaging…, Splitting a broad flat by place must not invent a turn in it. The plate below…, Add one flat quad, with its own vertices, to a mesh under construction., Two broad faces both looking straight up, one raised above the other. The case… (+5 more)

### Community 181 - "open_writer"
Cohesion: 0.08
Nodes (28): _encode_arguments(), _encoders(), ffmpeg_path(), _FFmpegWriter, _no_window(), open_writer(), Path, RuntimeError (+20 more)

### Community 182 - "section.py"
Cohesion: 0.21
Nodes (7): Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Which side of the plane survives the cut., SectionAxis, SectionMode

### Community 183 - "HotkeyBinder"
Cohesion: 0.15
Nodes (13): QKeySequence, QShortcut, HotkeyBinder, QObject, Turns the map into the shortcuts of one window, and keeps them current., Put every command's keys where they are heard. Cheap; run on any change., Say in a control's tooltip what key it answers to, if it is one of ours. A copy…, The shortcut answering for a command, for a test that wants to press it. (+5 more)

### Community 184 - ".refresh"
Cohesion: 0.18
Nodes (3): Bind the panel to the viewport's transform tool., Turn the active object, or note how the next file is read when there is none., Write the active object's placement into the boxes.

### Community 185 - "lzw"
Cohesion: 0.36
Nodes (5): lzw(), The GIF flavour of LZW: variable-width codes, packed low bit first. Straight…, A plain GIF LZW decoder, for testing the encoder against. Deliberately written…, TestLzw, unlzw()

### Community 186 - "ModelPanel"
Cohesion: 0.13
Nodes (5): ModelPanel, Reflect the tool state without re-emitting the toggle., Choose the gesture, from the menu or a key., Bake the active object's turn and scale into its mesh., Lists the objects, places the active one, and reports what came out of its file.

### Community 187 - "ui/preferences.py"
Cohesion: 0.09
Nodes (21): current(), forget(), PreferenceStore, QObject, QSettings, _qcolor(), Where the preferences are kept, and what happens when one changes.…, Push the preferences that something in the process holds a copy of.… (+13 more)

### Community 188 - "MeasureTool"
Cohesion: 0.12
Nodes (10): MeasureTool, Handle, ndarray, The nearest grabbable endpoint under the cursor, if any. Only unlocked, visible…, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview. (+2 more)

### Community 189 - "ThreadWakeLock"
Cohesion: 0.22
Nodes (4): Hold sleep off, or stop holding it, whichever is not already true., Drop the request, if one is out. Safe to call more than once., Holds sleep off from a thread of its own, for as long as some work runs. For a…, ThreadWakeLock

### Community 190 - "test_render_panel.py"
Cohesion: 0.20
Nodes (4): app(), panel(), fixture, The Render panel and the Render window, offscreen.

### Community 191 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 192 - "stroke_renderer.py"
Cohesion: 0.29
Nodes (8): Replace the reference grids; pass ``None`` to take them away. ``lines`` is a…, build_segment_vertices(), _expand(), ndarray, Geometry for the surface annotations and the cross-section contour. Strokes are…, Expand loose ``(n, 2, 3)`` segments -- the section contour -- the same way. The…, Six vertices per segment, in the layout the stroke shader expects., _segment_block()

### Community 193 - "ui/hotkeys.py"
Cohesion: 0.07
Nodes (35): QKeySequenceEdit, assign(), control_of(), decorate(), describe(), forget(), group_of(), HotkeyStore (+27 more)

### Community 194 - ".__init__"
Cohesion: 0.10
Nodes (10): _plain(), QAction, Open the preferences, on one group when the menu asked for one., Push the preferences that this window's own parts hold a copy of. The store has…, Put the docks and the hand-built panels back where they were. Unless the artist…, A menu entry's text as a name: no accelerator ampersand, no trailing dots., Give each panel a dock of its own, tabbed together on the right. Each panel can…, Which panels are open, and the panels the artist builds. Rebuilt every time it… (+2 more)

### Community 195 - ".refresh_list"
Cohesion: 0.20
Nodes (4): QTreeWidgetItem, Rebuild the tree from the store, with the active object current., Offer every object the active one could hang from., Commit a renamed or re-checked row, if anything actually changed.

### Community 196 - "cube"
Cohesion: 0.22
Nodes (10): cube(), How far the least well served of ``wanted`` is from anything offered., The one form whose planes are not a matter of opinion., The sample limit is a speed measure, so it must not move the planes. Asked of a…, A cube with hard edges, each face cut into a grid of triangles., A mode with no fitter behind it would shade as an unbroken surface., test_a_cube_breaks_into_its_own_six_faces(), test_every_mode_the_panel_offers_can_be_fitted() (+2 more)

### Community 197 - "test_workspace_layout.py"
Cohesion: 0.24
Nodes (7): app(), _Plain, fixture, QMainWindow, A layout saved before a panel existed still tabs that panel in with the rest., test_a_new_panel_joins_the_tab_strip_of_an_old_layout(), _window()

### Community 198 - "ask_for"
Cohesion: 0.15
Nodes (12): ask_for(), command_for(), HotkeyDialog, Command, QAction, QDialog, The command a control stands for, or ``None`` if it has no name to go by. A…, A menu entry. Its keys are heard anywhere in the window and shown in the menu. (+4 more)

### Community 201 - ".source_mesh"
Cohesion: 0.25
Nodes (5): setter, The active object turned and centred but not posed or placed., The active object exactly as its file stored it., Set the active object's file mesh; its rest mesh is turned from it as at a load., The active object, made on the spot when a mesh is handed to an empty scene.

### Community 202 - "StrokeBuffers"
Cohesion: 0.25
Nodes (3): A single vertex buffer holding every visible stroke., Replace the buffer contents with a prepared vertex block., StrokeBuffers

### Community 203 - "test_leaning_on_position_breaks_a_form_up_as_well_as_down"
Cohesion: 0.22
Nodes (9): bent_plate(), ndarray, A plate creased down the middle, and which column each vertex is in. Flat to…, Vertices on a turn are ambiguous about their plane, so they are quieted. The…, How many planes have another plane pointing very nearly where they do., The coefficients have to reach the fit, and reaching it has to show. Two planes…, same_facing(), test_a_turn_in_the_form_gets_less_of_a_say_than_a_flat() (+1 more)

### Community 204 - "CHANGELOG.md"
Cohesion: 0.15
Nodes (13): Shift-snapped orbiting (1.1.0), Cross-section tool (1.1.0), High Quality shading mode (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4 (+5 more)

### Community 205 - "_WindowsBackend"
Cohesion: 0.25
Nodes (5): ``SetThreadExecutionState``: a flag on this thread, not a handle. The flags…, _WindowsBackend, skipif, The flag the viewer sets is the one Windows reports back afterwards., test_windows_really_sets_the_execution_state()

### Community 206 - "lumpy"
Cohesion: 0.25
Nodes (8): lumpy(), A form with real planes in it, and more than one facing the same way., The fit and the shader have to agree, or the boundaries drawn are not the…, Narrow it and only the flattest surface has a say; widen it and the rounded…, The planes moved out of a uniform array and into a texture so that the count…, test_a_coefficient_of_zero_takes_the_term_out_of_the_shader_too(), test_the_fit_reaches_past_the_old_ceiling_of_sixty_four(), test_the_flat_span_says_how_much_of_the_form_counts_as_flat()

### Community 207 - "_MacBackend"
Cohesion: 0.33
Nodes (3): c_void_p, _MacBackend, An IOKit power assertion, held by id until it is released.

### Community 208 - ".refresh_list"
Cohesion: 0.40
Nodes (3): QTreeWidgetItem, Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing.

### Community 209 - "._back_point"
Cohesion: 0.33
Nodes (3): Take back the landmark before this one and ask for it again., Take back the last landmark a freeform was given, guess and all., The mirrored landmarks reflected from ``key``, which it anchors.

### Community 210 - "._commit_node_drag"
Cohesion: 0.33
Nodes (3): Record the finished gesture: a move, a resize, or a plain click. A press that…, Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…

### Community 211 - "FormRun"
Cohesion: 0.40
Nodes (3): FormRun, Begin a run against a form already in the store., A guided form part-way through.

### Community 213 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 214 - "box"
Cohesion: 0.50
Nodes (4): box(), A unit cube, shaded flat: six planes and twelve right angles., Every edge of a cube is a right angle, and no reading of AutoSmooth short of…, test_autosmooth_leaves_a_real_plane_change_hard()

### Community 215 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

## Knowledge Gaps
- **26 isolated node(s):** `refview`, `FunctionTable`, `OptixDenoiserOptions`, `OptixDenoiserGuideLayer`, `OptixDenoiserLayer` (+21 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `ExportLook`, `obj_loader.py`, `SceneObject`, `trace/scene.py`, `core/camera.py`, `RenderSettings`, `MeshBuffers`, `ViewerState`, `Skeleton`, `SurfacePicker`, `PoseTool`, `test_body_regions.py`, `mesh_renderer.py`, `Bounds`, `plane_volume.py`, `FilmRecorder`, `test_plane_clusters.py`, `FrameTarget`, `Camera`, `skeleton.py`, `test_trace_bvh.py`, `gltf_loader.py`, `README.md`, `ExportVideoDialog`, `raycast_mesh`, `body_regions.py`, `Coefficients`, `section_segments`, `step`, `BodyRegionSettings`, `section.py`, `FilmExport`, `test_skeleton.py`, `Progress`, `test_forms.py`, `PrimaryForm`, `cube`, `test_objects.py`, `test_skin.py`, `test_plane_solids.py`, `.source_mesh`, `test_leaning_on_position_breaks_a_form_up_as_well_as_down`, `SkinEdit`, `lumpy`, `PlaneSettings`, `viewport.py`, `box`, `main_window.py`, `OrientationSettings`, `FormStore`, `Path`, `plane_axes`, `SectionSettings`, `Path`, `VideoSettings`, `Landmark`?**
  _High betweenness centrality (0.165) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `._upload_sculpt`, `._sync_scene`, `test_preferences.py`, `AnnotateTool`, `ExportLook`, `MainWindow`, `ViewerState`, `._picker`, `SurfacePicker`, `PoseTool`, `.paintGL`, `FilmRecorder`, `.__init__`, `film_export.py`, `._place_armature_node`, `sample_count`, `ExportVideoDialog`, `._active_changed`, `FilmExport`, `MeasureTool`, `test_forms.py`, `application.py`, `.__init__`, `PrimaryForm`, `test_objects.py`, `._place_joint`, `ObjectTool`, `._place_form_landmark`, `ArmatureTool`, `NavigationController`, `._commit_node_drag`, `viewport.py`, `ViewportRenderPreview`, `main_window.py`, `.mouseReleaseEvent`, `ViewportOverlay`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `test_preferences.py`, `Viewport`, `SceneObject`, `trace/scene.py`, `MainWindow`, `RenderController`, `Armature`, `CameraPanel`, `SurfacePicker`, `test_body_regions.py`, `test_planes_panel.py`, `PoseTool`, `RenderView`, `render_window.py`, `ShadingPanel`, `panel`, `.__init__`, `skeleton.py`, `README.md`, `body_regions.py`, `test_matcap_preview.py`, `BodyRegionSettings`, `test_skeleton.py`, `test_render_panel.py`, `application.py`, `.__init__`, `PrimaryForm`, `test_objects.py`, `test_workspace_layout.py`, `.source_mesh`, `SkinSettings`, `test_custom_panels.py`, `SkinEdit`, `._commit_objects`, `viewport.py`, `MatcapPanel`, `main_window.py`, `RenderWindow`, `test_elements.py`, `Mesh`, `OrientationSettings`, `OverlayParts`, `Path`, `Task`, `Session`, `ViewportOverlay`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._
- **Are the 60 inferred relationships involving `Mesh` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Mesh` has 60 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `OverlayParts`) actually correct?**
  _`ViewerState` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Skeleton` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Skeleton` has 9 INFERRED edges - model-reasoned connections that need verification._