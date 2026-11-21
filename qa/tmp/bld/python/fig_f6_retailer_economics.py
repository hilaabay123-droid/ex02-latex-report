"""F6: what a retailer nets per order from ClosetTwin, against the return reduction it achieves.
Run from the project root:  python python/fig_f6_retailer_economics.py   ->  figures/f6-retailer-economics.pdf
All numbers come from python/data/assumptions.csv through model.py."""
import numpy as np
import ct_style as ct
import model

rows, inputs, _ = model.load_inputs()
derived = model.compute(inputs)

cost_per_order = derived["D04"]        # fit-related return cost per order (USD)
prices = {"Growth": inputs["A07"], "Enterprise": inputs["A08"]}
base_rho = inputs["A04"]               # base-case reduction of fit-related returns
rho = np.linspace(inputs["A05a"], inputs["A05b"], 200)

fig, ax = ct.figure(1.0, 0.5)
for (tier, price), colour, nudge in zip(prices.items(), (ct.INK, ct.MOCHA), (-1, 1)):
    net_cents = (cost_per_order * rho - price) * 100          # net saving per order, in US cents
    ax.plot(rho * 100, net_cents, color=colour)
    break_even = price / cost_per_order                        # reduction at which the retailer breaks even
    ax.plot(break_even * 100, 0, "o", color=colour, ms=5)
    ct.label(ax, break_even * 100, 0, f"{tier}: break-even at {break_even:.1%}", dx=6, dy=-11 if nudge > 0 else -23)
    ct.label(ax, rho[-1] * 100, net_cents[-1], tier, dx=4, dy=4 * nudge)

ax.axhline(0, color=ct.INK, lw=0.6)
ax.axvline(base_rho * 100, color=ct.MOCHA_PALE, lw=1.2, zorder=0)
ct.label(ax, base_rho * 100, ax.get_ylim()[1], f"Base case {base_rho:.0%}", dx=4, dy=-6)
ax.set_xlabel("Reduction of fit-related returns (%)")
ax.set_ylabel("Net saving per order (US cents)")
ax.set_xlim(0, rho[-1] * 100 + 6)
print(ct.save(fig, "f6-retailer-economics"))
