# Sources notes (R1) — writer-se, 2026-11-18

18 entries in `C:\biu\02\references.bib`. Verification: DOIs resolved through the Crossref API (title, authors,
volume, pages match the bib). Industry/arXiv URLs opened, HTTP 200, 2026-11-18.
"Read" = I read the text myself. "Abstract only" = I read only the abstract (via Crossref/Semantic Scholar/arXiv);
quote nothing beyond the abstract for these.
Section numbers come from my text extraction, not the print pagination; check them in the PDF before putting a page number in the text.

## 1. Return rates and cost of returns

**nrf2024** (NRF + Happy Returns, 5 Dec 2024; read the landing page, not the PDF)
- Total returns for the retail industry are projected at **$890 billion in 2024** (key findings list).
- 76% of consumers say free returns are a key factor in where they shop; 93% of retailers call return fraud a significant issue.
- Chapters: Intro & Problem, Risks.
- WARNING: the figure conflicts with appriss2024 ($685 B). The methods differ (NRF projection vs. Appriss/Deloitte survey plus Census). Cite one, or state the range and name both.

**appriss2024** (Appriss Retail + Deloitte; read the PDF)
- Total 2024 returns **$685 B = 13.21% of sales**; fraud and abuse **$103 B = 15.14%** of returns (Executive Summary, p. 1).
- Return rate from online sales (BORO+BORIS) **24.52%**, about $215 B (summary table); returns from online sales are $362 B (p. 2).
- BORIS+BORO account for over 52% of all return dollars.
- Basis: surveys of 150 North American retail executives and 1,000 consumers, plus U.S. Census data.
- Chapters: Intro & Problem, Market (the SAM argument), Financials (return rate).

**coresight2023** (Coresight Research, 4 Apr 2023; read)
- Online apparel return rate **24.4%** for the 12 months ended 6 Mar 2023, against a 16.5% average online rate (NRF figure quoted by Coresight). Survey of 100 US apparel decision-makers.
- 24.4% of Coresight's $155.8 B estimate of the 2023 US online apparel and footwear market is **$38 B** in returns, with **$25.1 B** processing cost.
- Top return reasons: size/fit **53%**, colour 16%, damage 10% (Figure 5).
- Chapters: Intro & Problem, Market, Financials.
- Caveat: US only, and a small survey sample.

**gustafsson2021** (IJPDLM 51(8):877–896; read the full text)
- The cost of a return is about **17% of prime cost**. Handling plus transport are **72%** of the total (Abstract; Section 6).
- If well calibrated, digital product fitting can cut fit-related return costs by **up to 80%** (Abstract).
- Case: a Scandinavian fashion-footwear retailer, 2,229 returns over 261 days, overall return rate 28% (Sections 3–4).
- Section 6 gives a break-even rule for the fitting tool's cost, which we can reuse as the **formula** in the Financial Plan. It is about EUR 1.1, 1.6 and 2.1 per pair at 40%, 60% and 80% fit verification, which is about EUR 12k, 18k and 23k per year.
- Chapters: Intro & Problem, Product, Business Model (the value we create for the client), Financials.
- Caveat: footwear, not apparel, and one retailer.

**patel2025** (J. Innov. & Knowl. 10(5):100779; read abstract and parts of the text)
- Data: 496,365 items ordered by 75,707 customers, Swedish fashion platform, 2015–2022.
- Customers using the size finder were **0.65% more likely to return an item**. But customer lifetime value rose **7.51%** next quarter and 5.53% the quarter after.
- Chapters: Risks (honest counter-evidence: a size tool does not automatically cut returns), Business Model (the CLV argument), Go-to-Market.
- Use this to say that ClosetTwin must prove its effect with a pilot and A/B test.

## 2. Virtual try-on, AR

**chen2024** (Applied Sciences 14(24):11839; abstract read)
- Systematic review of **69 articles** on how virtual try-on (VTO) affects consumer behaviour. Key drivers of purchase and adoption: attitudes, media, symbolic and technological gratification, emotional and utilitarian value, user attributes.
- Chapters: Competition, Go-to-Market (why shoppers adopt).

**islam2024** (IEEE Access 12:29475–29502; abstract read)
- Survey of deep-learning VTO models in three types: image-based, multi-pose, video. States that VTO "has the potential to reduce returns and optimise conversion rates".
- Chapters: Product & Tech, Competition.

**ghodhbani2022** (Multimed. Tools Appl. 81(14):19967–19998; metadata only)
- Survey of virtual try-on outfits and their challenges. I saw no abstract text, so no facts to quote.
- Chapters: Product & Tech (background only).

**song2023** (arXiv:2311.04811, preprint, v4 Sep 2024; abstract read)
- Survey of image-based try-on: pipeline, person representation, clothing warping, try-on stage. Evaluates open-source methods with unified metrics (CLIP-based semantic check).
- Chapters: Product & Tech. Preprint, so label it as such.

**pfaff2025** (J. Retail. Consum. Serv. 87:104442; abstract read)
- AR enablement is most effective for larger products with higher spatial fit uncertainty (home-interior retailer, pandemic store closures as the identification strategy).
- It is not apparel, so use it only as analogous evidence that AR can lower fit uncertainty and raise online sales.
- Chapters: Intro & Problem (fit uncertainty), Product (analogy).

## 3. Body scanning and size recommendation

**alhassawi2025** (Sci. Rep. 15:40781; read the open-access text)
- 677 participants scanned in 3D. **90.84%** showed size variation across bust, waist and hip, and **35.45%** were not adequately accommodated by the existing sizing scheme.
- SVM on primary measurements reached **89.66%** accuracy (PCA-SVM 68.97%). Sizes 32 and 34 got no correct predictions because of overlapping features and too few samples.
- Chapters: Product & Tech (model choice), Risks (accuracy limits on edge sizes).

**alemany2013** (3DBODY.TECH proceedings; read)
- Clothing companies each define their own size chart, so shoppers must try several sizes. Returns carry high management, logistics and operations cost.
- Existing technologies have "not achieved a compromise between cost, efficacy and accuracy", which is a gap we can claim to address.
- Chapters: Intro & Problem, Product & Tech, Competition. It is a 2013 paper, so call it background.

**peng2023** (3DBODY.TECH 2023, Decathlon; read the abstract)
- Textile return rate is reported between **20% and 40%**. Experiment with 175 women (XS–4XL), 6 garments, 3D scanner.
- Fit preference significantly changes the chosen size, and knowing the 3D shape alone is not enough for size recommendation.
- Chapters: Intro & Problem, Product & Tech (our model needs preference input as well as the scan).

**sembium2017** (RecSys '17:243–250; abstract read)
- Latent-factor model on Amazon shoe data. **17–21% AUC improvement** over baselines. Online A/B test: +0.49% in the share of "Fit" transactions.
- Chapters: Product & Tech (data-driven size recommendation), Competition.

**abdulla2019** (WWW '19 Companion:327–334; abstract read)
- Size recommender using Word2Vec embeddings plus GBM. States that online shopping "yields a large percentage of returns due to size and fit".
- Chapters: Product & Tech, Competition.

## 4. Market size

**imarc2026** (IMARC Group; read)
- Virtual fitting room market **USD 8.5 B in 2025**, forecast **USD 52.6 B by 2034**, CAGR **21.80%** (2026–2034).
- Chapters: Market (TAM).
- Caveat: a commercial market-research page, and market-research publishers' figures vary widely (I saw about 4.9 B for 2023 and 6.9 B for 2024 in other listings). State the definition and show the range.

**kings2026** (Kings Research; read)
- Global e-commerce apparel market **USD 726.05 B in 2024**, USD 779.28 B in 2025, USD 1,345.45 B by 2032, CAGR 8.11%. Asia-Pacific 42.70%.
- Chapters: Market (the context for the TAM funnel).

## 5. Consumer behaviour and body diversity

**zhang2024** (J. Acad. Mark. Sci. 53(2):643–672; abstract read)
- Thin-model photography makes larger-size shoppers perceive more fit risk and buy less. Models of the shopper's own size reduce this effect. Free returns and measurement information hide it.
- Chapters: Product (inclusive avatars as a design principle), Go-to-Market.

## Count by type

- Peer-reviewed journal articles with DOI: 8 (gustafsson2021, patel2025, chen2024, islam2024, ghodhbani2022, alhassawi2025, pfaff2025, zhang2024)
- Peer-reviewed conference papers with DOI: 4 (alemany2013, peng2023, sembium2017, abdulla2019)
- Preprint (arXiv): 1 (song2023)
- Industry reports and market research with URL: 5 (nrf2024, appriss2024, coresight2023, imarc2026, kings2026)
- Total: **18**

## Chapter coverage and gaps

| Chapter | Sources | Status |
|---|---|---|
| Intro & Problem | nrf2024, appriss2024, coresight2023, gustafsson2021, peng2023, alemany2013, pfaff2025 | covered |
| Market TAM/SAM/SOM | imarc2026, kings2026, coresight2023, appriss2024 | covered for TAM and SAM. **No source for SOM**, which is our own assumption and must be labelled so. No source for regional or retailer-count data (number of fashion e-commerce sites). |
| Competition | chen2024, islam2024, abdulla2019, sembium2017 | **GAP**: no primary source on named vendors (e.g. size-recommendation and try-on providers). I did not invent any. Need vendor pages or press releases, to be checked one by one. |
| Product & Technology | alhassawi2025, alemany2013, peng2023, sembium2017, abdulla2019, song2023, islam2024 | covered. |
| Business Model & Pricing | gustafsson2021, patel2025 | **GAP**: no source for SaaS pricing benchmarks or per-scan costs. Prices are assumptions. |
| Go-to-Market | patel2025, chen2024, zhang2024 | partial. **GAP**: no source for B2B sales cycles or retailer integration (e.g. Shopify platform data). |
| Operations / Team / Roadmap | none | **GAP**, probably acceptable: mostly our own plan. If we state cloud or GPU costs, we need a vendor price page. |
| Financial Plan | gustafsson2021 (formula), coresight2023, appriss2024 | covered for the benefit model. All our own figures are labelled assumptions. |
| Risks | patel2025, alhassawi2025, nrf2024 | partial. **GAP**: privacy and biometric-data law (e.g. GDPR text on EUR-Lex). I know it exists but have not opened it, so it is not in the bib yet. |
| Conclusion | none needed | n/a |

## Known weak points

- Return-rate headline numbers conflict (NRF $890 B vs. Appriss $685 B; online apparel 24.4% Coresight vs. 24.52% Appriss for all online sales; 20–40% in Peng). The text should say "roughly a quarter of online apparel orders" and cite two sources.
- McKinsey *State of Fashion* and Statista were on the requested list. I could not open the McKinsey page (the request timed out) and Statista needs a login, so neither is in the bib. Better to leave them out than to cite them unread.
- MarketsandMarkets blocked my fetch (HTTP 403) and was excluded. Sembium, Abdulla, Pfaff and Islam publisher pages were also blocked or empty, so I used Crossref plus Semantic Scholar abstracts and treated them as abstract-only.
- The bib passes `biber --tool --validate-datamodel`. No LaTeX build was run because there is no LaTeX yet.

---

# R2 additions (2026-11-18)

All pages below were opened (HTTP 200) on 2026-11-18. Vendor pages are the vendor's own marketing claims, so in the text write
"X states that ..." and never present them as independent evidence. Only what the page itself says is recorded here.

## 6. Competition (official vendor pages)

| Key | Offering (as stated) | Scan? | B2B model (as stated) |
|---|---|---|---|
| **truefit_web** (True Fit) | "Fit & Sizing Intelligence for Retailers"; "20 years of real purchase-and-return outcomes across apparel and footwear"; also virtual try-on from a shopper photo and a Shopify integration page. | The page does not mention body scanning. Try-on uses the shopper's own photo. | Sold to retailers ("For Business", "Get a Demo"). No price on the page. |
| **fitanalytics_web** (Fit Analytics) | Size and fit recommendations by machine learning from "shopper preferences, sales and returns records, and a database of body scans". Deployed as a sizing widget or a full AI shopping assistant. | The shopper does not scan. Body scans are a training database. | For "apparel retailers", "Let's Talk" (contact sales). The page does not mention Snap, so I do not claim any ownership link. |
| **threedlook_web** (3DLOOK) | AI mobile body scanning from smartphone photos, 80+ measurements. Use cases include made-to-measure, uniform fitting, fitness and health, insurance. | Yes. Two guided smartphone photos, no hardware. | API plus iOS/Android SDKs, sold to businesses. Fashion is only one of its use cases. |
| **boldmetrics_web** (Bold Metrics) | "AI body data platform": a digital twin per shopper from "4–6 inputs" into "50+ body measurements"; products such as Virtual Sizer and Smart Size Chart; customer stories with Canada Goose, Helly Hansen and others. | **No scan**: "No scanning, photos, or measuring tapes". | Brand/retailer platform, "Request a Demo". |
| **mysize_web** (MySize) | "Omnichannel e-commerce platform and provider of AI-driven apparel sizing and digital experience solutions"; products list includes Size Recommendation, Smart Mirror and Smart Catalogue. | Not stated on the page I could read (much of it is script-rendered). Only the generic line above is safe to cite. | Sells to businesses ("Let's grow your business"). |
| **google2023tryon** (Google, 14 Jun 2023) | Generative-AI try-on: from one clothing image it shows how a garment drapes on real models, sizes XXS–4XL, various skin tones (Monk Skin Tone Scale). Launched for US women's tops (Anthropologie, Everlane, H&M, LOFT). Google reports that 42% of online shoppers do not feel represented by model images and 59% were dissatisfied because an item looked different on them than expected (footnote 1 on the page, source not checked). | No scan: shows the garment on pre-selected models, not on the shopper's own body (as of this 2023 post). | Free consumer feature inside Google Search/Shopping. It is a platform threat, not a B2B vendor. Later versions added the shopper's own photo, which I did not verify from a Google page. |
| **walmart2021zeekit** (Walmart, 13 May 2021) | Plan to acquire Zeekit, a "virtual fitting room platform". Customers "upload their picture or choose from a series of models" to see themselves in an item. | Photo upload, not a scan. | Acquired and used in Walmart's own shop. This shows consolidation, not a vendor you can compare prices with. |

Chapters: Competition (positioning map: scan vs. no scan; B2B vs. platform). Use the "no scan" row to say why ClosetTwin's scan is a differentiator, and
say plainly that 3DLOOK already offers scanning as an API.

## 7. Risks / privacy

**gdpr2016** (official Publications Office page; title, date and CELEX read there)
- Regulation (EU) 2016/679 of 27 April 2016, OJ L 119, CELEX 32016R0679. The page gives the OJ reference as JOL_2016_119_R_0001.
- Art. 9(1): processing of "biometric data for the purpose of uniquely identifying a natural person" is prohibited unless an exception applies. Art. 9(2)(a) allows it with explicit consent.
- Art. 4(14): biometric data is personal data from "specific technical processing relating to the physical, physiological or behavioural characteristics of a natural person, which allow or confirm the unique identification" of that person.
- **Caveat on verification**: EUR-Lex returned an empty bot-challenge page (HTTP 202) to my tools, so I could not open the official text. I read the wording of Art. 9 and Art. 4(14) on gdpr-info.eu, an unofficial copy. The bib points to the official Publications Office page, which I did open and which confirms the title and identifiers. Before the final build, someone with a browser should check the Art. 9(1) and 4(14) wording on EUR-Lex.
- Whether ClosetTwin's body measurements count as "biometric data for unique identification" is a legal question. State it as a risk and the design choice (explicit consent, on-device processing, no identification), not as a legal conclusion.
- Chapters: Risks, Product (privacy-by-design).

**BIPA (740 ILCS 14): NOT included.** The official ilga.gov site refused the connection (ECONNREFUSED) from here, through two tools and several URLs.
I did not use a secondary summary as a primary legal text. Request: someone opens the text in a browser, or I use it in the text as a named statute without a bib entry. Not recommended.

## 8. Pricing and GTM

**threedlook_pricing** (3DLOOK public pricing page)
- FitXpress (body scan API): **Starter $1,000/month** with 500 API requests, extra requests $2.00; **Pro $1,500/month** with 1,000 requests, extra $1.50; custom volume pricing above that. No integration fee.
- Mobile Tailor (made-to-measure apparel; "billed per successful scan: front and side photos turned into 80+ measurements"): **Basic $499/month**, up to 100 scans; **Premium $999/month**, up to 500 scans (7-day trial).
- Use: the only public price points I found for a smartphone body-scan API: about $2.00 down to $1.50 per scan at the margin, and about $2 per scan at the Premium Mobile Tailor tier ($999 / 500 scans). Good as a cost or price benchmark. It is a health/made-to-measure scan product, not a retail size-recommendation product.
- Chapters: Business Model & Pricing, Financials (cost-of-goods assumption for scan cost).

**popsize_shopify** (Shopify App Store listing, Popsize)
- The listing says "Free plan available. Free trial available." and describes AI size recommendations on product pages, "set up in 2 minutes". The listing text I could read does not show the paid tiers. A third-party site mirrors tiers (about $25/$50/$150 per month), but I did not verify it, so it is not cited.
- Use: shows the low-end, self-serve freemium price point for SMB Shopify merchants, which is a different segment from ClosetTwin's enterprise B2B. State that contrast.
- Chapters: Business Model & Pricing, Go-to-Market.

**shopify_dev_build** (Shopify developer docs, "Build")
- An app is a set of components declared in the app configuration; the Admin API and extensions are the integration surface; the app is distributed through the Shopify App Store; the developer hosts only the backend.
- Chapters: Go-to-Market and Product (integration path: widget plus backend).
- Salesforce Commerce docs were not checked, so there is no source for it.

## Updated count (R1 + R2)

- Peer-reviewed journal articles: 8; conference papers: 4; preprint: 1 → 13 academic.
- Industry reports and market research: 5.
- Vendor pages and press releases: 7 (truefit_web, fitanalytics_web, threedlook_web, boldmetrics_web, mysize_web, google2023tryon, walmart2021zeekit).
- Legal text: 1 (gdpr2016).
- Pricing and platform docs: 3 (threedlook_pricing, popsize_shopify, shopify_dev_build).
- Total: **29** entries.

## Remaining gaps

- BIPA: official text unreachable. No entry.
- GDPR wording: verified only through an unofficial copy (see above). Identifiers verified on the official EU page.
- Enterprise B2B SaaS pricing benchmark for size recommendation: none public (True Fit, Fit Analytics, Bold Metrics, MySize all say "contact sales"). The text must say that enterprise pricing is not public and that our prices are assumptions, benchmarked only against 3DLOOK (scan API) and Popsize (SMB).
- Salesforce Commerce Cloud integration source: not checked.
- SOM, team, roadmap, cloud/GPU cost: our own assumptions (no source).
- McKinsey State of Fashion, Statista: still excluded.
