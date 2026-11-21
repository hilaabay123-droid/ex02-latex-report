# Incident 06: I-6: 6.03% in math font, 4.52% in Rubik

Date: 2026-11-20. Found by: the user in draft v1 (prompt 06). Handled by: fix-se. Skill: incident v1.0.

## What happened
Page 25 (8.3): `$\rho=\derived{6.03\%}$` printed 6.03% in Latin Modern Math and `\derived{4.52\%}` in Rubik.
Where: ch.8 section 8.3 (and `$r=24.4\%$`, `$c=\$6.80$` in 8.1).

## Root cause
Digits inside `$...$` are math characters (Latin Modern Math). The tag macros did not isolate their argument from math mode, and inline math digits had no rule.

## Why no detector caught it
No check compared the font of numbers in running text; pdffonts per document hides it because both fonts are used elsewhere. No detector had a criterion for this, and the visual look at every page (book 19.5 item 5) was postponed to the next session.

## Fix (in the CLS or a skill, not in the text)
closettwin v0.20: (1) `\sourced/\derived/\assumed` set their argument with `\text` when called in math; (2) digits in INLINE math are active math characters that set themselves in the text font (displayed equations stay Latin Modern Math). Verified with `pdffonts` on a test page and by eye; subscripts such as `x_1` work.

## New check
qa-typeset v1.1: per-span font scan (`page.get_text('dict')`): in running text every digit span must be Rubik; digits in Latin Modern Math are allowed only on pages with an `eq:` label. Writer rule: no digits in `$...$` in prose.

## Status
Fixed in closettwin v0.20 (see `fix/CHANGELOG.md`). Re-check by qa-super after the next build.
