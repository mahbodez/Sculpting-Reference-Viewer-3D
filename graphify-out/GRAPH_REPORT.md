# Graph Report - reference-viewer  (2026-09-03)

## Corpus Check
- 69 files · ~203,708 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1258 nodes · 2761 edges · 58 communities (54 shown, 4 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 139 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `05a8832e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Stroke
- application.py
- SectionPanel
- Viewport Widget
- AnnotateTool
- ViewportOverlay
- MainWindow
- MeasurePanel
- raycast_mesh
- Bounds
- Render Settings and Frame Draw
- main_window.py
- mesh_renderer.py
- OrientationSettings
- Camera
- README.md
- gltf_loader.py
- viewport.py
- Offscreen Render Targets
- SectionSettings
- ShadingPanel
- ShaderProgram
- Measurement
- Scene Renderer and GL Buffers
- CameraPanel
- BookmarkStore
- Navigation and Angle Snapping
- History
- Mesh
- core/__init__.py
- camera_panel.py
- Projection
- obj_loader.py
- test_camera.py
- Panel
- test_mesh_io.py
- Cross-section Panel
- ViewerState
- _primitive_geometry
- SectionAxis
- load_obj
- Snapped Orbit Tests
- .__init__
- Session
- environment.yml
- .from_dict
- AnnotatePanel
- release.yml
- Agent Graph-First Instructions
- CHANGELOG.md
- shaders.py
- Screen-to-World Panning
- MatcapPanel
- session.py
- settings.py
- SliderSpin
- orientation.py
- ModelPanel

## God Nodes (most connected - your core abstractions)
1. `Camera` - 71 edges
2. `Mesh` - 57 edges
3. `Viewport` - 47 edges
4. `ViewerState` - 46 edges
5. `MainWindow` - 38 edges
6. `SceneRenderer` - 37 edges
7. `Stroke` - 33 edges
8. `Measurement` - 30 edges
9. `AnnotateTool` - 27 edges
10. `Panel` - 27 edges

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

## Communities (58 total, 4 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.06
Nodes (37): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+29 more)

### Community 1 - "application.py"
Cohesion: 0.06
Nodes (54): ArgumentParser, Color, Namespace, QApplication, QSplashScreen, Charcoal matcap, Terracotta clay matcap, Jade matcap (+46 more)

### Community 2 - "SectionPanel"
Cohesion: 0.23
Nodes (5): Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 3 - "Viewport Widget"
Cohesion: 0.07
Nodes (15): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current., Drop whatever gesture is half-finished, without disarming the tool., Record the finished drag as a single undo step., Rub out the stroke points under the eraser, live. (+7 more)

### Community 4 - "AnnotateTool"
Cohesion: 0.06
Nodes (29): Handle, AnnotateMode, AnnotationSettings, Enum, str, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a… (+21 more)

### Community 5 - "ViewportOverlay"
Cohesion: 0.11
Nodes (22): QColor, QPainter, QPointF, MeasureTool, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed… (+14 more)

### Community 6 - "MainWindow"
Cohesion: 0.08
Nodes (13): QAction, QMainWindow, MainWindow, Path, Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits., Apply a matcap image, reporting unreadable files to the user. (+5 more)

### Community 7 - "MeasurePanel"
Cohesion: 0.10
Nodes (11): QTreeWidgetItem, Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, MeasurePanel, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed. (+3 more)

### Community 8 - "raycast_mesh"
Cohesion: 0.06
Nodes (45): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.… (+37 more)

### Community 9 - "Bounds"
Cohesion: 0.18
Nodes (15): Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray, A turntable-style disc the model can stand on. A ground plane gives the eye… (+7 more)

### Community 10 - "Render Settings and Frame Draw"
Cohesion: 0.12
Nodes (21): Everything the viewport needs in order to draw a frame., RenderSettings, light_directions(), normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.… (+13 more)

### Community 11 - "main_window.py"
Cohesion: 0.13
Nodes (15): QScrollArea, MatcapLoadError, RuntimeError, Matcap texture loading and upload., Raised when an image cannot be used as a matcap., Application window: viewport, docked panels, menus and shortcuts., Shared plumbing for the dockable side panels., Dockable control panels. (+7 more)

### Community 12 - "mesh_renderer.py"
Cohesion: 0.15
Nodes (23): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-…, Return ``v`` scaled to unit length, or ``fallback`` for a zero vector. (+15 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 14 - "Camera"
Cohesion: 0.15
Nodes (9): Camera, ndarray, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling…, A look-at camera with orbit / pan / zoom behaviour. The orthographic extent is…, Vertical half-extent of the frustum at the focal plane. (+1 more)

### Community 15 - "README.md"
Cohesion: 0.27
Nodes (10): Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets (+2 more)

### Community 16 - "gltf_loader.py"
Cohesion: 0.19
Nodes (17): STL and glTF import (1.1.0), Units are adopted, never guessed, _buffers(), GltfLoadError, load_gltf(), _primitives(), Path, glTF 2.0 reader for ``.glb`` and ``.gltf`` files. Only what a reference viewer… (+9 more)

### Community 17 - "viewport.py"
Cohesion: 0.17
Nodes (11): Freehand annotations painted onto the model surface. A stroke is a polyline of…, MeasurementSettings, Named point-to-point measurements and their presentation options., How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., Qt user interface: the viewport widget, the panels and the main window., Two-click measuring, plus dragging the endpoints of an unlocked measurement., 2D overlay drawn on top of the GL scene with QPainter. Measurements are… (+3 more)

### Community 18 - "Offscreen Render Targets"
Cohesion: 0.08
Nodes (17): bind_default(), ColorTarget, current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the… (+9 more)

### Community 19 - "SectionSettings"
Cohesion: 0.12
Nodes (22): ndarray, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn. (+14 more)

### Community 20 - "ShadingPanel"
Cohesion: 0.24
Nodes (6): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., ShadingPanel

### Community 21 - "ShaderProgram"
Cohesion: 0.12
Nodes (9): OpenGL rendering layer: shader programs, textures and the scene renderer., ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError (+1 more)

### Community 22 - "Measurement"
Cohesion: 0.12
Nodes (10): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+2 more)

### Community 23 - "Scene Renderer and GL Buffers"
Cohesion: 0.09
Nodes (10): MeshBuffers, Replace the ground disc; pass ``None`` to hide it., Replace the annotation geometry; pass an empty list to hide it., Vertex/index buffers for one mesh, bound through a single VAO., Forget the contents without releasing the buffer objects., default_matcap_pixels(), ndarray, A neutral studio matcap, used before the user picks one. (+2 more)

### Community 24 - "CameraPanel"
Cohesion: 0.13
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 25 - "BookmarkStore"
Cohesion: 0.12
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Deletion goes through the undo stack, so the store only tracks position., test_bookmarks_cycle_and_wrap() (+1 more)

### Community 26 - "Navigation and Angle Snapping"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "History"
Cohesion: 0.09
Nodes (20): Camera motion is deliberately not undoable, AddItem, Append an item to a document list., Command, History, One reversible change, named for the undo menu., A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive… (+12 more)

### Community 28 - "Mesh"
Cohesion: 0.13
Nodes (7): Mesh, ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, test_bounds_of_an_empty_point_set()

### Community 29 - "core/__init__.py"
Cohesion: 0.13
Nodes (23): Qt-free geometry, camera and document model for the reference viewer., compute_vertex_normals(), One entry point for every mesh format the viewer reads. Callers ask for a path…, MeshLoadError, RuntimeError, Triangle-mesh containers shared by the loader, the renderer and picking., Raised when a file cannot be interpreted as a triangle mesh., Area-weighted smooth vertex normals for an indexed triangle soup. (+15 more)

### Community 30 - "camera_panel.py"
Cohesion: 0.13
Nodes (9): The handful of undoable edits the whole application is built from.…, Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, Surface annotation tool: brush, shape and eraser settings., Projection settings, standard views and named camera bookmarks. (+1 more)

### Community 31 - "Projection"
Cohesion: 0.33
Nodes (4): Projection, Enum, str, Projection used by :class:`Camera`.

### Community 32 - "obj_loader.py"
Cohesion: 0.22
Nodes (14): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), ndarray, Minimal, dependency-free Wavefront OBJ reader. Only the geometry statements a…, Resolve ``v``, ``v/vt``, ``v//vn`` or ``v/vt/vn`` corners to 0-based pairs.… (+6 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (8): parametrize, camera(), fixture, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_serialisation_round_trip(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "Panel"
Cohesion: 0.16
Nodes (8): QStyledItemDelegate, Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block., _NameOnlyDelegate, Allows in-place editing of the name column only.

### Community 35 - "test_mesh_io.py"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

### Community 36 - "Cross-section Panel"
Cohesion: 0.17
Nodes (5): Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Move the camera so ``bounds`` fills the view, keeping the direction., Point the camera along ``direction``, measured object-to-eye., Adopt the pose of ``other`` without replacing this instance.

### Community 37 - "ViewerState"
Cohesion: 0.10
Nodes (15): QObject, ndarray, Path, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements and…, Rotate the measurements and annotations onto the turned model. A point sits at…, Take the display unit from the file when the format declares one. Only glTF… (+7 more)

### Community 38 - "_primitive_geometry"
Cohesion: 0.24
Nodes (11): _accessor(), _local_transform(), _primitive_geometry(), ndarray, _quaternion_matrix(), Read one accessor into an ``(n, components)`` array., A node's own transform, from either a matrix or a TRS triple., Rotation matrix for a glTF ``(x, y, z, w)`` quaternion. (+3 more)

### Community 39 - "SectionAxis"
Cohesion: 0.22
Nodes (7): Enum, str, The direction the section plane faces., Unit axis, or ``None`` for a custom direction., Which side of the plane survives the cut., SectionAxis, SectionMode

### Community 40 - "load_obj"
Cohesion: 0.27
Nodes (12): _load_generic(), load_obj(), Path, Line-by-line reader for files the fast path declines., Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, OBJ parsing: normals, triangulation and index handling., test_empty_file_is_rejected(), test_missing_normals_are_computed() (+4 more)

### Community 41 - "Snapped Orbit Tests"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 43 - "Session"
Cohesion: 0.14
Nodes (14): Named camera positions the artist can jump between while sculpting., Path, A snapshot of everything worth keeping between runs., Session file that sits beside a model, e.g. ``bust.refview.json``., Session, sidecar_path(), Session persistence, measurements and bookmarks., Version 1 files predate the annotation layer and the endpoint lock. (+6 more)

### Community 44 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 46 - "AnnotatePanel"
Cohesion: 0.28
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 47 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "CHANGELOG.md"
Cohesion: 0.25
Nodes (7): Cross-section tool (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding

### Community 50 - "shaders.py"
Cohesion: 0.50
Nodes (3): GLSL sources for the viewport. Six small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., _with_section()

### Community 52 - "MatcapPanel"
Cohesion: 0.16
Nodes (10): QIcon, QPixmap, lock_icon(), Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if…, _render(), MatcapPanel, Rebuild the thumbnail list from the resources folder. (+2 more)

### Community 55 - "session.py"
Cohesion: 0.27
Nodes (9): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Persisted viewer state: camera, shading, measurements and bookmarks. (+1 more)

### Community 56 - "settings.py"
Cohesion: 0.10
Nodes (17): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, LightSettings, MatcapSettings, Enum, str, QualitySettings (+9 more)

### Community 57 - "SliderSpin"
Cohesion: 0.13
Nodes (11): QFormLayout, QGroupBox, QPushButton, ColorButton, form_group(), QWidget, A swatch button that opens a colour picker. Colours are exchanged as 0-1 RGB…, A titled group box with a form layout, ready to be filled. (+3 more)

### Community 61 - "orientation.py"
Cohesion: 0.33
Nodes (5): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Camera` connect `Camera` to `test_camera.py`, `Cross-section Panel`, `ViewportOverlay`, `raycast_mesh`, `Bounds`, `Render Settings and Frame Draw`, `Session`, `mesh_renderer.py`, `.from_dict`, `.__init__`, `README.md`, `Snapped Orbit Tests`, `viewport.py`, `Screen-to-World Panning`, `BookmarkStore`, `Navigation and Angle Snapping`, `core/__init__.py`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `Mesh` connect `Mesh` to `obj_loader.py`, `test_mesh_io.py`, `ViewerState`, `SectionAxis`, `raycast_mesh`, `load_obj`, `Bounds`, `mesh_renderer.py`, `OrientationSettings`, `gltf_loader.py`, `viewport.py`, `SectionSettings`, `Scene Renderer and GL Buffers`, `core/__init__.py`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `Panel`, `Viewport Widget`, `ViewportOverlay`, `MainWindow`, `.__init__`, `main_window.py`, `OrientationSettings`, `README.md`, `viewport.py`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `ViewportOverlay`) actually correct?**
  _`ViewerState` has 3 INFERRED edges - model-reasoned connections that need verification._