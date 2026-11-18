# QA skill specifications (qa-se, task QS1)

Version 1.0, 2026-11-18. Owner: qa-se. Input for **fix-se**, who owns `.claude/skills/` and turns each section into
`.claude/skills/<name>/SKILL.md` (frontmatter `name`, `description`, `version:`).
Criteria IDs refer to `qa/acceptance-criteria.md` **v1.3** (117 criteria). Assignment source: Table 2, "Recommended skills for quality control" (A4).

Run everything from `C:\biu\02`. Tools: poppler (`pdftotext`, `pdffonts`, `pdfinfo`, `pdftoppm`, `pdfimages`), `python` (never `python3`/`py`),
Git Bash for `grep`. Scratch output goes to `qa/tmp/` (never committed). The helper scripts named below live in `qa/scripts/`
(written by qa-se, listed at the end); a skill calls them with `python -I qa/scripts/<name>.py`.

**Detector rule (all skills):** a skill finds and reports. It never edits a deliverable, never fixes, never commits. A skill that
"would fix" something writes the finding and its owner instead.

---

## 0. Common to all eight skills

### 0.1 Finding format (one block per finding, from `qa/CLAUDE.md`)
```
### F-<skill>-<nn>  [blocker|major|minor]  <criterion ID(s)>
- Where:     <file>:<line>   | PDF page <printed page> (<pdf page index>)
- What:      <one sentence>
- Evidence:  <exact log line / command + output / "PNG qa/tmp/p-012.png: ...">
- Recurring: yes|no   (if yes: list EVERY place; owner = fix-se)
- Owner:     writer-se | art-se | fix-se | master-se
- Status:    open  (re-check mode sets: fixed in build <hash> | still open in build <hash>)
```
`<skill>` is the short name (`bidi`, `table`, `code`, `img`, `typeset`, `infra`, `clsver`, `super`). `<nn>` counts per report.
Page references always give both the printed page and the PDF page index, because front matter is roman (printed = PDF index - front-matter pages).

### 0.2 Sub-skill return value (to qa-super)
A sub-skill returns: (a) the list of finding blocks; (b) a one-line summary `checked <n> criteria, <p> pass, <f> fail, <s> skipped (reason)`;
(c) the build id (`git rev-parse --short HEAD` + whether the tree was clean). A criterion that could not be checked is `skipped` with a reason; **never silently passed**.

### 0.3 The recurring rule (iron rule support)
A finding is **recurring = yes** when any one of these holds:
1. The same criterion fails in **two or more places** (two pages, two chapters, two figures, two tables).
2. The cause is a **class** of CLS behaviour: spacing, RTL/LTR direction, fonts, caption style, table look, numbering, float placement, citation format, colors, banner/footer.
3. The same finding was reported in an earlier report and **reappears** after a fix or in a later build.
A recurring finding lists every place, names **fix-se** as owner, and **never proposes an edit to a chapter**. A one-off content error (a typo, one wrong number)
is `recurring: no` and goes to its content owner. Each skill's section lists the criteria that are *recurring-prone* (a first hit is checked against the whole document).

### 0.4 Severity
Taken from the criterion row. A skill may raise severity (never lower it) when the evidence is worse than the criterion assumes, and says why.

### 0.5 Build preconditions
Skills other than qa-super do **not** build. They read the artifacts of the build qa-super made: `main.pdf`, `main.log`, `main.blg`, `main.bcf`, `main.aux`, `main.toc`.
If an artifact is missing or older than the newest `.tex`/`.cls`/`.bib`, the skill stops with `BLOCKED: stale or missing build` and says which file.

---

## 1. qa-super: the orchestrator (the "QA manager of all QA families")
**Purpose.** Run the whole QA pass: build, call the seven other skills in a fixed order, do the checks that need human judgment, merge and de-duplicate the
findings, apply the recurring rule across skills, and write the one report master-se receives. Also runs **re-check mode** and the **final report** for the Definition of Done.

**Inputs.** The working tree at a commit; optional `--scope <criterion IDs | skill names>`; optional `--recheck qa/reports/NN-<topic>.md`; optional `--final`.

**Steps.**
1. Record the build id: `git rev-parse --short HEAD`; `git status --porcelain` (non-empty = report "dirty tree").
2. Build, from the root, capturing every exit code and `main.log`/`main.blg` copies in `qa/tmp/`:
   `lualatex --disable-installer main` → `biber main` → `lualatex --disable-installer main` → `lualatex --disable-installer main`.
   If any command exits non-zero, record BU1-BU2 as findings and still run the skills that need only sources (qa-infra, qa-cls-version).
3. Run the seven skills in this order: `qa-infra`, `qa-cls-version`, `qa-typeset`, `qa-BiDi`, `qa-table`, `qa-img`, `qa-code`.
4. Do the **judgment checks** that no script can do (read the chapters and the PDF pages, record the result as pass/finding):
   - D14, R13: classify every number in ch. 2, 5, 6, 7, 8, 9 and captions as sourced / derived / assumed (list the unclassified ones).
   - R5, R8, R9, R10, R12: open each source, trace each statistic (claim-trace table: claim, cite key, quoted sentence, page, number found yes/no), check legal sources are official.
   - D15, TB5, I9: competitor claims are sourced; table numbers equal text numbers; a graph matches its caption and data.
   - D16, D2: the editorial look and body language against PRD §5.3; the "break-even within" grep (see 5. below).
   - The book's 19.5 item 5 (a look at **every page** at a readable size) and item 6 (a human reads the summary): record the page list; item 6 is a request to master-se.
5. Greps owned by qa-super (PRD-specific traps): `grep -rniE "break-even within|breakeven within" chapters/` must be 0 (PRD MC-1); `grep -rniE "BIPA|Illinois" chapters/ references.bib` must be 0 (R12);
   `grep -rnE "\\\\(ils|usd|pct)\{" chapters/ | wc -l` is reported (macro use); the 53%/24.4%/24.52% figures never appear merged (CT-3): `grep -rn "24.4\|24.52" chapters/` listed for reading.
6. **Merge:** concatenate finding blocks, sort by severity then page, **de-duplicate** (same criterion + same location from two skills becomes one finding naming both), then apply 0.3 across the whole set (a problem two skills each saw once may be recurring).
7. Write `qa/reports/NN-<topic>.md` (NN = next free number in `qa/reports/`). Then `SendMessage` master-se `REPORT <scope>`: report path, counts by severity, blockers listed inline.
8. **Re-check mode (`--recheck`):** rebuild from scratch (delete `main.aux main.bbl main.toc main.bcf` first), re-run only the skills that own the listed criteria, and for each earlier finding write
   `fixed in build <hash>` or `still open in build <hash>`. A finding is never marked fixed on someone's word; it needs the new evidence line.
9. **Final mode (`--final`):** do a **fresh clone** build (`git clone . qa/tmp/clone && cd qa/tmp/clone`, same four commands) and run everything; run S9 (second build: same page count, same `pdftotext` per page, same `pdffonts` list, same warning counts);
   write `qa/reports/NN-final.md` with the DoD sign-off section: (a) 0 open blocker/major, each old finding marked "rechecked in build <hash>"; (b) the six 19.5 items with page lists; (c) sign-off lines for the human (name, date, pages; filled by the human, left blank by qa-se).

**Criteria checked.** All 117, by delegation. Directly: S5-S9, D2, D14, D15, D16, R5, R8-R10, R12, R13, TB5, I9, BU1-BU4, BU8-BU10, and the 19.5 checklist.

**Report format.** The report file:
```
# QA report NN: <topic>          build <hash> (clean|dirty)   date
## Summary      counts: blocker n, major n, minor n; skills run; criteria pass/fail/skipped
## Blockers     (inline list: ID, one line)
## Findings     (all blocks, sorted)
## Recurring    (table: problem | places | owner=fix-se | criterion IDs)
## Judgment checks   (claim-trace table, number-class list, page-by-page look list)
## Skipped      (criterion, reason)
## Re-check     (only in re-check/final mode)
```

**Marking recurring.** After the merge, qa-super builds the **Recurring** table. It promotes a finding to recurring if rule 0.3 applies across skills (for example qa-table sees a wide table and qa-typeset sees an overfull box on the same table: one recurring "table width" problem, owner fix-se).

---

## 2. qa-BiDi: Hebrew/English direction
**Purpose.** Prove the Hebrew executive-summary page is perfect BiDi and that no direction or glyph error exists elsewhere.

**Inputs.** `main.pdf`, `main.log`, `main.toc`, the Hebrew page source (path from `main.tex`), `qa/scripts/bidi_runs.txt` (the corpus list: Latin runs and number runs that must appear).

**Steps.**
1. Find the Hebrew pages: `python -I qa/scripts/hebrew_pages.py main.pdf` (per page, counts letters U+0590-U+05FF; prints the page list). Expect **exactly one**, in the front matter (B1, B8). Hebrew letters on any other page are findings unless on the documented exception list.
2. Missing glyphs: `grep -c "Missing character" main.log` must be 0 (B9; with `\tracinglostchars=3` it is an error `!` line, so also `grep -n "^!" main.log`).
3. Corpus: confirm the Hebrew page holds ≥ 6 Latin runs (ClosetTwin, TAM, SAM, SOM, B2B, AI), ≥ 5 numbers with units, 1 parenthesis, 1 sentence end next to a Latin run (B11):
   `pdftotext -f <N> -l <N> -bbox main.pdf qa/tmp/heb.html` then `python -I qa/scripts/bidi_bbox_check.py qa/tmp/heb.html qa/scripts/bidi_runs.txt`.
   The script (a) finds each required run **as written**, (b) fails if its reverse is present ("niwTtesolC", "6202", "IA"), (c) checks `xMin` of the Latin words and digits of one run increase in reading order, (d) prints the word list in right-to-left line order for the human check.
4. Render and look (B2-B6, B10): `pdftoppm -r 150 -f <N> -l <N> -png main.pdf qa/tmp/heb`. Read the PNG: the first word of each paragraph at the right edge; bullets and numbers on the right; heading RTL and in Rubik; punctuation at run boundaries on the correct side; parentheses not mirrored wrongly; banner/footer present and not colliding (B7). Record every Latin run seen, one line each, in the report. **State "verified by eye" for B2-B6: pdftotext can order Hebrew wrongly and is not proof.**
5. Cover and body direction: C4 (English cover is LTR); D2 (every other page LTR English): `python -I qa/scripts/hebrew_pages.py --rtl-paragraph-check` flags any non-Hebrew page whose text has a right-aligned block.
6. Fonts on the Hebrew page: `pdffonts -f <N> -l <N> main.pdf` must list Rubik only (plus no Playfair for Hebrew headings, B6/D5).

**Criteria checked.** B1-B11, C4, D2, D3, D5 (Hebrew part).

**Report format.** Common finding blocks, plus a **corpus table**: `run | required | found as written | reverse found | read-order ok`, plus the list "Latin runs seen on the Hebrew page" with the verdict per run.

**Marking recurring.** Recurring-prone: B2, B3, B4, B5, B7, B9 (all direction/spacing/glyph classes belong to the CLS or the `hebrewpage` environment). One reversed run in one place is still `recurring: yes` if the same construct (a number with `%`, a parenthesis at a run boundary) would occur wherever such text is typed; the finding names the construct and the CLS macro (`hebrewpage`, `\pct`, `\usd`), owner fix-se. A wrong Hebrew word or a typo is `recurring: no`, owner writer-se.

---

## 3. qa-table: tables
**Purpose.** Check every table's structure, order, alignment, width, caption, label, reference, numbers and assumption labeling.

**Inputs.** `chapters/*.tex`, `main.pdf`, `main.log`, `main.aux`, `main.lot`.

**Steps.**
1. Inventory: `grep -n "begin{table\|begin{tabular\|begin{tabularx\|\\\\caption\|\\\\label{tab:" chapters/*.tex`. Count tables (TB1: ≥ 1; target 5: vendor claims, pricing tiers, funnel/pilot, assumptions, risk mitigations); each table has `\caption` **before** the body (caption above) and a `\label{tab:...}` (TB2).
2. References: every `tab:` label in `main.aux` has a `\ref`/`\autoref` in the text (the label is cited at least once): `python -I qa/scripts/label_refs.py tab` (TB2). LOG: `grep -n "undefined" main.log` has no `tab:`.
3. Locate each table in the PDF: from `main.aux` (`\newlabel{tab:x}{{n}{page}...}`) get the page; render `pdftoppm -r 100 -f <p> -l <p> -png main.pdf qa/tmp/tab`.
4. Look (TB3, TB4, TB7): width within the text block (15.0 cm), no cell text past the margin, header row ivory with hairline, numbers **right-aligned** (or decimal-aligned), text left, same look in every table, a table is not split and no heading is alone above it.
5. Width by log: `grep -n "Overfull .hbox" main.log` lines that fall on table pages (parse with `python -I qa/scripts/overfull.py main.log --pages main.aux`) (TB3). Threshold **1 pt**.
6. Numbers: extract each table's numbers (`pdftotext -layout -f <p> -l <p> main.pdf -`) and compare with the same numbers in the text and, for the assumptions table, with `assumptions.csv` (TB5). Recompute totals (script `table_sums.py` reads the numbers qa-se marks).
7. Assumption labeling (TB6): financial tables have a caption or note containing "Assumption" and a class column (sourced / derived / assumed) with a source for each row (D14 feeds from this). Vendor table: caption "Vendor claims", blank cells read "not stated" (PRD ch. 3).
8. Column order: first column is the row label; units in the header, not repeated in each cell.

**Criteria checked.** TB1-TB7; partly D14 (table classes), D9 (≥ 1 table), D18 (header text contrast), D16 (≤ 1 table per page).

**Report format.** Common blocks, plus a **table inventory**: `label | caption (first 8 words) | chapter | PDF page | width ok | caption above | referenced | numbers ok`.

**Marking recurring.** Recurring-prone: TB2 (caption/label), TB3 (width), TB4 (alignment/look), TB7 (split table). A width or alignment defect in one table is `recurring: yes` if the table uses the CLS table macro and the cause could affect others (name every table that shares the column spec); owner fix-se. A wrong number in one cell (TB5) is `recurring: no`, owner writer-se.

---

## 4. qa-code: the Appendix A `pythonbox` and the Python scripts
**Purpose.** Check the one code box (K1-K4) and that every Python script runs and reproduces its figure (K5).

**Inputs.** `chapters/*appendix*.tex` (or wherever Appendix A is), `python/*.py`, `figures/`, `main.pdf`, `main.log`.

**Steps.**
1. Count boxes: `grep -rn "pythonbox" chapters/ main.tex` → exactly **1** use in Appendix A (K1); it takes a **path** to a `python/*.py` file and the chapter holds no pasted code (K4).
2. Find the page(s): from `main.aux` the page of the `app:` label; render `pdftoppm -r 150 -f <p> -l <p> -png main.pdf qa/tmp/code`. Check by eye (K1, K2): ivory fill, hairline, line numbers, LTR, indentation kept, no reversed punctuation, nothing past the right margin.
3. Margin by coordinates: `pdftotext -f <p> -l <p> -bbox main.pdf qa/tmp/code.html`; the script `bbox_margin.py` fails if any word has `xMax` > right margin (page width minus 3.0 cm) (K1).
4. Source equality (K4): `pdftotext -layout -f <p> -l <p> main.pdf -` vs the file named in the `pythonbox` argument; `python -I qa/scripts/code_diff.py <pdf-text> python/<file>.py` ignores line numbers and compares the shown range; any differing line is a finding.
5. Fonts (K3, D4): `python -I qa/scripts/fonts_by_page.py main.pdf` lists fonts per page; JetBrains Mono must appear **only** on the Appendix A page(s); any other monospace font anywhere is a failure; figure PDFs have no mono font (`pdffonts figures/*.pdf`).
6. Run every script (K5): for each `python/*.py` run `python python/<name>.py` from the root; exit code 0; the output file named in the script exists in `figures/` and is newer than the run start; **no `findfont`, `Glyph ... missing`, or `Warning` line on stderr** (I8). Record the stderr.
7. Reproduction (K4): the figure produced by the script named in the box is the figure the appendix claims (same file name; compare `pdftotext` of the figure PDF with the caption's description).
8. License/safety: no hard-coded absolute path (`C:\`) or secret in the scripts (FS4).

**Criteria checked.** K1-K5, R-25 (PRD), D4/K3 (monospace), I8 (script warnings), FS4 (paths in `.py`).

**Report format.** Common blocks, plus a **script table**: `script | exit | stderr lines | output file | in figures/ | used by figure`.

**Marking recurring.** Recurring-prone: K3 (a mono font leaking onto another page is a CLS font-switch problem), K1/K2 (box margin, direction: the `pythonbox` macro). A script warning that appears in two scripts (the same fallback glyph) is recurring → owner art-se for `ct_style.py`, not for each script; a wrong constant in one script is `recurring: no`, owner art-se. The pythonbox look/direction/margin is owner fix-se.

---

## 5. qa-img: figures and images
**Purpose.** Check every figure's file, framing, caption, label, reference, size, fonts, colors, contrast, grayscale and honesty against its data.

**Inputs.** `figures/*` (PDF and TikZ `.tex`), `python/*.py`, `chapters/*.tex`, `main.pdf`, `main.aux`, `main.lof`.

**Steps.**
1. Inventory (I1, D9, D12): `grep -n "begin{figure\|includegraphics\|\\\\input{figures" chapters/*.tex`; expected 7 figures (F1-F7 of PRD §5.4), ≥ 1 Python graph and ≥ 1 TikZ diagram; ch. 1 uses stat cards (not figures). Every file exists: `grep -i "not found\|File .* not found" main.log` is 0 (I2). **No internet images:** no `http` in an `\includegraphics`; every figure file maps to a script in `python/` or a TikZ source in `figures/` (I6, D12).
2. Caption, label, reference (I3, I10): each figure has `\caption` and `\label{fig:...}`, is `\ref`-ed in the text (`label_refs.py fig`), and the sentence explaining it exists; first mention on the same or next page.
3. Size (I4): figures sit at **1:1 within 15.0 cm** (PRD: fixed canvas = text width); check `\includegraphics[width=...]` is `\textwidth` or absent, never a scale factor: `grep -n "scale=\|width=" chapters/*.tex`; for a rendered page, measure the figure bbox with `pdfimages -list` / the page PNG.
4. Fonts (I8): `pdffonts figures/*.pdf` lists only Rubik/Playfair, all embedded, **none `Type 3`**; run each script (qa-code does) and read stderr for fallback.
5. Palette (I7, D6): `grep -noE "#[0-9A-Fa-f]{6}" python/*.py figures/*.tex` → only {111111, F7F3EE, A47864, E8C6C0, 6B4B3D, D3BBAE, E3DCD4, 6F6862}; mixed `\definecolor`/`rgb` values also listed.
6. Contrast (D18) and grayscale (I12): render each figure page `pdftoppm -r 150`; `python -I qa/scripts/contrast_colors.py <png> --text` computes the WCAG ratio of the text colors against their background (≥ 4.5:1 small, ≥ 3:1 large/graphics); `--gray` converts to grayscale and reports the luminance gap between series (≥ 20% or a direct label).
7. Look (I5, I11): zoom `-r 150`: labels not overlapping, text ≥ 8 pt at print size, axes/legend complete, understandable without the text, no cropped edge (I2), one y-axis, ≤ 4 series (D16).
8. Honesty against data (I9, I14): compare plotted values with the text and with `assumptions.csv`/`python/model.py` output; titles/axes/units equal the text; financial charts say "Assumption"; **F5 marks the first profitable year and the peak deficit and shows nothing past Y5**; F6 marks the retailer break-even ρ = 6.03% / 4.52%; **F2's axes are two columns of the ch. 3 vendor table** and each vendor's position equals its table cells; F1 is "not to scale" with one year per label.
9. Page share (I13): figures cover ≤ 50% of the text block on every content page; ≤ 1 figure per page (D16).

**Criteria checked.** I1-I14, D6 (figure part), D9, D12, D16 (figure part), D18 (figure part), R-10 (PRD).

**Report format.** Common blocks, plus a **figure inventory**: `fig | file | tool | ch. | PDF page | 1:1 | fonts ok | palette ok | contrast ok | gray ok | referenced | data checked`.

**Marking recurring.** Recurring-prone: I3, I4, I5 (when the same overlap/scale appears in two figures), I7, I8, I12, I13. A defect in `ct_style.py` (fonts, palette, canvas) is recurring by construction → owner art-se for the style module, fix-se if the cause is the CLS figure environment or caption. A single mislabeled axis or wrong value in one figure is `recurring: no`, owner art-se.

---

## 6. qa-typeset: compilation warnings and pagination
**Purpose.** Turn the TeX log and the rendered pages into a check of overfull/underfull boxes, page count, page budget, and the layout rules of book ch. 19.4.

**Inputs.** `main.log`, `main.toc`, `main.aux`, `main.pdf`.

**Steps.**
1. Overfull (BU5, C5, L9): `python -I qa/scripts/overfull.py main.log` parses every `Overfull \hbox (Xpt too wide)` and `Overfull \vbox`, with the page number (via `main.aux`/`\shipout` order) and the source line from the log. **Fail if X > 1.0 pt.** Print the full table, not only failures. The book allows 5 pt; our rule is 1 pt (Q-4).
2. Underfull (BU6): `grep -c "Underfull" main.log` and badness 10000 lines in body text, listed with pages.
3. Other build warnings (BU2-BU4, BU7, BU8): `grep -c "^!" main.log`; `grep -c "undefined" main.log`; `grep -c "Missing character" main.log`; `grep -i "rerun" main.log` (empty on the last pass); `grep -E "ERROR|WARN" main.blg`. A float that cannot be placed: `grep -n "Float too large\|too many unprocessed floats" main.log`.
4. Page count and budget (D1, D17, BU9): `pdfinfo main.pdf | grep Pages`; chapter first pages from `main.toc` (printed pages) and the roman/arabic split. Content = ch. 1 through ch. 10, references and Appendix A excluded. `python -I qa/scripts/page_stats.py` prints per chapter: first page, pages, and checks the budget table of D17 (±1 page, conclusion exactly 1, **total ≥ 25 hard**). Print the table.
5. Per-page statistics (L2, L4): `python -I qa/scripts/page_stats.py --pages` runs `pdftotext -layout -f p -l p` for every page and prints characters, words, the last non-empty line and the first line. Flags: a page with < 600 characters that is not a chapter's last page or the one-page conclusion (L4); a last non-empty line that matches a heading pattern (large font via `-bbox` height or the heading numbering) (L2 orphan heading); a one-word last line (L5).
6. Look at every page (L1, L3, L7, L8, 19.5 item 5): `pdftoppm -r 80 -png main.pdf qa/tmp/p` then read each PNG at a size one can read, recording the page list: new page per chapter, TOC, references and Hebrew page (L1); no table/figure/box split by a page break (L3); banner and footer on every page except the cover, not overlapping (L7); page numbers continuous and equal to the TOC (L8); text inside the margins (L9); a TOC with every chapter and section (L6).
7. Airy rule (D16, I13): margins 3.0 cm measured on a rendered page (`bbox_margin.py --margins`); ≤ 1 figure + 1 table per page; no content page more than half figure.
8. Cover (C2, C3, C5): page 1 has no number or footer; roman front matter, arabic from chapter 1: `grep -n "frontmatter\|mainmatter" main.tex`.

**Criteria checked.** BU2-BU10, L1-L9, D1, D17, D16 (layout part), C2, C3, C5, I10, TB7, R7, R-20 (PRD).

**Report format.** Common blocks, plus three tables: **overfull/underfull list** (`kind | amount | page | source line`), **page budget** (`chapter | budget | actual | accept range | verdict`), **page stats** (`page | chars | last line | flags`).

**Marking recurring.** Recurring-prone: BU5, L1, L2, L3, L4, L7, L9. Two overfull boxes of the same kind (a long URL in the bibliography, a table wider than the block) are one recurring finding listing all lines; owner fix-se (CLS: URL breaking, `\FloatBarrier`, `\needspace`, table width). A short page caused by one chapter's content volume is `recurring: no`, owner writer-se, unless it appears in ≥ 2 chapters (then it is a CLS float/spacing problem).

---

## 7. qa-infra: project structure, sources and reproducibility
**Purpose.** Check the repository: required files, ownership folders, paths, fonts provenance, bibliography mechanics, the ID-number rule, repo contents for submission, and reproducibility from a fresh clone.

**Inputs.** The git working tree and history, `references.bib`, `main.bcf`, `main.blg`, `fonts/`, `.claude/skills/`, `README.md`, `.gitignore`, `PRD.md`.

**Steps.**
1. Required files (FS1, S4): `ls main.tex closettwin.cls PRD.md PLAN.md TODO.md README.md references.bib`; `ls chapters/` has 10 chapter files `NN-*.tex` + the Hebrew page file; `ls figures python fonts`.
2. Chapter structure (FS2, FS3, T5): `grep -n "\\\\input\|\\\\include" main.tex` shows each chapter; `grep -nE "writer/|art/|qa/|fix/" main.tex chapters/*.tex` is 0; chapters contain no `\documentclass`, `\usepackage`, `\begin{document}`.
3. Portability (FS4): `grep -rnE "C:\\\\|\\\\Users|/Users/" --include=*.tex --include=*.cls --include=*.py --include=*.bib .` is 0.
4. Fonts provenance (FS5, R-07): `ls fonts/` contains Playfair Display, Rubik, JetBrains Mono, their OFL texts and `SOURCES.md`; `sha256sum` of the Playfair Display and JetBrains Mono files equals the hashes in `SOURCES.md`; `grep -n "Path" closettwin.cls` shows relative loading.
5. **No ID numbers (C6):** the four greps of C6 over files, grouped forms, **git history** (`git log --all -p`) and `pdftotext main.pdf -` (excluding 875523402); `pdfinfo main.pdf` metadata holds no ID. Any hit is a **blocker**; the finding reports file:line (or commit) but **never prints the number itself** (the report is committed): it prints the first 2 digits and `*******`.
6. Bibliography mechanics (R1-R4, R6, R7, R11): `grep -ci "undefined citation\|didn't find a database" main.log main.blg` is 0; `python -I qa/scripts/bib_vs_cited.py main.bcf references.bib` prints (a) cited keys missing from the bib, (b) bib keys **never cited** (R11, must be empty), (c) entries missing author/title/year/venue/DOI-or-URL (R6), (d) `@online` entries without `urldate` (R11), (e) the count (≥ 12 real, PRD: 29); `pdftotext main.pdf - | grep -nE "\[[A-Za-z]"` is 0 (no key printed instead of a number, R2); `grep -n "biblatex" closettwin.cls` shows `style=ieee` (R3).
7. Link check (R5 mechanical half): for each `doi`/`url` in the bib: `curl -sIL -o /dev/null -w "%{http_code}" https://doi.org/<doi>` (200/301/302 accepted; others listed). Resolving is necessary, not sufficient: the metadata match and the claim trace stay with qa-super (R5, R10).
8. Skills (S2, S3): `ls .claude/skills/` has the 8 folders; each `SKILL.md` has frontmatter `name:`, `description:`, `version:`; README lists the skills used and the build commands and the MiKTeX package list with versions (FS8, RT-F2).
9. Repository contents (FS7, S1, S4): `git ls-files` includes `main.pdf`, `.bib`, `.cls`, `.tex`, `figures/`, `python/`, `fonts/`, `.claude/skills/`; `.gitignore` excludes `*.aux *.log *.bbl *.blg *.bcf *.run.xml *.toc *.out *.lof *.lot` and `qa/tmp/` but not `main.pdf`; `git status --porcelain` is empty at the end.
10. **Reproducibility (FS6, S9, R-16):** `git clone . qa/tmp/clone`; in the clone run the four build commands; compare with the original build: `pdfinfo` page count, `pdftotext` per page (`diff`), `pdffonts` list, error/warning counts. Equal = pass. Byte identity is **not** required.
11. Prompts and process (S5, S6): `ls prompts/` holds the requirement-complete agent prompt; compare `fix/CHANGELOG.md` rows with the recurring problems of the QA reports (S6).

**Criteria checked.** FS1-FS8, S1-S4, S5, S6, S9, C6, R1-R4, R6, R7, R11, T5, D12 (no internet files), R-07, R-16, R-17, R-18, R-23, R-24 (PRD).

**Report format.** Common blocks, plus a **file checklist** (`path | required | present`), a **bib table** (`key | cited | complete | urldate | link status`), and the **reproducibility table** (`item | original | clone | equal`).

**Marking recurring.** Recurring-prone: FS3, FS4 (a path or an agent-folder reference in one chapter likely occurs elsewhere), R2/R3 (citation format), T5 (chapters with formatting). Missing or malformed entries in the bib are `recurring: no` (owner writer-se); a wrong biblatex option that prints keys, or a missing `.gitignore` rule, is recurring → fix-se/master-se per the ownership table. An ID found in history cannot be fixed by an edit: report as blocker, owner master-se (history rewrite is a decision for master-se and the user).

---

## 8. qa-cls-version: template version discipline
**Purpose.** Check that the CLS is the one `main.tex` uses, that its version is the logged version, that every CLS/skill change has a CHANGELOG row, and that chapters hold no manual formatting that the CLS should own (the iron rule).

**Inputs.** `closettwin.cls`, `main.tex`, `main.log`, `fix/CHANGELOG.md`, `.claude/skills/*/SKILL.md`, `chapters/*.tex`, `git log`.

**Steps.**
1. Class in use (T1): `grep -n "documentclass" main.tex` is `\documentclass{closettwin}` (book-based; no `article/report/book` directly); the file exists.
2. Version (T2): `grep -n "ProvidesClass" closettwin.cls` returns `\ProvidesClass{closettwin}[YYYY/MM/DD vX.Y ...]`; `grep -i "closettwin" main.log` prints the **same string**; the newest row of `fix/CHANGELOG.md` has the same `vX.Y` and a date ≥ the class date. A mismatch in any of the three is a finding. Also check the CLS minimum-package dates (`\NeedsTeXFormat`, `\RequirePackage[date]`) exist (RT-F2).
3. Change discipline (T6, S6): `git log --format="%h %ad %s" --date=short -- closettwin.cls` — every commit that touched the CLS after the first has a CHANGELOG row of the same date (date, version, problem, root cause, fix, reporter); `git diff <prev>..HEAD -- closettwin.cls | grep "ProvidesClass"` shows the version was **bumped**. For each skill: `git log -- .claude/skills/<name>/SKILL.md` vs its frontmatter `version:`.
4. No manual formatting in chapters (T3): `grep -nE "\\\\(vspace|hspace|newpage|clearpage|pagebreak|fontsize|selectfont|setmainfont|setlength|raggedright|centering|bfseries|itshape)\b" chapters/*.tex` and `grep -nE "\\\\(textcolor|color)\{" chapters/*.tex` (raw colors) and `grep -nE "\\\\definecolor" chapters/*.tex`; allowed: `\needspace` and the CLS macros (`\pct`, `\usd`, `\ils`, `\sourced`, `\derived`, `\assumed`, `statcard`, `pullquote`, `pythonbox`, `hebrewpage`). Report **each hit with file:line**.
5. Recurrence vs fixes (S6): read the previous QA reports in `qa/reports/`; for each recurring finding, check a CHANGELOG row exists that references it and its version is in the current CLS; if the same finding **reappears** after its row, report "fix did not hold" (recurring: yes, third time → escalate to master-se).
6. Hand patches (iron rule): `git log -p -- chapters/ | grep -E "^\+.*\\\\(vspace|hspace|newpage|clearpage)"` over the history shows patches that went into the text.

**Criteria checked.** T1, T2, T3, T4 (undefined commands, from the log), T5, T6, S6, R-05, R-19 (PRD).

**Report format.** Common blocks, plus the **version triple** table: `source | string | date | match` (class file, build log, CHANGELOG, each skill) and the **manual-formatting hit list** (`file:line | command | allowed?`).

**Marking recurring.** T3 hits are `recurring: yes` by definition (a formatting command in a chapter means the CLS lacks a macro): the finding names the missing CLS capability (for example "no macro for a tighter list"), owner fix-se, and says explicitly *do not patch the text*. T2/T6 mismatches are `recurring: no` for that single release, owner fix-se.

---

## Helper scripts qa-se will write (in `qa/scripts/`; skills call them)
| Script | Used by | What it does |
|--------|---------|--------------|
| `hebrew_pages.py` | qa-BiDi | per-page Hebrew-letter count, page list, RTL-block check on other pages |
| `bidi_bbox_check.py` + `bidi_runs.txt` | qa-BiDi | required Latin/number runs present as written, reverses absent, `xMin` reading order |
| `fonts_by_page.py` | qa-code, qa-BiDi, qa-super | `pdffonts` per page; whitelist, LM Math only on `eq:` pages, JetBrains Mono only on Appendix A |
| `overfull.py` | qa-typeset, qa-table | parse `Overfull/Underfull` with pages; fail > 1.0 pt |
| `page_stats.py` | qa-typeset | per-page chars, last line, flags; chapter budget table (D17); content total (D1) |
| `bbox_margin.py` | qa-code, qa-typeset | `xMax`/margins from `pdftotext -bbox` |
| `label_refs.py` | qa-table, qa-img | `tab:`/`fig:` labels vs `\ref` use |
| `contrast_colors.py` | qa-img, qa-table | WCAG ratio of text colors; grayscale luminance gap; page-corner color (D19) |
| `code_diff.py` | qa-code | PDF code text vs the `python/` file |
| `bib_vs_cited.py` | qa-infra | cited vs bib keys, incomplete entries, missing `urldate` |
| `id_scan.py` | qa-infra | the C6 scan over files, history and PDF text, masked output |
| `table_sums.py` | qa-table | recompute totals of marked tables |

Each script exits non-zero on a failing check and prints a one-line summary plus the evidence lines, so a skill can paste them into a finding.
Open for master-se: fix-se owns `.claude/skills/`; qa-se owns `qa/scripts/`. Skills reference scripts by path, so a script change is a qa-se change, a skill change is a fix-se change.
