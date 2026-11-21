"""ClosetTwin financial model.
Single source of truth: python/data/assumptions.csv.

Run from the root:  python python/model.py
Writes python/data/model_out.csv (every derived value)
and python/data/sensitivity_out.csv (for F6).
Deterministic: no randomness, no network, no clock.
"""
import csv
from pathlib import Path
from statistics import NormalDist

DATA = Path(__file__).resolve().parent / "data"
YEARS = range(1, 6)
ROUND_TOL = 0.5   # clients: the year-average client counts are whole numbers, so reach may be short by up to half a client (year 3: 2.2 needed vs 2.0)


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


def pilots_i(a, y):
    """Israeli pilots in year y."""
    return a["A26ip_1"] if y == 1 else a[f"A26iq_{y}"]


def pilots_e(a, y):
    """European pilots in year y: none before the entry year A45; ramp step 0 = A26eq_4, later steps = A26eq_5."""
    step = y - int(a["A45"])
    return 0.0 if step < 0 else (a["A26eq_4"] if step == 0 else a["A26eq_5"])


def pilot_fee_rev(a, y):
    return (pilots_i(a, y) * a["A31i"] * a["A09i"] + pilots_i(a, y) * (1 - a["A31i"]) * a["A32"]
            + pilots_e(a, y) * a["A31e"] * a["A09e"] + pilots_e(a, y) * (1 - a["A31e"]) * a["A32"])


def pilot_cash(a, y):
    return (pilots_i(a, y) * (a["A31i"] * a["A33a"] + (1 - a["A31i"]) * a["A33b"])
            + pilots_e(a, y) * (a["A31e"] * a["A33a"] + (1 - a["A31e"]) * a["A33b"]))


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
    d["D09"] = d["D05"] * a["A11e"]
    d["D10"] = a["A07"] * a["A11e"]
    d["D11"] = a["A12"] * a["A13"]
    d["D12"] = (d["D08"] - d["D11"]) / d["D08"]
    d["D13"] = a["S08"] / a["A12"]
    d["D14"] = a["S04"] / a["A01"]
    d["D15"] = d["D14"] * d["D08"]
    d["D16"] = 1 - a["S05"]
    d["D17"] = d["D15"] * d["D16"] * a["A06"]
    d["D18"] = sample_per_arm(d["D03"], a["A04"], a["A20a"], a["A20b"])
    # --- Israel (beachhead) and Europe (expansion): market sizes ---
    d["D29"] = a["S10"] * a["S09c"]
    d["D30"] = d["D29"] / a["A01"]
    d["D31"] = d["D30"] * a["A39"]
    d["D32"] = a["A40a"] * a["A41a"] + a["A40b"] * a["A41b"] + a["A40c"] * a["A41c"]
    d["D33"] = a["A40a"] * a["A41a"] + a["A40b"] * a["A41b"]
    d["D34"] = d["D33"] * d["D08"]
    d["D34b_tam"] = d["D30"] * d["D08"]
    d["D34b_local"] = d["D31"] * d["D08"]
    d["D35"] = a["S04"] * a["A42"] / a["A01"]
    d["D36"] = d["D35"] * d["D08"]
    d["D37"] = d["D36"] * a["A06"]
    d["D38"] = a["A44"] * a["A41a"] + (1 - a["A44"]) * a["A41b"]
    d["D39"] = a["A40a"] + a["A40b"]
    d["X01"] = 3.70
    a_i = d["A11i"] = d["D38"]                                       # A11i (derived)
    # pilot sizing: orders per arm in the 4-week window
    for tag, orders in (("D19e", a["A11e"]), ("D19i", a["A41a"]), ("D19i2", a["A41b"])):
        d[tag] = mde_relative(d["D03"], orders * a["A22"] / 52 / 2, a["A20a"], a["A20b"])
    d["_n_window_per_arm"] = a["A11e"] * a["A22"] / 52 / 2
    cum, peak = 0.0, 0.0
    for y in YEARS:
        sub_i = a[f"A26i_{y}"] * a_i * d["D08"]
        sub_e = a[f"A26e_{y}"] * a["A11e"] * d["D08"]
        rev = sub_i + sub_e + pilot_fee_rev(a, y)
        cogs = (a[f"A26i_{y}"] * a_i + a[f"A26e_{y}"] * a["A11e"]) * d["D11"]
        opex = a[f"A25_{y}"] * a["A14"]
        pcash = pilot_cash(a, y)
        d[f"SUBI_{y}"], d[f"SUBE_{y}"] = sub_i, sub_e
        d[f"D20_{y}"], d[f"D21_{y}"], d[f"D22_{y}"], d[f"D28_{y}"] = rev, cogs, opex, pcash
        d[f"D23_{y}"] = rev - cogs - opex - pcash
        cum += d[f"D23_{y}"]
        d[f"CUM_{y}"] = cum
        peak = min(peak, cum)
    d["D24"] = peak
    d["D25"] = -peak * (1 + a["A30"])
    d["D26"] = d["D20_5"]
    d["D27"] = (d["SUBI_5"] + d["SUBE_5"]) / (d["D34"] + d["D37"])   # subscription revenue / combined SAM
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
            net_month = (saving - price) * a["A11e"] / 12
            row[f"net_per_order_{tag}"] = saving - price
            row[f"annual_net_{tag}"] = net_month * 12
            row[f"payback_months_{tag}"] = (a["A09e"] / net_month) if net_month > 0 else ""
        out.append(row)
    return out


def funnel_check(a):
    """Israel + Europe funnel consistency (MC-3, IL-M1). Returns (rows, failures).
    1. Reach: new paying clients in year y = A26_y - A26_(y-1)*(1-churn A27) (Israel; Europe has no earlier clients)
       must not exceed the previous year's pilots x A17 (sales cycle A18 < 12 months).
    2. Capacity: contacts for the year's pilots (Israel pilots/A16i/A15i + Europe pilots/A16e/A15e) must not exceed
       sales FTE (A35 x A25_y) x A36 contacts/week x A37 weeks (one shared sales team).
    3. Pilot effort (A34a/b FTE-months, direct/low-touch) must not exceed the headcount's FTE-months.
    4. Pool caps (A46a/b/c): Israeli paying clients vs the pool D39, and large clients (A44 share) vs the A40a large retailers."""
    rows, fails = [], []
    pool = a["A40a"] + a["A40b"]
    for y in YEARS:
        pi, pe = pilots_i(a, y), pilots_e(a, y)
        contacts = pi / a["A16i"] / a["A15i"] + pe / a["A16e"] / a["A15e"]
        cap = a["A35"] * a[f"A25_{y}"] * a["A36"] * a["A37"]
        effort = (pi * (a["A31i"] * a["A34a"] + (1 - a["A31i"]) * a["A34b"])
                  + pe * (a["A31e"] * a["A34a"] + (1 - a["A31e"]) * a["A34b"]))
        fte_months = a[f"A25_{y}"] * 12
        new_i = new_e = ""
        if y >= 2:
            new_i = max(0.0, a[f"A26i_{y}"] - a[f"A26i_{y-1}"] * (1 - a["A27"]))
            new_e = max(0.0, a[f"A26e_{y}"] - a[f"A26e_{y-1}"] * (1 - a["A27"]))
            if new_i > pilots_i(a, y - 1) * a["A17"] + ROUND_TOL:
                fails.append(f"Year {y}: {new_i:.1f} new Israeli clients but the {pilots_i(a, y-1):.0f} pilots of year {y-1} give only {pilots_i(a, y-1) * a['A17']:.1f} at {a['A17']:.0%}.")
            if new_e > pilots_e(a, y - 1) * a["A17"] + ROUND_TOL:
                fails.append(f"Year {y}: {new_e:.1f} new European clients but the {pilots_e(a, y-1):.0f} pilots of year {y-1} give only {pilots_e(a, y-1) * a['A17']:.1f} at {a['A17']:.0%}.")
        share_cap = a["A46a"] if y <= 3 else a["A46b"]
        if a[f"A26i_{y}"] > share_cap * pool + 1e-9:
            fails.append(f"Year {y}: {a[f'A26i_{y}']:.0f} Israeli paying clients > {share_cap:.0%} of the pool of {pool:.0f}.")
        if a["A44"] * a[f"A26i_{y}"] > a["A46c"] * a["A40a"] + 1e-9:
            fails.append(f"Year {y}: large Israeli paying clients {a['A44'] * a[f'A26i_{y}']:.1f} > {a['A46c']:.0%} of the {a['A40a']:.0f} large retailers.")
        if contacts > cap + 1e-9:
            fails.append(f"Year {y}: {contacts:.0f} outbound contacts needed > sales capacity {cap:.0f}.")
        if effort > fte_months + 1e-9:
            fails.append(f"Year {y}: pilot effort {effort:.1f} FTE-months > headcount {fte_months:.0f}.")
        rows.append({"year": y, "pilots_israel": pi, "pilots_europe": pe, "new_clients_israel": new_i, "new_clients_europe": new_e,
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
    hand = [  # outline section 10.5 D (IL-O1)
        ("D02 cost per return", d["D02"], 6.80),
        ("D05 break-even per order", d["D05"], 0.0996),
        ("D08 blended price", d["D08"], 0.036),
        ("D19i MDE large IL", d["D19i"], 0.079),
        ("D19i2 MDE mid IL", d["D19i2"], 0.19),
        ("D19e MDE Europe", d["D19e"], 0.061),
        ("D20_1 revenue Y1", d["D20_1"], 10000),
        ("D20_2 revenue Y2", d["D20_2"], 28000),
        ("D20_3 revenue Y3", d["D20_3"], 46000),
        ("D20_4 revenue Y4", d["D20_4"], 97500),
        ("D20_5 revenue Y5", d["D20_5"], 782000),
        ("D28_4 pilot cash Y4", d["D28_4"], 49500),
        ("D28_5 pilot cash Y5", d["D28_5"], 73500),
        ("D23_1 op result Y1", d["D23_1"], -272000),
        ("D23_2 op result Y2", d["D23_2"], -347750),
        ("D23_3 op result Y3", d["D23_3"], -423500),
        ("D23_4 op result Y4", d["D23_4"], -771375),
        ("D23_5 op result Y5", d["D23_5"], -517750),
        ("CUM_5", d["CUM_5"], -2332375),
        ("D24 peak deficit", d["D24"], -2332375),
        ("D25 ask", d["D25"], 2798850),
        ("D34 Israeli SAM fee pool", d["D34"], 0.20e6),
        ("D18 sample per arm", d["D18"], 6000),
    ]
    print(f"{'value':28s} {'model':>16s} {'hand':>14s} {'delta %':>9s}")
    for name, m, h in hand:
        dl = (m - h) / h * 100
        print(f"{name:28s} {m:16,.4f} {h:14,.4f} {dl:+9.2f}{'  <-- >1%' if abs(dl) > 1 else ''}")
    print("\nextra:", {k: round(v, 4) for k, v in d.items() if k in ("D03", "D04", "D06a", "D06b", "D07a", "D07b", "D09", "D10", "D11", "D12", "D13", "D14", "D16", "D27", "D34", "D37", "D38")})
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
