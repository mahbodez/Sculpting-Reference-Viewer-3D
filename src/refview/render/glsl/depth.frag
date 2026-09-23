#version 330 core
#include "section.glsl"

in vec3 vWorldPosition;
in vec3 vViewNormal;

out vec4 fragNormal;

void main() {
    clipSection(vWorldPosition);
    fragNormal = vec4(normalize(vViewNormal) * 0.5 + 0.5, 1.0);
}
