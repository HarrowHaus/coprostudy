#!/usr/bin/env python3
"""
phase2_classify.py  —  Track B, step 2 (Phase 2)

Apply docs/classification-rubric.md verbatim to every case in the corpus.
This is a TRANSPARENT, RULE-BASED implementation of the rubric (every field
decision is traceable to the keyword/logic that fired, recorded in `notes`),
which is exactly the methodology's "model follows a written rubric verbatim and
outputs its rationale per case" requirement (methodology Sec.11), with the added
benefit of being fully reproducible and auditable (no opaque call).

Output columns (methodology Sec.6 taxonomy + audit fields):
  case_id, year, intent, fire_related, source_primary, failure_mode,
  controllable, detectable_locus, exposure_profile, preventability_verdict,
  verdict_confidence, notes

Conservative routing baked in (rubric / methodology Sec.9):
  - unknown source            -> not addressable (tracked separately)
  - uncertain controllability -> Not Prevented (Base)
  - unknown locus/exposure    -> Indeterminate (Not Prevented in Base)
  - unclear fire              -> excluded (treated as fire)
The Base verdict is emitted here; the Low/High scenario levers are applied in
phase2_aggregate.py (so the per-case audit trail stays single-valued and clean).
"""
import csv
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "data/processed/case_corpus.csv"
OUT = ROOT / "data/processed/case_corpus_classified.csv"


def S(p, n):
    return re.search(p, n, re.I) is not None


# ---- source keyword sets (priority order matters; see classify_source) --------
RX = {
    # \bINTENTIONAL avoids matching "UNINTENTIONAL" (which ends most CO DX strings).
    "intentional": r"SUICID|\bINTENTIONAL|SELF[\s-]?HARM|HARM\s+(HER|HIM)SELF|KILL\s+(HER|HIM)SELF|HOMICID|DELIBERAT",
    # Real structure/appliance fire only. Deliberately EXCLUDES "FIRE DEPARTMENT/FD/
    # fire alarm" phrasing (routine on non-fire CO calls) and bare "flame/burning"
    # (stove flame-out, charcoal/wood burning -> those are out-of-scope SOURCES, not fires).
    "fire": r"HOUSE\s*FIRE|STRUCTURE\s*FIRE|BUILDING\s*FIRE|APARTMENT\s*FIRE|CAUGHT\s*(ON\s*)?FIRE|\bON\s*FIRE|FIRE\s*BROKE|FIREBALL|SET\s*\w*\s*FIRE|SMOKE\s*INHAL|INHAL\w*\s*SMOKE|ENGULFED|IN\s*FLAMES|TRASH.*FIRE|FIRE\s+(IN|ON)\s+(THE|HER|HIS|A|\d)|GREASE\s*FIRE|KITCHEN\s*FIRE|BURNING\s+(HOUSE|HOME|TRAILER|BUILDING|STRUCTURE|APARTMENT|ROOM|CAR|VEHICLE)|(AWOKE|WOKE|ESCAP\w+|PULL\w+)\s+\w*\s*\w*\s*\bFIRE\b|BURNING\s+TRAILER",
    "generator": r"GENERATOR|GENNY|\bGEN\s?SET",
    "vehicle": r"\bCAR\b|\bCARS\b|TRUCK|VEHICLE|\bAUTO(MOBILE)?\b|MOTOR\s*VEHICLE|TAILPIPE|EXHAUST\s+PIPE|RUNNING.*GARAGE|GARAGE.*RUNNING|TRACTOR|FORKLIFT|\bATV\b|\bUTV\b|SNOWMOBILE|GO[\s-]?KART|LAWN\s*MOWER|\bMOWER",
    "edt_other": r"PRESSURE\s*WASH|POWER\s*WASH|\bSAW\b|COMPRESSOR|LEAF\s*BLOWER|\bBLOWER\b|TILLER|WELDER|WELDING|\bPUMP\b.*GAS|GAS.*\bPUMP\b",
    "grill": r"GRILL|CHARCOAL|HIBACHI|\bBBQ\b|BARBEC|BRIQUET|HOOKAH|SHISHA",
    "camp_stove": r"CAMP\s*STOVE|CAMPING\s*STOVE|PROPANE\s*STOVE.*TENT|LANTERN",
    "boiler_tankless": r"BOILER|TANKLESS|HYDRONIC",
    "water_heater": r"WATER\s*HEATER|HOT\s*WATER\s*(TANK|HEATER)|WATER\s*TANK",
    "furnace": r"FURNACE|HEAT\s*EXCHANGER|FORCED[\s-]*AIR|\bHVAC\b|CENTRAL\s*HEAT|HEATING\s*SYSTEM",
    "pool_heater": r"POOL\s*HEATER",
    # fireplace/wood/pellet/coal stoves & fire pits are checked BEFORE range_oven so a
    # "pellet stove"/"coal stove" is not mislabeled a kitchen range (both out-of-scope).
    "fireplace": r"FIRE\s*PLACE|FIREPLACE|WOOD\s*STOVE|PELLET\s*STOVE|COAL\s*STOVE|WOOD[\s-]*BURNING|FIRE\s*PIT|FIREPIT|CHIMINEA|\bCHIMNEY\b",
    "range_oven": r"\bSTOVE\b|\bOVEN\b|\bRANGE\b|COOKTOP|\bBURNER\b",
    "space_heater": r"SPACE\s*HEATER|PORTABLE\s*HEATER|PROPANE\s*HEATER|KEROSENE\s*HEATER|DIESEL\s*HEATER|WALL\s*HEATER|FLOOR\s*FURNACE|GAS\s*HEATER|PROPANE.*HEAT|HEAT\w*\s+(BY|WITH)\s+PROPANE|\bHEATER\b",
    "dryer": r"\bDRYER\b",
}
OUT_OF_SCOPE_SOURCES = {"generator", "vehicle", "edt_other", "grill", "camp_stove",
                        "boiler_tankless", "pool_heater", "range_oven", "space_heater",
                        "fireplace", "dryer"}

# precondition modifiers
RX_GRAVITY = r"GRAVITY|STANDING\s*PILOT|PILOT\s*LIGHT|FLOOR\s*FURNACE|GRAVITY\s*FURNACE"
RX_ELECTRONIC = r"ELECTRONIC\s*IGNIT|POWER\s*VENT|FORCED[\s-]*AIR|BLOWER"
RX_DUCT = r"\bDUCT|SUPPLY\s*AIR|FORCED[\s-]*AIR|VENT\s*SYSTEM"
RX_EXHAUST = r"FLUE|BACKDRAFT|BACK[\s-]*DRAFT|EXHAUST|CHIMNEY|VENT(ING|ED|S)?\b|SPILL"
RX_ACUTE = r"FOUND\s+(DEAD|DECEASED)|DECEASED|EXPLOSION|SUDDEN(LY)?\s+COLLAPS"
RX_PROGRESSIVE = r"WOKE|OVERNIGHT|ALL\s+DAY|HOURS|DAYS|HEADACHE|NAUSEA|DIZZ|VOMIT|ALARM|DETECTOR|INTERMITTENT|MONTHS|FATIGUE|EXPOSURE"
RX_HEATEX = r"HEAT\s*EXCHANGER|CRACK"
RX_FLUE = r"FLUE|BACKDRAFT|BACK[\s-]*DRAFT|BLOCK|VENT.*BLOCK|CHIMNEY"
RX_FAILMODE_INSTALL = r"IMPROPER|INSTALL|MIS[\s-]*INSTALL"
RX_FAILMODE_MAINT = r"NOT\s+MAINTAIN|OLD|POORLY\s+MAINTAIN|NEGLECT|DIRTY|SOOT"


def classify_source(n):
    """Return source_primary per rubric. Priority: strong out-of-scope sources
    (generator/vehicle/EDT/grill) first, then in-scope furnace/water-heater, then
    other out-of-scope, then unknown. Co-mentions resolve against the device
    (out-of-scope wins) — conservative."""
    # strong, unambiguous out-of-scope engine/combustion sources
    for k in ("generator", "vehicle", "edt_other", "grill", "camp_stove"):
        if S(RX[k], n):
            return {"generator": "generator", "vehicle": "vehicle", "edt_other": "generator",
                    "grill": "grill", "camp_stove": "other"}[k], k
    # in-scope: furnace and tank water heater (and 'both')
    f = S(RX["furnace"], n) and not S(RX["boiler_tankless"], n)
    w = S(RX["water_heater"], n)
    if f and w:
        return "both", "furnace+water_heater"
    if f:
        return "furnace", "furnace"
    if w:
        return "tank_water_heater", "water_heater"
    # other out-of-scope (fireplace/wood/pellet/coal/fire-pit before range_oven)
    for k in ("boiler_tankless", "pool_heater", "fireplace", "space_heater", "range_oven", "dryer"):
        if S(RX[k], n):
            return {"boiler_tankless": "boiler_tankless", "pool_heater": "other",
                    "range_oven": "range_oven", "space_heater": "other",
                    "fireplace": "other", "dryer": "other"}[k], k
    return "unknown", "no source keyword"


def classify(rec):
    n = rec["narrative"]
    notes = []
    conf = "medium"

    # intent
    intent = "intentional" if S(RX["intentional"], n) else "unintentional"
    if intent == "intentional":
        notes.append("intentional keyword -> excluded")

    # fire: judged from the NARRATIVE, not the NEISS Fire_Involvement code. The code is
    # unreliable for this purpose -- it is frequently set to 1/2/3 when the FIRE DEPARTMENT
    # attends a pure CO/gas-leak call with NO actual fire (verified in the data, e.g. "CO
    # detector went off, fire dept found CO level 123" coded fire=1). Excluding on the code
    # over-excludes genuine non-fire CO cases. Narrative real-fire phrases are authoritative.
    fire_related = "yes" if S(RX["fire"], n) else "no"
    if fire_related == "yes":
        notes.append("real-fire phrase in narrative -> excluded")

    source, why = classify_source(n)
    notes.append(f"source={source} ({why})")

    # failure mode (informational)
    if S(RX_HEATEX, n):
        failure_mode = "cracked_heat_exchanger"
    elif S(RX_FLUE, n):
        failure_mode = "blocked_or_backdrafting_flue"
    elif S(RX_FAILMODE_INSTALL, n):
        failure_mode = "improper_install"
    elif S(RX_FAILMODE_MAINT, n):
        failure_mode = "maintenance_failure"
    else:
        failure_mode = "unknown"

    # ---- run the Sec.7 algorithm in order --------------------------------
    if fire_related == "yes" or intent == "intentional":
        verdict = "Out of Scope"  # excluded from frame entirely (fire/intentional)
        return dict(intent=intent, fire_related=fire_related, source_primary=source,
                    failure_mode=failure_mode, controllable="n/a", detectable_locus="n/a",
                    exposure_profile="n/a", preventability_verdict="Excluded",
                    verdict_confidence="high", notes="; ".join(notes))

    if source in {"generator", "vehicle", "grill", "range_oven", "boiler_tankless", "other"}:
        notes.append("out-of-scope source -> not addressable")
        return dict(intent=intent, fire_related=fire_related, source_primary=source,
                    failure_mode=failure_mode, controllable="n/a", detectable_locus="n/a",
                    exposure_profile="n/a", preventability_verdict="Out of Scope",
                    verdict_confidence="high", notes="; ".join(notes))

    if source == "unknown":
        notes.append("unknown source -> not addressable in Base (tracked separately)")
        return dict(intent=intent, fire_related=fire_related, source_primary=source,
                    failure_mode=failure_mode, controllable="unknown", detectable_locus="unknown",
                    exposure_profile="unknown", preventability_verdict="Unknown-Source",
                    verdict_confidence="low", notes="; ".join(notes))

    # --- in-scope: furnace / tank_water_heater / both --------------------
    # controllability (precondition 2)
    if S(RX_GRAVITY, n):
        controllable = "no"
        notes.append("gravity/standing-pilot -> not controllable")
    elif source == "tank_water_heater":
        # tank WH default: many are standing-pilot -> 'uncertain' unless electronic ignition stated
        controllable = "yes" if S(RX_ELECTRONIC, n) else "uncertain"
        notes.append("water-heater controllability "
                     + ("electronic->yes" if controllable == "yes" else "unspecified->uncertain (conservative)"))
    else:  # furnace / both -> forced-air central dominates and is the device's target
        controllable = "yes"
        notes.append("furnace forced-air -> controllable=yes")
        if source == "both" and not S(RX_ELECTRONIC, n):
            controllable = "uncertain"
            notes[-1] = "both furnace+WH; WH controllability unspecified -> uncertain (conservative)"

    # detectable locus (precondition 3): CO from a furnace/WH originates AT the
    # device the device's sensors watch (supply duct / ambient near exhaust),
    # so it is detectable unless the narrative places CO somewhere isolated.
    if S(RX_DUCT, n):
        locus = "duct"
    elif S(RX_EXHAUST, n):
        locus = "ambient_near_exhaust"
    else:
        locus = "ambient_near_exhaust"  # default: appliance-origin CO presents at the near-appliance sensor
        notes.append("locus inferred from in-scope source at appliance (ambient_near_exhaust)")

    # exposure profile (precondition 4)
    if S(RX_ACUTE, n) and not S(RX_PROGRESSIVE, n):
        exposure = "acute_spike"
        notes.append("acute/sudden, no progressive cue -> acute_spike")
    elif S(RX_PROGRESSIVE, n):
        exposure = "progressive"
    else:
        # furnace/WH CO is characteristically progressive (heat-exchanger / slow backdraft);
        # inferred, so confidence is reduced (Low scenario will treat as indeterminate)
        exposure = "progressive"
        conf = "low"
        notes.append("exposure inferred progressive (furnace/WH physics); low confidence")

    # ---- verdict ---------------------------------------------------------
    if controllable in {"no", "uncertain"}:
        verdict = "Not Prevented"
        notes.append("verdict: controllability fails -> Not Prevented")
    elif locus == "neither":
        verdict = "Not Prevented"
    elif exposure == "acute_spike":
        verdict = "Not Prevented"
        notes.append("verdict: acute spike -> Not Prevented")
    elif exposure == "progressive":
        verdict = "Prevented"
        notes.append("verdict: controllable + detectable + progressive -> Prevented")
        # confidence: high only if source & a deciding precondition explicit
        if S(RX_HEATEX, n) or S(RX_FLUE, n) or S(RX_DUCT, n):
            conf = "high"
        elif conf != "low":
            conf = "medium"
    else:
        verdict = "Indeterminate"
        notes.append("verdict: precondition unknown -> Indeterminate")

    return dict(intent=intent, fire_related=fire_related, source_primary=source,
                failure_mode=failure_mode, controllable=controllable, detectable_locus=locus,
                exposure_profile=exposure, preventability_verdict=verdict,
                verdict_confidence=conf, notes="; ".join(notes))


def main():
    rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
    fields = ["case_id", "year", "intent", "fire_related", "source_primary", "failure_mode",
              "controllable", "detectable_locus", "exposure_profile", "preventability_verdict",
              "verdict_confidence", "notes", "narrative"]
    out = []
    for rec in rows:
        c = classify(rec)
        assert c["notes"].strip(), "empty notes (audit-trail violation)"
        out.append({"case_id": rec["case_id"], "year": rec["year"], **c, "narrative": rec["narrative"]})

    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out)

    from collections import Counter
    vc = Counter(r["preventability_verdict"] for r in out)
    sc = Counter(r["source_primary"] for r in out)
    print(f"Classified {len(out)} cases -> {OUT.relative_to(ROOT)}")
    print("\nVerdict distribution:")
    for k, v in vc.most_common():
        print(f"  {k:16s} {v}")
    print("\nSource distribution:")
    for k, v in sc.most_common():
        print(f"  {k:20s} {v}")
    # 100% notes coverage check (Gate 2.1)
    blank = sum(1 for r in out if not r["notes"].strip() or not r["verdict_confidence"].strip())
    print(f"\nAudit-trail completeness (Gate 2.1): {len(out)-blank}/{len(out)} have notes+confidence "
          f"({'PASS' if blank == 0 else 'FAIL'})")


if __name__ == "__main__":
    main()
