# MANUAL_FETCH_NEEDED.md

> Sources that could not be pulled autonomously. Each entry gives the exact retrieval
> steps so a human can fetch it in a couple of minutes. **Nothing here blocks the study**
> — each affected check is logged as *deferred* in `outputs/GATES.md`, and re-running the
> relevant phase after the file is dropped in will fold the data in. No data is faked.

---

## 1. CDC WONDER — national CO-poisoning mortality totals (magnitude cross-check, DEFERRED)

**Why manual:** CDC WONDER is an interactive query-builder gated by a session and a
data-use agreement. The datarequest endpoint returned HTTP 500 to an unauthenticated
programmatic call. This is the expected, documented friction (see `SETUP.md` §2).

**What it's for:** a *cross-check on magnitude only* (Gate 1.2). CDC ICD-10 codes do not
name the appliance, so CDC is **not** used for source attribution — only to confirm the
CPSC national total sits in a plausible band. Its absence does not change any headline
number; the study proceeds on CPSC totals.

**Exact steps to fetch (≈2 minutes):**
1. Go to **https://wonder.cdc.gov/ucd-icd10.html** (Underlying Cause of Death, 1999–2020)
   and/or **https://wonder.cdc.gov/ucd-icd10-expanded.html** (2018+ expanded) — accept the terms.
2. **Group Results By:** `Year`.
3. **Demographics / Year:** select the most recent 5 available years (to match the CPSC
   2018–2022 window).
4. **Cause of death → ICD-10 Codes**, select **underlying cause**:
   - `T58` (Toxic effect of carbon monoxide) — *for contributing-cause cross-reference*, and
   - `X47` (Accidental poisoning by/exposure to other gases and vapours — includes CO),
   - exclude `X67` (intentional) and `Y17` (undetermined) to match the study's unintentional scope,
     or pull them separately so the intentional share can be removed.
5. **Other options:** keep "Export Results" checked; leave suppression at defaults.
6. **Send** → on the results page click **Export** → save the tab-delimited file as:
   `data/raw/cdc_wonder/cdc_co_mortality_by_year.txt`
7. Re-run Phase 1 (`scripts/phase1_*`); the CDC band cross-check (Gate 1.2) will activate automatically.

**Note:** WONDER underlying-cause data may lag (often through 2020–2021). If the most recent
CPSC years (2021–2022) are not yet in WONDER, the cross-check uses the overlapping years only;
that is acceptable and should be noted, not forced.

---

## 2. NFIRS — fire-service CO incident microdata (SUPPLEMENTARY, not load-bearing)

**Why manual:** USFA/FEMA NFIRS research microdata requires a (free) registration/request;
it cannot be pulled autonomously.

**What it's for:** an *optional* additional Track-B narrative source. The study is designed to
produce its result without NFIRS (methodology §5; SETUP.md §2).

**Exact steps to request (optional):**
1. Search "USFA NFIRS public data release research" for the current request portal.
2. Request the most recent available NFIRS Public Data Release (PDR) flat files.
3. On receipt, place CO-relevant incident extracts in `data/raw/nfirs/` and re-run Phase 2;
   the case corpus assembly will include them.

If you do not want fire-service data, no action is needed — the study completes without it.
