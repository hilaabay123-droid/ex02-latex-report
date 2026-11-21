"""Compare the text extracted from the code page of a PDF with python/appendix_f6_code.py.
Usage: python fix/chk_code.py main.pdf [page]   (default: the page holding 'Appendix A')"""
import sys, pymupdf
pdf = sys.argv[1]
d = pymupdf.open(pdf)
n = int(sys.argv[2]) - 1 if len(sys.argv) > 2 else next(i for i, p in enumerate(d) if "Appendix A" in p.get_text() and "import" in p.get_text())
t = d[n].get_text()
src = open("python/appendix_f6_code.py", encoding="utf-8").read()
sp = set(c for c in src if not c.isalnum() and c not in " \n")
ep = set(c for c in t if not c.isalnum() and c not in " \n")
print("page", n + 1)
print("in PDF but not in source:", ascii("".join(sorted(ep - sp))))
print("in source but not in PDF:", ascii("".join(sorted(sp - ep))))
norm = lambda x: " ".join(x.split())
ex = [norm(l) for l in t.split("\n")]
import re
# code and its trailing comment are separate lines in the extraction: compare segment by segment
miss = [seg for l in src.split("\n") for seg in re.split(r"\s{2,}", l.strip()) if seg and norm(seg) not in ex]
print("source lines not found verbatim in the extraction:", len(miss))
for l in miss[:12]:
    print("  ", ascii(l))
sys.exit(1 if (ep - sp) or miss else 0)
