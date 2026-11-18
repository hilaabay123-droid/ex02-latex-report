Save this prompt to prompts/03-expert-committee.md, then execute it.

PROJECT: A professional business plan for "ClosetTwin" - a B2B AI virtual
fitting room for fashion e-commerce sites that scans the customer's body to
reduce clothing returns. LuaLaTeX + MiKTeX, built by our 5-agent team.

READ FIRST: ref/ - the assignment requirements (binding), the course book
(Part B, chapters 13-19) and the multi-agent lesson.

FIXED DECISIONS (ours - do not change):
- Body: English, LTR, at least 25 pages of content (front matter not counted).
- One Hebrew executive-summary page (RTL, with English brand names and
  numbers inside Hebrew text) to demonstrate perfect BiDi.
- Style: fashion-magazine inspiration (Vogue) - clean, airy, not noisy,
  with touches of trendy fashion colors.
- Fonts (stored in fonts/, OFL, so the build is reproducible):
  Playfair Display = English headings; Rubik = English body AND all
  Hebrew text, including Hebrew headings. No other fonts.
- Approved palette: ink #111111, ivory #F7F3EE, mocha #A47864, powder pink #E8C6C0.
- Page budget: Intro & Problem 3, Market TAM/SAM/SOM 4, Competition 3,
  Product & Technology 4, Business Model & Pricing 3, Go-to-Market 2,
  Operations/Team/Roadmap 2, Financial Plan 3 (with a formula), Risks 2,
  Conclusion 1, References IEEE 1-2.
- Excellence: banner + footer, at least one figure, table and formula;
  graphs from Python, diagrams in TikZ, NO internet images.
- Only real, verifiable sources. Financial figures are labeled as assumptions.

TASK:
1. Form an expert committee of 5: LaTeX/CLS architect, fashion editorial
   designer, business-plan analyst, data-viz designer, QA engineer.
   Assign research to the peers now so no one waits:
   writer-se -> 12+ real, verifiable sources on return rates, virtual try-on,
     body scanning (DOI/link for each) -> draft references.bib (IEEE);
   art-se -> chart style guide matching the palette + palette swatch PNG
     in docs/screenshots/;
   fix-se -> CLS feasibility: fonts, Hebrew RTL page, banner, footer,
     biblatex IEEE;
   qa-se -> measurable acceptance criteria per QA family (course book ch.19).
2. Merge into PRD.md: vision, audience, design system, page budget,
   requirements table (ID | requirement | target | how verified), Definition of Done.
3. Red team: send PRD.md to every peer. For each finding write
   Adopted/Rejected + reason in a "Review log" section. Bump the version.
4. Write PLAN.md (stages, owner, dependencies) and TODO.md (atomic tasks,
   owner, check).
5. Ask me only what is still open - in ONE round. Commit and push.
Do NOT write LaTeX yet.
