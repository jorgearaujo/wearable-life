# Wearable Life Game — Concept Spec v2

Last updated: 2026-11-11

## Concept and platforms

A calm, cozy mobile game where a character's world reflects the player's real sleep, recovery and activity, read passively from their wearable. The player never logs anything: they live their life, and the character and the world respond.

- **Purpose:** players use the app to check their health and see how their habits play out. It is not competitive.
- **Data sources:** Google Health Connect on Android and Apple HealthKit on iOS. Both are planned from the start.
- **App framework / engine:** Flutter with the Flame game engine, with our own native bridge to Health Connect and HealthKit (see `docs/decisions/`).
- **Orientation:** portrait only in v1. Scenes are authored wider than the portrait frame so a landscape mode (tablets, foldables, phone on a stand) can be added later as a camera change, not a redesign.
- **What the player sees:** only three meters (Sleep, Energy, Activity) plus the world itself. All other numbers are internal.

## Project phases

1. **Phase 0 — Discovery**
   - **Framework discovery:** compare candidate stacks (for example Godot, Unity, Flutter + Flame) against the criteria below, build a throwaway spike in the top one or two, and record the decision.
   - **Data discovery:** a bare app that only reads Health Connect (and HealthKit when possible) and logs what arrives and when, run on real wearables for 1–2 weeks. Output: which data types each wearable provides, typical sync delays, and sample data files for testing.
2. **Phase 1 — Scoring prototype:** the meters, baselines and Mood score running on real data with placeholder visuals (plain bars, simple shapes). Goal: check the meters feel fair and explainable.
3. **Phase 1b — Visual style exploration** (in parallel, independent of code): settle the pixel-art direction, day and night palettes, and one scene mock-up.
4. **Phase 2 — Phased build plan,** written once Phases 0–1 have replaced guesses with facts.

**Framework criteria**

| Criterion | What to check |
| --- | --- |
| Health Connect access | Read all needed data types, background reads, history reads; plugin maturity or effort of a native bridge |
| HealthKit access | Same on iOS, including behavior while the phone is locked |
| 2D pixel-art rendering | Layered parallax scenes, pixel-perfect scaling, custom shaders (palette swaps, color grading), particles. If pixel art in a 3D setting is chosen: 3D scenes with pixelated rendering |
| Performance and battery | Smooth animation on mid-range phones; low battery use while the app is open |
| Phone integration | Next alarm time (Android), coarse location, notifications |
| Developer experience | Iteration speed, testing support, how well a coding agent can work in it, tooling for pixel art and animation |
| Shipping | Build size, store requirements, licensing costs |

## Data

The game reads everything it needs from Health Connect or HealthKit and works at every level of data quality. Data discovery will confirm exactly which data types each major wearable provides.

**Inputs**

- Sleep: duration, stages (Deep, REM), timing, efficiency, naps
- Heart: heart rate, resting heart rate, HRV (when available)
- Breathing rate, SpO2 (when available)
- Activity: heart-rate-based strain, exercise sessions, steps
- Next alarm on the phone, for wake time (Android only; iOS offers no way to read it, so the usual wake time is used there)

Skin temperature is not read in the first release (decided 2026-11-11): one wearable app in six writes it, and Google Play reviews that permission more strictly.

**Data quality: decided per input.** The game must be fully playable with only steps and sleep duration, and that is the expected case for many players, not a rare fallback. Real wearable apps do not write neat bundles (one has HRV but no breathing rate, another has heart rate but no resting heart rate), so scoring checks each input on its own and uses what is there. See `docs/findings/2026-11-11-wearable-apps-and-store-rules.md`.

| Input present | What it adds |
| --- | --- |
| Steps and sleep duration (always required; phone only works for steps) | Activity from steps; simple sleep and energy |
| Sleep stages | Deep + REM in the sleep score |
| Heart rate | Heart-rate strain for Activity and Energy drain |
| Resting heart rate | Recovery compared with the player's baseline |
| Breathing rate | Sharper recovery |
| HRV | Sharpest recovery |

The names Full, Partial and Minimal remain as shorthand for the data layer: Minimal is steps and sleep only, Full is every input above, Partial is anything in between.

**Sharing must be switched on by the player.** No wearable app writes to Health Connect by default. Onboarding explains how to turn sharing on in the player's wearable app; without it the game sees only the phone's steps.

**HRV fallback.** HRV cannot be calculated from Health Connect heart rate samples, which are averaged BPM, not beat-to-beat intervals. Without HRV, recovery uses overnight resting heart rate versus the user's baseline, breathing rate versus baseline, and the sleep score. HRV is an optional input that sharpens the score.

**Baselines, not fixed thresholds.** Apple Watch records HRV as SDNN from occasional readings; most Android wearables record RMSSD overnight. Every metric is compared with the user's own baseline, per data source.

**Syncing**

- Pull data periodically, plus on every app open. Wearable apps often write to Health Connect in batches, sometimes an hour or more after waking.
- Request background reads and history reads (older than 30 days) on Android.
- iOS: HealthKit can't be read while the phone is locked, so plan to catch up when the app opens rather than relying on background delivery.
- Intraday strain arrives in jumps; the Energy chart behaves like a forecast, not a live gauge.

**Calibration**

- Minimum 24 hours, even when there is already plenty of data. More time if little history exists.
- History reads build the baseline immediately where possible.
- While the baseline is still forming, scores move less sharply.

## Core meters

The player sees three meters: Sleep, Energy and Activity. Each must be explainable in one sentence when tapped.

### Sleep (sleep pressure)

- **Morning:** last night's sleep score sets the starting value. From there the meter falls in a straight line to the zero point (decided 2026-11-11 for the prototype; to be judged by feel). The score is Whoop-like: hours versus need, consistency, efficiency, Deep + REM.
- **During the day:** the meter drains as sleep pressure builds.
- **Bedtime recommendation:** based on sleep need plus sleep debt, counted back from the next phone alarm (or the usual wake time when there's no alarm). It can shift during the day with strain.
- **Sleep need** starts at 7 hours and may learn from the player's own longer nights, between 7 and 9 hours (decided 2026-11-11).
- **Sleep debt:** capped at 2 hours. The bedtime recommendation repays at most 30 minutes a day, so it stays doable.
- **Zero point:** the meter reaches 0 at the recommended bedtime + 1 hour.
- **Naps** restore part of the meter.
- Internally this is sleep pressure, not a draining sleep score.

### Energy

- **Morning:** starts at the recovery score (Whoop-like: HRV when available, resting heart rate, breathing rate, sleep score).
- **During the day:** drains with strain.
- **Hard to regain, but not impossible.** The player has a few levers: naps, quiet periods with low heart rate, and mindfulness or breathing sessions when the device records them.
- A clear chart shows whether the player risks reaching 0 before bedtime. It behaves like a forecast, since data arrives in batches.

### Activity

- **No fixed start value or time:** the meter carries over from one day to the next (decided 2026-11-11).
- **Target:** reaching the day's strain target means hitting 100. The target is set by the Energy level at the start of the day, so a low morning asks for less. For the Mood score a good morning never makes the day harder: it counts against the smaller of the usual target and today's.
- **Inputs:** heart-rate strain for intensity (workouts, runs) blended with steps for general movement, so a 15,000-step day at low heart rate still counts. Steps alone are the fallback for players without a wearable.
- **Daily steps come from Health Connect's own total,** never from adding sources together. A wearable and the phone count mostly the same steps; the total takes one source where both have data and fills each one's gaps. It follows the source order the player sets in Health Connect. (Decided 2026-11-11; HealthKit's equivalent is untested.)
- **Draining:** drains whenever no strain is being added, and reaches 0 after about 48 to 72 hours of doing practically nothing.
- **Overdoing it:** activity beyond the target causes extra Energy drain, on top of the normal strain drain.

## Hidden values and explainability

The game uses many internal numbers to make decisions, but every visible change must be explainable in one plain sentence.

- **Hidden inputs may shape the day:** HRV, resting heart rate and breathing rate can set morning Energy, adjust the Activity target, or trigger rest mode. Players experience this as "my body is tired today", which feels fair.
- **Hidden inputs never grade the player:** metrics the player doesn't directly control never lower the Mood score, the weather or level progress.
- **The numbers are hidden, the use is not:** the permission screen, onboarding and the privacy policy say in plain words which data shapes Energy and the day. Only the internal numbers stay out of sight.
- **A night whose data never arrives** (decided 2026-11-11): after 4 hours the character wakes anyway, the meters start from the player's usual values, and that night is left out of the Mood score.
- **Tap for the reason:** tapping a meter gives a plain-language cause without showing the number. Example: "Energy starts lower today: your resting heart rate is higher than usual." A reason is at most about 75 letters in English, which is four lines in the speech bubble (decided 2026-11-11; `spikes/fw-flame/README.md`).

## Mood score, level and rest mode

Progress only ever moves forward; the current state shows through the weather and mood, never through losing what was earned.

### Mood score

The weekly score is called the Mood score (named 2026-11-11).

- Reflects how well the player did over the past week on Sleep, Energy and Activity, plus weekly goals. It is the three meters combined, counting only what the player controls (decided 2026-11-11, to try in Phase 1; `docs/decisions/2026-11-11-scoring-rules.md`):
  - Sleep: sleeping as long as needed, at the usual times. Sleep stages are not counted.
  - Activity: reaching the day's target.
  - Energy: not running out before the recommended bedtime. Where Energy started in the morning is not counted.
- A player who meets all three every day of the week has a Mood score of 100. How easy that is in practice is to be checked on real data.
- SpO2 is not part of it; it may only adjust the day.
- Drives the weather (see The world).

### Level and flourishing

- The level rises with consistently good habits and completed weekly goals.
- **The level never drops.** Flourishing is permanent and only accumulates.
- When habits slip, things go dormant rather than disappearing: animals hide, flowers close, but they come back.
- Weekly goals are set by an admin, not by the player, and ship inside the app: a change to the goals arrives with an app update, and the app makes no network call for them (decided 2026-11-11).

### Rest mode

- For illness, injury, travel and similar periods. Resting is rewarded instead of penalized.
- Turned on by the player. An automatic suggestion based on skin temperature was dropped for the first release.

## Visual direction

Pixel art in the spirit of Cast n Chill: charming, calm, and genuinely beautiful. Visual design ideas are still being explored before the final style is locked.

- **References:** Cast n Chill is the lead and defines the look; the others only fill gaps (see References below). Wildwood's stop-motion look was considered but is far more expensive to produce.
- **Built in layers:** sky, lighting and color grading, particles (rain, snow, leaves, petals, fog), foliage, creatures, character. Each layer animates on its own, and time of day and weather come largely from palette and lighting changes over shared art.
- **Portrait only in v1,** with scenes wider than the frame and a camera that pans as the character moves.
- **Night is its own look,** not a darkened day. Many opens happen after dark, especially in winter. Night is designed in its own visual design phase.
- **Bad weather still looks great and cozy.** Storms should feel sheltered, never punishing.

### References

**Cast n Chill is the lead reference and defines the game's look, including the character style.** When references disagree, Cast n Chill wins. The other references only cover what Cast n Chill doesn't: Kingdom Two Crowns for how the world changes over time, Celeste for how the character moves and expresses state, and Miki for charm. All of them work within Cast n Chill's pixel resolution and palette.

**Cast n Chill (lead): what defines the game**

- **The premise image:** a character and their dog in a small boat on calm water. This is literally the calibration intro, and the boat and dog stay central afterwards.
- **Pixel resolution and palette:** the target density of detail, and the color world the whole game lives in.
- **Lush, almost over-the-top nature:** dense layered forests, rich foliage, big skies, water as the heart of every scene.
- **Time-of-day color:** each moment of the day has its own palette (for example pink mornings and deep blue nights), not just brighter or darker versions of one scene. Fog rolls in on early mornings, reflections shift with the light, and sunsets bathe the scene in warm color.
- **Note:** Cast n Chill changes with time of day but has no dynamic weather or seasons (its winter is a separate location). That is why Kingdom Two Crowns is the reference for weather and seasons.
- **Side-view composition with depth:** layered backgrounds and a camera that moves gently through wide scenes.
- **Water and sky together:** light and color on the water carrying the mood of the moment.
- **Character and dog style:** small pixel figures that sit naturally in the landscape, drawn at the same resolution and palette as the world. This is the base style for our character and dog.
- **Calm pacing and the dog as companion:** a game designed to be pleasant to simply watch, with a loyal dog that makes the scene feel lived-in.
- **Minimal, unobtrusive UI** that leaves the scene in front.

**Supporting references: only for what Cast n Chill doesn't cover**

| Reference | Take from it | Leave out |
| --- | --- | --- |
| [Kingdom Two Crowns](https://store.steampowered.com/app/701160/Kingdom_Two_Crowns/) | How one place transforms with seasons and weather (snow, autumn colors, rain; fog is reserved for sleep); the world visibly growing as you progress (a model for flourishing); wildlife wandering the scene; the world itself telling you what's going on | Its art style and pixel resolution; combat, nightly threats and any sense that darkness is dangerous (night here is safe and cozy); management pressure; landscape-only framing |
| [Celeste](https://store.steampowered.com/app/504230/Celeste/) | Small character sprites that stay readable; satisfying feedback on actions (light squash and stretch, dust, small bounces); character state shown on the character (as Madeline's hair shows her dash); the campfire scene as the mood for the evening wind-down; gentle, non-judging design | Its environment style and pixel resolution; Madeline's look; platforming difficulty and pace |
| Miki from [Neko Odyssey](https://store.steampowered.com/app/2476350/) | Character charm and warmth; how a distinctive silhouette makes a character recognizable | Her look: outfit, hairstyle, palette, silhouette. Her level of detail and anime-style proportions. Neko Odyssey's 3D setting (see Open items) |

### Character (original design)

The main character is an original design in the Cast n Chill character style: a small pixel figure that belongs in the landscape, expressive mainly through motion rather than facial detail. References guide the style and feel, never the look of a specific existing character.

- **Base style: Cast n Chill.** The character and dog are drawn like Cast n Chill's: small figures at the same pixel resolution and palette as the world, so they never look pasted in. The world is the star, and the character lives inside it.
- **Layered on top:**
    - **Celeste** for how the character moves and expresses state: readable small-sprite animation, satisfying feedback on actions, and tiredness or energy shown through the body.
    - **Miki from Neko Odyssey** for charm and a recognizable silhouette.
- **Why small:** small, simple sprites keep the animation workload manageable across every action and seasonal outfit.
- **Qualities to aim for** (adjust to taste):
    - Small, simple sprite in Cast n Chill's style, at its pixel resolution
    - Expression through body language and motion: yawning, slow walking when tired, stretching, looking around
    - A warm, distinctive silhouette recognizable even at tiny size, helped by one signature item (for example a hat, scarf or backpack)
    - Soft palette that sits naturally in the Cast n Chill–style scenes
    - Warm, gentle personality that comes across without dialogue
- **Close-ups at key moments:** the camera zooms in during the morning reveal and the evening campfire, so players see the character's expression and bond with them. The rest of the time the character stays small in the landscape.
- **The dog gets as much personality as the character.** Players often bond with the companion first; give it its own idle behaviors, reactions and moods.
- **Seasonal outfits:** shorts and a T-shirt in summer, layers in autumn, winter gear in snow, rain gear on wet days. The signature item stays in every outfit.
- **Must be clearly distinct from Cast n Chill's characters, Miki and Madeline:** same style family, but our own outfit, hairstyle, color palette and silhouette. The dog is our own design too.
- **Never use an existing character's name in AI image prompts or art briefs**; describe the qualities instead.

## Audio

Sound matters as much as the visuals for a calm game. Audio is layered like the visuals and follows the same real-world state.

- **Ambient layers:** fire crackle, water lapping, wind, rain, thunder, snow hush, birds by day, crickets and owls at night. Each follows weather, season and time of day.
- **Music:** calm and sparse, changing gently with time of day and season. Never loud or urgent, even in bad weather.
- **Action sounds:** soft, satisfying feedback for every interaction (chopping, a stone skipping, oars, the dog's tail thumping).
- **Rituals:** the morning reveal and the evening wind-down each get their own gentle audio cue.
- **Silent by default when the phone is on silent;** works well with headphones.
- **Reference:** Celeste's soundtrack for how much music can carry the mood.

## The world

Everything in the scene answers something about the player's real life or the real world.

### Calibration intro

- On first launch, the character rows a boat across a lake or fjord with their dog in a stunning landscape while data is collected.
- Calibration lasts at least 24 hours, longer when there's little data. The game starts for real the first morning after calibration ends.
- When it ends, the character reaches land in a smooth animation and can start moving freely.

### Weather

The Mood score sets the weather, and the real season sets its look. Days in between get in-between weather: rain instead of heavy rain, cloudy instead of sunny.

| Season | Good day | Bad day |
| --- | --- | --- |
| Spring | Sunny, flowers up everywhere in many colors, bees moving between them | Heavy rain, flowers pushed down and looking sad |
| Summer | Sunny and pleasant, character in shorts and a T-shirt | Stormy with rain; hail on a very bad day |
| Autumn | Sunny, autumn leaves falling calmly | Very windy, trees losing huge amounts of leaves, hard to move |
| Winter | Sunny snow sparkling in the light, perfect skiing weather | Blizzard, barely able to see |

### Time, sun and moon

- **Time of day follows the real clock:** night, dawn, morning, afternoon, dusk, evening, night.
- **The sun is where it really is,** rising in the east and setting in the west at the real times. Uses coarse location, with a timezone fallback.
- **Seasons follow the real calendar** and the player's hemisphere.
- **The moon shows its real phase:** new, waxing crescent, first quarter, waxing gibbous, full, waning gibbous, third quarter, waning crescent.

### Flourishing

The player's level shows as how much the place flourishes. It starts fairly simple (but still stunning) and fills over time with more vegetation, flowers and trees, and more animals: squirrels, rabbits, deer, and eventually a moose.

## How the meters appear in the world

Each meter has a visible metaphor, so players read moods instead of numbers. Playing with these things never changes the meters.

| Meter | In the world | Rule |
| --- | --- | --- |
| Energy | The woodpile: more energy, more stacked logs | The campfire is free ambience; chopping a log and throwing it on the fire doesn't raise Energy |
| Sleep | The character and dog wind down: yawning, slower walking, the dog lying by the door, the cabin light glowing warmer near bedtime. Fog: rolls in past the recommended bedtime; in the morning, its thickness shows last night's sleep | Fog only comes from sleep (see below). It should feel like the world getting ready for sleep, not a lecture |
| Activity | The dog: when the player has been still, it brings a stick and paces. The character also moves and rows faster with higher activity | Throwing the stick is a toy and doesn't raise Activity |

**Fog is the sleep layer.** It only ever comes from sleep, never from random weather, so it stays a reliable signal.

- **Night fog = time to sleep:** rolls in after the recommended bedtime and thickens gradually, staying low over the water so the moon and stars stay visible.
- **Morning fog = last night's sleep:** thicker after a poor sleep score, light or absent after a good one. It burns off by mid-morning, so a bad night means a misty start, never a grey day.
- **Always beautiful:** light shafts through the mist, the lake fading into soft white. Cozy, never gloomy.
- **Explainable on tap:** for example "Misty morning: you slept less than you needed last night."

## Interactions and idle life

The player can do small things just for fun, so the place feels alive rather than numbers with nice visuals. Every animation shows the character actually doing the action. None of these change the meters.

- **Pet the dog:** tap the dog; the character walks over and pets its head, and the dog wags its tail.
- **Row:** the character gets into the boat from the start of the adventure and rows around.
- **Skip stones:** go to the shore, pick a stone, skip it.
- **Chop wood:** cut a log and throw it on the fire.
- **Throw the stick:** when the dog brings it.

**Idle life.** When the player watches without interacting, small things happen now and then: a bird flies past, a tree or flowers sway, the character or the dog does something on their own. This is on top of the weather.

## Rituals and retention

Players come back to check their health and see how their habits play out, anchored by three rituals.

- **Morning reveal (required):** the character is still asleep in the cabin or tent until last night's data arrives, then wakes up and the day's weather and meters are revealed. This also covers wearables that sync late. The camera starts close on the character, then pulls back to the landscape, where the amount of morning fog over the lake shows how well the player slept.
- **Evening campfire wind-down (required):** the camera moves in close to the campfire, the character banks the fire, the dog curls up, and the app gently nudges the player toward bed and putting the phone down.
- **Weekly event:** when the week's results land, something happens in the world, such as a new animal visiting or something blooming.

## Rewards

Weekly goals give meaningful items right away, and each item unlocks new things to do.

- Lantern: walk around at night. One of the first items a player earns (decided 2026-11-11): at night only the cabin window and the campfire give light, so the rest of the place is dark until the lantern arrives.
- Skis: ski in winter
- Rake: autumn activities with the leaves

A points shop may be added later.

## Privacy

All health data stays on the device, read from Health Connect or HealthKit. The app makes no medical claims. Health data is special-category data under GDPR, and Google Play's health app declaration applies.

- **Permissions are asked for in stages:** steps and sleep first; heart rate, resting heart rate, HRV and breathing rate later, each with a written reason. SpO2 only if a visible feature needs it. Skin temperature is not requested.
- **What the game stores is encrypted by the app** (decided 2026-11-11, `docs/decisions/2026-11-11-encryption-at-rest.md`): one small file in the app's private storage, with a key held in the phone's secure key store, kept out of backups. It holds reduced daily figures, baselines and meter results, never raw records. The Android app ships without the internet permission.
- **Progress survives a phone change through the system backup** of the player's Google or Apple account (decided 2026-11-11, for now): a separate file with only the level, unlocked items and world state. No login, no phone number, no server. It does not move between Android and iPhone. To confirm before release: Apple's rule against health information in iCloud, and Android backup without the internet permission.
- **Store requirements:** a privacy policy at a public address, reachable from the permission screen, and a statement in the store text that the app is not a medical device. Neither sends health data anywhere.

## Open items

- [x] App framework / engine (Phase 0): Flutter + Flame, `docs/decisions/2026-11-11-framework.md`
- [ ] Data discovery: which data types each major wearable writes to Health Connect and HealthKit, and when (Phase 0)
- [x] Name for the weekly score: Mood score
- [x] Weekly goals: set by an admin, not by the player, and shipped inside the app (decided 2026-11-11). The goals themselves, and how they rotate from week to week, are still to be designed (deferred by the project owner, 2026-11-11). First ideas: a minimum Sleep level, reaching a step count, filling the Activity meter. Each has to be worded without internal numbers and must not depend on hidden values.
- [x] Progress when a player changes phones: progress-only file in the system backup, for now (`docs/decisions/2026-11-11-encryption-at-rest.md`)
- [ ] Moving progress between Android and iPhone (later; a manual transfer is the candidate)
- [ ] Final visual style after exploring design ideas
- [ ] Character design: original concept based on the qualities in Visual direction
- [ ] Rendering approach: flat 2D layers (Cast n Chill) or pixel art in a 3D setting (Neko Odyssey); affects the framework choice
- [ ] Portrait composition reference: find a portrait mobile game whose scene composition works well on a tall screen
- [ ] Mood board and one test scene (character, dog and campfire in one weather state, at the chosen pixel resolution) to check the references work together
- [ ] Music and sound: compose, license, or commission
- [ ] Sleep anxiety: avoid making the sleep meter a source of stress (later)
- [ ] Landscape mode (later)
- [ ] Points shop (later)
- [ ] Search for indie games driven by wearable data, beyond Finch, Pokémon Sleep and Pikmin Bloom
