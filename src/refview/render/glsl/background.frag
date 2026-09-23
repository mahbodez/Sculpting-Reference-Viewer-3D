#version 330 core

in vec2 vUv;
out vec4 fragColor;

uniform vec3 uTopColor;
uniform vec3 uBottomColor;
//: Draw the HDRI rather than the gradient: the ray through each pixel is
//: uBackgroundBasis applied to (x, y, 1) in the -1 to 1 square of the screen.
uniform bool  uBackgroundEnv;
uniform mat3  uBackgroundBasis;
uniform float uBackgroundLod;
//: How radiance is put on the screen: clamped, as the display-space modes
//: do, or through the skin's exposure, tone curve and sRGB encoding, so the
//: model and the room behind it are developed alike.
uniform bool  uBackgroundFilmic;
uniform float uBackgroundExposure;

#include "environment.glsl"

void main() {
    if (uBackgroundEnv && uEnvOn) {
        vec3 ray = normalize(uBackgroundBasis * vec3(vUv * 2.0 - 1.0, 1.0));
        vec3 c = envRadiance(ray, uBackgroundLod);
        if (uBackgroundFilmic) {
            c *= exp2(uBackgroundExposure);
            c = c / (1.0 + c);
            c = mix(12.92 * c, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055,
                    step(vec3(0.0031308), c));
        }
        fragColor = vec4(clamp(c, 0.0, 1.0), 1.0);
        return;
    }
    fragColor = vec4(mix(uBottomColor, uTopColor, vUv.y), 1.0);
}
