#!/usr/bin/env python3
"""
phase3_tables.py  —  Phase 3 (sensitivity & output tables)

Produce Tables 1-4 (methodology Sec.12) as both .md and .csv in outputs/tables/,
plus a recomputed occupancy split for Table 4. Deaths come from Track A (CPSC,
conservative); injuries from Track B (NEISS weighted) x the Track B injury fraction.
Tracks are NOT averaged (Gate 2.4): each fraction applies only to its own outcome.

Every figure here is computed from committed inputs:
  - data/processed/trackA_estimate.csv   (deaths: addressable + fraction)
  - data/processed/trackB_estimate.csv   (injury preventable fraction)
  - data/processed/case_corpus_classified.csv + case_corpus.csv (NEISS weights, occupancy)
Device installed-base denominators are from EIA RECS 2020 HC6.1 (cited inline).
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TBL = ROOT / "outputs/tables"
YEARS_NEISS = 5

# ---- in-scope device installed base (EIA RECS 2020, Table HC6.1) -------------
# Fossil-fuel central warm-air (forced-air) furnaces -- the device's primary install
# (mounts in the supply duct ~6 ft from the bend). Counts in millions of homes.
# SF = single-family detached + attached + mobile; MF = 2-4 unit + 5+ unit apartments.
FURNACE_HOMES_M = {
    "SF": 46.40 + 4.01 + 2.23,   # detached + attached + mobile = 52.64
    "MF": 2.94 + 4.80,           # 2-4 unit + 5+ unit            = 7.74
}
FURNACE_HOMES_M["total"] = FURNACE_HOMES_M["SF"] + FURNACE_HOMES_M["MF"]
RECS_CITE = "EIA RECS 2020 Table HC6.1 (fossil central warm-air furnaces: 60.38M homes; SF 52.64M, MF 7.74M)."


def load1(path):
    return list(csv.DictReader(path.open(encoding="utf-8")))


def neiss_addressable_injuries():
    """National weighted in-scope (furnace+WH) CO ED visits/yr, and SF/MF split among
    cases with an identifiable dwelling type."""
    import re
    cls = load1(ROOT / "data/processed/case_corpus_classified.csv")
    corpus = {r["case_id"]: r for r in load1(ROOT / "data/processed/case_corpus.csv")}
    inscope = [r for r in cls if r["source_primary"] in {"furnace", "tank_water_heater", "both"}
               and r["preventability_verdict"] in {"Prevented", "Not Prevented", "Indeterminate"}]
    MF = re.compile(r"\bAPARTMENT|\bAPT\b|\bCONDO|\bUNIT\b|COMPLEX|\bDUPLEX|TENANT|LANDLORD|HIGH[\s-]?RISE", re.I)
    SF = re.compile(r"\bHOUSE\b|\bHOME\b|RESIDENCE|\bTRAILER\b|MOBILE\s*HOME|BASEMENT", re.I)

    def wt(r):
        try:
            return float(corpus[r["case_id"]]["weight"])
        except Exception:
            return 0.0

    total = sum(wt(r) for r in inscope) / YEARS_NEISS
    furn = sum(wt(r) for r in inscope if r["source_primary"] == "furnace") / YEARS_NEISS
    wh = sum(wt(r) for r in inscope if r["source_primary"] == "tank_water_heater") / YEARS_NEISS
    sf = sum(wt(r) for r in inscope if SF.search(r["narrative"]) and not MF.search(r["narrative"]))
    mf = sum(wt(r) for r in inscope if MF.search(r["narrative"]))
    known = sf + mf
    return {"total": total, "furnace": furn, "water_heater": wh,
            "sf_share": sf / known, "mf_share": mf / known}


def write_table(name, header, rows, note=""):
    # csv
    with (TBL / f"{name}.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    # md
    md = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for r in rows:
        md.append("| " + " | ".join(str(c) for c in r) + " |")
    if note:
        md.append("")
        md.append(note)
    (TBL / f"{name}.md").write_text("\n".join(md) + "\n")


def main():
    TBL.mkdir(parents=True, exist_ok=True)
    A = {r["window"]: r for r in load1(ROOT / "data/processed/trackA_estimate.csv")}["2018-2022"]
    B = load1(ROOT / "data/processed/trackB_estimate.csv")[0]
    inj = neiss_addressable_injuries()

    add_deaths = float(A["addressable_deaths_yr"])               # 28.6
    furn_deaths = float(A["furnace_inscope_deaths_yr"])          # 20.8 (boiler-carved)
    wh_deaths = float(A["water_heater_deaths_yr"])               # 7.8
    add_inj = inj["total"]                                       # ~1273

    a_frac = {s: float(A[f"prev_frac_{s}"]) for s in ("low", "base", "high")}
    b_frac = {s: float(B[f"prev_frac_{s}"]) for s in ("low", "base", "high")}

    # ---- TABLE 1: addressable harm (per year, multi-year averaged) ----------
    t1 = [
        ["Furnaces (in-scope, boiler-carved)", f"{furn_deaths:.1f}", f"{inj['furnace']:,.0f}",
         "CPSC 2022 Table1 (deaths, 2018-2022 avg); NEISS 2019-2023 weighted (injuries)"],
        ["Tank water heaters", f"{wh_deaths:.1f}", f"{inj['water_heater']:,.0f}",
         "CPSC 2022 Table1 (deaths); NEISS weighted (injuries)"],
        ["Total addressable", f"{add_deaths:.1f}", f"{add_inj:,.0f}", "Sum of furnace + tank water heater"],
    ]
    write_table("table1_addressable_harm", ["Source", "Deaths/yr", "ER injuries/yr", "Basis"], t1,
                note="Deaths: CPSC consumer-product non-fire CO, 2018-2022 avg, furnace line carved "
                     "-12% for bundled out-of-scope boilers (RECS-grounded). Injuries: NEISS national "
                     "weighted estimate, 2019-2023; boilers route to a separate out-of-scope NEISS "
                     "category so no carve-out applies.")

    # ---- TABLE 2: preventable fraction (both tracks) ------------------------
    t2 = []
    for s in ("low", "base", "high"):
        t2.append([s.capitalize(), f"{a_frac[s]:.1%}", f"{b_frac[s]:.1%}",
                   "Track A=deaths (CPSC+model); Track B=injuries (NEISS bottom-up)"])
    write_table("table2_preventable_fraction",
                ["Scenario", "Deaths fraction (Track A)", "Injuries fraction (Track B)", "Source"], t2,
                note="Tracks are NOT averaged. They reconcile as a documented band (deaths are less "
                     "preventable than injuries; ranges overlap). Each fraction is applied only to its "
                     "own outcome below.")

    # ---- TABLE 3: prevented harm at scale (if universally installed) --------
    t3 = []
    for s in ("low", "base", "high"):
        d = add_deaths * a_frac[s]
        i = add_inj * b_frac[s]
        t3.append([s.capitalize(), f"{d:.1f}", f"{i:,.0f}"])
    write_table("table3_prevented_at_scale", ["Scenario", "Deaths averted/yr", "Injuries averted/yr"], t3,
                note="Deaths averted = addressable deaths x Track A fraction; injuries averted = "
                     "addressable injuries x Track B fraction. Universal-installation upper reference.")

    # ---- TABLE 4: per-device-year harm reduction, BY OCCUPANCY --------------
    # numerator harm split by occupancy (NEISS known-dwelling split, applied to both
    # outcomes -- documented assumption: appliance-occupancy distribution is a property
    # of where the in-scope appliances physically are).
    occ = {"Single-family": ("SF", inj["sf_share"]), "Multifamily/commercial": ("MF", inj["mf_share"])}
    t4 = []
    for label, (key, share) in occ.items():
        dev_m = FURNACE_HOMES_M[key]                      # millions of device-homes
        dev = dev_m * 1e6
        for s in ("low", "base", "high"):
            d_av = add_deaths * a_frac[s] * share
            i_av = add_inj * b_frac[s] * share
            d_per_k = d_av / dev * 1000
            i_per_k = i_av / dev * 1000
            d_per_100k = d_av / dev * 1e5
            i_per_100k = i_av / dev * 1e5
            t4.append([label, s.capitalize(), f"{dev_m:.1f}",
                       f"{d_per_k:.5f}", f"{i_per_k:.4f}",
                       f"{d_per_100k:.4f}", f"{i_per_100k:.3f}"])
    write_table("table4_per_device_year_by_occupancy",
                ["Occupancy", "Scenario", "Device-homes (millions)",
                 "Deaths averted /1,000 dev-yr", "Injuries averted /1,000 dev-yr",
                 "Deaths averted /100,000 dev-yr", "Injuries averted /100,000 dev-yr"], t4,
                note=f"Device base: {RECS_CITE} Occupancy harm split from NEISS in-scope cases with "
                     f"identifiable dwelling type: SF {inj['sf_share']:.0%} / MF {inj['mf_share']:.0%} "
                     f"(thin MF sample; ~45% of cases had no stated dwelling type -- a documented "
                     f"limitation). FINDING: in-scope furnace/tank-WH CO harm is single-family-dominant; "
                     f"multifamily/commercial CO risk is dominated by OUT-OF-SCOPE central boilers, so "
                     f"this device's per-device harm reduction concentrates in single-family.")

    # ---- console summary ----------------------------------------------------
    print("Tables written to outputs/tables/ (.md + .csv): table1..table4")
    print(f"\nTable 1 addressable: deaths {add_deaths:.1f}/yr, injuries {add_inj:,.0f}/yr")
    print(f"Table 2 fractions: deaths {a_frac['low']:.0%}/{a_frac['base']:.0%}/{a_frac['high']:.0%}; "
          f"injuries {b_frac['low']:.0%}/{b_frac['base']:.0%}/{b_frac['high']:.0%}")
    print(f"Table 3 Base averted: deaths {add_deaths*a_frac['base']:.1f}/yr, injuries {add_inj*b_frac['base']:,.0f}/yr")
    print(f"Table 4 occupancy split: SF {inj['sf_share']:.0%} / MF {inj['mf_share']:.0%}; "
          f"devices SF {FURNACE_HOMES_M['SF']:.1f}M / MF {FURNACE_HOMES_M['MF']:.1f}M")


if __name__ == "__main__":
    main()
