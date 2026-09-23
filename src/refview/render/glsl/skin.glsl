uniform vec3 uSkinColor;
uniform vec3 uSkinScatter;
uniform float uSkinRoughness;
uniform float uSkinSpecular;
uniform float uSkinOil;
uniform float uSkinSSS;
uniform float uSkinRadius;
uniform float uSkinTransmission;
uniform float uSkinLightSize;
uniform float uSkinExposure;
uniform float uSkinIndirect;
uniform float uSkinEpsilon;
uniform bool uSkinFurniture;
uniform int uSkinSample;
uniform int uSkinNodeCount;
uniform sampler2D uSkinNodes;
uniform sampler2D uSkinTriangles;
uniform sampler2D uSkinAttributes;
// The tables are laid out 1 << uSkinTableShift texels wide.
uniform int uSkinTableShift;
uniform sampler3D uSkinRelief;
uniform sampler2D uSkinDiffusion;
uniform float uSkinDetail;
uniform float uSkinPoreSize;
uniform float uSkinMottle;
uniform float uSkinBlood;
uniform float uSkinFuzz;
uniform float uSkinBlemishes;
uniform float uSkinFreckles;
uniform float uSkinNevi;
uniform float uSkinAcne;
// The body map: seven region weights and, last, how much is assigned at
// all, over the box from uSkinBodyOrigin of size 1/uSkinBodyInvSize.
uniform bool uSkinBodyOn;
uniform sampler3D uSkinBodyA;
uniform sampler3D uSkinBodyB;
uniform vec3 uSkinBodyOrigin;
uniform vec3 uSkinBodyInvSize;
// Per-region multipliers, four regions to a vec4, in the map's order:
// head, neck, torso, arms; hands, legs, feet, (unused).
uniform vec4 uSkinAcneA, uSkinAcneB;
uniform vec4 uSkinNeviA, uSkinNeviB;
uniform vec4 uSkinFrecklesA, uSkinFrecklesB;
uniform vec4 uSkinBlemishA, uSkinBlemishB;
uniform vec4 uSkinOilA, uSkinOilB;
uniform vec4 uSkinBloodA, uSkinBloodB;

const float SKIN_RELIEF_CELLS = @CELLS@;
const float SKIN_LUT_LOG_MIN = @LUT_MIN@;
const float SKIN_LUT_LOG_SPAN = @LUT_SPAN@;
// Linear tint of light that has passed through blood-rich dermis: red survives.
const vec3 SKIN_FLUSH = vec3(1.04, 0.70, 0.64);

vec3 skinLinear(vec3 c) {
    return mix(c / 12.92, pow((c + 0.055) / 1.055, vec3(2.4)),
               step(vec3(0.04045), c));
}
vec3 skinDisplay(vec3 c) {
    c = max(c, vec3(0.0));
    return mix(12.92 * c, 1.055 * pow(c, vec3(1.0 / 2.4)) - 0.055,
               step(vec3(0.0031308), c));
}
// Random numbers, stratified over the samples: every pixel walks a 2D
// low-discrepancy sequence per pair of dimensions -- R2 for the first,
// Kronecker lattices on square roots of primes for the rest -- from a start
// of its own, so a pixel's first sixteen samples already cover the key's
// disc, the diffusion radii and the bounce hemisphere evenly, where white
// noise leaves gaps a quarter of the time.  The pixels stay uncorrelated
// with one another, so what noise is left is fine grain, not pattern.
uvec2 skinPixel;
int skinPair;
const vec2 SKIN_SEQUENCE[8] = vec2[8](
    vec2(0.7548776662, 0.5698402910), vec2(0.4142135624, 0.7320508076),
    vec2(0.2360679775, 0.6457513111), vec2(0.3166247904, 0.6055512755),
    vec2(0.1231056256, 0.3588989435), vec2(0.7958315233, 0.3851648071),
    vec2(0.5677643628, 0.0827625303), vec2(0.4031242374, 0.5574385243));
uint skinHash(uint x) {
    x ^= x >> 16; x *= 0x7feb352du; x ^= x >> 15; x *= 0x846ca68bu; x ^= x >> 16;
    return x;
}
vec2 skinRandom2() {
    int k = skinPair++;
    uint h = skinHash(skinPixel.x * 1973u + skinPixel.y * 9277u + uint(k) * 26699u + 1u);
    uint g = skinHash(h ^ 0x9e3779b9u);
    vec2 start = vec2(float(h & 0x00ffffffu), float(g & 0x00ffffffu)) / 16777216.0;
    return fract(start + float(uSkinSample) * SKIN_SEQUENCE[k & 7]);
}
mat3 skinBasis(vec3 n) {
    vec3 t = normalize(cross(abs(n.z) < 0.9 ? vec3(0,0,1) : vec3(0,1,0), n));
    return mat3(t, cross(n, t), n);
}
vec4 skinTexel(sampler2D table, int index) {
    int mask = (1 << uSkinTableShift) - 1;
    return texelFetch(table, ivec2(index & mask, index >> uSkinTableShift), 0);
}
bool skinClipped(vec3 p) {
    for (int i=0; i<uSectionCount; ++i)
        if (dot(p, uSectionPlanes[i].xyz) > uSectionPlanes[i].w) return true;
    return false;
}
// Deep enough for any tree the builder makes: it splits by area, and the
// stack only ever holds the farther child of each node on the way down.
const int SKIN_STACK = 40;
// Walk the tree from origin along ray, out to tMax.  Returns the triangle
// hit, or -1, with tMax shortened to it and its barycentrics.  With anyHit
// the first triangle found will do, which is all a shadow ray asks.
int skinTrace(vec3 origin, vec3 ray, inout float tMax, bool anyHit, out vec2 bary) {
    bary = vec2(0.0);
    if (uSkinNodeCount <= 0) return -1;
    vec3 safeRay = mix(ray, mix(vec3(-1e-12), vec3(1e-12), step(vec3(0), ray)),
                        lessThan(abs(ray), vec3(1e-12)));
    vec3 inv = 1.0 / safeRay;
    int stack[SKIN_STACK];
    int top = 0;
    int node = 0;
    int found = -1;
    for (;;) {
        int base = node * 4;
        vec4 a0 = skinTexel(uSkinNodes, base), a1 = skinTexel(uSkinNodes, base + 1);
        vec4 b0 = skinTexel(uSkinNodes, base + 2), b1 = skinTexel(uSkinNodes, base + 3);
        vec3 la = (a0.xyz - origin) * inv, ha = (a1.xyz - origin) * inv;
        vec3 lb = (b0.xyz - origin) * inv, hb = (b1.xyz - origin) * inv;
        vec3 na = min(la, ha), fa = max(la, ha), nb = min(lb, hb), fb = max(lb, hb);
        float enterA = max(max(na.x, na.y), max(na.z, 0.0));
        float exitA = min(min(fa.x, fa.y), min(fa.z, tMax));
        float enterB = max(max(nb.x, nb.y), max(nb.z, 0.0));
        float exitB = min(min(fb.x, fb.y), min(fb.z, tMax));
        bool hitA = enterA <= exitA, hitB = enterB <= exitB;
        int refs[2] = int[2](int(a0.w), int(a1.w));
        // Leaves are opened on the spot; only interior children go on.
        for (int side = 0; side < 2; ++side) {
            bool reached = side == 0 ? hitA : hitB;
            if (!reached || refs[side] >= 0) continue;
            if (side == 0) hitA = false; else hitB = false;
            for (int t = -refs[side] - 1;; ++t) {
                vec4 p0 = skinTexel(uSkinTriangles, t * 3);
                vec4 e1 = skinTexel(uSkinTriangles, t * 3 + 1);
                vec3 e2 = skinTexel(uSkinTriangles, t * 3 + 2).xyz;
                vec3 q = cross(ray, e2);
                float det = dot(e1.xyz, q);
                if (abs(det) >= e1.w) {
                    float invDet = 1.0 / det;
                    vec3 s = origin - p0.xyz;
                    float u = dot(s, q) * invDet;
                    vec3 r = cross(s, e1.xyz);
                    float v = dot(ray, r) * invDet;
                    float d = dot(e2, r) * invDet;
                    if (u >= 0.0 && v >= 0.0 && u + v <= 1.0 && d >= uSkinEpsilon * 0.25
                        && d < tMax && !skinClipped(origin + ray * d)) {
                        tMax = d;
                        found = t;
                        bary = vec2(u, v);
                        if (anyHit) return found;
                    }
                }
                if (p0.w >= 2.0) break;   // the last triangle of the leaf
            }
        }
        if (hitA && hitB) {
            bool aFirst = enterA <= enterB;
            if (top < SKIN_STACK) stack[top++] = aFirst ? refs[1] : refs[0];
            node = aFirst ? refs[0] : refs[1];
        } else if (hitA) {
            node = refs[0];
        } else if (hitB) {
            node = refs[1];
        } else {
            if (top == 0) break;
            node = stack[--top];
        }
    }
    return found;
}
struct SkinHit { float distance; vec3 normal; vec3 color; int material; };
bool skinRay(vec3 origin, vec3 ray, float reach, out SkinHit hit) {
    hit.distance = reach;
    hit.material = -1;
    hit.normal = vec3(0.0, 0.0, 1.0);
    hit.color = vec3(0.0);
    vec2 bary;
    int t = skinTrace(origin, ray, hit.distance, false, bary);
    if (t < 0) return false;
    // Only the nearest hit needs its shading: read it once, at the end.
    vec4 n0 = skinTexel(uSkinAttributes, t * 3);
    vec4 n1 = skinTexel(uSkinAttributes, t * 3 + 1);
    vec4 n2 = skinTexel(uSkinAttributes, t * 3 + 2);
    vec3 normal = n0.xyz * (1.0 - bary.x - bary.y) + n1.xyz * bary.x + n2.xyz * bary.y;
    if (dot(normal, normal) < 1e-12) {
        normal = cross(skinTexel(uSkinTriangles, t * 3 + 1).xyz,
                       skinTexel(uSkinTriangles, t * 3 + 2).xyz);
    }
    hit.normal = normalize(normal);
    hit.color = skinLinear(vec3(n0.w, n1.w, n2.w));
    hit.material = int(mod(skinTexel(uSkinTriangles, t * 3).w, 2.0));
    return true;
}
float skinVisible(vec3 p, vec3 n, vec3 l) {
    float reach = 1e30;
    vec2 bary;
    return skinTrace(p + n * uSkinEpsilon, l, reach, true, bary) >= 0 ? 0.0 : 1.0;
}
vec3 skinLight(vec3 direction, vec2 xi) {
    if (!uSkinTrace || uSkinLightSize<=0.0) return direction;
    float angle=2.0*PI*xi.x;
    float c=mix(1.0, cos(uSkinLightSize), xi.y);
    float s=sqrt(max(0.0,1.0-c*c));
    return skinBasis(direction)*vec3(cos(angle)*s,sin(angle)*s,c);
}
vec3 skinFresnel(float vdh) {
    // eta=1.4 gives normal-incidence reflectance 0.0278; tint remains neutral.
    return clamp(fresnelSchlick(vec3(0.02778), vdh)*uSkinSpecular,0.0,0.99);
}
float skinLobe(vec3 n, vec3 v, vec3 l, float roughness) {
    vec3 halfVector=v+l;
    if (dot(halfVector,halfVector)<1e-10) return 0.0;
    vec3 h=normalize(halfVector);
    float nv=max(dot(n,v),1e-5), nl=max(dot(n,l),1e-5);
    float a=roughness*roughness;
    return distributionGGX(max(dot(n,h),0.0),a)*geometrySmith(nv,nl,a)/(4.0*nv*nl);
}
vec3 skinSpec(vec3 n, vec3 v, vec3 l, float roughness, float oil) {
    if (dot(n,l)<=0.0 || dot(n,v)<=0.0) return vec3(0);
    vec3 h=normalize(l+v);
    return skinFresnel(max(dot(v,h),0.0)) * mix(
        skinLobe(n,v,l,roughness), skinLobe(n,v,l,0.18),oil);
}
// The studio rig's sky-and-ground ambient, as radiance from a direction.
// The HDRI is not in here: its light is sampled as a light where the skin
// is traced, and read from its harmonics where it is not.
vec3 skinEnvironment(vec3 direction) {
    return skinLinear(uAmbientColor)*uAmbientIntensity
         * mix(0.35,1.0,clamp(direction.y*0.5+0.5,0.0,1.0));
}
// Surface micro-structure, read from the tileable relief volume at world
// position. Slopes are unitless (height per pore width) so the bump amount
// means the same thing at every pore size.
struct SkinSurface { vec3 slope; float tone; float flush; float fade; };
SkinSurface skinRelief(vec3 p) {
    vec3 q=p/(uSkinPoreSize*SKIN_RELIEF_CELLS);
    SkinSurface s;
    // Once a pore covers only a few pixels its bump can only alias, so the
    // relief fades out before that; the mip chain averages what remains.
    s.fade=1.0-smoothstep(0.12,0.5,length(fwidth(q))*SKIN_RELIEF_CELLS);
    // A second fetch, rotated and rescaled, hides the tile period; the chain
    // rule turns its slope back with the transpose (vector * matrix).
    const mat3 twist=mat3(0.36,0.48,-0.80, -0.80,0.60,0.00, 0.48,0.64,0.60);
    vec4 a=texture(uSkinRelief,q);
    vec4 b=texture(uSkinRelief,twist*q*1.63+vec3(0.37,0.71,0.19));
    s.slope=a.xyz+(b.xyz*twist)*(0.5*1.63);
    // Pigment and blood vary over a much larger scale than the pores do, with
    // a little of the fine grain mixed into the pigment.
    s.tone=mix(texture(uSkinRelief,q*0.19+vec3(0.50,0.13,0.77)).w,a.w,0.25);
    s.flush=texture(uSkinRelief,q*0.11+vec3(0.23,0.61,0.41)).w;
    return s;
}
vec3 skinBump(vec3 n, vec3 slope, float amount) {
    // A height field offset along n tilts the normal against its tangential slope.
    vec3 tangential=slope-n*dot(n,slope);
    return normalize(n-tangential*amount);
}
vec3 skinAlbedo(vec3 base, SkinSurface s, float blood) {
    vec3 albedo=base*(1.0+uSkinMottle*0.22*(s.tone*2.0-1.0));
    float pooled=blood*smoothstep(0.25,0.85,s.flush);
    return clamp(mix(albedo,albedo*SKIN_FLUSH,pooled),0.0,1.0);
}

// Where on the body the point is: how much each kind of mark, and the oil
// and the blood, are turned up or down there.  Off the map, or off a
// figure, everything is 1.
struct SkinRegion {
    float acne; float nevi; float freckles; float blemishes; float oil; float blood;
};
SkinRegion skinRegion(vec3 p) {
    SkinRegion r=SkinRegion(1.0,1.0,1.0,1.0,1.0,1.0);
    if (!uSkinBodyOn) return r;
    vec3 uvw=(p-uSkinBodyOrigin)*uSkinBodyInvSize;
    vec4 a=texture(uSkinBodyA,uvw), b=texture(uSkinBodyB,uvw);
    // What is not assigned to any region keeps the slider as it is.
    float rest=max(1.0-b.w,0.0);
    b.w=0.0;
    r.acne=rest+dot(a,uSkinAcneA)+dot(b,uSkinAcneB);
    r.nevi=rest+dot(a,uSkinNeviA)+dot(b,uSkinNeviB);
    r.freckles=rest+dot(a,uSkinFrecklesA)+dot(b,uSkinFrecklesB);
    r.blemishes=rest+dot(a,uSkinBlemishA)+dot(b,uSkinBlemishB);
    r.oil=rest+dot(a,uSkinOilA)+dot(b,uSkinOilB);
    r.blood=rest+dot(a,uSkinBloodA)+dot(b,uSkinBloodB);
    return r;
}

vec4 skinHash4(vec3 cell) {
    vec4 p4=fract(vec4(cell.xyzx)*vec4(0.1031,0.1030,0.0973,0.1099));
    p4+=dot(p4,p4.wzxy+33.33);
    return fract((p4.xxyz+p4.yzzw)*p4.zywx);
}
// One round spot on a jittered lattice in a plane, in lattice units: how
// much of the point it covers (a soft disc), a random for what kind of spot
// it is, the unit direction away from its centre, and the distance out as
// a share of its radius.  The jitter and the radius together stay inside
// the cell, so only the point's own cell can carry a spot that reaches it.
float skinSpot(vec2 q, float seed, float density, float radius, float soft,
               out float kind, out vec2 away, out float t) {
    vec2 cell=floor(q);
    vec4 h=skinHash4(vec3(cell,seed)), k=skinHash4(vec3(cell,seed+71.0));
    kind=k.x;
    away=vec2(1.0,0.0);
    t=2.0;
    if (h.w>=density) return 0.0;
    vec2 centre=cell+0.5+(h.xy-0.5)*0.5;
    float r=radius*mix(0.55,1.0,k.y);
    vec2 d=q-centre;
    float s=length(d);
    t=s/r;
    away=d/max(s,1e-6);
    return 1.0-smoothstep(soft,1.0,t);
}
// The slope of a dome of height h (in lattice units) over a spot: in
// towards the centre, feathered at the rim.
vec2 skinDome(vec2 away, float t, float h, float r) {
    float edge=1.0-smoothstep(0.75,1.0,t);
    return -away*(2.0*h*t/max(r,1e-6))*edge;
}

// The marks on the skin at p: what they do to the albedo, how they bump
// the surface (a slope, as the relief's is), and how they change the shine.
struct SkinMarks { vec3 tint; vec3 slope; float oil; float rough; };

// The spots on one plane through p: its coordinates in that plane, the
// world directions of the plane's axes, and a seed telling this plane's
// lattices from the others'.
SkinMarks skinSpots(vec2 uv, vec3 uAxis, vec3 vAxis, float seed, float perPixel,
                    float freckles, float nevi, float acne) {
    SkinMarks m;
    m.tint=vec3(1.0); m.slope=vec3(0.0); m.oil=0.0; m.rough=0.0;
    float pore=max(uSkinPoreSize,1e-9);
    float kind, t; vec2 away;
    // Freckles: small, thick on the ground, light brown, flat.
    {
        float cell=4.0*pore;
        float fade=1.0-smoothstep(0.08,0.30,perPixel/cell);
        float cover=skinSpot(uv/cell+vec2(11.3,7.1),seed,min(freckles*0.6,1.0),0.25,0.1,
                             kind,away,t)*fade;
        float strength=mix(0.3,0.85,kind);
        m.tint*=mix(vec3(1.0),vec3(0.62,0.45,0.35),cover*strength);
    }
    // Moles: dark, a few pores across, few, faintly raised.
    {
        float cell=10.0*pore;
        float fade=1.0-smoothstep(0.05,0.20,perPixel/cell);
        float cover=skinSpot(uv/cell+vec2(5.7,13.1),seed+3.0,min(nevi*0.08,1.0),0.25,0.65,
                             kind,away,t)*fade;
        vec3 dark=mix(vec3(0.30,0.20,0.17),vec3(0.52,0.36,0.30),step(0.7,kind));
        m.tint*=mix(vec3(1.0),dark,cover);
        vec2 dome=skinDome(away,t,0.04,0.25)*cover;
        m.slope+=uAxis*dome.x+vAxis*dome.y;
        m.rough+=cover*0.15;
    }
    // Acne: red papules, raised and shining, some come to a pale head.
    {
        float cell=6.0*pore;
        float fade=1.0-smoothstep(0.06,0.25,perPixel/cell);
        float cover=skinSpot(uv/cell+vec2(2.3,4.7),seed+6.0,min(acne*0.25,1.0),0.25,0.45,
                             kind,away,t)*fade;
        float flush=cover*(0.55+0.45*(1.0-smoothstep(0.0,0.8,t)));
        m.tint*=mix(vec3(1.0),vec3(1.08,0.52,0.46),flush);
        float bump=1.0-smoothstep(0.35,0.7,t);
        vec2 dome=skinDome(away,t*1.4,0.15,0.25)*cover*bump;
        m.slope+=uAxis*dome.x+vAxis*dome.y;
        float head=step(0.62,kind)*(1.0-smoothstep(0.0,0.30,t))*cover;
        m.tint=mix(m.tint,vec3(1.0,0.90,0.72),head);
        m.oil+=cover*bump*0.6;
    }
    return m;
}

// The marks at p on a surface with normal n.  The spots are laid on three
// planes, one per axis, and blended by how squarely the surface faces each
// -- the projection a texture is put on a mesh without a UV layout by --
// so that every spot is a disc on the skin whichever way the skin turns.
// Blemishes are patches read off the relief's tone noise in the volume.
SkinMarks skinMarks(vec3 p, vec3 n, SkinRegion region) {
    SkinMarks m;
    m.tint=vec3(0.0); m.slope=vec3(0.0); m.oil=0.0; m.rough=0.0;
    // World units per pixel, once, for the fades: a spot a pixel or two
    // across only sparkles, so each lattice fades out before that.  Taken
    // here, outside every branch, to stay defined.
    float perPixel=length(fwidth(p));
    float freckles=uSkinFreckles*region.freckles;
    float nevi=uSkinNevi*region.nevi;
    float acne=uSkinAcne*region.acne;
    float blemishes=uSkinBlemishes*region.blemishes;
    vec3 w=pow(abs(n),vec3(4.0));
    w/=max(w.x+w.y+w.z,1e-6);
    if (freckles+nevi+acne>0.0) {
        if (w.x>0.005) {
            SkinMarks a=skinSpots(p.yz,vec3(0,1,0),vec3(0,0,1),1.0,perPixel,freckles,nevi,acne);
            m.tint+=a.tint*w.x; m.slope+=a.slope*w.x; m.oil+=a.oil*w.x; m.rough+=a.rough*w.x;
        } else m.tint+=vec3(w.x);
        if (w.y>0.005) {
            SkinMarks a=skinSpots(p.zx,vec3(0,0,1),vec3(1,0,0),2.0,perPixel,freckles,nevi,acne);
            m.tint+=a.tint*w.y; m.slope+=a.slope*w.y; m.oil+=a.oil*w.y; m.rough+=a.rough*w.y;
        } else m.tint+=vec3(w.y);
        if (w.z>0.005) {
            SkinMarks a=skinSpots(p.xy,vec3(1,0,0),vec3(0,1,0),3.0,perPixel,freckles,nevi,acne);
            m.tint+=a.tint*w.z; m.slope+=a.slope*w.z; m.oil+=a.oil*w.z; m.rough+=a.rough*w.z;
        } else m.tint+=vec3(w.z);
    } else m.tint=vec3(1.0);
    // Blemishes: patches, coarser than the pores, of irritated redness and
    // of dry, duller skin, read at two scales that share no period.
    if (blemishes>0.0) {
        vec3 q=p/(uSkinPoreSize*SKIN_RELIEF_CELLS);
        float red=texture(uSkinRelief,q*0.043+vec3(0.71,0.29,0.53)).w
                 *texture(uSkinRelief,q*0.027+vec3(0.17,0.61,0.37)).w*2.0;
        float sore=smoothstep(0.52,0.80,red)*blemishes;
        m.tint*=mix(vec3(1.0),vec3(1.05,0.78,0.72),sore);
        float dry=smoothstep(0.58,0.82,texture(uSkinRelief,q*0.031+vec3(0.13,0.83,0.47)).w)
                 *blemishes;
        m.tint*=mix(vec3(1.0),vec3(0.86,0.79,0.75),dry);
        m.rough+=dry*0.3;
    }
    return m;
}
vec3 skinDiffusionLengths(vec3 albedo) {
    // Burley's fit from mean free path and albedo to the profile's length d.
    vec3 s=1.9-albedo+3.5*(albedo-0.8)*(albedo-0.8);
    return max(uSkinRadius*uSkinScatter/s,vec3(uSkinEpsilon*2.0));
}
float skinSphereRadius(vec3 smoothNormal) {
    // How far the surface travels per unit of normal turn, from screen derivatives.
    float turn=length(fwidth(smoothNormal));
    float travel=length(fwidth(vWorldPosition));
    return clamp(travel/max(turn,1e-6),uSkinEpsilon,1e6);
}
vec3 skinWrap(float ndl, vec3 lengths, float sphereRadius) {
    // Pre-integrated Burley diffusion over a sphere, one row per channel.
    vec2 texel=1.0/vec2(textureSize(uSkinDiffusion,0));
    float column=mix(0.5*texel.x,1.0-0.5*texel.x,ndl*0.5+0.5);
    vec3 row=clamp((log2(sphereRadius/lengths)-SKIN_LUT_LOG_MIN)/SKIN_LUT_LOG_SPAN,0.0,1.0);
    row=mix(vec3(0.5*texel.y),vec3(1.0-0.5*texel.y),row);
    return vec3(texture(uSkinDiffusion,vec2(column,row.r)).r,
                texture(uSkinDiffusion,vec2(column,row.g)).r,
                texture(uSkinDiffusion,vec2(column,row.b)).r);
}
// The rays one traced sample casts, as jobs for a single loop.  A GPU
// inlines every call, and ten calls to the traversal are ten copies of it
// competing for registers -- slower per ray than the same rays cast one
// after another from one copy, which is what the loop does.  Later jobs
// read what earlier ones found: an exit point, the skin a diffusion sample
// landed on, the surface a bounce reached.
const int JOB_SEES = 0;        // 0-2: key, fill, HDRI seen from the point
const int JOB_EXIT = 3;        // 3-5: where each light's backlight leaves
const int JOB_EXIT_SEES = 6;   // 6-8: whether that exit sees the light
const int JOB_DIFFUSE = 9;     // where the diffusion sample enters the skin
const int JOB_ENTRY_SEES = 10; // 10-11: whether the entry sees key and fill
const int JOB_ROOM = 12;       // the HDRI seen along a cosine-weighted direction
const int JOB_BOUNCE = 13;     // the diffuse bounce
const int JOB_BOUNCE_SEES = 14;// 14-15: whether the bounce sees key and fill
const int JOB_REFLECT = 16;    // whether the HDRI's reflection is blocked
const int JOB_COUNT = 17;

vec3 skinShade(vec3 viewNormal, vec3 viewDirection) {
    skinPixel=uvec2(gl_FragCoord.xy);
    skinPair=0;
    mat3 toWorld=transpose(uNormalMatrix);
    vec3 n=normalize(toWorld*viewNormal), v=normalize(toWorld*viewDirection);
    // Offsets use the geometric normal, independent of normal simplification.
    vec3 gn=normalize(cross(dFdx(vWorldPosition),dFdy(vWorldPosition)));
    if (dot(gn,v)<0.0) gn=-gn;
    vec3 p=vWorldPosition;
    vec3 key=skinLight(normalize(toWorld*uKeyDirection),skinRandom2());
    vec3 fill=skinLight(normalize(toWorld*uFillDirection),skinRandom2());
    // Traced, the HDRI is a third light: one direction per sample, picked in
    // proportion to the light arriving along it, carrying radiance / density.
    vec2 envXi=skinRandom2();
    vec3 envDirection=vec3(0.0,1.0,0.0), envLit=vec3(0.0);
    if (uSkinTrace && uEnvOn) {
        vec3 radiance;
        float density;
        envDirection=envSample(envXi,radiance,density);
        envLit=density>0.0 ? radiance/density : vec3(0.0);
    }
    // The relief and the marks are fetched on every path so the derivatives
    // they need stay defined.
    SkinSurface surface=skinRelief(p);
    SkinRegion region=skinRegion(p);
    SkinMarks marks=skinMarks(p,n,region);
    float detail=uSkinFurniture ? 0.0 : uSkinDetail*surface.fade;
    float oil=uSkinFurniture ? 0.0 : clamp(uSkinOil*region.oil+marks.oil,0.0,1.0);
    float roughness=clamp(uSkinRoughness+(uSkinFurniture ? 0.0 : marks.rough),0.12,1.0);
    float blood=uSkinFurniture ? 0.0 : clamp(uSkinBlood*region.blood,0.0,1.0);
    // A mark's own relief is not the artist's detail slider: a papule stands
    // up on the smoothest skin.
    vec3 markSlope=uSkinFurniture ? vec3(0.0) : marks.slope;
    vec3 nSpec=skinBump(n,surface.slope*detail+markSlope,1.0);
    vec3 nDiff=skinBump(n,surface.slope*detail*0.35+markSlope*0.6,1.0);
    vec3 albedo=uSkinFurniture ? skinLinear(uDiffuseColor)
        : clamp(skinAlbedo(skinLinear(uSkinColor),surface,blood)*marks.tint,0.0,1.0);
    vec3 lengths=skinDiffusionLengths(albedo);
    float sphereRadius=skinSphereRadius(n);
    float sss=uSkinFurniture ? 0.0 : uSkinSSS;
    float nv=max(dot(nSpec,v),0.0);
    vec3 fuzzColor=mix(albedo,vec3(1.0),0.6);
    float rim=pow(1.0-max(dot(n,v),0.0),3.0);
    vec3 reflected=reflect(-v,nSpec);
    // Screen-space occlusion stands in for traced visibility in the preview;
    // a cavity goes red before it goes dark, blue being absorbed first, and
    // more so the more blood there is under the surface.
    float ao=uSkinTrace ? 1.0 : occlusionFactor();
    vec3 tint=uSkinFurniture ? vec3(ao)
            : pow(vec3(ao),1.0+(1.0-uSkinScatter)*(1.0+2.0*blood));
    vec3 ls[3]=vec3[3](key,fill,envDirection);
    vec3 powers[3]=vec3[3](skinLinear(uLightColor)*uKeyIntensity,
                           skinLinear(uLightColor)*uFillIntensity, envLit);
    bool on[3];
    for (int i=0;i<3;++i) on[i]=max(powers[i].r,max(powers[i].g,powers[i].b))>0.0;

    // -- the traced sample's rays ------------------------------------------
    float seen[3]=float[3](0.0,0.0,0.0);
    vec3 carried[3]=vec3[3](vec3(0.0),vec3(0.0),vec3(0.0));
    vec3 exitPoint[3]=vec3[3](vec3(0.0),vec3(0.0),vec3(0.0));
    bool exits[3]=bool[3](false,false,false);
    float entrySeen[3]=float[3](0.0,0.0,0.0);
    float bounceSeen[2]=float[2](0.0,0.0);
    bool entered=false, bounced=false;
    vec3 entry=p, entryNormal=n, bouncePoint=p, bounceNormal=n, bounceColor=vec3(0.0);
    float reflectSeen=1.0, roomSeen=1.0;
    float r=0.0;
    vec3 diffuseOrigin=p, bounceDirection=n, reflectRay=reflected, roomRay=nDiff;
    float height=0.0;
    if (uSkinTrace) {
        // The random numbers are drawn in a fixed order whatever runs, so
        // each keeps its own stratified sequence.
        vec2 pick=skinRandom2(), spot=skinRandom2(), turn=skinRandom2(), wobble=skinRandom2();
        vec2 hemi=skinRandom2();
        float hz=sqrt(hemi.y), hr=sqrt(max(0.0,1.0-hemi.y));
        roomRay=skinBasis(nDiff)*vec3(hr*cos(2.0*PI*hemi.x),hr*sin(2.0*PI*hemi.x),hz);
        // One Burley-distributed radius: a quarter from the short
        // exponential, three quarters from the one three times longer.
        int channel=min(int(pick.x*3.0),2);
        float reach=pick.y<0.25 ? 1.0 : 3.0;
        r=-log(max(1.0-spot.x,1e-5))*lengths[channel]*reach;
        float phi=2.0*PI*spot.y;
        height=max(3.0*uSkinRadius,r);
        diffuseOrigin=p+skinBasis(gn)*vec3(r*cos(phi),r*sin(phi),0)+gn*height;
        // One diffuse bounce, cosine-distributed.
        float z=sqrt(turn.y), across=sqrt(max(0.0,1.0-turn.y));
        bounceDirection=skinBasis(nDiff)*vec3(across*cos(2.0*PI*turn.x),
                                              across*sin(2.0*PI*turn.x),z);
        // The reflection's visibility, thrown a lobe's width about the
        // mirror direction.
        reflectRay=normalize(skinBasis(reflected)*vec3(
            (wobble-0.5)*2.0*roughness*roughness,1.0));
        for (int job=0;job<JOB_COUNT;++job) {
            vec3 origin=p+gn*uSkinEpsilon, ray=vec3(0.0,1.0,0.0);
            float reach=1e30;
            bool any=true, run=false;
            if (job<JOB_EXIT) {
                int i=job;
                ray=ls[i];
                run=on[i] && (dot(n,ray)>0.0 || dot(nDiff,ray)>0.0);
            } else if (job<JOB_EXIT_SEES) {
                int i=job-JOB_EXIT;
                ray=ls[i];
                origin=p-gn*uSkinEpsilon;
                reach=uSkinRadius*12.0;
                any=false;
                run=on[i] && !uSkinFurniture && dot(n,ray)<0.0
                    && uSkinTransmission>0.0 && sss>0.0;
            } else if (job<JOB_DIFFUSE) {
                int i=job-JOB_EXIT_SEES;
                ray=ls[i];
                origin=exitPoint[i]+ray*uSkinEpsilon;
                run=exits[i];
            } else if (job==JOB_DIFFUSE) {
                origin=diffuseOrigin;
                ray=-gn;
                reach=2.0*height;
                any=false;
                run=sss>0.0;
            } else if (job<JOB_ROOM) {
                int i=job-JOB_ENTRY_SEES;
                ray=ls[i];
                origin=entry+entryNormal*uSkinEpsilon;
                run=entered && on[i] && dot(entryNormal,ray)>0.0;
            } else if (job==JOB_ROOM) {
                ray=roomRay;
                run=uEnvOn && dot(ray,gn)>0.0;
            } else if (job==JOB_BOUNCE) {
                ray=bounceDirection;
                any=false;
                run=uSkinIndirect>0.0;
            } else if (job<JOB_REFLECT) {
                int i=job-JOB_BOUNCE_SEES;
                ray=ls[i];
                origin=bouncePoint+bounceNormal*uSkinEpsilon;
                run=bounced && on[i] && dot(bounceNormal,ray)>0.0;
            } else {
                ray=reflectRay;
                run=uEnvOn && !uSkinFurniture && dot(ray,gn)>0.0;
            }
            if (!run) continue;
            float distance=reach;
            vec2 bary;
            int hit=skinTrace(origin,ray,distance,any,bary);
            if (any) {
                float open=hit<0 ? 1.0 : 0.0;
                if (job<JOB_EXIT) seen[job]=open;
                else if (job<JOB_DIFFUSE) carried[job-JOB_EXIT_SEES]*=open;
                else if (job<JOB_ROOM) entrySeen[job-JOB_ENTRY_SEES]=open;
                else if (job==JOB_ROOM) roomSeen=open;
                else if (job<JOB_REFLECT) bounceSeen[job-JOB_BOUNCE_SEES]=open;
                else reflectSeen=open;
                continue;
            }
            if (hit<0) continue;
            // A nearest hit: read what it hit, once.
            vec4 n0=skinTexel(uSkinAttributes,hit*3);
            vec4 n1=skinTexel(uSkinAttributes,hit*3+1);
            vec4 n2=skinTexel(uSkinAttributes,hit*3+2);
            vec3 normal=n0.xyz*(1.0-bary.x-bary.y)+n1.xyz*bary.x+n2.xyz*bary.y;
            if (dot(normal,normal)<1e-12)
                normal=cross(skinTexel(uSkinTriangles,hit*3+1).xyz,
                             skinTexel(uSkinTriangles,hit*3+2).xyz);
            normal=normalize(normal);
            bool skin=mod(skinTexel(uSkinTriangles,hit*3).w,2.0)<0.5;
            if (job<JOB_EXIT_SEES) {
                int i=job-JOB_EXIT;
                if (skin) {
                    exits[i]=true;
                    exitPoint[i]=origin+ray*distance;
                    carried[i]=exp(-distance/max(uSkinRadius*uSkinScatter,vec3(uSkinEpsilon)));
                }
            } else if (job==JOB_DIFFUSE) {
                if (skin && dot(normal,n)>0.25) {
                    entered=true;
                    entry=origin+ray*distance;
                    entryNormal=normal;
                }
            } else {
                bounced=true;
                bounceNormal=dot(normal,ray)>0.0 ? -normal : normal;
                bouncePoint=origin+ray*distance;
                bounceColor=skin ? skinLinear(uSkinColor)
                                 : skinLinear(vec3(n0.w,n1.w,n2.w));
            }
        }
    }

    // How much of the HDRI's light reaches the point, as a share: the two
    // rays thrown at it -- one where the map is bright, one about the normal
    // -- weighted by the light each would have brought.  The share times the
    // map's smooth irradiance is the traced HDRI.  Its noise is only the
    // noise of the visibility, where radiance over density on its own is
    // the noise of a whole panorama squeezed through one direction a sample.
    float envShare=1.0;
    if (uSkinTrace && uEnvOn) {
        const vec3 LUMA=vec3(0.2126,0.7152,0.0722);
        float w0=dot(envLit,LUMA)*max(dot(nDiff,envDirection),0.0)*(on[2] ? 1.0 : 0.0);
        float w1=dot(roomRay,gn)>0.0 ? PI*dot(envRadiance(roomRay,2.0),LUMA) : 0.0;
        envShare=w0+w1>0.0 ? (w0*seen[2]+w1*roomSeen)/(w0+w1) : 1.0;
    }

    // -- the lights ----------------------------------------------------------
    vec3 result=vec3(0), localIrradiance=vec3(0), wrapIrradiance=vec3(0);
    for (int i=0;i<3;++i) {
        if (!on[i]) continue;
        vec3 power=powers[i];
        vec3 l=ls[i];
        float nl=max(dot(nDiff,l),0.0);
        if (i==2) {
            // The HDRI's sample only carries its backlight; its diffuse is
            // the share above, its sheen the harmonics'.
            if (dot(n,l)<0.0 && uSkinTransmission>0.0 && exits[2] && !uSkinFurniture)
                result += albedo*SKIN_FLUSH*power*carried[2]*max(-dot(n,l),0.0)
                        *uSkinTransmission*sss/PI;
            continue;
        }
        // A light behind the surface is not looked for through the body: it
        // is blocked by definition, and what it gives is transmission.
        float visibility=uSkinTrace ? seen[i]
                         : (i==0 ? shadowFactor(max(dot(n,l),0.0)) : 1.0);
        vec3 lit=power*visibility;
        localIrradiance += lit*nl;
        if (!uSkinTrace) wrapIrradiance += lit*skinWrap(dot(n,l),lengths,sphereRadius);
        if (uSkinFurniture) continue;
        // The HDRI's highlights are read off the blurred map below, where a
        // direction picked for its light rather than for the lobe would only
        // make fireflies of the oily sheen.
        if (i<2) result += skinSpec(nSpec,v,l,roughness,oil)*lit*max(dot(nSpec,l),0.0);
        if (uSkinFuzz>0.0) {
            // Vellus hair catches light at the rim, from the lit side and a
            // little from behind; it is not occluded the way the surface is.
            float side=clamp(dot(n,l)*0.5+0.5,0.0,1.0);
            vec3 seenPower=mix(power,lit,step(0.0,dot(n,l)));
            result += fuzzColor*seenPower*rim*side*uSkinFuzz/PI;
        }
        if (dot(n,l)<0.0 && uSkinTransmission>0.0) {
            // Traced: Beer's law through the thickness to where the light
            // leaves, if the light can see that exit.  Previewed: a cheap
            // wrap standing in for it, with no thickness to go on.
            vec3 transmission=uSkinTrace ? (exits[i] ? carried[i] : vec3(0.0))
                                         : uSkinScatter*0.15;
            vec3 source=uSkinTrace ? power : lit;
            result += albedo*SKIN_FLUSH*source*transmission*max(-dot(n,l),0.0)
                    *uSkinTransmission*sss/PI;
        }
    }
    if (uEnvOn && !uSkinTrace) {
        // The HDRI in the preview, from its harmonics: the diffusion softens
        // the higher bands the way the table softens the key's terminator,
        // and the shadow map, cast from the map's dominant light when it is
        // the only light, takes that light's share out where it is blocked.
        vec3 sun=normalize(toWorld*uEnvSunView);
        float blocked=uEnvShadow ? 1.0-shadowFactor(max(dot(n,sun),0.0)) : 0.0;
        vec3 soften=clamp(2.0*lengths/sphereRadius,0.0,1.0);
        vec3 direct=max(envIrradiance(nDiff)-blocked*uEnvSunColor*max(dot(nDiff,sun),0.0),
                        vec3(0.0));
        vec3 wrapped=max(envIrradianceSoft(n,soften)
                         -blocked*uEnvSunColor*max(dot(n,sun),0.0),vec3(0.0));
        localIrradiance += direct*tint;
        wrapIrradiance += wrapped*tint;
        if (!uSkinFurniture) {
            result += albedo*SKIN_FLUSH*envIrradiance(-n)*uSkinScatter*0.15
                    *uSkinTransmission*sss/PI;
        }
    }
    if (uEnvOn && uSkinTrace) localIrradiance += envIrradiance(nDiff)*envShare;
    if (uEnvOn && !uSkinFurniture) {
        // Vellus hair against the room, not occluded, as against the key.
        result += fuzzColor*envIrradiance(n)*rim*uSkinFuzz*0.5/PI;
    }

    // -- diffusion -----------------------------------------------------------
    vec3 diffuseIrradiance=localIrradiance;
    if (sss>0.0) {
        if (uSkinTrace) {
            vec3 scattered=localIrradiance;
            if (entered) {
                // The entry is a diffusion length away: near enough to share
                // the point's view of the room.
                scattered=uEnvOn ? envIrradiance(entryNormal)*envShare : vec3(0.0);
                for (int i=0;i<2;++i)
                    if (on[i]) scattered += powers[i]*max(dot(entryNormal,ls[i]),0.0)*entrySeen[i];
            }
            // Radial PDF mixture across channels; the 2*pi*r factors cancel.
            vec3 pdf=(0.25*exp(-r/lengths)+0.25*exp(-r/(3.0*lengths)))/lengths;
            vec3 weights=pdf/max(dot(pdf,vec3(1.0/3.0)),1e-20);
            diffuseIrradiance=mix(localIrradiance,scattered*weights,sss);
        } else {
            diffuseIrradiance=mix(localIrradiance,wrapIrradiance,sss);
        }
    }
    vec3 fresnelView=uSkinFurniture ? vec3(0.0) : skinFresnel(nv);
    vec3 diffuseWeight=albedo*(1.0-fresnelView);
    result += diffuseWeight*diffuseIrradiance/PI;

    // -- what the room gives -------------------------------------------------
    vec3 gloss=fresnelView*(1.0-0.7*roughness);
    if (uEnvOn && !uSkinFurniture) {
        // The HDRI's reflection, blurred to the broad lobe, hidden where the
        // traced ray found the body in the way or the occlusion says so.
        result += gloss*envRadiance(reflected,envLod(roughness))*(uSkinTrace ? reflectSeen : ao);
    }
    if (!uSkinTrace) {
        result += diffuseWeight*skinEnvironment(nDiff)*tint*uSkinIndirect;
        result += gloss*skinEnvironment(reflected)*ao*uSkinIndirect;
    } else if (uSkinIndirect>0.0) {
        // One diffuse path bounce. Cosine sampling cancels cos(theta)/pi.
        vec3 incoming;
        if (bounced) {
            // The light that reached the bounce: key and fill as traced, the
            // HDRI from its harmonics -- plenty for light bounced once.
            vec3 arriving=envIrradiance(bounceNormal);
            for (int i=0;i<2;++i)
                if (on[i]) arriving += powers[i]*max(dot(bounceNormal,ls[i]),0.0)*bounceSeen[i];
            incoming=bounceColor*arriving/PI;
        } else {
            // A miss sees the studio sky.  Not the HDRI: that was sampled
            // as a light above, and counting it here as well would count
            // it twice.
            incoming=skinEnvironment(bounceDirection);
        }
        result += diffuseWeight*incoming*uSkinIndirect;
        // Glossy paths are not traced; the hemisphere stands in for them.
        result += gloss*skinEnvironment(reflected)*uSkinIndirect;
    }
    result *= exp2(uSkinExposure);
    // The accumulation pass reverses this transform before averaging in
    // radiance space, preserving legacy overlays drawn into the same frame.
    return skinDisplay(result/(1.0+result));
}
