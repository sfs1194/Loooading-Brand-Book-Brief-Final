"""Story Instagram 1080x1920 : photo plein cadre + logo officiel The Zellijist (icône + texte).
Usage : python3 make_story.py photo.jpg sortie.jpg [focus_x 0..1] [top|bottom] [blanc|noir|auto]"""
import sys
from PIL import Image, ImageOps, ImageStat

W, H = 1080, 1920
LOGOS = __file__.rsplit('/', 2)[0] + '/assets/logos/the-zellijist-icone-{}.png'
LOGO_W = 250
# zones de sécurité Instagram : ~200 px en haut (profil), ~280 px en bas (réponse)
TOP_Y, BOTTOM_MARGIN = 210, 170

def cover(im):
    s = max(W / im.width, H / im.height)
    return im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)

def story(src, out, focus_x=0.5, where='top', color='auto'):
    im = cover(ImageOps.exif_transpose(Image.open(src)).convert('RGB'))
    x = min(max(0, round(im.width * focus_x - W / 2)), im.width - W)
    y = (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H))

    w = LOGO_W
    h = round(w * 929 / 1260)
    ly = TOP_Y if where == 'top' else H - BOTTOM_MARGIN - h
    lx = (W - w) // 2
    if color == 'auto':
        lum = ImageStat.Stat(im.crop((lx, ly, lx + w, ly + h)).convert('L')).mean[0]
        color = 'noir' if lum > 140 else 'blanc'
    logo = Image.open(LOGOS.format(color)).resize((w, h), Image.LANCZOS)
    im.paste(logo, (lx, ly), logo)
    im.save(out, quality=94)
    return color

if __name__ == '__main__':
    a = sys.argv
    print(story(a[1], a[2], float(a[3]) if len(a) > 3 else 0.5,
                a[4] if len(a) > 4 else 'top', a[5] if len(a) > 5 else 'auto'))
