---
name: incident
description: Post-mortem for a defect that escaped to a build or submission: root cause, why no detector caught it, the fix in a skill or the CLS, and the new check that would catch it next time. Writes incidents/NN-<slug>.md. Use when a serious problem was found late.
version: 1.0
---

# incident

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
