"""The wake lock: it must ask once, drop once, and never take the viewer down."""

from __future__ import annotations

import sys

import pytest

from refview.wakelock import WakeLock, _platform_backend


class Recorder:
    """A backend that writes down what it was asked to do."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def hold(self) -> None:
        self.calls.append("hold")

    def release(self) -> None:
        self.calls.append("release")


class Broken(Recorder):
    """A platform that refuses, the way an old or locked-down one might."""

    def hold(self) -> None:
        super().hold()
        raise OSError("no power management here")

    def release(self) -> None:
        super().release()
        raise OSError("no power management here")


def test_repeated_activations_ask_the_platform_once():
    backend = Recorder()
    lock = WakeLock(backend)

    for _ in range(3):
        lock.set_held(True)
    assert lock.held is True
    assert backend.calls == ["hold"]

    for _ in range(3):
        lock.set_held(False)
    assert lock.held is False
    assert backend.calls == ["hold", "release"]


def test_the_lock_starts_free_and_releasing_it_early_is_harmless():
    backend = Recorder()
    lock = WakeLock(backend)
    assert lock.held is False
    lock.release()
    assert backend.calls == []


def test_a_window_that_comes_and_goes_holds_and_drops_each_time():
    backend = Recorder()
    lock = WakeLock(backend)
    for active in (True, False, True, False):
        lock.set_held(active)
    assert backend.calls == ["hold", "release", "hold", "release"]


def test_a_platform_that_refuses_leaves_the_lock_free():
    """The viewer must open and close normally on a machine that says no."""
    backend = Broken()
    lock = WakeLock(backend)

    lock.set_held(True)
    assert lock.held is False, "a failed request must not be remembered as held"
    assert backend.calls == ["hold"]

    # Still willing to try again, rather than wedged.
    lock.set_held(True)
    assert backend.calls == ["hold", "hold"]


def test_this_machine_gets_a_backend_of_its_own():
    backend = _platform_backend()
    # Whatever it is, holding and dropping it must not raise.
    lock = WakeLock(backend)
    lock.set_held(True)
    lock.release()
    assert lock.held is False


@pytest.mark.skipif(sys.platform != "win32", reason="Windows power API")
def test_windows_really_sets_the_execution_state():
    """The flag the viewer sets is the one Windows reports back afterwards."""
    import ctypes

    from refview.wakelock import _WindowsBackend

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.SetThreadExecutionState.argtypes = [ctypes.c_uint32]
    kernel32.SetThreadExecutionState.restype = ctypes.c_uint32

    backend = _WindowsBackend()
    backend.hold()
    # Setting the state returns the state that was in force before it.
    previous = kernel32.SetThreadExecutionState(_WindowsBackend._CONTINUOUS)
    expected = (
        _WindowsBackend._CONTINUOUS
        | _WindowsBackend._SYSTEM_REQUIRED
        | _WindowsBackend._DISPLAY_REQUIRED
    )
    assert previous == expected

    backend.release()
    previous = kernel32.SetThreadExecutionState(_WindowsBackend._CONTINUOUS)
    assert previous == _WindowsBackend._CONTINUOUS
