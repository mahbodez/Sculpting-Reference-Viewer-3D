# Graph Report - reference-viewer  (2026-09-15)

## Corpus Check
- 138 files · ~454,707 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4583 nodes · 10257 edges · 181 communities (167 shown, 14 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 481 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `20ea8927`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SettingsWindow
- test_preferences.py
- update_check.py
- Viewport
- Mesh
- main_window.py
- MainWindow
- Stroke
- GifWriter
- camera.py
- RenderSettings
- plane_solids.py
- elements/__init__.py
- _derived
- Armature
- ShadingMode
- ViewerState
- PlaneSettings
- framebuffer.py
- CameraPanel
- UpdateChecker
- ShaderProgram
- QPointF
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- Writer
- SectionSettings
- ndarray
- ControlsWindow
- TriangleIndex
- ShadingPanel
- ball
- test_camera.py
- test_plane_clusters.py
- WakeLock
- MatcapPreview
- FormTool
- CustomPanel
- film_export.py
- viewport.py
- Camera
- Bone
- ValueSlider
- mesh.py
- ExportVideoDialog
- open_writer
- landmarks.py
- Agent Graph-First Instructions
- VideoSettings
- settings.py
- test_matcap_preview.py
- test_armature.py
- test_forms.py
- OrientationSettings
- HotkeyMap
- FilmExport
- FormsPanel
- PlanesPanel
- forms.py
- ArmatureTool
- Workspace
- ui/hotkeys.py
- Solid
- application.py
- MeasureTool
- Link
- PrimaryForm
- AddItem
- obj_loader.py
- AnnotatePanel
- test_plane_solids.py
- _wires
- session.py
- KeyBox
- MeshBuffers
- load_matcap_pixels
- test_custom_panels.py
- test_hotkeys.py
- core/preferences.py
- test_contour_shading.py
- NavigationController
- core/__init__.py
- plane_count
- test_forms_panel.py
- raycast_mesh
- HotkeyBinder
- convex.py
- MatcapPanel
- ColorButton
- Frame
- _Encoder
- ._picker
- test_elements.py
- mesh_renderer.py
- FormRun
- ReflowLayout
- Measurement
- ArmaturePanel
- SceneRenderer
- clone.py
- ._sync_scene
- Path
- clay_lumps
- .mouseReleaseEvent
- test_panel_docks.py
- ._menu_action
- ._place_armature_node
- test_mesh_io.py
- Release
- DockTitle
- test_reflow.py
- MatcapSettings
- plane_volume.py
- Preferences
- ._build
- test_open_files.py
- OpenRequests
- FormStore
- SetAttributes
- ViewportOverlay
- release.yml
- block_splits
- .stage_images
- _tab_switch
- Reflow
- ._carrying_a_copy
- ._advance_pending
- PreferenceStore
- test_navigation.py
- ._buried_nodes
- OverlayParts
- ExportLook
- ._place_form_landmark
- preview
- armature.py
- palette.py
- stone_field
- box
- SectionGizmo
- _drag_over
- .mouseMoveEvent
- .image
- fixture
- _shifts
- parametrize
- union_field
- carve
- test_a_session_saved_without_panels_leaves_the_ones_open_alone
- .install
- coarse_lattice
- test_resetting_the_layout_puts_the_docks_back_at_once
- ._turn
- ui/preferences.py
- restored
- test_resetting_keeps_the_panels_built_by_hand
- test_a_panel_does_not_cover_its_own_title
- test_the_switch_is_not_squeezed_to_nothing
- test_a_panel_can_be_taken_away_and_another_built_after_a_restore
- test_loading_a_session_over_a_restored_layout_survives
- test_the_dock_of_a_panel_taken_away_is_used_again
- test_a_reused_dock_does_not_bring_the_old_panels_contents_with_it
- .column_of
- ._build
- sample_count
- Wires
- ._rename_point
- coarse_lattice
- environment.yml
- mirror_landmarks
- _height_of
- _file_drag
- .pan
- app
- kept_off
- _wire_frame
- .new_armature
- scrollable
- app
- app
- .ortho_half_height

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 147 edges
2. `Viewport` - 118 edges
3. `Camera` - 86 edges
4. `MainWindow` - 84 edges
5. `ViewerState` - 80 edges
6. `PrimaryForm` - 79 edges
7. `Armature` - 74 edges
8. `PlaneSettings` - 67 edges
9. `FormsPanel` - 63 edges
10. `ArmaturePanel` - 62 edges

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

## Communities (181 total, 14 thin omitted)

### Community 0 - "SettingsWindow"
Cohesion: 0.15
Nodes (11): The preferences as they stand. Treat as read-only; use :meth:`set`., QWidget, Fill in the groups. A switch with nothing to put in the caption column is given…, Every command with its keys, each key a box that takes one keystroke. The list…, The one button that is not a preference, and what the window is for., Say what the view is really drawing with, beside what was asked for. A sample…, Put one field back into the store, which applies and saves it., Pull every control back into line with the store. Run when the window is built,… (+3 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.10
Nodes (19): What the artist prefers: kept apart from the document, and acted upon. Two…, An external drive that is not plugged in is not an empty gallery., Windows that clean up after themselves, and a settings file that does., A session is not the only thing worth carrying on from., Otherwise the marks from one piece of work arrive on top of another., test_a_matcap_folder_that_has_gone_falls_back_to_the_bundled_ones(), test_a_remembered_file_that_has_gone_is_passed_over(), test_a_saved_session_beats_the_model_it_was_saved_from() (+11 more)

### Community 2 - "update_check.py"
Cohesion: 0.14
Nodes (22): check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed). (+14 more)

### Community 3 - "Viewport"
Cohesion: 0.07
Nodes (14): QOpenGLWidget, Slide the view so a point sits at the centre, keeping the angle., A form changed: work its clay out again and redraw., Slide the view so a measurement sits at the centre, keeping the angle., End any film being recorded, and wait for its thread to really stop. For…, The document being drawn., The film of the form's making, as far as it has been recorded., Whether frames are being rendered out of a film right now. (+6 more)

### Community 4 - "Mesh"
Cohesion: 0.08
Nodes (35): flat_mesh(), A flat-shaded mesh, every triangle with its own three corners. Corners are not…, A mesh from ``(n, 3, 3)`` triangle corners, shaded flat per triangle., Mesh, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, plane_axes(), Split the mesh's normals into planes, keeping every count on the way. (+27 more)

### Community 5 - "main_window.py"
Cohesion: 0.05
Nodes (61): QIcon, The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, MatcapLoadError, RuntimeError, Matcap texture loading and upload, and the small data table beside it., Raised when an image cannot be used as a matcap., framed() (+53 more)

### Community 6 - "MainWindow"
Cohesion: 0.05
Nodes (19): MainWindow, QMainWindow, Open an empty panel of the artist's own and bring it to the front., Put the docks and the hand-built panels back where they were. Unless the artist…, Put the panels back where they started, now., Follow the machine's sleep to whether this window is in front., Wires the viewport, the panels and the document together., Give each panel a dock of its own, tabbed together on the right. Each panel can… (+11 more)

### Community 7 - "Stroke"
Cohesion: 0.07
Nodes (35): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+27 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "camera.py"
Cohesion: 0.13
Nodes (20): Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., look_at(), normalize(), orthographic() (+12 more)

### Community 10 - "RenderSettings"
Cohesion: 0.10
Nodes (21): Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, normal_matrix(), ndarray, Replace the section contour, prepared by the caller as stroke vertices., Replace the depth guide: stroke vertices fading about ``centre``. Empty…, Everything in the frame, into whichever framebuffer is bound. (+13 more)

### Community 11 - "plane_solids.py"
Cohesion: 0.09
Nodes (36): auto_smooth(), A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, planes_for(), The stages a form passes through on its way from a block to a figure. The…, How many solids each stage of a film is made of. Every count from the coarsest…, The detail setting that asks for ``solids``, or ``None`` if none does. The…, Work the form stage by stage, handing each one back as it is finished. A…, A stage as it is to be drawn, with its normals read at ``smooth``. Kept out of… (+28 more)

### Community 12 - "elements/__init__.py"
Cohesion: 0.06
Nodes (50): Make every control under ``root`` that can be copied Alt-draggable. A group is…, watch_tree(), make_switch(), One dock per panel, with a bar of its own across the top. Every panel is its…, The square that shows or hides what a panel draws. One is kept on each dock's…, The widgets the panels are built out of, and the rules they follow. Four ideas,…, can_take_key(), is_hotkey_click() (+42 more)

### Community 13 - "_derived"
Cohesion: 0.09
Nodes (25): _kept_laying(), Fresh bones, laid the way the armature was already laying them. The bone list…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _derived(), A guess the artist corrects is theirs, and the mirror leaves it alone., The new list is the edit; the old one has to survive to be undone to., Hips, then the ribcage, then the head, then the limbs largest first. This order… (+17 more)

### Community 14 - "Armature"
Cohesion: 0.04
Nodes (34): Armature, ArmatureStore, ndarray, Point3, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, Every node position as ``(n, 3)``., The two points a bone runs between, or ``None`` if it dangles. (+26 more)

### Community 15 - "ShadingMode"
Cohesion: 0.08
Nodes (23): High Quality shading mode (1.1.0), Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command, High Quality without ray tracing, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter (+15 more)

### Community 16 - "ViewerState"
Cohesion: 0.08
Nodes (21): Command, Path, QObject, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements, annotations,… (+13 more)

### Community 17 - "PlaneSettings"
Cohesion: 0.04
Nodes (61): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, Holds the working state between one turn of the sliders and the next.…, The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache, PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor… (+53 more)

### Community 18 - "framebuffer.py"
Cohesion: 0.07
Nodes (18): AccumTarget, ColorTarget, DepthTarget, FrameTarget, GeometryTarget, Offscreen render targets used by the high-quality, ghost and smoothing passes.…, A depth-only framebuffer, sampled afterwards as a texture., ``clamp_to_lit`` makes everything outside the map read as unshadowed. (+10 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): CameraPanel, QListWidgetItem, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 21 - "ShaderProgram"
Cohesion: 0.11
Nodes (10): OpenGL rendering layer: shader programs, textures and the scene renderer., Fill the shader's table with a level, if it is not already in it., ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform… (+2 more)

### Community 22 - "QPointF"
Cohesion: 0.39
Nodes (6): QPointF, draw_rail(), One marker object for endpoints, nodes, landmarks and tool previews., The screen-space cue for one degree of freedom. A vertical rail that fades out…, VisualMarker, test_shared_marker_styles_and_depth_guide_paint()

### Community 23 - "test_planes_panel.py"
Cohesion: 0.07
Nodes (25): app(), _names(), panel(), fixture, The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as… (+17 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.10
Nodes (12): MeasurePanel, _NameOnlyDelegate, QStyledItemDelegate, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing… (+4 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.13
Nodes (7): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., test_bookmarks_cycle_and_wrap()

### Community 26 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 27 - "SectionSettings"
Cohesion: 0.07
Nodes (32): Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, The direction the section plane faces. (+24 more)

### Community 28 - "ndarray"
Cohesion: 0.13
Nodes (21): _back_inside(), dual_contour(), _flat_mesh(), ndarray, The surface where ``value`` changes sign, one vertex per lattice cell. Each…, The gradient of a lattice field, by central differences. Which is the direction…, Drop the loose pieces, keeping the form and anything of its size. A block is a…, Read lattice fields at places between their corners, straight-line. Nearest-… (+13 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "TriangleIndex"
Cohesion: 0.09
Nodes (28): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Box the leaves up, coarsest level first and the leaves themselves last., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the… (+20 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.13
Nodes (13): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Slot that writes one field of the contour shading settings., Freeze the slices the way the camera faces now. The view direction is the one…, Show what this mode is actually lit and shaded by, and hide the rest. A matcap… (+5 more)

### Community 32 - "ball"
Cohesion: 0.05
Nodes (44): QThread, Film, A whole making, from the coarsest stage to the one the slider asks for. Held by…, FilmRecorder, QObject, The film being recorded, or the last one finished., Whether a film is being made right now., The film already held for ``key``, if there is one. (+36 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (8): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_serialisation_round_trip(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (58): angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What… (+50 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (32): c_void_p, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., Holds sleep off while the window that owns it is the one in front. The class… (+24 more)

### Community 36 - "MatcapPreview"
Cohesion: 0.09
Nodes (15): _clone_preview(), MatcapPreview, _pull_preview(), _push_preview(), QSize, QWidget, A matcap on a sphere, which is also how the matcap is graded., Point the preview at the settings it edits. The object itself, not a copy: this… (+7 more)

### Community 37 - "FormTool"
Cohesion: 0.08
Nodes (26): FormLandmarkRef, FormSettings, How the forms are drawn, and how their landmarks are placed., FormTool, ndarray, Every landmark the walk will ask for under these choices. With mirroring on,…, The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now. For a freeform, the one… (+18 more)

### Community 38 - "CustomPanel"
Cohesion: 0.07
Nodes (26): carried(), in_flight(), The id of what a copy copies, or an empty string., Read a drag's payload back, or ``None`` if it is not one of ours., source_of(), CustomPanel, _detach(), QFormLayout (+18 more)

### Community 39 - "film_export.py"
Cohesion: 0.08
Nodes (17): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+9 more)

### Community 40 - "viewport.py"
Cohesion: 0.04
Nodes (62): AnnotateMode, AnnotationSettings, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a… (+54 more)

### Community 41 - "Camera"
Cohesion: 0.08
Nodes (17): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Rays through a batch of pixels, as ``(origins, unit directions)``, ``(N, 3)``…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Project ``(N, 3)`` world points to ``(xs, ys, ndc_depths)`` in widget pixels. (+9 more)

### Community 42 - "Bone"
Cohesion: 0.07
Nodes (31): BoneRef, ArmatureNode, Bone, The graph with ``node`` appended, optionally joined to an existing one., The graph with a node dropped into the middle of a bone. The bone becomes two,…, One joint of the wire: where it is, and how thick the form is there., A length of wire between two nodes, by their index in the armature. A bone…, Preset (+23 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (12): _clone_slider(), _pull_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end., Set the value the way a hand on the control would. (+4 more)

### Community 44 - "mesh.py"
Cohesion: 0.06
Nodes (54): Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, STL and glTF import (1.1.0), Units are adopted, never guessed (+46 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.10
Nodes (13): QProgressDialog, even(), ExportVideoDialog, Path, QDialog, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the…, What the frames are to look like, as the controls have it. (+5 more)

### Community 46 - "open_writer"
Cohesion: 0.08
Nodes (28): _encode_arguments(), _encoders(), ffmpeg_path(), _FFmpegWriter, _no_window(), open_writer(), Path, RuntimeError (+20 more)

### Community 47 - "landmarks.py"
Cohesion: 0.14
Nodes (23): _Build, _build_arm(), build_humanoid(), _build_leg(), _build_torso(), _humanoid_bones(), _humanoid_landmarks(), _mid() (+15 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "VideoSettings"
Cohesion: 0.18
Nodes (7): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, TestTiming

### Community 50 - "settings.py"
Cohesion: 0.03
Nodes (75): Coefficients, _empty(), PlaneAxes, PlaneSet, ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, One level of a fit: the planes the shader is to quantise against. A plane is a…, A level with no place in it: nearest direction wins, as before. (+67 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.11
Nodes (30): QPoint, _drag(), parametrize, The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc., Dragging further than the range goes is not a negative gamma., Alt and a drag copies a control; the disc must not swallow that. (+22 more)

### Community 52 - "test_armature.py"
Cohesion: 0.07
Nodes (53): _chain(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other., The femoral head is in from the ASIS, below it and behind it, by shares of the…, A wire in two halves is not an armature anybody could bend., Version 4 files predate the armature; they open with an empty one. (+45 more)

### Community 53 - "test_forms.py"
Cohesion: 0.08
Nodes (34): merged(), The hull of the points with its faces bowed out; see :func:`rounded_hull`., Several flat meshes as one, or ``None`` when there is nothing to draw., _closed(), _inside(), _marks(), ndarray, The forms: convex solids, the landmarks that build them, the walk, and the… (+26 more)

### Community 54 - "OrientationSettings"
Cohesion: 0.09
Nodes (24): OrientationSettings, Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., UpAxis (+16 more)

### Community 55 - "HotkeyMap"
Cohesion: 0.07
Nodes (19): Command, HotkeyMap, Any, Which keys do what, as the artist has decided rather than as it ships. A hotkey…, Whether the artist has moved this command off what it ships with., Which command has these keys, if any., Every command with keys on it, declared or not, as id -> keys., Put ``keys`` on a command, taking them off whatever had them. Returns the id of… (+11 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (11): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+3 more)

### Community 57 - "FormsPanel"
Cohesion: 0.06
Nodes (22): FormsPanel, Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., The freeform the highlighted row belongs to, when no run is on., Take back the landmark before this one and ask for it again., Take back the last landmark a freeform was given, guess and all., Ready the landmark the next click lays down, from the name and side boxes. (+14 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.08
Nodes (22): PlanesPanel, QListWidgetItem, Lay one length of wire earlier or later, as one undoable step., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Show what this way of working needs, and put the rest away. A setting that does… (+14 more)

### Community 59 - "forms.py"
Cohesion: 0.06
Nodes (44): DegenerateHullError, The points are flat, collinear or too few to hold any volume., build_freeform(), _centre(), form_spec(), FormFill, FormPreset, FormStage (+36 more)

### Community 60 - "ArmatureTool"
Cohesion: 0.06
Nodes (39): LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, Handle, Begin a preset run against an armature already in the store., The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now. (+31 more)

### Community 61 - "Workspace"
Cohesion: 0.06
Nodes (25): QTabBar, _number_in(), QMainWindow, QObject, QSettings, QWidget, Keep every switch agreeing with the panel it speaks for., Hang a show/hide switch on every dock tab that wants one. A dock stacked behind… (+17 more)

### Community 62 - "ui/hotkeys.py"
Cohesion: 0.11
Nodes (23): control_of(), decorate(), describe(), forget(), group_of(), HotkeyStore, listed(), QObject (+15 more)

### Community 63 - "Solid"
Cohesion: 0.09
Nodes (42): One convex piece of a form: its hull vertices and outward-wound faces., The longest side of the box the solid sits in., Whether a point lies inside, or within ``slack`` of the surface., Solid, _across(), blend_rings(), build_head(), build_pelvis() (+34 more)

### Community 64 - "application.py"
Cohesion: 0.08
Nodes (35): ArgumentParser, Namespace, QSplashScreen, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font(), main() (+27 more)

### Community 65 - "MeasureTool"
Cohesion: 0.22
Nodes (4): MeasureTool, Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview.

### Community 66 - "Link"
Cohesion: 0.11
Nodes (10): CloneGesture, Link, _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original., Whether the copy is being used right now and must not be written. (+2 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.07
Nodes (56): PlacedLandmark, One anatomical point the artist put on the model during a guided run., build_form(), built_count(), form_landmark_title(), form_mesh(), landmark_signature(), median_plane_ready() (+48 more)

### Community 68 - "AddItem"
Cohesion: 0.07
Nodes (28): Camera motion is deliberately not undoable, AddItem, Command, Append an item to a document list., Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems (+20 more)

### Community 69 - "obj_loader.py"
Cohesion: 0.11
Nodes (29): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic(), load_obj(), ObjLoadError (+21 more)

### Community 70 - "AnnotatePanel"
Cohesion: 0.20
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 71 - "test_plane_solids.py"
Cohesion: 0.04
Nodes (81): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), block(), dumbbell(), edge_use(), flatness() (+73 more)

### Community 72 - "_wires"
Cohesion: 0.11
Nodes (29): The order the artist put the bones in is what the scrub walks through, which is…, The claim the whole film rests on, asked again with an armature under it: an…, test_a_film_of_clay_on_a_wire_lays_it_down_in_the_order_it_was_listed(), test_the_last_stage_of_a_film_on_a_wire_is_the_form_the_slider_gives(), _bar(), _holds(), A long ellipsoid: one closed form with an obvious axis to lie along., Whether a fitted solid has a point inside it. (+21 more)

### Community 73 - "session.py"
Cohesion: 0.08
Nodes (28): Named camera positions the artist can jump between while sculpting., _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``. (+20 more)

### Community 74 - "KeyBox"
Cohesion: 0.10
Nodes (16): QKeySequenceEdit, assign(), HotkeyDialog, KeyBox, normalize(), press(), QDialog, QWidget (+8 more)

### Community 75 - "MeshBuffers"
Cohesion: 0.07
Nodes (14): MeshBuffers, Whichever geometry is standing for the model this frame., Replace the annotation geometry; pass an empty list to hide it., Vertex/index buffers for one mesh, bound through a single VAO., A single vertex buffer holding every visible stroke., StrokeBuffers, DataTexture, default_matcap_pixels() (+6 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.15
Nodes (23): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+15 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.05
Nodes (30): Cross-section tool (1.1.0), QMimeData, Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel (+22 more)

### Community 78 - "test_hotkeys.py"
Cohesion: 0.11
Nodes (23): QKeySequence, app(), _map(), fixture, Hotkeys: the map, the store, the binder, and the gesture that assigns one., One offscreen Qt application for the run; see test_film_recorder., End to end: the filter is on the panel's buttons and the window hears it., A key given to something else comes off what had it, and the map says what that… (+15 more)

### Community 79 - "core/preferences.py"
Cohesion: 0.12
Nodes (18): _as_kind_of(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any, What the artist prefers, as distinct from what the document says. There are two… (+10 more)

### Community 80 - "test_contour_shading.py"
Cohesion: 0.29
Nodes (5): parametrize, The contour shading mode: slices across the form, read off it like a map., test_a_custom_direction_is_normalised_and_an_empty_one_falls_back(), test_the_density_floor_keeps_the_spacing_finite(), test_the_slices_face_the_way_that_was_asked()

### Community 81 - "NavigationController"
Cohesion: 0.08
Nodes (18): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Degrees of yaw per pixel, signed by whether the drag is inverted. (+10 more)

### Community 82 - "core/__init__.py"
Cohesion: 0.07
Nodes (30): Shift-snapped orbiting (1.1.0), Qt-free geometry, camera and document model for the reference viewer., Bounds, _gathered(), ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Which group each of ``total`` things lands in, given pairs that agree. Hooking… (+22 more)

### Community 83 - "plane_count"
Cohesion: 0.12
Nodes (12): _along(), lattice_fineness(), plane_count(), Where a detail setting sits on its slider, 0 to 1., How much finer than usual a detail setting asks the lattice to be. One at the…, How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., How much of a turn in the surface one plane covers, in degrees. Linear in…, How many planes a mode fitted to the model keeps. The climb from two planes to… (+4 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.11
Nodes (30): app(), _click(), panel(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The… (+22 more)

### Community 85 - "raycast_mesh"
Cohesion: 0.11
Nodes (29): _cross(), Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Row-wise cross product, without :func:`numpy.cross`'s axis shuffling., Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface. (+21 more)

### Community 86 - "HotkeyBinder"
Cohesion: 0.13
Nodes (15): QShortcut, ask_for(), HotkeyBinder, Command, QAction, Turns the map into the shortcuts of one window, and keeps them current., A menu entry. Its keys are heard anywhere in the window and shown in the menu., A key heard only while the view has the focus. The menu entry for it, if there… (+7 more)

### Community 87 - "convex.py"
Cohesion: 0.14
Nodes (19): convex_hull(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, The outward unit normal at each vertex: the area-weighted mean of its faces'. A…, The barycentric ``(w, u, v)`` of an even grid over a triangle., The hull of the points with every face bowed out into a cubic patch. A flat… (+11 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.15
Nodes (10): MatcapPanel, Rebuild the thumbnail list from the resources folder., The disc was dragged: show the renderer and the numbers what it did., A different matcap: the disc draws whichever one is on the model., Put the numbers back in line with the settings, and redraw the disc. Separate…, Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, It is the panel's main control; a click on a bar must not take it away. (+2 more)

### Community 89 - "ColorButton"
Cohesion: 0.07
Nodes (19): _clone_point(), _clone_swatch(), _pull_point(), _pull_swatch(), _push_point(), _push_swatch(), _AxisBox, ColorButton (+11 more)

### Community 90 - "Frame"
Cohesion: 0.07
Nodes (19): _pull_frame(), _push_frame(), Nothing: each row inside the copy is linked on its own., Frame, FrameBar, QFormLayout, QPainter, QSize (+11 more)

### Community 91 - "_Encoder"
Cohesion: 0.22
Nodes (6): Queue, _Encoder, QObject, QWidget, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 92 - "._picker"
Cohesion: 0.14
Nodes (7): ndarray, Rub out the stroke points under the eraser, live., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on., Take hold of a form's landmark, to move it or just to say which one it is.

### Community 93 - "test_elements.py"
Cohesion: 0.08
Nodes (21): app(), fixture, Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., A matcap has no light to aim, so the Light group goes -- and its space. The… (+13 more)

### Community 94 - "mesh_renderer.py"
Cohesion: 0.12
Nodes (17): Unit vector for an azimuth/elevation pair, with +Y as the pole., spherical_direction(), bind_default(), current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., Restore a framebuffer captured with :func:`current_framebuffer`., _ghost_depth_range(), key_world_direction() (+9 more)

### Community 95 - "FormRun"
Cohesion: 0.40
Nodes (3): FormRun, Begin a run against a form already in the store., A guided form part-way through.

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - "Measurement"
Cohesion: 0.12
Nodes (11): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+3 more)

### Community 98 - "ArmaturePanel"
Cohesion: 0.06
Nodes (22): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take back the landmark before this one and ask for it again., Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., Run a bone between the row selected now and the node held before it. (+14 more)

### Community 99 - "SceneRenderer"
Cohesion: 0.15
Nodes (8): Forget the contents without releasing the buffer objects., Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are…, Lay the offscreen frame over the screen, smoothed., Lay the summed ghost over the scene already in the frame., SceneRenderer

### Community 100 - "clone.py"
Cohesion: 0.06
Nodes (57): QAbstractButton, QComboBox, QLineEdit, QSlider, QSpinBox, _begin(), can_clone(), clone() (+49 more)

### Community 101 - "._sync_scene"
Cohesion: 0.12
Nodes (6): Regenerate the pedestal and the cut contour when their settings move. Both are…, The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on., Cut the mesh with each section plane and expand the result to strokes.

### Community 102 - "Path"
Cohesion: 0.13
Nodes (11): opens_as(), Path, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window., Open a file by what it is: a model, a session or a matcap. The one door every…, A path written down last time, if it is one and it is still there., What a file would open as -- ``"model"``, ``"session"`` or ``"matcap"`` -- by… (+3 more)

### Community 103 - "clay_lumps"
Cohesion: 0.16
Nodes (18): _box_facings(), clay_lumps(), clay_pieces(), fit_piece(), _frame(), grow_piece(), join_pieces(), Which three ways a lump of material runs. Columns, thinnest first. Thinnest… (+10 more)

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.11
Nodes (9): Record the finished drag as a single undo step., Record the finished gesture: a move, a resize, or a plain click. A press that…, Record the finished drag as one step, or read a press as a selection., Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…, Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Record the finished drag as one step, or read a press as a selection. (+1 more)

### Community 105 - "test_panel_docks.py"
Cohesion: 0.14
Nodes (3): Each panel in a dock of its own, and putting the docks back next time. Two…, test_a_restored_copy_drives_the_new_windows_own_control(), test_the_layout_comes_back_through_the_settings()

### Community 106 - "._menu_action"
Cohesion: 0.40
Nodes (4): _plain(), QAction, A menu entry's text as a name: no accelerator ampersand, no trailing dots., Add a menu entry, optionally with a window-wide shortcut. Given a ``command``…

### Community 107 - "._place_armature_node"
Cohesion: 0.22
Nodes (4): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…, The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…

### Community 108 - "test_mesh_io.py"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

### Community 109 - "Release"
Cohesion: 0.18
Nodes (12): The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, is_skipped(), QWidget, Background release check and the notice it puts in front of the artist. The…, Whether the artist already dismissed this exact version., Offer the release page, with the option never to be asked again. (+4 more)

### Community 110 - "DockTitle"
Cohesion: 0.08
Nodes (14): QDockWidget, QToolButton, DockTitle, PanelDock, QCheckBox, QSize, QWidget, Put a show/hide switch at the left of the bar and return it. (+6 more)

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - "MatcapSettings"
Cohesion: 0.22
Nodes (12): MatcapSettings, Post-processing applied to the sampled matcap texel., grade(), ndarray, Draw the matcap onto a sphere of ``size`` pixels, graded. Returns ``(size,…, The matcap image, in the orientation the renderer uploads it. ``None`` for the…, Apply the matcap grading to float RGB in 0-1, as the shader does. A…, sample() (+4 more)

### Community 113 - "plane_volume.py"
Cohesion: 0.18
Nodes (15): _axes(), encloses(), lattice(), lay_bed(), nearest_surface(), _passes(), Blocking a form in out of its own planes, from the outside or from a core. A…, Read the model onto a lattice, ready for solids to be laid on it. (+7 more)

### Community 114 - "Preferences"
Cohesion: 0.19
Nodes (15): _clamp(), Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, Pull anything out of range back into it. The window cannot produce these…, Restore Defaults, or a copy of one of these controls in another panel., The font size is a string; everything beside it still arrives., test_a_field_from_a_later_version_is_ignored() (+7 more)

### Community 115 - "._build"
Cohesion: 0.27
Nodes (6): QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 116 - "test_open_files.py"
Cohesion: 0.15
Nodes (11): app(), opened(), fixture, parametrize, Files arriving from outside: the command line, a drop, or the desktop's "Open…, One offscreen Qt application for the run; see test_film_recorder., What the window was asked to open, by kind, without loading anything., Finder sends the launching file as an event, which can land before the window. (+3 more)

### Community 117 - "OpenRequests"
Cohesion: 0.15
Nodes (8): Application, OpenRequests, Path, QApplication, The Qt application, listening for the desktop's way of handing over a file., Files the desktop asked the viewer to open, kept until there is a window. On…, Open ``path`` in the window, or hold it until there is one., Name the window files go to, and hand over any that came early.

### Community 118 - "FormStore"
Cohesion: 0.15
Nodes (5): FormStore, An ordered, named collection of forms, like the other stores., The live list; the undo commands operate on it directly., A name for a new form of this recipe, numbered past any it already has. A form…, test_a_form_store_names_forms_past_the_ones_it_has()

### Community 119 - "SetAttributes"
Cohesion: 0.11
Nodes (10): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, QTreeWidgetItem, Run a row's edit once Qt has finished delivering the current signal. Committing…, Record an edit the viewport's tool worked out., Join two nodes of one armature, if they are two and they are one armature., Rebuild the tree from the store, keeping the tool's selection shown. A node… (+2 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.13
Nodes (21): QRectF, project_visible(), Handle, QColor, QFont, QPainter, Draws measurements, tool previews, the orientation gizmo and the readout., A short line in one corner of the frame; returns where it went. For an exported… (+13 more)

### Community 121 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 122 - "block_splits"
Cohesion: 0.17
Nodes (12): block_labels(), block_splits(), blocks(), _cuts(), _hull_air(), The corners a hull round ``points`` holds that ``points`` do not fill. The hull…, Where a block might be cut in two: a direction, and a point to pass through.…, The greedy split, with every count along the way kept. The same walk… (+4 more)

### Community 123 - ".stage_images"
Cohesion: 0.23
Nodes (7): QOpenGLFramebufferObject, QImage, One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A…, An offscreen target the frames are drawn into, made once per export.…, Draw the scene into ``surface`` and read it back as an image., Lay the overlay -- and the caption, if it was asked for -- on a frame. Painted…

### Community 124 - "_tab_switch"
Cohesion: 0.29
Nodes (7): The show/hide switch on the tab named ``title``, if it has one., Stacked behind another panel is where the switch is worth the most., It is fifteen pixels wide and carries no words, which is exactly the shape the…, _tab_switch(), test_a_panel_that_draws_nothing_gets_no_switch_on_its_tab(), test_a_tabbed_panel_still_shows_its_switch(), test_clicking_the_switch_on_a_tab_works()

### Community 125 - "Reflow"
Cohesion: 0.30
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 126 - "._carrying_a_copy"
Cohesion: 0.20
Nodes (4): Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model., Take a copied control out of whichever hand-built panel holds it.

### Community 127 - "._advance_pending"
Cohesion: 0.18
Nodes (5): Begin a run against a fresh form: a preset's walk, or a freeform's., Take up the selected freeform again, so more landmarks can go on it. The same…, After a landmark goes down: a fresh numbered name, the same side., Refit the focused freeform's clay; for a new one, remember the choice., Record an edit the viewport's tool worked out. A freeform's placed landmark is…

### Community 128 - "PreferenceStore"
Cohesion: 0.20
Nodes (7): PreferenceStore, QObject, QSettings, The preferences, and one signal saying they have changed. A single instance,…, Adopt ``value``, push what has to be pushed, and say so. Always announces, even…, Back to how the application ships., Read the preferences off the machine. Never raises.

### Community 129 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 131 - "OverlayParts"
Cohesion: 0.15
Nodes (6): MarkerVisibility, Cache surface occlusion by view and position for every kind of marker., Answer for a batch of points at once, ahead of being asked one by one. Every…, OverlayParts, Every point the frame will ask the surface about, so it is asked once. Casting…, Which of the things drawn over the model are wanted this time. The viewport…

### Community 132 - "ExportLook"
Cohesion: 0.08
Nodes (19): The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, ExportLook, What the frames are to look like, as against what they are of. Laid over the…, Which of the things drawn over the model belong in the frames., ``base`` with this export's choices laid over it. (+11 more)

### Community 134 - "preview"
Cohesion: 0.40
Nodes (5): app(), preview(), fixture, One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "armature.py"
Cohesion: 0.27
Nodes (7): BoneLabels, Buried, Enum, str, A graph of named points under the form, and the wire it stands for. An armature…, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…

### Community 136 - "palette.py"
Cohesion: 0.11
Nodes (16): css(), outline(), QColor, The colours the hand-drawn elements paint with. Kept apart from…, Draw the hairline that separates a control from the panel. One line, the same…, A colour as a style sheet function, for the parts Qt draws., Change the one colour that is not grey, everywhere at once. The hand-painted…, set_accent() (+8 more)

### Community 137 - "stone_field"
Cohesion: 0.20
Nodes (10): Bed, block_bounds(), coarse_bounds(), point_support(), The lattice a form is worked on, and the model read onto it. Everything here…, The union of the blocks a labelling cuts the model into, and its facings. Stone…, The index range each block covers. ``(count, 3)`` lows and highs, inclusive. A…, Those ranges, read on the fine lattice the coarse one stands for. (+2 more)

### Community 138 - "box"
Cohesion: 0.50
Nodes (4): box(), A unit cube, shaded flat: six planes and twelve right angles., Every edge of a cube is a right angle, and no reading of AutoSmooth short of…, test_autosmooth_leaves_a_real_plane_change_hard()

### Community 139 - "SectionGizmo"
Cohesion: 0.22
Nodes (6): Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo, ndarray, Rotate the measurements, annotations, armature and forms onto the turned model.…

### Community 140 - "_drag_over"
Cohesion: 0.22
Nodes (10): _drag_over(), _middle_of_the_view(), A drag of ``holder`` arriving at ``point`` in the window's coordinates. A real…, The gesture the whole thing rests on: drag it onto the model, it goes., A gesture that destroys something only fires where it clearly meant to., Refused at the door it would never reach the model; so it is let in., test_a_copy_dropped_on_the_model_is_thrown_away(), test_a_copy_is_let_into_the_window_wherever_it_arrives() (+2 more)

### Community 141 - ".mouseMoveEvent"
Cohesion: 0.20
Nodes (4): Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Apply the drag live, so the clay re-forms under the cursor.

### Community 142 - ".image"
Cohesion: 0.22
Nodes (4): QMenu, Path, Offer the picture back as a file: as graded here, or as it came. A grading…, The matcap as a picture, at its own resolution. Square and opaque, with the…

### Community 143 - "fixture"
Cohesion: 0.22
Nodes (9): app(), model(), fixture, One triangle, which is a mesh as far as any of this is concerned., One offscreen Qt application for the run; see test_film_recorder., A store of its own, and the application put back the way it was found.…, store(), test_a_preference_survives_the_application_closing() (+1 more)

### Community 144 - "_shifts"
Cohesion: 0.25
Nodes (8): _balloon(), close_gaps(), outside_points(), Fill the slots the lumps leave between them, without taking clay away. The…, Grow or shrink a solid by ``reach`` cells, one axis at a time. A separable…, Where the model stops: the corners just outside ``room``. ``(n, 3)``. Only the…, The pair of slices that read a lattice ``span`` cells over along ``axis``., _shifts()

### Community 145 - "parametrize"
Cohesion: 0.67
Nodes (3): parametrize, test_a_panel_that_draws_nothing_has_no_switch(), test_the_switch_on_a_dock_bar_is_the_panels_own_visibility()

### Community 146 - "union_field"
Cohesion: 0.25
Nodes (8): block_field(), piece_bounds(), One row of coordinates per axis over ``box``, shaped so they broadcast., The union of the blocks, as a field whose zero is its surface. Each block is…, The box a lump of clay lives in, read off the six facings of its frame. Those…, The union of a set of convex solids, as a field whose zero is its surface. The…, _rows(), union_field()

### Community 147 - "carve"
Cohesion: 0.32
Nodes (8): carve(), _corner_facings(), facings(), fitted_facings(), The form ``directions`` leave of the model, worked one way or the other.…, Twenty-six directions round a cube, for judging how much air a block holds.…, The supporting directions a block may be cut along. ``(m, 3)``. The twenty-six…, The form's own facings alone, both ways round and without duplicates. What a…

### Community 149 - ".install"
Cohesion: 0.29
Nodes (6): QApplication, Put the rule in place for every switch in the application., The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter., test_a_switch_answers_a_press_anywhere_on_its_face(), test_alt_is_left_alone_so_a_switch_can_still_be_copied()

### Community 150 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 152 - "._turn"
Cohesion: 0.17
Nodes (9): _angle(), QImage, QRect, Turn the matcap by the angle the cursor swept about the centre. By angle and…, Where the sphere goes: square, centred, above the legend., The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…, The angle of ``point`` about ``centre``, anticlockwise with y upwards., An angle difference brought back into -pi to pi. (+1 more)

### Community 153 - "ui/preferences.py"
Cohesion: 0.15
Nodes (13): current(), forget(), _qcolor(), Where the preferences are kept, and what happens when one changes.…, Push the preferences that something in the process holds a copy of.…, A core colour triple as the Qt colour the palette wants., The preferences as they stand, for a caller that only wants to read., Drop the loaded store, so the next call reads the settings again. For tests,… (+5 more)

### Community 154 - "restored"
Cohesion: 0.29
Nodes (7): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., A window with the saved layout out of the way, and put back after. Shown,…, A second window, built from a layout the first one saved. The point is…, restored(), window()

### Community 162 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 163 - "._build"
Cohesion: 0.39
Nodes (4): QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 164 - "sample_count"
Cohesion: 0.50
Nodes (3): How many samples the framebuffer bound right now is drawing with. One where…, sample_count(), How many samples this view is really drawing with, or ``None``. Asked of GL…

### Community 165 - "Wires"
Cohesion: 0.29
Nodes (4): An armature, as the clay reads it: where each length of wire runs. The order…, How many lumps the wire itself asks for., What a cache has to compare to know the wire has not moved., Wires

### Community 166 - "._rename_point"
Cohesion: 0.33
Nodes (4): QTreeWidgetItem, Commit a renamed or re-checked form, or a renamed landmark, if anything changed., Give a freeform's own landmark the name typed into its row., Run a row's edit once Qt has finished delivering the current signal. Committing…

### Community 167 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 168 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 169 - "mirror_landmarks"
Cohesion: 0.33
Nodes (5): mirror_landmarks(), The midline landmarks, which are what the median plane is fitted to., The landmark list with every paired landmark reflected into place. A point the…, test_the_mirror_fills_in_the_side_the_artist_did_not_place(), test_the_mirror_leaves_a_corrected_point_where_the_artist_put_it()

### Community 170 - "_height_of"
Cohesion: 0.40
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 171 - "_file_drag"
Cohesion: 0.40
Nodes (5): _file_drag(), A file being dragged over the middle of the view, as ``kind`` of event., Entering, moving and dropping: a drop lands only where the move before it was…, test_a_file_the_window_cannot_open_is_refused_on_the_way_past(), test_a_model_file_is_welcome_at_every_step_of_its_drag()

### Community 173 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 174 - "kept_off"
Cohesion: 0.50
Nodes (4): kept_off(), Which points lie in the sleeve a length of wire declares round itself. The wire…, Which material lies under a length of wire that is to take no clay. Turning a…, within_sleeve()

### Community 175 - "_wire_frame"
Cohesion: 0.50
Nodes (4): _perpendicular(), Two unit directions across ``along``, neither of them near it., Which three ways a lump laid along a wire runs. Columns, thinnest first. The…, _wire_frame()

### Community 177 - "scrollable"
Cohesion: 0.67
Nodes (3): QScrollArea, Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, scrollable()

### Community 178 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application, made once and never torn down.

### Community 179 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `ExportLook`, `stone_field`, `box`, `plane_solids.py`, `SectionGizmo`, `ViewerState`, `PlaneSettings`, `carve`, `SectionSettings`, `ndarray`, `TriangleIndex`, `ball`, `test_plane_clusters.py`, `FormTool`, `Wires`, `viewport.py`, `mesh.py`, `ExportVideoDialog`, `settings.py`, `test_forms.py`, `OrientationSettings`, `forms.py`, `Solid`, `PrimaryForm`, `obj_loader.py`, `test_plane_solids.py`, `_wires`, `MeshBuffers`, `core/__init__.py`, `raycast_mesh`, `convex.py`, `mesh_renderer.py`, `SceneRenderer`, `test_mesh_io.py`, `plane_volume.py`, `FormStore`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `._buried_nodes`, `ExportLook`, `main_window.py`, `MainWindow`, `._place_form_landmark`, `SectionGizmo`, `.mouseMoveEvent`, `ViewerState`, `ball`, `sample_count`, `FormTool`, `film_export.py`, `viewport.py`, `Bone`, `ExportVideoDialog`, `FilmExport`, `ArmatureTool`, `MeasureTool`, `PrimaryForm`, `NavigationController`, `_Encoder`, `._picker`, `._sync_scene`, `.mouseReleaseEvent`, `._place_armature_node`, `Preferences`, `ViewportOverlay`, `.stage_images`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `SettingsWindow`, `Viewport`, `main_window.py`, `ViewerState`, `UpdateChecker`, `restored`, `ControlsWindow`, `viewport.py`, `ExportVideoDialog`, `Workspace`, `application.py`, `test_hotkeys.py`, `HotkeyBinder`, `Path`, `test_panel_docks.py`, `._menu_action`, `Release`, `test_open_files.py`, `OpenRequests`, `._carrying_a_copy`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `MainWindow` (e.g. with `ExportVideoDialog` and `ControlsWindow`) actually correct?**
  _`MainWindow` has 9 INFERRED edges - model-reasoned connections that need verification._