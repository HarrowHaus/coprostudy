#!/usr/bin/env python3
"""
phase2_aggregate.py  —  Track B, step 4 (Phase 2)

Aggregate the case-level verdicts into a bottom-up preventable fraction with the
three sensitivity scenarios (methodology Sec.10), and reconcile against Track A
(Gate 2.4).

IMPORTANT FRAMING: Track B is built on NEISS, which is ED-treated INJURY/exposure
surveillance. So Track B's preventable fraction is an INJURY fraction; Track A's is
a DEATH fraction. They describe related-but-different populations (deaths skew more
severe/acute/less-preventable than injuries). We therefore reconcile the two as a
documented band and DO NOT average them; each fraction is later applied to its own
outcome (deaths vs injuries) in Phase 3.

Scenario levers (mapping Sec.10 to the case data):
  - In-scope addressable = Prevented + Not Prevented + Indeterminate (rubric).
  - Base : verdict as classified; device non-actuation discount 10%.
  - Low  : also drop low-confidence Prevented verdicts (treat as not prevented);
           non-actuation 15%.
  - High : also credit uncertain-controllability cases (would be prevented if the
           appliance is in fact interruptible) and apportion a fraction (25%) of
           Unknown-Source cases into the in-scope denominator+numerator;
           non-actuation 5%.
"""
import csv
import json
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLS = ROOT / "data/processed/case_corpus_classified.csv"
OUT = ROOT / "data/processed/trackB_estimate.csv"

DEVICE_FAIL = {"low": 0.15, "base": 0.10, "high": 0.05}
HIGH_UNKNOWN_APPORTION = 0.25  # High only: literature-style apportionment of unknown-source


def main():
    rows = list(csv.DictReader(CLS.open(encoding="utf-8")))
    inscope = [r for r in rows if r["source_primary"] in {"furnace", "tank_water_heater", "both"}
               and r["preventability_verdict"] in {"Prevented", "Not Prevented", "Indeterminate"}]
    n_in = len(inscope)
    prevented = [r for r in inscope if r["preventability_verdict"] == "Prevented"]
    notprev = [r for r in inscope if r["preventability_verdict"] == "Not Prevented"]
    indet = [r for r in inscope if r["preventability_verdict"] == "Indeterminate"]
    unknown_src = [r for r in rows if r["preventability_verdict"] == "Unknown-Source"]

    p_high_conf = [r for r in prevented if r["verdict_confidence"] in {"high", "medium"}]
    # cases marked Not Prevented specifically because controllability was uncertain
    uncertain_ctrl = [r for r in notprev if "uncertain" in r["notes"]]

    # ----- scenario fractions (mechanical), then apply device-failure discount -----
    res = {}

    # Base
    base_mech = len(prevented) / n_in
    res["base"] = base_mech * (1 - DEVICE_FAIL["base"])

    # Low: only medium/high-confidence prevented count
    low_mech = len(p_high_conf) / n_in
    res["low"] = low_mech * (1 - DEVICE_FAIL["low"])

    # High: prevented + uncertain-controllability credited; plus unknown apportionment
    extra_unknown = round(HIGH_UNKNOWN_APPORTION * len(unknown_src))
    high_num = len(prevented) + len(uncertain_ctrl) + extra_unknown
    high_den = n_in + extra_unknown
    high_mech = high_num / high_den
    res["high"] = high_mech * (1 - DEVICE_FAIL["high"])

    # ensure ordering
    assert res["low"] <= res["base"] <= res["high"], "Track B scenario ordering violated"

    out = {
        "track": "B (NEISS injuries, bottom-up)",
        "corpus_total": len(rows),
        "in_scope_addressable": n_in,
        "prevented": len(prevented),
        "not_prevented": len(notprev),
        "indeterminate": len(indet),
        "unknown_source": len(unknown_src),
        "uncertain_controllability": len(uncertain_ctrl),
        "prev_frac_low": round(res["low"], 4),
        "prev_frac_base": round(res["base"], 4),
        "prev_frac_high": round(res["high"], 4),
        "base_mechanical": round(base_mech, 4),
    }
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out.keys()))
        w.writeheader(); w.writerow(out)

    print(f"In-scope addressable cases: {n_in}  "
          f"(Prevented {len(prevented)}, Not Prevented {len(notprev)}, Indeterminate {len(indet)})")
    print(f"Unknown-source (tracked separately): {len(unknown_src)}")
    print(f"Uncertain-controllability (Not Prevented in Base): {len(uncertain_ctrl)}")
    print(f"\nTrack B preventable fraction (INJURIES), realized incl. device-failure discount:")
    print(f"  Low {res['low']:.1%}  /  Base {res['base']:.1%}  /  High {res['high']:.1%}")
    print(f"  (Base mechanical, pre-discount: {base_mech:.1%})")

    # ----- Gate 2.4 reconciliation vs Track A -----
    ta = next(csv.DictReader((ROOT / "data/processed/trackA_estimate.csv").open()))
    a_low, a_base, a_high = float(ta["prev_frac_low"]), float(ta["prev_frac_base"]), float(ta["prev_frac_high"])
    print("\n--- Gate 2.4 reconciliation ---")
    print(f"  Track A (deaths):  Low {a_low:.1%} / Base {a_base:.1%} / High {a_high:.1%}")
    print(f"  Track B (injuries):Low {res['low']:.1%} / Base {res['base']:.1%} / High {res['high']:.1%}")
    overlap = not (res["high"] < a_low or a_high < res["low"])
    print(f"  Ranges overlap: {overlap}")
    print(f"  Base ratio B/A: {res['base']/a_base:.2f}x")


if __name__ == "__main__":
    main()
