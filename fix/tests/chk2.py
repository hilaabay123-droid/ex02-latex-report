from fontTools.ttLib import TTFont
c=TTFont(r"C:\biu\02\fonts\PlayfairDisplay-Bold.ttf").getBestCmap()
print("missing", [x for x in "–—“”‘’%$€£&@#№0123456789" if ord(x) not in c])
t=TTFont(r"C:\biu\02\fonts\PlayfairDisplay-Bold.ttf"); print("lnum" , any(f.FeatureTag=="lnum" for f in t["GSUB"].table.FeatureList.FeatureRecord))
