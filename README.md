# Reference Viewer 3D

<p align="center">
  <img src="resources/images/readme.png" alt="Reference Viewer 3D" width="900">
</p>

A small, fast 3D reference viewer for clay sculpting. Load an OBJ, STL or
glTF, drop a matcap on it, orbit around it, and take the measurements you need
— with the numbers saved by name in the side panel and drawn on the model.

Built with PySide6 and OpenGL 3.3.

---

## Features

**Viewing**

- Loads OBJ, STL (binary or ASCII) and glTF/GLB files, centring the model on
  the origin automatically. glTF is the one common format that declares its
  unit — metres — and the measurement panel adopts it; OBJ and STL declare
  nothing, so nothing is guessed. A glTF with a skin arrives with its
  skeleton, and posable.
- Matcap shading with adjustable rotation, contrast, gamma, brightness,
  saturation, tint and vertical flip, inside the **Shading** panel when Matcap
  is selected. High-precision textures and subtle dithering reduce colour banding.
- Analytic shading modes: Lambert, Phong, Blinn-Phong, Cook-Torrance PBR and a
  normals view — each with key/fill/ambient lights and a full surface material
  (diffuse, specular colour and level, shininess, metalness, roughness,
  reflection colour).
- **HDRI lighting.** Every lit mode — Lambert, Phong, Blinn-Phong, PBR, High
  Quality and Human Skin — can be lit by an HDRI instead of the studio rig,
  or by both: **Lighting** in the Light group. The map lights the diffuse from
  its spherical harmonics and puts its own reflection in the highlights,
  blurred to the roughness of the surface; with the map as the only light,
  the shadow map is cast from its brightest direction. Pick one of the maps
  in `resources/hdris`, **Load HDRI...** an `.hdr` or `.exr` of your own, or
  drop one on the window. **Strength** is scaled so that one lights the model
  about as brightly as the studio key, whatever exposure the map was shot at;
  **Rotation** turns it; the map can be shown, blurred, behind the model.
  `Shift` + right-drag in the view turns every light at once — the key and
  the fill across and up, the HDRI with them — as one undo step.
- A **Contour** shading mode that cuts the form with a stack of evenly spaced
  planes and draws the cuts, the way a contour map reads land: the lines crowd
  where the surface turns across the planes and spread where it runs along
  them, and a flat facing them has none at all, so the curves and the flats of
  a form read at a glance. The planes follow the camera by default — depth
  slices, the sculptor's sighting across the form — or face X, Y or Z, or
  whichever way the camera happened to face when you pinned them.
- Anti-aliasing you can change without a restart — FXAA, or supersampling at
  twice the size — beside the multisampling that is fixed when the window is
  made, and an optional FPS counter in whichever corner you want it. All under
  **Settings > Preferences > Viewport**.
- Flat (faceted) shading and a wireframe overlay for reading topology.
- **AutoSmooth**, under the shading mode: the model shaded smooth across
  gentle edges and hard across ones sharper than the angle, as 3ds Max's
  AutoSmooth does — for a scan or a hard-surface model whose normals were
  lost, or averaged over its creases. The smoothing groups are worked out
  once per object, so a moved or posed object stays smoothed through the drag.
- A **Ghost** mode with a solidity slider, which draws the model see-through so
  you can read what is inside it: the far side of a form, the cut of a
  cross-section, the armature standing in it, or the clay of the forms.
  Every surface along the view
  is summed rather than sorted, so a limb crossing a torso reads the same from
  any angle instead of coming apart where the form folds over itself.
- A **Planes** filter that breaks the surface into the flat planes a
  sculptor blocks a form in with, from a six-sided box down to a barely
  faceted surface -- on a fixed grid, or fitted to the model itself by any of
  three clusterings of its own surface. It can round the shading normals onto
  those planes, in which case it works under whichever shading mode you are
  in, or cut the form itself into them -- additive like clay or subtractive
  like stone -- in which case the silhouette, the wireframe and the shadow all
  come out faceted too. Either way the model itself is left alone.
- **Record the making of a form and scrub through it**, rather than only
  arriving at the end of it. Every stage is the form exactly as the Detail
  slider set that far would build it, so what you scrub past is what you could
  stop at. The recording runs in the background and the stages become
  scrubbable as they land, coarsest first.
- **Export that making as a video** — MP4, AVI, GIF or WebP — with each stage
  held on screen for as long as you say, the frame size, shading and ghosting
  chosen for the clip rather than inherited from the window, and each helper
  ticked in or out of shot. Which stage a frame is can be burned into its
  corner. GIF needs nothing installed; the other three use ffmpeg if it is
  there and say so plainly if it is not.
- Adjustable background gradient.
- The screen stays awake while the window is in front, so a pose holds
  while your hands are in the clay.

**Navigation**

| Gesture | Action |
| --- | --- |
| Left drag | Orbit around the point under the cursor, on the camera-facing plane through the object centre |
| Right or middle drag | Pan |
| Wheel | Zoom towards whatever the cursor is over |
| Alt + left drag | Orbit even while a tool is armed |
| Alt + click | Make the object under the cursor active, whichever tool is armed |
| Shift + left drag | Orbit in whole steps of the snap angle (15° by default) |
| Shift + right drag | Turn the lights, the HDRI with them (lit modes); `Esc` puts them back |
| `F` | Frame the object |
| `P` | Toggle perspective / orthographic |
| `1` … `6` | Front, back, left, right, top, bottom |

**Camera**

- Field of view from 5° to 120°, and a true orthographic projection. The
  orthographic extent is derived from the FOV and distance, so switching
  projection keeps the object the same size on screen.
- The near and far clipping planes are fitted to the scene every frame, so
  nothing is ever cut off by accident. Tick **Set by hand** under Clipping in
  the Camera tab to take them over: pull the near plane in to go inside a
  model, or push it out to spend the depth buffer where the model is. The
  bars start where the fit left them, hold still as the camera moves, and are
  saved with the session and with each saved view.
- Save any camera pose under a name, rename it in place (`F2` or a double
  click), overwrite it, and cycle through the list with `[` and `]` or recall
  directly with `Ctrl+1` … `Ctrl+9`.

**Objects**

A scene holds any number of models. **File > Open Model** (`Ctrl+O`) still
opens one as the whole scene; **File > Add Model** (`Ctrl+Shift+O`), or the
`+` in the Model tab, adds another standing at the origin, and the picking,
the section, the pedestal, the planes and the shadows all read the scene as
one. The Model tab lists the objects as a tree, as an outliner does:

- Double-click a name to rename it. Tick a box to show or hide an object; when
  every object is hidden the viewport says so. The bar on each row is the
  object's own **solidity** — the same ghost the Shading tab applies to the
  whole scene, one object at a time — so a reference can be laid over a
  block-in and seen through.
- One object is *active*: bold in the list, the one the boxes describe and
  the transform tool moves. Click a row, `Alt`-click an object in the view
  (whichever tool is armed, as in ZBrush), or plain-click one with the
  transform tool armed. Whichever way an object becomes active, a line is
  drawn round its edge for a moment and fades, so the eye can find it.
- **Duplicate** makes a copy of the active object standing on top of it,
  ready to be moved aside — the mesh only: a rig and any children stay with
  the original.
- **Move, turn and scale** an object by hand: press `T` and the active object
  grows a gizmo — three arms along the axes and a ring at the centre. Drag an
  arm to move along, turn about, or scale along that axis; drag the ring to
  move across the view, turn about the line of sight, or scale the whole.
  `Shift` snaps a turn to round angles, `Esc` puts the object back, and each
  drag is one undo step. The Model tab's Gesture box says which of the three
  a drag does — or press `W`, `E` or `R` while the tool is armed — and the
  Position, Rotation and Scale boxes take exact numbers.
  Scaling acts on all three axes together by default; a switch lets each axis
  go its own way. A move, a turn and a scale are about the object's own
  pivot, which is the centre of its box as it was read in.
- **Reset XForm** writes the active object's rotation and scale into its
  mesh, as 3ds Max's does: afterwards it is unturned and unscaled, stands
  where it stood, and nothing in the view has moved. Its mesh is no longer
  its file's, so saving the session writes it out as an OBJ beside it, as a
  merged object is; a rig the file gave it is kept and saved beside it too.
- **Normalize Objects** scales the selected objects so that each is the
  size of the active one — the largest of its three extents is matched,
  about its own pivot, the same on every axis — so a head scanned in
  millimetres and a figure modelled in metres come out the same height and
  can be set against each other. `Ctrl`-click rows to select more than one;
  it is one undo step.
- **Link** an object to another by dragging its row onto that one — or with
  the Parent box — and it follows its parent's moves, turns and scales, as a
  child does in any modelling application. Linking keeps the child where it
  stands. What else a child follows is under **Linking**, with the usual
  answers switched on: hiding a parent hides its children, a parent's
  solidity is handed down, and removing a parent hangs its children from the
  grandparent rather than removing them too. Each of those can be turned the
  other way.
- **Merge** the selected objects into one mesh standing where they stood
  (`Ctrl`-click rows to select several), or **Split** an object into its
  loose pieces — the parts that share no vertices — each an object of its own,
  which is how a file that packs several parts into one mesh comes apart. A
  merged or split object has no file of its own until the session is saved,
  at which point it is written out as an OBJ beside the session file.
- A rigged model's skeleton moves with it, so a figure can be placed and still
  posed. Measurements, annotations, armatures and forms are marks in the
  scene rather than on any one object, and stay where they were made.

**Progress**

Everything that takes a while says so in one way: a card floated over the
foot of the view, with what is being done, what it is doing right now, a bar
that fills when the work can count and sweeps when it cannot, and a cross to
stop it. Opening or adding a model, loading a session, skinning a figure,
rebuilding a form from planes, recording a form's making, exporting a video
and checking for updates all report through it, and the work behind a card
runs off the window, so the scene stays up and answering while a scan is read
or a figure is skinned. A job over in a blink never shows a card at all.

**Grid**

A reference grid on the ground, on by default, and two more for the walls
behind and beside the model, under **Shading > Grid**. The number of lines,
their spacing (or a round number picked to suit the scene), a heavier line
every so many, the colour, the line width and how solid the lines are, are all
settable, and the world axes are drawn through the grid in their own colours.
The lines fade with distance from the camera — how far, as a multiple of the
camera's distance to the grid, is a slider too, and nought turns the fade off —
so the far squares go before they can crowd into a moiré at the horizon. The
ground grid sits under the scene's lowest point unless told to pass through
the origin, so it never cuts the model in two.

**Orientation**

Formats disagree about which axis points up — CAD and Blender exports are
usually Z-up, most sculpting tools are Y-up, and STL declares nothing — so a
file can arrive lying on its side. The Model tab turns it upright: pick the up
axis the file used, flip it if it came in upside down, and spin it a quarter
turn to face forwards. Each object has an orientation of its own, so a Z-up
scan and a Y-up sculpt can share a scene; the setting shown is the active
object's, the next model added is read the same way — files from one
pipeline share an up axis — and **Apply to All** turns every object alike.
Measurements and annotations turn with the model, and going back to the
previous setting puts everything exactly where it was.

**Armature**

A wire under the form, laid out before any clay goes on: a graph of named nodes
joined by bones. It is not a rig — nothing is animated by it, nothing is skinned
or weighted. It is there to be read off the screen while you bend real wire to
length, and to tell the clay mode where the masses of a figure belong.

- Press `R` and click to place nodes along a limb, each joined to the last.
  Drag one to move it, `Shift`+drag to change how thick the form is there.
  Nodes can be dissolved out of the middle of a chain without breaking it and
  locked once they are right. Each of those is one undo step.
- Clicking a node selects it and highlights its row, whether or not the tool is
  armed — reading which node is which should not first require arming anything.
  With the tool armed, clicking a *second* node runs a bone between them;
  `Ctrl`+click (`Cmd` on macOS) does the same at any time, in the viewport or
  in the list, which is how you close a shoulder or a pelvic bar.
- Clicking a bone drops a node into the middle of it and splits it in two, so a
  chain can be subdivided where it needs more articulation rather than only
  extended from its end. The new node takes its thickness from the two it was
  dropped between.
- Double-click a row to rename a node or the armature itself.
- Every node carries its thickness as a radius in scene units rather than as a
  dot on the screen, so the ring grows as you zoom in and reads as the body
  rather than as a handle.
- The armature lives inside the model, so it is drawn over the form rather than
  hidden by it, and the part standing behind the surface is dimmed instead of
  cut away.

Or let a **guided preset** work the figure out for you. It walks a list of
anatomical landmarks — the C7 bump, the jugular notch, the two hip points, the
epicondyles either side of a knee — and never asks for a joint centre, because
nobody can point at the middle of a femoral head. The hip is placed from the
two hip points and the two dimples alone: a fixed share of the width between
the hip points in from each, and a little below and behind it, which is the
rule gait laboratories use to find the joint from the same markers. Nothing on
the list is anatomy a pose can hide — the trochanter, which a bent hip
swallows, is not asked for. Asking for what is visible and inferring the rest
is both less to point at and more accurate than asking for the guess directly.

Every rule is a ratio of the figure's own measured spans, so one preset fits a
child and a heroic nude and nothing drifts when the pose changes. The paired
landmarks then pay twice: the two epicondyles that locate an elbow are also the
width of the elbow, so every joint arrives already sized and you are never
asked for a thickness at all.

Place the midline and one side and the other is reflected across a plane fitted
through the midline landmarks — eighteen placements instead of thirty-one. A
mirrored point is drawn hollow, so a guess reads as a guess; correct one and it
is yours, because the mirror never writes over a point you have taken hold of.

The landmarks are kept afterwards rather than consumed, so nudging one
re-derives the nodes that read it: a misplaced hip point is a correction, not a
restart. A locked node keeps its place and its size through that — one padlock,
one meaning — and moving any node by hand hands the armature over to you and
stops the re-derivation, in the same undo step, so one `Ctrl+Z` puts it back
under the preset.

Every placed landmark is listed in the panel, in the preset's own order down
the figure, with its position in `X`, `Y` and `Z` in whatever unit the Measure
panel is set to. Select a row to ring that cross in the view; type or nudge a
number and the joints reading it follow at once, one undo step per number. Or
drag the cross itself, the way you would a node: the figure re-forms under the
cursor and the whole drag is one step. A cross answers within a tighter reach
than a node handle, so where the two sit together — which is half the joints of
a preset — aiming at the cross picks the landmark and a few pixels out picks the
node.
Deleting a landmark takes any guess mirrored from it along with it. An armature
you have taken over by hand keeps the nodes you made — its landmarks stay an
editable record of where the anatomy is, and **Rebuild Nodes** is how you hand
it back to the preset, keeping your names and whatever you locked.

**Pose**

A skeleton in the sense a rigging application means it, and the one thing the
armature is not: every joint but the root hangs from a parent, turning a joint
carries everything below it, and a model that came with skin weights follows
the bones.

- A rigged GLB or glTF brings its skeleton in with it — the joints, their bind
  matrices, the weights tying each vertex to up to four of them — and is
  posable the moment it opens. Files with no skin load as they always did.
- Posing is by pulling, as a bone is turned in 3ds Max once it is picked:
  drag a joint and the bone above it swings to follow, carrying the limb;
  drag a root and the whole figure moves; `Shift`+drag rolls a joint about
  its own bone; `Ctrl`+drag pulls it in depth. Dragging a bone is dragging
  the joint at its far end. Each pull is one undo step, and `Esc` drops a
  half-made one.
- The **Pose** panel lists the joints as the tree they are, turns the
  selected one by three sliders for a number read off a reference, re-hangs
  it from another joint, resets a joint, a branch or the whole pose, and has
  a switch for whether the model follows the skeleton at all — off, the bones
  pose in the air and the model stands at rest, which is how a pose is
  compared against the reference it was read from.
- Press `B` and click to build a skeleton of your own, each joint hung from
  the selected one; or stand up the **Humanoid** preset, proportioned to the
  model's height, and pull it into the model in **Fit** mode, where dragging a
  joint moves where it rests and its children stay put.
- Armatures and skeletons convert into one another. A skeleton is *grown*
  out of an armature from a root — the node selected in the Armature tab,
  else the pelvis, else the best-connected node — and any bone that would
  close a loop is left out and counted. The other way, any skeleton lays an
  armature under itself as it is posed, roles and all, so the clay modes can
  read a figure off a rig that came with the model.
- Rigs are read as figures by their names: joints named the way Mixamo,
  Biped, Unreal, Rigify or Character Creator name them are recognised, and a
  model whose rig reads as a humanoid is offered the mapping when it opens.
  A guess, correctable joint by joint in the Role box.
- **Simplify** takes the detail out of a rig — the fingers, the toes past the
  ball, the face, the breasts, the twist and share and end helpers — and
  re-hangs what is left, weights folding onto the joints that stayed. A
  hundred-joint game rig comes down to the two dozen a pose is read from.
- **Auto-skin.** A skeleton the model did not come with — the preset
  fitted, a chain clicked in, one grown out of an armature — is given skin
  weights by **Skin to Model**, under **Auto-skin** in the Pose tab (folded
  away by default), and from then on posing the bones poses the model. Not
  the weights a rigger would paint, but made in a second or two and good
  enough to turn a figure to read a pose off. The skeleton is bound where it
  stands: its pose becomes its rest. Heat diffusion is the default — each
  bone's warmth spreads over the *surface* of the model, so a hand resting
  on a hip stays the hand's and a blend is as wide as the limb is thick —
  with envelope (by distance) and nearest-bone (rigid) beside it, a cap on
  how many bones share a vertex, a heat knob for how tightly the weights
  hug the nearest bone, and a preference for bones that lie behind the skin
  over ones out in front of it, which is what tells the torso from the arm
  beside it. **Unskin** takes the weights off; either is one undo step.
- The session keeps the skeletons and the pose; a file's skin weights stay in
  the model file and are matched back to the joints by the names the file gave
  them, so renaming a joint costs nothing and deleting one hands its weights
  to the nearest ancestor left. A skin made here is written to a small
  archive beside the session, named for the session and the object, and put
  back when the session loads.

**Forms**

The simple masses a figure is blocked in with, built in clay over the model.
Three come as presets: the pelvis as a bucket with its front corner chipped
off, the ribcage as an egg with the thoracic arch chipped out of its front,
and the head as a wedge that is then given its width, the block of its
cranium and its jaw. None of those masses can be measured off a model
directly, but every one is pinned down by anatomy you can find on its
surface, so each is a guided walk like the armature's. The rest of the figure
-- and the presets are only special cases of this -- is a **freeform**: put
down whatever landmarks you choose, name them as you go, and the form is the
hull of them.

- Pick `Freeform` in the Forms tab, give it a name if you like, and press
  `Start`. Type a name for the next landmark, say whether it is on the
  midline or the left or the right, and click; the side carries over from
  one landmark to the next until you change it, and the names are numbered
  for you if you do not type any. A hand, a knee, a breast, a nose, a
  clavicle, a scapula, a muscle, the fat over a hip: any of them is a few
  points and a hull. The clay appears once four points span a volume and
  re-forms as each further point goes down.
- The fill is yours: **Faceted** is the convex hull of the points as it
  comes, planes meeting at edges, which is right for bone; **Smooth** bows
  each face of that hull out into a cubic patch between the points, for
  muscle and fat. Either way the clay passes through every landmark, and the
  fill can be changed after the fact.
- Landmarks can go inside the model as well as on it: **Ctrl/Cmd-drag** a
  marker up to move deeper, or down to move toward the camera. A fading depth
  ruler shows the signed movement, and a grid facing the camera is laid
  through the point in the scene itself, where the model stands in front of
  it or behind it and says which; Escape restores the starting position.
  The gesture works for measurements, armature nodes, and all landmarks.
  A click off the model places a point on the view plane through its centre.
- Markers have a small shadow for contrast. Markers behind the model surface
  are faded and surrounded by a dashed ring.
- A left or right landmark is mirrored to the other side once enough of the
  midline is down to fit a plane through, exactly as a preset's are; place
  both sides by hand and they are a pair, which the symmetric build
  averages. A freeform with no pair at all is left as placed, so a hand
  marked "centre" throughout stays a hand rather than being pressed flat
  onto a plane. Landmarks can be renamed in the list, and `Back` takes the
  last one off again. A finished freeform is never closed for good: select
  it in the list and press `Append` to take it up again and add landmarks.

- Pick a form in the Forms tab, press `Start`, and click the landmarks it asks
  for — the crests of the hips and the two points at the front of them, the
  notch at the top of the breastbone and the bottom of it, the widest point of
  the skull. Nothing on the lists is anatomy a pose or a body can hide: the
  sitting bones are asked for but not waited for, and the trochanters are not
  asked for at all. The form is worked out from the points and grows as they
  go down: the bucket closes over the pelvis as its last point is placed.
  Place the midline and one side and the other side is mirrored, as it is for
  the armature.
- The thoracic arch is chipped out along the costal margins point by point —
  the corners of the rectus abdominis beside the xiphoid, where its outer edge
  crosses the ninth rib, the corner at the tenth — so the arch curves in under
  the ribcage as a real one does, rather than being one flat cut a side. The
  margin is the bottom ring of the egg itself, so the surface passes through
  every one of those points before it is chipped along them; and the front
  corners of the ribcage, where the cartilages turn back from the breastbone,
  can be placed to flatten the front of the egg to the real ribs.
- Every form is planes meeting at edges, the head included: the cranium is a
  block planed out to the bulges of the forehead, the corners of the crown and
  the mastoids, not a ball. Planes are what a block-in is for.
- The forms are bone, and bone is symmetric, so by default each is built from
  its landmarks made exactly symmetric about the median plane — the midline
  dropped onto it, each pair averaged across it. The landmarks stay where you
  put them; only the clay is straightened. Switch it off in the panel to build
  from the points exactly as placed.
- The head arrives in stages — the wedge, its width, the cranium, the jaw and
  muzzle, and last the nose, the first of the secondary forms — and the
  landmarks are asked for a stage at a time. Every stage is
  kept and a slider scrubs back through them, so what you can look at is not
  only the finished block-in but the order it was built in.
- Clay goes on and does not come off. Each stage is laid over the ones before
  it rather than cut out of them, which is why the head starts as a wedge that
  is widened rather than a ball that is sliced — and why it is widened above
  the eyes and below them, and not between: the eye sockets are the gap left
  between the cranium and the jaw, and nothing is ever laid into them.
- The landmarks stay editable afterwards, listed in the panel with their
  positions. Drag a cross in the view or type a number and the clay re-forms
  under it. Every placement and every move is one undo step.
- The forms are drawn with the model rather than in place of it, in their own
  clay colour, and take shadows and occlusion like anything else. Ghost the
  model — the switch is in the Forms tab as well as the Shading tab — to read
  the clay standing inside it.
- A form is its landmarks: a session file carries a dozen points per form, and
  the solids are worked out again from them whenever they are drawn.

**Cross-section**

- Cut the scene with a plane: X, Y, Z, or any direction — *Set Plane From View*
  squares the cut up with whatever you are looking at. `Ctrl+K` toggles it.
- Keep the material below the plane, above it, or a slice of a thickness you
  set, which is the view that shows how a form is built at that level.
- The profile at the cut is traced as a bright contour, and the exposed
  interior is flooded flat so the cut reads as solid material rather than as a
  hollow shell.

**Planes**

Drawing and sculpting both start by reducing a form to flat planes: the front
of the forehead, the side of the nose, the top of the cheekbone. The Planes
tab does that to the model.

*Simplify* chooses what the planes are used for, and the two settings are
mutually exclusive because the second contains the first.

**Simplify Normals** leaves the geometry alone. Every shading normal is
snapped to the nearest of a small set of directions, so the surface reads as a
handful of flats with hard edges between them, and the light on each flat is
even -- which is exactly what makes the turn of a form easy to see and to
copy. The silhouette stays as round as the model is.

*Planes from* chooses where that set of directions comes from.

**Grid** uses the same directions for every model: a cube, bevelled as far as
you ask. It is how a sculptor blocks a form in before they have looked at it,
and it is the mode to reach for when you want the planes measured against the
world rather than against the model.

The *Detail* slider sets how much of a turn one plane covers: 90 degrees at
the coarse end, which is exactly the six planes of a blocked-in box, down to
8 degrees, by which point only the sheen still facets. The slider is linear in
that angle, so a step at the coarse end changes the form by as much as a step
at the fine end -- move it slowly and the box grows bevels off its corners
first, and only then do the planes themselves subdivide. Every setting keeps a
plane square on each axis, so the front, side and top planes stay where an
artist expects them.

**PCA** reads the directions off the model instead. Every vertex normal is a
point on the sphere, weighted by how much surface it stands for, and that
cloud is split along its principal axes: the direction of greatest spread in a
group of normals is its first principal component, and the group is cut in
half across it. The group with the most spread left in it is always cut next,
so the first directions to appear are the big planes of the form and the later
ones refine them. The planes are the model's own -- the flat of a cheek, the
underside of a brow -- rather than a box the model happens to sit inside.

Here the *Detail* slider is a count of planes rather than an angle, climbing
from 2 to 256. It climbs by proportion rather than by a fixed step: going from
four planes to five redraws a form and going from two hundred to two hundred
and one is invisible, so each step of the slider is worth a roughly constant
*share* more planes. That leaves real control at the coarse end, where the
blocking-in happens, while the fine end still reaches into the hundreds.
Adding a plane splits a single one in two and leaves the rest alone, which
means the slider refines the break rather than rebuilding it each step. The fit runs
once, the first time the mode is turned on, off a thinned but fixed sample of
the normals -- so it costs nothing to load a model you never look at this way,
and a model always breaks the same way twice. A cube gives back its six faces
exactly.

**Regions** reads where the surface is as well as which way it faces, which
is what lets it tell two parts of a form apart when they happen to face the
same way -- the plane of a cheek and the plane of a temple stay two planes
with a seam between them, where PCA has only one direction to offer for both.
Each vertex becomes a row of a design matrix holding its normal, its position,
and how far out its own tangent plane lies; the surface is cut into a few
hundred small patches and then merged back together, at every step joining the
two patches that cost the least, which is Ward's criterion. Because the merge
is a hierarchy, the *Detail* slider is a cut of one tree: adding a plane
splits one and leaves the rest, exactly as in PCA mode. This is the one to
try first.

**Flats** asks a blunter question of the whole model at once: which single
plane does the most surface agree on? It takes that one, removes its surface,
and asks again -- so the largest flat of the form arrives first and the rest
in the order a sculptor would block them in. Nothing is averaged, so a stray
patch or a noisy scan cannot pull a plane off the flat it belongs to. The
price is that it does not nest: each step of the slider re-asks the question
rather than subdividing the last answer, so the planes shift about as you
drag. Reach for it when a form has real flats in it and you want those rather
than an even share-out of the surface.

Both of these weigh a vertex by the area it stands for *and* by how flat its
neighbourhood is, so the flats of the form decide where a plane sits and the
rounded turns between them follow along.

*Design matrix* — folded away under the boundary controls, because the
defaults are chosen to read a figure and most work never needs to open it —
is where those weights can be argued with. *Position* is what a whole radius
of travel across the form counts for against a right angle of turn in the
surface: at zero the fit reads facings only, like PCA, and two parts of the
form that face the same way come back as one plane; raise it and the form is
broken up as well as broken down, until at the top the planes are patches of
surface that happen to face somewhere. *Coplanarity* is what the gap between
two parallel planes counts for, which is what keeps two patches lying in one
plane together however far apart they sit. *Flat within* is how far a
vertex's neighbours may turn away from it before it stops counting as part of
a flat: narrow it and only the flattest surface decides where the planes go,
widen it and the turns get their say back. Each of these refits the model, so
they take effect when you let go of the slider rather than as you drag, and
*Reset to defaults* puts all three back. Each plane's direction is settled by
an M-estimate rather than an average -- the members that disagree most with
the first guess are down-weighted and the guess is taken again -- so a handful
of bad normals inside a patch cannot tilt it. Like PCA, they fit once, the
first time you pick the mode, and a model always breaks the same way twice.

**Simplify Geometry** rebuilds the form out of those planes instead of
rounding the light off them, so it really is faceted: straight runs of
silhouette, hard edges where the planes meet, a wireframe that follows the
flats, and a shadow to match. The planes come from the same fit the shading
setting uses and the *Design matrix* below weighs it for both, but only their
*facings* are taken -- where each flat actually goes is decided by the
material it stands for, not by the fit.

None of this is done by moving the model's vertices, because that cannot be
made to work: a patch of surface wraps and a plane does not, so flattening a
shoulder onto the shoulder's plane folds the far side of it back through the
near side. Instead the model is read into a lattice as a solid, worked as a
volume, and its surface found again from scratch. A plane arrives as a cut,
which is what a plane is to a sculptor.

*Method* is the choice between the two ways of making a form, and they do not
give the same one.

**Subtractive** is stone. The form starts as the block it would be carved out
of -- the convex hull of the whole model -- and every step of *Detail* is
another cut. The cut is taken through whichever part of the block is holding
the most air, and each half is then hulled again, so the hollows open up
deepest first: the gap between an arm and the ribs, then the knees, then the
face. The result always holds the whole model inside it, so it is a rough-out
with all the reach still present, waiting for the next cut to bring it down.

Detail buys two things at once here, and they are not equally worth having: a
cut opens one hollow, while another direction to cut along shaves every block
of the form at the same time. Doubling the directions brings the stone in
about twice as far as tripling the cuts does, so most of the slider goes
there. At the far end a figure comes back within a twelfth of its own volume
-- a carving rather than a rough-out, and still every bit of it a flat.

**Additive** is clay, and it is built rather than cut. The largest rectangular
block that will fit inside the model without poking out of it anywhere is
pressed into the form; then another into whatever is still bare, and another.
On a figure those land in the ribcage, the pelvis and the thighs, in that
order, because the order is simply where the most uncovered material is.
*Masses* is how many of them there are, and it is a control rather than a
measurement: how many masses a form has is a reading, and a torso is one mass
or two depending on who is looking. The range runs from a single lump in the
largest form up to every mass a standing figure has -- head, neck, ribcage,
pelvis, and upper arm, forearm, hand, thigh, shin and foot twice over -- and
the blocks stay clean the whole way, because a mass is a plain box set square
to the form it sits in and boxes stacked along a limb agree with each other.
Detail is laid on top of the masses rather than sharing a budget with them, so
reading a figure as more masses never costs it any modelling.

After the masses come the tubes. Every step of *Detail* lays another lump into
whichever part of the model the clay has not covered yet, largest first, so
the arms arrive before the hands and the hands before the fingers. A tube is
grown exactly as a mass is, but it is allowed the form's own planes as well as
the three axes of the mass it sits in, so it comes out bevelled where the
model turns. Nothing is ever told what a limb is.

Where two lumps cross they leave a notch, and a form full of notches reads as
a heap of stones rather than as one body. So the seams are filled, and in two
stages, because they come in two sizes.

The large ones are filled with more clay. Every pair of lumps that lie near
enough to be joined gets a further piece pushed across the seam between them,
shaped as the hull of what of each lump lies within a collar of the other --
which is the shape of a thumb-full of clay worked into a join. That hull is
then pulled back until it fits inside the model, exactly the way a lump is
grown out to it, so a join is made of flats like everything else and cannot
reach through the surface. A join that has to be pulled in further than the
lumps are thick is dropped: the two lie on opposite sides of a gap in the form
rather than across a seam, and a piece spanning them would be bridging air.
The collar is what keeps this honest. The hull of two *whole* lumps, on a form
anywhere near convex, is most of the form -- allow it and the mode quietly
stops being clay pressed into a shape and becomes a cast taken from one.

The small ones are closed in the volume, by a median filter run over the field
before the surface is read back out of it. A median is the right filter for
this and a blur is not: over a neighbourhood laid symmetrically about a point,
the median of a field that is planar there is that point's own value exactly,
so a flat passes through untouched however many passes are run. What it does
change is everything a flat is not -- a slot one cell wide is outvoted by the
material either side of it, a spike is outvoted by the air around it, and a
pinhole closes. Those are precisely the things a lattice cannot make a clean
surface out of, and one pass removes all of them: an additive form comes back
with no open edges at all, and a quarter as many places where the surface
passes through itself.

Both ends of that filter are yours, under *Finishing*. *Median* is how many
passes are run and *Median size* is how far each one reaches, in cells -- one
being the three-by-three-by-three block of corners around each corner. The
size is not a strength knob so much as which slots are within reach at all: a
pass reaching one cell has a cell of material either side of a one-cell slot
and closes it, and sees as much slot as material in a two-cell one and leaves
it exactly where it was. What keeps both ranges short is that a median cuts
both ways. A slot closes because it has material either side of it; by the
same arithmetic a corner is shaved because it has air on more sides than
material. One pass at one cell takes the slots out and leaves the form its
size; four passes at three cells take three fifths of the form away with
them.

*Relax* is the pass a sculptor makes last, going over the block-in with the
flat of a tool: the planes still read, but the form is no longer quarried out
of them. It works on the finished mesh rather than on the volume, because by
that point the volume has said everything it has to say. Each pass draws every
point towards the middle of its neighbours and then pushes it back out by a
shade more, which takes the corners off without letting the form shrink away,
and anything that ends up outside the model is put back onto it -- so relaxing
can never undo the containment the rest of the mode is careful about. At zero
you get the block-in exactly as it was cut. It does nothing in subtractive,
which is meant to keep its corners.

Past a point the slider stops adding lumps and starts bevelling the ones there
are, which is deliberate. A form built of sixty lumps reads as masses with
clean flats between them; the same form built of two hundred reads as rubble,
because every pair of lumps that cross at an angle leaves a ridge and enough
ridges are all you can see. Joining the lumps is what closes the gaps -- more
lumps is not, since a smaller lump in a gap leaves two narrower gaps.

**AutoSmooth** shades the result, in either mode, and does the same job as the
control of that name in 3ds Max. A facet that comes out of a lattice is only
roughly one plane: its triangles each lean by a fraction of a degree, and
shading every one of them on its own turns a clean flat into a mosaic. The
slider is the angle at which a turn stops being noise and starts being an
edge -- neighbouring triangles that agree to within it are gathered into a
group and share their normals, and anything sharper is left as the hard edge
it is. Thirty degrees is the usual reading and the default: every real plane
change on a blocked-in form is a far sharper turn than that. Nothing moves;
it is a change of shading and not of shape, and because it re-reads the
normals of a form that has already been built it costs a tenth of a second
rather than a rebuild. At zero every triangle is shaded on its own again.

**Detail and Masses have soft ends.** Both sliders stop where their useful
range stops, and both will take a number typed into the box past that: the
slider then grows to reach it, and can be dragged over the wider range from
then on.

For *Masses* that is room for a form that is not a figure. Sixty-four is past
every mass anyone reads a standing figure as, and going much beyond it the
block-in stops reading as masses and starts reading as rubble -- measured on a
figure, the surface holds a third fewer of its area in its commonest facings
at two hundred and fifty-six masses than at thirty-two, which is what rubble
looks like as a number. It is offered because it is yours to say.

For *Detail* it buys something different from what the slider itself buys. At
the slider's own end the form already has every plane a fit will give it and
every block or lump those planes buy, and going past that changes nothing:
doubling the planes to five hundred moved a carving by a hundredth of its
volume and left the clay exactly where it was. What is holding it there is the
lattice the form is worked on, so that is what a typed value lifts -- the same
reading of the form, resolved finer. It shows as crisper flats and straighter
creases rather than as more of them, and it costs, because a lattice is
three-dimensional: at the top of the range a figure comes back with three
times the triangles and takes about eight seconds to rebuild instead of three.
Two hundred is where the lattice meets its own memory ceiling and stops
getting finer, which is why that is the end of it.

Read either against the model's own silhouette and it says how much of the
form is mass and how much is detail.

What comes back either way is a union of convex solids, each one the meeting
of a handful of half-spaces, and the surface is read off the lattice by dual
contouring: one vertex per cell, placed where the planes crossing that cell
agree. Those planes are exact, so a cell inside a flat lands dead on it, a
cell along a crease lands on the line where two flats cross, and a cell at a
corner lands where three do. The flats come out flat to the last digit, the
creases straight, and the surface closed and free of folds, because an
isosurface always is. That is also why the clay is joined as a volume and
never as surfaces: a tube laid across a mass leaves no seam where they meet
and no sliver where they cross, because there is nothing there to stitch. The
model itself is then held against the result as a floor under the stone and a
ceiling over the clay, so that one is larger than the model and the other
smaller by construction rather than by luck.

*Detail* is a count of planes, coarse to fine, and with it a count of solids.
Rebuilding geometry is real work, so it takes effect on letting go of the
slider rather than at every value a drag passes over, though the line under
the slider follows the handle so the drag is not blind. The fit is kept apart
from the rebuild and only run again when the model or the design matrix
changes, which makes flipping between additive and subtractive, or working the
masses, free.

**The model is never modified.** What the viewer draws is a stand-in, and
picking, measuring, painting and the section cut all still read the real
surface underneath. Unlike the shading filter, the stand-in is a mesh of its
own -- its own vertices and its own triangles, a good deal fewer of both,
found from the volume rather than moved from the model's. Marks already made
on the model stay where they were made, so they will sit off the flats by
however far the flats moved.

*Draw the plane boundaries* lines every seam between two planes, in a colour
and width you set, the way a construction drawing marks where the form turns.
The lines are worked out from the quantisation itself rather than found by
comparing pixels -- from the grid in Grid mode, and in the fitted modes from
where the two nearest planes are equally near -- so they hold the width you
asked for at any zoom. Where two planes meet without the form turning at all,
which is what happens when a fit that reads position divides a broad flat, no
line is drawn: the shading runs straight through, so a line there would say
the form turns where it does not. They
fade out where the planes themselves shrink to a pixel or two -- around the
silhouette, or at the fine end of the slider -- instead of flooding the
surface. They belong to *Simplify Normals*: once the geometry has been cut,
the seams are real edges of the model, and the wireframe or faceted shading
already shows them.

The planes are worked out on the model rather than on the screen, so they stay
put on the form as you orbit around it. And because rounding the normals
changes them and not the shading, that setting applies to a matcap, to any of
the analytic modes and to the normals view alike. Flat (faceted) shading,
which quantises per triangle instead of per direction, sits on the same tab,
and is worth turning on under *Simplify Geometry* to see the flats with no
softening across their edges at all.

**High Quality**

A shading mode that adds soft shadows from the key light and screen-space
ambient occlusion to the usual clay shading, with strength, softness, bias,
radius and intensity all adjustable. Neither traces a ray: a shadow map, a
depth and normal pre-pass and one occlusion pass cost a few milliseconds
between them, so the view stays live while you orbit it. Turn off *Light
follows camera* for a shadow that stays put as the model turns.

**Human Skin**

Available under **Shading → Mode**. It uses neutral dielectric
reflections with broad skin and narrow oily highlights, plus subsurface scattering.
Choose a tone preset, then adjust skin colour, roughness, reflection strength,
oiliness, scattering colour/depth, transmission, and exposure. Presets describe
tones and undertones; they are editable starting points, not ethnic classifications.

The surface is not smooth: pores and the furrow network between them are bumped
into any mesh from a tileable 3D volume, so nothing needs a UV layout. **Surface
detail** sets how deep they read and **Pore size** how far apart they sit, as a
fraction of model radius (a head wants a smaller value than a full figure). The
highlights see the full relief, the diffuse light a third of it, and the
scattering none, which is what keeps it from looking like wax. **Tone variation**
mottles the pigment, **Blood / flush** reddens patches, cavities and backlit
edges, and **Peach fuzz** adds the soft rim that vellus hair gives.

Skin is marked, and the marks are what separate it from *perfect* skin.
**Freckles** are small light-brown dots, thick on the ground; **Moles** are
dark, a few pores across, few and faintly raised; **Acne** is red papules,
raised and shining, some come to a pale head; **Blemishes** are patches,
coarser than the pores, of irritated redness and of dry, duller skin. The
spots are round discs on jittered lattices worked out from the world
position, projected onto the skin whichever way it faces, so like the pores
they need no UV layout and never repeat; their size follows the pore size.
All four start at nought.

Where they fall is the **Body Regions** group's business. Acne gathers on
the face, the chest and the back; freckles and moles on the arms and the
shoulders; the knuckles and the feet run redder than the forearm; the
forehead shines where the calf does not. The regions come from a skeleton
with humanoid roles when the scene has one — the preset, a rig read by its
names, one grown out of the guided armature — which places every limb, and
otherwise from the height bands of a standing figure, which tell the head,
the neck, the torso and the legs apart; a bust or a hand is best told what
it is with *The whole model is one region*. Each region has a multiplier
for each kind of mark and for the oiliness and the flush, starting from
where marks tend to fall, and each can be turned up, down or off. The map
behind it is a small volume of region weights laid over the scene, built
off the thread whenever the scene or the bones move and read by the shader
at the same world position as the pores.

Orbiting, panning and zooming use a fast preview. With **Refine while idle** on,
the view starts accumulating after 200 ms at rest: triangle-ray soft shadows from
both lights, one diffuse indirect bounce, sampled subsurface diffusion and
thickness-dependent backlighting. The sample counter stops at the requested limit.
Changes to the camera, lights, material, clipping, geometry, or viewport size start
a fresh image. Light angular radius controls traced shadow softness. Refinement
resolution trades detail for speed; use **1.0 × viewport** for a final reference.

Refinement is close to real time: a frame runs as many samples as fit in a
couple of dozen milliseconds, each sample is a few milliseconds on a current
GPU, and the samples are stratified, so sixty-four of them — the default —
look as clean as a hundred and twenty-eight used to, and a figure clears in
about half a second. Lit by an HDRI, the traced skin samples the map where
its light is, and shadows, diffuses and backlights with the whole room.

Scattering depth is a fraction of the model's bounding radius because OBJ has no
physical units. A head and a full figure need different values. Closed meshes give
the most dependable transmission; holes and intersecting shells can produce light
leaks. This is an RGB diffusion approximation, not a spectral tissue simulation.
Ghost mode and exported form-stage videos use the fast preview. Screenshots of the
viewport retain its current refinement. See [the skin renderer notes](docs/skin-renderer.md)
for the model, limits and extension points.

**Render**

The **Render** panel path-traces the view on the processor, with every
core — a real render, not the viewport's approximation of one. Press `F12`
(**Render → Render Image**) and the **Render window** fills in, bucket by
bucket or pass by pass; `Esc` stops it, `Ctrl+S` saves it as PNG (8 or
16 bits) or OpenEXR, and **Save all passes** writes the beauty, denoised,
albedo, normal and depth passes into one multilayer EXR. The view transform
and exposure can be changed on the finished picture without rendering again.
`Shift+F12` turns on the **rendered viewport**: the view itself, path-traced
and denoised while you work in it, coarse as it turns and sharp once it stops.

What you set up in the Shading panel is what renders. PBR, Lambert, Phong,
Blinn-Phong and High Quality become the materials they describe, lit by the
studio key and fill (as soft as **Light softness** says) and the HDRI; Matcap,
Normals and Contour are ways of looking rather than materials, so they render
as a clay whose colour and shine the panel sets. Human Skin renders as the
whole skin shader — pores, marks, vessels, the oily highlight, subsurface
scattering and backlighting — with the viewport's exposure and tone curve,
so a render matches the refined view.

- **Presets** — Preview, Draft, Final, Production — set the samples, noise
  threshold, bounces and denoising together. **Noise threshold** stops each
  part of the picture once it is clean enough, so flat background costs
  little and hair-fine detail gets the samples.
- **Output** sizes run from 720p to A4 at 300 dpi, or the viewport's own
  size. The **safe frame** shades the view outside the frame and draws the
  action-safe and title-safe guides; `F12` renders exactly what is inside it.
- **Denoising** uses Intel Open Image Denoise — on an NVIDIA GPU where there
  is one — or the NVIDIA OptiX denoiser from the graphics driver, with a
  built-in filter when neither can run. **Auto** picks the best available
  and the panel says which. A few dozen samples, denoised, make a clean
  picture.
- **Neural Rendering** runs NVIDIA DLSS 5's AI model over the denoised
  picture, relighting skin and materials towards a photograph. **Enhance the
  render** shows the result as the Render window's **Neural** pass;
  **Enhance the rendered viewport** does the same to the view as it refines.
  It needs a GeForce RTX 50 series GPU and the **Neuroframe Engine** from
  Merserk's [Visual Enhancer](https://github.com/Merserk/dlss5-visual-enhancer): 
  set **Preferences → Folders → Neural engine** to a Visual Enhancer folder.
- **Method**: *progressive* refines the whole picture a pass at a time and can
  be stopped whenever it looks done; *bucket* finishes it a tile at a time,
  in a spiral, Hilbert, row or random order. Both give the same image.
- **Light paths**, **camera lens** (depth of field), **film** (pixel filter)
  and **colour** (view transform, exposure, contrast, gamma) are there when
  wanted, folded away when not.

The render kernels are compiled to machine code the first time they are
needed — a few tens of seconds, once per version — and kept. See
[the path tracer notes](docs/path-tracer.md).

**Pedestal**

Stand the model on a disc, either at its lowest vertex or at a level you
choose, with adjustable diameter, thickness and colour. It is ordinary
geometry, so it catches the cast shadow — which is what makes contact and
height readable.

While a section is on, a rail stands at the right edge of the viewport in the
contour's colour, spanning the same range as the panel's offset slider. Drag
its handle — or the rail itself — to slide the plane along its normal; Escape
cancels and Undo restores the cut. It is the same cue as the depth ruler,
and like it stays put while the view turns.

**Measuring**

- Press `M`, then click two points on the surface. Dragging still orbits, so
  the left button serves both gestures.
- Optional snapping to the nearest vertex, or free placement anywhere in space
  for spans that do not start on the model.
- Every measurement is listed by name in the panel, is renameable, can be
  hidden individually, and stays drawn in the scene as a thick labelled line.
- Measurements start locked. Click the padlock on a row to unlock one, and its
  endpoints turn into square handles you can drag in the view — on the surface,
  or along the view depth axis with **Ctrl/Cmd-drag**. Selecting a measurement
  in the list highlights its line and endpoints in the viewport.
- Set a unit label and a scale factor once per model — an OBJ carries no units,
  so the viewer does not guess.

**Annotating**

- Press `A`, then draw straight onto the surface: freehand, straight lines or
  circles, in any colour and width. Useful for blocking in muscle masses, bony
  landmarks and plane breaks.
- Strokes are real geometry lifted a hair off the mesh, so the model hides the
  ones painted on its far side instead of letting them bleed through.
- The eraser (`E`) rubs out the parts of a stroke under the brush and splits
  what is left, rather than deleting whole strokes.
- A stroke that runs off the silhouette breaks there instead of bridging the
  gap, so paint never floats in front of the background.

**The interface**

Every panel is its own dock and goes wherever you put it — any edge of the
window, stacked with others into a tab strip, or floated off on its own. A
panel dragged to the top or the bottom has width rather than height, so its
groups break into columns to use it; nothing about the panel changes, only how
much room it was given. Every group folds away behind its own bar, and a group
whose settings have gone dead folds itself.

Any control can be **copied out of the panel it lives in**: hold `Alt`, drag
it, and drop it into a panel of your own (`Ctrl+Shift+N` opens an empty one).
Alt-dragging a group's bar takes the whole group. A copy is a second pair of
hands on the same control, not a second setting — move either and both move,
because there is only one of them. That is for the handful of controls a
particular piece of work keeps reaching for, which are almost never the
handful that happen to share a subject. Drop a copy on the model to be rid of
it.

Where the panels are, and any you have built, are remembered between runs and
written into the session file alongside the marks on the model.

**Hotkeys**

Every key is yours to move. **Ctrl+Alt-click** (Cmd+Option on a Mac) any
button or switch in a panel — the switch on a dock's bar that takes the
armature off the model, a "Clear All", a form's "Start" — and press the key
you want on it; from then on the key does what the click did, wherever you
are in the window, and the control's tooltip says so. The menus' entries and
the single letters the view answers to (`F`, `M`, `1`…`6` and the rest) are
listed under **Settings › Hotkeys**, each with a box to press a new key into.
One key does one thing: assign a key that is already in use and you are told
what it does now and asked before it is moved. What you change is kept on the
machine, apart from the session, like the rest of the preferences.

**The matcap is its own control**

A matcap is a picture of a sphere, and the sphere is the whole of what it says
— so the sphere under the gallery is drawn with the grading applied and is
dragged rather than described. Drag it and it turns under your hand; `Shift` and
drag sets brightness across and contrast up and down; `Ctrl` and drag sets
saturation and gamma; double-click puts the grading back. What is drawn is
exactly what the shader will do, because for a sphere facing the camera the
renderer's reflection lookup collapses to the matcap image itself, turned. The
five numbers are still underneath, folded away, for typing an exact rotation
into or copying out into a panel of your own. Right-click the sphere to save
the matcap as an image, graded as you have it or as it came, so a grading
arrived at by hand can be kept and used anywhere else.

A matcap loaded from outside the matcap folder — with **Load Matcap...**,
dropped on the window, opened from the File menu or brought in by a session —
joins the gallery, after the built-in, and stays there from then on.
Right-click one of those to take it out of the gallery again; the file is
left where it is.

**Preferences**

`Ctrl+,`, or the Settings menu for one group of them. What belongs to the piece
of work — the matcap, the section, the planes — travels in the session file;
what belongs to you stays on the machine and follows you from model to model:
the accent colour and type size, how fast the orbit turns and which way round,
the splash screen, the release check, whether the machine is kept awake,
whether to carry on from whatever was last open, the anti-aliasing and the
frame counter, and a folder of your own to read matcaps from. Every change
applies as you make it — multisampling alone waits for a restart, and says so —
and the window is built out of the same folding groups and sliders the panels
are, so a control in it can be Alt-dragged into a panel like any other.

**Undo**

`Ctrl+Z` / `Ctrl+Shift+Z` cover measurements, annotations and saved views. Each
edit is a command that knows how to reverse itself, and an interactive gesture
— a dragged endpoint, a swipe of the eraser — records as a single step.

Camera motion is deliberately not recorded: orbiting is a gesture rather than
an edit, and burying real changes under a hundred camera steps is what makes
undo useless in a 3D viewer.

**Sessions**

Camera, shading, matcap choice, the objects with their places and parents,
measurements, annotations and saved views are written to a JSON file. Saving with `Ctrl+S` writes `<model>.refview.json` next
to the model, and that sidecar is picked up automatically the next time the
model is opened. Files written by an older build still load. Model, session and
image files can also be dropped onto the window, opened with the viewer from
the desktop's **Open with…** menu, or dragged onto the application itself.

---

## Install

```bash
conda env create -f environment.yml
```

```bash
conda activate refview
```

Then run it:

```bash
python run.py
```

Or install the package and use the console script:

```bash
pip install -e .
```

```bash
refview resources/models/Pose_02.obj --matcap resources/matcaps/clay_terracotta.png
```

`refview --help` lists the startup options. Any number of files may be named:
each opens as what it is — a model, a session (`.json`) or a matcap image — so
the same command serves the desktop's **Open with…** and a file dragged onto
the executable. `--matcap` and `--session` name the two explicitly.

### Desktop releases

Push a tag such as `v1.1.0` to build self-contained archives for Windows,
Intel macOS and Apple Silicon macOS. The GitHub Actions release workflow
publishes the three archives to a GitHub release automatically.

### Requirements

- Python 3.10+, a GPU with OpenGL 3.3 core profile.
- PySide6 is pinned below 6.8: newer Qt builds need a more recent MSVC runtime
  than many Windows machines have installed, and fail with
  `DLL load failed while importing QtCore`.
- `numpy`, `PySide6`, `PyOpenGL` and `OpenEXR` are installed with pip rather
  than conda so each brings its own runtime libraries; mixing conda-forge
  numpy with pip Qt wheels can produce a broken BLAS on Windows. `OpenEXR`
  reads `.exr` HDRIs; `.hdr` files are read without it.
- `numba` compiles the path tracer (its `llvmlite` wheel carries LLVM, so no
  compiler is needed) and `mitsuba-oidn` brings Intel Open Image Denoise.
  Without numba the viewer runs as before and the Render panel says why it
  cannot render. The OptiX denoiser needs nothing installed: it is loaded
  from an NVIDIA graphics driver when there is one.
- DLSS 5 Neural Rendering needs a GeForce RTX 50 series GPU, a current
  driver, and the Neuroframe Engine (`neuroframe_engine_neural_rendering.dll`,
  `neuroframe_caller.dll`, `nvngx_dlssnr.dll`) from a Visual Enhancer
  release. The engine DLLs are © Merserk, shipped under the MIT license in
  that release's `LICENSE-Merserk.txt`; `nvngx_dlssnr.dll` is NVIDIA's, under `LICENSE-NVIDIA-DLSS.txt`.
  None of them is committed to this repository. Keep both license files
  beside the DLLs when bundling them.

#### Getting the Neural Rendering engine

The engine is never committed, so the desktop releases built by GitHub
Actions do not carry it; a build made on a machine with it in
`resources/dlssnr/` does. The Render panel's Neural Rendering group says
whether it was found. To get it:

1. Download the latest `Visual.Enhancer.v*.zip` from the
   [Visual Enhancer releases](https://github.com/Merserk/dlss5-visual-enhancer/releases/latest)
   (about 700 MB; only a few files are needed).
2. In the zip, open `bin/runtime/dlssnr/`. It holds the three DLLs and the
   two license files.
3. Either copy those five files into `resources/dlssnr/` in this repository
   (which a release build then bundles), or unzip Visual Enhancer anywhere
   and set **Preferences → Folders → Neural engine** to its folder. The
   Visual Enhancer folder, its `bin` or `bin/runtime`, or the `dlssnr`
   folder itself all work.
4. Open the Render panel: the Neural Rendering group should show
   *✓ DLSS 5 Neural Rendering (Neuroframe Engine …)*. Tick **Enhance the
   render** and press `F12`.

To check the engine on your GPU, run
`REFVIEW_NEURAL_ENGINE=resources/dlssnr pytest tests/test_trace_neural.py -k real`.

---

## Resources

```
resources/
  matcaps/   any PNG/JPG dropped here appears in the Matcap gallery
  hdris/     any .hdr/.exr here is offered in the Light group's HDRI list
  models/    the default folder the file dialog opens in
  dlssnr/    optional, never committed: the Neuroframe Engine's three DLLs,
             bundled into a release build for DLSS 5 Neural Rendering
```

Regenerate the bundled matcap set (analytic sphere renders, no downloads):

```bash
python tools/generate_matcaps.py
```

Point `REFVIEW_RESOURCES` at another directory to use your own library.

---

## Layout

```
src/refview/
  core/      pure Python, no Qt: mesh, the OBJ/STL/glTF loaders, the picking
             index, camera, raycasting, cross-sections, the pedestal, the
             grid, the scene's objects and their transforms,
             measurements, annotations, the armature and its landmark
             presets, the forms and the convex solids they are built from,
             the skeleton, its skinning and the rigging that grows one out
             of an armature or reads one off a file's joint names, the
             auto-skinning that gives a skeleton weights and the archive
             they are kept in, the body regions the skin's marks fall by,
             the progress a long job reports through, bookmarks, undo
             commands, settings, session persistence
  render/    OpenGL: shader programs, matcap and HDRI textures, offscreen
             targets, the skin tracer's tables, the scene and stroke renderers
  render/glsl/
             the shaders themselves, a file a stage, with the pieces several
             share -- the cross-section, the HDRI, the skin -- pulled in by
             #include
  trace/     the CPU path tracer: numba kernels for the BVH, the materials,
             the lights, the skin and the integrator, the film and its
             colour, the render jobs that run them across the cores, and
             the denoisers (Open Image Denoise, OptiX through ctypes, and a
             built-in filter), and DLSS 5 Neural Rendering through the
             Neuroframe Engine
  ui/        Qt: viewport widget, navigation, the measuring, annotating,
             armature, forms, pose and transform tools, the 2D overlay, the
             observable document, panels, the docks they live in, the tasks
             run off the window and the cards that show them, and the main
             window
  ui/elements/
             the controls the panels are built from: the reflowing layout,
             the folding frame, the sliders and swatches drawn by hand, and
             the machinery that copies a control into a panel of your own
tools/       the matcap generator and the path tracer benchmark
tests/       pytest suite for the core layer
```

Three rules keep the pieces apart:

- **`core` never imports Qt.** All of the geometry and document logic is
  testable without a display, which is what the test suite exercises.
- **`render` owns every GL call.** The viewport widget hands it a camera and a
  settings object and gets a drawn frame back. It also restores a neutral GL
  state afterwards, because the 2D overlay is painted with `QPainter` on the
  same context.
- **`trace` never imports Qt or GL, and nothing imports it at startup.** It
  takes numpy arrays and settings dataclasses and hands back a film, so it
  runs on worker threads and in tests without a display; the interface
  imports it the first time something is rendered, so numba costs nothing
  until then.
- **Panels edit dataclasses, never widgets belonging to someone else.** They
  mutate the settings held by `ViewerState` and emit a change signal; the
  viewport listens and repaints.
- **Every document edit is a command.** Four generic commands — set attributes,
  add, remove, replace — cover measurements, annotations, armatures and
  bookmarks alike, so undo needs no new code when a new kind of object turns
  up. The armature was added without a fifth, and so were the forms and the
  skeletons. The objects added one: an edit to the list -- a move, a
  linking, a merge -- is recorded as the list before and after, since a
  removal that re-hangs three children is not one attribute of one object.

Measurements are drawn in screen space with `QPainter` rather than as 3D
geometry. That gives reliable line thickness and antialiasing on every driver,
keeps them legible in front of the model, and makes the text labels free.

The armature is drawn in screen space for the opposite reason: it lives inside
the form, so geometry the model could hide would be a wire nobody ever saw. The
part behind the surface is dimmed instead, which takes one ray per node — cheap
for a figure, and cached against the camera so an orbit does not pay for it
every frame.

Annotations go the other way and are drawn as geometry, because paint on the
back of the model has to be hidden by it. Each segment becomes a quad that the
vertex shader widens in screen space, which keeps the brush a constant number
of pixels wide at any zoom — something `glLineWidth` cannot promise on a core
profile. The section contour is expanded through the same shader.

Every click, hover and painted sample casts a ray, so picking speed is what
decides whether a large scan still feels direct. Triangles are sorted along a
Morton curve into leaf boxes; a ray tests every box in one vectorised sweep and
then intersects only the triangles in the leaves it entered. On a
half-million-triangle mesh that is about 0.5 ms per ray against 90 ms for the
brute-force pass it replaced.

## Tests

```bash
pytest
```

## Changelog

Release notes live in [CHANGELOG.md](CHANGELOG.md).
