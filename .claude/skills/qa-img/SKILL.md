---
name: qa-img
description: Detector (report-only) for figures: file exists, caption/label/reference, 1:1 width, fonts, palette, contrast and grayscale, no overlap, honest against the data. Use after a build or when asked to check figures or graphs.
version: 1.1
---

# qa-img

Checks every figure's file, framing, caption, label, reference, size, fonts, colours, contrast, grayscale and honesty against its data.

**Report-only.** This skill finds and reports. It never edits a chapter, figure, script, bib or the CLS, never fixes, never commits.
A fix goes to the owner named in the finding; a recurring problem goes to fix-se (iron rule, root `CLAUDE.md`).
If `main.pdf`, `main.log` or `main.aux` is older than the newest `.tex`/`.cls`/`.bib`, stop with `BLOCKED: stale or missing build`.
Criteria IDs refer to `qa/acceptance-criteria.md`; full step detail is in `qa/skill-specs.md`. Helper scripts live in `qa/scripts/` and run as `python -I qa/scripts/<name>.py`.
A criterion that could not be checked is `skipped` with a reason, never silently passed.
Save to `qa/reports/NN-<topic>.md` (NN = next free number). Reply to master-se: `REPORT <scope>` + path + counts by severity.

## When to use
After a build with new or changed figures; part of `qa-super`.

## Inputs
`figures/*`, `python/*.py`, `chapters/*.tex`, `main.pdf`, `main.aux`, `main.lof`, `python/data/*.csv`.

## Procedure
1. Inventory: `grep -n "begin{figure\|includegraphics\|\\input{figures" chapters/*.tex`. Expect 7 figures (F1-F7 of PRD 5.4), at least one Python graph and one TikZ diagram. Every file exists (`grep -i "not found" main.log` empty). No `http` image; each figure maps to a script or TikZ source (I1, I2, I6, D12).
2. Each figure has `\caption`, `\label{fig:...}`, a `\ref` in the text (`python -I qa/scripts/label_refs.py fig`), first mention on the same or next page (I3, I10).
3. Size (I4): width is `\textwidth` or absent, never a scale factor: `grep -n "scale=\|width=" chapters/*.tex`.
4. Fonts (I8): `pdffonts figures/*.pdf` lists only Rubik/Playfair, all embedded, none Type 3.
5. Palette (I7, D6): `grep -noE "#[0-9A-Fa-f]{6}" python/*.py figures/*.tex`: only 111111, F7F3EE, A47864, E8C6C0, 6B4B3D, D3BBAE, E3DCD4, 6F6862.
6. Contrast (D18) and grayscale (I12): render the page at 150 dpi; `python -I qa/scripts/contrast_colors.py <png> --text` (WCAG 4.5:1 small, 3:1 large) and `--gray` (luminance gap of series at least 20% or a direct label).
7. Look (I5, I11): labels not overlapping, text at least 8 pt, axes and legend complete, no cropped edge, one y-axis, at most 4 series (D16).
8. Honesty (I9, I14): plotted values equal the text, `assumptions.csv` and `python/model.py` output; financial charts say "Assumption"; F5 marks first profitable year and peak deficit and shows nothing past Y5; F6 marks retailer break-even; F2 axes equal two columns of the vendor table; F1 is "not to scale".
9. Page share (I13): figures at most 50% of the text block, at most one figure per page.

## Outputs
Finding blocks plus a figure inventory: `fig | file | tool | ch. | PDF page | 1:1 | fonts ok | palette ok | contrast ok | gray ok | referenced | data checked`.

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

Recurring-prone: I3, I4, I5, I7, I8, I12, I13. A defect in `ct_style.py` is recurring: owner art-se for the style module, fix-se if the cause is the CLS figure environment or caption. One wrong axis or value: recurring = no, owner art-se.

## Success check
I1-I14, D6, D9, D12, D16, D18 (figure parts) each pass, fail or are skipped with a reason; the inventory has one row per figure in the PDF.

## New checks (v1.1)
10. **Figure and table in the lists:** every figure caption in `main.lof` has no underscore, file name or bracketed note (same rule as qa-table 9).
