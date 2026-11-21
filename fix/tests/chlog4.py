BS=chr(92)
row=("| 2026-11-20 | closettwin v0.22 | master-se via qa-se round 2 (F-clsver-02, figure centering, texttt) and writer-se (cannot find file '') | "
"(a) v0.21 had no CHANGELOG row (now logged, see the v0.21 row above); (b) 4 figure floats carry a manual "+BS+"centering; (d) "+BS+"texttt printed Latin Modern Mono in prose; (e) a scratch document without "+BS+"ctbibresource ended with the LuaTeX fatal \"cannot find file ''\" | "
"(b) the class had no default for figures; (d) no rule for the mono font; (e) biblatex loaded with no resource at all | "
"(b) "+BS+"AtBeginEnvironment{figure}{"+BS+"centering} (writer-se can remove the manual "+BS+"centering); (d) "+BS+"texttt sets its argument in the text font and writes a class warning \"closettwin Warning: "+BS+"texttt used in the text\" per use (qa-code greps main.log for it); (e) default "+BS+"addbibresource{references.bib} when none was declared; verified on a 1-page test document. (c) tried and dropped: tables that flow in place and split once (a "+BS+"vbox/"+BS+"vsplit rewrite of the table environment) broke the tabular rows and conflicts with the no-split table rule; gaps are handled by moving the table in the chapter source (writer-se did so for ch.9) | closettwin.cls |\n")
p=r"C:\biu\02\fix\CHANGELOG.md"
s=open(p,encoding='utf8').read().rstrip("\n")+"\n"+row
open(p,'w',encoding='utf8').write(s)
