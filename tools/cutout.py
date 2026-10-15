"""Turns a photo on a plain white background into portrait.webp (transparent) and avatar.webp.

    python tools/cutout.py uploads/Profile.jpeg

1. Flood-fill the near-white background from the image edges (plus enclosed
   white gaps in the lower half, e.g. between arms and body).
2. Along the edge of the person, "un-mix" the white: each edge pixel is
   treated as  colour = a * foreground + (1 - a) * white,  where the
   foreground colour is the darkest colour nearby. This gives a soft alpha
   for hair strands and removes the white halo instead of leaving it grey.
"""
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

src = Image.open(sys.argv[1]).convert("RGB")
w, h = src.size
rgb = np.asarray(src).astype(np.float32)
px = src.load()

# ---- 1. hard background mask ----
bg = np.zeros((h, w), bool)
def white(p, t=232):
    return p[0] > t and p[1] > t and p[2] > t
q = deque([(x, 0) for x in range(w)] + [(0, y) for y in range(h)] + [(w - 1, y) for y in range(h)])
while q:
    x, y = q.popleft()
    if bg[y, x] or not white(px[x, y]):
        continue
    bg[y, x] = True
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if 0 <= nx < w and 0 <= ny < h and not bg[ny, nx]:
            q.append((nx, ny))
bg[int(h * 0.4):] |= rgb[int(h * 0.4):].min(axis=2) > 236

# ---- 2. soft edge with the white removed ----
def to_img(a):
    return Image.fromarray((a * 255).astype(np.uint8))

fg = ~bg
# edge band: foreground pixels within ~6 px of the background
near_bg = np.asarray(to_img(bg).filter(ImageFilter.MaxFilter(13))) > 0
band = fg & near_bg
# white peeking through gaps between hair strands, a little further in
near_bg_wide = np.asarray(to_img(bg).filter(ImageFilter.MaxFilter(41))) > 0
band |= fg & near_bg_wide & (rgb.min(axis=2) > 195)
# light, colourless (grey) pixels near the edge are background bled into hair tips by JPEG;
# skin is never neutral grey, so it is left alone
neutral = (rgb.max(axis=2) - rgb.min(axis=2)) < 22
band |= fg & near_bg_wide & neutral & (rgb.min(axis=2) > 105)

lum = rgb.mean(axis=2)
W = 247.0  # brightness of the studio background
# local foreground brightness = darkest value in a 15 px window (hair -> dark, skin -> skin)
lum_img = Image.fromarray(np.clip(lum, 0, 255).astype(np.uint8))
lf = np.asarray(lum_img.filter(ImageFilter.MinFilter(15))).astype(np.float32)

alpha = fg.astype(np.float32)
a_band = np.clip((W - lum) / np.maximum(W - lf, 25.0), 0.0, 1.0)
alpha[band] = a_band[band]

# un-mix white from edge colours: F = (C - (1 - a) * W) / a
a3 = np.maximum(alpha, 0.05)[..., None]
fg_rgb = np.where(band[..., None], (rgb - (1 - a3) * W) / a3, rgb)
fg_rgb = np.clip(fg_rgb, 0, 255)

# slight soften so the edge isn't jagged, then drop near-transparent specks
alpha = np.asarray(to_img(alpha).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32) / 255.0
alpha[alpha < 0.06] = 0.0

img = Image.fromarray(np.dstack([fg_rgb, alpha * 255]).astype(np.uint8), "RGBA")
img = img.crop(img.getbbox())

dest = Path("assets/img")
target_h = 1200
img = img.resize((round(img.width * target_h / img.height), target_h), Image.LANCZOS)
img.save(dest / "portrait.webp", quality=88, method=6)
print("portrait", img.size)

# square avatar centred on the face (keeps the original background)
face = src.crop((int(w * 0.22), int(h * 0.03), int(w * 0.78), int(h * 0.03 + w * 0.56))).resize((300, 300), Image.LANCZOS)
face.save(dest / "avatar.webp", quality=88)
print("avatar", face.size)
