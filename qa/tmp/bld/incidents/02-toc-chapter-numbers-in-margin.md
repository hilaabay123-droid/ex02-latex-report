# Incident 02: I-2: stray numbers 1, 2, 3 in the left margin

Date: 2026-11-20. Found by: the user in draft v1 (prompt 06). Handled by: fix-se. Skill: incident v1.0.

## What happened
The user saw the numbers 1, 2, 3 in the left margin next to the Hebrew summary.
Where: Not reproduced on the Hebrew page: a coordinate scan of every page found no word outside the text block there. The only words outside the 85 pt left margin are the ten chapter numbers of the TOC (x = 61 pt) on the page directly after the Hebrew page, so the report most probably refers to those.

## Root cause
`\titlecontents{chapter}[0pt]{...}{\contentslabel{2.2em}}` hangs the label 2.2em to the LEFT of the left margin: the chapter numbers stood 24 pt outside the text block.

## Why no detector caught it
No check measured text positions against the margins on every page (bbox_margin.py is used for the code page and a `--margins` check on a sample only). No detector had a criterion for this, and the visual look at every page (book 19.5 item 5) was postponed to the next session.

## Fix (in the CLS or a skill, not in the text)
closettwin v0.20: chapter entries `[2.2em]`, label width 2.2em: numbers start at the margin, titles at 2.2em, sections align with chapter titles. Verified by the scan: zero words left of 85 pt on pages with a TOC.

## New check
qa-BiDi v1.1 / qa-typeset v1.1: scan every page with PyMuPDF `get_text('words')`; any word with xMin < left margin or xMax > right margin (page width minus 3 cm) is a finding, short digit-only words are reported as 'stray numbers'. If the user's file differs from this analysis, master-se sends the page and a screenshot.

## Status
Fixed in closettwin v0.20 (see `fix/CHANGELOG.md`). Re-check by qa-super after the next build.
