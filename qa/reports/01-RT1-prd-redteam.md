# RT1: red team of PRD.md v1.0 (qa-se)

Inputs: `PRD.md` v1.0, `qa/acceptance-criteria.md` v1.1, assignment PDF. Format: RT-Q<n> | PRD § | quote | problem | proposed change.
Contrast ratios were computed by qa-se with the WCAG 2.x formula from the palette hex values.

**RT-Q1 | §7 R-01 / R-02, §6 | "≥ 25 English content pages" and "Each chapter within ±1 page of §6"**
Problem: the two rows do not add up. With every chapter at its lower bound the content is 27 - 10 = 17 pages, so R-02 can pass while R-01 fails. Also R-01 counts "ch. 1 → ch. 10" while qa D1 counts through the references, so the two documents give different totals (27 vs 28-29).
Change: define content = ch. 1 through ch. 10 (references excluded, the stricter reading). Say in R-02 "and R-01 prevails". qa will change D1 to the same definition.

**RT-Q2 | §8 DoD items 3 and 4 | "qa-super reports no findings" / "a human (the user) has looked at every page"**
Problem: "no findings" cannot be proven (absence of evidence) and makes the detector judge its own pass. Item 4 names an actor (the user) who is not in the team, without a record of when or what they signed.
Change: DoD 3 = "the final qa report, from a fresh clone build, lists 0 open blocker and 0 open major findings, and every earlier finding has a 'rechecked in build <hash>' line". DoD 4 = "sign-off lines (name, date, page list) for the 19.5 items are in `qa/reports/`; the human reads the exec summary and conclusion and records it".

**RT-Q3 | §7 R-03 | "Visual check of the rendered page (pdftotext scrambles Hebrew)"**
Problem: "English names and numbers in correct order" has no test corpus and no pass rule, so a reviewer can pass any page. Visual-only is the weakest check for the course's headline requirement.
Change: require the Hebrew page to contain at least 6 Latin brand/acronym runs (ClosetTwin, TAM, SAM, SOM, B2B, AI), 5 numbers with a unit (%, $, years), 1 parenthesis and 1 sentence end next to a Latin run. Add a machine check: `pdftotext -bbox` must contain each Latin run as written and must **not** contain its reverse ("niwTtesolC", "6202"). Visual check confirms the rest. qa B3 will cite this list.

**RT-Q4 | §5.4 / §7 R-06, R-10 | "Rubik 8 pt ... Text stays live in the vector PDF" / "Only Playfair Display + Rubik are embedded"**
Problem: matplotlib falls back to DejaVu for any glyph Rubik lacks (arrows "→", "≈", "×", minus sign) and embeds Type 3 fonts by default. A single such glyph puts a third font into `pdffonts` or makes text unsearchable; nothing in the PRD forbids or checks it. Same for TikZ labels using the wrong family.
Change: add to R-06 "figure PDFs: `pdf.fonttype = 42`, no `findfont`/`Glyph ... missing` warning in the script run, `pdffonts` of each `figures/*.pdf` lists only Rubik/Playfair". qa I8 already checks this; the PRD must make it a requirement for art-se.

**RT-Q5 | §5.1, §7 R-08, R-21 | "mocha ... captions labels, links", "nothing cluttered", "works in grayscale"**
Problem: three unmeasurable or failing items. (a) Mocha #A47864 on white is **3.85:1** and on ivory **3.5:1**, below WCAG AA 4.5:1 for small text; the PRD uses it for small caption labels and links. Powder pink on ivory is about 1.4:1 (only usable with the ink edge the PRD already requires). (b) "every figure works in grayscale" has no test. (c) "nothing cluttered" (R-21) is a taste, not a target. qa also has no contrast criterion (a gap in qa v1.1).
Change: add "text under 14 pt bold / 18 pt regular has contrast >= 4.5:1 against its background; large text and graphics >= 3:1" to R-08. Use mocha-deep #6B4B3D (about 7.8:1 on white) for small mocha text; this makes Q-A (approve the tint) a dependency, not a nicety. Grayscale test: convert each figure to gray, series must differ by >= 20% luminance or be direct-labeled. R-21: replace "not cluttered" with measurable ones: margins >= 2.5 cm, <= 4 series, <= 1 figure and <= 1 table per page unless a pair is intended.

**RT-Q6 | §7 R-14 | "Every financial number and the SOM are labeled an assumption, through \assumption{} or the caption" / "Review of ch. 2, 5 and 8"**
Problem: scope is too narrow (ch. 6 conversion rates and CAC, ch. 7 team costs, and numbers inside charts are financial or assumption numbers too), and "review" has no pass rule. A macro that exists does not prove it was used on every number.
Change: scope = ch. 2, 5, 6, 7, 8, 9 and every figure/table caption in them. Pass rule: each number with $, USD, ILS, %, "x" multipliers or "years" in those chapters is either in `\assumption{}`, has a `\cite{}` in the same sentence, or sits in a table/figure whose caption starts with "Assumption:". qa greps and lists the numbers that fail. ch. 8 must open with a sentence that all projections are illustrative.

**RT-Q7 | §7 R-13, §1 | "29 verified entries, all cited" / "About 24% ... 53% ... up to 80%"**
Problem: "verified" is claimed but the PRD does not say what was verified. The criteria check that an entry exists, not that the number in the sentence is in the source. The thesis numbers are exactly the ones a grader will check. Vendor and market-report pages (`*_web`, imarc, kings) change or sit behind paywalls; IEEE web entries need an access date, and the PRD says "no invented dates" without defining it.
Change: add (a) each `@online` entry has `urldate` and, where possible, an archived link; (b) each statistic in the PRD §1 and in ch. 1-2 is traced to the source by quoting the sentence and page in `qa/reports/` (a claim-trace table); (c) a statistic with only a vendor or paywalled source is marked "reported by <source>" in the text. qa will add R10 (claim trace) to family 8.

**RT-Q8 | §7 R-16 and missing rows | "A fresh clone builds the same PDF"; (no rows for cover, prompts, topic approval, per-chapter files)**
Problem: PDFs are not byte-identical (creation date, IDs), so "same PDF" cannot pass as written. Also, assignment items that qa checks have no PRD requirement: the cover page (C1-C5, Q-E is open), the assignment's step "give the agent a prompt that includes all requirements" (S5), the assignment's topic-approval remark, and `.tex` file per chapter (FS2).
Change: R-16 = "same page count, same `pdftotext` per page, same `pdffonts` list, and 0 diff in the logs' error and warning counts between two builds". Add rows: R-22 Cover (title, subtitle, course, date, no page number, per Q-E); R-23 Prompts (`prompts/` holds the requirement-complete agent prompt, assignment §4 step 6); R-24 one `.tex` per chapter, all `\input` from `main.tex`; and a note in §3 that a business plan is an example the assignment lists, so it needs no topic approval.
