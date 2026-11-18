"""contrast_colors.py: qa-img / qa-table. Palette, contrast, grayscale, page colour (D6, D7, D18, D19, I7, I12).

Usage: python qa/scripts/contrast_colors.py page.png [more.png]  |  main.pdf --pages 3,5 [--dpi 100]
          [--cover 1] [--figure] [--series 111111,A47864,E8C6C0] [--pairs "6B4B3D/FFFFFF=4.5"]

Per image (or per rendered PDF page):
  D19   page colour: the four corners must be white (#FFFFFF), except on --cover pages (ivory allowed)
  D6    palette: pixels that are not a palette colour or a blend of two palette colours (anti-aliasing).
        More than 0.2% unexplained pixels = failure (default hyperref blue/red boxes land here)
  D18   small text in mocha or powder pink (connected components shorter than 18 pt at the render dpi)
        have 3.85:1 / 1.4:1 contrast and fail the 4.5:1 rule
  I12   --figure: dominant series colours must differ by >= 20% relative luminance, or be direct-labelled (confirm by eye)
--pairs: explicit contrast checks FG/BG=min_ratio (hex), e.g. 6B4B3D/FFFFFF=4.5 . Needs numpy and PIL.
"""
import argparse
import os
import re
import sys
import tempfile
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_common import Report, front_arg, need_file, parse_range, render_pages

try:
    import numpy as np
    from PIL import Image
except ImportError:
    print("BLOCKED: needs numpy and Pillow (pip install numpy pillow)")
    sys.exit(2)

PALETTE = {"ink": "111111", "ivory": "F7F3EE", "mocha": "A47864", "pink": "E8C6C0", "mocha-deep": "6B4B3D",
           "mocha-pale": "D3BBAE", "grid": "E3DCD4", "muted": "6F6862", "white": "FFFFFF", "black": "000000"}


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def lum(c):
    def f(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(c1, c2):
    a, b = sorted((lum(c1), lum(c2)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def unexplained_fraction(arr, tol=14.0):
    """Fraction of pixels that are neither a palette colour nor a blend of two palette colours."""
    px = arr.reshape(-1, 3).astype(np.float32)
    uniq, inv, cnt = np.unique(px, axis=0, return_inverse=True, return_counts=True)
    pal = np.array([rgb(h) for h in PALETTE.values()], dtype=np.float32)
    ok = np.zeros(len(uniq), dtype=bool)
    for i in range(len(pal)):
        for j in range(i, len(pal)):
            a, b = pal[i], pal[j]
            d = b - a
            dd = float((d * d).sum())
            t = np.clip(((uniq - a) @ d) / dd, 0, 1) if dd > 0 else np.zeros(len(uniq))
            proj = a + t[:, None] * d
            ok |= np.sqrt(((uniq - proj) ** 2).sum(axis=1)) < tol
    bad = ~ok
    frac = cnt[bad].sum() / cnt.sum()
    worst = uniq[bad][np.argsort(-cnt[bad])][:3] if bad.any() else []
    return float(frac), ["#%02X%02X%02X" % tuple(int(x) for x in w) for w in worst]


def small_text_components(mask, max_h):
    """Connected components of a boolean mask with bbox height < max_h. Returns (small, large) counts."""
    ys, xs = np.nonzero(mask)
    if len(ys) == 0 or len(ys) > 300000:
        return 0, 0
    pts = set(zip(ys.tolist(), xs.tolist()))
    small = large = 0
    while pts:
        stack = [pts.pop()]
        y0 = y1 = stack[0][0]
        n = 0
        while stack:
            y, x = stack.pop()
            n += 1
            y0, y1 = min(y0, y), max(y1, y)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    q = (y + dy, x + dx)
                    if q in pts:
                        pts.remove(q)
                        stack.append(q)
        if n < 6:
            continue
        if (y1 - y0 + 1) < max_h:
            small += 1
        else:
            large += 1
    return small, large


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="PNG files, or one PDF with --pages")
    ap.add_argument("--pages", default="")
    ap.add_argument("--dpi", type=int, default=100)
    ap.add_argument("--cover", default="1", help="PDF pages allowed to be ivory (default 1); for PNGs use --cover-file")
    ap.add_argument("--cover-file", nargs="*", default=[])
    ap.add_argument("--figure", action="store_true")
    ap.add_argument("--series", default="")
    ap.add_argument("--pairs", default="")
    ap.add_argument("--tmp", default=os.path.join("qa", "tmp", "contrast"))
    front_arg(ap)
    a = ap.parse_args()
    rep = Report("img", "contrast_colors.py")

    items = []   # (label, path, is_cover)
    if a.inputs[0].lower().endswith(".pdf"):
        need_file(a.inputs[0], "PDF")
        pages = sorted(parse_range(a.pages)) or [1]
        cover = parse_range(a.cover)
        for p, path in sorted(render_pages(a.inputs[0], pages, a.dpi, a.tmp).items()):
            items.append((rep.where(page=p, front=a.front), path, p in cover))
    else:
        for path in a.inputs:
            need_file(path, "image")
            items.append((rep.where(file=path), path, os.path.basename(path) in [os.path.basename(c) for c in a.cover_file]))

    for spec in [s for s in a.pairs.split(",") if s]:
        m = re.match(r"([0-9A-Fa-f]{6})/([0-9A-Fa-f]{6})=([\d.]+)$", spec.strip())
        if m:
            r = ratio(rgb(m.group(1)), rgb(m.group(2)))
            rep.check("D18", r >= float(m.group(3)), sev="major", where="--pairs",
                      what="contrast %s on %s is %.2f:1, needs %.1f:1" % (m.group(1), m.group(2), r, float(m.group(3))),
                      recurring="yes", owner="fix-se / art-se (colour use)", places=[spec])

    for label, path, is_cover in items:
        img = np.array(Image.open(path).convert("RGB"))
        h, w, _ = img.shape
        # D19 page colour: mean of a 5x5 patch at each corner, away from the antialiased edge
        corners = [img[4:9, 4:9], img[4:9, w - 9:w - 4], img[h - 9:h - 4, 4:9], img[h - 9:h - 4, w - 9:w - 4]]
        cols = [tuple(int(v) for v in c.reshape(-1, 3).mean(axis=0)) for c in corners]
        target = rgb(PALETTE["ivory"] if is_cover else "FFFFFF")
        okc = all(max(abs(x - y) for x, y in zip(c, target)) <= 3 for c in cols)
        rep.check("D19", okc, sev="major", where=label,
                  what="page background is %s, expected %s%s" % ("#%02X%02X%02X" % cols[0], "ivory (cover)" if is_cover else "white",
                                                                   " (ivory only on the cover and inside boxes)" if not is_cover else ""),
                  recurring="yes", owner="fix-se", places=[label])
        # D6 palette
        frac, worst = unexplained_fraction(img)
        rep.check("D6", frac <= 0.002, sev="major", where=label,
                  what="%.2f%% of the pixels are not palette colours or blends of two palette colours" % (frac * 100),
                  evidence="most common off-palette colours: %s" % ", ".join(worst), recurring="yes",
                  owner="fix-se (CLS colours, hyperref) / art-se (figures)", places=[label])
        # D18 small mocha / pink text
        bgc = np.array(rgb("FFFFFF" if not is_cover else PALETTE["ivory"]))
        for name in ("mocha", "pink"):
            col = np.array(rgb(PALETTE[name]))
            mask = (np.abs(img.astype(int) - col).max(axis=2) <= 6)
            small, large = small_text_components(mask, 18.0 / 72.0 * a.dpi)
            r = ratio(rgb(PALETTE[name]), tuple(int(x) for x in bgc))
            if r < 4.5:
                rep.check("D18", small < 8, sev="major", where=label,
                          what="%d small component(s) (< 18 pt) in %s (contrast %.2f:1, text needs 4.5:1): small text or thin marks in a low-contrast colour"
                               % (small, name, r),
                          evidence="large components (>= 18 pt): %d. Allowed for large type, rules, fills; not for small text" % large,
                          recurring="yes", owner="fix-se (use mocha-deep for small text)", places=[label])
        # I12 grayscale gaps among dominant colours
        if a.figure or a.series:
            if a.series:
                series = [rgb(s) for s in a.series.split(",") if s]
            else:
                px = Counter(map(tuple, img.reshape(-1, 3)[::7].tolist()))
                series = [c for c, n in px.most_common(40) if n > 0.004 * (h * w / 7) and max(abs(c[0] - 255), abs(c[1] - 255), abs(c[2] - 255)) > 12][:5]
            gaps = [(a1, b1, abs(lum(a1) - lum(b1))) for i, a1 in enumerate(series) for b1 in series[i + 1:]]
            weak = [g for g in gaps if g[2] < 0.20]
            rep.check("I12", not weak, sev="major", where=label,
                      what="%d pair(s) of series colours differ by < 20%% luminance in grayscale: they need direct labels (confirm by eye)" % len(weak),
                      evidence="; ".join("#%02X%02X%02X vs #%02X%02X%02X: %.2f" % (*g[0], *g[1], g[2]) for g in weak[:4]),
                      recurring="yes", owner="art-se (ct_style.py)", places=[label])
    sys.exit(rep.emit())


if __name__ == "__main__":
    main()
