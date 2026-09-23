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
