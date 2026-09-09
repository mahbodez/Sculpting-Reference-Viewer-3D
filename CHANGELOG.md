# Changelog

All notable changes to Reference Viewer are recorded here. Versions follow
[semantic versioning](https://semver.org/): the minor number moves when
features land, the patch number when only fixes do.

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
