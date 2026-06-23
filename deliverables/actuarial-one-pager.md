# CO/PRO Source-Shutoff — Loss-Avoidance Brief

## INPUTS STILL NEEDED
*(External loss-cost inputs the study did not produce. The study stops at harm-averted per device-year, Table 4; the dollar conversion needs these. No values are invented.)*
- **`cost_per_death`** — average CO wrongful-death / bodily-injury settlement or loss reserve per fatality (carrier actuarial / claims). [EXTERNAL]
- **`cost_per_injury`** — average CO bodily-injury + medical cost per ED-treated CO injury. [EXTERNAL]
- **`cost_per_property_claim`** — average associated property/fire claim avoided per prevented incident. [EXTERNAL]
- **`loss_avoided` / `breakeven_credit`** — derived once the three costs above are supplied (formula and harm-averted inputs are already in place below).

---

### For underwriting / risk evaluation — single-family lines (primary); multifamily/commercial (limited — see note)

**The device, in one line.** A duct-and-ambient carbon-monoxide source-shutoff that de-energizes the furnace and tank water heater at 25 ppm, stopping CO production at the source — distinct from a hallway alarm, which only warns. *(Supplemental to, not a replacement for, code-required CO alarms.)*

**The addressable hazard (scoped, not inflated).** Of U.S. non-fire unintentional CO harm, this device addresses only the furnace and water-heater fraction — generators (~110 deaths/yr alone), vehicles, grills, and ranges are explicitly excluded.
- Addressable deaths/yr: **~28.6** (≈12% of non-fire consumer-product CO deaths) `[STUDY:Table1]`
- Addressable serious (ED-treated) injuries/yr: **~1,273** `[STUDY:Table1]`

**Modeled mitigation effect (conservative; full method pre-registered).**
- Preventable fraction reported **separately by outcome** (never averaged):
  - **Deaths — Base 38%** (range **21%–61%**) `[STUDY:Table2, Track A]`
  - **Injuries — Base 59%** (range **50%–94%**) `[STUDY:Table2, Track B, 94.5%-validated]`
- Method: counterfactual modeling over public incident data (CPSC death reports + NEISS injury narratives); unknowns and indeterminates scored against the device; explicit device non-actuation discount applied. *(Mirrors the CPSC's own generator-rule analysis in form.)*

**Expected harm reduction per device-year — segmented (the underwriting-relevant figure).**
*(Expressed per **100,000 device-years**; the per-unit number is tiny because CO is rare-but-catastrophic. Base scenario.)*

| Occupancy | Device-homes | Deaths averted / 100k device-yrs | Injuries averted / 100k device-yrs |
|---|---|---|---|
| Single-family | 52.6M | **0.020** | **1.36** |
| Multifamily / commercial | 7.7M | **0.0065** | **0.45** |

> **Note the shape — and an honest reversal of the usual assumption.** CO is **low-frequency / high-severity**, so the per-unit number is small everywhere. But for the device's **in-scope appliances** (forced-air furnaces + tank water heaters), the harm — and therefore the per-device benefit — is **concentrated in single-family**, not multifamily/commercial. Multifamily/commercial CO severity is driven by **central boilers and larger systems that are out of scope** for this device. The commercial case is therefore **built in single-family first**, and the multifamily/commercial case waits on a boiler-compatible variant (separately validated).

**Loss-avoidance translation.**
```
Expected loss avoided / device-year
  = (deaths averted/device-yr   × {{cost_per_death [EXTERNAL]}})
  + (injuries averted/device-yr × {{cost_per_injury [EXTERNAL]}})
  + (associated property/fire claims avoided × {{cost_per_property_claim [EXTERNAL]}})
```
- Expected loss avoided / device-year: **pending the three external loss-costs above** (see INPUTS STILL NEEDED). The harm-averted multiplicands are ready: e.g., single-family Base = **0.020 deaths + 1.36 injuries per 100,000 device-years**.

**The breakeven.**
```
A premium credit or device subsidy is favorable to the carrier when:
   cost of the credit/subsidy  <  expected loss avoided / device-year
```
- Implied favorable credit ceiling: **DERIVED once loss-costs are supplied** (not invented).
- Precedent: carriers already reward *automatic shutoff* over detection in the water-leak category (incremental credit specifically for an automatic valve), and at least one high-value carrier already discounts automatic **gas-line** shutoff valves.

**The ask (modest, specific).**
- List the device as an approved/recognized above-code CO **mitigation** device; pilot a small premium credit in a **single-family** book (where the modeled benefit concentrates); and enter a data-sharing trial to validate the modeled harm-reduction against claims experience. *Defer the multifamily/commercial credit until a boiler-compatible variant is validated.*

**Honesty / limitations.** Modeled, pre-registered, conservative: addressable harm is a scoped ~12% of non-fire CO deaths; "would have prevented" is a modeled inference under stated assumptions, **not field-observed**; deaths and injuries are different populations and are never averaged; the in-scope benefit is **single-family-concentrated**; this is a manufacturer-affiliated analysis offered with transparent method and pre-registration; **field-pilot validation is the next step, not yet complete.** (Full caveats: `outputs/tables/FINDINGS.md`.)

*Sources & full method: `outputs/` (this repo) and `docs/methodology.md`.*
