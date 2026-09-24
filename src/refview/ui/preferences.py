"""Where the preferences are kept, and what happens when one changes.

:mod:`refview.core.preferences` says what a preference *is*; this says where it
lives and who it has to be told to.  Two jobs, and they are separate because
the first one has to stay free of Qt.

Living: one JSON blob under one settings key, rather than a key per field.
Preferences are read and written all at once -- the window applies the whole
object every time anything in it moves -- and a blob means a field added in a
later version arrives with its default instead of arriving missing, which is
the same thing but without any code to make it so.

Telling: some preferences are read at the moment they matter and need nothing
doing -- whether to check for updates is looked up once, on the way in.  The
rest have somebody holding a copy: the palette holds the accent, the style
sheet holds the type size, the navigation controller holds the orbit rate.
:func:`PreferenceStore.apply` pushes to the ones that belong to the process;
the window connects to :attr:`PreferenceStore.changed` for the ones that
belong to a widget it owns.  Nothing polls.
"""

from __future__ import annotations

import json

from PySide6.QtCore import QObject, QSettings, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication

from .. import paths
from ..core.preferences import Preferences

#: Where the whole of it is written.
KEY = "preferences/all"

#: The session last saved or loaded, and the model last opened, for
#: :attr:`~refview.core.preferences.StartupPreferences.reopen_last_session`.
#: Both, because most of what is worked on never becomes a session: a session
#: is what you save when there are marks on the model worth keeping, and
#: somebody who has spent an afternoon turning a model over has nothing saved
#: and still expects to find it there tomorrow.  Remembered whether or not the
#: preference is on, because it may be switched on tomorrow about the work
#: being done today.
LAST_SESSION = "session/last"
LAST_MODEL = "session/last_model"


class PreferenceStore(QObject):
    """The preferences, and one signal saying they have changed.

    A single instance, reached through :func:`store`.  It is a singleton
    because a preference is a fact about the machine rather than about any one
    window, and because two of them disagreeing would be a bug nobody would
    think to look for.
    """

    changed = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._value = Preferences()

    @property
    def value(self) -> Preferences:
        """The preferences as they stand.  Treat as read-only; use :meth:`set`."""
        return self._value

    def set(self, value: Preferences, *, save: bool = True) -> None:
        """Adopt ``value``, push what has to be pushed, and say so.

        Always announces, even when nothing in it moved.  Working out what
        actually changed would save a repaint and cost a comparison of every
        field in the object, and the thing being saved is a repaint of an
        interface somebody is looking at while they change it.
        """
        self._value = value
        if save:
            self.save()
        self.apply()
        self.changed.emit()

    def reset(self) -> None:
        """Back to how the application ships."""
        self.set(Preferences())

    # -- the settings file ----------------------------------------------

    def load(self, settings: QSettings | None = None) -> Preferences:
        """Read the preferences off the machine.  Never raises."""
        settings = settings or QSettings()
        written = settings.value(KEY, "")
        if isinstance(written, str) and written.strip():
            try:
                self._value = Preferences.from_dict(json.loads(written))
            except ValueError:
                # Hand-edited into something that is not JSON.  The defaults
                # are a working application; refusing to start is not.
                self._value = Preferences()
        self.apply()
        return self._value

    def save(self, settings: QSettings | None = None) -> None:
        settings = settings or QSettings()
        settings.setValue(KEY, json.dumps(self._value.to_dict()))

    # -- telling the rest of the process --------------------------------

    def apply(self) -> None:
        """Push the preferences that something in the process holds a copy of.

        Deliberately not the whole list.  What is here is everything with a
        holder that is not a widget -- the palette, the style sheet, the
        folder the matcaps come from.  Anything belonging to a window is that
        window's to apply, because the store has no business knowing which
        windows exist.
        """
        from .elements import frame, palette
        from .theme import apply_dark_theme, set_font_size

        interface = self._value.interface
        palette.set_accent(_qcolor(interface.accent))
        set_font_size(interface.font_size)
        frame.set_fold_disabled(interface.fold_disabled)
        paths.set_matcap_dir(self._value.folders.matcaps or None)
        from ..trace.neural import set_engine_dir

        set_engine_dir(self._value.folders.neural_engine or None)

        app = QApplication.instance()
        if isinstance(app, QApplication):
            apply_dark_theme(app)
            # The style sheet reaches every widget Qt draws; the ones drawn by
            # hand read the palette when they paint, and have to be asked.
            for window in app.topLevelWidgets():
                window.update()


def _qcolor(color) -> QColor:
    """A core colour triple as the Qt colour the palette wants."""
    red, green, blue = (max(0.0, min(1.0, float(one))) for one in color)
    return QColor.fromRgbF(red, green, blue)


_store: PreferenceStore | None = None


def store() -> PreferenceStore:
    """The one store, loading it off the machine the first time it is asked."""
    global _store
    if _store is None:
        _store = PreferenceStore()
        _store.load()
    return _store


def current() -> Preferences:
    """The preferences as they stand, for a caller that only wants to read."""
    return store().value


def forget() -> None:
    """Drop the loaded store, so the next call reads the settings again.

    For tests, which set an organisation and application name of their own and
    would otherwise be handed whatever the first of them loaded.
    """
    global _store
    _store = None
