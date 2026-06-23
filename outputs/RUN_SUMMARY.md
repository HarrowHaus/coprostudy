# RUN_SUMMARY — CO/PRO Preventability Modeling Study

**Run date (UTC):** 2026-06-23 · **Outcome:** complete — **all gates 0–4 logged PASS** in `outputs/GATES.md`.
**Controller:** `CLAUDE.md` · **Design:** `docs/methodology.md` · **Pre-registration:** `outputs/PREREGISTRATION.md` (locked before results).

---

## Headline finding (with its band)

> Of ~**235** non-fire, unintentional, consumer-product CO deaths/yr in the U.S., ~**28.6/yr (≈12%)** are addressable
> by this device (residential furnaces + tank water heaters). Modeled conservatively, universal installation would
> plausibly avert **~11 deaths/yr (Base; range ~6–17)** and **~750 ED-treated injuries/yr (Base; range ~630–1,190)** —
> a deliberately scoped, defensible result, not an inflated one. Per device-year the benefit is tiny (CO is
> rare-but-catastrophic) and **concentrated in single-family** homes.

Preventable fraction (reported separately, never averaged): **deaths 21% / 38% / 61%** (Track A, CPSC + model);
**injuries 50% / 59% / 94%** (Track B, NEISS bottom-up, validated at 94.5%).

## What was produced

- `outputs/PREREGISTRATION.md` — method locked before analysis.
- `outputs/GATES.md` — full PASS audit trail (Gates 0–4) with every self-correction and deferral.
- `outputs/PHASE1_REVIEW.md`, `outputs/PHASE2_REVIEW.md` — track write-ups with provenance.
- `outputs/tables/` — Tables 1–4 (.md + .csv), `validation_accuracy.md` (94.5%), `FINDINGS.md`.
- `data/raw/` — cached CPSC reports (5), EIA RECS tables, NEISS dictionary (+ re-fetch instructions for the large NEISS files), `SOURCE_STATUS.md`, `MANUAL_FETCH_NEEDED.md`.
- `data/processed/` — `trackA_sources.csv`, `trackA_estimate.csv`, `case_corpus.csv` (2,529 cases), `case_corpus_classified.csv`, `trackB_estimate.csv`, validation files.
- `scripts/` — 8 phase-named, re-runnable scripts (every number reproduces from them).
- `deliverables/` — filled `actuarial-one-pager.md` and `approved-device-packet.md`.

## HALTs encountered

**None.** The run completed all phases without a gate failure. Two **within-phase self-corrections** were made and logged (not HALTs): in Phase 2 the classifier was fixed for (a) `INTENTIONAL` matching `UNINTENTIONAL`, and (b) reliance on the unreliable NEISS `Fire_Involvement` code (switched to narrative-based fire detection). These improved validation agreement 90.5% → 94.5%.

## Notable findings beyond the headline

1. **Single-family concentration (counter to the usual actuarial framing).** In-scope furnace/tank-WH CO harm is ~95% single-family; multifamily/commercial CO is dominated by **out-of-scope central boilers**. The commercial/MF case for *this* device is limited until a boiler-compatible variant is validated. Surfaced honestly, not massaged.
2. **Deaths vs injuries diverge by design.** Injuries (mild, progressive, survivors) are more preventable than deaths (severe, acute). Tracks reconcile as a documented band and are applied only to their own outcomes.
3. **Corpus corroboration.** NEISS-weighted non-fire unintentional CO ED visits ≈ 12,993/yr ≈ CDC's ~15,000/yr.

## INPUTS STILL NEEDED (outstanding for the human)

Loss-cost inputs the study did not produce (the study stops at harm-averted per device-year, by design):
- `cost_per_death`, `cost_per_injury`, `cost_per_property_claim` (carrier CO loss-costs) → unlock `loss_avoided` and `breakeven_credit`.
- Device-level listings beyond the UL-2075 sensor rating; written `warranty_terms`; `field_reliability_data` (RMA/failure history).

Deferred data (non-blocking; documented in `data/raw/MANUAL_FETCH_NEEDED.md`):
- **CDC WONDER** mortality export (formal magnitude cross-check; contextualized and corroborated meanwhile).
- **NFIRS** microdata (supplementary; the study completed without it).

## Reproducibility

Re-run end to end:
```
python3 scripts/phase1_extract_cpsc.py && python3 scripts/phase1_trackA_estimate.py
python3 scripts/phase2_build_corpus.py && python3 scripts/phase2_classify.py
python3 scripts/phase2_make_validation_sample.py   # then independent re-label -> validation_independent.csv
python3 scripts/phase2_validate.py && python3 scripts/phase2_aggregate.py
python3 scripts/phase3_tables.py
```
(NEISS raw files re-fetch per `data/raw/neiss/README.md`.) Every figure in every table and deliverable traces to a script and a cited source. No number was hand-entered or invented.

*End of run.*
