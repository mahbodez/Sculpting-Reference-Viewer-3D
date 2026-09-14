# Graph Report - reference-viewer  (2026-09-14)

## Corpus Check
- 123 files · ~417,921 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 3944 nodes · 8864 edges · 142 communities (137 shown, 5 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 406 edges (avg confidence: 0.57)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `72c8e821`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_forms.py
- VideoSettings
- update_check.py
- Viewport
- plane_axes
- settings.py
- MainWindow
- Stroke
- GifWriter
- mesh_renderer.py
- ._draw_scene
- test_plane_film.py
- naming.py
- _wires
- Armature
- README.md
- ViewerState
- SectionPanel
- framebuffer.py
- CameraPanel
- UpdateChecker
- ShaderProgram
- ViewportOverlay
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- NavigationController
- core/__init__.py
- ndarray
- ControlsWindow
- VideoError
- ShadingPanel
- PlaneSet
- test_camera.py
- test_plane_clusters.py
- WakeLock
- plane_volume.py
- _derived
- Frame
- film_export.py
- SurfacePicker
- Camera
- test_armature.py
- ValueSlider
- compute_vertex_normals
- form_group
- open_writer
- _Build
- Agent Graph-First Instructions
- SceneRenderer
- plane_clusters.py
- surface_of
- landmarks.py
- custom.py
- OrientationSettings
- PlaneSettings
- FilmExport
- FormsPanel
- PlanesPanel
- forms.py
- ArmatureTool
- Workspace
- Mesh
- Solid
- clay_lumps
- MeasureTool
- Link
- PrimaryForm
- History
- mesh.py
- AnnotatePanel
- plane_regions
- Release
- Measurement
- PlaneAxes
- Texture2D
- application.py
- test_custom_panels.py
- ArmaturePanel
- Coefficients
- session.py
- Wires
- Bounds
- symbol_button
- test_forms_panel.py
- TriangleIndex
- stl_loader.py
- ._picker
- .new_armature
- PointEdit
- FrameBar
- load_obj
- .mousePressEvent
- test_elements.py
- PlaneMode
- FormRun
- ReflowLayout
- .split_point
- _Encoder
- picking.py
- clone.py
- ._sync_scene
- .dropEvent
- .film_changed
- .mouseReleaseEvent
- test_panel_docks.py
- ._place_armature_node
- test_mesh_io.py
- viewport.py
- DockTitle
- test_reflow.py
- ball
- build_form
- ArmatureStore
- plane_solids.py
- .update_enabled
- Reflow
- ShadingMode
- SetAttributes
- ._draw_hud
- release.yml
- plane_axes.py
- wakelock.py
- BoneLabels
- _ScreenSaverBackend
- ndarray
- ExportLook
- ._place_form_landmark
- .refresh_list
- .column_of
- theme.py
- _height_of
- ._commit_node_drag
- section
- _WindowsBackend
- _MacBackend
- WholeFaceToggles
- app
- test_plane_solids.py
- refview/__init__.py
- .with_landmark_at
- ._buried_nodes

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 143 edges
2. `Viewport` - 101 edges
3. `PrimaryForm` - 78 edges
4. `Camera` - 75 edges
5. `Armature` - 73 edges
6. `MainWindow` - 68 edges
7. `PlaneSettings` - 67 edges
8. `ViewerState` - 67 edges
9. `FormsPanel` - 63 edges
10. `ArmaturePanel` - 62 edges

## Surprising Connections (you probably didn't know these)
- `Pedestal (1.1.0)` --rationale_for--> `PedestalSettings`  [EXTRACTED]
  CHANGELOG.md → src/refview/core/pedestal.py
- `The cut interior is flooded flat` --rationale_for--> `SceneRenderer`  [INFERRED]
  README.md → src/refview/render/mesh_renderer.py
- `Orthographic extent derived from FOV and distance` --rationale_for--> `Camera`  [EXTRACTED]
  README.md → src/refview/core/camera.py
- `Every document edit is a command` --rationale_for--> `SetAttributes`  [EXTRACTED]
  README.md → src/refview/core/commands.py
- `Every document edit is a command` --rationale_for--> `AddItem`  [EXTRACTED]
  README.md → src/refview/core/commands.py

## Import Cycles
- 3-file cycle: `src/refview/ui/elements/__init__.py -> src/refview/ui/elements/clone.py -> src/refview/ui/elements/slider.py -> src/refview/ui/elements/__init__.py`
- 4-file cycle: `src/refview/ui/elements/__init__.py -> src/refview/ui/elements/custom.py -> src/refview/ui/elements/clone.py -> src/refview/ui/elements/slider.py -> src/refview/ui/elements/__init__.py`

## Hyperedges (group relationships)
- **The bundled matcap set** — resources_matcaps_clay_terracotta_matcap, resources_matcaps_charcoal_matcap, resources_matcaps_jade_matcap, resources_matcaps_steel_matcap, resources_matcaps_studio_white_matcap, resources_matcaps_wax_skin_matcap, tools_generate_matcaps_matcappreset, tools_generate_matcaps_render [INFERRED 0.85]
- **The four generic undo commands** — src_refview_core_commands_setattributes, src_refview_core_commands_additem, src_refview_core_commands_removeitem, src_refview_core_commands_replaceitems, src_refview_core_history_command, readme_every_edit_is_a_command [EXTRACTED 1.00]
- **Windows binary-compatibility decisions** — readme_pyside6_pinned_below_68, environment_pip_installed_binaries, environment_python_311, github_workflows_release_pyinstaller_build [INFERRED 0.75]

## Communities (142 total, 5 thin omitted)

### Community 0 - "test_forms.py"
Cohesion: 0.06
Nodes (47): A graph of named points under the form, and the wire it stands for. An armature…, The hull of the points with its faces bowed out; see :func:`rounded_hull`., median_plane_ready(), mirror_form_landmarks(), The midline landmarks, which are what the median plane is fitted to., The landmark list with every paired landmark reflected into place. The…, Whether enough of the midline is down for the mirror to have a plane., median_plane() (+39 more)

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

### Community 5 - "settings.py"
Cohesion: 0.04
Nodes (57): QIcon, _along(), lattice_fineness(), plane_count(), plane_span_deg(), Serialisable description of how the object should be shaded. Every value here…, Where a detail setting sits on its slider, 0 to 1., How much finer than usual a detail setting asks the lattice to be. One at the… (+49 more)

### Community 6 - "MainWindow"
Cohesion: 0.06
Nodes (17): QAction, MainWindow, QMainWindow, Wires the viewport, the panels and the document together., Give each panel a dock of its own, tabbed together on the right. Ten docks…, Keep every dock's switch agreeing with the panel it speaks for., Which panels are open, and the panels the artist builds. Rebuilt every time it…, Add a menu entry, optionally with a window-wide shortcut. (+9 more)

### Community 7 - "Stroke"
Cohesion: 0.07
Nodes (34): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+26 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "mesh_renderer.py"
Cohesion: 0.09
Nodes (34): Named camera positions the artist can jump between while sculpting., Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., look_at(), normalize() (+26 more)

### Community 10 - "._draw_scene"
Cohesion: 0.11
Nodes (17): normal_matrix(), ndarray, The model's own planes under ``mode``, fitted once and kept., Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.…, How see-through the model is this frame, or ``None`` if it is solid. Asked in…, The model, the pedestal under it and the flat cap over the cut., Point the shading pass at the shadow map and the occlusion buffer. (+9 more)

### Community 11 - "test_plane_film.py"
Cohesion: 0.06
Nodes (41): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, coarse_lattice(), film_of(), fixture, MonkeyPatch, parametrize, Scrubbing through the making of a form, rather than only arriving at it. The… (+33 more)

### Community 12 - "naming.py"
Cohesion: 0.13
Nodes (25): _clone_slider(), _asked(), caption_for(), element_id(), _free(), _from_id(), lookup(), name_tree() (+17 more)

### Community 13 - "_wires"
Cohesion: 0.12
Nodes (31): The order the artist put the bones in is what the scrub walks through, which is…, The claim the whole film rests on, asked again with an armature under it: an…, test_a_film_of_clay_on_a_wire_lays_it_down_in_the_order_it_was_listed(), test_the_last_stage_of_a_film_on_a_wire_is_the_form_the_slider_gives(), _bar(), _bed_for(), _holds(), A long ellipsoid: one closed form with an obvious axis to lie along. (+23 more)

### Community 14 - "Armature"
Cohesion: 0.05
Nodes (38): Armature, ArmatureNode, Bone, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves., A plausible thickness for a node placed by hand. (+30 more)

### Community 15 - "README.md"
Cohesion: 0.14
Nodes (18): High Quality shading mode (1.1.0), numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, Annotations drawn as widened geometry, core never imports Qt, Every document edit is a command (+10 more)

### Community 16 - "ViewerState"
Cohesion: 0.09
Nodes (19): ndarray, Path, QObject, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements, annotations,… (+11 more)

### Community 17 - "SectionPanel"
Cohesion: 0.16
Nodes (7): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 18 - "framebuffer.py"
Cohesion: 0.07
Nodes (20): AccumTarget, bind_default(), ColorTarget, current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality and ghost passes. Four of…, A single-channel colour framebuffer, used for the occlusion buffers. (+12 more)

### Community 19 - "CameraPanel"
Cohesion: 0.12
Nodes (7): CameraPanel, QListWidgetItem, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 21 - "ShaderProgram"
Cohesion: 0.12
Nodes (9): OpenGL rendering layer: shader programs, textures and the scene renderer., ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError (+1 more)

### Community 22 - "ViewportOverlay"
Cohesion: 0.16
Nodes (19): QPointF, project_visible(), Handle, QColor, QPainter, Draws measurements, tool previews, the orientation gizmo and the readout., A line laid over its own dark outline, so it reads against anything., An unfilled circle: how thick the form is here, not how big a dot is. (+11 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.07
Nodes (25): app(), _names(), panel(), fixture, The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as… (+17 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.10
Nodes (11): MeasurePanel, _NameOnlyDelegate, QStyledItemDelegate, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing… (+3 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.13
Nodes (7): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., test_bookmarks_cycle_and_wrap()

### Community 26 - "NavigationController"
Cohesion: 0.10
Nodes (22): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+14 more)

### Community 27 - "core/__init__.py"
Cohesion: 0.07
Nodes (37): The cut interior is flooded flat, Qt-free geometry, camera and document model for the reference viewer., Enum, ndarray, str, Cutting the model open with planes. A section is described by one plane -- an…, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled. (+29 more)

### Community 28 - "ndarray"
Cohesion: 0.08
Nodes (38): block_bounds(), block_field(), block_labels(), block_splits(), blocks(), carve(), coarse_bounds(), _corner_facings() (+30 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "VideoError"
Cohesion: 0.09
Nodes (19): _encode_arguments(), _encoders(), _FFmpegWriter, _no_window(), ndarray, RuntimeError, An export that could not be written, said in words for the artist., Which encoders this ffmpeg was built with. Asked once, because a build without… (+11 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.20
Nodes (7): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel

### Community 32 - "PlaneSet"
Cohesion: 0.09
Nodes (19): QThread, PlaneSet, One level of a fit: the planes the shader is to quantise against. A plane is a…, Film, A whole making, from the coarsest stage to the one the slider asks for. Held by…, FilmRecorder, QObject, Recording a form's making in the background, so the app stays usable. A film is… (+11 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (8): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_serialisation_round_trip(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.07
Nodes (44): angle_deg(), cube(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What…, How far the least well served of ``wanted`` is from anything offered., The one form whose planes are not a matter of opinion. (+36 more)

### Community 35 - "WakeLock"
Cohesion: 0.17
Nodes (13): Holds sleep off while the window that owns it is the one in front. The class…, WakeLock, Broken, The wake lock: it must ask once, drop once, and never take the viewer down., A backend that writes down what it was asked to do., A platform that refuses, the way an old or locked-down one might., The viewer must open and close normally on a machine that says no., Recorder (+5 more)

### Community 36 - "plane_volume.py"
Cohesion: 0.10
Nodes (29): _axes(), _balloon(), close_gaps(), encloses(), lattice(), lay_bed(), nearest_surface(), outside_points() (+21 more)

### Community 37 - "_derived"
Cohesion: 0.10
Nodes (24): _kept_laying(), Fresh bones, laid the way the armature was already laying them. The bone list…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _derived(), A guess the artist corrects is theirs, and the mirror leaves it alone., The new list is the edit; the old one has to survive to be undone to., Hips, then the ribcage, then the head, then the limbs largest first. This order… (+16 more)

### Community 38 - "Frame"
Cohesion: 0.08
Nodes (17): carried(), _push_frame(), Nothing: each row inside the copy is linked on its own., Read a drag's payload back, or ``None`` if it is not one of ours., CustomPanel, Move a copy already in a panel to a new place in this one. ``frame`` and…, The group under a point in the panel, if there is one., Which row of a group a drop at ``point`` should become. (+9 more)

### Community 39 - "film_export.py"
Cohesion: 0.07
Nodes (21): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+13 more)

### Community 40 - "SurfacePicker"
Cohesion: 0.06
Nodes (28): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+20 more)

### Community 41 - "Camera"
Cohesion: 0.07
Nodes (19): Orthographic extent derived from FOV and distance, Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults… (+11 more)

### Community 42 - "test_armature.py"
Cohesion: 0.07
Nodes (56): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _chain(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other., The femoral head is in from the ASIS, below it and behind it, by shares of the… (+48 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (11): _pull_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end., Set the value the way a hand on the control would., The value the track stands at ``x`` pixels across. (+3 more)

### Community 44 - "compute_vertex_normals"
Cohesion: 0.13
Nodes (26): _accessor(), _buffers(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry(), _primitives(), ndarray (+18 more)

### Community 45 - "form_group"
Cohesion: 0.11
Nodes (15): QDialog, QProgressDialog, even(), ExportVideoDialog, Path, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+7 more)

### Community 46 - "open_writer"
Cohesion: 0.13
Nodes (16): ffmpeg_path(), open_writer(), Path, Where ffmpeg is, or ``None``. Looked for in the order of how deliberate each…, Why ``format`` cannot be written here, or ``None`` if it can., Start an encoder for ``settings``, or say why there cannot be one., unavailable(), frames() (+8 more)

### Community 47 - "_Build"
Cohesion: 0.21
Nodes (14): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _mid(), ndarray, Somewhere to collect nodes while the rules that need each other run. (+6 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "SceneRenderer"
Cohesion: 0.07
Nodes (19): _ghost_depth_range(), MeshBuffers, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are…, Whichever geometry is standing for the model this frame., Fill the shader's table with a level, if it is not already in it. (+11 more)

### Community 50 - "plane_clusters.py"
Cohesion: 0.09
Nodes (29): _compact(), _consensus(), _cut(), _first_planes(), _fit(), _leaves(), Patches, plane_flats() (+21 more)

### Community 51 - "surface_of"
Cohesion: 0.11
Nodes (19): _back_inside(), Bed, dual_contour(), The surface where ``value`` changes sign, one vertex per lattice cell. Each…, The gradient of a lattice field, by central differences. Which is the direction…, Drop the loose pieces, keeping the form and anything of its size. A block is a…, Read lattice fields at places between their corners, straight-line. Nearest-…, Put anything that has drifted out of the model back onto its surface. One… (+11 more)

### Community 52 - "landmarks.py"
Cohesion: 0.09
Nodes (21): _humanoid_landmarks(), mirror_landmarks(), mirror_point(), _node_name(), Preset, Enum, Guided presets: the anatomy an artist points at, and the joints it implies. A…, An ordered set of landmarks and the armature they build. (+13 more)

### Community 53 - "custom.py"
Cohesion: 0.13
Nodes (15): Make every control under ``root`` that can be copied Alt-draggable. A group is…, watch_tree(), _detach(), QFormLayout, QWidget, A panel the artist builds, out of copies of controls from the fixed ones. The…, Take a copy out of this panel and destroy it., Whether a control already says what it is, so needs no caption. Three do. A… (+7 more)

### Community 54 - "OrientationSettings"
Cohesion: 0.09
Nodes (24): OrientationSettings, Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., UpAxis (+16 more)

### Community 55 - "PlaneSettings"
Cohesion: 0.05
Nodes (36): Holds the working state between one turn of the sliders and the next.…, Drop everything held, so the next call starts from the fit., The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache, PlaneSettings, Discretisation of the shading normals into the planes of the form. A sculptor…, How much of a turn in the surface one plane covers, in degrees. Linear in… (+28 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (12): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+4 more)

### Community 57 - "FormsPanel"
Cohesion: 0.04
Nodes (35): FormsPanel, QPushButton, QTreeWidgetItem, QWidget, A strip of buttons that one form row can show or hide as a unit., Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle. (+27 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.09
Nodes (20): PlanesPanel, QListWidgetItem, Lay one length of wire earlier or later, as one undoable step., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Show what this way of working needs, and put the rest away. A setting that does…, The line under the normals slider: what the setting has asked for., The line under the geometry slider: how the form is being worked. ``wires`` is… (+12 more)

### Community 59 - "forms.py"
Cohesion: 0.07
Nodes (42): build_freeform(), _centre(), form_landmark_title(), form_spec(), FormFill, FormPreset, FormStage, freeform_landmark() (+34 more)

### Community 60 - "ArmatureTool"
Cohesion: 0.06
Nodes (39): LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, Handle, Begin a preset run against an armature already in the store., The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now. (+31 more)

### Community 61 - "Workspace"
Cohesion: 0.05
Nodes (30): QDockWidget, QScrollArea, QSettings, QTabBar, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top., forget(), Drop every id under a prefix; for a panel that has been thrown away. (+22 more)

### Community 62 - "Mesh"
Cohesion: 0.14
Nodes (13): Mesh, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, flatness(), neighbour_agreement(), How nearly each vertex faces the way its neighbours do, as a cosine. One along…, How much each vertex's opinion of its plane is worth, 0 to 1., Thin the model down to a design matrix, or say it has nothing to give. (+5 more)

### Community 63 - "Solid"
Cohesion: 0.06
Nodes (64): convex_hull(), DegenerateHullError, flat_mesh(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, The outward unit normal at each vertex: the area-weighted mean of its faces'. A… (+56 more)

### Community 64 - "clay_lumps"
Cohesion: 0.16
Nodes (18): _box_facings(), clay_lumps(), clay_pieces(), fit_piece(), _frame(), grow_piece(), join_pieces(), Which three ways a lump of material runs. Columns, thinnest first. Thinnest… (+10 more)

### Community 65 - "MeasureTool"
Cohesion: 0.15
Nodes (7): Which of the things drawn over the model belong in the frames., MeasureTool, Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview., OverlayParts, Which of the things drawn over the model are wanted this time. The viewport…

### Community 66 - "Link"
Cohesion: 0.11
Nodes (10): CloneGesture, Link, _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original., Whether the copy is being used right now and must not be written. (+2 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.05
Nodes (43): FormLandmarkRef, PlacedLandmark, One anatomical point the artist put on the model during a guided run., FormSettings, FormStore, PrimaryForm, Point3, One form in the document: which recipe, and where its landmarks are. The solids… (+35 more)

### Community 68 - "History"
Cohesion: 0.06
Nodes (27): Camera motion is deliberately not undoable, AddItem, Append an item to a document list., Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems, Command (+19 more)

### Community 69 - "mesh.py"
Cohesion: 0.08
Nodes (32): Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL and glTF import (1.1.0), Units are adopted, never guessed, _gathered() (+24 more)

### Community 70 - "AnnotatePanel"
Cohesion: 0.19
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 71 - "plane_regions"
Cohesion: 0.08
Nodes (44): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), dumbbell(), flatness(), parametrize, The invariant an artist actually sees, on the finished stand-in: clay is added… (+36 more)

### Community 72 - "Release"
Cohesion: 0.18
Nodes (12): The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, is_skipped(), QWidget, Background release check and the notice it puts in front of the artist. The…, Whether the artist already dismissed this exact version., Offer the release page, with the option never to be asked again. (+4 more)

### Community 73 - "Measurement"
Cohesion: 0.12
Nodes (10): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+2 more)

### Community 74 - "PlaneAxes"
Cohesion: 0.22
Nodes (5): PlaneAxes, The planes a model falls into, at every count. Built once per mesh and per…, The best ``count`` planes, or as many as the model supports. A model whose…, fit_planes(), The planes of ``mesh`` under ``mode``; empty where the mode needs none.

### Community 75 - "Texture2D"
Cohesion: 0.13
Nodes (7): DataTexture, ndarray, Matcap texture loading and upload, and the small data table beside it., An RGBA8 2D texture with clamped edges and mipmapped minification., A small RGBA32F table the shader reads exact values out of. Not a picture:…, Store an ``(h, w, 4)`` float array, reallocating only when resized., Texture2D

### Community 76 - "application.py"
Cohesion: 0.05
Nodes (56): ArgumentParser, Color, Namespace, QSplashScreen, REFVIEW_RESOURCES resource override, Charcoal matcap, Terracotta clay matcap, Jade matcap (+48 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.07
Nodes (23): QMimeData, app(), custom(), _drop_on(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error., A group is not a row, so it goes ahead of the group it was dropped on. (+15 more)

### Community 78 - "ArmaturePanel"
Cohesion: 0.09
Nodes (11): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Take back the landmark before this one and ask for it again., Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors., The multiplier the position boxes are read and written through., Show the landmark group only once there are landmarks to show. (+3 more)

### Community 79 - "Coefficients"
Cohesion: 0.13
Nodes (14): Coefficients, What each block of the design matrix counts for, against the normals. A fit…, Whether anything but the normals is being read at all., The design-matrix settings, in the form the fitters want them., lumpy(), A form with real planes in it, and more than one facing the same way., How many planes have another plane pointing very nearly where they do., The coefficients have to reach the fit, and reaching it has to show. Two planes… (+6 more)

### Community 80 - "session.py"
Cohesion: 0.08
Nodes (29): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., Path (+21 more)

### Community 81 - "Wires"
Cohesion: 0.18
Nodes (8): kept_off(), An armature, as the clay reads it: where each length of wire runs. The order…, How many lumps the wire itself asks for., What a cache has to compare to know the wire has not moved., Which points lie in the sleeve a length of wire declares round itself. The wire…, Which material lies under a length of wire that is to take no clay. Turning a…, Wires, within_sleeve()

### Community 82 - "Bounds"
Cohesion: 0.11
Nodes (19): Bounds, ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc() (+11 more)

### Community 83 - "symbol_button"
Cohesion: 0.21
Nodes (9): QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row(), QPushButton, A button that carries a drawing instead of a word. For the few actions that… (+1 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.11
Nodes (30): app(), _click(), panel(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The… (+22 more)

### Community 85 - "TriangleIndex"
Cohesion: 0.14
Nodes (14): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., Build the index from expanded triangle corners, shape ``(T, 3, 3)``. (+6 more)

### Community 86 - "stl_loader.py"
Cohesion: 0.20
Nodes (14): STL corner welding, _ascii_corners(), _binary_corners(), load_stl(), ndarray, Path, Binary and ASCII STL reader. STL stores three loose corners per facet and…, Raised when a file cannot be interpreted as an STL mesh. (+6 more)

### Community 87 - "._picker"
Cohesion: 0.17
Nodes (5): Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Apply the drag live, so the clay re-forms under the cursor., Rub out the stroke points under the eraser, live.

### Community 89 - "PointEdit"
Cohesion: 0.13
Nodes (10): _clone_point(), _pull_point(), _push_point(), _AxisBox, PointEdit, QDoubleSpinBox, QWidget, Three boxes for one point in space. Keyboard tracking is off, so a typed number… (+2 more)

### Community 90 - "FrameBar"
Cohesion: 0.09
Nodes (13): FrameBar, framed(), QFormLayout, QPainter, QSize, QWidget, The mark beside a group's name: filled when open, a ring when shut. It is the…, The rows inside the frame. ``layout()`` is the frame's own, which stacks the… (+5 more)

### Community 91 - "load_obj"
Cohesion: 0.24
Nodes (13): _load_generic(), load_obj(), Path, Line-by-line reader for files the fast path declines., Load ``path`` and return a :class:`~refview.core.mesh.Mesh`. Faces with more…, _push_slider(), OBJ parsing: normals, triangulation and index handling., test_empty_file_is_rejected() (+5 more)

### Community 92 - ".mousePressEvent"
Cohesion: 0.15
Nodes (6): ndarray, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on., Take hold of a form's landmark, to move it or just to say which one it is., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…

### Community 93 - "test_elements.py"
Cohesion: 0.08
Nodes (19): Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., A matcap has no light to aim, so the Light group goes -- and its space. The…, Run the refresh the shared timer would have run., ``self._mode`` is ``mode``; the group called Mode settles for a number. (+11 more)

### Community 94 - "PlaneMode"
Cohesion: 0.17
Nodes (8): PlaneMode, PlaneTarget, Enum, str, What the planes filter is allowed to act on. The two are mutually exclusive…, How the plane directions are arrived at. ``shader_id`` must stay in sync with…, Whether the directions are read off the model rather than imposed., Whether the mode reads the design matrix, and so its coefficients. Grid reads…

### Community 95 - "FormRun"
Cohesion: 0.40
Nodes (3): FormRun, Begin a run against a form already in the store., A guided form part-way through.

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - ".split_point"
Cohesion: 0.20
Nodes (9): BoneRef, _project(), The nearest bone under the cursor, for showing its length., Where on a bone a click at ``(x, y)`` landed. The share along the bone is read…, A world point in widget pixels, or ``None`` when it is behind the camera., How far along a screen-space segment the cursor's nearest point lies., Pixels from the cursor to the segment, or ``None`` if either end is behind., _segment_distance() (+1 more)

### Community 98 - "_Encoder"
Cohesion: 0.25
Nodes (5): Queue, _Encoder, QObject, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 99 - "picking.py"
Cohesion: 0.09
Nodes (31): Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``. (+23 more)

### Community 100 - "clone.py"
Cohesion: 0.04
Nodes (73): QAbstractButton, QComboBox, QLineEdit, QSlider, QSpinBox, _begin(), can_clone(), clone() (+65 more)

### Community 101 - "._sync_scene"
Cohesion: 0.12
Nodes (6): Regenerate the pedestal and the cut contour when their settings move. Both are…, The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on., Cut the mesh with each section plane and expand the result to strokes.

### Community 102 - ".dropEvent"
Cohesion: 0.12
Nodes (7): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window., Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model., Take a copied control out of whichever hand-built panel holds it.

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.16
Nodes (6): Record the finished drag as one step, or read a press as a selection., Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Record the finished drag as one step, or read a press as a selection., Track the form landmark under the cursor; True when it changed., Record the finished drag as a single undo step.

### Community 105 - "test_panel_docks.py"
Cohesion: 0.05
Nodes (39): app(), _drag_over(), _middle_of_the_view(), fixture, parametrize, Each panel in a dock of its own, and putting the docks back next time. Two…, A drag of ``holder`` arriving at ``point`` in the window's coordinates. A real…, The gesture the whole thing rests on: drag it onto the model, it goes. (+31 more)

### Community 107 - "._place_armature_node"
Cohesion: 0.22
Nodes (4): The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 108 - "test_mesh_io.py"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

### Community 109 - "viewport.py"
Cohesion: 0.10
Nodes (22): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, What the annotate tool does with a drag. The first three describe the shape a…, The handful of undoable edits the whole application is built from.…, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, MeasurementSettings (+14 more)

### Community 110 - "DockTitle"
Cohesion: 0.09
Nodes (14): QToolButton, DockTitle, make_switch(), QCheckBox, QSize, QWidget, One dock per panel, with a bar of its own across the top. Every panel is its…, Put a show/hide switch at the left of the bar and return it. (+6 more)

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - "ball"
Cohesion: 0.11
Nodes (28): app(), coarse_lattice(), fixture, MonkeyPatch, Recording a film on a thread, without taking the process down with it. The rest…, Which is what the panel puts its controls to sleep by, so it has to be true…, Shutdown must not care whether the thread beat it to the exit. A recording that…, The guard that decides whether to scrub an existing film or record a new one.… (+20 more)

### Community 113 - "build_form"
Cohesion: 0.09
Nodes (36): merged(), Several flat meshes as one, or ``None`` when there is nothing to draw., build_form(), built_count(), form_mesh(), landmark_signature(), ndarray, The landmarks as a mapping a builder can read. (+28 more)

### Community 114 - "ArmatureStore"
Cohesion: 0.18
Nodes (4): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 115 - "plane_solids.py"
Cohesion: 0.12
Nodes (25): planes_for(), The stages a form passes through on its way from a block to a figure. The…, How many solids each stage of a film is made of. Every count from the coarsest…, The detail setting that asks for ``solids``, or ``None`` if none does. The…, Work the form stage by stage, handing each one back as it is finished. A…, record(), stage_counts(), block_count() (+17 more)

### Community 116 - ".update_enabled"
Cohesion: 0.10
Nodes (11): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., Run a bone between the row selected now and the node held before it., Take off the panel whatever does not apply right now., The node the selected row stands for, if the row is a node at all., The armature the selected row stands for, when the row is not a node. (+3 more)

### Community 117 - "Reflow"
Cohesion: 0.30
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 118 - "ShadingMode"
Cohesion: 0.18
Nodes (4): Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode, TestEven

### Community 119 - "SetAttributes"
Cohesion: 0.14
Nodes (8): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, QTreeWidgetItem, Run a row's edit once Qt has finished delivering the current signal. Committing…, Record an edit the viewport's tool worked out., Join two nodes of one armature, if they are two and they are one armature., Commit a renamed or re-checked row, if anything actually changed.

### Community 120 - "._draw_hud"
Cohesion: 0.24
Nodes (5): QFont, Burn a line into the bottom of a frame, for an exported clip. Which stage of…, What the forms tool is waiting for, said in as few lines as it takes., Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, What the armature tool is waiting for, said in as few lines as it takes.

### Community 121 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 122 - "plane_axes.py"
Cohesion: 0.13
Nodes (15): _empty(), ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, A level with no place in it: nearest direction wins, as before., How much surface each vertex stands for: a third of each triangle on it.…, The plane direction of a group, its spread, and its total weight., Cut a group across its first principal component, or refuse to., _split() (+7 more)

### Community 125 - "wakelock.py"
Cohesion: 0.22
Nodes (7): _Backend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The backend for this machine, or a do-nothing one if it cannot be had., A way of asking one platform to stay awake., Ask for sleep to be held off., Withdraw the request.

### Community 127 - "BoneLabels"
Cohesion: 0.29
Nodes (6): BoneLabels, Buried, Enum, str, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…

### Community 128 - "_ScreenSaverBackend"
Cohesion: 0.22
Nodes (4): The freedesktop screensaver service, which hands back a cookie., Hold sleep off, or stop holding it, whichever is not already true., Drop the request, if one is out. Safe to call more than once., _ScreenSaverBackend

### Community 130 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 132 - "ExportLook"
Cohesion: 0.10
Nodes (17): QOpenGLFramebufferObject, The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, ExportLook, What the frames are to look like, as against what they are of. Laid over the…, ``base`` with this export's choices laid over it. (+9 more)

### Community 134 - ".refresh_list"
Cohesion: 0.29
Nodes (3): The landmarks in the preset's own order, top of the figure down. Placement…, Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing.

### Community 135 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 136 - "theme.py"
Cohesion: 0.25
Nodes (8): css(), outline(), QColor, Draw the hairline that separates a control from the panel. One line, the same…, A colour as a style sheet function, for the parts Qt draws., A dark theme, so the viewport is what draws the eye. The colours themselves…, The style sheet, written out of the palette so the two cannot disagree., _stylesheet()

### Community 138 - "_height_of"
Cohesion: 0.40
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 139 - "._commit_node_drag"
Cohesion: 0.33
Nodes (3): Record the finished gesture: a move, a resize, or a plain click. A press that…, Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…

### Community 144 - "section"
Cohesion: 0.50
Nodes (4): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., section()

### Community 147 - "_WindowsBackend"
Cohesion: 0.25
Nodes (5): ``SetThreadExecutionState``: a flag on this thread, not a handle. The flags…, _WindowsBackend, skipif, The flag the viewer sets is the one Windows reports back afterwards., test_windows_really_sets_the_execution_state()

### Community 148 - "_MacBackend"
Cohesion: 0.33
Nodes (3): c_void_p, _MacBackend, An IOKit power assertion, held by id until it is released.

### Community 149 - "WholeFaceToggles"
Cohesion: 0.14
Nodes (10): QApplication, QObject, Making the whole of a switch the part you can press. The theme turns every…, Turns a press anywhere on a switch into a click on it., Put the rule in place for every switch in the application., WholeFaceToggles, The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter. (+2 more)

### Community 151 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 152 - "test_plane_solids.py"
Cohesion: 0.05
Nodes (42): ndarray, Points spread over the model closely enough for a lattice to feel it. The…, surface_seeds(), block(), box(), coarse_lattice(), fixture, MonkeyPatch (+34 more)

### Community 153 - "refview/__init__.py"
Cohesion: 0.50
Nodes (3): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version()

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `VideoSettings`, `plane_axes`, `ExportLook`, `mesh_renderer.py`, `test_plane_film.py`, `_wires`, `README.md`, `ViewerState`, `test_plane_solids.py`, `core/__init__.py`, `ndarray`, `PlaneSet`, `test_plane_clusters.py`, `plane_volume.py`, `compute_vertex_normals`, `SceneRenderer`, `plane_clusters.py`, `surface_of`, `OrientationSettings`, `PlaneSettings`, `FilmExport`, `forms.py`, `Solid`, `PrimaryForm`, `mesh.py`, `plane_regions`, `PlaneAxes`, `Coefficients`, `Wires`, `Bounds`, `TriangleIndex`, `stl_loader.py`, `load_obj`, `picking.py`, `test_mesh_io.py`, `viewport.py`, `ball`, `build_form`, `plane_solids.py`, `ShadingMode`, `plane_axes.py`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `ExportLook`, `._place_form_landmark`, `MainWindow`, `._commit_node_drag`, `ViewerState`, `ViewportOverlay`, `NavigationController`, `._buried_nodes`, `PlaneSet`, `film_export.py`, `SurfacePicker`, `form_group`, `FilmExport`, `ArmatureTool`, `MeasureTool`, `PrimaryForm`, `._picker`, `.mousePressEvent`, `_Encoder`, `._sync_scene`, `.mouseReleaseEvent`, `._place_armature_node`, `viewport.py`, `build_form`?**
  _High betweenness centrality (0.075) - this node is a cross-community bridge._
- **Why does `Armature` connect `Armature` to `test_forms.py`, `ndarray`, `settings.py`, `.refresh_list`, `ViewportOverlay`, `test_planes_panel.py`, `core/__init__.py`, `.with_landmark_at`, `_derived`, `test_armature.py`, `landmarks.py`, `PlaneSettings`, `ArmatureTool`, `ArmaturePanel`, `session.py`, `.new_armature`, `.split_point`, `viewport.py`, `ArmatureStore`, `plane_solids.py`, `.update_enabled`, `._draw_hud`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 15 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PrimaryForm` (e.g. with `PlacedLandmark` and `DegenerateHullError`) actually correct?**
  _`PrimaryForm` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._