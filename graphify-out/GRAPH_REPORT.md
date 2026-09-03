# Graph Report - reference-viewer  (2026-09-03)

## Corpus Check
- 72 files · ~204,897 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1313 nodes · 2873 edges · 47 communities (45 shown, 2 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 140 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7081419f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Stroke
- application.py
- main_window.py
- Viewport Widget
- AnnotateTool
- ViewportOverlay
- MainWindow
- MeasurePanel
- raycast_mesh
- core/__init__.py
- RenderSettings
- render/__init__.py
- mesh_renderer.py
- OrientationSettings
- Camera
- README.md
- gltf_loader.py
- viewport.py
- _Target
- SectionSettings
- MeasureTool
- ShaderProgram
- .point
- SceneRenderer
- CameraPanel
- BookmarkStore
- Navigation and Angle Snapping
- History
- Mesh
- mesh.py
- RemoveItem
- .clip_planes
- obj_loader.py
- test_camera.py
- Panel
- test_mesh_io.py
- ViewerState
- section.py
- Snapped Orbit Tests
- state.py
- .from_dict
- Agent Graph-First Instructions
- Screen-to-World Panning
- session.py
- ShadingMode
- SliderSpin
- orientation.py

## God Nodes (most connected - your core abstractions)
1. `Camera` - 71 edges
2. `Mesh` - 57 edges
3. `Viewport` - 47 edges
4. `ViewerState` - 46 edges
5. `MainWindow` - 44 edges
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

## Communities (47 total, 2 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.06
Nodes (36): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+28 more)

### Community 1 - "application.py"
Cohesion: 0.05
Nodes (54): ArgumentParser, Color, Namespace, QApplication, QSplashScreen, Charcoal matcap, Terracotta clay matcap, Jade matcap (+46 more)

### Community 2 - "main_window.py"
Cohesion: 0.07
Nodes (44): QRunnable, check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and… (+36 more)

### Community 3 - "Viewport Widget"
Cohesion: 0.07
Nodes (15): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current., Drop whatever gesture is half-finished, without disarming the tool., Record the finished drag as a single undo step., Rub out the stroke points under the eraser, live. (+7 more)

### Community 4 - "AnnotateTool"
Cohesion: 0.10
Nodes (18): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+10 more)

### Community 5 - "ViewportOverlay"
Cohesion: 0.22
Nodes (14): QColor, QPainter, QPointF, project_visible(), QFont, A square grip, so an editable end reads differently from a fixed one., Preview the gesture under way; finished strokes are drawn in 3D., The cursor ring: the eraser's reach, or the width of the brush. (+6 more)

### Community 6 - "MainWindow"
Cohesion: 0.07
Nodes (16): QAction, QMainWindow, QScrollArea, MainWindow, Path, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while… (+8 more)

### Community 7 - "MeasurePanel"
Cohesion: 0.07
Nodes (20): QIcon, QPixmap, QStyledItemDelegate, QTreeWidgetItem, Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, lock_icon() (+12 more)

### Community 8 - "raycast_mesh"
Cohesion: 0.06
Nodes (45): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.… (+37 more)

### Community 9 - "core/__init__.py"
Cohesion: 0.11
Nodes (24): Qt-free geometry, camera and document model for the reference viewer., Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray (+16 more)

### Community 10 - "RenderSettings"
Cohesion: 0.12
Nodes (19): Everything the viewport needs in order to draw a frame., RenderSettings, light_directions(), normal_matrix(), ndarray, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.…, The model, the pedestal under it and the flat cap over the cut. (+11 more)

### Community 11 - "render/__init__.py"
Cohesion: 0.15
Nodes (10): OpenGL rendering layer: shader programs, textures and the scene renderer., default_matcap_pixels(), MatcapLoadError, ndarray, RuntimeError, Matcap texture loading and upload., Raised when an image cannot be used as a matcap., A neutral studio matcap, used before the user picks one. (+2 more)

### Community 12 - "mesh_renderer.py"
Cohesion: 0.11
Nodes (27): Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., look_at(), normalize(), orthographic() (+19 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 14 - "Camera"
Cohesion: 0.11
Nodes (13): Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling… (+5 more)

### Community 15 - "README.md"
Cohesion: 0.10
Nodes (23): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, refview (+15 more)

### Community 16 - "gltf_loader.py"
Cohesion: 0.09
Nodes (35): Cross-section tool (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, STL and glTF import (1.1.0) (+27 more)

### Community 17 - "viewport.py"
Cohesion: 0.10
Nodes (18): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, What the annotate tool does with a drag. The first three describe the shape a…, Measurement, Named point-to-point measurements and their presentation options., A straight distance between two points on the model surface. (+10 more)

### Community 18 - "_Target"
Cohesion: 0.10
Nodes (10): bind_default(), current_framebuffer(), Offscreen render targets used by the high-quality pass. Three of them are…, The framebuffer object bound right now -- Qt's, in a widget., Restore a framebuffer captured with :func:`current_framebuffer`., Fail loudly on an unusable attachment rather than rendering nothing. An…, Shared lifetime handling for a framebuffer with one attachment. The GL objects…, Reallocate the attachment, but only when the size actually changed. (+2 more)

### Community 19 - "SectionSettings"
Cohesion: 0.11
Nodes (22): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, Unit axis, or ``None`` for a custom direction., A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn. (+14 more)

### Community 20 - "MeasureTool"
Cohesion: 0.12
Nodes (10): Handle, MeasureTool, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., Where a click at ``(x, y)`` would put a point. With free placement the point… (+2 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - ".point"
Cohesion: 0.29
Nodes (4): ndarray, Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-…, Screen-to-world scale at a given depth along the view direction.

### Community 23 - "SceneRenderer"
Cohesion: 0.09
Nodes (14): ColorTarget, DepthTarget, GeometryTarget, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the…, A depth-only framebuffer, sampled afterwards as a texture., ``clamp_to_lit`` makes everything outside the map read as unshadowed., MeshBuffers (+6 more)

### Community 24 - "CameraPanel"
Cohesion: 0.13
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 25 - "BookmarkStore"
Cohesion: 0.13
Nodes (7): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., test_bookmarks_cycle_and_wrap()

### Community 26 - "Navigation and Angle Snapping"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "History"
Cohesion: 0.05
Nodes (30): Camera motion is deliberately not undoable, AddItem, Append an item to a document list., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, ReplaceItems, Command, History, One reversible change, named for the undo menu. (+22 more)

### Community 28 - "Mesh"
Cohesion: 0.13
Nodes (7): Mesh, ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, test_bounds_of_an_empty_point_set()

### Community 29 - "mesh.py"
Cohesion: 0.14
Nodes (20): compute_vertex_normals(), One entry point for every mesh format the viewer reads. Callers ask for a path…, MeshLoadError, RuntimeError, Triangle-mesh containers shared by the loader, the renderer and picking., Raised when a file cannot be interpreted as a triangle mesh., Area-weighted smooth vertex normals for an indexed triangle soup., _ascii_corners() (+12 more)

### Community 30 - "RemoveItem"
Cohesion: 0.33
Nodes (4): Delete the item at ``index``, putting it back in place on undo., RemoveItem, Deletion goes through the undo stack, so the store only tracks position., test_deleting_a_bookmark_moves_the_cycling_position()

### Community 32 - "obj_loader.py"
Cohesion: 0.12
Nodes (28): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic(), load_obj(), ObjLoadError (+20 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "Panel"
Cohesion: 0.10
Nodes (18): QFormLayout, QGroupBox, The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, Surface annotation tool: brush, shape and eraser settings., Panel, QWidget, Shared plumbing for the dockable side panels. (+10 more)

### Community 35 - "test_mesh_io.py"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

### Community 37 - "ViewerState"
Cohesion: 0.09
Nodes (16): The document this window edits., ndarray, Path, QObject, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements and…, Rotate the measurements and annotations onto the turned model. A point sits at… (+8 more)

### Community 39 - "section.py"
Cohesion: 0.27
Nodes (7): Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Which side of the plane survives the cut., SectionAxis, SectionMode

### Community 41 - "Snapped Orbit Tests"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 43 - "state.py"
Cohesion: 0.11
Nodes (19): Named camera positions the artist can jump between while sculpting., MeasurementSettings, How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., Path, A snapshot of everything worth keeping between runs., Session file that sits beside a model, e.g. ``bust.refview.json``., Session (+11 more)

### Community 45 - ".from_dict"
Cohesion: 0.29
Nodes (3): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., test_serialisation_round_trip()

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 55 - "session.py"
Cohesion: 0.27
Nodes (9): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Persisted viewer state: camera, shading, measurements and bookmarks. (+1 more)

### Community 56 - "ShadingMode"
Cohesion: 0.14
Nodes (10): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, Enum, str, QualitySettings, Soft shadows and ambient occlusion for the high-quality mode. Both are screen-…, Shading model applied to the mesh. ``shader_id`` must stay in sync with the… (+2 more)

### Community 57 - "SliderSpin"
Cohesion: 0.06
Nodes (21): QPushButton, AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle., Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear… (+13 more)

### Community 61 - "orientation.py"
Cohesion: 0.19
Nodes (8): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis, ModelPanel, What was imported and which way up it should stand., Turns the model the right way up and reports what came out of the file.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Camera` connect `Camera` to `test_camera.py`, `ViewportOverlay`, `raycast_mesh`, `core/__init__.py`, `RenderSettings`, `state.py`, `mesh_renderer.py`, `.from_dict`, `Snapped Orbit Tests`, `README.md`, `viewport.py`, `Screen-to-World Panning`, `BookmarkStore`, `Navigation and Angle Snapping`, `RemoveItem`, `.clip_planes`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Why does `Mesh` connect `Mesh` to `obj_loader.py`, `test_mesh_io.py`, `ViewerState`, `section.py`, `raycast_mesh`, `core/__init__.py`, `state.py`, `mesh_renderer.py`, `OrientationSettings`, `gltf_loader.py`, `SectionSettings`, `SceneRenderer`, `mesh.py`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport Widget` to `main_window.py`, `AnnotateTool`, `ViewportOverlay`, `MainWindow`, `ViewerState`, `viewport.py`, `MeasureTool`, `Navigation and Angle Snapping`?**
  _High betweenness centrality (0.070) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `ViewportOverlay`) actually correct?**
  _`ViewerState` has 3 INFERRED edges - model-reasoned connections that need verification._