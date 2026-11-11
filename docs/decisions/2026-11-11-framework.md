# Framework: Flutter + Flame

- **Date:** 2026-11-11
- **Question:** Which framework or engine do we build the game in?
- **Decision:** **Flutter with the Flame game engine.** Decided by the project owner after the desk research and two hands-on spikes.
- **Evidence:** `docs/findings/2026-11-10-framework-comparison.md` (research matrix and spike measurements), `spikes/fw-flame/`, `spikes/fw-godot/`.

## Options considered

Godot 4.7, Flutter + Flame, React Native + Skia, native per platform (Kotlin Multiplatform), Unity 6.3 and Defold 1.14. Godot and Flutter + Flame were spiked; the others were dropped on paper for the reasons in the comparison.

## Why Flutter + Flame

Measured on a Pixel 7a with the same scene and art in both spikes:

| | Godot | Flutter + Flame |
| --- | --- | --- |
| Frame rate | 60 fps, worst frame 16 ms | 60 fps, worst frame 17 ms |
| Battery, screen on | about 300 mA | about 300 mA |
| Download size, approximate | 28 MB | 7.7 MB |

1. **Performance and battery are a tie,** so they do not decide it.
2. **Health data on both platforms through existing plugins.** The step count needed no Kotlin in Flutter. Godot needed its own Android plugin, and its HealthKit bridge on iOS is the largest untested risk of any candidate and could not be tested in an Android-only phase.
3. **Scoring can be a pure Dart package** tested with plain `dart test`, outside any engine. This matches the architecture principle that scoring is a pure, platform-independent module.
4. **Smaller app:** about a quarter of Godot's download size.
5. **Everything is text and code,** with hot reload on the device.

## What we give up

- **Rendering features are ours to build and keep correct.** Godot had integer scaling, parallax and particles built in and was pixel-exact on every screen size with no work. In Flame, parallax, integer scaling and rain were hand-written (about 80 lines plus a rain component).
- **No visual scene editor.** Scenes are composed in code.
- **No built-in frame-rate cap.**

## Known risks

1. **Pixel-exact scaling is code we own.** Flame's fixed-resolution viewport stretched the picture on three of six screen sizes. A 40-line fix made every size exact on the emulator. This should become an automated screenshot check in the real app. Tablets, landscape and shimmer during fast movement are untested.
2. **Flutter + Flame is a 2D stack.** This choice in practice settles the spec's open rendering question in favour of flat 2D layers; pixel art in a 3D setting would need a different engine.
3. **Lighting beyond a full-screen color grade (tested 2026-11-11 on the emulator; works).** Flame has no built-in 2D lights. A campfire glow and a lit window were added to the grade shader in about 60 lines, with a stepped pixel-art falloff and a mask that keeps the glow off the sky and hills (`spikes/fw-flame/README.md`). Still open: the cost on a real phone, and lights that are partly hidden by single objects or cast shadows, which this approach does not do. A second pass the same day replaced the grade with a palette lookup per time of day, flat-band glows and a mirrored water reflection, drawing the scene once; it works on the emulator, and its new limit is that indexed art cannot blend (fog, rain).
4. **Health plugin maturity (resolved: we write our own bridge, see `2026-11-11-health-bridge.md`; reason 2 above no longer applies).** `health` 13.3 exposes no last-modified time and triggers a build warning that a future Flutter version will turn into an error. `health_connector` is the alternative. Which one to use, or whether to write a thin bridge of our own, is decided after the data findings. Compared in `docs/findings/2026-11-11-health-plugin-comparison.md`; `health` also writes health values to the phone's log, which rule 6 forbids.
5. **Background reads need our own Kotlin worker** in the Android host project, in any stack. Running it alongside Flutter is untested; the logger's worker is the starting point.
6. **Battery at a capped frame rate** was not measured, and each battery figure is a single run.
7. **iOS is entirely untested.**
8. Flame 2.0 is in prerelease; expect a migration.

## Consequences

- The real app will be a Flutter project with Flame for the scene, a pure Dart scoring package, and Kotlin (later Swift) in the host projects for background health reads.
- `spikes/fw-godot/` and `spikes/fw-flame/` stay as throwaway references. The real app is not built on top of the spike.
- Phase 0 continues until the Health Connect data collection is written up.
