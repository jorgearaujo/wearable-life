#version 460 core
#include <flutter/runtime_effect.glsl>

// Second pass: the scene image holds palette indices, not colours (see tools/make_art.py).
//   red = index * 4, green = 1 where firelight may reach, blue = 1 where it floats on the water.
// The palette image has one row per time of day and one row of firelit colours, so night and dusk are
// full re-colourings, not a tint over the day art. That block of five rows is repeated once per season.
// Below the waterline the scene is mirrored.
uniform vec2 uSize;    // size of the drawn rectangle
uniform vec2 uTexels;  // size of the scene image in art pixels
uniform vec3 uTime;    // palette row A, palette row B, mix between them
uniform float uDark;   // 0 by day, 1 at night: how strongly lights show
uniform float uWaterY; // waterline in view pixels
uniform float uStep;   // counts up 8 times a second; drives the water shimmer
uniform float uWet;    // 0 clear, 1 rain or fog: pulls the colours down toward a cool grey
uniform float uCamX;   // left edge of the view in the world, so the glints stay put while the view moves
uniform vec3 uSeason;  // palette block A, palette block B, mix between them
uniform vec4 uLight0;  // x, y in view pixels, radius in art pixels, strength
uniform vec4 uLight1;
uniform sampler2D uScene;
uniform sampler2D uPalette;

out vec4 fragColor;

const vec2 PALETTE = vec2(64.0, 20.0);
const float SEASON_ROWS = 5.0;
const float LIT_ROW = 4.0;
const float WATER_TINT = 62.0;
const float WATER_HI = 63.0;
const float BANDS = 3.0;

vec3 entry(float index, float row, float season) {
    return texture(uPalette, (vec2(index, row + season * SEASON_ROWS) + 0.5) / PALETTE).rgb;
}

vec3 pal(float index, float row) {
    return mix(entry(index, row, uSeason.x), entry(index, row, uSeason.y), uSeason.z);
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

    // Anything drawn below the waterline with blue set floats on the water (a duck): it is shown as it is,
    // in place of the reflection.
    vec4 own = texture(uScene, (texel + 0.5) / uTexels);
    bool afloat = water && own.b > 0.5;
    if (afloat) {
        src = texel;
    }
    vec4 s = afloat ? own : texture(uScene, (src + 0.5) / uTexels);
    float index = floor(s.r * 255.0 / 4.0 + 0.5);
    vec3 c = now(index);
    // Weather mutes the scene before the lights are added, so firelight stays warm in rain. Real art would use hand-picked wet palette rows instead.
    float luma = dot(c, vec3(0.299, 0.587, 0.114));
    c = mix(c, luma * vec3(0.78, 0.86, 0.96), 0.5 * uWet);

    float g = min(1.0, glow(uLight0, src) + glow(uLight1, src)) * uDark * step(0.5, s.g);
    c = mix(c, pal(index, LIT_ROW), g);

    if (water && !afloat) {
        c = mix(c, now(WATER_TINT), 0.3 + min(0.25, depth / 160.0));
        // Calm glints: thin dashes of mixed length. Each one lives in its own 12-pixel cell of its row,
        // on its own slow beat (1.5 to 3.5 seconds), lit for half of it, short at the start and end of its
        // life, and in a new spot each time. All of them drift sideways one pixel a second.
        float wx = texel.x + uCamX - floor(uStep / 8.0) + floor(hash(vec2(texel.y, 7.0)) * 12.0);
        vec2 cell = vec2(floor(wx / 12.0), texel.y);
        float inCell = wx - cell.x * 12.0;
        float period = 12.0 + floor(hash(cell) * 17.0);
        float life = (uStep + floor(hash(cell + 0.5) * period)) / period;
        float age = fract(life);
        vec2 seed = cell + mod(floor(life), 64.0) * vec2(0.37, 0.11);
        // None on the bank's own reflection and few just below it; fewer still in rain and fog, so the ripples
        // of landing drops stand out.
        float chance = 0.11 * clamp((depth - 3.0) / 10.0, 0.0, 1.0) * (1.0 - 0.7 * uWet);
        float len = 1.0 + floor(pow(hash(seed + 0.3), 2.0) * 8.0);
        float start = floor(hash(seed + 0.7) * (13.0 - len));
        if (age < 0.08 || age > 0.42) {
            float cut = floor(len / 2.0);
            start += floor(cut / 2.0);
            len -= cut;
        }
        if (age < 0.5 && hash(seed) < chance && inCell >= start && inCell < start + len) {
            c = now(WATER_HI);
        }
    }
    fragColor = vec4(c, 1.0);
}
