# NEISS raw data — re-fetch instructions

The five NEISS annual case files (~60 MB each, ~300 MB total) are **not committed**
(see repo `.gitignore`) to keep the repository light. They are public and re-fetchable
exactly; every downstream number is reproducible from them via
`scripts/phase2_build_corpus.py`.

## Re-fetch (exact URLs)

```
for y in 2019 2020 2021 2022 2023; do
  curl -L "https://www.cpsc.gov/cgibin/NEISSQuery/Data/Archived%20Data/${y}/neiss${y}.tsv" \
       -o "data/raw/neiss/neiss${y}.tsv"
done
```

Tab-delimited, latin-1 encoded, 25 columns. Key fields used:
`Narrative_1` (free text), `Diagnosis`, `Fire_Involvement`, `Product_1/2/3`,
`Location`, `Disposition`, `Weight` (statistical weight for national estimates).

## Committed derivatives (reproducible from the above)
- `data/raw/neiss/NEISS_DataDictionary.xlsx` — CPSC code definitions (small; committed).
- `data/processed/case_corpus.csv` — CO-filtered cases with verbatim narratives + weights.

## Important data note (documented finding)
`Fire_Involvement` codes 1/2/3 ("Fire Involved") are **unreliable** for separating real
fires from non-fire CO calls: NEISS frequently sets them when the **fire department
attends a pure CO/gas-leak call with no actual fire**. The study therefore judges
fire involvement from the **narrative**, not the code (see `scripts/phase2_classify.py`).
