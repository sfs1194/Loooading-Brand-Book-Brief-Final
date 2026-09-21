# -*- coding: utf-8 -*-
"""Genere le recto et le verso : PDF prets a imprimer + apercus."""
import os, cairosvg, kit2
import recto, verso

OUT = "../affiches"
PAGES = [("recto", recto), ("verso", verso)]
for d in ("pdf", "png", "svg"):
    os.makedirs(f"{OUT}/{d}", exist_ok=True)

for name, mod in PAGES:
    kit2.BLEED = 5.0
    cairosvg.svg2pdf(bytestring=mod.build().encode(),
                     write_to=f"{OUT}/pdf/BEYT-ET-CO-x-LATE-{name}-A1-fonds-perdus.pdf")
    kit2.BLEED = 0.0
    s = mod.build()
    open(f"{OUT}/svg/BEYT-ET-CO-x-LATE-{name}-A1.svg", "w").write(s)
    cairosvg.svg2pdf(bytestring=s.encode(),
                     write_to=f"{OUT}/pdf/BEYT-ET-CO-x-LATE-{name}-A1.pdf")
    cairosvg.svg2png(bytestring=s.encode(),
                     write_to=f"{OUT}/png/BEYT-ET-CO-x-LATE-{name}.png",
                     output_width=1600)
    print("ok", name)
