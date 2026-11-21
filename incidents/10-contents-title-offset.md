# Incident 10: I-10: Contents title not aligned with the rule above

Date: 2026-11-20. Found by: the user in draft v1 (prompt 06). Handled by: fix-se. Skill: incident v1.0.

## What happened
On the Contents, List of figures and List of tables pages the title started about 7 pt to the right of the mocha rule above it.
Where: TOC page (pdf 3): rule at x = 85 pt, title at about 92 pt.

## Root cause
The chapter opener title paragraph started with the paragraph indent (`\parindent`) inside titlesec's block: all openers, numbered and unnumbered, shared it.

## Why no detector caught it
The earlier check compared only the y positions of rule and title (v0.15), not x. No detector had a criterion for this, and the visual look at every page (book 19.5 item 5) was postponed to the next session.

## Fix (in the CLS or a skill, not in the text)
closettwin v0.20: `\noindent` in both opener macros (`\ctchapterhead`, `\ctchapterheadstar`). Hebrew openers use a separate macro and were not affected.

## New check
qa-typeset v1.1: on every opener page the x of the rule and the first glyph of the title differ by at most 2 pt (the side bearing of the first letter).

## Status
Fixed in closettwin v0.20 (see `fix/CHANGELOG.md`). Re-check by qa-super after the next build.
