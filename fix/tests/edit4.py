p='closettwin.cls'; s=open(p,encoding='utf8').read()
BS=chr(92)
a=BS+"AtBeginDocument{"+BS+"let"+BS+"ct@origcaption"
assert a in s
s=s.replace(a, BS+"AddToHook{begindocument/end}{"+BS+"let"+BS+"ct@origcaption")
open(p,'w',encoding='utf8').write(s)
