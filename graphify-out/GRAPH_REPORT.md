# Graph Report - reference-viewer  (2026-09-06)

## Corpus Check
- 79 files · ~224,075 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1604 nodes · 3465 edges · 73 communities (72 shown, 1 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 176 edges (avg confidence: 0.62)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `97a593ec`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Stroke
- application.py
- main_window.py
- Viewport Widget
- plane_axes
- AnnotateTool
- MainWindow
- ViewerState
- Mesh
- Bounds
- RenderSettings
- Camera
- camera.py
- OrientationSettings
- SceneRenderer
- README.md
- gltf_loader.py
- form_group
- mesh_renderer.py
- CameraPanel
- _morton_order
- ShaderProgram
- plane_axes.py
- render/__init__.py
- MeasurePanel
- BookmarkStore
- NavigationController
- History
- SliderSpin
- mesh_io.py
- Measurement
- ShadingPanel
- test_mesh_io.py
- test_camera.py
- test_plane_clusters.py
- WakeLock
- ndarray
- AddItem
- release_from_payload
- SectionSettings
- SectionPanel
- Snapped Orbit Tests
- section.py
- state.py
- UpdateChecker
- test_session.py
- TriangleIndex
- load_matcap_pixels
- Agent Graph-First Instructions
- matcap_panel.py
- Panel
- Screen-to-World Panning
- MatcapPanel
- AnnotatePanel
- viewport.py
- Path
- settings.py
- plane_clusters.py
- annotation.py
- obj_loader.py
- measure_panel.py
- RemoveItem
- ColorButton
- SetAttributes
- generate_matcaps.py
- .drag_target
- .point
- lock_icon
- _NameOnlyDelegate
- vertex_weights
- Projection
- PlanesPanel
- scrollable

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 84 edges
2. `Camera` - 71 edges
3. `Viewport` - 47 edges
4. `MainWindow` - 46 edges
5. `ViewerState` - 46 edges
6. `SceneRenderer` - 40 edges
7. `Stroke` - 33 edges
8. `Measurement` - 30 edges
9. `Panel` - 29 edges
10. `AnnotateTool` - 27 edges

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

## Communities (73 total, 1 thin omitted)

### Community 0 - "Stroke"
Cohesion: 0.06
Nodes (38): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+30 more)

### Community 1 - "application.py"
Cohesion: 0.12
Nodes (21): ArgumentParser, Namespace, QApplication, QPixmap, QSplashScreen, _apply_startup_arguments(), build_parser(), _create_splash() (+13 more)

### Community 2 - "main_window.py"
Cohesion: 0.13
Nodes (23): check_for_update(), fetch_latest_release(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed)., The newest published release, as GitHub describes it., Return the newest published release, or raise :class:`UpdateCheckError`., The newest release when it is later than ``current_version``, else ``None``. (+15 more)

### Community 3 - "Viewport Widget"
Cohesion: 0.07
Nodes (15): QOpenGLWidget, ndarray, Regenerate the pedestal and the cut contour when their settings move. Both are…, Cut the mesh with each section plane and expand the result to strokes., Free every GL object while the owning context is still current., Drop whatever gesture is half-finished, without disarming the tool., Record the finished drag as a single undo step., Rub out the stroke points under the eraser, live. (+7 more)

### Community 4 - "plane_axes"
Cohesion: 0.12
Nodes (27): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+19 more)

### Community 5 - "AnnotateTool"
Cohesion: 0.11
Nodes (17): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Painting annotations onto the model surface. Every shape is laid down the same…, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses. (+9 more)

### Community 6 - "MainWindow"
Cohesion: 0.08
Nodes (11): QAction, QMainWindow, MainWindow, Wires the viewport, the panels and the document together., Add a menu entry, optionally with a window-wide shortcut., Single-key shortcuts, scoped so they never eat text input. They only fire while…, Keep the menu entry agreeing with the panel's own checkbox., Keep the panel button and the menu entry agreeing with the tool. (+3 more)

### Community 7 - "ViewerState"
Cohesion: 0.06
Nodes (34): QColor, QPainter, QPointF, The document this window edits., MeasureTool, Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview. (+26 more)

### Community 8 - "Mesh"
Cohesion: 0.10
Nodes (28): Qt-free geometry, camera and document model for the reference viewer., Mesh, Triangle-mesh containers shared by the loader, the renderer and picking., Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, Hit, intersects_bounds(), ndarray (+20 more)

### Community 9 - "Bounds"
Cohesion: 0.11
Nodes (19): Bounds, ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, An axis-aligned bounding box., Radius of the sphere circumscribing the box (never zero)., build_pedestal(), _disc() (+11 more)

### Community 10 - "RenderSettings"
Cohesion: 0.11
Nodes (20): Everything the viewport needs in order to draw a frame., RenderSettings, light_directions(), normal_matrix(), ndarray, The model's own planes under ``mode``, fitted once and kept., Replace the section contour, prepared by the caller as stroke vertices., Draw one frame, then hand a neutral GL state back to the caller.… (+12 more)

### Community 11 - "Camera"
Cohesion: 0.08
Nodes (17): Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around., Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Turntable-orbit around ``pivot`` (defaults to the camera target). (+9 more)

### Community 12 - "camera.py"
Cohesion: 0.14
Nodes (22): Interactive camera model driving both perspective and orthographic views., look_at(), normalize(), orthographic(), perspective(), ndarray, Small linear-algebra helpers using OpenGL conventions. Matrices are stored row-…, Return ``v`` scaled to unit length, or ``fallback`` for a zero vector. (+14 more)

### Community 13 - "OrientationSettings"
Cohesion: 0.09
Nodes (25): OrientationSettings, Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., UpAxis (+17 more)

### Community 14 - "SceneRenderer"
Cohesion: 0.12
Nodes (10): ColorTarget, A single-channel colour framebuffer, used for the occlusion buffers., MeshBuffers, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Replace the ground disc; pass ``None`` to hide it., Fill the shader's table with a level, if it is not already in it., Replace the annotation geometry; pass an empty list to hide it., Vertex/index buffers for one mesh, bound through a single VAO. (+2 more)

### Community 15 - "README.md"
Cohesion: 0.09
Nodes (25): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, refview (+17 more)

### Community 16 - "gltf_loader.py"
Cohesion: 0.09
Nodes (33): Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor() (+25 more)

### Community 17 - "form_group"
Cohesion: 0.22
Nodes (11): QFormLayout, QGroupBox, Everything that acts on the shading normals rather than on the shading. Faceted…, Cross-section controls: the cutting plane, what it keeps and how it reads., collapsible_group(), form_group(), _panel_form(), Small reusable controls shared by the side panels. (+3 more)

### Community 18 - "mesh_renderer.py"
Cohesion: 0.08
Nodes (16): bind_default(), current_framebuffer(), DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality pass. Three of them are…, Depth plus view-space normals: the inputs the occlusion pass reads. Storing the…, The framebuffer object bound right now -- Qt's, in a widget., Restore a framebuffer captured with :func:`current_framebuffer`. (+8 more)

### Community 19 - "CameraPanel"
Cohesion: 0.13
Nodes (7): QListWidgetItem, CameraPanel, Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions.

### Community 20 - "_morton_order"
Cohesion: 0.28
Nodes (7): _morton_order(), ndarray, Build the index from expanded triangle corners, shape ``(T, 3, 3)``., Triangle indices worth intersecting for this ray, possibly empty., Indices that sort ``points`` along a Morton (Z-order) curve. Neighbours on the…, Interleave each 10-bit value with two zero bits, ready to be shifted., _spread_bits()

### Community 21 - "ShaderProgram"
Cohesion: 0.13
Nodes (8): ndarray, RuntimeError, Thin wrapper around an OpenGL shader program., Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "plane_axes.py"
Cohesion: 0.13
Nodes (13): _empty(), PlaneAxes, PlaneSet, ndarray, Reading the planes of a form out of the model's own normals. The grid quantiser…, One level of a fit: the planes the shader is to quantise against. A plane is a…, A level with no place in it: nearest direction wins, as before., The planes a model falls into, at every count. Built once per mesh and per… (+5 more)

### Community 23 - "render/__init__.py"
Cohesion: 0.10
Nodes (13): OpenGL rendering layer: shader programs, textures and the scene renderer., DataTexture, default_matcap_pixels(), MatcapLoadError, ndarray, RuntimeError, Matcap texture loading and upload, and the small data table beside it., An RGBA8 2D texture with clamped edges and mipmapped minification. (+5 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.17
Nodes (6): QTreeWidgetItem, MeasurePanel, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Lists saved measurements and controls how they are drawn.

### Community 25 - "BookmarkStore"
Cohesion: 0.10
Nodes (11): BookmarkStore, CameraBookmark, Named camera positions the artist can jump between while sculpting., A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Projection settings, standard views and named camera bookmarks. (+3 more)

### Community 26 - "NavigationController"
Cohesion: 0.12
Nodes (12): Shift-snapped orbiting (1.1.0), DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is… (+4 more)

### Community 27 - "History"
Cohesion: 0.14
Nodes (6): Camera motion is deliberately not undoable, Command, History, One reversible change, named for the undo menu., A bounded undo/redo stack., Record ``command``, applying it first unless it already ran. Interactive…

### Community 28 - "SliderSpin"
Cohesion: 0.16
Nodes (7): QFrame, CollapsibleGroup, QWidget, A group whose rows fold away behind its title. For settings that are worth…, A float slider paired with a spin box, kept in sync. The slider works in…, Re-scale the control, e.g. once a model's size is known., SliderSpin

### Community 29 - "mesh_io.py"
Cohesion: 0.15
Nodes (18): STL corner welding, One entry point for every mesh format the viewer reads. Callers ask for a path…, MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., _ascii_corners(), _binary_corners(), load_stl() (+10 more)

### Community 30 - "Measurement"
Cohesion: 0.11
Nodes (12): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+4 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.23
Nodes (6): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., ShadingPanel

### Community 32 - "test_mesh_io.py"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

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
Cohesion: 0.16
Nodes (12): _fit(), Patches, ndarray, The design matrix, and the frame it was measured in., Distance out to each vertex's own tangent plane. ``(m,)``., The rows the clusterers actually see. ``(m, 7)``., What the clusterers see: one row per patch of surface. ``moments`` is the *sum*…, Unit direction of each patch. ``(p, 3)``. (+4 more)

### Community 37 - "AddItem"
Cohesion: 0.19
Nodes (13): AddItem, Append an item to a document list., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch(), test_commands_carry_their_channel_and_name() (+5 more)

### Community 38 - "release_from_payload"
Cohesion: 0.19
Nodes (14): is_newer(), _padded(), parse_version(), Numeric components of ``text``, or ``None`` when it is not a version. A pre-…, Whether ``candidate`` is a strictly later version than ``current``., Pull the tag and page link out of a GitHub release document., release_from_payload(), parametrize (+6 more)

### Community 39 - "SectionSettings"
Cohesion: 0.11
Nodes (22): ndarray, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., Line segments where ``plane`` cuts ``mesh``, shape ``(n, 2, 3)``. Every…, Unit axis, or ``None`` for a custom direction., A half-space: everything past ``offset`` along ``normal`` is cut away., Signed distance of each point; positive means cut away., How the model is cut open, and how the cut is drawn. (+14 more)

### Community 40 - "SectionPanel"
Cohesion: 0.21
Nodes (6): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 41 - "Snapped Orbit Tests"
Cohesion: 0.36
Nodes (10): _azimuth(), Mouse gestures driving the camera, including Shift-snapped orbiting., Compass angle of the camera around the object, in degrees., Snapped angles are measured from the press, so the two modes agree., _start(), test_a_free_orbit_follows_the_mouse_exactly(), test_releasing_shift_resumes_the_free_orbit_from_there(), test_snapping_holds_still_until_the_next_step() (+2 more)

### Community 42 - "section.py"
Cohesion: 0.27
Nodes (7): Enum, str, Cutting the model open with planes. A section is described by one plane -- an…, The direction the section plane faces., Which side of the plane survives the cut., SectionAxis, SectionMode

### Community 43 - "state.py"
Cohesion: 0.09
Nodes (25): Handle, MeasurementSettings, How measurements are drawn and how their lengths are written out., Render a scene-unit length as a labelled display string., _coerce(), decode(), encode(), Any (+17 more)

### Community 44 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 45 - "test_session.py"
Cohesion: 0.12
Nodes (14): Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., A step of the slider is worth a fixed share more planes, not a fixed number of…, The ceiling went from 64 planes to 256 without moving the slider under anyone:…, The panel edits the settings; the fit has to be told what they are., Both modes answer in degrees of turn, so the panel can just ask., Version 1 files predate the annotation layer and the endpoint lock., test_a_session_from_before_annotations_still_loads() (+6 more)

### Community 46 - "TriangleIndex"
Cohesion: 0.14
Nodes (15): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list., TriangleIndex, _grid(), The picking accelerator: it must be fast without changing any answer. (+7 more)

### Community 47 - "load_matcap_pixels"
Cohesion: 0.31
Nodes (13): Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels(), Path (+5 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "matcap_panel.py"
Cohesion: 0.31
Nodes (11): available_matcaps(), _bundled_root(), image_path(), matcap_dir(), model_dir(), Path, Locations of the bundled resources. ``REFVIEW_RESOURCES`` overrides the search,…, Return PyInstaller's extracted application directory when frozen. (+3 more)

### Community 50 - "Panel"
Cohesion: 0.21
Nodes (5): Panel, QWidget, A panel bound to the :class:`ViewerState`. Subclasses build their controls in…, Pull current values out of the state and into the widgets., Ignore widget signals for the duration of the block.

### Community 52 - "MatcapPanel"
Cohesion: 0.27
Nodes (4): MatcapPanel, Rebuild the thumbnail list from the resources folder., Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…

### Community 53 - "AnnotatePanel"
Cohesion: 0.27
Nodes (3): AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle.

### Community 54 - "viewport.py"
Cohesion: 0.23
Nodes (7): Named point-to-point measurements and their presentation options., Qt user interface: the viewport widget, the panels and the main window., Two-click measuring, plus dragging the endpoints of an unlocked measurement., 2D overlay drawn on top of the GL scene with QPainter. Measurements are…, configure_surface_format(), The interactive 3D view. Navigation is: left-drag orbits about the point under…, Request a core-profile context; must run before the QApplication.

### Community 55 - "Path"
Cohesion: 0.29
Nodes (3): Path, Apply a matcap image, reporting unreadable files to the user., Load a model, reporting failures without tearing down the window.

### Community 56 - "settings.py"
Cohesion: 0.05
Nodes (37): High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, Coefficients, What each block of the design matrix counts for, against the normals. A fit…, Whether anything but the normals is being read at all., fit_planes(), The planes of ``mesh`` under ``mode``; empty where the mode needs none. (+29 more)

### Community 57 - "plane_clusters.py"
Cohesion: 0.11
Nodes (25): _compact(), _consensus(), _cut(), _first_planes(), flatness(), _leaves(), neighbour_agreement(), plane_flats() (+17 more)

### Community 58 - "annotation.py"
Cohesion: 0.22
Nodes (6): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a…

### Community 59 - "obj_loader.py"
Cohesion: 0.11
Nodes (30): compute_vertex_normals(), Area-weighted smooth vertex normals for an indexed triangle soup., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic() (+22 more)

### Community 60 - "measure_panel.py"
Cohesion: 0.15
Nodes (8): The handful of undoable edits the whole application is built from.…, Swap the whole contents of a document list. Used for bulk edits -- clearing the…, ReplaceItems, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, Surface annotation tool: brush, shape and eraser settings., Shared plumbing for the dockable side panels., Dockable control panels., Measurement list and display options.

### Community 61 - "RemoveItem"
Cohesion: 0.22
Nodes (4): Any, Delete the item at ``index``, putting it back in place on undo., RemoveItem, test_remove_puts_the_item_back_where_it_was()

### Community 62 - "ColorButton"
Cohesion: 0.31
Nodes (3): QPushButton, ColorButton, A swatch button that opens a colour picker. Colours are exchanged as 0-1 RGB…

### Community 63 - "SetAttributes"
Cohesion: 0.31
Nodes (4): Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable.

### Community 64 - "generate_matcaps.py"
Cohesion: 0.32
Nodes (7): Color, main(), _normalize(), ndarray, Path, Render the bundled matcap set. Each preset is evaluated analytically over the…, save()

### Community 65 - ".drag_target"
Cohesion: 0.29
Nodes (4): ndarray, Consume a picked point; returns a measurement on the second click., Where a click at ``(x, y)`` would put a point. With free placement the point…, Where a grabbed endpoint should move to. Free placement -- and a drag that…

### Community 66 - ".point"
Cohesion: 0.29
Nodes (4): ndarray, Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-…, Screen-to-world scale at a given depth along the view direction.

### Community 67 - "lock_icon"
Cohesion: 0.33
Nodes (4): QIcon, lock_icon(), Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if…

### Community 68 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): QStyledItemDelegate, _NameOnlyDelegate, Allows in-place editing of the name column only.

### Community 69 - "vertex_weights"
Cohesion: 0.50
Nodes (4): How much surface each vertex stands for: a third of each triangle on it.…, vertex_weights(), A finely tessellated sliver must not outvote a broad flat face. The mesh here…, test_a_plane_is_weighed_by_its_area_not_by_its_vertex_count()

### Community 70 - "Projection"
Cohesion: 0.33
Nodes (4): Projection, Enum, str, Projection used by :class:`Camera`.

### Community 71 - "PlanesPanel"
Cohesion: 0.39
Nodes (3): PlanesPanel, Breaks the surface normals down into the planes of the form., Put the design matrix back the way it reads a figure.

### Community 72 - "scrollable"
Cohesion: 0.67
Nodes (3): QScrollArea, Wrap a panel so it scrolls when it is taller than the dock. The controls keep…, scrollable()

## Knowledge Gaps
- **1 isolated node(s):** `refview`
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `plane_axes`, `ViewerState`, `Bounds`, `OrientationSettings`, `SceneRenderer`, `gltf_loader.py`, `mesh_renderer.py`, `plane_axes.py`, `mesh_io.py`, `test_mesh_io.py`, `test_plane_clusters.py`, `ndarray`, `SectionSettings`, `section.py`, `state.py`, `TriangleIndex`, `settings.py`, `plane_clusters.py`, `obj_loader.py`, `vertex_weights`?**
  _High betweenness centrality (0.132) - this node is a cross-community bridge._
- **Why does `Camera` connect `Camera` to `test_camera.py`, `ViewerState`, `Mesh`, `Bounds`, `RenderSettings`, `state.py`, `camera.py`, `Snapped Orbit Tests`, `README.md`, `mesh_renderer.py`, `Screen-to-World Panning`, `viewport.py`, `BookmarkStore`, `NavigationController`?**
  _High betweenness centrality (0.084) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `main_window.py`, `Viewport Widget`, `MainWindow`, `state.py`, `OrientationSettings`, `README.md`, `Panel`, `viewport.py`, `measure_panel.py`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `Mesh` (e.g. with `GltfLoadError` and `TriangleIndex`) actually correct?**
  _`Mesh` has 15 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `Viewport` (e.g. with `MainWindow` and `AnnotateTool`) actually correct?**
  _`Viewport` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `MainWindow` (e.g. with `ViewerState` and `UpdateChecker`) actually correct?**
  _`MainWindow` has 3 INFERRED edges - model-reasoned connections that need verification._