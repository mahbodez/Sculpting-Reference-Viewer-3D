# Graph Report - reference-viewer  (2026-09-16)

## Corpus Check
- 152 files · ~485,039 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5076 nodes · 11594 edges · 200 communities (181 shown, 19 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 554 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `adec1c9f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SettingsWindow
- test_preferences.py
- update_check.py
- Viewport
- plane_axes.py
- settings.py
- MainWindow
- Stroke
- GifWriter
- Joint
- SceneRenderer
- convex.py
- main_window.py
- _wires
- Armature
- mesh_io.py
- ViewerState
- Skeleton
- skin_refinement.py
- CameraPanel
- SetAttributes
- ShaderProgram
- test_forms.py
- test_planes_panel.py
- MeasurePanel
- test_session.py
- Writer
- SectionSettings
- plane_volume.py
- ControlsWindow
- spatial.py
- ShadingPanel
- PlaneSettings
- test_camera.py
- test_plane_clusters.py
- WakeLock
- ._built
- MatcapPreview
- Frame
- film_export.py
- SurfacePicker
- Camera
- Wires
- ValueSlider
- gltf_loader.py
- ExportVideoDialog
- open_writer
- _Build
- Agent Graph-First Instructions
- VideoSettings
- plane_clusters.py
- test_matcap_preview.py
- test_armature.py
- ArmaturePanel
- PrimaryForm
- test_hotkeys.py
- FilmExport
- FormsPanel
- PlanesPanel
- test_skeleton.py
- ArmatureTool
- Workspace
- ui/hotkeys.py
- Solid
- application.py
- MeasureTool
- Link
- FormTool
- pose_panel.py
- load_obj
- AnnotatePanel
- test_plane_solids.py
- ._selected
- .load
- PoseTool
- texture.py
- load_matcap_pixels
- test_custom_panels.py
- MeshBuffers
- _fill
- test_contour_shading.py
- NavigationController
- Bounds
- raycast_mesh
- test_forms_panel.py
- Mesh
- QWidget
- core/__init__.py
- MatcapPanel
- ColorButton
- FrameBar
- _Encoder
- ._picker
- test_elements.py
- AnnotateTool
- obj_loader.py
- ReflowLayout
- Measurement
- ._selected_landmark
- OrientationSettings
- clone.py
- test_skin.py
- Path
- _derived
- .mouseReleaseEvent
- test_panel_docks.py
- ._menu_action
- ._place_armature_node
- load_mesh
- Release
- DockTitle
- test_reflow.py
- MatcapSettings
- Skin
- Rig
- ._build
- test_open_files.py
- OpenRequests
- Hit
- AddItem
- ViewportOverlay
- release.yml
- ArmatureStore
- PointEdit
- _tab_switch
- Reflow
- ._carrying_a_copy
- CHANGELOG.md
- Preferences
- ._sync_scene
- Stage
- MarkerVisibility
- ExportLook
- ._place_form_landmark
- preview
- orientation.py
- palette.py
- plane_count
- watch_keys
- ._apply
- _drag_over
- UpdateChecker
- paths.py
- Command
- .mouseMoveEvent
- .split_point
- ReplaceItems
- session.py
- FormStore
- WholeFaceToggles
- Session
- test_resetting_the_layout_puts_the_docks_back_at_once
- navigation.py
- .update_enabled
- restored
- test_resetting_keeps_the_panels_built_by_hand
- viewport.py
- test_the_switch_is_not_squeezed_to_nothing
- ._chosen_armature
- .install
- coarse_lattice
- TriangleIndex
- .column_of
- .update_enabled
- Human Skin renderer
- test_spatial.py
- .refresh_list
- coarse_lattice
- environment.yml
- ._build
- _height_of
- _file_drag
- generate_matcaps.py
- ._build
- ndarray
- test_the_switch_on_a_dock_bar_is_the_panels_own_visibility
- quad
- test_a_session_saved_without_panels_leaves_the_ones_open_alone
- test_a_panel_does_not_cover_its_own_title
- app
- test_a_panel_can_be_taken_away_and_another_built_after_a_restore
- test_loading_a_session_over_a_restored_layout_survives
- skin_detail.py
- test_the_dock_of_a_panel_taken_away_is_used_again
- .with_landmark_at
- test_a_reused_dock_does_not_bring_the_old_panels_contents_with_it
- ModelPanel
- wakelock.py
- ._commit_node_drag
- ._buried_nodes
- _clamp
- Cloner
- .new_armature
- ._selected_rows
- ._place_joint
- section
- panel
- ._export_surface
- ._scene_center
- test_the_window_follows_a_change_it_did_not_make

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 165 edges
2. `Viewport` - 130 edges
3. `ViewerState` - 96 edges
4. `Camera` - 91 edges
5. `MainWindow` - 87 edges
6. `Skeleton` - 85 edges
7. `Armature` - 81 edges
8. `PrimaryForm` - 79 edges
9. `PlaneSettings` - 68 edges
10. `SurfacePicker` - 66 edges

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

## Communities (200 total, 19 thin omitted)

### Community 0 - "SettingsWindow"
Cohesion: 0.07
Nodes (30): What the artist prefers, as distinct from what the document says. There are two…, current(), forget(), PreferenceStore, QObject, QSettings, _qcolor(), Where the preferences are kept, and what happens when one changes.… (+22 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.12
Nodes (19): app(), model(), fixture, What the artist prefers: kept apart from the document, and acted upon. Two…, One triangle, which is a mesh as far as any of this is concerned., Windows that clean up after themselves, and a settings file that does., A session is not the only thing worth carrying on from., Otherwise the marks from one piece of work arrive on top of another. (+11 more)

### Community 2 - "update_check.py"
Cohesion: 0.10
Nodes (31): check_for_update(), fetch_latest_release(), is_newer(), _macos_root_certificates(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and… (+23 more)

### Community 3 - "Viewport"
Cohesion: 0.07
Nodes (14): QOpenGLWidget, Renders the scene and turns mouse gestures into camera and tool actions., Slide the view so a point sits at the centre, keeping the angle., Slide the view so a measurement sits at the centre, keeping the angle., End any film being recorded, and wait for its thread to really stop. For…, The document being drawn., How many samples this view is really drawing with, or ``None``. Asked of GL…, The film of the form's making, as far as it has been recorded. (+6 more)

### Community 4 - "plane_axes.py"
Cohesion: 0.08
Nodes (39): _empty(), plane_axes(), ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, A level with no place in it: nearest direction wins, as before., How much surface each vertex stands for: a third of each triangle on it.…, The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to. (+31 more)

### Community 5 - "settings.py"
Cohesion: 0.05
Nodes (38): Coefficients, What each block of the design matrix counts for, against the normals. A fit…, Whether anything but the normals is being read at all., fit_planes(), The planes of ``mesh`` under ``mode``; empty where the mode needs none., ContourDirection, ContourShadingSettings, LightSettings (+30 more)

### Community 6 - "MainWindow"
Cohesion: 0.05
Nodes (19): MainWindow, QMainWindow, Open the preferences, on one group when the menu asked for one., Push the preferences that this window's own parts hold a copy of. The store has…, Open an empty panel of the artist's own and bring it to the front., Put the docks and the hand-built panels back where they were. Unless the artist…, Put the panels back where they started, now., Follow the machine's sleep to whether this window is in front. (+11 more)

### Community 7 - "Stroke"
Cohesion: 0.06
Nodes (37): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+29 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "Joint"
Cohesion: 0.07
Nodes (35): Quat, Quat4, compose(), euler_to_quat(), matrix_to_quat(), quat_between(), quat_conjugate(), quat_multiply() (+27 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.06
Nodes (43): look_at(), orthographic(), Right-handed view matrix looking from ``eye`` towards ``target``., Symmetric orthographic projection with the given vertical half-extent., Unit vector for an azimuth/elevation pair, with +Y as the pole., spherical_direction(), vec3(), Everything the viewport needs in order to draw a frame. (+35 more)

### Community 11 - "convex.py"
Cohesion: 0.12
Nodes (22): convex_hull(), flat_mesh(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, The outward unit normal at each vertex: the area-weighted mean of its faces'. A…, The barycentric ``(w, u, v)`` of an even grid over a triangle. (+14 more)

### Community 12 - "main_window.py"
Cohesion: 0.05
Nodes (57): QIcon, The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, _draw_glyph(), glyph(), lock_icon(), QColor, QPixmap (+49 more)

### Community 13 - "_wires"
Cohesion: 0.11
Nodes (29): The order the artist put the bones in is what the scrub walks through, which is…, The claim the whole film rests on, asked again with an armature under it: an…, test_a_film_of_clay_on_a_wire_lays_it_down_in_the_order_it_was_listed(), test_the_last_stage_of_a_film_on_a_wire_is_the_form_the_slider_gives(), _bar(), _holds(), A long ellipsoid: one closed form with an obvious axis to lie along., Whether a fitted solid has a point inside it. (+21 more)

### Community 14 - "Armature"
Cohesion: 0.05
Nodes (40): Armature, ArmatureNode, Bone, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves., A plausible thickness for a node placed by hand. (+32 more)

### Community 15 - "mesh_io.py"
Cohesion: 0.23
Nodes (11): Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets (+3 more)

### Community 16 - "ViewerState"
Cohesion: 0.07
Nodes (25): Session file that sits beside a model, e.g. ``bust.refview.json``., sidecar_path(), Command, ndarray, Path, QObject, The skeletons changed; re-pose the model if one of them drives it. ``live`` is…, Emit the change signal a command's channel maps onto. (+17 more)

### Community 17 - "Skeleton"
Cohesion: 0.08
Nodes (19): _matrix16(), A copy with the rest translation replaced and the frame kept., A tree -- or a forest -- of joints and the pose they stand in., Every joint, parents before children. A file may list a child before its…, Every joint below ``index``, nearest first., Every joint's transform in scene space, as ``(n, 4, 4)``. With ``rest`` the…, Where every joint sits, as ``(n, 3)``., Every ``(parent, child)`` pair, parents first. (+11 more)

### Community 18 - "skin_refinement.py"
Cohesion: 0.05
Nodes (27): AccumTarget, bind_default(), ColorTarget, DepthTarget, FrameTarget, GeometryTarget, Offscreen render targets used by the high-quality, ghost and smoothing passes.…, A depth-only framebuffer, sampled afterwards as a texture. (+19 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): CameraPanel, QListWidgetItem, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "SetAttributes"
Cohesion: 0.06
Nodes (21): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, PosePanel, QTreeWidgetItem, QWidget, Run a row's edit once Qt has finished delivering the current signal., Arms the pose tool, lists the joints and poses the selected one., Adopt the viewport's tools: the pose tool, and the armature's for its selection. (+13 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "test_forms.py"
Cohesion: 0.07
Nodes (38): merged(), The hull of the points with its faces bowed out; see :func:`rounded_hull`., Several flat meshes as one, or ``None`` when there is nothing to draw., _closed(), _inside(), _left_only(), _marks(), ndarray (+30 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.08
Nodes (21): _names(), The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as…, Or there would be no way to turn one back on., A limb is four bones, and deciding not to block the arms in is one decision.…, It is rebuilt on every change, and ticking one row of a selected limb would be… (+13 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.13
Nodes (8): MeasurePanel, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn.

### Community 25 - "test_session.py"
Cohesion: 0.06
Nodes (23): BookmarkStore, CameraBookmark, Named camera positions the artist can jump between while sculpting., A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Session persistence, measurements and bookmarks. (+15 more)

### Community 26 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 27 - "SectionSettings"
Cohesion: 0.08
Nodes (29): Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, The direction the section plane faces. (+21 more)

### Community 28 - "plane_volume.py"
Cohesion: 0.04
Nodes (108): _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field(), block_labels(), block_splits() (+100 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "spatial.py"
Cohesion: 0.19
Nodes (11): _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Box the leaves up, coarsest level first and the leaves themselves last., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the…, Interleave each 10-bit value with two zero bits, ready to be shifted., Build the index from expanded triangle corners, shape ``(T, 3, 3)``., Triangle indices worth intersecting for this ray, possibly empty. (+3 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.20
Nodes (6): Chooses the shading model and edits its light and surface parameters., Freeze the slices the way the camera faces now. The view direction is the one…, Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel, test_a_copied_group_still_drives_the_originals(), test_copying_a_group_brings_its_rows()

### Community 32 - "PlaneSettings"
Cohesion: 0.05
Nodes (72): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, Holds the working state between one turn of the sliders and the next.…, The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache, PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor… (+64 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (57): The joint list with ``index`` resting at ``target`` and its children left be., angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad() (+49 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (31): c_void_p, _Backend, _MacBackend, _platform_backend(), The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., Holds sleep off while the window that owns it is the one in front. The class…, Hold sleep off, or stop holding it, whichever is not already true. (+23 more)

### Community 36 - "._built"
Cohesion: 0.13
Nodes (8): QMenu, Path, QImage, QRect, Offer the picture back as a file: as graded here, or as it came. A grading…, The matcap as a picture, at its own resolution. Square and opaque, with the…, Where the sphere goes: square, centred, above the legend., The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…

### Community 37 - "MatcapPreview"
Cohesion: 0.10
Nodes (11): MatcapPreview, QSize, QWidget, A matcap on a sphere, which is also how the matcap is graded., Redraw from the settings, which something else has changed., Put the grading back, which is the one thing a disc cannot show., Turn the matcap by the angle the cursor swept about the centre. By angle and…, Two grades on one drag: one along each axis of the movement. Both move together… (+3 more)

### Community 38 - "Frame"
Cohesion: 0.04
Nodes (61): carried(), in_flight(), Read a drag's payload back, or ``None`` if it is not one of ours., Make every control under ``root`` that can be copied Alt-draggable. A group is…, watch_tree(), CustomPanel, _detach(), QFormLayout (+53 more)

### Community 39 - "film_export.py"
Cohesion: 0.08
Nodes (17): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+9 more)

### Community 40 - "SurfacePicker"
Cohesion: 0.07
Nodes (33): Any, Take the choices out of a settings file, keeping what makes sense. Forgiving,…, Where a click at ``(x, y)`` would put a landmark: on the surface, or nowhere.…, A view of the scene from one camera, sized to the widget., Pixels between a world point and the cursor, or ``None`` if behind., SurfacePicker, Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction. (+25 more)

### Community 41 - "Camera"
Cohesion: 0.04
Nodes (46): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., Camera, Projection, Enum, ndarray, str, Interactive camera model driving both perspective and orthographic views. (+38 more)

### Community 42 - "Wires"
Cohesion: 0.08
Nodes (21): QThread, Film, A whole making, from the coarsest stage to the one the slider asks for. Held by…, An armature, as the clay reads it: where each length of wire runs. The order…, How many lumps the wire itself asks for., What a cache has to compare to know the wire has not moved., Wires, FilmRecorder (+13 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (11): _pull_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end., Set the value the way a hand on the control would., The value the track stands at ``x`` pixels across. (+3 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.10
Nodes (36): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), _first_skin(), GltfLoadError, load_gltf(), _local_transform() (+28 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.10
Nodes (13): QProgressDialog, even(), ExportVideoDialog, Path, QDialog, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+5 more)

### Community 46 - "open_writer"
Cohesion: 0.08
Nodes (28): _encode_arguments(), _encoders(), ffmpeg_path(), _FFmpegWriter, _no_window(), open_writer(), Path, RuntimeError (+20 more)

### Community 47 - "_Build"
Cohesion: 0.19
Nodes (14): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _mid(), ndarray, Somewhere to collect nodes while the rules that need each other run. (+6 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "VideoSettings"
Cohesion: 0.18
Nodes (7): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, TestTiming

### Community 50 - "plane_clusters.py"
Cohesion: 0.06
Nodes (41): PlaneAxes, PlaneSet, One level of a fit: the planes the shader is to quantise against. A plane is a…, The planes a model falls into, at every count. Built once per mesh and per…, The best ``count`` planes, or as many as the model supports. A model whose…, _compact(), _consensus(), _cut() (+33 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.10
Nodes (32): QPoint, _drag(), parametrize, The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc., Dragging further than the range goes is not a negative gamma., Alt and a drag copies a control; the disc must not swallow that. (+24 more)

### Community 52 - "test_armature.py"
Cohesion: 0.08
Nodes (54): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _chain(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other., The femoral head is in from the ASIS, below it and behind it, by shares of the… (+46 more)

### Community 53 - "ArmaturePanel"
Cohesion: 0.14
Nodes (5): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Take back the landmark before this one and ask for it again., Record an edit the viewport's tool worked out., The multiplier the position boxes are read and written through.

### Community 54 - "PrimaryForm"
Cohesion: 0.06
Nodes (44): build_form(), built_count(), form_mesh(), landmark_signature(), median_plane_ready(), PrimaryForm, ndarray, Point3 (+36 more)

### Community 55 - "test_hotkeys.py"
Cohesion: 0.05
Nodes (36): Command, HotkeyMap, Which keys do what, as the artist has decided rather than as it ships. A hotkey…, Whether the artist has moved this command off what it ships with., Which command has these keys, if any., Every command with keys on it, declared or not, as id -> keys., Put ``keys`` on a command, taking them off whatever had them. Returns the id of…, Back to the shipped keys, for one command or for all of them. For one command… (+28 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (11): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+3 more)

### Community 57 - "FormsPanel"
Cohesion: 0.04
Nodes (32): FormsPanel, QTreeWidgetItem, Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Begin a run against a fresh form: a preset's walk, or a freeform's., Take up the selected freeform again, so more landmarks can go on it. The same…, The freeform the highlighted row belongs to, when no run is on. (+24 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.16
Nodes (7): PlanesPanel, Lay one length of wire earlier or later, as one undoable step., Put the design matrix back the way it reads a figure., Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Breaks the form into planes, in the shading or in the geometry itself., Re-read the armatures and what the chosen one is laying down. Called whenever…

### Community 59 - "test_skeleton.py"
Cohesion: 0.12
Nodes (32): quat_from_axis_angle(), The model as ``skeleton`` poses it, or ``rest`` itself when it cannot. Linear…, skinned_mesh(), _arm(), ndarray, parametrize, Skeletons: the joint tree, posing, skinning, and where skeletons come from., The strip as a GLB with a two-joint skin, optionally saved mid-bend. (+24 more)

### Community 60 - "ArmatureTool"
Cohesion: 0.06
Nodes (39): LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, Handle, Begin a preset run against an armature already in the store., The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now. (+31 more)

### Community 61 - "Workspace"
Cohesion: 0.05
Nodes (32): QDockWidget, QScrollArea, QTabBar, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top., Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, scrollable(), _number_in() (+24 more)

### Community 62 - "ui/hotkeys.py"
Cohesion: 0.04
Nodes (60): QKeySequence, QKeySequenceEdit, QShortcut, ask_for(), assign(), command_for(), control_of(), decorate() (+52 more)

### Community 63 - "Solid"
Cohesion: 0.10
Nodes (42): DegenerateHullError, One convex piece of a form: its hull vertices and outward-wound faces., The longest side of the box the solid sits in., Whether a point lies inside, or within ``slack`` of the surface., The points are flat, collinear or too few to hold any volume., Solid, _across(), blend_rings() (+34 more)

### Community 64 - "application.py"
Cohesion: 0.14
Nodes (17): ArgumentParser, Namespace, QSplashScreen, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font(), main() (+9 more)

### Community 65 - "MeasureTool"
Cohesion: 0.12
Nodes (10): MeasureTool, Handle, ndarray, The nearest grabbable endpoint under the cursor, if any. Only unlocked, visible…, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview. (+2 more)

### Community 66 - "Link"
Cohesion: 0.11
Nodes (10): CloneGesture, Link, _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original., Whether the copy is being used right now and must not be written. (+2 more)

### Community 67 - "FormTool"
Cohesion: 0.07
Nodes (28): FormLandmarkRef, FormSettings, How the forms are drawn, and how their landmarks are placed., FormRun, FormTool, ndarray, Begin a run against a form already in the store., Every landmark the walk will ask for under these choices. With mirroring on,… (+20 more)

### Community 68 - "pose_panel.py"
Cohesion: 0.06
Nodes (45): What to call the joint filling a humanoid slot: ``"knee.L"`` is ``"Knee L"``., role_name(), armature_from_skeleton(), armature_root(), build_humanoid_skeleton(), detail_joints(), humanoid_positions(), humanoid_roles() (+37 more)

### Community 69 - "load_obj"
Cohesion: 0.24
Nodes (13): load_obj(), Path, Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, _push_slider(), Negative face indices count back from the most recent vertex., test_obj_relative_indices_still_load(), OBJ parsing: normals, triangulation and index handling., test_empty_file_is_rejected() (+5 more)

### Community 70 - "AnnotatePanel"
Cohesion: 0.20
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 71 - "test_plane_solids.py"
Cohesion: 0.04
Nodes (85): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), block(), coarse_lattice(), dumbbell(), edge_use() (+77 more)

### Community 72 - "._selected"
Cohesion: 0.14
Nodes (7): Run a row's edit once Qt has finished delivering the current signal. Committing…, Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., Run a bone between the row selected now and the node held before it., Join two nodes of one armature, if they are two and they are one armature., The node the selected row stands for, if the row is a node at all., The armature the selected row stands for, when the row is not a node.

### Community 73 - ".load"
Cohesion: 0.20
Nodes (9): Version 4 files predate the armature; they open with an empty one., test_a_session_from_before_the_armature_still_loads(), test_an_armature_survives_a_session_round_trip(), test_a_session_carries_the_hand_built_panels(), Version 1 files predate the annotation layer and the endpoint lock., Version 6 files predate panels being something a session could carry., test_a_session_from_before_annotations_still_loads(), test_a_session_from_before_the_panels_moved_still_loads() (+1 more)

### Community 74 - "PoseTool"
Cohesion: 0.06
Nodes (47): JointRef, quat_to_matrix(), The 3x3 rotation a unit quaternion stands for., How skeletons are drawn, and how the pose tool behaves., SkeletonSettings, PoseTool, _project_many(), ndarray (+39 more)

### Community 75 - "texture.py"
Cohesion: 0.07
Nodes (19): OpenGL rendering layer: shader programs, textures and the scene renderer., DataTexture, default_matcap_pixels(), MatcapLoadError, ndarray, RuntimeError, Matcap texture loading and upload, and the small data table beside it., An RGBA16F 2D texture with clamped edges and mipmapped minification. (+11 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.27
Nodes (14): Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels(), Path (+6 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.05
Nodes (30): Cross-section tool (1.1.0), QMimeData, Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel (+22 more)

### Community 78 - "MeshBuffers"
Cohesion: 0.08
Nodes (12): _ghost_depth_range(), MeshBuffers, Where the form starts along the view, and how deep it is. The ghost weighs a…, Forget the contents without releasing the buffer objects., Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are…, Whichever geometry is standing for the model this frame. (+4 more)

### Community 79 - "_fill"
Cohesion: 0.29
Nodes (7): _as_kind_of(), equal(), _fill(), Any, Copy what type-checks out of ``written`` and into ``group``. The default…, ``value`` as the same sort of thing as ``like``, or ``None`` if it is not. A…, Whether two preference objects say the same thing. Dataclasses compare by value…

### Community 80 - "test_contour_shading.py"
Cohesion: 0.29
Nodes (5): parametrize, The contour shading mode: slices across the form, read off it like a map., test_a_custom_direction_is_normalised_and_an_empty_one_falls_back(), test_the_density_floor_keeps_the_spacing_finite(), test_the_slices_face_the_way_that_was_asked()

### Community 81 - "NavigationController"
Cohesion: 0.10
Nodes (12): NavigationController, Orbit in whole increments of ``step`` degrees from the drag's start., Degrees of yaw per pixel, signed by whether the drag is inverted., The per-notch multiplier, scaled about 1 rather than multiplied. Zoom is…, Tracks an in-progress drag and applies it to a camera., Apply the motion since the previous event. Returns ``True`` if moved., How a drag turns into camera motion, so the preferences can set it., test_panning_ignores_the_snap_angle() (+4 more)

### Community 82 - "Bounds"
Cohesion: 0.10
Nodes (23): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, Bounds, ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero). (+15 more)

### Community 83 - "raycast_mesh"
Cohesion: 0.17
Nodes (18): _cross(), intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Row-wise cross product, without :func:`numpy.cross`'s axis shuffling., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``., The closest hit along each of a batch of rays, ``None`` where one misses. One… (+10 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.10
Nodes (32): app(), _click(), panel(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The… (+24 more)

### Community 85 - "Mesh"
Cohesion: 0.04
Nodes (72): auto_smooth(), compute_vertex_normals(), _gathered(), Mesh, Triangle-mesh containers shared by the loader, the renderer and picking., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Return a copy whose bounding-box centre sits at the origin., Which group each of ``total`` things lands in, given pairs that agree. Hooking… (+64 more)

### Community 86 - "QWidget"
Cohesion: 0.10
Nodes (26): QSpinBox, _begin(), can_clone(), clone(), _clone_frame(), _clone_point(), _clone_slider(), _clone_spin() (+18 more)

### Community 87 - "core/__init__.py"
Cohesion: 0.04
Nodes (82): BoneLabels, PlacedLandmark, Enum, str, A graph of named points under the form, and the wire it stands for. An armature…, One anatomical point the artist put on the model during a guided run., When the length of a bone is written beside it., build_freeform() (+74 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.15
Nodes (10): MatcapPanel, Rebuild the thumbnail list from the resources folder., The disc was dragged: show the renderer and the numbers what it did., A different matcap: the disc draws whichever one is on the model., Put the numbers back in line with the settings, and redraw the disc. Separate…, Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, It is the panel's main control; a click on a bar must not take it away. (+2 more)

### Community 89 - "ColorButton"
Cohesion: 0.15
Nodes (8): _clone_swatch(), _pull_swatch(), _push_swatch(), ColorButton, QColor, QSize, A swatch that opens a colour picker. Colours are exchanged as 0-1 RGB tuples,…, Open the picker, as a click on the swatch does.

### Community 90 - "FrameBar"
Cohesion: 0.08
Nodes (11): FrameBar, QFormLayout, QPainter, QSize, QWidget, The mark beside a group's name: filled when open, a ring when shut. It is the…, The rows inside the frame. ``layout()`` is the frame's own, which stacks the…, The row layout the frames are filled with. (+3 more)

### Community 91 - "_Encoder"
Cohesion: 0.25
Nodes (5): Queue, _Encoder, QObject, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 92 - "._picker"
Cohesion: 0.16
Nodes (6): Rub out the stroke points under the eraser, live., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…, Take hold of a landmark, to move it or just to say which one it is., Take hold of a joint -- or of a bone, by its far end., Take hold of a form's landmark, to move it or just to say which one it is.

### Community 93 - "test_elements.py"
Cohesion: 0.09
Nodes (17): Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., A matcap has no light to aim, so the Light group goes -- and its space. The…, Run the refresh the shared timer would have run., ``self._mode`` is ``mode``; the group called Mode settles for a number. (+9 more)

### Community 94 - "AnnotateTool"
Cohesion: 0.08
Nodes (19): AnnotateMode, AnnotationSettings, Enum, str, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a…, AnnotateTool (+11 more)

### Community 95 - "obj_loader.py"
Cohesion: 0.15
Nodes (19): MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast() (+11 more)

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - "Measurement"
Cohesion: 0.10
Nodes (15): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+7 more)

### Community 98 - "._selected_landmark"
Cohesion: 0.12
Nodes (7): Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors., Show the landmark group only once there are landmarks to show., The landmark the highlighted row stands for, if the row is one., Which armature the landmark list is pointing into, row or heading., Follow the highlighted landmark, and say which one it is in the view.

### Community 99 - "OrientationSettings"
Cohesion: 0.18
Nodes (14): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., test_an_identity_turn_reuses_the_mesh(), test_every_up_axis_lands_on_world_up() (+6 more)

### Community 100 - "clone.py"
Cohesion: 0.09
Nodes (33): QAbstractButton, QComboBox, QLineEdit, QSlider, _clone_button(), _clone_check(), _clone_combo(), _clone_label() (+25 more)

### Community 101 - "test_skin.py"
Cohesion: 0.09
Nodes (25): build_scene(), ndarray, Stackless BVH tables for the OpenGL 3.3 skin tracer (no compute extension).…, Build on a worker from the immutable meshes currently drawn by the renderer., Pack a linear texel array within the driver's actual 2D texture limit., texture_table(), TraceScene, pixel_jitter() (+17 more)

### Community 102 - "Path"
Cohesion: 0.13
Nodes (10): Path, Pick up whatever was last being worked on, if that was asked for. A session…, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window., Take a copied control out of whichever hand-built panel holds it., Open a file by what it is: a model, a session or a matcap. The one door every…, A path written down last time, if it is one and it is still there. (+2 more)

### Community 103 - "_derived"
Cohesion: 0.10
Nodes (24): _kept_laying(), Fresh bones, laid the way the armature was already laying them. The bone list…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _derived(), A guess the artist corrects is theirs, and the mirror leaves it alone., The new list is the edit; the old one has to survive to be undone to., Hips, then the ribcage, then the head, then the limbs largest first. This order… (+16 more)

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.13
Nodes (8): Record the finished drag as a single undo step., Record the finished drag as one step, or read a press as a selection., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Record the finished pull as one step, or read a press as a selection., Track the joint and bone under the cursor; True when either changed., Record the finished drag as one step, or read a press as a selection., Track the form landmark under the cursor; True when it changed.

### Community 105 - "test_panel_docks.py"
Cohesion: 0.14
Nodes (3): Each panel in a dock of its own, and putting the docks back next time. Two…, test_a_restored_copy_drives_the_new_windows_own_control(), test_the_layout_comes_back_through_the_settings()

### Community 106 - "._menu_action"
Cohesion: 0.40
Nodes (4): _plain(), QAction, A menu entry's text as a name: no accelerator ampersand, no trailing dots., Add a menu entry, optionally with a window-wide shortcut. Given a ``command``…

### Community 107 - "._place_armature_node"
Cohesion: 0.15
Nodes (6): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…, The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, A skeleton changed: redraw it., Hand the renderer a re-posed model and nothing else. For the frames of a pose…

### Community 108 - "load_mesh"
Cohesion: 0.22
Nodes (14): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one(), test_binary_stl_welds_shared_corners() (+6 more)

### Community 109 - "Release"
Cohesion: 0.18
Nodes (12): The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, is_skipped(), QWidget, Background release check and the notice it puts in front of the artist. The…, Whether the artist already dismissed this exact version., Offer the release page, with the option never to be asked again. (+4 more)

### Community 110 - "DockTitle"
Cohesion: 0.09
Nodes (14): QToolButton, DockTitle, make_switch(), QCheckBox, QSize, QWidget, One dock per panel, with a bar of its own across the top. Every panel is its…, Put a show/hide switch at the left of the bar and return it. (+6 more)

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - "MatcapSettings"
Cohesion: 0.11
Nodes (22): MatcapSettings, Post-processing applied to the sampled matcap texel., _angle(), _clone_preview(), grade(), _pull_preview(), _push_preview(), ndarray (+14 more)

### Community 113 - "Skin"
Cohesion: 0.25
Nodes (4): Which joints move each vertex, and by how much. Plain arrays, and never written…, The skin in the space a rigid ``matrix`` carries the model into., Skin, ValueError

### Community 114 - "Rig"
Cohesion: 0.09
Nodes (9): Buried, What becomes of the part of the armature the model is standing in front of. An…, An ordered collection of skeletons, like the other document stores., The skeleton the model follows: the first one bound to its rig., The skeleton a model file came with, in the model's own coordinates. Read once…, A document skeleton standing exactly where the file's joints stand., Which document joint each rig joint answers to. Returns two ``(j,)`` arrays:…, Rig (+1 more)

### Community 115 - "._build"
Cohesion: 0.27
Nodes (6): QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 116 - "test_open_files.py"
Cohesion: 0.18
Nodes (9): app(), opened(), fixture, Files arriving from outside: the command line, a drop, or the desktop's "Open…, One offscreen Qt application for the run; see test_film_recorder., What the window was asked to open, by kind, without loading anything., Finder sends the launching file as an event, which can land before the window., test_a_file_the_desktop_hands_over_early_waits_for_the_window() (+1 more)

### Community 117 - "OpenRequests"
Cohesion: 0.15
Nodes (8): Application, OpenRequests, Path, QApplication, The Qt application, listening for the desktop's way of handing over a file., Files the desktop asked the viewer to open, kept until there is a window. On…, Open ``path`` in the window, or hold it until there is one., Name the window files go to, and hand over any that came early.

### Community 118 - "Hit"
Cohesion: 0.16
Nodes (11): Hit, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., snap_to_vertex(), ndarray, Closest surface intersection under the cursor, or ``None``., Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-… (+3 more)

### Community 119 - "AddItem"
Cohesion: 0.14
Nodes (16): AddItem, Append an item to a document list., History, A bounded undo/redo stack., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made() (+8 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.08
Nodes (31): QPointF, QRectF, project_visible(), project_visible_many(), Handle, ndarray, QColor, QFont (+23 more)

### Community 121 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 122 - "ArmatureStore"
Cohesion: 0.18
Nodes (4): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 123 - "PointEdit"
Cohesion: 0.14
Nodes (9): _pull_point(), _push_point(), _AxisBox, PointEdit, QDoubleSpinBox, QWidget, Three boxes for one point in space. Keyboard tracking is off, so a typed number…, Match the arrows to the size of the thing being moved. (+1 more)

### Community 124 - "_tab_switch"
Cohesion: 0.29
Nodes (7): The show/hide switch on the tab named ``title``, if it has one., Stacked behind another panel is where the switch is worth the most., It is fifteen pixels wide and carries no words, which is exactly the shape the…, _tab_switch(), test_a_panel_that_draws_nothing_gets_no_switch_on_its_tab(), test_a_tabbed_panel_still_shows_its_switch(), test_clicking_the_switch_on_a_tab_works()

### Community 125 - "Reflow"
Cohesion: 0.30
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 126 - "._carrying_a_copy"
Cohesion: 0.16
Nodes (7): opens_as(), Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model., What a file would open as -- ``"model"``, ``"session"`` or ``"matcap"`` -- by…, parametrize, test_a_file_is_known_by_its_suffix()

### Community 127 - "CHANGELOG.md"
Cohesion: 0.25
Nodes (7): Shift-snapped orbiting (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding

### Community 128 - "Preferences"
Cohesion: 0.11
Nodes (19): Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, Back to how the application ships., An external drive that is not plugged in is not an empty gallery., The font size is a string; everything beside it still arrives., test_a_field_from_a_later_version_is_ignored(), test_a_matcap_folder_that_has_gone_falls_back_to_the_bundled_ones() (+11 more)

### Community 129 - "._sync_scene"
Cohesion: 0.12
Nodes (6): Regenerate the pedestal and the cut contour when their settings move. Both are…, The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on., Cut the mesh with each section plane and expand the result to strokes.

### Community 130 - "Stage"
Cohesion: 0.17
Nodes (9): The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, The line burned into the corner of the frame for ``stage``. Counted off the…, QImage, One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A… (+1 more)

### Community 131 - "MarkerVisibility"
Cohesion: 0.18
Nodes (5): MarkerVisibility, Cache surface occlusion by view and position for every kind of marker. The…, Whether the last pass is recent enough to be read instead of repeated., Mark these points as standing in front of the surface, untested. For frames…, Answer for a batch of points at once, ahead of being asked one by one. Every…

### Community 132 - "ExportLook"
Cohesion: 0.09
Nodes (17): ExportLook, What the frames are to look like, as against what they are of. Laid over the…, Which of the things drawn over the model belong in the frames., ``base`` with this export's choices laid over it., app(), FakeViewport, fixture, QImage (+9 more)

### Community 134 - "preview"
Cohesion: 0.40
Nodes (5): app(), preview(), fixture, One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "orientation.py"
Cohesion: 0.33
Nodes (5): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis

### Community 136 - "palette.py"
Cohesion: 0.13
Nodes (16): The small controls that are not sliders: a swatch, and a point in space., css(), outline(), QColor, The colours the hand-drawn elements paint with. Kept apart from…, Draw the hairline that separates a control from the panel. One line, the same…, A colour as a style sheet function, for the parts Qt draws., Change the one colour that is not grey, everywhere at once. The hand-painted… (+8 more)

### Community 137 - "plane_count"
Cohesion: 0.12
Nodes (12): _along(), lattice_fineness(), plane_count(), Where a detail setting sits on its slider, 0 to 1., How much finer than usual a detail setting asks the lattice to be. One at the…, How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., How much of a turn in the surface one plane covers, in degrees. Linear in…, How many planes a mode fitted to the model keeps. The climb from two planes to… (+4 more)

### Community 138 - "watch_keys"
Cohesion: 0.15
Nodes (14): can_take_key(), is_hotkey_click(), KeyGesture, QObject, QWidget, The gesture that puts a key on a control: Ctrl/Cmd, Alt and a click. It sits…, Whether a mouse press is the assignment gesture rather than a click., Whether a widget is the kind a key can sensibly be put on. A button or a switch… (+6 more)

### Community 139 - "._apply"
Cohesion: 0.24
Nodes (5): Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Slot that writes one field of the contour shading settings.

### Community 140 - "_drag_over"
Cohesion: 0.22
Nodes (10): _drag_over(), _middle_of_the_view(), A drag of ``holder`` arriving at ``point`` in the window's coordinates. A real…, The gesture the whole thing rests on: drag it onto the model, it goes., A gesture that destroys something only fires where it clearly meant to., Refused at the door it would never reach the model; so it is let in., test_a_copy_dropped_on_the_model_is_thrown_away(), test_a_copy_is_let_into_the_window_wherever_it_arrives() (+2 more)

### Community 141 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 142 - "paths.py"
Cohesion: 0.26
Nodes (13): available_matcaps(), _bundled_root(), image_path(), matcap_dir(), model_dir(), Path, Locations of the bundled resources. ``REFVIEW_RESOURCES`` overrides the search,…, Return PyInstaller's extracted application directory when frozen. (+5 more)

### Community 143 - "Command"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 144 - ".mouseMoveEvent"
Cohesion: 0.17
Nodes (5): Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Apply the pull live, so the figure moves under the cursor., Apply the drag live, so the clay re-forms under the cursor.

### Community 145 - ".split_point"
Cohesion: 0.20
Nodes (9): BoneRef, _project(), The nearest bone under the cursor, for showing its length., Where on a bone a click at ``(x, y)`` landed. The share along the bone is read…, A world point in widget pixels, or ``None`` when it is behind the camera., How far along a screen-space segment the cursor's nearest point lies., Pixels from the cursor to the segment, or ``None`` if either end is behind., _segment_distance() (+1 more)

### Community 146 - "ReplaceItems"
Cohesion: 0.13
Nodes (7): Any, Command, Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems, test_replace_items_covers_bulk_edits()

### Community 147 - "session.py"
Cohesion: 0.27
Nodes (9): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Persisted viewer state: camera, shading, measurements and bookmarks. (+1 more)

### Community 148 - "FormStore"
Cohesion: 0.15
Nodes (5): FormStore, An ordered, named collection of forms, like the other stores., The live list; the undo commands operate on it directly., A name for a new form of this recipe, numbered past any it already has. A form…, test_a_form_store_names_forms_past_the_ones_it_has()

### Community 149 - "WholeFaceToggles"
Cohesion: 0.29
Nodes (4): QObject, Making the whole of a switch the part you can press. The theme turns every…, Turns a press anywhere on a switch into a click on it., WholeFaceToggles

### Community 150 - "Session"
Cohesion: 0.27
Nodes (8): Path, A snapshot of everything worth keeping between runs., Session, test_the_settings_survive_a_session_and_an_older_file_has_them_by_default(), test_a_posed_skeleton_survives_a_session_round_trip(), test_an_old_session_has_no_skeletons(), test_old_sessions_without_relief_fields_load_with_defaults(), test_skin_session_roundtrip_and_old_defaults()

### Community 152 - "navigation.py"
Cohesion: 0.22
Nodes (6): DragMode, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Start a drag, resolving the orbit pivot from the cursor position.

### Community 153 - ".update_enabled"
Cohesion: 0.22
Nodes (6): Hold the settings a recording is built from still while it runs. A film is a…, Show what this way of working needs, and put the rest away. A setting that does…, The line under the normals slider: what the setting has asked for., The bones of the chosen armature, in the order the clay goes down. Every intact…, What can be done to the list, given where the handle is and whether a film is…, _summary()

### Community 154 - "restored"
Cohesion: 0.29
Nodes (7): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., A window with the saved layout out of the way, and put back after. Shown,…, A second window, built from a layout the first one saved. The point is…, restored(), window()

### Community 156 - "viewport.py"
Cohesion: 0.08
Nodes (25): Freehand annotations painted onto the model surface. A stroke is a polyline of…, MeasurementSettings, Named point-to-point measurements and their presentation options., How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., Painting annotations onto the model surface. Every shape is laid down the same…, Qt user interface: the viewport widget, the panels and the main window., DepthDrag (+17 more)

### Community 158 - "._chosen_armature"
Cohesion: 0.28
Nodes (5): QListWidgetItem, The armature the clay is being built on, or ``None``. An index past the end of…, Take lengths of wire out of the clay, or put them back. A tick on a row that…, Put the clay on all of the wire, or take it off all of it., Write which lengths of wire take clay, as one undoable step.

### Community 159 - ".install"
Cohesion: 0.29
Nodes (6): QApplication, Put the rule in place for every switch in the application., The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter., test_a_switch_answers_a_press_anywhere_on_its_face(), test_alt_is_left_alone_so_a_switch_can_still_be_copied()

### Community 160 - "coarse_lattice"
Cohesion: 0.33
Nodes (6): app(), coarse_lattice(), fixture, MonkeyPatch, One Qt application for the whole run; offscreen, so CI needs no display.…, Read every model on a small lattice, so the suite stays quick.

### Community 161 - "TriangleIndex"
Cohesion: 0.29
Nodes (6): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., Leaf bounding boxes over a Morton-sorted triangle list., TriangleIndex, test_an_empty_index_returns_no_candidates()

### Community 162 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 163 - ".update_enabled"
Cohesion: 0.17
Nodes (6): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., Follow the highlighted row, without rebuilding the list underneath it. Going…, Highlight the row for a node picked in the view., Highlight the row for a landmark picked in the view.

### Community 164 - "Human Skin renderer"
Cohesion: 0.33
Nodes (5): Human Skin renderer, Material and transport, Scheduling, precision and compatibility, Surface, Where to change it

### Community 165 - "test_spatial.py"
Cohesion: 0.26
Nodes (11): _grid(), The picking accelerator: it must be fast without changing any answer., A bumpy height field, so rays hit different triangles at different depths., The pruned candidate set must never miss the true intersection., Every parent must enclose its children, or a ray could slip past a leaf., test_a_batch_of_rays_gets_the_same_candidates_as_one_at_a_time(), test_a_ray_that_misses_the_model_is_pruned_away(), test_every_triangle_lands_in_exactly_one_leaf() (+3 more)

### Community 166 - ".refresh_list"
Cohesion: 0.22
Nodes (5): QTreeWidgetItem, The landmarks in the preset's own order, top of the figure down. Placement…, Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing., Commit a renamed or re-checked row, if anything actually changed.

### Community 167 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 168 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 169 - "._build"
Cohesion: 0.33
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 170 - "_height_of"
Cohesion: 0.40
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 171 - "_file_drag"
Cohesion: 0.40
Nodes (5): _file_drag(), A file being dragged over the middle of the view, as ``kind`` of event., Entering, moving and dropping: a drop lands only where the move before it was…, test_a_file_the_window_cannot_open_is_refused_on_the_way_past(), test_a_model_file_is_welcome_at_every_step_of_its_drag()

### Community 172 - "generate_matcaps.py"
Cohesion: 0.32
Nodes (7): Color, main(), _normalize(), ndarray, Path, Render the bundled matcap set. Each preset is evaluated analytically over the…, save()

### Community 173 - "._build"
Cohesion: 0.39
Nodes (4): QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 174 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 175 - "test_the_switch_on_a_dock_bar_is_the_panels_own_visibility"
Cohesion: 0.67
Nodes (3): parametrize, test_a_panel_that_draws_nothing_has_no_switch(), test_the_switch_on_a_dock_bar_is_the_panels_own_visibility()

### Community 176 - "quad"
Cohesion: 0.67
Nodes (3): fixture, quad(), Two triangles covering the unit square on the z = 0 plane.

### Community 179 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 182 - "skin_detail.py"
Cohesion: 0.11
Nodes (26): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section(), burley_marginal(), burley_profile(), cellular() (+18 more)

### Community 187 - "wakelock.py"
Cohesion: 0.33
Nodes (4): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version(), Keeping the machine awake while the viewer is the window in front. An artist…

### Community 188 - "._commit_node_drag"
Cohesion: 0.33
Nodes (3): Record the finished gesture: a move, a resize, or a plain click. A press that…, Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…

### Community 190 - "_clamp"
Cohesion: 0.50
Nodes (4): _clamp(), What the 3D view costs the machine., Pull anything out of range back into it. The window cannot produce these…, ViewportPreferences

### Community 191 - "Cloner"
Cohesion: 0.50
Nodes (4): Cloner, How to make, drive and refresh a copy of one kind of control., Teach the copier about a kind of control., register_cloner()

### Community 195 - "section"
Cohesion: 0.50
Nodes (4): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., section()

### Community 196 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

## Knowledge Gaps
- **5 isolated node(s):** `refview`, `Surface`, `Material and transport`, `Scheduling, precision and compatibility`, `Where to change it`
  These have ≤1 connection - possible missing edges or undocumented components.
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `Stage`, `plane_axes.py`, `settings.py`, `ExportLook`, `Joint`, `SceneRenderer`, `convex.py`, `_wires`, `mesh_io.py`, `ViewerState`, `Skeleton`, `FormStore`, `test_forms.py`, `SectionSettings`, `plane_volume.py`, `viewport.py`, `PlaneSettings`, `TriangleIndex`, `test_plane_clusters.py`, `test_spatial.py`, `SurfacePicker`, `Wires`, `gltf_loader.py`, `ExportVideoDialog`, `quad`, `plane_clusters.py`, `PrimaryForm`, `test_skeleton.py`, `Solid`, `FormTool`, `load_obj`, `test_plane_solids.py`, `PoseTool`, `MeshBuffers`, `Bounds`, `raycast_mesh`, `test_forms_panel.py`, `core/__init__.py`, `obj_loader.py`, `OrientationSettings`, `test_skin.py`, `load_mesh`, `Skin`, `Rig`, `Hit`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `._sync_scene`, `Stage`, `ExportLook`, `._place_form_landmark`, `MainWindow`, `main_window.py`, `ViewerState`, `.mouseMoveEvent`, `skin_refinement.py`, `navigation.py`, `viewport.py`, `film_export.py`, `SurfacePicker`, `Wires`, `ExportVideoDialog`, `PrimaryForm`, `FilmExport`, `ArmatureTool`, `._buried_nodes`, `._commit_node_drag`, `MeasureTool`, `._place_joint`, `FormTool`, `._export_surface`, `._scene_center`, `PoseTool`, `NavigationController`, `_Encoder`, `._picker`, `AnnotateTool`, `.mouseReleaseEvent`, `._place_armature_node`, `ViewportOverlay`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `ValueSlider` connect `ValueSlider` to `Link`, `clone.py`, `load_obj`, `Frame`, `palette.py`, `main_window.py`, `QWidget`, `Cloner`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `OverlayParts`) actually correct?**
  _`ViewerState` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._