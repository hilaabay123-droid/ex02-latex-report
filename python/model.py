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


def pilots(a, y):
    return a["A26p"] if y == 1 else a[f"A26q_{y}"]


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
        n_pilots = pilots(a, y)
        pilot_rev = n_pilots * a["A31"] * a["A09"] + n_pilots * (1 - a["A31"]) * a["A32"]
        pilot_cost = n_pilots * (a["A31"] * a["A33a"] + (1 - a["A31"]) * a["A33b"])
        clients = 0.0 if y == 1 else a[f"A26_{y}"]
        rev = clients * a["A11"] * d["D08"] + pilot_rev
        cogs = clients * a["A11"] * d["D11"]
        opex = a[f"A25_{y}"] * a["A14"]
        d[f"D20_{y}"], d[f"D21_{y}"], d[f"D22_{y}"], d[f"D28_{y}"] = rev, cogs, opex, pilot_cost
        d[f"D23_{y}"] = rev - cogs - opex - pilot_cost
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


def funnel_check(a):
    """MC-3 / MC-3c: the client path must be reachable through the funnel, and sales capacity must cover it.
    1. Reach: new clients in year y = A26_y - A26_(y-1)*(1-churn) (churn A27); each needs 1/A17 pilots, run in
       year y-1 (sales cycle A18 = 9 months), so pilots(y-1) * A17 >= new_y.
    2. Capacity: contacts needed for the pilots started in year y (pilots / A16 / A15) must not exceed
       sales FTE (A35 * A25_y) * A36 contacts/week * A37 weeks.
    3. Pilot effort (A34a/b FTE-months) must not exceed the headcount's FTE-months (A25_y * 12).
    Returns (rows, failures)."""
    rows, fails = [], []
    for y in range(1, 6):
        n_p = pilots(a, y)
        contacts = n_p / a["A16"] / a["A15"]
        sales_fte = a["A35"] * a[f"A25_{y}"]
        cap = sales_fte * a["A36"] * a["A37"]
        effort = n_p * (a["A31"] * a["A34a"] + (1 - a["A31"]) * a["A34b"])
        fte_months = a[f"A25_{y}"] * 12
        new = ""
        if y >= 2:
            new = max(0.0, a[f"A26_{y}"] - (a[f"A26_{y-1}"] if y > 2 else 0.0) * (1 - a["A27"]))
            reach = pilots(a, y - 1) * a["A17"]
            if new > reach + 1e-9:
                fails.append(f"Year {y} needs {new:.1f} new paying clients but the {pilots(a, y-1):.0f} pilots of year {y-1} "
                             f"give only {reach:.1f} at {a['A17']:.0%}.")
        if contacts > cap + 1e-9:
            fails.append(f"Year {y}: {contacts:.0f} outbound contacts needed > sales capacity {cap:.0f}.")
        if effort > fte_months + 1e-9:
            fails.append(f"Year {y}: pilot effort {effort:.1f} FTE-months > headcount {fte_months:.0f}.")
        rows.append({"year": y, "pilots": n_p, "new_clients_in_year": new,
                     "contacts_needed": contacts, "sales_contact_capacity": cap,
                     "contact_utilisation": contacts / cap, "pilot_effort_fte_months": effort,
                     "headcount_fte_months": fte_months})
    return rows, fails


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

    frows, fails = funnel_check(a)
    write_csv(DATA / "funnel_check_out.csv", [{k: (format(v, ".10g") if v != "" else "") for k, v in r.items()} for r in frows], list(frows[0]))

    # --- check against writer-se's hand numbers (outline section 10.3) ---
    hand = [
        ("D02 cost per return", d["D02"], 6.80),
        ("D05 break-even per order", d["D05"], 0.0996),
        ("D08 blended price", d["D08"], 0.036),
        ("D15 TAM fee pool", d["D15"], 0.33e9),
        ("D17 SAM fee pool", d["D17"], 75e6),
        ("D23_1 op result Y1", d["D23_1"], -358e3),
        ("D23_2 op result Y2", d["D23_2"], -487.5e3),
        ("D23_3 op result Y3", d["D23_3"], -538.1e3),
        ("D23_4 op result Y4", d["D23_4"], -73.5e3),
        ("D23_5 op result Y5", d["D23_5"], 916.5e3),
        ("CUM_1", d["CUM_1"], -358e3),
        ("CUM_2", d["CUM_2"], -845.5e3),
        ("CUM_3", d["CUM_3"], -1383.6e3),
        ("CUM_4", d["CUM_4"], -1457.1e3),
        ("CUM_5", d["CUM_5"], -540.6e3),
        ("D24 peak deficit", d["D24"], -1.457e6),
        ("D25 ask", d["D25"], 1.75e6),
        ("D18 sample per arm", d["D18"], 6000),
    ]
    print(f"{'value':28s} {'model':>16s} {'hand':>14s} {'delta %':>9s}")
    for name, m, h in hand:
        dl = (m - h) / h * 100
        print(f"{name:28s} {m:16,.4f} {h:14,.4f} {dl:+9.2f}{'  <-- >1%' if abs(dl) > 1 else ''}")
    print("\nextra:", {k: round(v, 4) for k, v in d.items() if k in ("D03", "D04", "D06a", "D06b", "D07a", "D07b", "D09", "D10", "D11", "D12", "D13", "D14", "D16", "D19", "D27")})
    print("cumulative:", [round(d[f"CUM_{y}"]) for y in YEARS], "| op result:", [round(d[f"D23_{y}"]) for y in YEARS])


def _main_with_exit():
    import sys
    main()
    _, fails = funnel_check(load_inputs()[1])
    if fails:
        print("\n*** FUNNEL CONSISTENCY CHECK FAILED (MC-3) ***", file=sys.stderr)
        for f in fails:
            print(" -", f, file=sys.stderr)
        sys.exit(1)
    print("\nfunnel consistency check: OK")


if __name__ == "__main__":
    _main_with_exit()
