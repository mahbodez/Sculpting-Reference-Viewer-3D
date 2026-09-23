#version 330 core

// The line drawn round an object the artist just made active: every pixel
// outside its mask that has the mask within a line's width of it.  Sixteen
// taps round a ring at the full width and sixteen at half, so a limb thinner
// than the ring cannot slip between two taps.  The mask is read with linear
// filtering, which is what softens the line's outer edge.

in vec2 vUv;
out vec4 fragColor;

uniform sampler2D uMask;
uniform vec2 uTexelSize;
uniform float uRadius;
uniform vec4 uColor;

void main() {
    if (texture(uMask, vUv).r > 0.5) {
        discard;  // The line goes round the object, not over it.
    }
    float near = 0.0;
    for (int i = 0; i < 16; ++i) {
        float angle = float(i) * 0.39269908;  // A sixteenth of a turn.
        vec2 step = vec2(cos(angle), sin(angle)) * uTexelSize * uRadius;
        near = max(near, texture(uMask, vUv + step).r);
        near = max(near, texture(uMask, vUv + step * 0.5).r);
    }
    if (near <= 0.0) {
        discard;
    }
    fragColor = vec4(uColor.rgb, uColor.a * near);
}
