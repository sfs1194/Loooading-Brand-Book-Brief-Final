# -*- coding: utf-8 -*-
"""Boite a outils BEYT x LATE : texte vectorise, rayures peintes, placement d'icones."""
import json, math, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen

SHAPES = json.load(open("shapes.json"))

# ---------- palette ----------
ORANGE       = "#F55000"
ORANGE_LIGHT = "#F97A37"
BLUE         = "#C3E9FB"
BLUE_LIGHT   = "#E2F2F9"
CREAM        = "#F7EFDC"
CREAM_DEEP   = "#EDE2C7"

_FONTS = {}
def font(name):
    if name not in _FONTS:
        f = TTFont(f"fonts/{name}.ttf")
        _FONTS[name] = (f, f.getGlyphSet(), f["head"].unitsPerEm,
                        f.getBestCmap(), f["hmtx"])
    return _FONTS[name]

def text_width(name, txt, size, tracking=0.0):
    _, _, upm, cmap, hmtx = font(name)
    w = 0
    for ch in txt:
        g = cmap.get(ord(ch))
        if g is None:
            w += 0.32 * upm
        else:
            w += hmtx[g][0]
    return w / upm * size + tracking * size * max(0, len(txt) - 1)

def text_path(name, txt, size, x=0, y=0, tracking=0.0, anchor="start"):
    """Renvoie un <path> SVG : le texte converti en courbes (aucune police requise)."""
    _, gs, upm, cmap, hmtx = font(name)
    s = size / upm
    total = text_width(name, txt, size, tracking)
    if anchor == "middle":
        x -= total / 2
    elif anchor == "end":
        x -= total
    out, cur = [], x
    for ch in txt:
        g = cmap.get(ord(ch))
        if g is not None:
            pen = SVGPathPen(gs)
            gs[g].draw(pen)
            d = pen.getCommands()
            if d:
                out.append(f'<path d="{d}" transform="translate({cur:.2f},{y:.2f}) '
                           f'scale({s:.5f},{-s:.5f})"/>')
            cur += hmtx[g][0] * s
        else:
            cur += 0.32 * size
        cur += tracking * size
    return "".join(out)

def fit_size(name, txt, target_w, tracking=0.0):
    """La taille de corps qui fait tomber la ligne pile sur target_w."""
    unit = text_width(name, txt, 100, tracking)
    return 100 * target_w / unit


def text(name, txt, size, x, y, fill, tracking=0.0, anchor="start", opacity=None):
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<g fill="{fill}"{op}>'
            + text_path(name, txt, size, x, y, tracking, anchor) + "</g>")

# ---------- rayures peintes a la main ----------
def stripes(w, h, base, stripe, seed=7, period=34, width_ratio=0.42, wobble=5.0, segs=5):
    """Rayures verticales legerement tremblees, comme peintes au pinceau."""
    rnd = random.Random(seed)
    out = [f'<rect x="0" y="0" width="{w}" height="{h}" fill="{base}"/>']
    x = -period * 0.5
    while x < w + period:
        sw = period * width_ratio * rnd.uniform(0.62, 1.38)
        left, right = [], []
        for i in range(segs + 1):
            yy = h * i / segs
            dx = rnd.uniform(-wobble, wobble)
            taper = 1.0 + 0.16 * math.sin(i / segs * math.pi * rnd.uniform(0.7, 1.9))
            left.append((x + dx, yy))
            right.append((x + dx + sw * taper, yy))
        d = f'M{left[0][0]:.1f},{left[0][1]:.1f}'
        for i in range(1, len(left)):
            px, py = left[i - 1]; cx, cy = left[i]
            d += f' C{px:.1f},{(py+cy)/2:.1f} {cx:.1f},{(py+cy)/2:.1f} {cx:.1f},{cy:.1f}'
        d += f' L{right[-1][0]:.1f},{right[-1][1]:.1f}'
        for i in range(len(right) - 1, 0, -1):
            px, py = right[i]; cx, cy = right[i - 1]
            d += f' C{px:.1f},{(py+cy)/2:.1f} {cx:.1f},{(py+cy)/2:.1f} {cx:.1f},{cy:.1f}'
        d += " Z"
        out.append(f'<path d="{d}" fill="{stripe}"/>')
        x += period * rnd.uniform(0.82, 1.2)
    return "".join(out)

# ---------- icones ----------
def shape(key, x, y, w=None, h=None, fill=CREAM, anchor="tl",
          rotate=0.0, opacity=None, clip=None, flip=False):
    s = SHAPES[key]
    sw, sh = s["w"], s["h"]
    sc = (w / sw) if w else (h / sh)
    W, H = sw * sc, sh * sc
    ax = {"tl": 0, "t": .5, "tr": 1, "l": 0, "c": .5, "r": 1,
          "bl": 0, "b": .5, "br": 1}[anchor]
    ay = {"tl": 0, "t": 0, "tr": 0, "l": .5, "c": .5, "r": .5,
          "bl": 1, "b": 1, "br": 1}[anchor]
    ox, oy = x - W * ax, y - H * ay
    t = f"translate({ox:.2f},{oy:.2f}) "
    if rotate:
        t += f"rotate({rotate},{W/2:.2f},{H/2:.2f}) "
    if flip:
        t += f"translate({W:.2f},0) scale(-1,1) "
    t += f"scale({sc:.5f})"
    op = f' opacity="{opacity}"' if opacity is not None else ""
    cl = f' clip-path="url(#{clip})"' if clip else ""
    return f'<g transform="{t}"{op}{cl}><path d="{s["d"]}" fill="{fill}"/></g>'

def shape_box(key, w=None, h=None):
    s = SHAPES[key]
    sc = (w / s["w"]) if w else (h / s["h"])
    return s["w"] * sc, s["h"] * sc

# ---------- la croix de collaboration ----------
def cross(cx, cy, size, fill=CREAM, weight=0.085, rotate=45):
    """Croix ✕ dessinee : deux barres a bouts droits, tracee net."""
    t = size * weight
    a = size / 2
    d = (f"M{-t/2:.2f},{-a:.2f} L{t/2:.2f},{-a:.2f} L{t/2:.2f},{-t/2:.2f} "
         f"L{a:.2f},{-t/2:.2f} L{a:.2f},{t/2:.2f} L{t/2:.2f},{t/2:.2f} "
         f"L{t/2:.2f},{a:.2f} L{-t/2:.2f},{a:.2f} L{-t/2:.2f},{t/2:.2f} "
         f"L{-a:.2f},{t/2:.2f} L{-a:.2f},{-t/2:.2f} L{-t/2:.2f},{-t/2:.2f} Z")
    return (f'<g transform="translate({cx:.2f},{cy:.2f}) rotate({rotate})">'
            f'<path d="{d}" fill="{fill}"/></g>')

def dot(cx, cy, r, fill=CREAM):
    return f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}"/>'

def rule(x1, y1, x2, y2, w, fill=CREAM, opacity=None):
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{fill}" stroke-width="{w:.2f}"{op}/>')

def arch(x, y, w, h, fill=CREAM, extra=""):
    """Une arche : plein cintre en haut, pieds droits — la porte de la maison."""
    r = w / 2
    d = (f"M{x:.1f},{y+h:.1f} L{x:.1f},{y+r:.1f} "
         f"A{r:.1f},{r:.1f} 0 0 1 {x+w:.1f},{y+r:.1f} "
         f"L{x+w:.1f},{y+h:.1f} Z")
    return f'<path d="{d}" fill="{fill}"{extra}/>'


def arch_clip(cid, x, y, w, h):
    r = w / 2
    d = (f"M{x:.1f},{y+h:.1f} L{x:.1f},{y+r:.1f} "
         f"A{r:.1f},{r:.1f} 0 0 1 {x+w:.1f},{y+r:.1f} "
         f"L{x+w:.1f},{y+h:.1f} Z")
    return f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'


BLEED = 0.0          # fonds perdus, en mm ; pilote par build.py


def ground(w, h, fill=None, **stripe_kw):
    """Le fond, etendu jusqu'aux fonds perdus."""
    b = BLEED
    if fill is not None and not stripe_kw:
        return (f'<rect x="{-b}" y="{-b}" width="{w+2*b}" height="{h+2*b}" '
                f'fill="{fill}"/>')
    return (f'<g transform="translate({-b},{-b})">'
            + stripes(w + 2 * b, h + 2 * b, **stripe_kw) + '</g>')


def svg(w, h, body, defs=""):
    b = BLEED
    W, H = w + 2 * b, h + 2 * b
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}mm" height="{H}mm" viewBox="{-b} {-b} {W} {H}">'
            f'<defs>{defs}</defs>{body}</svg>')
