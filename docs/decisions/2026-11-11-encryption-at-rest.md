# Encryption at rest for what the game stores

- **Date:** 2026-11-11
- **Status:** **proposed, not decided.** This touches health data storage, so the project owner decides. Nothing is built; the real app does not exist yet.
- **Question:** Google Play asks Health Connect apps to encrypt health data at rest and in transit. What does the game store, and how should it be protected?
- **Recommendation:** store as little as possible, in one small file in the app's private storage, encrypted by the app with a key held in the phone's secure key store, and kept out of backups. This needs no new dependency. Ship the Android app without the internet permission, so "nothing in transit" can be checked by anyone.
- **Evidence:** store research in `docs/findings/2026-11-11-wearable-apps-and-store-rules.md`; data sizes in `docs/findings/2026-11-11-health-connect-data.md`; a web check on 2026-11-11 that the AndroidX security-crypto library is deprecated. Platform behaviour below is from documentation and general knowledge, not tested in this project.

## What would be stored

The game does not need its own copy of the raw records: Health Connect and HealthKit keep them, and the game can read them again.

| Stored | Health data? | Why it is needed |
| --- | --- | --- |
| One reduced figure per night and per day, per source (for example time asleep, one HRV figure, one resting heart rate, daily steps), for the baseline window | Yes | Baselines compare today with the player's usual values. History reads cover the past, but re-reading and reducing weeks of heart rate on every start is slow (tens of megabytes). |
| Baselines per source | Yes, derived | The comparison itself. |
| Daily meter results and the reasons shown | Yes, derived | The Mood score looks back over a week. |
| Level, unlocked items, world state | Game progress, derived from health data | Rule 1: the level never drops. |
| Health Connect change tokens, settings | No | Reading only what is new. |

Not stored: raw heart rate samples, sleep stage lists, anything from a third party, anything that identifies the player. The whole store is small, well under a megabyte.

## Options

| Option | Protects against | Cost |
| --- | --- | --- |
| **A. Platform storage only.** App-private files; the phone's own storage encryption (Android file-based encryption, iOS Data Protection). | A lost or stolen locked phone; other apps. | Nothing to build. Does not protect a copy that leaves the phone in a backup, or a phone with root access. Whether Play accepts this alone as "encryption at rest" is not stated anywhere we found. |
| **B. A plus the app encrypts its own file.** Authenticated encryption (AES-GCM) with a key created in the Android Keystore or iOS Keychain; the key never leaves the phone's secure hardware. | As A, plus a copied file is unreadable anywhere else. | A small piece of code in our own native bridge on each platform, using only what the platforms ship. No new dependency. The file is read and written whole, which suits a store this small. |
| **C. An encrypted database library** (SQLCipher or similar, through a Flutter plugin). | As B. | A new dependency with native code, a larger build, licence terms to check. Worth it only for a large or heavily queried store, which this is not. |

**Recommended: B.** It gives a plain answer to Play's requirement, keeps rule 6 strict, adds no dependency, and fits the decision to own the health bridge. The AndroidX library that used to wrap this is deprecated, so writing against the platform key store directly is also the current advice.

## Details that come with B

- **Backups: keep health-derived data out.** Android: exclude the file from cloud backup and device-to-device transfer. iOS: exclude it from backup, which Apple's rule against health information in iCloud requires anyway.
- **The key is tied to the phone.** A restored or new phone cannot read the old file. Combined with the backup exclusion, **a player who changes phones starts again**: baselines rebuild from history reads within a day, but the level and world would be lost. See the open question below.
- **Reading while locked.** Background reads run while the phone is locked. The key must not require the player to be present (no fingerprint prompt), only that the phone has been unlocked once since it started. On iOS the file's protection class must allow access after first unlock for the same reason.
- **An unreadable file is a normal state,** like "data not arrived yet": the game starts a fresh baseline instead of failing. It must never lower the level because of it (rule 1).
- **Erase everything** is a setting: delete the file and the key.
- **Logs** never contain health values (rule 6); this already holds for the spikes.
- **In transit:** nothing is sent. The Android app ships without the `INTERNET` permission, as the spikes do. The privacy policy link opens in the browser, which needs no permission. A release check confirms the permission is absent from the built app.

## Open questions for the project owner

1. **Approve B?** Or A only, accepting the risk that Play asks for more.
2. **Progress when changing phones.** The level and world are game progress, but they are derived from health data. Three choices:
   - *Lose them* on a new phone: simplest and strictest; hard on a long-time player, and at odds with the spirit of rule 1.
   - *Back up progress only* (level, unlocked items, world state; no health figures, no baselines): keeps the player's world. It puts a health-derived summary in the player's own cloud backup, which needs a line in the privacy policy and a view on Apple's iCloud rule.
   - *A manual transfer* the player starts on purpose (for example a file or a code moved between their own phones): nothing in the cloud, more to build.
   My recommendation is to back up progress only, and to confirm against Apple's rule before release.
3. **How long the baseline window is,** which sets how many nights of reduced figures are kept. This is a scoring decision for Phase 1; the storage design does not depend on the number.

## Not verified

- That Play accepts option A alone, or what evidence of encryption its reviewers ask for.
- Behaviour of key store keys across Android backup and restore on real devices, and of the iOS protection classes with HealthKit background delivery.
- Whether a level number and world state count as "health information" under Apple guideline 5.1.3.
