"""Undo/redo and the commands the UI builds on."""

from __future__ import annotations

from refview.core.annotation import AnnotationStore, Stroke
from refview.core.commands import AddItem, RemoveItem, ReplaceItems, SetAttributes
from refview.core.history import MEASUREMENTS, History
from refview.core.measurement import Measurement, MeasurementStore


def measurement(name: str = "A") -> Measurement:
    return Measurement(start=(0.0, 0.0, 0.0), end=(1.0, 0.0, 0.0), name=name)


def test_new_measurements_start_locked():
    assert measurement().locked is True


def test_push_applies_then_undo_reverts():
    store = MeasurementStore()
    history = History()
    history.push(AddItem(store.items, measurement(), text="Add A", channel=MEASUREMENTS))
    assert len(store) == 1
    assert history.can_undo and not history.can_redo
    assert history.undo_text == "Add A"

    history.undo()
    assert len(store) == 0
    assert history.can_redo

    history.redo()
    assert len(store) == 1


def test_a_gesture_can_record_a_change_it_already_made():
    """Dragging an endpoint edits the measurement live and commits on release."""
    item = measurement()
    before = item.start
    item.start = (5.0, 0.0, 0.0)

    history = History()
    history.push(
        SetAttributes(
            item, {"start": item.start}, channel=MEASUREMENTS, previous={"start": before}
        ),
        apply=False,
    )
    assert item.start == (5.0, 0.0, 0.0)
    history.undo()
    assert item.start == before


def test_set_attributes_restores_every_field():
    item = measurement()
    history = History()
    history.push(SetAttributes(item, {"name": "Jaw", "locked": False}, channel=MEASUREMENTS))
    assert (item.name, item.locked) == ("Jaw", False)
    history.undo()
    assert (item.name, item.locked) == ("A", True)


def test_remove_puts_the_item_back_where_it_was():
    store = MeasurementStore([measurement("A"), measurement("B"), measurement("C")])
    history = History()
    history.push(RemoveItem(store.items, 1, channel=MEASUREMENTS))
    assert [item.name for item in store] == ["A", "C"]
    history.undo()
    assert [item.name for item in store] == ["A", "B", "C"]


def test_replace_items_covers_bulk_edits():
    store = AnnotationStore([Stroke(points=[(0.0, 0.0, 0.0), (1.0, 0.0, 0.0)])])
    history = History()
    history.push(ReplaceItems(store.items, []))
    assert len(store) == 0
    history.undo()
    assert len(store) == 1


def test_a_new_edit_discards_the_redo_branch():
    store = MeasurementStore()
    history = History()
    history.push(AddItem(store.items, measurement("A")))
    history.undo()
    assert history.can_redo

    history.push(AddItem(store.items, measurement("B")))
    assert not history.can_redo
    assert [item.name for item in store] == ["B"]


def test_the_stack_is_bounded():
    store = MeasurementStore()
    history = History(limit=3)
    for index in range(6):
        history.push(AddItem(store.items, measurement(str(index))))
    for _ in range(3):
        assert history.undo() is not None
    assert history.undo() is None
    # The three edits that fell off the end stay applied.
    assert len(store) == 3


def test_undo_and_redo_on_an_empty_stack_are_safe():
    history = History()
    assert history.undo() is None
    assert history.redo() is None
    assert history.undo_text == ""


def test_commands_carry_their_channel_and_name():
    command = AddItem([], measurement(), text="Add A", channel=MEASUREMENTS)
    assert command.channel == MEASUREMENTS
    assert command.text == "Add A"
    assert "Add A" in repr(command)
