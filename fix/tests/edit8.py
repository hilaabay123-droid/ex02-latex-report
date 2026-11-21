p=r"C:\biu\02\closettwin.cls"
s=open(p,encoding='utf8').read()
a=s.index("% (v0.22) TABLES FLOW IN PLACE")
b=s.index("% (v0.22) "+chr(92)+"texttt prints")
s=s[:a]+s[b:]
open(p,'w',encoding='utf8').write(s)
print(s.count("ct@tblplace"))
