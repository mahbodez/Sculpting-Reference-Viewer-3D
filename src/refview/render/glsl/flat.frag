#version 330 core
#include "section.glsl"

in vec3 vWorldPosition;
out vec4 fragColor;
uniform vec4 uColor;

void main() {
    clipSection(vWorldPosition);
    fragColor = uColor;
}
