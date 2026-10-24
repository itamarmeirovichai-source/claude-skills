"""Light film finish (same recipe as v1) + contact sheet. Usage: python3 finish.py <pick.png> <outdir>"""
import sys, glob, os
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB").resize((1080, 1080), Image.LANCZOS)
im = im.filter(ImageFilter.GaussianBlur(0.5))
im = ImageEnhance.Contrast(im).enhance(0.96)
im = ImageEnhance.Color(im).enhance(0.92)
a = np.asarray(im).astype(np.float32)
luma = (0.299*a[...,0] + 0.587*a[...,1] + 0.114*a[...,2]) / 255.0
rng = np.random.default_rng(1080)
g = rng.normal(0, 1, luma.shape).astype(np.float32)
g = np.asarray(Image.fromarray(((g*40)+128).clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32) - 128
w = 0.35 + 0.65*np.clip(1 - np.abs(luma - 0.45)*1.6, 0, 1)   # grain strongest in midtones
a = np.clip(a + (g/40*4.0*w)[..., None], 0, 255)
im = Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.UnsharpMask(radius=1.2, percent=35, threshold=2))
im.save(os.path.join(out, "otto_v2_pfp_1080.png"), optimize=True)
im.resize((320, 320), Image.LANCZOS).save(os.path.join(out, "otto_v2_pfp_320.png"), optimize=True)

def circ(img, s=110):
    t = img.convert("RGB").resize((s*4, s*4), Image.LANCZOS)
    m = Image.new("L", (s*4, s*4), 0); ImageDraw.Draw(m).ellipse([0, 0, s*4-1, s*4-1], fill=255)
    bg = Image.new("RGB", (s*4, s*4), (250, 250, 250)); bg.paste(t, (0, 0), m)
    return bg.resize((s, s), Image.LANCZOS)
try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
except Exception: font = ImageFont.load_default()
here = os.path.dirname(os.path.abspath(__file__))
items = [(f, os.path.basename(f)[:-8]) for f in sorted(glob.glob(os.path.join(here, "explore", "e*_t01.png")))]
items += [(f, os.path.basename(f)[:-8]) for f in sorted(glob.glob(os.path.join(here, "final", "g*_t01.png")))]
items += [(os.path.join(here, "ref", "v1_face.png"), "v1 final (before)"), (os.path.join(out, "otto_v2_pfp_1080.png"), "v2 PICK g1 finished")]
T, C, P = 300, 110, 20
cols = 5; rows = (len(items) + cols - 1)//cols
cw, ch = T + 2*P, T + C + 3*P + 24
sheet = Image.new("RGB", (cols*cw, rows*ch + 50), (250, 250, 250)); d = ImageDraw.Draw(sheet)
d.text((P, 15), "OTTO PFP v2 - Soul Cinema x6 explore, Flare 2k x2 finals, finished pick (square + 110 px circle)", fill=(20, 20, 20), font=font)
for i, (f, lab) in enumerate(items):
    x, y = (i % cols)*cw + P, (i//cols)*ch + 50
    im2 = Image.open(f)
    sheet.paste(im2.convert("RGB").resize((T, T), Image.LANCZOS), (x, y))
    d.text((x, y + T + 6), lab, fill=(180, 20, 20) if "PICK" in lab else (20, 20, 20), font=font)
    sheet.paste(circ(im2, C), (x + (T - C)//2, y + T + 30))
sheet.save(os.path.join(out, "otto_v2_contact_sheet.png"), optimize=True)
print("ok")
