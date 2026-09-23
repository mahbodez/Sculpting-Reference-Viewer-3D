#version 330 core
#include "section.glsl"
#include "environment.glsl"

const int MODE_MATCAP       = 0;
const int MODE_LAMBERT      = 1;
const int MODE_PHONG        = 2;
const int MODE_BLINN_PHONG  = 3;
const int MODE_PBR          = 4;
const int MODE_NORMALS      = 5;
const int MODE_HIGH_QUALITY = 6;
const int MODE_CONTOUR      = 7;
const int MODE_HUMAN_SKIN   = 8;

// Grid is the one mode that quantises against something other than a fitted
// set of planes; the rest differ only in how that set was arrived at.
const int PLANE_GRID = 0;

const float PI = 3.14159265359;

in vec3 vViewPosition;
in vec3 vViewNormal;
in vec3 vWorldNormal;
in vec3 vWorldPosition;

out vec4 fragColor;
//: The second half of the ghost's running total -- see ``uAccumulate``.  The
//: frame itself has no attachment there, so on an ordinary pass this write
//: goes nowhere, which is cheaper than compiling the shader twice.
layout(location = 1) out vec4 fragReveal;

uniform int  uMode;
uniform bool uFlatShading;
uniform bool uOrthographic;
uniform mat3 uNormalMatrix;

uniform bool  uPlaneShading;
uniform int   uPlaneMode;
uniform float uPlaneCellSize;
//: The fitted planes, two texels apiece: row 0 is (direction.xyz, offset) and
//: row 1 is (anchor.xyz, unused).  A table rather than a uniform array so that
//: how many planes there can be is not a question about the driver.
uniform sampler2D uPlaneTable;
uniform int   uPlaneAxisCount;
uniform vec3  uPlaneOrigin;         // world point the normalised frame is about
uniform float uPlaneScale;          // world units -> normalised units
uniform float uPlaneLocality;       // weight on being in the same place
uniform float uPlaneCoplanar;       // weight on lying in the same plane
uniform float uPlaneSpan;           // radians of turn per plane
uniform bool  uPlaneContour;
uniform vec3  uPlaneContourColor;
uniform float uPlaneContourWidth;   // device pixels

//: The contour mode's stack of slicing planes: which way they face (world
//: space, unit length), how far apart they are in world units, how thick
//: their lines are in device pixels, and what is painted on either side.
uniform vec3  uSliceDirection;
uniform float uSliceSpacing;
uniform float uSliceWidth;
uniform vec3  uSliceColor;
uniform vec3  uSlicePaper;
uniform bool  uSliceLit;

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
uniform float uOpacity;
//: Sum this fragment into the two order-independent buffers rather than
//: writing it straight into the frame.  See ``ghostWeight`` below.
uniform bool  uAccumulate;
//: View depth at which the form begins, and how deep it is, so a fragment can
//: say how far through the form it lies.
uniform float uGhostNear;
uniform float uGhostSpan;
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

void planeScores(
    vec3 n, vec3 world, out int nearest, out int runnerUp, out float best, out float second
) {
    // The planes were fitted to this model, so there is no grid to round
    // against: a fragment belongs to whichever plane is nearest it.  Nearest
    // is measured in the space the fit was made in -- how nearly the fragment
    // faces the way the plane does, how far it is from where the plane sits,
    // and how far it is from lying in the plane -- so the boundaries the
    // shader draws are the boundaries between the clusters that were found.
    //
    // A fit made only of directions sets both weights to zero, which leaves
    // the nearest direction and nothing else, exactly as before.
    vec3 p = (world - uPlaneOrigin) * uPlaneScale;
    float lie = dot(p, n);
    nearest = 0;
    runnerUp = 0;
    best = -1e30;
    second = -1e30;
    for (int i = 0; i < @MAX_PLANE_AXES@; ++i) {
        if (i >= uPlaneAxisCount) {
            break;
        }
        vec4 plane = texelFetch(uPlaneTable, ivec2(i, 0), 0);
        vec3 anchor = texelFetch(uPlaneTable, ivec2(i, 1), 0).xyz;
        vec3 facing = n - plane.xyz;
        vec3 across = p - anchor;
        float depth = lie - plane.w;
        float score = -(dot(facing, facing)
                      + uPlaneLocality * dot(across, across)
                      + uPlaneCoplanar * depth * depth);
        if (score > best) {
            second = best;
            runnerUp = nearest;
            best = score;
            nearest = i;
        } else if (score > second) {
            second = score;
            runnerUp = i;
        }
    }
}

vec3 planeAxisNormal(vec3 n, vec3 world) {
    if (uPlaneAxisCount < 2) {
        return n;   // No model to fit, or a model with only one plane in it.
    }
    int nearest;
    int runnerUp;
    float best;
    float second;
    planeScores(n, world, nearest, runnerUp, best, second);
    return normalize(texelFetch(uPlaneTable, ivec2(nearest, 0), 0).xyz);
}

float planeAxisContour(vec3 n, vec3 world) {
    // A fragment sits on a boundary exactly where the two nearest planes are
    // equally near, so the gap between the best and the second best is a
    // signed distance to the seam.  Dividing it by how fast it changes in one
    // pixel turns it into a distance in pixels, which is what gives a line of
    // an even width at any zoom -- the same reasoning as the grid mode's, on a
    // quantity that does not need a grid to exist.  Two planes that differ in
    // where they sit and not only in which way they face still have a gap that
    // moves across the surface, so the seam between them is found the same way.
    if (uPlaneAxisCount < 2) {
        return 0.0;
    }
    int nearest;
    int runnerUp;
    float best;
    float second;
    planeScores(n, world, nearest, runnerUp, best, second);
    float gap = best - second;
    float travel = max(fwidth(gap), 1e-6);
    float halfWidth = max(uPlaneContourWidth, 0.0) * 0.5;
    float ink = 1.0 - smoothstep(halfWidth - 0.5, halfWidth + 0.5, gap / travel);
    // Where a plane is down to a pixel or two -- around the silhouette, or with
    // the slider far to the right -- the lines would crowd into a solid mass,
    // so they fade instead.  The normal turning by more than a plane's worth
    // inside one pixel is what says that has happened.
    float turn = length(fwidth(n)) / max(uPlaneSpan, 1e-4);
    ink *= 1.0 - smoothstep(0.25, 0.75, turn);
    // Two planes can meet without the form turning at all: a fit that reads
    // where the surface is will divide a broad flat between two planes facing
    // the same way, and the shading runs straight through the join.  A line
    // there would say the form turns where it does not, so the line is only
    // drawn to the extent that the two planes really do face apart.
    float apart = 1.0 - dot(texelFetch(uPlaneTable, ivec2(nearest, 0), 0).xyz,
                            texelFetch(uPlaneTable, ivec2(runnerUp, 0), 0).xyz);
    ink *= smoothstep(0.0005, 0.0040, apart);   // about 2 to 5 degrees
    return clamp(ink, 0.0, 1.0);
}

vec3 contourShade(vec3 n, vec3 v) {
    // Where a stack of evenly spaced planes cuts the surface.  The fragment's
    // height along the stack, in planes, is a coordinate that runs through a
    // whole number at every cut; how far it moves in one pixel gives the
    // distance to the nearest cut in pixels, and that draws a line of an even
    // width at any zoom and any angle.  Where the surface runs along the
    // planes the coordinate barely moves and the lines spread out; where it
    // turns across them they crowd -- which is what the mode is for.
    float height = dot(vWorldPosition, uSliceDirection) / max(uSliceSpacing, 1e-9);
    float travel = max(fwidth(height), 1e-6);                  // planes per pixel
    float toCut = abs(fract(height + 0.5) - 0.5) / travel;      // pixels
    float halfWidth = max(uSliceWidth, 0.0) * 0.5;
    float ink = 1.0 - smoothstep(halfWidth - 0.5, halfWidth + 0.5, toCut);
    // Down to a pixel or two apart the lines would flood the surface, so they
    // fade to a tone instead -- which still reads as the surface turning
    // sharply across the planes.
    ink *= 1.0 - smoothstep(0.25, 0.6, travel);
    float crowd = smoothstep(0.25, 0.6, travel) * clamp(halfWidth * 2.0 * travel, 0.0, 0.5);

    vec3 paper = uSlicePaper;
    if (uSliceLit) {
        // A soft key with a wide fill, so the paper itself models the form
        // without ever going dark enough to swallow the lines.
        float key = max(dot(n, normalize(uKeyDirection)), 0.0);
        float wrap = dot(n, v) * 0.5 + 0.5;
        paper *= 0.55 + 0.30 * key + 0.15 * wrap;
    }
    return mix(paper, uSliceColor, clamp(max(ink, crowd), 0.0, 1.0));
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
    // Whether a surface is being seen from its back has to be settled before
    // the normal is quantised.  Which side of a form you are looking at is a
    // fact about the form, not about the plane its normal was rounded onto, and
    // a plane that tips a degree past the horizon would otherwise turn end for
    // end -- a hard 180-degree seam around the silhouette that no plane of the
    // model put there.
    vec3 n;
    vec3 unrounded;
    if (uPlaneShading) {
        // Quantised in object space and rotated into view space afterwards,
        // so the planes stay locked to the form while the camera orbits it.
        vec3 world = uFlatShading
            ? normalize(cross(dFdx(vWorldPosition), dFdy(vWorldPosition)))
            : normalize(vWorldNormal);
        unrounded = normalize(uNormalMatrix * world);
        gWorldNormal = uPlaneMode == PLANE_GRID
            ? planeNormal(world)
            : planeAxisNormal(world, vWorldPosition);
        n = normalize(uNormalMatrix * gWorldNormal);
    } else {
        gWorldNormal = normalize(vWorldNormal);
        n = uFlatShading
            ? normalize(cross(dFdx(vViewPosition), dFdy(vViewPosition)))
            : normalize(vViewNormal);
        unrounded = n;
    }
    return dot(unrounded, viewDir) < 0.0 ? -n : n;
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

//: The HDRI's dominant light, in view space, and the irradiance it delivers
//: facing it; when the map is the only light the shadow map is cast from it,
//: and uEnvShadow says to take its share out of the shadowed places.
uniform bool uEnvShadow;
uniform vec3 uEnvSunView;
uniform vec3 uEnvSunColor;

vec3 viewToWorld(vec3 viewDirection) {
    // uNormalMatrix is the view's rotation, so its transpose undoes it.
    return transpose(uNormalMatrix) * viewDirection;
}

vec3 envDiffuse(vec3 n, bool shadowed) {
    // A map has no one direction to cast from, so the shadow is the
    // dominant light's: where the map says it is blocked, its share of the
    // irradiance comes off and the rest of the room still lights the form.
    vec3 e = envIrradiance(viewToWorld(n));
    if (shadowed && uEnvShadow) {
        float ndl = max(dot(n, normalize(uEnvSunView)), 0.0);
        e = max(e - (1.0 - shadowFactor(ndl)) * uEnvSunColor * ndl, vec3(0.0));
    }
    return e;
}

//: What a GGX lobe reflects of a prefiltered environment, as a scale and a
//: bias on the reflectance at normal incidence (Karis' fit for mobile).
vec2 envBrdf(float ndv, float roughness) {
    const vec4 c0 = vec4(-1.0, -0.0275, -0.572, 0.022);
    const vec4 c1 = vec4(1.0, 0.0425, 1.04, -0.04);
    vec4 r = roughness * c0 + c1;
    float a004 = min(r.x * r.x, exp2(-9.28 * ndv)) * r.x + r.y;
    return vec2(-1.04, 1.04) * a004 + r.zw;
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
    if (uEnvOn) {
        // The room lights the diffuse the way the sky did, and the
        // highlight is the room's own reflection, blurred to the lobe a
        // Phong exponent of this shininess has (alpha^2 = 2 / (n + 2)).
        color += uDiffuseColor * envDiffuse(n, shadowed) / PI * diffuseAo;
        if (mode != MODE_LAMBERT) {
            float exponent = max(uShininess, 1.0) * (mode == MODE_PHONG ? 1.0 : 4.0);
            float roughness = sqrt(sqrt(2.0 / (exponent + 2.0)));
            float ndv = max(dot(n, v), 1e-4);
            vec3 f0 = vec3(0.16 * uSpecularLevel) * uSpecularColor;
            vec2 ab = envBrdf(ndv, roughness);
            vec3 reflected = envRadiance(viewToWorld(reflect(-v, n)), envLod(roughness));
            color += reflected * (f0 * ab.x + ab.y * min(uSpecularLevel, 1.0)) * ao;
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
    if (uEnvOn) {
        // Image-based lighting by the split sum: the irradiance for the
        // diffuse, and for the specular the map blurred to the lobe's width
        // times the lobe's own response to it.
        vec2 ab = envBrdf(ndv, uRoughness);
        vec3 specular = envRadiance(viewToWorld(reflect(-v, n)), envLod(uRoughness))
                      * (f0 * ab.x + ab.y);
        vec3 kd = (1.0 - fresnelSchlick(f0, ndv)) * (1.0 - uMetalness);
        color += uDiffuseColor * kd * envDiffuse(n, false) / PI + specular;
    }
    return color;
}

#include "skin.glsl"

//: How many surfaces a ghosted form is taken to stack up between its near side
//: and its far one.  Correct front-to-back compositing gives the nth layer a
//: share ``(1 - alpha)^(n - 1)`` of the light, so reading n off the fragment's
//: depth through the form gives the same falloff without knowing which layer
//: it actually is.  Four is a figure seen across a limb: slope enough that the
//: near surface reads as the near one, little enough that the far side does
//: not vanish, which is the whole point of a ghost.
const float GHOST_LAYERS = 4.0;

float ghostWeight(float alpha) {
    // Normalised against the form's own depth rather than the window's: a
    // tightly framed model occupies a sliver of the depth buffer, and every
    // fragment of it would come out weighted the same.
    float through = clamp((abs(vViewPosition.z) - uGhostNear) / max(uGhostSpan, 1e-6), 0.0, 1.0);
    return max(pow(1.0 - alpha, through * GHOST_LAYERS), 1e-4);
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
    } else if (uMode == MODE_CONTOUR) {
        color = contourShade(n, v);
    } else if (uMode == MODE_HUMAN_SKIN) {
        color = skinShade(n, v);
    } else {
        color = analyticShade(n, v, uMode, false, 1.0);
    }
    if (uPlaneShading && uPlaneContour) {
        // Every flag branched on here is uniform, so the derivatives inside
        // stay well defined.
        vec3 turning = normalize(vWorldNormal);
        float ink = uPlaneMode == PLANE_GRID
            ? planeContour(turning)
            : planeAxisContour(turning, vWorldPosition);
        color = mix(color, uPlaneContourColor, ink);
    }
    if (uMode == MODE_MATCAP) {
        float noise = fract(52.9829189 * fract(dot(gl_FragCoord.xy,
                            vec2(0.06711056, 0.00583715)))) - 0.5;
        color += vec3(noise / 255.0);
    }
    vec3 shaded = max(color, vec3(0.0));
    if (uAccumulate) {
        // Both writes are sums, so whichever triangle of the form reached this
        // pixel first cannot change the answer.  The colours are averaged
        // under ghostWeight, and the transmittances multiplied -- as a sum of
        // their logarithms, since one blend function has to serve for both
        // attachments.
        float alpha = clamp(uOpacity, 0.0, 0.999);
        float weight = alpha * ghostWeight(alpha);
        fragColor = vec4(shaded * weight, weight);
        fragReveal = vec4(log(1.0 - alpha), 0.0, 0.0, 0.0);
    } else {
        fragColor = vec4(shaded, uOpacity);
        fragReveal = vec4(0.0);
    }
}
