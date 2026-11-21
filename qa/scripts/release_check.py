"""qa-se release check (prompt 07 part 3). Detector only; never edits the repo.

Usage (from the project root):  python -I qa/scripts/release_check.py [--clone DIR] [--no-build] [--history]
Checks: (1) fresh clone of HEAD builds with the 4 commands, same page count as main.pdf;
(2) required files tracked; (3) .gitignore coverage and tracked junk, gitlinks;
(4) emails / tokens / passwords / ID-like numbers in tracked files and (with --history) in all history;
(5) README.md relative links and images resolve to tracked files with exact case.
Secrets are never printed in full (masked).
"""
import argparse, os, re, subprocess, sys, shutil

ALLOW_NUM = {"875523402"}            # course number (allowed)
ALLOW_TEXT = ("sg00ha11",)          # group code (allowed)
REQUIRED = ["main.tex", "closettwin.cls", "references.bib", "PRD.md", "PLAN.md", "TODO.md", "README.md", "main.pdf"]
REQ_DIRS = ["chapters/", "prompts/", ".claude/skills/", "python/", "figures/", "fonts/"]
JUNK_RE = re.compile(r"\.(aux|log|bbl|bcf|blg|toc|lof|lot|out|synctex\.gz|fls|fdb_latexmk)$|\.run\.xml$|__pycache__|(^|/)\.DS_Store$|Thumbs\.db$")
JUNK_DIRS = ("qa/tmp/", "qa/build/", "qa/b4out", "fix/bld/", "art/test/", "writer/tmp/", "ref/")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}")
TOKEN = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
PASSW = re.compile(r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|token)\b\s*[:=]\s*['\"]?[^\s'\"<>]{6,}")
NINE = re.compile(r"(?<![\d.,/-])(\d{9})(?![\d.,-])")


def run(*a, cwd=None, check=False):
    return subprocess.run(a, cwd=cwd, capture_output=True, text=True, encoding="utf8", errors="replace")


def mask(s):
    return s[:2] + "*" * max(len(s) - 4, 1) + s[-2:] if len(s) > 4 else "****"


def scan_line(line):
    out = []
    for m in EMAIL.finditer(line):
        out.append(("email", mask(m.group(0).split("@")[0]) + "@" + m.group(0).split("@")[1]))
    for m in TOKEN.finditer(line):
        out.append(("token", mask(m.group(0))))
    for m in PASSW.finditer(line):
        out.append(("password-like", line[max(0, m.start()):m.start() + 12] + "..."))
    for m in NINE.finditer(line):
        if m.group(1) not in ALLOW_NUM:
            out.append(("9-digit", mask(m.group(1))))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone", default="qa/tmp/rel")
    ap.add_argument("--no-build", action="store_true")
    ap.add_argument("--history", action="store_true")
    a = ap.parse_args()
    F = []
    def f(sev, crit, msg): F.append((sev, crit, msg)); print(f"[{sev}] {crit}: {msg}")

    head = run("git", "rev-parse", "--short", "HEAD").stdout.strip()
    dirty = run("git", "status", "--porcelain", "--untracked-files=no").stdout.strip()
    print("HEAD", head, "| tracked changes:", len(dirty.splitlines()))
    if dirty:
        print("NOTE: tracked files modified in the working tree:\n" + "\n".join(dirty.splitlines()[:15]))
    files = run("git", "ls-files").stdout.splitlines()
    fset = set(files)
    lower = {}
    for p in files: lower.setdefault(p.lower(), []).append(p)

    # (2) required files
    for r in REQUIRED:
        if r not in fset: f("major", "REL2", f"required file not tracked: {r}")
    for d in REQ_DIRS:
        if not any(p.startswith(d) for p in files): f("major", "REL2", f"required folder has no tracked file: {d}")
    if not any(p.startswith("chapters/") and p.endswith(".tex") for p in files): f("major", "REL2", "no chapters/*.tex tracked")
    print("REL2 required files: checked")

    # (3) ignore / junk / gitlinks
    gl = [l.split("\t")[1] for l in run("git", "ls-files", "-s").stdout.splitlines() if l.startswith("160000")]
    for g in gl: f("major", "REL3", f"gitlink (nested repo, mode 160000) tracked: {g}  -> `git rm --cached {g}` and add to .gitignore")
    junk = [p for p in files if JUNK_RE.search(p) or p.startswith(JUNK_DIRS)]
    if junk:
        by = {}
        for p in junk: by.setdefault("/".join(p.split("/")[:2]), []).append(p)
        f("major", "REL3", f"{len(junk)} junk/temp files tracked: " + ", ".join(f"{k} ({len(v)})" for k, v in sorted(by.items())))
    ign = open(".gitignore", encoding="utf8").read() if os.path.exists(".gitignore") else ""
    for need in ["ref/", "*.aux", "*.log", "*.bbl", "*.bcf", "*.blg", "*.run.xml", "*.toc", "*.lof", "*.lot", "*.out", "qa/tmp", "fix/bld", "art/test"]:
        if need not in ign: f("minor", "REL3", f".gitignore has no entry for {need}")
    big = [(os.path.getsize(p), p) for p in files if os.path.exists(p) and os.path.getsize(p) > 5_000_000]
    for s, p in big: f("minor", "REL3", f"large tracked file {p}: {s/1e6:.1f} MB")

    # (4) secrets in tracked files (working tree copy of tracked files)
    hits = {}
    for p in files:
        if not os.path.isfile(p): continue
        try: data = open(p, "rb").read()
        except OSError: continue
        if b"\0" in data[:4096]: continue
        for i, line in enumerate(data.decode("utf8", "replace").splitlines(), 1):
            if any(t in line for t in ALLOW_TEXT) and not NINE.search(line) and not EMAIL.search(line): continue
            for kind, m in scan_line(line):
                hits.setdefault((p, kind), []).append((i, m))
    for (p, kind), v in sorted(hits.items()):
        f("major" if kind in ("token", "password-like") else "minor", "REL4", f"{kind} in tracked file {p}: {len(v)} hit(s), e.g. line {v[0][0]} {v[0][1]}")
    print("REL4 tracked files scanned:", len(files))
    if a.history:
        p = subprocess.Popen(["git", "log", "-p", "--all", "--no-color", "--format=commit %h"], stdout=subprocess.PIPE, text=True, encoding="utf8", errors="replace")
        cur, seen, cnt, fn = "", set(), 0, ""
        for line in p.stdout:
            if line.startswith("commit "): cur = line.split()[1]; continue
            if line.startswith("+++ "): fn = line[6:].strip(); continue
            if not line.startswith("+") or line.startswith("+++"): continue
            if any(t in line for t in ALLOW_TEXT) and not NINE.search(line) and not EMAIL.search(line): continue
            for kind, m in scan_line(line):
                k = (kind, m, fn)
                if k not in seen:
                    seen.add(k); cnt += 1
                    if cnt <= 60: print(f"  history {kind} {m} in {fn} (first seen in commit {cur})")
        if cnt: f("major", "REL4-history", f"{cnt} distinct hits in added lines of history (see list above; masked)")
        else: print("REL4 history: clean")

    # (5) README links
    if os.path.exists("README.md"):
        txt = open("README.md", encoding="utf8").read()
        links = re.findall(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", txt) + re.findall(r'(?:src|href)="([^"]+)"', txt)
        n = 0
        for l in links:
            if re.match(r"^(https?:|mailto:|#)", l): continue
            n += 1
            path = re.sub(r"[#?].*$", "", l)
            from urllib.parse import unquote
            path = unquote(path).lstrip("./") if path.startswith("./") else unquote(path)
            if path.startswith("/"): path = path[1:]
            if path.endswith("/"):
                ok = any(p.startswith(path) for p in files)
                if not ok: f("major", "REL5", f"README link to folder with no tracked file: {l}")
                continue
            if path in fset: continue
            if path.lower() in lower: f("major", "REL5", f"README link differs in case: {l}  (tracked as {lower[path.lower()][0]})")
            else: f("major", "REL5", f"README link target not tracked: {l}")
        print("REL5 relative links checked:", n)
    # (1) clean clone build
    if not a.no_build:
        if os.path.exists(a.clone): shutil.rmtree(a.clone, ignore_errors=True)
        r = run("git", "clone", "-q", ".", a.clone)
        if r.returncode: f("blocker", "REL1", "git clone failed: " + r.stderr[:200])
        else:
            codes = []
            for cmd in (["lualatex", "--disable-installer", "main"], ["biber", "main"], ["lualatex", "--disable-installer", "main"], ["lualatex", "--disable-installer", "main"]):
                codes.append(run(*cmd, cwd=a.clone).returncode)
            print("REL1 build exit codes:", codes)
            if any(codes): f("blocker", "REL1", f"clean clone build failed, exit codes {codes}")
            def pages(p):
                m = re.search(r"Pages:\s+(\d+)", run("pdfinfo", p).stdout); return int(m.group(1)) if m else -1
            pc, pm = pages(os.path.join(a.clone, "main.pdf")), pages("main.pdf")
            print("REL1 pages: clone", pc, "| committed main.pdf", pm)
            if pc != pm: f("major", "REL1", f"page count differs: clone {pc}, main.pdf {pm}")
            tc = run("pdftotext", "-layout", os.path.join(a.clone, "main.pdf"), "-").stdout
            tm = run("pdftotext", "-layout", "main.pdf", "-").stdout
            print("REL1 text identical:", tc == tm)
            if tc != tm: f("major", "REL1", "text of the clone PDF differs from the committed main.pdf")
            lg = open(os.path.join(a.clone, "main.log"), encoding="utf8", errors="replace").read()
            print("REL1 log: errors", len(re.findall(r"^! ", lg, re.M)), "| undefined", len(re.findall(r"undefined", lg, re.I)))
    print(f"SUMMARY release_check.py: findings={len(F)} " + ", ".join(f"{s}={sum(1 for x in F if x[0]==s)}" for s in ("blocker", "major", "minor")))


if __name__ == "__main__":
    main()
