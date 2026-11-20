---
name: qa-typeset
description: Detector (report-only) for compilation warnings and pagination: overfull/underfull boxes over 1 pt, undefined refs, page count and budget, orphan headings, short pages, margins, banner/footer. Use after a build.
version: 1.0
---

# qa-typeset

Turns the TeX log and the rendered pages into a check of overfull/underfull boxes, page count, page budget and the layout rules.

**Report-only.** This skill finds and reports. It never edits a chapter, figure, script, bib or the CLS, never fixes, never commits.
A fix goes to the owner named in the finding; a recurring problem goes to fix-se (iron rule, root `CLAUDE.md`).
If `main.pdf`, `main.log` or `main.aux` is older than the newest `.tex`/`.cls`/`.bib`, stop with `BLOCKED: stale or missing build`.
Criteria IDs refer to `qa/acceptance-criteria.md`; full step detail is in `qa/skill-specs.md`. Helper scripts live in `qa/scripts/` and run as `python -I qa/scripts/<name>.py`.
A criterion that could not be checked is `skipped` with a reason, never silently passed.
Save to `qa/reports/NN-<topic>.md` (NN = next free number). Reply to master-se: `REPORT <scope>` + path + counts by severity.

## When to use
After every full build; part of `qa-super`.

## Inputs
`main.log`, `main.blg`, `main.toc`, `main.aux`, `main.pdf`.

## Procedure
1. Overfull (BU5, C5, L9): `python -I qa/scripts/overfull.py main.log`: every `Overfull \hbox/\vbox` with page and source line. Fail if more than 1.0 pt. Print the full table.
2. Underfull (BU6): count and list badness 10000 lines in body text with pages.
3. Other warnings (BU2-BU4, BU7, BU8): `grep -c "^!" main.log`; `grep -c "undefined" main.log`; `grep -c "Missing character" main.log`; `grep -i "rerun" main.log` empty on the last pass; `grep -E "ERROR|WARN" main.blg`; `grep -n "Float too large\|too many unprocessed floats" main.log`.
4. Page count and budget (D1, D17, BU9): `pdfinfo main.pdf | grep Pages`; `python -I qa/scripts/page_stats.py` prints per chapter first page, pages and the budget check (conclusion exactly 1 page, content total at least 25 pages, chapters 1-10 only).
5. Per-page statistics (L2, L4, L5): `python -I qa/scripts/page_stats.py --pages`: flags a page under 600 characters that is not a chapter end or the conclusion, a last line that is a heading (orphan heading), a one-word last line.
6. Look at every page (L1, L3, L6-L9, 19.5 item 5): `pdftoppm -r 80 -png main.pdf qa/tmp/p`, read each PNG, record the page list: new page per chapter, TOC complete, no float or box split, banner and footer on every page except the cover and openers, page numbers equal the TOC, text inside the margins.
7. Airy rule (D16, I13): `python -I qa/scripts/bbox_margin.py --margins`; at most one figure and one table per page.
8. Cover (C2, C3, C5): page 1 has no number or footer; roman front matter, arabic from chapter 1.

## Outputs
Finding blocks plus three tables: overfull/underfull list (`kind | amount | page | source line`), page budget (`chapter | budget | actual | range | verdict`), page stats (`page | chars | last line | flags`).

## Finding format (one block per finding)
```
### F-<skill>-<nn>  [blocker|major|minor]  <criterion ID(s)>
- Where:     <file>:<line> | PDF page <printed page> (<pdf index>)
- What:      <one sentence: the rule broken>
- Evidence:  <exact text / log line / command + output>
- Recurring: yes|no  (yes = same criterion in 2+ places, a CLS-class cause, or it reappeared; list EVERY place; owner fix-se)
- Owner:     writer-se | art-se | fix-se | master-se
- Status:    open
```

Recurring-prone: BU5, L1, L2, L3, L4, L7, L9. Two overfull boxes of one kind (long URL, wide table) are ONE recurring finding listing all lines, owner fix-se. A short page from one chapter's volume: recurring = no, owner writer-se, unless it appears in 2 or more chapters.

## Success check
BU2-BU10, L1-L9, D1, D17, C2, C3, C5 each pass, fail or are skipped with reason; page budget table printed; the overfull table is complete, not only failures.
