# Graph Report - reference-viewer  (2026-09-03)

## Corpus Check
- 69 files · ~203,595 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1256 nodes · 2755 edges · 64 communities (61 shown, 3 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 139 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `91c6d22a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Stroke
- application.py
- SectionPanel
- Viewport Widget
- AnnotateTool
- ViewerState
- MainWindow
- MeasurePanel
- raycast_mesh
- Bounds
- Render Settings and Frame Draw
- form_group
- mesh_renderer.py
- OrientationSettings
- Camera
- Build, Packaging and Architecture Rules
- gltf_loader.py
- MeasurementSettings
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
- ndarray
- core/__init__.py
- camera_panel.py
- main_window.py
- obj_loader.py
- Camera Tests
- Panel
- mesh_io.py
- Cross-section Panel
- load_matcap_pixels
- StrokeBuffers
- TriangleIndex
- load_obj
- Snapped Orbit Tests
- state.py
- Session
- ShadingMode
- Morton Curve Spatial Index
- AnnotatePanel
- GL Texture Wrapper
- Agent Graph-First Instructions
- CHANGELOG.md
- Mesh
- Screen-to-World Panning
- ColorButton
- section_segments
- annotation.py
- decode
- settings.py
- SliderSpin
- test_annotation.py
- test_spatial.py
- .split
- orientation.py
- ModelPanel
- .handle_at

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
- `Terracotta clay matcap` --shares_data_with--> `available_matcaps()`  [INFERRED]
  resources/matcaps/clay_terracotta.png → src/refview/paths.py
- `The cut interior is flooded flat` --rationale_for--> `SceneRenderer`  [INFERRED]
  README.md → src/refview/render/mesh_renderer.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The bundled matcap set** — resources_matcaps_clay_terracotta_matcap, resources_matcaps_charcoal_matcap, resources_matcaps_jade_matcap, resources_matcaps_steel_matcap, resources_matcaps_studio_white_matcap, resources_matcaps_wax_skin_matcap, tools_generate_matcaps_matcappreset, tools_generate_matcaps_render [INFERRED 0.85]
- **The four generic undo commands** — src_refview_core_commands_setattributes, src_refview_core_commands_additem, src_refview_core_commands_removeitem, src_refview_core_commands_replaceitems, src_refview_core_history_command, readme_every_edit_is_a_command [EXTRACTED 1.00]
- **Windows binary-compatibility decisions** — readme_pyside6_pinned_below_68, environment_pip_installed_binaries, environment_python_311, github_workflows_release_pyinstaller_build [INFERRED 0.75]

## Communities (64 total, 3 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.12
Nodes (12): AnnotationStore, An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Stroke, The strokes being laid down; the overlay previews them in 2D., The surviving arc wraps past the start of the list, so the gap is rotated to… (+4 more)

### Community 1 - "application.py"
Cohesion: 0.06
Nodes (41): ArgumentParser, Namespace, QApplication, QIcon, QPixmap, QSplashScreen, _apply_startup_arguments(), build_parser() (+33 more)

### Community 2 - "SectionPanel"
Cohesion: 0.11
Nodes (13): Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Unit axis, or ``None`` for a custom direction., Which side of the plane survives the cut., SectionAxis, SectionMode (+5 more)

### Community 3 - "Viewport Widget"
Cohesion: 0.07
Nodes (15): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current., Drop whatever gesture is half-finished, without disarming the tool., Record the finished drag as a single undo step., Rub out the stroke points under the eraser, live. (+7 more)

### Community 4 - "AnnotateTool"
Cohesion: 0.11
Nodes (17): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Painting annotations onto the model surface. Every shape is laid down the same…, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+9 more)

### Community 5 - "ViewerState"
Cohesion: 0.05
Nodes (38): QColor, QPainter, QPointF, Qt user interface: the viewport widget, the panels and the main window., MeasureTool, Two-click measuring, plus dragging the endpoints of an unlocked measurement., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed… (+30 more)

### Community 6 - "MainWindow"
Cohesion: 0.08
Nodes (13): QAction, QMainWindow, MainWindow, Path, Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits., Apply a matcap image, reporting unreadable files to the user. (+5 more)

### Community 7 - "MeasurePanel"
Cohesion: 0.12
Nodes (10): QStyledItemDelegate, QTreeWidgetItem, MeasurePanel, _NameOnlyDelegate, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Lock or unlock one measurement, making its endpoints draggable. (+2 more)

### Community 8 - "raycast_mesh"
Cohesion: 0.15
Nodes (20): Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``. (+12 more)

### Community 9 - "Bounds"
Cohesion: 0.18
Nodes (15): Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray, A turntable-style disc the model can stand on. A ground plane gives the eye… (+7 more)

### Community 10 - "Render Settings and Frame Draw"
Cohesion: 0.12
Nodes (21): Everything the viewport needs in order to draw a frame., RenderSettings, light_directions(), normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.… (+13 more)

### Community 11 - "form_group"
Cohesion: 0.17
Nodes (10): QFormLayout, QGroupBox, Shared plumbing for the dockable side panels., Dockable control panels., What was imported and which way up it should stand., Cross-section controls: the cutting plane, what it keeps and how it reads., Shading mode, lighting, surface material and scene furniture controls., form_group() (+2 more)

### Community 12 - "mesh_renderer.py"
Cohesion: 0.15
Nodes (23): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-…, Return ``v`` scaled to unit length, or ``fallback`` for a zero vector. (+15 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 14 - "Camera"
Cohesion: 0.15
Nodes (9): Camera, ndarray, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling…, A look-at camera with orbit / pan / zoom behaviour. The orthographic extent is…, Vertical half-extent of the frustum at the focal plane. (+1 more)

### Community 15 - "Build, Packaging and Architecture Rules"
Cohesion: 0.10
Nodes (23): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, refview (+15 more)

### Community 16 - "gltf_loader.py"
Cohesion: 0.12
Nodes (28): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry() (+20 more)

### Community 17 - "MeasurementSettings"
Cohesion: 0.15
Nodes (9): QObject, MeasurementSettings, How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., ndarray, Consume a picked point; returns a measurement on the second click., Where a click at ``(x, y)`` would put a point. With free placement the point…, Where a grabbed endpoint should move to. Free placement -- and a drag that… (+1 more)

### Community 18 - "Offscreen Render Targets"
Cohesion: 0.08
Nodes (17): bind_default(), ColorTarget, current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the… (+9 more)

### Community 19 - "SectionSettings"
Cohesion: 0.23
Nodes (13): How the model is cut open, and how the cut is drawn., SectionSettings, _box(), Cutting planes, the contour they produce and the pedestal under the model., A closed axis-aligned cube centred on the origin., The contour of a plane through a cube is its cross-section outline., test_a_custom_normal_is_normalised(), test_a_disabled_section_cuts_with_nothing() (+5 more)

### Community 20 - "ShadingPanel"
Cohesion: 0.23
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
Cohesion: 0.12
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 25 - "BookmarkStore"
Cohesion: 0.12
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Deletion goes through the undo stack, so the store only tracks position., test_bookmarks_cycle_and_wrap() (+1 more)

### Community 26 - "Navigation and Angle Snapping"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "History"
Cohesion: 0.07
Nodes (23): Camera motion is deliberately not undoable, AddItem, Any, Assign one or more attributes on an object, remembering the old values.…, Append an item to a document list., SetAttributes, Command, History (+15 more)

### Community 28 - "ndarray"
Cohesion: 0.20
Nodes (4): ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, test_bounds_of_an_empty_point_set()

### Community 29 - "core/__init__.py"
Cohesion: 0.14
Nodes (22): Qt-free geometry, camera and document model for the reference viewer., compute_vertex_normals(), MeshLoadError, RuntimeError, Triangle-mesh containers shared by the loader, the renderer and picking., Raised when a file cannot be interpreted as a triangle mesh., Area-weighted smooth vertex normals for an indexed triangle soup., ObjLoadError (+14 more)

### Community 30 - "camera_panel.py"
Cohesion: 0.14
Nodes (9): The handful of undoable edits the whole application is built from.…, Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, Surface annotation tool: brush, shape and eraser settings., Projection settings, standard views and named camera bookmarks. (+1 more)

### Community 31 - "main_window.py"
Cohesion: 0.14
Nodes (13): QScrollArea, Projection, Enum, str, Projection used by :class:`Camera`., MatcapLoadError, RuntimeError, Matcap texture loading and upload. (+5 more)

### Community 32 - "obj_loader.py"
Cohesion: 0.22
Nodes (14): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), ndarray, Minimal, dependency-free Wavefront OBJ reader. Only the geometry statements a…, Resolve ``v``, ``v/vt``, ``v//vn`` or ``v/vt/vn`` corners to 0-based pairs.… (+6 more)

### Community 33 - "Camera Tests"
Cohesion: 0.12
Nodes (7): parametrize, camera(), fixture, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "Panel"
Cohesion: 0.21
Nodes (5): Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block.

### Community 35 - "mesh_io.py"
Cohesion: 0.21
Nodes (14): load_mesh(), Path, One entry point for every mesh format the viewer reads. Callers ask for a path…, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+6 more)

### Community 36 - "Cross-section Panel"
Cohesion: 0.17
Nodes (5): Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Move the camera so ``bounds`` fills the view, keeping the direction., Point the camera along ``direction``, measured object-to-eye., Adopt the pose of ``other`` without replacing this instance.

### Community 37 - "load_matcap_pixels"
Cohesion: 0.18
Nodes (20): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+12 more)

### Community 38 - "StrokeBuffers"
Cohesion: 0.16
Nodes (12): build_segment_vertices(), build_vertices(), _expand(), ndarray, Geometry for the surface annotations and the cross-section contour. Strokes are…, A single vertex buffer holding every visible stroke., Replace the buffer contents with a prepared vertex block., Expand strokes into the triangle soup the stroke shader expects. Every segment… (+4 more)

### Community 39 - "TriangleIndex"
Cohesion: 0.15
Nodes (13): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., Build the index from expanded triangle corners, shape ``(T, 3, 3)``. (+5 more)

### Community 40 - "load_obj"
Cohesion: 0.24
Nodes (13): load_obj(), Path, Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, Negative face indices count back from the most recent vertex., test_obj_quads_are_triangulated(), test_obj_relative_indices_still_load(), OBJ parsing: normals, triangulation and index handling., test_empty_file_is_rejected() (+5 more)

### Community 41 - "Snapped Orbit Tests"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 42 - "state.py"
Cohesion: 0.21
Nodes (9): Named camera positions the artist can jump between while sculpting., Named point-to-point measurements and their presentation options., Persisted viewer state: camera, shading, measurements and bookmarks., Session file that sits beside a model, e.g. ``bust.refview.json``., sidecar_path(), NavigationSettings, How mouse gestures drive the camera., The observable document shared by the viewport and the side panels. Panels… (+1 more)

### Community 43 - "Session"
Cohesion: 0.20
Nodes (10): Path, A snapshot of everything worth keeping between runs., Session, Session persistence, measurements and bookmarks., Version 1 files predate the annotation layer and the endpoint lock., test_a_session_from_before_annotations_still_loads(), test_measurement_length_and_midpoint(), test_session_round_trip() (+2 more)

### Community 44 - "ShadingMode"
Cohesion: 0.22
Nodes (4): str, Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode

### Community 45 - "Morton Curve Spatial Index"
Cohesion: 0.29
Nodes (3): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., test_serialisation_round_trip()

### Community 46 - "AnnotatePanel"
Cohesion: 0.27
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 47 - "GL Texture Wrapper"
Cohesion: 0.29
Nodes (4): ndarray, Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-…, Screen-to-world scale at a given depth along the view direction.

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "CHANGELOG.md"
Cohesion: 0.17
Nodes (12): Cross-section tool (1.1.0), High Quality shading mode (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding (+4 more)

### Community 50 - "Mesh"
Cohesion: 0.15
Nodes (8): Mesh, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, _load_generic(), Line-by-line reader for files the fast path declines., fixture, quad(), Two triangles covering the unit square on the z = 0 plane.

### Community 52 - "ColorButton"
Cohesion: 0.24
Nodes (4): QPushButton, A draggable split: thumbnails above, adjustments below. The gallery is the one…, ColorButton, A swatch button that opens a colour picker. Colours are exchanged as 0-1 RGB…

### Community 53 - "section_segments"
Cohesion: 0.22
Nodes (8): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., section_segments(), SectionPlane

### Community 54 - "annotation.py"
Cohesion: 0.22
Nodes (6): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a…

### Community 55 - "decode"
Cohesion: 0.27
Nodes (8): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., T

### Community 56 - "settings.py"
Cohesion: 0.22
Nodes (8): LightSettings, MatcapSettings, Enum, Serialisable description of how the object should be shaded. Every value here…, Post-processing applied to the sampled matcap texel., A key light, an opposing fill and a hemispherical ambient term., Material parameters shared by the analytic shading modes., SurfaceSettings

### Community 57 - "SliderSpin"
Cohesion: 0.29
Nodes (4): QWidget, A float slider paired with a spin box, kept in sync. The slider works in…, Re-scale the control, e.g. once a model's size is known., SliderSpin

### Community 58 - "test_annotation.py"
Cohesion: 0.31
Nodes (9): line_stroke(), Surface annotations: erasing, splitting and the geometry handed to GL., A stroke running along +X, one unit apart, with +Y normals., test_a_closed_stroke_gains_the_wrapping_segment(), test_each_segment_becomes_six_vertices(), test_erasing_keeps_the_brush_and_drops_stubs(), test_erasing_nothing_reports_no_change(), test_erasing_the_middle_splits_a_stroke_in_two() (+1 more)

### Community 59 - "test_spatial.py"
Cohesion: 0.29
Nodes (9): _grid(), The picking accelerator: it must be fast without changing any answer., A bumpy height field, so rays hit different triangles at different depths., The pruned candidate set must never miss the true intersection., test_a_ray_that_misses_the_model_is_pruned_away(), test_an_empty_index_returns_no_candidates(), test_every_triangle_lands_in_exactly_one_leaf(), test_the_index_finds_the_triangle_a_ray_actually_hits() (+1 more)

### Community 60 - ".split"
Cohesion: 0.29
Nodes (5): ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., Normals padded to match the points, so callers can zip them freely., Break the stroke into the runs of points ``keep`` marks as surviving., _runs()

### Community 61 - "orientation.py"
Cohesion: 0.33
Nodes (5): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Camera` connect `Camera` to `Camera Tests`, `Cross-section Panel`, `ViewerState`, `raycast_mesh`, `Bounds`, `state.py`, `Render Settings and Frame Draw`, `mesh_renderer.py`, `Morton Curve Spatial Index`, `Snapped Orbit Tests`, `Build, Packaging and Architecture Rules`, `Session`, `MeasurementSettings`, `Screen-to-World Panning`, `BookmarkStore`, `Navigation and Angle Snapping`, `core/__init__.py`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Why does `Mesh` connect `Mesh` to `obj_loader.py`, `SectionPanel`, `mesh_io.py`, `ViewerState`, `TriangleIndex`, `load_obj`, `Bounds`, `raycast_mesh`, `state.py`, `mesh_renderer.py`, `OrientationSettings`, `gltf_loader.py`, `SectionSettings`, `section_segments`, `Scene Renderer and GL Buffers`, `test_spatial.py`, `ndarray`, `core/__init__.py`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `Panel`, `Viewport Widget`, `MainWindow`, `state.py`, `form_group`, `OrientationSettings`, `Build, Packaging and Architecture Rules`, `MeasurementSettings`, `main_window.py`?**
  _High betweenness centrality (0.076) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `ViewportOverlay`) actually correct?**
  _`ViewerState` has 3 INFERRED edges - model-reasoned connections that need verification._