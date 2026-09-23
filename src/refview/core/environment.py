"""HDRI environment maps: reading them, and what the shaders need made of them.

An HDRI is a photograph of all the light arriving at one point, laid out as
an equirectangular panorama in linear radiance.  Lighting a model with one
means asking, for every point of the surface, how much of that light it
catches -- which, done by brute force, is a sum over every texel of the map
per pixel of the screen.  Nothing here does that.  The map is instead read
once, off the thread, into the handful of things a shader can look up at the
cost of a texture fetch or two:

- **Irradiance**, as nine spherical-harmonic coefficients per channel
  (Ramamoorthi and Hanrahan).  Diffuse light is so smooth a function of the
  normal that its first three bands carry all but a few percent of it, so the
  whole of a matte surface's lighting is a short polynomial in the normal.
- **The dominant light**: the direction and colour of a single distant light
  that would account for the map's first band -- the softbox in a studio, the
  sun outdoors.  It is where the shadow map is cast from when the map is the
  only light, and what an approximate shadow is taken out of.
- **Importance-sampling tables**: the map's luminance at a coarse resolution,
  weighted by the solid angle each row covers, as a marginal and a set of
  conditional cumulative distributions, so the skin tracer can send its
  shadow rays where the light actually is (Pharr, Jakob and Humphreys,
  *PBRT*, section 14.2.4).
- **The radiance itself**, downsized to a width a texture can carry, for the
  reflections and for drawing the map behind the model.  The mip chain the
  renderer builds on it stands in for a prefiltered specular map.

Directions follow one convention throughout, in the map's own frame with y
up: the centre of the panorama looks down -z, its left edge down +z from
behind, and its top row straight up.  :func:`direction_to_uv` and
:func:`uv_to_direction` are the whole of it, and the GLSL in
:mod:`refview.render.environment` mirrors them.

Radiance ``.hdr`` files are read here in numpy.  OpenEXR's compression
schemes (PIZ, the usual one, is a wavelet and a Huffman coder) are not worth
reimplementing, so ``.exr`` goes through the ``OpenEXR`` package.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

#: The panoramas the viewer reads.
ENVIRONMENT_SUFFIXES = (".hdr", ".exr")
#: Widest radiance map handed to the GPU.  Two thousand texels round the
#: horizon is sharper than the background is ever seen at, and 16 MB of half
#: floats with its mips.
MAX_RADIANCE_WIDTH = 2048
#: Width of the map the tracer samples from.  Coarse on purpose: the tables
#: are searched per ray, and the radiance a sample carries is read from the
#: same coarse cells so the estimate stays unbiased at any resolution.
SAMPLING_WIDTH = 256
#: Width the harmonics are projected from.  Irradiance has no detail finer
#: than a few degrees; a finer map changes the ninth decimal place.
SH_WIDTH = 128
#: Largest value a half-float texture can carry, less a margin.
HALF_MAX = 65000.0


class EnvironmentLoadError(RuntimeError):
    """Raised when a file cannot be read as an HDRI."""


# -- directions --------------------------------------------------------------


def uv_to_direction(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Unit directions for panorama coordinates, ``u`` across and ``v`` down, both 0 to 1."""
    u = np.asarray(u, dtype=np.float64)
    v = np.asarray(v, dtype=np.float64)
    phi = (u - 0.5) * 2.0 * math.pi
    theta = v * math.pi
    sin_theta = np.sin(theta)
    return np.stack(
        [sin_theta * np.sin(phi), np.cos(theta), -sin_theta * np.cos(phi)], axis=-1
    )


def direction_to_uv(direction: np.ndarray) -> np.ndarray:
    """Panorama coordinates ``(u, v)`` for unit directions; :func:`uv_to_direction` undone."""
    d = np.asarray(direction, dtype=np.float64)
    u = np.arctan2(d[..., 0], -d[..., 2]) / (2.0 * math.pi) + 0.5
    v = np.arccos(np.clip(d[..., 1], -1.0, 1.0)) / math.pi
    return np.stack([u, v], axis=-1)


def rotation_y(degrees: float) -> np.ndarray:
    """A turn about the vertical axis, as a 3x3 matrix."""
    angle = math.radians(degrees)
    c, s = math.cos(angle), math.sin(angle)
    return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]])


# -- reading -----------------------------------------------------------------


def read_radiance(path: str | Path) -> np.ndarray:
    """Read an HDRI into an ``(H, W, 3)`` float32 array of linear radiance, top row first."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix not in ENVIRONMENT_SUFFIXES:
        raise EnvironmentLoadError(f"{path.name} is not an HDRI (.hdr or .exr)")
    try:
        pixels = _read_hdr(path.read_bytes()) if suffix == ".hdr" else _read_exr(path)
    except OSError as error:
        raise EnvironmentLoadError(f"{path.name} could not be read: {error}") from error
    if pixels.ndim != 3 or pixels.shape[0] < 2 or pixels.shape[1] < 4:
        raise EnvironmentLoadError(f"{path.name} is too small to be a panorama")
    return pixels


def _read_exr(path: Path) -> np.ndarray:
    try:
        import OpenEXR
    except ImportError as error:  # pragma: no cover - a dependency, but say so if missing
        raise EnvironmentLoadError(
            "Reading .exr needs the OpenEXR package (pip install OpenEXR); "
            ".hdr files work without it"
        ) from error
    try:
        # The channels are only readable while the file is open.
        with OpenEXR.File(str(path)) as exr:
            channels = {name: np.asarray(channel.pixels)
                        for name, channel in exr.channels().items()}
    except Exception as error:  # OpenEXR raises bare RuntimeErrors and IOErrors
        raise EnvironmentLoadError(
            f"{path.name} is not a readable OpenEXR file ({error})"
        ) from error
    return _exr_rgb(path, channels)


def _exr_rgb(path: Path, channels: dict[str, np.ndarray]) -> np.ndarray:
    """The colour out of an EXR's channels, however they were grouped."""
    for grouped in ("RGBA", "RGB"):
        if grouped in channels:
            return np.ascontiguousarray(channels[grouped][..., :3], dtype=np.float32)
    if all(name in channels for name in "RGB"):
        return np.stack([channels[name] for name in "RGB"], axis=-1).astype(np.float32)
    if "Y" in channels:
        grey = np.asarray(channels["Y"], dtype=np.float32)
        return np.repeat(grey[..., None], 3, axis=-1)
    raise EnvironmentLoadError(f"{path.name} has no RGB channels ({', '.join(channels)})")


def _read_hdr(data: bytes) -> np.ndarray:
    """Decode a Radiance RGBE picture: the header, the size line, the scanlines."""
    if not (data.startswith(b"#?RADIANCE") or data.startswith(b"#?RGBE")):
        raise EnvironmentLoadError("not a Radiance .hdr file")
    position = 0
    while True:
        end = data.find(b"\n", position)
        if end < 0:
            raise EnvironmentLoadError("the .hdr header never ends")
        line = data[position:end].strip()
        position = end + 1
        if line.startswith(b"FORMAT=") and line != b"FORMAT=32-bit_rle_rgbe":
            name = line[7:].decode(errors="replace")
            raise EnvironmentLoadError(f"unsupported .hdr format {name}")
        if not line:
            break
    end = data.find(b"\n", position)
    size = data[position:end].split()
    position = end + 1
    if len(size) != 4 or size[0] not in (b"-Y", b"+Y") or size[2] not in (b"+X", b"-X"):
        raise EnvironmentLoadError("unsupported .hdr orientation")
    height, width = int(size[1]), int(size[3])
    raw = np.frombuffer(data, dtype=np.uint8, offset=position)
    rgbe = np.empty((height, width, 4), dtype=np.uint8)
    offset = 0
    for row in range(height):
        head = raw[offset:offset + 4]
        if (
            8 <= width < 32768 and len(head) == 4 and head[0] == 2 and head[1] == 2
            and not head[2] & 0x80 and (int(head[2]) << 8 | int(head[3])) == width
        ):
            # The adaptive run-length scheme: each channel of the line on its
            # own, as runs (a count over 128, then one byte repeated) and
            # dumps (a count, then that many bytes).
            offset += 4
            for channel in range(4):
                out = rgbe[row, :, channel]
                x = 0
                while x < width:
                    count = int(raw[offset])
                    offset += 1
                    if count > 128:
                        count -= 128
                        out[x:x + count] = raw[offset]
                        offset += 1
                    else:
                        out[x:x + count] = raw[offset:offset + count]
                        offset += count
                    x += count
        else:
            # Flat: four bytes a pixel.
            line = raw[offset:offset + width * 4]
            if len(line) < width * 4:
                raise EnvironmentLoadError("the .hdr file is cut short")
            rgbe[row] = line.reshape(width, 4)
            offset += width * 4
    if size[0] == b"+Y":
        rgbe = rgbe[::-1]
    if size[2] == b"-X":
        rgbe = rgbe[:, ::-1]
    exponent = rgbe[..., 3].astype(np.int32)
    scale = np.where(exponent > 0, np.ldexp(1.0, exponent - 136), 0.0).astype(np.float32)
    return rgbe[..., :3].astype(np.float32) * scale[..., None]


# -- what the shaders need ---------------------------------------------------


def _halve(pixels: np.ndarray) -> np.ndarray:
    """Average each block of two by two; an odd last row or column is dropped."""
    h, w = pixels.shape[0] // 2 * 2, pixels.shape[1] // 2 * 2
    p = pixels[:h, :w]
    return 0.25 * (p[0::2, 0::2] + p[1::2, 0::2] + p[0::2, 1::2] + p[1::2, 1::2])


def downsized(pixels: np.ndarray, width: int) -> np.ndarray:
    """The panorama box-filtered down to at most ``width`` across, twice as wide as high."""
    result = np.asarray(pixels, dtype=np.float32)
    while result.shape[1] > width and result.shape[0] > 1:
        result = _halve(result)
    if result.shape[1] != width or result.shape[0] != width // 2:
        # Resample onto an exact 2:1 grid by area, so the tables below may
        # assume one.  Nearest-row and nearest-column after the halving is
        # within a texel of an area average and costs nothing.
        rows = np.minimum((np.arange(width // 2) + 0.5) * result.shape[0] / (width // 2),
                          result.shape[0] - 1).astype(int)
        cols = np.minimum((np.arange(width) + 0.5) * result.shape[1] / width,
                          result.shape[1] - 1).astype(int)
        result = result[rows][:, cols]
    return np.ascontiguousarray(result, dtype=np.float32)


def _row_directions(height: int, width: int) -> tuple[np.ndarray, np.ndarray]:
    """Texel-centre directions of an equirectangular grid, and the solid angle of each row."""
    v = (np.arange(height) + 0.5) / height
    u = (np.arange(width) + 0.5) / width
    uu, vv = np.meshgrid(u, v)
    directions = uv_to_direction(uu, vv)
    solid = (2.0 * math.pi / width) * (math.pi / height) * np.sin(v * math.pi)
    return directions, solid


#: Band weights of the clamped cosine, which turn radiance harmonics into
#: irradiance ones (Ramamoorthi and Hanrahan, 2001).
_COSINE_BANDS = np.array([math.pi] + [2.0 * math.pi / 3.0] * 3 + [math.pi / 4.0] * 5)


def sh_basis(directions: np.ndarray) -> np.ndarray:
    """The nine real spherical harmonics up to band two, at each direction."""
    d = np.asarray(directions, dtype=np.float64)
    x, y, z = d[..., 0], d[..., 1], d[..., 2]
    return np.stack([
        np.full_like(x, 0.282095),
        0.488603 * y, 0.488603 * z, 0.488603 * x,
        1.092548 * x * y, 1.092548 * y * z, 0.315392 * (3.0 * z * z - 1.0),
        1.092548 * x * z, 0.546274 * (x * x - y * y),
    ], axis=-1)


def irradiance_sh(pixels: np.ndarray) -> np.ndarray:
    """Nine irradiance coefficients per channel, ``(9, 3)``: E(n) = basis(n) @ coefficients."""
    small = downsized(pixels, SH_WIDTH)
    directions, solid = _row_directions(*small.shape[:2])
    basis = sh_basis(directions)                         # (h, w, 9)
    weighted = small * solid[:, None, None]              # radiance x solid angle
    radiance = np.einsum("hwk,hwc->kc", basis, weighted)
    return (radiance * _COSINE_BANDS[:, None]).astype(np.float32)


def evaluate_sh(coefficients: np.ndarray, directions: np.ndarray) -> np.ndarray:
    """Irradiance at unit ``directions`` from :func:`irradiance_sh` coefficients."""
    return sh_basis(directions) @ np.asarray(coefficients, dtype=np.float64)


def dominant_light(coefficients: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The direction and colour of the one distant light that best explains band one.

    A distant light of irradiance ``c`` from ``d`` puts ``c / 2 * dot(d, n)``
    into the first band of the irradiance, so the band's vector says which
    way the light comes from and twice its length how strong it is.  The
    colour is capped at the irradiance the whole map delivers facing that
    way, so the approximate shadow cast with it can never take away more
    light than there was.
    """
    c = np.asarray(coefficients, dtype=np.float64)
    # Band one is (y, z, x) in the basis above; put it back in (x, y, z).
    band = np.stack([c[3], c[1], c[2]], axis=0)
    luminance = band @ np.array([0.2126, 0.7152, 0.0722])
    length = float(np.linalg.norm(luminance))
    if length < 1e-9:
        return np.array([0.0, 1.0, 0.0]), np.zeros(3)
    direction = luminance / length
    # The first-band irradiance the map puts on a normal facing the light,
    # per channel; a single light would put exactly half its own there.
    facing = evaluate_sh(c, direction) - evaluate_sh(c, -direction)   # = 2 * band-one part
    color = np.maximum(facing, 0.0)                                    # 2 * (c / 2)
    total = np.maximum(evaluate_sh(c, direction), 0.0)
    return direction, np.minimum(color, total)


@dataclass
class SamplingTables:
    """What the tracer needs to pick directions in proportion to the light.

    ``radiance`` is the coarse map, ``(h, w, 3)``, each texel's radiance the
    average of the full map over it; ``density`` is the probability density
    of picking a point of each texel, over the unit square of panorama
    coordinates.  ``conditional`` holds, per row, the cumulative distribution
    across it (``w + 1`` entries from 0 to 1), and ``marginal`` the one down
    the rows (``h + 1`` entries).  A density over the sphere is the one over
    the square divided by ``2 pi^2 sin(theta)``.
    """

    radiance: np.ndarray
    density: np.ndarray
    conditional: np.ndarray
    marginal: np.ndarray

    def packed(self) -> tuple[np.ndarray, np.ndarray]:
        """Two RGBA32F tables: radiance and density per texel, then the distributions.

        The second is ``(h + 1, w + 1)``: row ``i < h`` is row ``i``'s
        conditional distribution in its red channel, and row ``h`` holds the
        marginal in the first ``h + 1`` texels.
        """
        h, w = self.density.shape
        texels = np.concatenate([self.radiance, self.density[..., None]], axis=-1)
        cdf = np.zeros((h + 1, w + 1, 4), dtype=np.float32)
        cdf[:h, :, 0] = self.conditional
        cdf[h, : h + 1, 0] = self.marginal
        return texels.astype(np.float32), cdf


def sampling_tables(pixels: np.ndarray) -> SamplingTables:
    """Build the importance-sampling distributions over a coarse copy of the map."""
    small = downsized(pixels, SAMPLING_WIDTH)
    h, w = small.shape[:2]
    luminance = small @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    sin_theta = np.sin((np.arange(h) + 0.5) / h * math.pi)
    # A floor under the dark texels, so every direction can still be picked:
    # a map that is black somewhere is not a promise that nothing arrives
    # from there once it has been rotated under a bright key.
    weights = (np.maximum(luminance, 0.0) + 1e-3 * max(float(luminance.mean()), 1e-6))
    weights = weights * sin_theta[:, None]
    rows = weights.sum(axis=1)
    total = float(rows.sum())
    conditional = np.zeros((h, w + 1), dtype=np.float64)
    conditional[:, 1:] = np.cumsum(weights, axis=1) / np.maximum(rows[:, None], 1e-30)
    conditional[:, -1] = 1.0
    marginal = np.zeros(h + 1, dtype=np.float64)
    marginal[1:] = np.cumsum(rows) / max(total, 1e-30)
    marginal[-1] = 1.0
    density = weights * (h * w) / max(total, 1e-30)
    return SamplingTables(
        radiance=small.astype(np.float32),
        density=density.astype(np.float32),
        conditional=conditional.astype(np.float32),
        marginal=marginal.astype(np.float32),
    )


@dataclass
class EnvironmentMap:
    """An HDRI read and made ready for the renderer.  Built off the thread."""

    #: Where it was read from.
    path: Path
    #: The panorama, top row first, at most :data:`MAX_RADIANCE_WIDTH` wide
    #: and clamped into what a half-float texture can carry.
    radiance: np.ndarray
    #: Irradiance harmonics, ``(9, 3)``; see :func:`irradiance_sh`.
    sh: np.ndarray
    #: The dominant light, in the map's frame: which way it comes from and
    #: the irradiance it delivers facing it.
    sun_direction: np.ndarray
    sun_color: np.ndarray
    sampling: SamplingTables
    #: The map's mean radiance, for the panel to say how bright it is.
    mean: float
    #: The irradiance, as a luminance, on a surface facing the dominant light:
    #: the brightest a matte surface can be lit by the map, near enough.
    peak: float

    @property
    def name(self) -> str:
        return self.path.stem

    @property
    def normalization(self) -> float:
        """What the radiance is multiplied by so that :attr:`peak` comes out at one.

        One is the irradiance the studio key delivers at its default, so a
        strength of one lights the model about as brightly as the rig it
        replaces, whatever the exposure the map was shot at.
        """
        return 1.0 / max(self.peak, 1e-6)


def prepare_environment(pixels: np.ndarray, path: str | Path = "environment") -> EnvironmentMap:
    """Everything :class:`EnvironmentMap` holds, from linear radiance ``(H, W, 3)``."""
    pixels = np.asarray(pixels, dtype=np.float32)
    # A NaN or an infinity from a badly written file would poison every
    # sum below, and a negative radiance is not light.
    pixels = np.nan_to_num(pixels, nan=0.0, posinf=HALF_MAX, neginf=0.0)
    pixels = np.maximum(pixels, 0.0)
    width = min(MAX_RADIANCE_WIDTH, 1 << int(math.floor(math.log2(max(pixels.shape[1], 4)))))
    radiance = np.minimum(downsized(pixels, width), HALF_MAX)
    sh = irradiance_sh(pixels)
    sun_direction, sun_color = dominant_light(sh)
    facing = np.maximum(evaluate_sh(sh, sun_direction), 0.0)
    peak = float(facing @ np.array([0.2126, 0.7152, 0.0722]))
    return EnvironmentMap(
        path=Path(path),
        radiance=radiance,
        sh=sh,
        sun_direction=sun_direction.astype(np.float32),
        sun_color=sun_color.astype(np.float32),
        sampling=sampling_tables(pixels),
        mean=float(pixels.mean()),
        peak=peak,
    )


def load_environment(path: str | Path) -> EnvironmentMap:
    """Read an HDRI from disk and prepare it; raises :class:`EnvironmentLoadError`."""
    path = Path(path)
    return prepare_environment(read_radiance(path), path)
