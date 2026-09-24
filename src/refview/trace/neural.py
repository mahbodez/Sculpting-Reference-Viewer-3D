"""NVIDIA DLSS 5 Neural Rendering on a finished picture, through Merserk's Neuroframe Engine.

DLSS 5 Neural Rendering is an AI model that relights and re-materials a
rendered frame: it gives skin, cloth and stone the lighting response a
photograph has.  NVIDIA offers it to games through its own SDK; the
**Neuroframe Engine** from Merserk's *Visual Enhancer* is what lets it run on
a single still picture.
The engine is not part of this repository.  It is three DLLs --

* ``neuroframe_engine_neural_rendering.dll``, the engine (Merserk),
* ``neuroframe_caller.dll``, its loader shim (Merserk),
* ``nvngx_dlssnr.dll``, NVIDIA's Neural Rendering runtime,

-- found either in the folder the Preferences name (a Visual Enhancer install
or the ``dlssnr`` folder inside one) or bundled with the application in
``resources/dlssnr``.  They need an NVIDIA GeForce RTX 50 series GPU and a
current driver.

What goes in is a *display* picture -- light already developed through the
view transform, exposure and gamma, as the Render window shows it -- in
sRGB values between nought and one, which is what the engine was trained on.
What comes back is the same, relit; the alpha is left as it was.

The engine keeps NVIDIA's NGX runtime loaded for the life of the process:
its author found that shutting NGX down or unloading it can wedge the
driver, so neither is ever done here.  Every native call runs under a
watchdog, and one that hangs or faults marks the engine unusable until the
application restarts rather than risking a second call into broken state.
"""

from __future__ import annotations

import contextlib
import ctypes
import os
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..core.path_trace import NeuralSettings

#: The interface version of the engine's frame calls this module speaks.
BRIDGE_ABI_VERSION = 6
BRIDGE_NAME = "neuroframe_engine_neural_rendering.dll"
SHIM_NAME = "neuroframe_caller.dll"
RUNTIME_NAME = "nvngx_dlssnr.dll"
REQUIRED_FILES = (BRIDGE_NAME, SHIM_NAME, RUNTIME_NAME)

#: The sizes the engine accepts: at least 64 pixels a side, at most 8K.
MIN_SIDE = 64
MAX_LONG_SIDE = 7680
MAX_SHORT_SIDE = 4320

#: How long one pass may take before the engine is taken to have hung.
WATCHDOG_SECONDS = 45.0

_MEMORY_NONE = 2

#: A folder of the artist's to find the engine in; see :func:`set_engine_dir`.
_engine_override: Path | None = None


def set_engine_dir(folder: str | Path | None) -> None:
    """Look for the engine in ``folder`` (from the preferences), or only where it ships."""
    global _engine_override
    if folder is None or not str(folder).strip():
        _engine_override = None
        return
    _engine_override = Path(folder).expanduser()


def _complete(folder: Path) -> bool:
    return all((folder / name).is_file() for name in REQUIRED_FILES)


def engine_dir() -> Path | None:
    """The folder holding all three engine files, or ``None`` when there is none.

    The artist's folder may be a Visual Enhancer install, its ``bin`` or
    ``runtime`` folder, or the ``dlssnr`` folder itself: all are looked in.
    """
    from ..paths import resources_dir

    candidates = []
    if _engine_override is not None:
        root = _engine_override
        candidates += [root, root / "dlssnr", root / "runtime" / "dlssnr",
                       root / "bin" / "runtime" / "dlssnr"]
    candidates.append(resources_dir() / "dlssnr")
    for folder in candidates:
        if _complete(folder):
            return folder
    return None


def missing_reason() -> str:
    """Why no engine was found, in words that say what to do."""
    if _engine_override is not None:
        return (f"the engine was not found in {_engine_override}; it needs "
                f"{', '.join(REQUIRED_FILES)}")
    return "no engine found; set the Visual Enhancer folder in Preferences > Folders"


def check_size(width: int, height: int) -> None:
    """Raise if the engine cannot take a ``width`` by ``height`` picture."""
    if min(width, height) < MIN_SIDE:
        raise NeuralError(f"{width} x {height} is below the {MIN_SIDE} x {MIN_SIDE} "
                          "Neural Rendering needs")
    if max(width, height) > MAX_LONG_SIDE or min(width, height) > MAX_SHORT_SIDE:
        raise NeuralError(f"{width} x {height} is larger than the {MAX_LONG_SIDE} x "
                          f"{MAX_SHORT_SIDE} Neural Rendering takes")


class NeuralError(RuntimeError):
    """Neural Rendering could not be done, and says why."""


class NeuralPoisonedError(NeuralError):
    """The engine hung or faulted; it is not called again until the application restarts."""


class RenderParameters(ctypes.Structure):
    """The engine's controls for one frame, as its ABI version 6 lays them out.

    Each version only appended to the one before, so the order is the
    engine's history: version 3's controls and mask, version 4's face and
    grain, version 5's passes, version 6's temporal controls.
    """

    _fields_ = [
        ("struct_size", ctypes.c_uint32),
        ("abi_version", ctypes.c_uint32),
        ("style", ctypes.c_int32),
        ("intensity", ctypes.c_float),
        ("tone", ctypes.c_float),
        ("structure", ctypes.c_float),
        ("skin", ctypes.c_float),
        ("automask", ctypes.c_int32),
        ("reset", ctypes.c_int32),
        ("color_strength", ctypes.c_float),
        ("tone_preservation", ctypes.c_float),
        ("mask_memory_type", ctypes.c_uint32),
        ("mask_width", ctypes.c_uint32),
        ("mask_height", ctypes.c_uint32),
        ("mask_stride", ctypes.c_uint32),
        ("mask_plane", ctypes.c_uint64),
        ("face_skin_protection", ctypes.c_float),
        ("grain_preservation", ctypes.c_float),
        ("nr_passes", ctypes.c_int32),
        ("shimmer_suppression", ctypes.c_float),
        ("prefer_nvof", ctypes.c_int32),
    ]


def render_parameters(settings: NeuralSettings) -> RenderParameters:
    """The engine's controls for a still picture with ``settings``.

    A still has no frame before it, so every evaluation starts the engine's
    history afresh (``reset``) and the temporal controls are off.
    """
    value = RenderParameters()
    value.struct_size = ctypes.sizeof(RenderParameters)
    value.abi_version = BRIDGE_ABI_VERSION
    value.style = settings.style.code
    value.intensity = float(settings.intensity)
    value.tone = float(settings.local_tone)
    value.structure = float(settings.local_structure)
    value.skin = float(settings.skin_structure)
    value.automask = int(bool(settings.auto_mask))
    value.reset = 1
    value.color_strength = float(settings.color_strength)
    value.tone_preservation = float(settings.tone_preservation)
    value.mask_memory_type = _MEMORY_NONE
    value.face_skin_protection = float(settings.face_skin_protection)
    value.grain_preservation = 0.0
    value.nr_passes = int(settings.passes)
    value.shimmer_suppression = 0.0
    value.prefer_nvof = 0
    return value


def _text(value: bytes | None) -> str:
    return value.decode("utf-8", "replace") if value else ""


_c_float_p = ctypes.POINTER(ctypes.c_float)
#: The engine calls this module uses: name, argument types, result type.
_SIGNATURES = {
    "dlss5nr_version": ([], ctypes.c_char_p),
    "dlss5nr_gpu_name": ([], ctypes.c_char_p),
    "dlss5nr_frame_abi_version": ([], ctypes.c_uint32),
    "dlss5nr_init": ([ctypes.c_int, ctypes.c_wchar_p, ctypes.c_char_p, ctypes.c_int],
                     ctypes.c_int),
    "dlss5nr_process_v6": ([_c_float_p, _c_float_p, ctypes.c_int, ctypes.c_int,
                            ctypes.POINTER(RenderParameters), ctypes.c_char_p, ctypes.c_int],
                           ctypes.c_int),
}


class NeuralBridge:
    """The engine, loaded once, and the calls into it.

    ``library`` stands in for the DLL in tests: anything with the engine's
    functions as attributes.
    """

    def __init__(self, directory: Path, library=None) -> None:
        # Absolute: Windows refuses a relative DLL directory, and the engine
        # is handed this path to find NVIDIA's runtime by.
        self.directory = Path(directory).resolve()
        self._library = library
        self._dll_directory = None
        self.version = "unloaded"
        self.gpu_name = ""
        self._initialized = False
        self._poisoned = ""
        self._kept: list = []
        self._feature_shape: tuple | None = None

    @property
    def poisoned(self) -> str:
        return self._poisoned

    def load(self) -> None:
        """Load the engine and check it speaks this module's ABI; binds no GPU yet."""
        if self._library is None:
            if not _complete(self.directory):
                raise NeuralError(missing_reason())
            loader = getattr(ctypes, "WinDLL", None)
            if loader is None:
                raise NeuralError("Neural Rendering runs on Windows only")
            if hasattr(os, "add_dll_directory"):
                # The engine's own dependencies sit beside it.
                self._dll_directory = os.add_dll_directory(str(self.directory))
            try:
                self._library = loader(str(self.directory / BRIDGE_NAME))
            except OSError as error:
                raise NeuralError(f"the engine could not be loaded: {error}") from error
        library = self._library
        for name, (argtypes, restype) in _SIGNATURES.items():
            function = getattr(library, name, None)
            if function is None:
                raise NeuralError(f"the engine has no {name}; it may be too old or too new")
            function.argtypes = argtypes
            function.restype = restype
        release = getattr(library, "dlss5nr_release_session", None)
        if release is not None:
            release.argtypes = []
            release.restype = ctypes.c_int
        self.version = _text(library.dlss5nr_version()) or "unknown"
        abi = int(library.dlss5nr_frame_abi_version())
        if abi != BRIDGE_ABI_VERSION:
            raise NeuralError(f"Neuroframe Engine {self.version} speaks ABI {abi}; this "
                              f"version of refview needs ABI {BRIDGE_ABI_VERSION}")

    def _guard(self) -> None:
        if self._poisoned:
            raise NeuralPoisonedError(
                f"Neural Rendering stopped after {self._poisoned}; restart refview to use it again")

    def _call(self, label: str, function, keep: tuple = (), timeout: float = WATCHDOG_SECONDS):
        """Run a native call on a thread of its own, and give up on it if it hangs."""
        done = threading.Event()
        outcome: list = []
        failure: list = []

        def invoke() -> None:
            try:
                outcome.append(function())
            except BaseException as error:  # noqa: BLE001 -- reported below
                failure.append(error)
            finally:
                done.set()

        threading.Thread(target=invoke, name=f"neural-{label}", daemon=True).start()
        if not done.wait(timeout):
            self._poisoned = f"{label} took longer than {timeout:g} seconds"
            # Native code may still be writing into these; keep them alive.
            self._kept.extend(keep)
            self._guard()
        if failure:
            self._poisoned = f"a native error during {label} ({failure[0]})"
            self._guard()
        return outcome[0]

    def initialize(self, ordinal: int = 0) -> None:
        """Bind the engine to the CUDA device ``ordinal``; done once per process."""
        self._guard()
        if self._initialized:
            return
        error = ctypes.create_string_buffer(4096)
        ok = self._call("start-up", lambda: self._library.dlss5nr_init(
            int(ordinal), str(self.directory), error, len(error)), (error,))
        if not ok:
            raise NeuralError(f"the engine could not start: "
                              f"{_text(error.value) or 'no reason given'}")
        self._initialized = True
        self.gpu_name = _text(self._library.dlss5nr_gpu_name()) or "NVIDIA GPU"

    def process(self, rgb: np.ndarray, settings: NeuralSettings) -> np.ndarray:
        """Neural Rendering of ``rgb``, an ``(h, w, 3)`` display picture in [0, 1]."""
        self._guard()
        h, w = rgb.shape[:2]
        check_size(w, h)
        source = np.ascontiguousarray(np.clip(rgb[..., :3], 0.0, 1.0), dtype=np.float32)
        out = np.empty_like(source)
        params = render_parameters(settings)
        shape = (w, h, params.nr_passes)
        if self._feature_shape is not None and self._feature_shape != shape:
            # The engine's features are made for one size; free them for the next.
            self.release()
        error = ctypes.create_string_buffer(4096)
        ok = self._call(
            "Neural Rendering",
            lambda: self._library.dlss5nr_process_v6(
                source.ctypes.data_as(_c_float_p), out.ctypes.data_as(_c_float_p), w, h,
                ctypes.byref(params), error, len(error)),
            (source, out, params, error),
            timeout=min(180.0, WATCHDOG_SECONDS * params.nr_passes),
        )
        if not ok:
            detail = _text(error.value) or "no reason given"
            if any(word in detail.lower() for word in (
                    "corrupt", "access violation", "device removal", "device recovery",
                    "reinitialization failed")):
                self._poisoned = detail
                self._guard()
            raise NeuralError(detail)
        self._feature_shape = shape
        return np.clip(out, 0.0, 1.0)

    def release(self) -> None:
        """Free the engine's features, keeping NGX itself loaded (never shut down)."""
        self._feature_shape = None
        release = getattr(self._library, "dlss5nr_release_session", None)
        if release is not None and self._initialized and not self._poisoned:
            self._call("release", release)


@dataclass(frozen=True)
class NeuralInfo:
    """Whether Neural Rendering can run here, and on what."""

    available: bool
    #: "Neuroframe Engine 11.0", once the engine is loaded.
    engine: str = ""
    #: The GPU it runs on, once it has run.
    device: str = ""
    reason: str | None = None

    @property
    def summary(self) -> str:
        if not self.available:
            return f"DLSS 5 Neural Rendering: {self.reason}"
        where = f" on {self.device}" if self.device else ""
        return f"DLSS 5 Neural Rendering ({self.engine}){where}"


class NeuralService:
    """The one thread Neural Rendering runs on, and the engine it has loaded.

    One thread, so NGX is always called from where it was started and two
    pictures are never enhanced at once.  The engine can be loaded only once
    in a process: if the preferences point at another folder later, the
    change takes effect at the next start.
    """

    def __init__(self, bridge_factory=NeuralBridge) -> None:
        self._pool = ThreadPoolExecutor(1, thread_name_prefix="neural")
        self._factory = bridge_factory
        self._bridge: NeuralBridge | None = None
        self._error: str | None = None
        self._info: NeuralInfo | None = None
        self._lock = threading.Lock()

    def probe(self) -> Future:
        """Find out, on the service thread, whether the engine is here.

        The future holds a :class:`NeuralInfo`.
        """
        return self._pool.submit(self._probe)

    def info(self) -> NeuralInfo | None:
        """What the last probe found, or ``None`` before one has finished."""
        with self._lock:
            return self._info

    def _set_info(self, info: NeuralInfo) -> NeuralInfo:
        with self._lock:
            self._info = info
        return info

    def _probe(self) -> NeuralInfo:
        directory = engine_dir()
        if self._bridge is not None:
            if directory is not None and directory.resolve() != self._bridge.directory:
                return self._set_info(NeuralInfo(
                    False, reason="restart refview to use the engine in the new folder"))
            if self._bridge.poisoned:
                return self._set_info(NeuralInfo(False, reason=self._bridge.poisoned))
            return self._set_info(NeuralInfo(True, f"Neuroframe Engine {self._bridge.version}",
                                             self._bridge.gpu_name))
        if directory is None:
            return self._set_info(NeuralInfo(False, reason=missing_reason()))
        bridge = self._factory(directory)
        try:
            bridge.load()
        except Exception as error:  # noqa: BLE001 -- shown in the panel
            return self._set_info(NeuralInfo(False, reason=str(error)))
        self._bridge = bridge
        return self._set_info(NeuralInfo(True, f"Neuroframe Engine {bridge.version}"))

    def submit(self, display: np.ndarray, settings: NeuralSettings) -> Future:
        """Enhance ``display``, ``(h, w, 4)`` display values, off the calling thread.

        The future holds ``(image, info)``: the enhanced ``(h, w, 4)`` picture
        with the alpha it came with, and where it was done.
        """
        return self._pool.submit(self._enhance, display, settings)

    def _enhance(self, display: np.ndarray, settings: NeuralSettings):
        info = self._probe()
        if not info.available or self._bridge is None:
            raise NeuralError(info.reason or "Neural Rendering is not available")
        bridge = self._bridge
        bridge.initialize()
        rgb = bridge.process(display[..., :3], settings)
        out = np.empty(display.shape, np.float32)
        out[..., :3] = rgb
        out[..., 3] = display[..., 3] if display.shape[-1] > 3 else 1.0
        info = self._set_info(NeuralInfo(True, f"Neuroframe Engine {bridge.version}",
                                         bridge.gpu_name))
        return out, info

    def shutdown(self) -> None:
        def close():
            if self._bridge is not None:
                with contextlib.suppress(Exception):
                    self._bridge.release()

        with contextlib.suppress(Exception):
            self._pool.submit(close).result(timeout=5.0)
        self._pool.shutdown(wait=False, cancel_futures=True)
