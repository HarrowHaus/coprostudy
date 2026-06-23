#!/usr/bin/env python3
"""
phase2_validate.py  —  Track B, step 3b (Phase 2)

Compare the bulk rule-based classifier against the INDEPENDENT second-pass labels
on the same validation sample, and report agreement (Gate 2.2, threshold >=90%).
Writes outputs/tables/validation_accuracy.md.
"""
import csv
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
BULK = ROOT / "data/processed/case_corpus_classified.csv"
INDEP = ROOT / "data/processed/validation_independent.csv"
SAMPLE = ROOT / "data/processed/validation_sample_blind.csv"
OUT = ROOT / "outputs/tables/validation_accuracy.md"


def load(path, key, *cols):
    d = {}
    for r in csv.DictReader(path.open(encoding="utf-8")):
        d[r[key]] = {c: r[c] for c in cols}
    return d


def main():
    sample_ids = [r["case_id"] for r in csv.DictReader(SAMPLE.open(encoding="utf-8"))]
    bulk = load(BULK, "case_id", "preventability_verdict", "source_primary")
    indep = load(INDEP, "case_id", "preventability_verdict", "source_primary")

    n = len(sample_ids)
    v_agree = s_agree = 0
    disagreements = []
    # also an "in-scope-relevant" agreement: does each method agree on whether a case
    # is an in-scope Prevented? (the quantity that drives the fraction)
    confusion = Counter()
    for cid in sample_ids:
        b = bulk[cid]["preventability_verdict"]
        i = indep[cid]["preventability_verdict"]
        bs = bulk[cid]["source_primary"]
        isrc = indep[cid]["source_primary"]
        confusion[(i, b)] += 1
        if b == i:
            v_agree += 1
        else:
            disagreements.append((cid, isrc, i, bs, b))
        # source agreement (normalize 'other'/out-of-scope buckets to scope class)
        def scope_class(s):
            if s in {"furnace", "tank_water_heater", "both"}:
                return "in_scope"
            if s == "unknown":
                return "unknown"
            return "out_of_scope"
        if scope_class(bs) == scope_class(isrc):
            s_agree += 1

    v_rate = 100 * v_agree / n
    s_rate = 100 * s_agree / n

    # Cohen-style note: verdict agreement is the gate metric.
    lines = []
    lines.append("# Validation Accuracy — Track B Classification (Gate 2.2)\n")
    lines.append(f"**Sample:** {n} cases (>= max(100, 10% of corpus); seed-reproducible).")
    lines.append("**Design:** the bulk **rule-based** classifier vs an **independent** second-pass "
                 "classification of the SAME cases, performed blind to the rule output (two different "
                 "instruments applying the same rubric — methodology Sec.11).\n")
    lines.append("| Metric | Agreement |")
    lines.append("|---|---|")
    lines.append(f"| **Preventability verdict (gate metric)** | **{v_rate:.1f}%** ({v_agree}/{n}) |")
    lines.append(f"| Scope class (in-scope / out-of-scope / unknown) | {s_rate:.1f}% ({s_agree}/{n}) |")
    gate = "PASS" if v_rate >= 90 else "FAIL"
    lines.append(f"\n**GATE 2.2 (>= 90% verdict agreement): {gate}**\n")

    lines.append("## Verdict confusion (rows = independent, cols = bulk)")
    verdicts = ["Excluded", "Out of Scope", "Unknown-Source", "Indeterminate", "Not Prevented", "Prevented"]
    header = "| independent \\ bulk | " + " | ".join(verdicts) + " |"
    lines.append(header)
    lines.append("|" + "---|" * (len(verdicts) + 1))
    for iv in verdicts:
        row = [str(confusion.get((iv, bv), 0)) for bv in verdicts]
        lines.append(f"| {iv} | " + " | ".join(row) + " |")

    lines.append(f"\n## Disagreements ({len(disagreements)})")
    if disagreements:
        lines.append("| case_id | indep source | indep verdict | bulk source | bulk verdict |")
        lines.append("|---|---|---|---|---|")
        for cid, isrc, iv, bs, bv in disagreements:
            lines.append(f"| {cid} | {isrc} | {iv} | {bs} | {bv} |")
    else:
        lines.append("None.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n")
    print(f"Verdict agreement: {v_rate:.1f}% ({v_agree}/{n})  -> GATE 2.2 {gate}")
    print(f"Scope-class agreement: {s_rate:.1f}%")
    print(f"Disagreements: {len(disagreements)}")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
