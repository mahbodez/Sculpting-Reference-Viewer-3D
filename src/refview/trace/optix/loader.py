"""Finding OptiX in the NVIDIA driver and asking it for its function table.

On Windows ``nvoptix.dll`` is not on any search path: it sits in the
driver's folder in the driver store, beside the OpenGL driver the display
adapter's registry key names.  This follows NVIDIA's own ``optix_stubs.h``:
the system folder first, then the folder of each display adapter's OpenGL
driver, and -- a last resort of ours -- any NVIDIA driver folder in the store.
"""

from __future__ import annotations

import ctypes
import glob
import os
import sys

from . import abi

_CLASS_KEY = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"


class OptixError(RuntimeError):
    """OptiX cannot be used here; the message says why, for the Render panel."""


def _windows_candidates() -> list[str]:
    system = os.path.join(os.environ.get("SYSTEMROOT", r"C:\Windows"), "System32")
    found = [os.path.join(system, "nvoptix.dll")]
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, _CLASS_KEY) as root:
            index = 0
            while True:
                try:
                    name = winreg.EnumKey(root, index)
                except OSError:
                    break
                index += 1
                try:
                    with winreg.OpenKey(root, name) as key:
                        value, _kind = winreg.QueryValueEx(key, "OpenGLDriverName")
                except OSError:
                    continue
                for entry in value if isinstance(value, list) else [value]:
                    folder = os.path.dirname(str(entry))
                    if folder:
                        found.append(os.path.join(folder, "nvoptix.dll"))
    except Exception:  # noqa: BLE001 -- the registry is a hint, not a requirement
        pass
    store = os.path.join(system, "DriverStore", "FileRepository")
    found.extend(sorted(glob.glob(os.path.join(store, "nv*", "nvoptix.dll"))))
    return found


def load_library():
    """The OptiX library, loaded, or :class:`OptixError`."""
    if sys.platform == "win32":
        errors = []
        for path in _windows_candidates():
            if not os.path.isfile(path):
                continue
            try:
                return ctypes.WinDLL(path)
            except OSError as error:
                errors.append(str(error))
        raise OptixError("No NVIDIA driver with OptiX was found"
                               + (f" ({errors[0]})" if errors else ""))
    if sys.platform.startswith("linux"):
        try:
            return ctypes.CDLL("libnvoptix.so.1")
        except OSError as error:
            raise OptixError(f"No NVIDIA driver with OptiX was found ({error})") from error
    raise OptixError("OptiX needs an NVIDIA GPU on Windows or Linux")


class Optix:
    """The function table, with the denoiser's functions ready to call."""

    def __init__(self) -> None:
        library = load_library()
        try:
            query = library.optixQueryFunctionTable
        except AttributeError as error:
            raise OptixError("The driver's OptiX has no function table") from error
        query.restype = abi.QUERY_FUNCTION_TABLE[0]
        query.argtypes = list(abi.QUERY_FUNCTION_TABLE[1:])
        table = abi.FunctionTable()
        result = query(abi.ABI_VERSION, 0, None, None, ctypes.byref(table),
                       ctypes.sizeof(table))
        if result != abi.OPTIX_SUCCESS:
            raise OptixError(
                f"The driver's OptiX does not offer interface {abi.ABI_VERSION} (error {result})")
        self._library = library
        self._table = table
        for name, prototype in abi.SIGNATURES.items():
            address = getattr(table, name)
            if not address:
                raise OptixError(f"The driver's OptiX has no {name}")
            setattr(self, name, prototype(address))

    def error_text(self, result: int) -> str:
        try:
            name = self.optixGetErrorName(result)
            text = self.optixGetErrorString(result)
            return f"{name.decode()}: {text.decode()}" if name and text else str(result)
        except Exception:  # noqa: BLE001
            return str(result)

    def check(self, result: int, what: str) -> None:
        if result != abi.OPTIX_SUCCESS:
            raise OptixError(f"{what} failed ({self.error_text(result)})")
