import pathlib
R = pathlib.Path(r"C:\biu\02\.claude\skills")
FMT = r"""
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
"""
RULE = r"""
**Report-only.** This skill finds and reports. It never edits a chapter, figure, script, bib or the CLS, never fixes, never commits.
A fix goes to the owner named in the finding; a recurring problem goes to fix-se (iron rule, root `CLAUDE.md`).
If `main.pdf`, `main.log` or `main.aux` is older than the newest `.tex`/`.cls`/`.bib`, stop with `BLOCKED: stale or missing build`.
Criteria IDs refer to `qa/acceptance-criteria.md`; full step detail is in `qa/skill-specs.md`. Helper scripts live in `qa/scripts/` and run as `python -I qa/scripts/<name>.py`.
A criterion that could not be checked is `skipped` with a reason, never silently passed.
Save to `qa/reports/NN-<topic>.md` (NN = next free number). Reply to master-se: `REPORT <scope>` + path + counts by severity.
"""


def w(name, desc, body):
    (R / name / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {desc}\nversion: 1.0\n---\n\n# {name}\n\n" + body.strip() + "\n",
        encoding="utf8")


w("qa-BiDi",
  "Detector (report-only) for Hebrew/English direction: reversed runs, bullets/numbers on the wrong side, punctuation and parentheses at run boundaries, missing glyphs, wrong fonts on the Hebrew page. Use after a build, or when asked to check Hebrew/RTL.",
  r"""
Proves the Hebrew executive-summary page is correct BiDi and that no direction or glyph error exists elsewhere.
""" + RULE + r"""
## When to use
After every full build that touches the Hebrew page, the CLS, or any text with Hebrew; always as part of `qa-super`.

## Inputs
`main.pdf`, `main.log`, `main.toc`, the Hebrew page source (`chapters/00-*.tex`), `qa/scripts/bidi_runs.txt` (required Latin runs and numbers).

## Procedure
1. Find Hebrew pages: `python -I qa/scripts/hebrew_pages.py main.pdf`. Expect exactly one, in the front matter (B1, B8). Hebrew letters elsewhere = finding.
2. Missing glyphs: `grep -c "Missing character" main.log` must be 0; also `grep -n "^!" main.log` (B9).
3. Corpus: `pdftotext -f N -l N -bbox main.pdf qa/tmp/heb.html`, then `python -I qa/scripts/bidi_bbox_check.py qa/tmp/heb.html qa/scripts/bidi_runs.txt`. It finds each required run as written, fails if its reverse is present (`niwTtesolC`, `6202`), checks reading-order `xMin`, prints words in RTL line order (B11: at least 6 Latin runs, 5 numbers with units, a parenthesis, a sentence end next to a Latin run).
4. Look: `pdftoppm -r 150 -f N -l N -png main.pdf qa/tmp/heb` and read the PNG: first word of each paragraph at the right edge, bullets/numbers on the right, heading RTL in Rubik, punctuation and parentheses on the correct side, banner/footer not colliding (B2-B7, B10). Write "verified by eye"; pdftotext can order Hebrew wrongly and is not proof.
5. English body is LTR: `python -I qa/scripts/hebrew_pages.py --rtl-paragraph-check` flags non-Hebrew pages with a right-aligned block (C4, D2).
6. Fonts: `pdffonts -f N -l N main.pdf` lists Rubik only on the Hebrew page, no Playfair for Hebrew (B6, D5).

## Outputs
Finding blocks plus a corpus table `run | required | found as written | reverse found | read-order ok` and the list of Latin runs seen on the Hebrew page, one verdict each.
""" + FMT + r"""
Recurring-prone: B2-B5, B7, B9 (direction/spacing/glyph classes belong to the CLS or `hebrewpage`): recurring = yes, owner fix-se, name the construct and macro (`hebrewpage`, `\pct`, `\usd`, `\range`). A wrong Hebrew word or typo: recurring = no, owner writer-se.

## Success check
Criteria B1-B11, C4, D2, D3, D5 each pass, fail or are skipped with a reason; one summary line `checked n, pass p, fail f, skipped s`.
""")

w("qa-table",
  "Detector (report-only) for tables: caption above, label and reference, width within the text block, right-aligned numbers, header look, numbers equal to text and CSV, assumption labelling. Use after a build or when asked to check tables.",
  r"""
Checks every table's structure, order, alignment, width, caption, label, reference, numbers and assumption labelling.
""" + RULE + r"""
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
""" + FMT + r"""
Recurring-prone: TB2, TB3, TB4, TB7. A width or alignment defect in a table built with the CLS table macro is recurring = yes (name every table sharing the column spec), owner fix-se. A wrong number in one cell is recurring = no, owner writer-se.

## Success check
Criteria TB1-TB7 (and the table parts of D9, D16, D18) each pass, fail or are skipped with a reason; summary line present; the inventory covers every table in the PDF.
""")

w("qa-code",
  "Detector (report-only) for the code appendix and Python scripts: one pythonbox, margin, LTR, code equals the real file, JetBrains Mono only there, every script runs clean and reproduces its figure. Use after a build or when asked to check code.",
  r"""
Checks the one code box (K1-K4) and that every Python script runs and reproduces its figure (K5).
""" + RULE + r"""
## When to use
After a build with the code appendix, or after any change to `python/*.py` or `pythonbox`; part of `qa-super`.

## Inputs
`chapters/app*.tex`, `python/*.py`, `figures/`, `main.pdf`, `main.log`, `main.aux`.

## Procedure
1. `grep -rn "pythonbox" chapters/ main.tex`: exactly one use, in the appendix, taking a path to a `python/*.py` file; no pasted code in chapters (K1, K4).
2. Find the page from the `app:` label in `main.aux`; render at 150 dpi; look: ivory fill, hairline, line numbers, LTR, indentation kept, nothing past the right margin (K1, K2).
3. Margin by coordinates: `pdftotext -f p -l p -bbox main.pdf qa/tmp/code.html`; `python -I qa/scripts/bbox_margin.py` fails if `xMax` is past page width minus 3.0 cm.
4. Source equality: `pdftotext -layout -f p -l p main.pdf -` against the file; `python -I qa/scripts/code_diff.py <pdf-text> python/<file>.py` (ignores line numbers); any differing line is a finding (K4).
5. Fonts: `python -I qa/scripts/fonts_by_page.py main.pdf`: JetBrains Mono only on appendix pages; no mono font in `pdffonts figures/*.pdf` (K3, D4).
6. Run every script from the root with `python python/<name>.py`: exit 0, output file in `figures/` newer than the run start, no `findfont`/`Glyph ... missing`/`Warning` on stderr (K5, I8). Record stderr.
7. The figure made by the script named in the box is the figure the appendix claims.
8. No `C:\` path or secret in any script (FS4).

## Outputs
Finding blocks plus a script table: `script | exit | stderr lines | output file | in figures/ | used by figure`.
""" + FMT + r"""
Recurring-prone: K3, K1/K2 (the `pythonbox` macro: owner fix-se). The same fallback-glyph warning in two scripts is recurring: owner art-se for `ct_style.py`. A wrong constant in one script: recurring = no, owner art-se.

## Success check
K1-K5, I8, FS4 each pass, fail or are skipped with a reason; the script table lists every file in `python/`.
""")

w("qa-img",
  "Detector (report-only) for figures: file exists, caption/label/reference, 1:1 width, fonts, palette, contrast and grayscale, no overlap, honest against the data. Use after a build or when asked to check figures or graphs.",
  r"""
Checks every figure's file, framing, caption, label, reference, size, fonts, colours, contrast, grayscale and honesty against its data.
""" + RULE + r"""
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
""" + FMT + r"""
Recurring-prone: I3, I4, I5, I7, I8, I12, I13. A defect in `ct_style.py` is recurring: owner art-se for the style module, fix-se if the cause is the CLS figure environment or caption. One wrong axis or value: recurring = no, owner art-se.

## Success check
I1-I14, D6, D9, D12, D16, D18 (figure parts) each pass, fail or are skipped with a reason; the inventory has one row per figure in the PDF.
""")
