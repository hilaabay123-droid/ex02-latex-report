---
name: qa-code
description: Detector (report-only) for the code appendix and Python scripts: one pythonbox, margin, LTR, code equals the real file, JetBrains Mono only there, every script runs clean and reproduces its figure. Use after a build or when asked to check code.
version: 1.0
---

# qa-code

Checks the one code box (K1-K4) and that every Python script runs and reproduces its figure (K5).

**Report-only.** This skill finds and reports. It never edits a chapter, figure, script, bib or the CLS, never fixes, never commits.
A fix goes to the owner named in the finding; a recurring problem goes to fix-se (iron rule, root `CLAUDE.md`).
If `main.pdf`, `main.log` or `main.aux` is older than the newest `.tex`/`.cls`/`.bib`, stop with `BLOCKED: stale or missing build`.
Criteria IDs refer to `qa/acceptance-criteria.md`; full step detail is in `qa/skill-specs.md`. Helper scripts live in `qa/scripts/` and run as `python -I qa/scripts/<name>.py`.
A criterion that could not be checked is `skipped` with a reason, never silently passed.
Save to `qa/reports/NN-<topic>.md` (NN = next free number). Reply to master-se: `REPORT <scope>` + path + counts by severity.

## When to use
After a build with the code appendix, or after any change to `python/*.py` or `pythonbox`; part of `qa-super`.

## Inputs
`chapters/app*.tex`, `python/*.py`, `figures/`, `main.pdf`, `main.log`, `main.aux`.

## Procedure
1. `grep -rn "pythonbox" chapters/ main.tex`: exactly one use, in the appendix, taking a path to a `python/*.py` file; no pasted code in chapters (K1, K4).
2. Find the page from the `app:` label in `main.aux`; render at 150 dpi; look: ivory fill, hairline, line numbers, LTR, indentation kept, nothing past the right margin (K1, K2).
3. Margin by coordinates: `pdftotext -f p -l p -bbox main.pdf qa/tmp/code.html`; `python -I qa/scripts/bbox_margin.py` fails if `xMax` is past page width minus 3.0 cm.
4. Source equality: `pdftotext -layout -f p -l p main.pdf -` against the file; `python -I qa/scripts/code_diff.py <pdf-text> python/<file>.py` (ignores line numbers); any differing line is a finding (K4).
5. Fonts: `python -I qa/scripts/fonts_by_page.py main.pdf`: JetBrains Mono only on appendix pages; no mono font in `pdffonts figures/*.pdf` (K3, D4).
6. Run every script from the root with `python python/<name>.py`: exit 0, output file in `figures/` newer than the run start, no `findfont`/`Glyph ... missing`/`Warning` on stderr (K5, I8). Record stderr.
7. The figure made by the script named in the box is the figure the appendix claims.
8. No `C:\` path or secret in any script (FS4).

## Outputs
Finding blocks plus a script table: `script | exit | stderr lines | output file | in figures/ | used by figure`.

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

Recurring-prone: K3, K1/K2 (the `pythonbox` macro: owner fix-se). The same fallback-glyph warning in two scripts is recurring: owner art-se for `ct_style.py`. A wrong constant in one script: recurring = no, owner art-se.

## Success check
K1-K5, I8, FS4 each pass, fail or are skipped with a reason; the script table lists every file in `python/`.
