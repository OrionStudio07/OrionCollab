# Orion Studios — Mandatory Pre-Task Checklist

Every task, no exceptions. @lead runs this before delegating ANY work.
If any item cannot be answered from the spec documents, that is a gray area.
Gray areas require a written plan and user approval before execution.

---

## Checklist

Answer every item explicitly before proceeding:

```
PRE-TASK CHECKLIST
──────────────────
□ 1. Which spec document section covers this task?
       → Quote the section header: ___________________

□ 2. What is the exact class/module name from trd.md?
       → ___________________

□ 3. What lifecycle type is this class?
       → [ ] World Subsystem  [ ] Command Component
         [ ] Actor            [ ] Game Instance  [ ] UMG Widget

□ 4. What CVT base class does this extend (if any)?
       → ___________________

□ 5. Are there any [SPEC] items in trd.md for this not yet read?
       → ___________________

□ 6. What does flow_diagrams.md say happens first for this feature?
       → ___________________

□ 7. Do open questions Q1–Q5 affect this task?
       → [ ] Yes — STOP and flag which ones
         [ ] No — proceed

□ 8. Does this task touch CVT base code?
       → [ ] Yes — STOP, plan surgical extension approach first
         [ ] No — proceed
```

---

## Open Questions Reference

These are unresolved. Any task touching them must STOP and flag:

- **Q1** — Plant 3D Python script access → affects Pipeline B / MetadataLinker
- **Q2** — 2D CAD drawing format (PNG vs PDF) → affects WBP_EquipmentDetails Drawings tab
- **Q3** — Equipment animation type (skeletal vs procedural) → affects ZoneAnimationManager
- **Q4** — NPC character model type (MetaHuman vs Mannequin) → affects NPCManager
- **Q5** — Session recording scope → affects BP_SessionRecorder

Flag format:
```
⚠️ OPEN QUESTION DEPENDENCY
  Question: Q[N] — [description]
  Blocks: [what cannot proceed without this answer]
  Action: Implement placeholder only per AI_EXECUTION_PLAN.md guidance
  Needs: User input before continuing
```

---

## Out-of-Scope Guard

Immediately flag and block any work on these v1 exclusions:

- Mode B — Training mode
- Live Simulation Data
- Thermal / Safety Heatmaps
- Construction Timeline
- Hindi / English Localization content
- Cloud Session Logging
- Standalone Meta Quest APK
- Client Plugin System

Flag format:
```
⛔ OUT OF SCOPE (v1)
  Requested: [description]
  Reason: Listed as out-of-scope in PRD Section "Out of Scope (v1)"
  Architecture prep: [what placeholder exists per the spec]
  Action: Implement placeholder/interface only, not the feature
```

---

## Phase Gate Enforcement

Build order is dependency-locked. Never work out of order.

```
Phase 0 — Foundation
  0.1 CVT Audit → 0.2 C++ Types → 0.3 Config System → 0.4 Data Tables

Phase 1 — Core Architecture  [BLOCKED until Phase 0 gates pass]
  1.1 ModeManager → 1.2 MetadataLinker → 1.3 HierarchyManager → 1.4 TelemetryManager

Phase 2 — Navigation  [BLOCKED until Phase 1 gates pass]
  2.1 CameraSweep → 2.2 TreeBrowser → 2.3 SearchBar → 2.4 Minimap → 2.5 Carousel

Phase 3 — Mode A: Showcase  [BLOCKED until Phase 2 gates pass; streams run parallel]
  Stream A: Xray → Explode → CropBox → Measurement
  Stream B: GuidedTour → NPC System
  Stream C: ZoneAnimation → Lighting

Phase 4 — Mode C: Operations  [BLOCKED until Phase 3 tools complete]
  4.1 EquipmentDetails → 4.2 InspectionManager → 4.3 MaintenanceCallouts → 4.4 P&ID
```

Before starting any phase, verify all gate checks from `AI_EXECUTION_PLAN.md`
for the preceding phase. If gates are incomplete, block work and report what
is missing.

---

## Plan-Before-Execute Format

For any multi-step task, @lead produces this plan and waits for user approval
before delegating:

```
TASK: [task name]
SPEC REFERENCE: [trd.md / prd.md section]

1. [Step] → verify: [exact check]
2. [Step] → verify: [exact check]
3. [Step] → verify: [exact check]

GRAY AREAS: [items needing clarification, or "none"]
AWAITING APPROVAL: yes
```

Do not delegate until the user approves the plan.
