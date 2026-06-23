# PREREGISTRATION — CO/PRO Preventability Modeling Study

> **This document locks the method before any result exists.** It is written and
> dated *before* Phase 1 analysis. Its purpose is the pre-registration discipline
> required by `docs/methodology.md` §11 and `CLAUDE.md` §7: no one can later claim
> the method was tuned to the answer, because the method was committed first.

**Pre-registered (UTC):** 2026-06-23T13:22:29Z
**Controller:** `CLAUDE.md` · **Design:** `docs/methodology.md` v1.0 · **Coding rules:** `docs/classification-rubric.md`
**Status at registration:** Phase 0 (setup) complete; no analytical results computed yet.

---

## 1. Research question (verbatim from methodology §2)

> Of documented, unintentional, non-fire carbon-monoxide deaths and injuries in the
> United States attributable to residential furnaces and tank water heaters (or their
> venting), what fraction would plausibly have been interrupted by a duct-and-ambient
> source-shutoff device that de-energizes the appliance at a 25 ppm activation
> threshold with a sub-90-second response time?

**Secondary questions:**
- **Addressable harm** — annual deaths/injuries from in-scope sources (furnace + tank water heater), independent of the device.
- **Preventable fraction** — of that addressable harm, the share the device plausibly interrupts, reported Low / Base / High.
- **Expected harm reduction per device-year** — the single handoff number the actuarial one-pager consumes, segmented by occupancy type.

This question is **falsifiable**: it can return a small or unfavorable number, and that is a valid outcome (methodology §1, §9).

---

## 2. What this study is / is not (methodology §1)

- **IS:** a counterfactual modeling / preventability analysis over public incident data. We analyze real recorded cases and model "what if the device had been present."
- **IS NOT:** a meta-analysis (we use raw incident records, not pooled studies); a clinical/field trial (no devices deployed); marketing (a modest honest number beats an inflated one).
- **Precedent legitimizing the method:** CPSC's own counterfactual analysis over ~511 real generator fatalities used to justify the federal portable-generator rule.

---

## 3. Scope — locked before analysis (methodology §3)

**IN SCOPE (addressable by the device):**
- CO from **residential furnaces** (single / dual / variable stage) burning any fossil fuel.
- CO from **tank-type water heaters** (manual pilot or electronic ignition).
- CO entering living space via **supply-duct distribution** or **exhaust/flue spillage near the appliance** (the two loci the device's sensors watch).

**EXPLICITLY OUT OF SCOPE (excluded entirely — carving these out is the central honesty move):**
- Portable generators and engine-driven tools (CPSC's domain; ~110 deaths/yr alone in recent CPSC data).
- Vehicle exhaust; charcoal grills/hibachis indoors; gas ranges/ovens; portable/space/room heaters; wall/floor furnaces where controllability is not a forced-air control circuit; pool heaters; lanterns; camp stoves.
- Tankless water heaters and boiler/hydronic systems **unless** wiring/control compatibility is established — handled only as a separately labeled sensitivity case, never in Base.
- Fire-related CO; **intentional** CO (suicide/homicide); marine / RV / tent / cabin CO.

> **Known data-quality caveat registered up front:** the CPSC by-product table reports a
> line **"Furnaces (incl. Boilers)"** that bundles boilers (out of scope) with furnaces.
> We cannot split them from the published table. We therefore treat that line as a slight
> **over-inclusion** in Track A addressable harm and flag it explicitly; the Track B
> case-level pass applies the boiler carve-out and the device-failure discount that bring
> the Base estimate back down. We never silently inflate.

---

## 4. The device and the preconditions for "prevented" (methodology §4)

**Device facts (3DA1 spec):** activates (cuts appliance power) at **25 ppm**, restores at 15 ppm; dual sensors (supply-duct + ambient-near-exhaust); response **< 90 s**; de-energizes furnace and/or tank water heater via dry relays; sensor range 0–99 ppm; mounts in supply duct ~6 ft from the bend.

**A case is "Prevented" only if all five preconditions plausibly hold:**
1. **Source match** — in-scope furnace or tank water heater.
2. **Controllability** — appliance on a control circuit the device can interrupt (de-energizing actually stops combustion). Gravity/standing-pilot edge cases → uncertain.
3. **Detectable locus** — CO reaches the duct or ambient-near-exhaust sensor.
4. **Progressive accumulation with margin** — CO rose past 25 ppm with enough time, given <90 s response, to interrupt before an incapacitating/lethal dose. Acute instantaneous release → not preventable.
5. **Device functional** — assumed installed and working in the counterfactual; its own failure rate is applied as a separate discount (§6 below).

Any precondition fails → **Not Prevented**. Record too thin to judge a precondition → **Indeterminate** (scored against the device in Base).

---

## 5. The counterfactual decision algorithm (methodology §7 — applied identically to every case)

```
Fire-related?            yes -> EXCLUDE
Intentional?             yes -> EXCLUDE
Source = furnace / tank water heater (or their venting)?
        no (other known) -> OUT OF SCOPE (not addressable)
        unknown          -> UNKNOWN handling (not addressable in Base)
        yes -> counts toward ADDRESSABLE harm, continue:
Controllable by device?  no / uncertain -> NOT PREVENTED
CO reaches duct/ambient sensor?  neither -> NOT PREVENTED ; unknown -> INDETERMINATE
Exposure progressive w/ margin?  acute spike -> NOT PREVENTED ; progressive -> PREVENTED ; unknown -> INDETERMINATE
```
Every case lands in exactly one of: **Prevented · Not Prevented · Out of Scope · Indeterminate.**

**Preventable fraction (Base) = Prevented ÷ (Prevented + Not Prevented + Indeterminate).**
Out-of-Scope and excluded (fire/intentional) cases are in neither numerator nor denominator.

---

## 6. Conservative assumptions / bias controls — locked (methodology §9)

Every one of these errs **against** the device:

1. **Unknown source → not addressable** (excluded from prevented count in Base; reported separately, never apportioned in the device's favor).
2. **Indeterminate → Not Prevented** in Base.
3. **Uncertain controllability → Not Prevented** in Base.
4. **Device-imperfection discount** — an explicit false-negative / failure-to-actuate rate applied even to mechanically-preventable cases (sensor drift, miswire, occupant bypass). Conservative rate, cited basis, locked in §7 below.
5. **No chronic-health credit in Base** — long-term low-level CO morbidity excluded from the headline; any inclusion is a labeled upside scenario only.
6. **Multi-year averaging** — every headline figure is a rolling multi-year mean, never a single anomalous year.
7. **Attribution humility** — where source is inferred rather than documented, down-weight or flag.

---

## 7. The three sensitivity scenarios — locked (methodology §10)

| Lever | **Low** (conservative floor) | **Base** (primary estimate) | **High** (optimistic ceiling) |
|---|---|---|---|
| Indeterminate cases | not prevented | not prevented | a fraction counted as prevented |
| Device failure / non-actuation rate | high (registered: **15%**) | moderate (registered: **10%**) | low (registered: **5%**) |
| Chronic morbidity | excluded | excluded | partial inclusion (labeled) |
| Unknown-source apportionment | excluded | excluded | partial (literature-based, labeled) |

**Pre-registered device-failure discount values:** Low 15% / Base 10% / High 5% non-actuation,
applied multiplicatively to the mechanically-preventable count. Basis to be cited from CO-alarm/
sensor reliability literature in Phase 1; if no defensible citation is found, the discount is **kept**
(removing it would favor the device) and the missing citation is logged as a gap, not a reason to drop it.

**The headline is the Base figure; the Low–High band is the honesty signal.** Reported as
"between X and Y, most likely Z" — never a single bare number.

---

## 8. Two analytical tracks (methodology §8)

- **Track A — population-level apportionment (Phase 1):** CPSC by-source death tabulation × furnace+water-heater share, multi-year averaged, × literature-grounded preventable fraction. Fast, transparent, lower resolution.
- **Track B — case-level classification (Phase 2):** classify individual narrative records via §4–7 of the methodology and `docs/classification-rubric.md`; compute the preventable fraction bottom-up; validate on a hand-labeled sample (≥90% agreement gate).
- Where the tracks agree → high confidence. Where they diverge → **do not average**; report the divergence as a finding and HALT (Gate 2.4).

---

## 9. Data sources and access state at registration

| Source | Role | Access state (probed 2026-06-23) |
|---|---|---|
| CPSC "Non-Fire CO Deaths…Consumer Products" annual reports | **Primary, Phase 1.** By-product death tables. | **Reachable.** 5 reports (2018–2022 editions) downloaded to `data/raw/cpsc_reports/`; the 2022 edition tabulates 2012–2022. |
| CDC WONDER (mortality, ICD-10) | Magnitude cross-check only | HTML reachable; programmatic query endpoint returns 500. **Manual-fetch documented** in `data/raw/MANUAL_FETCH_NEEDED.md`; CDC cross-check **deferred** (not a blocker, per methodology §5 / Gate 1.2). |
| CPSC NEISS (injury narratives) | Phase 2 corpus | Reachable; pull deferred to Phase 2. |
| NFIRS (fire-service incidents) | Supplementary only | Registration typically required; **not load-bearing**; request steps to be documented; study does not block on it. |
| Peer-reviewed CO epidemiology | Preventable-fraction grounding, device-failure basis | Public abstracts/papers; cite every figure used. |

**Provenance rule (locked):** every external number carries a citation (source, year, page/table, URL)
recorded next to it. An orphan number is a gate failure.

---

## 10. Outputs the study will produce (methodology §12)

- **Table 1** — addressable harm (deaths/yr, injuries/yr) by source, multi-year averaged.
- **Table 2** — preventable fraction (Low / Base / High).
- **Table 3** — preventable harm at scale (deaths & injuries averted/yr).
- **Table 4** — expected harm reduction per device-year, **segmented by occupancy** (single-family vs multifamily/commercial).
- `PHASE1_REVIEW.md`, `validation_accuracy.md`, `FINDINGS.md`, `RUN_SUMMARY.md`, and the running `GATES.md` audit log.

---

## 11. Environment (locked, Phase 0)

- **Python** 3.11.15.
- **Libraries:** pandas 3.0.3 · pdfplumber 0.11.10 · beautifulsoup4 4.15.0 · matplotlib 3.11.0 · requests 2.33.1 · cffi 2.0.0.
- All raw downloads cached in `data/raw/` (unmodified, with SHA-256 sums); all transformations scripted into `scripts/` so every number is reproducible. No manual edits to data.

---

## 12. Stopping rules (the Gate Protocol — CLAUDE.md §1)

The run proceeds phase-by-phase only while every exit-gate assertion passes. Any gate failure
rooted in a methodological problem (data won't support the claim, classification accuracy too low,
tracks diverge, numbers don't reconcile) is a **HALT** logged to `outputs/GATES.md` — not a
work-around, and never a method tuned to pass. An unfavorable honest result is logged plainly.

*End of pre-registration. Committed before Phase 1 analysis.*
