#!/usr/bin/env python3
"""Placeholder art for the second pass of the Flame spike, as indexed images plus one palette image.

Run from the spike folder: python3 tools/make_art.py

Every art pixel stores a palette index, not a colour:
  red   = index * 4
  green = 255 where firelight may reach the pixel, else 0
The shader looks the index up in assets/images/palette.png, which is 64 entries wide and has one row
per time of day (night, dawn, day, dusk) plus one row of firelit colours.
"""
import math
import random
from PIL import Image, ImageDraw

W, H = 660, 280  # five screens of 120 of land and dock, then half a screen of open water
S = 2  # art pixels per world unit: the art is drawn twice as fine as the world's units (W, H, BANK are units)
SKY_W = 240  # in art pixels. The sky does not scroll, so it only has to cover the widest view
BANK, WATER = 196, 208  # top of the bank the character stands on; waterline
random.seed(11)

# name -> day colour. Order fixes the index (1-based; 0 is unused).
DAY = {
    "sky1": (86, 150, 214), "sky2": (112, 172, 224), "sky3": (146, 196, 232), "sky4": (182, 216, 236),
    "sky5": (214, 232, 236), "star": (250, 252, 255), "sun": (255, 246, 206),
    "halo1": (196, 224, 238), "halo2": (228, 238, 230),
    "cloud": (244, 246, 240), "cloud_shade": (204, 216, 228),
    "hill_far": (136, 168, 178), "hill_near": (104, 144, 140),
    "tree": (44, 92, 78), "tree_light": (78, 128, 86), "tree_gold": (196, 150, 64), "trunk": (84, 62, 52),
    "bank_top": (136, 176, 98), "bank": (98, 140, 82), "bank_face": (92, 78, 66), "tuft": (160, 196, 110),
    "wall": (138, 96, 68), "wall_shade": (108, 74, 56), "roof": (88, 70, 92), "door": (84, 56, 44),
    "window": (236, 214, 150),
    "skin": (238, 200, 164), "hat": (70, 84, 120), "coat": (198, 96, 70), "legs": (58, 62, 92),
    "scarf": (240, 196, 84),
    "dog": (232, 226, 210), "dog_shade": (176, 150, 120),
    "log": (74, 50, 34), "flame": (255, 138, 42), "core": (255, 226, 122),
    # Added for the third pass. New entries go at the end: the game code refers to some by number.
    "tarp": (132, 146, 160), "tarp_shade": (100, 112, 132), "rope": (206, 186, 146),
    "petal": (238, 128, 150), "petal_light": (252, 238, 204), "ash": (112, 106, 108),
    "moon": (226, 234, 244), "moon_shade": (196, 210, 230),
    "moon_dark": (126, 174, 220),  # the unlit part: a step away from the sky, so the whole disc can be made out
    "star_dim": (170, 204, 236),  # stars are drawn by the game, which decides when each one is out
    # Added for the finer art (two art pixels per unit): shades and lights for detail.
    "tree_dark": (30, 68, 66), "hill_snow": (228, 236, 240), "hill_shade": (116, 150, 168),
    "bank_dark": (76, 114, 74), "roof_light": (116, 94, 116), "wall_light": (166, 122, 86), "coat_shade": (158, 72, 60),
}
NAMES = list(DAY)
INDEX = {n: i + 1 for i, n in enumerate(NAMES)}
WATER_TINT, WATER_HI = 62, 63  # fixed indices the shader knows


def ramp(stops, c):
    """Map a colour's brightness onto a three-colour ramp."""
    lum = (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) / 255
    a, b, t = (stops[0], stops[1], lum * 2) if lum < 0.5 else (stops[1], stops[2], lum * 2 - 1)
    return tuple(a[i] + (b[i] - a[i]) * t for i in range(3))


def recolour(stops, keep):
    """A whole-scene re-colouring: mostly the ramp, with a little of the day hue kept."""
    return lambda c: tuple(round(r * (1 - keep) + c[i] * keep) for i, r in enumerate(ramp(stops, c)))


night = recolour([(8, 12, 36), (34, 52, 104), (120, 150, 205)], 0.12)
dawn = recolour([(58, 52, 104), (176, 128, 170), (255, 226, 206)], 0.35)
dusk = recolour([(44, 28, 76), (150, 78, 124), (255, 196, 170)], 0.28)


def lit(c):
    return tuple(min(255, round(c[i] * m + a)) for i, (m, a) in enumerate([(1.2, 26), (0.95, 10), (0.62, 0)]))


# Hand-picked entries that the ramps must not flatten: skies, sun and moon, and everything that glows.
OVERRIDE = {
    "night": {
        "sky1": (10, 14, 40), "sky2": (14, 20, 52), "sky3": (20, 28, 66), "sky4": (28, 38, 82), "sky5": (38, 50, 98),
        "star": (236, 240, 255), "sun": (236, 240, 255), "halo1": (30, 42, 88), "halo2": (52, 68, 120),
        "window": (255, 214, 120), "cloud": (44, 58, 108), "cloud_shade": (32, 44, 90),
        "sun": (255, 236, 190), "moon": (236, 240, 255), "moon_shade": (190, 202, 236), "moon_dark": (36, 46, 86), "star_dim": (112, 132, 196),
    },
    "dawn": {
        "sky1": (96, 104, 168), "sky2": (150, 130, 186), "sky3": (214, 160, 188), "sky4": (246, 196, 184),
        "sky5": (252, 226, 190), "star": (255, 240, 232), "sun": (255, 236, 190), "halo1": (250, 208, 190),
        "halo2": (254, 226, 196), "window": (255, 214, 120),
        "moon": (236, 226, 236), "moon_shade": (214, 196, 222), "moon_dark": (164, 146, 192), "star_dim": (178, 158, 204),
    },
    "day": {},
    "dusk": {
        "sky1": (72, 52, 120), "sky2": (128, 70, 136), "sky3": (196, 96, 132), "sky4": (240, 138, 116),
        "sky5": (252, 186, 128), "star": (255, 232, 222), "sun": (255, 214, 140), "halo1": (250, 160, 120),
        "halo2": (254, 190, 130), "window": (255, 214, 120),
        "moon": (244, 222, 226), "moon_shade": (216, 180, 204), "moon_dark": (118, 76, 134), "star_dim": (158, 112, 170),
    },
    "lit": {"window": (255, 214, 120)},
}
ROWS = [("night", night), ("dawn", dawn), ("day", lambda c: c), ("dusk", dusk), ("lit", lit)]
WATER_ROWS = {  # tint, highlight
    "night": ((10, 18, 50), (110, 140, 200)), "dawn": ((120, 110, 170), (255, 230, 220)),
    "day": ((70, 120, 160), (220, 236, 244)), "dusk": ((96, 60, 120), (255, 200, 170)),
    "lit": ((70, 120, 160), (220, 236, 244)),
}

palette = Image.new("RGB", (64, len(ROWS)))
for y, (row, fn) in enumerate(ROWS):
    for name in NAMES:
        c = OVERRIDE[row].get(name) or (DAY[name] if name in ("flame", "core") else fn(DAY[name]))
        palette.putpixel((INDEX[name], y), c)
    palette.putpixel((WATER_TINT, y), WATER_ROWS[row][0])
    palette.putpixel((WATER_HI, y), WATER_ROWS[row][1])
palette.save("assets/images/palette.png")


def c(name, light=True):
    return (INDEX[name] * 4, 255 if light else 0, 0, 255)


def far(name):
    return c(name, light=False)


def scale2x(img):
    """Twice the size with the Scale2x rule: flat areas stay flat, diagonal edges get the finer step."""
    w, h = img.size
    src, out = img.load(), Image.new("RGBA", (w * 2, h * 2))
    o = out.load()
    for y in range(h):
        for x in range(w):
            p = src[x, y]
            a, b = src[x, max(0, y - 1)], src[min(w - 1, x + 1), y]
            cc, dd = src[max(0, x - 1), y], src[x, min(h - 1, y + 1)]
            o[2 * x, 2 * y] = a if cc == a and cc != dd and a != b else p
            o[2 * x + 1, 2 * y] = b if a == b and a != cc and b != dd else p
            o[2 * x, 2 * y + 1] = cc if dd == cc and dd != b and cc != a else p
            o[2 * x + 1, 2 * y + 1] = dd if b == dd and b != a and dd != cc else p
    return out


def save(img, name, native=False):
    """Pieces drawn in world units are doubled here; pieces drawn in art pixels pass native=True."""
    (img if native else scale2x(img)).save(f"assets/images/{name}.png")


def speckle(img, box, on, names, count, longest=2, rng=None):
    """Scatter short one-pixel-high dashes over the pixels of one colour: texture at the fine size."""
    rng = rng or random
    x0, y0, x1, y1 = box
    for _ in range(count):
        x, y, colour = rng.randint(x0, x1), rng.randint(y0, y1), c(rng.choice(names))
        for k in range(rng.randint(1, longest)):
            if x + k < img.width and img.getpixel((x + k, y)) == on:
                img.putpixel((x + k, y), colour)


def layer(width=W):
    img = Image.new("RGBA", (width, H), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


# Sky, in art pixels: flat bands. The sun and moon are their own pieces (below).
sky = Image.new("RGBA", (SKY_W, H * S), (0, 0, 0, 0))
d = ImageDraw.Draw(sky)
SKY_TOPS = [0, 112, 172, 228, 274]
for i, top in enumerate(SKY_TOPS):
    d.rectangle([0, top, SKY_W, H * S], fill=far(f"sky{i + 1}"))
# Each band edge is broken up over twelve rows with the two colours it already has: a quarter, a half,
# then three quarters of the lower colour. It softens the stripes and costs no palette entries.
for i, top in enumerate(SKY_TOPS[1:]):
    for row in range(-6, 6):
        y = top + row
        for x in range(SKY_W):
            quarter = x % 2 == 0 and y % 2 == 0 and (x // 2 + y // 2) % 2 == 0
            half = (x + y) % 2 == 0
            lower = quarter if row < -2 else half if row < 2 else not quarter
            sky.putpixel((x, y), far(f"sky{i + 2}" if lower else f"sky{i + 1}"))
save(sky, "sky", native=True)

# Clouds are their own pieces, one per 112x36 cell, so the game can drift each at its own pace.
CLOUD_WIDTHS = [36, 50, 28, 24, 30]
rs = random.Random(21)
clouds = Image.new("RGBA", (112 * len(CLOUD_WIDTHS), 36), (0, 0, 0, 0))
d = ImageDraw.Draw(clouds)
for n, w in enumerate(CLOUD_WIDTHS):
    cx, cy = n * 112 + 56, 26
    d.ellipse([cx - w, cy - 5, cx + w, cy + 8], fill=far("cloud_shade"))
    for k in range(5):  # rounded tops of different heights
        px, r = cx - w + 8 + k * (2 * w - 16) // 4, rs.randint(w // 5 + 3, w // 3 + 5)
        d.ellipse([px - r, cy - r - 2, px + r, cy + r - 4], fill=far("cloud"))
        d.ellipse([px - r + 3, cy + 1, px + r - 1, cy + 6], fill=far("cloud_shade"))
    d.rectangle([cx - w + 4, cy + 6, cx + w - 4, cy + 8], fill=far("cloud_shade"))  # flat underside
save(clouds, "clouds", native=True)

# Sun and moon, in art pixels, each in a 70x70 frame (35 units) so the game can move them.
# Sun: a disc with a paler heart and two halo rings. Each ring ends in a thin checkered band, so the rings
# read as glow rather than as hard plates.
sun = Image.new("RGBA", (70, 70), (0, 0, 0, 0))
for y in range(70):
    for x in range(70):
        r = math.hypot(x - 34.5, y - 34.5)
        checker = (x + y) % 2 == 0
        name = None
        if r <= 7 or (r <= 9 and checker):
            name = "star"
        elif r <= 12.5:
            name = "sun"
        elif r <= 20 or (r <= 23 and checker):
            name = "halo2"
        elif r <= 31 or (r <= 34.5 and checker):
            name = "halo1"
        if name:
            sun.putpixel((x, y), far(name))
save(sun, "sun", native=True)

# Moon: eight phases side by side: new, waxing crescent, first quarter, waxing gibbous, full, then waning.
# A 26-pixel disc, the size of the sun's. The darker patches are our own made-up seas, plus a few small
# craters and a shaded rim on the lower left.
moon = Image.new("RGBA", (70 * 8, 70), (0, 0, 0, 0))
MOON_R = 13
MOON_SEAS = [(-5, -5, 4.2, 3.2), (-1, -8, 2.6, 1.6), (4, -2, 3.0, 2.4), (-4, 4, 3.2, 2.2), (3, 6, 2.2, 1.5), (7, 3, 1.4, 1.8)]
MOON_CRATERS = [(8, -6), (-9, 0), (0, 2), (6, 9), (-2, 9), (1, -3), (9, -1)]
# Where the shadow line sits in each phase, as a share of each row's half width. Crescent and gibbous are
# pushed a little further from new and full than the true geometry, so they are easy to tell apart.
MOON_EDGE = [1.0, 0.55, 0.0, -0.55, -1.0, -0.55, 0.0, 0.55]
for phase in range(8):
    for y in range(-MOON_R, MOON_R):
        for x in range(-MOON_R, MOON_R):
            fx, fy = x + 0.5, y + 0.5
            r = math.hypot(fx, fy)
            if r > MOON_R:
                continue
            edge = MOON_EDGE[phase] * math.sqrt(MOON_R * MOON_R - fy * fy)
            lit = fx > edge if phase <= 4 else fx < -edge
            sea = any(((fx - sx) / a) ** 2 + ((fy - sy) / b) ** 2 <= 1 for sx, sy, a, b in MOON_SEAS)
            rim = r > MOON_R - 1.6 and fx - fy < -4 and (x + y) % 2 == 0
            shade = sea or rim or (x, y) in MOON_CRATERS
            # The unlit part is drawn in its own dim colour, so the full disc stays visible in every phase.
            name = ("moon_shade" if shade else "moon") if lit else "moon_dark"
            moon.putpixel((70 * phase + 35 + x, 35 + y), far(name))
save(moon, "moon", native=True)

# Wildlife. Both reuse colours the scene already has, so they cost no palette entries.
def creature(name, frames, colours, width, afloat=False):
    """A sheet with the frames facing right in the top row and mirrored in the bottom row."""
    height = len(frames[0])
    img = Image.new("RGBA", (width * len(frames), height * 2), (0, 0, 0, 0))
    for f, rows in enumerate(frames):
        for y, row in enumerate(rows):
            for x, ch in enumerate(row.ljust(width, ".")):
                if ch != ".":
                    index = WATER_HI if colours[ch] == "wake" else INDEX[colours[ch]]
                    # Blue marks pixels that float on the water: the shader shows them instead of the reflection.
                    px = (index * 4, 255, 255 if afloat else 0, 255)
                    img.putpixel((f * width + x, y), px)
                    img.putpixel((f * width + width - 1 - x, height + y), px)
    save(img, name)


DUCK = [
    "........hh..",
    ".......hhhbb",
    ".......hh...",
    "t.dddddww...",
    "tddddddwww..",
    ".dddddwwww..",
    "..wwwwwww...",
]
creature("duck", [DUCK + ["k.kkkkkkk.kk"], DUCK + ["kk.kkkkkkk.k"]],
         {"h": "tree", "b": "scarf", "d": "dog_shade", "w": "dog", "t": "dog", "k": "wake"}, 12, afloat=True)
SIT = [
    "tttt...e.e..",
    "tttt..hhhh..",
    "ttt...hkhhn.",
    ".tt..bhhhh..",
    ".tt.bbbww...",
    "..tbbbbww...",
    "..tbbbbw....",
    "...bbbbbf...",
    "...ff..ff...",
]
RUN = [
    "tt..........",
    "ttt.....e.e.",
    ".ttt...hhhh.",
    "..ttbbbhkhhn",
    "...bbbbbbhh.",
    "...bbbbbbw..",
]
creature("squirrel", [
    [".tt........."] + SIT,
    ["..tt........"] + [".ttt...e.e.."] + SIT[1:],
    ["", "", ""] + RUN + ["..f.f...f.f."],
    ["", ""] + RUN + ["...ff..ff...", ""],
], {"t": "coat", "b": "wall", "h": "wall", "e": "wall_shade", "f": "wall_shade", "w": "dog", "k": "log", "n": "log"}, 12)

# Far hills, in art pixels: a ridge with mountains (snow on top, one face in shade), and a
# nearer ridge with a ragged, wooded top. This layer moves at 0.3 of the camera, so only its left part shows.
hills = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
d = ImageDraw.Draw(hills)
PEAKS = [(150, 96, 1.2), (400, 150, 1.35), (640, 120, 1.25)]  # centre, top, steepness
for x in range(W * S):
    y = 2 * (150 + 16 * math.sin(x / 62.0) + 6 * math.sin(x / 18.0 + 2))
    peak = None
    for cx, top, steep in PEAKS:
        py = top + abs(x - cx) * steep + 5 * math.sin(x / 7.0) + 3 * math.sin(x / 3.1)
        if py < y:
            y, peak = py, (cx, top)
    y = int(y)
    d.line([x, y, x, H * S], fill=far("hill_far"))
    if peak:
        cx, top = peak
        snow = top + 40 + int(10 * abs((x / 11.0) % 2 - 1)) + int(4 * math.sin(x / 3.0))
        if y < snow:
            d.line([x, y, x, snow], fill=far("hill_snow"))
        if x > cx:  # the face away from the light: one flat tone, with a broken edge down the spur and below
            deep = 76 + int(18 * math.sin(x / 9.0) + 8 * math.sin(x / 3.7))
            for yy in range(y + 1, min(y + deep, 340)):
                spur = cx + 0.3 * (yy - top) + 5 * math.sin(yy / 8.0) + 2 * math.sin(yy / 2.9)
                fade = yy > y + deep - 10 and (x + yy) % 2 == 0
                if x > spur and not fade:
                    hills.putpixel((x, yy), far("hill_shade"))
rh = random.Random(4)
for x in range(W * S):
    y = int(2 * (172 + 10 * math.sin(x / 46.0 + 4) + 4 * math.sin(x / 14.0))) - [0, 2, 5, 3, 1][x % 5] - rh.randint(0, 2)
    d.line([x, y, x, H * S], fill=far("hill_near"))
    if x % 5 == 2 and rh.random() < 0.6:
        d.line([x, y - rh.randint(2, 5), x, y], fill=far("hill_near"))
save(hills, "hills", native=True)

# Trees, in art pixels: three kinds (open-boughed conifers, round-crowned trees, thin sparse ones) in mixed
# sizes, some golden, with undergrowth in front and a darker row of plain shapes behind.
trees = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
d = ImageDraw.Draw(trees)
# The forest stops where the land does. This layer moves at 0.6 of the camera, so its end is placed to line
# up with the shore when the shore is mid-screen; past it there are only the hills and the water.
FOREST_END = 342
FLOOR = 190 * S
d.polygon([(0, FLOOR), (FOREST_END * S, FLOOR), (FOREST_END * S + 24, WATER * S), (FOREST_END * S + 24, H * S), (0, H * S)],
          fill=c("tree"))
rt = random.Random(5)


GREEN = ("tree", "tree_light", "tree_dark")
GOLD = ("tree_gold", "scarf", "wall_light")
RUST = ("coat", "tree_gold", "coat_shade")
FLAT = ("tree_dark", None, None)  # the row behind: shapes only


TARGET = trees  # the layer that tput, clump and rock draw on


def tput(x, y, name):
    if 0 <= x < W * S and 0 <= y < H * S:
        # Below the waterline only pixels marked afloat are shown; the rest is replaced by the reflection.
        TARGET.putpixel((int(x), int(y)), (INDEX[name] * 4, 255, 255, 255) if y >= WATER * S else c(name))


def grain(x, y, salt=0):
    """A fixed random number from 0 to 1 for a pixel."""
    n = (int(x) * 73856093) ^ (int(y) * 19349663) ^ (salt * 83492791)
    n = (n ^ (n >> 13)) * 1274126177 & 0x7FFFFFFF
    return (n ^ (n >> 16)) % 1000 / 1000.0


def clump(cx, cy, rx, ry, tones):
    """A mass of leaves: a ragged blob, lit from the upper right in loose patches, dark underneath."""
    body, light, dark = tones
    for y in range(int(cy - ry - 2), int(cy + ry + 3)):
        for x in range(int(cx - rx - 2), int(cx + rx + 3)):
            u, v = (x - cx) / rx, (y - cy) / ry
            r = math.hypot(u, v)
            # The outline is broken in runs of a few pixels, so it reads as foliage and not as a disc.
            if r > 0.86 + 0.22 * grain(x // 3, y // 2, 1):
                continue
            name = body
            if light:
                lit = (u - v * 1.3) / 1.6  # toward the upper right
                patch = grain(x // 4, y // 3, 2)
                if lit > 0.08 + 0.32 * patch or (lit > -0.25 and grain(x // 2, y, 3) < 0.12):
                    name = light
                elif lit < -0.5 + 0.25 * patch or v > 0.7:
                    name = dark
            tput(x, y, name)


def trunk(x, base, top, wide, bend=0.0, plain=None):
    """A tapering trunk with a dark side, bark marks and a flare at the foot. Returns its centre at each row."""
    centre = {}
    for y in range(int(top), int(base) + 7):
        p = min(1.0, (base - y) / max(1, base - top))
        cx = x + bend * math.sin(p * math.pi) + 0.6 * math.sin(y / 9.0 + x)
        half = max(0.5, wide / 2 * (1 - p * 0.75)) + (max(0, 6 - (base - y)) * 0.4 if y < base else 2.5)
        centre[y] = cx
        for px in range(int(round(cx - half)), int(round(cx + half)) + 1):
            name = plain or ("log" if px > cx + half * 0.25 or grain(px, y // 3, 4) < 0.12 else "trunk")
            tput(px, y, name)
    return centre


def branch(x0, y0, x1, y1, name, thick=1):
    steps = int(max(abs(x1 - x0), abs(y1 - y0))) + 1
    for k in range(steps + 1):
        t = k / steps
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t - 4 * math.sin(t * math.pi) * 0.5
        for w in range(thick if t < 0.5 else 1):
            tput(x, y + w, name)


def spruce(x, h, tones):
    """A conifer with its trunk showing: separate drooping boughs, uneven in length, with gaps between."""
    body, light, dark = tones
    top = FLOOR - h
    centre = trunk(x, FLOOR, top + 4, 3 + h // 45, rt.uniform(-3, 3), None if light else body)
    y = top + 8
    while y < FLOOR - h * 0.16:
        p = (y - top) / h
        for side in (-1, 1):
            if rt.random() < 0.12:
                continue  # a missing bough
            long = int((h * 0.2 + 12) * p ** 0.75 * rt.uniform(0.65, 1.15)) + 3
            yb = y + rt.randint(-3, 3)
            for k in range(long):
                t = k / long
                droop = k * 0.22 + t * t * 5
                thick = 1.5 + 5.5 * math.sin(math.pi * min(1.0, t * 1.15) ** 0.7) * (0.6 + 0.4 * p)
                px = int(centre.get(yb, x)) + side * k
                lo, hi = int(yb + droop - thick * 0.45), int(yb + droop + thick * 0.55 + [0, 1, 2, 0, 3, 1][(k + yb) % 6])
                for py in range(lo, hi + 1):
                    name = body
                    if light:
                        if py >= hi - 1 and thick > 3:
                            name = dark
                        elif py <= lo + 1 and (side > 0 or grain(px // 2, py, 5) < 0.35):
                            name = light
                        elif side < 0 and grain(px // 3, py, 6) < 0.3:
                            name = dark
                    tput(px, py, name)
        y += rt.randint(8, 13) + int(p * 5)
    clump(x, top + 5, 3, 7, tones)  # the tip


def broadleaf(x, h, tones):
    """A round-crowned tree: a forking trunk under a crown built from overlapping clumps."""
    top = FLOOR - h
    wide, tall = h * rt.uniform(0.26, 0.36), h * rt.uniform(0.3, 0.4)
    cy = top + tall
    plain = None if tones[1] else tones[0]
    centre = trunk(x, FLOOR, cy, 4 + h // 40, rt.uniform(-4, 4), plain)
    for side in (-1, 1):
        y0 = int(cy + tall * rt.uniform(0.5, 0.9))
        branch(centre.get(y0, x), y0, x + side * wide * 0.6, cy + tall * 0.1, plain or "trunk", 2)
    spots = [(rt.uniform(-1, 1), rt.uniform(-1, 1)) for _ in range(40)]
    spots = sorted([sp for sp in spots if math.hypot(*sp) <= 1][:int(9 + h / 22)], key=lambda sp: -sp[1])
    for u, v in spots:  # lowest first, so the upper clumps overlap them
        r = rt.uniform(0.3, 0.5) * wide
        clump(x + u * wide * 0.75, cy + v * tall * 0.75, r, r * rt.uniform(0.7, 0.95), tones)


def sparse(x, h, tones):
    """A thin, leaning tree with bare branches and a few small tufts of leaves left on them."""
    top = FLOOR - h
    plain = None if tones[1] else tones[0]
    centre = trunk(x, FLOOR, top, 3, rt.uniform(-7, 7), plain)
    for k in range(4 + h // 30):
        y0 = int(top + h * rt.uniform(0.08, 0.6))
        side = 1 if k % 2 else -1
        long = h * rt.uniform(0.1, 0.24) * (0.5 + (y0 - top) / h)
        x1, y1 = centre.get(y0, x) + side * long, y0 - long * rt.uniform(0.3, 0.8)
        branch(centre.get(y0, x), y0, x1, y1, plain or "log")
        for _ in range(rt.randint(1, 3)):
            t = rt.uniform(0.5, 1.0)
            r = rt.uniform(2.5, 6)
            clump(centre.get(y0, x) + (x1 - centre.get(y0, x)) * t, y0 + (y1 - y0) * t - 2, r, r * 0.8, tones)
    clump(centre.get(top, x), top, 5, 4, tones)


def shrub(x, tones):
    for _ in range(rt.randint(2, 4)):
        r = rt.uniform(6, 13)
        clump(x + rt.uniform(-10, 10), FLOOR - r * 0.5 + 3, r, r * 0.75, tones)


KINDS = [(spruce, 0.5), (broadleaf, 0.8), (sparse, 1.0)]


def plant(x, h, tones):
    roll = rt.random()
    next(kind for kind, share in KINDS if roll <= share)(x, h, tones)


x = 6
while x < FOREST_END * S - 30:
    plant(x, rt.randint(110, 230), FLAT)
    x += rt.randint(24, 44)
x = 20
while x < FOREST_END * S - 44:
    plant(x, rt.randint(130, 300), GOLD if rt.random() < 0.25 else GREEN)
    x += rt.randint(40, 72)
x = 10
while x < FOREST_END * S - 20:  # undergrowth in front of the trunks
    shrub(x, rt.choice([GREEN, GREEN, GOLD, RUST]))
    x += rt.randint(34, 80)
save(trees, "trees", native=True)

# The bank and a cabin (the dog is its own sprite, further down). Below the waterline the shader shows the
# reflection instead, except where a pixel is marked as afloat.
ground, d = layer()
d.rectangle([0, BANK, W, H], fill=c("bank"))
d.rectangle([0, WATER - 4, W, H], fill=c("bank_face"))
d.rectangle([50, BANK - 30, 96, BANK - 1], fill=c("wall"))
for y in range(BANK - 26, BANK, 6):
    d.line([50, y, 96, y], fill=c("wall_shade"))
d.polygon([(44, BANK - 30), (73, BANK - 50), (102, BANK - 30)], fill=c("roof"))
d.rectangle([58, BANK - 18, 67, BANK - 1], fill=c("door"))
d.rectangle([78, BANK - 22, 88, BANK - 13], fill=c("window", light=False))
d.line([83, BANK - 22, 83, BANK - 13], fill=c("wall_shade"))

# What the wider map adds, spread over the five screens. Placeholder shapes in colours the scene already has.
def afloat(name):
    """Below the waterline only pixels with blue set are shown; the rest is replaced by the reflection."""
    return (INDEX[name] * 4, 255, 255, 255)


# Screen 1, left of the cabin: the woodpile (the spec's picture of Energy), three rows of log ends.
for row, count in enumerate([4, 3, 2]):
    for k in range(count):
        x, y = 10 + row * 3 + k * 6, BANK - 4 - row * 4
        d.rectangle([x, y, x + 4, y + 3], fill=c("log"))
        d.rectangle([x + 1, y + 1, x + 3, y + 2], fill=c("wall"))
        d.point([x + 2, y + 1], fill=c("rope"))
# Screen 2, right of the fire: a chopping block.
d.rectangle([190, BANK - 6, 197, BANK - 1], fill=c("trunk"))
d.rectangle([190, BANK - 6, 197, BANK - 6], fill=c("rope"))
# Screen 2 to 3: two boulders.
for left, right, tall in [(232, 256, 13), (252, 264, 7)]:
    d.chord([left, BANK - tall, right, BANK + tall - 2], 180, 360, fill=c("tarp_shade"))
    d.chord([left + 3, BANK - tall + 1, right - 8, BANK - 2], 180, 360, fill=c("tarp"))
# Screen 4: one big tree on the bank, in front of the forest. The character walks in front of it.
TREE = 430
d.rectangle([TREE - 4, BANK - 40, TREE + 3, BANK], fill=c("trunk"))
d.line([TREE - 4, BANK - 40, TREE - 4, BANK], fill=c("door"))
CROWN = [(TREE, BANK - 52, 26, 16), (TREE - 10, BANK - 66, 18, 14), (TREE + 9, BANK - 72, 17, 13), (TREE, BANK - 84, 13, 10)]
for cx, cy, rx, ry in CROWN:
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=c("tree"))
for cx, cy, rx, ry in CROWN:  # lighter on top, so it stands out from the dark forest behind it
    d.ellipse([cx - rx + 2, cy - ry, cx + rx - 5, cy + ry - 8], fill=c("tree_light"))
# Screen 3: a pebble shore, the place for skipping stones.
d.rectangle([282, BANK, 352, WATER - 1], fill=c("rope"))
for _ in range(90):
    x, y = random.randint(280, 353), random.randint(BANK, WATER - 2)
    d.rectangle([x, y, x + random.randint(0, 2), y], fill=c(random.choice(["tarp", "ash", "dog_shade", "tarp_shade"])))
# Reeds at the water's edge, between the landmarks. They stand above the waterline, so they are mirrored.
for left in (206, 364, 474, 502):
    for k in range(7):
        x, tall = left + k * 2 + random.randint(0, 1), random.randint(5, 11)
        d.line([x, WATER - 1 - tall, x, WATER - 1], fill=c("tree"))
        if k % 2:
            d.line([x, WATER - 2 - tall, x, WATER - tall], fill=c("trunk"))
# Screen 5: the land ends and a low dock runs on from it, level with the bank, so the character walks
# straight onto it. Seen from the side, with the rowing boat on the water next to it. The deck and its
# posts are above the waterline, so the shader mirrors them like everything else.
SHORE, DOCK_END = 530, 597
for x in range(SHORE, W):
    for y in range(H):
        if y < WATER and x > SHORE + max(0, y - BANK) // 2:  # past the shore, leave only a short slope of bank
            ground.putpixel((x, y), (0, 0, 0, 0))
d.rectangle([SHORE - 10, BANK, DOCK_END, BANK + 2], fill=c("wall_shade"))
d.line([SHORE - 10, BANK, DOCK_END, BANK], fill=c("wall"))
for x in range(SHORE - 10, DOCK_END, 7):
    d.point([x, BANK], fill=c("wall_shade"))  # gaps between the planks
for x in range(SHORE + 4, DOCK_END, 14):
    d.rectangle([x, BANK + 3, x + 1, WATER - 1], fill=c("trunk"))
top = WATER + 3
d.polygon([(558, top), (594, top), (589, top + 7), (563, top + 7)], fill=afloat("wall_shade"))
d.line([558, top, 594, top], fill=afloat("rope"))
d.line([563, top + 4, 589, top + 4], fill=afloat("door"))
d.line([568, top - 3, 584, top - 1], fill=c("trunk"))  # an oar lying across it
# Everything above was drawn in world units. Double it, then add the detail only the finer size can hold.
ground = scale2x(ground)
d = ImageDraw.Draw(ground)
rg = random.Random(9)
B2, W2 = BANK * S, WATER * S
speckle(ground, (0, B2 + 4, SHORE * S, W2 - 9), c("bank"), ["bank_dark", "bank_dark", "bank_top"], 2600, 3, rg)
speckle(ground, (0, W2 - 8, SHORE * S, W2 - 1), c("bank_face"), ["log", "wall_shade"], 900, 4, rg)
# The cabin: a lit edge on every log, log ends at the corners, shingles, a chimney, window frame, door planks.
for y in range(BANK - 26, BANK, 6):
    d.line([100, y * S - 1, 193, y * S - 1], fill=c("wall_light"))
for y in range(BANK - 29, BANK - 1, 6):
    for x in (100, 190):
        d.rectangle([x, y * S, x + 3, y * S + 7], fill=c("wall_shade"))
        d.rectangle([x + 1, y * S + 2, x + 2, y * S + 5], fill=c("wall_light"))
d.rectangle([172, B2 - 96, 181, B2 - 70], fill=c("tarp_shade"))  # chimney
d.rectangle([170, B2 - 98, 183, B2 - 95], fill=c("ash"))
d.line([172, B2 - 86, 181, B2 - 86], fill=c("ash"))
d.line([172, B2 - 78, 181, B2 - 78], fill=c("ash"))
for y in range(B2 - 100, B2 - 59):
    for x in range(88, 206):
        if ground.getpixel((x, y)) == c("roof"):
            row = (y - (B2 - 100)) // 6
            if (y - (B2 - 100)) % 6 == 5 or ((x + row * 5) % 10 == 0 and (y - (B2 - 100)) % 6 < 5 and row % 1 == 0 and (x + y) % 2 == 0):
                ground.putpixel((x, y), c("roof_light"))
d.rectangle([155, B2 - 45, 177, B2 - 25], outline=c("wall_shade"))
d.line([154, B2 - 24, 178, B2 - 24], fill=c("wall_light"))  # sill
d.line([156, B2 - 35, 176, B2 - 35], fill=c("wall_shade"))
for x in (121, 126, 131):
    d.line([x, B2 - 36, x, B2 - 2], fill=c("log"))
d.rectangle([116, B2 - 37, 135, B2 - 36], fill=c("log"))
d.rectangle([131, B2 - 20, 132, B2 - 18], fill=c("scarf"))  # door handle
# Boulders, the big tree and the pebbles get texture.
speckle(ground, (464, B2 - 26, 530, B2), c("tarp_shade"), ["ash", "tarp"], 60, 3, rg)
speckle(ground, (464, B2 - 26, 530, B2), c("tarp"), ["moon_shade", "tarp_shade"], 40, 2, rg)
T2 = TREE * S
speckle(ground, (T2 - 60, B2 - 190, T2 + 60, B2 - 60), c("tree_light"), ["tree", "tuft", "tree"], 900, 3, rg)
speckle(ground, (T2 - 60, B2 - 190, T2 + 60, B2 - 60), c("tree"), ["tree_dark", "tree_dark", "tree_light"], 700, 3, rg)
for x in (T2 - 5, T2 - 1, T2 + 3):
    for y in range(B2 - 80, B2, 9):
        d.line([x + rg.randint(-1, 1), y, x + rg.randint(-1, 1), y + rg.randint(3, 7)], fill=c("log"))
for root in (-10, 8):  # roots
    d.polygon([(T2 + root, B2), (T2 + root // 2, B2 - 8), (T2 + root // 2 + 3, B2)], fill=c("trunk"))
for left in (206, 364, 474, 502):  # thin reeds among the thick ones
    for k in range(9):
        x, tall = left * S + rg.randint(-4, 30), rg.randint(8, 26)
        d.line([x, W2 - 1 - tall, x, W2 - 1], fill=c(rg.choice(["tree", "tuft", "tree_light"])))
for x in range((SHORE - 10) * S, DOCK_END * S, 14):  # plank ends on the dock
    d.line([x, B2, x, B2 + 1], fill=c("log"))

# Depth. The view looks slightly down on the ground: the grass carries on behind the line the character
# walks along, up to the foot of the forest, and things stand on it at different distances. Whatever is
# nearer than the walking line goes on a separate front layer, drawn over the character.
BACK = B2 - 34  # the far edge of the grass
LAND = SHORE * S  # the grass stops where the land does
rd = random.Random(21)


def rock(cx, base, wide, tall):
    """A boulder with a lit top-left face, a shaded right face, a dark foot and a little moss."""
    break_at = rd.uniform(0.45, 0.65)
    for k in range(int(wide)):
        t = k / max(1, wide - 1)
        top = tall * math.sin(math.pi * (0.08 + 0.84 * t)) ** 0.55 * (1.0 if t < break_at else 0.86)
        top += rd.choice([0, 0, 1])
        for r in range(int(top) + 1):
            y = base - r
            if r <= 1:
                name = "ash"
            elif t > break_at + 0.12 * (r / tall) or r < tall * 0.25:
                name = "tarp_shade"
            else:
                name = "tarp"
            if r >= int(top) - 1 and t < break_at and grain(cx + k, y, 7) < 0.45:
                name = "bank_top"  # moss
            elif name != "ash" and grain((cx + k) // 3, y // 2, 8) < 0.1:
                name = "tarp_shade" if name == "tarp" else "ash"
            tput(cx - wide / 2 + k, y, name)


def tussock(cx, base, tall, tones=("bank", "bank_top", "tuft")):
    for k in range(-5, 6):
        long = int(tall * (1 - abs(k) / 7) * rd.uniform(0.6, 1.0))
        for r in range(long):
            tput(cx + k + (k * r) // 14, base - r, tones[2] if r > long - 3 else tones[(k + r // 3) % 2])


# The grass plane behind the walking line, composed under everything already drawn.
plane = Image.new("RGBA", ground.size, (0, 0, 0, 0))
TARGET = plane
for x in range(LAND + 8):
    back_y = BACK + int(3 * math.sin(x / 37.0) + 2 * math.sin(x / 11.0 + 1))
    for y in range(back_y, B2 + 2):
        depth = (y - back_y) / (B2 - back_y)  # 0 at the far edge, 1 at the walking line
        if x > LAND - 14 + depth * 22:
            continue  # the shore slopes away at the end of the land
        band = depth + 0.25 * grain(x // 5, y // 2, 9)
        tput(x, y, "bank_top" if band < 0.45 else "bank")
    if grain(x, 0, 10) < 0.5 and x < LAND - 14:  # a ragged fringe along the far edge
        for r in range(1 + int(4 * grain(x, 1, 10))):
            tput(x, back_y - r, "bank_top" if grain(x, r, 11) < 0.6 else "tuft")
plane.alpha_composite(ground)
ground = plane
TARGET = ground
d = ImageDraw.Draw(ground)
# Blades all over the plane, shorter the further away, and a worn path where the character walks.
for _ in range(2600):
    x, y = rd.randint(0, LAND - 30), rd.randint(BACK + 6, W2 - 10)
    if ground.getpixel((x, y)) in (c("bank"), c("bank_top")):
        tall = 1 + int(3 * (y - BACK) / (W2 - BACK) + rd.random() * 2)
        d.line([x, y - tall, x, y], fill=c(rd.choice(["tuft", "bank_top", "bank_dark", "bank_dark"])))
for _ in range(700):
    x, y = rd.randint(0, LAND - 20), B2 + rd.randint(-1, 5)
    if ground.getpixel((x, y)) in (c("bank"), c("bank_top"), c("bank_dark")):
        d.line([x, y, x + rd.randint(1, 5), y], fill=c(rd.choice(["rope", "bank_face", "dog_shade"])))

# The cabin gets a side: a wall and a roof slope running back to the right, both in shade.
SIDE, RISE = 30, 14
d.polygon([(146, B2 - 93), (99, B2 - 60), (193, B2 - 60)], fill=c("wall"))  # the gable end is logs, under the roof's edge
for y in range(B2 - 88, B2 - 60, 6):
    half_w = int((y - (B2 - 93)) * 47 / 33)
    d.line([146 - half_w, y, 146 + half_w, y], fill=c("wall_shade"))
d.line([146, B2 - 101, 88, B2 - 61], fill=c("roof_light"))
d.polygon([(194, B2 - 60), (194 + SIDE, B2 - 60 - RISE), (194 + SIDE, B2 - RISE), (194, B2 - 1)], fill=c("wall_shade"))
for y in range(B2 - 52, B2, 12):
    d.line([194, y - 1, 194 + SIDE, y - 1 - RISE], fill=c("door"))
d.rectangle([206, B2 - 46, 215, B2 - 30], fill=c("window", light=False))  # a small side window
d.rectangle([206, B2 - 46, 215, B2 - 30], outline=c("door"))
d.polygon([(146, B2 - 100), (146 + SIDE, B2 - 100 - RISE), (206 + SIDE, B2 - 60 - RISE), (206, B2 - 60)], fill=c("roof"))
for k in range(0, 58, 6):  # courses of shingles down the slope
    d.line([146 + k, B2 - 100 + k * 2 // 3, 146 + k + SIDE, B2 - 100 + k * 2 // 3 - RISE], fill=c("roof_light"))
d.line([146, B2 - 100, 146 + SIDE, B2 - 100 - RISE], fill=c("roof_light"))  # the ridge
d.rectangle([172, B2 - 118, 181, B2 - 92], fill=c("tarp_shade"))  # the chimney, now standing on the slope
d.rectangle([170, B2 - 120, 183, B2 - 117], fill=c("ash"))
d.rectangle([178, B2 - 116, 181, B2 - 92], fill=c("ash"))
d.rectangle([112, B2 - 1, 140, B2 + 3], fill=c("wall_light"))  # a doorstep
d.line([112, B2 + 4, 140, B2 + 4], fill=c("wall_shade"))
for k in range(6):  # a ground shadow under the side wall
    d.line([196 + k * 5, B2 + 1 - k * 2, 196 + SIDE + 6, B2 + 1 - k * 2], fill=c("bank_dark"))

# A pool lying in the grass behind the walking line. It is painted in the water's own colour: the shader
# mirrors only about the one straight waterline, so this pool reflects nothing.
POND = (760, B2 - 19, 54, 8)
for y in range(POND[1] - POND[3] - 3, POND[1] + POND[3] + 2):
    for x in range(POND[0] - POND[2] - 2, POND[0] + POND[2] + 3):
        wob = 3 * math.sin(x / 9.0) * (1 if y < POND[1] else 0.4)
        u, v = (x - POND[0]) / POND[2], (y - POND[1] + wob * 0.4) / POND[3]
        v_up = (y + 3 - POND[1] + wob * 0.4) / POND[3]
        if u * u + v * v <= 1:
            glint = grain(x // 5, y, 14) < 0.07 and v > -0.5
            ground.putpixel((x, y), ((WATER_HI if glint else WATER_TINT) * 4, 0, 0, 255))
            if u * u + v_up * v_up > 1:
                ground.putpixel((x, y), far("bank_face"))  # the far bank's cut edge
        elif u * u + ((y - 1 - POND[1]) / POND[3]) ** 2 <= 1 and v > 0:
            ground.putpixel((x, y), c("bank_dark"))  # the near lip
for x in (POND[0] - 50, POND[0] - 43, POND[0] + 38, POND[0] + 47):
    tussock(x, POND[1] + rd.randint(-2, 6), rd.randint(9, 14), ("bank_dark", "bank", "tuft"))
rock(POND[0] + 22, POND[1] - 5, 16, 8)

# Things standing behind the walking line: boulders, bushes, tussocks and a fallen log.
for x in range(20, LAND - 40, 1):
    if 80 < x < 240 or 290 < x < 375 or POND[0] - 70 < x < POND[0] + 70 or rd.random() > 0.022:
        continue
    base = rd.randint(BACK + 8, B2 - 5)
    kind = rd.random()
    if kind < 0.4:
        rock(x, base, rd.randint(14, 34), rd.randint(8, 20))
        if rd.random() < 0.5:
            rock(x + rd.randint(12, 20), base + 2, rd.randint(8, 14), rd.randint(5, 9))
        tussock(x - 8, base + 2, 7)
    elif kind < 0.75:
        tones = rd.choice([GREEN, GREEN, GOLD, RUST])
        for _ in range(rd.randint(2, 3)):
            r = rd.uniform(7, 12)
            clump(x + rd.uniform(-9, 9), base - r * 0.6, r, r * 0.8, tones)
    else:
        tussock(x, base, rd.randint(8, 14))
        tussock(x + 7, base + 1, rd.randint(6, 10))
d.rectangle([620, B2 - 16, 668, B2 - 10], fill=c("trunk"))  # a fallen log by the pebble shore
d.line([620, B2 - 16, 668, B2 - 16], fill=c("wall_light"))
d.line([620, B2 - 10, 668, B2 - 10], fill=c("log"))
d.ellipse([614, B2 - 17, 623, B2 - 9], fill=c("wall_light"), outline=c("log"))
save(ground, "ground", native=True)

# The front layer: rocks and grass at the water's edge and stones standing in the shallows, nearer than
# the character. Parts below the waterline are marked afloat, so the shader shows them, not the mirror.
front = Image.new("RGBA", ground.size, (0, 0, 0, 0))
TARGET = front
x = 14
while x < LAND - 30:
    pebbles = 560 < x < 710
    kind = rd.random()
    if kind < 0.45 and not pebbles:
        tussock(x, W2 - rd.randint(2, 9), rd.randint(9, 16))
        tussock(x + 8, W2 - rd.randint(1, 6), rd.randint(7, 12))
    elif kind < 0.85:
        rock(x, W2 + rd.randint(0, 5), rd.randint(12, 30), rd.randint(7, 15))
        if rd.random() < 0.6:
            rock(x + rd.randint(14, 24), W2 + rd.randint(3, 9), rd.randint(8, 16), rd.randint(4, 8))
    else:
        tones = rd.choice([GREEN, GOLD, RUST])
        r = rd.uniform(7, 11)
        clump(x, W2 - r * 0.5, r, r * 0.7, tones)
    x += rd.randint(26, 76)
for x in (150, 470, 760, 1010, LAND + 20, LAND + 70):  # stones out in the shallows
    rock(x, W2 + rd.randint(12, 22), rd.randint(12, 22), rd.randint(4, 7))
# Two trees on the near edge of the bank. The character walks behind their trunks.
for x, tall, tones in ((500, 250, GREEN), (990, 215, GOLD)):
    base = W2 - 4
    centre = trunk(x, base, base - tall, 13, rd.uniform(-5, 5))
    for side, up in ((-1, 0.55), (1, 0.66), (-1, 0.8)):
        y0 = int(base - tall * up)
        branch(centre[y0], y0, x + side * 30, y0 - 22, "trunk", 2)
        clump(x + side * 32, y0 - 26, 20, 13, tones)
    for u, v, r in ((-0.7, 0.2, 22), (0.75, 0.1, 24), (-0.3, -0.25, 26), (0.35, -0.4, 24), (0, -0.75, 20), (0, 0.25, 22)):
        clump(x + u * 42, base - tall + 14 + v * 36, r, r * 0.8, tones)
    tussock(x - 9, base + 3, 8)
    tussock(x + 10, base + 2, 7)
save(front, "front", native=True)

# Dormant and flourishing pieces, drawn over the same cabin and bank. World position is in main.dart.
# A tarp over the whole cabin: 66x54, placed at (40, BANK - 53).
tarp = Image.new("RGBA", (66, 54), (0, 0, 0, 0))
d = ImageDraw.Draw(tarp)
d.polygon([(33, 0), (2, 24), (3, 53), (62, 53), (63, 24)], fill=c("tarp"))
d.polygon([(33, 0), (2, 24), (8, 24), (33, 5)], fill=c("tarp_shade"))
for x in (12, 24, 41, 53):
    d.line([x, 26 + (x % 5), x, 53], fill=c("tarp_shade"))
for y in (24, 40):
    d.line([2, y, 63, y], fill=c("rope"))
for x in (0, 64):
    d.rectangle([x, 51, x + 1, 53], fill=c("trunk"))
d.line([2, 40, 0, 51], fill=c("rope"))
d.line([63, 40, 65, 51], fill=c("rope"))
save(tarp, "tarp")

# Flowers along the front of the cabin, two frames of 70x8: closed buds, then open.
flowers = Image.new("RGBA", (140, 8), (0, 0, 0, 0))
d = ImageDraw.Draw(flowers)
spots = [(random.randint(1, 67), random.randint(3, 5)) for _ in range(13)]
for f in range(2):
    for i, (x, h) in enumerate(spots):
        ox = f * 70 + x
        d.line([ox, 7 - h, ox, 7], fill=c("tuft"))
        if f == 0:
            d.point([ox, 7 - h], fill=c("tree_light"))
        else:
            d.rectangle([ox - 1, 6 - h, ox + 1, 7 - h], fill=c("petal" if i % 3 else "petal_light"))
            d.point([ox, 6 - h], fill=c("petal_light" if i % 3 else "petal"))
save(flowers, "flowers")

# The interface is ordinary colour, not indices: it is drawn after the shader.
# Row 0: three meter icons, 7x7, each as filled then empty. Below: a small font, one glyph per 6x10 cell.
ICONS = [
    ("..ooo.. .oaao.. oaao... oaao... oaaoo.o .oaaao. ..ooo..", (236, 226, 160)),  # moon: Sleep
    ("...oo.. ..oao.. .oaaoo. oaaaao. .ooaao. ..oao.. ..oo...", (255, 176, 72)),   # spark: Energy
    (".oo.... oaao... oaao... oaaooo. oaaaaao oaaaaao .ooooo.", (150, 200, 120)),  # boot: Activity
]
# Font: capitals 7 tall, lower case 5 tall with 2 rows below the line, up to 5 wide. Each glyph is
# (first row it uses, rows); cells are 6 wide and 10 tall with the baseline under row 6.
GLYPHS = {
    "A": (0, ".XXX. X...X X...X XXXXX X...X X...X X...X"), "B": (0, "XXXX. X...X X...X XXXX. X...X X...X XXXX."),
    "C": (0, ".XXX. X...X X.... X.... X.... X...X .XXX."), "D": (0, "XXXX. X...X X...X X...X X...X X...X XXXX."),
    "E": (0, "XXXXX X.... X.... XXXX. X.... X.... XXXXX"), "F": (0, "XXXXX X.... X.... XXXX. X.... X.... X...."),
    "G": (0, ".XXX. X...X X.... X.XXX X...X X...X .XXX."), "H": (0, "X...X X...X X...X XXXXX X...X X...X X...X"),
    "I": (0, "XXX .X. .X. .X. .X. .X. XXX"), "J": (0, "..XXX ...X. ...X. ...X. ...X. X..X. .XX.."),
    "K": (0, "X...X X..X. X.X.. XX... X.X.. X..X. X...X"), "L": (0, "X.... X.... X.... X.... X.... X.... XXXXX"),
    "M": (0, "X...X XX.XX X.X.X X.X.X X...X X...X X...X"), "N": (0, "X...X XX..X X.X.X X..XX X...X X...X X...X"),
    "O": (0, ".XXX. X...X X...X X...X X...X X...X .XXX."), "P": (0, "XXXX. X...X X...X XXXX. X.... X.... X...."),
    "Q": (0, ".XXX. X...X X...X X...X X.X.X X..X. .XX.X"), "R": (0, "XXXX. X...X X...X XXXX. X.X.. X..X. X...X"),
    "S": (0, ".XXXX X.... X.... .XXX. ....X ....X XXXX."), "T": (0, "XXXXX ..X.. ..X.. ..X.. ..X.. ..X.. ..X.."),
    "U": (0, "X...X X...X X...X X...X X...X X...X .XXX."), "V": (0, "X...X X...X X...X X...X X...X .X.X. ..X.."),
    "W": (0, "X...X X...X X...X X.X.X X.X.X XX.XX X...X"), "X": (0, "X...X X...X .X.X. ..X.. .X.X. X...X X...X"),
    "Y": (0, "X...X X...X .X.X. ..X.. ..X.. ..X.. ..X.."), "Z": (0, "XXXXX ....X ...X. ..X.. .X... X.... XXXXX"),
    "a": (2, ".XX. ...X .XXX X..X .XXX"), "b": (0, "X... X... XXX. X..X X..X X..X XXX."),
    "c": (2, ".XX X.. X.. X.. .XX"), "d": (0, "...X ...X .XXX X..X X..X X..X .XXX"),
    "e": (2, ".XX. X..X XXXX X... .XXX"), "f": (0, ".XX X.. XXX X.. X.. X.. X.."),
    "g": (2, ".XXX X..X X..X X..X .XXX ...X .XX."), "h": (0, "X... X... XXX. X..X X..X X..X X..X"),
    "i": (0, "X . X X X X X"), "j": (0, ".X .. .X .X .X .X .X .X X."),
    "k": (0, "X... X... X..X X.X. XX.. X.X. X..X"), "l": (0, "X X X X X X X"),
    "m": (2, "XX.X. X.X.X X.X.X X.X.X X.X.X"), "n": (2, "XXX. X..X X..X X..X X..X"),
    "o": (2, ".XX. X..X X..X X..X .XX."), "p": (2, "XXX. X..X X..X X..X XXX. X... X..."),
    "q": (2, ".XXX X..X X..X X..X .XXX ...X ...X"), "r": (2, "X.X XX. X.. X.. X.."),
    "s": (2, ".XXX X... .XX. ...X XXX."), "t": (1, ".X. XXX .X. .X. .X. ..X"),
    "u": (2, "X..X X..X X..X X..X .XXX"), "v": (2, "X...X X...X .X.X. .X.X. ..X.."),
    "w": (2, "X...X X...X X.X.X X.X.X .X.X."), "x": (2, "X.X X.X .X. X.X X.X"),
    "y": (2, "X..X X..X X..X X..X .XXX ...X .XX."), "z": (2, "XXXX ...X .XX. X... XXXX"),
    ".": (6, "X"), ",": (6, ".X X."), "'": (0, "X X"), "!": (0, "X X X X X . X"),
    "?": (0, ".XX. X..X ...X ..X. .X.. .... .X.."), "-": (4, "XXX"), ":": (3, "X . . X"),
}
INK = (44, 36, 56, 255)
ui = Image.new("RGBA", (96, 8 + 10 * 4), (0, 0, 0, 0))
for i, (rows, colour) in enumerate(ICONS):
    for y, row in enumerate(rows.split()):
        for x, ch in enumerate(row):
            if ch != ".":
                ui.putpixel((i * 14 + x, y), INK if ch == "o" else colour + (255,))
                ui.putpixel((i * 14 + 7 + x, y), (20, 24, 48, 120))
for i, (top, rows) in enumerate(GLYPHS.values()):
    for y, row in enumerate(rows.split()):
        for x, ch in enumerate(row):
            if ch == "X":
                ui.putpixel((i % 16 * 6 + x, 8 + i // 16 * 10 + top + y), INK)
save(ui, "ui", native=True)  # the game draws the meters and letters in units, so this sheet is not doubled
print("font order:", "".join(GLYPHS))

# Character: frames of 24x30 facing right, with the same frames mirrored in a second row.
# A hat brim, a nose, an eye, a scarf tail and a hand show which way it faces.
#   0-1 idle, 2-5 walk, 6-7 petting (arm out, hand moving), 8 picking something up, 9 wind-up, 10 throw
def person(d, ox, bob=0, legs="stand", arm="down", crouch=0, hat=True):
    """Drawn in half-frame units like the first version (U), then given detail in art pixels (P)."""
    ox *= S
    top = bob + crouch

    def U(x0, y0, x1, y1, name):
        d.rectangle([ox + x0 * 2, y0 * 2, ox + x1 * 2 + 1, y1 * 2 + 1], fill=c(name))

    def P(x0, y0, x1, y1, name):  # y is measured from the top of the body, so details bob with it
        d.rectangle([ox + x0, y0 + top * 2, ox + x1, y1 + top * 2], fill=c(name) if name else (0, 0, 0, 0))

    for a, b in {"stand": [(9, 11), (13, 15)], "stride": [(7, 9), (15, 17)], "pass": [(10, 12), (12, 14)],
                 "stride2": [(8, 10), (14, 16)]}[legs]:
        U(a, 22 + crouch, b, 29, "legs")
        d.rectangle([ox + a * 2, 55, ox + b * 2 + 3, 59], fill=c("log"))  # boots, toes forward
        d.line([ox + a * 2, 44 + crouch * 2, ox + a * 2, 54], fill=c("hat"))
    if hat:
        U(8, 1 + top, 15, 3 + top, "hat")
        P(18, 0, 29, 1, "hat")  # a rounded crown
        P(14, 8, 37, 9, "hat")  # the brim, longer in front
        P(16, 6, 31, 7, "legs")  # hat band
    U(9, 5 + top, 14, 9 + top, "skin")
    P(18, 10, 19, 17, "log")  # hair at the back
    P(30, 14, 31, 16, "skin")  # nose
    P(26, 12, 27, 14, "legs")  # eye
    P(22, 10, 29, 10, "log")  # the brim's shadow on the forehead
    P(20, 10, 21, 13, "log")  # hair down to the ear
    P(28, 18, 29, 19, None)  # chin
    P(18, 18, 19, 19, None)
    P(22, 17, 27, 17, "wall_light")  # shade under the cheek
    if hat:
        P(16, 2, 17, 3, None)  # a rounder crown
        P(30, 2, 31, 3, None)
        P(18, 2, 27, 2, "legs")  # the crown's crease
    else:
        P(18, 6, 29, 9, "log")  # a head of hair
        P(20, 5, 27, 5, "log")
    U(7, 12 + top, 16, 21 + crouch, "coat")
    d.rectangle([ox + 14, 24 + top * 2, ox + 16, 43 + crouch * 2], fill=c("coat_shade"))
    d.rectangle([ox + 14, 42 + crouch * 2, ox + 33, 43 + crouch * 2], fill=c("coat_shade"))
    P(28, 27, 29, 28, "scarf")  # buttons
    P(28, 34, 29, 35, "scarf")
    U(8, 10 + top, 15, 11 + top, "scarf")
    U(6, 11 + top, 6, 15 + top, "scarf")
    P(12, 32, 13, 34, "wall_light")  # fringe on the scarf tail
    P(16, 22, 31, 22, "wall_light")
    P(14, 24, 15, 25, None)  # rounded shoulders
    P(32, 24, 33, 25, None)
    P(18, 40, 33, 41, "log")  # belt
    P(26, 40, 27, 41, "scarf")
    if arm in ("down", "scratch1", "scratch2"):
        P(26, 26, 29, 39, "coat_shade")
        P(30, 26, 31, 39, "coat")
        U(15, 20 + top, 16, 21 + top, "skin")
    if arm in ("scratch1", "scratch2"):  # hat held at the hip, the other hand in the hair
        P(32, 38, 41, 43, "hat")
        P(29, 44, 44, 45, "hat")
        P(32, 42, 41, 43, "legs")
        h = 0 if arm == "scratch1" else 1
        U(5, 7 + top, 6, 13 + top, "coat_shade")
        U(6 + h, 4 + top - h, 8 + h, 5 + top - h, "skin")
    elif arm in ("up1", "up2"):  # a stretch: both arms overhead, then spread a little
        h = 0 if arm == "up1" else 1
        U(15 + h, 5 + top, 16 + h, 12 + top, "coat")
        U(15 + 2 * h, 3 + top, 16 + 2 * h, 4 + top, "skin")
        U(6 - h, 5 + top, 7 - h, 12 + top, "coat_shade")
        U(6 - 2 * h, 3 + top, 7 - 2 * h, 4 + top, "skin")
    elif arm in ("drink1", "drink2"):  # a bottle from the pack, raised to the mouth
        h = 0 if arm == "drink1" else 1
        U(15, 13 + top, 17, 14 + top, "coat")
        U(17, 10 + top - h, 18, 13 + top, "coat")
        U(17, 8 + top - h, 18, 9 + top - h, "skin")
        U(15, 6 + top - h, 16 + h, 8 + top - h, "tarp")
        U(15, 5 + top - h, 15 + h, 5 + top - h, "moon")
    elif arm == "lace2":
        U(18, 17 + top, 19, 22 + top, "coat")
        U(18, 23 + top, 19, 24 + top, "skin")
    elif arm in ("pet_up", "pet_down"):
        h = -1 if arm == "pet_up" else 0
        U(15, 12 + h, 19, 13 + h, "coat")
        d.line([ox + 30, 28 + h * 2, ox + 39, 28 + h * 2], fill=c("coat_shade"))
        U(20, 12 + h, 21, 13 + h, "skin")
    elif arm == "pick":
        U(17, 17 + top, 18, 22 + top, "coat")
        U(17, 23 + top, 18, 24 + top, "skin")
    elif arm == "back":
        U(3, 10 + top, 7, 11 + top, "coat")
        U(2, 8 + top, 3, 9 + top, "skin")
    elif arm == "throw":
        U(15, 14 + top, 20, 15 + top, "coat")
        U(21, 14 + top, 22, 15 + top, "skin")


POSES = [
    dict(), dict(bob=1),
    dict(legs="stride", bob=1), dict(legs="pass"), dict(legs="stride2", bob=1), dict(legs="pass"),
    dict(arm="pet_up"), dict(arm="pet_down"),
    dict(arm="pick", crouch=5), dict(arm="back", legs="stride2"), dict(arm="throw", legs="stride", bob=1),
    # Things to do when left alone: 11-12 a stretch, 13-14 hat off and a scratch, 15-16 a drink, 17-18 a lace.
    dict(arm="up1"), dict(arm="up2"),
    dict(arm="scratch1", hat=False), dict(arm="scratch2", hat=False),
    dict(arm="drink1"), dict(arm="drink2"),
    dict(arm="pick", crouch=5, legs="pass"), dict(arm="lace2", crouch=5, legs="pass"),
]


def both_ways(sheet, width, height, count):
    """Adds a second row with every frame mirrored, so the game never flips a sprite onto half pixels."""
    for f in range(count):
        frame = sheet.crop((f * width, 0, (f + 1) * width, height)).transpose(Image.FLIP_LEFT_RIGHT)
        sheet.paste(frame, (f * width, height))


sheet = Image.new("RGBA", (48 * len(POSES), 120), (0, 0, 0, 0))
d = ImageDraw.Draw(sheet)
for f, pose in enumerate(POSES):
    person(d, f * 24, **pose)
both_ways(sheet, 48, 60, len(POSES))
save(sheet, "character", native=True)

# The dog, facing right, 48x34 art pixels a frame, drawn from rounded shapes, with every frame mirrored
# in a second row. 0-1 sitting (tail down, tail up), 2-3 sitting and scratching an ear, 4-7 walking,
# 8-9 standing with its nose to the ground.
DOG_FRAMES = 10
sheet = Image.new("RGBA", (48 * DOG_FRAMES, 68), (0, 0, 0, 0))
d = ImageDraw.Draw(sheet)
for f in range(4):
    ox = f * 48

    def E(x0, y0, x1, y1, name):
        d.ellipse([ox + x0, y0, ox + x1, y1], fill=c(name))

    def P(x0, y0, x1, y1, name):
        d.rectangle([ox + x0, y0, ox + x1, y1], fill=c(name))

    if f != 1:  # tail resting on the ground, or up and curled
        P(1, 30, 9, 32, "dog_shade")
        P(1, 28, 3, 30, "dog_shade")
        P(1, 27, 2, 28, "dog")
    else:
        P(4, 22, 6, 31, "dog_shade")
        P(2, 16, 4, 23, "dog_shade")
        P(3, 14, 5, 16, "dog")
    E(5, 17, 24, 35, "dog")  # haunch
    P(5, 30, 24, 33, "dog")
    d.polygon([(ox + 10, 19), (ox + 26, 9), (ox + 33, 12), (ox + 33, 33), (ox + 10, 33)], fill=c("dog"))  # back and chest
    E(24, 12, 36, 28, "dog")  # chest
    E(6, 21, 19, 34, "dog_shade")  # the patch on the haunch
    P(6, 31, 19, 33, "dog_shade")
    P(12, 31, 23, 33, "dog")  # hind paw
    P(13, 33, 23, 33, "dog_shade")
    E(22, 0, 38, 15, "dog")  # head
    P(34, 7, 43, 13, "dog")  # muzzle
    P(35, 6, 41, 6, "dog")
    P(41, 7, 43, 9, "door")  # nose
    P(43, 7, 43, 7, "dog")
    P(36, 13, 41, 13, "dog_shade")  # mouth
    P(34, 4, 35, 6, "door")  # eye
    P(34, 4, 34, 4, "moon")
    d.polygon([(ox + 23, 3), (ox + 29, 1), (ox + 30, 10), (ox + 27, 15), (ox + 23, 13)], fill=c("dog_shade"))  # ear
    P(27, 2, 32, 2, "moon")  # light on the top of the head
    d.line([ox + 13, 17, ox + 23, 11], fill=c("moon"))  # light along the back
    P(26, 16, 35, 18, "coat")  # collar
    P(26, 19, 34, 19, "coat_shade")
    P(31, 19, 32, 21, "scarf")  # tag
    P(27, 20, 30, 33, "dog")  # front legs
    P(32, 22, 35, 33, "dog")
    P(31, 22, 31, 33, "dog_shade")
    P(26, 22, 26, 31, "dog_shade")
    P(27, 32, 37, 33, "dog")  # paws
    P(27, 33, 37, 33, "dog_shade")
    P(26, 24, 26, 28, "dog_shade")  # chest fluff
    P(36, 20, 36, 24, "dog_shade")
    if f >= 2:  # a hind leg up at the ear
        k = f - 2
        d.line([ox + 14, 24, ox + 23, 9 + k * 3], fill=c("dog"), width=3)
        P(22, 6 + k * 3, 25, 8 + k * 3, "dog_shade")
for f in range(4, DOG_FRAMES):
    ox = f * 48

    def E(x0, y0, x1, y1, name):
        d.ellipse([ox + x0, y0, ox + x1, y1], fill=c(name))

    def P(x0, y0, x1, y1, name):
        d.rectangle([ox + x0, y0, ox + x1, y1], fill=c(name))

    sniff = f >= 8
    step = (f - 4) % 4
    # Legs: the far pair in shade, the near pair light, swinging in opposite pairs.
    swing = [(-2, 2), (0, 0), (2, -2), (0, 0)][step] if not sniff else (0, 0)
    for base_x, sw, name in ((11, -swing[0], "dog_shade"), (29, -swing[1], "dog_shade"),
                             (8, swing[0], "dog"), (26, swing[1], "dog")):
        d.polygon([(ox + base_x, 22), (ox + base_x + 4, 22), (ox + base_x + 4 + sw, 32), (ox + base_x + sw, 32)], fill=c(name))
        P(base_x + sw, 32, base_x + 5 + sw, 33, name)
    E(5, 12, 33, 26, "dog")  # body
    E(9, 13, 22, 24, "dog_shade")  # the patch
    d.line([ox + 9, 13, ox + 28, 12], fill=c("moon"))  # light along the back
    if sniff:
        P(2, 12, 4, 20, "dog_shade")  # tail up, moving
        P(1 + (f - 8) * 2, 9, 3 + (f - 8) * 2, 12, "dog")
        d.polygon([(ox + 27, 13), (ox + 34, 15), (ox + 40, 26), (ox + 33, 28)], fill=c("dog"))  # neck, down
        P(28, 15, 33, 17, "coat")  # collar
        hx, hy = 31 + (f - 8), 20
    else:
        P(1, 13, 5, 15, "dog_shade")  # tail out behind
        P(0, 11 + step % 2, 2, 13 + step % 2, "dog")
        d.polygon([(ox + 26, 13), (ox + 33, 6), (ox + 38, 10), (ox + 34, 22)], fill=c("dog"))  # neck
        P(29, 12, 36, 14, "coat")  # collar
        P(32, 15, 33, 17, "scarf")
        hx, hy = 28, 0 + step % 2
    E(hx, hy, hx + 13, hy + 12, "dog")  # head
    P(hx + 10, hy + 6, hx + 18, hy + 11, "dog")  # muzzle
    P(hx + 16, hy + 6, hx + 18, hy + 8, "door")  # nose
    P(hx + 11, hy + 11, hx + 16, hy + 11, "dog_shade")
    P(hx + 9, hy + 3, hx + 10, hy + 5, "door")  # eye
    d.polygon([(ox + hx + 1, hy + 2), (ox + hx + 6, hy + 1), (ox + hx + 7, hy + 9), (ox + hx + 4, hy + 13), (ox + hx + 1, hy + 11)], fill=c("dog_shade"))  # ear
both_ways(sheet, 48, 34, DOG_FRAMES)
save(sheet, "dog", native=True)

# The campfire, in art pixels: crossed logs, then four frames of flame, 32x40 each. The first frame is
# the dormant one: logs under a little ash.
sheet = Image.new("RGBA", (32 * 5, 40), (0, 0, 0, 0))
d = ImageDraw.Draw(sheet)
rf = random.Random(11)
for f in range(5):
    ox = f * 32
    d.polygon([(ox + 4, 34), (ox + 6, 32), (ox + 27, 37), (ox + 26, 39), (ox + 5, 36)], fill=far("log"))
    d.polygon([(ox + 27, 34), (ox + 25, 32), (ox + 4, 37), (ox + 5, 39), (ox + 26, 36)], fill=far("log"))
    d.line([ox + 7, 33, ox + 16, 35], fill=far("trunk"))
    d.line([ox + 24, 33, ox + 17, 35], fill=far("trunk"))
    for sx in (3, 9, 22, 27):  # stones around it
        d.rectangle([ox + sx, 37, ox + sx + 3, 39], fill=far("ash"))
        d.point((ox + sx, 37), fill=(0, 0, 0, 0))
    if f == 0:
        d.rectangle([ox + 9, 33, ox + 22, 34], fill=far("ash"))
        d.rectangle([ox + 12, 31, ox + 19, 32], fill=far("ash"))
        continue
    sway = [0, 2, 0, -2][f - 1]
    tall = [26, 22, 28, 23][f - 1]
    for y in range(36 - tall, 36):  # a teardrop that leans as it rises, with a paler heart
        p = (36 - y) / tall  # 0 at the base, 1 at the tip
        half = 9.5 * math.sin(math.pi * min(1.0, 0.18 + p * 0.82) ** 0.75) * (1 - p * 0.35)
        cx = 15.5 + sway * p * p + 1.5 * math.sin(p * 7 + f * 1.7)
        for x in range(32):
            dist = abs(x + 0.5 - cx)
            if dist <= half * 0.42 and p < 0.62:
                sheet.putpixel((ox + x, y), far("core"))
            elif dist <= half:
                sheet.putpixel((ox + x, y), far("flame"))
    # a tongue licking off to one side, and sparks
    side = 1 if f % 2 else -1
    for k in range(5):
        sheet.putpixel((ox + 16 + side * (7 + k // 2), 22 - k * 2 - f % 2), far("flame"))
        sheet.putpixel((ox + 16 + side * (7 + k // 2), 23 - k * 2 - f % 2), far("flame"))
    for _ in range(3):
        sheet.putpixel((ox + rf.randint(8, 23), rf.randint(1, 36 - tall - 2)), far("flame"))
save(sheet, "fire", native=True)
print(f"{len(NAMES)} palette entries")
