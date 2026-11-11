#!/usr/bin/env python3
"""Good Shepherd brand renderer: the logo (stacked, one-line, mark), the app icon, and every
capsule and banner cut from the illustration drawn by tools/scene.py.

    pip install playwright pillow   (Chromium for Playwright must be installed)
    python3 tools/brand.py          (writes into assets/branding and assets/previews)

Everything is drawn here from shapes and Bree Serif (assets/fonts, OFL); edit the SVG
strings below to change the mark. Colours are the brand palette on the press page.
"""
import os, sys, asyncio, base64
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, "assets", "branding")
FONT = base64.b64encode(open(os.path.join(ROOT, "assets/fonts/BreeSerif-Regular.woff2"), "rb").read()).decode()
PAPER, INK, GOLD, MEADOW, NIGHT, LAMP, WOOD, WOOL, FACE = "#f4ead6", "#2e2620", "#efc57a", "#6f8f5e", "#2b2350", "#ffc483", "#6b4a2e", "#fbf6ea", "#4a382c"

STYLE = f"""<style>@font-face{{font-family:Bree;src:url(data:font/woff2;base64,{FONT})}}
text{{font-family:Bree;paint-order:stroke;stroke-linejoin:round;stroke-linecap:round}}</style>"""


def layered(text, x, y, size, spacing=0, anchor="middle", k=1.0):
    """Cut-paper lettering: an ink shadow, an ink backing, a gold sheet, the cream face."""
    a = f'x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" letter-spacing="{spacing}"'
    return (f'<text {a} transform="translate(0,{size*0.05*k:.1f})" fill="{INK}" stroke="{INK}" stroke-width="{size*0.15*k:.1f}" opacity=".55">{text}</text>'
            f'<text {a} fill="{INK}" stroke="{INK}" stroke-width="{size*0.13*k:.1f}">{text}</text>'
            f'<text {a} fill="{GOLD}" stroke="{GOLD}" stroke-width="{size*0.06*k:.1f}">{text}</text>'
            f'<text {a} fill="{PAPER}">{text}</text>')


def sun(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r*1.22}" fill="{INK}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{GOLD}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.62}" fill="{PAPER}" opacity=".55"/>')


def moon(cx, cy, r):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r*1.22}" fill="{INK}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{NIGHT}"/>'
            f'<path d="M{cx+r*0.25},{cy-r*0.72} a{r*0.74},{r*0.74} 0 1,0 {r*0.42},{r*1.2} a{r*0.6},{r*0.6} 0 1,1 {-r*0.42},{-r*1.2}z" fill="{PAPER}"/>')


def crook(x, top, bottom, s=1.0, lamp=True):
    """A shepherd's crook standing at x, its hook curling to the right, a lamp hung from it."""
    w = 26 * s
    hook = f'M{x},{bottom} L{x},{top+90*s} C{x},{top-20*s} {x+150*s},{top-20*s} {x+150*s},{top+78*s} C{x+150*s},{top+128*s} {x+92*s},{top+132*s} {x+88*s},{top+92*s}'
    out = (f'<path d="{hook}" fill="none" stroke="{INK}" stroke-width="{w+16*s}" stroke-linecap="round"/>'
           f'<path d="{hook}" fill="none" stroke="{WOOD}" stroke-width="{w}" stroke-linecap="round"/>'
           f'<path d="M{x-5*s},{bottom-10*s} L{x-5*s},{top+100*s}" fill="none" stroke="#8a6440" stroke-width="{6*s}" stroke-linecap="round" opacity=".8"/>')
    if lamp:
        lx, ly = x + 150 * s, top + 170 * s
        out += (f'<line x1="{lx}" y1="{top+96*s}" x2="{lx}" y2="{ly-12*s}" stroke="{INK}" stroke-width="{5*s}"/>'
                f'<circle cx="{lx}" cy="{ly+4*s}" r="{74*s}" fill="{LAMP}" opacity=".32"/><circle cx="{lx}" cy="{ly+4*s}" r="{44*s}" fill="{LAMP}" opacity=".4"/>'
                f'<path d="M{lx-46*s},{ly} L{lx+40*s},{ly} L{lx+66*s},{ly-12*s} L{lx+58*s},{ly+8*s} Q{lx+36*s},{ly+40*s} {lx-4*s},{ly+40*s} Q{lx-40*s},{ly+38*s} {lx-46*s},{ly}z" fill="#a4552c" stroke="{INK}" stroke-width="{7*s}" stroke-linejoin="round"/>'
                f'<path d="M{lx-30*s},{ly+9*s} L{lx+34*s},{ly+9*s}" stroke="#c97a48" stroke-width="{6*s}" stroke-linecap="round"/>'
                f'<path d="M{lx+62*s},{ly-14*s} q{-18*s},{-24*s} {2*s},{-52*s} q{18*s},{28*s} {-2*s},{52*s}z" fill="{GOLD}" stroke="{INK}" stroke-width="{5*s}" stroke-linejoin="round"/>')
    return out


def sheep(cx, cy, s=1.0, face_right=True):
    d = 1 if face_right else -1
    puffs = "".join(f'<circle cx="{cx+dx*s}" cy="{cy+dy*s}" r="{r*s}"/>' for dx, dy, r in
                    [(-34, 4, 30), (-8, -18, 34), (24, -8, 30), (36, 14, 26), (4, 20, 32), (-24, 24, 26)])
    hx = cx + 52 * s * d
    return (
        f'<g fill="{INK}" stroke="{INK}" stroke-width="{12*s}">{puffs}</g><g fill="{WOOL}">{puffs}</g>'
        f'<ellipse cx="{hx}" cy="{cy+2*s}" rx="{24*s}" ry="{20*s}" fill="{FACE}" stroke="{INK}" stroke-width="{6*s}"/>'
        f'<ellipse cx="{hx-20*s*d}" cy="{cy-8*s}" rx="{14*s}" ry="{7*s}" fill="{FACE}" stroke="{INK}" stroke-width="{5*s}" transform="rotate({-25*d} {hx-20*s*d} {cy-8*s})"/>'
        f'<path d="M{hx-10*s},{cy} q{6*s},{6*s} {12*s},0 M{hx+4*s},{cy} q{5*s},{6*s} {10*s},0" stroke="{PAPER}" stroke-width="{3.2*s}" fill="none" stroke-linecap="round"/>')


def paper_defs(w):
    """Filters and the day-to-night gradients the title's sheets are cut from."""
    def lg(i, a, b):
        return (f'<linearGradient id="{i}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="0"><stop offset=".30" stop-color="{a}"/>'
                f'<stop offset=".78" stop-color="{b}"/></linearGradient>')
    return ('<defs><filter id="lp" x="-10%" y="-25%" width="120%" height="160%"><feDropShadow dx="0" dy="7" stdDeviation="6" flood-color="#120c18" flood-opacity=".5"/></filter>'
            '<filter id="lp2" x="-10%" y="-25%" width="120%" height="160%"><feDropShadow dx="0" dy="3" stdDeviation="2.5" flood-color="#120c18" flood-opacity=".42"/></filter>'
            '<filter id="paper" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="4" stdDeviation="3" flood-color="#120c18" flood-opacity=".45"/></filter>'
            # the back sheet is torn, not cut: a rough edge, as on an old dungeon map
            '<filter id="torn" x="-10%" y="-25%" width="120%" height="160%"><feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="2" seed="4" result="n"/>'
            '<feDisplacementMap in="SourceGraphic" in2="n" scale="9" xChannelSelector="R" yChannelSelector="G" result="d"/>'
            '<feDropShadow in="d" dx="0" dy="7" stdDeviation="6" flood-color="#120c18" flood-opacity=".5"/></filter>'
            + lg("sh2", "#c9703f", "#5f4a9a") + lg("sh3", GOLD, "#b9c2ea") + lg("face", PAPER, "#eef0fa") + '</defs>')


# the sheets of the lettering, back to front: (fill, how far it shows round the letter as a share of the size)
SHEETS = [(INK, 0.150), ("url(#sh2)", 0.098), ("url(#sh3)", 0.050)]


def paper_text(text, x, y, size, anchor="middle", spacing=0):
    """Layered cut-paper lettering: a torn dark sheet at the back, then two coloured sheets, each
    smaller than the one under it and casting its own shadow, then the face. Left to right the
    sheets turn from the day's colours (terracotta, gold, cream) to the night's (plum, moonlight)."""
    a = f'x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" letter-spacing="{spacing}"'
    out = ""
    for k, (col, grow) in enumerate(SHEETS):
        drop = size * 0.022 * (len(SHEETS) - k)
        out += (f'<g filter="url(#{"torn" if k == 0 else "lp2"})"><text {a} transform="translate(0,{drop:.1f})" fill="{col}" stroke="{col}" '
                f'stroke-width="{size*grow*2:.1f}">{text}</text></g>')
    return out + f'<g filter="url(#lp2)"><text {a} fill="url(#face)">{text}</text></g>'


def paper_staff(x0, x1, y, s=1.0):
    """The crook lying on its side under the name, layered like the letters, its hook rising at
    the right; a sheep stands on its day end and a wolf on its night end, facing each other."""
    d = f"M{x0},{y} L{x1-120*s},{y} C{x1-10*s},{y} {x1},{y-70*s} {x1},{y-130*s} C{x1},{y-200*s} {x1-96*s},{y-200*s} {x1-96*s},{y-136*s}"
    out = f'<g filter="url(#torn)"><path d="{d}" fill="none" stroke="{INK}" stroke-width="{46*s}" stroke-linecap="round" stroke-linejoin="round"/></g>'
    out += f'<g filter="url(#lp2)"><path d="{d}" fill="none" stroke="{WOOD}" stroke-width="{26*s}" stroke-linecap="round" stroke-linejoin="round"/></g>'
    out += f'<path d="{d}" fill="none" stroke="#9a7048" stroke-width="{7*s}" stroke-linecap="round" stroke-linejoin="round" transform="translate(0,{-5*s})"/>'
    top = y - 13 * s
    out += scene.sheep(x0 + 104 * s, top - 74 * 0.7 * s, 0.7 * s, True)
    wx = x1 - 150 * s
    # the wolf is cut from night paper with a moonlit sheet behind it, so it shows on any ground
    rim = scene.wolf(wx, top, 0.36 * s, "#b9c2ea")
    out += (f'<g transform="translate({2*wx},0) scale(-1,1)"><g stroke="#b9c2ea" stroke-width="{16*s}" stroke-linejoin="round">{rim}</g>'
            f'{scene.wolf(wx, top, 0.36 * s, "#3a2f62")}</g>')
    return out


def logo_stacked(w=1280, h=720, tagline=True, with_crook=True):
    """The title: two lines of layered paper lettering over the shepherd's staff, a sheep on one
    end of it and a wolf on the other."""
    g = [paper_defs(w)]
    g.append(paper_text("Good", 640, 232, 176))
    g.append(paper_text("Shepherd", 640, 446, 204))
    if with_crook:
        g.append(paper_staff(30, 1252, 596))
    if tagline:
        g.append(f'<text x="640" y="690" font-size="36" text-anchor="middle" fill="{PAPER}" stroke="{INK}" stroke-width="9">Tend the flock by day. Go after the one by night.</text>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{STYLE}{"".join(g)}</svg>'


def logo_line(w=1500, h=330, with_crook=True):
    """One line, for small spaces."""
    g = [paper_defs(w), paper_text("Good Shepherd", 750, 176, 150)]
    if with_crook:
        g.append(paper_staff(24, 1476, 290, 0.74))
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{STYLE}{"".join(g)}</svg>'


def mark(size=1024, shape="circle"):
    """The emblem: day on the left, night on the right, the crook and its lamp between,
    one sheep at its foot. `shape`: circle (avatar) or squircle (app and project icon)."""
    s = size / 1024.0
    clip = '<circle cx="512" cy="512" r="470"/>' if shape == "circle" else '<rect x="42" y="42" width="940" height="940" rx="210"/>'
    ring = (f'<circle cx="512" cy="512" r="478" fill="none" stroke="{INK}" stroke-width="34"/><circle cx="512" cy="512" r="470" fill="none" stroke="{GOLD}" stroke-width="16"/>'
            if shape == "circle" else
            f'<rect x="38" y="38" width="948" height="948" rx="214" fill="none" stroke="{INK}" stroke-width="34"/><rect x="46" y="46" width="932" height="932" rx="206" fill="none" stroke="{GOLD}" stroke-width="16"/>')
    body = f'''<defs><clipPath id="c">{clip}</clipPath>
      <linearGradient id="day" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#bcd6e6"/><stop offset="1" stop-color="#f3e6c4"/></linearGradient>
      <linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c1738"/><stop offset="1" stop-color="#4a3a72"/></linearGradient>
      <radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{LAMP}" stop-opacity=".85"/><stop offset="1" stop-color="{LAMP}" stop-opacity="0"/></radialGradient></defs>
    <g clip-path="url(#c)">
      <rect x="0" y="0" width="540" height="1024" fill="url(#day)"/><rect x="540" y="0" width="484" height="1024" fill="url(#night)"/>
      <circle cx="300" cy="290" r="96" fill="{GOLD}"/><circle cx="300" cy="290" r="60" fill="{PAPER}" opacity=".5"/>
      <path d="M790,170 a84,84 0 1,0 60,150 a70,70 0 1,1 -60,-150z" fill="{PAPER}"/>
      <g fill="{PAPER}"><circle cx="690" cy="330" r="7"/><circle cx="880" cy="420" r="6"/><circle cx="640" cy="200" r="5"/><circle cx="905" cy="250" r="5"/></g>
      <circle cx="700" cy="560" r="260" fill="url(#glow)"/>
      <path d="M0,720 C200,640 400,660 540,700 L540,1024 L0,1024z" fill="{MEADOW}"/><path d="M0,800 C220,740 400,760 540,790 L540,1024 L0,1024z" fill="#85a56f"/>
      <path d="M540,700 C700,660 880,690 1024,740 L1024,1024 L540,1024z" fill="#3a2f5e"/><path d="M540,790 C720,760 900,790 1024,830 L1024,1024 L540,1024z" fill="#241d40"/>
      {crook(540, 250, 900, 1.45)}
      {sheep(330, 800, 2.25)}
    </g>{ring}'''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 1024 1024">{body}</svg>'


async def raster(jobs):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        br = await p.chromium.launch()
        for svg, w, h, path in jobs:
            page = await br.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
            await page.set_content(f'<html><body style="margin:0;background:transparent">{svg}</body></html>')
            await page.wait_for_timeout(250)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            await page.screenshot(path=path, omit_background=True)
            await page.close()
        await br.close()


def main():
    tmp = os.path.join(ROOT, "tools", ".out")
    os.makedirs(tmp, exist_ok=True)
    logo_dir = os.path.join(B, "logo")
    os.makedirs(logo_dir, exist_ok=True)
    for name, svg in [("logo-stacked.svg", logo_stacked()), ("logo-one-line.svg", logo_line()), ("mark-circle.svg", mark(1024, "circle")), ("mark-app.svg", mark(1024, "squircle"))]:
        open(os.path.join(logo_dir, name), "w").write(svg)
    jobs = [(logo_stacked(), 1280, 720, os.path.join(B, "steam/library-logo-1280x720.png")),
            (logo_stacked(tagline=False), 1280, 720, os.path.join(tmp, "stack.png")),
            (logo_stacked(tagline=False), 1280, 720, os.path.join(logo_dir, "logo-stacked-1280x720.png")),
            (logo_line(), 1500, 330, os.path.join(tmp, "line.png")),
            (logo_line(), 1500, 330, os.path.join(logo_dir, "logo-one-line-1500x330.png")),
            (mark(1024, "circle"), 1024, 1024, os.path.join(tmp, "mark.png")),
            (scene.scene(), scene.W, scene.H, os.path.join(tmp, "scene.png")),
            (mark(1024, "squircle"), 1024, 1024, os.path.join(logo_dir, "app-icon-1024.png"))]
    asyncio.run(raster(jobs))
    if "--logos" in sys.argv:
        return
    compose(tmp, logo_dir)


def fit_logo(img, max_w, max_h):
    box = img.getbbox()
    img = img.crop(box)
    k = min(max_w / img.width, max_h / img.height)
    return img.resize((max(1, int(img.width * k)), max(1, int(img.height * k))), Image.LANCZOS)


def crop_art(src, w, h, focus_x, focus_y=1.0):
    """The largest w:h window of the scene, placed by focus (0..1 across, 0 top .. 1 bottom)."""
    ch = src.height
    cw = ch * w / h
    if cw > src.width:
        cw = src.width
        ch = cw * h / w
    x0 = min(max(focus_x * src.width - cw / 2, 0), src.width - cw)
    y0 = (src.height - ch) * focus_y
    return src.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.LANCZOS)


BANDS = ["#efc57a", "#d98f52", "#c06d48", "#a46361", "#855779", "#684d90", "#5e4899"]   # the logo's paper bands, day to night


def frame(art, weight=1.0):
    """A cut-paper border in the logo's own layers: an ink edge, a cream band, a thin band of
    colour running day to night across the picture, and an ink hairline with a soft shadow
    falling inside it. Corners of the window are rounded; the outside stays square (Steam
    rounds or crops capsules itself). `weight` scales the border for very small formats."""
    from PIL import ImageDraw, ImageFilter
    w, h = art.size
    k = 3                                    # supersample
    u = max(2.0, min(w, h) * 0.011 * weight) * k   # one layer's width
    W, H = w * k, h * k
    def ring(outer, inner, radius):
        m = Image.new("L", (W, H), 0)
        d = ImageDraw.Draw(m)
        d.rounded_rectangle((outer, outer, W - outer, H - outer), radius=max(radius + (inner - outer), 0), fill=255)
        d.rounded_rectangle((inner, inner, W - inner, H - inner), radius=radius, fill=0)
        return m
    rad = u * 2.2
    over = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # soft shadow inside the window
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).rounded_rectangle((u * 3.0, u * 3.0, W - u * 3.0, H - u * 3.0), radius=rad, fill=255)
    edge = Image.eval(sh.filter(ImageFilter.GaussianBlur(u * 1.2)), lambda v: int((255 - v) * 0.55))
    over.paste(Image.new("RGBA", (W, H), (40, 25, 10, 255)), (0, 0), Image.composite(edge, Image.new("L", (W, H), 0), sh))
    grad = Image.new("RGB", (len(BANDS), 1))
    grad.putdata([tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) for c in BANDS])
    grad = grad.resize((W, H), Image.BILINEAR).convert("RGBA")
    solid = lambda c: Image.new("RGBA", (W, H), tuple(int(c[i:i + 2], 16) for i in (1, 3, 5)) + (255,))
    full = Image.new("L", (W, H), 0)
    ImageDraw.Draw(full).rectangle((0, 0, W, H), fill=255)
    inner0 = Image.new("L", (W, H), 0)
    ImageDraw.Draw(inner0).rounded_rectangle((u * 0.55, u * 0.55, W - u * 0.55, H - u * 0.55), radius=rad + u * 2.4, fill=255)
    over.paste(solid(INK), (0, 0), Image.composite(Image.new("L", (W, H), 0), full, inner0))   # ink edge (square outside)
    over.paste(solid(PAPER), (0, 0), ring(u * 0.55, u * 1.9, rad + u * 1.1))                    # cream band
    over.paste(grad, (0, 0), ring(u * 1.9, u * 2.6, rad + u * 0.4))                             # day-to-night band
    over.paste(solid(INK), (0, 0), ring(u * 2.6, u * 3.0, rad))                                 # hairline
    out = art.convert("RGBA")
    out.alpha_composite(over.resize((w, h), Image.LANCZOS))
    return out


# Formats that sit on a store shelf among other games wear the frame; banners, the hero and
# the page background (which Steam or the platform lays things over, edge to edge) do not.
FRAMED = {"steam/main-capsule-1232x706.png": 1.0, "steam/header-capsule-920x430.png": 1.0, "steam/small-capsule-462x174.png": 1.25,
          "steam/vertical-capsule-748x896.png": 1.0, "steam/library-capsule-600x900.png": 1.0, "steam/package-header-1414x464.png": 1.0}


def compose(tmp, logo_dir):
    # the illustration itself (tools/scene.py): one logo-free master, everything else is cut from it
    master = Image.open(os.path.join(tmp, "scene.png")).convert("RGB")
    os.makedirs(os.path.join(B, "source"), exist_ok=True)
    master.save(os.path.join(B, "source", "key-scene-3840x2160.png"))
    master.crop((0, 800, 3840, 2040)).save(os.path.join(B, "steam/library-hero-3840x1240.png"))
    master.crop((0, 800, 3840, 2040)).resize((1920, 620), Image.LANCZOS).save(os.path.join(ROOT, "assets/previews/hero.jpg"), quality=86)
    master.resize((1438, 809), Image.LANCZOS).resize((1438, 810)).save(os.path.join(B, "steam/page-background-1438x810.png"))
    stack = Image.open(os.path.join(tmp, "stack.png")).convert("RGBA")
    line = Image.open(os.path.join(tmp, "line.png")).convert("RGBA")
    mark_img = Image.open(os.path.join(tmp, "mark.png")).convert("RGBA")
    # name, size, focus x, focus y (1 = keep the ground, trim sky), which logo, logo box (x, y, w, h as fractions)
    # The name never covers the shepherd and never sits in the top-left corner, where Steam
    # hangs its own flags: on wide formats it goes on the night sky to his right, on tall ones
    # in the sky above him with the top band left clear.
    plan = [
        ("goodshepherd-key-art-1920x1080.png", (1920, 1080), 0.50, 1.0, stack, (0.595, 0.045, 0.385, 0.36)),
        ("steam/main-capsule-1232x706.png", (1232, 706), 0.50, 1.0, stack, (0.595, 0.045, 0.385, 0.36)),
        ("steam/header-capsule-920x430.png", (920, 430), 0.56, 0.93, stack, (0.60, 0.05, 0.385, 0.50)),
        ("steam/small-capsule-462x174.png", (462, 174), 0.80, 0.86, line, (0.315, 0.10, 0.67, 0.80)),
        ("steam/vertical-capsule-748x896.png", (748, 896), 0.53, 1.0, stack, (0.08, 0.125, 0.84, 0.28)),
        ("steam/library-capsule-600x900.png", (600, 900), 0.53, 1.0, stack, (0.06, 0.13, 0.88, 0.26)),
        ("steam/package-header-1414x464.png", (1414, 464), 0.58, 0.90, stack, (0.60, 0.06, 0.38, 0.60)),
        ("social/x-bluesky-header-1500x500.png", (1500, 500), 0.58, 0.90, stack, (0.60, 0.06, 0.38, 0.60)),
        ("social/youtube-banner-2560x1440.png", (2560, 1440), 0.50, 1.0, stack, (0.575, 0.355, 0.225, 0.21)),
        ("social/portrait-post-1080x1350.png", (1080, 1350), 0.53, 1.0, stack, (0.08, 0.12, 0.84, 0.27)),
    ]
    for name, (w, h), fx, fy, logo, (lx, ly, lw, lh) in plan:
        art = crop_art(master, w, h, fx, fy).convert("RGBA")
        if logo is line:   # the small capsule: the shepherd at the left edge, the name across the night beside him
            art = master.crop((1650, 1010, 3840, 1835)).resize((w, h), Image.LANCZOS).convert("RGBA")
        lg = fit_logo(logo, lw * w, lh * h)
        art.alpha_composite(lg, (int(lx * w + (lw * w - lg.width) / 2), int(ly * h + (lh * h - lg.height) / 2)))
        if name in FRAMED:
            art = frame(art, FRAMED[name])
        art.convert("RGB").save(os.path.join(B, name))
    mark_img.resize((800, 800), Image.LANCZOS).save(os.path.join(B, "social/avatar-800x800.png"))
    app = Image.open(os.path.join(logo_dir, "app-icon-1024.png")).convert("RGBA")
    for n in (512, 256, 128, 64, 32):
        app.resize((n, n), Image.LANCZOS).save(os.path.join(logo_dir, f"app-icon-{n}.png"))
    app.save(os.path.join(logo_dir, "app-icon.ico"), sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    # the page's own lightweight previews
    prev = {"key-art": "goodshepherd-key-art-1920x1080.png", "main": "steam/main-capsule-1232x706.png", "header": "steam/header-capsule-920x430.png",
            "small": "steam/small-capsule-462x174.png", "vertical": "steam/vertical-capsule-748x896.png", "library": "steam/library-capsule-600x900.png",
            "package": "steam/package-header-1414x464.png", "portrait": "social/portrait-post-1080x1350.png"}
    for k, src in prev.items():
        im = Image.open(os.path.join(B, src)).convert("RGB")
        if im.width > 1280:
            im = im.resize((1280, int(im.height * 1280 / im.width)), Image.LANCZOS)
        im.save(os.path.join(ROOT, "assets/previews", k + ".jpg"), quality=86)


if __name__ == "__main__":
    main()
