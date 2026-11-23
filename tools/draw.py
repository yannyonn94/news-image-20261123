#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news poster (1024x1024 PNG).

Concept (winner): a storm-wrapped globe split between two named stories
with numbers, under the biggest element on the page - the date
MONDAY 23 NOVEMBER 2026. Drawn entirely with PIL; no stock photos.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def text_center(d, y, s, f, fill):
    w = d.textlength(s, font=f)
    d.text(((W - w) / 2, y), s, font=f, fill=fill)
    return y + f.size

def wrap(d, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

img = Image.new("RGB", (W, H), (8, 22, 44))
d = ImageDraw.Draw(img, "RGBA")
# vertical gradient: deep navy -> dark teal
for y in range(H):
    t = y / H
    r = int(8 + (10 - 8) * t)
    g = int(22 + (58 - 22) * t)
    b = int(44 + (92 - 44) * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))
# faint stars / dots
import random
random.seed(23112026)
for _ in range(90):
    x, y = random.randint(0, W - 1), random.randint(0, 300)
    d.ellipse([x, y, x + 2, y + 2], fill=(255, 255, 255, 40))

AMBER = (255, 176, 32)
WHITE = (255, 255, 255)
MUTED = (180, 205, 230)
ORANGE = (255, 122, 26)
RED = (255, 72, 72)
TEAL = (46, 196, 182)

# ---- date block: the biggest element on the page ----
y = 34
text_center(d, y, "THE WORLD TODAY  •  MONDAY", font(BOLD, 34), AMBER)
y = 84
text_center(d, y, "23 NOVEMBER", font(BOLD, 122), WHITE)
y = 208
text_center(d, y, "2026", font(BOLD, 122), AMBER)
d.line([(90, 340), (934, 340)], fill=(255, 176, 32, 200), width=4)

# ---- storm-wrapped globe, centre ----
cx, cy, R = 512, 462, 100
d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(24, 96, 160))
d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(140, 200, 240), width=5)
# abstract continents
d.ellipse([cx - 78, cy - 62, cx - 8, cy + 6], fill=(58, 160, 90))
d.ellipse([cx + 6, cy + 8, cx + 74, cy + 66], fill=(58, 160, 90))
d.ellipse([cx - 20, cy - 88, cx + 44, cy - 40], fill=(84, 178, 110))
# storm swirl arcs (white)
for r, a0, a1 in [(128, 200, 330), (146, 20, 160), (118, 300, 60)]:
    d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=(255, 255, 255, 220), width=7)
# lightning crack splitting the globe
d.line([(cx - 6, cy - R - 14), (cx + 14, cy - 30), (cx - 10, cy + 6),
        (cx + 12, cy + 46), (cx - 2, cy + R + 14)], fill=AMBER, width=7, joint="curve")

# ---- two story panels ----
def panel(x0, x1, y0, y1, accent, chip, big, headline, summary):
    d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=(13, 38, 66, 255),
                        outline=accent, width=3)
    d.rounded_rectangle([x0, y0, x1, y0 + 14], radius=7, fill=accent)
    f_chip = font(BOLD, 27)
    d.text((x0 + 26, y0 + 30), chip, font=f_chip, fill=accent)
    f_big = font(BOLD, 96)
    d.text((x0 + 24, y0 + 62), big, font=f_big, fill=WHITE)
    f_head = font(BOLD, 38)
    lines = wrap(d, headline, f_head, x1 - x0 - 52)
    hy = y0 + 172
    for ln in lines:
        d.text((x0 + 26, hy), ln, font=f_head, fill=WHITE)
        hy += 46
    f_sum = font(REG, 25)
    slines = wrap(d, summary, f_sum, x1 - x0 - 52)
    sy = hy + 8
    for ln in slines:
        d.text((x0 + 26, sy), ln, font=f_sum, fill=MUTED)
        sy += 33

panel(36, 500, 600, 950, ORANGE, "CLIMATE  •  ANTALYA",
      "0", "COP31 COLLAPSES",
      "No deal in Antalya — the final draft never mentions fossil fuels.")
panel(524, 988, 600, 950, RED, "INDONESIA  •  BANTEN",
      "24", "FACTORY FIRE",
      "Body bags recovered from a candy factory blaze; search resumes Monday.")

# ---- footer ----
text_center(d, 968, "AS REPORTED  •  REUTERS  •  XINHUA  •  23 NOV 2026",
            font(BOLD, 22), (140, 170, 200))

img.save("/home/hatch/news-image-20261123/entry.png", "PNG", optimize=True)
print("saved")
