# fw-flame (Phase 0 spike, throwaway)

The shared framework test from the Phase 0 plan, built in Flutter 3.47.9 with Flame 1.38.2. It uses the same placeholder art as `spikes/fw-godot`.

- `lib/main.dart` — portrait scene, 180 px wide, integer scaling worked out by hand from the screen width; sky plus three layers with parallax; a panning camera (drag, or it drifts on its own); an animated character; rain; a debug label; a placeholder campfire. The step count through the `health` plugin was removed on 2026-11-11 (we write our own bridge, and the plugin writes health values to the phone's log); it is in the first commit.
- `shaders/grade.frag` — one full-screen shader that grades the same art from day through dusk to night, and adds two point lights (campfire, cabin window) when it is dark.
- `lib/daylight.dart`, `test/daylight_test.dart` — a pure-logic function and its test, with no engine involved.
- `android/` — host project. The release build asks for no permission at all: no health permission, no `INTERNET`.

## Build

```sh
flutter build apk --release --target-platform android-arm64
adb install -r build/app/outputs/flutter-apk/app-release.apk
adb shell am start -n dev.wearablelife.fw_flame/.MainActivity
dart test        # pure-logic test, no device needed
```

For screenshots: `--dart-define=FIXED_TIME=0` holds one time of day (thousandths; 0 = midnight, 500 = noon). `--dart-define=LIGHTS=off` or `LIGHTS=nomask` switches the lights off or lets them light every layer.

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

## Problems hit

1. **The scene rendered upside down.** A vertical flip that Flutter's shader documentation suggests for the OpenGL backend was wrong for an image produced by Flame's post-process step. Removing it fixed both the emulator (OpenGL) and the phone (Vulkan).
2. The first build downloaded a second Android platform and an NDK on its own (several minutes, about 2 GB).
3. The build warns that the `health` plugin applies the Kotlin Gradle plugin in a way future Flutter versions will reject. The plugin will need an update before a Flutter upgrade.
4. The debug text uses the default smooth font, not a pixel font. A bitmap font would need its own setup.
5. **Flame has no built-in integer scaling, and its fixed-resolution viewport stretches.** On any screen whose width or height is not a whole multiple of the scale, it stretched the picture by a fraction and some art pixels came out wider or taller than others. The fix (`PixelFit` in `lib/main.dart`, about 40 lines) puts the game in a box that is an exact whole multiple of the art size, centred on a physical pixel, leaving a border of at most a few pixels. Checked by measuring screenshots, not by eye.
