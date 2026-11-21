# Incident 09: I-9: cover without the course number

Date: 2026-11-20. Found by: the user in draft v1 (prompt 06). Handled by: fix-se. Skill: incident v1.0.

## What happened
Cover read `Generative AI for Management` without `(875523402)`.
Where: `main.tex`: `\ctcourse{Generative AI for Management}` (my own entry, written without the number).

## Root cause
A one-off content omission in the cover field, not a class defect: the class prints whatever `\ctcourse` holds. The course number is allowed (only student IDs are forbidden, rule C6).

## Why no detector caught it
No cover-text check existed: qa-typeset checks that the cover has no number or footer, not what it says. No detector had a criterion for this, and the visual look at every page (book 19.5 item 5) was postponed to the next session.

## Fix (in the CLS or a skill, not in the text)
`main.tex`: `\ctcourse{Generative AI for Management (875523402)}`. No CLS change.

## New check
qa-typeset v1.1, step 8: cover text must contain 'Generative AI for Management (875523402)', 'Dr. Yoram Segal' and the doctype label 'BUSINESS PLAN'; and no other 9-digit number.

## Status
Fixed in closettwin v0.20 (see `fix/CHANGELOG.md`). Re-check by qa-super after the next build.
