# Graph Report - reference-viewer  (2026-09-11)

## Corpus Check
- 91 files · ~282,775 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2407 nodes · 5375 edges · 110 communities (100 shown, 10 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 208 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `073d0ad9`
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
- TriangleIndex
- Measurement
- RenderSettings
- StrokeBuffers
- mesh_renderer.py
- OrientationSettings
- Armature
- README.md
- gltf_loader.py
- ColorButton
- GeometryTarget
- CameraPanel
- test_plane_film.py
- ShaderProgram
- ViewportOverlay
- PlanesPanel
- MeasurePanel
- BookmarkStore
- NavigationController
- SectionSettings
- SectionPanel
- test_session.py
- Session
- ShadingPanel
- main_window.py
- test_camera.py
- test_plane_clusters.py
- WakeLock
- surface_of
- History
- update_check.py
- Mesh
- test_mesh_io.py
- Camera
- test_armature.py
- MeasureTool
- UpdateChecker
- PlacedLandmark
- compute_vertex_normals
- landmarks.py
- Agent Graph-First Instructions
- SceneRenderer
- settings.py
- Texture2D
- union_field
- wakelock.py
- render/__init__.py
- plane_film.py
- test_navigation.py
- ._draw_hud
- plane_count
- core/__init__.py
- clay_lumps
- Path
- Projection
- plane_volume.py
- MatcapPanel
- viewport.py
- ._commit_node_drag
- ndarray
- stl_loader.py
- stone_field
- ReplaceItems
- test_plane_solids.py
- application.py
- block
- _back_inside
- ArmatureStore
- AnnotatePanel
- carve
- ArmaturePanel
- dual_contour
- _ScreenSaverBackend
- ArmatureTool
- PlaneSettings
- _WindowsBackend
- annotation.py
- box
- ._start_update_check
- .mouseMoveEvent
- ._build
- coarse_lattice
- welded
- test_a_block_holds_every_point_it_was_measured_from
- .mousePressEvent
- SculptCache
- block_splits
- ._sync_scene
- test_a_hull_is_cut_from_every_side
- test_the_fill_leaves_a_flat_alone_and_closes_a_slot
- _MacBackend
- test_the_fill_never_takes_clay_away
- test_how_far_the_fill_reaches_says_how_wide_a_slot_it_closes
- test_a_lump_lies_in_the_box_it_says_it_does
- test_the_lumps_are_joined_as_a_volume_and_not_as_surfaces
- _derived
- ._refresh_cursor
- ._upload_sculpt
- .pan
- ._picker
- refview/__init__.py
- .new_armature

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 117 edges
2. `Camera` - 72 edges
3. `Viewport` - 70 edges
4. `PlaneSettings` - 63 edges
5. `Armature` - 60 edges
6. `ArmaturePanel` - 60 edges
7. `ViewerState` - 51 edges
8. `MainWindow` - 48 edges
9. `SceneRenderer` - 43 edges
10. `ArmatureTool` - 41 edges

## Surprising Connections (you probably didn't know these)
- `Orthographic extent derived from FOV and distance` --rationale_for--> `Camera`  [EXTRACTED]
  README.md → src/refview/core/camera.py
- `Pedestal (1.1.0)` --rationale_for--> `PedestalSettings`  [EXTRACTED]
  CHANGELOG.md → src/refview/core/pedestal.py
- `REFVIEW_RESOURCES resource override` --rationale_for--> `available_matcaps()`  [EXTRACTED]
  README.md → src/refview/paths.py
- `The cut interior is flooded flat` --rationale_for--> `SceneRenderer`  [INFERRED]
  README.md → src/refview/render/mesh_renderer.py
- `Every document edit is a command` --rationale_for--> `SetAttributes`  [EXTRACTED]
  README.md → src/refview/core/commands.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The bundled matcap set** — resources_matcaps_clay_terracotta_matcap, resources_matcaps_charcoal_matcap, resources_matcaps_jade_matcap, resources_matcaps_steel_matcap, resources_matcaps_studio_white_matcap, resources_matcaps_wax_skin_matcap, tools_generate_matcaps_matcappreset, tools_generate_matcaps_render [INFERRED 0.85]
- **The four generic undo commands** — src_refview_core_commands_setattributes, src_refview_core_commands_additem, src_refview_core_commands_removeitem, src_refview_core_commands_replaceitems, src_refview_core_history_command, readme_every_edit_is_a_command [EXTRACTED 1.00]
- **Windows binary-compatibility decisions** — readme_pyside6_pinned_below_68, environment_pip_installed_binaries, environment_python_311, github_workflows_release_pyinstaller_build [INFERRED 0.75]

## Communities (110 total, 10 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.08
Nodes (25): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+17 more)

### Community 1 - "FilmRecorder"
Cohesion: 0.08
Nodes (22): QThread, Film, The stage at ``index``, clamped to what has actually been recorded., A stage as it is to be drawn, with its normals read at ``smooth``. Kept out of…, One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., A whole making, from the coarsest stage to the one the slider asks for. Held by…, shaded() (+14 more)

### Community 2 - "Release"
Cohesion: 0.18
Nodes (15): check_for_update(), fetch_latest_release(), RuntimeError, The release could not be looked up (offline, rate limited, malformed)., The newest published release, as GitHub describes it., Return the newest published release, or raise :class:`UpdateCheckError`., The newest release when it is later than ``current_version``, else ``None``., Release (+7 more)

### Community 3 - "Viewport"
Cohesion: 0.11
Nodes (9): QOpenGLWidget, End any film being recorded, and wait for its thread to really stop. For…, Free every GL object while the owning context is still current., Arm one tool, disarming the rest. Only one gesture can own the left button, so…, Drop whatever gesture is half-finished, without disarming the tool., Renders the scene and turns mouse gestures into camera and tool actions., Slide the view so a point sits at the centre, keeping the angle., Slide the view so a measurement sits at the centre, keeping the angle. (+1 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - "AnnotateTool"
Cohesion: 0.11
Nodes (14): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses., Continue the open run with a hit, or end it where the ray missed. (+6 more)

### Community 6 - "MainWindow"
Cohesion: 0.08
Nodes (11): QAction, QMainWindow, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits., Keep the menu entry agreeing with the panel's own checkbox. (+3 more)

### Community 7 - "ViewerState"
Cohesion: 0.10
Nodes (14): ndarray, Path, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements, annotations…, Rotate the measurements, annotations and armature onto the turned model. A… (+6 more)

### Community 8 - "TriangleIndex"
Cohesion: 0.08
Nodes (28): Cross-section tool (1.1.0), Model orientation (1.1.0), Picking about a hundred times faster, Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, Morton-curve leaf boxes for picking (+20 more)

### Community 9 - "Measurement"
Cohesion: 0.10
Nodes (12): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+4 more)

### Community 10 - "RenderSettings"
Cohesion: 0.11
Nodes (20): Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, light_directions(), normal_matrix(), ndarray, Draw one frame, then hand a neutral GL state back to the caller.…, Draw the model, see-through when it is being ghosted. Depth writes go off for a… (+12 more)

### Community 11 - "StrokeBuffers"
Cohesion: 0.16
Nodes (12): build_segment_vertices(), build_vertices(), _expand(), ndarray, Geometry for the surface annotations and the cross-section contour. Strokes are…, A single vertex buffer holding every visible stroke., Replace the buffer contents with a prepared vertex block., Expand strokes into the triangle soup the stroke shader expects. Every segment… (+4 more)

### Community 12 - "mesh_renderer.py"
Cohesion: 0.15
Nodes (23): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-…, Return ``v`` scaled to unit length, or ``fallback`` for a zero vector. (+15 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.09
Nodes (24): OrientationSettings, Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., UpAxis (+16 more)

### Community 14 - "Armature"
Cohesion: 0.07
Nodes (25): Armature, ArmatureNode, Bone, ndarray, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, Every node position as ``(n, 3)``., The two points a bone runs between, or ``None`` if it dangles. (+17 more)

### Community 15 - "README.md"
Cohesion: 0.09
Nodes (25): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, refview (+17 more)

### Community 16 - "gltf_loader.py"
Cohesion: 0.12
Nodes (28): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry() (+20 more)

### Community 17 - "ColorButton"
Cohesion: 0.08
Nodes (15): QFrame, CollapsibleGroup, ColorButton, PointEdit, QPushButton, QWidget, Re-scale the control, e.g. once a model's size is known., Three spin boxes for one point in space. Keyboard tracking is off, so a typed… (+7 more)

### Community 18 - "GeometryTarget"
Cohesion: 0.08
Nodes (17): bind_default(), ColorTarget, current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the… (+9 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "test_plane_film.py"
Cohesion: 0.10
Nodes (26): Which side of the surface the planes are worked from. The two ways of making a…, SculptMode, coarse_lattice(), film_of(), fixture, MonkeyPatch, parametrize, Scrubbing through the making of a form, rather than only arriving at it. The… (+18 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "ViewportOverlay"
Cohesion: 0.17
Nodes (18): QColor, QPainter, QPointF, project_visible(), Handle, A line laid over its own dark outline, so it reads against anything., An unfilled circle: how thick the form is here, not how big a dot is., A square grip, so an editable end reads differently from a fixed one. (+10 more)

### Community 23 - "PlanesPanel"
Cohesion: 0.17
Nodes (9): PlanesPanel, The line under the normals slider: what the setting has asked for., Breaks the form into planes, in the shading or in the geometry itself., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Show what this way of working needs, and put the rest away. A setting that does… (+1 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.09
Nodes (15): lock_icon(), Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if…, _render(), MeasurePanel, _NameOnlyDelegate, QStyledItemDelegate, QTreeWidgetItem (+7 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.12
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Deletion goes through the undo stack, so the store only tracks position., test_bookmarks_cycle_and_wrap() (+1 more)

### Community 26 - "NavigationController"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "SectionSettings"
Cohesion: 0.12
Nodes (22): ndarray, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn. (+14 more)

### Community 28 - "SectionPanel"
Cohesion: 0.11
Nodes (13): Enum, str, The direction the section plane faces., Unit axis, or ``None`` for a custom direction., Which side of the plane survives the cut., SectionAxis, SectionMode, Turn the cut on or off, for the menu and the keyboard shortcut. (+5 more)

### Community 29 - "test_session.py"
Cohesion: 0.12
Nodes (14): Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., A step of the slider is worth a fixed share more planes, not a fixed number of…, The ceiling went from 64 planes to 256 without moving the slider under anyone:…, The panel edits the settings; the fit has to be told what they are., Both modes answer in degrees of turn, so the panel can just ask., test_length_formatting_uses_the_display_unit(), test_plane_detail_moves_the_plane_size_evenly() (+6 more)

### Community 30 - "Session"
Cohesion: 0.15
Nodes (15): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Path (+7 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.22
Nodes (7): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel

### Community 32 - "main_window.py"
Cohesion: 0.08
Nodes (31): QFormLayout, QGroupBox, The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, Application window: viewport, docked panels, menus and shortcuts., Surface annotation tool: brush, shape and eraser settings., The armature: its nodes, the guided presets, and how the wire is drawn., Panel (+23 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (8): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_serialisation_round_trip(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (58): angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What… (+50 more)

### Community 35 - "WakeLock"
Cohesion: 0.17
Nodes (13): Holds sleep off while the window that owns it is the one in front. The class…, WakeLock, Broken, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do., A platform that refuses, the way an old or locked-down one might., The viewer must open and close normally on a machine that says no., Recorder (+5 more)

### Community 36 - "surface_of"
Cohesion: 0.20
Nodes (11): Bed, The gradient of a lattice field, by central differences. Which is the direction…, Drop the loose pieces, keeping the form and anything of its size. A block is a…, Settle the surface into itself, without letting it out of the model. What a…, The lattice a form is worked on, and the model read onto it. Everything here…, Which way the model's own surface faces, at every corner., Hold a field of solids against the model and read its surface out. The second…, relax_surface() (+3 more)

### Community 37 - "History"
Cohesion: 0.09
Nodes (20): Camera motion is deliberately not undoable, AddItem, Append an item to a document list., Command, History, One reversible change, named for the undo menu., A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive… (+12 more)

### Community 38 - "update_check.py"
Cohesion: 0.19
Nodes (15): is_newer(), _padded(), parse_version(), Ask GitHub whether a newer release exists. The check is deliberately small and…, Numeric components of ``text``, or ``None`` when it is not a version. A pre-…, Whether ``candidate`` is a strictly later version than ``current``., Pull the tag and page link out of a GitHub release document., release_from_payload() (+7 more)

### Community 39 - "Mesh"
Cohesion: 0.08
Nodes (31): auto_smooth(), _gathered(), Mesh, Triangle-mesh containers shared by the loader, the renderer and picking., Return a copy whose bounding-box centre sits at the origin., Which group each of ``total`` things lands in, given pairs that agree. Hooking…, A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, An indexed triangle mesh with per-vertex positions and normals. The viewer… (+23 more)

### Community 40 - "test_mesh_io.py"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

### Community 41 - "Camera"
Cohesion: 0.08
Nodes (16): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target). (+8 more)

### Community 42 - "test_armature.py"
Cohesion: 0.09
Nodes (48): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _chain(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., The femoral head is inside the bump you can feel, not on it., A wire in two halves is not an armature anybody could bend. (+40 more)

### Community 43 - "MeasureTool"
Cohesion: 0.12
Nodes (10): MeasureTool, Handle, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., Where a click at ``(x, y)`` would put a point. With free placement the point… (+2 more)

### Community 44 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 45 - "PlacedLandmark"
Cohesion: 0.06
Nodes (28): Point3, PlacedLandmark, One anatomical point the artist put on the model during a guided run., The landmark list with one point moved, and no longer a guess. A landmark the…, The landmark list with these points taken back off the model. More than one at…, _humanoid_landmarks(), Landmark, mirror_landmarks() (+20 more)

### Community 46 - "compute_vertex_normals"
Cohesion: 0.09
Nodes (34): compute_vertex_normals(), One entry point for every mesh format the viewer reads. Callers ask for a path…, MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., Area-weighted smooth vertex normals for an indexed triangle soup., _assemble(), _face_corners() (+26 more)

### Community 47 - "landmarks.py"
Cohesion: 0.11
Nodes (27): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), median_plane(), _mid(), mirror_point() (+19 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "SceneRenderer"
Cohesion: 0.09
Nodes (13): MeshBuffers, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Whichever geometry is standing for the model this frame., Fill the shader's table with a level, if it is not already in it., Replace the annotation geometry; pass an empty list to hide it., Replace the section contour, prepared by the caller as stroke vertices. (+5 more)

### Community 50 - "settings.py"
Cohesion: 0.04
Nodes (74): Coefficients, _empty(), PlaneAxes, PlaneSet, ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, One level of a fit: the planes the shader is to quantise against. A plane is a…, A level with no place in it: nearest direction wins, as before. (+66 more)

### Community 51 - "Texture2D"
Cohesion: 0.14
Nodes (6): DataTexture, ndarray, An RGBA8 2D texture with clamped edges and mipmapped minification., A small RGBA32F table the shader reads exact values out of. Not a picture:…, Store an ``(h, w, 4)`` float array, reallocating only when resized., Texture2D

### Community 52 - "union_field"
Cohesion: 0.25
Nodes (8): block_field(), piece_bounds(), One row of coordinates per axis over ``box``, shaped so they broadcast., The union of the blocks, as a field whose zero is its surface. Each block is…, The box a lump of clay lives in, read off the six facings of its frame. Those…, The union of a set of convex solids, as a field whose zero is its surface. The…, _rows(), union_field()

### Community 53 - "wakelock.py"
Cohesion: 0.22
Nodes (7): _Backend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The backend for this machine, or a do-nothing one if it cannot be had., A way of asking one platform to stay awake., Ask for sleep to be held off., Withdraw the request.

### Community 54 - "render/__init__.py"
Cohesion: 0.33
Nodes (5): OpenGL rendering layer: shader programs, textures and the scene renderer., MatcapLoadError, RuntimeError, Matcap texture loading and upload, and the small data table beside it., Raised when an image cannot be used as a matcap.

### Community 55 - "plane_film.py"
Cohesion: 0.08
Nodes (33): planes_for(), The stages a form passes through on its way from a block to a figure. The…, How many solids each stage of a film is made of. Every count from the coarsest…, The detail setting that asks for ``solids``, or ``None`` if none does. The…, Work the form stage by stage, handing each one back as it is finished. A…, record(), stage_counts(), block_count() (+25 more)

### Community 56 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 57 - "._draw_hud"
Cohesion: 0.38
Nodes (3): QFont, Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, What the armature tool is waiting for, said in as few lines as it takes.

### Community 58 - "plane_count"
Cohesion: 0.12
Nodes (12): _along(), lattice_fineness(), plane_count(), Where a detail setting sits on its slider, 0 to 1., How much finer than usual a detail setting asks the lattice to be. One at the…, How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., How much of a turn in the surface one plane covers, in degrees. Linear in…, How many planes a mode fitted to the model keeps. The climb from two planes to… (+4 more)

### Community 59 - "core/__init__.py"
Cohesion: 0.06
Nodes (32): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, Qt-free geometry, camera and document model for the reference viewer., Bounds, ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations… (+24 more)

### Community 60 - "clay_lumps"
Cohesion: 0.16
Nodes (16): _box_facings(), clay_lumps(), clay_pieces(), fit_piece(), _frame(), grow_piece(), join_pieces(), Which three ways a lump of material runs. Columns, thinnest first. Thinnest… (+8 more)

### Community 61 - "Path"
Cohesion: 0.29
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 62 - "Projection"
Cohesion: 0.33
Nodes (4): Projection, Enum, str, Projection used by :class:`Camera`.

### Community 63 - "plane_volume.py"
Cohesion: 0.19
Nodes (13): _balloon(), close_gaps(), outside_points(), _passes(), Blocking a form in out of its own planes, from the outside or from a core. A…, Fill the slots the lumps leave between them, without taking clay away. The…, Grow or shrink a solid by ``reach`` cells, one axis at a time. A separable…, Where the model stops: the corners just outside ``room``. ``(n, 3)``. Only the… (+5 more)

### Community 64 - "MatcapPanel"
Cohesion: 0.18
Nodes (8): QIcon, QScrollArea, MatcapPanel, Rebuild the thumbnail list from the resources folder., Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, scrollable()

### Community 65 - "viewport.py"
Cohesion: 0.09
Nodes (23): BoneLabels, Buried, Enum, str, A graph of named points under the form, and the wire it stands for. An armature…, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…, Named camera positions the artist can jump between while sculpting. (+15 more)

### Community 66 - "._commit_node_drag"
Cohesion: 0.33
Nodes (3): Record the finished gesture: a move, a resize, or a plain click. A press that…, Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…

### Community 67 - "ndarray"
Cohesion: 0.23
Nodes (13): _axes(), encloses(), lattice(), lay_bed(), nearest_surface(), ndarray, Read the model onto a lattice, ready for solids to be laid on it., A cubic lattice covering the model with ``margin`` of room around it. Cubic… (+5 more)

### Community 68 - "stl_loader.py"
Cohesion: 0.20
Nodes (14): STL corner welding, _ascii_corners(), _binary_corners(), load_stl(), ndarray, Path, Binary and ASCII STL reader. STL stores three loose corners per facet and…, Raised when a file cannot be interpreted as an STL mesh. (+6 more)

### Community 69 - "stone_field"
Cohesion: 0.25
Nodes (8): block_bounds(), coarse_bounds(), point_support(), The union of the blocks a labelling cuts the model into, and its facings. Stone…, The index range each block covers. ``(count, 3)`` lows and highs, inclusive. A…, Those ranges, read on the fine lattice the coarse one stands for., The same, read off the model's own surface rather than off the lattice. Which…, stone_field()

### Community 70 - "ReplaceItems"
Cohesion: 0.14
Nodes (5): Any, Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems

### Community 71 - "test_plane_solids.py"
Cohesion: 0.07
Nodes (64): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), ball(), dumbbell(), edge_use(), flatness() (+56 more)

### Community 72 - "application.py"
Cohesion: 0.07
Nodes (50): ArgumentParser, Color, Namespace, QApplication, QPixmap, QSplashScreen, Charcoal matcap, Terracotta clay matcap (+42 more)

### Community 73 - "block"
Cohesion: 0.33
Nodes (6): block(), A closed box with hard edges, each face cut into a grid of triangles., Counting crossings is exact on a closed surface and meaningless on anything…, A box is six triangles the size of the whole thing; the lattice has to feel it…, test_an_open_model_is_read_some_other_way(), test_the_samples_cover_a_surface_however_it_was_tessellated()

### Community 74 - "_back_inside"
Cohesion: 0.50
Nodes (4): _back_inside(), Read lattice fields at places between their corners, straight-line. Nearest-…, Put anything that has drifted out of the model back onto its surface. One…, _read_at()

### Community 75 - "ArmatureStore"
Cohesion: 0.18
Nodes (4): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 76 - "AnnotatePanel"
Cohesion: 0.27
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 77 - "carve"
Cohesion: 0.24
Nodes (10): carve(), _corner_facings(), facings(), fitted_facings(), _flat_mesh(), A mesh that shades every facet flat and every crease as an edge. A vertex on a…, The form ``directions`` leave of the model, worked one way or the other.…, Twenty-six directions round a cube, for judging how much air a block holds.… (+2 more)

### Community 78 - "ArmaturePanel"
Cohesion: 0.05
Nodes (31): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, ArmaturePanel, QTreeWidgetItem, Run a row's edit once Qt has finished delivering the current signal. Committing…, Arms the armature tool, lists its nodes and runs the guided presets., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle. (+23 more)

### Community 79 - "dual_contour"
Cohesion: 0.50
Nodes (4): dual_contour(), How far to move, along the directions the planes actually pin down., The surface where ``value`` changes sign, one vertex per lattice cell. Each…, _truncated_solve()

### Community 80 - "_ScreenSaverBackend"
Cohesion: 0.22
Nodes (4): The freedesktop screensaver service, which hands back a cookie., Hold sleep off, or stop holding it, whichever is not already true., Drop the request, if one is out. Safe to call more than once., _ScreenSaverBackend

### Community 81 - "ArmatureTool"
Cohesion: 0.06
Nodes (30): BoneRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, GuideRun, _project(), Handle, Begin a preset run against an armature already in the store. (+22 more)

### Community 82 - "PlaneSettings"
Cohesion: 0.07
Nodes (35): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor…, The grid step, in cube-face coordinates, that gives that span. A cell of this…, The design-matrix settings, in the form the fitters want them., Roughly how much of a turn one of those planes covers, in degrees., The plane size of whichever mode is running. (+27 more)

### Community 83 - "_WindowsBackend"
Cohesion: 0.25
Nodes (5): skipif, ``SetThreadExecutionState``: a flag on this thread, not a handle. The flags…, _WindowsBackend, The flag the viewer sets is the one Windows reports back afterwards., test_windows_really_sets_the_execution_state()

### Community 84 - "annotation.py"
Cohesion: 0.20
Nodes (7): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a…, Painting annotations onto the model surface. Every shape is laid down the same…

### Community 85 - "box"
Cohesion: 0.50
Nodes (4): box(), A unit cube, shaded flat: six planes and twelve right angles., Every edge of a cube is a right angle, and no reading of AutoSmooth short of…, test_autosmooth_leaves_a_real_plane_change_hard()

### Community 86 - "._start_update_check"
Cohesion: 0.29
Nodes (4): Ask GitHub for the newest release in the background. The startup check is…, QWidget, show_failure_dialog(), show_up_to_date_dialog()

### Community 87 - ".mouseMoveEvent"
Cohesion: 0.22
Nodes (3): Rub out the stroke points under the eraser, live., Apply the drag live, so the artist sees the wire bend as they pull it., Orbit increment while Shift is held, or 0 for a free orbit.

### Community 88 - "._build"
Cohesion: 0.19
Nodes (9): _NameOnlyDelegate, QPushButton, QStyledItemDelegate, QWidget, Allows in-place editing of the name column only., Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit. (+1 more)

### Community 89 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 90 - "welded"
Cohesion: 0.67
Nodes (3): ndarray, Which point each vertex really is, once copies of a position are one point., welded()

### Community 92 - ".mousePressEvent"
Cohesion: 0.20
Nodes (4): ndarray, Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…, Object centre, which anchors the plane the orbit pivot lies on.

### Community 93 - "SculptCache"
Cohesion: 0.25
Nodes (7): Holds the working state between one turn of the sliders and the next.…, The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache, AutoSmooth reads the normals of a form that has already been built, so it must…, test_reshading_the_form_does_not_rebuild_it(), test_the_cache_stands_aside_unless_the_geometry_target_asked_for_it()

### Community 94 - "block_splits"
Cohesion: 0.20
Nodes (10): block_labels(), block_splits(), blocks(), _cuts(), _hull_air(), The corners a hull round ``points`` holds that ``points`` do not fill. The hull…, Where a block might be cut in two: a direction, and a point to pass through.…, The greedy split, with every count along the way kept. The same walk… (+2 more)

### Community 98 - "_MacBackend"
Cohesion: 0.33
Nodes (3): c_void_p, _MacBackend, An IOKit power assertion, held by id until it is released.

### Community 103 - "_derived"
Cohesion: 0.18
Nodes (13): The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _derived(), A guess the artist corrects is theirs, and the mirror leaves it alone., The new list is the edit; the old one has to survive to be undone to., Mirroring moves a guess in place, which must not reach the undo history., test_a_locked_node_keeps_the_size_it_was_given(), test_deriving_never_writes_through_the_landmarks_it_is_handed() (+5 more)

### Community 104 - "._refresh_cursor"
Cohesion: 0.33
Nodes (3): Record the finished drag as a single undo step., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed.

### Community 105 - "._upload_sculpt"
Cohesion: 0.33
Nodes (3): Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on.

### Community 107 - "._picker"
Cohesion: 0.18
Nodes (4): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…, The nodes the model is standing in front of, worked out at most once. A node is…

### Community 112 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `FilmRecorder`, `plane_axes`, `ViewerState`, `TriangleIndex`, `mesh_renderer.py`, `OrientationSettings`, `gltf_loader.py`, `SectionSettings`, `SectionPanel`, `test_plane_clusters.py`, `surface_of`, `test_mesh_io.py`, `compute_vertex_normals`, `SceneRenderer`, `settings.py`, `plane_film.py`, `core/__init__.py`, `plane_volume.py`, `viewport.py`, `stl_loader.py`, `test_plane_solids.py`, `block`, `carve`, `PlaneSettings`, `box`, `welded`, `SculptCache`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `main_window.py`, `viewport.py`, `FilmRecorder`, `._commit_node_drag`, `AnnotateTool`, `MainWindow`, `ViewerState`, `._refresh_cursor`, `._upload_sculpt`, `MeasureTool`, `._picker`, `ArmatureTool`, `ViewportOverlay`, `.mouseMoveEvent`, `NavigationController`, `.mousePressEvent`, `._sync_scene`?**
  _High betweenness centrality (0.072) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera` to `viewport.py`, `test_camera.py`, `Mesh`, `Measurement`, `.pan`, `RenderSettings`, `mesh_renderer.py`, `README.md`, `ViewportOverlay`, `test_navigation.py`, `BookmarkStore`, `NavigationController`, `core/__init__.py`, `Session`, `._draw_hud`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `PlaneSettings` (e.g. with `Film` and `Stage`) actually correct?**
  _`PlaneSettings` has 6 INFERRED edges - model-reasoned connections that need verification._