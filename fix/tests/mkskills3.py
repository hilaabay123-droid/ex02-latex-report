import pathlib
R = pathlib.Path(r"C:\biu\02\.claude\skills")


def w(name, desc, body):
    (R / name / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {desc}\nversion: 1.0\n---\n\n# {name}\n\n" + body.strip() + "\n",
        encoding="utf8")


w("qa-fixer",
  "Fixer: takes findings from a QA report and fixes them at the right level. A repeating problem is fixed in the CLS (version bump + CHANGELOG); a single-place problem is fixed in that sentence only. Recompiles, re-runs the detector, records before and after. Use when master-se sends qa findings to fix-se.",
  r"""
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
""")

w("writer",
  "Production skill for chapter writing: continuous professional prose, every claim cited from references.bib, every money figure from python/model.py, assumptions labelled, honest funding ask and break-even year. Use when writing or revising chapters/*.tex.",
  r"""
Rules for writing the business-plan chapters (writer-se, and qa-se for chapters 6-10 in the speed session).

## When to use
Writing or revising any `chapters/NN-*.tex` or the Hebrew summary.

## Inputs
`PRD.md` (page budget, required items), `writer/outline.md`, `references.bib`, `python/model.py` and `python/data/*.csv` outputs, `docs/cls-commands.md`, `figures/` labels.

## Procedure
1. Read the chapter's outline and page budget (within one page of it; conclusion exactly one page).
2. Write **continuous prose** in English: paragraphs with an argument, not bullet lists. Short lists only where a list is the natural form.
3. **Every factual claim** has `\cite{key}` with a key that exists in `references.bib`. No key invented. A claim with no source is rewritten as an assumption or removed.
4. **Every money figure and percentage** comes from `python/model.py` output or a cited source; copy the number, never invent or round differently. Tag it with `\sourced{}`, `\derived{}` or `\assumed{}`; label assumptions with `\assumption{}`.
5. Use CLS macros for formatting: `\pct \usd \ils \range`, `statcard`, `pullquote`, `insightbox`, plain `table`/`figure` (no placement argument). **Never** `\vspace`, `\newpage`, manual fonts or colours; if something is missing in the CLS, ask master-se to pass it to fix-se.
6. Each table and figure has `\caption`, a `\label{tab:...}`/`\label{fig:...}` and a sentence in the text that references it.
7. State the funding ask and the break-even year honestly, exactly as the model says, with the risks that could move them. Never write "break-even within ..." as a slogan.
8. Hebrew page only: Hebrew text inside `hebrewpage`, English terms and numbers as Latin runs (`ClosetTwin`, `AI`, `\pct{30}`); no Hebrew in `references.bib`; non-English sources use an English title and `language = {hebrew}`.
9. No ID numbers anywhere. Team chapter lists roles only.
10. Compile the chapter from the root; fix every warning that came from your text.

## Outputs
`chapters/NN-*.tex` and, when new sources are used, `references.bib` entries (complete author/title/year/venue/DOI-or-URL, `urldate` for online). Reply `DONE` with the page count of the chapter.

## Success check
No uncited claim, no number that differs from the model, no manual formatting command, all labels referenced, chapter within its page budget, build clean.
""")

w("illustrator",
  "Production skill for figures: Python graphs and TikZ diagrams in the project palette, text at least 8 pt, data from the model, captioned, labelled and referenced. Use when creating or changing anything in figures/ or python/.",
  r"""
Rules for art-se when making graphs and diagrams.

## When to use
Creating or changing a Python chart, a TikZ diagram, or the code appendix script.

## Inputs
`python/ct_style.py` (palette, fonts, canvas), `python/model.py` and `python/data/*.csv`, `art/chart-style-guide.md`, PRD 5.3-5.4 (F1-F7), `docs/cls-commands.md` (TikZ keys).

## Procedure
1. One idea per figure; one y-axis; at most 4 series; a title that states the finding.
2. **Python graphs**: import everything visual from `python/ct_style.py`; only the eight palette colours (#111111, #F7F3EE, #A47864, #E8C6C0, #6B4B3D, #D3BBAE, #E3DCD4, #6F6862); Rubik/Playfair text at least 8 pt at print size; fixed canvas equal to the text width (15.0 cm) so it prints 1:1; vector PDF with embedded fonts, no Type 3. Script writes to `figures/`, uses relative paths only, runs with `python python/<name>.py` with no warning on stderr.
3. **Data honesty**: plot only model or sourced values; financial charts say "Assumption"; F5 shows nothing past year 5 and marks the first profitable year and the peak deficit; F6 marks the retailer break-even; F2 axes are two columns of the vendor table; F1 is "not to scale".
4. **TikZ diagrams**: use the `ct ...` keys only, no raw colours, 8 pt text, nodes not overlapping.
5. Series must differ by more than colour: at least 20% luminance gap in grayscale or a direct label; text contrast at least 4.5:1 (3:1 for large text).
6. Each figure: `\caption` below, `\label{fig:...}`, referenced in the text. Do not edit chapters; send writer-se the label and a one-line description.
7. The code appendix script is an ASCII, runnable, line-length-80 file; shown with `\pythonbox{python/<file>.py}`.
8. Render the page at 150 dpi and look before reporting done.

## Outputs
`figures/*.pdf` or `figures/*.tex`, `python/*.py`; reply `DONE` listing file, label and caption text.

## Success check
`qa-img` and `qa-code` would pass: palette, fonts, contrast, 1:1, labels, no stderr, values equal the model.
""")

w("red-team",
  "Adversarial review of the whole plan before submission, from the course book Prompt 9: attack the plan as a sceptical investor, the lecturer's rubric, and a hostile fact-checker, and list what breaks. Report-only. Use before submission or after a major content change.",
  r"""
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
""")

w("incident",
  "Post-mortem for a defect that escaped to a build or submission: root cause, why no detector caught it, the fix in a skill or the CLS, and the new check that would catch it next time. Writes incidents/NN-<slug>.md. Use when a serious problem was found late.",
  r"""
Turns an escaped defect into a permanent improvement of the detectors.

## When to use
A blocker or major problem was found by a human, by master-se, or after a commit, and no detector had reported it; or a fix did not hold.

## Inputs
The defect (page, exact text), the build hash where it first appeared (`git log`, `git bisect` if needed), the QA reports of earlier builds, the detector skills, `fix/CHANGELOG.md`.

## Procedure
1. **Describe** the defect: what, where (page, file:line), when it entered (commit), who noticed it and how.
2. **Root cause**: ask "why" until you reach a cause in a rule, a macro, a skill or a missing check, not a person. Separate the trigger (the text that showed it) from the cause (what allowed it).
3. **Why no detector caught it**: read each detector skill. Was there no criterion, a criterion with no check, a check that ran on the wrong input, a skipped item, or a finding that was reported and not acted on?
4. **Fix**: if the cause is recurring, the fix goes in the CLS or the relevant skill (fix-se: bump version, CHANGELOG row). A one-off content error is fixed by its owner.
5. **New check**: write the exact command, script change or checklist line that detects this class of defect, and say which detector skill gets it (raise that skill's version). Run it on the current build and show it fires on the old build.
6. **Write** `incidents/NN-<slug>.md` (NN = next free number): title, date, impact, timeline, root cause, why not caught, fix, new check, owner, status.

## Outputs
`incidents/NN-<slug>.md`; updated skill or CLS with version bump and a CHANGELOG row; message `DONE incident NN` to master-se.

## Success check
The report names a cause in a rule or skill (not blame); a concrete new check exists and was shown to detect the defect on the old build; the relevant skill's version increased.
""")
