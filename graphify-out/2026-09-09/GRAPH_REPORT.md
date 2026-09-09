# Graph Report - reference-viewer  (2026-09-09)

## Corpus Check
- 82 files · ~253,410 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1846 nodes · 4011 edges · 76 communities (71 shown, 5 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 190 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d8a0d9c4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Stroke
- application.py
- main_window.py
- Viewport
- plane_axes
- AnnotateTool
- MainWindow
- ViewerState
- TriangleIndex
- test_plane_solids.py
- RenderSettings
- PlaneSettings
- camera.py
- OrientationSettings
- SceneRenderer
- README.md
- gltf_loader.py
- planes_panel.py
- mesh_renderer.py
- CameraPanel
- ball
- ShaderProgram
- ndarray
- block
- MeasurePanel
- BookmarkStore
- NavigationController
- SectionSettings
- SliderSpin
- core/__init__.py
- MeasurementStore
- ShadingPanel
- Panel
- test_camera.py
- test_plane_clusters.py
- WakeLock
- plane_volume.py
- History
- update_check.py
- decode
- SectionPanel
- test_navigation.py
- Camera
- viewport.py
- UpdateChecker
- environment.yml
- obj_loader.py
- .handle_at
- Agent Graph-First Instructions
- render/__init__.py
- release.yml
- ._build
- Projection
- AnnotatePanel
- SetAttributes
- ShadingMode
- .drag_target
- settings.py
- shaders.py
- Bounds
- Command
- Path
- ColorButton
- RemoveItem
- ReplaceItems
- test_session.py
- box
- test_relaxing_settles_the_clay_and_leaves_the_stone_alone
- .pan
- solid_count
- Mesh
- plane_regions
- .plane_point
- lock_icon
- rounded
- ._build

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 105 edges
2. `Camera` - 71 edges
3. `Viewport` - 48 edges
4. `MainWindow` - 46 edges
5. `ViewerState` - 46 edges
6. `SceneRenderer` - 42 edges
7. `plane_regions()` - 34 edges
8. `PlaneSettings` - 34 edges
9. `Stroke` - 33 edges
10. `sculpt_mesh()` - 31 edges

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

## Communities (76 total, 5 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.06
Nodes (38): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+30 more)

### Community 1 - "application.py"
Cohesion: 0.05
Nodes (54): ArgumentParser, Color, Namespace, QApplication, QPixmap, QSplashScreen, Charcoal matcap, Terracotta clay matcap (+46 more)

### Community 2 - "main_window.py"
Cohesion: 0.19
Nodes (15): The newest published release, as GitHub describes it., Release, Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version(), Application window: viewport, docked panels, menus and shortcuts., is_skipped(), QWidget (+7 more)

### Community 3 - "Viewport"
Cohesion: 0.07
Nodes (16): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current., Drop whatever gesture is half-finished, without disarming the tool., Record the finished drag as a single undo step. (+8 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - "AnnotateTool"
Cohesion: 0.10
Nodes (18): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Painting annotations onto the model surface. Every shape is laid down the same…, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+10 more)

### Community 6 - "MainWindow"
Cohesion: 0.09
Nodes (11): QAction, QMainWindow, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, Keep the menu entry agreeing with the panel's own checkbox., Keep the panel button and the menu entry agreeing with the tool. (+3 more)

### Community 7 - "ViewerState"
Cohesion: 0.06
Nodes (34): QColor, QPainter, QPointF, The document this window edits., MeasureTool, Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview. (+26 more)

### Community 8 - "TriangleIndex"
Cohesion: 0.10
Nodes (22): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., Build the index from expanded triangle corners, shape ``(T, 3, 3)``. (+14 more)

### Community 9 - "test_plane_solids.py"
Cohesion: 0.09
Nodes (25): edge_use(), flatness(), ndarray, parametrize, Blocking a form in out of its planes, as stone is cut and as clay is built.…, Which point each vertex really is, once copies of a position are one point., Edges used once, edges used more than twice, and edges in all. Once would mean…, The share of the surface lying in the twenty commonest directions. A form made… (+17 more)

### Community 10 - "RenderSettings"
Cohesion: 0.12
Nodes (17): Everything the viewport needs in order to draw a frame., RenderSettings, normal_matrix(), ndarray, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.…, The model, the pedestal under it and the flat cap over the cut., Point the shading pass at the shadow map and the occlusion buffer. (+9 more)

### Community 11 - "PlaneSettings"
Cohesion: 0.05
Nodes (31): _along(), lattice_fineness(), plane_count(), PlaneSettings, Where a detail setting sits on its slider, 0 to 1., How much finer than usual a detail setting asks the lattice to be. One at the…, How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., Discretisation of the shading normals into the planes of the form. A sculptor… (+23 more)

### Community 12 - "camera.py"
Cohesion: 0.12
Nodes (24): Named camera positions the artist can jump between while sculpting., Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-… (+16 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.07
Nodes (30): Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, OrientationSettings, Enum (+22 more)

### Community 14 - "SceneRenderer"
Cohesion: 0.11
Nodes (12): MeshBuffers, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Whichever geometry is standing for the model this frame., Fill the shader's table with a level, if it is not already in it., Replace the annotation geometry; pass an empty list to hide it., Vertex/index buffers for one mesh, bound through a single VAO. (+4 more)

### Community 15 - "README.md"
Cohesion: 0.27
Nodes (10): Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets (+2 more)

### Community 16 - "gltf_loader.py"
Cohesion: 0.12
Nodes (28): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry() (+20 more)

### Community 17 - "planes_panel.py"
Cohesion: 0.12
Nodes (21): QFormLayout, QGroupBox, Shared plumbing for the dockable side panels., Dockable control panels., Matcap selection and colour grading., Measurement list and display options., What was imported and which way up it should stand., Everything that acts on the shading normals rather than on the shading. Faceted… (+13 more)

### Community 18 - "mesh_renderer.py"
Cohesion: 0.08
Nodes (20): bind_default(), ColorTarget, current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the… (+12 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "ball"
Cohesion: 0.17
Nodes (12): ball(), The one thing the additive mode rests on, asked of the lump rather than of the…, Left to itself a facing that no single point of the wall is holding back runs…, A join starts life as the hull of two lumps, which is a shape that pokes out of…, A closed sphere: wrapped at the seam, capped at both poles., AutoSmooth reads the normals of a form that has already been built, so it must…, test_a_lump_is_held_to_the_material_it_was_pressed_into(), test_a_lump_never_grows_out_through_the_model() (+4 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "ndarray"
Cohesion: 0.29
Nodes (6): ndarray, A level with no place in it: nearest direction wins, as before., The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to., _split(), _summarise()

### Community 23 - "block"
Cohesion: 0.20
Nodes (10): ndarray, Points spread over the model closely enough for a lattice to feel it. The…, surface_seeds(), block(), A closed box with hard edges, each face cut into a grid of triangles., Counting crossings is exact on a closed surface and meaningless on anything…, A box is six triangles the size of the whole thing; the lattice has to feel it…, test_a_form_already_made_of_flats_is_left_about_where_it_was() (+2 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.15
Nodes (8): QTreeWidgetItem, MeasurePanel, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn.

### Community 25 - "BookmarkStore"
Cohesion: 0.12
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Deletion goes through the undo stack, so the store only tracks position., test_bookmarks_cycle_and_wrap() (+1 more)

### Community 26 - "NavigationController"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "SectionSettings"
Cohesion: 0.08
Nodes (29): Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, The direction the section plane faces. (+21 more)

### Community 28 - "SliderSpin"
Cohesion: 0.15
Nodes (8): QFrame, CollapsibleGroup, QWidget, Re-scale the control, e.g. once a model's size is known., Grow the slider to take in a value from beyond its end., A float slider paired with a spin box, kept in sync. The slider works in…, A group whose rows fold away behind its title. For settings that are worth…, SliderSpin

### Community 29 - "core/__init__.py"
Cohesion: 0.07
Nodes (47): Qt-free geometry, camera and document model for the reference viewer., compute_vertex_normals(), load_mesh(), Path, One entry point for every mesh format the viewer reads. Callers ask for a path…, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., MeshLoadError, RuntimeError (+39 more)

### Community 30 - "MeasurementStore"
Cohesion: 0.14
Nodes (6): MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., One end of the measurement, ``0`` for the start and ``1`` for the end., An ordered, named collection of measurements. Deliberately plain: the Qt layer…

### Community 31 - "ShadingPanel"
Cohesion: 0.18
Nodes (8): Material parameters shared by the analytic shading modes., SurfaceSettings, Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., ShadingPanel

### Community 32 - "Panel"
Cohesion: 0.23
Nodes (5): Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block.

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (8): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_serialisation_round_trip(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (58): angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What… (+50 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (32): c_void_p, skipif, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had. (+24 more)

### Community 36 - "plane_volume.py"
Cohesion: 0.05
Nodes (80): _axes(), _back_inside(), block_bounds(), block_field(), blocks(), _box_facings(), carve(), clay_pieces() (+72 more)

### Community 37 - "History"
Cohesion: 0.14
Nodes (16): AddItem, Append an item to a document list., History, A bounded undo/redo stack., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made() (+8 more)

### Community 38 - "update_check.py"
Cohesion: 0.14
Nodes (22): check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed). (+14 more)

### Community 39 - "decode"
Cohesion: 0.27
Nodes (8): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., T

### Community 40 - "SectionPanel"
Cohesion: 0.21
Nodes (6): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 41 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 42 - "Camera"
Cohesion: 0.08
Nodes (16): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target). (+8 more)

### Community 43 - "viewport.py"
Cohesion: 0.09
Nodes (25): Measurement, MeasurementSettings, Named point-to-point measurements and their presentation options., A straight distance between two points on the model surface., Distance in scene units., Name of the attribute a handle edits, for building an undo command., How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string. (+17 more)

### Community 44 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 45 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 46 - "obj_loader.py"
Cohesion: 0.08
Nodes (39): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic(), load_obj(), ndarray (+31 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "render/__init__.py"
Cohesion: 0.11
Nodes (11): OpenGL rendering layer: shader programs, textures and the scene renderer., DataTexture, MatcapLoadError, ndarray, RuntimeError, Matcap texture loading and upload, and the small data table beside it., An RGBA8 2D texture with clamped edges and mipmapped minification., Raised when an image cannot be used as a matcap. (+3 more)

### Community 50 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 51 - "._build"
Cohesion: 0.33
Nodes (3): QStyledItemDelegate, _NameOnlyDelegate, Allows in-place editing of the name column only.

### Community 52 - "Projection"
Cohesion: 0.33
Nodes (4): Projection, Enum, str, Projection used by :class:`Camera`.

### Community 53 - "AnnotatePanel"
Cohesion: 0.24
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 54 - "SetAttributes"
Cohesion: 0.29
Nodes (3): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes

### Community 55 - "ShadingMode"
Cohesion: 0.12
Nodes (11): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, PlaneTarget, str, QualitySettings, Soft shadows and ambient occlusion for the high-quality mode. Both are screen-…, What the planes filter is allowed to act on. The two are mutually exclusive… (+3 more)

### Community 56 - ".drag_target"
Cohesion: 0.29
Nodes (4): ndarray, Consume a picked point; returns a measurement on the second click., Where a click at ``(x, y)`` would put a point. With free placement the point…, Where a grabbed endpoint should move to. Free placement -- and a drag that…

### Community 57 - "settings.py"
Cohesion: 0.04
Nodes (68): Coefficients, _empty(), PlaneAxes, PlaneSet, Reading the planes of a form out of the model's own normals. The grid quantiser…, One level of a fit: the planes the shader is to quantise against. A plane is a…, The planes a model falls into, at every count. Built once per mesh and per…, The best ``count`` planes, or as many as the model supports. A model whose… (+60 more)

### Community 58 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Six small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 59 - "Bounds"
Cohesion: 0.13
Nodes (17): Bounds, ndarray, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray (+9 more)

### Community 60 - "Command"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 61 - "Path"
Cohesion: 0.23
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 62 - "ColorButton"
Cohesion: 0.16
Nodes (7): QPushButton, QScrollArea, A draggable split: thumbnails above, adjustments below. The gallery is the one…, ColorButton, A swatch button that opens a colour picker. Colours are exchanged as 0-1 RGB…, Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, scrollable()

### Community 65 - "test_session.py"
Cohesion: 0.10
Nodes (16): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a…, The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that… (+8 more)

### Community 66 - "box"
Cohesion: 0.50
Nodes (4): box(), A unit cube, shaded flat: six planes and twelve right angles., Every edge of a cube is a right angle, and no reading of AutoSmooth short of…, test_autosmooth_leaves_a_real_plane_change_hard()

### Community 67 - "test_relaxing_settles_the_clay_and_leaves_the_stone_alone"
Cohesion: 0.50
Nodes (4): How far each point sits from the middle of its neighbours, as a share of the…, The relax is a pass over the finished surface rather than anything the volume…, roughness(), test_relaxing_settles_the_clay_and_leaves_the_stone_alone()

### Community 69 - "solid_count"
Cohesion: 0.28
Nodes (9): block_count(), piece_count(), How many blocks a count of planes asks the stone to be cut into. One at the…, How many lumps a count of planes asks the clay to be built out of. The masses…, How many solids the form is made of, whichever way it is being worked., solid_count(), The masses are a reading of the form and the tubes are how far the modelling is…, test_asking_for_more_masses_never_costs_the_clay_its_detail() (+1 more)

### Community 70 - "Mesh"
Cohesion: 0.09
Nodes (16): auto_smooth(), _gathered(), Mesh, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Return a copy whose bounding-box centre sits at the origin., Which group each of ``total`` things lands in, given pairs that agree. Hooking…, A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.… (+8 more)

### Community 71 - "plane_regions"
Cohesion: 0.09
Nodes (36): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, The stand-in these settings ask for, or ``None`` for the model itself., sculpt_mesh(), dumbbell(), Two balls of different size, far enough apart to be two masses., Enclosed volume, by the divergence theorem over the triangles. (+28 more)

### Community 80 - "lock_icon"
Cohesion: 0.40
Nodes (4): QIcon, lock_icon(), Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if…

### Community 81 - "rounded"
Cohesion: 0.40
Nodes (5): MonkeyPatch, coarse_lattice(), fixture, Read every model on a small lattice, so the suite stays quick., rounded()

### Community 82 - "._build"
Cohesion: 0.24
Nodes (7): PlanesPanel, The line under the normals slider: what the setting has asked for., The line under the geometry slider: how the form is being worked., Breaks the form into planes, in the shading or in the geometry itself., Put the design matrix back the way it reads a figure., _sculpt_summary(), _summary()

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `plane_axes`, `ViewerState`, `TriangleIndex`, `test_plane_solids.py`, `OrientationSettings`, `SceneRenderer`, `gltf_loader.py`, `mesh_renderer.py`, `ball`, `block`, `SectionSettings`, `core/__init__.py`, `test_plane_clusters.py`, `plane_volume.py`, `viewport.py`, `obj_loader.py`, `settings.py`, `Bounds`, `box`, `test_relaxing_settles_the_clay_and_leaves_the_stone_alone`, `plane_regions`, `rounded`?**
  _High betweenness centrality (0.181) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `main_window.py`, `AnnotateTool`, `MainWindow`, `ViewerState`, `viewport.py`, `NavigationController`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera` to `test_camera.py`, `.pan`, `ViewerState`, `test_navigation.py`, `RenderSettings`, `viewport.py`, `camera.py`, `README.md`, `mesh_renderer.py`, `BookmarkStore`, `NavigationController`, `Bounds`, `core/__init__.py`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `MainWindow` (e.g. with `ViewerState` and `UpdateChecker`) actually correct?**
  _`MainWindow` has 3 INFERRED edges - model-reasoned connections that need verification._