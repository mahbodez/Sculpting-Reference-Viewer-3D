# Graph Report - reference-viewer  (2026-09-11)

## Corpus Check
- 91 files · ~286,116 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2449 nodes · 5500 edges · 111 communities (108 shown, 3 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 210 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `073d0ad9`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Stroke
- FilmRecorder
- Release
- Viewport
- plane_axes.py
- AnnotateTool
- MainWindow
- ViewerState
- spatial.py
- Measurement
- SceneRenderer
- StrokeBuffers
- camera.py
- OrientationSettings
- Armature
- README.md
- SetAttributes
- form_group
- mesh_renderer.py
- CameraPanel
- test_plane_film.py
- ShaderProgram
- ViewportOverlay
- planes_panel.py
- MeasurePanel
- BookmarkStore
- NavigationController
- SectionSettings
- SectionPanel
- test_session.py
- decode
- ShadingPanel
- Panel
- test_camera.py
- test_plane_clusters.py
- WakeLock
- ndarray
- AddItem
- update_check.py
- picking.py
- mesh.py
- ndarray
- test_armature.py
- MeasureTool
- UpdateChecker
- PlacedLandmark
- compute_vertex_normals
- landmarks.py
- Agent Graph-First Instructions
- ._accumulate_ghost
- Mesh
- MeshBuffers
- Landmark
- SliderSpin
- matcap_panel.py
- plane_solids.py
- Camera
- ._draw_hud
- plane_count
- core/__init__.py
- clay_lumps
- Path
- .update_enabled
- plane_volume.py
- MatcapPanel
- viewport.py
- ndarray
- lay_bed
- PlaneMode
- stone_field
- main_window.py
- test_plane_solids.py
- application.py
- raycast_mesh
- .copy
- ArmatureStore
- AnnotatePanel
- record
- ._selected_landmark
- History
- armature.py
- ArmatureTool
- PlaneSettings
- ._selected
- Command
- auto_smooth
- ._start_update_check
- ._picker
- ._build
- rounded
- .point
- test_spatial.py
- .mousePressEvent
- ball
- block_splits
- TriangleIndex
- ndarray
- environment.yml
- release.yml
- shaders.py
- .refresh_list
- coarse_lattice
- ._arm
- _NameOnlyDelegate
- ._commit_node_drag
- ._upload_sculpt
- ._buried_nodes
- ._place_armature_node
- .surface_opacity
- refview/__init__.py
- ArmaturePanel

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 117 edges
2. `Camera` - 75 edges
3. `Viewport` - 73 edges
4. `PlaneSettings` - 63 edges
5. `Armature` - 60 edges
6. `ArmaturePanel` - 60 edges
7. `ArmatureTool` - 51 edges
8. `ViewerState` - 51 edges
9. `MainWindow` - 48 edges
10. `SceneRenderer` - 46 edges

## Surprising Connections (you probably didn't know these)
- `Orthographic extent derived from FOV and distance` --rationale_for--> `Camera`  [EXTRACTED]
  README.md → src/refview/core/camera.py
- `Pedestal (1.1.0)` --rationale_for--> `PedestalSettings`  [EXTRACTED]
  CHANGELOG.md → src/refview/core/pedestal.py
- `REFVIEW_RESOURCES resource override` --rationale_for--> `available_matcaps()`  [EXTRACTED]
  README.md → src/refview/paths.py
- `The cut interior is flooded flat` --rationale_for--> `SceneRenderer`  [INFERRED]
  README.md → src/refview/render/mesh_renderer.py
- `Units are adopted, never guessed` --semantically_similar_to--> `STL and glTF import (1.1.0)`  [INFERRED] [semantically similar]
  README.md → CHANGELOG.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The bundled matcap set** — resources_matcaps_clay_terracotta_matcap, resources_matcaps_charcoal_matcap, resources_matcaps_jade_matcap, resources_matcaps_steel_matcap, resources_matcaps_studio_white_matcap, resources_matcaps_wax_skin_matcap, tools_generate_matcaps_matcappreset, tools_generate_matcaps_render [INFERRED 0.85]
- **The four generic undo commands** — src_refview_core_commands_setattributes, src_refview_core_commands_additem, src_refview_core_commands_removeitem, src_refview_core_commands_replaceitems, src_refview_core_history_command, readme_every_edit_is_a_command [EXTRACTED 1.00]
- **Windows binary-compatibility decisions** — readme_pyside6_pinned_below_68, environment_pip_installed_binaries, environment_python_311, github_workflows_release_pyinstaller_build [INFERRED 0.75]

## Communities (111 total, 3 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.08
Nodes (25): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+17 more)

### Community 1 - "FilmRecorder"
Cohesion: 0.09
Nodes (17): QThread, Film, The stage at ``index``, clamped to what has actually been recorded., A whole making, from the coarsest stage to the one the slider asks for. Held by…, FilmRecorder, QObject, The film being recorded, or the last one finished., Whether a film is being made right now. (+9 more)

### Community 2 - "Release"
Cohesion: 0.23
Nodes (12): check_for_update(), fetch_latest_release(), The newest published release, as GitHub describes it., Return the newest published release, or raise :class:`UpdateCheckError`., The newest release when it is later than ``current_version``, else ``None``., Release, is_skipped(), Background release check and the notice it puts in front of the artist. The… (+4 more)

### Community 3 - "Viewport"
Cohesion: 0.11
Nodes (10): QOpenGLWidget, Slide the view so a measurement sits at the centre, keeping the angle., Regenerate the pedestal and the cut contour when their settings move. Both are…, End any film being recorded, and wait for its thread to really stop. For…, Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current., Drop whatever gesture is half-finished, without disarming the tool., Renders the scene and turns mouse gestures into camera and tool actions. (+2 more)

### Community 4 - "plane_axes.py"
Cohesion: 0.08
Nodes (39): _empty(), plane_axes(), ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, A level with no place in it: nearest direction wins, as before., How much surface each vertex stands for: a third of each triangle on it.…, The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to. (+31 more)

### Community 5 - "AnnotateTool"
Cohesion: 0.10
Nodes (15): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+7 more)

### Community 6 - "MainWindow"
Cohesion: 0.08
Nodes (11): QAction, QMainWindow, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits., Keep the menu entry agreeing with the panel's own checkbox. (+3 more)

### Community 7 - "ViewerState"
Cohesion: 0.09
Nodes (15): ndarray, Path, QObject, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements, annotations… (+7 more)

### Community 8 - "spatial.py"
Cohesion: 0.24
Nodes (8): _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Build the index from expanded triangle corners, shape ``(T, 3, 3)``., Triangle indices worth intersecting for this ray, possibly empty., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the…, Interleave each 10-bit value with two zero bits, ready to be shifted., _spread_bits()

### Community 9 - "Measurement"
Cohesion: 0.11
Nodes (12): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+4 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.11
Nodes (23): Everything the viewport needs in order to draw a frame., RenderSettings, light_directions(), normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.… (+15 more)

### Community 11 - "StrokeBuffers"
Cohesion: 0.16
Nodes (12): build_segment_vertices(), build_vertices(), _expand(), ndarray, Geometry for the surface annotations and the cross-section contour. Strokes are…, A single vertex buffer holding every visible stroke., Replace the buffer contents with a prepared vertex block., Expand strokes into the triangle soup the stroke shader expects. Every segment… (+4 more)

### Community 12 - "camera.py"
Cohesion: 0.11
Nodes (26): Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., look_at(), normalize(), orthographic() (+18 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.05
Nodes (52): Model orientation (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry() (+44 more)

### Community 14 - "Armature"
Cohesion: 0.07
Nodes (33): Armature, ArmatureNode, Bone, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves., A plausible thickness for a node placed by hand. (+25 more)

### Community 15 - "README.md"
Cohesion: 0.27
Nodes (10): Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets (+2 more)

### Community 16 - "SetAttributes"
Cohesion: 0.14
Nodes (7): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Run a row's edit once Qt has finished delivering the current signal. Committing…, Record an edit the viewport's tool worked out., Join two nodes of one armature, if they are two and they are one armature., Commit a renamed or re-checked row, if anything actually changed.

### Community 17 - "form_group"
Cohesion: 0.11
Nodes (15): QFormLayout, QFrame, QGroupBox, collapsible_group(), CollapsibleGroup, ColorButton, form_group(), _panel_form() (+7 more)

### Community 18 - "mesh_renderer.py"
Cohesion: 0.07
Nodes (21): AccumTarget, bind_default(), ColorTarget, current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality and ghost passes. Four of…, A single-channel colour framebuffer, used for the occlusion buffers. (+13 more)

### Community 19 - "CameraPanel"
Cohesion: 0.12
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "test_plane_film.py"
Cohesion: 0.09
Nodes (31): coarse_lattice(), film_of(), fixture, MonkeyPatch, parametrize, Scrubbing through the making of a form, rather than only arriving at it. The…, The same the other way about: a lump adds material, so the form grows., A stage is something to look at, so it has to be closed and wound out.… (+23 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.12
Nodes (9): Fill the shader's table with a level, if it is not already in it., ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError (+1 more)

### Community 22 - "ViewportOverlay"
Cohesion: 0.17
Nodes (18): QColor, QPainter, QPointF, project_visible(), Handle, A line laid over its own dark outline, so it reads against anything., An unfilled circle: how thick the form is here, not how big a dot is., A square grip, so an editable end reads differently from a fixed one. (+10 more)

### Community 23 - "planes_panel.py"
Cohesion: 0.14
Nodes (12): PlanesPanel, Everything that acts on the shading normals rather than on the shading. Faceted…, The line under the normals slider: what the setting has asked for., The line under the geometry slider: how the form is being worked., Breaks the form into planes, in the shading or in the geometry itself., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Size the scrub slider to the film as it is recorded. The stages arrive one at a… (+4 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.11
Nodes (11): MeasurePanel, _NameOnlyDelegate, QStyledItemDelegate, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing… (+3 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.10
Nodes (11): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around. (+3 more)

### Community 26 - "NavigationController"
Cohesion: 0.09
Nodes (16): Shift-snapped orbiting (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, DragMode, NavigationController (+8 more)

### Community 27 - "SectionSettings"
Cohesion: 0.12
Nodes (22): ndarray, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn. (+14 more)

### Community 28 - "SectionPanel"
Cohesion: 0.11
Nodes (14): Cross-section tool (1.1.0), Enum, str, The direction the section plane faces., Unit axis, or ``None`` for a custom direction., Which side of the plane survives the cut., SectionAxis, SectionMode (+6 more)

### Community 29 - "test_session.py"
Cohesion: 0.08
Nodes (25): Path, A snapshot of everything worth keeping between runs., Session file that sits beside a model, e.g. ``bust.refview.json``., Session, sidecar_path(), Version 4 files predate the armature; they open with an empty one., test_a_session_from_before_the_armature_still_loads(), test_an_armature_survives_a_session_round_trip() (+17 more)

### Community 30 - "decode"
Cohesion: 0.27
Nodes (8): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., T

### Community 31 - "ShadingPanel"
Cohesion: 0.22
Nodes (7): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel

### Community 32 - "Panel"
Cohesion: 0.11
Nodes (15): Panel, QWidget, Shared plumbing for the dockable side panels., A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block., Dockable control panels., What was imported and which way up it should stand. (+7 more)

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

### Community 37 - "AddItem"
Cohesion: 0.20
Nodes (13): AddItem, Append an item to a document list., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch(), test_commands_carry_their_channel_and_name() (+5 more)

### Community 38 - "update_check.py"
Cohesion: 0.16
Nodes (18): is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed)., Numeric components of ``text``, or ``None`` when it is not a version. A pre-…, Whether ``candidate`` is a strictly later version than ``current``. (+10 more)

### Community 39 - "picking.py"
Cohesion: 0.23
Nodes (11): Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays., snap_to_vertex() (+3 more)

### Community 40 - "mesh.py"
Cohesion: 0.09
Nodes (35): STL and glTF import (1.1.0), load_mesh(), Path, One entry point for every mesh format the viewer reads. Callers ask for a path…, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., MeshLoadError, RuntimeError, Triangle-mesh containers shared by the loader, the renderer and picking. (+27 more)

### Community 41 - "ndarray"
Cohesion: 0.15
Nodes (7): ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Near/far planes fitted to the scene bounding sphere.

### Community 42 - "test_armature.py"
Cohesion: 0.13
Nodes (34): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., The femoral head is inside the bump you can feel, not on it., A wire in two halves is not an armature anybody could bend., Place every landmark the run asks for; returns how many were asked. (+26 more)

### Community 43 - "MeasureTool"
Cohesion: 0.12
Nodes (10): MeasureTool, Handle, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., Where a click at ``(x, y)`` would put a point. With free placement the point… (+2 more)

### Community 44 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 45 - "PlacedLandmark"
Cohesion: 0.08
Nodes (24): Point3, PlacedLandmark, One anatomical point the artist put on the model during a guided run., The landmark list with one point moved, and no longer a guess. A landmark the…, The landmark list with these points taken back off the model. More than one at…, mirror_landmarks(), Preset, The midline landmarks, which are what the median plane is fitted to. (+16 more)

### Community 46 - "compute_vertex_normals"
Cohesion: 0.11
Nodes (30): compute_vertex_normals(), Area-weighted smooth vertex normals for an indexed triangle soup., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic() (+22 more)

### Community 47 - "landmarks.py"
Cohesion: 0.10
Nodes (27): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), median_plane(), _mid(), mirror_point() (+19 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "._accumulate_ghost"
Cohesion: 0.17
Nodes (6): _ghost_depth_range(), Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Sum a see-through model into the ghost buffers, to be resolved after. Blending…, Where the form starts along the view, and how deep it is. The ghost weighs a…, Forget the contents without releasing the buffer objects.

### Community 50 - "Mesh"
Cohesion: 0.07
Nodes (38): Mesh, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, _compact(), _consensus(), _cut(), _first_planes(), _fit() (+30 more)

### Community 51 - "MeshBuffers"
Cohesion: 0.08
Nodes (13): OpenGL rendering layer: shader programs, textures and the scene renderer., MeshBuffers, Whichever geometry is standing for the model this frame., Replace the annotation geometry; pass an empty list to hide it., Vertex/index buffers for one mesh, bound through a single VAO., DataTexture, default_matcap_pixels(), ndarray (+5 more)

### Community 52 - "Landmark"
Cohesion: 0.12
Nodes (12): _humanoid_landmarks(), Landmark, _node_name(), The landmarks worth asking for under these choices. With mirroring on the…, The midline first, then each pair left before right., What to call a landmark in a menu or an undo step. The preset's own words when…, One point of anatomy the artist is asked to find., The name with its side, for a prompt. (+4 more)

### Community 53 - "SliderSpin"
Cohesion: 0.14
Nodes (7): PointEdit, Re-scale the control, e.g. once a model's size is known., Grow the slider to take in a value from beyond its end., Three spin boxes for one point in space. Keyboard tracking is off, so a typed…, Match the arrows to the size of the thing being moved., A float slider paired with a spin box, kept in sync. The slider works in…, SliderSpin

### Community 54 - "matcap_panel.py"
Cohesion: 0.22
Nodes (8): QScrollArea, MatcapLoadError, RuntimeError, Matcap texture loading and upload, and the small data table beside it., Raised when an image cannot be used as a matcap., Matcap selection and colour grading., Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, scrollable()

### Community 55 - "plane_solids.py"
Cohesion: 0.06
Nodes (40): PlaneAxes, PlaneSet, One level of a fit: the planes the shader is to quantise against. A plane is a…, The planes a model falls into, at every count. Built once per mesh and per…, The best ``count`` planes, or as many as the model supports. A model whose…, planes_for(), The stages a form passes through on its way from a block to a figure. The…, How many solids each stage of a film is made of. Every count from the coarsest… (+32 more)

### Community 56 - "Camera"
Cohesion: 0.15
Nodes (17): Camera, Screen-to-world scale at the focal plane; identical in both modes., Slide the camera parallel to the image plane by a pixel delta., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling…, A look-at camera with orbit / pan / zoom behaviour. The orthographic extent is…, Vertical half-extent of the frustum at the focal plane., _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting. (+9 more)

### Community 57 - "._draw_hud"
Cohesion: 0.38
Nodes (3): QFont, Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, What the armature tool is waiting for, said in as few lines as it takes.

### Community 58 - "plane_count"
Cohesion: 0.12
Nodes (12): _along(), lattice_fineness(), plane_count(), Where a detail setting sits on its slider, 0 to 1., How much finer than usual a detail setting asks the lattice to be. One at the…, How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., How much of a turn in the surface one plane covers, in degrees. Linear in…, How many planes a mode fitted to the model keeps. The climb from two planes to… (+4 more)

### Community 59 - "core/__init__.py"
Cohesion: 0.06
Nodes (42): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, Qt-free geometry, camera and document model for the reference viewer., Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal() (+34 more)

### Community 60 - "clay_lumps"
Cohesion: 0.14
Nodes (18): _box_facings(), clay_lumps(), clay_pieces(), fit_piece(), _frame(), grow_piece(), join_pieces(), piece_bounds() (+10 more)

### Community 61 - "Path"
Cohesion: 0.29
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 62 - ".update_enabled"
Cohesion: 0.14
Nodes (7): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., The armature the selected row stands for, when the row is not a node., Follow the highlighted row, without rebuilding the list underneath it. Going…, Highlight the row for a node picked in the view., Highlight the row for a landmark picked in the view.

### Community 63 - "plane_volume.py"
Cohesion: 0.17
Nodes (15): _balloon(), block_labels(), blocks(), close_gaps(), outside_points(), Blocking a form in out of its own planes, from the outside or from a core. A…, Fill the slots the lumps leave between them, without taking clay away. The…, Grow or shrink a solid by ``reach`` cells, one axis at a time. A separable… (+7 more)

### Community 64 - "MatcapPanel"
Cohesion: 0.27
Nodes (4): MatcapPanel, Rebuild the thumbnail list from the resources folder., Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…

### Community 65 - "viewport.py"
Cohesion: 0.10
Nodes (19): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, What the annotate tool does with a drag. The first three describe the shape a…, Named camera positions the artist can jump between while sculpting., MeasurementSettings, Named point-to-point measurements and their presentation options. (+11 more)

### Community 66 - "ndarray"
Cohesion: 0.17
Nodes (6): _gathered(), ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Which group each of ``total`` things lands in, given pairs that agree. Hooking…, test_bounds_of_an_empty_point_set()

### Community 67 - "lay_bed"
Cohesion: 0.15
Nodes (14): _axes(), encloses(), lattice(), lay_bed(), nearest_surface(), _passes(), Read the model onto a lattice, ready for solids to be laid on it., A cubic lattice covering the model with ``margin`` of room around it. Cubic… (+6 more)

### Community 68 - "PlaneMode"
Cohesion: 0.18
Nodes (7): fit_planes(), The planes of ``mesh`` under ``mode``; empty where the mode needs none., PlaneMode, How the plane directions are arrived at. ``shader_id`` must stay in sync with…, Whether the directions are read off the model rather than imposed., Whether the mode reads the design matrix, and so its coefficients. Grid reads…, The model's own planes under ``mode``, fitted once and kept.

### Community 69 - "stone_field"
Cohesion: 0.14
Nodes (14): Bed, block_bounds(), block_field(), coarse_bounds(), point_support(), The lattice a form is worked on, and the model read onto it. Everything here…, The union of the blocks a labelling cuts the model into, and its facings. Stone…, One row of coordinates per axis over ``box``, shaped so they broadcast. (+6 more)

### Community 70 - "main_window.py"
Cohesion: 0.11
Nodes (16): QIcon, The handful of undoable edits the whole application is built from.…, Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, lock_icon() (+8 more)

### Community 71 - "test_plane_solids.py"
Cohesion: 0.05
Nodes (68): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), block(), dumbbell(), flatness(), parametrize (+60 more)

### Community 72 - "application.py"
Cohesion: 0.07
Nodes (50): ArgumentParser, Color, Namespace, QApplication, QPixmap, QSplashScreen, Charcoal matcap, Terracotta clay matcap (+42 more)

### Community 73 - "raycast_mesh"
Cohesion: 0.23
Nodes (11): Return the closest front- or back-facing hit along the ray, or ``None``., raycast_mesh(), fixture, quad(), Ray/mesh intersection and vertex snapping., Two triangles covering the unit square on the z = 0 plane., test_closest_of_two_surfaces_wins(), test_hits_the_surface() (+3 more)

### Community 74 - ".copy"
Cohesion: 0.18
Nodes (4): Move the camera so ``bounds`` fills the view, keeping the direction., Point the camera along ``direction``, measured object-to-eye., Adopt the pose of ``other`` without replacing this instance., test_serialisation_round_trip()

### Community 75 - "ArmatureStore"
Cohesion: 0.18
Nodes (4): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 76 - "AnnotatePanel"
Cohesion: 0.24
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 77 - "record"
Cohesion: 0.23
Nodes (12): Work the form stage by stage, handing each one back as it is finished. A…, record(), carve(), _corner_facings(), facings(), fitted_facings(), The form ``directions`` leave of the model, worked one way or the other.…, Twenty-six directions round a cube, for judging how much air a block holds.… (+4 more)

### Community 78 - "._selected_landmark"
Cohesion: 0.12
Nodes (7): Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors., Show the landmark group only once there are landmarks to show., The landmark the highlighted row stands for, if the row is one., Which armature the landmark list is pointing into, row or heading., Follow the highlighted landmark, and say which one it is in the view.

### Community 79 - "History"
Cohesion: 0.20
Nodes (4): History, A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive…, test_undo_and_redo_on_an_empty_stack_are_safe()

### Community 80 - "armature.py"
Cohesion: 0.27
Nodes (7): BoneLabels, Buried, Enum, str, A graph of named points under the form, and the wire it stands for. An armature…, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…

### Community 81 - "ArmatureTool"
Cohesion: 0.05
Nodes (53): BoneRef, LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), ArmatureTool, _project() (+45 more)

### Community 82 - "PlaneSettings"
Cohesion: 0.09
Nodes (27): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor…, The grid step, in cube-face coordinates, that gives that span. A cell of this…, The design-matrix settings, in the form the fitters want them., Roughly how much of a turn one of those planes covers, in degrees., The plane size of whichever mode is running. (+19 more)

### Community 83 - "._selected"
Cohesion: 0.24
Nodes (4): Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., Run a bone between the row selected now and the node held before it., The node the selected row stands for, if the row is a node at all.

### Community 84 - "Command"
Cohesion: 0.28
Nodes (3): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu.

### Community 85 - "auto_smooth"
Cohesion: 0.17
Nodes (10): auto_smooth(), A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., box(), A unit cube, shaded flat: six planes and twelve right angles., Every edge of a cube is a right angle, and no reading of AutoSmooth short of…, The reason it is here. A facet that comes out of a lattice is only roughly one… (+2 more)

### Community 86 - "._start_update_check"
Cohesion: 0.29
Nodes (4): Ask GitHub for the newest release in the background. The startup check is…, QWidget, show_failure_dialog(), show_up_to_date_dialog()

### Community 87 - "._picker"
Cohesion: 0.20
Nodes (4): Rub out the stroke points under the eraser, live., Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit.

### Community 88 - "._build"
Cohesion: 0.29
Nodes (6): QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 89 - "rounded"
Cohesion: 0.40
Nodes (5): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick., rounded()

### Community 90 - ".point"
Cohesion: 0.22
Nodes (5): ndarray, Closest surface intersection under the cursor, or ``None``., Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-…, Screen-to-world scale at a given depth along the view direction.

### Community 91 - "test_spatial.py"
Cohesion: 0.33
Nodes (8): _grid(), The picking accelerator: it must be fast without changing any answer., A bumpy height field, so rays hit different triangles at different depths., The pruned candidate set must never miss the true intersection., test_a_ray_that_misses_the_model_is_pruned_away(), test_every_triangle_lands_in_exactly_one_leaf(), test_the_index_finds_the_triangle_a_ray_actually_hits(), test_the_index_is_built_once_and_kept()

### Community 92 - ".mousePressEvent"
Cohesion: 0.18
Nodes (5): ndarray, Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on.

### Community 93 - "ball"
Cohesion: 0.10
Nodes (20): A film nobody is waiting for any more is abandoned rather than finished.…, A model the fit cannot break down has no making to show, and says so by handing…, test_a_recording_can_be_stopped_part_way(), test_the_film_is_empty_for_a_model_with_no_planes_in_it(), ball(), How far each point sits from the middle of its neighbours, as a share of the…, The relax is a pass over the finished surface rather than anything the volume…, The one thing the additive mode rests on, asked of the lump rather than of the… (+12 more)

### Community 94 - "block_splits"
Cohesion: 0.33
Nodes (6): block_splits(), _cuts(), _hull_air(), The corners a hull round ``points`` holds that ``points`` do not fill. The hull…, Where a block might be cut in two: a direction, and a point to pass through.…, The greedy split, with every count along the way kept. The same walk…

### Community 95 - "TriangleIndex"
Cohesion: 0.29
Nodes (6): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., Leaf bounding boxes over a Morton-sorted triangle list., TriangleIndex, test_an_empty_index_returns_no_candidates()

### Community 96 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 97 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 98 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 99 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 100 - ".refresh_list"
Cohesion: 0.40
Nodes (3): QTreeWidgetItem, Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing.

### Community 101 - "coarse_lattice"
Cohesion: 0.33
Nodes (6): app(), coarse_lattice(), fixture, MonkeyPatch, One Qt application for the whole run; offscreen, so CI needs no display.…, Read every model on a small lattice, so the suite stays quick.

### Community 103 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 104 - "._commit_node_drag"
Cohesion: 0.13
Nodes (7): Track the node and bone under the cursor; True when anything changed., Record the finished drag as a single undo step., Record the finished gesture: a move, a resize, or a plain click. A press that…, Record the finished drag as one step, or read a press as a selection., Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…, Track whatever the cursor is over, so the overlay can respond.

### Community 105 - "._upload_sculpt"
Cohesion: 0.33
Nodes (3): Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on.

### Community 107 - "._place_armature_node"
Cohesion: 0.25
Nodes (3): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 112 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 113 - "ArmaturePanel"
Cohesion: 0.15
Nodes (6): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Add an empty armature and select it., Begin a preset run against a fresh armature., Take back the landmark before this one and ask for it again., The multiplier the position boxes are read and written through.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `FilmRecorder`, `plane_axes.py`, `ViewerState`, `OrientationSettings`, `mesh_renderer.py`, `test_plane_film.py`, `SectionSettings`, `SectionPanel`, `test_plane_clusters.py`, `ndarray`, `picking.py`, `mesh.py`, `compute_vertex_normals`, `._accumulate_ghost`, `MeshBuffers`, `plane_solids.py`, `core/__init__.py`, `plane_volume.py`, `viewport.py`, `ndarray`, `PlaneMode`, `stone_field`, `test_plane_solids.py`, `raycast_mesh`, `record`, `PlaneSettings`, `auto_smooth`, `rounded`, `test_spatial.py`, `ball`, `TriangleIndex`?**
  _High betweenness centrality (0.143) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `viewport.py`, `FilmRecorder`, `AnnotateTool`, `main_window.py`, `MainWindow`, `ViewerState`, `._arm`, `._buried_nodes`, `MeasureTool`, `._place_armature_node`, `._commit_node_drag`, `._upload_sculpt`, `ArmatureTool`, `ViewportOverlay`, `._picker`, `NavigationController`, `.mousePressEvent`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera` to `viewport.py`, `test_camera.py`, `picking.py`, `ViewerState`, `ndarray`, `.copy`, `SceneRenderer`, `camera.py`, `README.md`, `._accumulate_ghost`, `mesh_renderer.py`, `ArmatureTool`, `ViewportOverlay`, `BookmarkStore`, `NavigationController`, `core/__init__.py`, `test_session.py`, `._draw_hud`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `PlaneSettings` (e.g. with `Film` and `Stage`) actually correct?**
  _`PlaneSettings` has 6 INFERRED edges - model-reasoned connections that need verification._