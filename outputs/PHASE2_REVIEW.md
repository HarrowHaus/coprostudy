# PHASE 2 REVIEW — Track B (Case-Level Classification)

**Date (UTC):** 2026-06-23
**Track:** B (bottom-up, auditable case by case; methodology §8)
**Scripts:** `phase2_build_corpus.py` → `phase2_classify.py` → `phase2_make_validation_sample.py` → (independent agent) → `phase2_validate.py` → `phase2_aggregate.py`
**Data:** `data/processed/case_corpus.csv`, `case_corpus_classified.csv`, `validation_sample_blind.csv`, `validation_independent.csv`, `trackB_estimate.csv`; `outputs/tables/validation_accuracy.md`

---

## 1. Corpus

**2,529 CO-related cases** from CPSC **NEISS** ED surveillance, 2019–2023 (5 yrs), filtered from ~1.67M annual records by an unambiguous CO-narrative match (deliberately excluding "C/O" = "complains of"). One row per incident with the verbatim narrative + NEISS context (diagnosis, disposition, location, fire-involvement, product codes, statistical weight).

> **Track B measures INJURIES, not deaths.** NEISS is ED-treated injury/exposure surveillance. This is by design (methodology §8 makes Track B narrative-driven) and is the key to reading the result correctly (see §4).

## 2. Classification

Every case coded against `docs/classification-rubric.md` by a **transparent rule-based classifier** — each field decision traces to the keyword/logic that fired, recorded in a mandatory per-case `notes` rationale + `verdict_confidence` (methodology §11's "follow the rubric verbatim and output rationale," made fully reproducible).

| Verdict | Count |
|---|---|
| Unknown-Source (tracked separately, not addressable in Base) | 826* |
| Out of Scope (generator/vehicle/grill/range/boiler/other) | 775 |
| Excluded (fire / intentional) | 687 |
| **Prevented** (in-scope, controllable, detectable, progressive) | **129** |
| **Not Prevented** (uncertain controllability, gravity, acute) | **68** |
| Indeterminate | 0 |

*Unknown-Source 826 here counts only non-fire/unintentional unknown cases; 1,401 cases have `source_primary=unknown` overall (some excluded as fire/intentional).

**In-scope addressable = 197** (Prevented 129 + Not Prevented 68). Not Prevented is dominated by **62 tank-water-heater cases with uncertain (likely standing-pilot) controllability**, routed against the device per rubric.

Two classifier bugs were found via validation and **self-corrected within the phase** (logged): (a) the token `INTENTIONAL` was matching `UNINTENTIONAL` (over-excluding); (b) the NEISS `Fire_Involvement` code is unreliable — it is set to "fire involved" for fire-department-attended CO calls with **no actual fire** (e.g., "CO detector went off, fire dept found CO 123 ppm") — so fire is now judged from the **narrative**, which is authoritative.

## 3. Validation (Gate 2.2)

A **253-case** random sample (10% of corpus, seed-reproducible) was re-classified by an **independent agent**, blind to the rule output (two different instruments applying the same rubric). **Verdict agreement: 94.5% (239/253).** Of 14 disagreements, only **4 touch the in-scope preventable fraction**, and those net **3 under-counts vs 1 over-count** for the rule classifier — i.e., it is marginally *more conservative* than the independent reading (errs against the device). Full confusion matrix and case list: `outputs/tables/validation_accuracy.md`.

## 4. Track B preventable fraction (INJURIES) and reconciliation (Gate 2.4)

Realized fractions (mechanical preventability × device non-actuation discount), three scenarios (methodology §10):

| | Low | **Base** | High |
|---|---|---|---|
| **Track B (injuries)** | 49.6% | **58.9%** | 93.6% |
| Track A (deaths) | 21.0% | 37.8% | 60.6% |

**The tracks reconcile as a documented band, and are NOT averaged.** They measure **different outcomes**: Track A = deaths, Track B = injuries. Injuries are *more* preventable than deaths because deaths concentrate the severe/acute/standing-pilot exposures that a 25 ppm source-shutoff is least able to interrupt, while ED-treated injuries are dominated by milder, progressive, early-detected leaks. The ~1.56× Base difference is in the **expected direction** and the Low–High ranges **overlap** (Track A High 60.6% > Track B Low 49.6%). Per methodology §8 the divergence is itself a finding, reported honestly.

**Consequence for Phase 3 (conservative):** deaths-averted uses the lower **Track A (deaths)** fraction; injuries-averted uses **Track B (injuries)**. Each fraction is applied only to its own outcome — never cross-applied, never averaged.

## 5. National injury magnitude (NEISS statistical weights)

Weighting the corpus to national estimates:
- Non-fire unintentional CO ED visits/yr ≈ **12,993** — consistent with the independent CDC figure (~15,000), validating the corpus.
- **In-scope (furnace + tank water heater) addressable injuries/yr ≈ 1,273** (furnaces ~955, water heaters ~332). NEISS narratives route boilers to a separate out-of-scope category, so no boiler carve-out is needed for injuries.

*Track B complete. Proceed to Gate 2.*
