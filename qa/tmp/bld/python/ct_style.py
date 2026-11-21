"""ClosetTwin shared chart style. Every graph script does:  import ct_style as ct

Palette is fixed by the team (PRD); tints are derived from mocha only (no new hues).
Fonts: Playfair Display (headings) / Rubik (body) from <root>/fonts/*.ttf when present;
otherwise falls back to Georgia / Segoe UI / DejaVu so scripts still run.
"""
from pathlib import Path
import matplotlib as mpl
from matplotlib import font_manager as fm
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figures"
FONT_DIR = ROOT / "fonts"

# --- fixed palette -------------------------------------------------------
INK, IVORY, MOCHA, PINK = "#111111", "#F7F3EE", "#A47864", "#E8C6C0"
# --- derived tints (mocha mixed with ink / ivory; same hue) --------------
MOCHA_DEEP = "#6B4B3D"   # mocha 60% + ink 40%
MOCHA_PALE = "#D3BBAE"   # mocha 50% + ivory 50%
GRID = "#E3DCD4"         # hairline grid on ivory
MUTED = "#6F6862"        # secondary text (contrast >= 4.5:1 on ivory)

# categorical order: assign by entity, never cycle, max 4 series
CAT = [INK, MOCHA, PINK, MOCHA_DEEP]
# sequential (magnitude), light -> dark, one hue
SEQ = [PINK, MOCHA_PALE, MOCHA, MOCHA_DEEP, INK]

# --- geometry ------------------------------------------------------------
TEXTWIDTH_IN = 5.906     # 15.0 cm text width (master-se; the CLS value). Single source of truth
BODY_PT = 9              # in-figure text size at 1:1 (body is ~11pt)
SMALL_PT = 8

HEAD_FONT, BODY_FONT = "Playfair Display", "Rubik"
USING_BRAND_FONTS = True


def _register_fonts():
    """Add the static brand TTFs by path. No fallback: a missing font is an error (qa I8)."""
    files = sorted(FONT_DIR.glob("*.ttf"))   # top level only; fonts/source/ is not used
    if not files:
        raise FileNotFoundError(f"no fonts found in {FONT_DIR}")
    for p in files:
        fm.fontManager.addfont(str(p))
    have = {f.name for f in fm.fontManager.ttflist}
    for name in (HEAD_FONT, BODY_FONT):
        if name not in have:
            raise RuntimeError(f"font {name!r} not found in {FONT_DIR}")


_register_fonts()


def apply():
    mpl.rcParams.update({
        "figure.facecolor": "none", "axes.facecolor": "none", "savefig.facecolor": "none",  # page is white
        "savefig.transparent": True,
        "font.family": BODY_FONT, "font.size": BODY_PT, "text.color": INK,
        "axes.labelcolor": MUTED, "axes.labelsize": SMALL_PT,
        "axes.edgecolor": INK, "axes.linewidth": 0.6,
        "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
        "axes.grid": True, "axes.grid.axis": "y", "axes.axisbelow": True,
        "grid.color": GRID, "grid.linewidth": 0.5,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "xtick.labelsize": SMALL_PT, "ytick.labelsize": SMALL_PT,
        "xtick.major.size": 0, "ytick.major.size": 0,
        "axes.prop_cycle": mpl.cycler(color=CAT),
        "lines.linewidth": 1.8, "lines.solid_capstyle": "round",
        "patch.linewidth": 0.6, "patch.edgecolor": INK,
        "legend.frameon": False, "legend.fontsize": SMALL_PT,
        "pdf.fonttype": 42, "ps.fonttype": 42,      # embed TrueType, keep text real
        "figure.constrained_layout.use": True,   # fixed canvas, no bbox tight
        "figure.constrained_layout.h_pad": 0.04, "figure.constrained_layout.w_pad": 0.04,
        "svg.fonttype": "none",
    })


def figure(width_frac=1.0, aspect=0.55, **kw):
    r"""Fixed canvas of exactly width_frac * \textwidth; the PDF page size is that width,
    so \includegraphics[width=<same fraction>\textwidth] scales by 1.0 and type stays 8pt."""
    w = TEXTWIDTH_IN * width_frac
    return plt.subplots(figsize=(w, w * aspect), **kw)


def head(ax, text, **kw):
    """Optional in-figure heading/hero number in Playfair (captions normally live in LaTeX)."""
    kw.setdefault("fontfamily", HEAD_FONT)
    kw.setdefault("fontsize", 12)
    return ax.text(0, 1.04, text, transform=ax.transAxes, **kw)


def label(ax, x, y, text, color=INK, dx=4, dy=0, ha="left", va="center", **kw):
    """Direct label in text ink (text never wears the series color)."""
    return ax.annotate(text, (x, y), xytext=(dx, dy), textcoords="offset points",
                       ha=ha, va=va, fontsize=SMALL_PT, color=color, **kw)


def outlined(**kw):
    """Fill kwargs for bars/areas: hairline ink edge keeps pale fills visible and grayscale-safe."""
    return {"edgecolor": INK, "linewidth": 0.6, **kw}


def save(fig, name):
    """Write figures/<name>.pdf (vector). Returns the path."""
    FIG_DIR.mkdir(exist_ok=True)
    out = FIG_DIR / f"{name}.pdf"
    fig.savefig(out)
    return out


apply()
