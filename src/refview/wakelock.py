"""Keeping the machine awake while the viewer is the window in front.

An artist works from this view with both hands in clay: minutes go by with no
key pressed and no mouse moved, which is exactly when the screen dims and the
pose on it goes away.  While the window is active the platform is asked to
hold sleep off; the moment it is not, the request is dropped, so a viewer left
open behind other windows costs a laptop nothing.

None of this is load-bearing.  Every platform hook is allowed to fail -- an
old Windows build, a Mac framework that will not load, a Linux session with no
screensaver service -- and a machine that refuses simply sleeps the way it
always did.
"""

from __future__ import annotations

import ctypes
import sys

from . import APP_NAME


class _Backend:
    """A way of asking one platform to stay awake."""

    def hold(self) -> None:
        """Ask for sleep to be held off."""

    def release(self) -> None:
        """Withdraw the request."""


class _WindowsBackend(_Backend):
    """``SetThreadExecutionState``: a flag on this thread, not a handle.

    The flags stay in force until they are set again, so releasing means
    setting the bare continuous flag rather than undoing a handle.  Both calls
    have to come from the same thread, which is the UI thread either way.
    """

    _CONTINUOUS = 0x80000000
    _SYSTEM_REQUIRED = 0x00000001
    _DISPLAY_REQUIRED = 0x00000002

    def __init__(self) -> None:
        self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self._kernel32.SetThreadExecutionState.argtypes = [ctypes.c_uint32]
        self._kernel32.SetThreadExecutionState.restype = ctypes.c_uint32

    def hold(self) -> None:
        self._kernel32.SetThreadExecutionState(
            self._CONTINUOUS | self._SYSTEM_REQUIRED | self._DISPLAY_REQUIRED
        )

    def release(self) -> None:
        self._kernel32.SetThreadExecutionState(self._CONTINUOUS)


class _MacBackend(_Backend):
    """An IOKit power assertion, held by id until it is released."""

    #: Keeps the display awake, and with it the machine.
    _ASSERTION_TYPE = b"PreventUserIdleDisplaySleep"
    _LEVEL_ON = 255
    _UTF8 = 0x08000100

    def __init__(self) -> None:
        self._iokit = ctypes.cdll.LoadLibrary(
            "/System/Library/Frameworks/IOKit.framework/IOKit"
        )
        self._core = ctypes.cdll.LoadLibrary(
            "/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation"
        )
        self._core.CFStringCreateWithCString.argtypes = [
            ctypes.c_void_p,
            ctypes.c_char_p,
            ctypes.c_uint32,
        ]
        self._core.CFStringCreateWithCString.restype = ctypes.c_void_p
        self._core.CFRelease.argtypes = [ctypes.c_void_p]
        self._iokit.IOPMAssertionCreateWithName.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_uint32),
        ]
        self._iokit.IOPMAssertionCreateWithName.restype = ctypes.c_int
        self._iokit.IOPMAssertionRelease.argtypes = [ctypes.c_uint32]
        self._iokit.IOPMAssertionRelease.restype = ctypes.c_int
        self._assertion: int | None = None

    def _string(self, text: bytes) -> ctypes.c_void_p:
        return ctypes.c_void_p(self._core.CFStringCreateWithCString(None, text, self._UTF8))

    def hold(self) -> None:
        if self._assertion is not None:
            return
        kind = self._string(self._ASSERTION_TYPE)
        name = self._string(APP_NAME.encode("utf-8"))
        assertion = ctypes.c_uint32(0)
        try:
            status = self._iokit.IOPMAssertionCreateWithName(
                kind, self._LEVEL_ON, name, ctypes.byref(assertion)
            )
        finally:
            self._core.CFRelease(kind)
            self._core.CFRelease(name)
        if status == 0:  # kIOReturnSuccess
            self._assertion = assertion.value

    def release(self) -> None:
        if self._assertion is None:
            return
        self._iokit.IOPMAssertionRelease(ctypes.c_uint32(self._assertion))
        self._assertion = None


class _ScreenSaverBackend(_Backend):
    """The freedesktop screensaver service, which hands back a cookie."""

    _SERVICE = "org.freedesktop.ScreenSaver"
    _PATH = "/org/freedesktop/ScreenSaver"

    def __init__(self) -> None:
        from PySide6.QtDBus import QDBusConnection, QDBusInterface

        self._interface = QDBusInterface(
            self._SERVICE, self._PATH, self._SERVICE, QDBusConnection.sessionBus()
        )
        if not self._interface.isValid():
            raise RuntimeError("no screensaver service on the session bus")
        self._cookie: int | None = None

    def hold(self) -> None:
        if self._cookie is not None:
            return
        reply = self._interface.call("Inhibit", APP_NAME, "Showing a reference to work from")
        arguments = reply.arguments()
        if arguments:
            self._cookie = int(arguments[0])

    def release(self) -> None:
        if self._cookie is None:
            return
        self._interface.call("UnInhibit", self._cookie)
        self._cookie = None


def _platform_backend() -> _Backend:
    """The backend for this machine, or a do-nothing one if it cannot be had."""
    candidates = {
        "win32": _WindowsBackend,
        "darwin": _MacBackend,
    }
    backend = candidates.get(sys.platform)
    if backend is None and sys.platform.startswith("linux"):
        backend = _ScreenSaverBackend
    if backend is None:
        return _Backend()
    try:
        return backend()
    except Exception:
        # A viewer has to open on a machine that refuses; it just sleeps as before.
        return _Backend()


class WakeLock:
    """Holds sleep off while the window that owns it is the one in front.

    The class keeps track of whether the request is out, so that the window can
    call :meth:`set_held` on every activation change without the platform
    seeing a stream of repeats.
    """

    def __init__(self, backend: _Backend | None = None) -> None:
        self._backend = _platform_backend() if backend is None else backend
        self._held = False

    @property
    def held(self) -> bool:
        return self._held

    def set_held(self, held: bool) -> None:
        """Hold sleep off, or stop holding it, whichever is not already true."""
        if held == self._held:
            return
        try:
            self._backend.hold() if held else self._backend.release()
        except Exception:
            # A power API is never worth taking the window down over.
            return
        self._held = held

    def release(self) -> None:
        """Drop the request, if one is out.  Safe to call more than once."""
        self.set_held(False)
