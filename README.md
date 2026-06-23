# CO/PRO Preventability Modeling Study

Repository for the counterfactual modeling study estimating how much furnace /
water-heater carbon-monoxide harm a source-shutoff device could prevent.

## Start here
1. Read **SETUP.md** (spoiler: no API keys or accounts needed).
2. Claude Code reads **CLAUDE.md** first — it is the build controller.

## What's pre-supplied (read-only inputs)
- `CLAUDE.md` — build controller: gates, runbook, definition of done
- `SETUP.md` — credentials/setup note
- `docs/methodology.md` — the scientific design
- `docs/classification-rubric.md` — verbatim case-coding rules
- `templates/` — the two authoring deliverables as fill-in shells

## What Claude Code creates when it runs
- `data/raw/`, `data/processed/` — source data + cleaned/classified sets
- `scripts/` — every analysis script (re-runnable)
- `outputs/` — PREREGISTRATION, GATES log, PHASE1_REVIEW, tables/, FINDINGS, RUN_SUMMARY
- `deliverables/` — the filled actuarial one-pager and approved-device packet

(Empty folders are seeded with `.gitkeep` so the structure is visible before the run.)
