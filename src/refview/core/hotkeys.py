"""Which keys do what, as the artist has decided rather than as it ships.

A hotkey is a preference in the sense :mod:`refview.core.preferences` means
it: a fact about the person at the machine, kept on the machine, and carried
from one model to the next.  It is kept apart from the rest of the
preferences because it is not a fixed set of fields.  The commands a key can
be put on are declared by the window as it builds -- the menu entries, the
single keys the view answers to -- and then by every button and switch in
every panel, which is a list that grows with the panels built by hand and is
not known until the panels are.

So the map holds two things.  The *commands*, declared at run time, each with
the keys it ships with; and the artist's *choices*, which is the only part
written down: what they moved, and what they took away.  A command they never
touched keeps its shipped keys, which means a release that adds a command
arrives with that command's keys already on it, and a choice made about a
control that is not there today -- a copy in a panel since thrown away, a
button a later version renamed -- is kept rather than dropped, in case it
comes back.

One key, one command.  A key that opened two things would open neither, and
the window asks before it takes a key away from what had it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

#: Where a command's keys are listened for.  ``"window"`` is anywhere in the
#: window, which is what a menu entry gets; ``"view"`` is only while the 3D
#: view has the focus, which is what the single-letter keys get so that a
#: letter typed into a name never arms a tool.
SCOPES = ("window", "view")

#: Commands made out of the panels' own buttons and switches carry this in
#: front of the control's id, so that ``section.enabled`` the control and a
#: command that happened to share the name could never be confused.
CONTROL_PREFIX = "control:"


@dataclass(frozen=True)
class Command:
    """Something a key can be put on: what it is called, and what it ships with."""

    id: str
    label: str
    default: str = ""
    scope: str = "window"
    #: Where it is found, for a list that has to sort hundreds of these.
    group: str = ""


class HotkeyMap:
    """The commands, their shipped keys, and the artist's changes to them."""

    def __init__(self) -> None:
        self._commands: dict[str, Command] = {}
        #: Command id -> keys, only for what the artist moved; ``""`` for a
        #: command whose keys were taken away.
        self._chosen: dict[str, str] = {}

    # -- the commands ---------------------------------------------------

    def declare(self, command: Command) -> None:
        """Make a command known, or bring its label and default up to date."""
        if command.scope not in SCOPES:
            raise ValueError(f"unknown hotkey scope {command.scope!r}")
        self._commands[command.id] = command
        # The choices are read before the window has declared anything, so
        # a shipped key the artist has since put on something else is only
        # found out about now -- and has to come off this command, or both
        # would answer to it.
        taken = any(chosen == command.default for chosen in self._chosen.values())
        if command.id not in self._chosen and command.default and taken:
            self._chosen[command.id] = ""

    def forget(self, command_id: str) -> None:
        """Take a command off the list, keeping any choice made about it."""
        self._commands.pop(command_id, None)

    def command(self, command_id: str) -> Command | None:
        return self._commands.get(command_id)

    def commands(self) -> list[Command]:
        return list(self._commands.values())

    # -- what the keys are ----------------------------------------------

    def keys_for(self, command_id: str) -> str:
        """The keys on a command now: the artist's choice, else what it ships with."""
        if command_id in self._chosen:
            return self._chosen[command_id]
        command = self._commands.get(command_id)
        return command.default if command is not None else ""

    def default_for(self, command_id: str) -> str:
        command = self._commands.get(command_id)
        return command.default if command is not None else ""

    def is_changed(self, command_id: str) -> bool:
        """Whether the artist has moved this command off what it ships with."""
        return command_id in self._chosen

    def holder_of(self, keys: str) -> str | None:
        """Which command has these keys, if any."""
        if not keys:
            return None
        for command_id, chosen in self._chosen.items():
            if chosen == keys:
                return command_id
        for command in self._commands.values():
            if command.default == keys and command.id not in self._chosen:
                return command.id
        return None

    def bound(self) -> dict[str, str]:
        """Every command with keys on it, declared or not, as id -> keys."""
        keys = {
            command.id: command.default
            for command in self._commands.values()
            if command.default and command.id not in self._chosen
        }
        keys.update((command_id, chosen) for command_id, chosen in self._chosen.items() if chosen)
        return keys

    # -- changing them --------------------------------------------------

    def assign(self, command_id: str, keys: str) -> str | None:
        """Put ``keys`` on a command, taking them off whatever had them.

        Returns the id of the command the keys were taken from, if there was
        one; asking first is the window's job, and it asks before it calls.
        ``""`` takes the command's keys away.  Choosing the shipped keys again
        is the same as never having chosen, so the choice is dropped rather
        than written down.
        """
        previous = self.holder_of(keys) if keys else None
        if previous == command_id:
            previous = None
        if previous is not None:
            self._choose(previous, "")
        self._choose(command_id, keys)
        return previous

    def clear(self, command_id: str) -> None:
        self._choose(command_id, "")

    def reset(self, command_id: str | None = None) -> str | None:
        """Back to the shipped keys, for one command or for all of them.

        For one command this is an assignment like any other, and says which
        command the shipped keys came off, if the artist had put them there.
        """
        if command_id is None:
            self._chosen.clear()
            return None
        return self.assign(command_id, self.default_for(command_id))

    def _choose(self, command_id: str, keys: str) -> None:
        if keys == self.default_for(command_id):
            self._chosen.pop(command_id, None)
        else:
            self._chosen[command_id] = keys

    # -- the settings file ----------------------------------------------

    def to_dict(self) -> dict[str, str]:
        """Only the choices; the commands and their defaults belong to the code."""
        return dict(self._chosen)

    def read(self, data: Any) -> None:
        """Take the choices out of a settings file, keeping what makes sense.

        Forgiving, for the same reason the preferences are: a file edited by
        hand or written by another version should cost the one entry that is
        nonsense and not the rest.  A key found on two commands is left with
        the first of them, since two commands on one key is the one state the
        map is not allowed to be in.
        """
        self._chosen.clear()
        if not isinstance(data, dict):
            return
        seen: set[str] = set()
        for command_id, keys in data.items():
            if not isinstance(command_id, str) or not isinstance(keys, str) or not command_id:
                continue
            if keys and keys in seen:
                continue
            self._chosen[command_id] = keys
            if keys:
                seen.add(keys)
        # A shipped key the file gave to something else has to come off the
        # command that ships with it, or both would answer to it.
        for command in self._commands.values():
            if command.id in self._chosen or not command.default:
                continue
            if command.default in seen:
                self._chosen[command.id] = ""

    def is_default(self) -> bool:
        return not self._chosen
