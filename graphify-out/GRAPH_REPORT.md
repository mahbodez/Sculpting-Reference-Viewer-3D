# Graph Report - reference-viewer  (2026-09-16)

## Corpus Check
- 144 files · ~476,886 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4984 nodes · 11352 edges · 192 communities (174 shown, 18 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 526 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cbde5c21`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- form_group
- test_preferences.py
- update_check.py
- Viewport
- plane_axes
- .__init__
- MainWindow
- AnnotationStore
- GifWriter
- camera.py
- SceneRenderer
- solid_count
- main_window.py
- _derived
- Armature
- README.md
- ViewerState
- Skeleton
- framebuffer.py
- CameraPanel
- SetAttributes
- ShaderProgram
- QPointF
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- VideoError
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
- SurfacePicker
- Camera
- .split_point
- ValueSlider
- gltf_loader.py
- ExportVideoDialog
- open_writer
- _Build
- Agent Graph-First Instructions
- VideoSettings
- Mesh
- test_matcap_preview.py
- test_armature.py
- ArmaturePanel
- test_forms.py
- HotkeyMap
- FilmExport
- FormsPanel
- PlanesPanel
- Landmark
- ArmatureTool
- Workspace
- ui/hotkeys.py
- build_ribcage
- application.py
- MeasureTool
- CloneGesture
- PrimaryForm
- test_skeleton.py
- load_obj
- AnnotatePanel
- test_plane_solids.py
- ._selected
- Session
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
- compute_vertex_normals
- .__init__
- forms.py
- MatcapPanel
- ColorButton
- FrameBar
- OverlayParts
- ._picker
- test_elements.py
- core/__init__.py
- FormRun
- ReflowLayout
- Measurement
- ._selected_landmark
- MeshBuffers
- clone.py
- ._sync_scene
- Path
- rigging.py
- .mouseReleaseEvent
- test_panel_docks.py
- ._build_menus
- ._place_armature_node
- load_mesh
- Release
- DockTitle
- test_reflow.py
- MatcapSettings
- ShadingMode
- SectionPanel
- ._build
- test_open_files.py
- OpenRequests
- test_a_moving_view_reads_the_last_pass_and_asks_again_once_it_has_settled
- AddItem
- ViewportOverlay
- release.yml
- ArmatureStore
- ._build_selection
- _tab_switch
- Reflow
- ._carrying_a_copy
- CHANGELOG.md
- ui/preferences.py
- SectionAxis
- ._buried_nodes
- MarkerVisibility
- ExportLook
- ._place_form_landmark
- preview
- SkeletonStore
- theme.py
- ._write
- workspace.py
- SectionGizmo
- _drag_over
- .mouseMoveEvent
- paths.py
- ._chosen_armature
- test_navigation.py
- ._draw_hud
- mesh_renderer.py
- _clone_preview
- ndarray
- WholeFaceToggles
- coarse_lattice
- test_resetting_the_layout_puts_the_docks_back_at_once
- ._built
- .set_value
- restored
- test_resetting_keeps_the_panels_built_by_hand
- ._step
- test_the_switch_is_not_squeezed_to_nothing
- ._commit_node_drag
- LightSettings
- ._marked_points
- .pan
- .column_of
- .update_enabled
- sample_count
- test_spatial.py
- .refresh_list
- coarse_lattice
- environment.yml
- .transformed
- _height_of
- _file_drag
- refview/__init__.py
- ._join_to
- _NameOnlyDelegate
- ._selected_rows
- .new_armature
- .film_changed
- ._place_joint
- app
- ndarray
- panel
- shaders.py
- test_the_disc_samples_where_the_shader_would
- .with_landmark_at
- welded
- section
- app
- .surface_opacity
- .pending
- .set_shown
- .shown

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 160 edges
2. `Viewport` - 130 edges
3. `ViewerState` - 95 edges
4. `Camera` - 89 edges
5. `MainWindow` - 87 edges
6. `Skeleton` - 85 edges
7. `Armature` - 81 edges
8. `PrimaryForm` - 79 edges
9. `PlaneSettings` - 67 edges
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

## Communities (192 total, 18 thin omitted)

### Community 0 - "form_group"
Cohesion: 0.11
Nodes (17): QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row(), The preferences as they stand. Treat as read-only; use :meth:`set`., QWidget, Fill in the groups. A switch with nothing to put in the caption column is given…, Every command with its keys, each key a box that takes one keystroke. The list… (+9 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.07
Nodes (41): Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, app(), model(), fixture, What the artist prefers: kept apart from the document, and acted upon. Two…, An external drive that is not plugged in is not an empty gallery. (+33 more)

### Community 2 - "update_check.py"
Cohesion: 0.10
Nodes (31): check_for_update(), fetch_latest_release(), is_newer(), _macos_root_certificates(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and… (+23 more)

### Community 3 - "Viewport"
Cohesion: 0.06
Nodes (14): QOpenGLWidget, Renders the scene and turns mouse gestures into camera and tool actions., Slide the view so a point sits at the centre, keeping the angle., A form changed: work its clay out again and redraw., Slide the view so a measurement sits at the centre, keeping the angle., End any film being recorded, and wait for its thread to really stop. For…, The document being drawn., The film of the form's making, as far as it has been recorded. (+6 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - ".__init__"
Cohesion: 0.20
Nodes (7): QWidget, Pull current values out of the state and into the widgets., QWidget, Let a panel be narrower than the sentences inside it. How narrow a panel will…, Let a widget be given less width than its own text asks for., relax_widths(), _squeezable()

### Community 6 - "MainWindow"
Cohesion: 0.06
Nodes (16): MainWindow, QMainWindow, Pick up whatever was last being worked on, if that was asked for. A session…, Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window., Open an empty panel of the artist's own and bring it to the front., Put the panels back where they started, now., Follow the machine's sleep to whether this window is in front. (+8 more)

### Community 7 - "AnnotationStore"
Cohesion: 0.07
Nodes (28): AnnotationStore, An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., build_segment_vertices(), build_vertices(), _expand(), ndarray, Geometry for the surface annotations and the cross-section contour. Strokes are… (+20 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "camera.py"
Cohesion: 0.06
Nodes (52): Quat, Quat4, Interactive camera model driving both perspective and orthographic views., compose(), euler_to_quat(), look_at(), matrix_to_quat(), normalize() (+44 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.09
Nodes (27): Everything the viewport needs in order to draw a frame., RenderSettings, light_directions(), normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the section contour, prepared by the caller as stroke vertices., Replace the depth guide: stroke vertices fading about ``centre``. Empty… (+19 more)

### Community 11 - "solid_count"
Cohesion: 0.15
Nodes (15): block_count(), piece_count(), How many blocks a count of planes asks the stone to be cut into. One at the…, How many lumps a count of planes asks the clay to be built out of. The masses…, How many solids the form is made of, whichever way it is being worked., solid_count(), The line under the geometry slider: how the form is being worked. ``wires`` is…, _sculpt_summary() (+7 more)

### Community 12 - "main_window.py"
Cohesion: 0.07
Nodes (45): QIcon, The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, MatcapLoadError, RuntimeError, Raised when an image cannot be used as a matcap., _draw_glyph(), glyph() (+37 more)

### Community 13 - "_derived"
Cohesion: 0.10
Nodes (24): _kept_laying(), Fresh bones, laid the way the armature was already laying them. The bone list…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _derived(), A guess the artist corrects is theirs, and the mirror leaves it alone., The new list is the edit; the old one has to survive to be undone to., Hips, then the ribcage, then the head, then the limbs largest first. This order… (+16 more)

### Community 14 - "Armature"
Cohesion: 0.05
Nodes (47): Armature, ArmatureNode, Bone, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves., A plausible thickness for a node placed by hand. (+39 more)

### Community 15 - "README.md"
Cohesion: 0.19
Nodes (14): High Quality shading mode (1.1.0), Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, High Quality without ray tracing, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance (+6 more)

### Community 16 - "ViewerState"
Cohesion: 0.09
Nodes (20): ndarray, Path, QObject, The skeletons changed; re-pose the model if one of them drives it. ``live`` is…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., The rest mesh as the bound skeleton poses it, or the rest mesh itself. Skinning…, The skeleton the model follows, if it has one. (+12 more)

### Community 17 - "Skeleton"
Cohesion: 0.05
Nodes (31): Joint, _matrix16(), _pose_matrices(), ndarray, Whether the pose differs from the rest at all., A copy with the rest translation replaced and the frame kept., A tree -- or a forest -- of joints and the pose they stand in., Every joint, parents before children. A file may list a child before its… (+23 more)

### Community 18 - "framebuffer.py"
Cohesion: 0.07
Nodes (18): AccumTarget, ColorTarget, DepthTarget, FrameTarget, GeometryTarget, Offscreen render targets used by the high-quality, ghost and smoothing passes.…, A depth-only framebuffer, sampled afterwards as a texture., ``clamp_to_lit`` makes everything outside the map read as unshadowed. (+10 more)

### Community 19 - "CameraPanel"
Cohesion: 0.09
Nodes (11): Projection, Enum, str, Projection used by :class:`Camera`., CameraPanel, QListWidgetItem, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place. (+3 more)

### Community 20 - "SetAttributes"
Cohesion: 0.06
Nodes (20): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, PosePanel, QTreeWidgetItem, Run a row's edit once Qt has finished delivering the current signal., Arms the pose tool, lists the joints and poses the selected one., Adopt the viewport's tools: the pose tool, and the armature's for its selection., Add an empty skeleton, for a chain to be clicked into. (+12 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.12
Nodes (9): OpenGL rendering layer: shader programs, textures and the scene renderer., ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError (+1 more)

### Community 22 - "QPointF"
Cohesion: 0.16
Nodes (14): QPointF, draw_rail(), draw_text(), One marker object for endpoints, nodes, landmarks and tool previews., Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, The screen-space cue for one degree of freedom. A vertical rail that fades out…, VisualMarker, project_visible_many() (+6 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.08
Nodes (21): _names(), The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as…, Or there would be no way to turn one back on., A limb is four bones, and deciding not to block the arms in is one decision.…, It is rebuilt on every change, and ticking one row of a selected limb would be… (+13 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.10
Nodes (11): MeasurePanel, _NameOnlyDelegate, QStyledItemDelegate, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing… (+3 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.10
Nodes (10): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around. (+2 more)

### Community 26 - "VideoError"
Cohesion: 0.08
Nodes (20): _encode_arguments(), _encoders(), _FFmpegWriter, _no_window(), ndarray, RuntimeError, An export that could not be written, said in words for the artist., Which encoders this ffmpeg was built with. Asked once, because a build without… (+12 more)

### Community 27 - "SectionSettings"
Cohesion: 0.12
Nodes (21): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn., section_segments() (+13 more)

### Community 28 - "plane_volume.py"
Cohesion: 0.04
Nodes (112): _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field(), block_labels(), block_splits() (+104 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "TriangleIndex"
Cohesion: 0.13
Nodes (17): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Box the leaves up, coarsest level first and the leaves themselves last., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the… (+9 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.13
Nodes (13): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Slot that writes one field of the contour shading settings., Freeze the slices the way the camera faces now. The view direction is the one…, Show what this mode is actually lit and shaded by, and hide the rest. A matcap… (+5 more)

### Community 32 - "PlaneSettings"
Cohesion: 0.03
Nodes (79): QThread, Film, film_key(), What a film depends on. Everything that changes the shape of any stage, and…, A whole making, from the coarsest stage to the one the slider asks for. Held by…, _along(), lattice_fineness(), plane_count() (+71 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (59): The joint list with ``index`` resting at ``target`` and its children left be., angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad() (+51 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (32): c_void_p, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., Holds sleep off while the window that owns it is the one in front. The class… (+24 more)

### Community 36 - "MatcapPreview"
Cohesion: 0.09
Nodes (15): QMenu, MatcapPreview, _push_preview(), Path, QSize, QWidget, A matcap on a sphere, which is also how the matcap is graded., Offer the picture back as a file: as graded here, or as it came. A grading… (+7 more)

### Community 37 - "._turn"
Cohesion: 0.15
Nodes (7): _angle(), Redraw from the settings, which something else has changed., Put the grading back, which is the one thing a disc cannot show., Turn the matcap by the angle the cursor swept about the centre. By angle and…, Two grades on one drag: one along each axis of the movement. Both move together…, Keep the angle in -180 to 180, the range the setting is stored in., The angle of ``point`` about ``centre``, anticlockwise with y upwards.

### Community 38 - "Frame"
Cohesion: 0.07
Nodes (26): carried(), _pull_frame(), _push_frame(), Nothing: each row inside the copy is linked on its own., Read a drag's payload back, or ``None`` if it is not one of ours., CustomPanel, _detach(), QFormLayout (+18 more)

### Community 39 - "film_export.py"
Cohesion: 0.08
Nodes (20): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+12 more)

### Community 40 - "SurfacePicker"
Cohesion: 0.05
Nodes (44): JointRef, AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+36 more)

### Community 41 - "Camera"
Cohesion: 0.13
Nodes (11): Camera, ndarray, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Project ``(N, 3)`` world points to ``(xs, ys, ndc_depths)`` in widget pixels., Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling…, Point the camera along ``direction``, measured object-to-eye. (+3 more)

### Community 42 - ".split_point"
Cohesion: 0.22
Nodes (7): BoneRef, The nearest bone under the cursor, for showing its length., Where on a bone a click at ``(x, y)`` landed. The share along the bone is read…, How far along a screen-space segment the cursor's nearest point lies., Pixels from the cursor to the segment, or ``None`` if either end is behind., _segment_distance(), _segment_share()

### Community 43 - "ValueSlider"
Cohesion: 0.11
Nodes (4): _pull_slider(), QSize, A named, filled bar that sets one number., ValueSlider

### Community 44 - "gltf_loader.py"
Cohesion: 0.08
Nodes (40): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), _first_skin(), GltfLoadError, load_gltf(), _local_transform() (+32 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.11
Nodes (13): QProgressDialog, even(), ExportVideoDialog, Path, QDialog, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+5 more)

### Community 46 - "open_writer"
Cohesion: 0.13
Nodes (16): ffmpeg_path(), open_writer(), Path, Where ffmpeg is, or ``None``. Looked for in the order of how deliberate each…, Why ``format`` cannot be written here, or ``None`` if it can., Start an encoder for ``settings``, or say why there cannot be one., unavailable(), frames() (+8 more)

### Community 47 - "_Build"
Cohesion: 0.19
Nodes (14): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _mid(), ndarray, Somewhere to collect nodes while the rules that need each other run. (+6 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "VideoSettings"
Cohesion: 0.12
Nodes (10): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, Pump the event loop until ``done()`` or the clock runs out., run_until() (+2 more)

### Community 50 - "Mesh"
Cohesion: 0.03
Nodes (95): auto_smooth(), _gathered(), Mesh, Triangle-mesh containers shared by the loader, the renderer and picking., Which group each of ``total`` things lands in, given pairs that agree. Hooking…, A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, An indexed triangle mesh with per-vertex positions and normals. The viewer…, Coefficients (+87 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.14
Nodes (24): QPoint, _drag(), The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc., Dragging further than the range goes is not a negative gamma., Alt and a drag copies a control; the disc must not swallow that., Tint and flip are not dragged on the disc, so they are not reset by it. (+16 more)

### Community 52 - "test_armature.py"
Cohesion: 0.07
Nodes (56): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _chain(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other., The femoral head is in from the ASIS, below it and behind it, by shares of the… (+48 more)

### Community 53 - "ArmaturePanel"
Cohesion: 0.14
Nodes (5): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Take back the landmark before this one and ask for it again., Record an edit the viewport's tool worked out., The multiplier the position boxes are read and written through.

### Community 54 - "test_forms.py"
Cohesion: 0.08
Nodes (43): merged(), Several flat meshes as one, or ``None`` when there is nothing to draw., build_form(), built_count(), form_mesh(), freeform_landmark(), landmark_signature(), A landmark the artist has just named, keyed so it does not collide. (+35 more)

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
Cohesion: 0.14
Nodes (10): PlanesPanel, Lay one length of wire earlier or later, as one undoable step., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Show what this way of working needs, and put the rest away. A setting that does…, The line under the normals slider: what the setting has asked for., Breaks the form into planes, in the shading or in the geometry itself., Re-read the armatures and what the chosen one is laying down. Called whenever… (+2 more)

### Community 59 - "Landmark"
Cohesion: 0.09
Nodes (15): _centre(), _pair(), A left landmark, then the right one that mirrors it., The freeform landmark the artist named with this key, if any., The named landmarks with one more, or the same one re-described., Every landmark, in the order the walk asks for them., _humanoid_landmarks(), Landmark (+7 more)

### Community 60 - "ArmatureTool"
Cohesion: 0.06
Nodes (40): LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, Handle, Begin a preset run against an armature already in the store., The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now. (+32 more)

### Community 61 - "Workspace"
Cohesion: 0.06
Nodes (23): QDockWidget, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top., QMainWindow, QObject, QSettings, QWidget, Keep every switch agreeing with the panel it speaks for. (+15 more)

### Community 62 - "ui/hotkeys.py"
Cohesion: 0.05
Nodes (53): QKeySequenceEdit, QShortcut, ask_for(), assign(), command_for(), control_of(), decorate(), describe() (+45 more)

### Community 63 - "build_ribcage"
Cohesion: 0.07
Nodes (55): _across(), blend_rings(), build_head(), build_pelvis(), build_ribcage(), fit_plane(), _head_frame(), _HeadFrame (+47 more)

### Community 64 - "application.py"
Cohesion: 0.12
Nodes (20): ArgumentParser, Namespace, QSplashScreen, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font(), main() (+12 more)

### Community 65 - "MeasureTool"
Cohesion: 0.22
Nodes (4): MeasureTool, Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview.

### Community 66 - "CloneGesture"
Cohesion: 0.14
Nodes (7): CloneGesture, _Pulse, QObject, One timer for every copy in the window., Bring the copy up to date with its original., Whether the copy is being used right now and must not be written., Watches for Alt and a drag, and turns it into a copy on the cursor. Installed…

### Community 67 - "PrimaryForm"
Cohesion: 0.05
Nodes (50): FormLandmarkRef, PlacedLandmark, One anatomical point the artist put on the model during a guided run., FormSettings, FormStore, mirror_form_landmarks(), PrimaryForm, Point3 (+42 more)

### Community 68 - "test_skeleton.py"
Cohesion: 0.09
Nodes (37): build_humanoid_skeleton(), A proportioned humanoid skeleton, roles and all, standing on ``feet``., make_joint(), A joint at a position in its parent's frame, with no turn of its own., The model as ``skeleton`` poses it, or ``rest`` itself when it cannot. Linear…, skinned_mesh(), _arm(), ndarray (+29 more)

### Community 69 - "load_obj"
Cohesion: 0.22
Nodes (14): load_obj(), Path, Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, _push_slider(), Negative face indices count back from the most recent vertex., test_obj_quads_are_triangulated(), test_obj_relative_indices_still_load(), OBJ parsing: normals, triangulation and index handling. (+6 more)

### Community 70 - "AnnotatePanel"
Cohesion: 0.21
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 71 - "test_plane_solids.py"
Cohesion: 0.03
Nodes (147): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), film_of(), parametrize, Scrubbing through the making of a form, rather than only arriving at it. The…, A cut takes material away, so no stage of a carving is larger than the one… (+139 more)

### Community 72 - "._selected"
Cohesion: 0.24
Nodes (4): Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., The node the selected row stands for, if the row is a node at all., Follow the highlighted row, without rebuilding the list underneath it. Going…

### Community 73 - "Session"
Cohesion: 0.09
Nodes (25): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Path (+17 more)

### Community 74 - "PoseTool"
Cohesion: 0.10
Nodes (32): PoseTool, The pose shift that puts joint ``index`` at ``target``, children and all., Turns pulls on joints into pose edits, and clicks into new joints., Where a pulled joint is being pulled to. Across the camera-facing plane through…, app(), _arm(), _event(), _front_camera() (+24 more)

### Community 75 - "default_matcap_pixels"
Cohesion: 0.10
Nodes (11): Fill the shader's table with a level, if it is not already in it., Replace the annotation geometry; pass an empty list to hide it., DataTexture, default_matcap_pixels(), ndarray, Matcap texture loading and upload, and the small data table beside it., An RGBA16F 2D texture with clamped edges and mipmapped minification., A neutral studio matcap, used before the user picks one. (+3 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.17
Nodes (21): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+13 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.08
Nodes (16): app(), custom(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error., A group is not a row, so it goes ahead of the group it was dropped on., One offscreen Qt application for the run; see test_film_recorder., It is named "Offset" in the panel it came from; it says so here too. (+8 more)

### Community 78 - "test_hotkeys.py"
Cohesion: 0.09
Nodes (28): QKeySequence, lookup(), The control an id names, if the window still has it., app(), _click(), _map(), fixture, Hotkeys: the map, the store, the binder, and the gesture that assigns one. (+20 more)

### Community 79 - "core/preferences.py"
Cohesion: 0.11
Nodes (20): _as_kind_of(), _clamp(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any (+12 more)

### Community 80 - "ContourShadingSettings"
Cohesion: 0.20
Nodes (8): ContourShadingSettings, Parallel slices drawn across the form, the way a contour map reads land. The…, The unit direction the slices are stacked along, in world space., parametrize, The contour shading mode: slices across the form, read off it like a map., test_a_custom_direction_is_normalised_and_an_empty_one_falls_back(), test_the_density_floor_keeps_the_spacing_finite(), test_the_slices_face_the_way_that_was_asked()

### Community 81 - "NavigationController"
Cohesion: 0.08
Nodes (18): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Degrees of yaw per pixel, signed by whether the drag is inverted. (+10 more)

### Community 82 - "Bounds"
Cohesion: 0.12
Nodes (18): Bounds, ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings (+10 more)

### Community 83 - "raycast_mesh"
Cohesion: 0.08
Nodes (31): _cross(), Hit, intersects_bounds(), ndarray, Row-wise cross product, without :func:`numpy.cross`'s axis shuffling., Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays. (+23 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.05
Nodes (54): Model orientation (1.1.0), OrientationSettings, Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it. (+46 more)

### Community 85 - "compute_vertex_normals"
Cohesion: 0.07
Nodes (41): compute_vertex_normals(), One entry point for every mesh format the viewer reads. Callers ask for a path…, MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., Area-weighted smooth vertex normals for an indexed triangle soup., _assemble(), _face_corners() (+33 more)

### Community 86 - ".__init__"
Cohesion: 0.11
Nodes (8): HotkeyBinder, Turns the map into the shortcuts of one window, and keeps them current., The shortcut answering for a command, for a test that wants to press it., Push the preferences that this window's own parts hold a copy of. The store has…, Put the docks and the hand-built panels back where they were. Unless the artist…, Give each panel a dock of its own, tabbed together on the right. Each panel can…, Single-key shortcuts, scoped so they never eat text input. They only fire while…, Say which panel buttons are the same thing as a menu entry. The button that…

### Community 87 - "forms.py"
Cohesion: 0.04
Nodes (72): convex_hull(), DegenerateHullError, flat_mesh(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, The outward unit normal at each vertex: the area-weighted mean of its faces'. A… (+64 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.17
Nodes (8): MatcapPanel, Rebuild the thumbnail list from the resources folder., The disc was dragged: show the renderer and the numbers what it did., A different matcap: the disc draws whichever one is on the model., Put the numbers back in line with the settings, and redraw the disc. Separate…, Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, test_the_disc_draws_the_matcap_that_is_on_the_model()

### Community 89 - "ColorButton"
Cohesion: 0.11
Nodes (11): _pull_swatch(), _push_swatch(), _AxisBox, ColorButton, QColor, QDoubleSpinBox, QSize, QWidget (+3 more)

### Community 90 - "FrameBar"
Cohesion: 0.09
Nodes (13): FrameBar, framed(), QFormLayout, QPainter, QSize, QWidget, The mark beside a group's name: filled when open, a ring when shut. It is the…, The rows inside the frame. ``layout()`` is the frame's own, which stacks the… (+5 more)

### Community 91 - "OverlayParts"
Cohesion: 0.17
Nodes (8): Queue, _Encoder, QObject, Which of the things drawn over the model belong in the frames., The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`., OverlayParts, Which of the things drawn over the model are wanted this time. The viewport…

### Community 92 - "._picker"
Cohesion: 0.13
Nodes (8): ndarray, Rub out the stroke points under the eraser, live., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on., Take hold of a joint -- or of a bone, by its far end., Take hold of a form's landmark, to move it or just to say which one it is.

### Community 93 - "test_elements.py"
Cohesion: 0.09
Nodes (17): Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., A matcap has no light to aim, so the Light group goes -- and its space. The…, Run the refresh the shared timer would have run., ``self._mode`` is ``mode``; the group called Mode settles for a number. (+9 more)

### Community 94 - "core/__init__.py"
Cohesion: 0.04
Nodes (64): AnnotateMode, Enum, ndarray, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An empty stroke carrying the current brush., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns… (+56 more)

### Community 95 - "FormRun"
Cohesion: 0.40
Nodes (3): FormRun, Begin a run against a form already in the store., A guided form part-way through.

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - "Measurement"
Cohesion: 0.08
Nodes (15): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+7 more)

### Community 98 - "._selected_landmark"
Cohesion: 0.12
Nodes (7): Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors., Show the landmark group only once there are landmarks to show., The landmark the highlighted row stands for, if the row is one., Which armature the landmark list is pointing into, row or heading., Follow the highlighted landmark, and say which one it is in the view.

### Community 99 - "MeshBuffers"
Cohesion: 0.12
Nodes (7): MeshBuffers, Forget the contents without releasing the buffer objects., Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are…, Whichever geometry is standing for the model this frame., Vertex/index buffers for one mesh, bound through a single VAO.

### Community 100 - "clone.py"
Cohesion: 0.03
Nodes (104): QAbstractButton, QComboBox, QLineEdit, QSlider, QSpinBox, _begin(), can_clone(), clone() (+96 more)

### Community 101 - "._sync_scene"
Cohesion: 0.15
Nodes (6): Regenerate the pedestal and the cut contour when their settings move. Both are…, The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on., Cut the mesh with each section plane and expand the result to strokes.

### Community 102 - "Path"
Cohesion: 0.19
Nodes (8): opens_as(), Path, Write down the session just saved or loaded, for the next start., Open a file by what it is: a model, a session or a matcap. The one door every…, A path written down last time, if it is one and it is still there., What a file would open as -- ``"model"``, ``"session"`` or ``"matcap"`` -- by…, Apply a matcap image, reporting unreadable files to the user., _remembered()

### Community 103 - "rigging.py"
Cohesion: 0.10
Nodes (26): detail_joints(), humanoid_positions(), humanoid_roles(), looks_humanoid(), ndarray, Where skeletons come from: an armature, a preset, or the names in a file. Three…, Every humanoid role's place for a figure this tall standing on ``feet``., A joint name broken into lower-case words. ``LeftUpLeg`` is ``left up leg``;… (+18 more)

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.14
Nodes (8): Record the finished drag as a single undo step., Record the finished drag as one step, or read a press as a selection., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Record the finished pull as one step, or read a press as a selection., Track the joint and bone under the cursor; True when either changed., Record the finished drag as one step, or read a press as a selection., Track the form landmark under the cursor; True when it changed.

### Community 105 - "test_panel_docks.py"
Cohesion: 0.07
Nodes (19): parametrize, Each panel in a dock of its own, and putting the docks back next time. Two…, An older file must not be able to sweep away the artist's own panels., A dock puts the panel below its bar's *hint*, not below its bar. Leave the hint…, The crash this is about takes the process with it, so arriving is passing., The path the artist actually walks: File, Load Session, twice., Parked rather than destroyed, so the count does not climb for ever., It is a new panel, whatever it happens to be made out of. (+11 more)

### Community 106 - "._build_menus"
Cohesion: 0.20
Nodes (6): _plain(), QAction, Open the preferences, on one group when the menu asked for one., A menu entry's text as a name: no accelerator ampersand, no trailing dots., Which panels are open, and the panels the artist builds. Rebuilt every time it…, Add a menu entry, optionally with a window-wide shortcut. Given a ``command``…

### Community 107 - "._place_armature_node"
Cohesion: 0.15
Nodes (6): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…, The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, A skeleton changed: redraw it., Hand the renderer a re-posed model and nothing else. For the frames of a pose…

### Community 108 - "load_mesh"
Cohesion: 0.24
Nodes (13): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one(), test_binary_stl_welds_shared_corners() (+5 more)

### Community 109 - "Release"
Cohesion: 0.11
Nodes (19): QRunnable, The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, _CheckTask, is_skipped(), QObject, QWidget (+11 more)

### Community 110 - "DockTitle"
Cohesion: 0.09
Nodes (14): QToolButton, DockTitle, make_switch(), QCheckBox, QSize, QWidget, One dock per panel, with a bar of its own across the top. Every panel is its…, Put a show/hide switch at the left of the bar and return it. (+6 more)

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - "MatcapSettings"
Cohesion: 0.20
Nodes (14): MatcapSettings, Post-processing applied to the sampled matcap texel., grade(), ndarray, The matcap itself, as the control for grading it. A matcap is a picture of a…, Draw the matcap onto a sphere of ``size`` pixels, graded. Returns ``(size,…, An angle difference brought back into -pi to pi., Apply the matcap grading to float RGB in 0-1, as the shader does. A… (+6 more)

### Community 113 - "ShadingMode"
Cohesion: 0.12
Nodes (6): Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode, FakeViewport, QImage, A viewport that renders nothing, at whatever size it is asked for.

### Community 114 - "SectionPanel"
Cohesion: 0.19
Nodes (6): Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 115 - "._build"
Cohesion: 0.29
Nodes (6): QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 116 - "test_open_files.py"
Cohesion: 0.15
Nodes (11): app(), opened(), fixture, parametrize, Files arriving from outside: the command line, a drop, or the desktop's "Open…, One offscreen Qt application for the run; see test_film_recorder., What the window was asked to open, by kind, without loading anything., Finder sends the launching file as an event, which can land before the window. (+3 more)

### Community 117 - "OpenRequests"
Cohesion: 0.15
Nodes (8): Application, OpenRequests, Path, QApplication, The Qt application, listening for the desktop's way of handing over a file., Files the desktop asked the viewer to open, kept until there is a window. On…, Open ``path`` in the window, or hold it until there is one., Name the window files go to, and hand over any that came early.

### Community 118 - "test_a_moving_view_reads_the_last_pass_and_asks_again_once_it_has_settled"
Cohesion: 0.14
Nodes (7): Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Rays through a batch of pixels, as ``(origins, unit directions)``, ``(N, 3)``…, Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Move the camera so ``bounds`` fills the view, keeping the direction., Adopt the pose of ``other`` without replacing this instance., Frames within the throttle reuse the answers; the first frame after it recasts., test_a_moving_view_reads_the_last_pass_and_asks_again_once_it_has_settled()

### Community 119 - "AddItem"
Cohesion: 0.06
Nodes (30): Camera motion is deliberately not undoable, Every document edit is a command, AddItem, Any, Command, Append an item to a document list., Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the… (+22 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.14
Nodes (18): project_visible(), Handle, QColor, QPainter, Project a world point, returning ``None`` when it is behind the camera., Draws measurements, tool previews, the orientation gizmo and the readout., Draw everything over the scene. ``occlude`` off skips asking the surface which…, A line laid over its own dark outline, so it reads against anything. (+10 more)

### Community 121 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 122 - "ArmatureStore"
Cohesion: 0.16
Nodes (5): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied., test_an_armature_survives_a_session_round_trip()

### Community 123 - "._build_selection"
Cohesion: 0.27
Nodes (4): _NameOnlyDelegate, QStyledItemDelegate, QWidget, _row()

### Community 124 - "_tab_switch"
Cohesion: 0.29
Nodes (7): The show/hide switch on the tab named ``title``, if it has one., Stacked behind another panel is where the switch is worth the most., It is fifteen pixels wide and carries no words, which is exactly the shape the…, _tab_switch(), test_a_panel_that_draws_nothing_gets_no_switch_on_its_tab(), test_a_tabbed_panel_still_shows_its_switch(), test_clicking_the_switch_on_a_tab_works()

### Community 125 - "Reflow"
Cohesion: 0.30
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 126 - "._carrying_a_copy"
Cohesion: 0.20
Nodes (4): Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model., Take a copied control out of whichever hand-built panel holds it.

### Community 127 - "CHANGELOG.md"
Cohesion: 0.25
Nodes (7): Shift-snapped orbiting (1.1.0), Cross-section tool (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding

### Community 128 - "ui/preferences.py"
Cohesion: 0.11
Nodes (17): current(), forget(), PreferenceStore, QObject, QSettings, _qcolor(), Where the preferences are kept, and what happens when one changes.…, Push the preferences that something in the process holds a copy of.… (+9 more)

### Community 129 - "SectionAxis"
Cohesion: 0.18
Nodes (7): Enum, str, The direction the section plane faces., Unit axis, or ``None`` for a custom direction., Which side of the plane survives the cut., SectionAxis, SectionMode

### Community 131 - "MarkerVisibility"
Cohesion: 0.18
Nodes (5): MarkerVisibility, Cache surface occlusion by view and position for every kind of marker. The…, Whether the last pass is recent enough to be read instead of repeated., Mark these points as standing in front of the surface, untested. For frames…, Answer for a batch of points at once, ahead of being asked one by one. Every…

### Community 132 - "ExportLook"
Cohesion: 0.10
Nodes (17): QOpenGLFramebufferObject, The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, ExportLook, What the frames are to look like, as against what they are of. Laid over the…, ``base`` with this export's choices laid over it. (+9 more)

### Community 134 - "preview"
Cohesion: 0.40
Nodes (5): app(), preview(), fixture, One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "SkeletonStore"
Cohesion: 0.18
Nodes (3): An ordered collection of skeletons, like the other document stores., The skeleton the model follows: the first one bound to its rig., SkeletonStore

### Community 136 - "theme.py"
Cohesion: 0.20
Nodes (10): css(), outline(), QColor, Draw the hairline that separates a control from the panel. One line, the same…, A colour as a style sheet function, for the parts Qt draws., Change the one colour that is not grey, everywhere at once. The hand-painted…, set_accent(), A dark theme, so the viewport is what draws the eye. The colours themselves… (+2 more)

### Community 137 - "._write"
Cohesion: 0.20
Nodes (3): Set the value the way a hand on the control would., The value the track stands at ``x`` pixels across., Put a text box over the bar so an exact number can be typed.

### Community 138 - "workspace.py"
Cohesion: 0.09
Nodes (22): QScrollArea, QTabBar, can_take_key(), is_hotkey_click(), KeyGesture, QObject, QWidget, The gesture that puts a key on a control: Ctrl/Cmd, Alt and a click. It sits… (+14 more)

### Community 139 - "SectionGizmo"
Cohesion: 0.31
Nodes (4): Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo

### Community 140 - "_drag_over"
Cohesion: 0.22
Nodes (10): _drag_over(), _middle_of_the_view(), A drag of ``holder`` arriving at ``point`` in the window's coordinates. A real…, The gesture the whole thing rests on: drag it onto the model, it goes., A gesture that destroys something only fires where it clearly meant to., Refused at the door it would never reach the model; so it is let in., test_a_copy_dropped_on_the_model_is_thrown_away(), test_a_copy_is_let_into_the_window_wherever_it_arrives() (+2 more)

### Community 141 - ".mouseMoveEvent"
Cohesion: 0.17
Nodes (5): Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Apply the pull live, so the figure moves under the cursor., Apply the drag live, so the clay re-forms under the cursor.

### Community 142 - "paths.py"
Cohesion: 0.26
Nodes (13): available_matcaps(), _bundled_root(), image_path(), matcap_dir(), model_dir(), Path, Locations of the bundled resources. ``REFVIEW_RESOURCES`` overrides the search,…, Return PyInstaller's extracted application directory when frozen. (+5 more)

### Community 143 - "._chosen_armature"
Cohesion: 0.24
Nodes (6): QListWidgetItem, The armature the clay is being built on, or ``None``. An index past the end of…, The bones of the chosen armature, in the order the clay goes down. Every intact…, Take lengths of wire out of the clay, or put them back. A tick on a row that…, Put the clay on all of the wire, or take it off all of it., Write which lengths of wire take clay, as one undoable step.

### Community 144 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 145 - "._draw_hud"
Cohesion: 0.29
Nodes (5): QRectF, QFont, A short line in one corner of the frame; returns where it went. For an exported…, Text as filled outlines; see :func:`markers.draw_text` for why., What the pose tool is waiting for.

### Community 146 - "mesh_renderer.py"
Cohesion: 0.24
Nodes (8): bind_default(), current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., Restore a framebuffer captured with :func:`current_framebuffer`., _ghost_depth_range(), OpenGL scene renderer: background, shaded mesh, wireframe, section and paint.…, Sum a see-through model into the ghost buffers, to be resolved after. Blending…, Where the form starts along the view, and how deep it is. The ghost weighs a…

### Community 147 - "_clone_preview"
Cohesion: 0.31
Nodes (5): _clone_preview(), _pull_preview(), Point the preview at the settings it edits. The object itself, not a copy: this…, The matcap image, in the orientation the renderer uploads it. ``None`` for the…, The matcap image this is drawing, for a copy of it to draw too.

### Community 148 - "ndarray"
Cohesion: 0.25
Nodes (7): _empty(), ndarray, A level with no place in it: nearest direction wins, as before., The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to., _split(), _summarise()

### Community 149 - "WholeFaceToggles"
Cohesion: 0.14
Nodes (10): QApplication, QObject, Making the whole of a switch the part you can press. The theme turns every…, Turns a press anywhere on a switch into a click on it., Put the rule in place for every switch in the application., WholeFaceToggles, The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter. (+2 more)

### Community 150 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 152 - "._built"
Cohesion: 0.33
Nodes (4): QImage, QRect, Where the sphere goes: square, centred, above the legend., The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…

### Community 153 - ".set_value"
Cohesion: 0.25
Nodes (4): QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end.

### Community 154 - "restored"
Cohesion: 0.29
Nodes (7): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., A window with the saved layout out of the way, and put back after. Shown,…, A second window, built from a layout the first one saved. The point is…, restored(), window()

### Community 156 - "._step"
Cohesion: 0.29
Nodes (3): Command, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…

### Community 158 - "._commit_node_drag"
Cohesion: 0.33
Nodes (3): Record the finished gesture: a move, a resize, or a plain click. A press that…, Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…

### Community 159 - "LightSettings"
Cohesion: 0.40
Nodes (4): LightSettings, A key light, an opposing fill and a hemispherical ambient term., Material parameters shared by the analytic shading modes., SurfaceSettings

### Community 162 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 163 - ".update_enabled"
Cohesion: 0.17
Nodes (6): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., The armature the selected row stands for, when the row is not a node., Highlight the row for a node picked in the view., Highlight the row for a landmark picked in the view.

### Community 164 - "sample_count"
Cohesion: 0.50
Nodes (3): How many samples the framebuffer bound right now is drawing with. One where…, sample_count(), How many samples this view is really drawing with, or ``None``. Asked of GL…

### Community 165 - "test_spatial.py"
Cohesion: 0.26
Nodes (11): _grid(), The picking accelerator: it must be fast without changing any answer., A bumpy height field, so rays hit different triangles at different depths., The pruned candidate set must never miss the true intersection., Every parent must enclose its children, or a ray could slip past a leaf., test_a_batch_of_rays_gets_the_same_candidates_as_one_at_a_time(), test_a_ray_that_misses_the_model_is_pruned_away(), test_every_triangle_lands_in_exactly_one_leaf() (+3 more)

### Community 166 - ".refresh_list"
Cohesion: 0.16
Nodes (6): QTreeWidgetItem, Run a row's edit once Qt has finished delivering the current signal. Committing…, The landmarks in the preset's own order, top of the figure down. Placement…, Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing., Commit a renamed or re-checked row, if anything actually changed.

### Community 167 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 168 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 170 - "_height_of"
Cohesion: 0.40
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 171 - "_file_drag"
Cohesion: 0.17
Nodes (12): QMimeData, _drop_on(), The end of the gesture: the payload a drag carries, delivered., Drop ``mime`` on the top-left of ``panel``; was it taken? The caller keeps hold…, test_a_drop_carrying_a_control_takes_a_copy_of_it(), test_a_drop_carrying_something_else_is_refused(), test_a_drop_naming_a_control_that_is_gone_is_refused(), _file_drag() (+4 more)

### Community 172 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 174 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 179 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 180 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 181 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 182 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 183 - "test_the_disc_samples_where_the_shader_would"
Cohesion: 0.33
Nodes (6): parametrize, ``sampleMatcap``, transcribed from the GLSL, for a camera down +z. Deliberately…, The mapping :func:`sample` uses, for one normal rather than a grid., _shader_uv(), test_the_disc_samples_where_the_shader_would(), _widget_uv()

### Community 185 - "welded"
Cohesion: 0.67
Nodes (3): ndarray, Which point each vertex really is, once copies of a position are one point., welded()

### Community 186 - "section"
Cohesion: 0.50
Nodes (4): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., section()

### Community 187 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `SectionAxis`, `plane_axes`, `ExportLook`, `SkeletonStore`, `ViewerState`, `Skeleton`, `mesh_renderer.py`, `SectionSettings`, `plane_volume.py`, `TriangleIndex`, `PlaneSettings`, `test_plane_clusters.py`, `test_spatial.py`, `SurfacePicker`, `.transformed`, `gltf_loader.py`, `ExportVideoDialog`, `VideoSettings`, `test_forms.py`, `FilmExport`, `welded`, `PrimaryForm`, `test_skeleton.py`, `load_obj`, `test_plane_solids.py`, `PoseTool`, `default_matcap_pixels`, `Bounds`, `raycast_mesh`, `test_forms_panel.py`, `compute_vertex_normals`, `forms.py`, `core/__init__.py`, `MeshBuffers`, `load_mesh`, `ShadingMode`, `test_a_moving_view_reads_the_last_pass_and_asks_again_once_it_has_settled`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `test_preferences.py`, `._buried_nodes`, `ExportLook`, `._place_form_landmark`, `MainWindow`, `SectionGizmo`, `main_window.py`, `.mouseMoveEvent`, `ViewerState`, `QPointF`, `._commit_node_drag`, `PlaneSettings`, `sample_count`, `film_export.py`, `SurfacePicker`, `ExportVideoDialog`, `._place_joint`, `test_forms.py`, `FilmExport`, `ArmatureTool`, `MeasureTool`, `PrimaryForm`, `PoseTool`, `NavigationController`, `.__init__`, `OverlayParts`, `._picker`, `core/__init__.py`, `._sync_scene`, `.mouseReleaseEvent`, `._place_armature_node`, `AddItem`, `ViewportOverlay`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera` to `camera.py`, `SceneRenderer`, `README.md`, `test_navigation.py`, `._draw_hud`, `mesh_renderer.py`, `QPointF`, `BookmarkStore`, `.pan`, `test_camera.py`, `SurfacePicker`, `ArmatureTool`, `Session`, `PoseTool`, `NavigationController`, `Bounds`, `compute_vertex_normals`, `core/__init__.py`, `test_a_moving_view_reads_the_last_pass_and_asks_again_once_it_has_settled`, `AddItem`, `ViewportOverlay`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `OverlayParts`) actually correct?**
  _`ViewerState` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._