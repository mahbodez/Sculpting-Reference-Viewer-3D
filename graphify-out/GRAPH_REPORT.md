# Graph Report - reference-viewer  (2026-09-13)

## Corpus Check
- 106 files · ~397,708 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3355 nodes · 7745 edges · 138 communities (130 shown, 8 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 348 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1fe1e4ee`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FormRun
- VideoSettings
- update_check.py
- Viewport
- plane_axes
- Panel
- MainWindow
- AnnotationStore
- GifWriter
- widgets.py
- RenderSettings
- coarse_lattice
- camera.py
- _wires
- Armature
- README.md
- ViewerState
- FormStore
- framebuffer.py
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
- plane_solids.py
- VideoError
- ShadingPanel
- Film
- test_camera.py
- Mesh
- WakeLock
- ndarray
- _derived
- mesh_renderer.py
- film_export.py
- SurfacePicker
- Camera
- test_armature.py
- ExportLook
- gltf_loader.py
- ExportVideoDialog
- open_writer
- landmarks.py
- Agent Graph-First Instructions
- SceneRenderer
- settings.py
- DataTexture
- armature_tool.py
- load_matcap_pixels
- OrientationSettings
- PlaneSettings
- FilmExport
- FormsPanel
- PlanesPanel
- forms.py
- ArmatureTool
- SliderSpin
- MatcapPanel
- build_ribcage
- load_obj
- MeasureTool
- section.py
- PrimaryForm
- History
- obj_loader.py
- AnnotatePanel
- test_plane_solids.py
- main_window.py
- block_splits
- Solid
- form_group
- application.py
- matcap_panel.py
- ArmaturePanel
- test_tab_switches.py
- viewport.py
- ._chosen_armature
- core/__init__.py
- ._build
- test_forms_panel.py
- TriangleIndex
- mesh.py
- ._picker
- .new_armature
- .pan
- wakelock.py
- Writer
- .mousePressEvent
- test_navigation.py
- RemoveItem
- test_spatial.py
- clay_lumps
- test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else
- _Encoder
- raycast_mesh
- union_field
- ._sync_scene
- Path
- CHANGELOG.md
- .mouseReleaseEvent
- carve
- ._draw_wire
- ._place_armature_node
- test_mesh_io.py
- armature_panel.py
- shading_panel.py
- plane_volume.py
- coarse_lattice
- stone_field
- ArmatureStore
- Wires
- ndarray
- ColorButton
- ShadingMode
- SetAttributes
- _shifts
- release.yml
- shaders.py
- environment.yml
- QualitySettings
- .point_for
- kept_off
- ._selected_rows
- .film_changed
- panel
- ndarray
- .with_landmark_at
- .stage_images
- ._place_form_landmark
- .refresh_list
- test_the_list_and_the_summary_follow_an_edit_without_being_told_to
- _wire_frame
- .point

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 143 edges
2. `Viewport` - 101 edges
3. `PrimaryForm` - 78 edges
4. `Camera` - 75 edges
5. `Armature` - 73 edges
6. `PlaneSettings` - 67 edges
7. `FormsPanel` - 63 edges
8. `ArmaturePanel` - 62 edges
9. `ViewerState` - 61 edges
10. `PlacedLandmark` - 60 edges

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

## Communities (138 total, 8 thin omitted)

### Community 0 - "FormRun"
Cohesion: 0.40
Nodes (3): FormRun, Begin a run against a form already in the store., A guided form part-way through.

### Community 1 - "VideoSettings"
Cohesion: 0.09
Nodes (13): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, FakeViewport, QImage (+5 more)

### Community 2 - "update_check.py"
Cohesion: 0.14
Nodes (22): check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed). (+14 more)

### Community 3 - "Viewport"
Cohesion: 0.08
Nodes (13): QOpenGLWidget, Slide the view so a point sits at the centre, keeping the angle., A form changed: work its clay out again and redraw., Slide the view so a measurement sits at the centre, keeping the angle., End any film being recorded, and wait for its thread to really stop. For…, The document being drawn., The film of the form's making, as far as it has been recorded., Whether frames are being rendered out of a film right now. (+5 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - "Panel"
Cohesion: 0.13
Nodes (8): Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Whether what this panel draws is on screen, or ``None`` if it draws nothing.…, Show or hide what this panel draws; see :meth:`shown`., Ignore widget signals for the duration of the block., Dockable control panels.

### Community 6 - "MainWindow"
Cohesion: 0.06
Nodes (16): QAction, QMainWindow, QTabWidget, MainWindow, Wires the viewport, the panels and the document together., A checkbox on the tab that shows or hides what the panel draws. The same switch…, Keep every tab's switch agreeing with the panel it speaks for., Add a menu entry, optionally with a window-wide shortcut. (+8 more)

### Community 7 - "AnnotationStore"
Cohesion: 0.05
Nodes (34): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, Normals padded to match the points, so callers can zip them freely., Break the stroke into the runs of points ``keep`` marks as surviving. (+26 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "widgets.py"
Cohesion: 0.13
Nodes (17): QFormLayout, QFrame, QScrollArea, collapsible_group(), CollapsibleGroup, _panel_form(), QWidget, Small reusable controls shared by the side panels. (+9 more)

### Community 10 - "RenderSettings"
Cohesion: 0.11
Nodes (21): Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, light_directions(), normal_matrix(), ndarray, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.… (+13 more)

### Community 11 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 12 - "camera.py"
Cohesion: 0.10
Nodes (28): Named camera positions the artist can jump between while sculpting., Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., look_at(), normalize() (+20 more)

### Community 13 - "_wires"
Cohesion: 0.14
Nodes (27): _bar(), _bed_for(), _holds(), A long ellipsoid: one closed form with an obvious axis to lie along., A model read onto a lattice, ready for lumps to be laid on it., Whether a fitted solid has a point inside it., An armature for the volume, with ``off`` naming the rows taking no clay., The claim the whole armature mode rests on. A lump that merely landed near its… (+19 more)

### Community 14 - "Armature"
Cohesion: 0.06
Nodes (36): Armature, ArmatureNode, Bone, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves., A plausible thickness for a node placed by hand. (+28 more)

### Community 15 - "README.md"
Cohesion: 0.23
Nodes (11): Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets (+3 more)

### Community 16 - "ViewerState"
Cohesion: 0.10
Nodes (15): ndarray, Path, QObject, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements, annotations,… (+7 more)

### Community 17 - "FormStore"
Cohesion: 0.20
Nodes (3): FormStore, An ordered, named collection of forms, like the other stores., A name for a new form of this recipe, numbered past any it already has. A form…

### Community 18 - "framebuffer.py"
Cohesion: 0.08
Nodes (16): AccumTarget, ColorTarget, DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality and ghost passes. Four of…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the…, The pair of buffers a see-through model is summed into. Attachment 0 holds the… (+8 more)

### Community 19 - "CameraPanel"
Cohesion: 0.12
Nodes (7): CameraPanel, QListWidgetItem, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "ViewportOverlay"
Cohesion: 0.17
Nodes (18): QColor, QPainter, QPointF, project_visible(), QFont, Draws measurements, tool previews, the orientation gizmo and the readout., Burn a line into the bottom of a frame, for an exported clip. Which stage of…, A line laid over its own dark outline, so it reads against anything. (+10 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.09
Nodes (19): _names(), The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as…, Or there would be no way to turn one back on., A limb is four bones, and deciding not to block the arms in is one decision.…, It is rebuilt on every change, and ticking one row of a selected limb would be… (+11 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.10
Nodes (11): MeasurePanel, _NameOnlyDelegate, QStyledItemDelegate, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing… (+3 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.12
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Deletion goes through the undo stack, so the store only tracks position., test_bookmarks_cycle_and_wrap() (+1 more)

### Community 26 - "NavigationController"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "SectionSettings"
Cohesion: 0.11
Nodes (22): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, Unit axis, or ``None`` for a custom direction., A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn. (+14 more)

### Community 28 - "SectionPanel"
Cohesion: 0.18
Nodes (7): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 29 - "plane_solids.py"
Cohesion: 0.10
Nodes (22): block_count(), piece_count(), ndarray, Handing the planes of a fit to the thing that actually works the volume. The…, The mesh's normals, made unit, with anything unusable recomputed., How finely the model has to be sampled for the lattice it will be read on., Points spread over the model closely enough for a lattice to feel it. The…, How many blocks a count of planes asks the stone to be cut into. One at the… (+14 more)

### Community 30 - "VideoError"
Cohesion: 0.13
Nodes (13): _encode_arguments(), _encoders(), _FFmpegWriter, _no_window(), RuntimeError, An export that could not be written, said in words for the artist., Which encoders this ffmpeg was built with. Asked once, because a build without…, Keep a console window from flashing up on Windows for each ffmpeg call. (+5 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.21
Nodes (7): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel

### Community 32 - "Film"
Cohesion: 0.09
Nodes (13): QThread, Film, A whole making, from the coarsest stage to the one the slider asks for. Held by…, QObject, The film being recorded, or the last one finished., The film already held for ``key``, if there is one., Stop any recording in flight and forget what it was making. The thread is asked…, Begin recording, abandoning whatever was being recorded before. (+5 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (8): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_serialisation_round_trip(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "Mesh"
Cohesion: 0.05
Nodes (63): Mesh, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, A stage as it is to be drawn, with its normals read at ``smooth``. Kept out of…, shaded(), angle_deg(), bent_plate(), cube() (+55 more)

### Community 35 - "WakeLock"
Cohesion: 0.11
Nodes (18): Holds sleep off while the window that owns it is the one in front. The class…, Hold sleep off, or stop holding it, whichever is not already true., Drop the request, if one is out. Safe to call more than once., WakeLock, Broken, skipif, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do. (+10 more)

### Community 36 - "ndarray"
Cohesion: 0.13
Nodes (21): _back_inside(), dual_contour(), _flat_mesh(), ndarray, The surface where ``value`` changes sign, one vertex per lattice cell. Each…, The gradient of a lattice field, by central differences. Which is the direction…, Drop the loose pieces, keeping the form and anything of its size. A block is a…, Read lattice fields at places between their corners, straight-line. Nearest-… (+13 more)

### Community 37 - "_derived"
Cohesion: 0.10
Nodes (24): _kept_laying(), Fresh bones, laid the way the armature was already laying them. The bone list…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _derived(), A guess the artist corrects is theirs, and the mirror leaves it alone., The new list is the edit; the old one has to survive to be undone to., Hips, then the ribcage, then the head, then the limbs largest first. This order… (+16 more)

### Community 38 - "mesh_renderer.py"
Cohesion: 0.12
Nodes (14): bind_default(), current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., Restore a framebuffer captured with :func:`current_framebuffer`., OpenGL rendering layer: shader programs, textures and the scene renderer., _ghost_depth_range(), OpenGL scene renderer: background, shaded mesh, wireframe, section and paint.…, Where the form starts along the view, and how deep it is. The ghost weighs a… (+6 more)

### Community 39 - "film_export.py"
Cohesion: 0.08
Nodes (20): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+12 more)

### Community 40 - "SurfacePicker"
Cohesion: 0.06
Nodes (28): FormLandmarkRef, AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+20 more)

### Community 41 - "Camera"
Cohesion: 0.08
Nodes (16): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target). (+8 more)

### Community 42 - "test_armature.py"
Cohesion: 0.07
Nodes (56): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _chain(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other., The femoral head is in from the ASIS, below it and behind it, by shares of the… (+48 more)

### Community 43 - "ExportLook"
Cohesion: 0.12
Nodes (13): The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, ExportLook, What the frames are to look like, as against what they are of. Laid over the…, Which of the things drawn over the model belong in the frames., ``base`` with this export's choices laid over it. (+5 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.13
Nodes (26): _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry(), _primitives(), ndarray (+18 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.12
Nodes (12): QDialog, QProgressDialog, even(), ExportVideoDialog, Path, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+4 more)

### Community 46 - "open_writer"
Cohesion: 0.13
Nodes (16): ffmpeg_path(), open_writer(), Path, Where ffmpeg is, or ``None``. Looked for in the order of how deliberate each…, Why ``format`` cannot be written here, or ``None`` if it can., Start an encoder for ``settings``, or say why there cannot be one., unavailable(), frames() (+8 more)

### Community 47 - "landmarks.py"
Cohesion: 0.11
Nodes (24): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _humanoid_landmarks(), _mid(), _node_name() (+16 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "SceneRenderer"
Cohesion: 0.11
Nodes (11): MeshBuffers, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are…, Whichever geometry is standing for the model this frame., Sum a see-through model into the ghost buffers, to be resolved after. Blending…, Lay the summed ghost over the scene already in the frame. (+3 more)

### Community 50 - "settings.py"
Cohesion: 0.03
Nodes (78): Coefficients, _empty(), PlaneAxes, PlaneSet, ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, One level of a fit: the planes the shader is to quantise against. A plane is a…, A level with no place in it: nearest direction wins, as before. (+70 more)

### Community 51 - "DataTexture"
Cohesion: 0.12
Nodes (8): Fill the shader's table with a level, if it is not already in it., Replace the annotation geometry; pass an empty list to hide it., DataTexture, default_matcap_pixels(), ndarray, A neutral studio matcap, used before the user picks one., A small RGBA32F table the shader reads exact values out of. Not a picture:…, Store an ``(h, w, 4)`` float array, reallocating only when resized.

### Community 52 - "armature_tool.py"
Cohesion: 0.09
Nodes (20): BoneRef, mirror_landmarks(), The midline landmarks, which are what the median plane is fitted to., The landmark list with every paired landmark reflected into place. A point the…, GuideRun, _project(), Placing and editing the nodes of an armature, freehand or led by a preset.…, Begin a preset run against an armature already in the store. (+12 more)

### Community 53 - "load_matcap_pixels"
Cohesion: 0.18
Nodes (20): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+12 more)

### Community 54 - "OrientationSettings"
Cohesion: 0.09
Nodes (23): OrientationSettings, Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., UpAxis (+15 more)

### Community 55 - "PlaneSettings"
Cohesion: 0.04
Nodes (88): film_key(), planes_for(), The stages a form passes through on its way from a block to a figure. The…, What a film depends on. Everything that changes the shape of any stage, and…, How many solids each stage of a film is made of. Every count from the coarsest…, The detail setting that asks for ``solids``, or ``None`` if none does. The…, Work the form stage by stage, handing each one back as it is finished. A…, record() (+80 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (12): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+4 more)

### Community 57 - "FormsPanel"
Cohesion: 0.04
Nodes (32): FormsPanel, QTreeWidgetItem, Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Begin a run against a fresh form: a preset's walk, or a freeform's., Take up the selected freeform again, so more landmarks can go on it. The same…, The freeform the highlighted row belongs to, when no run is on. (+24 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.19
Nodes (6): PlanesPanel, Lay one length of wire earlier or later, as one undoable step., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Breaks the form into planes, in the shading or in the geometry itself., Re-read the armatures and what the chosen one is laying down. Called whenever…

### Community 59 - "forms.py"
Cohesion: 0.05
Nodes (62): DegenerateHullError, The points are flat, collinear or too few to hold any volume., build_freeform(), _centre(), form_landmark_title(), form_spec(), FormFill, FormPreset (+54 more)

### Community 60 - "ArmatureTool"
Cohesion: 0.06
Nodes (38): LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, Handle, The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now., How many landmarks are placed, out of how many will be asked for. (+30 more)

### Community 61 - "SliderSpin"
Cohesion: 0.14
Nodes (7): PointEdit, Re-scale the control, e.g. once a model's size is known., Grow the slider to take in a value from beyond its end., Three spin boxes for one point in space. Keyboard tracking is off, so a typed…, Match the arrows to the size of the thing being moved., A float slider paired with a spin box, kept in sync. The slider works in…, SliderSpin

### Community 62 - "MatcapPanel"
Cohesion: 0.22
Nodes (6): QIcon, QPixmap, MatcapPanel, Rebuild the thumbnail list from the resources folder., Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…

### Community 63 - "build_ribcage"
Cohesion: 0.07
Nodes (58): _across(), blend_rings(), build_head(), build_pelvis(), build_ribcage(), fit_plane(), _head_frame(), _HeadFrame (+50 more)

### Community 64 - "load_obj"
Cohesion: 0.22
Nodes (14): _load_generic(), load_obj(), Path, Line-by-line reader for files the fast path declines., Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, Negative face indices count back from the most recent vertex., test_obj_relative_indices_still_load(), OBJ parsing: normals, triangulation and index handling. (+6 more)

### Community 65 - "MeasureTool"
Cohesion: 0.14
Nodes (6): MeasureTool, Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., What the forms tool is waiting for, said in as few lines as it takes., What the armature tool is waiting for, said in as few lines as it takes.

### Community 66 - "section.py"
Cohesion: 0.20
Nodes (8): Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Which side of the plane survives the cut., SectionAxis, SectionMode, Cross-section controls: the cutting plane, what it keeps and how it reads.

### Community 67 - "PrimaryForm"
Cohesion: 0.07
Nodes (56): PlacedLandmark, One anatomical point the artist put on the model during a guided run., build_form(), built_count(), form_mesh(), landmark_signature(), mirror_form_landmarks(), PrimaryForm (+48 more)

### Community 68 - "History"
Cohesion: 0.06
Nodes (27): Camera motion is deliberately not undoable, AddItem, Append an item to a document list., Command, History, One reversible change, named for the undo menu., A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive… (+19 more)

### Community 69 - "obj_loader.py"
Cohesion: 0.15
Nodes (19): MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast() (+11 more)

### Community 70 - "AnnotatePanel"
Cohesion: 0.19
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 71 - "test_plane_solids.py"
Cohesion: 0.04
Nodes (99): auto_smooth(), A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), block(), box() (+91 more)

### Community 72 - "main_window.py"
Cohesion: 0.19
Nodes (15): The newest published release, as GitHub describes it., Release, Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version(), Application window: viewport, docked panels, menus and shortcuts., is_skipped(), QWidget (+7 more)

### Community 73 - "block_splits"
Cohesion: 0.17
Nodes (12): block_labels(), block_splits(), blocks(), _cuts(), _hull_air(), The corners a hull round ``points`` holds that ``points`` do not fill. The hull…, Where a block might be cut in two: a direction, and a point to pass through.…, The greedy split, with every count along the way kept. The same walk… (+4 more)

### Community 74 - "Solid"
Cohesion: 0.06
Nodes (42): convex_hull(), flat_mesh(), merged(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, The outward unit normal at each vertex: the area-weighted mean of its faces'. A… (+34 more)

### Community 75 - "form_group"
Cohesion: 0.26
Nodes (7): QGroupBox, QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row(), form_group(), A titled group box with a form layout, ready to be filled.

### Community 76 - "application.py"
Cohesion: 0.13
Nodes (19): ArgumentParser, Namespace, QApplication, QSplashScreen, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font() (+11 more)

### Community 77 - "matcap_panel.py"
Cohesion: 0.31
Nodes (11): available_matcaps(), _bundled_root(), image_path(), matcap_dir(), model_dir(), Path, Locations of the bundled resources. ``REFVIEW_RESOURCES`` overrides the search,…, Return PyInstaller's extracted application directory when frozen. (+3 more)

### Community 78 - "ArmaturePanel"
Cohesion: 0.07
Nodes (16): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take back the landmark before this one and ask for it again., Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors. (+8 more)

### Community 79 - "test_tab_switches.py"
Cohesion: 0.29
Nodes (7): app(), fixture, parametrize, The switch on each tab: it reads what the panel draws and writes it back. Every…, One offscreen Qt application for the run; see test_film_recorder., test_a_panel_that_draws_nothing_has_no_switch(), test_the_switch_is_the_panels_own_visibility_setting()

### Community 80 - "viewport.py"
Cohesion: 0.04
Nodes (63): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a…, One painted polyline lying on the surface., Stroke (+55 more)

### Community 81 - "._chosen_armature"
Cohesion: 0.19
Nodes (7): QListWidgetItem, The armature the clay is being built on, or ``None``. An index past the end of…, The bones of the chosen armature, in the order the clay goes down. Every intact…, Take lengths of wire out of the clay, or put them back. A tick on a row that…, Put the clay on all of the wire, or take it off all of it., Write which lengths of wire take clay, as one undoable step., What can be done to the list, given where the handle is and whether a film is…

### Community 82 - "core/__init__.py"
Cohesion: 0.15
Nodes (18): Qt-free geometry, camera and document model for the reference viewer., Bounds, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc(), PedestalSettings, ndarray (+10 more)

### Community 83 - "._build"
Cohesion: 0.27
Nodes (6): QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 84 - "test_forms_panel.py"
Cohesion: 0.12
Nodes (29): app(), _click(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The…, A form row hands the whole form to update_enabled, whose landmark list must be… (+21 more)

### Community 85 - "TriangleIndex"
Cohesion: 0.15
Nodes (13): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., Build the index from expanded triangle corners, shape ``(T, 3, 3)``. (+5 more)

### Community 86 - "mesh.py"
Cohesion: 0.15
Nodes (18): compute_vertex_normals(), _gathered(), Triangle-mesh containers shared by the loader, the renderer and picking., Which group each of ``total`` things lands in, given pairs that agree. Hooking…, Area-weighted smooth vertex normals for an indexed triangle soup., _ascii_corners(), _binary_corners(), load_stl() (+10 more)

### Community 87 - "._picker"
Cohesion: 0.17
Nodes (5): Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Apply the drag live, so the clay re-forms under the cursor., Rub out the stroke points under the eraser, live.

### Community 90 - "wakelock.py"
Cohesion: 0.09
Nodes (14): c_void_p, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., A way of asking one platform to stay awake. (+6 more)

### Community 91 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 92 - ".mousePressEvent"
Cohesion: 0.15
Nodes (6): ndarray, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on., Take hold of a form's landmark, to move it or just to say which one it is., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…

### Community 93 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 94 - "RemoveItem"
Cohesion: 0.12
Nodes (8): Delete the item at ``index``, putting it back in place on undo., RemoveItem, Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., Run a bone between the row selected now and the node held before it., The node the selected row stands for, if the row is a node at all., The armature the selected row stands for, when the row is not a node., Follow the highlighted row, without rebuilding the list underneath it. Going…

### Community 95 - "test_spatial.py"
Cohesion: 0.29
Nodes (9): _grid(), The picking accelerator: it must be fast without changing any answer., A bumpy height field, so rays hit different triangles at different depths., The pruned candidate set must never miss the true intersection., test_a_ray_that_misses_the_model_is_pruned_away(), test_an_empty_index_returns_no_candidates(), test_every_triangle_lands_in_exactly_one_leaf(), test_the_index_finds_the_triangle_a_ray_actually_hits() (+1 more)

### Community 96 - "clay_lumps"
Cohesion: 0.16
Nodes (18): _box_facings(), clay_lumps(), clay_pieces(), fit_piece(), _frame(), grow_piece(), join_pieces(), Which three ways a lump of material runs. Columns, thinnest first. Thinnest… (+10 more)

### Community 97 - "test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else"
Cohesion: 0.33
Nodes (5): lattice_fineness(), How much finer than usual a detail setting asks the lattice to be. One at the…, How much finer than usual the geometry's lattice is worked on., The slider's own end already asks for every plane a fit will give, so what a…, test_typing_past_the_geometry_slider_buys_a_finer_lattice_and_nothing_else()

### Community 98 - "_Encoder"
Cohesion: 0.25
Nodes (5): Queue, _Encoder, QObject, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 99 - "raycast_mesh"
Cohesion: 0.13
Nodes (22): Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``. (+14 more)

### Community 100 - "union_field"
Cohesion: 0.25
Nodes (8): block_field(), piece_bounds(), One row of coordinates per axis over ``box``, shaped so they broadcast., The union of the blocks, as a field whose zero is its surface. Each block is…, The box a lump of clay lives in, read off the six facings of its frame. Those…, The union of a set of convex solids, as a field whose zero is its surface. The…, _rows(), union_field()

### Community 101 - "._sync_scene"
Cohesion: 0.13
Nodes (6): Regenerate the pedestal and the cut contour when their settings move. Both are…, The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on., Cut the mesh with each section plane and expand the result to strokes.

### Community 102 - "Path"
Cohesion: 0.23
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 103 - "CHANGELOG.md"
Cohesion: 0.25
Nodes (8): Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, STL and glTF import (1.1.0), Units are adopted, never guessed

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.11
Nodes (9): Record the finished gesture: a move, a resize, or a plain click. A press that…, Record the finished drag as one step, or read a press as a selection., Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…, Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Record the finished drag as one step, or read a press as a selection., Track the form landmark under the cursor; True when it changed. (+1 more)

### Community 105 - "carve"
Cohesion: 0.32
Nodes (8): carve(), _corner_facings(), facings(), fitted_facings(), The form ``directions`` leave of the model, worked one way or the other.…, Twenty-six directions round a cube, for judging how much air a block holds.…, The supporting directions a block may be cut along. ``(m, 3)``. The twenty-six…, The form's own facings alone, both ways round and without duplicates. What a…

### Community 106 - "._draw_wire"
Cohesion: 0.32
Nodes (4): Handle, A world radius in pixels, measured rather than converted. Projecting the node…, Convert a 0-1 RGB tuple to a QColor., to_qcolor()

### Community 107 - "._place_armature_node"
Cohesion: 0.22
Nodes (4): The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 108 - "test_mesh_io.py"
Cohesion: 0.22
Nodes (14): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one(), test_binary_stl_welds_shared_corners() (+6 more)

### Community 109 - "armature_panel.py"
Cohesion: 0.11
Nodes (14): BoneLabels, Buried, Enum, str, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…, lock_icon(), Small painted icons. Drawing the padlock rather than shipping an image file… (+6 more)

### Community 110 - "shading_panel.py"
Cohesion: 0.33
Nodes (5): LightSettings, Material parameters shared by the analytic shading modes., A key light, an opposing fill and a hemispherical ambient term., SurfaceSettings, Shading mode, lighting, surface material and scene furniture controls.

### Community 111 - "plane_volume.py"
Cohesion: 0.18
Nodes (15): _axes(), encloses(), lattice(), lay_bed(), nearest_surface(), _passes(), Blocking a form in out of its own planes, from the outside or from a core. A…, Read the model onto a lattice, ready for solids to be laid on it. (+7 more)

### Community 112 - "coarse_lattice"
Cohesion: 0.33
Nodes (6): app(), coarse_lattice(), fixture, MonkeyPatch, One Qt application for the whole run; offscreen, so CI needs no display.…, Read every model on a small lattice, so the suite stays quick.

### Community 113 - "stone_field"
Cohesion: 0.20
Nodes (10): Bed, block_bounds(), coarse_bounds(), point_support(), The lattice a form is worked on, and the model read onto it. Everything here…, The union of the blocks a labelling cuts the model into, and its facings. Stone…, The index range each block covers. ``(count, 3)`` lows and highs, inclusive. A…, Those ranges, read on the fine lattice the coarse one stands for. (+2 more)

### Community 114 - "ArmatureStore"
Cohesion: 0.18
Nodes (4): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 115 - "Wires"
Cohesion: 0.13
Nodes (10): Holds the working state between one turn of the sliders and the next.…, Drop everything held, so the next call starts from the fit., The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache, An armature, as the clay reads it: where each length of wire runs. The order…, How many lumps the wire itself asks for., What a cache has to compare to know the wire has not moved. (+2 more)

### Community 116 - "ndarray"
Cohesion: 0.17
Nodes (5): ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, test_bounds_of_an_empty_point_set(), ValueError

### Community 117 - "ColorButton"
Cohesion: 0.38
Nodes (3): ColorButton, QPushButton, A swatch button that opens a colour picker. Colours are exchanged as 0-1 RGB…

### Community 118 - "ShadingMode"
Cohesion: 0.18
Nodes (4): Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode, TestEven

### Community 119 - "SetAttributes"
Cohesion: 0.14
Nodes (8): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, QTreeWidgetItem, Run a row's edit once Qt has finished delivering the current signal. Committing…, Record an edit the viewport's tool worked out., Join two nodes of one armature, if they are two and they are one armature., Commit a renamed or re-checked row, if anything actually changed.

### Community 120 - "_shifts"
Cohesion: 0.25
Nodes (8): _balloon(), close_gaps(), outside_points(), Fill the slots the lumps leave between them, without taking clay away. The…, Grow or shrink a solid by ``reach`` cells, one axis at a time. A separable…, Where the model stops: the corners just outside ``room``. ``(n, 3)``. Only the…, The pair of slices that read a lattice ``span`` cells over along ``axis``., _shifts()

### Community 121 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 122 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 123 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 124 - "QualitySettings"
Cohesion: 0.50
Nodes (5): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, QualitySettings, Soft shadows and ambient occlusion for the high-quality mode. Both are screen-…

### Community 126 - "kept_off"
Cohesion: 0.50
Nodes (4): kept_off(), Which points lie in the sleeve a length of wire declares round itself. The wire…, Which material lies under a length of wire that is to take no clay. Turning a…, within_sleeve()

### Community 129 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 130 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 132 - ".stage_images"
Cohesion: 0.16
Nodes (8): QOpenGLFramebufferObject, QImage, The nodes the model is standing in front of, worked out at most once. A node is…, One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A…, An offscreen target the frames are drawn into, made once per export.…, Draw the scene into ``surface`` and read it back as an image., Lay the overlay -- and the caption, if it was asked for -- on a frame. Painted…

### Community 134 - ".refresh_list"
Cohesion: 0.29
Nodes (3): The landmarks in the preset's own order, top of the figure down. Placement…, Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing.

### Community 138 - "_wire_frame"
Cohesion: 0.50
Nodes (4): _perpendicular(), Two unit directions across ``along``, neither of them near it., Which three ways a lump laid along a wire runs. Columns, thinnest first. The…, _wire_frame()

### Community 140 - ".point"
Cohesion: 0.29
Nodes (4): ndarray, Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-…, Screen-to-world scale at a given depth along the view direction.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `VideoSettings`, `plane_axes`, `_wires`, `README.md`, `ViewerState`, `FormStore`, `SectionSettings`, `plane_solids.py`, `Film`, `ndarray`, `mesh_renderer.py`, `ExportLook`, `gltf_loader.py`, `SceneRenderer`, `settings.py`, `DataTexture`, `OrientationSettings`, `PlaneSettings`, `FilmExport`, `forms.py`, `load_obj`, `section.py`, `PrimaryForm`, `obj_loader.py`, `test_plane_solids.py`, `Solid`, `viewport.py`, `core/__init__.py`, `TriangleIndex`, `mesh.py`, `test_spatial.py`, `raycast_mesh`, `carve`, `test_mesh_io.py`, `plane_volume.py`, `stone_field`, `Wires`, `ndarray`, `ShadingMode`?**
  _High betweenness centrality (0.156) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `.stage_images`, `._place_form_landmark`, `MainWindow`, `ViewerState`, `ViewportOverlay`, `NavigationController`, `film_export.py`, `SurfacePicker`, `ExportLook`, `ExportVideoDialog`, `PlaneSettings`, `FilmExport`, `forms.py`, `ArmatureTool`, `MeasureTool`, `PrimaryForm`, `main_window.py`, `Solid`, `viewport.py`, `._picker`, `.mousePressEvent`, `_Encoder`, `._sync_scene`, `.mouseReleaseEvent`, `._place_armature_node`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `Armature` connect `Armature` to `ndarray`, `.with_landmark_at`, `.refresh_list`, `test_planes_panel.py`, `plane_solids.py`, `_derived`, `test_armature.py`, `armature_tool.py`, `ArmatureTool`, `MeasureTool`, `ArmaturePanel`, `viewport.py`, `core/__init__.py`, `.new_armature`, `RemoveItem`, `._draw_wire`, `armature_panel.py`, `ArmatureStore`, `Wires`?**
  _High betweenness centrality (0.058) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PrimaryForm` (e.g. with `PlacedLandmark` and `DegenerateHullError`) actually correct?**
  _`PrimaryForm` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._