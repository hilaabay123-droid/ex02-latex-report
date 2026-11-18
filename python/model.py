"""ClosetTwin financial model. Single source of truth: python/data/assumptions.csv.

Run from the root:  python python/model.py
Writes python/data/model_out.csv (every derived value) and python/data/sensitivity_out.csv (for F6).
Deterministic: no randomness, no network, no clock.
"""
import csv
from pathlib import Path
from statistics import NormalDist

DATA = Path(__file__).resolve().parent / "data"
YEARS = range(1, 6)


def load_inputs():
    rows = list(csv.DictReader(open(DATA / "assumptions.csv", encoding="utf-8", newline="")))
    inputs, meta = {}, {}
    for r in rows:
        meta[r["id"]] = r
        if r["class"] in ("sourced", "assumed"):
            try:
                inputs[r["id"]] = float(r["value"])
            except ValueError:
                pass  # text rows (A19, A29*): not used in arithmetic
    return rows, inputs, meta


def sample_per_arm(p1, rel, alpha, power):
    """Two-proportion sample size per arm for a relative reduction `rel` of p1."""
    p2 = p1 * (1 - rel)
    z = NormalDist().inv_cdf(1 - alpha / 2) + NormalDist().inv_cdf(power)
    return z * z * (p1 * (1 - p1) + p2 * (1 - p2)) / (p1 - p2) ** 2


def mde_relative(p1, n, alpha, power):
    """Smallest relative reduction detectable with n per arm (bisection; sample_per_arm is decreasing in rel)."""
    lo, hi = 1e-6, 0.99
    for _ in range(200):
        mid = (lo + hi) / 2
        if sample_per_arm(p1, mid, alpha, power) > n:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def compute(a):
    d = {}
    d["D01"] = a["A02"] * a["A01"]
    d["D02"] = a["S02"] * d["D01"]
    d["D03"] = a["S01"] * a["A03"]
    d["D04"] = d["D03"] * d["D02"]
    d["D05"] = a["A04"] * a["S01"] * a["A03"] * d["D02"]          # formula (1)
    d["D06a"] = a["A07"] / d["D05"]
    d["D06b"] = a["A08"] / d["D05"]
    d["D07a"] = a["A07"] / d["D04"]
    d["D07b"] = a["A08"] / d["D04"]
    d["D08"] = a["A10a"] * a["A07"] + a["A10b"] * a["A08"]
    d["D09"] = d["D05"] * a["A11"]
    d["D10"] = a["A07"] * a["A11"]
    d["D11"] = a["A12"] * a["A13"]
    d["D12"] = (d["D08"] - d["D11"]) / d["D08"]
    d["D13"] = a["S08"] / a["A12"]
    d["D14"] = a["S04"] / a["A01"]
    d["D15"] = d["D14"] * d["D08"]
    d["D16"] = 1 - a["S05"]
    d["D17"] = d["D15"] * d["D16"] * a["A06"]
    d["D18"] = sample_per_arm(d["D03"], a["A04"], a["A20a"], a["A20b"])
    n_window = a["A11"] * a["A22"] / 52 / 2                         # orders per arm in the pilot window
    d["D19"] = mde_relative(d["D03"], n_window, a["A20a"], a["A20b"])
    cum, peak = 0.0, 0.0
    for y in YEARS:
        rev = a["A26p"] * a["A09"] if y == 1 else a[f"A26_{y}"] * a["A11"] * d["D08"]
        cogs = 0.0 if y == 1 else a[f"A26_{y}"] * a["A11"] * d["D11"]
        opex = a[f"A25_{y}"] * a["A14"]
        d[f"D20_{y}"], d[f"D21_{y}"], d[f"D22_{y}"] = rev, cogs, opex
        d[f"D23_{y}"] = rev - cogs - opex
        cum += d[f"D23_{y}"]
        d[f"CUM_{y}"] = cum
        peak = min(peak, cum)
    d["D24"] = peak
    d["D25"] = -peak * (1 + a["A30"])
    d["D26"] = d["D20_5"]
    d["D27"] = d["D20_5"] / d["D17"]
    d["_n_window_per_arm"] = n_window
    return d


def sensitivity(a, d, steps=41):
    """Return-reduction effect rho from A05a to A05b. Client view at 1M orders/year.
    saving per order = D04 * rho; fee = price per order. Payback = pilot fee / monthly net saving."""
    lo, hi = a["A05a"], a["A05b"]
    out = []
    for i in range(steps):
        rho = lo + (hi - lo) * i / (steps - 1)
        saving = d["D04"] * rho
        row = {"rho": rho, "saving_per_order": saving}
        for tag, price in (("growth", a["A07"]), ("enterprise", a["A08"]), ("blended", d["D08"])):
            net_month = (saving - price) * a["A11"] / 12
            row[f"net_per_order_{tag}"] = saving - price
            row[f"annual_net_{tag}"] = net_month * 12
            row[f"payback_months_{tag}"] = (a["A09"] / net_month) if net_month > 0 else ""
        out.append(row)
    return out


def write_csv(path, rows, fields):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    rows, a, meta = load_inputs()
    d = compute(a)
    out = []
    for r in rows:
        if r["class"] == "derived":
            out.append({"id": r["id"], "name": r["name"], "value": format(d[r["id"]], ".10g"), "unit": r["unit"]})
    for y in YEARS:
        out.append({"id": f"CUM_{y}", "name": f"Cumulative operating result year {y}", "value": format(d[f"CUM_{y}"], ".10g"), "unit": "USD"})
    write_csv(DATA / "model_out.csv", out, ["id", "name", "value", "unit"])
    sens = sensitivity(a, d)
    write_csv(DATA / "sensitivity_out.csv", [{k: format(v, ".10g") if v != "" else "" for k, v in r.items()} for r in sens], list(sens[0]))

    # --- check against writer-se's hand numbers (outline section 10.3) ---
    hand = [
        ("D02 cost per return", d["D02"], 6.80),
        ("D05 break-even per order", d["D05"], 0.0996),
        ("D08 blended price", d["D08"], 0.036),
        ("D15 TAM fee pool", d["D15"], 0.33e9),
        ("D17 SAM fee pool", d["D17"], 75e6),
        ("D20_1 revenue Y1", d["D20_1"], 10e3),
        ("D20_2 revenue Y2", d["D20_2"], 0.29e6),
        ("D20_3 revenue Y3", d["D20_3"], 0.90e6),
        ("D20_4 revenue Y4", d["D20_4"], 2.16e6),
        ("D20_5 revenue Y5", d["D20_5"], 4.32e6),
        ("D24 peak deficit", d["D24"], -1.48e6),
        ("D25 ask", d["D25"], 1.8e6),
        ("D18 sample per arm", d["D18"], 6000),
    ]
    print(f"{'value':28s} {'model':>16s} {'hand':>14s} {'delta %':>9s}")
    for name, m, h in hand:
        dl = (m - h) / h * 100
        print(f"{name:28s} {m:16,.4f} {h:14,.4f} {dl:+9.2f}{'  <-- >1%' if abs(dl) > 1 else ''}")
    print("\nextra:", {k: round(v, 4) for k, v in d.items() if k in ("D03", "D04", "D06a", "D06b", "D07a", "D07b", "D09", "D10", "D11", "D12", "D13", "D14", "D16", "D19", "D27")})
    print("cumulative:", [round(d[f"CUM_{y}"]) for y in YEARS], "| op result:", [round(d[f"D23_{y}"]) for y in YEARS])


if __name__ == "__main__":
    main()
