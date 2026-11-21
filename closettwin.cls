%% closettwin.cls -- ClosetTwin business-plan report class (owner: fix-se)
%% LuaLaTeX only.  Build from the project root:  lualatex --disable-installer main
\NeedsTeXFormat{LaTeX2e}[2025/11/01]
\ProvidesClass{closettwin}[2026/11/20 v0.23 ClosetTwin report class]

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
  ItalicFont=PlayfairDisplay-Italic,BoldItalicFont=PlayfairDisplay-BoldItalic,Numbers=Lining,Ligatures=TeX]
% Rubik Medium for emphasis
\newfontfamily\ctmediumfont{Rubik-Medium}[Ligatures=TeX]
% Code font: only inside pythonbox (see S2.4)
\newfontfamily\ctcodefont{JetBrainsMono-Regular}[BoldFont=JetBrainsMono-Bold,
  ItalicFont=JetBrainsMono-Italic,BoldItalicFont=JetBrainsMono-BoldItalic,Scale=0.85,RawFeature={-tlig;-liga;-calt}]

%%% ---------- maths: Latin Modern Math only inside formulas ---
\RequirePackage{amsmath}
\RequirePackage{unicode-math}
\setmathfont{latinmodern-math.otf}[Path={},Extension={}]
% (v0.7) math is uniformly Latin Modern Math (letters, digits, \mathrm). Text-mode \pct etc. stay Rubik.
\AddToHook{begindocument/end}{\let\mathrm\symup \let\mathbf\symbfup \let\mathit\symit}

% (v0.20) digits inside INLINE math ($r=24.4\%$ in a sentence) are set in the text font (Rubik) like every
% other number in the prose; displayed equations stay Latin Modern Math (v0.7). Each digit is an active
% math character that sets itself with \text. \everymath is not used by displays.
\newcommand*{\ct@mdig}[1]{{\text{#1}}}% a braced group: valid after _ and ^ too
\begingroup\catcode`\~=13
\def\ct@defdig#1{\lccode`\~=`#1 \lowercase{\gdef~}{\ct@mdig{#1}}}
\ct@defdig0\ct@defdig1\ct@defdig2\ct@defdig3\ct@defdig4\ct@defdig5\ct@defdig6\ct@defdig7\ct@defdig8\ct@defdig9
\endgroup
\def\ct@digsactive{\@tempcnta=48 \@whilenum\@tempcnta<58 \do{\mathcode\@tempcnta="8000 \advance\@tempcnta\@ne}}
\AtBeginDocument{\everymath\expandafter{\the\everymath\ct@digsactive}}

%%% ---------- typography --------------------------------------------------
\DeclareTextComposite{\c}{TU}{T}{"0162}\DeclareTextComposite{\c}{TU}{t}{"0163}
\RequirePackage{microtype}
% microtype.cfg lists \c T and \c t for TU, but TU has no such composites (warning on the first font): declare them
\RequirePackage{csquotes}

\AtBeginDocument{\frenchspacing}% equal word spaces: no extra space after a period ("Dr. Yoram")
%%% ---------- no-break space after abbreviations: "Dr. X" never stretches ----
% (v0.19) NO percent sign inside \directlua: TeX reads it as a comment and cuts the Lua code off
% (the rule was silently dead before). The Lua pattern characters are built from string.char(37).
\directlua{
  local pc = string.char(37)
  local nb = "\string\u{A0}"
  local abbr = {"Dr","Prof","Mr","Mrs","Ms","Fig","Eq","Sec","Ch","Tab","No"}
  luatexbase.add_to_callback("process_input_buffer", function(line)
    for _, a in ipairs(abbr) do
      local pat = pc .. "f[" .. pc .. "a]" .. a .. pc .. ". (" .. pc .. "S)"
      line = line:gsub(pat, a .. "." .. nb .. pc .. "1")
    end
    return line
  end, "closettwin.abbreviation.tie")
}
%%% ---------- a missing glyph is an ERROR, not a warning (RT-F4) ----------
\AtBeginDocument{\tracinglostchars=3 }

%%% ================= v0.2: BiDi rules, hebrewpage, \pct \usd \ils ==========
% Heading font: Playfair for English, Rubik for Hebrew (Playfair has no Hebrew).
\RequirePackage{etoolbox}
\newcommand*{\ctheadingfont}{\ifdefstring{\languagename}{hebrew}{\normalfont\bfseries}{\ctheadfont\bfseries}}
% Numbers + units kept in one unbreakable run
\newcommand*{\pct}[1]{\mbox{#1\%}}
% \range{2024}{2026}: always 2024-2026 left to right, also inside a Hebrew (RTL) paragraph
\newcommand*{\range}[2]{\mbox{\foreignlanguage{english}{#1\textendash #2}}}
\newcommand*{\usd}[1]{\mbox{\textdollar #1}}
\newcommand*{\ils}[1]{\ifdefstring{\languagename}{hebrew}%
  {\mbox{#1\,{\char"05E9}{\char"05F4}{\char"05D7}}}{\mbox{{\char"20AA}#1}}}
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
  {\noindent\ctheadfont\bfseries\fontsize{28}{34}\selectfont\raggedright #1\par}}% \noindent: the title starts exactly under the rule (v0.20)
\newcommand*{\ctchapterheadstar}[1]{{\color{mocha}\ctheadfont\fontsize{54}{54}\selectfont\phantom{0}\par}\vspace{0.35em}%
  {\color{mocha}\rule{3cm}{0.6pt}\par}\vspace{0.9em}%
  {\noindent\ctheadfont\bfseries\fontsize{28}{34}\selectfont\raggedright #1\par}}
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
% (v0.23) compact heading for an appendix that must share its page with its content (no 54pt number line,
% 22pt title, short top space): rule + title + intro + code fit on ONE page. In the contents like \ctunnumbered.
\newcommand*{\ctappendix}[1]{\clearpage\FloatBarrier\phantomsection\markboth{#1}{#1}%
  \addcontentsline{toc}{chapter}{#1}\thispagestyle{plain}%
  \vspace*{1.2cm}{\color{mocha}\rule{3cm}{0.6pt}\par}\vspace{0.7em}%
  {\noindent\ctheadfont\bfseries\fontsize{22}{26}\selectfont\raggedright #1\par}\vspace{1em}}
\newcommand*{\ctunnumbered}[1]{\chapter*{#1}\markboth{#1}{#1}%
  \addcontentsline{toc}{chapter}{#1}}
% table of contents and lists
\renewcommand*{\contentsname}{Contents}
\renewcommand*{\listfigurename}{List of figures}
\renewcommand*{\listtablename}{List of tables}
% (v0.20) chapter numbers of the contents sit INSIDE the text block (they hung 24pt into the left margin: the 'stray 1,2,3')
\titlecontents{chapter}[2.2em]{\addvspace{0.9em}\bfseries}
  {\color{mochadeep}\contentslabel{2.2em}}{\hspace*{-2.2em}}
  {\hfill\contentspage}[\addvspace{0.1em}]
\titlecontents{section}[2.2em]{\small}
  {\contentslabel{2.2em}}{\hspace*{-2.2em}}
  {\titlerule*[5pt]{\color{mochapale}.}\contentspage}
\titlecontents{figure}[0pt]{\small}
  {\makebox[2.6em][l]{\thecontentslabel}}{\hspace*{-2.6em}}
  {\titlerule*[5pt]{\color{mochapale}.}\contentspage}
\titlecontents{table}[0pt]{\small}
  {\makebox[2.6em][l]{\thecontentslabel}}{\hspace*{-2.6em}}
  {\titlerule*[5pt]{\color{mochapale}.}\contentspage}
% (v0.20) the plain babel-english names: \contentsname is wrapped by babel's ensure and shifted the title 6.5pt right
\renewcommand*{\tableofcontents}{\ctunnumberednotoc{\englishcontentsname}\@starttoc{toc}\clearpage}
\renewcommand*{\listoffigures}{\ctunnumberednotoc{\englishlistfigurename}\@starttoc{lof}\clearpage}
\renewcommand*{\listoftables}{\ctunnumberednotoc{\englishlisttablename}\@starttoc{lot}\clearpage}
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
% (v0.23) a table with ONE wide label column and n numeric columns: \ctnumcols{n}, then columns W (label,
% weight 1.6) and V (numbers, right-aligned, weight (n+1-1.6)/n so the weights add up to n+1 as tabularx needs):
%   \ctnumcols{4}\begin{tabularx}{\textwidth}{WVVVV} ... \end{tabularx}
\newcommand*{\ct@v}{0.85}
\newcommand*{\ctnumcols}[1]{\edef\ct@v{\strip@pt\dimexpr(#1pt+1pt-1.6pt)/#1\relax}}
\newcolumntype{W}{>{\hsize=1.6\hsize\raggedright\arraybackslash}X}
\newcolumntype{V}{>{\hsize=\ct@v\hsize\raggedleft\arraybackslash}X}
% (v0.20) text columns of a tabularx are ragged right: never justified, so no stretched spaces in a narrow cell
\renewcommand*{\tabularxcolumn}[1]{>{\raggedright\arraybackslash}p{#1}}
% (v0.20) the list-of-tables/figures entry of a caption without a short form stops before the first "(":
% remarks in brackets (file names, model notes) never reach the lists. \caption[short]{long} still wins.
% (v0.23) cut in Lua (no percent sign, hash or backslash-backslash inside \directlua): the entry stops before the first
% '(' or ':' or '$', so brackets, sub-titles and formulas never reach the lists
\directlua{
  function ct_capcut(s)
    local cut = string.len(s) + 1
    for _, d in ipairs({"(", ":", "$"}) do
      local i = string.find(s, d, 1, true)
      if i and i > 1 and i < cut then cut = i end
    end
    local r = string.sub(s, 1, cut - 1)
    while string.sub(r, -1) == " " do r = string.sub(r, 1, -2) end
    tex.sprint(r)
  end
}
\newcommand*{\ct@capcut}[1]{\directlua{ct_capcut("\luaescapestring{\detokenize{#1}}")}}
\AddToHook{begindocument/end}{\let\ct@origcaption\caption
\RenewDocumentCommand{\caption}{s o m}{%
  \IfBooleanTF{#1}{\ct@origcaption*{#3}}{%
    \IfNoValueTF{#2}{\ct@origcaption[\ct@capcut{#3}]{#3}}{\ct@origcaption[#2]{#3}}}}}
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
\newdimen\ctboxsep \ctboxsep=14pt% ONE gap token: floats and boxes
\setlength{\textfloatsep}{\ctboxsep plus 2pt minus 2pt}\setlength{\floatsep}{\ctboxsep plus 2pt minus 2pt}
\setlength{\intextsep}{\ctboxsep plus 2pt minus 2pt}
% (v0.22) figures are centred by the class (authors no longer write \centering)
\AtBeginEnvironment{figure}{\centering}
% (v0.22) \texttt prints in Latin Modern Mono, a font outside the palette: it is set in the text font and
% a class warning "closettwin: \texttt used" is written for every use (qa-code greps the log for it)
\AddToHook{begindocument/end}{\renewcommand*{\texttt}[1]{\ClassWarning{closettwin}{\string\texttt\space used in the text: set in the text font; remove it}#1}}
% assumption tags: S = sourced, D = derived, A = assumed (PRD RT-W8/RT-Q6)
\newcommand*{\ct@tag}[1]{\textsuperscript{\color{mochadeep}\bfseries\scriptsize #1}}
% (v0.20) inside a formula the value is set in the TEXT font (\text), never in math digits; and the
% first tagged number of the document carries the legend as a footnote (only in running text:
% a footnote is impossible inside a table, caption, box or formula, so the legend waits for the next use).
\newif\ifct@legendshown
\def\ct@docenv{document}
\newcommand*{\ct@val}[1]{\ifmmode\text{#1}\else#1\fi}
\newcommand*{\ct@firstlegend}{\ifct@legendshown\else\ifmmode\else\ifx\@currenvir\ct@docenv
  \global\ct@legendshowntrue\footnote{\ctlegend}\fi\fi\fi}
\newcommand*{\sourced}[1]{\ct@val{#1}\ct@tag{S}\ct@firstlegend}
\newcommand*{\derived}[1]{\ct@val{#1}\ct@tag{D}\ct@firstlegend}
\newcommand*{\assumed}[1]{\ct@val{#1}\ct@tag{A}\ct@firstlegend}
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
\newcommand*{\ct@numsize}{\fontsize{\strip@pt\dimexpr(\ct@measure-31.6pt)*45/2060\relax}{12.5}\selectfont}
% Keep a box with the line(s) before it, so a box is never alone at the top of a page
% (the preceding line moves with it; a stat card / quote is never split).
% minimal \Needspace (the needspace package is not installed): break the page if less than #1 is left
\newcommand*{\Needspace}[1]{\par\begingroup\dimen@=#1\relax
  \ifdim\pagegoal<\maxdimen\ifdim\dimexpr\pagegoal-\pagetotal\relax<\dimen@\endgroup\pagebreak[4]\else\endgroup\fi\else\endgroup\fi}
% ONE gap mechanism for boxes (every gap = \ctboxsep).  \lastskip and \addvspace are unreliable here
% (LuaTeX vertical list, \if@minipage left true by boxes), so a flag does the work: a box sets
% "a box was the last thing"; any paragraph resets it (callback at line breaking, so nothing the
% kernel does with \everypar can disturb it).
% * after a box: an explicit gap \ctboxsep (text that follows an explicit \vskip adds no \parskip)
% * before a box: nothing if a box was just before (its gap is already there), otherwise
%   \ctboxsep with a no-break penalty before it, so the box stays with the line above and is
%   never alone at the top of a page
\directlua{
  ct_afterbox = 0
  luatexbase.add_to_callback("pre_linebreak_filter", function(head) ct_afterbox = 0 return head end,
    "closettwin.afterbox.reset")}
\newcommand*{\ctkeepprev}{\par
  \ifnum\directlua{tex.sprint(ct_afterbox)}=1 \vskip\dimexpr\parskip\relax% tcolorbox cancels one \parskip at its start
  \else\nopagebreak[4]\vskip\ctboxsep\relax\fi
  \directlua{ct_afterbox = 0}}
\newcommand*{\ct@boxafter}{\par\vskip\ctboxsep\relax\directlua{ct_afterbox = 1}}
% \statcard{big number}{one-line claim}{source}
\newcommand*{\statcard}[3]{\ctkeepprev
  \begin{tcolorbox}[enhanced,breakable=false,colback=ivory,colframe=mochapale,boxrule=0.4pt,
    arc=0pt,left=14pt,right=14pt,top=10pt,bottom=10pt,before skip=0pt,after skip=0pt]
  {\color{mocha}\ctheadfont\bfseries\fontsize{34}{38}\selectfont #1\par}\vspace{2pt}
  {\color{ink}\fontsize{11}{15}\selectfont #2\par}\vspace{3pt}
  {\color{mutedgray}\footnotesize #3\par}
  \end{tcolorbox}\ct@boxafter}
% \pullquote{text}{attribution}
\newcommand*{\pullquote}[2]{\ctkeepprev
  \begin{tcolorbox}[enhanced,breakable=false,colback=white,frame hidden,boxrule=0pt,arc=0pt,
    borderline west={3pt}{0pt}{powderpink},left=16pt,right=6pt,top=6pt,bottom=6pt,
    before skip=0pt,after skip=0pt]
  {\ctheadfont\itshape\fontsize{14}{20}\selectfont #1\par}\vspace{4pt}
  {\color{mutedgray}\footnotesize #2\par}
  \end{tcolorbox}\ct@boxafter}
% insight box (ivory, hairline, small mocha-deep label); never split: keep it shorter than half a page
% the body is collected first (+b), so the box is typeset by ordinary macro code like \statcard:
% an environment start/end would add a hidden \parskip to the gaps
\NewDocumentEnvironment{insightbox}{O{Insight} +b}
  {\ctkeepprev\begin{tcolorbox}[enhanced,breakable=false,colback=ivory,colframe=mochapale,boxrule=0.4pt,
    arc=0pt,left=14pt,right=14pt,top=9pt,bottom=9pt,before skip=0pt,after skip=0pt]
    {\color{mochadeep}\bfseries\fontsize{8}{10}\selectfont\MakeUppercase{#1}\par}\vspace{4pt}
    \setlength{\parskip}{0.5em}#2
  \end{tcolorbox}\ct@boxafter}
  {}
% \pythonbox[first=N,last=M]{python/file.py}: shows the REAL file (never pasted code), LTR,
% ivory fill + 0.4pt hairline, JetBrains Mono, line numbers = file line numbers, long lines wrap
% inside the box.  The only place the code font is used.  (the font family is scaled 0.85,
% so 9.5pt below is 8.1pt real: about 82 characters per line at the text width)
\lstdefinestyle{ctpython}{language=Python,basicstyle=\ctcodefont\ct@codesize,
  numbers=left,numberstyle=\ctcodefont\ct@numsize\color{mochadeep!70},
  numbersep=8pt,breaklines=true,breakatwhitespace=false,columns=fullflexible,keepspaces=true,
  showstringspaces=false,tabsize=4,frame=none,extendedchars=true,breakindent=1.5em,postbreak=\mbox{\textcolor{mocha}{\textbackslash}\space},
  keywordstyle=\color{mochadeep}\bfseries,commentstyle=\color{mutedgray},
  stringstyle=\color{ink}}
\define@key{ctpy}{first}{\def\ct@pyfirst{#1}}
\define@key{ctpy}{last}{\def\ct@pylast{#1}}
% number of lines of the box = min(last, file length) - first + 1; a box of at most
% \ct@pysplitmax lines is never split across pages, a longer one (Appendix A) may break.
\newcommand*{\ct@pysplitmax}{45}% (v0.20) was 15: the 41-line Appendix A box is never split (3 lines alone on a page)
\newcommand*{\pythonbox}[2][]{%
  \begingroup
  \def\ct@pyfirst{1}\def\ct@pylast{100000}\setkeys{ctpy}{#1}%
  \edef\ct@pytotal{\directlua{local n=0 for _ in io.lines("\luaescapestring{#2}") do n=n+1 end tex.sprint(n)}}%
  \ifnum\ct@pylast>\ct@pytotal\relax\edef\ct@pylast{\ct@pytotal}\fi
  \edef\ct@pylong{\directlua{local n=0 local i=0 for l in io.lines("\luaescapestring{#2}") do i=i+1 if i>=\ct@pyfirst\space and i<=\ct@pylast\space and utf8.len(l)>80 then n=n+1 end end tex.sprint(n)}}%
  \ifnum\ct@pylong>0\ClassWarningNoLine{closettwin}{pythonbox: \ct@pylong\space line(s) of #2 are longer than 80 characters and will wrap (marked with a backslash)}\fi
  \selectlanguage{english}% always left-to-right, even if called inside hebrewpage
  \ctkeepprev% after the language switch: a whatsit between the penalty and the box would allow a break
  % (v0.21) split plan: a box that does not fit the rest of the page is cut ONCE, at the last line that
  % fits, with at least \ct@pyminfrag lines on each side; if that is impossible it moves whole.
  \ct@pyn=\numexpr\ct@pylast-\ct@pyfirst+1\relax
  \ct@pysplitat=0
  \ifdim\pagegoal<\maxdimen
    \ct@pyfit=\numexpr\dimexpr\pagegoal-\pagetotal-19pt\relax/\dimexpr12.5pt\relax\relax
    \ifnum\ct@pyfit<\ct@pyn
      \ifnum\ct@pyn<\numexpr2*\ct@pyminfrag\relax\else
        \ifnum\ct@pyfit>\numexpr\ct@pyn-\ct@pyminfrag\relax\ct@pyfit=\numexpr\ct@pyn-\ct@pyminfrag\relax\fi
        \ifnum\ct@pyfit<\ct@pyminfrag\else\ct@pysplitat=\ct@pyfit\fi
      \fi
    \fi
  \fi
  \ifnum\ct@pysplitat>0
    \ct@pya=\ct@pyfirst\relax \ct@pyb=\numexpr\ct@pyfirst+\ct@pysplitat-1\relax
    \ct@pybox{#2}%
    \par\penalty0
    \ct@pya=\numexpr\ct@pyfirst+\ct@pysplitat\relax \ct@pyb=\ct@pylast\relax
    \ct@pybox{#2}%
  \else
    \ct@pya=\ct@pyfirst\relax \ct@pyb=\ct@pylast\relax
    \ct@pybox{#2}%
  \fi
  \endgroup\ct@boxafter}
\newcount\ct@pyn \newcount\ct@pyfit \newcount\ct@pysplitat \newcount\ct@pya \newcount\ct@pyb
\newcommand*{\ct@pyminfrag}{8}
% one box with lines \ct@pya..\ct@pyb of the file; unbreakable up to \ct@pysplitmax lines
\newcommand*{\ct@pybox}[1]{%
  \ifnum\numexpr\ct@pyb-\ct@pya+1\relax>\ct@pysplitmax\relax
    \def\ct@pybreak{breakable}\else\def\ct@pybreak{unbreakable}\fi
  \tcbinputlisting{listing file={#1},listing only,enhanced,\ct@pybreak,colback=ivory,
    colframe=mochapale,boxrule=0.4pt,arc=0pt,left=24pt,right=4pt,top=6pt,bottom=6pt,
    listing options={style=ctpython,firstline=\the\ct@pya,lastline=\the\ct@pyb,firstnumber=\the\ct@pya},
    before skip=0pt,after skip=0pt}}

%%% ================= v0.5: cover, banner, footer, matter ===================
% Cover fields: main.tex sets these macros (NO ID numbers anywhere).
\newcommand*{\cttitle}[1]{\gdef\ct@title{#1}}
\newcommand*{\ctsubtitle}[1]{\gdef\ct@subtitle{#1}}
\newcommand*{\ctauthors}[1]{\gdef\ct@authors{#1}}
\newcommand*{\ctgroup}[1]{\gdef\ct@group{#1}}
\newcommand*{\ctcourse}[1]{\gdef\ct@course{#1}}
\newcommand*{\ctlecturer}[1]{\gdef\ct@lecturer{#1}}
\newcommand*{\ctdate}[1]{\gdef\ct@date{#1}}
\newcommand*{\ctdoctype}[1]{\gdef\ct@doctype{#1}}\ctdoctype{}% small label on the cover, e.g. "Business plan"
\newcommand*{\ctbrand}[1]{\gdef\ct@brand{#1}}\ctbrand{ClosetTwin}% brand name (banner/footer/cover)
\newcommand*{\ctbrandline}[1]{\gdef\ct@brandline{#1}}\ctbrandline{}% optional footer tagline
% footer wording per language (override in main.tex if needed)
\newcommand*{\ctpageword}{Page}\newcommand*{\ctofword}{of}
\newcommand*{\cthebpageword}{עמוד}\newcommand*{\cthebofword}{מתוך}
\cttitle{ClosetTwin}\ctsubtitle{}\ctauthors{}\ctgroup{}\ctcourse{}\ctlecturer{}\ctdate{\today}
% ---- cover (stage 5): fashion-magazine style, TikZ only, all text from the \ct... fields ----
\newcommand*{\ctlabelauthors}{Authors}\newcommand*{\ctlabelgroup}{Group}
\newcommand*{\ctlabelcourse}{Course}\newcommand*{\ctlabellecturer}{Lecturer}
% the "twin": a dress on a hanger, drawn once filled and once as a dashed outline
\newcommand*{\ct@dresspath}{(-1.9,1.9) -- (-1.35,0.2) -- (-0.95,-0.9) -- (-3.1,-6.0)
  .. controls (-1.5,-6.6) and (1.5,-6.6) .. (3.1,-6.0) -- (0.95,-0.9) -- (1.35,0.2) -- (1.9,1.9)
  .. controls (1.1,1.35) and (-1.1,1.35) .. cycle}
\newcommand*{\ct@coverlabel}[2]{\ifx\relax#2\relax\else
  {\color{mochadeep}\fontsize{7.5}{9}\selectfont\MakeUppercase{#1}}\par\vspace{1pt}%
  {\fontsize{10.5}{13}\selectfont #2}\par\vspace{7pt}\fi}
\newcommand*{\ctmakecover}{%
  \begingroup\pagecolor{ivory}\thispagestyle{empty}\noindent
  \begin{tikzpicture}[overlay,x=1cm,y=1cm]
    % top strip
    \node[anchor=south west,inner sep=0,text=mochadeep] at (0,1.55) {\fontsize{7.5}{9}\selectfont\MakeUppercase{\ct@date}};
    \ifx\ct@doctype\@empty\else
      \node[anchor=south east,inner sep=0,text=mochadeep] at (15,1.55) {\fontsize{7.5}{9}\selectfont\bfseries\MakeUppercase{\ct@doctype}};
    \fi
    \draw[line width=0.5pt,ink] (0,1.4) -- (15,1.4);
    % masthead: the title spans the full measure
    \node[anchor=north west,inner sep=0,text=ink] at (0,1.15) {\ctheadfont\bfseries\resizebox{15cm}{!}{\ct@title}};
    \draw[line width=1.4pt,ink] (0,-2.3) -- (15,-2.3);
    \draw[line width=0.4pt,ink] (0,-2.45) -- (15,-2.45);
    \node[anchor=north,inner sep=0,text=mochadeep,align=center,text width=13cm] at (7.5,-2.95) {\ctheadfont\itshape\fontsize{14}{18}\selectfont\ct@subtitle};
    % illustration: powder-pink arch, the hanger, the dress and its dashed digital twin
    \fill[powderpink] (2.2,-20.0) -- (2.2,-11.4) arc[start angle=180,end angle=0,radius=5.3] -- (12.8,-20.0) -- cycle;
    \begin{scope}[shift={(7.5,-12.9)}]
      \draw[line width=1.5pt,ink,line cap=round] (0,2.95) -- (0,3.35) arc[start angle=180,end angle=-60,radius=0.38];
      \draw[line width=1.5pt,ink,line cap=round,line join=round] (-3.0,1.65) -- (0,2.95) -- (3.0,1.65) -- cycle;
      \fill[mocha] \ct@dresspath;
      \draw[line width=0.9pt,ink,line join=round] \ct@dresspath;
      \begin{scope}[shift={(0.55,-0.25)}]
        \draw[line width=0.7pt,mochadeep,dash pattern=on 3pt off 2.4pt] \ct@dresspath;
      \end{scope}
      \fill[mochadeep] (-0.95,-0.9) -- (0.95,-0.9) -- (0.8,-1.25) -- (-0.8,-1.25) -- cycle;
      \foreach \p in {(-1.35,0.2),(1.35,0.2),(-0.95,-0.9),(0.95,-0.9),(-3.1,-6.0),(3.1,-6.0)}
        \fill[ivory,draw=ink,line width=0.5pt] \p circle (0.09);
    \end{scope}
    % cover lines
    \draw[line width=0.4pt,ink] (0,-20.9) -- (15,-20.9);
    \node[anchor=north west,inner sep=0,text width=5.2cm,align=left] at (0,-21.3) {\setlength{\parskip}{0pt}\ct@coverlabel{\ctlabelauthors}{\ct@authors}};
    \node[anchor=north west,inner sep=0,text width=4.6cm,align=left] at (5.6,-21.3) {\setlength{\parskip}{0pt}\ct@coverlabel{\ctlabelgroup}{\ct@group}};
    \node[anchor=north west,inner sep=0,text width=4.0cm,align=left] at (10.9,-21.3) {\setlength{\parskip}{0pt}\ct@coverlabel{\ctlabellecturer}{\ct@lecturer}};
    \node[anchor=north west,inner sep=0,text width=15cm,align=left] at (0,-22.7) {\setlength{\parskip}{0pt}\ct@coverlabel{\ctlabelcourse}{\ct@course}};
  \end{tikzpicture}\clearpage\endgroup\nopagecolor}
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
% chapter openers (and the Hebrew opener) use "plain": NO banner, footer kept (magazine style)
\def\ps@plain{%
  \let\@mkboth\markboth
  \def\@oddhead{}\let\@evenhead\@oddhead
  \def\@oddfoot{\ctfooter}\let\@evenfoot\@oddfoot}
\pagestyle{closettwin}
\setlength{\footskip}{18pt}% the footer is a \vtop: its rule sits 18pt under the text block
% the Hebrew page sets the banner's chapter-name slot to its Hebrew title
\renewenvironment{hebrewpage}[1][]
  {\clearpage\thispagestyle{plain}\markboth{\ctmediumfont\fontsize{9.5}{9.5}\selectfont #1}{\ctmediumfont\fontsize{9.5}{9.5}\selectfont #1}\begin{otherlanguage}{hebrew}\ct@hebfoottrue\raggedright\setlength{\parskip}{0.7em}\ct@hebrewlists}
  {\clearpage\end{otherlanguage}\clearpage}
% RTL lists: the physical indent is on the left, so mirror it to the right
\newcommand*{\ct@hebrewlists}{\setlist[itemize]{label=\makebox[1.1em][l]{\textcolor{mocha}{\textbullet}},leftmargin=0pt,rightmargin=1.6em,labelsep=0.5em}\setlist[enumerate]{label=\makebox[1.1em][l]{\textcolor{mochadeep}{\arabic*.}},leftmargin=0pt,rightmargin=1.6em,labelsep=0.5em}}
% no widows/orphans; floats never take a page of their own unless nearly full
\clubpenalty=10000 \widowpenalty=10000 \displaywidowpenalty=10000
% floats go here (h), else to the top of the next page (t) or a page of their own (p): never to the
% bottom (b), which left a hole above a table pushed to the foot of the page. A float page starts at
% the top (not vertically centred), with the free space below.
\renewcommand*{\fps@figure}{htp}\renewcommand*{\fps@table}{htp}
\setlength{\@fptop}{0pt}\setlength{\@fpsep}{\ctboxsep}\setlength{\@fpbot}{0pt plus 1fil}
% the class decides where floats go: an author's placement ([tbp], [t] ...) is ignored, so no
% chapter can create a hole or push a float above its heading
\let\ct@xfloat\@xfloat
\def\@xfloat#1[#2]{\edef\reserved@a{\noexpand\ct@xfloat{#1}[\csname fps@#1\endcsname]}\reserved@a}
% a heading forbids a top float on its own page, so a float never lands above the heading it follows
\renewcommand*{\sectionmark}[1]{\suppressfloats[t]}\renewcommand*{\subsectionmark}[1]{\suppressfloats[t]}
% every chapter flushes its floats first
\preto\chapter{\FloatBarrier}
%%% ================= v0.14: references (biblatex, IEEE, biber) ============
\RequirePackage[backend=biber,style=ieee,sorting=none,maxbibnames=6,minbibnames=3,
  giveninits=true,doi=true,url=true,isbn=false,eprint=false]{biblatex}
\DeclareLanguageMapping{hebrew}{english}% no biblatex module for Hebrew: no warning
\renewcommand*{\bibfont}{\small}
\renewcommand*{\mkonepagegrouped}[1]{#1}% IEEE style groups digits (100 779): switch it off
\renewcommand*{\bibrangedash}{\nobreak\textendash\nobreak}% a page range never breaks
% A non-English source: `language = {hebrew}` in the .bib prints "(in Hebrew)" inside the closing
% quote of the translated English title (IEEE practice). No Hebrew script is ever in the .bib.
\newcommand*{\ct@inlang}{}
\newcommand*{\ct@uc}[1]{\MakeUppercase{#1}}
\newcommand*{\ct@langitem}[1]{\ifstrequal{#1}{english}{}{\ifdefempty{\ct@inlang}{\gdef\ct@inlang{(in \expandafter\ct@uc#1)}}{}}}
\DeclareListFormat{language}{\ct@langitem{#1}}% records the language, prints nothing
\AtEveryBibitem{\gdef\ct@inlang{}\setbox0\hbox{\printlist{language}}\clearlist{language}}
\DeclareFieldFormat[article,inproceedings,incollection,book,report,online,misc]{title}{%
  \mkbibquote{#1\ifdefempty{\ct@inlang}{}{\space\ct@inlang}\isdot}}
% \ctbibresource{references.bib} in the preamble, \ctreferences where the list goes
\newcommand*{\ctbibresource}[1]{\def\ct@bibset{}\addbibresource{#1}}
% (v0.22) a document that never calls \ctbibresource (scratch/test builds) used to end with the LuaTeX fatal
% "cannot find file ''" (biblatex without any resource); it now defaults to the project's references.bib
\AtEndPreamble{\ifdefined\ct@bibset\else\addbibresource{references.bib}\fi}
\defbibheading{ctbib}[\bibname]{\ctunnumbered{#1}}
\newcommand*{\ctreferences}{\printbibliography[heading=ctbib,title={References}]}
% hyperref last: palette colours only, no boxes
\RequirePackage[colorlinks=true,linkcolor=mochadeep,citecolor=mochadeep,urlcolor=mochadeep,
  bookmarksnumbered=true,unicode=true,pdfusetitle=false]{hyperref}
\urlstyle{same}

\endinput
