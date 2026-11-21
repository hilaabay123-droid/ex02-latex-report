import re, fitz, sys
doc = fitz.open("main.pdf")
print(repr(doc[0].get_text()[:400]))
for i,p in enumerate(doc):
    t = p.get_text()
    for m in re.finditer(r"(?<!\d)\d{9}(?!\d)", t):
        if m.group(0)!="875523402":
            ctx = t[max(0,m.start()-40):m.end()+10].replace("\n"," ")
            print("page",i+1, re.sub(r"\d","#",ctx))
for pn in (40,46,47,42):
    p = doc[pn-1]; H=p.rect.height
    bl = [(round(b[1]),round(b[3])) for b in p.get_text("blocks")]
    dr = [(round(fitz.Rect(d["rect"]).y0),round(fitz.Rect(d["rect"]).y1)) for d in p.get_drawings()][:30]
    print(pn, H, "blocks", bl[-6:], "draw max", max([y for _,y in dr] or [0]))
