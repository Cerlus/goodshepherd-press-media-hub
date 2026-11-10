#!/usr/bin/env python3
"""The Good Shepherd key scene, drawn as layered cut paper (SVG): the day on the left, the
night on the right, the shepherd between them with the lamb across his shoulders.

One master, 3840 x 2160, with no lettering. Everything that matters sits in the band
y 780..2020 (the 3840 x 1240 library hero); the sky above it is there for tall formats.
Every other capsule is cropped from this by tools/brand.py.
"""
import math, random

W, H = 3840, 2160
INK, PAPER, GOLD, LAMP, WOOL, FACE = "#2e2620", "#f4ead6", "#efc57a", "#ffc483", "#fbf6ea", "#4a382c"


def grad(i, day, night, mid=0.52, soft=0.16):
    """A left-to-right gradient from a day colour to a night colour, turning near the shepherd."""
    return (f'<linearGradient id="g{i}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">'
            f'<stop offset="0" stop-color="{day}"/><stop offset="{mid-soft:.3f}" stop-color="{day}"/>'
            f'<stop offset="{mid+soft:.3f}" stop-color="{night}"/><stop offset="1" stop-color="{night}"/></linearGradient>')


def hill(i, pts, bottom=H):
    """A smooth ridge through pts (x, y), filled down to the bottom, with a cut-paper shadow."""
    d = f"M0,{bottom} L{pts[0][0]},{pts[0][1]} "
    for k in range(1, len(pts)):
        x0, y0 = pts[k - 1]
        x1, y1 = pts[k]
        mx = (x0 + x1) / 2
        d += f"C{mx},{y0} {mx},{y1} {x1},{y1} "
    d += f"L{W},{bottom} Z"
    return f'<path d="{d}" fill="url(#g{i})" filter="url(#paper)"/>'


def sheep(cx, cy, s=1.0, right=True, graze=False, lamb=False):
    d = 1 if right else -1
    puffs = [(-40, 0, 34), (-12, -24, 38), (26, -14, 34), (44, 10, 28), (8, 20, 36), (-30, 22, 30)]
    body = "".join(f'<circle cx="{cx+dx*s*d:.1f}" cy="{cy+dy*s:.1f}" r="{r*s:.1f}"/>' for dx, dy, r in puffs)
    hx, hy = cx + (62 if not graze else 58) * s * d, cy + (0 if not graze else 40) * s
    legs = "".join(f'<rect x="{cx+lx*s*d-6*s:.1f}" y="{cy+34*s:.1f}" width="{12*s:.1f}" height="{(40 if not lamb else 46)*s:.1f}" rx="{5*s:.1f}" fill="{FACE}"/>' for lx in (-28, -8, 18, 36))
    ear_rot = -25 * d
    shade = "".join('<circle cx="%.1f" cy="%.1f" r="%.1f"/>' % (cx + dx * s * d, cy + (dy + 16) * s, r * s * 0.62) for dx, dy, r in puffs[3:])
    return (f'<g filter="url(#paper)">{legs}<g fill="{WOOL}">{body}</g>'
            f'<g fill="#e6dcc6" opacity=".7">{shade}</g>'
            f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="{27*s:.1f}" ry="{23*s:.1f}" fill="{FACE}"/>'
            f'<ellipse cx="{hx-22*s*d:.1f}" cy="{hy-10*s:.1f}" rx="{16*s:.1f}" ry="{8*s:.1f}" fill="{FACE}" transform="rotate({ear_rot} {hx-22*s*d:.1f} {hy-10*s:.1f})"/>'
            f'<circle cx="{cx+(34*d)*s:.1f}" cy="{cy-34*s:.1f}" r="{17*s:.1f}" fill="{WOOL}"/>'
            f'<path d="M{hx-12*s:.1f},{hy-2*s:.1f} q{6*s:.1f},{7*s:.1f} {12*s:.1f},0 M{hx+3*s:.1f},{hy-2*s:.1f} q{6*s:.1f},{7*s:.1f} {12*s:.1f},0" stroke="{PAPER}" stroke-width="{3.4*s:.1f}" fill="none" stroke-linecap="round"/></g>')


def olive(x, y, s=1.0, leaf="#7d9a6a", lit="#a9bf8f"):
    blobs = [(-90, -250, 110), (40, -300, 130), (150, -230, 100), (-10, -200, 120), (90, -170, 90), (-120, -170, 80)]
    return (f'<g filter="url(#paper)"><path d="M{x-26*s},{y} C{x-10*s},{y-90*s} {x-50*s},{y-130*s} {x-20*s},{y-210*s} L{x+24*s},{y-210*s} C{x+50*s},{y-120*s} {x+10*s},{y-80*s} {x+30*s},{y} Z" fill="#6b4a2e"/>'
            f'<path d="M{x-4*s},{y-150*s} L{x-90*s},{y-240*s} M{x+8*s},{y-160*s} L{x+110*s},{y-230*s}" stroke="#6b4a2e" stroke-width="{22*s}" stroke-linecap="round"/></g>'
            f'<g filter="url(#paper)" fill="{leaf}">' + "".join(f'<ellipse cx="{x+bx*s}" cy="{y+by*s}" rx="{r*s}" ry="{r*s*0.62}"/>' for bx, by, r in blobs) + '</g>'
            f'<g fill="{lit}">' + "".join(f'<ellipse cx="{x+(bx+14)*s}" cy="{y+(by-22)*s}" rx="{r*s*0.62}" ry="{r*s*0.3}"/>' for bx, by, r in blobs[:4]) + '</g>')


def cloud(x, y, s=1.0, col=PAPER):
    return (f'<g filter="url(#paper)" fill="{col}"><ellipse cx="{x}" cy="{y}" rx="{170*s}" ry="{46*s}"/><circle cx="{x-70*s}" cy="{y-34*s}" r="{56*s}"/>'
            f'<circle cx="{x+10*s}" cy="{y-58*s}" r="{74*s}"/><circle cx="{x+88*s}" cy="{y-28*s}" r="{50*s}"/></g>')


def flower(x, y, s=1.0, col="#c9483c"):
    petals = "".join(f'<ellipse cx="{x+math.cos(a)*15*s:.1f}" cy="{y-70*s+math.sin(a)*15*s:.1f}" rx="{14*s}" ry="{11*s}" fill="{col}"/>' for a in [k * math.tau / 5 for k in range(5)])
    return (f'<g filter="url(#paper)"><path d="M{x},{y} q{-8*s},{-36*s} 0,{-66*s}" stroke="#4f7a48" stroke-width="{7*s}" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x},{y-26*s} q{24*s},{-18*s} {34*s},{-2*s} q{-20*s},{10*s} {-34*s},{2*s}z" fill="#5f8f55"/>{petals}<circle cx="{x}" cy="{y-70*s}" r="{8*s}" fill="{INK}"/></g>')


def tuft(x, y, s=1.0, col="#5f8f55"):
    blades = "".join(f'<path d="M{x+dx*s},{y} q{lean*s},{-h*s*0.6} {lean*1.6*s},{-h*s} q{-lean*0.2*s},{h*s*0.55} {(16-lean*1.6)*s},{h*s}z" fill="{col}"/>' for dx, lean, h in [(-36, -14, 70), (-14, -4, 104), (10, 8, 84), (30, 18, 62)])
    return f'<g filter="url(#paper)">{blades}</g>'


def cave(x, y, s=1.0):
    """A stone arch with the dark behind it and eyes in the dark."""
    stones = ""
    n = 9
    for k in range(n):
        a = math.pi * (1.0 - k / (n - 1))
        cx, cy = x + math.cos(a) * 250 * s, y - math.sin(a) * 230 * s
        stones += f'<rect x="{cx-52*s:.1f}" y="{cy-44*s:.1f}" width="{104*s:.1f}" height="{88*s:.1f}" rx="{22*s:.1f}" fill="{"#5d5468" if k % 2 else "#6e6478"}" transform="rotate({90-math.degrees(a):.1f} {cx:.1f} {cy:.1f})"/>'
    eyes = "".join(f'<path d="M{ex-20*s},{ey} q{20*s},{-14*s} {40*s},0 q{-20*s},{9*s} {-40*s},0z" fill="#f2c64e"/><path d="M{ex+50*s},{ey} q{20*s},{-14*s} {40*s},0 q{-20*s},{9*s} {-40*s},0z" fill="#f2c64e"/>'
                   for ex, ey in [(x - 120 * s, y - 70 * s), (x + 30 * s, y - 28 * s)])
    return (f'<g filter="url(#paper)"><path d="M{x-212*s},{y+20*s} L{x-212*s},{y-40*s} A{212*s},{200*s} 0 0 1 {x+212*s},{y-40*s} L{x+212*s},{y+20*s} Z" fill="#0f0b18"/>'
            f'<ellipse cx="{x}" cy="{y-20*s}" rx="{150*s}" ry="{90*s}" fill="#3a2a1c" opacity=".55"/>{eyes}</g><g filter="url(#paper)">{stones}'
            f'<rect x="{x-300*s}" y="{y-40*s}" width="{96*s}" height="{90*s}" rx="{20*s}" fill="#5d5468"/><rect x="{x+204*s}" y="{y-40*s}" width="{96*s}" height="{90*s}" rx="{20*s}" fill="#6e6478"/></g>')


def bare_tree(x, y, s=1.0, col="#1a1530"):
    return (f'<g filter="url(#paper)" stroke="{col}" stroke-linecap="round" fill="none"><path d="M{x},{y} C{x-10*s},{y-120*s} {x+20*s},{y-200*s} {x},{y-320*s}" stroke-width="{34*s}"/>'
            f'<path d="M{x+4*s},{y-200*s} q{90*s},{-50*s} {120*s},{-150*s} M{x},{y-250*s} q{-80*s},{-40*s} {-110*s},{-130*s} M{x},{y-320*s} q{30*s},{-70*s} {10*s},{-140*s} M{x+86*s},{y-290*s} q{50*s},{-10*s} {80*s},{-60*s} M{x-80*s},{y-330*s} q{-40*s},{-10*s} {-60*s},{-70*s}" stroke-width="{16*s}"/></g>')


def wolf(x, y, s=1.0, col="#17122a"):
    """A wolf on the ridge, head up, seen against the night."""
    return (f'<g filter="url(#paper)" fill="{col}"><path d="M{x-150*s},{y} L{x-140*s},{y-90*s} Q{x-150*s},{y-150*s} {x-80*s},{y-150*s} L{x+40*s},{y-160*s} Q{x+70*s},{y-200*s} {x+96*s},{y-250*s} L{x+104*s},{y-290*s} L{x+124*s},{y-256*s} L{x+150*s},{y-282*s} L{x+152*s},{y-240*s} L{x+214*s},{y-212*s} L{x+160*s},{y-190*s} Q{x+130*s},{y-120*s} {x+110*s},{y-90*s} L{x+116*s},{y} L{x+84*s},{y} L{x+70*s},{y-80*s} L{x-70*s},{y-76*s} L{x-100*s},{y} Z"/>'
            f'<path d="M{x-140*s},{y-120*s} q{-80*s},{20*s} {-110*s},{90*s} q{60*s},{-30*s} {120*s},{-40*s}z"/></g><path d="M{x+138*s},{y-232*s} l{22*s},{-6*s} l{-16*s},{12*s}z" fill="#f2c64e"/>')


def shepherd(x, y, s=1.0):
    """The shepherd, feet at (x, y): robe and sash, headcloth, a kind face, the lamb across
    his shoulders with its legs held at his chest, the crook in his other hand, a lamp on it."""
    robe, robe_d, robe_l = "#8a5a36", "#6f4428", "#a8713f"
    skin, beard, cloth = "#b98458", "#3d2a1e", "#efe6d2"
    P = lambda dx, dy: f"{x+dx*s:.1f},{y+dy*s:.1f}"
    out = []
    # ground shadow
    out.append(f'<ellipse cx="{x}" cy="{y+6*s}" rx="{300*s}" ry="{34*s}" fill="#1c1420" opacity=".35"/>')
    # the crook, behind his hand, with the lamp
    sx, top = x - 300 * s, y - 1010 * s
    hook = f"M{sx},{y+10*s} L{sx},{top+120*s} C{sx},{top-40*s} {sx-200*s},{top-40*s} {sx-200*s},{top+96*s} C{sx-200*s},{top+132*s} {sx-176*s},{top+150*s} {sx-150*s},{top+140*s}"
    out.append(f'<g filter="url(#paper)"><path d="{hook}" fill="none" stroke="#5a3d26" stroke-width="{40*s}" stroke-linecap="round"/><path d="M{sx-8*s},{y} L{sx-8*s},{top+130*s}" stroke="#7a573a" stroke-width="{9*s}" stroke-linecap="round" opacity=".8"/></g>')
    lx, ly = sx - 200 * s, top + 290 * s
    out.append(f'<line x1="{lx}" y1="{top+120*s}" x2="{lx}" y2="{ly-10*s}" stroke="{INK}" stroke-width="{7*s}"/>'
               f'<circle cx="{lx}" cy="{ly}" r="{210*s}" fill="url(#lampglow)"/>'
               f'<g filter="url(#paper)"><path d="M{lx-74*s},{ly} L{lx+62*s},{ly} L{lx+104*s},{ly-20*s} L{lx+92*s},{ly+12*s} Q{lx+56*s},{ly+62*s} {lx-6*s},{ly+62*s} Q{lx-64*s},{ly+58*s} {lx-74*s},{ly}z" fill="#a4552c"/>'
               f'<path d="M{lx-50*s},{ly+14*s} L{lx+54*s},{ly+14*s}" stroke="#c97a48" stroke-width="{9*s}" stroke-linecap="round"/></g>'
               f'<path d="M{lx+98*s},{ly-22*s} q{-30*s},{-38*s} {4*s},{-86*s} q{30*s},{46*s} {-4*s},{86*s}z" fill="{GOLD}"/><path d="M{lx+98*s},{ly-26*s} q{-14*s},{-20*s} {2*s},{-46*s} q{14*s},{24*s} {-2*s},{46*s}z" fill="{PAPER}"/>')
    # robe: a broad bell, a lighter panel on the day side, darker folds on the night side
    out.append(f'<g filter="url(#paper)"><path d="M{P(-150,-690)} C{P(-190,-400)} {P(-260,-150)} {P(-290,0)} L{P(290,0)} C{P(260,-150)} {P(190,-400)} {P(150,-690)} Z" fill="{robe}"/>'
               f'<path d="M{P(-150,-690)} C{P(-190,-400)} {P(-260,-150)} {P(-290,0)} L{P(-110,0)} C{P(-100,-260)} {P(-70,-480)} {P(-50,-690)} Z" fill="{robe_l}"/>'
               f'<path d="M{P(60,-690)} C{P(80,-420)} {P(120,-180)} {P(140,0)} L{P(290,0)} C{P(260,-150)} {P(190,-400)} {P(150,-690)} Z" fill="{robe_d}"/>'
               f'<path d="M{P(-20,-420)} C{P(-10,-280)} {P(-20,-140)} {P(-40,0)}" stroke="{robe_d}" stroke-width="{9*s}" fill="none" opacity=".7"/></g>')
    # sash and its tail
    out.append(f'<g filter="url(#paper)"><path d="M{P(-196,-420)} Q{P(0,-380)} {P(196,-420)} L{P(204,-360)} Q{P(0,-318)} {P(-204,-360)} Z" fill="{GOLD}"/>'
               f'<path d="M{P(-30,-372)} L{P(22,-372)} L{P(34,-200)} L{P(-4,-230)} L{P(-42,-200)} Z" fill="#d9a85a"/></g>')
    # the lamb across his shoulders: body behind the neck, head by his right (our right) shoulder
    puffs = [(-250, -760, 86), (-150, -800, 96), (-40, -812, 90), (70, -812, 92), (170, -796, 96), (262, -760, 84), (-200, -720, 80), (200, -720, 80)]
    out.append(f'<g filter="url(#paper)" fill="{WOOL}">' + "".join(f'<circle cx="{x+px*s:.1f}" cy="{y+py*s:.1f}" r="{r*s:.1f}"/>' for px, py, r in puffs) + '</g>')
    out.append(f'<g fill="#e6dcc6" opacity=".8">' + "".join(f'<circle cx="{x+px*s:.1f}" cy="{y+(py+34)*s:.1f}" r="{r*s*0.6:.1f}"/>' for px, py, r in puffs[:6]) + '</g>')
    # shoulders and arms over the robe: both arms come up to hold the lamb's legs at his chest
    out.append(f'<g filter="url(#paper)"><path d="M{P(-200,-700)} Q{P(-250,-560)} {P(-150,-520)} L{P(-60,-560)} L{P(-70,-640)} Q{P(-130,-640)} {P(-140,-720)} Z" fill="{robe_l}"/>'
               f'<path d="M{P(200,-700)} Q{P(250,-560)} {P(150,-520)} L{P(60,-560)} L{P(70,-640)} Q{P(130,-640)} {P(140,-720)} Z" fill="{robe_d}"/></g>')
    # the robe's neck, closing the chest under the beard
    out.append(f'<path d="M{P(-150,-700)} L{P(150,-700)} L{P(96,-540)} L{P(-96,-540)} Z" fill="{robe}"/><path d="M{P(-40,-700)} L{P(40,-700)} L{P(0,-610)} Z" fill="{robe_d}"/>')
    # lamb's legs hanging down his chest, one pair each side, and the hands that hold them
    for d in (-1, 1):
        out.append(f'<g filter="url(#paper)"><rect x="{x+(d*118-17)*s:.1f}" y="{y-760*s:.1f}" width="{34*s:.1f}" height="{220*s:.1f}" rx="{15*s:.1f}" fill="{WOOL}"/>'
                   f'<rect x="{x+(d*78-15)*s:.1f}" y="{y-760*s:.1f}" width="{30*s:.1f}" height="{206*s:.1f}" rx="{14*s:.1f}" fill="#efe7d6"/>'
                   f'<rect x="{x+(d*118-19)*s:.1f}" y="{y-566*s:.1f}" width="{38*s:.1f}" height="{34*s:.1f}" rx="{10*s:.1f}" fill="{FACE}"/><rect x="{x+(d*78-17)*s:.1f}" y="{y-578*s:.1f}" width="{34*s:.1f}" height="{30*s:.1f}" rx="{10*s:.1f}" fill="{FACE}"/>'
                   f'<ellipse cx="{x+d*98*s:.1f}" cy="{y-640*s:.1f}" rx="{58*s:.1f}" ry="{44*s:.1f}" fill="{skin}"/>'
                   f'<path d="M{x+(d*98-40)*s:.1f},{y-650*s:.1f} h{80*s:.1f} M{x+(d*98-40)*s:.1f},{y-630*s:.1f} h{80*s:.1f}" stroke="#9a6a44" stroke-width="{5*s:.1f}" opacity=".6"/></g>')
    # the lamb's head resting by his shoulder, ear and a sleepy eye
    hx, hy = x + 300 * s, y - 800 * s
    out.append(f'<g filter="url(#paper)"><ellipse cx="{hx}" cy="{hy}" rx="{64*s}" ry="{54*s}" fill="{FACE}"/><ellipse cx="{hx+44*s}" cy="{hy-40*s}" rx="{36*s}" ry="{17*s}" fill="{FACE}" transform="rotate(30 {hx+44*s} {hy-40*s})"/>'
               f'<circle cx="{hx-40*s}" cy="{hy-46*s}" r="{40*s}" fill="{WOOL}"/></g>'
               f'<path d="M{hx-22*s},{hy-4*s} q{14*s},{14*s} {28*s},0" stroke="{PAPER}" stroke-width="{6*s}" fill="none" stroke-linecap="round"/><ellipse cx="{hx+34*s}" cy="{hy+22*s}" rx="{12*s}" ry="{8*s}" fill="#2c211a"/>')
    # head: the cloth, the face, the beard, the band
    out.append(f'<g filter="url(#paper)"><path d="M{P(-150,-900)} C{P(-160,-1070)} {P(160,-1070)} {P(150,-900)} L{P(176,-700)} Q{P(120,-680)} {P(96,-740)} L{P(-96,-740)} Q{P(-120,-680)} {P(-176,-700)} Z" fill="{cloth}"/>'
               f'<path d="M{P(40,-1024)} C{P(150,-1000)} {P(150,-900)} {P(150,-900)} L{P(176,-700)} Q{P(120,-680)} {P(96,-740)} Z" fill="#d9cdb4"/></g>')
    out.append(f'<g filter="url(#paper)"><path d="M{P(-92,-900)} Q{P(-96,-990)} {P(0,-992)} Q{P(96,-990)} {P(92,-900)} L{P(92,-840)} Q{P(0,-720)} {P(-92,-840)} Z" fill="{skin}"/></g>'
               f'<path d="M{P(-94,-860)} Q{P(-60,-838)} {P(-40,-856)} Q{P(0,-838)} {P(40,-856)} Q{P(60,-838)} {P(94,-860)} L{P(92,-822)} Q{P(60,-716)} {P(0,-706)} Q{P(-60,-716)} {P(-92,-822)} Z" fill="{beard}"/>'
               f'<path d="M{P(-24,-822)} Q{P(0,-806)} {P(24,-822)}" stroke="#b98458" stroke-width="{7*s}" fill="none" stroke-linecap="round"/>'
               f'<path d="M{P(-60,-912)} q{20*s},{16*s} {40*s},0 M{P(20,-912)} q{20*s},{16*s} {40*s},0" stroke="{INK}" stroke-width="{8*s}" fill="none" stroke-linecap="round"/>'
               f'<path d="M{P(-66,-940)} q{26*s},{-14*s} {50*s},{-2*s} M{P(16,-942)} q{26*s},{-12*s} {50*s},{2*s}" stroke="{beard}" stroke-width="{9*s}" fill="none" stroke-linecap="round"/>'
               f'<path d="M{P(-6,-900)} q{-10*s},{30*s} {8*s},{38*s}" stroke="#9a6a44" stroke-width="{6*s}" fill="none" stroke-linecap="round"/>')
    out.append(f'<path d="M{P(-148,-952)} Q{P(0,-1010)} {P(148,-952)} L{P(150,-918)} Q{P(0,-976)} {P(-150,-918)} Z" fill="#c9483c"/>')
    # the hand on the crook
    out.append(f'<g filter="url(#paper)"><path d="M{P(-196,-690)} Q{P(-330,-640)} {P(-330,-560)} L{P(-270,-540)} Q{P(-250,-610)} {P(-160,-640)} Z" fill="{robe_l}"/><ellipse cx="{sx+4*s}" cy="{y-548*s}" rx="{44*s}" ry="{50*s}" fill="{skin}"/></g>')
    return "".join(out)


def scene():
    rnd = random.Random(7)
    d = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>'
         f'<filter id="paper" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="14" stdDeviation="12" flood-color="#150e1e" flood-opacity=".3"/></filter>'
         f'<linearGradient id="sky" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0"><stop offset="0" stop-color="#a9cde2"/><stop offset=".3" stop-color="#d9e6dc"/><stop offset=".47" stop-color="#f6dca4"/>'
         f'<stop offset=".56" stop-color="#e79a6c"/><stop offset=".66" stop-color="#7a4f86"/><stop offset=".8" stop-color="#2f2558"/><stop offset="1" stop-color="#151030"/></linearGradient>'
         f'<linearGradient id="skyv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c0a22" stop-opacity=".32"/><stop offset=".55" stop-color="#0c0a22" stop-opacity="0"/></linearGradient>'
         f'<radialGradient id="sunglow"><stop offset="0" stop-color="#fff3cf" stop-opacity=".9"/><stop offset="1" stop-color="#fff3cf" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="lampglow"><stop offset="0" stop-color="{LAMP}" stop-opacity=".9"/><stop offset=".4" stop-color="{LAMP}" stop-opacity=".35"/><stop offset="1" stop-color="{LAMP}" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="lampspill" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{LAMP}" stop-opacity=".42"/><stop offset="1" stop-color="{LAMP}" stop-opacity="0"/></radialGradient>'
         + grad(1, "#c6dcc8", "#4b3f78") + grad(2, "#a3c394", "#3a2f62") + grad(3, "#84ab72", "#2c2450") + grad(4, "#6f995f", "#221b40") + grad(5, "#c9804a", "#191430", 0.54, 0.12)
         + '</defs>']
    d.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/><rect width="{W}" height="{H}" fill="url(#skyv)"/>')
    # stars and the moon on the night side
    for _ in range(90):
        sx = rnd.uniform(2350, W - 20)
        sy = rnd.uniform(30, 1180)
        r = rnd.choice([3, 4, 5, 7])
        d.append(f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{r}" fill="{PAPER}" opacity="{rnd.uniform(0.35, 0.95) * min(1.0, (sx - 2300) / 500):.2f}"/>')
    for sx, sy, r in [(2760, 520, 22), (3560, 300, 26), (3040, 880, 18), (3700, 960, 20), (2900, 1000, 14)]:
        d.append(f'<path d="M{sx},{sy-r} L{sx+r*0.25},{sy-r*0.25} L{sx+r},{sy} L{sx+r*0.25},{sy+r*0.25} L{sx},{sy+r} L{sx-r*0.25},{sy+r*0.25} L{sx-r},{sy} L{sx-r*0.25},{sy-r*0.25}Z" fill="{PAPER}"/>')
    d.append(f'<g filter="url(#paper)"><path d="M3330,560 a170,170 0 1,0 135,305 a143,143 0 1,1 -135,-305z" fill="#f6ecd2"/></g>')
    # the sun, its glow, and paper clouds on the day side
    d.append(f'<circle cx="900" cy="960" r="560" fill="url(#sunglow)"/><g filter="url(#paper)"><circle cx="900" cy="960" r="190" fill="{GOLD}"/></g><circle cx="900" cy="960" r="142" fill="#f8dfa2"/>')
    d.append(cloud(330, 900, 1.1) + cloud(1500, 330, 1.0, "#fbf3e0") + cloud(1330, 1010, 0.7, "#fbf3e0") + cloud(2560, 940, 0.8, "#9a7aa6") + cloud(520, 300, 1.2) + cloud(2900, 380, 0.9, "#5a477e"))
    # far hills, a lone wolf on the night ridge
    d.append(hill(1, [(0, 1250), (520, 1130), (1100, 1230), (1700, 1100), (2300, 1200), (2900, 1060), (3400, 1160), (W, 1100)]))
    d.append(wolf(3010, 1068, 0.62))
    d.append(olive(1560, 1150, 0.62, "#93b086", "#b4caa2") + olive(420, 1168, 0.5, "#93b086", "#b4caa2"))
    # middle hills: the fold and its olive on the day side, a bare tree on the night side
    d.append(hill(2, [(0, 1430), (600, 1330), (1300, 1440), (1900, 1350), (2600, 1450), (3200, 1330), (W, 1420)]))
    d.append(olive(1080, 1420, 1.0))
    fold = "".join(f'<rect x="{560+k*74}" y="{1318+abs(k-3.5)*5:.0f}" width="80" height="62" rx="18" fill="{"#cdbf9f" if k % 2 else "#b8a98a"}"/>' for k in range(8) if k not in (3, 4))
    d.append(f'<g filter="url(#paper)">{fold}<rect x="772" y="1290" width="16" height="90" rx="6" fill="#6b4a2e"/><rect x="856" y="1290" width="16" height="90" rx="6" fill="#6b4a2e"/></g>')
    d.append(bare_tree(2700, 1440, 0.9))
    d.append(sheep(420, 1330, 0.62) + sheep(1420, 1392, 0.56, False, True))
    # near hills: the flock, the cave
    d.append(hill(3, [(0, 1640), (500, 1540), (1200, 1650), (1900, 1560), (2500, 1660), (3100, 1560), (W, 1640)]))
    d.append(cave(3080, 1640, 1.0))
    d.append(sheep(250, 1560, 1.0, True) + sheep(680, 1520, 0.8, False, True) + sheep(1080, 1610, 0.95, True, True) + sheep(1500, 1580, 0.8, False) + sheep(860, 1650, 0.5, True, False, True))
    d.append(hill(4, [(0, 1830), (700, 1760), (1500, 1850), (2100, 1780), (2800, 1860), (3400, 1790), (W, 1850)]))
    d.append(sheep(420, 1800, 1.3, True) + sheep(1330, 1820, 1.1, False, True) + sheep(1010, 1840, 0.62, True, False, True))
    # the lamp's light spilling toward the night
    d.append(f'<ellipse cx="2020" cy="1500" rx="900" ry="620" fill="url(#lampspill)"/>')
    d.append(shepherd(2030, 1960, 1.0))
    # foreground: warm earth by day, cold by night, flowers and grass
    d.append(hill(5, [(0, 2010), (600, 1960), (1300, 2020), (2000, 1985), (2700, 2030), (3300, 1975), (W, 2020)]))
    for fx, fy, fs in [(180, 2110, 1.3), (640, 2090, 1.0), (1180, 2120, 1.2), (1640, 2100, 0.9)]:
        d.append(flower(fx, fy, fs))
    for tx, ty, ts, col in [(60, 2150, 1.3, "#5f8f55"), (420, 2130, 1.0, "#6f9c5f"), (900, 2150, 1.4, "#5f8f55"), (1420, 2140, 1.1, "#6f9c5f"), (1860, 2150, 1.0, "#5a7a55"),
                            (2380, 2150, 1.2, "#2c2550"), (2760, 2140, 1.0, "#342c5c"), (3200, 2150, 1.4, "#2c2550"), (3600, 2140, 1.1, "#342c5c")]:
        d.append(tuft(tx, ty, ts, col))
    d.append('</svg>')
    return "".join(d)


if __name__ == "__main__":
    import sys
    open(sys.argv[1] if len(sys.argv) > 1 else "scene.svg", "w").write(scene())
