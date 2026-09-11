# Graph Report - reference-viewer  (2026-09-11)

## Corpus Check
- 92 files · ~297,007 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2600 nodes · 5844 edges · 121 communities (118 shown, 3 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 212 edges (avg confidence: 0.58)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `069cca0f`
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
- spatial.py
- Measurement
- SceneRenderer
- _wires
- camera.py
- gltf_loader.py
- Armature
- README.md
- SetAttributes
- planes_panel.py
- AccumTarget
- CameraPanel
- coarse_lattice
- ShaderProgram
- ViewportOverlay
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- NavigationController
- SectionSettings
- SectionPanel
- test_session.py
- Session
- ShadingPanel
- Panel
- test_camera.py
- test_plane_clusters.py
- WakeLock
- ndarray
- History
- update_check.py
- picking.py
- test_mesh_io.py
- Camera
- test_armature.py
- ArmatureNode
- UpdateChecker
- .split_point
- obj_loader.py
- landmarks.py
- Agent Graph-First Instructions
- MeshBuffers
- plane_clusters.py
- Texture2D
- Landmark
- SliderSpin
- OrientationSettings
- Mesh
- test_navigation.py
- PlaneAxes
- PlanesPanel
- Bounds
- clay_lumps
- Path
- .update_enabled
- _shifts
- MatcapPanel
- core/__init__.py
- ndarray
- plane_volume.py
- mesh_renderer.py
- stone_field
- main_window.py
- test_plane_solids.py
- application.py
- raycast_mesh
- Projection
- ArmatureStore
- AnnotatePanel
- _corner_facings
- ._selected_landmark
- MeshLoadError
- BoneLabels
- ArmatureTool
- PlaneSettings
- ._selected
- load_obj
- box
- ._start_update_check
- ._picker
- ._build
- section_segments
- .point
- test_spatial.py
- .mousePressEvent
- ShadingMode
- block_splits
- TriangleIndex
- ndarray
- environment.yml
- release.yml
- shaders.py
- .refresh_list
- coarse_lattice
- CHANGELOG.md
- wakelock.py
- ._commit_node_drag
- ._sync_scene
- section.py
- ._place_armature_node
- .surface_opacity
- _ScreenSaverBackend
- _WindowsBackend
- union_field
- refview/__init__.py
- ArmaturePanel
- _MacBackend
- ModelPanel
- lumpy
- QualitySettings
- .__init__
- kept_off
- _wire_frame

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 120 edges
2. `Camera` - 75 edges
3. `Viewport` - 75 edges
4. `Armature` - 73 edges
5. `PlaneSettings` - 67 edges
6. `ArmaturePanel` - 60 edges
7. `ViewerState` - 52 edges
8. `ArmatureTool` - 51 edges
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
- `Every document edit is a command` --rationale_for--> `SetAttributes`  [EXTRACTED]
  README.md → src/refview/core/commands.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **The bundled matcap set** — resources_matcaps_clay_terracotta_matcap, resources_matcaps_charcoal_matcap, resources_matcaps_jade_matcap, resources_matcaps_steel_matcap, resources_matcaps_studio_white_matcap, resources_matcaps_wax_skin_matcap, tools_generate_matcaps_matcappreset, tools_generate_matcaps_render [INFERRED 0.85]
- **The four generic undo commands** — src_refview_core_commands_setattributes, src_refview_core_commands_additem, src_refview_core_commands_removeitem, src_refview_core_commands_replaceitems, src_refview_core_history_command, readme_every_edit_is_a_command [EXTRACTED 1.00]
- **Windows binary-compatibility decisions** — readme_pyside6_pinned_below_68, environment_pip_installed_binaries, environment_python_311, github_workflows_release_pyinstaller_build [INFERRED 0.75]

## Communities (121 total, 3 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.06
Nodes (38): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+30 more)

### Community 1 - "Film"
Cohesion: 0.09
Nodes (14): QThread, Film, The stage at ``index``, clamped to what has actually been recorded., A whole making, from the coarsest stage to the one the slider asks for. Held by…, QObject, The film being recorded, or the last one finished., The film already held for ``key``, if there is one., Stop any recording in flight and forget what it was making. The thread is asked… (+6 more)

### Community 2 - "Release"
Cohesion: 0.18
Nodes (15): check_for_update(), fetch_latest_release(), RuntimeError, The release could not be looked up (offline, rate limited, malformed)., The newest published release, as GitHub describes it., Return the newest published release, or raise :class:`UpdateCheckError`., The newest release when it is later than ``current_version``, else ``None``., Release (+7 more)

### Community 3 - "Viewport"
Cohesion: 0.11
Nodes (10): QOpenGLWidget, Slide the view so a point sits at the centre, keeping the angle., Slide the view so a measurement sits at the centre, keeping the angle., End any film being recorded, and wait for its thread to really stop. For…, Free every GL object while the owning context is still current., Arm one tool, disarming the rest. Only one gesture can own the left button, so…, Drop whatever gesture is half-finished, without disarming the tool., Renders the scene and turns mouse gestures into camera and tool actions. (+2 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - "AnnotateTool"
Cohesion: 0.09
Nodes (18): AnnotateMode, AnnotationSettings, Enum, str, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a…, AnnotateTool (+10 more)

### Community 6 - "MainWindow"
Cohesion: 0.08
Nodes (11): QAction, QMainWindow, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits., Keep the menu entry agreeing with the panel's own checkbox. (+3 more)

### Community 7 - "ViewerState"
Cohesion: 0.09
Nodes (17): Session file that sits beside a model, e.g. ``bust.refview.json``., sidecar_path(), ndarray, Path, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it. (+9 more)

### Community 8 - "spatial.py"
Cohesion: 0.24
Nodes (8): _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Build the index from expanded triangle corners, shape ``(T, 3, 3)``., Triangle indices worth intersecting for this ray, possibly empty., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the…, Interleave each 10-bit value with two zero bits, ready to be shifted., _spread_bits()

### Community 9 - "Measurement"
Cohesion: 0.11
Nodes (12): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+4 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.10
Nodes (27): Everything the viewport needs in order to draw a frame., RenderSettings, key_world_direction(), light_directions(), light_view_projection(), normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`… (+19 more)

### Community 11 - "_wires"
Cohesion: 0.11
Nodes (32): The order the artist put the bones in is what the scrub walks through, which is…, The claim the whole film rests on, asked again with an armature under it: an…, test_a_film_of_clay_on_a_wire_lays_it_down_in_the_order_it_was_listed(), test_the_last_stage_of_a_film_on_a_wire_is_the_form_the_slider_gives(), _bar(), _bed_for(), _holds(), A long ellipsoid: one closed form with an obvious axis to lie along. (+24 more)

### Community 12 - "camera.py"
Cohesion: 0.19
Nodes (16): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-…, Return ``v`` scaled to unit length, or ``fallback`` for a zero vector. (+8 more)

### Community 13 - "gltf_loader.py"
Cohesion: 0.14
Nodes (24): _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry(), _primitives(), ndarray (+16 more)

### Community 14 - "Armature"
Cohesion: 0.05
Nodes (46): Point3, Armature, Bone, PlacedLandmark, A graph of named points under the form, and the wire it stands for. An armature…, The end that is not ``index``., One anatomical point the artist put on the model during a guided run., A graph of nodes and the bones joining them. When it came from a preset the… (+38 more)

### Community 15 - "README.md"
Cohesion: 0.24
Nodes (10): Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets, render owns every GL call (+2 more)

### Community 16 - "SetAttributes"
Cohesion: 0.19
Nodes (6): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Run a row's edit once Qt has finished delivering the current signal. Committing…, Record an edit the viewport's tool worked out., Join two nodes of one armature, if they are two and they are one armature., Commit a renamed or re-checked row, if anything actually changed.

### Community 17 - "planes_panel.py"
Cohesion: 0.09
Nodes (23): QFormLayout, QGroupBox, Shared plumbing for the dockable side panels., Dockable control panels., Matcap selection and colour grading., What was imported and which way up it should stand., Everything that acts on the shading normals rather than on the shading. Faceted…, Cross-section controls: the cutting plane, what it keeps and how it reads. (+15 more)

### Community 18 - "AccumTarget"
Cohesion: 0.08
Nodes (16): AccumTarget, ColorTarget, DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality and ghost passes. Four of…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the…, The pair of buffers a see-through model is summed into. Attachment 0 holds the… (+8 more)

### Community 19 - "CameraPanel"
Cohesion: 0.12
Nodes (7): CameraPanel, QListWidgetItem, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 21 - "ShaderProgram"
Cohesion: 0.12
Nodes (9): OpenGL rendering layer: shader programs, textures and the scene renderer., ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError (+1 more)

### Community 22 - "ViewportOverlay"
Cohesion: 0.08
Nodes (31): QColor, QPainter, QPointF, MeasureTool, Handle, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any. (+23 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.07
Nodes (25): app(), _names(), panel(), fixture, The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as… (+17 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.14
Nodes (8): MeasurePanel, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn.

### Community 25 - "BookmarkStore"
Cohesion: 0.15
Nodes (7): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., test_bookmarks_cycle_and_wrap()

### Community 26 - "NavigationController"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "SectionSettings"
Cohesion: 0.21
Nodes (14): Cross-section tool (1.1.0), How the model is cut open, and how the cut is drawn., SectionSettings, _box(), Cutting planes, the contour they produce and the pedestal under the model., A closed axis-aligned cube centred on the origin., The contour of a plane through a cube is its cross-section outline., test_a_custom_normal_is_normalised() (+6 more)

### Community 28 - "SectionPanel"
Cohesion: 0.21
Nodes (6): Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 29 - "test_session.py"
Cohesion: 0.11
Nodes (17): Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., A step of the slider is worth a fixed share more planes, not a fixed number of…, The ceiling went from 64 planes to 256 without moving the slider under anyone:…, The panel edits the settings; the fit has to be told what they are., Both modes answer in degrees of turn, so the panel can just ask., Version 1 files predate the annotation layer and the endpoint lock., Deletion goes through the undo stack, so the store only tracks position. (+9 more)

### Community 30 - "Session"
Cohesion: 0.15
Nodes (15): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Path (+7 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.18
Nodes (9): LightSettings, A key light, an opposing fill and a hemispherical ambient term., Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Show what this mode is actually lit and shaded by, and hide the rest. A matcap… (+1 more)

### Community 32 - "Panel"
Cohesion: 0.12
Nodes (11): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only., Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block. (+3 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.07
Nodes (48): angle_deg(), bent_plate(), cube(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What…, How far the least well served of ``wanted`` is from anything offered. (+40 more)

### Community 35 - "WakeLock"
Cohesion: 0.17
Nodes (13): Holds sleep off while the window that owns it is the one in front. The class…, WakeLock, Broken, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do., A platform that refuses, the way an old or locked-down one might., The viewer must open and close normally on a machine that says no., Recorder (+5 more)

### Community 36 - "ndarray"
Cohesion: 0.13
Nodes (21): _back_inside(), dual_contour(), _flat_mesh(), ndarray, The surface where ``value`` changes sign, one vertex per lattice cell. Each…, The gradient of a lattice field, by central differences. Which is the direction…, Drop the loose pieces, keeping the form and anything of its size. A block is a…, Read lattice fields at places between their corners, straight-line. Nearest-… (+13 more)

### Community 37 - "History"
Cohesion: 0.09
Nodes (20): Camera motion is deliberately not undoable, AddItem, Append an item to a document list., Command, History, One reversible change, named for the undo menu., A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive… (+12 more)

### Community 38 - "update_check.py"
Cohesion: 0.19
Nodes (15): is_newer(), _padded(), parse_version(), Ask GitHub whether a newer release exists. The check is deliberately small and…, Numeric components of ``text``, or ``None`` when it is not a version. A pre-…, Whether ``candidate`` is a strictly later version than ``current``., Pull the tag and page link out of a GitHub release document., release_from_payload() (+7 more)

### Community 39 - "picking.py"
Cohesion: 0.23
Nodes (11): Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays., snap_to_vertex() (+3 more)

### Community 40 - "test_mesh_io.py"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

### Community 41 - "Camera"
Cohesion: 0.09
Nodes (16): Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Screen-to-world scale at the focal plane; identical in both modes., Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole. (+8 more)

### Community 42 - "test_armature.py"
Cohesion: 0.08
Nodes (55): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _derived(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer. (+47 more)

### Community 43 - "ArmatureNode"
Cohesion: 0.09
Nodes (22): ArmatureNode, The graph with ``node`` appended, optionally joined to an existing one., The graph with a node dropped into the middle of a bone. The bone becomes two,…, One joint of the wire: where it is, and how thick the form is there., _chain(), A straight run of nodes one unit apart along +X., Nothing stands between one neighbour, so there is nothing to bridge., test_a_bone_at_the_end_of_the_list_cannot_be_moved_off_it() (+14 more)

### Community 44 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 45 - ".split_point"
Cohesion: 0.20
Nodes (9): BoneRef, _project(), The nearest bone under the cursor, for showing its length., Where on a bone a click at ``(x, y)`` landed. The share along the bone is read…, A world point in widget pixels, or ``None`` when it is behind the camera., How far along a screen-space segment the cursor's nearest point lies., Pixels from the cursor to the segment, or ``None`` if either end is behind., _segment_distance() (+1 more)

### Community 46 - "obj_loader.py"
Cohesion: 0.22
Nodes (14): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), ndarray, Minimal, dependency-free Wavefront OBJ reader. Only the geometry statements a…, Resolve ``v``, ``v/vt``, ``v//vn`` or ``v/vt/vn`` corners to 0-based pairs.… (+6 more)

### Community 47 - "landmarks.py"
Cohesion: 0.10
Nodes (27): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), median_plane(), _mid(), mirror_point() (+19 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "MeshBuffers"
Cohesion: 0.10
Nodes (9): MeshBuffers, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Whichever geometry is standing for the model this frame., Fill the shader's table with a level, if it is not already in it., Replace the annotation geometry; pass an empty list to hide it., Sum a see-through model into the ghost buffers, to be resolved after. Blending…, Vertex/index buffers for one mesh, bound through a single VAO. (+1 more)

### Community 50 - "plane_clusters.py"
Cohesion: 0.07
Nodes (39): How much surface each vertex stands for: a third of each triangle on it.…, vertex_weights(), _compact(), _consensus(), _cut(), _first_planes(), _fit(), flatness() (+31 more)

### Community 51 - "Texture2D"
Cohesion: 0.10
Nodes (12): DataTexture, default_matcap_pixels(), MatcapLoadError, ndarray, RuntimeError, Matcap texture loading and upload, and the small data table beside it., An RGBA8 2D texture with clamped edges and mipmapped minification., Raised when an image cannot be used as a matcap. (+4 more)

### Community 52 - "Landmark"
Cohesion: 0.11
Nodes (14): _humanoid_landmarks(), Landmark, _node_name(), Preset, The landmarks worth asking for under these choices. With mirroring on the…, The midline landmarks, which are what the median plane is fitted to., The midline first, then each pair left before right., What to call a landmark in a menu or an undo step. The preset's own words when… (+6 more)

### Community 53 - "SliderSpin"
Cohesion: 0.10
Nodes (11): QFrame, CollapsibleGroup, PointEdit, QWidget, Re-scale the control, e.g. once a model's size is known., Grow the slider to take in a value from beyond its end., Three spin boxes for one point in space. Keyboard tracking is off, so a typed…, Match the arrows to the size of the thing being moved. (+3 more)

### Community 54 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 55 - "Mesh"
Cohesion: 0.04
Nodes (70): auto_smooth(), compute_vertex_normals(), _gathered(), Mesh, Triangle-mesh containers shared by the loader, the renderer and picking., Return a copy whose bounding-box centre sits at the origin., Which group each of ``total`` things lands in, given pairs that agree. Hooking…, A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.… (+62 more)

### Community 56 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 57 - "PlaneAxes"
Cohesion: 0.12
Nodes (11): _empty(), PlaneAxes, ndarray, A level with no place in it: nearest direction wins, as before., The planes a model falls into, at every count. Built once per mesh and per…, The best ``count`` planes, or as many as the model supports. A model whose…, The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to. (+3 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.06
Nodes (32): _along(), lattice_fineness(), plane_count(), Where a detail setting sits on its slider, 0 to 1., How much finer than usual a detail setting asks the lattice to be. One at the…, How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., How much of a turn in the surface one plane covers, in degrees. Linear in…, How many planes a mode fitted to the model keeps. The climb from two planes to… (+24 more)

### Community 59 - "Bounds"
Cohesion: 0.18
Nodes (15): Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray, A turntable-style disc the model can stand on. A ground plane gives the eye… (+7 more)

### Community 60 - "clay_lumps"
Cohesion: 0.16
Nodes (18): _box_facings(), clay_lumps(), clay_pieces(), fit_piece(), _frame(), grow_piece(), join_pieces(), Which three ways a lump of material runs. Columns, thinnest first. Thinnest… (+10 more)

### Community 61 - "Path"
Cohesion: 0.29
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 62 - ".update_enabled"
Cohesion: 0.14
Nodes (7): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., The armature the selected row stands for, when the row is not a node., Follow the highlighted row, without rebuilding the list underneath it. Going…, Highlight the row for a node picked in the view., Highlight the row for a landmark picked in the view.

### Community 63 - "_shifts"
Cohesion: 0.25
Nodes (8): _balloon(), close_gaps(), outside_points(), Fill the slots the lumps leave between them, without taking clay away. The…, Grow or shrink a solid by ``reach`` cells, one axis at a time. A separable…, Where the model stops: the corners just outside ``room``. ``(n, 3)``. Only the…, The pair of slices that read a lattice ``span`` cells over along ``axis``., _shifts()

### Community 64 - "MatcapPanel"
Cohesion: 0.18
Nodes (8): QIcon, QScrollArea, MatcapPanel, Rebuild the thumbnail list from the resources folder., Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, scrollable()

### Community 65 - "core/__init__.py"
Cohesion: 0.09
Nodes (23): Freehand annotations painted onto the model surface. A stroke is a polyline of…, Named camera positions the artist can jump between while sculpting., Qt-free geometry, camera and document model for the reference viewer., MeasurementSettings, Named point-to-point measurements and their presentation options., How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., Enum (+15 more)

### Community 66 - "ndarray"
Cohesion: 0.20
Nodes (4): ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, test_bounds_of_an_empty_point_set()

### Community 67 - "plane_volume.py"
Cohesion: 0.18
Nodes (15): _axes(), encloses(), lattice(), lay_bed(), nearest_surface(), _passes(), Blocking a form in out of its own planes, from the outside or from a core. A…, Read the model onto a lattice, ready for solids to be laid on it. (+7 more)

### Community 68 - "mesh_renderer.py"
Cohesion: 0.10
Nodes (16): Unit vector for an azimuth/elevation pair, with +Y as the pole., spherical_direction(), fit_planes(), The planes of ``mesh`` under ``mode``; empty where the mode needs none., PlaneMode, How the plane directions are arrived at. ``shader_id`` must stay in sync with…, Whether the directions are read off the model rather than imposed., Whether the mode reads the design matrix, and so its coefficients. Grid reads… (+8 more)

### Community 69 - "stone_field"
Cohesion: 0.20
Nodes (10): Bed, block_bounds(), coarse_bounds(), point_support(), The lattice a form is worked on, and the model read onto it. Everything here…, The union of the blocks a labelling cuts the model into, and its facings. Stone…, The index range each block covers. ``(count, 3)`` lows and highs, inclusive. A…, Those ranges, read on the fine lattice the coarse one stands for. (+2 more)

### Community 70 - "main_window.py"
Cohesion: 0.11
Nodes (16): Every document edit is a command, The handful of undoable edits the whole application is built from.…, Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, lock_icon() (+8 more)

### Community 71 - "test_plane_solids.py"
Cohesion: 0.04
Nodes (89): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), A flat with a scattering of bad normals is still shaded as that flat. Averaging…, test_strays_inside_a_plane_do_not_tilt_it(), block(), coarse_lattice() (+81 more)

### Community 72 - "application.py"
Cohesion: 0.07
Nodes (50): ArgumentParser, Color, Namespace, QApplication, QPixmap, QSplashScreen, Charcoal matcap, Terracotta clay matcap (+42 more)

### Community 73 - "raycast_mesh"
Cohesion: 0.23
Nodes (11): Return the closest front- or back-facing hit along the ray, or ``None``., raycast_mesh(), fixture, quad(), Ray/mesh intersection and vertex snapping., Two triangles covering the unit square on the z = 0 plane., test_closest_of_two_surfaces_wins(), test_hits_the_surface() (+3 more)

### Community 74 - "Projection"
Cohesion: 0.15
Nodes (7): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., Projection, Enum, str, Projection used by :class:`Camera`., test_serialisation_round_trip()

### Community 75 - "ArmatureStore"
Cohesion: 0.15
Nodes (5): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied., QObject

### Community 76 - "AnnotatePanel"
Cohesion: 0.24
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 77 - "_corner_facings"
Cohesion: 0.40
Nodes (6): _corner_facings(), facings(), fitted_facings(), Twenty-six directions round a cube, for judging how much air a block holds.…, The supporting directions a block may be cut along. ``(m, 3)``. The twenty-six…, The form's own facings alone, both ways round and without duplicates. What a…

### Community 78 - "._selected_landmark"
Cohesion: 0.12
Nodes (7): Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors., Show the landmark group only once there are landmarks to show., The landmark the highlighted row stands for, if the row is one., Which armature the landmark list is pointing into, row or heading., Follow the highlighted landmark, and say which one it is in the view.

### Community 79 - "MeshLoadError"
Cohesion: 0.17
Nodes (15): STL corner welding, MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., _ascii_corners(), _binary_corners(), load_stl(), ndarray (+7 more)

### Community 80 - "BoneLabels"
Cohesion: 0.29
Nodes (6): BoneLabels, Buried, Enum, str, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…

### Community 81 - "ArmatureTool"
Cohesion: 0.06
Nodes (41): LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, Handle, The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now., How many landmarks are placed, out of how many will be asked for. (+33 more)

### Community 82 - "PlaneSettings"
Cohesion: 0.04
Nodes (73): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor…, The grid step, in cube-face coordinates, that gives that span. A cell of this…, The design-matrix settings, in the form the fitters want them., Roughly how much of a turn one of those planes covers, in degrees., The plane size of whichever mode is running. (+65 more)

### Community 83 - "._selected"
Cohesion: 0.24
Nodes (4): Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., Run a bone between the row selected now and the node held before it., The node the selected row stands for, if the row is a node at all.

### Community 84 - "load_obj"
Cohesion: 0.22
Nodes (14): _load_generic(), load_obj(), ObjLoadError, Path, Line-by-line reader for files the fast path declines., Raised when a file cannot be interpreted as an OBJ mesh., Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, OBJ parsing: normals, triangulation and index handling. (+6 more)

### Community 85 - "box"
Cohesion: 0.50
Nodes (4): box(), A unit cube, shaded flat: six planes and twelve right angles., Every edge of a cube is a right angle, and no reading of AutoSmooth short of…, test_autosmooth_leaves_a_real_plane_change_hard()

### Community 86 - "._start_update_check"
Cohesion: 0.29
Nodes (4): Ask GitHub for the newest release in the background. The startup check is…, QWidget, show_failure_dialog(), show_up_to_date_dialog()

### Community 87 - "._picker"
Cohesion: 0.20
Nodes (4): Orbit increment while Shift is held, or 0 for a free orbit., Rub out the stroke points under the eraser, live., Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor.

### Community 88 - "._build"
Cohesion: 0.29
Nodes (6): QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 89 - "section_segments"
Cohesion: 0.18
Nodes (9): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, Unit axis, or ``None`` for a custom direction., A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., section_segments() (+1 more)

### Community 90 - ".point"
Cohesion: 0.22
Nodes (5): ndarray, Closest surface intersection under the cursor, or ``None``., Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-…, Screen-to-world scale at a given depth along the view direction.

### Community 91 - "test_spatial.py"
Cohesion: 0.33
Nodes (8): _grid(), The picking accelerator: it must be fast without changing any answer., A bumpy height field, so rays hit different triangles at different depths., The pruned candidate set must never miss the true intersection., test_a_ray_that_misses_the_model_is_pruned_away(), test_every_triangle_lands_in_exactly_one_leaf(), test_the_index_finds_the_triangle_a_ray_actually_hits(), test_the_index_is_built_once_and_kept()

### Community 92 - ".mousePressEvent"
Cohesion: 0.18
Nodes (5): ndarray, Object centre, which anchors the plane the orbit pivot lies on., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…, Take hold of a landmark, to move it or just to say which one it is.

### Community 93 - "ShadingMode"
Cohesion: 0.17
Nodes (6): PlaneTarget, str, What the planes filter is allowed to act on. The two are mutually exclusive…, Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode

### Community 94 - "block_splits"
Cohesion: 0.17
Nodes (12): block_labels(), block_splits(), blocks(), _cuts(), _hull_air(), The corners a hull round ``points`` holds that ``points`` do not fill. The hull…, Where a block might be cut in two: a direction, and a point to pass through.…, The greedy split, with every count along the way kept. The same walk… (+4 more)

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

### Community 102 - "CHANGELOG.md"
Cohesion: 0.20
Nodes (9): Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL and glTF import (1.1.0), Units are adopted, never guessed, MeshUnits (+1 more)

### Community 103 - "wakelock.py"
Cohesion: 0.22
Nodes (7): _Backend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The backend for this machine, or a do-nothing one if it cannot be had., A way of asking one platform to stay awake., Ask for sleep to be held off., Withdraw the request.

### Community 104 - "._commit_node_drag"
Cohesion: 0.14
Nodes (7): Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Record the finished drag as a single undo step., Record the finished gesture: a move, a resize, or a plain click. A press that…, Record the finished drag as one step, or read a press as a selection., Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…

### Community 105 - "._sync_scene"
Cohesion: 0.12
Nodes (6): Regenerate the pedestal and the cut contour when their settings move. Both are…, The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on., Cut the mesh with each section plane and expand the result to strokes.

### Community 106 - "section.py"
Cohesion: 0.27
Nodes (7): Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Which side of the plane survives the cut., SectionAxis, SectionMode

### Community 107 - "._place_armature_node"
Cohesion: 0.22
Nodes (4): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…, The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…

### Community 109 - "_ScreenSaverBackend"
Cohesion: 0.22
Nodes (4): The freedesktop screensaver service, which hands back a cookie., Hold sleep off, or stop holding it, whichever is not already true., Drop the request, if one is out. Safe to call more than once., _ScreenSaverBackend

### Community 110 - "_WindowsBackend"
Cohesion: 0.25
Nodes (5): skipif, ``SetThreadExecutionState``: a flag on this thread, not a handle. The flags…, _WindowsBackend, The flag the viewer sets is the one Windows reports back afterwards., test_windows_really_sets_the_execution_state()

### Community 111 - "union_field"
Cohesion: 0.25
Nodes (8): block_field(), piece_bounds(), One row of coordinates per axis over ``box``, shaped so they broadcast., The union of the blocks, as a field whose zero is its surface. Each block is…, The box a lump of clay lives in, read off the six facings of its frame. Those…, The union of a set of convex solids, as a field whose zero is its surface. The…, _rows(), union_field()

### Community 112 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 113 - "ArmaturePanel"
Cohesion: 0.15
Nodes (6): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Add an empty armature and select it., Begin a preset run against a fresh armature., Take back the landmark before this one and ask for it again., The multiplier the position boxes are read and written through.

### Community 114 - "_MacBackend"
Cohesion: 0.33
Nodes (3): c_void_p, _MacBackend, An IOKit power assertion, held by id until it is released.

### Community 116 - "lumpy"
Cohesion: 0.33
Nodes (6): lumpy(), A form with real planes in it, and more than one facing the same way., The coefficients have to reach the fit, and reaching it has to show. Two planes…, The fit and the shader have to agree, or the boundaries drawn are not the…, test_a_coefficient_of_zero_takes_the_term_out_of_the_shader_too(), test_leaning_on_position_breaks_a_form_up_as_well_as_down()

### Community 117 - "QualitySettings"
Cohesion: 0.50
Nodes (5): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, QualitySettings, Soft shadows and ambient occlusion for the high-quality mode. Both are screen-…

### Community 119 - "kept_off"
Cohesion: 0.50
Nodes (4): kept_off(), Which points lie in the sleeve a length of wire declares round itself. The wire…, Which material lies under a length of wire that is to take no clay. Turning a…, within_sleeve()

### Community 120 - "_wire_frame"
Cohesion: 0.50
Nodes (4): _perpendicular(), Two unit directions across ``along``, neither of them near it., Which three ways a lump laid along a wire runs. Columns, thinnest first. The…, _wire_frame()

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `Film`, `plane_axes`, `ViewerState`, `_wires`, `gltf_loader.py`, `README.md`, `SectionSettings`, `test_plane_clusters.py`, `ndarray`, `picking.py`, `test_mesh_io.py`, `obj_loader.py`, `MeshBuffers`, `plane_clusters.py`, `OrientationSettings`, `PlaneAxes`, `Bounds`, `core/__init__.py`, `ndarray`, `plane_volume.py`, `mesh_renderer.py`, `stone_field`, `test_plane_solids.py`, `raycast_mesh`, `MeshLoadError`, `PlaneSettings`, `load_obj`, `box`, `section_segments`, `test_spatial.py`, `TriangleIndex`, `CHANGELOG.md`, `section.py`, `lumpy`?**
  _High betweenness centrality (0.139) - this node is a cross-community bridge._
- **Why does `Armature` connect `Armature` to `ndarray`, `core/__init__.py`, `main_window.py`, `test_armature.py`, `ArmatureStore`, `ArmatureNode`, `.split_point`, `._selected_landmark`, `ArmatureTool`, `ArmaturePanel`, `test_planes_panel.py`, `ViewportOverlay`, `Mesh`, `.update_enabled`, `Session`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera` to `SceneRenderer`, `camera.py`, `README.md`, `CameraPanel`, `ViewportOverlay`, `BookmarkStore`, `NavigationController`, `test_session.py`, `Session`, `test_camera.py`, `picking.py`, `MeshBuffers`, `test_navigation.py`, `Bounds`, `core/__init__.py`, `mesh_renderer.py`, `Projection`, `ArmatureStore`, `ArmatureTool`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 20 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Armature` (e.g. with `SculptCache` and `Session`) actually correct?**
  _`Armature` has 2 INFERRED edges - model-reasoned connections that need verification._