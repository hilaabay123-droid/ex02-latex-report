"""Print the vertical gap (pt) between consecutive ivory boxes on every page of a PDF."""
import sys
import pymupdf

d = pymupdf.open(sys.argv[1])
for i, p in enumerate(d, 1):
    boxes = []
    for dr in p.get_drawings():
        r = dr["rect"]
        f = dr.get("fill")
        if f and r.width > 300 and r.height > 25 and abs(f[0] - 0.969) < 0.01:
            boxes.append((round(r.y0, 1), round(r.y1, 1)))
    boxes = sorted(set(boxes))
    gaps = [round(b[0] - a[1], 1) for a, b in zip(boxes, boxes[1:])]
    print(f"page {i}: boxes {len(boxes)} gaps(pt) {gaps}")
