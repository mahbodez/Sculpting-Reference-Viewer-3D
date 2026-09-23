#version 330 core

// Feeds both the shadow map and the occlusion pre-pass.  The shadow pass wants
// only the depth; the occlusion pass also wants the surface normal, which is
// far steadier than one reconstructed from the depth buffer's derivatives.

layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aNormal;

uniform mat4 uView;
uniform mat4 uProjection;
uniform mat3 uNormalMatrix;

out vec3 vWorldPosition;
out vec3 vViewNormal;

void main() {
    vWorldPosition = aPosition;
    vViewNormal = uNormalMatrix * aNormal;
    gl_Position = uProjection * uView * vec4(aPosition, 1.0);
}
