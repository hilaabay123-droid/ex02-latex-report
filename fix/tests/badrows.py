"""List lines that end in a single backslash (a table row that lost one backslash); optional --fix writes the doubled form."""
import glob, sys
BS = chr(92)
root = sys.argv[1]
fix = "--fix" in sys.argv
for f in sorted(glob.glob(root + "/chapters/*.tex")):
    lines = open(f, encoding="utf8", newline="").read().split("\n")
    changed = False
    for i, l in enumerate(lines):
        t = l.rstrip("\r")
        if t.endswith(BS) and not t.endswith(BS + BS):
            print(f, i + 1, t[-40:])
            if fix:
                lines[i] = t + BS + l[len(t):]
                changed = True
    if fix and changed:
        open(f, "w", encoding="utf8", newline="").write("\n".join(lines))
