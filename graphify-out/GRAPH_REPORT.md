# Graph Report - reference-viewer  (2026-09-18)

## Corpus Check
- 166 files · ~528,441 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5801 nodes · 13556 edges · 202 communities (193 shown, 9 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 701 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8a6aefb4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- form_group
- test_preferences.py
- update_check.py
- Viewport
- SceneObject
- Bounds
- MainWindow
- Stroke
- GifWriter
- linalg.py
- SceneRenderer
- elements/__init__.py
- main_window.py
- MeshBuffers
- Armature
- environment.yml
- .apply_session
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
- PlaneSettings
- test_camera.py
- test_plane_clusters.py
- WakeLock
- test_forms.py
- MatcapPreview
- Frame
- film_export.py
- convex.py
- Camera
- autoskin.py
- ValueSlider
- gltf_loader.py
- ExportVideoDialog
- VideoSettings
- landmarks.py
- Agent Graph-First Instructions
- body_regions.py
- Mesh
- test_matcap_preview.py
- test_armature.py
- ArmaturePanel
- SkinSettings
- test_hotkeys.py
- .cancel
- FormsPanel
- PlanesPanel
- test_skeleton.py
- Progress
- Workspace
- HotkeyStore
- Solid
- application.py
- MeasureTool
- Link
- PrimaryForm
- ShadingMode
- test_objects.py
- test_skin.py
- test_plane_solids.py
- ObjectTool
- Path
- ArmatureTool
- mesh_renderer.py
- load_matcap_pixels
- test_custom_panels.py
- ViewerState
- core/preferences.py
- VideoError
- NavigationController
- Joint
- ._commit_objects
- test_forms_panel.py
- plane_solids.py
- QPointF
- build_form
- MatcapPanel
- AnnotatePanel
- frame.py
- Panel
- quat_to_matrix
- test_elements.py
- WholeFaceToggles
- compute_vertex_normals
- ReflowLayout
- Measurement
- ColorButton
- OrientationSettings
- clone.py
- skin_detail.py
- Path
- ._turn
- .mouseReleaseEvent
- test_panel_docks.py
- OverlayParts
- ._place_armature_node
- test_tasks.py
- GuideRun
- DockTitle
- test_reflow.py
- ._oriented
- Task
- scene.py
- ._build_objects
- test_open_files.py
- settings.py
- Session
- AddItem
- ViewportOverlay
- project_visible
- ArmatureStore
- SetAttributes
- _tab_switch
- Reflow
- forms.py
- SectionPanel
- ._upload_sculpt
- ._sync_scene
- .stage_images
- SurfacePicker
- ExportLook
- obj_loader.py
- preview
- symbol_button
- matcap_panel.py
- Release
- load_mesh
- OpenRequests
- _drag_over
- spatial.py
- palette.py
- MatcapSettings
- ._picker
- ._carrying_a_copy
- euler_to_quat
- app
- ._current_skeleton
- FormStore
- test_body_regions.py
- ContourShadingSettings
- Texture2D
- SkeletonStore
- restored
- .refresh
- test_spatial.py
- test_the_switch_is_not_squeezed_to_nothing
- shaders.py
- .paintGL
- load_obj
- ProgressCard
- .column_of
- RegionSource
- Human Skin renderer
- SectionGizmo
- .from_dict
- coarse_lattice
- .refresh_list
- sample_count
- _height_of
- TriangleIndex
- SculptCache
- mesh_io.py
- ._active_changed
- TestEven
- raycast_mesh
- quat_from_axis_angle
- ._add_skeleton
- app
- ._commit_node_drag
- FormRun
- ._place_banner
- .refresh_camera
- .selected_objects
- test_the_dock_of_a_panel_taken_away_is_used_again
- ModelPanel
- PreferenceStore
- ._offer_humanoid_mapping
- _NameOnlyDelegate
- coarse_lattice
- release.yml
- quad
- ._menu_action
- ._place_joint
- ._place_form_landmark
- _file_drag
- Hit
- PanelDock
- tasks.py
- ._build
- .pending

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 230 edges
2. `ViewerState` - 176 edges
3. `Viewport` - 152 edges
4. `Skeleton` - 114 edges
5. `MainWindow` - 99 edges
6. `Camera` - 98 edges
7. `SceneObject` - 83 edges
8. `Armature` - 81 edges
9. `PrimaryForm` - 79 edges
10. `PlaneSettings` - 69 edges

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

## Communities (202 total, 9 thin omitted)

### Community 0 - "form_group"
Cohesion: 0.06
Nodes (36): QScrollArea, A layout that turns a column of groups into columns when given the width. A…, describe(), group_of(), listed(), What a command is called, for a list or a question about it., The commands worth a row in the editor, in the order they are shown. Every…, The preferences as they stand. Treat as read-only; use :meth:`set`. (+28 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.07
Nodes (43): _clamp(), Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, Pull anything out of range back into it. The window cannot produce these…, Read the preferences off the machine. Never raises., app(), model() (+35 more)

### Community 2 - "update_check.py"
Cohesion: 0.10
Nodes (31): check_for_update(), fetch_latest_release(), is_newer(), _macos_root_certificates(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and… (+23 more)

### Community 3 - "Viewport"
Cohesion: 0.06
Nodes (15): QOpenGLWidget, One of the renderer's :data:`~refview.render.mesh_renderer.ANTIALIASING_MODES`., Renders the scene and turns mouse gestures into camera and tool actions., Slide the view so a point sits at the centre, keeping the angle., The gesture a key press chooses, if the transform tool is armed to hear it., A form changed: work its clay out again and redraw., Slide the view so a measurement sits at the centre, keeping the angle., Hand the renderer how solid each object is now; nothing else moved. (+7 more)

### Community 4 - "SceneObject"
Cohesion: 0.07
Nodes (24): duplicate_object(), merge_objects(), ObjectSettings, ObjectStore, ndarray, Snapshot, What a parent's state means for its children, and how the tools scale. Each is…, One model in the scene. Three meshes are kept, as the viewer kept them when… (+16 more)

### Community 5 - "Bounds"
Cohesion: 0.09
Nodes (27): build_grid(), GridLines, GridSettings, nice_step(), Reference grids on the three axis planes, fading with distance. A grid gives…, Segments, with their colours and widths, ready for the stroke buffer., Every line of every enabled grid, or ``None`` when none is on., The nearest 1, 2 or 5 times a power of ten at or below ``value``. (+19 more)

### Community 6 - "MainWindow"
Cohesion: 0.05
Nodes (20): MainWindow, QMainWindow, Put every panel button and menu entry where the tools now stand. Only one tool…, Swap between the eraser and the drawing mode it was called from., Open the preferences, on one group when the menu asked for one., Push the preferences that this window's own parts hold a copy of. The store has…, Open an empty panel of the artist's own and bring it to the front., Put the docks and the hand-built panels back where they were. Unless the artist… (+12 more)

### Community 7 - "Stroke"
Cohesion: 0.05
Nodes (39): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+31 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "linalg.py"
Cohesion: 0.12
Nodes (25): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, quat_between(), Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-… (+17 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.06
Nodes (44): Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., light_directions(), normal_matrix(), ndarray (+36 more)

### Community 11 - "elements/__init__.py"
Cohesion: 0.05
Nodes (55): Which keys do what, as the artist has decided rather than as it ships. A hotkey…, make_switch(), QCheckBox, One dock per panel, with a bar of its own across the top. Every panel is its…, Put a show/hide switch at the left of the bar and return it., A square that is on or off, and is clickable all over. A check box decides…, The square that shows or hides what a panel draws. One is kept on each dock's…, Switch (+47 more)

### Community 12 - "main_window.py"
Cohesion: 0.04
Nodes (71): Quat4, Freehand annotations painted onto the model surface. A stroke is a polyline of…, BoneLabels, Buried, Enum, str, A graph of named points under the form, and the wire it stands for. An armature…, When the length of a bone is written beside it. (+63 more)

### Community 13 - "MeshBuffers"
Cohesion: 0.10
Nodes (9): MeshBuffers, Forget the contents without releasing the buffer objects., Replace the model: the whole scene as one mesh, and the objects it is made of.…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are…, Every buffer standing for the model, for the passes that draw them all alike., Replace the annotation geometry; pass an empty list to hide it. (+1 more)

### Community 14 - "Armature"
Cohesion: 0.04
Nodes (65): Armature, ArmatureNode, Bone, ndarray, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, Every node position as ``(n, 3)``., The two points a bone runs between, or ``None`` if it dangles. (+57 more)

### Community 15 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 16 - ".apply_session"
Cohesion: 0.10
Nodes (11): A parenting policy changed: what is shown and how solid may have too., Take the display unit from the file when the format declares one. Only glTF…, Fit the scene in the view without changing the direction., Adopt a session's settings, leaving the loaded meshes alone., The skeletons changed; re-pose the model if one of them drives it. ``live`` is…, The skeleton bound to ``obj``'s rig, if one is and no other object has it., ``rest`` as the bound skeleton poses it, or ``rest`` itself. Skinning is done…, Join the shown objects into :attr:`mesh` and say that it changed. ``live``… (+3 more)

### Community 17 - "Skeleton"
Cohesion: 0.08
Nodes (20): _matrix16(), A copy with the rest translation replaced and the frame kept., A tree -- or a forest -- of joints and the pose they stand in., Every joint, parents before children. A file may list a child before its…, Every joint below ``index``, nearest first., Every joint's transform in scene space, as ``(n, 4, 4)``. With ``rest`` the…, Where every joint sits, as ``(n, 3)``., Every ``(parent, child)`` pair, parents first. (+12 more)

### Community 18 - "_Target"
Cohesion: 0.07
Nodes (13): AccumTarget, DepthTarget, GeometryTarget, A depth-only framebuffer, sampled afterwards as a texture., ``clamp_to_lit`` makes everything outside the map read as unshadowed., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the…, The pair of buffers a see-through model is summed into. Attachment 0 holds the…, Empty both sums, and the depth nothing has been laid into yet. Zero starts each… (+5 more)

### Community 19 - "CameraPanel"
Cohesion: 0.14
Nodes (7): CameraPanel, QListWidgetItem, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions., test_the_camera_panel_takes_the_clip_planes_in_hand_where_the_fit_left_them()

### Community 20 - "PosePanel"
Cohesion: 0.07
Nodes (14): _NameOnlyDelegate, PosePanel, QStyledItemDelegate, QWidget, Highlight a row, in the tree and in the view., Highlight the row for a joint picked in the view., Arms the pose tool, lists the joints and poses the selected one., Adopt the viewport's tools: the pose tool, and the armature's for its selection. (+6 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): Fill the shader's table with a level, if it is not already in it., ndarray, RuntimeError, Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "PoseTool"
Cohesion: 0.15
Nodes (25): PoseTool, Turns pulls on joints into pose edits, and clicks into new joints., app(), _arm(), _event(), _front_camera(), fixture, The pose tool, its gestures in the viewport, and the panel that lists the… (+17 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.07
Nodes (25): app(), _names(), panel(), fixture, The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as… (+17 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.13
Nodes (8): MeasurePanel, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn.

### Community 25 - "BookmarkStore"
Cohesion: 0.13
Nodes (7): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., test_bookmarks_cycle_and_wrap()

### Community 26 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 27 - "SectionSettings"
Cohesion: 0.08
Nodes (30): Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, The direction the section plane faces. (+22 more)

### Community 28 - "plane_volume.py"
Cohesion: 0.03
Nodes (117): Work the form stage by stage, handing each one back as it is finished. A…, record(), _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field() (+109 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "auto_skin"
Cohesion: 0.15
Nodes (32): auto_skin(), bone_segments(), Skin ``mesh`` to ``skeleton``, both given in the same coordinates. The skeleton…, ``names`` with any repeat numbered, since the skin matches joints by name., Every bone as ``(start, end)`` points, and which joint each belongs to. A joint…, unique_names(), AutoSkinSettings, What the artist sets before auto-skinning, and rarely needs to. (+24 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.10
Nodes (13): Chooses the shading model and edits its light and surface parameters., Where on the body the marks fall, and how much of each in each region., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Slot that writes one field of the contour shading settings., Slot that writes one field of the grid settings. (+5 more)

### Community 32 - "PlaneSettings"
Cohesion: 0.04
Nodes (64): QThread, Film, film_key(), The stages a form passes through on its way from a block to a figure. The…, The stage at ``index``, clamped to what has actually been recorded., What a film depends on. Everything that changes the shape of any stage, and…, A stage as it is to be drawn, with its normals read at ``smooth``. Kept out of…, One moment in the making of a form. :attr:`solids` is how many blocks or lumps… (+56 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (59): The joint list with ``index`` resting at ``target`` and its children left be., angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad() (+51 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (32): c_void_p, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., Holds sleep off while the window that owns it is the one in front. The class… (+24 more)

### Community 36 - "test_forms.py"
Cohesion: 0.06
Nodes (45): The hull of the points with its faces bowed out; see :func:`rounded_hull`., median_plane_ready(), mirror_form_landmarks(), The midline landmarks, which are what the median plane is fitted to., The landmark list with every paired landmark reflected into place. The…, Whether enough of the midline is down for the mirror to have a plane., Placing the landmarks of a form, led by a preset or by the artist, and…, _closed() (+37 more)

### Community 37 - "MatcapPreview"
Cohesion: 0.07
Nodes (19): QMenu, MatcapPreview, _push_preview(), Path, QImage, QRect, QSize, QWidget (+11 more)

### Community 38 - "Frame"
Cohesion: 0.06
Nodes (30): carried(), in_flight(), _push_frame(), The id of what a copy copies, or an empty string., Nothing: each row inside the copy is linked on its own., Read a drag's payload back, or ``None`` if it is not one of ours., source_of(), CustomPanel (+22 more)

### Community 39 - "film_export.py"
Cohesion: 0.08
Nodes (17): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+9 more)

### Community 40 - "convex.py"
Cohesion: 0.13
Nodes (21): convex_hull(), flat_mesh(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, The outward unit normal at each vertex: the area-weighted mean of its faces'. A…, The barycentric ``(w, u, v)`` of an even grid over a triangle. (+13 more)

### Community 41 - "Camera"
Cohesion: 0.06
Nodes (32): Camera, ndarray, Near/far planes fitted to the scene bounding sphere., The near and far planes this frame: the fitted ones, unless set by hand. A…, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Rays through a batch of pixels, as ``(origins, unit directions)``, ``(N, 3)``…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Project ``(N, 3)`` world points to ``(xs, ys, ndc_depths)`` in widget pixels. (+24 more)

### Community 42 - "autoskin.py"
Cohesion: 0.07
Nodes (38): AutoSkin, AutoSkinError, _baked_rest(), _conjugate_gradients(), _CotLaplacian, _envelope_weights(), _Graph, _heat_weights() (+30 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (13): _clone_slider(), _pull_slider(), _push_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end. (+5 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.10
Nodes (35): Units are adopted, never guessed, _accessor(), _buffers(), _first_skin(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry() (+27 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.09
Nodes (15): Queue, _Encoder, ExportVideoDialog, Path, QDialog, QObject, QWidget, The encoding itself, living on a thread of its own. It takes frames off a short… (+7 more)

### Community 46 - "VideoSettings"
Cohesion: 0.09
Nodes (23): ffmpeg_path(), open_writer(), Path, How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds. (+15 more)

### Community 47 - "landmarks.py"
Cohesion: 0.11
Nodes (28): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _humanoid_landmarks(), median_plane(), _mid() (+20 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "body_regions.py"
Cohesion: 0.12
Nodes (23): band_weights(), BodySource, bone_weights(), build_body_map(), looks_like_a_figure(), ndarray, Where on the body a point of the skin is, so that the skin can be marked as…, The bones a skeleton's humanoid roles describe, as ``(count, 7)`` rows. Each… (+15 more)

### Community 50 - "Mesh"
Cohesion: 0.03
Nodes (102): concatenated(), _gathered(), loose_parts(), Mesh, ndarray, Triangle-mesh containers shared by the loader, the renderer and picking., Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations… (+94 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.12
Nodes (28): QPoint, _drag(), parametrize, The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc., Dragging further than the range goes is not a negative gamma., Alt and a drag copies a control; the disc must not swallow that. (+20 more)

### Community 52 - "test_armature.py"
Cohesion: 0.05
Nodes (77): build_humanoid(), _kept_laying(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, Fresh bones, laid the way the armature was already laying them. The bone list…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _chain(), _derived() (+69 more)

### Community 53 - "ArmaturePanel"
Cohesion: 0.05
Nodes (26): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Begin a preset run against a fresh armature., Take back the landmark before this one and ask for it again., Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked. (+18 more)

### Community 54 - "SkinSettings"
Cohesion: 0.11
Nodes (19): BodyRegionSettings, Where the regions come from, and what each does to the marks., One region's multiplier for ``effect`` after another, in :data:`REGIONS` order., LightSettings, A key light, an opposing fill and a hemispherical ambient term., Material parameters shared by the analytic shading modes., SurfaceSettings, Artist-facing skin parameters, in sRGB colours and relative scene units.… (+11 more)

### Community 55 - "test_hotkeys.py"
Cohesion: 0.05
Nodes (42): QKeySequence, Command, HotkeyMap, Any, Whether the artist has moved this command off what it ships with., Which command has these keys, if any., Every command with keys on it, declared or not, as id -> keys., Put ``keys`` on a command, taking them off whatever had them. Returns the id of… (+34 more)

### Community 56 - ".cancel"
Cohesion: 0.13
Nodes (8): frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in…, Offer the encoder the last stage before the first is written. Only the built-in…, Close, and do not leave an encoding thread behind. Waiting is the right thing…, parametrize

### Community 57 - "FormsPanel"
Cohesion: 0.05
Nodes (31): FormsPanel, QTreeWidgetItem, Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Begin a run against a fresh form: a preset's walk, or a freeform's., Take up the selected freeform again, so more landmarks can go on it. The same…, The freeform the highlighted row belongs to, when no run is on. (+23 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.09
Nodes (18): PlanesPanel, QListWidgetItem, Lay one length of wire earlier or later, as one undoable step., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Show what this way of working needs, and put the rest away. A setting that does… (+10 more)

### Community 59 - "test_skeleton.py"
Cohesion: 0.08
Nodes (44): detail_joints(), Which joints are detail, and which kind, read off their names. A toe past the…, The joint list with the detail taken out, and how much of each kind went. What…, The joint list with these roles written in, and every other role cleared., simplified(), with_roles(), make_joint(), A joint at a position in its parent's frame, with no turn of its own. (+36 more)

### Community 60 - "Progress"
Cohesion: 0.09
Nodes (18): Progress, What a long piece of work says about itself while it runs, and how it is…, Ask the work to stop at its next report., How far along, 0 to 1, or ``None`` when the work has not said., Whether the work has said how much there is to do., A window onto part of a parent's range; see :meth:`Progress.slice`., A progress nobody is watching, for work run without a window., How far a task has got, and whether it has been told to stop. ``on_change`` is… (+10 more)

### Community 61 - "Workspace"
Cohesion: 0.08
Nodes (19): QTabBar, QMainWindow, QObject, QSettings, Keep every switch agreeing with the panel it speaks for., Hang a show/hide switch on every dock tab that wants one. A dock stacked behind…, The panel whose dock is called ``title``, if there is one., Open the dock a hand-built panel lives in and bring it to the front. (+11 more)

### Community 62 - "HotkeyStore"
Cohesion: 0.05
Nodes (43): QKeySequenceEdit, QShortcut, ask_for(), assign(), decorate(), HotkeyBinder, HotkeyDialog, HotkeyStore (+35 more)

### Community 63 - "Solid"
Cohesion: 0.10
Nodes (40): One convex piece of a form: its hull vertices and outward-wound faces., The longest side of the box the solid sits in., Whether a point lies inside, or within ``slack`` of the surface., Solid, _across(), blend_rings(), build_head(), build_pelvis() (+32 more)

### Community 64 - "application.py"
Cohesion: 0.09
Nodes (28): ArgumentParser, Namespace, QSplashScreen, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font(), main() (+20 more)

### Community 65 - "MeasureTool"
Cohesion: 0.14
Nodes (8): MeasureTool, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., Where a click at ``(x, y)`` would put a point. With free placement the point…, Where a grabbed endpoint should move to. Free placement -- and a drag that…

### Community 66 - "Link"
Cohesion: 0.12
Nodes (9): CloneGesture, Link, _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original., Whether the copy is being used right now and must not be written. (+1 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.05
Nodes (48): FormLandmarkRef, PlacedLandmark, Point3, One anatomical point the artist put on the model during a guided run., The landmark list with one point moved, and no longer a guess. A landmark the…, The landmark list with these points taken back off the model. More than one at…, FormSettings, PrimaryForm (+40 more)

### Community 68 - "ShadingMode"
Cohesion: 0.09
Nodes (16): Shift-snapped orbiting (1.1.0), Cross-section tool (1.1.0), High Quality shading mode (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4 (+8 more)

### Community 69 - "test_objects.py"
Cohesion: 0.12
Nodes (33): Where an object stands relative to its parent: an affine placement. Held as the…, Transform, app(), _key(), _mouse(), _overridden(), fixture, Several objects in one scene: placing, linking, merging, splitting, saving. (+25 more)

### Community 70 - "test_skin.py"
Cohesion: 0.10
Nodes (21): build_scene(), ndarray, Stackless BVH tables for the OpenGL 3.3 skin tracer (no compute extension).…, Build on a worker from the immutable meshes currently drawn by the renderer., Pack a linear texel array within the driver's actual 2D texture limit., texture_table(), TraceScene, pixel_jitter() (+13 more)

### Community 71 - "test_plane_solids.py"
Cohesion: 0.03
Nodes (150): auto_smooth(), A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), film_of(), parametrize (+142 more)

### Community 72 - "ObjectTool"
Cohesion: 0.12
Nodes (14): _axis_param(), Gizmo, _Grip, ObjectTool, ndarray, The three directions the arms run along, in world space. A move and a turn are…, Where the gizmo for an object at ``world`` falls on screen, or ``None`` if…, Which handle a screen point is over: ``"centre"``, ``"x"``, ``"y"``, ``"z"`` or… (+6 more)

### Community 73 - "Path"
Cohesion: 0.10
Nodes (18): ObjectRecord, What a session writes down about an object; the mesh itself stays in its file., The store as a session writes it: parents by index into the same list., records_for(), Path, Set the active matcap, or fall back to the built-in one., Write the document, and whatever the window says its layout is. The layout…, Write every skin made here beside the session; see :mod:`rig_file`. (+10 more)

### Community 74 - "ArmatureTool"
Cohesion: 0.05
Nodes (49): BoneRef, LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, _project(), Handle, ndarray (+41 more)

### Community 75 - "mesh_renderer.py"
Cohesion: 0.06
Nodes (34): bind_default(), ColorTarget, FrameTarget, Offscreen render targets used by the high-quality, ghost and smoothing passes.…, A single-channel colour framebuffer, used for the occlusion buffers., Restore a framebuffer captured with :func:`current_framebuffer`., The whole frame, drawn offscreen so it can be smoothed on the way out. A colour…, OpenGL rendering layer: shader programs, textures and the scene renderer. (+26 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.17
Nodes (21): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+13 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.08
Nodes (16): app(), custom(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error., A group is not a row, so it goes ahead of the group it was dropped on., One offscreen Qt application for the run; see test_film_recorder., It is named "Offset" in the panel it came from; it says so here too. (+8 more)

### Community 78 - "ViewerState"
Cohesion: 0.06
Nodes (24): BakeEdit, Command, ndarray, QObject, Write ``obj``'s turn and scale into its mesh, leaving it standing as it is.…, Dressing an object in a skin made for a skeleton, or taking it off. One step…, The 4x4 that takes a point on the old rest mesh onto the new one. A point sits…, Carry the measurements, annotations, armature and forms through ``carry``. (+16 more)

### Community 79 - "core/preferences.py"
Cohesion: 0.12
Nodes (18): _as_kind_of(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any, What the artist prefers, as distinct from what the document says. There are two… (+10 more)

### Community 80 - "VideoError"
Cohesion: 0.18
Nodes (12): _encode_arguments(), _encoders(), _FFmpegWriter, _no_window(), RuntimeError, An export that could not be written, said in words for the artist., Which encoders this ffmpeg was built with. Asked once, because a build without…, Keep a console window from flashing up on Windows for each ffmpeg call. (+4 more)

### Community 81 - "NavigationController"
Cohesion: 0.08
Nodes (17): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Degrees of yaw per pixel, signed by whether the drag is inverted. (+9 more)

### Community 82 - "Joint"
Cohesion: 0.12
Nodes (11): Joint, _pose_matrices(), ndarray, Whether the pose differs from the rest at all., The list with these joints -- or every joint -- put back at rest., One joint: where it sits at rest, and how it is turned right now., A document skeleton standing exactly where the file's joints stand., Which document joint each rig joint answers to. Returns two ``(j,)`` arrays:… (+3 more)

### Community 83 - "._commit_objects"
Cohesion: 0.07
Nodes (20): ObjectsEdit, Snapshot, Scale ``objects`` so each is the size of the active one, as one undo step. The…, The largest of ``obj``'s three extents as it stands in the world., Re-read how solid each part is drawn, without touching the geometry., An edit to the objects -- a move, a parenting, a removal -- as two snapshots.…, Where everything stands now; the start of a gesture keeps one., Move each bound skeleton by however far its object moved since ``before``. (+12 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.11
Nodes (30): app(), _click(), panel(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The… (+22 more)

### Community 85 - "plane_solids.py"
Cohesion: 0.09
Nodes (29): planes_for(), How many solids each stage of a film is made of. Every count from the coarsest…, The detail setting that asks for ``solids``, or ``None`` if none does. The…, stage_counts(), block_count(), piece_count(), ndarray, Handing the planes of a fit to the thing that actually works the volume. The… (+21 more)

### Community 86 - "QPointF"
Cohesion: 0.21
Nodes (11): QPointF, draw_rail(), draw_text(), Shared marker appearance, visibility, and constrained depth gestures., One marker object for endpoints, nodes, landmarks and tool previews., Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, The screen-space cue for one degree of freedom. A vertical rail that fades out…, VisualMarker (+3 more)

### Community 87 - "build_form"
Cohesion: 0.12
Nodes (24): merged(), Several flat meshes as one, or ``None`` when there is nothing to draw., build_form(), built_count(), form_mesh(), landmark_signature(), The solids of every stage the landmarks can build, coarsest first. A stage…, How many stages actually have clay in them, counting from the first. (+16 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.15
Nodes (10): MatcapPanel, Rebuild the thumbnail list from the resources folder., The disc was dragged: show the renderer and the numbers what it did., A different matcap: the disc draws whichever one is on the model., Put the numbers back in line with the settings, and redraw the disc. Separate…, Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, It is the panel's main control; a click on a bar must not take it away. (+2 more)

### Community 89 - "AnnotatePanel"
Cohesion: 0.20
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 90 - "frame.py"
Cohesion: 0.08
Nodes (16): FrameBar, framed(), QFormLayout, QPainter, QSize, QWidget, A titled frame that folds away behind its own bar. Every group of controls in…, The mark beside a group's name: filled when open, a ring when shut. It is the… (+8 more)

### Community 91 - "Panel"
Cohesion: 0.12
Nodes (8): Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Whether what this panel draws is on screen, or ``None`` if it draws nothing.…, Show or hide what this panel draws; see :meth:`shown`., Ignore widget signals for the duration of the block., Nothing: the reflow already packs its groups against the top. Kept because…

### Community 92 - "quat_to_matrix"
Cohesion: 0.13
Nodes (12): compose(), quat_to_matrix(), The 3x3 rotation a unit quaternion stands for., A 4x4 from a translation, a quaternion and a scale, applied scale first., ndarray, The turn the parent takes so that joint ``index`` points at ``target``. The…, The rotation joint ``index`` takes after rolling about its own bone., The pose shift that puts joint ``index`` at ``target``, children and all. (+4 more)

### Community 93 - "test_elements.py"
Cohesion: 0.07
Nodes (23): app(), fixture, Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., A matcap has no light to aim, so the Light group goes -- and its space. The… (+15 more)

### Community 94 - "WholeFaceToggles"
Cohesion: 0.14
Nodes (10): QApplication, QObject, Making the whole of a switch the part you can press. The theme turns every…, Turns a press anywhere on a switch into a click on it., Put the rule in place for every switch in the application., WholeFaceToggles, The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter. (+2 more)

### Community 95 - "compute_vertex_normals"
Cohesion: 0.13
Nodes (21): compute_vertex_normals(), Area-weighted smooth vertex normals for an indexed triangle soup., _ascii_corners(), _binary_corners(), load_stl(), ndarray, Path, Binary and ASCII STL reader. STL stores three loose corners per facet and… (+13 more)

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - "Measurement"
Cohesion: 0.10
Nodes (13): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+5 more)

### Community 98 - "ColorButton"
Cohesion: 0.06
Nodes (23): _clone_point(), _clone_swatch(), _pull_point(), _pull_swatch(), _push_point(), _push_swatch(), _AxisBox, ColorButton (+15 more)

### Community 99 - "OrientationSettings"
Cohesion: 0.10
Nodes (24): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Path, Turn every object the same way; see :meth:`set_object_orientation`. For files…, Turn one object, bringing the marks made on it along. Measurements,…, Turning an imported model the right way up., A Z-up scan and a Y-up sculpt stand in one scene, each read its own way. (+16 more)

### Community 100 - "clone.py"
Cohesion: 0.06
Nodes (61): QAbstractButton, QComboBox, QLineEdit, QSlider, QSpinBox, _begin(), can_clone(), clone() (+53 more)

### Community 101 - "skin_detail.py"
Cohesion: 0.18
Nodes (19): burley_marginal(), burley_profile(), cellular(), diffusion_lut(), _fade(), fbm(), ndarray, Procedural skin micro-relief and the pre-integrated diffusion table. Reference… (+11 more)

### Community 102 - "Path"
Cohesion: 0.13
Nodes (11): A flat-shaded mesh, every triangle with its own three corners. Corners are not…, Path, Pick up whatever was last being worked on, if that was asked for. A session…, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window. In the…, Read a model file off the window, then hand it to ``adopt`` here., Add a model to the scene beside what is already there. (+3 more)

### Community 103 - "._turn"
Cohesion: 0.13
Nodes (9): _angle(), Redraw from the settings, which something else has changed., Put the grading back, which is the one thing a disc cannot show., Turn the matcap by the angle the cursor swept about the centre. By angle and…, Two grades on one drag: one along each axis of the movement. Both move together…, Keep the angle in -180 to 180, the range the setting is stored in., The angle of ``point`` about ``centre``, anticlockwise with y upwards., An angle difference brought back into -pi to pi. (+1 more)

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.10
Nodes (10): Record the finished drag as a single undo step., Alt forces the camera gesture, whichever tool is armed., Record the finished drag as one step, or read a press as a selection., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Make the object under the cursor the active one., Record the finished pull as one step, or read a press as a selection., Track the joint and bone under the cursor; True when either changed. (+2 more)

### Community 105 - "test_panel_docks.py"
Cohesion: 0.07
Nodes (20): parametrize, Each panel in a dock of its own, and putting the docks back next time. Two…, An older file must not be able to sweep away the artist's own panels., Not "clear the setting and restart": tidied now, or it is not tidying., They are work, not arrangement., A dock puts the panel below its bar's *hint*, not below its bar. Leave the hint…, The crash this is about takes the process with it, so arriving is passing., The path the artist actually walks: File, Load Session, twice. (+12 more)

### Community 106 - "OverlayParts"
Cohesion: 0.10
Nodes (10): Which of the things drawn over the model belong in the frames., MarkerVisibility, Cache surface occlusion by view and position for every kind of marker. The…, Whether the last pass is recent enough to be read instead of repeated., Mark these points as standing in front of the surface, untested. For frames…, Answer for a batch of points at once, ahead of being asked one by one. Every…, OverlayParts, ndarray (+2 more)

### Community 107 - "._place_armature_node"
Cohesion: 0.33
Nodes (3): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 108 - "test_tasks.py"
Cohesion: 0.15
Nodes (18): BodyMap, Region weights over the scene, as two RGBA volumes the shader samples by…, app(), fixture, Work run off the window, and the cards that show it running., Turn the event loop until ``until()`` says so, or give up., runner(), _spin() (+10 more)

### Community 109 - "GuideRun"
Cohesion: 0.40
Nodes (3): GuideRun, Begin a preset run against an armature already in the store., A guided preset part-way through. The index walks the preset's own list rather…

### Community 110 - "DockTitle"
Cohesion: 0.13
Nodes (7): QToolButton, DockTitle, QSize, QWidget, The bar across the top of a dock: a switch, a name and two buttons., As tall as the bar really is. A dock puts the panel directly below its title…, StandardPixmap

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - "._oriented"
Cohesion: 0.20
Nodes (6): setter, The active object turned and centred but not posed or placed., The active object exactly as its file stored it., Set the active object's file mesh; its rest mesh is turned from it as at a load., The active object, made on the spot when a mesh is handed to an empty scene., Turn a freshly read mesh the right way up and centre it.

### Community 113 - "Task"
Cohesion: 0.11
Nodes (14): BaseException, QObject, T, Ask the work to stop. It stops at its next report, not before., Mark the task over. The runner does this; a begun task's driver does., Runs work off the GUI thread and keeps the window told. :attr:`started` and…, Every task in flight, oldest first., The blocking task running now, if there is one. (+6 more)

### Community 114 - "scene.py"
Cohesion: 0.12
Nodes (14): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis, _bare(), Several models in one scene: what each is called, where it stands, what it…, An angle in (-180, 180], with the floating-point dust brushed off. (+6 more)

### Community 115 - "._build_objects"
Cohesion: 0.19
Nodes (6): _ObjectTree, QPushButton, QWidget, A tree whose rows can be dropped onto one another to hang one from another. Qt…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 116 - "test_open_files.py"
Cohesion: 0.18
Nodes (9): app(), opened(), fixture, Files arriving from outside: the command line, a drop, or the desktop's "Open…, One offscreen Qt application for the run; see test_film_recorder., What the window was asked to open, by kind, without loading anything., Finder sends the launching file as an event, which can land before the window., test_a_file_the_desktop_hands_over_early_waits_for_the_window() (+1 more)

### Community 117 - "settings.py"
Cohesion: 0.06
Nodes (29): _along(), ContourDirection, lattice_fineness(), plane_count(), plane_span_deg(), PlaneMode, PlaneTarget, Enum (+21 more)

### Community 118 - "Session"
Cohesion: 0.06
Nodes (36): _coerce(), decode(), encode(), Any, T, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``. (+28 more)

### Community 119 - "AddItem"
Cohesion: 0.07
Nodes (26): Camera motion is deliberately not undoable, AddItem, Command, Append an item to a document list., Delete the item at ``index``, putting it back in place on undo., RemoveItem, Command, History (+18 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.13
Nodes (19): QRectF, Handle, QColor, QFont, QPainter, Convert a 0-1 RGB tuple to a QColor., Draws measurements, tool previews, the orientation gizmo and the readout., Draw everything over the scene. ``occlude`` off skips asking the surface which… (+11 more)

### Community 121 - "project_visible"
Cohesion: 0.14
Nodes (9): project_visible(), project_visible_many(), Project a world point, returning ``None`` when it is behind the camera., Every point of a batch in widget pixels, ``None`` where one is behind the…, An unfilled circle: how thick the form is here, not how big a dot is., A world radius in pixels, measured rather than converted. Projecting the node…, The landmarks of a guided run, and the point about to be placed., A bone as a lozenge: wide near the joint it hangs from, tapering to its end.… (+1 more)

### Community 122 - "ArmatureStore"
Cohesion: 0.18
Nodes (4): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 123 - "SetAttributes"
Cohesion: 0.12
Nodes (10): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, QTreeWidgetItem, Run a row's edit once Qt has finished delivering the current signal. Committing…, Record an edit the viewport's tool worked out., Join two nodes of one armature, if they are two and they are one armature., Commit a renamed or re-checked row, if anything actually changed. (+2 more)

### Community 124 - "_tab_switch"
Cohesion: 0.29
Nodes (7): The show/hide switch on the tab named ``title``, if it has one., Stacked behind another panel is where the switch is worth the most., It is fifteen pixels wide and carries no words, which is exactly the shape the…, _tab_switch(), test_a_panel_that_draws_nothing_gets_no_switch_on_its_tab(), test_a_tabbed_panel_still_shows_its_switch(), test_clicking_the_switch_on_a_tab_works()

### Community 125 - "Reflow"
Cohesion: 0.30
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 126 - "forms.py"
Cohesion: 0.06
Nodes (48): DegenerateHullError, ValueError, The points are flat, collinear or too few to hold any volume., build_freeform(), _centre(), form_landmark_title(), form_spec(), FormFill (+40 more)

### Community 127 - "SectionPanel"
Cohesion: 0.18
Nodes (6): Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 128 - "._upload_sculpt"
Cohesion: 0.15
Nodes (6): Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, Cut the stand-in on a thread; see :meth:`_upload_sculpt`., Show the recording as a task, its bar the stages landed so far., The cross on the recording's card: the film is dropped, the switch too., A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on.

### Community 129 - "._sync_scene"
Cohesion: 0.11
Nodes (8): The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, A skeleton changed: redraw it, and let the skin's body map follow its bones., Tell the renderer what the skin's body map is made from now., Hand the renderer a re-posed model and nothing else. For the frames of a pose…, Regenerate the pedestal and the cut contour when their settings move. Both are…, Rebuild the reference grids for the scene as it stands., The armature the clay is to be built on, if one was chosen. Read here rather…, Cut the mesh with each section plane and expand the result to strokes.

### Community 130 - ".stage_images"
Cohesion: 0.23
Nodes (7): QOpenGLFramebufferObject, QImage, One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A…, An offscreen target the frames are drawn into, made once per export.…, Draw the scene into ``surface`` and read it back as an image., Lay the overlay -- and the caption, if it was asked for -- on a frame. Painted…

### Community 131 - "SurfacePicker"
Cohesion: 0.04
Nodes (54): JointRef, AnnotateMode, AnnotationSettings, Enum, str, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a… (+46 more)

### Community 132 - "ExportLook"
Cohesion: 0.09
Nodes (19): ExportLook, FilmExport, What the frames are to look like, as against what they are of. Laid over the…, ``base`` with this export's choices laid over it., The line burned into the corner of the frame for ``stage``. Counted off the…, One export, rendered from the event loop and encoded behind it. The renderer…, app(), FakeViewport (+11 more)

### Community 133 - "obj_loader.py"
Cohesion: 0.20
Nodes (15): STL and glTF import (1.1.0), _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), ndarray, Minimal, dependency-free Wavefront OBJ reader. Only the geometry statements a… (+7 more)

### Community 134 - "preview"
Cohesion: 0.40
Nodes (5): app(), preview(), fixture, One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "symbol_button"
Cohesion: 0.15
Nodes (13): QTreeWidget, _NameOnlyDelegate, QPushButton, QStyledItemDelegate, QWidget, Allows in-place editing of the name column only., Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list… (+5 more)

### Community 136 - "matcap_panel.py"
Cohesion: 0.23
Nodes (14): available_matcaps(), _bundled_root(), image_path(), matcap_dir(), model_dir(), Path, Locations of the bundled resources. ``REFVIEW_RESOURCES`` overrides the search,…, Return PyInstaller's extracted application directory when frozen. (+6 more)

### Community 137 - "Release"
Cohesion: 0.11
Nodes (19): QRunnable, The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, _CheckTask, is_skipped(), QObject, QWidget (+11 more)

### Community 138 - "load_mesh"
Cohesion: 0.22
Nodes (14): load_mesh(), Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one(), test_binary_stl_welds_shared_corners() (+6 more)

### Community 139 - "OpenRequests"
Cohesion: 0.15
Nodes (8): Application, OpenRequests, Path, QApplication, The Qt application, listening for the desktop's way of handing over a file., Files the desktop asked the viewer to open, kept until there is a window. On…, Open ``path`` in the window, or hold it until there is one., Name the window files go to, and hand over any that came early.

### Community 140 - "_drag_over"
Cohesion: 0.22
Nodes (10): _drag_over(), _middle_of_the_view(), A drag of ``holder`` arriving at ``point`` in the window's coordinates. A real…, The gesture the whole thing rests on: drag it onto the model, it goes., A gesture that destroys something only fires where it clearly meant to., Refused at the door it would never reach the model; so it is let in., test_a_copy_dropped_on_the_model_is_thrown_away(), test_a_copy_is_let_into_the_window_wherever_it_arrives() (+2 more)

### Community 141 - "spatial.py"
Cohesion: 0.19
Nodes (11): _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Box the leaves up, coarsest level first and the leaves themselves last., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the…, Interleave each 10-bit value with two zero bits, ready to be shifted., Build the index from expanded triangle corners, shape ``(T, 3, 3)``., Triangle indices worth intersecting for this ray, possibly empty. (+3 more)

### Community 142 - "palette.py"
Cohesion: 0.17
Nodes (12): css(), outline(), QColor, The colours the hand-drawn elements paint with. Kept apart from…, Draw the hairline that separates a control from the panel. One line, the same…, A colour as a style sheet function, for the parts Qt draws., Change the one colour that is not grey, everywhere at once. The hand-painted…, set_accent() (+4 more)

### Community 143 - "MatcapSettings"
Cohesion: 0.15
Nodes (16): MatcapSettings, Post-processing applied to the sampled matcap texel., _clone_preview(), grade(), _pull_preview(), ndarray, Draw the matcap onto a sphere of ``size`` pixels, graded. Returns ``(size,…, Point the preview at the settings it edits. The object itself, not a copy: this… (+8 more)

### Community 144 - "._picker"
Cohesion: 0.08
Nodes (13): ndarray, Rub out the stroke points under the eraser, live., Take hold of a node, to move it, resize it, or just to select it. This works…, Apply the drag live, so the artist sees the wire bend as they pull it., Take hold of a landmark, to move it or just to say which one it is., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Object centre, which anchors the plane the orbit pivot lies on. (+5 more)

### Community 145 - "._carrying_a_copy"
Cohesion: 0.11
Nodes (10): opens_as(), Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model., Take a copied control out of whichever hand-built panel holds it., Open a file by what it is: a model, a session or a matcap. The one door every…, What a file would open as -- ``"model"``, ``"session"`` or ``"matcap"`` -- by…, Apply a matcap image, reporting unreadable files to the user. (+2 more)

### Community 146 - "euler_to_quat"
Cohesion: 0.16
Nodes (14): Quat, euler_to_quat(), matrix_to_quat(), quat_conjugate(), quat_multiply(), quat_normalize(), quat_to_euler(), A unit quaternion, or the identity for one that has collapsed. (+6 more)

### Community 147 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 148 - "._current_skeleton"
Cohesion: 0.14
Nodes (5): The skeleton the panel is about: the selected row's, else the last., Lay an armature under the selected skeleton as it is posed., Guess the humanoid roles off the joint names; returns how many were found., Take the detail joints out of the current skeleton; returns how many went., Skin the active model to the current skeleton, on a thread, with a bar. Returns…

### Community 149 - "FormStore"
Cohesion: 0.15
Nodes (5): FormStore, An ordered, named collection of forms, like the other stores., The live list; the undo commands operate on it directly., A name for a new form of this recipe, numbered past any it already has. A form…, test_a_form_store_names_forms_past_the_ones_it_has()

### Community 150 - "test_body_regions.py"
Cohesion: 0.29
Nodes (12): _column(), _figure_bones(), ndarray, Where on the body the skin is: bones, height bands, the map, and the settings., A thin column standing from the ground to ``height``., _region(), test_height_bands_follow_the_canon_and_are_soft_at_the_edges(), test_points_go_to_the_region_of_the_nearest_bone_and_blend_between() (+4 more)

### Community 151 - "ContourShadingSettings"
Cohesion: 0.20
Nodes (9): ContourShadingSettings, Parallel slices drawn across the form, the way a contour map reads land. The…, The unit direction the slices are stacked along, in world space., parametrize, The contour shading mode: slices across the form, read off it like a map., test_a_custom_direction_is_normalised_and_an_empty_one_falls_back(), test_the_density_floor_keeps_the_spacing_finite(), test_the_settings_survive_a_session_and_an_older_file_has_them_by_default() (+1 more)

### Community 152 - "Texture2D"
Cohesion: 0.18
Nodes (5): ndarray, An RGBA16F 2D texture with clamped edges and mipmapped minification., Store a ``(depth, height, width, 4)`` float array., Store an ``(h, w, 4)`` float array, reallocating only when resized., Texture2D

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

### Community 158 - "shaders.py"
Cohesion: 0.25
Nodes (6): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section(), Skin BRDF and bounded-depth light transport, shared by preview and refinement.…

### Community 159 - ".paintGL"
Cohesion: 0.29
Nodes (3): Use the same cached visibility test for bones and all point markers., Which part wears the line this frame, and how solid it is, or ``None``. Also…, Hand the renderer the depth grid, or take it away, before a frame.

### Community 160 - "load_obj"
Cohesion: 0.22
Nodes (14): _load_generic(), load_obj(), ObjLoadError, Line-by-line reader for files the fast path declines., Raised when a file cannot be interpreted as an OBJ mesh., Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, test_obj_quads_are_triangulated(), OBJ parsing: normals, triangulation and index handling. (+6 more)

### Community 161 - "ProgressCard"
Cohesion: 0.15
Nodes (7): ProgressCard, QPainter, QWidget, One task: its name, its message, its bar, and a cross to stop it. Painted by…, The cards for the window's tasks, floated over the bottom of the viewport. Told…, TaskBanner, test_a_card_paints_every_state_it_can_be_in()

### Community 162 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 163 - "RegionSource"
Cohesion: 0.18
Nodes (8): _default_profiles(), Enum, str, How much of each kind of mark one region gets, as multipliers of the sliders., Where skin marks tend to fall on a body, as a starting point., Where the region map comes from., RegionProfile, RegionSource

### Community 164 - "Human Skin renderer"
Cohesion: 0.29
Nodes (6): Human Skin renderer, Marks and body regions, Material and transport, Scheduling, precision and compatibility, Surface, Where to change it

### Community 165 - "SectionGizmo"
Cohesion: 0.31
Nodes (4): Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo

### Community 166 - ".from_dict"
Cohesion: 0.20
Nodes (6): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., _distance_or_none(), A clipping distance as a file wrote it, or ``None`` for one left to the fit., test_clip_planes_set_by_hand_override_the_fit_within_reason(), test_serialisation_round_trip()

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
Cohesion: 0.29
Nodes (6): Holds the working state between one turn of the sliders and the next.…, The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache, test_the_cache_re_cuts_the_form_when_the_wire_moves(), test_the_cache_stands_aside_unless_the_geometry_target_asked_for_it()

### Community 173 - "mesh_io.py"
Cohesion: 0.15
Nodes (17): Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets (+9 more)

### Community 175 - "TestEven"
Cohesion: 0.32
Nodes (4): even(), ``value`` rounded down to a multiple of four. Two would do for H.264, which…, What the frames are to look like, as the controls have it., TestEven

### Community 176 - "raycast_mesh"
Cohesion: 0.17
Nodes (18): _cross(), intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Row-wise cross product, without :func:`numpy.cross`'s axis shuffling., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``., The closest hit along each of a batch of rays, ``None`` where one misses. One… (+10 more)

### Community 177 - "quat_from_axis_angle"
Cohesion: 0.47
Nodes (6): quat_from_axis_angle(), A ribbon along +X with two joints, the far half held by the second., _skinned_strip(), test_a_session_saved_beside_a_rigged_model_keeps_the_pose(), test_posing_the_bound_skeleton_re_skins_the_model_and_undo_puts_it_back(), test_turning_the_model_carries_the_skeleton_and_the_skin_with_it()

### Community 178 - "._add_skeleton"
Cohesion: 0.22
Nodes (4): Add an empty skeleton, for a chain to be clicked into., Stand a proportioned humanoid skeleton in the model's box., Grow a skeleton out of the armature chosen in the box., Record a structural edit the viewport's tool worked out.

### Community 179 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 180 - "._commit_node_drag"
Cohesion: 0.33
Nodes (3): Record the finished gesture: a move, a resize, or a plain click. A press that…, Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…

### Community 181 - "FormRun"
Cohesion: 0.40
Nodes (3): FormRun, Begin a run against a form already in the store., A guided form part-way through.

### Community 186 - "ModelPanel"
Cohesion: 0.13
Nodes (5): ModelPanel, Reflect the tool state without re-emitting the toggle., Choose the gesture, from the menu or a key., Bake the active object's turn and scale into its mesh., Lists the objects, places the active one, and reports what came out of its file.

### Community 187 - "PreferenceStore"
Cohesion: 0.14
Nodes (11): PreferenceStore, QObject, QSettings, _qcolor(), Push the preferences that something in the process holds a copy of.…, A core colour triple as the Qt colour the palette wants., The preferences, and one signal saying they have changed. A single instance,…, Adopt ``value``, push what has to be pushed, and say so. Always announces, even… (+3 more)

### Community 188 - "._offer_humanoid_mapping"
Cohesion: 0.50
Nodes (3): looks_humanoid(), Whether a guessed mapping is enough of a figure to be worth offering., Ask whether a rig that arrived with the model should be read as a figure. Only…

### Community 189 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 190 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 191 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 192 - "quad"
Cohesion: 0.67
Nodes (3): fixture, quad(), Two triangles covering the unit square on the z = 0 plane.

### Community 195 - "._menu_action"
Cohesion: 0.40
Nodes (4): _plain(), QAction, A menu entry's text as a name: no accelerator ampersand, no trailing dots., Add a menu entry, optionally with a window-wide shortcut. Given a ``command``…

### Community 206 - "_file_drag"
Cohesion: 0.17
Nodes (12): QMimeData, _drop_on(), The end of the gesture: the payload a drag carries, delivered., Drop ``mime`` on the top-left of ``panel``; was it taken? The caller keeps hold…, test_a_drop_carrying_a_control_takes_a_copy_of_it(), test_a_drop_carrying_something_else_is_refused(), test_a_drop_naming_a_control_that_is_gone_is_refused(), _file_drag() (+4 more)

### Community 207 - "Hit"
Cohesion: 0.16
Nodes (11): Hit, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., snap_to_vertex(), ndarray, Closest surface intersection under the cursor, or ``None``., Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-… (+3 more)

### Community 208 - "PanelDock"
Cohesion: 0.13
Nodes (9): QDockWidget, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top., _number_in(), QWidget, Dress the tabs once Qt has finished rearranging them., An empty panel of the artist's own, docked on the right. A dock put away…, Take a parked dock back out under ``key``, emptied and renamed. (+1 more)

### Community 210 - "tasks.py"
Cohesion: 0.12
Nodes (15): Exception, QIcon, CancelledError, Raised inside the work when it has been told to stop., _draw_glyph(), glyph(), QColor, QPixmap (+7 more)

### Community 215 - "._build"
Cohesion: 0.33
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

## Knowledge Gaps
- **6 isolated node(s):** `refview`, `Surface`, `Marks and body regions`, `Material and transport`, `Scheduling, precision and compatibility` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `SurfacePicker`, `SceneObject`, `Bounds`, `obj_loader.py`, `ExportLook`, `load_mesh`, `SceneRenderer`, `main_window.py`, `MeshBuffers`, `.apply_session`, `Skeleton`, `FormStore`, `test_body_regions.py`, `SkeletonStore`, `SectionSettings`, `plane_volume.py`, `test_spatial.py`, `auto_skin`, `load_obj`, `PlaneSettings`, `test_plane_clusters.py`, `RegionSource`, `convex.py`, `autoskin.py`, `TriangleIndex`, `gltf_loader.py`, `mesh_io.py`, `SculptCache`, `TestEven`, `raycast_mesh`, `body_regions.py`, `quat_from_axis_angle`, `SkinSettings`, `test_skeleton.py`, `Solid`, `quad`, `PrimaryForm`, `test_objects.py`, `test_skin.py`, `test_plane_solids.py`, `Path`, `mesh_renderer.py`, `ViewerState`, `Hit`, `Joint`, `plane_solids.py`, `build_form`, `compute_vertex_normals`, `OrientationSettings`, `Path`, `test_tasks.py`, `._oriented`, `scene.py`, `forms.py`?**
  _High betweenness centrality (0.191) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `._upload_sculpt`, `._sync_scene`, `.stage_images`, `SurfacePicker`, `ExportLook`, `test_preferences.py`, `MainWindow`, `main_window.py`, `._picker`, `PoseTool`, `.paintGL`, `PlaneSettings`, `SectionGizmo`, `film_export.py`, `sample_count`, `ExportVideoDialog`, `._active_changed`, `._commit_node_drag`, `MeasureTool`, `PrimaryForm`, `test_objects.py`, `._place_joint`, `ObjectTool`, `._place_form_landmark`, `ArmatureTool`, `ViewerState`, `NavigationController`, `build_form`, `.mouseReleaseEvent`, `._place_armature_node`, `ViewportOverlay`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `SceneRenderer` connect `SceneRenderer` to `MeasureTool`, `Stroke`, `mesh_renderer.py`, `main_window.py`, `MeshBuffers`, `mesh_io.py`, `body_regions.py`, `_Target`, `Mesh`, `ShaderProgram`, `Texture2D`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `Mesh` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Mesh` has 58 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `OverlayParts`) actually correct?**
  _`ViewerState` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Skeleton` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Skeleton` has 9 INFERRED edges - model-reasoned connections that need verification._