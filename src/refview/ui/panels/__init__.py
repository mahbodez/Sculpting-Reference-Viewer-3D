"""Dockable control panels."""

from .base import Panel
from .camera_panel import CameraPanel
from .matcap_panel import MatcapPanel
from .measure_panel import MeasurePanel
from .planes_panel import PlanesPanel
from .shading_panel import ShadingPanel

__all__ = ["CameraPanel", "MatcapPanel", "MeasurePanel", "Panel", "PlanesPanel", "ShadingPanel"]
