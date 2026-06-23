# CO/PRO Preventability Modeling Study — Methodology Specification
### A counterfactual, secondary-data analysis to estimate how much furnace/water-heater CO harm a source-shutoff device could prevent

**Version:** 1.0 (draft for execution)
**Purpose of this document:** A complete, handoff-ready methodology. Whoever runs the analysis — you, an AI agent, or an academic partner — should be able to execute from this spec without further instruction. It is written to be *defensible under hostile review* (a skeptical insurance underwriter or regulator), which is the whole point: a number that survives scrutiny is worth more than a big number that doesn't.

> **What this study is, in one sentence:** Take the existing public record of real carbon-monoxide deaths and injuries, identify the share caused by furnaces and tank water heaters, and estimate — case by case, conservatively — what fraction a device that shuts those appliances off at 25 ppm would plausibly have interrupted before harm occurred.

> **A plain-language glossary of every technical term is at the end (Section 14). If a word is unfamiliar, it's defined there.**

---

## 1. What this is — and what it is NOT

| | |
|---|---|
| **It IS** | A *counterfactual modeling study* (a.k.a. secondary-data / preventability analysis) over public incident data. You analyze real, already-recorded cases and model "what would have happened if the device had been present." |
| **It is NOT a meta-analysis** | A meta-analysis statistically *pools multiple existing studies* measuring the same outcome. We are not pooling studies — we are analyzing raw incident records. Calling it a meta-analysis to a serious audience would be a tell that the method is misunderstood. Use **"counterfactual modeling study"** or **"preventability analysis."** |
| **It is NOT a clinical trial / field trial** | We deploy no devices and wait for no outcomes. A real-world trial measuring *deaths* is effectively impossible here (Section 12), which is exactly why a modeling study is the right first instrument. |
| **It is NOT marketing** | The output may be modest. A conservative, honest result that an underwriter believes beats an inflated one they discount on sight. Designed to find the truth, not to flatter the product. |

**Precedent that legitimizes this method:** The U.S. Consumer Product Safety Commission did exactly this to justify the federal portable-generator rule — it ran ~140,000 simulations against 511 real generator fatalities and estimated that compliant auto-shutoff generators would have averted nearly all of them. That is a counterfactual modeling study over public incident data, used to support federal regulation. This study is the furnace/water-heater analog of that work.

---

## 2. Research question (precise and falsifiable)

> **Of documented, unintentional, non-fire carbon-monoxide deaths and injuries in the United States attributable to residential furnaces and tank water heaters (or their venting), what fraction would plausibly have been interrupted by a duct-and-ambient source-shutoff device that de-energizes the appliance at a 25 ppm activation threshold with a sub-90-second response time?**

Secondary questions:
- What is the **addressable harm** — the annual count of deaths/injuries from the in-scope sources (independent of the device)?
- What is the **preventable fraction** of that addressable harm (with a low/base/high range, not a single number)?
- What is the **expected harm reduction per installed device-year** — the single output the actuarial one-pager needs?

---

## 3. Scope and boundaries (state these loudly — honest carve-outs build trust)

**IN SCOPE (addressable by the device):**
- Carbon monoxide originating from **residential furnaces** (single, dual, variable stage) burning any fossil fuel.
- Carbon monoxide originating from **tank-type water heaters** (manual pilot or electronic ignition).
- CO entering living space via **supply-duct distribution** or **exhaust/flue spillage near the appliance** — the two things the device's duct and ambient sensors actually watch.

**EXPLICITLY OUT OF SCOPE (the device cannot prevent these — exclude them entirely):**
- Portable generators and engine-driven tools (this is the CPSC's domain; ~100 deaths/yr on its own — *removing it is the single most important honesty move in the study*).
- Vehicle exhaust (attached-garage warm-up, etc.).
- Charcoal grills / hibachis used indoors.
- Gas ranges/ovens used for cooking or as space heat.
- Tankless water heaters and boiler/hydronic systems **unless** wiring/control compatibility is established (note as a separate sensitivity case).
- Fire-related CO (structure fires).
- **Intentional** CO exposure (suicide/homicide).
- Marine, RV, and tent/cabin CO.

> Carving these out *reduces* your headline number on purpose. Do it anyway. The credibility you buy is worth more than the deaths you'd be overclaiming.

---

## 4. Device mechanism → the preconditions for prevention (the analytical core)

For the device to have prevented a given real case, a specific chain of conditions must hold. This chain is the spine of the whole study — every case is judged against it.

**Device facts (from the 3DA1 spec sheet):**
- Activates (cuts appliance power) at **25 ppm**; restores at **15 ppm**.
- **Dual sensors:** supply-duct air + ambient air near exhaust.
- **Response time < 90 seconds** (10%→90% of range).
- Acts via dry relays that **de-energize the furnace and/or water heater** it is wired to.
- Sensor/display range 0–99 ppm; mounts in supply duct ~6 ft from the bend.

**Preconditions for a "prevented" verdict (all must be plausibly true):**
1. **Source match** — the CO source was an in-scope furnace or tank water heater (Section 3).
2. **Controllability** — the appliance was on a control circuit the device can interrupt (i.e., de-energizing it actually stops combustion). Most modern gas furnaces/water heaters: yes. Gravity/standing-pilot edge cases: flag as uncertain.
3. **Detectable locus** — the CO would have reached the duct or ambient-near-exhaust sensor (not a release geometrically isolated from both sensor positions).
4. **Progressive accumulation with margin** — CO rose past 25 ppm with enough time, given the sub-90-second response, to interrupt the source *before* occupants received an incapacitating/lethal dose. The classic preventable pattern (cracked heat exchanger venting into supply air; blocked/backdrafting flue spilling near the unit) is progressive. An instantaneous massive release that incapacitates before any threshold-and-response window is **not** preventable and must be scored as such.
5. **Device functional** — assumed installed and working in the counterfactual (its own failure rate is handled as a separate discount, Section 9).

If any precondition fails → the case is **Not Prevented**. If preconditions hold → **Prevented**. If the record is too thin to judge a precondition → **Indeterminate** (handled conservatively, Section 9).

---

## 5. Data sources (concrete, public, with what each gives and where it's weak)

| Source | What it provides | Limitation to manage |
|---|---|---|
| **CPSC "Non-Fire Carbon Monoxide Deaths Associated with the Use of Consumer Products"** (annual report series) | **The Phase-1 goldmine.** Already tabulates non-fire CO deaths *by source/appliance category* (heating systems, water heaters, engine-driven tools, ranges, etc.). Lets you size addressable harm without classifying raw records. | Categories are broad; "heating systems" may bundle furnaces with other heaters. Multi-year averaging needed (annual counts are volatile). |
| **CDC WONDER** (mortality, ICD-10) | National death counts for CO poisoning (codes around T58 / X47 and related), by year/demographics/geography. | ICD codes almost never name the *appliance*. Use for totals and denominators, not source attribution. |
| **CPSC NEISS** (National Electronic Injury Surveillance System) | ER-treated **injury** estimates with **free-text incident narratives** — narratives often hint at source. | Sample-based (weighted estimates); narratives short and uneven. |
| **CPSC in-depth investigation files / IPII / death-certificate files** | The richest **case-level** source detail — many reports explicitly identify the appliance and failure mode. | Not every death is investigated; access/format varies; messy free text. |
| **NFIRS** (National Fire Incident Reporting System, USFA) | Large volume of fire-service **CO incident** responses, including non-fire CO calls, with some incident detail. | Source coding inconsistent across departments; many "good intent / no hazard" calls to filter. |
| **Peer-reviewed CO epidemiology** | Published **source-attribution fractions**, exposure-response relationships, response-time/dose modeling to ground assumptions. | Varies in setting and vintage; cite, don't over-extrapolate. |
| **State medical-examiner / vital-records datasets** (where public) | Deeper narrative case detail for a subset of states; useful for a validation sub-sample. | Coverage uneven; some require request. |

---

## 6. Case classification taxonomy (the variables coded for every case-level record)

For each incident analyzed at the case level, record:

- `case_id`
- `year`
- `intent` — unintentional / intentional / undetermined *(keep only unintentional)*
- `fire_related` — yes / no *(keep only no)*
- `source_primary` — furnace / tank_water_heater / both / generator / vehicle / range_oven / grill / boiler_tankless / other / **unknown**
- `failure_mode` — cracked_heat_exchanger / blocked_or_backdrafting_flue / depressurization / improper_install / maintenance_failure / other / unknown
- `controllable` — yes / no / uncertain *(precondition 2)*
- `detectable_locus` — duct / ambient_near_exhaust / both / neither / unknown *(precondition 3)*
- `exposure_profile` — progressive / acute_spike / chronic_low_level / unknown *(precondition 4)*
- `preventability_verdict` — **Prevented / Not Prevented / Out of Scope / Indeterminate**
- `verdict_confidence` — high / medium / low
- `notes` — free text rationale (required; this is your audit trail)

---

## 7. The counterfactual decision algorithm (apply identically to every case)

```
START
 │
 ├─ Fire-related?            ── yes ─▶ EXCLUDE (out of frame)
 ├─ Intentional?            ── yes ─▶ EXCLUDE (out of frame)
 │
 ├─ Source = furnace or tank water heater (or their venting)?
 │        ├─ no (other known source) ─▶ OUT OF SCOPE (addressable harm = no)
 │        └─ unknown ─────────────────▶ route to UNKNOWN handling (Sec. 9)
 │   (yes ↓ — this case counts toward ADDRESSABLE harm)
 │
 ├─ Appliance controllable by the device? ── no ─▶ NOT PREVENTED
 │   (uncertain ─▶ treat as NOT PREVENTED in base case)
 │
 ├─ CO would reach duct or ambient sensor? ── neither ─▶ NOT PREVENTED
 │   (unknown ─▶ INDETERMINATE)
 │
 ├─ Exposure progressive with margin before lethal/incapacitating dose?
 │        ├─ acute spike, no margin ─▶ NOT PREVENTED
 │        ├─ progressive, margin ───▶ PREVENTED
 │        └─ unknown ──────────────▶ INDETERMINATE
 │
END
```

Every case lands in exactly one bucket: **Prevented**, **Not Prevented**, **Out of Scope**, or **Indeterminate**.

---

## 8. Two analytical tracks (run both; report separately)

The biggest real-world problem is that **many CO death records don't record the source.** Don't paper over it — run two complementary tracks and present both.

**Track A — Population-level apportionment (fast, Phase 1).**
Use the CPSC source-category tabulations to estimate *addressable harm* directly: (total non-fire unintentional CO deaths/injuries) × (published furnace + water-heater share). Then apply a *literature-grounded* preventable fraction. This gives a defensible first estimate in days, without touching raw records. Lower resolution, but transparent and quick.

**Track B — Case-level classification (deep, Phase 2).**
Pull individual narrative records (NEISS, CPSC investigations, NFIRS, ME files), classify each via Section 6–7, and compute the preventable fraction *bottom-up*. Higher resolution, auditable case by case, far more credible — but labor-intensive (this is where AI does the heavy lifting, Section 11).

Where Track A and Track B agree, confidence is high. Where they diverge, that divergence is itself a finding to report honestly.

---

## 9. Conservative assumptions and bias controls (always err AGAINST the device)

State every one of these in the published methodology. They are what convert "manufacturer's study" into "study an underwriter will read."

- **Unknown source → not addressable.** Cases with unidentifiable source are excluded from the prevented count (not split in the device's favor) in the base case.
- **Indeterminate → not prevented** in the base case.
- **Uncertain controllability → not prevented.**
- **Device imperfection discount.** Apply an explicit false-negative / failure-to-actuate rate (e.g., sensor drift, miswire, occupant bypass). Even a functioning device doesn't prevent 100% of mechanically-preventable cases. Pick a conservative rate and cite the basis.
- **No chronic-health credit in the base case.** Long-term low-level CO morbidity is real but hard to substantiate per-case; exclude it from the headline and treat any inclusion as an explicitly-labeled upside scenario.
- **Multi-year averaging.** Use a rolling multi-year mean for all annual figures; never headline a single anomalous year.
- **Attribution humility.** Where source is inferred rather than documented, down-weight or flag.

---

## 10. Sensitivity analysis (report a RANGE, never a single number)

Run three scenarios and publish all three:

| Scenario | Indeterminate cases | Device failure rate | Chronic morbidity | Unknown-source |
|---|---|---|---|---|
| **Low (conservative floor)** | counted as not prevented | high | excluded | excluded |
| **Base (primary estimate)** | counted as not prevented | moderate | excluded | excluded |
| **High (optimistic ceiling)** | fraction counted as prevented | low | partial inclusion | partial apportionment |

The headline is the **Base** figure; the **Low–High** band is the honesty signal. A defensible study says "between X and Y, most likely Z," not "Z."

---

## 11. Execution playbook (how to actually run it, including the AI-agent path)

**Phase 1 — Population estimate (Track A).** *Days, not weeks.*
1. Pull the most recent ~5 years of CPSC Non-Fire CO Death reports; extract the by-source tables.
2. Pull CDC WONDER totals for the same years as a cross-check on magnitude.
3. Compute addressable harm = total × (furnace + water-heater share), multi-year averaged.
4. Apply a literature-grounded preventable fraction → first Base/Low/High estimate.
5. Output: the Section 12 summary table, Phase-1 version. *This alone is enough to open insurance and PR conversations.*

**Phase 2 — Case-level classification (Track B).** *The AI-leverage phase.*
6. Assemble case corpus: NEISS narratives, CPSC investigation reports, NFIRS non-fire CO incidents, any obtainable ME datasets.
7. **AI-assisted classification:** an LLM agent reads each free-text narrative and codes the Section-6 variables, applying the Section-7 algorithm. This is a legitimate, scalable use of AI — narrative incident classification is exactly the kind of messy, high-volume text work models do well. *Guardrails:* (a) a written classification rubric the model follows verbatim; (b) the model must output its rationale per case (the `notes` field) for auditability; (c) a human (or a second model) hand-checks a random validation sub-sample to measure classification accuracy; (d) low-confidence cases route to human review.
8. Aggregate verdicts → bottom-up preventable fraction with confidence bands.

**Phase 3 — Sensitivity + external review.**
9. Run the three scenarios (Section 10).
10. Hand the methodology + a data sub-sample to a third party (academic, independent engineer, or actuary) for critique *before* publishing. Pre-register the methodology (write it down and date it publicly) so no one can claim the method was tuned to the answer.

---

## 12. Output schema — the deliverables (and the one number the actuary needs)

**Table 1 — Addressable harm (per year, multi-year averaged)**
| Source | Deaths/yr | ER injuries/yr | Basis |
|---|---|---|---|
| Furnaces | *TBD* | *TBD* | CPSC / case-level |
| Tank water heaters | *TBD* | *TBD* | CPSC / case-level |
| **Total addressable** | *TBD* | *TBD* | |

**Table 2 — Preventable fraction**
| Scenario | Preventable fraction | Source |
|---|---|---|
| Low | *TBD %* | Track A & B |
| **Base** | *TBD %* | |
| High | *TBD %* | |

**Table 3 — Preventable harm at scale (if universally installed)**
| Scenario | Deaths averted/yr | Injuries averted/yr |
|---|---|---|
| Low / Base / High | *TBD* | *TBD* |

**Table 4 — THE HANDOFF NUMBER → expected harm reduction per device-year**
> Preventable harm ÷ relevant installed-base denominator = **expected deaths and injuries averted per installed device per year** (often expressed per 1,000 or per 100,000 device-years, since the per-unit number is tiny — CO is rare-but-catastrophic).

*(All values above are placeholders. The study produces them; this spec does not presuppose them.)*

---

## 13. The bridge to the actuarial one-pager (explicit handoff)

This study stops at **expected harm averted per device-year** (Table 4). The actuarial one-pager picks up from there and does the dollar conversion:

```
[Table 4 output: harm averted per device-year]
        ×  [cost per loss: wrongful-death settlement, bodily-injury, medical, associated property/fire claim]
        =  EXPECTED LOSS AVOIDED per device-year
        →  compare to the cost of a premium discount
        →  recommended discount / approved-device case
```

**What this means for sequencing:** because CO is low-frequency / high-severity, the per-unit loss-avoided is small in ordinary homeowner lines and **large in commercial, landlord, and multifamily lines** (one wrongful-death tail event dominates the math). So Table 4 should be produced **segmented by occupancy type** — single-family vs multifamily/commercial — because the actuarial case is built first where the severity is concentrated.

**Reuse beyond insurance:** the same Table 1–3 outputs are the evidence base for above-code/regulatory recognition, the justification for grant-funded installs, and — same numbers, different voice — the spine of the public editorial/data asset. One analytical engine, four destinations.

---

## 14. Limitations and threats to validity (publish these; don't bury them)

- **"Would have prevented" is an inference, not an observation.** Every verdict is a counterfactual judgment about a case that already happened. Honest framing: *plausible* prevention under stated assumptions.
- **Source mis/under-coding.** CO records frequently omit or blur the appliance source; intentional/accidental and fire/non-fire are sometimes conflated. This is the central data-quality risk.
- **Timing and dose inference.** Whether the device's threshold-and-response window beat the exposure is often judged from incomplete timelines.
- **Device failure modes** (drift, miswire, occupant bypass, gravity-system incompatibility) cap real-world efficacy below the model.
- **Advocacy discount.** A manufacturer-funded study is weighed as advocacy evidence. Third-party validation, pre-registration, transparent data/code, and conservative assumptions are the only real countermeasures.
- **No field confirmation yet.** A modeling study justifies and *precedes* a real-world pilot; it does not permanently replace it. The eventual pilot measures "saves" (source-CO detected and appliance shut off in a situation a hallway detector would have missed) — a common-enough event to count, unlike deaths.

---

## 15. Glossary (plain language)

- **Counterfactual** — a "what if it had been different" estimate. Here: what if the device had been installed in cases that really happened?
- **Secondary-data analysis** — analyzing data someone else already collected (public death/injury records), rather than running a new experiment.
- **Meta-analysis** — statistically combining several *existing studies* of the same thing. *Not what this is* (we use raw incident data, not studies).
- **Clinical/field trial** — deploying the real thing and waiting to measure outcomes. Impractical for rare-death prevention; hence the modeling approach.
- **Addressable harm** — the slice of total CO harm the device could even theoretically touch (furnace + water-heater sources only).
- **Preventable fraction** — of that addressable slice, the share the device would plausibly have stopped.
- **Point estimate vs range** — a point estimate is a single number; a range (low–high) shows the uncertainty around it. Serious studies report the range.
- **Sensitivity analysis** — re-running the math under different assumptions to see how much the answer moves; proves the result isn't cherry-picked.
- **Attribution** — pinning a death/injury to a specific cause or source. CO records are often weak on this.
- **Pre-registration** — publicly writing down your method *before* you run it, so no one can claim you tuned the method to get the answer you wanted.
- **Device-year** — one device operating for one year; the unit insurers and engineers use to express rare-event rates (e.g., "deaths averted per 1,000 device-years").
- **Low-frequency / high-severity** — rare but catastrophic when it happens. CO's signature shape, and the reason the insurance case is strongest in commercial/landlord lines.

---

*End of specification. Next builds in sequence: (1) the actuarial one-pager that consumes Table 4; (2) the approved-device submission packet that bundles the study + actuarial case for carrier and code-body review.*
