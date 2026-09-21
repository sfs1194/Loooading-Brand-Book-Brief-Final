# -*- coding: utf-8 -*-
"""Genere les trois affiches BEYT x LATE : PDF prets a imprimer + apercus PNG."""
import os, cairosvg, kit
import p1, p2, p3

OUT = "../affiches"
POSTERS = [("01-collaboration", p1), ("02-invitation", p2), ("03-deux-maisons", p3)]
PREVIEW_W = 1600

os.makedirs(f"{OUT}/pdf", exist_ok=True)
os.makedirs(f"{OUT}/png", exist_ok=True)
os.makedirs(f"{OUT}/svg", exist_ok=True)

for name, mod in POSTERS:
    # --- PDF avec 5 mm de fonds perdus, pour l'imprimeur
    kit.BLEED = 5.0
    svg_bleed = mod.build()
    cairosvg.svg2pdf(bytestring=svg_bleed.encode(),
                     write_to=f"{OUT}/pdf/BEYT-x-LATE-{name}-A1-fonds-perdus.pdf")

    # --- format final, sans debord : SVG source + PDF + apercu PNG
    kit.BLEED = 0.0
    s = mod.build()
    open(f"{OUT}/svg/BEYT-x-LATE-{name}-A1.svg", "w").write(s)
    cairosvg.svg2pdf(bytestring=s.encode(),
                     write_to=f"{OUT}/pdf/BEYT-x-LATE-{name}-A1.pdf")
    cairosvg.svg2png(bytestring=s.encode(),
                     write_to=f"{OUT}/png/BEYT-x-LATE-{name}.png",
                     output_width=PREVIEW_W)
    print("ok", name)
