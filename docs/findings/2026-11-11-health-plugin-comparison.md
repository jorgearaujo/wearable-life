# Flutter health plugin: `health` vs `health_connector` vs our own bridge

- **Date:** 2026-11-11
- **Question:** How should the Flutter app read Health Connect (and later HealthKit)?
- **Answer:** The project owner chose **our own bridge** (option C); see `docs/decisions/2026-11-11-health-bridge.md`. The recommendation below was `health_connector`, with our own bridge as the fallback. `health` is ruled out as it stands because it writes health values to the phone's log (rule 6).
- **Evidence:** Source of `health` 13.3.2 and `health_connector` 3.14.0 (with its Android package 3.11.0), read on 2026-11-11. Neither was run for this comparison; `health` was run once for a step count in `spikes/fw-flame`. What the game needs comes from `docs/findings/2026-11-11-health-connect-data.md`.

## Comparison

| Need | `health` 13.3.2 | `health_connector` 3.14.0 |
| --- | --- | --- |
| All record types the spec uses | Yes | Yes |
| Source app of each record | Yes | Yes |
| Recording method (manual or automatic) | Yes | Yes |
| Last-modified time | **No** | Yes |
| Client record ID and version | No | Yes |
| Time-zone offset on each record | Little | Yes |
| "What changed since last time" | Yes (changes token) | Yes (sync token) |
| Health Connect's own totals (de-duplicated steps) | Steps only | Yes, general aggregates |
| Check which features the phone supports | Partly | Yes |
| Background and history permissions | Yes | Yes |
| Network or telemetry code | None found | None found |
| **Health values in the phone's log** | **Yes, always on** | No; logging is off by default and messages are operation names |
| HealthKit | Yes, same API | Yes, separate package behind the same API |
| Health Connect library version | 1.2.0-alpha02 | 1.2.0-alpha03 |
| Build | Triggers a warning that a future Flutter version turns into an error | Not built yet |

## Findings

1. **`health` breaks rule 6 as shipped.** Its Android code logs step totals (`HealthDataReader.kt` lines 512 and 558) and the full contents of a record read by ID (line 242) to the system log, in release builds, with no switch to turn it off. The system log is readable over USB and is included in bug reports. Using it would mean maintaining a patched copy.
2. **`health` cannot tell us when a record changed.** The data findings show sources rewrite records, and that scoring must tell a rewrite from new data. Without a last-modified time or record version, that has to be done by comparing contents.
3. **`health_connector` exposes what the logger exposed:** origin, last-modified time, client record ID and version, device, recording method, zone offsets, aggregates and a sync token. It maps almost one-to-one onto the fields the data findings rely on.
4. **Both depend on an alpha version of Google's Health Connect library.** There is no stable release with the features we need, so this does not separate them.
5. **Neither plugin does background reads on a schedule.** Both only answer calls from running Dart code. The Kotlin worker is ours in every option.
6. **`health_connector` is the less proven of the two:** a single maintainer, a younger package, four packages to keep in step. Its HealthKit side is unread and untested here.

## Options

| Option | For | Against |
| --- | --- | --- |
| A. `health` | Most used; already ran in the spike | Logs health values; no last-modified time; build warning. Needs a fork to be usable |
| B. `health_connector` | Covers every field we need; logging off by default; HealthKit behind the same API | Less proven; single maintainer; not yet run by us |
| C. Our own bridge | Exactly the fields we need; one Kotlin code path shared by the app and the background worker; no third-party code touching health data | We write and maintain it, and a second one in Swift for HealthKit, which cannot be tested in this phase |

## Recommendation

**Option B, behind our own data layer interface.** The architecture already asks for one interface over both platforms, so the plugin sits behind it and can be replaced by option C later without touching scoring. The background worker stays in Kotlin and writes to the same local store the app reads.

One design question follows from this and is not settled: whether the background worker and the app both read Health Connect (two code paths, Kotlin and plugin), or only the worker reads and the app reads the worker's store. The second is simpler to keep consistent and pushes towards option C on Android. This is what the next spike (worker alongside Flutter) should answer.

## Not checked

- `health_connector` has not been built or run by us. Adding it to a spike is a new dependency and needs the project owner's approval.
- HealthKit behaviour of either plugin.
- Whether `health_connector`'s sync token survives the token expiry Health Connect applies after 30 days.
