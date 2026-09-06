# Graph Report - reference-viewer  (2026-09-06)

## Corpus Check
- 73 files · ~207,571 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1329 nodes · 2913 edges · 58 communities (55 shown, 3 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 143 edges (avg confidence: 0.64)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a226dd0b`
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
- ShadingMode
- raycast_mesh
- Bounds
- RenderSettings
- texture.py
- mesh_renderer.py
- OrientationSettings
- Camera
- README.md
- mesh.py
- viewport.py
- GeometryTarget
- SectionSettings
- TriangleIndex
- ShaderProgram
- _NameOnlyDelegate
- SceneRenderer
- CameraPanel
- BookmarkStore
- Navigation and Angle Snapping
- History
- ndarray
- load_stl
- ._suppressed
- ShadingPanel
- obj_loader.py
- test_camera.py
- main_window.py
- test_mesh_io.py
- load_obj
- ViewerState
- release_from_payload
- core/__init__.py
- SectionPanel
- Snapped Orbit Tests
- state.py
- UpdateChecker
- .from_dict
- load_matcap_pixels
- .copy
- Agent Graph-First Instructions
- Mesh
- .__init__
- Screen-to-World Panning
- AnnotatePanel
- Path
- settings.py
- scrollable
- CHANGELOG.md
- ._start_update_check
- PlaneSettings

## God Nodes (most connected - your core abstractions)
1. `Camera` - 71 edges
2. `Mesh` - 57 edges
3. `Viewport` - 47 edges
4. `ViewerState` - 46 edges
5. `MainWindow` - 44 edges
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

## Communities (58 total, 3 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.06
Nodes (36): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+28 more)

### Community 1 - "application.py"
Cohesion: 0.06
Nodes (41): ArgumentParser, Namespace, QApplication, QIcon, QPixmap, QSplashScreen, _apply_startup_arguments(), build_parser() (+33 more)

### Community 2 - "Release"
Cohesion: 0.18
Nodes (16): check_for_update(), fetch_latest_release(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed)., The newest published release, as GitHub describes it., Return the newest published release, or raise :class:`UpdateCheckError`., The newest release when it is later than ``current_version``, else ``None``. (+8 more)

### Community 3 - "Viewport Widget"
Cohesion: 0.07
Nodes (15): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current., Drop whatever gesture is half-finished, without disarming the tool., Record the finished drag as a single undo step., Rub out the stroke points under the eraser, live. (+7 more)

### Community 4 - "annotation.py"
Cohesion: 0.16
Nodes (11): AnnotateMode, AnnotationSettings, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a… (+3 more)

### Community 5 - "AnnotateTool"
Cohesion: 0.05
Nodes (40): Handle, QColor, QPainter, QPointF, AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved. (+32 more)

### Community 6 - "MainWindow"
Cohesion: 0.09
Nodes (10): QAction, QMainWindow, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits., Keep the menu entry agreeing with the panel's own checkbox. (+2 more)

### Community 7 - "ShadingMode"
Cohesion: 0.22
Nodes (4): str, Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode

### Community 8 - "raycast_mesh"
Cohesion: 0.14
Nodes (21): Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``. (+13 more)

### Community 9 - "Bounds"
Cohesion: 0.18
Nodes (15): Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray, A turntable-style disc the model can stand on. A ground plane gives the eye… (+7 more)

### Community 10 - "RenderSettings"
Cohesion: 0.12
Nodes (19): Everything the viewport needs in order to draw a frame., RenderSettings, light_directions(), normal_matrix(), ndarray, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.…, The model, the pedestal under it and the flat cap over the cut. (+11 more)

### Community 11 - "texture.py"
Cohesion: 0.40
Nodes (4): MatcapLoadError, RuntimeError, Matcap texture loading and upload., Raised when an image cannot be used as a matcap.

### Community 12 - "mesh_renderer.py"
Cohesion: 0.11
Nodes (27): Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., look_at(), normalize(), orthographic() (+19 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.09
Nodes (24): OrientationSettings, Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., UpAxis (+16 more)

### Community 14 - "Camera"
Cohesion: 0.15
Nodes (9): Camera, ndarray, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling…, A look-at camera with orbit / pan / zoom behaviour. The orthographic extent is…, Vertical half-extent of the frustum at the focal plane. (+1 more)

### Community 15 - "README.md"
Cohesion: 0.10
Nodes (23): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, refview (+15 more)

### Community 16 - "mesh.py"
Cohesion: 0.09
Nodes (36): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry() (+28 more)

### Community 17 - "viewport.py"
Cohesion: 0.15
Nodes (8): The handful of undoable edits the whole application is built from.…, Swap the whole contents of a document list. Used for bulk edits -- clearing the…, ReplaceItems, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, Qt user interface: the viewport widget, the panels and the main window., configure_surface_format(), The interactive 3D view. Navigation is: left-drag orbits about the point under…, Request a core-profile context; must run before the QApplication.

### Community 18 - "GeometryTarget"
Cohesion: 0.08
Nodes (17): bind_default(), ColorTarget, current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the… (+9 more)

### Community 19 - "SectionSettings"
Cohesion: 0.16
Nodes (15): Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., How the model is cut open, and how the cut is drawn., SectionSettings, _box(), Cutting planes, the contour they produce and the pedestal under the model., A closed axis-aligned cube centred on the origin., The contour of a plane through a cube is its cross-section outline. (+7 more)

### Community 20 - "TriangleIndex"
Cohesion: 0.11
Nodes (21): Picking about a hundred times faster, Morton-curve leaf boxes for picking, _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., Build the index from expanded triangle corners, shape ``(T, 3, 3)``., Triangle indices worth intersecting for this ray, possibly empty. (+13 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.12
Nodes (9): OpenGL rendering layer: shader programs, textures and the scene renderer., ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError (+1 more)

### Community 22 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): QStyledItemDelegate, _NameOnlyDelegate, Allows in-place editing of the name column only.

### Community 23 - "SceneRenderer"
Cohesion: 0.10
Nodes (12): MeshBuffers, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the ground disc; pass ``None`` to hide it., Replace the annotation geometry; pass an empty list to hide it., Vertex/index buffers for one mesh, bound through a single VAO., Forget the contents without releasing the buffer objects., SceneRenderer, default_matcap_pixels() (+4 more)

### Community 24 - "CameraPanel"
Cohesion: 0.05
Nodes (20): QListWidgetItem, QTreeWidgetItem, Any, Assign one or more attributes on an object, remembering the old values.…, Delete the item at ``index``, putting it back in place on undo., RemoveItem, SetAttributes, CameraPanel (+12 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.13
Nodes (8): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Deletion goes through the undo stack, so the store only tracks position., test_deleting_a_bookmark_moves_the_cycling_position()

### Community 26 - "Navigation and Angle Snapping"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "History"
Cohesion: 0.06
Nodes (28): Camera motion is deliberately not undoable, AddItem, Append an item to a document list., Command, History, One reversible change, named for the undo menu., A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive… (+20 more)

### Community 28 - "ndarray"
Cohesion: 0.18
Nodes (4): ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, test_bounds_of_an_empty_point_set()

### Community 29 - "load_stl"
Cohesion: 0.21
Nodes (12): _ascii_corners(), _binary_corners(), load_stl(), ndarray, Path, Raised when a file cannot be interpreted as an STL mesh., Load ``path``, choosing the binary or ASCII reader by inspection., Facet corners from a binary STL, or ``None`` if this is not one. The declared… (+4 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.24
Nodes (6): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., ShadingPanel

### Community 32 - "obj_loader.py"
Cohesion: 0.22
Nodes (14): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), ndarray, Minimal, dependency-free Wavefront OBJ reader. Only the geometry statements a…, Resolve ``v``, ``v/vt``, ``v//vn`` or ``v/vt/vn`` corners to 0-based pairs.… (+6 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "main_window.py"
Cohesion: 0.10
Nodes (24): QFormLayout, QGroupBox, QPushButton, Application window: viewport, docked panels, menus and shortcuts., Surface annotation tool: brush, shape and eraser settings., Panel, Shared plumbing for the dockable side panels., A panel bound to the :class:`ViewerState`. Subclasses build their controls in… (+16 more)

### Community 35 - "test_mesh_io.py"
Cohesion: 0.22
Nodes (14): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one(), test_binary_stl_welds_shared_corners() (+6 more)

### Community 36 - "load_obj"
Cohesion: 0.22
Nodes (14): load_obj(), ObjLoadError, Path, Raised when a file cannot be interpreted as an OBJ mesh., Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, Negative face indices count back from the most recent vertex., test_obj_relative_indices_still_load(), OBJ parsing: normals, triangulation and index handling. (+6 more)

### Community 37 - "ViewerState"
Cohesion: 0.09
Nodes (15): ndarray, Path, QObject, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements and…, Rotate the measurements and annotations onto the turned model. A point sits at…, Take the display unit from the file when the format declares one. Only glTF… (+7 more)

### Community 38 - "release_from_payload"
Cohesion: 0.19
Nodes (14): is_newer(), _padded(), parse_version(), Numeric components of ``text``, or ``None`` when it is not a version. A pre-…, Whether ``candidate`` is a strictly later version than ``current``., Pull the tag and page link out of a GitHub release document., release_from_payload(), parametrize (+6 more)

### Community 39 - "core/__init__.py"
Cohesion: 0.14
Nodes (15): Qt-free geometry, camera and document model for the reference viewer., Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, The direction the section plane faces., Unit axis, or ``None`` for a custom direction. (+7 more)

### Community 40 - "SectionPanel"
Cohesion: 0.23
Nodes (5): Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 41 - "Snapped Orbit Tests"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 43 - "state.py"
Cohesion: 0.07
Nodes (37): Named camera positions the artist can jump between while sculpting., Measurement, MeasurementSettings, Named point-to-point measurements and their presentation options., A straight distance between two points on the model surface., Distance in scene units., Name of the attribute a handle edits, for building an undo command., How measurements are drawn and how their lengths are written out. (+29 more)

### Community 44 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 45 - ".from_dict"
Cohesion: 0.29
Nodes (3): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., test_serialisation_round_trip()

### Community 46 - "load_matcap_pixels"
Cohesion: 0.18
Nodes (20): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+12 more)

### Community 47 - ".copy"
Cohesion: 0.17
Nodes (5): Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Move the camera so ``bounds`` fills the view, keeping the direction., Point the camera along ``direction``, measured object-to-eye., Adopt the pose of ``other`` without replacing this instance.

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "Mesh"
Cohesion: 0.14
Nodes (9): Mesh, Picking accelerator, built on first use and kept for the mesh's life., Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, _load_generic(), Line-by-line reader for files the fast path declines., fixture, quad() (+1 more)

### Community 53 - "AnnotatePanel"
Cohesion: 0.28
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 55 - "Path"
Cohesion: 0.29
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 56 - "settings.py"
Cohesion: 0.22
Nodes (8): LightSettings, MatcapSettings, Enum, Serialisable description of how the object should be shaded. Every value here…, Material parameters shared by the analytic shading modes., Post-processing applied to the sampled matcap texel., A key light, an opposing fill and a hemispherical ambient term., SurfaceSettings

### Community 57 - "scrollable"
Cohesion: 0.17
Nodes (5): QScrollArea, QWidget, Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, Re-scale the control, e.g. once a model's size is known., scrollable()

### Community 60 - "CHANGELOG.md"
Cohesion: 0.17
Nodes (12): Cross-section tool (1.1.0), High Quality shading mode (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding (+4 more)

### Community 63 - "._start_update_check"
Cohesion: 0.29
Nodes (4): Ask GitHub for the newest release in the background. The startup check is…, QWidget, show_failure_dialog(), show_up_to_date_dialog()

### Community 68 - "PlaneSettings"
Cohesion: 0.18
Nodes (8): PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor…, How much of a turn in the surface one plane covers, in degrees. Linear in…, The grid step, in cube-face coordinates, that gives that span. A cell of this…, PlanesPanel, Breaks the surface normals down into the planes of the form., The slider is linear in how much of a turn one plane covers., test_plane_detail_moves_the_plane_size_evenly()

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Camera` connect `Camera` to `test_camera.py`, `AnnotateTool`, `ViewerState`, `core/__init__.py`, `raycast_mesh`, `Bounds`, `RenderSettings`, `state.py`, `mesh_renderer.py`, `.from_dict`, `Snapped Orbit Tests`, `README.md`, `.copy`, `Screen-to-World Panning`, `BookmarkStore`, `Navigation and Angle Snapping`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Why does `Mesh` connect `Mesh` to `obj_loader.py`, `test_mesh_io.py`, `load_obj`, `ViewerState`, `core/__init__.py`, `raycast_mesh`, `Bounds`, `state.py`, `mesh_renderer.py`, `OrientationSettings`, `mesh.py`, `SectionSettings`, `TriangleIndex`, `SceneRenderer`, `ndarray`, `load_stl`?**
  _High betweenness centrality (0.094) - this node is a cross-community bridge._
- **Why does `MainWindow` connect `MainWindow` to `application.py`, `main_window.py`, `Release`, `Viewport Widget`, `ViewerState`, `UpdateChecker`, `viewport.py`, `Path`, `scrollable`, `._start_update_check`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `ViewportOverlay`) actually correct?**
  _`ViewerState` has 3 INFERRED edges - model-reasoned connections that need verification._