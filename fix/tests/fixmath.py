import re
p=r"C:\biu\02\fix\tests\t5.tex"
s=open(p,encoding="utf8").read()
new="\\setmathfont{Latin Modern Math}\n\\setmathfont{Rubik-Regular}[Path=../../fonts/,Extension=.ttf,range={up/{Latin,latin,num}},Scale=MatchLowercase]"
s=re.sub(r"\\setmathfont\{Rubik-Regular\}.*?Scale=MatchLowercase\]",lambda m:new,s,flags=re.S)
open(p,"w",encoding="utf8").write(s)
