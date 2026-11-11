# hc-bridge (Phase 0 spike, throwaway)

Tests the decision in `docs/decisions/2026-11-11-health-bridge.md`: our own Health Connect bridge inside a Flutter app, with no health plugin. The question is whether a Kotlin background worker can read Health Connect while Flutter is not running, and whether the Flutter screen can use the same Kotlin code and see what the worker stored.

- `android/app/src/main/kotlin/.../HealthReader.kt` — the only code that reads Health Connect. Counts the steps, sleep and HRV records of the last 24 hours and appends one line per read to `reads.jsonl` in app-private storage.
- `.../ReadWorker.kt` — WorkManager job, every 15 minutes, calls `HealthReader`.
- `.../MainActivity.kt` — hosts Flutter and answers one platform channel (`wearablelife/health`): `status`, `requestPermissions`, `readNow`, `history`, `compareSteps`.
- `lib/main.dart` — one screen: permission state, "Grant", "Read now", "Compare steps", and the list of stored reads.

**What is stored:** the time of each read, who triggered it, whether Flutter was running, how old the process was, and record counts. No health values are stored, shown or logged. "Compare steps" stores nothing and shows only ratios between step totals, never a step count.

**Permissions:** `READ_STEPS`, `READ_SLEEP`, `READ_HEART_RATE_VARIABILITY`, `READ_HEALTH_DATA_IN_BACKGROUND`. No `INTERNET` permission in the release build. WorkManager adds `WAKE_LOCK`, `ACCESS_NETWORK_STATE`, `RECEIVE_BOOT_COMPLETED` and `FOREGROUND_SERVICE` on its own, as it did in the logger.

**Dependencies:** `androidx.health.connect:connect-client:1.1.0` and `androidx.work:work-runtime-ktx:2.12.0`, the same versions as `spikes/hc-logger`. No Dart packages beyond Flutter itself.

## Build

```sh
flutter build apk --debug --target-platform android-arm64     # debug, so reads.jsonl can be read with run-as
adb install -r build/app/outputs/flutter-apk/app-debug.apk
adb shell am start -n dev.wearablelife.hc_bridge/.MainActivity
adb shell run-as dev.wearablelife.hc_bridge cat files/reads.jsonl
```

On a real phone, install the **release** build (`flutter build apk --release --target-platform android-arm64`): Flutter's debug build adds the `INTERNET` permission. A release build cannot be read with `run-as`, so the screen shows a summary instead: number of reads, how many were in the background and without Flutter, errors, and the longest gap between reads.

Installed on the Pixel 7a on 2026-11-11 with default battery settings (not "Unrestricted"), to see what an ordinary install gets. Result to be read at the mid-collection check.

## Results (2026-11-10 and 11, emulator only, synthetic records)

| Check | Result |
| --- | --- |
| Flutter screen calls our Kotlin over a platform channel | Works. Status, read and history all return. |
| Permission state through the bridge | Works: "4 of 4". Permissions were granted with `adb`; the "Grant" button was later used on the Pixel 7a and Health Connect's own permission screen granted all four. |
| Read triggered from the screen | Works, 628 ms. |
| Background read while the app is open | Works, 270 ms. The worker and the screen share one process and one lock. |
| **Background read with the app process killed** | **Works.** 15 min 36 s after the previous run, Android started a new process (1 second old at the time of the read), the worker read Health Connect in 139 ms, and no Flutter engine was started. |
| **Background read after a reboot, app never opened** | **Works.** The emulator was cold-booted; 3 minutes later, and 15 min 37 s after the previous run, the worker read Health Connect in 389 ms. No Flutter engine, no activity; the process was 178 seconds old, so it was started at boot, most likely by WorkManager's own boot receiver. |
| Flutter screen sees what the worker stored | Works, through `history`. |
| Release build | 16.7 MB APK, no `INTERNET` permission. |

### The stored read log

All four reads on the emulator (UTC; counts are of synthetic records):

| Time | Trigger | Flutter running | Process age | Duration | Gap since previous |
| --- | --- | --- | --- | --- | --- |
| 10 Nov 23:41:08 | background | yes | 9 s | 270 ms | – |
| 10 Nov 23:41:28 | screen | yes | 28 s | 628 ms | 20 s |
| 10 Nov 23:57:04 | background | **no** | 1 s | 139 ms | 15 min 36 s |
| 11 Nov 00:12:41 | background | **no** | 178 s | 389 ms | 15 min 37 s (emulator was shut down and cold-booted in between) |

No read failed. Every read returned the same counts.

## Step totals: Health Connect's own total against each source (2026-11-11)

The question from the data findings: should scoring take one step source per day, or Health Connect's own de-duplicated total? "Compare steps" asks Health Connect, for each of the last 7 local days, for its total over all sources and for each source's own total, and reads the raw records. It shows:

- `sum/total`: all sources' own totals added up, divided by Health Connect's total. Above 1 means Health Connect removed overlap.
- `largest/total`: the biggest single source divided by the total.
- per source: `share` (its own total divided by the total), number of records, and `raw/own` (its records simply added up, divided by Health Connect's total for that source).

**Emulator result,** with two copies of the seeder writing 10-minute step records that overlap by half:

| Finding | Evidence |
| --- | --- |
| **The total is a priority merge, not a sum and not the largest source.** Where two sources overlap in time, one source's steps count and the other's are dropped for the overlapping part. | `sum/total` 1.83 and 1.09 on the two days. On one day the second source alone was 1.27 times the total: the total was *lower* than a single source. |
| **A source that is not on Health Connect's own list of sources counts as zero,** although its records can be read. | The second seeder was first given permission with `adb`: its records were returned, but its total and its part of the overall total were 0. After allowing it on Health Connect's own permission screen, it counted. |
| **A record that crosses midnight is split between the two days by the total,** while the raw record is returned whole for both days. | `raw/own` between 0.64 and 1.09 on the days with a record across midnight, for a source with no overlap inside itself. |

So Health Connect's total depends on a priority order the player controls in Health Connect's settings. Whether the app can read that order was not checked, and which source wins (here the first one allowed) was not varied.

**Real phone result** (Pixel 7a, 2026-11-11, read off the screen; ratios only). Two sources wrote steps in the last 7 days: the Whoop reader (`app.pulse`) and the phone's own counter.

| Day | Sources' totals added / Health Connect total | Largest source / total | Whoop reader share | Phone share |
| --- | --- | --- | --- | --- |
| 10 Nov | 1.13 | 0.96 | 0.96 | 0.18 |
| 9 Nov | 1.49 | 0.88 | 0.88 | 0.60 |
| 8 Nov | 1.60 | 0.84 | 0.77 | 0.84 |
| 7 Nov | 1.10 | 0.88 | 0.88 | 0.22 |
| 6 Nov | 1.57 | 0.91 | 0.91 | 0.66 |
| 5 Nov | 1.90 | 0.96 | 0.96 | 0.94 |

(11 Nov had only the phone, minutes after midnight: total equals the phone.)

- **Adding sources would overcount by 10 to 90 percent.** This confirms finding 5 of the data findings with Health Connect's own figures.
- **Health Connect's total was 4 to 19 percent higher than the best single source on every day.** It takes one source where both have data and fills the other's gaps: steps taken with the phone but without the strap, and the reverse.
- **The best single source changes from day to day** (the phone on 8 November, the strap on the others), so "one source per day" would need a rule for choosing, and would still miss the gap steps.
- Each source's records simply added up equal Health Connect's total for that source on every day (`raw/own` 1): no overlap inside a source and no record across midnight in this week.
- The total was never lower than a single source here. That only happened on the emulator, where the two sources disagreed strongly about the same minutes.

**Reading:** Health Connect's total is the better daily step figure for this phone. Its weak points are the ones seen on the emulator: it follows a source order the player can change, and a source missing from that order counts as zero.

## Problems hit

1. **A background run cannot be forced for testing.** `cmd jobscheduler run -f` starts the process, but WorkManager declines to run periodic work before its 15 minutes are up. Tests of the worker need either a real wait or a one-off work request for test builds.
2. **`FlutterActivity` cannot launch the Health Connect permission screen** the modern way; the host activity must be `FlutterFragmentActivity`.
3. A release build cannot be made readable with `run-as`: Flutter treats a debuggable Android build type as a debug build.
4. Killing the process with `am kill` makes WorkManager believe the app was force-stopped and reschedule its job. The job still ran on time.

## Not tested

- A real phone, overnight, with battery saving and Doze. The emulator says nothing about that.
- A swipe-away from recents. A reboot of a real phone (the emulator reboot worked).
- The worker and the screen reading at the same moment (covered by a lock, not exercised).
- Passing real record contents over the channel; only counts and ratios cross it here.
- What happens to the step total when the player reorders sources in Health Connect, and whether the app can read that order.
- The step comparison with an official wearable app as a source.
