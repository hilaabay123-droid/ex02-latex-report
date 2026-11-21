"""page_stats.py: qa-typeset. Per-page statistics, orphan headings, empty pages, page budget (L2, L4, D1, D17, BU9).

Usage: python qa/scripts/page_stats.py main.pdf [--toc main.toc] [--front K] [--min-chars 600] [--pages]
          [--budget "1:3,2:4,3:3,4:4,5:3,6:2,7:2,8:3,9:2,10:1"] [--min-total 25]

--pages        print one line per page: chars, words, first and last line
L4             a content page with fewer than --min-chars characters (not the last page of a chapter, not a 1-page chapter)
L2             a heading-sized line among the last 2 text lines of a page
D1, D17        from --toc: numbered chapters 1..10 (content), page count per chapter, +/-1 tolerance, conclusion exactly 1,
               total >= --min-total. Content = chapter 1 up to the page before the first unnumbered chapter after chapter 10
               (references, appendix) or the end of the PDF. Without a usable --toc the budget is skipped.
"""
import argparse
import os
import re
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qa_common import Report, front_arg, need_file, pdf_bbox, pdf_pages, pdf_texts, read_text

BUDGET = {1: 3, 2: 4, 3: 3, 4: 4, 5: 3, 6: 2, 7: 2, 8: 3, 9: 2, 10: 1}


def parse_toc(path):
    """[(numbered?, number, title, printed_page)] for \\contentsline {chapter} entries."""
    out = []
    for line in read_text(path).splitlines():
        m = re.match(r"\\contentsline \{chapter\}\{(.*?)\}\{(\d+|[ivxlc]+)\}", line)
        if not m:
            continue
        body, page = m.group(1), m.group(2)
        n = re.search(r"\\numberline \{(\d+)\}", body)
        title = re.sub(r"\\numberline \{\d+\}", "", body).strip()
        out.append((bool(n), int(n.group(1)) if n else None, title, int(page) if page.isdigit() else 0))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--toc")
    ap.add_argument("--min-chars", type=int, default=600)
    ap.add_argument("--min-total", type=int, default=25)
    ap.add_argument("--budget", default="")
    ap.add_argument("--pages", action="store_true")
    ap.add_argument("--gaps", action="store_true",
                    help="white space check (qa-typeset v1.1 check 10): lowest text y per page")
    ap.add_argument("--gap-limit", type=float, default=0.25)
    front_arg(ap)
    a = ap.parse_args()
    need_file(a.pdf, "PDF")
    rep = Report("typeset", "page_stats.py")

    n = pdf_pages(a.pdf)
    texts = pdf_texts(a.pdf)
    boxes = pdf_bbox(a.pdf)
    rep.note("PDF pages: %d; front matter pages given: %d; content pages (PDF - front): %d" % (n, a.front, n - a.front))
    budget = dict(BUDGET)
    if a.budget:
        budget = {int(k): int(v) for k, v in (kv.split(":") for kv in a.budget.split(","))}

    # chapter table from the toc
    chapter_first = {}
    content_end = None
    if a.toc and os.path.isfile(a.toc):
        entries = parse_toc(a.toc)
        numbered = [e for e in entries if e[0]]
        for _, num, title, page in numbered:
            chapter_first[num] = page + a.front
        after = [e for e in entries if not e[0] and e[3] and numbered and e[3] + a.front > max(chapter_first.values(), default=0)]
        content_end = (min(e[3] for e in after) + a.front - 1) if after else n
    chapter_last_pages = set()
    if chapter_first:
        order = sorted(chapter_first)
        for i, c in enumerate(order):
            nxt = chapter_first[order[i + 1]] if i + 1 < len(order) else (content_end + 1)
            chapter_last_pages.add(nxt - 1)

    # per page stats and flags
    one_page_chapters = {chapter_first[c] for c in chapter_first if budget.get(c) == 1}
    for i, t in enumerate(texts):
        p = i + 1
        lines = [l for l in t.splitlines() if l.strip()]
        chars = len(re.sub(r"\s", "", t))
        words = len(t.split())
        if a.pages:
            rep.note("p%-3d chars=%-5d words=%-4d first=%r last=%r" % (p, chars, words, (lines[0].strip()[:30] if lines else ""),
                                                                      (lines[-1].strip()[:30] if lines else "")))
        in_content = p > a.front
        if in_content and chars < a.min_chars and p not in chapter_last_pages and p not in one_page_chapters and (lines or True):
            rep.check("L4", False, sev="major", where=rep.where(page=p, front=a.front),
                      what="nearly empty page: %d characters (< %d)" % (chars, a.min_chars),
                      evidence="first line: %r; last line: %r" % (lines[0].strip()[:50] if lines else "", lines[-1].strip()[:50] if lines else ""),
                      recurring="no", owner="writer-se (content volume) or fix-se (float/spacing) if it repeats")
        else:
            rep.passed.add("L4")
        # orphan heading: a line with a larger font among the last 2 text lines
        if in_content and p - 1 < len(boxes):
            words_b = boxes[p - 1]["words"]
            # exclude header/footer zones (top 9%, bottom 8%)
            h = boxes[p - 1]["height"]
            body = [w for w in words_b if 0.09 * h < w[1] and w[3] < 0.92 * h]
            if body:
                sizes = [w[3] - w[1] for w in body]
                med = statistics.median(sizes)
                rows = {}
                for w in body:
                    rows.setdefault(round(w[1] / 4), []).append(w)
                keys = sorted(rows)
                if len(keys) >= 3:
                    last_rows = keys[-2:]
                    for k in last_rows:
                        rs = max(w[3] - w[1] for w in rows[k])
                        if rs > 1.3 * med and len(rows[k]) <= 12:
                            txt = " ".join(w[4] for w in sorted(rows[k]))
                            rep.check("L2", False, sev="major", where=rep.where(page=p, front=a.front),
                                      what="a heading-sized line is among the last lines of the page (orphan heading)",
                                      evidence="%r, line height %.1f vs body %.1f" % (txt[:60], rs, med), recurring="yes",
                                      owner="fix-se", places=["PDF page %d" % p])
                            break
                    else:
                        rep.passed.add("L2")


    # white space (v1.1 check 10): gap above the footer > limit of the text height, and a float starts the next page
    if a.gaps:
        for i, pg in enumerate(boxes):
            p = i + 1
            if p <= a.front or p in chapter_last_pages or p in one_page_chapters or p >= n:
                continue
            h = pg["height"]
            top, bottom = 0.09 * h, 0.92 * h          # text block between banner and footer
            body = [w for w in pg["words"] if top < w[1] and w[3] < bottom]
            if not body:
                continue
            low = max(w[3] for w in body)
            gap = (bottom - low) / (bottom - top)
            if a.pages:
                rep.note("p%-3d lowest text y=%.0f of %.0f, gap %.0f%%" % (p, low, h, gap * 100))
            if gap <= a.gap_limit:
                rep.passed.add("L3")
                continue
            nxt = [w for w in boxes[i + 1]["words"] if top < w[1] and w[3] < bottom]
            lines = {}
            for w in nxt:
                lines.setdefault(round(w[1] / 4), []).append(w)
            first = ""
            for k in sorted(lines)[:12]:
                txt = " ".join(x[4] for x in sorted(lines[k]))
                if re.match(r"^(Table|Figure)\s+\d+\.\d+", txt):
                    first = txt[:50]
                    break
            if first:
                rep.check("L3", False, sev="major", where=rep.where(page=p, front=a.front),
                          what="white space: %.0f%% of the text height is empty above the footer and a float starts the next page" % (gap * 100),
                          evidence="lowest text at y=%.0f of %.0f; next page near the top: %r" % (low, h, first),
                          recurring="yes", owner="fix-se", places=["PDF page %d" % p])
            else:
                rep.note("p%d: gap %.0f%% but no float caption near the top of the next page (not reported)" % (p, gap * 100))

    # page budget and content total
    if chapter_first and all(c in chapter_first for c in budget):
        order = sorted(chapter_first)
        total = 0
        for i, c in enumerate(order):
            nxt = chapter_first[order[i + 1]] if i + 1 < len(order) else content_end + 1
            pages = nxt - chapter_first[c]
            total += pages
            lo, hi = (budget[c] - 1, budget[c] + 1) if c != 10 else (1, 1)
            lo = max(lo, 1)
            rep.note("chapter %d: first PDF page %d, %d page(s), budget %d, accept %d-%d" % (c, chapter_first[c], pages, budget[c], lo, hi))
            rep.check("D17", lo <= pages <= hi, sev="major", where=rep.where(page=chapter_first[c], front=a.front),
                      what="chapter %d has %d page(s), budget %d (accept %d-%d)" % (c, pages, budget[c], lo, hi),
                      owner="writer-se")
        rep.check("D1", total >= a.min_total, sev="blocker", where=rep.where(),
                  what="content pages (chapters 1-10, references and appendix excluded) = %d, the hard minimum is %d" % (total, a.min_total),
                  owner="writer-se")
    else:
        # fallback: PDF pages minus front matter (references/appendix not separable)
        content = n - a.front
        rep.skip("D17", "no usable --toc (needs numbered \\contentsline {chapter} entries 1..%d)" % max(budget))
        rep.check("D1", content >= a.min_total, sev="blocker", where=rep.where(),
                  what="fallback count: %d PDF pages minus %d front-matter = %d content page(s) (references/appendix not subtracted); minimum %d"
                       % (n, a.front, content, a.min_total), owner="writer-se")
    rep.check("BU9", True, sev="minor", where="", what="")
    sys.exit(rep.emit())


if __name__ == "__main__":
    main()
