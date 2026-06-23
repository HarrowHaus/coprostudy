# Validation Accuracy — Track B Classification (Gate 2.2)

**Sample:** 253 cases (>= max(100, 10% of corpus); seed-reproducible).
**Design:** the bulk **rule-based** classifier vs an **independent** second-pass classification of the SAME cases, performed blind to the rule output (two different instruments applying the same rubric — methodology Sec.11).

| Metric | Agreement |
|---|---|
| **Preventability verdict (gate metric)** | **94.5%** (239/253) |
| Scope class (in-scope / out-of-scope / unknown) | 68.4% (173/253) |

**GATE 2.2 (>= 90% verdict agreement): PASS**

## Verdict confusion (rows = independent, cols = bulk)
| independent \ bulk | Excluded | Out of Scope | Unknown-Source | Indeterminate | Not Prevented | Prevented |
|---|---|---|---|---|---|---|
| Excluded | 85 | 3 | 3 | 0 | 0 | 0 |
| Out of Scope | 0 | 70 | 4 | 0 | 0 | 0 |
| Unknown-Source | 0 | 0 | 68 | 0 | 0 | 0 |
| Indeterminate | 0 | 0 | 0 | 0 | 0 | 0 |
| Not Prevented | 0 | 0 | 0 | 0 | 6 | 1 |
| Prevented | 0 | 1 | 1 | 0 | 1 | 10 |

## Disagreements (14)
| case_id | indep source | indep verdict | bulk source | bulk verdict |
|---|---|---|---|---|
| NEISS-2019-190618322 | other | Excluded | unknown | Unknown-Source |
| NEISS-2019-191030416 | furnace | Prevented | other | Out of Scope |
| NEISS-2020-200161357 | furnace | Not Prevented | furnace | Prevented |
| NEISS-2020-200254201 | other | Excluded | other | Out of Scope |
| NEISS-2020-201109455 | furnace | Prevented | unknown | Unknown-Source |
| NEISS-2020-201137376 | other | Out of Scope | unknown | Unknown-Source |
| NEISS-2020-201242263 | other | Excluded | other | Out of Scope |
| NEISS-2020-201243427 | other | Out of Scope | unknown | Unknown-Source |
| NEISS-2021-210433635 | other | Out of Scope | unknown | Unknown-Source |
| NEISS-2021-211202924 | other | Excluded | other | Out of Scope |
| NEISS-2022-220544765 | other | Excluded | unknown | Unknown-Source |
| NEISS-2022-220557147 | other | Excluded | unknown | Unknown-Source |
| NEISS-2023-230860022 | both | Prevented | both | Not Prevented |
| NEISS-2023-231206813 | other | Out of Scope | unknown | Unknown-Source |
