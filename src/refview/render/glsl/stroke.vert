#version 330 core

// Thick surface strokes.  Each segment arrives as two triangles whose corners
// carry both of the segment's endpoints; the shader projects them, works out
// the screen-space direction and pushes each corner sideways by half the brush
// width.  Doing the widening here keeps the line thickness in pixels at any
// zoom, which glLineWidth cannot promise on a core profile.

layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aOther;
layout(location = 2) in vec3 aNormal;
layout(location = 3) in vec3 aColor;
layout(location = 4) in float aSide;
layout(location = 5) in float aWidth;

uniform mat4 uViewProjection;
uniform vec2 uViewport;      // drawable size in device pixels
uniform float uWidthScale;   // device pixels per logical pixel
uniform float uNormalOffset; // world units lifted off the surface
uniform float uDepthBias;    // extra nudge towards the viewer, in NDC

out vec3 vColor;
out vec3 vWorldPosition;

vec2 to_screen(vec4 clip) {
    float w = abs(clip.w) < 1e-6 ? 1e-6 : clip.w;
    return clip.xy / w * uViewport * 0.5;
}

void main() {
    vWorldPosition = aPosition + aNormal * uNormalOffset;
    vec4 clip = uViewProjection * vec4(vWorldPosition, 1.0);
    vec4 other = uViewProjection * vec4(aOther + aNormal * uNormalOffset, 1.0);

    vec2 delta = to_screen(other) - to_screen(clip);
    float travel = length(delta);
    vec2 direction = travel > 1e-5 ? delta / travel : vec2(1.0, 0.0);
    float half_width = max(aWidth * uWidthScale, 1.0) * 0.5;

    // Sideways for the ribbon, backwards for a cap that also fills the joins.
    vec2 offset = vec2(-direction.y, direction.x) * (aSide * half_width)
                - direction * half_width;

    float w = abs(clip.w) < 1e-6 ? 1e-6 : clip.w;
    clip.xy += offset / (uViewport * 0.5) * w;
    clip.z -= uDepthBias * w;
    gl_Position = clip;
    vColor = aColor;
}
