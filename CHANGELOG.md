# Changelog

All notable changes to Reference Viewer are recorded here. Versions follow
[semantic versioning](https://semver.org/): the minor number moves when
features land, the patch number when only fixes do.

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
