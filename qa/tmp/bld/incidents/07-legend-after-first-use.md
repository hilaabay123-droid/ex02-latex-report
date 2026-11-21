# Incident 07: I-7: superscript S/D/A without a legend before first use

Date: 2026-11-20. Found by: the user in draft v1 (prompt 06). Handled by: fix-se. Skill: incident v1.0.

## What happened
The mocha superscripts D and A appear after numbers, and the legend is printed later (ch.1 line 30 vs first use at line 24).
Where: ch.1: `\assumed{24.4\%}` comes before `\ctlegend`.

## Root cause
The legend was a manual call placed by the author; nothing in the class guarantees it appears before the first tag.

## Why no detector caught it
qa-table checked the legend inside financial tables only; no check of the first use of a tag in the document. No detector had a criterion for this, and the visual look at every page (book 19.5 item 5) was postponed to the next session.

## Fix (in the CLS or a skill, not in the text)
closettwin v0.20: the first `\sourced/\derived/\assumed` in running text adds the legend as a footnote on that page (`\ct@firstlegend`; skipped silently inside tables, captions, boxes and formulas, where a footnote is impossible, and tried again at the next use). The manual `\ctlegend` stays valid.

## New check
qa-table v1.1 / qa-typeset: the first page that carries a tag superscript must also carry the legend text 'sourced', 'derived', 'assumption'.

## Status
Fixed in closettwin v0.20 (see `fix/CHANGELOG.md`). Re-check by qa-super after the next build.
