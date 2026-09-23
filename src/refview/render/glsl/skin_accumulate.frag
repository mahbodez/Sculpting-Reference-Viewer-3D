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
