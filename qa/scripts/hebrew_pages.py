"""hebrew_pages.py: qa-BiDi. Where is Hebrew in the PDF?  (criteria B1, B6, B8, B9, C4)

Usage: python qa/scripts/hebrew_pages.py main.pdf [--log main.log] [--front 3] [--exceptions 7,9] [--min-letters 30]

Checks
  B1  exactly one Hebrew page (>= --min-letters Hebrew letters); with --front, it must be a front-matter page
  B8  no Hebrew letters on any other page (except --exceptions)
  B6  the Hebrew page uses no Playfair Display (Hebrew headings must be Rubik)
  B9  the log has no 'Missing character' line and no '!' error line (needs --log)
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_common import (HEBREW, Report, front_arg, need_file, parse_range, pdf_fonts, pdf_texts, read_text)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--log")
    ap.add_argument("--exceptions", default="", help="PDF pages allowed to hold a little Hebrew, e.g. 12,13")
    ap.add_argument("--min-letters", type=int, default=30, help="Hebrew letters that make a page a 'Hebrew page'")
    front_arg(ap)
    a = ap.parse_args()
    need_file(a.pdf, "PDF")

    rep = Report("bidi", "hebrew_pages.py")
    texts = pdf_texts(a.pdf)
    counts = [len(HEBREW.findall(t)) for t in texts]
    exc = parse_range(a.exceptions)
    hebrew_pages = [i + 1 for i, c in enumerate(counts) if c >= a.min_letters and (i + 1) not in exc]
    rep.note("Hebrew letters per page: %s" % ", ".join("p%d=%d" % (i + 1, c) for i, c in enumerate(counts) if c))
    rep.note("Hebrew pages (>= %d letters): %s" % (a.min_letters, hebrew_pages or "none"))

    # B1: exactly one Hebrew page
    rep.check("B1", len(hebrew_pages) == 1, sev="blocker",
              where=rep.where(page=hebrew_pages[0] if hebrew_pages else None, front=a.front),
              what="expected exactly 1 Hebrew executive-summary page, found %d" % len(hebrew_pages),
              evidence="pages with >= %d Hebrew letters: %s" % (a.min_letters, hebrew_pages), owner="writer-se")
    if len(hebrew_pages) == 1:
        h = hebrew_pages[0]
        if a.front:
            rep.check("B1", h <= a.front, sev="blocker", where=rep.where(page=h, front=a.front),
                      what="the Hebrew page must be in the front matter (PRD Q-3), it is page %d but front matter ends at %d" % (h, a.front),
                      owner="master-se")
        else:
            rep.skip("B1-front", "--front not given: cannot tell whether the Hebrew page is front matter")
        # B6: no Playfair on the Hebrew page
        fonts = [f["name"] for f in pdf_fonts(a.pdf, h)]
        bad = [n for n in fonts if n.startswith("PlayfairDisplay")]
        rep.note("fonts on the Hebrew page %d: %s" % (h, ", ".join(sorted(set(fonts)))))
        rep.check("B6", not bad, sev="major", where=rep.where(page=h, front=a.front),
                  what="Playfair Display is embedded on the Hebrew page; Hebrew text and headings must be Rubik "
                       "(Playfair has no Hebrew glyphs; a Latin heading word is allowed, so confirm by eye)",
                  evidence="fonts: %s" % ", ".join(sorted(set(fonts))), recurring="yes",
                  owner="fix-se", places=["Hebrew page %d" % h])

    # B8: Hebrew elsewhere
    stray = [(i + 1, c) for i, c in enumerate(counts) if c and (i + 1) not in hebrew_pages and (i + 1) not in exc]
    rep.check("B8", not stray, sev="major", where=rep.where(page=stray[0][0] if stray else None, front=a.front),
              what="Hebrew letters outside the Hebrew page",
              evidence="; ".join("page %d: %d letters" % s for s in stray), recurring="yes" if len(stray) > 1 else "no",
              owner="writer-se", places=["page %d" % s[0] for s in stray])

    # B9: missing glyphs and errors in the log
    if a.log:
        need_file(a.log, "log")
        log = read_text(a.log)
        missing = re.findall(r"^Missing character:.*$", log, re.M)
        errors = re.findall(r"^!.*$", log, re.M)
        rep.check("B9", not missing, sev="blocker", where=rep.where(file=a.log),
                  what="%d 'Missing character' line(s): a glyph is absent from the font in use" % len(missing),
                  evidence="\n".join(sorted(set(m[:110] for m in missing))[:8]), recurring="yes", owner="fix-se",
                  places=["%d lines in %s" % (len(missing), a.log)])
        rep.check("B9-errors", not errors, sev="blocker", where=rep.where(file=a.log),
                  what="%d TeX error line(s) starting with '!'" % len(errors),
                  evidence="\n".join(errors[:6]), owner="master-se")
    else:
        rep.skip("B9", "--log not given")
    sys.exit(rep.emit())


if __name__ == "__main__":
    main()
