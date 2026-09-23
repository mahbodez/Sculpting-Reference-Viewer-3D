// The cross-section: up to two half-spaces, and material past a plane's
// offset is cut away.  Included by every shader that draws the model, so the
// mesh, the wireframe, the annotations and the shadow map all stop at the cut.
uniform int uSectionCount;
uniform vec4 uSectionPlanes[2];

void clipSection(vec3 worldPosition) {
    for (int i = 0; i < uSectionCount; ++i) {
        if (dot(worldPosition, uSectionPlanes[i].xyz) > uSectionPlanes[i].w) {
            discard;
        }
    }
}
