import pathlib, re
R = pathlib.Path(r"C:\biu\02\.claude\skills")


def bump(name, ver, old, new):
    p = R / name / "SKILL.md"
    s = p.read_text(encoding="utf8")
    s = re.sub(r"^version: .*$", f"version: {ver}", s, count=1, flags=re.M)
    assert old in s, (name, old[:40])
    s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf8")


bump("qa-typeset", "1.2",
     "12. **Number font in running text (incident 06):** `page.get_text('dict')` spans: in running text every digit span must be Rubik; Latin Modern Math digits are allowed only on pages that carry an `eq:` label.",
     "12. **Number font in running text (incident 06, decision of master-se 2026-11-20 on F-fonts-01):** `page.get_text('dict')` spans: DIGITS in running text and in inline math must always be Rubik. Latin Modern Math is allowed for inline math SYMBOLS (rho, varphi, operators) and for displayed equations; a Latin Modern Math span that contains a digit outside an `eq:` display is a finding.")

bump("qa-code", "1.2",
     "10. **Any monospace font outside the appendix (incident 03):**",
     "10. **Math font rule (decision 2026-11-20, F-fonts-01):** Latin Modern Math is allowed for inline math symbols and displayed equations; digits are never math font (qa-typeset 12). `fonts_by_page.py` therefore must not flag Latin Modern Math on a page for symbols alone.\n11. **`\\texttt` warning (v0.22):** `grep -c \"texttt used in the text\" main.log` must be 0; each hit is a finding for the chapter owner.\n12. **Any monospace font outside the appendix (incident 03):**")

bump("qa-table", "1.2",
     "9. **Lists (incident 03):** read `main.lot` and `main.lof`; fail on `_`, `.csv`, `.py`, `\\texttt`, `table_check`, a `(` or an entry longer than one line.",
     "9. **Lists (incident 03, v0.23):** read `main.lot` and `main.lof`; fail on `_`, `.csv`, `.py`, `\\texttt`, `table_check`, `(`, `:`, `$`/math, or an entry that wraps to a second line. The class cuts the entry at the first `(`, `:` or `$`; an entry that is still too long needs `\\caption[short]{long}` from the owner.\n9b. **Wide label column (v0.23):** a table whose first column holds labels with 5 or more words should use `\\ctnumcols{n}` and columns `W` + `V` (label 1.6 weight); report equal-width `XRRRR` tables whose first column is under 3.5 cm.")

# incident 12
inc = r"""# Incident 12: appendix over two pages, narrow label column, long list entries (F-code-01, Table 8.1, LOF/LOT)

Date: 2026-11-20. Found by: qa-se (qa/reports/05-qa-super-round3.md) and master-se. Handled by: fix-se.

## What happened
- F-code-01: the Appendix A box was split 18+8 over two pages and the second page was 75% empty.
- Table 8.1 (company-level sensitivity) had five equal columns: the label column about 3 cm, wrapping to 3 lines.
- LOF/LOT entries 3.1, 4.1 and 8.2 wrapped to two lines or showed a formula.

## Root cause
- The 54 pt number line and 28 pt title of the numbered/unnumbered opener use 130 pt of the page, a 26-line box plus intro does not fit under them, so v0.21 split the box instead. An appendix is content, not a chapter opener.
- Table 8.1 is generated with the specification `XRRRR`: tabularx gives equal widths to all X columns; the class had no helper for "one wide label column".
- v0.20 cut list entries only at the first "("; sub-titles after ":" and formulas stayed.

## Why no detector caught it
qa-table checked width and alignment but not the width of the first column; the LOF/LOT scan of v1.1 (check 9) was a recipe without a rule about a second line.

## Fix (CLS v0.23)
- `\ctappendix{title}`: compact heading (no number line, 22 pt title, 1.2 cm top). Verified: heading, intro and the whole 26-line box on ONE page (test document and main.tex).
- `\ctnumcols{n}` with column types `W` (label, weight 1.6) and `V` (numbers, right aligned, weights sum to n+1): table 8.1 label column 154 pt instead of 85 pt in the test. Usage change: art-se's `python/company_sensitivity.py` writes `\ctnumcols{4}` before `\begin{tabularx}` and the spec `WVVVV` (REQUEST to master-se).
- List entries are cut by Lua at the first of "(", ":" or "$" (`\caption[short]{long}` still wins).
- Skills: qa-typeset 1.2 (digits never math font; Latin Modern Math allowed for symbols and equations, decision of master-se on F-fonts-01), qa-code 1.2 (same rule, `\texttt` warning grep), qa-table 1.2 (list rule, wide label column).

## New check
qa-table 9 and 9b, qa-typeset 12 (see the skills).

## Status
Fixed in closettwin v0.23; usage change pending for art-se (table spec).
"""
(pathlib.Path(r"C:\biu\02\incidents") / "12-appendix-label-column-list-entries.md").write_text(inc, encoding="utf8")

BS = chr(92)
row = ("| 2026-11-20 | closettwin v0.23 | qa-se round 3 via master-se (F-code-01, F-fonts-01, Table 8.1, LOF/LOT 3.1/4.1/8.2) | "
       "Appendix A over two pages (18+8 lines, 75% empty); Table 8.1 label column narrow; LOF/LOT entries wrap or show a formula; math-font rule unclear | "
       "Opener uses 130pt of the page; equal X widths; list cut only at '('; digits vs symbols rule not stated | "
       "`" + BS + "ctappendix` compact heading (appendix on ONE page); `" + BS + "ctnumcols{n}` + column types `W`/`V`; Lua list cut at '(' ':' '$'; skills qa-typeset/qa-code/qa-table 1.2 (digits never math font, Latin Modern Math allowed for symbols and equations). Incident 12. Usage: main.tex uses " + BS + "ctappendix; art-se must write " + BS + "ctnumcols{4} and WVVVV in the generated table | closettwin.cls, main.tex, .claude/skills/{qa-typeset,qa-code,qa-table}, incidents/12 |\n")
p = pathlib.Path(r"C:\biu\02\fix\CHANGELOG.md")
p.write_text(p.read_text(encoding="utf8").rstrip("\n") + "\n" + row, encoding="utf8")
print("ok")
