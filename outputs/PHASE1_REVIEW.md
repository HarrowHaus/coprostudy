# PHASE 1 REVIEW — Track A (Population-Level Estimate)

**Date (UTC):** 2026-06-23
**Track:** A (population-level apportionment — fast, transparent, lower-resolution first pass; methodology §8)
**Scripts (re-runnable):** `scripts/phase1_extract_cpsc.py` → `scripts/phase1_trackA_estimate.py`
**Data:** `data/processed/trackA_sources.csv`, `data/processed/trackA_estimate.csv`, `data/processed/trackA_citations.json`
**Headline window:** 2018–2022 (the last 5 available report-years). Cross-reference window: 2020–2022 (CPSC's own 3-year headline).

---

## 1. The headline number (Base, 2018–2022 average)

> Of an estimated **235 non-fire, unintentional, consumer-product carbon-monoxide deaths per year** in the U.S., about
> **29 per year (12%)** are attributable to in-scope residential **furnaces and tank water heaters**. Applying a
> conservative, pre-registered preventability model, a duct-and-ambient source-shutoff device — if universally installed
> on those appliances — would **plausibly have interrupted on the order of 11 of those deaths per year (Base), within a
> range of about 6 to 17 (Low–High).**

| Quantity (deaths/yr) | 2018–2022 (headline) | 2020–2022 (x-ref) |
|---|---|---|
| Total non-fire consumer-product CO deaths (CPSC) | **235.2** | 237.7 |
| In-scope furnaces (boiler-carved) | 20.8 | 20.2 |
| Tank water heaters | 7.8 | 5.3 |
| **Addressable harm (furnace + tank WH)** | **28.6  (12.2%)** | 25.6  (10.8%) |
| Preventable fraction — Low / **Base** / High | 21% / **38%** / 61% | 21% / **38%** / 61% |
| **Prevented deaths/yr — Low / Base / High** | **6.0 / 10.8 / 17.3** | 5.4 / 9.7 / 15.5 |

**ER injuries:** intentionally **deferred to Phase 2 (NEISS)**, where incident narratives permit source attribution.
For context only, CDC estimates ~15,000 unintentional non-fire CO ED visits/yr across *all* sources; apportioning that to
furnace/water-heater sources requires the case-level work of Track B and is **not** estimated here (avoiding a weakly-grounded
apportionment in the headline). See §6.

---

## 2. Every input, with provenance (Gate 1.5)

| Input | Value | Source (cited) |
|---|---|---|
| Non-fire consumer-product CO deaths by product, 2012–2022 | full table → `trackA_sources.csv` | **CPSC**, *Non-Fire CO Deaths Associated with the Use of Consumer Products: 2022 Annual Estimates* (pub. May 2026), **Table 1 pp.11–12**, **Table 2 p.13** (Multiple Products). Cached: `data/raw/cpsc_reports/cpsc_co_2022.pdf` (SHA-256 in `SHA256SUMS.txt`). |
| "Furnaces (incl. Boilers)" deaths/yr (2018–2022) | 23.6 (raw) | CPSC Table 1, "Heating Systems → Furnaces (incl. Boilers)". |
| "Water Heaters" deaths/yr (2018–2022) | 7.8 | CPSC Table 1, "Water Heaters". |
| Boiler carve-out (12%) | furnaces 60.39M vs boilers 8.13M homes | **EIA RECS 2020**, Table HC6.1 (cached `data/raw/eia_recs/RECS2020_HC6.1_space_heating.pdf`). Boilers = 8.13/(60.39+8.13)=11.9% of bundled stock. |
| Controllability factor f_control (0.55/0.70/0.85) | pre-registered band | Grounded in RECS HC6.1 (fossil forced-air central furnaces ~60M homes, all electrically interruptible); discounted below 1 because CO-death furnaces skew older (standing-pilot/gravity minority). |
| Detectable-locus + progressive factor f_LP (0.45/0.60/0.75) | pre-registered band | Grounded in CPSC 2022 report narrative (furnace CO via cracked heat exchangers → supply duct, and blocked/backdrafting flues → ambient-near-exhaust, are *progressive*, p.10) and CO clinical epidemiology (gradual overnight buildup is the classic furnace pattern). |
| Device non-actuation discount (15/10/5%) | pre-registered | Conservative assumption; CO/smoke-alarm field-reliability literature as analog. Kept regardless (removing it would favor the device). |
| CDC magnitude context (~430 deaths/yr all-source; ~15,000 ED visits/yr) | context only | **CDC/NVSS & MMWR** (1999–2010 averages; MMWR 56(50) & 63). Not used for source attribution. |

Full citation strings: `data/processed/trackA_citations.json`. **No number in this review is without a source or an explicit, pre-registered derivation.**

---

## 3. How the preventable fraction was built (and what it is *not*)

There is **no single published "preventable fraction" for a furnace/water-heater source-shutoff device.** Inventing one
would violate the honesty protocol. Instead, Track A uses a transparent **precondition decomposition** (methodology §4),
each factor carried as a Low/Base/High band:

```
preventable fraction = f_control x f_locus_progressive x (1 - device_failure)
  Low  = 0.55 x 0.45 x 0.85 = 0.210   (21%)
  Base = 0.70 x 0.60 x 0.90 = 0.378   (38%)
  High = 0.85 x 0.75 x 0.95 = 0.606   (61%)
```

- **This is a model-based plausibility estimate, explicitly provisional.** It is the methodology's intended "fast, lower-resolution" Track-A pass (§8).
- **Track B (Phase 2) measures this fraction bottom-up**, case by case, against `docs/classification-rubric.md`. **Gate 2.4 reconciles the two tracks**; if they diverge sharply, the run HALTS and reports the divergence rather than averaging.
- **Ceiling sanity:** the CPSC portable-generator rulemaking found a *source-shutoff* would avert nearly all of ~511 real generator deaths — evidence that source-shutoff can be highly effective when the source is controllable and CO accumulates before a lethal dose. Our High (61%) sits well below "nearly all," because furnace/WH cases include uncontrollable (gravity), isolated-locus, and acute sub-populations that we score against the device.

---

## 4. Sanity checks performed

- **Reconciliation (Gate 1.1):** sum of top-level CPSC categories vs the printed Total — **2020–2022: 234.7 vs 237.7 (−1.3%)**, **2018–2022: 230.6 vs 235.2 (−2.0%)**. Both within ±5%. Residual = independent per-category rounding + suppressed (`*`→0) small cells; the in-scope furnace/water-heater lines are never suppressed.
- **Extraction fidelity:** computed 2020–2022 averages match CPSC's printed "Average Estimate" column (Furnaces 23, Water Heaters 5, Heating Systems 68, EDT 110, Total 238).
- **Plausibility (Gate 1.3):** addressable share = 12.2% ∈ (0%,100%); prevented ≤ addressable in every scenario (max 17.3 ≤ 28.6).
- **Multi-year (Gate 1.4):** every headline figure is a 5-year (2018–2022) average; no single year is headlined. (Note the value of this: water-heater deaths swing from 3 to 18 across the window — a single year would mislead.)
- **Scenario ordering (Gate 1.6):** 6.0 ≤ 10.8 ≤ 17.3 and 21% ≤ 38% ≤ 61%.

---

## 5. Magnitude cross-check (Gate 1.2 — CDC deferred, but contextualized)

CDC WONDER could not be pulled autonomously (manual steps in `data/raw/MANUAL_FETCH_NEEDED.md`), so the formal CDC band
check is **deferred** (sanctioned by methodology §5 / SETUP.md). It is **not** a blocker, and the relationship is already
explainable from published CDC summaries:

- CDC/NVSS: **~430** unintentional **non-fire CO deaths/yr** (all sources).
- CPSC: **~235** non-fire **consumer-product** CO deaths/yr.
- The gap (~195/yr) is dominated by **motor-vehicle exhaust** (e.g., car running in an attached garage), which CDC counts
  but CPSC's "consumer products" scope **excludes** — and which is **out of scope** for this device anyway. The CPSC total
  sitting *below* the CDC all-source total, by roughly the motor-vehicle share, is the expected, documented relationship.
  When the CDC export is supplied, the script will activate the formal year-matched band check.

---

## 6. What this estimate DOES and DOES NOT claim

**Does claim:** Using the best public by-source death data (CPSC), the slice of U.S. non-fire CO mortality the device could
even theoretically touch is **small and explicitly bounded (~12%, ~29 deaths/yr)**; and under a conservative, pre-registered
model, universal installation would plausibly interrupt **~11 deaths/yr (Base, range 6–17).**

**Does NOT claim:**
- Not a measured/observed effect — every "prevented" count is a **counterfactual inference under stated assumptions**, not a field observation.
- Not the final preventable fraction — Track B (Phase 2) produces the auditable, case-level number; this Track-A figure is **provisional** and will be reconciled (Gate 2.4).
- Not an injuries estimate — ER injuries are **deferred to Phase 2 (NEISS)**.
- Not a per-device number — that is Table 4 (Phase 3), segmented by occupancy.
- Says nothing about chronic low-level CO morbidity (excluded from Base by design).

---

## 7. Honesty moves already baked in (methodology §9)

Generators/EDT (110/yr), vehicles, ranges, grills, portable/space heaters, pool heaters, lanterns, camp stoves — **all
carved out**. Boilers carved out of the furnace line (−12%). Wall/floor furnaces (gravity/standing-pilot) **excluded** from
Base addressable. Device-failure discount applied. No chronic-morbidity credit. Multi-year averaging throughout. Every
external number cited. The number was **shrunk on purpose** at every step — which is the point.

*Track A complete. Proceed to Gate 1.*
