# QA report 06: final qa-super (number consistency, Table 8.1, F5, Hebrew page, reproducibility)      build fedf4b3 + dirty tree (186 changed paths)      2026-11-21

Inputs: the root `main.pdf` (48 pages, built 2026-11-21 17:59; no `.tex/.cls/.bib` is newer, so the build is not stale), CLS **v0.23**. I did **not** rebuild in the root. For reproducibility I built a private copy (`qa/tmp/fin2`, see FS6). Detector only: no deliverable was edited.

## Summary
Counts: **blocker 0, major 5, minor 6.** (Round-3 blocker F-infra-01, the nine-digit number, is now explained: it is the course number printed on the cover, not a personal ID; see Tool notes. It is not counted.)
The money numbers in the model, the chapters, Table 8.1, the Hebrew page, F5 and F6 agree with `python/data/model_out.csv` and `company_sensitivity_out.csv`, with **two stale values** (F-super-01 in figure F1, F-super-02 in ch. 2) and **one gap** (F-super-03: pilot cash cost and cost of goods are in the model but not in ch. 8).
Skills run: qa-infra, qa-cls-version, qa-typeset (`--gaps`), qa-BiDi, qa-table, qa-img, qa-code, the PRD traps, the number audit (below) and 11 pages seen by eye (PDF 2, 6, 14, 34, 35, 36, 37, 38, 43, 48).
Build facts (both root and private copy): 0 errors, 0 undefined references or citations, 0 missing glyphs, 48 pages (36 content pages for ch. 1-10: PDF 8-43; printed = PDF - 7; "of 41" counts the references and the appendix), 1 overfull box of 0.12 pt (ch. 10, `main.log` line 2225, under 1 pt), 2 underfull boxes.

## Blockers
None.

## Findings

### F-super-01  [major]  D14, R-14 (number consistency, a figure against the model)
- Where:     `figures/f1-market.tex:25` | PDF page 7 (14), Figure 2.1
- What:      the Europe SOM box says "year 5: subscription $0.65 M", the model's year-5 European subscription revenue is $324,000.
- Evidence:  `f1-market.tex:25` `\textbf{SOM}, year 5: subscription \$0.65\,M`. Model (ch. 8, ch. 2 line 59, `model_out.csv` D48_5): 9 billed clients x 1,000,000 x 0.036 = 324,000; with the Israeli 54,000 the subscription total is 378,000. 0.65 M is the old full-year figure (18 x 36,000 = 648,000, the "648" of the stale list) from before the half-year billing change. The figure also contradicts ch. 2 on the same page ("European subscription revenue is $324,000").
- Recurring: no (one figure). Owner: art-se (`figures/f1-market.tex`). Suggested value: `\$0.32\,M` (or `\$0.324\,M`).
- Status:    open

### F-super-02  [major]  D14, R-14 (stale value in the text)
- Where:     chapters/02-market.tex:25 | PDF page 7 (14)
- What:      "the cumulative operating result at the end of year 3 ... is a deficit of $1.04 million"; the model gives $1,295,250 (about $1.30 million).
- Evidence:  `company_sensitivity_out.csv` base, `cum_y3_usd` = -1,295,250. The 1.04 M equals the old value before the three new cost lines (1,295,250 - 94,000 - 79,000 - 79,000 = 1,043,250), so the sentence was not updated in the model rebuild.
- Recurring: no. Owner: writer-se. Status: open

### F-super-03  [major]  D14, R-14, D15 (the model has cost lines the chapter does not state)
- Where:     chapters/08-finance.tex:13-17 and the Table 8.2 (printed 30, PDF 37); chapters/02-market.tex:25 (cross-reference)
- What:      ch. 8 says "Besides payroll, the model has three cost lines" (94, 79, 79, 184, 224 thousand). The operating result also contains **cost of goods** (D21: 0, 3,750, 7,500, 9,375, 78,750) and a **pilot cash cost** (D28: 12,000, 12,000, 12,000, 49,500, 73,500, i.e. $3,000 per direct pilot). A reader cannot reproduce the stated results from the text.
- Evidence: Year 1 from the text: 10,000 - 270,000 - 94,000 = -354,000, but the text says -366,000; the 12,000 difference is the pilot cash cost. Year 5: 458,000 - 78,750 - 1,080,000 - 224,000 - 73,500 = -998,250 matches only with both lines. Ch. 2 line 25 says "we assume a cash cost of $3,000 for a direct pilot (Chapter 8)", but `grep "3,000" chapters/08-finance.tex` finds nothing, and Table 8.2 has no row for it. Bar totals in F5 (about 376 thousand in year 1) include both lines.
- Recurring: no. Owner: writer-se (state the two lines and the $3,000 in 8.2 and Table 8.2, or change the sentence "three cost lines"). Status: open

### F-super-04  [major]  D17, L4 (chapter 10 spills; chapter 8 is double its budget)
- Where:     chapters/10-conclusion.tex | PDF page 43 (printed 36); chapter 8 PDF 33-38
- What:      the conclusion ends with 2 lines alone on PDF page 43 (161 characters, page about 98% empty), so chapter 10 has 2 pages against "exactly 1". Chapter 8 has 6 pages against a budget of 3 (accept 2-4); its last page (PDF 38, Figure 8.2 alone) is 63% empty.
- Evidence:  `page_stats.py --toc main.toc --front 7`: "chapter 10: first PDF page 42, 2 page(s), budget 1, accept 1-1"; "chapter 8: first PDF page 33, 6 page(s), budget 3, accept 2-4". Image PDF 43: "five years. The Israeli pilots come first ... we stop and do not scale." and nothing else. Content total is 36 pages, so R-01 (>= 25) holds; the budget table in PRD 6 is not updated for the red-team additions (company sensitivity text and table).
- Recurring: no. Owner: writer-se (cut about 3 lines of ch. 10, or ch. 8) or master-se (move the budget in `PLAN.md`; the chapter 10 line count cannot be accepted as it is: a 2-line page).
- Status:    open (chapter 8 budget: open since round 2)

### F-infra-02  [major]  R6 (carried from round 3, F-infra-02)
- Where:     references.bib: truefit_web, fitanalytics_web, threedlook_web, boldmetrics_web, mysize_web, threedlook_pricing, popsize_shopify, shopify_dev_build, il_ppl_en, il_cpfta_guide
- What:      10 `@online` entries have no `year` or `date` (`urldate` is present, and the printed entries read "Accessed: ... [Online]").
- Evidence:  `bib_vs_cited.py` "entry '...' (online) is incomplete: missing year/date", 10 hits. Not changed since round 3.
- Recurring: yes (10 entries, one cause). Owner: writer-se for the field; master-se decides whether "Accessed" is enough for undated vendor pages (IEEE allows it). Status: open

### F-super-05  [minor]  TB4, TB5 (Table 8.1 and Table 8.2 look)
- Where:     figures/tab-company-sens.tex | printed 28 (PDF 35); chapters/08-finance.tex Table 8.2 | printed 30 (PDF 37)
- What:      Table 8.1: the first column is still narrow: "Scenario (US$ thousand)" takes 3 lines and "Pilot-to-paying 35%" and "Low-touch 250 k" wrap to 2 lines each, though the other columns have spare width. Table 8.2: every text column is the same width, so 8 of 13 rows wrap to 2 lines ("Cost per person-year", "Below the 53% who name fit").
- Evidence:  image PDF 35 and 37. v0.23 changed the `W` weight from 1.6 to 1.2 (`closettwin.cls` working tree), which narrows the label column; the by-eye result is better than round 3 (5 lines) but not clean. The numbers in Table 8.1 are correct (every cell checked against `company_sensitivity_out.csv`, see Number audit).
- Recurring: yes (2 tables with one cause: column weights in the `X`/`W` types). Owner: fix-se (CLS column types); art-se for the spec of `tab-company-sens.tex`. Status: open

### F-super-06  [minor]  typography of negative amounts
- Where:     chapters/08-finance.tex:13 (5 amounts), :33 (2 amounts) | printed 27 and 29 (PDF 34, 36)
- What:      negative money prints as "$-366,000" (a hyphen after the dollar sign) in 7 places; the usual form is "-$366,000" or "−$366,000" (and in the table the minus is the proper math minus).
- Evidence:  `grep -o 'usd{-[0-9,]*}' chapters/*.tex`: -366,000, -426,750, -502,500, -955,375, -998,250 (line 13); -570,750, -998,250 (line 33). PDF text "$-366,000".
- Recurring: yes (7 places, the `\usd` macro does not handle a sign). Owner: fix-se (macro), not a text edit. Status: open

### F-super-07  [minor]  model_out.csv traceability
- Where:     python/data/model_out.csv rows D14, D15, D16, D17 | no page
- What:      four rows from the old global model remain: TAM orders 9,075,625,000, TAM fee pool 326,722,500, SAM share 0.573, "SAM fee pool" 74,884,797. No chapter or figure uses them; the chapters use D34-D37 (Israeli SAM 198,000; Europe TAM 81.68 M; Europe SAM 32.67 M). A reader of the CSV finds two different "SAM fee pool" figures.
- Evidence:  `grep "326\|74\.9\|9\.07" chapters figures` finds nothing; `model.py:115-118`.
- Recurring: no. Owner: art-se (drop or relabel the rows). Status: open

### F-typeset-01  [minor]  BU6
- Where:     main.log:2201 | printed 19 (PDF 26): underfull box badness 10000 (and one more at 2200).
- Evidence:  `overfull.py main.log`: "Underfull boxes: 2". Not visible by eye. Recurring: no. Owner: writer-se/fix-se, not significant. Status: open (carried)

### F-super-08  [minor]  by-eye, Hebrew page and lists (no defect; recorded as checks)
- See "Judgment checks": Hebrew page, LOF/LOT and Appendix A pass. Listed here only so that the count is traceable: the scripts' B4 and K4 and R2 hits are false positives (Tool notes).

## Recurring
| Problem | Places | Owner | Criteria |
|---|---|---|---|
| Table column weights (label column wraps) | Table 8.1 (3 wrapped labels), Table 8.2 (8 wrapped rows) | fix-se | TB4 |
| Negative money printed "$-N" | ch. 8 lines 13 and 33, 7 amounts | fix-se (`\usd`) | TB5 / typography |
| @online entries without a year | 10 entries | writer-se, master-se decides | R6 |

## Judgment checks

### Number audit (priority 1)
Method: every money, count, percent and ratio in `chapters/*.tex`, `figures/*.tex`, the Hebrew page and the F5/F6 images was compared with `model_out.csv` (rows D01-D48, X01, A33a) and `company_sensitivity_out.csv`; derived sums were recomputed.

| Claim (where) | Text | Model | Result |
|---|---|---|---|
| Revenue y1-y5 (ch. 8, F5) | 10,000 ... 458,000 | D20 | match |
| Operating result y1-y5 (ch. 8) | -366,000; -426,750; -502,500; -955,375; -998,250 | D23 | match; recomputed from revenue - D21 - D22 - D44 - D28: match |
| Cumulative deficit, ask (ch. 8, 10, Hebrew, F5 "3.25 M") | 3,248,875; 3,898,650 (= x1.2); 3.9 M; 3.25 M | D24, D25 | match |
| Cost lines 94/79/79/184/224 (ch. 8) | as text | D44 (= D40+D41+D42+D43) | match, but see F-super-03 |
| Subscriptions 54,000 / 324,000 / pilot fees 80,000 (ch. 2:59, ch. 8) | sum 458,000 | D20_5 | match |
| 44 clients, 18 clients, $28,500 contribution (ch. 8, 10, Hebrew) | as text | D46 = 44.03, D47, `european_clients_end_y5` 18 | match |
| Year-3 deficit (ch. 2:25) | 1.04 M | cum_y3 1,295,250 | **stale (F-super-02)** |
| F1 Europe SOM (figure 2.1) | 0.65 M | 324,000 | **stale (F-super-01)** |
| Table 8.1 (7 rows x 5 columns = 35 cells) | thousands | `company_sensitivity_out.csv` | all 35 match (round half up; -1,126,500 -> -1,127) |
| Text of the rows in ch. 8 (344,600; 4,034,595; 296,000; 4,052,550; 275,750; 4,071,788; 104,000; 4,017,450; 4,047,420; 998,000; -570,750; 3,352,375; 4,022,850; 30 clients) | as text | same csv | all match |
| Spread of the ask, "0.17, 0.15 and 0.12 to 0.15 million" (ch. 8) | as text | ask minus 3,898,650 = 173k, 154k, 119-149k | match |
| Israeli SAM 198,000, 5.5 M orders, 0.67 M, Europe 2.27 B / 81.7 M / 32.7 M / 32.9 M, share 1.1% (ch. 2, F1) | as text | D33, D34, D34b_tam, D35-D37, D27 = 1.15% | match |
| Funnel table 6.1 (17 Israeli pilots; 36 and 60 European; 22/22/22/417/678; capacity; 5/4/3/34/41%) | as text | `funnel_check_out.csv` | match |
| MDE 7.8%, 6.1%, 19%, break-even 6.03% / 4.52%, 12,000 per arm (= 2 x 6,011) (ch. 6, 8, 10, Hebrew) | as text | D19i, D19e, D19i2, D07a, D07b, D18 | match |
| $0.0996, $0.66, $6.80, $24.29, $99,600, 79% margin, 66.6x -> "50 to 67 times" (ch. 5, 9) | as text | D05, D04, D45, D09, D12, D13 | match |
| Hebrew page (685-890 B, 24.4%, 53%, 17%, 6.80, 0.036, 0.13, 7.8%, 0.2 M, 0.46 M, 3.25 M, 44, 18, 3.9 M, 20%) | | | all match; no stale value |

Stale-value grep (`782 | 648 | 2.33 | 2.8 M | 37 clients | year 6`) on `chapters/`, `figures/*.tex`, `python/*.py` and the PDF text: **0 hits** in text. The one that survives in substance is the 648 k, as 0.65 M in F1 (F-super-01) and the 1.04 M (F-super-02). Note, no claim of a year 6 or of break-even in a stated year remains; ch. 8 says "we do not say in which year it would come".
Notes without a finding: (a) Israeli paying clients: ch. 6 says "about 6", the funnel gives 7.1 new clients in years 2-5; ch. 8 covers it with "Israeli client numbers are year averages". (b) The "$0.04 / $0.03" tier prices round the break-even shares to "40% / 30%"; the model values are 40.2% and 30.1%. Both are consistent with the text.

### Table 8.1, the sensitivity table and F5 by eye (priority 2)
- Table 8.1 (PDF 35): numbers right-aligned, minus signs math, thin-space thousands, header row 3 lines. By eye the table is readable; see F-super-05 for the wrapped labels.
- F5 (PDF 35): panel (a) revenue vs total cost, y5 revenue about 458 and cost about 1,456 (= 78.75 + 1,080 + 224 + 73.5), y1 cost about 376; panel (b) the cumulative line ends at -3.25 M with the label "Peak deficit US$3.25 M". Hebrew absent, fonts Rubik. Matches the caption ("no operating profit in the horizon"). Pass.
- F6 (PDF 38): break-even marks 4.5% and 6.0%, base case 15%, labels readable; the figure stands alone on its page (see F-super-04). Matches caption and ch. 8.
- LOF/LOT (PDF 6, 7): 3.1 "Positioning of the vendors, our reading of vendor pages", 4.1 "Data flow", 8.2 "Retailer's economics against the achieved reduction": each on one line, no maths symbol, no wrap. Table 3.1, 8.1 and 8.2 also one line. **Pass** (round-3 F-table-02 fixed).
- Appendix A (PDF 48, printed 41): one page, 26 lines, all 26 lines of `python/appendix_f6_code.py` found in the page text; only JetBrains Mono on this page. **Pass** (round-3 F-code-01 fixed). The cap at the bottom of the page is empty space, as expected for the last page.
- Hebrew page (PDF 2): title, subtitle and 4 paragraphs right-to-left; Latin runs (ClosetTwin, B2B, AI, Appriss, NRF, Coresight, IMARC, GDPR, Shopify) and numbers in the right order; the final "Shopify." keeps its full stop on the correct side (zoomed at 200 dpi); percent and dollar figures read correctly; footer "עמוד ii מתוך 41". `bidi_bbox_check`: runs and reverses pass; no Latin run is reversed. **Pass.**

### PRD traps and class checks
`break-even within` = 0; `BIPA|Illinois` = 0; 24.52% (online sales share, ch. 1:12), 24.4% (return rate) and 53% (fit reason) are kept separate. `\usd \pct \ils` are used throughout. Fonts: Playfair, Rubik, LM Math (pages 15, 30, 34-38, symbols only, allowed by the R-06 amendment), JetBrains Mono on page 48 only. Margins min 2.9 cm left/right. R-17: `main.pdf` is now tracked in git (modified: commit the final build).

### CLS version and logging
`closettwin.cls` says v0.23 and `fix/CHANGELOG.md` has the v0.23 row (2026-11-20, qa-se round 3, F-code-01, F-fonts-01, Table 8.1, LOF/LOT). The working tree has a 4-line change to `W`/`ctnumcols` (weight 1.6 -> 1.2) that matches this row. Skills: qa-code, qa-table, qa-typeset are v1.2, qa-BiDi, qa-img, writer v1.1. Pass.

### FS6: reproducibility build (priority 3)
Copy of the working tree (all tracked and untracked non-ignored files, without `qa/`, `prompts/`, `docs/`), built in `qa/tmp/fin2` with the 4-step sequence: exit codes 0, 0, 0, 0; 48 pages; 0 errors, 0 undefined; 1 overfull (0.12 pt), 2 underfull. `pdftotext -layout` of the copy is **byte-identical** to the root `main.pdf` text, same font list, same warning counts. **Pass.**
Limit: this is the working tree, not a clone of HEAD (fedf4b3). HEAD does not contain the final model, the chapters or the figures; a clean clone of HEAD would not reproduce this PDF until master-se commits. Re-run `git clone` once after the final commit (it takes about 3 minutes).

## Tool notes (my scripts, not deliverable defects)
- `id_scan.py` C6: 1 hit (+19 in history) of a nine-digit number in `prompts/log/2026-11-20.md`. It is the course number "Generative AI for Management (8…2)", which PRD R-22 requires on the cover; it also appears in PRD.md, docs and skills. Not a personal ID. I will add the course number to the allow list in `id_scan.py`; no action for master-se. The round-3 history finding (fabricated test values in `qa/tests/run_selftest.py`, commit 904c663) is separate and was accepted by master-se.
- `code_diff.py` K4 (main.tex) and `bib_vs_cited.py` R2 ("27 citations printed as [Online]") are script errors: I passed the wrong source to `code_diff.py`, and R2 counted the "[Online]" tag of the reference list. Checked by hand: 26 of 26 code lines present; citations in the text are numbers ([24], [6], [18] ...).
- `bidi_bbox_check.py` B4 ("no Latin run ending a sentence"): script false negative, the by-eye check above shows "Shopify." at the sentence end.
- `page_stats.py --gaps` L3 at PDF 16, 23, 38 are the last pages of chapters 2, 4 and 8 before the next chapter opener; only PDF 38 is a real concern (F-super-04).

## Skipped
- TB5 sums: `table_sums.py` found no "Total" row in the 7 tables (nothing to recompute). 
- Link spot-check of the bibliography URLs: not repeated this round (no change in `references.bib` except what round 3 saw); the bib has 39 entries, 39 cited keys.
- Pages not seen by eye this round: 1, 3-5, 8-13, 15-32, 33, 39-42, 44-47 (seen in rounds 2-3, text unchanged except ch. 8 and 10 and the figures F1/F5).

## Re-check (round 3 findings)
| Round 3 | Status in this build (fedf4b3 + tree) |
|---|---|
| F-code-01 code box split over 2 pages | fixed: one page (PDF 48) |
| F-typeset-01 chapter 8 = 5 pages | still open: now 6 pages (F-super-04) |
| F-fonts-01 LM Math on non-formula pages | fixed by the R-06 amendment (symbols allowed) |
| F-infra-02 undated @online | still open (10 entries) |
| F-table-01 Table 8.1 first column | partly fixed: 3-line label header and 2 wrapped rows left (F-super-05) |
| F-table-02 LOF entries 3.1, 4.1, 8.2 | fixed |
| F-typeset-02 underfull, p26 | still open (minor) |
| F-infra-03 `main.pdf` not tracked | fixed (tracked; commit the final build) |
| F-infra-01 C6 test values (history) | accepted by master-se |
| F-bib-01 gustafsson2021 | not re-checked this round (skipped, see above) |

## Sign-off (final)
Open blocker: 0. Open major: 5 (F-super-01, -02, -03, -04, F-infra-02). The release is not clean until F-super-01 to -04 are fixed and a build re-checked; F-infra-02 needs a decision from master-se. The six 19.5 items: (1) build clean (pass), (2) numbers consistent (2 stale, 1 gap), (3) Hebrew page (pass, PDF 2), (4) figures and tables by eye (pass; F-super-05 minor), (5) page-by-page view (11 of 48 pages this round; rest rounds 2-3), (6) reproducibility (pass on the working tree; repeat after commit).

Human sign-off lines:
Reviewer: ____________________  Date: ____________
Course group (Hila Abay, Shirel Giladi): ____________________  Date: ____________
