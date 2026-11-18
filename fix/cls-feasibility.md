# CLS feasibility study (task F1) — fix-se, 2026-11-18

Engine: LuaHBTeX 1.24 (MiKTeX 25.12), biber 2.21, biblatex 3.21. Everything below was compiled, not assumed.
Test files: `fix/tests/t1..t5.tex` (t3 = minimal winning Hebrew setup, t5 = full prototype: banner, footer, ivory page, Playfair headings, formula, table, Hebrew page with citation, IEEE bibliography).

## 1. Recommendation (short)

| Topic | Decision |
|-------|----------|
| CLS name | `closettwin.cls` (article-based; loads everything; the only file `main.tex` needs besides chapters) |
| Bidi engine | **babel** with `bidi=basic` (+ `\babelprovide[import,onchar=ids fonts]{hebrew}`). **Not polyglossia** (see 3) |
| Fonts | `fontspec`, loaded **by path** from `fonts/` (`Path=`, `Extension=.ttf`), **static TTFs** generated from the OFL variable fonts |
| Banner / footer | `fancyhdr` + a TikZ overlay (`remember picture,overlay`, `current page`) for the full-bleed banner |
| Page colour | `\pagecolor{ivory}` (xcolor) + text colour ink |
| Bibliography | `biblatex` `style=ieee`, `backend=biber` (+ `csquotes`) |
| Math | `unicode-math`: Latin Modern Math for symbols, Rubik for upright Latin/digits (see risk R2) |
| Hebrew page | an environment `\begin{hebrewpage}...\end{hebrewpage}` wrapping `otherlanguage{hebrew}` |

## 2. Fonts

* Source: official OFL files from the `google/fonts` repo (`ofl/playfairdisplay`, `ofl/rubik`), with `OFL-*.txt`, in `C:\biu\02\fonts\`. The original variable fonts are kept in `fonts/source/`.
* **Why static instances:** luaotfload does not reliably select named instances of variable fonts (`wght` axis). I generated static weights with `fontTools.varLib.instancer` (`python -m fontTools.varLib.instancer X[wght].ttf wght=400 -o X-Regular.ttf --update-name-table`). Result in `fonts/`:
  `PlayfairDisplay-{Regular,Bold,Italic,BoldItalic}.ttf`, `Rubik-{Regular,Medium,Bold,Italic,BoldItalic}.ttf`. Embedded correctly (pdffonts: all `emb yes`).
* **Loading by path works** and makes the build reproducible on any machine with no installed fonts: `\defaultfontfeatures{Path=<cls dir>/fonts/,Extension=.ttf}`. Gotchas: the path is relative to the *working directory*, so the CLS must build the path from the project root (the build is always run from `C:\biu\02`, so `Path=./fonts/`). `Path=` also leaks into `\setmathfont{...}` for other fonts, so for Latin Modern Math reset it: `[Path={},Extension={}]`.
* **Rubik Hebrew coverage (checked with fontTools):** all 27 letters U+05D0–05EA incl. finals, niqqud (U+05B0…), geresh/gershayim U+05F3/05F4, maqaf U+05BE, shekel sign U+20AA, `% $ € ( ) [ ] / : ; , . - – — “ ” ‘ ’`, fi ligature. Missing only U+200E/200F (control marks, not needed as glyphs). 47 Hebrew-block glyphs.
* **Playfair Display has NO Hebrew glyphs.** A Hebrew heading set with Playfair shows tofu boxes (proved in t5). So Hebrew headings must use Rubik; the CLS must do this automatically (a Hebrew heading macro / Hebrew-aware heading hook), otherwise writer-se will hit it.
* Playfair numerals are old-style by default (`30%` renders as old-style). Recommend `Numbers=Lining` for headings if the editorial look needs it (art-se/master to decide).

## 3. babel vs polyglossia vs luabidi (the key finding)

| Setup | Result |
|-------|--------|
| babel `bidi=default` (t1) | **FAIL**: Latin and digits inside Hebrew are reversed (`ClosetTwin`→`niwTtesolC`, `2026`→`6202`) |
| polyglossia (t2) | **FAIL**, same reversal (polyglossia already loads luabidi; adding `\usepackage{luabidi}` again errors `\localnumeral already defined`) |
| **babel `bidi=basic`** (t3, t5) | **PASS**: Latin, numbers, `30%`, `49.90`, parentheses, `[1]` citation, English brand names and `ש"ח` all in correct visual order |

So: `\usepackage[english,bidi=basic]{babel}`, `\babelprovide[import,main]{english}`, `\babelprovide[import,onchar=ids fonts]{hebrew}`, then `\begin{otherlanguage}{hebrew}…\end{otherlanguage}`. Page direction, paragraphs, lists inside the block flip to RTL; the rest of the document stays LTR. The banner/footer (absolute TikZ coordinates) stay LTR on the Hebrew page, which is what we want ("banner + footer on every page").

## 4. Banner and footer

Proved in t5: a full-bleed mocha banner across the top (`tikz` overlay, `current page.north west/east`), brand name in Playfair, footer `ClosetTwin | page` in mocha, on every page including the first page and the Hebrew page (`fancypagestyle{plain}` redefined so chapter-first pages keep it). Open detail: fancyhdr warns `\headheight too small`; the CLS must set `\setlength{\headheight}{…}` and a top margin that clears the banner (I used 3.2 cm top margin, banner 1.6 cm high). `biblatex-ieee`, `fancyhdr`, `luabidi`, `unicode-math`, `csquotes` all load without problem.

## 5. biblatex-ieee in MiKTeX

Works: `style=ieee`, `backend=biber`; bibliography entry and numeric `[1]` citation rendered correctly (t5, build sequence lualatex→biber→lualatex→lualatex). Warnings to handle in the CLS: `csquotes missing` (load `csquotes`), `Language 'hebrew' not supported` (harmless; the bibliography is English only).

## 6. Known BiDi pitfalls and how the CLS handles them

1. **Never write a bare `%` in the text** (obviously a LaTeX comment): use `\%`. This cost me a false failure; writer-se will hit it in Hebrew text too. A macro `\pct{30}` is cheap insurance.
2. **Latin inside Hebrew**: fine with `bidi=basic`. Do not wrap it in `\textenglish` (not needed).
3. **Numbers and units** (`49.90`, `2026`, `30%`, `ROI = 25%`): correct in t5. Always keep a number and its `%`/currency in one run; the CLS can offer `\ils{49.90}` = `49.90 ש״ח` with a no-break space.
4. **Gershayim**: type `״` (U+05F4) not ASCII `"`; ASCII `"` also renders but is wrong typographically. Provide `\shekel`/`\ils` macros.
5. **Parentheses/brackets** are mirrored properly; a citation `\cite{..}` in a Hebrew sentence renders `[1]` in LTR run correctly.
6. **Math in Hebrew**: renders LTR inside the RTL line. Fine for small expressions (`ROI = 25%`); avoid display math on the Hebrew page.
7. **Hebrew heading font**: Playfair has no Hebrew (see 2) → handled by the heading macro.
8. **Bold Hebrew**: `\textbf` works (Rubik-Bold). Italic Hebrew is a synthetic-looking slant; recommend avoiding italic in Hebrew.
9. **pdftotext order** of Hebrew is logical/odd; QA must check Hebrew visually (render the PDF page to PNG) rather than by text extraction.
10. Hyphenation/line breaking in Hebrew: babel's Hebrew has no hyphenation; justified Hebrew can give loose lines. Recommend `\raggedleft`-style (ragged) Hebrew page or `\RaggedLeft`-equivalent; I'd keep the Hebrew page unjustified.

## 7. Public macros (proposed API of `closettwin.cls`)

* Options: none required (a4paper, 11pt fixed); optional `draft`.
* `\ctbrand` (brand string), `\ctversion`.
* Colours: `ink`, `ivory`, `mocha`, `powderpink` (xcolor names).
* `\pct{30}` → 30%, `\ils{49.90}` → `49.90 ש״ח`, `\usd{…}`.
* Environment `hebrewpage` (RTL page, Rubik headings, ragged, forces `\clearpage` before and after).
* `\hebsection{…}` / Hebrew-aware `\section*` that switches to Rubik Bold.
* Heading styles: Playfair Bold for `\section/\subsection` (via `titlesec`), Rubik body.
* Figure/table helpers: `\ctfigure`, caption style (mocha label, ink text), `booktabs` table look, `\assumption{…}` tag for financial assumptions ("Financial figures are labeled as assumptions").
* Standard packages preloaded: `tikz`, `pgfplots`, `booktabs`, `caption`, `csquotes`, `biblatex` (ieee), `hyperref` (last), `microtype`.

## 8. What I proved by compiling (all green)

| Test | Proves |
|------|--------|
| t1/t3 | babel `bidi=basic` + Rubik: Hebrew + Latin + numbers + `30%` + `[3]` + `ש"ח`, bold Hebrew |
| t2 | polyglossia reverses Latin → rejected |
| t5 | Full stack on 3 pages: fonts by path (only Playfair + Rubik + LM Math embedded), ivory page, mocha banner, footer with page number, formula `\dfrac` and `\sum`, booktabs table, Hebrew page with cite, `style=ieee` biber build, no errors |

## 9. Open risks

* **R1 Environment:** MiKTeX did not have many packages. Compiles **hang** on the GUI "install missing package" prompt (it hung my first `kpsewhich` and `lualatex` calls). I installed with `mpm` (user scope): polyglossia, luabidi, biblatex-ieee, fancyhdr, unicode-math, booktabs, caption, microtype, csquotes, siunitx, enumitem, titlesec, lualatex-math, lm-math, infwarerr, kvoptions, ltxcmds, etexcmds, letltxmacro, refcount, gettitlestring, intcalc, bitset, bigintcalc, auxhook, rerunfilecheck, uniquecounter, hycolor, kvsetkeys, kvdefinekeys, stringenc, pdfescape, hopatch, xstring, logreq. **Every agent must build with `lualatex --disable-installer`** (or MiKTeX must be set to "install on the fly: Yes") or the build can hang forever. master-se should put this in the build recipe and README. More packages may turn up missing (hyperref's deps, pgfplots, etc.).
* **R2 "Fonts ONLY Playfair + Rubik":** math symbols (∑, ≈, ×, fraction rule, Greek) need a math font; Rubik has no math table. t5 uses Latin Modern Math for symbols only (it is embedded). Decision needed from master-se: accept LM Math as a math-symbol exception (recommended; it only appears inside formulas) or avoid symbol-heavy math. Same for `\mathrm` digits: those come from Rubik.
* **R3 Variable fonts:** if anyone swaps in the variable TTFs, weights break. Keep the static files.
* **R4 Path:** relative `Path=` needs the build from the project root; a build from a subfolder fails to find fonts. The CLS should resolve it via `\input@path`/`\jobname` root or document "always build from C:\biu\02".
* **R5 Playfair Hebrew / old-style digits** (see 2).
* **R6 Hebrew justification quality** (see 6.10) and italics.
* **R7 biblatex language warning** for Hebrew (harmless), and `\cite` in the Hebrew page shows `[1]` in the English reference list: fine for the single summary page.
* **R8 Banner geometry:** fancyhdr `\headheight` and the top margin must be set so the 1.6 cm banner never overlaps body text; needs to be tuned together with the page-budget (25+ pages).

---
## 10. F1b — font licence fix (2026-11-18, requested by master-se)

* **Problem:** my fontTools instances of Playfair Display are *Modified Versions* that still carry the Reserved Font Name "Playfair Display" (OFL §3 forbids this).
* **Fix:** replaced them by the **official, unmodified static TTFs** of Playfair Display v1.200 (ttfautohint), taken from `google/fonts` commit `10a708073179c32928eb894e53465fca8106772f` (`ofl/playfairdisplay/static/`, the last commit before static files were removed; the upstream GitHub releases 2.200–2.203 ship variable fonts only). File sizes match the GitHub listing byte for byte (Regular 210208, Bold 213592, Italic 213028, BoldItalic 215008). `OFL-PlayfairDisplay.txt` replaced by the one from the same commit. `fonts/source/` keeps the unmodified variable originals. Black/BlackItalic not used.
* **Rubik:** its OFL header is `Copyright 2015 The Rubik Project Authors` — **no Reserved Font Name**, so the fontTools static instances (Regular/Medium/Bold/Italic/BoldItalic) may stay as Modified Versions. They keep the OFL file and the same family name; the originals are in `fonts/source/`.
* **Re-proof:** `fix/tests/t5.tex` rebuilt (lualatex → biber → lualatex ×2) with the official Playfair files: 3 pages, no errors, no undefined references; `pdffonts` shows `PlayfairDisplay-Regular/Bold` + Rubik + LM Math. The only "Missing character" lines are the deliberate Hebrew-in-Playfair demonstration, which the CLS Hebrew heading macro will route to Rubik. Playfair v1.200 has all of `– — “ ” ‘ ’ % $ € £ & @ # №` and digits, and the `lnum` feature (lining numerals).

## 11. Proposed page geometry (for F2)

A4 = 210 × 297 mm, one-sided.

| | value | note |
|---|---|---|
| left / right margin | **3.0 cm** | airy, ≥ 2.5 cm |
| **text width** | **15.0 cm** (= 5.906 in) | ~70–75 characters per line in Rubik 11 pt: ideal |
| top margin | **3.6 cm** | clears the 1.6 cm banner + 2 cm air |
| bottom margin | **3.0 cm** | footer hairline + page number inside it |
| text height | 297 − 36 − 30 = **231 mm** | |
| body | Rubik 11 pt on 15.5 pt baseline (≈1.4) | `\parskip` 0.6 em, no indent |
| `TEXTWIDTH_IN` for art-se | **5.906** | full-width figure = 15 cm; half = 7.2 cm |

Capacity warning for master/writer: at 15 cm × 231 mm and 1.4 line spacing a page holds ~430–480 words, so 27 content pages with figures/tables on ~40 % of the space means ≈ 7–8 k words of text. Do not shrink the margins to hit the page count; add content instead.
