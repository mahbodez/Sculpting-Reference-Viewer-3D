"""The CPU path tracer: numpy and numba, never Qt and never OpenGL.

Importing this package is cheap; numba itself is loaded only when a module
that compiles kernels is imported, which the interface does the first time a
render is asked for rather than at start-up.
"""

from __future__ import annotations


def available() -> bool:
    """Whether the path tracer can run here (numba loads)."""
    from . import jit

    return jit.available()


def unavailable_reason() -> str | None:
    """Why the path tracer cannot run, or ``None`` when it can."""
    from . import jit

    return jit.unavailable_reason()
