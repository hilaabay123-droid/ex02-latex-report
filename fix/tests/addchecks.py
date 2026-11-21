import pathlib, re
R = pathlib.Path(r"C:\biu\02\.claude\skills")

ADD = {
"qa-typeset": """
## New checks (v1.1, from incidents 01, 02, 06, 08, 09, 10)
9. **Literal hyphens (incident 01):** `pdftotext main.pdf - | grep -n -- '--'` must be empty outside the code-box pages. Also `---`.
10. **White space per page (incident 08):** with PyMuPDF find the lowest text/figure y on each page; if the gap above the footer is over 25% of the text height and the page is not a chapter's last page or the conclusion, report it, naming the float that starts the next page.
11. **Words outside the margins / stray numbers (incident 02):** `page.get_text('words')` on every page; any word with xMin below the left margin (3.0 cm) or xMax beyond the right margin is a finding; digit-only words there are reported as "stray numbers" with page and x.
12. **Number font in running text (incident 06):** `page.get_text('dict')` spans: in running text every digit span must be Rubik; Latin Modern Math digits are allowed only on pages that carry an `eq:` label.
13. **Cover text (incident 09):** the cover must contain `Generative AI for Management (875523402)`, `Dr. Yoram Segal` and `BUSINESS PLAN`; any other 9-digit number is a blocker (rule C6).
14. **Opener alignment (incident 10):** on every chapter-opener and Contents/List page the x of the mocha rule and of the first title glyph differ by at most 2 pt.
15. **Legend (incident 07):** the first page with a tag superscript must carry the legend words "sourced", "derived", "assumption".
16. **Page holding only a heading (incident 05):** a page whose only text is a chapter title is reported (a box that did not fit under the opener).
""",
"qa-table": """
## New checks (v1.1, from incidents 03, 04, 07)
9. **Lists (incident 03):** read `main.lot` and `main.lof`; fail on `_`, `.csv`, `.py`, `\\texttt`, `table_check`, a `(` or an entry longer than one line.
10. **Column widths (incident 04):** per table, take each column's width from `pdftotext -bbox`; fail if the first column is under 3 cm while another column holds long text, or if a cell has a word space wider than twice the normal one (a justified narrow cell). Text columns must be ragged right.
11. **Legend before first tag (incident 07):** the legend (sourced/derived/assumption) must be on the page of the first tag superscript in the document.
""",
"qa-BiDi": """
## New checks (v1.1, from incident 02)
7. **Margins on every page:** scan all pages (not only the Hebrew page) for words outside the text block; digit-only words at x below the left margin are "stray numbers" (the TOC chapter-number case). Report page, x and text.
8. **Hebrew ranges:** a range like `2024-2024` (same value twice) or `2024-2026` read right to left on the Hebrew page is a finding (content: writer-se; the `\\range` macro is the CLS tool).
""",
"qa-code": """
## New checks (v1.1, from incidents 03, 05)
9. **Split code box (incident 05):** if the box is on two pages, each fragment must have at least 8 lines; a box under 46 lines must not be split.
10. **Any monospace font outside the appendix (incident 03):** `\\texttt` in a caption or text prints Latin Modern Mono; `fonts_by_page.py` must show no mono font except JetBrains Mono on appendix pages (a finding names the page and the source line).
""",
"qa-img": """
## New checks (v1.1)
10. **Figure and table in the lists:** every figure caption in `main.lof` has no underscore, file name or bracketed note (same rule as qa-table 9).
""",
"writer": """
## Added rules (v1.1, from incidents 03, 06)
11. A caption has no file names, no `\\texttt`, no script or model names; put such facts in the text or use `\\caption[short]{long}`.
12. In prose, no digits inside `$...$`; write numbers in the text font (`\\pct{}`, `\\usd{}`, `\\derived{}` work inside and outside formulas). Formulas with symbols only are fine.
13. Tables: use `X` for long text columns and `l` only for short ones; the first column must stay readable (at least 3 cm); a table should not be the last element of a chapter when it will not fit the page (put text after it).
14. A range of years or numbers in Hebrew text uses `\\range{a}{b}` with two different values.
""",
}

for name, text in ADD.items():
    p = R / name / "SKILL.md"
    s = p.read_text(encoding="utf8")
    s = re.sub(r"^version: .*$", "version: 1.1", s, count=1, flags=re.M)
    s = s.rstrip("\n") + "\n" + text
    p.write_text(s, encoding="utf8")
    print("updated", name)
