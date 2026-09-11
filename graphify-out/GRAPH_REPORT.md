# Graph Report - reference-viewer  (2026-09-12)

## Corpus Check
- 98 files · ~369,823 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2892 nodes · 6510 edges · 134 communities (124 shown, 10 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 294 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `069cca0f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Stroke
- FilmRecorder
- Release
- Viewport
- plane_axes
- AnnotateTool
- MainWindow
- ViewerState
- GifWriter
- Measurement
- SceneRenderer
- _wires
- mesh_renderer.py
- Mesh
- Armature
- README.md
- SetAttributes
- main_window.py
- AccumTarget
- CameraPanel
- test_plane_film.py
- ShaderProgram
- ViewportOverlay
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- NavigationController
- SectionSettings
- SectionPanel
- test_session.py
- Session
- ShadingPanel
- Panel
- test_camera.py
- test_plane_clusters.py
- WakeLock
- ndarray
- History
- update_check.py
- film_export.py
- load_obj
- Camera
- test_armature.py
- ExportLook
- UpdateChecker
- ExportVideoDialog
- VideoSettings
- landmarks.py
- Agent Graph-First Instructions
- ._set_geometry
- plane_clusters.py
- MeshBuffers
- PlacedLandmark
- ColorButton
- OrientationSettings
- viewport.py
- FilmExport
- _derived
- PlanesPanel
- Bounds
- clay_lumps
- Path
- .update_enabled
- _shifts
- MatcapPanel
- overlay.py
- open_writer
- plane_volume.py
- PlaneMode
- stone_field
- ReplaceItems
- test_plane_solids.py
- load_matcap_pixels
- raycast_mesh
- StrokeBuffers
- ArmatureStore
- application.py
- carve
- ArmaturePanel
- VideoError
- armature_panel.py
- ArmatureTool
- PlaneSettings
- ._selected
- Command
- box
- paths.py
- ._picker
- ._build
- annotation.py
- Writer
- _create_splash
- .mousePressEvent
- ShadingMode
- block_splits
- record
- ._chosen_armature
- test_annotation.py
- _Encoder
- shaders.py
- .refresh_list
- coarse_lattice
- CHANGELOG.md
- wakelock.py
- ._commit_node_drag
- ._upload_sculpt
- ._draw_hud
- ._place_armature_node
- .surface_opacity
- _ScreenSaverBackend
- _WindowsBackend
- union_field
- refview/__init__.py
- .new_armature
- _MacBackend
- ModelPanel
- ._sync_scene
- FakeViewport
- .split
- kept_off
- _wire_frame
- test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else
- ._accumulate_ghost
- rounded
- .pan
- _NameOnlyDelegate
- _NameOnlyDelegate
- ._selected_rows
- .film_changed
- test_relaxing_settles_the_clay_and_leaves_the_stone_alone
- panel
- .matrix
- ._buried_nodes
- _summary

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 126 edges
2. `Viewport` - 90 edges
3. `Camera` - 75 edges
4. `Armature` - 73 edges
5. `PlaneSettings` - 67 edges
6. `ArmaturePanel` - 60 edges
7. `ViewerState` - 54 edges
8. `ArmatureTool` - 52 edges
9. `MainWindow` - 50 edges
10. `SceneRenderer` - 46 edges

## Surprising Connections (you probably didn't know these)
- `Orthographic extent derived from FOV and distance` --rationale_for--> `Camera`  [EXTRACTED]
  README.md → src/refview/core/camera.py
- `Pedestal (1.1.0)` --rationale_for--> `PedestalSettings`  [EXTRACTED]
  CHANGELOG.md → src/refview/core/pedestal.py
- `REFVIEW_RESOURCES resource override` --rationale_for--> `available_matcaps()`  [EXTRACTED]
  README.md → src/refview/paths.py
- `The cut interior is flooded flat` --rationale_for--> `SceneRenderer`  [INFERRED]
  README.md → src/refview/render/mesh_renderer.py
- `Terracotta clay matcap` --shares_data_with--> `load_matcap_pixels()`  [INFERRED]
  resources/matcaps/clay_terracotta.png → src/refview/render/texture.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The bundled matcap set** — resources_matcaps_clay_terracotta_matcap, resources_matcaps_charcoal_matcap, resources_matcaps_jade_matcap, resources_matcaps_steel_matcap, resources_matcaps_studio_white_matcap, resources_matcaps_wax_skin_matcap, tools_generate_matcaps_matcappreset, tools_generate_matcaps_render [INFERRED 0.85]
- **The four generic undo commands** — src_refview_core_commands_setattributes, src_refview_core_commands_additem, src_refview_core_commands_removeitem, src_refview_core_commands_replaceitems, src_refview_core_history_command, readme_every_edit_is_a_command [EXTRACTED 1.00]
- **Windows binary-compatibility decisions** — readme_pyside6_pinned_below_68, environment_pip_installed_binaries, environment_python_311, github_workflows_release_pyinstaller_build [INFERRED 0.75]

## Communities (134 total, 10 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.12
Nodes (12): AnnotationStore, An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Stroke, The strokes being laid down; the overlay previews them in 2D., The surviving arc wraps past the start of the list, so the gap is rotated to… (+4 more)

### Community 1 - "FilmRecorder"
Cohesion: 0.09
Nodes (18): QThread, Film, The stage at ``index``, clamped to what has actually been recorded., A whole making, from the coarsest stage to the one the slider asks for. Held by…, FilmRecorder, QObject, The film being recorded, or the last one finished., Whether a film is being made right now. (+10 more)

### Community 2 - "Release"
Cohesion: 0.18
Nodes (12): The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, is_skipped(), QWidget, Background release check and the notice it puts in front of the artist. The…, Whether the artist already dismissed this exact version., Offer the release page, with the option never to be asked again. (+4 more)

### Community 3 - "Viewport"
Cohesion: 0.11
Nodes (10): QOpenGLWidget, Slide the view so a point sits at the centre, keeping the angle., End any film being recorded, and wait for its thread to really stop. For…, The document being drawn., Whether frames are being rendered out of a film right now., Free every GL object while the owning context is still current., Arm one tool, disarming the rest. Only one gesture can own the left button, so…, Drop whatever gesture is half-finished, without disarming the tool. (+2 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - "AnnotateTool"
Cohesion: 0.13
Nodes (13): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses., Continue the open run with a hit, or end it where the ray missed. (+5 more)

### Community 6 - "MainWindow"
Cohesion: 0.07
Nodes (15): QAction, QMainWindow, QScrollArea, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits. (+7 more)

### Community 7 - "ViewerState"
Cohesion: 0.10
Nodes (14): ndarray, Path, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements, annotations…, Rotate the measurements, annotations and armature onto the turned model. A… (+6 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "Measurement"
Cohesion: 0.11
Nodes (11): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+3 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.11
Nodes (23): Everything the viewport needs in order to draw a frame., RenderSettings, light_directions(), normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.… (+15 more)

### Community 11 - "_wires"
Cohesion: 0.11
Nodes (32): The order the artist put the bones in is what the scrub walks through, which is…, The claim the whole film rests on, asked again with an armature under it: an…, test_a_film_of_clay_on_a_wire_lays_it_down_in_the_order_it_was_listed(), test_the_last_stage_of_a_film_on_a_wire_is_the_form_the_slider_gives(), _bar(), _bed_for(), _holds(), A long ellipsoid: one closed form with an obvious axis to lie along. (+24 more)

### Community 12 - "mesh_renderer.py"
Cohesion: 0.09
Nodes (32): Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., look_at(), normalize(), orthographic() (+24 more)

### Community 13 - "Mesh"
Cohesion: 0.04
Nodes (81): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry() (+73 more)

### Community 14 - "Armature"
Cohesion: 0.05
Nodes (37): Armature, ArmatureNode, Bone, ndarray, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, Every node position as ``(n, 3)``., The two points a bone runs between, or ``None`` if it dangles. (+29 more)

### Community 15 - "README.md"
Cohesion: 0.10
Nodes (23): High Quality shading mode (1.1.0), numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix (+15 more)

### Community 16 - "SetAttributes"
Cohesion: 0.19
Nodes (6): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Run a row's edit once Qt has finished delivering the current signal. Committing…, Record an edit the viewport's tool worked out., Join two nodes of one armature, if they are two and they are one armature., Commit a renamed or re-checked row, if anything actually changed.

### Community 17 - "main_window.py"
Cohesion: 0.05
Nodes (58): QGroupBox, Named camera positions the artist can jump between while sculpting., The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, Named point-to-point measurements and their presentation options., Coefficients, What each block of the design matrix counts for, against the normals. A fit…, Whether anything but the normals is being read at all. (+50 more)

### Community 18 - "AccumTarget"
Cohesion: 0.08
Nodes (16): AccumTarget, ColorTarget, DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality and ghost passes. Four of…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the…, The pair of buffers a see-through model is summed into. Attachment 0 holds the… (+8 more)

### Community 19 - "CameraPanel"
Cohesion: 0.12
Nodes (7): CameraPanel, QListWidgetItem, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "test_plane_film.py"
Cohesion: 0.08
Nodes (34): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, coarse_lattice(), film_of(), fixture, MonkeyPatch, parametrize, Scrubbing through the making of a form, rather than only arriving at it. The… (+26 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.14
Nodes (7): ndarray, RuntimeError, Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "ViewportOverlay"
Cohesion: 0.17
Nodes (18): QColor, QPainter, QPointF, project_visible(), Handle, A line laid over its own dark outline, so it reads against anything., An unfilled circle: how thick the form is here, not how big a dot is., A square grip, so an editable end reads differently from a fixed one. (+10 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.08
Nodes (21): _names(), The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as…, Or there would be no way to turn one back on., A limb is four bones, and deciding not to block the arms in is one decision.…, It is rebuilt on every change, and ticking one row of a selected limb would be… (+13 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.14
Nodes (8): MeasurePanel, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn.

### Community 25 - "BookmarkStore"
Cohesion: 0.11
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around. (+1 more)

### Community 26 - "NavigationController"
Cohesion: 0.13
Nodes (11): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+3 more)

### Community 27 - "SectionSettings"
Cohesion: 0.12
Nodes (22): ndarray, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn. (+14 more)

### Community 28 - "SectionPanel"
Cohesion: 0.11
Nodes (13): Enum, str, The direction the section plane faces., Unit axis, or ``None`` for a custom direction., Which side of the plane survives the cut., SectionAxis, SectionMode, Turn the cut on or off, for the menu and the keyboard shortcut. (+5 more)

### Community 29 - "test_session.py"
Cohesion: 0.08
Nodes (22): Session file that sits beside a model, e.g. ``bust.refview.json``., sidecar_path(), Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., A step of the slider is worth a fixed share more planes, not a fixed number of…, The ceiling went from 64 planes to 256 without moving the slider under anyone:…, The panel edits the settings; the fit has to be told what they are., Both modes answer in degrees of turn, so the panel can just ask. (+14 more)

### Community 30 - "Session"
Cohesion: 0.15
Nodes (15): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Path (+7 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.21
Nodes (7): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel

### Community 32 - "Panel"
Cohesion: 0.21
Nodes (5): Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block.

### Community 33 - "test_camera.py"
Cohesion: 0.11
Nodes (8): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_serialisation_round_trip(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (58): angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What… (+50 more)

### Community 35 - "WakeLock"
Cohesion: 0.17
Nodes (13): Holds sleep off while the window that owns it is the one in front. The class…, WakeLock, Broken, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do., A platform that refuses, the way an old or locked-down one might., The viewer must open and close normally on a machine that says no., Recorder (+5 more)

### Community 36 - "ndarray"
Cohesion: 0.13
Nodes (21): _back_inside(), dual_contour(), _flat_mesh(), ndarray, The surface where ``value`` changes sign, one vertex per lattice cell. Each…, The gradient of a lattice field, by central differences. Which is the direction…, Drop the loose pieces, keeping the form and anything of its size. A block is a…, Read lattice fields at places between their corners, straight-line. Nearest-… (+13 more)

### Community 37 - "History"
Cohesion: 0.14
Nodes (16): AddItem, Append an item to a document list., History, A bounded undo/redo stack., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made() (+8 more)

### Community 38 - "update_check.py"
Cohesion: 0.14
Nodes (22): check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed). (+14 more)

### Community 39 - "film_export.py"
Cohesion: 0.07
Nodes (21): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+13 more)

### Community 40 - "load_obj"
Cohesion: 0.12
Nodes (24): load_obj(), Path, Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+16 more)

### Community 41 - "Camera"
Cohesion: 0.08
Nodes (25): Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling… (+17 more)

### Community 42 - "test_armature.py"
Cohesion: 0.08
Nodes (50): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _chain(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., The femoral head is inside the bump you can feel, not on it., A wire in two halves is not an armature anybody could bend. (+42 more)

### Community 43 - "ExportLook"
Cohesion: 0.10
Nodes (17): QOpenGLFramebufferObject, One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, ExportLook, What the frames are to look like, as against what they are of. Laid over the…, Which of the things drawn over the model belong in the frames., ``base`` with this export's choices laid over it. (+9 more)

### Community 44 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 45 - "ExportVideoDialog"
Cohesion: 0.12
Nodes (12): QDialog, QProgressDialog, even(), ExportVideoDialog, Path, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+4 more)

### Community 46 - "VideoSettings"
Cohesion: 0.12
Nodes (10): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, Pump the event loop until ``done()`` or the clock runs out., run_until() (+2 more)

### Community 47 - "landmarks.py"
Cohesion: 0.11
Nodes (27): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), median_plane(), _mid(), mirror_point() (+19 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "._set_geometry"
Cohesion: 0.14
Nodes (5): Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Fill the shader's table with a level, if it is not already in it., Replace the annotation geometry; pass an empty list to hide it., Forget the contents without releasing the buffer objects.

### Community 50 - "plane_clusters.py"
Cohesion: 0.08
Nodes (37): How much surface each vertex stands for: a third of each triangle on it.…, vertex_weights(), _compact(), _consensus(), _cut(), _first_planes(), _fit(), flatness() (+29 more)

### Community 51 - "MeshBuffers"
Cohesion: 0.10
Nodes (9): MeshBuffers, Whichever geometry is standing for the model this frame., Vertex/index buffers for one mesh, bound through a single VAO., DataTexture, ndarray, An RGBA8 2D texture with clamped edges and mipmapped minification., A small RGBA32F table the shader reads exact values out of. Not a picture:…, Store an ``(h, w, 4)`` float array, reallocating only when resized. (+1 more)

### Community 52 - "PlacedLandmark"
Cohesion: 0.06
Nodes (32): Point3, PlacedLandmark, One anatomical point the artist put on the model during a guided run., The landmark list with one point moved, and no longer a guess. A landmark the…, The landmark list with these points taken back off the model. More than one at…, _humanoid_landmarks(), Landmark, mirror_landmarks() (+24 more)

### Community 53 - "ColorButton"
Cohesion: 0.06
Nodes (19): QFormLayout, QFrame, AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle., collapsible_group(), CollapsibleGroup, ColorButton (+11 more)

### Community 54 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 55 - "viewport.py"
Cohesion: 0.05
Nodes (49): auto_smooth(), A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, _empty(), PlaneAxes, PlaneSet, ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, One level of a fit: the planes the shader is to quantise against. A plane is a… (+41 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (12): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. (+4 more)

### Community 57 - "_derived"
Cohesion: 0.10
Nodes (24): _kept_laying(), Fresh bones, laid the way the armature was already laying them. The bone list…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _derived(), A guess the artist corrects is theirs, and the mirror leaves it alone., The new list is the edit; the old one has to survive to be undone to., Hips, then the ribcage, then the head, then the limbs largest first. This order… (+16 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.16
Nodes (10): PlanesPanel, Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Show what this way of working needs, and put the rest away. A setting that does…, The line under the geometry slider: how the form is being worked. ``wires`` is…, Breaks the form into planes, in the shading or in the geometry itself., Re-read the armatures and what the chosen one is laying down. Called whenever…, What can be done to the list, given where the handle is and whether a film is… (+2 more)

### Community 59 - "Bounds"
Cohesion: 0.09
Nodes (22): Move the camera so ``bounds`` fills the view, keeping the direction., Point the camera along ``direction``, measured object-to-eye., Bounds, _gathered(), ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Which group each of ``total`` things lands in, given pairs that agree. Hooking… (+14 more)

### Community 60 - "clay_lumps"
Cohesion: 0.16
Nodes (18): _box_facings(), clay_lumps(), clay_pieces(), fit_piece(), _frame(), grow_piece(), join_pieces(), Which three ways a lump of material runs. Columns, thinnest first. Thinnest… (+10 more)

### Community 61 - "Path"
Cohesion: 0.23
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 62 - ".update_enabled"
Cohesion: 0.20
Nodes (5): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., Highlight the row for a node picked in the view., Highlight the row for a landmark picked in the view.

### Community 63 - "_shifts"
Cohesion: 0.25
Nodes (8): _balloon(), close_gaps(), outside_points(), Fill the slots the lumps leave between them, without taking clay away. The…, Grow or shrink a solid by ``reach`` cells, one axis at a time. A separable…, Where the model stops: the corners just outside ``room``. ``(n, 3)``. Only the…, The pair of slices that read a lattice ``span`` cells over along ``axis``., _shifts()

### Community 64 - "MatcapPanel"
Cohesion: 0.24
Nodes (5): QIcon, MatcapPanel, Rebuild the thumbnail list from the resources folder., Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…

### Community 65 - "overlay.py"
Cohesion: 0.08
Nodes (18): MeasurementSettings, How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., MeasureTool, Handle, ndarray, Two-click measuring, plus dragging the endpoints of an unlocked measurement., Consume a picked point; returns a measurement on the second click. (+10 more)

### Community 66 - "open_writer"
Cohesion: 0.13
Nodes (16): ffmpeg_path(), open_writer(), Path, Where ffmpeg is, or ``None``. Looked for in the order of how deliberate each…, Why ``format`` cannot be written here, or ``None`` if it can., Start an encoder for ``settings``, or say why there cannot be one., unavailable(), frames() (+8 more)

### Community 67 - "plane_volume.py"
Cohesion: 0.18
Nodes (15): _axes(), encloses(), lattice(), lay_bed(), nearest_surface(), _passes(), Blocking a form in out of its own planes, from the outside or from a core. A…, Read the model onto a lattice, ready for solids to be laid on it. (+7 more)

### Community 68 - "PlaneMode"
Cohesion: 0.17
Nodes (8): fit_planes(), The planes of ``mesh`` under ``mode``; empty where the mode needs none., PlaneMode, str, How the plane directions are arrived at. ``shader_id`` must stay in sync with…, Whether the directions are read off the model rather than imposed., Whether the mode reads the design matrix, and so its coefficients. Grid reads…, The model's own planes under ``mode``, fitted once and kept.

### Community 69 - "stone_field"
Cohesion: 0.20
Nodes (10): Bed, block_bounds(), coarse_bounds(), point_support(), The lattice a form is worked on, and the model read onto it. Everything here…, The union of the blocks a labelling cuts the model into, and its facings. Stone…, The index range each block covers. ``(count, 3)`` lows and highs, inclusive. A…, Those ranges, read on the fine lattice the coarse one stands for. (+2 more)

### Community 70 - "ReplaceItems"
Cohesion: 0.10
Nodes (7): Any, Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems, Remove the selected node, or the whole armature when its row is picked., The armature the selected row stands for, when the row is not a node.

### Community 71 - "test_plane_solids.py"
Cohesion: 0.05
Nodes (78): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), block(), dumbbell(), edge_use(), flatness() (+70 more)

### Community 72 - "load_matcap_pixels"
Cohesion: 0.18
Nodes (19): Color, Charcoal matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels(), Path (+11 more)

### Community 73 - "raycast_mesh"
Cohesion: 0.07
Nodes (36): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., intersects_bounds(), ndarray, Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``., raycast_mesh() (+28 more)

### Community 74 - "StrokeBuffers"
Cohesion: 0.16
Nodes (12): build_segment_vertices(), build_vertices(), _expand(), ndarray, Geometry for the surface annotations and the cross-section contour. Strokes are…, A single vertex buffer holding every visible stroke., Replace the buffer contents with a prepared vertex block., Expand strokes into the triangle soup the stroke shader expects. Every segment… (+4 more)

### Community 75 - "ArmatureStore"
Cohesion: 0.18
Nodes (4): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 76 - "application.py"
Cohesion: 0.16
Nodes (14): ArgumentParser, Namespace, QApplication, _apply_startup_arguments(), build_parser(), main(), Command-line entry point and application bootstrap., Open whatever the command line asked for, falling back to sane defaults. (+6 more)

### Community 77 - "carve"
Cohesion: 0.32
Nodes (8): carve(), _corner_facings(), facings(), fitted_facings(), The form ``directions`` leave of the model, worked one way or the other.…, Twenty-six directions round a cube, for judging how much air a block holds.…, The supporting directions a block may be cut along. ``(m, 3)``. The twenty-six…, The form's own facings alone, both ways round and without duplicates. What a…

### Community 78 - "ArmaturePanel"
Cohesion: 0.10
Nodes (11): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Take back the landmark before this one and ask for it again., Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors., The multiplier the position boxes are read and written through., Show the landmark group only once there are landmarks to show. (+3 more)

### Community 79 - "VideoError"
Cohesion: 0.18
Nodes (12): _encode_arguments(), _encoders(), _FFmpegWriter, _no_window(), RuntimeError, An export that could not be written, said in words for the artist., Which encoders this ffmpeg was built with. Asked once, because a build without…, Keep a console window from flashing up on Windows for each ffmpeg call. (+4 more)

### Community 80 - "armature_panel.py"
Cohesion: 0.24
Nodes (8): BoneLabels, Buried, Enum, str, A graph of named points under the form, and the wire it stands for. An armature…, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…, The armature: its nodes, the guided presets, and how the wire is drawn.

### Community 81 - "ArmatureTool"
Cohesion: 0.05
Nodes (51): BoneRef, LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, _project(), Handle, The landmarks still to place, in order, the current one first. (+43 more)

### Community 82 - "PlaneSettings"
Cohesion: 0.06
Nodes (39): PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor…, How much of a turn in the surface one plane covers, in degrees. Linear in…, The grid step, in cube-face coordinates, that gives that span. A cell of this…, The design-matrix settings, in the form the fitters want them., How many planes a mode fitted to the model keeps. The climb from two planes to…, Roughly how much of a turn one of those planes covers, in degrees., The plane size of whichever mode is running. (+31 more)

### Community 83 - "._selected"
Cohesion: 0.22
Nodes (4): Write a structural change, detaching the armature from its preset., Run a bone between the row selected now and the node held before it., The node the selected row stands for, if the row is a node at all., Follow the highlighted row, without rebuilding the list underneath it. Going…

### Community 84 - "Command"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 85 - "box"
Cohesion: 0.50
Nodes (4): box(), A unit cube, shaded flat: six planes and twelve right angles., Every edge of a cube is a right angle, and no reading of AutoSmooth short of…, test_autosmooth_leaves_a_real_plane_change_hard()

### Community 86 - "paths.py"
Cohesion: 0.32
Nodes (11): Terracotta clay matcap, available_matcaps(), _bundled_root(), image_path(), matcap_dir(), model_dir(), Path, Locations of the bundled resources. ``REFVIEW_RESOURCES`` overrides the search,… (+3 more)

### Community 87 - "._picker"
Cohesion: 0.16
Nodes (6): Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Rub out the stroke points under the eraser, live., Apply the drag live, so the artist sees the wire bend as they pull it.

### Community 88 - "._build"
Cohesion: 0.27
Nodes (6): QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 89 - "annotation.py"
Cohesion: 0.20
Nodes (7): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a…, Painting annotations onto the model surface. Every shape is laid down the same…

### Community 90 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 91 - "_create_splash"
Cohesion: 0.22
Nodes (10): QPixmap, QSplashScreen, _create_splash(), _fitted_title_font(), QFont, Largest title font that still draws the whole app name inside ``width``., lock_icon(), Small painted icons. Drawing the padlock rather than shipping an image file… (+2 more)

### Community 92 - ".mousePressEvent"
Cohesion: 0.18
Nodes (5): ndarray, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…

### Community 93 - "ShadingMode"
Cohesion: 0.18
Nodes (4): Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode, TestEven

### Community 94 - "block_splits"
Cohesion: 0.17
Nodes (12): block_labels(), block_splits(), blocks(), _cuts(), _hull_air(), The corners a hull round ``points`` holds that ``points`` do not fill. The hull…, Where a block might be cut in two: a direction, and a point to pass through.…, The greedy split, with every count along the way kept. The same walk… (+4 more)

### Community 95 - "record"
Cohesion: 0.20
Nodes (11): Work the form stage by stage, handing each one back as it is finished. A…, record(), ndarray, The mesh's normals, made unit, with anything unusable recomputed., Points spread over the model closely enough for a lattice to feel it. The…, surface_seeds(), unit_normals(), A film nobody is waiting for any more is abandoned rather than finished.… (+3 more)

### Community 96 - "._chosen_armature"
Cohesion: 0.24
Nodes (6): QListWidgetItem, The armature the clay is being built on, or ``None``. An index past the end of…, The bones of the chosen armature, in the order the clay goes down. Every intact…, Take lengths of wire out of the clay, or put them back. A tick on a row that…, Put the clay on all of the wire, or take it off all of it., Write which lengths of wire take clay, as one undoable step.

### Community 97 - "test_annotation.py"
Cohesion: 0.31
Nodes (9): line_stroke(), Surface annotations: erasing, splitting and the geometry handed to GL., A stroke running along +X, one unit apart, with +Y normals., test_a_closed_stroke_gains_the_wrapping_segment(), test_each_segment_becomes_six_vertices(), test_erasing_keeps_the_brush_and_drops_stubs(), test_erasing_nothing_reports_no_change(), test_erasing_the_middle_splits_a_stroke_in_two() (+1 more)

### Community 98 - "_Encoder"
Cohesion: 0.25
Nodes (5): Queue, _Encoder, QObject, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 99 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 100 - ".refresh_list"
Cohesion: 0.40
Nodes (3): QTreeWidgetItem, Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing.

### Community 101 - "coarse_lattice"
Cohesion: 0.33
Nodes (6): app(), coarse_lattice(), fixture, MonkeyPatch, One Qt application for the whole run; offscreen, so CI needs no display.…, Read every model on a small lattice, so the suite stays quick.

### Community 102 - "CHANGELOG.md"
Cohesion: 0.25
Nodes (7): Cross-section tool (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding

### Community 103 - "wakelock.py"
Cohesion: 0.22
Nodes (7): _Backend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The backend for this machine, or a do-nothing one if it cannot be had., A way of asking one platform to stay awake., Ask for sleep to be held off., Withdraw the request.

### Community 104 - "._commit_node_drag"
Cohesion: 0.16
Nodes (5): Record the finished drag as one step, or read a press as a selection., Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…, Record the finished drag as a single undo step., Record the finished gesture: a move, a resize, or a plain click. A press that…

### Community 105 - "._upload_sculpt"
Cohesion: 0.22
Nodes (4): The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on.

### Community 106 - "._draw_hud"
Cohesion: 0.31
Nodes (4): QFont, Burn a line into the bottom of a frame, for an exported clip. Which stage of…, Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, What the armature tool is waiting for, said in as few lines as it takes.

### Community 107 - "._place_armature_node"
Cohesion: 0.22
Nodes (4): The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 109 - "_ScreenSaverBackend"
Cohesion: 0.22
Nodes (4): The freedesktop screensaver service, which hands back a cookie., Hold sleep off, or stop holding it, whichever is not already true., Drop the request, if one is out. Safe to call more than once., _ScreenSaverBackend

### Community 110 - "_WindowsBackend"
Cohesion: 0.25
Nodes (5): ``SetThreadExecutionState``: a flag on this thread, not a handle. The flags…, _WindowsBackend, skipif, The flag the viewer sets is the one Windows reports back afterwards., test_windows_really_sets_the_execution_state()

### Community 111 - "union_field"
Cohesion: 0.25
Nodes (8): block_field(), piece_bounds(), One row of coordinates per axis over ``box``, shaped so they broadcast., The union of the blocks, as a field whose zero is its surface. Each block is…, The box a lump of clay lives in, read off the six facings of its frame. Those…, The union of a set of convex solids, as a field whose zero is its surface. The…, _rows(), union_field()

### Community 112 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 114 - "_MacBackend"
Cohesion: 0.33
Nodes (3): c_void_p, _MacBackend, An IOKit power assertion, held by id until it is released.

### Community 117 - "FakeViewport"
Cohesion: 0.28
Nodes (3): FakeViewport, QImage, A viewport that renders nothing, at whatever size it is asked for.

### Community 118 - ".split"
Cohesion: 0.29
Nodes (5): ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., Normals padded to match the points, so callers can zip them freely., Break the stroke into the runs of points ``keep`` marks as surviving., _runs()

### Community 119 - "kept_off"
Cohesion: 0.50
Nodes (4): kept_off(), Which points lie in the sleeve a length of wire declares round itself. The wire…, Which material lies under a length of wire that is to take no clay. Turning a…, within_sleeve()

### Community 120 - "_wire_frame"
Cohesion: 0.50
Nodes (4): _perpendicular(), Two unit directions across ``along``, neither of them near it., Which three ways a lump laid along a wire runs. Columns, thinnest first. The…, _wire_frame()

### Community 121 - "test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else"
Cohesion: 0.33
Nodes (5): lattice_fineness(), How much finer than usual a detail setting asks the lattice to be. One at the…, How much finer than usual the geometry's lattice is worked on., The slider's own end already asks for every plane a fit will give, so what a…, test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else()

### Community 122 - "._accumulate_ghost"
Cohesion: 0.33
Nodes (5): bind_default(), current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., Restore a framebuffer captured with :func:`current_framebuffer`., Sum a see-through model into the ghost buffers, to be resolved after. Blending…

### Community 123 - "rounded"
Cohesion: 0.40
Nodes (5): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick., rounded()

### Community 125 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 126 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 129 - "test_relaxing_settles_the_clay_and_leaves_the_stone_alone"
Cohesion: 0.50
Nodes (4): How far each point sits from the middle of its neighbours, as a share of the…, The relax is a pass over the finished surface rather than anything the volume…, roughness(), test_relaxing_settles_the_clay_and_leaves_the_stone_alone()

### Community 130 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `FilmRecorder`, `test_relaxing_settles_the_clay_and_leaves_the_stone_alone`, `plane_axes`, `ViewerState`, `_wires`, `mesh_renderer.py`, `main_window.py`, `SectionSettings`, `SectionPanel`, `test_plane_clusters.py`, `ndarray`, `load_obj`, `ExportLook`, `VideoSettings`, `._set_geometry`, `plane_clusters.py`, `OrientationSettings`, `viewport.py`, `FilmExport`, `Bounds`, `plane_volume.py`, `PlaneMode`, `stone_field`, `test_plane_solids.py`, `raycast_mesh`, `carve`, `PlaneSettings`, `box`, `ShadingMode`, `record`, `FakeViewport`, `rounded`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera` to `test_camera.py`, `overlay.py`, `NavigationController`, `SceneRenderer`, `._draw_hud`, `mesh_renderer.py`, `Mesh`, `README.md`, `main_window.py`, `ArmatureTool`, `ViewportOverlay`, `BookmarkStore`, `._accumulate_ghost`, `Bounds`, `.pan`, `test_session.py`, `Session`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `FilmRecorder`, `._buried_nodes`, `AnnotateTool`, `MainWindow`, `ViewerState`, `Measurement`, `main_window.py`, `ViewportOverlay`, `NavigationController`, `film_export.py`, `ExportLook`, `ExportVideoDialog`, `viewport.py`, `FilmExport`, `overlay.py`, `ArmatureTool`, `._picker`, `.mousePressEvent`, `_Encoder`, `._commit_node_drag`, `._upload_sculpt`, `._place_armature_node`, `._sync_scene`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Armature` (e.g. with `SculptCache` and `Session`) actually correct?**
  _`Armature` has 2 INFERRED edges - model-reasoned connections that need verification._