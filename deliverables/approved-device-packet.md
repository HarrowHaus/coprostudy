# CO/PRO® 3DA1 — Approved/Recognized Device Submission

## INPUTS STILL NEEDED
*(All `[EXTERNAL]` gaps the human supplies; none invented.)*
- **`additional_listings_or_certifications`** — device-level listings beyond the UL-2075 sensor rating (confirm). [EXTERNAL]
- **`warranty_terms`** — written warranty period/terms. [EXTERNAL]
- **`field_reliability_data`** — failure/non-actuation rates, RMA data, field history if available. [EXTERNAL]
- **`loss_avoided` / `breakeven_credit`** — depend on external loss-costs (see `deliverables/actuarial-one-pager.md` → INPUTS STILL NEEDED). [EXTERNAL]

---

## 1. Summary & the precise ask
The CO/PRO® 3DA1 is a duct-and-ambient carbon-monoxide **source-shutoff** that de-energizes a home's furnace and tank water heater at 25 ppm — stopping CO production at the source rather than only warning after it spreads. A pre-registered counterfactual modeling study over public U.S. incident data (CPSC death reports + CPSC NEISS injury narratives) estimates that, if universally installed on in-scope appliances, the device would plausibly avert **~11 CO deaths/yr (range ~6–17)** and **~750 ED-treated CO injuries/yr (range ~630–1,190)** — a modest, deliberately conservative, scoped figure (in-scope sources are ~12% of non-fire consumer-product CO deaths).

**Requested action:** add the device to the carrier's approved/recognized **enhanced (above-code) CO-mitigation** device list, eligible for a premium credit, with an initial **single-family** pilot (where the modeled benefit concentrates).
**Explicitly NOT requested:** treatment as a substitute for code-required CO alarms. The device is supplemental.

## 2. What the device is
- Function: source-shutoff that de-energizes furnace and tank water heater at **25 ppm** (restores at 15 ppm) — stops CO at the source vs. warning after spread. [SPEC]
- Sensing: dual sensors (supply-duct + ambient-near-exhaust); response **< 90 s**. [SPEC]
- Compatibility: fossil-fuel furnaces (single/dual/variable stage) and tank water heaters; 24 VAC. [SPEC]
- Install: professional, ~15–20 min, supply duct ~6 ft from bend. [SPEC]

## 3. Standards & listings
- Sensors: **UL-2075** rated. [SPEC]
- Enclosure: polycarbonate UL94 V0. [SPEC]
- Relevant standards landscape: CO alarms governed by UL 2034 / NFPA 72; this device is a supplemental source-shutoff, not a UL 2034 alarm. [STUDY/docs]
- Additional device-level listings/certifications: **{{additional_listings_or_certifications [EXTERNAL]}}** — see INPUTS STILL NEEDED.
- Warranty: **{{warranty_terms [EXTERNAL]}}** (spec indicates up to 10-year sensor life). [SPEC/EXTERNAL]

## 4. The evidence — preventability modeling study
- Method: counterfactual modeling over public CO incident data (CPSC death reports, CPSC NEISS), pre-registered, conservative (out-of-scope sources carved out — generators ~110 deaths/yr alone; unknowns and indeterminates scored against the device; explicit device non-actuation discount). [STUDY]
- Addressable harm/yr: **~28.6** deaths, **~1,273** serious (ED-treated) injuries. [STUDY:Table1]
- Preventable fraction (reported separately by outcome, never averaged): **deaths Base 38%** (range 21%–61%); **injuries Base 59%** (range 50%–94%, validated at 94.5% inter-rater agreement). [STUDY:Table2]
- Harm averted per **100,000 device-years** (Base), by occupancy: **single-family 0.020 deaths / 1.36 injuries**; **multifamily-commercial 0.0065 deaths / 0.45 injuries**. [STUDY:Table4]
- Precedent for the method: the federal CPSC generator rulemaking relied on the same class of counterfactual analysis over real fatalities.

## 5. The risk/loss case (carrier audience)
- Expected loss avoided per device-year: **{{loss_avoided [EXTERNAL loss-costs pending]}}** — multiplicands (harm averted/device-yr) are in §4; dollar conversion needs the carrier's CO loss-costs. [STUDY×EXTERNAL]
- Breakeven credit ceiling: **{{breakeven_credit [DERIVED once loss-costs supplied]}}**. [DERIVED]
- Category precedent: carriers already credit *automatic shutoff* above mere detection in the water-leak category; gas-line auto-shutoff valves are already credited by at least one high-value carrier.
- *(Full derivation: `deliverables/actuarial-one-pager.md`.)*

## 6. Regulatory / liability context
- Federal posture trending toward shutoff: CPSC now advises consumers to seek generators *with CO shut-off features*; federal CO-alarm mandates already apply to HUD-assisted housing. [STUDY/docs]
- State/local: CO-alarm mandates are broad, with landlord-liability exposure — the device reduces exposure below the alarm baseline. [STUDY/docs]
- Positioning: enhanced/above-code protection layered on top of required alarms.

## 7. Installation, maintenance, reliability
- Professional install via HVAC/plumbing channel; daily automatic self-test; up to 10-year sensor life. [SPEC]
- Field reliability data: **{{field_reliability_data [EXTERNAL]}}** — see INPUTS STILL NEEDED.

## 8. Limitations (stated plainly)
Modeled (not field-observed) prevention under conservative, pre-registered assumptions; addressable harm is a scoped ~12% of non-fire CO deaths; deaths and injuries are different populations and are never averaged; the in-scope benefit is **single-family-concentrated** (multifamily/commercial CO is dominated by out-of-scope central boilers — a boiler-compatible variant would be a separate submission); manufacturer-affiliated study offered with transparent, pre-registered method and open code/data; CDC magnitude cross-check deferred but corroborated by the NEISS-weighted ED total; field-pilot validation pending; supplemental to, not a replacement for, code-required alarms. (Full: `outputs/tables/FINDINGS.md`.)

## 9. Appendices
- A: Full methodology (`docs/methodology.md`)
- B: Study outputs & provenance (`outputs/` — PREREGISTRATION, GATES audit log, PHASE1/PHASE2 reviews, Tables 1–4, validation accuracy, FINDINGS)
- C: Product spec sheet (3DA1)
- D: Reproducible analysis scripts (`scripts/`) and cached source data (`data/`).
