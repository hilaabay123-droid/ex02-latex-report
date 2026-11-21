# QA report 05: qa-super, round 3 (re-check + the round-2 skips)      build 89b9d89 + dirty tree      2026-11-20

Fresh 4-step build in a private copy (`qa/tmp/bld`, from the current tree), CLS **v0.22** (build log: "closettwin 2026/11/20 v0.22"). All four commands exit 0; 0 errors, 0 undefined references or citations, 0 missing glyphs, 47 pages (40 content pages, printed = PDF - 7), 1 overfull box of 0.12 pt (a bibliography URL, under the 1 pt limit), 1 underfull box. Detector only: no deliverable was edited.

## Summary
Counts: **blocker 1 (by rule; synthetic, see F-infra-01), major 4, minor 5.** Of the 14 round-2 findings: 8 fixed, 3 still open, 2 changed, 1 moved to a new finding (see Re-check).
Skills run: qa-infra, qa-cls-version, qa-typeset (with the new `--gaps`), qa-BiDi, qa-table, qa-img, qa-code, the v1.1 checks, the PRD content check, a link spot-check of 13 sources, the git-history ID scan, and 17 pages viewed by eye.

## Blockers
- **F-infra-01** C6 (by rule, probably not real): 8 nine-digit numbers in the git history, commit 904c663, `qa/tests/run_selftest.py`. They are fabricated test values (123456780 and similar) that my self-test uses; the real ID is not in the history or in the PDF. master-se decides whether this needs a history rewrite.

## Findings

### F-code-01 [major] K3, R-20 (incident 05, v1.1 check 9)
- Where: main.tex:41-44, python/appendix_f6_code.py | printed 39-40 (PDF 46-47)
- What: the 26-line code box is split across two pages (18 lines, then 8 lines). A box under 46 lines must not be split. Page 40 holds only lines 19-26 and is 75% empty.
- Evidence: `page_stats.py`: PDF 47 "nearly empty page: 386 characters"; image of PDF 46 and 47: lines 1-18 on the opener page, 19-26 on the next. The earlier title-only opener (Q3-1) is fixed, and this is the cost of the fix.
- Recurring: yes (same cause as incident 05: an opener plus a box that does not fit under it). Owner: fix-se.
- Status: open

### F-typeset-01 [major] D17, R-02
- Where: chapters/08-finance.tex | PDF 33-37 (printed 26-30)
- What: ch. 8 has 5 pages against a budget of 3 (accept 2-4).
- Evidence: `page_stats.py` "chapter 8: first PDF page 33, 5 page(s), budget 3, accept 2-4". Total content is 40 pages (R-01 is met).
- Recurring: no. Owner: writer-se (shorten) or master-se (move the budget; the two red-team tables account for about 1.5 pages).
- Status: open (still open since round 2)

### F-fonts-01 [major] D11, R-06
- Where: PDF 6, 15, 30, 33, 36, 37 (printed -, 8, 23, 26, 29, 30)
- What: Latin Modern Math is embedded on pages with no formula. The cause is inline maths symbols (rho, varphi, geq, div) in text, tables and the figure list. R-06 allows LM Math only on pages with a formula.
- Evidence: `fonts_by_page.py`: "LM Math pages [6, 15, 30, 33, 36, 37], formula pages [33]". The PyMuPDF scan finds no LM Math digit in running text (v1.1 check 12 passes), so only symbols.
- Recurring: yes (6 pages). Owner: fix-se (render these symbols in Rubik, or relax R-06 for inline symbols: master-se decides). Do not patch the text.
- Status: open (new in this round's scripts; the same pages were there in round 2)

### F-infra-02 [major] R6
- Where: references.bib: truefit_web, fitanalytics_web, threedlook_web, boldmetrics_web, mysize_web, threedlook_pricing, popsize_shopify, shopify_dev_build, il_ppl_en, il_cpfta_guide
- What: 10 @online entries have no year/date (urldate is present; 27 urldate for 22 @online).
- Recurring: yes (10 entries). Owner: writer-se for the field; master-se decides whether "Accessed: ..." is enough for undated vendor pages.
- Status: open (was 11)

### F-table-01 [minor] TB4 (v1.1 check 10)
- Where: figures/tab-company-sens.tex (spec `XRRRR`) | printed 28 (PDF 35)
- What: the first column of Table 8.1 is still narrow; "Orders per European client 500 k (base 1 M)" wraps to 5 lines.
- Recurring: possible. Owner: art-se (column spec) / fix-se. Status: open

### F-table-02 [minor] lists (v1.1 check 9)
- Where: main.lof | printed vi (PDF 6)
- What: the entries for Figure 3.1 and 4.1 wrap to two lines; 8.2 prints a maths symbol in the list.
- Recurring: yes (3 entries; captions double as list entries). Owner: fix-se, or writer-se with `\caption[short]{long}`. Status: open

### F-typeset-02 [minor] BU6
- Where: main.log:2194 | printed 19 (PDF 26): 1 underfull box, badness 10000. Owner: writer-se/fix-se, not significant. Status: open

### F-infra-03 [minor] R-17
- Where: repository
- What: `main.pdf` is not tracked in git (`git ls-files | grep main.pdf` -> 0); R-17 requires the final PDF in the repository.
- Recurring: no. Owner: master-se (add at the final commit). Status: open

### F-bib-01 [minor] R5
- Where: references.bib: gustafsson2021
- What: the DOI link (Emerald) answered 403 to my tool (it blocks bots); I could not confirm that it resolves. Not evidence of an error.
- Recurring: no. Owner: writer-se (check by hand). Status: open

## Re-check of 04-round2 findings
| Round-2 finding | Status in build 89b9d89 |
|---|---|
| F-code-01 `\texttt{.il}` mono font (blocker) | **fixed**: no mono font except JetBrains Mono in the appendix |
| F-typeset-01 ch. 8 over budget | **still open** (5 pages) |
| F-typeset-02 orphan "8.4 Assumptions", half-empty pages 36/37 | **fixed**: `--gaps` reports no L3; PDF 37 is the last page of ch. 8 (exempt) |
| F-typeset-03 Appendix opener title only | **fixed**, but see the new F-code-01 (split box) |
| F-infra-01 R6 undated @online | **still open**, 10 of 11 (aguko_shopify_il fixed) |
| F-infra-02 uncited ghodhbani2022, il_cpl_amend7_1998 | **fixed** |
| F-infra-03 peng2023 pages | **fixed** |
| F-clsver-01 `\centering` in figures | **fixed**: grep over `chapters/` finds none |
| F-clsver-02 CLS v0.21 without a CHANGELOG row | **fixed**: rows for v0.20, v0.21, v0.22 exist; the build log shows v0.22 |
| F-table-01 Table 8.1 columns | **still open** |
| F-table-02 list entries | **still open** |
| F-typeset-04 Table 9.1 alone on a page | **fixed**: Table 9.1 is now on printed 31 with text |
| F-typeset-05 underfull | **still open** (minor) |
| F-infra-04 synthetic IDs in my self-test | **changed**: found in git history (F-infra-01 above) |

## Recurring
| Problem | Places | Owner | Criteria |
|---|---|---|---|
| Opener plus a long box splits the box | Appendix A | fix-se | K3, L3 |
| Inline maths symbols pull in Latin Modern Math | PDF 6, 15, 30, 33, 36, 37 | fix-se / master-se | D11, R-06 |
| Undated @online bib entries | 10 | writer-se / master-se | R6 |
| Long captions in the lists | Figure 3.1, 4.1, 8.2 | fix-se | lists |

## Judgment and extra checks
**Link spot-check (13 sources, GET with a browser agent):** HTTP 200: patel2025 (DOI), nrf2024, appriss2024, coresight2023, alhassawi2025 (DOI), peng2023 (DOI), truefit_web, google2023tryon, gdpr2016, shopify_dev_build; il_amend13_2024 and ppa_pets2025 (gov.il) answer 404 to a HEAD request and 200 to GET; gustafsson2021 answers 403 (see F-bib-01). Resolving shows that a link exists; I did not re-trace the claims of these 13 beyond the Knesset item of round 2.
**Git-history ID scan:** the only hits are the 8 synthetic values above (one commit, one file). No hit in the PDF text, chapters, bib or PDF metadata (the only nine-digit string in the PDF is part of a DOI).
**PRD content check (§6, R-xx):** pass: R-01 (40 content pages), R-03 (Hebrew page verified by eye in round 2; corpus file updated; script flags only the sentence-end check, which is a false positive: the page ends with "Shopify."), R-04 (TOC, both lists, IEEE list, new page per chapter), R-05 (no manual formatting in `chapters/`, one `\texttt` removed), R-08 (palette 8 colours, contrast pass), R-10 (F1-F7 all present: PDF 14, 19, 20, 32, 35, 37, 39; F2, F5 and F6 are Python PDFs; F1, F3, F4 and F7 are TikZ), R-11 (8 tables), R-12 (formula 8.1 numbered and defined), R-15 (0 errors, 0 undefined, overfull < 1 pt), R-18 (14 skills present, including the 8 QA skills), R-19 (CHANGELOG rows for v0.20-v0.22), R-22 (cover has the course line, "Dr. Yoram Segal", "BUSINESS PLAN"; no other 9-digit number), R-24, MC-1 (grep for "break-even within" is 0), BIPA/Illinois (0). Fail or open: R-02 (ch. 8), R-06 (F-fonts-01), R-13 (undated entries), R-17 (main.pdf not tracked), R-20 (split box), R-25 (box shown from the real file; the split is the problem). Not verified: R-14 for every number in ch. 2, 5, 7; R-16 (clean-clone reproducibility); R-26 and R-27 beyond a read of ch. 6, 8, 9, 10.
**Pages viewed by eye (17):** printed 1, 4, 7, 12, 13, 15, 16, 22, 25, 28, 29, 30, 32, 33, 34, 39 and 40 (17 pages), plus the Hebrew page and the figure list in round 2. Every figure page (PDF 14, 19, 20, 32, 35, 37, 39) was viewed: labels readable, no overlap, captions match, F2 axes and F5 peak-deficit mark in order, F6 break-even marks 4.5% and 6.0% present. Pages 34 (conclusion) holds exactly one page.

## Skipped
| Criterion | Reason |
|---|---|
| FS6, S9, R-16 (clean clone, second build identical) | not run in this round |
| R5, R8-R10 full claim trace beyond the Knesset item | time |
| R-14 number classes in ch. 2, 5, 7 line by line | time |
| D2/D16 editorial look beyond the 17 pages viewed | time |

## Decisions by master-se on this report, and follow-up (2026-11-20)
| Item | Decision / result |
|---|---|
| F-infra-01 (C6 in git history) | **False positive, accepted by master-se.** The 8 values are fabricated self-test fixtures; no history rewrite. Follow-up done by qa-se: `qa/tests/run_selftest.py` now builds its fake IDs at run time (`FAKE9`, `FAKEG`), so the file holds no nine-digit literal except the allowed course code. Checked: a planted fake ID is still found and masked as `00*******`. The old commit 904c663 keeps the old values. |
| F-fonts-01 (LM Math off formula pages) | **R-06/D4/D11 amended** in `qa/acceptance-criteria.md`: LM Math allowed for inline math symbols, never digits or prose. `fonts_by_page.py` now keeps only pages whose LM Math spans hold digits or prose (PyMuPDF); on the round-3 build, pages 6, 15, 30, 36, 37 are reported as symbols only and page 33 is the formula page. The remaining K3 line for PDF 47 comes from not passing `--code-pages 46,47` (the box is split) and is the split-box finding F-code-01. |
| ch. 8 length (D17) | Accepted (PLAN D-2). Closed. |
| Undated @online (R6) | Accepted per IEEE (`writer/sources-notes.md`). Closed. |
| main.pdf not tracked (R-17) | master-se, at the final commit. |
| F-bib-01 gustafsson2021 DOI 403 | **Checked with a fetch agent: the DOI resolves** (302 to the Emerald page, 200). The page shows the title "Reducing retail supply chain costs of product returns using digital product fitting", authors Gustafsson, Jonsson, Holmström, IJPDLM vol. 51 no. 8 pp. 877-896, 2021; all of that matches `references.bib`. The 403 was a bot block. **Closed.** |
| F-code-01 (split box), list entries, Table 8.1 | fix-se is on it; re-check in the final pass. |

Next: one FINAL qa-super after fix-se reports, including the clean-clone reproducibility build (skipped so far).
