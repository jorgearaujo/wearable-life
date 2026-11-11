# Health data access: our own bridge

- **Date:** 2026-11-11
- **Question:** How does the Flutter app read Health Connect, and later HealthKit?
- **Decision:** **Our own native bridge, with no third-party health plugin.** Decided by the project owner as the most robust option.
- **Evidence:** `docs/findings/2026-11-11-health-plugin-comparison.md`, `docs/findings/2026-11-11-health-connect-data.md`, `spikes/hc-logger/`.

## Options considered

The `health` plugin, the `health_connector` plugin, and our own bridge. Details are in the plugin comparison.

## Why our own bridge

1. **No third-party code touches health data.** `health` writes health values to the phone's log, which rule 6 forbids. With our own code, what is logged and stored is fully in our hands.
2. **The background worker has to be our own Kotlin in any case.** Neither plugin reads on a schedule. A plugin would mean two code paths reading Health Connect; the bridge gives one.
3. **It exposes exactly the fields scoring needs:** source app, last-modified time, client record ID and version, zone offsets, and Health Connect's own totals. The logger already reads all of them.
4. **No dependence on a plugin's release schedule** for Flutter or Health Connect updates.

## What we give up

- **We write and maintain the Android side** (the logger is the starting point) **and a second bridge in Swift for HealthKit.** The Swift side cannot be tested in this phase.
- No community fixes for platform quirks; we find them ourselves.

## Known risks

1. **HealthKit is unbuilt and untested.** It is the larger unknown: different permission model, no "which permissions were granted" answer for reads, different background delivery.
2. **The Health Connect library versions with the newest features are alpha releases.** The logger runs on the stable 1.1.0, which covered every type in the collection.
3. **Running the worker inside a Flutter app works on the emulator** (`spikes/hc-bridge`): it read Health Connect with the app killed and without starting Flutter. A real phone overnight is still untested.

## Consequences

- The data layer interface from the architecture principles is implemented by Kotlin code on Android and Swift code on iOS, reached from Dart over a platform channel.
- The framework decision's point that health data comes "through existing plugins" no longer applies. The other reasons for Flutter + Flame stand.
- Open design question for `spikes/hc-bridge`: whether only the background worker reads Health Connect and the app reads the worker's local store, or both read.
