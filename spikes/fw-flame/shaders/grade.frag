#version 460 core
#include <flutter/runtime_effect.glsl>

// Full-screen color grade over the shared art: day is untouched, dusk is warm, night is a blue ramp.
// Two point lights bring the ungraded, warmed art back around a campfire and a window when it is dark.
// The scene arrives as a low-resolution image; sampling is snapped to texel centres to keep pixels square.
uniform vec2 uSize;    // size of the drawn rectangle
uniform vec2 uTexels;  // size of the scene image in pixels
uniform float uTime;   // 0 = midnight, 0.5 = noon
uniform vec4 uLight0;  // x, y in scene pixels, radius in scene pixels, strength
uniform vec4 uLight1;
uniform sampler2D uScene;
uniform sampler2D uMask;  // alpha > 0 where a light may reach (near layers only)

out vec4 fragColor;

const float TAU = 6.28318530718;
const float BANDS = 5.0;

// Light falloff in a few flat steps, with a 2x2 dither between steps, instead of a smooth gradient.
float glow(vec4 light, vec2 texel) {
    float f = clamp(1.0 - distance(texel, light.xy) / max(light.z, 1.0), 0.0, 1.0);
    f = f * f * BANDS;
    float dither = mod(texel.x + texel.y, 2.0) * 0.5 + 0.25;
    return (floor(f) + step(dither, fract(f))) / BANDS * light.w;
}

void main() {
    vec2 uv = FlutterFragCoord().xy / uSize;
    vec2 texel = floor(uv * uTexels);
    uv = (texel + 0.5) / uTexels;
    vec3 base = texture(uScene, uv).rgb;
    vec3 c = base;
    float lum = dot(c, vec3(0.299, 0.587, 0.114));
    float sun = 0.5 - 0.5 * cos(uTime * TAU);
    float night = 1.0 - smoothstep(0.15, 0.45, sun);
    float dusk = smoothstep(0.1, 0.35, sun) * (1.0 - smoothstep(0.35, 0.7, sun));
    vec3 duskC = c * vec3(1.15, 0.85, 0.7) + vec3(0.06, 0.0, 0.03);
    vec3 nightC = mix(vec3(0.04, 0.05, 0.14), vec3(0.45, 0.55, 0.85), lum);
    c = mix(c, duskC, dusk * 0.8);
    c = mix(c, nightC, night * 0.9);

    float dark = 1.0 - smoothstep(0.3, 0.65, sun);
    float reach = step(0.5, texture(uMask, uv).a);
    float g = min(1.0, glow(uLight0, texel) + glow(uLight1, texel)) * dark * reach;
    vec3 lit = base * vec3(1.25, 0.95, 0.6) + vec3(0.10, 0.04, 0.0);
    c = mix(c, lit, g);
    fragColor = vec4(c, 1.0);
}
