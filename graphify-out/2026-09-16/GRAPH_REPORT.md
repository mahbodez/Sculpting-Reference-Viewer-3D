# Graph Report - reference-viewer  (2026-09-16)

## Corpus Check
- 151 files · ~481,670 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5041 nodes · 11514 edges · 187 communities (175 shown, 12 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 552 edges (avg confidence: 0.6)
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
- plane_axes
- scrollable
- MainWindow
- Stroke
- GifWriter
- camera.py
- ndarray
- Solid
- settings.py
- _wires
- Armature
- README.md
- ViewerState
- Skeleton
- mesh_renderer.py
- CameraPanel
- SetAttributes
- ShaderProgram
- VisualMarker
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
- MatcapPreview
- ._turn
- Frame
- film_export.py
- test_viewport_markers.py
- Camera
- Film
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
- ArmaturePanel
- PrimaryForm
- HotkeyMap
- FilmExport
- FormsPanel
- PlanesPanel
- naming.py
- SurfacePicker
- Workspace
- ui/hotkeys.py
- test_forms.py
- application.py
- MeasureTool
- Link
- FormTool
- test_skeleton.py
- load_obj
- AnnotatePanel
- test_plane_solids.py
- ._selected
- test_session.py
- PoseTool
- default_matcap_pixels
- load_matcap_pixels
- test_custom_panels.py
- test_hotkeys.py
- core/preferences.py
- ContourShadingSettings
- NavigationController
- Bounds
- raycast_mesh
- test_forms_panel.py
- core/__init__.py
- HotkeyBinder
- forms.py
- MatcapPanel
- ColorButton
- frame.py
- _Encoder
- ._picker
- test_elements.py
- state.py
- compute_vertex_normals
- ReflowLayout
- Measurement
- ._selected_landmark
- OrientationSettings
- clone.py
- test_skin.py
- Path
- ask_for
- .mouseReleaseEvent
- test_panel_docks.py
- ._menu_action
- ._place_armature_node
- load_mesh
- main_window.py
- DockTitle
- test_reflow.py
- MatcapSettings
- Rig
- SectionPanel
- symbol_button
- test_open_files.py
- OpenRequests
- Hit
- AddItem
- ViewportOverlay
- release.yml
- ArmatureStore
- QComboBox
- _tab_switch
- Reflow
- ._carrying_a_copy
- CHANGELOG.md
- ui/preferences.py
- SectionAxis
- .stage_images
- MarkerVisibility
- RenderSettings
- ._place_form_landmark
- preview
- orientation.py
- palette.py
- AnnotateTool
- elements/__init__.py
- SectionGizmo
- _drag_over
- UpdateChecker
- paths.py
- Command
- test_navigation.py
- ._draw_hud
- ReplaceItems
- lock_icon
- FormStore
- theme.py
- rounded
- test_resetting_the_layout_puts_the_docks_back_at_once
- ._built
- KeyBox
- restored
- test_resetting_keeps_the_panels_built_by_hand
- picking.py
- test_the_switch_is_not_squeezed_to_nothing
- RemoveItem
- .install
- coarse_lattice
- block
- .column_of
- .update_enabled
- Human Skin renderer
- test_spatial.py
- .refresh_list
- test_plane_film.py
- environment.yml
- _NameOnlyDelegate
- _height_of
- _file_drag
- box
- app
- _NameOnlyDelegate
- test_the_switch_on_a_dock_bar_is_the_panels_own_visibility
- quad
- test_a_session_saved_without_panels_leaves_the_ones_open_alone
- test_a_panel_does_not_cover_its_own_title
- app
- test_a_panel_can_be_taken_away_and_another_built_after_a_restore
- test_loading_a_session_over_a_restored_layout_survives
- shaders.py
- test_the_dock_of_a_panel_taken_away_is_used_again
- .with_landmark_at
- test_a_reused_dock_does_not_bring_the_old_panels_contents_with_it
- .pending

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 164 edges
2. `Viewport` - 130 edges
3. `ViewerState` - 96 edges
4. `Camera` - 90 edges
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

## Communities (187 total, 12 thin omitted)

### Community 0 - "SettingsWindow"
Cohesion: 0.15
Nodes (11): The preferences as they stand. Treat as read-only; use :meth:`set`., QWidget, Fill in the groups. A switch with nothing to put in the caption column is given…, Every command with its keys, each key a box that takes one keystroke. The list…, The one button that is not a preference, and what the window is for., Say what the view is really drawing with, beside what was asked for. A sample…, Put one field back into the store, which applies and saves it., Pull every control back into line with the store. Run when the window is built,… (+3 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.07
Nodes (41): Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, app(), model(), fixture, What the artist prefers: kept apart from the document, and acted upon. Two…, An external drive that is not plugged in is not an empty gallery. (+33 more)

### Community 2 - "update_check.py"
Cohesion: 0.10
Nodes (31): check_for_update(), fetch_latest_release(), is_newer(), _macos_root_certificates(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and… (+23 more)

### Community 3 - "Viewport"
Cohesion: 0.05
Nodes (22): QOpenGLWidget, Renders the scene and turns mouse gestures into camera and tool actions., The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, Slide the view so a point sits at the centre, keeping the angle., A skeleton changed: redraw it., A form changed: work its clay out again and redraw., Hand the renderer a re-posed model and nothing else. For the frames of a pose…, Regenerate the pedestal and the cut contour when their settings move. Both are… (+14 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - "scrollable"
Cohesion: 0.14
Nodes (12): QScrollArea, QWidget, Pull current values out of the state and into the widgets., name_sliders(), QWidget, Move each slider's caption off the row and into the slider itself. A slider…, Let a panel be narrower than the sentences inside it. How narrow a panel will…, Let a widget be given less width than its own text asks for. (+4 more)

### Community 6 - "MainWindow"
Cohesion: 0.05
Nodes (20): MainWindow, QMainWindow, Open the preferences, on one group when the menu asked for one., Push the preferences that this window's own parts hold a copy of. The store has…, Open an empty panel of the artist's own and bring it to the front., Put the docks and the hand-built panels back where they were. Unless the artist…, Put the panels back where they started, now., Follow the machine's sleep to whether this window is in front. (+12 more)

### Community 7 - "Stroke"
Cohesion: 0.05
Nodes (44): AnnotateMode, AnnotationStore, Enum, ndarray, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An empty stroke carrying the current brush. (+36 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "camera.py"
Cohesion: 0.07
Nodes (48): Quat, Interactive camera model driving both perspective and orthographic views., compose(), euler_to_quat(), look_at(), matrix_to_quat(), normalize(), orthographic() (+40 more)

### Community 10 - "ndarray"
Cohesion: 0.12
Nodes (14): light_directions(), ndarray, Depth pre-pass from the camera, then occlusion and a blur over it., Fill the bound depth buffer -- and normal buffer, if any -- with the scene., Upload up to two clipping half-spaces; more than two are ignored., Key and fill directions in view space, pointing surface -> light. With…, Replace the section contour, prepared by the caller as stroke vertices., Replace the depth guide: stroke vertices fading about ``centre``. Empty… (+6 more)

### Community 11 - "Solid"
Cohesion: 0.07
Nodes (36): convex_hull(), DegenerateHullError, flat_mesh(), merged(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary… (+28 more)

### Community 12 - "settings.py"
Cohesion: 0.04
Nodes (59): The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, _along(), ContourDirection, LightSettings, plane_count(), plane_span_deg(), PlaneMode (+51 more)

### Community 13 - "_wires"
Cohesion: 0.11
Nodes (32): The order the artist put the bones in is what the scrub walks through, which is…, The claim the whole film rests on, asked again with an armature under it: an…, test_a_film_of_clay_on_a_wire_lays_it_down_in_the_order_it_was_listed(), test_the_last_stage_of_a_film_on_a_wire_is_the_form_the_slider_gives(), _bar(), _bed_for(), _holds(), A long ellipsoid: one closed form with an obvious axis to lie along. (+24 more)

### Community 14 - "Armature"
Cohesion: 0.05
Nodes (47): Armature, ArmatureNode, Bone, ndarray, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, Every node position as ``(n, 3)``., The two points a bone runs between, or ``None`` if it dangles. (+39 more)

### Community 15 - "README.md"
Cohesion: 0.27
Nodes (10): Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets (+2 more)

### Community 16 - "ViewerState"
Cohesion: 0.07
Nodes (26): Session file that sits beside a model, e.g. ``bust.refview.json``., sidecar_path(), Command, ndarray, Path, QObject, The skeletons changed; re-pose the model if one of them drives it. ``live`` is…, Emit the change signal a command's channel maps onto. (+18 more)

### Community 17 - "Skeleton"
Cohesion: 0.05
Nodes (33): Joint, _matrix16(), _pose_matrices(), ndarray, Whether the pose differs from the rest at all., A copy with the rest translation replaced and the frame kept., A tree -- or a forest -- of joints and the pose they stand in., Every joint, parents before children. A file may list a child before its… (+25 more)

### Community 18 - "mesh_renderer.py"
Cohesion: 0.03
Nodes (72): AccumTarget, bind_default(), ColorTarget, current_framebuffer(), DepthTarget, FrameTarget, GeometryTarget, Offscreen render targets used by the high-quality, ghost and smoothing passes.… (+64 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): CameraPanel, QListWidgetItem, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "SetAttributes"
Cohesion: 0.07
Nodes (16): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, PosePanel, QTreeWidgetItem, Run a row's edit once Qt has finished delivering the current signal., Arms the pose tool, lists the joints and poses the selected one., Adopt the viewport's tools: the pose tool, and the armature's for its selection., Lay an armature under the selected skeleton as it is posed. (+8 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.14
Nodes (7): ndarray, RuntimeError, Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "VisualMarker"
Cohesion: 0.22
Nodes (8): draw_rail(), draw_text(), One marker object for endpoints, nodes, landmarks and tool previews., Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, The screen-space cue for one degree of freedom. A vertical rail that fades out…, VisualMarker, The cues that share the overlay's text path get its halo too., test_overlay_text_is_drawn_as_outlined_paths()

### Community 23 - "test_planes_panel.py"
Cohesion: 0.07
Nodes (25): app(), _names(), panel(), fixture, The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as… (+17 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.12
Nodes (8): MeasurePanel, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn.

### Community 25 - "BookmarkStore"
Cohesion: 0.10
Nodes (10): BookmarkStore, CameraBookmark, Named camera positions the artist can jump between while sculpting., A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one. (+2 more)

### Community 26 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 27 - "SectionSettings"
Cohesion: 0.11
Nodes (23): ndarray, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn. (+15 more)

### Community 28 - "plane_volume.py"
Cohesion: 0.04
Nodes (108): _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field(), block_labels(), block_splits() (+100 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "TriangleIndex"
Cohesion: 0.13
Nodes (17): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Box the leaves up, coarsest level first and the leaves themselves last., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the… (+9 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.15
Nodes (9): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Slot that writes one field of the contour shading settings., Freeze the slices the way the camera faces now. The view direction is the one…, Show what this mode is actually lit and shaded by, and hide the rest. A matcap… (+1 more)

### Community 32 - "PlaneSettings"
Cohesion: 0.05
Nodes (50): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor…, How much of a turn in the surface one plane covers, in degrees. Linear in…, The grid step, in cube-face coordinates, that gives that span. A cell of this…, The design-matrix settings, in the form the fitters want them., How many planes a mode fitted to the model keeps. The climb from two planes to… (+42 more)

### Community 33 - "test_camera.py"
Cohesion: 0.08
Nodes (13): Projection, Enum, str, Projection used by :class:`Camera`., camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures. (+5 more)

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (59): The joint list with ``index`` resting at ``target`` and its children left be., angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad() (+51 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (32): c_void_p, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., Holds sleep off while the window that owns it is the one in front. The class… (+24 more)

### Community 36 - "MatcapPreview"
Cohesion: 0.10
Nodes (12): QMenu, MatcapPreview, _push_preview(), Path, QSize, QWidget, A matcap on a sphere, which is also how the matcap is graded., Offer the picture back as a file: as graded here, or as it came. A grading… (+4 more)

### Community 37 - "._turn"
Cohesion: 0.13
Nodes (9): _angle(), Redraw from the settings, which something else has changed., Put the grading back, which is the one thing a disc cannot show., Turn the matcap by the angle the cursor swept about the centre. By angle and…, Two grades on one drag: one along each axis of the movement. Both move together…, Keep the angle in -180 to 180, the range the setting is stored in., The angle of ``point`` about ``centre``, anticlockwise with y upwards., An angle difference brought back into -pi to pi. (+1 more)

### Community 38 - "Frame"
Cohesion: 0.07
Nodes (25): carried(), _push_frame(), Nothing: each row inside the copy is linked on its own., Read a drag's payload back, or ``None`` if it is not one of ours., CustomPanel, _detach(), QFormLayout, QWidget (+17 more)

### Community 39 - "film_export.py"
Cohesion: 0.08
Nodes (17): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+9 more)

### Community 40 - "test_viewport_markers.py"
Cohesion: 0.12
Nodes (20): Any, Take the choices out of a settings file, keeping what makes sense. Forgiving,…, app(), event(), fixture, parametrize, Marker interaction, selection identity, and section dragging regressions., A grid facing the camera, through the point wherever it has got to. (+12 more)

### Community 41 - "Camera"
Cohesion: 0.07
Nodes (20): Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Rays through a batch of pixels, as ``(origins, unit directions)``, ``(N, 3)``…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Project ``(N, 3)`` world points to ``(xs, ys, ndc_depths)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Screen-to-world scale at the focal plane; identical in both modes. (+12 more)

### Community 42 - "Film"
Cohesion: 0.08
Nodes (15): QThread, Film, The stage at ``index``, clamped to what has actually been recorded., A whole making, from the coarsest stage to the one the slider asks for. Held by…, QObject, The film being recorded, or the last one finished., The film already held for ``key``, if there is one., Stop any recording in flight and forget what it was making. The thread is asked… (+7 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (12): _clone_slider(), _pull_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end., Set the value the way a hand on the control would. (+4 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.11
Nodes (32): _accessor(), _buffers(), _first_skin(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry(), _primitive_skin() (+24 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.11
Nodes (12): QProgressDialog, even(), ExportVideoDialog, Path, QDialog, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+4 more)

### Community 46 - "open_writer"
Cohesion: 0.08
Nodes (28): _encode_arguments(), _encoders(), ffmpeg_path(), _FFmpegWriter, _no_window(), open_writer(), Path, RuntimeError (+20 more)

### Community 47 - "landmarks.py"
Cohesion: 0.15
Nodes (20): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _humanoid_landmarks(), _kept_laying(), _mid() (+12 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "VideoSettings"
Cohesion: 0.18
Nodes (7): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, TestTiming

### Community 50 - "Mesh"
Cohesion: 0.03
Nodes (100): auto_smooth(), _gathered(), Mesh, Triangle-mesh containers shared by the loader, the renderer and picking., Which group each of ``total`` things lands in, given pairs that agree. Hooking…, A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, An indexed triangle mesh with per-vertex positions and normals. The viewer…, Coefficients (+92 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.13
Nodes (26): QPoint, _drag(), parametrize, The matcap as its own control, and whether it tells the truth. The disc is only…, The picture follows the hand, which is the whole reason for the disc., Dragging further than the range goes is not a negative gamma., Alt and a drag copies a control; the disc must not swallow that., Tint and flip are not dragged on the disc, so they are not reset by it. (+18 more)

### Community 52 - "test_armature.py"
Cohesion: 0.05
Nodes (75): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _chain(), _derived(), _figure(), ndarray (+67 more)

### Community 53 - "ArmaturePanel"
Cohesion: 0.13
Nodes (7): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Add an empty armature and select it., Begin a preset run against a fresh armature., Take back the landmark before this one and ask for it again., Record an edit the viewport's tool worked out., The multiplier the position boxes are read and written through.

### Community 54 - "PrimaryForm"
Cohesion: 0.06
Nodes (60): PlacedLandmark, One anatomical point the artist put on the model during a guided run., The landmark list with these points taken back off the model. More than one at…, build_form(), built_count(), form_mesh(), landmark_signature(), median_plane_ready() (+52 more)

### Community 55 - "HotkeyMap"
Cohesion: 0.08
Nodes (17): Command, HotkeyMap, Which keys do what, as the artist has decided rather than as it ships. A hotkey…, Whether the artist has moved this command off what it ships with., Which command has these keys, if any., Every command with keys on it, declared or not, as id -> keys., Put ``keys`` on a command, taking them off whatever had them. Returns the id of…, Back to the shipped keys, for one command or for all of them. For one command… (+9 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (11): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+3 more)

### Community 57 - "FormsPanel"
Cohesion: 0.04
Nodes (36): FormsPanel, QPushButton, QTreeWidgetItem, QWidget, A strip of buttons that one form row can show or hide as a unit., Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle. (+28 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.06
Nodes (31): block_count(), piece_count(), How many blocks a count of planes asks the stone to be cut into. One at the…, How many lumps a count of planes asks the clay to be built out of. The masses…, How many solids the form is made of, whichever way it is being worked., solid_count(), PlanesPanel, QListWidgetItem (+23 more)

### Community 59 - "naming.py"
Cohesion: 0.13
Nodes (23): _asked(), caption_for(), element_id(), _free(), _from_id(), name_tree(), _named_after(), QWidget (+15 more)

### Community 60 - "SurfacePicker"
Cohesion: 0.05
Nodes (57): BoneRef, LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, GuideRun, _project(), Handle (+49 more)

### Community 61 - "Workspace"
Cohesion: 0.07
Nodes (20): QMainWindow, QObject, QSettings, QWidget, Keep every switch agreeing with the panel it speaks for., Hang a show/hide switch on every dock tab that wants one. A dock stacked behind…, The panel whose dock is called ``title``, if there is one., Dress the tabs once Qt has finished rearranging them. (+12 more)

### Community 62 - "ui/hotkeys.py"
Cohesion: 0.11
Nodes (22): assign(), control_of(), describe(), forget(), group_of(), HotkeyStore, listed(), QSettings (+14 more)

### Community 63 - "test_forms.py"
Cohesion: 0.07
Nodes (64): _across(), blend_rings(), build_head(), build_pelvis(), build_ribcage(), fit_plane(), _head_frame(), _lagrange() (+56 more)

### Community 64 - "application.py"
Cohesion: 0.13
Nodes (19): ArgumentParser, Namespace, QSplashScreen, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font(), main() (+11 more)

### Community 65 - "MeasureTool"
Cohesion: 0.12
Nodes (8): MeasureTool, Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., OverlayParts, ndarray, Every point the frame will ask the surface about, so it is asked once. Casting…, Which of the things drawn over the model are wanted this time. The viewport…

### Community 66 - "Link"
Cohesion: 0.12
Nodes (9): CloneGesture, Link, _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original., Whether the copy is being used right now and must not be written. (+1 more)

### Community 67 - "FormTool"
Cohesion: 0.06
Nodes (31): FormLandmarkRef, FormSettings, How the forms are drawn, and how their landmarks are placed., FormRun, FormTool, ndarray, Begin a run against a form already in the store., Every landmark the walk will ask for under these choices. With mirroring on,… (+23 more)

### Community 68 - "test_skeleton.py"
Cohesion: 0.05
Nodes (61): What to call the joint filling a humanoid slot: ``"knee.L"`` is ``"Knee L"``., role_name(), build_humanoid_skeleton(), detail_joints(), humanoid_positions(), humanoid_roles(), looks_humanoid(), ndarray (+53 more)

### Community 69 - "load_obj"
Cohesion: 0.24
Nodes (13): load_obj(), Path, Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, _push_slider(), Negative face indices count back from the most recent vertex., test_obj_relative_indices_still_load(), OBJ parsing: normals, triangulation and index handling., test_empty_file_is_rejected() (+5 more)

### Community 70 - "AnnotatePanel"
Cohesion: 0.20
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 71 - "test_plane_solids.py"
Cohesion: 0.05
Nodes (78): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), dumbbell(), edge_use(), flatness(), ndarray (+70 more)

### Community 72 - "._selected"
Cohesion: 0.14
Nodes (7): Run a row's edit once Qt has finished delivering the current signal. Committing…, Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., Run a bone between the row selected now and the node held before it., Join two nodes of one armature, if they are two and they are one armature., The node the selected row stands for, if the row is a node at all., Follow the highlighted row, without rebuilding the list underneath it. Going…

### Community 73 - "test_session.py"
Cohesion: 0.07
Nodes (26): lattice_fineness(), How much finer than usual a detail setting asks the lattice to be. One at the…, How much finer than usual the geometry's lattice is worked on., Version 4 files predate the armature; they open with an empty one., test_a_session_from_before_the_armature_still_loads(), test_a_session_carries_the_hand_built_panels(), Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers. (+18 more)

### Community 74 - "PoseTool"
Cohesion: 0.08
Nodes (36): PoseTool, ndarray, The turn the parent takes so that joint ``index`` points at ``target``. The…, The rotation joint ``index`` takes after rolling about its own bone., The pose shift that puts joint ``index`` at ``target``, children and all., Which way the bone at joint ``index`` runs, in the scene. Towards its first…, The frame a joint's pose is written in: its parent's, then its rest., Joint ``index``'s pose rotation after a scene-space turn ``delta``. (+28 more)

### Community 75 - "default_matcap_pixels"
Cohesion: 0.18
Nodes (9): default_matcap_pixels(), ndarray, A neutral studio matcap, used before the user picks one., Store an ``(h, w, 4)`` float array, reallocating only when resized., Positive rotation moves a feature clockwise, which is the way a drag goes.…, A matcap written out and read back in is the same matcap., test_the_graded_save_carries_the_grading(), test_the_original_saves_the_way_it_was_read() (+1 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.18
Nodes (20): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+12 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.07
Nodes (23): QMimeData, app(), custom(), _drop_on(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error., A group is not a row, so it goes ahead of the group it was dropped on. (+15 more)

### Community 78 - "test_hotkeys.py"
Cohesion: 0.09
Nodes (29): QKeySequence, lookup(), The control an id names, if the window still has it., Qt user interface: the viewport widget, the panels and the main window., app(), _click(), _map(), fixture (+21 more)

### Community 79 - "core/preferences.py"
Cohesion: 0.11
Nodes (20): _as_kind_of(), _clamp(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any (+12 more)

### Community 80 - "ContourShadingSettings"
Cohesion: 0.20
Nodes (9): ContourShadingSettings, Parallel slices drawn across the form, the way a contour map reads land. The…, The unit direction the slices are stacked along, in world space., parametrize, The contour shading mode: slices across the form, read off it like a map., test_a_custom_direction_is_normalised_and_an_empty_one_falls_back(), test_the_density_floor_keeps_the_spacing_finite(), test_the_settings_survive_a_session_and_an_older_file_has_them_by_default() (+1 more)

### Community 81 - "NavigationController"
Cohesion: 0.08
Nodes (18): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Degrees of yaw per pixel, signed by whether the drag is inverted. (+10 more)

### Community 82 - "Bounds"
Cohesion: 0.08
Nodes (25): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, Bounds, ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Return a copy whose bounding-box centre sits at the origin. (+17 more)

### Community 83 - "raycast_mesh"
Cohesion: 0.15
Nodes (20): _cross(), intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Row-wise cross product, without :func:`numpy.cross`'s axis shuffling., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``., The closest hit along each of a batch of rays, ``None`` where one misses. One… (+12 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.11
Nodes (30): app(), _click(), panel(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The… (+22 more)

### Community 85 - "core/__init__.py"
Cohesion: 0.15
Nodes (20): Qt-free geometry, camera and document model for the reference viewer., One entry point for every mesh format the viewer reads. Callers ask for a path…, MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., ObjLoadError, Raised when a file cannot be interpreted as an OBJ mesh., _ascii_corners() (+12 more)

### Community 86 - "HotkeyBinder"
Cohesion: 0.12
Nodes (18): QShortcut, command_for(), decorate(), HotkeyBinder, press(), QObject, QWidget, The command a control stands for, or ``None`` if it has no name to go by. A… (+10 more)

### Community 87 - "forms.py"
Cohesion: 0.06
Nodes (46): build_freeform(), _centre(), form_landmark_title(), form_spec(), FormFill, FormPreset, FormStage, freeform_landmark() (+38 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.15
Nodes (10): MatcapPanel, Rebuild the thumbnail list from the resources folder., The disc was dragged: show the renderer and the numbers what it did., A different matcap: the disc draws whichever one is on the model., Put the numbers back in line with the settings, and redraw the disc. Separate…, Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, It is the panel's main control; a click on a bar must not take it away. (+2 more)

### Community 89 - "ColorButton"
Cohesion: 0.11
Nodes (12): _clone_swatch(), _pull_swatch(), _push_swatch(), _AxisBox, ColorButton, QColor, QDoubleSpinBox, QSize (+4 more)

### Community 90 - "frame.py"
Cohesion: 0.08
Nodes (16): FrameBar, framed(), QFormLayout, QPainter, QSize, QWidget, A titled frame that folds away behind its own bar. Every group of controls in…, The mark beside a group's name: filled when open, a ring when shut. It is the… (+8 more)

### Community 91 - "_Encoder"
Cohesion: 0.25
Nodes (5): Queue, _Encoder, QObject, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 92 - "._picker"
Cohesion: 0.08
Nodes (13): ndarray, Rub out the stroke points under the eraser, live., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…, Apply the drag live, so the artist sees the wire bend as they pull it., Take hold of a landmark, to move it or just to say which one it is., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit. (+5 more)

### Community 93 - "test_elements.py"
Cohesion: 0.07
Nodes (23): app(), fixture, Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., A matcap has no light to aim, so the Light group goes -- and its space. The… (+15 more)

### Community 94 - "state.py"
Cohesion: 0.03
Nodes (62): JointRef, Quat4, AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., BoneLabels, Buried, Enum, str (+54 more)

### Community 95 - "compute_vertex_normals"
Cohesion: 0.17
Nodes (18): compute_vertex_normals(), Area-weighted smooth vertex normals for an indexed triangle soup., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic() (+10 more)

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - "Measurement"
Cohesion: 0.09
Nodes (14): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+6 more)

### Community 98 - "._selected_landmark"
Cohesion: 0.12
Nodes (7): Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors., Show the landmark group only once there are landmarks to show., The landmark the highlighted row stands for, if the row is one., Which armature the landmark list is pointing into, row or heading., Follow the highlighted landmark, and say which one it is in the view.

### Community 99 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 100 - "clone.py"
Cohesion: 0.05
Nodes (69): QAbstractButton, QLineEdit, QSlider, QSpinBox, _begin(), can_clone(), clone(), _clone_button() (+61 more)

### Community 101 - "test_skin.py"
Cohesion: 0.14
Nodes (15): build_scene(), ndarray, Stackless BVH tables for the OpenGL 3.3 skin tracer (no compute extension).…, Build on a worker from the immutable meshes currently drawn by the renderer., Pack a linear texel array within the driver's actual 2D texture limit., texture_table(), TraceScene, Skin persistence, UI wiring, acceleration layout, and refinement resets. (+7 more)

### Community 102 - "Path"
Cohesion: 0.11
Nodes (14): opens_as(), Path, Pick up whatever was last being worked on, if that was asked for. A session…, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window., Take a copied control out of whichever hand-built panel holds it., Open a file by what it is: a model, a session or a matcap. The one door every… (+6 more)

### Community 103 - "ask_for"
Cohesion: 0.16
Nodes (12): ask_for(), HotkeyDialog, normalize(), Command, QAction, QDialog, A menu entry. Its keys are heard anywhere in the window and shown in the menu., A key heard only while the view has the focus. The menu entry for it, if there… (+4 more)

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.09
Nodes (13): Record the finished drag as a single undo step., Record the finished gesture: a move, a resize, or a plain click. A press that…, Record the finished drag as one step, or read a press as a selection., Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…, Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Which skeleton an edit lands in: the selected one, else the last. (+5 more)

### Community 105 - "test_panel_docks.py"
Cohesion: 0.14
Nodes (3): Each panel in a dock of its own, and putting the docks back next time. Two…, test_a_restored_copy_drives_the_new_windows_own_control(), test_the_layout_comes_back_through_the_settings()

### Community 106 - "._menu_action"
Cohesion: 0.40
Nodes (4): _plain(), QAction, A menu entry's text as a name: no accelerator ampersand, no trailing dots., Add a menu entry, optionally with a window-wide shortcut. Given a ``command``…

### Community 107 - "._place_armature_node"
Cohesion: 0.33
Nodes (3): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 108 - "load_mesh"
Cohesion: 0.22
Nodes (14): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one(), test_binary_stl_welds_shared_corners() (+6 more)

### Community 109 - "main_window.py"
Cohesion: 0.14
Nodes (16): The newest published release, as GitHub describes it., Release, Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version(), Application window: viewport, docked panels, menus and shortcuts., Ask GitHub for the newest release in the background. The startup check is…, is_skipped() (+8 more)

### Community 110 - "DockTitle"
Cohesion: 0.10
Nodes (10): QDockWidget, QToolButton, DockTitle, PanelDock, QSize, QWidget, A dock that can go anywhere, with :class:`DockTitle` across the top., The bar across the top of a dock: a switch, a name and two buttons. (+2 more)

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - "MatcapSettings"
Cohesion: 0.15
Nodes (17): MatcapSettings, Post-processing applied to the sampled matcap texel., _clone_preview(), grade(), _pull_preview(), ndarray, The matcap itself, as the control for grading it. A matcap is a picture of a…, Draw the matcap onto a sphere of ``size`` pixels, graded. Returns ``(size,… (+9 more)

### Community 113 - "Rig"
Cohesion: 0.15
Nodes (10): MeshUnits, The real-world unit a file declared its coordinates in. Only some formats say:…, Which joints move each vertex, and by how much. Plain arrays, and never written…, The skin in the space a rigid ``matrix`` carries the model into., The skeleton a model file came with, in the model's own coordinates. Read once…, Rig, Skin, Two joints: one at x=0 holding x<1, one at x=1 holding x>=1. (+2 more)

### Community 114 - "SectionPanel"
Cohesion: 0.17
Nodes (7): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 115 - "symbol_button"
Cohesion: 0.21
Nodes (9): QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row(), QPushButton, A button that carries a drawing instead of a word. For the few actions that… (+1 more)

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
Cohesion: 0.13
Nodes (21): QPointF, project_visible(), project_visible_many(), Handle, QColor, QPainter, Project a world point, returning ``None`` when it is behind the camera., Every point of a batch in widget pixels, ``None`` where one is behind the… (+13 more)

### Community 121 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 122 - "ArmatureStore"
Cohesion: 0.16
Nodes (5): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied., test_an_armature_survives_a_session_round_trip()

### Community 123 - "QComboBox"
Cohesion: 0.24
Nodes (6): QComboBox, _push_combo(), _NameOnlyDelegate, QStyledItemDelegate, QWidget, _row()

### Community 124 - "_tab_switch"
Cohesion: 0.29
Nodes (7): The show/hide switch on the tab named ``title``, if it has one., Stacked behind another panel is where the switch is worth the most., It is fifteen pixels wide and carries no words, which is exactly the shape the…, _tab_switch(), test_a_panel_that_draws_nothing_gets_no_switch_on_its_tab(), test_a_tabbed_panel_still_shows_its_switch(), test_clicking_the_switch_on_a_tab_works()

### Community 125 - "Reflow"
Cohesion: 0.30
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 126 - "._carrying_a_copy"
Cohesion: 0.24
Nodes (3): Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model.

### Community 127 - "CHANGELOG.md"
Cohesion: 0.22
Nodes (9): Shift-snapped orbiting (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, STL and glTF import (1.1.0) (+1 more)

### Community 128 - "ui/preferences.py"
Cohesion: 0.11
Nodes (17): current(), forget(), PreferenceStore, QObject, QSettings, _qcolor(), Where the preferences are kept, and what happens when one changes.…, Push the preferences that something in the process holds a copy of.… (+9 more)

### Community 129 - "SectionAxis"
Cohesion: 0.20
Nodes (7): Enum, str, The direction the section plane faces., Unit axis, or ``None`` for a custom direction., Which side of the plane survives the cut., SectionAxis, SectionMode

### Community 130 - ".stage_images"
Cohesion: 0.14
Nodes (9): QOpenGLFramebufferObject, QImage, Use the same cached visibility test for bones and all point markers., Hand the renderer the depth grid, or take it away, before a frame., One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A…, An offscreen target the frames are drawn into, made once per export.…, Draw the scene into ``surface`` and read it back as an image. (+1 more)

### Community 131 - "MarkerVisibility"
Cohesion: 0.15
Nodes (7): MarkerVisibility, Cache surface occlusion by view and position for every kind of marker. The…, Whether the last pass is recent enough to be read instead of repeated., Mark these points as standing in front of the surface, untested. For frames…, Answer for a batch of points at once, ahead of being asked one by one. Every…, One frame asks about every node together; the answers match the one-by-one ones., test_a_batch_of_markers_is_tested_in_one_pass_and_answered_alike()

### Community 132 - "RenderSettings"
Cohesion: 0.09
Nodes (16): Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, ExportLook, What the frames are to look like, as against what they are of. Laid over the…, Which of the things drawn over the model belong in the frames., ``base`` with this export's choices laid over it., The line burned into the corner of the frame for ``stage``. Counted off the… (+8 more)

### Community 134 - "preview"
Cohesion: 0.40
Nodes (5): app(), preview(), fixture, One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "orientation.py"
Cohesion: 0.19
Nodes (7): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis, ModelPanel, Turns the model the right way up and reports what came out of the file.

### Community 136 - "palette.py"
Cohesion: 0.25
Nodes (7): outline(), QColor, The colours the hand-drawn elements paint with. Kept apart from…, Draw the hairline that separates a control from the panel. One line, the same…, Change the one colour that is not grey, everywhere at once. The hand-painted…, set_accent(), The slider the whole application is set with. One flat bar: the name of the…

### Community 137 - "AnnotateTool"
Cohesion: 0.21
Nodes (5): AnnotateTool, Turns drags into strokes, and reports what the eraser is touching., Abandon the stroke in progress., The strokes being laid down; the overlay previews them in 2D., End the drag and return the strokes it produced.

### Community 138 - "elements/__init__.py"
Cohesion: 0.07
Nodes (28): QTabBar, make_switch(), QCheckBox, One dock per panel, with a bar of its own across the top. Every panel is its…, Put a show/hide switch at the left of the bar and return it., A square that is on or off, and is clickable all over. A check box decides…, The square that shows or hides what a panel draws. One is kept on each dock's…, Switch (+20 more)

### Community 139 - "SectionGizmo"
Cohesion: 0.24
Nodes (6): Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo, The rail stands still while the camera moves, and never leaves the frame., test_section_rail_is_a_screen_space_cue_at_the_right_edge()

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

### Community 144 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 145 - "._draw_hud"
Cohesion: 0.19
Nodes (7): QRectF, QFont, A short line in one corner of the frame; returns where it went. For an exported…, What the forms tool is waiting for, said in as few lines as it takes., Text as filled outlines; see :func:`markers.draw_text` for why., What the pose tool is waiting for., What the armature tool is waiting for, said in as few lines as it takes.

### Community 146 - "ReplaceItems"
Cohesion: 0.18
Nodes (3): Any, Swap the whole contents of a document list. Used for bulk edits -- clearing the…, ReplaceItems

### Community 147 - "lock_icon"
Cohesion: 0.27
Nodes (10): QIcon, _draw_glyph(), glyph(), lock_icon(), QColor, QPixmap, Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if… (+2 more)

### Community 148 - "FormStore"
Cohesion: 0.18
Nodes (4): FormStore, An ordered, named collection of forms, like the other stores., A name for a new form of this recipe, numbered past any it already has. A form…, test_a_form_store_names_forms_past_the_ones_it_has()

### Community 149 - "theme.py"
Cohesion: 0.15
Nodes (12): css(), A colour as a style sheet function, for the parts Qt draws., QObject, Making the whole of a switch the part you can press. The theme turns every…, Turns a press anywhere on a switch into a click on it., WholeFaceToggles, apply_dark_theme(), QApplication (+4 more)

### Community 150 - "rounded"
Cohesion: 0.40
Nodes (5): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick., rounded()

### Community 152 - "._built"
Cohesion: 0.33
Nodes (4): QImage, QRect, Where the sphere goes: square, centred, above the legend., The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…

### Community 153 - "KeyBox"
Cohesion: 0.24
Nodes (4): QKeySequenceEdit, KeyBox, A box that takes one keystroke and says when it has one, or has none. Qt's box…, Show ``keys`` without that counting as the artist entering them.

### Community 154 - "restored"
Cohesion: 0.29
Nodes (7): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., A window with the saved layout out of the way, and put back after. Shown,…, A second window, built from a layout the first one saved. The point is…, restored(), window()

### Community 156 - "picking.py"
Cohesion: 0.25
Nodes (5): DepthDrag, Shared marker appearance, visibility, and constrained depth gestures., A grid across the depth axis, at the depth the point has reached. Returns…, A fixed world axis through the grabbed point; upward drags go deeper., Turning cursor positions into points in the scene. Both interactive tools need…

### Community 158 - "RemoveItem"
Cohesion: 0.29
Nodes (5): Command, Delete the item at ``index``, putting it back in place on undo., RemoveItem, Deletion goes through the undo stack, so the store only tracks position., test_deleting_a_bookmark_moves_the_cycling_position()

### Community 159 - ".install"
Cohesion: 0.29
Nodes (6): QApplication, Put the rule in place for every switch in the application., The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter., test_a_switch_answers_a_press_anywhere_on_its_face(), test_alt_is_left_alone_so_a_switch_can_still_be_copied()

### Community 160 - "coarse_lattice"
Cohesion: 0.33
Nodes (6): app(), coarse_lattice(), fixture, MonkeyPatch, One Qt application for the whole run; offscreen, so CI needs no display.…, Read every model on a small lattice, so the suite stays quick.

### Community 161 - "block"
Cohesion: 0.33
Nodes (6): block(), A closed box with hard edges, each face cut into a grid of triangles., Counting crossings is exact on a closed surface and meaningless on anything…, A box is six triangles the size of the whole thing; the lattice has to feel it…, test_an_open_model_is_read_some_other_way(), test_the_samples_cover_a_surface_however_it_was_tessellated()

### Community 162 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 163 - ".update_enabled"
Cohesion: 0.17
Nodes (6): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., The armature the selected row stands for, when the row is not a node., Highlight the row for a node picked in the view., Highlight the row for a landmark picked in the view.

### Community 164 - "Human Skin renderer"
Cohesion: 0.40
Nodes (4): Human Skin renderer, Material and transport, Scheduling, precision and compatibility, Where to change it

### Community 165 - "test_spatial.py"
Cohesion: 0.26
Nodes (11): _grid(), The picking accelerator: it must be fast without changing any answer., A bumpy height field, so rays hit different triangles at different depths., The pruned candidate set must never miss the true intersection., Every parent must enclose its children, or a ray could slip past a leaf., test_a_batch_of_rays_gets_the_same_candidates_as_one_at_a_time(), test_a_ray_that_misses_the_model_is_pruned_away(), test_every_triangle_lands_in_exactly_one_leaf() (+3 more)

### Community 166 - ".refresh_list"
Cohesion: 0.22
Nodes (5): QTreeWidgetItem, The landmarks in the preset's own order, top of the figure down. Placement…, Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing., Commit a renamed or re-checked row, if anything actually changed.

### Community 167 - "test_plane_film.py"
Cohesion: 0.10
Nodes (28): coarse_lattice(), film_of(), fixture, MonkeyPatch, parametrize, Scrubbing through the making of a form, rather than only arriving at it. The…, A cut takes material away, so no stage of a carving is larger than the one…, The same the other way about: a lump adds material, so the form grows. (+20 more)

### Community 168 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 169 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 170 - "_height_of"
Cohesion: 0.40
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 171 - "_file_drag"
Cohesion: 0.40
Nodes (5): _file_drag(), A file being dragged over the middle of the view, as ``kind`` of event., Entering, moving and dropping: a drop lands only where the move before it was…, test_a_file_the_window_cannot_open_is_refused_on_the_way_past(), test_a_model_file_is_welcome_at_every_step_of_its_drag()

### Community 172 - "box"
Cohesion: 0.50
Nodes (4): box(), A unit cube, shaded flat: six planes and twelve right angles., Every edge of a cube is a right angle, and no reading of AutoSmooth short of…, test_autosmooth_leaves_a_real_plane_change_hard()

### Community 173 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application, made once and never torn down.

### Community 174 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 175 - "test_the_switch_on_a_dock_bar_is_the_panels_own_visibility"
Cohesion: 0.67
Nodes (3): parametrize, test_a_panel_that_draws_nothing_has_no_switch(), test_the_switch_on_a_dock_bar_is_the_panels_own_visibility()

### Community 176 - "quad"
Cohesion: 0.67
Nodes (3): fixture, quad(), Two triangles covering the unit square on the z = 0 plane.

### Community 179 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 182 - "shaders.py"
Cohesion: 0.25
Nodes (6): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section(), Skin BRDF and bounded-depth light transport, shared by preview and refinement.…

## Knowledge Gaps
- **4 isolated node(s):** `refview`, `Material and transport`, `Scheduling, precision and compatibility`, `Where to change it`
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `SectionAxis`, `MarkerVisibility`, `plane_axes`, `RenderSettings`, `camera.py`, `Solid`, `_wires`, `ViewerState`, `Skeleton`, `mesh_renderer.py`, `FormStore`, `rounded`, `SectionSettings`, `plane_volume.py`, `picking.py`, `TriangleIndex`, `PlaneSettings`, `block`, `test_plane_clusters.py`, `test_spatial.py`, `test_viewport_markers.py`, `Camera`, `Film`, `gltf_loader.py`, `box`, `quad`, `PrimaryForm`, `FormTool`, `test_skeleton.py`, `load_obj`, `test_plane_solids.py`, `Bounds`, `raycast_mesh`, `core/__init__.py`, `forms.py`, `state.py`, `compute_vertex_normals`, `OrientationSettings`, `test_skin.py`, `load_mesh`, `Rig`, `Hit`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `test_preferences.py`, `.stage_images`, `RenderSettings`, `._place_form_landmark`, `MainWindow`, `AnnotateTool`, `SectionGizmo`, `ViewerState`, `ReplaceItems`, `picking.py`, `PlaneSettings`, `film_export.py`, `test_viewport_markers.py`, `Film`, `ExportVideoDialog`, `Mesh`, `PrimaryForm`, `FilmExport`, `SurfacePicker`, `MeasureTool`, `FormTool`, `PoseTool`, `test_hotkeys.py`, `NavigationController`, `_Encoder`, `._picker`, `Measurement`, `.mouseReleaseEvent`, `._place_armature_node`, `main_window.py`, `ViewportOverlay`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `PlanesPanel` connect `PlanesPanel` to `settings.py`, `main_window.py`, `MainWindow`, `test_planes_panel.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `OverlayParts`) actually correct?**
  _`ViewerState` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._