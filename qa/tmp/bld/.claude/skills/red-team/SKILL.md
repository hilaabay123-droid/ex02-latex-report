---
name: red-team
description: Adversarial review of the whole plan before submission, from the course book Prompt 9: attack the plan as a sceptical investor, the lecturer's rubric, and a hostile fact-checker, and list what breaks. Report-only. Use before submission or after a major content change.
version: 1.0
---

# red-team

A structured attack on the document, after the course book's red-team prompt (ch. 19, Prompt 9). Report-only: it finds, it does not fix.

## When to use
Before the final submission; after chapters 1-10 are complete; whenever a number or claim in the plan changes.

## Inputs
`main.pdf`, `chapters/*.tex`, `PRD.md`, `references.bib`, `python/model.py` outputs, `ref/BIU26-27-A-ex02-pdf-via-LaTex-print.pdf` (the assignment), `qa/acceptance-criteria.md`.

## Procedure
Adopt each role in turn and write what that reader would object to, with the page and exact text:
1. **Assignment grader**: go through every requirement of the assignment and the PRD one by one; mark each present / weak / missing, with the page.
2. **Sceptical investor**: attack the market size, the unit economics, the funding ask, the break-even year, the competitor comparison and the risks. Which number would you ask to see the source for? Which assumption carries the whole result? What happens if it is 30% worse?
3. **Hostile fact-checker**: take 10 statistics at random; open each cited source; does it say that number on that page? Does a legal or regulatory statement match the official text? Any claim a competitor could call false?
4. **Consistency**: the same number must be identical in text, tables, captions, figures, summary and Hebrew page; the Hebrew summary must say what the English chapters say.
5. **Reader**: where does a non-expert get lost; which sentence is empty marketing; which section has no argument?
6. **Process and integrity**: any ID number, any invented source, any figure not reproducible from `python/`.

## Outputs
`qa/reports/NN-redteam.md`: per role, findings in the common block format (page, exact text, rule/expectation broken, severity, owner), a ranked top-10 "what would sink this plan", and a table of assignment requirements with status. Reply `REPORT redteam` to master-se.

## Success check
Every assignment requirement has a status; at least 10 claims were traced to their sources with the result recorded; every finding names page and exact text; nothing in the plan was edited.
