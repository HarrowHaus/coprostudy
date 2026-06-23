# approved-device-packet.template.md

> **TEMPLATE — Phase 4 only. Copy to `deliverables/approved-device-packet.md` and fill every `{{placeholder}}`. `[STUDY]` = from your outputs; `[SPEC]` = from the product spec sheet (`docs/methodology.md` §4 / the 3DA1 sheet); `[EXTERNAL]` = supplied by the human, never invented. Audience: an insurance carrier's device-approval team OR a code/standards body considering above-code recognition. Purpose: get the device onto an approved/recognized list, NOT to claim it replaces a code-required detector.**

---

## INPUTS STILL NEEDED
*(All `[EXTERNAL]` gaps. Delete if empty.)*
- …

---

# CO/PRO® 3DA1 — Approved/Recognized Device Submission

## 1. Summary & the precise ask
{{one_paragraph_summary}}
**Requested action:** {{requested_action — e.g., add to approved smart-home/safety-mitigation device list; recognize as an above-code enhanced-protection measure eligible for premium credit; pilot recognition in [jurisdiction/book].}}
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
- {{additional_listings_or_certifications [EXTERNAL — confirm device-level listings beyond sensor rating]}}
- Warranty: {{warranty_terms [SPEC/EXTERNAL]}}

## 4. The evidence — preventability modeling study
- Method: counterfactual modeling over public CO incident data (CDC, CPSC, NEISS, fire-service), pre-registered, conservative (out-of-scope sources carved out; unknowns scored against the device; device-failure discount applied). [STUDY]
- Addressable harm/yr: **{{addressable_deaths}}** deaths, **{{addressable_injuries}}** serious injuries. [STUDY:Table1]
- Preventable fraction — Base **{{preventable_base}}** (range {{preventable_low}}–{{preventable_high}}). [STUDY:Table2]
- Harm averted per 1,000 device-years, by occupancy: SF {{sf_deaths_per_k}} deaths / MF-commercial {{mf_deaths_per_k}} deaths. [STUDY:Table4]
- Precedent for the method: the federal CPSC generator rulemaking relied on the same class of counterfactual analysis over real fatalities.

## 5. The risk/loss case (carrier audience)
- Expected loss avoided per device-year ({{occupancy_line}}): **{{loss_avoided}}**. [STUDY×EXTERNAL]
- Breakeven credit ceiling: **{{breakeven_credit}}**. [DERIVED]
- Category precedent: carriers already credit *automatic shutoff* above mere detection in the water-leak category; gas-line auto-shutoff valves are already credited by at least one high-value carrier.
- *(Full derivation: `deliverables/actuarial-one-pager.md`.)*

## 6. Regulatory / liability context
- Federal posture trending toward shutoff: CPSC now advises consumers to seek generators *with CO shut-off features*; federal CO-alarm mandates already apply to HUD-assisted housing (2018 IFC). [STUDY/docs]
- State/local: CO-alarm mandates are broad (e.g., Illinois 430 ILCS 135; Chicago ordinance), with landlord-liability exposure — the device reduces exposure below the alarm baseline. [STUDY/docs]
- Positioning: enhanced/above-code protection layered on top of required alarms.

## 7. Installation, maintenance, reliability
- Professional install via HVAC/plumbing channel; daily automatic self-test; up to 10-year sensor life. [SPEC]
- {{field_reliability_data [EXTERNAL — failure rates, RMA data, field history if available]}}

## 8. Limitations (stated plainly)
{{limitations [STUDY:Findings]}} — modeled (not field-observed) prevention under conservative assumptions; manufacturer-affiliated study offered with transparent, pre-registered method; field-pilot validation pending; supplemental to, not a replacement for, code-required alarms.

## 9. Appendices
- A: Full methodology (`docs/methodology.md`)
- B: Study outputs & provenance (`outputs/`)
- C: Product spec sheet (3DA1)
- D: {{additional_appendices}}
