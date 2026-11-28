#!/usr/bin/env python3
"""Title-logo drafts (2026-11-28): five lockups of the name with the shepherd's crook in the
lettering and a sheep and a wolf on it. No rainbow: cream letters, one night-indigo outline,
and two paper colours only (day gold, night blue). Writes lab/logos/<n>.png and sheet.png.

    python3 tools/logo_drafts.py
"""
import os, sys, json, subprocess
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene as S
import brand

ROOT = brand.ROOT
OUT = os.path.join(ROOT, "lab", "logos")
TMP = os.path.join(ROOT, "tools", ".out")
W, H = 1500, 860
EDGE, CREAM, GOLD, BLUE, WOOD, WOODL = "#1b1240", "#fff8e2", "#f5b53a", "#8f9bf5", "#7a4e2a", "#b98452"
F = TTFont(os.path.join(ROOT, "assets/fonts/BreeSerif-Regular.woff2"))
GS, CM, UPM = F.getGlyphSet(), F.getBestCmap(), F["head"].unitsPerEm


def text(t, x, y, size, ls=0, anchor="start"):
    """Outlines of t with its baseline at y. Returns (path d, [(char, x0, advance, xmin, xmax, ymax)])."""
    sc = size / UPM
    wd = sum(GS[CM[ord(c)]].width * sc + ls for c in t) - ls
    x = x - wd / 2 if anchor == "middle" else x
    d, boxes = "", []
    for c in t:
        gn = CM[ord(c)]
        pen = SVGPathPen(GS, ntos=lambda v: f"{v:.1f}")
        GS[gn].draw(TransformPen(pen, (sc, 0, 0, -sc, x, y)))
        bp = BoundsPen(GS); GS[gn].draw(bp)
        b = bp.bounds or (0, 0, 0, 0)
        d += pen.getCommands()
        boxes.append((c, x, GS[gn].width * sc, x + b[0] * sc, x + b[2] * sc, y - b[3] * sc))
        x += GS[gn].width * sc + ls
    return d, boxes


def letters(d, size, sheet=GOLD, face=CREAM, k=1.0):
    """(edge, fill) for cut-paper lettering: indigo backing with a solid drop, a coloured sheet, the face."""
    e = size * 0.16 * k
    edge = (f'<path d="{d}" transform="translate(0,{size*0.07:.1f})" fill="{EDGE}" stroke="{EDGE}" stroke-width="{e:.1f}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="{EDGE}" stroke="{EDGE}" stroke-width="{e:.1f}" stroke-linejoin="round"/>')
    fill = (f'<path d="{d}" transform="translate(0,{size*0.028:.1f})" fill="{sheet}" stroke="{sheet}" stroke-width="{size*0.075:.1f}" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="{face}"/>')
    return edge, fill


def hook(x, y0, top, r, way=1):
    """A crook standing at x from y0 up to `top`, its hook of radius r curling to `way`."""
    return (f"M{x},{y0} L{x},{top+r} C{x},{top-r*0.25} {x+way*2*r},{top-r*0.25} {x+way*2*r},{top+r*0.95} "
            f"C{x+way*2*r},{top+r*1.55} {x+way*1.22*r},{top+r*1.6} {x+way*1.15*r},{top+r*1.05}")


def staff(d, w):
    edge = (f'<path d="{d}" transform="translate(0,{w*0.35:.1f})" fill="none" stroke="{EDGE}" stroke-width="{w*1.75:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{EDGE}" stroke-width="{w*1.75:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    fill = (f'<path d="{d}" fill="none" stroke="{WOOD}" stroke-width="{w:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" transform="translate({-w*0.18:.1f},{-w*0.1:.1f})" fill="none" stroke="{WOODL}" stroke-width="{w*0.26:.1f}" stroke-linecap="round" stroke-linejoin="round"/>')
    return edge, fill


def sticker(inner, w=13):
    return f'<g stroke="{EDGE}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round">{inner}</g>{inner}'


def sheep(x, feet, s, right=True):
    return sticker(S.sheep(x, feet - 74 * s, s, right).replace(' filter="url(#paper)"', ""))


def wolf(x, feet, s, right=True, col="#2a2058"):
    """The brand's wolf as a sticker: night body, a moonlit keyline, the indigo edge outside it."""
    w = S.wolf(x, feet, s, col)
    inner = w[w.index(">") + 1:w.index("</g>")]
    eye = w[w.index("</g>") + 4:]
    g = (f'<g fill="{EDGE}" stroke="{EDGE}" stroke-width="24" stroke-linejoin="round">{inner}</g>'
         f'<g fill="#b4bcff" stroke="#b4bcff" stroke-width="11" stroke-linejoin="round">{inner}</g><g fill="{col}">{inner}</g>{eye}')
    return g if right else f'<g transform="translate({2*x},0) scale(-1,1)">{g}</g>'


def lamp(x, y, s):
    return (f'<line x1="{x}" y1="{y-70*s}" x2="{x}" y2="{y}" stroke="{EDGE}" stroke-width="{6*s}"/><circle cx="{x}" cy="{y+22*s}" r="{70*s}" fill="#ffc46a" opacity=".35"/>'
            f'<rect x="{x-24*s}" y="{y}" width="{48*s}" height="{58*s}" rx="{10*s}" fill="{GOLD}" stroke="{EDGE}" stroke-width="{9*s}"/><rect x="{x-11*s}" y="{y+12*s}" width="{22*s}" height="{34*s}" rx="{7*s}" fill="{CREAM}"/>')


def svg(parts):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><filter id="drop" x="-10%" y="-10%" width="120%" height="130%">'
            f'<feDropShadow dx="0" dy="10" stdDeviation="9" flood-color="#0c0820" flood-opacity=".45"/></filter></defs><g filter="url(#drop)">{"".join(parts)}</g></svg>')


def box(bs, ch, nth=0):
    return [b for b in bs if b[0] == ch][nth]


def d1():
    """The last d's stem is the crook, rising beside 'Good' with the lamp on it; a sheep on the S."""
    dg, bg = text("Good", 700, 330, 290, anchor="middle")
    ds, bs = text("Shepherd", 700, 650, 290, anchor="middle")
    e1, f1 = letters(dg, 290, GOLD); e2, f2 = letters(ds, 290, BLUE)
    b = box(bs, "d")
    sx = b[4] - 290 * 0.062
    ce, cf = staff(hook(sx, 640, 70, 70, -1), 30)
    sh = box(bs, "S")
    return svg([ce, e1, e2, f1, f2, cf, lamp(sx - 140, 215, 1.0), sheep(sh[1] + 100, sh[5] - 6, 1.0, True)])


def d2():
    """Left-set. The d of 'Good' grows into the crook; under its hook a wolf walks the tops of 'erd', a sheep sits on the G."""
    dg, bg = text("Good", 110, 340, 300)
    ds, bs = text("Shepherd", 110, 660, 300)
    e1, f1 = letters(dg, 300, GOLD); e2, f2 = letters(ds, 300, BLUE)
    b = box(bg, "d")
    sx = b[4] - 300 * 0.062
    ce, cf = staff(hook(sx, 330, 40, 86, 1), 31)
    r = box(bs, "r")
    g_ = box(bg, "G")
    return svg([ce, e1, e2, f1, f2, cf, wolf(r[1] + 20, r[5] + 4, 0.56, False), sheep(g_[1] + 120, g_[5] - 4, 0.95, True)])


def d3():
    """The two o's: a sheep in the day one, a wolf's eyes in the night one. The crook underlines it."""
    dg, bg = text("Good", 750, 330, 310, anchor="middle")
    ds, bs = text("Shepherd", 750, 630, 270, anchor="middle")
    e1, f1 = letters(dg, 310, GOLD); e2, f2 = letters(ds, 270, GOLD)
    o1, o2 = box(bg, "o", 0), box(bg, "o", 1)
    xh = 330 - o1[5]
    def cx(o): return (o[3] + o[4]) / 2
    cy = 330 - xh / 2
    rx, ry = (o1[4] - o1[3]) * 0.30, xh * 0.34
    eyes = "".join(f'<path d="M{cx(o2)+k*rx*0.52-rx*0.3:.1f},{cy-4:.1f} q{rx*0.3:.1f},{-ry*0.42:.1f} {rx*0.6:.1f},{0} q{-rx*0.3:.1f},{ry*0.3:.1f} {-rx*0.6:.1f},0z" fill="#ffd75a"/>' for k in (-1, 1))
    day = f'<ellipse cx="{cx(o1):.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{GOLD}"/>'
    night = f'<ellipse cx="{cx(o2):.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="#241a5a"/>' + eyes
    face = (f'<g transform="translate({cx(o1):.1f},{cy+ry*0.2:.1f}) scale({ry/62:.2f})"><circle cx="0" cy="-38" r="26" fill="{CREAM}"/><circle cx="-22" cy="-28" r="18" fill="{CREAM}"/><circle cx="22" cy="-28" r="18" fill="{CREAM}"/>'
            f'<ellipse cx="-34" cy="-8" rx="15" ry="8" fill="#4a382c" transform="rotate(20 -34 -8)"/><ellipse cx="34" cy="-8" rx="15" ry="8" fill="#4a382c" transform="rotate(-20 34 -8)"/>'
            f'<path d="M-24,-20 Q0,-30 24,-20 L20,22 Q0,46 -20,22Z" fill="#4a382c"/><path d="M-13,0 q5,6 10,0 M3,0 q5,6 10,0" stroke="{CREAM}" stroke-width="3.5" fill="none" stroke-linecap="round"/></g>')
    x0, x1 = bs[0][3] - 10, bs[-1][4] + 60
    und = f"M{x0},{735} L{x1-90},{735} C{x1-10},{735} {x1},{690} {x1},{650} C{x1},{600} {x1-70},{600} {x1-70},{648}"
    ce, cf = staff(und, 26)
    return svg([ce, e1, e2, f1, f2, day, night, face, cf])


def d4():
    """A plaque: the name on a night-indigo plate with a gold edge, the crook behind it, the sheep and the wolf facing each other on top."""
    dg, bg = text("Good", 750, 400, 230, anchor="middle")
    ds, bs = text("Shepherd", 750, 650, 250, anchor="middle")
    plate = (f'<rect x="150" y="205" width="1200" height="520" rx="60" fill="{EDGE}" transform="translate(0,18)"/><rect x="150" y="205" width="1200" height="520" rx="60" fill="{EDGE}"/>'
             f'<rect x="168" y="223" width="1164" height="484" rx="46" fill="{GOLD}"/><rect x="182" y="237" width="1136" height="456" rx="36" fill="#2c2170"/>')
    ce, cf = staff(hook(1290, 840, 40, 80, -1), 30)
    fill = f'<path d="{dg}" transform="translate(0,9)" fill="{GOLD}"/><path d="{dg}" fill="{CREAM}"/><path d="{ds}" transform="translate(0,10)" fill="{GOLD}"/><path d="{ds}" fill="{CREAM}"/>'
    return svg([ce, cf, plate, fill, sheep(380, 212, 1.15, True), wolf(930, 212, 0.62, False)])


def d5():
    """The crook stands at the left and its hook sweeps over 'GOOD' and a sheep, keeping them; the wolf waits outside on the last letters."""
    dg, bg = text("GOOD", 705, 318, 150, ls=10, anchor="middle")
    ds, bs = text("Shepherd", 800, 640, 300, anchor="middle")
    e1, f1 = letters(dg, 150, GOLD, k=1.15); e2, f2 = letters(ds, 300, BLUE)
    s0 = box(bs, "S")
    x = s0[3] - 70
    top, r = 60, 330
    path = (f"M{x},{800} L{x},{top+200} C{x},{top-10} {x+260},{top} {x+r*1.3},{top} C{x+r*2.5},{top} {x+r*2.75},{top+120} {x+r*2.75},{top+200} "
            f"C{x+r*2.75},{top+262} {x+r*2.52},{top+266} {x+r*2.5},{top+215}")
    ce, cf = staff(path, 32)
    r_ = box(bs, "r")
    p = box(bs, "p")
    return svg([ce, e1, e2, f1, f2, cf, sheep(x + 175, 336, 0.95, True), wolf(r_[1] + 90, r_[5] + 4, 0.56, False)])


def d6():
    """The blend Daniel chose: #1's centred lettering (gold under 'Good', night blue under
    'Shepherd'), #3's crook as the underline with no lamp, #2's sheep on the G and wolf on 'er'."""
    dg, bg = text("Good", 720, 345, 290, anchor="middle")
    ds, bs = text("Shepherd", 720, 650, 290, anchor="middle")
    e1, f1 = letters(dg, 290, GOLD); e2, f2 = letters(ds, 290, BLUE)
    x0, x1 = bs[0][3] - 10, bs[-1][4] + 64
    und = f"M{x0},{765} L{x1-96},{765} C{x1-10},{765} {x1},{716} {x1},{672} C{x1},{618} {x1-76},{618} {x1-76},{670}"
    ce, cf = staff(und, 28)
    g_, r = box(bg, "G"), box(bs, "r")
    return svg([ce, e1, e2, f1, f2, cf, wolf(r[1] + 84, r[5] + 4, 0.5, False), sheep(g_[1] + 118, g_[5] - 4, 0.95, True)])


def d7():
    """The chosen logo on one line, for small spaces."""
    size = 196
    dg, bg = text("Good", 60, 500, size)
    ds, bs = text("Shepherd", bg[-1][1] + bg[-1][2] + size * 0.26, 500, size)
    e1, f1 = letters(dg, size, GOLD); e2, f2 = letters(ds, size, BLUE)
    x0, x1 = bg[0][3] - 6, bs[-1][4] + 46
    und = f"M{x0},{582} L{x1-70},{582} C{x1-8},{582} {x1},{548} {x1},{516} C{x1},{476} {x1-56},{476} {x1-56},{514}"
    ce, cf = staff(und, 20)
    g_, r = box(bg, "G"), box(bs, "r")
    return svg([ce, e1, e2, f1, f2, cf, wolf(r[1] + 50, r[5] + 3, 0.36, False), sheep(g_[1] + 80, g_[5] - 3, 0.66, True)])


DRAFTS = [("1-crook-d-and-lamp", d1), ("2-crook-wolf-under-the-hook", d2), ("3-the-two-os", d3), ("4-plaque", d4), ("5-kept-under-the-hook", d5), ("6-blend", d6), ("7-blend-one-line", d7)]


def main():
    os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)
    spec = []
    for n, fn in DRAFTS:
        p = os.path.join(TMP, "logo_" + n + ".svg"); open(p, "w").write(fn())
        spec.append({"svg": p, "png": os.path.join(OUT, n + ".png"), "w": W, "h": H})
    subprocess.run(["node", os.path.join(ROOT, "tools", "raster.js"), json.dumps(spec)], check=True)
    if "--only" in sys.argv:
        n = sys.argv[sys.argv.index("--only") + 1]
        lg = Image.open(os.path.join(OUT, n + ".png")).convert("RGBA")
        sh = Image.new("RGB", (W * 2 + 60, H + 40 + 330), (27, 40, 56))
        for j, bgc in enumerate(((126, 200, 238), (40, 30, 96))):
            c = Image.new("RGBA", (W, H), bgc + (255,)); c.alpha_composite(lg); sh.paste(c.convert("RGB"), (20 + j * (W + 20), 20))
        x = 20
        for bgc, sw in (((240, 150, 80), 520), ((60, 130, 80), 300), ((126, 200, 238), 180), ((40, 30, 96), 180)):
            hh = int(sw * H / W); c = Image.new("RGBA", (sw, hh), bgc + (255,)); c.alpha_composite(lg.resize((sw, hh), Image.LANCZOS)); sh.paste(c.convert("RGB"), (x, H + 40)); x += sw + 20
        sh.save(os.path.join(OUT, n + "-sheet.png"))
        return
    cw, chh = 700, int(700 * H / W)
    sheet = Image.new("RGB", (cw * 2 + 300 + 80, (chh + 20) * len(DRAFTS) + 20), (27, 40, 56))
    for i, (n, _) in enumerate(DRAFTS):
        lg = Image.open(os.path.join(OUT, n + ".png")).convert("RGBA")
        y = 20 + i * (chh + 20)
        for j, bgc in enumerate(((126, 200, 238), (40, 30, 96))):
            cell = Image.new("RGBA", (cw, chh), bgc + (255,)); cell.alpha_composite(lg.resize((cw, chh), Image.LANCZOS)); sheet.paste(cell.convert("RGB"), (20 + j * (cw + 20), y))
        for j, (bgc, sw) in enumerate((((240, 150, 80), 280), ((60, 130, 80), 150))):
            sh_ = int(sw * H / W); cell = Image.new("RGBA", (sw, sh_), bgc + (255,)); cell.alpha_composite(lg.resize((sw, sh_), Image.LANCZOS))
            sheet.paste(cell.convert("RGB"), (20 + 2 * (cw + 20), y + j * 180))
    sheet.save(os.path.join(OUT, "sheet.png"))


if __name__ == "__main__":
    main()
