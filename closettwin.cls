%% closettwin.cls -- ClosetTwin business-plan report class (owner: fix-se)
%% LuaLaTeX only.  Build from the project root:  lualatex --disable-installer main
\NeedsTeXFormat{LaTeX2e}[2025/11/01]
\ProvidesClass{closettwin}[2026/11/18 v0.5 ClosetTwin report class]

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
\RequirePackage{etoolbox}
\newcommand*{\ctheadingfont}{\ifdefstring{\languagename}{hebrew}{\normalfont\bfseries}{\ctheadfont\bfseries}}
% Numbers + units kept in one unbreakable run
\newcommand*{\pct}[1]{\mbox{#1\%}}
\newcommand*{\usd}[1]{\mbox{\textdollar #1}}
\newcommand*{\ils}[1]{\ifdefstring{\languagename}{hebrew}%
  {\mbox{#1\,{\char"05E9}{\char"05F4}{\char"05D7}}}{\mbox{{\char"20AA}\,#1}}}
% The one Hebrew page: RTL, ragged (no Hebrew hyphenation), Rubik everywhere.
\newenvironment{hebrewpage}
  {\clearpage\begin{otherlanguage}{hebrew}\raggedleft\setlength{\parskip}{0.7em}}
  {\end{otherlanguage}\clearpage}
% Hebrew headings (Rubik Bold, never Playfair): use inside hebrewpage
\newcommand*{\hebtitle}[1]{{\normalfont\bfseries\fontsize{26}{32}\selectfont #1\par}\vspace{0.6em}}
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
\setlist[itemize]{label=\textcolor{mocha}{\textbullet},leftmargin=1.4em,itemsep=0.2em,topsep=0.3em,parsep=0pt}
\setlist[enumerate]{label=\textcolor{mochadeep}{\arabic*.},leftmargin=1.6em,itemsep=0.2em,topsep=0.3em,parsep=0pt}

%%% ================= v0.4: tables, captions, devices, TikZ keys ===========
\definecolor{pink}{HTML}{E8C6C0}   % alias used by art-se
\definecolor{muted}{HTML}{6F6862}  % alias used by art-se
\RequirePackage{array,colortbl,booktabs,tabularx}
\setlength{\heavyrulewidth}{0.8pt}
\setlength{\lightrulewidth}{0.4pt}
\setlength{\cmidrulewidth}{0.4pt}
\renewcommand*{\arraystretch}{1.25}
\setlength{\tabcolsep}{6pt}
% right-aligned numeric column and header row (ivory fill)
\newcolumntype{R}{>{\raggedleft\arraybackslash}X}
\newcommand*{\ctheaderrow}{\rowcolor{ivory}}
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
\RequirePackage[most]{tcolorbox}
\tcbuselibrary{listings,skins,breakable}
% \statcard{big number}{one-line claim}{source}
\newcommand*{\statcard}[3]{%
  \begin{tcolorbox}[enhanced,breakable=false,colback=ivory,colframe=mochapale,boxrule=0.4pt,
    arc=0pt,left=14pt,right=14pt,top=10pt,bottom=10pt,before skip=12pt,after skip=12pt]
  {\color{mocha}\ctheadfont\bfseries\fontsize{34}{38}\selectfont #1\par}\vspace{2pt}
  {\color{ink}\fontsize{11}{15}\selectfont #2\par}\vspace{3pt}
  {\color{mutedgray}\footnotesize #3\par}
  \end{tcolorbox}}
% \pullquote{text}{attribution}
\newcommand*{\pullquote}[2]{%
  \begin{tcolorbox}[enhanced,breakable=false,colback=white,frame hidden,boxrule=0pt,arc=0pt,
    borderline west={3pt}{0pt}{powderpink},left=16pt,right=6pt,top=6pt,bottom=6pt,
    before skip=12pt,after skip=12pt]
  {\ctheadfont\itshape\fontsize{14}{20}\selectfont #1\par}\vspace{4pt}
  {\color{mutedgray}\footnotesize #2\par}
  \end{tcolorbox}}
% \pythonbox[first line]{last line}? no: \pythonbox{python/file.py}  (reads the real file)
\lstdefinestyle{ctpython}{language=Python,basicstyle=\ctcodefont\fontsize{7.5}{9.5}\selectfont,
  numbers=left,numberstyle=\ctcodefont\fontsize{6.5}{9.5}\selectfont\color{mutedgray},
  numbersep=8pt,breaklines=true,breakatwhitespace=false,columns=fullflexible,keepspaces=true,
  showstringspaces=false,tabsize=4,frame=none,extendedchars=true,
  keywordstyle=\color{mochadeep}\bfseries,commentstyle=\color{mutedgray},
  stringstyle=\color{ink}}
\newcommand*{\pythonbox}[1]{%
  \tcbinputlisting{listing file={#1},listing only,enhanced,breakable,colback=ivory,
    colframe=mochapale,boxrule=0.4pt,arc=0pt,left=22pt,right=6pt,top=6pt,bottom=6pt,
    listing options={style=ctpython},before skip=10pt,after skip=10pt}}

%%% ================= v0.5: cover, banner, footer, matter ===================
% Cover fields: main.tex sets these macros (NO ID numbers anywhere).
\newcommand*{\cttitle}[1]{\gdef\ct@title{#1}}
\newcommand*{\ctsubtitle}[1]{\gdef\ct@subtitle{#1}}
\newcommand*{\ctauthors}[1]{\gdef\ct@authors{#1}}
\newcommand*{\ctgroup}[1]{\gdef\ct@group{#1}}
\newcommand*{\ctcourse}[1]{\gdef\ct@course{#1}}
\newcommand*{\ctlecturer}[1]{\gdef\ct@lecturer{#1}}
\newcommand*{\ctdate}[1]{\gdef\ct@date{#1}}
\cttitle{ClosetTwin}\ctsubtitle{}\ctauthors{}\ctgroup{}\ctcourse{}\ctlecturer{}\ctdate{\today}
\newcommand*{\ct@coverline}[2]{\ifx\relax#2\relax\else{\color{mochadeep}\fontsize{8}{10}\selectfont\MakeUppercase{#1}}\\[1pt]
  {\fontsize{11}{15}\selectfont #2}\\[9pt]\fi}
\newcommand*{\ctmakecover}{%
  \begingroup
  \pagecolor{ivory}\thispagestyle{empty}
  \noindent{\ctheadfont\bfseries\fontsize{15}{18}\selectfont ClosetTwin}\hspace{8pt}%
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
  \nopagecolor
  \setcounter{page}{1}}
% banner (inset to the text block, no fill) and footer (hairline + page number), via the page style
\setlength{\headheight}{18pt}
\newcommand*{\ctbanner}{%
  \vbox to 18pt{\vss
    \hbox to \textwidth{{\ctheadfont\bfseries\fontsize{13}{14}\selectfont\color{ink}ClosetTwin}%
      \hspace{8pt}\raisebox{0.4ex}{\color{powderpink}\rule{1.1cm}{3pt}}\hfill
      {\color{mochadeep}\fontsize{7.5}{9}\selectfont\MakeUppercase{\leftmark}}}%
    \vskip 4pt
    {\color{ink}\hrule width\textwidth height 0.5pt}\vss}}
\newcommand*{\ctfooter}{%
  \vbox{\hbox to \textwidth{\color{mochapale}\leaders\hrule height 0.4pt\hfill}\vskip 6pt
    \hbox to \textwidth{\hfil\fontsize{9}{11}\selectfont\color{ink}\thepage\hfil}}}
\def\ps@closettwin{%
  \let\@mkboth\markboth
  \def\@oddhead{\ctbanner}\let\@evenhead\@oddhead
  \def\@oddfoot{\ctfooter}\let\@evenfoot\@oddfoot}
\let\ps@plain\ps@closettwin
\pagestyle{closettwin}
% the Hebrew page sets the banner's chapter-name slot to its Hebrew title
\renewenvironment{hebrewpage}[1][]
  {\clearpage\markboth{#1}{#1}\begin{otherlanguage}{hebrew}\raggedleft\setlength{\parskip}{0.7em}}
  {\end{otherlanguage}\clearpage}
% every chapter flushes its floats first
\preto\chapter{\FloatBarrier}
% hyperref last: palette colours only, no boxes
\RequirePackage[colorlinks=true,linkcolor=mochadeep,citecolor=mochadeep,urlcolor=mochadeep,
  bookmarksnumbered=true,unicode=true,pdfusetitle=false]{hyperref}
\urlstyle{same}

\endinput
