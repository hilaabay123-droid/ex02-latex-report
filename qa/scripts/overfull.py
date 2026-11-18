"""overfull.py: qa-typeset / qa-table. TeX log checker (criteria BU2-BU8, BU5, BU6, TB3, L9).

Usage: python qa/scripts/overfull.py main.log [--max 1.0] [--front K] [--underfull-min 10000]

Fails on: Overfull \\hbox/\\vbox wider than --max pt (default 1.0, the project rule; the book says 5),
          '!' error lines (BU2), 'undefined' references/citations (BU3/BU4), 'Missing character' (BU7),
          'Rerun to get cross-references right' on the last pass (BU8), unplaceable floats.
Reports Underfull boxes with badness >= --underfull-min as minor (BU6).
Page numbers are estimated from the [n] ship-out marks in the log ("page ~n"); confirm in the PDF.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_common import Report, front_arg, need_file, read_text

SHIP = re.compile(r"\[(\d+)(?:\{[^}\n]*\})?(?:<[^>\n]*>)*\]")
FILE_OPEN = re.compile(r"\(((?:\./|\.\./)?[\w./\\-]+\.(?:tex|cls|sty|bbl))")


def scan(log):
    """Yield (kind, amount, line_no, page, file, snippet) for every Overfull/Underfull box."""
    lines = log.splitlines()
    page = 1
    cur_file = "?"
    out = []
    for i, line in enumerate(lines):
        for m in FILE_OPEN.finditer(line):
            cur_file = m.group(1)
        for m in SHIP.finditer(line):
            page = max(page, int(m.group(1)) + 1)
        m = re.match(r"^(Overfull|Underfull) \\([hv]box) \((?:([\d.]+)pt too (?:wide|high)|badness (\d+))\)(.*)$", line)
        if m:
            amount = float(m.group(3)) if m.group(3) else float(m.group(4))
            snippet = " ".join(l.strip() for l in lines[i + 1:i + 3])[:100]
            out.append((m.group(1), m.group(2), amount, i + 1, page, cur_file, m.group(5).strip(), snippet))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("log")
    ap.add_argument("--max", type=float, default=1.0)
    ap.add_argument("--underfull-min", type=float, default=10000)
    front_arg(ap)
    a = ap.parse_args()
    need_file(a.log, "log")
    log = read_text(a.log)
    rep = Report("typeset", "overfull.py")

    boxes = scan(log)
    over = [b for b in boxes if b[0] == "Overfull"]
    bad = [b for b in over if b[2] > a.max]
    rep.note("Overfull boxes: %d (over %.1f pt: %d); Underfull boxes: %d"
             % (len(over), a.max, len(bad), len([b for b in boxes if b[0] == "Underfull"])))
    for b in over:
        rep.note("overfull %s %.2fpt  %s:log line %d  page~%d  %s" % (b[1], b[2], b[5], b[3], b[4], b[6][:60]))
    if bad:
        rep.add("major", "BU5", rep.where(file=a.log, line=bad[0][3], page=bad[0][4], front=a.front),
                "%d overfull box(es) wider than %.1f pt (worst %.2f pt)" % (len(bad), a.max, max(b[2] for b in bad)),
                "\n".join("%s \\%sbox %.2fpt, log line %d, page~%d, in %s: %s" % (b[0], b[1], b[2], b[3], b[4], b[5], b[7][:70]) for b in bad[:8]),
                recurring="yes" if len(bad) > 1 else "no", owner="fix-se (CLS) unless one-off content",
                places=["log line %d (page~%d)" % (b[3], b[4]) for b in bad])
    else:
        rep.passed.add("BU5")

    under = [b for b in boxes if b[0] == "Underfull" and b[2] >= a.underfull_min]
    rep.check("BU6", not under, sev="minor", where=rep.where(file=a.log, line=under[0][3] if under else None,
              page=under[0][4] if under else None, front=a.front),
              what="%d underfull box(es) with badness %d (loose lines, large gaps)" % (len(under), a.underfull_min),
              evidence="\n".join("badness %d, log line %d, page~%d, %s" % (b[2], b[3], b[4], b[7][:60]) for b in under[:6]),
              recurring="yes" if len(under) > 1 else "no", owner="fix-se", places=["page~%d" % b[4] for b in under])

    errors = re.findall(r"^!.*$", log, re.M)
    rep.check("BU2", not errors, sev="blocker", where=rep.where(file=a.log),
              what="%d TeX error line(s) starting with '!'" % len(errors), evidence="\n".join(errors[:6]), owner="master-se")
    und = re.findall(r"^.*(?:Reference|Citation|reference|citation)[^\n]*undefined.*$", log, re.M)
    und += re.findall(r"^LaTeX Warning: There were undefined references\.$", log, re.M)
    rep.check("BU3", not und, sev="blocker", where=rep.where(file=a.log),
              what="%d undefined reference/citation warning(s)" % len(und), evidence="\n".join(und[:6]), owner="writer-se")
    miss = re.findall(r"^Missing character:.*$", log, re.M)
    rep.check("BU7", not miss, sev="blocker", where=rep.where(file=a.log),
              what="%d 'Missing character' line(s)" % len(miss),
              evidence="\n".join(sorted(set(m[:110] for m in miss))[:6]), recurring="yes", owner="fix-se",
              places=["%d lines" % len(miss)])
    rerun = re.findall(r"^.*(?:Rerun to get|Please \(re\)run).*$", log, re.M | re.I)
    rep.check("BU8", not rerun, sev="major", where=rep.where(file=a.log),
              what="the log still asks for another run (cross-references not stable)", evidence="\n".join(rerun[:3]),
              owner="master-se")
    floats = re.findall(r"^.*(?:Float too large|too many unprocessed floats|`h' float specifier changed).*$", log, re.M)
    rep.check("L3", not floats, sev="major", where=rep.where(file=a.log),
              what="%d float placement warning(s)" % len(floats), evidence="\n".join(floats[:4]), recurring="yes",
              owner="fix-se", places=["%d warnings" % len(floats)])
    sys.exit(rep.emit())


if __name__ == "__main__":
    main()
