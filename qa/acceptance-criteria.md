# Acceptance criteria: ClosetTwin business plan (qa-se, task Q1)

Version 1.3, 2026-11-18 (v1.1 applied master-se's answers Q-1..Q-5; v1.2 applied red-team RT-Q1..Q8 and the other reviewers' additions; v1.3 applies the user's answers UD-1..UD-8 of PRD v2.0; see "Decisions" at the end). Owner: qa-se. Not a deliverable. master-se merges it into `PRD.md`.

Sources (binding order): (1) assignment PDF `ref/BIU26-27-A-ex02-pdf-via-LaTex-print.pdf` ("Assignment", pages A1-A5);
(2) fixed decisions in `prompts/03-expert-committee.md`; (3) course book `ref/preparation-report-book.pdf`, Part B, ch. 19
("Quality control: a checklist for a ready document"). Book page numbers are the **printed** numbers (PDF page = printed + 14):
ch. 19 is printed pp. 76-79. The assignment's skills table is "Table 2 on A4".

How to read the tables: **Sev** = severity if the criterion fails (`blocker` / `major` / `minor`).
**Check** = how qa-se verifies it. Build commands run from `C:\biu\02`.
`LOG` = `main.log`. `PDFPAGE n` = render page n to PNG (`pdftoppm -r 80 -f n -l n -png main.pdf qa/tmp/p`) and look at it.
Any criterion marked **recurring-prone** that fails goes to fix-se (CLS or skill) under the iron rule, never to the chapter text.

Families use the nine names of the book's **Table 19.1 "Families of checks"** (printed p. 77): Template, Cover page,
Directionality, Tables, Images, Code, Layout (ch. 19.4 rules, p. 78), Sources, File structure.
Three extra groups cover what the book does not: **B** Build, **D** our fixed decisions, **S** assignment submission/process.

---

## Family 1: Template (תבנית) - book p. 77: "outdated version, no manual changes"
Failure sign in the book: "commands that are not recognised". Also assignment §3.2 (a custom `.cls` is mandatory) and the
iron rule (A3).

| ID | Criterion | Target | Check | Sev |
|----|-----------|--------|-------|-----|
| T1 | Project uses one custom class file | `main.tex` starts with `\documentclass{<our cls>}`; the file exists in the root; no standard `article/report/book` | `grep -n documentclass main.tex`; `ls *.cls` | blocker |
| T2 | CLS version is current and logged | `\ProvidesClass` has a version `vX.Y`; same version is the newest row in `fix/CHANGELOG.md`; LOG prints the same string | `grep ProvidesClass *.cls`; `grep -i "<clsname>" main.log`; read CHANGELOG | major |
| T3 | No manual formatting overrides in chapters (the iron rule) | 0 hits for `\vspace`, `\hspace`, `\newpage`, `\clearpage`, `\fontsize`, `\selectfont`, `\setmainfont`, `\color{`/`\textcolor{` with raw hex, `\setlength`, `\raggedright` in `chapters/*.tex` (allowed: `\needspace` and CLS macros) | `grep -nE "\\\\(vspace\|hspace\|newpage\|clearpage\|fontsize\|selectfont\|setmainfont\|setlength\|raggedright)" chapters/*.tex` | major, recurring |
| T4 | No undefined commands | LOG has 0 lines `Undefined control sequence` | `grep -c "Undefined control sequence" main.log` | blocker |
| T5 | Chapter files are only content | each `chapters/*.tex` has no `\documentclass`, `\usepackage`, `\begin{document}` | grep | major |
| T6 | Every CLS/skill fix is logged (assignment A3: "fix the generator, not the text") | each change to the CLS between two commits adds a CHANGELOG row (date, version, problem, root cause, fix, reporter) | `git log --stat -- *.cls fix/CHANGELOG.md` | major |

## Family 2: Cover page (דף שער) - book p. 77: "no page number, direction, without a number"
| ID | Criterion | Target | Check | Sev |
|----|-----------|--------|-------|-----|
| C1 | **Ivory cover** is page 1 of the PDF (PRD R-22, UD-2, UD-5) | ivory #F7F3EE background; title "ClosetTwin", subtitle, **Hila Abay, Shirel Giladi**, group code **sg00ha11**, course **Generative AI for Management (875523402)**, lecturer **Dr. Yoram Segal**, date; palette-only colors; no footer or page number | PDFPAGE 1 | blocker |
| C2 | Cover carries no page number and no running footer number | no digit in the footer area of PDF page 1 | PDFPAGE 1; `pdftotext -f 1 -l 1 -layout main.pdf -` shows no stray number | minor, recurring |
| C3 | Front matter numbering is separate from the content | front matter (cover, TOC, Hebrew executive summary) in roman or unnumbered; content starts at arabic 1 | PDFPAGE of first content page; `grep -n "frontmatter\|mainmatter" main.tex` | major |
| C4 | Cover direction is right for its language | English cover is LTR; the title is not reversed | PDFPAGE 1 | major |
| C5 | Cover contains no overfull line and no text outside the margins | LOG has no overfull on page 1; visual margin check | PDFPAGE 1 | minor |
| C6 | **No personal ID number anywhere** (UD-5, R-22; the repo is public) | 0 nine-digit numbers in the repo files, in the **git history**, and in the PDF text, except the course code **875523402**. Also 0 hits for the grouped form `ddd-ddd-ddd` or `ddd ddd ddd` | `grep -rnIE "\b[0-9]{9}\b" --exclude-dir=.git . \| grep -v 875523402`; `grep -rnIE "[0-9]{3}[- ][0-9]{3}[- ][0-9]{3}" --exclude-dir=.git .`; `git log --all -p \| grep -E "\b[0-9]{9}\b" \| grep -v 875523402`; `pdftotext main.pdf - \| grep -E "\b[0-9]{9}\b" \| grep -v 875523402`; also check `main.pdf` metadata with `pdfinfo` (Author/Title/Keywords hold no ID) | blocker |

## Family 3: Directionality (כיווניות) - book p. 77: "mixed line", ch. 14 (printed pp. 44-50)
The book's three levels of direction (ch. 14.2-14.3) and "four hints that break without being read" (14.5).

| ID | Criterion | Target | Check | Sev |
|----|-----------|--------|-------|-----|
| B1 | Exactly one Hebrew page (RTL executive summary), a **full page**, in the **front matter** (roman-numbered, not counted in the 25) | one page whose paragraphs are RTL; the rest of the document is LTR | PDFPAGE (the Hebrew page); `pdftotext` per page, count pages containing U+05D0-U+05EA | blocker |
| B2 | Hebrew text is not reversed | the first word of each Hebrew paragraph is on the right edge; reading right to left gives the intended text | PDFPAGE visual. Mark as **verified by eye only**: `pdftotext` can order Hebrew wrongly | blocker |
| B3 | English brand names and numbers inside Hebrew keep LTR order | "ClosetTwin", "TAM/SAM/SOM", "B2B", "AI", "2026", "$", "%", "12.5%" read left-to-right inside the RTL line; digits are never reversed ("2026" not "6202") | PDFPAGE zoom `-r 150` on every Latin run; list each run in the report; plus the machine check of B11 | blocker |
| B4 | Punctuation and parentheses at the run boundary are on the correct side | a period ends on the left of the last Hebrew word; `( )` and quotes are not mirrored wrongly; "(ClosetTwin)" opens/closes correctly | PDFPAGE zoom | major |
| B5 | Hebrew list, bullets and numbering are on the right | bullets at the right margin; numbers are on the right | PDFPAGE | major, recurring |
| B6 | Hebrew section heading is RTL and in Rubik (not Playfair) | heading right-aligned, Rubik | PDFPAGE; `pdffonts` (F-rule D4) | major |
| B7 | Page furniture of the Hebrew page is correct | banner and footer present; page number and footer text do not collide; direction of footer text matches its language | PDFPAGE | major, recurring |
| B8 | No Hebrew outside the Hebrew page, except one-word Hebrew in figures if art-se uses it, and then it renders right | `pdftotext` per page: Hebrew letters only on the Hebrew page (and a documented exception list) | script in `qa/` loops pages | major |
| B9 | No missing glyphs | LOG has 0 lines `Missing character` | `grep -c "Missing character" main.log` | blocker, recurring |
| B10 | Hebrew page is perfect BiDi **in the cross-reference and citation cases** (a `\cite`, a `\ref`, a number with a unit) if any occur there | if used: a citation number "[3]" stays "[3]" and sits at the logical place | PDFPAGE zoom | major |
| B11 | **BiDi test corpus and machine check** (RT-Q3) | the Hebrew page contains at least **6 Latin runs** (ClosetTwin, TAM, SAM, SOM, B2B, AI), **5 numbers with a unit** (%, $/USD, years), **1 parenthesis** and **1 sentence end next to a Latin run**. `pdftotext -bbox` of that page contains each Latin run exactly as written and contains **none** of its reverses ("niwTtesolC", "6202", "IA") | `pdftotext -f N -l N -bbox main.pdf out.html`; script in `qa/` greps the 6 runs and their reverses; then the visual check of B2-B4 | blocker |

## Family 4: Tables (טבלאות) - book p. 77: "column order, alignment, width, caption"; ch. 11.1 / 16.5 rules
Book p. 78: "table width up to 12.4 cm"; "a table that is too wide (11pt table) overflows". The book's "Iron Rule of Figures and Tables" is ch. 11.1 (printed p. 33).

| ID | Criterion | Target | Check | Sev |
|----|-----------|--------|-------|-----|
| TB1 | At least 1 table | 1 or more `table` environments; the report is expected to carry about 5-8 (market, competition, pricing, financial, risks) | `grep -c "begin{table" chapters/*.tex` | blocker (0), minor (<4) |
| TB2 | Every table has a caption **above** it and a `\label`, and is referenced in the text | caption above; each label is `\ref`-ed at least once, before or near the table | `grep -n "caption\|label" chapters/*.tex`; LOG has no `Reference ... undefined` | major, recurring |
| TB3 | Width | each table is at most the text width; our own cap is 12.4 cm (book) for narrow tables, never beyond the margins | PDFPAGE; LOG overfull `hbox` on table lines | major, recurring |
| TB4 | Columns align by type | text left, numbers right (or decimal-aligned); header in bold, palette color; same look in every table | PDFPAGE | minor, recurring |
| TB5 | Numeric consistency | each number in a table equals the same number in the text; totals add up (checked by hand/script) | read; arithmetic check | major |
| TB6 | Financial table is labeled as assumptions | the caption or a note contains the word "assumption(s)" and the source of each assumption | grep "ssumption" near each financial table | major |
| TB7 | A table is never split with a heading at the page bottom | no table starts in the last 3 lines of a page and breaks; no heading alone (see L2) | PDFPAGE every table page | major |

## Family 5: Images (תמונות) - book p. 77: "framing, borders, caption"; failure: "image missing or cropped"
Book: figure width up to **12.5 cm**, no overlapping labels, Hebrew caption/`\label`, one sentence in the text explaining it (prompt 5, p. 73);
"a figure that is not mentioned in the text" is a defect (prompt 8, p. 74).

| ID | Criterion | Target | Check | Sev |
|----|-----------|--------|-------|-----|
| I1 | At least 1 figure (>= 1 Python graph **and** >= 1 TikZ diagram); target 9 (PRD §5.4). Chapter 1 may use **stat cards** instead of a chart (allowed; the cards are not counted as figures) | `\includegraphics` or TikZ `figure` count | `grep -c "begin{figure" chapters/*.tex` | blocker (0), minor (<4) |
| I2 | Every figure file exists and is not cropped | LOG has 0 `File ... not found`; PNG/PDF shows full axes and legend | `grep -i "not found" main.log`; PDFPAGE | blocker |
| I3 | Caption and label; each figure is referenced in the text, and the text sentence says what we learn | `\caption` + `\label`; `\ref` exists | grep; LOG no undefined ref | major, recurring |
| I4 | Width | at most 12.5 cm (book rule) and inside the margins | read `\includegraphics[width=...]` or measure on page | major, recurring |
| I5 | No overlapping labels; text in a figure is readable | font in figure at least 8 pt at print size; labels do not touch | PDFPAGE zoom `-r 150` | major |
| I6 | No internet images; no photo files not made by us | all figures are in `figures/`, made by `python/` scripts or TikZ; each script exists | `ls figures python`; every figure file maps to a script/TikZ source | blocker |
| I7 | Graph colors are from the palette only | ink #111111, ivory #F7F3EE, mocha #A47864, powder pink #E8C6C0 (and tints of them); 0 off-palette hex in `python/*.py` | `grep -noE "#[0-9A-Fa-f]{6}" python/*.py figures/*.tex` and compare with the 4-value list | major, recurring |
| I8 | Figure fonts (RT-Q4): Python graphs use only Rubik/Playfair, **TrueType embedded (`pdf.fonttype = 42`, no Type 3)**, and **no fallback** (no `findfont` or `Glyph ... missing` warning when the script runs; no DejaVu for "→ ≈ × −") | run each script and capture stderr; `pdffonts figures/*.pdf` lists only Rubik/Playfair, none `Type 3` | blocker, recurring |
| I9 | A graph matches its caption and its data | title, axis labels, units and values are the same as the text; financial series are labeled "assumption" | read; compare with text | major |
| I10 | Figure is not far from its first mention | on the same or the next page | PDFPAGE | minor |
| I11 | Alt-reading test: every figure is understandable without the text | axis labels + units + legend | PDFPAGE | minor |
| I12 | Grayscale and contrast of figures (RT-Q5) | each figure converted to grayscale: any two series differ by >= 20% luminance **or** are direct-labeled; graphic elements >= 3:1 against the background | `pdftoppm` + Python/PIL grayscale script in `qa/`; visual | major, recurring |
| I13 | No content page is more than half figure | on every content page the figures cover <= 50% of the text block area (so each page keeps text) | PDFPAGE; measure image bbox with `pdfimages -list`/page render | major |
| I14 | Positioning-map axes come from the verified vendor-table columns | each axis of the ch. 3 map is a column of the ch. 3 vendor comparison table (for example "scan: yes/no", "B2B: yes/no"), the vendor positions equal the table cells, and the caption says the axes are qualitative | compare the figure with the table, vendor by vendor | major |

## Family 6: Code (קוד) - book p. 77: "background, direction, indentation"; failure: "unclear background"; assignment `qa-code` = "background and pythonbox"
PRD R-25 / UD-4: the report has **one** code box, the `pythonbox` in **Appendix A** ("How our charts are made"). K1-K4 cover it. JetBrains Mono is allowed **only** there.

| ID | Criterion | Target | Check | Sev |
|----|-----------|--------|-------|-----|
| K1 | `pythonbox` has an **ivory fill with a hairline**, **line numbers**, and **nothing past the margin** | Appendix A contains exactly **1** `pythonbox`; ivory #F7F3EE fill with a 0.4 pt mocha-pale hairline; line numbers visible; every line ends inside the text block (15.0 cm); no overfull `hbox` on its lines | PDFPAGE of the Appendix A page(s); `grep -c "begin{pythonbox\|pythonbox{" chapters/*.tex main.tex` = 1; overfull lines in LOG on those pages; `pdftotext -bbox` max xMax <= right margin | major |
| K2 | Code is **LTR**, monospace, and keeps its indentation | the code reads left to right, indentation preserved, no reversed punctuation (`)` `:` `#`), no Hebrew inside | PDFPAGE zoom; `pdftotext -layout` of the page | major |
| K3 | **JetBrains Mono only on the code-box page(s)** (UD-4; reverses the v1.1 "no monospace" rule) | `pdffonts -f N -l N` on each page: JetBrains Mono appears **only** on the Appendix A page(s) and on no other page; any other monospace font (Courier, Latin Modern Mono, NimbusMono, DejaVu Sans Mono, Consolas...) anywhere = failure. URLs stay in Rubik (`\urlstyle{same}`); figure PDFs have no mono font | per-page `pdffonts` loop (script `fonts_by_page.py`); `grep -n "urlstyle" *.cls` | blocker, recurring |
| K4 | The box shows a **real script, read from its file** (PRD R-25), and the script runs | the code in the box is read from a `python/*.py` file by the CLS (`pythonbox` takes a path; no pasted code in the chapter), and the PDF text equals the file's lines (modulo the shown range); running that script reproduces the chart it claims | `grep -n "pythonbox" chapters/*.tex` shows a path argument; extract the box text with `pdftotext -layout` and diff against the file; run the script and compare its output with the figure it names | blocker |
| K5 | Every Python script runs (formerly K4) | `python python/<each>.py` exits 0 and writes its figure to `figures/` | run each script | blocker |

## Family 7: Layout / pagination (עימוד), the four rules of ch. 19.4 (book p. 78)
Rule text: "the table of contents, the summary, every chapter and the bibliography start on a new page; a heading is not left alone at the bottom; no box/table/figure is cut between pages; no almost-empty pages; `\needspace` is used."

| ID | Criterion | Target | Check | Sev |
|----|-----------|--------|-------|-----|
| L1 | Each chapter, the TOC, the executive summary and the references start on a new page | `chapter` starts a page (CLS) | PDFPAGE first page of each chapter | major, recurring |
| L2 | No orphan heading | no heading is among the last 2 lines of a page | PDFPAGE every page; helper: `pdftotext -layout` per page and look at the last non-empty line | major, recurring |
| L3 | No box, table or figure is cut by a page break | zero | PDFPAGE | major, recurring |
| L4 | No nearly empty page | every content page is at least 40% filled, except the last page of a chapter and the one-page chapters | PDFPAGE (count characters per page via `pdftotext`; flag pages with < 600 characters) | major |
| L5 | No widow/orphan lines and no one-word last lines | LOG warning count `Overfull`/`Underfull` tracked; visual check | PDFPAGE | minor |
| L6 | Table of contents exists, is correct and complete | entries for every chapter and section; page numbers match; TOC is in the PDF | PDFPAGE; `main.toc` vs headings | major |
| L7 | Banner and footer on every content page | same position, same content, not overlapping text; no footer on the cover | PDFPAGE all pages | major, recurring |
| L8 | Page numbers are continuous and match the TOC | no gaps | PDFPAGE | major |
| L9 | No text outside the margins (including long URLs in references) | none | PDFPAGE; LOG overfull | major, recurring |

## Family 8: Sources (מקורות) - book p. 77: "citation in list, and everything is accurate"; ch. 17 (printed p. 67-68)
Rule from the table on p. 78: cite a source only from the list; "a key instead of a number" is a defect.

| ID | Criterion | Target | Check | Sev |
|----|-----------|--------|-------|-----|
| R1 | Every `\cite` resolves | LOG and BLG: 0 `undefined citation`, 0 `Warning--I didn't find a database entry` | `grep -ci "undefined citation\|didn't find a database" main.log main.blg` | blocker |
| R2 | Citations print as numbers (IEEE), never as a key | PDF shows "[n]" everywhere; no "Segal2026" text | `pdftotext main.pdf - \| grep -nE "\[[A-Za-z]"` finds 0 | major, recurring |
| R3 | IEEE style, one style for all entries | `biblatex` `style=ieee`; numeric order of first citation | `grep -n "biblatex" *.cls main.tex` | major, recurring |
| R4 | Number of real sources | at least 12 distinct entries in `references.bib` and all 12 cited at least once in the body | count entries; `biber --tool` or `main.bcf` cited keys vs bib | major |
| R5 | Every source is real and verifiable | each entry has a DOI or a working URL; qa-se opens the DOI/URL and compares title, authors, year, venue. Any entry that fails to resolve or does not match is a **fabrication** | `curl -sIL https://doi.org/<doi>` (status 200/302) and compare metadata; record in the report one row per entry | blocker |
| R6 | Entry completeness | author(s), title, venue/publisher, year, pages or article number, DOI/URL; no "unknown"/"n.d." | read `references.bib` | major |
| R7 | Reference list starts on a new page, is not orphaned, has no overfull URL | 1-2 pages | PDFPAGE | minor |
| R8 | A claim with a number has a source or is labeled as our assumption | every statistic (return rate, market size) has `\cite{}` or the word "assumption"/"estimate" | read each chapter; list unsupported claims | major |
| R9 | Source dates are credible for a 2026 report | no source after Nov 2026; prefer 2018+ except classics | read | minor |
| R10 | **Claim-trace table** (RT-Q7) | every statistic in PRD §1 and in ch. 1-2 (24%, 53%, up to 80%, the market sizes, the $685 B-$890 B range) is traced: claim, cite key, **quoted source sentence, page**, "number found: yes/no". A statistic with only a vendor or paywalled source is worded "reported by <source>" in the text. Table lives in `qa/reports/` | qa-se opens each source and records one row per claim | blocker (a number not in its source) |
| R11 | No unused bib entry; every `@online` has `urldate` | every key in `references.bib` is cited at least once (biber warns nothing; qa diffs `main.bcf` cited keys vs bib keys); each web entry has `urldate` (and an archive link where possible) | script: bib keys minus cited keys = empty; `grep -L urldate` on web entries | major |
| R12 | **Legal sources are official** (PRD R-26, UD-7) | Israel's Privacy Protection Law **Amendment 13** (primary) and **GDPR Art. 9** (secondary) are cited from official texts (Knesset/Nevo-official gazette or the Privacy Protection Authority for Israel; EUR-Lex for GDPR). A law blog, a law firm page or a news article is not an official source. Every legal claim in the text (biometric data = "data of special sensitivity", the in-force date 14 Aug 2025) has a `\cite` to the official text; **no legal claim without a source**; BIPA appears nowhere (`grep -rni "BIPA\|Illinois" chapters/ references.bib` = 0). The text argues "fit, not identification" + privacy-by-design as an advantage | open each legal source, check the publisher and that the quoted provision exists; grep | blocker (legal claim with no official source), major (non-official source) |
| R13 | **Israeli numbers are sourced or tagged** (PRD R-27, UD-6, UD-8) | every Israeli market number (online apparel sales, number of e-tailers, platform mix, prices in ILS) is `\cite`d to an official or reputable Israeli source, or tagged `\derived`/`\assumed`; Europe is the expansion stage and is not in the Y1-Y3 base case; ILS amounts use `\ils{}` and a single assumed exchange rate that matches the `assumptions.csv` row; the reporting currency is USD | list every number in ch. 2, 6, 8 with ILS or "Israel"; compare to its class and source; grep the rate | blocker (an Israeli number with no class), major (wrong or mixed rate) |

## Family 9: File structure (מבנה קבצים) - book p. 77: "folders, paths, limits"; assignment §3.3
| ID | Criterion | Target | Check | Sev |
|----|-----------|--------|-------|-----|
| FS1 | Required root files exist (assignment §3.3) | `main.tex`, `<cls>`, `PRD.md`, `PLAN.md`, `TODO.md`, `README.md` | `ls` | blocker |
| FS2 | **One `.tex` per chapter** (PRD R-24; assignment: "additional .tex files (for example one per chapter)") | 10 chapter files in `chapters/*.tex` (+ the Hebrew page file), each `\input` from `main.tex`, no chapter inside another | `grep -n "input\|include" main.tex` | major |
| FS3 | No deliverable `\input`s from an agent folder | 0 hits for `writer/`, `art/`, `qa/`, `fix/` in `main.tex` and chapters | grep | major |
| FS4 | Paths are relative and portable; no `C:\` in sources | 0 hits for `C:\\` or `\\Users` in `.tex`, `.cls`, `.py` | `grep -rnE "C:\\\\|Users" --include=*.tex --include=*.cls --include=*.py .` | major |
| FS5 | Fonts are in `fonts/` (OFL) and loaded by relative path; **provenance** (PRD R-07) | `fonts/` contains Playfair Display, Rubik and **JetBrains Mono** files plus their OFL texts and `fonts/SOURCES.md`; the Playfair Display and JetBrains Mono files are byte-identical to the official releases (`sha256sum` equals the hashes in `SOURCES.md`); CLS uses `Path=` | `ls fonts`; `grep -n "Path" *.cls` | major |
| FS6 | Reproducibility | a fresh clone builds with the 4-command sequence and gives the same page count | clone to a temp folder, build (this is the assignment's "proof of repro-ducibility") | blocker |
| FS7 | `.gitignore` excludes build junk but not the final PDF, `.bib`, `.cls`, `.tex`, `figures/` | `git ls-files` shows `main.pdf` (assignment requires the PDF in the repo) | `git ls-files` | major |
| FS8 | README states the build command and the list of skills used | README has the 4 commands and the skills list | read | minor |

---

## Group B: Build (clean build is a hard gate)
Sequence: `lualatex main`, `biber main`, `lualatex main`, `lualatex main`. (Assignment §7, book ch. 18.8 prompt 7 p. 73.)
Our threshold is **stricter than the book**: the book allows "overfull wider than 5pt" to be fixed, we fix everything over **1pt**.

| ID | Criterion | Target | Check | Sev |
|----|-----------|--------|-------|-----|
| BU1 | The four commands finish | exit code 0 for each; `main.pdf` is created | run; `$LASTEXITCODE` | blocker |
| BU2 | 0 errors | LOG: 0 lines starting with `!` | `grep -c "^!" main.log` | blocker |
| BU3 | 0 undefined references | 0 `LaTeX Warning: Reference` ... `undefined`; 0 `There were undefined references` | `grep -c "undefined" main.log` | blocker |
| BU4 | 0 undefined citations | see R1; `biber` reports 0 errors and 0 warnings of "not found" | `grep -E "ERROR\|WARN" main.blg` | blocker |
| BU5 | No overfull box over 1pt | every `Overfull \hbox (Xpt too wide)` has X <= 1.0; also 0 `Overfull \vbox` over 1pt | `grep -E "Overfull" main.log`, parse values | major, recurring |
| BU6 | Underfull boxes are reviewed | report the count; badness 10000 in body text is a finding | `grep -c Underfull main.log` | minor |
| BU7 | No `Missing character`, no `Font ... not found` | 0 | grep | blocker |
| BU8 | References are stable after the last pass | the third run prints no `Rerun to get cross-references right` | `grep -i "rerun" main.log` | major |
| BU9 | Page count is printed and recorded | the report states total pages and content pages (D1) | `pdfinfo main.pdf` | minor |
| BU10 | Build time and warnings are repeatable | two builds in a row give the same page count | build twice | minor |

## Group D: Our fixed decisions
| ID | Criterion (decision) | Target | Check | Sev |
|----|----------------------|--------|-------|-----|
| D1 | 25 or more **content** pages (front matter excluded; hard requirement; PRD R-01 **prevails** over the per-chapter tolerance of R-02) | content pages >= 25. Content = from the first page of chapter 1 to the **last page of chapter 10 (Conclusion)**. Excluded: cover, TOC, lists, the Hebrew executive-summary page (front matter, Q-3) **and the references** (RT-Q1) | `pdfinfo main.pdf` (total) minus the number of front-matter pages (read from the roman-numbered pages on `main.toc` or `\pageref`) | blocker |
| D2 | Body language is English LTR | all content pages except the Hebrew page: LTR and English | `pdftotext` per page | major |
| D3 | One Hebrew RTL executive-summary page with perfect BiDi | exactly 1 page; see B1-B10 | see family 3 | blocker |
| D4 | **Font whitelist: Playfair Display, Rubik, Latin Modern Math (formula pages only), JetBrains Mono (code-box page(s) only)** (PRD R-06; UD-3, UD-4) | `pdffonts main.pdf` lists only fonts whose name starts with `PlayfairDisplay`, `Rubik`, `LatinModernMath`/`LMMath` or `JetBrainsMono` (any weight/style subset), all with `emb = yes`; **per page**: LM Math appears only on pages that hold a formula (pages of the `eq:` labels in `main.aux`), plus inline math symbols (not digits, not prose; amended 2026-11-20, master-se), JetBrains Mono only on the Appendix A page(s) (K3); **figure PDFs** contain only Playfair and Rubik (I8). Any other name (LatinModern, DejaVu, Cambria Math, NimbusMono, TeX Gyre, STIX...) = defect; any other monospace font is a failure (K3); any other math font is a failure (D11). Also check PDFs inside figures | `pdffonts main.pdf` ; compare names | blocker, recurring |
| D5 | Heading fonts and body fonts are assigned right | English headings Playfair Display; English body Rubik; all Hebrew text, including Hebrew headings, Rubik | PDFPAGE + `pdffonts`; `pdftotext -bbox` not needed | major, recurring |
| D6 | **Palette only** | colors in PDF are ink #111111, ivory #F7F3EE, mocha #A47864, powder pink #E8C6C0, the approved tints mocha-deep #6B4B3D and mocha-pale #D3BBAE, the figure-only neutrals grid #E3DCD4 and muted #6F6862, and white. No other hue. No other hue. Methods: (a) `grep -noE "#?[0-9A-Fa-f]{6}" *.cls chapters/*.tex python/*.py figures/*.tex` -> only the four values; (b) render pages to PNG and count dominant colors (Python script in `qa/`) | grep + image check | major, recurring |
| D7 | Hyperlink colors, table rules, code backgrounds, `\hypersetup` colors also follow the palette (the default hyperref blue/red boxes would break D6) | 0 default blue/red link boxes in PDF | PDFPAGE; `grep -n hypersetup *.cls` | major, recurring |
| D8 | Banner and footer on every content page | see L7 | PDFPAGE | major |
| D9 | At least 1 figure, 1 table and 1 formula | figures >= 1, tables >= 1, numbered formula (`equation`) >= 1; target 6 / 5 / 2 | `grep -c` for `begin{figure`, `begin{table`, `begin{equation` (and `align`) | blocker |
| D10 | Formula is in the Financial Plan chapter, numbered, introduced in the text, with each symbol defined | `\label{eq:...}` + `\eqref`; symbols listed after the formula | read; PDFPAGE | major |
| D11 | **Latin Modern Math only inside formulas** (UD-3; Q-1 closed) | Formula (1) in ch. 8 and any other equation: letters and digits in Rubik, symbols in LM Math; LM Math appears on no page without a formula, except inline math SYMBOLS (rho, varphi, geq...) in text or tables; never digits or prose (amended 2026-11-20, master-se, R-06); no other math font (STIX, Cambria Math, Libertinus Math...) | per-page `pdffonts` against the pages of the `eq:` labels | `pdffonts` | major |
| D12 | Graphs from Python, diagrams in TikZ, **no internet images** | see I6 | `ls`; no `http` in `\includegraphics` | blocker |
| D13 | IEEE references, **all real** | see R1-R6 | see family 8 | blocker |
| D14 | **Financial figures are labeled** (RT-Q6; PRD R-14). Scope: ch. **2, 5, 6, 7, 8, 9** and every figure/table caption in them | every number with `$`, USD, ILS, `%`, a multiplier ("x") or "years" is in exactly one of 3 classes: **sourced** (`\cite{}` in the same sentence), **derived** (computed from sourced/assumed numbers, with the formula or inputs named), **assumed** (inside `\assumption{}` or under a caption that starts "Assumption:"). Ch. 8 opens with a statement that all projections are illustrative assumptions | grep the numbers in the scoped chapters; qa lists every number in none of the 3 classes | blocker |
| D15 | Real-company claims are factual or labeled | competitor names, funding, features: sourced or "as of <date>"; no invented customers/partners | read vs source | major |
| D16 | Style: fashion-editorial, clean, airy, made **measurable** (RT-Q5) | margins >= 2.5 cm; <= 4 series per chart; <= 1 figure and <= 1 table per page unless a pair is intended; no content page more than half figure (I13); devices of PRD §5.3 used consistently | measure margins on a rendered page; count; PDFPAGE | minor |
| D17 | **Page budget per chapter** (see table below) | each chapter's page count within the tolerance | `pdftotext` per page + `main.toc` | major |
| D18 | **Contrast** (RT-Q5) | text under 14 pt bold / 18 pt regular: contrast >= **4.5:1** with its background; large text and graphics >= **3:1**. Mocha #A47864 is 3.85:1 on white and 3.5:1 on ivory, so **small mocha text (caption labels, links) uses mocha-deep #6B4B3D (about 7.8:1); the tints mocha-deep and mocha-pale are **approved (UD-1)**. Powder pink never carries text (1.4:1).** Large mocha text (chapter numbers) is allowed | compute the WCAG ratio of every text color against its background (script in `qa/`); PDFPAGE | major, recurring |
| D19 | **White page; ivory only on the cover and inside boxes** (UD-2) | the page background is white (#FFFFFF); ivory appears on the cover and inside stat cards, pull quotes, table header rows and the code box, each with a 0.4 pt mocha-pale hairline; no ivory page | render pages and sample the page-corner pixel (script `contrast_colors.py`); PDFPAGE | major, recurring |

### D17 page budget (from `03-expert-committee.md`)
Pages are counted from the chapter's first page to the page before the next chapter's first page. Tolerance (approved by master-se, Q-5): **+/- 1 page** per chapter, **exactly 1** for the conclusion; total content >= 25 is a **hard requirement** (D1), and <= 32.

| Chapter | Budget | Accept | Reject |
|---------|-------:|--------|--------|
| Intro & Problem | 3 | 2-4 | otherwise |
| Market TAM/SAM/SOM | 4 | 3-5 | |
| Competition | 3 | 2-4 | |
| Product & Technology | 4 | 3-5 | |
| Business Model & Pricing | 3 | 2-4 | |
| Go-to-Market | 2 | 1-3 | |
| Operations / Team / Roadmap | 2 | 1-3 | |
| Financial Plan (with a formula) | 3 | 2-4 | |
| Risks | 2 | 1-3 | |
| Conclusion | 1 | exactly 1 | |
| References (IEEE) | 1-2 | 1-2 | |
| **Sum of budgets** | **27 + 1-2 = 28-29** | total content 25-32 | below 25 is a blocker (D1) |

The sum of the budgets (28-29 pages) covers D1 with 3-4 pages of margin. The Hebrew executive-summary page is front matter and is **not** in the budget or in the 25 (decision Q-3).
Note: with the lower bounds above the chapters sum to only 18 (ch. 1-10), so D1 (>= 25 for ch. 1-10, references excluded) is the binding limit; a build in which every chapter is within tolerance but ch. 1-10 total < 25 **fails** (RT-Q1).

## Group S: Assignment submission and process (from the assignment PDF)
| ID | Criterion | Target | Check | Sev |
|----|-----------|--------|-------|-----|
| S1 | One final PDF | `main.pdf` in the repo, built by the 4 commands | `git ls-files` | blocker |
| S2 | Required skills are present and used | the QA skills of the assignment's Table 2 exist under `.claude/skills/`: `qa-super`, `qa-BiDi`, `qa-table`, `qa-code`, `qa-img`, `qa-typeset`, `qa-infra`, `qa-cls-version`; each has a frontmatter `version:` | `ls .claude/skills` | major |
| S3 | The list of skills used is in the repo (assignment §6) | README (or a `SKILLS.md`) lists every skill used, **including the files themselves** | read | major |
| S4 | The submission has: all source files (`.bib .cls .tex`), the docs (`PRD.md PLAN.md TODO.md README.md`), the final PDF, the skills list | all present in the one shared repo | `git ls-files` | blocker |
| S5 | **Agent prompt includes all requirements** (PRD R-23; assignment §4 step 6) | `prompts/` holds a requirement-complete prompt that lists every assignment requirement (length, content, structure, design, CLS, BiDi, skills, build) | read against assignment A2 Table 1 | major |
| S6 | Recurring problems were fixed in the CLS or a skill, not in the text (assignment "iron rule") | CHANGELOG rows match the problems seen in QA reports | compare `fix/CHANGELOG.md` with `qa/reports/` | major |
| S7 | Pre-submission checklist of book 19.5 (p. 79) all passes (see list below) | all 6 | run | blocker |
| S8 | **Definition-of-Done sign-off lines** (RT-Q2) | `qa/reports/` holds: (a) the final report from a **fresh-clone** build with 0 open blocker and 0 open major findings, each earlier finding marked "rechecked in build <hash>"; (b) sign-off lines (name, date, page list) for each of the six 19.5 items; (c) a human's record of reading the exec summary and conclusion. qa-se does not claim "no findings", only "0 open blocker/major" | read `qa/reports/` | blocker |
| S9 | **Reproducibility is measured, not byte-compared** (RT-Q8; PRD R-16) | two builds (and a fresh clone) give the same page count, the same `pdftotext` per page, the same `pdffonts` list and the same error/warning counts | build twice; diff the outputs | blocker |

### Book 19.5 pre-submission checklist (printed p. 79) mapped to criteria
1. Zero compile errors, and no ignored warnings -> BU2-BU8.
2. No reversed Hebrew; no text outside the margins -> B1-B10, L9.
3. All tables aligned and all images appear -> TB1-TB7, I1-I11.
4. Every source is checked and read -> R1-R9.
5. Someone looked at every page, at a size one can read -> a PDFPAGE pass of **all** pages (qa-se records the page list in the report).
6. A human read the summary and understood the problem and the solution -> master-se or a teammate reads the exec summary and the conclusion; qa-se records the sign-off.
The book's warning (p. 79): do not accept "the model said it checked"; qa-se asks for page numbers and findings and opens the pages itself.

---

## Counts per family
| Family | Criteria |
|--------|---------:|
| 1 Template | 6 |
| 2 Cover page | 6 |
| 3 Directionality | 11 |
| 4 Tables | 7 |
| 5 Images | 14 |
| 6 Code | 5 |
| 7 Layout (pagination) | 9 |
| 8 Sources | 13 |
| 9 File structure | 8 |
| **Book families total** | **79** |
| B Build | 10 |
| D Fixed decisions | 19 (+ the D17 budget table) |
| S Submission/process | 9 |
| **Grand total** | **117** |

## Assignment requirements that are NOT in our fixed decisions
Source: assignment PDF pages A1-A5. The assignment is binding, so each item needs a PRD row (master-se) and an owner.

1. **Custom `.cls` template is mandatory** (A2 §3.2) and the design requirement "CLS" (Table 1, row "Design"). Our decisions name fonts and palette but not the CLS file as a requirement. -> T1, T2, owner fix-se.
2. **Table of contents** is a minimum requirement: "division into chapters, **table of contents**, bibliography list (IEEE)" (Table 1, row "Structure"). Our decisions list banner/footer but no TOC. -> L6.
3. **Content minimum**: "images, graphs, summaries, texts, tables" (Table 1, row "Content"). We say figure/table/formula; the assignment also wants **summaries** (we have the Hebrew exec summary; qa-se also expects a conclusion) and **texts**. Covered by D3 and the Conclusion chapter.
4. **Length alternative**: 25 pages English **or** 15 pages Hebrew+English mixed (Table 1). We chose 25 English; no conflict. But the assignment counts "pages" without saying "excluding front matter": our stricter reading (D1) is safe.
5. **Compiler**: LuaLaTeX on MiKTeX (A2 §3.1). Build must succeed on MiKTeX, with `lualatex` and `biber`. -> BU1, FS6.
6. **Folder structure** (A3 §3.3): `main.tex`, extra `.tex` files, `.cls`, `PRD.md`, `PLAN.md`, `TODO.md`, `README.md` **in the project root**. -> FS1, FS2.
7. **Workflow** (A3 §4): a PRD, a detailed PLAN, atomic TODO, **use of the QA skills** (`qa-super` and the others), **an agent prompt that includes all requirements** ("prompt engineering"), run, check, and "fix the generator (CLS/skill), not by hand", then keep all files (.pdf .md .cls .tex). -> S2, S5, S6.
8. **The iron rule** (A3): "never fix a problem directly in the text; every fix goes through the generator (CLS or skill)". We have it in CLAUDE.md; the PRD must list it as a requirement. -> T3, T6, S6.
9. **Skills list** (A4 §5, Table 2): the repo must carry the **list of skills used, including the files**. The 8 named skills: qa-super, qa-BiDi, qa-table, qa-code, qa-img, qa-typeset, qa-infra, qa-cls-version. -> S2, S3.
10. **Submission** (A4 §6): one shared GitHub repo per group with source files, docs, the final PDF and the skills list. -> S1, S4, FS7.
11. **Reproducibility proof** (A5 §7 "important": the submission must hold all files so that `lualatex` can be re-run and gives the same PDF). -> FS6, BU10.
12. **Build sequence** (A5 tips): first pass, biber, two more passes. -> BU1.
13. **Topic approval** (A2 recommendation box): the topic must be a practical project (seminar, article, plan, price offer...); a topic that differs from these **needs advance approval**. A business plan matches the examples ("a detailed business plan"), so it needs no approval; master-se should record that in the PRD.
14. **Hebrew/English BiDi perfect** is a "Excellence" item (Table 1). We cover it with the one Hebrew page; the assignment says "BiDi perfect, Hebrew and English", so qa-se also checks that **no direction error appears anywhere** in the English pages (for example Hebrew words in figure labels): B8.
15. **Excellence column** items: footer + banner "professional" (L7), at least 1 figure, 1 table, 1 formula (D9). These are already in our decisions.
16. **Date and author block** on the cover: the assignment is dated "Nov 2026" and credits the lecturer; our cover should carry the group, the course and the date. -> C1 (qa-se asks master-se whether names are wanted).

Items 1, 2, 5-12 and 13 are the "not in our fixed decisions" set (**11 items**); items 3, 4, 14-16 are partial overlaps listed for completeness.

## Decisions applied in v1.3 (the user's answers, PRD v2.0)
UD-4 K1-K5 rewritten for the Appendix A `pythonbox` (ivory fill, hairline, line numbers, LTR, nothing past the margin, reads a real `python/` file; K4 old "scripts run" is now K5); K3 **reversed**: JetBrains Mono allowed only on the code-box page(s) ·
UD-3 D4/D11: LM Math allowed only on formula pages (whitelist is per page) · UD-1 D18/D6: the tints are approved; mocha-deep for small text · UD-2 D19 (white page, ivory only on the cover and in boxes) ·
UD-5 C1 (ivory cover with names, sg00ha11, 875523402, lecturer) and **C6 (no personal ID number: 9-digit grep over files, git history and PDF, excluding 875523402)** ·
UD-7 R12 (official legal sources, no BIPA) · UD-6/UD-8 R13 (Israeli numbers sourced or tagged, one assumed ILS rate, USD reporting) · FS5 now checks JetBrains Mono and the SHA-256 hashes (R-07).
Closed: Q-A, Q-1/Q-C. Count: 117 criteria.

## Decisions applied in v1.2 (red team RT1, all 8 adopted by master-se)
RT-Q1 D1/D17 (ch. 1-10, refs excluded, R-01 prevails) · RT-Q2 S8 (sign-off lines) · RT-Q3 B11 (BiDi corpus + bbox check) · RT-Q4 I8 (fonttype 42, no fallback) ·
RT-Q5 D18 (contrast), I12 (grayscale), D16 (measurable style) · RT-Q6 D14 (scope + 3 classes) · RT-Q7 R10 (claim trace), R11 (no unused entry, urldate) ·
RT-Q8 S9 (reproducibility), C1 (R-22 cover), S5 (R-23 prompt), FS2 (R-24 one .tex per chapter). From the other reviewers: I13 (no page more than half figure), R11 (no unused bib entry),
I1 (ch. 1 stat cards allowed), I14 (positioning-map axes from the vendor table). Open: Q-A (mocha-deep) decides the D18 fallback; Q-1/Q-C (math font) still decides D11.

## Decisions (master-se, applied in v1.1)
- **Q-1 Math font vs "only two fonts": OPEN.** Neither Playfair Display nor Rubik has math glyphs. fix-se checks whether the formula can be set with Rubik only; otherwise it goes to the user's open-questions round. Until then D11 is "pending".
- **Q-2 No monospace font. DECIDED.** URLs are set in Rubik (`\urlstyle{same}`); a mono font in `pdffonts` is a failure (K3, D4).
- **Q-3 The Hebrew page is front matter, not counted in the 25. DECIDED** (B1, C3, D1, D17).
- **Q-4 Overfull threshold is 1pt. DECIDED** (shared CLAUDE.md wins over the book's 5pt; BU5).
- **Q-5 Page budget tolerance: +/- 1 page per chapter, conclusion exactly 1, total content >= 25 hard. DECIDED** (D17).
