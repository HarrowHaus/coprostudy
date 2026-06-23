# SETUP.md — What you need before running (spoiler: no keys)

> **Read this once before running Claude Code. Short version: there is nothing to provision. No API keys, no paid accounts, no credentials. CO incident data is public. This file just documents the two small bits of friction that *can* come up, so neither you nor Claude Code is surprised.**

---

## 1. The bottom line

| Question | Answer |
|---|---|
| API keys needed? | **No.** |
| Paid accounts needed? | **No.** |
| Anything to put in the repo as secrets/credentials? | **No.** Nothing. |
| Can the study run start-to-finish without any setup from you? | **Yes**, in the expected case. The two items below are the only possible exceptions, and neither blocks the core study. |

There is no `.env` file, no secrets manager, no login. If any instruction ever asks you for a key for this project, something is wrong — these datasets don't use them.

---

## 2. The data sources, by how much they need you

**Runs on its own (no action from you):**
- **CPSC "Non-Fire Carbon Monoxide Deaths…" annual reports** — public PDFs, direct download. *This is the irreducible minimum for the study, and it's the least likely to give trouble.*
- **CPSC NEISS** (injury narratives) — public query tool + downloadable data, no login.

**Public, but *might* need a 2-minute manual export from you:**
- **CDC WONDER** (mortality data) — free, no account. It's a web query-builder, so programmatic pulls are awkward. Claude Code will try to script it; if it can't, it writes the exact query parameters to `data/raw/MANUAL_FETCH_NEEDED.md`, and you run the query in your browser and export the CSV (literally a couple of minutes). **This does not halt the study** — Code proceeds using CPSC totals and flags the CDC cross-check as deferred.

**Optional, start-in-parallel if you want it (NOT required):**
- **NFIRS (National Fire Incident Reporting System)** — U.S. Fire Administration / FEMA. The full research microdata usually requires a **request/registration** (still free — not a paid key). It is **supplementary, not load-bearing**: the study is designed to run and produce its result without NFIRS.
  - If you want fire-service data eventually: begin the access request now so it's ready later. Search "USFA NFIRS public data release research" for the current request process.
  - If you don't: do nothing. Claude Code documents the request steps and moves on.

---

## 3. What a "manual fetch" flag looks like (so you recognize it)

If Claude Code hits a source it can't pull autonomously, it will **not** stop the whole run and it will **not** fake the data. It will:
1. Write the exact retrieval steps (URL, query parameters, export format) to `data/raw/MANUAL_FETCH_NEEDED.md`.
2. Note the affected cross-check as *deferred* in `outputs/GATES.md`.
3. Continue with everything that doesn't depend on it.

When the run finishes, check `MANUAL_FETCH_NEEDED.md` — if it's empty, nothing needed you. If it lists something, that's your short to-do, and re-running the relevant phase after you fetch it will fold the data in.

---

## 4. Your pre-run checklist (the whole thing)

- [ ] Nothing to provision — confirmed, no keys/accounts.
- [ ] *(Optional)* Started an NFIRS data request, if you want fire-service data later.
- [ ] That's it. Run Claude Code.

The only hard requirement is that Claude Code can reach the public **CPSC reports**. Everything else either runs on its own or degrades gracefully into a flag for you — never a silent gap, never a fabricated number.
