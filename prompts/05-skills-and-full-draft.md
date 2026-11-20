Save this prompt to prompts/05-skills-and-full-draft.md, then execute it.
All 5 agents are online. Work autonomously - stop and ask me ONLY at the
end, or if a decision changes the content of the business plan.

PART 0 - Status (5 lines): check git log and qa/reports/. Did yesterday's
changes land (cover label "BUSINESS PLAN · 2026", IEEE "(in Hebrew)" rule,
Hebrew test fixture removed, B4 findings fixed)? Finish anything missing.

PART 1 - Skills (fix-se writes them, you review). Create
.claude/skills/<name>/SKILL.md (name, description, when to use, procedure,
inputs, outputs, success check), based on course book ch.14 and ch.19:
 Detectors - REPORT ONLY (page, exact text, rule broken), save to qa/reports/:
  qa-super (runs in order: qa-infra -> qa-cls-version -> build -> qa-BiDi,
  qa-table, qa-img, qa-code, qa-typeset -> one merged report),
  qa-BiDi, qa-table, qa-code, qa-img, qa-typeset, qa-infra, qa-cls-version.
 Fixer: qa-fixer - repeating issue -> fix in the CLS (bump version +
  CHANGELOG); single place -> fix that sentence only. Recompile, re-run
  the detector, record before/after.
 Production: writer, illustrator, red-team (course book Prompt 9),
  incident (root cause, why no detector caught it, fix in skill/CLS,
  new check -> incidents/NN-<slug>.md).

PART 2 - Full draft, in parallel:
 writer-se: write every chapter per writer/outline.md and PRD.md page
  budget - chapters/*.tex in English, Hebrew executive-summary page in
  Hebrew. Continuous professional prose, not bullet lists. Every factual
  claim has \cite{} from references.bib only. All money figures come
  from python/model.py outputs - never invent numbers; label assumptions.
  Explain the funding ask and the year of break-even honestly.
 art-se: all graphs from python/ (palette from python/ct_style.py) to
  figures/, all diagrams in TikZ. Every figure has a caption, a \label,
  and is referenced in the text. Include the code appendix (one chart's
  Python code in the code box).
 fix-se: assemble main.tex (cover, Hebrew summary, TOC, lists, chapters,
  references, appendix) and keep the build green.
 You: review each chapter as it lands; max 2 review rounds per chapter.

PART 3 - First QA pass: qa-se runs qa-super on the full PDF; fix-se runs
 qa-fixer on the findings; one re-check.

FINISH: commit and push. Then show me: the PDF path, total page count and
body page count (target >= 25), a list of open findings, and render a
contact sheet of all pages to docs/screenshots/draft-v1-contact.png.

SPEED MODE (overrides the parts above where they conflict):
- Split the writing: writer-se writes chapters 1-5 + the Hebrew summary;
  qa-se writes chapters 6-10 (same writer rules) until PART 3.
- fix-se writes the skills AND assembles main.tex in parallel.
- Max 1 review round per chapter. Fix only real errors, not style.
- PART 3 is postponed to the next session: today only a green build,
  page count and the contact sheet.
