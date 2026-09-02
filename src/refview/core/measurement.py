"""Named point-to-point measurements and their presentation options."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

Color = tuple[float, float, float]

#: Unit labels offered in the UI.  The conversion itself is the user-supplied
#: ``MeasurementSettings.unit_scale``, since an OBJ file carries no units.
UNIT_NAMES: tuple[str, ...] = ("mm", "cm", "m", "in", "units")


@dataclass
class Measurement:
    """A straight distance between two points on the model surface."""

    start: tuple[float, float, float]
    end: tuple[float, float, float]
    name: str = "Measurement"
    visible: bool = True
    color: Color = (1.0, 0.78, 0.22)
    #: Locked measurements ignore the mouse.  New ones start locked so that
    #: taking the next measurement cannot nudge the last one out of place.
    locked: bool = True

    #: Attribute names of the two endpoints, indexed by handle.
    ENDPOINTS = ("start", "end")

    @property
    def length(self) -> float:
        """Distance in scene units."""
        return float(np.linalg.norm(np.subtract(self.end, self.start)))

    def endpoint(self, handle: int) -> np.ndarray:
        """One end of the measurement, ``0`` for the start and ``1`` for the end."""
        return np.asarray(getattr(self, self.ENDPOINTS[handle]), dtype=np.float64)

    def endpoint_field(self, handle: int) -> str:
        """Name of the attribute a handle edits, for building an undo command."""
        return self.ENDPOINTS[handle]

    @property
    def midpoint(self) -> np.ndarray:
        return (self.endpoint(0) + self.endpoint(1)) * 0.5


@dataclass
class MeasurementSettings:
    """How measurements are drawn and how their lengths are written out."""

    #: Name of the display unit, purely a label.
    unit_name: str = "cm"
    #: Multiplier from scene units to the display unit.
    unit_scale: float = 1.0
    decimals: int = 2
    line_width: float = 3.0
    point_radius: float = 4.0
    label_size: int = 11
    show_labels: bool = True
    show_all: bool = True
    snap_to_vertex: bool = False
    #: Pixel radius within which a click snaps to the nearest triangle corner.
    snap_pixels: float = 12.0
    #: Place and drag points anywhere in space instead of on the surface.  The
    #: point lands on the camera-facing plane through the object centre, so it
    #: stays where the cursor put it when the view turns.
    free_placement: bool = False
    #: Pixel radius of the draggable endpoint handles on unlocked measurements.
    handle_radius: float = 6.0

    def format_length(self, length: float) -> str:
        """Render a scene-unit length as a labelled display string."""
        return f"{length * self.unit_scale:.{self.decimals}f} {self.unit_name}".strip()


class MeasurementStore:
    """An ordered, named collection of measurements.

    Deliberately plain: the Qt layer wraps it and emits change signals, which
    keeps this class testable without a running application.
    """

    def __init__(self, items: list[Measurement] | None = None) -> None:
        self._items: list[Measurement] = list(items or [])

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index: int) -> Measurement:
        return self._items[index]

    @property
    def items(self) -> list[Measurement]:
        """The live list; mutate through the methods below where possible."""
        return self._items

    def add(self, measurement: Measurement) -> Measurement:
        self._items.append(measurement)
        return measurement

    def create(self, start: np.ndarray, end: np.ndarray, name: str | None = None) -> Measurement:
        """Append a measurement, auto-naming it when no name is supplied."""
        measurement = Measurement(
            start=tuple(float(v) for v in start),
            end=tuple(float(v) for v in end),
            name=name or self.next_name(),
        )
        return self.add(measurement)

    def next_name(self) -> str:
        return f"Measurement {len(self._items) + 1}"

    def clear(self) -> None:
        self._items.clear()
