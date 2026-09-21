# -*- coding: utf-8 -*-
"""Affiche 1 — BEYT x LATE, le lockup sous l'arche (fond orange)."""
from kit import *

W, H = 594, 841
M = 46

AW = 398                      # l'arche
AX = (W - AW) / 2
AY = 124
AH = 580

def build():
    b = [ground(W, H, base=ORANGE, stripe=ORANGE_LIGHT, seed=11, period=27,
                width_ratio=0.52, wobble=2.0, segs=4)]

    # --- bandeau haut
    y = 74
    b.append(rule(M, y - 3.4, M + 74, y - 3.4, 1.5, CREAM))
    b.append(text("Archivo-Bold", "COLLABORATION", 10, W / 2, y,
                  CREAM, tracking=0.4, anchor="middle"))
    b.append(rule(W - M - 74, y - 3.4, W - M, y - 3.4, 1.5, CREAM))

    # --- l'arche : le champ clair ou respire le lockup
    b.append(arch(AX, AY, AW, AH, CREAM))

    # --- dans l'arche : soleil, BEYT, croix, LATE
    b.append(shape("sun", W / 2, AY + 70, w=64, fill=ORANGE, anchor="c"))

    bw = 318
    _, bh = shape_box("beyt", w=bw)
    by = AY + 120
    b.append(shape("beyt", W / 2, by, w=bw, anchor="t", fill=ORANGE))

    cy = by + bh + 46
    b.append(cross(W / 2, cy, 44, ORANGE, weight=0.115))

    lw = 172
    _, lh = shape_box("late_mark", w=lw)
    ly = cy + 46
    b.append(shape("late_mark", W / 2, ly, w=lw, anchor="t", fill=ORANGE))
    b.append(shape("late_sub", W / 2, ly + lh + 14, w=132, anchor="t", fill=ORANGE))

    # --- deux poteries posees de part et d'autre du seuil
    b.append(shape("jug", AX - 30, AY + AH, h=116, fill=CREAM, anchor="b"))
    b.append(shape("vase", AX + AW + 34, AY + AH, h=106, fill=CREAM, anchor="b"))

    # --- le message, sous l'arche
    b.append(text("Italiana-Regular", "LE CAFÉ, À LA MAISON", 31, W / 2,
                  758, CREAM, tracking=0.14, anchor="middle"))
    b.append(rule(W / 2 - 54, 777, W / 2 + 54, 777, 1.2, CREAM, opacity=0.55))
    b.append(text("Archivo-Medium",
                  "LE COFFEE SHOP LATE EST MAINTENANT CHEZ BEŶT", 9,
                  W / 2, 797, CREAM, tracking=0.3, anchor="middle"))
    return svg(W, H, "".join(b))

if __name__ == "__main__":
    import cairosvg
    open("p1.svg", "w").write(build())
    cairosvg.svg2png(url="p1.svg", write_to="p1.png", output_width=760)
    print("ok")
