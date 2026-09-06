# Graph Report - reference-viewer  (2026-09-06)

## Corpus Check
- 79 files · ~220,497 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1559 nodes · 3360 edges · 72 communities (69 shown, 3 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 162 edges (avg confidence: 0.63)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `97a593ec`
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
- core/__init__.py
- Bounds
- SceneRenderer
- Camera
- mesh_renderer.py
- OrientationSettings
- .copy
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
- mesh.py
- viewport.py
- ShadingPanel
- test_mesh_io.py
- test_camera.py
- test_plane_clusters.py
- WakeLock
- CHANGELOG.md
- ViewerState
- update_check.py
- SectionSettings
- SectionPanel
- Snapped Orbit Tests
- section.py
- state.py
- UpdateChecker
- wakelock.py
- test_spatial.py
- _ScreenSaverBackend
- Agent Graph-First Instructions
- _WindowsBackend
- Panel
- Screen-to-World Panning
- ._step
- AnnotatePanel
- _MacBackend
- Path
- settings.py
- plane_clusters.py
- orientation.py
- obj_loader.py
- SetAttributes
- load_obj
- refview/__init__.py
- PlaneSettings
- ndarray
- PlaneMode
- decode
- ._start_update_check
- LightSettings
- .from_dict
- Projection
- PlanesPanel

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 82 edges
2. `Camera` - 71 edges
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
- `Every document edit is a command` --rationale_for--> `AddItem`  [EXTRACTED]
  README.md → src/refview/core/commands.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The bundled matcap set** — resources_matcaps_clay_terracotta_matcap, resources_matcaps_charcoal_matcap, resources_matcaps_jade_matcap, resources_matcaps_steel_matcap, resources_matcaps_studio_white_matcap, resources_matcaps_wax_skin_matcap, tools_generate_matcaps_matcappreset, tools_generate_matcaps_render [INFERRED 0.85]
- **The four generic undo commands** — src_refview_core_commands_setattributes, src_refview_core_commands_additem, src_refview_core_commands_removeitem, src_refview_core_commands_replaceitems, src_refview_core_history_command, readme_every_edit_is_a_command [EXTRACTED 1.00]
- **Windows binary-compatibility decisions** — readme_pyside6_pinned_below_68, environment_pip_installed_binaries, environment_python_311, github_workflows_release_pyinstaller_build [INFERRED 0.75]

## Communities (72 total, 3 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.06
Nodes (37): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+29 more)

### Community 1 - "application.py"
Cohesion: 0.05
Nodes (54): ArgumentParser, Color, Namespace, QApplication, QPixmap, QSplashScreen, Charcoal matcap, Terracotta clay matcap (+46 more)

### Community 2 - "Release"
Cohesion: 0.18
Nodes (15): check_for_update(), fetch_latest_release(), RuntimeError, The release could not be looked up (offline, rate limited, malformed)., The newest published release, as GitHub describes it., Return the newest published release, or raise :class:`UpdateCheckError`., The newest release when it is later than ``current_version``, else ``None``., Release (+7 more)

### Community 3 - "Viewport Widget"
Cohesion: 0.07
Nodes (15): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current., Drop whatever gesture is half-finished, without disarming the tool., Record the finished drag as a single undo step., Rub out the stroke points under the eraser, live. (+7 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - "AnnotateTool"
Cohesion: 0.06
Nodes (31): Handle, AnnotateMode, AnnotationSettings, Enum, str, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a… (+23 more)

### Community 6 - "MainWindow"
Cohesion: 0.08
Nodes (11): QAction, QMainWindow, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits., Keep the menu entry agreeing with the panel's own checkbox. (+3 more)

### Community 7 - "ViewportOverlay"
Cohesion: 0.11
Nodes (22): QColor, QPainter, QPointF, MeasureTool, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed… (+14 more)

### Community 8 - "core/__init__.py"
Cohesion: 0.14
Nodes (22): Qt-free geometry, camera and document model for the reference viewer., Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays. (+14 more)

### Community 9 - "Bounds"
Cohesion: 0.18
Nodes (15): Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray, A turntable-style disc the model can stand on. A ground plane gives the eye… (+7 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.10
Nodes (22): bind_default(), current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., Restore a framebuffer captured with :func:`current_framebuffer`., normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the annotation geometry; pass an empty list to hide it. (+14 more)

### Community 11 - "Camera"
Cohesion: 0.15
Nodes (9): Camera, ndarray, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling…, A look-at camera with orbit / pan / zoom behaviour. The orthographic extent is…, Vertical half-extent of the frustum at the focal plane. (+1 more)

### Community 12 - "mesh_renderer.py"
Cohesion: 0.13
Nodes (27): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-…, Return ``v`` scaled to unit length, or ``fallback`` for a zero vector. (+19 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 14 - ".copy"
Cohesion: 0.17
Nodes (5): Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Move the camera so ``bounds`` fills the view, keeping the direction., Point the camera along ``direction``, measured object-to-eye., Adopt the pose of ``other`` without replacing this instance.

### Community 15 - "README.md"
Cohesion: 0.09
Nodes (24): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, refview (+16 more)

### Community 16 - "gltf_loader.py"
Cohesion: 0.12
Nodes (28): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry() (+20 more)

### Community 17 - "main_window.py"
Cohesion: 0.08
Nodes (29): QFormLayout, QGroupBox, QPushButton, QScrollArea, MatcapLoadError, RuntimeError, Raised when an image cannot be used as a matcap., Application window: viewport, docked panels, menus and shortcuts. (+21 more)

### Community 18 - "GeometryTarget"
Cohesion: 0.09
Nodes (13): ColorTarget, DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the…, Fail loudly on an unusable attachment rather than rendering nothing. An…, Shared lifetime handling for a framebuffer with one attachment. The GL objects… (+5 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "TriangleIndex"
Cohesion: 0.17
Nodes (12): Picking about a hundred times faster, Morton-curve leaf boxes for picking, _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., Build the index from expanded triangle corners, shape ``(T, 3, 3)``., Triangle indices worth intersecting for this ray, possibly empty. (+4 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.12
Nodes (10): ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload an ``(n, 3)`` array into a ``vec3[]`` uniform in one call., Upload an ``(n, 4)`` array into a ``vec4[]`` uniform in one call., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform… (+2 more)

### Community 22 - "plane_axes.py"
Cohesion: 0.12
Nodes (15): _empty(), PlaneAxes, PlaneSet, ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, The planes a model falls into, at every count. Built once per mesh and per…, The best ``count`` planes, or as many as the model supports. A model whose…, How much surface each vertex stands for: a third of each triangle on it.… (+7 more)

### Community 23 - "MeshBuffers"
Cohesion: 0.09
Nodes (11): OpenGL rendering layer: shader programs, textures and the scene renderer., MeshBuffers, Replace the ground disc; pass ``None`` to hide it., Vertex/index buffers for one mesh, bound through a single VAO., Forget the contents without releasing the buffer objects., default_matcap_pixels(), ndarray, Matcap texture loading and upload. (+3 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.12
Nodes (11): QIcon, QTreeWidgetItem, lock_icon(), A padlock, shut or hanging open. Open reads as "this measurement will move if…, MeasurePanel, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed. (+3 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.12
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Deletion goes through the undo stack, so the store only tracks position., test_bookmarks_cycle_and_wrap() (+1 more)

### Community 26 - "NavigationController"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "History"
Cohesion: 0.09
Nodes (21): Camera motion is deliberately not undoable, AddItem, Append an item to a document list., Command, History, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, One reversible change, named for the undo menu., A bounded undo/redo stack. (+13 more)

### Community 28 - "Mesh"
Cohesion: 0.18
Nodes (6): Mesh, Picking accelerator, built on first use and kept for the mesh's life., Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, _load_generic(), Line-by-line reader for files the fast path declines.

### Community 29 - "mesh.py"
Cohesion: 0.13
Nodes (21): STL corner welding, compute_vertex_normals(), One entry point for every mesh format the viewer reads. Callers ask for a path…, MeshLoadError, RuntimeError, Triangle-mesh containers shared by the loader, the renderer and picking., Raised when a file cannot be interpreted as a triangle mesh., Area-weighted smooth vertex normals for an indexed triangle soup. (+13 more)

### Community 30 - "viewport.py"
Cohesion: 0.08
Nodes (19): Freehand annotations painted onto the model surface. A stroke is a polyline of…, Measurement, MeasurementStore, ndarray, Named point-to-point measurements and their presentation options., The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface. (+11 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.24
Nodes (6): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., ShadingPanel

### Community 32 - "test_mesh_io.py"
Cohesion: 0.22
Nodes (14): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one(), test_binary_stl_welds_shared_corners() (+6 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.07
Nodes (46): angle_deg(), bent_plate(), cube(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What…, How far the least well served of ``wanted`` is from anything offered. (+38 more)

### Community 35 - "WakeLock"
Cohesion: 0.17
Nodes (13): Holds sleep off while the window that owns it is the one in front. The class…, WakeLock, Broken, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do., A platform that refuses, the way an old or locked-down one might., The viewer must open and close normally on a machine that says no., Recorder (+5 more)

### Community 36 - "CHANGELOG.md"
Cohesion: 0.29
Nodes (6): Cross-section tool (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4

### Community 37 - "ViewerState"
Cohesion: 0.13
Nodes (13): ndarray, Path, QObject, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements and…, Rotate the measurements and annotations onto the turned model. A point sits at…, Take the display unit from the file when the format declares one. Only glTF… (+5 more)

### Community 38 - "update_check.py"
Cohesion: 0.19
Nodes (15): is_newer(), _padded(), parse_version(), Ask GitHub whether a newer release exists. The check is deliberately small and…, Numeric components of ``text``, or ``None`` when it is not a version. A pre-…, Whether ``candidate`` is a strictly later version than ``current``., Pull the tag and page link out of a GitHub release document., release_from_payload() (+7 more)

### Community 39 - "SectionSettings"
Cohesion: 0.23
Nodes (13): How the model is cut open, and how the cut is drawn., SectionSettings, _box(), Cutting planes, the contour they produce and the pedestal under the model., A closed axis-aligned cube centred on the origin., The contour of a plane through a cube is its cross-section outline., test_a_custom_normal_is_normalised(), test_a_disabled_section_cuts_with_nothing() (+5 more)

### Community 40 - "SectionPanel"
Cohesion: 0.23
Nodes (5): Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 41 - "Snapped Orbit Tests"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 42 - "section.py"
Cohesion: 0.11
Nodes (16): Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, The direction the section plane faces. (+8 more)

### Community 43 - "state.py"
Cohesion: 0.08
Nodes (27): Named camera positions the artist can jump between while sculpting., MeasurementSettings, How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., Path, Persisted viewer state: camera, shading, measurements and bookmarks., A snapshot of everything worth keeping between runs., Session file that sits beside a model, e.g. ``bust.refview.json``. (+19 more)

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
Cohesion: 0.15
Nodes (8): QStyledItemDelegate, Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block., _NameOnlyDelegate, Allows in-place editing of the name column only.

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
Cohesion: 0.12
Nodes (13): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, MatcapSettings, Enum, str, QualitySettings, Serialisable description of how the object should be shaded. Every value here… (+5 more)

### Community 57 - "plane_clusters.py"
Cohesion: 0.08
Nodes (37): _compact(), _consensus(), _cut(), _first_planes(), _fit(), flatness(), _leaves(), neighbour_agreement() (+29 more)

### Community 58 - "orientation.py"
Cohesion: 0.21
Nodes (7): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis, ModelPanel, Turns the model the right way up and reports what came out of the file.

### Community 59 - "obj_loader.py"
Cohesion: 0.22
Nodes (14): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), ndarray, Minimal, dependency-free Wavefront OBJ reader. Only the geometry statements a…, Resolve ``v``, ``v/vt``, ``v//vn`` or ``v/vt/vn`` corners to 0-based pairs.… (+6 more)

### Community 60 - "SetAttributes"
Cohesion: 0.11
Nodes (11): Every document edit is a command, Any, The handful of undoable edits the whole application is built from.…, Assign one or more attributes on an object, remembering the old values.…, Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems (+3 more)

### Community 61 - "load_obj"
Cohesion: 0.22
Nodes (14): load_obj(), ObjLoadError, Path, Raised when a file cannot be interpreted as an OBJ mesh., Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, Negative face indices count back from the most recent vertex., test_obj_relative_indices_still_load(), OBJ parsing: normals, triangulation and index handling. (+6 more)

### Community 62 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 63 - "PlaneSettings"
Cohesion: 0.14
Nodes (9): PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor…, How much of a turn in the surface one plane covers, in degrees. Linear in…, The grid step, in cube-face coordinates, that gives that span. A cell of this…, How many planes a mode fitted to the model keeps. The slider reads straight…, Roughly how much of a turn one of those planes covers, in degrees. The…, The plane size of whichever mode is running., The line under the slider: what the setting has actually asked for. (+1 more)

### Community 64 - "ndarray"
Cohesion: 0.20
Nodes (4): ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, test_bounds_of_an_empty_point_set()

### Community 65 - "PlaneMode"
Cohesion: 0.22
Nodes (6): fit_planes(), The planes of ``mesh`` under ``mode``; empty where the mode needs none., PlaneMode, How the plane directions are arrived at. ``shader_id`` must stay in sync with…, Whether the directions are read off the model rather than imposed., The model's own planes under ``mode``, fitted once and kept.

### Community 66 - "decode"
Cohesion: 0.27
Nodes (8): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., T

### Community 67 - "._start_update_check"
Cohesion: 0.29
Nodes (4): Ask GitHub for the newest release in the background. The startup check is…, QWidget, show_failure_dialog(), show_up_to_date_dialog()

### Community 68 - "LightSettings"
Cohesion: 0.40
Nodes (4): LightSettings, Material parameters shared by the analytic shading modes., A key light, an opposing fill and a hemispherical ambient term., SurfaceSettings

### Community 69 - ".from_dict"
Cohesion: 0.29
Nodes (3): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., test_serialisation_round_trip()

### Community 70 - "Projection"
Cohesion: 0.33
Nodes (4): Projection, Enum, str, Projection used by :class:`Camera`.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `plane_axes`, `AnnotateTool`, `core/__init__.py`, `Bounds`, `mesh_renderer.py`, `OrientationSettings`, `gltf_loader.py`, `TriangleIndex`, `plane_axes.py`, `MeshBuffers`, `mesh.py`, `test_mesh_io.py`, `test_plane_clusters.py`, `ViewerState`, `SectionSettings`, `section.py`, `state.py`, `test_spatial.py`, `plane_clusters.py`, `obj_loader.py`, `load_obj`, `ndarray`, `PlaneMode`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera` to `test_camera.py`, `.from_dict`, `AnnotateTool`, `ViewportOverlay`, `core/__init__.py`, `Bounds`, `SceneRenderer`, `state.py`, `mesh_renderer.py`, `ViewerState`, `.copy`, `README.md`, `Snapped Orbit Tests`, `Screen-to-World Panning`, `BookmarkStore`, `NavigationController`, `viewport.py`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `Viewport Widget`, `MainWindow`, `ViewportOverlay`, `state.py`, `OrientationSettings`, `README.md`, `main_window.py`, `Panel`, `._step`, `viewport.py`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `MainWindow` (e.g. with `ViewerState` and `UpdateChecker`) actually correct?**
  _`MainWindow` has 3 INFERRED edges - model-reasoned connections that need verification._