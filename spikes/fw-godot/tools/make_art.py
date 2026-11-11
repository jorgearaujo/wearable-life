#!/usr/bin/env python3
"""Placeholder pixel art for the framework spike. Run from the spike folder: python3 tools/make_art.py"""
import math
import random
from PIL import Image, ImageDraw

W, H, GROUND = 360, 480, 380
random.seed(7)


def save(img, name):
    img.save(f"art/{name}.png")


# Sky: banded vertical gradient, no smoothing.
sky = Image.new("RGBA", (W, H))
d = ImageDraw.Draw(sky)
bands = [(96, 160, 216), (120, 180, 224), (150, 200, 232), (184, 220, 236), (214, 234, 236), (236, 240, 226)]
for i, c in enumerate(bands):
    d.rectangle([0, i * H // len(bands), W, (i + 1) * H // len(bands)], fill=c)
d.ellipse([120, 110, 148, 138], fill=(255, 244, 200))
save(sky, "sky")

# Far hills.
hills = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(hills)
for x in range(W):
    y = 300 + int(22 * math.sin(x / 38.0) + 10 * math.sin(x / 13.0 + 1))
    d.line([x, y, x, H], fill=(122, 158, 150))
save(hills, "hills")

# Mid trees.
trees = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(trees)
d.rectangle([0, 356, W, H], fill=(70, 112, 84))
for x in range(6, W, 26):
    h = random.randint(40, 78)
    x += random.randint(-5, 5)
    d.rectangle([x + 6, 356 - 12, x + 8, 360], fill=(84, 62, 52))
    for i in range(4):
        w = 3 + i * 3
        top = 356 - h + i * (h // 5)
        d.polygon([(x + 7, top), (x + 7 - w, top + h // 3), (x + 7 + w, top + h // 3)], fill=(52, 96, 74))
save(trees, "trees")

# Ground with a cabin and grass tufts.
ground = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(ground)
d.rectangle([0, GROUND, W, H], fill=(96, 140, 80))
d.rectangle([0, GROUND, W, GROUND + 2], fill=(128, 172, 96))
d.rectangle([0, GROUND + 40, W, H], fill=(78, 118, 70))
for _ in range(120):
    x, y = random.randint(0, W - 2), random.randint(GROUND + 4, H - 4)
    d.line([x, y, x, y - 2], fill=(140, 184, 104))
d.rectangle([60, GROUND - 34, 110, GROUND], fill=(132, 92, 66))
d.polygon([(54, GROUND - 34), (85, GROUND - 58), (116, GROUND - 34)], fill=(110, 60, 56))
d.rectangle([80, GROUND - 18, 90, GROUND], fill=(84, 56, 44))
d.rectangle([96, GROUND - 26, 104, GROUND - 18], fill=(250, 220, 130))
save(ground, "ground")

# Character: 4 frames of 16x24, a small idle bob.
sheet = Image.new("RGBA", (64, 24), (0, 0, 0, 0))
d = ImageDraw.Draw(sheet)
for f, bob in enumerate([0, 1, 1, 0]):
    ox = f * 16
    d.rectangle([ox + 5, 3 + bob, ox + 10, 8 + bob], fill=(238, 200, 164))   # head
    d.rectangle([ox + 5, 2 + bob, ox + 10, 3 + bob], fill=(90, 60, 50))      # hair
    d.rectangle([ox + 4, 9 + bob, ox + 11, 17], fill=(196, 84, 72))          # coat
    d.rectangle([ox + 5, 18, ox + 7, 23], fill=(60, 64, 96))                 # legs
    d.rectangle([ox + 9, 18, ox + 10, 23], fill=(60, 64, 96))
    if f == 2:
        d.point([ox + 6, 5 + bob], fill=(40, 30, 30))                        # blink frame has one eye
    else:
        d.point([ox + 6, 5 + bob], fill=(40, 30, 30))
        d.point([ox + 9, 5 + bob], fill=(40, 30, 30))
save(sheet, "character")

drop = Image.new("RGBA", (1, 5), (200, 220, 255, 200))
save(drop, "drop")
