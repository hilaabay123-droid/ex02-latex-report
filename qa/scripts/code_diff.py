"""code_diff.py: qa-code. Does the pythonbox in the PDF show the real script? (K4, R-25)

Usage: python qa/scripts/code_diff.py main.pdf --page 41 python/fig_f6_retailer_economics.py [--front K]
       python qa/scripts/code_diff.py extracted.txt python/fig_f6_retailer_economics.py

The first argument is a PDF (with --page) or a text file already extracted with `pdftotext -layout`.
Line numbers at the start of a line are removed, white space is normalised. The code box shows one contiguous
range of the script: the longest matching block of lines is located and every PDF line inside that block's span
that is not in the file is a finding (a changed or pasted line). A line that is only a piece of a longer source
line is accepted as a wrapped line. Fewer than 3 matching lines = the box does not show this file.
"""
import argparse
import difflib
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_common import Report, front_arg, need_file, pdf_texts, read_text


def norm(line):
    return re.sub(r"\s+", " ", line.strip())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="PDF or extracted text of the code page")
    ap.add_argument("script", nargs="?", help="python/<file>.py; with a PDF first argument, give --page")
    ap.add_argument("--page", type=int)
    front_arg(ap)
    a = ap.parse_args()
    rep = Report("code", "code_diff.py")
    script = a.script
    need_file(a.source, "source")
    need_file(script, "script")

    if a.source.lower().endswith(".pdf"):
        if not a.page:
            print("BLOCKED: --page is required with a PDF")
            sys.exit(2)
        text = pdf_texts(a.source)[a.page - 1]
        where = rep.where(page=a.page, front=a.front)
    else:
        text = read_text(a.source)
        where = rep.where(file=a.source)

    pdf_lines = []
    for raw in text.splitlines():
        l = re.sub(r"^\s*\d{1,4}\s{1,}", "", raw)   # strip line numbers
        l = norm(l)
        if l:
            pdf_lines.append(l)
    src_lines = [norm(l) for l in read_text(script).splitlines() if norm(l)]

    sm = difflib.SequenceMatcher(None, pdf_lines, src_lines, autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size > 0]
    matched = sum(b.size for b in blocks)
    rep.check("K4", matched >= 3, sev="blocker", where=where,
              what="the code box does not show %s (only %d line(s) match)" % (script, matched),
              evidence="first PDF lines: %s" % " / ".join(pdf_lines[:3]), owner="fix-se (pythonbox must read the file) / art-se")
    if matched >= 3:
        first = min(b.a for b in blocks if b.size >= 2) if any(b.size >= 2 for b in blocks) else blocks[0].a
        last = max(b.a + b.size for b in blocks if b.size >= 2) if any(b.size >= 2 for b in blocks) else blocks[-1].a + blocks[-1].size
        inside = set()
        for b in blocks:
            inside.update(range(b.a, b.a + b.size))
        bad = []
        for i in range(first, last):
            if i in inside:
                continue
            l = pdf_lines[i]
            if any(l in s for s in src_lines):   # wrapped piece of a longer line
                continue
            bad.append((i, l))
        rep.check("K4", not bad, sev="blocker", where=where,
                  what="%d line(s) in the code box differ from %s (changed or pasted code)" % (len(bad), script),
                  evidence="\n".join("pdf line %d: %s" % (i + 1, l[:90]) for i, l in bad[:8]),
                  owner="fix-se (pythonbox) / art-se")
        rep.note("box shows source lines ~%d..%d of %s (%d matching lines)"
                 % (min(sm_i.b for sm_i in blocks) + 1, max(sm_i.b + sm_i.size for sm_i in blocks), script, matched))
    sys.exit(rep.emit())


if __name__ == "__main__":
    main()
