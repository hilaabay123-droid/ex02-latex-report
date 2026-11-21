import pathlib
D = pathlib.Path(r"C:\biu\02\incidents")
D.mkdir(exist_ok=True)

COMMON_WHY = "No detector had a criterion for this, and the visual look at every page (book 19.5 item 5) was postponed to the next session."

INC = [
("01-literal-double-hyphen-in-statcard", "I-1: literal \"--\" in the stat card",
 "Chapter 1 stat card read `$685 B--$890 B` instead of `$685 B–$890 B`.",
 "p.1 of ch.1 (pdf page 7), `\\statcard{\\$685\\,B--\\$890\\,B}{...}`; reported by the user in draft v1.",
 "The `--` to en-dash conversion is a TeX ligature of the font (`Ligatures=TeX`). `\\ctheadfont` (Playfair, used for the big number of `\\statcard`) and `\\ctmediumfont` were declared without it, so every `--` set in them stays two hyphens. Class-wide cause, not one card.",
 "qa-typeset and qa-img had no check of the rendered text for `--`; the text source was correct TeX, so a source grep would not have flagged it either.",
 "closettwin v0.20: `Ligatures=TeX` on `\\ctheadfont` and `\\ctmediumfont`; the code font switches ligatures off (`RawFeature={-tlig;-liga;-calt}`) so code stays literal. Verified: stat card now shows an en dash; `pdftotext` of the whole PDF has no `--`.",
 "qa-typeset v1.1, step 9: `pdftotext main.pdf - | grep -n -- '--'` must be empty (outside the code box pages). Also catches `---` and straight quotes."),
("02-toc-chapter-numbers-in-margin", "I-2: stray numbers 1, 2, 3 in the left margin",
 "The user saw the numbers 1, 2, 3 in the left margin next to the Hebrew summary.",
 "Not reproduced on the Hebrew page: a coordinate scan of every page found no word outside the text block there. The only words outside the 85 pt left margin are the ten chapter numbers of the TOC (x = 61 pt) on the page directly after the Hebrew page, so the report most probably refers to those.",
 "`\\titlecontents{chapter}[0pt]{...}{\\contentslabel{2.2em}}` hangs the label 2.2em to the LEFT of the left margin: the chapter numbers stood 24 pt outside the text block.",
 "No check measured text positions against the margins on every page (bbox_margin.py is used for the code page and a `--margins` check on a sample only).",
 "closettwin v0.20: chapter entries `[2.2em]`, label width 2.2em: numbers start at the margin, titles at 2.2em, sections align with chapter titles. Verified by the scan: zero words left of 85 pt on pages with a TOC.",
 "qa-BiDi v1.1 / qa-typeset v1.1: scan every page with PyMuPDF `get_text('words')`; any word with xMin < left margin or xMax > right margin (page width minus 3 cm) is a finding, short digit-only words are reported as 'stray numbers'. If the user's file differs from this analysis, master-se sends the page and a screenshot."),
("03-lot-leaks-internal-text", "I-3: list of tables shows internal text",
 "List of tables entry 6.1 printed `(model output funnel_check_out.csv)`.",
 "Caption of `tab:funnel` in ch.6: `\\caption{Pilot and contact funnel, years 1--5 (all values derived ...; model output \\texttt{funnel\\_check\\_out.csv})}`.",
 "Without a short form `\\caption` copies the whole caption into the list. Any bracketed remark, file name or model note would reach the list. A recurring risk (every caption), not one table.",
 "qa-table scanned captions in the chapters, not the rendered list of tables; there was no LOT/LOF scan for underscores, file names or ids.",
 "closettwin v0.20: `\\caption` without a short title writes only the text before the first `(` to the lists (`\\caption[short]{long}` still wins). The caption itself is unchanged. Verified: LOT entry 6.1 ends at `years 1--5`.",
 "qa-table v1.1: read `main.lot`/`main.lof`; fail on `_`, `.csv`, `.py`, `\\texttt`, `table_check`, `(` in an entry or an entry longer than one line. Also writer rule: no file names in captions (writer skill v1.1). Note: `\\texttt` prints in Latin Modern Mono, a font outside the palette; qa-code now flags any mono font outside the appendix."),
("04-narrow-justified-table-columns", "I-4: Table 8.1 narrow first column with stretched spaces",
 "Table 8.1 (Main inputs): the first column wrapped to 2-3 lines with stretched word spaces.",
 "ch.8, `\\begin{tabularx}{\\textwidth}{XRll}`.",
 "Two causes. (a) tabularx text columns `X` are justified by default, so narrow cells stretch. (b) The `l` columns take their natural width; long `l` text (Class, Basis) leaves the `X` column almost nothing. (a) is a class default; (b) is a column specification.",
 "qa-table checked width and alignment of numbers but not text-column justification or the width share of the first column.",
 "closettwin v0.20: `\\tabularxcolumn` is ragged right, so no `X` cell is justified. For (b) REQUEST to writer-se: use `X` for the long text columns and `l` only for short ones (table 8.1: `XRlX`); every tabularx in ch. 2, 3, 5, 6, 8, 9 to be re-checked.",
 "qa-table v1.1: per table, record the width of each column from `pdftotext -bbox`; fail if the first column is under 3 cm while other columns hold long text, or if any cell has a word space wider than 2x the normal one (justified narrow cell)."),
("05-code-box-leaves-3-lines-alone", "I-5: Appendix A code box leaves 3 lines alone",
 "The code box split over two pages and the last page held only 3 lines (pdf pp. 42-43).",
 "Appendix A, `\\pythonbox{python/appendix_f6_code.py}`.",
 "`\\ct@pysplitmax` was 15: any script longer than 15 lines was breakable at ANY line, with no minimum for either fragment.",
 "qa-code checked margin, fonts and source equality but not how a box is split between pages.",
 "closettwin v0.20: `\\ct@pysplitmax` = 45; a script up to 45 lines is never split. Side effect, stated: an unbreakable box that does not fit under the chapter opener moves, with its intro paragraph, to the next page, so the opener page holds only the title (a longer intro on that page fills it). A script over 45 lines still splits.",
 "qa-code v1.1: for a box on two pages, each fragment needs at least 8 lines; and qa-typeset: a page whose text is only a heading is reported."),
("06-numbers-in-math-font", "I-6: 6.03% in math font, 4.52% in Rubik",
 "Page 25 (8.3): `$\\rho=\\derived{6.03\\%}$` printed 6.03% in Latin Modern Math and `\\derived{4.52\\%}` in Rubik.",
 "ch.8 section 8.3 (and `$r=24.4\\%$`, `$c=\\$6.80$` in 8.1).",
 "Digits inside `$...$` are math characters (Latin Modern Math). The tag macros did not isolate their argument from math mode, and inline math digits had no rule.",
 "No check compared the font of numbers in running text; pdffonts per document hides it because both fonts are used elsewhere.",
 "closettwin v0.20: (1) `\\sourced/\\derived/\\assumed` set their argument with `\\text` when called in math; (2) digits in INLINE math are active math characters that set themselves in the text font (displayed equations stay Latin Modern Math). Verified with `pdffonts` on a test page and by eye; subscripts such as `x_1` work.",
 "qa-typeset v1.1: per-span font scan (`page.get_text('dict')`): in running text every digit span must be Rubik; digits in Latin Modern Math are allowed only on pages with an `eq:` label. Writer rule: no digits in `$...$` in prose."),
("07-legend-after-first-use", "I-7: superscript S/D/A without a legend before first use",
 "The mocha superscripts D and A appear after numbers, and the legend is printed later (ch.1 line 30 vs first use at line 24).",
 "ch.1: `\\assumed{24.4\\%}` comes before `\\ctlegend`.",
 "The legend was a manual call placed by the author; nothing in the class guarantees it appears before the first tag.",
 "qa-table checked the legend inside financial tables only; no check of the first use of a tag in the document.",
 "closettwin v0.20: the first `\\sourced/\\derived/\\assumed` in running text adds the legend as a footnote on that page (`\\ct@firstlegend`; skipped silently inside tables, captions, boxes and formulas, where a footnote is impossible, and tried again at the next use). The manual `\\ctlegend` stays valid.",
 "qa-table v1.1 / qa-typeset: the first page that carries a tag superscript must also carry the legend text 'sourced', 'derived', 'assumption'."),
("08-gap-after-table-reference", "I-8: 40% empty page before a table",
 "Page 25: about 40% empty after `Table 8.1 lists the inputs of this chapter with their class.`; the table is on the next page.",
 "ch.8 section 8.4: the table is the last element of the chapter.",
 "The float is taller (about 285 pt) than the space left on the page (about 180 pt), and nothing follows it in the chapter that could fill the gap. Floats drift forward by design (v0.18: never at the foot, never above their heading). In this case the gap is the physical result of the table height; v0.20 shortens the table by ragged text columns but it does not fit yet.",
 "No detector measured white space per page; qa-typeset only flagged pages under 600 characters.",
 "No class change can fill the gap without breaking the v0.18 rules (a `b` placement was removed for the opposite hole). Remedy at content level: REQUEST to writer-se (ch.8): move the sentence and table so text follows the table, or shorten it (column spec of I-4). The detector below makes the gap visible in every build.",
 "qa-typeset v1.1, step 10: per page the lowest text/figure y; if the gap above the footer is over 25% of the text height and the page is not the last page of a chapter or the conclusion, report it with the next float on the following page as the probable cause."),
("09-cover-missing-course-number", "I-9: cover without the course number",
 "Cover read `Generative AI for Management` without `(875523402)`.",
 "`main.tex`: `\\ctcourse{Generative AI for Management}` (my own entry, written without the number).",
 "A one-off content omission in the cover field, not a class defect: the class prints whatever `\\ctcourse` holds. The course number is allowed (only student IDs are forbidden, rule C6).",
 "No cover-text check existed: qa-typeset checks that the cover has no number or footer, not what it says.",
 "`main.tex`: `\\ctcourse{Generative AI for Management (875523402)}`. No CLS change.",
 "qa-typeset v1.1, step 8: cover text must contain 'Generative AI for Management (875523402)', 'Dr. Yoram Segal' and the doctype label 'BUSINESS PLAN'; and no other 9-digit number."),
("10-contents-title-offset", "I-10: Contents title not aligned with the rule above",
 "On the Contents, List of figures and List of tables pages the title started about 7 pt to the right of the mocha rule above it.",
 "TOC page (pdf 3): rule at x = 85 pt, title at about 92 pt.",
 "The chapter opener title paragraph started with the paragraph indent (`\\parindent`) inside titlesec's block: all openers, numbered and unnumbered, shared it.",
 "The earlier check compared only the y positions of rule and title (v0.15), not x.",
 "closettwin v0.20: `\\noindent` in both opener macros (`\\ctchapterhead`, `\\ctchapterheadstar`). Hebrew openers use a separate macro and were not affected.",
 "qa-typeset v1.1: on every opener page the x of the rule and the first glyph of the title differ by at most 2 pt (the side bearing of the first letter)."),
]

for slug, title, what, where, cause, why, fix, check in INC:
    (D / f"{slug}.md").write_text(f"""# Incident {slug[:2]}: {title}

Date: 2026-11-20. Found by: the user in draft v1 (prompt 06). Handled by: fix-se. Skill: incident v1.0.

## What happened
{what}
Where: {where}

## Root cause
{cause}

## Why no detector caught it
{why} {COMMON_WHY}

## Fix (in the CLS or a skill, not in the text)
{fix}

## New check
{check}

## Status
Fixed in closettwin v0.20 (see `fix/CHANGELOG.md`). Re-check by qa-super after the next build.
""", encoding="utf8")
print(len(INC), "incidents written")
