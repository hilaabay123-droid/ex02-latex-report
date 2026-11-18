"""fonts_by_page.py: qa-code / qa-BiDi / qa-super. Font whitelist per page (criteria D4, D11, K3, I8).

Usage: python qa/scripts/fonts_by_page.py main.pdf [--aux main.aux] [--front K]
          [--formula-pages 12,14] [--code-pages 31] [--figures "figures/*.pdf"]

Whitelist (PRD R-06): PlayfairDisplay*, Rubik*, LatinModernMath/LMMath* (formula pages only),
JetBrainsMono* (code-box page(s) only). Any other font, any non-embedded font, any other monospace = failure.
Formula pages come from --formula-pages (PDF pages) or from the `eq:` labels in --aux (printed pages + --front).
Code pages come from --code-pages or from `app:`/`lst:`/`code:` labels in --aux.
Figure PDFs (--figures): only Playfair/Rubik, no Type 3.
"""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_common import (Report, front_arg, need_file, parse_aux_labels, parse_range, pdf_fonts, pdf_pages)

TEXT = ("PlayfairDisplay", "Rubik")
MATH = ("LatinModernMath", "LMMath", "LatinModern-Math")
CODE = ("JetBrainsMono",)
MONO = re.compile(r"(mono|courier|consolas|typewriter|cmtt|lmmono|inconsolata|menlo|lucida ?console)", re.I)


def family(name):
    if name.startswith(TEXT):
        return "text"
    if name.startswith(MATH):
        return "math"
    if name.startswith(CODE):
        return "code"
    if MONO.search(name):
        return "other-mono"
    return "other"


def aux_pages(aux, prefixes, front):
    """PDF pages of labels with one of the prefixes (printed page + front)."""
    pages = set()
    for lab, (_, pg) in parse_aux_labels(aux).items():
        if lab.startswith(prefixes) and pg.isdigit():
            pages.add(int(pg) + front)
    return pages


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--aux")
    ap.add_argument("--formula-pages", default="")
    ap.add_argument("--code-pages", default="")
    ap.add_argument("--figures", default="", help="glob of figure PDFs, e.g. 'figures/*.pdf'")
    front_arg(ap)
    a = ap.parse_args()
    need_file(a.pdf, "PDF")
    rep = Report("code", "fonts_by_page.py")

    formula = parse_range(a.formula_pages)
    code = parse_range(a.code_pages)
    if a.aux:
        formula |= aux_pages(a.aux, ("eq:",), a.front)
        code |= aux_pages(a.aux, ("app:", "lst:", "code:"), a.front)
    have_formula = bool(a.formula_pages or a.aux)
    have_code = bool(a.code_pages or a.aux)

    n = pdf_pages(a.pdf)
    seen = {"math": [], "code": []}
    for p in range(1, n + 1):
        for f in pdf_fonts(a.pdf, p):
            fam = family(f["name"])
            where = rep.where(page=p, front=a.front)
            if fam in ("other", "other-mono"):
                rep.check("K3" if fam == "other-mono" else "D4", False, sev="blocker", where=where,
                          what="font '%s' is not on the whitelist (%s)" % (f["name"], "a monospace font" if fam == "other-mono" else "not Playfair/Rubik/LM Math/JetBrains Mono"),
                          evidence="pdffonts page %d: %s (%s)" % (p, f["name"], f["type"]), recurring="yes",
                          owner="fix-se", places=["PDF page %d" % p])
            elif not f["emb"]:
                rep.check("D4", False, sev="blocker", where=where, what="font '%s' is not embedded" % f["name"],
                          owner="fix-se", recurring="yes", places=["PDF page %d" % p])
            elif fam in seen and p not in seen[fam]:
                seen[fam].append(p)
    rep.passed.add("D4")  # D4 is reported failed above if any finding added it (check() keeps failed wins)

    rep.note("Latin Modern Math on PDF pages: %s" % (seen["math"] or "none"))
    rep.note("JetBrains Mono on PDF pages: %s" % (seen["code"] or "none"))
    if have_formula:
        stray = [p for p in seen["math"] if p not in formula]
        rep.check("D11", not stray, sev="major", where=rep.where(page=stray[0] if stray else None, front=a.front),
                  what="Latin Modern Math appears on page(s) without a formula",
                  evidence="LM Math pages %s, formula pages %s" % (seen["math"], sorted(formula)), recurring="yes",
                  owner="fix-se", places=["PDF page %d" % p for p in stray])
    else:
        rep.skip("D11", "no --formula-pages / --aux: cannot tell which pages hold a formula")
    if have_code:
        stray = [p for p in seen["code"] if p not in code]
        rep.check("K3", not stray, sev="blocker", where=rep.where(page=stray[0] if stray else None, front=a.front),
                  what="JetBrains Mono appears outside the code-box page(s)",
                  evidence="JetBrains pages %s, code pages %s" % (seen["code"], sorted(code)), recurring="yes",
                  owner="fix-se", places=["PDF page %d" % p for p in stray])
    else:
        rep.skip("K3", "no --code-pages / --aux: cannot tell which page is Appendix A")

    # figure PDFs
    for pattern in [g for g in a.figures.split(",") if g]:
        for path in sorted(glob.glob(pattern)):
            for f in pdf_fonts(path):
                fam = family(f["name"])
                ok = fam == "text" and f["emb"] and "Type 3" not in f["type"]
                rep.check("I8", ok, sev="blocker", where=rep.where(file=path),
                          what="figure font '%s' (%s%s) breaks the rule: only embedded Playfair/Rubik, no Type 3"
                               % (f["name"], f["type"], "" if f["emb"] else ", not embedded"),
                          evidence="pdffonts %s" % path, recurring="yes", owner="art-se (ct_style.py)",
                          places=[path])
    sys.exit(rep.emit())


if __name__ == "__main__":
    main()
