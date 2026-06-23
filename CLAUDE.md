# CLAUDE.md — Build Controller: CO/PRO Preventability Modeling Study

> **You are Claude Code. This file governs the entire project. Read it fully before doing anything. Follow it exactly. Do not improvise scope, methods, or assumptions — everything you need is here or in the referenced files. When something genuinely cannot be resolved from these documents, you HALT and log it (see the Gate Protocol); you do not guess.**

---

## 0. Prime directive

Execute the counterfactual modeling study defined in `docs/methodology.md`, producing the output tables it specifies, then populate the two authoring deliverables from those tables. Run **autonomously through the phases**, governed by **gates**: automated pass/fail checks you run on your own work at the end of each phase. As long as gates pass, keep going. The instant a gate fails, you **stop, log the failure, and wait** — you never proceed past a failed gate.

Your goal is not speed. It is a result that **survives a hostile read by an insurance underwriter or regulator.** Conservative and defensible beats large and fragile, every time.

---

## 1. How you work (the Gate Protocol)

This is the heart of the project. Internalize it.

- The work is split into **Phases 0–4**. Each phase has an **objective, inputs, tasks, outputs, and an EXIT GATE.**
- An **EXIT GATE** is a numbered list of concrete pass/fail assertions about your own output.
- At the end of every phase you **run the gate**: evaluate each assertion, write the result to `outputs/GATES.md` (append, never overwrite), and:
  - **All assertions PASS** → log `GATE n: PASS`, then proceed to the next phase.
  - **Any assertion FAILS** → log `GATE n: FAIL` with the specific assertion(s), write what you observed, write your best hypothesis for the cause, and **HALT**. Do not attempt the next phase. Do not "work around" it silently. Stop and surface it.
- `outputs/GATES.md` is the project's audit trail and your running log. Every gate evaluation, every halt, every resume goes here, timestamped.
- **You may self-correct *within* a phase** (a failed assertion you can fix by redoing the phase's own work — e.g., re-pulling a file that downloaded corrupt). Log the correction. But a gate failure rooted in a *methodological* problem (data won't support the claim, classification accuracy too low, numbers don't reconcile) is a HALT, not a self-fix — those require a human decision.
- **Never tune a method to pass a gate.** If a gate fails because the honest result is unfavorable, that is a finding, not a bug. Log it as such and halt.

---

## 2. The dependency chain (why order is non-negotiable)

```
docs/methodology.md  ──▶  PHASE 1 & 2 (run the study)  ──▶  PHASE 3 (numbers: Tables 1–4)
                                                                      │
                                                                      ▼
                                                      PHASE 4 (author deliverables FROM the numbers)
```

The two authoring deliverables — the actuarial one-pager and the approved-device packet — are **blocked** until Phase 3 produces real numbers. Their templates contain `{{placeholders}}` that map to specific output cells. **You may not fill a placeholder with anything you did not compute in Phases 1–3.** No invented figures, ever. If Phase 3 hasn't produced a number a template needs, that placeholder stays empty and you log the gap.

---

## 3. Repository structure (the human created the repo; you create and populate everything below it)

```
.
├── CLAUDE.md                         ← this file (controller)
├── docs/
│   ├── methodology.md                ← the scientific design (pre-supplied; read-only reference)
│   └── classification-rubric.md      ← verbatim case-coding rules (pre-supplied; read-only reference)
├── templates/
│   ├── actuarial-one-pager.template.md
│   └── approved-device-packet.template.md
├── data/
│   ├── raw/                          ← you create: unmodified downloaded source data
│   └── processed/                    ← you create: cleaned, classified datasets
├── scripts/                          ← you create: every script you write lives here, named by phase
├── outputs/
│   ├── PREREGISTRATION.md            ← you create FIRST (Phase 0), before any analysis
│   ├── GATES.md                      ← you create: the running gate/audit log
│   ├── PHASE1_REVIEW.md              ← you create: human-readable Phase-1 result + provenance
│   └── tables/                       ← you create: Tables 1–4 as both .md and .csv
└── deliverables/                     ← you create: the FILLED templates (Phase 4 only)
    ├── actuarial-one-pager.md
    └── approved-device-packet.md
```

Rules: **never modify** `docs/` or `templates/` (read-only inputs). All raw downloads land in `data/raw/` untouched; all transformations are scripted into `data/processed/` so every number is reproducible from a script. No manual edits to data.

---

## 4. Environment & tooling (Phase 0 establishes this)

- **Language:** Python 3. Install with `pip install --break-system-packages` as needed.
- **Core libraries:** `pandas`, `requests`, `pdfplumber` (for CPSC PDF report tables), `beautifulsoup4`, `matplotlib` (charts only if a table benefits). Install what you use; record versions in `PREREGISTRATION.md`.
- **Internet:** available via bash. You may fetch public data and documentation URLs. Cache everything you pull into `data/raw/` so the run is reproducible offline.
- **No paid APIs, no API keys.** Everything used must be free and public. If a source requires registration or manual export you cannot complete autonomously, you do **not** fake it — you document the exact retrieval steps in `data/raw/MANUAL_FETCH_NEEDED.md` (precise query parameters, the URL, the export format) and treat that dataset as pending (see §5).

---

## 5. Data sources & access reality (read before Phase 1)

Full source table is in `docs/methodology.md` §5. Operational notes:

| Source | Access | Your handling |
|---|---|---|
| **CPSC annual "Non-Fire Carbon Monoxide Deaths…" reports** | Public PDFs | Download last 5 available years to `data/raw/cpsc_reports/`. Extract the by-source tables with `pdfplumber`. **Primary Phase-1 source.** |
| **CDC WONDER** (mortality) | Web query tool; limited programmatic access | Pull the CO-poisoning totals you can; if the query must be run by hand, write exact steps to `MANUAL_FETCH_NEEDED.md` and proceed using CPSC totals, flagging the cross-check as pending. |
| **CPSC NEISS** (injuries, narratives) | Public query + downloadable data | Pull CO-related narratives for Phase 2. |
| **NFIRS** (fire-service incidents) | Registration/request often required | If unattainable autonomously, document the request steps; do **not** block the study on it — it is supplementary, not load-bearing. |
| **Peer-reviewed attribution fractions** | Public abstracts/papers | Use to ground the literature-based preventable fraction in Track A. Cite every figure used. |

**Provenance rule:** every external number you use gets a citation (source, year, page/table, URL) recorded next to it in the relevant output file. A figure with no provenance is a gate failure.

---

## 6. THE RUNBOOK

### PHASE 0 — Setup & pre-registration
**Objective:** lock the method before touching results; confirm you can execute.
**Tasks:**
1. Read `docs/methodology.md` and `docs/classification-rubric.md` end to end.
2. Set up the environment (§4); record library versions.
3. Write `outputs/PREREGISTRATION.md`: restate the research question, scope in/out, the preventability decision algorithm, every conservative assumption, and the three sensitivity scenarios — **copied from the methodology, dated now.** This is the "we decided the method before we saw the answer" record.
4. Probe each data source for reachability; log status (reachable / manual-fetch-needed) to `data/raw/SOURCE_STATUS.md`.

**EXIT GATE 0 — all must pass:**
- 0.1 `PREREGISTRATION.md` exists and contains the question, scope, algorithm, assumptions, and the three scenarios.
- 0.2 Environment works (a trivial `pandas` script runs).
- 0.3 At least the **CPSC report source is reachable** (it is the irreducible minimum for Phase 1). If CPSC reports cannot be obtained, HALT — the study cannot proceed without them.
- 0.4 `SOURCE_STATUS.md` documents the access state of every source, with manual steps written for any that need them.

---

### PHASE 1 — Population-level estimate (Track A)
**Objective:** a fast, defensible first estimate without classifying raw records.
**Inputs:** CPSC by-source death tables; CDC totals if obtained; literature preventable fraction.
**Tasks:**
1. Extract non-fire unintentional CO death counts **by source category**, last 5 available years, into `data/processed/trackA_sources.csv`.
2. Compute **addressable harm** = furnace + tank-water-heater share, multi-year averaged. Carve out generators/vehicles/grills/ranges explicitly (methodology §3).
3. Apply a **literature-grounded preventable fraction** (cite it) to produce Low / Base / High addressable-harm-prevented figures.
4. Write `outputs/PHASE1_REVIEW.md`: the headline number, every input with provenance, the sanity-check results, and a plain-language statement of what it does and doesn't claim.

**EXIT GATE 1 — all must pass:**
- 1.1 **Reconciliation:** the CPSC source categories sum to within ±5% of that report's stated non-fire CO total. (If not, extraction is wrong → self-fix and re-run; if the report itself doesn't reconcile, HALT and log.)
- 1.2 **Magnitude cross-check:** if CDC totals were obtained, the CPSC total sits within a documented, explained band of the CDC total. Large unexplained divergence → HALT. (If CDC pending, log the cross-check as deferred — not a failure.)
- 1.3 **Plausibility:** addressable fraction is >0% and <100%; the prevented count ≤ addressable count in all three scenarios.
- 1.4 **Multi-year:** every headline figure is a multi-year average, never a single year.
- 1.5 **Provenance complete:** every number in `PHASE1_REVIEW.md` carries a citation. Any orphan number → HALT.
- 1.6 **Scenario ordering:** Low ≤ Base ≤ High.

*(On PASS: proceed. `PHASE1_REVIEW.md` is the artifact a human can review asynchronously; you do not wait on them unless a gate failed.)*

---

### PHASE 2 — Case-level classification (Track B)
**Objective:** a bottom-up preventable fraction, auditable case by case.
**Inputs:** NEISS narratives, CPSC investigation/case detail, NFIRS (if available); the rubric in `docs/classification-rubric.md`.
**Tasks:**
1. Assemble the case corpus into `data/processed/case_corpus.csv` (one row per incident, with the source narrative text).
2. **Classify every case strictly per `docs/classification-rubric.md`**, populating the taxonomy fields (methodology §6) **plus a mandatory non-empty `notes` rationale and a `verdict_confidence`** for each.
3. **Build the validation sample:** before trusting the full classification, hand-label a random sample (target ≥100 cases or 10% of corpus, whichever is larger) by applying the rubric carefully yourself in a separate pass, then compare to the bulk classification. Record agreement rate to `outputs/tables/validation_accuracy.md`.
4. Aggregate verdicts → Track B preventable fraction (Low/Base/High per the §9 conservative rules: Indeterminate and Unknown count against the device in Base).

**EXIT GATE 2 — all must pass:**
- 2.1 **Audit trail complete:** 100% of classified cases have a non-empty `notes` rationale and a `verdict_confidence`. Any blank → HALT.
- 2.2 **Classification accuracy:** validation-sample agreement ≥ **90%**. Below 90% → the rubric is being applied inconsistently → HALT (the rubric needs human revision; do not proceed on shaky classification).
- 2.3 **Conservative routing verified:** spot-confirm that Indeterminate/Unknown/uncertain-controllability cases are scored against the device in the Base scenario, per methodology §9.
- 2.4 **Track reconciliation:** Track B Base preventable fraction is within a documented band of Track A's. If they diverge sharply, **do not average them** — HALT, log both, and surface the divergence as the finding it is.

---

### PHASE 3 — Sensitivity & output tables
**Objective:** the final numbers, with their uncertainty, segmented where it matters.
**Tasks:**
1. Run all three scenarios (methodology §10) across both tracks.
2. Produce **Tables 1–4** (methodology §12) as both `.md` and `.csv` in `outputs/tables/`.
3. **Segment Table 4 (per-device-year harm reduction) by occupancy type** — single-family vs multifamily/commercial — because the downstream actuarial case depends on this split.
4. Write a short `outputs/tables/FINDINGS.md` stating the Base headline and the Low–High band in plain language, with the honest caveats.

**EXIT GATE 3 — all must pass:**
- 3.1 All four tables exist in both formats; no cell is blank without an explicit "n/a — reason."
- 3.2 Scenario ordering holds in every table (Low ≤ Base ≤ High).
- 3.3 **Traceability:** every figure in every table is reproducible from a script in `scripts/` (no hand-entered numbers). Spot-check three at random; if any can't be traced → HALT.
- 3.4 Table 4 is segmented by occupancy type.
- 3.5 **Honesty checklist** (methodology §9) fully satisfied: generators carved out, unknown/indeterminate scored against device, device-failure discount applied, no chronic-morbidity credit in Base, multi-year averaging throughout. Any item unmet → HALT.

---

### PHASE 4 — Author deliverables (UNLOCKED ONLY BY GATE 3 PASS)
**Objective:** turn numbers into the two persuasion documents.
**Tasks:**
1. Copy `templates/actuarial-one-pager.template.md` → `deliverables/actuarial-one-pager.md`. Fill every `{{placeholder}}` from the Table-4 / Findings outputs. Where the template needs an external loss-cost input the study didn't produce (settlement values, claim frequencies), **do not invent it** — leave the placeholder, and list it in a `## INPUTS STILL NEEDED` block at the top for the human to supply.
2. Copy `templates/approved-device-packet.template.md` → `deliverables/approved-device-packet.md`. Fill from study outputs + the product spec facts; same no-invention rule.

**EXIT GATE 4 — all must pass:**
- 4.1 No `{{placeholder}}` remains *that could have been filled from study outputs.* Any placeholder left empty is listed under `INPUTS STILL NEEDED` with what's required and who supplies it.
- 4.2 Every quantitative claim in both deliverables traces to a specific table/cell in `outputs/tables/`. No figure appears that isn't in the study output.
- 4.3 Both deliverables include their limitations/honesty section (carried from `FINDINGS.md`).
- 4.4 Tone check: neither document overstates. Phrases like "would prevent" appear only as "plausibly would have prevented, under stated assumptions."

---

## 7. The honesty protocol (cross-cutting — applies in every phase)

Bake these in continuously, not just at gates:
- Carve out everything the device can't touch (methodology §3). Shrinking the number on purpose is the job.
- Score uncertainty against the device in the Base case. Always.
- Apply the device-failure discount. A working device still isn't perfect.
- Cite every external figure. No orphan numbers.
- An unfavorable honest result is a valid, valuable outcome — log it plainly, never massage it.
- Pre-registration (Phase 0) locks the method before results exist, so no one can claim it was tuned.

---

## 8. Definition of Done

The project is complete when **all** exist and **all gates logged PASS** in `outputs/GATES.md`:
- `outputs/PREREGISTRATION.md`
- `outputs/PHASE1_REVIEW.md`
- `outputs/tables/` → Tables 1–4 (.md + .csv), `validation_accuracy.md`, `FINDINGS.md`
- `data/raw/` (cached sources) + `data/processed/` (trackA_sources.csv, case_corpus.csv, classified set)
- `scripts/` (every analysis script, phase-named, re-runnable)
- `deliverables/actuarial-one-pager.md` + `deliverables/approved-device-packet.md` (filled, with any gaps under `INPUTS STILL NEEDED`)
- `outputs/GATES.md` showing the full PASS trail

When done, write a final `outputs/RUN_SUMMARY.md`: what was produced, the headline finding with its band, every HALT encountered and how it resolved, and every `INPUTS STILL NEEDED` item outstanding for the human.

---

## 9. If you are unsure

You do not guess. You HALT, log the question precisely in `GATES.md`, and stop. A clean halt with a clear question is a success. A silent assumption is the one failure mode this whole structure exists to prevent.
