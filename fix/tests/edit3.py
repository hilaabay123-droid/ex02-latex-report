p='closettwin.cls'; s=open(p,encoding='utf8').read()
BS=chr(92)
def rep(a,b):
    global s
    assert a in s, a[:50]
    s=s.replace(a,b,1)
rep(BS+"newcommand*{"+BS+"ct@mdig}[1]{"+BS+"mathord{"+BS+"text{#1}}}", BS+"newcommand*{"+BS+"ct@mdig}[1]{{"+BS+"text{#1}}}% a braced group: valid after _ and ^ too")
rep(BS+"let"+BS+"ct@origcaption"+BS+"caption"+"\n"+BS+"RenewDocumentCommand{"+BS+"caption}{s o m}{%",
    BS+"AtBeginDocument{"+BS+"let"+BS+"ct@origcaption"+BS+"caption"+"\n"+BS+"RenewDocumentCommand{"+BS+"caption}{s o m}{%")
rep(BS+"IfNoValueTF{#2}{"+BS+"ct@origcaption["+BS+"ct@capcut{#3}]{#3}}{"+BS+"ct@origcaption[#2]{#3}}}}",
    BS+"IfNoValueTF{#2}{"+BS+"ct@origcaption["+BS+"ct@capcut{#3}]{#3}}{"+BS+"ct@origcaption[#2]{#3}}}}}")
open(p,'w',encoding='utf8').write(s)
