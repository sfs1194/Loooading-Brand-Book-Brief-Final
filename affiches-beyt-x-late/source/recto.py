# -*- coding: utf-8 -*-
"""RECTO — le lockup BEYT & CO x LATE (fond tomate)."""
from kit2 import *
import kit2

W, H = 594, 841
M = 56

def build():
    b = [ground(W, H, TOMATE)]

    # deux tasses encadrent le surtitre : l'objet dit ce que le texte ne dit pas
    b.append(put("tasse", M + 4, 92, h=30, anchor="bl", fill=CREME))
    b.append(put("sfenj", W - M - 4, 91, h=20, anchor="br", fill=CREME))
    b.append(text("Archivo-Bold", "COLLABORATION", 9, W/2, 88, CREME,
                  tr=.46, anchor="middle"))
    b.append(rule(M, 106, W-M, 106, .9, CREME, opacity=.55))

    # --- identite BEYT & CO
    bw = 406
    _, bh = box("beyt", w=bw)
    by = 160
    b.append(put("beyt", W/2, by, w=bw, anchor="t", fill=CREME))

    sy = by + bh + 16
    sh = 124
    b.append(put("andco", W/2, sy, h=sh, anchor="t", fill=CREME))

    # --- la croix, puis LATE
    cy = sy + sh + 48
    b.append(cross(W/2, cy, 34, CREME, weight=.10))

    ly = cy + 46
    lw = 156
    _, lh = late_box(w=lw)
    b.append(late(W/2, ly, w=lw, anchor="t", fill=CREME))

    # --- pied
    b.append(rule(M, 752, W-M, 752, .9, CREME, opacity=.55))
    b.append(text("Archivo-Medium", "LATE EST MAINTENANT CHEZ BEŶT & CO", 9.5,
                  W/2, 780, CREME, tr=.3, anchor="middle"))
    return svg(W, H, "".join(b))

if __name__ == "__main__":
    import cairosvg
    open("recto.svg", "w").write(build())
    cairosvg.svg2png(url="recto.svg", write_to="recto.png", output_width=740)
    print("ok")
