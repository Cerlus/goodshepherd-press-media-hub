#!/usr/bin/env python3
"""Drafts for a crisper capsule (2026-11-28): bolder day-to-night colour, no cream frame, a
larger title with a strong dark outline, and the same outline round the shepherd and the cards.
Writes lab/capsules/drafts/<name>-main.png, -small.png and sheet.png. Nothing here ships.

    python3 tools/capsule_drafts.py
"""
import os, sys, subprocess, json
from PIL import Image, ImageFilter, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene as S
import brand
import capsule_lab as L

ROOT = brand.ROOT
OUT = os.path.join(ROOT, "lab", "capsules", "drafts")
TMP = os.path.join(ROOT, "tools", ".out")
W, H = S.W, S.H
EDGE = (27, 18, 64)            # the outline: deep night indigo, not ink brown or cream
K = 2                          # supersample

# bolder paper: the same day-to-night run, more colour in it, crisper cut shadows
BOLD = {"#a9cde2": "#4fb4ee", "#d9e6dc": "#a8def4", "#f6dca4": "#ffe9b8", "#e79a6c": "#b9a0e6", "#7a4f86": "#5a45b0",   # (day blue, a pale gold at the turn, then dusk violet: no orange-pink sunset)
        "#2f2558": "#2c1f7a", "#151030": "#130c40",
        "#c6dcc8": "#a8e09a", "#a3c394": "#7dd072", "#84ab72": "#52b955", "#6f995f": "#35a04a", "#c9804a": "#cf7a3c",
        "#4b3f78": "#4a3aa6", "#3a2f62": "#372a86", "#2c2450": "#281d68", "#221b40": "#1c144e", "#191430": "#140e36",
        'stdDeviation="12" flood-color="#150e1e" flood-opacity=".3"': 'stdDeviation="5" flood-color="#150e1e" flood-opacity=".45"'}


def bold(svg):
    for a, b in BOLD.items():
        svg = svg.replace(a, b)
    return svg


def title_svg(style):
    """The name, large: Bree Serif, a thick night-indigo outline, a solid drop under it.
    'sweep': the letters themselves run sun-gold to moon-blue. 'cream': cream letters on a
    day-to-night sheet. Optional plain crook under it."""
    w, h = 1700, 900
    edge = "#1b1240"
    g = (f'<defs><linearGradient id="dn" gradientUnits="userSpaceOnUse" x1="120" y1="0" x2="1580" y2="0"><stop offset="0" stop-color="#ffd84a"/>'
         f'<stop offset=".34" stop-color="#ff9a3c"/><stop offset=".58" stop-color="#f0569a"/><stop offset=".8" stop-color="#8f6cf2"/><stop offset="1" stop-color="#9fd0ff"/></linearGradient>'
         f'<linearGradient id="hi" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>')
    def line(txt, y, size):
        a = f'x="{w/2}" y="{y}" font-size="{size}" text-anchor="middle"'
        o = f'<text {a} transform="translate(0,{size*0.075:.1f})" fill="{edge}" stroke="{edge}" stroke-width="{size*0.17:.1f}">{txt}</text>'
        o += f'<text {a} fill="{edge}" stroke="{edge}" stroke-width="{size*0.17:.1f}">{txt}</text>'
        if style == "cream":
            o += f'<text {a} transform="translate(0,{size*0.03:.1f})" fill="url(#dn)" stroke="url(#dn)" stroke-width="{size*0.085:.1f}">{txt}</text>'
            o += f'<text {a} fill="#fffbe9">{txt}</text>'
        else:
            o += f'<text {a} fill="#fffbe9" stroke="#fffbe9" stroke-width="{size*0.055:.1f}">{txt}</text>'
            o += f'<text {a} fill="url(#dn)">{txt}</text><text {a} fill="url(#hi)">{txt}</text>'
        return o
    g += line("Good", 330, 300) + line("Shepherd", 660, 330)
    if style == "crook":
        pass
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{brand.STYLE}{g}</svg>', w, h


def raster(jobs):
    os.makedirs(TMP, exist_ok=True)
    spec = []
    for name, svg, w, h in jobs:
        p = os.path.join(TMP, name + ".svg")
        open(p, "w").write(svg)
        spec.append({"svg": p, "png": os.path.join(TMP, name + ".png"), "w": w, "h": h})
    subprocess.run(["node", os.path.join(ROOT, "tools", "raster.js"), json.dumps(spec)], check=True)


def outlined(im, r, col=EDGE):
    """The picture on a round-cornered backing sheet r px wider than itself (a sticker edge)."""
    pad = int(r * 3)
    big = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
    big.alpha_composite(im, (pad, pad))
    a = big.split()[3].filter(ImageFilter.GaussianBlur(r * 0.6)).point(lambda v: 255 if v > 40 else 0).filter(ImageFilter.GaussianBlur(0.8))
    back = Image.new("RGBA", big.size, col + (255,))
    back.putalpha(a)
    back.alpha_composite(big)
    return back, pad


def shadow(layer, dy, blur, op):
    a = layer.split()[3].point(lambda v: int(v * op))
    sh = Image.new("RGBA", layer.size, (14, 8, 30, 255))
    sh.putalpha(a)
    out = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (0, int(dy)))
    return out


def band_frame(art, u):
    """A slim frame in bold colour: the day-to-night run with an indigo hairline inside it."""
    w, h = art.size
    cols = [(245, 181, 58), (245, 181, 58), (245, 181, 58), (143, 155, 245), (143, 155, 245), (143, 155, 245)]   # flipped to contrast: night indigo on the day side, gold on the night side;   # the title's two papers: day gold, night blue
    g = Image.new("RGB", (len(cols), 1)); g.putdata(cols)
    g = g.resize((w, h), Image.BILINEAR).convert("RGBA")
    m = Image.new("L", (w, h), 255)
    ImageDraw.Draw(m).rounded_rectangle((u, u, w - u, h - u), radius=u * 1.6, fill=0)
    out = art.copy()
    line = Image.new("L", (w, h), 0)
    ImageDraw.Draw(line).rounded_rectangle((u * 0.72, u * 0.72, w - u * 0.72, h - u * 0.72), radius=u * 1.9, outline=255, width=max(2, int(u * 0.3)))
    out.paste(g, (0, 0), m)
    out.paste(Image.new("RGBA", (w, h), EDGE + (255,)), (0, 0), line)   # a cream keyline inside the band, so the dark half still reads as an edge
    return out


# name: title style, frame, then per format: crop (x, y, height), shepherd on/off is the crop's,
# title box (x, y, w, h) and cards (file, cx, cy, height, tilt), as fractions of the capsule
DRAFTS = {
    "D-blend": {"say": "The blended logo (lab/logos/6-blend.png), a gold-to-blue outline round the capsule", "title": "blend", "frame": True},
}
FORMATS = {
    "main": {"size": (1232, 706), "crop": (980, 735, 900), "logo": (0.488, 0.04, 0.495, 0.54),
             "cards": [("staff", 0.585, 0.97, 0.56, -13), ("rod", 0.895, 0.97, 0.56, 13), ("bond", 0.74, 0.91, 0.60, 0)]},
    "small": {"size": (462, 174), "crop": (1215, 690, 760), "logo": (0.31, 0.03, 0.66, 0.94), "cards": []},
}


def build(name, fmt, bg, man, logos):
    d, f = DRAFTS[name], FORMATS[fmt]
    w, h = f["size"]
    x0, y0, ch = f["crop"]
    cw = ch * w / h
    box = (int(x0), int(y0), int(x0 + cw), int(y0 + ch))
    art = bg.crop(box).resize((w * K, h * K), Image.LANCZOS).convert("RGBA")
    layers = [("1-sky-and-hills", art.copy())]
    def stamp(label, im, at):
        art.alpha_composite(im, at)
        full = Image.new("RGBA", art.size, (0, 0, 0, 0))
        full.alpha_composite(im, at) if min(at) >= 0 else full.alpha_composite(im.crop((-at[0], -at[1], im.width, im.height)).crop((0, 0, art.width, art.height)))
        layers.append((label, full))
    r = max(3.0, h * 0.0085) * K
    m, pad = outlined(man.crop(box).resize((w * K, h * K), Image.LANCZOS), r)
    stamp("2-shepherd-shadow", shadow(m, r * 1.2, r * 0.9, 0.45), (-pad, -pad))
    stamp("3-shepherd", m, (-pad, -pad))
    for cname, cx, cy, ht, tilt in f["cards"]:
        cd, p = outlined(L.card(cname, ht * h * K, tilt), r * 0.8)
        at = (int(cx * w * K - cd.width / 2), int(cy * h * K - cd.height / 2))
        stamp(f"4-card-{cname}-shadow", shadow(cd, r * 1.4, r, 0.5), at)
        stamp(f"5-card-{cname}", cd, at)
    lx, ly, lw, lh = f["logo"]
    lg = brand.fit_logo(logos[d["title"]], lw * w * K, lh * h * K)
    at = (int(lx * w * K + (lw * w * K - lg.width) / 2), int(ly * h * K + (lh * h * K - lg.height) / 2))
    if d["title"] != "blend":   # (the blended logo carries its own shadow)
        stamp("6-title-shadow", shadow(lg, r * 1.5, r * 1.2, 0.5), at)
    stamp("7-title", lg, at)
    if "--layers" in sys.argv and fmt == "main":
        ld = os.path.join(OUT, name + "-layers"); os.makedirs(ld, exist_ok=True)
        for label, im in layers:
            im.resize((w, h), Image.LANCZOS).save(os.path.join(ld, label + ".png"))
    if d["frame"]:
        art = band_frame(art, max(3.0, h * 0.013) * K * (1.3 if fmt == "small" else 1.0))
    art = art.resize((w, h), Image.LANCZOS).convert("RGB")
    art.save(os.path.join(OUT, f"{name}-{fmt}.png"))
    return art


def main():
    os.makedirs(OUT, exist_ok=True)
    extra = f'<ellipse cx="1500" cy="1500" rx="900" ry="620" fill="url(#lampspill)"/>' + S.cloud(1050, 1010, 0.8) + S.cloud(700, 620, 1.0)
    jobs = [("d_bg", bold(L.backdrop(extra)), W, H),
            ("d_man", bold(L.defs() + S.shepherd(1500, 1960, 1.0, "upright") + "</svg>"), W, H)]
    for st in ("sweep", "cream"):
        s, tw, th = title_svg(st)
        jobs.append(("d_title_" + st, s, tw, th))
    raster(jobs)
    bg = Image.open(os.path.join(TMP, "d_bg.png")).convert("RGB")
    man = Image.open(os.path.join(TMP, "d_man.png")).convert("RGBA")
    logos = {st: Image.open(os.path.join(TMP, f"d_title_{st}.png")).convert("RGBA") for st in ("sweep", "cream")}
    logos["blend"] = Image.open(os.path.join(ROOT, "lab", "logos", "6-blend.png")).convert("RGBA")
    made = {n: {f: build(n, f, bg, man, logos) for f in FORMATS} for n in DRAFTS}
    cur = Image.open(os.path.join(brand.B, "steam", "main-capsule-1232x706.png")).convert("RGB")
    curs = Image.open(os.path.join(brand.B, "steam", "small-capsule-462x174.png")).convert("RGB")
    sheet = Image.new("RGB", (1232 * 2 + 60, (706 + 174 + 50) * ((len(DRAFTS) + 2) // 2) + 20), (27, 40, 56))
    cells = [("current", cur, curs)] + [(n, made[n]["main"], made[n]["small"]) for n in DRAFTS]
    for i, (n, mn, sm) in enumerate(cells):
        x, y = 20 + (i % 2) * 1252, 20 + (i // 2) * 930
        sheet.paste(mn, (x, y)); sheet.paste(sm, (x, y + 716)); sheet.paste(sm.resize((231, 87), Image.LANCZOS), (x + 482, y + 716))
        sheet.paste(mn.resize((231, 132), Image.LANCZOS), (x + 733, y + 716))
    sheet.save(os.path.join(OUT, "sheet.png"))


if __name__ == "__main__":
    main()
