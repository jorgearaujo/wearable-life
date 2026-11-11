# fw-flame (Phase 0 spike, throwaway)

The shared framework test from the Phase 0 plan, built in Flutter 3.47.9 with Flame 1.38.2. It uses the same placeholder art as `spikes/fw-godot`.

- `lib/main.dart` — portrait scene, 180 px wide, integer scaling worked out by hand from the screen width; sky plus three layers with parallax; a panning camera (drag, or it drifts on its own); an animated character; rain; a debug label; today's step count through the `health` plugin.
- `shaders/grade.frag` — one full-screen shader that grades the same art from day through dusk to night.
- `lib/daylight.dart`, `test/daylight_test.dart` — a pure-logic function and its test, with no engine involved.
- `android/` — host project. The manifest asks for `READ_STEPS` only and declares the Health Connect privacy-rationale screen. The release build has no `INTERNET` permission.

## Build

```sh
flutter build apk --release --target-platform android-arm64
adb install -r build/app/outputs/flutter-apk/app-release.apk
adb shell pm grant dev.wearablelife.fw_flame android.permission.health.READ_STEPS   # the spike has no permission screen
adb shell am start -n dev.wearablelife.fw_flame/.MainActivity
dart test        # pure-logic test, no device needed
```

## Results so far (2026-11-10)

| Check | Result |
| --- | --- |
| Scene, parallax, integer scaling | Works, but parallax and integer scaling are hand-written (about 80 lines). |
| Other screen sizes (emulator, 7 sizes from 720 to 1344 px wide) | First version drew uneven pixels on 3 of 6 sizes (1–3% of art pixels). After the fix in problem 5, every art pixel is an exact square on all 7. Godot was exact on all 6 it was run on with no extra work. |
| Day → night shader | Works after one fix (see problem 1). The scene is drawn to an image at 180 px wide every frame and the shader scales it up. |
| Rain | Works. Hand-written component; Flame's particle system was not needed for it. |
| Step count | Works on the emulator through the `health` plugin, with no Kotlin written. |
| Release build on the emulator | Runs at about 29 fps with a worst frame of 70 ms; Godot reached 43–46 fps on the same emulator. Emulator numbers are not a fair measure. |
| Release build on a Pixel 7a | Runs on Vulkan at a steady 60 fps, worst frame 17 ms, 180×400 view at 6×, scene the right way up. About 195 MB memory (Godot: about 172 MB). |
| Memory on the emulator | About 60 MB. |
| Release APK, arm64 only | 16.0 MB as a file, about 7.7 MB when compressed, which approximates the download. |
| Battery on the phone, screen on, uncapped 60 fps | 82 mAh in 16 min 20 s (872 → 790 mAh, from the phone's own battery history), an average of about 300 mA. Battery level 26% → 23%, adaptive brightness on. Same as Godot within the precision of the measurement. |
| Unit tests | `dart test` runs outside any engine. About 5 s including start-up. |
| Frame-rate cap | Not built. Flutter has no built-in cap. |

## Problems hit

1. **The scene rendered upside down.** A vertical flip that Flutter's shader documentation suggests for the OpenGL backend was wrong for an image produced by Flame's post-process step. Removing it fixed both the emulator (OpenGL) and the phone (Vulkan).
2. The first build downloaded a second Android platform and an NDK on its own (several minutes, about 2 GB).
3. The build warns that the `health` plugin applies the Kotlin Gradle plugin in a way future Flutter versions will reject. The plugin will need an update before a Flutter upgrade.
4. The debug text uses the default smooth font, not a pixel font. A bitmap font would need its own setup.
5. **Flame has no built-in integer scaling, and its fixed-resolution viewport stretches.** On any screen whose width or height is not a whole multiple of the scale, it stretched the picture by a fraction and some art pixels came out wider or taller than others. The fix (`PixelFit` in `lib/main.dart`, about 40 lines) puts the game in a box that is an exact whole multiple of the art size, centred on a physical pixel, leaving a border of at most a few pixels. Checked by measuring screenshots, not by eye.
