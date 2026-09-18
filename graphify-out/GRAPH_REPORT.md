# Graph Report - reference-viewer  (2026-09-18)

## Corpus Check
- 157 files · ~504,890 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5429 nodes · 12536 edges · 211 communities (186 shown, 25 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 596 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `82c89fec`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SettingsWindow
- test_preferences.py
- Release
- Viewport
- SceneObject
- settings.py
- MainWindow
- Stroke
- GifWriter
- viewport.py
- SceneRenderer
- naming.py
- main_window.py
- MeshBuffers
- Armature
- environment.yml
- .apply_session
- ._holds
- FrameTarget
- CameraPanel
- SetAttributes
- ShaderProgram
- test_hotkeys.py
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- Writer
- SectionSettings
- plane_volume.py
- ControlsWindow
- TriangleIndex
- ShadingPanel
- PlaneSettings
- test_camera.py
- test_plane_clusters.py
- WakeLock
- ._built
- MatcapPreview
- CustomPanel
- film_export.py
- forms.py
- Camera
- .abandon
- ValueSlider
- gltf_loader.py
- ExportVideoDialog
- open_writer
- landmarks.py
- Agent Graph-First Instructions
- VideoSettings
- Mesh
- test_matcap_preview.py
- test_armature.py
- ._selected_landmark
- .refresh_list
- HotkeyMap
- FilmExport
- FormsPanel
- PlanesPanel
- test_skeleton.py
- mesh_renderer.py
- Workspace
- ui/hotkeys.py
- test_forms.py
- application.py
- MeasureTool
- Link
- PrimaryForm
- rigging.py
- test_objects.py
- AnnotatePanel
- test_plane_solids.py
- ObjectTool
- session.py
- SurfacePicker
- texture.py
- load_matcap_pixels
- test_custom_panels.py
- ViewerState
- core/preferences.py
- _wires
- NavigationController
- Bounds
- ._commit_objects
- test_forms_panel.py
- test_asking_for_more_masses_never_costs_the_clay_its_detail
- SectionGizmo
- build_form
- MatcapPanel
- ColorButton
- Frame
- _Encoder
- _derived
- test_elements.py
- frame.py
- core/__init__.py
- ReflowLayout
- Measurement
- ArmatureSettings
- OrientationSettings
- clone.py
- skin_refinement.py
- Path
- ._turn
- .mouseReleaseEvent
- test_panel_docks.py
- MarkerVisibility
- ._place_armature_node
- HotkeyBinder
- armature.py
- DockTitle
- test_reflow.py
- .add_mesh
- Skeleton
- GridSettings
- ._build_objects
- test_open_files.py
- Joint
- test_session.py
- AddItem
- ViewportOverlay
- ArmaturePanel
- ArmatureStore
- ._selected
- _tab_switch
- Reflow
- Side
- SectionPanel
- lock_icon
- ._sync_scene
- .stage_images
- AnnotateTool
- ExportLook
- make_switch
- preview
- ._build
- .install
- UpdateChecker
- elements/__init__.py
- OpenRequests
- _drag_over
- PanelDock
- ._chosen_armature
- MatcapSettings
- ._picker
- in_flight
- .load
- app
- HotkeyStore
- .dress_tabs
- .refresh_list
- test_resetting_the_layout_puts_the_docks_back_at_once
- .update_enabled
- SkeletonStore
- restored
- test_resetting_keeps_the_panels_built_by_hand
- ._selected_rows
- test_the_switch_is_not_squeezed_to_nothing
- shaders.py
- .paintGL
- write
- Buried
- .column_of
- FormRun
- Human Skin renderer
- orientation.py
- lumpy
- ball
- ndarray
- sample_count
- _height_of
- _file_drag
- simplified
- _NameOnlyDelegate
- ._active_changed
- panel
- raycast_mesh
- test_the_switch_on_a_dock_bar_is_the_panels_own_visibility
- trusted_roots
- app
- test_a_session_saved_without_panels_leaves_the_ones_open_alone
- test_a_panel_does_not_cover_its_own_title
- .refresh
- test_a_panel_can_be_taken_away_and_another_built_after_a_restore
- test_loading_a_session_over_a_restored_layout_survives
- test_the_dock_of_a_panel_taken_away_is_used_again
- ModelPanel
- ui/preferences.py
- ._commit_node_drag
- test_a_reused_dock_does_not_bring_the_old_panels_contents_with_it
- ._dress_soon
- release.yml
- test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else
- coarse_lattice
- block
- ._menu_action
- refview/__init__.py
- .new_armature
- .film_changed
- ._place_joint
- ._place_form_landmark
- box
- .with_landmark_at
- welded
- test_a_block_holds_every_point_it_was_measured_from
- test_a_hull_is_cut_from_every_side
- test_the_fill_leaves_a_flat_alone_and_closes_a_slot
- test_the_fill_never_takes_clay_away
- test_how_far_the_fill_reaches_says_how_wide_a_slot_it_closes
- test_a_lump_lies_in_the_box_it_says_it_does
- test_the_lumps_are_joined_as_a_volume_and_not_as_surfaces

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 192 edges
2. `ViewerState` - 148 edges
3. `Viewport` - 146 edges
4. `Camera` - 97 edges
5. `Skeleton` - 90 edges
6. `MainWindow` - 90 edges
7. `Armature` - 81 edges
8. `PrimaryForm` - 79 edges
9. `PlaneSettings` - 69 edges
10. `SurfacePicker` - 69 edges

## Surprising Connections (you probably didn't know these)
- `Terracotta clay matcap` --shares_data_with--> `available_matcaps()`  [INFERRED]
  resources/matcaps/clay_terracotta.png → src/refview/paths.py
- `The cut interior is flooded flat` --rationale_for--> `SceneRenderer`  [INFERRED]
  README.md → src/refview/render/mesh_renderer.py
- `Units are adopted, never guessed` --semantically_similar_to--> `STL and glTF import (1.1.0)`  [INFERRED] [semantically similar]
  README.md → CHANGELOG.md
- `Orthographic extent derived from FOV and distance` --rationale_for--> `Camera`  [EXTRACTED]
  README.md → src/refview/core/camera.py
- `Every document edit is a command` --rationale_for--> `SetAttributes`  [EXTRACTED]
  README.md → src/refview/core/commands.py

## Import Cycles
- 3-file cycle: `src/refview/ui/elements/__init__.py -> src/refview/ui/elements/clone.py -> src/refview/ui/elements/slider.py -> src/refview/ui/elements/__init__.py`
- 4-file cycle: `src/refview/ui/elements/__init__.py -> src/refview/ui/elements/custom.py -> src/refview/ui/elements/clone.py -> src/refview/ui/elements/slider.py -> src/refview/ui/elements/__init__.py`

## Hyperedges (group relationships)
- **The bundled matcap set** — resources_matcaps_clay_terracotta_matcap, resources_matcaps_charcoal_matcap, resources_matcaps_jade_matcap, resources_matcaps_steel_matcap, resources_matcaps_studio_white_matcap, resources_matcaps_wax_skin_matcap, tools_generate_matcaps_matcappreset, tools_generate_matcaps_render [INFERRED 0.85]
- **The four generic undo commands** — src_refview_core_commands_setattributes, src_refview_core_commands_additem, src_refview_core_commands_removeitem, src_refview_core_commands_replaceitems, src_refview_core_history_command, readme_every_edit_is_a_command [EXTRACTED 1.00]
- **Windows binary-compatibility decisions** — readme_pyside6_pinned_below_68, environment_pip_installed_binaries, environment_python_311, github_workflows_release_pyinstaller_build [INFERRED 0.75]

## Communities (211 total, 25 thin omitted)

### Community 0 - "SettingsWindow"
Cohesion: 0.15
Nodes (11): The preferences as they stand. Treat as read-only; use :meth:`set`., QWidget, Fill in the groups. A switch with nothing to put in the caption column is given…, Every command with its keys, each key a box that takes one keystroke. The list…, The one button that is not a preference, and what the window is for., Say what the view is really drawing with, beside what was asked for. A sample…, Put one field back into the store, which applies and saves it., Pull every control back into line with the store. Run when the window is built,… (+3 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.07
Nodes (44): _clamp(), Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, Pull anything out of range back into it. The window cannot produce these…, Read the preferences off the machine. Never raises., app(), model() (+36 more)

### Community 2 - "Release"
Cohesion: 0.09
Nodes (35): QRunnable, check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and… (+27 more)

### Community 3 - "Viewport"
Cohesion: 0.06
Nodes (15): QOpenGLWidget, Renders the scene and turns mouse gestures into camera and tool actions., Slide the view so a point sits at the centre, keeping the angle., The gesture a key press chooses, if the transform tool is armed to hear it., A form changed: work its clay out again and redraw., Hand the renderer how solid each object is now; nothing else moved., End any film being recorded, and wait for its thread to really stop. For…, The document being drawn. (+7 more)

### Community 4 - "SceneObject"
Cohesion: 0.07
Nodes (20): ObjectSettings, ObjectStore, ndarray, Snapshot, An angle in (-180, 180], with the floating-point dust brushed off., What a parent's state means for its children, and how the tools scale. Each is…, One model in the scene. Three meshes are kept, as the viewer kept them when…, Drop the derived meshes, after the rest mesh has been replaced. (+12 more)

### Community 5 - "settings.py"
Cohesion: 0.03
Nodes (83): QThread, auto_smooth(), A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, Coefficients, PlaneSet, One level of a fit: the planes the shader is to quantise against. A plane is a…, What each block of the design matrix counts for, against the normals. A fit…, Whether anything but the normals is being read at all. (+75 more)

### Community 6 - "MainWindow"
Cohesion: 0.05
Nodes (19): MainWindow, QMainWindow, Put every panel button and menu entry where the tools now stand. Only one tool…, Swap between the eraser and the drawing mode it was called from., Open the preferences, on one group when the menu asked for one., Push the preferences that this window's own parts hold a copy of. The store has…, Open an empty panel of the artist's own and bring it to the front., Put the docks and the hand-built panels back where they were. Unless the artist… (+11 more)

### Community 7 - "Stroke"
Cohesion: 0.05
Nodes (40): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+32 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "viewport.py"
Cohesion: 0.04
Nodes (83): Quat, Quat4, compose(), euler_to_quat(), matrix_to_quat(), quat_between(), quat_conjugate(), quat_from_axis_angle() (+75 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.07
Nodes (35): Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, light_directions(), normal_matrix(), ndarray, Point the shading pass at the shadow map and the occlusion buffer., Flood the exposed interior with a flat colour so the cut reads solid. The… (+27 more)

### Community 11 - "naming.py"
Cohesion: 0.15
Nodes (22): _asked(), caption_for(), element_id(), _free(), _from_id(), name_tree(), _named_after(), QWidget (+14 more)

### Community 12 - "main_window.py"
Cohesion: 0.05
Nodes (57): QScrollArea, The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, MatcapLoadError, RuntimeError, Raised when an image cannot be used as a matcap., framed(), A frame with a form layout in it, ready to be filled. (+49 more)

### Community 13 - "MeshBuffers"
Cohesion: 0.08
Nodes (14): current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., _ghost_depth_range(), MeshBuffers, Forget the contents without releasing the buffer objects., Where the form starts along the view, and how deep it is. The ghost weighs a…, Replace the model: the whole scene as one mesh, and the objects it is made of.…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The… (+6 more)

### Community 14 - "Armature"
Cohesion: 0.06
Nodes (39): Armature, ArmatureNode, Bone, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves., A plausible thickness for a node placed by hand. (+31 more)

### Community 15 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 16 - ".apply_session"
Cohesion: 0.12
Nodes (10): The skeletons changed; re-pose the model if one of them drives it. ``live`` is…, The skeleton bound to ``obj``'s rig, if one is and no other object has it., Join the shown objects into :attr:`mesh` and say that it changed. ``live``…, Open a model as the whole scene: centre it on the origin and frame it.…, The skeleton the active object follows, if it has one., A parenting policy changed: what is shown and how solid may have too., Turn the models, bringing the marks made on them along. Measurements,…, Carry the measurements, annotations, armature and forms through ``carry``. (+2 more)

### Community 17 - "._holds"
Cohesion: 0.13
Nodes (10): _matrix16(), A copy with the rest translation replaced and the frame kept., Every joint, parents before children. A file may list a child before its…, Every joint's transform in scene space, as ``(n, 4, 4)``. With ``rest`` the…, The list with a joint removed and its children re-hung from its parent. The…, The list with these joints removed and every survivor re-hung. Each kept joint…, The list with one joint re-hung from another, keeping its place. Refused -- the…, The list with one joint's rest position moved and its children left be. What… (+2 more)

### Community 18 - "FrameTarget"
Cohesion: 0.06
Nodes (23): AccumTarget, bind_default(), ColorTarget, DepthTarget, FrameTarget, GeometryTarget, Offscreen render targets used by the high-quality, ghost and smoothing passes.…, A depth-only framebuffer, sampled afterwards as a texture. (+15 more)

### Community 19 - "CameraPanel"
Cohesion: 0.11
Nodes (9): CameraPanel, QListWidgetItem, Take the planes in hand where the fit left them, or hand them back., Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions. (+1 more)

### Community 20 - "SetAttributes"
Cohesion: 0.05
Nodes (23): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, PosePanel, QTreeWidgetItem, QWidget, Run a row's edit once Qt has finished delivering the current signal., Arms the pose tool, lists the joints and poses the selected one., Adopt the viewport's tools: the pose tool, and the armature's for its selection. (+15 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.09
Nodes (14): OpenGL rendering layer: shader programs, textures and the scene renderer., ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError (+6 more)

### Community 22 - "test_hotkeys.py"
Cohesion: 0.10
Nodes (25): QKeySequence, lookup(), The control an id names, if the window still has it., app(), _map(), fixture, Hotkeys: the map, the store, the binder, and the gesture that assigns one., One offscreen Qt application for the run; see test_film_recorder. (+17 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.08
Nodes (21): _names(), The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as…, Or there would be no way to turn one back on., A limb is four bones, and deciding not to block the arms in is one decision.…, It is rebuilt on every change, and ticking one row of a selected limb would be… (+13 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.10
Nodes (11): MeasurePanel, _NameOnlyDelegate, QStyledItemDelegate, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing… (+3 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.14
Nodes (7): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., test_bookmarks_cycle_and_wrap()

### Community 26 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 27 - "SectionSettings"
Cohesion: 0.07
Nodes (33): The cut interior is flooded flat, Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every… (+25 more)

### Community 28 - "plane_volume.py"
Cohesion: 0.04
Nodes (114): Work the form stage by stage, handing each one back as it is finished. A…, record(), _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field() (+106 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "TriangleIndex"
Cohesion: 0.13
Nodes (17): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Box the leaves up, coarsest level first and the leaves themselves last., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the… (+9 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.14
Nodes (10): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Slot that writes one field of the contour shading settings., Slot that writes one field of the grid settings., Freeze the slices the way the camera faces now. The view direction is the one… (+2 more)

### Community 32 - "PlaneSettings"
Cohesion: 0.06
Nodes (38): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor…, How much of a turn in the surface one plane covers, in degrees. Linear in…, The grid step, in cube-face coordinates, that gives that span. A cell of this…, The design-matrix settings, in the form the fitters want them., How many planes a mode fitted to the model keeps. The climb from two planes to… (+30 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.07
Nodes (51): The joint list with ``index`` resting at ``target`` and its children left be., angle_deg(), bent_plate(), cube(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What… (+43 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (32): c_void_p, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., Holds sleep off while the window that owns it is the one in front. The class… (+24 more)

### Community 36 - "._built"
Cohesion: 0.25
Nodes (5): QImage, QRect, The matcap as a picture, at its own resolution. Square and opaque, with the…, Where the sphere goes: square, centred, above the legend., The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…

### Community 37 - "MatcapPreview"
Cohesion: 0.09
Nodes (12): QMenu, MatcapPreview, Path, QSize, A matcap on a sphere, which is also how the matcap is graded., Redraw from the settings, which something else has changed., Offer the picture back as a file: as graded here, or as it came. A grading…, Put the grading back, which is the one thing a disc cannot show. (+4 more)

### Community 38 - "CustomPanel"
Cohesion: 0.08
Nodes (26): carried(), clone(), A working copy of ``source``, or ``None`` if its kind cannot be copied., Read a drag's payload back, or ``None`` if it is not one of ours., Make every control under ``root`` that can be copied Alt-draggable. A group is…, watch_tree(), CustomPanel, _detach() (+18 more)

### Community 39 - "film_export.py"
Cohesion: 0.08
Nodes (17): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+9 more)

### Community 40 - "forms.py"
Cohesion: 0.05
Nodes (55): convex_hull(), DegenerateHullError, flat_mesh(), merged(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary… (+47 more)

### Community 41 - "Camera"
Cohesion: 0.06
Nodes (27): Orthographic extent derived from FOV and distance, Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., Camera, ndarray, Near/far planes fitted to the scene bounding sphere., The near and far planes this frame: the fitted ones, unless set by hand. A…, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget… (+19 more)

### Community 42 - ".abandon"
Cohesion: 0.33
Nodes (3): Stop any recording in flight and forget what it was making. The thread is asked…, Let every thread finish, for shutdown. The only place waiting is the right…, Ask the recording to end at the next stage boundary. Called from the GUI…

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (11): _pull_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end., Set the value the way a hand on the control would., The value the track stands at ``x`` pixels across. (+3 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.07
Nodes (43): Units are adopted, never guessed, _accessor(), _buffers(), _first_skin(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry() (+35 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.10
Nodes (13): QProgressDialog, even(), ExportVideoDialog, Path, QDialog, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+5 more)

### Community 46 - "open_writer"
Cohesion: 0.08
Nodes (28): _encode_arguments(), _encoders(), ffmpeg_path(), _FFmpegWriter, _no_window(), open_writer(), Path, RuntimeError (+20 more)

### Community 47 - "landmarks.py"
Cohesion: 0.16
Nodes (18): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _humanoid_landmarks(), _mid(), Enum (+10 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "VideoSettings"
Cohesion: 0.18
Nodes (7): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, TestTiming

### Community 50 - "Mesh"
Cohesion: 0.03
Nodes (85): Mesh, Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Return a copy carried by a full 4x4 -- a move, a turn and a scale together.…, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, _empty(), plane_axes(), PlaneAxes (+77 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.09
Nodes (34): QPoint, _drag(), parametrize, The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc., Dragging further than the range goes is not a negative gamma., Alt and a drag copies a control; the disc must not swallow that. (+26 more)

### Community 52 - "test_armature.py"
Cohesion: 0.08
Nodes (54): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _chain(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other., The femoral head is in from the ASIS, below it and behind it, by shares of the… (+46 more)

### Community 53 - "._selected_landmark"
Cohesion: 0.12
Nodes (7): Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors., Show the landmark group only once there are landmarks to show., The landmark the highlighted row stands for, if the row is one., Which armature the landmark list is pointing into, row or heading., Follow the highlighted landmark, and say which one it is in the view.

### Community 54 - ".refresh_list"
Cohesion: 0.22
Nodes (5): QTreeWidgetItem, The landmarks in the preset's own order, top of the figure down. Placement…, Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing., Commit a renamed or re-checked row, if anything actually changed.

### Community 55 - "HotkeyMap"
Cohesion: 0.08
Nodes (18): Command, HotkeyMap, Any, Which keys do what, as the artist has decided rather than as it ships. A hotkey…, Whether the artist has moved this command off what it ships with., Which command has these keys, if any., Every command with keys on it, declared or not, as id -> keys., Put ``keys`` on a command, taking them off whatever had them. Returns the id of… (+10 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (11): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+3 more)

### Community 57 - "FormsPanel"
Cohesion: 0.04
Nodes (38): form_spec(), The recipe a form is built by: its preset, or a freeform's own., FormsPanel, QPushButton, QTreeWidgetItem, QWidget, A strip of buttons that one form row can show or hide as a unit., Arms the forms tool, runs the guided presets and lists what they built. (+30 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.14
Nodes (10): PlanesPanel, Lay one length of wire earlier or later, as one undoable step., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Show what this way of working needs, and put the rest away. A setting that does…, The line under the normals slider: what the setting has asked for., Breaks the form into planes, in the shading or in the geometry itself., Re-read the armatures and what the chosen one is laying down. Called whenever… (+2 more)

### Community 59 - "test_skeleton.py"
Cohesion: 0.10
Nodes (32): looks_humanoid(), Whether a guessed mapping is enough of a figure to be worth offering., The model as ``skeleton`` poses it, or ``rest`` itself when it cannot. Linear…, skinned_mesh(), _arm(), ndarray, parametrize, Skeletons: the joint tree, posing, skinning, and where skeletons come from. (+24 more)

### Community 60 - "mesh_renderer.py"
Cohesion: 0.10
Nodes (28): _distance_or_none(), Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., A clipping distance as a file wrote it, or ``None`` for one left to the fit., look_at() (+20 more)

### Community 61 - "Workspace"
Cohesion: 0.12
Nodes (10): _number_in(), QMainWindow, QObject, Keep every switch agreeing with the panel it speaks for., An empty panel of the artist's own, docked on the right. A dock put away…, Take a parked dock back out under ``key``, emptied and renamed., Open the dock a hand-built panel lives in and bring it to the front., The number at the end of a custom panel's key, or nought. (+2 more)

### Community 62 - "ui/hotkeys.py"
Cohesion: 0.07
Nodes (35): QKeySequenceEdit, assign(), control_of(), decorate(), describe(), forget(), group_of(), HotkeyDialog (+27 more)

### Community 63 - "test_forms.py"
Cohesion: 0.06
Nodes (62): _across(), blend_rings(), build_head(), build_pelvis(), build_ribcage(), fit_plane(), _head_frame(), _lagrange() (+54 more)

### Community 64 - "application.py"
Cohesion: 0.10
Nodes (31): ArgumentParser, Namespace, QSplashScreen, REFVIEW_RESOURCES resource override, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font() (+23 more)

### Community 65 - "MeasureTool"
Cohesion: 0.10
Nodes (15): MeasurementSettings, How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., MeasureTool, Handle, ndarray, The nearest grabbable endpoint under the cursor, if any. Only unlocked, visible…, Consume a picked point; returns a measurement on the second click. (+7 more)

### Community 66 - "Link"
Cohesion: 0.11
Nodes (10): CloneGesture, Link, _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original., Whether the copy is being used right now and must not be written. (+2 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.05
Nodes (48): FormLandmarkRef, PlacedLandmark, One anatomical point the artist put on the model during a guided run., _centre(), FormSettings, FormStore, PrimaryForm, Point3 (+40 more)

### Community 68 - "rigging.py"
Cohesion: 0.09
Nodes (25): What to call the joint filling a humanoid slot: ``"knee.L"`` is ``"Knee L"``., What to call a landmark in a menu or an undo step. The preset's own words when…, The name with its side, for a prompt., role_name(), armature_root(), build_humanoid_skeleton(), humanoid_positions(), humanoid_roles() (+17 more)

### Community 69 - "test_objects.py"
Cohesion: 0.12
Nodes (30): Path, Where an object stands relative to its parent: an affine placement. Held as the…, Transform, app(), _key(), _mouse(), _overridden(), fixture (+22 more)

### Community 70 - "AnnotatePanel"
Cohesion: 0.19
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 71 - "test_plane_solids.py"
Cohesion: 0.07
Nodes (59): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), dumbbell(), edge_use(), flatness(), parametrize (+51 more)

### Community 72 - "ObjectTool"
Cohesion: 0.11
Nodes (15): _axis_param(), Gizmo, _Grip, ObjectTool, ndarray, The three directions the arms run along, in world space. A move and a turn are…, Where the gizmo for an object at ``world`` falls on screen, or ``None`` if…, Which handle a screen point is over: ``"centre"``, ``"x"``, ``"y"``, ``"z"`` or… (+7 more)

### Community 73 - "session.py"
Cohesion: 0.10
Nodes (24): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Path (+16 more)

### Community 74 - "SurfacePicker"
Cohesion: 0.04
Nodes (38): BoneRef, JointRef, LandmarkRef, ArmatureTool, _project(), Handle, Where a click at ``(x, y)`` would put a node. With free placement the node…, Where a grabbed node should move to. Free placement -- and a drag that wanders… (+30 more)

### Community 75 - "texture.py"
Cohesion: 0.11
Nodes (11): DataTexture, default_matcap_pixels(), ndarray, Matcap texture loading and upload, and the small data table beside it., An RGBA16F 2D texture with clamped edges and mipmapped minification., Store a ``(depth, height, width, 4)`` float array., A neutral studio matcap, used before the user picks one., A small RGBA32F table the shader reads exact values out of. Not a picture:… (+3 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.15
Nodes (22): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+14 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.07
Nodes (24): QMimeData, The slider the whole application is set with. One flat bar: the name of the…, app(), custom(), _drop_on(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error. (+16 more)

### Community 78 - "ViewerState"
Cohesion: 0.06
Nodes (27): Qt user interface: the viewport widget, the panels and the main window., Command, QObject, Snapshot, A rest mesh as a file would store it, so that re-orienting it comes back to…, Everything the viewer displays, plus change notifications., Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a… (+19 more)

### Community 79 - "core/preferences.py"
Cohesion: 0.12
Nodes (18): _as_kind_of(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any, What the artist prefers, as distinct from what the document says. There are two… (+10 more)

### Community 80 - "_wires"
Cohesion: 0.11
Nodes (32): The order the artist put the bones in is what the scrub walks through, which is…, The claim the whole film rests on, asked again with an armature under it: an…, test_a_film_of_clay_on_a_wire_lays_it_down_in_the_order_it_was_listed(), test_the_last_stage_of_a_film_on_a_wire_is_the_form_the_slider_gives(), _bar(), _bed_for(), _holds(), A long ellipsoid: one closed form with an obvious axis to lie along. (+24 more)

### Community 81 - "NavigationController"
Cohesion: 0.07
Nodes (28): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Degrees of yaw per pixel, signed by whether the drag is inverted. (+20 more)

### Community 82 - "Bounds"
Cohesion: 0.08
Nodes (28): Shift-snapped orbiting (1.1.0), High Quality shading mode (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding (+20 more)

### Community 83 - "._commit_objects"
Cohesion: 0.10
Nodes (14): ObjectsEdit, ndarray, Move each bound skeleton by however far its object moved since ``before``., Put the objects back as a snapshot had them -- how a gesture is cancelled., Record the list as it is now against ``before``, and rebuild. ``geometry`` off…, Put ``obj`` at ``transform`` for the frames of a drag, without recording it., Put ``obj`` at ``transform`` as one undo step -- the panel's boxes., Make ``obj`` the active object. Not an edit: nothing is undone. (+6 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.12
Nodes (29): app(), _click(), panel(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The… (+21 more)

### Community 86 - "SectionGizmo"
Cohesion: 0.15
Nodes (10): draw_rail(), The screen-space cue for one degree of freedom. A vertical rail that fades out…, A screen-space rail for sliding the cutting plane along its normal. The rail…, Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo, The rail stands still while the camera moves, and never leaves the frame. (+2 more)

### Community 87 - "build_form"
Cohesion: 0.07
Nodes (46): build_form(), built_count(), form_landmark_title(), form_mesh(), landmark_signature(), median_plane_ready(), mirror_form_landmarks(), ndarray (+38 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.17
Nodes (8): MatcapPanel, Rebuild the thumbnail list from the resources folder., The disc was dragged: show the renderer and the numbers what it did., A different matcap: the disc draws whichever one is on the model., Put the numbers back in line with the settings, and redraw the disc. Separate…, Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, test_the_disc_draws_the_matcap_that_is_on_the_model()

### Community 89 - "ColorButton"
Cohesion: 0.11
Nodes (11): _pull_swatch(), _push_swatch(), _AxisBox, ColorButton, QColor, QDoubleSpinBox, QSize, QWidget (+3 more)

### Community 90 - "Frame"
Cohesion: 0.08
Nodes (16): _pull_frame(), _push_frame(), Nothing: each row inside the copy is linked on its own., Frame, FrameBar, QFormLayout, QPainter, QSize (+8 more)

### Community 91 - "_Encoder"
Cohesion: 0.25
Nodes (5): Queue, _Encoder, QObject, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 92 - "_derived"
Cohesion: 0.08
Nodes (29): _kept_laying(), Fresh bones, laid the way the armature was already laying them. The bone list…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _derived(), A guess the artist corrects is theirs, and the mirror leaves it alone., The new list is the edit; the old one has to survive to be undone to., Mirroring moves a guess in place, which must not reach the undo history. (+21 more)

### Community 93 - "test_elements.py"
Cohesion: 0.07
Nodes (23): app(), fixture, Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., A matcap has no light to aim, so the Light group goes -- and its space. The… (+15 more)

### Community 94 - "frame.py"
Cohesion: 0.09
Nodes (22): One dock per panel, with a bar of its own across the top. Every panel is its…, A titled frame that folds away behind its own bar. Every group of controls in…, Whether a group that goes dead folds away or merely greys out. Turning it back…, set_fold_disabled(), css(), outline(), QColor, The colours the hand-drawn elements paint with. Kept apart from… (+14 more)

### Community 95 - "core/__init__.py"
Cohesion: 0.04
Nodes (93): STL and glTF import (1.1.0), Annotations drawn as widened geometry, core never imports Qt, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Panels edit dataclasses, never foreign widgets, render owns every GL call, Named camera positions the artist can jump between while sculpting. (+85 more)

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - "Measurement"
Cohesion: 0.10
Nodes (13): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+5 more)

### Community 98 - "ArmatureSettings"
Cohesion: 0.12
Nodes (23): ArmatureSettings, How the armature is drawn, and how new nodes are placed., The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now., How many landmarks are placed, out of how many will be asked for., Pass over the landmark being asked for; the figure loses what it fed., Un-skip or un-place the landmark before this one, and ask again. Returns the…, _at() (+15 more)

### Community 99 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 100 - "clone.py"
Cohesion: 0.05
Nodes (65): QAbstractButton, QComboBox, QLineEdit, QSlider, QSpinBox, _begin(), can_clone(), _clone_button() (+57 more)

### Community 101 - "skin_refinement.py"
Cohesion: 0.05
Nodes (51): build_scene(), ndarray, Stackless BVH tables for the OpenGL 3.3 skin tracer (no compute extension).…, Build on a worker from the immutable meshes currently drawn by the renderer., Pack a linear texel array within the driver's actual 2D texture limit., texture_table(), TraceScene, burley_marginal() (+43 more)

### Community 102 - "Path"
Cohesion: 0.12
Nodes (13): opens_as(), Path, Pick up whatever was last being worked on, if that was asked for. A session…, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window., Ask whether a rig that arrived with the model should be read as a figure. Only…, Add a model to the scene beside what is already there. (+5 more)

### Community 103 - "._turn"
Cohesion: 0.33
Nodes (5): _angle(), Turn the matcap by the angle the cursor swept about the centre. By angle and…, The angle of ``point`` about ``centre``, anticlockwise with y upwards., An angle difference brought back into -pi to pi., _wrapped()

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.11
Nodes (10): Record the finished drag as a single undo step., Alt forces the camera gesture, whichever tool is armed., Record the finished drag as one step, or read a press as a selection., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Make the object under the cursor the active one., Record the finished pull as one step, or read a press as a selection., Track the joint and bone under the cursor; True when either changed. (+2 more)

### Community 105 - "test_panel_docks.py"
Cohesion: 0.14
Nodes (3): Each panel in a dock of its own, and putting the docks back next time. Two…, test_a_restored_copy_drives_the_new_windows_own_control(), test_the_layout_comes_back_through_the_settings()

### Community 106 - "MarkerVisibility"
Cohesion: 0.18
Nodes (5): MarkerVisibility, Cache surface occlusion by view and position for every kind of marker. The…, Whether the last pass is recent enough to be read instead of repeated., Mark these points as standing in front of the surface, untested. For frames…, Answer for a batch of points at once, ahead of being asked one by one. Every…

### Community 107 - "._place_armature_node"
Cohesion: 0.15
Nodes (6): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…, The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, A skeleton changed: redraw it., Hand the renderer a re-posed model and nothing else. For the frames of a pose…

### Community 108 - "HotkeyBinder"
Cohesion: 0.12
Nodes (16): QShortcut, ask_for(), command_for(), HotkeyBinder, Command, QAction, QObject, The command a control stands for, or ``None`` if it has no name to go by. A… (+8 more)

### Community 109 - "armature.py"
Cohesion: 0.09
Nodes (19): A graph of named points under the form, and the wire it stands for. An armature…, mirror_landmarks(), Preset, An ordered set of landmarks and the armature they build., The landmarks worth asking for under these choices. With mirroring on the…, The midline landmarks, which are what the median plane is fitted to., The landmark list with every paired landmark reflected into place. A point the…, GuideRun (+11 more)

### Community 110 - "DockTitle"
Cohesion: 0.15
Nodes (7): QToolButton, DockTitle, QSize, QWidget, The bar across the top of a dock: a switch, a name and two buttons., As tall as the bar really is. A dock puts the panel directly below its title…, StandardPixmap

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - ".add_mesh"
Cohesion: 0.11
Nodes (16): setter, ObjectRecord, What a session writes down about an object; the mesh itself stays in its file., Path, Open every object a session names, as the whole scene., Lay a session's object records over the objects already open. For the sidecar…, A path as a key two spellings of one file agree on., The active object turned and centred but not posed or placed. (+8 more)

### Community 113 - "Skeleton"
Cohesion: 0.11
Nodes (10): A tree -- or a forest -- of joints and the pose they stand in., Every joint below ``index``, nearest first., Where every joint sits, as ``(n, 3)``., Every ``(parent, child)`` pair, parents first., How long the bone above joint ``index`` is, or zero for a root., Whether any joint answers to a name out of the model's own rig., The list with a joint and everything below it removed., Skeleton (+2 more)

### Community 114 - "GridSettings"
Cohesion: 0.14
Nodes (18): build_grid(), GridLines, GridSettings, nice_step(), Reference grids on the three axis planes, fading with distance. A grid gives…, Segments, with their colours and widths, ready for the stroke buffer., Every line of every enabled grid, or ``None`` when none is on., The nearest 1, 2 or 5 times a power of ten at or below ``value``. (+10 more)

### Community 115 - "._build_objects"
Cohesion: 0.18
Nodes (9): _NameOnlyDelegate, _ObjectTree, QPushButton, QStyledItemDelegate, QWidget, Allows in-place editing of the name column only., A tree whose rows can be dropped onto one another to hang one from another. Qt…, A strip of buttons that one form row can show or hide as a unit. (+1 more)

### Community 116 - "test_open_files.py"
Cohesion: 0.15
Nodes (11): app(), opened(), fixture, parametrize, Files arriving from outside: the command line, a drop, or the desktop's "Open…, One offscreen Qt application for the run; see test_film_recorder., What the window was asked to open, by kind, without loading anything., Finder sends the launching file as an event, which can land before the window. (+3 more)

### Community 117 - "Joint"
Cohesion: 0.12
Nodes (11): Joint, _pose_matrices(), ndarray, Whether the pose differs from the rest at all., The list with ``joint`` appended, hung from whatever it names., The list with these joints -- or every joint -- put back at rest., One joint: where it sits at rest, and how it is turned right now., A document skeleton standing exactly where the file's joints stand. (+3 more)

### Community 118 - "test_session.py"
Cohesion: 0.10
Nodes (19): Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., A step of the slider is worth a fixed share more planes, not a fixed number of…, The ceiling went from 64 planes to 256 without moving the slider under anyone:…, The panel edits the settings; the fit has to be told what they are., Both modes answer in degrees of turn, so the panel can just ask., Version 1 files predate the annotation layer and the endpoint lock., Version 6 files predate panels being something a session could carry. (+11 more)

### Community 119 - "AddItem"
Cohesion: 0.06
Nodes (27): Camera motion is deliberately not undoable, Every document edit is a command, AddItem, Any, Command, Append an item to a document list., Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the… (+19 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.08
Nodes (36): QPointF, QRectF, draw_text(), One marker object for endpoints, nodes, landmarks and tool previews., Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, VisualMarker, project_visible(), project_visible_many() (+28 more)

### Community 121 - "ArmaturePanel"
Cohesion: 0.14
Nodes (5): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Take back the landmark before this one and ask for it again., Record an edit the viewport's tool worked out., The multiplier the position boxes are read and written through.

### Community 122 - "ArmatureStore"
Cohesion: 0.16
Nodes (5): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied., test_an_armature_survives_a_session_round_trip()

### Community 123 - "._selected"
Cohesion: 0.14
Nodes (7): Run a row's edit once Qt has finished delivering the current signal. Committing…, Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., Run a bone between the row selected now and the node held before it., Join two nodes of one armature, if they are two and they are one armature., The node the selected row stands for, if the row is a node at all., The armature the selected row stands for, when the row is not a node.

### Community 124 - "_tab_switch"
Cohesion: 0.29
Nodes (7): The show/hide switch on the tab named ``title``, if it has one., Stacked behind another panel is where the switch is worth the most., It is fifteen pixels wide and carries no words, which is exactly the shape the…, _tab_switch(), test_a_panel_that_draws_nothing_gets_no_switch_on_its_tab(), test_a_tabbed_panel_still_shows_its_switch(), test_clicking_the_switch_on_a_tab_works()

### Community 125 - "Reflow"
Cohesion: 0.30
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 126 - "Side"
Cohesion: 0.15
Nodes (16): freeform_landmark(), landmark_key(), paired_landmarks(), The side a landmark key ends in., The key of the landmark across the midline from this one; empty on the midline., A key for a freshly named landmark, and the name it will go by. The key is the…, A landmark the artist has just named, keyed so it does not collide., A freeform's landmarks with each side's twin worked in. A point placed on the… (+8 more)

### Community 127 - "SectionPanel"
Cohesion: 0.17
Nodes (7): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 128 - "lock_icon"
Cohesion: 0.27
Nodes (10): QIcon, _draw_glyph(), glyph(), lock_icon(), QColor, QPixmap, Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if… (+2 more)

### Community 129 - "._sync_scene"
Cohesion: 0.11
Nodes (7): Regenerate the pedestal and the cut contour when their settings move. Both are…, Rebuild the reference grids for the scene as it stands., The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on., Cut the mesh with each section plane and expand the result to strokes.

### Community 130 - ".stage_images"
Cohesion: 0.21
Nodes (7): QOpenGLFramebufferObject, QImage, One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A…, An offscreen target the frames are drawn into, made once per export.…, Draw the scene into ``surface`` and read it back as an image., Lay the overlay -- and the caption, if it was asked for -- on a frame. Painted…

### Community 131 - "AnnotateTool"
Cohesion: 0.09
Nodes (19): AnnotateMode, AnnotationSettings, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a… (+11 more)

### Community 132 - "ExportLook"
Cohesion: 0.08
Nodes (22): The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, ExportLook, What the frames are to look like, as against what they are of. Laid over the…, Which of the things drawn over the model belong in the frames., ``base`` with this export's choices laid over it. (+14 more)

### Community 133 - "make_switch"
Cohesion: 0.28
Nodes (6): make_switch(), QCheckBox, Put a show/hide switch at the left of the bar and return it., A square that is on or off, and is clickable all over. A check box decides…, The square that shows or hides what a panel draws. One is kept on each dock's…, Switch

### Community 134 - "preview"
Cohesion: 0.40
Nodes (5): app(), preview(), fixture, One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "._build"
Cohesion: 0.25
Nodes (7): QTreeWidget, QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 136 - ".install"
Cohesion: 0.29
Nodes (6): QApplication, Put the rule in place for every switch in the application., The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter., test_a_switch_answers_a_press_anywhere_on_its_face(), test_alt_is_left_alone_so_a_switch_can_still_be_copied()

### Community 137 - "UpdateChecker"
Cohesion: 0.16
Nodes (8): Ask GitHub for the newest release in the background. The startup check is…, QObject, QWidget, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., show_failure_dialog(), show_up_to_date_dialog(), UpdateChecker

### Community 138 - "elements/__init__.py"
Cohesion: 0.12
Nodes (16): The widgets the panels are built out of, and the rules they follow. Four ideas,…, can_take_key(), is_hotkey_click(), KeyGesture, QObject, QWidget, The gesture that puts a key on a control: Ctrl/Cmd, Alt and a click. It sits…, Whether a mouse press is the assignment gesture rather than a click. (+8 more)

### Community 139 - "OpenRequests"
Cohesion: 0.15
Nodes (8): Application, OpenRequests, Path, QApplication, The Qt application, listening for the desktop's way of handing over a file., Files the desktop asked the viewer to open, kept until there is a window. On…, Open ``path`` in the window, or hold it until there is one., Name the window files go to, and hand over any that came early.

### Community 140 - "_drag_over"
Cohesion: 0.22
Nodes (10): _drag_over(), _middle_of_the_view(), A drag of ``holder`` arriving at ``point`` in the window's coordinates. A real…, The gesture the whole thing rests on: drag it onto the model, it goes., A gesture that destroys something only fires where it clearly meant to., Refused at the door it would never reach the model; so it is let in., test_a_copy_dropped_on_the_model_is_thrown_away(), test_a_copy_is_let_into_the_window_wherever_it_arrives() (+2 more)

### Community 141 - "PanelDock"
Cohesion: 0.18
Nodes (5): QDockWidget, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top., QWidget, Give a panel a dock of its own, stacked with the ones before it.

### Community 142 - "._chosen_armature"
Cohesion: 0.24
Nodes (6): QListWidgetItem, The armature the clay is being built on, or ``None``. An index past the end of…, The bones of the chosen armature, in the order the clay goes down. Every intact…, Take lengths of wire out of the clay, or put them back. A tick on a row that…, Put the clay on all of the wire, or take it off all of it., Write which lengths of wire take clay, as one undoable step.

### Community 143 - "MatcapSettings"
Cohesion: 0.13
Nodes (19): MatcapSettings, Post-processing applied to the sampled matcap texel., _clone_preview(), grade(), _pull_preview(), _push_preview(), ndarray, QWidget (+11 more)

### Community 144 - "._picker"
Cohesion: 0.08
Nodes (13): ndarray, Rub out the stroke points under the eraser, live., Take hold of a node, to move it, resize it, or just to select it. This works…, Apply the drag live, so the artist sees the wire bend as they pull it., Take hold of a landmark, to move it or just to say which one it is., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Object centre, which anchors the plane the orbit pivot lies on. (+5 more)

### Community 145 - "in_flight"
Cohesion: 0.19
Nodes (5): in_flight(), Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model., Take a copied control out of whichever hand-built panel holds it.

### Community 146 - ".load"
Cohesion: 0.15
Nodes (8): forget(), Drop every id under a prefix; for a panel that has been thrown away., QSettings, Take a hand-built panel away. Its dock is parked, not destroyed. The dock has…, The part of the layout Qt cannot describe., Rebuild the panels built by hand. Call before :meth:`restore_state`. Whatever…, Write the whole layout, ours and Qt's, into the settings., Put the layout back. Returns whether there was one to put back.

### Community 147 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 148 - "HotkeyStore"
Cohesion: 0.22
Nodes (6): HotkeyStore, QSettings, Put ``keys`` on a command; says what they came off, if anything., Read the choices off the machine. Never raises., The map, and one signal saying it has changed., The map as it stands. Treat as read-only; change it through the store.

### Community 149 - ".dress_tabs"
Cohesion: 0.29
Nodes (5): QTabBar, Hang a show/hide switch on every dock tab that wants one. A dock stacked behind…, The panel whose dock is called ``title``, if there is one., Let a strip of tabs keep its names, and scroll if they do not fit. Ten panels…, _widen()

### Community 150 - ".refresh_list"
Cohesion: 0.15
Nodes (5): QTreeWidgetItem, Rebuild the tree from the store, with the active object current., Offer every object the active one could hang from., The objects whose rows are selected, in list order., Commit a renamed or re-checked row, if anything actually changed.

### Community 152 - ".update_enabled"
Cohesion: 0.17
Nodes (6): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., Follow the highlighted row, without rebuilding the list underneath it. Going…, Highlight the row for a node picked in the view., Highlight the row for a landmark picked in the view.

### Community 153 - "SkeletonStore"
Cohesion: 0.18
Nodes (3): An ordered collection of skeletons, like the other document stores., The skeleton the model follows: the first one bound to its rig., SkeletonStore

### Community 154 - "restored"
Cohesion: 0.29
Nodes (7): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., A window with the saved layout out of the way, and put back after. Shown,…, A second window, built from a layout the first one saved. The point is…, restored(), window()

### Community 158 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 159 - ".paintGL"
Cohesion: 0.29
Nodes (3): Use the same cached visibility test for bones and all point markers., Which part wears the line this frame, and how solid it is, or ``None``. Also…, Hand the renderer the depth grid, or take it away, before a frame.

### Community 160 - "write"
Cohesion: 0.36
Nodes (8): _push_slider(), OBJ parsing: normals, triangulation and index handling., test_empty_file_is_rejected(), test_missing_normals_are_computed(), test_negative_indices_are_relative(), test_quad_is_triangulated(), test_recentering_moves_bounds_onto_the_origin(), write()

### Community 161 - "Buried"
Cohesion: 0.29
Nodes (6): BoneLabels, Buried, Enum, str, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…

### Community 162 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 163 - "FormRun"
Cohesion: 0.40
Nodes (3): FormRun, Begin a run against a form already in the store., A guided form part-way through.

### Community 164 - "Human Skin renderer"
Cohesion: 0.33
Nodes (5): Human Skin renderer, Material and transport, Scheduling, precision and compatibility, Surface, Where to change it

### Community 165 - "orientation.py"
Cohesion: 0.29
Nodes (5): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis

### Community 166 - "lumpy"
Cohesion: 0.25
Nodes (8): lumpy(), A form with real planes in it, and more than one facing the same way., The coefficients have to reach the fit, and reaching it has to show. Two planes…, The fit and the shader have to agree, or the boundaries drawn are not the…, Narrow it and only the flattest surface has a say; widen it and the rounded…, test_a_coefficient_of_zero_takes_the_term_out_of_the_shader_too(), test_leaning_on_position_breaks_a_form_up_as_well_as_down(), test_the_flat_span_says_how_much_of_the_form_counts_as_flat()

### Community 167 - "ball"
Cohesion: 0.06
Nodes (46): coarse_lattice(), film_of(), fixture, MonkeyPatch, parametrize, Scrubbing through the making of a form, rather than only arriving at it. The…, A cut takes material away, so no stage of a carving is larger than the one…, The same the other way about: a lump adds material, so the form grows. (+38 more)

### Community 168 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 169 - "sample_count"
Cohesion: 0.50
Nodes (3): How many samples the framebuffer bound right now is drawing with. One where…, sample_count(), How many samples this view is really drawing with, or ``None``. Asked of GL…

### Community 170 - "_height_of"
Cohesion: 0.40
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 171 - "_file_drag"
Cohesion: 0.40
Nodes (5): _file_drag(), A file being dragged over the middle of the view, as ``kind`` of event., Entering, moving and dropping: a drop lands only where the move before it was…, test_a_file_the_window_cannot_open_is_refused_on_the_way_past(), test_a_model_file_is_welcome_at_every_step_of_its_drag()

### Community 172 - "simplified"
Cohesion: 0.38
Nodes (7): detail_joints(), Which joints are detail, and which kind, read off their names. A toe past the…, The joint list with the detail taken out, and how much of each kind went. What…, simplified(), _game_rig(), test_a_role_keeps_a_joint_and_its_ancestors_through_a_simplify(), test_simplifying_takes_the_detail_out_by_name_and_keeps_the_figure()

### Community 173 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 175 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 176 - "raycast_mesh"
Cohesion: 0.08
Nodes (41): _cross(), Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Row-wise cross product, without :func:`numpy.cross`'s axis shuffling., Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface. (+33 more)

### Community 177 - "test_the_switch_on_a_dock_bar_is_the_panels_own_visibility"
Cohesion: 0.67
Nodes (3): parametrize, test_a_panel_that_draws_nothing_has_no_switch(), test_the_switch_on_a_dock_bar_is_the_panels_own_visibility()

### Community 178 - "trusted_roots"
Cohesion: 0.29
Nodes (7): _macos_root_certificates(), The system root certificates as PEM text, or ``""`` if they cannot be read., A TLS context that can actually verify GitHub's certificate. Python's own…, trusted_roots(), SSLContext, Whatever the interpreter was built with, the context has roots in it., test_the_release_check_trusts_a_certificate_bundle()

### Community 179 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 186 - "ModelPanel"
Cohesion: 0.13
Nodes (4): ModelPanel, Reflect the tool state without re-emitting the toggle., Choose the gesture, from the menu or a key., Lists the objects, places the active one, and reports what came out of its file.

### Community 187 - "ui/preferences.py"
Cohesion: 0.11
Nodes (18): current(), forget(), PreferenceStore, QObject, QSettings, _qcolor(), Where the preferences are kept, and what happens when one changes.…, Push the preferences that something in the process holds a copy of.… (+10 more)

### Community 188 - "._commit_node_drag"
Cohesion: 0.33
Nodes (3): Record the finished gesture: a move, a resize, or a plain click. A press that…, Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…

### Community 190 - "._dress_soon"
Cohesion: 0.29
Nodes (3): Dress the tabs once Qt has finished rearranging them., Bring the first panel to the front of the tab strip., Put every dock back where it started, now. Not "forget the saved layout and…

### Community 191 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 192 - "test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else"
Cohesion: 0.33
Nodes (5): lattice_fineness(), How much finer than usual a detail setting asks the lattice to be. One at the…, How much finer than usual the geometry's lattice is worked on., The slider's own end already asks for every plane a fit will give, so what a…, test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else()

### Community 193 - "coarse_lattice"
Cohesion: 0.33
Nodes (6): app(), coarse_lattice(), fixture, MonkeyPatch, One Qt application for the whole run; offscreen, so CI needs no display.…, Read every model on a small lattice, so the suite stays quick.

### Community 194 - "block"
Cohesion: 0.33
Nodes (6): block(), A closed box with hard edges, each face cut into a grid of triangles., Counting crossings is exact on a closed surface and meaningless on anything…, A box is six triangles the size of the whole thing; the lattice has to feel it…, test_an_open_model_is_read_some_other_way(), test_the_samples_cover_a_surface_however_it_was_tessellated()

### Community 195 - "._menu_action"
Cohesion: 0.40
Nodes (4): _plain(), QAction, A menu entry's text as a name: no accelerator ampersand, no trailing dots., Add a menu entry, optionally with a window-wide shortcut. Given a ``command``…

### Community 196 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 201 - "box"
Cohesion: 0.50
Nodes (4): box(), A unit cube, shaded flat: six planes and twelve right angles., Every edge of a cube is a right angle, and no reading of AutoSmooth short of…, test_autosmooth_leaves_a_real_plane_change_hard()

### Community 203 - "welded"
Cohesion: 0.67
Nodes (3): ndarray, Which point each vertex really is, once copies of a position are one point., welded()

## Knowledge Gaps
- **5 isolated node(s):** `refview`, `Surface`, `Material and transport`, `Scheduling, precision and compatibility`, `Where to change it`
  These have ≤1 connection - possible missing edges or undocumented components.
- **25 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `ExportLook`, `settings.py`, `SceneObject`, `viewport.py`, `SceneRenderer`, `MeshBuffers`, `SkeletonStore`, `SectionSettings`, `plane_volume.py`, `TriangleIndex`, `PlaneSettings`, `test_plane_clusters.py`, `lumpy`, `ball`, `forms.py`, `Camera`, `gltf_loader.py`, `ExportVideoDialog`, `raycast_mesh`, `test_skeleton.py`, `mesh_renderer.py`, `block`, `PrimaryForm`, `test_objects.py`, `test_plane_solids.py`, `box`, `welded`, `ViewerState`, `_wires`, `Bounds`, `._commit_objects`, `build_form`, `core/__init__.py`, `OrientationSettings`, `skin_refinement.py`, `.add_mesh`, `Skeleton`, `GridSettings`, `Joint`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `test_preferences.py`, `Viewport`, `SceneObject`, `MainWindow`, `viewport.py`, `main_window.py`, `Armature`, `.apply_session`, `CameraPanel`, `panel`, `test_matcap_preview.py`, `MeasureTool`, `PrimaryForm`, `test_objects.py`, `ObjectTool`, `session.py`, `SurfacePicker`, `load_matcap_pixels`, `test_custom_panels.py`, `._commit_objects`, `test_forms_panel.py`, `SectionGizmo`, `MatcapPanel`, `test_elements.py`, `core/__init__.py`, `Measurement`, `OrientationSettings`, `skin_refinement.py`, `.add_mesh`, `Skeleton`, `ViewportOverlay`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `._sync_scene`, `.stage_images`, `AnnotateTool`, `ExportLook`, `test_preferences.py`, `MainWindow`, `viewport.py`, `main_window.py`, `._picker`, `.paintGL`, `PlaneSettings`, `film_export.py`, `sample_count`, `ExportVideoDialog`, `._active_changed`, `FilmExport`, `._commit_node_drag`, `MeasureTool`, `PrimaryForm`, `test_objects.py`, `._place_joint`, `ObjectTool`, `._place_form_landmark`, `SurfacePicker`, `ViewerState`, `NavigationController`, `SectionGizmo`, `build_form`, `_Encoder`, `Measurement`, `.mouseReleaseEvent`, `._place_armature_node`, `AddItem`, `ViewportOverlay`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Are the 44 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 44 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `OverlayParts`) actually correct?**
  _`ViewerState` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._