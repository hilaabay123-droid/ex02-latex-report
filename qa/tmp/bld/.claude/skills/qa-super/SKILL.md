---
name: qa-super
description: Orchestrator for the whole QA pass (report-only): runs qa-infra, qa-cls-version, the full build, then qa-BiDi, qa-table, qa-img, qa-code, qa-typeset, adds judgment checks, merges into one report. Supports re-check and final modes. Use for a full QA pass.
version: 1.0
---

# qa-super

The QA manager of all QA skills. Builds, calls the seven detectors in a fixed order, does the checks that need judgment, merges and de-duplicates findings, applies the recurring rule across skills and writes the one report master-se receives.

**Report-only.** This skill finds and reports. It never edits a chapter, figure, script, bib or the CLS, never fixes, never commits.
A fix goes to the owner named in the finding; a recurring problem goes to fix-se (iron rule, root `CLAUDE.md`).
If `main.pdf`, `main.log` or `main.aux` is older than the newest `.tex`/`.cls`/`.bib`, stop with `BLOCKED: stale or missing build`.
Criteria IDs refer to `qa/acceptance-criteria.md`; full step detail is in `qa/skill-specs.md`. Helper scripts live in `qa/scripts/` and run as `python -I qa/scripts/<name>.py`.
A criterion that could not be checked is `skipped` with a reason, never silently passed.
Save to `qa/reports/NN-<topic>.md` (NN = next free number). Reply to master-se: `REPORT <scope>` + path + counts by severity.

## When to use
A full QA pass on a build; a re-check after fixes (`--recheck <report>`); the final sign-off (`--final`).

## Inputs
The working tree at a commit; optional `--scope <criterion IDs | skill names>`; optional `--recheck qa/reports/NN-<topic>.md`; optional `--final`.

## Procedure
1. Record the build id: `git rev-parse --short HEAD`; `git status --porcelain` (non-empty = "dirty tree").
2. Run **qa-infra**, then **qa-cls-version** (they need only sources).
3. Build from the root, saving logs to `qa/tmp/`: `lualatex --disable-installer main`, `biber main`, `lualatex --disable-installer main`, `lualatex --disable-installer main`. A non-zero exit is a finding (BU1, BU2); still finish the source-only skills.
4. Run, in this order: **qa-BiDi, qa-table, qa-img, qa-code, qa-typeset**.
5. Judgment checks no script can do (read chapters and PDF pages): classify every number in the market, finance and risk chapters and captions as sourced/derived/assumed (D14, R13); trace each statistic to its source (claim-trace table: claim, cite key, quoted sentence, page, number found) (R5, R8-R10, R12); competitor claims sourced, table numbers equal text numbers, a graph matches its caption (D15, TB5, I9); editorial look and body language against PRD 5.3 (D16, D2); look at every page at a readable size (19.5 item 5).
6. PRD traps: `grep -rniE "break-even within|breakeven within" chapters/` must be 0 (MC-1); `grep -rniE "BIPA|Illinois" chapters/ references.bib` must be 0 (R12); list macro use of `\ils \usd \pct`; the 53% / 24.4% / 24.52% figures never merged (CT-3).
7. **Merge**: concatenate findings, sort by severity then page, de-duplicate (same criterion and location from two skills = one finding naming both), then apply the recurring rule across the whole set.
8. Write `qa/reports/NN-<topic>.md`, then `SendMessage` master-se `REPORT <scope>` with the path, counts by severity and the blockers inline.
9. **Re-check mode**: delete `main.aux main.bbl main.toc main.bcf`, rebuild, re-run only the owning skills; mark each earlier finding `fixed in build <hash>` or `still open in build <hash>` with a new evidence line. Never mark fixed on someone's word.
10. **Final mode**: build a fresh clone, run everything, check a second build is identical in page count, text per page, fonts and warning counts; write `qa/reports/NN-final.md` with the sign-off section (0 open blocker/major, the six 19.5 items with page lists, blank human sign-off lines).

## Outputs
```
# QA report NN: <topic>          build <hash> (clean|dirty)   date
## Summary      counts blocker/major/minor; skills run; criteria pass/fail/skipped
## Blockers     inline list
## Findings     all blocks, sorted
## Recurring    table: problem | places | owner=fix-se | criterion IDs
## Judgment checks   claim-trace table, number classes, page-by-page look list
## Skipped      criterion, reason
## Re-check     (re-check/final mode only)
```

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

## Success check
All eight skills ran (or are listed as skipped with reason); every criterion is pass, fail or skipped; the report has all sections; recurring findings name fix-se and propose no chapter edit.
