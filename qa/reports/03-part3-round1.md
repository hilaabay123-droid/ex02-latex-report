# 03 - Part 3, round 1 (qa-se, build of 2026-11-20, CLS v0.20)

Scope: fresh 4-step build from the root (47 pages), my own chapters 6-10 first, then a build-level check. The qa-super skill checks were NOT run in full: only the checks below. No PDF page-image review beyond p. 38-40, 45-47.

## Build
- lualatex + biber + lualatex x2: 47 pages, no errors, no undefined references or citations.
- 1 overfull box, 0.18 pt (bibliography URL, PDF p. 36 of the log, ref. 29): under the 1 pt limit, not a finding.

## Fixed by me (ch. 6-10, E-2)
- I-4: `XRll` to `XRlX` in ch. 8 "Main inputs"; ch. 9 mitigation table `lRX` to `XRX`.
- `\texttt` removed from the ch. 6 funnel caption.
- Ch. 10 overflowed to a second page (10.3 alone); trimmed, now one page (PDF 41).
- Table column specs checked in ch. 2, 3, 5, 6, 9: 2 `lrlX`, 3 `lXX`, 5 `lXRR`, 6 `lRRRRR` and `lX`, 9 `XRX`. I did not edit ch. 2, 3, 5.

## Findings
| ID | Sev | Location | What | Recurring | Owner |
|----|-----|----------|------|-----------|-------|
| Q3-1 | minor | PDF 46 (printed "Page 39 of 40") | Appendix A opener page holds only the title; the intro paragraph and the code start on PDF 47. In `main.tex` the paragraph sits right after `\ctunnumbered{...}` and `\pythonbox` follows it, so the paragraph is likely pulled to the next page together with the box (`\ctkeepprev`). | possibly (any unnumbered chapter followed by a long box); fix-se should check | fix-se (CLS) / master-se (main.tex) |
| Q3-2 | minor | PDF 40 (ch. 9) | Table 9.1 sits alone on a page; about 60% of the page is empty below it. The page before ends with 9.4/9.5 text. Float placement `[tbp]` with a table that did not fit the previous page. | yes (float placement; same pattern as other chapters if found) | fix-se (CLS float rules) |
| Q3-3 | minor | `writer/outline.md`, Hebrew claim H8 | Still says 7.9%; model D19i = 0.0779 (7.8%). Check that `00-summary-he.tex` says 7.8%. | no | writer-se |

Blockers: none. Counts: 0 blocker, 0 major, 3 minor.

## Not checked
Bidi and fonts in ch. 0-5 and the Hebrew page, figure readability (F1-F7), the content check against PRD, and the new skill checks of v1.1. Needs a full qa-super run.
