---
name: qa-table
description: Detector (report-only) for tables: caption above, label and reference, width within the text block, right-aligned numbers, header look, numbers equal to text and CSV, assumption labelling. Use after a build or when asked to check tables.
version: 1.0
---

# qa-table

Checks every table's structure, order, alignment, width, caption, label, reference, numbers and assumption labelling.

**Report-only.** This skill finds and reports. It never edits a chapter, figure, script, bib or the CLS, never fixes, never commits.
A fix goes to the owner named in the finding; a recurring problem goes to fix-se (iron rule, root `CLAUDE.md`).
If `main.pdf`, `main.log` or `main.aux` is older than the newest `.tex`/`.cls`/`.bib`, stop with `BLOCKED: stale or missing build`.
Criteria IDs refer to `qa/acceptance-criteria.md`; full step detail is in `qa/skill-specs.md`. Helper scripts live in `qa/scripts/` and run as `python -I qa/scripts/<name>.py`.
A criterion that could not be checked is `skipped` with a reason, never silently passed.
Save to `qa/reports/NN-<topic>.md` (NN = next free number). Reply to master-se: `REPORT <scope>` + path + counts by severity.

## When to use
After each build with new or changed tables; part of `qa-super`.

## Inputs
`chapters/*.tex`, `main.pdf`, `main.log`, `main.aux`, `main.lot`, `python/data/assumptions.csv`.

## Procedure
1. Inventory: `grep -n "begin{table\|begin{tabular\|begin{tabularx\|\\caption\|\\label{tab:" chapters/*.tex`. Each table has `\caption` before the body and `\label{tab:...}` (TB1, TB2). Target 5 tables.
2. Every `tab:` label is cited in the text: `python -I qa/scripts/label_refs.py tab` (TB2); no undefined `tab:` in `main.log`.
3. Page of each table from `main.aux`; render `pdftoppm -r 100 -f p -l p -png main.pdf qa/tmp/tab`.
4. Look (TB3, TB4, TB7): within 15.0 cm, no cell past the margin, ivory header with hairline, numbers right-aligned, text left, same look in every table, not split, no heading alone above it.
5. Width by log: `python -I qa/scripts/overfull.py main.log --pages main.aux`, overfull on table pages, threshold 1 pt.
6. Numbers (TB5): `pdftotext -layout -f p -l p main.pdf -`; compare with the text and with `assumptions.csv`; `python -I qa/scripts/table_sums.py` recomputes marked totals.
7. Labelling (TB6): financial tables say "Assumption" and have a class column (sourced/derived/assumed) with a source per row; vendor table caption "Vendor claims", blanks read "not stated".
8. Column order: row label first, units in the header only.

## Outputs
Finding blocks plus a table inventory: `label | caption (first 8 words) | chapter | PDF page | width ok | caption above | referenced | numbers ok`.

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

Recurring-prone: TB2, TB3, TB4, TB7. A width or alignment defect in a table built with the CLS table macro is recurring = yes (name every table sharing the column spec), owner fix-se. A wrong number in one cell is recurring = no, owner writer-se.

## Success check
Criteria TB1-TB7 (and the table parts of D9, D16, D18) each pass, fail or are skipped with a reason; summary line present; the inventory covers every table in the PDF.
