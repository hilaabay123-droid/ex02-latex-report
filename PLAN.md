# PLAN: ClosetTwin Business Plan

| | |
|---|---|
| **Version** | 1.0 |
| **Owner** | master-se |
| **Date** | 2026-11-18 |
| **Implements** | `PRD.md` v1.1 |
| **Method** | The assignment's 8-stage workflow (§4) + the book's CLS-in-six-stages (§15.3) + the QA loop (§19.1) |

## 1. Principles
- **CLS first, text second.** No chapter text is written until the CLS reaches v0.5, so writer-se uses only real macros.
  This follows the book's advice to start with a minimal project that compiles (assignment §7).
- **Parallel where safe.** Figures (art-se) and chapter text (writer-se) run in parallel once the CLS and the outline are fixed.
- **Every stage ends with a compile and a look.** Each stage has an exit check, and nothing is "done" on an agent's word alone (book §19.5).
- **The iron rule.** A problem seen twice is fixed by fix-se in the CLS or a skill, with a version bump and a CHANGELOG row.
- Only master-se commits, and it commits at the end of each stage.

## 2. Stages
| Stage | Name | Owner | Depends on | Output | Exit check |
|---|---|---|---|---|---|
| **S0** | Team setup | master-se | – | Roles, mesh check, the prompt-log system | ✅ done (mesh 20/20, hook live) |
| **S1** | Requirements | master-se + committee | S0 | ✅ PRD v1.1, PLAN, TODO, `qa/acceptance-criteria.md`, `references.bib` (29), style guide | The red team's findings are logged and the user's open questions answered |
| **S2** | CLS build (6 sub-stages, book §15.3) | fix-se | S1 | `closettwin.cls` v0.1 → v1.0, `fix/CHANGELOG.md`, a test page per sub-stage | Each sub-stage compiles; master-se views the test page image |
| S2.1 | Skeleton on `book` (oneside), geometry (text width 15.0 cm), fonts by path, `\tracinglostchars=3`, language switching | fix-se | S1 | v0.1 | Only Playfair + Rubik (+ LM Math if Q-C) in `pdffonts` |
| S2.2 | BiDi rules, `hebrewpage`, `\pct`, `\usd`, `\ils` | fix-se | S2.1 | v0.2 | The book's ch. 14 check page passes (Hebrew + ClosetTwin + 30% + [1]) |
| S2.3 | Headings, numbering, TOC, lists, chapter opener | fix-se | S2.2 | v0.3 | TOC numbers are correct; each chapter starts a new page |
| S2.4 | Tables, figure and caption style, stat card, pull quote, `\assumption`, TikZ style keys | fix-se (+ the key list from art-se) | S2.3 | v0.4 | The demo page shows every element in the palette |
| S2.5 | Cover, inset banner + footer (shipout hook; page number only), `\frontmatter`/`\mainmatter`, `\FloatBarrier` per chapter | fix-se | S2.4 | v0.5 → **writer-se may start** | No footer on the cover; the banner is on every other page, including the Hebrew page |
| S2.6 | biblatex IEEE, the command list (README section), a full example | fix-se | S2.5 | v1.0 | The example builds clean with the 4 commands |
| **S3** | QA skills | fix-se (content from qa-se's criteria) | S1 (drafts), S2.5 (for testing) | `.claude/skills/qa-{super,BiDi,table,code,img,typeset,infra,cls-version}/SKILL.md` | Each skill run once on the S2.6 example; findings reported |
| **S4** | Project skeleton | master-se (`main.tex`), writer-se (empty `chapters/*.tex`) | S2.5 | `main.tex` + 10 chapter stubs + a Hebrew summary stub | Compiles to a cover, the Hebrew page, the TOC and 10 chapter titles (book Prompt 1) |
| **S5** | Outline with page budget | writer-se | S4 | `writer/outline.md`: sections per chapter + the one claim each section must prove + its sources (book Prompt 2) | master-se approves; it matches PRD §6 |
| **S6** | Figures and data | art-se | S2.4 (TikZ keys), S5 (what each figure shows) | 7 figures (PRD §5.4) in `figures/`, scripts in `python/`, `python/data/assumptions.*` for the financials | art-se checklist (style guide §8); each figure seen inside the build |
| **S7** | Chapters | writer-se | S5, S2.5; figure labels from S6 | `chapters/01…10.tex`, then `chapters/00-exec-summary-he.tex` **last** (it summarizes the rest) | Each chapter compiles; within ±1 page of budget; every claim `\cite`d or `\assumption` |
| **S8** | Build + QA loop (book §19.1) | master-se builds → qa-se detects → fix-se / writer-se / art-se fix | S6, S7 | `qa/reports/NN-*.md`, CLS/skill bumps | qa-super has no blocker or major findings |
| **S9** | Red team on the PDF (book Prompt 9) | qa-se (fresh session) + master-se | S8 | `qa/reports/redteam-pdf.md` | Each finding Adopted/Rejected in the PRD review log, adopted ones fixed |
| **S10** | Submission | master-se | S9 | Final `main.pdf` committed, README (build, packages, skills list), fresh-clone test | Definition of Done (PRD §8) all ✓ and the user's own page-by-page look |

## 3. Dependency graph (critical path in bold)
```
S0 → S1 → **S2.1 → S2.2 → S2.3 → S2.4 → S2.5** → **S4 → S5 → S7** → **S8 → S9 → S10**
                                    S2.4 ──→ S6 (figures) ──→ S7 (labels) / S8
                    S1 ──→ S3 (skill drafts) ──(needs S2.5 to test)──→ S8
                                    S2.5 → S2.6 (bib + docs, parallel to S4/S5)
```

## 4. Hand-offs (what travels between agents)
| From → To | What | Channel |
|---|---|---|
| fix-se → writer-se, art-se | The CLS command list and version after each sub-stage | SendMessage + the CLS README section |
| art-se → fix-se | The TikZ style-key list (style guide §7) | REQUEST |
| art-se → writer-se | The figure label, a suggested caption, and "Assumption" flags | DONE message to master-se → forwarded |
| writer-se → art-se | The numbers a figure must show (from sources or assumptions) | via master-se |
| qa-se → master-se | Findings marked recurring or one-off, with their owner | `qa/reports/` + REPORT |
| master-se → owner | One task per finding | SendMessage |

## 5. Risks to the plan
| Risk | Mitigation |
|---|---|
| MiKTeX hangs on a missing package | `--disable-installer` in every build; missing packages go to master-se for `mpm` |
| Content runs short of 25 pages | Budget checked at S5 (outline) and after every chapter; ±1 tolerance per chapter |
| Hebrew page regressions | qa-BiDi checks the rendered page image, never text extraction |
| Writers hand-patch layout | The T3 grep for forbidden commands runs in every QA round |
| A source turns out wrong | qa-se re-opens every DOI/URL in S8 (R5) |

## Exception E-1 (2026-11-19): master-se edits the financial model
Approved by master-se under the rule "if they conflict, master-se approves the exception in writing". art-se is offline and the usage limit cut task T20.3 (IL-M1) in half: `assumptions.csv` already had the Israel rows, but `python/model.py` crashed on the old IDs. master-se edited `python/model.py` and one row of `python/data/assumptions.csv` (D27 text) and regenerated `python/data/*_out.csv`. Ownership returns to art-se on its next session; art-se must review the diff (`git show` of this commit) and re-run `python/fig_f6_retailer_economics.py` and F5.
