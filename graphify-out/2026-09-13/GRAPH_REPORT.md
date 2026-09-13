# Graph Report - reference-viewer  (2026-09-13)

## Corpus Check
- 106 files · ~397,343 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3349 nodes · 7729 edges · 142 communities (138 shown, 4 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 348 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1fe1e4ee`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FormTool
- PlaneAxes
- update_check.py
- Viewport
- plane_axes
- main_window.py
- MainWindow
- Stroke
- GifWriter
- Measurement
- SceneRenderer
- ball
- camera.py
- _wires
- Armature
- mesh.py
- .apply_session
- FormStore
- AccumTarget
- CameraPanel
- UpdateChecker
- ShaderProgram
- ViewportOverlay
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- NavigationController
- SectionSettings
- SectionPanel
- viewport.py
- VideoError
- ShadingPanel
- ArmatureTool
- test_camera.py
- test_plane_clusters.py
- WakeLock
- ndarray
- AddItem
- render/__init__.py
- film_export.py
- SurfacePicker
- Camera
- test_armature.py
- RenderSettings
- gltf_loader.py
- ExportVideoDialog
- VideoSettings
- landmarks.py
- Agent Graph-First Instructions
- MeshBuffers
- mesh_renderer.py
- Texture2D
- PlacedLandmark
- test_plane_solids.py
- OrientationSettings
- PlaneSettings
- FilmExport
- FormsPanel
- PlanesPanel
- Landmark
- ArmatureSettings
- SliderSpin
- .update_enabled
- form_shapes.py
- FormSettings
- overlay.py
- Mesh
- PrimaryForm
- History
- compute_vertex_normals
- AnnotatePanel
- plane_regions
- Release
- record
- convex.py
- ._build
- application.py
- test_forms.py
- ._selected_landmark
- ViewerState
- session.py
- ArmatureNode
- core/__init__.py
- ._build
- test_forms_panel.py
- TriangleIndex
- MeshLoadError
- ._picker
- ArmaturePanel
- .pan
- wakelock.py
- ._delete_selected
- .mousePressEvent
- Side
- ._selected
- .update_enabled
- clay_lumps
- test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else
- _Encoder
- picking.py
- .refresh_list
- ._upload_sculpt
- Path
- CHANGELOG.md
- SetAttributes
- Projection
- _ScreenSaverBackend
- ._place_armature_node
- test_mesh_io.py
- BoneLabels
- test_session.py
- plane_volume.py
- coarse_lattice
- stone_field
- ArmatureStore
- Wires
- ndarray
- _WindowsBackend
- ShadingMode
- ReplaceItems
- _shifts
- release.yml
- _MacBackend
- environment.yml
- _NameOnlyDelegate
- Session
- panel
- sidecar_path
- refview/__init__.py
- RemoveItem
- ndarray
- orientation.py
- .stage_images
- ._place_form_landmark
- .refresh_list
- ModelPanel
- ._back_point
- _NameOnlyDelegate
- _wire_frame
- plane_count
- .plane_point
- app

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 143 edges
2. `Viewport` - 101 edges
3. `PrimaryForm` - 77 edges
4. `Camera` - 75 edges
5. `Armature` - 73 edges
6. `PlaneSettings` - 67 edges
7. `ArmaturePanel` - 62 edges
8. `FormsPanel` - 61 edges
9. `ViewerState` - 61 edges
10. `PlacedLandmark` - 60 edges

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

## Communities (142 total, 4 thin omitted)

### Community 0 - "FormTool"
Cohesion: 0.09
Nodes (12): FormLandmarkRef, FormRun, FormTool, ndarray, Begin a run against a form already in the store., Where a click at ``(x, y)`` would put a landmark: on the surface, or nowhere.…, Where a grabbed landmark should move to. Free placement -- and a drag that…, The nearest grabbable landmark under the cursor, if any. Only the ones on… (+4 more)

### Community 1 - "PlaneAxes"
Cohesion: 0.12
Nodes (11): _empty(), PlaneAxes, ndarray, A level with no place in it: nearest direction wins, as before., The planes a model falls into, at every count. Built once per mesh and per…, The best ``count`` planes, or as many as the model supports. A model whose…, The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to. (+3 more)

### Community 2 - "update_check.py"
Cohesion: 0.14
Nodes (22): check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed). (+14 more)

### Community 3 - "Viewport"
Cohesion: 0.07
Nodes (15): QOpenGLWidget, Slide the view so a point sits at the centre, keeping the angle., A form changed: work its clay out again and redraw., Slide the view so a measurement sits at the centre, keeping the angle., Regenerate the pedestal and the cut contour when their settings move. Both are…, End any film being recorded, and wait for its thread to really stop. For…, The armature the clay is to be built on, if one was chosen. Read here rather…, The film of the form's making, as far as it has been recorded. (+7 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - "main_window.py"
Cohesion: 0.06
Nodes (43): QGroupBox, QScrollArea, The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, MatcapLoadError, RuntimeError, Matcap texture loading and upload, and the small data table beside it., Raised when an image cannot be used as a matcap. (+35 more)

### Community 6 - "MainWindow"
Cohesion: 0.06
Nodes (15): QAction, QMainWindow, QTabWidget, MainWindow, Wires the viewport, the panels and the document together., A checkbox on the tab that shows or hides what the panel draws. The same switch…, Keep every tab's switch agreeing with the panel it speaks for., Add a menu entry, optionally with a window-wide shortcut. (+7 more)

### Community 7 - "Stroke"
Cohesion: 0.06
Nodes (37): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+29 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "Measurement"
Cohesion: 0.12
Nodes (11): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+3 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.11
Nodes (21): light_directions(), normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.…, How see-through the model is this frame, or ``None`` if it is solid. Asked in…, Lay the summed ghost over the scene already in the frame. (+13 more)

### Community 11 - "ball"
Cohesion: 0.06
Nodes (44): coarse_lattice(), film_of(), fixture, MonkeyPatch, parametrize, Scrubbing through the making of a form, rather than only arriving at it. The…, A cut takes material away, so no stage of a carving is larger than the one…, The same the other way about: a lump adds material, so the form grows. (+36 more)

### Community 12 - "camera.py"
Cohesion: 0.14
Nodes (22): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-…, Return ``v`` scaled to unit length, or ``fallback`` for a zero vector. (+14 more)

### Community 13 - "_wires"
Cohesion: 0.09
Nodes (37): ndarray, The mesh's normals, made unit, with anything unusable recomputed., Points spread over the model closely enough for a lattice to feel it. The…, surface_seeds(), unit_normals(), The order the artist put the bones in is what the scrub walks through, which is…, The claim the whole film rests on, asked again with an armature under it: an…, test_a_film_of_clay_on_a_wire_lays_it_down_in_the_order_it_was_listed() (+29 more)

### Community 14 - "Armature"
Cohesion: 0.06
Nodes (30): Armature, Bone, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves., A plausible thickness for a node placed by hand., What to call a bone: its own name, or the two nodes it runs between. (+22 more)

### Community 15 - "mesh.py"
Cohesion: 0.18
Nodes (14): High Quality shading mode (1.1.0), core never imports Qt, Every document edit is a command, High Quality without ray tracing, Three-layer separation: core, render, ui, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets, The pedestal is ordinary geometry so it catches the shadow (+6 more)

### Community 16 - ".apply_session"
Cohesion: 0.16
Nodes (7): ndarray, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements, annotations,…, Rotate the measurements, annotations, armature and forms onto the turned model.…, Fit the current mesh in the view without changing the direction., Adopt a session's settings, leaving the loaded mesh alone.

### Community 17 - "FormStore"
Cohesion: 0.15
Nodes (5): FormStore, An ordered, named collection of forms, like the other stores., The live list; the undo commands operate on it directly., A name for a new form of this recipe, numbered past any it already has. A form…, test_a_form_store_names_forms_past_the_ones_it_has()

### Community 18 - "AccumTarget"
Cohesion: 0.08
Nodes (15): AccumTarget, ColorTarget, DepthTarget, GeometryTarget, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the…, The pair of buffers a see-through model is summed into. Attachment 0 holds the…, Empty both sums, and the depth nothing has been laid into yet. Zero starts each… (+7 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): CameraPanel, QListWidgetItem, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 21 - "ShaderProgram"
Cohesion: 0.14
Nodes (7): ndarray, RuntimeError, Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "ViewportOverlay"
Cohesion: 0.14
Nodes (22): QColor, QPainter, QPointF, project_visible(), Handle, QFont, Draws measurements, tool previews, the orientation gizmo and the readout., Burn a line into the bottom of a frame, for an exported clip. Which stage of… (+14 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.07
Nodes (25): app(), _names(), panel(), fixture, The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as… (+17 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.14
Nodes (8): MeasurePanel, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn.

### Community 25 - "BookmarkStore"
Cohesion: 0.12
Nodes (8): BookmarkStore, CameraBookmark, Named camera positions the artist can jump between while sculpting., A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., test_bookmarks_cycle_and_wrap()

### Community 26 - "NavigationController"
Cohesion: 0.10
Nodes (21): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Tracks an in-progress drag and applies it to a camera. (+13 more)

### Community 27 - "SectionSettings"
Cohesion: 0.08
Nodes (30): The cut interior is flooded flat, Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every… (+22 more)

### Community 28 - "SectionPanel"
Cohesion: 0.18
Nodes (6): Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 29 - "viewport.py"
Cohesion: 0.09
Nodes (30): planes_for(), The stages a form passes through on its way from a block to a figure. The…, How many solids each stage of a film is made of. Every count from the coarsest…, The detail setting that asks for ``solids``, or ``None`` if none does. The…, stage_counts(), block_count(), piece_count(), Handing the planes of a fit to the thing that actually works the volume. The… (+22 more)

### Community 30 - "VideoError"
Cohesion: 0.09
Nodes (15): _FFmpegWriter, ndarray, Path, RuntimeError, An export that could not be written, said in words for the artist., What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``. (+7 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.21
Nodes (7): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel

### Community 32 - "ArmatureTool"
Cohesion: 0.09
Nodes (12): LandmarkRef, ArmatureTool, Handle, Begin a preset run against an armature already in the store., Where a click at ``(x, y)`` would put a node. With free placement the node…, Where a grabbed node should move to. Free placement -- and a drag that wanders…, The thickness a resize drag is asking for: the cursor's reach, in world units., The nearest grabbable node under the cursor, if any. Only unlocked nodes of a… (+4 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (8): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_serialisation_round_trip(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (58): angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What… (+50 more)

### Community 35 - "WakeLock"
Cohesion: 0.17
Nodes (13): Holds sleep off while the window that owns it is the one in front. The class…, WakeLock, Broken, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do., A platform that refuses, the way an old or locked-down one might., The viewer must open and close normally on a machine that says no., Recorder (+5 more)

### Community 36 - "ndarray"
Cohesion: 0.13
Nodes (21): _back_inside(), dual_contour(), _flat_mesh(), ndarray, The surface where ``value`` changes sign, one vertex per lattice cell. Each…, The gradient of a lattice field, by central differences. Which is the direction…, Drop the loose pieces, keeping the form and anything of its size. A block is a…, Read lattice fields at places between their corners, straight-line. Nearest-… (+13 more)

### Community 37 - "AddItem"
Cohesion: 0.20
Nodes (13): AddItem, Append an item to a document list., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch(), test_commands_carry_their_channel_and_name() (+5 more)

### Community 38 - "render/__init__.py"
Cohesion: 0.33
Nodes (4): OpenGL rendering layer: shader programs, textures and the scene renderer., Thin wrapper around an OpenGL shader program., default_matcap_pixels(), A neutral studio matcap, used before the user picks one.

### Community 39 - "film_export.py"
Cohesion: 0.08
Nodes (26): _encode_arguments(), _encoders(), ffmpeg_path(), _no_window(), Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a… (+18 more)

### Community 40 - "SurfacePicker"
Cohesion: 0.08
Nodes (24): AnnotateMode, AnnotationSettings, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a… (+16 more)

### Community 41 - "Camera"
Cohesion: 0.08
Nodes (18): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target). (+10 more)

### Community 42 - "test_armature.py"
Cohesion: 0.11
Nodes (38): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other., The femoral head is in from the ASIS, below it and behind it, by shares of the…, A wire in two halves is not an armature anybody could bend. (+30 more)

### Community 43 - "RenderSettings"
Cohesion: 0.07
Nodes (25): The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, ExportLook (+17 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.13
Nodes (26): _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry(), _primitives(), ndarray (+18 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.11
Nodes (12): QDialog, QProgressDialog, even(), ExportVideoDialog, Path, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+4 more)

### Community 46 - "VideoSettings"
Cohesion: 0.10
Nodes (18): open_writer(), How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., Start an encoder for ``settings``, or say why there cannot be one., VideoSettings (+10 more)

### Community 47 - "landmarks.py"
Cohesion: 0.12
Nodes (22): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _humanoid_landmarks(), _kept_laying(), _mid() (+14 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "MeshBuffers"
Cohesion: 0.11
Nodes (8): MeshBuffers, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are…, Whichever geometry is standing for the model this frame., Sum a see-through model into the ghost buffers, to be resolved after. Blending…, Vertex/index buffers for one mesh, bound through a single VAO., Forget the contents without releasing the buffer objects.

### Community 50 - "mesh_renderer.py"
Cohesion: 0.04
Nodes (68): Coefficients, PlaneSet, Reading the planes of a form out of the model's own normals. The grid quantiser…, One level of a fit: the planes the shader is to quantise against. A plane is a…, How much surface each vertex stands for: a third of each triangle on it.…, What each block of the design matrix counts for, against the normals. A fit…, Whether anything but the normals is being read at all., vertex_weights() (+60 more)

### Community 51 - "Texture2D"
Cohesion: 0.10
Nodes (8): Fill the shader's table with a level, if it is not already in it., Replace the annotation geometry; pass an empty list to hide it., DataTexture, ndarray, An RGBA8 2D texture with clamped edges and mipmapped minification., A small RGBA32F table the shader reads exact values out of. Not a picture:…, Store an ``(h, w, 4)`` float array, reallocating only when resized., Texture2D

### Community 52 - "PlacedLandmark"
Cohesion: 0.05
Nodes (34): BoneRef, PlacedLandmark, Point3, A graph of named points under the form, and the wire it stands for. An armature…, One anatomical point the artist put on the model during a guided run., The landmark list with one point moved, and no longer a guess. A landmark the…, The landmark list with these points taken back off the model. More than one at…, Point3 (+26 more)

### Community 53 - "test_plane_solids.py"
Cohesion: 0.06
Nodes (37): block(), coarse_lattice(), fixture, MonkeyPatch, Blocking a form in out of its planes, as stone is cut and as clay is built.…, A closed box with hard edges, each face cut into a grid of triangles., It is cut out of a block rather than built up on anything, so handing it a wire…, How far each point sits from the middle of its neighbours, as a share of the… (+29 more)

### Community 54 - "OrientationSettings"
Cohesion: 0.16
Nodes (17): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it., test_an_identity_turn_reuses_the_mesh() (+9 more)

### Community 55 - "PlaneSettings"
Cohesion: 0.04
Nodes (48): QThread, Film, film_key(), What a film depends on. Everything that changes the shape of any stage, and…, A whole making, from the coarsest stage to the one the slider asks for. Held by…, PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor…, How much of a turn in the surface one plane covers, in degrees. Linear in… (+40 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (11): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+3 more)

### Community 57 - "FormsPanel"
Cohesion: 0.10
Nodes (9): FormsPanel, Arms the forms tool, runs the guided presets and lists what they built., Begin a run against a fresh form: a preset's walk, or a freeform's., Ready the landmark the next click lays down, from the name and side boxes., After a landmark goes down: a fresh numbered name, the same side., Refit the focused freeform's clay; for a new one, remember the choice., Record an edit the viewport's tool worked out. A freeform's placed landmark is…, The multiplier the position boxes are read and written through. (+1 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.08
Nodes (20): PlanesPanel, QListWidgetItem, Lay one length of wire earlier or later, as one undoable step., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Show what this way of working needs, and put the rest away. A setting that does… (+12 more)

### Community 59 - "Landmark"
Cohesion: 0.07
Nodes (27): One convex piece of a form: its hull vertices and outward-wound faces., The longest side of the box the solid sits in., Whether a point lies inside, or within ``slack`` of the surface., A flat-shaded mesh, every triangle with its own three corners. Corners are not…, Solid, build_freeform(), _centre(), FormFill (+19 more)

### Community 60 - "ArmatureSettings"
Cohesion: 0.06
Nodes (51): ArmatureSettings, How the armature is drawn, and how new nodes are placed., The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now., How many landmarks are placed, out of how many will be asked for., Pass over the landmark being asked for; the figure loses what it fed. (+43 more)

### Community 61 - "SliderSpin"
Cohesion: 0.07
Nodes (19): QFormLayout, QFrame, collapsible_group(), CollapsibleGroup, ColorButton, _panel_form(), PointEdit, QPushButton (+11 more)

### Community 62 - ".update_enabled"
Cohesion: 0.17
Nodes (6): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., The armature the selected row stands for, when the row is not a node., Highlight the row for a node picked in the view., Highlight the row for a landmark picked in the view.

### Community 63 - "form_shapes.py"
Cohesion: 0.09
Nodes (42): _across(), blend_rings(), build_head(), build_pelvis(), fit_plane(), _head_frame(), _HeadFrame, _lagrange() (+34 more)

### Community 64 - "FormSettings"
Cohesion: 0.11
Nodes (17): FormSettings, How the forms are drawn, and how their landmarks are placed., Every landmark the walk will ask for under these choices. With mirroring on,…, The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now. For a freeform, the one…, How many landmarks are placed, out of how many will be asked for. A freeform…, ``(stage index, placed in it, asked for in it)`` for the current landmark.…, Pass over the landmark being asked for; the form loses what it fed. (+9 more)

### Community 65 - "overlay.py"
Cohesion: 0.07
Nodes (22): Annotations drawn as widened geometry, Measurements drawn in screen space with QPainter, MeasurementSettings, Named point-to-point measurements and their presentation options., How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., Which of the things drawn over the model belong in the frames., MeasureTool (+14 more)

### Community 66 - "Mesh"
Cohesion: 0.09
Nodes (20): auto_smooth(), Mesh, Return a copy whose bounding-box centre sits at the origin., A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, An indexed triangle mesh with per-vertex positions and normals. The viewer…, A stage as it is to be drawn, with its normals read at ``smooth``. Kept out of…, shaded(), How finely the model has to be sampled for the lattice it will be read on. (+12 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.08
Nodes (51): build_form(), built_count(), form_landmark_title(), form_mesh(), form_spec(), landmark_signature(), median_plane_ready(), mirror_form_landmarks() (+43 more)

### Community 68 - "History"
Cohesion: 0.13
Nodes (7): Camera motion is deliberately not undoable, Command, History, One reversible change, named for the undo menu., A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive…, test_undo_and_redo_on_an_empty_stack_are_safe()

### Community 69 - "compute_vertex_normals"
Cohesion: 0.11
Nodes (30): compute_vertex_normals(), Area-weighted smooth vertex normals for an indexed triangle soup., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic() (+22 more)

### Community 70 - "AnnotatePanel"
Cohesion: 0.19
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 71 - "plane_regions"
Cohesion: 0.08
Nodes (46): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), dumbbell(), flatness(), parametrize, The invariant an artist actually sees, on the finished stand-in: clay is added… (+38 more)

### Community 72 - "Release"
Cohesion: 0.18
Nodes (12): The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, is_skipped(), QWidget, Background release check and the notice it puts in front of the artist. The…, Whether the artist already dismissed this exact version., Offer the release page, with the option never to be asked again. (+4 more)

### Community 73 - "record"
Cohesion: 0.12
Nodes (22): Work the form stage by stage, handing each one back as it is finished. A…, record(), block_labels(), block_splits(), blocks(), carve(), _corner_facings(), _cuts() (+14 more)

### Community 74 - "convex.py"
Cohesion: 0.12
Nodes (23): convex_hull(), DegenerateHullError, flat_mesh(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, The outward unit normal at each vertex: the area-weighted mean of its faces'. A… (+15 more)

### Community 75 - "._build"
Cohesion: 0.33
Nodes (4): QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 76 - "application.py"
Cohesion: 0.05
Nodes (54): ArgumentParser, Color, Namespace, QApplication, QIcon, QPixmap, QSplashScreen, Charcoal matcap (+46 more)

### Community 77 - "test_forms.py"
Cohesion: 0.10
Nodes (32): merged(), The hull of the points with its faces bowed out; see :func:`rounded_hull`., Several flat meshes as one, or ``None`` when there is nothing to draw., build_ribcage(), The egg of the ribcage, with the arch chipped out of the front of it. Three…, _closed(), _inside(), _left_only() (+24 more)

### Community 78 - "._selected_landmark"
Cohesion: 0.12
Nodes (7): Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors., Show the landmark group only once there are landmarks to show., The landmark the highlighted row stands for, if the row is one., Which armature the landmark list is pointing into, row or heading., Follow the highlighted landmark, and say which one it is in the view.

### Community 79 - "ViewerState"
Cohesion: 0.12
Nodes (11): QObject, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Take the display unit from the file when the format declares one. Only glTF…, Everything the viewer displays, plus change notifications., ViewerState, The document being drawn., test_forms_turn_with_the_model() (+3 more)

### Community 80 - "session.py"
Cohesion: 0.24
Nodes (9): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Persisted viewer state: camera, shading, measurements and bookmarks. (+1 more)

### Community 81 - "ArmatureNode"
Cohesion: 0.12
Nodes (19): ArmatureNode, One joint of the wire: where it is, and how thick the form is there., _chain(), A straight run of nodes one unit apart along +X., Nothing stands between one neighbour, so there is nothing to bridge., test_a_bone_at_the_end_of_the_list_cannot_be_moved_off_it(), test_a_bone_is_never_laid_twice_between_the_same_pair(), test_a_bone_left_dangling_is_not_one_the_clay_can_be_laid_on() (+11 more)

### Community 82 - "core/__init__.py"
Cohesion: 0.11
Nodes (22): Shift-snapped orbiting (1.1.0), Qt-free geometry, camera and document model for the reference viewer., Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings (+14 more)

### Community 83 - "._build"
Cohesion: 0.27
Nodes (6): QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 84 - "test_forms_panel.py"
Cohesion: 0.13
Nodes (25): _click(), _pending(), _pick(), _place_all(), The Forms panel: the guided run it drives, and the document it writes. The…, A form row hands the whole form to update_enabled, whose landmark list must be…, Type a name for the next landmark and, if given, pick its side., What the viewport does when a freeform run gets a click. (+17 more)

### Community 85 - "TriangleIndex"
Cohesion: 0.14
Nodes (14): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., Build the index from expanded triangle corners, shape ``(T, 3, 3)``. (+6 more)

### Community 86 - "MeshLoadError"
Cohesion: 0.16
Nodes (17): STL corner welding, MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., _ascii_corners(), _binary_corners(), load_stl(), ndarray (+9 more)

### Community 87 - "._picker"
Cohesion: 0.13
Nodes (8): Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Apply the drag live, so the clay re-forms under the cursor., Track the form landmark under the cursor; True when it changed., Rub out the stroke points under the eraser, live.

### Community 88 - "ArmaturePanel"
Cohesion: 0.13
Nodes (7): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Add an empty armature and select it., Begin a preset run against a fresh armature., Take back the landmark before this one and ask for it again., Record an edit the viewport's tool worked out., The multiplier the position boxes are read and written through.

### Community 90 - "wakelock.py"
Cohesion: 0.22
Nodes (7): _Backend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The backend for this machine, or a do-nothing one if it cannot be had., A way of asking one platform to stay awake., Ask for sleep to be held off., Withdraw the request.

### Community 91 - "._delete_selected"
Cohesion: 0.20
Nodes (5): Record an edited landmark list, mirrored where the mirror is on., Remove the selected landmark, or the whole form when its row is picked., The form the selected row stands for, when the row is a form., The landmark the highlighted row stands for, if the row is one., Follow the highlighted landmark, and say which one it is in the view.

### Community 92 - ".mousePressEvent"
Cohesion: 0.15
Nodes (6): ndarray, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on., Take hold of a form's landmark, to move it or just to say which one it is., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…

### Community 93 - "Side"
Cohesion: 0.14
Nodes (17): freeform_landmark(), landmark_key(), paired_landmarks(), The side a landmark key ends in., The key of the landmark across the midline from this one; empty on the midline., A key for a freshly named landmark, and the name it will go by. The key is the…, A landmark the artist has just named, keyed so it does not collide., A freeform's landmarks with each side's twin worked in. A point placed on the… (+9 more)

### Community 94 - "._selected"
Cohesion: 0.14
Nodes (7): Run a row's edit once Qt has finished delivering the current signal. Committing…, Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., Run a bone between the row selected now and the node held before it., Join two nodes of one armature, if they are two and they are one armature., The node the selected row stands for, if the row is a node at all., Follow the highlighted row, without rebuilding the list underneath it. Going…

### Community 95 - ".update_enabled"
Cohesion: 0.12
Nodes (7): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Show a stage of the focused form. A view choice, so not an undo step., Take off the panel whatever does not apply right now., Size the stage slider to the focused form, and hide it for a one-stage form., The form the stage slider speaks for: the one being guided, else the one picked., Highlight the row for a landmark picked in the view.

### Community 96 - "clay_lumps"
Cohesion: 0.15
Nodes (18): _box_facings(), clay_lumps(), fit_piece(), _frame(), grow_piece(), join_pieces(), piece_bounds(), Which three ways a lump of material runs. Columns, thinnest first. Thinnest… (+10 more)

### Community 97 - "test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else"
Cohesion: 0.33
Nodes (5): lattice_fineness(), How much finer than usual a detail setting asks the lattice to be. One at the…, How much finer than usual the geometry's lattice is worked on., The slider's own end already asks for every plane a fit will give, so what a…, test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else()

### Community 98 - "_Encoder"
Cohesion: 0.25
Nodes (5): Queue, _Encoder, QObject, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 99 - "picking.py"
Cohesion: 0.09
Nodes (32): Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``. (+24 more)

### Community 100 - ".refresh_list"
Cohesion: 0.20
Nodes (6): QTreeWidgetItem, The landmarks in the recipe's own order, stage by stage., Rebuild the tree from the store, keeping the landmark being edited shown. Not…, Commit a renamed or re-checked form, or a renamed landmark, if anything changed., Give a freeform's own landmark the name typed into its row., Run a row's edit once Qt has finished delivering the current signal. Committing…

### Community 101 - "._upload_sculpt"
Cohesion: 0.33
Nodes (3): Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on.

### Community 102 - "Path"
Cohesion: 0.29
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 103 - "CHANGELOG.md"
Cohesion: 0.25
Nodes (8): Cross-section tool (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL and glTF import (1.1.0), Units are adopted, never guessed

### Community 104 - "SetAttributes"
Cohesion: 0.14
Nodes (8): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Record the finished gesture: a move, a resize, or a plain click. A press that…, Record the finished drag as one step, or read a press as a selection., Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…, Record the finished drag as one step, or read a press as a selection., Record the finished drag as a single undo step.

### Community 105 - "Projection"
Cohesion: 0.33
Nodes (4): Projection, Enum, str, Projection used by :class:`Camera`.

### Community 106 - "_ScreenSaverBackend"
Cohesion: 0.22
Nodes (4): The freedesktop screensaver service, which hands back a cookie., Hold sleep off, or stop holding it, whichever is not already true., Drop the request, if one is out. Safe to call more than once., _ScreenSaverBackend

### Community 107 - "._place_armature_node"
Cohesion: 0.22
Nodes (4): The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 108 - "test_mesh_io.py"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

### Community 109 - "BoneLabels"
Cohesion: 0.24
Nodes (6): BoneLabels, Buried, Enum, str, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…

### Community 110 - "test_session.py"
Cohesion: 0.12
Nodes (15): Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., A step of the slider is worth a fixed share more planes, not a fixed number of…, The ceiling went from 64 planes to 256 without moving the slider under anyone:…, The panel edits the settings; the fit has to be told what they are., Both modes answer in degrees of turn, so the panel can just ask., Version 1 files predate the annotation layer and the endpoint lock., test_a_session_from_before_annotations_still_loads() (+7 more)

### Community 111 - "plane_volume.py"
Cohesion: 0.18
Nodes (15): _axes(), encloses(), lattice(), lay_bed(), nearest_surface(), _passes(), Blocking a form in out of its own planes, from the outside or from a core. A…, Read the model onto a lattice, ready for solids to be laid on it. (+7 more)

### Community 112 - "coarse_lattice"
Cohesion: 0.33
Nodes (6): app(), coarse_lattice(), fixture, MonkeyPatch, One Qt application for the whole run; offscreen, so CI needs no display.…, Read every model on a small lattice, so the suite stays quick.

### Community 113 - "stone_field"
Cohesion: 0.14
Nodes (14): Bed, block_bounds(), block_field(), coarse_bounds(), point_support(), The lattice a form is worked on, and the model read onto it. Everything here…, The union of the blocks a labelling cuts the model into, and its facings. Stone…, One row of coordinates per axis over ``box``, shaped so they broadcast. (+6 more)

### Community 114 - "ArmatureStore"
Cohesion: 0.18
Nodes (4): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 115 - "Wires"
Cohesion: 0.15
Nodes (10): clay_pieces(), kept_off(), An armature, as the clay reads it: where each length of wire runs. The order…, How many lumps the wire itself asks for., What a cache has to compare to know the wire has not moved., Which points lie in the sleeve a length of wire declares round itself. The wire…, Which material lies under a length of wire that is to take no clay. Turning a…, Lumps of clay pressed into the model, the biggest masses first. The seed of the… (+2 more)

### Community 116 - "ndarray"
Cohesion: 0.18
Nodes (6): _gathered(), ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Which group each of ``total`` things lands in, given pairs that agree. Hooking…, ValueError

### Community 117 - "_WindowsBackend"
Cohesion: 0.25
Nodes (5): ``SetThreadExecutionState``: a flag on this thread, not a handle. The flags…, _WindowsBackend, skipif, The flag the viewer sets is the one Windows reports back afterwards., test_windows_really_sets_the_execution_state()

### Community 118 - "ShadingMode"
Cohesion: 0.25
Nodes (3): Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode

### Community 119 - "ReplaceItems"
Cohesion: 0.22
Nodes (4): Any, Swap the whole contents of a document list. Used for bulk edits -- clearing the…, ReplaceItems, test_replace_items_covers_bulk_edits()

### Community 120 - "_shifts"
Cohesion: 0.20
Nodes (10): _balloon(), close_gaps(), outside_points(), Fill the slots the lumps leave between them, without taking clay away. The…, Grow or shrink a solid by ``reach`` cells, one axis at a time. A separable…, Where the model stops: the corners just outside ``room``. ``(n, 3)``. Only the…, The pair of slices that read a lattice ``span`` cells over along ``axis``., Hand a block's number to the corners just outside it. The blocks are cut on a… (+2 more)

### Community 121 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 122 - "_MacBackend"
Cohesion: 0.33
Nodes (3): c_void_p, _MacBackend, An IOKit power assertion, held by id until it is released.

### Community 123 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 124 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 125 - "Session"
Cohesion: 0.31
Nodes (7): Path, A snapshot of everything worth keeping between runs., Session, test_an_armature_survives_a_session_round_trip(), test_an_older_session_loads_without_forms(), test_forms_survive_a_session_round_trip(), test_session_round_trip()

### Community 126 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 127 - "sidecar_path"
Cohesion: 0.25
Nodes (5): Session file that sits beside a model, e.g. ``bust.refview.json``., sidecar_path(), Path, Set the active matcap, or fall back to the built-in one., test_sidecar_path_sits_next_to_the_model()

### Community 128 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 129 - "RemoveItem"
Cohesion: 0.29
Nodes (4): Delete the item at ``index``, putting it back in place on undo., RemoveItem, Deletion goes through the undo stack, so the store only tracks position., test_deleting_a_bookmark_moves_the_cycling_position()

### Community 130 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 131 - "orientation.py"
Cohesion: 0.33
Nodes (5): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis

### Community 132 - ".stage_images"
Cohesion: 0.17
Nodes (8): QOpenGLFramebufferObject, QImage, The nodes the model is standing in front of, worked out at most once. A node is…, One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A…, An offscreen target the frames are drawn into, made once per export.…, Draw the scene into ``surface`` and read it back as an image., Lay the overlay -- and the caption, if it was asked for -- on a frame. Painted…

### Community 134 - ".refresh_list"
Cohesion: 0.29
Nodes (4): QTreeWidgetItem, Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing., Commit a renamed or re-checked row, if anything actually changed.

### Community 136 - "._back_point"
Cohesion: 0.33
Nodes (3): Take back the landmark before this one and ask for it again., Take back the last landmark a freeform was given, guess and all., The mirrored landmarks reflected from ``key``, which it anchors.

### Community 137 - "_NameOnlyDelegate"
Cohesion: 0.33
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 138 - "_wire_frame"
Cohesion: 0.50
Nodes (4): _perpendicular(), Two unit directions across ``along``, neither of them near it., Which three ways a lump laid along a wire runs. Columns, thinnest first. The…, _wire_frame()

### Community 139 - "plane_count"
Cohesion: 0.50
Nodes (4): _along(), plane_count(), Where a detail setting sits on its slider, 0 to 1., How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`.

### Community 141 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `PlaneAxes`, `plane_axes`, `main_window.py`, `ball`, `_wires`, `mesh.py`, `.apply_session`, `FormStore`, `SectionSettings`, `viewport.py`, `test_plane_clusters.py`, `ndarray`, `RenderSettings`, `gltf_loader.py`, `MeshBuffers`, `mesh_renderer.py`, `Texture2D`, `test_plane_solids.py`, `OrientationSettings`, `PlaneSettings`, `Landmark`, `FormSettings`, `PrimaryForm`, `compute_vertex_normals`, `plane_regions`, `record`, `convex.py`, `test_forms.py`, `ViewerState`, `core/__init__.py`, `TriangleIndex`, `MeshLoadError`, `picking.py`, `test_mesh_io.py`, `plane_volume.py`, `stone_field`, `Wires`, `ndarray`?**
  _High betweenness centrality (0.166) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `FormTool`, `.stage_images`, `main_window.py`, `MainWindow`, `._place_form_landmark`, `ViewportOverlay`, `NavigationController`, `viewport.py`, `ArmatureTool`, `film_export.py`, `SurfacePicker`, `RenderSettings`, `ExportVideoDialog`, `PlaneSettings`, `FilmExport`, `overlay.py`, `PrimaryForm`, `ViewerState`, `._picker`, `.mousePressEvent`, `_Encoder`, `._upload_sculpt`, `SetAttributes`, `._place_armature_node`?**
  _High betweenness centrality (0.074) - this node is a cross-community bridge._
- **Why does `Armature` connect `Armature` to `ArmatureTool`, `overlay.py`, `ndarray`, `main_window.py`, `test_armature.py`, `._selected_landmark`, `session.py`, `ArmatureNode`, `core/__init__.py`, `ArmatureStore`, `PlacedLandmark`, `Session`, `ViewportOverlay`, `test_planes_panel.py`, `ArmaturePanel`, `ArmatureSettings`, `viewport.py`, `.update_enabled`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PrimaryForm` (e.g. with `PlacedLandmark` and `DegenerateHullError`) actually correct?**
  _`PrimaryForm` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._