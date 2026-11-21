p='closettwin.cls'; s=open(p,encoding='utf8').read()
BS=chr(92)
a=BS+"def"+BS+"ct@capcutaux#1(#2)#3"+BS+"relax{"+BS+"ct@capcutfin#1"+BS+"relax"+BS+"relax}"
b=BS+"def"+BS+"ct@capcutaux#1(#2)#3"+BS+"relax{"+BS+"ct@capcutfin#1 "+BS+"relax"+BS+"relax}"
assert a in s
s=s.replace(a,b)
open(p,'w',encoding='utf8').write(s)
