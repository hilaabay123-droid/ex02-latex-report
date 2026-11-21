# Incident 01: I-1: literal "--" in the stat card

Date: 2026-11-20. Found by: the user in draft v1 (prompt 06). Handled by: fix-se. Skill: incident v1.0.

## What happened
Chapter 1 stat card read `$685 B--$890 B` instead of `$685 B–$890 B`.
Where: p.1 of ch.1 (pdf page 7), `\statcard{\$685\,B--\$890\,B}{...}`; reported by the user in draft v1.

## Root cause
The `--` to en-dash conversion is a TeX ligature of the font (`Ligatures=TeX`). `\ctheadfont` (Playfair, used for the big number of `\statcard`) and `\ctmediumfont` were declared without it, so every `--` set in them stays two hyphens. Class-wide cause, not one card.

## Why no detector caught it
qa-typeset and qa-img had no check of the rendered text for `--`; the text source was correct TeX, so a source grep would not have flagged it either. No detector had a criterion for this, and the visual look at every page (book 19.5 item 5) was postponed to the next session.

## Fix (in the CLS or a skill, not in the text)
closettwin v0.20: `Ligatures=TeX` on `\ctheadfont` and `\ctmediumfont`; the code font switches ligatures off (`RawFeature={-tlig;-liga;-calt}`) so code stays literal. Verified: stat card now shows an en dash; `pdftotext` of the whole PDF has no `--`.

## New check
qa-typeset v1.1, step 9: `pdftotext main.pdf - | grep -n -- '--'` must be empty (outside the code box pages). Also catches `---` and straight quotes.

## Status
Fixed in closettwin v0.20 (see `fix/CHANGELOG.md`). Re-check by qa-super after the next build.
