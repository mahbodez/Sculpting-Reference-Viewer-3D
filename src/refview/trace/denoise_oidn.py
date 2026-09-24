"""Intel Open Image Denoise, through the ``mitsuba-oidn`` bindings.

Open Image Denoise runs on the CPU anywhere, on CUDA wherever an NVIDIA
driver is present -- no toolkit needed -- and on Metal on a Mac.  A filter
and its device buffers are made once for a picture size and kept, which is
what makes a denoise of a 4K frame take a fifth of a second on a GPU rather
than several: setting the network up is most of the cost of a single call.
"""

from __future__ import annotations

import numpy as np

from ..core.path_trace import DenoiserDevice, DenoiserQuality


class OidnError(RuntimeError):
    pass


def _module():
    try:
        import mitsuba_oidn
    except Exception as error:  # noqa: BLE001
        raise OidnError(f"Open Image Denoise is not installed ({error})") from error
    return mitsuba_oidn


def gpu_name() -> str | None:
    """The GPU Open Image Denoise would use, or ``None`` for none."""
    oidn = _module()
    try:
        for device in oidn.physical_devices():
            if device.type in (oidn.DeviceType.CUDA, oidn.DeviceType.HIP, oidn.DeviceType.SYCL,
                               oidn.DeviceType.Metal):
                return str(device.name)
    except Exception:  # noqa: BLE001
        return None
    return None


class OidnDenoiser:
    """A filter, kept for its size.  One instance belongs to one thread."""

    def __init__(self, device: DenoiserDevice = DenoiserDevice.AUTO) -> None:
        oidn = _module()
        self._oidn = oidn
        kinds = {
            DenoiserDevice.CPU: oidn.DeviceType.CPU,
            DenoiserDevice.AUTO: oidn.DeviceType.Default,
        }
        if device is DenoiserDevice.GPU:
            if gpu_name() is None:
                raise OidnError("Open Image Denoise found no GPU it can use")
            kind = oidn.DeviceType.Default
        else:
            kind = kinds[device]
        try:
            self._device = oidn.Device(kind)
            if not self._device.committed:
                self._device.commit()
        except Exception as error:  # noqa: BLE001
            raise OidnError(f"Open Image Denoise could not start ({error})") from error
        self.on_gpu = self._device.type is not oidn.DeviceType.CPU
        self.device_name = (gpu_name() or "GPU") if self.on_gpu else "CPU"
        self._key = None
        self._filter = None
        self._buffers: dict[str, object] = {}

    def _prepare(self, width, height, albedo, normal, quality, clean_aux):
        key = (width, height, albedo, normal, quality, clean_aux)
        if key == self._key:
            return
        oidn = self._oidn
        storage = oidn.Storage.Device if self.on_gpu else oidn.Storage.Host
        size = width * height * 12
        self._buffers = {name: self._device.new_buffer(size, storage)
                         for name in ("color", "output", "albedo", "normal")}
        f = self._device.new_filter("RT")
        f.hdr = True
        f.clean_aux = clean_aux
        f.set("quality", {DenoiserQuality.HIGH: oidn.Quality.High,
                          DenoiserQuality.BALANCED: oidn.Quality.Balanced,
                          DenoiserQuality.FAST: oidn.Quality.Fast}[quality])
        fmt = oidn.Format.Float3
        f.set_image("color", self._buffers["color"], fmt, width, height)
        f.set_image("output", self._buffers["output"], fmt, width, height)
        if albedo:
            f.set_image("albedo", self._buffers["albedo"], fmt, width, height)
        if normal:
            f.set_image("normal", self._buffers["normal"], fmt, width, height)
        f.commit()
        self._filter = f
        self._key = key

    def denoise(self, color: np.ndarray, albedo: np.ndarray | None = None,
                normal: np.ndarray | None = None, quality=DenoiserQuality.HIGH,
                clean_aux: bool = False) -> np.ndarray:
        color = np.ascontiguousarray(color[..., :3], dtype=np.float32)
        height, width = color.shape[:2]
        use_normal = normal is not None and albedo is not None   # OIDN: normals need the albedo
        self._prepare(width, height, albedo is not None, use_normal, quality, clean_aux)
        self._buffers["color"].write(color)
        if albedo is not None:
            self._buffers["albedo"].write(
                np.ascontiguousarray(np.clip(albedo[..., :3], 0.0, 1.0), dtype=np.float32))
        if use_normal:
            self._buffers["normal"].write(np.ascontiguousarray(normal[..., :3], dtype=np.float32))
        self._filter.execute()
        out = np.empty_like(color)
        self._buffers["output"].read(out)
        return out

    def close(self) -> None:
        self._filter = None
        self._buffers.clear()
