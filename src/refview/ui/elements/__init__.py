"""The widgets the panels are built out of, and the rules they follow.

Four ideas, in the order they depend on each other:

``reflow``
    A panel is a list of groups and the layout decides how many columns to
    break it into, from the width it was given.  That is what lets the same
    panel be a strip down the side of the window and a band across the bottom
    without knowing which it is.

``frame``
    A group of controls under a bar you can click to fold it away.  Every
    group in the application is one, including the ones in panels built by
    hand.

``slider`` and ``controls``
    The controls themselves, drawn rather than assembled, so that a row says
    what it is and what it is set to in one row's worth of height.

``clone`` and ``custom``
    Alt-drag a control and a working copy comes away, to be dropped into a
    panel you built.  The copy drives the original; it is not a second one.

``keys``
    Ctrl-Alt-click a button and a key can be put on it.  The gesture only
    says which button; what the key does about it is the window's business.
"""

from .clone import can_clone, watch_tree
from .clone import clone as clone_of
from .controls import ColorButton, PointEdit
from .custom import CustomPanel
from .dock import PanelDock
from .frame import Frame, frame_form, framed
from .keys import COMMAND_PROPERTY, KeyGesture, can_take_key, watch_keys
from .naming import caption_for, lookup, name_tree, register
from .reflow import COLUMN_WIDTH, Reflow, ReflowLayout
from .slider import ValueSlider

__all__ = [
    "COLUMN_WIDTH",
    "COMMAND_PROPERTY",
    "ColorButton",
    "CustomPanel",
    "Frame",
    "KeyGesture",
    "PanelDock",
    "PointEdit",
    "Reflow",
    "ReflowLayout",
    "ValueSlider",
    "can_clone",
    "can_take_key",
    "caption_for",
    "clone_of",
    "frame_form",
    "framed",
    "lookup",
    "name_tree",
    "register",
    "watch_keys",
    "watch_tree",
]
