# 02 - Red team (content): ten weakest points of the ClosetTwin plan

Reviewer: independent red-team reviewer, read-only. Procedure: `.claude/skills/red-team/SKILL.md` (v1.0): sceptical investor, assignment grader and hostile fact-checker roles.
Material: `main.pdf` (43 PDF pages; printed page = PDF page - 7 for chapters 1-10; the Hebrew summary is PDF 2 = printed ii), `chapters/*.tex`, `references.bib`, `python/data/{assumptions,model_out,funnel_check_out,sensitivity_out}.csv`, `PRD.md`.
Date: 2026-11-20. No plan file was edited.

## Ranked table

| # | Weak point | PDF / printed page | Severity | Owner of fix |
|---|-----------|-------------------|----------|--------------|
| 1 | Year-5 revenue ($782k, of which $648k comes from Europe) rests on 18 European clients, each averaging 1M orders, all paying for the whole of their first year. The 1M figure has no source, and 75% of the pilots behind it are free app-store installs | 15/8, 25/18, 31/24, 32/25 | Critical | art-se (model), writer-se (ch. 2, 5, 8) |
| 2 | Gustafsson is misread. The 17% is the return cost **per pair sold**, not per return, so the break-even formula counts the return rate twice, and all prices and break-even effects are derived from a wrong `c` | 10/3, 23/16, 31/24, 8/1 | Critical (fact) | writer-se, art-se |
| 3 | rho = 15% is applied to the whole shop, but only 25% of orders include a scan. Per scanned order that needs about a 60% cut, which is above Gustafsson's lowest scenario. "Deliberately modest" is false, and the billing base is ambiguous | 24/17, 25/18, 29/22 | Critical | writer-se, art-se |
| 4 | The "year 6 break-even" is an extrapolation that the PRD forbids. It assumes a frozen team of 12, no churn and payroll as the only cost. The ask stops at Y5 yet claims to fund Y6. There is no company-level sensitivity, and the single up-front seed contradicts the stage gate | 31/24, 37/30 | High | art-se, writer-se, master-se (PRD MC-1) |
| 5 | The pilot design does not work for 25 of the 30 Israeli candidates. A mid-size retailer gets about 3,850 orders per arm in 4 weeks against the stated minimum of 12,000. Its MDE is 19%, above the 15% base case. The low-touch European pilots have no stated control | 27/20, 28/21, 26/19 | High | writer-se |
| 6 | The 50% pilot-to-paying rate has no source, is admittedly the weakest input, has no sensitivity analysis, and is not applied consistently (Israel actually converts at about 35%) | 26/19, 32/25, 35/28 | High | art-se, writer-se |
| 7 | The plan cherry-picks the Knesset report. The same report has Nov-2024 Statista order shares (AliExpress 57%, SHEIN 12%, Temu 7%; Terminal X 12% of local-site orders). The plan uses the 2020 ranking instead, and claims that no source sizes any Israeli fashion e-tailer | 13/6, 26/19 | High (fact) | writer-se |
| 8 | Israel strategy: 3 years and about $1.04M of burn in a market whose whole SAM is $198k a year. The reference value for Europe is asserted but never argued, and the Israel-to-EU bridge contradicts the European revenue model | 13/6, 26/19, 31/24 | High | writer-se |
| 9 | The cost base is unsupported. Scan cost $0.03 and $90k per person-year have no basis. There are no cost lines for marketing/CAC, cloud, legal or travel (A28 CAC $25k is defined but unused). The 3DLOOK "67x" comparison picks the wrong product and tier | 25/18, 29/22, 33/26, 35/28 | Medium-High | art-se, writer-se |
| 10 | The Hebrew summary contradicts the English (7.8% "drop in returns", "17% of production cost", an overstated legal "only"), contains a draft placeholder and "2024-2024", and omits the deficit and break-even. The English text has a broken `\ref` ("Chapter efch:business") and an unsourced "Google offers free try-on" | 2/ii, 16/9, 35/28 | Medium | writer-se (text), fix-se (if `\r` escaping recurs) |

---

## Details

### 1. Year-5 revenue sits on one stacked, unsupported assumption chain (Critical)
- **Where:** PDF 15 / p. 8: "Total revenue in year 5 is $782,000. Of this, Israeli subscription revenue is only $54,000, European subscription revenue is $648,000 and pilot fees make up the rest". PDF 25 / p. 18: "A European client with the assumed 1,000,000 orders a year pays $36,000, which is why the plan depends on Europe." PDF 32 / p. 25: "it does so on an assumed average of one million orders per European client."
- **Arithmetic check (passes):** the Y4 to Y5 jump does follow from `assumptions.csv`. Y4 = 5 x 250k x $0.036 (45,000) + 3 x $2,500 + 36 x 25% x $5,000 (45,000) = **$97,500**. Y5 = 6 x 250k x 0.036 (54,000) + 18 x 1M x 0.036 (648,000) + 2 x 2,500 + 60 x 25% x 5,000 (75,000) = **$782,000**. COGS, operating results, the peak deficit ($2,332,375) and the ask ($2,798,850 = 1.2 x deficit) all reproduce.
- **Why it is weak:** the arithmetic is right, but the inputs contradict each other.
  - `A26e_5` = 18 is a **year-average** count, equal to 50% of the 36 Y4 pilots. That means every converting pilot is already paying on 1 January of Y5. The plan's own timing makes this impossible: a 9-month sales cycle (A18), then 4 weeks of sales plus a 30-day return window per pilot, with all 36 pilots starting only in Y4 (European headcount also arrives only in Y4, PDF 29 / p. 22). Israel uses the realistic pattern (Y1 pilots, year-average 2 clients in Y2). Europe does not.
  - 1,000,000 orders per client is $80M of online GMV per client at the $80 AOV. It is `assumed` with no basis ("Unchanged"). Yet 75% of European pilots are **free low-touch app-store installs** (A31e = 0.25 direct), a channel that does not typically serve $80M-online retailers. Each converted low-touch pilot is still credited with 1M orders.
  - About 83% of Y5 revenue ($648k / $782k) and the whole break-even case depend on this one cell.
- **Fix demanded:** (a) in the model, convert pilots with a time lag (half-year convention or quarterly), so that Y5 European year-average clients reflect the timing. (b) Replace the single 1M with a distribution by channel: direct pilots get an enterprise size, low-touch pilots get a small-merchant size and their own conversion rate. Source at least one band (for example a European retailer-size source). (c) Restate the Y5 revenue, the SOM (2.1% of SAM) and F5 from the new model, in ch. 2 sec. 2.5, ch. 5 sec. 5.5, ch. 8 sec. 8.2 and the Hebrew page.

### 2. Gustafsson et al. are misquoted: 17% is the cost per pair sold, not per return (Critical, fact-check failure)
- **Where:** PDF 10 / p. 3: "the cost of a return is approximately 17% of the prime cost". PDF 23 / p. 16: "The cost of a return is 17% of the prime cost [4]. With an $80 order and a prime cost that we assume to be 50% of it, the prime cost is $40 and a return costs $6.80." PDF 31 / p. 24, eq. (8.1): `c_be = rho x r x phi x c` with `c = $6.80`. The stat card on PDF 8 / p. 1 says the same.
- **What the source says** (full text, IJPDLM 51(8), sec. 6): "The return cost per the net sales of shoes is then 52,501/11,133 ≈ 5 EUR per shoe, which is approximately 17% of the shoes' prime cost (which is assumed to be €30)". The conclusion reads: "The return cost **per net sales of shoes** ... was 17% of the prime cost". The paper's abstract compresses this to "the cost of a return", which is the sentence the plan copied. Table 2 gives €52,501 a year for about 3,117 returns a year (11,133 pairs x 28%), so the cost **per return** is about €16.8, roughly **56% of prime cost**. The paper's "prime cost" (€30) is the retailer's **purchase price**, one fifth of the €150 selling price. The plan's 50% of AOV is not that definition. The paper's own fit-related share is r2 = 0.55 r1, so 55% of returns, against the plan's assumed 40%.
- **Why it is weak:** the formula multiplies by the return rate `r` a second time, because the 17% figure already contains a 28% return rate. The core formula (the assignment's showcase equation), the $0.0996 value, the 40% / 30% price shares, the retailer break-even effects of 6.03% / 4.52%, F6 and the sensitivity CSV are all derived from a misread number. The error happens to understate the value, but a hostile reviewer only needs to show that the one cost source was misread.
- **Fix demanded:** in ch. 1 sec. 1.3, ch. 5 sec. 5.2, ch. 8 eq. (8.1) and Table 8.1, either (a) use the per-return cost implied by Table 2 (about 56% of purchase price, or about 11% of selling price) with the paper's definition of prime cost, or (b) keep 17% but define `c` as the return cost per order sold and drop `r` from the formula. Then re-derive the prices, the break-even rho and F6, and fix the stat card wording.

### 3. rho = 15% "shop-wide" with 25% scan uptake is not "deliberately modest" (Critical)
- **Where:** PDF 24 / p. 17: "The reduction of 15% is deliberately modest. Gustafsson et al. test reductions between 40% and 80%". PDF 29 / p. 22: "a scan cost of $0.03 on the 25% of orders that include a scan". In `assumptions.csv`, A04 is "relative reduction of fit-related returns **shop-wide**" and A13 = 0.25.
- **Why it is weak:** if only 25% of orders involve a scan and the tool can affect only those orders, a 15% shop-wide reduction needs about **60% fewer fit-related returns among scanned orders**. That is above Gustafsson's lowest (40%) scenario, and it contradicts Patel's +0.65% result. The plan never connects A04 and A13. The same dilution hits the pilot: under intention to treat, the 7.8% MDE at a large retailer corresponds to about a 31% effect among users. There is also a billing problem. Ch. 5 says the retailer pays "per order served", but the model bills **every** order of the client (A11 x D08). If "served" means orders that used the widget, revenue falls by about 75%.
- **Fix demanded:** in ch. 5 sec. 5.2 and ch. 8, split rho into `rho_user x uptake` and give uptake a basis or a range. Restate "deliberately modest" honestly. Define the billing base in Table 5.1 and make the model match it. In ch. 6, state the user-level effect that the ITT design can detect.

### 4. "Run-rate break-even in year 6" and the $2.8M ask do not hold together (High)
- **Where:** PDF 31 / p. 24: "Run-rate break-even needs about 37 European paying clients, a level the plan passes in year 6, outside the model horizon." PDF 37 / p. 30: "It funds the Israeli pilots, the Europe entry in year 4 and the run to run-rate break-even in year 6." "Nothing else is funded until a large-retailer pilot passes the 10% line."
- **Check:** 37 reproduces only under narrow conditions. Take fixed cost $1.08M + $73.5k pilots, minus pilot fees and the Israeli margin, divided by a contribution of $28,500 per European client: that gives about 36.2. This holds only if (i) headcount stays at 12 while serving 37 to 48 enterprise clients plus 60 pilots a year, (ii) churn is zero (A27 = 10% exists but is "optional" and unused), and (iii) payroll plus pilots is the whole cost base. Y6 reaches 48 clients only if 60 pilots at 50% conversion all pay from the start of the year.
- **Why it is weak:**
  - PRD MC-1 says "No extrapolation", and Y6 is not in the model.
  - The ask covers the deficit only to the end of Y5, but the text says it funds the run into Y6.
  - A single up-front seed of $2.8M contradicts "Nothing else is funded until ... pilot passes". An investor would tranche the round.
  - The only sensitivity shown is the **retailer's** (F6, `sensitivity_out.csv`). There is none for the company, so PRD sec. 1's "financials survive a zero effect" is not demonstrated.
  - Reviewer's arithmetic: at 35% conversion (30% worse), Y6 has about 33.6 clients, below 37, so break-even slips to Y7. A one-year Europe delay (risk L3/I5 in the plan's own table) adds roughly one more year of about $1M burn.
- **Fix demanded:** in ch. 8, either extend the model to Y6-Y7 explicitly with headcount growth and churn, or delete the year-6 claim. Add a company-level sensitivity table covering conversion, orders per client, Europe entry year and scan cost, with the resulting ask and break-even year. In ch. 10, split the ask into tranches tied to the pilot gate.

### 5. The pilot design cannot test most of the Israeli pool (High)
- **Where:** PDF 28 / p. 21, Table 6.2: "Sample: At least 12,000 orders per arm (twice the derived minimum)", "Duration: 4 weeks of sales". PDF 27 / p. 20: "A mid-size Israeli retailer of 100,000 orders a year could detect only about 19%. Mid-size pilots therefore count as pooled evidence". PDF 26 / p. 19: "17 of the 30 candidates become pilots over five years".
- **Why it is weak:** a 100k-order retailer produces about 7,700 orders in 4 weeks, so about 3,850 per arm, under a third of the table's 12,000 minimum. Its MDE (19%) is above the 15% base case, so a true base-case effect would usually be missed. 25 of the 30 candidates are mid-size. "Pooled evidence" has no stated design (pre-registration, a pooled power calculation, or handling of heterogeneity between retailers). Only 5 retailers can run a valid individual test, and the gate ("until a large-retailer pilot passes") depends on them agreeing. The 45 low-touch European app-store pilots (75% of 60) have no stated randomization or control. Return-reason codes as the metric are not checked for reliability.
- **Fix demanded:** in ch. 6, make the duration depend on size (for example 12+ weeks for mid-size), add the pooled power calculation, state the evidence design for low-touch pilots, and reconcile Table 6.2 with the MDE text.

### 6. The 50% pilot-to-paying rate: unsourced, untested, inconsistent (High)
- **Where:** PDF 32 / p. 25: "The 50% conversion of pilots to paying clients is the weakest assumption and stays untested until the first pilots finish." The same sentence is repeated on PDF 26 / p. 19, PDF 30 / p. 23 and PDF 35 / p. 28.
- **Why it is weak:** it is named four times and quantified nowhere. Conversion should be P(pass) x P(buy | pass). With Patel's null result and a 10% pass line, P(pass) alone could be well under 50%. Israel does not use 50% at all: 17 pilots lead to 6 clients by Y5, about 35%, because of hand-set A26i counts and the A46 caps. Europe uses exactly 50%. No source or analogue is given (for example a published B2B SaaS pilot-conversion benchmark).
- **Fix demanded:** in ch. 6 and ch. 8, decompose the rate, apply one rule to both markets, show results at 25% / 35% / 50%, and label the rate `assumed` with a stated basis.

### 7. The Knesset source is cherry-picked, and "no source sizes Israeli e-tailers" is false (High, fact-check)
- **Where:** PDF 13 / p. 6: "in the 2020 sales ranking of the Knesset report, Shein, Next, ASOS and Zara appear with $151, $96, $57 and $51 million ... and Temu and AliExpress are not listed". PDF 26 / p. 19: "The plan names no Israeli retailer, because we found no verified source that gives the online size of any Israeli fashion e-tailer."
- **What the source says:** the same report (RIC, p. 8, Figure 8, Statista Nov 2024, "by share of orders") lists local sites as Super-Pharm 22, Shufersal 20, KSP 15, **Terminal X 12**, and global sites as **AliExpress 57, SHEIN 12, Amazon 7, Temu 7**, Next 5, ASOS. The 2020 chart (Figure 7) is the State Comptroller's, and **Amazon leads it with $195M**, which the plan omits. The values 151/96/57/51 are present in the chart. Their labels are images and could not be machine-checked.
- **Why it is weak:** saying Temu and AliExpress are absent from a 2020 chart while a 2024 chart in the same report shows AliExpress with 57% of global-site orders is selective quoting. The 2024 chart is direct evidence for the **assumed 45% local share** (A39) and for the large band: Terminal X is a local fashion e-tailer with a measured share. Leaving it out understates how much data was available and makes Israel's $198k SAM look more arbitrary than it needs to be.
- **Fix demanded:** in ch. 2 sec. 2.4 and Table 2.1, use Figure 8 to calibrate A39 and the large band. Name Terminal X as a candidate (a sourced share). Report Amazon in the 2020 list, or explain why it is excluded. Correct the sentence in ch. 6 sec. 6.1.

### 8. Israel as the beachhead: high cost, unargued benefit (High)
- **Where:** PDF 13 / p. 6: "The Israeli SAM fee pool is about $0.2 million a year. No team can live on that." PDF 26 / p. 19: "the Europe stage ... is entered first through Israeli retailers that already sell to the EU".
- **Why it is weak:** cumulative burn before Europe opens (end of Y3) is $1,043,250 (CUM_3), spent in a market whose full SAM is $198k a year and where Y5 Israeli subscriptions are $54k. The plan asserts that Israeli references open Europe but gives no evidence that EU retailers accept them. The "via Israeli retailers that sell to the EU" bridge does not appear in the model: the European clients are 1M-order European retailers reached by 417 to 678 cold contacts a year. A sceptical investor asks why Europe is not entered in year 2.
- **Fix demanded:** in ch. 6 and ch. 8, add an explicit argument and a model scenario for "Europe entry year 2 vs 4" (A45 already exists), with its effect on the ask. Either model the Israel-to-EU retailer bridge or drop the claim.

### 9. The cost base and unit cost are unsupported (Medium-High)
- **Where:** PDF 25 / p. 18: "We assume that a scan costs us $0.03 and that 25% of orders include one ... gross margin of 79%". PDF 29 / p. 22: "fully loaded cost of $90,000 per person-year". PDF 35 / p. 28: "one vendor's list price of about $2.00 per scan [17] is 67 times our assumed $0.03".
- **Why it is weak:**
  - $0.03 per scan has no engineering basis (A12 note: "needs engineering benchmark").
  - $90k blended covers Israeli engineers and European salespeople and is unsourced.
  - Operating cost is **only** headcount x $90k. There is no marketing, no CAC (A28 = $25,000 is defined and never used), no cloud base cost, no legal or compliance review (the plan's own Y1 milestone), no travel for 36 to 60 European pilots a year, no G&A.
  - The 67x comparison uses Mobile Tailor ($999 / 500), which the plan itself calls a made-to-measure product. The 3DLOOK page also lists FitXpress Pro at $1.50 per additional request and custom pricing above 1,000 a month, so "list price per scan" is not one number.
- **Fix demanded:** in ch. 7 and ch. 8, add a cost build-up table with non-payroll lines and a sourced salary benchmark. Use A28 or delete it. In ch. 5 and ch. 9, give the scan-cost comparison as a range across 3DLOOK tiers and add a scan-cost sensitivity for gross margin.

### 10. The Hebrew summary is inconsistent, and visible defects remain (Medium)
- **Where and why:** PDF 2 / p. ii:
  - "פיילוט אקראי של 4 שבועות יכול לגלות ירידה של כ-7.8% בהחזרות" ("a 4-week randomized pilot can detect a drop of about 7.8% in returns"). The English 7.8% is the minimum detectable **relative** reduction of the **fit-related** return rate, not a drop in returns.
  - "מחיר החזרה הוא כ-17% מעלות הייצור" ("the cost of a return is about 17% of the production cost"). The source term is the retailer's purchase price, not production cost, and the figure is per pair sold (see #2).
  - "מזהה ביומטרי הוא מידע רגיש רק כשהוא משמש לזיהוי אדם" ("a biometric identifier is sensitive data **only** when it is used to identify a person"). The English ch. 4 and ch. 9 call health-data status "an open legal question". The Hebrew "only" overstates legal certainty.
  - "(ערך נגזר והנחה, שיתעדכן מהמודל)" ("a derived value and an assumption, to be updated from the model") is a draft placeholder left in the deliverable.
  - "ב-2024–2024" (from `\range{2024}{2024}`).
  - IMARC's $8.5B leads the market paragraph, although the English calls it "context only".
  - The summary omits the $2.33M deficit, the year-6 break-even, the dependence on Europe and the 50% conversion caveat.
  - English: PDF 16 / p. 9 prints "Chapter efch:business discusses the one public price list" (source line 5-6 of `03-competition.tex` has `\r` split by a line break, so the reference is broken). PDF 35 / p. 28: "Google offers free try-on [21]". The Google post (14 June 2023) does not say the feature is free.
- **Fix demanded:** rewrite the Hebrew summary from the English numbers (writer-se) and delete the placeholder. Fix the `\ref` and the "free" claim. If the `\range` with equal bounds or the broken `\r` sequence could recur, master-se routes it to fix-se under the iron rule (for example a `\range` guard or a qa grep).

---

## Source checks (hostile fact-checker)

| # | Claim in plan (page) | Source | Result |
|---|---------------------|--------|--------|
| 1 | 24.4% online apparel return rate, 12 mo. to March 2023, 100 decision-makers; 53% / 16% / 10%; $155.8B, $38B, $25.1B (PDF 8-10 / pp. 1-3) | coresight2023 (web page) | **Matches** |
| 2 | Return cost 17% of prime cost (PDF 10, 23, 31) | gustafsson2021 (full text, sec. 6, Table 2) | **Mismatch**: 17% is per pair **sold**; per return ≈ €16.8 ≈ 56% of the €30 prime cost; prime cost = purchase price (see #2) |
| 3 | 2,229 transactions; 72% handling + transport; EUR 1.1 / 1.6 / 2.1 at 40 / 60 / 80% verification (PDF 10, 23) | gustafsson2021 | **Matches** |
| 4 | $685B returns 2024; $362B online; 24.52% online rate; 15.14% fraud; 150 execs + 1,000 consumers (PDF 9 / p. 2) | appriss2024 (PDF) | **Matches** |
| 5 | NRF $890B "projects" (PDF 9 / p. 2) | nrf2024 | **Matches** ("projected to reach") |
| 6 | Global e-commerce apparel $726.05B in 2024, APAC 42.70% (PDF 15 / p. 8) | kings2026 | **Matches**; no Europe share on the page, so the 25% is correctly labeled assumed |
| 7 | VFR market $8.5B (2025), $52.6B (2034), 21.80% CAGR (PDF 12 / p. 5) | imarc2026 | **Matches** |
| 8 | 3DLOOK FitXpress $1,000/mo, 500 requests, $2.00 extra; Mobile Tailor $499 / 100, $999 / 500; two guided photos (PDF 25 / p. 18, PDF 20) | threedlook_pricing | **Matches**, but incomplete: Pro tier $1.50 per extra and custom above 1,000; the "two photos" quote is FitXpress (health/fitness), not apparel |
| 9 | Size-finder users 0.65% more likely to return; 496,365 items, 75,707 customers; CLV +7.51% (PDF 11, 31) | patel2025 | **Matches**. Note: that size finder used customer-supplied information, not scans |
| 10 | Israeli online commerce $6.1B / NIS 22.6B (2023), 2.6% of consumption, $6.9B (2024), $11.3B (2029), fashion 21.6% (2022) (PDF 12-13) | knesset_ric2025 | **Matches** (Statista, as the plan says) |
| 11 | 2020 ranking: Shein 151, Next 96, ASOS 57, Zara 51; "Temu and AliExpress not listed" (PDF 13 / p. 6) | knesset_ric2025 Fig. 7-8 | **Values present, framing selective**: Amazon leads with $195M; Fig. 8 (Nov 2024) has AliExpress 57%, Temu 7%, Terminal X 12% (see #7) |
| 12 | Alhassawi: 677 participants, SVM 89.66% vs PCA-SVM 68.97%, 35.45% not accommodated, sizes 32 / 34 no correct predictions (PDF 20-21) | alhassawi2025 (PMC) | **Matches**. The plan omits that all 677 are **female** (relevant to a general apparel claim) |
| 13 | Google try-on: one clothing image, models XXS-4XL (PDF 17); "Google offers free try-on" (PDF 35) | google2023tryon | First claim **matches**; "free" is **not in the source** |

Twelve sources were checked against their text (13 claims): 9 match, 1 is a substantive mismatch (#2), 1 is selective (#11), 2 are partial (#8, #13).
