%% closettwin.cls -- ClosetTwin business-plan report class (owner: fix-se)
%% LuaLaTeX only.  Build from the project root:  lualatex --disable-installer main
\NeedsTeXFormat{LaTeX2e}[2025/11/01]
\ProvidesClass{closettwin}[2026/11/19 v0.12 ClosetTwin report class]

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

%%% ---------- maths: Latin Modern Math only inside formulas ---
\RequirePackage{amsmath}
\RequirePackage{unicode-math}
\setmathfont{latinmodern-math.otf}[Path={},Extension={}]
% (v0.7) math is uniformly Latin Modern Math (letters, digits, \mathrm). Text-mode \pct etc. stay Rubik.
\AddToHook{begindocument/end}{\let\mathrm\symup \let\mathbf\symbfup \let\mathit\symit}

%%% ---------- typography --------------------------------------------------
\RequirePackage{microtype}
\RequirePackage{csquotes}

%%% ---------- a missing glyph is an ERROR, not a warning (RT-F4) ----------
\AtBeginDocument{\tracinglostchars=3 }

%%% ================= v0.2: BiDi rules, hebrewpage, \pct \usd \ils ==========
% Heading font: Playfair for English, Rubik for Hebrew (Playfair has no Hebrew).
\RequirePackage{etoolbox}
\newcommand*{\ctheadingfont}{\ifdefstring{\languagename}{hebrew}{\normalfont\bfseries}{\ctheadfont\bfseries}}
% Numbers + units kept in one unbreakable run
\newcommand*{\pct}[1]{\mbox{#1\%}}
\newcommand*{\usd}[1]{\mbox{\textdollar #1}}
\newcommand*{\ils}[1]{\ifdefstring{\languagename}{hebrew}%
  {\mbox{#1\,{\char"05E9}{\char"05F4}{\char"05D7}}}{\mbox{{\char"20AA}\,#1}}}
% The one Hebrew page: RTL, ragged (no Hebrew hyphenation), Rubik everywhere.
\newenvironment{hebrewpage}
  {\clearpage\begin{otherlanguage}{hebrew}\ct@hebfoottrue\raggedright\setlength{\parskip}{0.7em}\ct@hebrewlists}
  {\clearpage\end{otherlanguage}\clearpage}
% Hebrew headings (Rubik Bold, never Playfair): use inside hebrewpage
% v0.8: Hebrew opener = same language as the English chapter opener (mocha rule, large title, same rhythm)
\newcommand*{\hebtitle}[1]{\vspace*{108.7pt}{\noindent\color{mocha}\rule{3cm}{0.6pt}\par}\vspace{0.45em}%
  {\normalfont\ctmediumfont\fontsize{30}{38}\selectfont #1\par}\vspace{1.1cm}}
\newcommand*{\hebsubtitle}[1]{{\normalfont\bfseries\fontsize{13}{18}\selectfont #1\par}\vspace{0.2em}}

%%% ================= v0.3: headings, numbering, TOC, lists ================
\RequirePackage{etoolbox}
\RequirePackage{titlesec}
\RequirePackage{titletoc}
\setcounter{secnumdepth}{2}
\setcounter{tocdepth}{1}
% chapter opener: large mocha number, thin rule, generous space above
\newcommand*{\ctchapterhead}[1]{%
  {\color{mocha}\ctheadfont\fontsize{54}{54}\selectfont\thechapter\par}\vspace{0.35em}%
  {\color{mocha}\rule{3cm}{0.6pt}\par}\vspace{0.9em}%
  {\ctheadfont\bfseries\fontsize{28}{34}\selectfont\raggedright #1\par}}
\newcommand*{\ctchapterheadstar}[1]{%
  {\color{mocha}\rule{3cm}{0.6pt}\par}\vspace{0.9em}%
  {\ctheadfont\bfseries\fontsize{28}{34}\selectfont\raggedright #1\par}}
\titleformat{\chapter}[block]{}{}{0pt}{\ctchapterhead}
\titleformat{name=\chapter,numberless}[block]{}{}{0pt}{\ctchapterheadstar}
\titlespacing*{\chapter}{0pt}{1.6cm}{1.4cm}
\titleformat{\section}{\ctheadingfont\fontsize{16}{20}\selectfont\raggedright}
  {\color{mochadeep}\thesection}{0.8em}{}
\titlespacing*{\section}{0pt}{2.0ex plus 0.5ex minus 0.2ex}{0.8ex plus 0.2ex}
\titleformat{\subsection}{\ctheadingfont\fontsize{12.5}{16}\selectfont\raggedright}
  {\color{mochadeep}\thesubsection}{0.7em}{}
\titlespacing*{\subsection}{0pt}{1.6ex plus 0.4ex minus 0.2ex}{0.5ex plus 0.1ex}
% banner/running-head chapter name (also for unnumbered chapters)
\renewcommand*{\chaptermark}[1]{\markboth{#1}{#1}}
\newcommand*{\ctunnumbered}[1]{\chapter*{#1}\markboth{#1}{#1}%
  \addcontentsline{toc}{chapter}{#1}}
% table of contents and lists
\renewcommand*{\contentsname}{Contents}
\renewcommand*{\listfigurename}{List of figures}
\renewcommand*{\listtablename}{List of tables}
\titlecontents{chapter}[0pt]{\addvspace{0.9em}\bfseries}
  {\color{mochadeep}\contentslabel{2.2em}}{\hspace*{-2.2em}}
  {\hfill\contentspage}[\addvspace{0.1em}]
\titlecontents{section}[2.2em]{\small}
  {\contentslabel{2.4em}}{\hspace*{-2.4em}}
  {\titlerule*[5pt]{\color{mochapale}.}\contentspage}
\titlecontents{figure}[0pt]{\small}
  {\makebox[2.6em][l]{\thecontentslabel}}{\hspace*{-2.6em}}
  {\titlerule*[5pt]{\color{mochapale}.}\contentspage}
\titlecontents{table}[0pt]{\small}
  {\makebox[2.6em][l]{\thecontentslabel}}{\hspace*{-2.6em}}
  {\titlerule*[5pt]{\color{mochapale}.}\contentspage}
\renewcommand*{\tableofcontents}{\ctunnumberednotoc{\contentsname}\@starttoc{toc}\clearpage}
\renewcommand*{\listoffigures}{\ctunnumberednotoc{\listfigurename}\@starttoc{lof}\clearpage}
\renewcommand*{\listoftables}{\ctunnumberednotoc{\listtablename}\@starttoc{lot}\clearpage}
\newcommand*{\ctunnumberednotoc}[1]{\chapter*{#1}\markboth{#1}{#1}}
% lists
\RequirePackage{enumitem}
\setlist[itemize]{label=\textcolor{mocha}{\textbullet},leftmargin=1.6em,labelwidth=1.1em,labelsep=0.5em,align=left,itemsep=0.2em,topsep=0.3em,parsep=0pt}
\setlist[enumerate]{label=\textcolor{mochadeep}{\arabic*.},leftmargin=1.6em,labelwidth=1.1em,labelsep=0.5em,align=left,itemsep=0.2em,topsep=0.3em,parsep=0pt}

%%% ================= v0.4: tables, captions, devices, TikZ keys ===========
\colorlet{pink}{powderpink}   % alias used by art-se: ONE definition, powderpink
\colorlet{muted}{mutedgray}  % alias used by art-se
\RequirePackage{array,colortbl,booktabs,tabularx}
\setlength{\heavyrulewidth}{0.8pt}
\setlength{\lightrulewidth}{0.4pt}
\setlength{\cmidrulewidth}{0.4pt}
\renewcommand*{\arraystretch}{1.25}
\setlength{\tabcolsep}{6pt}
% right-aligned numeric column and header row (ivory fill)
\newcolumntype{R}{>{\raggedleft\arraybackslash}X}
\newcommand*{\ctheaderrow}{\rowcolor{ivory}}% band overhangs by \tabcolsep: write columns WITHOUT @{} and it ends exactly at the rules
\newcommand*{\cthead}[1]{\textbf{#1}}
% captions: label in mocha-deep bold, text ink; table caption above, figure caption below
\RequirePackage[font=small,labelfont={bf,color=mochadeep},labelsep=period,
  justification=raggedright,singlelinecheck=false,skip=6pt]{caption}
\captionsetup[table]{position=above}
\captionsetup[figure]{position=below}
% floats must never drift past a chapter end
\RequirePackage{placeins}
\newcommand*{\ctchapterend}{\FloatBarrier}
\renewcommand*{\topfraction}{0.85}
\renewcommand*{\bottomfraction}{0.7}
\renewcommand*{\textfraction}{0.15}
\renewcommand*{\floatpagefraction}{0.7}
\setcounter{topnumber}{2}\setcounter{bottomnumber}{1}\setcounter{totalnumber}{3}
\setlength{\textfloatsep}{16pt plus 4pt minus 4pt}
\setlength{\intextsep}{16pt plus 4pt minus 4pt}
% assumption tags: S = sourced, D = derived, A = assumed (PRD RT-W8/RT-Q6)
\newcommand*{\ct@tag}[1]{\textsuperscript{\color{mochadeep}\bfseries\scriptsize #1}}
\newcommand*{\sourced}[1]{#1\ct@tag{S}}
\newcommand*{\derived}[1]{#1\ct@tag{D}}
\newcommand*{\assumed}[1]{#1\ct@tag{A}}
\newcommand*{\assumption}[1]{\assumed{#1}}
\newcommand*{\ctlegend}{{\small\color{mutedgray}\textsuperscript{S} sourced \quad
  \textsuperscript{D} derived \quad \textsuperscript{A} assumption}}
% TikZ (diagrams drawn at the text width; keys requested by art-se, T2.5)
\RequirePackage{tikz}
\usetikzlibrary{arrows.meta,positioning,calc,shapes.geometric,fit,backgrounds}
\newcommand*{\ctsmallfont}{\fontsize{8}{10}\selectfont}
\tikzset{
  every picture/.append style={font=\ctsmallfont,text=ink,line width=0.6pt,draw=ink,
    node distance=12mm,rounded corners=0pt},
  ct node/.style={rectangle,minimum height=8mm,minimum width=20mm,inner sep=5pt,draw=ink,
    line width=0.6pt,fill=white,text=ink,align=center,rounded corners=2pt},
  ct node ivory/.style={ct node,fill=ivory,draw=mochapale,line width=0.4pt},
  ct node pink/.style={ct node,fill=pink},
  ct key/.style={ct node,fill=ink,text=ivory},
  ct decision/.style={ct node,draw=mocha},
  ct arrow/.style={-{Stealth[length=4pt]},line width=0.6pt,draw=ink},
  ct guide/.style={line width=0.4pt,draw=muted,dashed},
  ct label/.style={font=\ctsmallfont,text=ink,inner sep=2pt},
  ct title/.style={font=\ctheadfont\fontsize{11}{13}\selectfont,text=ink},
  ct bar/.style={rectangle,minimum height=4mm,draw=ink,line width=0.6pt,fill=mocha},
  ct bar milestone/.style={diamond,minimum height=3mm,minimum width=3mm,inner sep=0pt,draw=ink,fill=ink},
  ct cell 1/.style={rectangle,draw=ink,line width=0.4pt,fill=pink,text=ink,align=center},
  ct cell 2/.style={rectangle,draw=ink,line width=0.4pt,fill=mochapale,text=ink,align=center},
  ct cell 3/.style={rectangle,draw=ink,line width=0.4pt,fill=mocha,text=ink,align=center},
  ct cell 4/.style={rectangle,draw=ink,line width=0.4pt,fill=mochadeep,text=ivory,align=center},
  ct cell 5/.style={rectangle,draw=ink,line width=0.4pt,fill=ink,text=ivory,align=center},
}
% boxes: stat card, pull quote, code box
\RequirePackage{xkeyval}
\RequirePackage[most]{tcolorbox}
\tcbuselibrary{listings,skins,breakable}
% code size from the measure: 80 characters = text width minus box padding and the number column (31.6pt)
\newdimen\ct@measure \AtBeginDocument{\ct@measure=\textwidth}% tcolorbox shrinks \textwidth inside the box
\newcommand*{\ct@codesize}{\fontsize{\strip@pt\dimexpr(\ct@measure-31.6pt)*25/1030\relax}{12.5}\selectfont}
\newcommand*{\ct@numsize}{\fontsize{\strip@pt\dimexpr(\ct@measure-31.6pt)*20/1030\relax}{12.5}\selectfont}
% Keep a box with the line(s) before it, so a box is never alone at the top of a page
% (the preceding line moves with it; a stat card / quote is never split).
% minimal \Needspace (the needspace package is not installed): break the page if less than #1 is left
\newcommand*{\Needspace}[1]{\par\begingroup\dimen@=#1\relax
  \ifdim\pagegoal<\maxdimen\ifdim\dimexpr\pagegoal-\pagetotal\relax<\dimen@\endgroup\pagebreak[4]\else\endgroup\fi\else\endgroup\fi}
\newcommand*{\ctkeepprev}{\par\nopagebreak[4]}
% \statcard{big number}{one-line claim}{source}
\newcommand*{\statcard}[3]{\ctkeepprev
  \begin{tcolorbox}[enhanced,breakable=false,colback=ivory,colframe=mochapale,boxrule=0.4pt,
    arc=0pt,left=14pt,right=14pt,top=10pt,bottom=10pt,before skip=12pt,after skip=12pt]
  {\color{mocha}\ctheadfont\bfseries\fontsize{34}{38}\selectfont #1\par}\vspace{2pt}
  {\color{ink}\fontsize{11}{15}\selectfont #2\par}\vspace{3pt}
  {\color{mutedgray}\footnotesize #3\par}
  \end{tcolorbox}}
% \pullquote{text}{attribution}
\newcommand*{\pullquote}[2]{\ctkeepprev
  \begin{tcolorbox}[enhanced,breakable=false,colback=white,frame hidden,boxrule=0pt,arc=0pt,
    borderline west={3pt}{0pt}{powderpink},left=16pt,right=6pt,top=6pt,bottom=6pt,
    before skip=12pt,after skip=12pt]
  {\ctheadfont\itshape\fontsize{14}{20}\selectfont #1\par}\vspace{4pt}
  {\color{mutedgray}\footnotesize #2\par}
  \end{tcolorbox}}
% insight box (ivory, hairline, small mocha-deep label); never split: keep it shorter than half a page
\NewDocumentEnvironment{insightbox}{O{Insight}}
  {\ctkeepprev\begin{tcolorbox}[enhanced,breakable=false,colback=ivory,colframe=mochapale,boxrule=0.4pt,
    arc=0pt,left=14pt,right=14pt,top=9pt,bottom=9pt,before skip=12pt,after skip=12pt,
    before upper={{\color{mochadeep}\bfseries\fontsize{8}{10}\selectfont\MakeUppercase{#1}\par}\vspace{4pt}},
    parskip=0.5em]}
  {\end{tcolorbox}}
% \pythonbox[first=N,last=M]{python/file.py}: shows the REAL file (never pasted code), LTR,
% ivory fill + 0.4pt hairline, JetBrains Mono, line numbers = file line numbers, long lines wrap
% inside the box.  The only place the code font is used.  (the font family is scaled 0.85,
% so 9.5pt below is 8.1pt real: about 82 characters per line at the text width)
\lstdefinestyle{ctpython}{language=Python,basicstyle=\ctcodefont\ct@codesize,
  numbers=left,numberstyle=\ctcodefont\ct@numsize\color{mocha!80},
  numbersep=8pt,breaklines=true,breakatwhitespace=false,columns=fullflexible,keepspaces=true,
  showstringspaces=false,tabsize=4,frame=none,extendedchars=true,
  keywordstyle=\color{mochadeep}\bfseries,commentstyle=\color{mutedgray},
  stringstyle=\color{ink}}
\define@key{ctpy}{first}{\def\ct@pyfirst{#1}}
\define@key{ctpy}{last}{\def\ct@pylast{#1}}
% number of lines of the box = min(last, file length) - first + 1; a box of at most
% \ct@pysplitmax lines is never split across pages, a longer one (Appendix A) may break.
\newcommand*{\ct@pysplitmax}{15}
\newcommand*{\pythonbox}[2][]{%
  \begingroup
  \def\ct@pyfirst{1}\def\ct@pylast{100000}\setkeys{ctpy}{#1}%
  \edef\ct@pytotal{\directlua{local n=0 for _ in io.lines("\luaescapestring{#2}") do n=n+1 end tex.sprint(n)}}%
  \ifnum\ct@pylast>\ct@pytotal\relax\edef\ct@pylast{\ct@pytotal}\fi
  \ifnum\numexpr\ct@pylast-\ct@pyfirst+1\relax>\ct@pysplitmax\relax
    \def\ct@pybreak{breakable}\else\def\ct@pybreak{unbreakable}\fi
  \begin{otherlanguage}{english}% always left-to-right, even if called inside hebrewpage
  \ctkeepprev\tcbinputlisting{listing file={#2},listing only,enhanced,\ct@pybreak,colback=ivory,
    colframe=mochapale,boxrule=0.4pt,arc=0pt,left=24pt,right=4pt,top=6pt,bottom=6pt,
    listing options={style=ctpython,firstline=\ct@pyfirst,lastline=\ct@pylast,firstnumber=\ct@pyfirst},
    before skip=10pt,after skip=10pt}%
  \end{otherlanguage}%
  \endgroup}

%%% ================= v0.5: cover, banner, footer, matter ===================
% Cover fields: main.tex sets these macros (NO ID numbers anywhere).
\newcommand*{\cttitle}[1]{\gdef\ct@title{#1}}
\newcommand*{\ctsubtitle}[1]{\gdef\ct@subtitle{#1}}
\newcommand*{\ctauthors}[1]{\gdef\ct@authors{#1}}
\newcommand*{\ctgroup}[1]{\gdef\ct@group{#1}}
\newcommand*{\ctcourse}[1]{\gdef\ct@course{#1}}
\newcommand*{\ctlecturer}[1]{\gdef\ct@lecturer{#1}}
\newcommand*{\ctdate}[1]{\gdef\ct@date{#1}}
\newcommand*{\ctbrand}[1]{\gdef\ct@brand{#1}}\ctbrand{ClosetTwin}% brand name (banner/footer/cover)
\newcommand*{\ctbrandline}[1]{\gdef\ct@brandline{#1}}\ctbrandline{}% optional footer tagline
% footer wording per language (override in main.tex if needed)
\newcommand*{\ctpageword}{Page}\newcommand*{\ctofword}{of}
\newcommand*{\cthebpageword}{עמוד}\newcommand*{\cthebofword}{מתוך}
\cttitle{ClosetTwin}\ctsubtitle{}\ctauthors{}\ctgroup{}\ctcourse{}\ctlecturer{}\ctdate{\today}
\newcommand*{\ct@coverline}[2]{\ifx\relax#2\relax\else{\color{mochadeep}\fontsize{8}{10}\selectfont\MakeUppercase{#1}}\\[1pt]
  {\fontsize{11}{15}\selectfont #2}\\[9pt]\fi}
\newcommand*{\ctmakecover}{%
  \begingroup
  \pagecolor{ivory}\thispagestyle{empty}
  \noindent{\ctheadfont\bfseries\fontsize{15}{18}\selectfont\ct@brand}\hspace{8pt}%
  \raisebox{0.3ex}{\color{powderpink}\rule{1.4cm}{4pt}}\par
  \vspace*{3.2cm}
  {\color{mocha}\rule{3cm}{0.8pt}\par}\vspace{1.2em}
  {\ctheadfont\bfseries\fontsize{44}{50}\selectfont\raggedright\ct@title\par}\vspace{1em}
  {\ctheadfont\itshape\fontsize{18}{25}\selectfont\raggedright\ct@subtitle\par}
  \vfill
  \begin{minipage}{0.7\textwidth}\raggedright\setlength{\parskip}{0pt}
  \ct@coverline{Authors}{\ct@authors}%
  \ct@coverline{Group}{\ct@group}%
  \ct@coverline{Course}{\ct@course}%
  \ct@coverline{Lecturer}{\ct@lecturer}%
  \ct@coverline{Date}{\ct@date}%
  \end{minipage}
  \clearpage
  \endgroup
  \nopagecolor}
% banner (inset to the text block, no fill) and footer (hairline + page number), via the page style
\setlength{\headheight}{18pt}
\newcommand*{\ctbanner}{%
  \vbox to 18pt{\vss
    \hbox to \textwidth{\foreignlanguage{english}{{\ctheadfont\bfseries\fontsize{13}{14}\selectfont\color{ink}\ct@brand}%
      \hspace{8pt}\raisebox{0.4ex}{\color{powderpink}\rule{1.1cm}{3pt}}\hfill
      {\color{mochadeep}\fontsize{7.5}{9}\selectfont\MakeUppercase{\leftmark}}}}%
    \vskip 4pt
    {\color{mochadeep}\hrule width\textwidth height 0.5pt}\vss}}
% label LastPage (the lastpage package is not installed): written after the final page is shipped
\AtEndDocument{\clearpage\addtocounter{page}{-1}%
  \immediate\write\@auxout{\string\newlabel{LastPage}{{}{\thepage}{}{}{}}}\addtocounter{page}{1}}
\newif\ifct@hebfoot
% "Page N of M" (M = last page, no hard-coded total); Hebrew wording and direction on hebrewpage
\newcommand*{\ct@pageof}{%
  \ifct@hebfoot
    \foreignlanguage{hebrew}{\color{mutedgray}\cthebpageword\ {\color{ink}\bfseries\thepage}\ \cthebofword\ \pageref*{LastPage}}%
  \else
    {\color{mutedgray}\ctpageword}\ {\color{ink}\bfseries\thepage}\ {\color{mutedgray}\ctofword}\ \pageref*{LastPage}%
  \fi}

\newcommand*{\ctfooter}{%
  \vtop{\hbox to \textwidth{\color{mochadeep}\leaders\hrule height 0.4pt\hfill}\vskip 6pt
    \hbox to \textwidth{\foreignlanguage{english}{{\ctheadfont\bfseries\fontsize{9}{11}\selectfont\color{ink}\ct@brand}%
      \ifx\ct@brandline\@empty\else\hspace{6pt}{\color{mutedgray}\fontsize{8}{11}\selectfont\ct@brandline}\fi
      }\hfill\fontsize{9}{11}\selectfont\ct@pageof}}}
\def\ps@closettwin{%
  \let\@mkboth\markboth
  \def\@oddhead{\ctbanner}\let\@evenhead\@oddhead
  \def\@oddfoot{\ctfooter}\let\@evenfoot\@oddfoot}
\let\ps@plain\ps@closettwin
\pagestyle{closettwin}
\setlength{\footskip}{18pt}% the footer is a \vtop: its rule sits 18pt under the text block
% the Hebrew page sets the banner's chapter-name slot to its Hebrew title
\renewenvironment{hebrewpage}[1][]
  {\clearpage\markboth{\ctmediumfont\fontsize{9.5}{9.5}\selectfont #1}{\ctmediumfont\fontsize{9.5}{9.5}\selectfont #1}\begin{otherlanguage}{hebrew}\ct@hebfoottrue\raggedright\setlength{\parskip}{0.7em}\ct@hebrewlists}
  {\clearpage\end{otherlanguage}\clearpage}
% RTL lists: the physical indent is on the left, so mirror it to the right
\newcommand*{\ct@hebrewlists}{\setlist[itemize]{label=\makebox[1.1em][l]{\textcolor{mocha}{\textbullet}},leftmargin=0pt,rightmargin=1.6em,labelsep=0.5em}\setlist[enumerate]{label=\makebox[1.1em][l]{\textcolor{mochadeep}{\arabic*.}},leftmargin=0pt,rightmargin=1.6em,labelsep=0.5em}}
% no widows/orphans; floats never take a page of their own unless nearly full
\clubpenalty=10000 \widowpenalty=10000 \displaywidowpenalty=10000
\renewcommand*{\fps@figure}{tbp}\renewcommand*{\fps@table}{tbp}
% every chapter flushes its floats first
\preto\chapter{\FloatBarrier}
% hyperref last: palette colours only, no boxes
\RequirePackage[colorlinks=true,linkcolor=mochadeep,citecolor=mochadeep,urlcolor=mochadeep,
  bookmarksnumbered=true,unicode=true,pdfusetitle=false]{hyperref}
\urlstyle{same}

\endinput
