# Status

Where the project stands, so a new session can pick up without the old conversation. Update it at the end of each working session. Rules live in `CLAUDE.md`, game rules in `docs/spec.md`; this file only says what is done, what is waiting and what is next.

Last updated: 2026-11-11.

## Phase

Phase 0, discovery. Framework decided: Flutter + Flame. Starting Phase 1 is the project owner's call; the real app is not scaffolded yet.

## Decided (each has a record)

| Topic | Decision | Record |
|---|---|---|
| Framework | Flutter + Flame | `docs/decisions/2026-11-11-framework.md` |
| Health data access | Our own native bridge, no third-party health plugin | `docs/decisions/2026-11-11-health-bridge.md` |
| Encryption at rest | Option B: the app encrypts its own small file, key in the phone's key store, kept out of backups, no internet permission | `docs/decisions/2026-11-11-encryption-at-rest.md` |
| Progress on a new phone | A second, progress-only file (level, unlocked items, world state) in the system backup of the player's Google or Apple account. No login, no server | same file |
| Scoring rules | A set of rules to try in Phase 1; all numbers are starting values, not yet run against data | `docs/decisions/2026-11-11-scoring-rules.md` |
| Step totals | Health Connect's own total is the rule | `docs/spec.md` |
| Skin temperature | Not read in the first release | `docs/spec.md`, `CLAUDE.md` rule 2 |
| Weekly goals | Shipped inside the app; content and rotation deferred | `docs/spec.md` |

Drafts, not submitted: `docs/store/2026-11-11-store-paperwork-drafts.md`.

## Spikes (all throwaway)

- `spikes/hc-logger` — Kotlin logger, **still collecting** on the owner's Pixel 7a. Raw pulls go to `spikes/hc-logger/data/raw/` (git-ignored, never committed).
- `spikes/hc-bridge` — background-read test of the bridge idea, installed on the phone and collecting.
- `spikes/fw-godot` — framework comparison, finished.
- `spikes/fw-flame` — the visual spike. Its `README.md` has one dated section per question answered. So far: indexed palette and time-of-day shader, firelight, mirrored water, rain and fog, meters and one-line reasons, dormant and flourishing states, sun, moon and phases, readable font (75 letters max per sentence), stars, duck and squirrel, petting the dog, skipping stones, tap to walk with the camera locked on the character, a map five screens wide with hold-to-walk, a walking-speed switch, a side-on dock at the right end, a 216-wide view (smaller pixels, the reference's size), calmer water glints, and the art redrawn twice as large and finer for that view (2 art pixels per world unit, waterline 78% down). Every pass up to the wide map ran at 60 fps, worst frame 17 ms, on the Pixel 7a; the wide map was judged smooth by the owner, with no figure reported. All art is our own placeholder shapes.

## Waiting on something

1. **Around 14 Nov 2026:** owner plugs in the phone and opens HC Bridge. Then pull (`ANDROID_SERIAL=<serial> spikes/hc-logger/scripts/pull.sh`), run `scripts/summarize.py`, read the bridge summary, and decide worker-only versus both-read in the health bridge record.
2. **End of collection (1–2 weeks):** finish `docs/findings/2026-11-11-health-connect-data.md`; apply the remaining proposed spec changes (one HRV value per night per source, sources rewriting old records, tier from recent data, main sleep versus naps); cut an anonymized fixture into `fixtures/`; run the scoring rules over the recorded days to see where a normal week lands; tick "Data discovery" in the spec.
3. **Owner decisions still open:** `READ_MINDFULNESS` yes or no, minimum age, developer of record (store drafts); weekly goal content; whether tap-to-walk with a character-locked camera goes into the spec as the navigation rule, and with it hold-to-walk.
4. **Owner's second look at the wide map on the Pixel 7a** (installed 2026-11-11): the side-on dock at the right end with open water past it (the character is centred at the dock's end), and walking at 25 px a second (the owner's choice; its beat is uneven and it has not been seen on the phone yet). Also to judge, in the build with the redrawn art (installed 2026-11-11, later the same day): the pixel size and level of detail (not decided), the framing (water in the bottom fifth, bigger trees, higher sun and moon), the fps figure (the scene is 3.2 times as many pixels as the 120 view) and the calmer water glints. Decided so far: hold-to-walk stays, spacing waits for the final visuals, the lantern is one of the first weekly-goal items.

## Next steps, in order

1. Drifting clouds as their own pieces.
2. Desk research: indie games driven by wearable data; portrait composition references.

Unsettled in the Flame spike: the redrawn sun and moon (26-px moon with seas and craters) have no verdict yet; the dithered sky band edges; the real sky look is deferred to art direction.

## Working notes for the next session

- Phone builds of any spike are **release** builds (a Flutter debug build adds the internet permission). Check the permission list before installing.
- Address the phone by its adb serial; never unlock it; capture its screen only when the owner says the spike is in the foreground.
- Never print health values in the terminal; analyse structure and timing only.
- `docs/references/` is git-ignored: other games' screenshots, for direction only. The game's setting, character, dog and palette are our own designs.
- Flame spike toolchain: `JAVA_HOME` is Android Studio's bundled runtime; art is regenerated with `python3 tools/make_art.py` from `spikes/fw-flame`; emulator AVD is `hclogger`.
