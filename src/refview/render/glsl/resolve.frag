#version 330 core

in vec2 vUv;
out vec4 fragColor;

uniform sampler2D uFrame;
uniform vec2 uTexelSize;   // one texel of uFrame, in texture coordinates
uniform bool uFxaa;

float luma(vec3 rgb) {
    return dot(rgb, vec3(0.299, 0.587, 0.114));
}

//: Fast approximate anti-aliasing, in the compact form Timothy Lottes gave
//: it: read the four diagonal neighbours, find the direction the brightness
//: changes least along -- which runs along an edge rather than across it --
//: and blend a short way along that direction.  A blend that lands outside
//: the neighbourhood's own range has overshot an edge, and the shorter one
//: is kept instead.  Costs a handful of texture reads, and nothing at all in
//: the flat interior of a form, which comes out as it went in.
const float SPAN_MAX = 8.0;
const float REDUCE_MUL = 1.0 / 8.0;
const float REDUCE_MIN = 1.0 / 128.0;

void main() {
    vec3 middle = texture(uFrame, vUv).rgb;
    if (!uFxaa) {
        // Reading a double-size frame here, through its linear filter at the
        // screen's own pixel centres, averages each block of four: that is
        // the whole of the supersampling resolve.
        fragColor = vec4(middle, 1.0);
        return;
    }
    vec3 nw = texture(uFrame, vUv + vec2(-1.0, -1.0) * uTexelSize).rgb;
    vec3 ne = texture(uFrame, vUv + vec2( 1.0, -1.0) * uTexelSize).rgb;
    vec3 sw = texture(uFrame, vUv + vec2(-1.0,  1.0) * uTexelSize).rgb;
    vec3 se = texture(uFrame, vUv + vec2( 1.0,  1.0) * uTexelSize).rgb;
    float lumaNW = luma(nw), lumaNE = luma(ne), lumaSW = luma(sw), lumaSE = luma(se);
    float lumaM = luma(middle);
    float lumaMin = min(lumaM, min(min(lumaNW, lumaNE), min(lumaSW, lumaSE)));
    float lumaMax = max(lumaM, max(max(lumaNW, lumaNE), max(lumaSW, lumaSE)));

    vec2 dir = vec2(-((lumaNW + lumaNE) - (lumaSW + lumaSE)),
                     ((lumaNW + lumaSW) - (lumaNE + lumaSE)));
    float reduce = max((lumaNW + lumaNE + lumaSW + lumaSE) * (0.25 * REDUCE_MUL), REDUCE_MIN);
    float inverse = 1.0 / (min(abs(dir.x), abs(dir.y)) + reduce);
    dir = clamp(dir * inverse, vec2(-SPAN_MAX), vec2(SPAN_MAX)) * uTexelSize;

    vec3 near = 0.5 * (texture(uFrame, vUv + dir * (1.0 / 3.0 - 0.5)).rgb
                     + texture(uFrame, vUv + dir * (2.0 / 3.0 - 0.5)).rgb);
    vec3 far = near * 0.5 + 0.25 * (texture(uFrame, vUv + dir * -0.5).rgb
                                  + texture(uFrame, vUv + dir *  0.5).rgb);
    float lumaFar = luma(far);
    vec3 blended = (lumaFar < lumaMin || lumaFar > lumaMax) ? near : far;
    fragColor = vec4(blended, 1.0);
}
