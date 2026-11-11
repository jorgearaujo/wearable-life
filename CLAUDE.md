# CLAUDE.md

A calm, cozy pixel-art mobile game where a character's world reflects the player's real sleep, recovery and activity, read passively from Health Connect (Android) and HealthKit (iOS).

The full product spec is in `docs/spec.md`. Read it before starting any feature, and treat it as the source of truth for game rules.

`STATUS.md` says what is done, what is waiting and what is next. Read it at the start of a session and update it at the end.

## Current phase

**Phase 0 — Discovery.** The framework is decided: **Flutter + Flame** (`docs/decisions/2026-11-11-framework.md`). Data discovery is still running: the Health Connect logger is collecting on a real phone.

- Do not scaffold the real app until the project owner says to start Phase 1.
- Discovery code is throwaway. Keep it in `spikes/<name>/` and keep it small. The real app is not built on top of a spike.
- When a spike answers a question, write the finding in `docs/decisions/` or `docs/findings/` (date, question, answer, evidence).

## Rules that must never be broken

1. **The level never drops.** Flourishing only accumulates. When habits slip, things go dormant, never disappear.
2. **Hidden values never grade the player.** HRV, resting heart rate, breathing rate and SpO2 may shape the day (morning Energy, Activity target, rest mode) but never lower the Mood score, the weather or level progress. Skin temperature is not read in the first release.
3. **In-game interactions never change the meters.** Chopping wood, throwing the stick, rowing, petting the dog and skipping stones are toys.
4. **The game must be fully playable with only steps and sleep duration.** Every richer input (HRV, sleep stages, heart rate, breathing rate) is optional.
5. **Every visible change is explainable in one plain sentence,** without showing internal numbers.
6. **Health data never leaves the device.** No network calls, analytics, crash reports or logs that contain health data. No backend for health data.
7. **No medical claims** in UI text, store text or code comments meant for users.
8. **The player only ever sees Sleep, Energy and Activity** plus the world. All other numbers stay internal.

## Architecture principles

- **Scoring is a pure, platform-independent module:** inputs are health records plus time, outputs are meter values, explanations and world state. No engine or UI code inside it.
- **One data layer interface** over Health Connect and HealthKit. It reports which data quality tier is available (Full, Partial, Minimal), and scoring adapts to the tier.
- **Compare against the user's own baseline,** per data source. Never hard-code population thresholds for HRV or resting heart rate.
- **Inject time and location.** Sun position, moon phase, season, day boundaries and bedtime all depend on them; tests must be able to set any date, time and place.
- **Data arrives late and in batches.** Never assume last night's data exists at wake time; handle "not arrived yet" as a normal state.
- **World state and saved progress know nothing about the visual style:** no pixel positions, palette entries or sprite names. Places are named ("at the dock"), and distances and speeds are in neutral units. Everything specific to a style (art, shaders, scaling, fonts, tap targets, text length limits) lives in the visual layer, so a different style can be tried as a second drawing layer over the same state.
- **Visuals are built in independent layers:** sky, lighting and color grading, particles, foliage, creatures, character. Time of day and weather come from palette and lighting changes over shared art where possible.

## Working conventions

- Scoring logic gets unit tests, including tests driven by recorded sample data from `fixtures/` (real anonymized data collected in discovery).
- When a spec decision changes or an open item gets resolved, update `docs/spec.md` in the same change.
- Ask before adding a new dependency, a new permission, or anything that touches health data storage.
- If the spec is ambiguous or seems to conflict with these rules, ask instead of guessing.
- Keep changes small and focused; explain trade-offs when proposing an approach.
