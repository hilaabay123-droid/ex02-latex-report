"""Company-level sensitivity (red-team #4/#6/#1/#2). Run from the root: python python/company_sensitivity.py
Reads python/data/assumptions.csv through model.py; every scenario is a change to those inputs.
Writes python/data/company_sensitivity_out.csv and figures/tab-company-sens.tex.
Scenario rules (nothing beyond the model horizon Y1-Y5 is extrapolated, except where labelled):
  pilot-to-paying 35%    paying clients (A26i_y, A26e_y) scaled by 0.35 / A17, since clients = pilots x A17
  orders per Euro client A11e = 500,000
  low-touch size 250k    the low-touch share of European clients (1 - A31e = 75%) converts at A51 = 250,000 orders
                         instead of 1M (anchor: average Israeli client D38). Not in the base case.
  Europe one year later  A45 + 1, European paying-client series shifted one year later
  Europe in year 3       ALTERNATIVE plan: A45 = 3; European pilots one year earlier (36 in Y3, 60 in Y4-Y5);
                         clients at end of year = A17 x previous-year pilots (the base rule): Y4 = 18 (shifted from the
                         base Y5), Y5 = 30 (EXTRAPOLATED by the same rule from the 60 pilots of Y4);
                         headcount 9 in Y3, 12 in Y4-Y5. The funnel check is run and reported for it.
  scan cost x2           A12 x 2 (cost to serve D11) and the scan part of A33a (named in its note) added once more
"""
import csv
import re
from decimal import Decimal, ROUND_HALF_UP
import model

ROOT = model.DATA.parent.parent
YEARS = model.YEARS
rows, base, meta = model.load_inputs()


def run(a):
    d = model.compute(a)
    be = next((y for y in YEARS if d[f"D23_{y}"] >= 0), None)
    _, fails = model.funnel_check(a)
    return {"rev5": d["D20_5"], "deficit": -d["D24"], "ask": d["D25"], "be": be,
            "cum": [d[f"CUM_{y}"] for y in YEARS], "res5": d["D23_5"], "be_clients": d["D46"],
            "eu_end5": a["A26e_5"], "funnel_fails": fails, "rev": [d[f"D20_{y}"] for y in YEARS],
            "res": [d[f"D23_{y}"] for y in YEARS]}


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
    elif name == "lowtouch":
        a["_lowtouch"] = 1
    elif name == "late":
        a["A45"] += 1
        eu = [base[f"A26e_{y}"] for y in YEARS]
        for y in YEARS:
            a[f"A26e_{y}"] = 0.0 if y == 1 else eu[y - 2]
    elif name == "eu3":
        a["A45"] = 3
        for y, v in zip(YEARS, (0, 0, 0, a["A17"] * a["A26eq_4"], a["A17"] * a["A26eq_5"])):
            a[f"A26e_{y}"] = v
        for y, v in ((3, 9), (4, 12), (5, 12)):
            a[f"A25_{y}"] = v
    elif name == "scan":
        scan_part = float(re.search(r"(\d+) scan cost", meta["A33a"]["note"]).group(1))
        a["A33a"] += scan_part
        a["A12"] *= 2
    return a


SCEN = [("base", "Base case"),
        ("pilot", r"Pilot conv. 35\%"),
        ("orders", r"Orders 500\,k"),
        ("lowtouch", r"Low-touch 250\,k"),
        ("late", "Europe +1 yr"),
        ("scan", r"Scan cost $\times$2"),
        ("eu3", "Europe in yr 3")]
res = [(k, label, run(scenario(k))) for k, label in SCEN]

with open(model.DATA / "company_sensitivity_out.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["scenario", "y5_revenue_usd", "y5_operating_result_usd", "peak_cumulative_deficit_usd",
                "funding_ask_usd", "run_rate_break_even_year", "european_clients_end_y5",
                "run_rate_break_even_european_clients", "funnel_check"] + [f"cum_y{y}_usd" for y in YEARS])
    for k, _, r in res:
        w.writerow([k, round(r["rev5"]), round(r["res5"]), round(r["deficit"]), round(r["ask"]),
                    r["be"] if r["be"] else "outside model horizon", format(r["eu_end5"], ".4g"),
                    round(r["be_clients"], 1), "OK" if not r["funnel_fails"] else "FAILED: " + " | ".join(r["funnel_fails"])]
                   + [round(c) for c in r["cum"]])


def half_up(x):
    """Round half away from zero (not Python's round-half-even)."""
    return int(Decimal(repr(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def kfmt(x):
    """US$ thousand, rounded; thousands separator as thin space."""
    n = half_up(x / 1000)
    return f"{n:,}".replace(",", r"\,").replace("-", "$-$")


lines = [r"% Company-level sensitivity (python/company_sensitivity.py). All amounts US$ thousand. Caption and label tab:company-sens: qa-se.",
         r"\ctnumcols{5}", r"\begin{tabularx}{\textwidth}{WVVVVV}", r"\toprule",
         r"\ctheaderrow\cthead{Scenario (US\$ thousand)} & \cthead{Y5 revenue} & \cthead{Y5 result} & "
         r"\cthead{Peak deficit} & \cthead{Ask} & \cthead{Break-even clients}\\", r"\midrule"]
for key, label, r in res:
    lines.append(f"{label} & {kfmt(r['rev5'])} & {kfmt(r['res5'])} & {kfmt(r['deficit'])} & {kfmt(r['ask'])} & {half_up(r['be_clients'])}" + r"\\")
lines += [r"\bottomrule", r"\end{tabularx}"]
(ROOT / "figures" / "tab-company-sens.tex").write_text("\n".join(lines) + "\n", encoding="utf-8")
for key, _, r in res:
    print(key, round(r["rev5"]), round(r["res5"]), round(r["deficit"]), round(r["ask"]), r["be"], round(r["be_clients"], 1),
          "eu_end5", r["eu_end5"], "funnel", "OK" if not r["funnel_fails"] else r["funnel_fails"], [round(c) for c in r["cum"]])
