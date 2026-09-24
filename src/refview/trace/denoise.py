"""Denoising a render: choosing a denoiser, and running it on a thread of its own.

Three denoisers, in the order "Auto" tries them:

* **Intel Open Image Denoise** on a GPU -- CUDA with any NVIDIA driver, Metal
  on a Mac -- then **NVIDIA OptiX**, then Open Image Denoise on the CPU;
* the **built-in** edge-aware filter, which needs nothing and always works.

What each can do on this machine is found out once, the first time it is
asked, and kept; the Render panel lists the ones that cannot run, with the
reason.  All denoising happens on one thread, the :class:`DenoiseService`'s,
so a GPU's context stays current where it was made and two renders never
denoise at once on the same device.  A denoiser that fails mid-way is
reported and the built-in one used instead, so a render is never lost to it.
"""

from __future__ import annotations

import contextlib
import os
import threading
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass

import numpy as np

from ..core.path_trace import DenoiserBackend, DenoiserDevice, DenoiseSettings
from .film import Film


@dataclass(frozen=True)
class DenoiserInfo:
    backend: DenoiserBackend
    available: bool
    #: Where it runs, in words: "CUDA (NVIDIA GeForce ...)", "CPU".
    device: str = ""
    #: Why it cannot run, when it cannot.
    reason: str | None = None
    on_gpu: bool = False

    @property
    def summary(self) -> str:
        if not self.available:
            return f"{self.backend.label}: {self.reason}"
        where = f" on {self.device}" if self.device else ""
        return f"{self.backend.label}{where}"


@dataclass
class DenoiseRequest:
    color: np.ndarray                  # (h, w, 3) linear light
    albedo: np.ndarray | None = None   # (h, w, 3)
    normal: np.ndarray | None = None   # (h, w, 3), world space
    depth: np.ndarray | None = None    # (h, w)
    noise: np.ndarray | None = None    # (h, w) expected error, as a luminance
    #: World directions into the camera's frame, for OptiX's normals.
    view_rotation: np.ndarray | None = None


def request_from_film(film: Film, view_rotation: np.ndarray | None = None) -> DenoiseRequest:
    """The picture and its guides, as a film holds them."""
    beauty = film.beauty()
    noise = None
    if film.count.max() > 1:
        n = np.maximum(film.count, 1).astype(np.float32)
        half = np.maximum((film.count + 1) // 2, 1).astype(np.float32)
        full = film.rgba[..., :3] / n[..., None]
        even = film.even / half[..., None]
        noise = np.abs(full - even) @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    return DenoiseRequest(
        color=beauty[..., :3], albedo=film.albedo_pass(), normal=film.normal_pass(),
        depth=film.depth_pass(), noise=noise, view_rotation=view_rotation,
    )


class DenoiseService:
    """The one thread every denoise runs on, and the denoisers it has started."""

    def __init__(self) -> None:
        self._pool = ThreadPoolExecutor(1, thread_name_prefix="denoise")
        self._cpu_pool: ThreadPoolExecutor | None = None
        self._oidn: dict = {}
        self._optix = None
        self._optix_error: str | None = None
        self._infos: list[DenoiserInfo] | None = None
        self._lock = threading.Lock()

    # -- what can run here -----------------------------------------------------

    def probe(self) -> Future:
        """Find out, on the service thread, which denoisers can run.

        The future holds a list of :class:`DenoiserInfo`.
        """
        return self._pool.submit(self._probe)

    def infos(self) -> list[DenoiserInfo] | None:
        """What the last probe found, or ``None`` before one has finished."""
        with self._lock:
            return self._infos

    def _probe(self) -> list[DenoiserInfo]:
        with self._lock:
            if self._infos is not None:
                return self._infos
        infos = []
        try:
            from .denoise_oidn import gpu_name

            gpu = gpu_name()
            device = f"GPU ({gpu})" if gpu else "CPU"
            infos.append(DenoiserInfo(DenoiserBackend.OIDN, True, device, None, gpu is not None))
        except Exception as error:  # noqa: BLE001
            infos.append(DenoiserInfo(DenoiserBackend.OIDN, False, "", str(error)))
        try:
            optix = self._optix_denoiser()
            infos.append(DenoiserInfo(DenoiserBackend.OPTIX, True, f"GPU ({optix.device_name})",
                                      None, True))
        except Exception as error:  # noqa: BLE001
            infos.append(DenoiserInfo(DenoiserBackend.OPTIX, False, "", str(error)))
        infos.append(DenoiserInfo(DenoiserBackend.BUILTIN, True, "CPU", None, False))
        with self._lock:
            self._infos = infos
        return infos

    def resolve(self, backend: DenoiserBackend) -> DenoiserInfo:
        """The denoiser a setting stands for, here; probes if nothing has yet."""
        infos = {info.backend: info for info in self._probe_now()}
        if backend is not DenoiserBackend.AUTO:
            info = infos.get(backend)
            if info is not None and info.available:
                return info
            return infos[DenoiserBackend.BUILTIN]
        oidn = infos.get(DenoiserBackend.OIDN)
        optix = infos.get(DenoiserBackend.OPTIX)
        if oidn is not None and oidn.available and oidn.on_gpu:
            return oidn
        if optix is not None and optix.available:
            return optix
        if oidn is not None and oidn.available:
            return oidn
        return infos[DenoiserBackend.BUILTIN]

    def _probe_now(self) -> list[DenoiserInfo]:
        infos = self.infos()
        if infos is not None:
            return infos
        if threading.current_thread().name.startswith("denoise"):
            return self._probe()
        return self.probe().result()

    # -- denoising -------------------------------------------------------------

    def submit(self, request: DenoiseRequest, settings: DenoiseSettings) -> Future:
        """Denoise off the calling thread; the future holds ``(image, info, note)``."""
        return self._pool.submit(self._denoise, request, settings)

    def denoise(self, request: DenoiseRequest, settings: DenoiseSettings):
        return self.submit(request, settings).result()

    def _optix_denoiser(self):
        if self._optix is None:
            if self._optix_error is not None:
                raise RuntimeError(self._optix_error)
            try:
                from .optix.denoiser import OptixDenoiser

                self._optix = OptixDenoiser()
            except Exception as error:  # noqa: BLE001
                self._optix_error = str(error)
                raise
        return self._optix

    def _oidn_denoiser(self, device: DenoiserDevice):
        denoiser = self._oidn.get(device)
        if denoiser is None:
            from .denoise_oidn import OidnDenoiser

            denoiser = OidnDenoiser(device)
            self._oidn[device] = denoiser
        return denoiser

    def _denoise(self, request: DenoiseRequest, settings: DenoiseSettings):
        info = self.resolve(settings.backend)
        albedo = request.albedo if settings.use_albedo else None
        normal = request.normal if (settings.use_normal and albedo is not None) else None
        note = None
        color = np.ascontiguousarray(request.color[..., :3], dtype=np.float32)
        color = np.nan_to_num(np.maximum(color, 0.0), nan=0.0, posinf=0.0)
        try:
            if info.backend is DenoiserBackend.OIDN:
                oidn = self._oidn_denoiser(settings.device)
                out = oidn.denoise(color, albedo, normal, settings.quality,
                                   clean_aux=not settings.prefilter_guides)
                info = DenoiserInfo(DenoiserBackend.OIDN, True,
                                    f"GPU ({oidn.device_name})" if oidn.on_gpu else "CPU", None,
                                    oidn.on_gpu)
            elif info.backend is DenoiserBackend.OPTIX:
                cam_normal = None
                if normal is not None:
                    rotation = (np.eye(3) if request.view_rotation is None
                                else np.asarray(request.view_rotation, np.float32))
                    cam_normal = normal @ rotation.T
                out = self._optix_denoiser().denoise(color, albedo, cam_normal)
            else:
                out = self._builtin(color, albedo, request, settings)
        except Exception as error:  # noqa: BLE001 -- fall back rather than lose the render
            note = f"{info.backend.label} failed ({error}); used the built-in denoiser"
            info = DenoiserInfo(DenoiserBackend.BUILTIN, True, "CPU")
            out = self._builtin(color, albedo, request, settings)
        mix = min(max(float(settings.mix), 0.0), 1.0)
        if mix < 1.0:
            out = color + (out - color) * mix
        return np.ascontiguousarray(out, dtype=np.float32), info, note

    def _builtin(self, color, albedo, request, settings):
        from .denoise_atrous import atrous

        if self._cpu_pool is None:
            self._cpu_pool = ThreadPoolExecutor(max(1, (os.cpu_count() or 2) - 1),
                                                thread_name_prefix="denoise-cpu")
        return atrous(color, albedo, request.normal if settings.use_normal else None,
                      request.depth, request.noise, settings.atrous_passes, self._cpu_pool)

    def shutdown(self) -> None:
        def close():
            for denoiser in self._oidn.values():
                denoiser.close()
            self._oidn.clear()
            if self._optix is not None:
                with contextlib.suppress(Exception):
                    self._optix.close()
                self._optix = None

        with contextlib.suppress(Exception):
            self._pool.submit(close).result(timeout=5.0)
        self._pool.shutdown(wait=False, cancel_futures=True)
        if self._cpu_pool is not None:
            self._cpu_pool.shutdown(wait=False, cancel_futures=True)
