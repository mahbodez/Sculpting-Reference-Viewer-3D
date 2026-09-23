uniform bool  uEnvOn;
uniform sampler2D uEnvMap;
uniform sampler2D uEnvTexels;
uniform sampler2D uEnvCdf;
//: World directions into the map's own frame: its turn about the vertical,
//: and the view's rotation too while the lights follow the camera.
uniform mat3  uEnvFromWorld;
//: Irradiance harmonics, in the map's frame, before uEnvScale.
uniform vec3  uEnvSH[9];
uniform float uEnvScale;
uniform float uEnvLevels;
uniform float uEnvWidth;

const float ENV_PI = 3.14159265359;

vec2 envUv(vec3 d) {
    return vec2(atan(d.x, -d.z) / (2.0 * ENV_PI) + 0.5,
                acos(clamp(d.y, -1.0, 1.0)) / ENV_PI);
}
vec3 envDirection(vec2 uv) {
    float phi = (uv.x - 0.5) * 2.0 * ENV_PI;
    float theta = uv.y * ENV_PI;
    float s = sin(theta);
    return vec3(s * sin(phi), cos(theta), -s * cos(phi));
}
//: Radiance arriving from a world direction, blurred to a mip level.  Read
//: with an explicit level, so the seam where atan wraps round has no
//: derivative to break on.
vec3 envRadiance(vec3 worldDirection, float lod) {
    if (!uEnvOn) return vec3(0.0);
    vec3 d = normalize(uEnvFromWorld * worldDirection);
    return textureLod(uEnvMap, envUv(d), lod).rgb * uEnvScale;
}
//: The mip level whose texels are about as wide as a GGX lobe of this
//: roughness: alpha radians is the lobe, 2 pi / width the finest texel.
float envLod(float roughness) {
    float alpha = max(roughness * roughness, 1e-4);
    return clamp(log2(uEnvWidth * alpha / (2.0 * ENV_PI)) + 0.5, 0.0, max(uEnvLevels - 1.0, 0.0));
}
//: Irradiance on a surface facing worldNormal.  ``soften`` takes the higher
//: bands down, per channel, which is what light that has diffused a way
//: under the surface does to the picture: red, travelling furthest, wraps
//: round the form most.
vec3 envIrradianceSoft(vec3 worldNormal, vec3 soften) {
    if (!uEnvOn) return vec3(0.0);
    vec3 n = normalize(uEnvFromWorld * worldNormal);
    vec3 band0 = uEnvSH[0] * 0.282095;
    vec3 band1 = 0.488603 * (uEnvSH[1] * n.y + uEnvSH[2] * n.z + uEnvSH[3] * n.x);
    vec3 band2 = 1.092548 * (uEnvSH[4] * n.x * n.y + uEnvSH[5] * n.y * n.z + uEnvSH[7] * n.x * n.z)
               + 0.315392 * uEnvSH[6] * (3.0 * n.z * n.z - 1.0)
               + 0.546274 * uEnvSH[8] * (n.x * n.x - n.y * n.y);
    vec3 e = band0 + band1 * (1.0 - 0.5 * soften) + band2 * (1.0 - 0.85 * soften);
    return max(e, vec3(0.0)) * uEnvScale;
}
vec3 envIrradiance(vec3 worldNormal) {
    return envIrradianceSoft(worldNormal, vec3(0.0));
}
//: The largest index whose cumulative value is at most xi, along one row of
//: the distribution table.  The row's last entry is one, above any xi.
int envSearch(int row, int count, float xi) {
    int low = 0;
    int high = count;
    while (high - low > 1) {
        int middle = (low + high) / 2;
        if (texelFetch(uEnvCdf, ivec2(middle, row), 0).r <= xi) low = middle;
        else high = middle;
    }
    return low;
}
//: A world direction picked in proportion to the light arriving along it,
//: the radiance it carries and its density over solid angle.  The radiance
//: is the coarse cell's, the same one the density was built from, so the
//: estimate is exact however coarse the cells.
vec3 envSample(vec2 xi, out vec3 radiance, out float pdf) {
    ivec2 size = textureSize(uEnvTexels, 0);
    int row = envSearch(size.y, size.y, xi.y);
    float r0 = texelFetch(uEnvCdf, ivec2(row, size.y), 0).r;
    float r1 = texelFetch(uEnvCdf, ivec2(row + 1, size.y), 0).r;
    float dv = clamp((xi.y - r0) / max(r1 - r0, 1e-12), 0.0, 1.0);
    int column = envSearch(row, size.x, xi.x);
    float c0 = texelFetch(uEnvCdf, ivec2(column, row), 0).r;
    float c1 = texelFetch(uEnvCdf, ivec2(column + 1, row), 0).r;
    float du = clamp((xi.x - c0) / max(c1 - c0, 1e-12), 0.0, 1.0);
    vec2 uv = vec2((float(column) + du) / float(size.x), (float(row) + dv) / float(size.y));
    vec4 texel = texelFetch(uEnvTexels, ivec2(column, row), 0);
    float sinTheta = max(sin(uv.y * ENV_PI), 1e-4);
    pdf = texel.a / (2.0 * ENV_PI * ENV_PI * sinTheta);
    radiance = texel.rgb * uEnvScale;
    return transpose(uEnvFromWorld) * envDirection(uv);
}
