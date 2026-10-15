"""Generates the placeholder portrait, favicon and project illustrations (SVG).

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


# ---------- 01 fiber-optic hydrogen sensor ----------

fiber_cover = panel(fill="#eef1f7") + """
<rect x="70" y="268" width="660" height="64" rx="32" fill="#d5dbe8"/>
<path d="M70 268 H250 C300 268 310 286 350 286 H450 C490 286 500 268 550 268 H730 V332 H550 C500 332 490 314 450 314 H350 C310 314 300 332 250 332 H70 Z" fill="#c4ccde"/>
<rect x="70" y="293" width="660" height="14" fill="#7d8db3"/>
<rect x="338" y="279" width="124" height="42" rx="10" fill="#e6c34a"/>
<rect x="338" y="279" width="124" height="42" rx="10" fill="none" stroke="#6f7380" stroke-width="5"/>
<rect x="346" y="293" width="108" height="14" fill="#7d8db3"/>
<path d="M90 300 H700" stroke="#e5484d" stroke-width="3" stroke-dasharray="14 10"/>
<path d="M688 290 L708 300 L688 310" fill="none" stroke="#e5484d" stroke-width="3"/>
""" + h2(360, 210) + h2(420, 182) + h2(470, 228) + """
<path d="M378 236 L388 262 M440 206 L430 262 M478 252 L460 264" stroke="#9fb4ff" stroke-width="2" stroke-dasharray="4 5"/>
""" + label(80, 100, "Fiber-optic H₂ sensor", 30) + label(80, 132, "WO₃ + Pd on etched single-mode fiber", 18, "#5b6070", weight=400) \
    + label(400, 372, "WO₃ + Pd coating", 16, anchor="middle") + label(92, 372, "1310 nm", 16, "#e5484d") \
    + label(400, 160, "H₂", 18, "#4d64d6", anchor="middle") \
    + label(80, 520, "~9 µm core region", 15, "#5b6070", weight=400) + label(720, 520, "intensity readout", 15, "#5b6070", "end", 400)
write("projects/fiber-optic-hydrogen-sensor/cover.svg", fiber_cover)

fiber_detail = panel(fill="#eef1f7") + """
<rect x="110" y="120" width="220" height="50" rx="8" fill="#55607a"/>
<rect x="110" y="120" width="220" height="50" rx="8" fill="none" stroke="#2c3346" stroke-width="3"/>
<rect x="470" y="120" width="220" height="50" rx="8" fill="#9aa1ad"/>
<rect x="470" y="120" width="220" height="50" rx="8" fill="none" stroke="#2c3346" stroke-width="3"/>
<path d="M220 176 Q240 240 330 300 M580 176 Q560 240 470 300" stroke="#b58cff" stroke-width="4" fill="none" stroke-dasharray="2 9" stroke-linecap="round"/>
<circle cx="400" cy="380" r="120" fill="#c4ccde"/>
<circle cx="400" cy="380" r="88" fill="#6f7380"/>
<circle cx="400" cy="380" r="76" fill="#e6c34a"/>
<circle cx="400" cy="380" r="56" fill="#c4ccde"/>
<circle cx="400" cy="380" r="18" fill="#7d8db3"/>
<path d="M400 290 A90 90 0 0 1 488 372" stroke="#1c1d20" stroke-width="2" fill="none" stroke-dasharray="3 5"/>
""" + label(220, 152, "WO₃ · RF", 18, "#fff", "middle") + label(580, 152, "Pd · DC", 18, "#1c1d20", "middle") \
    + label(80, 84, "Ring coating around the fiber", 22) \
    + label(540, 470, "Pd", 16) + label(540, 498, "WO₃", 16) + label(540, 526, "etched fiber", 16, "#5b6070", weight=400) \
    + label(400, 386, "core", 13, "#fff", "middle")
write("projects/fiber-optic-hydrogen-sensor/detail.svg", fiber_detail)


# ---------- 02 MatrixAI ----------

def window(fill="#f7f8f7"):
    return panel(fill=fill) + """
<rect x="40" y="40" width="720" height="44" rx="18" fill="#e3e8e6"/><rect x="40" y="66" width="720" height="18" fill="#e3e8e6"/>
<circle cx="70" cy="62" r="6" fill="#ff6159"/><circle cx="90" cy="62" r="6" fill="#ffbd2e"/><circle cx="110" cy="62" r="6" fill="#28c941"/>
<rect x="300" y="52" width="200" height="20" rx="10" fill="#fff"/>
"""


matrix_cover = window() + """
<rect x="60" y="104" width="150" height="436" rx="10" fill="#0f3d3a"/>
<rect x="76" y="160" width="118" height="12" rx="6" fill="#4fb8a8"/>
<rect x="76" y="190" width="90" height="10" rx="5" fill="#ffffff55"/>
<rect x="76" y="214" width="100" height="10" rx="5" fill="#ffffff55"/>
<rect x="76" y="238" width="80" height="10" rx="5" fill="#ffffff55"/>
<rect x="230" y="104" width="330" height="270" rx="10" fill="#fff" stroke="#e0e5e3"/>
<path d="M260 340 H540 M260 340 V130" stroke="#c9d1ce" stroke-width="2"/>
<g fill="#9cc8c0">
<circle cx="290" cy="300" r="6"/><circle cx="320" cy="280" r="6"/><circle cx="345" cy="296" r="6"/><circle cx="372" cy="250" r="6"/>
<circle cx="400" cy="262" r="6"/><circle cx="420" cy="222" r="6"/><circle cx="452" cy="236" r="6"/><circle cx="470" cy="200" r="6"/>
</g>
<path d="M280 312 C360 280 420 220 520 168" stroke="#0f3d3a" stroke-width="2.5" fill="none"/>
<circle cx="506" cy="174" r="11" fill="#455ce9"/><circle cx="506" cy="174" r="20" fill="none" stroke="#455ce9" stroke-width="2" opacity=".5"/>
<rect x="580" y="104" width="160" height="270" rx="10" fill="#0f3d3a"/>
<rect x="596" y="160" width="128" height="8" rx="4" fill="#ffffff33"/><rect x="596" y="160" width="92" height="8" rx="4" fill="#4fb8a8"/>
<rect x="596" y="216" width="128" height="8" rx="4" fill="#ffffff33"/><rect x="596" y="216" width="60" height="8" rx="4" fill="#4fb8a8"/>
<rect x="596" y="272" width="128" height="8" rx="4" fill="#ffffff33"/><rect x="596" y="272" width="108" height="8" rx="4" fill="#4fb8a8"/>
<rect x="596" y="318" width="128" height="36" rx="18" fill="#455ce9"/>
<rect x="230" y="394" width="510" height="146" rx="10" fill="#fff" stroke="#e0e5e3"/>
""" + label(76, 136, "MatrixAI", 18, "#fff") + label(246, 128, "Suggested next run", 14, "#5b6070", weight=400) \
    + label(596, 136, "Parameters", 14, "#fff") + label(596, 152, "Power", 12, "#ffffffaa", weight=400) \
    + label(596, 208, "Pressure", 12, "#ffffffaa", weight=400) + label(596, 264, "Ar flow", 12, "#ffffffaa", weight=400) \
    + label(660, 341, "Suggest", 14, "#fff", "middle") \
    + label(250, 424, "Experiment ledger", 14, "#5b6070", weight=400) \
    + "".join(f'<rect x="250" y="{440 + k * 28}" width="470" height="18" rx="4" fill="{c}"/>' for k, c in enumerate(["#eef3f2", "#f6f8f8", "#eef3f2"]))
write("projects/matrixai/cover.svg", matrix_cover)

rows = ""
for k, (mat, col) in enumerate([("WO₃", "#e6c34a"), ("Pd", "#9aa1ad"), ("ITO", "#7fc4e8"), ("WO₃", "#e6c34a"), ("Pd", "#9aa1ad"), ("WO₃", "#e6c34a")]):
    y = 180 + k * 54
    rows += f'<rect x="70" y="{y}" width="660" height="44" rx="8" fill="{"#fff" if k % 2 else "#f1f5f4"}"/>'
    rows += f'<rect x="86" y="{y + 11}" width="60" height="22" rx="11" fill="{col}"/>' + label(116, y + 27, mat, 13, anchor="middle")
    rows += f'<rect x="180" y="{y + 17}" width="{120 + (k * 37) % 90}" height="10" rx="5" fill="#cfd8d5"/>'
    rows += f'<rect x="420" y="{y + 17}" width="{60 + (k * 53) % 80}" height="10" rx="5" fill="#cfd8d5"/>'
    rows += f'<rect x="600" y="{y + 12}" width="110" height="20" rx="10" fill="#0f3d3a" opacity="{0.25 + (k % 3) * 0.25}"/>'
matrix_detail = window() + label(70, 130, "Experiment ledger", 24) \
    + label(86, 166, "Material", 13, "#5b6070", weight=400) + label(180, 166, "Run notes", 13, "#5b6070", weight=400) \
    + label(420, 166, "Parameters", 13, "#5b6070", weight=400) + label(600, 166, "Result", 13, "#5b6070", weight=400) + rows
write("projects/matrixai/detail.svg", matrix_detail)


# ---------- 03 fiber etching ----------

etch_cover = panel(fill="#f3eff6") + """
<rect x="210" y="440" width="300" height="40" rx="8" fill="#3b2f4a"/>
<circle cx="250" cy="460" r="8" fill="#ff8a65"/>
<path d="M250 230 V420 Q250 436 266 436 H454 Q470 436 470 420 V230" fill="#ffffffaa" stroke="#3b2f4a" stroke-width="4"/>
<path d="M254 300 H466 V420 Q466 432 454 432 H266 Q254 432 254 420 Z" fill="#c9b8e6" opacity=".8"/>
<path d="M360 120 V400" stroke="#7d8db3" stroke-width="10" stroke-linecap="round"/>
<path d="M360 300 V400" stroke="#7d8db3" stroke-width="4" stroke-linecap="round"/>
<g stroke="#3b2f4a" stroke-width="3" fill="#fff"><rect x="560" y="160" width="36" height="250" rx="18"/></g>
<rect x="570" y="250" width="16" height="150" rx="8" fill="#e5484d"/>
<circle cx="578" cy="412" r="22" fill="#e5484d"/>
<g stroke="#3b2f4a" stroke-width="2"><path d="M600 200 H614 M600 240 H614 M600 280 H614 M600 320 H614 M600 360 H614"/></g>
""" + label(80, 100, "Fiber etching study", 30) + label(80, 132, "Temperature-controlled HF etching", 18, "#5b6070", weight=400) \
    + label(624, 205, "110 °C", 15, weight=400) + label(624, 365, "60 °C", 15, weight=400) \
    + label(360, 290, "HF", 18, "#3b2f4a", "middle") + label(80, 520, "60–110 °C · optical power", 15, "#5b6070", weight=400)
write("projects/fiber-etching-study/cover.svg", etch_cover)

etch_detail = panel(fill="#f3eff6") + """
<rect x="80" y="250" width="130" height="90" rx="12" fill="#3b2f4a"/>
<rect x="600" y="250" width="130" height="90" rx="12" fill="#3b2f4a"/>
<rect x="620" y="272" width="90" height="30" rx="4" fill="#c9f2d0"/>
<path d="M210 295 C260 295 270 400 330 400 H470 C530 400 540 295 600 295" stroke="#7d8db3" stroke-width="6" fill="none"/>
<path d="M210 295 C260 295 270 400 330 400 H470 C530 400 540 295 600 295" stroke="#e5484d" stroke-width="2" fill="none" stroke-dasharray="10 8"/>
<rect x="300" y="360" width="200" height="80" rx="10" fill="#c9b8e6" opacity=".85"/>
<rect x="290" y="450" width="220" height="26" rx="6" fill="#3b2f4a"/>
""" + label(80, 100, "Etch and measure", 26) + label(80, 132, "Optical power is logged while the fiber sits in the heated bath", 17, "#5b6070", weight=400) \
    + label(145, 300, "Laser", 16, "#fff", "middle") + label(145, 322, "1310 nm", 13, "#ffffffbb", "middle", 400) \
    + label(665, 293, "dBm", 14, "#1c1d20", "middle") + label(665, 328, "Power meter", 13, "#ffffffbb", "middle", 400) \
    + label(400, 408, "HF bath", 15, "#3b2f4a", "middle") + label(400, 468, "hot plate · 60–110 °C", 13, "#fff", "middle", 400)
write("projects/fiber-etching-study/detail.svg", etch_detail)


# ---------- 04 Maa restaurant ----------

def qr(x, y, s=8):
    import random
    rnd = random.Random(7)
    out = f'<rect x="{x - 8}" y="{y - 8}" width="{21 * s + 16}" height="{21 * s + 16}" rx="8" fill="#fff"/>'
    for i in range(21):
        for j in range(21):
            finder = any(i0 <= i < i0 + 7 and j0 <= j < j0 + 7 for i0, j0 in ((0, 0), (0, 14), (14, 0)))
            if finder:
                ii, jj = (i % 7 if i < 7 else (i - 14) % 7), (j % 7 if j < 7 else (j - 14) % 7)
                on = ii in (0, 6) or jj in (0, 6) or (2 <= ii <= 4 and 2 <= jj <= 4)
            else:
                on = rnd.random() < 0.45
            if on:
                out += f'<rect x="{x + j * s}" y="{y + i * s}" width="{s}" height="{s}" fill="#5a2a12"/>'
    return out


menu_rows = ""
for k, w in enumerate([150, 120, 170, 130]):
    y = 220 + k * 70
    menu_rows += f'<rect x="268" y="{y}" width="48" height="48" rx="10" fill="#e9b872"/>'
    menu_rows += f'<rect x="328" y="{y + 8}" width="{w}" height="10" rx="5" fill="#5a2a12"/>'
    menu_rows += f'<rect x="328" y="{y + 28}" width="60" height="9" rx="4" fill="#c99a6b"/>'
    menu_rows += f'<circle cx="514" cy="{y + 24}" r="13" fill="#5a2a12"/><path d="M508 {y + 24} H520 M514 {y + 18} V{y + 30}" stroke="#fff" stroke-width="2"/>'
maa_cover = panel(fill="#f7efe3") + """
<rect x="250" y="70" width="300" height="470" rx="40" fill="#2b1a10"/>
<rect x="262" y="82" width="276" height="446" rx="30" fill="#fffaf2"/>
<rect x="352" y="94" width="96" height="18" rx="9" fill="#2b1a10"/>
<rect x="268" y="132" width="264" height="64" rx="14" fill="#5a2a12"/>
""" + label(288, 160, "Maa Restaurant", 18, "#fff") + label(288, 182, "Puttur · menu", 13, "#f3d9b5", weight=400) + menu_rows \
    + label(268, 512, "", 12) + qr(590, 330, 6) + label(653, 480, "Table 4", 15, "#5a2a12", "middle") \
    + label(80, 100, "Order", 26, "#5a2a12") + label(80, 128, "from the table", 18, "#8a5a3a", weight=400)
write("projects/maa-restaurant-platform/cover.svg", maa_cover)

cols = ""
for k, (name, n) in enumerate([("New", 2), ("In the kitchen", 3), ("Ready", 1)]):
    x = 70 + k * 228
    cols += f'<rect x="{x}" y="150" width="208" height="380" rx="12" fill="#fff8ee"/>' + label(x + 16, 182, name, 15, "#5a2a12")
    for r in range(n):
        y = 200 + r * 104
        cols += f'<rect x="{x + 12}" y="{y}" width="184" height="90" rx="10" fill="#fff" stroke="#ead9c2"/>'
        cols += f'<rect x="{x + 26}" y="{y + 16}" width="70" height="10" rx="5" fill="#5a2a12"/>'
        cols += f'<rect x="{x + 26}" y="{y + 36}" width="130" height="8" rx="4" fill="#d8bfa0"/>'
        cols += f'<rect x="{x + 26}" y="{y + 52}" width="100" height="8" rx="4" fill="#d8bfa0"/>'
        cols += f'<rect x="{x + 120}" y="{y + 64}" width="64" height="18" rx="9" fill="{["#e5484d", "#e9a23b", "#3aa76d"][k]}"/>'
maa_detail = panel(fill="#f7efe3") + label(70, 112, "Live order board", 26, "#5a2a12") + cols
write("projects/maa-restaurant-platform/detail.svg", maa_detail)
