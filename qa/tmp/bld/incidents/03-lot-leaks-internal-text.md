# Incident 03: I-3: list of tables shows internal text

Date: 2026-11-20. Found by: the user in draft v1 (prompt 06). Handled by: fix-se. Skill: incident v1.0.

## What happened
List of tables entry 6.1 printed `(model output funnel_check_out.csv)`.
Where: Caption of `tab:funnel` in ch.6: `\caption{Pilot and contact funnel, years 1--5 (all values derived ...; model output \texttt{funnel\_check\_out.csv})}`.

## Root cause
Without a short form `\caption` copies the whole caption into the list. Any bracketed remark, file name or model note would reach the list. A recurring risk (every caption), not one table.

## Why no detector caught it
qa-table scanned captions in the chapters, not the rendered list of tables; there was no LOT/LOF scan for underscores, file names or ids. No detector had a criterion for this, and the visual look at every page (book 19.5 item 5) was postponed to the next session.

## Fix (in the CLS or a skill, not in the text)
closettwin v0.20: `\caption` without a short title writes only the text before the first `(` to the lists (`\caption[short]{long}` still wins). The caption itself is unchanged. Verified: LOT entry 6.1 ends at `years 1--5`.

## New check
qa-table v1.1: read `main.lot`/`main.lof`; fail on `_`, `.csv`, `.py`, `\texttt`, `table_check`, `(` in an entry or an entry longer than one line. Also writer rule: no file names in captions (writer skill v1.1). Note: `\texttt` prints in Latin Modern Mono, a font outside the palette; qa-code now flags any mono font outside the appendix.

## Status
Fixed in closettwin v0.20 (see `fix/CHANGELOG.md`). Re-check by qa-super after the next build.
