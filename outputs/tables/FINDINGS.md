# FINDINGS — CO/PRO Preventability Modeling Study

**Date (UTC):** 2026-06-23 · **Status:** Phases 1–3 complete; all gates PASS.
**Tables:** `outputs/tables/table1..table4` (.md + .csv). **Method:** pre-registered (`outputs/PREREGISTRATION.md`).

---

## The headline (plain language)

> Of roughly **235 non-fire, unintentional, consumer-product carbon-monoxide deaths per year** in the U.S.,
> about **29 per year** trace to in-scope residential **furnaces and tank water heaters** — the only sources a
> duct-and-ambient source-shutoff device can touch. Modeled conservatively, such a device, **if installed on
> every in-scope home, would plausibly have prevented about 11 of those deaths per year (Base; range ~6–17),
> and on the order of 750 emergency-department CO injuries per year (Base; range ~630–1,190).**

These are **modeled counterfactual inferences under stated, pre-registered assumptions** — not observed outcomes.

## The numbers, with their band

| Outcome (per year, if universally installed) | Low | **Base** | High |
|---|---|---|---|
| Deaths averted | 6.0 | **10.8** | 17.3 |
| ER injuries averted | 632 | **750** | 1,192 |

- **Addressable harm:** ~28.6 deaths/yr and ~1,273 ED injuries/yr (furnaces + tank water heaters), i.e. ~12% of non-fire consumer-product CO deaths. Everything else — generators (~110 deaths/yr alone), vehicles, grills, ranges, space heaters, boilers — is carved out.
- **Preventable fraction is reported separately for the two outcomes and never averaged:** deaths 21% / **38%** / 61% (Track A, CPSC + model); injuries 50% / **59%** / 94% (Track B, NEISS bottom-up, 94.5%-validated). Injuries are more preventable than deaths because deaths concentrate the severe/acute and standing-pilot exposures a 25 ppm shutoff is least able to interrupt.

## The handoff number (Table 4), and an honest surprise

Expected harm reduction **per device-year, by occupancy** (Base):

| Occupancy | Device-homes | Deaths averted /100k dev-yr | Injuries averted /100k dev-yr |
|---|---|---|---|
| Single-family | 52.6M | 0.020 | 1.36 |
| Multifamily/commercial | 7.7M | 0.0065 | 0.45 |

> **Finding that runs against the usual actuarial framing:** for the **in-scope appliances** (forced-air furnaces +
> tank water heaters), CO harm is **single-family-dominant** (~95% of injury cases with an identifiable dwelling
> type). The multifamily/commercial CO severity story is driven by **central boilers and larger systems, which are
> OUT OF SCOPE** for this device unless boiler/tankless compatibility is separately established. So the per-device
> harm reduction here is **concentrated in single-family**, the opposite of the "build the case in commercial first"
> default. The commercial/multifamily actuarial case for *this* device is limited until a boiler-compatible variant
> is validated (an explicitly labeled out-of-scope sensitivity).

## Honest caveats (carry these into every downstream document)

1. **Counterfactual, not observed.** Every "averted" figure is a "would plausibly have prevented, under stated assumptions" inference, never a field observation. Field-pilot validation is the next step, not done.
2. **Manufacturer-affiliated analysis**, offered with a pre-registered method, transparent code/data, and conservative assumptions as the only real countermeasures to advocacy discounting.
3. **Deaths vs injuries are different populations.** Track A (deaths) and Track B (injuries) diverge by design and are applied only to their own outcomes; do not average or cross-apply them.
4. **Boiler bundling.** The CPSC "Furnaces (incl. Boilers)" line is carved −12% (RECS-grounded) to remove out-of-scope boilers; the true in-scope furnace death count could be modestly lower or higher.
5. **Occupancy split is thin.** ~45% of in-scope injury cases gave no dwelling type; the MF sample is small. The single-family-dominance direction is robust (it follows from where forced-air furnaces physically are), but the exact SF/MF ratio is uncertain.
6. **CDC magnitude cross-check deferred** (WONDER not autonomously pullable); contextualized via CPSC-vs-CDC scope and corroborated by the NEISS-weighted ED total (~13k/yr ≈ CDC ~15k/yr).
7. **No chronic-morbidity credit** in any Base figure; multi-year (5-yr) averaging throughout; unknown-source and indeterminate cases scored against the device; an explicit device non-actuation discount (10% Base) applied.

## What this supports

A modest, defensible evidence base for: above-code/regulatory recognition of source-shutoff as enhanced protection; grant-funded installs; and a single-family-first (not commercial-first) insurance conversation — pending the dollar-loss inputs the actuarial one-pager needs and a field pilot.
