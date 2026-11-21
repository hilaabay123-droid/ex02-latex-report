import fitz
doc = fitz.open("main.pdf"); FRONT=7
for i,p in enumerate(doc):
    if i<FRONT: continue
    H=p.rect.height
    ys=[b[3] for b in p.get_text("blocks") if b[1]>50 and b[3]<790]
    ys+=[fitz.Rect(d["rect"]).y1 for d in p.get_drawings() if fitz.Rect(d["rect"]).y1<770 and fitz.Rect(d["rect"]).y1>50]
    ys+=[fitz.Rect(im["bbox"]).y1 for im in p.get_image_info() if fitz.Rect(im["bbox"]).y1<790]
    low=max(ys) if ys else 0
    gap=(775-low)/(775-60)
    first=[l for l in p.get_text().splitlines() if l.strip()][1:2]
    flag="  <<<" if gap>0.25 else ""
    print(f"pdf{i+1:2d} printed{i+1-FRONT:2d} empty {gap*100:3.0f}%  {first}{flag}")
