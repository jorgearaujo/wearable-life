# Framework comparison (desk research)

- **Date:** 2026-11-10
- **Question:** Which one or two candidate stacks are worth a hands-on spike, judged against the spec's framework criteria?
- **Answer:** Spike **Godot 4.7** and **Flutter + Flame**. React Native + Skia is the runner-up. Unity, Defold and native-per-platform drop out.
- **Evidence:** web research on 2026-11-10 against official docs, release notes and plugin repositories. The research sections were not built or measured; the spike measurements near the end were. Items marked *unverified* could not be confirmed from a primary source and are the things the spikes must test.

## Summary matrix

Verdicts: Strong / Adequate / Weak. No candidate has an outright blocker.

| Criterion | Godot 4.7 | Flutter + Flame | React Native + Skia | Native (KMP + Compose canvas) | Unity 6.3 LTS | Defold 1.14 |
| --- | --- | --- | --- | --- | --- | --- |
| Health Connect | Weak plugin, easy Kotlin bridge | Strong | Adequate | Strong | Weak | Weak |
| HealthKit | Weak (bridge is the risk) | Adequate | Strong | Strong | Adequate | Weak |
| 2D pixel-art rendering | Strong | Adequate | Strong shaders, engine hand-built | Adequate, engine hand-built | Strong | Adequate |
| Performance and battery | Adequate, unmeasured | Adequate, unmeasured | Adequate, unmeasured | Adequate, unmeasured | Adequate, unmeasured | Strong API, unmeasured |
| Phone integration | Adequate | Adequate | Adequate | Strong | Adequate | Adequate |
| Developer experience | Strong | Strong | Strong | Adequate | Adequate | Adequate |
| Shipping | Adequate | Strong | Adequate | Adequate | Adequate | Strong |

## What the research changed

1. **Every stack needs our own Kotlin code for background reads.** Google's pattern for reading Health Connect while the app is closed is a WorkManager worker, which runs without any engine. No plugin in any stack provides this. The `spikes/hc-logger` worker is therefore reusable whichever stack wins, and "Health Connect access" separates the candidates less than expected. What matters is how easily a Kotlin library drops into the stack.
2. **No stack has measured battery data** for a mostly still 2D scene. This can only be answered on the phone.
3. **iOS has no public API for the next alarm** (*unverified*, reported by two of three research passes). The spec's "counted back from the next phone alarm" is likely Android-only; iOS would fall back to the usual wake time.
4. **On-device step counts changed attribution in June 2026:** they are written under a device-specific package name instead of `android`. Per-source baselines must not hard-code the origin.
5. **Google Play requires a health data declaration** for apps that request Health Connect types. Details not yet researched.

## Per candidate

### Godot 4.7.2 — spike

- **Health Connect:** two community plugins exist; one covers only basic records (no resting heart rate, HRV, breathing rate, SpO2, skin temperature, change tokens or background reads) and the other no longer uses Health Connect. A custom Android plugin is a Kotlin library with annotated methods, so the logger's code carries over. It forces the Gradle build path.
- **HealthKit:** existing plugins cover steps only. A custom bridge is either an Objective-C library (the official doc page is flagged as not updated for 4.7) or Swift through SwiftGodot (pre-1.0, self-described experimental). **This is Godot's biggest risk.**
- **Rendering:** integer scaling for pixel art is built in (since 4.2), plus canvas shaders, full-screen post-processing, 2D lights and particles. The Compatibility renderer is the documented choice for 2D on low-end phones.
- **Battery:** `low_processor_mode` and `Engine.max_fps` exist; whether low-processor mode works on exported mobile builds is *unverified*.
- **Developer experience:** text scene and resource files, headless command-line import, export and tests (GUT, gdUnit4). Tests run inside the Godot binary, not outside the engine. Aseprite import through a well-maintained add-on.
- **Shipping:** MIT, no fees. Android template targets API 36 with 16 KB page support. App size roughly 19–36 MB by forum reports.

### Flutter 3.47 + Flame 1.38 — spike

- **Health Connect:** two maintained plugins. `health` 13.3 covers the needed types and permissions but exposes no last-modified time and has 202 open issues. `health_connector` 3.14 has typed records, a sync token and full metadata, but is a young single-maintainer package with three breaking major versions.
- **HealthKit:** both plugins read the needed types. Background delivery needs a small Swift addition.
- **Rendering:** fixed-resolution viewport letterboxes but has no integer scaling built in; "ghost lines" between sprites at non-integer scales are a documented problem with documented mitigations. A post-processing API on fragment shaders suits palette and color-grade passes. No built-in 2D lighting found (*unverified*). **This is Flame's biggest risk.**
- **Battery:** Flutter has no built-in frame-rate cap; Flame's options are *unverified*.
- **Developer experience:** everything is text and code. Scoring can be a pure Dart package with fast `dart test` runs outside any engine. Sub-second hot reload on device, including shaders. No visual scene editor. Flame 2.0 is in prerelease.
- **Shipping:** BSD and MIT, no fees. About 12–14 MB per-architecture APK by third-party figures.

### React Native (Expo SDK 58) + Skia — runner-up

- **Health:** `react-native-health-connect` 4.1 covers the needed records, change tokens and permissions (single maintainer, quiet since August 2026). `@kingstinct/react-native-healthkit` 16.2 is the best HealthKit wrapper found in any stack, with background delivery and anchored queries.
- **Rendering:** one shader language on both platforms and nearest-neighbour sprite atlases, but there is no game engine: camera, scene graph, animation states and particles are all hand-built.
- **Why not spiked first:** the Skia package was renamed about six weeks ago and its v3 switches rendering backend (Vulkan-only on Android, minimum Android 8). A profile on a low-end 120 Hz phone found heavy frame drops in exactly the always-animating pattern this game uses. Flame offers the same code-first workflow plus ready game components.

### Native per platform (Kotlin Multiplatform core + Compose Multiplatform canvas) — dropped

- Best possible access to both health APIs and all phone features, with no wrappers.
- Dropped because the renderer is built from scratch on a UI toolkit, shaders are written twice (AGSL needs Android 13, SkSL on iOS), and hot reload is desktop-only, which makes tuning pixel art on a phone slow. Separate renderers per platform would double the visual work. KorGE and libGDX both have weak iOS stories.

### Unity 6.3 LTS — dropped

- Excellent 2D toolset: pixel-perfect camera, 2D lights, shader graph, first-party Aseprite importer.
- Dropped because Health Connect has no open-source plugin (only closed-source paid assets that do not document the types we need, and are hard to audit against "health data never leaves the device"), scenes and prefabs are editor-authored files that a coding agent edits less safely, command-line use on a Personal licence is awkward, and the baseline app is the largest (about 31–37 MB). Free up to $200,000 revenue.

### Defold 1.14 — dropped

- Smallest builds (about 2–4 MB empty), a real engine-throttle API, free licence.
- Dropped because native extensions accept only Java and Objective-C/C++, not Kotlin or Swift. The Health Connect client is a Kotlin coroutine API, so the bridge becomes Lua → C++ → JNI → Java with no existing example. Integer pixel scaling is not built in, and 2026 brought several breaking engine changes.

## What the two spikes must answer

| Open risk | Godot | Flutter + Flame |
| --- | --- | --- |
| Pixel-perfect layered scene with palette-swap shader and rain, on the real phone | Expected easy; confirm | **Main risk:** ghost lines, integer scaling, lighting by hand |
| Battery and frame time over 15 minutes | Does low-processor mode work on Android? | Can the frame rate be capped at all? |
| Step count through a native bridge | Custom Kotlin plugin, Gradle build | Existing plugin; check metadata exposed |
| Background worker alongside the engine | Kotlin worker inside the plugin library | Kotlin worker in the Android host project |
| Unit tests for pure logic | Headless, inside the engine | Plain `dart test` |
| Release build size | Measure | Measure |
| iOS health bridge | **Main risk; not testable in an Android-only Phase 0** | Plugins exist |

## Spike measurements (2026-11-10)

Both spikes build the same scene from the same placeholder art. Measured on a Pixel 7a (Android 17) unless noted. Details and build steps are in `spikes/fw-godot/README.md` and `spikes/fw-flame/README.md`.

| Check | Godot 4.7.2 | Flutter 3.47.9 + Flame 1.38.2 |
| --- | --- | --- |
| Frame rate, uncapped | 60 fps, worst frame 16 ms | 60 fps, worst frame 17 ms |
| Battery, screen on, uncapped | 88 mAh in 17 min 28 s, about 300 mA | 82 mAh in 16 min 20 s, about 300 mA |
| Memory | about 172 MB (debug build) | about 195 MB (release build) |
| Release APK, arm64 | 82 MB file, about 28 MB compressed | 16.0 MB file, about 7.7 MB compressed |
| Graphics backend | OpenGL ES 3.2 | Vulkan (Impeller) |
| Integer scaling, parallax, rain | Built in; worked first try | Hand-written, about 80 lines plus a rain component |
| Exact square pixels on other screen sizes (emulator, 720 to 1344 px wide, measured from screenshots) | Exact on all 6 sizes with no extra work | Uneven pixels on 3 of 6 sizes at first; exact on all 7 after a 40-line fix |
| Day → night shader | Worked first try | Worked after removing a wrong vertical flip |
| Step count from Health Connect | Own Kotlin plugin (about 60 lines) plus export hook (about 50 lines) | Existing `health` plugin, no Kotlin |
| Pure-logic unit test | Headless inside the Godot binary, about 0.3 s | Plain `dart test`, about 5 s including start-up |
| Fragile build steps | Template's Android Gradle plugin must be patched after each install; manifest entries added by an export hook | `health` plugin triggers a Kotlin Gradle plugin warning that a future Flutter will reject |

What this settles and what it does not:

- **Performance and battery do not separate the two.** Both hold 60 fps, and the battery draw is the same within the precision of the measurement, so the screen dominates. The two battery runs were one after the other in the same light with adaptive brightness on; each is a single run.
- **Flame's main risk is real but was cheap to fix.** Its fixed-resolution viewport stretches by a fraction on screens the scale does not divide, which made 1–3% of art pixels uneven on three of six screen sizes. Sizing the game to an exact whole multiple of the art, centred on a physical pixel, removed it on every size tested (added 2026-11-11). Godot needed nothing. The test used still frames from the emulator; shimmer during fast movement was not measured.
- **Not tested:** a capped frame rate (30 or 15 fps) on battery, the background worker alongside each engine, tablets and landscape, 2D lighting beyond a color grade, and anything on iOS.

## Key sources

- Health Connect: https://developer.android.com/jetpack/androidx/releases/health-connect , https://developer.android.com/health-and-fitness/guides/health-connect/develop/read-data
- Store rules: https://developer.android.com/google/play/requirements/target-sdk , https://developer.android.com/guide/practices/page-sizes , https://developer.apple.com/news/upcoming-requirements/
- Godot: https://docs.godotengine.org/en/stable/tutorials/platform/android/android_plugin.html , https://docs.godotengine.org/en/stable/tutorials/platform/ios/ios_plugin.html , https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html , https://github.com/MrSfantaus/HealthConnect-Godot-Android-Plugin , https://github.com/SomniGameStudios/godot-healthkit-plugin , https://github.com/migueldeicaza/SwiftGodot , https://github.com/bitwes/Gut
- Flutter + Flame: https://pub.dev/packages/health , https://pub.dev/packages/health_connector , https://pub.dev/packages/flame , https://docs.flame-engine.org/latest/flame/rendering/post_processing.html , https://docs.flutter.dev/ui/design/graphics/fragment-shaders , https://github.com/flutter/flutter/issues/159797
- React Native: https://github.com/matinzd/react-native-health-connect , https://github.com/kingstinct/react-native-healthkit , https://github.com/wcandillon/react-native-skia , https://margelo.com/blog/profiling-skia-reanimated-low-end-android
- Native: https://kotlinlang.org/docs/multiplatform/compose-hot-reload.html , https://kotlinlang.org/docs/native-swift-export.html
- Unity: https://unity.com/releases/unity-6/support , https://unity.com/products/pricing-updates , https://docs.unity3d.com/Manual/AndroidJavaSourcePlugins.html , https://assetstore.unity.com/packages/package/365582
- Defold: https://defold.com/manuals/extensions/ , https://forum.defold.com/t/android-native-extensions-can-not-use-kotlin-file/81001 , https://defold.com/2026/01/12/Defold-1-12-0/ , https://defold.com/license/
