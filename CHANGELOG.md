# Changelog

All notable changes to Reference Viewer are recorded here. Versions follow
[semantic versioning](https://semver.org/): the minor number moves when
features land, the patch number when only fixes do.

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
