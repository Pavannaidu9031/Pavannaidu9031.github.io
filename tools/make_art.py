"""Generates the favicon and placeholder portrait/avatar (SVG).

    python tools/make_art.py

Swap any of these for real photos later: drop a .webp/.jpg next to them and
point content.py (portrait) or build.py (cover/detail) at it.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
FONT = "font-family=\"Inter, Helvetica Neue, Arial, sans-serif\""


def write(rel, body, w=800, h=600):
    p = IMG / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {FONT}>{body}</svg>\n',
        encoding="utf-8",
    )
    print("wrote", p.relative_to(ROOT))


def panel(x=40, y=40, w=720, h=520, fill="#f4f1ea"):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="{fill}"/>'


def label(x, y, text, size=18, fill="#1c1d20", anchor="start", weight=500, opacity=1):
    # scaled up so text stays readable when the image is shown small (home tiles, phone cards)
    size = max(round(size * 1.3), 18)
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" opacity="{opacity}">{text}</text>'


def h2(x, y):
    return f'<g><circle cx="{x}" cy="{y}" r="9" fill="#9fb4ff"/><circle cx="{x + 14}" cy="{y}" r="9" fill="#9fb4ff"/></g>'


# ---------- portrait + avatar + favicon ----------

write("portrait-placeholder.svg", """
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7f8385"/><stop offset="1" stop-color="#55585b"/></linearGradient></defs>
<ellipse cx="500" cy="380" rx="170" ry="200" fill="url(#g)"/>
<path d="M120 1100 C140 800 300 660 500 640 C700 660 860 800 880 1100 Z" fill="url(#g)"/>
<rect x="440" y="540" width="120" height="130" rx="40" fill="#6c7072"/>
""", 1000, 1100)

write("avatar-placeholder.svg", """
<rect width="200" height="200" fill="#3a3b3f"/>
<text x="100" y="124" font-size="72" fill="#e9ebec" text-anchor="middle" font-weight="500">PK</text>
""", 200, 200)

write("favicon.svg", """
<circle cx="32" cy="32" r="32" fill="#1c1d20"/>
<text x="32" y="43" font-size="32" fill="#fff" text-anchor="middle" font-weight="600">P</text>
""", 64, 64)
