# Graph Report - reference-viewer  (2026-09-23)

## Corpus Check
- 172 files · ~534,542 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 6010 nodes · 14078 edges · 236 communities (219 shown, 17 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 736 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8c592da8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- form_group
- test_preferences.py
- Release
- Viewport
- SceneObject
- Bounds
- MainWindow
- viewport.py
- GifWriter
- linalg.py
- SceneRenderer
- elements/__init__.py
- state.py
- MeshBuffers
- Armature
- environment.yml
- ViewerState
- Skeleton
- _Target
- CameraPanel
- PosePanel
- ShaderProgram
- PoseTool
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- Writer
- SectionSettings
- plane_volume.py
- ControlsWindow
- auto_skin
- ShadingPanel
- PlaneSet
- test_camera.py
- test_plane_clusters.py
- WakeLock
- test_forms.py
- ._built
- CustomPanel
- VideoFormat
- convex.py
- Camera
- autoskin.py
- ValueSlider
- gltf_loader.py
- ExportVideoDialog
- film_export.py
- landmarks.py
- Agent Graph-First Instructions
- body_regions.py
- plane_clusters.py
- test_matcap_preview.py
- test_armature.py
- ArmaturePanel
- SkinSettings
- HotkeyMap
- FilmExport
- FormsPanel
- PlanesPanel
- test_skeleton.py
- Progress
- Workspace
- ui/hotkeys.py
- build_ribcage
- application.py
- MeasureTool
- Link
- FormTool
- ShadingMode
- test_objects.py
- test_skin.py
- test_plane_solids.py
- ObjectTool
- save_mesh
- ArmatureTool
- mesh_renderer.py
- load_matcap_pixels
- test_custom_panels.py
- SkinEdit
- core/preferences.py
- core/environment.py
- NavigationController
- pose_panel.py
- ._commit_objects
- test_forms_panel.py
- PlaneSettings
- QPointF
- PrimaryForm
- MatcapPanel
- AnnotatePanel
- Frame
- Panel
- ._turned
- test_elements.py
- Mesh
- load_stl
- ReflowLayout
- OrientationSettings
- ColorButton
- plane_axes
- clone.py
- skin_detail.py
- Path
- Rig
- .mouseReleaseEvent
- test_panel_docks.py
- MarkerVisibility
- ._place_armature_node
- test_tasks.py
- armature_tool.py
- DockTitle
- test_reflow.py
- .source_mesh
- Task
- .matrix
- ._build_objects
- test_open_files.py
- LightingMode
- Session
- AddItem
- ViewportOverlay
- test_hotkeys.py
- core/__init__.py
- .__init__
- _tab_switch
- Reflow
- forms.py
- SectionPanel
- ._upload_sculpt
- ._sync_scene
- .stage_images
- SurfacePicker
- ExportLook
- compute_vertex_normals
- app
- symbol_button
- shading_panel.py
- ._start_update_check
- load_mesh
- _wires
- _drag_over
- spatial.py
- palette.py
- MatcapPreview
- ._picker
- ._carrying_a_copy
- SliderSpin
- app
- GridSettings
- test_viewport_markers.py
- test_body_regions.py
- ContourShadingSettings
- DataTexture
- SkeletonStore
- restored
- .refresh
- test_spatial.py
- test_the_switch_is_not_squeezed_to_nothing
- render/environment.py
- .paintGL
- lumpy
- ProgressCard
- .column_of
- RegionSource
- Human Skin renderer
- SectionGizmo
- test_skin_gl.py
- coarse_lattice
- .refresh_list
- sample_count
- _height_of
- TriangleIndex
- SculptCache
- README.md
- ._active_changed
- watch_keys
- raycast_mesh
- Coefficients
- Preferences
- app
- ._commit_node_drag
- VideoSettings
- ._draw_hud
- HotkeyBinder
- .selected_objects
- test_the_dock_of_a_panel_taken_away_is_used_again
- ModelPanel
- PreferenceStore
- MeasurementSettings
- _NameOnlyDelegate
- ball
- release.yml
- quad
- KeyBox
- .__init__
- ._build_menus
- plane_axes.py
- section.py
- ask_for
- ._place_joint
- ._place_form_landmark
- TaskRunner
- matcap_panel.py
- decode
- CHANGELOG.md
- _Encoder
- _file_drag
- Hit
- .skin_object
- CancelledError
- tasks.py
- ndarray
- trusted_roots
- OverlayParts
- UpdateChecker
- .plane_span_deg
- step
- fixture
- Projection
- LightSettings
- HotkeyDialog
- _Worker
- test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else
- decorate
- .cancel
- .with_landmark_at
- ._scene_center
- test_the_switch_on_a_dock_bar_is_the_panels_own_visibility
- no_ffmpeg
- test_a_session_saved_without_panels_leaves_the_ones_open_alone
- test_resetting_the_layout_puts_the_docks_back_at_once
- test_resetting_keeps_the_panels_built_by_hand
- test_a_panel_does_not_cover_its_own_title
- test_a_panel_can_be_taken_away_and_another_built_after_a_restore
- test_loading_a_session_over_a_restored_layout_survives
- test_a_reused_dock_does_not_bring_the_old_panels_contents_with_it

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 243 edges
2. `ViewerState` - 184 edges
3. `Viewport` - 161 edges
4. `Skeleton` - 114 edges
5. `Camera` - 101 edges
6. `MainWindow` - 99 edges
7. `SceneObject` - 83 edges
8. `Armature` - 81 edges
9. `PrimaryForm` - 79 edges
10. `SceneRenderer` - 70 edges

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

## Communities (236 total, 17 thin omitted)

### Community 0 - "form_group"
Cohesion: 0.11
Nodes (17): QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row(), The preferences as they stand. Treat as read-only; use :meth:`set`., QWidget, Fill in the groups. A switch with nothing to put in the caption column is given…, Every command with its keys, each key a box that takes one keystroke. The list… (+9 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.10
Nodes (20): What the artist prefers: kept apart from the document, and acted upon. Two…, An external drive that is not plugged in is not an empty gallery., Zoom is geometric, so twice the speed is twice the exponent., Restore Defaults, or a copy of one of these controls in another panel., Windows that clean up after themselves, and a settings file that does., A session is not the only thing worth carrying on from., Otherwise the marks from one piece of work arrive on top of another., test_a_matcap_folder_that_has_gone_falls_back_to_the_bundled_ones() (+12 more)

### Community 2 - "Release"
Cohesion: 0.09
Nodes (35): QRunnable, check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and… (+27 more)

### Community 3 - "Viewport"
Cohesion: 0.05
Nodes (18): QOpenGLWidget, Arm one tool, disarming the rest. Only one gesture can own the left button, so…, Drop whatever gesture is half-finished, without disarming the tool., One of the renderer's :data:`~refview.render.mesh_renderer.ANTIALIASING_MODES`., Renders the scene and turns mouse gestures into camera and tool actions., Slide the view so a point sits at the centre, keeping the angle., The gesture a key press chooses, if the transform tool is armed to hear it., A form changed: work its clay out again and redraw. (+10 more)

### Community 4 - "SceneObject"
Cohesion: 0.06
Nodes (19): ObjectStore, ndarray, Snapshot, An angle in (-180, 180], with the floating-point dust brushed off., One model in the scene. Three meshes are kept, as the viewer kept them when…, The centred mesh carried by ``matrix`` -- the mesh itself for the identity., Drop the derived meshes, after the rest mesh has been replaced., The objects of the scene, in the order the panel lists their roots. Exactly one… (+11 more)

### Community 5 - "Bounds"
Cohesion: 0.13
Nodes (16): Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray, A turntable-style disc the model can stand on. A ground plane gives the eye… (+8 more)

### Community 6 - "MainWindow"
Cohesion: 0.07
Nodes (13): MainWindow, QMainWindow, Put every panel button and menu entry where the tools now stand. Only one tool…, Swap between the eraser and the drawing mode it was called from., Open an empty panel of the artist's own and bring it to the front., Put the panels back where they started, now., Follow the machine's sleep to whether this window is in front., Keep the banner over the view as the docks push the view about. (+5 more)

### Community 7 - "viewport.py"
Cohesion: 0.04
Nodes (51): AnnotateMode, AnnotationStore, Enum, ndarray, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An empty stroke carrying the current brush. (+43 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "linalg.py"
Cohesion: 0.08
Nodes (43): Quat, Interactive camera model driving both perspective and orthographic views., compose(), euler_to_quat(), look_at(), matrix_to_quat(), normalize(), orthographic() (+35 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.06
Nodes (39): Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, light_rig(), LightRig, Which lights are on this frame and where they point. Directions point from the…, Settle the lights for one frame., light_directions() (+31 more)

### Community 11 - "elements/__init__.py"
Cohesion: 0.08
Nodes (37): clone(), A working copy of ``source``, or ``None`` if its kind cannot be copied., A panel the artist builds, out of copies of controls from the fixed ones. The…, A titled frame that folds away behind its own bar. Every group of controls in…, Whether a group that goes dead folds away or merely greys out. Turning it back…, set_fold_disabled(), The widgets the panels are built out of, and the rules they follow. Four ideas,…, _asked() (+29 more)

### Community 12 - "state.py"
Cohesion: 0.04
Nodes (67): Named camera positions the artist can jump between while sculpting., The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, concatenated(), _corner_groups(), _face_cross(), _gathered(), _group_normals() (+59 more)

### Community 13 - "MeshBuffers"
Cohesion: 0.07
Nodes (14): _ghost_depth_range(), MeshBuffers, Vertex/index buffers for one mesh, bound through a single VAO., Where the form starts along the view, and how deep it is. The ghost weighs a…, Forget the contents without releasing the buffer objects., Replace the model: the whole scene as one mesh, and the objects it is made of.…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it. (+6 more)

### Community 14 - "Armature"
Cohesion: 0.05
Nodes (48): Armature, ArmatureNode, Bone, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves., A plausible thickness for a node placed by hand. (+40 more)

### Community 15 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 16 - "ViewerState"
Cohesion: 0.08
Nodes (23): QObject, A parenting policy changed: what is shown and how solid may have too., Turn every object the same way; see :meth:`set_object_orientation`. For files…, Turn one object, bringing the marks made on it along. Measurements,…, Take the display unit from the file when the format declares one. Only glTF…, Set the active matcap, or fall back to the built-in one., Have the HDRI at ``path`` read off the thread, and light with it when it lands.…, Light with a map already read -- or with none. (+15 more)

### Community 17 - "Skeleton"
Cohesion: 0.06
Nodes (30): Joint, _matrix16(), _pose_matrices(), ndarray, Whether the pose differs from the rest at all., A copy with the rest translation replaced and the frame kept., A tree -- or a forest -- of joints and the pose they stand in., Every joint, parents before children. A file may list a child before its… (+22 more)

### Community 18 - "_Target"
Cohesion: 0.07
Nodes (15): AccumTarget, ColorTarget, DepthTarget, GeometryTarget, A depth-only framebuffer, sampled afterwards as a texture., ``clamp_to_lit`` makes everything outside the map read as unshadowed., A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the… (+7 more)

### Community 19 - "CameraPanel"
Cohesion: 0.10
Nodes (9): CameraPanel, QListWidgetItem, Take the planes in hand where the fit left them, or hand them back., Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions. (+1 more)

### Community 20 - "PosePanel"
Cohesion: 0.05
Nodes (23): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, PosePanel, QTreeWidgetItem, The skeleton the panel is about: the selected row's, else the last., Highlight a row, in the tree and in the view., Highlight the row for a joint picked in the view., Run a row's edit once Qt has finished delivering the current signal. (+15 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.14
Nodes (7): ndarray, RuntimeError, Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "PoseTool"
Cohesion: 0.12
Nodes (30): PoseTool, Turns pulls on joints into pose edits, and clicks into new joints., app(), _arm(), _event(), _front_camera(), fixture, The pose tool, its gestures in the viewport, and the panel that lists the… (+22 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.07
Nodes (25): app(), _names(), panel(), fixture, The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as… (+17 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.10
Nodes (12): MeasurePanel, _NameOnlyDelegate, QStyledItemDelegate, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing… (+4 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.11
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around. (+1 more)

### Community 26 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 27 - "SectionSettings"
Cohesion: 0.11
Nodes (22): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, Unit axis, or ``None`` for a custom direction., A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn. (+14 more)

### Community 28 - "plane_volume.py"
Cohesion: 0.04
Nodes (113): _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field(), block_labels(), block_splits() (+105 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "auto_skin"
Cohesion: 0.15
Nodes (32): auto_skin(), bone_segments(), Skin ``mesh`` to ``skeleton``, both given in the same coordinates. The skeleton…, ``names`` with any repeat numbered, since the skin matches joints by name., Every bone as ``(start, end)`` points, and which joint each belongs to. A joint…, unique_names(), AutoSkinSettings, What the artist sets before auto-skinning, and rarely needs to. (+24 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.09
Nodes (14): Chooses the shading model and edits its light and surface parameters., Where on the body the marks fall, and how much of each in each region., Slot that writes one field of the light settings., Pick an HDRI from disk and light with it., List the bundled HDRIs, and the one in use if it is from elsewhere., Put the light's numbers back in line with the settings, after a drag or an undo., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings. (+6 more)

### Community 32 - "PlaneSet"
Cohesion: 0.08
Nodes (20): QThread, PlaneSet, One level of a fit: the planes the shader is to quantise against. A plane is a…, Film, The stage at ``index``, clamped to what has actually been recorded., A whole making, from the coarsest stage to the one the slider asks for. Held by…, FilmRecorder, QObject (+12 more)

### Community 33 - "test_camera.py"
Cohesion: 0.10
Nodes (11): _distance_or_none(), A clipping distance as a file wrote it, or ``None`` for one left to the fit., camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_clip_planes_set_by_hand_override_the_fit_within_reason() (+3 more)

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.11
Nodes (33): The joint list with ``index`` resting at ``target`` and its children left be., cube(), parametrize, Fitting planes to a model's surface rather than only to its normals. What…, How far the least well served of ``wanted`` is from anything offered., The one form whose planes are not a matter of opinion., The reason for reading where the surface is and not only which way. Both faces…, Merging back from patches is a hierarchy, so the cuts of it nest. This is what… (+25 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (32): c_void_p, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., Holds sleep off while the window that owns it is the one in front. The class… (+24 more)

### Community 36 - "test_forms.py"
Cohesion: 0.07
Nodes (36): merged(), The hull of the points with its faces bowed out; see :func:`rounded_hull`., Several flat meshes as one, or ``None`` when there is nothing to draw., _closed(), _inside(), _marks(), ndarray, The forms: convex solids, the landmarks that build them, the walk, and the… (+28 more)

### Community 37 - "._built"
Cohesion: 0.13
Nodes (8): QMenu, Path, QImage, QRect, Offer the picture back as a file: as graded here, or as it came. A grading…, The matcap as a picture, at its own resolution. Square and opaque, with the…, Where the sphere goes: square, centred, above the legend., The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…

### Community 38 - "CustomPanel"
Cohesion: 0.08
Nodes (21): carried(), Read a drag's payload back, or ``None`` if it is not one of ours., CustomPanel, _detach(), QFormLayout, QWidget, Take a copy out of this panel and destroy it., Move a copy already in a panel to a new place in this one. ``frame`` and… (+13 more)

### Community 39 - "VideoFormat"
Cohesion: 0.09
Nodes (13): Enum, str, Quality, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31., WebP's quality, 0 to 100. (+5 more)

### Community 40 - "convex.py"
Cohesion: 0.12
Nodes (24): convex_hull(), DegenerateHullError, flat_mesh(), _outward(), _patch_samples(), ndarray, ValueError, Convex solids from points: the hull, a cut through it, and its mesh. A primary… (+16 more)

### Community 41 - "Camera"
Cohesion: 0.07
Nodes (21): Camera, ndarray, Near/far planes fitted to the scene bounding sphere., The near and far planes this frame: the fitted ones, unless set by hand. A…, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Rays through a batch of pixels, as ``(origins, unit directions)``, ``(N, 3)``…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Project ``(N, 3)`` world points to ``(xs, ys, ndc_depths)`` in widget pixels. (+13 more)

### Community 42 - "autoskin.py"
Cohesion: 0.10
Nodes (27): _baked_rest(), _conjugate_gradients(), _CotLaplacian, _envelope_weights(), _Graph, _heat_weights(), _joint_distances(), _nearest_weights() (+19 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (13): _clone_slider(), _pull_slider(), _push_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end. (+5 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.10
Nodes (36): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), _first_skin(), GltfLoadError, load_gltf(), _local_transform() (+28 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.10
Nodes (11): ExportVideoDialog, Path, QDialog, QWidget, Where an artist says how the film should be written out. Everything on the…, What the frames are to look like, as the controls have it., How long it runs and what it is written as., Fill the width and height boxes from whichever preset is chosen. A preset with… (+3 more)

### Community 46 - "film_export.py"
Cohesion: 0.09
Nodes (29): _encode_arguments(), _encoders(), ffmpeg_path(), _FFmpegWriter, _no_window(), open_writer(), Path, RuntimeError (+21 more)

### Community 47 - "landmarks.py"
Cohesion: 0.08
Nodes (33): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _humanoid_landmarks(), _kept_laying(), _mid() (+25 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "body_regions.py"
Cohesion: 0.10
Nodes (26): band_weights(), BodyMap, BodySource, bone_weights(), build_body_map(), looks_like_a_figure(), ndarray, Where on the body a point of the skin is, so that the skin can be marked as… (+18 more)

### Community 50 - "plane_clusters.py"
Cohesion: 0.07
Nodes (37): PlaneAxes, The planes a model falls into, at every count. Built once per mesh and per…, _compact(), _consensus(), _cut(), _first_planes(), _fit(), flatness() (+29 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.09
Nodes (36): QPoint, _drag(), _listed(), _matcap_file(), parametrize, The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc. (+28 more)

### Community 52 - "test_armature.py"
Cohesion: 0.07
Nodes (56): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _chain(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other., The femoral head is in from the ASIS, below it and behind it, by shares of the… (+48 more)

### Community 53 - "ArmaturePanel"
Cohesion: 0.04
Nodes (31): ArmaturePanel, QTreeWidgetItem, Run a row's edit once Qt has finished delivering the current signal. Committing…, Arms the armature tool, lists its nodes and runs the guided presets., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Add an empty armature and select it., Begin a preset run against a fresh armature. (+23 more)

### Community 54 - "SkinSettings"
Cohesion: 0.11
Nodes (16): BodyRegionSettings, _default_profiles(), How much of each kind of mark one region gets, as multipliers of the sliders., Where skin marks tend to fall on a body, as a starting point., Where the regions come from, and what each does to the marks., One region's multiplier for ``effect`` after another, in :data:`REGIONS` order., RegionProfile, Material parameters shared by the analytic shading modes. (+8 more)

### Community 55 - "HotkeyMap"
Cohesion: 0.07
Nodes (19): Command, HotkeyMap, Any, Which keys do what, as the artist has decided rather than as it ships. A hotkey…, Whether the artist has moved this command off what it ships with., Which command has these keys, if any., Every command with keys on it, declared or not, as id -> keys., Put ``keys`` on a command, taking them off whatever had them. Returns the id of… (+11 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (12): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+4 more)

### Community 57 - "FormsPanel"
Cohesion: 0.04
Nodes (32): FormsPanel, QTreeWidgetItem, Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Begin a run against a fresh form: a preset's walk, or a freeform's., Take up the selected freeform again, so more landmarks can go on it. The same…, The freeform the highlighted row belongs to, when no run is on. (+24 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.08
Nodes (20): PlanesPanel, QListWidgetItem, Lay one length of wire earlier or later, as one undoable step., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Show what this way of working needs, and put the rest away. A setting that does… (+12 more)

### Community 59 - "test_skeleton.py"
Cohesion: 0.10
Nodes (33): looks_humanoid(), Whether a guessed mapping is enough of a figure to be worth offering., The model as ``skeleton`` poses it, or ``rest`` itself when it cannot. Linear…, skinned_mesh(), _arm(), ndarray, parametrize, Skeletons: the joint tree, posing, skinning, and where skeletons come from. (+25 more)

### Community 60 - "Progress"
Cohesion: 0.10
Nodes (16): Progress, What a long piece of work says about itself while it runs, and how it is…, Ask the work to stop at its next report., How far along, 0 to 1, or ``None`` when the work has not said., Whether the work has said how much there is to do., A window onto part of a parent's range; see :meth:`Progress.slice`., A progress nobody is watching, for work run without a window., How far a task has got, and whether it has been told to stop. ``on_change`` is… (+8 more)

### Community 61 - "Workspace"
Cohesion: 0.06
Nodes (29): QDockWidget, QTabBar, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top., _number_in(), QMainWindow, QObject, QSettings (+21 more)

### Community 62 - "ui/hotkeys.py"
Cohesion: 0.11
Nodes (22): assign(), describe(), forget(), group_of(), HotkeyStore, listed(), normalize(), QSettings (+14 more)

### Community 63 - "build_ribcage"
Cohesion: 0.12
Nodes (36): _across(), blend_rings(), build_head(), build_pelvis(), build_ribcage(), fit_plane(), _head_frame(), _HeadFrame (+28 more)

### Community 64 - "application.py"
Cohesion: 0.05
Nodes (39): ArgumentParser, Namespace, QSplashScreen, Application, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font() (+31 more)

### Community 65 - "MeasureTool"
Cohesion: 0.22
Nodes (4): MeasureTool, Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview.

### Community 66 - "Link"
Cohesion: 0.12
Nodes (9): CloneGesture, Link, _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original., Whether the copy is being used right now and must not be written. (+1 more)

### Community 67 - "FormTool"
Cohesion: 0.06
Nodes (30): FormLandmarkRef, FormSettings, How the forms are drawn, and how their landmarks are placed., FormRun, FormTool, ndarray, Begin a run against a form already in the store., The landmarks still to place, in order, the current one first. (+22 more)

### Community 68 - "ShadingMode"
Cohesion: 0.15
Nodes (6): Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode, even(), ``value`` rounded down to a multiple of four. Two would do for H.264, which…, TestEven

### Community 69 - "test_objects.py"
Cohesion: 0.11
Nodes (34): Path, Where an object stands relative to its parent: an affine placement. Held as the…, Transform, app(), _key(), _mouse(), _overridden(), fixture (+26 more)

### Community 70 - "test_skin.py"
Cohesion: 0.11
Nodes (24): _area(), build_bvh(), build_scene(), ndarray, Bounding-volume hierarchy tables for the OpenGL 3.3 skin tracer. The tree is…, Build on a worker from the immutable meshes currently drawn by the renderer., How wide the tables are laid out under a driver's texture limit: a power of two., Pack a linear texel array within the driver's actual 2D texture limit. Always… (+16 more)

### Community 71 - "test_plane_solids.py"
Cohesion: 0.04
Nodes (81): A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), block(), box(), dumbbell(), flatness(), ndarray, parametrize (+73 more)

### Community 72 - "ObjectTool"
Cohesion: 0.12
Nodes (14): _axis_param(), Gizmo, _Grip, ObjectTool, ndarray, The three directions the arms run along, in world space. A move and a turn are…, Where the gizmo for an object at ``world`` falls on screen, or ``None`` if…, Which handle a screen point is over: ``"centre"``, ``"x"``, ``"y"``, ``"z"`` or… (+6 more)

### Community 73 - "save_mesh"
Cohesion: 0.14
Nodes (8): Path, Write a mesh out; only OBJ is written, whatever the suffix asked for., save_mesh(), Write ``obj``'s turn and scale into its mesh, leaving it standing as it is.…, Write the document, and whatever the window says its layout is. The layout…, Write every skin made here beside the session; see :mod:`rig_file`., A file for ``obj`` next to the session, named for both., An object's rest mesh as a file stores it, so that reading it back comes to…

### Community 74 - "ArmatureTool"
Cohesion: 0.04
Nodes (60): LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), ArmatureTool, Handle, The landmarks still to place, in order, the current one first. (+52 more)

### Community 75 - "mesh_renderer.py"
Cohesion: 0.08
Nodes (23): bind_default(), current_framebuffer(), FrameTarget, Offscreen render targets used by the high-quality, ghost and smoothing passes.…, The framebuffer object bound right now -- Qt's, in a widget., Restore a framebuffer captured with :func:`current_framebuffer`., The whole frame, drawn offscreen so it can be smoothed on the way out. A colour…, OpenGL rendering layer: shader programs, textures and the scene renderer. (+15 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.16
Nodes (22): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+14 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.07
Nodes (23): QMimeData, app(), custom(), _drop_on(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error., A group is not a row, so it goes ahead of the group it was dropped on. (+15 more)

### Community 78 - "SkinEdit"
Cohesion: 0.09
Nodes (10): BakeEdit, Command, Dressing an object in a skin made for a skeleton, or taking it off. One step…, Writing an object's turn and scale into its mesh -- Reset XForm -- or undoing…, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Take a skin made here off ``obj``; the skeleton keeps its joints., Put ``rig`` on the object's file mesh, or take the one it wears off. (+2 more)

### Community 79 - "core/preferences.py"
Cohesion: 0.11
Nodes (20): _as_kind_of(), _clamp(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any (+12 more)

### Community 80 - "core/environment.py"
Cohesion: 0.07
Nodes (61): direction_to_uv(), dominant_light(), downsized(), EnvironmentLoadError, evaluate_sh(), _exr_rgb(), _halve(), irradiance_sh() (+53 more)

### Community 81 - "NavigationController"
Cohesion: 0.08
Nodes (25): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Degrees of yaw per pixel, signed by whether the drag is inverted. (+17 more)

### Community 82 - "pose_panel.py"
Cohesion: 0.08
Nodes (34): What to call the joint filling a humanoid slot: ``"knee.L"`` is ``"Knee L"``., role_name(), build_humanoid_skeleton(), detail_joints(), humanoid_positions(), humanoid_roles(), ndarray, Where skeletons come from: an armature, a preset, or the names in a file. Three… (+26 more)

### Community 83 - "._commit_objects"
Cohesion: 0.07
Nodes (20): ObjectsEdit, Snapshot, A copy of ``obj``'s mesh on top of it, made active, as one undo step., Scale ``objects`` so each is the size of the active one, as one undo step. The…, The largest of ``obj``'s three extents as it stands in the world., Re-read how solid each part is drawn, without touching the geometry., An edit to the objects -- a move, a parenting, a removal -- as two snapshots.…, Where everything stands now; the start of a gesture keeps one. (+12 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.12
Nodes (29): app(), _click(), panel(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The… (+21 more)

### Community 85 - "PlaneSettings"
Cohesion: 0.03
Nodes (98): auto_smooth(), A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, plane_regions(), Break the surface into patches and merge them back into planes., film_key(), planes_for(), The stages a form passes through on its way from a block to a figure. The…, What a film depends on. Everything that changes the shape of any stage, and… (+90 more)

### Community 86 - "QPointF"
Cohesion: 0.17
Nodes (13): QPointF, draw_rail(), draw_text(), One marker object for endpoints, nodes, landmarks and tool previews., Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, The screen-space cue for one degree of freedom. A vertical rail that fades out…, VisualMarker, project_visible_many() (+5 more)

### Community 87 - "PrimaryForm"
Cohesion: 0.06
Nodes (46): PlacedLandmark, One anatomical point the artist put on the model during a guided run., One convex piece of a form: its hull vertices and outward-wound faces., The longest side of the box the solid sits in., Whether a point lies inside, or within ``slack`` of the surface., Solid, build_form(), built_count() (+38 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.13
Nodes (11): MatcapPanel, Path, Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, Rebuild the thumbnail list: the built-in, the ones added, then the folder., Put the matcap on the model into the gallery, if it came from somewhere else.…, The disc was dragged: show the renderer and the numbers what it did., A different matcap: the disc draws whichever one is on the model. (+3 more)

### Community 89 - "AnnotatePanel"
Cohesion: 0.19
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 90 - "Frame"
Cohesion: 0.07
Nodes (18): _pull_frame(), _push_frame(), Nothing: each row inside the copy is linked on its own., Frame, FrameBar, framed(), QFormLayout, QPainter (+10 more)

### Community 91 - "Panel"
Cohesion: 0.08
Nodes (19): QScrollArea, Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Whether what this panel draws is on screen, or ``None`` if it draws nothing.…, Show or hide what this panel draws; see :meth:`shown`., Ignore widget signals for the duration of the block. (+11 more)

### Community 92 - "._turned"
Cohesion: 0.11
Nodes (13): Quat4, normalized_rotation(), A pose rotation as the plain tuple a joint stores., ndarray, The turn the parent takes so that joint ``index`` points at ``target``. The…, The rotation joint ``index`` takes after rolling about its own bone., The pose shift that puts joint ``index`` at ``target``, children and all., Which way the bone at joint ``index`` runs, in the scene. Towards its first… (+5 more)

### Community 93 - "test_elements.py"
Cohesion: 0.06
Nodes (29): QApplication, Put the rule in place for every switch in the application., app(), fixture, Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can. (+21 more)

### Community 94 - "Mesh"
Cohesion: 0.08
Nodes (26): Mesh, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Return a copy carried by a full 4x4 -- a move, a turn and a scale together.…, Return a copy whose bounding-box centre sits at the origin., Which corners of a mesh share a normal under AutoSmooth, worked out once. What…, Whether ``mesh`` is laid out as the one the groups were read from., ``mesh`` -- the one the groups were read from, or it moved or posed -- shaded… (+18 more)

### Community 95 - "load_stl"
Cohesion: 0.21
Nodes (12): _ascii_corners(), _binary_corners(), load_stl(), ndarray, Path, Raised when a file cannot be interpreted as an STL mesh., Load ``path``, choosing the binary or ASCII reader by inspection., Facet corners from a binary STL, or ``None`` if this is not one. The declared… (+4 more)

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - "OrientationSettings"
Cohesion: 0.06
Nodes (32): Measurement, MeasurementStore, ndarray, Named point-to-point measurements and their presentation options., The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units. (+24 more)

### Community 98 - "ColorButton"
Cohesion: 0.07
Nodes (19): _clone_point(), _clone_swatch(), _pull_point(), _pull_swatch(), _push_point(), _push_swatch(), _AxisBox, ColorButton (+11 more)

### Community 99 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 100 - "clone.py"
Cohesion: 0.06
Nodes (58): QAbstractButton, QLineEdit, QSlider, QSpinBox, _begin(), can_clone(), _clone_button(), _clone_check() (+50 more)

### Community 101 - "skin_detail.py"
Cohesion: 0.17
Nodes (20): burley_marginal(), burley_profile(), cellular(), diffusion_lut(), _fade(), fbm(), ndarray, Procedural skin micro-relief and the pre-integrated diffusion table. Reference… (+12 more)

### Community 102 - "Path"
Cohesion: 0.12
Nodes (12): A flat-shaded mesh, every triangle with its own three corners. Corners are not…, Path, Pick up whatever was last being worked on, if that was asked for. A session…, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window. In the…, Read a model file off the window, then hand it to ``adopt`` here., Ask whether a rig that arrived with the model should be read as a figure. Only… (+4 more)

### Community 103 - "Rig"
Cohesion: 0.10
Nodes (20): AutoSkin, AutoSkinError, ValueError, Raised when there is nothing to skin, or nothing to skin it to., What :func:`auto_skin` hands back: the rig, and the joints to keep with it., load_rig(), Path, RuntimeError (+12 more)

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.09
Nodes (11): Record the finished drag as a single undo step., Record the turn as one undo step., Alt forces the camera gesture, whichever tool is armed., Record the finished drag as one step, or read a press as a selection., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Make the object under the cursor the active one., Record the finished pull as one step, or read a press as a selection. (+3 more)

### Community 105 - "test_panel_docks.py"
Cohesion: 0.14
Nodes (3): Each panel in a dock of its own, and putting the docks back next time. Two…, test_a_restored_copy_drives_the_new_windows_own_control(), test_the_layout_comes_back_through_the_settings()

### Community 106 - "MarkerVisibility"
Cohesion: 0.18
Nodes (5): MarkerVisibility, Cache surface occlusion by view and position for every kind of marker. The…, Whether the last pass is recent enough to be read instead of repeated., Mark these points as standing in front of the surface, untested. For frames…, Answer for a batch of points at once, ahead of being asked one by one. Every…

### Community 107 - "._place_armature_node"
Cohesion: 0.33
Nodes (3): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 108 - "test_tasks.py"
Cohesion: 0.17
Nodes (16): app(), fixture, Work run off the window, and the cards that show it running., Turn the event loop until ``until()`` says so, or give up., runner(), _spin(), test_a_result_arriving_after_the_cross_is_thrown_away(), test_a_task_called_off_while_waiting_never_starts() (+8 more)

### Community 109 - "armature_tool.py"
Cohesion: 0.12
Nodes (14): BoneRef, GuideRun, _project(), Placing and editing the nodes of an armature, freehand or led by a preset.…, Begin a preset run against an armature already in the store., The nearest bone under the cursor, for showing its length., A guided preset part-way through. The index walks the preset's own list rather…, A world point in widget pixels, or ``None`` when it is behind the camera. (+6 more)

### Community 110 - "DockTitle"
Cohesion: 0.09
Nodes (14): QToolButton, DockTitle, make_switch(), QCheckBox, QSize, QWidget, One dock per panel, with a bar of its own across the top. Every panel is its…, Put a show/hide switch at the left of the bar and return it. (+6 more)

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - ".source_mesh"
Cohesion: 0.25
Nodes (5): setter, The active object turned and centred but not posed or placed., The active object exactly as its file stored it., Set the active object's file mesh; its rest mesh is turned from it as at a load., The active object, made on the spot when a mesh is handed to an empty scene.

### Community 113 - "Task"
Cohesion: 0.14
Nodes (9): BaseException, T, Mark the task over. The runner does this; a begun task's driver does., Run ``work(progress)`` on a thread; ``done(result)`` back here. ``failed`` is…, A task driven by the caller, on the GUI thread, a step at a time. For work that…, The cards for the window's tasks, floated over the bottom of the viewport. Told…, One piece of work in flight, as the window sees it. Made by the runner, never…, Task (+1 more)

### Community 114 - ".matrix"
Cohesion: 0.50
Nodes (3): The 4x4 that carries the object's own coordinates into its parent's., _triple(), Vector

### Community 115 - "._build_objects"
Cohesion: 0.19
Nodes (6): _ObjectTree, QPushButton, QWidget, A tree whose rows can be dropped onto one another to hang one from another. Qt…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 116 - "test_open_files.py"
Cohesion: 0.18
Nodes (9): app(), opened(), fixture, Files arriving from outside: the command line, a drop, or the desktop's "Open…, One offscreen Qt application for the run; see test_film_recorder., What the window was asked to open, by kind, without loading anything., Finder sends the launching file as an event, which can land before the window., test_a_file_the_desktop_hands_over_early_waits_for_the_window() (+1 more)

### Community 117 - "LightingMode"
Cohesion: 0.14
Nodes (9): ContourDirection, LightingMode, PlaneTarget, Enum, str, The world axis, or ``None`` when it is the camera's or the artist's., What the lit shading modes are lit by. The studio rig is a key, a fill opposite…, What the planes filter is allowed to act on. The two are mutually exclusive… (+1 more)

### Community 118 - "Session"
Cohesion: 0.07
Nodes (35): ObjectRecord, What a session writes down about an object; the mesh itself stays in its file., Path, A snapshot of everything worth keeping between runs., Session file that sits beside a model, e.g. ``bust.refview.json``., Session, sidecar_path(), Path (+27 more)

### Community 119 - "AddItem"
Cohesion: 0.06
Nodes (27): Camera motion is deliberately not undoable, AddItem, Command, Append an item to a document list., Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems (+19 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.12
Nodes (18): project_visible(), Handle, QPainter, Convert a 0-1 RGB tuple to a QColor., Project a world point, returning ``None`` when it is behind the camera., Draws measurements, tool previews, the orientation gizmo and the readout., Whether the last frame drew from stale occlusion answers., Draw everything over the scene. ``occlude`` off skips asking the surface which… (+10 more)

### Community 121 - "test_hotkeys.py"
Cohesion: 0.11
Nodes (23): QKeySequence, app(), _map(), fixture, Hotkeys: the map, the store, the binder, and the gesture that assigns one., One offscreen Qt application for the run; see test_film_recorder., End to end: the filter is on the panel's buttons and the window hears it., A key given to something else comes off what had it, and the map says what that… (+15 more)

### Community 122 - "core/__init__.py"
Cohesion: 0.10
Nodes (13): ArmatureStore, BoneLabels, Buried, Enum, str, A graph of named points under the form, and the wire it stands for. An armature…, When the length of a bone is written beside it., An ordered, named collection of armatures, usually holding one. Deliberately… (+5 more)

### Community 124 - "_tab_switch"
Cohesion: 0.29
Nodes (7): The show/hide switch on the tab named ``title``, if it has one., Stacked behind another panel is where the switch is worth the most., It is fifteen pixels wide and carries no words, which is exactly the shape the…, _tab_switch(), test_a_panel_that_draws_nothing_gets_no_switch_on_its_tab(), test_a_tabbed_panel_still_shows_its_switch(), test_clicking_the_switch_on_a_tab_works()

### Community 125 - "Reflow"
Cohesion: 0.30
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 126 - "forms.py"
Cohesion: 0.06
Nodes (57): build_freeform(), _centre(), form_landmark_title(), form_spec(), FormFill, FormPreset, FormStage, freeform_landmark() (+49 more)

### Community 127 - "SectionPanel"
Cohesion: 0.18
Nodes (6): Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 128 - "._upload_sculpt"
Cohesion: 0.12
Nodes (7): The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, Cut the stand-in on a thread; see :meth:`_upload_sculpt`., Show the recording as a task, its bar the stages landed so far., The cross on the recording's card: the film is dropped, the switch too., A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on.

### Community 129 - "._sync_scene"
Cohesion: 0.11
Nodes (10): The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, A skeleton changed: redraw it, and let the skin's body map follow its bones., What the renderer draws: each object as it stands, AutoSmoothed if asked., ``mesh`` shaded by the object's smoothing groups, found once and kept. The…, The whole scene as one mesh, as the planes and the skin tracer read it. The…, Tell the renderer what the skin's body map is made from now., Hand the renderer a re-posed model and nothing else. For the frames of a pose…, Regenerate the pedestal and the cut contour when their settings move. Both are… (+2 more)

### Community 130 - ".stage_images"
Cohesion: 0.21
Nodes (7): QOpenGLFramebufferObject, QImage, One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A…, An offscreen target the frames are drawn into, made once per export.…, Draw the scene into ``surface`` and read it back as an image., Lay the overlay -- and the caption, if it was asked for -- on a frame. Painted…

### Community 131 - "SurfacePicker"
Cohesion: 0.08
Nodes (24): JointRef, AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+16 more)

### Community 132 - "ExportLook"
Cohesion: 0.09
Nodes (17): ExportLook, What the frames are to look like, as against what they are of. Laid over the…, Which of the things drawn over the model belong in the frames., ``base`` with this export's choices laid over it., The line burned into the corner of the frame for ``stage``. Counted off the…, app(), FakeViewport, fixture (+9 more)

### Community 133 - "compute_vertex_normals"
Cohesion: 0.10
Nodes (34): compute_vertex_normals(), Area-weighted smooth vertex normals for an indexed triangle soup., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic() (+26 more)

### Community 134 - "app"
Cohesion: 0.40
Nodes (5): app(), gallery_settings(), fixture, The gallery's list on a settings file of the tests' own, empty to begin with., One offscreen Qt application for the run; see test_film_recorder.

### Community 135 - "symbol_button"
Cohesion: 0.16
Nodes (13): QTreeWidget, _NameOnlyDelegate, QPushButton, QStyledItemDelegate, QWidget, Allows in-place editing of the name column only., Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list… (+5 more)

### Community 136 - "shading_panel.py"
Cohesion: 0.19
Nodes (18): available_environments(), available_matcaps(), _bundled_root(), environment_dir(), image_path(), matcap_dir(), model_dir(), Path (+10 more)

### Community 137 - "._start_update_check"
Cohesion: 0.31
Nodes (4): Ask GitHub for the newest release in the background. The startup check is…, QWidget, show_failure_dialog(), show_up_to_date_dialog()

### Community 138 - "load_mesh"
Cohesion: 0.24
Nodes (13): load_mesh(), Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one(), test_binary_stl_welds_shared_corners(), test_glb_applies_node_transforms_and_reports_metres() (+5 more)

### Community 139 - "_wires"
Cohesion: 0.12
Nodes (26): _bar(), _holds(), A long ellipsoid: one closed form with an obvious axis to lie along., Whether a fitted solid has a point inside it., An armature for the volume, with ``off`` naming the rows taking no clay., The claim the whole armature mode rests on. A lump that merely landed near its…, The wire says where the clay goes; the model still says how far. A lump started…, Which is what makes the order worth reordering, and what a film of a block-in… (+18 more)

### Community 140 - "_drag_over"
Cohesion: 0.22
Nodes (10): _drag_over(), _middle_of_the_view(), A drag of ``holder`` arriving at ``point`` in the window's coordinates. A real…, The gesture the whole thing rests on: drag it onto the model, it goes., A gesture that destroys something only fires where it clearly meant to., Refused at the door it would never reach the model; so it is let in., test_a_copy_dropped_on_the_model_is_thrown_away(), test_a_copy_is_let_into_the_window_wherever_it_arrives() (+2 more)

### Community 141 - "spatial.py"
Cohesion: 0.19
Nodes (11): _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Box the leaves up, coarsest level first and the leaves themselves last., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the…, Interleave each 10-bit value with two zero bits, ready to be shifted., Build the index from expanded triangle corners, shape ``(T, 3, 3)``., Triangle indices worth intersecting for this ray, possibly empty. (+3 more)

### Community 142 - "palette.py"
Cohesion: 0.11
Nodes (16): css(), outline(), QColor, The colours the hand-drawn elements paint with. Kept apart from…, Draw the hairline that separates a control from the panel. One line, the same…, A colour as a style sheet function, for the parts Qt draws., Change the one colour that is not grey, everywhere at once. The hand-painted…, set_accent() (+8 more)

### Community 143 - "MatcapPreview"
Cohesion: 0.06
Nodes (34): MatcapSettings, Post-processing applied to the sampled matcap texel., _angle(), _clone_preview(), grade(), MatcapPreview, _pull_preview(), _push_preview() (+26 more)

### Community 144 - "._picker"
Cohesion: 0.09
Nodes (12): Rub out the stroke points under the eraser, live., Turn the lights by how far the drag has come: across about the vertical, up in…, Take hold of a node, to move it, resize it, or just to select it. This works…, Apply the drag live, so the artist sees the wire bend as they pull it., Take hold of a landmark, to move it or just to say which one it is., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Where the active object's gizmo falls on screen, or ``None``. (+4 more)

### Community 145 - "._carrying_a_copy"
Cohesion: 0.11
Nodes (10): opens_as(), Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model., Take a copied control out of whichever hand-built panel holds it., Open a file by what it is: a model, a session, a matcap or an HDRI. The one…, What a file opens as, by its suffix: a model, a session, a matcap or an HDRI., Apply a matcap image, reporting unreadable files to the user. (+2 more)

### Community 146 - "SliderSpin"
Cohesion: 0.17
Nodes (11): QComboBox, _push_combo(), _NameOnlyDelegate, QStyledItemDelegate, QWidget, _row(), collapsible_group(), QFormLayout (+3 more)

### Community 147 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 148 - "GridSettings"
Cohesion: 0.14
Nodes (18): build_grid(), GridLines, GridSettings, nice_step(), Reference grids on the three axis planes, fading with distance. A grid gives…, Segments, with their colours and widths, ready for the stroke buffer., Every line of every enabled grid, or ``None`` when none is on., The nearest 1, 2 or 5 times a power of ten at or below ``value``. (+10 more)

### Community 149 - "test_viewport_markers.py"
Cohesion: 0.14
Nodes (20): app(), event(), fixture, parametrize, Marker interaction, selection identity, and section dragging regressions., A grid facing the camera, through the point wherever it has got to., _right(), test_contour_controls_follow_the_mode_and_pin_the_view() (+12 more)

### Community 150 - "test_body_regions.py"
Cohesion: 0.29
Nodes (12): _column(), _figure_bones(), ndarray, Where on the body the skin is: bones, height bands, the map, and the settings., A thin column standing from the ground to ``height``., _region(), test_height_bands_follow_the_canon_and_are_soft_at_the_edges(), test_points_go_to_the_region_of_the_nearest_bone_and_blend_between() (+4 more)

### Community 151 - "ContourShadingSettings"
Cohesion: 0.20
Nodes (8): ContourShadingSettings, Parallel slices drawn across the form, the way a contour map reads land. The…, The unit direction the slices are stacked along, in world space., parametrize, The contour shading mode: slices across the form, read off it like a map., test_a_custom_direction_is_normalised_and_an_empty_one_falls_back(), test_the_density_floor_keeps_the_spacing_finite(), test_the_slices_face_the_way_that_was_asked()

### Community 152 - "DataTexture"
Cohesion: 0.07
Nodes (16): EnvironmentMap, An HDRI read and made ready for the renderer. Built off the thread., What the radiance is multiplied by so that :attr:`peak` comes out at one. One…, EnvironmentTextures, The map, the sampling tables, and the uniforms that describe them., Put a map on the card, or take it off; cheap when it is the one already there., Point ``program`` at the map, scaled by ``scale_factor`` on top of the rig's…, Light with ``environment`` where the settings ask for an HDRI; ``None`` for… (+8 more)

### Community 153 - "SkeletonStore"
Cohesion: 0.18
Nodes (3): An ordered collection of skeletons, like the other document stores., The skeleton the model follows: the first one bound to its rig., SkeletonStore

### Community 154 - "restored"
Cohesion: 0.29
Nodes (7): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., A window with the saved layout out of the way, and put back after. Shown,…, A second window, built from a layout the first one saved. The point is…, restored(), window()

### Community 155 - ".refresh"
Cohesion: 0.18
Nodes (3): Bind the panel to the viewport's transform tool., Turn the active object, or note how the next file is read when there is none., Write the active object's placement into the boxes.

### Community 156 - "test_spatial.py"
Cohesion: 0.26
Nodes (11): _grid(), The picking accelerator: it must be fast without changing any answer., A bumpy height field, so rays hit different triangles at different depths., The pruned candidate set must never miss the true intersection., Every parent must enclose its children, or a ray could slip past a leaf., test_a_batch_of_rays_gets_the_same_candidates_as_one_at_a_time(), test_a_ray_that_misses_the_model_is_pruned_away(), test_every_triangle_lands_in_exactly_one_leaf() (+3 more)

### Community 158 - "render/environment.py"
Cohesion: 0.12
Nodes (17): A turn about the vertical axis, as a 3x3 matrix., rotation_y(), background_basis(), environment_matrix(), ndarray, The HDRI on the GPU: its textures, the GLSL that reads them, and the light rig.…, Columns that turn a screen position (-1 to 1 each way, 1) into a world ray. An…, World directions into the map's frame, for this view. (+9 more)

### Community 159 - ".paintGL"
Cohesion: 0.25
Nodes (3): Use the same cached visibility test for bones and all point markers., Which part wears the line this frame, and how solid it is, or ``None``. Also…, Hand the renderer the depth grid, or take it away, before a frame.

### Community 160 - "lumpy"
Cohesion: 0.10
Nodes (20): angle_deg(), bent_plate(), lumpy(), ndarray, A flat with a scattering of bad normals is still shaded as that flat. Averaging…, A plate creased down the middle, and which column each vertex is in. Flat to…, Vertices on a turn are ambiguous about their plane, so they are quieted. The…, Splitting a broad flat by place must not invent a turn in it. The plate below… (+12 more)

### Community 161 - "ProgressCard"
Cohesion: 0.19
Nodes (6): _outcome(), ProgressCard, QPainter, One task: its name, its message, its bar, and a cross to stop it. Painted by…, The word a finished card ends on., test_a_card_paints_every_state_it_can_be_in()

### Community 162 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 163 - "RegionSource"
Cohesion: 0.40
Nodes (4): Enum, str, Where the region map comes from., RegionSource

### Community 164 - "Human Skin renderer"
Cohesion: 0.25
Nodes (7): Human Skin renderer, Marks and body regions, Material and transport, Scheduling, precision and compatibility, Surface, The HDRI, Where to change it

### Community 165 - "SectionGizmo"
Cohesion: 0.24
Nodes (6): Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo, The rail stands still while the camera moves, and never leaves the frame., test_section_rail_is_a_screen_space_cue_at_the_right_edge()

### Community 166 - "test_skin_gl.py"
Cohesion: 0.18
Nodes (17): gl_context(), _patch(), fixture, Real GL tests; skipped only when the test host cannot create a GL context., Nearest hits and shadow rays through a deep tree, pixel by pixel, against numpy., The tile wraps: the slope read just past the edge equals the one at the start., Moles and acne darken and redden a patch; a map that gives the patch none takes…, A scene's three tracer tables on the card, bound where a test program reads… (+9 more)

### Community 167 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 168 - ".refresh_list"
Cohesion: 0.20
Nodes (4): QTreeWidgetItem, Rebuild the tree from the store, with the active object current., Offer every object the active one could hang from., Commit a renamed or re-checked row, if anything actually changed.

### Community 169 - "sample_count"
Cohesion: 0.50
Nodes (3): How many samples the framebuffer bound right now is drawing with. One where…, sample_count(), How many samples this view is really drawing with, or ``None``. Asked of GL…

### Community 170 - "_height_of"
Cohesion: 0.40
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 171 - "TriangleIndex"
Cohesion: 0.29
Nodes (6): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., Leaf bounding boxes over a Morton-sorted triangle list., TriangleIndex, test_an_empty_index_returns_no_candidates()

### Community 172 - "SculptCache"
Cohesion: 0.12
Nodes (12): The best ``count`` planes, or as many as the model supports. A model whose…, Holds the working state between one turn of the sliders and the next.…, Drop everything held, so the next call starts from the fit., The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache, The fit is the expensive part and it only goes stale when the model or the…, AutoSmooth reads the normals of a form that has already been built, so it must… (+4 more)

### Community 173 - "README.md"
Cohesion: 0.18
Nodes (15): High Quality shading mode (1.1.0), Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command, High Quality without ray tracing, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter (+7 more)

### Community 175 - "watch_keys"
Cohesion: 0.15
Nodes (14): can_take_key(), is_hotkey_click(), KeyGesture, QObject, QWidget, The gesture that puts a key on a control: Ctrl/Cmd, Alt and a click. It sits…, Whether a mouse press is the assignment gesture rather than a click., Whether a widget is the kind a key can sensibly be put on. A button or a switch… (+6 more)

### Community 176 - "raycast_mesh"
Cohesion: 0.17
Nodes (18): _cross(), intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Row-wise cross product, without :func:`numpy.cross`'s axis shuffling., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``., The closest hit along each of a batch of rays, ``None`` where one misses. One… (+10 more)

### Community 177 - "Coefficients"
Cohesion: 0.13
Nodes (11): Coefficients, What each block of the design matrix counts for, against the normals. A fit…, Whether anything but the normals is being read at all., fit_planes(), The planes of ``mesh`` under ``mode``; empty where the mode needs none., PlaneMode, How the plane directions are arrived at. ``shader_id`` must stay in sync with…, Whether the directions are read off the model rather than imposed. (+3 more)

### Community 178 - "Preferences"
Cohesion: 0.16
Nodes (17): Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, A store of its own, and the application put back the way it was found.…, The font size is a string; everything beside it still arrives., store(), test_a_field_from_a_later_version_is_ignored(), test_a_preference_survives_the_application_closing() (+9 more)

### Community 179 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 180 - "._commit_node_drag"
Cohesion: 0.33
Nodes (3): Record the finished gesture: a move, a resize, or a plain click. A press that…, Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…

### Community 181 - "VideoSettings"
Cohesion: 0.18
Nodes (7): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, TestTiming

### Community 182 - "._draw_hud"
Cohesion: 0.19
Nodes (8): QRectF, QColor, QFont, A short line in one corner of the frame; returns where it went. For an exported…, What the forms tool is waiting for, said in as few lines as it takes., Text as filled outlines; see :func:`markers.draw_text` for why., What the pose tool is waiting for., What the armature tool is waiting for, said in as few lines as it takes.

### Community 183 - "HotkeyBinder"
Cohesion: 0.17
Nodes (11): QShortcut, control_of(), HotkeyBinder, QObject, The live control a control command names, if the window still has it., Turns the map into the shortcuts of one window, and keeps them current., Put every command's keys where they are heard. Cheap; run on any change., Say in a control's tooltip what key it answers to, if it is one of ours. A copy… (+3 more)

### Community 186 - "ModelPanel"
Cohesion: 0.13
Nodes (5): ModelPanel, Reflect the tool state without re-emitting the toggle., Choose the gesture, from the menu or a key., Bake the active object's turn and scale into its mesh., Lists the objects, places the active one, and reports what came out of its file.

### Community 187 - "PreferenceStore"
Cohesion: 0.14
Nodes (12): PreferenceStore, QObject, QSettings, _qcolor(), Push the preferences that something in the process holds a copy of.…, A core colour triple as the Qt colour the palette wants., The preferences, and one signal saying they have changed. A single instance,…, Adopt ``value``, push what has to be pushed, and say so. Always announces, even… (+4 more)

### Community 188 - "MeasurementSettings"
Cohesion: 0.14
Nodes (10): MeasurementSettings, How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., Handle, ndarray, The nearest grabbable endpoint under the cursor, if any. Only unlocked, visible…, Consume a picked point; returns a measurement on the second click., Where a click at ``(x, y)`` would put a point. With free placement the point… (+2 more)

### Community 189 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 190 - "ball"
Cohesion: 0.09
Nodes (33): app(), coarse_lattice(), fixture, MonkeyPatch, Recording a film on a thread, without taking the process down with it. The rest…, Which is what the panel puts its controls to sleep by, so it has to be true…, Shutdown must not care whether the thread beat it to the exit. A recording that…, The guard that decides whether to scrub an existing film or record a new one.… (+25 more)

### Community 191 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 192 - "quad"
Cohesion: 0.67
Nodes (3): fixture, quad(), Two triangles covering the unit square on the z = 0 plane.

### Community 193 - "KeyBox"
Cohesion: 0.19
Nodes (7): QKeySequenceEdit, KeyBox, press(), QWidget, Do to a control what a click would; says whether there was one to do it to., A box that takes one keystroke and says when it has one, or has none. Qt's box…, Show ``keys`` without that counting as the artist entering them.

### Community 194 - ".__init__"
Cohesion: 0.14
Nodes (5): Push the preferences that this window's own parts hold a copy of. The store has…, Put the docks and the hand-built panels back where they were. Unless the artist…, Give each panel a dock of its own, tabbed together on the right. Each panel can…, Single-key shortcuts, scoped so they never eat text input. They only fire while…, Say which panel buttons are the same thing as a menu entry. The button that…

### Community 195 - "._build_menus"
Cohesion: 0.20
Nodes (6): _plain(), QAction, Open the preferences, on one group when the menu asked for one., A menu entry's text as a name: no accelerator ampersand, no trailing dots., Which panels are open, and the panels the artist builds. Rebuilt every time it…, Add a menu entry, optionally with a window-wide shortcut. Given a ``command``…

### Community 196 - "plane_axes.py"
Cohesion: 0.18
Nodes (11): _empty(), ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, A level with no place in it: nearest direction wins, as before., How much surface each vertex stands for: a third of each triangle on it.…, The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to., _split() (+3 more)

### Community 197 - "section.py"
Cohesion: 0.22
Nodes (8): Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Which side of the plane survives the cut., SectionAxis, SectionMode, Cross-section controls: the cutting plane, what it keeps and how it reads.

### Community 198 - "ask_for"
Cohesion: 0.22
Nodes (8): ask_for(), Command, QAction, A menu entry. Its keys are heard anywhere in the window and shown in the menu., A key heard only while the view has the focus. The menu entry for it, if there…, A key heard anywhere in the window, with no menu entry of its own., The gesture's other half: a key for whatever control was Ctrl-Alt-clicked.…, The gesture's other half: Ctrl-Alt-click on a button asks for a key. The…

### Community 201 - "TaskRunner"
Cohesion: 0.21
Nodes (6): QObject, QWidget, Runs work off the GUI thread and keeps the window told. :attr:`started` and…, Every task in flight, oldest first., The blocking task running now, if there is one., TaskRunner

### Community 202 - "matcap_panel.py"
Cohesion: 0.31
Nodes (10): added_matcaps(), forget_matcap(), Matcap selection and colour grading. The grading is done on the matcap itself:…, The matcaps added from outside the folder that are still on disk, newest first.…, Keep ``path`` in the gallery from now on., Take ``path`` out of the gallery; the file itself is left alone., _read_added(), remember_matcap() (+2 more)

### Community 203 - "decode"
Cohesion: 0.27
Nodes (8): _coerce(), decode(), encode(), Any, T, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``.

### Community 204 - "CHANGELOG.md"
Cohesion: 0.22
Nodes (8): Shift-snapped orbiting (1.1.0), Cross-section tool (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding

### Community 205 - "_Encoder"
Cohesion: 0.25
Nodes (5): Queue, _Encoder, QObject, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 206 - "_file_drag"
Cohesion: 0.40
Nodes (5): _file_drag(), A file being dragged over the middle of the view, as ``kind`` of event., Entering, moving and dropping: a drop lands only where the move before it was…, test_a_file_the_window_cannot_open_is_refused_on_the_way_past(), test_a_model_file_is_welcome_at_every_step_of_its_drag()

### Community 207 - "Hit"
Cohesion: 0.16
Nodes (11): Hit, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., snap_to_vertex(), ndarray, Closest surface intersection under the cursor, or ``None``., Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-… (+3 more)

### Community 208 - ".skin_object"
Cohesion: 0.25
Nodes (5): ndarray, The 4x4 that takes a point on the old rest mesh onto the new one. A point sits…, Carry the measurements, annotations, armature and forms through ``carry``., Dress ``obj`` in a skin made for ``skeleton``, as one undo step. ``made`` came…, The 4x4 that carries a point of the file mesh onto the rest mesh. The rest mesh…

### Community 209 - "CancelledError"
Cohesion: 0.29
Nodes (5): Exception, CancelledError, Raised inside the work when it has been told to stop., Say how far along the work is; raises :class:`CancelledError` to stop it. Any…, Raise :class:`CancelledError` if the work has been told to stop.

### Community 210 - "tasks.py"
Cohesion: 0.23
Nodes (11): QIcon, _draw_glyph(), glyph(), lock_icon(), QColor, QPixmap, Small painted icons. Drawing the padlock rather than shipping an image file…, One of the small line drawings above, as an icon. A button whose whole job is… (+3 more)

### Community 211 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 212 - "trusted_roots"
Cohesion: 0.29
Nodes (7): _macos_root_certificates(), The system root certificates as PEM text, or ``""`` if they cannot be read., A TLS context that can actually verify GitHub's certificate. Python's own…, trusted_roots(), SSLContext, Whatever the interpreter was built with, the context has roots in it., test_the_release_check_trusts_a_certificate_bundle()

### Community 213 - "OverlayParts"
Cohesion: 0.29
Nodes (4): OverlayParts, ndarray, Every point the frame will ask the surface about, so it is asked once. Casting…, Which of the things drawn over the model are wanted this time. The viewport…

### Community 214 - "UpdateChecker"
Cohesion: 0.38
Nodes (4): QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., UpdateChecker

### Community 215 - ".plane_span_deg"
Cohesion: 0.33
Nodes (3): Roughly how much of a turn one of those planes covers, in degrees., The plane size of whichever mode is running., Roughly how much of a turn one of those planes covers, in degrees.

### Community 216 - "step"
Cohesion: 0.33
Nodes (6): quad(), The limit the clustered fits exist to lift, stated as a fact., Add one flat quad, with its own vertices, to a mesh under construction., Two broad faces both looking straight up, one raised above the other. The case…, step(), test_reading_the_normals_alone_cannot_tell_that_step_apart()

### Community 217 - "fixture"
Cohesion: 0.33
Nodes (6): app(), model(), fixture, One triangle, which is a mesh as far as any of this is concerned., One offscreen Qt application for the run; see test_film_recorder., window()

### Community 218 - "Projection"
Cohesion: 0.40
Nodes (4): Projection, Enum, str, Projection used by :class:`Camera`.

### Community 219 - "LightSettings"
Cohesion: 0.40
Nodes (4): LightSettings, A key light, an opposing fill and a hemispherical ambient term -- or an HDRI.…, Turn every light by ``degrees`` about the vertical, and tip the key by…, test_turning_the_lights_turns_the_key_and_the_map_together()

### Community 220 - "HotkeyDialog"
Cohesion: 0.50
Nodes (3): HotkeyDialog, QDialog, One keystroke for one command, and the question if it is already taken.

### Community 221 - "_Worker"
Cohesion: 0.40
Nodes (3): Any, The function itself, living on the worker thread., _Worker

### Community 222 - "test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else"
Cohesion: 0.50
Nodes (4): lattice_fineness(), How much finer than usual a detail setting asks the lattice to be. One at the…, The slider's own end already asks for every plane a fit will give, so what a…, test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else()

### Community 223 - "decorate"
Cohesion: 0.50
Nodes (4): decorate(), What a tooltip says about a key., Write a control's key into its tooltip, or take the old one out. The line is…, tip_for()

### Community 227 - "test_the_switch_on_a_dock_bar_is_the_panels_own_visibility"
Cohesion: 0.67
Nodes (3): parametrize, test_a_panel_that_draws_nothing_has_no_switch(), test_the_switch_on_a_dock_bar_is_the_panels_own_visibility()

### Community 228 - "no_ffmpeg"
Cohesion: 0.67
Nodes (3): no_ffmpeg(), fixture, A machine with no video encoder on it, which is most of them.

## Knowledge Gaps
- **7 isolated node(s):** `refview`, `Surface`, `Marks and body regions`, `Material and transport`, `Scheduling, precision and compatibility` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `SceneObject`, `Bounds`, `compute_vertex_normals`, `viewport.py`, `ExportLook`, `load_mesh`, `_wires`, `state.py`, `MeshBuffers`, `ViewerState`, `Skeleton`, `GridSettings`, `test_viewport_markers.py`, `test_body_regions.py`, `PoseTool`, `SkeletonStore`, `SectionSettings`, `plane_volume.py`, `test_spatial.py`, `auto_skin`, `PlaneSet`, `lumpy`, `test_plane_clusters.py`, `RegionSource`, `test_forms.py`, `test_skin_gl.py`, `convex.py`, `Camera`, `autoskin.py`, `TriangleIndex`, `gltf_loader.py`, `SculptCache`, `raycast_mesh`, `body_regions.py`, `Coefficients`, `plane_clusters.py`, `SkinSettings`, `FilmExport`, `test_skeleton.py`, `ball`, `quad`, `FormTool`, `plane_axes.py`, `test_objects.py`, `section.py`, `test_plane_solids.py`, `test_skin.py`, `save_mesh`, `ShadingMode`, `mesh_renderer.py`, `SkinEdit`, `Hit`, `.skin_object`, `core/environment.py`, `pose_panel.py`, `PlaneSettings`, `PrimaryForm`, `step`, `load_stl`, `OrientationSettings`, `plane_axes`, `Path`, `Rig`, `.source_mesh`, `Session`, `core/__init__.py`, `forms.py`?**
  _High betweenness centrality (0.189) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `._upload_sculpt`, `._sync_scene`, `.stage_images`, `SurfacePicker`, `ExportLook`, `MainWindow`, `viewport.py`, `state.py`, `ViewerState`, `._picker`, `test_viewport_markers.py`, `PoseTool`, `.paintGL`, `PlaneSet`, `SectionGizmo`, `sample_count`, `ExportVideoDialog`, `film_export.py`, `._active_changed`, `Preferences`, `._commit_node_drag`, `FilmExport`, `application.py`, `MeasureTool`, `.__init__`, `FormTool`, `test_objects.py`, `._place_joint`, `ObjectTool`, `._place_form_landmark`, `ArmatureTool`, `_Encoder`, `NavigationController`, `PrimaryForm`, `._scene_center`, `.mouseReleaseEvent`, `._place_armature_node`, `ViewportOverlay`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `Viewport`, `SceneObject`, `MainWindow`, `viewport.py`, `state.py`, `Armature`, `CameraPanel`, `test_viewport_markers.py`, `test_body_regions.py`, `test_planes_panel.py`, `PoseTool`, `MeasurePanel`, `auto_skin`, `README.md`, `body_regions.py`, `Preferences`, `test_matcap_preview.py`, `._draw_hud`, `SkinSettings`, `application.py`, `MeasureTool`, `.__init__`, `test_objects.py`, `save_mesh`, `TaskRunner`, `test_custom_panels.py`, `SkinEdit`, `.skin_object`, `._commit_objects`, `test_forms_panel.py`, `OverlayParts`, `QPointF`, `PrimaryForm`, `MatcapPanel`, `Panel`, `test_elements.py`, `Mesh`, `OrientationSettings`, `.source_mesh`, `Session`, `ViewportOverlay`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 60 inferred relationships involving `Mesh` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Mesh` has 60 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `OverlayParts`) actually correct?**
  _`ViewerState` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Skeleton` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Skeleton` has 9 INFERRED edges - model-reasoned connections that need verification._