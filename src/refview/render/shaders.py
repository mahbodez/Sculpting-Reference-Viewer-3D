"""GLSL sources for the viewport.

Six small programs cover everything the viewer draws: a fullscreen background
gradient, the shaded mesh, a constant-colour pass reused for the wireframe and
the cut cap, the widened surface strokes, a depth-only pass that feeds both the
shadow map and the occlusion pre-pass, and the two fullscreen passes that turn
that depth into ambient occlusion.  The mesh shader branches on ``uMode``,
whose values mirror :attr:`refview.core.settings.ShadingMode.shader_id`.

Cross-section clipping is shared rather than duplicated: any fragment shader
that writes ``#pragma section`` gets the half-space test spliced in, so the
mesh, the wireframe, the annotations and the shadow map all disappear at the
cut together.

Lighting is deliberately evaluated in display space rather than linear space:
the colour swatches in the UI are what lands on screen, which is the
behaviour artists expect from a reference viewer.
"""

from __future__ import annotations

#: Up to two half-spaces; material past a plane's offset is cut away.
_SECTION_CLIP = """
uniform int uSectionCount;
uniform vec4 uSectionPlanes[2];

void clipSection(vec3 worldPosition) {
    for (int i = 0; i < uSectionCount; ++i) {
        if (dot(worldPosition, uSectionPlanes[i].xyz) > uSectionPlanes[i].w) {
            discard;
        }
    }
}
"""


def _with_section(source: str) -> str:
    """Splice the shared cross-section test into a fragment shader."""
    return source.replace("#pragma section", _SECTION_CLIP)


FULLSCREEN_VERTEX = """
#version 330 core

out vec2 vUv;

void main() {
    // Fullscreen triangle generated without any vertex buffer.
    vec2 corner = vec2(float((gl_VertexID << 1) & 2), float(gl_VertexID & 2));
    vUv = corner;
    gl_Position = vec4(corner * 2.0 - 1.0, 0.0, 1.0);
}
"""

BACKGROUND_VERTEX = FULLSCREEN_VERTEX

BACKGROUND_FRAGMENT = """
#version 330 core

in vec2 vUv;
out vec4 fragColor;

uniform vec3 uTopColor;
uniform vec3 uBottomColor;

void main() {
    fragColor = vec4(mix(uBottomColor, uTopColor, vUv.y), 1.0);
}
"""

MESH_VERTEX = """
#version 330 core

layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aNormal;

uniform mat4 uView;
uniform mat4 uProjection;
uniform mat3 uNormalMatrix;

out vec3 vViewPosition;
out vec3 vViewNormal;
out vec3 vWorldNormal;
out vec3 vWorldPosition;

void main() {
    vec4 viewPosition = uView * vec4(aPosition, 1.0);
    vViewPosition = viewPosition.xyz;
    vViewNormal = uNormalMatrix * aNormal;
    vWorldNormal = aNormal;
    vWorldPosition = aPosition;
    gl_Position = uProjection * viewPosition;
}
"""

MESH_FRAGMENT = _with_section("""
#version 330 core
#pragma section

const int MODE_MATCAP       = 0;
const int MODE_LAMBERT      = 1;
const int MODE_PHONG        = 2;
const int MODE_BLINN_PHONG  = 3;
const int MODE_PBR          = 4;
const int MODE_NORMALS      = 5;
const int MODE_HIGH_QUALITY = 6;

const float PI = 3.14159265359;

in vec3 vViewPosition;
in vec3 vViewNormal;
in vec3 vWorldNormal;
in vec3 vWorldPosition;

out vec4 fragColor;

uniform int  uMode;
uniform bool uFlatShading;
uniform bool uOrthographic;
uniform mat3 uNormalMatrix;

uniform bool  uPlaneShading;
uniform float uPlaneCellSize;
uniform bool  uPlaneContour;
uniform vec3  uPlaneContourColor;
uniform float uPlaneContourWidth;   // device pixels

uniform sampler2D uMatcap;
uniform float uMatcapRotation;
uniform float uMatcapContrast;
uniform float uMatcapGamma;
uniform float uMatcapBrightness;
uniform float uMatcapSaturation;
uniform vec3  uMatcapTint;
uniform bool  uMatcapFlipY;

uniform vec3  uKeyDirection;    // view space, surface -> light
uniform vec3  uFillDirection;   // view space, surface -> light
uniform vec3  uLightColor;
uniform float uKeyIntensity;
uniform float uFillIntensity;
uniform vec3  uAmbientColor;
uniform float uAmbientIntensity;

uniform vec3  uDiffuseColor;
uniform vec3  uSpecularColor;
uniform float uSpecularLevel;
uniform float uShininess;
uniform float uMetalness;
uniform float uRoughness;
uniform vec3  uReflectionColor;

uniform sampler2D uShadowMap;
uniform sampler2D uOcclusion;
uniform mat4  uLightViewProjection;
uniform vec2  uViewportSize;
uniform float uShadowStrength;
uniform float uShadowSoftness;
uniform float uShadowBias;
uniform bool  uUseShadow;
uniform bool  uUseOcclusion;

//: World-space shading normal, written by shadingNormal() and read by the
//: ambient term so that the sky gradient breaks into planes along with the
//: rest of the shading.
vec3 gWorldNormal;

float luminance(vec3 color) {
    return dot(color, vec3(0.2126, 0.7152, 0.0722));
}

vec3 planeNormal(vec3 n) {
    // The direction is pushed out onto the cube around the origin and its two
    // sideways components are rounded to a grid, so the centre of the cell it
    // lands in becomes the plane's direction.
    //
    // The grid is anchored on zero rather than divided into a whole number of
    // cells.  That keeps a plane square on each axis -- the front, the side
    // and the top an artist blocks a form in with -- and keeps the cells
    // symmetric, so a back face quantises to the negation of what its front
    // does and the two stay parallel.  It also lets the cell size vary
    // continuously: a full-width cell leaves the six axis planes, and
    // shrinking it grows bevels off their corners rather than jumping
    // straight to the next whole count of planes.
    float cellSize = max(uPlaneCellSize, 1e-3);
    vec3 magnitude = abs(n);
    float widest = max(magnitude.x, max(magnitude.y, magnitude.z));
    vec3 face = n / max(widest, 1e-6);
    // Exactly one axis owns the face even where two components tie, so a
    // direction sitting on the seam between two faces falls into one of them
    // instead of into a bevel of its own.
    vec3 dominant = magnitude.x >= widest ? vec3(1.0, 0.0, 0.0)
                  : (magnitude.y >= widest ? vec3(0.0, 1.0, 0.0) : vec3(0.0, 0.0, 1.0));
    // Clamped, so a cell overhanging the edge of the face becomes the bevel
    // along that edge instead of a direction off the cube altogether.
    vec3 cell = clamp(round(face / cellSize) * cellSize, -1.0, 1.0);
    // The component that chose the face stays out at the face itself,
    // otherwise every direction would pull in towards the cube's centre.
    return normalize(mix(cell, sign(face), dominant));
}

float planeContour(vec3 n) {
    // A plane boundary is a line of the quantisation grid, so it can be drawn
    // from the grid itself rather than found by comparing pixels: the distance
    // to the nearest cell edge, divided by how far the cell coordinate travels
    // in one pixel, is a distance in pixels, and that gives a line of an even
    // width at any zoom.
    //
    // The smooth normal is used even when flat shading is on, so that the
    // lines follow the turn of the form rather than the triangulation.
    float cellSize = max(uPlaneCellSize, 1e-3);
    vec3 magnitude = abs(n);
    float widest = max(magnitude.x, max(magnitude.y, magnitude.z));
    vec3 face = n / max(widest, 1e-6);
    vec3 coordinate = face / cellSize;
    vec3 travel = max(fwidth(coordinate), vec3(1e-6));         // cells per pixel
    // Cell centres sit on the whole numbers, so the edges are the halves.
    vec3 toEdge = abs(fract(coordinate) - 0.5) / travel;       // pixels

    // The axis that owns the face carries no grid of its own: its component is
    // pinned at the face.
    vec3 dominant = magnitude.x >= widest ? vec3(1.0, 0.0, 0.0)
                  : (magnitude.y >= widest ? vec3(0.0, 1.0, 0.0) : vec3(0.0, 0.0, 1.0));
    toEdge = mix(toEdge, vec3(1e6), dominant);

    // The seam where the owning axis changes -- an edge of the cube -- is a
    // boundary as well, but only when the outermost cell falls short of the
    // edge of the face.  When it reaches the edge, the two faces meeting there
    // quantise to the same direction and the surface runs on through.
    float middle = magnitude.x + magnitude.y + magnitude.z - widest
                 - min(magnitude.x, min(magnitude.y, magnitude.z));
    float seam = (1.0 - middle / max(widest, 1e-6)) / cellSize;
    float seamTravel = max(fwidth(seam), 1e-6);
    float seamJumps = 1.0 - step(1.0, round((1.0 - 1e-4) / cellSize) * cellSize);

    // Where the planes are themselves down to a pixel or two -- around the
    // silhouette, or at the fine end of the slider -- the lines would crowd
    // into a solid mass, so they fade out rather than flood the surface.
    float halfWidth = max(uPlaneContourWidth, 0.0) * 0.5;
    vec3 covered = 1.0 - smoothstep(vec3(halfWidth - 0.5), vec3(halfWidth + 0.5), toEdge);
    covered *= 1.0 - smoothstep(vec3(0.25), vec3(0.75), travel);
    float onSeam = (1.0 - smoothstep(halfWidth - 0.5, halfWidth + 0.5, seam / seamTravel))
                 * (1.0 - smoothstep(0.25, 0.75, seamTravel)) * seamJumps;
    float ink = max(max(covered.x, max(covered.y, covered.z)), onSeam);
    return clamp(ink, 0.0, 1.0);
}

vec3 shadingNormal(vec3 viewDir) {
    vec3 n;
    if (uPlaneShading) {
        // Quantised in object space and rotated into view space afterwards,
        // so the planes stay locked to the form while the camera orbits it.
        vec3 world = uFlatShading
            ? normalize(cross(dFdx(vWorldPosition), dFdy(vWorldPosition)))
            : normalize(vWorldNormal);
        gWorldNormal = planeNormal(world);
        n = normalize(uNormalMatrix * gWorldNormal);
    } else {
        gWorldNormal = normalize(vWorldNormal);
        n = uFlatShading
            ? normalize(cross(dFdx(vViewPosition), dFdy(vViewPosition)))
            : normalize(vViewNormal);
    }
    return dot(n, viewDir) < 0.0 ? -n : n;
}

vec3 gradeMatcap(vec3 color) {
    color = pow(max(color, vec3(0.0)), vec3(1.0 / max(uMatcapGamma, 0.01)));
    color = (color - 0.5) * uMatcapContrast + 0.5;
    color = mix(vec3(luminance(color)), color, uMatcapSaturation);
    return max(color * uMatcapBrightness * uMatcapTint, vec3(0.0));
}

vec3 sampleMatcap(vec3 n, vec3 viewDir) {
    // Reflection-vector lookup: stays stable off-centre and under wide FOVs.
    vec3 r = reflect(-viewDir, n);
    float c = cos(uMatcapRotation);
    float s = sin(uMatcapRotation);
    vec2 rotated = vec2(r.x * c - r.y * s, r.x * s + r.y * c);
    float m = 2.0 * sqrt(dot(rotated, rotated) + (r.z + 1.0) * (r.z + 1.0));
    vec2 uv = rotated / max(m, 1e-4) + 0.5;
    if (uMatcapFlipY) {
        uv.y = 1.0 - uv.y;
    }
    return gradeMatcap(texture(uMatcap, uv).rgb);
}

vec3 ambientTerm() {
    // Hemispherical ambient keyed off the world normal, so the underside of
    // the model stays readable without washing out the top.
    float sky = gWorldNormal.y * 0.5 + 0.5;
    return uAmbientColor * uAmbientIntensity * mix(0.35, 1.0, sky);
}

float shadowFactor(float ndl) {
    // Percentage-closer filtering over a 5x5 tap grid.  Widening the grid is
    // what makes the edge soft; the softness slider scales the tap spacing.
    if (!uUseShadow) {
        return 1.0;
    }
    vec4 lightClip = uLightViewProjection * vec4(vWorldPosition, 1.0);
    vec3 coords = lightClip.xyz / lightClip.w * 0.5 + 0.5;
    if (coords.z > 1.0 || any(lessThan(coords.xy, vec2(0.0)))
        || any(greaterThan(coords.xy, vec2(1.0)))) {
        return 1.0;
    }
    float bias = uShadowBias * (1.0 + 3.0 * (1.0 - ndl));
    vec2 texel = max(uShadowSoftness, 0.0) / vec2(textureSize(uShadowMap, 0));
    float lit = 0.0;
    for (int y = -2; y <= 2; ++y) {
        for (int x = -2; x <= 2; ++x) {
            float depth = texture(uShadowMap, coords.xy + vec2(x, y) * texel).r;
            lit += coords.z - bias <= depth ? 1.0 : 0.0;
        }
    }
    return mix(1.0, lit / 25.0, clamp(uShadowStrength, 0.0, 1.0));
}

float occlusionFactor() {
    if (!uUseOcclusion) {
        return 1.0;
    }
    return texture(uOcclusion, gl_FragCoord.xy / uViewportSize).r;
}

float specularPhong(vec3 n, vec3 l, vec3 v) {
    return pow(max(dot(reflect(-l, n), v), 0.0), max(uShininess, 1.0));
}

float specularBlinn(vec3 n, vec3 l, vec3 v) {
    return pow(max(dot(n, normalize(l + v)), 0.0), max(uShininess, 1.0) * 4.0);
}

vec3 analyticShade(vec3 n, vec3 v, int mode, bool shadowed, float ao) {
    // The high-quality mode shades through here as well, so that turning it on
    // keeps the brightness the light panel was tuned for and only adds the
    // shadow on the key light and the occlusion on the ambient and diffuse.
    vec3 color = uDiffuseColor * ambientTerm() * ao;
    // Occlusion belongs to the ambient term, but a cavity also catches less of
    // a broad studio light, so half of it carries into the direct diffuse.
    float diffuseAo = mix(1.0, ao, 0.5);
    vec3 directions[2] = vec3[2](uKeyDirection, uFillDirection);
    float intensities[2] = float[2](uKeyIntensity, uFillIntensity);

    for (int i = 0; i < 2; ++i) {
        vec3 l = normalize(directions[i]);
        float ndl = max(dot(n, l), 0.0);
        if (ndl <= 0.0 || intensities[i] <= 0.0) {
            continue;
        }
        // Only the key light casts: a fill that also cast would fight it and
        // needs a second map for no gain in a reference view.
        float visibility = (shadowed && i == 0) ? shadowFactor(ndl) : 1.0;
        vec3 radiance = uLightColor * intensities[i] * visibility;
        color += uDiffuseColor * ndl * radiance * diffuseAo;
        if (mode == MODE_PHONG) {
            color += uSpecularColor * uSpecularLevel * specularPhong(n, l, v) * radiance;
        } else if (mode == MODE_BLINN_PHONG || mode == MODE_HIGH_QUALITY) {
            color += uSpecularColor * uSpecularLevel * specularBlinn(n, l, v) * radiance;
        }
    }
    return color;
}

float distributionGGX(float ndh, float alpha) {
    float a2 = alpha * alpha;
    float d = ndh * ndh * (a2 - 1.0) + 1.0;
    return a2 / max(PI * d * d, 1e-6);
}

float geometrySmith(float ndv, float ndl, float alpha) {
    float k = alpha * 0.5;
    float gv = ndv / max(ndv * (1.0 - k) + k, 1e-6);
    float gl = ndl / max(ndl * (1.0 - k) + k, 1e-6);
    return gv * gl;
}

vec3 fresnelSchlick(vec3 f0, float cosine) {
    return f0 + (1.0 - f0) * pow(clamp(1.0 - cosine, 0.0, 1.0), 5.0);
}

vec3 pbrShade(vec3 n, vec3 v) {
    float alpha = max(uRoughness * uRoughness, 1e-3);
    vec3 f0 = mix(vec3(0.16 * uSpecularLevel) * uSpecularColor, uDiffuseColor, uMetalness);
    f0 *= uReflectionColor;
    vec3 albedo = uDiffuseColor * (1.0 - uMetalness);
    float ndv = max(dot(n, v), 1e-4);

    vec3 ambient = ambientTerm();
    vec3 color = albedo * ambient + f0 * ambient * (1.0 - uRoughness);

    vec3 directions[2] = vec3[2](uKeyDirection, uFillDirection);
    float intensities[2] = float[2](uKeyIntensity, uFillIntensity);
    for (int i = 0; i < 2; ++i) {
        vec3 l = normalize(directions[i]);
        float ndl = max(dot(n, l), 0.0);
        if (ndl <= 0.0 || intensities[i] <= 0.0) {
            continue;
        }
        vec3 h = normalize(l + v);
        vec3 fresnel = fresnelSchlick(f0, max(dot(v, h), 0.0));
        float specular = distributionGGX(max(dot(n, h), 0.0), alpha)
                       * geometrySmith(ndv, ndl, alpha)
                       / max(4.0 * ndv * ndl, 1e-4);
        vec3 diffuse = albedo * (1.0 - fresnel) / PI;
        color += (diffuse + fresnel * specular) * uLightColor * intensities[i] * ndl;
    }
    return color;
}

void main() {
    clipSection(vWorldPosition);

    vec3 v = uOrthographic ? vec3(0.0, 0.0, 1.0) : normalize(-vViewPosition);
    vec3 n = shadingNormal(v);

    vec3 color;
    if (uMode == MODE_MATCAP) {
        color = sampleMatcap(n, v);
    } else if (uMode == MODE_NORMALS) {
        color = n * 0.5 + 0.5;
    } else if (uMode == MODE_HIGH_QUALITY) {
        color = analyticShade(n, v, uMode, uUseShadow, occlusionFactor());
    } else if (uMode == MODE_PBR) {
        color = pbrShade(n, v);
    } else {
        color = analyticShade(n, v, uMode, false, 1.0);
    }
    if (uPlaneShading && uPlaneContour) {
        // Both flags are uniform, so the derivatives inside stay well defined.
        color = mix(color, uPlaneContourColor, planeContour(normalize(vWorldNormal)));
    }
    fragColor = vec4(max(color, vec3(0.0)), 1.0);
}
""")

FLAT_VERTEX = """
#version 330 core

layout(location = 0) in vec3 aPosition;

uniform mat4 uView;
uniform mat4 uProjection;

out vec3 vWorldPosition;

void main() {
    vWorldPosition = aPosition;
    gl_Position = uProjection * uView * vec4(aPosition, 1.0);
}
"""

FLAT_FRAGMENT = _with_section("""
#version 330 core
#pragma section

in vec3 vWorldPosition;
out vec4 fragColor;
uniform vec4 uColor;

void main() {
    clipSection(vWorldPosition);
    fragColor = uColor;
}
""")

DEPTH_VERTEX = """
#version 330 core

// Feeds both the shadow map and the occlusion pre-pass.  The shadow pass wants
// only the depth; the occlusion pass also wants the surface normal, which is
// far steadier than one reconstructed from the depth buffer's derivatives.

layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aNormal;

uniform mat4 uView;
uniform mat4 uProjection;
uniform mat3 uNormalMatrix;

out vec3 vWorldPosition;
out vec3 vViewNormal;

void main() {
    vWorldPosition = aPosition;
    vViewNormal = uNormalMatrix * aNormal;
    gl_Position = uProjection * uView * vec4(aPosition, 1.0);
}
"""

DEPTH_FRAGMENT = _with_section("""
#version 330 core
#pragma section

in vec3 vWorldPosition;
in vec3 vViewNormal;

out vec4 fragNormal;

void main() {
    clipSection(vWorldPosition);
    fragNormal = vec4(normalize(vViewNormal) * 0.5 + 0.5, 1.0);
}
""")

STROKE_VERTEX = """
#version 330 core

// Thick surface strokes.  Each segment arrives as two triangles whose corners
// carry both of the segment's endpoints; the shader projects them, works out
// the screen-space direction and pushes each corner sideways by half the brush
// width.  Doing the widening here keeps the line thickness in pixels at any
// zoom, which glLineWidth cannot promise on a core profile.

layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aOther;
layout(location = 2) in vec3 aNormal;
layout(location = 3) in vec3 aColor;
layout(location = 4) in float aSide;
layout(location = 5) in float aWidth;

uniform mat4 uViewProjection;
uniform vec2 uViewport;      // drawable size in device pixels
uniform float uWidthScale;   // device pixels per logical pixel
uniform float uNormalOffset; // world units lifted off the surface
uniform float uDepthBias;    // extra nudge towards the viewer, in NDC

out vec3 vColor;
out vec3 vWorldPosition;

vec2 to_screen(vec4 clip) {
    float w = abs(clip.w) < 1e-6 ? 1e-6 : clip.w;
    return clip.xy / w * uViewport * 0.5;
}

void main() {
    vWorldPosition = aPosition + aNormal * uNormalOffset;
    vec4 clip = uViewProjection * vec4(vWorldPosition, 1.0);
    vec4 other = uViewProjection * vec4(aOther + aNormal * uNormalOffset, 1.0);

    vec2 delta = to_screen(other) - to_screen(clip);
    float travel = length(delta);
    vec2 direction = travel > 1e-5 ? delta / travel : vec2(1.0, 0.0);
    float half_width = max(aWidth * uWidthScale, 1.0) * 0.5;

    // Sideways for the ribbon, backwards for a cap that also fills the joins.
    vec2 offset = vec2(-direction.y, direction.x) * (aSide * half_width)
                - direction * half_width;

    float w = abs(clip.w) < 1e-6 ? 1e-6 : clip.w;
    clip.xy += offset / (uViewport * 0.5) * w;
    clip.z -= uDepthBias * w;
    gl_Position = clip;
    vColor = aColor;
}
"""

STROKE_FRAGMENT = _with_section("""
#version 330 core
#pragma section

in vec3 vColor;
in vec3 vWorldPosition;
out vec4 fragColor;

void main() {
    clipSection(vWorldPosition);
    fragColor = vec4(vColor, 1.0);
}
""")

OCCLUSION_FRAGMENT = """
#version 330 core

// Screen-space ambient occlusion.  The scene's depth is rendered first; this
// pass reconstructs each pixel's view-space position from it, samples a
// hemisphere around that point and counts how many of those samples land
// behind geometry.  It is an approximation, but it costs one fullscreen pass
// and reads the cavities of a sculpt the way a soft studio light would.

in vec2 vUv;
out vec4 fragColor;

uniform sampler2D uDepth;
uniform sampler2D uNormals;
uniform mat4 uProjection;
uniform mat4 uInverseProjection;
uniform vec2 uViewportSize;
uniform float uRadius;
uniform float uIntensity;

const int SAMPLE_COUNT = 16;
const vec3 KERNEL[16] = vec3[16](
    vec3( 0.5381,  0.1856, 0.4319), vec3( 0.1379,  0.2486, 0.4430),
    vec3( 0.3371,  0.5679, 0.0057), vec3(-0.6999, -0.0451, 0.0019),
    vec3( 0.0689, -0.1598, 0.8547), vec3( 0.0560,  0.0069, 0.1843),
    vec3(-0.0146,  0.1402, 0.0762), vec3( 0.0100, -0.1924, 0.0344),
    vec3(-0.3577, -0.5301, 0.4358), vec3(-0.3169,  0.1063, 0.0158),
    vec3( 0.0103, -0.5869, 0.0046), vec3(-0.0897, -0.4940, 0.3287),
    vec3( 0.7119, -0.0154, 0.0918), vec3(-0.0533,  0.0596, 0.5411),
    vec3( 0.0352, -0.0631, 0.5460), vec3(-0.4776,  0.2847, 0.0271)
);

vec3 viewPosition(vec2 uv) {
    float depth = texture(uDepth, uv).r * 2.0 - 1.0;
    vec4 clip = uInverseProjection * vec4(uv * 2.0 - 1.0, depth, 1.0);
    return clip.xyz / clip.w;
}

float hash(vec2 seed) {
    return fract(sin(dot(seed, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
    if (texture(uDepth, vUv).r >= 1.0) {
        fragColor = vec4(1.0);  // background
        return;
    }
    vec3 origin = viewPosition(vUv);
    vec3 normal = normalize(texture(uNormals, vUv).xyz * 2.0 - 1.0);
    if (normal.z < 0.0) {
        normal = -normal;  // A back face still occludes towards the viewer.
    }
    // Step off the surface before sampling and compare with a tolerance that
    // grows with distance: without both, a plane seen at a grazing angle
    // occludes itself wherever the depth comparison rounds the wrong way.
    origin += normal * uRadius * 0.05;
    float bias = max(uRadius * 0.02, abs(origin.z) * 0.002);

    float angle = hash(vUv * uViewportSize) * 6.2831853;
    mat2 turn = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));

    float occluded = 0.0;
    for (int i = 0; i < SAMPLE_COUNT; ++i) {
        vec3 offset = normalize(KERNEL[i]);
        offset.xy = turn * offset.xy;
        if (dot(offset, normal) < 0.0) {
            offset = -offset;
        }
        // Spread the probes from close in to the full radius: the near ones
        // catch contact shading, the far ones the shape of the whole cavity.
        float reach = mix(0.25, 1.0, float(i) / float(SAMPLE_COUNT - 1));
        vec3 probe = origin + offset * uRadius * reach;
        vec4 clip = uProjection * vec4(probe, 1.0);
        vec2 uv = clip.xy / clip.w * 0.5 + 0.5;
        if (any(lessThan(uv, vec2(0.0))) || any(greaterThan(uv, vec2(1.0)))) {
            continue;
        }
        float sceneDepth = viewPosition(uv).z;
        if (sceneDepth >= probe.z + bias) {
            // Ignore a hit that is far closer than the radius: that is a
            // different surface in front, not a cavity wall.
            occluded += smoothstep(0.0, 1.0, uRadius / max(abs(origin.z - sceneDepth), 1e-4));
        }
    }
    // A raw hemisphere count peaks around a third even in a tight corner, so
    // the strength is applied as an exponent: it deepens the mid tones instead
    // of merely scaling a value that never got large.
    float open = clamp(1.0 - occluded / float(SAMPLE_COUNT), 0.0, 1.0);
    fragColor = vec4(vec3(pow(open, max(uIntensity, 0.0) * 3.0)), 1.0);
}
"""

BLUR_FRAGMENT = """
#version 330 core

// A 4x4 box blur, which is enough to hide the per-pixel rotation the
// occlusion pass uses to get away with only sixteen samples.

in vec2 vUv;
out vec4 fragColor;

uniform sampler2D uSource;

void main() {
    vec2 texel = 1.0 / vec2(textureSize(uSource, 0));
    float total = 0.0;
    for (int y = -2; y < 2; ++y) {
        for (int x = -2; x < 2; ++x) {
            total += texture(uSource, vUv + vec2(x, y) * texel).r;
        }
    }
    fragColor = vec4(vec3(total / 16.0), 1.0);
}
"""
