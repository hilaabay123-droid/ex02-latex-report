---
name: qa-cls-version
description: Detector (report-only) for template version discipline: the class in use, its version equal in cls, build log and CHANGELOG, every CLS/skill change logged, no manual formatting in chapters. Use after any CLS or skill change and in qa-super.
version: 1.0
---

# qa-cls-version

Checks that the CLS is the one `main.tex` uses, that its version is the logged version, that every CLS or skill change has a CHANGELOG row, and that chapters hold no manual formatting the CLS should own (iron rule).

**Report-only.** This skill finds and reports. It never edits a chapter, figure, script, bib or the CLS, never fixes, never commits.
A fix goes to the owner named in the finding; a recurring problem goes to fix-se (iron rule, root `CLAUDE.md`).
If `main.pdf`, `main.log` or `main.aux` is older than the newest `.tex`/`.cls`/`.bib`, stop with `BLOCKED: stale or missing build`.
Criteria IDs refer to `qa/acceptance-criteria.md`; full step detail is in `qa/skill-specs.md`. Helper scripts live in `qa/scripts/` and run as `python -I qa/scripts/<name>.py`.
A criterion that could not be checked is `skipped` with a reason, never silently passed.
Save to `qa/reports/NN-<topic>.md` (NN = next free number). Reply to master-se: `REPORT <scope>` + path + counts by severity.

## When to use
After any change to `closettwin.cls` or a skill; second step of `qa-super`.

## Inputs
`closettwin.cls`, `main.tex`, `main.log`, `fix/CHANGELOG.md`, `.claude/skills/*/SKILL.md`, `chapters/*.tex`, `git log`.

## Procedure
1. Class in use (T1): `grep -n "documentclass" main.tex` is `\documentclass{closettwin}`; the file exists.
2. Version (T2): `grep -n "ProvidesClass" closettwin.cls`; `grep -i "closettwin" main.log` shows the same string; the newest CHANGELOG row has the same `vX.Y` and a date not older than the class date. Any mismatch is a finding.
3. Change discipline (T6, S6): `git log --format="%h %ad %s" --date=short -- closettwin.cls`: each commit after the first has a CHANGELOG row of the same date, and the diff bumps `ProvidesClass`. For each skill, `git log -- .claude/skills/<name>/SKILL.md` against its `version:`.
4. No manual formatting in chapters (T3): `grep -nE "\\(vspace|hspace|newpage|clearpage|pagebreak|fontsize|selectfont|setmainfont|setlength|raggedright|centering|bfseries|itshape)\b" chapters/*.tex`, plus `\textcolor{`, `\color{`, `\definecolor` in chapters. Allowed: `\needspace` and the CLS macros (`\pct \usd \ils \range \sourced \derived \assumed statcard pullquote insightbox pythonbox hebrewpage`). Report each hit with file:line.
5. Recurrence (S6): read earlier reports in `qa/reports/`; for each recurring finding a CHANGELOG row must exist and its version be in the current CLS; if it reappears, report "fix did not hold" (third time: escalate to master-se).
6. Hand patches: `git log -p -- chapters/` for added `\vspace \hspace \newpage \clearpage` lines.

## Outputs
Finding blocks plus the version triple table (`source | string | date | match`: class, build log, CHANGELOG, each skill) and the manual-formatting hit list (`file:line | command | allowed?`).

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

Every T3 hit is recurring = yes by definition (the CLS lacks a macro): name the missing capability, owner fix-se, and say "do not patch the text". T2/T6 mismatches are recurring = no for that release, owner fix-se.

## Success check
T1-T6, S6, R-05, R-19 each pass, fail or are skipped with reason; the version triple table is complete.
