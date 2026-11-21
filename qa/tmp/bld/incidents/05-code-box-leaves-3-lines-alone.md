# Incident 05: I-5: Appendix A code box leaves 3 lines alone

Date: 2026-11-20. Found by: the user in draft v1 (prompt 06). Handled by: fix-se. Skill: incident v1.0.

## What happened
The code box split over two pages and the last page held only 3 lines (pdf pp. 42-43).
Where: Appendix A, `\pythonbox{python/appendix_f6_code.py}`.

## Root cause
`\ct@pysplitmax` was 15: any script longer than 15 lines was breakable at ANY line, with no minimum for either fragment.

## Why no detector caught it
qa-code checked margin, fonts and source equality but not how a box is split between pages. No detector had a criterion for this, and the visual look at every page (book 19.5 item 5) was postponed to the next session.

## Fix (in the CLS or a skill, not in the text)
closettwin v0.20: `\ct@pysplitmax` = 45; a script up to 45 lines is never split. Side effect, stated: an unbreakable box that does not fit under the chapter opener moves, with its intro paragraph, to the next page, so the opener page holds only the title (a longer intro on that page fills it). A script over 45 lines still splits.

## New check
qa-code v1.1: for a box on two pages, each fragment needs at least 8 lines; and qa-typeset: a page whose text is only a heading is reported.

## Status
Fixed in closettwin v0.20 (see `fix/CHANGELOG.md`). Re-check by qa-super after the next build.
