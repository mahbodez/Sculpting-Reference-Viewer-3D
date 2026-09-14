"""Making the whole of a switch the part you can press.

The theme turns every check box into a button: no tick box, a face, a border,
and the accent across it when it is on.  What the theme cannot reach is where
Qt thinks such a thing can be clicked.  A check box asks the style for that,
and the style works it out the only way it knows -- the tick box, plus the
gap, plus the words -- so what comes back is the text and nothing else.  The
result is a control that looks like a button the width of the panel and
answers only if you hit the letters in the middle of it, which is worse than
either of the two things it could have been.

So the press is taken before the check box sees it and turned into a click.
One filter on the application rather than a subclass, because the check boxes
are built in a dozen panels that have no reason to know any of this, and
because the ones that arrive later -- a copy dropped into a panel built by
hand, a dialog opened once -- are then covered by the same rule without
anybody having to remember it.

Alt is left alone: Alt and a drag is how a control is copied out of its panel,
and that gesture has to reach the filter that implements it whichever of the
two was installed first.
"""

from __future__ import annotations

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtWidgets import QApplication, QCheckBox, QRadioButton


class WholeFaceToggles(QObject):
    """Turns a press anywhere on a switch into a click on it."""

    _instance: "WholeFaceToggles | None" = None

    def __init__(self) -> None:
        super().__init__()
        self._armed: QObject | None = None

    @classmethod
    def install(cls, app: QApplication) -> "WholeFaceToggles":
        """Put the rule in place for every switch in the application."""
        if cls._instance is None:
            cls._instance = WholeFaceToggles()
            app.installEventFilter(cls._instance)
        return cls._instance

    def eventFilter(self, watched, event) -> bool:  # noqa: N802 - Qt contract
        if not isinstance(watched, QCheckBox | QRadioButton):
            return False
        kind = event.type()
        if kind == QEvent.Type.MouseButtonPress:
            if (
                event.button() != Qt.MouseButton.LeftButton
                or event.modifiers() & Qt.KeyboardModifier.AltModifier
                or not watched.isEnabled()
            ):
                return False
            self._armed = watched
            return True
        if kind == QEvent.Type.MouseButtonRelease and self._armed is watched:
            self._armed = None
            # A radio button that is already on stays on, as it should.
            already = isinstance(watched, QRadioButton) and watched.isChecked()
            if watched.rect().contains(event.position().toPoint()) and not already:
                watched.click()
            return True
        return False
