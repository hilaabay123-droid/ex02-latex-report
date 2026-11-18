from fontTools.ttLib import TTFont
f=TTFont(r"C:\biu\02\fonts\Rubik-Regular.ttf"); c=f.getBestCmap()
heb=[x for x in range(0x590,0x600) if x in c]
print("hebrew glyphs",len(heb), "letters 05D0-05EA", all(x in c for x in range(0x5D0,0x5EB)))
need="‎‏־״׳–—“”‘’%₪$€()[]/:;,.-"
print("missing", [hex(ord(x)) for x in need if ord(x) not in c])
print("niqqud", 0x5B0 in c, "shekel", 0x20AA in c, "ligfi", 0xFB01 in c)
p=TTFont(r"C:\biu\02\fonts\PlayfairDisplay-Regular.ttf").getBestCmap()
print("playfair hebrew", any(x in p for x in range(0x5D0,0x5EB)), "missing", [hex(ord(x)) for x in "–—“”%$€≈×" if ord(x) not in p])
