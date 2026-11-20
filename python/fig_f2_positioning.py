"""F2: positioning map. Run from the root: python python/fig_f2_positioning.py
Positions are our reading of vendor pages (claim-trace V01-V09), not measurements."""
import ct_style as ct

# (name, x: 0 = questionnaire / size chart ... 1 = body scan,
#        y: 0 = consumer app ... 1 = B2B plug-in, label dx, dy, ha)
V = [
    ("True Fit", 0.22, 0.88, 6, 0, "left"),
    ("Fit Analytics", 0.40, 0.76, 6, 0, "left"),
    ("Bold Metrics", 0.12, 0.64, 6, 0, "left"),
    ("3DLOOK", 0.84, 0.70, -6, 0, "right"),
    ("MySize", 0.55, 0.50, 6, 0, "left"),
    ("Google try-on", 0.30, 0.14, 6, 0, "left"),
    ("Walmart / Zeekit", 0.62, 0.22, 6, 0, "left"),
]
fig, ax = ct.figure(1.0, 0.62)
ax.grid(False)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
ax.axhline(0.5, color=ct.GRID, lw=0.8, zorder=0)
ax.axvline(0.5, color=ct.GRID, lw=0.8, zorder=0)
for name, x, y, dx, dy, ha in V:
    ax.plot(x, y, "o", color=ct.MOCHA, mec=ct.INK, mew=0.6, ms=8)
    ct.label(ax, x, y, name, dx=dx, dy=dy, ha=ha)
ax.plot(0.88, 0.92, "D", color=ct.INK, ms=9)
ct.label(ax, 0.88, 0.92, "ClosetTwin (target)", dx=-8, ha="right")
ax.set_xticks([]); ax.set_yticks([])
ax.set_xlabel("Questionnaire or size chart to body scan")
ax.set_ylabel("Consumer app to B2B plug-in")
print(ct.save(fig, "f2-positioning"))
