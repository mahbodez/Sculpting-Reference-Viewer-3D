# Graph Report - reference-viewer  (2026-09-18)

## Corpus Check
- 157 files · ~503,862 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5420 nodes · 12519 edges · 190 communities (178 shown, 12 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 596 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `82c89fec`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- form_group
- test_preferences.py
- main_window.py
- Viewport
- state.py
- settings.py
- MainWindow
- Stroke
- GifWriter
- camera.py
- SceneRenderer
- widgets.py
- Panel
- MeshBuffers
- Armature
- README.md
- ViewerState
- Skeleton
- mesh_renderer.py
- CameraPanel
- PosePanel
- ShaderProgram
- test_hotkeys.py
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- Writer
- SectionSettings
- ndarray
- ControlsWindow
- TriangleIndex
- ShadingPanel
- PlaneSettings
- test_camera.py
- test_plane_clusters.py
- WakeLock
- sample
- MatcapPreview
- Frame
- film_export.py
- test_viewport_markers.py
- Camera
- Wires
- ValueSlider
- gltf_loader.py
- ExportVideoDialog
- open_writer
- landmarks.py
- Agent Graph-First Instructions
- VideoSettings
- plane_axes
- test_matcap_preview.py
- test_armature.py
- ArmaturePanel
- SetAttributes
- HotkeyMap
- FilmExport
- FormsPanel
- PlanesPanel
- test_skeleton.py
- StrokeBuffers
- Workspace
- ui/hotkeys.py
- test_forms.py
- application.py
- MeasureTool
- PointEdit
- PrimaryForm
- pose_panel.py
- test_objects.py
- AnnotatePanel
- test_plane_solids.py
- ObjectTool
- session.py
- PoseTool
- texture.py
- load_matcap_pixels
- test_custom_panels.py
- ObjectsEdit
- core/preferences.py
- ._draw_hud
- NavigationController
- Bounds
- picking.py
- test_forms_panel.py
- solid_count
- SectionGizmo
- viewport.py
- MatcapPanel
- ColorButton
- FrameBar
- _Encoder
- .mousePressEvent
- test_elements.py
- annotation.py
- Mesh
- ReflowLayout
- Measurement
- section.py
- OrientationSettings
- clone.py
- test_skin.py
- Path
- ._turn
- .mouseReleaseEvent
- test_panel_docks.py
- MarkerVisibility
- ._place_armature_node
- QPointF
- test_navigation.py
- DockTitle
- test_reflow.py
- .source_mesh
- clay_lumps
- plane_volume.py
- ._build_objects
- test_open_files.py
- block_splits
- .point
- AddItem
- ViewportOverlay
- .split
- ArmatureStore
- _NameOnlyDelegate
- _tab_switch
- Reflow
- Command
- SectionPanel
- measure_panel.py
- ._sync_scene
- .stage_images
- AnnotateTool
- ExportLook
- make_switch
- preview
- kept_off
- .install
- OverlayParts
- watch_keys
- ._add_skeleton
- _drag_over
- stone_field
- ._build
- _clone_preview
- ._picker
- .update_enabled
- ReplaceItems
- test_tab_switches.py
- ._draw_annotation
- .dress_tabs
- _shifts
- test_resetting_the_layout_puts_the_docks_back_at_once
- union_field
- carve
- restored
- test_resetting_keeps_the_panels_built_by_hand
- ._on_bone_toggled
- test_the_switch_is_not_squeezed_to_nothing
- shaders.py
- .paintGL
- .read
- test_contour_shading.py
- .column_of
- FormRun
- Human Skin renderer
- test_spatial.py
- _wire_frame
- coarse_lattice
- app
- sample_count
- _height_of
- _file_drag
- .pan
- _NameOnlyDelegate
- ._active_changed
- panel
- raycast_mesh
- test_the_switch_on_a_dock_bar_is_the_panels_own_visibility
- quad
- app
- test_a_session_saved_without_panels_leaves_the_ones_open_alone
- test_a_panel_does_not_cover_its_own_title
- skin_detail.py
- test_a_panel_can_be_taken_away_and_another_built_after_a_restore
- test_loading_a_session_over_a_restored_layout_survives
- test_the_dock_of_a_panel_taken_away_is_used_again
- ModelPanel
- ui/preferences.py
- ._commit_node_drag
- test_a_reused_dock_does_not_bring_the_old_panels_contents_with_it

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 192 edges
2. `ViewerState` - 147 edges
3. `Viewport` - 146 edges
4. `Camera` - 95 edges
5. `Skeleton` - 90 edges
6. `MainWindow` - 90 edges
7. `Armature` - 81 edges
8. `PrimaryForm` - 79 edges
9. `PlaneSettings` - 69 edges
10. `SurfacePicker` - 69 edges

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

## Communities (190 total, 12 thin omitted)

### Community 0 - "form_group"
Cohesion: 0.10
Nodes (19): QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row(), The preferences as they stand. Treat as read-only; use :meth:`set`., QWidget, Fill in the groups. A switch with nothing to put in the caption column is given…, Every command with its keys, each key a box that takes one keystroke. The list… (+11 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.07
Nodes (43): Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, app(), model(), fixture, What the artist prefers: kept apart from the document, and acted upon. Two…, An external drive that is not plugged in is not an empty gallery. (+35 more)

### Community 2 - "main_window.py"
Cohesion: 0.06
Nodes (53): QRunnable, check_for_update(), fetch_latest_release(), is_newer(), _macos_root_certificates(), _padded(), parse_version(), RuntimeError (+45 more)

### Community 3 - "Viewport"
Cohesion: 0.06
Nodes (14): QOpenGLWidget, Renders the scene and turns mouse gestures into camera and tool actions., Slide the view so a point sits at the centre, keeping the angle., The gesture a key press chooses, if the transform tool is armed to hear it., A form changed: work its clay out again and redraw., Hand the renderer how solid each object is now; nothing else moved., End any film being recorded, and wait for its thread to really stop. For…, The document being drawn. (+6 more)

### Community 4 - "state.py"
Cohesion: 0.05
Nodes (39): concatenated(), Several meshes as one, in the coordinates they already stand in. The units are…, The triangles of ``mesh`` named by index, with only the vertices they use., submesh(), _bare(), duplicate_object(), merge_objects(), ObjectSettings (+31 more)

### Community 5 - "settings.py"
Cohesion: 0.03
Nodes (102): GridSettings, Which planes carry a grid, how fine it is, and how it fades., Coefficients, PlaneAxes, PlaneSet, Reading the planes of a form out of the model's own normals. The grid quantiser…, One level of a fit: the planes the shader is to quantise against. A plane is a…, The planes a model falls into, at every count. Built once per mesh and per… (+94 more)

### Community 6 - "MainWindow"
Cohesion: 0.04
Nodes (29): MainWindow, _plain(), QAction, QMainWindow, Put every panel button and menu entry where the tools now stand. Only one tool…, Swap between the eraser and the drawing mode it was called from., Open the preferences, on one group when the menu asked for one., Push the preferences that this window's own parts hold a copy of. The store has… (+21 more)

### Community 7 - "Stroke"
Cohesion: 0.11
Nodes (19): AnnotationStore, An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., One painted polyline lying on the surface., Stroke, line_stroke(), Surface annotations: erasing, splitting and the geometry handed to GL., A stroke running along +X, one unit apart, with +Y normals. (+11 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "camera.py"
Cohesion: 0.05
Nodes (62): Quat, Quat4, Named camera positions the artist can jump between while sculpting., Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`. (+54 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.06
Nodes (41): Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, light_directions(), normal_matrix(), ndarray, Point the shading pass at the shadow map and the occlusion buffer., Flood the exposed interior with a flat colour so the cut reads solid. The… (+33 more)

### Community 11 - "widgets.py"
Cohesion: 0.05
Nodes (61): QScrollArea, can_clone(), clone(), A working copy of ``source``, or ``None`` if its kind cannot be copied., Make every control under ``root`` that can be copied Alt-draggable. A group is…, watch_tree(), The small controls that are not sliders: a swatch, and a point in space., A panel the artist builds, out of copies of controls from the fixed ones. The… (+53 more)

### Community 12 - "Panel"
Cohesion: 0.12
Nodes (8): Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Whether what this panel draws is on screen, or ``None`` if it draws nothing.…, Show or hide what this panel draws; see :meth:`shown`., Ignore widget signals for the duration of the block., Nothing: the reflow already packs its groups against the top. Kept because…

### Community 13 - "MeshBuffers"
Cohesion: 0.09
Nodes (12): _ghost_depth_range(), MeshBuffers, Forget the contents without releasing the buffer objects., Where the form starts along the view, and how deep it is. The ghost weighs a…, Replace the model: the whole scene as one mesh, and the objects it is made of.…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are… (+4 more)

### Community 14 - "Armature"
Cohesion: 0.02
Nodes (118): BoneRef, LandmarkRef, Armature, ArmatureNode, ArmatureSettings, Bone, BoneLabels, PlacedLandmark (+110 more)

### Community 15 - "README.md"
Cohesion: 0.12
Nodes (20): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, refview (+12 more)

### Community 16 - "ViewerState"
Cohesion: 0.05
Nodes (43): ObjectRecord, What a session writes down about an object; the mesh itself stays in its file., ndarray, Path, Snapshot, A rest mesh as a file would store it, so that re-orienting it comes back to…, Open every object a session names, as the whole scene., Everything the viewer displays, plus change notifications. (+35 more)

### Community 17 - "Skeleton"
Cohesion: 0.06
Nodes (24): _matrix16(), A copy with the rest translation replaced and the frame kept., A tree -- or a forest -- of joints and the pose they stand in., Every joint, parents before children. A file may list a child before its…, Every joint below ``index``, nearest first., Every joint's transform in scene space, as ``(n, 4, 4)``. With ``rest`` the…, Where every joint sits, as ``(n, 3)``., Every ``(parent, child)`` pair, parents first. (+16 more)

### Community 18 - "mesh_renderer.py"
Cohesion: 0.05
Nodes (31): AccumTarget, bind_default(), ColorTarget, current_framebuffer(), DepthTarget, FrameTarget, GeometryTarget, Offscreen render targets used by the high-quality, ghost and smoothing passes.… (+23 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): CameraPanel, QListWidgetItem, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "PosePanel"
Cohesion: 0.07
Nodes (16): PosePanel, QTreeWidgetItem, QWidget, Run a row's edit once Qt has finished delivering the current signal., Arms the pose tool, lists the joints and poses the selected one., Adopt the viewport's tools: the pose tool, and the armature's for its selection., Lay an armature under the selected skeleton as it is posed., Guess the humanoid roles off the joint names; returns how many were found. (+8 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): Fill the shader's table with a level, if it is not already in it., ndarray, RuntimeError, Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "test_hotkeys.py"
Cohesion: 0.16
Nodes (14): _click(), _map(), Hotkeys: the map, the store, the binder, and the gesture that assigns one., End to end: the filter is on the panel's buttons and the window hears it., A key given to something else comes off what had it, and the map says what that…, test_a_choice_about_a_control_not_yet_seen_is_kept(), test_a_command_keeps_its_shipped_keys_until_the_artist_moves_them(), test_a_control_says_its_key_in_its_tooltip_and_a_tool_button_in_its_name() (+6 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.08
Nodes (21): _names(), The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as…, Or there would be no way to turn one back on., A limb is four bones, and deciding not to block the arms in is one decision.…, It is rebuilt on every change, and ticking one row of a selected limb would be… (+13 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.12
Nodes (9): MeasurePanel, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn. (+1 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.10
Nodes (11): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around. (+3 more)

### Community 26 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 27 - "SectionSettings"
Cohesion: 0.11
Nodes (22): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, Unit axis, or ``None`` for a custom direction., A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn. (+14 more)

### Community 28 - "ndarray"
Cohesion: 0.13
Nodes (21): _back_inside(), dual_contour(), _flat_mesh(), ndarray, The surface where ``value`` changes sign, one vertex per lattice cell. Each…, The gradient of a lattice field, by central differences. Which is the direction…, Drop the loose pieces, keeping the form and anything of its size. A block is a…, Read lattice fields at places between their corners, straight-line. Nearest-… (+13 more)

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
Cohesion: 0.04
Nodes (41): The best ``count`` planes, or as many as the model supports. A model whose…, film_key(), What a film depends on. Everything that changes the shape of any stage, and…, Holds the working state between one turn of the sliders and the next.…, Drop everything held, so the next call starts from the fit., The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache (+33 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (59): The joint list with ``index`` resting at ``target`` and its children left be., angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad() (+51 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (32): c_void_p, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., Holds sleep off while the window that owns it is the one in front. The class… (+24 more)

### Community 36 - "sample"
Cohesion: 0.20
Nodes (8): QImage, QRect, Draw the matcap onto a sphere of ``size`` pixels, graded. Returns ``(size,…, The matcap as a picture, at its own resolution. Square and opaque, with the…, Where the sphere goes: square, centred, above the legend., The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…, sample(), test_the_disc_is_a_disc()

### Community 37 - "MatcapPreview"
Cohesion: 0.09
Nodes (14): QMenu, MatcapPreview, _push_preview(), Path, QSize, QWidget, A matcap on a sphere, which is also how the matcap is graded., Offer the picture back as a file: as graded here, or as it came. A grading… (+6 more)

### Community 38 - "Frame"
Cohesion: 0.07
Nodes (26): carried(), _push_frame(), Nothing: each row inside the copy is linked on its own., Read a drag's payload back, or ``None`` if it is not one of ours., CustomPanel, _detach(), QFormLayout, QWidget (+18 more)

### Community 39 - "film_export.py"
Cohesion: 0.07
Nodes (21): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+13 more)

### Community 40 - "test_viewport_markers.py"
Cohesion: 0.13
Nodes (18): app(), event(), fixture, parametrize, Marker interaction, selection identity, and section dragging regressions., The cues that share the overlay's text path get its halo too., A grid facing the camera, through the point wherever it has got to., test_contour_controls_follow_the_mode_and_pin_the_view() (+10 more)

### Community 41 - "Camera"
Cohesion: 0.08
Nodes (18): Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Rays through a batch of pixels, as ``(origins, unit directions)``, ``(N, 3)``…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Project ``(N, 3)`` world points to ``(xs, ys, ndc_depths)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target). (+10 more)

### Community 42 - "Wires"
Cohesion: 0.05
Nodes (43): QThread, Film, The stage at ``index``, clamped to what has actually been recorded., A whole making, from the coarsest stage to the one the slider asks for. Held by…, An armature, as the clay reads it: where each length of wire runs. The order…, How many lumps the wire itself asks for., What a cache has to compare to know the wire has not moved., Wires (+35 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (11): _pull_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end., Set the value the way a hand on the control would., The value the track stands at ``x`` pixels across. (+3 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.07
Nodes (42): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), _first_skin(), GltfLoadError, load_gltf(), _local_transform() (+34 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.11
Nodes (13): QProgressDialog, even(), ExportVideoDialog, Path, QDialog, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+5 more)

### Community 46 - "open_writer"
Cohesion: 0.08
Nodes (28): _encode_arguments(), _encoders(), ffmpeg_path(), _FFmpegWriter, _no_window(), open_writer(), Path, RuntimeError (+20 more)

### Community 47 - "landmarks.py"
Cohesion: 0.09
Nodes (30): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _humanoid_landmarks(), _kept_laying(), median_plane() (+22 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "VideoSettings"
Cohesion: 0.18
Nodes (7): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, TestTiming

### Community 50 - "plane_axes"
Cohesion: 0.08
Nodes (38): _empty(), plane_axes(), ndarray, A level with no place in it: nearest direction wins, as before., How much surface each vertex stands for: a third of each triangle on it.…, The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to., Split the mesh's normals into planes, keeping every count on the way. (+30 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.12
Nodes (28): QPoint, _drag(), parametrize, The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc., Dragging further than the range goes is not a negative gamma., Alt and a drag copies a control; the disc must not swallow that. (+20 more)

### Community 52 - "test_armature.py"
Cohesion: 0.06
Nodes (73): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _chain(), _derived(), _figure(), ndarray (+65 more)

### Community 53 - "ArmaturePanel"
Cohesion: 0.05
Nodes (29): QTreeWidget, ArmaturePanel, QPushButton, QWidget, Arms the armature tool, lists its nodes and runs the guided presets., Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, Adopt the viewport's tool, which is where the guided run lives. (+21 more)

### Community 54 - "SetAttributes"
Cohesion: 0.13
Nodes (9): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, QTreeWidgetItem, Run a row's edit once Qt has finished delivering the current signal. Committing…, Record an edit the viewport's tool worked out., Join two nodes of one armature, if they are two and they are one armature., Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing. (+1 more)

### Community 55 - "HotkeyMap"
Cohesion: 0.12
Nodes (8): HotkeyMap, Whether the artist has moved this command off what it ships with., Every command with keys on it, declared or not, as id -> keys., Only the choices; the commands and their defaults belong to the code., The commands, their shipped keys, and the artist's changes to them., Take a command off the list, keeping any choice made about it., The keys on a command now: the artist's choice, else what it ships with., The map as it stands. Treat as read-only; change it through the store.

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (12): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+4 more)

### Community 57 - "FormsPanel"
Cohesion: 0.04
Nodes (32): FormsPanel, QTreeWidgetItem, Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Begin a run against a fresh form: a preset's walk, or a freeform's., Take up the selected freeform again, so more landmarks can go on it. The same…, The freeform the highlighted row belongs to, when no run is on. (+24 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.18
Nodes (6): PlanesPanel, Put the design matrix back the way it reads a figure., Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Breaks the form into planes, in the shading or in the geometry itself., Re-read the armatures and what the chosen one is laying down. Called whenever…

### Community 59 - "test_skeleton.py"
Cohesion: 0.10
Nodes (33): Which document joint each rig joint answers to. Returns two ``(j,)`` arrays:…, The model as ``skeleton`` poses it, or ``rest`` itself when it cannot. Linear…, skinned_mesh(), _arm(), ndarray, parametrize, Skeletons: the joint tree, posing, skinning, and where skeletons come from., The strip as a GLB with a two-joint skin, optionally saved mid-bend. (+25 more)

### Community 60 - "StrokeBuffers"
Cohesion: 0.14
Nodes (13): Replace the reference grids; pass ``None`` to take them away. ``lines`` is a…, build_segment_vertices(), build_vertices(), _expand(), ndarray, Geometry for the surface annotations and the cross-section contour. Strokes are…, A single vertex buffer holding every visible stroke., Replace the buffer contents with a prepared vertex block. (+5 more)

### Community 61 - "Workspace"
Cohesion: 0.07
Nodes (22): QDockWidget, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top., _number_in(), QMainWindow, QObject, QSettings, QWidget (+14 more)

### Community 62 - "ui/hotkeys.py"
Cohesion: 0.04
Nodes (59): QKeySequence, QKeySequenceEdit, QShortcut, ask_for(), assign(), command_for(), control_of(), decorate() (+51 more)

### Community 63 - "test_forms.py"
Cohesion: 0.05
Nodes (75): One convex piece of a form: its hull vertices and outward-wound faces., The hull of the points with its faces bowed out; see :func:`rounded_hull`., The longest side of the box the solid sits in., Whether a point lies inside, or within ``slack`` of the surface., Solid, _across(), blend_rings(), build_head() (+67 more)

### Community 64 - "application.py"
Cohesion: 0.06
Nodes (40): ArgumentParser, Namespace, QSplashScreen, Application, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font() (+32 more)

### Community 65 - "MeasureTool"
Cohesion: 0.14
Nodes (8): MeasureTool, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., Where a click at ``(x, y)`` would put a point. With free placement the point…, Where a grabbed endpoint should move to. Free placement -- and a drag that…

### Community 66 - "PointEdit"
Cohesion: 0.07
Nodes (16): _clone_point(), CloneGesture, Link, _pull_point(), _Pulse, _push_point(), QObject, One timer for every copy in the window. (+8 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.03
Nodes (95): FormLandmarkRef, DegenerateHullError, The points are flat, collinear or too few to hold any volume., build_freeform(), _centre(), form_landmark_title(), form_spec(), FormFill (+87 more)

### Community 68 - "pose_panel.py"
Cohesion: 0.06
Nodes (48): Buried, What becomes of the part of the armature the model is standing in front of. An…, What to call the joint filling a humanoid slot: ``"knee.L"`` is ``"Knee L"``., role_name(), armature_from_skeleton(), armature_root(), build_humanoid_skeleton(), detail_joints() (+40 more)

### Community 69 - "test_objects.py"
Cohesion: 0.12
Nodes (31): Path, Where an object stands relative to its parent: an affine placement. Held as the…, Transform, app(), _key(), _mouse(), _overridden(), fixture (+23 more)

### Community 70 - "AnnotatePanel"
Cohesion: 0.20
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 71 - "test_plane_solids.py"
Cohesion: 0.03
Nodes (152): auto_smooth(), A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), film_of(), parametrize (+144 more)

### Community 72 - "ObjectTool"
Cohesion: 0.12
Nodes (14): _axis_param(), Gizmo, _Grip, ObjectTool, ndarray, The three directions the arms run along, in world space. A move and a turn are…, Where the gizmo for an object at ``world`` falls on screen, or ``None`` if…, Which handle a screen point is over: ``"centre"``, ``"x"``, ``"y"``, ``"z"`` or… (+6 more)

### Community 73 - "session.py"
Cohesion: 0.04
Nodes (52): Shift-snapped orbiting (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, _coerce() (+44 more)

### Community 74 - "PoseTool"
Cohesion: 0.07
Nodes (42): JointRef, How skeletons are drawn, and how the pose tool behaves., SkeletonSettings, PoseTool, _project_many(), The nearest unlocked joint of a visible skeleton under the cursor., The bone under the cursor, named by the joint at its far end. Taking hold of a…, The pose shift that puts joint ``index`` at ``target``, children and all. (+34 more)

### Community 75 - "texture.py"
Cohesion: 0.07
Nodes (16): OpenGL rendering layer: shader programs, textures and the scene renderer., DataTexture, default_matcap_pixels(), ndarray, Matcap texture loading and upload, and the small data table beside it., An RGBA16F 2D texture with clamped edges and mipmapped minification., A tileable RGBA16F volume, trilinear and mipmapped, for world-space detail.…, Store a ``(depth, height, width, 4)`` float array. (+8 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.15
Nodes (23): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+15 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.07
Nodes (23): QMimeData, app(), custom(), _drop_on(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error., A group is not a row, so it goes ahead of the group it was dropped on. (+15 more)

### Community 78 - "ObjectsEdit"
Cohesion: 0.14
Nodes (6): ObjectsEdit, Command, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, An edit to the objects -- a move, a parenting, a removal -- as two snapshots.…, _RenameObject

### Community 79 - "core/preferences.py"
Cohesion: 0.11
Nodes (20): _as_kind_of(), _clamp(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any (+12 more)

### Community 80 - "._draw_hud"
Cohesion: 0.18
Nodes (9): QRectF, QColor, QFont, A short line in one corner of the frame; returns where it went. For an exported…, What the forms tool is waiting for, said in as few lines as it takes., Text as filled outlines; see :func:`markers.draw_text` for why., What the pose tool is waiting for., What the armature tool is waiting for, said in as few lines as it takes. (+1 more)

### Community 81 - "NavigationController"
Cohesion: 0.08
Nodes (16): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Degrees of yaw per pixel, signed by whether the drag is inverted. (+8 more)

### Community 82 - "Bounds"
Cohesion: 0.06
Nodes (35): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, build_grid(), GridLines, nice_step(), Reference grids on the three axis planes, fading with distance. A grid gives…, Segments, with their colours and widths, ready for the stroke buffer. (+27 more)

### Community 83 - "picking.py"
Cohesion: 0.17
Nodes (12): Hit, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., snap_to_vertex(), DepthDrag, Shared marker appearance, visibility, and constrained depth gestures., A grid across the depth axis, at the depth the point has reached. Returns… (+4 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.12
Nodes (29): app(), _click(), panel(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The… (+21 more)

### Community 85 - "solid_count"
Cohesion: 0.15
Nodes (15): block_count(), piece_count(), How many blocks a count of planes asks the stone to be cut into. One at the…, How many lumps a count of planes asks the clay to be built out of. The masses…, How many solids the form is made of, whichever way it is being worked., solid_count(), The line under the geometry slider: how the form is being worked. ``wires`` is…, _sculpt_summary() (+7 more)

### Community 86 - "SectionGizmo"
Cohesion: 0.20
Nodes (7): A screen-space rail for sliding the cutting plane along its normal. The rail…, Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo, The rail stands still while the camera moves, and never leaves the frame., test_section_rail_is_a_screen_space_cue_at_the_right_edge()

### Community 87 - "viewport.py"
Cohesion: 0.05
Nodes (55): convex_hull(), flat_mesh(), merged(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, The outward unit normal at each vertex: the area-weighted mean of its faces'. A… (+47 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.15
Nodes (10): MatcapPanel, Rebuild the thumbnail list from the resources folder., The disc was dragged: show the renderer and the numbers what it did., A different matcap: the disc draws whichever one is on the model., Put the numbers back in line with the settings, and redraw the disc. Separate…, Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, It is the panel's main control; a click on a bar must not take it away. (+2 more)

### Community 89 - "ColorButton"
Cohesion: 0.11
Nodes (12): _clone_swatch(), _pull_swatch(), _push_swatch(), _AxisBox, ColorButton, QColor, QDoubleSpinBox, QSize (+4 more)

### Community 90 - "FrameBar"
Cohesion: 0.08
Nodes (16): FrameBar, framed(), QFormLayout, QPainter, QSize, QWidget, The mark beside a group's name: filled when open, a ring when shut. It is the…, The rows inside the frame. ``layout()`` is the frame's own, which stacks the… (+8 more)

### Community 91 - "_Encoder"
Cohesion: 0.25
Nodes (5): Queue, _Encoder, QObject, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 92 - ".mousePressEvent"
Cohesion: 0.12
Nodes (7): ndarray, Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on., Take hold of a joint -- or of a bone, by its far end., Take hold of a form's landmark, to move it or just to say which one it is.

### Community 93 - "test_elements.py"
Cohesion: 0.07
Nodes (23): app(), fixture, Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., A matcap has no light to aim, so the Light group goes -- and its space. The… (+15 more)

### Community 94 - "annotation.py"
Cohesion: 0.14
Nodes (10): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a…, The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that… (+2 more)

### Community 95 - "Mesh"
Cohesion: 0.04
Nodes (83): Qt-free geometry, camera and document model for the reference viewer., compute_vertex_normals(), _gathered(), load_mesh(), Path, One entry point for every mesh format the viewer reads. Callers ask for a path…, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Write a mesh out; only OBJ is written, whatever the suffix asked for. (+75 more)

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - "Measurement"
Cohesion: 0.07
Nodes (20): Measurement, MeasurementSettings, MeasurementStore, ndarray, Named point-to-point measurements and their presentation options., The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface. (+12 more)

### Community 98 - "section.py"
Cohesion: 0.20
Nodes (8): Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Which side of the plane survives the cut., SectionAxis, SectionMode, Cross-section controls: the cutting plane, what it keeps and how it reads.

### Community 99 - "OrientationSettings"
Cohesion: 0.11
Nodes (23): OrientationSettings, Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., UpAxis (+15 more)

### Community 100 - "clone.py"
Cohesion: 0.06
Nodes (59): QAbstractButton, QComboBox, QLineEdit, QSlider, QSpinBox, _begin(), _clone_button(), _clone_check() (+51 more)

### Community 101 - "test_skin.py"
Cohesion: 0.10
Nodes (22): build_scene(), ndarray, Stackless BVH tables for the OpenGL 3.3 skin tracer (no compute extension).…, Build on a worker from the immutable meshes currently drawn by the renderer., Pack a linear texel array within the driver's actual 2D texture limit., texture_table(), TraceScene, gl_context() (+14 more)

### Community 102 - "Path"
Cohesion: 0.13
Nodes (12): opens_as(), Path, Pick up whatever was last being worked on, if that was asked for. A session…, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window., Add a model to the scene beside what is already there., Open a file by what it is: a model, a session or a matcap. The one door every… (+4 more)

### Community 103 - "._turn"
Cohesion: 0.13
Nodes (9): _angle(), Redraw from the settings, which something else has changed., Put the grading back, which is the one thing a disc cannot show., Turn the matcap by the angle the cursor swept about the centre. By angle and…, Two grades on one drag: one along each axis of the movement. Both move together…, Keep the angle in -180 to 180, the range the setting is stored in., The angle of ``point`` about ``centre``, anticlockwise with y upwards., An angle difference brought back into -pi to pi. (+1 more)

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.09
Nodes (9): Record the finished drag as a single undo step., Record the finished drag as one step, or read a press as a selection., Make the object under the cursor the active one., Which skeleton an edit lands in: the selected one, else the last., Add a joint where the click landed, under the selected joint., Record the finished pull as one step, or read a press as a selection., Which form an edit lands in, counting a guided run as binding., Record the landmark a guided form is asking for. (+1 more)

### Community 105 - "test_panel_docks.py"
Cohesion: 0.14
Nodes (3): Each panel in a dock of its own, and putting the docks back next time. Two…, test_a_restored_copy_drives_the_new_windows_own_control(), test_the_layout_comes_back_through_the_settings()

### Community 106 - "MarkerVisibility"
Cohesion: 0.18
Nodes (5): MarkerVisibility, Cache surface occlusion by view and position for every kind of marker. The…, Whether the last pass is recent enough to be read instead of repeated., Mark these points as standing in front of the surface, untested. For frames…, Answer for a batch of points at once, ahead of being asked one by one. Every…

### Community 107 - "._place_armature_node"
Cohesion: 0.15
Nodes (6): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…, The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, A skeleton changed: redraw it., Hand the renderer a re-posed model and nothing else. For the frames of a pose…

### Community 108 - "QPointF"
Cohesion: 0.25
Nodes (9): QPointF, draw_rail(), draw_text(), One marker object for endpoints, nodes, landmarks and tool previews., Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, The screen-space cue for one degree of freedom. A vertical rail that fades out…, VisualMarker, project_visible_many() (+1 more)

### Community 109 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 110 - "DockTitle"
Cohesion: 0.13
Nodes (7): QToolButton, DockTitle, QSize, QWidget, The bar across the top of a dock: a switch, a name and two buttons., As tall as the bar really is. A dock puts the panel directly below its title…, StandardPixmap

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - ".source_mesh"
Cohesion: 0.24
Nodes (6): setter, The active object turned and centred but not posed or placed., The active object exactly as its file stored it., Set the active object's file mesh; its rest mesh is turned from it as at a load., The active object, made on the spot when a mesh is handed to an empty scene., Turn a freshly read mesh the right way up and centre it.

### Community 113 - "clay_lumps"
Cohesion: 0.16
Nodes (18): _box_facings(), clay_lumps(), clay_pieces(), fit_piece(), _frame(), grow_piece(), join_pieces(), Which three ways a lump of material runs. Columns, thinnest first. Thinnest… (+10 more)

### Community 114 - "plane_volume.py"
Cohesion: 0.18
Nodes (15): _axes(), encloses(), lattice(), lay_bed(), nearest_surface(), _passes(), Blocking a form in out of its own planes, from the outside or from a core. A…, Read the model onto a lattice, ready for solids to be laid on it. (+7 more)

### Community 115 - "._build_objects"
Cohesion: 0.17
Nodes (9): _NameOnlyDelegate, _ObjectTree, QPushButton, QStyledItemDelegate, QWidget, Allows in-place editing of the name column only., A tree whose rows can be dropped onto one another to hang one from another. Qt…, A strip of buttons that one form row can show or hide as a unit. (+1 more)

### Community 116 - "test_open_files.py"
Cohesion: 0.15
Nodes (11): app(), opened(), fixture, parametrize, Files arriving from outside: the command line, a drop, or the desktop's "Open…, One offscreen Qt application for the run; see test_film_recorder., What the window was asked to open, by kind, without loading anything., Finder sends the launching file as an event, which can land before the window. (+3 more)

### Community 117 - "block_splits"
Cohesion: 0.17
Nodes (12): block_labels(), block_splits(), blocks(), _cuts(), _hull_air(), The corners a hull round ``points`` holds that ``points`` do not fill. The hull…, Where a block might be cut in two: a direction, and a point to pass through.…, The greedy split, with every count along the way kept. The same walk… (+4 more)

### Community 118 - ".point"
Cohesion: 0.22
Nodes (5): ndarray, Closest surface intersection under the cursor, or ``None``., Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-…, Screen-to-world scale at a given depth along the view direction.

### Community 119 - "AddItem"
Cohesion: 0.08
Nodes (22): Camera motion is deliberately not undoable, AddItem, Append an item to a document list., Command, History, One reversible change, named for the undo menu., A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive… (+14 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.15
Nodes (14): project_visible(), Handle, QPainter, Project a world point, returning ``None`` when it is behind the camera., Draws measurements, tool previews, the orientation gizmo and the readout., Whether the last frame drew from stale occlusion answers., Draw everything over the scene. ``occlude`` off skips asking the surface which…, A line laid over its own dark outline, so it reads against anything. (+6 more)

### Community 121 - ".split"
Cohesion: 0.22
Nodes (6): ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, Normals padded to match the points, so callers can zip them freely., Break the stroke into the runs of points ``keep`` marks as surviving., _runs()

### Community 122 - "ArmatureStore"
Cohesion: 0.18
Nodes (4): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 124 - "_tab_switch"
Cohesion: 0.29
Nodes (7): The show/hide switch on the tab named ``title``, if it has one., Stacked behind another panel is where the switch is worth the most., It is fifteen pixels wide and carries no words, which is exactly the shape the…, _tab_switch(), test_a_panel_that_draws_nothing_gets_no_switch_on_its_tab(), test_a_tabbed_panel_still_shows_its_switch(), test_clicking_the_switch_on_a_tab_works()

### Community 125 - "Reflow"
Cohesion: 0.30
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 126 - "Command"
Cohesion: 0.20
Nodes (6): Command, Which keys do what, as the artist has decided rather than as it ships. A hotkey…, Something a key can be put on: what it is called, and what it ships with., Make a command known, or bring its label and default up to date., test_a_command_declared_after_its_key_was_given_away_arrives_without_it(), test_an_unknown_scope_is_refused()

### Community 127 - "SectionPanel"
Cohesion: 0.18
Nodes (7): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 128 - "measure_panel.py"
Cohesion: 0.12
Nodes (18): QIcon, _draw_glyph(), glyph(), lock_icon(), QColor, QPixmap, Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if… (+10 more)

### Community 129 - "._sync_scene"
Cohesion: 0.13
Nodes (7): Regenerate the pedestal and the cut contour when their settings move. Both are…, Rebuild the reference grids for the scene as it stands., The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on., Cut the mesh with each section plane and expand the result to strokes.

### Community 130 - ".stage_images"
Cohesion: 0.23
Nodes (7): QOpenGLFramebufferObject, QImage, One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A…, An offscreen target the frames are drawn into, made once per export.…, Draw the scene into ``surface`` and read it back as an image., Lay the overlay -- and the caption, if it was asked for -- on a frame. Painted…

### Community 131 - "AnnotateTool"
Cohesion: 0.11
Nodes (14): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses., Continue the open run with a hit, or end it where the ray missed. (+6 more)

### Community 132 - "ExportLook"
Cohesion: 0.09
Nodes (15): One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, ExportLook, What the frames are to look like, as against what they are of. Laid over the…, ``base`` with this export's choices laid over it., The line burned into the corner of the frame for ``stage``. Counted off the…, FakeViewport (+7 more)

### Community 133 - "make_switch"
Cohesion: 0.28
Nodes (6): make_switch(), QCheckBox, Put a show/hide switch at the left of the bar and return it., A square that is on or off, and is clickable all over. A check box decides…, The square that shows or hides what a panel draws. One is kept on each dock's…, Switch

### Community 134 - "preview"
Cohesion: 0.40
Nodes (5): app(), preview(), fixture, One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "kept_off"
Cohesion: 0.50
Nodes (4): kept_off(), Which points lie in the sleeve a length of wire declares round itself. The wire…, Which material lies under a length of wire that is to take no clay. Turning a…, within_sleeve()

### Community 136 - ".install"
Cohesion: 0.29
Nodes (6): QApplication, Put the rule in place for every switch in the application., The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter., test_a_switch_answers_a_press_anywhere_on_its_face(), test_alt_is_left_alone_so_a_switch_can_still_be_copied()

### Community 137 - "OverlayParts"
Cohesion: 0.22
Nodes (5): Which of the things drawn over the model belong in the frames., OverlayParts, ndarray, Every point the frame will ask the surface about, so it is asked once. Casting…, Which of the things drawn over the model are wanted this time. The viewport…

### Community 138 - "watch_keys"
Cohesion: 0.15
Nodes (13): can_take_key(), is_hotkey_click(), KeyGesture, QObject, QWidget, The gesture that puts a key on a control: Ctrl/Cmd, Alt and a click. It sits…, Whether a mouse press is the assignment gesture rather than a click., Whether a widget is the kind a key can sensibly be put on. A button or a switch… (+5 more)

### Community 139 - "._add_skeleton"
Cohesion: 0.18
Nodes (5): Add an empty skeleton, for a chain to be clicked into., Stand a proportioned humanoid skeleton in the model's box., Grow a skeleton out of the armature chosen in the box., Record a structural edit the viewport's tool worked out., Highlight a row, in the tree and in the view.

### Community 140 - "_drag_over"
Cohesion: 0.22
Nodes (10): _drag_over(), _middle_of_the_view(), A drag of ``holder`` arriving at ``point`` in the window's coordinates. A real…, The gesture the whole thing rests on: drag it onto the model, it goes., A gesture that destroys something only fires where it clearly meant to., Refused at the door it would never reach the model; so it is let in., test_a_copy_dropped_on_the_model_is_thrown_away(), test_a_copy_is_let_into_the_window_wherever_it_arrives() (+2 more)

### Community 141 - "stone_field"
Cohesion: 0.20
Nodes (10): Bed, block_bounds(), coarse_bounds(), point_support(), The lattice a form is worked on, and the model read onto it. Everything here…, The union of the blocks a labelling cuts the model into, and its facings. Stone…, The index range each block covers. ``(count, 3)`` lows and highs, inclusive. A…, Those ranges, read on the fine lattice the coarse one stands for. (+2 more)

### Community 142 - "._build"
Cohesion: 0.28
Nodes (4): Lay one length of wire earlier or later, as one undoable step., The armature the clay is being built on, or ``None``. An index past the end of…, Put the clay on all of the wire, or take it off all of it., Write which lengths of wire take clay, as one undoable step.

### Community 143 - "_clone_preview"
Cohesion: 0.16
Nodes (11): _clone_preview(), grade(), _pull_preview(), ndarray, Point the preview at the settings it edits. The object itself, not a copy: this…, The matcap image, in the orientation the renderer uploads it. ``None`` for the…, The matcap image this is drawing, for a copy of it to draw too., Apply the matcap grading to float RGB in 0-1, as the shader does. A… (+3 more)

### Community 144 - "._picker"
Cohesion: 0.10
Nodes (11): Rub out the stroke points under the eraser, live., Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Where the active object's gizmo falls on screen, or ``None``., Apply the pull live, so the figure moves under the cursor. (+3 more)

### Community 145 - ".update_enabled"
Cohesion: 0.29
Nodes (4): Hold the settings a recording is built from still while it runs. A film is a…, Show what this way of working needs, and put the rest away. A setting that does…, The bones of the chosen armature, in the order the clay goes down. Every intact…, What can be done to the list, given where the handle is and whether a film is…

### Community 146 - "ReplaceItems"
Cohesion: 0.14
Nodes (6): Any, Command, Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems

### Community 147 - "test_tab_switches.py"
Cohesion: 0.29
Nodes (7): app(), fixture, parametrize, The switch on each tab: it reads what the panel draws and writes it back. Every…, One offscreen Qt application for the run; see test_film_recorder., test_a_panel_that_draws_nothing_has_no_switch(), test_the_switch_is_the_panels_own_visibility_setting()

### Community 148 - "._draw_annotation"
Cohesion: 0.29
Nodes (4): Convert a 0-1 RGB tuple to a QColor., Preview the gesture under way; finished strokes are drawn in 3D., The cursor ring: the eraser's reach, or the width of the brush., to_qcolor()

### Community 149 - ".dress_tabs"
Cohesion: 0.29
Nodes (5): QTabBar, Hang a show/hide switch on every dock tab that wants one. A dock stacked behind…, The panel whose dock is called ``title``, if there is one., Let a strip of tabs keep its names, and scroll if they do not fit. Ten panels…, _widen()

### Community 150 - "_shifts"
Cohesion: 0.25
Nodes (8): _balloon(), close_gaps(), outside_points(), Fill the slots the lumps leave between them, without taking clay away. The…, Grow or shrink a solid by ``reach`` cells, one axis at a time. A separable…, Where the model stops: the corners just outside ``room``. ``(n, 3)``. Only the…, The pair of slices that read a lattice ``span`` cells over along ``axis``., _shifts()

### Community 152 - "union_field"
Cohesion: 0.25
Nodes (8): block_field(), piece_bounds(), One row of coordinates per axis over ``box``, shaped so they broadcast., The union of the blocks, as a field whose zero is its surface. Each block is…, The box a lump of clay lives in, read off the six facings of its frame. Those…, The union of a set of convex solids, as a field whose zero is its surface. The…, _rows(), union_field()

### Community 153 - "carve"
Cohesion: 0.32
Nodes (8): carve(), _corner_facings(), facings(), fitted_facings(), The form ``directions`` leave of the model, worked one way or the other.…, Twenty-six directions round a cube, for judging how much air a block holds.…, The supporting directions a block may be cut along. ``(m, 3)``. The twenty-six…, The form's own facings alone, both ways round and without duplicates. What a…

### Community 154 - "restored"
Cohesion: 0.29
Nodes (7): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., A window with the saved layout out of the way, and put back after. Shown,…, A second window, built from a layout the first one saved. The point is…, restored(), window()

### Community 156 - "._on_bone_toggled"
Cohesion: 0.29
Nodes (4): QListWidgetItem, Catch the selection a click on a checkbox is about to collapse. Qt selects a…, Which bones of the armature the picked-out rows stand for., Take lengths of wire out of the clay, or put them back. A tick on a row that…

### Community 158 - "shaders.py"
Cohesion: 0.25
Nodes (6): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section(), Skin BRDF and bounded-depth light transport, shared by preview and refinement.…

### Community 159 - ".paintGL"
Cohesion: 0.29
Nodes (3): Use the same cached visibility test for bones and all point markers., Which part wears the line this frame, and how solid it is, or ``None``. Also…, Hand the renderer the depth grid, or take it away, before a frame.

### Community 160 - ".read"
Cohesion: 0.20
Nodes (5): Any, Which command has these keys, if any., Put ``keys`` on a command, taking them off whatever had them. Returns the id of…, Back to the shipped keys, for one command or for all of them. For one command…, Take the choices out of a settings file, keeping what makes sense. Forgiving,…

### Community 161 - "test_contour_shading.py"
Cohesion: 0.29
Nodes (5): parametrize, The contour shading mode: slices across the form, read off it like a map., test_a_custom_direction_is_normalised_and_an_empty_one_falls_back(), test_the_density_floor_keeps_the_spacing_finite(), test_the_slices_face_the_way_that_was_asked()

### Community 162 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 163 - "FormRun"
Cohesion: 0.40
Nodes (3): FormRun, Begin a run against a form already in the store., A guided form part-way through.

### Community 164 - "Human Skin renderer"
Cohesion: 0.33
Nodes (5): Human Skin renderer, Material and transport, Scheduling, precision and compatibility, Surface, Where to change it

### Community 165 - "test_spatial.py"
Cohesion: 0.26
Nodes (11): _grid(), The picking accelerator: it must be fast without changing any answer., A bumpy height field, so rays hit different triangles at different depths., The pruned candidate set must never miss the true intersection., Every parent must enclose its children, or a ray could slip past a leaf., test_a_batch_of_rays_gets_the_same_candidates_as_one_at_a_time(), test_a_ray_that_misses_the_model_is_pruned_away(), test_every_triangle_lands_in_exactly_one_leaf() (+3 more)

### Community 166 - "_wire_frame"
Cohesion: 0.50
Nodes (4): _perpendicular(), Two unit directions across ``along``, neither of them near it., Which three ways a lump laid along a wire runs. Columns, thinnest first. The…, _wire_frame()

### Community 167 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 168 - "app"
Cohesion: 0.33
Nodes (6): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., store(), test_the_store_writes_only_the_choices_and_reads_them_back(), window()

### Community 169 - "sample_count"
Cohesion: 0.50
Nodes (3): How many samples the framebuffer bound right now is drawing with. One where…, sample_count(), How many samples this view is really drawing with, or ``None``. Asked of GL…

### Community 170 - "_height_of"
Cohesion: 0.40
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 171 - "_file_drag"
Cohesion: 0.40
Nodes (5): _file_drag(), A file being dragged over the middle of the view, as ``kind`` of event., Entering, moving and dropping: a drop lands only where the move before it was…, test_a_file_the_window_cannot_open_is_refused_on_the_way_past(), test_a_model_file_is_welcome_at_every_step_of_its_drag()

### Community 173 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 175 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 176 - "raycast_mesh"
Cohesion: 0.18
Nodes (17): _cross(), intersects_bounds(), ndarray, Row-wise cross product, without :func:`numpy.cross`'s axis shuffling., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``., The closest hit along each of a batch of rays, ``None`` where one misses. One…, raycast_many() (+9 more)

### Community 177 - "test_the_switch_on_a_dock_bar_is_the_panels_own_visibility"
Cohesion: 0.67
Nodes (3): parametrize, test_a_panel_that_draws_nothing_has_no_switch(), test_the_switch_on_a_dock_bar_is_the_panels_own_visibility()

### Community 178 - "quad"
Cohesion: 0.67
Nodes (3): fixture, quad(), Two triangles covering the unit square on the z = 0 plane.

### Community 179 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 182 - "skin_detail.py"
Cohesion: 0.17
Nodes (20): burley_marginal(), burley_profile(), cellular(), diffusion_lut(), _fade(), fbm(), ndarray, Procedural skin micro-relief and the pre-integrated diffusion table. Reference… (+12 more)

### Community 186 - "ModelPanel"
Cohesion: 0.07
Nodes (11): ModelPanel, QTreeWidgetItem, Bind the panel to the viewport's transform tool., Reflect the tool state without re-emitting the toggle., Choose the gesture, from the menu or a key., Rebuild the tree from the store, with the active object current., Offer every object the active one could hang from., The objects whose rows are selected, in list order. (+3 more)

### Community 187 - "ui/preferences.py"
Cohesion: 0.06
Nodes (31): css(), A colour as a style sheet function, for the parts Qt draws., QObject, Making the whole of a switch the part you can press. The theme turns every…, Turns a press anywhere on a switch into a click on it., WholeFaceToggles, current(), forget() (+23 more)

### Community 188 - "._commit_node_drag"
Cohesion: 0.33
Nodes (3): Record the finished gesture: a move, a resize, or a plain click. A press that…, Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…

## Knowledge Gaps
- **5 isolated node(s):** `refview`, `Surface`, `Material and transport`, `Scheduling, precision and compatibility`, `Where to change it`
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `state.py`, `settings.py`, `ExportLook`, `SceneRenderer`, `stone_field`, `MeshBuffers`, `ViewerState`, `Skeleton`, `mesh_renderer.py`, `carve`, `SectionSettings`, `ndarray`, `TriangleIndex`, `PlaneSettings`, `test_plane_clusters.py`, `test_spatial.py`, `Camera`, `Wires`, `gltf_loader.py`, `ExportVideoDialog`, `raycast_mesh`, `plane_axes`, `quad`, `FilmExport`, `test_skeleton.py`, `test_forms.py`, `PrimaryForm`, `pose_panel.py`, `test_objects.py`, `test_plane_solids.py`, `PoseTool`, `Bounds`, `picking.py`, `viewport.py`, `section.py`, `OrientationSettings`, `test_skin.py`, `.source_mesh`, `plane_volume.py`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `._sync_scene`, `main_window.py`, `AnnotateTool`, `ExportLook`, `.stage_images`, `MainWindow`, `test_preferences.py`, `Armature`, `ViewerState`, `._picker`, `.paintGL`, `film_export.py`, `test_viewport_markers.py`, `sample_count`, `Wires`, `ExportVideoDialog`, `._active_changed`, `FilmExport`, `._commit_node_drag`, `application.py`, `MeasureTool`, `PrimaryForm`, `test_objects.py`, `ObjectTool`, `PoseTool`, `NavigationController`, `picking.py`, `SectionGizmo`, `viewport.py`, `_Encoder`, `.mousePressEvent`, `Measurement`, `.mouseReleaseEvent`, `._place_armature_node`, `ViewportOverlay`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `test_preferences.py`, `main_window.py`, `Viewport`, `state.py`, `MainWindow`, `OverlayParts`, `widgets.py`, `Panel`, `Armature`, `README.md`, `test_tab_switches.py`, `._draw_annotation`, `MeasurePanel`, `test_viewport_markers.py`, `panel`, `test_matcap_preview.py`, `application.py`, `MeasureTool`, `PrimaryForm`, `test_objects.py`, `PoseTool`, `test_custom_panels.py`, `ObjectsEdit`, `._draw_hud`, `test_forms_panel.py`, `viewport.py`, `MatcapPanel`, `test_elements.py`, `Measurement`, `OrientationSettings`, `test_skin.py`, `.source_mesh`, `ViewportOverlay`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 44 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 44 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `OverlayParts`) actually correct?**
  _`ViewerState` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._