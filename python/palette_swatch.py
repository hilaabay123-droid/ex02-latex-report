"""Palette swatch -> docs/screenshots/palette-swatch.png.  Run: python python/palette_swatch.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ct_style as ct
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

OUT = ct.ROOT / "docs" / "screenshots" / "palette-swatch.png"
core = [("Ink", ct.INK), ("Ivory", ct.IVORY), ("Mocha", ct.MOCHA), ("Powder pink", ct.PINK)]
tints = [("Mocha deep", ct.MOCHA_DEEP), ("Mocha pale", ct.MOCHA_PALE)]

fig = plt.figure(figsize=(8, 4.2), facecolor=ct.IVORY)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 8); ax.set_ylim(0, 4.2); ax.axis("off"); ax.grid(False)
ax.text(0.4, 3.85, "ClosetTwin palette", fontfamily=ct.HEAD_FONT, fontsize=20, color=ct.INK, va="center")
ax.text(0.4, 3.5, "Playfair Display headings  ·  Rubik body"
        + ("" if ct.USING_BRAND_FONTS else "  (fallback fonts in use)"),
        fontfamily=ct.BODY_FONT, fontsize=8, color=ct.MUTED, va="center")

def dark(h):
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (1, 3, 5)); return 0.2126*r+0.7152*g+0.0722*b < 0.5

for i, (n, h) in enumerate(core):
    x = 0.4 + i * 1.85
    ax.add_patch(Rectangle((x, 1.35), 1.65, 1.8, fc=h, ec=ct.INK, lw=0.6))
    ax.text(x, 1.1, n, fontfamily=ct.HEAD_FONT, fontsize=11, color=ct.INK, va="center")
    ax.text(x, 0.85, h.upper(), fontfamily=ct.BODY_FONT, fontsize=8.5, color=ct.MUTED, va="center")
ax.text(0.4, 0.45, "Derived tints (mocha only):", fontfamily=ct.BODY_FONT, fontsize=7.5, color=ct.MUTED, va="center")
for i, (n, h) in enumerate(tints):
    x = 2.55 + i * 2.2
    ax.add_patch(Rectangle((x, 0.3), 0.35, 0.3, fc=h, ec=ct.INK, lw=0.6))
    ax.text(x + 0.45, 0.45, f"{n}  {h}", fontfamily=ct.BODY_FONT, fontsize=7.5, color=ct.INK, va="center")
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT, dpi=200, bbox_inches=None)
print(OUT)
