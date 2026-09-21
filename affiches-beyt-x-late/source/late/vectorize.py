import json
import numpy as np
import potrace
from PIL import Image

SRC = {
    "beyt":    ("assets/img_53.png", 2),   # wordmark BEYT
    "late":    ("assets/img_57.png", 3),   # logo LATE + MATCHA+COFFEE
    "sip":     ("assets/img_90.png", 3),   # fille qui boit
    "cookie":  ("assets/img_56.png", 3),   # fille aux cookies
    "jug":     ("assets/img_46.png", 3),   # pichet
    "vase":    ("assets/img_58.png", 3),   # vase a anse
    "sun":     ("assets/img_54.png", 3),   # soleil
    "hand":    ("assets/img_81.png", 3),   # main
}

def trace(path, scale):
    im = Image.open(path).convert("RGB")
    a = np.array(im).max(axis=2)          # noir = fond, encre = clair
    # crop to ink
    ys, xs = np.where(a > 40)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    im = im.crop((x0, y0, x1, y1))
    if scale != 1:
        im = im.resize((im.width * scale, im.height * scale), Image.LANCZOS)
    a = np.array(im).max(axis=2) > 100
    bmp = potrace.Bitmap(a)
    bmp.invert()   # Bitmap.__init__ inverse deja une fois
    plist = bmp.trace(turdsize=max(2, (scale * scale)), alphamax=1.0,
                      opttolerance=0.2)
    d = []
    for curve in plist:
        sx, sy = curve.start_point.x, curve.start_point.y
        d.append(f"M{sx:.2f},{sy:.2f}")
        for seg in curve:
            if seg.is_corner:
                cx, cy = seg.c.x, seg.c.y; ex, ey = seg.end_point.x, seg.end_point.y
                d.append(f"L{cx:.2f},{cy:.2f}L{ex:.2f},{ey:.2f}")
            else:
                c1, c2 = seg.c1, seg.c2; ex, ey = seg.end_point.x, seg.end_point.y
                d.append(f"C{c1.x:.2f},{c1.y:.2f} {c2.x:.2f},{c2.y:.2f} {ex:.2f},{ey:.2f}")
        d.append("Z")
    return {"d": "".join(d), "w": im.width, "h": im.height}





# --- le logo LATE sans le sous-titre : on ne garde que le lettrage
def trace_crop(path, scale, frac0, frac1):
    im = Image.open(path).convert("RGB")
    a = np.array(im).max(axis=2)
    ys, xs = np.where(a > 100)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    H = im.height
    im = im.crop((0, int(H * frac0), im.width, int(H * frac1)))
    a = np.array(im).max(axis=2) > 100
    ys, xs = np.where(a)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    tmp = "late/_part.png"; im.save(tmp)
    return trace(tmp, scale)


if __name__ == "__main__":
    out = trace_crop("late/late-logo-source.png", 3, 0.00, 0.80)
    json.dump(out, open("late/late-mark.json", "w"))
    print("late-mark", out["w"], "x", out["h"])
