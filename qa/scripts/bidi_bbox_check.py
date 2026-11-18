"""bidi_bbox_check.py: qa-BiDi. Machine check of the Hebrew page test corpus (criteria B3, B4, B11).

Usage: python qa/scripts/bidi_bbox_check.py main.pdf [--page N] [--runs qa/scripts/bidi_runs.txt] [--dump]

Reads the words of the Hebrew page with `pdftotext -bbox` and checks
  - each required Latin/number run is present AS WRITTEN (whole word, punctuation stripped)   [B11, B3]
  - none of its reverses is present ("niwTtesolC", "6202", ...)                              [B3]
  - the page holds >= 5 numbers with a unit (%, $, USD, ILS, years), >= 1 parenthesis,
    >= 1 Latin run ending a sentence                                                         [B11, B4]
  - no digit/percent order error such as "%30"                                                [B3]
--dump prints the page in right-to-left line order, for the by-eye check of B2-B4.
This is a machine check only. B2-B6 are still 'verified by eye' from the rendered PNG.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_common import (HEBREW, Report, need_file, pdf_bbox, pdf_texts, read_text)

DEFAULT_RUNS = [("ClosetTwin", ["niwTtesolC"]), ("TAM", ["MAT"]), ("SAM", ["MAS"]), ("SOM", ["MOS"]),
                ("B2B", []), ("AI", ["IA"]), ("2026", ["6202"])]
STRIP = " \t.,;:!?()[]{}\"'“”‘’״׳"


def load_runs(path):
    if not path or not os.path.isfile(path):
        return DEFAULT_RUNS, "built-in list"
    runs = []
    for line in read_text(path).splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        left, _, right = line.partition("|")
        runs.append((left.strip(), [r.strip() for r in right.split(",") if r.strip()]))
    return runs, path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--page", type=int, help="PDF page of the Hebrew summary (default: first page with >= 30 Hebrew letters)")
    ap.add_argument("--runs", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "bidi_runs.txt"))
    ap.add_argument("--dump", action="store_true")
    ap.add_argument("--min-numbers", type=int, default=5)
    a = ap.parse_args()
    need_file(a.pdf, "PDF")
    rep = Report("bidi", "bidi_bbox_check.py")

    page = a.page
    if not page:
        for i, t in enumerate(pdf_texts(a.pdf)):
            if len(HEBREW.findall(t)) >= 30:
                page = i + 1
                break
    if not page:
        rep.add("blocker", "B11", rep.where(), "no Hebrew page found (no page with >= 30 Hebrew letters)", owner="writer-se")
        sys.exit(rep.emit())

    words = pdf_bbox(a.pdf)[page - 1]["words"]
    tokens = [w[4] for w in words]
    stripped = [t.strip(STRIP) for t in tokens]
    where = rep.where(page=page)
    runs, src = load_runs(a.runs)
    rep.note("Hebrew page = PDF page %d; %d words; runs from %s" % (page, len(words), src))

    # required runs and their reverses
    for run, reverses in runs:
        found = any(s == run for s in stripped)
        rep.check("B11", found, sev="blocker", where=where,
                  what="required Latin/number run '%s' is not on the Hebrew page as written" % run,
                  evidence="words seen: %s" % " ".join(t for t in tokens if re.search(r"[A-Za-z0-9]", t))[:200],
                  owner="writer-se")
        for rv in reverses:
            if rv == run:
                continue
            bad = any(s == rv for s in stripped)
            rep.check("B3", not bad, sev="blocker", where=where,
                      what="reversed run '%s' found (should read '%s'): Latin/number text is reversed inside Hebrew" % (rv, run),
                      evidence="word list contains %r" % rv, recurring="yes", owner="fix-se",
                      places=["Hebrew page %d" % page])

    # digit/percent order errors
    wrong = [t for t in tokens if re.match(r"^%\d", t) or re.match(r"^\d+[.,]?\d*\$$", t)]
    rep.check("B3", not wrong, sev="blocker", where=where,
              what="number/unit order error (a unit before its digits, e.g. '%30'): digits and symbols are reordered",
              evidence="tokens: %s" % " ".join(wrong), recurring="yes", owner="fix-se", places=["Hebrew page %d" % page])

    # B11 corpus: numbers with a unit
    unit_words = {"USD", "ILS", "years", "year", "$", "%", "₪", "M", "B"}
    n_units = 0
    for i, t in enumerate(tokens):
        if re.search(r"\d", t) and (re.search(r"[%$₪]", t) or (i + 1 < len(tokens) and tokens[i + 1].strip(STRIP) in unit_words)
                                    or (i and tokens[i - 1].strip(STRIP) in {"USD", "ILS", "$"})):
            n_units += 1
    rep.check("B11", n_units >= a.min_numbers, sev="blocker", where=where,
              what="the Hebrew page has %d number(s) with a unit, the test corpus needs >= %d" % (n_units, a.min_numbers),
              evidence="counted tokens with a digit and %, $, USD, ILS, years", owner="writer-se")
    n_par = sum(1 for t in tokens if "(" in t or ")" in t)
    rep.check("B4", n_par >= 1, sev="major", where=where,
              what="no parenthesis on the Hebrew page: the boundary test (B4/B11) needs >= 1", owner="writer-se")
    ends = [t for t in tokens if re.search(r"[A-Za-z0-9]", t) and re.search(r"[.!?]$", t)]
    rep.check("B4", len(ends) >= 1, sev="major", where=where,
              what="no Latin run ending a sentence on the Hebrew page: the B11 corpus needs >= 1",
              owner="writer-se")

    if a.dump:
        # right-to-left reading order: group by line (yMin), right edge first
        lines = {}
        for x0, y0, x1, y1, t in words:
            lines.setdefault(round(y0 / 3), []).append((x1, t))
        rep.note("reading order, line by line, right to left; Latin/number runs are shown left to right as they read (approximate, for the by-eye check):")
        for key in sorted(lines):
            toks = [t for _, t in sorted(lines[key], reverse=True)]
            out, run = [], []
            for t in toks + [None]:
                if t is not None and re.search(r"[A-Za-z0-9%$]", t) and not HEBREW.search(t):
                    run.append(t)
                else:
                    out += run[::-1]
                    run = []
                    if t is not None:
                        out.append(t)
            rep.note("  " + " ".join(out))
    sys.exit(rep.emit())


if __name__ == "__main__":
    main()
