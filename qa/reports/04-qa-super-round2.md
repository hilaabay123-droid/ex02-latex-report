# QA report 04: qa-super, round 2 (full pass, v1.1 checks)      build 4950e4c (dirty tree)      2026-11-20

Built in a private copy (`qa/tmp/bld`, because another agent was running lualatex in the root and corrupted `main.aux` once). CLS in the build: **v0.20**. While I ran, the tree changed to **v0.21** (`closettwin.cls` line 4, no CHANGELOG row yet, so T2/T6 is open); v0.21 is not tested here. Q3-1/Q3-2 are therefore re-checked only in round 3. 47 PDF pages (printed page = PDF - 7).
Detector only: no deliverable was edited in this round.

## Summary
Counts: **blocker 1, major 9, minor 8**. Build: 4 steps exit 0, 0 errors, 0 undefined references/citations, 0 missing characters, 1 overfull of 0.18 pt (under the 1 pt limit), 1 underfull (badness 10000).
Skills run: qa-infra, qa-cls-version (partial), qa-typeset, qa-BiDi, qa-table, qa-img, qa-code, plus the v1.1 checks (margins, number font, white space, cover, legend, literal hyphens, heading-only pages). Not done in full: claim-trace of every statistic (R5, R8-R10), link check of every DOI (R5), git-history ID scan, fresh-clone reproducibility (FS6): skipped, see the end.

## Blockers
- **F-code-01** K3: monospace font Latin Modern Mono on PDF 28 (printed 21): `\texttt{.il}` in `chapters/06-gtm.tex:4`.

## Findings (sorted)

### F-code-01 [blocker] K3 (v1.1 check 10)
- Where: chapters/06-gtm.tex:4 | printed 21 (PDF 28)
- What: `\texttt{.il}` in running text prints LMMono12 outside Appendix A.
- Evidence: `fonts_by_page.py`: "LMMono12-Regular on PDF 28"; PyMuPDF span `.il` font LMMono12-Regular. I removed the same class from the ch. 6 caption last round; it reappeared in the text.
- Recurring: yes (same cause as incident 03; reappeared). Places: this one. Owner: **writer-se** (remove `\texttt`; write ".il" plainly) and fix-se (make `\texttt` map to Rubik or warn).
- Status: open

### F-typeset-01 [major] D17
- Where: chapters/08-finance.tex | PDF 33-37 (printed 26-30)
- What: ch. 8 has 5 pages against a budget of 3 (accept 2-4). Cause: my red-team additions (long Table 8.1 caption, two new paragraphs, the sensitivity table).
- Evidence: `page_stats.py`: "chapter 8: first PDF page 33, 5 page(s), budget 3, accept 2-4". Total content is 40 pages (>= 25 OK).
- Recurring: no. Owner: writer-se (shorten the Table 8.1 caption, which is 6 lines; move the input mapping into the text). master-se decides if the budget is moved.
- Status: open

### F-typeset-02 [major] L2, L4, D16
- Where: PDF 36 (printed 29) and PDF 37 (printed 30)
- What: heading "8.4 Assumptions" and one sentence end PDF 36, 43% of the page is empty, and Table 8.2 starts PDF 37, which is 44% empty. The float did not fit and was pushed.
- Evidence: `page_stats.py`: PDF 36 "510 characters", heading-sized line "8.4 Assumptions" among the last lines; white-space scan: 43% and 44% empty.
- Recurring: yes (float placement; the same pattern at PDF 40 below). Owner: fix-se (CLS float rules / `\Needspace` for headings before floats).
- Status: open

### F-typeset-03 [major] L4, I10 (v1.1 check 16)
- Where: main.tex:41-44 | PDF 46 (printed 39)
- What: Appendix A opener page holds only the title (62 characters); intro and code start on PDF 47. (= Q3-1 of the earlier report.)
- Evidence: PyMuPDF: page 46 lines `['Appendix A: Code of the', 'retailer-economics chart']`. Not re-tested with v0.21.
- Recurring: possibly (any unnumbered chapter followed by a long box). Owner: fix-se (the intro paragraph is kept with the box by `\ctkeepprev`) / master-se (main.tex).
- Status: open

### F-infra-01 [major] R6 (recurring)
- Where: references.bib: truefit_web, fitanalytics_web, threedlook_web, boldmetrics_web, mysize_web, threedlook_pricing, popsize_shopify, shopify_dev_build, il_ppl_en, il_cpfta_guide, aguko_shopify_il (11 @online entries)
- What: no year/date field (urldate is present).
- Evidence: `bib_vs_cited.py` "missing year/date" for each of the 11. For undated vendor pages this may be acceptable if the style prints "n.d." or the urldate; the printed list reads "Accessed: Nov. 18, 2026" with no year.
- Recurring: yes (11 entries, one class). Owner: writer-se for the field (give the page date where one exists); master-se decides whether undated web pages are acceptable for R6.
- Status: open

### F-infra-02 [major] R11
- Where: references.bib: ghodhbani2022, il_cpl_amend7_1998
- What: entries are never cited (bibliography has 39 entries, 37 are cited).
- Recurring: no. Owner: writer-se (cite or delete).
- Status: open

### F-infra-03 [major] R6
- Where: references.bib: peng2023 (inproceedings)
- What: missing pages or article number.
- Recurring: no. Owner: writer-se.
- Status: open

### F-clsver-01 [major] T3 (recurring by definition)
- Where: chapters/07-operations.tex:13, chapters/08-finance.tex:20 and :36, chapters/09-risks.tex:7
- What: `\centering` inside figure floats (written by me under E-2). The CLS has no figure macro that centers.
- Recurring: yes (4 places, all figures). Owner: fix-se (provide a figure environment or `\ctfigure` that centers), then writer-se removes the four lines. Do not patch the text.
- Status: open

### F-clsver-02 [major] T2, T6
- Where: closettwin.cls:4 vs fix/CHANGELOG.md
- What: the tree has CLS v0.21; the build log and CHANGELOG say v0.20; no CHANGELOG row for v0.21.
- Evidence: `grep ProvidesClass closettwin.cls` -> `v0.21`; `grep -c v0.21 fix/CHANGELOG.md` -> 0. Likely fix-se mid-work.
- Recurring: no (one release). Owner: fix-se.
- Status: open

### F-table-01 [minor] TB4 (v1.1 check 10)
- Where: figures/tab-company-sens.tex (spec `XRRRR`) | printed 28 (PDF 35)
- What: the first column is narrow (about 3 cm), so "Orders per European client 500k (base 1M)" wraps to 5 lines; the numeric columns are wide.
- Recurring: possible (same spec pattern as other X+R tables); Owner: art-se (column spec) / fix-se if the `R` column is the cause.
- Status: open

### F-table-02 [minor] D14 / lists (v1.1 check 9)
- Where: main.lof | printed vi (PDF 6)
- What: the list entries for Figure 3.1 and 4.1 wrap to two lines (captions are long); the entry for 8.2 shows "reduction ρ" (math in a list).
- Recurring: yes (captions used as list entries). Owner: fix-se (short caption option) or writer-se (`\caption[short]{long}`).
- Status: open

### F-typeset-04 [minor] L4
- Where: PDF 40 (printed 33)
- What: Table 9.1 sits on its own page, 57% empty. Last page of ch. 9, so exempt from L4 by rule; reported for float placement (same cause as F-typeset-02).
- Recurring: yes (see F-typeset-02). Owner: fix-se.
- Status: open

### F-typeset-05 [minor] BU6
- Where: main.log:2193 | printed 19 (PDF 26)
- What: 1 underfull box, badness 10000. Overfull 0.18 pt at log line 2216 (a bibliography URL, PDF 37 in the log) is under the limit.
- Recurring: no. Owner: writer-se/fix-se (not significant).
- Status: open

### F-infra-04 [minor] C6
- Where: qa/tests/run_selftest.py (lines 107, 274-293)
- What: 8 synthetic nine-digit numbers (test fixtures) are matched by the ID scan. They are not real IDs. Mine to fix: build them at run time. No real ID found in the PDF text, chapters or bib (the only 9-digit hit in the PDF is part of a DOI string).
- Recurring: no. Owner: qa-se (own file). The git-history scan (`--history`) was not run.
- Status: open

### F-bidi-01..04 (script output, not findings)
`bidi_bbox_check.py` reports TAM, SAM, SOM missing and no Latin run ending a sentence (B11). This is the stale corpus file `qa/scripts/bidi_runs.txt` (mine) against the rewritten Hebrew page, which now uses ClosetTwin, B2B, AI, Appriss, NRF, Coresight, IMARC, GDPR, Shopify. **Verified by eye** (PNG at 110 dpi): the page is correct. See the corpus table. `hebrew_pages.py` B6 (Playfair on the Hebrew page) is the brand name in the footer; the Hebrew heading and text are Rubik. Both are script false positives; I will update the corpus file.

### Notes (checked, pass)
- `code_diff.py` reports 3 lines differing in the Appendix A box; by eye lines 9-11 are the same as the file (the "-" in comments is extracted as a minus sign). The box shows the real file, 26 lines, whole.
- Page numbers and Contents agree; roman front matter; cover has the course line, "Dr. Yoram Segal" and "BUSINESS PLAN" (cover-text check passes); no other 9-digit number on the cover.
- Legend: the first tag is on PDF 11 and the legend words are on that page.
- Margins: no word outside the text block (v1.1 check 11); no stray numbers.
- Number font: no Latin Modern Math digit in running text. Latin Modern Math appears on PDF 6, 15, 30, 33-34, 36, 37 as symbols (rho, varphi, geq, div), not digits.
- Literal "--" in the PDF text: 0 outside the code box.
- Palette: 8 colours, all in the whitelist; fonts of figures: Rubik only; contrast script: 4 of 4 pass. Python scripts: 6 of 6 exit 0 with no stderr.
- PRD traps: "break-even within" 0; BIPA/Illinois 0; macro uses of `\usd \pct \ils`: 53.
- `label_refs.py`: 8 tables, 7 figures, 1 equation, all referenced.

## Recurring
| Problem | Places | Owner | Criteria |
|---|---|---|---|
| Floats pushed to the next page leave a half-empty page and an orphan heading | PDF 36, 37, 40 | fix-se | L2, L4 |
| `\texttt` prints Latin Modern Mono | ch. 6 caption (fixed), ch. 6 text line 4 | fix-se + writer-se | K3 |
| `\centering` in figure floats | ch. 7, 8 (x2), 9 | fix-se | T3 |
| Long captions in the lists | Fig. 3.1, 4.1, Table 8.1 | fix-se | lists |
| Undated @online bib entries | 11 entries | writer-se / master-se | R6 |

## Judgment checks
**Hebrew page corpus** (read by eye, PDF 2): Latin runs seen, all correct and in reading order: ClosetTwin (x3 plus footer), B2B, AI (heading and text), Appriss, NRF, Coresight, IMARC, GDPR, Shopify (the last word of the final sentence, followed by the period on the left side: correct). Numbers with units correct: 685 and 890 billion, 24.4%, 53%, 17%, 6.80, 6.9 billion, 0.2 million, 0.13 NIS, 0.036, 7.8%, 4 weeks, 14 August 2025, 0.78 million, 2.33 million, 20%, 2.8 million, 2026. Parentheses and ranges correct; paragraphs start at the right edge; heading in Rubik; footer "עמוד ii מתוך 40".
**Fact-check requested by master-se (Knesset report, `knesset_ric2025`, PDF p. 8, Figure 8, Statista Nov 2024, by share of orders): VERIFIED.** I downloaded the report (31 pages) and read page 12 of the PDF (printed p. 8): local sites: Super-Pharm 22, Shufersal 20, KSP 15, **Terminal X 12**, Rami Levi 9; global sites: **AliExpress 57**, SHEIN 12, Amazon 7, Temu 7, Next 5. The text above it says the 2020 ranking is led by Amazon with $195M. The sentence now in ch. 6 (Amazon first in 2020, Terminal X 12% in 2024) matches. Note: the shares are shares within each list (local and global), not of all Israeli orders, and cover all categories; ch. 6 says "order shares of several local sites", which is correct.
**Number classes:** ch. 6, 8, 9, 10 numbers carry `\assumed`/`\derived`/`\sourced` or sit in tables with a class column; not every number in ch. 2, 5, 7 was traced (skipped).
**Page-by-page look:** viewed PDF 1, 2, 6, 35-38, 40, 47 as images. Pages 3-5, 8-34, 39, 41-46 were checked by text statistics and the scripts only, not by eye.
**Content vs PRD:** not done (skipped).

## Skipped
| Criterion | Reason |
|---|---|
| R5, R8, R10, R12 (full claim trace, DOI link check) | Time; only the Knesset item was traced. Needs a separate pass |
| C6 history scan, FS6/S9 clean-clone reproducibility | Not run (`--history` needs time; a clone build conflicts with other builds) |
| D14/R13 number classes in ch. 2, 5, 7 | Not read line by line |
| Q3-1/Q3-2 re-check | CLS v0.21 was not in the build; do in round 3 |
| Content vs PRD list (D1-D9) | Skipped |
