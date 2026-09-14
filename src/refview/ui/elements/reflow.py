"""A layout that turns a column of groups into columns when given the width.

A panel docked down the side of the window is a tall narrow strip and wants
its groups stacked; the same panel docked along the bottom is a short wide
strip and wants them side by side.  Rather than have a panel ask where it is
and rebuild itself, the layout reads the only thing that actually matters --
how much width it has been given -- and fills as many columns as will fit.
Nothing about a panel changes when it is moved; it is simply laid out again.

Groups are not all the same height, so a group is dropped into whichever
column is currently shortest.  Filling left to right instead would leave the
last column short by however much the tallest group in the row overhangs,
which on a panel of mixed groups is most of a column of wasted space.
"""

from __future__ import annotations

from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtWidgets import QLayout, QLayoutItem, QSizePolicy, QWidget

#: The width a column wants, in pixels.  Wide enough for a caption, a slider
#: worth dragging and its number; narrow enough that a panel dragged along the
#: bottom of a 1440-wide window breaks into four or five columns rather than
#: two.  A layout given less than this still lays out -- in one column, which
#: is then narrower than it would like, which is what scrolling is for.
COLUMN_WIDTH = 260


class ReflowLayout(QLayout):
    """Lays its items out in as many equal columns as the width allows."""

    def __init__(
        self,
        parent: QWidget | None = None,
        column_width: int = COLUMN_WIDTH,
        spacing: int = 6,
        margin: int = 6,
    ) -> None:
        super().__init__(parent)
        self._items: list[QLayoutItem] = []
        self._column_width = max(int(column_width), 1)
        self.setSpacing(spacing)
        self.setContentsMargins(margin, margin, margin, margin)

    # -- the four methods QLayout requires --------------------------------

    def addItem(self, item: QLayoutItem) -> None:  # noqa: N802 - Qt contract
        self._items.append(item)

    def count(self) -> int:
        return len(self._items)

    def itemAt(self, index: int) -> QLayoutItem | None:  # noqa: N802 - Qt contract
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index: int) -> QLayoutItem | None:  # noqa: N802 - Qt contract
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

    # -- inserting, for the panels that are rearranged by hand -------------

    def insert_widget(self, index: int, widget: QWidget) -> None:
        """Add a widget at a position, rather than only at the end."""
        self.addWidget(widget)
        if 0 <= index < len(self._items) - 1:
            self._items.insert(index, self._items.pop())
        self.invalidate()

    def index_of(self, widget: QWidget) -> int:
        for index, item in enumerate(self._items):
            if item.widget() is widget:
                return index
        return -1

    # -- what the layout is worth ------------------------------------------

    def expandingDirections(self) -> Qt.Orientations:  # noqa: N802 - Qt contract
        return Qt.Orientations(0)

    def hasHeightForWidth(self) -> bool:  # noqa: N802 - Qt contract
        return True

    def heightForWidth(self, width: int) -> int:  # noqa: N802 - Qt contract
        return self._arrange(QRect(0, 0, width, 0), place=False)

    def setGeometry(self, rect: QRect) -> None:  # noqa: N802 - Qt contract
        super().setGeometry(rect)
        self._arrange(rect, place=True)

    def minimumSize(self) -> QSize:  # noqa: N802 - Qt contract
        margins = self.contentsMargins()
        width = max(
            (item.minimumSize().width() for item in self._items if not item.isEmpty()),
            default=0,
        )
        return QSize(
            width + margins.left() + margins.right(),
            margins.top() + margins.bottom(),
        )

    def sizeHint(self) -> QSize:  # noqa: N802 - Qt contract
        margins = self.contentsMargins()
        width = self._column_width + margins.left() + margins.right()
        return QSize(width, self.heightForWidth(width))

    # -- placing -----------------------------------------------------------

    def column_width(self) -> int:
        return self._column_width

    def set_column_width(self, width: int) -> None:
        self._column_width = max(int(width), 1)
        self.invalidate()

    def columns_at(self, width: int) -> int:
        """How many columns this layout would break into at ``width``."""
        margins = self.contentsMargins()
        inner = width - margins.left() - margins.right()
        live = len([item for item in self._items if not item.isEmpty()])
        return self._columns(inner, live)

    def column_of(self, widget: QWidget) -> int:
        """Which column a widget currently sits in, or -1 if it is not laid out."""
        geometry = self.geometry()
        columns = self.columns_at(geometry.width())
        if columns <= 1 or not widget.isVisible():
            return 0 if self.index_of(widget) >= 0 else -1
        margins = self.contentsMargins()
        left = geometry.left() + margins.left()
        span = max(
            (geometry.width() - margins.left() - margins.right()) // columns, 1
        )
        return max(0, min(columns - 1, (widget.geometry().left() - left) // span))

    def _columns(self, inner_width: int, items: int) -> int:
        if items <= 0:
            return 1
        spacing = self.spacing()
        fit = (inner_width + spacing) // (self._column_width + spacing)
        return max(1, min(int(fit), items))

    def _arrange(self, rect: QRect, place: bool) -> int:
        margins = self.contentsMargins()
        area = rect.adjusted(
            margins.left(), margins.top(), -margins.right(), -margins.bottom()
        )
        spacing = self.spacing()
        items = [item for item in self._items if not item.isEmpty()]
        if not items:
            return margins.top() + margins.bottom()

        columns = self._columns(area.width(), len(items))
        width = max((area.width() - spacing * (columns - 1)) // columns, 1)

        #: Which column each item went into, and how tall it wants to be.
        packed: list[list[tuple[QLayoutItem, int]]] = [[] for _ in range(columns)]
        filled = [0] * columns
        for item in items:
            # Taking the minimum over the pairs keeps the leftmost of equally
            # short columns, so a panel whose groups all match lays out in
            # reading order rather than in whatever order the heights tie.
            column = min(range(columns), key=lambda index: (filled[index], index))
            height = _height_of(item, width)
            if packed[column]:
                filled[column] += spacing
            packed[column].append((item, height))
            filled[column] += height

        natural = max(filled) + margins.top() + margins.bottom()
        if place:
            self._place(area, packed, filled, width, spacing)
        return natural

    def _place(
        self,
        area: QRect,
        packed: list[list[tuple[QLayoutItem, int]]],
        filled: list[int],
        width: int,
        spacing: int,
    ) -> None:
        """Put the items where the packing said, sharing out any room left.

        A panel is usually shorter than the dock holding it, and the room left
        over goes to whatever in it asked to grow -- the armature's tree, the
        matcap gallery, the list of saved views.  Those are the controls whose
        usefulness is how much of them you can see at once, and a layout that
        left them at their natural height would be one where making the dock
        taller did nothing at all.  Nothing grows unless it said it wanted to,
        so a column of plain groups still sits at the top.
        """
        for column, rows in enumerate(packed):
            greedy = [item for item, _ in rows if _wants_height(item)]
            slack = max(area.height() - filled[column], 0)
            share = slack // len(greedy) if greedy else 0
            extra = slack - share * len(greedy) if greedy else 0
            top = area.top()
            left = area.left() + column * (width + spacing)
            for index, (item, height) in enumerate(rows):
                if index:
                    top += spacing
                if item in greedy:
                    height += share
                    if item is greedy[-1]:
                        height += extra
                item.setGeometry(QRect(left, top, width, height))
                top += height


def _wants_height(item: QLayoutItem) -> bool:
    """Whether an item asked to be given more height than it needs."""
    widget = item.widget()
    if widget is None:
        return bool(item.expandingDirections() & Qt.Orientation.Vertical)
    return bool(
        widget.sizePolicy().expandingDirections() & Qt.Orientation.Vertical
    )


def _height_of(item: QLayoutItem, width: int) -> int:
    """How tall an item needs to be once it has been given ``width``."""
    widget = item.widget()
    if widget is not None and widget.hasHeightForWidth():
        return max(widget.heightForWidth(width), widget.minimumSizeHint().height())
    if item.hasHeightForWidth():
        return max(item.heightForWidth(width), item.minimumSize().height())
    return max(item.sizeHint().height(), item.minimumSize().height())


class Reflow(QWidget):
    """A widget laid out by :class:`ReflowLayout`, sized to fit its columns.

    A scroll area asks the widget inside it how tall it is, and asks before it
    has settled how wide to make it -- so a height that depends on the width,
    as this one's does, has to be pushed back in once the width is known.  That
    is what the resize does, and why the height is only written when it has
    actually changed: writing it unconditionally is a resize that causes a
    resize.
    """

    def __init__(
        self,
        parent: QWidget | None = None,
        column_width: int = COLUMN_WIDTH,
        spacing: int = 6,
        margin: int = 6,
    ) -> None:
        super().__init__(parent)
        self._reflow = ReflowLayout(self, column_width, spacing, margin)
        policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)

    def reflow(self) -> ReflowLayout:
        return self._reflow

    def add(self, widget: QWidget) -> QWidget:
        self._reflow.addWidget(widget)
        self._settle()
        return widget

    def insert(self, index: int, widget: QWidget) -> QWidget:
        self._reflow.insert_widget(index, widget)
        self._settle()
        return widget

    def columns(self) -> int:
        """How many columns the widget is currently broken into."""
        return self._reflow.columns_at(self.width())

    def hasHeightForWidth(self) -> bool:  # noqa: N802 - Qt contract
        return True

    def heightForWidth(self, width: int) -> int:  # noqa: N802 - Qt contract
        return self._reflow.heightForWidth(width)

    def resizeEvent(self, event) -> None:  # noqa: N802 - Qt contract
        super().resizeEvent(event)
        self._settle()

    def _settle(self) -> None:
        wanted = self._reflow.heightForWidth(max(self.width(), 1))
        if wanted != self.minimumHeight():
            self.setMinimumHeight(wanted)
