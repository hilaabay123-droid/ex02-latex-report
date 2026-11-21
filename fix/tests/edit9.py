p=r"C:\biu\02\closettwin.cls"
s=open(p,encoding='utf8').read()
BS=chr(92)
a=s.index(BS+"def"+BS+"ct@capcut#1{")
b=s.index(BS+"let"+BS+"ct@origcaption") if (BS+"let"+BS+"ct@origcaption") in s else None
# find end of the three \def lines
end=s.index(BS+"def"+BS+"ct@capcutfin")
end=s.index("\n",end)+1
new=("% (v0.23) cut in Lua (no percent sign, hash or backslash-backslash inside \directlua): the entry stops before the first\n"
"% '(' or ':' or '$', so brackets, sub-titles and formulas never reach the lists\n"
+BS+"directlua{\n"
"  function ct_capcut(s)\n"
"    local cut = string.len(s) + 1\n"
"    for _, d in ipairs({\"(\", \":\", \"$\"}) do\n"
"      local i = string.find(s, d, 1, true)\n"
"      if i and i > 1 and i < cut then cut = i end\n"
"    end\n"
"    local r = string.sub(s, 1, cut - 1)\n"
"    while string.sub(r, -1) == \" \" do r = string.sub(r, 1, -2) end\n"
"    tex.sprint(r)\n"
"  end\n"
"}\n"
+BS+"newcommand*{"+BS+"ct@capcut}[1]{"+BS+"directlua{ct_capcut(\"" +BS+"luaescapestring{"+BS+"detokenize{#1}}\")}}\n")
s=s[:a]+new+s[end:]
open(p,'w',encoding='utf8').write(s)
