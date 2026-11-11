# fw-godot (Phase 0 spike, throwaway)

The shared framework test from the Phase 0 plan, built in Godot 4.7.2 with the Compatibility renderer.

- `main.tscn`, `main.gd` — portrait scene, 180 px wide base, integer scaling; sky plus three layers with parallax; a panning camera (drag, or it drifts on its own); an animated character; rain particles; a debug label.
- `grade.gdshader` — one full-screen shader that grades the same art from day through dusk to night.
- `plugin/` — Kotlin Android plugin (`HcBridge`) that reads today's step count from Health Connect and sends it to GDScript as a signal. It logs nothing.
- `addons/hc_bridge/` — the export hook that adds the plugin, its dependency and the Health Connect manifest entries.
- `tools/make_art.py` — draws the placeholder art.

Double-tap cycles the frame-rate cap: uncapped, 30, 15.

## Build

```sh
(cd plugin && JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home" ./gradlew copyAar)
godot --headless --path . --install-android-build-template --export-debug Android build/fw-godot.apk   # first time: fails, see below
sed -i '' "s/androidGradlePlugin: '8.6.1'/androidGradlePlugin: '8.9.1'/" android/build/config.gradle
godot --headless --path . --export-debug Android build/fw-godot.apk
adb install -r build/fw-godot.apk
adb shell pm grant dev.wearablelife.fwgodot android.permission.health.READ_STEPS   # the spike has no permission screen
```

Desktop check: `godot --path . -- --shot=<folder>` saves noon, dusk and night frames and quits.

## Results so far (2026-11-10)

| Check | Result |
| --- | --- |
| Scene, parallax, integer scaling | Worked first try from hand-written text files. 1080×2400 screen gives a 180×400 view at exactly 6×. |
| Day → night shader | Worked first try on desktop and emulator. |
| Rain particles | Worked first try. |
| Step count through a Kotlin bridge | Works on the emulator. About 60 lines of Kotlin plus 50 lines of export hook. |
| Debug build on a Pixel 7a | Runs on OpenGL ES 3.2 at a steady 60 fps, worst frame 16 ms, 180×400 view at 6×, about 172 MB memory. |
| Release APK, arm64 only | 82 MB as a file (the engine library is stored uncompressed), about 28 MB when compressed, which approximates the download. Not yet trimmed. |
| Battery on the phone, screen on, uncapped 60 fps | 88 mAh in 17 min 28 s (866 → 778 mAh, from the phone's own battery history), an average of about 300 mA. Battery level 25% → 23%, adaptive brightness on. |
| Headless unit tests | `godot --headless --path . -s tests/run.gd` runs a pure-logic test in about 0.3 s with a proper exit code. It still needs the Godot binary; no test add-on was used. |

## Problems hit

1. **Godot's Android build template uses Android Gradle plugin 8.6.1; the Health Connect client 1.1.0 needs 8.9.1 or newer.** The template is copied into `android/build/` and has to be patched after every install (one line, shown above).
2. **Health Connect removes health permissions from an app that does not declare a privacy-rationale screen.** The export hook has to add an intent filter and an activity alias to the manifest; without them the grant is silently revoked.
3. The plugin must be compiled against the same Android API level as the template (36), or the export fails.
4. Export fails until ETC2/ASTC texture import is switched on in the project settings.
5. Coroutines are not on the compile path through the Health Connect client alone; they need their own compile-only line.

None of these took more than a few minutes, but 1 and 2 are the kind of thing that would break again on an engine upgrade.
