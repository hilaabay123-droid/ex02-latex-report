p = r"C:\biu\02\closettwin.cls"
s = open(p, encoding="utf8").read()
a = s.index(r"  \ifnum\numexpr\ct@pylast-\ct@pyfirst+1\relax>\ct@pysplitmax\relax")
b = s.index(r"  \endgroup\ct@boxafter}", a) + len(r"  \endgroup\ct@boxafter}")
new = r"""  \selectlanguage{english}% always left-to-right, even if called inside hebrewpage
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
    before skip=0pt,after skip=0pt}}"""
s = s[:a] + new + s[b:]
s = s.replace(r"2026/11/20 v0.20 ClosetTwin", r"2026/11/20 v0.21 ClosetTwin")
open(p, "w", encoding="utf8").write(s)
print("ok")
