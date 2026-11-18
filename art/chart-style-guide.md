# ClosetTwin chart style guide (art-se, v1.0, 2026-11-18)

Look: Vogue-like. Airy, hairline rules, lots of ivory, one idea per figure. Fixed by the team: ink `#111111`, ivory `#F7F3EE`, mocha `#A47864`, powder pink `#E8C6C0`; Playfair Display (headings), Rubik (body). All Python figures import `python/ct_style.py`; no script sets colors, fonts or sizes by hand.

## 1. Color
| Token | Hex | Role |
|---|---|---|
| ink | `#111111` | text, axes, the primary series, "ours" |
| mocha | `#A47864` | series 2 |
| powder pink | `#E8C6C0` | series 3, fills, bands (needs ink outline) |
| ivory | `#F7F3EE` | NOT the figure background (page is white, figures are transparent); only for light fills inside a figure and the swatch PNG |
| **mocha-deep** (derived) | `#6B4B3D` | series 4, emphasis. mocha mixed 60/40 with ink |
| **mocha-pale** (derived) | `#D3BBAE` | sequential ramp step. mocha mixed 50/50 with ivory |
| grid | `#E3DCD4` | hairline gridlines |
| muted | `#6F6862` | tick/axis labels, secondary text (4.96:1 on ivory) |

**Proposal: add the two derived tints, no new hues.** The four fixed colors give only three distinguishable fills on ivory (ivory is the background), so a 4th series and a sequential ramp need them.

- **Categorical order (fixed, never cycled, max 4):** ink → mocha → powder pink → mocha-deep. Color follows the entity: "ClosetTwin" is always ink, the market/baseline always mocha, across every figure. A 5th series becomes "Other" in mocha-pale, or the chart is split.
- **Sequential (magnitude, e.g. TAM→SAM→SOM nested):** pink → mocha-pale → mocha → mocha-deep → ink (light→dark, one hue family).
- **Diverging:** not used. Avoid it; use ink vs mocha with a zero line.
- **Text never wears a series color.** Labels are ink (values) or muted (axes). Colored marks beside them carry identity.
- Highlight pattern: the one series that matters is ink or mocha-deep; everything else mocha-pale / grid gray.

### Validator note (honest result)
`validate_palette.js` run on ink/mocha/pink/mocha-deep: **PASS** colorblind separation (worst adjacent ΔE 24) and normal-vision separation; **FAIL** lightness band and chroma floor (ink and the pastels are deliberately neutral, which is the editorial look); **WARN** pink is 1.43:1 on ivory. These are expected for a fashion palette. Required relief, enforced in `ct_style`: every fill gets a 0.6pt ink hairline edge, every series is direct-labeled, and pink/pale never carry information by color alone.

## 2. Type
| Element | Font | Size at 1:1 |
|---|---|---|
| Optional in-figure heading or hero number (`ct.head`) | Playfair Display | 12pt |
| Direct labels, value labels | Rubik | 8pt, ink |
| Tick labels, axis titles | Rubik | 8pt, muted |
| Annotations | Rubik | 8pt, ink |

Figures are placed at their native size (no scaling), so 8–9pt in the figure is 8–9pt on the page, slightly smaller than the 11pt body. Captions and titles live in LaTeX (`\caption`), so figures carry **no title by default**. Fonts load from `fonts/*.ttf`; until they exist `ct_style` falls back to Georgia / Segoe UI (the swatch says "fallback fonts in use"). Text stays real text in the PDF (`pdf.fonttype 42`). Figures are English only; Hebrew text inside a figure is avoided (needs BiDi shaping in matplotlib). If one is needed, art-se will use a TikZ figure instead.

## 3. Axes, grid, labels
- Only a thin ink baseline on x; **no top, right or left spines**. Horizontal hairline grid (0.5pt, `#E3DCD4`), none vertical. No tick marks.
- **Direct labels over legends**: label each line at its right end, each bar at its tip. With 2 or more series that cannot be directly labeled cleanly, add a legend (no frame, above the plot, left-aligned).
- One y-axis only. Never dual axes: two scales means two panels or indexing.
- Units in the axis title or label ("USD thousands", "% of orders"), not in the caption alone. Thousands separators; 0–1 decimals.
- Number every claim to its source in the LaTeX caption; assumptions are labeled "Assumption" in the caption (rule from PRD).
- Value labels on at most the key points (the end value, the break-even, the peak), never on every point.

## 4. Geometry and output
- Width: `ct.figure(width_frac, aspect)` gives `width_frac × 6.27in` (A4 minus 1in margins). In LaTeX: `\includegraphics[width=\textwidth]{...}` for full, `0.48\textwidth` for half. **If fix-se's text width differs, change `TEXTWIDTH_IN` in `ct_style.py` once.**
- Default aspect 0.55 (full), 0.75 (half-width). Generous margins; `bbox tight` with 0.04in padding.
- Output: **vector PDF** `figures/<name>.pdf`, transparent background (the page is white; ivory is only for banner, boxes and table headers). PNG only for the swatch/screenshots.
- Lines 1.8pt, round caps. Markers ≥ 4pt only at labeled points. Bars: flat, 0.6pt ink edge, gap between bars ≥ 35% of bar width, no rounded corners, no 3D, no shadows.

## 5. Chart types per use
| Use | Form | Notes |
|---|---|---|
| **TAM / SAM / SOM** | Concentric (nested) circles or a horizontal nested-bar stack, sequential ramp, outside direct labels "TAM  USD X bn" | Nested circles are not area-proportional at this scale; say so in the caption, or use three horizontal bars (preferred if values differ by 100×). A figure, not a table. |
| **Revenue / cost over 5 years** | Grouped bars (revenue ink, costs mocha) by year, with a net-profit line in mocha-deep; or lines for revenue and cost | One axis. Label the Year 5 values. Mark "Assumption" in caption. |
| **Break-even** | Two lines (cumulative revenue ink, cumulative cost mocha) crossing, pink band for loss area, one annotated dot at the crossing "Break-even: month N" | The crossing is the single hero label. |
| **Return-rate comparison** | Horizontal bars sorted descending (category, e.g. industry average vs with ClosetTwin), highlighted bar ink, others mocha-pale | Show the % at the bar tip. Zero baseline mandatory. |
| **Competitor positioning** | 2×2 scatter (two named axes, mid-lines as hairlines), dots 8pt, ClosetTwin ink, competitors mocha, name labels beside dots | No numeric scale unless data is real. A positioning map is qualitative: label axes "Low → High" and say so in the caption. Never fabricate numbers. |
| Cost/benefit pie | Avoid. Use horizontal bars. | |

## 6. Grayscale and print
Luminance (relative): ink 0.006, mocha-deep 0.085, mocha 0.222, mocha-pale 0.524, powder pink 0.613. Ink, deep and mocha separate clearly in gray. **Pale and pink are almost identical in gray**, so never use both in one chart without a different edge or hatch. Rules: every filled mark has the ink hairline edge; lines add direct labels (or dash style for the second line if labels would collide); no adjacent pair of fills closer than ink/mocha-deep/mocha/pink in tone. For the rare chart needing 4 fills in print, use hatch `////` (0.4pt) on one of them.

## 7. TikZ diagrams (style spec for the writer of `figures/*.tex`)
Keep every diagram inside one `\begin{tikzpicture}` using shared style keys (to be defined once in the CLS by fix-se; art-se will supply the key list):
- Colors: `ink`, `mocha`, `pink`, `ivory`, `mochadeep`, `mochapale` named exactly as above.
- Lines: 0.6pt ink for node borders and arrows (`line width=0.6pt`), 0.4pt for guides, `-{Stealth[length=4pt]}` arrowheads. No shadows, gradients or rounded corners above `rounded corners=2pt`.
- Nodes: rectangles `minimum height=8mm, inner sep=5pt`, fill ivory or pink, ink border; the key node (ClosetTwin) is filled ink with ivory text. Decision/state nodes use the same rectangle with a mocha border; no clip-art.
- Text: Rubik 8–9pt in nodes, Playfair only for a diagram title. English only.
- Spacing: `node distance=12mm`, align on a grid; one flow direction (left→right) and ≤ 7 nodes per diagram.
- Width: `\textwidth`-based via `resizebox` only if unavoidable (avoid it; scaling changes text size).

## 8. Checklist before art-se reports DONE on any figure
1. Imports `ct_style`; no hard-coded colors/fonts/absolute paths; fixed random seed if any.
2. Output is `figures/<name>.pdf`; the command is `python python\<script>.py` from the root.
3. Direct labels present; no dual axis; no title inside the figure (caption in LaTeX).
4. Looks right in grayscale (convert and check).
5. Checked inside the built PDF (fonts embedded, size at 1:1).

## Decisions (master-se, provisional until the user's round)
1. Tints mocha-deep and mocha-pale provisionally approved. They are named tokens in `ct_style.py`; drop by deleting them and `CAT[3]`/`SEQ`.
2. Text width comes from the single constant `TEXTWIDTH_IN`; master-se will send the real value after fix-se F1.
3. Page is white; figures are transparent.
4. Fonts: fallbacks until `fonts/` exists.
