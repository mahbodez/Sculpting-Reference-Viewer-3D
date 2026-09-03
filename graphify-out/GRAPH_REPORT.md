# Graph Report - .  (2026-09-03)

## Corpus Check
- 80 files · ~61,708 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1248 nodes · 2734 edges · 53 communities (49 shown, 4 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 136 edges (avg confidence: 0.64)
- Token cost: 41,000 input · 7,000 output

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
Nodes (37): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+29 more)

### Community 1 - "Startup and Bundled Matcaps"
Cohesion: 0.07
Nodes (43): ArgumentParser, Color, Namespace, QApplication, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap (+35 more)

### Community 2 - "Measure Tool and Handles"
Cohesion: 0.10
Nodes (24): Handle, QColor, QFont, QPainter, QPointF, MeasureTool, ndarray, Consume a picked point; returns a measurement on the second click. (+16 more)

### Community 3 - "Viewport Widget"
Cohesion: 0.08
Nodes (14): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current., Drop whatever gesture is half-finished, without disarming the tool., Record the finished drag as a single undo step., Rub out the stroke points under the eraser, live. (+6 more)

### Community 4 - "Annotate Tool and Brush"
Cohesion: 0.09
Nodes (22): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., Named point-to-point measurements and their presentation options., AnnotateTool, ndarray, Painting annotations onto the model surface. Every shape is laid down the same…, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved. (+14 more)

### Community 5 - "Viewer State and Model Loading"
Cohesion: 0.09
Nodes (18): QObject, Session file that sits beside a model, e.g. ``bust.refview.json``., sidecar_path(), ndarray, Path, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements and… (+10 more)

### Community 6 - "Main Window, Menus and Drops"
Cohesion: 0.08
Nodes (13): QAction, QMainWindow, MainWindow, Path, Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits., Apply a matcap image, reporting unreadable files to the user. (+5 more)

### Community 7 - "Matcap Panel and Painted Icons"
Cohesion: 0.08
Nodes (16): QIcon, QPixmap, QTreeWidgetItem, lock_icon(), Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if…, _render(), MatcapPanel (+8 more)

### Community 8 - "Raycasting and Surface Picking"
Cohesion: 0.07
Nodes (34): Hit, intersects_bounds(), ndarray, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``., raycast_mesh() (+26 more)

### Community 9 - "Mesh and Bounds"
Cohesion: 0.09
Nodes (22): Bounds, Mesh, ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Return a copy whose bounding-box centre sits at the origin., An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero). (+14 more)

### Community 10 - "Render Settings and Frame Draw"
Cohesion: 0.10
Nodes (23): Everything the viewport needs in order to draw a frame., RenderSettings, bind_default(), current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., Restore a framebuffer captured with :func:`current_framebuffer`., light_directions(), normal_matrix() (+15 more)

### Community 11 - "Panel Layout Construction"
Cohesion: 0.11
Nodes (15): QFormLayout, QGroupBox, QPushButton, A draggable split: thumbnails above, adjustments below. The gallery is the one…, Cross-section controls: the cutting plane, what it keeps and how it reads., Shading mode, lighting, surface material and scene furniture controls., ColorButton, form_group() (+7 more)

### Community 12 - "Projection and Linear Algebra"
Cohesion: 0.11
Nodes (27): Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., look_at(), normalize(), orthographic() (+19 more)

### Community 13 - "Model Orientation"
Cohesion: 0.09
Nodes (25): OrientationSettings, Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., UpAxis (+17 more)

### Community 14 - "Camera Gestures"
Cohesion: 0.11
Nodes (12): Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling… (+4 more)

### Community 15 - "Build, Packaging and Architecture Rules"
Cohesion: 0.09
Nodes (26): High Quality shading mode (1.1.0), numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix (+18 more)

### Community 16 - "glTF Loader"
Cohesion: 0.12
Nodes (28): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry() (+20 more)

### Community 17 - "Bookmarks and Section Enums"
Cohesion: 0.11
Nodes (21): Named camera positions the artist can jump between while sculpting., Qt-free geometry, camera and document model for the reference viewer., Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Which side of the plane survives the cut., SectionAxis (+13 more)

### Community 18 - "Offscreen Render Targets"
Cohesion: 0.09
Nodes (13): ColorTarget, DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the…, Fail loudly on an unusable attachment rather than rendering nothing. An…, Shared lifetime handling for a framebuffer with one attachment. The GL objects… (+5 more)

### Community 19 - "Section Planes and Contours"
Cohesion: 0.11
Nodes (22): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, Unit axis, or ``None`` for a custom direction., A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn. (+14 more)

### Community 20 - "Shading Modes and Materials"
Cohesion: 0.12
Nodes (11): Enum, str, Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode, Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings. (+3 more)

### Community 21 - "Shader Programs"
Cohesion: 0.12
Nodes (9): OpenGL rendering layer: shader programs, textures and the scene renderer., ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError (+1 more)

### Community 22 - "Measurement Store"
Cohesion: 0.11
Nodes (11): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+3 more)

### Community 23 - "Scene Renderer and GL Buffers"
Cohesion: 0.12
Nodes (9): MeshBuffers, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the ground disc; pass ``None`` to hide it., Replace the annotation geometry; pass an empty list to hide it., Vertex/index buffers for one mesh, bound through a single VAO., Forget the contents without releasing the buffer objects., SceneRenderer, default_matcap_pixels() (+1 more)

### Community 24 - "Camera Panel and Bookmark List"
Cohesion: 0.13
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 25 - "Camera Bookmark Store"
Cohesion: 0.11
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around. (+1 more)

### Community 26 - "Navigation and Angle Snapping"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "Undo History Stack"
Cohesion: 0.17
Nodes (15): History, A bounded undo/redo stack., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch(), test_commands_carry_their_channel_and_name() (+7 more)

### Community 28 - "Release Notes and Picking Index"
Cohesion: 0.12
Nodes (14): Cross-section tool (1.1.0), Model orientation (1.1.0), Picking about a hundred times faster, Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, Morton-curve leaf boxes for picking (+6 more)

### Community 29 - "Mesh IO and STL Loader"
Cohesion: 0.15
Nodes (18): STL corner welding, One entry point for every mesh format the viewer reads. Callers ask for a path…, MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., _ascii_corners(), _binary_corners(), load_stl() (+10 more)

### Community 30 - "Undo Commands and Panel Plumbing"
Cohesion: 0.15
Nodes (9): The handful of undoable edits the whole application is built from.…, Swap the whole contents of a document list. Used for bulk edits -- clearing the…, ReplaceItems, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, Surface annotation tool: brush, shape and eraser settings., Shared plumbing for the dockable side panels., Projection settings, standard views and named camera bookmarks., Dockable control panels. (+1 more)

### Community 31 - "Matcap Textures and UI Wiring"
Cohesion: 0.15
Nodes (13): QScrollArea, MatcapLoadError, RuntimeError, Matcap texture loading and upload., Raised when an image cannot be used as a matcap., Qt user interface: the viewport widget, the panels and the main window., Application window: viewport, docked panels, menus and shortcuts., Matcap selection and colour grading. (+5 more)

### Community 32 - "OBJ Loader and Normals"
Cohesion: 0.17
Nodes (18): compute_vertex_normals(), Area-weighted smooth vertex normals for an indexed triangle soup., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic() (+10 more)

### Community 33 - "Camera Tests"
Cohesion: 0.12
Nodes (8): parametrize, camera(), fixture, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_serialisation_round_trip(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "Panel Base Class"
Cohesion: 0.15
Nodes (8): QStyledItemDelegate, Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block., _NameOnlyDelegate, Allows in-place editing of the name column only.

### Community 35 - "Mesh Format Tests"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

### Community 36 - "Cross-section Panel"
Cohesion: 0.23
Nodes (5): Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 37 - "Removal Command and Session Tests"
Cohesion: 0.14
Nodes (11): Delete the item at ``index``, putting it back in place on undo., RemoveItem, Session persistence, measurements and bookmarks., Version 1 files predate the annotation layer and the endpoint lock., Deletion goes through the undo stack, so the store only tracks position., test_a_session_from_before_annotations_still_loads(), test_deleting_a_bookmark_moves_the_cycling_position(), test_length_formatting_uses_the_display_unit() (+3 more)

### Community 38 - "OBJ Parsing Tests"
Cohesion: 0.27
Nodes (12): load_obj(), ObjLoadError, Path, Raised when a file cannot be interpreted as an OBJ mesh., Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, OBJ parsing: normals, triangulation and index handling., test_empty_file_is_rejected(), test_missing_normals_are_computed() (+4 more)

### Community 39 - "Command Protocol"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 40 - "Session Snapshot and Units"
Cohesion: 0.24
Nodes (7): MeasurementSettings, How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., Path, A snapshot of everything worth keeping between runs., Session, test_session_round_trip()

### Community 41 - "Snapped Orbit Tests"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 42 - "Annotation Model and Modes"
Cohesion: 0.22
Nodes (6): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a…

### Community 43 - "SetAttributes Command"
Cohesion: 0.29
Nodes (3): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes

### Community 44 - "Dataclass JSON Serialization"
Cohesion: 0.31
Nodes (8): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., T

### Community 45 - "Morton Curve Spatial Index"
Cohesion: 0.28
Nodes (7): _morton_order(), ndarray, Build the index from expanded triangle corners, shape ``(T, 3, 3)``., Triangle indices worth intersecting for this ray, possibly empty., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the…, Interleave each 10-bit value with two zero bits, ready to be shifted., _spread_bits()

### Community 46 - "Annotate Panel"
Cohesion: 0.28
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 47 - "GL Texture Wrapper"
Cohesion: 0.29
Nodes (3): ndarray, An RGBA8 2D texture with clamped edges and mipmapped minification., Texture2D

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Camera` connect `Camera Gestures` to `Camera Tests`, `Measure Tool and Handles`, `Annotate Tool and Brush`, `Viewer State and Model Loading`, `Removal Command and Session Tests`, `Session Snapshot and Units`, `Mesh and Bounds`, `Render Settings and Frame Draw`, `Snapped Orbit Tests`, `Projection and Linear Algebra`, `Build, Packaging and Architecture Rules`, `Bookmarks and Section Enums`, `Frustum Fitting`, `Screen-to-World Panning`, `Camera Bookmark Store`, `Navigation and Angle Snapping`, `Matcap Textures and UI Wiring`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Why does `Mesh` connect `Mesh and Bounds` to `OBJ Loader and Normals`, `Mesh Format Tests`, `Annotate Tool and Brush`, `Viewer State and Model Loading`, `OBJ Parsing Tests`, `Raycasting and Surface Picking`, `Projection and Linear Algebra`, `Model Orientation`, `glTF Loader`, `Bookmarks and Section Enums`, `Section Planes and Contours`, `Scene Renderer and GL Buffers`, `Release Notes and Picking Index`, `Mesh IO and STL Loader`, `Matcap Textures and UI Wiring`?**
  _High betweenness centrality (0.122) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `Viewer State and Model Loading` to `Measure Tool and Handles`, `Panel Base Class`, `Annotate Tool and Brush`, `Viewport Widget`, `Main Window, Menus and Drops`, `Model Orientation`, `Build, Packaging and Architecture Rules`, `Undo Commands and Panel Plumbing`, `Matcap Textures and UI Wiring`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `ViewportOverlay`) actually correct?**
  _`ViewerState` has 3 INFERRED edges - model-reasoned connections that need verification._