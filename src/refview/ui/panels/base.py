"""Shared plumbing for the dockable side panels."""

from __future__ import annotations

from contextlib import contextmanager

from PySide6.QtWidgets import QVBoxLayout, QWidget

from ..state import ViewerState
from ..widgets import relax_widths


class Panel(QWidget):
    """A panel bound to the :class:`ViewerState`.

    Subclasses build their controls in ``_build`` and refresh them from the
    state in ``refresh``.  Refreshes run inside :meth:`_suppressed` so that
    programmatic widget updates never echo back as user edits.

    Whatever they build is then made squeezable, once, here rather than in each
    of them -- see :func:`~refview.ui.widgets.relax_widths`.  A panel is a
    column of controls in a dock the artist sizes to taste, so none of it is
    allowed to have an opinion about how wide that dock has to be.
    """

    def __init__(self, state: ViewerState, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._state = state
        self._suppress_depth = 0
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(8, 8, 8, 8)
        self._layout.setSpacing(8)
        self._build()
        relax_widths(self)
        self.refresh()

    # -- hooks ----------------------------------------------------------

    def _build(self) -> None:  # pragma: no cover - overridden by subclasses
        raise NotImplementedError

    def refresh(self) -> None:
        """Pull current values out of the state and into the widgets."""

    def shown(self) -> bool | None:
        """Whether what this panel draws is on screen, or ``None`` if it draws nothing.

        The switch on the panel's tab reads this and writes :meth:`set_shown`,
        so the forms, the armature, the measurements can be shown or hidden
        without opening the tab.  A panel that only sets things -- the camera,
        the matcap -- leaves it at ``None`` and gets no switch.
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
        self._layout.addWidget(widget)
        return widget

    def _add_stretch(self) -> None:
        self._layout.addStretch(1)
