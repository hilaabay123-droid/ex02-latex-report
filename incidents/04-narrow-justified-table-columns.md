# Incident 04: I-4: Table 8.1 narrow first column with stretched spaces

Date: 2026-11-20. Found by: the user in draft v1 (prompt 06). Handled by: fix-se. Skill: incident v1.0.

## What happened
Table 8.1 (Main inputs): the first column wrapped to 2-3 lines with stretched word spaces.
Where: ch.8, `\begin{tabularx}{\textwidth}{XRll}`.

## Root cause
Two causes. (a) tabularx text columns `X` are justified by default, so narrow cells stretch. (b) The `l` columns take their natural width; long `l` text (Class, Basis) leaves the `X` column almost nothing. (a) is a class default; (b) is a column specification.

## Why no detector caught it
qa-table checked width and alignment of numbers but not text-column justification or the width share of the first column. No detector had a criterion for this, and the visual look at every page (book 19.5 item 5) was postponed to the next session.

## Fix (in the CLS or a skill, not in the text)
closettwin v0.20: `\tabularxcolumn` is ragged right, so no `X` cell is justified. For (b) REQUEST to writer-se: use `X` for the long text columns and `l` only for short ones (table 8.1: `XRlX`); every tabularx in ch. 2, 3, 5, 6, 8, 9 to be re-checked.

## New check
qa-table v1.1: per table, record the width of each column from `pdftotext -bbox`; fail if the first column is under 3 cm while other columns hold long text, or if any cell has a word space wider than 2x the normal one (justified narrow cell).

## Status
Fixed in closettwin v0.20 (see `fix/CHANGELOG.md`). Re-check by qa-super after the next build.
