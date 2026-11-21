# ClosetTwin report (assignment 02)

A Hebrew/English (RTL + LTR) business-plan report, typeset with **LuaLaTeX** (MiKTeX) and the project class `closettwin.cls`.

* What we deliver: `PRD.md`. How and in what order: `PLAN.md`. Who does what now: `TODO.md`.
* Using the class in another document: **`docs/template-README.md`**. Every command with an example: `docs/cls-commands.md`.
* Class history: `fix/CHANGELOG.md`.

## Build
From the project root, always this order (the class loads the fonts by relative path from `fonts/`):

```
lualatex --disable-installer main
biber main
lualatex --disable-installer main
lualatex --disable-installer main
```

`--disable-installer` makes a missing MiKTeX package an error instead of a hanging install prompt.
A build is clean only with no errors, no undefined references or citations, and no overfull boxes over 1 pt.
Python is run as `python`; the graph scripts in `python/` write to `figures/`.

## Requirements
* MiKTeX with LuaLaTeX, biber 2.21, biblatex 3.21 (MiKTeX 25.12).
* MiKTeX packages: fontspec, unicode-math, babel (hebrew, english), titlesec, titletoc, enumitem, booktabs, colortbl,
  tabularx, caption, placeins, microtype, csquotes, tikz, tcolorbox (listings, skins, breakable), listings, xkeyval,
  etoolbox, iftex, hyperref, geometry, amsmath, biblatex, biblatex-ieee, biber.
  (`lastpage` and `needspace` are not needed: the class has its own.)
* Fonts (OFL, in `fonts/`): Playfair Display (English headings), Rubik (body and all Hebrew), JetBrains Mono (code box only);
  Latin Modern Math for formulas.
* Python 3 with matplotlib and PyMuPDF for the figures and the page renders.

## Layout of the repository
| Path | Content |
|------|---------|
| `main.tex`, `chapters/` | the report |
| `closettwin.cls`, `fonts/` | the class and its fonts |
| `references.bib` | bibliography (no Hebrew script; see `docs/cls-commands.md`) |
| `python/`, `figures/` | graph scripts and their output |
| `docs/` | class documentation and screenshots |
| `prompts/` | curated prompts and the automatic prompt log |
| `writer/`, `art/`, `qa/`, `fix/` | each agent's notes and reports (not part of the deliverable) |

Team rules: `CLAUDE.md`.
