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
