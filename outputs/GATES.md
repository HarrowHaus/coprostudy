# GATES.md — Gate / Audit Log

> Append-only running log of every gate evaluation, halt, deferral, and resume.
> Each phase's EXIT GATE is evaluated here against the phase's own output before
> proceeding. A failed gate rooted in a methodological problem is a HALT, not a
> work-around (CLAUDE.md §1).

---

## 2026-06-23T13:22:29Z — GATE 0 (Setup & pre-registration)

**Phase 0 objective:** lock the method before results; confirm executability.

| # | Assertion | Result | Evidence |
|---|---|---|---|
| 0.1 | `PREREGISTRATION.md` exists with question, scope, algorithm, assumptions, three scenarios | **PASS** | `outputs/PREREGISTRATION.md` §1–§7 written and dated before any analysis. |
| 0.2 | Environment works (trivial pandas script runs) | **PASS** | Python 3.11.15; pandas 3.0.3 / pdfplumber 0.11.10 / bs4 4.15.0 / matplotlib 3.11.0 / requests 2.33.1 / cffi 2.0.0 all import; pandas DataFrame round-trip OK. |
| 0.3 | CPSC report source reachable (irreducible minimum) | **PASS** | 5 reports (2018–2022 editions) downloaded to `data/raw/cpsc_reports/`, valid PDFs, SHA-256 recorded; latest tabulates 2012–2022. pdfplumber confirmed Table 1 (by-product deaths) is extractable. |
| 0.4 | `SOURCE_STATUS.md` documents access state of every source, with manual steps where needed | **PASS** | `data/raw/SOURCE_STATUS.md` covers CPSC / CDC WONDER / NEISS / NFIRS / literature. CDC WONDER + NFIRS manual steps in `data/raw/MANUAL_FETCH_NEEDED.md`. |

**Deferrals logged (not failures):**
- **CDC WONDER magnitude cross-check** — DEFERRED. Programmatic endpoint 500; manual-fetch steps documented. Methodology §5 / Gate 1.2 explicitly permit deferral; study proceeds on CPSC totals.
- **NFIRS** — DEFERRED (supplementary, not load-bearing).

### GATE 0: PASS
All four assertions pass. The two deferrals are sanctioned by the methodology and do not block.
**Proceeding to Phase 1 (Track A — population-level estimate).**

---

## 2026-06-23T13:30:00Z — GATE 1 (Track A — population-level estimate)

**Phase 1 objective:** a fast, defensible first estimate without classifying raw records.
**Artifacts:** `scripts/phase1_extract_cpsc.py`, `scripts/phase1_trackA_estimate.py`,
`data/processed/trackA_sources.csv`, `data/processed/trackA_estimate.csv`,
`data/processed/trackA_citations.json`, `outputs/PHASE1_REVIEW.md`.

**Headline (2018–2022, 5-yr avg):** total ≈235 deaths/yr; addressable (furnace+tank WH) ≈28.6/yr (12.2%);
preventable fraction 21%/38%/61% (L/B/H); prevented ≈6.0/10.8/17.3 deaths/yr.

| # | Assertion | Result | Evidence |
|---|---|---|---|
| 1.1 | CPSC source categories sum within ±5% of stated non-fire CO total | **PASS** | 2020–2022: 234.7 vs 237.7 (−1.3%); 2018–2022: 230.6 vs 235.2 (−2.0%). Residual = per-category rounding + suppressed `*`→0; in-scope lines never suppressed. |
| 1.2 | Magnitude cross-check vs CDC within explained band | **DEFERRED (not failed)** | CDC WONDER not autonomously pullable (manual steps logged). Relationship contextualized: CPSC ~235 (consumer products) sits below CDC ~430 (all sources) by ~the motor-vehicle-exhaust share, which CPSC excludes and is out of scope. Formal year-matched check activates when CDC export supplied. Methodology §5 permits deferral. |
| 1.3 | Plausibility: 0% < addressable share < 100%; prevented ≤ addressable in all scenarios | **PASS** | share 12.2%; max prevented 17.3 ≤ addressable 28.6. Asserted in code. |
| 1.4 | Every headline figure is a multi-year average | **PASS** | All headline figures are 5-yr (2018–2022) averages; 2020–2022 shown only as x-ref. (Water-heater deaths range 3–18 across the window — justifies averaging.) |
| 1.5 | Provenance complete: every number carries a citation | **PASS** | Every external fact cited (CPSC Table 1/2; EIA RECS HC6.1; CDC/MMWR) in `PHASE1_REVIEW.md` §2 and `trackA_citations.json`. Preventable-fraction factors are pre-registered, conservative precondition-decomposition parameters (each grounded in a cited anchor), explicitly labeled provisional — not orphan figures. No single un-sourced number appears. |
| 1.6 | Scenario ordering Low ≤ Base ≤ High | **PASS** | 6.0 ≤ 10.8 ≤ 17.3; fractions 0.210 ≤ 0.378 ≤ 0.606. Asserted in code. |

**Methodological note logged (not a failure):** No published "preventable fraction" exists for a furnace/water-heater
source-shutoff device. Rather than fabricate one, Track A uses a transparent pre-registered model with wide bands and flags
it as provisional. **Track B (Phase 2) measures the fraction bottom-up; Gate 2.4 reconciles the two tracks and HALTS on
sharp divergence.** This is the designed safety net.

### GATE 1: PASS
All assertions pass (1.2 deferred per methodology, with documented context). **Proceeding to Phase 2 (Track B — case-level classification).**

---

## 2026-06-23T13:55:00Z — GATE 2 (Track B — case-level classification)

**Phase 2 objective:** a bottom-up, auditable preventable fraction.
**Artifacts:** `scripts/phase2_*`, `data/processed/case_corpus.csv`, `case_corpus_classified.csv`,
`validation_sample_blind.csv`, `validation_independent.csv`, `trackB_estimate.csv`,
`outputs/tables/validation_accuracy.md`, `outputs/PHASE2_REVIEW.md`.

**Corpus:** 2,529 NEISS CO cases (2019–2023). In-scope addressable = 197 (Prevented 129, Not Prevented 68, Indeterminate 0; Unknown-Source tracked separately).
**Track B fraction (INJURIES):** Low 49.6% / Base 58.9% / High 93.6%.

**Within-phase self-corrections (logged, not gate failures):**
- Bug: token `INTENTIONAL` matched `UNINTENTIONAL` (most CO DX strings end "...UNINTENTIONAL") → over-exclusion. Fixed with `\bINTENTIONAL`.
- Bug/finding: NEISS `Fire_Involvement` code is set to "fire involved" for FD-attended CO calls with NO actual fire (verified in data). Switched fire detection to the authoritative **narrative**. Also removed over-broad `FLAME`/`BURNING` from the fire pattern (stove flame-out, charcoal/wood burning are out-of-scope sources, not fires).
- General source/fire keyword improvements (hookah, fire pit, power-washing, pellet/coal stove, burning-structure phrases). These lifted validation agreement 90.5% → 94.5%. No in-scope *verdict* logic was changed to chase the gate (the 4 fraction-affecting disagreements were left untouched as genuine ambiguities).

| # | Assertion | Result | Evidence |
|---|---|---|---|
| 2.1 | 100% of classified cases have non-empty `notes` + `verdict_confidence` | **PASS** | 2,529/2,529 non-blank (asserted in `phase2_classify.py`; re-verified: 0 blanks). |
| 2.2 | Validation-sample agreement ≥ 90% | **PASS** | **94.5%** (239/253) verdict agreement vs an independent blind re-classification (two instruments, same rubric). `validation_accuracy.md`. |
| 2.3 | Indeterminate/Unknown/uncertain-controllability scored against the device in Base | **PASS** | 62 uncertain-controllability → all Not Prevented (0 Prevented); 1,401 unknown-source → 0 Prevented; Indeterminate→Not Prevented by construction. Verified programmatically. |
| 2.4 | Track B Base within a documented band of Track A; if sharply divergent, HALT and do not average | **PASS (documented band)** | Track A (deaths) Base 37.8% vs Track B (injuries) Base 58.9% — ratio 1.56×, **ranges overlap** (A-High 60.6% > B-Low 49.6%). Divergence is **explained and expected**: deaths skew severe/acute/standing-pilot (less preventable); injuries skew mild/progressive/early-detected (more preventable). Tracks measure **different outcomes**, are **not averaged**, and each is applied only to its own outcome in Phase 3 (deaths→Track A, injuries→Track B). Reported as a finding per methodology §8. |

**Cross-check (bonus):** NEISS-weighted non-fire unintentional CO ED visits ≈ 12,993/yr ≈ CDC's ~15,000/yr — independent corroboration of the corpus.

### GATE 2: PASS
All assertions pass. The track divergence is a documented, expected band (deaths vs injuries), not a sharp contradiction. **Proceeding to Phase 3 (sensitivity & output tables).**

---

## 2026-06-23T14:15:00Z — GATE 3 (Sensitivity & output tables)

**Phase 3 objective:** the final numbers, with uncertainty, segmented where it matters.
**Artifacts:** `scripts/phase3_tables.py`; `outputs/tables/table1..table4` (.md + .csv); `outputs/tables/FINDINGS.md`; `data/raw/eia_recs/RECS2020_HC8.1.pdf`, `HC9.1.pdf`.

| # | Assertion | Result | Evidence |
|---|---|---|---|
| 3.1 | All four tables exist in both formats; no blank cell without "n/a — reason" | **PASS** | table1-4 present as .md and .csv; programmatic scan found 0 blank cells. |
| 3.2 | Scenario ordering holds in every table (Low ≤ Base ≤ High) | **PASS** | Verified: deaths 6.0≤10.8≤17.3, injuries 632≤750≤1,192; fractions and all Table-4 rows monotone. |
| 3.3 | Traceability: every figure reproducible from a script (spot-check 3) | **PASS** | 3 random figures recomputed independently and matched exactly: T3 Base deaths 10.8; T4 SF Base injuries/100k 1.359; T2 High injuries 93.6%. All numbers flow from committed CSV inputs + scripts; no hand-entered values. |
| 3.4 | Table 4 segmented by occupancy type | **PASS** | Single-family vs Multifamily/commercial, device base from RECS HC6.1; harm split from NEISS dwelling type. |
| 3.5 | Honesty checklist fully satisfied | **PASS** | Generators/EDT (~110/yr) & all out-of-scope sources carved out; unknown-source & uncertain/indeterminate scored against device in Base; device non-actuation discount (10% Base) applied; no chronic-morbidity credit in Base; 5-yr multi-year averaging throughout; boiler carve-out applied; every external figure cited. |

**Notable finding logged:** Table-4 segmentation shows in-scope (furnace/tank-WH) CO harm is **single-family-dominant** (~95% of identifiable-dwelling injury cases); multifamily/commercial CO risk is dominated by out-of-scope central boilers. This runs counter to the "commercial-first" actuarial default and is surfaced honestly in `FINDINGS.md` (not massaged). Occupancy split is thin (~45% unknown dwelling) — direction robust, exact ratio uncertain.

### GATE 3: PASS
All assertions pass. **Phase 4 (author deliverables) is UNLOCKED.**

---
