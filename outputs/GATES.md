# GATES.md — Gate / Audit Log

> Append-only running log of every gate evaluation, halt, deferral, and resume.
> Each phase's EXIT GATE is evaluated here against the phase's own output before
> proceeding. A failed gate rooted in a methodological problem is a HALT, not a
> work-around (CLAUDE.md §1).

---

## 2026-06-23T13:22:29Z — GATE 0 (Setup & pre-registration)

**Phase 0 objective:** lock the method before results; confirm executability.

| # | Assertion | Result | Evidence |
|---|---|---|---|
| 0.1 | `PREREGISTRATION.md` exists with question, scope, algorithm, assumptions, three scenarios | **PASS** | `outputs/PREREGISTRATION.md` §1–§7 written and dated before any analysis. |
| 0.2 | Environment works (trivial pandas script runs) | **PASS** | Python 3.11.15; pandas 3.0.3 / pdfplumber 0.11.10 / bs4 4.15.0 / matplotlib 3.11.0 / requests 2.33.1 / cffi 2.0.0 all import; pandas DataFrame round-trip OK. |
| 0.3 | CPSC report source reachable (irreducible minimum) | **PASS** | 5 reports (2018–2022 editions) downloaded to `data/raw/cpsc_reports/`, valid PDFs, SHA-256 recorded; latest tabulates 2012–2022. pdfplumber confirmed Table 1 (by-product deaths) is extractable. |
| 0.4 | `SOURCE_STATUS.md` documents access state of every source, with manual steps where needed | **PASS** | `data/raw/SOURCE_STATUS.md` covers CPSC / CDC WONDER / NEISS / NFIRS / literature. CDC WONDER + NFIRS manual steps in `data/raw/MANUAL_FETCH_NEEDED.md`. |

**Deferrals logged (not failures):**
- **CDC WONDER magnitude cross-check** — DEFERRED. Programmatic endpoint 500; manual-fetch steps documented. Methodology §5 / Gate 1.2 explicitly permit deferral; study proceeds on CPSC totals.
- **NFIRS** — DEFERRED (supplementary, not load-bearing).

### GATE 0: PASS
All four assertions pass. The two deferrals are sanctioned by the methodology and do not block.
**Proceeding to Phase 1 (Track A — population-level estimate).**

---
