"""The CUDA driver, as much of it as moving a picture to the GPU and back needs.

Only the driver's own library (``nvcuda.dll``, ``libcuda.so.1``) is used --
no toolkit, no runtime -- so this works on any machine with an NVIDIA driver.
The primary context of device zero is borrowed, as every CUDA application on
the machine can share it, and made current around each call.
"""

from __future__ import annotations

import contextlib
import ctypes
import sys

CUDA_SUCCESS = 0


class CudaError(RuntimeError):
    pass


class Cuda:
    """The driver, and the primary context of one device."""

    def __init__(self, ordinal: int = 0) -> None:
        name = "nvcuda.dll" if sys.platform == "win32" else "libcuda.so.1"
        try:
            loader = ctypes.WinDLL if sys.platform == "win32" else ctypes.CDLL
            self._lib = loader(name)
        except OSError as error:
            raise CudaError(f"The NVIDIA driver's CUDA library is not here ({error})") from error
        lib = self._lib
        self._check(lib.cuInit(0), "cuInit")
        device = ctypes.c_int()
        self._check(lib.cuDeviceGet(ctypes.byref(device), ordinal), "cuDeviceGet")
        self.device = device.value
        raw = ctypes.create_string_buffer(256)
        self._check(lib.cuDeviceGetName(raw, 256, self.device), "cuDeviceGetName")
        self.name = raw.value.decode(errors="replace")
        context = ctypes.c_void_p()
        self._check(lib.cuDevicePrimaryCtxRetain(ctypes.byref(context), self.device),
                    "cuDevicePrimaryCtxRetain")
        self.context = context
        lib.cuMemAlloc_v2.argtypes = [ctypes.POINTER(ctypes.c_uint64), ctypes.c_size_t]
        lib.cuMemFree_v2.argtypes = [ctypes.c_uint64]
        lib.cuMemcpyHtoD_v2.argtypes = [ctypes.c_uint64, ctypes.c_void_p, ctypes.c_size_t]
        lib.cuMemcpyDtoH_v2.argtypes = [ctypes.c_void_p, ctypes.c_uint64, ctypes.c_size_t]
        lib.cuCtxPushCurrent_v2.argtypes = [ctypes.c_void_p]
        lib.cuCtxPopCurrent_v2.argtypes = [ctypes.POINTER(ctypes.c_void_p)]

    def _check(self, result: int, what: str) -> None:
        if result != CUDA_SUCCESS:
            text = ctypes.c_char_p()
            try:
                self._lib.cuGetErrorString(result, ctypes.byref(text))
                message = text.value.decode(errors="replace") if text.value else str(result)
            except Exception:  # noqa: BLE001
                message = str(result)
            raise CudaError(f"{what} failed: {message}")

    def push(self) -> None:
        self._check(self._lib.cuCtxPushCurrent_v2(self.context), "cuCtxPushCurrent")

    def pop(self) -> None:
        popped = ctypes.c_void_p()
        self._lib.cuCtxPopCurrent_v2(ctypes.byref(popped))

    def alloc(self, size: int) -> int:
        pointer = ctypes.c_uint64()
        self._check(self._lib.cuMemAlloc_v2(ctypes.byref(pointer), max(int(size), 1)),
                    "cuMemAlloc")
        return pointer.value

    def free(self, pointer: int) -> None:
        if pointer:
            self._lib.cuMemFree_v2(pointer)

    def upload(self, pointer: int, array) -> None:
        self._check(self._lib.cuMemcpyHtoD_v2(pointer, array.ctypes.data, array.nbytes),
                    "cuMemcpyHtoD")

    def download(self, array, pointer: int) -> None:
        self._check(self._lib.cuMemcpyDtoH_v2(array.ctypes.data, pointer, array.nbytes),
                    "cuMemcpyDtoH")

    def synchronize(self) -> None:
        self._check(self._lib.cuCtxSynchronize(), "cuCtxSynchronize")

    def release(self) -> None:
        with contextlib.suppress(Exception):
            self._lib.cuDevicePrimaryCtxRelease_v2(self.device)
