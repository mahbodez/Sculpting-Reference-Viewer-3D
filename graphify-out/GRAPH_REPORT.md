# Graph Report - reference-viewer  (2026-09-06)

## Corpus Check
- 77 files · ~212,901 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1455 nodes · 3133 edges · 71 communities (69 shown, 2 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 148 edges (avg confidence: 0.64)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5012b69e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Stroke
- application.py
- Release
- Viewport Widget
- plane_axes
- AnnotateTool
- MainWindow
- ViewportOverlay
- raycast_mesh
- Bounds
- SceneRenderer
- ndarray
- mesh_renderer.py
- OrientationSettings
- Camera
- README.md
- gltf_loader.py
- main_window.py
- GeometryTarget
- CameraPanel
- TriangleIndex
- ShaderProgram
- plane_axes.py
- MeshBuffers
- MeasurePanel
- BookmarkStore
- NavigationController
- History
- Mesh
- core/__init__.py
- MeasurementSettings
- ShadingPanel
- obj_loader.py
- test_camera.py
- form_group
- WakeLock
- CHANGELOG.md
- .apply_session
- update_check.py
- SectionSettings
- SectionPanel
- Snapped Orbit Tests
- section.py
- Measurement
- UpdateChecker
- wakelock.py
- test_spatial.py
- _ScreenSaverBackend
- Agent Graph-First Instructions
- _WindowsBackend
- Panel
- Screen-to-World Panning
- ViewerState
- AnnotatePanel
- _MacBackend
- Path
- settings.py
- .__init__
- orientation.py
- stroke_renderer.py
- RemoveItem
- SliderSpin
- refview/__init__.py
- QTreeWidgetItem
- SetAttributes
- environment.yml
- release.yml
- shaders.py
- LightSettings
- _NameOnlyDelegate
- ._move_marks

## God Nodes (most connected - your core abstractions)
1. `Camera` - 71 edges
2. `Mesh` - 66 edges
3. `Viewport` - 47 edges
4. `MainWindow` - 46 edges
5. `ViewerState` - 46 edges
6. `SceneRenderer` - 38 edges
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

## Communities (71 total, 2 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.07
Nodes (28): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+20 more)

### Community 1 - "application.py"
Cohesion: 0.05
Nodes (56): ArgumentParser, Color, Namespace, QApplication, QPixmap, QSplashScreen, Charcoal matcap, Terracotta clay matcap (+48 more)

### Community 2 - "Release"
Cohesion: 0.18
Nodes (12): The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, is_skipped(), QWidget, Background release check and the notice it puts in front of the artist. The…, Whether the artist already dismissed this exact version., Offer the release page, with the option never to be asked again. (+4 more)

### Community 3 - "Viewport Widget"
Cohesion: 0.07
Nodes (15): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current., Drop whatever gesture is half-finished, without disarming the tool., Record the finished drag as a single undo step., Rub out the stroke points under the eraser, live. (+7 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - "AnnotateTool"
Cohesion: 0.11
Nodes (17): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+9 more)

### Community 6 - "MainWindow"
Cohesion: 0.10
Nodes (10): QAction, QMainWindow, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., The document this window edits., Keep the menu entry agreeing with the panel's own checkbox., Keep the panel button and the menu entry agreeing with the tool. (+2 more)

### Community 7 - "ViewportOverlay"
Cohesion: 0.14
Nodes (18): QColor, QPainter, QPointF, MeasureTool, Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., project_visible() (+10 more)

### Community 8 - "raycast_mesh"
Cohesion: 0.11
Nodes (24): Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``. (+16 more)

### Community 9 - "Bounds"
Cohesion: 0.12
Nodes (19): Bounds, ndarray, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray (+11 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.11
Nodes (22): Everything the viewport needs in order to draw a frame., RenderSettings, light_directions(), normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, The model's own plane directions, fitted once and kept., Replace the section contour, prepared by the caller as stroke vertices. (+14 more)

### Community 11 - "ndarray"
Cohesion: 0.15
Nodes (6): ndarray, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling…, Near/far planes fitted to the scene bounding sphere.

### Community 12 - "mesh_renderer.py"
Cohesion: 0.11
Nodes (29): Named camera positions the artist can jump between while sculpting., Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., look_at(), normalize() (+21 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 14 - "Camera"
Cohesion: 0.14
Nodes (9): Camera, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Move the camera so ``bounds`` fills the view, keeping the direction., Point the camera along ``direction``, measured object-to-eye., Adopt the pose of ``other`` without replacing this instance., A look-at camera with orbit / pan / zoom behaviour. The orthographic extent is…, Vertical half-extent of the frustum at the focal plane. (+1 more)

### Community 15 - "README.md"
Cohesion: 0.18
Nodes (15): High Quality shading mode (1.1.0), Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command, High Quality without ray tracing, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter (+7 more)

### Community 16 - "gltf_loader.py"
Cohesion: 0.14
Nodes (24): _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry(), _primitives(), ndarray (+16 more)

### Community 17 - "main_window.py"
Cohesion: 0.08
Nodes (27): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, What the annotate tool does with a drag. The first three describe the shape a…, The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, Named point-to-point measurements and their presentation options. (+19 more)

### Community 18 - "GeometryTarget"
Cohesion: 0.08
Nodes (17): bind_default(), ColorTarget, current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the… (+9 more)

### Community 19 - "CameraPanel"
Cohesion: 0.12
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "TriangleIndex"
Cohesion: 0.14
Nodes (14): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., Build the index from expanded triangle corners, shape ``(T, 3, 3)``. (+6 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.12
Nodes (10): OpenGL rendering layer: shader programs, textures and the scene renderer., ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload an ``(n, 3)`` array into a ``vec3[]`` uniform in one call., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform… (+2 more)

### Community 22 - "plane_axes.py"
Cohesion: 0.16
Nodes (11): PlaneAxes, ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, Cut a group across its first principal component, or refuse to., The directions a model's normals fall into, at every count. Built once per…, The best ``count`` directions, or as many as the model supports. A model whose…, How much surface each vertex stands for: a third of each triangle on it.…, The plane direction of a group, its spread, and its total weight. (+3 more)

### Community 23 - "MeshBuffers"
Cohesion: 0.07
Nodes (12): MeshBuffers, Replace the ground disc; pass ``None`` to hide it., Replace the annotation geometry; pass an empty list to hide it., Vertex/index buffers for one mesh, bound through a single VAO., Forget the contents without releasing the buffer objects., A single vertex buffer holding every visible stroke., StrokeBuffers, default_matcap_pixels() (+4 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.20
Nodes (4): MeasurePanel, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Lists saved measurements and controls how they are drawn.

### Community 25 - "BookmarkStore"
Cohesion: 0.10
Nodes (11): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around. (+3 more)

### Community 26 - "NavigationController"
Cohesion: 0.13
Nodes (11): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Tracks an in-progress drag and applies it to a camera. (+3 more)

### Community 27 - "History"
Cohesion: 0.06
Nodes (27): Camera motion is deliberately not undoable, AddItem, Append an item to a document list., Command, History, One reversible change, named for the undo menu., A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive… (+19 more)

### Community 28 - "Mesh"
Cohesion: 0.14
Nodes (8): Mesh, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, fixture, quad(), Two triangles covering the unit square on the z = 0 plane.

### Community 29 - "core/__init__.py"
Cohesion: 0.15
Nodes (21): Qt-free geometry, camera and document model for the reference viewer., compute_vertex_normals(), One entry point for every mesh format the viewer reads. Callers ask for a path…, MeshLoadError, RuntimeError, Triangle-mesh containers shared by the loader, the renderer and picking., Raised when a file cannot be interpreted as a triangle mesh., Area-weighted smooth vertex normals for an indexed triangle soup. (+13 more)

### Community 30 - "MeasurementSettings"
Cohesion: 0.13
Nodes (10): Handle, MeasurementSettings, How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., ndarray, Two-click measuring, plus dragging the endpoints of an unlocked measurement., Consume a picked point; returns a measurement on the second click., Where a click at ``(x, y)`` would put a point. With free placement the point… (+2 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.24
Nodes (6): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., ShadingPanel

### Community 32 - "obj_loader.py"
Cohesion: 0.07
Nodes (44): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast() (+36 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "form_group"
Cohesion: 0.21
Nodes (7): QFormLayout, QGroupBox, QPushButton, ColorButton, form_group(), A swatch button that opens a colour picker. Colours are exchanged as 0-1 RGB…, A titled group box with a form layout, ready to be filled.

### Community 35 - "WakeLock"
Cohesion: 0.17
Nodes (13): Holds sleep off while the window that owns it is the one in front. The class…, WakeLock, Broken, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do., A platform that refuses, the way an old or locked-down one might., The viewer must open and close normally on a machine that says no., Recorder (+5 more)

### Community 36 - "CHANGELOG.md"
Cohesion: 0.14
Nodes (13): Shift-snapped orbiting (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, STL and glTF import (1.1.0) (+5 more)

### Community 37 - ".apply_session"
Cohesion: 0.15
Nodes (7): Path, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements and…, Set the active matcap, or fall back to the built-in one., Fit the current mesh in the view without changing the direction., Adopt a session's settings, leaving the loaded mesh alone.

### Community 38 - "update_check.py"
Cohesion: 0.14
Nodes (22): check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed). (+14 more)

### Community 39 - "SectionSettings"
Cohesion: 0.12
Nodes (21): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn., section_segments() (+13 more)

### Community 40 - "SectionPanel"
Cohesion: 0.22
Nodes (6): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 41 - "Snapped Orbit Tests"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 42 - "section.py"
Cohesion: 0.18
Nodes (9): Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Unit axis, or ``None`` for a custom direction., Which side of the plane survives the cut., SectionAxis, SectionMode (+1 more)

### Community 43 - "Measurement"
Cohesion: 0.09
Nodes (26): Measurement, A straight distance between two points on the model surface., Distance in scene units., Name of the attribute a handle edits, for building an undo command., _coerce(), decode(), encode(), Any (+18 more)

### Community 44 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 45 - "wakelock.py"
Cohesion: 0.22
Nodes (7): _Backend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The backend for this machine, or a do-nothing one if it cannot be had., A way of asking one platform to stay awake., Ask for sleep to be held off., Withdraw the request.

### Community 46 - "test_spatial.py"
Cohesion: 0.33
Nodes (8): _grid(), The picking accelerator: it must be fast without changing any answer., A bumpy height field, so rays hit different triangles at different depths., The pruned candidate set must never miss the true intersection., test_a_ray_that_misses_the_model_is_pruned_away(), test_every_triangle_lands_in_exactly_one_leaf(), test_the_index_finds_the_triangle_a_ray_actually_hits(), test_the_index_is_built_once_and_kept()

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
Cohesion: 0.21
Nodes (5): Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block.

### Community 52 - "ViewerState"
Cohesion: 0.19
Nodes (6): QObject, Take the display unit from the file when the format declares one. Only glTF…, Everything the viewer displays, plus change notifications., Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, ViewerState

### Community 53 - "AnnotatePanel"
Cohesion: 0.24
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 54 - "_MacBackend"
Cohesion: 0.33
Nodes (3): c_void_p, _MacBackend, An IOKit power assertion, held by id until it is released.

### Community 55 - "Path"
Cohesion: 0.29
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 56 - "settings.py"
Cohesion: 0.06
Nodes (26): PlaneMode, PlaneSettings, Enum, str, Serialisable description of how the object should be shaded. Every value here…, How the plane directions are arrived at. ``shader_id`` must stay in sync with…, Discretisation of the shading normals into the planes of the form. A sculptor…, How much of a turn in the surface one plane covers, in degrees. Linear in… (+18 more)

### Community 57 - ".__init__"
Cohesion: 0.22
Nodes (4): QScrollArea, Single-key shortcuts, scoped so they never eat text input. They only fire while…, Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, scrollable()

### Community 58 - "orientation.py"
Cohesion: 0.19
Nodes (8): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis, ModelPanel, What was imported and which way up it should stand., Turns the model the right way up and reports what came out of the file.

### Community 59 - "stroke_renderer.py"
Cohesion: 0.24
Nodes (10): build_segment_vertices(), build_vertices(), _expand(), ndarray, Geometry for the surface annotations and the cross-section contour. Strokes are…, Replace the buffer contents with a prepared vertex block., Expand strokes into the triangle soup the stroke shader expects. Every segment…, Expand loose ``(n, 2, 3)`` segments -- the section contour -- the same way. The… (+2 more)

### Community 60 - "RemoveItem"
Cohesion: 0.22
Nodes (3): Any, Delete the item at ``index``, putting it back in place on undo., RemoveItem

### Community 61 - "SliderSpin"
Cohesion: 0.29
Nodes (4): QWidget, A float slider paired with a spin box, kept in sync. The slider works in…, Re-scale the control, e.g. once a model's size is known., SliderSpin

### Community 62 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 63 - "QTreeWidgetItem"
Cohesion: 0.28
Nodes (5): QIcon, QTreeWidgetItem, lock_icon(), A padlock, shut or hanging open. Open reads as "this measurement will move if…, Commit a renamed or re-checked row, if anything actually changed.

### Community 64 - "SetAttributes"
Cohesion: 0.31
Nodes (4): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable.

### Community 65 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 66 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 67 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Six small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 68 - "LightSettings"
Cohesion: 0.40
Nodes (4): LightSettings, Material parameters shared by the analytic shading modes., A key light, an opposing fill and a hemispherical ambient term., SurfaceSettings

### Community 69 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): QStyledItemDelegate, _NameOnlyDelegate, Allows in-place editing of the name column only.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `plane_axes`, `raycast_mesh`, `Bounds`, `mesh_renderer.py`, `OrientationSettings`, `gltf_loader.py`, `main_window.py`, `TriangleIndex`, `plane_axes.py`, `MeshBuffers`, `core/__init__.py`, `obj_loader.py`, `CHANGELOG.md`, `.apply_session`, `SectionSettings`, `section.py`, `test_spatial.py`, `ViewerState`, `._move_marks`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera` to `test_camera.py`, `ViewportOverlay`, `raycast_mesh`, `Bounds`, `SceneRenderer`, `ndarray`, `mesh_renderer.py`, `Snapped Orbit Tests`, `Measurement`, `README.md`, `main_window.py`, `Screen-to-World Panning`, `ViewerState`, `BookmarkStore`, `NavigationController`, `core/__init__.py`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport Widget` to `AnnotateTool`, `MainWindow`, `ViewportOverlay`, `main_window.py`, `ViewerState`, `.__init__`, `NavigationController`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `MainWindow` (e.g. with `ViewerState` and `UpdateChecker`) actually correct?**
  _`MainWindow` has 3 INFERRED edges - model-reasoned connections that need verification._