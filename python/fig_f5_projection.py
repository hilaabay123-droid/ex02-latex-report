"""F5: five-year projection, two panels. Run from the root: python python/fig_f5_projection.py
All numbers come from python/data/assumptions.csv through model.py."""
import numpy as np
import ct_style as ct
import model

_, inputs, _ = model.load_inputs()
d = model.compute(inputs)
Y = np.arange(1, 6)
rev = np.array([d[f"D20_{y}"] for y in Y]) / 1e3
cost = np.array([d[f"D21_{y}"] + d[f"D22_{y}"] + d[f"D28_{y}"] for y in Y]) / 1e3
cum = np.array([d[f"CUM_{y}"] for y in Y]) / 1e6

fig, (a, b) = ct.plt.subplots(1, 2, figsize=(ct.TEXTWIDTH_IN, ct.TEXTWIDTH_IN * 0.45))
w = 0.38
a.bar(Y - w / 2, rev, w, color=ct.MOCHA, label="Revenue", **ct.outlined())
a.bar(Y + w / 2, cost, w, color=ct.PINK, label="Total cost", **ct.outlined())
a.legend(loc="upper left")
a.set_xticks(Y, [f"Y{y}" for y in Y])
a.set_ylabel("US$ thousand per year")
a.set_title("(a) Revenue and cost", loc="left", fontsize=ct.BODY_PT)

b.plot(Y, cum, color=ct.INK, marker="o", ms=4)
i = int(np.argmin(cum))
b.plot(Y[i], cum[i], "o", color=ct.MOCHA, mec=ct.INK, ms=8)
ct.label(b, Y[i], cum[i], f"Peak deficit US${-cum[i]:.2f} M", dx=-6, dy=-12, ha="right")
b.axhline(0, color=ct.INK, lw=0.6)
b.set_xticks(Y, [f"Y{y}" for y in Y])
b.set_ylim(cum.min() * 1.25, 0.2)
b.set_xlim(0.7, 5.4)
b.set_ylabel("Cumulative result, US$ M")
b.set_title("(b) Cumulative result", loc="left", fontsize=ct.BODY_PT)
print(ct.save(fig, "f5-projection"))
