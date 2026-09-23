#version 330 core

layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aNormal;

uniform mat4 uView;
uniform mat4 uProjection;
uniform mat3 uNormalMatrix;

out vec3 vViewPosition;
out vec3 vViewNormal;
out vec3 vWorldNormal;
out vec3 vWorldPosition;

void main() {
    vec4 viewPosition = uView * vec4(aPosition, 1.0);
    vViewPosition = viewPosition.xyz;
    vViewNormal = uNormalMatrix * aNormal;
    vWorldNormal = aNormal;
    vWorldPosition = aPosition;
    gl_Position = uProjection * viewPosition;
}
