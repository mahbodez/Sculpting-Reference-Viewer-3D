"""What the artist prefers, as distinct from what the document says.

There are two kinds of setting in this application and keeping them apart is
the whole point of this module.  A render setting belongs to the thing being
looked at: the matcap on it, where the section is cut, how the planes are
fitted.  Those travel in the session file, because handing someone the session
should hand them the view you were talking about.  A preference belongs to the
person at the machine: how fast the orbit turns under their hand, how large
the type is, whether the splash screen is worth the second it costs.  Those
stay on the machine and follow the artist from one model to the next, and it
would be wrong for opening somebody else's session to change how your mouse
behaves.

Everything here is a plain dataclass with a default, and the defaults are the
behaviour the application had before there was a preference for it -- so an
installation that never opens the Preferences window is not in some other mode
than one that does.  :func:`Preferences.from_dict` is deliberately forgiving:
settings written by a newer version, or edited by hand into nonsense, fall
back to the default for that one field rather than costing the artist the
rest of their preferences.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields, is_dataclass
from typing import Any

Color = tuple[float, float, float]

#: The orange the interface is built around, as it ships.  Kept here rather
#: than imported from the palette because core must not know about Qt, and
#: because this is the number a preference overrides -- the palette is where
#: the override lands, not where it starts.
DEFAULT_ACCENT: Color = (0.929, 0.545, 0.129)

#: How small and how large the interface type may be set, in pixels.  Below
#: the floor the captions inside the sliders stop being legible at arm's
#: length, which is the distance this application is read from; above the
#: ceiling a panel holds four rows.
MIN_FONT_SIZE = 8
MAX_FONT_SIZE = 20

#: Multiples of the shipped orbit and zoom rates.  A tenth is slow enough to
#: place a highlight exactly; three times is fast enough to spin the model
#: round with a flick, and past that a drag crosses the model twice.
MIN_SPEED = 0.1
MAX_SPEED = 3.0

#: Multisampling counts the viewport will ask a driver for.  Zero means "do
#: not ask", which is the setting for a machine where the edges matter less
#: than the frame rate.
SAMPLE_COUNTS = (0, 2, 4, 8, 16)


@dataclass
class InterfacePreferences:
    """How the application looks and how much of it folds away."""

    #: The one colour the interface uses for state -- a switch that is on, the
    #: track of a slider, the dot beside a group's name.  It is a preference
    #: because the sculpting applications an artist has open beside this one
    #: each have their own, and matching them is worth more than any argument
    #: about which orange is the right orange.
    accent: Color = DEFAULT_ACCENT
    #: Interface type size, in pixels.  Eleven is what the panels were drawn
    #: against; the rows grow with it, so a larger size costs panel width as
    #: well as height.
    font_size: int = 11
    #: Whether a group whose settings have gone dead folds itself away.  On is
    #: the rule the panels were rebuilt around: a control that cannot be used
    #: is worse than absent, because it takes the room of one that can.  Off
    #: is for anyone who would rather the panel never changed shape under
    #: them, and can live with the dead rows.
    fold_disabled: bool = True
    #: Whether the panels come back where they were left.  Off starts every
    #: session from the arrangement the application ships with, which is what
    #: a shared machine or a teaching room wants.
    restore_layout: bool = True


@dataclass
class NavigationPreferences:
    """How much camera a gesture buys.

    Nothing here changes what the gestures are, only how far each one goes.
    The two inversions exist because which way a drag should turn a model is
    the one question in navigation nobody has ever agreed on, and because an
    artist who has spent ten years in an application that does it the other
    way is not going to be argued out of it.
    """

    #: Multiple of the shipped degrees-of-orbit per pixel.
    orbit_speed: float = 1.0
    #: Multiple of the shipped zoom per wheel notch.
    zoom_speed: float = 1.0
    invert_orbit_x: bool = False
    invert_orbit_y: bool = False


@dataclass
class StartupPreferences:
    """What happens between the icon being clicked and the window arriving."""

    show_splash: bool = True
    #: Whether a release check runs quietly on the way in.  It already stays
    #: silent unless there is something newer, and it already runs off the
    #: UI thread -- but a machine with no route to the internet should not be
    #: reaching for one at all, and that is a decision for whoever owns it.
    check_updates: bool = True
    #: Whether the session last saved or loaded is opened again.  Off by
    #: default because the application is as often opened to look at something
    #: new as to carry on with something old, and restoring is the slower of
    #: the two to undo.
    reopen_last_session: bool = False


@dataclass
class ViewportPreferences:
    """What the 3D view costs the machine."""

    #: Multisample count asked of the driver.  Read once, on the way up: a
    #: context's sample count is fixed when it is made, so this one takes a
    #: restart, and the Preferences window says so rather than pretending.
    samples: int = 4
    #: Whether the machine is asked to stay awake while this window is in
    #: front.  An artist reads a pose for minutes with both hands in clay,
    #: which is exactly when the screen dims -- but a laptop on a train is a
    #: different proposition, so it is a preference and not a rule.
    keep_awake: bool = True


@dataclass
class FolderPreferences:
    """Where the artist's own material is kept.

    One entry so far, and the one that matters: a matcap collection is a
    thing artists build over years and keep with their brushes, not something
    they would like to copy into an application's own folder every time it is
    reinstalled.
    """

    #: Folder to read matcaps from, or empty for the ones that ship.
    matcaps: str = ""


@dataclass
class Preferences:
    """Everything above, in one object, which is what gets saved and applied."""

    interface: InterfacePreferences = field(default_factory=InterfacePreferences)
    navigation: NavigationPreferences = field(default_factory=NavigationPreferences)
    startup: StartupPreferences = field(default_factory=StartupPreferences)
    viewport: ViewportPreferences = field(default_factory=ViewportPreferences)
    folders: FolderPreferences = field(default_factory=FolderPreferences)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Any) -> "Preferences":
        """Read preferences back, keeping whatever makes sense and no less.

        A field that is missing, of the wrong type, or out of range is filled
        from the default and the rest are kept.  Settings files are edited by
        hand, copied between machines and written by other versions of this
        application, and none of those is a reason to hand somebody back a
        window with default everything.
        """
        prefs = cls()
        if not isinstance(data, dict):
            return prefs
        for group in fields(cls):
            written = data.get(group.name)
            if isinstance(written, dict):
                _fill(getattr(prefs, group.name), written)
        _clamp(prefs)
        return prefs


def _fill(group: Any, written: dict[str, Any]) -> None:
    """Copy what type-checks out of ``written`` and into ``group``.

    The default already sitting in the field is what says which type is
    wanted, so there is no schema to keep in step with the dataclasses: add a
    field above and it is read back without anything being added here.
    """
    for entry in fields(group):
        if entry.name not in written:
            continue
        current = getattr(group, entry.name)
        value = _as_kind_of(written[entry.name], current)
        if value is not None:
            setattr(group, entry.name, value)


def _as_kind_of(value: Any, like: Any) -> Any:
    """``value`` as the same sort of thing as ``like``, or ``None`` if it is not.

    A bool is checked before an int because in Python it is one, and ``True``
    arriving where a font size belongs is nonsense rather than the number one.
    """
    if isinstance(like, bool):
        return value if isinstance(value, bool) else None
    if isinstance(value, bool):
        return None
    if isinstance(like, int):
        return value if isinstance(value, int) else None
    if isinstance(like, float):
        return float(value) if isinstance(value, int | float) else None
    if isinstance(like, str):
        return value if isinstance(value, str) else None
    if isinstance(like, tuple):
        if not isinstance(value, list | tuple) or len(value) != len(like):
            return None
        numbers = tuple(float(one) for one in value if isinstance(one, int | float))
        return numbers if len(numbers) == len(like) else None
    return None


def _clamp(prefs: "Preferences") -> None:
    """Pull anything out of range back into it.

    The window cannot produce these values; a settings file can, and a font
    size of nought is an application nobody can read their way out of.
    """
    interface = prefs.interface
    interface.font_size = int(min(max(interface.font_size, MIN_FONT_SIZE), MAX_FONT_SIZE))
    interface.accent = tuple(min(max(channel, 0.0), 1.0) for channel in interface.accent)
    navigation = prefs.navigation
    navigation.orbit_speed = min(max(navigation.orbit_speed, MIN_SPEED), MAX_SPEED)
    navigation.zoom_speed = min(max(navigation.zoom_speed, MIN_SPEED), MAX_SPEED)
    if prefs.viewport.samples not in SAMPLE_COUNTS:
        prefs.viewport.samples = ViewportPreferences().samples


def equal(one: Any, other: Any) -> bool:
    """Whether two preference objects say the same thing.

    Dataclasses compare by value already; this exists so a caller can ask the
    question without having to know that, and so that comparing a group to
    something that is not one is False rather than an error.
    """
    if not is_dataclass(one) or not is_dataclass(other):
        return False
    return type(one) is type(other) and asdict(one) == asdict(other)
