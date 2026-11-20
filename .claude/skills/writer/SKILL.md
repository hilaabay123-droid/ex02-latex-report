---
name: writer
description: Production skill for chapter writing: continuous professional prose, every claim cited from references.bib, every money figure from python/model.py, assumptions labelled, honest funding ask and break-even year. Use when writing or revising chapters/*.tex.
version: 1.0
---

# writer

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
