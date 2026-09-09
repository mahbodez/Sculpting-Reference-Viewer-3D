# Graph Report - reference-viewer  (2026-09-09)

## Corpus Check
- 85 files · ~262,759 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1965 nodes · 4320 edges · 90 communities (88 shown, 2 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 200 edges (avg confidence: 0.61)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a5073bc3`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Stroke
- Film
- Release
- Viewport
- plane_axes
- AnnotateTool
- MainWindow
- ViewerState
- raycast_mesh
- box
- ndarray
- ShadingMode
- mesh_renderer.py
- OrientationSettings
- SceneRenderer
- README.md
- gltf_loader.py
- main_window.py
- GeometryTarget
- CameraPanel
- ball
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
- plane_volume.py
- History
- release_from_payload
- ColorButton
- test_mesh_io.py
- test_navigation.py
- .from_dict
- viewport.py
- UpdateChecker
- .copy
- obj_loader.py
- PlaneAxes
- Agent Graph-First Instructions
- render/__init__.py
- core/__init__.py
- shaders.py
- load_obj
- .pan
- ReplaceItems
- Mesh
- MeasureTool
- settings.py
- plane_count
- Bounds
- refview/__init__.py
- Path
- CollapsibleGroup
- section_segments
- MatcapPanel
- test_session.py
- Camera
- test_relaxing_settles_the_clay_and_leaves_the_stone_alone
- stl_loader.py
- CHANGELOG.md
- Command
- test_plane_solids.py
- application.py
- section.py
- session.py
- ndarray
- AnnotatePanel
- SliderSpin
- SetAttributes
- AnnotateMode
- lock_icon
- rounded
- PlaneSettings
- ._start_update_check
- .empty
- environment.yml
- release.yml
- ModelPanel
- MeshLoadError
- edge_use

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 116 edges
2. `Camera` - 71 edges
3. `PlaneSettings` - 57 edges
4. `Viewport` - 53 edges
5. `MainWindow` - 46 edges
6. `ViewerState` - 46 edges
7. `SceneRenderer` - 42 edges
8. `plane_regions()` - 38 edges
9. `Stroke` - 33 edges
10. `sculpt_mesh()` - 33 edges

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

## Communities (90 total, 2 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.06
Nodes (37): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+29 more)

### Community 1 - "Film"
Cohesion: 0.12
Nodes (13): Film, The stage at ``index``, clamped to what has actually been recorded., A whole making, from the coarsest stage to the one the slider asks for. Held by…, FilmRecorder, QObject, The film being recorded, or the last one finished., The film already held for ``key``, if there is one., Stop any recording in flight and forget what it was making. The thread is asked… (+5 more)

### Community 2 - "Release"
Cohesion: 0.18
Nodes (16): check_for_update(), fetch_latest_release(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed)., The newest published release, as GitHub describes it., Return the newest published release, or raise :class:`UpdateCheckError`., The newest release when it is later than ``current_version``, else ``None``. (+8 more)

### Community 3 - "Viewport"
Cohesion: 0.06
Nodes (18): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on., Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current. (+10 more)

### Community 4 - "plane_axes"
Cohesion: 0.08
Nodes (36): _empty(), plane_axes(), ndarray, A level with no place in it: nearest direction wins, as before., The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to., Split the mesh's normals into planes, keeping every count on the way., _split() (+28 more)

### Community 5 - "AnnotateTool"
Cohesion: 0.11
Nodes (17): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Painting annotations onto the model surface. Every shape is laid down the same…, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+9 more)

### Community 6 - "MainWindow"
Cohesion: 0.08
Nodes (11): QAction, QMainWindow, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits., Keep the menu entry agreeing with the panel's own checkbox. (+3 more)

### Community 7 - "ViewerState"
Cohesion: 0.10
Nodes (14): ndarray, Path, Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements and…, Rotate the measurements and annotations onto the turned model. A point sits at…, Take the display unit from the file when the format declares one. Only glTF… (+6 more)

### Community 8 - "raycast_mesh"
Cohesion: 0.06
Nodes (43): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.… (+35 more)

### Community 9 - "box"
Cohesion: 0.50
Nodes (4): box(), A unit cube, shaded flat: six planes and twelve right angles., Every edge of a cube is a right angle, and no reading of AutoSmooth short of…, test_autosmooth_leaves_a_real_plane_change_hard()

### Community 10 - "ndarray"
Cohesion: 0.13
Nodes (15): normal_matrix(), ndarray, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.…, The model, the pedestal under it and the flat cap over the cut., Point the shading pass at the shadow map and the occlusion buffer., Flood the exposed interior with a flat colour so the cut reads solid. The…, The bright outline where the section plane meets the surface. (+7 more)

### Community 11 - "ShadingMode"
Cohesion: 0.17
Nodes (8): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, QualitySettings, Soft shadows and ambient occlusion for the high-quality mode. Both are screen-…, Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode

### Community 12 - "mesh_renderer.py"
Cohesion: 0.10
Nodes (32): Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., look_at(), normalize(), orthographic() (+24 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 14 - "SceneRenderer"
Cohesion: 0.11
Nodes (10): MeshBuffers, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Whichever geometry is standing for the model this frame., Fill the shader's table with a level, if it is not already in it., Replace the annotation geometry; pass an empty list to hide it., Vertex/index buffers for one mesh, bound through a single VAO. (+2 more)

### Community 15 - "README.md"
Cohesion: 0.23
Nodes (11): Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets (+3 more)

### Community 16 - "gltf_loader.py"
Cohesion: 0.14
Nodes (24): _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry(), _primitives(), ndarray (+16 more)

### Community 17 - "main_window.py"
Cohesion: 0.10
Nodes (27): QFormLayout, QGroupBox, The handful of undoable edits the whole application is built from.…, Delete the item at ``index``, putting it back in place on undo., RemoveItem, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, MatcapLoadError, RuntimeError (+19 more)

### Community 18 - "GeometryTarget"
Cohesion: 0.08
Nodes (17): bind_default(), ColorTarget, current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the… (+9 more)

### Community 19 - "CameraPanel"
Cohesion: 0.11
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "ball"
Cohesion: 0.08
Nodes (36): coarse_lattice(), film_of(), fixture, MonkeyPatch, parametrize, Scrubbing through the making of a form, rather than only arriving at it. The…, The same the other way about: a lump adds material, so the form grows., A stage is something to look at, so it has to be closed and wound out.… (+28 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "ViewportOverlay"
Cohesion: 0.22
Nodes (14): QColor, QPainter, QPointF, project_visible(), QFont, A square grip, so an editable end reads differently from a fixed one., Preview the gesture under way; finished strokes are drawn in 3D., The cursor ring: the eraser's reach, or the width of the brush. (+6 more)

### Community 23 - "PlanesPanel"
Cohesion: 0.16
Nodes (10): PlanesPanel, The line under the normals slider: what the setting has asked for., The line under the geometry slider: how the form is being worked., Breaks the form into planes, in the shading or in the geometry itself., Put the design matrix back the way it reads a figure., Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Show what this way of working needs, and put the rest away. A setting that does… (+2 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.18
Nodes (6): QTreeWidgetItem, MeasurePanel, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Lists saved measurements and controls how they are drawn.

### Community 25 - "BookmarkStore"
Cohesion: 0.12
Nodes (10): BookmarkStore, CameraBookmark, Named camera positions the artist can jump between while sculpting., A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Deletion goes through the undo stack, so the store only tracks position. (+2 more)

### Community 26 - "NavigationController"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "SectionSettings"
Cohesion: 0.14
Nodes (19): How the model is cut open, and how the cut is drawn., SectionSettings, LightSettings, MatcapSettings, Material parameters shared by the analytic shading modes., Post-processing applied to the sampled matcap texel., A key light, an opposing fill and a hemispherical ambient term., SurfaceSettings (+11 more)

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
Cohesion: 0.20
Nodes (7): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel

### Community 32 - "Panel"
Cohesion: 0.23
Nodes (5): Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block.

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (58): angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What… (+50 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (32): c_void_p, skipif, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had. (+24 more)

### Community 36 - "plane_volume.py"
Cohesion: 0.04
Nodes (97): _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field(), block_labels(), block_splits() (+89 more)

### Community 37 - "History"
Cohesion: 0.14
Nodes (16): AddItem, Append an item to a document list., History, A bounded undo/redo stack., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made() (+8 more)

### Community 38 - "release_from_payload"
Cohesion: 0.19
Nodes (14): is_newer(), _padded(), parse_version(), Numeric components of ``text``, or ``None`` when it is not a version. A pre-…, Whether ``candidate`` is a strictly later version than ``current``., Pull the tag and page link out of a GitHub release document., release_from_payload(), parametrize (+6 more)

### Community 39 - "ColorButton"
Cohesion: 0.18
Nodes (6): QPushButton, QStyledItemDelegate, _NameOnlyDelegate, Allows in-place editing of the name column only., ColorButton, A swatch button that opens a colour picker. Colours are exchanged as 0-1 RGB…

### Community 40 - "test_mesh_io.py"
Cohesion: 0.22
Nodes (14): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one(), test_binary_stl_welds_shared_corners() (+6 more)

### Community 41 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 42 - ".from_dict"
Cohesion: 0.29
Nodes (3): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., test_serialisation_round_trip()

### Community 43 - "viewport.py"
Cohesion: 0.15
Nodes (13): Freehand annotations painted onto the model surface. A stroke is a polyline of…, MeasurementSettings, Named point-to-point measurements and their presentation options., How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., Qt user interface: the viewport widget, the panels and the main window., Two-click measuring, plus dragging the endpoints of an unlocked measurement., 2D overlay drawn on top of the GL scene with QPainter. Measurements are… (+5 more)

### Community 44 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 45 - ".copy"
Cohesion: 0.17
Nodes (5): Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Move the camera so ``bounds`` fills the view, keeping the direction., Point the camera along ``direction``, measured object-to-eye., Adopt the pose of ``other`` without replacing this instance.

### Community 46 - "obj_loader.py"
Cohesion: 0.22
Nodes (14): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), ndarray, Minimal, dependency-free Wavefront OBJ reader. Only the geometry statements a…, Resolve ``v``, ``v/vt``, ``v//vn`` or ``v/vt/vn`` corners to 0-based pairs.… (+6 more)

### Community 47 - "PlaneAxes"
Cohesion: 0.29
Nodes (3): PlaneAxes, The planes a model falls into, at every count. Built once per mesh and per…, The best ``count`` planes, or as many as the model supports. A model whose…

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "render/__init__.py"
Cohesion: 0.11
Nodes (10): OpenGL rendering layer: shader programs, textures and the scene renderer., DataTexture, default_matcap_pixels(), ndarray, Matcap texture loading and upload, and the small data table beside it., An RGBA8 2D texture with clamped edges and mipmapped minification., A neutral studio matcap, used before the user picks one., A small RGBA32F table the shader reads exact values out of. Not a picture:… (+2 more)

### Community 50 - "core/__init__.py"
Cohesion: 0.18
Nodes (9): Qt-free geometry, camera and document model for the reference viewer., Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis, NavigationSettings, How mouse gestures drive the camera. (+1 more)

### Community 51 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Six small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 52 - "load_obj"
Cohesion: 0.27
Nodes (12): load_obj(), Path, Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, Negative face indices count back from the most recent vertex., test_obj_relative_indices_still_load(), OBJ parsing: normals, triangulation and index handling., test_empty_file_is_rejected(), test_missing_normals_are_computed() (+4 more)

### Community 54 - "ReplaceItems"
Cohesion: 0.18
Nodes (4): Any, Swap the whole contents of a document list. Used for bulk edits -- clearing the…, ReplaceItems, test_replace_items_covers_bulk_edits()

### Community 55 - "Mesh"
Cohesion: 0.06
Nodes (47): auto_smooth(), compute_vertex_normals(), _gathered(), Mesh, Triangle-mesh containers shared by the loader, the renderer and picking., Return a copy whose bounding-box centre sits at the origin., Which group each of ``total`` things lands in, given pairs that agree. Hooking…, A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.… (+39 more)

### Community 56 - "MeasureTool"
Cohesion: 0.12
Nodes (10): Handle, MeasureTool, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., Where a click at ``(x, y)`` would put a point. With free placement the point… (+2 more)

### Community 57 - "settings.py"
Cohesion: 0.05
Nodes (54): Coefficients, How much surface each vertex stands for: a third of each triangle on it.…, What each block of the design matrix counts for, against the normals. A fit…, Whether anything but the normals is being read at all., vertex_weights(), _compact(), _consensus(), _cut() (+46 more)

### Community 58 - "plane_count"
Cohesion: 0.12
Nodes (12): _along(), lattice_fineness(), plane_count(), Where a detail setting sits on its slider, 0 to 1., How much finer than usual a detail setting asks the lattice to be. One at the…, How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., How much of a turn in the surface one plane covers, in degrees. Linear in…, How many planes a mode fitted to the model keeps. The climb from two planes to… (+4 more)

### Community 59 - "Bounds"
Cohesion: 0.18
Nodes (15): Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray, A turntable-style disc the model can stand on. A ground plane gives the eye… (+7 more)

### Community 60 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 61 - "Path"
Cohesion: 0.29
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 62 - "CollapsibleGroup"
Cohesion: 0.16
Nodes (11): QFrame, QScrollArea, CollapsibleGroup, QWidget, Let a panel be narrower than the sentences inside it. How narrow a panel will…, Let a widget be given less width than its own text asks for., Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, A group whose rows fold away behind its title. For settings that are worth… (+3 more)

### Community 63 - "section_segments"
Cohesion: 0.18
Nodes (9): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, Unit axis, or ``None`` for a custom direction., A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., section_segments() (+1 more)

### Community 64 - "MatcapPanel"
Cohesion: 0.27
Nodes (4): MatcapPanel, Rebuild the thumbnail list from the resources folder., Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…

### Community 65 - "test_session.py"
Cohesion: 0.15
Nodes (13): Path, A snapshot of everything worth keeping between runs., Session file that sits beside a model, e.g. ``bust.refview.json``., Session, sidecar_path(), Session persistence, measurements and bookmarks., Version 1 files predate the annotation layer and the endpoint lock., test_a_session_from_before_annotations_still_loads() (+5 more)

### Community 66 - "Camera"
Cohesion: 0.15
Nodes (9): Camera, ndarray, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling…, A look-at camera with orbit / pan / zoom behaviour. The orthographic extent is…, Vertical half-extent of the frustum at the focal plane. (+1 more)

### Community 67 - "test_relaxing_settles_the_clay_and_leaves_the_stone_alone"
Cohesion: 0.50
Nodes (4): How far each point sits from the middle of its neighbours, as a share of the…, The relax is a pass over the finished surface rather than anything the volume…, roughness(), test_relaxing_settles_the_clay_and_leaves_the_stone_alone()

### Community 68 - "stl_loader.py"
Cohesion: 0.22
Nodes (13): _ascii_corners(), _binary_corners(), load_stl(), ndarray, Path, Binary and ASCII STL reader. STL stores three loose corners per facet and…, Raised when a file cannot be interpreted as an STL mesh., Load ``path``, choosing the binary or ASCII reader by inspection. (+5 more)

### Community 69 - "CHANGELOG.md"
Cohesion: 0.18
Nodes (10): Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, STL and glTF import (1.1.0), Units are adopted, never guessed (+2 more)

### Community 70 - "Command"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 71 - "test_plane_solids.py"
Cohesion: 0.05
Nodes (68): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), block(), dumbbell(), flatness(), parametrize (+60 more)

### Community 72 - "application.py"
Cohesion: 0.07
Nodes (49): ArgumentParser, Color, Namespace, QApplication, QSplashScreen, Charcoal matcap, Terracotta clay matcap, Jade matcap (+41 more)

### Community 73 - "section.py"
Cohesion: 0.24
Nodes (7): Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Which side of the plane survives the cut., SectionAxis, SectionMode

### Community 74 - "session.py"
Cohesion: 0.27
Nodes (9): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Persisted viewer state: camera, shading, measurements and bookmarks. (+1 more)

### Community 75 - "ndarray"
Cohesion: 0.20
Nodes (4): ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, test_bounds_of_an_empty_point_set()

### Community 76 - "AnnotatePanel"
Cohesion: 0.27
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 77 - "SliderSpin"
Cohesion: 0.27
Nodes (4): Re-scale the control, e.g. once a model's size is known., Grow the slider to take in a value from beyond its end., A float slider paired with a spin box, kept in sync. The slider works in…, SliderSpin

### Community 78 - "SetAttributes"
Cohesion: 0.31
Nodes (4): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable.

### Community 79 - "AnnotateMode"
Cohesion: 0.25
Nodes (5): AnnotateMode, Enum, str, An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a…

### Community 80 - "lock_icon"
Cohesion: 0.29
Nodes (6): QIcon, QPixmap, lock_icon(), Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if…, _render()

### Community 81 - "rounded"
Cohesion: 0.40
Nodes (5): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick., rounded()

### Community 82 - "PlaneSettings"
Cohesion: 0.06
Nodes (34): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, Holds the working state between one turn of the sliders and the next.…, The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache, PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor… (+26 more)

### Community 83 - "._start_update_check"
Cohesion: 0.29
Nodes (4): Ask GitHub for the newest release in the background. The startup check is…, QWidget, show_failure_dialog(), show_up_to_date_dialog()

### Community 84 - ".empty"
Cohesion: 0.29
Nodes (4): Drop everything held, so the next call starts from the fit., A model the fit cannot break down has no making to show, and says so by handing…, test_the_film_is_empty_for_a_model_with_no_planes_in_it(), test_a_model_with_no_planes_in_it_comes_back_as_it_went_in()

### Community 85 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 86 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 88 - "MeshLoadError"
Cohesion: 0.40
Nodes (5): MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., ObjLoadError, Raised when a file cannot be interpreted as an OBJ mesh.

### Community 92 - "edge_use"
Cohesion: 0.40
Nodes (5): edge_use(), ndarray, Which point each vertex really is, once copies of a position are one point., Edges used once, edges used more than twice, and edges in all. Once would mean…, welded()

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `Film`, `plane_axes`, `ViewerState`, `raycast_mesh`, `box`, `mesh_renderer.py`, `OrientationSettings`, `SceneRenderer`, `README.md`, `gltf_loader.py`, `ball`, `SectionSettings`, `test_plane_clusters.py`, `plane_volume.py`, `test_mesh_io.py`, `viewport.py`, `obj_loader.py`, `PlaneAxes`, `core/__init__.py`, `load_obj`, `settings.py`, `Bounds`, `section_segments`, `test_relaxing_settles_the_clay_and_leaves_the_stone_alone`, `stl_loader.py`, `CHANGELOG.md`, `test_plane_solids.py`, `section.py`, `ndarray`, `rounded`, `PlaneSettings`, `MeshLoadError`, `edge_use`?**
  _High betweenness centrality (0.194) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera` to `test_camera.py`, `test_session.py`, `test_navigation.py`, `.from_dict`, `ndarray`, `mesh_renderer.py`, `.copy`, `viewport.py`, `README.md`, `core/__init__.py`, `CameraPanel`, `.pan`, `ViewportOverlay`, `BookmarkStore`, `NavigationController`, `Bounds`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `Film`, `AnnotateTool`, `MainWindow`, `ViewerState`, `viewport.py`, `main_window.py`, `ViewportOverlay`, `MeasureTool`, `NavigationController`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `PlaneSettings` (e.g. with `Film` and `Stage`) actually correct?**
  _`PlaneSettings` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 9 INFERRED edges - model-reasoned connections that need verification._