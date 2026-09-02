"""GLSL sources for the viewport.

Three small programs cover everything the viewer draws: a fullscreen
background gradient, the shaded mesh, and a constant-colour pass reused for
the wireframe overlay.  The mesh shader branches on ``uMode``, whose values
mirror :attr:`refview.core.settings.ShadingMode.shader_id`.

Lighting is deliberately evaluated in display space rather than linear space:
the colour swatches in the UI are what lands on screen, which is the
behaviour artists expect from a reference viewer.
"""

from __future__ import annotations

BACKGROUND_VERTEX = """
#version 330 core

out vec2 vUv;

void main() {
    // Fullscreen triangle generated without any vertex buffer.
    vec2 corner = vec2(float((gl_VertexID << 1) & 2), float(gl_VertexID & 2));
    vUv = corner;
    gl_Position = vec4(corner * 2.0 - 1.0, 0.0, 1.0);
}
"""

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

void main() {
    vec4 viewPosition = uView * vec4(aPosition, 1.0);
    vViewPosition = viewPosition.xyz;
    vViewNormal = uNormalMatrix * aNormal;
    vWorldNormal = aNormal;
    gl_Position = uProjection * viewPosition;
}
"""

MESH_FRAGMENT = """
#version 330 core

const int MODE_MATCAP      = 0;
const int MODE_LAMBERT     = 1;
const int MODE_PHONG       = 2;
const int MODE_BLINN_PHONG = 3;
const int MODE_PBR         = 4;
const int MODE_NORMALS     = 5;

const float PI = 3.14159265359;

in vec3 vViewPosition;
in vec3 vViewNormal;
in vec3 vWorldNormal;

out vec4 fragColor;

uniform int  uMode;
uniform bool uFlatShading;
uniform bool uOrthographic;

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

float luminance(vec3 color) {
    return dot(color, vec3(0.2126, 0.7152, 0.0722));
}

vec3 shadingNormal(vec3 viewDir) {
    vec3 n = uFlatShading
        ? normalize(cross(dFdx(vViewPosition), dFdy(vViewPosition)))
        : normalize(vViewNormal);
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
    float sky = vWorldNormal.y * 0.5 + 0.5;
    return uAmbientColor * uAmbientIntensity * mix(0.35, 1.0, sky);
}

float specularPhong(vec3 n, vec3 l, vec3 v) {
    return pow(max(dot(reflect(-l, n), v), 0.0), max(uShininess, 1.0));
}

float specularBlinn(vec3 n, vec3 l, vec3 v) {
    return pow(max(dot(n, normalize(l + v)), 0.0), max(uShininess, 1.0) * 4.0);
}

vec3 analyticShade(vec3 n, vec3 v, int mode) {
    vec3 color = uDiffuseColor * ambientTerm();
    vec3 directions[2] = vec3[2](uKeyDirection, uFillDirection);
    float intensities[2] = float[2](uKeyIntensity, uFillIntensity);

    for (int i = 0; i < 2; ++i) {
        vec3 l = normalize(directions[i]);
        float ndl = max(dot(n, l), 0.0);
        if (ndl <= 0.0 || intensities[i] <= 0.0) {
            continue;
        }
        vec3 radiance = uLightColor * intensities[i];
        color += uDiffuseColor * ndl * radiance;
        if (mode == MODE_PHONG) {
            color += uSpecularColor * uSpecularLevel * specularPhong(n, l, v) * radiance;
        } else if (mode == MODE_BLINN_PHONG) {
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
    vec3 v = uOrthographic ? vec3(0.0, 0.0, 1.0) : normalize(-vViewPosition);
    vec3 n = shadingNormal(v);

    vec3 color;
    if (uMode == MODE_MATCAP) {
        color = sampleMatcap(n, v);
    } else if (uMode == MODE_NORMALS) {
        color = n * 0.5 + 0.5;
    } else if (uMode == MODE_PBR) {
        color = pbrShade(n, v);
    } else {
        color = analyticShade(n, v, uMode);
    }
    fragColor = vec4(max(color, vec3(0.0)), 1.0);
}
"""

FLAT_VERTEX = """
#version 330 core

layout(location = 0) in vec3 aPosition;

uniform mat4 uView;
uniform mat4 uProjection;

void main() {
    gl_Position = uProjection * uView * vec4(aPosition, 1.0);
}
"""

FLAT_FRAGMENT = """
#version 330 core

out vec4 fragColor;
uniform vec4 uColor;

void main() {
    fragColor = uColor;
}
"""

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

vec2 to_screen(vec4 clip) {
    float w = abs(clip.w) < 1e-6 ? 1e-6 : clip.w;
    return clip.xy / w * uViewport * 0.5;
}

void main() {
    vec4 clip = uViewProjection * vec4(aPosition + aNormal * uNormalOffset, 1.0);
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

STROKE_FRAGMENT = """
#version 330 core

in vec3 vColor;
out vec4 fragColor;

void main() {
    fragColor = vec4(vColor, 1.0);
}
"""
