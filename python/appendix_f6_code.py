"""F6 chart code (Appendix A): the retailer's net saving per order."""
import numpy as np
import ct_style as ct
import model

rows, inputs, _ = model.load_inputs()
derived = model.compute(inputs)

cost = derived["D04"]       # fit-related return cost per order, USD
prices = {"Growth": inputs["A07"], "Enterprise": inputs["A08"]}
base = inputs["A04"]        # base-case reduction of fit returns
rho = np.linspace(inputs["A05a"], inputs["A05b"], 200)

fig, ax = ct.figure(1.0, 0.5)
for (tier, price), colour in zip(prices.items(), (ct.INK, ct.MOCHA)):
    net = (cost * rho - price) * 100        # US cents per order
    ax.plot(rho * 100, net, color=colour)
    be = price / cost                       # break-even reduction
    ax.plot(be * 100, 0, "o", color=colour, ms=5)
    ct.label(ax, be * 100, 0, f"{tier}: {be:.1%}", dy=-11)

ax.axhline(0, color=ct.INK, lw=0.6)
ax.axvline(base * 100, color=ct.MOCHA_PALE, lw=1.2, zorder=0)
ax.set_xlabel("Reduction of fit-related returns (%)")
ax.set_ylabel("Net saving per order (US cents)")
ct.save(fig, "appendix-f6-demo")
