# Graph Report - reference-viewer  (2026-09-14)

## Corpus Check
- 135 files · ~437,602 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4348 nodes · 9751 edges · 168 communities (150 shown, 18 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 460 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `68bcb195`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- form_group
- test_preferences.py
- Release
- Viewport
- plane_axes
- main_window.py
- MainWindow
- Stroke
- GifWriter
- mesh_renderer.py
- SceneRenderer
- plane_solids.py
- elements/__init__.py
- rebuild
- Armature
- README.md
- ViewerState
- PlaneSettings
- framebuffer.py
- CameraPanel
- UpdateChecker
- ShaderProgram
- test_viewport_markers.py
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- Writer
- SectionSettings
- plane_volume.py
- ControlsWindow
- TriangleIndex
- ShadingPanel
- mesh.py
- test_camera.py
- test_plane_clusters.py
- WakeLock
- MatcapPreview
- SectionPanel
- Frame
- film_export.py
- SurfacePicker
- Camera
- ArmatureNode
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
- load_obj
- OrientationSettings
- ._turn
- FilmExport
- FormsPanel
- PlanesPanel
- forms.py
- ArmatureTool
- Workspace
- section_segments
- test_forms.py
- application.py
- MeasureTool
- Link
- PrimaryForm
- History
- compute_vertex_normals
- AnnotatePanel
- test_plane_solids.py
- .__init__
- Session
- ndarray
- MeshBuffers
- load_matcap_pixels
- test_custom_panels.py
- .split_point
- core/preferences.py
- ContourShadingSettings
- NavigationController
- Bounds
- plane_count
- test_forms_panel.py
- picking.py
- MeshLoadError
- _clone_preview
- MatcapPanel
- ColorButton
- frame.py
- _Encoder
- ._picker
- test_elements.py
- FakeViewport
- FormRun
- ReflowLayout
- core/__init__.py
- ArmaturePanel
- CHANGELOG.md
- clone.py
- ._sync_scene
- Path
- paths.py
- .mouseReleaseEvent
- test_panel_docks.py
- ._build_menus
- ._place_armature_node
- test_mesh_io.py
- ._start_update_check
- DockTitle
- test_reflow.py
- MatcapSettings
- ndarray
- ArmatureStore
- ModelPanel
- ._on_bone_toggled
- .refresh
- ShadingMode
- SetAttributes
- ViewportOverlay
- release.yml
- _tick
- .stage_images
- _tab_switch
- shaders.py
- test_the_disc_samples_where_the_shader_would
- welded
- GuideRun
- section.py
- ._buried_nodes
- OverlayParts
- ExportLook
- ._place_form_landmark
- preview
- refview/__init__.py
- theme.py
- .film_changed
- box
- SectionGizmo
- _drag_over
- panel
- .with_landmark_at
- .refresh
- ._scene_center
- parametrize
- section
- _summary
- test_a_session_saved_without_panels_leaves_the_ones_open_alone
- .install
- coarse_lattice
- test_resetting_the_layout_puts_the_docks_back_at_once
- ._built
- ui/preferences.py
- restored
- test_resetting_keeps_the_panels_built_by_hand
- test_a_panel_does_not_cover_its_own_title
- test_the_switch_is_not_squeezed_to_nothing
- test_a_panel_can_be_taken_away_and_another_built_after_a_restore
- test_loading_a_session_over_a_restored_layout_survives
- test_the_dock_of_a_panel_taken_away_is_used_again
- test_a_reused_dock_does_not_bring_the_old_panels_contents_with_it
- Q: Where are the todo viewport marker and shading changes implemented?
- sample_count
- coarse_lattice
- environment.yml
- palette.py
- app

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 144 edges
2. `Viewport` - 118 edges
3. `Camera` - 83 edges
4. `PrimaryForm` - 79 edges
5. `ViewerState` - 79 edges
6. `MainWindow` - 76 edges
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

## Communities (168 total, 18 thin omitted)

### Community 0 - "form_group"
Cohesion: 0.11
Nodes (17): QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row(), The preferences as they stand. Treat as read-only; use :meth:`set`., QWidget, Fill in the groups. A switch with nothing to put in the caption column is given…, The one button that is not a preference, and what the window is for. (+9 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.07
Nodes (44): _clamp(), Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, Pull anything out of range back into it. The window cannot produce these…, Read the preferences off the machine. Never raises., app(), model() (+36 more)

### Community 2 - "Release"
Cohesion: 0.11
Nodes (30): check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed). (+22 more)

### Community 3 - "Viewport"
Cohesion: 0.07
Nodes (13): QOpenGLWidget, Slide the view so a point sits at the centre, keeping the angle., A form changed: work its clay out again and redraw., Slide the view so a measurement sits at the centre, keeping the angle., End any film being recorded, and wait for its thread to really stop. For…, The film of the form's making, as far as it has been recorded., Whether frames are being rendered out of a film right now., Free every GL object while the owning context is still current. (+5 more)

### Community 4 - "plane_axes"
Cohesion: 0.08
Nodes (37): plane_axes(), ndarray, A level with no place in it: nearest direction wins, as before., How much surface each vertex stands for: a third of each triangle on it.…, The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to., Split the mesh's normals into planes, keeping every count on the way., _split() (+29 more)

### Community 5 - "main_window.py"
Cohesion: 0.06
Nodes (46): QScrollArea, The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, MatcapLoadError, RuntimeError, Matcap texture loading and upload, and the small data table beside it., Raised when an image cannot be used as a matcap., framed() (+38 more)

### Community 6 - "MainWindow"
Cohesion: 0.06
Nodes (15): MainWindow, QMainWindow, Put the panels back where they started, now., Follow the machine's sleep to whether this window is in front., Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model., Wires the viewport, the panels and the document together. (+7 more)

### Community 7 - "Stroke"
Cohesion: 0.05
Nodes (39): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An empty stroke carrying the current brush., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface. (+31 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "mesh_renderer.py"
Cohesion: 0.10
Nodes (30): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-…, Return ``v`` scaled to unit length, or ``fallback`` for a zero vector. (+22 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.07
Nodes (34): Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, bind_default(), current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., Restore a framebuffer captured with :func:`current_framebuffer`., light_directions() (+26 more)

### Community 11 - "plane_solids.py"
Cohesion: 0.07
Nodes (33): planes_for(), How many solids each stage of a film is made of. Every count from the coarsest…, The detail setting that asks for ``solids``, or ``None`` if none does. The…, stage_counts(), block_count(), piece_count(), ndarray, Handing the planes of a fit to the thing that actually works the volume. The… (+25 more)

### Community 12 - "elements/__init__.py"
Cohesion: 0.08
Nodes (37): clone(), A working copy of ``source``, or ``None`` if its kind cannot be copied., Make every control under ``root`` that can be copied Alt-draggable. A group is…, watch_tree(), A panel the artist builds, out of copies of controls from the fixed ones. The…, One dock per panel, with a bar of its own across the top. Every panel is its…, The widgets the panels are built out of, and the rules they follow. Four ideas,…, _asked() (+29 more)

### Community 13 - "rebuild"
Cohesion: 0.15
Nodes (12): _kept_laying(), Fresh bones, laid the way the armature was already laying them. The bone list…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), Mirror what is missing, then rebuild the figure from the whole set. The…, A nudged landmark rebuilds the whole wire, and it would be intolerable for that…, test_a_freehand_armature_has_no_preset_to_rebuild_from(), test_a_locked_node_keeps_the_size_it_was_given() (+4 more)

### Community 14 - "Armature"
Cohesion: 0.06
Nodes (31): Armature, Bone, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves., A plausible thickness for a node placed by hand., What to call a bone: its own name, or the two nodes it runs between. (+23 more)

### Community 15 - "README.md"
Cohesion: 0.17
Nodes (15): High Quality shading mode (1.1.0), Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, High Quality without ray tracing, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance (+7 more)

### Community 16 - "ViewerState"
Cohesion: 0.08
Nodes (18): Path, QObject, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements, annotations,…, Take the display unit from the file when the format declares one. Only glTF… (+10 more)

### Community 17 - "PlaneSettings"
Cohesion: 0.04
Nodes (47): _empty(), The best ``count`` planes, or as many as the model supports. A model whose…, film_key(), What a film depends on. Everything that changes the shape of any stage, and…, Holds the working state between one turn of the sliders and the next.…, Drop everything held, so the next call starts from the fit., The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself. (+39 more)

### Community 18 - "framebuffer.py"
Cohesion: 0.07
Nodes (18): AccumTarget, ColorTarget, DepthTarget, FrameTarget, GeometryTarget, Offscreen render targets used by the high-quality, ghost and smoothing passes.…, A depth-only framebuffer, sampled afterwards as a texture., ``clamp_to_lit`` makes everything outside the map read as unshadowed. (+10 more)

### Community 19 - "CameraPanel"
Cohesion: 0.12
Nodes (7): CameraPanel, QListWidgetItem, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 21 - "ShaderProgram"
Cohesion: 0.12
Nodes (9): OpenGL rendering layer: shader programs, textures and the scene renderer., ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError (+1 more)

### Community 22 - "test_viewport_markers.py"
Cohesion: 0.08
Nodes (28): DepthDrag, draw_rail(), draw_text(), Shared marker appearance, visibility, and constrained depth gestures., A grid across the depth axis, at the depth the point has reached. Returns…, Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, The screen-space cue for one degree of freedom. A vertical rail that fades out…, A fixed world axis through the grabbed point; upward drags go deeper. (+20 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.08
Nodes (21): _names(), The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as…, Or there would be no way to turn one back on., A limb is four bones, and deciding not to block the arms in is one decision.…, It is rebuilt on every change, and ticking one row of a selected limb would be… (+13 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.09
Nodes (14): lock_icon(), A padlock, shut or hanging open. Open reads as "this measurement will move if…, MeasurePanel, _NameOnlyDelegate, QStyledItemDelegate, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row. (+6 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.12
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Deletion goes through the undo stack, so the store only tracks position., test_bookmarks_cycle_and_wrap() (+1 more)

### Community 26 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 27 - "SectionSettings"
Cohesion: 0.16
Nodes (17): How the model is cut open, and how the cut is drawn., SectionSettings, LightSettings, A key light, an opposing fill and a hemispherical ambient term., Material parameters shared by the analytic shading modes., SurfaceSettings, _box(), Cutting planes, the contour they produce and the pedestal under the model. (+9 more)

### Community 28 - "plane_volume.py"
Cohesion: 0.04
Nodes (114): Work the form stage by stage, handing each one back as it is finished. A…, record(), _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field() (+106 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "TriangleIndex"
Cohesion: 0.15
Nodes (13): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., Build the index from expanded triangle corners, shape ``(T, 3, 3)``. (+5 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.20
Nodes (9): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Slot that writes one field of the contour shading settings., ShadingPanel, test_a_copied_group_still_drives_the_originals() (+1 more)

### Community 32 - "mesh.py"
Cohesion: 0.05
Nodes (47): QThread, auto_smooth(), _gathered(), Triangle-mesh containers shared by the loader, the renderer and picking., Which group each of ``total`` things lands in, given pairs that agree. Hooking…, A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, PlaneSet, One level of a fit: the planes the shader is to quantise against. A plane is a… (+39 more)

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
Cohesion: 0.10
Nodes (12): QMenu, MatcapPreview, Path, QSize, QWidget, A matcap on a sphere, which is also how the matcap is graded., Offer the picture back as a file: as graded here, or as it came. A grading…, The matcap as a picture, at its own resolution. Square and opaque, with the… (+4 more)

### Community 37 - "SectionPanel"
Cohesion: 0.19
Nodes (6): Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 38 - "Frame"
Cohesion: 0.07
Nodes (25): carried(), _push_frame(), Nothing: each row inside the copy is linked on its own., Read a drag's payload back, or ``None`` if it is not one of ours., CustomPanel, _detach(), QFormLayout, QWidget (+17 more)

### Community 39 - "film_export.py"
Cohesion: 0.07
Nodes (21): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+13 more)

### Community 40 - "SurfacePicker"
Cohesion: 0.09
Nodes (20): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses., Continue the open run with a hit, or end it where the ray missed. (+12 more)

### Community 41 - "Camera"
Cohesion: 0.07
Nodes (18): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Screen-to-world scale at the focal plane; identical in both modes. (+10 more)

### Community 42 - "ArmatureNode"
Cohesion: 0.08
Nodes (25): ArmatureNode, One joint of the wire: where it is, and how thick the form is there., ndarray, The thickness a resize drag is asking for: the cursor's reach, in world units., Drop a new node into the middle of a bone, taking its thickness from the ends., What the armature becomes when a picked point is dropped into it. Returns the…, The same question in three dimensions, for interpolating along a bone., _share_between() (+17 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (13): _clone_slider(), _pull_slider(), _push_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end. (+5 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.13
Nodes (27): Units are adopted, never guessed, _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry(), _primitives() (+19 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.12
Nodes (12): QDialog, QProgressDialog, even(), ExportVideoDialog, Path, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Open the file and begin. Any failure here is reported, not raised., Where an artist says how the film should be written out. Everything on the… (+4 more)

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
Cohesion: 0.12
Nodes (10): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, Pump the event loop until ``done()`` or the clock runs out., run_until() (+2 more)

### Community 50 - "Mesh"
Cohesion: 0.04
Nodes (63): Mesh, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, Coefficients, PlaneAxes, Reading the planes of a form out of the model's own normals. The grid quantiser…, The planes a model falls into, at every count. Built once per mesh and per…, What each block of the design matrix counts for, against the normals. A fit… (+55 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.14
Nodes (24): QPoint, _drag(), The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc., Dragging further than the range goes is not a negative gamma., Alt and a drag copies a control; the disc must not swallow that., Tint and flip are not dragged on the disc, so they are not reset by it. (+16 more)

### Community 52 - "test_armature.py"
Cohesion: 0.09
Nodes (46): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other., The femoral head is in from the ASIS, below it and behind it, by shares of the…, A wire in two halves is not an armature anybody could bend. (+38 more)

### Community 53 - "load_obj"
Cohesion: 0.22
Nodes (14): load_obj(), ObjLoadError, Path, Raised when a file cannot be interpreted as an OBJ mesh., Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, Negative face indices count back from the most recent vertex., test_obj_relative_indices_still_load(), OBJ parsing: normals, triangulation and index handling. (+6 more)

### Community 54 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 55 - "._turn"
Cohesion: 0.17
Nodes (5): Redraw from the settings, which something else has changed., Put the grading back, which is the one thing a disc cannot show., Turn the matcap by the angle the cursor swept about the centre. By angle and…, Two grades on one drag: one along each axis of the movement. Both move together…, Keep the angle in -180 to 180, the range the setting is stored in.

### Community 56 - "FilmExport"
Cohesion: 0.14
Nodes (11): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in…, Offer the encoder the last stage before the first is written. Only the built-in… (+3 more)

### Community 57 - "FormsPanel"
Cohesion: 0.05
Nodes (29): FormsPanel, QTreeWidgetItem, Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Begin a run against a fresh form: a preset's walk, or a freeform's., Take up the selected freeform again, so more landmarks can go on it. The same…, The freeform the highlighted row belongs to, when no run is on. (+21 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.15
Nodes (11): PlanesPanel, Lay one length of wire earlier or later, as one undoable step., Hold the settings a recording is built from still while it runs. A film is a…, Show what this way of working needs, and put the rest away. A setting that does…, Breaks the form into planes, in the shading or in the geometry itself., The armature the clay is being built on, or ``None``. An index past the end of…, Re-read the armatures and what the chosen one is laying down. Called whenever…, The bones of the chosen armature, in the order the clay goes down. Every intact… (+3 more)

### Community 59 - "forms.py"
Cohesion: 0.05
Nodes (47): DegenerateHullError, The points are flat, collinear or too few to hold any volume., build_freeform(), _centre(), FormFill, FormPreset, FormStage, FormStore (+39 more)

### Community 60 - "ArmatureTool"
Cohesion: 0.06
Nodes (43): LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, Handle, The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now., How many landmarks are placed, out of how many will be asked for. (+35 more)

### Community 61 - "Workspace"
Cohesion: 0.05
Nodes (28): QDockWidget, QTabBar, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top., _number_in(), QMainWindow, QObject, QSettings (+20 more)

### Community 62 - "section_segments"
Cohesion: 0.18
Nodes (9): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, Unit axis, or ``None`` for a custom direction., A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., section_segments() (+1 more)

### Community 63 - "test_forms.py"
Cohesion: 0.04
Nodes (98): convex_hull(), flat_mesh(), merged(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, The outward unit normal at each vertex: the area-weighted mean of its faces'. A… (+90 more)

### Community 64 - "application.py"
Cohesion: 0.14
Nodes (17): ArgumentParser, Namespace, QSplashScreen, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font(), main() (+9 more)

### Community 65 - "MeasureTool"
Cohesion: 0.12
Nodes (10): MeasureTool, Handle, ndarray, The nearest grabbable endpoint under the cursor, if any. Only unlocked, visible…, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview. (+2 more)

### Community 66 - "Link"
Cohesion: 0.11
Nodes (10): CloneGesture, Link, _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original., Whether the copy is being used right now and must not be written. (+2 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.04
Nodes (85): FormLandmarkRef, PlacedLandmark, One anatomical point the artist put on the model during a guided run., build_form(), built_count(), form_landmark_title(), form_mesh(), form_spec() (+77 more)

### Community 68 - "History"
Cohesion: 0.08
Nodes (22): Camera motion is deliberately not undoable, AddItem, Append an item to a document list., Command, History, One reversible change, named for the undo menu., A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive… (+14 more)

### Community 69 - "compute_vertex_normals"
Cohesion: 0.17
Nodes (18): compute_vertex_normals(), Area-weighted smooth vertex normals for an indexed triangle soup., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic() (+10 more)

### Community 70 - "AnnotatePanel"
Cohesion: 0.19
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 71 - "test_plane_solids.py"
Cohesion: 0.03
Nodes (133): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), film_of(), parametrize, Scrubbing through the making of a form, rather than only arriving at it. The…, A cut takes material away, so no stage of a carving is larger than the one… (+125 more)

### Community 72 - ".__init__"
Cohesion: 0.18
Nodes (4): Give each panel a dock of its own, tabbed together on the right. Each panel can…, Single-key shortcuts, scoped so they never eat text input. They only fire while…, Push the preferences that this window's own parts hold a copy of. The store has…, Put the docks and the hand-built panels back where they were. Unless the artist…

### Community 73 - "Session"
Cohesion: 0.12
Nodes (20): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Path (+12 more)

### Community 74 - "ndarray"
Cohesion: 0.17
Nodes (5): ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, test_bounds_of_an_empty_point_set(), ValueError

### Community 75 - "MeshBuffers"
Cohesion: 0.06
Nodes (16): MeshBuffers, Forget the contents without releasing the buffer objects., Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are…, Whichever geometry is standing for the model this frame., Replace the annotation geometry; pass an empty list to hide it., Vertex/index buffers for one mesh, bound through a single VAO. (+8 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.15
Nodes (23): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+15 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.07
Nodes (23): QMimeData, app(), custom(), _drop_on(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error., A group is not a row, so it goes ahead of the group it was dropped on. (+15 more)

### Community 78 - ".split_point"
Cohesion: 0.20
Nodes (9): BoneRef, _project(), The nearest bone under the cursor, for showing its length., Where on a bone a click at ``(x, y)`` landed. The share along the bone is read…, A world point in widget pixels, or ``None`` when it is behind the camera., How far along a screen-space segment the cursor's nearest point lies., Pixels from the cursor to the segment, or ``None`` if either end is behind., _segment_distance() (+1 more)

### Community 79 - "core/preferences.py"
Cohesion: 0.12
Nodes (18): _as_kind_of(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any, What the artist prefers, as distinct from what the document says. There are two… (+10 more)

### Community 80 - "ContourShadingSettings"
Cohesion: 0.20
Nodes (8): ContourShadingSettings, Parallel slices drawn across the form, the way a contour map reads land. The…, The unit direction the slices are stacked along, in world space., parametrize, The contour shading mode: slices across the form, read off it like a map., test_a_custom_direction_is_normalised_and_an_empty_one_falls_back(), test_the_density_floor_keeps_the_spacing_finite(), test_the_slices_face_the_way_that_was_asked()

### Community 81 - "NavigationController"
Cohesion: 0.07
Nodes (28): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Degrees of yaw per pixel, signed by whether the drag is inverted. (+20 more)

### Community 82 - "Bounds"
Cohesion: 0.18
Nodes (15): Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray, A turntable-style disc the model can stand on. A ground plane gives the eye… (+7 more)

### Community 83 - "plane_count"
Cohesion: 0.20
Nodes (7): _along(), plane_count(), Where a detail setting sits on its slider, 0 to 1., How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., How much of a turn in the surface one plane covers, in degrees. Linear in…, How many planes a mode fitted to the model keeps. The climb from two planes to…, How many planes the form itself is rebuilt out of.

### Community 84 - "test_forms_panel.py"
Cohesion: 0.11
Nodes (30): app(), _click(), panel(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The… (+22 more)

### Community 85 - "picking.py"
Cohesion: 0.08
Nodes (36): Projection, Enum, str, Projection used by :class:`Camera`., Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test… (+28 more)

### Community 86 - "MeshLoadError"
Cohesion: 0.16
Nodes (17): STL corner welding, MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., _ascii_corners(), _binary_corners(), load_stl(), ndarray (+9 more)

### Community 87 - "_clone_preview"
Cohesion: 0.27
Nodes (6): _clone_preview(), _pull_preview(), ndarray, Point the preview at the settings it edits. The object itself, not a copy: this…, The matcap image, in the orientation the renderer uploads it. ``None`` for the…, The matcap image this is drawing, for a copy of it to draw too.

### Community 88 - "MatcapPanel"
Cohesion: 0.10
Nodes (18): QIcon, _draw_glyph(), glyph(), QColor, QPixmap, One of the small line drawings above, as an icon. A button whose whole job is…, _render(), MatcapPanel (+10 more)

### Community 89 - "ColorButton"
Cohesion: 0.11
Nodes (12): _clone_swatch(), _pull_swatch(), _push_swatch(), _AxisBox, ColorButton, QColor, QDoubleSpinBox, QSize (+4 more)

### Community 90 - "frame.py"
Cohesion: 0.08
Nodes (14): FrameBar, QFormLayout, QPainter, QSize, QWidget, A titled frame that folds away behind its own bar. Every group of controls in…, The mark beside a group's name: filled when open, a ring when shut. It is the…, The rows inside the frame. ``layout()`` is the frame's own, which stacks the… (+6 more)

### Community 91 - "_Encoder"
Cohesion: 0.22
Nodes (6): Queue, _Encoder, QObject, QWidget, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 92 - "._picker"
Cohesion: 0.11
Nodes (9): Rub out the stroke points under the eraser, live., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…, Apply the drag live, so the artist sees the wire bend as they pull it., Take hold of a landmark, to move it or just to say which one it is., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Take hold of a form's landmark, to move it or just to say which one it is. (+1 more)

### Community 93 - "test_elements.py"
Cohesion: 0.11
Nodes (10): Copies of controls: what they drive, and what keeps them honest. The contract a…, Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., A matcap has no light to aim, so the Light group goes -- and its space. The…, ``self._mode`` is ``mode``; the group called Mode settles for a number., test_a_folded_group_is_only_as_tall_as_its_bar(), test_a_group_comes_back_the_way_it_was_left(), test_a_group_folds_away_when_its_settings_go_dead() (+2 more)

### Community 94 - "FakeViewport"
Cohesion: 0.28
Nodes (3): FakeViewport, QImage, A viewport that renders nothing, at whatever size it is asked for.

### Community 95 - "FormRun"
Cohesion: 0.40
Nodes (3): FormRun, Begin a run against a form already in the store., A guided form part-way through.

### Community 96 - "ReflowLayout"
Cohesion: 0.08
Nodes (19): Orientations, QLayout, QLayoutItem, _height_of(), QRect, QSize, QWidget, How many columns this layout would break into at ``width``. (+11 more)

### Community 97 - "core/__init__.py"
Cohesion: 0.04
Nodes (61): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, What the annotate tool does with a drag. The first three describe the shape a…, BoneLabels, Buried, Enum (+53 more)

### Community 98 - "ArmaturePanel"
Cohesion: 0.04
Nodes (34): ArmaturePanel, _NameOnlyDelegate, QPushButton, QStyledItemDelegate, QWidget, Allows in-place editing of the name column only., Arms the armature tool, lists its nodes and runs the guided presets., Add a group below the list rather than to the panel root. (+26 more)

### Community 99 - "CHANGELOG.md"
Cohesion: 0.25
Nodes (7): Shift-snapped orbiting (1.1.0), Cross-section tool (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4

### Community 100 - "clone.py"
Cohesion: 0.05
Nodes (65): QAbstractButton, QComboBox, QLineEdit, QSlider, QSpinBox, _begin(), can_clone(), _clone_button() (+57 more)

### Community 101 - "._sync_scene"
Cohesion: 0.12
Nodes (6): Regenerate the pedestal and the cut contour when their settings move. Both are…, The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on., Cut the mesh with each section plane and expand the result to strokes.

### Community 102 - "Path"
Cohesion: 0.15
Nodes (9): Path, Take a copied control out of whichever hand-built panel holds it., A path written down last time, if it is one and it is still there., Apply a matcap image, reporting unreadable files to the user., Pick up whatever was last being worked on, if that was asked for. A session…, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window. (+1 more)

### Community 103 - "paths.py"
Cohesion: 0.26
Nodes (13): available_matcaps(), _bundled_root(), image_path(), matcap_dir(), model_dir(), Path, Locations of the bundled resources. ``REFVIEW_RESOURCES`` overrides the search,…, Return PyInstaller's extracted application directory when frozen. (+5 more)

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.11
Nodes (9): Record the finished drag as a single undo step., Record the finished gesture: a move, a resize, or a plain click. A press that…, Record the finished drag as one step, or read a press as a selection., Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…, Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Record the finished drag as one step, or read a press as a selection. (+1 more)

### Community 105 - "test_panel_docks.py"
Cohesion: 0.13
Nodes (4): Each panel in a dock of its own, and putting the docks back next time. Two…, test_a_restored_copy_drives_the_new_windows_own_control(), test_a_session_carries_the_hand_built_panels(), test_the_layout_comes_back_through_the_settings()

### Community 106 - "._build_menus"
Cohesion: 0.25
Nodes (4): QAction, Which panels are open, and the panels the artist builds. Rebuilt every time it…, Add a menu entry, optionally with a window-wide shortcut., Open the preferences, on one group when the menu asked for one.

### Community 107 - "._place_armature_node"
Cohesion: 0.22
Nodes (4): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…, The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…

### Community 108 - "test_mesh_io.py"
Cohesion: 0.20
Nodes (15): STL and glTF import (1.1.0), load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+7 more)

### Community 109 - "._start_update_check"
Cohesion: 0.29
Nodes (4): Ask GitHub for the newest release in the background. The startup check is…, QWidget, show_failure_dialog(), show_up_to_date_dialog()

### Community 110 - "DockTitle"
Cohesion: 0.09
Nodes (13): QToolButton, DockTitle, make_switch(), QCheckBox, QSize, QWidget, Put a show/hide switch at the left of the bar and return it., A square that is on or off, and is clickable all over. A check box decides… (+5 more)

### Community 111 - "test_reflow.py"
Cohesion: 0.14
Nodes (20): app(), _block(), _panel(), fixture, QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., One offscreen Qt application for the run; see test_film_recorder. (+12 more)

### Community 112 - "MatcapSettings"
Cohesion: 0.16
Nodes (16): MatcapSettings, Post-processing applied to the sampled matcap texel., _angle(), grade(), _push_preview(), The matcap itself, as the control for grading it. A matcap is a picture of a…, Draw the matcap onto a sphere of ``size`` pixels, graded. Returns ``(size,…, The angle of ``point`` about ``centre``, anticlockwise with y upwards. (+8 more)

### Community 113 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 114 - "ArmatureStore"
Cohesion: 0.18
Nodes (4): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 116 - "._on_bone_toggled"
Cohesion: 0.29
Nodes (4): QListWidgetItem, Catch the selection a click on a checkbox is about to collapse. Qt selects a…, Which bones of the armature the picked-out rows stand for., Take lengths of wire out of the clay, or put them back. A tick on a row that…

### Community 118 - "ShadingMode"
Cohesion: 0.17
Nodes (4): Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode, TestEven

### Community 119 - "SetAttributes"
Cohesion: 0.09
Nodes (13): Every document edit is a command, Any, Assign one or more attributes on an object, remembering the old values.…, Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems, SetAttributes (+5 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.13
Nodes (23): QPointF, QRectF, One marker object for endpoints, nodes, landmarks and tool previews., VisualMarker, project_visible(), Handle, QColor, QFont (+15 more)

### Community 121 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 122 - "_tick"
Cohesion: 0.29
Nodes (7): The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Run the refresh the shared timer would have run., test_a_copy_follows_the_original_on_the_tick(), test_a_copy_goes_dead_when_its_original_does(), test_switching_the_original_off_switches_the_copy_off(), _tick()

### Community 123 - ".stage_images"
Cohesion: 0.23
Nodes (7): QOpenGLFramebufferObject, QImage, One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A…, An offscreen target the frames are drawn into, made once per export.…, Draw the scene into ``surface`` and read it back as an image., Lay the overlay -- and the caption, if it was asked for -- on a frame. Painted…

### Community 124 - "_tab_switch"
Cohesion: 0.29
Nodes (7): The show/hide switch on the tab named ``title``, if it has one., Stacked behind another panel is where the switch is worth the most., It is fifteen pixels wide and carries no words, which is exactly the shape the…, _tab_switch(), test_a_panel_that_draws_nothing_gets_no_switch_on_its_tab(), test_a_tabbed_panel_still_shows_its_switch(), test_clicking_the_switch_on_a_tab_works()

### Community 125 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 126 - "test_the_disc_samples_where_the_shader_would"
Cohesion: 0.33
Nodes (6): parametrize, ``sampleMatcap``, transcribed from the GLSL, for a camera down +z. Deliberately…, The mapping :func:`sample` uses, for one normal rather than a grid., _shader_uv(), test_the_disc_samples_where_the_shader_would(), _widget_uv()

### Community 127 - "welded"
Cohesion: 0.67
Nodes (3): ndarray, Which point each vertex really is, once copies of a position are one point., welded()

### Community 128 - "GuideRun"
Cohesion: 0.40
Nodes (3): GuideRun, Begin a preset run against an armature already in the store., A guided preset part-way through. The index walks the preset's own list rather…

### Community 129 - "section.py"
Cohesion: 0.21
Nodes (7): Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Which side of the plane survives the cut., SectionAxis, SectionMode

### Community 131 - "OverlayParts"
Cohesion: 0.18
Nodes (5): Which of the things drawn over the model belong in the frames., MarkerVisibility, Cache surface occlusion by view and position for every kind of marker., OverlayParts, Which of the things drawn over the model are wanted this time. The viewport…

### Community 132 - "ExportLook"
Cohesion: 0.15
Nodes (10): The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, ExportLook, What the frames are to look like, as against what they are of. Laid over the…, ``base`` with this export's choices laid over it., The line burned into the corner of the frame for ``stage``. Counted off the… (+2 more)

### Community 134 - "preview"
Cohesion: 0.40
Nodes (5): app(), preview(), fixture, One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 136 - "theme.py"
Cohesion: 0.15
Nodes (12): css(), A colour as a style sheet function, for the parts Qt draws., QObject, Making the whole of a switch the part you can press. The theme turns every…, Turns a press anywhere on a switch into a click on it., WholeFaceToggles, apply_dark_theme(), QApplication (+4 more)

### Community 138 - "box"
Cohesion: 0.50
Nodes (4): box(), A unit cube, shaded flat: six planes and twelve right angles., Every edge of a cube is a right angle, and no reading of AutoSmooth short of…, test_autosmooth_leaves_a_real_plane_change_hard()

### Community 139 - "SectionGizmo"
Cohesion: 0.18
Nodes (8): Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo, ndarray, Rotate the measurements, annotations, armature and forms onto the turned model.…, The rail stands still while the camera moves, and never leaves the frame., test_section_rail_is_a_screen_space_cue_at_the_right_edge()

### Community 140 - "_drag_over"
Cohesion: 0.22
Nodes (10): _drag_over(), _middle_of_the_view(), A drag of ``holder`` arriving at ``point`` in the window's coordinates. A real…, The gesture the whole thing rests on: drag it onto the model, it goes., A gesture that destroys something only fires where it clearly meant to., Refused at the door it would never reach the model; so it is let in., test_a_copy_dropped_on_the_model_is_thrown_away(), test_a_copy_is_let_into_the_window_wherever_it_arrives() (+2 more)

### Community 141 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 145 - "parametrize"
Cohesion: 0.67
Nodes (3): parametrize, test_a_panel_that_draws_nothing_has_no_switch(), test_the_switch_on_a_dock_bar_is_the_panels_own_visibility()

### Community 146 - "section"
Cohesion: 0.50
Nodes (4): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., section()

### Community 149 - ".install"
Cohesion: 0.29
Nodes (6): QApplication, Put the rule in place for every switch in the application., The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter., test_a_switch_answers_a_press_anywhere_on_its_face(), test_alt_is_left_alone_so_a_switch_can_still_be_copied()

### Community 150 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 152 - "._built"
Cohesion: 0.33
Nodes (4): QImage, QRect, Where the sphere goes: square, centred, above the legend., The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…

### Community 153 - "ui/preferences.py"
Cohesion: 0.11
Nodes (18): current(), forget(), PreferenceStore, QObject, QSettings, _qcolor(), Where the preferences are kept, and what happens when one changes.…, Push the preferences that something in the process holds a copy of.… (+10 more)

### Community 154 - "restored"
Cohesion: 0.29
Nodes (7): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., A second window, built from a layout the first one saved. The point is…, A window with the saved layout out of the way, and put back after. Shown,…, restored(), window()

### Community 162 - "Q: Where are the todo viewport marker and shading changes implemented?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Where are the todo viewport marker and shading changes implemented?, Source Nodes

### Community 164 - "sample_count"
Cohesion: 0.50
Nodes (3): How many samples the framebuffer bound right now is drawing with. One where…, sample_count(), How many samples this view is really drawing with, or ``None``. Asked of GL…

### Community 167 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 168 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 171 - "palette.py"
Cohesion: 0.25
Nodes (7): outline(), QColor, The colours the hand-drawn elements paint with. Kept apart from…, Draw the hairline that separates a control from the panel. One line, the same…, Change the one colour that is not grey, everywhere at once. The hand-painted…, set_accent(), The slider the whole application is set with. One flat bar: the name of the…

### Community 173 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

## Knowledge Gaps
- **4 isolated node(s):** `refview`, `Answer`, `Outcome`, `Source Nodes`
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `section.py`, `plane_axes`, `ExportLook`, `mesh_renderer.py`, `box`, `plane_solids.py`, `SectionGizmo`, `README.md`, `ViewerState`, `PlaneSettings`, `test_viewport_markers.py`, `SectionSettings`, `plane_volume.py`, `TriangleIndex`, `mesh.py`, `test_plane_clusters.py`, `gltf_loader.py`, `VideoSettings`, `load_obj`, `OrientationSettings`, `FilmExport`, `forms.py`, `section_segments`, `test_forms.py`, `PrimaryForm`, `compute_vertex_normals`, `test_plane_solids.py`, `ndarray`, `MeshBuffers`, `Bounds`, `picking.py`, `MeshLoadError`, `FakeViewport`, `core/__init__.py`, `test_mesh_io.py`, `ShadingMode`, `welded`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `test_preferences.py`, `._buried_nodes`, `ExportLook`, `main_window.py`, `MainWindow`, `._place_form_landmark`, `SectionGizmo`, `ViewerState`, `._scene_center`, `test_viewport_markers.py`, `mesh.py`, `sample_count`, `film_export.py`, `SurfacePicker`, `ExportVideoDialog`, `FilmExport`, `ArmatureTool`, `MeasureTool`, `PrimaryForm`, `.__init__`, `NavigationController`, `_Encoder`, `._picker`, `core/__init__.py`, `._sync_scene`, `.mouseReleaseEvent`, `._place_armature_node`, `ViewportOverlay`, `.stage_images`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `application.py`, `core/__init__.py`, `Release`, `form_group`, `History`, `main_window.py`, `Path`, `Viewport`, `.__init__`, `test_panel_docks.py`, `._build_menus`, `ExportVideoDialog`, `._start_update_check`, `ViewerState`, `Workspace`, `UpdateChecker`, `restored`, `ControlsWindow`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PrimaryForm` (e.g. with `PlacedLandmark` and `DegenerateHullError`) actually correct?**
  _`PrimaryForm` has 7 INFERRED edges - model-reasoned connections that need verification._