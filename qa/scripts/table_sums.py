"""table_sums.py: qa-table. Recompute the 'Total' rows of tables (criterion TB5).

Usage: python qa/scripts/table_sums.py [chapters main.tex ...] [--tol 0.5]

In every tabular found in the .tex sources, a row whose first cell starts with Total / Sum / Subtotal is checked:
for each column, the numbers of the rows above it (back to the last \\midrule/\\hline, or the table start after
the header row) are added and compared with the number in the Total row. The tolerance is --tol units of the
last printed decimal (default 0.5, i.e. rounding). Numbers may carry \\$, \\%, commas, \\usd{..}, \\pct{..}, \\ils{..},
$..$, thin spaces or a unit suffix. Cells with no number are ignored. Tables without a Total row are not checked.
"""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_common import Report, read_text

NUM = re.compile(r"[-\u2212]?\d[\d,]*\.?\d*")


def clean(cell):
    c = re.sub(r"\\(?:usd|pct|ils|derived|assumed|sourced|textbf|textit|emph)\{([^}]*)\}", r"\1", cell)
    c = re.sub(r"\\[,;: ]|\\\$|\\%|\$|\\,|~|\{|\}", " ", c)
    return c


def to_number(cell):
    m = NUM.search(clean(cell))
    if not m:
        return None, 0
    s = m.group(0).replace(",", "").replace("\u2212", "-")
    try:
        v = float(s)
    except ValueError:
        return None, 0
    dec = len(s.split(".")[1]) if "." in s else 0
    return v, dec


def gather(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += sorted(glob.glob(os.path.join(p, "**", "*.tex"), recursive=True))
        elif os.path.isfile(p):
            files.append(p)
    return files


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", nargs="*")
    ap.add_argument("--tol", type=float, default=0.5)
    a = ap.parse_args()
    src = a.src or [p for p in ("chapters", "main.tex") if os.path.exists(p)]
    rep = Report("table", "table_sums.py")
    ntab = ntotal = 0
    for f in gather(src):
        text = "\n".join(re.sub(r"(?<!\\)%.*$", "", l) for l in read_text(f).splitlines())
        for m in re.finditer(r"\\begin\{(tabular\*?|tabularx|longtable|tabulary)\}(?:\{[^}]*\})?(?:\{[^}]*\})?(.*?)\\end\{\1\}", text, re.S):
            ntab += 1
            body = m.group(2)
            base_line = text.count("\n", 0, m.start()) + 1
            rows = []
            for chunk in re.split(r"\\\\(?:\[[^\]]*\])?", body):
                rule = bool(re.search(r"\\(midrule|hline|bottomrule)", chunk))
                chunk = re.sub(r"\\(toprule|midrule|bottomrule|hline|cmidrule(\([^)]*\))?\{[^}]*\}|addlinespace(\[[^\]]*\])?)", "", chunk)
                cells = [c.strip() for c in chunk.split("&")]
                if any(cells):
                    rows.append((rule, cells))
            start = 1  # skip header row
            for ri, (rule, cells) in enumerate(rows):
                first = clean(cells[0]).strip().lower()
                if rule and not re.match(r"^(sub)?total\b|^sum\b", first):
                    start = ri
                if re.match(r"^(sub)?total\b|^sum\b", first):
                    ntotal += 1
                    for ci in range(1, len(cells)):
                        tv, dec = to_number(cells[ci])
                        if tv is None:
                            continue
                        vals = [to_number(r[1][ci])[0] for r in rows[start:ri] if ci < len(r[1]) and to_number(r[1][ci])[0] is not None]
                        if not vals:
                            continue
                        s = sum(vals)
                        ok = abs(s - tv) <= a.tol * (10 ** -dec)
                        rep.check("TB5", ok, sev="major", where=rep.where(file=f, line=base_line + 1),
                                  what="Total row, column %d: the rows above add up to %s but the table prints %s" % (ci + 1, ("%.*f" % (dec, s)), cells[ci]),
                                  evidence="added %d value(s): %s" % (len(vals), ", ".join(str(v) for v in vals[:8])), owner="writer-se")
    rep.note("%d tabular environment(s) scanned, %d Total row(s) checked" % (ntab, ntotal))
    if not ntotal:
        rep.skip("TB5", "no 'Total' rows found (nothing to recompute)")
    sys.exit(rep.emit())


if __name__ == "__main__":
    main()
