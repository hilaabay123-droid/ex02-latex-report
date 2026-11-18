# TODO: ClosetTwin Business Plan

Status: ☐ open · ◐ in progress · ☑ done · ⧗ blocked. Each task has **one** owner and a **check** that proves it is done.
Stages and dependencies are in `PLAN.md`.

## S1: Requirements
| ID | Task | Owner | Check | Status |
|---|---|---|---|---|
| T1.1 | 12 or more verified sources → `references.bib` (IEEE) + `writer/sources-notes.md` | writer-se | 29 entries; every DOI resolved, every URL HTTP 200 | ☑ |
| T1.2 | Chart style guide + `python/ct_style.py` + palette swatch PNG | art-se | `python python\palette_swatch.py` writes `docs/screenshots/palette-swatch.png` | ☑ |
| T1.3 | CLS feasibility study + tests t1–t5 + fonts | fix-se | t5 builds; `pdffonts` shows only Playfair, Rubik and LM Math | ☑ |
| T1.4 | Acceptance criteria per QA family | qa-se | `qa/acceptance-criteria.md` v1.1, 103 criteria | ☑ |
| T1.5 | Replace the Playfair instances with official static OFL files (Reserved Font Name) | fix-se | `fonts/SOURCES.md` SHA-256; t5 rebuilds | ☑ |
| T1.6 | Merge into PRD v1.0 | master-se | PRD has §1–§10 | ☑ |
| T1.7 | Red team the PRD (4 reviews) → review log → PRD v1.1 | master-se | 32 findings logged in PRD §10 | ☑ |
| T1.7b | Acceptance criteria v1.2 (red-team items) | qa-se | 112 criteria | ☑ |
| T1.8 | The user answers Q-A…Q-F | user | Answers recorded in PRD §9 | ☐ |
| T1.9 | Verify the GDPR Art. 9 wording on EUR-Lex (+ BIPA if Q-F = yes) in a browser | user | Confirmed, or entry adjusted | ☐ |

## S2: CLS (fix-se)
| ID | Task | Owner | Check | Status |
|---|---|---|---|---|
| T2.1 | Skeleton on `book` oneside + geometry 15.0 cm + fonts by path + `\tracinglostchars=3` + babel `bidi=basic` (v0.1) | fix-se | Test page; `pdffonts` | ☐ |
| T2.2 | `hebrewpage`, Hebrew heading → Rubik, `\pct`, `\usd`, `\ils` (v0.2) | fix-se | The ch. 14 check page renders correctly (viewed as an image) | ☐ |
| T2.3 | Headings in Playfair (lining numerals), chapter opener, TOC, lists (v0.3) | fix-se | TOC page image | ☐ |
| T2.4 | Tables (booktabs, ivory header), captions, stat card, pull quote, `\assumption`, TikZ keys (v0.4) | fix-se | Demo page image | ☐ |
| T2.5 | TikZ style-key list → fix-se | art-se | REQUEST sent with the key names + values | ☐ |
| T2.6 | Cover, inset banner (shipout hook), footer with page number, `\frontmatter`/`\mainmatter`, `\FloatBarrier`, palette-only hyperref (v0.5) | fix-se | 3-page demo: cover with no footer, banner elsewhere | ☐ |
| T2.7 | biblatex IEEE + `\urlstyle{same}` + command list + full example (v1.0) | fix-se | Example builds clean with the 4 commands | ☐ |
| T2.8 | `TEXTWIDTH_IN = 5.906` (15.0 cm) + a fixed canvas, no `bbox tight`, fonttype 42, no fallback (RT-A8, RT-Q4) | art-se | Every figure PDF is exactly 15.0 cm wide; `pdffonts` clean | ☐ |

## S3: QA skills (fix-se writes, qa-se supplies the criteria)
| ID | Task | Owner | Check | Status |
|---|---|---|---|---|
| T3.1 | `qa-super` (runs all families in the book's order, merges reports) | fix-se | Runs on the T2.7 example | ☐ |
| T3.2 | `qa-BiDi` (renders the Hebrew page to PNG; checks B1–B10) | fix-se | Catches a planted reversed word | ☐ |
| T3.3 | `qa-table`, `qa-img`, `qa-code` | fix-se | Each runs on the example | ☐ |
| T3.4 | `qa-typeset` (log: overfull > 1 pt, undefined, missing char), `qa-infra` (files, fresh clone), `qa-cls-version` | fix-se | Each runs on the example | ☐ |

## S4–S5: Skeleton and outline
| ID | Task | Owner | Check | Status |
|---|---|---|---|---|
| T4.1 | `main.tex` (cover fields, front matter, `\input` of 10 chapters, bibliography) | master-se | Compiles | ☐ |
| T4.2 | Chapter stubs `chapters/01-intro … 10-conclusion.tex` + `00-exec-summary-he.tex` | writer-se | Compiles to 10 titled chapters + the Hebrew stub | ☐ |
| T5.0 | Claim-trace table: every statistic with its quote and page (R-13) | writer-se | qa-se spot-checks 5 | ☐ |
| T5.1 | `writer/outline.md`: sections, the claim each proves, its sources, page budget | writer-se | master-se approves against PRD §6 | ☐ |
| T5.2 | `python/data/assumptions.csv`: every financial assumption (prices, CAC, churn, costs), one source of truth | writer-se proposes → art-se owns the file | Every number in ch. 5 and 8 traces to a row | ☐ |

## S6: Figures (art-se)
| ID | Figure | Chapter | Tool | Status |
|---|---|---|---|---|
| T6.1 | F1 TAM/SAM/SOM nested shapes, not to scale, one year per label | 2 | Python/TikZ | ☐ |
| T6.2 | F2 Positioning map (axes from verified vendor columns) | 3 | Python | ☐ |
| T6.3 | F3 Scan + garment specs + fit preference → size data flow | 4 | TikZ | ☐ |
| T6.4 | F4 Roadmap Gantt strip (6 rows) | 7 | TikZ | ☐ |
| T6.5 | F5 5-year projection + break-even (two panels) | 8 | Python | ☐ |
| T6.6 | F6 Sensitivity: break-even month vs. return-reduction effect | 8 | Python | ☐ |
| T6.7 | F7 Risk heat matrix | 9 | TikZ | ☐ |
| T6.8 | Ch. 1 stat cards (no chart unless ≥ 4 comparable sourced values) | 1 | CLS `statcard` | ☐ |

Check for every figure: the style-guide §8 checklist, viewed inside the built PDF.

## S7: Chapters (writer-se), in this order
| ID | File | Pages | Status |
|---|---|---|---|
| T7.1 | `01-intro-problem.tex` | 3 | ☐ |
| T7.2 | `02-market.tex` | 4 | ☐ |
| T7.3 | `03-competition.tex` | 3 | ☐ |
| T7.4 | `04-product-tech.tex` | 4 | ☐ |
| T7.5 | `05-business-model.tex` | 3 | ☐ |
| T7.6 | `06-gtm.tex` (funnel table + pilot design) | 2 | ☐ |
| T7.7 | `07-ops-team-roadmap.tex` | 2 | ☐ |
| T7.8 | `08-financials.tex` (formula (1), assumptions table, sensitivity) | 3 | ☐ |
| T7.9 | `09-risks.tex` | 2 | ☐ |
| T7.10 | `10-conclusion.tex` | 1 | ☐ |
| T7.11 | `00-exec-summary-he.tex` (Hebrew, RTL, exactly 1 page; written **last**) | 1 (front) | ☐ |

Check for every chapter: it compiles, it is within ±1 page of budget, every claim is `\cite`d or `\assumption`, and no forbidden command appears (T3).

## S8–S10: QA, red team, submission
| ID | Task | Owner | Check | Status |
|---|---|---|---|---|
| T8.1 | Full build + `qa-super` round 1 → `qa/reports/01-*.md` | master-se builds, qa-se runs | Report filed | ☐ |
| T8.2 | Fix loop until no blocker or major findings remain | owners per finding | The re-check by qa-se passes | ☐ |
| T9.1 | Red team the PDF from a fresh session (book Prompt 9) | qa-se | 10 weakest points, each with page and quote | ☐ |
| T9.2 | Log each one Adopted/Rejected in PRD §10; fix the adopted ones | master-se | Review log updated | ☐ |
| T10.1 | README: build, MiKTeX package list, skills list + files, structure | master-se | FS8, S3 pass | ☐ |
| T10.2 | Fresh-clone reproducibility build | qa-se | Same page count (FS6) | ☐ |
| T10.3 | Commit the final `main.pdf` + tag | master-se | `git ls-files main.pdf` | ☐ |
| T10.4 | The user's own page-by-page look (book §19.5 #5–6) | user | Sign-off | ☐ |
