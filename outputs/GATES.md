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
