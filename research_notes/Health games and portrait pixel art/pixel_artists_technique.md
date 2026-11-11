# Pixel artists, artworks and technique for a portrait side-view landscape scene (state as of November 2026)

How to read these notes:

- **"Viewed"** means I downloaded the image file and looked at it. Shares of frame height are **my estimates by eye** (I overlaid gridlines every 10% of height on the three Living Worlds scenes; the others are plain eyeballing).
- **"Not viewed"** means I only have text about it. I do not describe the look of anything I did not view, except in clearly labelled "unverified recollection" lines in the Gaps sections.
- Many of the candidate artists could not be researched in the time available. They are listed in the Gaps of Part A, not silently dropped.
- Pages that refused automated access: Tumblr (1041uuu, Kirokaze: HTTP 403), Medium (Retronator's Kingdom article, Ian Gilman's Living Worlds article: 403), TIGSource forums (Kingdom devlog: 403), Lospec gallery tag pages (404) and full-size Lospec images, the old Effect Games Q&A mirror (connection refused). GDC Vault and YouTube talks were not watched; nothing below quotes a talk directly.

## Part A — Artists and artworks: who offers usable vertical side-view landscape references?

### Takeaway

The best vertical references I could actually view are Mark Ferrari's twelve Living Worlds scenes, which the official site shows as tall crops of 640x480 landscape originals; they show three reusable portrait recipes (reflective water in the lower half, full-height foreground tree trunks, a ground plane that climbs the frame). Most of the famous ambient pixel artists I could check work in landscape or square formats (Kirokaze, Gutty Kreum, Slynyrd) or do vertical work that is urban rather than lake-and-forest (Waneella), so they are references for mood, light and looping, not for portrait composition.

### Cited Findings

#### Mark Ferrari — Living Worlds / Seize the Day (strongest reference; viewed)

- The Living Worlds app is "a modern recreation of a set of dynamic pixel art scenes first published in the early 90s as part of an 'illustrated personal organizer' named Seize the Day"; art by Mark Ferrari, original software by Ian Gilman, extra code by Joseph Huckaby. It contains "all twelve of the original scenes". — [Pixfabrik: Living Worlds](http://pixfabrik.com/livingworlds/)
- What changes over the day, in the makers' words: "The sun rises and falls in real time, storms pass through, flowers bloom, the moon and stars cross the sky. Smaller details like chimney smoke and animal footprints come and go." — [Pixfabrik: Living Worlds](http://pixfabrik.com/livingworlds/)
- The Android version works as a live wallpaper; the iOS version does not. — [Pixfabrik: Living Worlds](http://pixfabrik.com/livingworlds/)
- The originals are 640x480, 256-colour, single flat images: the HTML5 demo uses "35 of Mark's original 640x480 pixel masterpieces", each "just one single flat image with one 256 color palette", originally Amiga IFF/ILBM files made in Deluxe Paint. — [Joseph Huckaby, "Old School Color Cycling with HTML5", Effect Games](http://www.effectgames.com/effect/article-Old_School_Color_Cycling_with_HTML5.html)
- The same scene ships as separate time-of-day and weather variants in the HTML5 demo: its scene list includes "Jungle Waterfall - Morning", "Jungle Waterfall - Rain" and "Jungle Waterfall - Night"; "Mirror Pond - Morning" and "Mirror Pond - Rain"; "Deep Forest - Day" and "Deep Forest - Rain"; "Seascape - Day" and "Seascape - Sunset"; "Mountain Stream - Morning" and "Mountain Stream - Night"; "Winter Forest - Snow"; "Water City Gates - Fog". (Read directly from the demo's scene list file.) — [Canvas Cycle demo, scenes.js](http://www.effectgames.com/demos/canvascycle/scenes.js); demo page: [Canvas Cycle](http://www.effectgames.com/demos/canvascycle/)
- A 2024 paper reports that Ferrari, using a fixed index map, made different times of day only by changing palette colours (secondary source, found through a search summary; I did not open the paper). — [SciTePress paper 124325](https://www.scitepress.org/Papers/2024/124325/124325.pdf)
- Ferrari's GDC 2016 talk "8 Bit & '8 Bitish' Graphics-Outside the Box" covers his colour cycling and palette shifting methods for background animation without frame animation (from the session description; I did not watch the talk). — [GDC Vault](https://gdcvault.com/play/1023586/8-Bit-8-Bitish-Graphics)
- The official site shows each of the twelve scenes as a tall image of 690x910 pixels (about 3:4), named by month. These are crops of the 640x480 landscape originals. I viewed all twelve. — images at `http://pixfabrik.com/livingworlds/img/jan.png` through `dec.png`, for example [nov.png](http://pixfabrik.com/livingworlds/img/nov.png), [jan.png](http://pixfabrik.com/livingworlds/img/jan.png), [oct.png](http://pixfabrik.com/livingworlds/img/oct.png)

Three of the twelve, looked at closely (viewed; all shares are my estimates):

- **November, the mirror pond** ([nov.png](http://pixfabrik.com/livingworlds/img/nov.png)). The closest match to "lake, forest, mountains".
  - Height split at the centre of the frame: clear sky about the top 10%; snowy mountains from about 10% to 40%; a band of dark pines overlapping the mountains from about 8% to 45% (the tallest trees at the edges reach the top of the frame); far bank and a lit grass mound from about 42% to 52%; water with a full mirror image of mountains and pines from about 50% to 88%; dark foreground grass across the bottom 12%, rising up both sides to about 60%.
  - So water takes roughly 35 to 40% of the height and sky only 10 to 15%. The reflection is what fills the tall frame: the mountain appears twice.
  - Depth: three value steps (near-black foreground grass, mid-dark pines, light warm mountains), a saturated blue sky repeated in the water, and foreground grass that makes a dark U-shaped frame around the water.
  - Ground plane: the water is seen from slightly above (you look down onto its surface), while trees and mountains are drawn in straight side elevation.
- **January, the winter forest** ([jan.png](http://pixfabrik.com/livingworlds/img/jan.png)).
  - Four or five foreground trunks run the full height of the frame, from 0% to 100%. Sky is only a small gap at the top centre (about the top 10%). Far mountains sit at about 8 to 22%, a distant town at about 22 to 30%, mid-distance snowy conifers from about 30% to 62%, and a snow path fills the bottom 38% or so.
  - Depth: overlap (trunks in front of everything), scale drop (huge trunks, tiny town), and colour shift from brown, detailed trunks to pale blue-violet distance. The path climbs up the frame towards the town, so distance is stacked vertically.
- **October, the autumn ruins** ([oct.png](http://pixfabrik.com/livingworlds/img/oct.png)).
  - Leaf canopy across the top 12% and trunks down both sides for the full height; pink-to-violet dusk sky from about 10% to 40%; ruined castle as a grey-violet silhouette from about 10% to 47%; grassy hill from about 45% to 68%; leaf-covered ground for the bottom 32%.
  - Time of day is carried by the sky gradient (pink low, violet high), by the castle being reduced to a flat cool silhouette, and by warm rim colour on the leaves.

Across all twelve (viewed as small thumbnails): March (island in a sea) is the only one that gives most of the frame, about 55%, to open sky and clouds; the rest fill the height with tall things (trunks, cliffs, a waterfall, a cave mouth) or with water. None has a human figure large enough to judge character scale.

#### Slynyrd (Raymond Schlitter) — tutorials with worked landscapes (viewed; square or 4:3, not vertical)

- His landscape tutorial scenes are not portrait: Pixelblog 62 uses a 192x144 canvas (4:3) and its exported animations are 1024x1024 files; the Pixelblog 11 and Pixelblog 10 tutorial plates are 768x768. (File sizes read from the downloaded files.) — [Pixelblog 62](https://www.slynyrd.com/blog/2026/5/27/pixelblog-62-landscape-backgrounds), [Pixelblog 11](https://www.slynyrd.com/blog/2018/11/16/pixelblog-11-landscape-pixeling), [Pixelblog 10](https://www.slynyrd.com/blog/2018/10/12/pixelblog-10-water-in-motion)
- Pixelblog 11's plate "Atmospheric perspective and vertical hierarchy" (viewed): a small framed landscape with a diagram at its side reading NEAR at the top, HORIZON / FARTHEST in the middle, NEAR at the bottom. The horizon sits about 65% of the way down the picture; clouds get smaller and flatter as they approach it from above, hills get paler and bluer as they approach it from below; one colour ramp runs from sky blue through pale haze to dark green. — [plate image](https://images.squarespace-cdn.com/content/v1/551a19f8e4b0e8322a93850a/1542954453861-I4T99DLMOBF6GK9RAOB3/22-Atmospheric_Perspective.gif)
- Pixelblog 10's water reflection plate (viewed): a single tree and its ground strip mirrored into water below, in one colour family, with the steps "Draw scene, reflect layer, add highlights, apply effect". The water takes roughly the lower 40% of that small scene. — [plate image](https://images.squarespace-cdn.com/content/v1/551a19f8e4b0e8322a93850a/1539557481600-WREP7J6ET4BJYCNNTHXF/20_Water_Reflection.gif)
- His technique statements are in Part B.

#### Waneella — vertical work exists, but it is urban (partly viewed)

- She sells still wallpaper packs. The July 2021 pack has two wallpapers: "Morning" at 2500x5000 pixels (a 1:2 vertical) and "Heat" at 5400x2700. Pack No.1 has 29 high-resolution wallpapers. — [Motionless Wallpaper Pack JUL'21](https://waneella.gumroad.com/l/WMWJUL21), [Motionless Wallpaper Pack No.1](https://waneella.gumroad.com/l/WMWPN1)
- Viewed: only the product cover images. The visible slice of "Morning" is a snowy back alley with brick walls, air-conditioner units, a bare tree trunk up the left edge and a patch of pale sky at the top right, in a muted grey-violet morning palette. The Pack No.1 cover is a mosaic of about thirty scenes, nearly all dense city views at night or dusk (lanterns, signs, lit windows); several tiles are tall and narrow. No lake, forest or cabin scenes are visible on either cover.
- What transfers: how a narrow frame is filled by stacking built structures and letting one tall element (trunk, pole, building edge) run up a side; night scenes lit by a few small warm light sources against a cool dark base.

#### Yuuta Toyoi / 1041uuu (interview read; artworks not viewed)

- Toyoi has posted animated pixel GIFs of everyday Japan as 1041uuu since 2011. — [Neocha, "Japan, Pixelated"](https://neocha.com/magazine/japan-pixelated/) (via search summary; page did not load for me)
- From his Pixivision interview: "Until now, I have been limiting my color palette to 32 colors"; tools are EDGE2 for pixels and Adobe Lightroom for colour adjustment; "You have to make loops almost unnoticeable"; he mixes cycles, "some looping at multiples of 3 and some looping at multiples of 4"; he spreads motion across the frame ("I try to sprinkle them over the whole canvas"); "By making the background move, you can express a feeling of time going by"; he often uses "a scrolling background, rain or petals". — [Pixivision interview](https://www.pixivision.net/en/a/2686)
- His Tumblr refused access (403), so I could not check formats or describe any piece.

#### Kirokaze (Gerardo Quiroz) — landscape format (dimensions checked)

- Independent pixel artist from Lima, Peru, known for animated loops inspired by science fiction. — [Inspiration Grid feature](https://theinspirationgrid.com/animated-pixel-art-creations-by-kirokaze)
- All 18 loops in that feature are landscape or square files (for example 960x540, 1280x720, 1536x648, one 540x540); none is portrait. (Dimensions read from the downloaded GIFs; I did not study their content.) — [Inspiration Grid feature](https://theinspirationgrid.com/animated-pixel-art-creations-by-kirokaze)

#### Gutty Kreum — landscape format, Japanese town scenes (viewed promotional images only)

- Canada-based pixel artist whose scenes are based on real Japanese locations found through Street View; one SuperRare piece is described as 30 colours on a 4000x2000 canvas (2:1 landscape). — [SuperRare editorial](https://superrare.com/editorial/7354)
- Sells "The Japan Collection: Backgrounds" asset pack. Viewed: the store's promo images show wide street-level views of houses, power lines and cars under very large cumulus clouds, each offered in day, sunset, dusk and night colourings of the same drawing. — [itch.io store page](https://guttykreum.itch.io/the-japan-collection-backgrounds)
- Relevance: a direct example of one drawing sold in several times of day, and of clouds taking half or more of the picture. Not a vertical reference.

#### Octavi Navarro (Pixels Huh) and Pixel Jeff (text only; not viewed)

- Navarro is a Barcelona illustrator behind Pixels Huh who also made backgrounds and animations for Thimbleweed Park; he mixes his own painting methods with pixel constraints and does not aim to recreate 8-bit or 16-bit art faithfully. — [Dribbble interview, 2016](https://dribbble.com/stories/2016/05/03/timeout-with-octavi-navarro), [Vice](https://www.vice.com/en/article/meet-the-artist-building-pixelated-sci-fi-landscapes/)
- Pixel Jeff is a Taipei pixel artist working since 2013 in illustration and motion, mixing retro, cyberpunk and lo-fi room scenes. — [RhinoShield artist page](https://shop.rhinoshield.co/design-studio/collections/pixeljeff)
- I found no vertical lake, forest or cabin piece by either and could not load their galleries.

#### Phone wallpaper packs by smaller artists (viewed)

- **biscdisc, "Pixel Art Phone Wallpaper Pack I"** — true phone-format pixel art (files are 720x1280 and 540x960). The most useful one is a view through an open window: wall and window frame make a border on all sides; inside the window, sky and layered cumulus fill roughly the top 55% of the whole image, the sea runs from about 60% to 78% with the horizon at about 60%, a sill with a cat and a potted plant sits at about 70 to 82%, and wall fills the rest. The lower part of the sky is paler than the top, and the sea darkens towards the viewer. A wind chime hangs from the top edge into the sky area. The other images in the pack are a single flower on a tall stem against clouds and character close-ups. — [itch.io page](https://biscdisc.itch.io/pixel-phone-wallpaper)
- **franrekk, "Big Small Worlds – Pixelart Mobile Wallpaper Pack #2"** — viewed only as a phone mock-up: a giant stone hand rising diagonally from bottom left to upper right carries a small village and windmill; flat saturated sky fills about the top 45%, cumulus sits behind the subject in the middle, and green fields fill about the bottom 20%. The top third is left almost empty, which is where the clock and widgets sit. — [Gumroad page](https://franrekk.gumroad.com/l/etdko)
- Checked and not useful: snurlsss's collection and mmeira-m's pack are small centred motifs on flat colour, not scenes; upmala's "winter wallpaper series" is photographs, not pixel art. — [snurlsss](https://snurlsss.itch.io/snurlys-wallpaper-collection), [mmeira-m](https://mmeira-m.itch.io/pixel-phone-wallpapers), [upmala](https://upmala.itch.io/winter-wallpaper-series)

### Inferences

- The Living Worlds tall crops suggest that a good 4:3 side-view landscape survives being cut to a tall frame when it already has (a) something tall at the sides, (b) water or a path in the lower third to half, and (c) a small bright far subject near the upper third. Scenes built as wide horizontal bands with open sky do not have these and would crop badly.
- In the mirror pond scene the reflection doubles the subject, so about 70% of the height is "mountains and trees" in some form while the sky stays small. This is the cheapest way I saw to fill a tall frame with a lake scene without inventing more content.
- Wallpaper artists leave the top third calm (flat sky or soft cloud) because the lock-screen clock sits there. A game has the same need for its meters, so the "quiet top band" habit transfers.
- None of the viewed vertical pieces contains a readable walking character, so they give no evidence on character scale. That has to come from games (the other researcher's scope) or from testing.
- The Canvas Cycle scene list shows Ferrari kept one drawing and offered morning, night, rain, snow and fog as variants. That is direct precedent for the project's "time of day and weather from palette changes over shared art" principle.

### Gaps

- **Not researched at all for lack of time:** APO+ (apo), Faxdoc, Motocross Saito, Mrmo Tarius, Jubilee, Aleha_84, Franek Nowotniak, Paul Robertson, Brandon James Greer's artworks, Kenze Wee and Pixel Dailies, Deceiver, Ivan Dixon, Stefanie Grunwald, Thomas Feichtmeir (Cyangmou), eBoy, Nelson Wang, r/PixelArt top posts, pixel-art Apple Watch faces. I have no sourced findings on any of them.
- **Unverified recollection, not checked in this session, treat as leads only:** Aleha_84 is known for tall, densely stacked city scenes; Jubilee and Mrmo Tarius for large painterly nature landscapes; eBoy for isometric cityscapes and Paul Robertson for dense character animation (both contrasts, not models); Waneella also publishes animated loops, not only stills.
- I could not confirm whether the Living Worlds app in portrait on a phone shows these same 3:4 crops, lets the user pan, or letterboxes. Ian Gilman's article on the project (linked from the site) returned 403: [Medium article](https://medium.com/@iangilman/living-worlds-for-ios-android-46b4a4e9b048).
- How many palettes each Living Worlds scene has and how they are blended through the day: not found in any page I could open. The original Q&A with Ferrari on Effect Games did not load.
- Lospec's gallery front page listed pond-themed entries (for example [shadrach/chill-pond](https://lospec.com/gallery/shadrach/chill-pond), [harrypujols/on-golden-pond](https://lospec.com/gallery/harrypujols/on-golden-pond)), but I could not load the full images or their dimensions, so none is described.
- I did not find a single vertical pixel-art piece that shows exactly the target subject (side-view lake, cabin, forest, small figure). The closest viewed is the mirror pond, which has no cabin or figure.

## Part B — Technique: what do good sources say about building such a scene?

### Takeaway

The written sources agree on the depth recipe (the near layer is the most saturated and contrasty; each layer back gets paler, less saturated and closer to the sky colour; distance is also shown by height in the frame) and offer three workable day/night methods (palette substitution, a set of colour lookup tables, or a whole-canvas tint plus additive lights). Almost nothing is written specifically about portrait pixel art on phones: the engine documentation treats "pixel art" and "portrait mobile" as separate cases, and Sword & Sworcery, often cited as a portrait pixel game, actually explores in landscape and uses portrait only for combat and its book.

### Cited Findings

#### Logical resolution, integer scaling and phone aspect ratios

- Godot's documentation, pixel-art case: "Most pixel art games use viewport sizes between 256×224 and 640×480"; set stretch mode to `viewport` and scale mode to `integer`, which "prevents uneven pixel scaling from occurring, which makes pixel art not display as intended." — [Godot docs: Multiple resolutions](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html)
- Godot's documentation, portrait mobile case (not pixel-art specific): base size 720 wide by 1280 high, stretch aspect `expand`, which "allows for supporting multiple aspect ratios and makes better use of tall smartphone displays." The page says nothing about notches or safe areas. — [Godot docs: Multiple resolutions](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html)
- A Godot forum user building exactly this noted the gap: "The documentation has a section on pixel art and a section on mobile, but not for pixel art on mobile", and could not find how to avoid fractional scaling without black bars. The thread has no answer beyond a link to the docs. — [Godot forum thread](https://forum.godotengine.org/t/what-are-the-right-resolution-aspect-mode-and-scaling-for-pixel-art-games-for-mobile/94804)
- Flame (the project's chosen engine): `CameraComponent.withFixedResolution` "will let you pretend that the user's device has a fixed resolution of your choice", but "will underutilize the user's available screen space, unless their device happens to have the same aspect ratio as your chosen dimensions"; `FixedResolutionViewport` adds "black bars on the sides if it doesn't match the aspect ratio". The default `MaxViewport` "expands to the maximum size allowed by the game". The camera exposes `visibleWorldRect`, the world region currently visible, and a `backdrop` component "statically rendered below the world". The page gives no guidance on integer scaling or pixel-perfect rendering. — [Flame docs: Camera & World](https://docs.flame-engine.org/main/flame/camera.html)
- Construct's guidance (via search summary, page not opened): pick an aspect ratio and scale to fit instead of targeting one resolution; integer letterbox scaling keeps pixels exact but can leave bars on all sides. — [Construct: Supporting multiple screen sizes](https://www.construct.net/en/tutorials/supporting-multiple-screen-17)
- Slynyrd on export: scale pixel art "only in multiples of 100%" with nearest neighbour. — [Pixelblog 23](https://www.slynyrd.com/blog/2019/11/12/pixelblog-23-parallax-scrolling)
- Sword & Sworcery's environments were authored as fixed-size paintings: "All of the environments are basically just paintings, 512×512 or 1024×512", with "a zillion entities – shrubs, tree trunks, objects, particles, twinkles, sky, clouds" layered on top; Craig Adams credits the "hard-edged, resolution-independent pixels" for making iPad support easy. — [CDM interview with Craig Adams](https://cdm.link/inside-handheld-game-art-the-art-style-and-making-of-swords-sworcery-superbrothers-pixel-cinema/)

#### Composing in a vertical frame; Sword & Sworcery's use of portrait

- Sword & Sworcery is explored in landscape; portrait is a mode switch. Rotating to portrait draws the sword for combat and, on iPad, opens the Megatome book. An early hands-on: you turn the iPhone "as the game switches to a vertical view" to unsheathe the sword. — [Engadget GDC 2010 hands-on](https://www.engadget.com/2010/03/15/gdc-2010-hands-on-with-superbrothers-sword-and-sorcery/), [TouchArcade iPad review](https://toucharcade.com/2011/03/23/superbrothers-sword-sworcery-ep-for-ipad-review/), [Wikipedia](https://en.wikipedia.org/wiki/Superbrothers:_Sword_%26_Sworcery_EP)
- I found no statement by Craig Adams or Capy about composing the portrait view. In the CDM interview he does not discuss orientation, lighting or parallax at all. — [CDM interview](https://cdm.link/inside-handheld-game-art-the-art-style-and-making-of-swords-sworcery-superbrothers-pixel-cinema/)
- Vertical position as a depth cue: "The vertical position of an object on the canvas also informs the depth. The closer an object is to the vertical position of the horizon, the more distant it appears." — [Slynyrd, Pixelblog 11](https://www.slynyrd.com/blog/2018/11/16/pixelblog-11-landscape-pixeling)
- Building a landscape in bands: start with "solid horizontal bars of color to define the horizon line", split sky and ground into bands, then add mountain layers, a haze band, grass detail and cloud layers. In a forest the viewing distance is shorter, layer-to-layer changes are smaller, and foliage reaches the top of the canvas. He also leaves the bottom of the frame open for character sprites. — [Slynyrd, Pixelblog 62](https://www.slynyrd.com/blog/2026/5/27/pixelblog-62-landscape-backgrounds)
- Kingdom keeps water in a fixed band: its river is described as always filling the bottom third of the screen (from a search summary of the Retronator article; the article itself returned 403, so the wording is unverified). — [Retronator Magazine, "The fall and rise of Kingdom"](https://medium.com/retronator-magazine/the-fall-and-rise-of-kingdom-f6a3da699f0d)

#### Atmospheric perspective and palette ramps per depth layer

- "The further the object, the more it takes on the color of atmospheric haze. In a day time setting, close objects are more saturated with clear contrast between light and shadow, while far objects become less saturated and contain less colors." — [Slynyrd, Pixelblog 11](https://www.slynyrd.com/blog/2018/11/16/pixelblog-11-landscape-pixeling)
- "As it goes, the closest plane is the most saturated with strongest contrast between light and shadow." With each plane back, saturation falls, lightness rises, and hue moves towards the sky colour; the illusion of depth comes "primarily" from colour choice. — [Slynyrd, Pixelblog 62](https://www.slynyrd.com/blog/2026/5/27/pixelblog-62-landscape-backgrounds)
- Detail scales with distance: nearest grass shows thick blades, far planes use one- or two-pixel clusters. Colours are reused across layers (the far mountain shadow reuses a sky colour), keeping each whole scene to 15 colours. — [Slynyrd, Pixelblog 62](https://www.slynyrd.com/blog/2026/5/27/pixelblog-62-landscape-backgrounds)
- The hue path differs by biome: in his valley the near grass is warmest and each plane shifts towards blue; in his forest near greens with a blue tint shift to warm yellow in the distance. — [Slynyrd, Pixelblog 62](https://www.slynyrd.com/blog/2026/5/27/pixelblog-62-landscape-backgrounds)
- Clouds follow the same rule: the nearest clouds have the most contrast and detail; the farthest are "baked into the sky background". — [Slynyrd, Pixelblog 62](https://www.slynyrd.com/blog/2026/5/27/pixelblog-62-landscape-backgrounds)
- Hue shifting within a ramp (shadows cooler, lights warmer, not just darker and lighter) is the standard advice; ramps that change only brightness are called a beginner mistake. — [GameDev.net, "Color Palettes"](https://gamedev.net/tutorials/visual-arts/color-palettes-r4964) (via search summary)
- Toyoi on edges and depth: "I didn't use anti-aliasing and I took advantage of the jaggies effect in order to create a sense of depth", while lights are drawn "carefully with anti-aliasing to give them a shape". — [Pixivision interview](https://www.pixivision.net/en/a/2686)

#### Parallax, including scenes that barely scroll

- Parallax "may not be convincing if your scene doesn't already convey depth"; it suits "layered scenes that exhibit atmospheric perspective, such as landscape scenery". — [Slynyrd, Pixelblog 23](https://www.slynyrd.com/blog/2019/11/12/pixelblog-23-parallax-scrolling)
- Movement must be in whole art pixels ("you can't move a half pixel") and at a constant rate; "I try to avoid slower than 1 pixel per frame, as the motion can look a bit jittery." Start the farthest layer at the slowest clean rate and step each nearer layer up. — [Slynyrd, Pixelblog 23](https://www.slynyrd.com/blog/2019/11/12/pixelblog-23-parallax-scrolling)
- Pick a canvas width with many divisors so layer speeds divide evenly: 96 "can divide by 1,2,3,4,6,8,12,16,24,32,48", and "192px works nicely" for pixel-perfect parallax. — [Pixelblog 23](https://www.slynyrd.com/blog/2019/11/12/pixelblog-23-parallax-scrolling), [Pixelblog 62](https://www.slynyrd.com/blog/2026/5/27/pixelblog-62-landscape-backgrounds)
- Layers without a dominant focal point hide the repeat; clouds and stars are the recommended first parallax subjects. — [Slynyrd, Pixelblog 23](https://www.slynyrd.com/blog/2019/11/12/pixelblog-23-parallax-scrolling)
- Flame supports a static parallax component in the camera backdrop, behind a moving world. — [Flame docs: Camera & World](https://docs.flame-engine.org/main/flame/camera.html)

#### Day and night: palette substitution, lookup tables, tint plus lights, colour cycling

- Colour cycling: on 8-bit systems changing the palette changed the whole screen at once, cheaply; it was used for water, fire and weather. Huckaby's "BlendShift" variant fades colours into each other as they shift for smoother motion at the same speed. Ferrari used it for rain, snow, waves and waterfalls. — [Huckaby, Effect Games](http://www.effectgames.com/effect/article-Old_School_Color_Cycling_with_HTML5.html)
- Whole-palette substitution: a Game Boy Advance devlog reproduces Pokémon Gold/Silver day and night by swapping only the tile palette. — [Green Memories devlog](https://tengukaze.itch.io/green-memories-gba/devlog/416470/daynight-cycle-like-pokemon-goldsilver) (via search summary)
- Lookup tables (Graveyard Keeper): the artist "created 10 different LUTs for different time of day", each made by applying colour layers over the neutral table; ambient light is darker at night with its colour set by a gradient; "By nightfall a light source not only becomes darker but gets blue tint." The article does not say how the tables are blended between times. — [Game Developer: "Graveyard Keeper: How the graphics effects are made"](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made)
- Tint plus lights (Usagi Shima, a real-time-clock cozy game in Godot): three parts, a whole-canvas tint, a clock, and lights on every lantern and window. Base tints for sunrise, day, sunset and night are interpolated every minute; example sunset tint `Color(0.99, 0.85, 0.75)` moving to night `Color(0.39, 0.51, 0.64)` between 5 PM and 7 PM. Light energy is interpolated too (0 by day, 0.5 at sunset, 1.0 at night) and light textures use additive blending so they glow through the tint. — [Usagi Shima devlog 2](https://usagishima.net/2021/04/13/devlog-2-real-time-day-night-cycle/)
- Gradient maps: tools exist that recolour an image through a gradient chosen by a value mask, used for day/night. — [GradientMapFX](https://nulltale.itch.io/gradientmapfx) (via search summary)
- Mood by sky: "Lighting totally changes the mood of a scene. Bright blue skies gives both an energetic and relaxing feeling. The warm hues of dawn create a contemplative mood, while a fiery sunset can speak of romance." — [Slynyrd, Pixelblog 11](https://www.slynyrd.com/blog/2018/11/16/pixelblog-11-landscape-pixeling)
- Non-pixel reference: Alto's Adventure advertises "fully dynamic lighting and weather effects, including thunderstorms, blizzards, fog, rainbows, shooting stars", and its day cycle carries over between runs. I did not find its makers' technical write-up. — [App Store listing](https://apps.apple.com/app/950812012), [Wikipedia](https://en.wikipedia.com/wiki/Alto%27s_Adventure)

#### Weather: particles, fog, wind

- Living Worlds treats weather as part of the picture's day: "storms pass through", with rain, snow and fog variants of the same scenes in the HTML5 demo. — [Pixfabrik](http://pixfabrik.com/livingworlds/), [Canvas Cycle scenes.js](http://www.effectgames.com/demos/canvascycle/scenes.js)
- Fog in Graveyard Keeper is many horizontal cloud sprites; "the upper part of all the sprites is covered with a fewer amount of fog sprites", so roofs and treetops stay clear. — [Game Developer](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made)
- Wind in Graveyard Keeper is a vertex shader instead of hand animation: sideways shift grows with height ("The highest point will be shaken the most intensely"), phase varies by position, and on trees only some leaves move. — [Game Developer](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made)
- Toyoi uses rain or falling petals as the moving element over a still picture, with loops of different lengths so the repeat is hard to notice. — [Pixivision interview](https://www.pixivision.net/en/a/2686)
- In the desert scene Slynyrd puts a swirled texture into the sky gradient itself to strengthen haze. — [Pixelblog 62](https://www.slynyrd.com/blog/2026/5/27/pixelblog-62-landscape-backgrounds)

#### Water and reflections

- "A reflective water surface adds lovely atmosphere to a scene and is surprisingly easy to execute": flip the scene, add highlights, then add ripple distortion; "If your scene looks bad without animation, it won't look any better with it." His sparkling surface is a 6-frame loop, and highlights are placed to echo the cloud shapes above. — [Slynyrd, Pixelblog 10](https://www.slynyrd.com/blog/2018/10/12/pixelblog-10-water-in-motion)
- Thomas van den Berg (Kingdom's creator), about a later 3D pixel project, not Kingdom: the water is "a few effects" with "a camera that renders the scene from below to generate the reflections". — [80.lv interview](https://80.lv/articles/kingdom-developer-on-creating-pixel-environments/)
- Ready-made Kingdom-style reflective water shaders exist for Godot; a forum description of Kingdom's look mentions a second distortion texture scrolling at a different speed for a rolling effect (third-party observation, not the developer's account). — [Godot Shaders: 2D water with reflections](https://godotshaders.com/shader/2d-water-with-reflections/), [Defold forum thread](https://forum.defold.com/t/water-reflections/75802)
- A step-by-step shader write-up for pixel-art water surfaces exists (not opened). — [Marcin Klimek, "Water surface shader for 2D Pixel art games"](https://marcinklimek.github.io/posts/2024-02-26-water-surface-shader-for-2d-pixel-art-games)

#### A ground strip seen slightly from above in a side-view scene

- I found no written source that explains this convention for Kingdom, Eastward, Children of Morta or Sword & Sworcery.
- The nearest evidence is visual: Ferrari's mirror pond and winter path scenes show water and ground from slightly above while trees and mountains stay in side elevation (viewed; see Part A). — [nov.png](http://pixfabrik.com/livingworlds/img/nov.png), [jan.png](http://pixfabrik.com/livingworlds/img/jan.png)
- Slynyrd's "vertical hierarchy" (higher on the canvas, up to the horizon, means farther) is the stated principle behind it. — [Pixelblog 11](https://www.slynyrd.com/blog/2018/11/16/pixelblog-11-landscape-pixeling)

### Inferences

- **Integer scaling across phone shapes (my arithmetic, not from a source).** Fixing the logical size forces bars on some phones (Flame and Construct both say so). The alternative is to fix the integer scale factor and let the visible world area vary. With a logical width of 180 art pixels at 6x on a 1080-pixel-wide screen, the visible height runs from 320 rows on a 9:16 screen to 420 rows on a 9:21 screen. So the scene needs about 100 rows of "optional" content (extra sky above, extra water or foreground below) around a 180x320 core that always shows. Screens whose width is not a multiple of the logical width need either a slightly wider visible strip or thin side bars; this has to be decided per device family and I did not source device pixel widths.
- In Flame this points to the default `MaxViewport`, an integer `viewfinder` zoom computed from the screen width, and `visibleWorldRect` to know what is on screen, instead of `withFixedResolution`. This is an inference from the documentation's descriptions and should be tested in a spike.
- Because the tallest phones add rows, sky and water are the right bands to stretch: they can grow without new drawing (a sky gradient, a longer reflection). The band that holds the character, cabin and shoreline should be anchored to a fixed distance from the bottom safe area.
- A scene that barely scrolls should not rely on parallax for depth. Slynyrd's points (parallax only helps a scene that already reads as deep; sub-pixel speeds look jittery) suggest depth should come from value and saturation steps and overlap, with motion from independent drifting clouds, particles and water. If the camera follows the character over a wide map, layer offsets should be rounded to whole art pixels.
- The three day/night methods map onto the project's layer principle differently. Indexed palette substitution (Ferrari) gives the most control and the best-looking results but requires all art to be authored as indexed colour. A stack of lookup tables (Graveyard Keeper) works on any art and is one texture per time of day. A whole-canvas tint plus additive lights (Usagi Shima) is the cheapest and already fits a real-time clock, but tints everything equally unless the sky is a separate layer. A sensible combination: separate sky gradient per time of day, lookup table or tint for the world layers, additive lights for the cabin window and lantern.
- Reflection is cheapest as "flip, darken, add highlights, ripple", and the flip automatically inherits whatever time-of-day colouring the upper scene has, which keeps water consistent with the sky at no extra art cost.
- Toyoi's "different loop lengths" rule applies directly to ambient idles (smoke, water sparkle, leaves, dog tail): unequal periods stop the whole scene from visibly repeating.

### Gaps

- **Talks not watched:** Mark Ferrari's GDC 2016 talk ([GDC Vault](https://gdcvault.com/play/1023586/8-Bit-8-Bitish-Graphics); a YouTube upload is reported at [this address](https://www.youtube.com/watch?v=aMcJ1Jvtef0)), and any GDC talks on Kingdom, Hyper Light Drifter, Eastward, Owlboy or The Last Night. I searched for none of the last four.
- **Video tutorials not checked:** AdamCYounis (a video on choosing resolution is referenced by others but I did not find or watch it), Brandon James Greer, MortMort, Pixel Pete.
- **Written tutorials not opened:** Saint11 (Pedro Medeiros; his articles are reported to live at saint11.org/pixel_articles/, unverified), Derek Yu's pixel-art tutorial (a 2019 blog post says he rebooted it: [GBGames](https://gbgames.com/2019/12/19/derek-yus-updated-pixel-art-tutorial)), Lospec tutorials.
- **Kingdom's own water, lighting and parallax method:** the developer's TIGSource devlog (topic 40539) returned 403 and the Retronator article returned 403. The "bottom third" figure is from a search summary only.
- **Safe areas and notches for pixel art:** no source found. The Godot and Flame pages I read do not mention them.
- **Character size relative to the frame for mobile pixel art:** no source found.
- **How Graveyard Keeper blends between its 10 lookup tables:** not stated in the article.
- **Alto's Adventure lighting method:** the makers' write-up was not found.
- **Sword & Sworcery portrait composition:** no creator statement found; the premise that it was designed for portrait and landscape equally appears to be wrong (portrait is the combat and book mode).

## Part C — Summary: what works in portrait, what wastes the frame, and what to study first

### Takeaway

In the vertical pieces I could view, the tall frame is filled by doubling the subject in water, by tall foreground elements running the full height at the sides, and by stacking distance up the frame, with sky kept to a modest calm band; open-sky-over-thin-ground compositions and straight crops of wide scenes are what waste it. Mark Ferrari's Living Worlds and Slynyrd's Pixelblog are the two sources most worth studying first, one for finished examples with time of day and weather, the other for the written method.

### Cited Findings

Approaches that work in portrait (each tied to a viewed example or a quoted source):

- **Reflective water as the lower third to half.** The mirror pond gives about 35 to 40% of the height to water that repeats the mountains and trees (my estimate). — [nov.png](http://pixfabrik.com/livingworlds/img/nov.png); method in [Pixelblog 10](https://www.slynyrd.com/blog/2018/10/12/pixelblog-10-water-in-motion)
- **Full-height foreground elements at the sides.** Trunks in the winter forest and autumn ruins run from top to bottom edge and make a dark frame around a small bright far subject. — [jan.png](http://pixfabrik.com/livingworlds/img/jan.png), [oct.png](http://pixfabrik.com/livingworlds/img/oct.png)
- **Distance stacked vertically.** A path or water surface seen slightly from above climbs the frame; objects nearer the horizon line read as farther. — [jan.png](http://pixfabrik.com/livingworlds/img/jan.png); principle in [Pixelblog 11](https://www.slynyrd.com/blog/2018/11/16/pixelblog-11-landscape-pixeling)
- **A frame within the frame.** The window wallpaper borders the view on all four sides and hangs an object from the top edge into the sky. — [biscdisc pack](https://biscdisc.itch.io/pixel-phone-wallpaper)
- **Depth by colour steps, not by motion.** Near layer most saturated and contrasty; each layer back paler, less saturated, closer to sky colour, with less detail. — [Pixelblog 62](https://www.slynyrd.com/blog/2026/5/27/pixelblog-62-landscape-backgrounds)
- **A calm upper band.** Phone wallpaper artists leave the top third as flat sky or soft cloud. — [franrekk pack](https://franrekk.gumroad.com/l/etdko), [biscdisc pack](https://biscdisc.itch.io/pixel-phone-wallpaper)
- **Forest as a "short view".** When foliage reaches the top of the canvas the scene needs fewer depth layers and smaller changes between them. — [Pixelblog 62](https://www.slynyrd.com/blog/2026/5/27/pixelblog-62-landscape-backgrounds)
- **One drawing, many times of day and weathers.** — [Canvas Cycle scene list](http://www.effectgames.com/demos/canvascycle/scenes.js), [Gutty Kreum backgrounds](https://guttykreum.itch.io/the-japan-collection-backgrounds)

Approaches that waste the tall frame (cited where a source supports it; the rest are in Inferences):

- **Fixed-resolution letterboxing.** A fixed logical size "will underutilize the user's available screen space" on any phone with a different shape. — [Flame docs](https://docs.flame-engine.org/main/flame/camera.html)
- **Relying on parallax for depth.** It "may not be convincing if your scene doesn't already convey depth", and slow sub-pixel drift looks jittery. — [Pixelblog 23](https://www.slynyrd.com/blog/2019/11/12/pixelblog-23-parallax-scrolling)
- **Using landscape-format artists as layout models.** Every Kirokaze loop sampled and the Gutty Kreum and Slynyrd scenes are wide or square. — [Inspiration Grid](https://theinspirationgrid.com/animated-pixel-art-creations-by-kirokaze), [SuperRare](https://superrare.com/editorial/7354), [Pixelblog 62](https://www.slynyrd.com/blog/2026/5/27/pixelblog-62-landscape-backgrounds)

Ranked list of what to study, with one line each:

1. **Mark Ferrari, Living Worlds (app and the twelve tall images on the site)** — the only viewed set that combines tall crops, water, forest, real-time day cycle and passing weather over one drawing. — [Pixfabrik](http://pixfabrik.com/livingworlds/)
2. **Slynyrd, Pixelblog 62, 11, 10 and 23** — the clearest written recipe for layer order, per-layer colour, reflections and pixel-exact parallax, with step images. — [62](https://www.slynyrd.com/blog/2026/5/27/pixelblog-62-landscape-backgrounds), [11](https://www.slynyrd.com/blog/2018/11/16/pixelblog-11-landscape-pixeling), [10](https://www.slynyrd.com/blog/2018/10/12/pixelblog-10-water-in-motion), [23](https://www.slynyrd.com/blog/2019/11/12/pixelblog-23-parallax-scrolling)
3. **Canvas Cycle demo and Huckaby's article** — lets you switch the same scene between morning, night, rain and snow in a browser and explains colour cycling. — [demo](http://www.effectgames.com/demos/canvascycle/), [article](http://www.effectgames.com/effect/article-Old_School_Color_Cycling_with_HTML5.html)
4. **Usagi Shima devlog 2** — a small, concrete real-clock day cycle (tint plus additive lights) for a cozy game, with actual colour values. — [devlog](https://usagishima.net/2021/04/13/devlog-2-real-time-day-night-cycle/)
5. **Graveyard Keeper graphics article** — lookup tables per time of day, layered fog that leaves treetops clear, and shader wind, all applicable to independent layers. — [Game Developer](https://www.gamedeveloper.com/programming/graveyard-keeper-how-the-graphics-effects-are-made)
6. **Yuuta Toyoi's Pixivision interview** — rules for calm ambient loops: few moving things, spread across the frame, unequal loop lengths, small palette. — [Pixivision](https://www.pixivision.net/en/a/2686)
7. **Flame camera docs and Godot multiple-resolutions docs** — the constraints behind the logical-resolution decision; neither solves portrait pixel art outright. — [Flame](https://docs.flame-engine.org/main/flame/camera.html), [Godot](https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html)
8. **Waneella's vertical wallpapers** — how to fill a 1:2 frame and light a night scene with a few warm sources; subject matter is urban. — [JUL'21 pack](https://waneella.gumroad.com/l/WMWJUL21), [Pack No.1](https://waneella.gumroad.com/l/WMWPN1)
9. **biscdisc's window wallpaper** — a compact example of the frame-within-a-frame device at true phone proportions. — [itch.io](https://biscdisc.itch.io/pixel-phone-wallpaper)
10. **Gutty Kreum's background pack** — one drawing recoloured for day, sunset, dusk and night, with skies that carry the mood; landscape format. — [itch.io](https://guttykreum.itch.io/the-japan-collection-backgrounds)
11. **Mark Ferrari's GDC 2016 talk** — likely the best account of palette shifting from its originator, but I did not watch it, so its rank is provisional. — [GDC Vault](https://gdcvault.com/play/1023586/8-Bit-8-Bitish-Graphics)
12. **Sword & Sworcery (Craig Adams interview)** — useful for "painted background plus many small layered entities" and hard-edged big pixels; not a portrait composition reference. — [CDM](https://cdm.link/inside-handheld-game-art-the-art-style-and-making-of-swords-sworcery-superbrothers-pixel-cinema/)

### Inferences

- A portrait layout that follows the viewed evidence, top to bottom: a calm sky band that can grow on taller phones (roughly 15 to 25%); far hills or mountains and a mid tree line (roughly 20 to 25%); the shoreline strip with cabin, character and dog (roughly 15 to 20%); water with the reflection of everything above (roughly 25 to 35%); a dark foreground fringe of grass, reeds or a branch at the bottom and up one side (roughly 5 to 10%). These shares are my proposal, extrapolated mainly from the mirror pond; they are not taken from any single source.
- Things I expect to waste the frame, by reasoning from the above and not from a source: a horizon near the middle with empty sky above and a thin ground strip below; a pure flat side elevation with no reflection and no foreground, which leaves two thirds of the screen as backdrop; cropping a finished wide scene without tall side elements; a large empty sky kept only to make room for interface.
- For this project the shoreline strip is the natural place for the "seen slightly from above" ground: it gives the character and dog depth to walk in and out of, and the water below it can stay a flat mirrored plane.
- The world-state rule in the project (no style specifics in state) fits all three day/night methods, since each takes "time of day" and "weather" as inputs to the drawing layer only.

### Gaps

- The ranking is limited to what I could open. Artists listed as not researched in Part A (notably Aleha_84, Jubilee, Mrmo Tarius, Faxdoc, APO+, Motocross Saito) might outrank several entries once checked.
- No viewed example contains a small character in a tall lake scene, so the proposed band shares are untested for character readability and tap targets.
- No source was found for night readability on phone screens (how dark a night palette can go outdoors or at low brightness).
- Everything about video sources (GDC talks, YouTube tutorials) is unverified; none was watched.
