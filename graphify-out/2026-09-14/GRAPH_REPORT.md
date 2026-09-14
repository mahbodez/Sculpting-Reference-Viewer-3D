# Graph Report - reference-viewer  (2026-09-14)

## Corpus Check
- 134 files · ~433,589 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 4287 nodes · 9622 edges · 156 communities (151 shown, 5 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 450 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `68bcb195`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SettingsWindow
- test_preferences.py
- main_window.py
- Viewport
- plane_axes
- form_group
- MainWindow
- Stroke
- GifWriter
- mesh_renderer.py
- SceneRenderer
- solid_count
- naming.py
- _derived
- Armature
- README.md
- ViewerState
- PlaneSettings
- framebuffer.py
- CameraPanel
- UpdateChecker
- ShaderProgram
- ViewportOverlay
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- VideoError
- SectionSettings
- plane_volume.py
- ControlsWindow
- mesh.py
- ShadingPanel
- FilmRecorder
- test_camera.py
- test_plane_clusters.py
- WakeLock
- MatcapPreview
- SectionPanel
- CustomPanel
- film_export.py
- AnnotateTool
- Camera
- test_armature.py
- ValueSlider
- gltf_loader.py
- ExportVideoDialog
- VideoSettings
- _Build
- Agent Graph-First Instructions
- StrokeBuffers
- Mesh
- test_matcap_preview.py
- build_humanoid
- settings_window.py
- OrientationSettings
- MeasurementStore
- FilmExport
- FormsPanel
- PlanesPanel
- forms.py
- ArmatureTool
- Workspace
- Command
- test_forms.py
- application.py
- MeasureTool
- Link
- PrimaryForm
- History
- compute_vertex_normals
- ReplaceItems
- test_plane_solids.py
- .__init__
- decode
- ._advance_pending
- texture.py
- load_matcap_pixels
- test_custom_panels.py
- AddItem
- core/preferences.py
- test_session.py
- NavigationController
- Bounds
- _NameOnlyDelegate
- test_forms_panel.py
- raycast_mesh
- MeshLoadError
- .refresh_list
- MatcapPanel
- ColorButton
- Frame
- _Encoder
- ._picker
- test_elements.py
- ._focused_form
- FormRun
- ReflowLayout
- core/__init__.py
- ArmaturePanel
- .load
- clone.py
- ._upload_sculpt
- Path
- paths.py
- .mouseReleaseEvent
- test_panel_docks.py
- icons.py
- ._place_armature_node
- test_mesh_io.py
- annotation.py
- DockTitle
- test_reflow.py
- MatcapSettings
- .update_enabled
- ArmatureStore
- ._build
- ._arm
- Reflow
- ShadingMode
- SetAttributes
- QPointF
- release.yml
- .split
- .stage_images
- test_annotation.py
- _MacBackend
- .endpoint
- welded
- FormStore
- SectionAxis
- ._forms_hud
- OverlayParts
- ExportLook
- ._place_form_landmark
- ._armature_hud
- .column_of
- theme.py
- .mouseMoveEvent
- _height_of
- SectionGizmo
- _drag_over
- section
- panel
- MeshBuffers
- .install
- coarse_lattice
- app
- ._built
- PreferenceStore
- restored
- Q: Where are the todo viewport marker and shading changes implemented?
- sample_count
- coarse_lattice
- environment.yml
- palette.py
- app

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 144 edges
2. `Viewport` - 115 edges
3. `Camera` - 81 edges
4. `PrimaryForm` - 79 edges
5. `ViewerState` - 77 edges
6. `MainWindow` - 76 edges
7. `Armature` - 74 edges
8. `PlaneSettings` - 67 edges
9. `FormsPanel` - 63 edges
10. `ArmaturePanel` - 62 edges

## Surprising Connections (you probably didn't know these)
- `Orthographic extent derived from FOV and distance` --rationale_for--> `Camera`  [EXTRACTED]
  README.md → src/refview/core/camera.py
- `REFVIEW_RESOURCES resource override` --rationale_for--> `available_matcaps()`  [EXTRACTED]
  README.md → src/refview/paths.py
- `Terracotta clay matcap` --shares_data_with--> `available_matcaps()`  [INFERRED]
  resources/matcaps/clay_terracotta.png → src/refview/paths.py
- `The cut interior is flooded flat` --rationale_for--> `SceneRenderer`  [INFERRED]
  README.md → src/refview/render/mesh_renderer.py
- `Every document edit is a command` --rationale_for--> `SetAttributes`  [EXTRACTED]
  README.md → src/refview/core/commands.py

## Import Cycles
- 3-file cycle: `src/refview/ui/elements/__init__.py -> src/refview/ui/elements/clone.py -> src/refview/ui/elements/slider.py -> src/refview/ui/elements/__init__.py`
- 4-file cycle: `src/refview/ui/elements/__init__.py -> src/refview/ui/elements/custom.py -> src/refview/ui/elements/clone.py -> src/refview/ui/elements/slider.py -> src/refview/ui/elements/__init__.py`

## Hyperedges (group relationships)
- **The bundled matcap set** — resources_matcaps_clay_terracotta_matcap, resources_matcaps_charcoal_matcap, resources_matcaps_jade_matcap, resources_matcaps_steel_matcap, resources_matcaps_studio_white_matcap, resources_matcaps_wax_skin_matcap, tools_generate_matcaps_matcappreset, tools_generate_matcaps_render [INFERRED 0.85]
- **The four generic undo commands** — src_refview_core_commands_setattributes, src_refview_core_commands_additem, src_refview_core_commands_removeitem, src_refview_core_commands_replaceitems, src_refview_core_history_command, readme_every_edit_is_a_command [EXTRACTED 1.00]
- **Windows binary-compatibility decisions** — readme_pyside6_pinned_below_68, environment_pip_installed_binaries, environment_python_311, github_workflows_release_pyinstaller_build [INFERRED 0.75]

## Communities (156 total, 5 thin omitted)

### Community 0 - "SettingsWindow"
Cohesion: 0.16
Nodes (10): The preferences as they stand. Treat as read-only; use :meth:`set`., QWidget, Fill in the groups. A switch with nothing to put in the caption column is given…, The one button that is not a preference, and what the window is for., Say what the view is really drawing with, beside what was asked for. A sample…, Put one field back into the store, which applies and saves it., Pull every control back into line with the store. Run when the window is built,…, Open one group and fold the rest, for the Settings menu's entries. Folding the… (+2 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.07
Nodes (39): Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, app(), model(), fixture, What the artist prefers: kept apart from the document, and acted upon. Two…, An external drive that is not plugged in is not an empty gallery. (+31 more)

### Community 2 - "main_window.py"
Cohesion: 0.09
Nodes (37): check_for_update(), fetch_latest_release(), is_newer(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and…, The release could not be looked up (offline, rate limited, malformed). (+29 more)

### Community 3 - "Viewport"
Cohesion: 0.07
Nodes (13): QOpenGLWidget, Slide the view so a point sits at the centre, keeping the angle., A form changed: work its clay out again and redraw., Slide the view so a measurement sits at the centre, keeping the angle., Regenerate the pedestal and the cut contour when their settings move. Both are…, End any film being recorded, and wait for its thread to really stop. For…, The document being drawn., The film of the form's making, as far as it has been recorded. (+5 more)

### Community 4 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 5 - "form_group"
Cohesion: 0.07
Nodes (35): The handful of undoable edits the whole application is built from.…, Delete the item at ``index``, putting it back in place on undo., RemoveItem, Undo/redo stack. Every document edit is expressed as a :class:`Command` that…, framed(), A frame with a form layout in it, ready to be filled., Surface annotation tool: brush, shape and eraser settings., The armature: its nodes, the guided presets, and how the wire is drawn. (+27 more)

### Community 6 - "MainWindow"
Cohesion: 0.05
Nodes (21): QAction, MainWindow, QMainWindow, Put the panels back where they started, now., Follow the machine's sleep to whether this window is in front., Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model. (+13 more)

### Community 7 - "Stroke"
Cohesion: 0.12
Nodes (11): AnnotationStore, An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Stroke, The strokes being laid down; the overlay previews them in 2D., The surviving arc wraps past the start of the list, so the gap is rotated to… (+3 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "mesh_renderer.py"
Cohesion: 0.10
Nodes (29): Projection, Enum, str, Interactive camera model driving both perspective and orthographic views., Projection used by :class:`Camera`., look_at(), normalize(), orthographic() (+21 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.10
Nodes (23): Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, normal_matrix(), ndarray, Owns every GL resource the viewport needs. The widget calls :meth:`initialize`…, Fill the shader's table with a level, if it is not already in it., Replace the section contour, prepared by the caller as stroke vertices. (+15 more)

### Community 11 - "solid_count"
Cohesion: 0.17
Nodes (15): How many solids each stage of a film is made of. Every count from the coarsest…, stage_counts(), block_count(), piece_count(), How many blocks a count of planes asks the stone to be cut into. One at the…, How many lumps a count of planes asks the clay to be built out of. The masses…, How many solids the form is made of, whichever way it is being worked., solid_count() (+7 more)

### Community 12 - "naming.py"
Cohesion: 0.11
Nodes (28): _clone_slider(), _asked(), caption_for(), element_id(), forget(), _free(), _from_id(), name_tree() (+20 more)

### Community 13 - "_derived"
Cohesion: 0.09
Nodes (22): _derived(), A guess the artist corrects is theirs, and the mirror leaves it alone., The new list is the edit; the old one has to survive to be undone to., Which is what keeps a dragged cross and a typed position one behaviour. The…, Hips, then the ribcage, then the head, then the limbs largest first. This order…, A nudged landmark rebuilds the whole wire, and it would be intolerable for that…, Which is the difference between the parts of a figure an artist wants blocked…, The budget is spent on what is actually laid, so skipping the hips means the… (+14 more)

### Community 14 - "Armature"
Cohesion: 0.03
Nodes (71): BoneRef, Armature, ArmatureNode, Bone, ndarray, Point3, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the… (+63 more)

### Community 15 - "README.md"
Cohesion: 0.12
Nodes (20): High Quality shading mode (1.1.0), Annotations drawn as widened geometry, core never imports Qt, Every document edit is a command, High Quality without ray tracing, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance (+12 more)

### Community 16 - "ViewerState"
Cohesion: 0.08
Nodes (21): Path, QObject, Emit the change signal a command's channel maps onto., Run an edit through the history so it can be undone. ``apply=False`` records a…, Load a model, centre it on the origin and frame it in the view. The current…, Turn a freshly read mesh the right way up and centre it., Turn the model, bringing the marks made on it along. Measurements, annotations,…, Take the display unit from the file when the format declares one. Only glTF… (+13 more)

### Community 17 - "PlaneSettings"
Cohesion: 0.05
Nodes (36): film_key(), What a film depends on. Everything that changes the shape of any stage, and…, Holds the working state between one turn of the sliders and the next.…, Drop everything held, so the next call starts from the fit., The fit these settings ask for, refitting only if it has gone stale. The fit is…, The stand-in these settings ask for, or ``None`` for the model itself., SculptCache, lattice_fineness() (+28 more)

### Community 18 - "framebuffer.py"
Cohesion: 0.08
Nodes (16): AccumTarget, ColorTarget, DepthTarget, GeometryTarget, Offscreen render targets used by the high-quality and ghost passes. Four of…, A depth-only framebuffer, sampled afterwards as a texture., ``clamp_to_lit`` makes everything outside the map read as unshadowed., A single-channel colour framebuffer, used for the occlusion buffers. (+8 more)

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
Cohesion: 0.18
Nodes (11): One marker object for endpoints, nodes, landmarks and tool previews., VisualMarker, project_visible(), Handle, Draws measurements, tool previews, the orientation gizmo and the readout., An unfilled circle: how thick the form is here, not how big a dot is., A world radius in pixels, measured rather than converted. Projecting the node…, The landmarks of a guided run, and the point about to be placed. (+3 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.07
Nodes (25): app(), _names(), panel(), fixture, The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as… (+17 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.10
Nodes (11): MeasurePanel, _NameOnlyDelegate, QStyledItemDelegate, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing… (+3 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.12
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around. (+1 more)

### Community 26 - "VideoError"
Cohesion: 0.09
Nodes (15): _FFmpegWriter, ndarray, Path, RuntimeError, An export that could not be written, said in words for the artist., What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``. (+7 more)

### Community 27 - "SectionSettings"
Cohesion: 0.15
Nodes (16): The cut interior is flooded flat, Unit plane normal, honouring the flip toggle., The half-spaces the current mode cuts with; empty when disabled., How the model is cut open, and how the cut is drawn., SectionSettings, _box(), Cutting planes, the contour they produce and the pedestal under the model., A closed axis-aligned cube centred on the origin. (+8 more)

### Community 28 - "plane_volume.py"
Cohesion: 0.04
Nodes (114): Work the form stage by stage, handing each one back as it is finished. A…, record(), _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field() (+106 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "mesh.py"
Cohesion: 0.10
Nodes (23): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Triangle-mesh containers shared by the loader, the renderer and picking., Picking accelerator, built on first use and kept for the mesh's life., _morton_order(), ndarray, Spatial index that keeps picking fast on large meshes. Every click, every hover…, Leaf bounding boxes over a Morton-sorted triangle list. (+15 more)

### Community 31 - "ShadingPanel"
Cohesion: 0.16
Nodes (10): Chooses the shading model and edits its light and surface parameters., Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel, test_a_copied_group_still_drives_the_originals() (+2 more)

### Community 32 - "FilmRecorder"
Cohesion: 0.06
Nodes (36): QThread, Film, A whole making, from the coarsest stage to the one the slider asks for. Held by…, FilmRecorder, QObject, The film being recorded, or the last one finished., Whether a film is being made right now., The film already held for ``key``, if there is one. (+28 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.06
Nodes (54): angle_deg(), bent_plate(), cube(), lumpy(), ndarray, parametrize, quad(), Fitting planes to a model's surface rather than only to its normals. What… (+46 more)

### Community 35 - "WakeLock"
Cohesion: 0.06
Nodes (29): _Backend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., Holds sleep off while the window that owns it is the one in front. The class…, Hold sleep off, or stop holding it, whichever is not already true., Drop the request, if one is out. Safe to call more than once. (+21 more)

### Community 36 - "MatcapPreview"
Cohesion: 0.08
Nodes (19): _clone_preview(), MatcapPreview, _pull_preview(), _push_preview(), ndarray, QSize, QWidget, A matcap on a sphere, which is also how the matcap is graded. (+11 more)

### Community 37 - "SectionPanel"
Cohesion: 0.18
Nodes (7): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 38 - "CustomPanel"
Cohesion: 0.08
Nodes (27): carried(), in_flight(), The id of what a copy copies, or an empty string., Read a drag's payload back, or ``None`` if it is not one of ours., source_of(), CustomPanel, _detach(), QFormLayout (+19 more)

### Community 39 - "film_export.py"
Cohesion: 0.07
Nodes (27): _encode_arguments(), _encoders(), ffmpeg_path(), _no_window(), Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a… (+19 more)

### Community 40 - "AnnotateTool"
Cohesion: 0.13
Nodes (13): AnnotationSettings, The annotate tool's brush, shared by every stroke it lays down., AnnotateTool, ndarray, Centre and world radius of the eraser, or ``None`` when off the model., Add one freehand point, unless the cursor has barely moved., Project screen-space samples onto the surface, breaking at the misses., Continue the open run with a hit, or end it where the ray missed. (+5 more)

### Community 41 - "Camera"
Cohesion: 0.07
Nodes (28): Camera, ndarray, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Intersect the pixel ray with the camera-facing plane through a point. Defaults…, Screen-to-world scale at the focal plane; identical in both modes., Turntable-orbit around ``pivot`` (defaults to the camera target)., Reject rotations that would drive the view onto the up-axis pole. (+20 more)

### Community 42 - "test_armature.py"
Cohesion: 0.10
Nodes (33): _chain(), The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other., Place every landmark the run asks for; returns how many were asked., A straight run of nodes one unit apart along +X., Nothing stands between one neighbour, so there is nothing to bridge., _run(), test_a_bone_at_the_end_of_the_list_cannot_be_moved_off_it() (+25 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (11): _pull_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end., Set the value the way a hand on the control would., The value the track stands at ``x`` pixels across. (+3 more)

### Community 44 - "gltf_loader.py"
Cohesion: 0.10
Nodes (33): Shift-snapped orbiting (1.1.0), Model orientation (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL and glTF import (1.1.0), Units are adopted, never guessed, _accessor() (+25 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.11
Nodes (12): QDialog, QProgressDialog, even(), ExportVideoDialog, Path, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the… (+4 more)

### Community 46 - "VideoSettings"
Cohesion: 0.10
Nodes (18): open_writer(), How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., Start an encoder for ``settings``, or say why there cannot be one., VideoSettings (+10 more)

### Community 47 - "_Build"
Cohesion: 0.21
Nodes (14): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _mid(), ndarray, Somewhere to collect nodes while the rules that need each other run. (+6 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "StrokeBuffers"
Cohesion: 0.16
Nodes (12): build_segment_vertices(), build_vertices(), _expand(), ndarray, Geometry for the surface annotations and the cross-section contour. Strokes are…, A single vertex buffer holding every visible stroke., Replace the buffer contents with a prepared vertex block., Expand strokes into the triangle soup the stroke shader expects. Every segment… (+4 more)

### Community 50 - "Mesh"
Cohesion: 0.03
Nodes (99): Mesh, Return a copy whose bounding-box centre sits at the origin., An indexed triangle mesh with per-vertex positions and normals. The viewer…, Coefficients, _empty(), PlaneAxes, PlaneSet, ndarray (+91 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.10
Nodes (32): QPoint, _angle(), The angle of ``point`` about ``centre``, anticlockwise with y upwards., _drag(), parametrize, The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc. (+24 more)

### Community 52 - "build_humanoid"
Cohesion: 0.19
Nodes (21): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _figure(), ndarray, The femoral head is in from the ASIS, below it and behind it, by shares of the…, A wire in two halves is not an armature anybody could bend., Every required humanoid landmark, both sides, scaled about the origin., _roles() (+13 more)

### Community 53 - "settings_window.py"
Cohesion: 0.12
Nodes (14): QScrollArea, A layout that turns a column of groups into columns when given the width. A…, QWidget, Pull current values out of the state and into the widgets., The window the preferences are set in. Built out of the same elements the…, name_sliders(), QWidget, Move each slider's caption off the row and into the slider itself. A slider… (+6 more)

### Community 54 - "OrientationSettings"
Cohesion: 0.09
Nodes (24): OrientationSettings, Enum, str, Putting an imported model the right way up. Formats disagree about which axis…, Which axis of the file points up., A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., UpAxis (+16 more)

### Community 55 - "MeasurementStore"
Cohesion: 0.18
Nodes (4): MeasurementStore, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., An ordered, named collection of measurements. Deliberately plain: the Qt layer…

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (11): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+3 more)

### Community 57 - "FormsPanel"
Cohesion: 0.10
Nodes (10): FormsPanel, Arms the forms tool, runs the guided presets and lists what they built., Take back the landmark before this one and ask for it again., Take back the last landmark a freeform was given, guess and all., Ready the landmark the next click lays down, from the name and side boxes., Record an edited landmark list, mirrored where the mirror is on., Remove the selected landmark, or the whole form when its row is picked., The mirrored landmarks reflected from ``key``, which it anchors. (+2 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.08
Nodes (22): PlanesPanel, QListWidgetItem, Lay one length of wire earlier or later, as one undoable step., Put the design matrix back the way it reads a figure., Hold the settings a recording is built from still while it runs. A film is a…, Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Show what this way of working needs, and put the rest away. A setting that does… (+14 more)

### Community 59 - "forms.py"
Cohesion: 0.04
Nodes (60): convex_hull(), DegenerateHullError, flat_mesh(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, The outward unit normal at each vertex: the area-weighted mean of its faces'. A… (+52 more)

### Community 60 - "ArmatureTool"
Cohesion: 0.07
Nodes (36): LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, Handle, Begin a preset run against an armature already in the store., The landmarks still to place, in order, the current one first., The landmark the artist is being asked for right now. (+28 more)

### Community 61 - "Workspace"
Cohesion: 0.05
Nodes (27): QDockWidget, QTabBar, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top., QMainWindow, QObject, QSettings, QWidget (+19 more)

### Community 62 - "Command"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 63 - "test_forms.py"
Cohesion: 0.05
Nodes (76): One convex piece of a form: its hull vertices and outward-wound faces., The longest side of the box the solid sits in., Whether a point lies inside, or within ``slack`` of the surface., What is left on the ``normal @ x <= offset`` side of a plane. The hull of the…, Solid, _across(), blend_rings(), build_head() (+68 more)

### Community 64 - "application.py"
Cohesion: 0.10
Nodes (24): ArgumentParser, Namespace, QSplashScreen, _apply_startup_arguments(), build_parser(), _create_splash(), _fitted_title_font(), main() (+16 more)

### Community 65 - "MeasureTool"
Cohesion: 0.22
Nodes (4): MeasureTool, Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview.

### Community 66 - "Link"
Cohesion: 0.12
Nodes (9): CloneGesture, Link, _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original., Whether the copy is being used right now and must not be written. (+1 more)

### Community 67 - "PrimaryForm"
Cohesion: 0.04
Nodes (91): FormLandmarkRef, PlacedLandmark, One anatomical point the artist put on the model during a guided run., merged(), Several flat meshes as one, or ``None`` when there is nothing to draw., build_form(), built_count(), form_landmark_title() (+83 more)

### Community 68 - "History"
Cohesion: 0.17
Nodes (14): History, A bounded undo/redo stack., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made(), test_a_new_edit_discards_the_redo_branch(), test_commands_carry_their_channel_and_name() (+6 more)

### Community 69 - "compute_vertex_normals"
Cohesion: 0.11
Nodes (31): compute_vertex_normals(), Area-weighted smooth vertex normals for an indexed triangle soup., _assemble(), _face_corners(), _float_table(), _index_pairs(), _load_fast(), _load_generic() (+23 more)

### Community 70 - "ReplaceItems"
Cohesion: 0.12
Nodes (6): Swap the whole contents of a document list. Used for bulk edits -- clearing the…, ReplaceItems, AnnotatePanel, Arms the annotate tool and edits the brush it paints with., Reflect the tool state without re-emitting the toggle., test_replace_items_covers_bulk_edits()

### Community 71 - "test_plane_solids.py"
Cohesion: 0.03
Nodes (147): auto_smooth(), A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), film_of(), parametrize (+139 more)

### Community 72 - ".__init__"
Cohesion: 0.12
Nodes (5): Give each panel a dock of its own, tabbed together on the right. Each panel can…, Single-key shortcuts, scoped so they never eat text input. They only fire while…, Push the preferences that this window's own parts hold a copy of. The store has…, Ask GitHub for the newest release in the background. The startup check is…, Put the docks and the hand-built panels back where they were. Unless the artist…

### Community 73 - "decode"
Cohesion: 0.24
Nodes (9): _coerce(), decode(), encode(), Any, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``., T (+1 more)

### Community 74 - "._advance_pending"
Cohesion: 0.25
Nodes (4): Begin a run against a fresh form: a preset's walk, or a freeform's., Take up the selected freeform again, so more landmarks can go on it. The same…, After a landmark goes down: a fresh numbered name, the same side., Record an edit the viewport's tool worked out. A freeform's placed landmark is…

### Community 75 - "texture.py"
Cohesion: 0.11
Nodes (13): OpenGL rendering layer: shader programs, textures and the scene renderer., DataTexture, default_matcap_pixels(), MatcapLoadError, ndarray, RuntimeError, Matcap texture loading and upload, and the small data table beside it., An RGBA16F 2D texture with clamped edges and mipmapped minification. (+5 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.17
Nodes (21): Color, Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels() (+13 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.07
Nodes (23): QMimeData, app(), custom(), _drop_on(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error., A group is not a row, so it goes ahead of the group it was dropped on. (+15 more)

### Community 78 - "AddItem"
Cohesion: 0.22
Nodes (4): AddItem, Append an item to a document list., Add an empty armature and select it., Begin a preset run against a fresh armature.

### Community 79 - "core/preferences.py"
Cohesion: 0.11
Nodes (20): _as_kind_of(), _clamp(), equal(), _fill(), FolderPreferences, InterfacePreferences, NavigationPreferences, Any (+12 more)

### Community 80 - "test_session.py"
Cohesion: 0.11
Nodes (17): Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., A step of the slider is worth a fixed share more planes, not a fixed number of…, The ceiling went from 64 planes to 256 without moving the slider under anyone:…, The panel edits the settings; the fit has to be told what they are., Both modes answer in degrees of turn, so the panel can just ask., Deletion goes through the undo stack, so the store only tracks position., test_deleting_a_bookmark_moves_the_cycling_position() (+9 more)

### Community 81 - "NavigationController"
Cohesion: 0.08
Nodes (18): DragMode, NavigationController, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Orbit in whole increments of ``step`` degrees from the drag's start., Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Degrees of yaw per pixel, signed by whether the drag is inverted. (+10 more)

### Community 82 - "Bounds"
Cohesion: 0.09
Nodes (23): Pedestal (1.1.0), Bounds, _gathered(), ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Which group each of ``total`` things lands in, given pairs that agree. Hooking…, An axis-aligned bounding box. (+15 more)

### Community 83 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 84 - "test_forms_panel.py"
Cohesion: 0.14
Nodes (26): _click(), _pending(), _pick(), _place_all(), The Forms panel: the guided run it drives, and the document it writes. The…, A form row hands the whole form to update_enabled, whose landmark list must be…, Type a name for the next landmark and, if given, pick its side., What the viewport does when a freeform run gets a click. (+18 more)

### Community 85 - "raycast_mesh"
Cohesion: 0.09
Nodes (26): Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test…, Snap a hit onto the nearest corner of its triangle, when close enough.…, A point where a ray met the mesh surface., Slab test against an axis-aligned box; tolerant of axis-parallel rays., Return the closest front- or back-facing hit along the ray, or ``None``. (+18 more)

### Community 86 - "MeshLoadError"
Cohesion: 0.16
Nodes (17): STL corner welding, MeshLoadError, RuntimeError, Raised when a file cannot be interpreted as a triangle mesh., _ascii_corners(), _binary_corners(), load_stl(), ndarray (+9 more)

### Community 87 - ".refresh_list"
Cohesion: 0.24
Nodes (5): QTreeWidgetItem, Rebuild the tree from the store, keeping the landmark being edited shown. Not…, Commit a renamed or re-checked form, or a renamed landmark, if anything changed., Give a freeform's own landmark the name typed into its row., Run a row's edit once Qt has finished delivering the current signal. Committing…

### Community 88 - "MatcapPanel"
Cohesion: 0.17
Nodes (8): MatcapPanel, Rebuild the thumbnail list from the resources folder., The disc was dragged: show the renderer and the numbers what it did., A different matcap: the disc draws whichever one is on the model., Put the numbers back in line with the settings, and redraw the disc. Separate…, Picks the matcap image and tunes how it is sampled., A draggable split: thumbnails above, adjustments below. The gallery is the one…, test_the_disc_draws_the_matcap_that_is_on_the_model()

### Community 89 - "ColorButton"
Cohesion: 0.07
Nodes (19): _clone_point(), _clone_swatch(), _pull_point(), _pull_swatch(), _push_point(), _push_swatch(), _AxisBox, ColorButton (+11 more)

### Community 90 - "Frame"
Cohesion: 0.07
Nodes (19): _pull_frame(), _push_frame(), Nothing: each row inside the copy is linked on its own., Frame, FrameBar, QFormLayout, QPainter, QSize (+11 more)

### Community 91 - "_Encoder"
Cohesion: 0.25
Nodes (5): Queue, _Encoder, QObject, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 92 - "._picker"
Cohesion: 0.14
Nodes (7): ndarray, Rub out the stroke points under the eraser, live., Alt forces the camera gesture, whichever tool is armed., Take hold of a node, to move it, resize it, or just to select it. This works…, Take hold of a landmark, to move it or just to say which one it is., Object centre, which anchors the plane the orbit pivot lies on., Take hold of a form's landmark, to move it or just to say which one it is.

### Community 93 - "test_elements.py"
Cohesion: 0.09
Nodes (17): Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., A matcap has no light to aim, so the Light group goes -- and its space. The…, Run the refresh the shared timer would have run., ``self._mode`` is ``mode``; the group called Mode settles for a number. (+9 more)

### Community 94 - "._focused_form"
Cohesion: 0.22
Nodes (4): Refit the focused freeform's clay; for a new one, remember the choice., Show a stage of the focused form. A view choice, so not an undo step., Size the stage slider to the focused form, and hide it for a one-stage form., The form the stage slider speaks for: the one being guided, else the one picked.

### Community 95 - "FormRun"
Cohesion: 0.40
Nodes (3): FormRun, Begin a run against a form already in the store., A guided form part-way through.

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - "core/__init__.py"
Cohesion: 0.04
Nodes (69): BoneLabels, Buried, Enum, str, A graph of named points under the form, and the wire it stands for. An armature…, When the length of a bone is written beside it., What becomes of the part of the armature the model is standing in front of. An…, Named camera positions the artist can jump between while sculpting. (+61 more)

### Community 98 - "ArmaturePanel"
Cohesion: 0.05
Nodes (28): ArmaturePanel, QPushButton, QWidget, Arms the armature tool, lists its nodes and runs the guided presets., Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle. (+20 more)

### Community 99 - ".load"
Cohesion: 0.20
Nodes (9): Version 4 files predate the armature; they open with an empty one., test_a_session_from_before_the_armature_still_loads(), test_an_armature_survives_a_session_round_trip(), test_a_session_carries_the_hand_built_panels(), Version 1 files predate the annotation layer and the endpoint lock., Version 6 files predate panels being something a session could carry., test_a_session_from_before_annotations_still_loads(), test_a_session_from_before_the_panels_moved_still_loads() (+1 more)

### Community 100 - "clone.py"
Cohesion: 0.06
Nodes (61): QAbstractButton, QComboBox, QLineEdit, QSlider, QSpinBox, _begin(), can_clone(), clone() (+53 more)

### Community 101 - "._upload_sculpt"
Cohesion: 0.22
Nodes (4): The armature the clay is to be built on, if one was chosen. Read here rather…, Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on.

### Community 102 - "Path"
Cohesion: 0.20
Nodes (7): Path, A path written down last time, if it is one and it is still there., Pick up whatever was last being worked on, if that was asked for. A session…, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window., _remembered()

### Community 103 - "paths.py"
Cohesion: 0.26
Nodes (13): available_matcaps(), _bundled_root(), image_path(), matcap_dir(), model_dir(), Path, Locations of the bundled resources. ``REFVIEW_RESOURCES`` overrides the search,…, Return PyInstaller's extracted application directory when frozen. (+5 more)

### Community 104 - ".mouseReleaseEvent"
Cohesion: 0.11
Nodes (9): Record the finished gesture: a move, a resize, or a plain click. A press that…, Record the finished drag as one step, or read a press as a selection., Run a bone between two nodes of the same armature., A node moved by hand stops following its landmarks. Recorded as its own step…, Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Record the finished drag as one step, or read a press as a selection., Track the form landmark under the cursor; True when it changed. (+1 more)

### Community 105 - "test_panel_docks.py"
Cohesion: 0.05
Nodes (31): parametrize, Each panel in a dock of its own, and putting the docks back next time. Two…, An older file must not be able to sweep away the artist's own panels., The show/hide switch on the tab named ``title``, if it has one., Stacked behind another panel is where the switch is worth the most., It is fifteen pixels wide and carries no words, which is exactly the shape the…, Not "clear the setting and restart": tidied now, or it is not tidying., They are work, not arrangement. (+23 more)

### Community 106 - "icons.py"
Cohesion: 0.24
Nodes (10): QIcon, _draw_glyph(), glyph(), lock_icon(), QColor, QPixmap, Small painted icons. Drawing the padlock rather than shipping an image file…, A padlock, shut or hanging open. Open reads as "this measurement will move if… (+2 more)

### Community 107 - "._place_armature_node"
Cohesion: 0.22
Nodes (4): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…, The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…

### Community 108 - "test_mesh_io.py"
Cohesion: 0.18
Nodes (16): load_mesh(), Path, Load any supported mesh file, raising :class:`MeshLoadError` otherwise., Reading the mesh formats the viewer imports., Negative face indices count back from the most recent vertex., A minimal GLB holding the tetrahedron under a scaled node., test_an_unsupported_suffix_is_reported(), test_ascii_stl_matches_the_binary_one() (+8 more)

### Community 109 - "annotation.py"
Cohesion: 0.20
Nodes (7): AnnotateMode, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a…, Painting annotations onto the model surface. Every shape is laid down the same…

### Community 110 - "DockTitle"
Cohesion: 0.09
Nodes (14): QToolButton, DockTitle, make_switch(), QCheckBox, QSize, QWidget, One dock per panel, with a bar of its own across the top. Every panel is its…, Put a show/hide switch at the left of the bar and return it. (+6 more)

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - "MatcapSettings"
Cohesion: 0.17
Nodes (15): MatcapSettings, Post-processing applied to the sampled matcap texel., grade(), Draw the matcap onto a sphere of ``size`` pixels, graded. Returns ``(size,…, Apply the matcap grading to float RGB in 0-1, as the shader does. A…, sample(), app(), preview() (+7 more)

### Community 113 - ".update_enabled"
Cohesion: 0.12
Nodes (8): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., The freeform the highlighted row belongs to, when no run is on., Take off the panel whatever does not apply right now., The form the selected row stands for, when the row is a form., The landmark the highlighted row stands for, if the row is one., Follow the highlighted landmark, and say which one it is in the view., Highlight the row for a landmark picked in the view.

### Community 114 - "ArmatureStore"
Cohesion: 0.18
Nodes (4): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 115 - "._build"
Cohesion: 0.33
Nodes (4): QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 117 - "Reflow"
Cohesion: 0.30
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 118 - "ShadingMode"
Cohesion: 0.25
Nodes (3): Shading model applied to the mesh. ``shader_id`` must stay in sync with the…, Whether the shadow and occlusion pre-passes need to run., ShadingMode

### Community 119 - "SetAttributes"
Cohesion: 0.11
Nodes (10): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, QTreeWidgetItem, Run a row's edit once Qt has finished delivering the current signal. Committing…, Record an edit the viewport's tool worked out., Join two nodes of one armature, if they are two and they are one armature., Rebuild the tree from the store, keeping the tool's selection shown. A node… (+2 more)

### Community 120 - "QPointF"
Cohesion: 0.16
Nodes (15): QPointF, QRectF, draw_rail(), The screen-space cue for one degree of freedom. A vertical rail that fades out…, QColor, QFont, QPainter, A short line in one corner of the frame; returns where it went. For an exported… (+7 more)

### Community 121 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 122 - ".split"
Cohesion: 0.29
Nodes (5): ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., Normals padded to match the points, so callers can zip them freely., Break the stroke into the runs of points ``keep`` marks as surviving., _runs()

### Community 123 - ".stage_images"
Cohesion: 0.17
Nodes (8): QOpenGLFramebufferObject, QImage, Use the same cached visibility test for bones and all point markers., One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A…, An offscreen target the frames are drawn into, made once per export.…, Draw the scene into ``surface`` and read it back as an image., Lay the overlay -- and the caption, if it was asked for -- on a frame. Painted…

### Community 124 - "test_annotation.py"
Cohesion: 0.31
Nodes (9): line_stroke(), Surface annotations: erasing, splitting and the geometry handed to GL., A stroke running along +X, one unit apart, with +Y normals., test_a_closed_stroke_gains_the_wrapping_segment(), test_each_segment_becomes_six_vertices(), test_erasing_keeps_the_brush_and_drops_stubs(), test_erasing_nothing_reports_no_change(), test_erasing_the_middle_splits_a_stroke_in_two() (+1 more)

### Community 125 - "_MacBackend"
Cohesion: 0.33
Nodes (3): c_void_p, _MacBackend, An IOKit power assertion, held by id until it is released.

### Community 127 - "welded"
Cohesion: 0.67
Nodes (3): ndarray, Which point each vertex really is, once copies of a position are one point., welded()

### Community 128 - "FormStore"
Cohesion: 0.18
Nodes (4): FormStore, An ordered, named collection of forms, like the other stores., A name for a new form of this recipe, numbered past any it already has. A form…, test_a_form_store_names_forms_past_the_ones_it_has()

### Community 129 - "SectionAxis"
Cohesion: 0.18
Nodes (7): Enum, str, The direction the section plane faces., Unit axis, or ``None`` for a custom direction., Which side of the plane survives the cut., SectionAxis, SectionMode

### Community 131 - "OverlayParts"
Cohesion: 0.18
Nodes (5): Which of the things drawn over the model belong in the frames., MarkerVisibility, Cache surface occlusion by view and position for every kind of marker., OverlayParts, Which of the things drawn over the model are wanted this time. The viewport…

### Community 132 - "ExportLook"
Cohesion: 0.08
Nodes (21): The stage at ``index``, clamped to what has actually been recorded., One moment in the making of a form. :attr:`solids` is how many blocks or lumps…, What to call this stage in the panel, under the scrub handle., Stage, ExportLook, What the frames are to look like, as against what they are of. Laid over the…, ``base`` with this export's choices laid over it., The line burned into the corner of the frame for ``stage``. Counted off the… (+13 more)

### Community 135 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 136 - "theme.py"
Cohesion: 0.13
Nodes (14): css(), A colour as a style sheet function, for the parts Qt draws., QObject, Making the whole of a switch the part you can press. The theme turns every…, Turns a press anywhere on a switch into a click on it., WholeFaceToggles, apply_dark_theme(), QApplication (+6 more)

### Community 137 - ".mouseMoveEvent"
Cohesion: 0.20
Nodes (4): Apply the drag live, so the artist sees the wire bend as they pull it., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Apply the drag live, so the clay re-forms under the cursor.

### Community 138 - "_height_of"
Cohesion: 0.40
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 139 - "SectionGizmo"
Cohesion: 0.22
Nodes (6): Centre, half-length and offset span of the rail, or ``None``., Handle position, drag axis in pixels per scene unit, and its direction., Whether ``(x, y)`` lands on the rail or its handle., SectionGizmo, ndarray, Rotate the measurements, annotations, armature and forms onto the turned model.…

### Community 140 - "_drag_over"
Cohesion: 0.22
Nodes (10): _drag_over(), _middle_of_the_view(), A drag of ``holder`` arriving at ``point`` in the window's coordinates. A real…, The gesture the whole thing rests on: drag it onto the model, it goes., A gesture that destroys something only fires where it clearly meant to., Refused at the door it would never reach the model; so it is let in., test_a_copy_dropped_on_the_model_is_thrown_away(), test_a_copy_is_let_into_the_window_wherever_it_arrives() (+2 more)

### Community 146 - "section"
Cohesion: 0.50
Nodes (4): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., section()

### Community 147 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 148 - "MeshBuffers"
Cohesion: 0.08
Nodes (15): bind_default(), current_framebuffer(), The framebuffer object bound right now -- Qt's, in a widget., Restore a framebuffer captured with :func:`current_framebuffer`., _ghost_depth_range(), MeshBuffers, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it. (+7 more)

### Community 149 - ".install"
Cohesion: 0.29
Nodes (6): QApplication, Put the rule in place for every switch in the application., The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter., test_a_switch_answers_a_press_anywhere_on_its_face(), test_alt_is_left_alone_so_a_switch_can_still_be_copied()

### Community 150 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 151 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 152 - "._built"
Cohesion: 0.33
Nodes (4): QImage, QRect, Where the sphere goes: square, centred, above the legend., The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…

### Community 153 - "PreferenceStore"
Cohesion: 0.16
Nodes (10): PreferenceStore, QObject, QSettings, _qcolor(), Push the preferences that something in the process holds a copy of.…, A core colour triple as the Qt colour the palette wants., The preferences, and one signal saying they have changed. A single instance,…, Adopt ``value``, push what has to be pushed, and say so. Always announces, even… (+2 more)

### Community 154 - "restored"
Cohesion: 0.29
Nodes (7): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., A second window, built from a layout the first one saved. The point is…, A window with the saved layout out of the way, and put back after. Shown,…, restored(), window()

### Community 162 - "Q: Where are the todo viewport marker and shading changes implemented?"
Cohesion: 0.40
Nodes (4): Answer, Outcome, Q: Where are the todo viewport marker and shading changes implemented?, Source Nodes

### Community 164 - "sample_count"
Cohesion: 0.50
Nodes (3): How many samples the framebuffer bound right now is drawing with. One where…, sample_count(), How many samples this view is really drawing with, or ``None``. Asked of GL…

### Community 167 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 168 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 171 - "palette.py"
Cohesion: 0.25
Nodes (7): outline(), QColor, The colours the hand-drawn elements paint with. Kept apart from…, Draw the hairline that separates a control from the panel. One line, the same…, Change the one colour that is not grey, everywhere at once. The hand-painted…, set_accent(), The slider the whole application is set with. One flat bar: the name of the…

### Community 173 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

## Knowledge Gaps
- **4 isolated node(s):** `refview`, `Answer`, `Outcome`, `Source Nodes`
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `FormStore`, `SectionAxis`, `plane_axes`, `ExportLook`, `mesh_renderer.py`, `SectionGizmo`, `README.md`, `ViewerState`, `PlaneSettings`, `MeshBuffers`, `SectionSettings`, `plane_volume.py`, `mesh.py`, `FilmRecorder`, `test_plane_clusters.py`, `gltf_loader.py`, `ExportVideoDialog`, `OrientationSettings`, `forms.py`, `test_forms.py`, `PrimaryForm`, `compute_vertex_normals`, `test_plane_solids.py`, `Bounds`, `raycast_mesh`, `MeshLoadError`, `core/__init__.py`, `test_mesh_io.py`, `welded`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `test_preferences.py`, `main_window.py`, `ExportLook`, `._place_form_landmark`, `MainWindow`, `.mouseMoveEvent`, `SectionGizmo`, `ViewerState`, `ViewportOverlay`, `FilmRecorder`, `sample_count`, `film_export.py`, `AnnotateTool`, `ExportVideoDialog`, `FilmExport`, `ArmatureTool`, `MeasureTool`, `PrimaryForm`, `.__init__`, `NavigationController`, `_Encoder`, `._picker`, `core/__init__.py`, `._upload_sculpt`, `.mouseReleaseEvent`, `._place_armature_node`, `._arm`, `.stage_images`?**
  _High betweenness centrality (0.104) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `test_preferences.py`, `main_window.py`, `OverlayParts`, `._forms_hud`, `form_group`, `MainWindow`, `._armature_hud`, `Viewport`, `SectionGizmo`, `README.md`, `section`, `panel`, `ViewportOverlay`, `test_planes_panel.py`, `ShadingPanel`, `test_matcap_preview.py`, `settings_window.py`, `OrientationSettings`, `MeasureTool`, `PrimaryForm`, `.__init__`, `test_custom_panels.py`, `MatcapPanel`, `test_elements.py`, `core/__init__.py`, `QPointF`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Are the 33 inferred relationships involving `Mesh` (e.g. with `DegenerateHullError` and `Solid`) actually correct?**
  _`Mesh` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `Camera` (e.g. with `BookmarkStore` and `CameraBookmark`) actually correct?**
  _`Camera` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `PrimaryForm` (e.g. with `PlacedLandmark` and `DegenerateHullError`) actually correct?**
  _`PrimaryForm` has 7 INFERRED edges - model-reasoned connections that need verification._