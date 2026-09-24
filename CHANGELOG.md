# Changelog

All notable changes to Reference Viewer are recorded here. Versions follow
[semantic versioning](https://semver.org/): the minor number moves when
features land, the patch number when only fixes do.

## [2.9.0]

### Added

- **NVIDIA DLSS 5 Neural Rendering.**  A new **Neural Rendering** group in
  the Render panel runs DLSS 5's AI model over a render once it is
  denoised, relighting skin and materials towards a photograph's response
  to light.  **Enhance the render** does it to every finished render, and
  the Render window shows the result as a new **Neural** pass, with an
  **Enhance** button to run it again.  **Enhance the rendered viewport**
  does it to the viewport each time it is denoised.  Style (Default,
  Natural, Cinematic), intensity, passes, local tone and structure, skin
  structure, colour strength, tone preservation, skin protection and the
  automatic mask are all there.  Changing the view transform or exposure
  enhances the picture again a moment after the slider stops.
- It runs through the **Neuroframe Engine** from Merserk's Visual Enhancer,
  used with its author's permission.  The engine is not in this repository:
  point **Preferences > Folders > Neural engine** at a Visual Enhancer
  folder, or build with its `dlssnr` folder in `resources/dlssnr`.  It needs
  a GeForce RTX 50 series GPU.

### Changed

- The Neural pass is a finished picture, not scene light, so it saves as
  PNG; saving it as OpenEXR says so instead.

## [2.8.0]

### Added

- **Path-traced rendering.**  A new **Render** panel and **Render** menu
  path-trace the view on the processor, with every core: next-event
  estimation from the key and fill lights and the HDRI, weighted against the
  bounces by multiple importance sampling; separate diffuse, glossy and
  transmission bounce limits; clamping, glossy filtering and Russian
  roulette; Owen-scrambled Sobol samples; and adaptive sampling that stops
  each part of the image once its noise falls under the threshold.  The
  shading panel's settings carry over: PBR, Lambert, Phong, Blinn-Phong and
  High Quality render as the materials they describe, Matcap, Normals and
  Contour as a clay of their own, the pedestal and forms in their colours,
  the cross-section with its cap, and ghosted objects half there.  The
  kernels are compiled to machine code by numba the first time and kept, so
  only the first render of a version waits for them.

- **Human Skin, path-traced.**  The whole of the skin shader, ported: the
  pores and furrows, the regions and their marks, the vessels, the two-lobe
  oily highlight, disk-projected subsurface scattering, thickness
  transmission and the fuzz.  Its exposure and Reinhard tone curve are the
  viewport's, so a render matches the refined view it was made from.

- **Render Image (`F12`)** opens the **Render window**, filling in bucket by
  bucket or pass by pass.  It shows the beauty, denoised, albedo, normal,
  depth, alpha and sample-count passes; the view transform and exposure
  change the finished picture without rendering it again; and it saves PNG
  (8 or 16 bits), OpenEXR (half or float) or every pass in one multilayer
  EXR.  `Esc` stops a render, `Ctrl+F12` brings the window back.

- **Rendered viewport (`Shift+F12`).**  The view itself path-traced and
  denoised as you work in it: coarse while it turns, sharpening as soon as
  it stops, started over by anything that changes the picture and by
  nothing that does not.

- **AI denoising.**  Intel Open Image Denoise -- on an NVIDIA GPU through
  CUDA where there is one, on the processor everywhere else -- and the
  NVIDIA OptiX denoiser, reached through the graphics driver with nothing
  to install; a built-in edge-avoiding filter stands in when neither can
  run.  **Auto** picks the best one here and the panel says which.  A 4K
  frame denoises in about a fifth of a second on a laptop GPU.

- **Output size and safe frame.**  Presets from 720p to A4 at 300 dpi,
  the viewport's own size, or any size with its proportions kept.  The
  **safe frame** shades the view outside what will be rendered and draws
  the action-safe and title-safe guides; `F12` renders exactly what is
  inside it.

- **Presets** -- Preview, Draft, Final and Production -- set the samples,
  noise threshold, bounces and denoising at once; any edit after that makes
  them Custom.  Every control has a tooltip saying what it does to the
  picture.

### Changed

- Sessions are version 12 and keep the Render panel's settings; older
  sessions open with its defaults.
- `numba` and `mitsuba-oidn` are new dependencies; the desktop releases
  carry both.

## [2.7.0]

### Changed

- **Human Skin backlighting.** Traced transmission uses the measured distance
  to the opposite, outward-facing skin surface. Blood and a new, adjustable
  vessel pattern increase absorption along that path, so thin areas glow while
  thick areas stay opaque. The vessel pattern adds a faint cool tint in
  reflection, fades when too small to resolve, and needs no UV map.
- The Human Skin panel has a **Subtle veins** control. It starts low and is
  preserved when changing tone presets. Its vessels now vary gently in width
  and strength, and each Body Region has an editable vein multiplier.

## [2.6.0]

### Added

- **HDRI lighting.**  Every lit mode -- Lambert, Phong, Blinn-Phong, PBR,
  High Quality and Human Skin -- can be lit by an HDRI in place of the
  studio rig, or by both: **Lighting** in the Light group.  The map lights
  the diffuse from nine spherical-harmonic coefficients and puts its own
  reflection in the highlights, read off its mip chain at the width of the
  surface's lobe (the split sum, for PBR); with the map as the only light
  the shadow map is cast from its dominant direction, and the shadowed
  places lose that light's share.  The traced skin samples the map in
  proportion to its light -- a marginal and a conditional distribution over
  a coarse copy -- and shadows, scatters and backlights with the whole room.
  The maps in `resources/hdris` are listed, **Load HDRI...** or a drop on
  the window takes any `.hdr` or `.exr`, and a session remembers which.
  **Strength** is normalised so that one lights the model about as brightly
  as the studio key whatever exposure the map was shot at; **Rotation**
  turns it; it can be shown, blurred, behind the model.  Radiance `.hdr` is
  read in numpy; OpenEXR through the `OpenEXR` package, now a dependency.

- **Turning the lights by hand.**  `Shift` + right-drag in a lit mode turns
  every light at once -- the key and the fill across and up, the HDRI with
  them -- as one undo step, with the angles in a caption while it runs and
  `Esc` to put them back.

- **AutoSmooth** under the shading mode, with its angle: the model shaded
  smooth across gentle edges and hard across sharp ones, for a scan or a
  hard-surface model whose normals were lost or averaged over its creases.
  The smoothing groups are found once per object, so a moved or posed
  object stays smoothed through every frame of the drag.

- **The matcap gallery keeps what was loaded.**  A matcap from outside the
  matcap folder -- loaded, dropped, opened, or brought in by a session --
  joins the gallery after the built-in and stays there; right-click it to
  take it out again.

### Changed

- **Human Skin refines close to real time.**  A traced sample costs about a
  quarter of what it did -- 8 ms against 28 on a full figure, 18 against 63
  close up -- and a frame runs as many as fit in 24 ms, so 128 samples
  arrive in one to two seconds where they took three to eight.  The samples are
  stratified -- a low-discrepancy sequence per pair of dimensions from a
  random start per pixel -- so 16 now look as clean as 128 of the old
  noise, and the default is 64.  The pieces:
  - The tracer's tree is built by the surface-area heuristic, a level at a
    time in numpy, and keeps both children's boxes in each node, so a ray
    walks into the nearer first and culls everything behind its first hit.
  - Shadow rays stop at the first triangle they find.
  - Every ray of a sample goes through one traversal in a loop of jobs,
    where it used to be inlined at a dozen call sites.
  - The mesh shader is compiled twice, with the tracer as a constant in
    each, so the preview -- and every other mode -- no longer carries the
    tracer's register load.
  - Tables are laid out a power of two wide and read with a shift and a
    mask; triangle normals are read once, for the nearest hit.
- **The skin refines through what does not concern it.**  A button held on
  a panel, a tab or a menu used to count as navigating the view and threw
  the samples away; now only a drag in the view that has moved does.  And
  the refinement starts over only when something it draws changes -- not
  for the matcap's grading, the contour paper, the analytic modes' surface,
  the High Quality sliders, the planes while they are off, or the
  wireframe's colour while there is no wireframe.
- **Matcap thumbnails are made once.**  Every gallery in the process shares
  them, so a rescan or a second window does not decode the collection again.
- **The shaders live in `render/glsl`**, a file a stage, the pieces several
  share pulled in with `#include`.

### Fixed

- Traced backlight transmission was always black: the light was looked for
  through the body before the light through it was worked out.

## [2.5.0]

### Added

- **Auto-skin.** A skeleton the model did not come with -- the humanoid
  preset pulled into place, a chain clicked in, one grown out of an armature
  -- can now be given skin weights in one press, so that posing the bones
  poses the model.  **Skin to Model** under **Pose > Auto-skin** (folded
  away by default) makes them and binds the skeleton where it stands, its
  pose becoming its rest; **Unskin** takes them off; either is one undo
  step.  Three ways of deciding the weights: **Heat diffusion**, the
  default, after Baran and Popović's *Pinocchio* -- each bone's warmth is
  let spread over the surface of the model and the temperature it settles
  at is the weight, so a hand resting on a hip stays the hand's and the
  blend at a knee is as wide as the leg is thick; **Envelope**, which
  shares each vertex among its nearest bones by distance; and **Nearest
  bone**, which gives each vertex wholly to one.  How many bones may share a
  vertex, how tightly the heat hugs the nearest bone, and whether a bone
  that lies out in front of the skin is passed over for one behind it, are
  the knobs.  The heat solve is a conjugate-gradient pass over a
  two-level Laplacian of the welded mesh, in numpy, and takes a second or
  two on a figure of twenty thousand vertices.  A skin made here is saved
  as a small archive beside the session, named for the session and the
  object, and put back when the session is loaded.  Sessions are at
  version 10.

- **Progress, shown.** Everything that takes a while now says so in one
  way: a card floated over the foot of the view, with what is being done,
  what it is doing right now, a bar that fills when the work can count and
  sweeps when it cannot, and a cross to stop it.  Opening or adding a
  model, loading a session, skinning a figure, rebuilding a form from
  planes, recording a form's making, exporting a video and checking for
  updates all report through it.  A job over in a blink never shows a card
  at all.  The work behind a card runs off the window, so a scan being read
  or a figure being skinned no longer freezes it: the last scene stays up
  and answering until the new one is ready, and a second scene-changing
  job asked for meanwhile waits its turn.  The video export's card sits in
  its own dialog, since that dialog is modal and a cross the artist could
  not reach would be no cross at all.

- **An orientation for each object.**  Which axis of the file is up, whether
  it arrived upside down and the quarter turn that faces it forwards now
  belong to the object rather than to the scene, so a Z-up scan and a Y-up
  sculpt can stand side by side.  The Orientation group on the Model tab
  shows and sets the active object's; the next model added is read the same
  way, since files from one pipeline share an up axis, and **Apply to All**
  turns every object alike.  Sessions are at version 11; one from before
  reads every object the one way it named.

- **Normalize Objects.**  Scales the selected objects so that each is the
  size of the active one -- the largest of its three extents is matched,
  about its own pivot, the same on every axis -- so a head scanned in
  millimetres and a figure modelled in metres come out the same height and
  can be set against each other.  Parents are resized before their
  children, so a child chosen along with its parent is not scaled twice.
  One undo step.

- **Reset XForm.**  Writes the active object's rotation and scale into its
  mesh, as 3ds Max's does: afterwards it is unturned and unscaled, stands
  where it stood, and nothing in the view has moved.  Its mesh is no longer
  its file's, so saving the session writes it out as an OBJ beside it, as a
  merged object is; a rig the file gave it is kept, marked as a skin made
  here, and saved beside the session too.  One undo step.

- **Skin that is marked.**  Four more knobs under Human Skin: **Freckles**,
  small light-brown dots, thick on the ground; **Moles**, dark, a few pores
  across, few and faintly raised; **Acne**, red papules raised and shining,
  some come to a pale head; and **Blemishes**, patches coarser than the
  pores of irritated redness and of dry, duller skin.  The spots are round
  discs on jittered lattices worked out in the shader from the world
  position and projected onto the skin whichever way it faces -- one hash
  per lattice, no UV layout, no repeat -- and their size follows the pore
  size.  All start at nought, and a tone preset leaves them alone.

- **Body regions.**  Where the marks fall is worked out from what the scene
  knows about the body.  A skeleton with humanoid roles -- the preset, a rig
  read by its names, one grown out of the guided armature -- places every
  limb: each point of the skin goes to the region of the nearest bone,
  softened between bones.  Without one, the height bands of a standing
  figure tell the head, the neck, the torso and the legs apart; a bust or a
  hand can be told what it is.  Seven regions, each with a multiplier for
  each kind of mark and for the oiliness and the flush, starting from where
  marks tend to fall -- acne on the face, the chest and the back, freckles
  on the arms, red knuckles, a shining forehead -- and each editable in the
  new **Body Regions** group.  The map behind it is a small volume of region
  weights over the scene, built off the thread when the scene or the bones
  move, that the shader reads at the same world position as the pores.

### Changed

- Rebuilding a form from planes no longer stops the window with a wait
  cursor: it is cut on a thread, the last stand-in stays up until the new
  one lands, and a setting turned meanwhile asks for one more rebuild
  rather than one per value it passed through.
- The Pose tab says whether a skeleton's skin came with the model or was
  made here, and for which object.

## [2.4.0]

### Added

- **Several models in one scene.** `File > Add Model` (`Ctrl+Shift+O`) puts a
  second, third, tenth model into the scene beside the first, each an
  *object* with a name, a place and a solidity of its own.  The **Model** tab
  lists them as a tree: rename a row, tick it to show or hide the object, and
  drag its solidity bar to ghost that one object -- the same see-through the
  Shading tab applies to the whole scene, one object at a time.  When every
  object is hidden the viewport says so.  One object is active: the one the
  panel's boxes describe and the tools move.  Everything the viewer already
  did -- picking, measuring, the section, the pedestal, the planes, the
  shadows, the skin tracer -- reads the scene as one mesh and needs no
  telling.

- **Move, turn and scale by hand.** `T` arms the transform tool: the active
  object grows a gizmo of three arms and a ring.  Drag an arm to move along,
  turn about or scale along that axis; drag the ring for a free move across
  the view, a turn about the line of sight, or a scale of the whole.  `Shift`
  snaps a turn to round angles, `Esc` cancels, and every drag is one undo
  step.  Position, Rotation and Scale boxes take exact numbers; scaling acts
  on all axes together unless told otherwise.  While the tool is armed, `W`,
  `E` and `R` choose the gesture -- move, rotate, scale -- ahead of whatever
  else those letters do.  Clicking another object with the tool armed makes
  that one active.

- **Picking an object by eye.** `Alt`-click an object in the view and it
  becomes the active one, whichever tool is armed, as in ZBrush (an `Alt`-drag
  still orbits).  Whichever way an object becomes active -- a click, a row in
  the list, an Add or a Duplicate -- a line is drawn round its edge for a
  moment and then fades, so the eye can find it among the others.

- **Clipping planes by hand.** The near and far planes have always been fitted
  to the scene each frame; **Set by hand** under Clipping in the Camera tab
  now takes them over.  The two bars start where the fit left them and hold
  still as the camera moves -- pull the near plane in to look inside a model,
  or push it out for finer depth where the model is -- and untick to hand
  them back.  They are saved with the session and with each saved view.

- **Duplicate.** A button in the Model tab, and `Model > Duplicate Object`,
  make a copy of the active object standing exactly on top of it, ready to be
  moved aside.  Only the mesh is copied: a rig stays with the original, and
  so do the children.  The copy has no file until the session is saved.

- **Linking.** Drag a row onto another in the Model tab -- or choose a Parent
  -- and the object follows its parent's moves, turns and scales, keeping its
  place at the moment it is linked.  The tree shows the hierarchy the way an
  outliner does.  What else a child follows is set under **Linking**: hiding a
  parent hides its children, a parent's solidity is handed down, and removing
  a parent re-hangs its children rather than removing them, each of which can
  be turned the other way.

- **Merge and split.** Merge the selected objects into one mesh standing
  where they stood, or split an object into its loose pieces -- the parts that
  share no vertices -- each an object of its own.  An object made this way has
  no file until the session is saved, when it is written out as an OBJ beside
  the session.

- **A grid.** A ground grid, on by default, and two more for the walls behind
  and beside the model, under **Shading > Grid**.  Lines, spacing (or a round
  number picked to suit the scene), a heavier line every so many, colour,
  width and solidity are all settable; the world axes are drawn through the
  grid in their own colours; and the lines fade with distance from the camera,
  by a settable multiple of its distance to the grid.  The ground sits under
  the scene's lowest point unless told to pass through the origin.  An
  exported clip can leave it out.

- Sessions are at version 9 and carry the objects, their places and their
  parents; older files load as before, as one object at the model's path.

### Changed

- A rigged model's skeleton moves with the object it is bound to, so a figure
  can be placed and still posed.  Measurements, annotations, armatures and
  forms are marks in the scene rather than on any one object, and stay where
  they were made when an object is moved.
- The orientation setting applies to every object in the scene.

## [2.3.0]

### Added

- **Human Skin shading.** Fast navigation preview and progressive idle rendering
  with ray-traced soft shadows, one diffuse light bounce, sampled subsurface
  diffusion, and thickness-dependent backlighting. Geometry preparation runs in
  the background; changes to the view or scene restart refinement automatically.
- Skin tone presets and saved controls for colour, roughness, reflection strength,
  oily highlights, scattering depth/colour, transmission, light size, exposure,
  indirect lighting, sample count, and refinement resolution.
- **Skin surface detail without UVs.** Pores and furrows come from a tileable 3D
  relief volume sampled at world position, with separate normals for highlights,
  diffuse and scattering. Burley's diffusion profile replaces the single
  exponential, read from a curvature-indexed table while navigating and sampled
  while idle. Pigment mottling, blood flush, coloured occlusion and a peach-fuzz
  rim, with controls for surface detail, pore size, tone variation, blood and fuzz.

## [2.2.0]

### Added

- **Pose.** A skeleton in the sense a rigging application means it: every
  joint but the root hangs from a parent, turning a joint carries everything
  below it, and a model that came with skin weights follows the bones.  A
  rigged GLB or glTF brings its skeleton in with it -- the joints, their bind
  matrices and the weights that tie the vertices to them -- and the figure
  is posable the moment it opens.  Posing is by pulling, as a bone is turned
  in 3ds Max once it is picked: drag a joint and the bone above it swings to
  follow, carrying the limb; drag a root and the figure moves; `Shift`+drag
  rolls a joint about its own bone, `Ctrl`+drag pulls it in depth.  Each pull
  is one undo step.  The **Pose** panel lists the joints as the tree they
  are, turns the selected one by three sliders, re-hangs it from another
  joint, resets a joint, a branch or the whole pose, and says whether the
  model follows the skeleton at all.  `B` arms the tool; with it armed, a
  click that lands on nothing adds a joint under the selected one, so a
  skeleton can be built by clicking along it as an armature is.

- **A humanoid skeleton preset**, proportioned to the model's height and
  stood on the bottom of its box, with the same roles the guided armature
  uses.  A starting point rather than a fit: in **Fit** mode dragging a joint
  moves where it rests and its children stay put, so the knee is pulled
  into the knee without the ankle following.

- **Armatures and skeletons convert into one another.**  An armature is a
  graph and a skeleton is a tree, so a skeleton is *grown* out of an
  armature from a root -- the node selected in the Armature tab, else the
  pelvis, else the best-connected node -- and any bone that would close a
  loop is left out and counted, which the status bar says.  A guided
  humanoid comes across whole.  The other way, any skeleton lays an
  armature under itself as it is posed, roles and all, so the clay modes can
  read a figure off a rig that arrived with the model.

- **Rigs are read as figures by their names.**  Joints named the way Mixamo,
  3ds Max's Biped, Unreal, Blender's Rigify and Character Creator name them
  are recognised -- `LeftUpLeg`, `Bip01 L Thigh`, `thigh_l`, `thigh.L`,
  `CC_Base_L_Thigh` are all the left hip -- and a model whose rig reads as a
  humanoid is offered the mapping when it opens.  The guess is a guess, and
  each joint's Role box is where to correct it.  The role vocabulary is the
  armature's, so the two agree about what a figure is, and a Biped or any
  other naming that arrives later only needs its names added to one table.

- **Simplify a rig.**  A game rig carries a hundred joints and a pose is
  read from twenty of them, so **Simplify** takes out the fingers, the toes
  past the ball, the face, the breasts, and the twist, share, roll and end
  helpers, by their names, and re-hangs what is left from the nearest joint
  that stayed.  A joint with a humanoid role always stays, and the skin
  weights of what went fold onto the joint that took its place, so the model
  still follows.  One undo step.

- **Sessions keep the pose.**  The skeletons, their roles and the pose each
  stands in are written into the session; the skin weights are not, since
  they are the model's, and are read back out of the model file and matched
  to the joints by the names the file gave them.  A joint you have deleted
  hands its weights to the nearest ancestor that still exists.  Sessions from
  earlier versions load unchanged.

### Changed

- The glTF loader reads the first skin of a file and puts the vertices
  where the file's own joint transforms put them, which is where every other
  viewer shows them.  A file saved mid-pose opens mid-pose and unbends.
  Files with no skin load exactly as before.
- Turning a model with the Model tab carries its skeletons with it, as it
  does the armature.
- The video export's "Armature" switch now also covers the skeleton.

## [2.1.0]

### Added

- **Hotkeys.** Every key is yours to move. Ctrl+Alt-click (Cmd+Option on a
  Mac) any button or switch in a panel and press the key to put on it; the
  menus' entries and the view's single letters are listed under
  **Settings > Hotkeys**, each with a box to press a new key into. A key that
  is already in use is not taken silently: you are told what it does and
  asked. A control with a key on it says so in its tooltip, and the buttons
  that arm the tools show the letter after their name, as the menu entries
  do. What you change is kept on the machine, apart from the session.

- **Open a file from the desktop.** A model, a session or a matcap image
  opened with the viewer from the desktop's "Open with" menu, or dragged onto
  the application itself, opens as what it is. The macOS bundle declares the
  file types so that Finder offers it. Any number of files may be named on
  the command line, in place of the single model it took before.

### Fixed

- **Showing an armature no longer halves the frame rate.** The overlay tests
  every node against the surface on every frame of an orbit, and on a large
  scan each of those tests swept every leaf of the picking index. The index
  now boxes its leaves up in levels and descends only into what the ray
  enters; the rays for a frame's nodes are cast together in one pass; and the
  camera keeps the projection it last built rather than rebuilding it for
  every marker. On a two-million-triangle scan the cost of a visible wire
  with two dozen nodes falls from around a third of a second a frame to a few
  milliseconds. Hovering and painting are faster for the same reason.

- **Dropping a file on the window works again.** The window let a file in
  and then refused it on every move, which is where a drop is decided.

- **The release check works on macOS.** Python there, and a frozen build
  anywhere, could not verify GitHub's certificate and reported an SSL error.
  The check now trusts the `certifi` bundle, which is shipped with the app,
  and falls back to the Mac's own system root certificates.

## [2.0.0]

The interface is rebuilt around the way ZBrush is worked: every panel goes
anywhere, every control can be copied out to where it is wanted, and the
things that are yours rather than the model's have a window of their own.
Sessions from 1.x load unchanged.

### Added

- **Panels that go anywhere.** Every panel is a dock of its own: any edge of
  the window, stacked into a tab strip with others, or floated. Docked to the
  top or the bottom, a panel's groups break into columns to use the width
  rather than squeezing. Every group folds away behind its own bar, and a
  group whose settings have gone dead folds itself. The controls the panels
  are built from -- the sliders, the swatches, the folding frames -- are drawn
  by hand so that they wrap, reflow and stay legible however narrow the dock
  is pulled.

- **Copy any control out of its panel.** Hold `Alt` and drag a control -- or
  a group's bar, for the whole group -- into a panel of your own
  (`Ctrl+Shift+N` opens an empty one; its right-click menu adds, names and
  removes the groups in it, and names the panel).
  A copy is a second pair of hands on the same control, not a second setting:
  move either and both move. Drop a copy on the model to be rid of it. The
  arrangement, and every panel you have built, is remembered between runs and
  written into the session file.

- **Preferences.** `Ctrl+,`, or the Settings menu for one group of them: the
  accent colour and type size, orbit and zoom speed and direction, the splash
  screen, the release check, whether the machine is kept awake, reopening the
  last session, the viewport's multisampling, anti-aliasing and frame counter,
  and a folder of your own matcaps. Every change applies as it is made,
  multisampling excepted, which says so.

- **The matcap is its own control.** The sphere under the gallery is drawn
  with the grading applied and is dragged rather than described: drag to
  turn it, `Shift`-drag for brightness and contrast, `Ctrl`-drag for
  saturation and gamma, double-click to put the grading back. What is drawn
  is exactly what the shader does. Right-click it to save the matcap as an
  image, graded or as it came. The Matcap panel itself has moved into the
  Shading panel and appears when Matcap is the mode.

- **Contour shading.** A new shading mode cuts the form with a stack of
  evenly spaced planes and draws the cuts, the way a contour map reads land.
  The lines crowd where the surface turns across the planes and spread where
  it runs along them, so curves and flats read at a glance. The planes follow
  the camera by default, or face X, Y or Z, or are pinned the way the camera
  faced with `Slice Along the View`; density, width and colour, the paper
  between the lines and whether it is lit are all adjustable.

- **Anti-aliasing at runtime.** FXAA, or supersampling at twice the size,
  chosen in Preferences and applied at once -- the frame is drawn into a
  buffer of the renderer's own and smoothed on its way to the screen -- beside
  the multisampling that is fixed when the window is made.

- **A frame counter**, in whichever corner of the viewport you ask for; it
  keeps clear of the readout and the orientation gizmo.

- **A gesture for depth.** Markers -- measurement ends, armature nodes, every
  kind of landmark -- go inside the model or off it by `Ctrl`/`Cmd`-dragging
  them: up moves deeper, down moves toward the camera, along a fixed axis
  through the point. A fading ruler beside the point shows the signed travel,
  and a grid facing the camera is laid through the point in the scene, where
  the model stands in front of it or behind it and says which. Escape puts
  the point back. The `Free points` switches are gone; the gesture replaces
  them.

- **One kind of marker.** Every marker in the viewport is drawn by one
  object, so they share a shadow against the surface, a highlight when
  grabbed, and a faded body inside a dashed ring when they sit behind the
  surface rather than on it.

- **A rail for the cut.** While a section is on, a rail at the right edge of
  the viewport, in the contour's colour, slides the plane along its normal
  over the same range as the panel's slider. It is the depth ruler's own cue,
  and stays put while the view turns.

- **The selected measurement** is highlighted in the viewport when picked in
  the list.

### Changed

- Matcap textures are kept at sixteen bits and the shading dithered, which
  takes the colour banding off gradients.
- Every piece of text drawn over the model -- the readout, the labels, the
  depth ruler, the section rail -- is drawn as filled outlines with a dark
  halo, so it reads over the model and the background alike on every driver.
- Session files are at version 7: they carry the arrangement of the panels.

## [1.12.0]

### Added

- **Freeform forms.** The Forms tab now offers `Freeform` beside the pelvis,
  the ribcage and the head, and those three turn out to be special cases of
  it: put down whatever landmarks you choose, name them as you go, and the
  form is the convex hull of them. A hand, a knee, a breast, a nose, a
  clavicle, a scapula, a muscle, the fat over a hip -- any of them is a few
  points and a hull. Each landmark is placed as centre, left or right, and
  the side carries over from one to the next until you change it; the names
  are numbered for you if you do not type any, and can be changed in the
  list afterwards. The fill is yours: **Faceted** is the hull as it comes,
  planes meeting at edges, for bone; **Smooth** bows each face of that hull
  out into a cubic patch between the points -- a point-normal triangle,
  tangent at each corner to the surface there -- and hulls the result, for
  muscle and fat. Either way the clay passes through every landmark. A left
  or right landmark is mirrored across the median plane as a preset's is
  once enough of the midline is down; placed on both sides by hand, the two
  are a pair and the symmetric build averages them. A freeform with no pair
  at all is left as placed rather than pressed onto a plane. `Back` takes
  the last landmark off again, and every placement, rename and refit is one
  undo step. A finished freeform can be taken up again: select it in the
  list and press `Append` to add landmarks to it.

- **Free points for freeforms.** A `Free points` switch in the Placement
  group puts a freeform's landmarks anywhere in space -- inside the model,
  for a mass the skin only hints at -- on the plane facing the camera, as the
  measure tool's free points go. The presets ignore it: their landmarks are
  anatomy on the skin.

- **A switch on every tab that draws something.** The Planes, Section,
  Measure, Annotate, Armature and Forms tabs each carry a checkbox in the tab
  itself that shows or hides what that tab puts on the model, so the clay,
  the cut, the measurements, the strokes, the wire and the forms can be taken
  off the model without opening the tab. It is the same switch as the one in
  each panel's Display group, and the two always agree.

### Changed

- The Forms panel's `Primary forms` group is now `Build`, and the menu's
  `Start Primary Form` is `Start Form`: with the freeform in it, the panel
  builds every form of the figure, primary or not.

## [1.11.0]

### Added

- **Block the figure in with its primary forms.** A new Forms tab builds the
  big simple masses a sculptor starts from, in clay, over the model: the
  pelvis as a bucket with its front corner chipped off along the plane from
  the two ASIS down to the pubic symphysis; the ribcage as an egg lofted from
  the thoracic inlet through the widest ribs to the lowest, with the arch
  chipped out of its front along the costal margins point by point -- the
  corners of the rectus abdominis beside the xiphoid, where its outer edge
  crosses the ninth rib, the corner at the tenth -- so the arch curves in
  under the ribcage as a real one does, the margin being the bottom ring of
  the egg itself so that its surface passes through every one of those
  points before it is chipped along them, its front flattened to the front
  corners of the ribcage where the cartilages turn back from the
  breastbone, and its back bowed at the apex of the thoracic curve; the head as a wedge that is given its
  width, the block of its cranium and its jaw in turn.  Every form is planes
  meeting at edges, the head included, because planes are what a block-in is
  for.

  None of those masses can be pointed at on a model -- nobody can find the
  axis of the pelvic bucket -- but every one of them is pinned down by anatomy
  that *can* be found on the surface, so each form is a guided walk like the
  armature's. Pick the form, press Start, and click the landmarks it asks for;
  the form is worked out from them and grows as they go down. Place the
  midline and one side and the other is mirrored across the plane fitted
  through the midline.  Nothing on the lists is anatomy a pose or a body can
  hide: the sitting bones, buried on most models, are asked for but not
  waited for -- skip them and the bottom of the bucket is put where they
  are, from the hip points -- and the trochanters are not asked for at all.

- **A head arrives in stages, and the stages are kept.** A wedge first -- the
  profile of the head as a thin slab, which is where a head is read from --
  then its width from the skull, the cheekbones and the corners of the jaw,
  then the cranium planed out over that to the bulges of the forehead, the
  corners of the crown and of the back of the skull and the mastoids, then
  the jaw and muzzle as one lump, and last the nose -- the first secondary
  form, a wedge from its root to its tip and out to its wings, laid on the
  muzzle. The landmarks are asked for a stage at a time, so the head thickens
  under your hand as the paired points follow the midline ones, and a slider
  in the panel scrubs back through every stage afterwards. Clay goes on and
  does not come off: each stage is laid over the ones before it rather than
  cut out of them, which is why the head starts as a wedge that is widened
  rather than a ball that is sliced -- and why it is widened above the eyes
  and below them, and not between. The eye sockets are the gap left between
  the cranium and the jaw, and nothing is ever laid into them.

- **The forms are built symmetric.** The pelvis, the ribcage and the skull
  are bone, and bone is symmetric to within less than a click's error, so by
  default each form is worked out from its landmarks made exactly symmetric
  about the median plane: the midline points dropped onto it, each pair
  averaged across it. The landmarks stay where you put them; only the clay is
  straightened. A switch in the panel builds from the points as placed.

- **A form is its landmarks.** The clay is worked out again from them
  whenever it is drawn, so a landmark dragged in the view or nudged from the
  panel re-forms the clay under it, every placement and every move is one
  undo step, and a session file carries a dozen points per form rather than a
  mesh. The forms are drawn with the model rather than in place of it, in a
  clay colour of their own, and throw shadows and take occlusion like
  anything else on the pedestal. Ghost the model -- the switch is in the
  Forms tab as well as the Shading tab -- to read the clay standing inside it.

- Under the hood, every primary form is a union of a few convex solids, each
  the hull of some sampled points or such a hull with a plane cut through it.
  That is the same family of shapes the clay modes already work in, and a
  small hull-and-cut kit is all the geometry it takes.

### Changed

- **The armature's hip no longer asks for the greater trochanter.** A bent
  hip swallows it, so it was the one landmark on the list a pose could hide.
  The femoral head is now placed from the two hip points and the two dimples
  alone -- a fixed share of the width between the ASIS in from each, and a
  little below and behind it, which is the rule gait laboratories use to find
  the joint centre from the same markers. Eighteen placements now rather than
  nineteen. Sessions that carry a trochanter still load; it is simply no
  longer read.

## [1.10.0]

### Added

- **Hand the making to someone who was not there.** The film a form's making
  is recorded as can now be written out as a file: *Export Video...* under the
  scrub slider, or `Ctrl+E`. Every stage becomes a frame, held on screen for
  as long as you say -- a fifth of a second is the block-in arriving at about
  the pace of a hand, half a second is a lesson, two seconds is a slideshow of
  block-ins -- and the finished form is left standing at the end for a moment
  rather than being cut away from the instant it arrives.

  The timing is asked for in seconds per stage rather than in frames per
  second, because a stage is not a frame of anything. It is a step in the
  making, and how long it should be looked at is a judgement about reading a
  form. What the file does with that is the file's business: MP4 and AVI hold
  each stage for as many frames as it takes, and a GIF carries the delay
  itself.

  MP4 for a portfolio or a lesson, AVI for an editing suite that will not take
  one, GIF for sending to another artist because it plays by itself in the
  message it arrives in, and WebP for the same errand at a quarter of the
  size.

- **A clip is not a screenshot, so it is composed rather than captured.** The
  export window is its own set of choices, laid over how you have been working
  rather than replacing it. Pick the frame size -- up to 4K, or the shape of
  the viewport so the framing is the one you have been looking at -- the
  shading mode, whether the form is ghosted, wireframed, standing on its
  pedestal. Then tick which of the helpers are in shot: the readout naming a
  file and a triangle count earns its place while you work and is clutter in
  something you send, and the armature that told the clay where the masses go
  has done its job before anyone presses play. Everything you do not name --
  the matcap and how it is graded, the light rig, the section cut, the
  colours -- comes out exactly as you left it.

  Which stage this is can be burned into the corner of every frame, with the
  count of solids and the Detail setting that rebuilds it, so a viewer can
  stop the clip somewhere worth keeping and go and get it.

  The frame beside the options is a real one, rendered through the path the
  export will use at the shape the export will have, and it follows every
  change. A window full of checkboxes whose effect you only find out about
  after waiting a minute for a file is a window people fill in twice.

- **It runs in the background, and it can be stopped.** Rendering a hundred
  stages at 4K is a minute of work. It is done a frame at a time off the event
  loop with the encoding on a thread behind it, so the window answers
  throughout -- including answering Cancel, which leaves no half-written file
  behind.

- **A GIF needs nothing installed.** The other three formats are ffmpeg's job,
  and if there is no ffmpeg the window says so in words you can act on rather
  than failing when you press the button. GIF is the exception: it is written
  here, palette and LZW and all, so the one format an artist actually sends
  someone works on a machine with nothing on it. Where ffmpeg *is* present it
  is used for GIFs too, being better at the palette and faster at the rest.

## [1.9.0]

### Added

- **Clay built on the armature, the way clay is really built.** The additive
  geometry mode can now be given an armature to stand on. Pick one under
  *Planes → Simplify geometry → Built on*, and instead of asking the distance
  field where the masses of the form are, the mode asks nobody: a lump is laid
  along each length of wire, centred on it, and pushed out until either the
  model or the thickness the wire declares at its ends stops it. The pelvis is
  the pelvis because you said so by bending the wire, not because it happened
  to be the deepest material anything could find.

  Bones are named now rather than being anonymous pairs of indices, because
  what a sculptor lays down is a *thigh*, not a *hip to knee*. A wire derived
  from the humanoid preset arrives already in the order a figure is built up --
  hips, then the ribcage, then the head, then the limbs largest mass first,
  both sides of one before either side of the next -- so a block-in stopped
  half way is a figure standing evenly rather than one limb modelled and its
  pair still wire.

  Detail and Masses keep their meanings and gain the wire's. Detail decides how
  far down the bone list the clay gets, and what it has not bought is greyed in
  the list rather than hidden, so you can see what one more step would buy.
  Masses says how many of the first lengths of wire are laid as plain
  rectangular blocks before the rest arrive as bevelled tubes. And detail spent
  past the end of the wire is still found the old way -- the armature is a
  guide, not a cage -- which is what puts the hands and the feet in after the
  block-in is standing.

  Bend a node and the clay follows it when you let go, the same bargain the
  geometry sliders make. Record the making and the film scrubs through your own
  order rather than through a reading of the field.

- **Which bones take clay, and in what order, is yours to say.** The bone list
  in the Planes panel is the armature's own, so reordering it is an edit of the
  document: one undo step, and a nudged landmark no longer puts your order
  back.

  Untick a bone to keep the clay off it altogether -- not merely to skip its
  lump, but to leave that part of the form bare and keep it bare. However far
  you then push Detail, nothing seeds there and nothing grows in: the material
  under a bone that takes no clay leaves the lattice before anything is laid at
  all. Which is the difference between the parts of a figure you want blocked
  in and the parts you mean to model yourself. The bone is still wire, still
  drawn and measured and holding its two joints apart. How wide a berth the
  clay gives it is the thickness its two nodes declare, and material a bone you
  kept also reaches stays with that one, so turning the hand off does not take
  a bite out of the forearm it shares a wrist with.

  Rows come in handfuls, so they are picked in handfuls: Ctrl-click or
  Shift-click as many as you mean and ticking any one of them ticks the lot, as
  a single step. *All* and *None* do the whole list, which is the quick way to
  start from one end -- None, then tick back the four bones you actually want.

## [1.8.0]

### Added

- **A wire under the form, before any clay goes on.** The new Armature tab lays
  out a graph of named nodes joined by bones. Nothing is animated by it: there
  is no skinning, no weights, no rig. It is there to be read off the screen
  while you bend real wire to length, and -- shortly -- to tell the clay mode
  where the masses of a figure actually belong instead of letting it infer
  them from the distance field alone.

  Every node carries how thick the form is where it sits, as a radius in scene
  units rather than as a dot on the screen, so a ring grows as you zoom in and
  reads as the body rather than as a handle. Press `R` and click to place nodes
  along a limb, each joined to the last; drag one to move it, `Shift`+drag to
  change its thickness. Nodes can be dissolved out of the middle of a chain
  without breaking it, joined across to close a shoulder or a pelvic bar, and
  locked once they are where they belong. Every one of those is a single undo
  step.

  An armature lives inside the model, so hiding the buried half would hide
  almost all of it. It is drawn over the form instead, and the part standing
  behind the surface is dimmed rather than cut away -- still readable, still
  clearly on the far side of the skin.

- **A guided humanoid preset, which asks for anatomy rather than for joints.**
  Instead of placing the nodes by eye, you can walk a list of landmarks and let
  the figure be worked out from them. Each one is a bump or a hollow you can
  actually find on a model -- the C7 bump at the base of the neck, the jugular
  notch, the two hip points, the epicondyles either side of a knee -- and never
  a joint centre, because nobody can point at the middle of a femoral head. The
  hip is placed a quarter of the way from the trochanter you *can* feel towards
  the centre of the pelvis, which carries it medial and a little up and back,
  where it really is. Asking for what is visible and inferring the rest is both
  less to point at and more accurate than asking for the guess directly.

  Every rule is a ratio of the figure's own measured spans rather than an
  absolute distance, so one preset fits a child and a heroic nude, and nothing
  drifts when the pose changes. The paired landmarks then pay for themselves
  twice: the two epicondyles that locate an elbow are also the width of the
  elbow, so every joint arrives already sized and the artist is never asked for
  a thickness at all.

  Place the midline and one side and the other is reflected across a plane
  fitted through the midline landmarks -- nineteen placements rather than
  thirty-three. A mirrored point is drawn hollow so a guess reads as a guess,
  and correcting one makes it yours, because the mirror never writes over a
  point you have taken hold of. A midline too nearly straight to fit a plane
  through is refused rather than guessed at.

  The landmarks are kept afterwards, not consumed. Nudging one re-derives the
  nodes that read it, so a misplaced ASIS is a correction rather than a restart.
  A locked node keeps its place and its size through that -- one padlock, one
  meaning -- and moving any node by hand hands the armature over to you and
  stops the re-derivation, in the same undo step, so one `Ctrl+Z` puts it back
  under the preset.

- **The landmarks are a list you can edit, not a record you can only read.**
  A Landmarks group in the Armature panel lists every point you placed, in the
  preset's own order down the figure rather than in the order you happened to
  get to them, so a skipped point and every mirrored one still read as anatomy.
  Selecting a row rings that cross in the view, so the name and the point on
  the model are obviously the same thing.

  Each one has its position in `X`, `Y` and `Z`, in whatever unit the Measure
  panel is set to, stepping by a hundredth of the model so an arrow key is a
  nudge whether the figure is two units tall or two hundred. Move one and the
  joints that read it follow immediately -- the promise the guided preset has
  always made, now with something to nudge it with. Each committed number is
  one undo step, not one per digit.

  A cross can also just be dragged in the view, the way a node can, which is
  how a landmark put down a centimetre off gets corrected: the figure re-forms
  under the cursor and the whole drag lands in the history as one step. A cross
  lights up as the cursor crosses it, and it answers within a tighter reach
  than a node handle -- half the joints of a preset sit right beside the
  landmarks that placed them, so aiming at the cross picks the cross and a few
  pixels out picks the node. Dragging a mirrored guess makes it yours, exactly
  as typing over it does, and a landmark clicked rather than dragged selects
  its row instead of moving anything.

  Deleting a landmark takes any guess mirrored from it along, rather than
  leaving a cross anchored to nothing. And an armature you have taken over by
  hand keeps the nodes you made: its landmarks stay a record of where the
  anatomy is, editable without the wire moving under you, and *Rebuild Nodes*
  is how you deliberately hand it back to the preset -- keeping your names and
  whatever you locked.

- **Ghost shading.** A checkbox and a solidity slider in the Shading panel draw
  the model see-through. A reference is often something you want to look *into*
  rather than at, so what comes back is every surface along the view laid over
  the others -- which reads as glass rather than as a hole. It works under every
  shading mode, and the pedestal stays solid under it.

  The surfaces are not ordered at all, which is what makes the result the same
  from every angle. Blending is not commutative, and a ghost drawn in whatever
  order the triangles happen to sit in the file turns to haze at a low solidity
  and to wreckage at a high one, with the back of a skull painted over its
  face. Sorting a form per triangle every frame is out of the question, so each
  fragment is summed instead: the colours averaged by how far through the form
  they lie, the transmittances multiplied, and the two divided out in one
  fullscreen pass at the end. Addition does not care what order it happens in,
  so the answer holds for however many surfaces a pixel covers -- and it costs
  one draw call over the geometry, not two. A ghost at full solidity is
  indistinguishable from a solid model, which is what the top of the slider
  ought to mean.

### Changed

- Sessions are now version 5 and carry the armature, its landmarks and its
  display settings, and version 5 also carries the ghost settings. Older files
  still open, with an empty armature and ghosting off.
- The armature list sits in a splitter, so a figure with thirty nodes can be
  given the height to show them.
- A node picked in the view now actually highlights its row in the list. The
  row was made current but never selected, because it was asked for before the
  armature it hangs under had been put in the tree.
- Arming a tool is written once rather than as a pairwise dance between every
  two of them, which is what a third tool made worth doing.

## [1.7.0]

### Added

- **The making of a form, not just its end.** Both geometry modes now record
  every stage a form passes through and let you scrub back and forth along it
  with a slider. A block-in is a sequence before it is a shape -- which mass
  went down first, what the second cut took off, where the thing stopped being
  a block and started being a body -- and that sequence is the part a sculptor
  learns from.

  It is read out rather than reconstructed. Both modes already work one solid
  at a time: stone splits the block holding the most air, over and over, so the
  form in *k* blocks is the form in *k+1* with the last cut not yet made; clay
  lays each lump into whatever the ones before it left bare, so the first *k*
  lumps *are* the form at *k* lumps. In additive mode the masses go down first
  and the detail follows, which is the order a figure is actually built in.

  Every stage is the form exactly as the *Detail* slider set that far would
  build it -- finishing passes and all -- so what you scrub past is what you
  could stop at. The panel says which *Detail* setting would rebuild the stage
  you are looking at, and says nothing where no setting would: clay's masses
  arrive together, so a film shows them landing one by one but the *Masses*
  slider cannot ask for half of them, and claiming otherwise would be a lie.

  Recording runs in the background. The stages become scrubbable as they land,
  coarsest first, and the slider grows under the handle rather than appearing
  whole at the end -- so a film you are half way through recording is already
  a film you can scrub. Changing anything a stage is built from abandons the
  recording in flight rather than queueing another behind it, and *AutoSmooth*
  deliberately does not: it re-reads normals rather than rebuilding a form, so
  a film survives it.

  Scrubbing itself is free. Every stage was built when the film was recorded,
  and moving the handle only picks one.

### Changed

- The expensive half of a carving -- reading the model into a lattice and
  finding its distance field, about a second on a figure -- is now laid once
  and shared. A whole film of dozens of stages therefore costs a few times one
  build rather than dozens of them.

- **The settings a film is being recorded from are held still while it
  records.** A film is a walk through one set of settings, and changing one
  part way through does not make a film of the new settings -- it makes a
  recording of one form wearing another form's label. *Detail*, *Method*,
  *Masses*, the finishing passes and the design matrix all go quiet for the
  duration, with a note saying why.

  The scrub slider deliberately stays live, because being able to watch the
  form arrive while it is still arriving is the whole point of recording in
  the background; so does *AutoSmooth*, which only re-reads normals and cannot
  change a stage's shape. Unticking *Record the making* cancels a recording
  and gives everything back.

### Fixed

- **Changing a setting while a film was recording crashed the program.** Not
  an error dialog -- an abort. Abandoning a recording dropped the last handle
  to a thread that was still running, and Qt answers that by taking the
  process down rather than trying to unwind it. Since every settings change
  abandons the recording it no longer wants, and a slider drag makes several,
  this was easy to meet.

  An abandoned recording is now held until it reports that it has really
  stopped, and only then let go of. The window waits for one on its way out
  too, because a live thread meeting an interpreter that is dismantling itself
  is the same crash wearing a different hat.

## [1.6.1]

### Fixed

- **The pass that closes the clay's seams no longer eats the form it is
  mending.** *Simplify Geometry* in additive mode lays lumps of clay into the
  model, and two lumps crossing at an angle leave a slot between them -- a
  dark slit to the eye, and a spike to the thing that finds the surface. That
  slot was being closed with a median filter, which was the wrong tool for a
  reason worth stating: a median closes a slot because the material either
  side of it outvotes it, and by the very same arithmetic it shaves a convex
  corner because the air on more sides of it outvotes *that*. One pass took
  the slots out and a slice of the form with them; the corners and thin walls
  the mode exists to show were the first thing to go.

  What a sculptor does about a slot is press clay into it, so that is what
  this does now. It works the solid rather than the field -- the clay is grown
  a cell or two into the slot and the surface is then let back the same
  distance, which leaves the fill in the slot and nowhere else -- and it only
  ever *adds*. Nothing is taken away, so no corner is shaved, no thin part is
  thinned, and a flat comes through untouched to the last digit.

  Measured on a posed figure, the fill now hands back about five per cent more
  of the form than it used to take away, and the share of the surface lying in
  the planes of the fit -- which is the whole point of the mode -- rises by
  something like two thirds. The *Median* sliders in *Finishing* are now
  *Fill seams* and *Fill size*, and the trade they used to make is gone: more
  passes close wider slots and none of them make the form smaller.

- **The clay may now be detailed twice as far.** The ceiling on the tubes laid
  into the block-in rises from sixty-four to a hundred and twenty-eight. It
  was held low because a form built from many crossing tubes used to read as
  rubble -- but the rubble was the median shaving the ridges between them
  rather than the tubes themselves, and with the seams filled instead of
  shaved the extra lumps land clean. At the fine end of *Detail* the clay now
  covers about eighty-five per cent of the model where it covered eighty, and
  still reads as flats.

## [1.6.0]

### Added

- **The planes can now be cut into the form itself, not only into its
  shading.** The Planes tab has a *Simplify* choice at the top with two
  mutually exclusive settings. *Simplify Normals* is everything the tab did
  before: the geometry is left alone and each shading normal is rounded onto
  one of the planes, so the model reads as blocked-in flats while its
  silhouette stays round. *Simplify Geometry* moves the surface onto those
  planes instead, so the form really is faceted -- straight runs of
  silhouette, hard edges where the planes meet, a wireframe that follows the
  flats, and a shadow to match.

  It is done by working the volume rather than by moving the model's
  vertices, which cannot be made to work at all: a patch of surface wraps and
  a plane does not, so flattening a shoulder onto the shoulder's plane folds
  the far side of it back through the near side, and about a third of the
  triangles on a figure end up inside out. So the model is read into a lattice
  as a solid, cut into blocks, each block replaced by the flats that hold it,
  and the surface found again from scratch. A plane arrives as a cut, which is
  what a plane is to a sculptor.

  The two ways of arriving at a form are both offered, because they do not
  give the same one.

  *Subtractive* is stone. The form starts as the block it would be carved out
  of -- the convex hull of the whole model -- and every step of *Detail* is
  another cut, taken through whichever part of the block is holding the most
  air, with each half hulled again afterwards. So the hollows open up deepest
  first: the gap between an arm and the ribs, then the knees, then the face.
  The result always holds the whole model inside it.

  *Additive* is clay, and it is built rather than cut. The largest rectangular
  block that will fit inside the model without poking out of it anywhere is
  pressed into the form, then another into whatever is still bare, and
  another; on a figure they land in the ribcage, the pelvis and the thighs, in
  that order, because the order is simply where the most uncovered material
  is. A new *Masses* slider says how many of those there are -- a control
  rather than a measurement, because how many masses a form has is a reading.
  It runs from one up to every mass a standing figure has, and the detail is
  laid on top of the masses rather than sharing a budget with them, so a fuller
  reading of the form never costs it any modelling.
  After them come the tubes: every step of *Detail* lays another lump into
  whatever the clay has not covered yet, largest first, so the arms arrive
  before the hands and the hands before the fingers. A tube is grown exactly
  as a mass is but is allowed the form's own planes as well as the three axes
  of the mass it sits in, so it comes out bevelled where the model turns.

  Growing a lump is one question asked twice, and both times the answer is a
  single pass over the model's surface: how far the lump's own shape will
  inflate about its seed before it touches, and then how far each facing in
  turn will push out on its own. Convexity is what makes both exact and what
  makes them cheap -- a lump that holds its seed and some point beyond the
  surface holds the whole way between them, so only the outside points nearest
  the model can ever bind.

  A *Relax* slider runs the pass a sculptor makes last, going over the
  block-in with the flat of a tool so the planes still read but the form is no
  longer quarried out of them. It works on the finished mesh rather than on the
  volume: every pass draws each point towards the middle of its neighbours and
  then pushes it back out by a shade more, which is Taubin's arrangement and is
  what keeps plain smoothing from shrinking the form away over a dozen passes.
  Anything that ends up outside the model is put back onto it -- read between
  the lattice corners rather than at the nearest one, because a surface pushed
  back in steps wears the steps as a ripple running across it in lattice rows.
  Off by default, and it says nothing to stone, which is meant to keep its
  corners.

  Where two lumps cross they would leave a notch, and a form full of notches
  reads as a heap of stones rather than as one body, so the seams are filled --
  in two stages, because they come in two sizes.

  The large ones get more clay. Every pair of lumps lying near enough to be
  joined is given a further piece pushed across the seam between them, shaped
  as the hull of what of each lump lies within a collar of the other, and that
  hull is then pulled back until it fits inside the model exactly as a lump is
  grown out to it. So a join is made of flats like everything else and cannot
  reach through the surface, and a join that has to come in further than the
  lumps are thick is dropped as bridging air rather than filling a seam. The
  collar is what keeps the mode honest: the hull of two *whole* lumps, on a
  form anywhere near convex, is most of the form, and allowing it turns clay
  pressed into a shape into a cast taken from one.

  The small ones are closed in the volume, with a median filter run over the
  field before the surface is read back out of it. A median is the right
  filter here and a blur is not: over a neighbourhood laid symmetrically about
  a point, the median of a field that is planar there is that point's own
  value exactly, so a flat passes through untouched however many passes are
  run, while a one-cell slot is outvoted by the material either side of it, a
  spike by the air around it, and a pinhole closes. An additive form now comes
  back with no open edges at all and a quarter as many places where the
  surface passes through itself.

  This replaced a softened union, which rounded the crease off instead. A soft
  minimum reaches past both of the solids it joins, and the only thing between
  it and the model was the model, so wherever it reached that far the clay came
  back wearing the model's own rounded surface rather than a flat of its own --
  at the fine end of the slider, a quarter of it did.

  Past a point the Detail slider stops adding lumps and starts bevelling the
  ones there are. That is deliberate and it is the thing that took the longest
  to get right: a form built of sixty lumps reads as masses with clean flats
  between them, and the same form built of two hundred reads as rubble,
  because every pair of lumps that cross at an angle leaves a ridge. Closing
  the gaps is the joins' job, not the count's -- a smaller lump dropped into a
  gap only leaves two narrower gaps.

- **The median filter's two ends are on the panel.** *Median* is how many
  passes are run over the clay volume before its surface is read back out, and
  *Median size* how far each reaches, in cells. The size decides which slots
  are within reach at all rather than how hard the filter pulls: a pass
  reaching one cell has material either side of a one-cell slot and closes it,
  and sees as much slot as material in a two-cell one and leaves it alone.
  Both ranges are short on purpose, because a median cuts both ways -- a slot
  closes because it has material either side of it, and by the same arithmetic
  a corner is shaved because it has air on more sides than material. Measured
  on a figure, one pass at one cell leaves the volume where it was; four
  passes at three cells take three fifths of it away. Neither says anything to
  stone, which leaves no slots between its cuts.

- **Soft ends on the Detail and Masses sliders.** Both stop where their useful
  range stops and both will take a number typed into the box past that; the
  slider grows to reach whatever was typed and can be dragged over the wider
  range from then on. A slider covering everything possible would spend most
  of its travel on values nobody wants, and one covering only what is useful
  is a wall -- this is neither.

  Masses now runs to sixty-four, which is past every mass anyone reads a
  standing figure as, and can be typed up to two hundred and fifty-six for a
  form that is not a figure at all. Past the slider's end a block-in stops
  reading as masses and starts reading as rubble: on a figure the surface
  holds a third less of its area in its commonest facings at two hundred and
  fifty-six masses than at thirty-two.

  Detail past its end buys something different from what the slider buys. At
  the end the form already has every plane a fit will give and every block or
  lump those planes buy, and more of them changes nothing measurable --
  doubling the planes to five hundred moved a carving by a hundredth of its
  volume and left the clay where it was. The lattice is what is holding it, so
  that is what the extra range lifts: the same reading of the form, resolved
  finer, which shows as crisper flats and straighter creases rather than as
  more of them. It costs in three dimensions -- at the top a figure comes back
  with three times the triangles and rebuilds in about eight seconds instead
  of three -- and two hundred is where the lattice meets its own memory
  ceiling, so that is the end of it. Nothing at or below the slider's own end
  moves by a hair, so every setting already saved reads exactly as it did.

- **AutoSmooth, on either way of working the geometry.** The same control as
  the one of that name in 3ds Max, and there for the same reason: a facet that
  comes out of a lattice is only roughly one plane, its triangles each leaning
  by a fraction of a degree, so shading every one of them on its own turns a
  clean flat into a mosaic. The slider is the angle at which a turn stops
  being noise and starts being an edge; neighbouring triangles agreeing to
  within it are gathered into a smoothing group and share their normals, and
  anything sharper is left as hard as it was. Thirty degrees is the default,
  because every real plane change on a blocked-in form is a far sharper turn
  than that. Nothing moves -- it is a change of shading and not of shape --
  and it re-reads the normals of a form already built, so it costs a tenth of
  a second rather than the seconds a rebuild costs, and has a cache slot of
  its own to make sure of it.

  The fine end of the slider goes a good deal further than it did in both
  modes. Stone runs to a hundred and ninety blocks over two hundred and fifty
  directions and comes back within a twelfth of the model's own volume; clay
  runs to sixty-four lumps and four fifths of it. Of the two things detail can
  buy the stone, another direction is worth about twice another cut, because a
  direction shaves every block of the form at once while a cut opens one
  hollow -- so most of the slider goes there.

  What comes back either way is a union of convex solids, read off the lattice
  by dual contouring -- one vertex per cell, placed where the planes crossing
  that cell agree. Those planes are exact, so a cell inside a flat lands dead
  on it, a cell along a crease lands on the line where two flats cross, and a
  cell at a corner lands where three do. The flats come out flat to the last
  digit, the creases straight, and the surface closed and free of folds,
  because an isosurface always is. It is also why the clay is joined as a
  volume and never as surfaces: a tube laid across a mass leaves no seam where
  they meet and no sliver where they cross, because there is nothing there to
  stitch, and why the seams between lumps are filled and the slots closed
  before the surface is read rather than mended after it. The model is then held against the result as a floor under the stone
  and a ceiling over the clay, so that one is larger than the model and the
  other smaller by construction rather than by luck.

  Only the *facings* of the fit are used; where each flat goes is decided by
  the material it stands for. The fit's own plane offsets, and all the
  machinery that used to hand individual vertices out to planes, are gone --
  a block asking how far its own material reaches along a direction is a
  better answer than any offset a fit could name.

  **The model is never modified.** Picking, measuring, painting and the
  section cut all still read the real surface underneath. Unlike the shading
  filter, the stand-in is a mesh of its own -- its own vertices and its own
  triangles, a good deal fewer of both -- rather than the model's topology
  with its points moved. Marks already made on the model stay where they were
  made, so they will sit off the flats by however far the flats moved. Cutting
  geometry is real work, so the Detail slider takes effect on letting go
  rather than at every value a drag passes over; the fit is kept apart from
  the carving and only run again when the model or the design matrix changes,
  which makes comparing additive against subtractive, or working the masses,
  free.

### Changed

- **A panel now shows what the mode in front of you can actually be told.** A
  setting that does not apply is taken off the panel rather than greyed out.
  Half the Planes tab belongs to one target and half to the other and the two
  have almost nothing in common, so leaving both up made the panel twice as
  long as the work, and finding the live controls meant reading past a column
  of dead ones. Under a matcap, which carries its own light baked into a
  picture, the light and surface groups are not dimmed versions of themselves
  -- they are questions the mode does not answer -- and the Shading tab is
  less than half as tall without them. The same goes for a thickness on a cut
  that is not a slab, a colour for a line nobody is drawing, and a pedestal
  height that the model is already deciding.

  What is left in the geometry mode is also sorted: how a form is *built* --
  method, detail, masses -- stays in front, and what is done to it afterwards
  -- the median, the relax, the shading -- folds away under *Finishing*.

### Fixed

- **Touching a slider no longer widens the control dock.** How narrow a panel
  will go was decided by whichever of its children insisted hardest, and the
  ones that insisted hardest were the ones holding sentences: a label that
  cannot wrap asks for its whole line at once, so a readout that grows as a
  slider moves took the dock wider with it and never gave the width back. The
  Planes panel would not go below 1176 pixels, and where it settled depended on
  what the sliders happened to say.

  Panels are now made squeezable once, centrally, as they are built: labels
  wrap, so what they ask for drops from a line to a word; combo boxes stop
  asking for their longest entry whether or not it is showing; and check boxes
  and buttons, which cannot wrap at all, are told they may be squeezed and keep
  their full text in a tooltip for when they are. That last one needs both a
  size policy and a minimum width, because a layout only reads a widget's own
  minimum where the policy says it may shrink -- and the default for a button
  is that it may grow and not shrink.

  The one thing still held to a single line is the caption down the left of a
  form row, which names the control beside it and has nowhere to put a second
  line. Every panel now sits between 228 and 340 pixels instead of up to 1176,
  none of them moves when a slider does, and the dock can be pulled to 300.

## [1.5.0]

### Added

- **The design matrix is now yours to argue with.** A *Design matrix* group
  in the Planes tab, folded away by default, exposes the three numbers the
  clustered modes weigh their features with. *Position* says what a whole
  radius of travel across the form counts for against a right angle of turn
  in the surface -- at zero the fit reads facings only, like PCA, and two
  parts of a form that face the same way come back as one plane; wound up, the
  planes become compact patches of surface that happen to face somewhere.
  *Coplanarity* says what the gap between two parallel planes counts for.
  *Flat within* says how far a vertex's neighbours may turn away from it
  before it stops counting as part of a flat, which is what decides how much
  the rounded parts of a form get to vote on where its planes go.

  The same numbers travel through to the shader, so a fragment is still given
  to a plane under exactly the measure the fit was made with and the
  boundaries drawn stay the boundaries between the clusters found. Each is a
  refit, so they take effect on letting go of the slider rather than at every
  value a drag passes over, and a handful of recent fits are kept so that
  going back to a setting just tried is instant. *Reset to defaults* restores
  all three.

### Changed

- **The Detail slider reaches 256 planes, up from 64.** The planes moved out
  of a shader uniform array and into a texture to get there: a uniform array
  is charged against a budget that OpenGL 3.3 only promises 1024 floats of,
  and a driver honouring exactly that would have refused to compile the shader
  outright rather than degrade. A texture has no such ceiling, so how many
  planes the viewer offers is now a question about what the eye can read
  rather than about whose GPU it is running on.

  In the fitted modes the slider now climbs to that count by proportion rather
  than by a fixed step, because that is how the eye reads it: four planes to
  five redraws a form, two hundred to two hundred and one is invisible. A
  side-effect worth having is that raising the ceiling did not move the slider
  under anyone -- the default detail still gives 37 planes where it gave 38,
  and a saved session reopens on the form it was left on. Read as a straight
  fraction of the maximum it would have jumped to 154.

- The merge and the consensus search were rewritten to hold their cost as the
  ceiling rose: the merge keeps each cluster's own cheapest partner instead of
  re-scanning the whole matrix at every step, and the consensus search
  subtracts the surface it has just taken from every proposal instead of
  re-asking all of them. A fit runs from three times as many patches as before
  -- needed, or a plane at the fine end would be quantised to the
  over-segmentation rather than to the form -- in about the same time.

## [1.4.0]

### Added

- **Two more ways to read the planes off a model, both clustering the surface
  rather than only its normals.** *Planes from* now offers Regions and Flats
  alongside Grid and PCA.

  PCA sees a model as a cloud of directions and nothing else, which means it
  cannot tell two parts of a form apart when they happen to face the same way:
  the plane of a cheek and the plane of a temple come back as one direction,
  and the seam the eye expects between them is never drawn. The new modes fit
  planes that carry a place as well as a direction. Every sampled vertex
  becomes a row of a design matrix holding its normal, its position scaled to
  the model's own size, and how far out its tangent plane lies -- so that
  clusters group by facing, by whereabouts, and by genuinely lying in one
  plane. Each row is weighted by the area it stands for and by how flat its
  neighbourhood is, so the flats of the form decide where the planes go and
  the rounded turns between them follow along instead of dragging a plane off
  true.

  **Regions** cuts the surface into a few hundred small patches and merges
  them back together by Ward's criterion, always joining the two that cost the
  least added variance. It is a hierarchy, so every count from 1 to 64 is a
  cut of one tree and the Detail slider refines the break rather than
  rebuilding it, exactly as in PCA mode. It is the one to try first.

  **Flats** asks which single plane the most surface agrees on, takes it,
  removes its surface and asks again -- maximum consensus, which is RANSAC's
  idea without the guessing, because every patch can be tried. The largest
  flat of the form arrives first and the rest in the order a sculptor would
  block them in, and geometry that agrees with nothing is never the winner
  rather than being averaged into a plane it does not belong to. It does not
  nest: a step of the slider re-asks the question rather than subdividing the
  last answer.

  Both settle each plane's direction with an M-estimate rather than an average
  -- the members disagreeing most with the first guess are down-weighted by
  Tukey's biweight and the guess is taken again -- so a handful of bad normals
  inside a patch cannot tilt the plane it is shaded with. Both fit once, the
  first time the mode is picked, off a thinned but fixed sample, and a model
  always breaks the same way twice. A cube gives back its six faces exactly.

  Density methods were tried and rejected on the evidence. A closed surface is
  a connected dense manifold, so DBSCAN and mean shift either chain the whole
  model into one cluster or shatter it into the tessellation: measured on a
  sphere, mean shift went from one plane straight to forty-three with no
  bandwidth in between, which is a slider that does nothing for most of its
  travel. Consensus does not care how the data connects up, only how much of
  it agrees.

### Changed

- **The shader now assigns a fragment to a plane by where it is as well as
  which way it faces**, under the same measure the fit was made with, so the
  boundaries drawn are the boundaries between the clusters that were found. A
  fit made only of directions weights position at zero, which leaves the
  nearest direction and nothing else -- so Grid and PCA are untouched.
- **No boundary is drawn between two planes that face the same way.** A fit
  reading position will divide a broad flat between two planes, and the
  shading runs straight through the join; a line there would say the form
  turns where it does not.

## [1.3.2]

### Added

- **Planes can now be read out of the model itself, by PCA.** The *Planes
  from* box in the Planes tab chooses between the existing fixed grid and the
  new fit. Every vertex normal is taken as a point on the sphere, weighted by
  the surface it stands for, and the cloud is split along its principal axes:
  the first principal component of a group of normals is the direction they
  spread along most, and the group is cut in half across it, always cutting
  whichever group has the most spread left in it. What comes out are the
  planes the form actually has -- the flat of a cheek, the underside of a brow
  -- rather than a box the model happens to sit inside. A cube gives back its
  six faces exactly.

  In this mode the *Detail* slider is the fraction of those principal
  directions to keep, from 2 up to 64, so the number it names is the number of
  planes. Each step splits one plane in two and leaves the others where they
  were, so the slider refines the break rather than rebuilding it. The fit
  runs once, the first time the mode is turned on, from a thinned but fixed
  sample of the normals: loading a model you never look at this way costs
  nothing, and the same model always breaks the same way.

  *Draw the plane boundaries* works here too. There is no grid to measure
  against, so a boundary is found where the two nearest directions are equally
  near -- a quantity that is zero exactly on a seam, and that divided by how
  fast it changes in one pixel gives a line of an even width at any zoom, as
  in the grid mode.

### Fixed

- **The planes filter no longer mirrors the planes around the silhouette.**
  Whether a surface is being seen from behind was settled after the normal had
  been rounded onto a plane, so a plane that tipped a degree past the horizon
  turned end for end -- a hard 180-degree seam ringing the model that no plane
  of the form had put there. It is now settled from the unrounded normal,
  which is where the fact actually lives. Both modes are affected; the change
  is most visible at the coarse end of the grid, where the side planes now
  take the light by where they face instead of all turning to face the camera.

## [1.3.1]

### Added

- **The screen no longer sleeps while the viewer is the window in front.**
  Working from a reference means minutes at a time with both hands busy and
  neither the keyboard nor the mouse touched, which is exactly when a machine
  decides nobody is there. The request is dropped the moment the window goes
  behind another, so a viewer left open in the background costs a laptop
  nothing, and it is dropped again when the window closes. Windows, macOS and
  the freedesktop screensaver service are each asked in their own way; a
  machine that has no answer for any of them simply sleeps as it always did.

## [1.3.0]

### Added

- **Planes.** A new tab that discretises the shading normals into the flat
  planes a form is blocked in with. Every normal is snapped to the nearest of
  a set of directions, and a *Detail* slider sets how much of a turn one of
  those planes covers: 90 degrees, exactly the six planes of a blocked-in box,
  down to 8, where only the sheen still facets. The slider is linear in that
  angle rather than in a count of planes, so it moves the form by as much at
  the coarse end as at the fine end: the box grows bevels off its corners
  before the planes themselves subdivide. Every setting keeps a plane square
  on each axis, so the front, side and top planes stay put. The quantisation
  happens on the model rather than on the screen, so the planes stay locked to
  the form while you orbit.

  *Draw the plane boundaries* puts a line along every seam between two planes,
  with the colour and width to hand. The lines come from the quantisation grid
  itself rather than from comparing neighbouring pixels, so they keep the
  width you set at any zoom, and they fade where the planes shrink to a pixel
  or two rather than flooding the silhouette.

  It filters the normals rather than the shading, so it is independent of the
  shading mode and applies to a matcap, an analytic light rig and the normals
  view alike.

### Changed

- **Flat (faceted) shading moved to the Planes tab**, next to the new filter:
  both decide which direction a fragment is shaded from rather than how it is
  lit. Sessions written by an earlier version still restore it.

## [1.2.0]

### Added

- **Update check on startup.** The viewer asks GitHub for the newest release
  when it opens and, if a later version exists, says so and offers the release
  page. The lookup runs off the UI thread, so a slow or unreachable network
  never delays the window, and the startup check stays quiet: nothing is shown
  when you are up to date, when you are offline, or for a version you told it
  to skip. **Help → Check for Updates...** asks on demand and always reports
  what it found.

## [1.1.2]

### Fixed

- **Hiding a measurement no longer closes the application.** Ticking a row's
  checkbox committed the change while Qt was still delivering the signal, so the
  list rebuilt itself and destroyed the row mid-flight; with more than one
  measurement on the list that took the process down. Visibility, renames and
  the padlock now commit once the click has been delivered.

## [1.1.0]

### Added

- **STL and glTF import.** Alongside OBJ, the viewer now opens `.stl` (binary
  and ASCII) and `.glb` / `.gltf` files, from the Open dialog or by dropping
  them on the window. STL corners are welded so a printed part arrives with
  shared vertices rather than three loose corners per facet; glTF node
  transforms are applied and triangle strips and fans are converted.
  A glTF file states that its coordinates are metres, so the measurement panel
  adopts that unit automatically. OBJ and STL declare nothing, and are left
  alone rather than guessed at.
- **Cross-section tool**, in its own panel and on `Ctrl+K`. Cut the scene with
  X, Y, Z or any custom plane — *Set Plane From View* squares the cut up with
  whatever you are looking at — then keep the material below it, above it, or a
  slice of a chosen thickness. The profile at the cut is traced as a bright
  contour, and the exposed interior is flooded with a flat colour so the cut
  reads as solid material instead of a hollow shell.
- **High Quality shading mode**: soft shadows from the key light and screen-space
  ambient occlusion, with strength, softness, bias, radius and intensity all
  adjustable. Both are approximations rather than traced rays — a full frame
  costs a few milliseconds, so the view stays live while you orbit it.
- **Pedestal.** Stand the model on a disc, either at its lowest vertex or at a
  level you choose, with adjustable diameter, thickness and colour. It is
  ordinary geometry, so it takes the cast shadow and gives the eye somewhere to
  read contact and height from.
- **Model orientation.** Formats disagree about which axis points up, and STL
  says nothing at all, so a file can arrive lying on its side. The new Model
  tab turns it upright: pick the up axis the file used, flip it if it came in
  upside down, and spin it a quarter turn to face forwards. The turn is a plain
  rotation applied once to the mesh, and measurements and annotations are
  carried through it, so marks stay where they were put. The same tab reports
  what came out of the file — name, triangle and vertex counts, size and where
  the unit came from.
- **Angle snapping while orbiting.** Hold Shift and the orbit lands on whole
  increments — 15° by default, set in the Camera panel — so a three-quarter
  view can be returned to exactly. The snapped angle is measured from where the
  drag started, so releasing Shift resumes the free orbit without a jump.

### Changed

- Every panel scrolls, so a tab taller than the dock — the Shading tab, on a
  laptop — no longer has its rows squashed or cut off. The matcap gallery sits
  above a draggable handle instead of a fixed height, so it can be given as
  much room as the artist wants and the adjustments scroll in what is left.
- **Picking is roughly a hundred times faster on large meshes.** Triangles are
  sorted along a Morton curve into leaf boxes, and a ray now intersects only
  the triangles in the leaves it enters instead of every triangle in the model.
  On a half-million-triangle scan a pick went from about 90 ms to 0.5 ms, which
  is what keeps hovering, measuring and painting responsive.
- OBJ files parse in numpy wherever they are regular, about a third faster, and
  corners that share a vertex and normal now share an output vertex. Anything
  irregular still falls through to the original line-by-line reader.
- The section contour is extracted from per-vertex distances and expands only
  the triangles that actually straddle the plane, so dragging the offset slider
  keeps up with the mouse.
- Sessions are version 4, carrying the section, pedestal, high-quality,
  navigation and orientation settings. Files written by 1.0 still load.

## [1.0.0]

First release: OBJ loading, matcap shading with full grading controls,
analytic shading modes (Lambert, Phong, Blinn-Phong, PBR, normals), cursor-led
orbit/pan/zoom, perspective and orthographic projection, named on-model
measurements with lockable draggable endpoints, surface annotations with a
splitting eraser, named camera bookmarks, undo/redo across every document
edit, and JSON sessions saved beside the model.
