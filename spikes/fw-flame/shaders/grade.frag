#version 460 core
#include <flutter/runtime_effect.glsl>

// Second pass: the scene image holds palette indices, not colours (see tools/make_art.py).
//   red = index * 4, green = 1 where firelight may reach.
// The palette image has one row per time of day and one row of firelit colours, so night and dusk are
// full re-colourings, not a tint over the day art. Below the waterline the scene is mirrored.
uniform vec2 uSize;    // size of the drawn rectangle
uniform vec2 uTexels;  // size of the scene image in art pixels
uniform vec3 uTime;    // palette row A, palette row B, mix between them
uniform float uDark;   // 0 by day, 1 at night: how strongly lights show
uniform float uWaterY; // waterline in view pixels
uniform float uStep;   // counts up 8 times a second; drives the water shimmer
uniform vec4 uLight0;  // x, y in view pixels, radius in art pixels, strength
uniform vec4 uLight1;
uniform sampler2D uScene;
uniform sampler2D uPalette;

out vec4 fragColor;

const vec2 PALETTE = vec2(64.0, 5.0);
const float LIT_ROW = 4.0;
const float WATER_TINT = 62.0;
const float WATER_HI = 63.0;
const float BANDS = 3.0;

vec3 pal(float index, float row) {
    return texture(uPalette, (vec2(index, row) + 0.5) / PALETTE).rgb;
}

vec3 now(float index) {
    return mix(pal(index, uTime.x), pal(index, uTime.y), uTime.z);
}

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

// Light falloff in a few clean flat bands: no gradient and no dither.
float glow(vec4 light, vec2 texel) {
    float f = clamp(1.0 - distance(texel, light.xy) / max(light.z, 1.0), 0.0, 1.0);
    return ceil(f * BANDS) / BANDS * light.w;
}

void main() {
    vec2 texel = floor(FlutterFragCoord().xy / uSize * uTexels);
    vec2 src = texel;
    float depth = texel.y - uWaterY;
    bool water = depth >= 0.0;
    if (water) {
        // Mirror about the waterline, then push whole rows sideways by a pixel or two: the broken,
        // streaky look of a reflection. Each row changes on its own beat, about once a second.
        src.y = uWaterY - 1.0 - depth;
        float beat = floor((uStep + hash(vec2(texel.y, 3.0)) * 8.0) / 8.0);
        float reach = min(1.0, depth / 6.0) * (1.0 + depth / 24.0);
        src.x += floor((hash(vec2(texel.y, beat)) - 0.5) * 3.0 * reach + 0.5);
        src = clamp(src, vec2(0.0), uTexels - 1.0);
    }

    vec4 s = texture(uScene, (src + 0.5) / uTexels);
    float index = floor(s.r * 255.0 / 4.0 + 0.5);
    vec3 c = now(index);

    float g = min(1.0, glow(uLight0, src) + glow(uLight1, src)) * uDark * step(0.5, s.g);
    c = mix(c, pal(index, LIT_ROW), g);

    if (water) {
        c = mix(c, now(WATER_TINT), 0.3 + min(0.25, depth / 160.0));
        // Sparse bright streaks, three pixels long, that come and go.
        float streak = hash(vec2(floor(texel.x / 3.0), texel.y) + floor(uStep / 6.0) * 0.37);
        if (streak > 0.975) {
            c = now(WATER_HI);
        }
    }
    fragColor = vec4(c, 1.0);
}
