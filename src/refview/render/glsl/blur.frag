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
