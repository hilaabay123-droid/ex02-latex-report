p='closettwin.cls'; s=open(p,encoding='utf8').read()
BS=chr(92)
for old,new in [("{"+BS+"contentsname}"+BS+"@starttoc{toc}","{"+BS+"englishcontentsname}"+BS+"@starttoc{toc}"),
                ("{"+BS+"listfigurename}"+BS+"@starttoc{lof}","{"+BS+"englishlistfigurename}"+BS+"@starttoc{lof}"),
                ("{"+BS+"listtablename}"+BS+"@starttoc{lot}","{"+BS+"englishlisttablename}"+BS+"@starttoc{lot}")]:
    assert old in s, old
    s=s.replace(old,new)
s=s.replace(BS+"renewcommand*{"+BS+"tableofcontents}","% (v0.20) the plain babel-english names: "+BS+"contentsname is wrapped by babel's ensure and shifted the title 6.5pt right\n"+BS+"renewcommand*{"+BS+"tableofcontents}",1)
open(p,'w',encoding='utf8').write(s)
