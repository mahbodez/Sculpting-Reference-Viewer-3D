"""The OptiX declarations match OptiX 8.0's headers, byte for byte.

A size or an offset out by one would not fail politely: the driver would
read past a structure and the program would crash.  The numbers here are
the headers' own, on 64-bit platforms.
"""

from __future__ import annotations

import ctypes

import pytest

from refview.trace.optix import abi, loader
from refview.trace.optix.loader import OptixError


def test_the_function_table_has_the_headers_48_members_in_order():
    assert abi.ABI_VERSION == 87
    assert len(abi.FUNCTION_TABLE) == 48
    assert ctypes.sizeof(abi.FunctionTable) == 48 * 8
    assert abi.FUNCTION_TABLE.index("optixLaunch") == 39
    assert abi.FUNCTION_TABLE.index("optixDenoiserCreate") == 40
    assert abi.FUNCTION_TABLE.index("optixDenoiserInvoke") == 44
    assert abi.FUNCTION_TABLE.index("optixDenoiserComputeIntensity") == 45


@pytest.mark.parametrize(("structure", "size"), [
    (abi.OptixImage2D, 32),
    (abi.OptixDenoiserOptions, 12),
    (abi.OptixDenoiserGuideLayer, 192),
    (abi.OptixDenoiserLayer, 104),
    (abi.OptixDenoiserParams, 32),
    (abi.OptixDenoiserSizes, 56),
    (abi.OptixDeviceContextOptions, 24),
])
def test_structure_sizes(structure, size):
    assert ctypes.sizeof(structure) == size


def test_field_offsets():
    assert abi.OptixImage2D.format.offset == 24
    assert abi.OptixDenoiserLayer.output.offset == 64
    assert abi.OptixDenoiserLayer.type.offset == 96
    assert abi.OptixDenoiserParams.hdrAverageColor.offset == 16
    assert abi.OptixDenoiserParams.temporalModeUsePreviousLayers.offset == 24
    assert abi.OptixDenoiserSizes.computeAverageColorSizeInBytes.offset == 32
    assert abi.OptixDenoiserSizes.internalGuideLayerPixelSizeInBytes.offset == 48
    assert abi.OptixDenoiserGuideLayer.normal.offset == 32


def test_no_driver_is_a_reason_not_a_crash(monkeypatch):
    def missing():
        raise OptixError("No NVIDIA driver with OptiX was found")

    monkeypatch.setattr(loader, "load_library", missing)
    with pytest.raises(OptixError, match="No NVIDIA driver"):
        loader.Optix()
