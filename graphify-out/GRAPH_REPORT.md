# Graph Report - reference-viewer  (2026-09-06)

## Corpus Check
- 75 files · ~208,853 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1387 nodes · 3001 edges · 66 communities (62 shown, 4 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 145 edges (avg confidence: 0.64)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `260daa36`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Stroke
- application.py
- Release
- Viewport Widget
- annotation.py
- AnnotateTool
- MainWindow
- ViewportOverlay
- Mesh
- Bounds
- RenderSettings
- render/__init__.py
- camera.py
- OrientationSettings
- Camera
- README.md
- gltf_loader.py
- main_window.py
- GeometryTarget
- CameraPanel
- TriangleIndex
- ShaderProgram
- Measurement
- SceneRenderer
- MeasurePanel
- BookmarkStore
- Navigation and Angle Snapping
- History
- MeshUnits
- core/__init__.py
- MeasureTool
- ShadingPanel
- obj_loader.py
- test_camera.py
- SliderSpin
- WakeLock
- state.py
- ViewerState
- update_check.py
- SectionSettings
- SectionPanel
- Snapped Orbit Tests
- session.py
- Session
- UpdateChecker
- wakelock.py
- test_spatial.py
- _ScreenSaverBackend
- Agent Graph-First Instructions
- _WindowsBackend
- Panel
- Screen-to-World Panning
- mesh_renderer.py
- ReplaceItems
- _MacBackend
- Path
- settings.py
- matcap_panel.py
- orientation.py
- Projection
- PlaneSettings
- ModelPanel
- refview/__init__.py
- .plane_point
- .new_stroke
- shading_panel.py

## God Nodes (most connected - your core abstractions)
1. `Camera` - 71 edges
2. `Mesh` - 57 edges
3. `Viewport` - 47 edges
4. `MainWindow` - 46 edges
5. `ViewerState` - 46 edges
6. `SceneRenderer` - 37 edges
7. `Stroke` - 33 edges
8. `Measurement` - 30 edges
9. `Panel` - 29 edges
10. `AnnotateTool` - 27 edges

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

## Communities (66 total, 4 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.06
Nodes (36): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+28 more)

### Community 1 - "application.py"
Cohesion: 0.05
Nodes (54): ArgumentParser, Color, Namespace, QApplication, QPixmap, QSplashScreen, Charcoal matcap, Terracotta clay matcap (+46 more)

### Community 2 - "Release"
Cohesion: 0.18
Nodes (12): The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, is_skipped(), QWidget, Background release check and the notice it puts in front of the artist. The…, Whether the artist already dismissed this exact version., Offer the release page, with the option never to be asked again. (+4 more)

### Community 3 - "Viewport Widget"
Cohesion: 0.07
Nodes (15): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current., Drop whatever gesture is half-finished, without disarming the tool., Record the finished drag as a single undo step., Rub out the stroke points under the eraser, live. (+7 more)

### Community 4 - "annotation.py"
Cohesion: 0.21
Nodes (7): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, What the annotate tool does with a drag. The first three describe the shape a…, Painting annotations onto the model surface. Every shape is laid down the same…, Surface annotation tool: brush, shape and eraser settings.

### Community 5 - "AnnotateTool"
Cohesion: 0.10
Nodes (18): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses., Continue the open run with a hit, or end it where the ray missed. (+10 more)

### Community 6 - "MainWindow"
Cohesion: 0.08
Nodes (11): QAction, QMainWindow, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits., Keep the menu entry agreeing with the panel's own checkbox. (+3 more)

### Community 7 - "ViewportOverlay"
Cohesion: 0.22
Nodes (14): QColor, QPainter, QPointF, project_visible(), QFont, A square grip, so an editable end reads differently from a fixed one., Preview the gesture under way; finished strokes are drawn in 3D., The cursor ring: the eraser's reach, or the width of the brush. (+6 more)

### Community 8 - "Mesh"
Cohesion: 0.10
Nodes (27): Mesh, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.… (+19 more)

### Community 9 - "Bounds"
Cohesion: 0.16
Nodes (15): Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray, A turntable-style disc the model can stand on. A ground plane gives the eye… (+7 more)

### Community 10 - "RenderSettings"
Cohesion: 0.11
Nodes (21): Everything the viewport needs in order to draw a frame., RenderSettings, current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., light_directions(), normal_matrix(), ndarray, Replace the section contour, prepared by the caller as stroke vertices. (+13 more)

### Community 11 - "render/__init__.py"
Cohesion: 0.14
Nodes (10): OpenGL rendering layer: shader programs, textures and the scene renderer., default_matcap_pixels(), MatcapLoadError, ndarray, RuntimeError, Matcap texture loading and upload., Raised when an image cannot be used as a matcap., A neutral studio matcap, used before the user picks one. (+2 more)

### Community 12 - "camera.py"
Cohesion: 0.17
Nodes (18): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-…, Return ``v`` scaled to unit length, or ``fallback`` for a zero vector. (+10 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 14 - "Camera"
Cohesion: 0.09
Nodes (14): Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling… (+6 more)

### Community 15 - "README.md"
Cohesion: 0.10
Nodes (22): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, refview (+14 more)

### Community 16 - "gltf_loader.py"
Cohesion: 0.14
Nodes (24): _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry(), _primitives(), ndarray (+16 more)

### Community 17 - "main_window.py"
Cohesion: 0.16
Nodes (11): The handful of undoable edits the whole application is built from.…, Delete the item at ``index``, putting it back in place on undo., RemoveItem, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, Qt user interface: the viewport widget, the panels and the main window., Application window: viewport, docked panels, menus and shortcuts., Projection settings, standard views and named camera bookmarks., Measurement list and display options. (+3 more)

### Community 18 - "GeometryTarget"
Cohesion: 0.09
Nodes (13): ColorTarget, DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the…, Fail loudly on an unusable attachment rather than rendering nothing. An…, Shared lifetime handling for a framebuffer with one attachment. The GL objects… (+5 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "TriangleIndex"
Cohesion: 0.15
Nodes (13): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., Build the index from expanded triangle corners, shape ``(T, 3, 3)``. (+5 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "Measurement"
Cohesion: 0.12
Nodes (10): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+2 more)

### Community 23 - "SceneRenderer"
Cohesion: 0.15
Nodes (7): MeshBuffers, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the ground disc; pass ``None`` to hide it., Replace the annotation geometry; pass an empty list to hide it., Vertex/index buffers for one mesh, bound through a single VAO., Forget the contents without releasing the buffer objects., SceneRenderer

### Community 24 - "MeasurePanel"
Cohesion: 0.08
Nodes (15): QIcon, QTreeWidgetItem, Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, lock_icon(), Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if… (+7 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.09
Nodes (12): BookmarkStore, CameraBookmark, Named camera positions the artist can jump between while sculpting., A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one. (+4 more)

### Community 26 - "Navigation and Angle Snapping"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "History"
Cohesion: 0.09
Nodes (20): Camera motion is deliberately not undoable, AddItem, Append an item to a document list., Command, History, One reversible change, named for the undo menu., A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive… (+12 more)

### Community 28 - "MeshUnits"
Cohesion: 0.20
Nodes (5): MeshUnits, ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, The real-world unit a file declared its coordinates in. Only some formats say:…

### Community 29 - "core/__init__.py"
Cohesion: 0.14
Nodes (22): core never imports Qt, Qt-free geometry, camera and document model for the reference viewer., compute_vertex_normals(), One entry point for every mesh format the viewer reads. Callers ask for a path…, MeshLoadError, RuntimeError, Triangle-mesh containers shared by the loader, the renderer and picking., Raised when a file cannot be interpreted as a triangle mesh. (+14 more)

### Community 30 - "MeasureTool"
Cohesion: 0.12
Nodes (10): Handle, MeasureTool, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., Where a click at ``(x, y)`` would put a point. With free placement the point… (+2 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.24
Nodes (6): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., ShadingPanel

### Community 32 - "obj_loader.py"
Cohesion: 0.07
Nodes (45): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast() (+37 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (8): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_serialisation_round_trip(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "SliderSpin"
Cohesion: 0.12
Nodes (13): QFormLayout, QGroupBox, QPushButton, A draggable split: thumbnails above, adjustments below. The gallery is the one…, Cross-section controls: the cutting plane, what it keeps and how it reads., ColorButton, form_group(), QWidget (+5 more)

### Community 35 - "WakeLock"
Cohesion: 0.17
Nodes (13): Holds sleep off while the window that owns it is the one in front. The class…, WakeLock, Broken, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do., A platform that refuses, the way an old or locked-down one might., The viewer must open and close normally on a machine that says no., Recorder (+5 more)

### Community 36 - "state.py"
Cohesion: 0.22
Nodes (8): MeasurementSettings, Named point-to-point measurements and their presentation options., How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., Two-click measuring, plus dragging the endpoints of an unlocked measurement., 2D overlay drawn on top of the GL scene with QPainter. Measurements are…, The observable document shared by the viewport and the side panels. Panels…, test_length_formatting_uses_the_display_unit()

### Community 37 - "ViewerState"
Cohesion: 0.09
Nodes (15): ndarray, Path, QObject, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements and…, Rotate the measurements and annotations onto the turned model. A point sits at…, Take the display unit from the file when the format declares one. Only glTF… (+7 more)

### Community 38 - "update_check.py"
Cohesion: 0.14
Nodes (22): check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed). (+14 more)

### Community 39 - "SectionSettings"
Cohesion: 0.08
Nodes (29): Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, The direction the section plane faces. (+21 more)

### Community 40 - "SectionPanel"
Cohesion: 0.12
Nodes (14): Cross-section tool (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, STL and glTF import (1.1.0) (+6 more)

### Community 41 - "Snapped Orbit Tests"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 42 - "session.py"
Cohesion: 0.27
Nodes (9): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Persisted viewer state: camera, shading, measurements and bookmarks. (+1 more)

### Community 43 - "Session"
Cohesion: 0.14
Nodes (15): Path, A snapshot of everything worth keeping between runs., Session file that sits beside a model, e.g. ``bust.refview.json``., Session, sidecar_path(), Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., Version 1 files predate the annotation layer and the endpoint lock. (+7 more)

### Community 44 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 45 - "wakelock.py"
Cohesion: 0.22
Nodes (7): _Backend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The backend for this machine, or a do-nothing one if it cannot be had., A way of asking one platform to stay awake., Ask for sleep to be held off., Withdraw the request.

### Community 46 - "test_spatial.py"
Cohesion: 0.29
Nodes (9): _grid(), The picking accelerator: it must be fast without changing any answer., A bumpy height field, so rays hit different triangles at different depths., The pruned candidate set must never miss the true intersection., test_a_ray_that_misses_the_model_is_pruned_away(), test_an_empty_index_returns_no_candidates(), test_every_triangle_lands_in_exactly_one_leaf(), test_the_index_finds_the_triangle_a_ray_actually_hits() (+1 more)

### Community 47 - "_ScreenSaverBackend"
Cohesion: 0.22
Nodes (4): The freedesktop screensaver service, which hands back a cookie., Hold sleep off, or stop holding it, whichever is not already true., Drop the request, if one is out. Safe to call more than once., _ScreenSaverBackend

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "_WindowsBackend"
Cohesion: 0.25
Nodes (5): skipif, ``SetThreadExecutionState``: a flag on this thread, not a handle. The flags…, _WindowsBackend, The flag the viewer sets is the one Windows reports back afterwards., test_windows_really_sets_the_execution_state()

### Community 50 - "Panel"
Cohesion: 0.16
Nodes (8): QStyledItemDelegate, Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block., _NameOnlyDelegate, Allows in-place editing of the name column only.

### Community 52 - "mesh_renderer.py"
Cohesion: 0.29
Nodes (7): bind_default(), Restore a framebuffer captured with :func:`current_framebuffer`., key_world_direction(), light_view_projection(), OpenGL scene renderer: background, shaded mesh, wireframe, section and paint.…, The key light's direction in world space, pointing surface -> light., An orthographic camera at the key light, framing the whole scene. The extent is…

### Community 53 - "ReplaceItems"
Cohesion: 0.14
Nodes (6): Swap the whole contents of a document list. Used for bulk edits -- clearing the…, ReplaceItems, AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle., test_replace_items_covers_bulk_edits()

### Community 54 - "_MacBackend"
Cohesion: 0.33
Nodes (3): c_void_p, _MacBackend, An IOKit power assertion, held by id until it is released.

### Community 55 - "Path"
Cohesion: 0.29
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 56 - "settings.py"
Cohesion: 0.09
Nodes (19): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, LightSettings, MatcapSettings, NavigationSettings, Enum, str (+11 more)

### Community 57 - "matcap_panel.py"
Cohesion: 0.25
Nodes (6): QScrollArea, Matcap selection and colour grading., What was imported and which way up it should stand., Small reusable controls shared by the side panels., Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, scrollable()

### Community 58 - "orientation.py"
Cohesion: 0.33
Nodes (5): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis

### Community 59 - "Projection"
Cohesion: 0.33
Nodes (4): Projection, Enum, str, Projection used by :class:`Camera`.

### Community 60 - "PlaneSettings"
Cohesion: 0.33
Nodes (4): PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor…, How much of a turn in the surface one plane covers, in degrees. Linear in…, The grid step, in cube-face coordinates, that gives that span. A cell of this…

### Community 62 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 68 - "shading_panel.py"
Cohesion: 0.21
Nodes (6): Shared plumbing for the dockable side panels., Dockable control panels., PlanesPanel, Everything that acts on the shading normals rather than on the shading. Faceted…, Breaks the surface normals down into the planes of the form., Shading mode, lighting, surface material and scene furniture controls.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Camera` connect `Camera` to `test_camera.py`, `state.py`, `ViewerState`, `ViewportOverlay`, `Mesh`, `Bounds`, `RenderSettings`, `Snapped Orbit Tests`, `camera.py`, `Session`, `README.md`, `Screen-to-World Panning`, `mesh_renderer.py`, `BookmarkStore`, `Navigation and Angle Snapping`, `core/__init__.py`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `Mesh` connect `Mesh` to `obj_loader.py`, `state.py`, `ViewerState`, `SectionSettings`, `Bounds`, `OrientationSettings`, `test_spatial.py`, `gltf_loader.py`, `TriangleIndex`, `mesh_renderer.py`, `SceneRenderer`, `MeshUnits`, `core/__init__.py`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `application.py`, `Release`, `Viewport Widget`, `ViewerState`, `UpdateChecker`, `main_window.py`, `Path`, `History`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `MainWindow` (e.g. with `ViewerState` and `UpdateChecker`) actually correct?**
  _`MainWindow` has 3 INFERRED edges - model-reasoned connections that need verification._