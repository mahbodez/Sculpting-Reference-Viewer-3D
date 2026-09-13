# Graph Report - reference-viewer  (2026-09-13)

## Corpus Check
- 105 files · ~391,165 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3246 nodes · 7440 edges · 137 communities (129 shown, 8 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 336 edges (avg confidence: 0.56)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5f349262`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FormTool
- PlaneSet
- update_check.py
- Viewport
- plane_axes
- viewport.py
- MainWindow
- Stroke
- GifWriter
- MeasurementStore
- SceneRenderer
- PlaneSettings
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
- QPainter
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- NavigationController
- SectionSettings
- SectionPanel
- plane_solids.py
- VideoError
- ShadingPanel
- ViewportOverlay
- test_camera.py
- test_plane_clusters.py
- WakeLock
- plane_volume.py
- History
- MeshBuffers
- film_export.py
- AnnotateTool
- Camera
- test_armature.py
- ExportLook
- gltf_loader.py
- ExportVideoDialog
- VideoSettings
- landmarks.py
- Agent Graph-First Instructions
- ._set_geometry
- plane_clusters.py
- Texture2D
- armature_tool.py
- AnnotationSettings
- OrientationSettings
- Film
- FilmExport
- FormsPanel
- PlanesPanel
- Solid
- ArmatureTool
- form_group
- .update_enabled
- form_shapes.py
- lock_icon
- MeasureTool
- test_navigation.py
- PrimaryForm
- Command
- Mesh
- AnnotatePanel
- test_plane_solids.py
- Release
- stroke_renderer.py
- convex.py
- ._build
- application.py
- test_forms.py
- ._selected_landmark
- build_pelvis
- Session
- _derived
- Bounds
- ._build
- test_forms_panel.py
- section.py
- shaders.py
- ._picker
- ArmaturePanel
- .pan
- wakelock.py
- RemoveItem
- .mousePressEvent
- settings.py
- ._selected
- .update_enabled
- mesh_renderer.py
- plane_count
- OverlayParts
- raycast_mesh
- .refresh_list
- ._sync_scene
- Path
- CHANGELOG.md
- SetAttributes
- picking.py
- _ScreenSaverBackend
- ._place_armature_node
- ._on_bone_toggled
- core/__init__.py
- test_annotation.py
- .split
- coarse_lattice
- ._start_update_check
- .film_changed
- coarse_lattice
- panel
- _WindowsBackend
- ShadingMode
- AddItem
- ._selected_form
- release.yml
- _MacBackend
- environment.yml
- _NameOnlyDelegate
- ring_through
- panel
- .endpoint
- refview/__init__.py
- .new_armature
- ndarray
- ._refresh_order
- .stage_images
- ._place_form_landmark
- .refresh_list
- .surface_opacity
- _summary

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

## Communities (137 total, 8 thin omitted)

### Community 0 - "FormTool"
Cohesion: 0.08
Nodes (23): FormLandmarkRef, FormSettings, How the forms are drawn, and how their landmarks are placed., FormRun, FormTool, ndarray, Every landmark the walk will ask for under these choices. With mirroring on,…, The landmarks still to place, in order, the current one first. (+15 more)

### Community 1 - "PlaneSet"
Cohesion: 0.09
Nodes (18): _empty(), PlaneAxes, PlaneSet, ndarray, One level of a fit: the planes the shader is to quantise against. A plane is a…, A level with no place in it: nearest direction wins, as before., The planes a model falls into, at every count. Built once per mesh and per…, The best ``count`` planes, or as many as the model supports. A model whose… (+10 more)

### Community 2 - "update_check.py"
Cohesion: 0.16
Nodes (18): is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed)., Numeric components of ``text``, or ``None`` when it is not a version. A pre-…, Whether ``candidate`` is a strictly later version than ``current``. (+10 more)

### Community 3 - "Viewport"
Cohesion: 0.08
Nodes (13): QOpenGLWidget, Slide the view so a point sits at the centre, keeping the angle., A form changed: work its clay out again and redraw., Slide the view so a measurement sits at the centre, keeping the angle., End any film being recorded, and wait for its thread to really stop. For…, The document being drawn., The film of the form's making, as far as it has been recorded., Whether frames are being rendered out of a film right now. (+5 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - "viewport.py"
Cohesion: 0.05
Nodes (51): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, What the annotate tool does with a drag. The first three describe the shape a…, Named camera positions the artist can jump between while sculpting., The handful of undoable edits the whole application is built from.…, Swap the whole contents of a document list. Used for bulk edits -- clearing the… (+43 more)

### Community 6 - "MainWindow"
Cohesion: 0.07
Nodes (12): QAction, QMainWindow, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, The document this window edits., Open the window that writes the film of a form's making to a file. Nothing is… (+4 more)

### Community 7 - "Stroke"
Cohesion: 0.13
Nodes (11): AnnotationStore, An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Stroke, The surviving arc wraps past the start of the list, so the gap is rotated to…, test_a_broken_circle_stays_one_piece() (+3 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "MeasurementStore"
Cohesion: 0.16
Nodes (5): MeasurementStore, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., An ordered, named collection of measurements. Deliberately plain: the Qt layer…, test_store_auto_names_new_measurements()

### Community 10 - "SceneRenderer"
Cohesion: 0.11
Nodes (23): Everything the viewport needs in order to draw a frame., RenderSettings, light_directions(), normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.… (+15 more)

### Community 11 - "PlaneSettings"
Cohesion: 0.04
Nodes (76): _gathered(), Triangle-mesh containers shared by the loader, the renderer and picking., Which group each of ``total`` things lands in, given pairs that agree. Hooking…, Reading the planes of a form out of the model's own normals. The grid quantiser…, film_key(), The stages a form passes through on its way from a block to a figure. The…, What a film depends on. Everything that changes the shape of any stage, and…, PlaneSettings (+68 more)

### Community 12 - "camera.py"
Cohesion: 0.14
Nodes (22): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-…, Return ``v`` scaled to unit length, or ``fallback`` for a zero vector. (+14 more)

### Community 13 - "_wires"
Cohesion: 0.13
Nodes (29): The order the artist put the bones in is what the scrub walks through, which is…, test_a_film_of_clay_on_a_wire_lays_it_down_in_the_order_it_was_listed(), _bar(), _bed_for(), _holds(), A long ellipsoid: one closed form with an obvious axis to lie along., A model read onto a lattice, ready for lumps to be laid on it., Whether a fitted solid has a point inside it. (+21 more)

### Community 14 - "Armature"
Cohesion: 0.04
Nodes (38): Armature, ArmatureStore, Bone, Point3, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves. (+30 more)

### Community 15 - "README.md"
Cohesion: 0.27
Nodes (10): Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets (+2 more)

### Community 16 - "ViewerState"
Cohesion: 0.10
Nodes (14): ndarray, Path, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements, annotations,…, Rotate the measurements, annotations, armature and forms onto the turned model.… (+6 more)

### Community 17 - "FormStore"
Cohesion: 0.18
Nodes (4): FormStore, An ordered, named collection of primary forms, like the other stores., A name for a new form of this preset, numbered past any it already has., test_a_form_store_names_forms_past_the_ones_it_has()

### Community 18 - "framebuffer.py"
Cohesion: 0.08
Nodes (16): AccumTarget, ColorTarget, DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality and ghost passes. Four of…, A single-channel colour framebuffer, used for the occlusion buffers., Depth plus view-space normals: the inputs the occlusion pass reads. Storing the…, The pair of buffers a see-through model is summed into. Attachment 0 holds the… (+8 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): CameraPanel, QListWidgetItem, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 21 - "ShaderProgram"
Cohesion: 0.12
Nodes (9): OpenGL rendering layer: shader programs, textures and the scene renderer., ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError (+1 more)

### Community 22 - "QPainter"
Cohesion: 0.18
Nodes (13): QColor, QPainter, QPointF, project_visible(), A line laid over its own dark outline, so it reads against anything., An unfilled circle: how thick the form is here, not how big a dot is., A square grip, so an editable end reads differently from a fixed one., The landmarks of a guided run, and the point about to be placed. (+5 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.08
Nodes (21): _names(), The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as…, Or there would be no way to turn one back on., A limb is four bones, and deciding not to block the arms in is one decision.…, It is rebuilt on every change, and ticking one row of a selected limb would be… (+13 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.11
Nodes (11): MeasurePanel, _NameOnlyDelegate, QStyledItemDelegate, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing… (+3 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.11
Nodes (10): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., QObject, Deletion goes through the undo stack, so the store only tracks position. (+2 more)

### Community 26 - "NavigationController"
Cohesion: 0.13
Nodes (11): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Tracks an in-progress drag and applies it to a camera. (+3 more)

### Community 27 - "SectionSettings"
Cohesion: 0.11
Nodes (22): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, Unit axis, or ``None`` for a custom direction., A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn. (+14 more)

### Community 28 - "SectionPanel"
Cohesion: 0.20
Nodes (7): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 29 - "plane_solids.py"
Cohesion: 0.10
Nodes (25): planes_for(), How many solids each stage of a film is made of. Every count from the coarsest…, The detail setting that asks for ``solids``, or ``None`` if none does. The…, stage_counts(), block_count(), piece_count(), ndarray, Handing the planes of a fit to the thing that actually works the volume. The… (+17 more)

### Community 30 - "VideoError"
Cohesion: 0.09
Nodes (15): _FFmpegWriter, ndarray, Path, RuntimeError, An export that could not be written, said in words for the artist., What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``. (+7 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.18
Nodes (9): LightSettings, A key light, an opposing fill and a hemispherical ambient term., Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Show what this mode is actually lit and shaded by, and hide the rest. A matcap… (+1 more)

### Community 32 - "ViewportOverlay"
Cohesion: 0.17
Nodes (11): Handle, QFont, Draws measurements, tool previews, the orientation gizmo and the readout., Burn a line into the bottom of a frame, for an exported clip. Which stage of…, A world radius in pixels, measured rather than converted. Projecting the node…, What the forms tool is waiting for, said in as few lines as it takes., Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, What the armature tool is waiting for, said in as few lines as it takes. (+3 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (8): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_serialisation_round_trip(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.07
Nodes (48): angle_deg(), bent_plate(), cube(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What…, How far the least well served of ``wanted`` is from anything offered. (+40 more)

### Community 35 - "WakeLock"
Cohesion: 0.17
Nodes (13): Holds sleep off while the window that owns it is the one in front. The class…, WakeLock, Broken, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do., A platform that refuses, the way an old or locked-down one might., The viewer must open and close normally on a machine that says no., Recorder (+5 more)

### Community 36 - "plane_volume.py"
Cohesion: 0.04
Nodes (114): Work the form stage by stage, handing each one back as it is finished. A…, record(), _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field() (+106 more)

### Community 37 - "History"
Cohesion: 0.17
Nodes (14): History, A bounded undo/redo stack., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch(), test_commands_carry_their_channel_and_name() (+6 more)

### Community 38 - "MeshBuffers"
Cohesion: 0.10
Nodes (9): MeshBuffers, Whichever geometry is standing for the model this frame., Fill the shader's table with a level, if it is not already in it., Replace the annotation geometry; pass an empty list to hide it., Vertex/index buffers for one mesh, bound through a single VAO., A single vertex buffer holding every visible stroke., StrokeBuffers, default_matcap_pixels() (+1 more)

### Community 39 - "film_export.py"
Cohesion: 0.08
Nodes (26): _encode_arguments(), _encoders(), ffmpeg_path(), _no_window(), Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a… (+18 more)

### Community 40 - "AnnotateTool"
Cohesion: 0.16
Nodes (7): AnnotateTool, Project screen-space samples onto the surface, breaking at the misses., Continue the open run with a hit, or end it where the ray missed., Turns drags into strokes, and reports what the eraser is touching., Abandon the stroke in progress., The strokes being laid down; the overlay previews them in 2D., End the drag and return the strokes it produced.

### Community 41 - "Camera"
Cohesion: 0.08
Nodes (16): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target). (+8 more)

### Community 42 - "test_armature.py"
Cohesion: 0.07
Nodes (58): ArmatureNode, One joint of the wire: where it is, and how thick the form is there., build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _chain(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer. (+50 more)

### Community 43 - "ExportLook"
Cohesion: 0.08
Nodes (21): The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, ExportLook, What the frames are to look like, as against what they are of. Laid over the…, ``base`` with this export's choices laid over it., The line burned into the corner of the frame for ``stage``. Counted off the… (+13 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.06
Nodes (55): STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry() (+47 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.12
Nodes (12): QDialog, QProgressDialog, even(), ExportVideoDialog, Path, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+4 more)

### Community 46 - "VideoSettings"
Cohesion: 0.10
Nodes (18): open_writer(), How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., Start an encoder for ``settings``, or say why there cannot be one., VideoSettings (+10 more)

### Community 47 - "landmarks.py"
Cohesion: 0.11
Nodes (24): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _humanoid_landmarks(), _mid(), _node_name() (+16 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "._set_geometry"
Cohesion: 0.20
Nodes (4): Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are…, Forget the contents without releasing the buffer objects.

### Community 50 - "plane_clusters.py"
Cohesion: 0.05
Nodes (52): Coefficients, How much surface each vertex stands for: a third of each triangle on it.…, What each block of the design matrix counts for, against the normals. A fit…, Whether anything but the normals is being read at all., vertex_weights(), _compact(), _consensus(), _cut() (+44 more)

### Community 51 - "Texture2D"
Cohesion: 0.14
Nodes (6): DataTexture, ndarray, An RGBA8 2D texture with clamped edges and mipmapped minification., A small RGBA32F table the shader reads exact values out of. Not a picture:…, Store an ``(h, w, 4)`` float array, reallocating only when resized., Texture2D

### Community 52 - "armature_tool.py"
Cohesion: 0.11
Nodes (15): mirror_landmarks(), The midline landmarks, which are what the median plane is fitted to., The landmark list with every paired landmark reflected into place. A point the…, GuideRun, Placing and editing the nodes of an armature, freehand or led by a preset.…, Begin a preset run against an armature already in the store., A guided preset part-way through. The index walks the preset's own list rather…, How far along a screen-space segment the cursor's nearest point lies. (+7 more)

### Community 53 - "AnnotationSettings"
Cohesion: 0.16
Nodes (9): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Start a drag. Returns ``False`` when there is nothing to paint on., Extend the drag. Returns ``True`` when the view needs repainting. (+1 more)

### Community 54 - "OrientationSettings"
Cohesion: 0.09
Nodes (24): OrientationSettings, Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., UpAxis (+16 more)

### Community 55 - "Film"
Cohesion: 0.09
Nodes (13): QThread, Film, A whole making, from the coarsest stage to the one the slider asks for. Held by…, QObject, The film being recorded, or the last one finished., The film already held for ``key``, if there is one., Stop any recording in flight and forget what it was making. The thread is asked…, Begin recording, abandoning whatever was being recorded before. (+5 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (11): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+3 more)

### Community 57 - "FormsPanel"
Cohesion: 0.13
Nodes (6): FormsPanel, Take back the landmark before this one and ask for it again., Record an edit the viewport's tool worked out., The multiplier the position boxes are read and written through., Keep the ghost switch agreeing with the Shading panel's., Arms the forms tool, runs the guided presets and lists what they built.

### Community 58 - "PlanesPanel"
Cohesion: 0.17
Nodes (10): PlanesPanel, Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Show what this way of working needs, and put the rest away. A setting that does…, Breaks the form into planes, in the shading or in the geometry itself., The armature the clay is being built on, or ``None``. An index past the end of…, Re-read the armatures and what the chosen one is laying down. Called whenever…, Put the clay on all of the wire, or take it off all of it. (+2 more)

### Community 59 - "Solid"
Cohesion: 0.15
Nodes (9): One convex piece of a form: its hull vertices and outward-wound faces., The longest side of the box the solid sits in., Whether a point lies inside, or within ``slack`` of the surface., A flat-shaded mesh, every triangle with its own three corners. Corners are not…, Solid, loft(), A closed curve round a mass, sampled at fixed angles about its centre. Kept as…, The convex solid through a stack of rings. (+1 more)

### Community 60 - "ArmatureTool"
Cohesion: 0.05
Nodes (46): BoneRef, LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, _project(), Handle, ndarray (+38 more)

### Community 61 - "form_group"
Cohesion: 0.04
Nodes (46): QFormLayout, QFrame, QGroupBox, QScrollArea, The armature: its nodes, the guided presets, and how the wire is drawn., Panel, QWidget, Shared plumbing for the dockable side panels. (+38 more)

### Community 62 - ".update_enabled"
Cohesion: 0.17
Nodes (6): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., Follow the highlighted row, without rebuilding the list underneath it. Going…, Highlight the row for a node picked in the view., Highlight the row for a landmark picked in the view.

### Community 63 - "form_shapes.py"
Cohesion: 0.14
Nodes (23): _across(), blend_rings(), build_head(), fit_plane(), _head_frame(), _HeadFrame, _lagrange(), _mid() (+15 more)

### Community 64 - "lock_icon"
Cohesion: 0.50
Nodes (4): lock_icon(), Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if…, _render()

### Community 65 - "MeasureTool"
Cohesion: 0.12
Nodes (10): MeasureTool, Handle, ndarray, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., Where a click at ``(x, y)`` would put a point. With free placement the point… (+2 more)

### Community 66 - "test_navigation.py"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.05
Nodes (73): PlacedLandmark, One anatomical point the artist put on the model during a guided run., merged(), Several flat meshes as one, or ``None`` when there is nothing to draw., build_form(), built_count(), _centre(), form_landmark_title() (+65 more)

### Community 68 - "Command"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 69 - "Mesh"
Cohesion: 0.06
Nodes (49): compute_vertex_normals(), One entry point for every mesh format the viewer reads. Callers ask for a path…, Mesh, MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., Return a copy whose bounding-box centre sits at the origin., Area-weighted smooth vertex normals for an indexed triangle soup. (+41 more)

### Community 70 - "AnnotatePanel"
Cohesion: 0.28
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 71 - "test_plane_solids.py"
Cohesion: 0.04
Nodes (92): auto_smooth(), A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), The claim the whole film rests on, asked again with an armature under it: an…, test_the_last_stage_of_a_film_on_a_wire_is_the_form_the_slider_gives() (+84 more)

### Community 72 - "Release"
Cohesion: 0.23
Nodes (12): check_for_update(), fetch_latest_release(), The newest published release, as GitHub describes it., Return the newest published release, or raise :class:`UpdateCheckError`., The newest release when it is later than ``current_version``, else ``None``., Release, is_skipped(), Background release check and the notice it puts in front of the artist. The… (+4 more)

### Community 73 - "stroke_renderer.py"
Cohesion: 0.24
Nodes (10): build_segment_vertices(), build_vertices(), _expand(), ndarray, Geometry for the surface annotations and the cross-section contour. Strokes are…, Replace the buffer contents with a prepared vertex block., Expand strokes into the triangle soup the stroke shader expects. Every segment…, Expand loose ``(n, 2, 3)`` segments -- the section contour -- the same way. The… (+2 more)

### Community 74 - "convex.py"
Cohesion: 0.16
Nodes (16): convex_hull(), DegenerateHullError, flat_mesh(), _outward(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, Every face as a unit normal and an offset, ``normal @ x <= offset`` inside., What is left on the ``normal @ x <= offset`` side of a plane. The hull of the… (+8 more)

### Community 75 - "._build"
Cohesion: 0.33
Nodes (4): QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 76 - "application.py"
Cohesion: 0.05
Nodes (54): ArgumentParser, Color, Namespace, QApplication, QIcon, QPixmap, QSplashScreen, Charcoal matcap (+46 more)

### Community 77 - "test_forms.py"
Cohesion: 0.14
Nodes (23): build_ribcage(), The egg of the ribcage, with the arch chipped out of the front of it. Three…, _closed(), _inside(), The primary forms: convex solids, the landmarks that build them, and the walk., Every edge shared by exactly two faces: the hull is a closed surface., An arch point well inside the egg an old build would have made is on the…, Clay goes on and does not come off, so nothing may ever fill a socket. (+15 more)

### Community 78 - "._selected_landmark"
Cohesion: 0.12
Nodes (7): Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors., Show the landmark group only once there are landmarks to show., The landmark the highlighted row stands for, if the row is one., Which armature the landmark list is pointing into, row or heading., Follow the highlighted landmark, and say which one it is in the view.

### Community 79 - "build_pelvis"
Cohesion: 0.18
Nodes (12): build_pelvis(), plane_through(), The plane through three points, as ``(normal, offset)`` with ``inside`` kept.…, The bucket of the pelvis, with its front corner chipped off. The rim of the…, _marks(), ndarray, test_planes_are_fitted_and_oriented(), test_the_bucket_tapers_from_the_crests_to_the_sitting_bones() (+4 more)

### Community 80 - "Session"
Cohesion: 0.13
Nodes (17): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Path (+9 more)

### Community 81 - "_derived"
Cohesion: 0.09
Nodes (26): The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _derived(), A guess the artist corrects is theirs, and the mirror leaves it alone., The new list is the edit; the old one has to survive to be undone to., Mirroring moves a guess in place, which must not reach the undo history., Which is what keeps a dragged cross and a typed position one behaviour. The…, Hips, then the ribcage, then the head, then the limbs largest first. This order… (+18 more)

### Community 82 - "Bounds"
Cohesion: 0.11
Nodes (19): Bounds, ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc() (+11 more)

### Community 83 - "._build"
Cohesion: 0.27
Nodes (6): QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 84 - "test_forms_panel.py"
Cohesion: 0.23
Nodes (13): _pick(), _place_all(), The Forms panel: the guided run it drives, and the document it writes. The…, A form row hands the whole form to update_enabled, whose landmark list must be…, test_a_one_stage_form_hides_the_slider(), test_back_takes_a_landmark_off_through_the_history(), test_clear_all_ends_the_run_and_undoes_as_one_step(), test_deleting_a_landmark_takes_its_mirrored_guess_with_it() (+5 more)

### Community 85 - "section.py"
Cohesion: 0.24
Nodes (7): Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Which side of the plane survives the cut., SectionAxis, SectionMode

### Community 86 - "shaders.py"
Cohesion: 0.33
Nodes (5): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section()

### Community 87 - "._picker"
Cohesion: 0.13
Nodes (8): Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Apply the drag live, so the clay re-forms under the cursor., Track the form landmark under the cursor; True when it changed., Rub out the stroke points under the eraser, live.

### Community 88 - "ArmaturePanel"
Cohesion: 0.17
Nodes (5): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Take back the landmark before this one and ask for it again., Record an edit the viewport's tool worked out., The multiplier the position boxes are read and written through.

### Community 90 - "wakelock.py"
Cohesion: 0.22
Nodes (7): _Backend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The backend for this machine, or a do-nothing one if it cannot be had., A way of asking one platform to stay awake., Ask for sleep to be held off., Withdraw the request.

### Community 91 - "RemoveItem"
Cohesion: 0.17
Nodes (6): Delete the item at ``index``, putting it back in place on undo., RemoveItem, Record an edited landmark list, mirrored where the mirror is on., Remove the selected landmark, or the whole form when its row is picked., The mirrored landmarks reflected from ``key``, which it anchors., The landmark the highlighted row stands for, if the row is one.

### Community 92 - ".mousePressEvent"
Cohesion: 0.15
Nodes (6): ndarray, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on., Take hold of a form's landmark, to move it or just to say which one it is., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…

### Community 93 - "settings.py"
Cohesion: 0.11
Nodes (15): MatcapSettings, plane_span_deg(), PlaneMode, PlaneTarget, Enum, str, Serialisable description of how the object should be shaded. Every value here…, Material parameters shared by the analytic shading modes. (+7 more)

### Community 94 - "._selected"
Cohesion: 0.14
Nodes (7): Run a row's edit once Qt has finished delivering the current signal. Committing…, Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., Run a bone between the row selected now and the node held before it., Join two nodes of one armature, if they are two and they are one armature., The node the selected row stands for, if the row is a node at all., The armature the selected row stands for, when the row is not a node.

### Community 95 - ".update_enabled"
Cohesion: 0.20
Nodes (5): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., Follow the highlighted landmark, and say which one it is in the view., Highlight the row for a landmark picked in the view.

### Community 96 - "mesh_renderer.py"
Cohesion: 0.24
Nodes (8): bind_default(), current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., Restore a framebuffer captured with :func:`current_framebuffer`., _ghost_depth_range(), OpenGL scene renderer: background, shaded mesh, wireframe, section and paint.…, Sum a see-through model into the ghost buffers, to be resolved after. Blending…, Where the form starts along the view, and how deep it is. The ghost weighs a…

### Community 97 - "plane_count"
Cohesion: 0.12
Nodes (12): _along(), lattice_fineness(), plane_count(), Where a detail setting sits on its slider, 0 to 1., How much finer than usual a detail setting asks the lattice to be. One at the…, How many planes a detail setting asks for. See :attr:`PlaneSettings.axis_count`., How much of a turn in the surface one plane covers, in degrees. Linear in…, How many planes a mode fitted to the model keeps. The climb from two planes to… (+4 more)

### Community 98 - "OverlayParts"
Cohesion: 0.17
Nodes (8): Queue, _Encoder, QObject, Which of the things drawn over the model belong in the frames., The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`., OverlayParts, Which of the things drawn over the model are wanted this time. The viewport…

### Community 99 - "raycast_mesh"
Cohesion: 0.05
Nodes (48): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.… (+40 more)

### Community 100 - ".refresh_list"
Cohesion: 0.25
Nodes (4): QTreeWidgetItem, Rebuild the tree from the store, keeping the landmark being edited shown. Not…, Commit a renamed or re-checked form, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…

### Community 101 - "._sync_scene"
Cohesion: 0.13
Nodes (6): Regenerate the pedestal and the cut contour when their settings move. Both are…, The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on., Cut the mesh with each section plane and expand the result to strokes.

### Community 102 - "Path"
Cohesion: 0.29
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 103 - "CHANGELOG.md"
Cohesion: 0.14
Nodes (14): Shift-snapped orbiting (1.1.0), High Quality shading mode (1.1.0), Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding (+6 more)

### Community 104 - "SetAttributes"
Cohesion: 0.11
Nodes (9): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Record the finished gesture: a move, a resize, or a plain click. A press that…, Record the finished drag as one step, or read a press as a selection., Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…, Record the finished drag as one step, or read a press as a selection. (+1 more)

### Community 105 - "picking.py"
Cohesion: 0.25
Nodes (5): Projection, Enum, str, Projection used by :class:`Camera`., Turning cursor positions into points in the scene. Both interactive tools need…

### Community 106 - "_ScreenSaverBackend"
Cohesion: 0.22
Nodes (4): The freedesktop screensaver service, which hands back a cookie., Hold sleep off, or stop holding it, whichever is not already true., Drop the request, if one is out. Safe to call more than once., _ScreenSaverBackend

### Community 107 - "._place_armature_node"
Cohesion: 0.22
Nodes (4): The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 108 - "._on_bone_toggled"
Cohesion: 0.29
Nodes (4): QListWidgetItem, Catch the selection a click on a checkbox is about to collapse. Qt selects a…, Which bones of the armature the picked-out rows stand for., Take lengths of wire out of the clay, or put them back. A tick on a row that…

### Community 109 - "core/__init__.py"
Cohesion: 0.24
Nodes (8): BoneLabels, Buried, Enum, str, A graph of named points under the form, and the wire it stands for. An armature…, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…, Qt-free geometry, camera and document model for the reference viewer.

### Community 110 - "test_annotation.py"
Cohesion: 0.36
Nodes (8): line_stroke(), Surface annotations: erasing, splitting and the geometry handed to GL., A stroke running along +X, one unit apart, with +Y normals., test_a_closed_stroke_gains_the_wrapping_segment(), test_each_segment_becomes_six_vertices(), test_erasing_keeps_the_brush_and_drops_stubs(), test_erasing_nothing_reports_no_change(), test_erasing_the_middle_splits_a_stroke_in_two()

### Community 111 - ".split"
Cohesion: 0.29
Nodes (5): ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., Normals padded to match the points, so callers can zip them freely., Break the stroke into the runs of points ``keep`` marks as surviving., _runs()

### Community 112 - "coarse_lattice"
Cohesion: 0.33
Nodes (6): app(), coarse_lattice(), fixture, MonkeyPatch, One Qt application for the whole run; offscreen, so CI needs no display.…, Read every model on a small lattice, so the suite stays quick.

### Community 113 - "._start_update_check"
Cohesion: 0.29
Nodes (4): Ask GitHub for the newest release in the background. The startup check is…, QWidget, show_failure_dialog(), show_up_to_date_dialog()

### Community 115 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 116 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 117 - "_WindowsBackend"
Cohesion: 0.25
Nodes (5): ``SetThreadExecutionState``: a flag on this thread, not a handle. The flags…, _WindowsBackend, skipif, The flag the viewer sets is the one Windows reports back afterwards., test_windows_really_sets_the_execution_state()

### Community 118 - "ShadingMode"
Cohesion: 0.18
Nodes (4): Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode, TestEven

### Community 119 - "AddItem"
Cohesion: 0.29
Nodes (3): AddItem, Append an item to a document list., Begin a preset run against a fresh form.

### Community 120 - "._selected_form"
Cohesion: 0.20
Nodes (4): Show a stage of the focused form. A view choice, so not an undo step., Size the stage slider to the focused form, and hide it for a one-stage form., The form the selected row stands for, when the row is a form., The form the stage slider speaks for: the one being guided, else the one picked.

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

### Community 125 - "ring_through"
Cohesion: 0.33
Nodes (6): _periodic_hermite(), A smooth closed curve through ``(angle, value)`` pairs, sampled evenly. Cubic…, A ring in the plane ``(origin, normal)`` passing through ``anchors``. The…, ring_through(), test_a_ring_passes_through_its_anchors_heights_included(), test_a_ring_through_four_axis_points_is_very_nearly_an_ellipse()

### Community 126 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 128 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

### Community 130 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 132 - ".stage_images"
Cohesion: 0.16
Nodes (8): QOpenGLFramebufferObject, QImage, The nodes the model is standing in front of, worked out at most once. A node is…, One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A…, An offscreen target the frames are drawn into, made once per export.…, Draw the scene into ``surface`` and read it back as an image., Lay the overlay -- and the caption, if it was asked for -- on a frame. Painted…

### Community 134 - ".refresh_list"
Cohesion: 0.22
Nodes (5): QTreeWidgetItem, The landmarks in the preset's own order, top of the figure down. Placement…, Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing., Commit a renamed or re-checked row, if anything actually changed.

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `FormTool`, `PlaneSet`, `plane_axes`, `viewport.py`, `PlaneSettings`, `_wires`, `ViewerState`, `FormStore`, `SectionSettings`, `plane_solids.py`, `test_plane_clusters.py`, `plane_volume.py`, `MeshBuffers`, `ExportLook`, `gltf_loader.py`, `._set_geometry`, `plane_clusters.py`, `OrientationSettings`, `Film`, `Solid`, `PrimaryForm`, `test_plane_solids.py`, `convex.py`, `Bounds`, `section.py`, `mesh_renderer.py`, `raycast_mesh`, `picking.py`, `core/__init__.py`, `ShadingMode`?**
  _High betweenness centrality (0.158) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `FormTool`, `.stage_images`, `viewport.py`, `MainWindow`, `._place_form_landmark`, `PlaneSettings`, `ViewerState`, `NavigationController`, `ViewportOverlay`, `film_export.py`, `AnnotateTool`, `ExportLook`, `ExportVideoDialog`, `FilmExport`, `ArmatureTool`, `MeasureTool`, `PrimaryForm`, `._picker`, `.mousePressEvent`, `OverlayParts`, `._sync_scene`, `SetAttributes`, `._place_armature_node`?**
  _High betweenness centrality (0.098) - this node is a cross-community bridge._
- **Why does `Armature` connect `Armature` to `ViewportOverlay`, `PlaneSet`, `ndarray`, `.new_armature`, `viewport.py`, `.refresh_list`, `test_armature.py`, `core/__init__.py`, `._selected_landmark`, `Session`, `_derived`, `form_group`, `armature_tool.py`, `test_planes_panel.py`, `ArmaturePanel`, `ArmatureTool`, `plane_solids.py`, `._selected`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 32 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `Armature` (e.g. with `SculptCache` and `Session`) actually correct?**
  _`Armature` has 2 INFERRED edges - model-reasoned connections that need verification._