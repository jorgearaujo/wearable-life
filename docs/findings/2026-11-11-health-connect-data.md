# Health Connect data: what arrives (interim)

- **Date:** 2026-11-11. **Interim:** based on the 90-day history read on the first evening. Arrival delays and overnight background reads are added after the 1–2 week collection.
- **Question:** Which data types do real sources write to Health Connect, in what shape, and what does that mean for scoring?
- **Answer so far:** A wearable source supplies every input the spec uses, at the Full tier. The records differ between sources in ways scoring must handle: how often a value is written, where its timestamp sits, and how several sources overlap on the same day. History timestamps cannot be used to measure delays.
- **Evidence:** `spikes/hc-logger` on a Pixel 7a (Android 17), pulled 2026-11-11; 67,496 logged records. Analysed for structure and timing only. No health values are quoted here.

## Sources on the test phone

| Source | What it is | Data present | Live during the collection? |
| --- | --- | --- | --- |
| `com.fitbit.FitbitMobile` | Official Fitbit app, Fitbit Air | 12 days in August 2026, plus calories every day since | Only calories; the device is no longer worn |
| `app.pulse` | The project owner's own app reading a Whoop 5.0 strap | 10 days from 1 November 2026 | Yes |
| `com.android.healthconnect.phone.<device id>` | The phone's own step counter | Steps for all 91 days; distance and active calories for 41 | Yes |
| Withings app | Installed | Nothing written | No |

**Limits.** Fitbit is the only source that shows what an ordinary player's phone contains, and its data is historical, so the collection cannot measure arrival delays for any official wearable app. Live delays will describe the Whoop reader, whose timing is set by that app's own design, and the phone's step counter. Delays for official apps have to come from desk research or other testers. `app.pulse` shows what a Whoop strap can supply, not what the official Whoop app writes; that app needs a subscription and was not tested.

## What each source writes

| Type | Fitbit app | Whoop via own app | Phone |
| --- | --- | --- | --- |
| Steps | 1-minute records | 1-minute records | Short bursts, seconds to minutes long |
| Distance | 1-minute records | – | Same bursts as steps |
| Sleep session with stages | Yes, every session | Yes, every session | – |
| Heart rate | 1-minute records, a sample about every 3 s | 1-minute records, a sample every second | – |
| HRV (RMSSD) | About 85 values a night, spread through sleep | One value a night | – |
| Resting heart rate | One a night | One a night | – |
| Breathing rate | One a night | One a night | – |
| Blood oxygen | – | One a night, on 6 of 10 nights | – |
| Skin temperature | One record a night | One record a night, on 6 of 10 nights | – |
| Exercise sessions | Yes (1 in 12 days) | Yes (13 in 10 days) | – |
| Active calories | – | – | Yes |
| Total calories | 1 to 15-minute records, every day | – | – |
| Body temperature, mindfulness | – | – | – |

Both wearable sources reach the **Full** tier. This is not typical: by their own published lists, most official wearable apps write less (see `2026-11-11-wearable-apps-and-store-rules.md`). The phone alone gives the **Minimal** tier's activity half (steps) but no sleep.

## Findings that affect scoring

1. **HRV comes in two shapes.** Fitbit writes a value about every five minutes during sleep; the Whoop reader writes one value per night. Scoring must reduce HRV to one figure per night per source before comparing with the baseline, and must not compare one source's figure with another's.
2. **Nightly values are stamped at the moment sleep ends.** Resting heart rate, breathing rate, blood oxygen and skin temperature all carry exactly the sleep session's end time, in both sources. They can be matched to a night by that timestamp. Fitbit's HRV samples sit inside the session instead.
3. **Sleep stages are complete and clean.** Every session has stages; they cover the whole session with no gaps or overlaps, at 1-minute resolution, using four codes (awake, light, deep, REM). Awake time is inside the session, so time asleep is the session minus awake stages.
4. **One day can hold several sleep sessions.** Fitbit wrote up to three sessions ending on the same day. Scoring needs a rule for which is the main sleep and which are naps or a split night.
5. **Step counts from different sources must not be added.** Wearable and phone both write steps for the same minutes, and their daily totals differ widely in both directions, depending on which device was carried. Scoring needs one source per day, or Health Connect's own de-duplicated total. Which of the two is better is not yet tested.
6. **Skin temperature is a difference, not a temperature.** Each record holds one deviation value; the baseline field was empty in 14 of 15 records. It can only be used as "above or below usual", which fits the baseline principle.
7. **Heart rate is large.** About 34,000 samples a day from Fitbit and 85,000 from the Whoop reader. Ninety days of raw samples is tens of megabytes. Strain should be computed in bounded windows or from Health Connect's aggregates, and never by loading the full history at once.
8. **An app writing data does not mean a wearable is being worn.** The Fitbit app has written estimated total calories every day for ten weeks after the device was last worn. The data tier must be judged from recent sleep and heart data, not from the presence of a source.
9. **"Last modified" on history is not the arrival time.** Fitbit's August sleep sessions carry modification times 15 to 20 days after the night, and the Whoop reader's records up to six days after. Sources rewrite old records in bulk. Delays can only be measured on records seen live, which is what the collection is for.
10. **Updates often change nothing.** The Whoop reader rewrote last night's sleep and nightly values 17 to 47 minutes after first writing them, with identical contents. Scoring must be safe to re-run on the same night, and a rewrite of an old night must never lower the level (rule 1).
11. **Time-zone offsets are present on every record,** and the history spans a daylight-saving change (+02:00 to +01:00). Day boundaries can use the record's own offset.
12. **The same field arrives as a whole number or a decimal** (distance, HRV, breathing rate). Parsers must accept both.
13. **The phone's step source uses a device-specific package name,** confirming the attribution change found in the framework research. Recognise it by its prefix.

## Checked and working

- A 90-day history read succeeded with the history permission; the oldest records are from 12 August 2026.
- Background reads ran four times in the first hour, never more than 23 minutes apart. Overnight behaviour is not yet known.
- The phone's own steps are written within about a minute and were read by the logger about six minutes later.

## Still open

- **Arrival delays** for sleep and the nightly values after waking: needs the live collection.
- **Background reads overnight** and under battery saving.
- **Next alarm:** the logger read no alarm in any of its 10 polls, which is correct: none was set. Reading a set alarm on the real phone is still untested.
- **Official Whoop, Garmin, Oura, Samsung and Withings apps:** not observed. Desk research is in `2026-11-11-wearable-apps-and-store-rules.md`: what each app lists as written is known, with varying confidence; arrival delays are not published by any vendor and stay open.
- **Health Connect's aggregated step total** versus picking one source. On the emulator the total is a priority merge: overlapping time is taken from one source, so the total can be lower than a single source, and a source missing from Health Connect's source list counts as zero (`spikes/hc-bridge/README.md`). On the real phone, over six days with the Whoop reader and the phone as sources, the total was 4 to 19 percent above the best single source and adding the sources would overcount by 10 to 90 percent. Decided 2026-11-11: daily steps use Health Connect's total (in `docs/spec.md`). Still open: what a reordering of sources by the player does, and an official wearable app as a source.
- **HealthKit:** not tested in this phase.

## Proposed spec changes (not yet applied)

- Data, HRV fallback: add that HRV may be one value or many per night and is reduced to one per night per source.
- Data, Syncing: add that sources rewrite old records, so scoring must be repeatable and history timestamps are not arrival times.
- Data, tiers: add that the tier is judged from recent data, not from which apps have written anything.
- Activity: steps come from Health Connect's total. **Applied 2026-11-11.**
- Sleep: define main sleep versus naps when a day has several sessions.
