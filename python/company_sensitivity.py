"""Company-level sensitivity (red-team #4/#6). Run from the root: python python/company_sensitivity.py
Reads python/data/assumptions.csv through model.py; every scenario is a change to those inputs.
Writes python/data/company_sensitivity_out.csv and figures/tab-company-sens.tex.
Scenario rules (nothing beyond the model horizon Y1-Y5 is extrapolated):
  pilot-to-paying 35%    paying clients (A26i_y, A26e_y) scaled by 0.35 / A17, since clients = pilots x A17
  orders per Euro client A11e = 500,000
  Europe one year later  A45 + 1, European paying-client series shifted one year later
  scan cost x2           A12 x 2 (cost to serve D11) and the scan part of A33a (named in its note) added once more
"""
import csv
import re
import model

ROOT = model.DATA.parent.parent
YEARS = model.YEARS
rows, base, meta = model.load_inputs()


def run(a):
    d = model.compute(a)
    be = next((y for y in YEARS if d[f"D23_{y}"] >= 0), None)
    return {"rev5": d["D20_5"], "deficit": -d["D24"], "ask": d["D25"], "be": be,
            "cum": [d[f"CUM_{y}"] for y in YEARS], "res5": d["D23_5"]}


def scenario(name):
    a = dict(base)
    if name == "pilot":
        k = 0.35 / a["A17"]
        for y in YEARS:
            for p in ("A26i", "A26e"):
                a[f"{p}_{y}"] *= k
        a["A17"] = 0.35
    elif name == "orders":
        a["A11e"] = 500_000
    elif name == "late":
        a["A45"] += 1
        eu = [base[f"A26e_{y}"] for y in YEARS]
        for y in YEARS:
            a[f"A26e_{y}"] = 0.0 if y == 1 else eu[y - 2]
    elif name == "scan":
        scan_part = float(re.search(r"(\d+) scan cost", meta["A33a"]["note"]).group(1))
        a["A33a"] += scan_part
        a["A12"] *= 2
    return a


SCEN = [("base", "Base case"),
        ("pilot", r"Pilot-to-paying 35\% (base 50\%)"),
        ("orders", r"Orders per European client 500\,k (base 1\,M)"),
        ("late", "Europe entry one year later (year 5)"),
        ("scan", "Scan cost doubled")]
res = [(k, label, run(scenario(k))) for k, label in SCEN]

with open(model.DATA / "company_sensitivity_out.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["scenario", "y5_revenue_usd", "y5_operating_result_usd", "peak_cumulative_deficit_usd",
                "funding_ask_usd", "run_rate_break_even_year"] + [f"cum_y{y}_usd" for y in YEARS])
    for k, _, r in res:
        w.writerow([k, round(r["rev5"]), round(r["res5"]), round(r["deficit"]), round(r["ask"]),
                    r["be"] if r["be"] else "outside model horizon"] + [round(c) for c in r["cum"]])


def usd(x):
    return r"\usd{" + f"{x:,.0f}".replace(",", r"\,") + "}"


lines = [r"% Company-level sensitivity (python/company_sensitivity.py). Caption and label tab:company-sens: qa-se.",
         r"\ctnumcols{4}", r"\begin{tabularx}{\textwidth}{WVVVV}", r"\toprule",
         r"\ctheaderrow\cthead{Scenario} & \cthead{Year-5 revenue} & \cthead{Peak deficit} & "
         r"\cthead{Funding ask} & \cthead{Run-rate break-even}\\", r"\midrule"]
for k, label, r in res:
    be = f"year {r['be']}" if r["be"] else "outside model horizon"
    lines.append(f"{label} & {usd(r['rev5'])} & {usd(r['deficit'])} & {usd(r['ask'])} & {be}" + r"\\")
lines += [r"\bottomrule", r"\end{tabularx}"]
(ROOT / "figures" / "tab-company-sens.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
for k, _, r in res:
    print(k, round(r["rev5"]), round(r["deficit"]), round(r["ask"]), r["be"], [round(c) for c in r["cum"]])
