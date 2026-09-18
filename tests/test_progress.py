"""What a long task says about itself, and how it is stopped."""

from __future__ import annotations

import pytest

from refview.core.progress import CancelledError, Progress, silent


def test_a_report_moves_the_bar_and_keeps_what_was_not_said() -> None:
    seen: list[tuple] = []
    progress = Progress("work", lambda p: seen.append((p.done, p.total, p.message)))
    assert progress.fraction is None and not progress.determinate
    progress.report(0, 4, "starting")
    progress.report(2)
    progress.report(message="half way")
    assert seen == [(0, 4, "starting"), (2, 4, "starting"), (2, 4, "half way")]
    assert progress.fraction == 0.5 and progress.determinate


def test_the_fraction_is_clamped_and_busy_without_a_total() -> None:
    progress = silent()
    progress.report(3, 0)
    assert progress.fraction is None
    progress.report(9, 4)
    assert progress.fraction == 1.0
    progress.report(-1, 4)
    assert progress.fraction == 0.0


def test_cancelling_stops_the_work_at_its_next_report() -> None:
    progress = Progress("work")
    progress.report(1, 2)
    progress.cancel()
    assert progress.cancelled
    with pytest.raises(CancelledError):
        progress.report(2, 2)
    with pytest.raises(CancelledError):
        progress.check()


def test_a_slice_maps_its_own_count_onto_part_of_the_whole() -> None:
    whole = Progress("work")
    first = whole.slice(0.0, 0.5, total=10)
    first.report(5, message="reading")
    assert whole.fraction == pytest.approx(0.25) and whole.message == "reading"
    second = whole.slice(0.5, 1.0)
    second.report(0, 4)
    assert whole.fraction == pytest.approx(0.5)
    second.report(4)
    assert whole.fraction == pytest.approx(1.0)
    # A stage that cannot count parks the bar at its start.
    third = whole.slice(0.2, 0.6, total=0)
    third.report(message="thinking")
    assert whole.fraction == pytest.approx(0.2)


def test_cancelling_the_whole_cancels_every_slice() -> None:
    whole = Progress("work")
    part = whole.slice(0.0, 1.0, total=3)
    whole.cancel()
    assert part.cancelled
    with pytest.raises(CancelledError):
        part.report(1)
