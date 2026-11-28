#!/usr/bin/env python3
"""The wide key scene, redrawn with more in it (2026-11-28): mountains behind the hills, a
proper stone sheepfold with a shelter and a gate, sheep with wool, faces and feet, a den in
a rock outcrop with wolves in its dark. 3840 x 2160, no lettering; the top-centre sky is
kept clear for the title. The shepherd, olives, clouds and the ridge wolf are scene.py's.
"""
import math, random
import scene as S

W, H = S.W, S.H
PAPER, GOLD, WOOL, FACE, EDGE = "#f4ead6", "#f5b53a", "#fffaf0", "#3f2f28", "#1b1240"


def dn(i, day, night, mid=0.52, soft=0.15):
    return (f'<linearGradient id="{i}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0"><stop offset="{mid-soft:.3f}" stop-color="{day}"/>'
            f'<stop offset="{mid+soft:.3f}" stop-color="{night}"/></linearGradient>')


def ridge(fill, pts, bottom=H, flt="paper"):
    d = f"M0,{bottom} L{pts[0][0]},{pts[0][1]} "
    for k in range(1, len(pts)):
        (x0, y0), (x1, y1) = pts[k - 1], pts[k]
        mx = (x0 + x1) / 2
        d += f"C{mx},{y0} {mx},{y1} {x1},{y1} "
    return f'<path d="{d}L{W},{bottom} Z" fill="{fill}" filter="url(#{flt})"/>'


def peaks(fill, snow, base, tops, seed):
    """A jagged mountain line: (x, height) tops joined by straight cuts, snow on the high ones."""
    r = random.Random(seed)
    pts = [(0, base)]
    for x, h in tops:
        pts += [(x - r.uniform(150, 230), base - h * 0.35), (x, base - h), (x + r.uniform(150, 230), base - h * 0.4)]
    pts.append((W, base))
    d = "M0,%d " % H + " ".join(f"L{x:.0f},{y:.0f}" for x, y in pts) + f" L{W},{H} Z"
    caps = "".join(f'<path d="M{x},{base-h} l{-h*0.2:.0f},{h*0.26:.0f} l{h*0.09:.0f},{-h*0.05:.0f} l{h*0.08:.0f},{h*0.08:.0f} l{h*0.07:.0f},{-h*0.09:.0f} l{h*0.16:.0f},{h*0.06:.0f}z" fill="url(#{snow})"/>' for x, h in tops if h > 250)
    return f'<g filter="url(#paper)"><path d="{d}" fill="url(#{fill})"/></g>{caps}'


def sheep(cx, cy, s=1.0, right=True, pose="stand", black=False, bell=False, awake=True, lamb=False):
    """A sheep in cut paper: legs with hooves, a wool cloud with a shaded underside and a lit top,
    a tail, a dark face with an ear, an eye and a nose, a tuft on its head."""
    d = 1 if right else -1
    wool, shade, lit = (("#40394a", "#2c2634", "#575063") if black else (WOOL, "#e3d8c2", "#ffffff"))
    face, hoof = ("#17131c" if black else FACE), "#241a16"
    X = lambda dx: cx + dx * s * d
    Y = lambda dy: cy + dy * s
    o = []
    lying = pose == "lie"
    if not lying:
        ll = 46 if lamb else 40
        for lx in (-30, -10, 16, 34):
            o.append(f'<rect x="{X(lx)-6*s:.1f}" y="{Y(30):.1f}" width="{12*s:.1f}" height="{ll*s:.1f}" rx="{5*s:.1f}" fill="{face}"/><rect x="{X(lx)-7*s:.1f}" y="{Y(30+ll-9):.1f}" width="{14*s:.1f}" height="{10*s:.1f}" rx="{4*s:.1f}" fill="{hoof}"/>')
    else:
        o.append(f'<ellipse cx="{X(26):.1f}" cy="{Y(40):.1f}" rx="{22*s:.1f}" ry="{8*s:.1f}" fill="{face}"/><ellipse cx="{X(-20):.1f}" cy="{Y(42):.1f}" rx="{20*s:.1f}" ry="{7*s:.1f}" fill="{face}"/>')
    puffs = [(-44, 2, 32), (-16, -24, 38), (22, -18, 36), (46, 6, 30), (10, 18, 36), (-26, 22, 32), (-58, -12, 20), (34, -34, 20)]
    if lying:
        puffs = [(px, py * 0.7 + 14, r) for px, py, r in puffs]
    o.append(f'<circle cx="{X(-74):.1f}" cy="{Y(-2 if not lying else 16):.1f}" r="{13*s:.1f}" fill="{wool}"/>')   # tail
    o.append(f'<g fill="{wool}">' + "".join(f'<circle cx="{X(px):.1f}" cy="{Y(py):.1f}" r="{r*s:.1f}"/>' for px, py, r in puffs) + '</g>')
    o.append(f'<g fill="{shade}">' + "".join(f'<circle cx="{X(px):.1f}" cy="{Y(py+15):.1f}" r="{r*s*0.6:.1f}"/>' for px, py, r in puffs[3:6]) + '</g>')
    o.append(f'<g fill="{lit}" opacity=".9">' + "".join(f'<circle cx="{X(px-4):.1f}" cy="{Y(py-9):.1f}" r="{r*s*0.5:.1f}"/>' for px, py, r in puffs[1:3]) + '</g>')
    o.append("".join(f'<path d="M{X(px)-9*s:.1f},{Y(py):.1f} q{9*s:.1f},{8*s:.1f} {18*s:.1f},0" stroke="{shade}" stroke-width="{3*s:.1f}" fill="none" stroke-linecap="round"/>' for px, py in ((-30, 0), (4, -6), (-8, 26))))
    hx, hy = X(66), Y(-2 if pose != "graze" else 36)
    if lying:
        hy = Y(14)
    o.append(f'<ellipse cx="{hx-20*s*d:.1f}" cy="{hy-13*s:.1f}" rx="{17*s:.1f}" ry="{8*s:.1f}" fill="{face}" transform="rotate({-28*d} {hx-20*s*d:.1f} {hy-13*s:.1f})"/>')
    o.append(f'<ellipse cx="{hx:.1f}" cy="{hy:.1f}" rx="{27*s:.1f}" ry="{23*s:.1f}" fill="{face}"/><ellipse cx="{hx+16*s*d:.1f}" cy="{hy+8*s:.1f}" rx="{13*s:.1f}" ry="{11*s:.1f}" fill="{"#2a2230" if black else "#54413a"}"/>')
    o.append(f'<circle cx="{hx-16*s*d:.1f}" cy="{hy-26*s:.1f}" r="{16*s:.1f}" fill="{wool}"/><circle cx="{hx-2*s*d:.1f}" cy="{hy-30*s:.1f}" r="{12*s:.1f}" fill="{wool}"/>')
    if awake:
        o.append(f'<circle cx="{hx+4*s*d:.1f}" cy="{hy-5*s:.1f}" r="{6.5*s:.1f}" fill="#fffaf0"/><circle cx="{hx+5.5*s*d:.1f}" cy="{hy-4.5*s:.1f}" r="{4*s:.1f}" fill="#120c10"/><circle cx="{hx+4.2*s*d:.1f}" cy="{hy-6.5*s:.1f}" r="{1.5*s:.1f}" fill="#fff"/>')
    else:
        o.append(f'<path d="M{hx-3*s:.1f},{hy-4*s:.1f} q{6*s:.1f},{6*s:.1f} {12*s:.1f},0" stroke="#fffaf0" stroke-width="{3*s:.1f}" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M{hx+20*s*d:.1f},{hy+5*s:.1f} l{5*s*d:.1f},{4*s:.1f} l{-5*s*d:.1f},{4*s:.1f}" stroke="#e8a59a" stroke-width="{2.6*s:.1f}" fill="none" stroke-linecap="round"/>')
    if bell:
        o.append(f'<path d="M{X(44):.1f},{Y(16):.1f} q{12*s*d:.1f},{16*s:.1f} {26*s*d:.1f},{6*s:.1f}" stroke="#c8482e" stroke-width="{6*s:.1f}" fill="none" stroke-linecap="round"/><circle cx="{X(58):.1f}" cy="{Y(34):.1f}" r="{9*s:.1f}" fill="{GOLD}"/><circle cx="{X(58):.1f}" cy="{Y(37):.1f}" r="{2.6*s:.1f}" fill="#7a4e12"/>')
    sh = f'<ellipse cx="{cx:.1f}" cy="{Y(76 if not lying else 50):.1f}" rx="{74*s:.1f}" ry="{11*s:.1f}" fill="#16102a" opacity=".22"/>'
    return sh + f'<g filter="url(#cut)">{"".join(o)}</g>'


def stone(x, y, w, h, col, rot=0):
    return (f'<g transform="rotate({rot:.1f} {x:.1f} {y:.1f})"><rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h*0.38:.1f}" fill="{col}"/>'
            f'<rect x="{x-w*0.36:.1f}" y="{y-h*0.36:.1f}" width="{w*0.5:.1f}" height="{h*0.2:.1f}" rx="{h*0.1:.1f}" fill="#fff" opacity=".28"/></g>')


def fold(cx, cy, s=1.0):
    """The sheepfold: a ring of dry stone two courses high, a thatched shelter at the back,
    a wooden gate standing open, straw on the ground, sheep inside."""
    r = random.Random(5)
    cols = ["#d7c9a8", "#c2b392", "#e2d6b8", "#b3a383"]
    rx, ry = 380 * s, 120 * s
    def wall(a0, a1, gap=None):
        o = ""
        for course in (0, 1):
            n = 15 - course
            for k in range(n):
                a = math.radians(a0 + (a1 - a0) * (k + 0.5 * course) / (n - 1))
                if gap and gap[0] < math.degrees(a) < gap[1]:
                    continue
                x, y = cx + math.cos(a) * rx, cy + math.sin(a) * ry - course * 40 * s
                o += stone(x, y, r.uniform(66, 86) * s, r.uniform(42, 50) * s, r.choice(cols), r.uniform(-5, 5))
        return f'<g filter="url(#cut)">{o}</g>'
    out = [f'<ellipse cx="{cx}" cy="{cy+30*s}" rx="{rx*1.12}" ry="{ry*1.25}" fill="#1c1430" opacity=".16"/>',
           f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*0.96}" ry="{ry*0.94}" fill="#e0c88e"/>']
    for _ in range(26):   # straw
        a, q = r.uniform(0, math.tau), r.uniform(0, 0.85)
        x, y = cx + math.cos(a) * rx * q, cy + math.sin(a) * ry * q
        out.append(f'<path d="M{x:.0f},{y:.0f} l{r.uniform(-26,26)*s:.0f},{r.uniform(-8,8)*s:.0f}" stroke="#c9a85a" stroke-width="{4*s:.1f}" stroke-linecap="round"/>')
    out.append(wall(188, 352))
    # the shelter: posts, a lean-to roof of thatch
    sx, sy = cx - 150 * s, cy - 100 * s
    out.append(f'<g filter="url(#cut)"><rect x="{sx-150*s}" y="{sy-120*s}" width="{16*s}" height="{170*s}" rx="{5*s}" fill="#6b4a2e"/><rect x="{sx+134*s}" y="{sy-100*s}" width="{16*s}" height="{160*s}" rx="{5*s}" fill="#6b4a2e"/>'
               f'<rect x="{sx-140*s}" y="{sy-60*s}" width="{280*s}" height="{112*s}" fill="#4a3320" opacity=".55"/>'
               f'<path d="M{sx-190*s},{sy-112*s} L{sx-20*s},{sy-206*s} L{sx+190*s},{sy-128*s} L{sx+176*s},{sy-70*s} L{sx-176*s},{sy-58*s} Z" fill="#d9a441"/>'
               f'<path d="M{sx-190*s},{sy-112*s} L{sx-20*s},{sy-206*s} L{sx+190*s},{sy-128*s} L{sx+186*s},{sy-108*s} L{sx-20*s},{sy-180*s} L{sx-186*s},{sy-92*s} Z" fill="#eec26a"/></g>'
               + "".join(f'<path d="M{sx+k*s},{sy-(160-abs(k)*0.3)*s:.0f} l{-6*s},{(86-abs(k)*0.1)*s:.0f}" stroke="#b9832e" stroke-width="{4*s}" stroke-linecap="round" opacity=".8"/>' for k in range(-150, 170, 34)))
    out.append(sheep(cx - 150 * s, cy - 38 * s, 0.62 * s, True, "lie", awake=False) + sheep(cx + 130 * s, cy - 44 * s, 0.7 * s, False, "stand"))
    # trough
    out.append(f'<g filter="url(#cut)"><rect x="{cx-30*s}" y="{cy+6*s}" width="{130*s}" height="{34*s}" rx="{8*s}" fill="#7a5433"/><rect x="{cx-22*s}" y="{cy+10*s}" width="{114*s}" height="{14*s}" rx="{6*s}" fill="#7fc4e8"/></g>')
    out.append(wall(8, 172, gap=(62, 104)))
    # the gate, standing open, and its posts with a lamp
    gx, gy = cx + math.cos(math.radians(62)) * rx, cy + math.sin(math.radians(62)) * ry
    px, py = cx + math.cos(math.radians(104)) * rx, cy + math.sin(math.radians(104)) * ry
    out.append(f'<g filter="url(#cut)"><rect x="{gx-10*s:.0f}" y="{gy-120*s:.0f}" width="{20*s}" height="{140*s}" rx="{6*s}" fill="#5b3a22"/><rect x="{px-10*s:.0f}" y="{py-120*s:.0f}" width="{20*s}" height="{140*s}" rx="{6*s}" fill="#5b3a22"/>'
               f'<g transform="translate({gx:.0f} {gy-60*s:.0f}) skewY(-16)"><rect x="0" y="{-44*s}" width="{150*s}" height="{14*s}" rx="{5*s}" fill="#8a5a36"/><rect x="0" y="{-8*s}" width="{150*s}" height="{14*s}" rx="{5*s}" fill="#8a5a36"/>'
               f'<rect x="0" y="{28*s}" width="{150*s}" height="{14*s}" rx="{5*s}" fill="#8a5a36"/><path d="M{6*s},{38*s} L{144*s},{-40*s}" stroke="#6b4a2e" stroke-width="{12*s}" stroke-linecap="round"/><rect x="{138*s}" y="{-50*s}" width="{14*s}" height="{98*s}" rx="{5*s}" fill="#6b4a2e"/></g>'
               f'<rect x="{px-14*s:.0f}" y="{py-152*s:.0f}" width="{28*s}" height="{34*s}" rx="{7*s}" fill="{GOLD}"/><rect x="{px-7*s:.0f}" y="{py-146*s:.0f}" width="{14*s}" height="{22*s}" rx="{5*s}" fill="#fffbe9"/></g>')
    return "".join(out)


def den(x, y, s=1.0):
    """The den: a rock outcrop with a cave mouth, wolves' heads and eyes in the dark, old bones outside."""
    r = random.Random(9)
    rock = [(-520, 40), (-470, -170), (-360, -330), (-210, -470), (-40, -540), (150, -500), (300, -400), (420, -250), (500, -90), (540, 40)]
    P = lambda l: " ".join(f"{x+a*s:.0f},{y+b*s:.0f}" for a, b in l)
    out = [f'<g filter="url(#paper)"><polygon points="{P(rock)}" fill="#4f4680"/></g>']
    for facet, col in (([(-470, -170), (-360, -330), (-300, -120), (-420, 40), (-520, 40)], "#5c5392"), ([(-210, -470), (-40, -540), (-60, -360), (-250, -300), (-360, -330)], "#6a61a4"),
                       ([(150, -500), (300, -400), (240, -260), (60, -380), (-40, -540)], "#584f8e"), ([(420, -250), (500, -90), (540, 40), (400, 40), (330, -150)], "#3d3568")):
        out.append(f'<polygon points="{P(facet)}" fill="{col}"/>')
    for a, b, l in ((-330, -200, 90), (200, -330, 110), (380, -80, 70), (-120, -420, 60)):
        out.append(f'<path d="M{x+a*s:.0f},{y+b*s:.0f} l{l*0.4*s:.0f},{l*0.7*s:.0f} l{-l*0.2*s:.0f},{l*0.5*s:.0f}" stroke="#2c2552" stroke-width="{7*s}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    for a, b, w in ((-260, -318, 150), (60, -470, 190), (330, -330, 120)):   # moss
        out.append(f'<path d="M{x+(a-w/2)*s:.0f},{y+b*s:.0f} q{w*0.25*s:.0f},{-26*s:.0f} {w*0.5*s:.0f},{-6*s:.0f} q{w*0.25*s:.0f},{-22*s:.0f} {w*0.5*s:.0f},{4*s:.0f} q{-w*0.2*s:.0f},{30*s:.0f} {-w*0.5*s:.0f},{20*s:.0f} q{-w*0.3*s:.0f},{12*s:.0f} {-w*0.5*s:.0f},{-18*s:.0f}z" fill="#3f8a7a" opacity=".85"/>')
    # the mouth and what waits in it
    out.append(f'<path d="M{x-230*s},{y+40*s} L{x-230*s},{y-60*s} A{230*s},{225*s} 0 0 1 {x+230*s},{y-60*s} L{x+230*s},{y+40*s} Z" fill="#0b0716"/>'
               f'<ellipse cx="{x}" cy="{y+10*s}" rx="{190*s}" ry="{70*s}" fill="#5a2c1c" opacity=".35"/>')
    def head(hx, hy, k, col):
        return (f'<g transform="translate({hx:.0f} {hy:.0f}) scale({k*s:.2f})"><path d="M-70,60 L-78,-20 L-104,-120 L-44,-66 Q0,-84 44,-66 L104,-120 L78,-20 L70,60 Q36,110 0,118 Q-36,110 -70,60Z" fill="{col}"/>'
                f'<path d="M-26,60 Q0,74 26,60 L10,104 Q0,110 -10,104Z" fill="#0b0716" opacity=".6"/>'
                f'<path d="M-58,-6 q24,-22 46,2 q-24,14 -46,-2z" fill="#ffd75a"/><path d="M12,-4 q22,-24 46,-2 q-22,16 -46,2z" fill="#ffd75a"/><ellipse cx="-34" cy="-6" rx="4" ry="9" fill="#1a1020"/><ellipse cx="36" cy="-6" rx="4" ry="9" fill="#1a1020"/></g>')
    out.append(head(x - 96 * s, y - 70 * s, 0.86, "#1b1436") + head(x + 110 * s, y - 40 * s, 0.7, "#161030") + head(x + 10 * s, y - 150 * s, 0.5, "#120d28"))
    out.append(f'<g filter="url(#b6)" opacity=".7">' + "".join(f'<ellipse cx="{x+a*s:.0f}" cy="{y+b*s:.0f}" rx="{26*s}" ry="{12*s}" fill="#ffd75a"/>' for a, b in ((-126, -75), (-66, -75), (86, -44), (136, -44))) + '</g>')
    stones = ""
    n = 9
    for k in range(n):
        a = math.pi * (1.0 - k / (n - 1))
        cx_, cy_ = x + math.cos(a) * 262 * s, y - 20 * s - math.sin(a) * 240 * s
        stones += stone(cx_, cy_, 112 * s, 92 * s, "#756aa8" if k % 2 else "#8a80bc", 90 - math.degrees(a))
    out.append(f'<g filter="url(#cut)">{stones}{stone(x-262*s, y+16*s, 104*s, 92*s, "#756aa8")}{stone(x+262*s, y+16*s, 104*s, 92*s, "#8a80bc")}</g>')
    def bone(bx, by, rot, k=1.0):
        return (f'<g transform="translate({bx:.0f} {by:.0f}) rotate({rot}) scale({k*s:.2f})" filter="url(#cut)" fill="#e9e2d0"><rect x="-44" y="-7" width="88" height="14" rx="7"/>'
                f'<circle cx="-46" cy="-8" r="10"/><circle cx="-46" cy="8" r="10"/><circle cx="46" cy="-8" r="10"/><circle cx="46" cy="8" r="10"/></g>')
    out.append(bone(x - 360 * s, y + 60 * s, -18) + bone(x + 330 * s, y + 74 * s, 24, 0.8) + bone(x - 250 * s, y + 96 * s, 40, 0.6))
    return "".join(out)


def scene():
    rnd = random.Random(7)
    d = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs>'
         f'<filter id="paper" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="12" stdDeviation="7" flood-color="#150e1e" flood-opacity=".4"/></filter>'
         f'<filter id="cut" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="6" stdDeviation="4" flood-color="#150e1e" flood-opacity=".42"/></filter>'
         f'<filter id="b6"><feGaussianBlur stdDeviation="9"/></filter><filter id="b40"><feGaussianBlur stdDeviation="40"/></filter>'
         f'<linearGradient id="sky" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0"><stop offset="0" stop-color="#3fa9ea"/><stop offset=".3" stop-color="#8fd3f4"/><stop offset=".47" stop-color="#ffe9b8"/>'
         f'<stop offset=".57" stop-color="#b9a0e6"/><stop offset=".68" stop-color="#5a45b0"/><stop offset=".82" stop-color="#2c1f7a"/><stop offset="1" stop-color="#130c40"/></linearGradient>'
         f'<linearGradient id="skyv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c0a3a" stop-opacity=".34"/><stop offset=".45" stop-color="#0c0a3a" stop-opacity="0"/><stop offset=".62" stop-color="#fff6dc" stop-opacity=".0"/><stop offset=".72" stop-color="#fff6dc" stop-opacity=".22"/></linearGradient>'
         f'<radialGradient id="sunglow"><stop offset="0" stop-color="#fff6d0" stop-opacity=".95"/><stop offset="1" stop-color="#fff6d0" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="moonglow"><stop offset="0" stop-color="#cfd6ff" stop-opacity=".55"/><stop offset="1" stop-color="#cfd6ff" stop-opacity="0"/></radialGradient>'
         f'<radialGradient id="lampspill"><stop offset="0" stop-color="#ffd58a" stop-opacity=".6"/><stop offset="1" stop-color="#ffd58a" stop-opacity="0"/></radialGradient>'
         + dn("m1", "#a9d4ee", "#3b3090") + dn("m2", "#86bfe2", "#30267c") + dn("snow", "#ffffff", "#aab4ff")
         + dn("h1", "#a8e09a", "#4a3aa6") + dn("h2", "#7dd072", "#372a86") + dn("h3", "#52b955", "#281d68") + dn("h4", "#35a04a", "#1c144e") + dn("h5", "#cf7a3c", "#140e36", 0.54, 0.12)
         + dn("path", "#ecd9a4", "#5a4c9a") + '</defs>']
    d.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/><rect width="{W}" height="{H}" fill="url(#skyv)"/>')
    for _ in range(150):   # stars
        sx, sy = rnd.uniform(2250, W - 20), rnd.uniform(30, 1150)
        d.append(f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{rnd.choice([3, 4, 5, 7])}" fill="{PAPER}" opacity="{rnd.uniform(0.35, 0.95) * min(1.0, (sx - 2200) / 500):.2f}"/>')
    for sx, sy, r in [(2990, 300, 22), (3740, 260, 26), (3700, 900, 20), (3400, 520, 16), (2860, 620, 14), (3560, 110, 18)]:
        d.append(f'<path d="M{sx},{sy-r} L{sx+r*0.22},{sy-r*0.22} L{sx+r},{sy} L{sx+r*0.22},{sy+r*0.22} L{sx},{sy+r} L{sx-r*0.22},{sy+r*0.22} L{sx-r},{sy} L{sx-r*0.22},{sy-r*0.22}Z" fill="{PAPER}"/>')
    # the moon with its halo, low on the night ridge
    d.append(f'<circle cx="3075" cy="900" r="520" fill="url(#moonglow)"/><circle cx="3075" cy="900" r="250" fill="none" stroke="#cfd6ff" stroke-width="5" opacity=".3"/>'
             f'<g filter="url(#paper)"><circle cx="3075" cy="900" r="190" fill="#f6efd8"/></g><circle cx="3020" cy="850" r="34" fill="#e3dac0"/><circle cx="3140" cy="960" r="24" fill="#e3dac0"/><circle cx="3120" cy="820" r="14" fill="#e3dac0"/><circle cx="3030" cy="965" r="12" fill="#e3dac0"/>')
    # the sun: glow, long soft rays, the disc
    rays = "".join(f'<polygon points="800,940 {800+1500*math.cos(math.radians(a)):.0f},{940+1500*math.sin(math.radians(a)):.0f} {800+1500*math.cos(math.radians(a+7)):.0f},{940+1500*math.sin(math.radians(a+7)):.0f}" fill="#fff6d0" opacity=".13"/>' for a in range(170, 380, 20))
    d.append(f'{rays}<circle cx="800" cy="940" r="620" fill="url(#sunglow)"/><g filter="url(#paper)"><circle cx="800" cy="940" r="196" fill="{GOLD}"/></g><circle cx="800" cy="940" r="150" fill="#ffd978"/><circle cx="760" cy="900" r="70" fill="#ffe9a8" opacity=".6"/>')
    d.append(S.cloud(300, 620, 1.15) + S.cloud(1010, 250, 0.8, "#fffaf0") + S.cloud(230, 220, 0.9) + S.cloud(1330, 1010, 0.6, "#fffaf0") + S.cloud(2560, 1010, 0.7, "#8f7cc8") + S.cloud(3600, 1010, 0.6, "#5a49a8"))
    for bx, by, k in ((520, 420, 1.0), (590, 380, 0.8), (640, 440, 0.7), (1260, 620, 0.8), (1320, 580, 0.6)):   # birds
        d.append(f'<path d="M{bx-26*k},{by} q{13*k},{-18*k} {26*k},0 q{13*k},{-18*k} {26*k},0" stroke="#2a3a5a" stroke-width="{6*k}" fill="none" stroke-linecap="round"/>')
    # mountains behind everything
    d.append(peaks("m1", "snow", 1190, [(260, 330), (760, 230), (1380, 300), (2060, 380), (2620, 260), (3250, 340), (3720, 250)], 3))
    d.append(peaks("m2", "snow", 1230, [(520, 210), (1100, 170), (1740, 240), (2380, 190), (2960, 230), (3520, 200)], 4))
    # far hills, the ridge wolf against the moon, far olives
    d.append(ridge("url(#h1)", [(0, 1260), (520, 1150), (1100, 1240), (1700, 1120), (2300, 1210), (2900, 1070), (3400, 1170), (W, 1110)]))
    d.append(S.wolf(3010, 1078, 0.62))
    d.append(S.olive(1560, 1170, 0.6, "#8fc27e", "#b7dca0") + S.olive(300, 1180, 0.5, "#8fc27e", "#b7dca0") + S.olive(1900, 1150, 0.42, "#8fc27e", "#b7dca0"))
    d.append(sheep(1250, 1180, 0.36, True, "graze") + sheep(1740, 1150, 0.34, False))
    # middle hills: the fold and its olive; a bare tree and rocks on the night side
    d.append(ridge("url(#h2)", [(0, 1440), (600, 1340), (1300, 1450), (1900, 1360), (2600, 1460), (3200, 1340), (W, 1430)]))
    d.append(f'<path d="M1010,1480 C1200,1560 1460,1600 1620,1760 C1700,1840 1760,1900 1800,1990 L1960,1990 C1900,1860 1820,1760 1700,1680 C1500,1560 1300,1520 1130,1450 Z" fill="url(#path)" opacity=".8"/>')
    d.append(S.olive(1330, 1420, 0.95, "#5fae5a", "#93d27e") + S.olive(250, 1420, 0.8, "#5fae5a", "#93d27e"))
    d.append(fold(760, 1400, 1.0))
    d.append(S.bare_tree(2700, 1450, 0.9, "#161038") + S.bare_tree(3560, 1420, 0.6, "#161038"))
    d.append(sheep(1500, 1400, 0.56, False, "graze") + sheep(330, 1470, 0.5, True, lamb=True))
    # near hills: the flock, the den
    d.append(ridge("url(#h3)", [(0, 1650), (500, 1550), (1200, 1660), (1900, 1570), (2500, 1670), (3100, 1570), (W, 1650)]))
    d.append(den(3090, 1690, 0.95))
    d.append(sheep(250, 1580, 0.95, True, bell=True) + sheep(640, 1620, 0.8, False, "graze") + sheep(1010, 1640, 0.9, True, "lie", awake=False) + sheep(1420, 1600, 0.78, False) + sheep(820, 1700, 0.5, True, lamb=True))
    d.append(ridge("url(#h4)", [(0, 1840), (700, 1770), (1500, 1860), (2100, 1790), (2800, 1870), (3400, 1800), (W, 1860)]))
    d.append(sheep(430, 1830, 1.25, True) + sheep(1210, 1850, 1.05, False, "graze") + sheep(830, 1880, 0.62, True, lamb=True) + sheep(1560, 1890, 0.95, True, black=True))
    for ex, ey in ((2440, 1790), (3620, 1740), (2620, 1900)):   # eyes in the night grass
        d.append(f'<ellipse cx="{ex-16}" cy="{ey}" rx="11" ry="5" fill="#ffd75a"/><ellipse cx="{ex+16}" cy="{ey}" rx="11" ry="5" fill="#ffd75a"/>')
    d.append(f'<rect x="2200" y="1560" width="1640" height="130" fill="#8f86d8" opacity=".12" filter="url(#b40)"/>')
    # the last warm light of the day round him, then the shepherd, centred
    d.append(f'<ellipse cx="1920" cy="1500" rx="900" ry="640" fill="url(#lampspill)"/>')
    d.append(S.shepherd(1920, 1975, 0.8, "upright"))   # (the lamb upright on his shoulders, as on the capsules: slung across, its hanging head read as a beard)
    d.append(ridge("url(#h5)", [(0, 2020), (600, 1970), (1300, 2030), (2000, 1995), (2700, 2040), (3300, 1985), (W, 2030)]))
    for fx, fy, fs, col in [(160, 2110, 1.3, "#c9483c"), (420, 2050, 0.9, "#f5b53a"), (640, 2090, 1.0, "#c9483c"), (900, 2060, 0.8, "#ffffff"), (1180, 2120, 1.2, "#c9483c"), (1440, 2060, 0.8, "#f5b53a"), (1640, 2100, 0.9, "#c9483c")]:
        d.append(S.flower(fx, fy, fs, col))
    for tx, ty, ts, col in [(60, 2150, 1.3, "#2f8f45"), (300, 2140, 1.0, "#3fa04f"), (760, 2150, 1.4, "#2f8f45"), (1040, 2140, 1.0, "#3fa04f"), (1320, 2150, 1.1, "#2f8f45"), (1560, 2140, 1.1, "#3fa04f"), (1800, 2150, 1.0, "#3a7a55"),
                            (2180, 2150, 1.1, "#2c2570"), (2440, 2150, 1.2, "#2c2570"), (2760, 2140, 1.0, "#372e80"), (3000, 2150, 1.2, "#2c2570"), (3260, 2150, 1.4, "#2c2570"), (3600, 2140, 1.1, "#372e80")]:
        d.append(S.tuft(tx, ty, ts, col))
    d.append('</svg>')
    return "".join(d)


if __name__ == "__main__":
    import sys
    open(sys.argv[1] if len(sys.argv) > 1 else "keyscene.svg", "w").write(scene())
