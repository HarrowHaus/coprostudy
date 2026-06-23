#!/usr/bin/env python3
"""
phase2_build_corpus.py  —  Track B, step 1 (Phase 2)

Assemble the case corpus for case-level classification from the cached NEISS
annual files (2019-2023). One row per CO-relevant ED-treated incident, carrying
the verbatim source narrative.

NEISS = CPSC National Electronic Injury Surveillance System (sample-based ED
injury/exposure surveillance with short free-text narratives). Source files:
data/raw/neiss/neiss{2019..2023}.tsv (downloaded from cpsc.gov, see SOURCE_STATUS.md).

CO filter: keep a record iff its narrative explicitly references carbon monoxide
via an unambiguous token. We deliberately EXCLUDE bare " CO " because in clinical
shorthand "C/O" = "complains of"; we require CO to be bound to a CO-specific word
(POISON/EXPOSURE/ALARM/DETECTOR/LEVEL/TOX/INHAL/LEAK/GAS) or use the explicit
"CARBON MONOXIDE" / carboxyhemoglobin tokens.

Output: data/processed/case_corpus.csv (case_id, year, source narrative, raw NEISS
context fields). Classification happens in phase2_classify.py.
"""
import csv
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
NEISS_DIR = ROOT / "data/raw/neiss"
OUT = ROOT / "data/processed/case_corpus.csv"
YEARS = range(2019, 2024)

# Unambiguous CO references (case-insensitive). Avoid bare " CO " (== "c/o").
CO_INCLUDE = re.compile(
    r"CARBON\s*MONOXIDE"
    r"|MONOXIDE"
    r"|CARBOXYHEMOGLOBIN|COHGB|COHB\b"
    r"|\bCO[\s\-]?(POISON|TOX|EXPOSURE|EXPOSED|INHAL|ALARM|DETECT|LEVEL|LEAK|GAS|FUME|INTOX|EXP\b)",
    re.I,
)
# Guard: drop matches where the only hit is "C/O" style (defensive; CO_INCLUDE already avoids it).
CO_BARE_CO = re.compile(r"\bC/O\b", re.I)


def main():
    csv.field_size_limit(10_000_000)
    rows = []
    seen = set()
    per_year = {}
    for y in YEARS:
        path = NEISS_DIR / f"neiss{y}.tsv"
        cnt = 0
        with path.open(encoding="latin-1") as f:
            r = csv.DictReader(f, delimiter="\t")
            for rec in r:
                narr = (rec.get("Narrative_1") or "").strip()
                if not narr:
                    continue
                if not CO_INCLUDE.search(narr):
                    continue
                cid = (rec.get("CPSC_Case_Number") or "").strip()
                key = (y, cid, narr[:40])
                if key in seen:
                    continue
                seen.add(key)
                rows.append({
                    "case_id": f"NEISS-{y}-{cid}",
                    "year": y,
                    "neiss_case_number": cid,
                    "treatment_date": (rec.get("Treatment_Date") or "").strip(),
                    "age": (rec.get("Age") or "").strip(),
                    "sex": (rec.get("Sex") or "").strip(),
                    "diagnosis_code": (rec.get("Diagnosis") or "").strip(),
                    "disposition_code": (rec.get("Disposition") or "").strip(),
                    "location_code": (rec.get("Location") or "").strip(),
                    "fire_involvement_code": (rec.get("Fire_Involvement") or "").strip(),
                    "product_1": (rec.get("Product_1") or "").strip(),
                    "product_2": (rec.get("Product_2") or "").strip(),
                    "product_3": (rec.get("Product_3") or "").strip(),
                    "weight": (rec.get("Weight") or "").strip(),
                    "narrative": narr,
                })
                cnt += 1
        per_year[y] = cnt

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print(f"Corpus written: {OUT.relative_to(ROOT)}  ({len(rows)} cases)")
    for y in YEARS:
        print(f"  {y}: {per_year[y]} CO cases")


if __name__ == "__main__":
    main()
