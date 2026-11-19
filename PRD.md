# PRD: ClosetTwin Business Plan (Assignment 02)

| | |
|---|---|
| **Version** | **2.1** (**v2.1 = IL-M1: the financial model is the Israel → Europe model; ask about $2.8 M, no operating profit inside five years**; v1.1 = red team, 32 findings; v1.2 = claim-trace corrections; v1.3 = outline decisions; v1.4 = model check; v1.5 = coherent funnel; **v2.0 = the user's answers Q-A…Q-F: Israel beachhead, code appendix**; see §10) |
| **Owner** | master-se |
| **Date** | 2026-11-19 |
| **Inputs** | `prompts/03-expert-committee.md` (user decisions) · `ref/BIU26-27-A-ex02-pdf-via-LaTex-print.pdf` (binding) · `ref/preparation-report-book.pdf` Part B ch. 13–19 · `ref/Multi-Agent-With-Claude.pdf` · committee reports `writer/sources-notes.md` (R1+R2), `art/chart-style-guide.md` (A1), `fix/cls-feasibility.md` (F1, F1b), `qa/acceptance-criteria.md` **v1.2** (112 criteria), `qa/reports/01-RT1-prd-redteam.md` |
| **Topic approval** | The assignment lists a "business plan" among its recommended topics (§2 box), so no special approval is needed |

## 1. Vision
An investor-grade **business plan for ClosetTwin**, a B2B AI virtual fitting room. Fashion e-commerce sites embed it.
**The beachhead market is Israel**, and **Europe is the expansion stage** (UD-6).
The shopper scans their body with a phone camera and gets a size recommendation that also takes in the garment's specs
and the shopper's fit preference. The **hypothesis** the plan sets out to prove is that this cuts fit-related returns.
**Privacy is part of the product:** ClosetTwin scans **for fit, not for identification**. It is built privacy-by-design for
Israel's Privacy Protection Law, Amendment 13 (in force since 14 Aug 2025), which classes biometric data as "data of special
sensitivity". The plan argues this is a **competitive advantage**, not just a compliance cost (UD-7).

The document is also the proof of the course's skills:
- a reproducible LuaLaTeX build from one custom CLS
- perfect Hebrew/English BiDi
- a Vogue-inspired editorial look
- QA run by skills, with recurring problems fixed at the source

*ClosetTwin is a fictional company created for this assignment. Every number is **sourced**, **derived** (from a source
plus our assumption) or **assumed**, and is labeled that way.*

**The evidence, stated exactly as the sources state it** (RT-W1):
- About a quarter of online-sales dollars are returned (24.52% of all online sales) [appriss2024]. Coresight's
  survey figure for **online apparel** is 24.4% [coresight2023].
- In a 2023 survey of 100 US apparel decision-makers, **53% named size/fit as the top return reason** [coresight2023].
- In a footwear case model, up to 80% of fit-related return cost could be avoided **at an assumed 80% verification rate**
  [gustafsson2021]. This is a scenario, not a measured result, and it never goes on a stat card as a promise.
- **Counter-evidence that we disclose:** in 496k items, size-finder users were 0.65% *more* likely to return, while their
  customer lifetime value was 7.51% higher [patel2025]. So the benefit is a hypothesis tested by a pilot (ch. 6), and the
  financials survive a zero effect (ch. 8 sensitivity).

## 2. Audience
| Reader | Needs from the document |
|---|---|
| Dr. Segal (the grader) | Every binding requirement met and easy to find, a clean build, and the CLS and skills used instead of hand patches |
| Investor persona (the implied reader: an Israeli seed investor) | The problem in numbers, an honest **Israeli** market size with a credible path to Europe, a defensible product, the revenue logic, survivable financials, and the risks with mitigations, including Amendment 13 |
| Hebrew-speaking stakeholder | A one-page Hebrew executive summary that reads naturally in RTL |

## 3. Fixed decisions (the user's; not open to change)
- The body is in **English, LTR**, with **at least 25 content pages**. Content means chapters 1–10. Front matter (including the Hebrew page) and the references are not counted.
- There is **one Hebrew executive-summary page**: RTL, with English brand names and numbers inside the Hebrew text.
- The style takes its inspiration from **fashion magazines (Vogue)**: clean, airy, not noisy, with touches of trendy color.
- The **fonts** are in `fonts/` (OFL). **Playfair Display** is for English headings. **Rubik** is for the English body and *all* Hebrew text.
- The **palette** is ink `#111111`, ivory `#F7F3EE`, mocha `#A47864` and powder pink `#E8C6C0`.
- The **page budget** is in §6. For excellence: a banner and a footer, plus at least one figure, one table and one formula. Graphs come from Python,
  diagrams from TikZ, and there are no internet images.
- Only real, verifiable sources are used. Financial figures are labeled as assumptions.

**The user's answers, 2026-11-18 (Q-A…Q-F; also fixed):**
- **Q-A:** the tints mocha-deep `#6B4B3D` and mocha-pale `#D3BBAE` are **approved**.
- **Q-B:** the **page is white**. Ivory appears **only on the cover and inside boxes**.
- **Q-C:** **Latin Modern Math is allowed inside formulas only**.
- **Q-D:** there is **one code box**: an appendix with the Python code that generates one of our charts, in **JetBrains Mono (OFL, in
  `fonts/`), for code only**. The reason: `qa-code` is a required skill.
- **Q-E:** the cover lists **Hila Abay, Shirel Giladi**, group code **sg00ha11**, the course **Generative AI for Management (875523402)**,
  the lecturer **Dr. Yoram Segal**, and the date. **No ID numbers anywhere: the repo is public.** The team chapter lists **roles only**.
- **Q-F:** the target market is **Israel (beachhead) → Europe (expansion)**. **BIPA is dropped.** The primary legal framework is **Israel's
  Privacy Protection Law, Amendment 13** (in force since 14 Aug 2025; biometric data is "data of special sensitivity"). **GDPR Art. 9
  is a secondary risk** (Israeli sites selling to EU customers). The text argues that scanning for fit, not identification, plus
  privacy-by-design, is a competitive advantage.

## 4. Technical architecture (proved by compiling `fix/tests/t5`)
| Topic | Decision |
|---|---|
| Template | **`closettwin.cls` based on `book` (oneside)** (RT-F1). This gives `\frontmatter` (roman) / `\mainmatter` (arabic 1), `\chapter`, a new page per chapter and `\chaptermark` for the banner |
| Engine | LuaLaTeX (MiKTeX 25.12) + biber 2.21 + biblatex 3.21. The CLS states the minimum package dates (`\NeedsTeXFormat`, `\RequirePackage[date]`) (RT-F2) |
| BiDi | **babel `[english,bidi=basic]`** + `\babelprovide[import,onchar=ids fonts]{hebrew}`, in a `hebrewpage` environment. *Rejected:* polyglossia and babel `bidi=default`. Both reverse Latin text and digits inside Hebrew (proved in t1/t2) |
| Fonts | `fontspec` loads the fonts by relative path from `fonts/` as static TTFs. **Playfair Display v1.200 is the official unmodified static release** (its Reserved Font Name requires this). Rubik instances are generated (it has no Reserved Font Name). Provenance and SHA-256 are in `fonts/SOURCES.md` (RT-F8). Playfair has no Hebrew, so Hebrew headings switch to Rubik automatically. **JetBrains Mono (OFL, official static release) is used for the code box only** (UD-4) |
| Missing glyphs | `\tracinglostchars=3`, so any missing glyph is a build **error**, not a silent warning (RT-F4) |
| Banner / footer | Drawn with the kernel `shipout/background` hook. No TikZ `remember picture`, so no extra pass is needed (RT-F6). Design in §5.3 |
| Floats | `\FloatBarrier` at each chapter's end, `\raggedbottom`, and tuned float parameters (RT-F7) |
| Bibliography | `biblatex` `style=ieee`, `backend=biber`, `csquotes`. URLs in Rubik (`\urlstyle{same}`). The bibliography is set in a smaller size so it fits 2 pages |
| Public macros | `\pct{}`, `\usd{}`, `\ils{}`, `\sourced`/`\derived`/`\assumed` tags (3 classes, RT-W8/RT-Q6), `hebrewpage`, the Hebrew heading, the color names, the TikZ style keys (from art-se), `statcard`, `pullquote`, **`pythonbox`** (the code box: an ivory background with a hairline, JetBrains Mono, LTR, line numbers, reading the real script file so the code shown is the code that ran) |
| Page geometry | A4, left/right margins 3.0 cm → **text width 15.0 cm** (`TEXTWIDTH_IN = 5.906`). Top 3.6 cm, bottom 3.0 cm. Rubik 11/15.5 pt, paragraph skip 0.6 em, no indent. About 430–480 words per page, so 27 pages need about 7–8k words. **Never shrink the margins to reach the page count** |
| Build | From the root only: `lualatex --disable-installer main` → `biber main` → `lualatex …` ×2. The README lists the MiKTeX packages and their versions (RT-F2) |

## 5. Design system
### 5.1 Color and contrast (RT-A1, RT-A3, RT-F5, RT-Q5)
| Token | Hex | Contrast on white | Allowed use |
|---|---|---|---|
| ink | `#111111` | 18.9:1 | All small text, rules, axes, ClosetTwin's own series |
| mocha | `#A47864` | 3.85:1 | **Only large type (≥ 18 pt)**: chapter numbers, the stat-card number, rules, fills, the market/baseline series. *Never small text* |
| powder pink | `#E8C6C0` | 1.4:1 | Fills and bars only (the pull-quote bar, highlight bands, series 3 with an ink hairline). **It never carries text** |
| ivory | `#F7F3EE` | 1.1:1 | **The cover background** and the fills **inside boxes** (stat card, pull quote, code box, table header), always with a 0.4 pt mocha-pale hairline inside the body. Never the page (UD-2) |
| mocha-deep | `#6B4B3D` | 7.8:1 | **Approved (UD-1)**: caption labels, links, the banner chapter name, series 4 |
| mocha-pale | `#D3BBAE` | – | **Approved (UD-1)**: hairlines and a step in the sequential ramp |
| grid / muted | `#E3DCD4` / `#6F6862` | – / 4.96:1 | Figure gridlines and tick labels only |

- **Contrast rule:** text ≥ 4.5:1, large text and graphics ≥ 3:1 (qa D18).
- **Page color: white** (UD-2). The cover is ivory. Figures are transparent.
- hyperref's default colors and boxes are forbidden.

### 5.2 Type
| Element | Font | Notes |
|---|---|---|
| Chapter titles | Playfair Display Bold with lining numerals | Opener: a large mocha number (≥ 18 pt), a thin rule and generous space |
| Section and subsection titles | Playfair Display | Two levels only |
| Body | Rubik 11/15.5 pt | Bold = Rubik Medium/Bold. No Hebrew italic |
| Captions | Rubik, small | Label in mocha-deep (or ink bold), text in ink |
| Hebrew (all) | Rubik | The Hebrew page is set ragged (no Hebrew hyphenation) |
| Figure text | Rubik 8 pt at exactly 1:1 | Python figures have a fixed canvas = text width, so they are never scaled (RT-A8) |
| Math | **Latin Modern Math for everything inside a formula (letters, digits, symbols), formulas only (UD-3; uniform look, changed in CLS v0.7)**; `\text{}` words inside math stay Rubik. Greek is kept rare | |
| Code | **JetBrains Mono**, small, in `pythonbox` only (UD-4) | Never in the body text, URLs or figures |

### 5.3 Layout and editorial devices (RT-A2, RT-F6)
- **Banner** (every page except the cover): inset to the text block, *not* full-bleed (office printers clip the edge).
  It has the Playfair **ClosetTwin** wordmark in ink, a short powder-pink accent bar for the touch of color, the chapter name in
  small caps (mocha-deep or ink), and a 0.5 pt ink rule underneath. There is no filled band. On the Hebrew page the banner
  keeps the same LTR layout with the Latin wordmark, and its chapter-name slot shows the Hebrew title in Rubik.
- **Footer:** a hairline and the page number only. The "N of M" format was dropped, because roman and arabic numbering make it ambiguous.
- **Devices, all defined in the CLS:**
  - a **stat card** (one big mocha number, a one-line claim, its source)
  - a **pull quote** (powder-pink bar)
  - booktabs **tables** (ivory header with a hairline, numbers right-aligned)
  - the **assumption tags**
- **Airy rule:** at most 1 figure *and* 1 table per page. **No content page is more than half figure**, and every counted page
  carries running text (RT-W7, qa I13). Front matter is numbered in roman, and the content starts at arabic 1.

### 5.4 Figures: 7, not 9 (RT-A4…A8, RT-W5)
Python figures `import ct_style`:
- a fixed canvas of the text width, `pdf.fonttype = 42`, and fonts added by path with **no fallback** (qa I8, RT-Q4)
- a `pdffonts` check on every figure PDF
- ink → mocha → pink → mocha-deep order, at most 4 series, direct labels
- one y-axis only, and grayscale-safe

| # | Figure | Ch. | Tool | Rule from the review |
|---|---|---|---|---|
| F1 | TAM / SAM / SOM as **nested shapes, explicitly not to scale**, with one reference year printed in each label | 2 | Python or TikZ | RT-A6: there are no bars, because SOM would be an invisible sliver |
| F2 | Positioning map. **Axes defined from verified vendor-table columns**: x = questionnaire/size chart ↔ body scan; y = consumer app ↔ B2B plug-in. The caption says "positions are our reading of vendor pages" | 3 | Python | RT-A7, RT-W5, qa I14 |
| F3 | Scan → body model **+ garment specs + fit preference** → size → retailer data flow | 4 | TikZ | RT-W4 (peng2023) |
| F4 | Roadmap: a 6-row Gantt strip | 7 | TikZ | RT-A4 |
| F5 | 5-year projection as **one figure with two small-multiple panels**: (a) annual revenue vs. cost, with the **first profitable year (Y5)** marked; (b) the cumulative result, with the **peak deficit** marked (value from the Israel model, IL-M1) and the end of Y5 labeled "cumulative payback beyond the plan horizon". No extrapolation past Y5 | 8 | Python | RT-A4, MC-1 |
| F6 | **Retailer economics vs. the return-reduction effect ρ** (0–40%): the retailer's net saving per order at the Growth and Enterprise prices, with the **retailer break-even ρ = 6.03% / 4.52%** marked and the assumed base case (15%) shown. This shows that a null pilot (patel2025) costs the retailer only the pilot fee | 8 | Python | RT-W3, MC-2 |
| F7 | Risk heat matrix (likelihood × impact, each score labeled as assumed) | 9 | TikZ | |

- **Chapter 1** uses **stat cards** instead of a chart (RT-A5). A chart is allowed only if writer-se finds 4 or more sourced, comparable values.
- **Chapter 6** uses a table for the funnel and the pilot design. There is no funnel figure.

## 6. Document structure and page budget
**Front matter (not counted):** the **cover** (ivory; names, group code, course, lecturer, date, **no IDs**), the **Hebrew executive summary
(exactly 1 page)**, the TOC, and the lists of figures and tables.
**Back matter (not counted):** the references, then **Appendix A: "How our charts are made"**, which holds one `pythonbox` with
the script for one chart (art-se picks a short, readable one, probably F6) plus one paragraph on reproducibility (UD-4).

| # | Chapter | Pages | Must contain | Sources (all 29 bib keys assigned; RT-W8) |
|---|---|---|---|---|
| 1 | Introduction & Problem | 3 | Stat cards. The cost of returns as a **range** ($685 B [appriss2024] – $890 B [nrf2024]) with the method difference noted. The problem framed exactly as in §1 | appriss2024, coresight2023, nrf2024, gustafsson2021, pfaff2025 |
| 2 | Market: TAM / SAM / SOM | 4 | **Israel first (beachhead), with Europe as the expansion layer (UD-6).** F1. A **bottom-up SAM for Israel** with each input tagged sourced, derived or assumed (online apparel sales × share of retailers above a size threshold × our price) (RT-W2). The publisher's definition and method stated as a limit. SOM tagged *assumed* | imarc2026, kings2026, coresight2023, appriss2024, **+ Israeli e-commerce sources (IL-R1, pending)** |
| 3 | Competition | 3 | Note that MySize is Israeli-founded (if its page says so). A table titled **"Vendor claims"** in two parts: *direct* (True Fit, Fit Analytics, 3DLOOK, Bold Metrics, MySize) and *platform/in-house threats* (Google, Walmart/Zeekit). Blank cells read "not stated". F2. A moat section where every advantage is tagged **proven, plausible or hypothesis** (RT-W5) | truefit_web, fitanalytics_web, threedlook_web, boldmetrics_web, mysize_web, google2023tryon, walmart2021zeekit |
| 4 | Product & Technology | 4 | F3. The pipeline with garment and preference inputs. **Accuracy limits** (alhassawi2025: 89.66% SVM accuracy, failure at edge sizes). Platform integration. Privacy-by-design | alemany2013, peng2023, alhassawi2025, sembium2017, abdulla2019, chen2024, islam2024, ghodhbani2022, song2023 (labeled a preprint), zhang2024, shopify_dev_build |
| 5 | Business Model & Pricing | 3 | **Value-based pricing**: the price is a share of the return cost avoided, using Gustafsson's break-even rule. A tier table (assumed). The statement that enterprise vendors publish no pricing, so our numbers are **not benchmarked**. 3DLOOK and Popsize appear only as non-comparable reference points (RT-W6) | gustafsson2021, threedlook_pricing, popsize_shopify |
| 6 | Go-to-Market | 2 | **Israeli fashion e-tailers first** (named only from verified sources), with the channels the Israeli platform mix supports (Shopify only if a source shows its share). **Europe as the expansion stage**, entered through Israeli retailers that sell to the EU. A funnel table. **The pilot design: metric = fit-related return rate, a control group, a minimum sample and a pass/fail threshold** (RT-W3) | shopify_dev_build, patel2025 |
| 7 | Operations, Team & Roadmap | 2 | **Roles only, no names (UD-5)** and F4 (it includes an Amendment 13 compliance milestone before pilot data collection). Every cost and date tagged assumed | – (assumed) |
| 8 | Financial Plan | 3 | **Formula (1): the break-even tool cost per order = the avoided returns × the cost per return**. The formula is **our own**, written "following the logic of [gustafsson2021, §6]". Gustafsson prints no equation, only a step-by-step calculation: €1.1, €1.6 and €2.1 per pair at 40%, 60% and 80% fit verification. It is numbered, with every symbol defined. F5, F6. An **assumptions table: value / class (sourced, derived, assumed) / source**. LTV/CAC is optional and comes only after the break-even (RT-W6) | gustafsson2021, patel2025 (CLV +7.51% as a second lever) |
| 9 | Risks | 2 | F7. A mitigation for each risk: **Israel's Privacy Protection Law, Amendment 13 (biometric data = special sensitivity) as the primary legal risk**; **GDPR Art. 9 as a secondary risk** (Israeli sites selling to EU customers; the expansion stage); a null pilot effect (patel2025), accuracy at edge sizes (alhassawi2025), platform risk (google2023tryon), **scan unit cost**: in-house scanning at about $0.03 per scan (assumed) is a precondition, because at 3DLOOK's list price of about $2 per scan the margin fails [threedlook_pricing] (OL-2) | **ppl_amend13 (pending, IL-R1)**, gdpr2016, patel2025, alhassawi2025, google2023tryon |
| 10 | Conclusion | 1 | The ask, **derived from the Israel model (IL-M1; the $1.75M figure of v1.5 is superseded until it is recomputed)**, tagged as an assumption, and the next steps (Israeli pilots first) | – |
| | **Content total** | **27** | **R-01 prevails:** content ≥ 25 pages is a hard requirement | |
| | References (IEEE) | ≤ 2 | Every entry cited, none unused. Set in a smaller size | |

**Abstract-only sources** (sembium2017, abdulla2019, chen2024, islam2024, pfaff2025, song2023): any claim from them uses
only the abstract's wording (RT-W4). Vendor-page facts are written as "reported by <vendor>" (RT-Q7).

## 7. Requirements
Each requirement maps to criteria in `qa/acceptance-criteria.md` **v1.3** (being updated for v2.0).

| ID | Requirement | Target | How verified (qa IDs) |
|---|---|---|---|
| R-01 | Content length | ≥ 25 pages, ch. 1–10, references excluded. **Prevails over R-02** | Page count from `main.toc` (D1) |
| R-02 | Page budget | Each chapter within ±1 page of §6, the conclusion exactly 1, *and* R-01 still true | `main.toc` (D17) |
| R-03 | Hebrew executive summary | Exactly 1 front-matter page, RTL. The test corpus has ≥ 6 Latin runs, ≥ 5 numbers with units, 1 parenthesis and 1 sentence ending in a Latin run. A machine check: `pdftotext -bbox` contains "ClosetTwin" and "2026" and **not** "niwTtesolC" or "6202". A visual check of the rendered PNG (RT-Q3) | B1–B11 |
| R-04 | Structure | Chapters, a TOC, lists of figures and tables, an IEEE bibliography. The TOC, each chapter and the references start on a new page | L1, L6 |
| R-05 | Template | One custom `closettwin.cls` (book-based). No local formatting in the chapters | T1–T6 |
| R-06 | Fonts | `pdffonts` shows only Playfair Display + Rubik + Latin Modern Math + **JetBrains Mono**. LM Math appears only on pages with formulas, and JetBrains Mono only on the code-box page(s). Figure PDFs contain only Playfair and Rubik | D4, D11, K3, I8 |
| R-07 | Font licensing | The Playfair Display and JetBrains Mono files are byte-identical to the official releases (SHA-256 in `fonts/SOURCES.md`). OFL texts are present | FS5 + the qa-infra hash check |
| R-08 | Palette and contrast | Only the §5.1 tokens. Text ≥ 4.5:1, large/graphics ≥ 3:1. No default hyperref colors | D6, D7, D18, I7 |
| R-09 | Banner + footer | §5.3, on every page except the cover, including chapter-first pages and the Hebrew page | L7, D8 |
| R-10 | Figures | The 7 figures of §5.4 (minimum: 1 Python + 1 TikZ). No internet images. Each has a caption, a number and a mention in the text, sits at 1:1 within the text width, and is grayscale-safe | I1–I14, D12 |
| R-11 | Tables | ≥ 1 (target 5: vendor claims, pricing tiers, the funnel/pilot, assumptions, risk mitigations). Caption above, numbers right-aligned, within the text width | TB1–TB7 |
| R-12 | Formula | Formula (1) in ch. 8: numbered, introduced in the text, every symbol defined | D9, D10 |
| R-13 | Sources | Every `\cite` key exists. **No unused bib entry**. IEEE. `urldate` on every `@online`. A **claim-trace table** (quote + page for every statistic) | R1–R11 |
| R-14 | Number labeling | Every money, %, × or year-count number in **ch. 2, 5, 6, 7, 8, 9 and in captions** is `\cite`d in its sentence, or tagged `\derived` or `\assumed`, or sits under a caption that starts "Assumption:" | D14, TB6 |
| R-15 | Build | Four passes; 0 errors; 0 undefined references or citations; no overfull box > 1 pt; **0 missing glyphs (an error by `\tracinglostchars=3`)** | BU1–BU10, B9 |
| R-16 | Reproducibility | A fresh clone gives the **same page count, the same `pdftotext` per page, the same `pdffonts` list and the same warning counts**. Byte identity is not required (RT-F2, RT-Q8). Fonts are in the repo. Graphs regenerate with `python`. The README has the package list with versions | FS6, S9 |
| R-17 | Repository | `main.tex`, chapters, the `.cls`, `references.bib`, `fonts/`, PRD/PLAN/TODO/README, the **final PDF** and the skill files | FS1–FS8, S1, S4 |
| R-18 | QA skills | `qa-super`, `qa-BiDi`, `qa-table`, `qa-code`, `qa-img`, `qa-typeset`, `qa-infra`, `qa-cls-version` are in `.claude/skills/`, used, and listed in the README | S2, S3 |
| R-19 | Iron rule | Every recurring problem is fixed in the CLS or a skill, with a version bump and a CHANGELOG row | T6, S6 |
| R-20 | Pagination | No heading at the bottom of a page, no split figure, table or box, no nearly empty page, and the airy rule of §5.3 | L2–L5, I13 |
| R-21 | Editorial look | Margins 3.0 cm; at most 1 figure + 1 table per page; at most 4 series per figure; the §5.3 devices used consistently | D16 |
| R-22 | Cover | Page 1, ivory: title, subtitle, **Hila Abay, Shirel Giladi**, group code **sg00ha11**, **Generative AI for Management (875523402)**, **Dr. Yoram Segal**, date. No footer, no number. **No ID number anywhere in the repo or the PDF** (a grep for 9-digit numbers outside the course code) | C1–C5 |
| R-23 | Prompts | The agent prompts carry all the requirements (assignment §4 step 6). Saved in `prompts/` | S5 |
| R-24 | One file per chapter | `chapters/NN-*.tex`, each `\input` by `main.tex` | FS2 |
| R-25 | Code box | Appendix A has exactly one `pythonbox` showing a **real script from `python/`**, read from its file (not pasted). It is LTR, with an ivory background and a hairline, JetBrains Mono, line numbers, and no line past the margin. Running the script reproduces the chart it claims to produce | K1–K4 (qa-code) |
| R-26 | Legal framing | Amendment 13 is the primary framework and GDPR Art. 9 is secondary. Both are cited from **official** texts. "Fit, not identification" + privacy-by-design is argued as an advantage. The plan makes no legal claim without a source | R5, D15 |
| R-27 | Market framing | Every Israeli market number is sourced (an official or reputable Israeli source) or tagged derived or assumed. Europe appears as the expansion stage, not counted in the Y1–Y3 base case | D14, R8 |

## 8. Definition of Done (RT-Q2)
The report is done only when **all** of the following hold:
1. A build from a **fresh clone** with the four commands ends with 0 errors, 0 undefined items, 0 missing glyphs and no overfull
   box above 1 pt (R-15, R-16).
2. The final qa report (`qa/reports/NN-final.md`), produced by `qa-super` on that fresh-clone build, has **0 open blocker or major
   findings**. Every earlier finding is marked "rechecked in build `<git hash>`". Any minor finding still open is listed in the README.
3. The book's §19.5 checklist passes all six points.
4. **Sign-off lines** in `qa/reports/NN-final.md`: the user's name, the date, and the list of pages the user looked at, including the Hebrew page.
5. Every recurring fix has a `fix/CHANGELOG.md` row that matches the CLS or skill version.
6. `main.pdf`, all sources, the docs and the skills are committed and pushed, and `TODO.md` has no open item.

## 9. Open questions
All six (Q-A…Q-F) were **answered by the user on 2026-11-18**. See §3 and the review log rows UD-1…UD-7.
Team tasks: **IL-R1** (Israeli sources, 10 verified, bib 39 entries) and **IL-O1** (outline) are done. **IL-M1** (the Israel model) was done by master-se on 2026-11-19 under the exception in `PLAN.md` (art-se offline): `model.py` reproduces the outline §10.5 hand numbers, and the funnel check is green. Still open: fix-se's `pythonbox` env (T20.4/T20.5).

## 10. Review log: red team RT1 on v1.0
Four reviewers, 32 findings. **29 adopted, 2 adopted in part, 1 rejected in part.**

| ID | Reviewer | Finding (short) | Decision | Reason / where applied |
|---|---|---|---|---|
| RT-W1 | writer-se | The 53%, 24% and 80% figures misstate their sources | **Adopted** | §1 rewritten word for word to the sources. 80% is never a stat-card promise |
| RT-W2 | writer-se | TAM/SAM from one publisher, no bottom-up SAM | **Adopted (partly)** | Bottom-up SAM + method limit added in §6 ch. 2. The "range across publishers" applies only if writer-se verifies other publishers; unverified figures are not cited |
| RT-W3 | writer-se | "Fewer returns" stated as fact against Patel 2025 | **Adopted** | §1 hypothesis framing; pilot design in ch. 6; sensitivity F6 in ch. 8 |
| RT-W4 | writer-se | alhassawi2025 unused; preference input missing; abstract-only limits | **Adopted** | §6 ch. 4 and ch. 9; F3 inputs; the abstract-only rule under §6 |
| RT-W5 | writer-se | Vendor table mixes types; moat unsourced; 2×2 weak | **Adopted** | Two-part "Vendor claims" table, "not stated" cells, moat tags; F2 axes from facts |
| RT-W6 | writer-se | Benchmarks not comparable; LTV/CAC circular | **Adopted** | Value-based pricing + Gustafsson formula (1); LTV/CAC optional |
| RT-W7 | writer-se | ±1 tolerance contradicts ≥25; density too high | **Adopted** | R-01 prevails; the airy rule; 7 figures |
| RT-W8 | writer-se | 5 orphan bib entries; assumption scope too narrow; no "derived" class; reference length | **Adopted** | All 29 keys assigned in §6; R-13 "no unused entry"; R-14 widened; 3 classes; smaller bibliography size |
| RT-A1 | art-se | Ivory on white is invisible | **Adopted** | Hairline edge on every ivory surface; white page recommended (Q-B) |
| RT-A2 | art-se | Full-bleed banner clips in print; Hebrew page banner undefined | **Adopted** | §5.3 inset banner, no fill; Hebrew page defined |
| RT-A3 | art-se | Mocha small text below 4.5:1; pink text unreadable | **Adopted** | §5.1 use rules; mocha-deep via Q-A |
| RT-A4 | art-se | 9 figures too many; ch. 8 duplicate charts | **Adopted** | 7 figures; the funnel becomes a table; F5 small multiples |
| RT-A5 | art-se | Ch. 1 bar chart of unrelated %s | **Adopted** | Stat cards; a chart only with ≥ 4 comparable sourced values |
| RT-A6 | art-se | SOM invisible on a linear scale; mixed years | **Adopted** | F1 nested, not to scale, one year per label |
| RT-A7 | art-se | Subjective 2×2 axes | **Adopted** | F2 axes from verified columns |
| RT-A8 | art-se | `bbox tight` → figures scaled unevenly | **Adopted** | Fixed canvas = text width (15.0 cm) |
| RT-Q1 | qa-se | R-01 vs R-02; what counts as content | **Adopted** | R-01/R-02 rewritten; content = ch. 1–10 |
| RT-Q2 | qa-se | DoD not provable; no record of the human check | **Adopted** | §8 items 2 and 4 |
| RT-Q3 | qa-se | No BiDi test corpus or pass rule | **Adopted** | R-03 corpus + bbox machine check |
| RT-Q4 | qa-se | matplotlib font fallback, Type 3 | **Adopted** | §5.4; R-06 covers every figure PDF |
| RT-Q5 | qa-se | No contrast or clutter test | **Adopted** | §5.1 contrast column; R-08; R-21 measurable |
| RT-Q6 | qa-se | R-14 scope and pass rule | **Adopted** | R-14 rewritten |
| RT-Q7 | qa-se | "Verified" undefined; numbers not traced | **Adopted** | Claim-trace table in R-13; `urldate`; "reported by" |
| RT-Q8 | qa-se | Byte-identical PDF impossible; missing rows (cover, prompts, files) | **Adopted** | R-16 reworded; R-22–R-24 added; topic note in the header |
| RT-F1 | fix-se | article class lacks chapters and front matter | **Adopted** | `book` (oneside) in §4 |
| RT-F2 | fix-se | Reproducibility: dates, IDs, package drift | **Adopted** | R-16; package versions in the README; `\RequirePackage[date]` |
| RT-F3 | fix-se | A formula is impossible with Rubik alone | **Adopted** | Q-C recommended yes; R-06 whitelist |
| RT-F4 | fix-se | Missing glyphs are only warnings; figure fallback | **Adopted** | `\tracinglostchars=3`; R-15; figure `pdffonts` |
| RT-F5 | fix-se | Mocha contrast (same as RT-A3) | **Adopted** | Merged with RT-A3 |
| RT-F6 | fix-se | Ivory banner invisible; "N of M" ambiguous; TikZ overlay needs extra passes | **Adopted (partly)** | Shipout hook and page-number-only footer adopted. The **mocha filled band is rejected** in favor of RT-A2's inset rule-and-wordmark banner, which is airier and print-safe and still gets color from the pink accent bar |
| RT-F7 | fix-se | Float drift; exact 1-page conclusion | **Adopted except one point** | `\FloatBarrier`, `\raggedbottom` adopted. **Rejected:** "accept ±1 for the conclusion". "Conclusion 1" is the user's fixed decision, so writer-se fits the content to one page; the layout is not bent to fit |
| RT-F8 | fix-se | Font provenance and integrity | **Adopted** | `fonts/SOURCES.md` exists; hash check in R-07 |

### v1.2: corrections from the claim-trace table (`writer/claim-trace.md`, T5.0)
| ID | Finding | Decision | Applied |
|---|---|---|---|
| CT-1 | Formula (1) is ours. Gustafsson has no equation, only a step-by-step calculation (€1.1/€1.6/€2.1 per pair) | **Adopted** | §6 ch. 8 now says "following the logic of" |
| CT-2 | Appriss online returns are $362 B (BORO $146.8 B + BORIS $215.3 B), not "$215 B online" | **Adopted** | Not repeated in the PRD; fixed in the sources notes |
| CT-3 | Coresight 24.4% (apparel) and Appriss 24.52% (all online) must never be merged | **Adopted** | §1 already keeps them separate; qa checks this in R10 |
| CT-4 | Use peng2023's "20–40% return rate" and NRF's $890 B only as "reported by", because one is an uncited abstract sentence and the other comes from the landing page only | **Adopted** | The rule on vendor facts under §6 extends to these |
| CT-5 | Don't use 3DLOOK's "96–97% accuracy" as evidence (a health/fitness claim with no method) | **Adopted** | Ch. 4 uses alhassawi2025 for accuracy |
| CT-6 | RT-W2's "range across publishers" can't be supported, because the other publishers' pages were never opened | **Adopted: no range** | Ch. 2 states IMARC alone, with its definition and method as a stated limit |

### v1.3: decisions from the outline (`writer/outline.md`, T5.1)
| ID | Point raised by writer-se | Decision | Applied |
|---|---|---|---|
| OL-1 | Floats and openers take about 40% of the 27 pages, so chapters 6, 8 and 9 have little text and the page count is at risk | **Adopted**: one chapter (ch. 1) is built first as a **calibration build** to measure words per page. The 800-word reserve sections are approved for use if the content falls under 26.5 pages. Margins are never shrunk | PLAN S7 starts with a calibration build of ch. 1 |
| OL-2 | Scan unit cost is a fifth risk | **Adopted** | §6 ch. 9; F7 now has 5 risks |
| OL-3 | Use one price everywhere | **Adopted**: TAM and SAM use the **blended price, $0.036 per order (assumed)**, the same value as in ch. 5 and 8 | `assumptions.csv` is the single source |
| OL-4 | The funding ask comes from the model | **Adopted**: about $1.8M, derived and tagged | §6 ch. 10 |
| OL-5 | 53% is not the fit share of returns | **Adopted**: the fit-related share of returns is **assumed at 40%**, deliberately below the survey's 53%, and it is a sensitivity variable | `assumptions.csv`; ch. 8 sensitivity |
| OL-6 | Our fee-pool TAM (about $0.33B) is far below IMARC's $8.5B | **Adopted**: ch. 2 explains the definition difference and uses IMARC as context only | §6 ch. 2 |
| OL-7 | Pilot fallback when the client can't randomize | **Adopted**: ch. 6 names a before-and-after design as the fallback, explicitly labeled **weaker evidence** | §6 ch. 6 |

### v1.4: decisions from the model check (`python/model.py`, T5.2)
The model reproduces writer-se's hand numbers within 1%, except for the ask.
| ID | Point raised by art-se | Decision | Applied |
|---|---|---|---|
| MC-0 | The ask is $1,775,400 (1.2 × $1,479,500), so "$1.8M" is 1.4% off | **Adopted**: write "about $1.78M" | §6 ch. 10 |
| MC-1 | Cumulative break-even falls outside the 5 years. Y5 is the first profitable year (+$0.9M), but the cumulative result is still −$0.58M at the end of Y5 | **Adopted**: F5 marks the first profitable year and the peak deficit. **No chapter may say "break-even within five years"**. The text says "operating profit in year 5; cumulative payback beyond the plan horizon". No extrapolation | F5; qa adds a grep for "break-even within" |
| MC-2 | F6 was undefined, because our revenue doesn't depend on ρ | **Adopted**: F6 shows the **retailer's** economics against ρ, with the retailer break-even at 6.03% / 4.52%. This is the value proposition and the answer to the Patel risk | F5/F6 rows above |
| MC-3 | The pilot-to-paid funnel (A15–A17) isn't tied to the number of paying clients per year (A26) | **Adopted**: `model.py` adds a **consistency check** (paying clients per year ≤ what the funnel implies) and fails loudly if it is broken. Ch. 6 shows funnel numbers consistent with A26 | `model.py` |

### v1.5: a coherent sales funnel (MC-3 check failed → writer-se option (b) → art-se recompute)
| ID | Finding | Decision | Applied |
|---|---|---|---|
| MC-4 | The funnel check failed: year 2 needed 8 paying clients, but year 1 had only 2 pilots (at most 1 client at 50% pilot→paid) | **Adopted option (b)**: 16 Y1 pilots (4 direct at $5,000 each, 12 low-touch Shopify App Store pilots at $0), then 36 / 75 / 132 / 132. Each pilot has an explicit cash cost ($3,000 direct, $500 low-touch). There is a contact-capacity check and a pilot-effort check. *Rejected:* relabeling the client numbers as an aspiration | `assumptions.csv` (A26p, A26q, A31–A37); `model.py` funnel check green (3 parts) |
| MC-5 | New results: revenue Y1–Y5 $20k / $333k / $994k / $2.33M / $4.49M; operating result −$358k … +$916.5k; cumulative at Y5 −$0.54M; **peak deficit −$1,457,125; ask $1,748,550 ("about $1.75M")**; SOM ≈ 6.0% of SAM | **Adopted** | F5 labels; ch. 8, ch. 10 |
| MC-6 | writer-se's caveats: (1) Y1 timing depends on the MVP in H1, so pilots run Q3–Q4 with design partners; (2) the low-touch pilots are pooled evidence, 4 weeks only at 1M orders/yr; (3) A11 = 1M orders is a blended average; (4) A17 = 50% is the weakest link | **Adopted as text requirements** | Ch. 5, 6, 7, 8, 9 |

### v2.0: the user's answers (Q-A…Q-F), 2026-11-18
| ID | User decision | Effect | Applied / owner |
|---|---|---|---|
| UD-1 | Q-A: the tints mocha-deep and mocha-pale are approved | Small colored text uses mocha-deep. Contrast passes | §5.1; fix-se (CLS colors), art-se (`ct_style`) |
| UD-2 | Q-B: a white page; ivory only on the cover and inside boxes | The cover background is ivory | §5.1; fix-se |
| UD-3 | Q-C: Latin Modern Math inside formulas only | R-06 whitelist | §5.2, R-06; qa D11 |
| UD-4 | Q-D: one code box (Appendix A) in JetBrains Mono, code only | A new `pythonbox` env, a new font, R-25. This reverses the PRD's earlier "no monospace" (K3) | fix-se (font + env), art-se (choose and clean the script), qa-se (K1–K4) |
| UD-5 | Q-E: the cover details; **no ID numbers**; the team chapter lists roles only | R-22 + an ID grep | master-se (`main.tex` cover fields), writer-se (ch. 7) |
| UD-6 | Q-F: **Israel is the beachhead and Europe the expansion** | Market, GTM, model and outline change: Israeli market size, retailer sizes, platform mix, prices and currency | writer-se (IL-R1 sources, IL-O1 outline), art-se (IL-M1 model) |
| UD-7 | Q-F: the primary legal framework is Israel's Privacy Protection Law, Amendment 13. GDPR Art. 9 is secondary. BIPA is dropped. Privacy is argued as an advantage | New bib entries from official sources, R-26 | writer-se (IL-R1) |
| UD-8 | *master-se decision:* the reporting currency stays **USD** (investor convention; most sources are in USD). Israeli figures in ILS are converted at **one assumed rate** (a row in `assumptions.csv`), and `\ils{}` is used where an ILS amount is quoted | Consistency | art-se (row), writer-se |
| UD-9 | *master-se, 2026-11-19, after the usage-limit interruption:* IL-M1 closed. `python/model.py` now models Israel (beachhead) and Europe (entry year 4) separately; the funnel check covers both markets, the Israeli pool caps and one shared sales team. Result: revenue $10 k → $782 k, **no operating profit inside five years**, cumulative deficit $2.33 M, **ask about $2.8 M** (supersedes $1.75 M). Year-average client counts are whole numbers, so the reach check allows 0.5 client of rounding (year 3: 2.2 needed vs 2.0) | F5 must not mark a profitable year; ch. 8 and 10 use the new numbers | writer-se (ch. 8, 10), art-se (F5, F6 on return) |
