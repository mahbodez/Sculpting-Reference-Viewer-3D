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
vec3 skinSpec(vec3 n, vec3 v, vec3 l) {
    if (dot(n,l)<=0.0 || dot(n,v)<=0.0) return vec3(0);
    vec3 h=normalize(l+v);
    return skinFresnel(max(dot(v,h),0.0)) * mix(
        skinLobe(n,v,l,uSkinRoughness), skinLobe(n,v,l,0.18),uSkinOil);
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
vec3 skinAlbedo(vec3 base, SkinSurface s) {
    vec3 albedo=base*(1.0+uSkinMottle*0.22*(s.tone*2.0-1.0));
    float pooled=uSkinBlood*smoothstep(0.25,0.85,s.flush);
    return clamp(mix(albedo,albedo*SKIN_FLUSH,pooled),0.0,1.0);
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
    // The relief is fetched on every path so the derivatives it needs stay defined.
    SkinSurface surface=skinRelief(p);
    float detail=uSkinFurniture ? 0.0 : uSkinDetail*surface.fade;
    vec3 nSpec=skinBump(n,surface.slope,detail);
    vec3 nDiff=skinBump(n,surface.slope,detail*0.35);
    vec3 albedo=uSkinFurniture ? skinLinear(uDiffuseColor)
                               : skinAlbedo(skinLinear(uSkinColor),surface);
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
        result += skinSpec(nSpec,v,l)*lit*max(dot(nSpec,l),0.0);
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
    vec3 gloss=fresnelView*(1.0-0.7*uSkinRoughness);
    if (!uSkinTrace) {
        float ao=occlusionFactor();
        // A cavity goes red before it goes dark: blue is absorbed first, and
        // more so the more blood there is under the surface.
        vec3 tint=uSkinFurniture ? vec3(ao)
                : pow(vec3(ao),1.0+(1.0-uSkinScatter)*(1.0+2.0*uSkinBlood));
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
