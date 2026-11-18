from fontTools.ttLib import TTFont
c=TTFont(r"C:\biu\02\fonts\Rubik-Regular.ttf").getBestCmap()
print("greek", any(x in c for x in range(0x391,0x3CA)), "minus", 0x2212 in c, "approx", 0x2248 in c, "times", 0xD7 in c, "plusminus",0xB1 in c)
def L(h):
    r=[int(h[i:i+2],16)/255 for i in (0,2,4)]; r=[x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4 for x in r]; return .2126*r[0]+.7152*r[1]+.0722*r[2]
def cr(a,b):
    a,b=L(a),L(b); a,b=max(a,b),min(a,b); return (a+.05)/(b+.05)
for n,(a,b) in {"mocha/white":("A47864","FFFFFF"),"mocha/ivory":("A47864","F7F3EE"),"mochadeep/white":("6B4B3D","FFFFFF"),"ivory/white":("F7F3EE","FFFFFF"),"pink/white":("E8C6C0","FFFFFF"),"ivory text on mocha":("F7F3EE","A47864"),"ink/mocha":("111111","A47864")}.items(): print(n, round(cr(a,b),2))
