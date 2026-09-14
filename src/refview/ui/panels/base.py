"""Shared plumbing for the dockable panels."""

from __future__ import annotations

from contextlib import contextmanager

from PySide6.QtWidgets import QWidget

from ..elements.naming import name_tree
from ..elements.reflow import Reflow
from ..state import ViewerState
from ..widgets import name_sliders, relax_widths


class Panel(Reflow):
    """A panel bound to the :class:`ViewerState`.

    Subclasses build their controls in ``_build`` and refresh them from the
    state in ``refresh``.  Refreshes run inside :meth:`_suppressed` so that
    programmatic widget updates never echo back as user edits.

    What a subclass builds is a list of groups, and how that list is laid out
    is not a subclass's business: the panel is a :class:`Reflow`, so the groups
    stack into one column in a dock down the side of the window and break into
    several in a dock along the bottom, from the width alone.  A panel does not
    know or care which of those it currently is.

    Two things are then done to whatever was built, once, here rather than in
    each of them.  It is made squeezable -- see
    :func:`~refview.ui.widgets.relax_widths` -- because a panel is sized by the
    artist and none of it is allowed to have an opinion about how wide its dock
    has to be.  And everything in it is named, so that a copy of any control
    can be written down and found again next time; see
    :mod:`refview.ui.elements.naming`.
    """

    def __init__(self, state: ViewerState, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._state = state
        self._suppress_depth = 0
        self._build()
        name_sliders(self)
        relax_widths(self)
        name_tree(self, owner=self)
        self.refresh()

    # -- hooks ----------------------------------------------------------

    def _build(self) -> None:  # pragma: no cover - overridden by subclasses
        raise NotImplementedError

    def refresh(self) -> None:
        """Pull current values out of the state and into the widgets."""

    def shown(self) -> bool | None:
        """Whether what this panel draws is on screen, or ``None`` if it draws nothing.

        The switch on the panel's own dock bar reads this and writes
        :meth:`set_shown`, so the forms, the armature, the measurements can be
        shown or hidden without opening the panel.  A panel that only sets
        things -- the camera, the matcap -- leaves it at ``None`` and gets no
        switch.
        """
        return None

    def set_shown(self, on: bool) -> None:
        """Show or hide what this panel draws; see :meth:`shown`."""

    # -- helpers --------------------------------------------------------

    @property
    def state(self) -> ViewerState:
        return self._state

    @contextmanager
    def _suppressed(self):
        """Ignore widget signals for the duration of the block."""
        self._suppress_depth += 1
        try:
            yield
        finally:
            self._suppress_depth -= 1

    @property
    def _busy(self) -> bool:
        return self._suppress_depth > 0

    def _add(self, widget: QWidget) -> QWidget:
        return self.add(widget)

    def _add_stretch(self) -> None:
        """Nothing: the reflow already packs its groups against the top.

        Kept because every panel ends with a call to it, and because what the
        call means -- "that is the last group" -- is still worth writing down
        even now that nothing has to be done about it.
        """
