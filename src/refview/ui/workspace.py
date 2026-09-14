"""Where the panels are, and remembering where the artist put them.

The window owns a viewport and a set of docks; this owns the docks.  Keeping
them here rather than in the window is what keeps the window readable, because
the docks are now the larger half of it: ten panels that each go anywhere, any
number of panels built by hand, and a layout that has to survive being closed
and opened again.

Two things are written down.  Qt writes where every dock is -- which edge,
which tab strip, how wide -- into one opaque blob, and that is the part nobody
should try to understand.  What Qt cannot write down is the panels that did
not exist when it started: a panel built by hand is a name and a list of
controls copied from elsewhere, and it has to be rebuilt before Qt is asked to
put the docks back, or Qt will find a dock missing and quietly drop its place
in the layout.  So: our part first, then Qt's.
"""

from __future__ import annotations

import json
from contextlib import suppress

from PySide6.QtCore import QByteArray, QObject, QSettings, Qt, QTimer, Signal
from PySide6.QtWidgets import QCheckBox, QMainWindow, QTabBar, QWidget

from .elements.clone import watch_tree
from .elements.custom import CustomPanel
from .elements.dock import PanelDock, make_switch
from .elements.naming import forget, name_tree, register
from .panels.base import Panel
from .widgets import scrollable

#: Where the settings for all this live.
_GEOMETRY = "workspace/geometry"
_STATE = "workspace/state"
_CUSTOM = "workspace/custom"

#: How narrow a dock may be pulled.  The panels no longer insist on a width of
#: their own, so this is the only thing left that decides, and it wants to be
#: the smallest number at which a row is still worth using: a caption, a bar
#: long enough to drag, and the number written in it.  A panel with a longer
#: caption than that scrolls rather than holding every other panel wide.
DOCK_MIN_WIDTH = 190

#: The name a panel built by hand gets when it is not given one.
NEW_PANEL_NAME = "Custom"


class Workspace(QObject):
    """The docks of one window: the fixed panels and the ones built by hand."""

    #: Something that would be written down has changed.
    changed = Signal()

    def __init__(self, window: QMainWindow) -> None:
        super().__init__(window)
        self._window = window
        #: Every dock, in the order it was added, keyed by the name Qt saves.
        self._docks: dict[str, PanelDock] = {}
        #: The fixed panels, keyed the same way.
        self._panels: dict[str, Panel] = {}
        #: The panels built by hand, keyed the same way.
        self._custom: dict[str, CustomPanel] = {}
        #: The switch on each dock bar and each dock tab, with its panel.
        self._switches: list[tuple[QCheckBox, Panel]] = []
        #: Docks of hand-built panels that have been taken away, kept rather
        #: than destroyed, and handed back out when another is asked for.  See
        #: :meth:`remove_custom_panel` for why they are not destroyed.
        self._parked: dict[str, PanelDock] = {}
        self._next_custom = 1

    # -- the fixed panels --------------------------------------------------

    def add_panel(self, key: str, title: str, panel: Panel) -> PanelDock:
        """Give a panel a dock of its own, stacked with the ones before it."""
        dock = self._dock(key, title, scrollable(panel))
        self._panels[key] = panel
        name_tree(panel, owner=panel)
        register(panel, key)
        watch_tree(panel)
        if panel.shown() is not None:
            switch = dock.bar().add_switch(
                f"Show or hide what the {title} panel puts on the model"
            )
            switch.setChecked(bool(panel.shown()))
            switch.toggled.connect(panel.set_shown)
            self._switches.append((switch, panel))
        return dock

    def panel(self, key: str) -> Panel | None:
        return self._panels.get(key)

    def panels(self) -> list[Panel]:
        return list(self._panels.values())

    def docks(self) -> list[PanelDock]:
        return list(self._docks.values())

    def sync_switches(self) -> None:
        """Keep every switch agreeing with the panel it speaks for."""
        for switch, panel in list(self._switches):
            try:
                blocked = switch.blockSignals(True)
            except RuntimeError:
                # Qt threw the tab away when the stack it was in came apart.
                self._switches.remove((switch, panel))
                continue
            switch.setChecked(bool(panel.shown()))
            switch.blockSignals(blocked)

    # -- the switch on a tab -----------------------------------------------

    def dress_tabs(self) -> None:
        """Hang a show/hide switch on every dock tab that wants one.

        A dock stacked behind others shows nothing but its tab: its own bar,
        and the switch on it, are hidden with the rest of the panel.  That is
        the state the panels spend almost all their time in, and it is exactly
        when the switch earns its keep -- "take the armature off for a second"
        is a thing you want to do while looking at the model, not a reason to
        go and find the armature panel.  So the switch is put on the tab too.

        Qt builds these tab bars itself, and throws them away and builds new
        ones as docks are stacked and unstacked, so there is nothing to hook
        on to and nothing that stays put.  Hence: look for bars that have not
        been dressed yet, and look again after anything that could have made
        one.  Dressing a tab twice is what the guard below is for.
        """
        for bar in self._window.findChildren(QTabBar):
            _widen(bar)
            for index in range(bar.count()):
                if bar.tabButton(index, QTabBar.ButtonPosition.LeftSide) is not None:
                    continue
                panel = self._panel_titled(bar.tabText(index))
                if panel is None or panel.shown() is None:
                    continue
                switch = make_switch(
                    f"Show or hide what the {bar.tabText(index)} panel puts on the model"
                )
                switch.setChecked(bool(panel.shown()))
                switch.toggled.connect(panel.set_shown)
                bar.setTabButton(index, QTabBar.ButtonPosition.LeftSide, switch)
                bar.setTabToolTip(index, bar.tabText(index))
                self._switches.append((switch, panel))

    def _panel_titled(self, title: str) -> Panel | None:
        """The panel whose dock is called ``title``, if there is one."""
        for key, dock in self._docks.items():
            if dock.windowTitle() == title:
                return self._panels.get(key)
        return None

    def _dress_soon(self) -> None:
        """Dress the tabs once Qt has finished rearranging them."""
        QTimer.singleShot(0, self.dress_tabs)

    # -- the panels built by hand ------------------------------------------

    def new_custom_panel(self, title: str | None = None, key: str | None = None) -> CustomPanel:
        """An empty panel of the artist's own, docked on the right.

        A dock put away earlier under the same name is taken back out and
        emptied rather than a new one being built, which is the whole of what
        keeps this safe; see :meth:`remove_custom_panel`.
        """
        if key is None:
            key = f"custom_{self._next_custom}"
            while key in self._docks:
                self._next_custom += 1
                key = f"custom_{self._next_custom}"
        self._next_custom = max(self._next_custom, _number_in(key) + 1)
        name = title or f"{NEW_PANEL_NAME} {_number_in(key)}"

        revived = self._revive(key, name)
        if revived is not None:
            self.changed.emit()
            return revived

        panel = CustomPanel(name)
        dock = self._dock(key, name, scrollable(panel))
        panel.changed.connect(self.changed.emit)
        panel.changed.connect(lambda: dock.setWindowTitle(panel.title()))
        self._custom[key] = panel
        self.changed.emit()
        return panel

    def _revive(self, key: str, name: str) -> CustomPanel | None:
        """Take a parked dock back out under ``key``, emptied and renamed."""
        dock = self._parked.pop(key, None)
        if dock is None:
            # Any parked dock will do: they differ only in what is written on
            # them, and the name a dock was saved under is not worth a crash.
            if not self._parked:
                return None
            key, dock = self._parked.popitem()
        panel = self._panel_in(dock)
        if panel is None:  # pragma: no cover - a dock we did not fill
            return None
        panel.clear()
        panel.set_title(name)
        dock.setWindowTitle(name)
        dock.show()
        self._docks[key] = dock
        self._custom[key] = panel
        self._dress_soon()
        return panel

    @staticmethod
    def _panel_in(dock: PanelDock) -> CustomPanel | None:
        body = dock.widget()
        found = body.findChildren(CustomPanel) if body is not None else []
        return found[0] if found else None

    def custom_panels(self) -> dict[str, CustomPanel]:
        return dict(self._custom)

    def reveal(self, panel: CustomPanel) -> None:
        """Open the dock a hand-built panel lives in and bring it to the front."""
        for key, held in self._custom.items():
            if held is panel:
                dock = self._docks.get(key)
                if dock is not None:
                    dock.show()
                    dock.raise_()
                return

    def remove_custom_panel(self, key: str) -> None:
        """Take a hand-built panel away.  Its dock is parked, not destroyed.

        The dock has to survive, and the reason is Qt's rather than ours.
        Once :meth:`QMainWindow.restoreState` has arranged the docks, taking
        one out of that arrangement and putting another in leaves the dock
        area reading freed memory, and the process goes down inside Qt's own
        layout with nothing of ours on the stack.  Every way of putting the
        dock down does it -- ``removeDockWidget`` alone is enough, with or
        without ``setParent(None)``, a deferred delete, or an immediate one --
        and a window whose layout was never restored survives all of them, so
        it is the restored arrangement that cannot be edited, not the removal.

        There being no way to tidy that up through the API, the dock is simply
        never given up: it is emptied, hidden, and kept for the next panel
        somebody builds.  A hidden dock shows nothing, costs a widget, and
        cannot be reached from the Panels menu, which lists what is in
        :attr:`_docks` and not what is parked.  The artist sees a panel go and
        another arrive; Qt sees the same docks it was handed at startup.
        """
        panel = self._custom.pop(key, None)
        dock = self._docks.pop(key, None)
        if panel is not None:
            forget(key)
            panel.clear()
        if dock is not None:
            dock.hide()
            self._parked[key] = dock
        self.changed.emit()

    # -- building a dock ---------------------------------------------------

    def _dock(self, key: str, title: str, body: QWidget) -> PanelDock:
        dock = PanelDock(key, title, self._window)
        body.setMinimumWidth(DOCK_MIN_WIDTH)
        dock.setWidget(body)
        previous = self._last_dock()
        self._window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        if previous is not None:
            # New docks arrive tabbed behind the ones already there, which is
            # the layout the application used to have and the only one that
            # fits ten panels on a laptop screen.  Dragging one out of the
            # strip is then a deliberate act rather than the starting state.
            self._window.tabifyDockWidget(previous, dock)
        dock.visibilityChanged.connect(lambda _shown: self._moved())
        dock.topLevelChanged.connect(lambda _floating: self._moved())
        dock.dockLocationChanged.connect(lambda _area: self._moved())
        self._docks[key] = dock
        self._dress_soon()
        return dock

    def _moved(self) -> None:
        self.changed.emit()
        self._dress_soon()

    def _last_dock(self) -> PanelDock | None:
        for dock in reversed(list(self._docks.values())):
            if self._window.dockWidgetArea(dock) == Qt.DockWidgetArea.RightDockWidgetArea:
                return dock
        return None

    def raise_first(self) -> None:
        """Bring the first panel to the front of the tab strip."""
        for dock in self._docks.values():
            dock.raise_()
            return

    # -- writing it down ---------------------------------------------------

    def to_dict(self) -> dict:
        """The part of the layout Qt cannot describe."""
        return {
            "custom": [
                {"key": key, **panel.to_dict()} for key, panel in self._custom.items()
            ],
        }

    def restore(self, data: dict) -> None:
        """Rebuild the panels built by hand.  Call before :meth:`restore_state`.

        Whatever was there is taken away first -- which parks those docks
        rather than destroying them, so the ones built here are usually the
        same docks under new names.  See :meth:`remove_custom_panel`.
        """
        for key in list(self._custom):
            self.remove_custom_panel(key)
        for entry in data.get("custom") or []:
            key = str(entry.get("key") or "")
            if not key:
                continue
            panel = self.new_custom_panel(str(entry.get("title") or ""), key=key)
            panel.restore(entry)
            dock = self._docks.get(key)
            if dock is not None:
                dock.setWindowTitle(panel.title())

    def save(self, settings: QSettings | None = None) -> None:
        """Write the whole layout, ours and Qt's, into the settings."""
        settings = settings or QSettings()
        settings.setValue(_GEOMETRY, self._window.saveGeometry())
        settings.setValue(_STATE, self._window.saveState())
        settings.setValue(_CUSTOM, json.dumps(self.to_dict()))

    def load(self, settings: QSettings | None = None) -> bool:
        """Put the layout back.  Returns whether there was one to put back."""
        settings = settings or QSettings()
        written = settings.value(_CUSTOM, "")
        if isinstance(written, str) and written.strip():
            # A settings file someone has edited, or one written by a version
            # that wrote something else: the layout is the least important
            # thing in the application, and none of it is worth refusing to
            # start over.
            with suppress(ValueError):
                self.restore(json.loads(written))
        state = settings.value(_STATE)
        geometry = settings.value(_GEOMETRY)
        if isinstance(geometry, QByteArray) and not geometry.isEmpty():
            self._window.restoreGeometry(geometry)
        if isinstance(state, QByteArray) and not state.isEmpty():
            put_back = self._window.restoreState(state)
            # Qt has just built whatever tab strips the saved layout called
            # for, and none of them carries a switch yet.
            self._dress_soon()
            return put_back
        self._dress_soon()
        return False

    def reset(self, settings: QSettings | None = None) -> None:
        """Put every dock back where it started, now.

        Not "forget the saved layout and restart": someone who has dragged the
        panels into a mess wants them tidied, and being told to close the
        application is not tidying.  So the arrangement is rebuilt here -- each
        dock returned to the right-hand side and stacked with the rest, in the
        order they were made, everything shown, the first one to the front --
        and the saved layout is dropped so that nothing puts the mess back.

        The panels built by hand are kept, with their copies: they are work,
        not arrangement.  They come back at the end of the same stack.
        """
        settings = settings or QSettings()
        for key in (_GEOMETRY, _STATE, _CUSTOM):
            settings.remove(key)

        previous: PanelDock | None = None
        for dock in self._docks.values():
            dock.setFloating(False)
            self._window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
            if previous is not None:
                self._window.tabifyDockWidget(previous, dock)
            dock.show()
            previous = dock
        self.raise_first()
        self._dress_soon()
        self.changed.emit()


def _widen(bar: QTabBar) -> None:
    """Let a strip of tabs keep its names, and scroll if they do not fit.

    Ten panels in one dock is ten tabs across the width of it, and with a
    switch on each there is not room for all ten names -- so Qt shortens them,
    and a strip reading "Pl...", "Se...", "Me..." is one you have to read
    twice.  Better that each tab be as wide as its name and the few that fall
    off the end be scrolled to: the name is the only thing on a tab worth
    anything, and scrolling costs you only the panels you were not looking at.
    """
    bar.setElideMode(Qt.TextElideMode.ElideNone)
    bar.setUsesScrollButtons(True)
    bar.setExpanding(False)


def _number_in(key: str) -> int:
    """The number at the end of a custom panel's key, or nought."""
    tail = key.rsplit("_", 1)[-1]
    return int(tail) if tail.isdigit() else 0
