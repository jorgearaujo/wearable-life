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

W, H = 240, 280
BANK, WATER = 196, 208  # top of the bank the character stands on; waterline
random.seed(11)

# name -> day colour. Order fixes the index (1-based; 0 is unused).
DAY = {
    "sky1": (86, 150, 214), "sky2": (112, 172, 224), "sky3": (146, 196, 232), "sky4": (182, 216, 236),
    "sky5": (214, 232, 236), "star": (86, 150, 214), "sun": (255, 246, 206),
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
        "sun": (255, 236, 190), "moon": (236, 240, 255), "moon_shade": (190, 202, 236),
    },
    "dawn": {
        "sky1": (96, 104, 168), "sky2": (150, 130, 186), "sky3": (214, 160, 188), "sky4": (246, 196, 184),
        "sky5": (252, 226, 190), "star": (96, 104, 168), "sun": (255, 236, 190), "halo1": (250, 208, 190),
        "halo2": (254, 226, 196), "window": (255, 214, 120),
        "moon": (236, 226, 236), "moon_shade": (214, 196, 222),
    },
    "day": {},
    "dusk": {
        "sky1": (72, 52, 120), "sky2": (128, 70, 136), "sky3": (196, 96, 132), "sky4": (240, 138, 116),
        "sky5": (252, 186, 128), "star": (72, 52, 120), "sun": (255, 214, 140), "halo1": (250, 160, 120),
        "halo2": (254, 190, 130), "window": (255, 214, 120),
        "moon": (244, 222, 226), "moon_shade": (216, 180, 204),
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


def save(img, name):
    img.save(f"assets/images/{name}.png")


def layer():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


# Sky: flat bands, a few stars and clouds. The sun and moon are their own pieces (below).
# The sky does not scroll, so everything sits in the first 120 columns.
sky, d = layer()
for i, top in enumerate([0, 44, 80, 112, 138]):
    d.rectangle([0, top, W, H], fill=far(f"sky{i + 1}"))
for _ in range(16):
    d.point([random.randint(2, 117), random.randint(2, 42)], fill=far("star"))
for cx, cy, w in [(26, 92, 22), (60, 120, 30), (104, 104, 14)]:
    d.ellipse([cx - w, cy - 4, cx + w, cy + 5], fill=far("cloud_shade"))
    d.ellipse([cx - w + 4, cy - 7, cx + w - 6, cy + 1], fill=far("cloud"))
    d.rectangle([cx - w, cy + 3, cx + w, cy + 5], fill=far("cloud_shade"))
save(sky, "sky")

# Sun with two flat halo rings, and a moon with no halo, each 35x35 so the game can move them.
sun = Image.new("RGBA", (35, 35), (0, 0, 0, 0))
d = ImageDraw.Draw(sun)
for r, name in [(17, "halo1"), (11, "halo2"), (6, "sun")]:
    d.ellipse([17 - r, 17 - r, 17 + r, 17 + r], fill=far(name))
save(sun, "sun")
moon = Image.new("RGBA", (35, 35), (0, 0, 0, 0))
# Drawn by hand: a computed circle this small comes out as an octagon, and computed craters as plus signs.
MOON = [
    "....#####....",
    "..#########..",
    ".###########.",
    ".##oo#######.",
    "###oo########",
    "##########o##",
    "#############",
    "#####oo######",
    "####ooo######",
    ".###oo###o##.",
    ".###########.",
    "..#########..",
    "....#####....",
]
for y, row in enumerate(MOON):
    for x, ch in enumerate(row):
        if ch != ".":
            moon.putpixel((11 + x, 11 + y), far("moon" if ch == "#" else "moon_shade"))
save(moon, "moon")

# Two ridges of far hills.
hills, d = layer()
for x in range(W):
    d.line([x, 150 + int(16 * math.sin(x / 31.0) + 6 * math.sin(x / 9.0 + 2)), x, H], fill=far("hill_far"))
for x in range(W):
    d.line([x, 172 + int(10 * math.sin(x / 23.0 + 4) + 4 * math.sin(x / 7.0)), x, H], fill=far("hill_near"))
save(hills, "hills")

# Trees: stacked wedges with light clusters on the sun side, a few golden ones.
trees, d = layer()
d.rectangle([0, 190, W, H], fill=c("tree"))
x = 4
while x < W:
    h = random.randint(34, 62)
    gold = random.random() < 0.25
    d.rectangle([x + 6, 184, x + 7, 192], fill=c("trunk"))
    for i in range(4):
        half = 3 + i * 3
        top = 190 - h + i * (h // 5)
        d.polygon([(x + 7, top), (x + 7 - half, top + h // 3), (x + 7 + half, top + h // 3)], fill=c("tree"))
        for _ in range(3 + i * 2):
            px = x + 7 + random.randint(0, half - 1)
            py = top + random.randint(h // 8, h // 3 - 1)
            if trees.getpixel((min(W - 1, px), py))[3]:
                d.line([px, py, px + random.randint(1, 2), py], fill=c("tree_gold" if gold else "tree_light"))
    x += random.randint(15, 24)
save(trees, "trees")

# The bank, a cabin and a dog. Everything below the waterline is replaced by the reflection.
ground, d = layer()
d.rectangle([0, BANK, W, H], fill=c("bank"))
d.rectangle([0, BANK, W, BANK + 1], fill=c("bank_top"))
d.rectangle([0, WATER - 4, W, H], fill=c("bank_face"))
for _ in range(40):
    x = random.randint(0, W - 2)
    d.line([x, BANK - random.randint(1, 3), x, BANK], fill=c("tuft"))
d.rectangle([50, BANK - 30, 96, BANK - 1], fill=c("wall"))
for y in range(BANK - 26, BANK, 6):
    d.line([50, y, 96, y], fill=c("wall_shade"))
d.polygon([(44, BANK - 30), (73, BANK - 50), (102, BANK - 30)], fill=c("roof"))
d.rectangle([58, BANK - 18, 67, BANK - 1], fill=c("door"))
d.rectangle([78, BANK - 22, 88, BANK - 13], fill=c("window", light=False))
d.line([83, BANK - 22, 83, BANK - 13], fill=c("wall_shade"))
dx, dy = 128, BANK - 17  # a large dog, sitting
d.rectangle([dx, dy + 6, dx + 12, dy + 16], fill=c("dog"))
d.rectangle([dx + 8, dy, dx + 16, dy + 8], fill=c("dog"))
d.rectangle([dx + 15, dy + 4, dx + 19, dy + 7], fill=c("dog"))
d.rectangle([dx + 8, dy, dx + 10, dy + 6], fill=c("dog_shade"))
d.rectangle([dx - 3, dy + 13, dx, dy + 15], fill=c("dog_shade"))
d.rectangle([dx, dy + 12, dx + 4, dy + 16], fill=c("dog_shade"))
d.point([dx + 14, dy + 3], fill=c("door"))
save(ground, "ground")

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
# Row 0: three meter icons, 7x7, each as filled then empty. Below: a small font, one glyph per 6x6 cell.
ICONS = [
    ("..ooo.. .oaao.. oaao... oaao... oaaoo.o .oaaao. ..ooo..", (236, 226, 160)),  # moon: Sleep
    ("...oo.. ..oao.. .oaaoo. oaaaao. .ooaao. ..oao.. ..oo...", (255, 176, 72)),   # spark: Energy
    (".oo.... oaao... oaao... oaaooo. oaaaaao oaaaaao .ooooo.", (150, 200, 120)),  # boot: Activity
]
GLYPHS = {
    "A": ".X. X.X XXX X.X X.X", "B": "XX. X.X XX. X.X XX.", "C": ".XX X.. X.. X.. .XX", "D": "XX. X.X X.X X.X XX.",
    "E": "XXX X.. XX. X.. XXX", "F": "XXX X.. XX. X.. X..", "G": ".XX X.. X.X X.X .XX", "H": "X.X X.X XXX X.X X.X",
    "I": "X X X X X", "J": "..X ..X ..X X.X .X.", "K": "X.X X.X XX. X.X X.X", "L": "X.. X.. X.. X.. XXX",
    "M": "X...X XX.XX X.X.X X...X X...X", "N": "X..X XX.X X.XX X..X X..X", "O": ".X. X.X X.X X.X .X.",
    "P": "XX. X.X XX. X.. X..", "Q": ".X. X.X X.X XXX .XX", "R": "XX. X.X XX. X.X X.X", "S": ".XX X.. .X. ..X XX.",
    "T": "XXX .X. .X. .X. .X.", "U": "X.X X.X X.X X.X XXX", "V": "X.X X.X X.X X.X .X.",
    "W": "X...X X...X X.X.X XX.XX X...X", "X": "X.X X.X .X. X.X X.X", "Y": "X.X X.X .X. .X. .X.",
    "Z": "XXX ..X .X. X.. XXX", ".": ". . . . X", ",": ".. .. .. .X X.", "'": "X X . . .", "!": "X X X . X",
    "?": "XX. ..X .X. ... .X.", "-": "... ... XXX ... ...", ":": ". X . X .",
}
INK = (44, 36, 56, 255)
ui = Image.new("RGBA", (96, 8 + 6 * 3), (0, 0, 0, 0))
for i, (rows, colour) in enumerate(ICONS):
    for y, row in enumerate(rows.split()):
        for x, ch in enumerate(row):
            if ch != ".":
                ui.putpixel((i * 14 + x, y), INK if ch == "o" else colour + (255,))
                ui.putpixel((i * 14 + 7 + x, y), (20, 24, 48, 120))
for i, rows in enumerate(GLYPHS.values()):
    for y, row in enumerate(rows.split()):
        for x, ch in enumerate(row):
            if ch == "X":
                ui.putpixel((i % 16 * 6 + x, 8 + i // 16 * 6 + y), INK)
save(ui, "ui")
print("font order:", "".join(GLYPHS))

# Character: 4 frames of 16x30, a small idle bob. A hat and a scarf carry the identity; no drawn eyes.
sheet = Image.new("RGBA", (64, 30), (0, 0, 0, 0))
d = ImageDraw.Draw(sheet)
for f, bob in enumerate([0, 1, 1, 0]):
    ox = f * 16
    d.rectangle([ox + 4, 1 + bob, ox + 11, 3 + bob], fill=c("hat"))
    d.rectangle([ox + 3, 4 + bob, ox + 12, 4 + bob], fill=c("hat"))
    d.rectangle([ox + 5, 5 + bob, ox + 10, 9 + bob], fill=c("skin"))
    d.rectangle([ox + 4, 10 + bob, ox + 11, 11 + bob], fill=c("scarf"))
    d.rectangle([ox + 3, 12 + bob, ox + 12, 21], fill=c("coat"))
    d.rectangle([ox + 3, 12 + bob, ox + 4, 19], fill=c("scarf") if f == 3 else c("coat"))
    d.rectangle([ox + 5, 22, ox + 7, 29], fill=c("legs"))
    d.rectangle([ox + 9, 22, ox + 11, 29], fill=c("legs"))
save(sheet, "character")
print(f"{len(NAMES)} palette entries")
