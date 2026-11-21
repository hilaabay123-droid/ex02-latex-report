# Incident 11: tall table alone on a page (Q3-2) and Appendix A opener alone (Q3-1)

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
