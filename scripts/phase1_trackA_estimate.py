#!/usr/bin/env python3
"""
phase1_trackA_estimate.py  —  Track A, steps 2-3 (Phase 1)

From the extracted CPSC by-source deaths (data/processed/trackA_sources.csv):
  (2) compute ADDRESSABLE harm = in-scope furnace + tank-water-heater deaths/yr,
      multi-year averaged, with an explicit, RECS-grounded boiler carve-out; and
  (3) apply a transparent, PRE-REGISTERED preventable-fraction model (Low/Base/High)
      to produce the prevented-deaths range.

Every EXTERNAL fact carries a citation (see CITATIONS below). The preventable-
fraction factors are NOT a single published number (none exists for a furnace/
water-heater source-shutoff); they are a pre-registered, conservative precondition
decomposition, each factor grounded in a cited anchor and carried as a Low/Base/High
band. Track B (Phase 2) measures this fraction bottom-up and Gate 2.4 reconciles the
two tracks. This is the methodology's intended "fast, lower-resolution" first pass
(methodology Sec.8), explicitly provisional.

Outputs:
  data/processed/trackA_estimate.csv   (machine-readable result, consumed by Phase 3)
  prints a human summary.

Headline window: 2018-2022 (the "last 5 available years", per CLAUDE.md Phase 1).
Cross-reference window: 2020-2022 (CPSC's own 3-year headline).
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "data/processed/trackA_sources.csv"
OUT = ROOT / "data/processed/trackA_estimate.csv"

# ---------------------------------------------------------------------------
# PRE-REGISTERED PARAMETERS (locked in outputs/PREREGISTRATION.md before results)
# ---------------------------------------------------------------------------
# Boiler carve-out: the CPSC "Furnaces (incl. Boilers)" line bundles out-of-scope
# boilers. EIA RECS 2020 (Table HC6.1): fossil-fuel central warm-air furnaces heat
# ~60.39M homes (natural gas 53.26 + fuel oil 3.10 + propane 4.03); fossil steam/
# hot-water boilers heat ~8.13M (natural gas 6.51 + fuel oil 1.62). Boilers are
# 8.13 / (60.39+8.13) = 11.9% of the bundled stock. We carve out 12% of the CPSC
# furnace line (assumes equal per-unit CO-death rate; if anything boilers kill less
# per unit, so 12% is conservative -> removes slightly MORE from the device's count).
BOILER_CARVE = 0.12

# Preventable-fraction decomposition (each factor: probability a precondition holds
# for an in-scope furnace/water-heater CO death). Low / Base / High.
F_CONTROL = {"low": 0.55, "base": 0.70, "high": 0.85}   # controllability (RECS: forced-air dominates; CO-death units skew old)
F_LOCUS_PROG = {"low": 0.45, "base": 0.60, "high": 0.75}  # detectable + progressive (CPSC furnace failure-mode narrative; CO clinical lit)
DEVICE_FAIL = {"low": 0.15, "base": 0.10, "high": 0.05}   # non-actuation rate (pre-registered; CO/smoke-alarm reliability analog)

HEADLINE_WINDOW = (2018, 2022)
XREF_WINDOW = (2020, 2022)

CITATIONS = {
    "cpsc_deaths": "U.S. CPSC, 'Non-Fire Carbon Monoxide Deaths Associated with the Use of "
                   "Consumer Products: 2022 Annual Estimates' (pub. May 2026), Table 1 (pp.11-12) "
                   "and Table 2 (p.13-16). data/raw/cpsc_reports/cpsc_co_2022.pdf.",
    "recs_furnace": "U.S. EIA, Residential Energy Consumption Survey (RECS) 2020, Table HC6.1 "
                    "'Space heating in U.S. homes'. Fossil central warm-air furnaces ~60.39M homes; "
                    "fossil steam/hot-water boilers ~8.13M. data/raw/eia_recs/RECS2020_HC6.1_space_heating.pdf.",
    "cdc_burden": "U.S. CDC/NVSS & MMWR: ~430 unintentional non-fire CO deaths/yr (1999-2010 avg) and "
                  "~15,000 unintentional non-fire CO ED visits/yr. Used for magnitude context only "
                  "(CDC counts ALL sources incl. motor-vehicle exhaust; CPSC counts consumer products only).",
    "device_fail": "Device non-actuation discount 15/10/5% (Low/Base/High) pre-registered as a "
                   "conservative assumption; basis = CO/smoke-alarm field-reliability literature (analog). "
                   "Kept even absent an exact furnace-shutoff figure (removing it would favor the device).",
    "cpsc_generator_precedent": "U.S. CPSC portable-generator rulemaking counterfactual: source-shutoff "
                   "(auto-CO-shutoff generators) estimated to avert nearly all of ~511 real generator "
                   "fatalities -- the closest measured precedent that a SOURCE-shutoff can be highly "
                   "effective; used to bound the High ceiling, not the Base.",
}


def load_avgs():
    rows = {}
    with SRC.open() as f:
        for r in csv.DictReader(f):
            rows[r["category"]] = r
    return rows


def window_avg(row, lo, hi):
    yrs = range(lo, hi + 1)
    return sum(int(row[str(y)]) for y in yrs) / len(list(yrs))


def main():
    rows = load_avgs()
    results = []

    for wname, (lo, hi) in (("2018-2022", HEADLINE_WINDOW), ("2020-2022", XREF_WINDOW)):
        total = window_avg(rows["Total"], lo, hi)
        furn_raw = window_avg(rows["Furnaces (incl. Boilers)"], lo, hi)
        wh = window_avg(rows["Water Heaters"], lo, hi)

        furn_inscope = furn_raw * (1 - BOILER_CARVE)
        addressable = furn_inscope + wh
        addressable_nocarve = furn_raw + wh  # upper bound if no boiler carve-out

        share = addressable / total

        # preventable fraction per scenario
        frac = {}
        prevented = {}
        for sc in ("low", "base", "high"):
            frac[sc] = F_CONTROL[sc] * F_LOCUS_PROG[sc] * (1 - DEVICE_FAIL[sc])
            prevented[sc] = addressable * frac[sc]

        results.append({
            "window": wname,
            "total_deaths_yr": round(total, 2),
            "furnace_raw_deaths_yr": round(furn_raw, 2),
            "furnace_inscope_deaths_yr": round(furn_inscope, 2),
            "water_heater_deaths_yr": round(wh, 2),
            "addressable_deaths_yr": round(addressable, 2),
            "addressable_deaths_yr_nocarve": round(addressable_nocarve, 2),
            "addressable_share": round(share, 4),
            "prev_frac_low": round(frac["low"], 4),
            "prev_frac_base": round(frac["base"], 4),
            "prev_frac_high": round(frac["high"], 4),
            "prevented_deaths_low": round(prevented["low"], 2),
            "prevented_deaths_base": round(prevented["base"], 2),
            "prevented_deaths_high": round(prevented["high"], 2),
        })

    # write machine-readable result
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        w.writeheader()
        w.writerows(results)

    # sanity checks (Gate 1.3, 1.6)
    for r in results:
        assert 0 < r["addressable_share"] < 1, "addressable share out of (0,1)"
        assert r["prevented_deaths_high"] <= r["addressable_deaths_yr"] + 1e-9, "prevented > addressable"
        assert (r["prevented_deaths_low"] <= r["prevented_deaths_base"]
                <= r["prevented_deaths_high"]), "scenario ordering violated"

    print(f"Wrote {OUT.relative_to(ROOT)}\n")
    print("PRE-REGISTERED parameters:")
    print(f"  boiler carve-out      : {BOILER_CARVE:.0%}  (RECS-grounded)")
    print(f"  f_control (L/B/H)     : {F_CONTROL['low']}/{F_CONTROL['base']}/{F_CONTROL['high']}")
    print(f"  f_locus_progressive   : {F_LOCUS_PROG['low']}/{F_LOCUS_PROG['base']}/{F_LOCUS_PROG['high']}")
    print(f"  device non-actuation  : {DEVICE_FAIL['low']}/{DEVICE_FAIL['base']}/{DEVICE_FAIL['high']}")
    for r in results:
        print(f"\n=== {r['window']} ===")
        print(f"  total non-fire CO deaths/yr (CPSC)     : {r['total_deaths_yr']}")
        print(f"  in-scope furnace deaths/yr (boiler-carved): {r['furnace_inscope_deaths_yr']}  "
              f"(raw furnace+boiler line: {r['furnace_raw_deaths_yr']})")
        print(f"  tank water-heater deaths/yr            : {r['water_heater_deaths_yr']}")
        print(f"  ADDRESSABLE deaths/yr                  : {r['addressable_deaths_yr']}  "
              f"(= {r['addressable_share']:.1%} of total; no-carve upper {r['addressable_deaths_yr_nocarve']})")
        print(f"  preventable fraction  L/B/H           : "
              f"{r['prev_frac_low']:.1%} / {r['prev_frac_base']:.1%} / {r['prev_frac_high']:.1%}")
        print(f"  PREVENTED deaths/yr   L/B/H           : "
              f"{r['prevented_deaths_low']} / {r['prevented_deaths_base']} / {r['prevented_deaths_high']}")

    # dump citations next to the numbers for provenance (Gate 1.5)
    (ROOT / "data/processed/trackA_citations.json").write_text(json.dumps(CITATIONS, indent=2))
    print("\nProvenance written to data/processed/trackA_citations.json")


if __name__ == "__main__":
    main()
