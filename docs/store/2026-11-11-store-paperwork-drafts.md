# Store paperwork: first drafts

- **Date:** 2026-11-11
- **Status:** drafts for the project owner to review. Nothing here has been submitted or published. None of it is legal advice; the privacy policy in particular should be read by someone qualified before release.
- **What this covers:** (1) the not-a-medical-device statement, (2) the texts shown when asking for health permissions, (3) the Google Play health declaration, (4) the privacy policy outline, (5) Apple's equivalents.
- **Based on:** `docs/spec.md` (Privacy, Hidden values), the rules in `CLAUDE.md`, and the store research in `docs/findings/2026-11-11-wearable-apps-and-store-rules.md`. Two short web checks on 2026-11-11 confirmed that Health Connect access is declared in the Health apps declaration form on the App content page of Play Console, and that vague justifications are a listed reason for refusal.
- **Placeholders** are written `[like this]`: the game's name, the developer's name, a contact address, the policy's web address.

## 1. Not-a-medical-device statement

For the store description on both stores, and repeated in the app's settings and in the privacy policy.

> [Game] is a game. It is not a medical device and does not diagnose, treat, cure or prevent any condition. Nothing in the game is medical advice. If you are worried about your health, talk to a doctor.

Wording rules for all store and in-app text, so the statement stays true (rule 7):

- Say "sleep", "energy", "activity", "rest", "tired". Do not say "recovery score", "health score", "illness", "symptoms", "stress level", "detect" or "monitor your health".
- Rest mode is described as "a quiet day", never as a response to being unwell.
- Do not promise outcomes ("sleep better", "improve your HRV"). Describe what the game does: the world reflects your day.

## 2. Permission texts

Shown before the system permission screen. Each says what is read, what it changes that the player can see, and that it stays on the phone. This is where the spec's "the numbers are hidden, the use is not" is carried out.

**Stage 1, at first start (steps and sleep):**

> [Game] reads your steps and your sleep from Health Connect. Steps fill the Activity meter. Sleep sets the Sleep meter and how the morning starts. Your data stays on this phone: the game has no account and sends nothing anywhere.

**Stage 2, offered later (heart rate, resting heart rate, heart rate variability, breathing rate, exercise):**

> With a wearable, [Game] can also read your heart rate, resting heart rate, heart rate variability, breathing rate and workouts. They shape the day: how full Energy starts in the morning, how much activity the day asks for, and whether the world suggests a quiet day. They never lower your Mood score or your level. You will not see these numbers in the game, only what they change, and tapping a meter tells you why. This is optional; the game is complete without it.

**Background and history:**

> Reading in the background lets the world be up to date when you open the game. Reading your past data lets the game learn what is usual for you from the first day.

**Privacy policy link** sits on each of these screens, as Play requires.

## 3. Google Play: health declaration

Filled in under App content > Health apps in Play Console. The live form must be checked when filling it in; its exact questions were not read.

**App purpose (draft):**

> [Game] is a health-integrated game. The player's real steps, sleep and heart data drive the game: three meters (Sleep, Energy, Activity), the weather and the growth of the game world. All processing happens on the device. The game has no account, no server and no advertising.

**Justification per permission.** Each names the visible feature, because "needed for app functionality" is the example Google gives of a refusal.

| Permission | Stage | What the player sees because of it |
| --- | --- | --- |
| `READ_STEPS` | 1 | The Activity meter fills with daily steps. Required: the game is playable on steps and sleep alone. |
| `READ_SLEEP` | 1 | The Sleep meter's morning value, the bedtime suggestion and the morning weather come from last night's sleep duration and stages. Required. |
| `READ_HEART_RATE` | 2 | Activity counts effort, not only steps: a run fills the meter faster than a stroll. Energy drains faster on a hard day. |
| `READ_EXERCISE` | 2 | Workouts recorded by the wearable count toward Activity. |
| `READ_RESTING_HEART_RATE` | 2 | Sets how full Energy starts in the morning, compared with the player's own usual value. Tapping Energy states this in a sentence. |
| `READ_HEART_RATE_VARIABILITY` | 2 | Same feature: morning Energy and the day's Activity target, compared with the player's own usual value. |
| `READ_RESPIRATORY_RATE` | 2 | Same feature: morning Energy, compared with the player's own usual value. |
| `READ_HEALTH_DATA_IN_BACKGROUND` | 1 | The world and meters are current when the game is opened; wearable apps write data in batches, sometimes hours late. |
| `READ_HEALTH_DATA_HISTORY` | 1 | The game compares each day with what is usual for this player; past data lets it do so from the first day instead of after weeks. |

Not requested in the first release: skin temperature (decided 2026-11-11), blood oxygen (only if a visible feature needs it), and every write permission. Mindfulness sessions are a spec input for regaining Energy; whether to request `READ_MINDFULNESS` in stage 2 is open.

**Points a reviewer may question, and the answer:**

- *A game reading heart rate variability and resting heart rate.* No other game was found doing so. The answer is the visible feature (morning Energy and the sentence shown on tap) and that the values are only compared with the player's own baseline, never shown, stored off the device or interpreted medically. If refused, the game still works: rule 4.
- *Data use limited to features visible in the interface.* Every permission above maps to a meter the player sees and a sentence the player can read.
- *Encryption at rest and in transit.* See `docs/decisions/2026-11-11-encryption-at-rest.md`. Nothing is in transit.

**Play's Data safety form** (separate from the health declaration), as the design stands: no data collected, no data shared. "Collected" in that form means sent off the device, and nothing is. This answer is only true while the app has no analytics, crash reporting or advertising library; adding any one of them changes it.

## 4. Privacy policy outline

Must be at a public web address, linked from the store pages and from inside the app. A short, plain policy is possible because so little happens.

1. **Who we are.** [Developer], contact [address].
2. **The short version.** The game reads health data from Health Connect or Apple Health on your phone. It never leaves your phone. We cannot see it. There is no account.
3. **What the game reads.** The list from section 2, in plain words, split into "always" (steps, sleep) and "only if you allow it" (heart rate, resting heart rate, heart rate variability, breathing rate, workouts). Reading in the background and reading past data.
4. **What the game does with it.** Works out the three meters, the weather and the growth of the world. Says openly that heart data shapes Energy and the day's activity target, and that the numbers themselves are not shown.
5. **What is stored on your phone.** Daily meter results, your usual values (baselines), and the state of the world. Encrypted by the game with a key that stays on the phone, and kept out of cloud backups (decided 2026-11-11). Separately, your level and the state of your world, with no health figures, are included in your phone's own backup to your Google or Apple account, so a new phone can restore them; we never receive them.
6. **What we do not do.** No server, no account, no advertising, no analytics, no crash reports containing health data, no selling or sharing, no use for anything other than the game.
7. **Your control.** Remove any permission in Health Connect or Apple Health at any time; the game keeps working with less. Erase everything the game has stored, from its settings. Uninstalling removes it too.
8. **Not a medical device.** The statement from section 1.
9. **Children.** The game is not aimed at children. (An age rating and a decision on the minimum age are needed; Play does not allow Health Connect apps aimed solely at children.)
10. **Changes.** How a change to the policy is announced; the date of the current version.

Open questions for the policy, for whoever reviews it:

- **Data protection law.** The data is special-category data under GDPR, but the developer never receives it. Whether the developer is a "controller" at all for data that stays on the player's device, and what the policy must therefore say about legal basis and rights, needs a qualified answer.
- **Weekly goals** ship inside the app, so they add no network call. If that ever changes, sections 2 and 6 change with it.
- **Who the developer is** (a person or a company) decides what contact details the stores show publicly.

## 5. Apple App Store

- **Usage text** (`NSHealthShareUsageDescription`), draft: "[Game] reads your steps, sleep and heart data to set the Sleep, Energy and Activity meters and the state of the game world. The data stays on this device."
- No write access is requested, so no update usage text is needed.
- The store description must make the use of health data clear and carry the statement from section 1.
- Health information must not be stored in iCloud (guideline 5.1.3): the encrypted file is excluded from backup. The progress-only file (level, world state) is included; whether Apple counts it as health information is to be confirmed. See the encryption decision.
- Apple does not name games as an approved use of HealthKit. The app must show a visible health or fitness purpose; the three meters are that purpose. This is a review risk that cannot be settled on paper.
- Privacy "nutrition label": data not collected, on the same condition as Play's Data safety form.

## Still to do before release

- Fill the placeholders; decide who the developer of record is.
- Have the privacy policy reviewed; publish it at a public address.
- Read the live Play Console form and adjust section 3 to its questions.
- Decide `READ_MINDFULNESS`, the minimum age, and confirm the two checks on progress in the system backup (Apple guideline 5.1.3; Android backup without the internet permission).
- Translate the permission texts along with the rest of the game.
