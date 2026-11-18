"""bib_vs_cited.py: qa-infra. Bibliography mechanics (R1, R2, R3, R4, R6, R11).

Usage: python qa/scripts/bib_vs_cited.py main.bcf references.bib [--pdf main.pdf] [--min 12] [--cls closettwin.cls]

R1   every cited key exists in the .bib (cited keys come from the biber control file main.bcf)
R11  every .bib key is cited at least once (no unused entry); every @online/@misc-with-url entry has urldate
R6   completeness: author or editor (or organization), title, year/date, a venue (journal/booktitle/publisher/
     institution/organization/eprint/url), a DOI or URL; articles and conference papers also pages or an article number
R4   at least --min distinct cited entries
R2   --pdf: no citation printed as a key ("[Segal2026]" instead of "[3]") in the PDF text
R3   --cls: the class loads biblatex with style=ieee
Resolving the DOI/URLs and matching titles to the real sources is a separate (manual, network) step of qa-infra/qa-super.
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_common import Report, need_file, pdf_texts, read_text


def parse_bib(text):
    """{key: {'type': t, 'fields': {name: value}}} with a tolerant brace parser."""
    entries = {}
    i = 0
    while True:
        m = re.search(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text[i:])
        if not m:
            break
        typ, key = m.group(1).lower(), m.group(2)
        start = i + m.end()
        depth, j = 1, start
        while j < len(text) and depth:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        body = text[start:j - 1]
        i = j
        if typ in ("comment", "string", "preamble"):
            continue
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*", body):
            k = fm.group(1).lower()
            pos = fm.end()
            if pos >= len(body):
                continue
            if body[pos] == "{":
                d, q = 1, pos + 1
                while q < len(body) and d:
                    d += (body[q] == "{") - (body[q] == "}")
                    q += 1
                val = body[pos + 1:q - 1]
            elif body[pos] == '"':
                q = body.find('"', pos + 1)
                val = body[pos + 1:q]
            else:
                val = re.match(r"[^,\n]*", body[pos:]).group(0)
            fields.setdefault(k, val.strip())
        entries[key] = {"type": typ, "fields": fields}
    return entries


def cited_keys(bcf):
    keys = re.findall(r"<bcf:citekey[^>]*>([^<]+)</bcf:citekey>", bcf)
    return list(dict.fromkeys(k.strip() for k in keys))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bcf")
    ap.add_argument("bib")
    ap.add_argument("--pdf")
    ap.add_argument("--cls")
    ap.add_argument("--min", type=int, default=12)
    a = ap.parse_args()
    need_file(a.bcf, "bcf")
    need_file(a.bib, "bib")
    rep = Report("infra", "bib_vs_cited.py")

    bib = parse_bib(read_text(a.bib))
    cites = cited_keys(read_text(a.bcf))
    star = "*" in cites
    cites = [c for c in cites if c != "*"]
    rep.note("%d entries in %s, %d distinct cited keys in %s%s" % (len(bib), a.bib, len(cites), a.bcf, " (+ \\nocite{*})" if star else ""))

    missing = [k for k in cites if k not in bib]
    rep.check("R1", not missing, sev="blocker", where=rep.where(file=a.bcf),
              what="%d cited key(s) are not in the .bib" % len(missing), evidence=", ".join(missing[:15]), owner="writer-se")
    unused = [k for k in bib if k not in cites] if not star else []
    rep.check("R11", not unused, sev="major", where=rep.where(file=a.bib),
              what="%d .bib entr%s never cited (no unused entry allowed)" % (len(unused), "y is" if len(unused) == 1 else "ies are"),
              evidence=", ".join(unused[:20]), owner="writer-se")
    rep.check("R4", len([k for k in cites if k in bib]) >= a.min, sev="major", where=rep.where(file=a.bib),
              what="%d distinct cited entries, at least %d needed" % (len([k for k in cites if k in bib]), a.min), owner="writer-se")

    for key, e in bib.items():
        f, t = e["fields"], e["type"]
        gaps = []
        if not (f.get("author") or f.get("editor") or f.get("organization") or f.get("institution")):
            gaps.append("author/editor/organization")
        if not f.get("title"):
            gaps.append("title")
        if not (f.get("year") or f.get("date")):
            gaps.append("year/date")
        if not any(f.get(x) for x in ("journal", "journaltitle", "booktitle", "publisher", "institution", "organization", "eprint", "url", "howpublished", "type")):
            gaps.append("venue/publisher")
        if not (f.get("doi") or f.get("url") or f.get("eprint")):
            gaps.append("doi or url")
        if t in ("article", "inproceedings", "conference") and not any(f.get(x) for x in ("pages", "eid", "articleno", "number", "article-number")):
            gaps.append("pages or article number")
        if gaps:
            rep.add("major", "R6", rep.where(file=a.bib), "entry '%s' (%s) is incomplete: missing %s" % (key, t, ", ".join(gaps)),
                    "fields present: %s" % ", ".join(sorted(f)), owner="writer-se")
        else:
            rep.passed.add("R6")
        if f.get("url") and not f.get("urldate") and t in ("online", "misc", "electronic", "www", "report", "techreport"):
            rep.add("major", "R11", rep.where(file=a.bib), "web entry '%s' has a url but no urldate (IEEE needs 'Accessed:')" % key,
                    "url = %s" % f["url"][:70], owner="writer-se")

    if a.pdf:
        need_file(a.pdf, "PDF")
        bad = []
        for p, t in enumerate(pdf_texts(a.pdf, layout=False), 1):
            for m in re.finditer(r"\[[A-Za-z][A-Za-z0-9_:-]{3,}\]", t):
                bad.append("p%d %s" % (p, m.group(0)))
        rep.check("R2", not bad, sev="major", where=rep.where(file=a.pdf), what="%d citation(s) printed as a key instead of a number" % len(bad),
                  evidence=", ".join(bad[:10]), recurring="yes", owner="fix-se (biblatex style)", places=bad[:10])
    if a.cls:
        need_file(a.cls, "cls")
        c = read_text(a.cls)
        rep.check("R3", bool(re.search(r"style\s*=\s*ieee", c)), sev="major", where=rep.where(file=a.cls),
                  what="the class does not load biblatex with style=ieee", recurring="yes", owner="fix-se")
    sys.exit(rep.emit())


if __name__ == "__main__":
    main()
