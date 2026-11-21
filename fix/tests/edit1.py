import re
p='closettwin.cls'; s=open(p,encoding='utf8').read()
BS=chr(92)
def rep(a,b,count=1):
    global s
    assert a in s, a[:60]
    s=s.replace(a,b,count)
rep("ItalicFont=PlayfairDisplay-Italic,BoldItalicFont=PlayfairDisplay-BoldItalic,Numbers=Lining]",
    "ItalicFont=PlayfairDisplay-Italic,BoldItalicFont=PlayfairDisplay-BoldItalic,Numbers=Lining,Ligatures=TeX]")
rep(BS+"newfontfamily"+BS+"ctmediumfont{Rubik-Medium}", BS+"newfontfamily"+BS+"ctmediumfont{Rubik-Medium}[Ligatures=TeX]")
rep("ItalicFont=JetBrainsMono-Italic,BoldItalicFont=JetBrainsMono-BoldItalic,Scale=0.85]",
    "ItalicFont=JetBrainsMono-Italic,BoldItalicFont=JetBrainsMono-BoldItalic,Scale=0.85,RawFeature={-tlig;-liga;-calt}]")
open(p,'w',encoding='utf8').write(s)
