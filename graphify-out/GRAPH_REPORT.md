# Graph Report - reference-viewer  (2026-09-15)

## Corpus Check
- 138 files · ~455,099 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4592 nodes · 10273 edges · 188 communities (176 shown, 12 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 481 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `20ea8927`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- form_group
- test_preferences.py
- update_check.py
- Viewport
- plane_axes
- Panel
- MainWindow
- Stroke
- GifWriter
- mesh_renderer.py
- ._draw_scene
- viewport.py
- main_window.py
- test_armature.py
- Armature
- README.md
- ViewerState
- test_session.py
- framebuffer.py
- CameraPanel
- UpdateChecker
- ShaderProgram
- test_viewport_markers.py
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- VideoError
- SectionSettings
- plane_volume.py
- ControlsWindow
- TriangleIndex
- ._apply
- PlaneSettings
- test_camera.py
- test_plane_clusters.py
- WakeLock
- MatcapPreview
- ._turn
- CustomPanel
- VideoFormat
- SurfacePicker
- Camera
- armature_tool.py
- ValueSlider
- gltf_loader.py
- ExportVideoDialog
- film_export.py
- landmarks.py
- Agent Graph-First Instructions
- VideoSettings
- plane_clusters.py
- test_matcap_preview.py
- build_humanoid
- ArmaturePanel
- OrientationSettings
- HotkeyMap
- FilmExport
- FormsPanel
- PlanesPanel
- Landmark
- ArmatureTool
- Workspace
- ui/hotkeys.py
- test_forms.py
- application.py
- MeasureTool
- Link
- PrimaryForm
- History
- PointEdit
- AnnotatePanel
- test_plane_solids.py
- ._selected
- session.py
- KeyBox
- default_matcap_pixels
- load_matcap_pixels
- test_custom_panels.py
- test_hotkeys.py
- core/preferences.py
- test_contour_shading.py
- NavigationController
- Bounds
- planes_panel.py
- test_forms_panel.py
- Mesh
- HotkeyBinder
- forms.py
- MatcapPanel
- ColorButton
- Frame
- _Encoder
- ._picker
- test_elements.py
- state.py
- FormRun
- ReflowLayout
- Measurement
- ._selected_landmark
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
- ndarray
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
- CHANGELOG.md
- PreferenceStore
- symbol_button
- ._buried_nodes
- overlay.py
- ExportLook
- ._place_form_landmark
- preview
- armature.py
- ui/preferences.py
- stone_field
- watch_keys
- SectionGizmo
- _drag_over
- .mouseMoveEvent
- paths.py
- ShadingPanel
- _shifts
- parametrize
- union_field
- carve
- test_a_session_saved_without_panels_leaves_the_ones_open_alone
- .install
- coarse_lattice
- test_resetting_the_layout_puts_the_docks_back_at_once
- ._built
- ask_for
- restored
- test_resetting_keeps_the_panels_built_by_hand
- test_a_panel_does_not_cover_its_own_title
- test_the_switch_is_not_squeezed_to_nothing
- test_a_panel_can_be_taken_away_and_another_built_after_a_restore
- test_loading_a_session_over_a_restored_layout_survives
- test_the_dock_of_a_panel_taken_away_is_used_again
- test_a_reused_dock_does_not_bring_the_old_panels_contents_with_it
- .column_of
- .update_enabled
- sample_count
- test_spatial.py
- .refresh_list
- coarse_lattice
- environment.yml
- .new_custom_panel
- _height_of
- _file_drag
- make_switch
- .reset
- kept_off
- generate_matcaps.py
- .new_armature
- PanelDock
- .dress_tabs
- app
- ndarray
- orientation.py
- shaders.py
- test_the_disc_samples_where_the_shader_would
- _create_splash
- HotkeyDialog
- section
- no_ffmpeg

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
- `Camera motion is deliberately not undoable` --rationale_for--> `Command`  [EXTRACTED]
  README.md → src/refview/core/history.py
- `Pedestal (1.1.0)` --rationale_for--> `PedestalSettings`  [EXTRACTED]
  CHANGELOG.md → src/refview/core/pedestal.py
- `REFVIEW_RESOURCES resource override` --rationale_for--> `available_matcaps()`  [EXTRACTED]
  README.md → src/refview/paths.py
- `Terracotta clay matcap` --shares_data_with--> `available_matcaps()`  [INFERRED]
  resources/matcaps/clay_terracotta.png → src/refview/paths.py

## Import Cycles
- 3-file cycle: `src/refview/ui/elements/__init__.py -> src/refview/ui/elements/clone.py -> src/refview/ui/elements/slider.py -> src/refview/ui/elements/__init__.py`
- 4-file cycle: `src/refview/ui/elements/__init__.py -> src/refview/ui/elements/custom.py -> src/refview/ui/elements/clone.py -> src/refview/ui/elements/slider.py -> src/refview/ui/elements/__init__.py`

## Hyperedges (group relationships)
- **The bundled matcap set** — resources_matcaps_clay_terracotta_matcap, resources_matcaps_charcoal_matcap, resources_matcaps_jade_matcap, resources_matcaps_steel_matcap, resources_matcaps_studio_white_matcap, resources_matcaps_wax_skin_matcap, tools_generate_matcaps_matcappreset, tools_generate_matcaps_render [INFERRED 0.85]
- **The four generic undo commands** — src_refview_core_commands_setattributes, src_refview_core_commands_additem, src_refview_core_commands_removeitem, src_refview_core_commands_replaceitems, src_refview_core_history_command, readme_every_edit_is_a_command [EXTRACTED 1.00]
- **Windows binary-compatibility decisions** — readme_pyside6_pinned_below_68, environment_pip_installed_binaries, environment_python_311, github_workflows_release_pyinstaller_build [INFERRED 0.75]

## Communities (188 total, 12 thin omitted)

### Community 0 - "form_group"
Cohesion: 0.13
Nodes (15): The preferences as they stand. Treat as read-only; use :meth:`set`., QWidget, Fill in the groups. A switch with nothing to put in the caption column is given…, Every command with its keys, each key a box that takes one keystroke. The list…, The one button that is not a preference, and what the window is for., Say what the view is really drawing with, beside what was asked for. A sample…, Put one field back into the store, which applies and saves it., Pull every control back into line with the store. Run when the window is built,… (+7 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.09
Nodes (24): app(), model(), fixture, What the artist prefers: kept apart from the document, and acted upon. Two…, An external drive that is not plugged in is not an empty gallery., Restore Defaults, or a copy of one of these controls in another panel., One triangle, which is a mesh as far as any of this is concerned., Windows that clean up after themselves, and a settings file that does. (+16 more)

### Community 2 - "update_check.py"
Cohesion: 0.10
Nodes (31): check_for_update(), fetch_latest_release(), is_newer(), _macos_root_certificates(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and… (+23 more)

### Community 3 - "Viewport"
Cohesion: 0.08
Nodes (12): QOpenGLWidget, Slide the view so a point sits at the centre, keeping the angle., A form changed: work its clay out again and redraw., Slide the view so a measurement sits at the centre, keeping the angle., End any film being recorded, and wait for its thread to really stop. For…, Whether frames are being rendered out of a film right now., Free every GL object while the owning context is still current., Arm one tool, disarming the rest. Only one gesture can own the left button, so… (+4 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - "Panel"
Cohesion: 0.09
Nodes (14): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only., Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Whether what this panel draws is on screen, or ``None`` if it draws nothing.… (+6 more)

### Community 6 - "MainWindow"
Cohesion: 0.06
Nodes (17): MainWindow, QMainWindow, Open an empty panel of the artist's own and bring it to the front., Put the docks and the hand-built panels back where they were. Unless the artist…, Put the panels back where they started, now., Follow the machine's sleep to whether this window is in front., Wires the viewport, the panels and the document together., Give each panel a dock of its own, tabbed together on the right. Each panel can… (+9 more)

### Community 7 - "Stroke"
Cohesion: 0.05
Nodes (39): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+31 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "mesh_renderer.py"
Cohesion: 0.09
Nodes (32): Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., look_at(), normalize(), orthographic() (+24 more)

### Community 10 - "._draw_scene"
Cohesion: 0.12
Nodes (17): normal_matrix(), ndarray, Replace the section contour, prepared by the caller as stroke vertices., Everything in the frame, into whichever framebuffer is bound., How see-through the model is this frame, or ``None`` if it is solid. Asked in…, The model, the pedestal under it and the flat cap over the cut., Point the shading pass at the shadow map and the occlusion buffer., Flood the exposed interior with a flat colour so the cut reads solid. The… (+9 more)

### Community 11 - "viewport.py"
Cohesion: 0.04
Nodes (66): _empty(), PlaneSet, ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, One level of a fit: the planes the shader is to quantise against. A plane is a…, A level with no place in it: nearest direction wins, as before., The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to. (+58 more)

### Community 12 - "main_window.py"
Cohesion: 0.07
Nodes (43): QScrollArea, _asked(), forget(), _free(), _from_id(), name_tree(), _named_after(), QWidget (+35 more)

### Community 13 - "test_armature.py"
Cohesion: 0.07
Nodes (50): ArmatureNode, One joint of the wire: where it is, and how thick the form is there., The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _chain(), _derived(), The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other. (+42 more)

### Community 14 - "Armature"
Cohesion: 0.04
Nodes (38): Armature, ArmatureStore, Bone, Point3, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves. (+30 more)

### Community 15 - "README.md"
Cohesion: 0.25
Nodes (10): Annotations drawn as widened geometry, Camera motion is deliberately not undoable, core never imports Qt, The cut interior is flooded flat, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets (+2 more)

### Community 16 - "ViewerState"
Cohesion: 0.09
Nodes (16): Command, Path, QObject, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements, annotations,… (+8 more)

### Community 17 - "test_session.py"
Cohesion: 0.11
Nodes (17): Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., A step of the slider is worth a fixed share more planes, not a fixed number of…, The ceiling went from 64 planes to 256 without moving the slider under anyone:…, The panel edits the settings; the fit has to be told what they are., Both modes answer in degrees of turn, so the panel can just ask., Version 6 files predate panels being something a session could carry., Deletion goes through the undo stack, so the store only tracks position. (+9 more)

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
Cohesion: 0.13
Nodes (8): ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "test_viewport_markers.py"
Cohesion: 0.11
Nodes (21): Any, Take the choices out of a settings file, keeping what makes sense. Forgiving,…, parametrize, test_a_panel_that_draws_nothing_has_no_switch(), test_the_switch_is_the_panels_own_visibility_setting(), app(), event(), fixture (+13 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.07
Nodes (25): app(), _names(), panel(), fixture, The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as… (+17 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.12
Nodes (9): MeasurePanel, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn. (+1 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.11
Nodes (9): BookmarkStore, CameraBookmark, Named camera positions the artist can jump between while sculpting., A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one. (+1 more)

### Community 26 - "VideoError"
Cohesion: 0.16
Nodes (10): _FFmpegWriter, ndarray, RuntimeError, An export that could not be written, said in words for the artist., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Raw frames down a pipe, a finished file out the other end. The frames go in as…, Nothing to do: ffmpeg reads the whole stream before it decides. (+2 more)

### Community 27 - "SectionSettings"
Cohesion: 0.06
Nodes (38): Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, The direction the section plane faces. (+30 more)

### Community 28 - "plane_volume.py"
Cohesion: 0.13
Nodes (21): _back_inside(), dual_contour(), _flat_mesh(), _passes(), Blocking a form in out of its own planes, from the outside or from a core. A…, The surface where ``value`` changes sign, one vertex per lattice cell. Each…, The gradient of a lattice field, by central differences. Which is the direction…, Drop the loose pieces, keeping the form and anything of its size. A block is a… (+13 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "TriangleIndex"
Cohesion: 0.13
Nodes (17): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Box the leaves up, coarsest level first and the leaves themselves last., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the… (+9 more)

### Community 31 - "._apply"
Cohesion: 0.20
Nodes (5): Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Slot that writes one field of the contour shading settings.

### Community 32 - "PlaneSettings"
Cohesion: 0.03
Nodes (73): QThread, film_key(), What a film depends on. Everything that changes the shape of any stage, and…, Holds the working state between one turn of the sliders and the next.…, The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache, An armature, as the clay reads it: where each length of wire runs. The order… (+65 more)

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
Nodes (14): QMenu, MatcapPreview, _push_preview(), Path, QSize, QWidget, A matcap on a sphere, which is also how the matcap is graded., Offer the picture back as a file: as graded here, or as it came. A grading… (+6 more)

### Community 37 - "._turn"
Cohesion: 0.13
Nodes (9): _angle(), Redraw from the settings, which something else has changed., Put the grading back, which is the one thing a disc cannot show., Turn the matcap by the angle the cursor swept about the centre. By angle and…, Two grades on one drag: one along each axis of the movement. Both move together…, Keep the angle in -180 to 180, the range the setting is stored in., The angle of ``point`` about ``centre``, anticlockwise with y upwards., An angle difference brought back into -pi to pi. (+1 more)

### Community 38 - "CustomPanel"
Cohesion: 0.09
Nodes (19): carried(), Read a drag's payload back, or ``None`` if it is not one of ours., CustomPanel, _detach(), QFormLayout, QWidget, Take a copy out of this panel and destroy it., Move a copy already in a panel to a new place in this one. ``frame`` and… (+11 more)

### Community 39 - "VideoFormat"
Cohesion: 0.13
Nodes (7): str, What an artist should know before picking this one., A container, and with it a codec and a set of trade-offs., The file dialog's filter line for this format., Whether this format can only be written by ffmpeg. GIF is the one that cannot:…, VideoFormat, TestFormats

### Community 40 - "SurfacePicker"
Cohesion: 0.06
Nodes (28): AnnotateMode, AnnotationSettings, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a… (+20 more)

### Community 41 - "Camera"
Cohesion: 0.07
Nodes (29): Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Rays through a batch of pixels, as ``(origins, unit directions)``, ``(N, 3)``…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Project ``(N, 3)`` world points to ``(xs, ys, ndc_depths)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Screen-to-world scale at the focal plane; identical in both modes. (+21 more)

### Community 42 - "armature_tool.py"
Cohesion: 0.08
Nodes (22): BoneRef, mirror_landmarks(), Preset, An ordered set of landmarks and the armature they build., The landmarks worth asking for under these choices. With mirroring on the…, The midline landmarks, which are what the median plane is fitted to., The landmark list with every paired landmark reflected into place. A point the…, GuideRun (+14 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (11): _pull_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end., Set the value the way a hand on the control would., The value the track stands at ``x`` pixels across. (+3 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.12
Nodes (28): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry() (+20 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.10
Nodes (13): QProgressDialog, even(), ExportVideoDialog, Path, QDialog, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the…, What the frames are to look like, as the controls have it. (+5 more)

### Community 46 - "film_export.py"
Cohesion: 0.07
Nodes (32): _encode_arguments(), _encoders(), ffmpeg_path(), _no_window(), open_writer(), Enum, Path, Quality (+24 more)

### Community 47 - "landmarks.py"
Cohesion: 0.11
Nodes (24): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _humanoid_landmarks(), _mid(), mirror_point() (+16 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "VideoSettings"
Cohesion: 0.18
Nodes (7): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, TestTiming

### Community 50 - "plane_clusters.py"
Cohesion: 0.05
Nodes (53): Coefficients, PlaneAxes, The planes a model falls into, at every count. Built once per mesh and per…, The best ``count`` planes, or as many as the model supports. A model whose…, How much surface each vertex stands for: a third of each triangle on it.…, What each block of the design matrix counts for, against the normals. A fit…, Whether anything but the normals is being read at all., vertex_weights() (+45 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.14
Nodes (24): QPoint, _drag(), The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc., Dragging further than the range goes is not a negative gamma., Alt and a drag copies a control; the disc must not swallow that., Tint and flip are not dragged on the disc, so they are not reset by it. (+16 more)

### Community 52 - "build_humanoid"
Cohesion: 0.12
Nodes (32): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _figure(), ndarray, The femoral head is in from the ASIS, below it and behind it, by shares of the…, A wire in two halves is not an armature anybody could bend., Place every landmark the run asks for; returns how many were asked., Every required humanoid landmark, both sides, scaled about the origin. (+24 more)

### Community 53 - "ArmaturePanel"
Cohesion: 0.14
Nodes (5): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Take back the landmark before this one and ask for it again., Record an edit the viewport's tool worked out., The multiplier the position boxes are read and written through.

### Community 54 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 55 - "HotkeyMap"
Cohesion: 0.08
Nodes (17): Command, HotkeyMap, Which keys do what, as the artist has decided rather than as it ships. A hotkey…, Whether the artist has moved this command off what it ships with., Which command has these keys, if any., Every command with keys on it, declared or not, as id -> keys., Put ``keys`` on a command, taking them off whatever had them. Returns the id of…, Back to the shipped keys, for one command or for all of them. For one command… (+9 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (11): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+3 more)

### Community 57 - "FormsPanel"
Cohesion: 0.04
Nodes (35): FormsPanel, QPushButton, QTreeWidgetItem, QWidget, A strip of buttons that one form row can show or hide as a unit., Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle. (+27 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.09
Nodes (18): PlanesPanel, QListWidgetItem, Lay one length of wire earlier or later, as one undoable step., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Show what this way of working needs, and put the rest away. A setting that does… (+10 more)

### Community 59 - "Landmark"
Cohesion: 0.07
Nodes (31): _centre(), FormPreset, FormStage, freeform_landmark(), freeform_preset(), landmark_key(), _pair(), paired_landmarks() (+23 more)

### Community 60 - "ArmatureTool"
Cohesion: 0.06
Nodes (39): LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, Handle, ndarray, The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now. (+31 more)

### Community 61 - "Workspace"
Cohesion: 0.12
Nodes (9): QMainWindow, QObject, QWidget, Keep every switch agreeing with the panel it speaks for., Dress the tabs once Qt has finished rearranging them., Take a parked dock back out under ``key``, emptied and renamed., Open the dock a hand-built panel lives in and bring it to the front., The docks of one window: the fixed panels and the ones built by hand. (+1 more)

### Community 62 - "ui/hotkeys.py"
Cohesion: 0.11
Nodes (21): assign(), control_of(), describe(), forget(), group_of(), HotkeyStore, listed(), normalize() (+13 more)

### Community 63 - "test_forms.py"
Cohesion: 0.06
Nodes (62): _across(), blend_rings(), build_head(), build_pelvis(), build_ribcage(), fit_plane(), _head_frame(), _lagrange() (+54 more)

### Community 64 - "application.py"
Cohesion: 0.12
Nodes (17): ArgumentParser, Namespace, _apply_startup_arguments(), build_parser(), main(), Command-line entry point and application bootstrap., Open whatever the command line asked for, falling back to sane defaults., Start the viewer and block until the window closes. (+9 more)

### Community 65 - "MeasureTool"
Cohesion: 0.12
Nodes (10): MeasureTool, Handle, ndarray, The nearest grabbable endpoint under the cursor, if any. Only unlocked, visible…, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview. (+2 more)

### Community 66 - "Link"
Cohesion: 0.12
Nodes (9): CloneGesture, Link, _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original., Whether the copy is being used right now and must not be written. (+1 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.04
Nodes (78): FormLandmarkRef, PlacedLandmark, One anatomical point the artist put on the model during a guided run., build_form(), built_count(), form_landmark_title(), form_mesh(), form_spec() (+70 more)

### Community 68 - "History"
Cohesion: 0.13
Nodes (15): History, A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive…, measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch() (+7 more)

### Community 69 - "PointEdit"
Cohesion: 0.09
Nodes (19): _clone_point(), Cloner, _pull_point(), _push_point(), _push_slider(), How to make, drive and refresh a copy of one kind of control., Teach the copier about a kind of control., register_cloner() (+11 more)

### Community 70 - "AnnotatePanel"
Cohesion: 0.19
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 71 - "test_plane_solids.py"
Cohesion: 0.03
Nodes (150): auto_smooth(), A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), film_of(), parametrize (+142 more)

### Community 72 - "._selected"
Cohesion: 0.14
Nodes (7): Run a row's edit once Qt has finished delivering the current signal. Committing…, Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., Run a bone between the row selected now and the node held before it., Join two nodes of one armature, if they are two and they are one armature., The node the selected row stands for, if the row is a node at all., The armature the selected row stands for, when the row is not a node.

### Community 73 - "session.py"
Cohesion: 0.10
Nodes (24): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Path (+16 more)

### Community 74 - "KeyBox"
Cohesion: 0.18
Nodes (7): QKeySequence, QKeySequenceEdit, KeyBox, A box that takes one keystroke and says when it has one, or has none. Qt's box…, Show ``keys`` without that counting as the artist entering them., test_rekeying_a_command_moves_the_menu_and_the_shortcut(), test_the_window_declares_its_menus_and_letters_and_keys_them()

### Community 75 - "default_matcap_pixels"
Cohesion: 0.11
Nodes (13): OpenGL rendering layer: shader programs, textures and the scene renderer., DataTexture, default_matcap_pixels(), MatcapLoadError, ndarray, RuntimeError, Matcap texture loading and upload, and the small data table beside it., An RGBA16F 2D texture with clamped edges and mipmapped minification. (+5 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.27
Nodes (14): Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels(), Path (+6 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.05
Nodes (29): QMimeData, Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel, app() (+21 more)

### Community 78 - "test_hotkeys.py"
Cohesion: 0.10
Nodes (25): lookup(), The control an id names, if the window still has it., app(), _click(), _map(), fixture, Hotkeys: the map, the store, the binder, and the gesture that assigns one., One offscreen Qt application for the run; see test_film_recorder. (+17 more)

### Community 79 - "core/preferences.py"
Cohesion: 0.11
Nodes (20): _as_kind_of(), _clamp(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any (+12 more)

### Community 80 - "test_contour_shading.py"
Cohesion: 0.33
Nodes (4): parametrize, The contour shading mode: slices across the form, read off it like a map., test_the_density_floor_keeps_the_spacing_finite(), test_the_slices_face_the_way_that_was_asked()

### Community 81 - "NavigationController"
Cohesion: 0.08
Nodes (17): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Degrees of yaw per pixel, signed by whether the drag is inverted. (+9 more)

### Community 82 - "Bounds"
Cohesion: 0.06
Nodes (30): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, Bounds, _gathered(), ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations… (+22 more)

### Community 83 - "planes_panel.py"
Cohesion: 0.13
Nodes (11): plane_count(), How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., How many planes a mode fitted to the model keeps. The climb from two planes to…, How many planes the form itself is rebuilt out of., Dockable control panels., Everything that acts on the shading normals rather than on the shading. Faceted…, The line under the normals slider: what the setting has asked for., _summary() (+3 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.11
Nodes (30): app(), _click(), panel(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The… (+22 more)

### Community 85 - "Mesh"
Cohesion: 0.04
Nodes (80): Qt-free geometry, camera and document model for the reference viewer., compute_vertex_normals(), One entry point for every mesh format the viewer reads. Callers ask for a path…, Mesh, MeshLoadError, RuntimeError, Triangle-mesh containers shared by the loader, the renderer and picking., Raised when a file cannot be interpreted as a triangle mesh. (+72 more)

### Community 86 - "HotkeyBinder"
Cohesion: 0.12
Nodes (18): QShortcut, command_for(), decorate(), HotkeyBinder, press(), QObject, QWidget, The command a control stands for, or ``None`` if it has no name to go by. A… (+10 more)

### Community 87 - "forms.py"
Cohesion: 0.06
Nodes (50): convex_hull(), DegenerateHullError, flat_mesh(), merged(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary… (+42 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.17
Nodes (8): MatcapPanel, Rebuild the thumbnail list from the resources folder., The disc was dragged: show the renderer and the numbers what it did., A different matcap: the disc draws whichever one is on the model., Put the numbers back in line with the settings, and redraw the disc. Separate…, Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, test_the_disc_draws_the_matcap_that_is_on_the_model()

### Community 89 - "ColorButton"
Cohesion: 0.10
Nodes (13): _clone_swatch(), _pull_swatch(), _push_swatch(), _AxisBox, ColorButton, QColor, QDoubleSpinBox, QSize (+5 more)

### Community 90 - "Frame"
Cohesion: 0.07
Nodes (18): _pull_frame(), _push_frame(), Nothing: each row inside the copy is linked on its own., Frame, FrameBar, framed(), QFormLayout, QPainter (+10 more)

### Community 91 - "_Encoder"
Cohesion: 0.22
Nodes (6): Queue, _Encoder, QObject, QWidget, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 92 - "._picker"
Cohesion: 0.14
Nodes (7): ndarray, Rub out the stroke points under the eraser, live., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on., Take hold of a form's landmark, to move it or just to say which one it is.

### Community 93 - "test_elements.py"
Cohesion: 0.11
Nodes (13): Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., Run the refresh the shared timer would have run., test_a_copy_follows_the_original_on_the_tick(), test_a_copy_goes_dead_when_its_original_does() (+5 more)

### Community 94 - "state.py"
Cohesion: 0.15
Nodes (11): Shift-snapped orbiting (1.1.0), MeasurementSettings, Named point-to-point measurements and their presentation options., How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., NavigationSettings, How mouse gestures drive the camera., Two-click measuring, plus dragging the endpoints of an unlocked measurement. (+3 more)

### Community 95 - "FormRun"
Cohesion: 0.40
Nodes (3): FormRun, Begin a run against a form already in the store., A guided form part-way through.

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - "Measurement"
Cohesion: 0.12
Nodes (11): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+3 more)

### Community 98 - "._selected_landmark"
Cohesion: 0.12
Nodes (7): Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors., Show the landmark group only once there are landmarks to show., The landmark the highlighted row stands for, if the row is one., Which armature the landmark list is pointing into, row or heading., Follow the highlighted landmark, and say which one it is in the view.

### Community 99 - "SceneRenderer"
Cohesion: 0.06
Nodes (22): bind_default(), current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., Restore a framebuffer captured with :func:`current_framebuffer`., _ghost_depth_range(), MeshBuffers, Forget the contents without releasing the buffer objects., Owns every GL resource the viewport needs. The widget calls :meth:`initialize`… (+14 more)

### Community 100 - "clone.py"
Cohesion: 0.05
Nodes (70): QAbstractButton, QComboBox, QLineEdit, QSlider, QSpinBox, _begin(), can_clone(), clone() (+62 more)

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
Cohesion: 0.15
Nodes (7): QToolButton, DockTitle, QSize, QWidget, The bar across the top of a dock: a switch, a name and two buttons., As tall as the bar really is. A dock puts the panel directly below its title…, StandardPixmap

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - "MatcapSettings"
Cohesion: 0.15
Nodes (16): MatcapSettings, Post-processing applied to the sampled matcap texel., _clone_preview(), grade(), _pull_preview(), ndarray, Draw the matcap onto a sphere of ``size`` pixels, graded. Returns ``(size,…, Point the preview at the settings it edits. The object itself, not a copy: this… (+8 more)

### Community 113 - "ndarray"
Cohesion: 0.15
Nodes (18): _axes(), encloses(), lattice(), lay_bed(), nearest_surface(), _perpendicular(), ndarray, Which lengths of wire take a lump, in the order they take one. (+10 more)

### Community 114 - "Preferences"
Cohesion: 0.16
Nodes (17): Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, The font size is a string; everything beside it still arrives., test_a_field_from_a_later_version_is_ignored(), test_a_setting_out_of_range_is_brought_back_into_it(), test_a_settings_file_that_is_not_settings_at_all_still_starts(), test_every_anti_aliasing_mode_is_reachable_and_nonsense_falls_back() (+9 more)

### Community 115 - "._build"
Cohesion: 0.27
Nodes (6): QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 116 - "test_open_files.py"
Cohesion: 0.12
Nodes (14): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version(), app(), opened(), fixture, parametrize, Files arriving from outside: the command line, a drop, or the desktop's "Open… (+6 more)

### Community 117 - "OpenRequests"
Cohesion: 0.15
Nodes (8): Application, OpenRequests, Path, QApplication, The Qt application, listening for the desktop's way of handing over a file., Files the desktop asked the viewer to open, kept until there is a window. On…, Open ``path`` in the window, or hold it until there is one., Name the window files go to, and hand over any that came early.

### Community 118 - "FormStore"
Cohesion: 0.18
Nodes (4): FormStore, An ordered, named collection of forms, like the other stores., A name for a new form of this recipe, numbered past any it already has. A form…, test_a_form_store_names_forms_past_the_ones_it_has()

### Community 119 - "SetAttributes"
Cohesion: 0.08
Nodes (24): Every document edit is a command, AddItem, Any, Command, The handful of undoable edits the whole application is built from.…, Assign one or more attributes on an object, remembering the old values.…, Append an item to a document list., Delete the item at ``index``, putting it back in place on undo. (+16 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.12
Nodes (23): QPointF, QRectF, project_visible(), Handle, QColor, QFont, QPainter, Draws measurements, tool previews, the orientation gizmo and the readout. (+15 more)

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

### Community 127 - "CHANGELOG.md"
Cohesion: 0.16
Nodes (9): Cross-section tool (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, ModelPanel (+1 more)

### Community 128 - "PreferenceStore"
Cohesion: 0.20
Nodes (7): PreferenceStore, QObject, QSettings, The preferences, and one signal saying they have changed. A single instance,…, Adopt ``value``, push what has to be pushed, and say so. Always announces, even…, Back to how the application ships., Read the preferences off the machine. Never raises.

### Community 129 - "symbol_button"
Cohesion: 0.18
Nodes (13): QIcon, _draw_glyph(), glyph(), lock_icon(), QColor, QPixmap, Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if… (+5 more)

### Community 131 - "overlay.py"
Cohesion: 0.09
Nodes (15): draw_rail(), draw_text(), MarkerVisibility, One marker object for endpoints, nodes, landmarks and tool previews., Cache surface occlusion by view and position for every kind of marker., Answer for a batch of points at once, ahead of being asked one by one. Every…, Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, The screen-space cue for one degree of freedom. A vertical rail that fades out… (+7 more)

### Community 132 - "ExportLook"
Cohesion: 0.10
Nodes (13): ExportLook, What the frames are to look like, as against what they are of. Laid over the…, Which of the things drawn over the model belong in the frames., ``base`` with this export's choices laid over it., The line burned into the corner of the frame for ``stage``. Counted off the…, FakeViewport, QImage, Pump the event loop until ``done()`` or the clock runs out. (+5 more)

### Community 134 - "preview"
Cohesion: 0.40
Nodes (5): app(), preview(), fixture, One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "armature.py"
Cohesion: 0.27
Nodes (7): BoneLabels, Buried, Enum, str, A graph of named points under the form, and the wire it stands for. An armature…, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…

### Community 136 - "ui/preferences.py"
Cohesion: 0.07
Nodes (28): One dock per panel, with a bar of its own across the top. Every panel is its…, css(), outline(), QColor, The colours the hand-drawn elements paint with. Kept apart from…, Draw the hairline that separates a control from the panel. One line, the same…, A colour as a style sheet function, for the parts Qt draws., Change the one colour that is not grey, everywhere at once. The hand-painted… (+20 more)

### Community 137 - "stone_field"
Cohesion: 0.17
Nodes (11): Bed, block_bounds(), coarse_bounds(), point_support(), The lattice a form is worked on, and the model read onto it. Everything here…, Which way the model's own surface faces, at every corner., The union of the blocks a labelling cuts the model into, and its facings. Stone…, The index range each block covers. ``(count, 3)`` lows and highs, inclusive. A… (+3 more)

### Community 138 - "watch_keys"
Cohesion: 0.19
Nodes (11): can_take_key(), is_hotkey_click(), KeyGesture, QObject, QWidget, The gesture that puts a key on a control: Ctrl/Cmd, Alt and a click. It sits…, Whether a mouse press is the assignment gesture rather than a click., Whether a widget is the kind a key can sensibly be put on. A button or a switch… (+3 more)

### Community 139 - "SectionGizmo"
Cohesion: 0.18
Nodes (8): Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo, ndarray, Rotate the measurements, annotations, armature and forms onto the turned model.…, The rail stands still while the camera moves, and never leaves the frame., test_section_rail_is_a_screen_space_cue_at_the_right_edge()

### Community 140 - "_drag_over"
Cohesion: 0.22
Nodes (10): _drag_over(), _middle_of_the_view(), A drag of ``holder`` arriving at ``point`` in the window's coordinates. A real…, The gesture the whole thing rests on: drag it onto the model, it goes., A gesture that destroys something only fires where it clearly meant to., Refused at the door it would never reach the model; so it is let in., test_a_copy_dropped_on_the_model_is_thrown_away(), test_a_copy_is_let_into_the_window_wherever_it_arrives() (+2 more)

### Community 141 - ".mouseMoveEvent"
Cohesion: 0.20
Nodes (4): Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Apply the drag live, so the clay re-forms under the cursor.

### Community 142 - "paths.py"
Cohesion: 0.26
Nodes (13): available_matcaps(), _bundled_root(), image_path(), matcap_dir(), model_dir(), Path, Locations of the bundled resources. ``REFVIEW_RESOURCES`` overrides the search,…, Return PyInstaller's extracted application directory when frozen. (+5 more)

### Community 143 - "ShadingPanel"
Cohesion: 0.18
Nodes (10): Chooses the shading model and edits its light and surface parameters., Freeze the slices the way the camera faces now. The view direction is the one…, Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel, A matcap has no light to aim, so the Light group goes -- and its space. The…, ``self._mode`` is ``mode``; the group called Mode settles for a number., test_a_copied_group_still_drives_the_originals(), test_a_group_the_mode_does_not_answer_leaves_no_room_behind() (+2 more)

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

### Community 152 - "._built"
Cohesion: 0.25
Nodes (5): QImage, QRect, The matcap as a picture, at its own resolution. Square and opaque, with the…, Where the sphere goes: square, centred, above the legend., The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…

### Community 153 - "ask_for"
Cohesion: 0.22
Nodes (8): ask_for(), Command, QAction, A menu entry. Its keys are heard anywhere in the window and shown in the menu., A key heard only while the view has the focus. The menu entry for it, if there…, A key heard anywhere in the window, with no menu entry of its own., The gesture's other half: a key for whatever control was Ctrl-Alt-clicked.…, The gesture's other half: Ctrl-Alt-click on a button asks for a key. The…

### Community 154 - "restored"
Cohesion: 0.29
Nodes (7): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., A window with the saved layout out of the way, and put back after. Shown,…, A second window, built from a layout the first one saved. The point is…, restored(), window()

### Community 162 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 163 - ".update_enabled"
Cohesion: 0.17
Nodes (6): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., Follow the highlighted row, without rebuilding the list underneath it. Going…, Highlight the row for a node picked in the view., Highlight the row for a landmark picked in the view.

### Community 164 - "sample_count"
Cohesion: 0.50
Nodes (3): How many samples the framebuffer bound right now is drawing with. One where…, sample_count(), How many samples this view is really drawing with, or ``None``. Asked of GL…

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

### Community 169 - ".new_custom_panel"
Cohesion: 0.20
Nodes (6): _number_in(), An empty panel of the artist's own, docked on the right. A dock put away…, Take a hand-built panel away. Its dock is parked, not destroyed. The dock has…, Rebuild the panels built by hand. Call before :meth:`restore_state`. Whatever…, Put the layout back. Returns whether there was one to put back., The number at the end of a custom panel's key, or nought.

### Community 170 - "_height_of"
Cohesion: 0.40
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 171 - "_file_drag"
Cohesion: 0.40
Nodes (5): _file_drag(), A file being dragged over the middle of the view, as ``kind`` of event., Entering, moving and dropping: a drop lands only where the move before it was…, test_a_file_the_window_cannot_open_is_refused_on_the_way_past(), test_a_model_file_is_welcome_at_every_step_of_its_drag()

### Community 172 - "make_switch"
Cohesion: 0.28
Nodes (6): make_switch(), QCheckBox, Put a show/hide switch at the left of the bar and return it., A square that is on or off, and is clickable all over. A check box decides…, The square that shows or hides what a panel draws. One is kept on each dock's…, Switch

### Community 173 - ".reset"
Cohesion: 0.22
Nodes (5): QSettings, Bring the first panel to the front of the tab strip., The part of the layout Qt cannot describe., Write the whole layout, ours and Qt's, into the settings., Put every dock back where it started, now. Not "forget the saved layout and…

### Community 174 - "kept_off"
Cohesion: 0.50
Nodes (4): kept_off(), Which points lie in the sleeve a length of wire declares round itself. The wire…, Which material lies under a length of wire that is to take no clay. Turning a…, within_sleeve()

### Community 175 - "generate_matcaps.py"
Cohesion: 0.32
Nodes (7): Color, main(), _normalize(), ndarray, Path, Render the bundled matcap set. Each preset is evaluated analytically over the…, save()

### Community 177 - "PanelDock"
Cohesion: 0.25
Nodes (3): QDockWidget, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top.

### Community 178 - ".dress_tabs"
Cohesion: 0.29
Nodes (5): QTabBar, Hang a show/hide switch on every dock tab that wants one. A dock stacked behind…, The panel whose dock is called ``title``, if there is one., Let a strip of tabs keep its names, and scroll if they do not fit. Ten panels…, _widen()

### Community 179 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 180 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 181 - "orientation.py"
Cohesion: 0.33
Nodes (5): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis

### Community 182 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 183 - "test_the_disc_samples_where_the_shader_would"
Cohesion: 0.33
Nodes (6): parametrize, ``sampleMatcap``, transcribed from the GLSL, for a camera down +z. Deliberately…, The mapping :func:`sample` uses, for one normal rather than a grid., _shader_uv(), test_the_disc_samples_where_the_shader_would(), _widget_uv()

### Community 184 - "_create_splash"
Cohesion: 0.50
Nodes (5): QSplashScreen, _create_splash(), _fitted_title_font(), QFont, Largest title font that still draws the whole app name inside ``width``.

### Community 185 - "HotkeyDialog"
Cohesion: 0.50
Nodes (3): HotkeyDialog, QDialog, One keystroke for one command, and the question if it is already taken.

### Community 186 - "section"
Cohesion: 0.50
Nodes (4): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., section()

### Community 187 - "no_ffmpeg"
Cohesion: 0.67
Nodes (3): no_ffmpeg(), fixture, A machine with no video encoder on it, which is most of them.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `plane_axes`, `ExportLook`, `stone_field`, `mesh_renderer.py`, `viewport.py`, `SectionGizmo`, `ViewerState`, `carve`, `SectionSettings`, `plane_volume.py`, `TriangleIndex`, `PlaneSettings`, `test_plane_clusters.py`, `test_spatial.py`, `gltf_loader.py`, `ExportVideoDialog`, `plane_clusters.py`, `OrientationSettings`, `Landmark`, `PrimaryForm`, `test_plane_solids.py`, `Bounds`, `forms.py`, `state.py`, `SceneRenderer`, `test_mesh_io.py`, `FormStore`?**
  _High betweenness centrality (0.120) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `._buried_nodes`, `ExportLook`, `._place_form_landmark`, `MainWindow`, `viewport.py`, `main_window.py`, `SectionGizmo`, `.mouseMoveEvent`, `ViewerState`, `test_viewport_markers.py`, `PlaneSettings`, `sample_count`, `SurfacePicker`, `ExportVideoDialog`, `film_export.py`, `FilmExport`, `ArmatureTool`, `application.py`, `MeasureTool`, `PrimaryForm`, `NavigationController`, `Mesh`, `forms.py`, `_Encoder`, `._picker`, `._sync_scene`, `.mouseReleaseEvent`, `._place_armature_node`, `Preferences`, `ViewportOverlay`, `.stage_images`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `form_group`, `Viewport`, `Stroke`, `main_window.py`, `ViewerState`, `UpdateChecker`, `ask_for`, `restored`, `ControlsWindow`, `ExportVideoDialog`, `Workspace`, `application.py`, `test_hotkeys.py`, `HotkeyBinder`, `Path`, `test_panel_docks.py`, `._menu_action`, `Release`, `test_open_files.py`, `OpenRequests`, `._carrying_a_copy`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `MainWindow` (e.g. with `ExportVideoDialog` and `ControlsWindow`) actually correct?**
  _`MainWindow` has 9 INFERRED edges - model-reasoned connections that need verification._