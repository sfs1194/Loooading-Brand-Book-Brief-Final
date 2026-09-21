# -*- coding: utf-8 -*-
"""Affiche 2 — l'invitation (fond bleu)."""
from kit import *
import kit

W, H = 594, 841
M = 46
BAND_Y = 660           # le bandeau creme du bas

def build():
    b = [ground(W, H, base=BLUE, stripe=BLUE_LIGHT, seed=23, period=26,
                width_ratio=0.5, wobble=1.8, segs=4)]

    # --- le soleil deborde du coin
    b.append(shape("sun", -66, -74, w=236, fill=ORANGE))

    # --- le titre : deux lignes calees sur la meme largeur optique
    tw = 340
    for i, line in enumerate(("ON PREND", "UN CAFÉ ?")):
        sz = fit_size("Anton-Regular", line, tw, 0.01)
        b.append(text("Anton-Regular", line, sz, W / 2, 240 + i * 102,
                      ORANGE, tracking=0.01, anchor="middle"))

    # --- le logo LATE, heros de l'affiche
    b.append(shape("late_mark", W / 2, 395, w=244, anchor="t", fill=ORANGE))

    # --- deux figures posees au bord du bandeau
    b.append(shape("cookie", 66, BAND_Y - 14, h=74, fill=ORANGE, anchor="b"))
    b.append(shape("sip", W - 66, BAND_Y - 14, h=74, fill=ORANGE, anchor="b",
                   flip=True))

    # --- le bandeau creme : la signature
    b.append(f'<rect x="{-kit.BLEED}" y="{BAND_Y}" width="{W+2*kit.BLEED}" '
             f'height="{H-BAND_Y+kit.BLEED}" fill="{CREAM}"/>')
    b.append(text("Archivo-Bold", "MAINTENANT CHEZ", 10, W / 2, BAND_Y + 40,
                  ORANGE, tracking=0.4, anchor="middle"))
    b.append(shape("beyt", W / 2, BAND_Y + 56, w=196, anchor="t", fill=ORANGE))
    return svg(W, H, "".join(b))

if __name__ == "__main__":
    import cairosvg
    open("p2.svg", "w").write(build())
    cairosvg.svg2png(url="p2.svg", write_to="p2.png", output_width=760)
    print("ok")
