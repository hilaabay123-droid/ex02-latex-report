# ClosetTwin business plan: outline with page and word budget (T5.1)

writer-se, 2026-11-18, for PRD v1.2 §6, **revised for Israel (IL-O1, PRD v2.0: Israel beachhead, Europe expansion from year 4)**. No chapter text yet and no LaTeX.
Row IDs (C01, M02, V10, L01, IL01 …) refer to `writer/claim-trace.md`. Bib keys refer to `references.bib` (39 entries).
**IL-O1 changes the numbers.** The Israeli addressable market is far smaller than the old global-SAM logic assumed, so §10.5 replaces the client path, the team size and the ask. Where an older row or table below disagrees with §10.5, §10.5 wins.

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
**Israel in ch. 1 (IL-O1):** one paragraph in 1.2 or 1.3 says that Israeli law gives online shoppers a statutory 14-day cancellation right, that using the product does not remove it, and that the refund is due within 14 days (IL11–IL13, il_cpfta_guide), with a fee of at most 5% or NIS 100 that may not be charged for defects (IL14). This is the qualitative reason returns are structurally material in Israel. **No verified Israeli return rate exists** (claim-trace G5), so the plan's return rate stays the US 24.4% (C11) and is written "an assumption anchored on a US survey, not Israeli data". The cancellation right is cited from the official Authority guide, not from a statute quote.

## Chapter 2. Market: TAM / SAM / SOM (4 pp, 1,200 words)

F1: nested shapes, not to scale, one reference year per label: **Israel online fashion (TAM) ⊃ local Israeli e-tailers in the large and mid bands (SAM) ⊃ our year-5 Israeli subscription revenue (SOM)**, with a separate **Europe layer** shown beside it (not nested, not in the Y1–Y3 base case, R-27). Table T1: SAM inputs with the class of each (sourced / derived / assumed).

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 2.1 | Method and its limits | We size Israel bottom-up in orders and fees. The Israeli market numbers are **Statista estimates relayed by a Knesset research report** (not a Central Bureau of Statistics release), and the 2022 fashion figure is of that year. Publisher figures for virtual fitting rooms are context only. | knesset_ric2025 IL17–IL19; imarc2026 M01 | 250 |
| 2.2 | Israeli online commerce in context | Israeli online commerce was about $6.1 B in 2023 (NIS 22.6 B), is estimated at $6.9 B in 2024 and forecast at $11.3 B in 2029; fashion is its largest category (21.6% in 2022). The virtual-fitting-room market is reported as growing fast (IMARC alone, with its limit). | IL17, IL17b, IL18, IL19; M01 | 250 |
| 2.3 | TAM: Israeli online fashion | Online fashion in Israel is about $1.49 B in 2024 (21.6% × $6.9 B, share held at its 2022 value; about NIS 5.5 B at 3.70), or about 18.6 M orders at an assumed $80 order value. At the blended fee that is a fee pool of only about $0.67 M a year. The ILS rate is 3.70, derived from IL18. | IL17b, IL18, IL19; X01, D29, D30 (§10.5) | 250 |
| 2.4 | SAM: local Israeli e-tailers only | The largest Israeli fashion sites are foreign (Shein, Next, ASOS, Zara; IL21) and are **not** in our SAM. We assume 45% of orders go to local e-tailers (about 8.4 M orders) in three size bands (5 large, 25 mid, 250 small, all assumed). We address large and mid retailers only: 5.5 M orders, a fee pool of about **$0.20 M a year**. | IL21; A39–A41 (§10.5) | 250 |
| 2.5 | Europe layer and SOM | The Israeli SAM cannot fund a team, so Israel is the **proof market** and Europe, entered in year 4, carries revenue. Europe's fee pool is about $82 M (25% of global e-commerce apparel, assumed) and its SAM about $33 M. The year-5 SOM is about $0.78 M, of which Israeli subscription revenue is only $54 k (§10.5). Tagged *assumed* or *derived*. | kings2026 M02, M03; A42; D35–D37 (§10.5) | 200 |

Notes: IMARC alone, with the limit "definition and method not public" (master-se ruling; no publisher range). T1 columns: input | value | class | source or basis. Say "fee pool", never "market size", for our numbers. The text must state in one sentence that **Israel's SAM fee pool is about $0.2 M a year, so the Israeli plan is a reference-customer strategy and not a revenue strategy.** Do not compute a cross-border share from IL20 (claim-trace IL20).

## Chapter 3. Competition (3 pp, 650 words)

Table T2 "Vendor claims", two parts (direct / platform and in-house threats), blank cells read "not stated". F2: positioning map, axes x = questionnaire or size chart ↔ body scan, y = consumer app ↔ B2B plug-in.

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 3.1 | How to read this table | Everything in it is what a vendor says about itself. | none | 80 |
| 3.2 | Direct vendors | The direct field splits on one question: does the shopper scan, give a few inputs, or neither? **MySize is Israel-based** (principal executive offices in Airport City per its FY2022 10-K, incorporated in Delaware, listed on Nasdaq), so it is a direct competitor in the home market; its own page says nothing checkable about scanning or price. | truefit_web V01–V02; fitanalytics_web V03; threedlook_web V05; boldmetrics_web V04; mysize_web V06; mysize10k2022 IL25 | 220 |
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
| 4.6 | Privacy by design: scan for fit, not identification | Under Israel's Privacy Protection Law as amended by Amendment 13 (in force 14 Aug 2025), a biometric identifier is "data of special sensitivity" when it is "used or intended to be used to identify a person or verify his identity". ClosetTwin scans for fit only, so the design never uses body data to identify anyone, collects the minimum, and offers explicit consent as **our design choice** (the law's definition of consent is "explicit or implied"). The regulator's own documents frame data minimization and privacy-enhancing technology as the route to trust: framed as the Authority's view, not as proof that customers pay for it. | il_amend13_2024 IL01–IL04; il_ppl_en IL05, IL08; ppa_data_minimization2021 IL09 *(draft opinion)*; ppa_pets2025 IL10; gdpr2016 L01–L03 (secondary, forward to ch. 9) | 100 |
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
| 5.5 | Unit economics and the scan-cost condition | Gross margin is high only if a scan costs us about $0.03. At 3DLOOK's list price per scan (about $2.00, derived from V11) the scan alone would cost about 67 times our assumed $0.03 (D13) and the model fails. **A second honest limit for Israel:** at 250,000 orders a year, an average Israeli client pays about $9,000 a year (D38 × D08), so the price per order is right for the client but the ticket is small. Prices are in USD, with the NIS equivalent at 3.70 where a retailer would read it in shekels (for example $0.036 ≈ NIS 0.13 per order). | V11; assumptions A12–A13, X01, D38 (§10.5) | 180 |

## Chapter 6. Go-to-Market (2 pp, 360 words)

Tables T4 (funnel) and T5 (pilot design). No funnel figure.

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 6.1 | Segments and channels | **Israel first, by direct sales to the 30 large and mid local fashion e-tailers** (5 large, 25 mid, assumed counts). We name no Israeli retailer, because no verified source gives any Israeli fashion e-tailer's online size (claim-trace G5). Shopify is a minor Israeli channel (about 4% of .il shops in one weak tracker, IL24; an agency launched in 2024, IL22), so the low-touch App Store route is reserved for the Europe stage. **Europe from year 4**, entered through Israeli retailers that sell to the EU and through the Shopify App Store. | globes2024shopify IL22, IL23; aguko_shopify_il IL24 *(low confidence)*; shopify_dev_build V14; knesset_ric2025 IL21 | 120 |
| 6.2 | The funnel | Israel: of 30 candidates, 17 become pilots over five years (57%) and about 6 paying clients in year 5 (20% of the pool). Europe: from year 4, 36 then 60 pilots a year. All rates assumed. The year-by-year path fits the sales team (T4). | T4; assumptions A15i, A16i, A17, A26i, A26e, A35–A37, A43 (§10.5) | 90 |
| 6.3 | The pilot design | A shopper-level randomized pilot can detect a relative reduction of about **7.9% at a large Israeli retailer (600,000 orders a year, 4 weeks)** and about 6.1% at a European retailer of 1M orders a year, against a pass line of 10% and a break-even effect of 4.5–6.0%. At a mid-size Israeli retailer (100,000 orders a year) the same pilot detects only about 19%, so mid-size pilots are pooled evidence and **only large-retailer pilots are individual tests**. A before-and-after comparison is the fallback if a retailer cannot randomize, labeled weaker evidence. | patel2025 C22–C24; T5; assumptions A19–A24, D19i, D19e (§10.5) | 150 |

T4 (funnel; all assumed or derived; check with `funnel_check_out.csv` after art-se updates the model), one row per year 1–5:

| Year | Israeli pilots | European pilots | Contacts needed | Sales-contact capacity | Capacity used |
|---|---|---|---|---|---|
| 1 | 4 | 0 | 22 | 414 | 5% |
| 2 | 4 | 0 | 22 | 552 | 4% |
| 3 | 4 | 0 | 22 | 690 | 3% |
| 4 | 3 | 36 | 417 | 1,242 | 34% |
| 5 | 2 | 60 | 678 | 1,656 | 41% |

Israeli contacts use a warmer funnel (contact → meeting 60%, meeting → pilot 30%, 18% of contacts) because the pool is 30 retailers and the market is small; European contacts use 30% × 30% = 9%. Israeli contacts never exceed the pool of 30. Capacity = 25% of headcount × 12 contacts a week × 46 weeks (A35–A37), with headcount 3 / 4 / 5 / 9 / 12.

T5 rows: metric (fit-related return rate = orders with a size/fit return reason ÷ orders), design (shopper-level 50/50 randomization, intention to treat), sample (derived), duration (4 weeks of sales plus a 30-day return window; longer for retailers below the order volume that gives a detectable effect), pass line (assumed), fail rule (stop and do not scale), evidence class (large-retailer pilots: individual tests; mid-size pilots: pooled evidence only), fallback if a retailer cannot randomize (matched before-and-after comparison, labeled weaker evidence).
Israeli pilots come from warm design-partner contacts (ch. 7). A pilot starts only after the Amendment 13 compliance milestone (ch. 7).

## Chapter 7. Operations, Team & Roadmap (2 pp, 540 words)

F4: Gantt strip, 6 rows, times as "Y1 Q1" style (no calendar dates). Everything here is tagged *assumed*.

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 7.1 | Operating model | The service is a capture widget, an inference backend and a data feed, run on rented cloud capacity. | none | 130 |
| 7.2 | Team and roles | A lean team of 3 growing to 12 over five years (3 / 4 / 5 / 9 / 12, assumed) covers engineering, data science, partnerships and compliance. **Roles only, no names (UD-5).** | none; assumption A25 | 180 |
| 7.3 | Roadmap | Six workstreams, with the pilot gating everything after it. Timing (assumed, relative quarters): MVP in Y1 Q1–Q2; **Amendment 13 compliance milestone (privacy review, consent flow, database-notification check) in Y1 Q2, before any pilot data are collected**; the first Israeli pilots in Y1 Q3–Q4 from warm design-partner contacts (a 9-month sales cycle, A18, leaves no time for cold starts); first paying Israeli clients in Y2; GDPR Art. 9 review in Y3 Q3; **Europe entry (pilots) in Y4**, first European paying clients in Y5. | F4; A18, A26ip, A26eq (§10.5); il_amend13_2024 IL02 | 150 |
| 7.4 | Dependencies | Three dependencies matter: the pilot result, a consent flow that holds up legally under Amendment 13, and the pilot-to-paying conversion of 50% (A17), which stays untested until the first pilots finish. Europe's revenue depends on all three. | link to ch. 8 and ch. 9 | 80 |

## Chapter 8. Financial Plan (3 pp, 450 words)

Formula (1), F5 (two panels: 5-year projection and break-even), F6 (sensitivity), Table T6 (assumptions: value / class / source).

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 8.1 | The break-even logic and formula (1) | The break-even tool cost per order is the fit-related return cost avoided per order, written "following the logic of [gustafsson2021, §6]" and defined symbol by symbol (§ 10 gives my symbols). | gustafsson2021 C20, C21; formula is ours | 150 |
| 8.2 | Five-year projection | **Hand estimate for the Israel model (art-se recomputes):** revenue grows from $10 k in year 1 to about $0.78 M in year 5, of which Israeli subscription revenue is only $54 k. The operating result is negative in every year of the horizon (about −$0.27 M, −$0.35 M, −$0.42 M, −$0.77 M, −$0.52 M) and the cumulative result is about −$2.33 M at the end of year 5. **There is no operating profit within five years.** Write "no operating profit within the five-year horizon; run-rate break-even needs about 37 European clients, which the plan passes in year 6 (outside the model horizon)". Never write "break-even within five years" or "operating profit in year 5". The funding ask is the cumulative deficit plus a 20% buffer, about $2.8 M (§10.5). Honest limits stated in the text: Israel's SAM is about $0.2 M a year, so Europe carries the revenue; A11_EU (1M orders per European client) is an assumed average; A17 (50% of pilots become paying clients) is the weakest link and stays untested until the first pilots finish. | F5; T6 | 120 |
| 8.3 | Sensitivity to the pilot result | F6 shows the retailer's economics against ρ: the retailer breaks even at ρ = 6.03% (Growth) and 4.52% (Enterprise) (D07a, D07b). At zero effect the client would pay for nothing, so the pilot gate must stop the rollout. This is also the answer to the Patel 2025 risk in ch. 9. | F6; patel2025 C22 | 100 |
| 8.4 | A second lever | In one study, size-finder use went with higher customer lifetime value, which we mention but do not put in the base case. | patel2025 C23–C24 | 40 |
| 8.5 | The assumptions table | Every number in this chapter appears in T6 with its class. | T6 | 40 |

## Chapter 9. Risks (2 pp, 315 words)

F7: heat matrix (likelihood × impact, scores labeled assumed). Table T7: risk | mitigation | owner or trigger.

| § | Section | It must prove | Keys · claim rows | Words |
|---|---|---|---|---|
| 9.1 | The register | Five risks are rated and each has a mitigation. | F7, T7 | 55 |
| 9.2 | **Israeli privacy law (primary legal risk), with GDPR secondary** | Amendment 13 treats a biometric identifier used or intended for identification as data of special sensitivity, with duties such as notifying the Authority above 100,000 people. The mitigation is design: scan for fit, never for identification, minimal data, consent flow, and a compliance milestone before pilot data. Three stated limits: explicit consent is our design choice (the law's consent is "explicit or implied"); whether body measurements count as health data is an open legal question, a design risk and not a conclusion; the Authority's data-minimization opinion is a 2021 draft. **GDPR Art. 9 is secondary**: it applies when Israeli sites sell to EU customers and in the Europe stage. | il_amend13_2024 IL02–IL04; il_ppl_en IL05–IL08; ppa_data_minimization2021 IL09; gdpr2016 L01–L03 | 100 |
| 9.3 | Null pilot effect and weak conversion | A size tool can fail to cut returns: the largest study in our sources found size-finder users slightly *more* likely to return, and the pilot gate is the mitigation. The pilot-to-paying conversion (A17 = 50%) is the weakest link of the plan and stays untested until the first pilots finish; it is named here with the null-effect risk. | patel2025 C22, C24; A17 | 70 |
| 9.4 | Accuracy at edge sizes | The size model fails for rare sizes, so rare-size shoppers get a fallback. | alhassawi2025 P03, P01 | 60 |
| 9.5 | Platform risk | Google offers free try-on, so a retailer may rely on the platform. | google2023tryon V07 | 60 |

**Register (five rows, ordered as in 9.2–9.5 plus the scan-cost row):** (1) Israeli privacy law, GDPR secondary; (2) null pilot effect and weak conversion; (3) accuracy at edge sizes; (4) platform risk (Google); (5) scan unit cost above the model (approved by master-se, OL-2). **Sixth risk, approved by master-se: "Europe entry slower than plan" (likelihood 3, impact 5, both assumed)**, because nearly all revenue depends on it (the Israeli SAM is about $0.2 M a year). The register therefore has six rows and ch. 9 gains about 40 words (target about 355).

## Chapter 10. Conclusion (1 p, 315 words)

| § | Section | It must prove | Keys | Words |
|---|---|---|---|---|
| 10.1 | The case | The problem is large and fit-driven, and a fit tool is a hypothesis with a cheap test. | – | 100 |
| 10.2 | The ask | A seed of about $2.8 M (derived: cumulative deficit of about $2.33 M at the end of year 5 plus a 20% buffer; **hand estimate, to be replaced by the Israel model's D25**) funds Israeli pilots, the Europe entry in year 4, and the run to run-rate break-even in year 6. The text says plainly that this is a reference-market-then-expansion plan, with no operating profit inside five years. | T6; §10.5 | 120 |
| 10.3 | Next steps | The Israeli pilots come first (after the Amendment 13 compliance milestone), and nothing else is funded until one passes. | – | 95 |

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
| H7 | The price is assumed at 0.036 dollars per order (blended), about 0.13 NIS. | A07, A08, X01 | – | 0.036 $ per order |
| H8 | A shopper-level pilot of 4 weeks tests the claim, and a large Israeli retailer's pilot can detect about a 7.9% effect. | T5, D19i | – | 4 weeks; 7.9% |
| H9 | The primary privacy rule is Israel's Privacy Protection Law, Amendment 13 (in force since 14 August 2025): a biometric identifier is special-sensitivity data only when it is used to identify a person, and ClosetTwin scans for fit, not identification. GDPR Art. 9 is secondary (the Europe stage). | IL02–IL04, L01 | GDPR | 14 August 2025 |
| H10 | Israel online commerce is estimated at 6.9 billion dollars in 2024, and fashion is its largest category. The first sales channel is direct sales to local fashion e-tailers (Israeli retailers first, then Europe from year 4 through Shopify). The sentence ends with the Latin word Shopify. | IL17, IL19, V14 | Shopify | 6.9 B$; year 4 |
| H11 | The document is dated 2026 and the funding ask is about 2.8 million dollars (derived, an assumption; the final value comes from the model). | §10.5 | – | 2026; 2.8 M$ |

R-03 corpus check: Latin runs = ClosetTwin, B2B, AI, Appriss, NRF, Coresight, IMARC, GDPR, Shopify (9, need ≥ 6). Numbers with units = 685–890 B$, 24.4%, 53%, 17%, 8.5 B$, 0.036 $, 4 weeks, 7.9%, 6.9 B$, 2.8 M$ (10, need ≥ 5). Parenthesis: H9 (in force since 14 August 2025) and H10 (need 1). Sentence ending in a Latin run: H10 ends with "Shopify" (need 1). The page text contains "ClosetTwin" and "2026" for the machine check.
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
| A26 | Paying clients, years 1–5 (year average) | 0, 8, 25, 60, 120 | no source; year 1 has pilots only | 8 |
| A26p | Pilots started in year 1 | 16 (4 direct at retailers of ≥ 1M orders/yr + 12 low-touch Shopify App Store pilots) | Needed to supply year 2's 8 paying clients at A17 = 50% (funnel check); warm design-partner contacts | 6, 7, 8 |
| A26q | Pilots started in years 2–5 | 36, 75, 132, 132 | Years 2–4 from the funnel check, rounded up; year 5 assumed equal to year 4 (steady state) | 6, 8 |
| A31 | Share of pilots that are direct | 25% | no source | 6, 8 |
| A32 | Low-touch pilot fee | $0 | Free App Store trial; conservative on revenue | 6, 8 |
| A33a / A33b | Pilot cash cost, direct / low-touch | $3,000 / $500 | Direct: about $2,400 integration support (assumed) + about $600 scan cost (derived: about 76,900 orders × A13 × A12); low-touch: cloud and tooling | 8 |
| A34a / A34b | Staff effort per pilot, direct / low-touch | 1.0 / 0.25 FTE-months | Capacity check only; staff are already costed in A25 × A14 | 6, 7 |
| A35 | Sales share of headcount | 25% | no source | 6, 7 |
| A36 / A37 | Outbound contacts per sales FTE per week / selling weeks per year | 12 / 46 | no source | 6, 7 |
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
| D20 | Revenue, years 1–5 (subscription A26 × A11 × D08, plus direct-pilot fees pilots × A31 × A09) | see model_out.csv | $20,000; $333,000; $993,750; $2,325,000; $4,485,000 |
| D21 | Cost of goods, years 2–5 | A26 × A11 × D11 | $0.06 M; $0.19 M; $0.45 M; $0.90 M |
| D22 | Operating cost, years 1–5 | A25 × A14 | $0.36 M; $0.72 M; $1.26 M; $1.80 M; $2.52 M |
| D23 | Operating result, years 1–5 (D20 − D21 − D22, minus pilot cash costs) | see model_out.csv | −$358,000; −$487,500; −$538,125; −$73,500; +$916,500 |
| D24 | Peak cumulative deficit | running sum of D23 | −$1,457,125 (end of year 4) |
| D25 | Funding ask | D24 × (1 + A30) | $1,748,550, written "about $1.75 M" |
| CUM_1–5 | Cumulative result | running sum of D23 | −$358,000; −$845,500; −$1,383,625; −$1,457,125; −$540,625. Never write "break-even within five years" |
| D26–D27 | SOM (year-5 revenue) and its share of SAM | D20_5; D26 ÷ D17 | $4,485,000; 6.0% |
| F-check | Contacts needed, years 1–5 | `funnel_check_out.csv` | 178; 400; 833; 1,467; 1,467 against capacity 552; 1,104; 1,932; 2,760; 3,864 |

Values taken from `python/data/model_out.csv` and `funnel_check_out.csv` (authoritative, PRD v1.5, funnel check green). Earlier hand figures are superseded where they differ: D07a 6.03%, D07b 4.52%, D13 66.6×, D17 $74.9 M, D19 6.06%.

Consistency rule: ch. 2 uses the blended price (D08) for both TAM and SAM, so TAM ≈ $0.33 B, SAM ≈ $75 M, and the year-5 SOM (revenue $4.485 M, which includes direct-pilot fees) is 6.0% of the SAM. Ch. 5 and 8 may quote the tier prices separately (A07, A08).

### 10.4 Symbols for formula (1) (ch. 8)

Break-even tool cost per order = ρ × r × φ × c, where
ρ = relative reduction of fit-related returns (A04),
r = return rate of online apparel orders (S01),
φ = fit-related share of returns (A03),
c = cost per return (D02).
Numeric check: 0.15 × 0.244 × 0.40 × $6.80 = $0.0996.
Formula (1) is ours, written "following the logic of [gustafsson2021, §6]".

### 10.5 Israel and Europe model rows (IL-O1): these replace the rows they name

Format: **id | old → new | class | basis**. "New" rows have no old value. My hand results are checks; `python/model.py` is authoritative. Everything is in USD (UD-8); the single ILS rate is row X01.

#### A. Currency and Israeli market (new rows)

| id | old → new | class | basis |
|---|---|---|---|
| X01 | – → 3.70 NIS per USD | derived | IL18: NIS 22.6 B ÷ $6.1 B = 3.705, rounded. Used only to show NIS equivalents (`\ils{}`) and the NIS fashion figure. |
| S09a / S09b / S09c | – → $6.0 B / $6.1 B / $6.9 B (Israeli online commerce 2022 / 2023 / 2024) | sourced | knesset_ric2025 IL17b, IL18, IL17 (Statista estimates; 2024 is an estimate). |
| S10 | – → 21.6% (fashion share of Israeli online commerce, 2022) | sourced | IL19 (pie label 21.6%; the text rounds to 22%). The NIS 4.37 B behind it is a 2022 Statista figure relayed by the Knesset report. |
| D29 | – → $1.49 B (NIS 5.5 B at X01) | derived | S10 × S09c, i.e. the 2022 share held at 2024. **Why not NIS 4.37 B ÷ 3.70:** the report's own 2022 figures imply 3.37 NIS per USD (NIS 20.2 B ÷ $6.0 B), so converting a 2022 shekel figure at the 2023 rate would mix years. Using the share avoids it. |
| D30 | – → 18.6 M orders | derived | D29 ÷ A01 ($80 ≈ NIS 296 at X01). |
| A39 | – → 45% (share of Israeli online fashion orders that go to local Israeli e-tailers) | assumed | The largest fashion sites are foreign (IL21: Shein $151 M, Next $96 M, ASOS $57 M, Zara $51 M in 2020 = about $355 M) and Temu and AliExpress are not listed, so the local share is well below 100%. 45% is our choice; replace it if a source is found. |
| D31 | – → 8.4 M orders | derived | D30 × A39. |
| A40a / A40b / A40c | – → 5 / 25 / 250 (candidate local e-tailers: large / mid / small) | assumed | No source sizes Israeli fashion e-tailers (claim-trace G5). Bands only; no names. |
| A41a / A41b / A41c | – → 600,000 / 100,000 / 12,000 (orders per retailer per year) | assumed | Chosen so the bands fill D31. |
| D32 | – → 8.5 M orders (check: within 5% of D31; here +1.4%) | derived | 5 × 600,000 + 25 × 100,000 + 250 × 12,000. |
| D33 | – → 5.5 M orders (SAM orders) | derived | Large + mid bands only. The small band is not addressed (a 12,000-order shop pays about $430 a year). |
| D34 | – → $198,000 a year (Israeli SAM fee pool) | derived | D33 × D08 ($0.036). |
| D34b | – → TAM fee pool $0.67 M (D30 × D08); local-only pool $0.30 M (D31 × D08) | derived | For F1 labels. |

#### B. Europe layer (new rows)

| id | old → new | class | basis |
|---|---|---|---|
| A42 | – → 25% (Europe's share of global e-commerce apparel) | assumed | The non-APAC share is 57.3% (S05, derived); the split between North America, Europe and the rest is our assumption. |
| D35 | – → 2.27 B orders | derived | S04 × A42 ÷ A01. |
| D36 | – → $81.7 M (Europe TAM fee pool) | derived | D35 × D08. |
| D37 | – → $32.7 M (Europe SAM fee pool) | derived | D36 × A06 (40% size filter, kept for Europe only). |
| A45 | – → year 4 (Europe entry: pilots start; first paying clients in year 5) | assumed | master-se decision; not in the Y1–Y3 base case (R-27). |

#### C. Changed rows: client path, team, pilots

| id | old → new | class | basis |
|---|---|---|---|
| A06 | 40% (retailers addressed as share of orders) → 40%, **Europe only**; Israel uses the bands (A40, A41) | assumed | Scope change. |
| A11 | 1,000,000 orders per paying client → **split**: A11e = 1,000,000 (Europe, unchanged); A11i = 250,000 (Israel, derived, D38) | assumed / derived | The largest Israeli retailer has 600,000 orders a year (A41a), so 1,000,000 cannot apply. |
| D38 / A44 | – → A44 = 30% of Israeli paying clients are large, 70% mid; D38 = 0.3 × 600,000 + 0.7 × 100,000 = 250,000 orders | assumed / derived | Large-first selling. |
| A25_1..5 | 4, 8, 14, 20, 28 → **3, 4, 5, 9, 12** FTE | assumed | Israeli revenue cannot carry a bigger team; the Europe year (4) adds 4 people. Roles only (UD-5). |
| A26_1..5 | 0, 8, 25, 60, 120 → **split** (below) | assumed | The old path needs 120 clients; Israel has 30 candidates. |
| A26i_1..5 (paying Israeli clients, year average) | – → 0, 2, 4, 5, 6 | assumed | New clients = 50% (A17) of the previous year's Israeli pilots, with 10% churn (A27). Caps (check): at most 20% of the 30 candidates in years 1–3 (here 13% in year 3), at most 35% in years 4–5 (here 20%), at most 60% of the 5 large retailers (here 0.3 × 6 = 1.8, 36%). |
| A26e_1..5 (paying European clients, year average) | – → 0, 0, 0, 0, 18 | assumed | = 50% of year-4 European pilots (A26eq_4). No European revenue before year 5 (R-27). |
| A26p | 16 (pilots in year 1) → **A26ip_1 = 4** (Israel) | assumed | 4 of the 30 candidates, from warm design-partner contacts. |
| A26q_2..5 | 36, 75, 132, 132 → **A26iq_2..5 (Israel) = 4, 4, 3, 2**; **A26eq_4..5 (Europe) = 36, 60** | assumed | Israeli pilots total 17 (57% of the pool of 30) over five years. Europe: 36 pilots in its first year, 60 in the second (sales capacity: 34% and 41% used). |
| A31 | 25% direct → **A31i = 100%** (Israeli pilots all direct); **A31e = 25%** (Europe) | assumed | Shopify is a minor Israeli channel (IL22–IL24), so no low-touch route in Israel. |
| A09 | $5,000 pilot fee (direct) → **A09i = $2,500** (Israel); **A09e = $5,000** (Europe, direct only) | assumed | Mid-size Israeli clients pay about $3,600 a year, so a $5,000 pilot fee would exceed it. |
| A15 / A16 | 30% / 30% → **A15i = 60% / A16i = 30%** (Israel, small warm market); 30% / 30% unchanged for Europe | assumed | 30 candidates only: contacts needed (22 a year) never exceed the pool. |
| A29a..e | null effect 3/5; GDPR 3/4; edge sizes 3/3; platform 3/4; scan cost 2/4 → **A29b becomes "Israeli privacy law (Amendment 13)" 3/4 and a new A29g "GDPR Art. 9 (secondary)" 2/3**; **new A29f "Europe entry slower than plan" 3/5 (needs approval)** | assumed | Order and primacy of the legal risk (UD-7). |
| A22, A23, A24, A12, A13, A14, A17, A18, A27, A28, A30, A32, A33a/b, A34a/b, A35–A37 | unchanged | | |

Changed meaning: A32 (low-touch pilot fee $0), A33b, A34b apply to Europe only.

#### D. Derived results (hand calculation, USD; art-se recomputes)

| id | name | value |
|---|---|---|
| D19i | Smallest relative reduction a 4-week pilot detects at a large Israeli retailer (600,000 orders a year, 23,077 per arm) | about 7.9% |
| D19i2 | The same at a mid-size Israeli retailer (100,000 orders a year, 3,846 per arm) | about 19% (pooled evidence only) |
| D19e | The same at a European retailer of 1M orders a year | about 6.1% (unchanged) |
| D20 | Revenue, years 1–5 (Israeli subscription A26i × A11i × D08; European subscription A26e × A11e × D08; pilot fees) | $10,000; $28,000; $46,000; $97,500; $782,000 |
| | of which Israeli subscription | $0; $18,000; $36,000; $45,000; $54,000 |
| | of which European subscription | $0; $0; $0; $0; $648,000 |
| D21 | Cost of goods (orders × $0.0075) | $0; $3,750; $7,500; $9,375; $146,250 |
| D22 | Operating cost (A25 × A14, $90,000 per FTE) | $270,000; $360,000; $450,000; $810,000; $1,080,000 |
| D28 | Pilot cash cost (Israel: 4, 4, 4, 3, 2 pilots × $3,000; Europe: 9 direct × $3,000 + 27 low-touch × $500 in year 4, 15 × $3,000 + 45 × $500 in year 5) | $12,000; $12,000; $12,000; $49,500; $73,500 |
| D23 | Operating result, years 1–5 | −$272,000; −$347,750; −$423,500; −$771,375; −$517,750 |
| CUM | Cumulative result | −$272,000; −$619,750; −$1,043,250; −$1,814,625; −$2,332,375 |
| D24 | Peak cumulative deficit in the horizon | −$2,332,375 (end of year 5; the deficit has not yet peaked in the horizon; a hand estimate puts the peak at the end of year 5, because year 6 is about break-even) |
| D25 | Funding ask = −D24 × (1 + A30) | $2,798,850, written "about $2.8 M" |
| D26 / D27 | SOM (year-5 revenue) and its share of the combined SAM | $782,000; subscription alone is $702,000 = 2.1% of (D34 + D37 = $32.9 M) |
| – | Run-rate break-even | European contribution per client = $36,000 − $7,500 = $28,500; Israeli gross profit in year 5 = $54,000 − $11,250 = $42,750; clients needed = ($1,080,000 − $42,750) ÷ $28,500 ≈ 36.4 |
| – | European clients in year 6 (derived) | 18 × 0.9 + 0.5 × 60 = 46.2, above the 36.4 needed, so year 6 is about break-even (outside the horizon; art-se may extend the model to year 6) |

**What changed in the story (for the text, ch. 8 and ch. 10):** the old plan reached operating profit in year 5 with 120 clients and a $1.75 M ask. Israel cannot supply that many clients (its SAM is $0.2 M a year, 30 candidate retailers), and Europe starts only in year 4, so the plan now shows **no operating profit within five years**, revenue of about $0.78 M in year 5, a cumulative deficit of about $2.33 M and an ask of about $2.8 M. F5 must not mark a "first profitable year" inside the horizon. A **Europe-scaled sensitivity** (72 pilots in year 4, 36 clients in year 5) would bring year 5 close to break-even, but it doubles the first-year European pilot load and is not the base case.

Funnel check: Israeli pilots 4, 4, 4, 3, 2 need 22, 22, 22, 17, 11 contacts at 18% (A15i × A16i); European pilots 36 and 60 need 400 and 667 at 9%. Totals: 22, 22, 22, 417, 678 contacts against capacity 414, 552, 690, 1,242, 1,656 (headcount 3, 4, 5, 9, 12 × 25% × 12 × 46). Pilot effort: 4, 4, 4, 18.75, 28.25 FTE-months against 36, 48, 60, 108, 144 (11%, 8%, 7%, 17%, 20%).

## 11. Open points for master-se (updated for IL-O1)

1. Closed: the sixth risk "Europe entry slower than plan" (3/5) is approved, as is the scan-cost risk (OL-2).
1a. **On hold until the user decides:** the ask and profitability wording (ch. 8.2, ch. 10.2, Hebrew claim H11, §10.5 results). The lean path is the base case for now; art-se is building a scenario with Europe entry one year earlier (pilots in Y3, revenue in Y4). I will not change those wording lines until the decision lands.
2. The Israeli plan is a **reference-market plan, not a revenue plan** (SAM about $0.2 M a year). §10.5 shows no operating profit within five years and an ask of about $2.8 M. This replaces the $1.75 M of PRD v1.5. PRD §1, §6 and the F5 caption must be updated: no "first profitable year (Y5)".
3. A Europe-scaled sensitivity (72 pilots in year 4) is available if you want F6 or a scenario line; it is not the base case.
4. Model changes needed from art-se: the old single client path becomes an Israeli path and a European path with their own order volumes (A11i, A11e), pilot fees and direct shares (A09i/e, A31i/e); a currency row X01; Israeli and Europe TAM/SAM rows; the funnel check per market; and, if wanted, a year-6 column for the run-rate break-even.
5. Hebrew summary claim H11 (the ask) now says about 2.8 million dollars; it must be refreshed from the model's D25 once art-se recomputes.
6. Calibration build: I still need one chapter compiled early to measure words per page.
