%% closettwin.cls -- ClosetTwin business-plan report class (owner: fix-se)
%% LuaLaTeX only.  Build from the project root:  lualatex --disable-installer main
\NeedsTeXFormat{LaTeX2e}[2025/11/01]
\ProvidesClass{closettwin}[2026/11/18 v0.2 ClosetTwin report class]

\RequirePackage{iftex}
\ifluatex\else\ClassError{closettwin}{LuaLaTeX is required}{Compile with lualatex.}\fi

%%% ---------- base class -------------------------------------------------
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions\relax
\LoadClass[a4paper,11pt,oneside]{book}

%%% ---------- geometry (PRD 4: text width 15.0 cm) ------------------------
\RequirePackage[a4paper,left=3cm,right=3cm,top=3.6cm,bottom=3cm,
  headheight=14pt,headsep=0.9cm,footskip=1.2cm]{geometry}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0.6em plus 0.1em minus 0.05em}
\linespread{1.0}% 11/15.5 pt is set below
\AtBeginDocument{\fontsize{11}{15.5}\selectfont}
\renewcommand{\normalsize}{\@setfontsize\normalsize{11}{15.5}}
\renewcommand{\small}{\@setfontsize\small{9.5}{13}}
\renewcommand{\footnotesize}{\@setfontsize\footnotesize{8.5}{11.5}}
\renewcommand{\large}{\@setfontsize\large{13}{17}}
\renewcommand{\Large}{\@setfontsize\Large{16}{20}}
\renewcommand{\LARGE}{\@setfontsize\LARGE{20}{25}}
\raggedbottom
\emergencystretch=2em

%%% ---------- colours (PRD 5.1) ------------------------------------------
\RequirePackage{xcolor}
\definecolor{ink}{HTML}{111111}
\definecolor{ivory}{HTML}{F7F3EE}
\definecolor{mocha}{HTML}{A47864}
\definecolor{powderpink}{HTML}{E8C6C0}
\definecolor{mochadeep}{HTML}{6B4B3D}
\definecolor{mochapale}{HTML}{D3BBAE}
\definecolor{gridgray}{HTML}{E3DCD4}
\definecolor{mutedgray}{HTML}{6F6862}
\color{ink}

%%% ---------- language and BiDi (feasibility study sec. 3) -----------------
\RequirePackage[english,bidi=basic]{babel}
\babelprovide[import,main]{english}
\babelprovide[import,onchar=ids fonts]{hebrew}

%%% ---------- fonts, loaded by path from fonts/ (PRD 4) -------------------
\RequirePackage{fontspec}
% Build from the project root; tests in fix/tests set \ctfontdir before \documentclass.
\providecommand*{\ctfontdir}{./fonts/}
\defaultfontfeatures{Path=\ctfontdir,Extension=.ttf}
\setmainfont{Rubik-Regular}[BoldFont=Rubik-Bold,ItalicFont=Rubik-Italic,
  BoldItalicFont=Rubik-BoldItalic,Numbers=Lining]
\babelfont{rm}{Rubik-Regular}[BoldFont=Rubik-Bold,ItalicFont=Rubik-Italic,
  BoldItalicFont=Rubik-BoldItalic,Numbers=Lining]
% Playfair Display (English headings only; it has NO Hebrew glyphs)
\newfontfamily\ctheadfont{PlayfairDisplay-Regular}[BoldFont=PlayfairDisplay-Bold,
  ItalicFont=PlayfairDisplay-Italic,BoldItalicFont=PlayfairDisplay-BoldItalic,Numbers=Lining]
% Rubik Medium for emphasis
\newfontfamily\ctmediumfont{Rubik-Medium}
% Code font: only inside pythonbox (see S2.4)
\newfontfamily\ctcodefont{JetBrainsMono-Regular}[BoldFont=JetBrainsMono-Bold,
  ItalicFont=JetBrainsMono-Italic,BoldItalicFont=JetBrainsMono-BoldItalic,Scale=0.85]

%%% ---------- maths: LM Math for symbols only, Rubik for letters/digits ---
\RequirePackage{amsmath}
\RequirePackage{unicode-math}
\setmathfont{latinmodern-math.otf}[Path={},Extension={}]
\setmathfont{Rubik-Regular}[Path=\ctfontdir,Extension=.ttf,
  range={up/{Latin,latin,num}},Scale=MatchLowercase]
\setmathfont{Rubik-Bold}[Path=\ctfontdir,Extension=.ttf,
  range={bfup/{Latin,latin,num}},Scale=MatchLowercase]

%%% ---------- typography --------------------------------------------------
\RequirePackage{microtype}
\RequirePackage{csquotes}

%%% ---------- a missing glyph is an ERROR, not a warning (RT-F4) ----------
\AtBeginDocument{\tracinglostchars=3 }

%%% ================= v0.2: BiDi rules, hebrewpage, \pct \usd \ils ==========
% Heading font: Playfair for English, Rubik for Hebrew (Playfair has no Hebrew).
\newcommand*{\ctheadingfont}{\iflanguage{hebrew}{\normalfont\bfseries}{\ctheadfont\bfseries}}
% Numbers + units kept in one unbreakable run
\newcommand*{\pct}[1]{\mbox{#1\%}}
\newcommand*{\usd}[1]{\mbox{\textdollar #1}}
\newcommand*{\ils}[1]{\iflanguage{hebrew}%
  {\mbox{#1\,{\char"05E9}{\char"05F4}{\char"05D7}}}{\mbox{{\char"20AA}\,#1}}}
% The one Hebrew page: RTL, ragged (no Hebrew hyphenation), Rubik everywhere.
\newenvironment{hebrewpage}
  {\clearpage\begin{otherlanguage}{hebrew}\raggedleft\setlength{\parskip}{0.7em}}
  {\end{otherlanguage}\clearpage}
% Hebrew headings (Rubik Bold, never Playfair): use inside hebrewpage
\newcommand*{\hebtitle}[1]{{\normalfont\bfseries\fontsize{26}{32}\selectfont #1\par}\vspace{0.6em}}
\newcommand*{\hebsubtitle}[1]{{\normalfont\bfseries\fontsize{13}{18}\selectfont #1\par}\vspace{0.2em}}

\endinput
