# -*- coding: utf-8 -*-
"""BEYT & CO x LATE — boite a outils affiches (assets officiels BEYT)."""
import json, re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

# ---------- palette ----------
TOMATE = "#E82613"   # rouge officiel BEYT
CREME  = "#F7EFDC"   # papier
BLEU   = "#C3E9FB"   # bleu LATE
INK    = "#1A1410"

# ---------- polices ----------
_F = {}
def font(n):
    if n not in _F:
        f = TTFont(f"fonts/{n}.ttf")
        _F[n] = (f.getGlyphSet(), f["head"].unitsPerEm, f.getBestCmap(), f["hmtx"])
    return _F[n]

def tw(n, txt, size, tr=0.0):
    _, upm, cmap, hmtx = font(n)
    w = sum(hmtx[cmap[ord(c)]][0] if ord(c) in cmap else .32 * upm for c in txt)
    return w / upm * size + tr * size * max(0, len(txt) - 1)

def fit(n, txt, target, tr=0.0):
    return 100 * target / tw(n, txt, 100, tr)

def text(n, txt, size, x, y, fill, tr=0.0, anchor="start", opacity=None):
    gs, upm, cmap, hmtx = font(n)
    s = size / upm
    total = tw(n, txt, size, tr)
    x -= total / 2 if anchor == "middle" else (total if anchor == "end" else 0)
    out, cur = [], x
    for ch in txt:
        g = cmap.get(ord(ch))
        if g is not None:
            pen = SVGPathPen(gs); gs[g].draw(pen); d = pen.getCommands()
            if d:
                out.append(f'<path d="{d}" transform="translate({cur:.2f},{y:.2f}) '
                           f'scale({s:.5f},{-s:.5f})"/>')
            cur += hmtx[g][0] * s
        else:
            cur += .32 * size
        cur += tr * size
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<g fill="{fill}"{op}>' + "".join(out) + "</g>"

# ---------- assets vectoriels officiels ----------
ASSETS = {
    "beyt":   "assets-beyt/2026-08-26-BEYT-Logo-Officiel-Vectorise-Tomate-v01.svg",
    "andco":  "assets-beyt/2026-09-04-BEYT-Tampon-Ovale-Beyt-And-Co-Vectorise-v01.svg",
    "tasse":  "assets-beyt/2026-08-20-BEYT-Icone-Tasse-Vectorisee-Noir-v01.svg",
    "sfenj":  "assets-beyt/2026-08-25-BEYT-Icone-Tasse-The-Sfenj-Vectorisee-Noir-v01.svg",
    "coupole": "assets-beyt/2026-08-20-BEYT-Icone-Coupole-Vectorisee-Noir-v01.svg",
    "oeil":   "assets-beyt/2026-08-20-BEYT-Icone-Oeil-Plein-Vectorisee-Noir-v01.svg",
}
_SVG = {}
def asset(k):
    """Renvoie (contenu interne, largeur, hauteur) avec la couleur neutralisee."""
    if k not in _SVG:
        raw = open(ASSETS[k], encoding="utf8").read()
        vb = re.search(r'viewBox="([\d.\-\s]+)"', raw).group(1).split()
        w, h = float(vb[2]), float(vb[3])
        inner = re.sub(r"^.*?<svg[^>]*>", "", raw, flags=re.S)
        inner = re.sub(r"</svg>\s*$", "", inner, flags=re.S)
        inner = re.sub(r"<title>.*?</title>", "", inner, flags=re.S)
        inner = inner.replace('fill="#000000"', 'fill="@C@"') \
                     .replace('fill="#E82613"', 'fill="@C@"') \
                     .replace('fill="currentColor"', 'fill="@C@"')
        _SVG[k] = (inner, w, h)
    return _SVG[k]

# le logo LATE reste celui des affiches d'origine, revectorise
_LATE = json.load(open("late/late-mark.json"))

def late(x, y, w=None, h=None, fill=CREME, anchor="tl"):
    s = _LATE
    sc = (w / s["w"]) if w else (h / s["h"])
    W, H = s["w"] * sc, s["h"] * sc
    ax = {"tl":0,"t":.5,"tr":1,"l":0,"c":.5,"r":1,"bl":0,"b":.5,"br":1}[anchor]
    ay = {"tl":0,"t":0,"tr":0,"l":.5,"c":.5,"r":.5,"bl":1,"b":1,"br":1}[anchor]
    return (f'<g transform="translate({x-W*ax:.2f},{y-H*ay:.2f}) scale({sc:.6f})">'
            f'<path d="{s["d"]}" fill="{fill}"/></g>')

def late_box(w=None, h=None):
    s = _LATE; sc = (w / s["w"]) if w else (h / s["h"])
    return s["w"] * sc, s["h"] * sc

def box(k, w=None, h=None):
    _, W, H = asset(k); sc = (w / W) if w else (h / H)
    return W * sc, H * sc

def put(k, x, y, w=None, h=None, fill=CREME, anchor="tl", opacity=None, rot=0):
    inner, W, H = asset(k)
    sc = (w / W) if w else (h / H)
    bw, bh = W * sc, H * sc
    ax = {"tl":0,"t":.5,"tr":1,"l":0,"c":.5,"r":1,"bl":0,"b":.5,"br":1}[anchor]
    ay = {"tl":0,"t":0,"tr":0,"l":.5,"c":.5,"r":.5,"bl":1,"b":1,"br":1}[anchor]
    ox, oy = x - bw * ax, y - bh * ay
    t = f"translate({ox:.2f},{oy:.2f}) "
    if rot:
        t += f"rotate({rot},{bw/2:.2f},{bh/2:.2f}) "
    t += f"scale({sc:.6f})"
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<g transform="{t}"{op}>' + inner.replace("@C@", fill) + "</g>"

# ---------- primitives ----------
def cross(cx, cy, size, fill=CREME, weight=.075, rot=45):
    t, a = size * weight, size / 2
    d = (f"M{-t/2:.2f},{-a:.2f} L{t/2:.2f},{-a:.2f} L{t/2:.2f},{-t/2:.2f} "
         f"L{a:.2f},{-t/2:.2f} L{a:.2f},{t/2:.2f} L{t/2:.2f},{t/2:.2f} "
         f"L{t/2:.2f},{a:.2f} L{-t/2:.2f},{a:.2f} L{-t/2:.2f},{t/2:.2f} "
         f"L{-a:.2f},{t/2:.2f} L{-a:.2f},{-t/2:.2f} L{-t/2:.2f},{-t/2:.2f} Z")
    return (f'<g transform="translate({cx:.2f},{cy:.2f}) rotate({rot})">'
            f'<path d="{d}" fill="{fill}"/></g>')

def rule(x1, y1, x2, y2, w, fill=CREME, opacity=None):
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{fill}" stroke-width="{w:.2f}"{op}/>')

BLEED = 0.0
def ground(w, h, fill):
    b = BLEED
    return (f'<rect x="{-b}" y="{-b}" width="{w+2*b}" height="{h+2*b}" fill="{fill}"/>')

def svg(w, h, body):
    b = BLEED; W, H = w + 2*b, h + 2*b
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" '
            f'viewBox="{-b} {-b} {W} {H}">{body}</svg>')
