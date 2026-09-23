# Graph Report - reference-viewer  (2026-09-23)

## Corpus Check
- 171 files · ~533,866 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5960 nodes · 14019 edges · 198 communities (194 shown, 4 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 729 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `06ffb3e1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SettingsWindow
- test_preferences.py
- update_check.py
- Viewport
- SceneObject
- _derived
- MainWindow
- Stroke
- GifWriter
- linalg.py
- SceneRenderer
- elements/__init__.py
- orientation.py
- MeshBuffers
- Armature
- environment.yml
- .apply_session
- Skeleton
- mesh_renderer.py
- CameraPanel
- PosePanel
- ShaderProgram
- PoseTool
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- VideoError
- core/__init__.py
- plane_volume.py
- ControlsWindow
- auto_skin
- ShadingPanel
- FilmRecorder
- test_camera.py
- test_plane_clusters.py
- WakeLock
- test_forms.py
- ._built
- Frame
- film_export.py
- convex.py
- Camera
- skeleton.py
- ValueSlider
- gltf_loader.py
- ExportVideoDialog
- ArmatureNode
- landmarks.py
- Agent Graph-First Instructions
- body_regions.py
- plane_clusters.py
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
- HotkeyStore
- form_shapes.py
- application.py
- test_session.py
- Link
- PrimaryForm
- ShadingMode
- test_objects.py
- test_skin.py
- test_plane_solids.py
- ObjectTool
- MatcapSettings
- ArmatureSettings
- load_obj
- load_matcap_pixels
- test_custom_panels.py
- .__init__
- core/preferences.py
- core/environment.py
- NavigationController
- ._apply
- ViewerState
- test_forms_panel.py
- PlaneSettings
- viewport.py
- build_form
- MatcapPanel
- AnnotatePanel
- FrameBar
- main_window.py
- OpenRequests
- test_elements.py
- Mesh
- MeasurementStore
- ReflowLayout
- state.py
- ColorButton
- FormStore
- clone.py
- skin_detail.py
- Path
- _accessor
- SetAttributes
- ._delete_selected
- MarkerVisibility
- plane_solids.py
- test_tasks.py
- .bone_at
- DockTitle
- test_reflow.py
- ._oriented
- Task
- test_history.py
- Solid
- test_open_files.py
- History
- Session
- AddItem
- ViewportOverlay
- test_hotkeys.py
- armature.py
- test_navigation.py
- .refresh_list
- Reflow
- forms.py
- SectionPanel
- ._upload_sculpt
- ._sync_scene
- Stage
- AnnotateTool
- ExportLook
- obj_loader.py
- preview
- _NameOnlyDelegate
- paths.py
- Release
- load_mesh
- Command
- ._advance_pending
- spatial.py
- theme.py
- MatcapPreview
- ._picker
- ._carrying_a_copy
- form_group
- app
- grid.py
- SurfacePicker
- test_body_regions.py
- test_contour_shading.py
- DataTexture
- Buried
- ._focused_form
- .install
- test_spatial.py
- GuideRun
- shader_files.py
- .paintGL
- outline
- .pan
- .column_of
- panel
- Human Skin renderer
- SectionGizmo
- test_skin_gl.py
- coarse_lattice
- .mouseMoveEvent
- sample_count
- _height_of
- TriangleIndex
- README.md
- ._active_changed
- raycast_mesh
- app
- VideoSettings
- HotkeyBinder
- ModelPanel
- settings_window.py
- MeasureTool
- release.yml
- quad
- KeyBox
- .__init__
- ._build_menus
- ask_for
- ._place_joint
- ._place_form_landmark
- decode
- CHANGELOG.md
- _Encoder
- Hit
- .skin_object
- ndarray
- UpdateChecker
- ui/hotkeys.py
- PlacedLandmark

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 244 edges
2. `ViewerState` - 186 edges
3. `Viewport` - 163 edges
4. `Skeleton` - 114 edges
5. `Camera` - 102 edges
6. `MainWindow` - 95 edges
7. `SceneObject` - 83 edges
8. `Armature` - 81 edges
9. `PrimaryForm` - 79 edges
10. `SceneRenderer` - 71 edges

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

## Communities (198 total, 4 thin omitted)

### Community 0 - "SettingsWindow"
Cohesion: 0.15
Nodes (11): The preferences as they stand. Treat as read-only; use :meth:`set`., QWidget, Fill in the groups. A switch with nothing to put in the caption column is given…, Every command with its keys, each key a box that takes one keystroke. The list…, The one button that is not a preference, and what the window is for., Say what the view is really drawing with, beside what was asked for. A sample…, Put one field back into the store, which applies and saves it., Pull every control back into line with the store. Run when the window is built,… (+3 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.06
Nodes (46): _clamp(), Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, Pull anything out of range back into it. The window cannot produce these…, Read the preferences off the machine. Never raises., app(), model() (+38 more)

### Community 2 - "update_check.py"
Cohesion: 0.10
Nodes (31): check_for_update(), fetch_latest_release(), is_newer(), _macos_root_certificates(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and… (+23 more)

### Community 3 - "Viewport"
Cohesion: 0.06
Nodes (16): QOpenGLWidget, Arm one tool, disarming the rest. Only one gesture can own the left button, so…, Drop whatever gesture is half-finished, without disarming the tool., One of the renderer's :data:`~refview.render.mesh_renderer.ANTIALIASING_MODES`., Renders the scene and turns mouse gestures into camera and tool actions., Slide the view so a point sits at the centre, keeping the angle., The gesture a key press chooses, if the transform tool is armed to hear it., A form changed: work its clay out again and redraw. (+8 more)

### Community 4 - "SceneObject"
Cohesion: 0.07
Nodes (20): ObjectSettings, ObjectStore, ndarray, Snapshot, What a parent's state means for its children, and how the tools scale. Each is…, One model in the scene. Three meshes are kept, as the viewer kept them when…, The centred mesh carried by ``matrix`` -- the mesh itself for the identity., Drop the derived meshes, after the rest mesh has been replaced. (+12 more)

### Community 5 - "_derived"
Cohesion: 0.08
Nodes (29): _kept_laying(), Fresh bones, laid the way the armature was already laying them. The bone list…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _derived(), A guess the artist corrects is theirs, and the mirror leaves it alone., The new list is the edit; the old one has to survive to be undone to., Mirroring moves a guess in place, which must not reach the undo history. (+21 more)

### Community 6 - "MainWindow"
Cohesion: 0.06
Nodes (14): MainWindow, QMainWindow, Put every panel button and menu entry where the tools now stand. Only one tool…, Swap between the eraser and the drawing mode it was called from., Open an empty panel of the artist's own and bring it to the front., Put the panels back where they started, now., Follow the machine's sleep to whether this window is in front., Keep the banner over the view as the docks push the view about. (+6 more)

### Community 7 - "Stroke"
Cohesion: 0.06
Nodes (38): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+30 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "linalg.py"
Cohesion: 0.08
Nodes (41): Quat, Interactive camera model driving both perspective and orthographic views., compose(), euler_to_quat(), look_at(), matrix_to_quat(), normalize(), orthographic() (+33 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.06
Nodes (48): A turn about the vertical axis, as a 3x3 matrix., rotation_y(), Unit vector for an azimuth/elevation pair, with +Y as the pole., spherical_direction(), Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, background_basis() (+40 more)

### Community 11 - "elements/__init__.py"
Cohesion: 0.05
Nodes (51): make_switch(), QCheckBox, One dock per panel, with a bar of its own across the top. Every panel is its…, Put a show/hide switch at the left of the bar and return it., A square that is on or off, and is clickable all over. A check box decides…, The square that shows or hides what a panel draws. One is kept on each dock's…, Switch, A titled frame that folds away behind its own bar. Every group of controls in… (+43 more)

### Community 12 - "orientation.py"
Cohesion: 0.33
Nodes (5): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis

### Community 13 - "MeshBuffers"
Cohesion: 0.10
Nodes (9): MeshBuffers, Vertex/index buffers for one mesh, bound through a single VAO., Forget the contents without releasing the buffer objects., Replace the model: the whole scene as one mesh, and the objects it is made of.…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are…, Every buffer standing for the model, for the passes that draw them all alike. (+1 more)

### Community 14 - "Armature"
Cohesion: 0.05
Nodes (41): Armature, Bone, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves., A plausible thickness for a node placed by hand., What to call a bone: its own name, or the two nodes it runs between. (+33 more)

### Community 15 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 16 - ".apply_session"
Cohesion: 0.09
Nodes (11): Turn every object the same way; see :meth:`set_object_orientation`. For files…, Turn one object, bringing the marks made on it along. Measurements,…, Take the display unit from the file when the format declares one. Only glTF…, Set the active matcap, or fall back to the built-in one., Have the HDRI at ``path`` read off the thread, and light with it when it lands.…, Light with a map already read -- or with none., Read the HDRI the settings name, if they light with one that is not here yet.…, Fit the scene in the view without changing the direction. (+3 more)

### Community 17 - "Skeleton"
Cohesion: 0.05
Nodes (31): Joint, _matrix16(), _pose_matrices(), ndarray, Whether the pose differs from the rest at all., A copy with the rest translation replaced and the frame kept., A tree -- or a forest -- of joints and the pose they stand in., Every joint, parents before children. A file may list a child before its… (+23 more)

### Community 18 - "mesh_renderer.py"
Cohesion: 0.05
Nodes (33): AccumTarget, bind_default(), ColorTarget, current_framebuffer(), DepthTarget, FrameTarget, GeometryTarget, Offscreen render targets used by the high-quality, ghost and smoothing passes.… (+25 more)

### Community 19 - "CameraPanel"
Cohesion: 0.11
Nodes (9): CameraPanel, QListWidgetItem, Take the planes in hand where the fit left them, or hand them back., Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions. (+1 more)

### Community 20 - "PosePanel"
Cohesion: 0.05
Nodes (23): Quat4, normalized_rotation(), A pose rotation as the plain tuple a joint stores., PosePanel, QTreeWidgetItem, The skeleton the panel is about: the selected row's, else the last., Highlight a row, in the tree and in the view., Highlight the row for a joint picked in the view. (+15 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): Fill the shader's table with a level, if it is not already in it., ndarray, RuntimeError, Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "PoseTool"
Cohesion: 0.06
Nodes (44): JointRef, How skeletons are drawn, and how the pose tool behaves., SkeletonSettings, PoseTool, ndarray, The nearest unlocked joint of a visible skeleton under the cursor., The bone under the cursor, named by the joint at its far end. Taking hold of a…, The turn the parent takes so that joint ``index`` points at ``target``. The… (+36 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.07
Nodes (25): app(), _names(), panel(), fixture, The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as… (+17 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.10
Nodes (11): MeasurePanel, _NameOnlyDelegate, QStyledItemDelegate, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing… (+3 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.10
Nodes (10): BookmarkStore, CameraBookmark, Named camera positions the artist can jump between while sculpting., A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one. (+2 more)

### Community 26 - "VideoError"
Cohesion: 0.11
Nodes (14): _FFmpegWriter, ndarray, Path, RuntimeError, An export that could not be written, said in words for the artist., What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``. (+6 more)

### Community 27 - "core/__init__.py"
Cohesion: 0.03
Nodes (85): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, GridSettings, Which planes carry a grid, how fine it is, and how it fades., Qt-free geometry, camera and document model for the reference viewer., Bounds, An axis-aligned bounding box. (+77 more)

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
Cohesion: 0.09
Nodes (14): Chooses the shading model and edits its light and surface parameters., Pick an HDRI from disk and light with it., List the bundled HDRIs, and the one in use if it is from elsewhere., Put the light's numbers back in line with the settings, after a drag or an undo., Freeze the slices the way the camera faces now. The view direction is the one…, Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel, A matcap has no light to aim, so the Light group goes -- and its space. The… (+6 more)

### Community 32 - "FilmRecorder"
Cohesion: 0.06
Nodes (37): QThread, Film, A whole making, from the coarsest stage to the one the slider asks for. Held by…, FilmRecorder, QObject, Recording a form's making in the background, so the app stays usable. A film is…, The film being recorded, or the last one finished., Whether a film is being made right now. (+29 more)

### Community 33 - "test_camera.py"
Cohesion: 0.08
Nodes (15): _distance_or_none(), Projection, Enum, str, Projection used by :class:`Camera`., A clipping distance as a file wrote it, or ``None`` for one left to the fit., camera(), fixture (+7 more)

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (59): The joint list with ``index`` resting at ``target`` and its children left be., angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad() (+51 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (32): c_void_p, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., Holds sleep off while the window that owns it is the one in front. The class… (+24 more)

### Community 36 - "test_forms.py"
Cohesion: 0.10
Nodes (32): build_ribcage(), The egg of the ribcage, with the arch chipped out of the front of it. Three…, _closed(), _inside(), _marks(), ndarray, The forms: convex solids, the landmarks that build them, the walk, and the…, Every edge shared by exactly two faces: the hull is a closed surface. (+24 more)

### Community 37 - "._built"
Cohesion: 0.13
Nodes (8): QMenu, Path, QImage, QRect, Offer the picture back as a file: as graded here, or as it came. A grading…, The matcap as a picture, at its own resolution. Square and opaque, with the…, Where the sphere goes: square, centred, above the legend., The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…

### Community 38 - "Frame"
Cohesion: 0.07
Nodes (25): carried(), _push_frame(), Nothing: each row inside the copy is linked on its own., Read a drag's payload back, or ``None`` if it is not one of ours., CustomPanel, _detach(), QFormLayout, QWidget (+17 more)

### Community 39 - "film_export.py"
Cohesion: 0.08
Nodes (26): _encode_arguments(), _encoders(), ffmpeg_path(), _no_window(), Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a… (+18 more)

### Community 40 - "convex.py"
Cohesion: 0.12
Nodes (24): convex_hull(), DegenerateHullError, flat_mesh(), _outward(), _patch_samples(), ndarray, ValueError, Convex solids from points: the hull, a cut through it, and its mesh. A primary… (+16 more)

### Community 41 - "Camera"
Cohesion: 0.08
Nodes (19): Camera, ndarray, Near/far planes fitted to the scene bounding sphere., The near and far planes this frame: the fitted ones, unless set by hand. A…, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Rays through a batch of pixels, as ``(origins, unit directions)``, ``(N, 3)``…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Project ``(N, 3)`` world points to ``(xs, ys, ndc_depths)`` in widget pixels. (+11 more)

### Community 42 - "skeleton.py"
Cohesion: 0.07
Nodes (39): AutoSkin, AutoSkinError, _baked_rest(), _conjugate_gradients(), _CotLaplacian, _envelope_weights(), _Graph, _heat_weights() (+31 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (13): _clone_slider(), _pull_slider(), _push_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end. (+5 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.15
Nodes (21): STL and glTF import (1.1.0), Units are adopted, never guessed, _buffers(), _first_skin(), GltfLoadError, load_gltf(), _primitives(), Path (+13 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.11
Nodes (11): even(), ExportVideoDialog, Path, QDialog, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the…, What the frames are to look like, as the controls have it., How long it runs and what it is written as. (+3 more)

### Community 46 - "ArmatureNode"
Cohesion: 0.10
Nodes (22): ArmatureNode, One joint of the wire: where it is, and how thick the form is there., Preset, An ordered set of landmarks and the armature they build., The midline landmarks, which are what the median plane is fitted to., _chain(), A straight run of nodes one unit apart along +X., Nothing stands between one neighbour, so there is nothing to bridge. (+14 more)

### Community 47 - "landmarks.py"
Cohesion: 0.13
Nodes (24): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), median_plane(), _mid(), mirror_point() (+16 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "body_regions.py"
Cohesion: 0.15
Nodes (20): band_weights(), BodySource, bone_weights(), build_body_map(), looks_like_a_figure(), ndarray, Where on the body a point of the skin is, so that the skin can be marked as…, Whether the bones say enough about a body to place its skin by. (+12 more)

### Community 50 - "plane_clusters.py"
Cohesion: 0.04
Nodes (80): _empty(), plane_axes(), PlaneAxes, PlaneSet, ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, One level of a fit: the planes the shader is to quantise against. A plane is a…, A level with no place in it: nearest direction wins, as before. (+72 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.09
Nodes (36): QPoint, _drag(), _listed(), _matcap_file(), parametrize, The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc. (+28 more)

### Community 52 - "test_armature.py"
Cohesion: 0.13
Nodes (35): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., The femoral head is in from the ASIS, below it and behind it, by shares of the…, A wire in two halves is not an armature anybody could bend., Version 4 files predate the armature; they open with an empty one. (+27 more)

### Community 53 - "ArmaturePanel"
Cohesion: 0.04
Nodes (35): QTreeWidget, ArmaturePanel, QPushButton, QTreeWidgetItem, QWidget, Run a row's edit once Qt has finished delivering the current signal. Committing…, Arms the armature tool, lists its nodes and runs the guided presets., Add a group below the list rather than to the panel root. (+27 more)

### Community 54 - "BodyRegionSettings"
Cohesion: 0.10
Nodes (14): BodyRegionSettings, _default_profiles(), Enum, str, How much of each skin effect one region gets, relative to its slider., Starting values for skin effects across a generic body., Where the regions come from, and what each does to the skin effects., One region's multiplier for ``effect`` after another, in :data:`REGIONS` order. (+6 more)

### Community 55 - "HotkeyMap"
Cohesion: 0.08
Nodes (18): Command, HotkeyMap, Any, Which keys do what, as the artist has decided rather than as it ships. A hotkey…, Whether the artist has moved this command off what it ships with., Which command has these keys, if any., Every command with keys on it, declared or not, as id -> keys., Put ``keys`` on a command, taking them off whatever had them. Returns the id of… (+10 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (11): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+3 more)

### Community 57 - "FormsPanel"
Cohesion: 0.09
Nodes (11): FormsPanel, Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take back the landmark before this one and ask for it again., Ready the landmark the next click lays down, from the name and side boxes., The multiplier the position boxes are read and written through., Keep the ghost switch agreeing with the Shading panel's. (+3 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.08
Nodes (22): PlanesPanel, QListWidgetItem, Lay one length of wire earlier or later, as one undoable step., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Show what this way of working needs, and put the rest away. A setting that does… (+14 more)

### Community 59 - "test_skeleton.py"
Cohesion: 0.06
Nodes (58): quat_from_axis_angle(), build_humanoid_skeleton(), detail_joints(), humanoid_positions(), humanoid_roles(), ndarray, Every humanoid role's place for a figure this tall standing on ``feet``., A proportioned humanoid skeleton, roles and all, standing on ``feet``. (+50 more)

### Community 60 - "Progress"
Cohesion: 0.08
Nodes (21): Exception, CancelledError, Progress, What a long piece of work says about itself while it runs, and how it is…, Ask the work to stop at its next report., How far along, 0 to 1, or ``None`` when the work has not said., Whether the work has said how much there is to do., A window onto part of a parent's range; see :meth:`Progress.slice`. (+13 more)

### Community 61 - "Workspace"
Cohesion: 0.06
Nodes (25): QTabBar, _number_in(), QMainWindow, QObject, QSettings, QWidget, Keep every switch agreeing with the panel it speaks for., Hang a show/hide switch on every dock tab that wants one. A dock stacked behind… (+17 more)

### Community 62 - "HotkeyStore"
Cohesion: 0.19
Nodes (8): HotkeyStore, QSettings, Put ``keys`` on a command; says what they came off, if anything., Read the choices off the machine. Never raises., The one store, loading it off the machine the first time it is asked., The map, and one signal saying it has changed., The map as it stands. Treat as read-only; change it through the store., store()

### Community 63 - "form_shapes.py"
Cohesion: 0.09
Nodes (41): _across(), blend_rings(), build_head(), build_pelvis(), fit_plane(), _head_frame(), _HeadFrame, _lagrange() (+33 more)

### Community 64 - "application.py"
Cohesion: 0.12
Nodes (20): ArgumentParser, Namespace, QSplashScreen, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font(), main() (+12 more)

### Community 65 - "test_session.py"
Cohesion: 0.09
Nodes (20): Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., A step of the slider is worth a fixed share more planes, not a fixed number of…, The ceiling went from 64 planes to 256 without moving the slider under anyone:…, The panel edits the settings; the fit has to be told what they are., Both modes answer in degrees of turn, so the panel can just ask., Version 1 files predate the annotation layer and the endpoint lock., Version 6 files predate panels being something a session could carry. (+12 more)

### Community 66 - "Link"
Cohesion: 0.12
Nodes (9): CloneGesture, Link, _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original., Whether the copy is being used right now and must not be written. (+1 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.05
Nodes (46): FormLandmarkRef, form_spec(), FormSettings, median_plane_ready(), mirror_form_landmarks(), PrimaryForm, The midline landmarks, which are what the median plane is fitted to., One form in the document: which recipe, and where its landmarks are. The solids… (+38 more)

### Community 68 - "ShadingMode"
Cohesion: 0.17
Nodes (4): Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode, TestEven

### Community 69 - "test_objects.py"
Cohesion: 0.11
Nodes (35): Write a mesh out; only OBJ is written, whatever the suffix asked for., save_mesh(), Path, Where an object stands relative to its parent: an affine placement. Held as the…, Transform, app(), _key(), _mouse() (+27 more)

### Community 70 - "test_skin.py"
Cohesion: 0.08
Nodes (31): What of the settings a refined skin image can show, as a key. The refinement…, traced_settings_key(), _area(), build_bvh(), build_scene(), ndarray, Bounding-volume hierarchy tables for the OpenGL 3.3 skin tracer. The tree is…, Build on a worker from the immutable meshes currently drawn by the renderer. (+23 more)

### Community 71 - "test_plane_solids.py"
Cohesion: 0.03
Nodes (148): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), film_of(), parametrize, Scrubbing through the making of a form, rather than only arriving at it. The…, A cut takes material away, so no stage of a carving is larger than the one… (+140 more)

### Community 72 - "ObjectTool"
Cohesion: 0.12
Nodes (14): _axis_param(), Gizmo, _Grip, ObjectTool, ndarray, The three directions the arms run along, in world space. A move and a turn are…, Where the gizmo for an object at ``world`` falls on screen, or ``None`` if…, Which handle a screen point is over: ``"centre"``, ``"x"``, ``"y"``, ``"z"`` or… (+6 more)

### Community 73 - "MatcapSettings"
Cohesion: 0.15
Nodes (16): MatcapSettings, Post-processing applied to the sampled matcap texel., _clone_preview(), grade(), _pull_preview(), ndarray, Draw the matcap onto a sphere of ``size`` pixels, graded. Returns ``(size,…, Point the preview at the settings it edits. The object itself, not a copy: this… (+8 more)

### Community 74 - "ArmatureSettings"
Cohesion: 0.11
Nodes (24): ArmatureSettings, How the armature is drawn, and how new nodes are placed., The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now., How many landmarks are placed, out of how many will be asked for., Pass over the landmark being asked for; the figure loses what it fed., Un-skip or un-place the landmark before this one, and ask again. Returns the…, _at() (+16 more)

### Community 75 - "load_obj"
Cohesion: 0.22
Nodes (14): load_obj(), ObjLoadError, Path, Raised when a file cannot be interpreted as an OBJ mesh., Write ``mesh`` as a plain OBJ: positions, normals and triangles. What a session…, Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, save_obj(), OBJ parsing: normals, triangulation and index handling. (+6 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.13
Nodes (26): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+18 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.07
Nodes (23): QMimeData, app(), custom(), _drop_on(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error., A group is not a row, so it goes ahead of the group it was dropped on. (+15 more)

### Community 78 - ".__init__"
Cohesion: 0.08
Nodes (12): BakeEdit, Command, QObject, Write ``obj``'s turn and scale into its mesh, leaving it standing as it is.…, Dressing an object in a skin made for a skeleton, or taking it off. One step…, An object's rest mesh as a file stores it, so that reading it back comes to…, Writing an object's turn and scale into its mesh -- Reset XForm -- or undoing…, Emit the change signal a command's channel maps onto. (+4 more)

### Community 79 - "core/preferences.py"
Cohesion: 0.12
Nodes (18): _as_kind_of(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any, What the artist prefers, as distinct from what the document says. There are two… (+10 more)

### Community 80 - "core/environment.py"
Cohesion: 0.06
Nodes (65): direction_to_uv(), dominant_light(), downsized(), EnvironmentLoadError, EnvironmentMap, evaluate_sh(), _exr_rgb(), _halve() (+57 more)

### Community 81 - "NavigationController"
Cohesion: 0.08
Nodes (16): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Degrees of yaw per pixel, signed by whether the drag is inverted. (+8 more)

### Community 82 - "._apply"
Cohesion: 0.19
Nodes (6): Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Slot that writes one field of the contour shading settings., Slot that writes one field of the grid settings.

### Community 83 - "ViewerState"
Cohesion: 0.07
Nodes (28): ObjectsEdit, Snapshot, A copy of ``obj``'s mesh on top of it, made active, as one undo step., Scale ``objects`` so each is the size of the active one, as one undo step. The…, The largest of ``obj``'s three extents as it stands in the world., A parenting policy changed: what is shown and how solid may have too., Everything the viewer displays, plus change notifications., The skeleton bound to ``obj``'s rig, if one is and no other object has it. (+20 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.14
Nodes (26): _click(), _pending(), _pick(), _place_all(), The Forms panel: the guided run it drives, and the document it writes. The…, A form row hands the whole form to update_enabled, whose landmark list must be…, Type a name for the next landmark and, if given, pick its side., What the viewport does when a freeform run gets a click. (+18 more)

### Community 85 - "PlaneSettings"
Cohesion: 0.05
Nodes (37): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, Holds the working state between one turn of the sliders and the next.…, The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache, _along(), lattice_fineness() (+29 more)

### Community 86 - "viewport.py"
Cohesion: 0.06
Nodes (34): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, What the annotate tool does with a drag. The first three describe the shape a…, Measurement, MeasurementSettings, ndarray (+26 more)

### Community 87 - "build_form"
Cohesion: 0.10
Nodes (31): merged(), Several flat meshes as one, or ``None`` when there is nothing to draw., build_form(), built_count(), form_landmark_title(), form_mesh(), landmark_signature(), ndarray (+23 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.10
Nodes (21): added_matcaps(), forget_matcap(), MatcapPanel, Path, QIcon, The matcaps added from outside the folder that are still on disk, newest first.…, Keep ``path`` in the gallery from now on., Take ``path`` out of the gallery; the file itself is left alone. (+13 more)

### Community 89 - "AnnotatePanel"
Cohesion: 0.19
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 90 - "FrameBar"
Cohesion: 0.09
Nodes (13): FrameBar, framed(), QFormLayout, QPainter, QSize, QWidget, The mark beside a group's name: filled when open, a ring when shut. It is the…, The rows inside the frame. ``layout()`` is the frame's own, which stacks the… (+5 more)

### Community 91 - "main_window.py"
Cohesion: 0.05
Nodes (57): QScrollArea, The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, _draw_glyph(), glyph(), lock_icon(), QColor, QIcon (+49 more)

### Community 92 - "OpenRequests"
Cohesion: 0.15
Nodes (8): Application, OpenRequests, Path, QApplication, The Qt application, listening for the desktop's way of handing over a file., Files the desktop asked the viewer to open, kept until there is a window. On…, Open ``path`` in the window, or hold it until there is one., Name the window files go to, and hand over any that came early.

### Community 93 - "test_elements.py"
Cohesion: 0.09
Nodes (19): app(), fixture, Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., Run the refresh the shared timer would have run. (+11 more)

### Community 94 - "Mesh"
Cohesion: 0.04
Nodes (73): auto_smooth(), _corner_groups(), _face_cross(), _gathered(), _group_normals(), One entry point for every mesh format the viewer reads. Callers ask for a path…, loose_parts(), Mesh (+65 more)

### Community 95 - "MeasurementStore"
Cohesion: 0.16
Nodes (5): MeasurementStore, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., An ordered, named collection of measurements. Deliberately plain: the Qt layer…, test_store_auto_names_new_measurements()

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - "state.py"
Cohesion: 0.06
Nodes (42): concatenated(), Several meshes as one, in the coordinates they already stand in. The units are…, OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., _bare(), duplicate_object(), merge_objects() (+34 more)

### Community 98 - "ColorButton"
Cohesion: 0.11
Nodes (12): _clone_swatch(), _pull_swatch(), _push_swatch(), _AxisBox, ColorButton, QColor, QDoubleSpinBox, QSize (+4 more)

### Community 99 - "FormStore"
Cohesion: 0.15
Nodes (5): FormStore, An ordered, named collection of forms, like the other stores., The live list; the undo commands operate on it directly., A name for a new form of this recipe, numbered past any it already has. A form…, test_a_form_store_names_forms_past_the_ones_it_has()

### Community 100 - "clone.py"
Cohesion: 0.04
Nodes (75): QAbstractButton, QLineEdit, QSlider, QSpinBox, _begin(), can_clone(), clone(), _clone_button() (+67 more)

### Community 101 - "skin_detail.py"
Cohesion: 0.17
Nodes (20): burley_marginal(), burley_profile(), cellular(), diffusion_lut(), _fade(), fbm(), ndarray, Procedural skin micro-relief and the pre-integrated diffusion table. Reference… (+12 more)

### Community 102 - "Path"
Cohesion: 0.12
Nodes (13): looks_humanoid(), Whether a guessed mapping is enough of a figure to be worth offering., Path, Pick up whatever was last being worked on, if that was asked for. A session…, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window. In the…, Read a model file off the window, then hand it to ``adopt`` here. (+5 more)

### Community 103 - "_accessor"
Cohesion: 0.21
Nodes (13): _accessor(), _local_transform(), _primitive_geometry(), _primitive_skin(), ndarray, _quaternion_matrix(), Read one accessor into an ``(n, components)`` array., A node's own transform, from either a matrix or a TRS triple. (+5 more)

### Community 104 - "SetAttributes"
Cohesion: 0.08
Nodes (13): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Record an edit the viewport's tool worked out., Record the finished drag as a single undo step., Record the turn as one undo step., Alt forces the camera gesture, whichever tool is armed., Record the finished gesture: a move, a resize, or a plain click. A press that…, Record the finished drag as one step, or read a press as a selection. (+5 more)

### Community 105 - "._delete_selected"
Cohesion: 0.19
Nodes (5): The freeform the highlighted row belongs to, when no run is on., Record an edited landmark list, mirrored where the mirror is on., Remove the selected landmark, or the whole form when its row is picked., The form the selected row stands for, when the row is a form., The landmark the highlighted row stands for, if the row is one.

### Community 106 - "MarkerVisibility"
Cohesion: 0.18
Nodes (5): MarkerVisibility, Cache surface occlusion by view and position for every kind of marker. The…, Whether the last pass is recent enough to be read instead of repeated., Mark these points as standing in front of the surface, untested. For frames…, Answer for a batch of points at once, ahead of being asked one by one. Every…

### Community 107 - "plane_solids.py"
Cohesion: 0.08
Nodes (36): compute_vertex_normals(), Area-weighted smooth vertex normals for an indexed triangle soup., planes_for(), The stages a form passes through on its way from a block to a figure. The…, How many solids each stage of a film is made of. Every count from the coarsest…, The detail setting that asks for ``solids``, or ``None`` if none does. The…, A stage as it is to be drawn, with its normals read at ``smooth``. Kept out of…, shaded() (+28 more)

### Community 108 - "test_tasks.py"
Cohesion: 0.15
Nodes (18): BodyMap, Region weights over the scene, as two RGBA volumes the shader samples by…, app(), fixture, Work run off the window, and the cards that show it running., Turn the event loop until ``until()`` says so, or give up., runner(), _spin() (+10 more)

### Community 109 - ".bone_at"
Cohesion: 0.22
Nodes (8): BoneRef, _project(), The nearest bone under the cursor, for showing its length., A world point in widget pixels, or ``None`` when it is behind the camera., How far along a screen-space segment the cursor's nearest point lies., Pixels from the cursor to the segment, or ``None`` if either end is behind., _segment_distance(), _segment_share()

### Community 110 - "DockTitle"
Cohesion: 0.10
Nodes (10): QDockWidget, QToolButton, DockTitle, PanelDock, QSize, QWidget, A dock that can go anywhere, with :class:`DockTitle` across the top., The bar across the top of a dock: a switch, a name and two buttons. (+2 more)

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - "._oriented"
Cohesion: 0.13
Nodes (8): setter, Dress ``obj`` in the skin a session says it wore, if it can be read., The active object turned and centred but not posed or placed., The active object exactly as its file stored it., Set the active object's file mesh; its rest mesh is turned from it as at a load., The active object, made on the spot when a mesh is handed to an empty scene., Turn a freshly read mesh the right way up and centre it., Put ``rig`` on the object's file mesh, or take the one it wears off.

### Community 113 - "Task"
Cohesion: 0.06
Nodes (26): BaseException, _outcome(), ProgressCard, Any, QObject, QPainter, QWidget, T (+18 more)

### Community 114 - "test_history.py"
Cohesion: 0.29
Nodes (11): measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch(), test_commands_carry_their_channel_and_name(), test_new_measurements_start_locked(), test_push_applies_then_undo_reverts() (+3 more)

### Community 115 - "Solid"
Cohesion: 0.18
Nodes (6): One convex piece of a form: its hull vertices and outward-wound faces., The hull of the points with its faces bowed out; see :func:`rounded_hull`., The longest side of the box the solid sits in., Whether a point lies inside, or within ``slack`` of the surface., A flat-shaded mesh, every triangle with its own three corners. Corners are not…, Solid

### Community 116 - "test_open_files.py"
Cohesion: 0.18
Nodes (9): app(), opened(), fixture, Files arriving from outside: the command line, a drop, or the desktop's "Open…, One offscreen Qt application for the run; see test_film_recorder., What the window was asked to open, by kind, without loading anything., Finder sends the launching file as an event, which can land before the window., test_a_file_the_desktop_hands_over_early_waits_for_the_window() (+1 more)

### Community 117 - "History"
Cohesion: 0.20
Nodes (4): History, A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive…, test_undo_and_redo_on_an_empty_stack_are_safe()

### Community 118 - "Session"
Cohesion: 0.08
Nodes (27): Path, A snapshot of everything worth keeping between runs., Session file that sits beside a model, e.g. ``bust.refview.json``., Session, sidecar_path(), Path, Write the document, and whatever the window says its layout is. The layout…, Write every skin made here beside the session; see :mod:`rig_file`. (+19 more)

### Community 119 - "AddItem"
Cohesion: 0.10
Nodes (11): Every document edit is a command, AddItem, Any, Command, Append an item to a document list., Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem (+3 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.07
Nodes (38): QPointF, QRectF, ArmatureTool, Turns clicks into nodes, and drags into moved or resized ones. The tool stays…, Drop the hover preview and the chain, leaving any guided run alone. Escape…, One marker object for endpoints, nodes, landmarks and tool previews., VisualMarker, OverlayParts (+30 more)

### Community 121 - "test_hotkeys.py"
Cohesion: 0.10
Nodes (24): QKeySequence, app(), _click(), _map(), fixture, Hotkeys: the map, the store, the binder, and the gesture that assigns one., One offscreen Qt application for the run; see test_film_recorder., End to end: the filter is on the panel's buttons and the window hears it. (+16 more)

### Community 122 - "armature.py"
Cohesion: 0.15
Nodes (5): ArmatureStore, A graph of named points under the form, and the wire it stands for. An armature…, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 123 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 124 - ".refresh_list"
Cohesion: 0.24
Nodes (5): QTreeWidgetItem, Rebuild the tree from the store, keeping the landmark being edited shown. Not…, Commit a renamed or re-checked form, or a renamed landmark, if anything changed., Give a freeform's own landmark the name typed into its row., Run a row's edit once Qt has finished delivering the current signal. Committing…

### Community 125 - "Reflow"
Cohesion: 0.30
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 126 - "forms.py"
Cohesion: 0.06
Nodes (42): build_freeform(), _centre(), FormFill, FormPreset, FormStage, freeform_landmark(), freeform_preset(), landmark_key() (+34 more)

### Community 127 - "SectionPanel"
Cohesion: 0.16
Nodes (7): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 128 - "._upload_sculpt"
Cohesion: 0.12
Nodes (7): The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, Cut the stand-in on a thread; see :meth:`_upload_sculpt`., Show the recording as a task, its bar the stages landed so far., The cross on the recording's card: the film is dropped, the switch too., A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on.

### Community 129 - "._sync_scene"
Cohesion: 0.07
Nodes (13): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…, The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, A skeleton changed: redraw it, and let the skin's body map follow its bones., What the renderer draws: each object as it stands, AutoSmoothed if asked., ``mesh`` shaded by the object's smoothing groups, found once and kept. The…, The whole scene as one mesh, as the planes and the skin tracer read it. The… (+5 more)

### Community 130 - "Stage"
Cohesion: 0.13
Nodes (12): QOpenGLFramebufferObject, The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, The line burned into the corner of the frame for ``stage``. Counted off the…, QImage, One stage, rendered as it would be exported. For the preview. (+4 more)

### Community 131 - "AnnotateTool"
Cohesion: 0.10
Nodes (15): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+7 more)

### Community 132 - "ExportLook"
Cohesion: 0.09
Nodes (17): ExportLook, What the frames are to look like, as against what they are of. Laid over the…, Which of the things drawn over the model belong in the frames., ``base`` with this export's choices laid over it., app(), FakeViewport, fixture, QImage (+9 more)

### Community 133 - "obj_loader.py"
Cohesion: 0.18
Nodes (16): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic(), ndarray, Minimal, dependency-free Wavefront OBJ reader. Only the geometry statements a… (+8 more)

### Community 134 - "preview"
Cohesion: 0.29
Nodes (7): app(), gallery_settings(), preview(), fixture, The gallery's list on a settings file of the tests' own, empty to begin with., One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 136 - "paths.py"
Cohesion: 0.21
Nodes (17): available_environments(), available_matcaps(), _bundled_root(), environment_dir(), image_path(), matcap_dir(), model_dir(), Path (+9 more)

### Community 137 - "Release"
Cohesion: 0.18
Nodes (12): The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, is_skipped(), QWidget, Background release check and the notice it puts in front of the artist. The…, Whether the artist already dismissed this exact version., Offer the release page, with the option never to be asked again. (+4 more)

### Community 138 - "load_mesh"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

### Community 139 - "Command"
Cohesion: 0.28
Nodes (3): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu.

### Community 140 - "._advance_pending"
Cohesion: 0.25
Nodes (4): Begin a run against a fresh form: a preset's walk, or a freeform's., Take up the selected freeform again, so more landmarks can go on it. The same…, After a landmark goes down: a fresh numbered name, the same side., Record an edit the viewport's tool worked out. A freeform's placed landmark is…

### Community 141 - "spatial.py"
Cohesion: 0.19
Nodes (11): _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Box the leaves up, coarsest level first and the leaves themselves last., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the…, Interleave each 10-bit value with two zero bits, ready to be shifted., Build the index from expanded triangle corners, shape ``(T, 3, 3)``., Triangle indices worth intersecting for this ray, possibly empty. (+3 more)

### Community 142 - "theme.py"
Cohesion: 0.13
Nodes (14): css(), A colour as a style sheet function, for the parts Qt draws., QObject, Making the whole of a switch the part you can press. The theme turns every…, Turns a press anywhere on a switch into a click on it., WholeFaceToggles, apply_dark_theme(), QApplication (+6 more)

### Community 143 - "MatcapPreview"
Cohesion: 0.08
Nodes (18): _angle(), MatcapPreview, _push_preview(), QSize, QWidget, A matcap on a sphere, which is also how the matcap is graded., Redraw from the settings, which something else has changed., Put the grading back, which is the one thing a disc cannot show. (+10 more)

### Community 144 - "._picker"
Cohesion: 0.10
Nodes (12): ndarray, Rub out the stroke points under the eraser, live., Take hold of a node, to move it, resize it, or just to select it. This works…, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Where the active object's gizmo falls on screen, or ``None``. (+4 more)

### Community 145 - "._carrying_a_copy"
Cohesion: 0.11
Nodes (10): opens_as(), Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model., Take a copied control out of whichever hand-built panel holds it., Open a file by what it is: a model, a session, a matcap or an HDRI. The one…, What a file opens as, by its suffix: a model, a session, a matcap or an HDRI., Apply a matcap image, reporting unreadable files to the user. (+2 more)

### Community 146 - "form_group"
Cohesion: 0.12
Nodes (15): QComboBox, What to call the joint filling a humanoid slot: ``"knee.L"`` is ``"Knee L"``., role_name(), QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row(), _NameOnlyDelegate (+7 more)

### Community 147 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 148 - "grid.py"
Cohesion: 0.14
Nodes (16): build_grid(), GridLines, nice_step(), Reference grids on the three axis planes, fading with distance. A grid gives…, Segments, with their colours and widths, ready for the stroke buffer., Every line of every enabled grid, or ``None`` when none is on., The nearest 1, 2 or 5 times a power of ten at or below ``value``., The spacing in use: the artist's, or a round share of the scene. (+8 more)

### Community 149 - "SurfacePicker"
Cohesion: 0.06
Nodes (36): LandmarkRef, Handle, Where a click at ``(x, y)`` would put a node. With free placement the node…, Where a grabbed node should move to. Free placement -- and a drag that wanders…, The thickness a resize drag is asking for: the cursor's reach, in world units., The nearest grabbable node under the cursor, if any. Only unlocked nodes of a…, The nearest grabbable landmark under the cursor, if any. Only the ones actually…, A view of the scene from one camera, sized to the widget. (+28 more)

### Community 150 - "test_body_regions.py"
Cohesion: 0.19
Nodes (16): The bones a skeleton's humanoid roles describe, as ``(count, 7)`` rows. Each…, role_bones(), What the skin shader's body map is worked out from, or ``None`` for no map. The…, _column(), _figure_bones(), ndarray, Where on the body the skin is: bones, height bands, the map, and the settings., A thin column standing from the ground to ``height``. (+8 more)

### Community 151 - "test_contour_shading.py"
Cohesion: 0.29
Nodes (5): parametrize, The contour shading mode: slices across the form, read off it like a map., test_a_custom_direction_is_normalised_and_an_empty_one_falls_back(), test_the_density_floor_keeps_the_spacing_finite(), test_the_slices_face_the_way_that_was_asked()

### Community 152 - "DataTexture"
Cohesion: 0.07
Nodes (18): EnvironmentTextures, The map, the sampling tables, and the uniforms that describe them., Put a map on the card, or take it off; cheap when it is the one already there., Point ``program`` at the map, scaled by ``scale_factor`` on top of the rig's…, OpenGL rendering layer: shader programs, textures and the scene renderer., DataTexture, default_matcap_pixels(), ndarray (+10 more)

### Community 153 - "Buried"
Cohesion: 0.11
Nodes (9): BoneLabels, Buried, Enum, str, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…, An ordered collection of skeletons, like the other document stores., The skeleton the model follows: the first one bound to its rig. (+1 more)

### Community 154 - "._focused_form"
Cohesion: 0.22
Nodes (4): Refit the focused freeform's clay; for a new one, remember the choice., Show a stage of the focused form. A view choice, so not an undo step., Size the stage slider to the focused form, and hide it for a one-stage form., The form the stage slider speaks for: the one being guided, else the one picked.

### Community 155 - ".install"
Cohesion: 0.29
Nodes (6): QApplication, Put the rule in place for every switch in the application., The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter., test_a_switch_answers_a_press_anywhere_on_its_face(), test_alt_is_left_alone_so_a_switch_can_still_be_copied()

### Community 156 - "test_spatial.py"
Cohesion: 0.26
Nodes (11): _grid(), The picking accelerator: it must be fast without changing any answer., A bumpy height field, so rays hit different triangles at different depths., The pruned candidate set must never miss the true intersection., Every parent must enclose its children, or a ray could slip past a leaf., test_a_batch_of_rays_gets_the_same_candidates_as_one_at_a_time(), test_a_ray_that_misses_the_model_is_pruned_away(), test_every_triangle_lands_in_exactly_one_leaf() (+3 more)

### Community 157 - "GuideRun"
Cohesion: 0.40
Nodes (3): GuideRun, Begin a preset run against an armature already in the store., A guided preset part-way through. The index walks the preset's own list rather…

### Community 158 - "shader_files.py"
Cohesion: 0.19
Nodes (9): _expand(), load_glsl(), Reading the GLSL out of :file:`render/glsl`. Each program's source lives in a…, The source of ``name`` with its includes, constants and defines worked in., _read(), GLSL sources for the viewport, read from :file:`render/glsl`. A handful of…, Skin BRDF and bounded-depth light transport, shared by preview and refinement.…, The GLSL on disk: its includes and constants, and that every program is whole. (+1 more)

### Community 159 - ".paintGL"
Cohesion: 0.20
Nodes (4): Use the same cached visibility test for bones and all point markers., Which part wears the line this frame, and how solid it is, or ``None``. Also…, Hand the renderer the depth grid, or take it away, before a frame., Whether a gesture in the view is moving something right now. What holds the…

### Community 160 - "outline"
Cohesion: 0.40
Nodes (5): outline(), QColor, Draw the hairline that separates a control from the panel. One line, the same…, Change the one colour that is not grey, everywhere at once. The hand-painted…, set_accent()

### Community 162 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 163 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 164 - "Human Skin renderer"
Cohesion: 0.25
Nodes (7): Human Skin renderer, Marks and body regions, Material and transport, Scheduling, precision and compatibility, Surface, The HDRI, Where to change it

### Community 165 - "SectionGizmo"
Cohesion: 0.21
Nodes (7): Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo, The rail stands still while the camera moves, and never leaves the frame., test_section_rail_is_a_screen_space_cue_at_the_right_edge(), test_section_rail_paints_its_label()

### Community 166 - "test_skin_gl.py"
Cohesion: 0.13
Nodes (22): Draw one frame, then hand a neutral GL state back to the caller.…, _closed_patch(), gl_context(), _patch(), fixture, Real GL tests; skipped only when the test host cannot create a GL context., Nearest hits and shadow rays through a deep tree, pixel by pixel, against numpy., The tile wraps: the slope read just past the edge equals the one at the start. (+14 more)

### Community 167 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 168 - ".mouseMoveEvent"
Cohesion: 0.13
Nodes (6): Turn the lights by how far the drag has come: across about the vertical, up in…, Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Apply the pull live, so the figure moves under the cursor., Apply the drag live, so the clay re-forms under the cursor.

### Community 169 - "sample_count"
Cohesion: 0.50
Nodes (3): How many samples the framebuffer bound right now is drawing with. One where…, sample_count(), How many samples this view is really drawing with, or ``None``. Asked of GL…

### Community 170 - "_height_of"
Cohesion: 0.40
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 171 - "TriangleIndex"
Cohesion: 0.29
Nodes (6): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., Leaf bounding boxes over a Morton-sorted triangle list., TriangleIndex, test_an_empty_index_returns_no_candidates()

### Community 173 - "README.md"
Cohesion: 0.29
Nodes (9): Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets, render owns every GL call (+1 more)

### Community 176 - "raycast_mesh"
Cohesion: 0.17
Nodes (18): _cross(), intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Row-wise cross product, without :func:`numpy.cross`'s axis shuffling., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``., The closest hit along each of a batch of rays, ``None`` where one misses. One… (+10 more)

### Community 179 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 181 - "VideoSettings"
Cohesion: 0.08
Nodes (19): open_writer(), How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., Start an encoder for ``settings``, or say why there cannot be one., VideoSettings (+11 more)

### Community 183 - "HotkeyBinder"
Cohesion: 0.21
Nodes (9): QShortcut, HotkeyBinder, QObject, Turns the map into the shortcuts of one window, and keeps them current., Put every command's keys where they are heard. Cheap; run on any change., Say in a control's tooltip what key it answers to, if it is one of ours. A copy…, The shortcut answering for a command, for a test that wants to press it., A key the way the platform writes it -- ``⌘K`` on a Mac, ``Ctrl+K`` elsewhere. (+1 more)

### Community 186 - "ModelPanel"
Cohesion: 0.05
Nodes (23): ModelPanel, _NameOnlyDelegate, _ObjectTree, QPushButton, QStyledItemDelegate, QTreeWidgetItem, QWidget, Bind the panel to the viewport's transform tool. (+15 more)

### Community 187 - "settings_window.py"
Cohesion: 0.09
Nodes (18): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version(), current(), forget(), PreferenceStore, QObject, QSettings (+10 more)

### Community 188 - "MeasureTool"
Cohesion: 0.12
Nodes (10): MeasureTool, Handle, ndarray, The nearest grabbable endpoint under the cursor, if any. Only unlocked, visible…, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview. (+2 more)

### Community 191 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 192 - "quad"
Cohesion: 0.67
Nodes (3): fixture, quad(), Two triangles covering the unit square on the z = 0 plane.

### Community 193 - "KeyBox"
Cohesion: 0.11
Nodes (15): QKeySequenceEdit, assign(), HotkeyDialog, KeyBox, normalize(), press(), QDialog, QWidget (+7 more)

### Community 194 - ".__init__"
Cohesion: 0.14
Nodes (5): Push the preferences that this window's own parts hold a copy of. The store has…, Put the docks and the hand-built panels back where they were. Unless the artist…, Give each panel a dock of its own, tabbed together on the right. Each panel can…, Single-key shortcuts, scoped so they never eat text input. They only fire while…, Say which panel buttons are the same thing as a menu entry. The button that…

### Community 195 - "._build_menus"
Cohesion: 0.20
Nodes (6): _plain(), QAction, Open the preferences, on one group when the menu asked for one., A menu entry's text as a name: no accelerator ampersand, no trailing dots., Which panels are open, and the panels the artist builds. Rebuilt every time it…, Add a menu entry, optionally with a window-wide shortcut. Given a ``command``…

### Community 198 - "ask_for"
Cohesion: 0.18
Nodes (10): ask_for(), command_for(), Command, QAction, The command a control stands for, or ``None`` if it has no name to go by. A…, A menu entry. Its keys are heard anywhere in the window and shown in the menu., A key heard only while the view has the focus. The menu entry for it, if there…, A key heard anywhere in the window, with no menu entry of its own. (+2 more)

### Community 203 - "decode"
Cohesion: 0.27
Nodes (8): _coerce(), decode(), encode(), Any, T, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``.

### Community 204 - "CHANGELOG.md"
Cohesion: 0.25
Nodes (7): Shift-snapped orbiting (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding

### Community 205 - "_Encoder"
Cohesion: 0.22
Nodes (6): Queue, _Encoder, QObject, QWidget, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 207 - "Hit"
Cohesion: 0.16
Nodes (11): Hit, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., snap_to_vertex(), ndarray, Closest surface intersection under the cursor, or ``None``., Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-… (+3 more)

### Community 208 - ".skin_object"
Cohesion: 0.25
Nodes (5): ndarray, The 4x4 that takes a point on the old rest mesh onto the new one. A point sits…, Carry the measurements, annotations, armature and forms through ``carry``., Dress ``obj`` in a skin made for ``skeleton``, as one undo step. ``made`` came…, The 4x4 that carries a point of the file mesh onto the rest mesh. The rest mesh…

### Community 211 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 214 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 223 - "ui/hotkeys.py"
Cohesion: 0.16
Nodes (15): control_of(), decorate(), describe(), forget(), group_of(), listed(), Where the hotkeys are kept, and how they become keys that do things.…, Drop the loaded store, so the next call reads the settings again. For tests. (+7 more)

### Community 225 - "PlacedLandmark"
Cohesion: 0.08
Nodes (19): PlacedLandmark, Point3, One anatomical point the artist put on the model during a guided run., The landmark list with one point moved, and no longer a guess. A landmark the…, The landmark list with these points taken back off the model. More than one at…, Point3, The landmark list with one point moved, and no longer a guess. The same bargain…, mirror_landmarks() (+11 more)

## Knowledge Gaps
- **7 isolated node(s):** `refview`, `Surface`, `Marks and body regions`, `Material and transport`, `Scheduling, precision and compatibility` (+2 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `Stage`, `SceneObject`, `obj_loader.py`, `ExportLook`, `load_mesh`, `MeshBuffers`, `.apply_session`, `Skeleton`, `mesh_renderer.py`, `grid.py`, `SurfacePicker`, `PoseTool`, `test_body_regions.py`, `Buried`, `core/__init__.py`, `plane_volume.py`, `test_spatial.py`, `auto_skin`, `FilmRecorder`, `test_plane_clusters.py`, `test_skin_gl.py`, `convex.py`, `Camera`, `skeleton.py`, `TriangleIndex`, `gltf_loader.py`, `raycast_mesh`, `body_regions.py`, `plane_clusters.py`, `BodyRegionSettings`, `test_skeleton.py`, `quad`, `PrimaryForm`, `ShadingMode`, `test_objects.py`, `test_skin.py`, `test_plane_solids.py`, `load_obj`, `.__init__`, `Hit`, `.skin_object`, `core/environment.py`, `ViewerState`, `PlaneSettings`, `viewport.py`, `build_form`, `main_window.py`, `state.py`, `FormStore`, `Path`, `plane_solids.py`, `test_tasks.py`, `._oriented`, `Solid`, `Session`, `forms.py`?**
  _High betweenness centrality (0.213) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `._upload_sculpt`, `._sync_scene`, `Stage`, `AnnotateTool`, `ExportLook`, `test_preferences.py`, `MainWindow`, `._picker`, `SurfacePicker`, `PoseTool`, `.paintGL`, `FilmRecorder`, `SectionGizmo`, `film_export.py`, `.mouseMoveEvent`, `sample_count`, `ExportVideoDialog`, `._active_changed`, `FilmExport`, `MeasureTool`, `application.py`, `.__init__`, `PrimaryForm`, `test_objects.py`, `._place_joint`, `ObjectTool`, `._place_form_landmark`, `_Encoder`, `NavigationController`, `ViewerState`, `viewport.py`, `build_form`, `main_window.py`, `SetAttributes`, `ViewportOverlay`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `test_preferences.py`, `Viewport`, `SceneObject`, `MainWindow`, `Armature`, `.apply_session`, `CameraPanel`, `SurfacePicker`, `test_body_regions.py`, `test_planes_panel.py`, `PoseTool`, `auto_skin`, `ShadingPanel`, `panel`, `SectionGizmo`, `README.md`, `test_matcap_preview.py`, `BodyRegionSettings`, `application.py`, `.__init__`, `PrimaryForm`, `test_objects.py`, `test_custom_panels.py`, `.__init__`, `.skin_object`, `viewport.py`, `MatcapPanel`, `main_window.py`, `test_elements.py`, `state.py`, `._oriented`, `Task`, `Session`, `ViewportOverlay`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 60 inferred relationships involving `Mesh` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Mesh` has 60 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `OverlayParts`) actually correct?**
  _`ViewerState` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Skeleton` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Skeleton` has 9 INFERRED edges - model-reasoned connections that need verification._