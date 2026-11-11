#version 460 core
#include <flutter/runtime_effect.glsl>

// Full-screen color grade over the shared art: day is untouched, dusk is warm, night is a blue ramp.
// The scene arrives as a low-resolution image; sampling is snapped to texel centres to keep pixels square.
uniform vec2 uSize;    // size of the drawn rectangle
uniform vec2 uTexels;  // size of the scene image in pixels
uniform float uTime;   // 0 = midnight, 0.5 = noon
uniform sampler2D uScene;

out vec4 fragColor;

const float TAU = 6.28318530718;

void main() {
    vec2 uv = FlutterFragCoord().xy / uSize;
    uv = (floor(uv * uTexels) + 0.5) / uTexels;
    vec3 c = texture(uScene, uv).rgb;
    float lum = dot(c, vec3(0.299, 0.587, 0.114));
    float sun = 0.5 - 0.5 * cos(uTime * TAU);
    float night = 1.0 - smoothstep(0.15, 0.45, sun);
    float dusk = smoothstep(0.1, 0.35, sun) * (1.0 - smoothstep(0.35, 0.7, sun));
    vec3 duskC = c * vec3(1.15, 0.85, 0.7) + vec3(0.06, 0.0, 0.03);
    vec3 nightC = mix(vec3(0.04, 0.05, 0.14), vec3(0.45, 0.55, 0.85), lum);
    c = mix(c, duskC, dusk * 0.8);
    c = mix(c, nightC, night * 0.9);
    fragColor = vec4(c, 1.0);
}
