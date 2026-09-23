#version 330 core
#include "section.glsl"

in vec3 vColor;
in vec3 vWorldPosition;
out vec4 fragColor;

//: A stroke can be asked to fade out with distance from a point: never quite
//: solid, so the form still reads through it, level to a third of the way
//: and gone at uFadeRadius.  Nought means no fade at all, which is what the
//: annotations and the contour ask for.  uFadePeak is how solid the line is
//: where it is not faded; uAlpha the same for a line that does not fade.
uniform vec3  uFadeCentre;
uniform float uFadeRadius;
uniform float uFadePeak;
uniform float uAlpha;

void main() {
    clipSection(vWorldPosition);
    float alpha = uAlpha;
    if (uFadeRadius > 0.0) {
        float away = distance(vWorldPosition, uFadeCentre) / uFadeRadius;
        alpha = uFadePeak * (1.0 - smoothstep(0.35, 1.0, away));
    }
    fragColor = vec4(vColor, alpha);
}
