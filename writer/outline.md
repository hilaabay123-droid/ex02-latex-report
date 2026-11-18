# ClosetTwin business plan: outline with page and word budget (T5.1)

writer-se, 2026-11-18, for PRD v1.2 §6. No chapter text yet and no LaTeX.
Row IDs (C01, M02, V10, L01 …) refer to `writer/claim-trace.md`. Bib keys refer to `references.bib` (29 entries).

**Labels used for every number in the chapters** (PRD R-14): *sourced* (cited in the sentence), *derived* (computed by us from sourced or assumed inputs, shown with its formula), *assumed* (our choice, with a one-line basis). Vendor-page facts are written "reported by <vendor>".
Section 10 holds the assumptions list that seeds `python/data/assumptions.csv`. It contains my hand calculations as a sanity check only. The model in `assumptions.csv` is authoritative.

## 0. Budget method

- 450 words per page of running text. Floats and chapter openers are subtracted: opener 0.3 page, stat-card row 0.4, figure 0.5–0.6, standard table 0.4–0.5, wide table 0.8, display formula 0.1.
- Word count is a target for the draft. After the first chapter compiles, I measure real words per page (Rubik 11 pt, margins ≥ 2.5 cm) and rescale the other chapters.

| # | Chapter | Pages | Floats and opener | Text pages | Target words |
|---|---|---|---|---|---|
| 1 | Introduction & Problem | 3 | 0.3 opener + 0.4 stat cards = 0.7 | 2.3 | 1,000 |
| 2 | Market: TAM / SAM / SOM | 4 | 0.3 + F1 0.5 + SAM-input table 0.5 = 1.3 | 2.7 | 1,200 |
| 3 | Competition | 3 | 0.3 + vendor table 0.8 + F2 0.5 = 1.6 | 1.4 | 650 |
| 4 | Product & Technology | 4 | 0.3 + F3 0.6 = 0.9 | 3.1 | 1,400 |
| 5 | Business Model & Pricing | 3 | 0.3 + tier table 0.4 = 0.7 | 2.3 | 1,030 |
| 6 | Go-to-Market | 2 | 0.3 + funnel table 0.4 + pilot table 0.5 = 1.2 | 0.8 | 360 |
| 7 | Operations, Team & Roadmap | 2 | 0.3 + F4 0.5 = 0.8 | 1.2 | 540 |
| 8 | Financial Plan | 3 | 0.3 + F5 0.6 + F6 0.5 + assumptions table 0.5 + formula 0.1 = 2.0 | 1.0 | 450 |
| 9 | Risks | 2 | 0.3 + F7 0.5 + mitigation table 0.5 = 1.3 | 0.7 | 315 |
| 10 | Conclusion | 1 | 0.3 | 0.7 | 315 |
| | **Total** | **27** | 10.8 pages of floats and openers (40%) | 16.2 | **7,260** |
| | Hebrew summary page (front matter, not counted) | – | – | – | about 230 Hebrew words |

**Three risks to the page count, for master-se**
1. 40% of the 27 pages are floats and openers. If figures are set smaller than I assumed, content drops below 25 pages. Reserve (about 800 words, written only if the first full build is under 26.5 pages): ch. 2 "SAM sensitivity to the retailer-share assumption" (+200), ch. 4 "Data requirements and onboarding" (+250), ch. 7 "Compliance checklist" (+150), ch. 3 "Reading the table: what vendors do not say" (+200).
2. Ch. 6, 8 and 9 have only 0.7–1.0 pages of text each. They carry their content in tables, formula and figures. I will not pad them. If qa-se wants more text there, the PRD page split should move one page from ch. 4 or ch. 2.
3. The opposite error is also possible: Rubik is a wide face. If it holds only about 400 words per page, the same words fill about 29 pages. The calibration build decides.

---

## Chapter 1. Introduction & Problem (3 pp, 1,000 words)

Stat cards (4 cards, one row): SC1 "$685 B – $890 B" returns in 2024 with the method difference; SC2 "24.4%" online apparel orders returned; SC3 "53%" of surveyed decision-makers name size/fit the top reason; SC4 "17%" cost of a return as a share of prime cost (footwear case).

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 1.1 | The returns bill | Returns are a cost line of the order of hundreds of billions of dollars, and the two best estimates differ because their methods differ. | appriss2024 C01–C03, C07; nrf2024 C08–C10 | 350 |
| 1.2 | Why fit is the core cause | Size and fit uncertainty is the most-cited reason for online apparel returns, and the literature treats it as a problem of information, not of product quality. | coresight2023 C13; peng2023 C25 ("reported by"); alemany2013 P08; abdulla2019 P10 *(AB)*; pfaff2025 P11 *(AB, analogy only)* | 300 |
| 1.3 | What one return costs | A return costs a retailer a measurable share of the product's prime cost, mostly handling and transport. | gustafsson2021 C15, C19; coresight2023 C11, C12, C14 (US, 2023) | 200 |
| 1.4 | The thesis and how this plan tests it | ClosetTwin's claim is a hypothesis, "a fit tool built on scan, garment data and preference lowers fit-related returns", that a pilot can accept or reject. | none (forward references to ch. 6, 8, 9) | 150 |

Notes: SC1 uses the range with one sentence of method (survey plus Census vs. industry projection). SC2 and SC3 are both Coresight (100 respondents) and say so on the card. Do not put "24%" next to Appriss's 24.52% on the same card (claim-trace caution 2).

## Chapter 2. Market: TAM / SAM / SOM (4 pp, 1,200 words)

F1: nested shapes, not to scale, one reference year per label. Table T1: SAM inputs with the class of each (sourced / derived / assumed).

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 2.1 | Method and its limits | We size the market bottom-up in orders and fees, and treat publisher figures only as context because their definitions are not public. | imarc2026 M01 | 250 |
| 2.2 | Context from market research | The virtual-fitting-room market is reported as growing fast, and the e-commerce apparel market is large. | imarc2026 M01 (alone, with its limit), kings2026 M02 | 250 |
| 2.3 | TAM: the global order-fee pool | At the blended fee per order (D08), the global pool is about $0.33 B a year. This is far below the headline market figures, because those count whole categories (hardware, stores) and we count only fees. | kings2026 M02; inputs A01, D08 (§10) | 250 |
| 2.4 | SAM: who we can serve | Excluding Asia-Pacific and retailers below a size threshold leaves about $75 M. | kings2026 M03; assumption A06 (§10) | 250 |
| 2.5 | SOM: what we can win | The financial plan implies about 6% of the SAM by year 5 (D20 ÷ D17). Tagged *assumed*. | link to ch. 8; no source | 200 |

Notes: IMARC alone, with the limit "definition and method not public" (master-se ruling; no publisher range). T1 columns: input | value | class | source or basis. Do not call $0.4 B our "market size" without the word "fee pool".

## Chapter 3. Competition (3 pp, 650 words)

Table T2 "Vendor claims", two parts (direct / platform and in-house threats), blank cells read "not stated". F2: positioning map, axes x = questionnaire or size chart ↔ body scan, y = consumer app ↔ B2B plug-in.

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 3.1 | How to read this table | Everything in it is what a vendor says about itself. | none | 80 |
| 3.2 | Direct vendors | The direct field splits on one question: does the shopper scan, give a few inputs, or neither? | truefit_web V01–V02; fitanalytics_web V03; threedlook_web V05; boldmetrics_web V04; mysize_web V06 | 220 |
| 3.3 | Platform and in-house threats | Google and Walmart already run free or captive try-on, so a retailer may not need a vendor for visualization. | google2023tryon V07–V08; walmart2021zeekit V09 | 130 |
| 3.4 | Positioning | ClosetTwin's chosen corner (scan plus garment specs plus preference, B2B plug-in) is occupied by no vendor on this table, which proves only that the vendors do not say they occupy it. | F2, T2 columns | 80 |
| 3.5 | The moat: proven, plausible or hypothesis | Each claimed advantage is tagged honestly. Expected tags: "combined scan + garment + preference input" *hypothesis*; "return reduction" *hypothesis until the pilot*; "no-scan alternative exists (Bold Metrics)" is a counter-argument we state. | V04, V05; peng2023 P04, P05 | 140 |

## Chapter 4. Product & Technology (4 pp, 1,400 words)

F3: scan → body model + garment specs + fit preference → size → retailer data flow (TikZ).

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 4.1 | What the shopper and the retailer see | The product is a widget on the retailer's product page and a data feed back to the retailer. | shopify_dev_build V14 | 200 |
| 4.2 | From scan to body model | A body model from scan data is feasible and well studied, and sizing schemes are poorly matched to real bodies. | alhassawi2025 P01; alemany2013 P07; threedlook_pricing V12 (VC, phone capture exists) | 300 |
| 4.3 | Why scan alone is not enough | Fit preference changes the size people choose, so the model needs garment specs and preference as inputs. | peng2023 P04–P06; sembium2017 P09 *(AB)*; abdulla2019 P10 *(AB)*; zhang2024 P14 *(AB)* | 300 |
| 4.4 | The size model and its accuracy limits | A supervised model reaches 89.66% accuracy on scan data, and fails at edge sizes. We state it as the best evidence in hand, not as ClosetTwin's measured performance. | alhassawi2025 P02, P03, P01 | 250 |
| 4.5 | Integration with retailer platforms | Integration is a standard app-plus-backend pattern on Shopify, with other platforms not yet checked. | shopify_dev_build V14 | 150 |
| 4.6 | Privacy by design | Body data is sensitive under GDPR Art. 9 if used to identify a person, so the design collects the minimum, with explicit consent. | gdpr2016 L01–L03 (forward to ch. 9) | 100 |
| 4.7 | Visualization: an extension, not the core | Try-on image generation exists and is surveyed, but this plan keeps it out of the first release. | islam2024 P13 *(AB)*; chen2024 P12 *(AB)*; song2023 P15 *(preprint, AB)*; ghodhbani2022 P16 *(metadata only; cite for "surveys exist" or drop)* | 100 |

Notes: only abstract wording from AB sources. Phone-scan accuracy has no independent source, so the chapter states it as an engineering target to be measured, not as a result.

## Chapter 5. Business Model & Pricing (3 pp, 1,030 words)

Table T3: pricing tiers (assumed).

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 5.1 | Who pays for what | The retailer pays per order served, because its benefit (avoided return cost) scales with orders. | none (assumed model) | 150 |
| 5.2 | Value-based price | A retailer breaks even if the tool costs less than the return cost it avoids: about $0.10 per order at the base case, so a $0.04 price takes 40% of the value. Formula (1) comes in ch. 8. | gustafsson2021 C15, C19, C20; coresight2023 C11; inputs A01–A05 | 300 |
| 5.3 | The tiers | Three tiers: a fixed-fee pilot, a Growth tier, an Enterprise tier. | T3 (all assumed) | 200 |
| 5.4 | Reference points, not benchmarks | The direct enterprise vendors publish no prices ("not stated" in T2), so our prices cannot be benchmarked. The only public prices are for a scan API (3DLOOK) and a small-merchant app (Popsize), and both are shown as non-comparable. | threedlook_pricing V10–V12; popsize_shopify V13 | 200 |
| 5.5 | Unit economics and the scan-cost condition | Gross margin is high only if a scan costs us about $0.03. At 3DLOOK's list price per scan (about $2.00, derived from V11) the scan alone would cost about 67 times our assumed $0.03 (D13) and the model fails. | V11; assumptions A12–A13 | 180 |

## Chapter 6. Go-to-Market (2 pp, 360 words)

Tables T4 (funnel) and T5 (pilot design). No funnel figure.

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 6.1 | Segments and channels | We start with mid-to-large fashion retailers, reaching small merchants through the Shopify App Store and larger ones through direct sales. | shopify_dev_build V14; popsize_shopify V13 (contrast) | 120 |
| 6.2 | The funnel | Per 100 qualified retailers contacted, about 4–5 become paying clients. All rates assumed. | T4; assumptions A15–A18 | 90 |
| 6.3 | The pilot design | A shopper-level randomized pilot can detect an effect at about the break-even size within one retailer's 4 weeks of traffic, and it has a stated pass line. | patel2025 C22–C24; T5; assumptions A19–A24 | 150 |

T5 rows: metric (fit-related return rate = orders with a size/fit return reason ÷ orders), design (shopper-level 50/50 randomization, intention to treat), sample (derived), duration (4 weeks of sales + 30-day return window), pass line (assumed), fail rule (stop and do not scale).

## Chapter 7. Operations, Team & Roadmap (2 pp, 540 words)

F4: Gantt strip, 6 rows, times as "Y1 Q1" style (no calendar dates). Everything here is tagged *assumed*.

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 7.1 | Operating model | The service is a capture widget, an inference backend and a data feed, run on rented cloud capacity. | none | 130 |
| 7.2 | Team and roles | A team of 4 growing to 28 over five years covers engineering, data science, partnerships and compliance. Roles only; names depend on the user's answer to Q-E. | none; assumption A25–A26 | 180 |
| 7.3 | Roadmap | Six workstreams, with the pilot gating everything after it: MVP, pilot, first paying clients, Shopify listing, GDPR/consent review, scale-out. | F4 | 150 |
| 7.4 | Dependencies | Two dependencies matter: the pilot result and a consent flow that holds up legally. | link to ch. 9 | 80 |

## Chapter 8. Financial Plan (3 pp, 450 words)

Formula (1), F5 (two panels: 5-year projection and break-even), F6 (sensitivity), Table T6 (assumptions: value / class / source).

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 8.1 | The break-even logic and formula (1) | The break-even tool cost per order is the fit-related return cost avoided per order, written "following the logic of [gustafsson2021, §6]" and defined symbol by symbol (§ 10 gives my symbols). | gustafsson2021 C20, C21; formula is ours | 150 |
| 8.2 | Five-year projection | Under the assumptions, the operating result is positive in year 5 (+$0.9 M) and the cumulative result is still −$0.58 M at the end of year 5. Write "operating profit in year 5; cumulative payback beyond the plan horizon", never "break-even within five years". The peak cumulative deficit is −$1.48 M (end of year 4). Source: `python/data/model_out.csv` (D23, D24, CUM_5). | F5; T6 | 120 |
| 8.3 | Sensitivity to the pilot result | F6 shows the retailer's economics against ρ: the retailer breaks even at ρ = 6.03% (Growth) and 4.52% (Enterprise) (D07a, D07b). At zero effect the client would pay for nothing, so the pilot gate must stop the rollout. This is also the answer to the Patel 2025 risk in ch. 9. | F6; patel2025 C22 | 100 |
| 8.4 | A second lever | In one study, size-finder use went with higher customer lifetime value, which we mention but do not put in the base case. | patel2025 C23–C24 | 40 |
| 8.5 | The assumptions table | Every number in this chapter appears in T6 with its class. | T6 | 40 |

## Chapter 9. Risks (2 pp, 315 words)

F7: heat matrix (likelihood × impact, scores labeled assumed). Table T7: risk | mitigation | owner or trigger.

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 9.1 | The register | Five risks are rated and each has a mitigation. | F7, T7 | 55 |
| 9.2 | Null pilot effect | A size tool can fail to cut returns: the largest study in our sources found size-finder users slightly *more* likely to return. The pilot gate is the mitigation. | patel2025 C22, C24 | 70 |
| 9.3 | Biometric data law | Under GDPR Art. 9, biometric data used for unique identification is prohibited without an exception such as explicit consent, so consent and data minimization are design requirements. | gdpr2016 L01–L03 | 70 |
| 9.4 | Accuracy at edge sizes | The size model fails for rare sizes, so rare-size shoppers get a fallback. | alhassawi2025 P03, P01 | 60 |
| 9.5 | Platform risk | Google offers free try-on, so a retailer may rely on the platform. | google2023tryon V07 | 60 |

**Proposed fifth risk (needs master-se's approval):** "scan unit cost above model", since ch. 5.5 shows the model fails at vendor scan prices. If rejected, ch. 5.5 carries it alone.

## Chapter 10. Conclusion (1 p, 315 words)

| § | Section | It must prove | Keys | Words |
|---|---|---|---|---|
| 10.1 | The case | The problem is large and fit-driven, and a fit tool is a hypothesis with a cheap test. | – | 100 |
| 10.2 | The ask | A seed of about $1.78 M (derived: peak cumulative deficit $1.48 M plus a 20% buffer, D24 and D25 in `model_out.csv`) funds the pilot and the first four years, until the operating result turns positive in year 5. | T6 | 120 |
| 10.3 | Next steps | The pilot comes first, and nothing else is funded until it passes. | – | 95 |

---

## 9. The Hebrew executive-summary page

About 230 Hebrew words, one page. Every claim has a row in the claim-trace. The page is a summary, so it repeats chapter text and adds nothing new.

| # | Claim in the Hebrew text | Source row | Latin run(s) | Number with unit |
|---|---|---|---|---|
| H1 | ClosetTwin is a B2B AI virtual fitting room for fashion e-commerce sites. | – | ClosetTwin, B2B, AI | – |
| H2 | Returns cost retailers between 685 and 890 billion dollars in 2024. | C01, C08 | Appriss, NRF | 685–890 B$ (מיליארד דולר) |
| H3 | In a survey, 24.4% of online apparel orders were returned. | C11 | Coresight | 24.4% |
| H4 | 53% of surveyed decision-makers name size/fit as the top reason. | C13 | – | 53% |
| H5 | A return costs about 17% of the prime cost (footwear case). | C15 | – | 17% |
| H6 | The virtual-fitting-room market is reported at 8.5 billion dollars in 2025. | M01 | IMARC | 8.5 B$ |
| H7 | The price is assumed at 0.04 dollars per order. | A-price | – | 0.04 $ per order |
| H8 | A shopper-level pilot of about 4 weeks tests the claim. | T5 | – | 4 weeks; about 6,000 orders per arm |
| H9 | The privacy rule is GDPR Art. 9 (explicit consent). | L01–L02 | GDPR | – |
| H10 | The first sales channel is Shopify (the App Store), then direct sales. | V14 | Shopify | – |
| H11 | The document is dated 2026 and the funding ask is about 1.78 million dollars. | T6 | – | 2026; 1.78 M$ |

R-03 corpus check: Latin runs = ClosetTwin, B2B, AI, Appriss, NRF, Coresight, IMARC, GDPR, Shopify (9, need ≥ 6). Numbers with units = 685–890 B$, 24.4%, 53%, 17%, 8.5 B$, 0.04 $, 4 weeks, 6,000 orders (8, need ≥ 5). Parenthesis: H9 and H10 (need 1). Sentence ending in a Latin run: H10 is written to end with "Shopify" (need 1). The page text contains "ClosetTwin" and "2026" for the machine check.
The Hebrew text is written only after master-se approves the English chapters, so that the numbers cannot drift.

---

## 10. Assumptions list (seed for `python/data/assumptions.csv`)

Columns for the CSV: `id, name, value, unit, class, basis, chapters`. Class: sourced (S), derived (D), assumed (A). My hand calculations after "=" are checks, to be recomputed by the model.

### 10.1 Sourced inputs

| id | name | value | basis (key, row) | chapters |
|---|---|---|---|---|
| S01 | Online apparel return rate | 24.4% | coresight2023 C11 (US survey of 100, 2023) | 1, 5, 8 |
| S02 | Cost of a return as a share of prime cost | 17% | gustafsson2021 C15 (footwear, one retailer) | 1, 5, 8 |
| S03 | Total returns 2024, low / high | $685 B / $890 B | appriss2024 C01 / nrf2024 C08 | 1 |
| S04 | Global e-commerce apparel market 2024 | $726.05 B | kings2026 M02 | 2 |
| S05 | Asia-Pacific share of that market | 42.70% | kings2026 M03 | 2 |
| S06 | Virtual-fitting-room market 2025 / 2034 / CAGR | $8.5 B / $52.6 B / 21.80% | imarc2026 M01 (context only, not in any calculation) | 2 |
| S07 | CLV uplift per unit of size-finder use | +7.51% (next quarter) | patel2025 C23 (second lever, not in the base case) | 8 |
| S08 | Reference scan price (Mobile Tailor Premium) | $999 / 500 scans ≈ $2.00 per scan (derived division) | threedlook_pricing V11 | 5 |

### 10.2 Assumed inputs

| id | name | value | one-line basis | chapters |
|---|---|---|---|---|
| A01 | Average order value (AOV) | $80 | Plausible mid-market apparel basket; replace if a sourced figure is found | 2, 5, 8 |
| A02 | Prime cost as share of AOV | 50% | Typical apparel mark-up logic; no source | 5, 8 |
| A03 | Fit-related share of returns | 40% | Below the 53% of respondents who name fit the top reason (a share of respondents is not a share of returns; claim-trace caution 3) | 5, 8 |
| A04 | Base-case relative reduction of fit-related returns, shop-wide (ρ) | 15% | Deliberately below Gustafsson's scenarios (40–80% verification) because Patel found no reduction; the pilot tests it | 5, 6, 8 |
| A05 | Sensitivity range for ρ | 0% to 40% | Covers a null result up to Gustafsson's lowest scenario | 8 |
| A06 | Retailers addressed as share of orders (SAM size filter) | 40% | Excludes marketplaces and small shops; no source | 2 |
| A07 | Price, Growth tier | $0.04 per order | 40% of the break-even value (derived below) | 5, 8 |
| A08 | Price, Enterprise tier | $0.03 per order | 30% of break-even; volume discount | 5, 8 |
| A09 | Price, Pilot | $5,000 fixed fee | Covers integration; no source | 5, 6 |
| A10 | Mix of paying clients | 60% Growth / 40% Enterprise | no source | 8 |
| A11 | Average orders per paying client per year | 1,000,000 | Mid-to-large online retailer | 8 |
| A12 | Cost per scan | $0.03 | Needs an engineering benchmark; the plan fails above about $0.1 | 5, 8, 9 |
| A13 | Share of orders that include a scan | 25% | Adoption guess; no source | 5, 8 |
| A14 | Fully loaded cost per FTE per year | $90,000 | Blended; replace if a sourced benchmark is found | 7, 8 |
| A15 | Contact → meeting | 30% | Funnel guess | 6 |
| A16 | Meeting → pilot | 30% | Funnel guess | 6 |
| A17 | Pilot → paying client | 50% | Funnel guess; depends on the pilot result | 6 |
| A18 | Sales cycle | 9 months | no source | 6, 7 |
| A19 | Pilot randomization | shopper level, 50/50 | Standard design | 6 |
| A20 | Significance and power | α = 0.05 (two-sided), power 80% | Textbook convention | 6 |
| A21 | Return window for follow-up | 30 days | Typical policy; no source | 6 |
| A22 | Pilot sales window | 4 weeks | no source | 6 |
| A23 | Pass line | observed relative reduction ≥ 10% and 95% interval above 0 | Margin above the break-even effect (4.52% to 6.03%, D07) | 6 |
| A24 | Planned orders per arm | 12,000 minimum (2× the derived minimum) | Margin for noise | 6 |
| A25 | Headcount, years 1–5 | 4, 8, 14, 20, 28 | no source | 7, 8 |
| A26 | Paying clients, years 1–5 (year average) | 0, 8, 25, 60, 120 (year 1: 2 pilots) | no source; year 1 has pilots only | 8 |
| A27 | Annual client churn (optional LTV) | 10% | no source | 8 |
| A28 | Customer acquisition cost (optional LTV/CAC) | $25,000 | no source | 8 |
| A29 | Risk scores (likelihood, impact), 1–5 | null effect (3,5); GDPR (3,4); edge sizes (3,3); platform (3,4); scan cost (2,4) | Judgement; labeled assumed on F7 | 9 |
| A30 | Funding buffer on the derived need | 20% | no source | 10 |

### 10.3 Derived values (my hand calculation; the model recomputes)

| id | name | formula | value |
|---|---|---|---|
| D01 | Prime cost per order | A02 × A01 | $40.00 |
| D02 | Cost per return | S02 × D01 | $6.80 |
| D03 | Fit-related returns per order | S01 × A03 | 0.0976 (9.76%) |
| D04 | Fit-related return cost per order | D03 × D02 | $0.664 |
| D05 | Break-even tool cost per order at base case, formula (1) | D04 × A04 | $0.0996 (≈ $0.10) |
| D06 | Price as a share of break-even | A07 / D05; A08 / D05 | 40%; 30% |
| D07 | Minimum effect for a retailer to break even | A07 / D04 | 6.0% (Growth), 4.5% (Enterprise) |
| D08 | Blended price | 0.6 × A07 + 0.4 × A08 | $0.036 per order |
| D09 | Client's annual saving at base case (1M orders) | D05 × A11 | about $99,600 |
| D10 | Client's annual fee (Growth, 1M orders) | A07 × A11 | $40,000 |
| D11 | Cost to serve per order | A12 × A13 | $0.0075 |
| D12 | Gross margin at the blended price | (D08 − D11) / D08 | about 79% |
| D13 | Scan-vendor price gap | S08 / A12 | about 67× (the plan needs in-house scan cost) |
| D14 | TAM, orders | S04 / A01 | 9.08 B orders |
| D15 | TAM, fee pool | D14 × D08 | about $0.33 B (at the blended price; $0.36 B at the Growth price) |
| D16 | SAM share by region | 1 − S05 | 57.30% |
| D17 | SAM, fee pool | D15 × D16 × A06 | about $75 M |
| D18 | Sample per arm for the base case | (z₁₋α/₂ + z₁₋β)² · [p₁(1−p₁) + p₂(1−p₂)] / Δ², with p₁ = D03, p₂ = D03 × (1 − A04), Δ = p₁ − p₂, and z₀.₉₇₅ + z₀.₈₀ = 1.96 + 0.84 | about 6,000 orders per arm |
| D19 | Minimum detectable relative effect in 4 weeks, at 1M orders/year | solve the same formula for Δ with n ≈ 38,000 per arm | about 6% |
| D20 | Revenue, years 1–5 | A26 × A11 × D08 (year 1: 2 × A09) | $10 k; $0.29 M; $0.90 M; $2.16 M; $4.32 M |
| D21 | Cost of goods, years 2–5 | A26 × A11 × D11 | $0.06 M; $0.19 M; $0.45 M; $0.90 M |
| D22 | Operating cost, years 1–5 | A25 × A14 | $0.36 M; $0.72 M; $1.26 M; $1.80 M; $2.52 M |
| D23 | Operating result, years 1–5 | D20 − D21 − D22 | −$0.35 M; −$0.49 M; −$0.55 M; −$0.09 M; +$0.90 M |
| D24 | Peak cumulative deficit | running sum of D23 | −$1.4795 M (end of year 4) |
| D25 | Funding ask | D24 × (1 + A30) | $1.7754 M, written "about $1.78 M" |
| CUM_5 | Cumulative result at the end of year 5 | running sum of D23 | −$0.5795 M. Never write "break-even within five years" |

Values checked against `python/data/model_out.csv` (authoritative). It matches my hand figures, with these refinements: D07a 6.03% and D07b 4.52%; D13 66.6×; D17 $74.9 M; D19 6.06%; D27 SOM share of SAM 5.77%.

Consistency rule: ch. 2 uses the blended price (D08) for both TAM and SAM, so TAM ≈ $0.33 B, SAM ≈ $75 M, and the year-5 SOM (revenue $4.32 M) is about 5.8% of the SAM (D20 ÷ D17). Ch. 5 and 8 may quote the tier prices separately (A07, A08).

### 10.4 Symbols for formula (1) (ch. 8)

Break-even tool cost per order = ρ × r × φ × c, where
ρ = relative reduction of fit-related returns (A04),
r = return rate of online apparel orders (S01),
φ = fit-related share of returns (A03),
c = cost per return (D02).
Numeric check: 0.15 × 0.244 × 0.40 × $6.80 = $0.0996.
Formula (1) is ours, written "following the logic of [gustafsson2021, §6]".

## 11. Open points for master-se

1. Fifth risk "scan unit cost" in ch. 9 (see above).
2. The chapters should use the blended price for TAM and SAM. PRD v1.2 does not state the price.
3. The funding ask in ch. 10 is about $1.78 M, from the model (D25), derived and tagged. (Closed by master-se, PRD v1.4.)
4. The pilot design assumes shopper-level randomization on a retailer's site. If the first client cannot randomize, the fallback is a matched before-and-after comparison, which is weaker. Do you want it named in ch. 6?
5. Calibration build: I need one chapter compiled early to measure words per page before I write the rest.
