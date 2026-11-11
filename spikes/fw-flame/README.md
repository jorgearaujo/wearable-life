# fw-flame (Phase 0 spike, throwaway)

The shared framework test from the Phase 0 plan, built in Flutter 3.47.9 with Flame 1.38.2. The first pass used the same placeholder art as `spikes/fw-godot`; the second pass (see below) has its own, made by `tools/make_art.py`.

- `lib/main.dart` — portrait scene, 120 px wide (180 in the first pass), integer scaling worked out by hand from the screen width; sky plus three layers with parallax; a panning camera (drag, or it drifts on its own); an animated character; a debug label; a placeholder campfire. Tap to hold a time of day. The step count through the `health` plugin was removed on 2026-11-11 (we write our own bridge, and the plugin writes health values to the phone's log); it is in the first commit.
- `shaders/grade.frag` — one full-screen shader that turns palette indices into colours for the time of day, adds two point lights (campfire, cabin window) when it is dark, and mirrors the water.
- `tools/make_art.py` — writes the indexed placeholder art and `palette.png` (needs Pillow; run from this folder).
- `lib/daylight.dart`, `test/daylight_test.dart` — a pure-logic function and its test, with no engine involved.
- `android/` — host project. The release build asks for no permission at all: no health permission, no `INTERNET`.

## Build

```sh
flutter build apk --release --target-platform android-arm64
adb install -r build/app/outputs/flutter-apk/app-release.apk
adb shell am start -n dev.wearablelife.fw_flame/.MainActivity
dart test        # pure-logic test, no device needed
```

For screenshots: `--dart-define=FIXED_TIME=0` holds one time of day (thousandths; 0 = midnight, 500 = noon).

## Results so far (2026-11-10)

| Check | Result |
| --- | --- |
| Scene, parallax, integer scaling | Works, but parallax and integer scaling are hand-written (about 80 lines). |
| Other screen sizes (emulator, 7 sizes from 720 to 1344 px wide) | First version drew uneven pixels on 3 of 6 sizes (1–3% of art pixels). After the fix in problem 5, every art pixel is an exact square on all 7. Godot was exact on all 6 it was run on with no extra work. |
| Day → night shader | Works after one fix (see problem 1). The scene is drawn to an image at 180 px wide every frame and the shader scales it up. |
| Rain | Works. Hand-written component; Flame's particle system was not needed for it. |
| Step count | Worked on the emulator through the `health` plugin, with no Kotlin written. Removed from the spike on 2026-11-11. |
| Release build on the emulator | Runs at about 29 fps with a worst frame of 70 ms; Godot reached 43–46 fps on the same emulator. Emulator numbers are not a fair measure. |
| Release build on a Pixel 7a | Runs on Vulkan at a steady 60 fps, worst frame 17 ms, 180×400 view at 6×, scene the right way up. About 195 MB memory (Godot: about 172 MB). |
| Memory on the emulator | About 60 MB. |
| Release APK, arm64 only | 16.0 MB as a file, about 7.7 MB when compressed, which approximates the download. |
| Battery on the phone, screen on, uncapped 60 fps | 82 mAh in 16 min 20 s (872 → 790 mAh, from the phone's own battery history), an average of about 300 mA. Battery level 26% → 23%, adaptive brightness on. Same as Godot within the precision of the measurement. |
| Unit tests | `dart test` runs outside any engine. About 5 s including start-up. |
| Frame-rate cap | Not built. Flutter has no built-in cap. |

## Lighting beyond a full-screen grade (2026-11-11)

Question (risk 3 of the framework decision): Flame has no 2D lights, so can a campfire glow and a lit cabin window be built, stay pixel-exact, and leave the sky alone?

**Answer: yes, inside the grade shader we already have, with about 60 more lines.** Checked on the emulator only, in release builds, at a fixed midnight.

How it works:

- The shader gets each light as four numbers (position in view pixels, radius, strength). Inside a light's radius it mixes the night-graded pixel back toward the original daytime pixel with a warm tint, so the art's own colors return near the fire. The lights fade in as it gets dark and are off by day.
- **The falloff is stepped, not smooth:** five flat bands with a checkerboard dither between them, computed per art pixel, so the glow is made of whole art pixels like everything else.
- **The flicker is stepped too:** the campfire's radius changes 8 times a second.
- **A light mask keeps the glow off far layers.** Flame lets a post-process draw its subtree more than once, so the scene is drawn a second time at 180 px wide with the sky and hills left out; the shader lights a pixel only where that second image has something in it. Without the mask the campfire visibly lit the hills behind it. With it, the glow lands on the ground, the trees, the cabin, the character and the rain.

| Check | Result |
| --- | --- |
| Campfire glow and window light at night | Work. |
| Glow limited to near layers | Works with the mask; fails without it (hills lit). |
| Light follows the camera pan | Works; positions are passed in whole art pixels. |
| Cost on the emulator | 21 fps with the mask, 23 fps with lights but no mask, single readings on a noisy emulator. Not a fair measure. |
| Cost on the Pixel 7a | **Not measured.** The build is installed; it needs the phone unlocked with the spike open (60 fps without lights is the figure to compare with). |

Limits found:

- **The mask is all-or-nothing per layer.** A light cannot be partly hidden behind a tree trunk, and nothing casts a shadow. Per-object occlusion would need a different approach.
- **The number of lights is fixed in the shader** (two here). More lights mean more uniforms or a small light texture.
- **A light only reveals the art's daytime colors, warmed.** The green ground near the fire looks yellow-green. A hand-picked "lit" palette per layer would look better and is an art-direction question.
- The scene is now drawn twice per frame at low resolution. The mask could be redrawn only when the camera or layers move.
- **First launch after install showed a black screen for 15 to 20 seconds on the emulator** before the first frame, in every variant. Later launches were not timed. Worth checking on the phone.

## Second pass after the art references (2026-11-11)

Question: the references (`docs/references/notes.md`) ask for chunkier pixels, a bigger character, glows in clean flat bands, night and dusk as full re-colourings, and mirror reflections on water. Can the spike do all of that, and what does it cost?

**Answer: yes, and it got simpler.** The scene is now drawn once per frame instead of twice. Checked on the emulator and, for speed, on the Pixel 7a; release build. The rain, the light mask pass and the dithered glow of the first pass are gone from the code (they are in git history).

What changed:

- **View 120 art pixels wide** (was 180). On a 1080×2400 screen that is 9 screen pixels per art pixel and a 120×266 view. The camera is anchored to the bottom, so a taller screen shows more sky.
- **Character 30 art pixels tall,** about 11 % of the screen height (was 7.5 %), with a large sitting dog next to it for scale. Placeholder shapes, our own.
- **The art stores palette indices, not colours** (`tools/make_art.py`). Each pixel's red value is an index; the shader looks it up in `palette.png`, which has one row per time of day (night, dawn, day, dusk) and one row of firelit colours. Between times the shader mixes two rows. So night is not day darkened: each of the 36 colours has its own night colour, and the window, the fire, the moon and the stars stay bright. Stars are a palette entry that equals the sky colour by day.
- **Glow in three flat bands, no dither.** Inside a band the pixel moves toward its colour in the firelit row.
- **The light mask is the green channel of the art** (set where firelight may reach), so the second drawing of the scene is no longer needed.
- **Water is a mirror made in the shader:** below the waterline it reads the scene upside down, shifts whole rows sideways by a pixel or two on a slow beat, tints toward a water colour per time of day, and adds sparse bright streaks. The firelight and the window are reflected too, with no extra drawing.
- **Tap steps through** cycle, night, dawn, day, dusk, to hold a time for looking at it.

| Check | Result |
| --- | --- |
| Four times of day from one set of art | Works. Dusk is pink-purple, night near-monochrome blue with bright accents. |
| Flat-band glow, limited to near layers | Works. |
| Reflection, including lights | Works. |
| Whole-pixel scaling at 120 wide | Works on 1080×2400. Other screen sizes not rechecked. |
| Cost on the emulator | 15 to 18 fps, about the same as the first pass (21). Not a fair measure. |
| Cost on the Pixel 7a | **60 fps, worst frame 17 ms** (read off the screen by the project owner, 2026-11-11). The phone's full refresh rate, the same as before any lights were added. |

Limits found:

- **Indexed art cannot blend.** Every pixel must be one palette entry at full opacity, so soft fog, translucent rain and smooth text cannot be drawn into the scene. They need a second, ordinary layer drawn after the shader (the debug text already moved outside the game for this reason). Fog bands like the references' are the first thing to test next.
- **The references use many colours, not a small palette.** 36 entries were enough for placeholder shapes; painted scenes may need a few hundred. The lookup itself does not care (the palette image can be wider), but each entry needs a colour per time of day. Here most were generated from three-colour ramps and about 30 picked by hand; that split is an art-pipeline decision.
- **The sun and moon are painted into the sky** and do not move. They should be their own sprites placed from the injected time and location.
- **The reflection mirrors the screen,** so it can only show what is in view above the waterline, and the bank's front face is mirrored as well. Good enough at this size.
- The tap handler uses a Flame mixin that is marked as deprecated.

## Problems hit

1. **The scene rendered upside down.** A vertical flip that Flutter's shader documentation suggests for the OpenGL backend was wrong for an image produced by Flame's post-process step. Removing it fixed both the emulator (OpenGL) and the phone (Vulkan).
2. The first build downloaded a second Android platform and an NDK on its own (several minutes, about 2 GB).
3. The build warns that the `health` plugin applies the Kotlin Gradle plugin in a way future Flutter versions will reject. The plugin will need an update before a Flutter upgrade.
4. The debug text uses the default smooth font, not a pixel font. A bitmap font would need its own setup.
5. **Flame has no built-in integer scaling, and its fixed-resolution viewport stretches.** On any screen whose width or height is not a whole multiple of the scale, it stretched the picture by a fraction and some art pixels came out wider or taller than others. The fix (`PixelFit` in `lib/main.dart`, about 40 lines) puts the game in a box that is an exact whole multiple of the art size, centred on a physical pixel, leaving a border of at most a few pixels. Checked by measuring screenshots, not by eye.

## Rain and fog on top of the indexed scene (2026-11-11)

Question from the second pass: the indexed art cannot blend, so can weather be drawn as an ordinary translucent layer after the shader?

**Yes.** After the shader has drawn the scene, the same post-process step scales the canvas to art pixels and draws plain translucent rectangles on top (`_weather` in `lib/main.dart`). No second render pass and no extra image.

| Part | How | Result on the emulator |
| --- | --- | --- |
| Rain | 70 slanted streaks, 5 art pixels tall, 38% opaque, falling 150 to 220 art pixels a second | Fine streaks over sky, land and water, on the pixel grid |
| Fog | A thin veil over everything, a thicker one near the water, 9 slow wisps that stack where they overlap | Trees and hills fade back; the character and cabin stay readable |
| Muted colours | One shader input (`uWet`) pulls every scene colour toward a cool grey before the lights are added | Day, dusk and night all read as overcast; firelight stays warm |
| Weather colour | Rain and fog are ordinary colours, so each has one colour per time of day, mixed like the palette rows | Blue fog at night, pink at dawn |
| Fade | Weather fades in and out over about a second | Works |
| Window light | Radius 20 to 9, strength 0.67 to 0.34: a flat lit shape with one thin ring, as in the references | Works |

Tap now steps through: cycle, night, dawn, day, dusk, day rain, dusk rain, night rain, dawn fog, night fog. `--dart-define=HOLD=5` starts on one of them.

**Limits found**

- The sun and moon are painted into the sky art, so they still shine through the rain. Overcast needs the sun as its own piece, or cloudy sky rows.
- The muting is one formula. The references pull each colour down by hand; real art would use wet palette rows (one more row per time of day).
- Fog is drawn over the lights, so it dulls the campfire glow. Drawing lights after fog would need the glow moved out of the shader or the fog moved into it.
- Fog wisps are stacked rectangles and look like bands. Drawn fog sprites would use the same layer.
- The campfire's own flame colours are muted with the scene.
- Rain does not splash or change the water.

**Cost on the Pixel 7a:** not yet measured for rain and fog; the build is installed.

**Bug fixed on the way:** the `Stack` holding the debug text needed an explicit alignment; without one the first frame threw on a fresh start and the screen stayed blank.
