# Graph Report - reference-viewer  (2026-09-13)

## Corpus Check
- 105 files · ~390,752 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3243 nodes · 7433 edges · 131 communities (126 shown, 5 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 336 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5f349262`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FormTool
- Landmark
- main_window.py
- Viewport
- plane_axes
- viewport.py
- MainWindow
- Stroke
- GifWriter
- MeasurementStore
- RenderSettings
- PlaneSettings
- camera.py
- _wires
- Armature
- README.md
- ViewerState
- FormStore
- mesh_renderer.py
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
- FormSettings
- Writer
- ShadingPanel
- Panel
- test_camera.py
- test_plane_clusters.py
- WakeLock
- plane_volume.py
- History
- MeshLoadError
- VideoFormat
- orientation.py
- Camera
- build_humanoid
- ExportLook
- compute_vertex_normals
- form_group
- VideoSettings
- landmarks.py
- Agent Graph-First Instructions
- SceneRenderer
- plane_clusters.py
- render/__init__.py
- PlacedLandmark
- Side
- Measurement
- Mesh
- FilmExport
- FormsPanel
- PlanesPanel
- ndarray
- ArmatureTool
- SliderSpin
- .update_enabled
- form_shapes.py
- MatcapPanel
- MeasureTool
- test_navigation.py
- PrimaryForm
- Command
- obj_loader.py
- AnnotatePanel
- test_plane_solids.py
- load_matcap_pixels
- .split_point
- Solid
- forms_panel.py
- application.py
- test_forms.py
- ._selected_landmark
- TriangleIndex
- test_session.py
- test_armature.py
- core/__init__.py
- ._build
- test_forms_panel.py
- test_mesh_io.py
- shaders.py
- .mouseMoveEvent
- ArmaturePanel
- .pan
- film_export.py
- ._delete_selected
- .mousePressEvent
- settings.py
- ._selected
- .update_enabled
- RemoveItem
- plane_count
- _Encoder
- mesh.py
- .refresh_list
- ._upload_sculpt
- test_spatial.py
- CHANGELOG.md
- SetAttributes
- Projection
- .point
- ._picker
- ._on_bone_toggled
- BoneLabels
- collapsible_group
- ._arm
- ball
- FakeViewport
- .film_changed
- coarse_lattice
- panel
- ReplaceItems
- ShadingMode
- AddItem
- ._focused_form
- release.yml
- ColorButton
- fit_planes
- _NameOnlyDelegate
- .with_landmark_at
- app
- no_ffmpeg
- ndarray
- ._buried_nodes
- .refresh_list

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 142 edges
2. `Viewport` - 101 edges
3. `Camera` - 75 edges
4. `Armature` - 73 edges
5. `PlaneSettings` - 67 edges
6. `PrimaryForm` - 61 edges
7. `ArmaturePanel` - 60 edges
8. `ViewerState` - 59 edges
9. `PlacedLandmark` - 57 edges
10. `ArmatureTool` - 52 edges

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

## Communities (131 total, 5 thin omitted)

### Community 0 - "FormTool"
Cohesion: 0.10
Nodes (12): FormLandmarkRef, FormRun, FormTool, ndarray, Where a click at ``(x, y)`` would put a landmark: on the surface, or nowhere., Where a grabbed landmark should move to. A drag that wanders off the model…, The nearest grabbable landmark under the cursor, if any. Only the ones on…, A guided primary form part-way through. (+4 more)

### Community 1 - "Landmark"
Cohesion: 0.12
Nodes (12): _humanoid_landmarks(), Landmark, _node_name(), The landmarks worth asking for under these choices. With mirroring on the…, The midline first, then each pair left before right., What to call a landmark in a menu or an undo step. The preset's own words when…, One point of anatomy the artist is asked to find., The name with its side, for a prompt. (+4 more)

### Community 2 - "main_window.py"
Cohesion: 0.09
Nodes (37): check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed). (+29 more)

### Community 3 - "Viewport"
Cohesion: 0.07
Nodes (15): QOpenGLWidget, The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, Slide the view so a point sits at the centre, keeping the angle., A form changed: work its clay out again and redraw., Slide the view so a measurement sits at the centre, keeping the angle., Regenerate the pedestal and the cut contour when their settings move. Both are…, End any film being recorded, and wait for its thread to really stop. For…, The document being drawn. (+7 more)

### Community 4 - "plane_axes"
Cohesion: 0.08
Nodes (37): plane_axes(), ndarray, A level with no place in it: nearest direction wins, as before., How much surface each vertex stands for: a third of each triangle on it.…, The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to., Split the mesh's normals into planes, keeping every count on the way., _split() (+29 more)

### Community 5 - "viewport.py"
Cohesion: 0.06
Nodes (35): AnnotateMode, AnnotationSettings, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a… (+27 more)

### Community 6 - "MainWindow"
Cohesion: 0.06
Nodes (15): QAction, QMainWindow, MainWindow, Path, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits. (+7 more)

### Community 7 - "Stroke"
Cohesion: 0.06
Nodes (37): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+29 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "MeasurementStore"
Cohesion: 0.16
Nodes (5): MeasurementStore, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., An ordered, named collection of measurements. Deliberately plain: the Qt layer…, test_store_auto_names_new_measurements()

### Community 10 - "RenderSettings"
Cohesion: 0.09
Nodes (22): Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, light_directions(), normal_matrix(), ndarray, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.… (+14 more)

### Community 11 - "PlaneSettings"
Cohesion: 0.04
Nodes (81): film_key(), planes_for(), The stages a form passes through on its way from a block to a figure. The…, What a film depends on. Everything that changes the shape of any stage, and…, How many solids each stage of a film is made of. Every count from the coarsest…, The detail setting that asks for ``solids``, or ``None`` if none does. The…, Work the form stage by stage, handing each one back as it is finished. A…, record() (+73 more)

### Community 12 - "camera.py"
Cohesion: 0.13
Nodes (23): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-…, Return ``v`` scaled to unit length, or ``fallback`` for a zero vector. (+15 more)

### Community 13 - "_wires"
Cohesion: 0.13
Nodes (28): _bar(), _bed_for(), _holds(), A long ellipsoid: one closed form with an obvious axis to lie along., A model read onto a lattice, ready for lumps to be laid on it., Whether a fitted solid has a point inside it., An armature for the volume, with ``off`` naming the rows taking no clay., The claim the whole armature mode rests on. A lump that merely landed near its… (+20 more)

### Community 14 - "Armature"
Cohesion: 0.05
Nodes (32): Armature, ArmatureStore, Bone, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves., A plausible thickness for a node placed by hand. (+24 more)

### Community 15 - "README.md"
Cohesion: 0.15
Nodes (16): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command (+8 more)

### Community 16 - "ViewerState"
Cohesion: 0.09
Nodes (17): Session file that sits beside a model, e.g. ``bust.refview.json``., sidecar_path(), ndarray, Path, QObject, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current… (+9 more)

### Community 17 - "FormStore"
Cohesion: 0.15
Nodes (5): FormStore, An ordered, named collection of primary forms, like the other stores., The live list; the undo commands operate on it directly., A name for a new form of this preset, numbered past any it already has., test_a_form_store_names_forms_past_the_ones_it_has()

### Community 18 - "mesh_renderer.py"
Cohesion: 0.07
Nodes (21): AccumTarget, bind_default(), ColorTarget, current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality and ghost passes. Four of…, A single-channel colour framebuffer, used for the occlusion buffers. (+13 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): CameraPanel, QListWidgetItem, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "ViewportOverlay"
Cohesion: 0.12
Nodes (24): QColor, QPainter, QPointF, project_visible(), Handle, QFont, Draws measurements, tool previews, the orientation gizmo and the readout., Burn a line into the bottom of a frame, for an exported clip. Which stage of… (+16 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.08
Nodes (21): _names(), The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as…, Or there would be no way to turn one back on., A limb is four bones, and deciding not to block the arms in is one decision.…, It is rebuilt on every change, and ticking one row of a selected limb would be… (+13 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.14
Nodes (8): MeasurePanel, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn.

### Community 25 - "BookmarkStore"
Cohesion: 0.11
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around. (+1 more)

### Community 26 - "NavigationController"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "SectionSettings"
Cohesion: 0.11
Nodes (22): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, Unit axis, or ``None`` for a custom direction., A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn. (+14 more)

### Community 28 - "SectionPanel"
Cohesion: 0.11
Nodes (15): Cross-section tool (1.1.0), Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Which side of the plane survives the cut., SectionAxis, SectionMode (+7 more)

### Community 29 - "FormSettings"
Cohesion: 0.11
Nodes (18): FormSettings, How the forms are drawn, and how their landmarks are placed., Every landmark the walk will ask for under these choices. With mirroring on,…, The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now., How many landmarks are placed, out of how many will be asked for., ``(stage index, placed in it, asked for in it)`` for the current landmark.…, Pass over the landmark being asked for; the form loses what it fed. (+10 more)

### Community 30 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 31 - "ShadingPanel"
Cohesion: 0.21
Nodes (7): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel

### Community 32 - "Panel"
Cohesion: 0.15
Nodes (8): Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block., _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (58): angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What… (+50 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (32): c_void_p, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., Holds sleep off while the window that owns it is the one in front. The class… (+24 more)

### Community 36 - "plane_volume.py"
Cohesion: 0.04
Nodes (108): _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field(), block_labels(), block_splits() (+100 more)

### Community 37 - "History"
Cohesion: 0.17
Nodes (14): History, A bounded undo/redo stack., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch(), test_commands_carry_their_channel_and_name() (+6 more)

### Community 38 - "MeshLoadError"
Cohesion: 0.18
Nodes (16): MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., _ascii_corners(), _binary_corners(), load_stl(), ndarray, Path (+8 more)

### Community 39 - "VideoFormat"
Cohesion: 0.09
Nodes (13): Enum, str, Quality, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31., WebP's quality, 0 to 100. (+5 more)

### Community 40 - "orientation.py"
Cohesion: 0.17
Nodes (8): Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., UpAxis, ModelPanel, What was imported and which way up it should stand., Turns the model the right way up and reports what came out of the file.

### Community 41 - "Camera"
Cohesion: 0.10
Nodes (14): Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole., Scale the view by ``factor`` about ``pivot`` (``< 1`` moves closer). Scaling… (+6 more)

### Community 42 - "build_humanoid"
Cohesion: 0.12
Nodes (32): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _figure(), ndarray, The femoral head is in from the ASIS, below it and behind it, by shares of the…, A wire in two halves is not an armature anybody could bend., Place every landmark the run asks for; returns how many were asked., Every required humanoid landmark, both sides, scaled about the origin. (+24 more)

### Community 43 - "ExportLook"
Cohesion: 0.09
Nodes (17): QOpenGLFramebufferObject, The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, ExportLook, What the frames are to look like, as against what they are of. Laid over the…, Which of the things drawn over the model belong in the frames. (+9 more)

### Community 44 - "compute_vertex_normals"
Cohesion: 0.12
Nodes (28): _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry(), _primitives(), ndarray (+20 more)

### Community 45 - "form_group"
Cohesion: 0.10
Nodes (16): QDialog, QGroupBox, QProgressDialog, even(), ExportVideoDialog, Path, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+8 more)

### Community 46 - "VideoSettings"
Cohesion: 0.18
Nodes (7): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, TestTiming

### Community 47 - "landmarks.py"
Cohesion: 0.12
Nodes (25): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _kept_laying(), median_plane(), _mid() (+17 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "SceneRenderer"
Cohesion: 0.11
Nodes (12): _ghost_depth_range(), MeshBuffers, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are…, Whichever geometry is standing for the model this frame., Sum a see-through model into the ghost buffers, to be resolved after. Blending… (+4 more)

### Community 50 - "plane_clusters.py"
Cohesion: 0.08
Nodes (35): _compact(), _consensus(), _cut(), _first_planes(), _fit(), flatness(), _leaves(), neighbour_agreement() (+27 more)

### Community 51 - "render/__init__.py"
Cohesion: 0.08
Nodes (15): OpenGL rendering layer: shader programs, textures and the scene renderer., Fill the shader's table with a level, if it is not already in it., Replace the annotation geometry; pass an empty list to hide it., DataTexture, default_matcap_pixels(), MatcapLoadError, ndarray, RuntimeError (+7 more)

### Community 52 - "PlacedLandmark"
Cohesion: 0.08
Nodes (23): PlacedLandmark, Point3, A graph of named points under the form, and the wire it stands for. An armature…, One anatomical point the artist put on the model during a guided run., The landmark list with one point moved, and no longer a guess. A landmark the…, The landmark list with these points taken back off the model. More than one at…, mirror_landmarks(), Preset (+15 more)

### Community 53 - "Side"
Cohesion: 0.14
Nodes (10): FormPreset, FormStage, One step of a form's making, and the landmarks it asks for., A primary form: its stages, in order, and the rule that builds them., Every landmark, in the order the walk asks for them., Which stage a landmark belongs to, or the last for an unknown key., Enum, str (+2 more)

### Community 54 - "Measurement"
Cohesion: 0.09
Nodes (25): Measurement, ndarray, A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end., Name of the attribute a handle edits, for building an undo command., OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world. (+17 more)

### Community 55 - "Mesh"
Cohesion: 0.04
Nodes (43): QThread, Mesh, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, _empty(), PlaneAxes, PlaneSet, Reading the planes of a form out of the model's own normals. The grid quantiser… (+35 more)

### Community 56 - "FilmExport"
Cohesion: 0.08
Nodes (20): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+12 more)

### Community 57 - "FormsPanel"
Cohesion: 0.13
Nodes (6): FormsPanel, Take back the landmark before this one and ask for it again., Record an edit the viewport's tool worked out., The multiplier the position boxes are read and written through., Keep the ghost switch agreeing with the Shading panel's., Arms the forms tool, runs the guided presets and lists what they built.

### Community 58 - "PlanesPanel"
Cohesion: 0.15
Nodes (12): PlanesPanel, Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Show what this way of working needs, and put the rest away. A setting that does…, Breaks the form into planes, in the shading or in the geometry itself., The armature the clay is being built on, or ``None``. An index past the end of…, Re-read the armatures and what the chosen one is laying down. Called whenever…, The bones of the chosen armature, in the order the clay goes down. Every intact… (+4 more)

### Community 59 - "ndarray"
Cohesion: 0.18
Nodes (6): _gathered(), ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Which group each of ``total`` things lands in, given pairs that agree. Hooking…, ValueError

### Community 60 - "ArmatureTool"
Cohesion: 0.07
Nodes (32): LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, Handle, ndarray, Begin a preset run against an armature already in the store., How many landmarks are placed, out of how many will be asked for. (+24 more)

### Community 61 - "SliderSpin"
Cohesion: 0.10
Nodes (11): QFrame, CollapsibleGroup, PointEdit, QWidget, Re-scale the control, e.g. once a model's size is known., Grow the slider to take in a value from beyond its end., Three spin boxes for one point in space. Keyboard tracking is off, so a typed…, Match the arrows to the size of the thing being moved. (+3 more)

### Community 62 - ".update_enabled"
Cohesion: 0.17
Nodes (6): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., Follow the highlighted row, without rebuilding the list underneath it. Going…, Highlight the row for a node picked in the view., Highlight the row for a landmark picked in the view.

### Community 63 - "form_shapes.py"
Cohesion: 0.10
Nodes (37): _across(), blend_rings(), build_head(), build_pelvis(), fit_plane(), _head_frame(), _HeadFrame, _lagrange() (+29 more)

### Community 64 - "MatcapPanel"
Cohesion: 0.12
Nodes (13): QIcon, QPixmap, QScrollArea, lock_icon(), Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if…, _render(), MatcapPanel (+5 more)

### Community 65 - "MeasureTool"
Cohesion: 0.09
Nodes (16): MeasurementSettings, How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., MeasureTool, Handle, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any. (+8 more)

### Community 66 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.08
Nodes (41): build_form(), built_count(), _centre(), form_landmark_title(), form_mesh(), landmark_signature(), median_plane_ready(), mirror_form_landmarks() (+33 more)

### Community 68 - "Command"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 69 - "obj_loader.py"
Cohesion: 0.12
Nodes (28): _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic(), load_obj(), ObjLoadError (+20 more)

### Community 70 - "AnnotatePanel"
Cohesion: 0.24
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 71 - "test_plane_solids.py"
Cohesion: 0.04
Nodes (89): auto_smooth(), A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, Holds the working state between one turn of the sliders and the next.…, The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself. (+81 more)

### Community 72 - "load_matcap_pixels"
Cohesion: 0.18
Nodes (20): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+12 more)

### Community 73 - ".split_point"
Cohesion: 0.20
Nodes (9): BoneRef, _project(), The nearest bone under the cursor, for showing its length., Where on a bone a click at ``(x, y)`` landed. The share along the bone is read…, A world point in widget pixels, or ``None`` when it is behind the camera., How far along a screen-space segment the cursor's nearest point lies., Pixels from the cursor to the segment, or ``None`` if either end is behind., _segment_distance() (+1 more)

### Community 74 - "Solid"
Cohesion: 0.10
Nodes (21): convex_hull(), DegenerateHullError, flat_mesh(), _outward(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, One convex piece of a form: its hull vertices and outward-wound faces., Every face as a unit normal and an offset, ``normal @ x <= offset`` inside. (+13 more)

### Community 75 - "forms_panel.py"
Cohesion: 0.23
Nodes (5): QPushButton, QWidget, The primary forms: the guided presets that build them, their stages, and the…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 76 - "application.py"
Cohesion: 0.10
Nodes (29): ArgumentParser, Namespace, QApplication, QSplashScreen, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font() (+21 more)

### Community 77 - "test_forms.py"
Cohesion: 0.10
Nodes (30): merged(), Several flat meshes as one, or ``None`` when there is nothing to draw., build_ribcage(), The egg of the ribcage, with the arch chipped out of the front of it. Three…, _closed(), _inside(), _marks(), ndarray (+22 more)

### Community 78 - "._selected_landmark"
Cohesion: 0.12
Nodes (7): Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors., Show the landmark group only once there are landmarks to show., The landmark the highlighted row stands for, if the row is one., Which armature the landmark list is pointing into, row or heading., Follow the highlighted landmark, and say which one it is in the view.

### Community 79 - "TriangleIndex"
Cohesion: 0.15
Nodes (13): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., Build the index from expanded triangle corners, shape ``(T, 3, 3)``. (+5 more)

### Community 80 - "test_session.py"
Cohesion: 0.07
Nodes (31): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Path (+23 more)

### Community 81 - "test_armature.py"
Cohesion: 0.07
Nodes (49): ArmatureNode, One joint of the wire: where it is, and how thick the form is there., The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _chain(), _derived(), The armature graph, the humanoid landmarks and the joints they infer., A guess the artist corrects is theirs, and the mirror leaves it alone. (+41 more)

### Community 82 - "core/__init__.py"
Cohesion: 0.11
Nodes (24): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, Qt-free geometry, camera and document model for the reference viewer., Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal() (+16 more)

### Community 83 - "._build"
Cohesion: 0.27
Nodes (6): QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 84 - "test_forms_panel.py"
Cohesion: 0.21
Nodes (14): _pick(), _place_all(), The Forms panel: the guided run it drives, and the document it writes. The…, A form row hands the whole form to update_enabled, whose landmark list must be…, test_a_one_stage_form_hides_the_slider(), test_back_takes_a_landmark_off_through_the_history(), test_clear_all_ends_the_run_and_undoes_as_one_step(), test_deleting_a_landmark_takes_its_mirrored_guess_with_it() (+6 more)

### Community 85 - "test_mesh_io.py"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

### Community 86 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 87 - ".mouseMoveEvent"
Cohesion: 0.20
Nodes (4): Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Apply the drag live, so the clay re-forms under the cursor.

### Community 88 - "ArmaturePanel"
Cohesion: 0.14
Nodes (7): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Add an empty armature and select it., Begin a preset run against a fresh armature., Take back the landmark before this one and ask for it again., Record an edit the viewport's tool worked out., The multiplier the position boxes are read and written through.

### Community 90 - "film_export.py"
Cohesion: 0.09
Nodes (29): _encode_arguments(), _encoders(), ffmpeg_path(), _FFmpegWriter, _no_window(), open_writer(), Path, RuntimeError (+21 more)

### Community 91 - "._delete_selected"
Cohesion: 0.20
Nodes (5): Record an edited landmark list, mirrored where the mirror is on., Remove the selected landmark, or the whole form when its row is picked., The mirrored landmarks reflected from ``key``, which it anchors., The form the selected row stands for, when the row is a form., The landmark the highlighted row stands for, if the row is one.

### Community 92 - ".mousePressEvent"
Cohesion: 0.15
Nodes (6): ndarray, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on., Take hold of a form's landmark, to move it or just to say which one it is., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…

### Community 93 - "settings.py"
Cohesion: 0.06
Nodes (31): Coefficients, What each block of the design matrix counts for, against the normals. A fit…, Whether anything but the normals is being read at all., LightSettings, MatcapSettings, plane_span_deg(), PlaneMode, PlaneTarget (+23 more)

### Community 94 - "._selected"
Cohesion: 0.16
Nodes (6): Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., Run a bone between the row selected now and the node held before it., Join two nodes of one armature, if they are two and they are one armature., The node the selected row stands for, if the row is a node at all., The armature the selected row stands for, when the row is not a node.

### Community 95 - ".update_enabled"
Cohesion: 0.20
Nodes (5): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., Follow the highlighted landmark, and say which one it is in the view., Highlight the row for a landmark picked in the view.

### Community 96 - "RemoveItem"
Cohesion: 0.20
Nodes (5): Any, Delete the item at ``index``, putting it back in place on undo., RemoveItem, Deletion goes through the undo stack, so the store only tracks position., test_deleting_a_bookmark_moves_the_cycling_position()

### Community 97 - "plane_count"
Cohesion: 0.12
Nodes (12): _along(), lattice_fineness(), plane_count(), Where a detail setting sits on its slider, 0 to 1., How much finer than usual a detail setting asks the lattice to be. One at the…, How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., How much of a turn in the surface one plane covers, in degrees. Linear in…, How many planes a mode fitted to the model keeps. The climb from two planes to… (+4 more)

### Community 98 - "_Encoder"
Cohesion: 0.22
Nodes (6): Queue, _Encoder, QObject, QWidget, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 99 - "mesh.py"
Cohesion: 0.13
Nodes (23): Triangle-mesh containers shared by the loader, the renderer and picking., Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays. (+15 more)

### Community 100 - ".refresh_list"
Cohesion: 0.20
Nodes (5): QTreeWidgetItem, The landmarks in the preset's own order, stage by stage., Rebuild the tree from the store, keeping the landmark being edited shown. Not…, Commit a renamed or re-checked form, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…

### Community 101 - "._upload_sculpt"
Cohesion: 0.22
Nodes (4): The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on.

### Community 102 - "test_spatial.py"
Cohesion: 0.29
Nodes (9): _grid(), The picking accelerator: it must be fast without changing any answer., A bumpy height field, so rays hit different triangles at different depths., The pruned candidate set must never miss the true intersection., test_a_ray_that_misses_the_model_is_pruned_away(), test_an_empty_index_returns_no_candidates(), test_every_triangle_lands_in_exactly_one_leaf(), test_the_index_finds_the_triangle_a_ray_actually_hits() (+1 more)

### Community 103 - "CHANGELOG.md"
Cohesion: 0.25
Nodes (8): Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, STL and glTF import (1.1.0), Units are adopted, never guessed

### Community 104 - "SetAttributes"
Cohesion: 0.11
Nodes (11): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Record the finished gesture: a move, a resize, or a plain click. A press that…, Record the finished drag as one step, or read a press as a selection., Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…, Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed. (+3 more)

### Community 105 - "Projection"
Cohesion: 0.25
Nodes (5): Projection, Enum, str, Projection used by :class:`Camera`., test_serialisation_round_trip()

### Community 106 - ".point"
Cohesion: 0.22
Nodes (5): ndarray, Closest surface intersection under the cursor, or ``None``., Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-…, Screen-to-world scale at a given depth along the view direction.

### Community 107 - "._picker"
Cohesion: 0.14
Nodes (6): Which form an edit lands in, counting a guided run as binding., Record the landmark a guided form is asking for., Rub out the stroke points under the eraser, live., Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 108 - "._on_bone_toggled"
Cohesion: 0.29
Nodes (4): QListWidgetItem, Catch the selection a click on a checkbox is about to collapse. Qt selects a…, Which bones of the armature the picked-out rows stand for., Take lengths of wire out of the clay, or put them back. A tick on a row that…

### Community 109 - "BoneLabels"
Cohesion: 0.24
Nodes (6): BoneLabels, Buried, Enum, str, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…

### Community 110 - "collapsible_group"
Cohesion: 0.50
Nodes (5): QFormLayout, collapsible_group(), _panel_form(), The row layout every group in the side panels is built on., A folded-away group with a form layout, shaped like :func:`form_group`.

### Community 112 - "ball"
Cohesion: 0.11
Nodes (28): app(), coarse_lattice(), fixture, MonkeyPatch, Recording a film on a thread, without taking the process down with it. The rest…, Which is what the panel puts its controls to sleep by, so it has to be true…, Shutdown must not care whether the thread beat it to the exit. A recording that…, The guard that decides whether to scrub an existing film or record a new one.… (+20 more)

### Community 113 - "FakeViewport"
Cohesion: 0.28
Nodes (3): FakeViewport, QImage, A viewport that renders nothing, at whatever size it is asked for.

### Community 115 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 116 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 117 - "ReplaceItems"
Cohesion: 0.25
Nodes (4): The handful of undoable edits the whole application is built from.…, Swap the whole contents of a document list. Used for bulk edits -- clearing the…, ReplaceItems, test_replace_items_covers_bulk_edits()

### Community 118 - "ShadingMode"
Cohesion: 0.25
Nodes (3): Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode

### Community 119 - "AddItem"
Cohesion: 0.29
Nodes (3): AddItem, Append an item to a document list., Begin a preset run against a fresh form.

### Community 120 - "._focused_form"
Cohesion: 0.29
Nodes (3): Show a stage of the focused form. A view choice, so not an undo step., Size the stage slider to the focused form, and hide it for a one-stage form., The form the stage slider speaks for: the one being guided, else the one picked.

### Community 121 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 122 - "ColorButton"
Cohesion: 0.38
Nodes (3): ColorButton, QPushButton, A swatch button that opens a colour picker. Colours are exchanged as 0-1 RGB…

### Community 123 - "fit_planes"
Cohesion: 0.50
Nodes (3): fit_planes(), The planes of ``mesh`` under ``mode``; empty where the mode needs none., The model's own planes under ``mode``, fitted once and kept.

### Community 124 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 126 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 127 - "no_ffmpeg"
Cohesion: 0.67
Nodes (3): no_ffmpeg(), fixture, A machine with no video encoder on it, which is most of them.

### Community 130 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 134 - ".refresh_list"
Cohesion: 0.20
Nodes (5): QTreeWidgetItem, Run a row's edit once Qt has finished delivering the current signal. Committing…, Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing., Commit a renamed or re-checked row, if anything actually changed.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `plane_axes`, `viewport.py`, `PlaneSettings`, `_wires`, `README.md`, `ViewerState`, `FormStore`, `mesh_renderer.py`, `SectionSettings`, `SectionPanel`, `FormSettings`, `test_plane_clusters.py`, `plane_volume.py`, `MeshLoadError`, `ExportLook`, `compute_vertex_normals`, `form_group`, `SceneRenderer`, `plane_clusters.py`, `render/__init__.py`, `Side`, `Measurement`, `FilmExport`, `ndarray`, `PrimaryForm`, `obj_loader.py`, `test_plane_solids.py`, `Solid`, `test_forms.py`, `TriangleIndex`, `core/__init__.py`, `test_mesh_io.py`, `settings.py`, `mesh.py`, `test_spatial.py`, `ball`, `FakeViewport`, `fit_planes`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `FormTool`, `main_window.py`, `._buried_nodes`, `viewport.py`, `MainWindow`, `ViewerState`, `ViewportOverlay`, `NavigationController`, `ExportLook`, `form_group`, `Mesh`, `FilmExport`, `ArmatureTool`, `MeasureTool`, `PrimaryForm`, `.mouseMoveEvent`, `film_export.py`, `.mousePressEvent`, `_Encoder`, `._upload_sculpt`, `SetAttributes`, `._picker`, `._arm`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Why does `Armature` connect `Armature` to `Landmark`, `ndarray`, `viewport.py`, `test_plane_solids.py`, `.split_point`, `build_humanoid`, `PlaneSettings`, `._selected_landmark`, `test_session.py`, `test_armature.py`, `core/__init__.py`, `PlacedLandmark`, `ViewportOverlay`, `test_planes_panel.py`, `ArmaturePanel`, `ArmatureTool`, `._selected`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Armature` (e.g. with `SculptCache` and `Session`) actually correct?**
  _`Armature` has 2 INFERRED edges - model-reasoned connections that need verification._