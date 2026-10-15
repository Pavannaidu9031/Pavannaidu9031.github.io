"""Turns a photo on a plain white background into portrait.webp (transparent) and avatar.webp.

    python tools/cutout.py uploads/Profile.jpeg
"""
import sys
from collections import deque
from pathlib import Path
from PIL import Image, ImageFilter, ImageChops

src = Image.open(sys.argv[1]).convert("RGB")
w, h = src.size
px = src.load()

# flood-fill near-white pixels connected to the top/left/right edges = background
bg = Image.new("L", (w, h), 0)
m = bg.load()
def white(p, t=232):
    return p[0] > t and p[1] > t and p[2] > t
q = deque()
for x in range(w):
    q.append((x, 0))
for y in range(h):
    q.append((0, y)); q.append((w - 1, y))
while q:
    x, y = q.popleft()
    if m[x, y] or not white(px[x, y]):
        continue
    m[x, y] = 255
    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        if 0 <= nx < w and 0 <= ny < h and not m[nx, ny]:
            q.append((nx, ny))

# enclosed white gaps (between arms and body) in the lower part of the photo
for y in range(int(h * 0.4), h):
    for x in range(w):
        if white(px[x, y], 236):
            m[x, y] = 255

alpha = ImageChops.invert(bg).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
out = src.convert("RGBA")
out.putalpha(alpha)
out = out.crop(out.getbbox())
img = Path("assets/img")
target_h = 1200
out = out.resize((round(out.width * target_h / out.height), target_h), Image.LANCZOS)
out.save(img / "portrait.webp", quality=86, method=6)
print("portrait", out.size)

# square avatar centred on the face, on the site's dark-grey
face = src.crop((w * 0.22, h * 0.03, w * 0.78, h * 0.03 + w * 0.56)).resize((300, 300), Image.LANCZOS)
face.save(img / "avatar.webp", quality=88)
print("avatar", face.size)
