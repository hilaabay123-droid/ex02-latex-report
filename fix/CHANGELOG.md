# CHANGELOG (owner: fix-se)

Format: date | version | finding / reporter | problem | root cause | fix | files.

| Date | Version | Reporter / ID | Problem | Root cause | Fix | Files |
|---|---|---|---|---|---|---|
| 2026-11-18 | closettwin v0.1 | master-se T2.1 (S2.1) | New class needed | n/a | Skeleton on `book` oneside; geometry 3.0/3.0/3.6/3.0 cm (text width 15.0 cm); Rubik/Playfair/JetBrains Mono by path (`\ctfontdir`); babel `bidi=basic` + Hebrew; palette (ink, ivory, mocha, powderpink, mochadeep, mochapale, gridgray, mutedgray); unicode-math (LM Math symbols, Rubik letters/digits); microtype, csquotes; `\tracinglostchars=3` | closettwin.cls, fonts/JetBrainsMono-*.ttf, fonts/SOURCES.md |
| 2026-11-18 | closettwin v0.2 | master-se T2.2 (S2.2) | Hebrew rules needed (proved in F1) | Playfair has no Hebrew; `bidi=basic` required; bare % is a comment | `hebrewpage` env (RTL, ragged, own page), `\hebtitle`/`\hebsubtitle` (Rubik Bold), `\ctheadingfont` (Playfair for English, Rubik when language is Hebrew), `\pct`, `\usd`, `\ils` (shekel sign in English, ש״ח in Hebrew) | closettwin.cls |
