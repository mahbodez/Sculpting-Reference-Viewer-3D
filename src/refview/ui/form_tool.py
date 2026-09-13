"""Placing the landmarks of a form, led by a preset or by the artist, and correcting them.

The armature tool's guided walk, with the nodes and bones taken out of it: a
form is nothing but its landmarks, so a click records the landmark the panel
is asking for and the form is rebuilt from everything placed so far.  The
artist sees the bucket close over the pelvis as the last of its points goes
down, and the head thicken from a wedge to a block as the paired points
follow the midline ones.

A freeform has no list to walk.  The panel keeps a landmark pending -- the
name the artist typed and the side they chose -- and each click lays that one
down and readies the next, on the same side, until the artist says otherwise.

A landmark already placed is grabbable, which is the only way to correct one:
the form is derived from the landmarks and has no other handle to take.

Nothing here touches the document.  The tool works out what the new landmark
list is and the viewport hands it to the undo history, which is what keeps a
whole preset run, or a single dragged landmark, to one step.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace

import numpy as np

from ..core.armature import PlacedLandmark
from ..core.forms import (
    FORM_PRESETS,
    FREEFORM,
    FormSettings,
    PrimaryForm,
    form_spec,
    median_plane_ready,
    mirror_form_landmarks,
)
from ..core.landmarks import Landmark
from .picking import SurfacePicker

#: A placed landmark, as ``(index in the store, the preset's key for it)``.
FormLandmarkRef = tuple[int, str]


@dataclass
class FormRun:
    """A guided form part-way through."""

    preset: str
    #: Which form in the store the run is building into.
    form: int = -1
    #: Landmarks the artist chose to pass over.
    skipped: set[str] = field(default_factory=set)
    #: Freeform only: the landmark the next click lays down, as the panel
    #: has named and sided it.
    pending: Landmark | None = None

    @property
    def freeform(self) -> bool:
        return self.preset == FREEFORM


class FormTool:
    """Turns clicks into landmarks, and drags into moved ones."""

    #: How near the cursor has to be to take hold of a cross, in pixels.
    LANDMARK_REACH = 8.0

    def __init__(self) -> None:
        self.active = False
        #: The landmark the panel's list is editing, ringed in the view.
        self.selected_landmark: FormLandmarkRef | None = None
        self.hover_point: np.ndarray | None = None
        #: Landmark under the cursor, highlighted so it looks grabbable.
        self.hover_landmark: FormLandmarkRef | None = None
        #: Landmark currently being dragged.
        self.grabbed_landmark: FormLandmarkRef | None = None
        self.guide: FormRun | None = None

    # -- state ----------------------------------------------------------

    def set_active(self, active: bool) -> None:
        self.active = active
        if not active:
            self.cancel()

    def cancel(self) -> None:
        """Drop the hover preview, leaving any guided run alone.

        Escape means "stop for now", not "throw away the landmarks I spent
        five minutes placing"; ending a run is the panel's Finish button.
        """
        self.hover_point = None

    def end_guide(self) -> None:
        self.guide = None

    @property
    def guiding(self) -> bool:
        return self.guide is not None

    # -- the guided walk -------------------------------------------------

    def start_guide(self, preset: str, form: int) -> FormRun | None:
        """Begin a run against a form already in the store."""
        if preset not in FORM_PRESETS and preset != FREEFORM:
            return None
        self.guide = FormRun(preset=preset, form=form)
        return self.guide

    def _asked(self, form: PrimaryForm, settings: FormSettings) -> list[Landmark]:
        """Every landmark the walk will ask for under these choices.

        With mirroring on, the reflected half drops out -- unless the midline
        is not yet down far enough to fit a plane through, in which case the
        mirror has nothing to reflect across and the other side is asked for
        after all rather than never arriving.
        """
        run = self.guide
        spec = form_spec(form) if run is not None else None
        if run is None or spec is None:
            return []
        mirrored = settings.mirror and median_plane_ready(form)
        return [
            entry
            for entry in spec.landmarks
            if entry.key not in run.skipped and not (mirrored and entry.mirror_of)
        ]

    def remaining(self, form: PrimaryForm, settings: FormSettings) -> list[Landmark]:
        """The landmarks still to place, in order, the current one first."""
        done = {entry.key for entry in form.landmarks}
        return [entry for entry in self._asked(form, settings) if entry.key not in done]

    def current(self, form: PrimaryForm, settings: FormSettings) -> Landmark | None:
        """The landmark the artist is being asked for right now.

        For a freeform, the one the panel has pending: there is no list to
        work down, only the next point the artist has named.
        """
        run = self.guide
        if run is not None and run.freeform:
            return run.pending
        remaining = self.remaining(form, settings)
        return remaining[0] if remaining else None

    def progress(self, form: PrimaryForm, settings: FormSettings) -> tuple[int, int]:
        """How many landmarks are placed, out of how many will be asked for.

        A freeform asks for nothing in advance, so both numbers are simply
        how many are down.
        """
        run = self.guide
        if run is not None and run.freeform:
            return (len(form.landmarks), len(form.landmarks))
        wanted = self._asked(form, settings)
        done = {entry.key for entry in form.landmarks}
        return (sum(1 for entry in wanted if entry.key in done), len(wanted))

    def stage_progress(
        self, form: PrimaryForm, settings: FormSettings
    ) -> tuple[int, int, int] | None:
        """``(stage index, placed in it, asked for in it)`` for the current landmark.

        ``None`` once every landmark is placed.
        """
        run = self.guide
        spec = form_spec(form) if run is not None else None
        entry = self.current(form, settings)
        if run is None or spec is None or entry is None or run.freeform:
            return None
        stage = spec.stage_of(entry.key)
        done = {held.key for held in form.landmarks}
        asked = [held for held in self._asked(form, settings) if spec.stage_of(held.key) == stage]
        return stage, sum(1 for held in asked if held.key in done), len(asked)

    def skip(self, form: PrimaryForm, settings: FormSettings) -> None:
        """Pass over the landmark being asked for; the form loses what it fed."""
        entry = self.current(form, settings)
        if entry is not None and self.guide is not None:
            self.guide.skipped.add(entry.key)

    def back(self, form: PrimaryForm, settings: FormSettings) -> str | None:
        """Un-skip or un-place the landmark before this one, and ask again.

        Returns the key that was taken back, so the caller can drop it from
        the form within the same undo step.
        """
        run = self.guide
        spec = form_spec(form) if run is not None else None
        if run is None or spec is None or run.freeform:
            return None
        current = self.current(form, settings)
        mirrored = settings.mirror and median_plane_ready(form)
        limit = next(
            (i for i, entry in enumerate(spec.landmarks) if current and entry.key == current.key),
            len(spec.landmarks),
        )
        done = {entry.key for entry in form.landmarks}
        for entry in reversed(spec.landmarks[:limit]):
            if mirrored and entry.mirror_of:
                continue
            if entry.key in run.skipped:
                run.skipped.discard(entry.key)
                return entry.key
            if entry.key in done:
                return entry.key
        return None

    # -- picking --------------------------------------------------------

    @staticmethod
    def free_points(form: PrimaryForm, settings: FormSettings) -> bool:
        """Whether this form's landmarks go anywhere in space rather than on the skin.

        Only a freeform's ever do: a preset's landmarks are surface anatomy
        by definition, however the switch is set.
        """
        return settings.free_placement and form.freeform

    def pick(
        self,
        x: float,
        y: float,
        picker: SurfacePicker,
        settings: FormSettings,
        free: bool = False,
    ) -> np.ndarray | None:
        """Where a click at ``(x, y)`` would put a landmark: on the surface, or nowhere.

        With ``free`` the point lands on the camera-facing plane through the
        object centre instead, as the measure tool's free points do, so a
        landmark can be put inside the model as easily as on it.
        """
        if free:
            return picker.plane_point(x, y, picker.camera.scene_center)
        return picker.point(x, y, snap=settings.snap_to_vertex, snap_pixels=settings.snap_pixels)

    def drag_target(
        self,
        x: float,
        y: float,
        picker: SurfacePicker,
        settings: FormSettings,
        current: np.ndarray,
        free: bool = False,
    ) -> np.ndarray:
        """Where a grabbed landmark should move to.

        Free placement -- and a drag that wanders off the model -- slides the
        point across the plane it already sits on, so it never jumps to a
        surface the artist did not aim at.
        """
        if not free:
            point = picker.point(
                x, y, snap=settings.snap_to_vertex, snap_pixels=settings.snap_pixels
            )
            if point is not None:
                return point
        return picker.plane_point(x, y, current)

    def landmark_at(
        self,
        x: float,
        y: float,
        forms,
        picker: SurfacePicker,
        settings: FormSettings,
    ) -> FormLandmarkRef | None:
        """The nearest grabbable landmark under the cursor, if any.

        Only the ones on screen offer a grip.  A mirrored guess is included:
        taking hold of one is how the artist says it was a bad guess, and
        :meth:`~refview.core.forms.PrimaryForm.with_landmark_at` clears the
        flag for them.
        """
        if not settings.show_all or not settings.show_landmarks:
            return None
        best: FormLandmarkRef | None = None
        best_distance = self.LANDMARK_REACH
        for outer, form in enumerate(forms):
            if not form.visible:
                continue
            for landmark in form.landmarks:
                distance = picker.screen_distance(landmark.at, x, y)
                if distance is not None and distance <= best_distance:
                    best, best_distance = (outer, landmark.key), distance
        return best

    # -- gestures -------------------------------------------------------

    def place(
        self, form: PrimaryForm, point: np.ndarray, settings: FormSettings
    ) -> list[PlacedLandmark] | None:
        """The landmark list once a picked point answers the current question.

        ``None`` when there is nothing to answer: no run, or every landmark
        already placed.
        """
        entry = self.current(form, settings)
        if entry is None:
            return None
        landmarks = [existing for existing in form.landmarks if existing.key != entry.key]
        landmarks.append(PlacedLandmark(key=entry.key, at=tuple(float(v) for v in point)))
        points = form.with_point(entry) if form.freeform else None
        return self.derive(form, landmarks, settings, points)

    def derive(
        self,
        form: PrimaryForm,
        landmarks: list[PlacedLandmark],
        settings: FormSettings,
        points: list[Landmark] | None = None,
    ) -> list[PlacedLandmark]:
        """Mirror what is missing, on a copy of the list handed in.

        Copied for the reason the armature copies: the mirror moves an
        existing guess in place, and the list is usually built out of the
        document's own entries, which the undo history still points at.
        ``points`` is the freeform's named landmarks as they will be once
        this edit lands, when the edit changes them.
        """
        proxy = PrimaryForm(
            preset=form.preset,
            landmarks=[replace(entry) for entry in landmarks],
            points=list(form.points if points is None else points),
            fill=form.fill,
        )
        if settings.mirror:
            return mirror_form_landmarks(proxy)
        return proxy.landmarks
