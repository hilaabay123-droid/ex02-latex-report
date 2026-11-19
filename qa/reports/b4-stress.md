# qa-se report: B4 stress page (closettwin v0.16)

Source: `qa/b4-stress.tex` (created in qa/, not fix/tests/, see note). Build: `lualatex --disable-installer -output-directory=qa/b4out qa/b4-stress.tex` from the root, biber, lualatex x2.
Render: `docs/screenshots/b4-stress.png` (PyMuPDF, 130 dpi). 1 page, 0 errors, 0 overfull/underfull boxes.
Note: ch.14 / ch.19 of the course book are not on disk, so "rule" below = PRD / cls-commands.md / general BiDi and layout practice. Please confirm against the book.

Note on a false alarm I made first: a heredoc turned `\\` into `\` and caused 100+ "Misplaced \noalign" errors. This is NOT a CLS problem; the final file was written with the Write tool.

## Findings (report only, no fixes)

| ID | Sev | Page area | Exact text | Rule broken / observation | Recurring? / owner |
|----|-----|-----------|-----------|---------------------------|--------------------|
| B4-1 | major | top of page, above the heading | "Table 1. Pricing tiers (assumptions)" and "Figure 1. Pipeline" printed BEFORE "0.1 Stress test: mixed English and Hebrew" | Floats `[tbp]` jump above the heading that introduces them; the page starts with a table, not the section. Layout rule: a float should not precede its section heading / be placed before the text that refers to it. | yes (every chapter with [tbp] floats) -> fix-se (CLS float default / placement) |
| B4-2 | minor | build log | `Package biblatex Warning: Language 'hebrew' not supported.` and `Package microtype Warning: Unknown slot number of character` (x2) | A clean build should have no package warnings from the Hebrew switch. | yes, every Hebrew page -> fix-se |
| B4-3 | minor | code box, lines 1 and 4 | line 1 `"""ClosetTwin financial model. Single source of truth: python/data/assumptions.csv.` wraps with a mocha `\` and `... python/data/sensitivity_out.csv (for F6).` wraps; log: `Class closettwin Warning: pythonbox: 2 line(s) of python/model.py are longer than 80` | Code lines over 80 characters. The box is by design; the source file breaks the 80-char rule. | no (one file) -> art-se (python/model.py) |
| B4-4 | minor | English sentence, line 2 | `$49.90 or ₪ 49.90 per order` | Currency format inconsistent in one sentence: `$` glued to the number, `₪` followed by a space. Documented behaviour of `\usd` / `\ils`, but it reads as an inconsistency. | yes (all `\ils` uses) -> fix-se / master-se decision |
| B4-5 | minor | Hebrew paragraph, line 1 | `בשנים 2024–2026` shows visually as `2026–2024` | The range is displayed with 2026 on the left. In an RTL run the en dash between two numbers takes the RTL direction. Check against ch.14 whether ranges must be isolated LTR (`2024–2026` visually). | yes (every range in Hebrew text) -> fix-se (a `\yrange`-type command or dash handling) |
| B4-6 | minor | between table and figure | gap between table bottom rule and the TikZ nodes is about 22 px; gap above/below other boxes is about 28 px | Vertical rhythm between floats is tighter than between boxes. | yes -> fix-se |
| B4-7 | minor (test artefact) | section heading | `0.1 Stress test...` | Number "0.1" appears because my test has no `\chapter`. Not a defect. | no |

## Checked and fine
- English line with Hebrew phrase `(ארון בגדים וירטואלי)`: parentheses correct, no reversal.
- Hebrew paragraph: flush right, `ב-30%`, `24.4`, `49.90 ש״ח`, `$49.90`, `AI`, `ו-API`, final period all correct; no missing glyphs.
- Decimals 24.4, 49.90, 199.00; percent; `$`; `₪` all render. Table: caption above, right-aligned numbers, header band ends at the rules.
- Formula in Latin Modern Math, equation number (1) at the right. TikZ nodes and arrows render, 8 pt text.
- Statcard, insight box and code box are not split or alone at the top. Footer `Page 1 of 1`.
