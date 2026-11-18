from fontTools.ttLib import TTFont
import glob
for f in sorted(glob.glob(r"C:\biu\02\fonts\PlayfairDisplay-*.ttf")):
    t=TTFont(f); n=t["name"]
    print(f.split("\\")[-1], len(open(f,"rb").read()), n.getDebugName(5), "| fvar" , "fvar" in t, "| heb", any(0x5D0 in c.cmap for c in t["cmap"].tables))
