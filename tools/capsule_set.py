#!/usr/bin/env python3
"""The shipped look (chosen 2026-11-28): bolder day-to-night colour, the blended logo
(tools/logo_drafts.py, #6 and its one-line #7), a night-indigo outline round the shepherd,
the cards and the letters, and a slim gold-to-blue edge round each capsule.

    python3 tools/capsule_set.py           every capsule into lab/capsules/set/ + sheet.png
    python3 tools/capsule_set.py --ship    also over assets/branding (capsules, logos, the hero,
                                           key art, page background, social banners) and previews
"""
import os, sys, subprocess
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene as S
import brand
import capsule_lab as L
import capsule_drafts as D
import logo_drafts as LG

ROOT, B = brand.ROOT, brand.B
OUT = os.path.join(ROOT, "lab", "capsules", "set")
D.OUT = OUT
D.DRAFTS = {"set": {"title": "blend", "frame": True}, "small": {"title": "blend", "frame": True}}
C3 = lambda y, k: [("staff", 0.585, y + 0.06, k, -13), ("rod", 0.895, y + 0.06, k, 13), ("bond", 0.74, y, k + 0.04, 0)]
D.FORMATS = {
    "main": {"size": (1232, 706), "crop": (980, 735, 900), "logo": (0.488, 0.04, 0.495, 0.54), "cards": C3(0.91, 0.56)},
    "header": {"size": (920, 430), "crop": (980, 735, 900), "logo": (0.488, 0.035, 0.495, 0.56), "cards": C3(0.955, 0.55)},
    "small": {"size": (462, 174), "crop": (1215, 690, 760), "logo": (0.30, 0.045, 0.675, 0.91), "cards": []},
    "package": {"size": (1414, 464), "crop": (880, 740, 880), "logo": (0.345, 0.05, 0.37, 0.90),
                "cards": [("staff", 0.775, 0.84, 0.70, -12), ("rod", 0.925, 0.84, 0.70, 12), ("bond", 0.85, 0.76, 0.76, 0)]},
    "vertical": {"size": (748, 896), "crop": (790, 240, 1790), "logo": (0.07, 0.022, 0.86, 0.235),
                 "cards": [("staff", 0.27, 0.93, 0.30, -14), ("rod", 0.73, 0.93, 0.30, 14), ("bond", 0.5, 0.90, 0.33, 0)]},
    "library": {"size": (600, 900), "crop": (906, 240, 1790), "logo": (0.06, 0.022, 0.88, 0.215),
                "cards": [("staff", 0.24, 0.93, 0.29, -14), ("rod", 0.76, 0.93, 0.29, 14), ("bond", 0.5, 0.90, 0.32, 0)]},
}
SHIP = dict(L.SHIP)


def on_canvas(lg, w, h, pad=0.04):
    """A logo cropped to its ink and centred on a transparent w x h canvas."""
    lg = brand.fit_logo(lg, w * (1 - pad * 2), h * (1 - pad * 2))
    c = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    c.alpha_composite(lg, ((w - lg.width) // 2, (h - lg.height) // 2))
    return c


def main():
    os.makedirs(OUT, exist_ok=True)
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "logo_drafts.py"), "--only", "6-blend"], check=True)
    D.raster([("d_mark_circle", LG.mark("circle"), 1024, 1024), ("d_mark_app", LG.mark("squircle"), 1024, 1024)])
    extra = f'<ellipse cx="1500" cy="1500" rx="900" ry="620" fill="url(#lampspill)"/>' + S.cloud(1050, 1010, 0.8) + S.cloud(700, 620, 1.0)
    D.raster([("d_bg", D.bold(L.backdrop(extra)), D.W, D.H), ("d_man", D.bold(L.defs() + S.shepherd(1500, 1960, 1.0, "upright") + "</svg>"), D.W, D.H),
              ("d_scene", D.bold(S.scene()), D.W, D.H)])
    T = lambda n: Image.open(os.path.join(D.TMP, n + ".png"))
    stack = Image.open(os.path.join(ROOT, "lab", "logos", "6-blend.png")).convert("RGBA")
    line = Image.open(os.path.join(ROOT, "lab", "logos", "7-blend-one-line.png")).convert("RGBA")
    plain = Image.open(os.path.join(ROOT, "lab", "logos", "8-blend-plain.png")).convert("RGBA")   # the small capsule: letters only, as tall as it allows
    made = {f: D.build("set", f, T("d_bg").convert("RGB"), T("d_man").convert("RGBA"), {"blend": plain if f == "small" else stack}) for f in D.FORMATS}
    sheet = Image.new("RGB", (1454 + 748 + 20 + 600 + 20, 1680), (27, 40, 56))
    for f, at in (("main", (20, 20)), ("package", (20, 746)), ("header", (20, 1230)), ("small", (960, 1230)), ("vertical", (1454, 20)), ("library", (2222, 20))):
        sheet.paste(made[f], at)
    sheet.paste(made["small"].resize((231, 87), Image.LANCZOS), (960, 1424)); sheet.paste(made["header"].resize((231, 108), Image.LANCZOS), (1210, 1424))
    sheet.save(os.path.join(OUT, "sheet.png"))
    if "--ship" not in sys.argv:
        return
    pv = lambda im, name: (im if im.width <= 1280 else im.resize((1280, int(im.height * 1280 / im.width)), Image.LANCZOS)).convert("RGB").save(os.path.join(ROOT, "assets", "previews", name + ".jpg"), quality=86)
    for f, im in made.items():
        im.save(os.path.join(B, "steam", SHIP[f])); pv(im, f)
    # the logos: transparent PNGs and their vector sources (outlined paths, no font needed)
    on_canvas(stack, 1280, 720).save(os.path.join(B, "steam", "library-logo-1280x720.png"))
    on_canvas(stack, 1280, 720).save(os.path.join(B, "logo", "logo-stacked-1280x720.png"))
    on_canvas(line, 1500, 330, 0.02).save(os.path.join(B, "logo", "logo-one-line-1500x330.png"))
    open(os.path.join(B, "logo", "logo-stacked.svg"), "w").write(LG.d6())
    open(os.path.join(B, "logo", "logo-one-line.svg"), "w").write(LG.d7())
    # the emblem (avatar) and the app icon, in the same look
    open(os.path.join(B, "logo", "mark-circle.svg"), "w").write(LG.mark("circle"))
    open(os.path.join(B, "logo", "mark-app.svg"), "w").write(LG.mark("squircle"))
    T("d_mark_circle").convert("RGBA").resize((800, 800), Image.LANCZOS).save(os.path.join(B, "social", "avatar-800x800.png"))
    app = T("d_mark_app").convert("RGBA")
    app.save(os.path.join(B, "logo", "app-icon-1024.png"))
    for n in (512, 256, 128, 64, 32):
        app.resize((n, n), Image.LANCZOS).save(os.path.join(B, "logo", f"app-icon-{n}.png"))
    app.save(os.path.join(B, "logo", "app-icon.ico"), sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    # the wide illustration in the same colours: the master, the library hero (no lettering), the page background
    master = T("d_scene").convert("RGB")
    master.save(os.path.join(B, "source", "key-scene-3840x2160.png"))
    master.crop((0, 800, 3840, 2040)).save(os.path.join(B, "steam", "library-hero-3840x1240.png"))
    pv(master.crop((0, 800, 3840, 2040)).resize((1920, 620), Image.LANCZOS), "hero")
    master.resize((1438, 810), Image.LANCZOS).save(os.path.join(B, "steam", "page-background-1438x810.png"))
    plan = [("goodshepherd-key-art-1920x1080.png", (1920, 1080), 0.50, 1.0, (0.595, 0.045, 0.385, 0.36), "key-art"),
            ("social/x-bluesky-header-1500x500.png", (1500, 500), 0.58, 0.90, (0.60, 0.06, 0.38, 0.66), None),
            ("social/youtube-banner-2560x1440.png", (2560, 1440), 0.50, 1.0, (0.575, 0.355, 0.225, 0.21), None),
            ("social/portrait-post-1080x1350.png", (1080, 1350), 0.53, 1.0, (0.08, 0.12, 0.84, 0.27), "portrait")]
    for name, (w, h), fx, fy, (lx, ly, lw, lh), prev in plan:
        art = brand.crop_art(master, w, h, fx, fy).convert("RGBA")
        lg = brand.fit_logo(stack, lw * w, lh * h)
        art.alpha_composite(lg, (int(lx * w + (lw * w - lg.width) / 2), int(ly * h + (lh * h - lg.height) / 2)))
        art.convert("RGB").save(os.path.join(B, name))
        if prev:
            pv(art, prev)
        if prev == "key-art":
            art.convert("RGB").save(os.path.join(ROOT, "assets", "previews", "key-art-hero.jpg"), quality=86)


if __name__ == "__main__":
    main()
