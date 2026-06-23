# classification-rubric.md — Verbatim Case-Coding Rules

> **Read-only reference. This is the exact rulebook for classifying each incident in Phase 2. Apply it literally and identically to every case. Your job is to be a consistent instrument, not a clever one. When a case is ambiguous, the rubric tells you which way to round — and it always rounds against the device.**

For every case in `data/processed/case_corpus.csv`, read the narrative/record and assign each field below. Record a one-to-three-sentence `notes` rationale for every case (mandatory) and a `verdict_confidence` (high/medium/low).

---

## Field-by-field rules

### `intent` — unintentional / intentional / undetermined
- Narrative indicates suicide, homicide, or deliberate exposure → **intentional**.
- Clearly accidental → **unintentional**.
- No indication either way → **undetermined**.
- **Keep only `unintentional`.** Exclude the rest from all prevented/addressable counts.

### `fire_related` — yes / no
- CO arising in the context of a structure fire → **yes** → EXCLUDE.
- Non-fire CO (appliance malfunction, venting failure, etc.) → **no** → keep.
- Unclear → **yes** (conservative: exclude rather than over-count). Note the uncertainty.

### `source_primary` — the appliance that produced the CO
Allowed values and how to choose:
- **furnace** — narrative names a furnace, forced-air heating unit, or central heating system.
- **tank_water_heater** — names a tank/storage water heater (gas).
- **both** — both implicated.
- **generator** — portable/standby generator or engine-driven tool → OUT OF SCOPE.
- **vehicle** — car/truck exhaust (e.g., running in attached garage) → OUT OF SCOPE.
- **range_oven** — gas stove/oven, including used for heat → OUT OF SCOPE.
- **grill** — charcoal/gas grill, hibachi → OUT OF SCOPE.
- **boiler_tankless** — boiler, hydronic, or tankless water heater → OUT OF SCOPE in Base (compatibility unestablished); may be revisited only in a labeled sensitivity case.
- **other** — fireplace, space heater not covered above, etc. → OUT OF SCOPE.
- **unknown** — source not identifiable from the record.

Rule: only `furnace`, `tank_water_heater`, and `both` are **in scope** and count toward addressable harm. `unknown` routes to the unknown-handling rule below. Everything else is **Out of Scope**.

### `failure_mode` — best-supported mechanism (informational; does not by itself decide the verdict)
cracked_heat_exchanger / blocked_or_backdrafting_flue / depressurization / improper_install / maintenance_failure / other / unknown. Record what the narrative supports; "unknown" is acceptable and common.

### `controllable` — could de-energizing the appliance stop the CO production? (Precondition 2)
- Modern gas furnace or water heater with electrical control → **yes**.
- Record indicates a gravity/standing-pilot system where cutting electrical power would **not** stop combustion → **no**.
- Cannot tell → **uncertain**.
- **Scoring:** `no` and `uncertain` both → verdict **Not Prevented** in the Base case.

### `detectable_locus` — would the CO have reached the duct or ambient-near-exhaust sensor? (Precondition 3)
- CO entered via supply air / near the appliance/exhaust → **duct**, **ambient_near_exhaust**, or **both**.
- CO clearly originated and concentrated somewhere geometrically isolated from both sensor positions → **neither** → **Not Prevented**.
- Cannot tell → **unknown** → routes to **Indeterminate**.

### `exposure_profile` — was there a threshold-and-response window? (Precondition 4)
- Gradual buildup over many minutes/hours (classic heat-exchanger or slow backdraft) → **progressive**.
- Instantaneous massive release that incapacitated occupants before any 25 ppm-plus-90-second window could act → **acute_spike** → **Not Prevented**.
- Chronic, very-low-level exposure causing illness over long periods → **chronic_low_level** → **Not Prevented in Base** (no chronic credit in Base; methodology §9).
- Cannot tell → **unknown** → **Indeterminate**.

---

## The verdict (apply the algorithm; do not shortcut it)

Run `docs/methodology.md` §7 in order. The result is exactly one of:

- **Out of Scope** — source is not furnace/tank water heater (or fire/intentional). Not addressable; excluded from both numerator and denominator of the preventable fraction.
- **Not Prevented** — in scope, but a precondition fails (not controllable, wrong locus, acute spike, chronic).
- **Indeterminate** — in scope, but the record is too thin to judge a precondition. **In the Base scenario, counts as Not Prevented.**
- **Prevented** — in scope and all preconditions plausibly hold.

**Preventable fraction (Base) = Prevented ÷ (all in-scope addressable cases).** In-scope addressable = Prevented + Not Prevented + Indeterminate (NOT Out of Scope; NOT excluded fire/intentional).

---

## Unknown-source handling

- A case with `source_primary = unknown` is **not** counted as addressable in the Base case (it does not enter the prevented numerator and it is reported separately, not apportioned in the device's favor).
- Track the unknown count explicitly. In the **High** sensitivity scenario only, a literature-based fraction of unknown-source cases may be apportioned to furnace/water-heater sources — clearly labeled as an upside assumption, never in Base.

---

## Confidence scoring

- **high** — source and the deciding precondition are explicitly stated in the record.
- **medium** — source clear, but at least one precondition inferred.
- **low** — source or a key precondition is inferred from thin detail. Low-confidence Prevented verdicts are reported separately and, in the conservative reading, can be down-weighted.

---

## Worked examples (calibration)

1. *"Family hospitalized; investigators found a cracked heat exchanger in the gas furnace venting CO into the supply ducts over the evening."* → unintentional / non-fire / **furnace** / cracked_heat_exchanger / controllable **yes** / locus **duct** / **progressive** → **Prevented**, confidence high.
2. *"Two found deceased; portable generator running in the basement after a storm."* → **generator** → **Out of Scope**, high.
3. *"Elderly resident died; CO present, no source determined in the record."* → **unknown** → not addressable in Base; tracked separately, medium/low.
4. *"Occupant overcome rapidly; gas water heater, standing pilot, in a closet; sudden venting blockage."* → **tank_water_heater** / controllable **uncertain** (standing pilot) → **Not Prevented** in Base (uncertain controllability rounds against the device), note the reasoning.
5. *"Chronic headaches over a winter later traced to minor flue leakage from the furnace."* → furnace / **chronic_low_level** → **Not Prevented in Base** (no chronic credit), flag for High-scenario discussion only.

---

## The one rule behind all the rules

When in doubt, round **against** the device. Every conservative call you make is what lets the final number withstand a hostile read. A defensible small number is the deliverable; an inflated one is worthless.
