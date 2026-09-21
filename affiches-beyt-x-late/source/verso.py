# -*- coding: utf-8 -*-
"""VERSO — cote LATE (fond bleu), hierarchie inversee : LATE chez BEYT & CO."""
from kit2 import *
import kit2

W, H = 594, 841
M = 56

def build():
    b = [ground(W, H, BLEU)]

    b.append(text("Archivo-Bold", "COLLABORATION", 9, W/2, 88, TOMATE,
                  tr=.46, anchor="middle"))
    b.append(rule(M, 106, W-M, 106, .9, TOMATE, opacity=.5))

    # --- LATE, heros de ce cote
    lw = 258
    _, lh = late_box(w=lw)
    b.append(late(W/2, 160, w=lw, anchor="t", fill=TOMATE))

    # --- deux tasses, meme ligne de sol : deux maisons, une seule table
    base = 524
    tw_, _ = box("tasse", h=132)
    sw_, _ = box("sfenj", h=68)
    gap = 50
    x0 = (W - (tw_ + gap + sw_)) / 2
    b.append(put("tasse", x0, base, h=132, anchor="bl", fill=TOMATE))
    b.append(put("sfenj", x0 + tw_ + gap, base, h=68, anchor="bl", fill=TOMATE))

    # --- la signature : chez BEYT & CO
    cy_ = 588
    b.append(rule(W/2 - 78, cy_ - 3.2, W/2 - 30, cy_ - 3.2, .9, TOMATE, opacity=.5))
    b.append(text("Archivo-Bold", "CHEZ", 9, W/2, cy_, TOMATE,
                  tr=.5, anchor="middle"))
    b.append(rule(W/2 + 30, cy_ - 3.2, W/2 + 78, cy_ - 3.2, .9, TOMATE, opacity=.5))

    bw = 236
    _, bh = box("beyt", w=bw)
    sh2 = 96
    sw2, _ = box("andco", h=sh2)
    g2 = 24
    tot2 = bw + g2 + sw2
    x1 = (W - tot2) / 2
    axis = 660
    b.append(put("beyt", x1, axis, w=bw, anchor="l", fill=TOMATE))
    b.append(put("andco", x1 + bw + g2, axis, h=sh2, anchor="l", fill=TOMATE))

    b.append(rule(M, 752, W-M, 752, .9, TOMATE, opacity=.5))
    b.append(text("Archivo-Medium", "DEUX MAISONS, UNE SEULE ADRESSE", 9.5,
                  W/2, 780, TOMATE, tr=.3, anchor="middle"))
    return svg(W, H, "".join(b))

if __name__ == "__main__":
    import cairosvg
    open("verso.svg", "w").write(build())
    cairosvg.svg2png(url="verso.svg", write_to="verso.png", output_width=740)
    print("ok")
