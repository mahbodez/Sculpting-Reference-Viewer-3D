"""numba, and how the tracer's kernels are compiled.

Every kernel in :mod:`refview.trace` is compiled by numba to machine code the
first time it is called, and the result is kept on disk so the next launch
does not pay for it again.  Three things have to be settled before numba is
imported, which is why this module is the only one that imports it directly:

* where the compiled kernels are kept -- a per-user folder named after this
  version of the application, so an upgrade never loads a stale kernel;
* how a frozen, one-file build finds them again: PyInstaller unpacks the
  program into a fresh temporary folder on every launch, and numba's own
  locators key the cache on the source folder, so without help every launch
  would compile from scratch;
* which fast-math liberties the kernels may take.  numba's ``fastmath=True``
  includes *no NaNs* and *no infinities*, which lets LLVM delete the very
  ``x != x`` checks the tracer uses to drop a broken sample, so the set here
  leaves those two out.

Nothing here is required for the rest of the application: when numba cannot
be loaded, :func:`available` says so and :func:`unavailable_reason` says why,
and the Render panel shows that in place of a Render button.
"""

from __future__ import annotations

import os
import sys
from functools import partial

from .. import __version__
from ..paths import cache_dir

#: Where the compiled kernels are kept.
CACHE_DIR = cache_dir() / f"numba-{__version__}"
os.environ.setdefault("NUMBA_CACHE_DIR", str(CACHE_DIR))

try:
    import numba

    _REASON: str | None = None
except Exception as error:  # noqa: BLE001 -- any failure means the same thing here
    numba = None
    _REASON = f"numba could not be loaded ({error.__class__.__name__}: {error})"

#: The fast-math flags the kernels are compiled with: everything but the
#: promises that no value is ever NaN or infinite.
FASTMATH = {"nsz", "arcp", "contract", "afn", "reassoc"}

#: Whether compiled kernels are kept on disk.  Turned off, with a note, when
#: a frozen build's locator cannot be installed.
CACHE = True
CACHE_NOTE: str | None = None


def available() -> bool:
    """Whether the path tracer can run here."""
    return numba is not None


def unavailable_reason() -> str | None:
    """Why it cannot, in words for the Render panel, or ``None`` when it can."""
    return _REASON


def _install_frozen_locator() -> None:
    """Keep a frozen build's kernels in one place from launch to launch.

    numba's locators hash the folder a function's source is in, and a one-file
    build unpacks into a new temporary folder every time; this locator ignores
    the folder and keys the cache on the executable instead (numba already
    stamps a frozen build's entries with the executable's size and time, so a
    new build never reads an old build's kernels).  It leans on numba's
    internal caching classes, so any failure only turns the cache off.
    """
    global CACHE, CACHE_NOTE
    try:
        from numba.core import caching

        class FrozenLocator(caching._SourceFileBackedLocatorMixin, caching._CacheLocator):
            def __init__(self, py_func, py_file):
                self._py_file = py_file
                self._lineno = py_func.__code__.co_firstlineno
                package = os.path.basename(os.path.dirname(py_file)) or "trace"
                self._cache_path = os.path.join(str(CACHE_DIR), "frozen", package)

            def get_cache_path(self):
                return self._cache_path

            @classmethod
            def from_function(cls, py_func, py_file):
                if not getattr(sys, "frozen", False):
                    return None
                self = cls(py_func, py_file)
                try:
                    self.ensure_cache_path()
                except OSError:
                    return None
                return self

        # ``CacheImpl`` in current numba, ``_CacheImpl`` in older releases.
        impl = getattr(caching, "CacheImpl", None) or caching._CacheImpl
        impl._locator_classes.insert(0, FrozenLocator)
    except Exception as error:  # noqa: BLE001
        CACHE = False
        CACHE_NOTE = f"Kernels are compiled on every launch ({error})"


if numba is not None and getattr(sys, "frozen", False):
    _install_frozen_locator()


def _unavailable(*_args, **_kwargs):
    raise RuntimeError(_REASON or "numba is not available")


if numba is not None:
    #: A kernel called from Python: compiled once, kept on disk, and run with
    #: the interpreter lock released so the render threads run side by side.
    kernel = partial(numba.njit, cache=CACHE, nogil=True, fastmath=FASTMATH, error_model="numpy")
    #: A helper only other kernels call; inlined by LLVM where it pays.
    device = partial(numba.njit, cache=CACHE, nogil=True, fastmath=FASTMATH, error_model="numpy")
else:  # pragma: no cover -- exercised only where numba is missing

    def kernel(*args, **kwargs):
        if args and callable(args[0]):
            return _unavailable
        return lambda function: _unavailable

    device = kernel
