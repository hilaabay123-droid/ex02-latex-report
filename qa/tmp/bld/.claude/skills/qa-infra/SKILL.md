---
name: qa-infra
description: Detector (report-only) for repository structure and reproducibility: required files, portability, fonts provenance, no ID numbers, bibliography mechanics, skills present with versions, git contents, fresh-clone build. Use before submission or when asked to check the repo.
version: 1.0
---

# qa-infra

Checks required files, ownership folders, paths, fonts provenance, bibliography mechanics, the no-ID rule, repository contents and reproducibility from a fresh clone.

**Report-only.** This skill finds and reports. It never edits a chapter, figure, script, bib or the CLS, never fixes, never commits.
A fix goes to the owner named in the finding; a recurring problem goes to fix-se (iron rule, root `CLAUDE.md`).
If `main.pdf`, `main.log` or `main.aux` is older than the newest `.tex`/`.cls`/`.bib`, stop with `BLOCKED: stale or missing build`.
Criteria IDs refer to `qa/acceptance-criteria.md`; full step detail is in `qa/skill-specs.md`. Helper scripts live in `qa/scripts/` and run as `python -I qa/scripts/<name>.py`.
A criterion that could not be checked is `skipped` with a reason, never silently passed.
Save to `qa/reports/NN-<topic>.md` (NN = next free number). Reply to master-se: `REPORT <scope>` + path + counts by severity.

## When to use
First step of `qa-super`; again before every submission (final mode).

## Inputs
The git tree and history, `references.bib`, `main.bcf`, `main.blg`, `fonts/`, `.claude/skills/`, `README.md`, `.gitignore`, `PRD.md`.

## Procedure
1. Required files (FS1, S4): `ls main.tex closettwin.cls PRD.md PLAN.md TODO.md README.md references.bib`; `chapters/` has the ten `NN-*.tex` plus the Hebrew page; `figures python fonts` exist.
2. Structure (FS2, FS3, T5): `grep -n "\\input" main.tex` lists each chapter; no `writer/ art/ qa/ fix/` path in `main.tex` or chapters; chapters contain no `\documentclass`, `\usepackage`, `\begin{document}`.
3. Portability (FS4): grep for `C:\`, `\Users`, `/Users/` in `.tex .cls .py .bib`: zero.
4. Fonts (FS5, R-07): `fonts/` has Playfair Display, Rubik, JetBrains Mono, their OFL texts and `SOURCES.md`; `sha256sum` equals the hashes in `SOURCES.md`; the CLS loads by relative path.
5. No ID numbers (C6): `python -I qa/scripts/id_scan.py` over files, `git log --all -p` and `pdftotext main.pdf -`; `pdfinfo` metadata. Any hit is a blocker. Never print the number: first 2 digits and `*******` only. A hit in history is owner master-se.
6. Bibliography (R1-R4, R6, R7, R11): no `undefined citation` or `didn't find a database` in `main.log`/`main.blg`; `python -I qa/scripts/bib_vs_cited.py main.bcf references.bib` (missing keys, never-cited keys, incomplete entries, `@online` without `urldate`, count); `pdftotext main.pdf - | grep -nE "\[[A-Za-z]"` empty; `style=ieee` in the CLS.
7. Links (R5, mechanical half): `curl -sIL -o /dev/null -w "%{http_code}"` on each doi/url (200/301/302 pass). Resolving is necessary, not sufficient: claim trace stays with qa-super.
8. Skills (S2, S3): every `.claude/skills/*/SKILL.md` has `name`, `description`, `version`; README lists skills, build commands and the MiKTeX package list.
9. Repo contents (FS7, S1): `git ls-files` has main.pdf, bib, cls, tex, figures, python, fonts, skills; `.gitignore` excludes aux/log/bbl/blg/bcf/toc/out/lof/lot and `qa/tmp/` but not `main.pdf`.
10. Reproducibility (FS6, S9): `git clone . qa/tmp/clone`, run the four build commands there, compare page count, `pdftotext` per page, `pdffonts`, warning counts with the original. Byte identity is not required.
11. Process (S5, S6): `prompts/` holds the prompt files; CHANGELOG rows match recurring problems in QA reports.

## Outputs
Finding blocks plus a file checklist (`path | required | present`), a bib table (`key | cited | complete | urldate | link status`) and the reproducibility table (`item | original | clone | equal`).

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

Recurring-prone: FS3, FS4, R2/R3, T5. A malformed bib entry: recurring = no, owner writer-se. A wrong biblatex option or missing `.gitignore` rule: recurring, owner fix-se / master-se by the ownership table.

## Success check
FS1-FS8, S1-S6, S9, C6, R1-R4, R6, R7, R11, T5 each pass, fail or are skipped with reason; no ID digits appear anywhere in the report.
