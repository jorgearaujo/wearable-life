# hc-logger (Phase 0 spike, throwaway)

A bare Android app that reads Health Connect and logs what arrives and when. It answers the spec's data discovery question: which data types each wearable writes, how late, and what the records look like.

It only reads. It has no `INTERNET` permission, so nothing can leave the phone except over USB.

## What it logs

Two files in the app's private storage:

- `observations.jsonl` — one line per record seen, updated or deleted, with the time the logger saw it (`seenAt`), the app that wrote it (`meta.origin`), when Health Connect last stored it (`meta.lastModified`) and the values (`data`).
- `runs.jsonl` — one line per poll: trigger (`open`, `manual`, `background`), granted permissions, available features, per-type counts and errors, and the phone's next alarm time.

The first poll for each type reads 90 days of history (`via: backfill`). After that it uses the Changes API (`via: change`), so only live records carry meaningful delays.

Polls happen when the app opens, when you tap **Read now**, and every 15 minutes in the background.

## Install on the phone

1. Enable developer options and USB debugging on the phone, connect it, accept the prompt.
2. From this folder:
   ```sh
   export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
   ./gradlew :app:installDebug
   ```
3. Open **HC Logger**, tap **Grant permissions**, allow everything, including "access past data" and "access data in the background".
4. In the phone's settings, set battery use for HC Logger to **Unrestricted**, or background polls will be throttled.
5. In your wearable's app, make sure syncing to Health Connect is turned on for every data type it offers.

Leave it installed for 1–2 weeks. Open it now and then; the table should show totals growing. Do not uninstall or clear its data, since that deletes the logs.

## Get the data

```sh
scripts/pull.sh                  # copies both files into data/raw/<timestamp>/ (git-ignored)
scripts/summarize.py             # per app and type: counts, rewrites, delays; no health values printed
scripts/anonymize.py data/raw/<timestamp> <name>   # writes fixtures/<name>/ for tests
```

`data/raw/` holds real health data and must never be committed. `anonymize.py` shifts all dates by a random number of whole weeks, replaces record IDs and drops device and phone details; the health values themselves are kept, since the tests need them.

## Emulator check

`seeder/` is a second tiny app that writes one synthetic record of every type. It exists only to test the logger on an emulator; never install it on a phone with real data.

```sh
./gradlew :app:installDebug :seeder:installDebug
# grant permissions with `adb shell pm grant <package> android.permission.health.<NAME>`, then:
adb shell am start -n dev.wearablelife.hcseeder/.SeedActivity --es action insert   # or update, delete
# two step sources for the bridge spike's comparison: build a second copy with -PseederId=dev.wearablelife.hcseeder2,
# then on each copy: --es action steps --el count 100 --el shift 0
```

## Known limits

- If a history read fails part-way (for example on a rate limit), the next poll starts that type's backfill again, so the log can contain duplicate backfill lines. `summarize.py` counts records by ID, so totals stay correct.
- Exercise routes and free-text titles and notes are not logged.
