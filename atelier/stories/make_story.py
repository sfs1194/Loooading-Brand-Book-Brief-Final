"""Story Instagram 1080x1920 : photo plein cadre + logo The Zellijist blanc.
Usage : python3 make_story.py photo.jpg sortie.jpg [focus_x 0..1] [top|bottom]"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFilter

W, H = 1080, 1920
LOGO = __file__.rsplit('/', 2)[0] + '/assets/logos/the-zellijist-blanc.png'

def story(src, out, focus_x=0.5, where='top'):
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = min(max(0, round(im.width * focus_x - W / 2)), im.width - W)
    y = (im.height - H) // 2
    im = im.crop((x, y, x + W, y + H))

    # dégradé sombre discret côté logo pour la lisibilité
    grad = Image.new('L', (1, H), 0)
    for j in range(H):
        d = j if where == 'top' else H - 1 - j
        t = max(0, 1 - d / (H * 0.30))
        grad.putpixel((0, j), int(130 * t ** 1.6))
    grad = grad.resize((W, H))
    im = Image.composite(Image.new('RGB', (W, H), (12, 20, 14)), im, grad)

    logo = Image.open(LOGO).convert('RGBA')
    lw = 440
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    # zones de sécurité IG : ~180 px en haut, ~300 px en bas
    y_logo = 200 if where == 'top' else H - 330 - logo.height
    im.paste(logo, ((W - lw) // 2, y_logo), logo)
    im.save(out, quality=94)

if __name__ == '__main__':
    story(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 0.5,
          sys.argv[4] if len(sys.argv) > 4 else 'top')
