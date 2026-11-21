---
name: qa-fixer
description: Fixer: takes findings from a QA report and fixes them at the right level. A repeating problem is fixed in the CLS (version bump + CHANGELOG); a single-place problem is fixed in that sentence only. Recompiles, re-runs the detector, records before and after. Use when master-se sends qa findings to fix-se.
version: 1.0
---

# qa-fixer

Turns detector findings into fixes without breaking the iron rule: fix the cause, not the symptom.

## When to use
After `qa-super` (or a single detector) produced `qa/reports/NN-*.md` and master-se assigned findings to fix-se. Not for detecting: detectors are report-only.

## Inputs
The report path and the finding IDs; `closettwin.cls`, `.claude/skills/`, `fix/CHANGELOG.md`; the detector skill that raised each finding.

## Procedure
1. **Classify** each finding by its `Recurring` field and by your own check: does the same cause occur in 2 or more places, or is it a class (spacing, direction, fonts, captions, tables, numbering, citations, floats)?
2. **Repeating** (CLS or skill problem): find the root cause with a minimal test in `fix/tests/`; fix it in `closettwin.cls` or in the skill; **bump the version** (`\ProvidesClass{...}[YYYY/MM/DD vX.Y ...]` or the skill's `version:`); add a row to `fix/CHANGELOG.md` (date, version, finding ID, problem, root cause, fix, files, reporter). If the text must adopt a new macro, send master-se the exact change for writer-se or art-se; do not edit their files.
3. **Single place** (one wrong number, one typo): do not touch the CLS. If the file is not yours, send the owner the path, line and exact change; fix-se edits that sentence only when master-se explicitly grants it for that one finding.
4. **Before**: record the evidence line from the report (page, text, rule).
5. **Recompile** with the full four-step build from the root; clean = no errors, no undefined refs, no overfull over 1 pt.
6. **Re-run the same detector** for the finding's criteria. **After**: record the new evidence line. A finding is fixed only on new evidence, never on belief.
7. Check nothing else broke: run `qa-typeset` on the whole build and compare page count and warnings with before.

## Outputs
- Changed CLS/skill files, with version bumped.
- `fix/CHANGELOG.md` row per recurring fix.
- A table in the reply: `finding | repeating? | fix level | version | before | after | status`.
- `DONE <finding IDs>` to master-se: root cause, new version, CHANGELOG row, usage change for other agents, build result.

## Success check
Every assigned finding is `fixed in build <hash>` with after-evidence, or `still open` with the reason; no chapter was edited for a recurring problem; the CLS/skill version moved forward exactly when it changed; the build is clean.

## Never
Edit chapters, figures, bib or `main.tex` for a recurring problem; change the CLS without bump and log; commit or push.
