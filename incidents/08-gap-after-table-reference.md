# Incident 08: I-8: 40% empty page before a table

Date: 2026-11-20. Found by: the user in draft v1 (prompt 06). Handled by: fix-se. Skill: incident v1.0.

## What happened
Page 25: about 40% empty after `Table 8.1 lists the inputs of this chapter with their class.`; the table is on the next page.
Where: ch.8 section 8.4: the table is the last element of the chapter.

## Root cause
The float is taller (about 285 pt) than the space left on the page (about 180 pt), and nothing follows it in the chapter that could fill the gap. Floats drift forward by design (v0.18: never at the foot, never above their heading). In this case the gap is the physical result of the table height; v0.20 shortens the table by ragged text columns but it does not fit yet.

## Why no detector caught it
No detector measured white space per page; qa-typeset only flagged pages under 600 characters. No detector had a criterion for this, and the visual look at every page (book 19.5 item 5) was postponed to the next session.

## Fix (in the CLS or a skill, not in the text)
No class change can fill the gap without breaking the v0.18 rules (a `b` placement was removed for the opposite hole). Remedy at content level: REQUEST to writer-se (ch.8): move the sentence and table so text follows the table, or shorten it (column spec of I-4). The detector below makes the gap visible in every build.

## New check
qa-typeset v1.1, step 10: per page the lowest text/figure y; if the gap above the footer is over 25% of the text height and the page is not the last page of a chapter or the conclusion, report it with the next float on the following page as the probable cause.

## Status
Fixed in closettwin v0.20 (see `fix/CHANGELOG.md`). Re-check by qa-super after the next build.
