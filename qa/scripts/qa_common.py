"""qa_common.py: the one shared helper of the qa-se scripts (draft v0.1).

Every script in this folder imports ONLY this module. It carries: the finding block format of
qa/skill-specs.md section 0.1, the report summary/exit-code convention, thin wrappers around the
poppler tools, and a few parsers (pdftotext -bbox, TeX log/aux).

Conventions
- Run from the project root, with relative paths. No network. Python 3, standard library
  (+ numpy/PIL only where a script says so).
- Exit codes: 0 = no finding, 1 = at least one finding, 2 = usage error or BLOCKED input.
- Detector rule: nothing here writes to a deliverable. Scratch goes to the folder given by --tmp
  (default qa/tmp).
"""
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

HEBREW = re.compile("[\u0590-\u05FF]")
MIKTEX_BIN = r"C:\Program Files\MiKTeX\miktex\bin\x64"


# --------------------------------------------------------------------------- tools
def tool(name):
    """Path of a poppler tool, or None."""
    found = shutil.which(name)
    if found:
        return found
    cand = os.path.join(MIKTEX_BIN, name + ".exe")
    return cand if os.path.exists(cand) else None


def run(args, timeout=120):
    """Run a command, return (returncode, stdout). Never raises on a non-zero exit."""
    try:
        p = subprocess.run(args, capture_output=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 127, "%s: %s" % (args[0], exc)
    return p.returncode, p.stdout.decode("utf-8", errors="replace")


def need_tool(name):
    t = tool(name)
    if not t:
        blocked("tool not found: %s (poppler). Install MiKTeX or put poppler on PATH." % name)
    return t


def blocked(msg):
    print("BLOCKED: %s" % msg)
    sys.exit(2)


def need_file(path, what="file"):
    if not path or not os.path.isfile(path):
        blocked("%s not found: %s" % (what, path))
    return path


def read_text(path):
    """Read a text file, utf-8 first, then cp1255/latin-1. Never raises on bad bytes."""
    with open(path, "rb") as fh:
        raw = fh.read()
    for enc in ("utf-8-sig", "cp1255", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


# --------------------------------------------------------------------------- pdf helpers
def pdf_pages(pdf):
    """Number of pages (pdfinfo)."""
    rc, out = run([need_tool("pdfinfo"), pdf])
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    if rc != 0 or not m:
        blocked("pdfinfo failed on %s" % pdf)
    return int(m.group(1))


def pdf_info(pdf):
    rc, out = run([need_tool("pdfinfo"), pdf])
    return out


def pdf_texts(pdf, layout=True):
    """List of page texts, index 0 = PDF page 1."""
    args = [need_tool("pdftotext"), "-enc", "UTF-8"]
    if layout:
        args.append("-layout")
    args += [pdf, "-"]
    rc, out = run(args, timeout=300)
    if rc != 0:
        blocked("pdftotext failed on %s" % pdf)
    pages = out.split("\f")
    if pages and pages[-1].strip() == "":
        pages.pop()
    return pages


def pdf_bbox(pdf):
    """List per page of dict(width, height, words=[(xmin, ymin, xmax, ymax, text)])."""
    rc, out = run([need_tool("pdftotext"), "-enc", "UTF-8", "-bbox", pdf, "-"], timeout=300)
    if rc != 0:
        blocked("pdftotext -bbox failed on %s" % pdf)
    pages = []
    for chunk in out.split("<page ")[1:]:
        m = re.match(r'width="([\d.]+)" height="([\d.]+)"', chunk)
        words = []
        for w in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', chunk):
            words.append((float(w.group(1)), float(w.group(2)), float(w.group(3)), float(w.group(4)),
                          html.unescape(w.group(5))))
        pages.append({"width": float(m.group(1)), "height": float(m.group(2)), "words": words})
    return pages


def pdf_fonts(pdf, first=None, last=None):
    """Rows of dict(name, type, emb) from pdffonts. name has the subset prefix removed."""
    args = [need_tool("pdffonts")]
    if first:
        args += ["-f", str(first), "-l", str(last or first)]
    args.append(pdf)
    rc, out = run(args)
    rows = []
    for line in out.splitlines()[2:]:
        m = re.match(r"^(\S+)\s+(.+?)\s{2,}\S+\s+(yes|no)\s+(yes|no)\s+(yes|no)", line)
        if not m:
            continue
        name = re.sub(r"^[A-Z]{6}\+", "", m.group(1))
        rows.append({"name": name, "type": m.group(2).strip(), "emb": m.group(3) == "yes"})
    return rows


def render_pages(pdf, pages, dpi, outdir):
    """Render PDF pages (1-based list) to PNG, return {page: path}."""
    os.makedirs(outdir, exist_ok=True)
    res = {}
    for p in pages:
        stem = os.path.join(outdir, "pg%03d" % p)
        run([need_tool("pdftoppm"), "-r", str(dpi), "-f", str(p), "-l", str(p), "-png", "-singlefile", pdf, stem])
        if os.path.exists(stem + ".png"):
            res[p] = stem + ".png"
    return res


# --------------------------------------------------------------------------- tex helpers
def parse_aux_labels(aux_path):
    """{label: (number, printed_page)} from \\newlabel lines of an .aux file."""
    labels = {}
    if not os.path.isfile(aux_path):
        return labels
    for line in read_text(aux_path).splitlines():
        m = re.match(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{([^}]*)\}", line)
        if m:
            labels[m.group(1)] = (m.group(2), m.group(3))
    return labels


def parse_range(spec):
    """'1,3-5' -> {1,3,4,5}."""
    out = set()
    for part in (spec or "").split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            out.update(range(int(a), int(b) + 1))
        else:
            out.add(int(part))
    return out


def mask_digits(s):
    """Hide all but the first 2 digits of a digit string (reports are committed)."""
    return s[:2] + "*" * (len(s) - 2)


# --------------------------------------------------------------------------- report
class Report:
    """Collects checks and findings; prints the common finding block format."""

    def __init__(self, skill, script):
        self.skill = skill
        self.script = script
        self.findings = []
        self.passed = set()
        self.failed = set()
        self.skipped = {}
        self.notes = []

    def where(self, file=None, line=None, page=None, front=0):
        parts = []
        if file:
            parts.append("%s%s" % (file, (":%s" % line) if line else ""))
        if page:
            if front and page <= front:
                parts.append("PDF page %d (front matter)" % page)
            elif front:
                parts.append("PDF page %d (printed %d)" % (page, page - front))
            else:
                parts.append("PDF page %d" % page)
        return " | ".join(parts) if parts else "(document)"

    def add(self, sev, crit, where, what, evidence="", recurring="no", owner="", places=None):
        self.failed.add(crit)
        self.findings.append(dict(sev=sev, crit=crit, where=where, what=what, evidence=evidence,
                                  recurring=recurring, owner=owner, places=places or []))

    def check(self, crit, ok, **kw):
        """Record a pass/fail for a criterion; on failure also add a finding (kw as in add)."""
        if ok:
            if crit not in self.failed:
                self.passed.add(crit)
        else:
            self.add(crit=crit, **kw)
        return ok

    def skip(self, crit, reason):
        self.skipped[crit] = reason

    def note(self, text):
        self.notes.append(text)

    def emit(self):
        order = {"blocker": 0, "major": 1, "minor": 2}
        for n, f in enumerate(sorted(self.findings, key=lambda x: order.get(x["sev"], 3)), 1):
            print("### F-%s-%02d  [%s]  %s" % (self.skill, n, f["sev"], f["crit"]))
            print("- Where:     %s" % f["where"])
            print("- What:      %s" % f["what"])
            ev = f["evidence"].strip("\n")
            if ev:
                lines = ev.splitlines()
                print("- Evidence:  %s" % lines[0])
                for extra in lines[1:12]:
                    print("             %s" % extra)
                if len(lines) > 12:
                    print("             ... (%d more lines)" % (len(lines) - 12))
            else:
                print("- Evidence:  -")
            rec = f["recurring"]
            if rec == "yes" and f["places"]:
                shown = "; ".join(f["places"][:25]) + (" ..." if len(f["places"]) > 25 else "")
                print("- Recurring: yes (places: %s)" % shown)
            else:
                print("- Recurring: %s" % rec)
            print("- Owner:     %s" % (f["owner"] or "?"))
            print("- Status:    open")
            print("")
        for n in self.notes:
            print("NOTE: %s" % n)
        for crit in sorted(self.skipped):
            print("SKIPPED %s: %s" % (crit, self.skipped[crit]))
        print("SUMMARY %s: checked=%d pass=%d fail=%d skipped=%d findings=%d"
              % (self.script, len(self.passed | self.failed), len(self.passed - self.failed),
                 len(self.failed), len(self.skipped), len(self.findings)))
        return 1 if self.findings else 0


def front_arg(parser):
    parser.add_argument("--front", type=int, default=0,
                        help="number of front-matter PDF pages (cover, TOC, Hebrew page...); printed page = PDF page - front")
    return parser
