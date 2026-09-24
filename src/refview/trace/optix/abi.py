"""The parts of the OptiX 8.0 host interface the denoiser uses, as ctypes declarations.

OptiX lives in the NVIDIA display driver (``nvoptix.dll``, ``libnvoptix.so.1``)
and is reached through one exported function, ``optixQueryFunctionTable``,
which fills a table of function pointers laid out for a given interface
version.  This module transcribes that version's table order and the few
structures and constants the denoiser needs, from NVIDIA's published headers
(``optix_function_table.h`` and ``optix_types.h`` of OptiX 8.0, interface
version 87); a driver that knows a newer interface still serves this one.

A layout that disagrees with the driver's would crash the program rather
than fail politely, so ``tests/test_optix_abi.py`` pins every size and
offset below to the header's.
"""

from __future__ import annotations

import ctypes

#: The interface version this transcription is of.
ABI_VERSION = 87

CUdeviceptr = ctypes.c_uint64
CUcontext = ctypes.c_void_p
CUstream = ctypes.c_void_p
OptixDeviceContext = ctypes.c_void_p
OptixDenoiser = ctypes.c_void_p
OptixResult = ctypes.c_int

OPTIX_SUCCESS = 0

OPTIX_PIXEL_FORMAT_FLOAT3 = 0x2203
OPTIX_PIXEL_FORMAT_FLOAT4 = 0x2204

OPTIX_DENOISER_MODEL_KIND_LDR = 0x2322
OPTIX_DENOISER_MODEL_KIND_HDR = 0x2323

OPTIX_DENOISER_ALPHA_MODE_COPY = 0
OPTIX_DENOISER_AOV_TYPE_NONE = 0

#: The function table's members, in the header's order: ``optixFoo`` is
#: pointer number ``FUNCTION_TABLE.index("optixFoo")``.
FUNCTION_TABLE = (
    "optixGetErrorName", "optixGetErrorString", "optixDeviceContextCreate",
    "optixDeviceContextDestroy", "optixDeviceContextGetProperty",
    "optixDeviceContextSetLogCallback", "optixDeviceContextSetCacheEnabled",
    "optixDeviceContextSetCacheLocation", "optixDeviceContextSetCacheDatabaseSizes",
    "optixDeviceContextGetCacheEnabled", "optixDeviceContextGetCacheLocation",
    "optixDeviceContextGetCacheDatabaseSizes", "optixModuleCreate", "optixModuleCreateWithTasks",
    "optixModuleGetCompilationState", "optixModuleDestroy", "optixBuiltinISModuleGet",
    "optixTaskExecute", "optixProgramGroupCreate", "optixProgramGroupDestroy",
    "optixProgramGroupGetStackSize", "optixPipelineCreate", "optixPipelineDestroy",
    "optixPipelineSetStackSize", "optixAccelComputeMemoryUsage", "optixAccelBuild",
    "optixAccelGetRelocationInfo", "optixCheckRelocationCompatibility", "optixAccelRelocate",
    "optixAccelCompact", "optixAccelEmitProperty", "optixConvertPointerToTraversableHandle",
    "optixOpacityMicromapArrayComputeMemoryUsage", "optixOpacityMicromapArrayBuild",
    "optixOpacityMicromapArrayGetRelocationInfo", "optixOpacityMicromapArrayRelocate",
    "optixDisplacementMicromapArrayComputeMemoryUsage", "optixDisplacementMicromapArrayBuild",
    "optixSbtRecordPackHeader", "optixLaunch", "optixDenoiserCreate", "optixDenoiserDestroy",
    "optixDenoiserComputeMemoryResources", "optixDenoiserSetup", "optixDenoiserInvoke",
    "optixDenoiserComputeIntensity", "optixDenoiserComputeAverageColor",
    "optixDenoiserCreateWithUserModel",
)


class FunctionTable(ctypes.Structure):
    _fields_ = [(name, ctypes.c_void_p) for name in FUNCTION_TABLE]


class OptixImage2D(ctypes.Structure):
    _fields_ = [
        ("data", CUdeviceptr),
        ("width", ctypes.c_uint),
        ("height", ctypes.c_uint),
        ("rowStrideInBytes", ctypes.c_uint),
        ("pixelStrideInBytes", ctypes.c_uint),
        ("format", ctypes.c_int),
    ]


class OptixDenoiserOptions(ctypes.Structure):
    _fields_ = [
        ("guideAlbedo", ctypes.c_uint),
        ("guideNormal", ctypes.c_uint),
        ("denoiseAlpha", ctypes.c_int),
    ]


class OptixDenoiserGuideLayer(ctypes.Structure):
    _fields_ = [
        ("albedo", OptixImage2D),
        ("normal", OptixImage2D),
        ("flow", OptixImage2D),
        ("previousOutputInternalGuideLayer", OptixImage2D),
        ("outputInternalGuideLayer", OptixImage2D),
        ("flowTrustworthiness", OptixImage2D),
    ]


class OptixDenoiserLayer(ctypes.Structure):
    _fields_ = [
        ("input", OptixImage2D),
        ("previousOutput", OptixImage2D),
        ("output", OptixImage2D),
        ("type", ctypes.c_int),
    ]


class OptixDenoiserParams(ctypes.Structure):
    _fields_ = [
        ("hdrIntensity", CUdeviceptr),
        ("blendFactor", ctypes.c_float),
        ("hdrAverageColor", CUdeviceptr),
        ("temporalModeUsePreviousLayers", ctypes.c_uint),
    ]


class OptixDenoiserSizes(ctypes.Structure):
    _fields_ = [
        ("stateSizeInBytes", ctypes.c_size_t),
        ("withOverlapScratchSizeInBytes", ctypes.c_size_t),
        ("withoutOverlapScratchSizeInBytes", ctypes.c_size_t),
        ("overlapWindowSizeInPixels", ctypes.c_uint),
        ("computeAverageColorSizeInBytes", ctypes.c_size_t),
        ("computeIntensitySizeInBytes", ctypes.c_size_t),
        ("internalGuideLayerPixelSizeInBytes", ctypes.c_size_t),
    ]


class OptixDeviceContextOptions(ctypes.Structure):
    _fields_ = [
        ("logCallbackFunction", ctypes.c_void_p),
        ("logCallbackData", ctypes.c_void_p),
        ("logCallbackLevel", ctypes.c_int),
        ("validationMode", ctypes.c_int),
    ]


def _fn(restype, *argtypes):
    return ctypes.CFUNCTYPE(restype, *argtypes)


#: The signatures of the functions the denoiser calls.
SIGNATURES = {
    "optixGetErrorName": _fn(ctypes.c_char_p, OptixResult),
    "optixGetErrorString": _fn(ctypes.c_char_p, OptixResult),
    "optixDeviceContextCreate": _fn(OptixResult, CUcontext,
                                    ctypes.POINTER(OptixDeviceContextOptions),
                                    ctypes.POINTER(OptixDeviceContext)),
    "optixDeviceContextDestroy": _fn(OptixResult, OptixDeviceContext),
    "optixDenoiserCreate": _fn(OptixResult, OptixDeviceContext, ctypes.c_int,
                               ctypes.POINTER(OptixDenoiserOptions),
                               ctypes.POINTER(OptixDenoiser)),
    "optixDenoiserDestroy": _fn(OptixResult, OptixDenoiser),
    "optixDenoiserComputeMemoryResources": _fn(OptixResult, OptixDenoiser, ctypes.c_uint,
                                               ctypes.c_uint, ctypes.POINTER(OptixDenoiserSizes)),
    "optixDenoiserSetup": _fn(OptixResult, OptixDenoiser, CUstream, ctypes.c_uint, ctypes.c_uint,
                              CUdeviceptr, ctypes.c_size_t, CUdeviceptr, ctypes.c_size_t),
    "optixDenoiserInvoke": _fn(OptixResult, OptixDenoiser, CUstream,
                               ctypes.POINTER(OptixDenoiserParams), CUdeviceptr, ctypes.c_size_t,
                               ctypes.POINTER(OptixDenoiserGuideLayer),
                               ctypes.POINTER(OptixDenoiserLayer), ctypes.c_uint, ctypes.c_uint,
                               ctypes.c_uint, CUdeviceptr, ctypes.c_size_t),
    "optixDenoiserComputeIntensity": _fn(OptixResult, OptixDenoiser, CUstream,
                                         ctypes.POINTER(OptixImage2D), CUdeviceptr, CUdeviceptr,
                                         ctypes.c_size_t),
}

#: ``optixQueryFunctionTable(abi, option count, option keys, option values, table, size)``.
QUERY_FUNCTION_TABLE = (OptixResult, ctypes.c_int, ctypes.c_uint, ctypes.c_void_p,
                        ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t)
