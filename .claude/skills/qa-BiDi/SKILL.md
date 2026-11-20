---
name: qa-BiDi
description: Detector (report-only) for Hebrew/English direction: reversed runs, bullets/numbers on the wrong side, punctuation and parentheses at run boundaries, missing glyphs, wrong fonts on the Hebrew page. Use after a build, or when asked to check Hebrew/RTL.
version: 1.0
---

# qa-BiDi

Proves the Hebrew executive-summary page is correct BiDi and that no direction or glyph error exists elsewhere.

**Report-only.** This skill finds and reports. It never edits a chapter, figure, script, bib or the CLS, never fixes, never commits.
A fix goes to the owner named in the finding; a recurring problem goes to fix-se (iron rule, root `CLAUDE.md`).
If `main.pdf`, `main.log` or `main.aux` is older than the newest `.tex`/`.cls`/`.bib`, stop with `BLOCKED: stale or missing build`.
Criteria IDs refer to `qa/acceptance-criteria.md`; full step detail is in `qa/skill-specs.md`. Helper scripts live in `qa/scripts/` and run as `python -I qa/scripts/<name>.py`.
A criterion that could not be checked is `skipped` with a reason, never silently passed.
Save to `qa/reports/NN-<topic>.md` (NN = next free number). Reply to master-se: `REPORT <scope>` + path + counts by severity.

## When to use
After every full build that touches the Hebrew page, the CLS, or any text with Hebrew; always as part of `qa-super`.

## Inputs
`main.pdf`, `main.log`, `main.toc`, the Hebrew page source (`chapters/00-*.tex`), `qa/scripts/bidi_runs.txt` (required Latin runs and numbers).

## Procedure
1. Find Hebrew pages: `python -I qa/scripts/hebrew_pages.py main.pdf`. Expect exactly one, in the front matter (B1, B8). Hebrew letters elsewhere = finding.
2. Missing glyphs: `grep -c "Missing character" main.log` must be 0; also `grep -n "^!" main.log` (B9).
3. Corpus: `pdftotext -f N -l N -bbox main.pdf qa/tmp/heb.html`, then `python -I qa/scripts/bidi_bbox_check.py qa/tmp/heb.html qa/scripts/bidi_runs.txt`. It finds each required run as written, fails if its reverse is present (`niwTtesolC`, `6202`), checks reading-order `xMin`, prints words in RTL line order (B11: at least 6 Latin runs, 5 numbers with units, a parenthesis, a sentence end next to a Latin run).
4. Look: `pdftoppm -r 150 -f N -l N -png main.pdf qa/tmp/heb` and read the PNG: first word of each paragraph at the right edge, bullets/numbers on the right, heading RTL in Rubik, punctuation and parentheses on the correct side, banner/footer not colliding (B2-B7, B10). Write "verified by eye"; pdftotext can order Hebrew wrongly and is not proof.
5. English body is LTR: `python -I qa/scripts/hebrew_pages.py --rtl-paragraph-check` flags non-Hebrew pages with a right-aligned block (C4, D2).
6. Fonts: `pdffonts -f N -l N main.pdf` lists Rubik only on the Hebrew page, no Playfair for Hebrew (B6, D5).

## Outputs
Finding blocks plus a corpus table `run | required | found as written | reverse found | read-order ok` and the list of Latin runs seen on the Hebrew page, one verdict each.

## Finding format (one block per finding)
```
### F-<skill>-<nn>  [blocker|major|minor]  <criterion ID(s)>
- Where:     <file>:<line> | PDF page <printed page> (<pdf index>)
- What:      <one sentence: the rule broken>
- Evidence:  <exact text / log line / command + output>
- Recurring: yes|no  (yes = same criterion in 2+ places, a CLS-class cause, or it reappeared; list EVERY place; owner fix-se)
- Owner:     writer-se | art-se | fix-se | master-se
- Status:    open
```

Recurring-prone: B2-B5, B7, B9 (direction/spacing/glyph classes belong to the CLS or `hebrewpage`): recurring = yes, owner fix-se, name the construct and macro (`hebrewpage`, `\pct`, `\usd`, `\range`). A wrong Hebrew word or typo: recurring = no, owner writer-se.

## Success check
Criteria B1-B11, C4, D2, D3, D5 each pass, fail or are skipped with a reason; one summary line `checked n, pass p, fail f, skipped s`.
