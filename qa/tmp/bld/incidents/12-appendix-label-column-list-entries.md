# Incident 12: appendix over two pages, narrow label column, long list entries (F-code-01, Table 8.1, LOF/LOT)

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
