"""label_refs.py: qa-table / qa-img. Labels, captions and references of tables, figures, equations (TB2, I3, D10).

Usage: python qa/scripts/label_refs.py tab|fig|eq [--src chapters main.tex] [--aux main.aux] [--front K]

  every table/figure environment has a \\caption and a \\label{<kind>:...}
  table caption is ABOVE the table body (TB2); figure caption may be either
  every label of the kind is referenced at least once (\\ref, \\autoref, \\cref, \\eqref, \\pageref, \\nameref)
  every reference to a <kind>: label points to an existing label (sources + --aux)
--src takes files or folders (default: chapters and main.tex when they exist).
"""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_common import Report, front_arg, parse_aux_labels, read_text

ENV = {"tab": "table", "fig": "figure", "eq": "equation"}
REF = re.compile(r"\\(?:ref|autoref|cref|Cref|eqref|pageref|nameref|vref)\*?\{([^}]+)\}")
LABEL = re.compile(r"\\label\{([^}]+)\}")


def gather(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += sorted(glob.glob(os.path.join(p, "**", "*.tex"), recursive=True))
        elif os.path.isfile(p):
            files.append(p)
        else:
            files += sorted(glob.glob(p))
    return files


def strip_comments(text):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", l) for l in text.splitlines())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=sorted(ENV))
    ap.add_argument("--src", nargs="*", default=None)
    ap.add_argument("--aux")
    front_arg(ap)
    a = ap.parse_args()
    src = a.src if a.src else [p for p in ("chapters", "main.tex") if os.path.exists(p)]
    files = gather(src)
    rep = Report("table" if a.kind == "tab" else "img", "label_refs.py")
    crit = {"tab": "TB2", "fig": "I3", "eq": "D10"}[a.kind]
    if not files:
        rep.skip(crit, "no .tex files found in %s" % src)
        sys.exit(rep.emit())

    labels = {}   # label -> (file, line)
    refs = {}     # label -> [(file, line)]
    env = ENV[a.kind]
    for f in files:
        text = strip_comments(read_text(f))
        for m in LABEL.finditer(text):
            if m.group(1).startswith(a.kind + ":"):
                labels[m.group(1)] = (f, text.count("\n", 0, m.start()) + 1)
        for m in REF.finditer(text):
            for lab in m.group(1).split(","):
                lab = lab.strip()
                if lab.startswith(a.kind + ":"):
                    refs.setdefault(lab, []).append((f, text.count("\n", 0, m.start()) + 1))
        # environments
        if a.kind in ("tab", "fig"):
            for m in re.finditer(r"\\begin\{%s\*?\}(.*?)\\end\{%s\*?\}" % (env, env), text, re.S):
                body = m.group(1)
                line = text.count("\n", 0, m.start()) + 1
                has_cap = "\\caption" in body
                has_lab = bool(re.search(r"\\label\{%s:" % a.kind, body))
                rep.check(crit, has_cap and has_lab, sev="major", where=rep.where(file=f, line=line),
                          what="%s environment without %s" % (env, " and ".join(x for x, ok in (("\\caption", has_cap), ("\\label{%s:...}" % a.kind, has_lab)) if not ok)),
                          recurring="yes", owner="writer-se (or fix-se if a CLS macro should force it)", places=["%s:%d" % (f, line)])
                if a.kind == "tab" and has_cap:
                    cap = body.find("\\caption")
                    tab = re.search(r"\\begin\{(?:tabular|tabularx|longtable|tabulary|tblr)", body)
                    if tab:
                        rep.check(crit, cap < tab.start(), sev="major", where=rep.where(file=f, line=line),
                                  what="table caption is below the table body; the book rule is caption ABOVE",
                                  recurring="yes", owner="fix-se (table macro) / writer-se", places=["%s:%d" % (f, line)])

    aux = parse_aux_labels(a.aux) if a.aux else {}
    rep.note("%d %s label(s) in sources, %d referenced label(s), %d in aux" % (len(labels), a.kind, len(refs), len([k for k in aux if k.startswith(a.kind + ':')])))
    unref = [l for l in labels if l not in refs]
    rep.check(crit, not unref, sev="major", where=rep.where(file=labels[unref[0]][0], line=labels[unref[0]][1]) if unref else "",
              what="%d %s label(s) never referenced in the text (a %s that the text does not mention)" % (len(unref), a.kind, env),
              evidence="\n".join("%s  %s:%d" % (l, labels[l][0], labels[l][1]) for l in unref[:10]),
              recurring="yes" if len(unref) > 1 else "no", owner="writer-se", places=unref)
    undef = [l for l in refs if l not in labels and l not in aux]
    rep.check(crit, not undef, sev="blocker", where=rep.where(file=refs[undef[0]][0][0], line=refs[undef[0]][0][1]) if undef else "",
              what="%d reference(s) to a %s label that does not exist" % (len(undef), a.kind),
              evidence="\n".join("%s  %s:%d" % (l, refs[l][0][0], refs[l][0][1]) for l in undef[:10]), owner="writer-se")
    sys.exit(rep.emit())


if __name__ == "__main__":
    main()
