# Graph Report - reference-viewer  (2026-09-09)

## Corpus Check
- 86 files · ~265,047 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1997 nodes · 4391 edges · 101 communities (97 shown, 4 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 200 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a5073bc3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Stroke
- FilmRecorder
- main_window.py
- Viewport
- plane_axes
- AnnotateTool
- MainWindow
- ViewerState
- TriangleIndex
- test_plane_solids.py
- SceneRenderer
- ShadingMode
- mesh_renderer.py
- OrientationSettings
- MeshBuffers
- README.md
- gltf_loader.py
- SliderSpin
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
- .point
- Measurement
- ShadingPanel
- Panel
- test_camera.py
- test_plane_clusters.py
- WakeLock
- ndarray
- History
- update_check.py
- core/__init__.py
- test_mesh_io.py
- Camera
- Projection
- state.py
- UpdateChecker
- .copy
- compute_vertex_normals
- PlaneSet
- Agent Graph-First Instructions
- render/__init__.py
- orientation.py
- shaders.py
- application.py
- StrokeBuffers
- ReplaceItems
- plane_solids.py
- .handle_at
- settings.py
- plane_count
- Mesh
- clay_lumps
- Path
- scrollable
- plane_volume.py
- MatcapPanel
- test_session.py
- ndarray
- lay_bed
- MeshLoadError
- stone_field
- Command
- plane_regions
- load_matcap_pixels
- matcap_panel.py
- session.py
- viewport.py
- ColorButton
- record
- SetAttributes
- annotation.py
- _create_splash
- rounded
- PlaneSettings
- test_annotation.py
- SculptCache
- environment.yml
- release.yml
- AddItem
- .split
- RemoveItem
- Film
- Stage
- .start
- ndarray
- block_splits
- .plane_span_deg
- coarse_lattice
- unit_normals
- stage_counts
- plane_span_deg
- .clustered

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 117 edges
2. `Camera` - 71 edges
3. `PlaneSettings` - 63 edges
4. `Viewport` - 54 edges
5. `MainWindow` - 46 edges
6. `ViewerState` - 46 edges
7. `SceneRenderer` - 42 edges
8. `plane_regions()` - 39 edges
9. `ball()` - 37 edges
10. `Stroke` - 33 edges

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

## Communities (101 total, 4 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.12
Nodes (12): AnnotationStore, An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Stroke, The strokes being laid down; the overlay previews them in 2D., The surviving arc wraps past the start of the list, so the gap is rotated to… (+4 more)

### Community 1 - "FilmRecorder"
Cohesion: 0.16
Nodes (9): FilmRecorder, QObject, Whether a film is being made right now., Stop any recording in flight and forget what it was making. The thread is asked…, Let every thread finish, for shutdown. The only place waiting is the right…, The work itself, living on the worker thread., Ask the recording to end at the next stage boundary. Called from the GUI…, Keeps one recording running at a time, on a thread of its own. :attr:`grew` is… (+1 more)

### Community 2 - "main_window.py"
Cohesion: 0.19
Nodes (15): The newest published release, as GitHub describes it., Release, Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version(), Application window: viewport, docked panels, menus and shortcuts., is_skipped(), QWidget (+7 more)

### Community 3 - "Viewport"
Cohesion: 0.06
Nodes (19): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, End any film being recorded, and wait for its thread to really stop. For…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on., Cut the mesh with each section plane and expand the result to strokes. (+11 more)

### Community 4 - "plane_axes"
Cohesion: 0.10
Nodes (30): plane_axes(), A level with no place in it: nearest direction wins, as before., Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies. (+22 more)

### Community 5 - "AnnotateTool"
Cohesion: 0.11
Nodes (17): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Painting annotations onto the model surface. Every shape is laid down the same…, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+9 more)

### Community 6 - "MainWindow"
Cohesion: 0.08
Nodes (12): QAction, QMainWindow, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits., Keep the menu entry agreeing with the panel's own checkbox. (+4 more)

### Community 7 - "ViewerState"
Cohesion: 0.11
Nodes (14): ndarray, Path, Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements and…, Rotate the measurements and annotations onto the turned model. A point sits at…, Take the display unit from the file when the format declares one. Only glTF… (+6 more)

### Community 8 - "TriangleIndex"
Cohesion: 0.10
Nodes (22): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., Build the index from expanded triangle corners, shape ``(T, 3, 3)``. (+14 more)

### Community 9 - "test_plane_solids.py"
Cohesion: 0.05
Nodes (43): block(), box(), ndarray, Blocking a form in out of its planes, as stone is cut and as clay is built.…, A closed box with hard edges, each face cut into a grid of triangles., Which point each vertex really is, once copies of a position are one point., How far each point sits from the middle of its neighbours, as a share of the…, The relax is a pass over the finished surface rather than anything the volume… (+35 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.12
Nodes (21): Everything the viewport needs in order to draw a frame., RenderSettings, light_directions(), normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.… (+13 more)

### Community 11 - "ShadingMode"
Cohesion: 0.25
Nodes (3): Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode

### Community 12 - "mesh_renderer.py"
Cohesion: 0.14
Nodes (24): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-…, Return ``v`` scaled to unit length, or ``fallback`` for a zero vector. (+16 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 14 - "MeshBuffers"
Cohesion: 0.13
Nodes (6): MeshBuffers, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Whichever geometry is standing for the model this frame., Vertex/index buffers for one mesh, bound through a single VAO., Forget the contents without releasing the buffer objects.

### Community 15 - "README.md"
Cohesion: 0.18
Nodes (15): High Quality shading mode (1.1.0), Annotations drawn as widened geometry, core never imports Qt, Every document edit is a command, High Quality without ray tracing, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance (+7 more)

### Community 16 - "gltf_loader.py"
Cohesion: 0.09
Nodes (33): Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor() (+25 more)

### Community 17 - "SliderSpin"
Cohesion: 0.08
Nodes (27): QFormLayout, QFrame, QGroupBox, Shared plumbing for the dockable side panels., Dockable control panels., Measurement list and display options., Everything that acts on the shading normals rather than on the shading. Faceted…, Cross-section controls: the cutting plane, what it keeps and how it reads. (+19 more)

### Community 18 - "GeometryTarget"
Cohesion: 0.08
Nodes (17): bind_default(), ColorTarget, current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the… (+9 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "test_plane_film.py"
Cohesion: 0.10
Nodes (28): coarse_lattice(), film_of(), fixture, MonkeyPatch, parametrize, Scrubbing through the making of a form, rather than only arriving at it. The…, The same the other way about: a lump adds material, so the form grows., A stage is something to look at, so it has to be closed and wound out.… (+20 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "ViewportOverlay"
Cohesion: 0.11
Nodes (22): QColor, QPainter, QPointF, MeasureTool, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed… (+14 more)

### Community 23 - "PlanesPanel"
Cohesion: 0.17
Nodes (9): PlanesPanel, The line under the normals slider: what the setting has asked for., Breaks the form into planes, in the shading or in the geometry itself., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Show what this way of working needs, and put the rest away. A setting that does… (+1 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.19
Nodes (6): QTreeWidgetItem, MeasurePanel, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Lists saved measurements and controls how they are drawn.

### Community 25 - "BookmarkStore"
Cohesion: 0.10
Nodes (10): BookmarkStore, CameraBookmark, Named camera positions the artist can jump between while sculpting., A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one. (+2 more)

### Community 26 - "NavigationController"
Cohesion: 0.13
Nodes (11): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+3 more)

### Community 27 - "SectionSettings"
Cohesion: 0.08
Nodes (30): The cut interior is flooded flat, Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every… (+22 more)

### Community 28 - "SectionPanel"
Cohesion: 0.20
Nodes (7): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 29 - ".point"
Cohesion: 0.22
Nodes (5): ndarray, Closest surface intersection under the cursor, or ``None``., Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-…, Screen-to-world scale at a given depth along the view direction.

### Community 30 - "Measurement"
Cohesion: 0.12
Nodes (10): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+2 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.18
Nodes (7): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel

### Community 32 - "Panel"
Cohesion: 0.15
Nodes (8): QStyledItemDelegate, Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block., _NameOnlyDelegate, Allows in-place editing of the name column only.

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (58): angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What… (+50 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (32): c_void_p, skipif, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had. (+24 more)

### Community 36 - "ndarray"
Cohesion: 0.14
Nodes (20): _back_inside(), dual_contour(), _flat_mesh(), ndarray, The gradient of a lattice field, by central differences. Which is the direction…, Drop the loose pieces, keeping the form and anything of its size. A block is a…, Read lattice fields at places between their corners, straight-line. Nearest-…, Put anything that has drifted out of the model back onto its surface. One… (+12 more)

### Community 37 - "History"
Cohesion: 0.17
Nodes (14): History, A bounded undo/redo stack., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch(), test_commands_carry_their_channel_and_name() (+6 more)

### Community 38 - "update_check.py"
Cohesion: 0.14
Nodes (22): check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed). (+14 more)

### Community 39 - "core/__init__.py"
Cohesion: 0.12
Nodes (25): Qt-free geometry, camera and document model for the reference viewer., auto_smooth(), _gathered(), Triangle-mesh containers shared by the loader, the renderer and picking., Which group each of ``total`` things lands in, given pairs that agree. Hooking…, A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, Hit, intersects_bounds() (+17 more)

### Community 40 - "test_mesh_io.py"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

### Community 41 - "Camera"
Cohesion: 0.15
Nodes (17): Camera, Screen-to-world scale at the focal plane; identical in both modes., Slide the camera parallel to the image plane by a pixel delta., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling…, A look-at camera with orbit / pan / zoom behaviour. The orthographic extent is…, Vertical half-extent of the frustum at the focal plane., _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting. (+9 more)

### Community 42 - "Projection"
Cohesion: 0.25
Nodes (5): Projection, Enum, str, Projection used by :class:`Camera`., test_serialisation_round_trip()

### Community 43 - "state.py"
Cohesion: 0.14
Nodes (12): MeasurementSettings, Named point-to-point measurements and their presentation options., How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., NavigationSettings, How mouse gestures drive the camera., Qt user interface: the viewport widget, the panels and the main window., Two-click measuring, plus dragging the endpoints of an unlocked measurement. (+4 more)

### Community 44 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 45 - ".copy"
Cohesion: 0.17
Nodes (5): Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Move the camera so ``bounds`` fills the view, keeping the direction., Point the camera along ``direction``, measured object-to-eye., Adopt the pose of ``other`` without replacing this instance.

### Community 46 - "compute_vertex_normals"
Cohesion: 0.11
Nodes (30): compute_vertex_normals(), Area-weighted smooth vertex normals for an indexed triangle soup., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic() (+22 more)

### Community 47 - "PlaneSet"
Cohesion: 0.33
Nodes (3): PlaneSet, One level of a fit: the planes the shader is to quantise against. A plane is a…, The best ``count`` planes, or as many as the model supports. A model whose…

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "render/__init__.py"
Cohesion: 0.08
Nodes (15): OpenGL rendering layer: shader programs, textures and the scene renderer., Fill the shader's table with a level, if it is not already in it., Replace the annotation geometry; pass an empty list to hide it., DataTexture, default_matcap_pixels(), MatcapLoadError, ndarray, RuntimeError (+7 more)

### Community 50 - "orientation.py"
Cohesion: 0.19
Nodes (8): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis, ModelPanel, What was imported and which way up it should stand., Turns the model the right way up and reports what came out of the file.

### Community 51 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Six small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 52 - "application.py"
Cohesion: 0.14
Nodes (16): ArgumentParser, Namespace, QApplication, _apply_startup_arguments(), build_parser(), main(), Command-line entry point and application bootstrap., Open whatever the command line asked for, falling back to sane defaults. (+8 more)

### Community 53 - "StrokeBuffers"
Cohesion: 0.16
Nodes (12): build_segment_vertices(), build_vertices(), _expand(), ndarray, Geometry for the surface annotations and the cross-section contour. Strokes are…, A single vertex buffer holding every visible stroke., Replace the buffer contents with a prepared vertex block., Expand strokes into the triangle soup the stroke shader expects. Every segment… (+4 more)

### Community 55 - "plane_solids.py"
Cohesion: 0.18
Nodes (13): block_count(), piece_count(), Handing the planes of a fit to the thing that actually works the volume. The…, How many blocks a count of planes asks the stone to be cut into. One at the…, How many lumps a count of planes asks the clay to be built out of. The masses…, How many solids the form is made of, whichever way it is being worked., solid_count(), str (+5 more)

### Community 57 - "settings.py"
Cohesion: 0.05
Nodes (59): Coefficients, PlaneAxes, Reading the planes of a form out of the model's own normals. The grid quantiser…, The planes a model falls into, at every count. Built once per mesh and per…, How much surface each vertex stands for: a third of each triangle on it.…, What each block of the design matrix counts for, against the normals. A fit…, Whether anything but the normals is being read at all., vertex_weights() (+51 more)

### Community 58 - "plane_count"
Cohesion: 0.12
Nodes (12): _along(), lattice_fineness(), plane_count(), Where a detail setting sits on its slider, 0 to 1., How much finer than usual a detail setting asks the lattice to be. One at the…, How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., How much of a turn in the surface one plane covers, in degrees. Linear in…, How many planes a mode fitted to the model keeps. The climb from two planes to… (+4 more)

### Community 59 - "Mesh"
Cohesion: 0.08
Nodes (25): Bounds, Mesh, ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Return a copy whose bounding-box centre sits at the origin., An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero). (+17 more)

### Community 60 - "clay_lumps"
Cohesion: 0.14
Nodes (18): _box_facings(), clay_lumps(), clay_pieces(), fit_piece(), _frame(), grow_piece(), join_pieces(), piece_bounds() (+10 more)

### Community 61 - "Path"
Cohesion: 0.23
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 62 - "scrollable"
Cohesion: 0.50
Nodes (3): QScrollArea, Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, scrollable()

### Community 63 - "plane_volume.py"
Cohesion: 0.17
Nodes (15): _balloon(), block_labels(), blocks(), close_gaps(), outside_points(), Blocking a form in out of its own planes, from the outside or from a core. A…, Fill the slots the lumps leave between them, without taking clay away. The…, Grow or shrink a solid by ``reach`` cells, one axis at a time. A separable… (+7 more)

### Community 64 - "MatcapPanel"
Cohesion: 0.27
Nodes (4): MatcapPanel, Rebuild the thumbnail list from the resources folder., Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…

### Community 65 - "test_session.py"
Cohesion: 0.10
Nodes (17): Session file that sits beside a model, e.g. ``bust.refview.json``., sidecar_path(), Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., A step of the slider is worth a fixed share more planes, not a fixed number of…, The ceiling went from 64 planes to 256 without moving the slider under anyone:…, The panel edits the settings; the fit has to be told what they are., Both modes answer in degrees of turn, so the panel can just ask. (+9 more)

### Community 66 - "ndarray"
Cohesion: 0.19
Nodes (5): ndarray, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Near/far planes fitted to the scene bounding sphere.

### Community 67 - "lay_bed"
Cohesion: 0.15
Nodes (14): _axes(), encloses(), lattice(), lay_bed(), nearest_surface(), _passes(), Read the model onto a lattice, ready for solids to be laid on it., A cubic lattice covering the model with ``margin`` of room around it. Cubic… (+6 more)

### Community 68 - "MeshLoadError"
Cohesion: 0.16
Nodes (17): STL corner welding, MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., _ascii_corners(), _binary_corners(), load_stl(), ndarray (+9 more)

### Community 69 - "stone_field"
Cohesion: 0.14
Nodes (14): Bed, block_bounds(), block_field(), coarse_bounds(), point_support(), The lattice a form is worked on, and the model read onto it. Everything here…, The union of the blocks a labelling cuts the model into, and its facings. Stone…, One row of coordinates per axis over ``box``, shaped so they broadcast. (+6 more)

### Community 70 - "Command"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 71 - "plane_regions"
Cohesion: 0.09
Nodes (42): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), dumbbell(), flatness(), parametrize, Two balls of different size, far enough apart to be two masses. (+34 more)

### Community 72 - "load_matcap_pixels"
Cohesion: 0.18
Nodes (20): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+12 more)

### Community 73 - "matcap_panel.py"
Cohesion: 0.31
Nodes (11): available_matcaps(), _bundled_root(), image_path(), matcap_dir(), model_dir(), Path, Locations of the bundled resources. ``REFVIEW_RESOURCES`` overrides the search,…, Return PyInstaller's extracted application directory when frozen. (+3 more)

### Community 74 - "session.py"
Cohesion: 0.15
Nodes (15): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Path (+7 more)

### Community 75 - "viewport.py"
Cohesion: 0.20
Nodes (9): planes_for(), The stages a form passes through on its way from a block to a figure. The…, The detail setting that asks for ``solids``, or ``None`` if none does. The…, A stage as it is to be drawn, with its normals read at ``smooth``. Kept out of…, shaded(), How finely the model has to be sampled for the lattice it will be read on., seed_spacing(), Recording a form's making in the background, so the app stays usable. A film is… (+1 more)

### Community 76 - "ColorButton"
Cohesion: 0.14
Nodes (6): QPushButton, AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle., ColorButton, A swatch button that opens a colour picker. Colours are exchanged as 0-1 RGB…

### Community 77 - "record"
Cohesion: 0.23
Nodes (12): Work the form stage by stage, handing each one back as it is finished. A…, record(), carve(), _corner_facings(), facings(), fitted_facings(), The form ``directions`` leave of the model, worked one way or the other.…, Twenty-six directions round a cube, for judging how much air a block holds.… (+4 more)

### Community 78 - "SetAttributes"
Cohesion: 0.22
Nodes (5): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable.

### Community 79 - "annotation.py"
Cohesion: 0.20
Nodes (7): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a…, Surface annotation tool: brush, shape and eraser settings.

### Community 80 - "_create_splash"
Cohesion: 0.20
Nodes (11): QIcon, QPixmap, QSplashScreen, _create_splash(), _fitted_title_font(), QFont, Largest title font that still draws the whole app name inside ``width``., lock_icon() (+3 more)

### Community 81 - "rounded"
Cohesion: 0.40
Nodes (5): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick., rounded()

### Community 82 - "PlaneSettings"
Cohesion: 0.09
Nodes (31): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor…, The grid step, in cube-face coordinates, that gives that span. A cell of this…, The design-matrix settings, in the form the fitters want them., Whether the shader should be rounding normals onto planes., Whether a planar stand-in should be built and drawn in place of the model. (+23 more)

### Community 83 - "test_annotation.py"
Cohesion: 0.31
Nodes (9): line_stroke(), Surface annotations: erasing, splitting and the geometry handed to GL., A stroke running along +X, one unit apart, with +Y normals., test_a_closed_stroke_gains_the_wrapping_segment(), test_each_segment_becomes_six_vertices(), test_erasing_keeps_the_brush_and_drops_stubs(), test_erasing_nothing_reports_no_change(), test_erasing_the_middle_splits_a_stroke_in_two() (+1 more)

### Community 84 - "SculptCache"
Cohesion: 0.13
Nodes (12): Holds the working state between one turn of the sliders and the next.…, Drop everything held, so the next call starts from the fit., The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache, A model the fit cannot break down has no making to show, and says so by handing…, test_the_film_is_empty_for_a_model_with_no_planes_in_it(), The fit is the expensive part and it only goes stale when the model or the… (+4 more)

### Community 85 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 86 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 87 - "AddItem"
Cohesion: 0.22
Nodes (4): AddItem, The handful of undoable edits the whole application is built from.…, Append an item to a document list., Undo/redo stack. Every document edit is expressed as a :class:`Command` that…

### Community 88 - ".split"
Cohesion: 0.29
Nodes (5): ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., Normals padded to match the points, so callers can zip them freely., Break the stroke into the runs of points ``keep`` marks as surviving., _runs()

### Community 89 - "RemoveItem"
Cohesion: 0.29
Nodes (4): Delete the item at ``index``, putting it back in place on undo., RemoveItem, Deletion goes through the undo stack, so the store only tracks position., test_deleting_a_bookmark_moves_the_cycling_position()

### Community 90 - "Film"
Cohesion: 0.29
Nodes (4): Film, A whole making, from the coarsest stage to the one the slider asks for. Held by…, The film being recorded, or the last one finished., The film already held for ``key``, if there is one.

### Community 91 - "Stage"
Cohesion: 0.29
Nodes (4): The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage

### Community 92 - ".start"
Cohesion: 0.40
Nodes (3): QThread, Begin recording, abandoning whatever was being recorded before., A thread has really stopped, so it is safe to let go of it. Every handle to it…

### Community 93 - "ndarray"
Cohesion: 0.33
Nodes (6): _empty(), ndarray, The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to., _split(), _summarise()

### Community 94 - "block_splits"
Cohesion: 0.33
Nodes (6): block_splits(), _cuts(), _hull_air(), The corners a hull round ``points`` holds that ``points`` do not fill. The hull…, Where a block might be cut in two: a direction, and a point to pass through.…, The greedy split, with every count along the way kept. The same walk…

### Community 95 - ".plane_span_deg"
Cohesion: 0.33
Nodes (3): Roughly how much of a turn one of those planes covers, in degrees., The plane size of whichever mode is running., Roughly how much of a turn one of those planes covers, in degrees.

### Community 96 - "coarse_lattice"
Cohesion: 0.33
Nodes (6): app(), coarse_lattice(), fixture, MonkeyPatch, One Qt application for the whole run; offscreen, so CI needs no display.…, Read every model on a small lattice, so the suite stays quick.

### Community 97 - "unit_normals"
Cohesion: 0.40
Nodes (5): ndarray, The mesh's normals, made unit, with anything unusable recomputed., Points spread over the model closely enough for a lattice to feel it. The…, surface_seeds(), unit_normals()

### Community 98 - "stage_counts"
Cohesion: 0.50
Nodes (4): How many solids each stage of a film is made of. Every count from the coarsest…, stage_counts(), A slider with a thousand stops is not a slider, and a stage that differs from…, test_a_long_making_is_thinned_rather_than_left_to_crawl()

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `FilmRecorder`, `plane_axes`, `ViewerState`, `TriangleIndex`, `test_plane_solids.py`, `mesh_renderer.py`, `OrientationSettings`, `MeshBuffers`, `README.md`, `gltf_loader.py`, `test_plane_film.py`, `SectionSettings`, `test_plane_clusters.py`, `ndarray`, `core/__init__.py`, `test_mesh_io.py`, `state.py`, `compute_vertex_normals`, `PlaneSet`, `render/__init__.py`, `plane_solids.py`, `settings.py`, `plane_volume.py`, `MeshLoadError`, `stone_field`, `plane_regions`, `viewport.py`, `record`, `rounded`, `PlaneSettings`, `SculptCache`, `Film`, `Stage`, `.start`, `unit_normals`?**
  _High betweenness centrality (0.198) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `FilmRecorder`, `main_window.py`, `AnnotateTool`, `MainWindow`, `ViewerState`, `viewport.py`, `state.py`, `ViewportOverlay`, `NavigationController`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera` to `RemoveItem`, `test_camera.py`, `ndarray`, `core/__init__.py`, `Projection`, `SceneRenderer`, `mesh_renderer.py`, `.copy`, `state.py`, `README.md`, `session.py`, `ViewportOverlay`, `BookmarkStore`, `NavigationController`, `Mesh`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `PlaneSettings` (e.g. with `Film` and `Stage`) actually correct?**
  _`PlaneSettings` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 9 INFERRED edges - model-reasoned connections that need verification._