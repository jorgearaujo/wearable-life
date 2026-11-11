# fw-flame (Phase 0 spike, throwaway)

The shared framework test from the Phase 0 plan, built in Flutter 3.47.9 with Flame 1.38.2. The first pass used the same placeholder art as `spikes/fw-godot`; the second pass (see below) has its own, made by `tools/make_art.py`.

- `lib/main.dart` — portrait scene, 120 px wide (180 in the first pass), integer scaling worked out by hand from the screen width; sky plus three layers with parallax; a panning camera (drag, or it drifts on its own); an animated character; a debug label; a placeholder campfire. Tap to hold a time of day. The step count through the `health` plugin was removed on 2026-11-11 (we write our own bridge, and the plugin writes health values to the phone's log); it is in the first commit.
- `shaders/grade.frag` — one full-screen shader that turns palette indices into colours for the time of day, adds two point lights (campfire, cabin window) when it is dark, and mirrors the water.
- `tools/make_art.py` — writes the indexed placeholder art and `palette.png` (needs Pillow; run from this folder).
- `lib/daylight.dart`, `test/daylight_test.dart` — a pure-logic function and its test, with no engine involved.
- `android/` — host project. The release build asks for no permission at all: no health permission, no `INTERNET`.

## Build

```sh
flutter build apk --release --target-platform android-arm64
adb install -r build/app/outputs/flutter-apk/app-release.apk
adb shell am start -n dev.wearablelife.fw_flame/.MainActivity
dart test        # pure-logic test, no device needed
```

For screenshots: `--dart-define=FIXED_TIME=0` holds one time of day (thousandths; 0 = midnight, 500 = noon).

## Results so far (2026-11-10)

| Check | Result |
| --- | --- |
| Scene, parallax, integer scaling | Works, but parallax and integer scaling are hand-written (about 80 lines). |
| Other screen sizes (emulator, 7 sizes from 720 to 1344 px wide) | First version drew uneven pixels on 3 of 6 sizes (1–3% of art pixels). After the fix in problem 5, every art pixel is an exact square on all 7. Godot was exact on all 6 it was run on with no extra work. |
| Day → night shader | Works after one fix (see problem 1). The scene is drawn to an image at 180 px wide every frame and the shader scales it up. |
| Rain | Works. Hand-written component; Flame's particle system was not needed for it. |
| Step count | Worked on the emulator through the `health` plugin, with no Kotlin written. Removed from the spike on 2026-11-11. |
| Release build on the emulator | Runs at about 29 fps with a worst frame of 70 ms; Godot reached 43–46 fps on the same emulator. Emulator numbers are not a fair measure. |
| Release build on a Pixel 7a | Runs on Vulkan at a steady 60 fps, worst frame 17 ms, 180×400 view at 6×, scene the right way up. About 195 MB memory (Godot: about 172 MB). |
| Memory on the emulator | About 60 MB. |
| Release APK, arm64 only | 16.0 MB as a file, about 7.7 MB when compressed, which approximates the download. |
| Battery on the phone, screen on, uncapped 60 fps | 82 mAh in 16 min 20 s (872 → 790 mAh, from the phone's own battery history), an average of about 300 mA. Battery level 26% → 23%, adaptive brightness on. Same as Godot within the precision of the measurement. |
| Unit tests | `dart test` runs outside any engine. About 5 s including start-up. |
| Frame-rate cap | Not built. Flutter has no built-in cap. |

## Lighting beyond a full-screen grade (2026-11-11)

Question (risk 3 of the framework decision): Flame has no 2D lights, so can a campfire glow and a lit cabin window be built, stay pixel-exact, and leave the sky alone?

**Answer: yes, inside the grade shader we already have, with about 60 more lines.** Checked on the emulator only, in release builds, at a fixed midnight.

How it works:

- The shader gets each light as four numbers (position in view pixels, radius, strength). Inside a light's radius it mixes the night-graded pixel back toward the original daytime pixel with a warm tint, so the art's own colors return near the fire. The lights fade in as it gets dark and are off by day.
- **The falloff is stepped, not smooth:** five flat bands with a checkerboard dither between them, computed per art pixel, so the glow is made of whole art pixels like everything else.
- **The flicker is stepped too:** the campfire's radius changes 8 times a second.
- **A light mask keeps the glow off far layers.** Flame lets a post-process draw its subtree more than once, so the scene is drawn a second time at 180 px wide with the sky and hills left out; the shader lights a pixel only where that second image has something in it. Without the mask the campfire visibly lit the hills behind it. With it, the glow lands on the ground, the trees, the cabin, the character and the rain.

| Check | Result |
| --- | --- |
| Campfire glow and window light at night | Work. |
| Glow limited to near layers | Works with the mask; fails without it (hills lit). |
| Light follows the camera pan | Works; positions are passed in whole art pixels. |
| Cost on the emulator | 21 fps with the mask, 23 fps with lights but no mask, single readings on a noisy emulator. Not a fair measure. |
| Cost on the Pixel 7a | **Not measured.** The build is installed; it needs the phone unlocked with the spike open (60 fps without lights is the figure to compare with). |

Limits found:

- **The mask is all-or-nothing per layer.** A light cannot be partly hidden behind a tree trunk, and nothing casts a shadow. Per-object occlusion would need a different approach.
- **The number of lights is fixed in the shader** (two here). More lights mean more uniforms or a small light texture.
- **A light only reveals the art's daytime colors, warmed.** The green ground near the fire looks yellow-green. A hand-picked "lit" palette per layer would look better and is an art-direction question.
- The scene is now drawn twice per frame at low resolution. The mask could be redrawn only when the camera or layers move.
- **First launch after install showed a black screen for 15 to 20 seconds on the emulator** before the first frame, in every variant. Later launches were not timed. Worth checking on the phone.

## Second pass after the art references (2026-11-11)

Question: the references (`docs/references/notes.md`) ask for chunkier pixels, a bigger character, glows in clean flat bands, night and dusk as full re-colourings, and mirror reflections on water. Can the spike do all of that, and what does it cost?

**Answer: yes, and it got simpler.** The scene is now drawn once per frame instead of twice. Checked on the emulator and, for speed, on the Pixel 7a; release build. The rain, the light mask pass and the dithered glow of the first pass are gone from the code (they are in git history).

What changed:

- **View 120 art pixels wide** (was 180). On a 1080×2400 screen that is 9 screen pixels per art pixel and a 120×266 view. The camera is anchored to the bottom, so a taller screen shows more sky.
- **Character 30 art pixels tall,** about 11 % of the screen height (was 7.5 %), with a large sitting dog next to it for scale. Placeholder shapes, our own.
- **The art stores palette indices, not colours** (`tools/make_art.py`). Each pixel's red value is an index; the shader looks it up in `palette.png`, which has one row per time of day (night, dawn, day, dusk) and one row of firelit colours. Between times the shader mixes two rows. So night is not day darkened: each of the 36 colours has its own night colour, and the window, the fire, the moon and the stars stay bright. Stars are a palette entry that equals the sky colour by day.
- **Glow in three flat bands, no dither.** Inside a band the pixel moves toward its colour in the firelit row.
- **The light mask is the green channel of the art** (set where firelight may reach), so the second drawing of the scene is no longer needed.
- **Water is a mirror made in the shader:** below the waterline it reads the scene upside down, shifts whole rows sideways by a pixel or two on a slow beat, tints toward a water colour per time of day, and adds sparse bright streaks. The firelight and the window are reflected too, with no extra drawing.
- **Tap steps through** cycle, night, dawn, day, dusk, to hold a time for looking at it.

| Check | Result |
| --- | --- |
| Four times of day from one set of art | Works. Dusk is pink-purple, night near-monochrome blue with bright accents. |
| Flat-band glow, limited to near layers | Works. |
| Reflection, including lights | Works. |
| Whole-pixel scaling at 120 wide | Works on 1080×2400. Other screen sizes not rechecked. |
| Cost on the emulator | 15 to 18 fps, about the same as the first pass (21). Not a fair measure. |
| Cost on the Pixel 7a | **60 fps, worst frame 17 ms** (read off the screen by the project owner, 2026-11-11). The phone's full refresh rate, the same as before any lights were added. |

Limits found:

- **Indexed art cannot blend.** Every pixel must be one palette entry at full opacity, so soft fog, translucent rain and smooth text cannot be drawn into the scene. They need a second, ordinary layer drawn after the shader (the debug text already moved outside the game for this reason). Fog bands like the references' are the first thing to test next.
- **The references use many colours, not a small palette.** 36 entries were enough for placeholder shapes; painted scenes may need a few hundred. The lookup itself does not care (the palette image can be wider), but each entry needs a colour per time of day. Here most were generated from three-colour ramps and about 30 picked by hand; that split is an art-pipeline decision.
- **The sun and moon are painted into the sky** and do not move. They should be their own sprites placed from the injected time and location.
- **The reflection mirrors the screen,** so it can only show what is in view above the waterline, and the bank's front face is mirrored as well. Good enough at this size.
- The tap handler uses a Flame mixin that is marked as deprecated.

## Problems hit

1. **The scene rendered upside down.** A vertical flip that Flutter's shader documentation suggests for the OpenGL backend was wrong for an image produced by Flame's post-process step. Removing it fixed both the emulator (OpenGL) and the phone (Vulkan).
2. The first build downloaded a second Android platform and an NDK on its own (several minutes, about 2 GB).
3. The build warns that the `health` plugin applies the Kotlin Gradle plugin in a way future Flutter versions will reject. The plugin will need an update before a Flutter upgrade.
4. The debug text uses the default smooth font, not a pixel font. A bitmap font would need its own setup.
5. **Flame has no built-in integer scaling, and its fixed-resolution viewport stretches.** On any screen whose width or height is not a whole multiple of the scale, it stretched the picture by a fraction and some art pixels came out wider or taller than others. The fix (`PixelFit` in `lib/main.dart`, about 40 lines) puts the game in a box that is an exact whole multiple of the art size, centred on a physical pixel, leaving a border of at most a few pixels. Checked by measuring screenshots, not by eye.

## Rain and fog on top of the indexed scene (2026-11-11)

Question from the second pass: the indexed art cannot blend, so can weather be drawn as an ordinary translucent layer after the shader?

**Yes.** After the shader has drawn the scene, the same post-process step scales the canvas to art pixels and draws plain translucent rectangles on top (`_weather` in `lib/main.dart`). No second render pass and no extra image.

| Part | How | Result on the emulator |
| --- | --- | --- |
| Rain | 70 slanted streaks, 5 art pixels tall, 38% opaque, falling 150 to 220 art pixels a second | Fine streaks over sky, land and water, on the pixel grid |
| Fog | A thin veil over everything, a thicker one near the water, 9 slow wisps that stack where they overlap | Trees and hills fade back; the character and cabin stay readable |
| Muted colours | One shader input (`uWet`) pulls every scene colour toward a cool grey before the lights are added | Day, dusk and night all read as overcast; firelight stays warm |
| Weather colour | Rain and fog are ordinary colours, so each has one colour per time of day, mixed like the palette rows | Blue fog at night, pink at dawn |
| Fade | Weather fades in and out over about a second | Works |
| Window light | Radius 20 to 9, strength 0.67 to 0.34: a flat lit shape with one thin ring, as in the references | Works |

Tap now steps through: cycle, night, dawn, day, dusk, day rain, dusk rain, night rain, dawn fog, night fog. `--dart-define=HOLD=5` starts on one of them.

**Limits found**

- The sun and moon were painted into the sky art, so they still shone through the rain. Fixed in the third pass: they are their own pieces and hide in rain.
- The muting is one formula. The references pull each colour down by hand; real art would use wet palette rows (one more row per time of day).
- Fog is drawn over the lights, so it dulls the campfire glow. Drawing lights after fog would need the glow moved out of the shader or the fog moved into it.
- Fog wisps are stacked rectangles and look like bands. Drawn fog sprites would use the same layer.
- The campfire's own flame colours are muted with the scene.
- Rain drops land on the water as small ripples (added on request): 30 at a time, each a bright dot that opens into a flat ring over half a second. The water's own highlight streaks are thinned out while it rains so the rings stand out. They are drawn in the same layer and do not disturb the reflection itself.

**Cost on the Pixel 7a:** 60 fps, worst frame 17 ms with rain and fog on (read off the screen by the project owner, 2026-11-11), the same as without weather. Measured before the ripples were added.

**Bug fixed on the way:** the `Stack` holding the debug text needed an explicit alignment; without one the first frame threw on a fresh start and the screen stayed blank.

## Third pass: meters and reasons, dormant states, moving sun and moon (2026-11-11)

Three questions, all in the same scene. Checked on the emulator, release build. **Cost on the Pixel 7a:** 60 fps, worst frame 17 ms (read off the screen by the project owner, 2026-11-11), the same as every earlier pass.

### 1. Meters and the one-line reason over the scene

**Works.** The interface is an ordinary Flame component outside the camera, so the shader never touches it. It draws in ordinary colours, scaled so one unit is one art pixel, and stays on the pixel grid.

- **Meters:** three rows of five 7x7 icons at the top left (moon for Sleep, spark for Energy, boot for Activity). A filled icon is in colour; an empty one is a dark see-through shape that works on any sky. No numbers, no bars, no panel (rule 8).
- **Reason:** tap a meter row and a speech bubble appears above the character for six seconds with one sentence (rule 5). Its tail follows the character as the view pans, and the bubble stays inside the screen.
- **Text:** our own small pixel font, drawn by `tools/make_art.py` into `ui.png` (capitals, 5 pixels tall, variable width). Sentences wrap to 96 art pixels: about 25 letters a line, three lines for the longest spec example.

Limits and things learned:

- **Replaced since: see the font section below.** The first font was a placeholder and hard to read. Capitals only, and V, U, N and W are close to each other at 3 to 5 pixels wide. A real pixel font with lower case needs about 5x7 per letter, which gives about 18 letters a line at this view width: a sentence of 70 letters becomes four lines. Sentence length and font size have to be designed together.
- The meter levels and sentences are made up. Nothing reads health data.
- Flame gives the camera the highest drawing priority, so anything added beside it is drawn underneath unless the camera's priority is lowered. Flame's `size` is the camera's view in art pixels, not the widget; `canvasSize` is the widget. Both cost time here.

### 2. Dormant and flourishing states of the same things

**Works, and each state is cheap.** Tap the cabin to step through three states; tap the fire to switch it. Each tap also shows a one-line reason in the bubble.

| Thing | Dormant | Normal | Flourishing |
| --- | --- | --- | --- |
| Cabin | A tarp sprite drawn over it; the window light fades out | Open, window lit | Same, and the flower buds along the front open |
| Fire | Logs under a little ash; its light fades out | Lit | – |

- Nothing is removed: the cabin is still under the tarp, the logs stay, the flowers close into buds (rule 1).
- Cost per state: one small sprite (tarp 66x54, flowers 70x8 in two frames) and three to six palette entries, each of which gets its night, dawn and dusk colours from the same ramps.
- Lights fade over half a second. The tarp and the flowers switch at once: indexed art cannot be half transparent, so a soft change would need drawn in-between frames.

### 3. Sun and moon as their own pieces

**Works.** Each is a 35x35 indexed sprite between the sky and the hills. The sun crosses from 0.22 to 0.78 of the day and the moon from 0.72 to 0.28, each on an arc, in whole-pixel steps; they rise and set behind the ridge and are mirrored in the water. In rain both are hidden once the rain is half faded in; in fog they stay.

- A sprite with an odd size must not use a centre anchor: it lands on half pixels and the edges pick up wrong palette indices (seen as stray blue marks). Placed by its top-left corner it is clean.
- Anything pinned to the screen (sun, moon, light positions, waterline) must be placed after the camera moves in the same frame. Placed before, it sits one pixel off for a frame at every camera step, and the sun and moon visibly shook while the view panned. Seen on the phone, not on the slow emulator; fixed.
- Sun and moon have separate palette entries, so both can be in the sky at dusk in the right colours.
- **Moon phases are drawn:** eight frames in one sheet (new, crescent, quarter, gibbous, full, and the waning four), stepped by tapping the moon. Changed after a look on the phone:
  - The unlit part has its own dim colour, one palette entry with a hand-picked value per time of day, so the whole disc can be made out in every phase and the new moon is a faint disc. Left empty, the quarter moon looked like a disc cut in half.
  - The moon is 13 pixels across, the same as the sun's disc without its halo (17 was tried and looked too big next to the sun). The shadow line for crescent and gibbous is pushed further from new and full than the true geometry: with true geometry at this size, gibbous differs from full by one column.
  - The dim colour is one flat colour over a banded sky, so it sits closer to the sky in some bands than others.
- Not done: choosing the phase from the date and real positions from date and place (the spec asks for both; that is arithmetic for the pure module, not a rendering question), and a soft way to hide sun and moon (they switch off at once, behind the rain).

Palette entries: 45, up from 36.

## A readable font and how long a sentence can be (2026-11-11)

**Question:** the capitals-only placeholder was hard to read. With a font people can read, how much text fits in the speech bubble?

**Answer: a sentence of up to about 50 letters fits in two or three lines and reads well; the spec's longest example (72 letters) takes four lines and still fits.** Checked in an enlarged preview and on the emulator; cost on the Pixel 7a not yet measured.

- **The font:** our own, drawn in `tools/make_art.py`: capitals 7 pixels tall, lower case 5 tall with 2 rows below the line, letters up to 5 wide, variable width. 59 glyphs: A–Z, a–z and `. , ' ! ? - :`. Lines are 10 pixels apart and wrap at 104 of the 120 pixels across.
- **What fits:** 20 to 24 letters a line.

| Sentence | Letters | Lines |
| --- | --- | --- |
| The fire is lit again. | 22 | 1 |
| Sleep is high: a long, steady night. | 36 | 2 |
| Activity is filling up: a good walk this morning. | 49 | 2 |
| The cabin is under its cover for now. Nothing is lost. | 54 | 3 |
| Energy starts lower today: your resting heart rate is higher than usual. | 72 | 4 |

- A four-line bubble is 45 art pixels tall, about a sixth of the screen height, and covers the treeline above the character. Two lines (25 pixels) sits comfortably.
- **Rule for writing reasons (decided by the project owner, 2026-11-11, in `docs/spec.md`):** at most about 75 letters. A 50-letter target was judged too short. The font was read on the Pixel 7a and judged good.

Limits:

- English only. No digits (rule 8 keeps numbers off the screen, but dates or counts in goals may need them), no accented letters. Other languages run longer, German by roughly a third, so the same limit in letters is tighter for them.
- The glyphs are a first drawing, not tuned letter by letter, and there is no kerning.
- The font sheet is ordinary colour drawn after the shader, so text does not darken at night; the cream bubble is bright against a night scene.

## Stars and wildlife (2026-11-11)

**Is the sky built in layers?** Partly. From back to front: the sky image (colour bands and clouds, does not scroll), stars (drawn by the game), sun and moon (their own sprites), then hills, trees and ground with parallax. Clouds are still painted into the sky image; drifting clouds would need to become their own piece, like the sun and moon did.

**Stars**
- Were 16 single points painted into the sky image, in one colour, all appearing at once. Now 34 points placed by the game from a fixed seed, kept apart from each other, denser toward the top and above the clouds.
- Three kinds: four cross-shaped bright ones, eleven bright single pixels, the rest dim single pixels. One new palette entry (`star_dim`), 46 in all.
- Each star has its own darkness at which it comes out, so the bright ones appear first at dusk and go last at dawn. Each blinks now and then, in steps three times a second, not as a fade.
- Rain hides all of them; fog hides the dim ones.
- The sky's band edges are now broken up over eight rows with a checker pattern of the two colours they already have. No new entries.

**Duck**
- 12x8, two frames (the wake under it alternates), both facing directions in the sheet so it is never flipped onto half pixels.
- The shader replaces everything below the waterline with the reflection, so a sprite drawn there would vanish. Fix: sprites that float are drawn with blue set, and the shader shows those pixels as they are, without the water tint or streaks. One texture read more per pixel. This is the way to put anything on the water: a boat, lily pads, a thrown stick.
- Close under the bank it was lost in the reflection of the dog; 30 pixels out it reads clearly.

**Squirrel**
- 12x10, four frames (sitting, tail flick, two for running), both directions. Dashes along the bank right of the fire, stops and sits.
- At night and in rain it runs off to the right and stays away, then comes back: the spec's "animals hide".
- Both animals reuse colours the scene already has, so they follow time of day, weather and firelight with no extra work.

**Limits**
- Placeholder art drawn as text grids in `tools/make_art.py`; real animals want more frames and an artist's hand.
- The duck has no reflection of its own and does not react to rain rings or to the character.
- The squirrel does not avoid the fire or the dog, and has no shadow.
- Phone cost on the Pixel 7a: 60 fps, worst frame 17 ms, the same as before the stars, the animals and the extra texture read.
- The dithered band edges are not settled: the project owner is unsure about them. The sky is left as it is in this spike; how the real sky is painted (band shapes, clouds as their own pieces) is an art decision for when art direction starts.

## Interactions: petting the dog and skipping stones (2026-11-11)

Question: do touch, walking and small animations work at this pixel size, and can a toy be thrown onto the mirrored water?

- **The character acts, the player points.** A tap on the dog or on the water is a request. The character walks there first (30 art px a second), then does it. A new tap replaces the request in progress.
- **Petting.** Tap the dog: the character walks round to its head, turns to face it and moves a hand over its head for about two seconds, and the dog's tail wags. The dog is now its own two-frame sprite (it used to be painted into the ground).
- **Skipping stones.** Tap the water: the character walks to a spot one throw away from the tapped point, crouches to pick a stone, winds up and throws. The stone lands where the tap was, then skips four more times, each hop shorter and lower, with a small ring at every touch. Stone and rings use the same "floats on the water" flag as the duck, so they show in place of the reflection.
- **Character sheet.** 11 frames of 24×30 (idle 2, walk 4, pet 2, pick up, wind-up, throw), each also stored mirrored, so the game never flips a sprite. Which way it faces reads from the hat brim, the scarf tail and the hand; no drawn eyes.
- **Camera.** While the character is doing something the view follows it; a tap also holds the slow drift for three seconds. The speech bubble's tail now follows the character.
- **The meters are not touched.** Neither toy reads or changes Sleep, Energy or Activity (rule 3).

Seen on the emulator: both work end to end. Limits and things real art must solve:

- The character walks *through* the dog to reach its head, drawn in front of it. Real art needs a rule (dog stands up and turns, or the character always approaches from the head side).
- The stone is 2×1 px and the rings 2 px dashes. They are readable but small; a splash frame would help.
- The tap target for the dog is its 24×19 px box, about 1 cm on the phone. Fine for one dog; closer objects will need priorities.
- Tap order is now: meters, moon, cabin, fire, dog, water, and anything else steps the time of day.

Phone result (Pixel 7a): 60 fps, worst frame 17 ms while walking and throwing. The dog is easy to hit. Two changes after the owner's look:

- **The dog answers.** When the petting ends, a small heart rises from the dog's head, and the dog keeps wagging and bobs for a moment. Without it the petting had no ending.
- **Bigger ripples.** The stone is 2×2, each touch starts with a small splash, and the ring is a flat oval that widens in three steps (up to about 20 px across on the first touch, smaller on each skip). The water already has streaks and reflections, so a 2 px mark was lost in it.
