# Graph Report - reference-viewer  (2026-09-03)

## Corpus Check
- 69 files · ~203,482 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1251 nodes · 2748 edges · 53 communities (49 shown, 4 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 140 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `91c6d22a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Annotation Store and Eraser
- Startup and Bundled Matcaps
- Measure Tool and Handles
- Viewport Widget
- Annotate Tool and Brush
- Viewer State and Model Loading
- Main Window, Menus and Drops
- Matcap Panel and Painted Icons
- Raycasting and Surface Picking
- Mesh and Bounds
- Render Settings and Frame Draw
- Panel Layout Construction
- Projection and Linear Algebra
- Model Orientation
- Camera Gestures
- Build, Packaging and Architecture Rules
- glTF Loader
- Bookmarks and Section Enums
- Offscreen Render Targets
- Section Planes and Contours
- Shading Modes and Materials
- Shader Programs
- Measurement Store
- Scene Renderer and GL Buffers
- Camera Panel and Bookmark List
- Camera Bookmark Store
- Navigation and Angle Snapping
- Undo History Stack
- Release Notes and Picking Index
- Mesh IO and STL Loader
- Undo Commands and Panel Plumbing
- Matcap Textures and UI Wiring
- OBJ Loader and Normals
- Camera Tests
- Panel Base Class
- Mesh Format Tests
- Cross-section Panel
- Removal Command and Session Tests
- OBJ Parsing Tests
- Command Protocol
- Session Snapshot and Units
- Snapped Orbit Tests
- Annotation Model and Modes
- SetAttributes Command
- Dataclass JSON Serialization
- Morton Curve Spatial Index
- Annotate Panel
- GL Texture Wrapper
- Agent Graph-First Instructions
- AddItem Command
- Frustum Fitting
- Screen-to-World Panning
- Package Entry Point

## God Nodes (most connected - your core abstractions)
1. `Camera` - 71 edges
2. `Mesh` - 57 edges
3. `Viewport` - 47 edges
4. `ViewerState` - 46 edges
5. `MainWindow` - 38 edges
6. `SceneRenderer` - 37 edges
7. `Stroke` - 33 edges
8. `Measurement` - 29 edges
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

## Communities (53 total, 4 thin omitted)

### Community 0 - "Annotation Store and Eraser"
Cohesion: 0.06
Nodes (36): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+28 more)

### Community 1 - "Startup and Bundled Matcaps"
Cohesion: 0.07
Nodes (45): ArgumentParser, Color, Namespace, QApplication, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap (+37 more)

### Community 2 - "Measure Tool and Handles"
Cohesion: 0.20
Nodes (16): QColor, QFont, QPainter, QPointF, QSplashScreen, _create_splash(), project_visible(), A square grip, so an editable end reads differently from a fixed one. (+8 more)

### Community 3 - "Viewport Widget"
Cohesion: 0.07
Nodes (15): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current., Drop whatever gesture is half-finished, without disarming the tool., Record the finished drag as a single undo step., Rub out the stroke points under the eraser, live. (+7 more)

### Community 4 - "Annotate Tool and Brush"
Cohesion: 0.10
Nodes (18): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+10 more)

### Community 5 - "Viewer State and Model Loading"
Cohesion: 0.06
Nodes (31): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Path (+23 more)

### Community 6 - "Main Window, Menus and Drops"
Cohesion: 0.06
Nodes (18): QAction, QMainWindow, MainWindow, Path, Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits., Apply a matcap image, reporting unreadable files to the user. (+10 more)

### Community 7 - "Matcap Panel and Painted Icons"
Cohesion: 0.08
Nodes (16): QIcon, QPixmap, QTreeWidgetItem, lock_icon(), Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if…, _render(), MatcapPanel (+8 more)

### Community 8 - "Raycasting and Surface Picking"
Cohesion: 0.06
Nodes (45): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.… (+37 more)

### Community 9 - "Mesh and Bounds"
Cohesion: 0.10
Nodes (30): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, Qt-free geometry, camera and document model for the reference viewer., Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal() (+22 more)

### Community 10 - "Render Settings and Frame Draw"
Cohesion: 0.12
Nodes (21): Everything the viewport needs in order to draw a frame., RenderSettings, light_directions(), normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.… (+13 more)

### Community 11 - "Panel Layout Construction"
Cohesion: 0.11
Nodes (15): QFormLayout, QGroupBox, QPushButton, A draggable split: thumbnails above, adjustments below. The gallery is the one…, Cross-section controls: the cutting plane, what it keeps and how it reads., Shading mode, lighting, surface material and scene furniture controls., ColorButton, form_group() (+7 more)

### Community 12 - "Projection and Linear Algebra"
Cohesion: 0.13
Nodes (24): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-…, Return ``v`` scaled to unit length, or ``fallback`` for a zero vector. (+16 more)

### Community 13 - "Model Orientation"
Cohesion: 0.10
Nodes (23): OrientationSettings, Enum, str, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., UpAxis, ModelPanel (+15 more)

### Community 14 - "Camera Gestures"
Cohesion: 0.15
Nodes (9): Camera, ndarray, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling…, A look-at camera with orbit / pan / zoom behaviour. The orthographic extent is…, Vertical half-extent of the frustum at the focal plane. (+1 more)

### Community 15 - "Build, Packaging and Architecture Rules"
Cohesion: 0.10
Nodes (23): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, refview (+15 more)

### Community 16 - "glTF Loader"
Cohesion: 0.13
Nodes (26): _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry(), _primitives(), ndarray (+18 more)

### Community 17 - "Bookmarks and Section Enums"
Cohesion: 0.12
Nodes (10): Handle, MeasureTool, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., Where a click at ``(x, y)`` would put a point. With free placement the point… (+2 more)

### Community 18 - "Offscreen Render Targets"
Cohesion: 0.08
Nodes (17): bind_default(), ColorTarget, current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the… (+9 more)

### Community 19 - "Section Planes and Contours"
Cohesion: 0.08
Nodes (29): Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, The direction the section plane faces. (+21 more)

### Community 20 - "Shading Modes and Materials"
Cohesion: 0.24
Nodes (6): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., ShadingPanel

### Community 21 - "Shader Programs"
Cohesion: 0.13
Nodes (8): ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "Measurement Store"
Cohesion: 0.18
Nodes (4): MeasurementStore, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., An ordered, named collection of measurements. Deliberately plain: the Qt layer…

### Community 23 - "Scene Renderer and GL Buffers"
Cohesion: 0.09
Nodes (10): MeshBuffers, Replace the ground disc; pass ``None`` to hide it., Replace the annotation geometry; pass an empty list to hide it., Vertex/index buffers for one mesh, bound through a single VAO., Forget the contents without releasing the buffer objects., default_matcap_pixels(), ndarray, A neutral studio matcap, used before the user picks one. (+2 more)

### Community 24 - "Camera Panel and Bookmark List"
Cohesion: 0.13
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 25 - "Camera Bookmark Store"
Cohesion: 0.13
Nodes (7): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., test_bookmarks_cycle_and_wrap()

### Community 26 - "Navigation and Angle Snapping"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "Undo History Stack"
Cohesion: 0.20
Nodes (13): AddItem, Append an item to a document list., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch(), test_commands_carry_their_channel_and_name() (+5 more)

### Community 28 - "Release Notes and Picking Index"
Cohesion: 0.12
Nodes (9): Mesh, MeshUnits, ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Return a copy whose bounding-box centre sits at the origin., The real-world unit a file declared its coordinates in. Only some formats say:…, An indexed triangle mesh with per-vertex positions and normals. The viewer… (+1 more)

### Community 29 - "Mesh IO and STL Loader"
Cohesion: 0.12
Nodes (22): Cross-section tool (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, STL and glTF import (1.1.0) (+14 more)

### Community 30 - "Undo Commands and Panel Plumbing"
Cohesion: 0.17
Nodes (7): QStyledItemDelegate, Swap the whole contents of a document list. Used for bulk edits -- clearing the…, ReplaceItems, _NameOnlyDelegate, Measurement list and display options., Allows in-place editing of the name column only., test_replace_items_covers_bulk_edits()

### Community 31 - "Matcap Textures and UI Wiring"
Cohesion: 0.20
Nodes (9): QScrollArea, OpenGL rendering layer: shader programs, textures and the scene renderer., MatcapLoadError, RuntimeError, Matcap texture loading and upload., Raised when an image cannot be used as a matcap., Matcap selection and colour grading., Wrap a panel so it scrolls when it is taller than the dock. The controls keep… (+1 more)

### Community 32 - "OBJ Loader and Normals"
Cohesion: 0.11
Nodes (30): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic(), load_obj(), ObjLoadError (+22 more)

### Community 33 - "Camera Tests"
Cohesion: 0.12
Nodes (7): parametrize, camera(), fixture, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "Panel Base Class"
Cohesion: 0.14
Nodes (9): Panel, QWidget, Shared plumbing for the dockable side panels., A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block., Projection settings, standard views and named camera bookmarks., Dockable control panels. (+1 more)

### Community 35 - "Mesh Format Tests"
Cohesion: 0.15
Nodes (19): load_mesh(), Path, One entry point for every mesh format the viewer reads. Callers ask for a path…, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., MeshLoadError, RuntimeError, Triangle-mesh containers shared by the loader, the renderer and picking., Raised when a file cannot be interpreted as a triangle mesh. (+11 more)

### Community 36 - "Cross-section Panel"
Cohesion: 0.17
Nodes (5): Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Move the camera so ``bounds`` fills the view, keeping the direction., Point the camera along ``direction``, measured object-to-eye., Adopt the pose of ``other`` without replacing this instance.

### Community 37 - "Removal Command and Session Tests"
Cohesion: 0.33
Nodes (4): Delete the item at ``index``, putting it back in place on undo., RemoveItem, Deletion goes through the undo stack, so the store only tracks position., test_deleting_a_bookmark_moves_the_cycling_position()

### Community 38 - "OBJ Parsing Tests"
Cohesion: 0.20
Nodes (4): QObject, History, A bounded undo/redo stack., test_undo_and_redo_on_an_empty_stack_are_safe()

### Community 39 - "Command Protocol"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 41 - "Snapped Orbit Tests"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 42 - "Annotation Model and Modes"
Cohesion: 0.08
Nodes (30): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, What the annotate tool does with a drag. The first three describe the shape a…, Named camera positions the artist can jump between while sculpting., The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that… (+22 more)

### Community 43 - "SetAttributes Command"
Cohesion: 0.29
Nodes (3): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes

### Community 44 - "Dataclass JSON Serialization"
Cohesion: 0.20
Nodes (5): Enum, str, Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode

### Community 45 - "Morton Curve Spatial Index"
Cohesion: 0.29
Nodes (3): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., test_serialisation_round_trip()

### Community 46 - "Annotate Panel"
Cohesion: 0.24
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 47 - "GL Texture Wrapper"
Cohesion: 0.29
Nodes (4): ndarray, Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-…, Screen-to-world scale at a given depth along the view direction.

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "AddItem Command"
Cohesion: 0.33
Nodes (4): Projection, Enum, str, Projection used by :class:`Camera`.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Release Notes and Picking Index` to `OBJ Loader and Normals`, `Mesh Format Tests`, `Viewer State and Model Loading`, `Raycasting and Surface Picking`, `Mesh and Bounds`, `Annotation Model and Modes`, `Projection and Linear Algebra`, `Model Orientation`, `glTF Loader`, `Section Planes and Contours`, `Scene Renderer and GL Buffers`, `Mesh IO and STL Loader`?**
  _High betweenness centrality (0.124) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera Gestures` to `Camera Tests`, `Measure Tool and Handles`, `Cross-section Panel`, `Removal Command and Session Tests`, `OBJ Parsing Tests`, `Viewer State and Model Loading`, `Raycasting and Surface Picking`, `Mesh and Bounds`, `Annotation Model and Modes`, `Render Settings and Frame Draw`, `Projection and Linear Algebra`, `Morton Curve Spatial Index`, `Snapped Orbit Tests`, `Build, Packaging and Architecture Rules`, `Screen-to-World Panning`, `Camera Bookmark Store`, `Navigation and Angle Snapping`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `Viewer State and Model Loading` to `Measure Tool and Handles`, `Panel Base Class`, `Viewport Widget`, `Main Window, Menus and Drops`, `OBJ Parsing Tests`, `Annotation Model and Modes`, `Model Orientation`, `Build, Packaging and Architecture Rules`, `Bookmarks and Section Enums`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `ViewportOverlay`) actually correct?**
  _`ViewerState` has 3 INFERRED edges - model-reasoned connections that need verification._