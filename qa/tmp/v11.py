"""qa-se v1.1 checks (scratch). Run from the build dir: python -I v11.py main.pdf"""
import sys, re
import fitz

doc = fitz.open(sys.argv[1])
FRONT = 7
CM = 28.3465
n = len(doc)
print("pages", n)

# cover
t0 = doc[0].get_text()
for need in ["Generative AI for Management (875523402)", "Dr. Yoram Segal", "BUSINESS PLAN"]:
    print("cover has", need, need in t0)
alltext = "\n".join(p.get_text() for p in doc)
nine = set(re.findall(r"(?<!\d)\d{9}(?!\d)", alltext))
print("9-digit numbers (masked):", [x[:2] + "*******" for x in nine if x != "875523402"])

# margins and stray numbers
for i, p in enumerate(doc):
    W = p.rect.width
    for x0, y0, x1, y1, w, *_ in p.get_text("words"):
        if i == 0:
            continue
        if x0 < 2.9 * CM or x1 > W - 2.85 * CM:
            if y0 > 60 and y1 < p.rect.height - 60:  # skip banner/footer
                print(f"margin p{i+1}: x0={x0/CM:.2f}cm x1={(W-x1)/CM:.2f}cm {w!r}")

# number font in running text, mono fonts outside appendix
eqpages = set()
for i, p in enumerate(doc):
    d = p.get_text("dict")
    for b in d["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                f = s["font"]
                if "Mono" in f and "JetBrains" not in f:
                    print(f"mono p{i+1}: {f} {s['text'][:40]!r}")
                if "LMMath" in f or "LatinModernMath" in f or "LMRoman" in f or "Math" in f:
                    if re.search(r"\d", s["text"]):
                        print(f"mathdigit p{i+1}: {f} {s['text'][:40]!r}")

# literal hyphens
for i, p in enumerate(doc):
    if i == n - 1:
        continue
    for m in re.finditer(r".{15}--.{15}", p.get_text().replace("\n", " ")):
        print(f"dashes p{i+1}: {m.group(0)!r}")

# white space: lowest content y per page vs footer
for i, p in enumerate(doc):
    if i < FRONT:
        continue
    H = p.rect.height
    ys = [b[3] for b in p.get_text("blocks") if b[3] < H - 55 and b[1] > 55]
    ys += [r.y1 for r in [fitz.Rect(d["rect"]) for d in p.get_drawings()] if r.y1 < H - 55 and r.y1 > 55 and r.width > 20]
    imgs = [fitz.Rect(im["bbox"]).y1 for im in p.get_image_info()]
    low = max(ys + imgs) if ys + imgs else 0
    gap = (H - 60 - low) / (H - 120)
    if gap > 0.25:
        print(f"whitespace p{i+1} (printed {i+1-FRONT}): empty {gap*100:.0f}% of text height; first line {p.get_text().strip().splitlines()[0][:40]!r}")

# legend at first tag
tagpage = None
for i, p in enumerate(doc):
    if i < FRONT:
        continue
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                if s["size"] < 7.5 and s["text"].strip() in ("S", "D", "A") and (s["flags"] & 1):
                    tagpage = tagpage or i
t = doc[tagpage].get_text().lower() if tagpage is not None else ""
print("first tag page", None if tagpage is None else tagpage + 1, "legend words", all(w in t for w in ["sourced", "derived", "assum"]))

# pages holding only a heading
for i, p in enumerate(doc):
    lines = [l for l in p.get_text().splitlines() if l.strip() and "ClosetTwin" not in l and "Page" not in l]
    if i >= FRONT - 1 and len(lines) <= 3:
        print(f"heading-only/sparse p{i+1}: {lines}")

# opener alignment: rule x vs first title glyph
for i, p in enumerate(doc):
    txt = p.get_text()
    if i >= 2 and re.match(r"\s*(\d+\s+)?[A-Z]", txt):
        pass
