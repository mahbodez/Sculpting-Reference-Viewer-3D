#version 330 core

in vec2 vUv;
out vec4 fragColor;

uniform sampler2D uAccum;
uniform sampler2D uReveal;

void main() {
    vec4 accum = texture(uAccum, vUv);
    // The transmittances were summed in the log, so the product of them --
    // what is left of the scene standing behind the ghost -- comes back as a
    // single exponential, and it is exact however many surfaces there were.
    float behind = exp(texture(uReveal, vUv).r);
    float alpha = 1.0 - behind;
    if (alpha <= 0.0) {
        discard;  // Nothing was drawn here; leave the frame alone.
    }
    fragColor = vec4(accum.rgb / max(accum.a, 1e-5), alpha);
}
