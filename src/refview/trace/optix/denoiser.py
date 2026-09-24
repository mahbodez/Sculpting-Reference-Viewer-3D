"""NVIDIA's OptiX AI denoiser, run on the GPU through the driver.

The denoiser is a neural network trained on path-traced pictures: given the
noisy image, and optionally the albedo and normals of the first surfaces it
saw, it returns the picture as it would look with far more samples.  The HDR
model is used, since a render is light, not display values; the picture's
average brightness is measured first so the network sees it at the exposure
it was trained on.

The normals must be in camera space for OptiX, not world space; the caller
passes the camera's rotation.  Everything else -- the device, its memory,
the model's state -- is set up once for a size and kept for the next
picture of the same size.  One instance belongs to one thread, the one it
was made on, since that is where its CUDA context is current.
"""

from __future__ import annotations

import ctypes

import numpy as np

from . import abi
from .cuda import Cuda, CudaError
from .loader import Optix, OptixError


class OptixDenoiser:
    def __init__(self) -> None:
        try:
            self.cuda = Cuda()
        except CudaError as error:
            raise OptixError(str(error)) from error
        self.optix = Optix()
        self.device_name = self.cuda.name
        self._context = abi.OptixDeviceContext()
        self._denoiser = None
        self._key = None
        self._buffers: dict[str, tuple[int, int]] = {}
        self._sizes = abi.OptixDenoiserSizes()
        self.cuda.push()
        try:
            options = abi.OptixDeviceContextOptions()
            self.optix.check(self.optix.optixDeviceContextCreate(
                self.cuda.context, ctypes.byref(options), ctypes.byref(self._context)),
                "Creating the OptiX context")
        finally:
            self.cuda.pop()

    # -- set-up ----------------------------------------------------------------

    def _buffer(self, name: str, size: int) -> int:
        pointer, held = self._buffers.get(name, (0, 0))
        if held >= size and pointer:
            return pointer
        if pointer:
            self.cuda.free(pointer)
        pointer = self.cuda.alloc(size)
        self._buffers[name] = (pointer, size)
        return pointer

    def _prepare(self, width: int, height: int, albedo: bool, normal: bool) -> None:
        key = (width, height, albedo, normal)
        if key == self._key:
            return
        if self._denoiser is not None:
            self.optix.optixDenoiserDestroy(self._denoiser)
            self._denoiser = None
        options = abi.OptixDenoiserOptions(int(albedo), int(normal),
                                           abi.OPTIX_DENOISER_ALPHA_MODE_COPY)
        denoiser = abi.OptixDenoiser()
        self.optix.check(self.optix.optixDenoiserCreate(
            self._context, abi.OPTIX_DENOISER_MODEL_KIND_HDR, ctypes.byref(options),
            ctypes.byref(denoiser)), "Creating the denoiser")
        self._denoiser = denoiser
        sizes = abi.OptixDenoiserSizes()
        self.optix.check(self.optix.optixDenoiserComputeMemoryResources(
            denoiser, width, height, ctypes.byref(sizes)), "Sizing the denoiser")
        self._sizes = sizes
        state = self._buffer("state", sizes.stateSizeInBytes)
        scratch_size = max(sizes.withoutOverlapScratchSizeInBytes,
                           sizes.computeIntensitySizeInBytes)
        scratch = self._buffer("scratch", scratch_size)
        self.optix.check(self.optix.optixDenoiserSetup(
            denoiser, None, width, height, state, sizes.stateSizeInBytes, scratch,
            sizes.withoutOverlapScratchSizeInBytes), "Setting the denoiser up")
        self._key = key

    @staticmethod
    def _image(pointer: int, width: int, height: int) -> abi.OptixImage2D:
        return abi.OptixImage2D(pointer, width, height, width * 12, 12,
                                abi.OPTIX_PIXEL_FORMAT_FLOAT3)

    # -- denoising -------------------------------------------------------------

    def denoise(self, color: np.ndarray, albedo: np.ndarray | None = None,
                normal: np.ndarray | None = None) -> np.ndarray:
        """``(h, w, 3)`` linear light in, the same out; guides are ``(h, w, 3)`` too.

        ``normal`` must already be in camera space.
        """
        color = np.ascontiguousarray(color[..., :3], dtype=np.float32)
        height, width = color.shape[:2]
        use_albedo = albedo is not None
        use_normal = normal is not None and use_albedo   # OptiX: normals need the albedo
        self.cuda.push()
        try:
            self._prepare(width, height, use_albedo, use_normal)
            nbytes = color.nbytes
            source = self._buffer("color", nbytes)
            target = self._buffer("output", nbytes)
            self.cuda.upload(source, color)
            guide = abi.OptixDenoiserGuideLayer()
            if use_albedo:
                data = np.ascontiguousarray(np.clip(albedo[..., :3], 0.0, 1.0), dtype=np.float32)
                pointer = self._buffer("albedo", data.nbytes)
                self.cuda.upload(pointer, data)
                guide.albedo = self._image(pointer, width, height)
            if use_normal:
                data = np.ascontiguousarray(normal[..., :3], dtype=np.float32)
                pointer = self._buffer("normal", data.nbytes)
                self.cuda.upload(pointer, data)
                guide.normal = self._image(pointer, width, height)
            layer = abi.OptixDenoiserLayer()
            layer.input = self._image(source, width, height)
            layer.output = self._image(target, width, height)
            layer.type = abi.OPTIX_DENOISER_AOV_TYPE_NONE
            sizes = self._sizes
            scratch_size = max(sizes.withoutOverlapScratchSizeInBytes,
                               sizes.computeIntensitySizeInBytes)
            scratch = self._buffer("scratch", scratch_size)
            intensity = self._buffer("intensity", 4)
            self.optix.check(self.optix.optixDenoiserComputeIntensity(
                self._denoiser, None, ctypes.byref(layer.input), intensity, scratch,
                sizes.computeIntensitySizeInBytes), "Measuring the picture's brightness")
            params = abi.OptixDenoiserParams()
            params.hdrIntensity = intensity
            params.blendFactor = 0.0
            state = self._buffer("state", sizes.stateSizeInBytes)
            self.optix.check(self.optix.optixDenoiserInvoke(
                self._denoiser, None, ctypes.byref(params), state, sizes.stateSizeInBytes,
                ctypes.byref(guide), ctypes.byref(layer), 1, 0, 0, scratch,
                sizes.withoutOverlapScratchSizeInBytes), "Denoising")
            self.cuda.synchronize()
            out = np.empty_like(color)
            self.cuda.download(out, target)
            return out
        except CudaError as error:
            raise OptixError(str(error)) from error
        finally:
            self.cuda.pop()

    def close(self) -> None:
        self.cuda.push()
        try:
            if self._denoiser is not None:
                self.optix.optixDenoiserDestroy(self._denoiser)
                self._denoiser = None
            for pointer, _size in self._buffers.values():
                self.cuda.free(pointer)
            self._buffers.clear()
            if self._context:
                self.optix.optixDeviceContextDestroy(self._context)
                self._context = abi.OptixDeviceContext()
        finally:
            self.cuda.pop()
            self.cuda.release()
