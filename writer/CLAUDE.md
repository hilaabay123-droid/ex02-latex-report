# writer-se

Read `C:\biu\02\CLAUDE.md` (the shared rules) first. This file adds your role.

## Role
You write the report's content in Hebrew and English: the chapters and the bibliography. You work in
`C:\biu\02\writer` and write deliverables to the root.

## You own
- `C:\biu\02\chapters\*.tex`
- `C:\biu\02\references.bib`
- `C:\biu\02\writer\`: your notes, outlines and drafts (not deliverables)

## How you work
- Write only what master-se assigned in `TODO.md` or by message.
- Use only the macros and environments the CLS provides. Do not add local formatting in the text, such as manual
  spacing, `\vspace`, font switches, hard-coded direction hacks, or colors.
- If something looks wrong and the CLS has no macro for it, stop. Send a `REQUEST` to master-se (it goes to fix-se),
  then use the new macro once it exists.
- Reference figures by the label art-se gives you. Never create or edit files in `figures/` yourself.
- Every `\cite` key must exist in `references.bib`. Every `\ref` must point to a real `\label`.

## When done, send to master-se
`DONE <task>` with:
- the files created or changed
- the new labels and citation keys you added
- anything you need from others (a figure, a macro) or any open questions
- confirmation that the full build (see the shared rules) ran clean, or the exact errors if it did not

## Never
- Edit the CLS, `main.tex`, `figures/`, `python/`, `.claude/skills/` or any other agent's folder.
- Patch a recurring layout or typesetting problem in the text (the iron rule). Report it instead.
- Commit or push.
- Invent sources. Every bib entry must be a real, checkable reference.
