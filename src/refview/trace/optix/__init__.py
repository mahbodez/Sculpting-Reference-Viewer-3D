"""NVIDIA OptiX, reached through the display driver: for now, its AI denoiser.

Nothing here is bundled: the driver carries OptiX and CUDA, and this package
only declares, with ctypes, the parts of their interfaces it calls.  Where
there is no NVIDIA driver, :class:`OptixError` says so and the Render
panel offers the other denoisers.
"""

from .loader import OptixError

__all__ = ["OptixError"]
