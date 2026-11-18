"""bbox_margin.py: qa-code / qa-typeset. Text outside the margins, measured margins (criteria L9, K1, D16).

Usage: python qa/scripts/bbox_margin.py main.pdf [--min-margin 2.5] [--pages 5-9] [--skip 1] [--front K]
          [--text-width 15.0]

For every word on the selected pages (from `pdftotext -bbox`) the distance to the page edge is computed.
L9/K1  a word closer than --min-margin cm to the left or right edge (default 2.5 cm, PRD margins are 3.0 cm,
       tolerance 0.5 pt), i.e. text outside the margin. Banner/footer words count too: they must stay inside.
D16    reports the measured left/right/top/bottom margins over the selected pages (informational).
--text-width: with it, also fails if any page's text spans wider than that many cm (needs margin-symmetric layout).
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_common import Report, front_arg, need_file, parse_range, pdf_bbox

CM = 28.3465


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--min-margin", type=float, default=2.5)
    ap.add_argument("--pages", default="")
    ap.add_argument("--skip", default="", help="PDF pages to skip, e.g. 1 (cover)")
    ap.add_argument("--text-width", type=float, default=0.0)
    front_arg(ap)
    a = ap.parse_args()
    need_file(a.pdf, "PDF")
    rep = Report("typeset", "bbox_margin.py")

    pages = pdf_bbox(a.pdf)
    only = parse_range(a.pages)
    skip = parse_range(a.skip)
    lim = a.min_margin * CM - 0.5
    left = right = top = bottom = None
    for i, pg in enumerate(pages):
        p = i + 1
        if (only and p not in only) or p in skip or not pg["words"]:
            continue
        W, H = pg["width"], pg["height"]
        xmin = min(w[0] for w in pg["words"])
        xmax = max(w[2] for w in pg["words"])
        ymin = min(w[1] for w in pg["words"])
        ymax = max(w[3] for w in pg["words"])
        left = xmin if left is None else min(left, xmin)
        right = (W - xmax) if right is None else min(right, W - xmax)
        top = ymin if top is None else min(top, ymin)
        bottom = (H - ymax) if bottom is None else min(bottom, H - ymax)
        out = [w for w in pg["words"] if w[0] < lim or (W - w[2]) < lim]
        rep.check("L9", not out, sev="major", where=rep.where(page=p, front=a.front),
                  what="%d word(s) closer than %.1f cm to the left/right page edge (text outside the margin)" % (len(out), a.min_margin),
                  evidence="; ".join("%r x=%.1f..%.1f (%.2f cm left, %.2f cm right)" % (w[4][:20], w[0], w[2], w[0] / CM, (W - w[2]) / CM) for w in out[:5]),
                  recurring="yes", owner="fix-se (CLS) unless one-off content", places=["PDF page %d" % p])
        if a.text_width:
            span = (xmax - xmin) / CM
            rep.check("K1", span <= a.text_width + 0.02, sev="major", where=rep.where(page=p, front=a.front),
                      what="text spans %.2f cm, wider than the text block %.2f cm" % (span, a.text_width), owner="fix-se")
    if left is not None:
        rep.note("measured minimum margins over the selected pages: left %.2f cm, right %.2f cm, top %.2f cm, bottom %.2f cm"
                 % (left / CM, right / CM, top / CM, bottom / CM))
    else:
        rep.skip("L9", "no pages with text selected")
    sys.exit(rep.emit())


if __name__ == "__main__":
    main()
