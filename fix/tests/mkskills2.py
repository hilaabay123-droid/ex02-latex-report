import pathlib, importlib.util
spec = importlib.util.spec_from_file_location("m1", r"C:\biu\02\fix\tests\mkskills1.py")
# reuse helpers without re-running skills 1: copy the constants
src = open(r"C:\biu\02\fix\tests\mkskills1.py", encoding="utf8").read().split("\nw(\"qa-BiDi\"")[0]
exec(src)

w("qa-typeset",
  "Detector (report-only) for compilation warnings and pagination: overfull/underfull boxes over 1 pt, undefined refs, page count and budget, orphan headings, short pages, margins, banner/footer. Use after a build.",
  r"""
Turns the TeX log and the rendered pages into a check of overfull/underfull boxes, page count, page budget and the layout rules.
""" + RULE + r"""
## When to use
After every full build; part of `qa-super`.

## Inputs
`main.log`, `main.blg`, `main.toc`, `main.aux`, `main.pdf`.

## Procedure
1. Overfull (BU5, C5, L9): `python -I qa/scripts/overfull.py main.log`: every `Overfull \hbox/\vbox` with page and source line. Fail if more than 1.0 pt. Print the full table.
2. Underfull (BU6): count and list badness 10000 lines in body text with pages.
3. Other warnings (BU2-BU4, BU7, BU8): `grep -c "^!" main.log`; `grep -c "undefined" main.log`; `grep -c "Missing character" main.log`; `grep -i "rerun" main.log` empty on the last pass; `grep -E "ERROR|WARN" main.blg`; `grep -n "Float too large\|too many unprocessed floats" main.log`.
4. Page count and budget (D1, D17, BU9): `pdfinfo main.pdf | grep Pages`; `python -I qa/scripts/page_stats.py` prints per chapter first page, pages and the budget check (conclusion exactly 1 page, content total at least 25 pages, chapters 1-10 only).
5. Per-page statistics (L2, L4, L5): `python -I qa/scripts/page_stats.py --pages`: flags a page under 600 characters that is not a chapter end or the conclusion, a last line that is a heading (orphan heading), a one-word last line.
6. Look at every page (L1, L3, L6-L9, 19.5 item 5): `pdftoppm -r 80 -png main.pdf qa/tmp/p`, read each PNG, record the page list: new page per chapter, TOC complete, no float or box split, banner and footer on every page except the cover and openers, page numbers equal the TOC, text inside the margins.
7. Airy rule (D16, I13): `python -I qa/scripts/bbox_margin.py --margins`; at most one figure and one table per page.
8. Cover (C2, C3, C5): page 1 has no number or footer; roman front matter, arabic from chapter 1.

## Outputs
Finding blocks plus three tables: overfull/underfull list (`kind | amount | page | source line`), page budget (`chapter | budget | actual | range | verdict`), page stats (`page | chars | last line | flags`).
""" + FMT + r"""
Recurring-prone: BU5, L1, L2, L3, L4, L7, L9. Two overfull boxes of one kind (long URL, wide table) are ONE recurring finding listing all lines, owner fix-se. A short page from one chapter's volume: recurring = no, owner writer-se, unless it appears in 2 or more chapters.

## Success check
BU2-BU10, L1-L9, D1, D17, C2, C3, C5 each pass, fail or are skipped with reason; page budget table printed; the overfull table is complete, not only failures.
""")

w("qa-infra",
  "Detector (report-only) for repository structure and reproducibility: required files, portability, fonts provenance, no ID numbers, bibliography mechanics, skills present with versions, git contents, fresh-clone build. Use before submission or when asked to check the repo.",
  r"""
Checks required files, ownership folders, paths, fonts provenance, bibliography mechanics, the no-ID rule, repository contents and reproducibility from a fresh clone.
""" + RULE + r"""
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
""" + FMT + r"""
Recurring-prone: FS3, FS4, R2/R3, T5. A malformed bib entry: recurring = no, owner writer-se. A wrong biblatex option or missing `.gitignore` rule: recurring, owner fix-se / master-se by the ownership table.

## Success check
FS1-FS8, S1-S6, S9, C6, R1-R4, R6, R7, R11, T5 each pass, fail or are skipped with reason; no ID digits appear anywhere in the report.
""")

w("qa-cls-version",
  "Detector (report-only) for template version discipline: the class in use, its version equal in cls, build log and CHANGELOG, every CLS/skill change logged, no manual formatting in chapters. Use after any CLS or skill change and in qa-super.",
  r"""
Checks that the CLS is the one `main.tex` uses, that its version is the logged version, that every CLS or skill change has a CHANGELOG row, and that chapters hold no manual formatting the CLS should own (iron rule).
""" + RULE + r"""
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
""" + FMT + r"""
Every T3 hit is recurring = yes by definition (the CLS lacks a macro): name the missing capability, owner fix-se, and say "do not patch the text". T2/T6 mismatches are recurring = no for that release, owner fix-se.

## Success check
T1-T6, S6, R-05, R-19 each pass, fail or are skipped with reason; the version triple table is complete.
""")

w("qa-super",
  "Orchestrator for the whole QA pass (report-only): runs qa-infra, qa-cls-version, the full build, then qa-BiDi, qa-table, qa-img, qa-code, qa-typeset, adds judgment checks, merges into one report. Supports re-check and final modes. Use for a full QA pass.",
  r"""
The QA manager of all QA skills. Builds, calls the seven detectors in a fixed order, does the checks that need judgment, merges and de-duplicates findings, applies the recurring rule across skills and writes the one report master-se receives.
""" + RULE + r"""
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
""" + FMT + r"""
## Success check
All eight skills ran (or are listed as skipped with reason); every criterion is pass, fail or skipped; the report has all sections; recurring findings name fix-se and propose no chapter edit.
""")
