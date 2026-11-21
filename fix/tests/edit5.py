p='closettwin.cls'; s=open(p,encoding='utf8').read()
BS=chr(92)
a=(BS+"titlecontents{chapter}[0pt]{"+BS+"addvspace{0.9em}"+BS+"bfseries}\n  {"+BS+"color{mochadeep}"+BS+"contentslabel{2.2em}}{"+BS+"hspace*{-2.2em}}\n  {"+BS+"hfill"+BS+"contentspage}["+BS+"addvspace{0.1em}]\n"
   +BS+"titlecontents{section}[2.2em]{"+BS+"small}\n  {"+BS+"contentslabel{2.4em}}{"+BS+"hspace*{-2.4em}}")
b=("% (v0.20) chapter numbers of the contents sit INSIDE the text block (they hung 24pt into the left margin: the 'stray 1,2,3')\n"
   +BS+"titlecontents{chapter}[2.2em]{"+BS+"addvspace{0.9em}"+BS+"bfseries}\n  {"+BS+"color{mochadeep}"+BS+"contentslabel{2.2em}}{"+BS+"hspace*{-2.2em}}\n  {"+BS+"hfill"+BS+"contentspage}["+BS+"addvspace{0.1em}]\n"
   +BS+"titlecontents{section}[2.2em]{"+BS+"small}\n  {"+BS+"contentslabel{2.2em}}{"+BS+"hspace*{-2.2em}}")
assert a in s
s=s.replace(a,b)
open(p,'w',encoding='utf8').write(s)
m=open('main.tex',encoding='utf8').read()
x=BS+"ctcourse{Generative AI for Management}"
assert x in m
m=m.replace(x,BS+"ctcourse{Generative AI for Management (875523402)}")
open('main.tex','w',encoding='utf8').write(m)
