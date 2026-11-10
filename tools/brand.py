#!/usr/bin/env python3
"""Good Shepherd brand renderer: the logo (stacked, one-line, mark), the app icon, and every
capsule and banner recomposed from the logo-free key art (steam/library-hero-3840x1240.png).

    pip install playwright pillow   (Chromium for Playwright must be installed)
    python3 tools/brand.py          (writes into assets/branding and assets/previews)

Everything is drawn here from shapes and Bree Serif (assets/fonts, OFL); edit the SVG
strings below to change the mark. Colours are the brand palette on the press page.
"""
import os, sys, asyncio, base64
from PIL import Image

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


def logo_stacked(w=1280, h=720, tagline=True, with_crook=True):
    cx = 770
    g = ['<g>']
    if with_crook:   # (left off where the art already shows the shepherd's own crook)
        g.append(crook(118, 70, 600, 1.0))
    # GOOD, with a sun and a moon for its two O's: the day and the night of the game
    g.append(layered("G", cx - 186, 236, 138))
    g.append(sun(cx - 62, 187, 43))
    g.append(moon(cx + 62, 187, 43))
    g.append(layered("D", cx + 186, 236, 138))
    g.append(layered("Shepherd", cx, 512, 212))
    g.append(sheep(1010, 372, 0.62))   # one lamb, up on the letters
    if tagline:
        g.append(f'<text x="{cx}" y="640" font-size="38" text-anchor="middle" fill="{PAPER}" stroke="{INK}" stroke-width="9" style="font-family:Bree">Tend the flock by day. Go after the one by night.</text>')
    g.append('</g>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{STYLE}{"".join(g)}</svg>'


def logo_line(w=1500, h=330, with_crook=True):
    """One line, for small spaces: crook, Good (sun and moon for the o's), Shepherd."""
    size, base = 190, 236
    r, cy = size * 0.235, base - size * 0.245
    g = [crook(66, 44, 304, 0.6, lamp=False)] if with_crook else []
    g.append(layered("G", 262, base, size))
    g.append(sun(366, cy, r))
    g.append(moon(478, cy, r))
    g.append(layered("d", 578, base, size))
    g.append(layered("Shepherd", 1058, base, size))
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
            (logo_stacked(tagline=False, with_crook=False), 1280, 720, os.path.join(tmp, "stack.png")),
            (logo_stacked(tagline=False), 1280, 720, os.path.join(logo_dir, "logo-stacked-1280x720.png")),
            (logo_line(with_crook=False), 1500, 330, os.path.join(tmp, "line.png")),
            (logo_line(), 1500, 330, os.path.join(logo_dir, "logo-one-line-1500x330.png")),
            (mark(1024, "circle"), 1024, 1024, os.path.join(tmp, "mark.png")),
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


def crop_art(hero, w, h, focus_x, zoom=1.0, focus_y=0.5):
    """Cut a w:h window out of the hero art centred on focus_x (0..1), as tall as allowed / zoom."""
    ch = hero.height / zoom
    cw = ch * w / h
    if cw > hero.width:
        cw = hero.width
        ch = cw * h / w
    x0 = min(max(focus_x * hero.width - cw / 2, 0), hero.width - cw)
    y0 = min(max(focus_y * hero.height - ch / 2, 0), hero.height - ch)
    return hero.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.LANCZOS)


def compose(tmp, logo_dir):
    hero = Image.open(os.path.join(B, "steam/library-hero-3840x1240.png")).convert("RGB")
    stack = Image.open(os.path.join(tmp, "stack.png")).convert("RGBA")
    line = Image.open(os.path.join(tmp, "line.png")).convert("RGBA")
    # tall formats need more sky than the hero has: the same art with its top edge drawn upward
    extra = int(hero.height * 0.55)
    tall = Image.new("RGB", (hero.width, hero.height + extra))
    tall.paste(hero.crop((0, 0, hero.width, 3)).resize((hero.width, extra), Image.BILINEAR), (0, 0))
    tall.paste(hero, (0, extra))
    mark_img = Image.open(os.path.join(tmp, "mark.png")).convert("RGBA")
    # name, size, art focus x, zoom, which logo, logo box (x, y, w, h as fractions), focus y
    plan = [
        ("goodshepherd-key-art-1920x1080.png", (1920, 1080), 0.50, 1.0, stack, (0.03, 0.05, 0.40, 0.44), 0.5),
        ("steam/main-capsule-1232x706.png", (1232, 706), 0.50, 1.0, stack, (0.02, 0.05, 0.38, 0.44), 0.5),
        ("steam/header-capsule-920x430.png", (920, 430), 0.47, 1.0, stack, (0.03, 0.05, 0.44, 0.74), 0.5),
        ("steam/small-capsule-462x174.png", (462, 174), 0.47, 1.0, line, (0.04, 0.16, 0.92, 0.68), 0.45),
        ("steam/vertical-capsule-748x896.png", (748, 896), 0.52, 1.0, stack, (0.07, 0.03, 0.86, 0.33), 1.0),
        ("steam/library-capsule-600x900.png", (600, 900), 0.535, 1.0, stack, (0.06, 0.03, 0.88, 0.30), 1.0),
        ("steam/package-header-1414x464.png", (1414, 464), 0.44, 1.0, stack, (0.03, 0.06, 0.36, 0.78), 0.5),
        ("social/x-bluesky-header-1500x500.png", (1500, 500), 0.46, 1.0, stack, (0.04, 0.08, 0.34, 0.76), 0.5),
        ("social/youtube-banner-2560x1440.png", (2560, 1440), 0.50, 1.0, stack, (0.205, 0.37, 0.25, 0.26), 0.5),
        ("social/portrait-post-1080x1350.png", (1080, 1350), 0.52, 1.0, stack, (0.08, 0.03, 0.84, 0.32), 1.0),
    ]
    for name, (w, h), fx, zoom, logo, (lx, ly, lw, lh), fy in plan:
        art = crop_art(tall if h > w else hero, w, h, fx, zoom, fy).convert("RGBA")
        if logo is line:   # a small capsule is read at thumbnail size: quiet the art so the name carries
            veil = Image.new("RGBA", (w, h), (46, 38, 32, 96))
            art = Image.alpha_composite(art, veil)
        lg = fit_logo(logo, lw * w, lh * h)
        art.alpha_composite(lg, (int(lx * w + (lw * w - lg.width) / 2), int(ly * h + (lh * h - lg.height) / 2)))
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
