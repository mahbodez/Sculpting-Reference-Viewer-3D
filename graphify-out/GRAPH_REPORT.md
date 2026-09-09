# Graph Report - reference-viewer  (2026-09-09)

## Corpus Check
- 82 files · ~255,774 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1857 nodes · 4029 edges · 81 communities (78 shown, 3 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 190 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `2e75ea44`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Stroke
- application.py
- Release
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
- form_group
- GeometryTarget
- CameraPanel
- ball
- ShaderProgram
- ViewportOverlay
- block
- MeasurePanel
- BookmarkStore
- NavigationController
- SectionSettings
- wakelock.py
- raycast_mesh
- Measurement
- SliderSpin
- Panel
- test_camera.py
- test_plane_clusters.py
- WakeLock
- plane_volume.py
- History
- update_check.py
- _ScreenSaverBackend
- mesh_io.py
- test_navigation.py
- .from_dict
- main_window.py
- UpdateChecker
- _WindowsBackend
- obj_loader.py
- PlaneAxes
- Agent Graph-First Instructions
- Texture2D
- _MacBackend
- shaders.py
- RemoveItem
- .pan
- SetAttributes
- settings.py
- MeasureTool
- plane_clusters.py
- plane_count
- core/__init__.py
- refview/__init__.py
- Path
- .__init__
- test_the_joins_never_turn_the_clay_into_a_cast_of_the_model
- MatcapPanel
- test_session.py
- Camera
- test_relaxing_settles_the_clay_and_leaves_the_stone_alone
- MeshLoadError
- .ortho_half_height
- Mesh
- plane_regions
- load_matcap_pixels
- sculpt_mesh
- .plane_point
- matcap_panel.py
- Coefficients
- _create_splash
- rounded
- PlaneSettings
- edge_use

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 105 edges
2. `Camera` - 71 edges
3. `Viewport` - 48 edges
4. `MainWindow` - 46 edges
5. `ViewerState` - 46 edges
6. `SceneRenderer` - 42 edges
7. `plane_regions()` - 35 edges
8. `PlaneSettings` - 34 edges
9. `Stroke` - 33 edges
10. `sculpt_mesh()` - 32 edges

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

## Communities (81 total, 3 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.06
Nodes (37): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+29 more)

### Community 1 - "application.py"
Cohesion: 0.14
Nodes (16): ArgumentParser, Namespace, QApplication, _apply_startup_arguments(), build_parser(), main(), Command-line entry point and application bootstrap., Open whatever the command line asked for, falling back to sane defaults. (+8 more)

### Community 2 - "Release"
Cohesion: 0.18
Nodes (12): The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, is_skipped(), QWidget, Background release check and the notice it puts in front of the artist. The…, Whether the artist already dismissed this exact version., Offer the release page, with the option never to be asked again. (+4 more)

### Community 3 - "Viewport"
Cohesion: 0.07
Nodes (16): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current., Drop whatever gesture is half-finished, without disarming the tool., Record the finished drag as a single undo step. (+8 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - "AnnotateTool"
Cohesion: 0.09
Nodes (19): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+11 more)

### Community 6 - "MainWindow"
Cohesion: 0.10
Nodes (10): QAction, QMainWindow, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., The document this window edits., Keep the menu entry agreeing with the panel's own checkbox., Keep the panel button and the menu entry agreeing with the tool. (+2 more)

### Community 7 - "ViewerState"
Cohesion: 0.10
Nodes (15): ndarray, Path, QObject, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements and…, Rotate the measurements and annotations onto the turned model. A point sits at…, Take the display unit from the file when the format declares one. Only glTF… (+7 more)

### Community 8 - "TriangleIndex"
Cohesion: 0.10
Nodes (22): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., Build the index from expanded triangle corners, shape ``(T, 3, 3)``. (+14 more)

### Community 9 - "test_plane_solids.py"
Cohesion: 0.09
Nodes (21): box(), Blocking a form in out of its planes, as stone is cut and as clay is built.…, A hull cut from the surface itself, rather than from the corners the lattice…, Six directions make a box however well they were chosen, and a box is no use as…, The two halves of what the seam-filler is for, and the first is why it is safe…, A thumb adds clay to a seam; it must not shave the block beside it. A corner of…, What the size of the filter buys, and why it is worth asking for. The fill…, Every lump is written into the lattice over its own bounding box only, so a box… (+13 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.12
Nodes (21): Everything the viewport needs in order to draw a frame., RenderSettings, light_directions(), normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.… (+13 more)

### Community 11 - "ShadingMode"
Cohesion: 0.12
Nodes (9): LightSettings, Material parameters shared by the analytic shading modes., Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., A key light, an opposing fill and a hemispherical ambient term., ShadingMode, SurfaceSettings, Dockable control panels. (+1 more)

### Community 12 - "mesh_renderer.py"
Cohesion: 0.11
Nodes (27): Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., look_at(), normalize(), orthographic() (+19 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.09
Nodes (25): OrientationSettings, Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., UpAxis (+17 more)

### Community 14 - "MeshBuffers"
Cohesion: 0.13
Nodes (6): MeshBuffers, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Whichever geometry is standing for the model this frame., Vertex/index buffers for one mesh, bound through a single VAO., Forget the contents without releasing the buffer objects.

### Community 15 - "README.md"
Cohesion: 0.10
Nodes (25): High Quality shading mode (1.1.0), numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix (+17 more)

### Community 16 - "gltf_loader.py"
Cohesion: 0.13
Nodes (26): _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry(), _primitives(), ndarray (+18 more)

### Community 17 - "form_group"
Cohesion: 0.11
Nodes (21): QFormLayout, QFrame, QGroupBox, Shared plumbing for the dockable side panels., Projection settings, standard views and named camera bookmarks., Measurement list and display options., Cross-section controls: the cutting plane, what it keeps and how it reads., collapsible_group() (+13 more)

### Community 18 - "GeometryTarget"
Cohesion: 0.08
Nodes (17): bind_default(), ColorTarget, current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the… (+9 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "ball"
Cohesion: 0.17
Nodes (12): ball(), The one thing the additive mode rests on, asked of the lump rather than of the…, Left to itself a facing that no single point of the wall is holding back runs…, A join starts life as the hull of two lumps, which is a shape that pokes out of…, A closed sphere: wrapped at the seam, capped at both poles., AutoSmooth reads the normals of a form that has already been built, so it must…, test_a_lump_is_held_to_the_material_it_was_pressed_into(), test_a_lump_never_grows_out_through_the_model() (+4 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.12
Nodes (9): OpenGL rendering layer: shader programs, textures and the scene renderer., ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError (+1 more)

### Community 22 - "ViewportOverlay"
Cohesion: 0.22
Nodes (14): QColor, QPainter, QPointF, project_visible(), QFont, A square grip, so an editable end reads differently from a fixed one., Preview the gesture under way; finished strokes are drawn in 3D., The cursor ring: the eraser's reach, or the width of the brush. (+6 more)

### Community 23 - "block"
Cohesion: 0.20
Nodes (10): ndarray, Points spread over the model closely enough for a lattice to feel it. The…, surface_seeds(), block(), A closed box with hard edges, each face cut into a grid of triangles., Counting crossings is exact on a closed surface and meaningless on anything…, A box is six triangles the size of the whole thing; the lattice has to feel it…, test_a_form_already_made_of_flats_is_left_about_where_it_was() (+2 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.14
Nodes (8): QTreeWidgetItem, MeasurePanel, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn.

### Community 25 - "BookmarkStore"
Cohesion: 0.13
Nodes (7): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., test_bookmarks_cycle_and_wrap()

### Community 26 - "NavigationController"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "SectionSettings"
Cohesion: 0.08
Nodes (29): Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, The direction the section plane faces. (+21 more)

### Community 28 - "wakelock.py"
Cohesion: 0.22
Nodes (7): _Backend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The backend for this machine, or a do-nothing one if it cannot be had., A way of asking one platform to stay awake., Ask for sleep to be held off., Withdraw the request.

### Community 29 - "raycast_mesh"
Cohesion: 0.14
Nodes (21): Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``. (+13 more)

### Community 30 - "Measurement"
Cohesion: 0.12
Nodes (10): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+2 more)

### Community 31 - "SliderSpin"
Cohesion: 0.05
Nodes (24): Cross-section tool (1.1.0), QPushButton, AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle., Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the… (+16 more)

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
Cohesion: 0.17
Nodes (13): Holds sleep off while the window that owns it is the one in front. The class…, WakeLock, Broken, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do., A platform that refuses, the way an old or locked-down one might., The viewer must open and close normally on a machine that says no., Recorder (+5 more)

### Community 36 - "plane_volume.py"
Cohesion: 0.05
Nodes (82): _axes(), _back_inside(), _balloon(), block_bounds(), block_field(), blocks(), _box_facings(), carve() (+74 more)

### Community 37 - "History"
Cohesion: 0.09
Nodes (20): Camera motion is deliberately not undoable, AddItem, Append an item to a document list., Command, History, One reversible change, named for the undo menu., A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive… (+12 more)

### Community 38 - "update_check.py"
Cohesion: 0.14
Nodes (22): check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed). (+14 more)

### Community 39 - "_ScreenSaverBackend"
Cohesion: 0.22
Nodes (4): The freedesktop screensaver service, which hands back a cookie., Hold sleep off, or stop holding it, whichever is not already true., Drop the request, if one is out. Safe to call more than once., _ScreenSaverBackend

### Community 40 - "mesh_io.py"
Cohesion: 0.16
Nodes (17): load_mesh(), Path, One entry point for every mesh format the viewer reads. Callers ask for a path…, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported() (+9 more)

### Community 41 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 42 - ".from_dict"
Cohesion: 0.29
Nodes (3): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., test_serialisation_round_trip()

### Community 43 - "main_window.py"
Cohesion: 0.08
Nodes (27): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, What the annotate tool does with a drag. The first three describe the shape a…, Named camera positions the artist can jump between while sculpting., The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that… (+19 more)

### Community 44 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 45 - "_WindowsBackend"
Cohesion: 0.25
Nodes (5): skipif, ``SetThreadExecutionState``: a flag on this thread, not a handle. The flags…, _WindowsBackend, The flag the viewer sets is the one Windows reports back afterwards., test_windows_really_sets_the_execution_state()

### Community 46 - "obj_loader.py"
Cohesion: 0.12
Nodes (28): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic(), load_obj(), ObjLoadError (+20 more)

### Community 47 - "PlaneAxes"
Cohesion: 0.11
Nodes (15): _empty(), PlaneAxes, PlaneSet, ndarray, One level of a fit: the planes the shader is to quantise against. A plane is a…, A level with no place in it: nearest direction wins, as before., The planes a model falls into, at every count. Built once per mesh and per…, The best ``count`` planes, or as many as the model supports. A model whose… (+7 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "Texture2D"
Cohesion: 0.10
Nodes (10): Fill the shader's table with a level, if it is not already in it., Replace the annotation geometry; pass an empty list to hide it., DataTexture, default_matcap_pixels(), ndarray, An RGBA8 2D texture with clamped edges and mipmapped minification., A neutral studio matcap, used before the user picks one., A small RGBA32F table the shader reads exact values out of. Not a picture:… (+2 more)

### Community 50 - "_MacBackend"
Cohesion: 0.33
Nodes (3): c_void_p, _MacBackend, An IOKit power assertion, held by id until it is released.

### Community 51 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Six small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 52 - "RemoveItem"
Cohesion: 0.33
Nodes (4): Delete the item at ``index``, putting it back in place on undo., RemoveItem, Deletion goes through the undo stack, so the store only tracks position., test_deleting_a_bookmark_moves_the_cycling_position()

### Community 54 - "SetAttributes"
Cohesion: 0.16
Nodes (5): Any, Assign one or more attributes on an object, remembering the old values.…, Swap the whole contents of a document list. Used for bulk edits -- clearing the…, ReplaceItems, SetAttributes

### Community 55 - "settings.py"
Cohesion: 0.13
Nodes (19): Reading the planes of a form out of the model's own normals. The grid quantiser…, block_count(), piece_count(), Handing the planes of a fit to the thing that actually works the volume. The…, How many blocks a count of planes asks the stone to be cut into. One at the…, How many lumps a count of planes asks the clay to be built out of. The masses…, How many solids the form is made of, whichever way it is being worked., solid_count() (+11 more)

### Community 56 - "MeasureTool"
Cohesion: 0.12
Nodes (10): Handle, MeasureTool, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., Where a click at ``(x, y)`` would put a point. With free placement the point… (+2 more)

### Community 57 - "plane_clusters.py"
Cohesion: 0.08
Nodes (37): How much surface each vertex stands for: a third of each triangle on it.…, vertex_weights(), _compact(), _consensus(), _cut(), _first_planes(), _fit(), flatness() (+29 more)

### Community 58 - "plane_count"
Cohesion: 0.12
Nodes (12): _along(), lattice_fineness(), plane_count(), Where a detail setting sits on its slider, 0 to 1., How much finer than usual a detail setting asks the lattice to be. One at the…, How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., How much of a turn in the surface one plane covers, in degrees. Linear in…, How many planes a mode fitted to the model keeps. The climb from two planes to… (+4 more)

### Community 59 - "core/__init__.py"
Cohesion: 0.09
Nodes (25): Qt-free geometry, camera and document model for the reference viewer., Bounds, _gathered(), MeshUnits, ndarray, Triangle-mesh containers shared by the loader, the renderer and picking., Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations… (+17 more)

### Community 60 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 61 - "Path"
Cohesion: 0.29
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 62 - ".__init__"
Cohesion: 0.22
Nodes (4): QScrollArea, Single-key shortcuts, scoped so they never eat text input. They only fire while…, Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, scrollable()

### Community 63 - "test_the_joins_never_turn_the_clay_into_a_cast_of_the_model"
Cohesion: 0.50
Nodes (4): flatness(), The share of the surface lying in the twenty commonest directions. A form made…, Filling the seams is the point; filling the model is not. A ball is where the…, test_the_joins_never_turn_the_clay_into_a_cast_of_the_model()

### Community 64 - "MatcapPanel"
Cohesion: 0.27
Nodes (4): MatcapPanel, Rebuild the thumbnail list from the resources folder., Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…

### Community 65 - "test_session.py"
Cohesion: 0.10
Nodes (22): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Path (+14 more)

### Community 66 - "Camera"
Cohesion: 0.11
Nodes (13): Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling… (+5 more)

### Community 67 - "test_relaxing_settles_the_clay_and_leaves_the_stone_alone"
Cohesion: 0.50
Nodes (4): How far each point sits from the middle of its neighbours, as a share of the…, The relax is a pass over the finished surface rather than anything the volume…, roughness(), test_relaxing_settles_the_clay_and_leaves_the_stone_alone()

### Community 68 - "MeshLoadError"
Cohesion: 0.11
Nodes (24): Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, STL and glTF import (1.1.0), Units are adopted, never guessed (+16 more)

### Community 70 - "Mesh"
Cohesion: 0.17
Nodes (8): Mesh, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, The mesh's normals, made unit, with anything unusable recomputed., unit_normals(), fixture, quad(), Two triangles covering the unit square on the z = 0 plane.

### Community 71 - "plane_regions"
Cohesion: 0.10
Nodes (29): plane_regions(), Break the surface into patches and merge them back into planes., dumbbell(), Two balls of different size, far enough apart to be two masses., Enclosed volume, by the divergence theorem over the triangles., One block is the block of stone: a single hull round the whole model, bridging…, Every step of the slider is another cut, and a cut can only take stone off. Not…, Every step of the slider lays another lump in, and a lump can only add… (+21 more)

### Community 72 - "load_matcap_pixels"
Cohesion: 0.18
Nodes (20): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+12 more)

### Community 74 - "sculpt_mesh"
Cohesion: 0.15
Nodes (18): auto_smooth(), A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, How finely the model has to be sampled for the lattice it will be read on., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, The stand-in these settings ask for, or ``None`` for the model itself., sculpt_mesh(), seed_spacing(), parametrize (+10 more)

### Community 76 - "matcap_panel.py"
Cohesion: 0.31
Nodes (11): available_matcaps(), _bundled_root(), image_path(), matcap_dir(), model_dir(), Path, Locations of the bundled resources. ``REFVIEW_RESOURCES`` overrides the search,…, Return PyInstaller's extracted application directory when frozen. (+3 more)

### Community 79 - "Coefficients"
Cohesion: 0.12
Nodes (13): Coefficients, What each block of the design matrix counts for, against the normals. A fit…, Whether anything but the normals is being read at all., fit_planes(), The planes of ``mesh`` under ``mode``; empty where the mode needs none., MatcapSettings, PlaneMode, How the plane directions are arrived at. ``shader_id`` must stay in sync with… (+5 more)

### Community 80 - "_create_splash"
Cohesion: 0.20
Nodes (11): QIcon, QPixmap, QSplashScreen, _create_splash(), _fitted_title_font(), QFont, Largest title font that still draws the whole app name inside ``width``., lock_icon() (+3 more)

### Community 81 - "rounded"
Cohesion: 0.40
Nodes (5): MonkeyPatch, coarse_lattice(), fixture, Read every model on a small lattice, so the suite stays quick., rounded()

### Community 82 - "PlaneSettings"
Cohesion: 0.07
Nodes (26): PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor…, The grid step, in cube-face coordinates, that gives that span. A cell of this…, Roughly how much of a turn one of those planes covers, in degrees., The plane size of whichever mode is running., Roughly how much of a turn one of those planes covers, in degrees., Whether the shader should be rounding normals onto planes., Whether a planar stand-in should be built and drawn in place of the model. (+18 more)

### Community 92 - "edge_use"
Cohesion: 0.40
Nodes (5): edge_use(), ndarray, Which point each vertex really is, once copies of a position are one point., Edges used once, edges used more than twice, and edges in all. Once would mean…, welded()

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `plane_axes`, `ViewerState`, `TriangleIndex`, `test_plane_solids.py`, `mesh_renderer.py`, `OrientationSettings`, `MeshBuffers`, `gltf_loader.py`, `ball`, `block`, `SectionSettings`, `raycast_mesh`, `test_plane_clusters.py`, `plane_volume.py`, `mesh_io.py`, `main_window.py`, `obj_loader.py`, `PlaneAxes`, `Texture2D`, `settings.py`, `plane_clusters.py`, `core/__init__.py`, `test_the_joins_never_turn_the_clay_into_a_cast_of_the_model`, `test_relaxing_settles_the_clay_and_leaves_the_stone_alone`, `MeshLoadError`, `plane_regions`, `sculpt_mesh`, `Coefficients`, `rounded`, `edge_use`?**
  _High betweenness centrality (0.177) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera` to `test_camera.py`, `test_session.py`, `.ortho_half_height`, `ViewerState`, `test_navigation.py`, `.from_dict`, `main_window.py`, `mesh_renderer.py`, `SceneRenderer`, `README.md`, `RemoveItem`, `.pan`, `ViewportOverlay`, `BookmarkStore`, `NavigationController`, `core/__init__.py`, `raycast_mesh`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `Panel`, `Viewport`, `MainWindow`, `main_window.py`, `OrientationSettings`, `README.md`, `form_group`, `ViewportOverlay`, `MeasureTool`, `.__init__`?**
  _High betweenness centrality (0.055) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `MainWindow` (e.g. with `ViewerState` and `UpdateChecker`) actually correct?**
  _`MainWindow` has 3 INFERRED edges - model-reasoned connections that need verification._