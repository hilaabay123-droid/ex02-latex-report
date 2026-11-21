BS = chr(92)
row = ("| 2026-11-20 | closettwin v0.21 | qa-se Q3-1, Q3-2 via master-se (qa/reports/03-part3-round1.md) | "
 "(Q3-1) Appendix A opener page held only the title, intro and code started on the next page; (Q3-2) Table 9.1 alone on a page with about 60% blank (same class as I-8; Table 8.2 on its own page too) | "
 "(Q3-1) v0.20 made the 26-line box unbreakable, it did not fit under the opener, and `" + BS + "ctkeepprev` ties it to its intro paragraph; (Q3-2) a float taller than the free space of the previous page moves to the next page, and nothing follows it in its chapter, so no text can fill the gap | "
 "(Q3-1) `" + BS + "pythonbox` plans a split: if the box does not fit the rest of the page it is cut ONCE at the last line that fits with at least 8 lines on each side (two boxes, continued line numbers); if that is impossible it moves whole. Verified: lines 1-18 under the opener, 19-26 on the next page. (Q3-2) NO class change: filling the gap needs text after the table, or a table split across pages, and a split table breaks acceptance criterion L3 (no table split), loses the float flow that lets text fill earlier gaps and cannot repeat a header row without rewriting every table. REQUEST sent to the chapter owners with exact pages (move the table block above following text in the section) | closettwin.cls |\n")
p = r"C:\biu\02\fix\CHANGELOG.md"
s = open(p, encoding="utf8").read().rstrip("\n") + "\n" + row
open(p, "w", encoding="utf8").write(s)

inc = r"""# Incident 11: tall table alone on a page (Q3-2) and Appendix A opener alone (Q3-1)

Date: 2026-11-20. Found by: qa-se, qa/reports/03-part3-round1.md. Handled by: fix-se. Skill: incident v1.0, qa-fixer v1.0.

## What happened
- Q3-1: the Appendix A opener page held only the title; the intro paragraph and the code box started on the next page.
- Q3-2: Table 9.1 sits alone on a page with about 60% of it blank; Table 8.2 has the same pattern (about 35% blank on the page before it).

## Root cause
- Q3-1: after incident 05 the 26-line box was unbreakable and tied to its intro paragraph; it did not fit under the opener, so both moved. A rule "never split" and a rule "no page alone" contradicted each other for any box taller than the space left.
- Q3-2: a float taller than the free space goes to the next page; nothing follows it in its chapter, so the gap stays. Floats fill gaps only with text that comes after them in the source.

## Why no detector caught it
The v1.1 white-space check (incident 08) is a text recipe that qa-se did not run in this pass (the report says the qa-super checks were not run in full).

## Fix
- Q3-1 (CLS v0.21): `\pythonbox` measures the room left on the page; a box that does not fit is split once, at the last fitting line, with at least 8 lines on each side; if that is not possible it moves whole. Before: PDF 46 title only, box on 47. After: see the rebuild report (lines 1-18 under the opener in the test, 19-26 next page).
- Q3-2: no safe CLS rule. A table split across pages would break acceptance criterion L3 and the header row cannot repeat without changing every table; floats cannot be pulled backwards. Remedy is in the content: put the table block earlier in its section so text follows it (REQUEST to the owners, exact pages in the report to master-se).

## New check
qa-typeset check 10 (white space per page) is run by a script, `python -I qa/scripts/page_stats.py --gaps` (request to qa-se): for each page the lowest text y; gap over 25% of the text height and a float on the next page = finding with the float label.

## Status
Q3-1 fixed in closettwin v0.21. Q3-2 open for the content owners.
"""
open(r"C:\biu\02\incidents\11-tall-table-alone-and-appendix-opener.md", "w", encoding="utf8").write(inc)
print("ok")
