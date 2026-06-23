#!/usr/bin/env python3
"""
phase1_extract_cpsc.py  —  Track A, step 1 (Phase 1)

Extract the by-source non-fire CO death counts from the latest CPSC
"Non-Fire Carbon Monoxide Deaths Associated with the Use of Consumer Products"
annual report (2022 edition, which tabulates 2012-2022), and write a tidy,
fully-traceable CSV to data/processed/trackA_sources.csv.

Source of truth:
  data/raw/cpsc_reports/cpsc_co_2022.pdf
    Table 1 (pp. 11-12): "Estimated Non-Fire CO Poisoning Deaths by Associated
                          Fuel-Burning Consumer Product, 2012-2022"
    Table 2 (pp. 14-16): same totals organized by fuel type; used ONLY to read
                          the top-level "Multiple Products" category (absent from Table 1).

Parsing rule (verified against the printed Total row):
  Each printed data row is:  <label> <2020-2022 avg> <avg %> <2012> ... <2022>
  i.e. label + 13 tokens (avg, percent, then 11 annual values).
  -> the LAST 11 tokens are the annual series 2012..2022
  -> the FIRST token after the label is the CPSC-published 2020-2022 average
  CPSC suppresses small/zero cells with "*"; we map "*" -> 0 (a slight, documented
  UNDER-count that never touches the in-scope furnace/water-heater lines, which
  are never suppressed).

No data is modified; this script only reads the cached PDF and emits a CSV.
"""
import re
import csv
import pathlib
import pdfplumber

ROOT = pathlib.Path(__file__).resolve().parents[1]
PDF = ROOT / "data/raw/cpsc_reports/cpsc_co_2022.pdf"
OUT = ROOT / "data/processed/trackA_sources.csv"

YEARS = list(range(2012, 2023))  # 2012..2022 inclusive (11 years)

# Top-level, mutually-exclusive product categories that partition the national total.
# (Heating Systems and Engine-Driven Tools are parents of the indented fuel/product
#  sub-rows; we capture them at the top level for reconciliation, and separately
#  capture the in-scope sub-rows Furnaces / Wall-Floor Furnaces for addressable harm.)
TOP_LEVEL = [
    "Total",
    "Heating Systems",
    "Charcoal/Charcoal Grills",
    "Engine-Driven Tools",
    "Ranges or Ovens",
    "Water Heaters",
    "Pool Heaters",
    "Lanterns",
    "Grills, Camp Stoves",
    "Multiple Products",
]
# In-scope / borderline sub-rows under "Heating Systems" we also need explicitly.
SUBROWS = [
    "Furnaces (incl. Boilers)",   # IN SCOPE (bundles out-of-scope boilers -> carved out in step 2)
    "Wall/Floor Furnaces",        # borderline (gravity/standing-pilot) -> excluded from Base addressable
    "Portable Heaters",           # out of scope (space heaters)
    "Room/Space Heaters",         # out of scope
    "Unspecified Heater/System",  # out of scope (cannot attribute to furnace)
]
WANTED = TOP_LEVEL + SUBROWS


def tok_to_int(t: str) -> int:
    """Map a printed cell token to an integer count. '*' (suppressed/<1) -> 0."""
    t = t.strip()
    if t in {"*", "", "**"}:
        return 0
    t = t.replace(",", "")
    return int(t)


def parse_row(line: str, label: str):
    """Given a text line that starts with `label`, return the 11 annual ints 2012..2022
    and the CPSC-published 2020-2022 average. Returns None if it doesn't parse."""
    rest = line[len(label):].strip()
    # tokens are integers or '*' or percentages like '10%'/'<1%'; drop percentages.
    raw = rest.split()
    toks = [t for t in raw if not (t.endswith("%") or t.startswith("<"))]
    # Expect: avg + 11 years = 12 numeric/'*' tokens (percent already dropped).
    if len(toks) < 12:
        return None
    avg = tok_to_int(toks[0])
    years = [tok_to_int(t) for t in toks[-11:]]
    return avg, years


def main():
    rows = {}
    with pdfplumber.open(PDF) as pdf:
        # Table 1 lives on pp.11-12 (idx 10-11); Multiple Products on Table 2 pp.14-16.
        pages_text = {i: (pdf.pages[i].extract_text() or "") for i in range(10, 17)}

    for label in WANTED:
        found = None
        for i in sorted(pages_text):
            for line in pages_text[i].split("\n"):
                s = line.strip()
                if s.startswith(label):
                    parsed = parse_row(s, label)
                    if parsed:
                        found = (i + 1, parsed)  # 1-based page
                        break
            if found:
                break
        if not found:
            raise SystemExit(f"FATAL: could not locate/parse row for '{label}'")
        page, (avg, years) = found
        rows[label] = {"page": page, "cpsc_avg_2020_2022": avg,
                       **{str(y): v for y, v in zip(YEARS, years)}}

    # ---- write tidy CSV -------------------------------------------------------
    IN_SCOPE = {"Furnaces (incl. Boilers)", "Water Heaters"}
    BORDERLINE = {"Wall/Floor Furnaces"}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = (["category", "row_type", "scope", "source_table_page",
                   "cpsc_avg_2020_2022"] + [str(y) for y in YEARS]
                  + ["avg_2018_2022", "avg_2020_2022_computed"])
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for label in WANTED:
            r = rows[label]
            ann = [r[str(y)] for y in YEARS]
            avg5 = round(sum(r[str(y)] for y in range(2018, 2023)) / 5, 3)
            avg3 = round(sum(r[str(y)] for y in range(2020, 2023)) / 3, 3)
            scope = ("in_scope" if label in IN_SCOPE
                     else "borderline_excluded" if label in BORDERLINE
                     else "total" if label == "Total"
                     else "out_of_scope" if label in SUBROWS
                     else "out_of_scope")
            row_type = "subrow" if label in SUBROWS else ("total" if label == "Total" else "top_level")
            w.writerow({"category": label, "row_type": row_type, "scope": scope,
                        "source_table_page": r["page"],
                        "cpsc_avg_2020_2022": r["cpsc_avg_2020_2022"],
                        **{str(y): v for y, v in zip(YEARS, ann)},
                        "avg_2018_2022": avg5, "avg_2020_2022_computed": avg3})

    # ---- reconciliation (Gate 1.1) -------------------------------------------
    top = [l for l in TOP_LEVEL if l != "Total"]
    print(f"Extracted {len(rows)} rows from {PDF.name} -> {OUT.relative_to(ROOT)}")
    print("\nReconciliation (Gate 1.1): top-level categories vs printed Total")
    for window, yrs in (("2020-2022", range(2020, 2023)), ("2018-2022", range(2018, 2023))):
        n = len(list(yrs))
        total = sum(rows["Total"][str(y)] for y in yrs) / n
        cat_sum = sum(sum(rows[l][str(y)] for y in yrs) / n for l in top)
        pct = 100 * (cat_sum - total) / total
        flag = "PASS" if abs(pct) <= 5 else "FAIL"
        print(f"  {window}: sum(categories)={cat_sum:.1f}  total={total:.1f}  "
              f"delta={pct:+.1f}%  [{flag}]")


if __name__ == "__main__":
    main()
