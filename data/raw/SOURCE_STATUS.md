# SOURCE_STATUS.md — Data-source reachability (Phase 0)

**Probed (UTC):** 2026-06-23T13:22:29Z
**Method:** HTTP probes via `curl` from the analysis environment; CPSC report PDFs downloaded and validated.

| Source | Status | Evidence | Handling |
|---|---|---|---|
| **CPSC Non-Fire CO Death annual reports** | ✅ **REACHABLE** | 5 PDFs downloaded to `data/raw/cpsc_reports/` (HTTP 200; valid PDF v1.6; SHA-256 in `SHA256SUMS.txt`). Latest edition (2022) tabulates 2012–2022 by product. | **Primary Phase-1 source.** Extract Table 1 (by-product deaths) with pdfplumber. |
| **CDC WONDER (mortality, ICD-10)** | ⚠️ **MANUAL-FETCH** | Landing page `ucd-icd10.html` → HTTP 200; datarequest API endpoint `D76` → HTTP 500 (session/terms-gated; no autonomous programmatic pull). | Steps written to `data/raw/MANUAL_FETCH_NEEDED.md`. CDC magnitude cross-check **DEFERRED** (methodology §5; Gate 1.2 allows deferral — not a blocker). Proceed on CPSC totals. |
| **CPSC NEISS (injury narratives)** | ✅ **REACHABLE** | `Research--Statistics/NEISS-Injury-Data` → HTTP 200. | Pull deferred to Phase 2 (case corpus). |
| **NFIRS (fire-service incidents)** | ⏸️ **REQUEST-REQUIRED / SUPPLEMENTARY** | USFA research microdata typically requires registration/request. | Document request steps; **not load-bearing**; study does not block on it (SETUP.md §2, methodology §5). |
| **Peer-reviewed CO epidemiology** | ✅ **PUBLIC** | Abstracts/papers publicly retrievable. | Cite each figure used (preventable fraction, device-failure basis) in Phase 1. |

## CPSC reports cached

| Edition | File | Bytes | Source URL (CPSC s3fs-public, versioned) |
|---|---|---|---|
| 2018 | `cpsc_co_2018.pdf` | 1,553,434 | `…/Non-Fire-Carbon-Monoxide-Deaths-…-2018-Annual-Estimates.pdf?VersionId=fzyP7THVI_9l6x9TeT10xb5unqo4Qc0H` |
| 2019 | `cpsc_co_2019.pdf` | 1,785,112 | `…/NonFireCarbonMonoxideDeaths…2019AnnualEstimates.pdf?VersionId=90WCZoH61aVUrTgDtOo16LLKZf1EeH3E` |
| 2020 | `cpsc_co_2020.pdf` | 2,388,513 | `…/Non-Fire-Carbon-Monoxide-Deaths-…-2020-Annual-Estimates.pdf?VersionId=mQ7JXFB_ec1GKlFgVQkLYCwN5_fybL4S` |
| 2021 | `cpsc_co_2021.pdf` | 1,796,366 | `…/Non-Fire-Carbon-Monoxide-Deaths-…-2021-Annual-Estimates-FY24.pdf?VersionId=220cncY7uzDF7iJuVNajVy1oP3Qj4w0d` |
| 2022 | `cpsc_co_2022.pdf` | 1,220,646 | `…/Non-Fire-Carbon-Monoxide-Deaths-…-2022-Annual-Estimates.pdf?VersionId=Mrnl7sqn3cjTUYyWDPBywktYX6THlwdh` |

All under host `https://www.cpsc.gov/s3fs-public/`. Index page: `https://www.cpsc.gov/Research--Statistics/Carbon-Monoxide`.

**Irreducible-minimum check (Gate 0.3):** CPSC report source is reachable and cached → **PASS**. The study can proceed to Phase 1.
