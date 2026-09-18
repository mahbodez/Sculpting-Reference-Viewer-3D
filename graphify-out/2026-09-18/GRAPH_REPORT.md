# Graph Report - reference-viewer  (2026-09-18)

## Corpus Check
- 164 files · ~518,243 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 5689 nodes · 13240 edges · 224 communities (201 shown, 23 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 677 edges (avg confidence: 0.59)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8a6aefb4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- SettingsWindow
- test_preferences.py
- update_check.py
- Viewport
- SceneObject
- core/__init__.py
- MainWindow
- Stroke
- GifWriter
- linalg.py
- SceneRenderer
- elements/__init__.py
- main_window.py
- MeshBuffers
- Armature
- environment.yml
- ViewerState
- Skeleton
- mesh_renderer.py
- CameraPanel
- PosePanel
- ShaderProgram
- PoseTool
- test_planes_panel.py
- MeasurePanel
- BookmarkStore
- Writer
- SectionAxis
- plane_volume.py
- ControlsWindow
- auto_skin
- ._apply
- PlaneSettings
- test_camera.py
- test_plane_clusters.py
- WakeLock
- ._built
- MatcapPreview
- CustomPanel
- film_export.py
- convex.py
- Camera
- autoskin.py
- ValueSlider
- Rig
- ExportVideoDialog
- open_writer
- _Build
- Agent Graph-First Instructions
- VideoSettings
- Mesh
- test_matcap_preview.py
- test_armature.py
- ._selected_landmark
- .refresh_list
- test_hotkeys.py
- FilmExport
- FormsPanel
- PlanesPanel
- test_skeleton.py
- Progress
- Workspace
- ui/hotkeys.py
- test_forms.py
- application.py
- MeasureTool
- Link
- FormTool
- plane_axes
- state.py
- test_skin.py
- test_plane_solids.py
- ObjectTool
- Session
- SurfacePicker
- texture.py
- load_matcap_pixels
- test_custom_panels.py
- SkinEdit
- core/preferences.py
- VideoError
- NavigationController
- ndarray
- ._commit_objects
- test_forms_panel.py
- solid_count
- test_viewport_markers.py
- PrimaryForm
- MatcapPanel
- ColorButton
- Frame
- _Encoder
- _derived
- test_elements.py
- WholeFaceToggles
- compute_vertex_normals
- ReflowLayout
- Measurement
- PointEdit
- OrientationSettings
- clone.py
- skin_detail.py
- Path
- ._turn
- SetAttributes
- test_panel_docks.py
- OverlayParts
- ._place_armature_node
- test_tasks.py
- GuideRun
- DockTitle
- test_reflow.py
- ._dress
- Task
- .render
- ._build_objects
- test_open_files.py
- ShadingPanel
- test_session.py
- AddItem
- ViewportOverlay
- ArmaturePanel
- ArmatureStore
- ._selected
- _tab_switch
- Reflow
- viewport.py
- SectionPanel
- ._upload_sculpt
- ._sync_scene
- .stage_images
- AnnotateTool
- ExportLook
- .__init__
- preview
- ._build
- paths.py
- Release
- watch_keys
- OpenRequests
- _drag_over
- PanelDock
- ._build
- matcap_preview.py
- ._picker
- ._carrying_a_copy
- .load
- app
- QComboBox
- .dress_tabs
- UpdateChecker
- test_resetting_the_layout_puts_the_docks_back_at_once
- .update_enabled
- skeleton.py
- restored
- test_resetting_keeps_the_panels_built_by_hand
- ._on_bone_toggled
- test_the_switch_is_not_squeezed_to_nothing
- shaders.py
- .paintGL
- write
- ProgressCard
- .column_of
- TaskRunner
- Human Skin renderer
- Command
- lumpy
- coarse_lattice
- ndarray
- sample_count
- _height_of
- _file_drag
- .refresh_list
- README.md
- ._active_changed
- panel
- raycast_mesh
- test_the_switch_on_a_dock_bar_is_the_panels_own_visibility
- ._add_skeleton
- app
- test_a_session_saved_without_panels_leaves_the_ones_open_alone
- test_a_panel_does_not_cover_its_own_title
- decode
- test_a_panel_can_be_taken_away_and_another_built_after_a_restore
- test_loading_a_session_over_a_restored_layout_survives
- test_the_dock_of_a_panel_taken_away_is_used_again
- ModelPanel
- Preferences
- navigation.py
- test_a_reused_dock_does_not_bring_the_old_panels_contents_with_it
- .reset
- release.yml
- ._refresh_cursor
- bent_plate
- _clone_preview
- ._build_menus
- generate_matcaps.py
- .new_armature
- _fill
- ._place_joint
- ._place_form_landmark
- box
- .with_landmark_at
- .update_enabled
- TaskBanner
- step
- _drop_on
- .point
- .new_custom_panel
- _create_splash
- _Worker
- .point_for
- _clamp
- _segment_distance
- .form
- _NameOnlyDelegate
- .cancel
- section
- .pending
- test_a_copied_slider_brings_its_caption_inside_itself
- test_a_control_with_nothing_written_on_it_gets_a_caption
- test_an_attribute_beats_a_group_title_to_a_name
- test_a_matcap_folder_that_has_gone_falls_back_to_the_bundled_ones
- test_the_window_follows_a_change_it_did_not_make

## God Nodes (most connected - your core abstractions)
1. `Mesh` - 218 edges
2. `ViewerState` - 161 edges
3. `Viewport` - 151 edges
4. `Skeleton` - 112 edges
5. `MainWindow` - 99 edges
6. `Camera` - 97 edges
7. `Armature` - 81 edges
8. `PrimaryForm` - 79 edges
9. `SceneObject` - 74 edges
10. `PlaneSettings` - 69 edges

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
- 3-file cycle: `src/refview/ui/elements/__init__.py -> src/refview/ui/elements/clone.py -> src/refview/ui/elements/slider.py -> src/refview/ui/elements/__init__.py`
- 4-file cycle: `src/refview/ui/elements/__init__.py -> src/refview/ui/elements/custom.py -> src/refview/ui/elements/clone.py -> src/refview/ui/elements/slider.py -> src/refview/ui/elements/__init__.py`

## Hyperedges (group relationships)
- **The bundled matcap set** — resources_matcaps_clay_terracotta_matcap, resources_matcaps_charcoal_matcap, resources_matcaps_jade_matcap, resources_matcaps_steel_matcap, resources_matcaps_studio_white_matcap, resources_matcaps_wax_skin_matcap, tools_generate_matcaps_matcappreset, tools_generate_matcaps_render [INFERRED 0.85]
- **The four generic undo commands** — src_refview_core_commands_setattributes, src_refview_core_commands_additem, src_refview_core_commands_removeitem, src_refview_core_commands_replaceitems, src_refview_core_history_command, readme_every_edit_is_a_command [EXTRACTED 1.00]
- **Windows binary-compatibility decisions** — readme_pyside6_pinned_below_68, environment_pip_installed_binaries, environment_python_311, github_workflows_release_pyinstaller_build [INFERRED 0.75]

## Communities (224 total, 23 thin omitted)

### Community 0 - "SettingsWindow"
Cohesion: 0.06
Nodes (35): Reference Viewer 3D -- a matcap-shaded OBJ, STL and glTF viewer for sculpting., Read the version from ``pyproject.toml``, bundled or in the source checkout., _read_version(), current(), forget(), PreferenceStore, QObject, QSettings (+27 more)

### Community 1 - "test_preferences.py"
Cohesion: 0.12
Nodes (19): app(), model(), fixture, What the artist prefers: kept apart from the document, and acted upon. Two…, One triangle, which is a mesh as far as any of this is concerned., Windows that clean up after themselves, and a settings file that does., A session is not the only thing worth carrying on from., Otherwise the marks from one piece of work arrive on top of another. (+11 more)

### Community 2 - "update_check.py"
Cohesion: 0.10
Nodes (31): check_for_update(), fetch_latest_release(), is_newer(), _macos_root_certificates(), _padded(), parse_version(), RuntimeError, Ask GitHub whether a newer release exists. The check is deliberately small and… (+23 more)

### Community 3 - "Viewport"
Cohesion: 0.06
Nodes (15): QOpenGLWidget, One of the renderer's :data:`~refview.render.mesh_renderer.ANTIALIASING_MODES`., Renders the scene and turns mouse gestures into camera and tool actions., Slide the view so a point sits at the centre, keeping the angle., The gesture a key press chooses, if the transform tool is armed to hear it., A form changed: work its clay out again and redraw., Hand the renderer how solid each object is now; nothing else moved., End any film being recorded, and wait for its thread to really stop. For… (+7 more)

### Community 4 - "SceneObject"
Cohesion: 0.06
Nodes (22): ObjectSettings, ObjectStore, ndarray, Path, Snapshot, What a parent's state means for its children, and how the tools scale. Each is…, One model in the scene. Three meshes are kept, as the viewer kept them when…, The centred mesh carried by ``matrix`` -- the mesh itself for the identity. (+14 more)

### Community 5 - "core/__init__.py"
Cohesion: 0.03
Nodes (92): Shift-snapped orbiting (1.1.0), High Quality shading mode (1.1.0), High Quality without ray tracing, The pedestal is ordinary geometry so it catches the shadow, Move the camera so ``bounds`` fills the view, keeping the direction., Point the camera along ``direction``, measured object-to-eye., build_grid(), GridLines (+84 more)

### Community 6 - "MainWindow"
Cohesion: 0.06
Nodes (14): MainWindow, QMainWindow, Put every panel button and menu entry where the tools now stand. Only one tool…, Swap between the eraser and the drawing mode it was called from., Open an empty panel of the artist's own and bring it to the front., Put the panels back where they started, now., Follow the machine's sleep to whether this window is in front., Keep the banner over the view as the docks push the view about. (+6 more)

### Community 7 - "Stroke"
Cohesion: 0.06
Nodes (37): AnnotationStore, ndarray, Half-open index ranges of the contiguous ``True`` regions of ``mask``., An ordered collection of strokes, oldest first., The live list; the undo commands operate on it directly., Strokes with the points within ``radius`` of ``center`` rubbed out. Returns…, One painted polyline lying on the surface., Normals padded to match the points, so callers can zip them freely. (+29 more)

### Community 8 - "GifWriter"
Cohesion: 0.07
Nodes (32): _bayer(), _blocks(), GifWriter, _indices(), _lookup(), lzw(), palette_of(), ndarray (+24 more)

### Community 9 - "linalg.py"
Cohesion: 0.04
Nodes (66): Quat, Quat4, Named camera positions the artist can jump between while sculpting., _distance_or_none(), Projection, Enum, str, Interactive camera model driving both perspective and orthographic views. (+58 more)

### Community 10 - "SceneRenderer"
Cohesion: 0.07
Nodes (37): Everything the viewport needs in order to draw a frame., How solid the model is drawn, 1.0 unless it is being ghosted., RenderSettings, key_world_direction(), light_directions(), light_view_projection(), normal_matrix(), ndarray (+29 more)

### Community 11 - "elements/__init__.py"
Cohesion: 0.05
Nodes (54): Make every control under ``root`` that can be copied Alt-draggable. A group is…, watch_tree(), The small controls that are not sliders: a swatch, and a point in space., A panel the artist builds, out of copies of controls from the fixed ones. The…, make_switch(), QCheckBox, One dock per panel, with a bar of its own across the top. Every panel is its…, Put a show/hide switch at the left of the bar and return it. (+46 more)

### Community 12 - "main_window.py"
Cohesion: 0.04
Nodes (73): QIcon, QScrollArea, Command, The handful of undoable edits the whole application is built from.…, Delete the item at ``index``, putting it back in place on undo., Swap the whole contents of a document list. Used for bulk edits -- clearing the…, RemoveItem, ReplaceItems (+65 more)

### Community 13 - "MeshBuffers"
Cohesion: 0.09
Nodes (12): _ghost_depth_range(), MeshBuffers, Forget the contents without releasing the buffer objects., Where the form starts along the view, and how deep it is. The ghost weighs a…, Replace the model: the whole scene as one mesh, and the objects it is made of.…, Draw ``mesh`` in place of the model; pass ``None`` to draw the model. The…, Replace the ground disc; pass ``None`` to hide it., Replace the clay of the primary forms; pass ``None`` to hide it. The forms are… (+4 more)

### Community 14 - "Armature"
Cohesion: 0.05
Nodes (49): Armature, ArmatureNode, Bone, The end that is not ``index``., A graph of nodes and the bones joining them. When it came from a preset the…, The two points a bone runs between, or ``None`` if it dangles., The longest bone, falling back to the span of the nodes themselves., A plausible thickness for a node placed by hand. (+41 more)

### Community 15 - "environment.yml"
Cohesion: 0.40
Nodes (5): numpy, PySide6 and PyOpenGL installed with pip, Python 3.11 from conda-forge, refview conda environment, refview, PySide6 pinned below 6.8

### Community 16 - "ViewerState"
Cohesion: 0.08
Nodes (20): Take the display unit from the file when the format declares one. Only glTF…, Set the active matcap, or fall back to the built-in one., Fit the scene in the view without changing the direction., Adopt a session's settings, leaving the loaded meshes alone., Everything the viewer displays, plus change notifications., The skeletons changed; re-pose the model if one of them drives it. ``live`` is…, Emit the change signal a command's channel maps onto., The skeleton bound to ``obj``'s rig, if one is and no other object has it. (+12 more)

### Community 17 - "Skeleton"
Cohesion: 0.06
Nodes (30): Joint, _matrix16(), _pose_matrices(), ndarray, Whether the pose differs from the rest at all., A copy with the rest translation replaced and the frame kept., A tree -- or a forest -- of joints and the pose they stand in., Every joint, parents before children. A file may list a child before its… (+22 more)

### Community 18 - "mesh_renderer.py"
Cohesion: 0.05
Nodes (31): AccumTarget, bind_default(), ColorTarget, current_framebuffer(), DepthTarget, FrameTarget, GeometryTarget, Offscreen render targets used by the high-quality, ghost and smoothing passes.… (+23 more)

### Community 19 - "CameraPanel"
Cohesion: 0.10
Nodes (9): CameraPanel, QListWidgetItem, Take the planes in hand where the fit left them, or hand them back., Update the projection controls only. The camera changes on every frame of an…, Start editing the selected view's name in place., Jump to a stored view by index., Step to the next or previous stored view, wrapping around., Edits the projection and manages the saved camera positions. (+1 more)

### Community 20 - "PosePanel"
Cohesion: 0.08
Nodes (12): PosePanel, The skeleton the panel is about: the selected row's, else the last., Highlight the row for a joint picked in the view., Run a row's edit once Qt has finished delivering the current signal., Arms the pose tool, lists the joints and poses the selected one., Adopt the viewport's tools: the pose tool, and the armature's for its selection., Lay an armature under the selected skeleton as it is posed., Take the detail joints out of the current skeleton; returns how many went. (+4 more)

### Community 21 - "ShaderProgram"
Cohesion: 0.14
Nodes (7): ndarray, RuntimeError, Raised when a shader fails to compile or link., Upload a row-major numpy 4x4, transposing for GL's column-major., Compiles a vertex/fragment pair and caches its uniform locations. Uniform…, ShaderError, ShaderProgram

### Community 22 - "PoseTool"
Cohesion: 0.08
Nodes (39): JointRef, How skeletons are drawn, and how the pose tool behaves., SkeletonSettings, PoseTool, _project_many(), The nearest unlocked joint of a visible skeleton under the cursor., The bone under the cursor, named by the joint at its far end. Taking hold of a…, The pose shift that puts joint ``index`` at ``target``, children and all. (+31 more)

### Community 23 - "test_planes_panel.py"
Cohesion: 0.08
Nodes (21): _names(), The Planes panel, where the clay is told which armature to build on. Most of…, It is a reordering of the making, not a structural edit, so an armature derived…, The question in front of this list is what one more step of Detail would buy,…, A session saved with two wires and reopened with one has to come back as…, Or there would be no way to turn one back on., A limb is four bones, and deciding not to block the arms in is one decision.…, It is rebuilt on every change, and ticking one row of a selected limb would be… (+13 more)

### Community 24 - "MeasurePanel"
Cohesion: 0.12
Nodes (9): MeasurePanel, QTreeWidgetItem, Reflect the tool state without re-emitting the toggle., Rebuild the tree from the store, preserving the selected row., Commit a renamed or re-checked row, if anything actually changed., Run a row's edit once Qt has finished delivering the current signal. Committing…, Lock or unlock one measurement, making its endpoints draggable., Lists saved measurements and controls how they are drawn. (+1 more)

### Community 25 - "BookmarkStore"
Cohesion: 0.11
Nodes (9): BookmarkStore, CameraBookmark, A camera pose stored under a name., An ordered list of :class:`CameraBookmark` with cycling support., Index of the most recently recalled bookmark, or ``-1``., Mark a bookmark as the one cycling continues from., Return the pose at ``index`` and remember it as the current one., Step forwards or backwards through the list, wrapping around. (+1 more)

### Community 26 - "Writer"
Cohesion: 0.18
Nodes (7): ndarray, What an export needs of whatever is doing the encoding., Offered the last frame before the first is written, if it helps., Write one frame, held for ``seconds``., Give up, leaving nothing half-written behind., Nothing to do: ffmpeg reads the whole stream before it decides., Writer

### Community 27 - "SectionAxis"
Cohesion: 0.18
Nodes (7): Enum, str, The direction the section plane faces., Unit axis, or ``None`` for a custom direction., Which side of the plane survives the cut., SectionAxis, SectionMode

### Community 28 - "plane_volume.py"
Cohesion: 0.04
Nodes (111): _axes(), _back_inside(), _balloon(), Bed, block_bounds(), block_field(), block_labels(), block_splits() (+103 more)

### Community 29 - "ControlsWindow"
Cohesion: 0.22
Nodes (6): ControlsWindow, QWidget, The window the controls reference is read in. It was a message box, which is…, A scrolled, searchable page of prose., Find the next occurrence, wrapping round the end., Open the controls reference. A message box was the wrong container for this: it…

### Community 30 - "auto_skin"
Cohesion: 0.12
Nodes (37): auto_skin(), AutoSkin, AutoSkinError, bone_segments(), ValueError, Skin ``mesh`` to ``skeleton``, both given in the same coordinates. The skeleton…, ``names`` with any repeat numbered, since the skin matches joints by name., Every bone as ``(start, end)`` points, and which joint each belongs to. A joint… (+29 more)

### Community 31 - "._apply"
Cohesion: 0.21
Nodes (6): Slot that writes one field of the light settings., Slot that writes one field of the surface settings., Slot that writes one field of the high-quality settings., Slot that writes one field of the pedestal settings., Slot that writes one field of the contour shading settings., Slot that writes one field of the grid settings.

### Community 32 - "PlaneSettings"
Cohesion: 0.03
Nodes (61): QThread, Film, The stage at ``index``, clamped to what has actually been recorded., A whole making, from the coarsest stage to the one the slider asks for. Held by…, _along(), lattice_fineness(), plane_count(), PlaneSettings (+53 more)

### Community 33 - "test_camera.py"
Cohesion: 0.12
Nodes (7): camera(), fixture, parametrize, Camera behaviour: framing, projection round trips and the navigation gestures., A drag applies many small steps, and the pivot barely moves on screen. It is…, test_orbit_keeps_the_pivot_under_the_cursor(), test_zoom_keeps_the_anchor_under_the_cursor()

### Community 34 - "test_plane_clusters.py"
Cohesion: 0.12
Nodes (31): The joint list with ``index`` resting at ``target`` and its children left be., cube(), parametrize, Fitting planes to a model's surface rather than only to its normals. What…, The one form whose planes are not a matter of opinion., The reason for reading where the surface is and not only which way. Both faces…, Merging back from patches is a hierarchy, so the cuts of it nest. This is what…, Every plane of a level as a hashable whole: direction, place and offset. (+23 more)

### Community 35 - "WakeLock"
Cohesion: 0.05
Nodes (32): c_void_p, _Backend, _MacBackend, _platform_backend(), Keeping the machine awake while the viewer is the window in front. An artist…, The freedesktop screensaver service, which hands back a cookie., The backend for this machine, or a do-nothing one if it cannot be had., Holds sleep off while the window that owns it is the one in front. The class… (+24 more)

### Community 36 - "._built"
Cohesion: 0.33
Nodes (4): QImage, QRect, Where the sphere goes: square, centred, above the legend., The graded disc at ``side`` pixels, rebuilt only when it has to be. A drag…

### Community 37 - "MatcapPreview"
Cohesion: 0.09
Nodes (14): QMenu, MatcapPreview, Path, QSize, QWidget, A matcap on a sphere, which is also how the matcap is graded., Offer the picture back as a file: as graded here, or as it came. A grading…, The matcap as a picture, at its own resolution. Square and opaque, with the… (+6 more)

### Community 38 - "CustomPanel"
Cohesion: 0.09
Nodes (21): carried(), Read a drag's payload back, or ``None`` if it is not one of ours., CustomPanel, _detach(), QFormLayout, QWidget, Take a copy out of this panel and destroy it., Move a copy already in a panel to a new place in this one. ``frame`` and… (+13 more)

### Community 39 - "film_export.py"
Cohesion: 0.09
Nodes (17): Enum, str, Quality, Turning a sequence of rendered frames into a file someone can play. A film of a…, What an artist should know before picking this one., How hard the encoder is asked to work at keeping the picture., H.264's constant-rate factor, where lower keeps more., MPEG-4's quantiser, 1 (best) to 31. (+9 more)

### Community 40 - "convex.py"
Cohesion: 0.12
Nodes (22): convex_hull(), flat_mesh(), _outward(), _patch_samples(), ndarray, Convex solids from points: the hull, a cut through it, and its mesh. A primary…, The outward unit normal at each vertex: the area-weighted mean of its faces'. A…, The barycentric ``(w, u, v)`` of an even grid over a triangle. (+14 more)

### Community 41 - "Camera"
Cohesion: 0.07
Nodes (30): Camera, ndarray, Near/far planes fitted to the scene bounding sphere., The near and far planes this frame: the fitted ones, unless set by hand. A…, Ray through a pixel, as ``(origin, unit direction)``. ``x``/``y`` are Qt widget…, Rays through a batch of pixels, as ``(origins, unit directions)``, ``(N, 3)``…, Project a world point to ``(x, y, ndc_depth)`` in widget pixels., Project ``(N, 3)`` world points to ``(xs, ys, ndc_depths)`` in widget pixels. (+22 more)

### Community 42 - "autoskin.py"
Cohesion: 0.10
Nodes (27): _baked_rest(), _conjugate_gradients(), _CotLaplacian, _envelope_weights(), _Graph, _heat_weights(), _joint_distances(), _nearest_weights() (+19 more)

### Community 43 - "ValueSlider"
Cohesion: 0.07
Nodes (11): _pull_slider(), QSize, QWidget, Re-scale the bar, e.g. once a model's size is known., Put the bar at a value without telling anyone it moved., Grow the bar to take in a value from beyond its end., Set the value the way a hand on the control would., The value the track stands at ``x`` pixels across. (+3 more)

### Community 44 - "Rig"
Cohesion: 0.06
Nodes (50): Units are adopted, never guessed, _accessor(), _buffers(), _first_skin(), GltfLoadError, load_gltf(), _local_transform(), _primitive_geometry() (+42 more)

### Community 45 - "ExportVideoDialog"
Cohesion: 0.09
Nodes (13): even(), ExportVideoDialog, Path, QDialog, QWidget, ``value`` rounded down to a multiple of four. Two would do for H.264, which…, Where an artist says how the film should be written out. Everything on the…, What the frames are to look like, as the controls have it. (+5 more)

### Community 46 - "open_writer"
Cohesion: 0.13
Nodes (16): ffmpeg_path(), open_writer(), Path, Where ffmpeg is, or ``None``. Looked for in the order of how deliberate each…, Why ``format`` cannot be written here, or ``None`` if it can., Start an encoder for ``settings``, or say why there cannot be one., unavailable(), frames() (+8 more)

### Community 47 - "_Build"
Cohesion: 0.19
Nodes (14): _Build, _build_arm(), _build_leg(), _build_torso(), _humanoid_bones(), _mid(), ndarray, Somewhere to collect nodes while the rules that need each other run. (+6 more)

### Community 48 - "Agent Graph-First Instructions"
Cohesion: 0.50
Nodes (3): Query the graph before reading source, Run graphify update after modifying code, Copilot: graph-first repo questions

### Community 49 - "VideoSettings"
Cohesion: 0.18
Nodes (7): How long the film runs and what it is written as. Everything here is about time…, One stage's hold, in whole milliseconds. The encoders are driven off this…, How many input frames the stage at ``index`` of ``count`` takes. One, except…, How long the stage at ``index`` of ``count`` is held for., How long the whole film runs, in seconds., VideoSettings, TestTiming

### Community 50 - "Mesh"
Cohesion: 0.03
Nodes (106): auto_smooth(), _gathered(), Mesh, Triangle-mesh containers shared by the loader, the renderer and picking., Which group each of ``total`` things lands in, given pairs that agree. Hooking…, A copy of ``mesh`` shaded smooth across every edge gentler than ``degrees``.…, An indexed triangle mesh with per-vertex positions and normals. The viewer…, Coefficients (+98 more)

### Community 51 - "test_matcap_preview.py"
Cohesion: 0.12
Nodes (28): QPoint, _drag(), parametrize, The matcap as its own control, and whether it tells the truth. The disc is only…, Positive rotation moves a feature clockwise, which is the way a drag goes.…, The picture follows the hand, which is the whole reason for the disc., Dragging further than the range goes is not a negative gamma., Alt and a drag copies a control; the disc must not swallow that. (+20 more)

### Community 52 - "test_armature.py"
Cohesion: 0.07
Nodes (56): build_humanoid(), Turn placed landmarks into a figure's armature. Anything whose landmarks are…, _chain(), _figure(), ndarray, The armature graph, the humanoid landmarks and the joints they infer., Every plane through a straight line is as good as every other., The femoral head is in from the ASIS, below it and behind it, by shares of the… (+48 more)

### Community 53 - "._selected_landmark"
Cohesion: 0.12
Nodes (7): Record an edited landmark list, re-deriving the wire if it still follows. An…, Put the nodes back under the preset the landmarks describe., The mirrored landmarks reflected from ``key``, which it anchors., Show the landmark group only once there are landmarks to show., The landmark the highlighted row stands for, if the row is one., Which armature the landmark list is pointing into, row or heading., Follow the highlighted landmark, and say which one it is in the view.

### Community 54 - ".refresh_list"
Cohesion: 0.22
Nodes (5): QTreeWidgetItem, The landmarks in the preset's own order, top of the figure down. Placement…, Rebuild the tree from the store, keeping the tool's selection shown. A node…, Rebuild the landmark list, keeping the row the panel is editing., Commit a renamed or re-checked row, if anything actually changed.

### Community 55 - "test_hotkeys.py"
Cohesion: 0.04
Nodes (47): QKeySequence, Command, HotkeyMap, Any, Which keys do what, as the artist has decided rather than as it ships. A hotkey…, Whether the artist has moved this command off what it ships with., Which command has these keys, if any., Every command with keys on it, declared or not, as id -> keys. (+39 more)

### Community 56 - "FilmExport"
Cohesion: 0.13
Nodes (11): FilmExport, frame_bytes(), QImage, An image's pixels, packed tight, whatever padding Qt left on its rows. Qt pads…, One export, rendered from the event loop and encoded behind it. The renderer…, Open the file and begin. Any failure here is reported, not raised., Stop where it is and leave no half-written file behind., Let the encoding thread finish, for shutdown. It calls off an export still in… (+3 more)

### Community 57 - "FormsPanel"
Cohesion: 0.04
Nodes (36): FormsPanel, QPushButton, QTreeWidgetItem, QWidget, A strip of buttons that one form row can show or hide as a unit., Arms the forms tool, runs the guided presets and lists what they built., Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle. (+28 more)

### Community 58 - "PlanesPanel"
Cohesion: 0.18
Nodes (6): PlanesPanel, Put the design matrix back the way it reads a figure., Size the scrub slider to the film as it is recorded. The stages arrive one at a…, The line under the scrub handle: which stage, and of how many., Breaks the form into planes, in the shading or in the geometry itself., Re-read the armatures and what the chosen one is laying down. Called whenever…

### Community 59 - "test_skeleton.py"
Cohesion: 0.06
Nodes (61): build_humanoid_skeleton(), detail_joints(), humanoid_positions(), humanoid_roles(), looks_humanoid(), ndarray, Where skeletons come from: an armature, a preset, or the names in a file. Three…, Every humanoid role's place for a figure this tall standing on ``feet``. (+53 more)

### Community 60 - "Progress"
Cohesion: 0.08
Nodes (22): Exception, CancelledError, Progress, What a long piece of work says about itself while it runs, and how it is…, Ask the work to stop at its next report., How far along, 0 to 1, or ``None`` when the work has not said., Whether the work has said how much there is to do., A window onto part of a parent's range; see :meth:`Progress.slice`. (+14 more)

### Community 61 - "Workspace"
Cohesion: 0.14
Nodes (8): QMainWindow, QObject, QWidget, Keep every switch agreeing with the panel it speaks for., Dress the tabs once Qt has finished rearranging them., Open the dock a hand-built panel lives in and bring it to the front., The docks of one window: the fixed panels and the ones built by hand., Workspace

### Community 62 - "ui/hotkeys.py"
Cohesion: 0.05
Nodes (56): QKeySequenceEdit, QShortcut, ask_for(), assign(), command_for(), control_of(), decorate(), describe() (+48 more)

### Community 63 - "test_forms.py"
Cohesion: 0.05
Nodes (81): DegenerateHullError, merged(), ValueError, One convex piece of a form: its hull vertices and outward-wound faces., The hull of the points with its faces bowed out; see :func:`rounded_hull`., The longest side of the box the solid sits in., Whether a point lies inside, or within ``slack`` of the surface., Several flat meshes as one, or ``None`` when there is nothing to draw. (+73 more)

### Community 64 - "application.py"
Cohesion: 0.18
Nodes (12): ArgumentParser, Namespace, _apply_startup_arguments(), build_parser(), main(), Command-line entry point and application bootstrap., Open whatever the command line asked for, falling back to sane defaults., Start the viewer and block until the window closes. (+4 more)

### Community 65 - "MeasureTool"
Cohesion: 0.12
Nodes (10): MeasureTool, Handle, ndarray, The nearest grabbable endpoint under the cursor, if any. Only unlocked, visible…, Consume a picked point; returns a measurement on the second click., Length of the rubber band currently being dragged out, if any., Picks points and turns pairs of them into measurements. The tool stays armed…, Drop the half-finished measurement and the hover preview. (+2 more)

### Community 66 - "Link"
Cohesion: 0.12
Nodes (9): CloneGesture, Link, _Pulse, QObject, One timer for every copy in the window., Holds a copy to the control it was copied from. Parented to the copy, so it…, Bring the copy up to date with its original., Whether the copy is being used right now and must not be written. (+1 more)

### Community 67 - "FormTool"
Cohesion: 0.06
Nodes (31): FormLandmarkRef, FormSettings, How the forms are drawn, and how their landmarks are placed., FormRun, FormTool, ndarray, Begin a run against a form already in the store., Every landmark the walk will ask for under these choices. With mirroring on,… (+23 more)

### Community 68 - "plane_axes"
Cohesion: 0.11
Nodes (29): plane_axes(), Split the mesh's normals into planes, keeping every count on the way., cube(), ndarray, Fitting planes to a model's own normals. The properties that matter are not…, Sampling is strided, not random, so a session reopens looking the same., Asking a flat plate for eight planes gets its one, not eight copies., The renderer reads an empty set as "leave the normals alone". (+21 more)

### Community 69 - "state.py"
Cohesion: 0.07
Nodes (48): concatenated(), loose_parts(), Several meshes as one, in the coordinates they already stand in. The units are…, The triangles of ``mesh`` named by index, with only the vertices they use., The triangles of ``mesh`` gathered into the pieces that touch, largest first.…, submesh(), _bare(), duplicate_object() (+40 more)

### Community 70 - "test_skin.py"
Cohesion: 0.10
Nodes (23): build_scene(), ndarray, Stackless BVH tables for the OpenGL 3.3 skin tracer (no compute extension).…, Build on a worker from the immutable meshes currently drawn by the renderer., Pack a linear texel array within the driver's actual 2D texture limit., texture_table(), TraceScene, gl_context() (+15 more)

### Community 71 - "test_plane_solids.py"
Cohesion: 0.03
Nodes (148): plane_regions(), Break the surface into patches and merge them back into planes., A stand-in for ``mesh`` blocked in out of ``planes``, worked from one side. The…, sculpt_mesh(), film_of(), parametrize, Scrubbing through the making of a form, rather than only arriving at it. The…, A cut takes material away, so no stage of a carving is larger than the one… (+140 more)

### Community 72 - "ObjectTool"
Cohesion: 0.12
Nodes (14): _axis_param(), Gizmo, _Grip, ObjectTool, ndarray, The three directions the arms run along, in world space. A move and a turn are…, Where the gizmo for an object at ``world`` falls on screen, or ``None`` if…, Which handle a screen point is over: ``"centre"``, ``"x"``, ``"y"``, ``"z"`` or… (+6 more)

### Community 73 - "Session"
Cohesion: 0.07
Nodes (32): ObjectRecord, What a session writes down about an object; the mesh itself stays in its file., The store as a session writes it: parents by index into the same list., records_for(), Path, A snapshot of everything worth keeping between runs., Session file that sits beside a model, e.g. ``bust.refview.json``., Session (+24 more)

### Community 74 - "SurfacePicker"
Cohesion: 0.05
Nodes (46): BoneRef, LandmarkRef, ArmatureSettings, How the armature is drawn, and how new nodes are placed., ArmatureTool, _project(), Handle, The landmarks still to place, in order, the current one first. (+38 more)

### Community 75 - "texture.py"
Cohesion: 0.08
Nodes (19): OpenGL rendering layer: shader programs, textures and the scene renderer., DataTexture, default_matcap_pixels(), MatcapLoadError, ndarray, RuntimeError, Matcap texture loading and upload, and the small data table beside it., An RGBA16F 2D texture with clamped edges and mipmapped minification. (+11 more)

### Community 76 - "load_matcap_pixels"
Cohesion: 0.31
Nodes (13): Charcoal matcap, Terracotta clay matcap, Jade matcap, Steel matcap, Studio white matcap, Wax skin matcap, load_matcap_pixels(), Path (+5 more)

### Community 77 - "test_custom_panels.py"
Cohesion: 0.10
Nodes (12): app(), custom(), fixture, Panels the artist builds, and putting them back next time. A hand-built panel…, A panel reorganised between versions loads with a gap, not an error., A group is not a row, so it goes ahead of the group it was dropped on., One offscreen Qt application for the run; see test_film_recorder., A check box already carries its words; a caption beside it repeats them. (+4 more)

### Community 78 - "SkinEdit"
Cohesion: 0.11
Nodes (10): Command, ndarray, Dressing an object in a skin made for a skeleton, or taking it off. One step…, Run an edit through the history so it can be undone. ``apply=False`` records a…, Dress ``obj`` in a skin made for ``skeleton``, as one undo step. ``made`` came…, Take a skin made here off ``obj``; the skeleton keeps its joints., The 4x4 that carries a point of the file mesh onto the rest mesh. The rest mesh…, The 4x4 that takes a point on the old rest mesh onto the new one. A point sits… (+2 more)

### Community 79 - "core/preferences.py"
Cohesion: 0.20
Nodes (9): FolderPreferences, InterfacePreferences, NavigationPreferences, What the artist prefers, as distinct from what the document says. There are two…, What happens between the icon being clicked and the window arriving., Where the artist's own material is kept. One entry so far, and the one that…, How the application looks and how much of it folds away., How much camera a gesture buys. Nothing here changes what the gestures are,… (+1 more)

### Community 80 - "VideoError"
Cohesion: 0.13
Nodes (13): _encode_arguments(), _encoders(), _FFmpegWriter, _no_window(), RuntimeError, An export that could not be written, said in words for the artist., Which encoders this ffmpeg was built with. Asked once, because a build without…, Keep a console window from flashing up on Windows for each ffmpeg call. (+5 more)

### Community 81 - "NavigationController"
Cohesion: 0.10
Nodes (12): NavigationController, Orbit in whole increments of ``step`` degrees from the drag's start., Degrees of yaw per pixel, signed by whether the drag is inverted., The per-notch multiplier, scaled about 1 rather than multiplied. Zoom is…, Tracks an in-progress drag and applies it to a camera., Apply the motion since the previous event. Returns ``True`` if moved., How a drag turns into camera motion, so the preferences can set it., test_panning_ignores_the_snap_angle() (+4 more)

### Community 82 - "ndarray"
Cohesion: 0.18
Nodes (5): ndarray, Expanded triangle corners, shape ``(T, 3, 3)``., Return a copy turned by a 3x3 rotation, e.g. to fix the up axis. Rotations…, Return a copy carried by a full 4x4 -- a move, a turn and a scale together.…, Return a copy whose bounding-box centre sits at the origin.

### Community 83 - "._commit_objects"
Cohesion: 0.08
Nodes (18): ObjectsEdit, Snapshot, Re-read how solid each part is drawn, without touching the geometry., An edit to the objects -- a move, a parenting, a removal -- as two snapshots.…, Where everything stands now; the start of a gesture keeps one., Move each bound skeleton by however far its object moved since ``before``., Put the objects back as a snapshot had them -- how a gesture is cancelled., Record the list as it is now against ``before``, and rebuild. ``geometry`` off… (+10 more)

### Community 84 - "test_forms_panel.py"
Cohesion: 0.12
Nodes (29): app(), _click(), panel(), _pending(), _pick(), _place_all(), fixture, The Forms panel: the guided run it drives, and the document it writes. The… (+21 more)

### Community 85 - "solid_count"
Cohesion: 0.15
Nodes (15): block_count(), piece_count(), How many blocks a count of planes asks the stone to be cut into. One at the…, How many lumps a count of planes asks the clay to be built out of. The masses…, How many solids the form is made of, whichever way it is being worked., solid_count(), The line under the geometry slider: how the form is being worked. ``wires`` is…, _sculpt_summary() (+7 more)

### Community 86 - "test_viewport_markers.py"
Cohesion: 0.06
Nodes (34): DepthDrag, draw_rail(), Shared marker appearance, visibility, and constrained depth gestures., A grid across the depth axis, at the depth the point has reached. Returns…, One marker object for endpoints, nodes, landmarks and tool previews., The screen-space cue for one degree of freedom. A vertical rail that fades out…, A fixed world axis through the grabbed point; upward drags go deeper., VisualMarker (+26 more)

### Community 87 - "PrimaryForm"
Cohesion: 0.05
Nodes (58): PlacedLandmark, One anatomical point the artist put on the model during a guided run., build_form(), built_count(), form_mesh(), FormStore, landmark_signature(), median_plane_ready() (+50 more)

### Community 88 - "MatcapPanel"
Cohesion: 0.15
Nodes (9): MatcapPanel, Rebuild the thumbnail list from the resources folder., The disc was dragged: show the renderer and the numbers what it did., A different matcap: the disc draws whichever one is on the model., Put the numbers back in line with the settings, and redraw the disc. Separate…, Picks the matcap image and tunes how it is sampled., It is the panel's main control; a click on a bar must not take it away., test_the_disc_draws_the_matcap_that_is_on_the_model() (+1 more)

### Community 89 - "ColorButton"
Cohesion: 0.09
Nodes (10): _pull_swatch(), _push_swatch(), ColorButton, QColor, QSize, A swatch that opens a colour picker. Colours are exchanged as 0-1 RGB tuples,…, Open the picker, as a click on the swatch does., AnnotatePanel (+2 more)

### Community 90 - "Frame"
Cohesion: 0.09
Nodes (13): _pull_frame(), _push_frame(), Nothing: each row inside the copy is linked on its own., Frame, FrameBar, QPainter, QSize, QWidget (+5 more)

### Community 91 - "_Encoder"
Cohesion: 0.25
Nodes (5): Queue, _Encoder, QObject, The encoding itself, living on a thread of its own. It takes frames off a short…, Abandon the file. Called from the GUI thread; see :meth:`run`.

### Community 92 - "_derived"
Cohesion: 0.10
Nodes (24): _kept_laying(), Fresh bones, laid the way the armature was already laying them. The bone list…, The nodes and bones an armature's landmarks now imply. A node's name and…, rebuild(), _derived(), A guess the artist corrects is theirs, and the mirror leaves it alone., The new list is the edit; the old one has to survive to be undone to., Hips, then the ribcage, then the head, then the limbs largest first. This order… (+16 more)

### Community 93 - "test_elements.py"
Cohesion: 0.11
Nodes (13): Copies of controls: what they drive, and what keeps them honest. The contract a…, The original changed without saying so; the copy catches up anyway., A panel taken apart underneath a copy must not take the window with it., Controls that cannot be used take the room of controls that can., Folding is not a lock: switching it on again restores what was there., Run the refresh the shared timer would have run., test_a_copy_follows_the_original_on_the_tick(), test_a_copy_goes_dead_when_its_original_does() (+5 more)

### Community 94 - "WholeFaceToggles"
Cohesion: 0.14
Nodes (10): QApplication, QObject, Making the whole of a switch the part you can press. The theme turns every…, Turns a press anywhere on a switch into a click on it., Put the rule in place for every switch in the application., WholeFaceToggles, The theme makes a check box a button; Qt still thinks it is a tick box. Left…, Alt and a drag copies a control; that gesture must reach its own filter. (+2 more)

### Community 95 - "compute_vertex_normals"
Cohesion: 0.04
Nodes (70): Model orientation (1.1.0), Pedestal (1.1.0), Every panel scrolls, Semantic versioning policy, Session format version 4, STL corner welding, STL and glTF import (1.1.0), compute_vertex_normals() (+62 more)

### Community 96 - "ReflowLayout"
Cohesion: 0.14
Nodes (9): Orientations, QLayout, QLayoutItem, QRect, Put the items where the packing said, sharing out any room left. A panel is…, Whether an item asked to be given more height than it needs., Lays its items out in as many equal columns as the width allows., ReflowLayout (+1 more)

### Community 97 - "Measurement"
Cohesion: 0.11
Nodes (11): Measurement, MeasurementStore, ndarray, The live list; mutate through the methods below where possible., Append a measurement, auto-naming it when no name is supplied., A straight distance between two points on the model surface., Distance in scene units., One end of the measurement, ``0`` for the start and ``1`` for the end. (+3 more)

### Community 98 - "PointEdit"
Cohesion: 0.13
Nodes (10): _clone_point(), _pull_point(), _push_point(), _AxisBox, PointEdit, QDoubleSpinBox, QWidget, Three boxes for one point in space. Keyboard tracking is off, so a typed number… (+2 more)

### Community 99 - "OrientationSettings"
Cohesion: 0.14
Nodes (18): OrientationSettings, A rigid turn from the file's axes to the viewer's Y-up world., Whether the model is used exactly as the file stored it., QObject, Turning an imported model the right way up., A tall, thin shape lying along +Z, as a Z-up export would store it., A negative determinant would turn the model inside out., A measurement is attached to the surface, so it turns with it. (+10 more)

### Community 100 - "clone.py"
Cohesion: 0.06
Nodes (60): QAbstractButton, QLineEdit, QSlider, QSpinBox, _begin(), can_clone(), clone(), _clone_button() (+52 more)

### Community 101 - "skin_detail.py"
Cohesion: 0.11
Nodes (25): burley_marginal(), burley_profile(), cellular(), diffusion_lut(), _fade(), fbm(), ndarray, Procedural skin micro-relief and the pre-integrated diffusion table. Reference… (+17 more)

### Community 102 - "Path"
Cohesion: 0.13
Nodes (11): Path, Pick up whatever was last being worked on, if that was asked for. A session…, Write down the session just saved or loaded, for the next start., Write down the model just opened, for when there is no session. This also…, Load a model, reporting failures without tearing down the window. In the…, Read a model file off the window, then hand it to ``adopt`` here., Ask whether a rig that arrived with the model should be read as a figure. Only…, Add a model to the scene beside what is already there. (+3 more)

### Community 103 - "._turn"
Cohesion: 0.17
Nodes (5): Redraw from the settings, which something else has changed., Put the grading back, which is the one thing a disc cannot show., Turn the matcap by the angle the cursor swept about the centre. By angle and…, Two grades on one drag: one along each axis of the movement. Both move together…, Keep the angle in -180 to 180, the range the setting is stored in.

### Community 104 - "SetAttributes"
Cohesion: 0.09
Nodes (12): Any, Assign one or more attributes on an object, remembering the old values.…, SetAttributes, Record the finished drag as a single undo step., Alt forces the camera gesture, whichever tool is armed., Record the finished gesture: a move, a resize, or a plain click. A press that…, Record the finished drag as one step, or read a press as a selection., Run a bone between two nodes of the same armature. (+4 more)

### Community 105 - "test_panel_docks.py"
Cohesion: 0.14
Nodes (3): Each panel in a dock of its own, and putting the docks back next time. Two…, test_a_restored_copy_drives_the_new_windows_own_control(), test_the_layout_comes_back_through_the_settings()

### Community 106 - "OverlayParts"
Cohesion: 0.11
Nodes (9): MarkerVisibility, Cache surface occlusion by view and position for every kind of marker. The…, Whether the last pass is recent enough to be read instead of repeated., Mark these points as standing in front of the surface, untested. For frames…, Answer for a batch of points at once, ahead of being asked one by one. Every…, OverlayParts, ndarray, Every point the frame will ask the surface about, so it is asked once. Casting… (+1 more)

### Community 107 - "._place_armature_node"
Cohesion: 0.33
Nodes (3): Which armature an edit lands in, counting a guided run as binding., Drop a node, or record the landmark a guided run is asking for., A click on a length of wire lengthens the chain rather than branching off it.…

### Community 108 - "test_tasks.py"
Cohesion: 0.18
Nodes (16): app(), fixture, Work run off the window, and the cards that show it running., Turn the event loop until ``until()`` says so, or give up., runner(), _spin(), test_a_result_arriving_after_the_cross_is_thrown_away(), test_a_task_called_off_while_waiting_never_starts() (+8 more)

### Community 109 - "GuideRun"
Cohesion: 0.40
Nodes (3): GuideRun, Begin a preset run against an armature already in the store., A guided preset part-way through. The index walks the preset's own list rather…

### Community 110 - "DockTitle"
Cohesion: 0.15
Nodes (7): QToolButton, DockTitle, QSize, QWidget, The bar across the top of a dock: a switch, a name and two buttons., As tall as the bar really is. A dock puts the panel directly below its title…, StandardPixmap

### Community 111 - "test_reflow.py"
Cohesion: 0.18
Nodes (17): _block(), _panel(), QLabel, The layout that decides how many columns a panel is. A panel does not know…, A tree or a gallery is worth as much of the dock as is going spare., What the columns are for: the same groups, in less height., The scroll area sizes the panel from this, so it has to be the truth., A column of plain groups sits at the top of a tall panel. (+9 more)

### Community 112 - "._dress"
Cohesion: 0.18
Nodes (7): setter, The active object turned and centred but not posed or placed., The active object exactly as its file stored it., Set the active object's file mesh; its rest mesh is turned from it as at a load., The active object, made on the spot when a mesh is handed to an empty scene., Turn a freshly read mesh the right way up and centre it., Put ``rig`` on the object's file mesh, or take the one it wears off.

### Community 113 - "Task"
Cohesion: 0.18
Nodes (7): BaseException, T, Mark the task over. The runner does this; a begun task's driver does., Run ``work(progress)`` on a thread; ``done(result)`` back here. ``failed`` is…, A task driven by the caller, on the GUI thread, a step at a time. For work that…, One piece of work in flight, as the window sees it. Made by the runner, never…, Task

### Community 114 - ".render"
Cohesion: 0.24
Nodes (8): Draw one frame, then hand a neutral GL state back to the caller.…, gl_context(), fixture, Real GL: several objects drawn at their own solidity, and the grid under them., A square facing the camera, standing a little in front of the grid's wall., _square(), test_a_highlighted_object_wears_a_line_round_it_and_only_it(), test_objects_are_drawn_at_their_own_solidity_over_the_grid()

### Community 115 - "._build_objects"
Cohesion: 0.23
Nodes (4): QPushButton, QWidget, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 116 - "test_open_files.py"
Cohesion: 0.18
Nodes (9): app(), opened(), fixture, Files arriving from outside: the command line, a drop, or the desktop's "Open…, One offscreen Qt application for the run; see test_film_recorder., What the window was asked to open, by kind, without loading anything., Finder sends the launching file as an event, which can land before the window., test_a_file_the_desktop_hands_over_early_waits_for_the_window() (+1 more)

### Community 117 - "ShadingPanel"
Cohesion: 0.17
Nodes (8): Chooses the shading model and edits its light and surface parameters., Freeze the slices the way the camera faces now. The view direction is the one…, Show what this mode is actually lit and shaded by, and hide the rest. A matcap…, ShadingPanel, A matcap has no light to aim, so the Light group goes -- and its space. The…, test_a_copied_group_still_drives_the_originals(), test_a_group_the_mode_does_not_answer_leaves_no_room_behind(), test_copying_a_group_brings_its_rows()

### Community 118 - "test_session.py"
Cohesion: 0.09
Nodes (20): Session persistence, measurements and bookmarks., The slider is linear in how much of a turn one plane covers., A step of the slider is worth a fixed share more planes, not a fixed number of…, The ceiling went from 64 planes to 256 without moving the slider under anyone:…, The panel edits the settings; the fit has to be told what they are., Both modes answer in degrees of turn, so the panel can just ask., Version 1 files predate the annotation layer and the endpoint lock., Version 6 files predate panels being something a session could carry. (+12 more)

### Community 119 - "AddItem"
Cohesion: 0.14
Nodes (17): AddItem, Append an item to a document list., History, A bounded undo/redo stack., measurement(), Undo/redo and the commands the UI builds on., Dragging an endpoint edits the measurement live and commits on release., test_a_gesture_can_record_a_change_it_already_made() (+9 more)

### Community 120 - "ViewportOverlay"
Cohesion: 0.10
Nodes (30): QPointF, QRectF, draw_text(), Draw text as a filled outline rather than as glyphs. Qt's OpenGL paint engine…, project_visible(), project_visible_many(), Handle, QColor (+22 more)

### Community 121 - "ArmaturePanel"
Cohesion: 0.14
Nodes (5): ArmaturePanel, Arms the armature tool, lists its nodes and runs the guided presets., Take back the landmark before this one and ask for it again., Record an edit the viewport's tool worked out., The multiplier the position boxes are read and written through.

### Community 122 - "ArmatureStore"
Cohesion: 0.18
Nodes (4): ArmatureStore, An ordered, named collection of armatures, usually holding one. Deliberately…, The live list; the undo commands operate on it directly., Append an empty armature, auto-naming it when no name is supplied.

### Community 123 - "._selected"
Cohesion: 0.14
Nodes (7): Run a row's edit once Qt has finished delivering the current signal. Committing…, Write a structural change, detaching the armature from its preset., Remove the selected node, or the whole armature when its row is picked., Run a bone between the row selected now and the node held before it., Join two nodes of one armature, if they are two and they are one armature., The node the selected row stands for, if the row is a node at all., Follow the highlighted row, without rebuilding the list underneath it. Going…

### Community 124 - "_tab_switch"
Cohesion: 0.29
Nodes (7): The show/hide switch on the tab named ``title``, if it has one., Stacked behind another panel is where the switch is worth the most., It is fifteen pixels wide and carries no words, which is exactly the shape the…, _tab_switch(), test_a_panel_that_draws_nothing_gets_no_switch_on_its_tab(), test_a_tabbed_panel_still_shows_its_switch(), test_clicking_the_switch_on_a_tab_works()

### Community 125 - "Reflow"
Cohesion: 0.30
Nodes (4): QWidget, A widget laid out by :class:`ReflowLayout`, sized to fit its columns. A scroll…, Add a widget at a position, rather than only at the end., Reflow

### Community 126 - "viewport.py"
Cohesion: 0.04
Nodes (71): BoneLabels, Enum, str, A graph of named points under the form, and the wire it stands for. An armature…, When the length of a bone is written beside it., _centre(), form_landmark_title(), form_spec() (+63 more)

### Community 127 - "SectionPanel"
Cohesion: 0.18
Nodes (7): Cross-section tool (1.1.0), Turn the cut on or off, for the menu and the keyboard shortcut., Face the plane along the camera, so the cut squares up with the view., Only the settings this cut has a use for. A thickness is what a slab is; the…, Slices the model with a plane and shows the profile at the cut., Write one field; ``arms`` also switches the cut on. Moving the plane is a clear…, SectionPanel

### Community 128 - "._upload_sculpt"
Cohesion: 0.15
Nodes (6): Rebuild the planar stand-in and hand it to the renderer. Cutting a form into…, Cut the stand-in on a thread; see :meth:`_upload_sculpt`., Show the recording as a task, its bar the stages landed so far., The cross on the recording's card: the film is dropped, the switch too., A stage landed: show it if it is the one being looked at., Draw whichever stage of ``film`` the scrub handle is on.

### Community 129 - "._sync_scene"
Cohesion: 0.10
Nodes (7): The wire changed: redraw it, and re-cut anything built on it. Not mid-drag,…, A skeleton changed: redraw it., Hand the renderer a re-posed model and nothing else. For the frames of a pose…, Regenerate the pedestal and the cut contour when their settings move. Both are…, Rebuild the reference grids for the scene as it stands., The armature the clay is to be built on, if one was chosen. Read here rather…, Cut the mesh with each section plane and expand the result to strokes.

### Community 130 - ".stage_images"
Cohesion: 0.21
Nodes (7): QOpenGLFramebufferObject, QImage, One stage, rendered as it would be exported. For the preview., Render each of ``stages`` offscreen, at the size and look asked for. A…, An offscreen target the frames are drawn into, made once per export.…, Draw the scene into ``surface`` and read it back as an image., Lay the overlay -- and the caption, if it was asked for -- on a frame. Painted…

### Community 131 - "AnnotateTool"
Cohesion: 0.08
Nodes (21): AnnotateMode, AnnotationSettings, Enum, str, Freehand annotations painted onto the model surface. A stroke is a polyline of…, The annotate tool's brush, shared by every stroke it lays down., An empty stroke carrying the current brush., What the annotate tool does with a drag. The first three describe the shape a… (+13 more)

### Community 132 - "ExportLook"
Cohesion: 0.08
Nodes (18): ExportLook, What the frames are to look like, as against what they are of. Laid over the…, Which of the things drawn over the model belong in the frames., ``base`` with this export's choices laid over it., The line burned into the corner of the frame for ``stage``. Counted off the…, app(), FakeViewport, fixture (+10 more)

### Community 133 - ".__init__"
Cohesion: 0.14
Nodes (5): Push the preferences that this window's own parts hold a copy of. The store has…, Put the docks and the hand-built panels back where they were. Unless the artist…, Give each panel a dock of its own, tabbed together on the right. Each panel can…, Single-key shortcuts, scoped so they never eat text input. They only fire while…, Say which panel buttons are the same thing as a menu entry. The button that…

### Community 134 - "preview"
Cohesion: 0.40
Nodes (5): app(), preview(), fixture, One offscreen Qt application for the run; see test_film_recorder., A disc the size the panel gives it, with settings of its own to write.

### Community 135 - "._build"
Cohesion: 0.25
Nodes (7): QTreeWidget, QPushButton, QWidget, Add a group below the list rather than to the panel root., The points the preset was built from, and the means to move them. Its own list…, A strip of buttons that one form row can show or hide as a unit., _row()

### Community 136 - "paths.py"
Cohesion: 0.26
Nodes (13): available_matcaps(), _bundled_root(), image_path(), matcap_dir(), model_dir(), Path, Locations of the bundled resources. ``REFVIEW_RESOURCES`` overrides the search,…, Return PyInstaller's extracted application directory when frozen. (+5 more)

### Community 137 - "Release"
Cohesion: 0.18
Nodes (12): The newest published release, as GitHub describes it., Release, Ask GitHub for the newest release in the background. The startup check is…, is_skipped(), QWidget, Background release check and the notice it puts in front of the artist. The…, Whether the artist already dismissed this exact version., Offer the release page, with the option never to be asked again. (+4 more)

### Community 138 - "watch_keys"
Cohesion: 0.19
Nodes (11): can_take_key(), is_hotkey_click(), KeyGesture, QObject, QWidget, The gesture that puts a key on a control: Ctrl/Cmd, Alt and a click. It sits…, Whether a mouse press is the assignment gesture rather than a click., Whether a widget is the kind a key can sensibly be put on. A button or a switch… (+3 more)

### Community 139 - "OpenRequests"
Cohesion: 0.15
Nodes (8): Application, OpenRequests, Path, QApplication, The Qt application, listening for the desktop's way of handing over a file., Files the desktop asked the viewer to open, kept until there is a window. On…, Open ``path`` in the window, or hold it until there is one., Name the window files go to, and hand over any that came early.

### Community 140 - "_drag_over"
Cohesion: 0.22
Nodes (10): _drag_over(), _middle_of_the_view(), A drag of ``holder`` arriving at ``point`` in the window's coordinates. A real…, The gesture the whole thing rests on: drag it onto the model, it goes., A gesture that destroys something only fires where it clearly meant to., Refused at the door it would never reach the model; so it is let in., test_a_copy_dropped_on_the_model_is_thrown_away(), test_a_copy_is_let_into_the_window_wherever_it_arrives() (+2 more)

### Community 141 - "PanelDock"
Cohesion: 0.25
Nodes (3): QDockWidget, PanelDock, A dock that can go anywhere, with :class:`DockTitle` across the top.

### Community 142 - "._build"
Cohesion: 0.28
Nodes (4): Lay one length of wire earlier or later, as one undoable step., The armature the clay is being built on, or ``None``. An index past the end of…, Put the clay on all of the wire, or take it off all of it., Write which lengths of wire take clay, as one undoable step.

### Community 143 - "matcap_preview.py"
Cohesion: 0.14
Nodes (15): _angle(), grade(), _push_preview(), ndarray, The matcap itself, as the control for grading it. A matcap is a picture of a…, Draw the matcap onto a sphere of ``size`` pixels, graded. Returns ``(size,…, The angle of ``point`` about ``centre``, anticlockwise with y upwards., An angle difference brought back into -pi to pi. (+7 more)

### Community 144 - "._picker"
Cohesion: 0.08
Nodes (13): ndarray, Rub out the stroke points under the eraser, live., Take hold of a node, to move it, resize it, or just to select it. This works…, Apply the drag live, so the artist sees the wire bend as they pull it., Take hold of a landmark, to move it or just to say which one it is., Apply the drag live, so the figure re-forms under the cursor., Orbit increment while Shift is held, or 0 for a free orbit., Object centre, which anchors the plane the orbit pivot lies on. (+5 more)

### Community 145 - "._carrying_a_copy"
Cohesion: 0.11
Nodes (10): opens_as(), Whether the drag is a copy being moved out of a hand-built panel., Whether this drag is a copied control being let go over the model. Dragging a…, Whether a point in the window's own coordinates is on the model., Take a copied control out of whichever hand-built panel holds it., Open a file by what it is: a model, a session or a matcap. The one door every…, What a file would open as -- ``"model"``, ``"session"`` or ``"matcap"`` -- by…, Apply a matcap image, reporting unreadable files to the user. (+2 more)

### Community 146 - ".load"
Cohesion: 0.33
Nodes (3): Take a hand-built panel away. Its dock is parked, not destroyed. The dock has…, Rebuild the panels built by hand. Call before :meth:`restore_state`. Whatever…, Put the layout back. Returns whether there was one to put back.

### Community 147 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 148 - "QComboBox"
Cohesion: 0.33
Nodes (4): QComboBox, _push_combo(), QWidget, _row()

### Community 149 - ".dress_tabs"
Cohesion: 0.29
Nodes (5): QTabBar, Hang a show/hide switch on every dock tab that wants one. A dock stacked behind…, The panel whose dock is called ``title``, if there is one., Let a strip of tabs keep its names, and scroll if they do not fit. Ten panels…, _widen()

### Community 150 - "UpdateChecker"
Cohesion: 0.22
Nodes (7): QRunnable, _CheckTask, QObject, Runs :func:`check_for_update` off the UI thread and reports back., Begin a check, unless one is already in flight., Announce the outcome. Always called on the checker's own thread., UpdateChecker

### Community 152 - ".update_enabled"
Cohesion: 0.17
Nodes (6): Adopt the viewport's tool, which is where the guided run lives., Reflect the tool state without re-emitting the toggle., Take off the panel whatever does not apply right now., The armature the selected row stands for, when the row is not a node., Highlight the row for a node picked in the view., Highlight the row for a landmark picked in the view.

### Community 153 - "skeleton.py"
Cohesion: 0.12
Nodes (9): Buried, What becomes of the part of the armature the model is standing in front of. An…, Enum, A hierarchy of joints, the pose it is in, and the skin that moves with it.…, How auto-skinning decides the weights; see :mod:`refview.core.autoskin`., An ordered collection of skeletons, like the other document stores., The skeleton the model follows: the first one bound to its rig., SkeletonStore (+1 more)

### Community 154 - "restored"
Cohesion: 0.29
Nodes (7): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., A window with the saved layout out of the way, and put back after. Shown,…, A second window, built from a layout the first one saved. The point is…, restored(), window()

### Community 156 - "._on_bone_toggled"
Cohesion: 0.29
Nodes (4): QListWidgetItem, Catch the selection a click on a checkbox is about to collapse. Qt selects a…, Which bones of the armature the picked-out rows stand for., Take lengths of wire out of the clay, or put them back. A tick on a row that…

### Community 158 - "shaders.py"
Cohesion: 0.25
Nodes (6): GLSL sources for the viewport. Seven small programs cover everything the viewer…, Splice the shared cross-section test into a fragment shader., Substitute the array sizes GLSL needs as compile-time constants., _with_limits(), _with_section(), Skin BRDF and bounded-depth light transport, shared by preview and refinement.…

### Community 159 - ".paintGL"
Cohesion: 0.29
Nodes (3): Use the same cached visibility test for bones and all point markers., Which part wears the line this frame, and how solid it is, or ``None``. Also…, Hand the renderer the depth grid, or take it away, before a frame.

### Community 160 - "write"
Cohesion: 0.31
Nodes (9): _push_slider(), OBJ parsing: normals, triangulation and index handling., test_bounds_of_an_empty_point_set(), test_empty_file_is_rejected(), test_missing_normals_are_computed(), test_negative_indices_are_relative(), test_quad_is_triangulated(), test_recentering_moves_bounds_onto_the_origin() (+1 more)

### Community 161 - "ProgressCard"
Cohesion: 0.19
Nodes (6): _outcome(), ProgressCard, QPainter, One task: its name, its message, its bar, and a cross to stop it. Painted by…, The word a finished card ends on., test_a_card_paints_every_state_it_can_be_in()

### Community 162 - ".column_of"
Cohesion: 0.25
Nodes (3): How many columns this layout would break into at ``width``., Which column a widget currently sits in, or -1 if it is not laid out., How many columns the widget is currently broken into.

### Community 163 - "TaskRunner"
Cohesion: 0.21
Nodes (6): QObject, QWidget, Runs work off the GUI thread and keeps the window told. :attr:`started` and…, Every task in flight, oldest first., The blocking task running now, if there is one., TaskRunner

### Community 164 - "Human Skin renderer"
Cohesion: 0.33
Nodes (5): Human Skin renderer, Material and transport, Scheduling, precision and compatibility, Surface, Where to change it

### Community 165 - "Command"
Cohesion: 0.21
Nodes (4): Camera motion is deliberately not undoable, Command, One reversible change, named for the undo menu., Record ``command``, applying it first unless it already ran. Interactive…

### Community 166 - "lumpy"
Cohesion: 0.20
Nodes (10): lumpy(), A form with real planes in it, and more than one facing the same way., How many planes have another plane pointing very nearly where they do., The coefficients have to reach the fit, and reaching it has to show. Two planes…, The fit and the shader have to agree, or the boundaries drawn are not the…, Narrow it and only the flattest surface has a say; widen it and the rounded…, same_facing(), test_a_coefficient_of_zero_takes_the_term_out_of_the_shader_too() (+2 more)

### Community 167 - "coarse_lattice"
Cohesion: 0.50
Nodes (4): coarse_lattice(), fixture, MonkeyPatch, Read every model on a small lattice, so the suite stays quick.

### Community 168 - "ndarray"
Cohesion: 0.29
Nodes (3): ndarray, Every node position as ``(n, 3)``., The landmarks as a mapping a preset builder can read.

### Community 169 - "sample_count"
Cohesion: 0.50
Nodes (3): How many samples the framebuffer bound right now is drawing with. One where…, sample_count(), How many samples this view is really drawing with, or ``None``. Asked of GL…

### Community 170 - "_height_of"
Cohesion: 0.40
Nodes (3): _height_of(), QSize, How tall an item needs to be once it has been given ``width``.

### Community 171 - "_file_drag"
Cohesion: 0.40
Nodes (5): _file_drag(), A file being dragged over the middle of the view, as ``kind`` of event., Entering, moving and dropping: a drop lands only where the move before it was…, test_a_file_the_window_cannot_open_is_refused_on_the_way_past(), test_a_model_file_is_welcome_at_every_step_of_its_drag()

### Community 172 - ".refresh_list"
Cohesion: 0.18
Nodes (3): QTreeWidgetItem, Show the knobs the chosen method reads, and no others., Rebuild the tree from the store, keeping the tool's selection shown. Not under…

### Community 173 - "README.md"
Cohesion: 0.27
Nodes (10): Annotations drawn as widened geometry, core never imports Qt, The cut interior is flooded flat, Every document edit is a command, Three-layer separation: core, render, ui, Measurements drawn in screen space with QPainter, Orthographic extent derived from FOV and distance, Panels edit dataclasses, never foreign widgets (+2 more)

### Community 175 - "panel"
Cohesion: 0.50
Nodes (4): app(), panel(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 176 - "raycast_mesh"
Cohesion: 0.05
Nodes (56): Picking about a hundred times faster, Morton-curve leaf boxes for picking, Picking accelerator, built on first use and kept for the mesh's life., _cross(), Hit, intersects_bounds(), ndarray, Ray/mesh intersection used by the measuring and annotating tools. The test… (+48 more)

### Community 177 - "test_the_switch_on_a_dock_bar_is_the_panels_own_visibility"
Cohesion: 0.67
Nodes (3): parametrize, test_a_panel_that_draws_nothing_has_no_switch(), test_the_switch_on_a_dock_bar_is_the_panels_own_visibility()

### Community 178 - "._add_skeleton"
Cohesion: 0.18
Nodes (5): Highlight a row, in the tree and in the view., Add an empty skeleton, for a chain to be clicked into., Stand a proportioned humanoid skeleton in the model's box., Grow a skeleton out of the armature chosen in the box., Record a structural edit the viewport's tool worked out.

### Community 179 - "app"
Cohesion: 0.67
Nodes (3): app(), fixture, One offscreen Qt application for the run; see test_film_recorder.

### Community 182 - "decode"
Cohesion: 0.27
Nodes (8): _coerce(), decode(), encode(), Any, T, Tolerant conversion between dataclasses and plain JSON structures. Sessions…, Convert dataclasses, enums, tuples and numpy arrays to JSON types., Build an instance of the dataclass ``cls`` from ``data``.

### Community 186 - "ModelPanel"
Cohesion: 0.08
Nodes (11): ModelPanel, QTreeWidgetItem, Bind the panel to the viewport's transform tool., Reflect the tool state without re-emitting the toggle., Choose the gesture, from the menu or a key., Rebuild the tree from the store, with the active object current., Offer every object the active one could hang from., The objects whose rows are selected, in list order. (+3 more)

### Community 187 - "Preferences"
Cohesion: 0.12
Nodes (19): Preferences, Everything above, in one object, which is what gets saved and applied., Read preferences back, keeping whatever makes sense and no less. A field that…, Back to how the application ships., The font size is a string; everything beside it still arrives., test_a_field_from_a_later_version_is_ignored(), test_a_setting_out_of_range_is_brought_back_into_it(), test_a_settings_file_that_is_not_settings_at_all_still_starts() (+11 more)

### Community 188 - "navigation.py"
Cohesion: 0.22
Nodes (6): DragMode, Enum, ndarray, Mouse-gesture to camera-motion mapping. Orbiting pivots on the point where the…, Zoom by wheel notches, keeping the point under the cursor fixed. ``anchor`` is…, Start a drag, resolving the orbit pivot from the cursor position.

### Community 190 - ".reset"
Cohesion: 0.22
Nodes (5): QSettings, Bring the first panel to the front of the tab strip., The part of the layout Qt cannot describe., Write the whole layout, ours and Qt's, into the settings., Put every dock back where it started, now. Not "forget the saved layout and…

### Community 191 - "release.yml"
Cohesion: 0.47
Nodes (5): Publish job creates the GitHub release, PyInstaller build from packaging/refview.spec, Release triggered by a v* tag, Windows, Intel macOS and Apple Silicon matrix, Tag-driven desktop releases

### Community 192 - "._refresh_cursor"
Cohesion: 0.27
Nodes (4): Track whatever the cursor is over, so the overlay can respond., Track the node and bone under the cursor; True when anything changed., Track the joint and bone under the cursor; True when either changed., Track the form landmark under the cursor; True when it changed.

### Community 193 - "bent_plate"
Cohesion: 0.20
Nodes (10): angle_deg(), bent_plate(), ndarray, How far the least well served of ``wanted`` is from anything offered., A flat with a scattering of bad normals is still shaded as that flat. Averaging…, A plate creased down the middle, and which column each vertex is in. Flat to…, Vertices on a turn are ambiguous about their plane, so they are quieted. The…, test_a_turn_in_the_form_gets_less_of_a_say_than_a_flat() (+2 more)

### Community 194 - "_clone_preview"
Cohesion: 0.31
Nodes (5): _clone_preview(), _pull_preview(), Point the preview at the settings it edits. The object itself, not a copy: this…, The matcap image, in the orientation the renderer uploads it. ``None`` for the…, The matcap image this is drawing, for a copy of it to draw too.

### Community 195 - "._build_menus"
Cohesion: 0.20
Nodes (6): _plain(), QAction, Open the preferences, on one group when the menu asked for one., A menu entry's text as a name: no accelerator ampersand, no trailing dots., Which panels are open, and the panels the artist builds. Rebuilt every time it…, Add a menu entry, optionally with a window-wide shortcut. Given a ``command``…

### Community 196 - "generate_matcaps.py"
Cohesion: 0.32
Nodes (7): Color, main(), _normalize(), ndarray, Path, Render the bundled matcap set. Each preset is evaluated analytically over the…, save()

### Community 198 - "_fill"
Cohesion: 0.29
Nodes (7): _as_kind_of(), equal(), _fill(), Any, Copy what type-checks out of ``written`` and into ``group``. The default…, ``value`` as the same sort of thing as ``like``, or ``None`` if it is not. A…, Whether two preference objects say the same thing. Dataclasses compare by value…

### Community 201 - "box"
Cohesion: 0.50
Nodes (4): box(), A unit cube, shaded flat: six planes and twelve right angles., Every edge of a cube is a right angle, and no reading of AutoSmooth short of…, test_autosmooth_leaves_a_real_plane_change_hard()

### Community 203 - ".update_enabled"
Cohesion: 0.29
Nodes (4): Hold the settings a recording is built from still while it runs. A film is a…, Show what this way of working needs, and put the rest away. A setting that does…, The bones of the chosen armature, in the order the clay goes down. Every intact…, What can be done to the list, given where the handle is and whether a film is…

### Community 205 - "step"
Cohesion: 0.25
Nodes (8): quad(), The limit the clustered fits exist to lift, stated as a fact., Splitting a broad flat by place must not invent a turn in it. The plate below…, Add one flat quad, with its own vertices, to a mesh under construction., Two broad faces both looking straight up, one raised above the other. The case…, step(), test_a_model_that_is_flat_all_over_gets_the_same_direction_everywhere(), test_reading_the_normals_alone_cannot_tell_that_step_apart()

### Community 206 - "_drop_on"
Cohesion: 0.29
Nodes (7): QMimeData, _drop_on(), The end of the gesture: the payload a drag carries, delivered., Drop ``mime`` on the top-left of ``panel``; was it taken? The caller keeps hold…, test_a_drop_carrying_a_control_takes_a_copy_of_it(), test_a_drop_carrying_something_else_is_refused(), test_a_drop_naming_a_control_that_is_gone_is_refused()

### Community 207 - ".point"
Cohesion: 0.29
Nodes (4): ndarray, Surface point under the cursor, optionally snapped to a vertex., Point on the camera-facing plane through ``anchor``. This is where free-…, Screen-to-world scale at a given depth along the view direction.

### Community 208 - ".new_custom_panel"
Cohesion: 0.29
Nodes (4): _number_in(), An empty panel of the artist's own, docked on the right. A dock put away…, Take a parked dock back out under ``key``, emptied and renamed., The number at the end of a custom panel's key, or nought.

### Community 209 - "_create_splash"
Cohesion: 0.50
Nodes (5): QSplashScreen, _create_splash(), _fitted_title_font(), QFont, Largest title font that still draws the whole app name inside ``width``.

### Community 210 - "_Worker"
Cohesion: 0.40
Nodes (3): Any, The function itself, living on the worker thread., _Worker

### Community 212 - "_clamp"
Cohesion: 0.50
Nodes (4): _clamp(), What the 3D view costs the machine., Pull anything out of range back into it. The window cannot produce these…, ViewportPreferences

### Community 213 - "_segment_distance"
Cohesion: 0.50
Nodes (4): How far along a screen-space segment the cursor's nearest point lies., Pixels from the cursor to the segment, or ``None`` if either end is behind., _segment_distance(), _segment_share()

### Community 214 - ".form"
Cohesion: 0.50
Nodes (3): QFormLayout, The rows inside the frame. ``layout()`` is the frame's own, which stacks the…, The row layout the frames are filled with.

### Community 215 - "_NameOnlyDelegate"
Cohesion: 0.50
Nodes (3): _NameOnlyDelegate, QStyledItemDelegate, Allows in-place editing of the name column only.

### Community 217 - "section"
Cohesion: 0.50
Nodes (4): app(), fixture, One offscreen Qt application for the run; see test_film_recorder., section()

## Knowledge Gaps
- **5 isolated node(s):** `refview`, `Surface`, `Material and transport`, `Scheduling, precision and compatibility`, `Where to change it`
  These have ≤1 connection - possible missing edges or undocumented components.
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mesh` connect `Mesh` to `SceneObject`, `core/__init__.py`, `ExportLook`, `main_window.py`, `MeshBuffers`, `ViewerState`, `Skeleton`, `mesh_renderer.py`, `PoseTool`, `skeleton.py`, `SectionAxis`, `plane_volume.py`, `auto_skin`, `PlaneSettings`, `test_plane_clusters.py`, `lumpy`, `convex.py`, `autoskin.py`, `Rig`, `ExportVideoDialog`, `raycast_mesh`, `test_skeleton.py`, `test_forms.py`, `bent_plate`, `FormTool`, `plane_axes`, `state.py`, `test_skin.py`, `test_plane_solids.py`, `Session`, `box`, `step`, `SkinEdit`, `ndarray`, `PrimaryForm`, `compute_vertex_normals`, `OrientationSettings`, `Path`, `._dress`, `.render`, `viewport.py`?**
  _High betweenness centrality (0.178) - this node is a cross-community bridge._
- **Why does `Viewport` connect `Viewport` to `._upload_sculpt`, `._sync_scene`, `.stage_images`, `AnnotateTool`, `ExportLook`, `.__init__`, `MainWindow`, `main_window.py`, `ViewerState`, `._picker`, `PoseTool`, `.paintGL`, `PlaneSettings`, `film_export.py`, `sample_count`, `ExportVideoDialog`, `._active_changed`, `FilmExport`, `Preferences`, `navigation.py`, `._refresh_cursor`, `MeasureTool`, `FormTool`, `state.py`, `._place_joint`, `ObjectTool`, `._place_form_landmark`, `SurfacePicker`, `NavigationController`, `test_viewport_markers.py`, `PrimaryForm`, `_Encoder`, `Measurement`, `SetAttributes`, `._place_armature_node`, `ViewportOverlay`, `viewport.py`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `ViewerState` connect `ViewerState` to `Viewport`, `SceneObject`, `.__init__`, `MainWindow`, `main_window.py`, `Armature`, `CameraPanel`, `PoseTool`, `MeasurePanel`, `auto_skin`, `TaskRunner`, `README.md`, `panel`, `test_matcap_preview.py`, `test_skeleton.py`, `Preferences`, `state.py`, `test_skin.py`, `Session`, `SurfacePicker`, `test_custom_panels.py`, `SkinEdit`, `._commit_objects`, `test_forms_panel.py`, `test_viewport_markers.py`, `PrimaryForm`, `MatcapPanel`, `section`, `test_an_attribute_beats_a_group_title_to_a_name`, `OrientationSettings`, `OverlayParts`, `._dress`, `ShadingPanel`, `ViewportOverlay`, `viewport.py`?**
  _High betweenness centrality (0.048) - this node is a cross-community bridge._
- **Are the 53 inferred relationships involving `Mesh` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Mesh` has 53 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `ViewerState` (e.g. with `MainWindow` and `OverlayParts`) actually correct?**
  _`ViewerState` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `Viewport` (e.g. with `_Encoder` and `ExportLook`) actually correct?**
  _`Viewport` has 20 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Skeleton` (e.g. with `AutoSkin` and `AutoSkinError`) actually correct?**
  _`Skeleton` has 9 INFERRED edges - model-reasoned connections that need verification._