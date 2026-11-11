#!/usr/bin/env python3
"""Capsule concepts, as mock-ups to compare before any of them replaces the shipped set
(lesson 5 from Mancalero: settle visuals on mock-ups; lesson 2: the hook must read from the
thumbnail). Each concept keeps to a few ideas and shows that the game is a deckbuilder.

    python3 tools/capsule_lab.py        writes lab/capsules/<concept>-header.png, -small.png
                                        and lab/capsules/sheet.png (all of them, at Steam's
                                        real sizes, with the small ones at list size)

Backdrops are drawn with tools/scene.py's own pieces; cards are the game's cut-paper cards
(lab/cards/*.png, copied from the game repo); the name is the shipped logo; the border is
brand.frame(). Rasterised with the Node Playwright that is on the PATH (tools/raster.js).
"""
import os, sys, subprocess, json
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene as S
import brand

ROOT = brand.ROOT
OUT = os.path.join(ROOT, "lab", "capsules")
TMP = os.path.join(ROOT, "tools", ".out")
W, H = S.W, S.H


def defs():
    full = S.scene()
    return full[:full.index("</defs>") + len("</defs>")]


def backdrop(extra, mid=None):
    """Sky, sun glow, stars and the four hill lines only: no flock, fold, cave or wolf."""
    import random
    rnd = random.Random(11)
    d = [defs(), f'<rect width="{W}" height="{H}" fill="url(#sky)"/><rect width="{W}" height="{H}" fill="url(#skyv)"/>']
    for _ in range(70):
        sx, sy = rnd.uniform(2350, W - 20), rnd.uniform(30, 1250)
        d.append(f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{rnd.choice([3, 4, 5, 7])}" fill="{S.PAPER}" opacity="{rnd.uniform(0.35, 0.95) * min(1.0, (sx - 2300) / 500):.2f}"/>')
    d.append(f'<circle cx="1050" cy="1000" r="620" fill="url(#sunglow)"/>')
    d.append(S.hill(1, [(0, 1250), (520, 1130), (1100, 1230), (1700, 1100), (2300, 1200), (2900, 1060), (3400, 1160), (W, 1100)]))
    d.append(S.hill(2, [(0, 1430), (600, 1330), (1300, 1440), (1900, 1350), (2600, 1450), (3200, 1330), (W, 1420)]))
    d.append(S.hill(3, [(0, 1640), (500, 1540), (1200, 1650), (1900, 1560), (2500, 1660), (3100, 1560), (W, 1640)]))
    d.append(extra)
    d.append("</svg>")
    return "".join(d)


def eyes(x, y, s=1.0):
    return "".join(f'<ellipse cx="{x + dx * s:.0f}" cy="{y}" rx="{20 * s:.0f}" ry="{8 * s:.0f}" fill="#ffd36b"/>' for dx in (-30, 30))


# Each concept: the backdrop's extras, then per format the crop of the 3840x2160 backdrop
# (x, y, height; width follows the format), the logo box and the cards (file, centre x, centre y,
# height, tilt in degrees), all as fractions of the capsule.
CONCEPTS = {
    # A. He fills the left of the frame with the lamb; his hand of cards is fanned on the night side.
    "a-shepherd-and-hand": {
        "say": "Shepherd + a hand of cards",
        "extra": f'<ellipse cx="2030" cy="1500" rx="900" ry="620" fill="url(#lampspill)"/>' + S.shepherd(2030, 1960, 1.0) + eyes(3050, 1500, 0.9) + eyes(3260, 1420, 0.6),
        "header": {"crop": (1560, 905, 800), "logo": (0.50, 0.05, 0.47, 0.50), "which": "stack",
                   "cards": [("staff", 0.585, 0.93, 0.62, -13), ("bond", 0.74, 0.86, 0.66, 0), ("rod", 0.895, 0.93, 0.62, 13)]},
        "small": {"crop": (1700, 930, 620), "logo": (0.30, 0.08, 0.50, 0.84), "which": "line",
                  "cards": [("bond", 0.905, 0.62, 1.05, 8)]},
    },
    # A, brighter: he stands in full daylight; the night is only the right-hand third, behind the name and the cards.
    "a2-shepherd-in-daylight": {
        "say": "A, with the day carried further across",
        "extra": f'<ellipse cx="1500" cy="1500" rx="900" ry="620" fill="url(#lampspill)"/>' + S.cloud(1050, 1010, 0.8) + S.shepherd(1500, 1960, 1.0),
        "header": {"crop": (1030, 905, 800), "logo": (0.50, 0.05, 0.47, 0.50), "which": "stack",
                   "cards": [("staff", 0.585, 0.93, 0.62, -13), ("bond", 0.74, 0.86, 0.66, 0), ("rod", 0.895, 0.93, 0.62, 13)]},
        "small": {"crop": (1170, 930, 620), "logo": (0.30, 0.08, 0.50, 0.84), "which": "line",
                  "cards": [("bond", 0.905, 0.62, 1.05, 8)]},
    },
    # D. The game's own 3D sheep (tools/trailer/pose_sheep.gd in the game repo) in daylight, with the 2D cards.
    "d-3d-sheep-2d-cards": {
        "say": "3D sheep from the game, 2D cards",
        "extra": S.cloud(1150, 1010, 0.8),
        "header": {"crop": (760, 905, 860), "logo": (0.50, 0.05, 0.47, 0.50), "which": "stack",
                   "models": [("sheep-left", 0.085, 0.60, 0.50, 0.75), ("sheep-right", 0.27, 0.56, 0.86, 1.0)],
                   "cards": [("staff", 0.585, 0.93, 0.62, -13), ("bond", 0.74, 0.86, 0.66, 0), ("rod", 0.895, 0.93, 0.62, 13)]},
        "small": {"crop": (900, 1000, 640), "logo": (0.33, 0.08, 0.48, 0.84), "which": "line",
                  "models": [("sheep-right", 0.17, 0.54, 0.98, 1.0)],
                  "cards": [("bond", 0.905, 0.62, 1.05, 8)]},
    },
}
SIZES = {"header": (920, 430), "small": (462, 174)}


def raster(jobs):
    os.makedirs(TMP, exist_ok=True)
    spec = []
    for name, svg in jobs:
        path = os.path.join(TMP, name + ".svg")
        open(path, "w").write(svg)
        spec.append({"svg": path, "png": os.path.join(TMP, name + ".png"), "w": W, "h": H})
    subprocess.run(["node", os.path.join(ROOT, "tools", "raster.js"), json.dumps(spec)], check=True)


def card(name, height, tilt):
    im = Image.open(os.path.join(ROOT, "lab", "cards", name + ".png")).convert("RGBA")
    im = im.resize((int(im.width * height / im.height), int(height)), Image.LANCZOS)
    return im.rotate(-tilt, resample=Image.BICUBIC, expand=True)


def build(key, fmt):
    c = CONCEPTS[key]
    w, h = SIZES[fmt]
    f = c[fmt]
    x0, y0, ch = f["crop"]
    cw = ch * w / h
    art = Image.open(os.path.join(TMP, key + ".png")).convert("RGB").crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.LANCZOS).convert("RGBA")
    for name, cx, cy, ht, light in f.get("models", []):   # 3D cut-outs: centre x, centre y, height, brightness
        m = Image.open(os.path.join(ROOT, "lab", "models", name + ".png")).convert("RGBA")
        m = m.resize((int(m.width * ht * h / m.height), int(ht * h)), Image.LANCZOS)
        if light != 1.0:
            from PIL import ImageEnhance
            r, g, b2, al = m.split()
            m = Image.merge("RGBA", (*ImageEnhance.Brightness(Image.merge("RGB", (r, g, b2))).enhance(light).split(), al))
        # a soft shadow on the ground under her, and a faint one behind
        sh = Image.new("RGBA", art.size, (0, 0, 0, 0))
        from PIL import ImageDraw
        gx, gy = cx * w, cy * h + m.height * 0.47
        ImageDraw.Draw(sh).ellipse((gx - m.width * 0.42, gy - m.height * 0.05, gx + m.width * 0.42, gy + m.height * 0.05), fill=(30, 22, 40, 110))
        art.alpha_composite(sh.filter(ImageFilter.GaussianBlur(h * 0.012)))
        art.alpha_composite(m, (int(cx * w - m.width / 2), int(cy * h - m.height / 2)))
    for name, cx, cy, ht, tilt in f["cards"]:
        cd = card(name, ht * h, tilt)
        art.alpha_composite(cd, (int(cx * w - cd.width / 2), int(cy * h - cd.height / 2)))
    lx, ly, lw, lh = f["logo"]
    logo = Image.open(os.path.join(brand.B, "logo", "logo-stacked-1280x720.png" if f["which"] == "stack" else "logo-one-line-1500x330.png")).convert("RGBA")
    lg = brand.fit_logo(logo, lw * w, lh * h)
    art.alpha_composite(lg, (int(lx * w + (lw * w - lg.width) / 2), int(ly * h + (lh * h - lg.height) / 2)))
    art = brand.frame(art, 1.25 if fmt == "small" else 1.0).convert("RGB")
    art.save(os.path.join(OUT, f"{key}-{fmt}.png"))
    return art


def main():
    os.makedirs(OUT, exist_ok=True)
    raster([(k, backdrop(c["extra"])) for k, c in CONCEPTS.items()])
    now = [Image.open(os.path.join(brand.B, "steam", n)).convert("RGB") for n in ("header-capsule-920x430.png", "small-capsule-462x174.png")]
    rows = []
    for k, c in CONCEPTS.items():
        rows.append((k, c["say"], build(k, "header"), build(k, "small")))
    # the sheet: header at full size, the small capsule at full size and at the 231 px Steam uses in lists
    sheet = Image.new("RGB", (920 + 30 + 462 + 30 + 231 + 40, len(rows) * 460 + 20), (27, 40, 56))   # Steam's own dark blue
    for i, (_k, _say, head, small) in enumerate(rows):
        y = 20 + i * 460
        sheet.paste(head, (20, y))
        sheet.paste(small, (970, y))
        sheet.paste(small.resize((231, 87), Image.LANCZOS), (970, y + 200))
        sheet.paste(head.resize((231, 108), Image.LANCZOS), (1220, y + 200))
    sheet.save(os.path.join(OUT, "sheet.png"))


if __name__ == "__main__":
    main()
