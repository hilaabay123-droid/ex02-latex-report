# closettwin.cls: command reference

Class `closettwin` (LuaLaTeX, based on `book`, oneside, A4, 11 pt). Owner: fix-se. The version is in
`\ProvidesClass` at the top of `closettwin.cls` and every change is logged in `fix/CHANGELOG.md`.
One purpose per command. Nothing in the class belongs to one document: every text comes from a command below.
Build from the project root (the fonts are loaded from `fonts/`).

## 1. Document set-up

| Command | Purpose | Example |
|---|---|---|
| `\documentclass{closettwin}` | Load the class. | `\documentclass{closettwin}` |
| `\ctfontdir` | Font folder (default `./fonts/`). Set it BEFORE `\documentclass` only in a test that is not built from the root. | `\newcommand*{\ctfontdir}{../../fonts/}` |
| `\ctbrand{Name}` | Brand name in the banner, footer and cover (default ClosetTwin). | `\ctbrand{ClosetTwin}` |
| `\ctbrandline{Tagline}` | Optional short line after the brand in the footer. | `\ctbrandline{Virtual fitting room}` |
| `\ctpageword` `\ctofword` | Footer words in English pages ("Page", "of"). Redefine with `\renewcommand*`. | `\renewcommand*{\ctpageword}{Page}` |
| `\cthebpageword` `\cthebofword` | Footer words on the Hebrew page. | `\renewcommand*{\cthebpageword}{עמוד}` |
| `\ctbibresource{file.bib}` | Register a bibliography file (preamble). | `\ctbibresource{references.bib}` |

## 2. Cover (`\ctmakecover`, stage 5)

Fields (all optional, no ID-number field exists):
`\cttitle` `\ctsubtitle` `\ctauthors` `\ctgroup` `\ctcourse` `\ctlecturer` `\ctdate`, plus `\ctdoctype{Business plan · 2026}` (small bold label at the top right of the cover; empty by default = no label).
Labels: `\ctlabelauthors` `\ctlabelgroup` `\ctlabelcourse` `\ctlabellecturer` (English defaults, redefinable).

```latex
\cttitle{ClosetTwin}
\ctsubtitle{An AI virtual fitting room for fashion e-commerce}
\ctauthors{Hila Abay, Shirel Giladi}
\ctgroup{sg00ha11}
\ctcourse{Generative AI for Management (875523402)}
\ctlecturer{Dr. Yoram Segal}
\ctdate{November 2026}
\begin{document}
\frontmatter
\ctmakecover      % ivory page, TikZ illustration, no banner and no footer
```

## 3. Hebrew page

| Command | Purpose | Example |
|---|---|---|
| `hebrewpage[title]` | Own page: RTL, Rubik, flush right, Hebrew footer ("עמוד N מתוך M"). The optional title is the running title; the page is an opener (no banner). | `\begin{hebrewpage}[תקציר מנהלים] ... \end{hebrewpage}` |
| `\hebtitle{text}` | Opener title: mocha rule + 30 pt Rubik Medium (same rhythm as a chapter opener). | `\hebtitle{תקציר מנהלים}` |
| `\hebsubtitle{text}` | Bold sub-heading. | `\hebsubtitle{ClosetTwin: חדר הלבשה}` |

Lists inside `hebrewpage` are mirrored automatically. A short Hebrew phrase in an English paragraph:
`\foreignlanguage{hebrew}{ארון בגדים}`.

## 4. Numbers and units (no Hebrew inside English units)

| Command | Output | Example |
|---|---|---|
| `\pct{30}` | 30% (unbreakable) | `\pct{30}` |
| `\usd{49.90}` | $49.90 | `\usd{49.90}` |
| `\ils{49.90}` | ₪49.90 in English (glued like `$49.90`), 49.90 ש״ח on the Hebrew page | `\ils{49.90}` |
| `\range{2024}{2026}` | A range that always reads 2024–2026 left to right, also inside a Hebrew paragraph. In Hebrew text write ranges this way (a bare `2024--2026` reverses there); in English text `2024--2026` is fine | `בשנים \range{2024}{2026}` |

## 5. Structure

| Command | Purpose | Example |
|---|---|---|
| `\chapter{..}` | Opener page: big mocha number, rule, Playfair title. The banner is hidden on this page, the footer stays. | `\chapter{Market}` |
| `\ctunnumbered{..}` | Unnumbered chapter that is still in the contents and the banner. | `\ctunnumbered{Appendix A}` |
| `\section` `\subsection` | Playfair headings with mocha-deep numbers. | |
| `\tableofcontents` `\listoffigures` `\listoftables` | Styled lists. | |
| `\ctchapterend` | Flush floats at the end of a chapter. | `\ctchapterend` |
| `itemize` `enumerate` | Mocha markers, same text edge. | |

## 6. Tables, figures, assumptions

| Command | Purpose | Example |
|---|---|---|
| `tabularx` + `\ctheaderrow` + `\cthead{}` + column `R` | Booktabs table, ivory header row, right-aligned numbers. Write the columns WITHOUT `@{}` so the header band ends at the rules. | see below |
| `\caption{}` | Table caption goes above, figure caption below, label in mocha-deep. | |
| `\sourced{x}` `\derived{x}` `\assumed{x}` `\assumption{x}` | Tag a number as S (sourced), D (derived) or A (assumed). `\ctlegend` prints the legend. | `\assumed{24\%}` |
| TikZ keys | `ct node`, `ct node ivory`, `ct node pink`, `ct key`, `ct decision`, `ct arrow`, `ct guide`, `ct label`, `ct title`, `ct bar`, `ct bar milestone`, `ct cell 1..5`. All text is 8 pt. | `\node[ct key]{ClosetTwin};` |

```latex
\begin{table}[tbp]
\caption{Pricing tiers (assumptions)}
\begin{tabularx}{\textwidth}{lRR}
\toprule
\ctheaderrow\cthead{Tier} & \cthead{Orders / month} & \cthead{Price (USD)}\\
\midrule
Starter & 1,000 & 99\\
\bottomrule
\end{tabularx}
\end{table}
```

## 7. Boxes (a box is never alone at the top of a page)

| Command | Purpose | Example |
|---|---|---|
| `\statcard{number}{claim}{source}` | Key-number callout (ivory, hairline). | `\statcard{24.4\%}{of apparel is returned}{Source: Coresight 2023}` |
| `\pullquote{text}{attribution}` | Magazine pull quote with a powder-pink bar. | `\pullquote{Fewer returns.}{ClosetTwin thesis}` |
| `insightbox[Label]` | Ivory insight box with a small label (never split; keep it under half a page). | `\begin{insightbox}[Key insight] ... \end{insightbox}` |
| `\pythonbox[first=N,last=M]{file.py}` | Code box that reads the REAL file: LTR, JetBrains Mono, file line numbers, 80 characters fill the box exactly, longer lines wrap with a mocha backslash and a class warning. Up to 15 lines it is never split; longer scripts break. | `\pythonbox[first=1,last=40]{python/model.py}` |

The code font is used in `pythonbox` only. Keep the script ASCII above the shown range (a non-ASCII character in a
skipped line adds a stray first line).

## 8. Maths

Formulas are Latin Modern Math only (letters, digits, `\mathrm`). Text-mode numbers stay Rubik.

```latex
\begin{equation}\mathrm{ROI}=\frac{G-C}{C}\times 100\%\end{equation}
```

## 9. References (biblatex, IEEE, biber)

```latex
\ctbibresource{references.bib}      % preamble
...
\ctreferences                       % where the list goes (unnumbered chapter "References")
```
### Non-English (Hebrew) sources: no Hebrew script in the .bib

IEEE practice: give the **English translation of the title** and mark the source as Hebrew with the `language` field.
The class prints `(in Hebrew)` inside the closing quote of the title. Protect proper nouns with braces (the style lowercases the title).

```bibtex
@article{cohen2024,
  author       = {Cohen, Dana and Levi, Yossi},
  title        = {A test of a translated title for a {Hebrew}-language source},
  journaltitle = {Journal of Examples},
  year         = {2024},
  volume       = {3},
  number       = {2},
  pages        = {10--20},
  language     = {hebrew},   % prints: ... source (in Hebrew),"
}
```
Result: `D. Cohen and Y. Levi, "A test of a translated title for a Hebrew-language source (in Hebrew)," Journal of Examples, vol. 3, no. 2, pp. 10-20, 2024.`
Do NOT also write "(in Hebrew)" in the title text and never put Hebrew letters in any field. Transliterate author names and keep the original title only in the `note` field if you need it, in Latin letters.

Cite with `\cite{key}`. Build: lualatex, biber, lualatex, lualatex.

### Typographic rules done by the class

* After `Dr.`, `Prof.`, `Mr.`, `Mrs.`, `Ms.`, `Fig.`, `Eq.`, `Sec.`, `Ch.`, `Tab.`, `No.` the space is a no-break space (`Dr. Yoram` never stretches), in every `.tex` file.
* References: digits are not grouped (`p. 100779`) and page ranges never break. No Hebrew script is ever put in `references.bib` (see section 9).

## 10. Colours (single definitions, PRD 5.1)

`ink` #111111, `ivory` #F7F3EE, `mocha` #A47864, `powderpink` #E8C6C0, `mochadeep` #6B4B3D, `mochapale` #D3BBAE,
`gridgray` #E3DCD4, `mutedgray` #6F6862. Aliases `pink` = powderpink and `muted` = mutedgray (art-se).

## 11. Page behaviour

* Banner (brand + chapter title) on every page except cover and openers; footer = brand + "Page N of M" on all pages except the cover.
* Widows and orphans are forbidden; boxes travel with the line before them and are never alone at the top of a page.
* Floats: write plain `\begin{table}` / `\begin{figure}` (no placement argument: the class ignores it). They go here, else to the top of the next page, else to a page of their own (never the foot of a page, never above the heading they follow).
* ONE gap, `\ctboxsep` = 14pt, separates boxes from boxes, text and floats; every box-to-box gap is the same.
* A missing glyph is a compile error (`\tracinglostchars=3`).
