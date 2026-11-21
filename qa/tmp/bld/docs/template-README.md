# closettwin template: how to use it

A LuaLaTeX class for a Hebrew/English magazine-style report (white page, ivory cover and boxes, mocha palette).
Command reference with one example per command: `cls-commands.md`.

## Files
```
closettwin.cls     the class (version in \ProvidesClass; every change in fix/CHANGELOG.md)
fonts/             Rubik, Playfair Display, JetBrains Mono (OFL, licences inside), loaded by path
references.bib     biblatex database (biber)
main.tex           your document
```

## Minimal main.tex
```latex
\documentclass{closettwin}
\cttitle{Title}\ctsubtitle{Subtitle}\ctauthors{Names}\ctcourse{Course}\ctlecturer{Lecturer}\ctdate{Month Year}
\ctbibresource{references.bib}
\begin{document}
\frontmatter
\ctmakecover
\begin{hebrewpage}[Hebrew running title]\hebtitle{Hebrew title} ... \end{hebrewpage}
\tableofcontents
\mainmatter
\chapter{First chapter} ...
\ctreferences
\end{document}
```

## Build (from the project root, always this order)
```
lualatex --disable-installer main
biber main
lualatex --disable-installer main
lualatex --disable-installer main
```
`--disable-installer` makes a missing MiKTeX package an error instead of a hanging prompt.

## Packages (MiKTeX)
fontspec, unicode-math, babel (hebrew, english), titlesec, titletoc, enumitem, booktabs, colortbl, tabularx, caption,
placeins, microtype, csquotes, tikz, tcolorbox (listings, skins, breakable), listings, xkeyval, etoolbox, iftex,
hyperref, geometry, amsmath, biblatex, biblatex-ieee, biber, and the fonts in `fonts/`.
Not needed: `lastpage` and `needspace` (the class has its own).

## Rules the class enforces
* Hebrew only inside `hebrewpage` or `\foreignlanguage{hebrew}{..}`; units (`\pct`, `\usd`, `\ils`) never contain Hebrew.
* Never fix spacing, fonts or colours in a chapter: ask fix-se to fix the class and bump its version.
* Tables: columns without `@{}`. Code boxes: real files from `python/`, 80 characters per line at most.
