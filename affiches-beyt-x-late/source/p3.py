# -*- coding: utf-8 -*-
"""Affiche 3 — l'arche inversee (fond creme)."""
from kit import *

W, H = 594, 841
M = 46

AW = 400
AX = (W - AW) / 2
AY = 92
AH = 452

def build():
    b = [ground(W, H, fill=CREAM)]

    # --- l'arche, remplie de rayures orange
    defs = arch_clip("a3", AX, AY, AW, AH)
    b.append(f'<g clip-path="url(#a3)">'
             + stripes(W, H, ORANGE, ORANGE_LIGHT, seed=5, period=25,
                       width_ratio=0.52, wobble=1.8, segs=4)
             + '</g>')

    # --- dans l'arche : la figure, en creme
    b.append(shape("sip", W / 2 - 8, AY + AH - 40, h=198, fill=CREAM, anchor="b"))
    b.append(shape("sun", AX + 74, AY + 116, w=54, fill=CREAM, anchor="c"))
    b.append(shape("jug", AX + AW - 66, AY + AH - 40, h=108, fill=CREAM, anchor="b"))

    # --- le lockup horizontal : BEYT  x  LATE
    gap = 30
    bw = 196
    _, bh = shape_box("beyt", w=bw)
    lh = 92
    lw, _ = shape_box("late_mark", h=lh)
    cs = 30
    total = bw + gap + cs + gap + lw
    x0 = (W - total) / 2
    axis = 636
    b.append(shape("beyt", x0, axis, w=bw, anchor="l", fill=ORANGE))
    b.append(cross(x0 + bw + gap + cs / 2, axis, cs, ORANGE, weight=0.135))
    b.append(shape("late_mark", x0 + bw + gap + cs + gap, axis, h=lh,
                   anchor="l", fill=ORANGE))

    # --- la ligne
    b.append(rule(W / 2 - 150, 712, W / 2 + 150, 712, 1.2, ORANGE, opacity=0.45))
    b.append(text("Italiana-Regular", "DEUX MAISONS, UNE SEULE ADRESSE", 25.5,
                  W / 2, 752, ORANGE, tracking=0.1, anchor="middle"))
    b.append(text("Archivo-Medium", "MATCHA  ·  CAFÉ  ·  FILTRE", 9.5,
                  W / 2, 786, ORANGE, tracking=0.34, anchor="middle",
                  opacity=0.75))
    return svg(W, H, "".join(b), defs)

if __name__ == "__main__":
    import cairosvg
    open("p3.svg", "w").write(build())
    cairosvg.svg2png(url="p3.svg", write_to="p3.png", output_width=760)
    print("ok")
