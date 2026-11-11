# Official wearable apps and store rules (desk research)

- **Date:** 2026-11-11
- **Questions:** (1) What do the official wearable apps write to Health Connect, and when? (2) Do Google Play and the App Store allow a game to read this data, and under what conditions?
- **Answer:** (1) Every official app needs the player to switch sharing on, and **only Fitbit / Google Health writes the full set of inputs the spec uses.** The others leave out HRV, resting heart rate or breathing rate, so most players with a wearable will not reach the Full tier. No vendor publishes how long after waking the night's data arrives. (2) **Google Play names games as an approved use of Health Connect**, with conditions. Skin temperature is singled out for stricter review, and data use must serve features visible in the app, which needs a decision about our hidden inputs. Apple neither permits nor forbids games; the app must have a visible health or fitness purpose.
- **Evidence:** Web research on 2026-11-11. No app was installed or observed. Sources are listed per section, with how far each was checked.

## How far to trust this

| Checked how | Applies to |
| --- | --- |
| **Page read twice** (research, then a separate check of the key claims) | Samsung's data table, Fitbit / Google Health's write list, Android's phone step counting, Google Play's Health Connect page (games paragraph, heightened scrutiny) |
| **Page read once** | Oura, Apple review guidelines, Android developer pages |
| **Search snippets and third-party quotes only** (the vendor's page could not be opened) | Whoop, Garmin, Withings |
| **User reports** (forums, issue trackers) | All timing and reliability remarks |

Vendors name categories ("heart rate", "sleep"), not Health Connect record types, except Samsung. A category being listed does not tell us the record's shape; the data findings show shapes differ between sources.

## 1. What the official apps write

"Yes" means the vendor lists it. "No" means a published list exists and the type is absent. "?" means no reliable statement was found.

| Input | Fitbit / Google Health | Oura | Whoop | Garmin | Samsung Health | Withings |
| --- | --- | --- | --- | --- | --- | --- |
| Steps | Yes | Yes | Conflicting | Yes | Yes | Reported |
| Sleep | Yes | Yes | Yes | Yes | Yes | ? |
| Sleep stages | Yes | Yes | ? | Yes | Yes | ? |
| Heart rate | Yes | Yes, 1-minute | No | Yes | Yes | ? |
| Resting heart rate | Yes | Night-time only | Yes | No | No | ? |
| HRV | Yes | Yes | No | No | No | ? |
| Breathing rate | Yes | No | Yes | No | No | ? |
| Blood oxygen | No | ? | Yes | No | Yes | ? |
| Skin temperature | Yes | No | No | No | No | ? |
| Exercise sessions | Yes | Yes | Yes | Yes | Yes | ? |
| Sharing is on by default | No | No | No | No | No | No |

Against the spec's tiers:

| App | Tier reached | What is missing for the next tier |
| --- | --- | --- |
| Fitbit / Google Health | **Full** | – |
| Oura | Partial, plus HRV | Breathing rate |
| Whoop (official app) | Partial, without heart rate | HRV, heart rate samples (strain) |
| Garmin | Below Partial as written | Resting heart rate, HRV, breathing rate |
| Samsung Health | Below Partial as written | Resting heart rate, HRV, breathing rate |
| Withings | Unknown; at least Minimal if steps and sleep arrive | – |
| Phone only | Minimal, activity half only | Sleep |

### Per app

- **Fitbit / Google Health** (renamed in May 2026). Sharing is switched on under Connections > Partner apps. Writes steps, distance, floors, exercise with route, total calories, sleep sessions and stages, heart rate, HRV, resting heart rate, breathing rate, skin temperature, body temperature. Blood oxygen and active calories are in its read list only. A user report describes HRV record counts for one night changing between reads and a partial night being completed later, which matches finding 10 of the data findings (sources rewrite records).
  Sources: support.google.com/fitbit/answer/14506680 (read twice); github.com/owen282000/life-dashboard-companion-app/issues/53 (user report).
- **Oura.** Sharing is switched on under Settings > Data Sharing > Health Connect; needs a Gen3 or later ring and a membership. Lists steps, sleep (stages according to its blog), heart rate at 1-minute resolution, HRV, exercise, active calories, distance. Breathing rate and temperature are not listed. Resting heart rate appears only as a night-time figure.
  Sources: support.ouraring.com/hc/en-us/articles/10786105824531 (updated 19 Aug 2026); ouraring.com/blog/data-sharing-partner-integrations/.
- **Whoop (official app).** Sharing since July 2023 under More > Integrations > Health Connect. Lists sleep, resting heart rate, breathing rate, blood oxygen, exercise, calories. HRV, heart rate and skin temperature are not on the list. Steps are conflicting: users report them missing from June 2025 to about May 2026, then arriving in batches about two days late. Users say the app often has to be opened for data to appear. Whether a membership is needed is conflicting.
  Sources (not opened directly): support.whoop.com "Google Health Integration for Android"; community.whoop.com threads 3156 and 3702; ultrafit360.com/blog/whoop-apple-health-health-connect; gadgetsandwearables.com (14 Jul 2023).
  Note: this is very different from the project owner's own Whoop reader (`app.pulse`), which writes the Full set. The data on the test phone does not represent Whoop owners.
- **Garmin Connect.** Since mid-2025, Android 14 or later, one way only, sent after each device sync. Lists steps, sleep with stages, heart rate, exercise, active and total calories, distance. No resting heart rate, HRV, breathing rate, blood oxygen or temperature.
  Sources: developer.android.com/health-and-fitness/community/newsletters/2025/08; notebookcheck.net (9 Jul 2025); ultrafit360.com/blog/garmin-apple-health-health-connect.
- **Samsung Health.** "To start data synchronization … you must enable it in the Samsung Health application." Its published table maps: all steps, blood oxygen, blood pressure, blood glucose, exercise (session, calories, distance, heart rate, power, speed, VO2 max), heart rate, nutrition, sleep session and stages, weight and body measurements. HRV, resting heart rate, breathing rate and skin temperature are not in it. "The Samsung Health's activity tracker data are not synchronized with Health Connect." Data reaches the phone when the watch reconnects or the user opens or refreshes the Samsung Health home screen; continuous heart rate "is not sent to the Samsung Health application on the smartphone immediately", for battery reasons. Users report steps arriving as one record covering the whole day, which would defeat per-minute comparison between sources.
  Sources: developer.samsung.com/health/blog/en/accessing-samsung-health-data-through-health-connect (18 Feb 2025, read twice); developer.samsung.com/health/health-connect-faq.html; Samsung Community threads us_3351258 and us_3154581 (user reports).
- **Withings.** Sharing is switched on under Profile > Settings. No published list of types was found. Its help text says to wait at least 15 minutes. Press reports say accounts created on or after 13 October 2026 need the paid plan for automatic export.
  Sources (not opened directly): Withings support snippets; androidauthority.com.
- **The phone itself.** "With Android 14 (API level 34) and SDK Extension version 20 or higher, Health Connect provides on-device step counting", active "only when at least one application on the device has been granted the `READ_STEPS` permission", written "no more frequently than once per minute". Records from before June 2026 carry the origin `android`; newer ones carry a per-device name beginning `com.android.healthconnect.phone.`, which "must not" be hard-coded. The name comes from `getCurrentDeviceDataSource()` (SDK Extension 22 or higher). An app that wants the phone's steps must match either origin.
  Source: developer.android.com/health-and-fitness/health-connect/features/steps (read twice).

### What this means

1. **Rule 4 describes the common case, not the fallback.** Steps and sleep are the only inputs every listed app supplies. The Minimal tier needs to be a good game in its own right.
2. **The tier table does not match real apps.** Oura has HRV but no breathing rate; Whoop has resting heart rate and breathing rate but no heart rate; Garmin and Samsung have heart rate but no resting heart rate. Tiers as fixed bundles leave four of six apps between rows. Scoring should decide per input whether it is available.
3. **Resting heart rate is missing where heart rate is present** (Garmin, Samsung). An overnight low could be derived from heart rate samples. That is a scoring design question, not answered here.
4. **Onboarding has to explain how to switch sharing on,** per app, because none does it by default. Without that step the game sees only the phone's steps.
5. **Some apps only write when opened** (Samsung, Whoop by user report). "Not arrived yet" can last all day; the architecture principle already treats this as a normal state.
6. **A paid plan may stand between the player's wearable and Health Connect** (Oura, possibly Whoop and Withings). The game cannot detect this; it sees missing data.
7. **Arrival delay after waking is still unknown for every official app.** Desk research cannot supply it. It needs testers with those apps, or stays an assumption.

## 2. Store rules

### Google Play

- **Games are an approved use.** The Health Connect policy page lists a category "Health-integrated games": "Games where gameplay mechanics, character progression, or in-game rewards are directly influenced" by the user's real activity or wellness data, with virtual pet games that need user activity among its examples. "The primary purpose must remain gaming; the app should not function as an unregulated medical tool."
- **Access is granted per data type after review.** The developer fills in a declaration with a justification for each type; the package is then allow-listed. Listed reasons for refusal include asking for a bulk list of permissions that are not needed.
- **Skin temperature gets stricter review.** "Access to high-sensitivity categories including … clinical vitals (for example, READ_BLOOD_PRESSURE, READ_SKIN_TEMPERATURE) … is subject to heightened scrutiny", and the developer must show the data is needed for a user-facing feature. HRV, resting heart rate and breathing rate are not named there. Blood oxygen is not named in that passage but appears elsewhere on the page only under medical care.
- **Data use must serve what the user can see.** Reported wording: data use is limited to "providing or improving the appropriate use case or features visible in the application's user interface." (Read once.)
- **Other conditions:** no advertising use of the data; not an app aimed solely at children; no app without a user interface; a privacy policy at a public address, reachable from the permission rationale screen; encryption of the data at rest and in transit; the store text must state that the app is not a medical device and does not diagnose, treat, cure or prevent any condition. The default history window is 30 days before the first grant.
- **Background and history permissions** are mentioned once, in a list of relevant permissions, with no rule of their own.
- **Not confirmed word for word:** on the general permissions page, the sentence listing approved uses ("fitness and wellness, rewards, fitness coaching, corporate wellness, medical care, health research, and games") and the sentence "Only applications or services with one or more features designed to benefit users' health and fitness are permitted to request access". The page was too long for the check to reach that section; both come from one reading.

Sources: support.google.com/googleplay/android-developer/answer/12991134 (read twice, in full) and /answer/9888170 (read once for the Health Connect section), /answer/16679511, /answer/14738291; developer.android.com Health Connect pages (declare access, get started, read data, feature availability).

### Apple App Store

- Guideline 2.5.1: "HealthKit should be used for health and fitness purposes and integrate with the Health app." Games are neither named as allowed nor excluded.
- Guideline 5.1.3: no advertising or data mining with health data; no health information stored in iCloud.
- The use of health data must be clear in the store text and in the app's interface; a privacy policy is required; a usage description string is required.
- Background delivery needs its own entitlement. The health store cannot be read while the phone is locked. An app cannot tell whether read access was refused: it sees no data.
- **Next alarm:** no way was found to read the phone's alarm or sleep schedule. AlarmKit (iOS 26 and later) returns only the app's own alarms. The spec already limits this input to Android.

Source: developer.apple.com/app-store/review/guidelines/ and HealthKit documentation (read once).

### Other games doing this

Pokémon Sleep reads sleep through Health Connect. Zywo: Workout Monster RPG reads steps and workouts. No game was found that reads HRV, blood oxygen, breathing rate or skin temperature.

## 3. Points where the spec and the rules meet

**Decided by the project owner on 2026-11-11 and applied to `docs/spec.md`:** (1) the use of hidden inputs is stated openly, only the numbers stay hidden; (2) skin temperature is dropped from the first release and the illness wording removed; (3) permissions are requested in the staged order below. Point 4 is drafted in `docs/store/2026-11-11-store-paperwork-drafts.md` and point 5 is decided in `docs/decisions/2026-11-11-encryption-at-rest.md` (the app encrypts its own file); the store texts are still drafts.

1. **Hidden inputs versus "features visible in the user interface".** Rule 8 keeps every number except Sleep, Energy and Activity out of sight; Play wants data use tied to visible features. The two fit if the game says in plain words which data shapes Energy (rule 5 already requires a one-sentence explanation), in the permission rationale screen and the privacy policy. Hiding the numbers is compatible; hiding that the data is used is not.
2. **Skin temperature.** The spec uses it to suggest rest mode and, in the weekly score section, for "illness detection". That phrase sits badly with rule 7 and with Play's medical-tool wording, and the permission is under stricter review. Only one of six apps writes it. Options: drop it from the first release; or keep it with a clearly described rest-mode feature and no illness wording.
3. **Which permissions to ask for at launch.** A long list risks refusal and nobody else's game reads vitals. A cautious order is steps and sleep first, then heart rate, resting heart rate, HRV and breathing rate with a written justification each, then blood oxygen and skin temperature only if a visible feature needs them.
4. **Store paperwork that does not exist yet:** a privacy policy at a public address, the not-a-medical-device statement, and the Play declaration form. None of it sends health data anywhere, so rule 6 is untouched.
5. **Encryption at rest.** Play asks for it. The bridge spike stores only counts; the real app's local store of health-derived values will need it. This touches health data storage and is a decision for Phase 1.

## Spec changes (applied 2026-11-11)

- Data, tiers: describe availability per input instead of three fixed bundles, and state that Minimal is the expected case for many wearables.
- Data, sources: add that sharing must be switched on by the player in each wearable app, and that onboarding guides this.
- Rest mode and weekly score: replace "illness detection" with wording that makes no medical claim; decide whether skin temperature stays.
- Phone integration: record that next alarm is Android only because iOS offers no way to read it.

## Not verified

- Anything about Whoop, Garmin and Withings beyond snippets and third-party articles.
- Time from waking to the night's data being readable, for every official app.
- Whether Oura writes blood oxygen; whether Whoop writes sleep stages.
- The two Play sentences marked above.
- Samsung's whole-day step record (user reports only).
- Apple's sleep schedule being unreadable (no documentation found either way).
- How Play reviewers treat a game asking for HRV, resting heart rate or breathing rate in practice; no precedent was found.
