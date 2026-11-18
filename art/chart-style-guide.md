# ClosetTwin chart style guide (art-se, v1.1, 2026-11-18)

Look: Vogue-like. Airy, hairline rules, one idea per figure. Fixed by the team: ink `#111111`, ivory `#F7F3EE`, mocha `#A47864`, powder pink `#E8C6C0`; Playfair Display (headings), Rubik (body). All Python figures import `python/ct_style.py`; no script sets colors, fonts or sizes by hand. The page is **white** and figures are **transparent**.

Changes in v1.1: text width 15.0 cm / 5.906 in; fixed canvas, no `bbox tight`; no font fallback; the 7-figure list (PRD §5.4); contrast rules (PRD §5.1); RT-A review results.

## 1. Color and contrast
| Token | Hex | Contrast on white | Allowed use in figures |
|---|---|---|---|
| ink | `#111111` | 18.9:1 | all text, axes, ClosetTwin's own series |
| mocha | `#A47864` | 3.85:1 | series 2 / market-baseline; fills, rules. **Never small text** |
| powder pink | `#E8C6C0` | 1.4:1 | fills and bands only, always with an ink hairline. **Never carries text** |
| ivory | `#F7F3EE` | 1.1:1 | light fill inside a figure only with a 0.4pt edge. Not the figure background |
| *mocha-deep* (pending Q-A) | `#6B4B3D` | 7.8:1 | series 4, emphasis |
| *mocha-pale* (pending Q-A) | `#D3BBAE` | – | a step in the sequential ramp, hairlines |
| grid | `#E3DCD4` | – | hairline gridlines |
| muted | `#6F6862` | 5.4:1 | tick/axis labels, secondary text |

If Q-A is *no*: delete `MOCHA_DEEP`/`MOCHA_PALE` in `ct_style.py`; the categorical order stops at 3 series and the sequential ramp becomes pink → mocha → ink.

- **Categorical order (fixed, never cycled, max 4):** ink → mocha → powder pink → mocha-deep. Color follows the entity: ClosetTwin is always ink, the market/baseline always mocha. A 5th series is "Other" in mocha-pale, or the chart is split.
- **Sequential:** pink → mocha-pale → mocha → mocha-deep → ink (one hue family, light → dark).
- **Diverging:** not used (ink vs mocha with a zero line).
- **Text never wears a series color.** Labels are ink (values) or muted (axes).
- Highlight pattern: the one series that matters is ink or mocha-deep; the rest mocha-pale or grid gray.

### Validator note
`validate_palette.js` on ink/mocha/pink/mocha-deep: **PASS** colorblind and normal-vision separation (worst adjacent ΔE 24); **FAIL** lightness band and chroma floor (ink and the pastels are neutral on purpose); **WARN** pink contrast. Relief, enforced in `ct_style`: 0.6pt ink hairline on every fill, every series direct-labeled, pink/pale never carry information by color alone.

## 2. Type
| Element | Font | Size at 1:1 |
|---|---|---|
| Optional in-figure hero number (`ct.head`) | Playfair Display | 12pt |
| Direct and value labels, annotations | Rubik | 8pt, ink |
| Tick labels, axis titles | Rubik | 8pt, muted |

Figures are exactly text width, so 8pt in the figure is 8pt on the page (body is 11pt). Captions and titles live in LaTeX, so figures have **no title**. Fonts load by path from `fonts/*.ttf` (static files, top level only); **there is no fallback**: `ct_style` raises an error if Playfair Display or Rubik is missing. Text stays live text in the PDF (`pdf.fonttype 42`; check with `pdffonts`). Figures are English only; Hebrew in a figure needs BiDi shaping, so use TikZ for it.

## 3. Axes, grid, labels
- A thin ink baseline on x; **no top, right or left spines**. Horizontal 0.5pt hairline grid only. No tick marks.
- **Direct labels over legends**: label lines at the right end, bars at the tip. A legend (no frame, above the plot, left-aligned) only when direct labels collide.
- One y-axis only. Two scales means two panels (small multiples) or indexing.
- Units in the axis label. Thousands separators; 0–1 decimals.
- The LaTeX caption gives the source and says "assumption" for modeled numbers (`\sourced` / `\derived` / `\assumed` tags).
- Value labels only on key points (end value, break-even, peak).

## 4. Geometry and output
- `TEXTWIDTH_IN = 5.906` (15.0 cm), one constant in `ct_style.py`. `ct.figure(width_frac, aspect)` makes a **fixed canvas** of `width_frac × 5.906 in`; no `bbox tight`, constrained layout. The PDF page is exactly that wide (verified: 425.232 pt at 1.0), so `\includegraphics[width=<same fraction>\textwidth]` scales by 1.0.
- Default aspect 0.55 (full width), 0.75 (half width, 0.48 `\textwidth`).
- Output: vector PDF `figures/<name>.pdf`, transparent. PNG only for screenshots.
- Lines 1.8pt, round caps. Markers ≥ 4pt only at labeled points. Bars flat with a 0.6pt ink edge, gap ≥ 35% of bar width. No 3D, shadows or rounded corners.

## 5. The seven figures (PRD §5.4)
| # | Figure | Ch. | Tool | Form and rules |
|---|---|---|---|---|
| F1 | TAM / SAM / SOM | 2 | Python or TikZ | Three **nested shapes, explicitly not to scale** (caption says so). One reference year printed in each label ("TAM 2025 …"). Sequential ramp, labels outside. No bars (SOM would be invisible) |
| F2 | Positioning map | 3 | Python | 2×2 scatter. x = questionnaire/size chart ↔ body scan; y = consumer app ↔ B2B plug-in, **from the vendor-table columns**. Dots 8pt, ClosetTwin ink, vendors mocha, name beside each dot. Caption: "positions are our reading of vendor pages". No numeric scale |
| F3 | Scan → body model + garment specs + fit preference → size → retailer data | 4 | TikZ | Left-to-right flow, ≤ 7 nodes |
| F4 | Roadmap | 7 | TikZ | 6-row Gantt strip |
| F5 | 5-year projection and break-even | 8 | Python | **One figure, two small-multiple panels** (left: revenue and cost by year; right: cumulative net with the break-even month annotated). No dual axis. Assumption in the caption |
| F6 | Sensitivity | 8 | Python | Break-even month against the return-reduction effect (0 → base case); one line, base case labeled |
| F7 | Risk heat matrix | 9 | TikZ | Likelihood × impact, each score labeled as assumed. Cells use the sequential ramp with the score in text, never color alone |

Ch. 1 uses stat cards, not a chart (a chart only if ≥ 4 sourced comparable values exist). Ch. 6 funnel is a table. Pie charts: never.

## 6. Grayscale and print
Relative luminance: ink 0.006, mocha-deep 0.085, mocha 0.222, mocha-pale 0.524, powder pink 0.613. Ink, deep and mocha separate in gray. **Pale and pink are nearly the same gray**: never use both in one chart without a different edge or hatch (`////`, 0.4pt). Every filled mark has the ink hairline; lines get direct labels or a dash style.

## 7. TikZ diagrams
One `tikzpicture` per diagram using shared style keys defined once in the CLS by fix-se (art-se supplies the key list):
- Colors named `ink`, `mocha`, `pink`, `ivory`, `mochadeep`, `mochapale`.
- Lines 0.6pt ink for borders and arrows, 0.4pt for guides, `-{Stealth[length=4pt]}` arrowheads. No shadows or gradients; `rounded corners` ≤ 2pt.
- Nodes: rectangles, `minimum height=8mm, inner sep=5pt`, fill ivory (with its 0.4pt edge) or pink, ink border; the key ClosetTwin node is ink-filled with ivory text. No clip-art.
- Text Rubik 8–9pt; Playfair only for a diagram title. English only.
- `node distance=12mm`, grid-aligned, one flow direction. No `resizebox` (it changes type size); design at 15.0 cm.

## 8. Checklist before art-se reports DONE on a figure
1. Imports `ct_style`; no hard-coded colors, fonts or absolute paths; fixed seed if random.
2. Output `figures/<name>.pdf`, made by `python python\<script>.py` from the root.
3. Direct labels, no dual axis, no in-figure title.
4. `pdffonts` shows only Rubik/Playfair, no Type 3; PDF width equals the fraction × 15.0 cm.
5. Grayscale check; checked inside the built PDF.

## Decisions on record
1. Mocha-deep and mocha-pale: PRD marks them pending Q-A (the user).
2. Text width 15.0 cm; page white; figures transparent (master-se).
3. T2.8 done: fixed canvas, fonttype 42, no fallback.
