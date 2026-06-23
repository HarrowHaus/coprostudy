# actuarial-one-pager.template.md

> **TEMPLATE — Phase 4 only. Copy to `deliverables/actuarial-one-pager.md` and fill every `{{placeholder}}` from study outputs. Placeholders tagged `[STUDY]` come from your Tables/Findings. Placeholders tagged `[EXTERNAL]` are loss-cost inputs the study did NOT produce — do not invent them; leave them and list them under `INPUTS STILL NEEDED`. Audience: an insurance underwriter / risk officer. One page. Risk math, not marketing.**

---

## INPUTS STILL NEEDED
*(List every `[EXTERNAL]` placeholder you could not fill, what it is, and who supplies it. Delete this block only if empty.)*
- …

---

# CO/PRO Source-Shutoff — Loss-Avoidance Brief
### For underwriting / risk evaluation — {{occupancy_line}} lines

**The device, in one line.** A duct-and-ambient carbon-monoxide source-shutoff that de-energizes the furnace and tank water heater at 25 ppm, stopping CO production at the source — distinct from a hallway alarm, which only warns. *(Supplemental to, not a replacement for, code-required CO alarms.)*

**The addressable hazard (scoped, not inflated).** Of U.S. non-fire unintentional CO harm, this device addresses only the furnace and water-heater fraction — generators, vehicles, grills, and ranges are explicitly excluded.
- Addressable deaths/yr: **{{addressable_deaths [STUDY:Table1]}}**
- Addressable serious injuries/yr: **{{addressable_injuries [STUDY:Table1]}}**

**Modeled mitigation effect (conservative; full method pre-registered).**
- Preventable fraction — Base: **{{preventable_base [STUDY:Table2]}}** (range **{{preventable_low}}–{{preventable_high}}**)
- Method: counterfactual modeling over public incident data; unknowns and indeterminates scored against the device; device-failure discount applied. *(Mirrors the CPSC's own generator-rule analysis in form.)*

**Expected harm reduction per device-year — segmented (the underwriting-relevant figure).**
| Occupancy | Deaths averted / 1,000 device-yrs | Injuries averted / 1,000 device-yrs |
|---|---|---|
| Single-family | {{sf_deaths_per_k [STUDY:Table4]}} | {{sf_injuries_per_k [STUDY:Table4]}} |
| Multifamily / commercial | {{mf_deaths_per_k [STUDY:Table4]}} | {{mf_injuries_per_k [STUDY:Table4]}} |

> Note the shape: CO is **low-frequency / high-severity.** The per-unit number is small in single-family and materially larger in multifamily/commercial, where one wrongful-death tail event dominates. The case is built there first.

**Loss-avoidance translation.**
```
Expected loss avoided / device-year
  = (deaths averted/device-yr   × {{cost_per_death [EXTERNAL: avg CO wrongful-death/BI settlement]}})
  + (injuries averted/device-yr × {{cost_per_injury [EXTERNAL: avg CO bodily-injury + medical]}})
  + (associated property/fire claims avoided × {{cost_per_property_claim [EXTERNAL]}})
```
- Expected loss avoided / device-year — {{occupancy_line}}: **{{loss_avoided [STUDY×EXTERNAL]}}**

**The breakeven.**
```
A premium credit or device subsidy is favorable to the carrier when:
   cost of the credit/subsidy  <  expected loss avoided / device-year
```
- Implied favorable credit ceiling: **{{breakeven_credit [DERIVED]}}**
- Precedent: carriers already reward *automatic shutoff* over detection in the water-leak category (e.g., incremental credit specifically for an automatic valve), and at least one high-value carrier already discounts automatic **gas-line** shutoff valves.

**The ask (modest, specific).**
- {{the_ask — e.g., list as an approved/recognized mitigation device; pilot a credit in one multifamily book; enter a data-sharing trial to validate against claims experience}}

**Honesty / limitations.** {{limitations [STUDY:Findings]}} — "would have prevented" is a modeled inference under stated conservative assumptions, not field-observed; manufacturer-affiliated analysis, offered with transparent method and pre-registration; field-pilot validation is the next step, not yet complete.

*Sources & full method: `outputs/` (this repo) and `docs/methodology.md`.*
