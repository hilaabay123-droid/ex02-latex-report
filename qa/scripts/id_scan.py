"""id_scan.py: qa-infra. No personal ID number anywhere (criterion C6; PRD R-22, UD-5: the repo is public).

Usage: python qa/scripts/id_scan.py [--root .] [--pdf main.pdf] [--history] [--allow 875523402]
          [--skip-dir .git,qa/tmp,ref,__pycache__] [--ignore-line REGEX]

Scans, for a 9-digit number (\\b\\d{9}\\b) or its grouped forms (ddd-ddd-ddd, ddd ddd ddd), excluding --allow
(the course code 875523402):
  - every text file under --root           (binary files and big files are skipped)
  - the PDF text and the PDF metadata       (--pdf)
  - the git history, added lines only       (--history; needs git and a .git folder; read-only `git log -p`)
The output NEVER prints the number: only its first 2 digits and asterisks, plus file:line (or commit and file).
An ID that sits in history cannot be removed by an edit: the finding goes to master-se.
"""
import argparse
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_common import Report, mask_digits, need_file, pdf_info, pdf_texts, read_text

NINE = re.compile(r"(?<![A-Za-z0-9.])(\d{9})(?![A-Za-z0-9])")
GROUP = re.compile(r"(?<![A-Za-z0-9])(\d{3})[- ](\d{3})[- ](\d{3})(?![A-Za-z0-9])")
BINARY_EXT = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".ttf", ".otf", ".woff", ".woff2", ".zip", ".gz", ".ico", ".pyc",
              ".bin", ".exe", ".dll", ".xz", ".7z", ".mp4", ".mov",
              # LaTeX build artifacts (gitignored): font object numbers and hashes live here
              ".log", ".aux", ".bbl", ".blg", ".bcf", ".toc", ".lof", ".lot", ".out", ".xml", ".fls", ".fdb_latexmk", ".synctex"}
# Lines that legitimately hold long digit runs: URLs, DOIs, hashes, pipe/session ids. A real ID typed on such a line is missed,
# which is why --ignore-line "" (empty) disables this default.
DEFAULT_IGNORE = r"https?://|doi\s*=|doi:|sha-?256|[0-9a-f]{20,}|uds:|cc-msg-|commit [0-9a-f]{7,}|\b(?:USD|ILS|EUR|NIS)\b|[$₪€]"


def hits_in(line, allow):
    out = []
    for m in NINE.finditer(line):
        if m.group(1) not in allow:
            out.append(m.group(1))
    for m in GROUP.finditer(line):
        d = "".join(m.groups())
        if d not in allow:
            out.append(d)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".")
    ap.add_argument("--pdf")
    ap.add_argument("--history", action="store_true")
    ap.add_argument("--allow", default="875523402")
    ap.add_argument("--skip-dir", default=".git,qa/tmp,ref,__pycache__,node_modules")
    ap.add_argument("--ignore-line", default=None, help="regex; lines that match are not scanned. Default: URLs, DOIs, hashes, session ids. Pass '' to scan every line")
    a = ap.parse_args()
    allow = set(x for x in a.allow.split(",") if x)
    skip = [s.strip().replace("\\", "/").strip("/") for s in a.skip_dir.split(",") if s.strip()]
    ign_pat = DEFAULT_IGNORE if a.ignore_line is None else a.ignore_line
    ign = re.compile(ign_pat, re.I) if ign_pat else None
    rep = Report("infra", "id_scan.py")

    found = []   # (where, masked)
    nfiles = 0
    root = os.path.abspath(a.root)
    for dirpath, dirs, files in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace("\\", "/")
        dirs[:] = [d for d in dirs if d not in skip and ((rel_dir + "/" + d).lstrip("./") not in skip)]
        for fn in files:
            path = os.path.join(dirpath, fn)
            if os.path.splitext(fn)[1].lower() in BINARY_EXT or os.path.getsize(path) > 5_000_000:
                continue
            with open(path, "rb") as fh:
                head = fh.read(2048)
            if b"\x00" in head:
                continue
            nfiles += 1
            rel = os.path.relpath(path, root).replace("\\", "/")
            for n, line in enumerate(read_text(path).splitlines(), 1):
                if ign and ign.search(line):
                    continue
                for h in hits_in(line, allow):
                    found.append(("%s:%d" % (rel, n), mask_digits(h)))
    rep.note("scanned %d text file(s) under %s" % (nfiles, a.root))
    rep.check("C6", not found, sev="blocker", where=found[0][0] if found else rep.where(file=a.root),
              what="%d nine-digit (ID-like) number(s) in repository files" % len(found),
              evidence="\n".join("%s  %s" % f for f in found[:12]), owner="master-se (decides); content owner removes", recurring="no")

    if a.pdf:
        need_file(a.pdf, "PDF")
        pf = []
        for p, t in enumerate(pdf_texts(a.pdf, layout=False), 1):
            for h in hits_in(t, allow):
                pf.append(("PDF page %d" % p, mask_digits(h)))
        for line in pdf_info(a.pdf).splitlines():
            if line.split(":")[0] in ("Title", "Author", "Subject", "Keywords", "Creator", "Producer"):
                for h in hits_in(line, allow):
                    pf.append(("PDF metadata (%s)" % line.split(":")[0], mask_digits(h)))
        rep.check("C6", not pf, sev="blocker", where=pf[0][0] if pf else rep.where(file=a.pdf),
                  what="%d ID-like number(s) in the PDF text or metadata" % len(pf),
                  evidence="\n".join("%s  %s" % f for f in pf[:12]), owner="master-se")

    if a.history:
        if not os.path.isdir(os.path.join(root, ".git")):
            rep.skip("C6-history", "no .git folder under %s" % a.root)
        else:
            p = subprocess.run(["git", "-C", root, "log", "--all", "-p", "--no-color", "--format=@@COMMIT %h"],
                               capture_output=True, timeout=300)
            commit, cur_file, hh = "?", "?", []
            for line in p.stdout.decode("utf-8", errors="replace").splitlines():
                if line.startswith("@@COMMIT "):
                    commit = line.split()[1]
                elif line.startswith("+++ b/"):
                    cur_file = line[6:]
                elif line.startswith("+") and not line.startswith("+++"):
                    if ign and ign.search(line):
                        continue
                    for h in hits_in(line[1:], allow):
                        hh.append(("commit %s %s" % (commit, cur_file), mask_digits(h)))
            rep.check("C6", not hh, sev="blocker", where=hh[0][0] if hh else "",
                      what="%d ID-like number(s) in the git HISTORY (removing the file now does not remove it from the public history)" % len(hh),
                      evidence="\n".join("%s  %s" % f for f in hh[:12]), owner="master-se (history rewrite is a decision for master-se and the user)")
    else:
        rep.skip("C6-history", "--history not given")
    sys.exit(rep.emit())


if __name__ == "__main__":
    main()
