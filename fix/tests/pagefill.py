"""Per page: body text lines (non-code), code lines, flags.  Usage: python pagefill.py file.pdf
Flags: BOX-ONLY (no text line besides code/box text), FEW (< 3 non-code lines: a box with a lone line),
NEARLY EMPTY (< 8 body lines in total)."""
import sys
import pymupdf

d = pymupdf.open(sys.argv[1])
bad = 0
for i, p in enumerate(d, 1):
    text = code = 0
    for b in p.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            y = l["bbox"][1]
            if not (90 < y < 770):
                continue
            fonts = " ".join(s["font"] for s in l["spans"])
            if "JetBrains" in fonts:
                code += 1
            elif l["spans"][0]["text"].strip() or len(l["spans"]) > 1:
                text += 1
    flags = []
    if code and text == 0:
        flags.append("BOX-ONLY")
    elif code and text < 3:
        flags.append("FEW-TEXT")
    if text + code < 8:
        flags.append("NEARLY-EMPTY")
    if flags:
        bad += 1
    print(f"page {i:2d}: text {text:3d}  code {code:3d}  {' '.join(flags)}")
print("pages flagged:", bad)
