#!/usr/bin/env python3
"""
phase2_make_validation_sample.py  —  Track B, step 3a (Phase 2)

Draw a reproducible random validation sample (>= max(100, 10% of corpus)) and emit
a BLIND narratives file (case_id, year, NEISS context, narrative) with NO rule-based
verdicts, for an independent second-pass classification (Gate 2.2). The independent
labels are compared to the bulk classifier in phase2_validate.py.
"""
import csv
import math
import pathlib
import random

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "data/processed/case_corpus.csv"
OUT = ROOT / "data/processed/validation_sample_blind.csv"
SEED = 20260623

def main():
    rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
    n = max(100, math.ceil(0.10 * len(rows)))
    random.seed(SEED)
    sample = random.sample(rows, n)
    sample.sort(key=lambda r: r["case_id"])
    fields = ["case_id", "year", "diagnosis_code", "disposition_code", "location_code",
              "fire_involvement_code", "product_1", "product_2", "product_3", "narrative"]
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(sample)
    print(f"Validation sample: {n} of {len(rows)} cases (seed={SEED}) -> {OUT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
