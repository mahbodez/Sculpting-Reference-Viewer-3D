"""Named camera positions the artist can jump between while sculpting."""

from __future__ import annotations

from dataclasses import dataclass, field

from .camera import Camera


@dataclass
class CameraBookmark:
    """A camera pose stored under a name."""

    name: str
    camera: dict = field(default_factory=dict)

    @classmethod
    def capture(cls, name: str, camera: Camera) -> "CameraBookmark":
        return cls(name=name, camera=camera.to_dict())

    def to_camera(self) -> Camera:
        return Camera.from_dict(self.camera)


class BookmarkStore:
    """An ordered list of :class:`CameraBookmark` with cycling support."""

    def __init__(self, items: list[CameraBookmark] | None = None) -> None:
        self._items: list[CameraBookmark] = list(items or [])
        self._current = -1

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index: int) -> CameraBookmark:
        return self._items[index]

    @property
    def items(self) -> list[CameraBookmark]:
        return self._items

    @property
    def current_index(self) -> int:
        """Index of the most recently recalled bookmark, or ``-1``."""
        return self._current if 0 <= self._current < len(self._items) else -1

    def set_current(self, index: int) -> None:
        """Mark a bookmark as the one cycling continues from."""
        self._current = index if 0 <= index < len(self._items) else -1

    def next_name(self) -> str:
        return f"View {len(self._items) + 1}"

    def add(self, name: str, camera: Camera) -> CameraBookmark:
        bookmark = CameraBookmark.capture(name or self.next_name(), camera)
        self._items.append(bookmark)
        self._current = len(self._items) - 1
        return bookmark

    def clear(self) -> None:
        self._items.clear()
        self._current = -1

    def recall(self, index: int) -> Camera | None:
        """Return the pose at ``index`` and remember it as the current one."""
        if not 0 <= index < len(self._items):
            return None
        self._current = index
        return self._items[index].to_camera()

    def cycle(self, step: int) -> tuple[int, Camera] | None:
        """Step forwards or backwards through the list, wrapping around."""
        if not self._items:
            return None
        index = (self.current_index + step) % len(self._items)
        if self.current_index < 0:
            index = 0 if step > 0 else len(self._items) - 1
        camera = self.recall(index)
        return (index, camera) if camera is not None else None
