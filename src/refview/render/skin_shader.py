"""Skin BRDF and bounded-depth light transport, shared by preview and refinement.

The surface carries three normals: the relief-bumped one for the specular
lobes, a gentler bump for diffuse, and the smooth geometric one for diffusion,
since light that has travelled through the dermis has forgotten the pores it
entered by. Two dielectric GGX lobes approximate broad skin and narrow sebum
reflections; a grazing sheen stands in for vellus hair. Albedo is unevenly
pigmented and flushed with blood from the same tileable volume that carries
the relief. Diffusion follows Burley's normalised profile: the preview reads a
curvature-indexed pre-integration of it, idle samples draw radii from it and
project them onto the nearby surface. Transmission is Beer attenuation through
the traced thickness. This is an RGB diffusion approximation, not a spectral
layered tissue or volumetric random-walk solver.

The marks -- freckles, moles and acne -- are round spots on jittered lattices
worked out in the shader from the world position: each lattice cell holds at
most one spot, jittered by no more than a quarter of the cell and no wider
than a quarter, so the cell a point falls in is the only one that can mark
it and one hash per lattice decides everything about that spot.  Blemishes
are patches read off the relief volume's tone channel at a coarser scale.
Where each falls, and how thickly, is scaled by the body map: a small volume
of region weights laid over the scene, read at the same world position, and
a multiplier per region and per kind of mark.
"""

from .skin_detail import LUT_LOG_MIN, LUT_LOG_SPAN, RELIEF_CELLS

SKIN_GLSL = """
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
uniform bool uSkinTrace;
uniform bool uSkinFurniture;
uniform int uSkinSample;
uniform int uSkinNodeCount;
uniform sampler2D uSkinNodes;
uniform sampler2D uSkinTriangles;
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
uint skinSeed;
float skinRandom() {
    skinSeed ^= skinSeed << 13u;
    skinSeed ^= skinSeed >> 17u;
    skinSeed ^= skinSeed << 5u;
    return (float(skinSeed & 0x00ffffffu) + 0.5) / 16777216.0;
}
mat3 skinBasis(vec3 n) {
    vec3 t = normalize(cross(abs(n.z) < 0.9 ? vec3(0,0,1) : vec3(0,1,0), n));
    return mat3(t, cross(n, t), n);
}
vec4 skinTexel(sampler2D table, int index) {
    int width = textureSize(table, 0).x;
    return texelFetch(table, ivec2(index % width, index / width), 0);
}
bool skinClipped(vec3 p) {
    for (int i=0; i<uSectionCount; ++i)
        if (dot(p, uSectionPlanes[i].xyz) > uSectionPlanes[i].w) return true;
    return false;
}
struct SkinHit { float distance; vec3 normal; vec3 color; int material; };
bool skinRay(vec3 origin, vec3 ray, float reach, out SkinHit hit) {
    hit.distance = reach;
    hit.material = -1;
    vec3 safeRay = mix(ray, mix(vec3(-1e-12), vec3(1e-12), step(vec3(0), ray)),
                        lessThan(abs(ray), vec3(1e-12)));
    vec3 inv = 1.0 / safeRay;
    int node = 0;
    while (node < uSkinNodeCount) {
        vec4 low = skinTexel(uSkinNodes, node*3);
        vec4 high = skinTexel(uSkinNodes, node*3+1);
        vec3 a = (low.xyz - origin)*inv, b = (high.xyz - origin)*inv;
        vec3 near = min(a,b), far = max(a,b);
        float entry = max(max(near.x, near.y), max(near.z, 0.0));
        float exitDistance = min(min(far.x, far.y), far.z);
        if (entry > exitDistance || entry > hit.distance) { node=int(low.w); continue; }
        int count = int(skinTexel(uSkinNodes, node*3+2).w);
        if (count == 0) { ++node; continue; }
        int first = int(high.w);
        for (int j=0; j<count; ++j) {
            int k = (first+j)*6;
            vec4 p0 = skinTexel(uSkinTriangles, k);
            vec3 e1 = skinTexel(uSkinTriangles, k+1).xyz-p0.xyz;
            vec3 e2 = skinTexel(uSkinTriangles, k+2).xyz-p0.xyz;
            vec3 q = cross(ray,e2);
            float det = dot(e1,q);
            if (abs(det) < 1e-12 * max(length(e1)*length(e2), 1e-20)) continue;
            vec3 s = origin-p0.xyz;
            float u = dot(s,q)/det;
            vec3 r = cross(s,e1);
            float v = dot(ray,r)/det, t = dot(e2,r)/det;
            if (u<0.0 || v<0.0 || u+v>1.0 || t<uSkinEpsilon*0.25
                || t>=hit.distance || skinClipped(origin+ray*t)) continue;
            vec4 n0=skinTexel(uSkinTriangles,k+3);
            vec4 n1=skinTexel(uSkinTriangles,k+4);
            vec4 n2=skinTexel(uSkinTriangles,k+5);
            vec3 normal = n0.xyz*(1.0-u-v)+n1.xyz*u+n2.xyz*v;
            if (dot(normal,normal)<1e-12) normal=cross(e1,e2);
            hit.normal=normalize(normal);
            hit.color=skinLinear(vec3(n0.w,n1.w,n2.w));
            hit.material=int(p0.w);
            hit.distance=t;
        }
        node=int(low.w);
    }
    return hit.material>=0;
}
float skinVisible(vec3 p, vec3 n, vec3 l) {
    SkinHit hit;
    return skinRay(p+n*uSkinEpsilon, l, 1e30, hit) ? 0.0 : 1.0;
}
vec3 skinLight(vec3 direction) {
    if (!uSkinTrace || uSkinLightSize<=0.0) return direction;
    float angle=2.0*PI*skinRandom();
    float c=mix(1.0, cos(uSkinLightSize), skinRandom());
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
vec3 skinEnvironment(vec3 direction) {
    return skinLinear(uAmbientColor)*uAmbientIntensity
         * mix(0.35,1.0,clamp(direction.y*0.5+0.5,0.0,1.0));
}
vec3 skinIrradiance(vec3 p, vec3 n, vec3 key, vec3 fill) {
    vec3 result=vec3(0);
    vec3 ls[2]=vec3[2](key,fill);
    float powers[2]=float[2](uKeyIntensity,uFillIntensity);
    for (int i=0;i<2;++i) {
        float cosine=max(dot(n,ls[i]),0.0);
        if (cosine>0.0 && powers[i]>0.0)
            result += skinLinear(uLightColor)*powers[i]*cosine*skinVisible(p,n,ls[i]);
    }
    return result;
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
vec3 skinShade(vec3 viewNormal, vec3 viewDirection) {
    skinSeed=uint(gl_FragCoord.x)*1973u+uint(gl_FragCoord.y)*9277u
            +uint(uSkinSample+1)*26699u+1u;
    mat3 toWorld=transpose(uNormalMatrix);
    vec3 n=normalize(toWorld*viewNormal), v=normalize(toWorld*viewDirection);
    // Offsets use the geometric normal, independent of normal simplification.
    vec3 gn=normalize(cross(dFdx(vWorldPosition),dFdy(vWorldPosition)));
    if (dot(gn,v)<0.0) gn=-gn;
    vec3 p=vWorldPosition;
    vec3 key=skinLight(normalize(toWorld*uKeyDirection));
    vec3 fill=skinLight(normalize(toWorld*uFillDirection));
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
    vec3 result=vec3(0), localIrradiance=vec3(0), wrapIrradiance=vec3(0);
    vec3 ls[2]=vec3[2](key,fill);
    float powers[2]=float[2](uKeyIntensity,uFillIntensity);
    for (int i=0;i<2;++i) {
        if (powers[i]<=0.0) continue;
        vec3 l=ls[i];
        float nl=max(dot(nDiff,l),0.0);
        float visibility=uSkinTrace ? skinVisible(p,gn,l)
                         : (i==0 ? shadowFactor(max(dot(n,l),0.0)) : 1.0);
        vec3 lit=skinLinear(uLightColor)*powers[i]*visibility;
        localIrradiance += lit*nl;
        if (!uSkinTrace) wrapIrradiance += lit*skinWrap(dot(n,l),lengths,sphereRadius);
        if (uSkinFurniture) continue;
        result += skinSpec(nSpec,v,l,roughness,oil)*lit*max(dot(nSpec,l),0.0);
        if (uSkinFuzz>0.0) {
            // Vellus hair catches light at the rim, from the lit side and a
            // little from behind; it is not occluded the way the surface is.
            float rim=pow(1.0-max(dot(n,v),0.0),3.0);
            float side=clamp(dot(n,l)*0.5+0.5,0.0,1.0);
            vec3 seen=mix(skinLinear(uLightColor)*powers[i],lit,step(0.0,dot(n,l)));
            result += fuzzColor*seen*rim*side*uSkinFuzz/PI;
        }
        if (dot(n,l)<0.0 && uSkinTransmission>0.0) {
            vec3 transmission=vec3(0);
            if (uSkinTrace) {
                SkinHit exitHit;
                vec3 origin=p-gn*uSkinEpsilon;
                if (skinRay(origin,l,uSkinRadius*12.0,exitHit) && exitHit.material==0) {
                    vec3 exitPoint=origin+l*exitHit.distance;
                    SkinHit obstruction;
                    if (!skinRay(exitPoint+l*uSkinEpsilon,l,1e30,obstruction))
                        transmission=exp(-exitHit.distance /
                            max(uSkinRadius*uSkinScatter,vec3(uSkinEpsilon)));
                }
            } else {
                // Deliberately cheap wrap/backlight preview, no thickness query.
                transmission=uSkinScatter*0.15;
            }
            result += albedo*SKIN_FLUSH*lit*transmission*max(-dot(n,l),0.0)
                    *uSkinTransmission*sss/PI;
        }
    }
    vec3 diffuseIrradiance=localIrradiance;
    if (sss>0.0) {
        if (uSkinTrace) {
            // One Burley-distributed radius: a quarter from the short
            // exponential, three quarters from the one three times longer.
            int channel=min(int(skinRandom()*3.0),2);
            float reach=skinRandom()<0.25 ? 1.0 : 3.0;
            float r=-log(max(1.0-skinRandom(),1e-5))*lengths[channel]*reach;
            float phi=2.0*PI*skinRandom();
            vec3 offset=skinBasis(gn)*vec3(r*cos(phi),r*sin(phi),0);
            float height=max(3.0*uSkinRadius,r);
            SkinHit sampleHit;
            vec3 origin=p+offset+gn*height;
            vec3 scattered=localIrradiance;
            if (skinRay(origin,-gn,2.0*height,sampleHit) && sampleHit.material==0
                && dot(sampleHit.normal,n)>0.25) {
                vec3 entry=origin-gn*sampleHit.distance;
                scattered=skinIrradiance(entry,sampleHit.normal,key,fill);
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
    vec3 gloss=fresnelView*(1.0-0.7*roughness);
    if (!uSkinTrace) {
        float ao=occlusionFactor();
        // A cavity goes red before it goes dark: blue is absorbed first, and
        // more so the more blood there is under the surface.
        vec3 tint=uSkinFurniture ? vec3(ao)
                : pow(vec3(ao),1.0+(1.0-uSkinScatter)*(1.0+2.0*blood));
        result += diffuseWeight*skinEnvironment(nDiff)*tint*uSkinIndirect;
        result += gloss*skinEnvironment(reflect(-v,nSpec))*ao*uSkinIndirect;
    } else if (uSkinIndirect>0.0) {
        // One diffuse path bounce. Cosine sampling cancels cos(theta)/pi.
        float phi=2.0*PI*skinRandom(), z=sqrt(skinRandom());
        float r=sqrt(max(0.0,1.0-z*z));
        vec3 direction=skinBasis(nDiff)*vec3(r*cos(phi),r*sin(phi),z);
        SkinHit bounce;
        vec3 incoming;
        if (skinRay(p+gn*uSkinEpsilon,direction,1e30,bounce)) {
            vec3 bn=bounce.normal;
            if (dot(bn,direction)>0.0) bn=-bn;
            vec3 bp=p+gn*uSkinEpsilon+direction*bounce.distance;
            vec3 bc=bounce.material==0 ? skinLinear(uSkinColor) : bounce.color;
            incoming=bc*skinIrradiance(bp,bn,key,fill)/PI;
        } else incoming=skinEnvironment(direction);
        result += diffuseWeight*incoming*uSkinIndirect;
        // Glossy paths are not traced; the hemisphere stands in for them.
        result += gloss*skinEnvironment(reflect(-v,nSpec))*uSkinIndirect;
    }
    result *= exp2(uSkinExposure);
    // The accumulation pass reverses this transform before averaging in
    // radiance space, preserving legacy overlays drawn into the same frame.
    return skinDisplay(result/(1.0+result));
}
""".replace("@CELLS@", f"{float(RELIEF_CELLS)}").replace(
    "@LUT_MIN@", f"{float(LUT_LOG_MIN)}").replace("@LUT_SPAN@", f"{float(LUT_LOG_SPAN)}")

ACCUMULATE_FRAGMENT = """
#version 330 core
in vec2 vUv;
out vec4 fragColor;
uniform sampler2D uCurrent;
uniform sampler2D uHistory;
uniform int uSamples;
void main() {
    vec3 current=texture(uCurrent,vUv).rgb;
    current=mix(current/12.92,pow((current+0.055)/1.055,vec3(2.4)),
                step(vec3(0.04045),current));
    // Undo the display transform before accumulation. This also keeps the
    // legacy background, clay, and overlay colours unchanged on presentation.
    current=current/max(vec3(1e-5),1.0-current);
    vec3 previous=uSamples==0 ? vec3(0) : texture(uHistory,vUv).rgb;
    fragColor=vec4(previous+(current-previous)/float(uSamples+1),1);
}
"""

PRESENT_FRAGMENT = """
#version 330 core
in vec2 vUv;
out vec4 fragColor;
uniform sampler2D uFrame;
void main() {
    vec3 color=max(texture(uFrame,vUv).rgb,vec3(0));
    color=color/(1.0+color);
    color=mix(12.92*color,1.055*pow(color,vec3(1.0/2.4))-0.055,
              step(vec3(0.0031308),color));
    fragColor=vec4(color,1);
}
"""
